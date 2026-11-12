// Cloudflare Worker: litigation portfolio document + data API.
//
//   GET /health            -> { ok, bucket, d1: { source_commit, seeded_at, age_days, stale } }
//   GET  /doc/<sha256>      -> R2 PDF bytes (application/pdf, ETag passthrough)
//   GET  /doc/<sha256>/meta -> { sha256, size, etag } from R2 HEAD
//   GET  /documents/<path> -> path index (or D1 documents_by_path) -> PDF bytes
//   PUT  /doc/<sha256>      -> upload bytes (rw) + upsert manifest row
//   GET /matters           -> D1 matter rows (mirrors `npm run q listMatters`)
//   GET /matters/<n>       -> one matter + clocks + documents (mirrors getMatter)
//   GET /upcoming?days=14  -> clock rows due within window (mirrors upcomingDeadlines)
//   GET /fuse              -> { fuse, wait, parked } (mirrors getFuseBoard)
//   POST /mcp              -> MCP endpoint (Streamable HTTP, stateless JSON-RPC):
//                             initialize / ping / tools/list / tools/call over the
//                             same read operations. CORS-open so browser-based
//                             MCP clients can call it.
//   GET /.well-known/oauth-authorization-server -> OAuth AS metadata (RFC 8414;
//                             also served under the /mcp path-inserted variant)
//   GET /.well-known/oauth-protected-resource   -> resource metadata (RFC 9728)
//   POST /oauth/register  -> Dynamic Client Registration (RFC 7591)
//   GET|POST /oauth/authorize -> owner-consent page / authorization-code issuance
//   POST /oauth/token     -> code exchange + refresh rotation (PKCE S256 mandatory)
//   POST /admin/reseed     -> guarded D1 re-apply of seed.sql
//                             (Authorization: Bearer <RESEED_SECRET>)
//
// R2 is reached through the DOCS *binding* — this file contains no keys,
// tokens, or secrets. Data routes return 503 { error: "d1_not_provisioned" }
// when the DB binding is absent. GET /doc stays open: every D1-registered
// document is readable without auth except the 14-path denylist. Unregistered
// hashes 404 so the route is not an R2 listing. Token holders can fetch the
// denylist. There is no blanket auth requirement on GET /doc.
//
// No delete route and no cron. Deletes are deliberately not reachable with a
// token (connected assistants hold rw tokens); remove a document or matter
// from the Cloudflare dashboard. The daily deadline digest moved to the
// portfolio-gate Worker, which reads clocks.json on main instead of D1.

import {
  HttpError,
  fuseData,
  getDocObject,
  assertDocVisible,
  getMatterData,
  headDocObject,
  listMattersData,
  upcomingData,
  damagesFrameworkData,
  seedSource,
  sha256ForDocumentPath,
} from "./data.mjs";
import { handleMcp } from "./mcp.mjs";
import { resolveAccess, requireWrite } from "./auth.mjs";
import {
  authorizationServerMetadata,
  protectedResourceMetadata,
  handleRegister,
  handleAuthorizeGet,
  handleAuthorizePost,
  handleToken,
} from "./oauth.mjs";
import {
  putDocBytes,
  recordAudit,
  upsertDocumentRow,
} from "./writes.mjs";
import { contentDispositionForPath } from "./documents.mjs";

const BUCKET = "litigation-documents";

const json = (data, status = 200) =>
  new Response(JSON.stringify(data), {
    status,
    headers: { "content-type": "application/json; charset=utf-8" },
  });

// Run a data-layer op and translate HttpError into its REST response.
// Unexpected exceptions propagate (the runtime turns them into 500s),
// exactly like the pre-refactor worker.
const route = (op) => async (...args) => {
  try {
    return json(await op(...args));
  } catch (e) {
    if (e instanceof HttpError) return json(e.body, e.status);
    throw e;
  }
};

// --- R2 routes --------------------------------------------------------------

const HASH_CACHE = "public, max-age=31536000, immutable";
const PATH_CACHE = "public, max-age=60";

