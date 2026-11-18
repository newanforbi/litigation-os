import { describe, expect, it } from "vitest";
import { formatCardCaption, formatCurrency, formatDate, formatMatterPath, formatNumber } from "./formatters";

describe("formatters", () => {
  it("formats whole-dollar currency by default", () => {
    expect(formatCurrency(1234567)).toBe("$1,234,567");
    expect(formatCurrency(0)).toBe("$0");
  });

  it("honours a fraction-digit override, and keeps both variants distinct", () => {
    // Both live in the same cache; a shared instance would leak digits between them.
    expect(formatCurrency(1234.567, 2)).toBe("$1,234.57");
    expect(formatCurrency(1234.567)).toBe("$1,235");
    expect(formatCurrency(1234.567, 2)).toBe("$1,234.57");
  });

  it("formats plain numbers with group separators", () => {
    expect(formatNumber(303)).toBe("303");
    expect(formatNumber(1234567)).toBe("1,234,567");
  });

  it("formats dates from strings and Date objects alike", () => {
    expect(formatDate(new Date(Date.UTC(2026, 7, 8)))).toMatch(/Aug \d, 2026/);
    expect(formatDate("2026-08-08T12:00:00Z")).toMatch(/Aug \d, 2026/);
  });

  it("keeps distinct date option sets distinct across cache hits", () => {
    const date = new Date(Date.UTC(2026, 7, 8, 12));
    const long = formatDate(date, { year: "numeric", month: "long", timeZone: "UTC" });
    const short = formatDate(date, { year: "numeric", month: "short", timeZone: "UTC" });
    expect(long).toBe("August 2026");
    expect(short).toBe("Aug 2026");
    expect(formatDate(date, { year: "numeric", month: "long", timeZone: "UTC" })).toBe(long);
  });

  it("builds matter routes", () => {
    expect(formatMatterPath(7)).toBe("/matters/7");
  });
});

describe("formatCardCaption", () => {
  it("shortens the full plaintiff name to Ngwa Nforbi on matter cards", () => {
    expect(formatCardCaption("Brendan Ngwa Nforbi v. Marriott International, Inc.")).toBe(
      "Ngwa Nforbi v. Marriott International, Inc.",
    );
  });

  it("leaves other captions unchanged", () => {
    expect(formatCardCaption("Newanforbi v. United Parcel Service, Inc.")).toBe(
      "Newanforbi v. United Parcel Service, Inc.",
    );
    expect(formatCardCaption("Ngwa Nforbi v. Example Corp.")).toBe("Ngwa Nforbi v. Example Corp.");
    expect(formatCardCaption("In re Brendan Ngwa Nforbi v. X")).toBe("In re Brendan Ngwa Nforbi v. X");
  });
});

