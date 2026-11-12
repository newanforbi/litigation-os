"""Westlaw research plan — Ngwa Nforbi v. The Hertz Corporation & HireRight, LLC (N.D. Cal.)."""
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
                                PageBreak, KeepTogether)

INK = colors.HexColor("#1b1f24"); MUTED = colors.HexColor("#5b6470")
ACCENT = colors.HexColor("#7a1f2b"); RULE = colors.HexColor("#c9ced6"); SHADE = colors.HexColor("#f3f4f6")

base = dict(fontName="Times-Roman", fontSize=10.5, leading=14, textColor=INK)
H1 = ParagraphStyle("h1", fontName="Times-Bold", fontSize=20, leading=24, textColor=INK, spaceAfter=4)
SUB = ParagraphStyle("sub", fontName="Times-Italic", fontSize=11, leading=14, textColor=MUTED, spaceAfter=10)
H2 = ParagraphStyle("h2", fontName="Times-Bold", fontSize=14, leading=18, textColor=ACCENT, spaceBefore=12, spaceAfter=4)
H3 = ParagraphStyle("h3", fontName="Times-Bold", fontSize=11.5, leading=15, textColor=INK, spaceBefore=8, spaceAfter=2)
P = ParagraphStyle("p", **base, spaceAfter=5)
SM = ParagraphStyle("sm", **{**base, "fontSize": 9, "leading": 11.5})
Q = ParagraphStyle("q", fontName="Courier", fontSize=8.6, leading=11, textColor=INK)
BUL = ParagraphStyle("b", **base, leftIndent=22, bulletIndent=0, spaceAfter=2)


def bullets(items):
    return [Paragraph(t, BUL, bulletText="[  ]") for t in items]


def qtable(rows, widths=(2.05 * inch, 4.85 * inch)):
    data = [[Paragraph("<b>Goal</b>", SM), Paragraph("<b>Westlaw query (Terms &amp; Connectors)</b>", SM)]]
    for goal, q in rows:
        data.append([Paragraph(goal, SM), Paragraph(q.replace("&", "&amp;").replace("<", "&lt;"), Q)])
    t = Table(data, colWidths=widths, repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), SHADE), ("LINEBELOW", (0, 0), (-1, 0), 0.6, INK),
        ("LINEBELOW", (0, 1), (-1, -1), 0.3, RULE), ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4)]))
    return t


def atable(rows):
    data = [[Paragraph(f"<b>{h}</b>", SM) for h in ("Authority", "Why it matters", "Status / KeyCite task")]]
    for a, w, s in rows:
        data.append([Paragraph(a, SM), Paragraph(w, SM), Paragraph(s, SM)])
    t = Table(data, colWidths=(2.35 * inch, 2.6 * inch, 1.95 * inch), repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), SHADE), ("LINEBELOW", (0, 0), (-1, 0), 0.6, INK),
        ("LINEBELOW", (0, 1), (-1, -1), 0.3, RULE), ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4)]))
    return t


def footer(c, d):
    c.saveState()
    c.setFont("Times-Roman", 8); c.setFillColor(MUTED)
    c.drawString(0.8 * inch, 0.5 * inch, "Westlaw Research Plan — Ngwa Nforbi v. The Hertz Corporation, et al. (N.D. Cal.) — work product, not for filing")
    c.drawRightString(7.7 * inch, 0.5 * inch, f"{d.page}")
    c.restoreState()


S = []
S += [Paragraph("Westlaw Research Plan", H1),
      Paragraph("Ngwa Nforbi v. The Hertz Corporation and HireRight, LLC — U.S. District Court, N.D. Cal. (San Jose). "
                "Prepared November 12, 2026, against the 25-page verified complaint.", SUB)]

