#!/usr/bin/env python3
"""Matter 29 — Plaintiff's second-wave written discovery to Accurate Background, LLC.
Newanforbi v. Amazon.com Services, LLC, et al., N.D. Cal. No. 4:26-cv-09249-ASK.

Builds, on the portfolio pleading paper, with the stretched signature:
  1. Plaintiff's Requests for Production to Accurate, Set Two (Nos. 21-33)
  2. Plaintiff's Interrogatories to Accurate, Set One (Nos. 1-21)
  3. Plaintiff's Requests for Admission to Accurate, Set One (Nos. 1-18), with
     Exhibit A (Oct. 14, 2026 consumer report) and Exhibit B (Oct. 28, 2026
     closing letter and enclosed report) appended when their PDFs are supplied.

Source text: the Nov. 11, 2026 revised drafts (precision and face-of-document
framing, preservation requests, mail-only service), merged with the Oct. 31
consolidated plan (internal/private/research/matter-29-discovery/
SYNTHESIS-3-MODEL.md) on three leverage points: firm-wide matching and alias
rules not limited to rules "applied" (RFP 26), the full governing agreement
with prices redacted (RFP 28), and post-2023 procedure changes and prior
false-alias matters (RFP 32; Interrogatory 20). Parole-status requests and the
four held RFAs remain out. Net-worth discovery is dropped.

Service is by first-class mail to counsel of record (no written consent to
email service); the email copy is a courtesy and is not relied on.

Discovery is served, not filed (Fed. R. Civ. P. 5(d)(1)(A)). Nothing is served
until Plaintiff serves it.

    python3 internal/scripts/matter29-accurate-discovery-set2.py --out-dir <dir> \\
        [--date "November 11, 2026"] [--exhibit-a <pdf>] [--exhibit-b <pdf>]
"""

from __future__ import annotations

import argparse
import importlib.util
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR / "lib"))
from pleading_paper import PleadingPaper  # noqa: E402
from pypdf import PdfReader, PdfWriter  # noqa: E402

_spec = importlib.util.spec_from_file_location(
    "m29zoom", SCRIPT_DIR / "matter29-zoom-appearance-admin-motion.py")
Z = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(Z)

CASE_NO, CASE_FILE, JUDGE = Z.CASE_NO, Z.CASE_FILE, Z.JUDGE
DEFAULT_DATE = "November 12, 2026"


def caption(title: list[str], set_label: str, rules: str) -> list[tuple[str, bool, bool]]:
    rows = [(f"Case No. {CASE_NO}", True, False), ("", False, False)]
    rows += [(t, True, False) for t in title]
    rows += [("", False, False),
             ("Propounding Party: Plaintiff", False, False),
             ("Responding Party: Accurate Background, LLC", False, False),
             (f"Set No.: {set_label}", False, False),
             (rules, False, False),
             (f"Judge: {JUDGE}", False, False)]
    return rows


TO_LINE = ("SUBHEAD", "TO DEFENDANT ACCURATE BACKGROUND, LLC AND ITS ATTORNEYS OF RECORD:")

DEFS_COMMON = ("\"Screening Order\" means Accurate reference 496623722; \"Report\" means Y94611404. \"Original "
               "report\" means the version bearing \"updated on 10/14/2026\" furnished to Plaintiff on October 14, "
               "2026. \"Revised report\" means the copy enclosed with Accurate's October 28, 2026 consumer closing "
               "letter. \"File disclosure\" means the separate disclosure bearing an October 27, 2026 cover and sent "
               "by Accurate's counsel on October 30, 2026. \"You\" and \"Accurate\" mean Defendant Accurate "
               "Background, LLC and its personnel, agents, vendors acting on its behalf, and systems. \"Amazon\" "
               "means Amazon.com Services, LLC and any affiliate that requested or received the Screening Order.")

