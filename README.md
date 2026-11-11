<img src="internal/public/logo-light.webp" alt="Newanforbi — In Propria Persona" width="180" align="left" />

# Interactive Litigation Portfolio

An interactive, single-page litigation dashboard for **Brendan Ngehsi Newanforbi**, Pro Se / In Propria Persona. The public site is a filings-and-redacted-docket view of **41** civil matters across federal and California state courts. Strategy memos, settlement figures, and personal contact information stay on the laptop graph.

**Live site:** [interactive-litigation-portfolio.vercel.app](https://interactive-litigation-portfolio.vercel.app)

<br clear="left" />

## Standing Stipulation Policy

All current and future matters follow the [Stipulation Defense — Plaintiff-First Standing Policy](internal/docs/STIPULATION_DEFENSE.md). Draft and review every stipulation for Plaintiff's maximum supported advantage: maintain or shorten defense deadlines where favorable, protect Plaintiff's preparation time, preserve hearing dates and rights, and identify every concession and its concrete benefit. Required review includes a deadline comparison and concession audit. This policy is also linked from Codex, Claude, and Cursor repository instructions.

## Contents

- [Overview](#overview)
- [Case Clusters](#case-clusters)
<!-- PORTFOLIO:CASE_CLUSTER_TOC:START -->
  - [1 — CHP Traffic Stop, DUI Arrest & DMV](#cluster-1)
  - [2 — Parole Retaliation, HOPE Abuse & Policy 19-03](#cluster-2)
  - [3 — Employment Violations](#cluster-3)
  - [4 — Administrative Writs & Habeas Corpus](#cluster-4)
  - [5 — Consumer Fraud / Defective Vehicle](#cluster-5)
  - [6 — Public Accommodation / Unruh](#cluster-6)
<!-- PORTFOLIO:CASE_CLUSTER_TOC:END -->
- [All Matters](#all-matters)
- [Upcoming Deadlines](#upcoming-deadlines)
- [Damages Summary](#damages-summary)
- [Attorney Fees Analysis](#attorney-fees-analysis)
- [Legal Theories](#legal-theories)
- [Tech Stack](#tech-stack)
- [Documents & MCP](#documents--mcp)
- [Citation Verification](#citation-verification)
- [CourtListener bridge](#courtlistener-bridge)
- [Local Development](#local-development)
- [Build](#build)
- [Deployment](#deployment)

---

## Overview

<!-- PORTFOLIO:OVERVIEW_TABLE:START -->
| Field | Detail |
|---|---|
| Plaintiff | Brendan Ngehsi Newanforbi |
| Representation | Pro Se / In Propria Persona |
| Jurisdictions | USDC E.D. Cal., USDC N.D. Cal., San Joaquin Sup. Ct., Alameda Sup. Ct., Sacramento Sup. Ct., Santa Clara Sup. Ct. |
| Total Matters | 44 |
| Active / Open | 24 |
| — of which Settled | 2 (Matter 22 — Newanforbi v. Pilot Travel Centers LLC, Jul. 14, 2026; 27 — Newanforbi v. Randstad, et al., Notice of Settlement Oct. 26, 2026) |
| Dismissed / Closed / Abandoned | 20 |
| Aggregate Exposure (Conservative) | ~$1,456,000+ |
| Aggregate Exposure (Moderate) | ~$3,523,000+ |
| Aggregate Exposure (Aggressive) | ~$7,793,000+ |
| Last Updated | September 7, 2026 |
<!-- PORTFOLIO:OVERVIEW_TABLE:END -->

<!-- PORTFOLIO:CLOSED_COUNT_NOTE:START -->
*Of the 20 dismissed/closed/abandoned matters: 7 abandoned, 11 dismissed, 2 otherwise closed (structured `lifecycle` on each matter JSON). See [All Matters](#all-matters) below for the full disposition table. Pre-filing matters stay in the Active table.*
<!-- PORTFOLIO:CLOSED_COUNT_NOTE:END -->

> **Housing status:** Homeless since July 2, 2026 — a direct consequence of a retaliatory inter-county parole transfer (Stockton → Santa Clara) imposed immediately after filing Matter 15 (*Newanforbi v. CDCR, et al.*). The transfer caused loss of Stockton family housing; Matters 3, 9, and 19 are also potential retaliatory predicate acts.
>
<!-- PORTFOLIO:SELF_REP_COST:START -->
> **Cost of self-representation:** All 43 matters are self-litigated. Estimated equivalent private-counsel cost: **$905,184–$1,536,556** (see [Attorney Fees Analysis](#attorney-fees-analysis)).
<!-- PORTFOLIO:SELF_REP_COST:END -->

[↑ Contents](#contents)

---

## Case Clusters

Numbered headings match `matter.cluster` and `internal/src/data/clusters.js`. They are not the named cross-matter graph (`chp-nov2024`, `megan-law-employment` in `index/clusters.json`).

<!-- PORTFOLIO:CLUSTER_HEADING_1:START -->
<a id="cluster-1"></a>
### Cluster 1 — CHP Traffic Stop, DUI Arrest & DMV (Matters 1–2, 7–8, 20, 24, 32–33)
<!-- PORTFOLIO:CLUSTER_HEADING_1:END -->

Arising from a November 1, 2024 CHP encounter on I-580. Officers arrested Plaintiff after he declined an optional PAS test, despite dashcam footage contradicting the DUI report's fabricated observations. No charges were filed; a PC §849(b)(1) Detention Certificate followed on November 5, 2024; a 5-day parole hold and a one-year Class A CDL suspension (APS Case 34739340) followed. The cluster now spans eight matters — six historical dockets plus two N.D. Cal. filings opened August 7, 2026:

- **Matter 1** (USDC E.D. Cal.): Federal §1983 against CHP officers; adverse F&R issued April 20, 2026 (Magistrate CSK recommends MTD GRANTED WOLA — 4th/14th Amendment, qualified immunity); District Judge DC adoption pending. If adopted, Matter 2 (Alameda, stayed) and the new Matter 32 N.D. Cal. filing become the primary vehicles.
- **Matter 2** (Alameda Sup. Ct.): Parallel state tort action (False Imprisonment, Battery, Bane Act); STAYED pending Matter 1 District Judge ruling.
- **Matter 7** (USDC E.D. Cal.): Federal §1983 against DMV Hearing Officer Candelaria and DMV Director Gordon; **DISMISSED WITHOUT PREJUDICE** by notice filed August 15, 2026 (FRCP 41(a)(1)(A)(i)), mooting the June 15 F&R and any objections. Claims were refiled as Matter 33 (N.D. Cal. 3:26-cv-08272-LJC).
- **Matter 8** (Sacramento Sup. Ct.): State Writ of Administrative Mandate challenging the same void APS decision — **ABANDONED** after the July 17, 2026 fee-waiver hearing (non-appearance) and the ~July 27, 2026 fee-payment deadline lapsed. PDFs live under Matter 33 (`matter-33/from-08/`).
- **Matter 20** (Alameda Sup. Ct.): State Writ of Mandate against CHP. After the August 28, 2026 hearing, Judge Whitman entered an August 29 order (notice of entry August 31): Count 1 overruled and proceeds; Counts 2–3 out without leave; Count 4 optional leave to amend by September 20, 2026. Dutra and Paul were dismissed by stipulation; live respondents are CHP and Serrato. CMC is October 28, 2026, 4:00 p.m., Dept. 25.
- **Matter 24** (USDC N.D. Cal.): §1983 against CHP Captain G. Serrato for arbitrary U Visa certification denial and retaliation; IFP granted June 29, 2026 (Krishnan screening order, now cited across the cluster). Sep. 11, 2026: Clerk's Notice of Impending Reassignment (Dkt. 28) — the case leaves Mag. Krishnan for a district judge; all Krishnan hearing dates vacated, including the Sep. 30 MTD hearing (Dkt. 21) — re-notice to follow; case-number suffix will change from -ASK. CMC continued per Dkt. 25 (no new date). Listed as related case on the Matter 32/33 JS-44s.
- **Matter 32** (USDC N.D. Cal.): *Nforbi v. Meza-Gonzalez & Melano*, **3:26-cv-08271-PHK** (related/reassigned as **4:26-cv-08271-ASK**); docketed August 10, 2026. Operative pleading is the August 17 FAC (Dkt. 5). Melano has been served. Signed Meza substituted-service return is in hand (Fischer / Run With It, Aug. 27 on Kim S. - H.R. at CHP Modesto) and still needs to be filed. A Civil L.R. 7-11 motion asking DAG Li to accept service was filed September 3 (Dkt. 13). Also owns the Meza-Gonzalez / CHP-cluster docket PDFs from Matters 1, 2, 20, and 24 under `matter-32/from-01|02|20|24/` and the new N.D. Cal. filing set under `matter-32/ndcal/`.
- **Matter 33** (USDC N.D. Cal.): *Nforbi v. Candelaria, et al.*, **3:26-cv-08272-LJC**; docketed August 10, 2026. Operative pleading is the August 17 FAC (Dkt. 6). Fiel Dizon Tigno (Supervising DAG) is PACER lead; William J. McMahon signed the September 4 answer to superseded Dkt. 1 (ECF No. 11). Plaintiff's motion to strike that answer is on file as Dkt. 17 (PACER Event Filed Sep. 9; CL entered Sep. 10). Opposition due September 23; reply September 30; hearing stacked on the November 12 1:30 p.m. CMC. McMahon asked five extra opposition days on September 18; Plaintiff remains silent — September 23 is not enlarged. Dkt. 12 sets defendants' magistrate consent/declination for September 22 (Dkt. 14 is a misfile — disregard). Name-conform granted Dkt. 19 (September 16) on the Dkt. 18 stipulation (filed September 14). Krishnan declined to relate the case to Serrato (Dkt. 13). Also owns the Nov. 1 / APS incident evidence (`matter-33/incident/`), Matter 7 PDFs (`from-07/`), Matter 8 PDFs (`from-08/`), the June 15, 2026 Candelaria F&R (`opinions/`), and the N.D. Cal. filing set under `matter-33/ndcal/`.

<!-- PORTFOLIO:CLUSTER_HEADING_2:START -->
<a id="cluster-2"></a>
### Cluster 2 — Parole Retaliation, HOPE Abuse & Policy 19-03 (Matters 3–6, 11, 13–18, 21, 28, 30, 34)
<!-- PORTFOLIO:CLUSTER_HEADING_2:END -->

The largest cluster — 14 matters — targeting CDCR's parole supervision apparatus, the HOPE Psychotherapy program, and constitutional violations across parole travel, housing, and employment decisions. Core allegations include:

- **First Amendment retaliation** by Agent Derrick, who suppressed speech and sabotaged Plaintiff's FedEx employment; explicit "you do not have freedom of speech" statement satisfies *Rhodes v. Robinson*.
- **Retaliatory inter-county transfer** on July 2, 2026 — supervision moved from San Joaquin to Santa Clara County immediately after filing Matter 15 naming Supervising Agent Noguchi; caused loss of Stockton family housing and employment; Plaintiff has been **homeless since July 2, 2026**. Matters 3, 9, and 19 are also potential retaliatory predicate acts for the transfer.
- **HOPE's structural fee incentive** (~$9,690–$10,600/year per parolee at standard billing rates; condemned in *In re Dwyer*, SC-080355A, San Mateo County Super. Ct., Mar. 20, 2023) with no completion credit — financial incentive to retain rather than discharge.
- **HOPE's blanket retention policy** requiring the full parole term regardless of clinical progress — documented in HOPE's own Clinical Operational Manual (HOPE_000294) and condemned in *In re Dwyer*; now forms the Monell theory in Matter 28.
- **Retaliatory reporting** — false no-shows logged and adverse CDCR Form 3043 reports directed by Shannon Smith; HOPE_000142/194 (produced in Matter 5) documents a no-show logged despite agent-confirmed technical error.
- **Facially defective Discharge Review** (November 2025) containing a copy-paste error naming "Eagan" rather than Plaintiff; fabricated 6.5-year retention minimum sourced from academic research rather than statute; unemployment (caused by Defendants' own conduct) cited as aggravating factor.
- **Policy 19-03** enforced after 15 CCR § 3574 superseded it in April 2025 — ultra vires categorical bar.
- Documented CDL career wage losses: $109,408 across 6 carriers (W-2 verified, 2022–2024).
- **Matter 5 (Palacios)** — state action disposed July 15, 2026 (demurrer sustained, exhaustion grounds); 542 pages of HOPE discovery (Bates HOPE_000001–542) produced before dismissal are now carried into **Matter 28** via Motion for Protective Order.
- **Matter 15** (San Joaquin Sup. Ct., STK-CV-UPI-2026-5417) — **ABANDONED.** Would have asserted Negligence, False Imprisonment, IIED, and Breach of Mandatory Duty against CDCR, Dodd, and Noguchi — the highest single-matter exposure in the portfolio. Complaint was filed and both individual defendants personally served; a responsive-pleading extension had been agreed with Deputy Attorney General Judith S. Gronna. Voluntarily dismissed with prejudice as to all defendants on July 24, 2026 due to a real, credible safety threat — unrelated to the Matter 19 habeas ruling.
- **Matter 28** (USDC N.D. Cal., Case No. 3:26-cv-07504, Hon. Lisa J. Cisneros): Federal successor; §1983 Monell (HOPE) + Individual Capacity (Shannon Smith, LCSW), Bane Act §52.1, Fraud/Negligent Misrepresentation, RICO 18 U.S.C. §1962(c)-(d); case filed July 20, 2026, Initial CMC set October 22, 2026. **Insured exposure: $1M per incident / $5M aggregate** — Philadelphia Indemnity Policy No. 067968, produced in Matter 5 discovery, covering HOPE Psychotherapy, Inc. and Shannon Smith, LCSW. This is the only carrier-funded floor in the portfolio: it does not depend on either defendant's balance sheet, and because the per-incident limit is one-fifth of the aggregate, pleading discrete violations rather than one omnibus claim is what reaches the full tower. Shannon Smith's individual-capacity exposure sits outside the corporate tower, adding personal settlement pressure on top of it.
- **Matter 30** (USDC N.D. Cal., San Jose Div.) — **PENDING (pre-complaint), filing contingent on parole discharge.** Asserts §1983 First Amendment Retaliation + Due Process, Bane Act §52.1, and IIED against Long Moua (Badge #7472), for the November 14, 2025 retaliatory 1502-DR and the July 2, 2026 inter-county parole transfer; Government Claims Act claim filed July 18, 2026, anticipated deemed-rejected September 1, 2026. This matter is not abandoned: Plaintiff intends to file it if discharged from CDCR parole supervision before its filing window closes, notwithstanding the safety-driven caution that led to abandoning the companion matters below. Outer deadline for the state-law claims is on or about March 1, 2027 (Gov. Code §945.6(a)(1), six months from the deemed rejection); the §1983 claims run on the longer two-year limitations period.
- **Matters 3, 4, 14, 16 (Derrick, Urrea, Rojo)** — all **ABANDONED** due to a real, credible safety threat. Matter 3's federal MTD was under submission at the time of withdrawal; Defendant Palacios's exposure survives independently through Matter 5's discovery record and Matter 28. Matters 6, 11, 13, 17, 18, and 21 — the federal §1983 companion suits against HOPE, Macomber, Urrea, Maloney, and Barocio, all filed the week of January 22, 2026 — were voluntarily dismissed (five with prejudice, together, on June 29, 2026) once the surviving vehicles above made the parallel federal claims unnecessary.

<!-- PORTFOLIO:CLUSTER_HEADING_3:START -->
<a id="cluster-3"></a>
### Cluster 3 — Employment Violations (Matters 22–23, 25–27, 29, 31, 36–39, 42–44)
<!-- PORTFOLIO:CLUSTER_HEADING_3:END -->

Cluster 3 centers on employer-side Penal Code § 290.46(j)(2)(E) claims and related background-screening theories. Matter 31 (First Advantage) is now a **conditional vendor-liability investigation**, not presumed additive liability: after the September 18 Carrillo/Mendoza stress test, any complaint must identify a First Advantage-specific FCRA/ICRAA breach rather than merely repackaging the employers' alleged registry misuse. Matters 36-39 are executed San Joaquin packets (AT&T, Home Depot, Swift, Best Buy) prepared for a September 8, 2026 walk-up and still unfiled as of September 7, 2026. Matter 40 (Uber Technologies, Inc. / TaskUs staffing) is a prospective monitoring file — Offer of Temporary Employment signed September 14, 2026 ($22/hour); same-day TA Ops hold of the September 23 start pending the First Advantage report (Order WPS-361214148; PRINSOS still running); MAA signed; no report viewable and no adverse action yet. (Matters 32 and 33 are CHP / DMV APS filings — see Cluster 1.)

- **Matter 22** (Newanforbi v. Pilot Travel Centers LLC) — **SETTLED July 14, 2026** — San Joaquin Superior Court (STK-CV-UWT-2026-0007649). Wrongful termination; Defendant's own Post-Adverse Action Notice admitted registry as sole termination basis. Resolved pro se in under seven weeks from filing, before service was completed. First portfolio settlement. Closing out August 2026: CM-200 Notice of Settlement / CIV-110 request for dismissal mailed August 3, 2026; POS completed August 5, 2026.
- **Matter 25** (Newanforbi v. Federal Express Corporation) — San Joaquin Superior Court (STK-CV-UWT-2026-0009118); PC §290.46(j) failure to hire; First Advantage BGC ran March 2025; final adverse action March 19, 2025; complaint filed July 15, 2026; assigned to Dept. 10B, Hon. Blanca Banuelos; CMC January 14, 2027. **SERVED July 24, 2026** on Ct Corporation System; responsive pleading due August 24, 2026.
- **Matter 26** (Newanforbi v. United Parcel Service, Inc.) — San Joaquin Superior Court (STK-CV-UWT-2026-0009113); PC §290.46(j) failure to hire; First Advantage BGC ran July 2024; final adverse action July 31, 2024; complaint filed July 15, 2026 — **2-year limitations period preserved (filed 16 days ahead of the July 31, 2026 cutoff)**; assigned to Dept. 11B, Hon. Robert T. Waters; CMC January 13, 2027. **SERVED July 22, 2026**; responsive pleading due August 21, 2026.
- **Matter 27** (Newanforbi v. Randstad US, LLC and RK Logistics Group, Inc.) — Alameda Superior Court, Case No. **26CV199902**, Hon. Thomas Weathers, Dept. 20, Rene C. Davidson Courthouse (reassigned August 7, 2026 from Hon. Karin Schwartz); PC §290.46(j) / FCRA / ICRAA / Tameny wrongful termination. Rehired July 7, 2026; InfoMart BGC shows Billing Code "RK LOGISTICS" with registry as the sole adverse flag; Randstad terminated July 15, 2026, two business days after the FCRA pre-adverse notice. Verified Complaint e-filed July 20, 2026. **On July 21, 2026, RK Logistics denied the $85,000 demand through counsel Garcia & Gurney, ALC**, arguing (1) Randstad was the employer and (2) the rejection was MVR-based — neither ground reaches Randstad, and the MVR defense cites a commercial Class A disqualification inapplicable to the Class C position. **SERVED July 30, 2026** on both defendants. Amended CCP §425.115 notices ($500,000 each) personally served August 21, 2026; POS-040s filed September 9, 2026. Randstad's responsive pleading is extended to September 15, 2026; Williams asked September 9 for a further extension and was declined. The August 19 / August 28 $55,000 / $85,000 demands were withdrawn by email September 9, 2026, 2:57 p.m. RK Logistics was granted to September 14, 2026 (single extension; no further).
- **Matter 29** (Newanforbi v. Amazon.com Services, LLC and Accurate Background LLC) — **REMOVED Aug. 31, 2026** from Alameda Superior Court **26CV201554** (Hon. Jamilah Jefferson, Dept. 520) to USDC N.D. Cal. **3:26-cv-09249-ASK** (U.S. Magistrate Judge Ajay S. Krishnan). Federal-question removal under 28 U.S.C. §§ 1331, 1441, 1446 on the FCRA count; Accurate Background consented (Exhibit 11, Jasmine J. Stanzick / Seyfarth Shaw, dated Aug. 28). Counsel: Andrew P. Frederick (Morgan Lewis). **CASE FILED July 28, 2026**; **BOTH DEFENDANTS SERVED July 31, 2026**. FRCP 81(c) response due **September 8, 2026** (7 days after removal landed on Labor Day; FRCP 6(a)(1)(C) roll). State CMC Jan. 6, 2027 and the Aug. 31 state answer are moot; §425.115 notices are a dead letter federally. **Lerma posture (corrected):** in *Lerma v. Amazon.com Services, LLC et al.*, No. 8:22-cv-01727 (C.D. Cal.), the PC §290.46(j) claim was **dismissed at the pleading stage (May 26, 2023)**; the case later settled (Sept. 29, 2023) on a surviving Fair Chance Act claim against Amazon only — useful Fair Chance / notice precedent, not a settled Megan's Law judgment against these defendants.
- **Matter 31** (Newanforbi v. First Advantage LLC) — **PRE-FILING / CONDITIONAL**. Identified July 30, 2026 via gap analysis; no complaint or demand. September 18 Carrillo/Vons/Asurint stress test materially narrowed the theory: *Mendoza* defeats direct §290.46 liability for mere CRA republication and is adverse to an ICRAA §1786.20(c) Megan's-Law-as-EEO theory; federal First Advantage cases also separate CRA adjudication/notice automation from the employer's final decision. Matter 31 is unpriced pending proof of an independent vendor-specific FCRA/ICRAA violation.
- **Matter 40** (Brendan Ngwa Nforbi v. Uber Technologies, Inc.) — **PENDING / pre-dispute monitoring.** Caption leads with Uber as end client / joint employer on the Uber AV Teammate campaign; TaskUs entities remain as the staffing / offer-letter employers. Offer of Temporary Employment signed September 14, 2026 (Teammate, $22/hour, San Jose). Same day, 11:24 a.m.: TA Ops US placed the September 23 start on a **standard administrative hold** pending the First Advantage background screening report — not a denial and not a pre-adverse notice. Order **WPS-361214148** is live (PRINSOS still In Progress; report not viewable). Saliva drug test still expires September 17. MAA signed. CA SOS: **TaskUs, LLC (200826810086) Converted Out**; USA LLC and Holdings Active via C T Corporation System. Uber CA SOS not yet pulled.

<!-- PORTFOLIO:CLUSTER_HEADING_4:START -->
<a id="cluster-4"></a>
### Cluster 4 — Administrative Writs & Habeas Corpus (Matters 9–10, 19)
<!-- PORTFOLIO:CLUSTER_HEADING_4:END -->

Three equitable proceedings seeking court orders directing CDCR to act — no tort damages sought. Two are now closed; one remains active:

- **Matter 9** (Sacramento Sup. Ct., 26WM000028): Writ of Mandate — **CLOSED**. Demurrer sustained without leave to amend May 29, 2026 (Hon. James P. Arguelles, Dept. 13A): CDCR has no duty under Pen. Code §3008 to conduct an individualized EDC assessment where §3000(b)(2)(B) mandates a 10-year parole term; habeas corpus is the correct vehicle. The substantive claim is live in Matter 19.
- **Matter 10** (Santa Clara Sup. Ct., C2602632): Habeas Corpus — **CLOSED**. Petition denied without prejudice April 27, 2026 (exhaustion; PC §3008(d)(2) certification required).
- **Matter 19** (Santa Clara Sup. Ct., C2604791): Habeas Corpus — **ACTIVE**. Seeks immediate and unconditional discharge from parole; filed April 3, 2026; Order Extending Time issued July 2, 2026 (Hon. Robert Hawk) setting a ruling deadline of August 1, 2026. **That deadline lapsed without a ruling** — as of August 7, 2026 Judge Hawk has not ruled and no further extension order has issued. The petition remains pending and under submission; it has not been denied, dismissed, or set for an Order to Show Cause. An HC-004 request-for-ruling packet was prepared August 7, 2026 and is ready to file.

<!-- PORTFOLIO:CLUSTER_HEADING_5:START -->
<a id="cluster-5"></a>
### Cluster 5 — Consumer Fraud / Defective Vehicle (Matters 12, 40–41)
<!-- PORTFOLIO:CLUSTER_HEADING_5:END -->

Fraud and UCL claims against Diamond Truck Sales, Inc. and Alpine Truck Sales, Inc. for concealing a DEF/emissions defect and prior CHP out-of-service order on a 2014 Volvo VNL (VIN: 4V4NC9EH6EN142206) purchased for $26,900. The truck entered catastrophic derate mode immediately after purchase, rendering it commercially unusable. Direct documented losses ~$25,129.44; lost hauling income >$46,800. At the August 12, 2026 CMC, both defendants appeared through counsel (Gulomjon Azimov), disputed service, and no default was entered; further CMC December 11, 2026. California SOS bizfile (August 28, 2026): Diamond Truck Sales, Inc. (Entity 3438768) — agent **Saliman Osmani**, 1201 S. Soderquist Road, Turlock (Stanislaus); Alpine Truck Sales, Inc. (Entity B20250280641, formed September 2, 2025) — agent **Sheran Osmani**, 7156 Golden State Highway, Bakersfield (Kern). Alpine's July 1, 2026 Turlock service was not the SOS agent address. Re-serve the Amended Summons and FAC on those agents (Alpine named as sued); meet and confer with Azimov first.

**Requested default prove-up (did not go forward):** The August 12, 2026 CMC did not convert to a prove-up because both defendants appeared through counsel, disputed service, and no default was entered. The figures below remain the litigated-damages floor:

| Component | Amount |
|---|---|
| Documented Out-of-Pocket (deposit $12,345.10 + GAP $1,895 + DMV $3,442 + Brannon Tire $1,197.34 + Mobile Will's $740 + Golden Empire Towing $562.50 + Western Truck Center $36.71) | $20,218.65 |
| Undocumented Out-of-Pocket, sworn testimony (Commercial Towing $750 + Almaraz Diesel $5,000) | $5,750.00 |
| Lost Commercial Hauling Income (18 wks × $1,300/wk; Amazon Relay carrier agreement on file) | $23,400.00 |
| Prejudgment Interest (Civ. Code §3287(a); 7% × ~3.04 yrs on documented losses) | $4,302.55 |
| **Compensatory Subtotal (per Declaration ISO Default Judgment, filed June 15, 2026)** | **$53,671.20** |
| Punitive Damages (Civ. Code §3294; fraudulent concealment + intentional misrepresentation; Diamond→Alpine rebrand as consciousness-of-liability badge) | ≥ $25,000.00 |
| Costs of Suit (per Form MC-010 — filing fees, sheriff's service fees, etc.) | per MC-010 |
| **Total Monetary Judgment Requested (per Default Judgment Packet)** | **≥ $78,671.20 + costs** |

*The $78,671.20 floor is established in the Declaration ISO Default Judgment filed June 15, 2026 against Diamond Truck Sales, Inc. Punitive damages and costs remain subject to judicial discretion if and when a future prove-up occurs. Lost income was deliberately underpled at 18 weeks (conservative) versus the FAC's $46,800+ allegation; FAC paragraph 31 controls the Greenup v. Rodman notice ceiling on lost income.*

**Post-judgment collection prep (as of July 29, 2026 — no judgment entered yet):** EJ-001 (Abstract of Judgment), EJ-130 (Writ of Execution), AT-138/EJ-125 (Judgment Debtor Examination), and MC-012 (Memorandum of Costs After Judgment) are pre-drafted with the case's fixed facts (parties, court, case number) already filled in, so they're ready to complete and file the same day or next business day if a future prove-up produces a judgment — no field asserts a judgment date or amount that hasn't happened. Alpine's joint-and-several exposure runs through its own pre-drafted default judgment packet (CIV-100, execution date Aug. 1, 2026), not a CCP §187 motion to amend the judgment — §187 amendment adds an alter ego who was never a named party, and generally isn't available where the underlying judgment is by default; Alpine is already a named, personally-served defendant, so its own default judgment is the correct vehicle.

**Default judgment packet review findings (flagged Jul. 29, 2026):**
- **Case number error** — every CIV-100 in both the Diamond and Alpine default judgment packets, and the original [Proposed] Judgment (JUD-100), showed the case number as `STK-CV-UF-2026-1094` instead of the actual `STK-CV-UF-2026-0001094`. The JUD-100 has been corrected (new file in the documents list, ready to submit at the Aug. 12 CMC) and also now names Alpine — not just Diamond — in Item 5a's operative "against defendant" field, since the original only mentioned Alpine's joint-and-several liability in freeform Item 8 text, which the abstract-of-judgment and writ-of-execution forms aren't built to read. Diamond's CIV-100/Declaration were already submitted to the court on 6/15/26 with the case-number error baked in — that can't be fixed by editing a repository copy; confirm with the clerk that the case docketed correctly, and fix Alpine's CIV-100 before it's filed Aug. 1.
- **"Osmani" vs. "Usmani"** — **Pinned August 28, 2026 from SOS bizfile.** Diamond's agent is **Saliman Osmani**; Alpine's agent is **Sheran Osmani**. The July 1 Alpine POS used Usmani (Mustagem/Mustaqem) at Turlock. Use Osmani on re-service, matching the SOS record. The alter-ego declaration's "Osmani family" spelling is now the SOS spelling.
- **Standing question on the lost-income claim** — the Lease-On Owner Operator Agreement behind the $23,400 lost-income figure is contractually between Gobbato Builders, LLC and a separate registered entity, "Altamont Freight LLC" (confirmed by its own W-9 and Amazon Relay driver roster, at a different Modesto address), not personally Brendan Ngwa Nforbi, though the Declaration frames the loss as his personally. Unlikely to be caught in an uncontested default prove-up, but worth resolving before relying on it in a contested posture.
- **DMV fee vs. pending use-tax exemption** — the $3,442 DMV fee claimed in full as damages includes ~$2,421 in CA use/city-use tax that a CDTFA exemption request in the same exhibit set sought to avoid; the Declaration doesn't disclose whether that exemption was granted, which could reduce the true out-of-pocket DMV obligation if it was.

**Bank levy prep (added Jul. 29, 2026; central-location question resolved Jul. 29, 2026):** AT-167/EJ-152 Memorandum of Garnishee — the form a garnishee bank returns to the levying officer disclosing what it holds, not a notice-of-levy instrument the creditor serves — has been caption-prefilled for both known target institutions (Bank of Stockton and JPMorgan Chase) against both Diamond and Alpine, four draft copies total, items 3–9 left blank for the bank to complete. Garnishee addresses used are each bank's Turlock branch nearest 1201 S Soderquist Road (Bank of Stockton, 134 S Golden State Blvd; Chase, 2951 Countryside Dr).

Both banks almost certainly exceed the 9-branch threshold under CCP §684.115, which requires financial institutions with more than nine California branches to designate a single central location for levy service statewide, filed with DFPI. DFPI's actual *Central Locations for Service of Legal Process* registry was obtained and searched in full (every cell, not just institution-name matches): **neither JPMorgan Chase Bank, N.A. nor Bank of Stockton has ever filed a designation.** The registry isn't limited to DFPI-licensed institutions — it includes other OCC-chartered national banks (e.g., American Plus Bank, N.A.; Chino Commercial Bank, N.A.), so the absence isn't a charter-type artifact. Under §684.115's default rule, a financial institution that fails to designate has *every* California branch deemed a valid central location for service. Net effect: the two Turlock branches above are legally valid levy targets for both banks as-is; no further address confirmation is needed. (Registry caveat: DFPI's file was last updated with new filings through Sep. 22, 2025, so a designation filed after that date wouldn't appear — low residual risk here since neither bank has any filing history at all, not a recently-lapsed one. Bank of Stockton's separate DFPI *regulated-entity* listing, a different dataset entirely, confirms its license and HQ at 301 East Miner Avenue, Stockton — supporting context, not a substitute for the central-locations finding.)

None of this is actionable yet regardless: it depends on the Writ of Execution (EJ-130) actually issuing, which requires a judgment first.

<!-- PORTFOLIO:CLUSTER_HEADING_6:START -->
<a id="cluster-6"></a>
### Cluster 6 — Public Accommodation / Unruh (Matter 35)
<!-- PORTFOLIO:CLUSTER_HEADING_6:END -->

Standalone retail civil-rights matter arising from an August 25, 2026 consumer racial-profiling detention at the Ross Dress for Less in Sunnyvale:

- **Matter 35** (Ngwa Nforbi v. Ross Stores, Inc., et al.) — Santa Clara Superior Court, First Street. On August 25, 2026 (~9:00 p.m.), Plaintiff entered Ross holding a Celsius drink purchased minutes earlier at the adjacent Sprouts, browsed men's clothing without taking Ross merchandise, and was physically blocked at the exit by a white loss-prevention employee who questioned whether he had paid for the drink, admitted Ross sells Celsius only "sometimes," and asserted "I'm allowed to do that." **~5-hour turnaround:** Verified Complaint (v9) for Unruh (Civ. Code §§51, 51.5, 52), False Imprisonment, and Negligent Training and Supervision **e-filed and paid August 26, 2026 at 2:06 AM PT** via One Legal (Confirmation #35442871) — under court clerk review; case number pending; service after summons issues.

[↑ Contents](#contents)

---

## All Matters

### Active / Open

<!-- PORTFOLIO:ACTIVE_MATTERS:START -->
| # | Caption | Case No. | Court | Type | Status |
|---|---|---|---|---|---|
| 19 | Newanforbi v. Macomber | C2604791 | Santa Clara Sup. Ct. | State | HC-004 filed Sep. 1 — ruling not verified |
| 20 | Newanforbi v. California Highway Patrol, et al. | 26CV191136 | Alameda Sup. Ct. | State | CMC Nov. 4; writ brief Nov. 13; hearing Jan. 8 |
| 22 | Newanforbi v. Pilot Travel Centers LLC | STK-CV-UWT-2026-0007649 | San Joaquin Sup. Ct. | State | Settled Jul. 14, 2026 — terms confidential |
| 24 | Newanforbi v. Serrato | 3:26-cv-05953-CRB | USDC N.D. Cal. (San Francisco Division) | Federal | MTD Dec. 18 10:00 a.m. Zoom (Breyer); CMC continued |
| 25 | Newanforbi v. Federal Express Corporation | 2:26-cv-02881-DAD-SCR | USDC E.D. Cal. (Sacramento Div.) | Federal | Dkt. 10 Sep. 24 — Oct. 8 outcome not verified |
| 26 | Newanforbi v. United Parcel Service, Inc. | 2:26-cv-02847-DAD-CKD | USDC E.D. Cal. (Sacramento Div.) | Federal | MTD under submission — Oct. 7 vacated |
| 27 | Newanforbi v. Randstad, et al. | 26CV199902 | Alameda Sup. Ct. (Rene C. Davidson Courthouse) | State | Settled; dismissal pending |
| 28 | Newanforbi v. Shannon Smith, LCSW, CEO, et al. | 3:26-cv-07504-LJC | USDC N.D. Cal. | Federal | MTD pending — claim preclusion withdrawn |
| 29 | Newanforbi v. Amazon.com Services, LLC | 4:26-cv-09249-ASK | USDC N.D. Cal. (Oakland; formerly 3:26-cv-09249-ASK) | Federal | 26(f) Nov. 6; MTD Nov. 18; CMC Dec. 1 |
| 30 | Newanforbi v. Moua, et al. | TBD | USDC N.D. Cal. | Federal | Pre-filing — Moua v9 ready; GCA (a)(2) window |
| 31 | Newanforbi v. First Advantage LLC | TBD | San Joaquin Sup. Ct. (anticipated) | State | Pre-filing — no demand or complaint yet |
| 32 | Nforbi v. Meza-Gonzalez, et al | 4:26-cv-08271-CRB | USDC N.D. Cal. (4:26-cv-08271-CRB; formerly 26-cv-08271-AMO, 4:26-cv-08271-ASK, and 3:26-cv-08271-PHK; related to Serrato 3:26-cv-05953-CRB) | Federal | CRB; opp. Nov. 9; MTD hearing to re-notice |
| 33 | Nforbi v. Candelaria et al. | 3:26-cv-08272-RFL | USDC N.D. Cal. (San Francisco Div.) | Federal | FAC answered (Dkt 26); 26(f) Nov. 18; CMC Dec. 9 |
| 34 | Newanforbi v. Counseling and Psychotherapy Center, Inc., et al. | TBD | USDC N.D. Cal. (San Jose Div.) / Santa Clara Sup. Ct. | Federal | Pre-filing — intake & compliance monitoring |
| 35 | Ngwa Nforbi v. Ross Stores, Inc., et al. | 26CV501995 | Santa Clara Sup. Ct. (Downtown / First Street) | State | Ross answered; discovery responses Nov. 17 |
| 36 | Brendan Ngwa Nforbi v. AT&T Mobility Services LLC | 2:26-cv-03314-DJC-AC (PS) | USDC E.D. Cal. | Federal | IFP granted / screened in — USM service pending |
| 37 | Brendan Ngwa Nforbi v. Home Depot U.S.A., Inc. | TBD | USDC E.D. Cal. (Sep. 16 walk-up; unfiled) / San Joaquin Sup. Ct. (Sep. 8 packet LOCKED, unfiled) | Federal | EDCA walk-up Sep. 16 — unfiled |
| 38 | Brendan Ngwa Nforbi v. Swift Transportation Co. of Arizona LLC | 2:26-cv-03312-DC-SCR | USDC E.D. Cal. (Sacramento Div.) | Federal | Filed; IFP-or-fee outcome not verified |
| 39 | Brendan Ngwa Nforbi v. Best Buy Co., Inc. | 2:26-cv-03315-DC-CKD (PS) | USDC E.D. Cal. (Sacramento Div.) | Federal | Fee paid Oct. 27; IFP withdrawn as moot |
| 40 | Brendan Ngwa Nforbi v. Uber Technologies, Inc. | TBD | TBD (pre-dispute — offer received Sep. 14, 2026) | State | Start withheld — complaint signed, not filed |
| 41 | Brendan Ngwa Nforbi v. Nuro, Inc. | TBD | TBD (pre-dispute — application Sep. 9, 2026) | State | Pending — no Checkr paper ingested |
| 42 | Brendan Ngwa Nforbi v. Staples The Office Superstore, LLC | 5:26-cv-12781-NW | USDC N.D. Cal. (San Jose Div.) | Federal | Filed Oct. 29 — serve by Jan. 27; CMC Feb. 2 |
| 43 | Brendan Ngwa Nforbi v. Hertz Global Holdings, Inc. | TBD | TBD — no action filed | State | Offer accepted — HireRight screening active |
| 44 | Ngwa Nforbi v. Marriott International, Inc., et al. | TBD | TBD | State | Pre-filing intake |
<!-- PORTFOLIO:ACTIVE_MATTERS:END -->

*Settled matters stay in the table above until dismissal is entered — a settlement resolves the merits, but the matter is still open on the docket. Their Status column reads "Settled" (see the Overview count above for which ones).*

### Dismissed / Closed / Archived

*Matters marked **ABANDONED** were voluntarily withdrawn due to real, credible safety threats.*

<!-- PORTFOLIO:CLOSED_MATTERS:START -->
| # | Caption | Case No. | Court | Disposition |
|---|---|---|---|---|
| 1 | Newanforbi v. CHP et al. | 2:25-cv-01460-DC-CSK | USDC E.D. Cal. | **DISMISSED** — Closed — E.D. Cal.; refiled as Matter 32 |
| 2 | Newanforbi v. Meza-Gonzalez et al. | 26CV168913 | Alameda Sup. Ct. | Dismissed w/o prejudice — Aug. 15, 2026 |
| 3 | Newanforbi v. Derrick et al. | 2:26-cv-00004-DJC-JDP | USDC E.D. Cal. | **ABANDONED** — Closed — E.D. Cal. 2:26-cv-00004 |
| 4 | Newanforbi v. Derrick et al. | TBD | San Joaquin Sup. Ct. | Abandoned — voluntarily dismissed |
| 5 | Newanforbi v. Palacios et al. | STK-CV-UF-2026-0001032 | San Joaquin Sup. Ct. | **DISMISSED** — Judgment entered WOP Nov. 4 — closed |
| 6 | Newanforbi v. HOPE et al. | 2:26-cv-00195-TLN-AC | USDC E.D. Cal. | Dismissed without prejudice — Jun. 1, 2026 |
| 7 | Newanforbi v. Candelaria | 2:26-cv-00983-DC-CSK | USDC E.D. Cal. | Dismissed w/o prejudice — Aug. 15; refiled as Matter 33 |
| 8 | Newanforbi v. Candelaria, et al. | 26WM000135 | Sacramento Sup. Ct. | Abandoned — fee-payment deadline lapsed Jul. 27, 2026 |
| 9 | Newanforbi v. Macomber | 26WM000028 | Sacramento Sup. Ct. | Closed — demurrer sustained May 29, 2026 |
| 10 | Newanforbi v. Macomber | C2602632 | Santa Clara Sup. Ct. | Closed — petition denied w/o prejudice Apr. 27, 2026 |
| 11 | Newanforbi v. Macomber | TBD (USDC E.D. Cal.) | USDC E.D. Cal. | Dismissed with prejudice — Jun. 29, 2026 |
| 12 | Brendan Ngwa Nforbi v. Diamond Truck Sales, Inc. | STK-CV-UF-2026-0001094 | San Joaquin Sup. Ct. | **DISMISSED** — Dismissal filed Oct. 26 — pending closure |
| 13 | Newanforbi v. Urrea et al. | 2:26-cv-00190-DC-SCR | USDC E.D. Cal. | Dismissed with prejudice — Jun. 29, 2026 |
| 14 | Newanforbi v. Urrea et al. | TBD (San Joaquin Sup. Ct.) | San Joaquin Sup. Ct. | Abandoned — voluntarily dismissed |
| 15 | Newanforbi v. California Department of Corrections and Rehabilitation, et al. | STK-CV-UPI-2026-5417 | San Joaquin Sup. Ct. | Abandoned — dismissed with prejudice Jul. 24, 2026 |
| 16 | Newanforbi v. Rojo | TBD (San Joaquin Sup. Ct.) | San Joaquin Sup. Ct. | Abandoned — voluntarily dismissed |
| 17 | Newanforbi v. Maloney et al. | 2:26-cv-00194-DAD-SCR | USDC E.D. Cal. | Dismissed with prejudice — Jun. 29, 2026 |
| 18 | Newanforbi v. Barocio | 2:26-cv-00191-DJC-CSK (PC) | USDC E.D. Cal. | Dismissed with prejudice — Jun. 29, 2026 |
| 21 | Newanforbi v. Rojo et al. | 2:26-cv-00193-DC-CKD | USDC E.D. Cal. | Dismissed with prejudice — Jun. 29, 2026 |
| 23 | Newanforbi v. Macy's Inc. et al. | TBD | San Joaquin Sup. Ct. | Abandoned — no adverse action occurred |
<!-- PORTFOLIO:CLOSED_MATTERS:END -->

[↑ Contents](#contents)

---

## Upcoming Deadlines

*Generated from `timeline` entries with `upcoming: true`.*

<!-- PORTFOLIO:UPCOMING_DEADLINES:START -->
| Date | Matter | Event |
|---|---|---|
| Sep. 17, 2026 | 32 | FILE — summons return / CCP § 415.20(b) declaration + Exhibit A USPS receipt + POS being refiled in Brendan Ngwa Nforbi v. Meza-Gonzalez et al. (4:26-cv-08271-CRB). USER REPORT Oct. 28, 2026. Sep. 17 mailing executed |
| Oct. 1, 2026 | 19 | Habeas ruling calendar (computed) — Newanforbi v. Macomber (C2604791). CRC 4.551(a)(6)(B) runs 30 days from the September 1, 2026 in-person filing of the… |
| Oct. 26, 2026 | 38 | IMPORTANT — DUE — Renewed IFP motion (complete AO 239: monthly income, monthly expenses, assets, all money received in the past 12 months) OR pay the filing fee — Brendan Ngwa Nforbi v. Swift Transportation Company (E.D. |
| Oct. 29, 2026 | 25 | CONTINGENT — FedEx responses to Plaintiff's Interrogatories, RFAs, and RFPs (Set One). Not yet served by mail as of Sep. 25, 2026. |
| Oct. 29, 2026 | 36 | DEADLINE — USM service packet and Notice of Submission in Brendan Ngwa Nforbi v. AT&T Mobility Services LLC (E.D. Cal. 2:26-cv-03314-DJC-AC (PS)). Within 15 days of Dkt. 4 (Oct. 14): deliver to the U.S. |
| Nov. 1, 2026 | 2 | CCP §335.1 two-year statute of limitations (computed) backstop, running from the Nov. 1, 2024 incident. (1) Matter 1's Fourth Amendment §1983 claim (borrowed… |
| Nov. 4, 2026 | 20 | Case Management Conference — Newanforbi v. CHP et al. (26CV191136), Nov. 4, 2026, 4:00 p.m., Dept. 25, Rene C. Davidson Courthouse, Hon. Jenna M. Whitman. USER REPORT Oct. 28, 2026: continued from Oct. 28. |
| Nov. 4, 2026 | 37 | WATCH — Home Depot answer or Rule 12 motion due, Ngwa Nforbi v. Home Depot U.S.A., Inc. (E.D. Cal. 2:26-cv-03310-TLN-AC). Served Oct. 14, 2026 → 21 days (Rule 12(a)(1)(A)(i)). |
| Nov. 5, 2026 | 25 | WATCH — FedEx responses to Plaintiff's Interrogatories, RFAs, and RFPs (Set One) due, Newanforbi v. Federal Express Corporation (E.D. Cal. 2:26-cv-02881-DAD-SCR). |
| Nov. 6, 2026 | 29 | Rule 26(f) / ADR L.R. 3-5 meet-and-confer, Fri. Nov. 6, 2026, 1:00–1:30 p.m. PT (invite sent as 3:00–3:30 p.m. Central), by Microsoft Teams — Newanforbi v. Amazon.com Services, LLC et al. (4:26-cv-09249-ASK). |
| Nov. 9, 2026 | 32 | Opposition to Dkt. 22 motion to dismiss/strike due Nov. 9, 2026 — Brendan Ngwa Nforbi v. Meza-Gonzalez et al. (4:26-cv-08271-CRB). Date set in the Dkt. 22 docket text (responses due 11/9/2026; replies 11/16/2026). |
| Nov. 10, 2026 | 29 | Deadline to file ADR Certification (ADR L.R. 3) and to meet and confer regarding initial disclosures, early settlement, ADR process selection, and a discovery… |
| Nov. 12, 2026 | 32 | ADR Certification (ADR L.R. 3) remains in effect — Brendan Ngwa Nforbi v. Meza-Gonzalez et al. (4:26-cv-08271-CRB), per Dkt. 4 and Serrato Dkt. 34 (Nov. 3, 2026). |
| Nov. 13, 2026 | 20 | Opening memorandum in support of the petition for writ of mandate due Nov. 13, 2026 (hearing Jan. 8, 2027) — Newanforbi v. CHP et al. (26CV191136). Set by the Oct. 26, 2026 Stipulation and Order re Briefing Schedule. |
| Nov. 13, 2026 | 29 | OPTIONAL: last day to request a Zoom appearance for the Nov. 18 Dkt. 19 MTD hearing. Krishnan Civil Standing Order (8/20/26) p.2: law-and-motion hearings are in person |
| Nov. 16, 2026 | 20 | Hand-deliver courtesy copy of the opening memorandum to Dept. 25 (Rene C. Davidson Courthouse) within one court day of filing — Newanforbi v. CHP et al. (26CV191136). Order of Oct. 26, 2026. |
| Nov. 16, 2026 | 24 | Email appearance names to crbcrd@cand.uscourts.gov |
| Nov. 16, 2026 | 32 | WATCH — Defendants' reply in support of Dkt. 22 motion to dismiss/strike due Nov. 16, 2026 per Dkt. 22 docket text — Brendan Ngwa Nforbi v. Meza-Gonzalez et al. (4:26-cv-08271-CRB). Briefing date continues |
| Nov. 17, 2026 | 35 | OPEN TASK — Matter 35: serve verified responses to Ross Form Interrogatories, Special Interrogatories (27), and RFPs (24), Set One (served Oct 15 by mail + email; 30 days + 2 court days, CCP § 1010.6). |
| Nov. 18, 2026 | 29 | Hearing on Dkt. 19 motion to dismiss — Newanforbi v. Amazon.com Services, LLC et al. (4:26-cv-09249-ASK), Nov. 18, 2026, 1:30 p.m., Courtroom 4, 3rd Floor, Hon. Ajay S. Krishnan. |
| Nov. 18, 2026 | 33 | Deadline to file ADR Certification (ADR L.R. 3) and to meet and confer regarding initial disclosures, early settlement, ADR process selection, and a discovery plan (Rule 26(f)) — Nforbi v. |
| Nov. 24, 2026 | 29 | Deadline to make initial disclosures (Fed. R. Civ. P. 26(a)(1)) and to file the Joint Case Management Statement (Standing Order for All Judges of the Northern… |
| Nov. 24, 2026 | 29 | OPTIONAL: request that the Dec. 1 initial CMC be held in person (in the Joint CMC Statement or a separate filing no later than seven days before the conference). Krishnan Civil Standing Order (8/20/26) p.4. |
| Nov. 25, 2026 | 32 | Case Management Statement due — Brendan Ngwa Nforbi v. Meza-Gonzalez et al. (4:26-cv-08271-CRB). Case-management-order deadline continues under Serrato Dkt. 34. |
| Nov. 28, 2026 | 29 | WATCH: Amazon CCPA request-to-know response due (Civ. Code §1798.130(a)(2)(A): 45 calendar days from receipt; extendable once by 45 days with notice). Letter 3 emailed Oct. 14, 2026, 2:48 p.m. |
| Dec. 1, 2026 | 29 | Initial Case Management Conference, 1:30 p.m. by Zoom (cand.uscourts.gov/ask) before Magistrate Judge Ajay S. Krishnan — Newanforbi v. Amazon.com Services, LLC… |
| Dec. 2, 2026 | 33 | Deadline to make initial disclosures and file the Case Management Statement — Nforbi v. Candelaria et al. (3:26-cv-08272-RFL), per Sep. 28 PACER true-up. |
| Dec. 9, 2026 | 33 | Initial Case Management Conference, 10:00 a.m. before Hon. Rita F. Lin — Nforbi v. Candelaria et al. (3:26-cv-08272-RFL). |
| Dec. 11, 2026 | 12 | Further Case Management Conference, 8:30 AM, Dept. 11B, Hon. Robert T. Waters — Ngwa Nforbi v. Diamond Truck Sales, Inc. et al. (STK-CV-UF-2026-0001094). |
| Dec. 11, 2026 | 20 | WATCH — Respondents' opposition due Dec. 11, 2026 — Newanforbi v. CHP et al. (26CV191136). Set by the Oct. 26, 2026 Stipulation and Order re Briefing Schedule. |
| Dec. 17, 2026 | 27 | Case Management Conference, Newanforbi v. Randstad US LLC and RK Logistics Group, Inc. (Matter 27) — Hon. Thomas Weathers, Dept. 20, Rene C. Davidson… |
| Dec. 17, 2026 | 28 | Joint status conference report due Dec. 17, 2026 (monthly through May 17, 2027) — Newanforbi v. Smith / HOPE (3:26-cv-07504-LJC). USER REPORT of the Oct. 27, 2026 order deferring the MTD pending San Joaquin judgment. |
| Dec. 18, 2026 | 20 | Reply due Dec. 18, 2026 on the petition for writ of mandate — Newanforbi v. CHP et al. (26CV191136). Set by the Oct. 26, 2026 Stipulation and Order re Briefing Schedule. |
| Dec. 18, 2026 | 24 | MTD FAC (Dkt. 18) Zoom before Judge Breyer — Dec. 18, 2026, 10:00 a.m. PT (Dkt. 33) |
| Dec. 21, 2026 | 20 | Hand-deliver courtesy copy of the reply to Dept. 25 (Rene C. Davidson Courthouse) within one court day of filing — Newanforbi v. CHP et al. (26CV191136). Order of Oct. 26, 2026. |
| Jan. 7, 2027 | 20 | WATCH — Tentative ruling posts (afternoon); read it. To argue, follow Dept. 25 contest procedure. |
| Jan. 8, 2027 | 20 | HEARING — Motion for peremptory writ of mandate, 9:00 a.m., Dept. 25, Hon. Jenna M. Whitman (Reservation ID 958052306492). |
| Jan. 12, 2027 | 35 | OPEN TASK — Matter 35 (26CV501995) meet-and-confer with appearing parties at least 30 calendar days before the Feb. 11, 2027 CMC (Santa Clara Civil Lawsuit… |
| Jan. 12, 2027 | 36 | WATCH — U.S. Marshal 90-day service deadline in Brendan Ngwa Nforbi v. AT&T Mobility Services LLC (E.D. Cal. 2:26-cv-03314-DJC-AC (PS)) (Dkt. 4; Fed. R. Civ. P. 4(m); 90 days from Oct. 14, 2026). |
| Jan. 12, 2027 | 42 | Last day to meet and confer re initial disclosures, early settlement, ADR process selection, and discovery plan (FRCP 26(f)) — Dkt. 5 Order, Ngwa Nforbi v. Staples The Office Superstore, LLC (N.D. Cal. 5:26-cv-12781-NW). |
| Jan. 12, 2027 | 42 | File ADR Certification (ADR L.R. 3-5) — Dkt. 5 Order, Ngwa Nforbi v. Staples The Office Superstore, LLC (N.D. Cal. 5:26-cv-12781-NW). ADR Multi-Option Program (ADR L.R. 3) |
| Jan. 17, 2027 | 28 | Joint status conference report due Jan. 17, 2027 (monthly through May 17, 2027) — Newanforbi v. Smith / HOPE (3:26-cv-07504-LJC). USER REPORT of the Oct. 27, 2026 order deferring the MTD pending San Joaquin judgment. |
| Jan. 26, 2027 | 42 | Serve FRCP 26(a)(1) initial disclosures — Dkt. 5 Order, Ngwa Nforbi v. Staples The Office Superstore, LLC (N.D. Cal. 5:26-cv-12781-NW). |
| Jan. 26, 2027 | 42 | File Joint Case Management Statement (Standing Order for All Judges of the N.D. Cal.) — Dkt. 5 Order, Ngwa Nforbi v. Staples The Office Superstore, LLC (N.D. Cal. 5:26-cv-12781-NW). |
| Jan. 27, 2027 | 35 | OPEN TASK — File and serve Case Management Statement (CM-110) in Matter 35 (26CV501995) at least 15 calendar days before the Feb. 11, 2027 CMC. |
| Jan. 27, 2027 | 42 | SERVE Staples — FRCP 4(m) 90-day service deadline (computed: complaint filed Oct. 29, 2026 + 90 days), Ngwa Nforbi v. Staples The Office Superstore, LLC (N.D. Cal. 5:26-cv-12781-NW). |
| Feb. 2, 2027 | 42 | INITIAL CASE MANAGEMENT CONFERENCE, 9:00 a.m., Courtroom 3, Hon. Noel Wise — Ngwa Nforbi v. Staples The Office Superstore, LLC (N.D. Cal. 5:26-cv-12781-NW). |
| Feb. 11, 2027 | 35 | CASE MANAGEMENT CONFERENCE — Ngwa Nforbi v. Ross Stores, Inc., et al. (Matter 35, Santa Clara Sup. Ct. No. 26CV501995), Hon. Vince Parrett, Dept. 16 (stamp… |
| Feb. 11, 2027 | 35 | OPEN TASK — Matter 35: post Plaintiff's $150 jury fee (or confirm fee-waiver coverage) on or before initial CMC (CCP § 631(c)(2)). |
| Feb. 17, 2027 | 28 | Joint status conference report due Feb. 17, 2027 (monthly through May 17, 2027) — Newanforbi v. Smith / HOPE (3:26-cv-07504-LJC). USER REPORT of the Oct. 27, 2026 order deferring the MTD pending San Joaquin judgment. |
| Mar. 1, 2027 | 30 | Gov. Code §945.6(a)(2) two-year suit period (computed) — Bane Act and IIED state-law claims, Newanforbi v. Moua, et al. (Matter 30). |
| Mar. 17, 2027 | 28 | Joint status conference report due Mar. 17, 2027 (monthly through May 17, 2027) — Newanforbi v. Smith / HOPE (3:26-cv-07504-LJC). USER REPORT of the Oct. 27, 2026 order deferring the MTD pending San Joaquin judgment. |
| Apr. 17, 2027 | 28 | Joint status conference report due Apr. 17, 2027 (monthly through May 17, 2027) — Newanforbi v. Smith / HOPE (3:26-cv-07504-LJC). USER REPORT of the Oct. 27, 2026 order deferring the MTD pending San Joaquin judgment. |
| May 17, 2027 | 28 | Joint status conference report due May 17, 2027 (monthly through May 17, 2027) — Newanforbi v. Smith / HOPE (3:26-cv-07504-LJC). USER REPORT of the Oct. 27, 2026 order deferring the MTD pending San Joaquin judgment. |
| Jun. 10, 2027 | 28 | Joint Case Management Conference statement due June 10, 2027 — Newanforbi v. Smith / HOPE (3:26-cv-07504-LJC). USER REPORT of the Oct. 27, 2026 order. Order is Dkt. 38 (filed Oct. 27, 2026; minute entry Dkt. 37) |
| Jun. 17, 2027 | 28 | Case Management Conference — Newanforbi v. Smith / HOPE (3:26-cv-07504-LJC), June 17, 2027, 1:30 p.m., Hon. Lisa J. Cisneros. USER REPORT of the Oct. 27, 2026 order deferring the MTD. |
| Jul. 27, 2028 | 29 | OUTER BOUND (conservative, computed) — FCRA (15 U.S.C. §1681p: 2 years from discovery, 5 years from violation) and ICRAA (Civ. |
<!-- PORTFOLIO:UPCOMING_DEADLINES:END -->

[↑ Contents](#contents)

---

## Damages Summary

<!-- PORTFOLIO:DAMAGES_SUMMARY:START -->
| Category | Matters | Conservative | Moderate | Aggressive |
|---|---|---|---|---|
| Lost Wages / Economic Harm | 1, 2, 7, 22 | $20,000 | $130,000 | $334,000 |
| False Imprisonment | 1, 2 | $40,000 | $85,000 | $215,000 |
| Emotional Distress | 1, 2, 5, 7, 22, 24 | $0 | $20,000 | $115,000 |
| Bane Act / Treble | 1, 2 | $15,000 | $50,000 | $70,000 |
| Punitive Damages | 1, 2, 7, 22, 24 | $30,000 | $120,000 | $450,000 |
| Consumer Fraud | 12 | $78,672 | $110,072 | $200,272 |
| Attorneys' Fees | 1, 7, 22, 24 | $28,000 | $45,000 | $70,000 |
| PC §290.46(j) Violation + Wrongful Termination (Matter 22) | 22 | $220,000 | $525,000 | $1,000,000 |
| 42 USC §1983 — Arbitrary U Visa Certification Denial & Retaliation (Matter 24) | 24 | $75,000 | $200,000 | $450,000 |
| PC §290.46(j) Failure to Hire — FedEx / UPS (Matters 25, 26) | 25, 26 | $75,000 | $180,000 | $420,000 |
| PC §290.46(j) — Wrongful Termination / Failure to Employ — Randstad / RK Logistics (Matter 27) | 27 | $155,000 | $387,000 | $734,000 |
| §1983 Monell / Individual + Bane Act + RICO — Shannon Smith / HOPE (Matter 28) | 28 | $249,000 | $666,000 | $1,510,000 |
| PC §290.46(j) Failure to Hire — Amazon (Matter 29) | 29 | $30,000 | $75,000 | $180,000 |
| §1983 Retaliation, Due Process, Bane Act & IIED — Moua (Matter 30) | 30 | $90,000 | $225,000 | $525,000 |
| Conditional CRA Investigation — First Advantage LLC (Matter 31) | 31 | $0 | $0 | $0 |
| N.D. Cal. §1983 Meza-Gonzalez (Matter 32) — pleaded >$214k; $0 here to avoid double-count w/ M1/M2 | 32 | $0 | $0 | $0 |
| N.D. Cal. §1983 Nforbi v. Candelaria et al. (Matter 33, 3:26-cv-08272-RFL, formerly LJC) — pleaded >$214k; $0 here to avoid double-count w/ M7 | 33 | $0 | $0 | $0 |
| §1983 Monell / Individual + Bane Act — Counseling & Psychotherapy Center (Matter 34) | 34 | $0 | $0 | $0 |
| Unruh / False Imprisonment / Negligent Training — Ross Stores (Matter 35) | 35 | $115,000 | $345,000 | $1,035,000 |
| FCRA / §290 failure-to-hire — AT&T / Home Depot / Swift / Best Buy (36–39) | 36, 37, 38, 39 | $235,000 | $360,000 | $485,000 |
| **Portfolio Total (pre-deduplication)** | | **$1,455,672** | **$3,523,072** | **$7,793,272** |
<!-- PORTFOLIO:DAMAGES_SUMMARY:END -->

*Note: The portfolio total reflects independent per-defendant exposure across all matters before deduplication of shared economic events (e.g., the same CDL wage-loss period underlying Matters 1, 2, 7, 15). Per-matter settlement negotiations treat each defendant independently.*

*Matter 22 (Pilot) settled July 14, 2026 — terms confidential per settlement agreement. Matters 32 and 33 plead compensatory damages exceeding $214,000 in their N.D. Cal. complaints; the $0 rows above keep the portfolio damages table from double-counting the same Nov. 1 / APS economic loss already modeled in Matters 1, 2, and 7. Matters 36–39 are post-favorable-MTD settlement figures for the executed San Joaquin packets, not confirming-report valuations and not sent demands.*

*Matters 3 (Derrick), 5 (Palacios), and 15 (CDCR/Dodd/Noguchi) have been excluded/reduced above following their abandonment or dismissal. Matter 3's Lost Income, Emotional Distress, Punitive, and Fees components; Matter 5's Lost CDL Wages, Bane Act/Treble, Punitive, and Fees components; and Matter 15's Lost CDL Wages, Liberty Deprivation, Emotional Distress, and Punitive components were all subtracted from their matching rows. Two gaps are worth flagging: Matter 5's own damages breakdown has no dedicated Emotional Distress line item, so that row still carries its unquantified share; and Matter 15's Out-of-Pocket Compliance Costs ($20K/$40K/$60K) and Retaliatory Transfer Losses ($15K/$30K/$64K) components never had a matching category row at all, so removing Matter 15 pulls more out of the Per-Matter total than out of this table. The Emotional Distress row's conservative estimate would have gone negative after Matter 15's subtraction (already reduced by Matter 3's share); it's floored at $0 rather than shown negative. Matter 30 (Moua) is included above at full value — it is pending, not abandoned; see the Cluster 2 notes.*

[↑ Contents](#contents)

---

## Attorney Fees Analysis

<!-- PORTFOLIO:ATTORNEY_FEES:START -->
Plaintiff is representing himself pro se across all 43 matters. The figures below represent what he would have been required to spend on private counsel to litigate this portfolio — costs he has absorbed entirely through self-representation. Based on real page counts extracted from 779 documents / 7,900 pages across matters with uploaded filings (Matter 32: 122 PDFs / 1,135 pages — N.D. Cal. ndcal/ filing billed; from-01|02|20|24/ stay attributed to source matters; Matter 33: 33 PDFs / 435 pages — N.D. Cal. refile + Nov. 1 / APS evidence; from-07/from-08 drafting stays on Matters 7/8; Matter 31 has no uploaded PDFs of its own), classified by document type and priced at a blended rate of **$280/hour** (senior partner $350–$450 / mid-associate $250–$350 / paralegal $150–$200). Opposing-party filings billed at light review rate only. Fee analysis date: October 28, 2026.

| Cluster | Matters | Low | Mid | High |
|---|---|---|---|---|
| CHP / DUI / DMV | 1, 2, 7, 8, 20, 24, 32, 33 | $175,056 | $233,912 | $292,768 |
| Parole Retaliation / HOPE | 3, 4, 5, 6, 11, 13, 14, 15, 16, 17, 18, 21, 28, 30, 34 | $474,712 | $626,752 | $782,992 |
| Consumer Fraud / Employment | 12, 22, 23, 25, 26, 27, 29, 31, 36, 37, 38, 39, 40, 41, 42, 43 | $198,156 | $278,390 | $358,596 |
| Administrative Writs & Habeas | 9, 10, 19 | $41,580 | $57,890 | $74,200 |
| Public Accommodation / Unruh | 35 | $15,680 | $21,840 | $28,000 |
| **Portfolio Total** | **43 matters** | **$905,184** | **$1,218,784** | **$1,536,556** |
| **Estimated Hours** | | **3,232.8 hrs** | **4,352.8 hrs** | **5,487.7 hrs** |

*Plaintiff has litigated all 43 matters pro se, absorbing the full economic equivalent of the above without compensation. Fee-shifting statutes (42 U.S.C. §1988, PC §290.46(j)(4)(A), RICO 18 U.S.C. §1964(c), FCRA, ICRAA) apply across the majority of active matters — mandatory fee recovery upon prevailing substantially offsets or eliminates the above costs.*
<!-- PORTFOLIO:ATTORNEY_FEES:END -->

[↑ Contents](#contents)

---

## Legal Theories

1. **First Amendment Retaliation as the Catalyst** — Derrick's explicit "you do not have freedom of speech" statement satisfies the *Rhodes v. Robinson* chilling effect test and anchors the retaliation cascade across multiple matters.

2. **HOPE Program Structural Incentive Misalignment** — Fee-for-service billing (~$9,690–$10,600/yr per parolee) with no completion bonus creates a documented financial incentive to retain rather than discharge. Condemned in *In re Dwyer* (SC-080355A, 2023) and *ACSOL v. Macomber*. Now forms the Monell theory in Matter 28.

3. **HOPE as State Actor under West v. Atkins** — CDCR vendor contract + mandatory parole condition + direct compliance reporting pipeline to parole agents (Form 3043) establish state-actor status under *West v. Atkins*, 487 U.S. 42 (1988). Central to Matter 28.

4. **Race-Based Disparate Treatment** — Sworn declarations from a white comparator parolee (favorable treatment) and a Black parolee (hostile treatment) under Agent Derrick establish an Equal Protection claim.

5. **Compounding Constitutional Harms** — Retaliation → unemployment → unemployment cited as retention basis → continued parole custody → blocked re-employment. Each matter reinforces damages in the others.

6. **Post-Notice Continuation (Punitive Damages)** — Defendants maintained their conduct after *In re Dwyer* (2023), *ACSOL v. Macomber* (2023), and the April 2025 statutory amendments (15 CCR § 3574), supporting conscious disregard under Cal. Civ. Code § 3294.

7. **Weaponization of Clinical Authority as Retaliation** — The February 18, 2026 CTM report's explicit "fixation on lawsuits" language strips the denial of titration from protected clinical discretion and constitutes direct documentary evidence of retaliation.

8. **Facially Defective Discharge Review as Independent Tort** — The "Eagan" copy-paste error in Noguchi's review proves no individualized assessment occurred. The 6.5-year retention minimum is sourced from academic literature (Cortoni et al. 2010), not statute. W-2 records from 6 CDL carriers document $109,408 in lost wages.

9. **Policy 19-03 as Ultra Vires Action** — Policy 19-03 is affirmatively contradictory to 15 CCR § 3574 (effective April 2025). Regulations have the force of statute (*Tidewater Marine*). *Mathews v. Eldridge* balancing confirms a due process violation.

10. **PC §290.46(j)(2)(E) Pattern Across Five Employers** — Matter 22 (Pilot, settled July 14, 2026), Matter 25 (FedEx, served), Matter 26 (UPS, served), Matter 27 (Randstad/RK Logistics, served), Matter 29 (Amazon + Accurate Background, filed July 28, 2026 / both served July 31, 2026; removed Aug. 31, 2026 to N.D. Cal. **3:26-cv-09249-ASK**). Matter 22's settlement confirms the statutory claim is viable; Matter 27's InfoMart report (Billing Code "RK LOGISTICS") is the strongest single evidence set; Matter 29 adds a Fair Chance Act (Gov. Code §12952) count alongside §290.46(j). **Lerma corrected:** in *Lerma v. Amazon.com Services, LLC et al.*, No. 8:22-cv-01727 (C.D. Cal.), the PC §290.46(j) claim was dismissed at the pleading stage (May 26, 2023); the Sept. 29, 2023 settlement resolved a surviving Fair Chance Act claim against Amazon only — useful notice / Fair Chance precedent, not a settled Megan's Law judgment against Amazon or Accurate Background. **Matter 27's July 21, 2026 denial letter** (Garcia & Gurney, ALC) argued Randstad-was-the-employer and MVR-based rejection; neither ground reaches Randstad's unanswered FCRA waiting-period violation, and the MVR defense cites a commercial Class A disqualification inapplicable to the Class C position.

11. **Consumer Reporting Agency Liability for Registry-Flagged Reports (Matter 31)** — First Advantage LLC generated and transmitted the registry-flagged background reports and every pre-adverse/adverse notice underlying both Matter 25 (FedEx, March 2025) and Matter 26 (UPS, July 2024) — an identical notice template and cadence, eight months apart, for two different employers — yet was never itself joined as a defendant in either matter, unlike the comparable vendors elsewhere in the same cluster (Accurate Background, Matter 29; HireRight, the abandoned Matter 23). This theory targets the vendor's own furnishing conduct under FCRA §§1681b(b) and 1681e(b) and ICRAA, rather than the employers' use of the reports, and is pled as additive to — not duplicative of — Matters 25 and 26.

12. **N.D. Cal. Refile of the Nov. 1 / APS Cluster (Matters 32 & 33)** — Both matters were docketed August 10, 2026 as **3:26-cv-08271-PHK** (Matter 32; related/reassigned as 4:26-cv-08271-ASK) and **3:26-cv-08272-LJC** (Matter 33). Matter 7 was dismissed without prejudice on August 15, 2026. Matter 32 brings six §1983 counts against the arresting CHP officers under the Ngwa Nforbi name form on the DS-367; Matter 33 brings the APS structural-bias / vacatur theory against Candelaria and Gordon. Both plead compensatory damages exceeding $214,000. Portfolio damages rows for 32/33 remain $0 so the shared CDL wage-loss period is not triple-counted against Matters 1, 2, and 7.

[↑ Contents](#contents)

---

## Tech Stack

- **Languages:** TypeScript + JavaScript (the app, mid-migration to TS — new modules should be `.ts`/`.tsx`), CSS, Python 3.11 (the document-automation scripts), YAML (the three CourtListener workflows)
- **Framework:** React 19
- **Build tool:** Vite 8
- **Linting:** ESLint 9 flat config (`eslint.config.js`) for JS/TS, ruff (`pyproject.toml`) for Python — ESLint runs in the `pre-push` hook; run `ruff check .` by hand
- **Deployment:** Vercel, on a schedule (see Deployment). GitHub Pages holds the last-published PDF library only.
- **CI:** none. The `pre-push` hook runs the gate locally; see [Local Development](#local-development).
- **Fonts:** Cormorant Garamond (headings), DM Sans (UI)
- **Styling:** `internal/src/styles/app.css` + component styles
- **Matter data:** `internal/src/data/matters/NN/` (split: identity + sibling tables). Index: `internal/src/data/index/matters.json`. The open SPA and D1 seed both run `publishMatter()` — shell `summaries.json` plus lazy `publish/NN.json`. Laptop `loadMatters()` / `npm run q` keep the full graph. Structured fields (prefer over parsing prose `status`):
  - `lifecycle` — disposition: `active` | `pre_filing` | `settled` | `dismissed` | `abandoned` | `closed`
  - `proceeding` — track: `state_civil` | `federal_civil` | `mandate` | `habeas`
  - `phase` — current stage on that track (e.g. `demurrer`, `fr_pending`, `under_submission`, `responsive_deadline`; `terminal` when disposed)
- **Timeline:** `clocks.json` is the live calendar; `timeline.json` is the archive (CourtListener still writes it). Generated `upcoming.json` feeds the shell deadline clock.
- **Documents:** canonical public tree is `documents/` (mirrors `/documents/matter-NN/...`). Phone-tap slugs stay in `internal/public/{slug}.pdf`. The 14-path private denylist lives under `internal/private/documents/` and is auth-only on the Worker. Without the full library on disk, `PORTFOLIO_SKIP_DISK_DOCS=1` checks paths against `internal/src/data/documents/manifest.json`. See [DOCUMENT_STORE.md](internal/docs/DOCUMENT_STORE.md) and [CANONICAL_DOCUMENT_STORE.md](internal/docs/CANONICAL_DOCUMENT_STORE.md).

### Graph (records, not a diary)

Crawl `internal/src/data/index/matters.json`, then the sibling file the question needs. `docket.json` is pleadings; `documents.json` is the file inventory; `clocks.json` is the live calendar. `events.jsonl` is append-only. Never invent a docket number. `{filed: true, dkt: 18}` is on file; a draft is not. README tables are generated (`npm run generate:readme`) — do not keep them in sync by hand. Schema is a contract for shape (`internal/src/data/index/schema.json`), not a speed limit. `status_label` is a 60-character UI chip. Word counts are advisory (`npm run report:prose`), not a schema fail.

On screen, prose over ~320 characters renders through `CollapsibleProse`, which clamps to a few lines with a "Show full …" toggle. That is display only. Nothing is truncated in the DOM — print, find-in-page, and the Markdown export still see the whole record.

## Documents & MCP

Public PDFs live under `documents/` in the repo and in R2. Any MCP-capable
model (ChatGPT, Claude, Cursor, others) points at:

`https://litigation-doc-api.ss8sxswwkt.workers.dev/mcp`

Reads do not need a token. Fourteen paths are auth-only (HOPE_000 discovery
+ two matter-12 card-authorization forms); everything else stays public.
Write tools need OAuth/`write` scope. Connection steps, example prompts,
and the denylist: [CANONICAL_DOCUMENT_STORE.md](internal/docs/CANONICAL_DOCUMENT_STORE.md).

Example: “List documents for matter 24, then read the first amended complaint as text.”

## Citation Verification

Authority quality is a liability surface: claims are cognizable and motions to dismiss are more likely to be denied. Locating a cite in a PDF is not enough — every load-bearing authority must **exist** and support the proposition claimed. The portfolio runs a four-stage funnel; `npm run validate` enforces the known-bad gate.

| Stage | Command | Output |
|---|---|---|
| 1. Index | `npm run citations:index` | `internal/docs/citation_index.json` / `CITATION_INDEX.md` — every cite keyed to page + filing role |
| 2. Lookup | `npm run citations:lookup:matter -- --matter N` | CourtListener + CAP `static.case.law` existence probe → `citation_lookup_matterNN.json` |
| 3. Overlay | edit `citation_verification_rounds.json` | Fold lookup consensus into statuses (existence `FOUND` can clear `UNVERIFIED`; proposition `MISCITED` / `MISCHARACTERIZED` stays) |
| 4. Ledger + gate | `npm run citations:verify` then `citations:check` | `citation_verification.json` / `CITATION_VERIFICATION.md`; the `pre-push` gate fails on **new** fabricated cites in plaintiff filings |

Controls (reconfirm when batching): *Richardson v. McKnight*, 521 U.S. 399 must resolve; *In re Leman*, 66 Cal.App.5th 200 must not. Justia is Cloudflare-blocked here; Google Scholar is unreliable; prefer CourtListener search + CAP static metadata/HTML.

### Scoreboard (paired authorities)

<!-- PORTFOLIO:CITATION_SCOREBOARD:START -->
| Status | Count |
|---|---|
| VERIFIED | 463 |
| MISCITED | 30 |
| MISCHARACTERIZED | 6 |
| NOT_FOUND | 4 |
| UNVERIFIED | 484 |

Paired authorities: **987**. P0 (plaintiff-only UNVERIFIED): **8**. P1 (plaintiff-only bad status): **29**. Ledger date: 2026-10-07.
<!-- PORTFOLIO:CITATION_SCOREBOARD:END -->

Priority queues from the ledger: **P0** = plaintiff-only + still `UNVERIFIED` (`npm run citations:queue`); **P1** = plaintiff-only + bad status (fix before the next brief). Pre-existing fabricated hits are debt-tracked in `citation_known_bad_debt.json` so the gate stays green while corrected drafts replace them.

Full reports: [`CITATION_INDEX.md`](internal/docs/CITATION_INDEX.md) · [`CITATION_AUDIT.md`](internal/docs/CITATION_AUDIT.md) · [`CITATION_VERIFICATION.md`](internal/docs/CITATION_VERIFICATION.md) · Matter 28 safe list [`MATTER_28_SAFE_CITE_LIST.md`](internal/docs/MATTER_28_SAFE_CITE_LIST.md). Claude Code sessions pick this up through the `citation-verify` skill in `.claude/skills/`.

**KeyCite treatment flags (Westlaw).** The scripted funnel covers existence + pin verification; KeyCite treatment flags are the one gap no free source fills. Westlaw access runs only through the San Diego Law Library's Patron Access (never the generic westlaw.com door, which demands a registration key), and it is not scriptable — treatment checks are manual browser spot-checks, batched per frozen draft. Full entry route, seat limits, URL patterns, and the post-draft workflow: [`WESTLAW_PATRON_ACCESS.md`](internal/docs/WESTLAW_PATRON_ACCESS.md).

[↑ Contents](#contents)

---

## CourtListener bridge

Federal matters bind to a stable CourtListener `docket_id` and ingest new PACER/RECAP entries as portfolio facts. Confirmed filings and orders can enter [`timeline.json`](internal/src/data/timeline.json). **Deadlines cannot** — they land in [`courtlistener/review.json`](internal/src/data/courtlistener/review.json) until approved. Run the sync on the laptop; it does not write to `main` from a workflow.

```bash
npm run court:resolve              # bind docket_id (Search API; token optional)
npm run court:sync -- --bootstrap  # first ingest: matters 24, 25, 26, 28, 29, 32, 33
npm run court:sync -- --active-only
npm run court:sync -- --since 2026-07-01 --bootstrap
```

Empty cursors refuse a full historical crawl unless you pass `--bootstrap`, `--active-only`, `--matter N`, or `--all`. Store `COURTLISTENER_TOKEN` in a gitignored `.env` (`COURTLISTENER_API_TOKEN` is accepted as an alias). Never put it in a `VITE_*` variable. Design notes: [`COURTLISTENER.md`](internal/docs/COURTLISTENER.md).

[↑ Contents](#contents)

---

## Local Development

```bash
npm install
npm run documents:pull   # fill internal/public/documents/ from origin/documents
npm run dev
```

Open http://localhost:5173/

Useful scripts:

```bash
npm run next                  # ranked "what's next to do" queue (see below)
npm run sync:summaries        # rebuild light matter summaries + document search index
npm run sync:registry         # rebuild path → label catalog
npm run sync:manifest         # sha256 inventory of public/documents (hashes only new/resized files)
npm run documents:pull        # restore PDFs from the documents branch (after clone)
npm run documents:push        # publish local PDFs to origin/documents
npm run sync:upcoming         # rebuild upcoming.json from clocks.json for the shell
npm run report:prose          # advisory word-count / docket-log report (not a schema fail)
npm run generate:readme       # regenerate marked README tables from portfolio data
npm run lint                  # ESLint over internal/src + internal/scripts
npm run lint:fix              # ...and auto-fix what is safely fixable
npm run gate                  # same six steps as pre-push (lint, typecheck, validate-portfolio, golden, vitest, citation)
npm run validate              # fuller check: lint + generated-file --check + schema + citations:check + coverage
npm run citations:index       # rebuild page-keyed citation index from PDFs
npm run citations:verify      # rebuild verification ledger
npm run citations:check       # known-bad gate (also run by validate)
npm run citations:queue       # print P0 plaintiff-only UNVERIFIED queue
npm run citations:lookup:matter -- --matter 20   # Citation Lookup + CAP probe for one matter
npm run court:resolve             # bind federal matters to CourtListener docket_id
npm run court:sync -- --bootstrap # first ingest of the seven live federal matters
npm run scaffold:matter -- 34 "Newanforbi v. Example"
```

### Next-actions monitor

`npm run next` answers "what's next on the list for me to do?" from the data
rather than from the generated README table above. It reads every `timeline.json`
entry still flagged `upcoming: true`, resolves matter captions from
`matters/summaries.json`, and ranks the result: past-due first, then the next 3
days, this week, and the rest of the horizon. Nothing is written to disk, so the
output cannot go stale the way a synced file can.

```bash
npm run next                  # 30-day horizon
npm run next -- --days 7      # tighter window
npm run next -- --all         # every upcoming entry, no horizon
npm run next -- --mine        # drop opposing-party and court/agency clocks
npm run next -- --matter 20   # one matter
npm run next -- --json        # same ranking, machine-readable
```

Within each urgency band, this litigant's own obligations sort ahead of dates
that run against someone else — an AG reply deadline or a CCP §430.41 demurrer
meet-and-confer is a date to watch, not a task. That ownership is inferred from
the event text and labelled `inferred — verify`; pin it by adding
`"actor": "you" | "opposing" | "agency"` to the timeline entry, and the script
uses the explicit value instead. Upcoming flags that only touch archived or
closed matters are skipped (with a count) rather than ranked as PAST DUE.

Two sections follow the bands: upcoming entries whose date can't be placed on one
calendar day (month-only or ranged), and active matters with no dated next step
at all — the coverage gap that a deadline table can't show you.

Claude Code sessions in this repo pick this up automatically through the
`whats-next` skill in `.claude/skills/`, so asking "what's next?" — or any
variation of it — runs the monitor instead of reading dates off the README.

### Python document scripts

The PDF/Word generators and auditors under `internal/scripts/` are run directly
and are independent of the web app — install their dependencies only when you
need them:

```bash
python3 -m pip install -r requirements.txt   # reportlab, pypdf, pymupdf, …
ruff check .                                 # lint (not run by any hook — run it yourself)
internal/scripts/ensure-pdf-tools.sh         # tesseract-ocr + the same pip install
```

OCR (`internal/scripts/ocr-text-layer.py` and `internal/scripts/pdf-audit/ocr.py`)
needs the `tesseract` binary on `PATH`. `ensure-pdf-tools.sh` installs it via
`apt-get` when missing (Debian/Ubuntu) and is safe to re-run. Nothing automated
lints or runs the Python scripts; `ruff check .` and `python -m compileall -q internal/scripts`
are the manual equivalents of the old CI job.

## Build

```bash
npm run build   # outputs to dist/ (copies public/documents unless VITE_COPY_DOCUMENTS=0)
npm run preview # preview the production build locally
```

Vercel builds with `VITE_COPY_DOCUMENTS=0` and `PORTFOLIO_SKIP_DISK_DOCS=1` so they never fetch or copy the PDF library; `/documents/*` is rewritten to the Cloudflare Worker that maps path → sha256. Details: [DOCUMENT_STORE.md](internal/docs/DOCUMENT_STORE.md).

## Deployment

**Vercel** serves production from the domain root, but **does not deploy on push**. The committed `vercel.json` sets `git.deploymentEnabled: false`; production advances when the scheduled Deploy Hook fires (Cloudflare Worker in `internal/workers/vercel-deploy-cron/`, four times a day, only if `main` is ahead of what is live) or when you trigger it by hand. Vercel's Ignored Build Step runs `internal/scripts/vercel-ignore-build.sh`, which skips any build whose inputs did not change. `/documents/:path*` is rewritten to the Cloudflare Worker so the Vercel build does not copy 660 MB of PDFs. Dashboard settings, cost model, and the "deploy now" commands are in [VERCEL_DEPLOYS.md](internal/docs/VERCEL_DEPLOYS.md). After a fresh clone, run `npm run documents:pull` before `npm run dev`.

**GitHub Pages** is no longer deployed. Phone taps are the `/{slug}.pdf` copies on Vercel. New PDFs from `npm run documents:push` go to R2 (when `R2_*` is set) and to the `documents` branch as a cold backup. The Worker serves `/documents/<path>` after the path index is published. `vite.config.js` keeps the `GITHUB_PAGES` base-path switch for a manual Pages build if one is ever needed.

**Pre-push gate.** There are no GitHub Actions workflows. `.githooks/pre-push` and `npm run gate` run the same fail-closed checks before `main`: lint, typecheck, `validate-portfolio`, golden damages math, the unit suite, and the fabricated-citation gate. `npm run prepare` installs the hook (`core.hooksPath = .githooks`). Missing `node_modules` or `python3` refuses the push. `SKIP_PORTFOLIO_GATE=EMERGENCY git push` may skip the hook on a feature branch only; a push that updates `refs/heads/main` cannot bypass. Phase 2 remote status is the Cloudflare Worker in `workers/portfolio-gate/` (Check Run `portfolio-gate` on PRs targeting `main`). Branch protection on `main` should require a PR, block force pushes, and — after that Worker is deployed — require the `portfolio-gate` check (Worker-posted, not Actions). See [WORKFLOW_NOTES.md](.github/WORKFLOW_NOTES.md).

**Dependencies.** Do not restore Dependabot (it runs on Actions runners). Weekly: `npm run deps:outdated`, then `npm run deps:update` for in-range npm. Optional PR factory is the Mend Renovate GitHub App using `.github/renovate.json` — see [WORKFLOW_NOTES.md](.github/WORKFLOW_NOTES.md).

---

*Public filings and a redacted docket view. The open Vercel site and Worker reads ship captions, court-facing clocks, and filed / phone-tap PDFs only. The full case graph stays laptop-only (`npm run q` / `npm run mcp`).*
