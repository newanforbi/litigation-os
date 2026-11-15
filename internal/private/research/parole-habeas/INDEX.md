# Parole / habeas workspace — INDEX

**Classification:** internal/private only. Do not copy into the public SPA, Worker/D1, README matter tables, fuse board, or any paper Plaintiff will send or file.

**As of:** 2026-10-28 (portfolio true-up PR #1039 on `main`). This folder is a research consolidation, not a live calendar. Clocks remain in each matter’s `clocks.json`.

**Petitioner:** Brendan Ngwa Nforbi / Brendan Ngehsi Newanforbi. CDC No. **BF3571**. Underlying criminal case: Santa Clara County Superior Court **C1761642**.

**Do not disclose** any Randstad (Matter 27) settlement figure in this workspace or anywhere defense counsel can see it.

---

## How to use this folder

| File | Job |
|---|---|
| `INDEX.md` (this file) | Every parole-touching matter, court, case no., status, key orders, deadlines, and a document map with repo paths |
| `TIMELINE.md` | Conviction → sentence → parole → revocations/holds → filings, in date order |
| `HABEAS-OPTIONS.md` | Federal habeas routes (2254 / 2241 / coram nobis / PC 1473.7 / 1203.4), *Heck* interplay with the § 1983 suits, viability ratings, missing records, citation verification |
| `coa-6th/` | **Draft only. Do not file.** Sixth District packet to compel a Santa Clara ruling on Matter 19: `MEMO.md` (vehicle), `PETITION-DRAFT.md` (mandate), `CHECKLIST.md` |

Query interface for live status: `npm run q getMatter -- --matter 19` (and 9, 10, 20, 28, 29, 32, 33, 30). Do not rebuild a docket from this memo.

---

## Snapshot the rest of the analysis depends on

These are **pled or documented** facts, not new findings.

| Fact | Source | Confidence |
|---|---|---|
| Convicted Jan. 12, 2018, Santa Clara C1761642, Hon. Arthur Bocanegra: Count 2 **PC § 289(a)(1)(A)** (4 years midterm) and Count 3 **PC § 220(a)(1)** (4 years concurrent). Total 6 years CDCR. Probation denied. Counts 1 and 4 dismissed. § 290 registration ordered. | `internal/private/prenup/IMMIGRATION_NOTES.md` (minute order uploaded 2026-10-04; original not stored in repo) | High as to statutes/term; **the minute order PDF is missing from the repo** |
| Released to CDCR parole **Dec. 2, 2020**. Controlling discharge date pled as **Dec. 2, 2030** (10-year statutory maximum). | Matter 19 `matter.json`; Matter 9 FAC; Accurate report (Matter 29) | High |
| Still on parole as of the Oct. 28, 2026 true-up. No CDCR discharge certificate is in the repo. Accurate’s Oct. 14, 2026 report still says “CURRENTLY ON PAROLE.” | Matter 19 status; Matter 29 accuracy audit | High that the portfolio treats him as on parole; **certificate missing** |
| CDC No. BF3571. Supervised at various times by Stockton 2 GPS (Moua / Noguchi / Derrick / Rojo / Urrea) and, after July 2, 2026, Santa Clara GPS. | Matters 15, 19, 30 | High |
| **No federal habeas petition has ever been filed.** Successive-petition bar of 28 U.S.C. § 2244(b) is not yet triggered. | Full matter crawl | High |
| Matter 19 (C2604791) is the **only live state habeas**. CRC 4.551(a)(6)(B) 30-day calendar from the Sep. 1, 2026 HC-004 ran through **Oct. 1, 2026**. **No ruling PDF ingested as of Oct. 28, 2026.** Status is UNCERTAIN. | Matter 19 `matter.json` (last_updated 2026-10-28); PR #1039 | High as to the gap |
| Recommended next **state** paper, if the clerk file still shows no ruling: petition for **writ of mandate** in the Court of Appeal, Sixth Appellate District, to compel Santa Clara to rule — **not** an original COA habeas that itself discharges him or orders a new review. The pending habeas prays **(1) immediate discharge** on futility **or (2)** a new lawful review on a date certain; ranking in `coa-6th/MEMO.md` § 2. Drafts are in `coa-6th/`. **Do not file from this INDEX.** | `coa-6th/MEMO.md` | Recommendation only; user must pull the live docket first |

---

## 1. Core habeas / discharge vehicles (Cluster 4 — Administrative Writs & Habeas)

Numbered cluster 4 is the UI bucket (`internal/src/data/clusters.js`). It is not the named graph in `index/clusters.json`.

### Matter 19 — live habeas (discharge)

| | |
|---|---|
| Caption | *Newanforbi v. Macomber* (petition caption also names Keely Dodd) |
| Court / no. | Santa Clara Super. Ct. **C2604791** (trial court no. C1761642) |
| Judge | Hon. Robert Hawk |
| Filed | Apr. 3, 2026 (signed Mar. 31, 2026) |
| Proceeding | State habeas, Pen. Code § 1473 — immediate unconditional discharge |
| Status | **ACTIVE / under submission.** HC-004 filed in person Sep. 1, 2026. Oct. 1 ruling calendar passed. **No ruling PDF. Do not treat the petition as granted or denied.** |
| Live clock | `19-deadline-1` 2026-10-01, status `open` (derived overdue). Actor: court. |
| Key orders | **Jul. 2, 2026** Order Extending Time (CRC 4.551(i)) — ruling deadline **Aug. 1, 2026**, which lapsed with no ruling. Path: `/documents/opinions/Newanforbi Habeas - Santa Clara Sup Ct - Order Extending Time Jul 2 2026.pdf` |
| What it asks | **Primary:** vacate the Dec. 1, 2025 Form 1502-DR and **immediate discharge** on a futility theory (Policy 19-03 blanket bar; boilerplate 1502-DR naming **Eagan**; prior denials; record supporting discharge). **Alternatively:** a new lawful individualized review on Form 3043 / 15 CCR § 3574 within a date certain (suggest 30 days). Declare Policy 19-03 invalid as a ground. **Candid ranking** (*Prather* / *Masoner I* / Matter 9): plead both; expect the court to grant (2) if anything. See `coa-6th/MEMO.md` § 2. |
| Prior habeas disclosed | Apr./May 2025 petition (3-year abstract vs. 10-year statute), **denied Aug. 27, 2025 by Judge Geffon**. No Geffon order PDF in the repo. |
| Risk flags in the petition itself | Cites ***In re Leman*, 66 Cal.App.5th 200 (2021)** — **known fabrication; do not reuse.** Claims “without a single arrest” over five years of parole — **in tension with the Nov. 1, 2024 CHP arrest** (Matter 32 / 20 / 33), even though that arrest was later reclassified under PC § 849(b)(1). Supervisor comments on the 1502-DR name **“Eagan”** on the face of the exhibit; some pleadings silently substituted “Newanforbi.” |
| Court of Appeal next step (draft only) | If the live clerk file still shows no 4.551(a)(8) ruling: **writ of mandate** in the Sixth District to compel a ruling — not original COA habeas. Packet: `coa-6th/`. **Do not file from the draft.** |

### Matter 10 — closed habeas (treatment length)

| | |
|---|---|
| Caption | *Newanforbi v. Macomber* |
| Court / no. | Santa Clara Super. Ct. **C2602632** (trial court no. C1761642) |
| Judge | Hon. Robert Hawk |
| Filed | Feb. 23, 2026 |
| Status | **CLOSED.** Order denying **without prejudice**, Apr. 27, 2026 |
| Holding | Sought relief from continued SOMP participation under PC § 3008(d)(2). Denied for **failure to exhaust**: program length is determined by the certified treatment professional in consultation with the parole officer, *then* approved by the court. Futility (citing *Dwyer*) was rejected because the determination is individualized. Path: `/documents/matter-10/ORDER_DENYING_PETITION_C2602632.pdf` |

### Matter 9 — closed mandate (same discharge review)

| | |
|---|---|
| Caption | *Newanforbi v. Macomber* |
| Court / no. | Sacramento Super. Ct. **26WM000028** |
| Judge | Hon. James P. Arguelles, Dept. 13A |
| Filed | Jan. 30, 2026 (FAC ~Feb. 2 / e-filed Mar. 31, 2026) |
| Status | **CLOSED.** Demurrer sustained **without leave to amend** May 29, 2026 (tentative became the order). Counsel for CDCR directed to prepare a formal order and judgment. |
| Holding (tentative, 7 pp.) | (1) Habeas, not mandate, is the proper vehicle because a parolee is in constructive custody (*Ex Parte Bandmann*). (2) Even treating it as mandate, **no ministerial duty**: PC § 3000(b)(2)(B) requires a **10-year** parole term for specified § 667.5(c) offenses, including sexual penetration (§ 667.5(c)(11) / PC § 289). Petitioner has not served 10 years. The court also noted it is “not clear why CDCR undertook the early parole review process.” Path: `/documents/matter-09/CU_26WM000028_e91359ab-2598-4573-a45a-fa7893fc4cb07.pdf` |
| Why it matters for federal habeas | This is the most developed **adverse construction** of the 10-year term. A later 2254 attacking the Dec. 2025 denial as a matter of *state* discharge law has to get past both this holding and *Swarthout v. Cooke*. |

### Matter 11 — closed federal § 1983 (Policy 19-03)

| | |
|---|---|
| Caption | *Newanforbi v. Macomber* |
| Court / no. | USDC E.D. Cal. (case no. TBD in identity JSON; never assigned a live docket in the index) |
| Filed | Mar. 2, 2026 |
| Status | **DISMISSED WITH PREJUDICE** Jun. 29, 2026, FRCP 41(a)(1)(A)(i) |
| Claims | Procedural due process against Policy 19-03’s 6.5-year bar after § 3574. Equitable relief only. Pled around *Heck* via *Wilkinson v. Dotson*. |
| Habeas note | A claim that “success would necessarily mean earlier discharge” is habeas-core under *Nettles*. This filing was § 1983, then abandoned with prejudice. |

---

## 2. Parole-agent / treatment / conditions (Cluster 2 — HOPE / parole)

Live: **28, 30**. Archives: 3–6, 11, 13–18, 21. Matter **15** dismissed with prejudice Jul. 24, 2026 — do not revive it (cluster lock).

| Matter | Court / case no. | Status | Parole connection | Key orders / clocks |
|---|---|---|---|---|
| **3** *Newanforbi v. Derrick* | E.D. Cal. 2:26-cv-00004-DJC-JDP | Closed Aug. 26, 2026. Derrick/Noguchi dismissed Jul. 22; Palacios dismissed Aug. 20–21 after OSC | First Amendment / speech in HOPE group; FedEx scheduling; CTM “ringleader” | Palacios MTD granted Jul. 24 with leave; then voluntary dismissal |
| **4** *Newanforbi v. Derrick* | San Joaquin Super. Ct. TBD | Abandoned | State parallel to Matter 3 | — |
| **5** *Newanforbi v. Palacios* | San Joaquin STK-CV-UF-2026-0001032 | Dismissed Jul. 15, 2026, demurrer to FAC **WOLA on exhaustion** (Abdallah). Oct. 28 true-up: Plaintiff requesting entry of judgment (no judgment PDF) | HOPE fraud / blanket no-completion-before-discharge; Form 3043 reports to parole; 542-page HOPE production | Clock `05-judgment-request` 2026-10-28 open (user report) |
| **6** *Newanforbi v. HOPE* | E.D. Cal. 2:26-cv-00195-TLN-AC | Dismissed without prejudice Jun. 1, 2026 (FRCP 41(a)(1)(A)(i) notice May 21) | First federal HOPE due-process case. **Must be disclosed** in Matter 28; a second voluntary dismissal of the same claim would be with prejudice | ECF No. 5 Notice of Related Cases (HOPE’s only paper) |
| **13** *Newanforbi v. Urrea* | E.D. Cal. 2:26-cv-00190-DC-SCR | Dismissed **with prejudice** Jun. 29, 2026 | **5-day Halloween curfew detention** — a completed parole hold, no nexus to the commitment offense | — |
| **14** *Newanforbi v. Urrea* | San Joaquin Super. Ct. TBD | Abandoned mandate | State parallel to 13 | — |
| **15** *Newanforbi v. CDCR* | San Joaquin STK-CV-UPI-2026-5417 | Abandoned — dismissed **with prejudice** Jul. 24, 2026 (safety). Originally Sacramento, recalibrated after Matter 9 tentative | Damages for the Nov. 2025 1502-DR (Eagan, Policy 19-03, obsolete form); false imprisonment / IIED. **Do not revive.** | CMC Dec. 9, 2026 vacated |
| **16** *Newanforbi v. Rojo* | San Joaquin TBD | Abandoned | Parole-agent damages | — |
| **17** *Newanforbi v. Maloney* | E.D. Cal. 2:26-cv-00194-DAD-SCR | Dismissed with prejudice Jun. 29, 2026 | Parole supervision; Macomber official-capacity injunctive | — |
| **18** *Newanforbi v. Barocio* | E.D. Cal. 2:26-cv-00191-DJC-CSK (PC) | Dismissed with prejudice Jun. 29, 2026 | Parole supervision (docketed as a (PC) prisoner case) | — |
| **21** *Newanforbi v. Rojo* | E.D. Cal. 2:26-cv-00193-DC-CKD | Dismissed with prejudice Jun. 29, 2026 | Free Exercise — Nov. 2025 Reno church-travel denial; unpublished “emergency or death” policy | — |
| **28** *Newanforbi v. Smith / HOPE* | N.D. Cal. **3:26-cv-07504-LJC** (Cisneros) | **ACTIVE.** Oct. 27 CMC+MTD held (user report). MTD deferred pending San Joaquin judgment; discovery stayed. **No Oct. 27 order PDF.** | Live SOMP-vendor § 1983 / Bane / fraud / RICO. Treatment-completion vs. parole discharge | Joint status reports **Nov. 17, 2026** monthly through May 17, 2027; joint CMC statement Jun. 10, 2027; CMC **Jun. 17, 2027, 1:30 p.m.** |
| **30** *Newanforbi v. Moua* | N.D. Cal. TBD — **unfiled** | Pre-filing. GCA claim Jul. 18, 2026; deemed rejected ~Sep. 1, 2026 | Retaliatory file transfer → fabricated Mar. 31, 2026 telehealth “no-show” → Jun. 29 / Jul. 2, 2026 Santa Clara transfer; Macy’s job loss. Complaint v9 is Moua + DOES only | Outer GCA window **Mar. 1, 2027** (`30-deadline-2`). Note in `matter.json`: if discharged before the window closes, Plaintiff still intends to file |

---

## 3. November 1, 2024 arrest while on parole (Cluster 1)

Live: **20, 24, 32, 33**. Archives: 1, 2, 7, 8.

These are not habeas cases. They matter because (a) the arrest happened **on parole**, (b) Matter 1’s F&R recorded a **parole-violation hold**, and (c) Accurate later used C1761642 + “currently on parole” in a 2026 background check.

| Matter | Court / case no. | Status | Parole hook | Key orders / clocks |
|---|---|---|---|---|
| **1** *Newanforbi v. CHP* | E.D. Cal. 2:25-cv-01460-DC-CSK | Closed Aug. 26, 2026; claims refiled as Matter 32 | F&R (ECF 23 at 2:16–17): “The incident also triggered a parole violation hold.” Valuation pin in `internal/private/negotiation/32.valuation.json` | Voluntary dismissal Aug. 15, 2026 |
| **2** *Newanforbi v. Meza-Gonzalez* | Alameda 26CV168913 | Dismissed | State parallel, same night | — |
| **20** *Newanforbi v. CHP* | Alameda **26CV191136**, Whitman Dept. 25 | **ACTIVE** mandate (PC § 679.10 U-visa certification). Count 1 survived Aug. 29 demurrer; Counts 2–3 WOLA; Count 4 leave lapsed | Same arrest; CHP Production Set One (AGO 000022–000025, 000029–000054, 000061) is the dashcam / arrest record, **not** a parole file. Privilege-log gaps: 000001–000021, 000026–000028, 000055–000060 | CMC **Nov. 4, 2026, 4:00 p.m.**; opening brief **Nov. 13**; opposition Dec. 11; reply Dec. 18; merits **Jan. 8, 2027** (user report; no continuance-order PDF) |
| **24** *Newanforbi v. Serrato* | N.D. Cal. **3:26-cv-05953-CRB** (Breyer) | **ACTIVE** § 1983 | Same I-918B denial | MTD hearing **Nov. 20, 2026, 10:00 a.m.** Zoom (Dkt. 30) |
| **32** *Nforbi v. Meza-Gonzalez* | N.D. Cal. **4:26-cv-08271-ASK** (Krishnan) | **ACTIVE** § 1983. Open PR #1035 catalogs Dkt. 22 MTD (Oct. 26) and Dkt. 23 magistrate declination; PDFs not all on `main` | Arrest, **five-day parole hold**, forced blood draw, Santa Rita booking. Defense: parole search condition (*Samson*). Computed opposition **Nov. 9, 2026** (Civ. L.R. 7-3(a) from Oct. 26) | Summons return being refiled (`32-deadline-1` open). CCP § 335.1 backstop **Nov. 1, 2026** |
| **7** *Newanforbi v. Candelaria* | E.D. Cal. 2:26-cv-00983-DC-CSK | Dismissed w/o prejudice Aug. 15, 2026; refiled as 33 | DMV APS from the same arrest (not habeas) | F&R Jun. 15, 2026 mooted |
| **8** *Newanforbi v. Candelaria* | Sacramento 26WM000135 | Abandoned mandate | APS | — |
| **33** *Nforbi v. Candelaria* | N.D. Cal. **3:26-cv-08272-RFL** (Lin; was LJC) | **ACTIVE** § 1983 APS | Same night; SR-22 through ~May 2029 | Dkt. 24 (Oct. 13) struck the Sep. 4 answer. FAC-response watch left open as of Oct. 28. 26(f) / ADR **Nov. 18, 2026**. Hearing/CMC **Dec. 9, 2026, 10:00 a.m.**; CMS Dec. 2 |

**AGO 000022–61 (Matter 20).** Production map: `internal/docs/Matter 20 - CHP Production Set One Map vs Answer (Oct 23 2026).md`. Dashcam Videos Coversheet is AGO 000022–000024. This is CHP arrest evidence. It is **not** a CDCR parole packet. Parole-hold proof, if it exists, is more likely in a CDCR/DAPO file that has not been produced.

---

## 4. Background-check use of parole / C1761642

| Matter | Court / case no. | Status | Parole hook | Clocks |
|---|---|---|---|---|
| **29** *Newanforbi v. Amazon / Accurate* | N.D. Cal. **4:26-cv-09249-ASK** (Krishnan; removed from Alameda 26CV201554) | **ACTIVE.** Dkt. 19 MTD; hearing **Nov. 18, 2026, 1:30 p.m.** | Accurate consumer report (search 496623722, completed **Oct. 14, 2026**) lists Santa Clara **C1761642**, release **12/02/2020**, and **“CURRENTLY ON PAROLE.”** No source or verification date for the parole line. Five other CRAs returned Santa Clara Clear/No Record. Audit: `internal/docs/matter-29/matter29-accurate-accuracy-audit.md` | 26(f) **Nov. 6**; ADR Nov. 10; Joint CMS Nov. 24; CMC **Dec. 1**. Accurate reinvestigation clock satisfied Oct. 28 (user report: “Newansorbi” alias removed; NSOR completeness **not** independently verified). Open PR #1036 is the private research room |

C1761642 itself is **not** a portfolio matter number. It is the 2018 criminal case. The certified docket is still an internal target (Matter 29 60-day calendar, Oct. 20: “order the certified Santa Clara docket”).

---

## 5. Immigration overlay (not a filed matter)

Private notes only: `internal/private/prenup/IMMIGRATION_NOTES.md`.

- Immigration Court, Aurora, Colorado, Judge Elizabeth McGrail, **Feb. 8, 2021**: removable under INA §§ 237(a)(1)(B) and 237(a)(2)(A)(iii) (aggravated felony). Asylum / withholding denied. **CAT deferral granted.** Removal to Cameroon ordered; both sides waived appeal — **final Feb. 8, 2021**. Letter-size scan: `internal/private/research/parole-habeas/Immigration-Judge-Order-Feb-8-2021-Letter.pdf`.
- ICE Form I-220B Order of Supervision Apr. 30, 2021; released May 10, 2021.
- This is a **second custody system** (ICE OSUP) sitting on top of CDCR parole. It is not CDCR habeas, but it is why PC § 1473.7 and vacatur of C1761642 matter, and why Matter 20’s U-visa writ is in the parole conversation.

Do not contact ICE, a spouse, or any third party from this workspace.

---

## 6. Document map (repo paths)

### Immigration (private)

| Doc | Path |
|---|---|
| Order of the Immigration Judge (Aurora, Feb. 8, 2021) — letter size (8.5×11 in) | `internal/private/research/parole-habeas/Immigration-Judge-Order-Feb-8-2021-Letter.pdf` |
| Prenup immigration notes | `internal/private/prenup/IMMIGRATION_NOTES.md` |

### Underlying conviction / parole term

| Doc | Path |
|---|---|
| Prenup immigration notes (minute-order facts; original not stored) | `internal/private/prenup/IMMIGRATION_NOTES.md` |
| Accurate “currently on parole” / C1761642 audit | `internal/docs/matter-29/matter29-accurate-accuracy-audit.md` |
| CDCR Form 1502-DR (Discharge Review Report) PDF | `documents/matter-28/evidence/Discharge_Review_Report.pdf` |
| Same, public sidecar (text layer empty on this checkout) | `internal/public/documents/matter-28/evidence/Discharge_Review_Report.txt` |
| Quoted 1502-DR language (Policy 19-03; 10-year term; “4 of 6.5 years”) | Matter 9 FAC `/documents/matter-09/WOM FAC.pdf`; tentative `/documents/matter-09/CU_26WM000028_…pdf` |

### State habeas / mandate

| Doc | Path |
|---|---|
| Matter 19 petition (filed Apr. 3, 2026, 67 pp.) | `documents/matter-19/Petition for Writ of Habeas Corpus (filed Apr. 3, 2026).pdf` also `/documents/matter-19/…` |
| HC-004 filed in person Sep. 1, 2026 | `/documents/matter-19/HC-004 Notice and Request for Ruling (Habeas Corpus, Executed Sep 1 2026).pdf` |
| Jul. 2, 2026 Order Extending Time | `/documents/opinions/Newanforbi Habeas - Santa Clara Sup Ct - Order Extending Time Jul 2 2026.pdf` |
| Public habeas-discharge packet (PR #648) | `internal/public/habeas-discharge.pdf` |
| Packet builder | `internal/scripts/matter19-habeas-discharge-packet.py` |
| Matter 10 denial (Apr. 27, 2026) | `/documents/matter-10/ORDER_DENYING_PETITION_C2602632.pdf` |
| Matter 9 FAC / opening brief / AG reply / tentative | `/documents/matter-09/WOM FAC.pdf`, `WOM_Opening Brief.pdf`, `26WM000028_Reply_to_Opp.pdf`, `CU_26WM000028_….pdf` |
| *In re Dwyer* (Matter 19 Ex. B) | Inside the Matter 19 petition PDF (San Mateo Super. Ct. SC-080355A / HC-3020, Mar. 20, 2023) |

### Nov. 1 arrest / parole hold / AGO production

| Doc | Path |
|---|---|
| Cluster 1 locked facts | `internal/docs/legal-intel/clusters/01-nov1-locked-facts.md` |
| Cluster 2 locked facts | `internal/docs/legal-intel/clusters/02-hope-parole-locked-facts.md` |
| Matter 32 valuation (parole hold pin) | `internal/private/negotiation/32.valuation.json` |
| CHP Production Set One map (AGO 000022–61) | `internal/docs/Matter 20 - CHP Production Set One Map vs Answer (Oct 23 2026).md` |
| Dashcam video descriptions | `internal/docs/matter-20-production-set-one/Matter 20 - CHP Production Set One Video (MP4) Descriptions (Oct 23 2026).md` |

### HOPE / SOMP (parole condition)

| Doc | Path |
|---|---|
| HOPE Bates HOPE_000001–542 (private text) | `internal/private/documents/matter-05/hope-discovery/text/` |
| Matter 28 complaint / MTD papers | `internal/public/documents/matter-28/` |
| Parole transfer request draft (Noguchi, Sep. 16, 2026) | `internal/docs/Cover Email - Parole Transfer Request to Stockton (Noguchi, Sep 16 2026).txt` |

### Identity JSON (do not treat README as live)

`internal/src/data/matters/09/`, `10/`, `11/`, `15/`, `19/`, plus cluster-2 and cluster-1 siblings listed above. Front door: `internal/src/data/index/matters.json`.

---

## 7. Recent PRs / branches crawled

Searched GitHub `newanforbi/interactive-litigation-portfolio` for parole, habeas, Macomber, C1761642, HC-004, discharge.

| PR / branch | State | What it added for this workspace |
|---|---|---|
| **#1039** True-up to Oct. 28, 2026 | **Merged** 2026-10-28 | Matter 19 status: Oct. 1 calendar passed, **ruling unverified**. Matter 20/28/29/32/33 clocks updated. Explicitly could not verify “Matter 19 habeas ruling after Oct. 1.” |
| **#1035** Matter 32 MTD architecture (ECF 22) | Open | DUI / Nov. 1 § 1983; Dkt. 22 MTD Oct. 26; Dkt. 23 |
| **#1036** Matter 29 think tank | Open | Accurate reinvestigation / “currently on parole” research room |
| **#648** Publish habeas-discharge packet | Closed / merged | `internal/public/habeas-discharge.pdf`, `/habeas-discharge` |
| **#614 / #609** Sep. 1 HC-004 | Closed | Matter 19 in-person filing |
| **#812** Email to Noguchi: parole transfer back to Stockton | Closed | Supervision-location ask, not a habeas filing |
| **#885 / #884 / #880 / #764** Matter 28 research | Closed | SOMP / § 3008 / *Dwyer* / *Swarthout* spine |
| `agent/matter-20-production-map` | Branch | AGO Bates map |
| `agent/matter-29-accurate-audit-dispute` | Branch | C1761642 / parole-status dispute |

No branch or PR contains a Santa Clara order ruling on C2604791 after Oct. 1, 2026.

---

## 8. Record conflicts (do not paper over)

1. **“Zero arrests” (Matter 19 petition ¶ 3) vs. Nov. 1, 2024 CHP arrest** (later PC § 849(b)(1) detention certificate Nov. 5, 2024). Any habeas or 2254 that repeats “no arrests” will be impeached with Matter 1/20/32/33.
2. **“Zero revocations”** is consistent with the Form 1502-DR’s verbal-reprimand / PACT handling, but **does not erase** (a) the Nov. 1 **parole hold**, (b) the Halloween **5-day detention** (Matter 13), or (c) the Mar. 31, 2026 telehealth write-up (Matter 30).
3. **Eagan vs. Newanforbi** on the 1502-DR supervisor comments. The form is the exhibit. Pleadings that silently substitute the petitioner’s name are a candor problem (`internal/docs/cross_matter_risk_index.json`).
4. **Abstract “3 years” vs. PC § 3000 10-year term.** Geffon denied that challenge Aug. 27, 2025 (order missing). Matter 9 independently held the 10-year statute controls.
5. ***In re Leman*** is in the Matter 19 petition and in `matter.json` `key_facts`. It is a **known-fabricated** cite. Do not put it in any new filing.

---

## 9. Missing records (short list; full list in HABEAS-OPTIONS)

Priority pulls:

1. Santa Clara clerk file for **C2604791** — any order after Jul. 2, 2026, especially after Oct. 1, 2026.
2. Judge **Geffon** Aug. 27, 2025 denial (the 2025 term-length habeas) and the petition it decided.
3. Certified **C1761642** docket, abstract of judgment, sentencing transcript, and the Jan. 12, 2018 minute order.
4. **CDCR discharge certificate** (or a letter that there is none) and the live DAPO face sheet / controlling discharge date.
5. CDCR **Policy 19-03 (Amended)** as promulgated, not just as quoted on the 1502-DR.
6. Form **3043** (or proof none was used) for the Nov./Dec. 2025 review.
7. DAPO records of the **Nov. 1, 2024 parole hold** and the **Halloween 5-day hold**.
8. Direct-appeal / habeas history in the California Court of Appeal and California Supreme Court (needed for 2254 exhaustion).
9. Matter 9 **formal order and judgment** (tentative says CDCR counsel shall prepare them).
10. Matter 5 **CCP § 581d judgment** (Matter 28 stay is waiting on it).
