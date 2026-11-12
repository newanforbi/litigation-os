import { documentsKeyFromUrl, sha256ForPath } from "./documents.mjs";
import { CLOSED_CLOCK_SQL, isClosedClockStatus } from "../../../internal/scripts/lib/clock-status.mjs";
import { todayKey } from "../../../internal/scripts/lib/next-actions.mjs";
import { nextFromClocks } from "../../../internal/scripts/lib/upcoming-from-clocks.mjs";
import {
  filterPublicDocuments,
  isPrivateDocument,
} from "../../../internal/scripts/lib/private-documents.mjs";

// Shared data layer for the litigation-doc-api Worker: R2 + D1 access and
// the portfolio query operations. Used by the REST routes (index.mjs) and
// the MCP endpoint (mcp.mjs).
//
// No request/response handling here — functions return plain data and throw
// HttpError on HTTP-mapped failures (400/404/503). Callers translate those
// into their own transport (REST JSON or MCP JSON-RPC errors).
//
// R2 is reached through the DOCS *binding* and D1 through the DB *binding* —
// this file contains no keys, tokens, or secrets.

export const BUCKET = "litigation-documents";
export const HEX64 = /^[0-9a-fA-F]{64}$/;

export class HttpError extends Error {
  constructor(status, body) {
    super(body && body.error ? String(body.error) : `http_${status}`);
    this.status = status;
    this.body = body;
  }
}

export const keyForSha256 = (sha) => `sha256/${sha.slice(0, 2)}/${sha.slice(2)}.pdf`;
export const keyForSha256Text = (sha) => {
  const c = String(sha ?? "").toLowerCase();
  return `text/${c.slice(0, 2)}/${c.slice(2)}.txt`;
};
// Court deadlines are California dates. UTC flipped "today" to tomorrow at
// 5 pm Pacific, so evening overdue flags were a day early.
export const portfolioToday = () => todayKey();
export const addDays = (key, n) => {
  const d = new Date(`${key}T12:00:00Z`);
  d.setUTCDate(d.getUTCDate() + n);
  return d.toISOString().slice(0, 10);
};

// Clamp a day-window parameter the same way the REST routes always have.
export function parseDays(value, fallback = 14) {
  let days = Number(value ?? fallback);
  if (!Number.isFinite(days)) days = fallback;
  return Math.min(90, Math.max(1, Math.round(days)));
}

// Clock statuses that no longer count as "upcoming". Canonical stored list is
// open | set | contingent | vacated | satisfied (clock-status.mjs). SQL also
// excludes unmigrated retired/cancelled/canceled aliases (treated as vacated).
// The D1 clocks table may predate the status column — every query that filters
// on it falls back to the unfiltered form when the column is absent.
const isClosedStatus = isClosedClockStatus;
const noStatusColumn = (e) => /no such column/i.test(e?.message ?? "");

function cleanSha(sha) {
  const c = String(sha ?? "").toLowerCase();
  if (!HEX64.test(c)) throw new HttpError(400, { error: "sha256 must be 64 hex chars" });
  return c;
}

// --- R2 ---------------------------------------------------------------------

export function r2Ready(env) {
  return !!env.DOCS;
}

// Resolves to { sha256, obj } where obj is the R2 object (has .body,
// .httpEtag, .size). Throws 503 when unbound, 400 on a bad hash, 404 when
// the key is absent.
export async function getDocObject(env, sha) {
  if (!r2Ready(env)) throw new HttpError(503, { error: "r2_not_bound" });
  const clean = cleanSha(sha);
  const obj = await env.DOCS.get(keyForSha256(clean));
  if (!obj) throw new HttpError(404, { error: "not_found", sha256: clean });
  return { sha256: clean, obj };
}

export async function headDocObject(env, sha) {
  if (!r2Ready(env)) throw new HttpError(503, { error: "r2_not_bound" });
  const clean = cleanSha(sha);
  const head = await env.DOCS.head(keyForSha256(clean));
  if (!head) throw new HttpError(404, { error: "not_found", sha256: clean });
  return { sha256: clean, size: head.size ?? null, etag: head.httpEtag ?? null };
}

