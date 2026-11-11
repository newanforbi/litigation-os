import summaries from "./matters/summaries.json" with { type: "json" };
import { withMatterIdentity } from "./matterIdentity.js";
import { summarizeLawyerFees, withDerivedCost } from "./lawyerFeeMath.js";

// Ground-truth lawyer-fee estimate for the portfolio.
// Hours are classified by document type and priced per docs/LAWYER_FEES_CALCULATOR.md.
// Cost, cluster rollups, and portfolio totals are derived from those hours
// (lawyerFeeMath.js) so they cannot drift. Matter identity (caption / case_no /
// court) joins from matter JSON via matterIdentity.js. `type` here is a fee-tab
// claim shorthand and may differ from matter.type by design.
const lawyer_fees_raw = [
  {
    number: 1,
    type: "Federal - 42 U.S.C. 1983 (4th/14th Amend., Monell)",
    documentsCount: 25,
    totalPagesReal: 116,
    hours: {
      low: 49.4,
      high: 88.2,
      mid: 68.8
    },
    cost: {
      low: 13832,
      high: 24696,
      mid: 19264
    },
    notes: "Real page counts are far smaller than a naive filename-based guess would suggest (116 total pages, not 1,000+); the MTD briefing cycle is genuinely modest in length. Opposing-party filings (CHP's MTD, AG's Reply) are billed only at a light review rate, not drafting rate. True-up increment: Notice of Change of Address and a Notice of Supplemental Authority (Serrato Order) were present on disk but not previously counted; billed at flat administrative rates."
  },
  {
    number: 2,
    type: "State - False Imprisonment, Battery, Bane Act",
    documentsCount: 16,
    totalPagesReal: 111,
    hours: {
      low: 68.4,
      high: 116.6,
      mid: 92.5
    },
    cost: {
      low: 19152,
      high: 32648,
      mid: 25900
    },
    notes: "Parallel state action tied to Matter 1; heaviest real cost driver is the 15-page complaint plus the Ex Parte Application and U-Visa reply briefing, not the shared discovery/evidence set."
  },
  {
    number: 3,
    type: "Federal",
    documentsCount: 26,
    totalPagesReal: 290,
    hours: {
      low: 190.8,
      high: 351.6,
      mid: 271.2
    },
    cost: {
      low: 53424,
      high: 98448,
      mid: 75936
    },
    notes: "Ground-truth PDFs (290 total pages across 26 files) show a much smaller record than the 664-pg complaint/685-pg MTQ referenced in the prior LAWYER_FEES_CALCULATOR.md draft — no such files exist in public/documents/matter-03; that figure appears to be a stale/incorrect prior estimate and was disregarded in favor of actual pdfinfo counts. Two documents listed in matters.js (PalaciosMTD_Doc24.pdf, Opposition_PalaciosMTD.pdf) are referenced but not present in the uploaded folder and were excluded from the page/hour tally; their substance is effectively captured by 'SLB MTD.pdf' and 'SLB Opposition to MTD.pdf', which are counted."
  },
  {
    number: 4,
    type: "State",
    documentsCount: 0,
    totalPagesReal: 0,
    hours: {
      low: 41.5,
      high: 94,
      mid: 67.75
    },
    cost: {
      low: 11620,
      high: 26320,
      mid: 18970
    },
    notes: "No documents folder exists for this matter (empty array in ground-truth extraction) — a complaint was filed (05/29/2026) and the case is confirmed real (Gov. Claim filed Feb. 2026, deemed rejected ~Apr. 2026) but voluntarily dismissed before any filing was uploaded to the portfolio site. Estimated conservatively as a moderate-length state complaint plus a Government Claim, given the matter never proceeded to motion practice or discovery."
  },
  {
    number: 5,
    type: "State",
    documentsCount: 38,
    totalPagesReal: 833,
    hours: {
      low: 422.1,
      high: 687.8,
      mid: 554.95
    },
    cost: {
      low: 118188,
      high: 192584,
      mid: 155386
    },
    notes: "Largest matter in this batch by real page count (833 pages across 38 files) — driven mainly by heavy bilateral discovery (377 pp) and two large Requests for Judicial Notice (222 pp combined). The prior 712-page 'CASOMB Complaint' estimate in LAWYER_FEES_CALCULATOR.md does not match the actual file (38 real pages); real pdfinfo counts were used throughout. Matters.js notes that 12 underlying discovery-production PDFs (defendants' document production) were removed from the public repository after review and are correctly absent from both the ground-truth JSON and this cost estimate. True-up increment: the Order Sustaining Demurrer to FAC (court order, light review only), a duplicate Tentative Ruling text file, and other previously uncounted administrative pages were added at light review/admin rates, not drafting rate."
  },
  {
    number: 6,
    type: "Federal",
    documentsCount: 4,
    totalPagesReal: 101,
    hours: {
      low: 193,
      high: 292,
      mid: 242.5
    },
    cost: {
      low: 54040,
      high: 81760,
      mid: 67900
    },
    notes: "Voluntarily dismissed one day after the sole defense appearance (Notice of Related Cases), before any answer or MSJ — so nearly all billable work is the two complaints themselves (96 pages total), not motion practice. A Minute Order PDF referenced in matters.js is not present in the uploaded folder and was excluded from the tally (immaterial — court orders are not billable attorney drafting time in any event)."
  },
  {
    number: 7,
    type: "Federal - 42 U.S.C. 1983 Procedural Due Process (structural bias, DMV APS)",
    documentsCount: 17,
    totalPagesReal: 185,
    hours: {
      low: 185.1,
      high: 289.4,
      mid: 237.25
    },
    cost: {
      low: 51828,
      high: 81032,
      mid: 66430
    },
    notes: "Highest-cost matter in the cluster because it contains two real complaint drafts (60p original + 31p FAC) totaling 91 pages of genuine pleading work; this is a defensible, non-inflated result since the original complaint is billed once at full rate and the FAC only at a reduced amendment rate. True-up increment: a Notice of Supplemental Authority (Serrato Order) present on disk but not previously counted, billed at a flat administrative rate."
  },
  {
    number: 8,
    type: "State - Writ of Administrative Mandate (CCP 1094.5)",
    documentsCount: 2,
    totalPagesReal: 88,
    hours: {
      low: 50.5,
      high: 81,
      mid: 65.75
    },
    cost: {
      low: 14140,
      high: 22680,
      mid: 18410
    },
    notes: "Single-document matter (writ petition); cost driven entirely by the flat specialized-writ rate, consistent with the 5-count 1094.5 causes of action asserted."
  },
  {
    number: 9,
    type: "Writ of Mandate (CCP §1085)",
    documentsCount: 9,
    totalPagesReal: 179,
    hours: {
      low: 65,
      high: 116,
      mid: 90.5
    },
    cost: {
      low: 18200,
      high: 32480,
      mid: 25340
    },
    notes: "Challenges CDCR's discharge-review denial (Form 1502-DR errors, wrong legal standard). AG's demurrer prompted a petitioner opposition (not present as a separate uploaded file) and an AG reply (present but not billable — opposing counsel's work). Estimate is conservative: it excludes the AG's own filing and treats voluminous notice/administrative bundles as flat per-document tasks rather than per-page briefing."
  },
  {
    number: 10,
    type: "Habeas Corpus (PC §3008(d)(2); 15 CCR §3574) — Treatment Termination",
    documentsCount: 2,
    totalPagesReal: 3,
    hours: {
      low: 40.5,
      high: 72,
      mid: 56.25
    },
    cost: {
      low: 11340,
      high: 20160,
      mid: 15750
    },
    notes: "Only 2 files sit in this matter's public folder (a notice and the court's denial order); the underlying petition PDF was never uploaded to the portfolio site. Because the case record independently establishes the petition was drafted, filed, and adjudicated on exhaustion grounds (PC §3008(d)(2) certification requirement), the estimate credits the standard habeas-drafting range rather than reporting a near-zero cost that would understate real work performed."
  },
  {
    number: 11,
    type: "Federal",
    documentsCount: 0,
    totalPagesReal: 0,
    hours: {
      low: 30.5,
      high: 76,
      mid: 53.25
    },
    cost: {
      low: 8540,
      high: 21280,
      mid: 14910
    },
    notes: "Filed 03/02/2026 and voluntarily dismissed with prejudice 06/29/2026 before any defendant answered or moved — case never reached motion practice or discovery. Estimated conservatively as a single-issue equitable-relief-only complaint (declaratory/injunctive, no damages claim) plus a short dismissal notice; no uploaded documents exist to verify actual length."
  },
  {
    number: 12,
    type: "State — Consumer Fraud / UCL",
    documentsCount: 20,
    totalPagesReal: 188,
    hours: {
      low: 151,
      high: 247,
      mid: 199
    },
    cost: {
      low: 42280,
      high: 69160,
      mid: 55720
    },
    notes: "Active case with a real 34-page amended complaint and a substantial 58-page default judgment packet already on file, so the fee estimate here is meaningfully higher than a generic 'early-stage/light filing' guess — the underlying documents show genuine substantive drafting work, not just a bare-bones complaint. Increment: 6-page CM-110 Case Management Statement (filed Jul. 20, 2026), billed as a flat administrative filing plus a short sworn declaration (Attachment 4b itemizing the $78,671.20 default judgment prove-up), not per-page drafting rate; a 2-page formal POS-010 Proof of Service for Alpine Truck Sales (Levying Officer File No. 2026002577) — a duplicate confirmation of the already-tracked July 1, 2026 service, billed at a nominal administrative rate; and a 49-page Alpine Default Judgment Packet, now a complete self-contained filing record: 3-page CIV-100 Request for Entry of Default/Court Judgment (flat administrative-filing rate), a 7-page supporting Declaration developing the derivative successor-liability/alter-ego theory (motion-brief-adjacent rate given the legal research and case citations required), and 39 pages of exhibits and exhibit covers (Exhibits 1–10) reattached from the Diamond prove-up package — billed at a nominal clerical/compilation rate since this is a duplicate of exhibits already fully priced once under the original Diamond packet, not fresh evidentiary drafting."
  },
  {
    number: 13,
    type: "Federal",
    documentsCount: 0,
    totalPagesReal: 0,
    hours: {
      low: 30.5,
      high: 76,
      mid: 53.25
    },
    cost: {
      low: 8540,
      high: 21280,
      mid: 14910
    },
    notes: "Filed 01/22/2026 and voluntarily dismissed with prejudice 06/29/2026 before any defendant answered or moved — same early-dismissal pattern as Matter 11. Estimated conservatively as a single-issue federal complaint plus a short dismissal notice; no uploaded documents exist to verify actual length."
  },
  {
    number: 14,
    type: "State",
    documentsCount: 1,
    totalPagesReal: 28,
    hours: {
      low: 70,
      high: 95,
      mid: 82.5
    },
    cost: {
      low: 19600,
      high: 26600,
      mid: 23100
    },
    notes: "Single 28-page combined writ/complaint filed June 30, 2026 and voluntarily dismissed shortly after; no motion practice occurred, so the estimate reflects drafting/research/filing only."
  },
  {
    number: 15,
    type: "State",
    documentsCount: 19,
    totalPagesReal: 448,
    hours: {
      low: 300.5,
      high: 419.5,
      mid: 360
    },
    cost: {
      low: 84140,
      high: 117460,
      mid: 100800
    },
    notes: "Largest matter in this batch (448 real pages, 19 files). Multiple complaint versions reflect genuine post-demurrer recalibration (companion Macomber mandate case, Matter 19/9, received an adverse tentative ruling that forced a damages-only rewrite) rather than pure duplication. The two ~110-page files were billed at evidence-compilation, not complaint, rates specifically to keep the estimate defensible rather than inflated. True-up increment: a meet-and-confer calendar invite and a minor administrative filing present on disk but not previously counted, billed at flat administrative rates."
  },
  {
    number: 16,
    type: "State",
    documentsCount: 1,
    totalPagesReal: 32,
    hours: {
      low: 64,
      high: 80,
      mid: 72
    },
    cost: {
      low: 17920,
      high: 22400,
      mid: 20160
    },
    notes: "Single 32-page complaint filed July 7, 2026, voluntarily dismissed; no further filings appear in the record."
  },
  {
    number: 17,
    type: "Federal",
    documentsCount: 0,
    totalPagesReal: 0,
    hours: {
      low: 56,
      high: 80,
      mid: 68
    },
    cost: {
      low: 15680,
      high: 22400,
      mid: 19040
    },
    notes: "No documents folder exists for this matter (empty in source data). Conservative estimate limited to complaint + minimal ancillary filings, since the case was voluntarily dismissed with prejudice before any defendant answered or filed a motion."
  },
  {
    number: 18,
    type: "Federal",
    documentsCount: 0,
    totalPagesReal: 0,
    hours: {
      low: 55,
      high: 75,
      mid: 65
    },
    cost: {
      low: 15400,
      high: 21000,
      mid: 18200
    },
    notes: "No documents folder exists for this matter. Estimate reflects a prisoner civil-rights complaint plus minor PLRA-related procedural filings before an early, self-executing voluntary dismissal with prejudice."
  },
  {
    number: 19,
    type: "Habeas Corpus — Immediate Discharge from Parole (Pen. Code §1473; PC §§3000, 3001, 3008(d)(2); 15 CCR §3574)",
    documentsCount: 4,
    totalPagesReal: 72,
    hours: {
      low: 43,
      high: 77,
      mid: 60
    },
    cost: {
      low: 12040,
      high: 21560,
      mid: 16800
    },
    notes: "Companion matter to Matters 9, 10, and 11 (same administrative record); targets the parole term itself rather than treatment compulsion. The 67-page petition is unusually dense for a habeas filing (5 causes of action, 6 exhibits, extensive regulatory/case-law analysis re: In re Gadlin, In re Leman, ACSOL v. Macomber), justifying the top of the 40-70 hr specialized-habeas range. True-up: Notice of Change of Address (admin) plus HC-004 Notice and Request for Ruling packet prepared Aug. 7, 2026 — only the HC-004 cover pages are new billable work (petition pages inside the packet are the same 67 pp. already counted; billed at flat administrative/form-fill rate, not habeas redraft)."
  },
  {
    number: 20,
    type: "State - Writ of Mandate (CCP 1085, PC 679.10 U-Visa Certification)",
    documentsCount: 44,
    totalPagesReal: 576,
    hours: {
      low: 84.8,
      high: 145.9,
      mid: 115.35
    },
    cost: {
      low: 23744,
      high: 40852,
      mid: 32298
    },
    notes: "Record now lives under matter-32/from-20/. Aug. 31 true-up: clerk-served 8-page notice-of-entry copy of the Aug. 29 Whitman order (6-page order already billed; +2 CES/mailing pages) plus the 1-page Dept. 25 EPOST email, billed at court-order/admin review, not drafting. Sheriff packets and individual-respondent oppositions stay at compilation rates. Aug. 28 true-up of the tentative and replies carries forward."
  },
  {
    number: 21,
    type: "Federal",
    documentsCount: 2,
    totalPagesReal: 21,
    hours: {
      low: 28.5,
      high: 42.5,
      mid: 35.5
    },
    cost: {
      low: 7980,
      high: 11900,
      mid: 9940
    },
    notes: "Only the complaint itself is billable drafting work; the folder also contains a 12-page CSK order (Barocio-related) present on disk but not previously counted — billed at a light review-only rate since court orders are not billable attorney drafting time. Case was voluntarily dismissed with prejudice before any defendant answered or moved, so no motion practice is billed."
  },
  {
    number: 22,
    type: "State — PC §290.46(j) / FCRA / ICRAA / UCL / Wrongful Termination",
    documentsCount: 8,
    totalPagesReal: 45,
    hours: {
      low: 63,
      high: 103.5,
      mid: 83.25
    },
    cost: {
      low: 17640,
      high: 28980,
      mid: 23310
    },
    notes: "Light litigation footprint by design: a complaint was drafted and filed, but the matter settled via demand letter and negotiation before service was even completed, so no answer, motion practice, or discovery ever occurred — billed accordingly at pre-litigation/negotiation intensity rather than full federal-style motion practice. True-up increment: the process server's Invoice and Signed Proof of Service (POS-010), relocated into this folder during an earlier cleanup, was present on disk but not previously counted — billed at evidence/exhibit rate."
  },
  {
    number: 23,
    type: "State — PC §290.46(j) / FCRA / ICRAA / UCL / Wrongful Termination (contemplated)",
    documentsCount: 2,
    totalPagesReal: 11,
    hours: {
      low: 4,
      high: 8,
      mid: 6
    },
    cost: {
      low: 1120,
      high: 2240,
      mid: 1680
    },
    notes: "Essentially pre-litigation only: no complaint, summons, or any court filing exists in this matter's file set — the two documents present are evidentiary background records reviewed during initial case assessment before the decision was made not to pursue."
  },
  {
    number: 24,
    type: "Federal - 42 U.S.C. 1983 (Due Process, 1st Amend. Retaliation - U-Visa certification denial)",
    documentsCount: 21,
    totalPagesReal: 168,
    hours: {
      low: 77.5,
      high: 135,
      mid: 106.25
    },
    cost: {
      low: 21700,
      high: 37800,
      mid: 29750
    },
    notes: "Aug. 28 true-up (21 PDFs / 168 pages). Intake complaint + N.D. Cal. paperwork carry forward. New billable work: FAC + Notice of Errata (related-action disclosure amendment, not a full re-plead); Civil L.R. 3-12 related-case motions (filed + supplemental; drafts billed incrementally); light review of Serrato's 18-page 12(b)(6)/12(f) MTD; and the 18-page Opposition v4 at motion-briefing 0.6–1.2 hr/page. Duplicate opposition formats (plain PDF, pleading-paper, unified + POS, page-1 scan) billed once at full rate plus incremental assembly. USM-285 return and the Aug. 24 relate order are administrative / light-review only."
  },
  {
    number: 25,
    type: "State — PC §290.46(j) / ICRAA / Wrongful Failure to Hire",
    documentsCount: 17,
    totalPagesReal: 53,
    hours: {
      low: 47,
      high: 79,
      mid: 63
    },
    cost: {
      low: 13160,
      high: 22120,
      mid: 17640
    },
    notes: "Filed July 15, 2026. The 18-page, six-count complaint is the only substantive drafting product; most remaining pages are single-page First Advantage notice/reminder emails reviewed for the factual record. Increment since the prior estimate: file-stamped complaint confirmation pages, the FW-003 fee waiver order (GRANTED), a duplicate Notice of Case Assignment/Hearing, and the SUM-100 Summons — all billed at light administrative/evidence-review rates, not drafting rate. No answer, motion practice, or discovery exists yet; service not yet completed."
  },
  {
    number: 26,
    type: "State — PC §290.46(j) / ICRAA / Wrongful Failure to Hire (removed to E.D. Cal.)",
    documentsCount: 55,
    totalPagesReal: 556,
    hours: {
      low: 80,
      high: 147,
      mid: 113.5
    },
    notes: "Oct. 28 true-up: 6-page opposition to UPS's consent motion for more time to reply (Sep. 4) billed at short-motion 0.6–1.2 hr/page plus POS/tracking at admin rates; Dkt. 14 UPS reply ISO the Rule 12(b)(6) (Sep. 14) at opposing-counsel light review only. Aug. 31 true-up: clerk-stamped Dkt. 10 opposition (Filed Aug. 28, 20 pp.) is the filed counterpart of the already-billed unfiled draft — incremental stamp-review only, not a second briefing. Proposed order remains unfiled (Drozd Standing Order I.E). Aug. 28 true-up of the ECF 7 MTD pack and opposition-pack-10 duplicates carries forward."
  },
  {
    number: 27,
    type: "State — PC §290.46(j) / Wrongful Termination / ICRAA / Negligence Per Se / UCL",
    documentsCount: 32,
    totalPagesReal: 140,
    hours: {
      low: 75.7,
      high: 130.2,
      mid: 102.95
    },
    notes: "Oct. 28 true-up: Sep. 16 proposed default judgment (JUD-100) at short-motion rates; executed stipulation to set aside the default (Sep. 17) as Plaintiff's counterpart; notice-of-settlement papers at administrative/negotiation rates only — opposing drafts at light review. Duplicate sheriff POS/SER packets stay incremental. Sep. 14 afternoon increment: Tai Gmail (1 p.) + Gurney CIV-141 (2 pp.) and Moskow Gmail (1 p.) + executed counterpart (6 pp.) billed at opposing-counsel light review only — served papers, not entered orders. Morning increment: Williams/Chapman counsel stipulation and proposed order plus the two-page Gmail print (Sep. 12 settlement email / e-sign ask Sep. 14) billed at opposing-counsel light review only, not drafting rate. Plaintiff counterpart (3-page stipulation + 2-page proposed order) is Plaintiff's own paper. Prior increment: complaint e-filed and RK Logistics responded, plus service confirmed. Thirteen new documents since the pre-filing estimate: the e-filing confirmation packet billed as light administrative/procedural tasks (0.5–2 hr/doc); a duplicate filed copy of the 19-page Complaint billed only incrementally; the 12-page Garcia & Gurney response letter, billed above the standard opposing-counsel light-review rate to account for the substantive rebuttal analysis it required, plus its 1-page Gmail transmittal; and the 2-page Sacramento County Sheriff Civil File Status confirming Jul. 30, 2026 dual service. Prior 12-document, 58-page base carries forward."
  },
  {
    number: 28,
    type: "Federal — 42 U.S.C. §1983 (Monell + Individual Capacity); Bane Act §52.1; Fraud/Negligent Misrepresentation; RICO 18 U.S.C. §1962(c)-(d)",
    documentsCount: 39,
    totalPagesReal: 758,
    hours: {
      low: 142,
      high: 255,
      mid: 198.5
    },
    notes: "Oct. 28 true-up: 24-page opposition to the Smith/HOPE MTD (served Sep. 22; sidecar pdfinfo) at motion-briefing 0.6–1.2 hr/page; e-service email at admin; 13-page name-conform packet at Civil L.R. 7-11 administrative rates; Dkt. 30 reply (10 pp.), supplemental RFJN (5 pp.), and certificate of service at opposing-counsel light review only. Aug. 28 true-up carries forward. ~478 pages under HOPE Discovery (Matter 5)/ stay Matter 5 production — $0 here. Fee-shifting under §1988 and RICO still applies on prevailing."
  },
  {
    number: 29,
    type: "State — PC §290.46(j) / FCRA / ICRAA / Failure to Hire",
    documentsCount: 32,
    totalPagesReal: 180,
    hours: {
      low: 98.5,
      high: 176,
      mid: 137.25
    },
    notes: "Oct. 28 true-up: 20-page opposition to Amazon's Dkt. 19 MTD (served Sep. 22–23; sidecar pdfinfo) at 0.6–1.2 hr/page; Amazon MTD (12 pp.) and Oct. 13 reply (6 pp.) at light review; Accurate Answer at light review; Dkt. 01–02 removal notice + 68-page exhibit stack at opposing-counsel review (state complaint inside already billed); 13-page name-conform packet at admin rates; magistrate-consent / conflicts / CMC / extension-stip counterparts at 0.5–2 hr/doc; Oct. 14 FCRA file-dispute letter at short-filing rates. Related-case PACER libraries (Lerma, Carrillo, Santee, Walker, Varela) are research copies — not re-billed as drafting. State-court complaint e-filing increment carries forward. Fee-shifting under PC §290.46(j)(4)(A), FCRA, and ICRAA applies upon prevailing."
  },
  {
    number: 30,
    type: "Federal — 42 U.S.C. §1983 (First Amendment Retaliation + Due Process); Bane Act Cal. Civ. Code §52.1; IIED",
    documentsCount: 12,
    totalPagesReal: 107,
    hours: {
      low: 56,
      high: 132,
      mid: 86.5
    },
    cost: {
      low: 15680,
      high: 36960,
      mid: 24220
    },
    notes: "Complaint filed Sep. 16, 2026. Twelve documents totaling 107 real pages (corrected from a 64-page estimate): 26-page verified complaint (Newanforbi v. Moua, et al.); 25-page Derrick FAC (Case 2:26-cv-00004-DJC-JDP, E.D. Cal. — scanned PDF, confirms triggering protected activity and Noguchi as named co-defendant); 3 CASOMB submission PDFs (~5 pages — Dr. Kirsten Mason inquiry, BNN responses, telehealth accommodation request); 4 screenshots (4 pages — Agent Moua contact card, Agent Brown text exchanges, CountySuite service records); Macy's job offer (~3 pages); Macy's work schedule (~2 pages); and a 42-page 'Newanforbi v. CDCR, et al 3.pdf' — on inspection this is a duplicate copy of the SUM-100 Summons and Complaint for Damages already fully billed under Matter 15 (case STK-CV-UPI-2026-5417), sitting in this folder as cross-reference evidence for the Noguchi/Rojo service history — billed at a nominal flat rate (not per-page) since it is fully duplicative of already-priced Matter 15 work, not new drafting. Hours are substantially elevated because: (1) the complaint requires three independent §1983 retaliation theories each with distinct factual predicates; (2) Bane Act §52.1 adds a state-law coercion theory requiring Shoyoye pleading of independence; (3) Heck v. Humphrey and absolute immunity must be preemptively addressed; (4) Government Claims Act exhaustion (GCA claim Jul. 18, deemed rejected Sep. 1) must be pleaded; (5) supervisory liability for Noguchi (named Derrick FAC co-defendant + 1502-DR co-author) and Rojo. Fee-shifting under 42 U.S.C. §1988 and mandatory Bane Act attorney fees make attorney fee recovery highly probable on prevailing."
  },
  {
    number: 31,
    type: "State — FCRA §1681b(b)/§1681e(b), ICRAA, Negligence Per Se, UCL §17200",
    documentsCount: 0,
    totalPagesReal: 0,
    hours: {
      low: 35,
      high: 78,
      mid: 56.5
    },
    cost: {
      low: 9800,
      high: 21840,
      mid: 15820
    },
    notes: "No new PDFs — the evidentiary basis (First Advantage's pre-adverse/adverse notices for both the UPS and FedEx sequences) is already measured and billed under Matters 26 and 25 respectively; counting those pages again here would double-count real work already priced elsewhere. Estimated instead from matters.js status text as a single-defendant vendor-liability complaint of moderate complexity: five causes of action (two FCRA provisions, ICRAA, negligence per se, UCL) drafted from an existing fact pattern rather than fresh investigation, roughly comparable in scope to Matter 8's single-document writ estimate. No motion practice, discovery, or service costs included since nothing has been filed."
  },
  {
    number: 32,
    type: "Federal — § 1983 (N.D. Cal.) + Nov. 1, 2024 CHP cluster document store",
    documentsCount: 122,
    totalPagesReal: 1135,
    hours: {
      low: 57,
      high: 90,
      mid: 73.5
    },
    notes: "Oct. 28 true-up: Rule 55(a) clerk-default packet (10 pp., Sep. 18) at short-motion/admin rates; name-conform administrative motion and CCP 415.20(b) mailing declarations at 0.5–2 hr/doc. Dkt. 22 MTD opposition was emailed as a courtesy copy Oct. 27 but is not an ECF entry through Oct. 28 — not billed as a filed opposition. Aug. 28 true-up carries forward. from-01|02|20|24/ PDFs remain attributed to source Matters 1, 2, 20, and 24 at $0 here. Nov. 1 / Candelaria APS evidence lives in Matter 33."
  },
  {
    number: 33,
    type: "Federal — § 1983 APS / N.D. Cal. refile + document store",
    documentsCount: 33,
    totalPagesReal: 435,
    hours: {
      low: 52.5,
      high: 99.5,
      mid: 76
    },
    notes: "Oct. 28 true-up: Dkt. 18 name-correction stipulation and Dkt. 16 certificate of interested entities at administrative rates; Dkt. 24 order granting the motion to strike (2 pp., Oct. 13) at court-order light review. Prior N.D. Cal. refile (Complaint v3 adaptation of Matter 7) and Nov. 1 / APS evidence-compilation line carry forward. from-07 / from-08 drafting stays on Matters 7 and 8."
  },
  {
    number: 34,
    type: "Federal — 42 U.S.C. §1983 (Monell + Individual); Bane Act Cal. Civ. Code §52.1; Fraud; UCL §17200",
    documentsCount: 0,
    totalPagesReal: 0,
    hours: {
      low: 15,
      high: 40,
      mid: 27.5
    },
    cost: {
      low: 4200,
      high: 11200,
      mid: 7700
    },
    notes: "Pre-filing intake and compliance-audit stage. No documents on disk yet (0 real pages). Estimated work encompasses initial client intake review, CASOMB provider verification and regulatory analysis under 15 CCR §3574, treatment contract analysis, and adaptation of the Matter 28 / Matter 5 pleading framework for Santa Clara County / CPC corporate defendants. Fee-shifting under 42 U.S.C. §1988 and Cal. Civ. Code §52.1(i) applies upon prevailing."
  },
  {
    number: 35,
    type: "State — Unruh / False Imprisonment / Negligent Training (Santa Clara Sup. Ct.)",
    documentsCount: 24,
    totalPagesReal: 250,
    hours: {
      low: 56,
      high: 100,
      mid: 78
    },
    notes: "Oct. 28 true-up: Ross verified answer and jury-fee notice (served Oct. 15) at opposing-counsel light review; Ross discovery Set One (specials 8 pp. + form interrogatories 9 pp. + RFPs 7 pp.) at review-to-respond rates, not a full drafted response set; Sep. 10 request to correct case title at administrative rates; signed POS-010s at 0.5–2 hr/doc. Aug. 28 true-up of the v9 complaint and CT / summons-first service packets carries forward. Fee-shifting under Civ. Code §52(a) and CCP §1021.5 applies upon prevailing."
  },
  {
    number: 36,
    type: "Federal — FCRA / ICRAA / Contract / § 290.46(j) (E.D. Cal. 2:26-cv-03314)",
    documentsCount: 43,
    totalPagesReal: 190,
    hours: {
      low: 52.5,
      high: 97,
      mid: 74.8
    },
    notes: "Oct. 28 true-up: E.D. Cal. filing (2:26-cv-03314-DJC-AC). 23-page intake packet is a venue adaptation of the already-billed 37-page San Joaquin complaint (not a second 2–3 hr/page draft); 24-page CT service packet at compilation; Dkt. 4 IFP/screening order (4 pp.), Dkt. 5 scheduling order (7 pp.), and Dkt. 6 summons (2 pp.) at court-order/admin review. Sep. 6 San Joaquin signed complaint and walk-up forms carry forward. First Advantage is not a named defendant."
  },
  {
    number: 37,
    type: "State — ICRAA / UCL / § 290.46(j) (San Joaquin packet + E.D. Cal. intake, unfiled)",
    documentsCount: 12,
    totalPagesReal: 90,
    hours: {
      low: 22,
      high: 46,
      mid: 34
    },
    notes: "Oct. 28 true-up: E.D. Cal. intake packet (complaint / JS 44 / AO 239 / AO 440 / MJ consent / print copy) billed as venue adaptation and assembly of the already-priced 25-page San Joaquin complaint, not a second 2–3 hr/page draft. Sep. 6 San Joaquin signed complaint and walk-up forms carry forward. No demand or CRD charge."
  },
  {
    number: 38,
    type: "State — ICRAA / UCL / § 290.46(j) I&B (San Joaquin packet + E.D. Cal. intake, unfiled)",
    documentsCount: 22,
    totalPagesReal: 165,
    hours: {
      low: 26,
      high: 54,
      mid: 40
    },
    notes: "Oct. 28 true-up: E.D. Cal. intake packet billed as venue adaptation/assembly of the already-priced 25-page San Joaquin complaint. Sep. 6 true-up carries forward (ICRAA § 1786.40; 17-page Oct. 5 post-adverse at evidence-compilation rates; 49-page encrypted pre-adverse at existence/admin only). No demand or CRD charge."
  },
  {
    number: 39,
    type: "Federal — ICRAA / UCL / § 290.46(j) I&B (E.D. Cal. filed Sep. 18, 2026)",
    documentsCount: 19,
    totalPagesReal: 105,
    hours: {
      low: 14,
      high: 32,
      mid: 23
    },
    notes: "Oct. 28 true-up: Dkt. 1 complaint packet (14 pp., filed Sep. 18) is the file-stamped counterpart of the already-billed 25-page draft — incremental stamp/assembly only; Dkt. 2 AO 239 IFP (5 pp.) at 0.5–2 hr/doc; 20-page print intake at compilation. Sep. 6 San Joaquin signed complaint and walk-up forms carry forward. First Advantage is not a named defendant."
  },
  {
    number: 40,
    type: "Federal — FCRA / ICRAA / § 290.46(j) (N.D. Cal. complaint signed, unfiled)",
    documentsCount: 22,
    totalPagesReal: 112,
    hours: {
      low: 21,
      high: 44,
      mid: 32.5
    },
    notes: "Oct. 28 true-up: 28-page N.D. Cal. complaint draft (Sep. 24 sidecar) billed at employment-cluster template-adaptation rates, not a full 2–3 hr/page first-impression pleading; Sep. 23 29-page version is a near-duplicate (incremental only); 42-page complete filing packet billed as assembly; AO 240 / JS-CAND 44 / three AO 440 summons / MJ consent / conflicts certificate at 0.5–2 hr/doc. Sep. 14 monitoring file (offer, FA screening, CA SOS, TA Ops hold) carries forward at the original 1–2.5 hr band. Unfiled.",
  },
  {
    number: 41,
    type: "State — prospective employment monitoring (Nuro, Inc.; pre-dispute)",
    documentsCount: 15,
    totalPagesReal: 34,
    hours: {
      low: 1,
      high: 2.5,
      mid: 1.75
    },
    cost: {
      low: 280,
      high: 700,
      mid: 490
    },
    notes: "Sep. 9–18, 2026: Indeed application + Greenhouse auto-reply + GoodTime scheduling flow (Elizabeth Gonzalez) + Sep. 16 Google Meet interview (James Craig) + Sep. 17 driving-eval advance with license-requirements/MVR email (Crystal Garcia) + Sep. 18 driving eval + DocuSign NDA/site-visit waiver (Michelle Nguyen). Checkr vendor is user-stated, unconfirmed. No background-check authorization, no report, no adverse action — monitoring file.",
  },
  {
    number: 42,
    type: "Federal — FCRA / ICRAA / § 290.46(j) (N.D. Cal. Staples draft, unfiled)",
    documentsCount: 3,
    totalPagesReal: 25,
    hours: {
      low: 16,
      high: 34,
      mid: 25
    },
    notes: "Oct. 28 true-up: 21-page N.D. Cal. complaint draft (to-file, Oct. 19) billed at employment-cluster template-adaptation rates, matching Matters 37–40 rather than a full 2–3 hr/page first-impression pleading; two JS-CAND 44 cover-sheet PDFs (2 pp. each) at 0.5–2 hr/doc. First Advantage Oct. 7 public-record notice is not in this priced set. Unfiled; no pre-adverse or adverse action in the record.",
  },
  {
    number: 43,
    type: "State — prospective employment monitoring (Hertz; HireRight screening; pre-dispute)",
    documentsCount: 16,
    totalPagesReal: 70,
    hours: {
      low: 1,
      high: 2.5,
      mid: 1.75
    },
    notes: "Oct. 28: 16-PDF monitoring file (offer, ADP WOTC, HireRight acknowledgments/authorization, MVR Express furnishing notice). Same band as Matter 41 — evidence preservation, not pleading. Page count is estimated from the 16-file inventory (PDFs not on the laptop disk for pdfinfo); sidecar coverage is incomplete. No complaint. No adverse action in the record.",
  },
  {
    number: 44,
    type: "Pre-filing employment intake",
    documentsCount: 0,
    totalPagesReal: 0,
    hours: { low: 0, high: 0, mid: 0 },
    notes: "No public filings or priced work recorded.",
  },
];