S += [Paragraph("How to use this", H2),
      Paragraph("Each section maps to a cause of action or a defense Hertz and HireRight are expected to raise on a "
                "Rule 12(b)(6) motion. Run the queries in the jurisdiction noted, sort by relevance, then by date. "
                "Every authority goes through KeyCite before it is cited; a red or yellow flag, a grant of review, or a "
                "depublication order (Cal. Rules of Court, rule 8.1115(e)) changes how it can be used. Status tags: "
                "<b>[V]</b> confirmed in a prior session; <b>[CHECK]</b> plausible but not yet read; nothing here is "
                "cleared for filing until pulled and read on Westlaw.", P),
      Paragraph("Connector key: <font face='Courier'>&amp;</font> and · space = or · "
                "<font face='Courier'>/s</font> same sentence · <font face='Courier'>/p</font> same paragraph · "
                "<font face='Courier'>!</font> root expander · <font face='Courier'>\"...\"</font> phrase · "
                "<font face='Courier'>%</font> but not · <font face='Courier'>CO()</font> court · "
                "<font face='Courier'>DA(aft ...)</font> date · <font face='Courier'>SY,DI()</font> synopsis/digest.", SM),
      Spacer(1, 6)]

S += [Paragraph("Start here: four moves before any searching", H2)] + bullets([
    "<b>Quick Check the complaint.</b> Upload the filed-version PDF to Westlaw Quick Check. Review the recommended "
    "authorities and any warnings on cited cases. This is the fastest way to find on-point cases the draft misses.",
    "<b>KeyCite every authority already in the complaint and memos</b> (table in Part 8). Set KeyCite Alerts on "
    "<i>Mendoza</i>, <i>Gilberg</i>, <i>Parsonage</i>, <i>Yeh</i>, <i>McInerney</i>, and <i>TransUnion</i>.",
    "<b>Pull the annotated statutes</b> (West's Ann. Cal. Penal Code § 290.46; Cal. Civ. Code §§ 1786.2, "
    "1786.16, 1786.50; Cal. Lab. Code § 432.7; Cal. Bus. &amp; Prof. Code §§ 16600–16600.5; 15 U.S.C. "
    "§§ 1681a, 1681e, 1681n, 1681o). Read current text, the Notes of Decisions, and the History notes. This "
    "settles the open text questions: § 432.7(c) intentional-violation remedy, § 290.46(j)(4)(B) "
    "aggrieved-person standing, and § 16600.5 wording.",
    "<b>Westlaw Dockets</b>: search Hertz and HireRight cases for FRCP 7.1 disclosure statements (HireRight's LLC "
    "member chain for diversity) and for prior complaints and orders on the same theories (Part 7).",
])

# ---------------------------------------------------------------- Count 1
S += [Paragraph("1. First Cause of Action — FCRA § 1681e(b) against HireRight", H2),
      Paragraph("<b>What must be established at the pleading stage:</b> (1) an inaccuracy — patently incorrect or "
                "materially misleading; (2) failure to follow reasonable procedures; (3) the report reached a third "
                "party and caused harm; (4) willfulness for statutory and punitive damages. <b>The soft spot:</b> "
                "attributing the \"[Criminal Information] Alcohols related offenses-Does not meet\" label to HireRight's "
                "adjudication service rather than to a Hertz reviewer.", P),
      qtable([
          ("Adjudication results as consumer-report information",
           '1681e(b) /p (adjudicat! "does not meet" "meets company standards" matrix grade! scor!) /p employ!'),
          ("CRA liability for employer-configured adjudication",
           '"consumer reporting agency" /p adjudicat! /p (client employer) /p (criteria matrix rule!) & 1681!'),
          ("Mislabeling non-criminal records as criminal",
           '1681e(b) /p (criminal /s (infraction traffic "administrative" DMV suspen! "license")) /p (misleading inaccura!)'),
          ("Ninth Circuit \"materially misleading\" standard",
           '"materially misleading" /s 1681e! & CO(9TH) — then KeyCite Carvalho and Shaw'),
          ("Reasonable-procedures pleading in employment screening",
           '1681e(b) /p "reasonable procedures" /p (employ! background screen!) & DA(aft 2018) & CO(CAND CACD CAED CASD 9TH)'),
          ("Willfulness after Safeco",
           '1681n /p (reckless! "objectively unreasonable") /p (background employ!) & CO(9TH CAND)'),
          ("Article III after TransUnion for misleading reports sent to employers",
           '1681e(b) /p TransUnion /p (disseminat! "third party" employer) & DA(aft 06/25/2021)'),
          ("HireRight track record",
           'HireRight & 1681e(b) — in Cases and in Dockets; note any adjudication-related rulings'),
      ])]