// Reads the pre-extracted text sidecar for one PDF: text/<first2>/<rest>.txt
// (poppler `pdftotext -layout`, written by internal/scripts/extract-doc-text.mjs
// and kept in sync by internal/scripts/r2-upload.mjs; an empty file means the
// PDF had no text layer). Returns a paginated slice so agents read document
// contents as tool results instead of fetching PDF bytes over HTTP.
// Throws 503 when unbound, 400 on a bad hash, 404 when no sidecar exists yet.
export async function getDocText(env, sha, offset = 0, limit = 20000) {
  if (!r2Ready(env)) throw new HttpError(503, { error: "r2_not_bound" });
  const clean = cleanSha(sha);
  const obj = await env.DOCS.get(keyForSha256Text(clean));
  if (!obj) throw new HttpError(404, { error: "text_not_extracted", sha256: clean });
  const text = await obj.text();
  const total = text.length;
  const start = Math.min(Math.max(0, Math.trunc(Number(offset) || 0)), total);
  const len = Math.min(Math.max(1, Math.trunc(Number(limit) || 20000)), 100000);
  const slice = text.slice(start, start + len);
  return {
    sha256: clean,
    total_chars: total,
    offset: start,
    limit: len,
    returned_chars: slice.length,
    truncated: start + slice.length < total,
    text: slice,
  };
}

// --- D1 ---------------------------------------------------------------------

async function dbAll(env, sql, params = []) {
  if (!env.DB) return null;
  try {
    const res = await env.DB.prepare(sql).bind(...params).all();
    return res.results ?? [];
  } catch (e) {
    // Binding exists but our schema was never applied (e.g. fresh local D1).
    if (/no such table/i.test(e?.message ?? "")) return null;
    throw e;
  }
}

// Null (no DB / no schema) becomes the standard 503; callers get rows.
function needDb(rows) {
  if (!rows) throw new HttpError(503, { error: "d1_not_provisioned" });
  return rows;
}

// Every matter's next clock, computed from the clocks table with the repo's
// own nextFromClocks() — the same rule index/matters.json uses. The stored
// matters.next_clock_* columns are not read: they are a denormalized copy
// that went stale between reseeds and that write tools could edit.
async function nextClocksByMatter(env, today) {
  let rows;
  try {
    rows = await dbAll(env, `SELECT matter_number, title, date, kind, status FROM clocks`);
  } catch (e) {
    if (!noStatusColumn(e)) throw e;
    rows = await dbAll(env, `SELECT matter_number, title, date, kind FROM clocks`);
  }
  const byMatter = new Map();
  for (const r of rows ?? []) {
    const list = byMatter.get(r.matter_number) ?? [];
    list.push({ title: r.title, date: r.date, kind: r.kind, status: r.status ?? "open" });
    byMatter.set(r.matter_number, list);
  }
  const next = new Map();
  for (const [n, list] of byMatter) next.set(n, nextFromClocks(list, today));
  return next;
}

const slimClock = (today, r, next) => {
  const nc = next?.next_clock ?? null;
  return {
    number: r.number,
    caption: r.caption,
    lifecycle: r.lifecycle,
    overdue: Boolean(next?.overdue),
    date: nc?.date ?? null,
    kind: nc?.kind ?? null,
    title: nc?.title ?? null,
  };
};

const slimMatter = (today, r, next) => {
  const nc = next?.next_clock ?? null;
  return {
    number: r.number,
    caption: r.caption,
    case_no: r.case_no,
    court: r.court,
    phase: r.phase,
    lifecycle: r.lifecycle,
    status_label: r.status_label,
    judge: r.judge,
    overdue: r.lifecycle === "active" && Boolean(next?.overdue),
    next_clock: nc?.date ? { date: nc.date, title: nc.title } : null,
  };
};

// Which commit of main D1 was seeded from (written by seed.mjs into `meta`).
// Null when the table predates this field; callers report that as unknown.
export async function seedSource(env, now = Date.now()) {
  let rows = null;
  try {
    rows = await dbAll(env, `SELECT key, value FROM meta`);
  } catch {
    rows = null;
  }
  const meta = Object.fromEntries((rows ?? []).map((r) => [r.key, r.value]));
  if (!meta.source_commit) return { source_commit: null, seeded_at: null, age_days: null, stale: true };
  const age = meta.seeded_at ? Math.floor((now - Date.parse(meta.seeded_at)) / 86_400_000) : null;
  return {
    source_commit: meta.source_commit,
    seeded_at: meta.seeded_at ?? null,
    age_days: age,
    // A reseed per merge is the goal; past a day the projection is suspect.
    stale: age == null || age >= 1,
  };
}

