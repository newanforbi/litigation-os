import { describe, expect, it } from "vitest";
import { cases } from "../data/matters";
import { timeline } from "../data/timeline";
import {
  STATUS_LABEL_MAX,
  clampStatusLabel,
  deriveStatusLabel,
  effectiveStatusLabel,
  pickPostureEvent,
  postureEventScore,
} from "./statusLabel";
import type { TimelineEvent } from "../types/portfolio";
import { matterRefsInclude } from "./matterRefs.js";

function eventsFor(matterNumber: number): TimelineEvent[] {
  return timeline.filter((event) => matterRefsInclude(event.matters, matterNumber));
}

describe("statusLabel derivation", () => {
  it("clamps long labels without breaking mid-word when possible", () => {
    const long = "A".repeat(70);
    expect(clampStatusLabel(long).length).toBeLessThanOrEqual(STATUS_LABEL_MAX);
    expect(clampStatusLabel("Short label")).toBe("Short label");
  });

  it("prefers demurrer hearings over earlier reply deadlines", () => {
    // Synthetic future dates — ranking rule only. Do not pin to Matter 20's
    // live calendar (Aug. 28 demurrer was held; that posture is covered below).
    const matter = { number: 20, lifecycle: "active" as const, phase: "demurrer" as const };
    const reply = {
      date: "Nov. 1, 2099",
      event: "AG reply deadline — Matter 20",
      type: "deadline",
      matters: [20],
      upcoming: true,
    } as TimelineEvent;
    const hearing = {
      date: "Nov. 15, 2099",
      event: "Demurrer Hearing — Matter 20",
      type: "hearing",
      matters: [20],
      upcoming: true,
    } as TimelineEvent;
    const events = [reply, hearing];
    expect(pickPostureEvent(events, matter.phase)?.date).toBe("Nov. 15, 2099");
    expect(deriveStatusLabel(matter, { events })).toContain("Nov. 15, 2099");
    expect(deriveStatusLabel(matter, { events })).toMatch(/Demurrer hearing/i);
  });

  it("uses the next live calendar date after a held demurrer hearing", () => {
    const matter = cases.find((item) => item.number === 20)!;
    const events = eventsFor(20);
    expect(matter.status_label).toMatch(/CMC Nov\. 4.*writ brief Nov\. 13.*hearing Jan\. 8/i);
    expect(effectiveStatusLabel(matter, { events })).toMatch(/CMC Nov\. 4.*writ brief Nov\. 13.*hearing Jan\. 8/i);
    // As of Nov. 10, 2026 the Nov. 4 CMC is past, so the next live posture
    // date is the Jan. 8, 2027 hearing (hearings outrank the Nov. 13 brief).
    expect(pickPostureEvent(events, matter.phase)?.date).toBe("Jan. 8, 2027");
  });

  it("derives default prove-up and CMC dates from upcoming hearings", () => {
    // Real portfolio data (both the matter's phase and its timeline events) keeps
    // moving, so pinning this to Matter 12's live record would make the test rot
    // every time its posture changes. Use a fully synthetic matter + event to
    // isolate the "default" phase + hearing → "Default prove-up — <date>"
    // behavior on its own.
    const defaultMatter = { ...cases.find((item) => item.number === 12)!, lifecycle: "active" as const, phase: "default" as const };
    const proveUp = {
      date: "Dec. 1, 2099",
      event: "Default prove-up hearing — Matter 12",
      type: "hearing",
      matters: [12],
      upcoming: true,
    } as TimelineEvent;
    expect(deriveStatusLabel(defaultMatter, { events: [proveUp] })).toBe("Default prove-up — Dec. 1, 2099");
    const cmcMatter = { number: 24, lifecycle: "active" as const, phase: "cmc" as const };
    const cmc = {
      date: "Nov. 15, 2099",
      event: "Initial Case Management Conference — Matter 24",
      type: "hearing",
      matters: [24],
      upcoming: true,
    } as TimelineEvent;
    expect(deriveStatusLabel(cmcMatter, { events: [cmc] })).toMatch(/CMC.*Nov\. 15, 2099/);
  });

  it("pairs served milestones with later CMC / response deadlines", () => {
    // Synthetic — Matter 25's live Aug. 31 FRCP 81(c) date is past and no
    // longer upcoming. Pin the pairing rule so the test does not rot.
    const servedMatter25 = {
      number: 25,
      lifecycle: "active" as const,
      phase: "responsive_deadline" as const,
      serviceTracking: [{ name: "FedEx", served: true, dateServed: "July 24, 2026" }],
    };
    const responseDue25 = {
      date: "Nov. 30, 2099",
      event: "Response due — Matter 25",
      type: "deadline",
      matters: [25],
      upcoming: true,
    } as TimelineEvent;
    expect(deriveStatusLabel(servedMatter25, { events: [responseDue25] })).toBe(
      "Served Jul. 24, 2026 — Response due Nov. 30, 2099",
    );
    // Synthetic — Matter 27's live calendar now includes the Dec. 17 CMC, which
    // outranks the August response date. Pin the pairing rule so the test does
    // not rot when that posture moves.
    const servedMatter = {
      number: 27,
      lifecycle: "active" as const,
      phase: "responsive_deadline" as const,
      serviceTracking: [{ name: "Randstad", served: true, dateServed: "July 30, 2026" }],
    };
    const responseDue = {
      date: "Dec. 15, 2099",
      event: "Response due — Matter 27",
      type: "deadline",
      matters: [27],
      upcoming: true,
    } as TimelineEvent;
    expect(deriveStatusLabel(servedMatter, { events: [responseDue] })).toBe(
      "Served Jul. 30, 2026 — Response due Dec. 15, 2099",
    );
  });

  it("keeps waiting phases from collapsing to an old Filed/Served date", () => {
    // Synthetic fixture — Matter 1 itself was voluntarily dismissed (terminal
    // lifecycle) Aug. 15, 2026, so it can no longer stand in for a live
    // "F&R pending" matter without this test rotting on every posture change.
    const frPendingMatter = { number: 1, lifecycle: "active" as const, phase: "fr_pending" as const };
    const filedEvent = {
      date: "May. 27, 2025",
      event: "Complaint filed",
      type: "filing",
      matters: [1],
      upcoming: false,
    } as TimelineEvent;
    expect(deriveStatusLabel(frPendingMatter, { events: [filedEvent] })).toBe("F&R pending");
    expect(deriveStatusLabel(cases.find((item) => item.number === 19)!, { events: eventsFor(19) })).toBe(
      "Under submission",
    );
  });

  it("uses status_label overrides when present", () => {
    const matter = cases.find((item) => item.number === 1)!;
    expect(matter.status_label).toBeTruthy();
    expect(effectiveStatusLabel(matter, { events: eventsFor(1) })).toBe(matter.status_label);
    expect(deriveStatusLabel(cases.find((item) => item.number === 22)!, { events: eventsFor(22) })).toBe("Settled");
  });

  it("produces an effective label ≤ 60 chars for every matter", () => {
    for (const matter of cases) {
      const label = effectiveStatusLabel(matter, { events: eventsFor(matter.number) });
      expect(label.trim(), `matter ${matter.number}`).not.toBe("");
      expect(label.length, `matter ${matter.number}: ${label}`).toBeLessThanOrEqual(STATUS_LABEL_MAX);
      expect(label, `matter ${matter.number}`).not.toMatch(/\n/);
    }
  });

  it("does not let a contingent SOL deadline make a waiting phase look scheduled", () => {
    // Synthetic fixture for the same reason as above — Matter 1 is now
    // dismissed/terminal and can't exercise the "waiting phase" branch.
    const matter = { number: 1, lifecycle: "active" as const, phase: "fr_pending" as const };
    const filedEvent = {
      date: "May. 27, 2025",
      event: "Complaint filed",
      type: "filing",
      matters: [1],
      upcoming: false,
    } as TimelineEvent;
    const solDeadline = {
      date: "Nov. 1, 2026",
      event: "CCP §335.1 two-year statute of limitations (computed) — Matter 1",
      type: "deadline",
      matters: [1],
      upcoming: true,
    } as TimelineEvent;
    expect(deriveStatusLabel(matter, { events: [filedEvent, solDeadline] })).toBe("F&R pending");
  });

  it("scores meet-and-confer below posture hearings", () => {
    const hearing = {
      date: "Aug. 28, 2026",
      event: "Demurrer Hearing — Matter 20",
      type: "hearing",
      matters: [20],
      upcoming: true,
    } as TimelineEvent;
    const chore = {
      date: "Aug. 21, 2026",
      event: "Meet-and-confer deadline — Matter 20",
      type: "deadline",
      matters: [20],
      upcoming: true,
    } as TimelineEvent;
    expect(postureEventScore(hearing, "demurrer")).toBeGreaterThan(postureEventScore(chore, "demurrer"));
  });
});