# ---------------------------------------------------------------- Count 2
S += [Paragraph("2. Second Cause of Action — Cal. Penal Code § 290.46(j) against Hertz", H2),
      Paragraph("<b>Elements:</b> (1) information \"disclosed pursuant to\" § 290.46; (2) use; (3) for purposes "
                "relating to employment; (4) not to protect a person at risk or otherwise authorized. "
                "<b>Soft spots:</b> the NSOPW \"federal disclosure\" argument, and use versus mere review.", P),
      qtable([
          ("Every decision construing § 290.46 employment use (current and former subdivisions)",
           '("290.46" "290.4") /p (employ! hir! terminat! rescind! applicant) — run in All State & Federal'),
          ("Historical numbering (former subd. (l)) to catch older cases",
           '"290.46(l)" "290.46 (l)" "290.4(d)"'),
          ("\"Disclosed pursuant to this section\"; derivative or national-index source",
           '("disclosed pursuant to this section" "megan\'s law" ) /p (nsopw "national sex offender" "public website" derivative indirect)'),
          ("NSOPW as conduit for state website records",
           '("national sex offender public website" nsopw) /p (state jurisdiction) /p (real-time "web service" display!)'),
          ("Meaning of \"use\" (review, screening, preliminary decision)",
           '"290.46" /p (use! /s (review! screen! consider! "preliminary"))'),
          ("\"Person at risk\" exception",
           '"person at risk" /p ("290.46" "megan\'s law") /p (employ! customer co-worker)'),
          ("Pattern-or-practice injunction (j)(4)(B)",
           '"290.46" /p "pattern or practice" /p (aggrieved injunct!)'),
          ("Information-and-belief pleading where facts are in the defendant's control",
           '"information and belief" /s "peculiarly within" /p (plausib! Iqbal Twombly) & CO(9TH)'),
          ("Iqbal \"obvious alternative explanation\" in screening/employment",
           '"obvious alternative explanation" /p (employ! background "consumer report") & CO(9TH CAND)'),
          ("Supplemental jurisdiction risk: novel state issue (§ 1367(c)(1)) and certification (CRC 8.548)",
           '1367(c)(1) /p "novel" /p (penal! "megan\'s law" "290.46") ; also "8.548" /p certif! /p employ!'),
      ]),
      Paragraph("<b>Also pull:</b> Attorney General Opinion No. 05-301 (2006) [V]; legislative history of AB 488 "
                "(2003–2004 Reg. Sess.) creating the Megan's Law website, including committee analyses on the "
                "employment-use bar [CHECK chaptering]; the later bill that renumbered former subd. (l) to (j) "
                "[CHECK which bill]. Search Westlaw's California Legislative History and Bill Analyses.", P)]

# ---------------------------------------------------------------- Count 3
S += [Paragraph("3. Third Cause of Action — ICRAA standalone disclosure against Hertz", H2),
      Paragraph("<b>Soft spots:</b> Article III in federal court for a disclosure-format claim; whether page 8 was a "
                "separate e-sign screen; whether a separate clean federal form cures anything.", P),
      qtable([
          ("Gilberg and its progeny under ICRAA",
           '"1786.16" /p ("solely of the disclosure" standalone "stand-alone") — KeyCite Gilberg, Citing References'),
          ("Electronic disclosures: separate screens and webpages",
           '(standalone "stand-alone" "solely of the disclosure") /p (electronic online screen webpage click!) /p (1681b 1786.16)'),
          ("ICRAA disclosure standing in federal court after TransUnion",
           '"1786.16" /p (standing "injury in fact" Article) & DA(aft 06/25/2021)'),
          ("Concrete harm where the undisclosed search was used against the applicant",
           '(1681b(b)(2) 1786.16) /p (standing concrete) /p ("used" adverse rescind!) & CO(9TH CAND CACD)'),
          ("\"Investigative consumer report\" reaches public-record reports",
           '"1786.2" /p "investigative consumer report" /p ("any means" "public record") — KeyCite Connor v. First Student'),
          ("Parsonage / Yeh status (review granted? depublished?)",
           'KeyCite: Parsonage v. Wal-Mart Associates (D083831); Yeh v. Barrington Pacific (B337904)'),
          ("Willful / grossly negligent (punitive under § 1786.50(b))",
           '"1786.50" /p (willful! "grossly negligent" punitive)'),
      ])]

