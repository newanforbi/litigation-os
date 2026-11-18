# Parole / habeas workspace — TIMELINE

**Classification:** internal/private. Not a live calendar. Dates below are from `clocks.json`, `docket.json`, `events.jsonl`, filed PDFs, and the private immigration notes. Where those conflict, clocks and filed orders win.

**As of:** 2026-10-28. Today’s open question is whether Santa Clara has ruled on Matter 19 (C2604791) after the Oct. 1, 2026 CRC 4.551 calendar. No ruling PDF is in the repo.

Labels: **FACT** (on a filed paper or identity JSON), **USER REPORT** (true-up / prenup notes without the source PDF), **INFERENCE**, **MISSING**.

---

## A. Conviction and sentence (C1761642)

| Date | Event | Label | Source |
|---|---|---|---|
| 2017-10-25 | Santa Clara criminal case **C1761642** filing date as later reported by Accurate | USER REPORT (CRA) | Matter 29 accuracy audit, CR p4. **Certified docket missing.** |
| 2018-01-12 | Sentencing, Hon. Arthur Bocanegra. Count 2 **PC § 289(a)(1)(A)**, 4 years midterm; Count 3 **PC § 220(a)(1)**, 4 years concurrent. Total **6 years CDCR**. Probation denied. Counts 1 (PC §§ 664/209(b)(1)) and 4 (PC §§ 664/242/243.4(a)) dismissed. **§ 290** registration ordered. Criminal protective order; notes say it appears to expire Jan. 12, 2028 | USER REPORT | `internal/private/prenup/IMMIGRATION_NOTES.md`. **Minute-order PDF not stored.** |
| 2018 (post-sentence) | Direct appeal? | MISSING | No notice of appeal, opinion, or remittitur in the repo. If none was filed, the judgment became final 60 days after sentencing (Cal. Rules of Court, rule 8.308) — **about Mar. 13, 2018**. That date, if true, starts the AEDPA one-year clock on a 2254 attacking the **conviction**. |
| ~2018–2020 | CDCR term served. CDC No. **BF3571** | FACT | Matter 19 petition; HOPE homework Bates (TP ID# BF3571) |

Offense date is **not** in the repo. Filing in October 2017 plus a January 2018 sentence implies a crime **on or after July 1, 2013**, which is the PC § 3000(b)(2)(B) cutoff (10-year parole “shall” rather than “not exceeding”). Confirm from the complaint / probation report.

---

## B. Parole start and immigration overlay

| Date | Event | Label | Source |
|---|---|---|---|
| **2020-12-02** | Released from prison onto CDCR parole. This is the date used everywhere: Matter 19, Matter 9 FAC, Accurate CR (“RELEASED FROM PRISON ONTO PAROLE”) | FACT (pled / CRA) | Matter 19 `key_facts`; Accurate CR p5–6. **CDCR release chrono missing.** |
| 2020-12-02 + 10 years | Controlling discharge date pled as **2030-12-02** | FACT (pled) | Matter 9 FAC; Matter 19. Follows PC § 3000(b)(2)(B) for a § 667.5(c)(11) offense (sexual penetration, PC § 289). Matter 9 tentative adopted that construction May 29, 2026 |
| 2021-02-08 | Immigration Court, Aurora, CO (Judge Elizabeth McGrail): removable; asylum/withholding denied; **CAT deferral granted**; removal to Cameroon ordered; both sides waived appeal — **final** | FACT (IJ order) | `internal/private/research/parole-habeas/Immigration-Judge-Order-Feb-8-2021-Letter.pdf` |
| 2021-03-05 | HOPE intake (Stockton). Pled as the date HOPE represented an achievable path to treatment completion | FACT (pled) | Matter 5 FAC `key_facts` |
| 2021-04-30 / 2021-05-10 | ICE I-220B issued; released from ICE custody onto order of supervision | USER REPORT | Prenup notes |
| 2021 (undated) | Prior supervising agent approved travel to Reno for a church service — later used as a comparator in Matter 21 | FACT (pled) | Matter 21 `key_facts` |

From Dec. 2, 2020 through Oct. 28, 2026 is **about 5 years 11 months** on parole. Policy 19-03’s “6.5 years” bar, as quoted on the 1502-DR in Nov. 2025, counted “approximately 4 years.” That internal count has never been reconciled in a CDCR letter in this repo.

---

## C. Supervision, technicals, and holds (2022–2025)

| Date | Event | Label | Source |
|---|---|---|---|
| 2022-01 | Forced resignation from United Road, pled as HOPE/GPS incompatibility with CDL work | FACT (pled) | Matter 5 |
| 2022-11 | Clinician Pamela Akins group-session representation re completion path | FACT (pled) | Matter 5 |
| 2024-01 / 2024-06 | Further HOPE statements (titration; missing homework) | FACT (pled) | Matter 5 |
| **2024-11-01 ~00:54** | CHP Meza-Gonzalez / Melano contact, I-580 East shoulder, Livermore (CHP RJ68845 / CAD 241101GG0064). Custodial arrest, blood-draw warrant WAR913372, Santa Rita booking | FACT | Cluster 1 locked facts; Matters 1/20/32/33 |
| 2024-11-01 ff. | **Parole-violation hold** after the arrest. Duration pled as **five days** (with the booking / blood draw) | FACT (pled in Matter 1 F&R; used in Matter 32 valuation) | `32.valuation.json` pin: E.D. Cal. 2:25-cv-01460, ECF 23 at 2:16–17. **DAPO hold paperwork missing.** |
| 2024-11-05 | CHP issues PC § 849(b)(1) Detention Certificate (Dublin CHP-01991 / File 202400898) — detention only, insufficient grounds for a complaint. DA filed nothing | FACT | Cluster 1 lock |
| ~Halloween 2024 or 2025 | Agent Urrea **5-day curfew detention**. Matter 13 describes it as pretextual Halloween curfew; year is not pinned in `matter.json` | FACT (pled) / year MISSING | Matter 13. Closed with prejudice Jun. 29, 2026 |
| 2025-01-24 / 2025-02-11 | DMV APS hearing / Candelaria decision; one-year Class A suspension Feb. 20, 2025 – Feb. 19, 2026 | FACT | Matter 33 |
| 2025-02-20 | HOPE grace-period revocation (locked date; not “early April”) | FACT | Cluster 2 lock; HOPE_000190 |
| 2025-03 / ~2025-04-17 | FedEx Office offer (~$20/hr); scheduling accommodation denied by Derrick / Palacios; resignation | FACT (pled) | Matters 3, 19 |
| 2025 (four incidents) | Technicals: missed HOPE sessions, uncharged GPS. Resolved by verbal reprimand or PACT. **No revocation** | FACT (pled on the 1502-DR / Matter 19) | Matter 19 `key_facts` |
| 2025-08 | CTM: Palacios “ringleader” / “abhorrent” characterizations in front of Chow, Noguchi, Derrick | FACT (pled) | Matters 3, 5 |
| **2025-08-27** | Prior Santa Clara habeas (3-year abstract vs. 10-year statute) **denied by Judge Geffon** | FACT (pled) | Matter 19 events.jsonl; petition CRC 4.552 disclosure. **Order PDF missing. Case number missing.** |
| 2025-11-14 | Moua authors CDCR **Form 1502-DR** (Rev. 01/22). Noguchi electronically signs as supervisor (badge 7284). Discharge review date printed **Dec. 1, 2025**. Dodd ratifies **Nov. 19, 2025** (pled) | FACT | Matter 15 `key_facts`; Matter 9 FAC Ex. A. Supervisor comments on the face of the form name **“Eagan.”** |
| 2025-11-17–21 | Rojo / Noguchi deny Reno church-travel request the morning of departure | FACT (pled) | Matter 21 |
| **2025-12-01** | Discharge Review Report operative date. Denial: Policy 19-03 10-year term / “only completed approximately 4 years of the required 6.5 years”; incomplete treatment; technicals; unemployment | FACT | Matter 9 tentative quoting FAP Ex. A p.4 |

No **formal parole revocation** (Morrissey hearing → return to prison) is documented. The two completed **holds** (Nov. 1, 2024; Halloween curfew) are the closest events. Matter 30 later alleges a **fabricated** Mar. 31, 2026 treatment violation that was cited for an inter-county **transfer**, not a revocation.

---

## D. 2026 litigation wave (discharge, habeas, § 1983)

| Date | Event | Matter | Label |
|---|---|---|---|
| 2026-01-05 | Derrick FAC / case filed (E.D. Cal.) | 3 | FACT |
| 2026-01-22 | HOPE, Urrea, Maloney, Barocio, Rojo federal complaints filed | 6, 13, 17, 18, 21 | FACT |
| ~2026-01-26 | Parole file transferred Stockton Derrick → **Long Moua** (~14 days after Derrick FAC) | 30 | FACT (pled) |
| 2026-01-30 | Sacramento mandate filed | 9 | FACT |
| 2026-02-10 | Government Tort Claim (preserves damages from the 1502-DR restraint); Matter 5 Palacios complaint filed | 19 / 5 | FACT (pled) |
| 2026-02-23 | Matter 10 habeas filed (treatment termination). CASOMB complaint against HOPE | 10 / 30 | FACT |
| 2026-03-02 | Matter 11 federal § 1983 (Policy 19-03) filed | 11 | FACT |
| 2026-03-18 / 2026-03-25 / **2026-03-31** | Moua directs telehealth with Pam Akins; texts a number but **no access code**; Mar. 31 missed session; Apr. 1 “Come to the office”; Moua says he will write a treatment-failure violation | 30 | FACT (pled; texts described) |
| **2026-04-03** | **Matter 19 habeas filed** (C2604791) — immediate discharge | 19 | FACT |
| 2026-04-09 / 2026-04-20 | I-918B request to CHP; Serrato five-sentence denial | 20 | FACT |
| **2026-04-27** | **Matter 10 denied without prejudice** (Hawk) — exhaust SOMP-length determination first | 10 | FACT |
| 2026-04-27 | Matter 7 Candelaria filed (E.D. Cal.) | 7 | FACT |
| 2026-05-13 / 2026-06-08 / 2026-06-11 | Matter 15 originally Sacramento, then recalibrated San Joaquin complaint | 15 | FACT |
| 2026-05-21 / 2026-06-01 | Matter 6 voluntary dismissal w/o prejudice; minute order closing | 6 | FACT |
| 2026-05-28 | Macy’s start, Stockton, $21.50/hr | 30 | FACT (pled) |
| **2026-05-29** | **Matter 9 demurrer sustained WOLA** (Arguelles). 10-year PC § 3000 term; habeas is the right vehicle; no 3008 duty | 9 | FACT |
| 2026-05-29 | Matter 20 U-visa writ filed | 20 | FACT |
| 2026-06-17 | Matter 24 Serrato § 1983 filed | 24 | FACT |
| 2026-06-22 | Matter 15 served on CDCR and Dodd | 15 | FACT |
| 2026-06-29 | Moua UA + announces transfer to Santa Clara GPS (“too many violations”) — 7 days after Matter 15 service | 30 | FACT (pled) |
| 2026-06-29 | Matters 11, 13, 17, 18, 21 dismissed **with prejudice** | several | FACT |
| **2026-07-02** | (1) First report to Agent Brown, Santa Clara GPS. (2) **Hawk Order Extending Time** on Matter 19 to **Aug. 1, 2026**. Same-day coincidence is pled as retaliatory in Matter 15/30; the order itself does not say that | 19 / 30 | FACT (order); INFERENCE (motive) |
| 2026-07-06 | Transient § 290 re-registration, Santa Clara Sheriff | 30 | FACT (pled) |
| 2026-07-15 | Matter 5 demurrer to FAC sustained WOLA (exhaustion) | 5 | FACT |
| 2026-07-18 | GCA claim (Matter 30) | 30 | FACT |
| 2026-07-20 / 2026-07-21 | Matter 28 filed (N.D. Cal.) | 28 | FACT |
| 2026-07-24 | Matter 15 dismissed **with prejudice** (safety) | 15 | FACT |
| 2026-07-28 / 2026-08-31 | Matter 29 filed (Alameda) / removed to N.D. Cal. | 29 | FACT |
| 2026-07-31 | Macy’s resignation attributed in writing to the Santa Clara transfer | 30 | FACT (pled) |
| **2026-08-01** | Matter 19 ruling deadline under the Jul. 2 order **lapses. No ruling.** | 19 | FACT |
| 2026-08-07 / 2026-08-17 | HC-004 packets prepared (not yet the operative filing); address restored to Cat Tail Drive | 19 | FACT |
| 2026-08-10 | Matters 32 and 33 docketed (N.D. Cal.) | 32 / 33 | FACT |
| 2026-08-15 | Matters 1 and 7 voluntarily dismissed (refiles already on file) | 1 / 7 | FACT |
| 2026-08-20–26 | Matter 3 Palacios dismissed; E.D. Cal. docket closed | 3 | FACT |
| 2026-08-28 / 2026-08-29 | Matter 20 demurrer hearing / Whitman order: Count 1 proceeds | 20 | FACT |
| **2026-09-01** | **HC-004 filed in person** at Santa Clara. CRC 4.551(a)(6)(B) 30-day calendar → **Oct. 1, 2026** | 19 | FACT |
| 2026-09-16 | Matter 20 RFP Set One to Ing; parole-transfer email to Noguchi drafted | 20 | FACT |
| 2026-09-16 | Matter 30 anticipated filing date — **not confirmed as filed** | 30 | FACT |
| 2026-09-21 / 2026-09-22 | Matter 28 Dkt. 15 MTD; opposition served | 28 | FACT |
| 2026-09-22 | Matter 29 Dkt. 19 MTD | 29 | FACT |
| **2026-10-01** | Matter 19 CRC 4.551 calendar date. **No ruling PDF as of Oct. 28 true-up.** Clock left `open` | 19 | FACT (calendar) / UNCERTAIN (whether the court ruled) |
| 2026-10-13 | Matter 28 Dkt. 30 reply; Matter 33 Dkt. 24 grants motion to strike | 28 / 33 | FACT |
| 2026-10-14 | Accurate report 496623722 completed: C1761642 + **“CURRENTLY ON PAROLE”** | 29 | FACT |
| 2026-10-23 | CHP Production Set One served (AGO 000022–61 ranges) | 20 | FACT |
| 2026-10-26 | Matter 32 Dkt. 22 MTD (cataloged on open PR #1035; not fully on `main`) | 32 | USER REPORT / PR |
| 2026-10-27 | Matter 28 CMC+MTD held; MTD deferred; discovery stayed (user report; **no order PDF**) | 28 | USER REPORT |
| **2026-10-28** | Portfolio true-up. Matter 19 still pending. Accurate user report: “Newansorbi” alias removed | 19 / 29 | FACT (status) / USER REPORT (alias) |

---

## E. Forward clocks that still matter to habeas strategy

From `clocks.json` after the Oct. 28 true-up. Vacated clocks omitted.

| Date | Matter | Clock | Why it matters here |
|---|---|---|---|
| 2026-10-01 (open / derived overdue) | 19 | HC-004 30-day ruling calendar | Until a ruling exists, a federal 2254 of the discharge claim is **unexhausted** |
| 2026-10-28 | 5 | Request entry of judgment | Matter 28 stay is waiting on the San Joaquin judgment |
| 2026-11-01 | 32 | CCP § 335.1 two-year backstop from Nov. 1, 2024 | Not habeas; do not miss it |
| 2026-11-04 16:00 | 20 | CMC, Whitman | U-visa path (immigration), not CDCR habeas |
| 2026-11-06 | 29 | Rule 26(f) | “Currently on parole” is an ICRAA/FCRA accuracy fact, not a custody fact |
| 2026-11-09 (computed) | 32 | Opposition to Dkt. 22 MTD | Confirm once the motion notice is ingested |
| 2026-11-13 | 20 | Opening brief on the writ | — |
| 2026-11-17 | 28 | First monthly joint status report | HOPE / SOMP record that also feeds the discharge theory |
| 2026-11-18 13:30 | 29 | Dkt. 19 MTD | — |
| 2026-11-18 | 33 | 26(f) / ADR | Candelaria |
| 2026-11-20 10:00 | 24 | Serrato MTD, Zoom | — |
| 2026-12-01 | 29 | CMC | — |
| 2026-12-09 10:00 | 33 | Hearing / CMC (Lin) | — |
| 2027-01-08 | 20 | Merits hearing | — |
| **2027-03-01** | 30 | Outer GCA six-month window | Last date to file Moua as currently scoped **unless discharged earlier and the note in `matter.json` is followed** |
| 2027-06-17 13:30 | 28 | CMC | — |
| **2030-12-02** | — | Statutory controlling discharge (pled) | If still on parole, *Jones* custody continues until then unless CDCR or a court discharges earlier |

---

## F. What is *not* on this timeline

- A signed **CDCR discharge**. Accurate still said “currently on parole” on Oct. 14, 2026. Matter 19 is still captioned as seeking discharge.
- A **Morrissey** revocation hearing or a return-to-prison.
- A **federal** habeas petition, a Ninth Circuit habeas appeal, or a California Supreme Court habeas.
- The **Geffon** 2025 file.
- A **direct appeal** of C1761642.

Those gaps are the missing-records list in `HABEAS-OPTIONS.md`.
