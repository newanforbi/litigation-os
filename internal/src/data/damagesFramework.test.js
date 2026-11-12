import { describe, it, expect } from "vitest";
import * as mod from "./damagesFramework.js";
const { damagesFramework, frameworkTotals, valuedCases, formatK, FRAMEWORK_DISCLAIMER } = mod;

describe("damagesFramework (public)", () => {
  it("has the 8 framework cases, 6 valued", () => {
    expect(damagesFramework).toHaveLength(8);
    expect(valuedCases).toHaveLength(6);
  });
  it("working-loaded total matches framework v2", () => {
    expect(frameworkTotals.high).toBe(4892213);
    expect(frameworkTotals.low).toBe(2295000);
  });
  it("exposes only public fields", () => {
    const allowed = new Set(["id", "label", "matter", "low", "high", "valuation", "statusOverride", "note"]);
    for (const c of damagesFramework) for (const k of Object.keys(c)) expect(allowed.has(k)).toBe(true);
    expect(Object.keys(mod).sort()).toEqual(["FRAMEWORK_DISCLAIMER", "damagesFramework", "formatK", "frameworkTotals", "valuedCases"]);
  });
  it("rounds to nearest $1K", () => {
    expect(formatK(216000)).toBe("$216K");
    expect(formatK(480918)).toBe("$481K");
    expect(formatK(4892213)).toBe("$4.892M");
    expect(formatK(2295000)).toBe("$2.295M");
    expect(formatK(1072695)).toBe("$1.073M");
  });
  it("carries the disclaimer", () => {
    expect(FRAMEWORK_DISCLAIMER).toMatch(/Not a settlement demand or offer/);
  });
});