// Mirrors `npm run q listMatters`.
export async function listMattersData(env) {
  const rows = needDb(
    await dbAll(
      env,
      `SELECT number, caption, case_no, court, phase, lifecycle, status_label,
              judge
       FROM matters ORDER BY number`,
    ),
  );
  const today = portfolioToday();
  const next = await nextClocksByMatter(env, today);
  return rows.map((r) => slimMatter(today, r, next.get(r.number)));
}

// Mirrors getMatter: identity + clocks + document manifest rows.
// Throws 404 when the matter number is unknown.
// --- public vs. authenticated document visibility -----------------------------
// Owner rule (2026-10-14): every D1-registered document is public except the
// 14-path denylist in private-documents.mjs (HOPE_000* discovery + two
// matter-12 card-authorization PDFs). Anonymous callers see the full
// `documents` catalog minus that set; a private hash or path is a plain 404
// so its existence is not revealed. Token holders (r or rw) see everything.
// There is no blanket auth requirement on GET /doc. New uploads default
// public unless their path or sha256 matches the denylist.

async function rowsForSha(env, sha) {
  const fromDocs =
    (await dbAll(env, `SELECT sha256, path, size, matter_number FROM documents WHERE sha256 = ?`, [sha])) ?? [];
  const fromPath =
    (await dbAll(
      env,
      `SELECT sha256, path, size, matter_number FROM documents_by_path WHERE sha256 = ?`,
      [sha],
    )) ?? [];
  return [...fromDocs, ...fromPath];
}

export async function loadDocumentRows(env, { matter, publicOnly = false } = {}) {
  const params = [];
  let where = "";
  if (Number.isInteger(matter)) {
    where = " WHERE matter_number = ?";
    params.push(matter);
  }
  const fromDocs = await dbAll(
    env,
    `SELECT sha256, path, size, matter_number FROM documents${where} ORDER BY path`,
    params,
  );
  const fromPath = await dbAll(
    env,
    `SELECT sha256, path, size, matter_number FROM documents_by_path${where} ORDER BY path`,
    params,
  );
  if (!fromDocs && !fromPath) return null;
  const byKey = new Map();
  for (const row of [...(fromDocs ?? []), ...(fromPath ?? [])]) {
    const key = `${row.path ?? ""}::${String(row.sha256 ?? "").toLowerCase()}`;
    if (!byKey.has(key)) byKey.set(key, row);
  }
  let rows = [...byKey.values()].sort((a, b) => String(a.path ?? "").localeCompare(String(b.path ?? "")));
  if (publicOnly) rows = filterPublicDocuments(rows);
  return rows;
}

export async function assertDocVisible(env, sha, publicOnly) {
  const clean = String(sha ?? "").toLowerCase();
  if (!HEX64.test(clean)) throw new HttpError(400, { error: "sha256 must be 64 hex chars" });
  const rows = await rowsForSha(env, clean);
  const privateHit = (rows ?? []).some((r) => isPrivateDocument(r)) || isPrivateDocument({ sha256: clean });
  if (privateHit) {
    if (publicOnly) throw new HttpError(404, { error: "not_found", sha256: clean });
    return;
  }
  if (!publicOnly) return;
  // Anonymous: registered in D1 and not denylisted. Unregistered hashes 404
  // so the open /doc route does not become an R2 bucket listing.
  if (!rows?.length) throw new HttpError(404, { error: "not_found", sha256: clean });
}

export async function getMatterData(env, n, { publicOnly = false } = {}) {
  const rows = needDb(
    await dbAll(
      env,
      `SELECT number, caption, case_no, court, phase, lifecycle, status_label,
              judge
       FROM matters WHERE number = ?`,
      [n],
    ),
  );
  if (!rows.length) throw new HttpError(404, { error: "not_found", matter: n });
  const r = rows[0];
  const today = portfolioToday();
  let clocks;
  try {
    clocks =
      (await dbAll(
        env,
        `SELECT title, date, kind, status FROM clocks WHERE matter_number = ? ORDER BY date`,
        [n],
      )) ?? [];
  } catch (e) {
    if (!noStatusColumn(e)) throw e;
    clocks =
      (await dbAll(
        env,
        `SELECT title, date, kind FROM clocks WHERE matter_number = ? ORDER BY date`,
        [n],
      )) ?? [];
  }
  const documents = needDb(await loadDocumentRows(env, { matter: n, publicOnly }));
  return {
    ...slimMatter(today, r, nextFromClocks(clocks.map((c) => ({ ...c, status: c.status ?? "open" })), today)),
    clocks: clocks.map((c) => ({
      title: c.title,
      date: c.date,
      kind: c.kind,
      status: c.status ?? null,
      overdue: !!c.date && c.date < today && !isClosedStatus(c.status),
    })),
    documents,
    document_count: documents.length,
  };
}

