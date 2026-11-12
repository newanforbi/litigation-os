// Public "8-case framework" (v2) — illustrative damages exposure RANGES ONLY.
//
// low  = expected value (EV), approximate
// high = working loaded figure
//
// PUBLIC FILE. Never add probabilities, demands, target/settlement ranges,
// line items, insurance floors, or settlement notes here. Negotiation data
// stays in damages.js / internal/private/negotiation, which this file does
// not import. Display rounds to the nearest $1K.
//
// matter: portfolio matter number the employer maps to (summaries.json);
// status for display is derived from that matter at render time unless
// statusOverride is set.

export const FRAMEWORK_DISCLAIMER =
  "Illustrative damages exposure ranges (expected value to working loaded). Not a settlement demand or offer.";

/** @type {{ id: string, label: string, matter: number | null, low: number | null, high: number | null, valuation: "range" | "contingent" | "none", statusOverride?: string, note?: string }[]} */
export const damagesFramework = [
  { id: "amazon", label: "Amazon", matter: 29, low: 216000, high: 480918, valuation: "range" },
  { id: "ups", label: "UPS", matter: 26, low: 720000, high: 1108194, valuation: "range" },
  { id: "home-depot", label: "Home Depot", matter: 37, low: 483000, high: 1072695, valuation: "range" },
  { id: "best-buy", label: "Best Buy", matter: 39, low: 529000, high: 1510242, valuation: "range", statusOverride: "Pre-filing" },
  { id: "att", label: "AT&T", matter: 36, low: 111000, high: 247400, valuation: "range" },
  { id: "fedex", label: "FedEx", matter: 25, low: 236000, high: 472764, valuation: "range" },
  { id: "staples", label: "Staples", matter: 42, low: null, high: null, valuation: "contingent", note: "Contingent, not valued" },
  { id: "accurate", label: "Accurate (background-check vendor)", matter: 29, low: null, high: null, valuation: "none", note: "No standalone range" },
];

export const valuedCases = damagesFramework.filter((c) => c.valuation === "range");

export const frameworkTotals = valuedCases.reduce(
  (acc, c) => ({ low: acc.low + c.low, high: acc.high + c.high }),
  { low: 0, high: 0 }
);

/** Round to the nearest $1K: $216K, and $1.108M for >= $1M (still $1K precision). */
export function formatK(value) {
  const k = Math.round(value / 1000);
  if (k >= 1000) return `$${Math.floor(k / 1000)}.${String(k % 1000).padStart(3, "0")}M`;
  return `$${k}K`;
}
