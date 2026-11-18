import { describe, expect, it } from "vitest";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { loadMatters, MATTERS_DIR } from "../../scripts/load-matters.mjs";
import { GRAPH_CONTRACT } from "../../scripts/lib/matter-layout.mjs";
import { STATUS_LABEL_MAX } from "../utils/statusLabel";
import {
  PROSE_BUDGETS,
  PROSE_FIELDS,
  PROSE_HINTS,
  docketLogIssues,
  docketLogSignals,
  proseBudgetIssues,
  wordCount,
} from "../utils/proseBudget";
import * as scriptModule from "../../scripts/prose-budget.mjs";

const matters = loadMatters();

describe("prose length budgets", () => {
  it("loads every matter record", () => {
    expect(matters.length).toBe(44);
  });

  it("counts words without being fooled by runs of whitespace", () => {
    expect(wordCount("  one   two\n\nthree ")).toBe(3);
    expect(wordCount("")).toBe(0);
    expect(wordCount(undefined)).toBe(0);
  });

  it("treats prose word counts as a report, not a schema fail, once every matter is split", () => {
    expect(matters.every((m) => m.__layout === "split")).toBe(true);
    expect(GRAPH_CONTRACT.agentOutputCaps).toBe(false);
  });

  it("keeps every leftover legacy prose field under its ceiling", () => {
    const breaches = [];
    for (const matter of matters) {
      if (matter.__layout === "split") continue;
      for (const issue of proseBudgetIssues(matter)) {
        if (issue.level === "over-ceiling") {
          breaches.push(`matter ${matter.number}: ${issue.field} ${issue.words}w > ${issue.ceiling}w`);
        }
      }
    }
    expect(breaches, breaches.join("\n")).toEqual([]);
  });

  it("keeps split identity as records next to an uncapped docket, not a line budget", () => {
    const split = matters.filter((m) => m.__layout === "split");
    expect(split.length).toBeGreaterThan(0);
    for (const matter of split) {
      expect(fs.existsSync(path.join(matter.__sourceDir, "docket.json"))).toBe(true);
      expect(fs.existsSync(path.join(matter.__sourceDir, "events.jsonl"))).toBe(true);
    }
  });

  it("does not put a line ceiling on the docket or the event log", () => {
    expect(GRAPH_CONTRACT.docketLineCeiling).toBeNull();
    expect(GRAPH_CONTRACT.eventsLineCeiling).toBeNull();
    expect(GRAPH_CONTRACT.eventsAppendOnly).toBe(true);
    expect(GRAPH_CONTRACT.inventDocketNumbers).toBe(false);
    expect(GRAPH_CONTRACT.overdueFailsSchema).toBe(false);
    expect(GRAPH_CONTRACT.agentOutputCaps).toBe(false);
    const dir = path.join(MATTERS_DIR, "24");
    const docketLines = fs.readFileSync(path.join(dir, "docket.json"), "utf8").split(/\n/).length;
    const eventLines = fs.readFileSync(path.join(dir, "events.jsonl"), "utf8").split(/\n/).filter(Boolean).length;
    expect(docketLines).toBeGreaterThan(80);
    expect(eventLines).toBeGreaterThan(0);
  });

  it("keeps GRAPH_CONTRACT, schema x-contract, and the UI chip width in lockstep", () => {
    const graphSchema = JSON.parse(
      fs.readFileSync(path.join(path.dirname(fileURLToPath(import.meta.url)), "index/schema.json"), "utf8"),
    );
    const x = graphSchema["x-contract"];
    expect(x.events_append_only).toBe(GRAPH_CONTRACT.eventsAppendOnly);
    expect(x.invent_docket_numbers).toBe(GRAPH_CONTRACT.inventDocketNumbers);
    expect(x.status_label_chars).toBe(GRAPH_CONTRACT.statusLabelChars);
    expect(x.status_label_chars).toBe(STATUS_LABEL_MAX);
    expect(x.docket_line_ceiling).toBeNull();
    expect(x.events_line_ceiling).toBeNull();
    expect(x.overdue_fails_schema).toBe(false);
    expect(x.agent_output_caps).toBe(false);
  });

  it("keeps ceilings above targets for every field", () => {
    for (const field of PROSE_FIELDS) {
      const { target, ceiling } = PROSE_BUDGETS[field];
      expect(ceiling, field).toBeGreaterThanOrEqual(target);
    }
  });

  it("carries an actionable hint for every budgeted field", () => {
    for (const field of PROSE_FIELDS) {
      expect(PROSE_HINTS[field], field).toBeTruthy();
    }
  });

  it("mirrors the script-side budgets used by the validator", () => {
    expect(scriptModule.PROSE_BUDGETS).toEqual(PROSE_BUDGETS);
    expect(scriptModule.PROSE_FIELDS).toEqual(PROSE_FIELDS);
    expect(scriptModule.PROSE_HINTS).toEqual(PROSE_HINTS);
    expect(scriptModule.wordCount("  one   two ")).toBe(wordCount("  one   two "));
    expect(typeof scriptModule.docketLogIssues).toBe("function");
    expect(typeof scriptModule.docketLogSignals).toBe("function");
  });

  it("flags dense docket-log prose and ignores short posture sentences", () => {
    const log =
      "SERVED July 24, 2026 on FedEx. COMPUTED: responsive pleading due August 24, 2026. " +
      "PUNITIVE AMOUNT REVISED — AUGUST 7, 2026: notice executed. SERVICE CONFIRMED July 31, 2026. " +
      "FILING — JULY 28, 2026 completed. ACTION ITEM: serve amended notice before August 31, 2026.";
    expect(docketLogSignals(log).score).toBeGreaterThanOrEqual(2);
    expect(docketLogIssues({ status: log, procedural_status: "Short posture." })).toHaveLength(1);

    const posture =
      "Filed July 15, 2026. Served July 24, 2026; responsive pleading due Aug. 24, 2026.";
    expect(docketLogSignals(posture).score).toBeLessThan(2);
  });
});