# ---------------------------------------------------------------- Count 4
S += [Paragraph("4. Fourth Cause of Action — Cal. Labor Code § 432.7 against Hertz (alternative)", H2),
      Paragraph("<b>Soft spot:</b> whether a DMV chemical-test refusal entry is a \"record of arrest or detention that "
                "did not result in conviction,\" and whether a driver-required job justifies reviewing it.", P),
      qtable([
          ("DMV / driving records under § 432.7",
           '"432.7" /p (DMV "driving record" "motor vehicle record" "license suspension" "driver\'s license")'),
          ("What counts as a \"record of arrest\"",
           '"432.7" /p "record of arrest" /p (administrative indirect derivative mention! referenc!)'),
          ("Lawful arrest as predicate for implied consent / refusal suspension",
           '(23612 13353) /p "lawful! arrest!" /p (refus! "chemical test") — California cases'),
          ("Current § 432.7(c) remedies and the intentional-violation language",
           'Pull current statute + History notes; ("432.7(c)" "432.7, subd. (c)") /p (treble intentional "$500")'),
          ("Applicant-only treble remedy (Fowler / Faria line)",
           '"432.7" /p (applicant /s treble) — KeyCite Faria v. San Jacinto Unified School Dist. (1996) 50 Cal.App.4th 1939 [CHECK]'),
          ("Employer review of MVR for non-commercial driving jobs",
           '(1808.1 "employer pull notice") /p (employ! non-commercial "class C") ; "432.7" /p (driv! /s job position)'),
      ])]

# ---------------------------------------------------------------- Count 5
S += [Paragraph("5. Fifth Cause of Action — Bus. &amp; Prof. Code §§ 16600–16600.5 against Hertz", H2),
      Paragraph("<b>Soft spots:</b> Article III and ripeness for a pre-enforcement challenge by a prospective "
                "employee; whether an offer term requiring a non-competition agreement is itself a void provision.", P),
      qtable([
          ("All decisions applying § 16600.5 (effective 2024)",
           '"16600.5" /p ("prospective employee" "private action" injunct!)'),
          ("Offer-letter or onboarding requirements to sign a noncompete",
           '(16600 16600.1 16600.5) /p ("offer letter" onboard! "condition of employment") /p (noncompet! "non-compet!")'),
          ("Standing / ripeness for declaratory relief on an unenforced covenant",
           '16600 /p (declaratory "2201") /p (standing ripe! "not enforced" "threat!") & CO(9TH CAND CACD)'),
          ("Edwards and the broad reading of § 16600",
           'KeyCite Edwards v. Arthur Andersen LLP (2008) 44 Cal.4th 937 [V]; Citing References re employment offers'),
          ("Hertz-specific: same clause in other California cases",
           'In Dockets: Hertz & ("non-competition" noncompet!) & (16600 "16600.5")'),
      ])]