SERVICE_LIST = [
    "Andrew P. Frederick, Morgan, Lewis & Bockius LLP, 1400 Page Mill Road, Palo Alto, CA 94304 "
    "(counsel for Defendant Amazon.com Services, LLC).",
    "Douglass G. Brown, Morgan, Lewis & Bockius LLP, 1717 Main Street, Suite 3200, Dallas, TX 75201 "
    "(counsel for Defendant Amazon.com Services, LLC).",
    "Jasmine J. Stanzick, Seyfarth Shaw LLP, 2029 Century Park East, Suite 3500, Los Angeles, CA "
    "90067-3021 (counsel for Defendant Accurate Background, LLC).",
]
COURTESY = ("On the same date, I also emailed copies to the counsel listed above (andrew.frederick@morganlewis.com; "
            "douglass.brown@morganlewis.com; jstanzick@seyfarth.com) and to John Drury (jdrury@seyfarth.com) as a "
            "courtesy. I do not rely on that email as electronic service under Rule 5(b)(2)(E).")

# ---------------------------------------------------------------- RFP Set Two
RFP_INTRO = [
    TO_LINE,
    ("PARA", "Under Federal Rules of Civil Procedure 26 and 34, Plaintiff Brendan Ngehsi Newanforbi requests "
             "that Defendant Accurate Background, LLC produce the documents and electronically stored "
             "information identified below within the time allowed by the Federal Rules."),
    ("HEADER", "DEFINITIONS AND INSTRUCTIONS"),
    ("PARA", "1. " + DEFS_COMMON),
    ("PARA", "2. Set One Requests for Production Nos. 1-20 and their definitions and instructions are "
             "incorporated to the extent consistent with these more specific definitions. Requests Nos. 21-33 "
             "supplement Set One; they do not withdraw or narrow any Set One request. The default Set One period "
             "ends November 15, 2026; a request that expressly extends through the date of response controls."),
    ("PARA", "3. State whether any responsive material is being withheld on the basis of an objection, as "
             "Rule 34(b)(2)(C) requires. Produce native or reasonably usable structured records where needed to "
             "preserve search parameters, timestamps, status codes, and version links. Do not unilaterally redact "
             "responsive material for confidentiality; use the protective order entered or to be entered in this "
             "action. Log any document withheld on a claim of privilege as Rule 26(b)(5) requires."),
    ("HEADER", "REQUESTS FOR PRODUCTION"),
]
RFPS = [
    "Produce the native or structured request and response exchanged for National Sex Offender Database Search "
    "496623723, including submitted name fields and other matching fields, vendor identity, timestamps, returned "
    "status, and any later request or response for that component through the date of response. Produce the "
    "record linking each result to each version of report Y94611404. If no later search occurred, state that in "
    "the Rule 34 response; no document is demanded to prove a negative.",
    "Produce the native or structured request and response for National Criminal Database Search 496623727 on "
    "order 496623722, including the submitted name and matching fields, vendor, timestamps, returned results or "
    "no-result status, and any review or exclusion code applied before report Y94611404 was generated.",
    "For San Joaquin County search 496644200, produce the source or vendor records, matching and exclusion "
    "decisions, and communications explaining the treatment of the three entries identified in the file "
    "disclosure by case references STK-CR-FMISC-2020-0002397, STK-CR-FMISC-2020-0004747, and "
    "STK-CR-FMISC-2025-0004687, including the meaning of the name-match and date-of-birth-match fields, any "
    "verification against court records, and whether any information about those entries was included in any "
    "report version or transmitted to Amazon.",
    "Produce the native or structured request and response exchanged with the vendor for Santa Clara County "
    "search 496644204, including the name fields as sent, the original source of those fields, timestamps, vendor "
    "case-source records, and any correction, manual review, or matching decision concerning the first-name value "
    "\"NEWANSORBI\" and last-name value \"NGWA.\"",
    "Produce version identifiers, generation and modification logs, and a copy or native export of each version "
    "of report Y94611404 from October 14, 2026 through the date of response, including the revision described in "
    "Accurate's October 28, 2026 letter. For each version, produce records showing when the challenged alias was "
    "added or removed and when that version was made available to or accessed by Amazon. Produce the October 2026 "
    "dispute status audit entries, distinguishing status updates from report deliveries.",
    "Produce the matching, name-normalization, alias-generation, \"Provided by Applicant,\" vendor-review, and "
    "reportability rules for criminal-history, national-criminal, and sex-offender searches in employment "
    "reports, in the versions operative on July 7, 2026 and when the October 2026 revision was made, and any "
    "version changed after May 26, 2023, together with the code definitions needed to interpret the produced "
    "results. This request is not limited to rules You contend were applied to order 496623722.",
    "Produce the certification, authorization, and employment-purpose representations received by Accurate for "
    "order 496623722, and the final content and dispatch or delivery records of notices Accurate generated or sent "
    "concerning that order. For any notice displaying \"[LINK]\" or \"[ENLACE]\" in a copy, produce the "
    "transmitted electronic version and the recorded hyperlink target, if any.",
    "Produce the account configuration, order instructions, service agreement, and statement of work that "
    "governed order 496623722, including amendments in force between July 7 and October 28, 2026, and the "
    "permissible-purpose and employment certifications then in effect. Pricing terms may be redacted; "
    "compliance, notice, report-delivery, certification, and adjudication or eligibility terms may not.",
    "Produce the nonprivileged ordinary-course records for dispute service request 20261014-15421955 showing "
    "intake, allegations received, steps taken to investigate the challenged alias and the national sex-offender "
    "search, any source or vendor contact, responses, report changes, completion, and notice or delivery of the "
    "revised report to Amazon. Produce responsive business records even if they were later provided to counsel; "
    "log any document withheld on a specific privilege claim.",
    "Produce nonprivileged ordinary-course communications in Accurate's possession, custody, or control with "
    "Amazon concerning order 496623722 from July 7, 2026 through the date of response, concerning identity "
    "inputs, search exceptions, report or component results, pending or status messages, furnishing or access, "
    "eligibility or adjudication, and report corrections. Include attachments and system messages.",
    "Produce the retention schedules, deletion or purge settings, preservation notices, and preservation actions "
    "that applied to order 496623722, its component searches, report versions, Amazon access logs, and dispute "
    "service request 20261014-15421955 from July 7, 2026 through the date of response, and records of any "
    "deletion, overwrite, or loss of those records.",
    "Produce nonprivileged documents sufficient to identify changes made after May 26, 2023 to Your procedures "
    "for sex-offender or alias handling in employment reports, and documents sufficient to identify lawsuits or "
    "regulator matters from January 1, 2023 through July 7, 2026 alleging a false alias or inaccurate "
    "registry information in an employment report. This request does not seek settlement agreements.",
    "To the extent not already produced, produce any insurance agreement under which an insurer may be liable to "
    "satisfy all or part of a possible judgment in this action or to indemnify or reimburse Accurate for payments "
    "made to satisfy the judgment.",
]