// Hash-addressed bytes are immutable; path-addressed bytes are revalidatable
// (the same court path can be re-filed under a new sha256).
async function serveDoc(env, sha, { cacheControl = HASH_CACHE, disposition } = {}) {
  try {
    const { obj } = await getDocObject(env, sha);
    const headers = new Headers();
    headers.set("content-type", "application/pdf");
    headers.set("cache-control", cacheControl);
    if (disposition) headers.set("content-disposition", disposition);
    if (obj.httpEtag) headers.set("etag", obj.httpEtag);
    if (obj.size != null) headers.set("content-length", String(obj.size));
    return new Response(obj.body, { headers });
  } catch (e) {
    if (e instanceof HttpError) return json(e.body, e.status);
    throw e;
  }
}

// 404 (not 403) for a hash outside the public projection, so an anonymous
// caller cannot probe which private documents exist.
async function visible(env, sha, publicOnly, serve) {
  try {
    await assertDocVisible(env, sha, publicOnly);
  } catch (e) {
    if (e instanceof HttpError) return json(e.body, e.status);
    throw e;
  }
  return serve();
}

async function serveDocumentsPath(env, pathname, publicOnly = false) {
  try {
    const { sha256 } = await sha256ForDocumentPath(env, pathname);
    await assertDocVisible(env, sha256, publicOnly);
    return serveDoc(env, sha256, {
      cacheControl: PATH_CACHE,
      disposition: contentDispositionForPath(pathname),
    });
  } catch (e) {
    if (e instanceof HttpError) return json(e.body, e.status);
    throw e;
  }
}

const docMeta = route(headDocObject);
const listMatters = route(listMattersData);
const getMatter = route((env, n, publicOnly) => getMatterData(env, n, { publicOnly }));
const upcoming = route((env, params) => upcomingData(env, params.get("days")));
const damagesFramework = route(damagesFrameworkData);
const fuse = route((env, params) => fuseData(env, params.get("days")));

// --- admin: D1 self-reseed --------------------------------------------------
// POST /admin/reseed with `Authorization: Bearer <RESEED_SECRET>` and the
// seed.sql text as the body (DELETE + INSERT lines, see seed.mjs).
// Applies the statements to the D1 binding in small batches, so the
// `d1-reseed.yml` workflow can keep D1 in sync with the repo after every
// portfolio-data merge. Fail-closed: 503 when RESEED_SECRET is not
// configured on the Worker, 403 on a Bearer <redacted>
async function handleReseed(request, env) {
  if (!env.RESEED_SECRET) return json({ error: "reseed_not_configured" }, 503);
  const auth = request.headers.get("authorization") || "";
  if (auth !== `Bearer ${env.RESEED_SECRET}`)
    return json({ error: "forbidden" }, 403);
  if (!env.DB) return json({ error: "d1_not_provisioned" }, 503);
  const body = await request.text();
  const statements = body
    .split("\n")
    .map((l) => l.trim())
    // CREATE TABLE IF NOT EXISTS lets a seed add an additive table (meta)
    // without a separate schema step; nothing here can drop or alter one.
    .filter((l) => /^(INSERT|DELETE|CREATE TABLE IF NOT EXISTS)\s/i.test(l));
  let applied = 0;
  for (let i = 0; i < statements.length; i += 50) {
    const chunk = statements.slice(i, i + 50);
    await env.DB.batch(chunk.map((sql) => env.DB.prepare(sql)));
    applied += chunk.length;
  }
  return json({ ok: true, statements: applied });
}

// --- document writes (rw scope) ---------------------------------------------
// PUT /doc/<sha256>?matter=<n>&path=<path>[&verify=false]  body = PDF bytes
//   -> R2 put (sha verified against the key by default) + manifest upsert.
// There is deliberately no DELETE route (see the header comment).
// Bytes live on REST (not MCP) because a PDF over JSON-RPC would be
// base64-bloated and some documents are >20 MB.

