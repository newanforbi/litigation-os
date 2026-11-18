import { memo } from "react";
import { Link } from "react-router";
import { GOLD, BORDER_BLUE } from "../../constants";
import { StatusBadge, ClusterBadge, TypeBadge, ArchiveBadge, ProceedingBadge, PhaseBadge } from "../Badges";
import { ServiceTracker } from "../ServiceTracker";
import { CollapsibleProse } from "../ui/CollapsibleProse";
import { useMatter } from "../../hooks/useMatter";
import { formatCardCaption, formatMatterPath } from "../../utils/formatters";
import { isArchivedMatter } from "../../utils/matterLifecycle";
import { effectiveStatusLabel } from "../../utils/statusLabel";
import type { MatterSummary, Matter } from "../../types/portfolio";

interface MatterCardProps {
  matter: MatterSummary;
  isOpen: boolean;
  /** Receives the matter number so the list can hold one stable callback for
   *  every card — an inline closure per card would defeat the memo below. */
  onToggle: (matterNumber: number) => void;
}

type RibbonVariant = "settled" | "default" | "dismissed" | "abandoned" | "denied" | "pending" | "timely" | "served";

const RIBBON_STYLES: Record<RibbonVariant, { label: string; background: string; color: string; border?: string }> = {
  settled: { label: "SETTLED", background: "#16a34a", color: "#fff" },
  default: { label: "DEFAULT", background: "#16a34a", color: "#fff" },
  dismissed: { label: "DISMISSED", background: "#dc2626", color: "#fff" },
  abandoned: { label: "ABANDONED", background: "#FFFFFF", color: "#1a1a1a", border: "1px solid #00000022" },
  denied: { label: "DENIED", background: "#6b7280", color: "#fff" },
  pending: { label: "PENDING", background: "#eab308", color: "#1a1a1a" },
  timely: { label: "TIMELY", background: "#0284c7", color: "#fff" },
  served: { label: "SERVED", background: "#0d9488", color: "#fff" },
};

function StatusRibbon({ variant }: { variant: RibbonVariant }) {
  const style = RIBBON_STYLES[variant];
  return (
    <div
      aria-label={style.label}
      style={{
        position: "absolute",
        top: 14,
        right: -28,
        width: 110,
        background: style.background,
        color: style.color,
        border: style.border,
        fontSize: 10,
        fontFamily: "'DM Sans', sans-serif",
        fontWeight: 800,
        letterSpacing: 2,
        textTransform: "uppercase",
        textAlign: "center",
        padding: "5px 0",
        transform: "rotate(45deg)",
        boxShadow: "0 2px 8px rgba(0,0,0,0.35)",
        pointerEvents: "none",
        zIndex: 10,
      }}
    >
      {style.label}
    </div>
  );
}

// badge "NONE" opts a matter out of the status ribbon (and the pending icon)
// without changing its lifecycle — e.g. an unfiled matter that is no longer
// waiting on external timing.
function resolveRibbonVariant(c: MatterSummary & { badge?: string }): RibbonVariant | null {
  if (c.lifecycle === "settled") return "settled";
  if (c.badge === "NONE") return null;
  if (c.badge === "DEFAULT") return "default";
  if (c.lifecycle === "dismissed" || c.badge === "DISMISSED") return "dismissed";
  if (c.lifecycle === "abandoned" || c.badge === "ABANDONED") return "abandoned";
  if (c.badge === "DENIED") return "denied";
  if (c.lifecycle === "pre_filing" || c.badge === "PENDING") return "pending";
  if (c.badge === "TIMELY") return "timely";
  if (c.badge === "SERVED") return "served";
  return null;
}