# ---------------------------------------------------------------- Interrogatories
ROG_INTRO = [
    TO_LINE,
    ("PARA", "Under Federal Rules of Civil Procedure 26 and 33, Plaintiff Brendan Ngehsi Newanforbi requests "
             "that Defendant Accurate Background, LLC answer each interrogatory separately and fully in writing "
             "under oath within the time allowed by the Federal Rules."),
    ("HEADER", "DEFINITIONS AND INSTRUCTIONS"),
    ("PARA", "1. " + DEFS_COMMON + " \"Reinvestigation\" means the reinvestigation of service request "
             "20261014-15421955."),
    ("PARA", "2. State times with time zone. An answer under Rule 33(d) must identify the responsive records by "
             "Bates number with enough specificity for Plaintiff to locate the answer. Personal identifiers need "
             "not be restated in a narrative answer when a produced, protected record supplies them. If You object "
             "to part of an interrogatory, answer the remainder."),
    ("HEADER", "INTERROGATORIES"),
]
ROGS = [
    "State when Amazon first could access any result or status of order 496623722 in Accurate's systems, "
    "identifying the status or result then available.",
    "State when the report version bearing \"updated on 10/14/2026\" was first transmitted to or made accessible "
    "to Amazon; if it was never transmitted or accessible, state that.",
    "Identify the source record and method by which \"NEWANSORBI\" was added to the alias line labeled "
    "\"Provided by Applicant\" in the original report.",
    "For search 496623723, identify the names and categories of other identifiers submitted to the vendor and the "
    "transmission time, referring to Bates-numbered native records for the identifier values.",
    "State whether National Sex Offender Database Search 496623723 was run again after July 7, 2026, and, if so, "
    "give the date and returned status of each re-run.",
    "Identify the vendor and returned status for National Criminal Database Search 496623727, distinguishing raw "
    "results from information included in any consumer report.",
    "State whether any component search of the Screening Order, including the Santa Clara County search or the "
    "National Sex Offender Database Search, was queried again in the Reinvestigation; identify each such query "
    "and its date, or state that none occurred.",
    "State the dates and times Accurate opened and completed the Reinvestigation, with time zone.",
    "Identify any source or vendor contacted about either disputed item during the Reinvestigation, or state that "
    "none was contacted.",
    "Explain what \"updated on 10/14/2026\" denotes in the report enclosed with Accurate's October 28, 2026 "
    "letter, including whether the notation reflects generation, a data refresh, or another system field.",
    "Explain the matching and reportability decision by which raw San Joaquin County search 496644200, including "
    "the three STK-CR-FMISC entries identified in the file disclosure, became the \"NO RECORD FOUND\" result in "
    "the original report, and state whether any information concerning those entries was made accessible to "
    "Amazon outside the printed report.",
    "State the Santa Clara County result or status available to the reviewer when package review 500363362 was "
    "completed on October 13, 2026.",
    "State the recorded reason, if any, that Santa Clara County search 496644204 was not completed until "
    "October 14, 2026.",
    "Explain how the first-name \"NEWANSORBI\" and last-name \"NGWA\" fields in the Santa Clara County vendor "
    "request for search 496644204 were generated, identifying their source data and any automated transformation "
    "or manual entry.",
    "State the recorded basis for selecting Santa Clara County for search 496644204 on order 496623722.",
    "Identify the entity and account from which Accurate received the employment-purpose certification for "
    "order 496623722, and the date the certification applicable to that order was received.",
    "State any status, adjudication, or eligibility result that Accurate communicated to Amazon for order "
    "496623722, and when; if Accurate communicated none, state that.",
    "State the date, time, recipient account, and delivery channel for the revised report described in "
    "Accurate's October 28, 2026 letter, and distinguish posting from any actual access or download shown in "
    "Accurate's logs.",
    "For the Santa Clara County public-record information included in report Y94611404, identify the notice, if "
    "any, Accurate sent under 15 U.S.C. § 1681k(a)(1), or the procedure it used to obtain information current as "
    "of reporting under § 1681k(a)(2).",
    "Identify the matching and verification procedure applied to National Sex Offender Database Search 496623723 "
    "when it was run and during the Reinvestigation, including the operative procedure version or effective "
    "date, and identify each change to that procedure for employment reports after May 26, 2023, or state that "
    "there was none.",
    "Identify any order, component-search, report-version, access-log, or dispute-case records for order "
    "496623722 that Accurate knows were deleted, overwritten, or lost after July 7, 2026, and state when that "
    "occurred; if none is known, say so.",
]

