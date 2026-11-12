import { useState } from "react";
import { Link } from "react-router";
import { cases, getMatterSummary } from "../data/matters";
import { damages_table, matter_damages } from "../data/damages";
import { coverageForMatter } from "../data/coverage";
import { GOLD } from "../constants";
import { useTheme } from "../ThemeContext";
import { formatCurrency } from "../utils/formatters";
import { formatMatterRefs } from "../utils/matterRefs.js";
import { isArchivedMatter } from "../utils/matterLifecycle";
import { effectiveStatusLabel } from "../utils/statusLabel";
import { HISTORICAL_EXPOSURE_MATTERS, isActiveExposureRow } from "../utils/portfolioStats";

// Prefer the derived posture label over any leftover analytic status prose.
const statusFor = (m) => {
  const summary = getMatterSummary(m.number);
  return summary ? effectiveStatusLabel(summary) : `Matter ${m.number}`;
};

const fmt = (n) => formatCurrency(n);
const VIEWS = ["conservative", "moderate", "aggressive"];

const byNumber = new Map(cases.map((c) => [Number(c.number), c]));
const liveRows = damages_table.filter((row) => isActiveExposureRow(row, byNumber));
const historicalRows = damages_table.filter((row) => !isActiveExposureRow(row, byNumber));

const PORTFOLIO_TOTALS = liveRows.reduce(
  (acc, d) => {
    acc.conservative += d.conservative;
    acc.moderate += d.moderate;
    acc.aggressive += d.aggressive;
    return acc;
  },
  { conservative: 0, moderate: 0, aggressive: 0 }
);

const MAX_PORTFOLIO_AGGRESSIVE = Math.max(0, ...liveRows.map((x) => x.aggressive));

const ARCHIVED_MATTER_NUMS = new Set(cases.filter(c => isArchivedMatter(c)).map(c => c.number));
const ACTIVE_MATTER_DAMAGES = matter_damages.filter(m =>
  !ARCHIVED_MATTER_NUMS.has(m.number) && !HISTORICAL_EXPOSURE_MATTERS.has(m.number)
);

const MATTER_TOTALS = ACTIVE_MATTER_DAMAGES.reduce(
  (acc, m) => {
    acc.conservative += m.conservative;
    acc.moderate += m.moderate;
    acc.aggressive += m.aggressive;
    return acc;
  },
  { conservative: 0, moderate: 0, aggressive: 0 }
);

const MAX_MATTER_AGGRESSIVE = Math.max(
  ...ACTIVE_MATTER_DAMAGES.map(m => m.aggressive)
);

// Risk badge color
const riskColor = (risk = "") => {
  const r = risk.toLowerCase();
  if (r.startsWith("extremely favorable")) return "#34D399";
  if (r.startsWith("favorable")) return "#60A5FA";
  if (r.startsWith("significant")) return "#FBBF24";
  return "#94A3B8";
};