async function putDoc(request, env, sha, url, access) {
  try {
    requireWrite(access);
  } catch (e) {
    return json(e.body, e.status);
  }
  try {
    // path is required: it feeds the NOT NULL documents.path column in D1.
    // Validate before reading the body or writing any bytes to R2 so a
    // missing path can never leave orphaned objects behind a 500.
    const pathParam = url.searchParams.get("path");
    if (!pathParam)
      return json(
        { error: "path query param is required (D1 documents.path is NOT NULL)" },
        400,
      );
    const bytes = await request.arrayBuffer();
    const verify = url.searchParams.get("verify") !== "false";
    const matterParam = url.searchParams.get("matter");
    const put = await putDocBytes(env, sha, bytes, { verify });
    const row = await upsertDocumentRow(env, {
      sha256: put.sha256,
      matter_number: matterParam != null && matterParam !== "" ? Number(matterParam) : null,
      path: pathParam,
      size: put.size,
    });
    await recordAudit(env, {
      actor: access.actor,
      action: "putDocument",
      target: put.sha256,
      detail: { matter: matterParam, path: pathParam, size: put.size },
      ok: true,
    });
    return json({ ok: true, ...put, row }, 201);
  } catch (e) {
    if (e instanceof HttpError) {
      await recordAudit(env, {
        actor: access.actor,
        action: "putDocument",
        target: sha,
        detail: { error: e.body },
        ok: false,
      });
      return json(e.body, e.status);
    }
    throw e;
  }
}

// --- entrypoint ---------------------------------------------------------------

export default {
  async fetch(request, env, _ctx) {
    const url = new URL(request.url);
    const path = url.pathname;

    // OAuth 2.1 authorization server (ChatGPT native MCP and friends).
    // Public endpoints, dispatched before the access gate; each one fails
    // closed (503) when D1, the oauth_* tables, or OAUTH_OWNER_KEY is missing.
    if (
      path === "/.well-known/oauth-authorization-server" ||
      path === "/.well-known/oauth-authorization-server/mcp"
    )
      return json(authorizationServerMetadata(url.origin));
    if (
      path === "/.well-known/oauth-protected-resource" ||
      path === "/.well-known/oauth-protected-resource/mcp"
    )
      return json(protectedResourceMetadata(url.origin));
    if (path === "/oauth/register") {
      if (request.method !== "POST") return json({ error: "method_not_allowed" }, 405);
      return handleRegister(request, env);
    }
    if (path === "/oauth/authorize") {
      if (request.method === "GET") return handleAuthorizeGet(request, env, url);
      if (request.method === "POST") return handleAuthorizePost(request, env);
      return json({ error: "method_not_allowed" }, 405);
    }
    if (path === "/oauth/token") {
      if (request.method !== "POST") return json({ error: "method_not_allowed" }, 405);
      return handleToken(request, env);
    }

    if (path === "/mcp") return handleMcp(request, env);

    if (path === "/admin/reseed") {
      if (request.method !== "POST")
        return json({ error: "method_not_allowed" }, 405);
      return handleReseed(request, env);
    }

    const access = await resolveAccess(request, env);
    let m;

    // The mutating document route (PUT) is matched before the GET guard.
    if ((m = path.match(/^\/doc\/([^/]+)$/))) {
      if (request.method === "PUT") return putDoc(request, env, m[1], url, access);
    }

    if (request.method !== "GET") return json({ error: "method_not_allowed" }, 405);

    if (path === "/health")
      return json({ ok: true, bucket: BUCKET, d1: env.DB ? await seedSource(env) : null }); // open

    // Existing Worker lock: API_KEYS without PUBLIC_READ=true 401s every
    // read. That is not a per-document /doc gate. Recommended production
    // is PUBLIC_READ=true so GET /doc stays open except the denylist.
    if (!access.canRead) return json({ error: "unauthorized" }, 401);

    // No token → hide the 14-path denylist. Do not require auth for every /doc.
    const publicOnly = !access.scope;
    if ((m = path.match(/^\/doc\/([^/]+)\/meta$/)))
      return visible(env, m[1], publicOnly, () => docMeta(env, m[1]));
    if ((m = path.match(/^\/doc\/([^/]+)$/)))
      return visible(env, m[1], publicOnly, () => serveDoc(env, m[1]));
    if (path.startsWith("/doc/")) return json({ error: "sha256 must be 64 hex chars" }, 400);

    if (path === "/documents" || path.startsWith("/documents/"))
      return serveDocumentsPath(env, path, publicOnly);

    if (path === "/matters") return listMatters(env);
    if ((m = path.match(/^\/matters\/(\d{1,2})$/)))
      return getMatter(env, Number(m[1]), publicOnly);
    if (path === "/damages-framework") return damagesFramework(env);
    if (path === "/upcoming") return upcoming(env, url.searchParams);
    if (path === "/fuse") return fuse(env, url.searchParams);

    return json({ error: "not_found" }, 404);
  },
};