# ---------------------------------------------------------------- RFAs
RFA_INTRO = [
    TO_LINE,
    ("PARA", "Under Federal Rules of Civil Procedure 26 and 36, Plaintiff Brendan Ngehsi Newanforbi requests "
             "that Defendant Accurate Background, LLC admit each matter below and the genuineness of the attached "
             "Exhibits A and B within the time allowed by the Federal Rules."),
    ("HEADER", "DEFINITIONS AND INSTRUCTIONS"),
    ("PARA", "1. " + DEFS_COMMON),
    ("PARA", "2. Exhibit A is the original report as furnished to Plaintiff on October 14, 2026. Exhibit B is "
             "Accurate's October 28, 2026 consumer closing letter and the enclosed revised report, as transmitted "
             "by Accurate's counsel on October 28, 2026. Neither exhibit is the file disclosure. The exhibits "
             "contain Plaintiff's personal identifiers; they are served on counsel and are not filed."),
    ("PARA", "3. Requests refer to the face of the identified records unless they expressly ask about an "
             "underlying event. Respond under Rule 36(a). A matter is admitted unless, within the time allowed, "
             "You serve a written answer or objection addressed to it (Rule 36(a)(3)). Under Rule 37(c)(2), if "
             "You fail to admit a matter that Plaintiff later proves, Plaintiff may seek the reasonable expenses "
             "of making that proof."),
    ("HEADER", "REQUESTS FOR ADMISSION"),
]
RFAS = [
    "Admit that Amazon.com Services, LLC requested Accurate screening order 496623722 concerning Plaintiff.",
    "Admit that Accurate prepared report Y94611404 under screening order 496623722, which bears an order date of "
    "July 7, 2026.",
    "Admit that Exhibit A displays \"NGWA NFORBI, NEWANSORBI\" as an alias labeled \"Provided by Applicant.\"",
    "Admit that Accurate's October 28, 2026 letter states that the updated report removes the disputed alias.",
    "Admit that the report enclosed with Accurate's October 28, 2026 letter does not display the alias line "
    "identified in Request No. 3.",
    "Admit that the report enclosed with Accurate's October 28, 2026 letter bears the printed notation "
    "\"updated on 10/14/2026.\"",
    "Admit that Exhibit A displays National Sex Offender Database Search 496623723 as \"NO RECORD FOUND\" and "
    "completed July 7, 2026.",
    "Admit that the entry for search 496623723 in Exhibit A does not display the names submitted for that search.",
    "Admit that the file disclosure identifies Tauxbe Data Inc. as a source for the National Sex Offender "
    "Database Search associated with report Y94611404.",
    "Admit that the raw Santa Clara County vendor-request data in the file disclosure for search 496644204 "
    "contains a first-name field \"NEWANSORBI\" and a last-name field \"NGWA.\"",
    "Admit that the raw San Joaquin County result for search 496644200 in the file disclosure lists case "
    "references STK-CR-FMISC-2020-0002397, STK-CR-FMISC-2020-0004747, and STK-CR-FMISC-2025-0004687, with "
    "\"identified_by_name\" set to false and \"identified_by_dob\" set to true for each entry.",
    "Admit that Exhibit A displays the San Joaquin County component 496644200 as \"NO RECORD FOUND.\"",
    "Admit that Accurate's October 28, 2026 letter states that Accurate received Plaintiff's disputes on "
    "October 15, 2026.",
    "Admit that Accurate's October 28, 2026 letter states that Accurate forwarded a copy of the revised report to "
    "the employer that requested it.",
    "Admit that Exhibit A displays package review 500363362 as completed October 13, 2026.",
    "Admit that Exhibit A displays Santa Clara County search 496644204 as completed October 14, 2026.",
    "Admit that Exhibit A is a true copy of the report bearing \"updated on 10/14/2026\" supplied to Plaintiff by "
    "Accurate on October 14, 2026.",
    "Admit that Exhibit B is a true copy of the October 28, 2026 consumer closing letter and enclosed report sent "
    "to Plaintiff as the attachment to Accurate's counsel's October 28, 2026 email.",
]


