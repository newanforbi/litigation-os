import { Link } from "react-router";
import { RangeChart } from "./charts/PortfolioCharts";
import { getMatterSummary } from "../data/matters";
import { damagesFramework, valuedCases, frameworkTotals, formatK, FRAMEWORK_DISCLAIMER } from "../data/damagesFramework";
import { GOLD } from "../constants";
import { useTheme } from "../ThemeContext";
import { effectiveStatusLabel } from "../utils/statusLabel";
import { ROUTES } from "../routes";

const SANS = "'DM Sans', sans-serif";

const statusFor = (c) => {
  if (c.statusOverride) return c.statusOverride;
  const summary = c.matter ? getMatterSummary(c.matter) : undefined;
  return summary ? effectiveStatusLabel(summary) : "—";
};

const rangeText = (c) =>
  c.valuation === "range" ? `${formatK(c.low)}–${formatK(c.high)}` : c.note;

export function DamagesLeverageTab() {
  const theme = useTheme();
  const card = { background: theme.cardBg, border: `1px solid ${theme.cardBorder}`, borderRadius: 10, padding: "16px 18px", marginBottom: 16 };
  const th = { textAlign: "left", padding: "8px 10px", fontSize: 11, letterSpacing: 0.5, textTransform: "uppercase", color: theme.subtleText, borderBottom: `1px solid ${theme.cardBorder}` };
  const td = { padding: "9px 10px", fontSize: 13, color: theme.secondaryText, borderBottom: `1px solid ${theme.cardBorder}` };

  return (
    <section aria-labelledby="leverage-heading" style={{ fontFamily: SANS }}>
      <p style={{ margin: "0 0 6px", fontSize: 12 }}>
        <Link to={ROUTES.damages} style={{ color: GOLD }}>← Damages</Link>
      </p>
      <h2 id="leverage-heading" style={{ color: theme.heading, margin: "0 0 6px", fontSize: 22 }}>Damages exposure — 8-case framework</h2>
      <p role="note" style={{ margin: "0 0 16px", fontSize: 13, color: GOLD, fontWeight: 600 }}>{FRAMEWORK_DISCLAIMER}</p>

      <div style={{ ...card, display: "flex", flexWrap: "wrap", gap: 16, alignItems: "baseline", justifyContent: "space-between" }}>
        <div>
          <div style={{ fontSize: 11, textTransform: "uppercase", letterSpacing: 0.5, color: theme.subtleText }}>Portfolio band ({valuedCases.length} valued cases)</div>
          <div data-testid="portfolio-band" style={{ fontSize: 26, fontWeight: 700, color: "#34D399" }}>{formatK(frameworkTotals.low)}–{formatK(frameworkTotals.high)}</div>
        </div>
        <div style={{ fontSize: 12, color: theme.subtleText }}>Low = expected value · High = working loaded</div>
      </div>

      <div style={{ ...card, overflowX: "auto" }}>
        <h3 style={{ color: theme.heading, fontSize: 15, margin: "0 0 10px" }}>Exposure band by case</h3>
        <RangeChart
          theme={theme}
          valueFmt={formatK}
          rows={[
            ...valuedCases.map((c) => ({ label: c.label, low: c.low, high: c.high })),
            { label: "Portfolio total", low: frameworkTotals.low, high: frameworkTotals.high },
          ]}
        />
      </div>

      <div style={{ ...card, overflowX: "auto" }}>
        <table style={{ width: "100%", borderCollapse: "collapse", minWidth: 420 }}>
          <caption style={{ textAlign: "left", color: theme.heading, fontWeight: 600, fontSize: 15, paddingBottom: 8 }}>Cases</caption>
          <thead><tr><th style={th}>Case</th><th style={th}>Matter</th><th style={th}>Status</th><th style={{ ...th, textAlign: "right" }}>Range</th></tr></thead>
          <tbody>
            {damagesFramework.map((c) => (
              <tr key={c.id}>
                <td style={{ ...td, color: theme.heading, fontWeight: 600 }}>{c.label}</td>
                <td style={td}>{c.matter ? <Link to={`${ROUTES.matters}/${c.matter}`} style={{ color: GOLD }}>M{c.matter}</Link> : "—"}</td>
                <td style={td}>{statusFor(c)}</td>
                <td style={{ ...td, textAlign: "right", fontFamily: "'Courier New', ui-monospace, monospace" }}>{rangeText(c)}</td>
              </tr>
            ))}
            <tr>
              <td style={{ ...td, color: theme.heading, fontWeight: 700 }} colSpan={3}>Portfolio total</td>
              <td style={{ ...td, textAlign: "right", fontWeight: 700, fontFamily: "'Courier New', ui-monospace, monospace" }}>{formatK(frameworkTotals.low)}–{formatK(frameworkTotals.high)}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </section>
  );
}

export default DamagesLeverageTab;