function MatterCardImpl({ matter: summary, isOpen, onToggle }: MatterCardProps) {
  const { matter: full, status } = useMatter(isOpen ? summary.number : null);
  const c = (full ?? summary) as Matter;
  const proseLoading = isOpen && status === "loading";
  const showPending = c.badge !== "NONE" && (c.lifecycle === "pre_filing" || c.badge === "PENDING");
  const ribbonVariant = resolveRibbonVariant(c);

  return (
    <div
      className="matter-card"
      style={{
        position: "relative",
        background: "var(--card-bg)",
        borderRadius: 10,
        border: isOpen ? `1px solid ${GOLD}40` : "1px solid var(--card-border)",
        overflow: "hidden",
        transition: "border-color 0.3s",
      }}
    >
      {ribbonVariant && <StatusRibbon variant={ribbonVariant} />}

      {/* Header row */}
      <button
        onClick={() => onToggle(c.number)}
        aria-expanded={isOpen}
        aria-controls={`matter-detail-${c.number}`}
        className="matter-card-header"
      >
        <div className="matter-card-number" style={{ background: "var(--navy-subtle-bg)" }}>{c.number}</div>
        <div className="matter-card-title-wrap">
          <div className="matter-card-caption" style={{ color: "var(--heading)" }} title={c.caption}>{formatCardCaption(c.caption)}</div>
          <div className="matter-card-meta" style={{ color: "var(--subtle-text)" }}>{c.case_no} · {c.court}</div>
        </div>
        <div className="matter-card-badges">
          <div className="matter-card-badge-row">
            <ClusterBadge cluster={c.cluster} />
            <TypeBadge type={c.type} />
            <ProceedingBadge proceeding={c.proceeding} />
            <PhaseBadge phase={c.phase} />
            <StatusBadge status={effectiveStatusLabel(c)} lifecycle={c.lifecycle} />
            {isArchivedMatter(c) && <ArchiveBadge />}
          </div>
          {c.note && (
            <div className="matter-card-note" style={{ color: "var(--secondary-text)" }}>
              {showPending ? "⏳" : "📌"} {c.note}
            </div>
          )}
        </div>
        <div aria-hidden="true" className="matter-card-chevron" style={{ color: "var(--subtle-text)", transform: isOpen ? "rotate(180deg)" : "rotate(0)" }}>▾</div>
      </button>

      {/* Expanded detail */}
      {isOpen && (
        <div id={`matter-detail-${c.number}`} className="matter-card-detail" style={{ borderTop: "1px solid var(--card-border)" }}>
          <div className="grid-2" style={{ paddingTop: 18 }}>
            <div>
              <div className="detail-label">Defendants</div>
              <p className="detail-copy" style={{ color: "var(--secondary-text)" }}>{c.defendants}</p>
            </div>
            <div>
              <div className="detail-label">Judge</div>
              <p className="detail-copy" style={{ color: "var(--secondary-text)", margin: "0 0 12px" }}>{c.judge}</p>
              <div className="detail-label">Filed</div>
              <p className="detail-copy" style={{ color: "var(--secondary-text)", margin: 0 }}>{c.filed}</p>
            </div>
          </div>

          <div style={{ marginTop: 18 }}>
            <div className="detail-label">Causes of Action</div>
            <div className="matter-card-pills">
              {(c.causes ?? []).map((ca, i) => (
                <span key={i} className="matter-card-pill" style={{ background: "var(--navy-subtle-bg)", color: "var(--secondary-text)", border: `1px solid ${BORDER_BLUE}30` }}>{ca}</span>
              ))}
            </div>
          </div>

          {proseLoading ? (
            <div className="matter-card-loading" style={{ color: "var(--subtle-text)" }}>Loading full matter record…</div>
          ) : (
            <>
              {c.key_facts ? (
                <div style={{ marginTop: 18 }}>
                  <div className="detail-label">Key Facts</div>
                  <CollapsibleProse text={c.key_facts} label="key facts" style={{ color: "var(--muted-text)", lineHeight: 1.7 }} />
                </div>
              ) : null}

              {(c.procedural_status || c.damages || c.risk) ? (
                <div className="grid-2" style={{ marginTop: 18 }}>
                  {c.procedural_status ? (
                    <div>
                      <div className="detail-label">Procedural Status</div>
                      <CollapsibleProse text={c.procedural_status} label="procedural status" style={{ color: "var(--muted-text)", lineHeight: 1.6 }} />
                    </div>
                  ) : null}
                  {(c.damages || c.risk) ? (
                    <div>
                      {c.damages ? (
                        <>
                          <div className="detail-label">Estimated Damages</div>
                          <p className="detail-copy" style={{ color: "#34D399", fontSize: 15, fontWeight: 700, margin: "0 0 12px" }}>{c.damages}</p>
                        </>
                      ) : null}
                      {c.risk ? (
                        <>
                          <div className="detail-label">Risk / Defense Notes</div>
                          <CollapsibleProse text={c.risk} label="risk notes" style={{ color: "#F59E0B", lineHeight: 1.6 }} />
                        </>
                      ) : null}
                    </div>
                  ) : null}
                </div>
              ) : null}

              {c.evidence?.length ? (
                <div style={{ marginTop: 18 }}>
                  <div className="detail-label">Key Evidence</div>
                  <div className="matter-card-pills">
                    {c.evidence.map((ev, i) => (
                      <span key={i} className="matter-card-pill" style={{ background: "var(--cluster-pill-bg)", color: "var(--cluster-pill-color)", border: "1px solid var(--cluster-pill-border)" }}>{ev}</span>
                    ))}
                  </div>
                </div>
              ) : null}
            </>
          )}

          {c.serviceTracking && <ServiceTracker serviceTracking={c.serviceTracking} />}

          <div className="matter-card-link">
            <Link to={formatMatterPath(c.number)} style={{ color: GOLD }}>
              Open dedicated matter page →
            </Link>
          </div>
        </div>
      )}
    </div>
  );
}

/** Expanding one card used to re-render every matter, each re-deriving its
 *  status badge. Only the two cards whose isOpen actually flipped re-render now. */
export const MatterCard = memo(MatterCardImpl);