def _numbered(label: str, items: list[str], start: int) -> list[tuple[str, str]]:
    out: list[tuple[str, str]] = []
    for i, t in enumerate(items, start):
        out.append(("SUBHEAD", f"{label} NO. {i}:"))
        out.append(("PARA", t))
    return out


def _pos(d: PleadingPaper, doc_titles: str, date: str, city: str) -> None:
    d.start_new_page()
    Z._render_body(d, [
        ("HEADER", "PROOF OF SERVICE"),
        ("PARA", "I am the Plaintiff in this action. My address is 1455 Cat Tail Drive, Stockton, CA 95204. "
                 f"On {date}, I served {doc_titles} by placing true copies in sealed envelopes with first-class "
                 f"postage prepaid and depositing them with the United States Postal Service at {city}, "
                 "California, addressed as follows (Fed. R. Civ. P. 5(b)(2)(C)):"),
    ] + [("LIST_ITEM", f"{i}. {t}") for i, t in enumerate(SERVICE_LIST, 1)] + [("PARA", COURTESY)])
    d.ensure_space(10)  # perjury clause + date + signature block stay on one page
    d.write_wrapped("I declare under penalty of perjury under the laws of the United States of America that "
                    "the foregoing is true and correct.", first_indent=36)
    d.blank_line()
    d.write_line(f"Dated: {date}")
    Z._signature(d, None, closer=False)


def _exhibit(w: PdfWriter, tmp: Path, letter: str, desc: str, src: Path | None) -> None:
    cover = tmp / f"_exh_{letter}.pdf"
    d = PleadingPaper(str(cover), doc_title_footer=f"EXHIBIT {letter}")
    for _ in range(10):
        d.blank_line()
    d.write_line(f"EXHIBIT {letter}", bold=True, center=True)
    d.blank_line()
    d.write_wrapped(desc)
    d.save()
    w.append(str(cover))
    cover.unlink()
    if src:
        w.append(str(src))