# ---------------------------------------------------------------- defenses
S += [Paragraph("6. Defenses to pre-empt and procedural issues", H2),
      qtable([
          ("Independent-source defense (Donaleski) and how plaintiffs have distinguished it",
           'KeyCite Donaleski v. Wal-Mart Stores (E.D. Cal. May 8, 2009), 2009 WL 1296257 [V]; Citing References'),
          ("Screening company is not the \"user\" (Mendoza) — limits and later treatment",
           'KeyCite Mendoza v. ADP Screening & Selection Services (2010) 182 Cal.App.4th 1644 [V]; "290.46" /p Mendoza'),
          ("Lerma dismissal (report showed no registry record) — distinguish",
           'Dockets: Lerma v. Amazon.com Services, 8:22-cv-01727 (C.D. Cal.), Dkt. 36 order [V]'),
          ("Specific-statute authorization defense (Pastrana; § 11105(c))",
           'Pastrana v. Local 9509 (S.D. Cal. 2008) [V]; "11105" /p (employ! /s authoriz!) /p "290.46"'),
          ("McGroarty (C.D. Cal. 2009) — read the order body",
           'McGroarty v. American Background Information Services, 2009 WL 980417 [CHECK reasoning]'),
          ("Anti-SLAPP in federal court reaches state claims only",
           '425.16 /p (federal /s claim) /p (inapplicable "does not apply") & CO(9TH) — KeyCite Planned Parenthood v. Ctr. for Medical Progress, 890 F.3d 828 (9th Cir. 2018) [CHECK]'),
          ("LLC citizenship pleaded on information and belief",
           'KeyCite Johnson v. Columbia Properties Anchorage, 437 F.3d 894 (9th Cir. 2006); Carolina Cas. Ins. Co. v. Team Equipment, 741 F.3d 1082 (9th Cir. 2014) [CHECK]'),
          ("FCRA preemption of the state counts (§ 1681t)",
           '1681t /p (ICRAA "1786" "290.46" "432.7") /p preempt!'),
          ("Alternative and inconsistent pleading",
           '"8(d)(2)" "8(d)(3)" /p (alternative inconsistent) /p plausib! & CO(9TH)'),
      ])]

# ---------------------------------------------------------------- dockets / intel
S += [Paragraph("7. Dockets, analytics, and fact development", H2)] + bullets([
    "<b>HireRight, LLC FRCP 7.1 statements</b> in any federal case: identifies its members and parents for the "
    "diversity allegation (¶ on HireRight citizenship).",
    "<b>Hertz Corporation FRCP 7.1 statements and 10-K</b> (Company Investigator / SEC filings): state of "
    "incorporation, principal place of business, and the parent relationship with Hertz Global Holdings.",
    "<b>Complaints pleading § 290.46(j)</b> anywhere: <font face='Courier'>\"290.46\" & (complaint petition) "
    "& (employ! hir!)</font> in Dockets. Collect allegation language that survived motions.",
    "<b>HireRight \"Managed Adjudication\"</b>: <font face='Courier'>HireRight & (\"managed adjudication\" "
    "adjudicat!)</font> in Dockets, News, and Company Investigator. Marketing and contract language can support the "
    "attribution allegation in the FCRA count.",
    "<b>Litigation Analytics</b>: San Jose Division judges' grant rates on FCRA and employment-screening Rule "
    "12(b)(6) motions, and on § 1367(c) declinations of novel state-law claims.",
    "<b>Monitor Matter 26</b> (UPS, E.D. Cal. 2:26-cv-02847): set a docket alert for Judge Delaney's ruling on the "
    "national-registry source argument.",
    "<b>Secondary sources</b>: National Consumer Law Center, <i>Fair Credit Reporting</i> (employment screening and "
    "criminal-record chapters); Rutter, <i>Cal. Practice Guide: Employment Litigation</i> (background checks; "
    "§ 432.7; Fair Chance); Witkin, <i>Summary of Cal. Law</i>; law reviews via "
    "<font face='Courier'>\"megan's law\" /p employ! /p (290.46 registr!)</font>.",
])