function MatterCard({ m, view, expanded, onToggle, theme }) {
  const total = m[view];
  const pct = (total / MAX_MATTER_AGGRESSIVE) * 100;
  const rc = riskColor(m.risk);
  const coverage = coverageForMatter(m.number);

  return (
    <div style={{
      background: theme.cardBg,
      borderRadius: 10,
      border: `1px solid ${expanded ? GOLD + "60" : theme.cardBorder}`,
      overflow: "hidden",
      transition: "border-color 0.2s"
    }}>
      {/* Header row */}
      <button
        onClick={onToggle}
        style={{
          width: "100%", background: "none", border: "none", cursor: "pointer",
          padding: "16px 20px", textAlign: "left", color: "inherit", font: "inherit"
        }}
      >
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", gap: 12, flexWrap: "wrap" }}>
          <div style={{ flex: 1, minWidth: 0 }}>
            <div style={{ display: "flex", alignItems: "center", gap: 8, flexWrap: "wrap", marginBottom: 3 }}>
              <span style={{
                fontFamily: "'DM Sans', sans-serif", fontSize: 10, fontWeight: 700,
                background: `${GOLD}22`, color: GOLD,
                padding: "2px 7px", borderRadius: 4, letterSpacing: 1, flexShrink: 0
              }}>M{m.number}</span>
              <span style={{
                fontFamily: "'DM Sans', sans-serif", fontSize: 13, fontWeight: 600,
                color: theme.secondaryText
              }}>{m.caption}</span>
            </div>
            <div style={{ display: "flex", gap: 8, flexWrap: "wrap", alignItems: "center" }}>
              <span style={{
                fontFamily: "'DM Sans', sans-serif", fontSize: 10,
                color: theme.subtleText
              }}>{m.court}</span>
              <span style={{ color: theme.subtleText, fontSize: 10 }}>·</span>
              <span style={{
                fontFamily: "'DM Sans', sans-serif", fontSize: 10,
                color: theme.subtleText
              }}>{statusFor(m)}</span>
              {coverage && (
                <>
                  <span style={{ color: theme.subtleText, fontSize: 10 }}>·</span>
                  <span
                    title={`${coverage.carrier} Policy No. ${coverage.policyNo} — ${coverage.insureds.join(" and ")}`}
                    style={{
                      fontFamily: "'DM Sans', sans-serif", fontSize: 10, fontWeight: 700,
                      color: "#34D399", border: "1px solid #34D39940",
                      padding: "1px 7px", borderRadius: 4, letterSpacing: 0.3
                    }}
                  >
                    🏛️ {coverage.limitsShort} insured
                  </span>
                </>
              )}
            </div>
          </div>
          <div style={{ display: "flex", alignItems: "center", gap: 12, flexShrink: 0 }}>
            <div style={{ textAlign: "right" }}>
              <div style={{
                fontFamily: "'DM Sans', sans-serif", fontSize: 18, fontWeight: 700,
                color: "#34D399"
              }}>{fmt(total)}{view === "aggressive" && "+"}</div>
              <div style={{
                fontFamily: "'DM Sans', sans-serif", fontSize: 10,
                color: theme.subtleText, textTransform: "capitalize"
              }}>{view}</div>
            </div>
            <span style={{
              fontFamily: "'DM Sans', sans-serif", fontSize: 14,
              color: theme.subtleText, transition: "transform 0.2s",
              display: "inline-block", transform: expanded ? "rotate(180deg)" : "none"
            }}>▾</span>
          </div>
        </div>

        {/* Progress bar */}
        <div style={{ height: 4, background: theme.barTrack, borderRadius: 2, overflow: "hidden", marginTop: 10 }}>
          <div style={{
            height: "100%", width: `${pct}%`,
            background: `linear-gradient(90deg, ${GOLD}, #34D399)`,
            borderRadius: 2, transition: "width 0.5s ease"
          }} />
        </div>
      </button>

      {/* Expanded detail */}
      {expanded && (
        <div style={{ borderTop: `1px solid ${theme.cardBorder}`, padding: "16px 20px 20px" }}>
          {/* Claims */}
          <div style={{
            fontFamily: "'DM Sans', sans-serif", fontSize: 11,
            color: GOLD, marginBottom: 12, letterSpacing: 0.5
          }}>{m.claims}</div>

          {/* Component table */}
          <div style={{ overflowX: "auto" }}>
            <table style={{ width: "100%", borderCollapse: "collapse" }}>
              <thead>
                <tr>
                  <th style={{ ...thStyle(theme), textAlign: "left" }}>Component</th>
                  <th style={{ ...thStyle(theme), textAlign: "right" }}>Conservative</th>
                  <th style={{ ...thStyle(theme), textAlign: "right" }}>Moderate</th>
                  <th style={{ ...thStyle(theme), textAlign: "right" }}>Aggressive</th>
                </tr>
              </thead>
              <tbody>
                {m.components.map((c, i) => (
                  <tr key={i}>
                    <td style={{ ...tdStyle(theme), color: theme.secondaryText }}>{c.label}</td>
                    <td style={{ ...tdStyle(theme), textAlign: "right", color: "#94A3B8" }}>{fmt(c.conservative)}</td>
                    <td style={{ ...tdStyle(theme), textAlign: "right", color: view === "moderate" ? "#34D399" : "#94A3B8", fontWeight: view === "moderate" ? 600 : 400 }}>{fmt(c.moderate)}</td>
                    <td style={{ ...tdStyle(theme), textAlign: "right", color: view === "aggressive" ? "#34D399" : "#94A3B8", fontWeight: view === "aggressive" ? 600 : 400 }}>{fmt(c.aggressive)}{view === "aggressive" ? "+" : ""}</td>
                  </tr>
                ))}
                {/* Total row */}
                <tr>
                  <td style={{ ...tdStyle(theme), borderTop: `1px solid ${theme.cardBorder}`, fontWeight: 700, color: theme.secondaryText, paddingTop: 10 }}>Total</td>
                  <td style={{ ...tdStyle(theme), borderTop: `1px solid ${theme.cardBorder}`, textAlign: "right", fontWeight: view === "conservative" ? 700 : 400, color: view === "conservative" ? "#34D399" : "#94A3B8", paddingTop: 10 }}>{fmt(m.conservative)}</td>
                  <td style={{ ...tdStyle(theme), borderTop: `1px solid ${theme.cardBorder}`, textAlign: "right", fontWeight: view === "moderate" ? 700 : 400, color: view === "moderate" ? "#34D399" : "#94A3B8", paddingTop: 10 }}>{fmt(m.moderate)}</td>
                  <td style={{ ...tdStyle(theme), borderTop: `1px solid ${theme.cardBorder}`, textAlign: "right", fontWeight: view === "aggressive" ? 700 : 400, color: view === "aggressive" ? "#34D399" : "#94A3B8", paddingTop: 10 }}>{fmt(m.aggressive)}{view === "aggressive" ? "+" : ""}</td>
                </tr>
              </tbody>
            </table>
          </div>

          {/* Risk + settlement notes */}
          <div className="grid-2" style={{ gap: 10, marginTop: 14 }}>
            <div style={{ background: theme.deepBg, borderRadius: 6, padding: "10px 12px" }}>
              <div style={{
                fontFamily: "'DM Sans', sans-serif", fontSize: 9, fontWeight: 700,
                color: rc, letterSpacing: 1.5, textTransform: "uppercase", marginBottom: 5
              }}>Risk Profile</div>
              <div style={{ fontFamily: "'DM Sans', sans-serif", fontSize: 11, color: theme.subtleText, lineHeight: 1.5 }}>{m.risk}</div>
            </div>
            <div style={{ background: theme.deepBg, borderRadius: 6, padding: "10px 12px" }}>
              <div style={{
                fontFamily: "'DM Sans', sans-serif", fontSize: 9, fontWeight: 700,
                color: GOLD, letterSpacing: 1.5, textTransform: "uppercase", marginBottom: 5
              }}>Settlement Note</div>
              <div style={{ fontFamily: "'DM Sans', sans-serif", fontSize: 11, color: theme.subtleText, lineHeight: 1.5 }}>{m.settlement_note}</div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

const thStyle = (theme) => ({
  fontFamily: "'DM Sans', sans-serif", fontSize: 10, fontWeight: 700,
  color: theme.subtleText, textTransform: "uppercase", letterSpacing: 1,
  padding: "0 8px 8px 0", whiteSpace: "nowrap"
});

const tdStyle = (theme) => ({
  fontFamily: "'DM Sans', sans-serif", fontSize: 12,
  padding: "6px 8px 6px 0", borderBottom: `1px solid ${theme.cardBorder}00`
});

export const DamagesTab = ({ damagesView, setDamagesView }) => {
  const theme = useTheme();
  const [dashMode, setDashMode] = useState("portfolio");
  const [expandedMatter, setExpandedMatter] = useState(null);

  const sortedMatters = [...ACTIVE_MATTER_DAMAGES].sort(
    (a, b) => b[damagesView] - a[damagesView]
  );

  const matterTotal = MATTER_TOTALS[damagesView];
  const portfolioTotal = PORTFOLIO_TOTALS[damagesView];

  return (
    <div>
      {/* Title + controls row */}
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 20, flexWrap: "wrap", gap: 12 }}>
        <h2 style={{ fontSize: 24, fontWeight: 700, color: theme.heading, margin: 0 }}>Damages Analysis</h2>
        <Link to="/damages/leverage" style={{ fontSize: 12, fontWeight: 600, color: GOLD }}>8-case exposure ranges →</Link>
        <div style={{ display: "flex", gap: 6, flexWrap: "wrap" }}>
          {/* Mode toggle */}
          {["portfolio", "per matter"].map(mode => (
            <button key={mode} onClick={() => setDashMode(mode)} style={{
              padding: "7px 14px", borderRadius: 6,
              border: dashMode === mode ? `1px solid ${GOLD}` : `1px solid ${theme.filterInactiveBorder}`,
              background: dashMode === mode ? `${GOLD}18` : theme.filterInactiveBg,
              color: dashMode === mode ? GOLD : theme.filterInactiveColor,
              fontFamily: "'DM Sans', sans-serif", fontSize: 11, fontWeight: 700,
              cursor: "pointer", textTransform: "uppercase", letterSpacing: 0.8
            }}>{mode}</button>
          ))}
          <div style={{ width: 1, background: theme.cardBorder, margin: "0 2px" }} />
          {/* Tier toggle */}
          {VIEWS.map(v => (
            <button key={v} onClick={() => setDamagesView(v)} style={{
              padding: "7px 14px", borderRadius: 6,
              border: damagesView === v ? `1px solid ${GOLD}` : `1px solid ${theme.filterInactiveBorder}`,
              background: damagesView === v ? `${GOLD}18` : theme.filterInactiveBg,
              color: damagesView === v ? GOLD : theme.filterInactiveColor,
              fontFamily: "'DM Sans', sans-serif", fontSize: 11, fontWeight: 600,
              cursor: "pointer", textTransform: "capitalize"
            }}>{v}</button>
          ))}
        </div>
      </div>

      {/* ── PORTFOLIO VIEW ── */}
      {dashMode === "portfolio" && (
        <>
          <div style={{ background: theme.aggregateCardBg, borderRadius: 12, padding: 28, border: `1px solid ${GOLD}30`, marginBottom: 24, textAlign: "center" }}>
            <div style={{ fontFamily: "'DM Sans', sans-serif", fontSize: 11, color: GOLD, fontWeight: 700, letterSpacing: 3, textTransform: "uppercase", marginBottom: 8 }}>
              Live Portfolio Exposure — {damagesView}
            </div>
            <div style={{ fontSize: 48, fontWeight: 700, color: theme.aggregateCardText }}>
              {fmt(portfolioTotal)}{damagesView === "aggressive" && <span style={{ fontSize: 28, color: GOLD }}>+</span>}
            </div>
            <div style={{ fontFamily: "'DM Sans', sans-serif", fontSize: 11, color: theme.subtleText, marginTop: 8 }}>
              Litigating matters only · settled/historical valuations (M22, M27) listed separately
            </div>
          </div>

          <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
            {liveRows.map((d, i) => {
              const val = d[damagesView];
              const pct = (val / MAX_PORTFOLIO_AGGRESSIVE) * 100;
              return (
                <div key={i} style={{ background: theme.cardBg, borderRadius: 8, padding: "16px 20px", border: `1px solid ${theme.cardBorder}` }}>
                  <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 8 }}>
                    <div>
                      <span style={{ fontFamily: "'DM Sans', sans-serif", fontSize: 13, fontWeight: 600, color: theme.secondaryText }}>{d.category}</span>
                      <span style={{ fontFamily: "'DM Sans', sans-serif", fontSize: 11, color: theme.subtleText, marginLeft: 10 }}>Matters {formatMatterRefs(d.matters)}</span>
                    </div>
                    <span style={{ fontFamily: "'DM Sans', sans-serif", fontSize: 16, fontWeight: 700, color: "#34D399" }}>
                      {fmt(val)}{damagesView === "aggressive" && "+"}
                    </span>
                  </div>
                  <div style={{ height: 5, background: theme.barTrack, borderRadius: 3, overflow: "hidden" }}>
                    <div style={{ height: "100%", width: `${pct}%`, background: `linear-gradient(90deg, ${GOLD}, #34D399)`, borderRadius: 3, transition: "width 0.6s ease" }} />
                  </div>
                </div>
              );
            })}
          </div>

          {historicalRows.length > 0 && (
            <div style={{ marginTop: 28 }}>
              <div style={{
                fontFamily: "'DM Sans', sans-serif", fontSize: 11, fontWeight: 700,
                letterSpacing: 2, textTransform: "uppercase", color: GOLD, marginBottom: 12,
              }}>Settled / historical valuations — not in the live total</div>
              {historicalRows.map((d, i) => (
                <div key={`hist-${i}`} style={{ background: theme.cardBg, borderRadius: 8, padding: "16px 20px", border: `1px solid ${theme.cardBorder}`, marginBottom: 8 }}>
                  <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                    <div>
                      <span style={{ fontFamily: "'DM Sans', sans-serif", fontSize: 13, fontWeight: 600, color: theme.secondaryText }}>{d.category}</span>
                      <span style={{ fontFamily: "'DM Sans', sans-serif", fontSize: 11, color: theme.subtleText, marginLeft: 10 }}>Matters {formatMatterRefs(d.matters)}</span>
                    </div>
                    <span style={{ fontFamily: "'DM Sans', sans-serif", fontSize: 13, fontWeight: 600, color: theme.mutedText, fontStyle: "italic" }}>
                      Not in live total
                    </span>
                  </div>
                </div>
              ))}
            </div>
          )}

          <div className="grid-3" style={{ marginTop: 24 }}>
            {VIEWS.map(v => {
              const total = PORTFOLIO_TOTALS[v];
              const isActive = v === damagesView;
              return (
                <button key={v} onClick={() => setDamagesView(v)} aria-pressed={isActive} style={{
                  width: "100%", background: isActive ? theme.damagesActiveBg : theme.damagesInactiveBg,
                  borderRadius: 10, padding: 20,
                  border: isActive ? `1px solid ${GOLD}40` : `1px solid ${theme.cardBorder}`,
                  cursor: "pointer", textAlign: "center", transition: "all 0.3s",
                  color: "inherit", font: "inherit", margin: 0
                }}>
                  <div style={{ fontFamily: "'DM Sans', sans-serif", fontSize: 11, color: isActive ? GOLD : theme.subtleText, fontWeight: 700, letterSpacing: 1, textTransform: "uppercase", marginBottom: 8 }}>{v}</div>
                  <div style={{ fontSize: 26, fontWeight: 700, color: isActive ? theme.aggregateCardText : theme.mutedText }}>
                    {fmt(total)}{v === "aggressive" && "+"}
                  </div>
                </button>
              );
            })}
          </div>
        </>
      )}

      {/* ── PER MATTER VIEW ── */}
      {dashMode === "per matter" && (
        <>
          {/* Summary total + disclaimer */}
          <div style={{ background: theme.aggregateCardBg, borderRadius: 12, padding: "20px 28px", border: `1px solid ${GOLD}30`, marginBottom: 16 }}>
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", flexWrap: "wrap", gap: 12 }}>
              <div>
                <div style={{ fontFamily: "'DM Sans', sans-serif", fontSize: 11, color: GOLD, fontWeight: 700, letterSpacing: 3, textTransform: "uppercase", marginBottom: 4 }}>
                  Per-Matter Sum — {damagesView}
                </div>
                <div style={{ fontSize: 36, fontWeight: 700, color: theme.aggregateCardText }}>
                  {fmt(matterTotal)}{damagesView === "aggressive" && <span style={{ fontSize: 22, color: GOLD }}>+</span>}
                </div>
              </div>
              <div style={{ maxWidth: 380 }}>
                <div style={{ fontFamily: "'DM Sans', sans-serif", fontSize: 11, color: theme.subtleText, lineHeight: 1.6 }}>
                  Individual case ceilings before deduplication. Shared economic events
                  (CDL wage loss underlying Matters 1, 2, 7, 15) are counted separately
                  here because each defendant pays independently. Portfolio view
                  ({fmt(portfolioTotal)}) is the single-recovery total.
                </div>
              </div>
            </div>
          </div>

          {/* Tier comparison strip */}
          <div className="grid-3" style={{ gap: 10, marginBottom: 20 }}>
            {VIEWS.map(v => {
              const total = MATTER_TOTALS[v];
              const isActive = v === damagesView;
              return (
                <button key={v} onClick={() => setDamagesView(v)} style={{
                  background: isActive ? theme.damagesActiveBg : theme.damagesInactiveBg,
                  borderRadius: 8, padding: "12px 16px",
                  border: isActive ? `1px solid ${GOLD}40` : `1px solid ${theme.cardBorder}`,
                  cursor: "pointer", textAlign: "center",
                  color: "inherit", font: "inherit", transition: "all 0.2s"
                }}>
                  <div style={{ fontFamily: "'DM Sans', sans-serif", fontSize: 10, color: isActive ? GOLD : theme.subtleText, fontWeight: 700, letterSpacing: 1, textTransform: "uppercase", marginBottom: 4 }}>{v}</div>
                  <div style={{ fontSize: 20, fontWeight: 700, color: isActive ? theme.aggregateCardText : theme.mutedText }}>
                    {fmt(total)}{v === "aggressive" && "+"}
                  </div>
                </button>
              );
            })}
          </div>

          {/* Matter cards sorted by current tier */}
          <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
            {sortedMatters.map(m => (
              <MatterCard
                key={m.number}
                m={m}
                view={damagesView}
                expanded={expandedMatter === m.number}
                onToggle={() => setExpandedMatter(expandedMatter === m.number ? null : m.number)}
                theme={theme}
              />
            ))}
          </div>

          {/* Ranked summary table */}
          <div style={{ background: theme.cardBg, borderRadius: 10, border: `1px solid ${theme.cardBorder}`, padding: "16px 20px", marginTop: 20 }}>
            <div style={{ fontFamily: "'DM Sans', sans-serif", fontSize: 11, fontWeight: 700, color: GOLD, letterSpacing: 2, textTransform: "uppercase", marginBottom: 14 }}>
              Settlement Priority Ranking — {damagesView}
            </div>
            <div style={{ overflowX: "auto" }}>
              <table style={{ width: "100%", borderCollapse: "collapse" }}>
                <thead>
                  <tr>
                    <th style={{ ...thStyle(theme), textAlign: "left" }}>#</th>
                    <th style={{ ...thStyle(theme), textAlign: "left" }}>Matter</th>
                    <th style={{ ...thStyle(theme), textAlign: "right" }}>Conservative</th>
                    <th style={{ ...thStyle(theme), textAlign: "right" }}>Moderate</th>
                    <th style={{ ...thStyle(theme), textAlign: "right" }}>Aggressive</th>
                  </tr>
                </thead>
                <tbody>
                  {sortedMatters.map((m, i) => (
                    <tr key={m.number}>
                      <td style={{ ...tdStyle(theme), color: theme.subtleText }}>{i + 1}</td>
                      <td style={{ ...tdStyle(theme), color: theme.secondaryText }}>
                        <span style={{ color: GOLD, fontWeight: 700, marginRight: 8 }}>M{m.number}</span>
                        {m.caption}
                      </td>
                      <td style={{ ...tdStyle(theme), textAlign: "right", color: damagesView === "conservative" ? "#34D399" : "#94A3B8", fontWeight: damagesView === "conservative" ? 700 : 400 }}>{fmt(m.conservative)}</td>
                      <td style={{ ...tdStyle(theme), textAlign: "right", color: damagesView === "moderate" ? "#34D399" : "#94A3B8", fontWeight: damagesView === "moderate" ? 700 : 400 }}>{fmt(m.moderate)}</td>
                      <td style={{ ...tdStyle(theme), textAlign: "right", color: damagesView === "aggressive" ? "#34D399" : "#94A3B8", fontWeight: damagesView === "aggressive" ? 700 : 400 }}>{fmt(m.aggressive)}+</td>
                    </tr>
                  ))}
                  <tr>
                    <td colSpan={2} style={{ ...tdStyle(theme), borderTop: `1px solid ${theme.cardBorder}`, fontWeight: 700, color: theme.secondaryText, paddingTop: 10 }}>Total (per-matter sum)</td>
                    <td style={{ ...tdStyle(theme), borderTop: `1px solid ${theme.cardBorder}`, textAlign: "right", fontWeight: 700, color: "#94A3B8", paddingTop: 10 }}>{fmt(MATTER_TOTALS.conservative)}</td>
                    <td style={{ ...tdStyle(theme), borderTop: `1px solid ${theme.cardBorder}`, textAlign: "right", fontWeight: 700, color: "#94A3B8", paddingTop: 10 }}>{fmt(MATTER_TOTALS.moderate)}</td>
                    <td style={{ ...tdStyle(theme), borderTop: `1px solid ${theme.cardBorder}`, textAlign: "right", fontWeight: 700, color: "#94A3B8", paddingTop: 10 }}>{fmt(MATTER_TOTALS.aggressive)}+</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </>
      )}
    </div>
  );
};