export const lawyer_fees = lawyer_fees_raw.map((row) =>
  withMatterIdentity(withDerivedCost(row)),
);

export const lawyer_fees_summary = summarizeLawyerFees(lawyer_fees, {
  analysisDate: "2026-10-28",
  trackedMatters: summaries.length,
  methodologyNote:
    "Hours are classified by document type and priced using the hours-per-page/per-document conversions in docs/LAWYER_FEES_CALCULATOR.md. Cost, cluster rollups, and portfolio totals are derived from those hours at the blended $280/hr rate (lawyerFeeMath.js). Opposing counsel's filings are billed only at a light review rate, never at drafting rate. Duplicate packs (opposition-pack-10, conformed copies, from-* stores, related-case PACER libraries) are billed incrementally or excluded. Matters with no uploaded PDFs are estimated conservatively from matter JSON status text. Oct. 28, 2026 true-up: M26 UPS extension opposition + Dkt. 14 reply review; M27 default-judgment / set-aside papers; M28 24-page MTD opposition + Dkt. 30 reply review; M29 Amazon MTD opposition and removal-cycle review; M32 Rule 55(a) default packet; M33 name-stip / Dkt. 24; M35 Ross answer and discovery Set One review; M36–M39 E.D. Cal. intake/filing; M40 28-page unfiled N.D. Cal. complaint; M42 Staples draft complaint; M43 Hertz monitoring file.",
});