# ---------------------------------------------------------------- KeyCite table
S += [PageBreak(), Paragraph("8. KeyCite checklist — every authority the complaint and memos rely on", H2),
      atable([
          ("Cal. Penal Code § 290.46(j)(1)–(4)", "Count 2 elements and remedies", "Read current text; confirm (j)(4)(B) aggrieved-person standing"),
          ("15 U.S.C. §§ 1681a, 1681e(b), 1681n, 1681o, 1681p", "Count 1; jurisdiction", "Read; Notes of Decisions on adjudication"),
          ("Cal. Civ. Code §§ 1786.2, 1786.16(a)(2)(B), 1786.50", "Count 3", "Read current text"),
          ("Cal. Lab. Code § 432.7(a)(1), (c)", "Count 4", "Confirm intentional-violation remedy"),
          ("Cal. Veh. Code §§ 23612(a)(1)(A), 13353", "Arrest predicate (¶ arrest)", "Confirm text"),
          ("Cal. Bus. & Prof. Code §§ 16600, 16600.1, 16600.5", "Count 5", "Read enrolled SB 699 / AB 1076 text"),
          ("34 U.S.C. §§ 20921, 20922; DOJ SMART NSOPW/NSOR fact sheet", "Source chain", "[V]; print fact sheet for exhibit if needed"),
          ("Mendoza v. ADP Screening (2010) 182 Cal.App.4th 1644", "User = employer; anti-SLAPP risk to vendor", "[V]; KeyCite flags"),
          ("Donaleski v. Wal-Mart (E.D. Cal. 2009) 2009 WL 1296257", "Independent-source defense", "[V]; citing refs"),
          ("Gilberg v. Cal. Check Cashing Stores, 913 F.3d 1169 (9th Cir. 2019)", "Count 3", "[V] secondary; read opinion"),
          ("Parsonage v. Wal-Mart Assocs. (Cal. Ct. App. 2026) D083831", "ICRAA statutory remedy without separate injury", "[CHECK] review / depublication"),
          ("Yeh v. Barrington Pacific (Cal. Ct. App. 2026) B337904", "ICRAA remedy; UCL standing", "[CHECK]"),
          ("McInerney v. Regents (Cal. Ct. App. 2026) B339467", "Fair Chance limits (not pleaded)", "[CHECK]"),
          ("TransUnion LLC v. Ramirez, 594 U.S. 413 (2021)", "Article III", "[V]"),
          ("Carvalho v. Equifax, 629 F.3d 876 (9th Cir. 2010); Shaw v. Experian, 891 F.3d 749 (9th Cir. 2018)", "Materially misleading", "[CHECK] pin cites"),
          ("Safeco Ins. Co. v. Burr, 551 U.S. 47 (2007)", "Willfulness", "[V] general"),
          ("Polo v. Innoventions Int'l, 833 F.3d 1193 (9th Cir. 2016)", "Remand vs. dismissal (removal only)", "[V] secondary; not applicable to original federal filing"),
          ("Park v. Bd. of Trustees of CSU (2017) 2 Cal.5th 1057", "Anti-SLAPP does not reach the hiring decision", "[V]"),
          ("Connor v. First Student (2018) 5 Cal.5th 1026", "ICRAA scope", "[CHECK]"),
          ("Edwards v. Arthur Andersen (2008) 44 Cal.4th 937", "§ 16600 breadth", "[V] general"),
          ("Soo Park v. Thompson, 851 F.3d 910 (9th Cir. 2017)", "Information-and-belief pleading", "[CHECK] pin"),
          ("AG Op. No. 05-301 (2006)", "(j) is unequivocal", "[V]"),
      ])]

S += [Paragraph("9. What a strong research result looks like", H2)] + bullets([
    "A published or reasoned decision holding that registry information retrieved through NSOPW or another "
    "national index remains \"information disclosed pursuant to\" a state Megan's Law statute.",
    "Any case treating a CRA's adjudication grade or reason code as consumer-report information under § 1681e(b).",
    "Any case finding a traffic, DMV, or administrative record misreported as \"criminal\" to be materially misleading.",
    "A post-TransUnion N.D. Cal. or Ninth Circuit decision finding standing for an ICRAA or FCRA disclosure claim "
    "where the undisclosed report was used to deny employment.",
    "Any § 16600.5 decision allowing a prospective employee's claim based on an offer-letter noncompete term.",
    "Anything adverse to the complaint's theories: log it, then decide whether to amend before filing.",
])

doc = SimpleDocTemplate(sys.argv[1], pagesize=letter, leftMargin=0.8 * inch, rightMargin=0.8 * inch,
                        topMargin=0.75 * inch, bottomMargin=0.8 * inch,
                        title="Westlaw Research Plan - Ngwa Nforbi v. Hertz", author="Brendan Ngwa Nforbi")
doc.build(S, onFirstPage=footer, onLaterPages=footer)
print(sys.argv[1])