// Mirrors upcomingDeadlines: clock rows due within the window (days, clamped
// 1..90), oldest first, including overdue ones.
export async function upcomingData(env, days) {
  const window = parseDays(days);
  const today = portfolioToday();
  const horizon = addDays(today, window);
  let rows;
  try {
    rows = await dbAll(
      env,
      `SELECT c.matter_number AS number, c.title, c.date, c.kind,
              m.caption, m.lifecycle
       FROM clocks c JOIN matters m ON m.number = c.matter_number
       WHERE c.date <= ?
         AND lower(ifnull(c.status, 'open')) NOT IN ${CLOSED_CLOCK_SQL}
       ORDER BY c.date, c.matter_number`,
      [horizon],
    );
  } catch (e) {
    if (!noStatusColumn(e)) throw e;
    rows = await dbAll(
      env,
      `SELECT c.matter_number AS number, c.title, c.date, c.kind,
              m.caption, m.lifecycle
       FROM clocks c JOIN matters m ON m.number = c.matter_number
       WHERE c.date <= ? ORDER BY c.date, c.matter_number`,
      [horizon],
    );
  }
  rows = needDb(rows);
  return rows.map((r) => ({
    number: r.number,
    caption: r.caption,
    lifecycle: r.lifecycle,
    overdue: !!r.date && r.date < today,
    date: r.date,
    kind: r.kind,
    title: r.title,
  }));
}

export const PATH_INDEX_KEY = "index/path-to-sha256.json";

// Path -> sha256 for GET /documents/<path>: the R2 path index first, then the
// D1 documents_by_path table (path is the identity — one sha256 can live
// under many court paths), then the legacy sha256-PK documents table.
// Throws 404 { error: "not_found", path } when nothing has the path.
export async function sha256ForDocumentPath(env, pathname) {
  const docPath = documentsKeyFromUrl(pathname);
  if (r2Ready(env)) {
    try {
      const obj = await env.DOCS.get(PATH_INDEX_KEY);
      const sha = sha256ForPath(obj ? await obj.json().catch(() => null) : null, pathname);
      if (sha) return { sha256: sha, path: docPath };
    } catch {
      // fall through to D1
    }
  }
  if (env.DB) {
    const byPath = await dbAll(env, `SELECT sha256 FROM documents_by_path WHERE path = ?`, [docPath]);
    let hit = byPath?.[0]?.sha256;
    if (!hit) {
      const legacy = await dbAll(env, `SELECT sha256 FROM documents WHERE path = ?`, [docPath]);
      hit = legacy?.[0]?.sha256;
    }
    if (typeof hit === "string" && hit) return { sha256: hit.toLowerCase(), path: docPath };
  }
  throw new HttpError(404, { error: "not_found", path: docPath });
}

// Mirrors getFuseBoard: { fuse, wait, parked } partitioned off the folded
// next_clock, exactly like the REST /fuse route.
export async function fuseData(env, days) {
  const window = parseDays(days);
  const today = portfolioToday();
  const horizon = addDays(today, window);
  const rows = needDb(
    await dbAll(
      env,
      `SELECT number, caption, lifecycle FROM matters`,
    ),
  );
  const next = await nextClocksByMatter(env, today);
  const slim = rows.map((r) => slimClock(today, r, next.get(r.number)));
  const fuseRows = slim
    .filter((m) => m.lifecycle === "active" && m.date && (m.overdue || m.date <= horizon))
    .sort((a, b) => a.date.localeCompare(b.date) || a.number - b.number);
  const inFuse = new Set(fuseRows.map((m) => m.number));
  const wait = slim
    .filter((m) => m.lifecycle === "active" && !inFuse.has(m.number))
    .sort(
      (a, b) => (a.date ?? "9999").localeCompare(b.date ?? "9999") || a.number - b.number,
    );
  const parked = slim
    .filter((m) => m.lifecycle === "pre_filing")
    .sort((a, b) => a.number - b.number);
  return { generated: today, today, horizon, source: await seedSource(env), fuse: fuseRows, wait, parked };
}

// Escape LIKE metacharacters so the query is a literal substring match.
const escapeLike = (s) => String(s).replace(/[\\%_]/g, (c) => `\\${c}`);

