/**
 * Signature quality gate — keeps the Aug 26 house-scan plate dead and
 * pins the live November 2026 445×106 wet-ink stamp.
 *
 * Asserts:
 *  - house source JPG and v3 bbox crop are absent
 *  - canonical PNG is 445×106 (not the 5544×820 v2 photo-loops archive)
 *  - retired extract-signature-scan.py exits non-zero
 */
import { spawnSync } from "node:child_process";
import { existsSync, readFileSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { describe, expect, it } from "vitest";

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../..");
const SIG = path.join(ROOT, "internal/assets/signature");
const SCRIPTS = path.join(ROOT, "internal/scripts");

function pngSize(p) {
  const buf = readFileSync(p);
  if (buf.subarray(0, 8).toString("binary") !== "\x89PNG\r\n\x1a\n") {
    throw new Error(`Not a PNG: ${p}`);
  }
  return { width: buf.readUInt32BE(16), height: buf.readUInt32BE(20) };
}

describe("canonical signature (445×106 wet-ink, not house)", () => {
  it("does not keep the wet-ink / house assets on disk", () => {
    expect(
      existsSync(path.join(SIG, "brendan-newanforbi-signature-source.jpg")),
    ).toBe(false);
    expect(
      existsSync(path.join(SIG, "brendan-newanforbi-signature-v3-bbox-crop.png")),
    ).toBe(false);
  });

  it("keeps the live stamp at 445×106, distinct from the v2 archive", () => {
    const canonical = path.join(SIG, "brendan-newanforbi-signature.png");
    const v2 = path.join(SIG, "brendan-newanforbi-signature-v2-photo-loops.png");
    expect(existsSync(canonical)).toBe(true);
    expect(existsSync(v2)).toBe(true);
    expect(pngSize(canonical)).toEqual({ width: 445, height: 106 });
    expect(pngSize(v2)).toEqual({ width: 5544, height: 820 });
  });

  it("passes the Python pixel quality gate", () => {
    const r = spawnSync(
      "python3",
      [
        "-c",
        "import sys; sys.path.insert(0,'internal/scripts/lib'); "
        + "from signature_quality import assert_canonical_stamp, assert_house_assets_gone; "
        + "assert_house_assets_gone(); assert_canonical_stamp(); print('ok')",
      ],
      { cwd: ROOT, encoding: "utf8" },
    );
    expect(r.status, r.stderr || r.stdout).toBe(0);
    expect(r.stdout).toContain("ok");
  });

  it("refuses to run the retired wet-scan extractor", () => {
    const r = spawnSync(
      "python3",
      [path.join(SCRIPTS, "extract-signature-scan.py")],
      { cwd: ROOT, encoding: "utf8" },
    );
    expect(r.status).not.toBe(0);
    expect((r.stderr || "") + (r.stdout || "")).toMatch(/retired|house/i);
  });
});