def build(out_dir: Path, date: str, exa: Path | None, exb: Path | None, city: str = "Stockton") -> list[Path]:
    outs = []
    specs = [
        ("RFP", f"Plaintiff's Requests for Production to Accurate - Set Two - {CASE_FILE}.pdf",
         ["PLAINTIFF'S REQUESTS FOR", "PRODUCTION OF DOCUMENTS TO", "DEFENDANT ACCURATE", "BACKGROUND, LLC (SET TWO)"],
         "Two", "(Fed. R. Civ. P. 26, 34)", "PLAINTIFF'S RFPs TO ACCURATE (SET TWO) -- NEWANFORBI v. AMAZON",
         RFP_INTRO + _numbered("REQUEST FOR PRODUCTION", RFPS, 21),
         "PLAINTIFF'S REQUESTS FOR PRODUCTION OF DOCUMENTS TO DEFENDANT ACCURATE BACKGROUND, LLC (SET TWO)"),
        ("ROG", f"Plaintiff's Interrogatories to Accurate - Set One - {CASE_FILE}.pdf",
         ["PLAINTIFF'S INTERROGATORIES", "TO DEFENDANT ACCURATE", "BACKGROUND, LLC (SET ONE)"],
         "One", "(Fed. R. Civ. P. 26, 33)", "PLAINTIFF'S INTERROGATORIES TO ACCURATE (SET ONE) -- NEWANFORBI v. AMAZON",
         ROG_INTRO + _numbered("INTERROGATORY", ROGS, 1),
         "PLAINTIFF'S INTERROGATORIES TO DEFENDANT ACCURATE BACKGROUND, LLC (SET ONE)"),
        ("RFA", f"Plaintiff's Requests for Admission to Accurate - Set One - {CASE_FILE}.pdf",
         ["PLAINTIFF'S REQUESTS FOR", "ADMISSION TO DEFENDANT", "ACCURATE BACKGROUND, LLC", "(SET ONE)"],
         "One", "(Fed. R. Civ. P. 26, 36)", "PLAINTIFF'S RFAs TO ACCURATE (SET ONE) -- NEWANFORBI v. AMAZON",
         RFA_INTRO + _numbered("REQUEST FOR ADMISSION", RFAS, 1),
         "PLAINTIFF'S REQUESTS FOR ADMISSION TO DEFENDANT ACCURATE BACKGROUND, LLC (SET ONE), with "
         "Exhibits A and B"),
    ]
    for kind, fname, title, setno, rules, footer, content, pos_title in specs:
        body = out_dir / ("_body_" + fname)
        d = PleadingPaper(str(body), doc_title_footer=footer)
        Z._header_block(d, caption(title, setno, rules))
        Z._render_body(d, content)
        Z._signature(d, date)
        _pos(d, pos_title, date, city)
        d.save()
        final = out_dir / fname
        w = PdfWriter()
        w.append(str(body))
        if kind == "RFA":
            _exhibit(w, out_dir, "A", "Accurate Background consumer report, reference 496623722, requestor "
                     "\"Amazon HVH,\" bearing \"updated on 10/14/2026,\" furnished to Plaintiff October 14, 2026. "
                     "Contains a partial date of birth and the last four digits of Plaintiff's Social Security "
                     "number; served on counsel only, not filed.",
                     exa)
            _exhibit(w, out_dir, "B", "Accurate Background letter to Plaintiff dated October 28, 2026, with "
                     "enclosed report, transmitted by Accurate's counsel October 28, 2026. Contains date of "
                     "birth; served on counsel only, not filed.", exb)
        w.write(str(final))
        body.unlink()
        outs.append(final)
    return outs


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--date", default=DEFAULT_DATE)
    ap.add_argument("--exhibit-a", type=Path)
    ap.add_argument("--exhibit-b", type=Path)
    ap.add_argument("--mail-city", default="Stockton")
    a = ap.parse_args()
    od = Path(a.out_dir)
    od.mkdir(parents=True, exist_ok=True)
    for p in build(od, a.date, a.exhibit_a, a.exhibit_b, a.mail_city):
        print(p, len(PdfReader(str(p)).pages), "pp")


if __name__ == "__main__":
    main()