function ftsQuery(raw) {
  // Quote each alphanumeric token so MATCH is literal, not a boolean trap.
  const tokens = String(raw)
    .toLowerCase()
    .match(/[a-z0-9]{2,}/g);
  if (!tokens?.length) return null;
  return tokens.map((t) => `"${t.replaceAll('"', "")}"`).join(" AND ");
}

function mapSearchRow(r) {
  return {
    sha256: r.sha256,
    matter_number: r.matter_number,
    matter_caption: r.caption ?? r.matter_caption ?? null,
    path: r.path,
    size: r.size,
    ...(r.snippet ? { snippet: r.snippet } : {}),
  };
}

// Full-text search: D1 FTS5 over extracted PDF text when `documents_fts`
// exists (populated by documents:sync). Falls back to a path/caption LIKE
// substring — the historical behavior — so an un-migrated D1 still works.
// FTS5 is the right index here: docket strings, statute numbers, and party
// names are keyword lookups; Vectorize would need a second product, an
// embedding pipeline, and still lose exact-token precision. Anonymous
// callers never see denylisted rows.
export async function searchDocumentsData(env, query, limit = 20, { publicOnly = false } = {}) {
  const q = String(query ?? "").trim();
  if (!q) throw new HttpError(400, { error: "query must be a non-empty string" });
  let n = Number(limit ?? 20);
  if (!Number.isFinite(n)) n = 20;
  n = Math.min(100, Math.max(1, Math.round(n)));

  const match = ftsQuery(q);
  if (match) {
    try {
      const fts = await dbAll(
        env,
        `SELECT d.sha256, d.matter_number, d.path, d.size, m.caption,
                snippet(documents_fts, 2, '', '', '…', 32) AS snippet
         FROM documents_fts
         JOIN documents d ON d.sha256 = documents_fts.sha256
         LEFT JOIN matters m ON m.number = d.matter_number
         WHERE documents_fts MATCH ?
         LIMIT ?`,
        [match, n * 3],
      );
      if (fts) {
        const rows = publicOnly ? filterPublicDocuments(fts) : fts;
        return rows.slice(0, n).map(mapSearchRow);
      }
    } catch (e) {
      if (!/no such table/i.test(e?.message ?? "")) throw e;
    }
  }

  const like = `%${escapeLike(q)}%`;
  const rows = needDb(
    await dbAll(
      env,
      `SELECT d.sha256, d.matter_number, d.path, d.size, m.caption
       FROM documents d LEFT JOIN matters m ON m.number = d.matter_number
       WHERE d.path LIKE ? ESCAPE '\\' OR m.caption LIKE ? ESCAPE '\\'
       ORDER BY d.path LIMIT ?`,
      [like, like, n * 3],
    ),
  );
  const visible = publicOnly ? filterPublicDocuments(rows) : rows;
  return visible.slice(0, n).map(mapSearchRow);
}

export async function listDocumentsData(env, { matter, limit = 100, offset = 0, publicOnly = false } = {}) {
  let n = Number(limit ?? 100);
  if (!Number.isFinite(n)) n = 100;
  n = Math.min(500, Math.max(1, Math.round(n)));
  let off = Number(offset ?? 0);
  if (!Number.isFinite(off) || off < 0) off = 0;
  const matterNum =
    matter === undefined || matter === null ? undefined : Number(matter);
  if (matter !== undefined && matter !== null && !Number.isInteger(matterNum)) {
    throw new HttpError(400, { error: "matter must be an integer matter number" });
  }
  const rows = needDb(
    await loadDocumentRows(env, {
      matter: Number.isInteger(matterNum) ? matterNum : undefined,
      publicOnly,
    }),
  );
  return {
    total: rows.length,
    offset: off,
    limit: n,
    documents: rows.slice(off, off + n),
  };
}

// Public 8-case damages framework (ranges only). Read-only; 503 until
// migrations/0001_damages_framework.sql is applied.
export async function damagesFrameworkData(env) {
  const rows = needDb(
    await dbAll(
      env,
      `SELECT id, label, matter_number, low_usd, high_usd, valuation, status_override, note
       FROM damages_framework ORDER BY sort`,
    ),
  );
  const valued = rows.filter((r) => r.valuation === "range");
  return {
    disclaimer:
      "Illustrative damages exposure ranges (expected value to working loaded). Not a settlement demand or offer.",
    cases: rows,
    total: {
      low_usd: valued.reduce((a, r) => a + (r.low_usd ?? 0), 0),
      high_usd: valued.reduce((a, r) => a + (r.high_usd ?? 0), 0),
    },
  };
}
