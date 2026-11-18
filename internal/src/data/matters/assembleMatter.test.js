import { describe, expect, it } from "vitest";
import fs from "node:fs";
import path from "node:path";
import { loadMatters, MATTERS_DIR } from "../../../scripts/load-matters.mjs";
import { assembleSplitMatter, GRAPH_CONTRACT } from "./assembleMatter.js";

describe("machine-first matter graph", () => {
  const matters = loadMatters();

  it("covers the whole portfolio from one loader", () => {
    expect(matters.map((m) => m.number)).toEqual([...Array(44)].map((_, i) => i + 1));
  });

  it("keeps Matter 24 split so the first fetch is identity, not the diary", () => {
    const m24 = matters.find((m) => m.number === 24);
    expect(m24.__layout).toBe("split");
    expect(m24.case_no).toBe("3:26-cv-05953-CRB");
    expect(m24.related).toEqual([1, 2, 7, 20, 32, 33]);
    expect(m24.same_incident).toBe("RJ68845");
    const dir = path.join(MATTERS_DIR, "24");
    for (const name of ["matter.json", "docket.json", "clocks.json", "events.jsonl"]) {
      expect(fs.existsSync(path.join(dir, name)), name).toBe(true);
    }
    const clocks = JSON.parse(fs.readFileSync(path.join(dir, "clocks.json"), "utf8"));
    const liveHearing = clocks.find((c) => c.id === "mtd-hearing");
    const vacated = clocks.find((c) => c.id === "mtd-hearing-sep30");
    expect(liveHearing.status).toBe("set");
    expect(liveHearing.date).toBe("2026-12-18");
    expect(liveHearing.time).toBe("10:00");
    expect(liveHearing.source_dkt).toBe(33);
    expect(vacated.status).toBe("vacated");
    const reset = clocks.find((c) => c.id === "mtd-hearing-nov20");
    expect(reset.status).toBe("vacated");
    const docket = JSON.parse(fs.readFileSync(path.join(dir, "docket.json"), "utf8"));
    const fac = docket.find((row) => row.operative === true);
    expect(fac.dkt).toBe(10);
    expect(fac.filed).toBe(true);
    const ask = docket.filter((row) => row.packet === "ask-packet");
    expect(ask.length).toBeGreaterThan(0);
    expect(ask.every((row) => row.superseded_by === "crb-packet")).toBe(true);
    const events = fs.readFileSync(path.join(dir, "events.jsonl"), "utf8").trim().split(/\n/);
    expect(events.every((line) => JSON.parse(line))).toBe(true);
    const identityLines = fs.readFileSync(path.join(dir, "matter.json"), "utf8").split(/\n/).length;
    const docketLines = fs.readFileSync(path.join(dir, "docket.json"), "utf8").split(/\n/).length;
    expect(docketLines).toBeGreaterThan(identityLines);
    expect(GRAPH_CONTRACT.eventsAppendOnly).toBe(true);
    expect(GRAPH_CONTRACT.inventDocketNumbers).toBe(false);
    expect(GRAPH_CONTRACT.docketLineCeiling).toBeNull();
    expect(GRAPH_CONTRACT.eventsLineCeiling).toBeNull();
  });

  it("splits every numbered matter; leftover NN.json is not the layout", () => {
    const leftovers = fs
      .readdirSync(MATTERS_DIR)
      .filter((name) => /^\d{2}\.json$/.test(name));
    expect(leftovers).toEqual([]);
    expect(matters.every((m) => m.__layout === "split")).toBe(true);
    for (const matter of matters) {
      const dir = path.join(MATTERS_DIR, String(matter.number).padStart(2, "0"));
      for (const name of ["matter.json", "docket.json", "clocks.json", "documents.json", "events.jsonl"]) {
        expect(fs.existsSync(path.join(dir, name)), `matter ${matter.number} ${name}`).toBe(true);
      }
    }
  });

  it("keeps Matter 24 docket as pleadings, inventory in documents.json", () => {
    const dir = path.join(MATTERS_DIR, "24");
    const docket = JSON.parse(fs.readFileSync(path.join(dir, "docket.json"), "utf8"));
    const documents = JSON.parse(fs.readFileSync(path.join(dir, "documents.json"), "utf8"));
    expect(docket.length).toBeLessThan(documents.length);
    expect(docket.every((row) => !/\.(jpe?g|png|gif|webp)$/i.test(row.path ?? ""))).toBe(true);
    const assembled = matters.find((m) => m.number === 24);
    expect(assembled.documents.length).toBe(documents.length);
  });

  it("prefers documents.json inventory over docket rows for the SPA file list", () => {
    const assembled = assembleSplitMatter({
      matter: { number: 99, procedural_status: "see clocks" },
      docket: [{ path: "/documents/matter-99/complaint.pdf", filed: true, dkt: 1 }],
      documents: [
        { path: "/documents/matter-99/complaint.pdf", filed: true },
        { path: "/documents/matter-99/mailing.jpg" },
      ],
    });
    expect(assembled.documents).toEqual([
      { path: "/documents/matter-99/complaint.pdf", filed: true },
      { path: "/documents/matter-99/mailing.jpg" },
    ]);
  });

  it("does not fold prose.json into the assembled projection", () => {
    const assembled = assembleSplitMatter({
      matter: {
        number: 99,
        caption: "Test",
        case_no: "x",
        court: "x",
        claims: "x",
        status: "short",
        lifecycle: "active",
        proceeding: "federal_civil",
        phase: "pleadings",
        filed: "x",
        judge: "x",
        cluster: 1,
        type: "Federal",
        archived: false,
        key_facts: "short facts",
        procedural_status: "see clocks",
      },
      docket: [{ path: "/documents/matter-99/a.pdf", filed: true, dkt: 1 }],
      damages: { narrative: "damages", risk: "risk" },
      evidence: [{ id: "e1", what_it_proves: "proof" }],
      claims: { counts: [{ id: 1, title: "Count I", status: "live" }] },
      parties: { defendants_label: "D" },
      prose: { procedural_status: "a thousand-word diary that must not leak" },
    });
    expect(assembled.procedural_status).toBe("see clocks");
    expect(assembled.documents).toEqual([{ path: "/documents/matter-99/a.pdf", filed: true }]);
    expect(assembled.defendants).toBe("D");
  });
});
