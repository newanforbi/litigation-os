#!/usr/bin/env python3
"""Matter 29 — Plaintiff's second-wave written discovery to Accurate Background, LLC.
Newanforbi v. Amazon.com Services, LLC, et al., N.D. Cal. No. 4:26-cv-09249-ASK.

Builds, on the portfolio pleading paper, with the stretched signature:
  1. Plaintiff's Requests for Production to Accurate, Set Two (Nos. 21-32)
  2. Plaintiff's Interrogatories to Accurate, Set One (Nos. 1-22)
  3. Plaintiff's Requests for Admission to Accurate, Set One (Nos. 1-18), with
     Exhibit A (Oct. 14, 2026 consumer report) and Exhibit B (Oct. 28, 2026
     closing letter and enclosed report) appended when their PDFs are supplied.

Source text: internal/private/research/matter-29-discovery/SYNTHESIS-3-MODEL.md,
Consolidated plan, sections A-C (Oct. 31, 2026). Set Two RFP 25 (parole
language) and the four held RFAs are omitted, as that plan directs; Set Two is
renumbered consecutively from 21.

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
DEFAULT_DATE = "November 11, 2026"


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

SERVICE_LIST = [
    "Andrew P. Frederick and Douglass G. Brown, Morgan, Lewis & Bockius LLP, 1400 Page Mill Road, "
    "Palo Alto, CA 94304 (andrew.frederick@morganlewis.com; douglass.brown@morganlewis.com), counsel "
    "for Defendant Amazon.com Services, LLC.",
    "Jasmine J. Stanzick, Seyfarth Shaw LLP, [VERIFY ADDRESS OF RECORD] (jstanzick@seyfarth.com), "
    "counsel for Defendant Accurate Background, LLC.",
    "John Drury, Seyfarth Shaw LLP, 233 S. Wacker Drive, Suite 8000, Chicago, IL 60606-6448 "
    "(jdrury@seyfarth.com), counsel for Defendant Accurate Background, LLC.",
]

# ---------------------------------------------------------------- RFP Set Two
RFP_INTRO = [
    TO_LINE,
    ("PARA", "Under Federal Rules of Civil Procedure 26 and 34, Plaintiff Brendan Ngehsi Newanforbi "
             "requests that Defendant Accurate Background, LLC produce the documents described below "
             "within thirty (30) days of service, at the address in the caption or by electronic "
             "delivery to bnn.cdl@gmail.com."),
    ("HEADER", "DEFINITIONS AND INSTRUCTIONS"),
    ("PARA", "1. The Definitions and Instructions in Plaintiff's First Requests for Production of "
             "Documents to Defendant Accurate Background, LLC (Set One) apply to these requests and are "
             "incorporated by reference, including the definitions of \"You,\" \"Plaintiff,\" "
             "\"Screening Order\" (Accurate reference 496623722 and its component search IDs), and "
             "\"Document.\""),
    ("PARA", "2. These requests supplement Set One. They do not withdraw, narrow, or replace any Set One "
             "request. Numbering continues from Set One."),
    ("PARA", "3. \"Report\" means background report Y94611404 prepared on the Screening Order, in every "
             "version. \"Dispute\" means Plaintiff's October 14, 2026 dispute and file request, service "
             "request 20261014-15421955, and the reinvestigation that followed."),
    ("PARA", "4. Where a request asks for raw input or raw output, produce the data as transmitted to or "
             "received from the vendor or source in its native or structured form. A formatted report "
             "block is not raw output."),
    ("PARA", "5. Pricing terms may be redacted where a request so states. Material designated "
             "confidential may be produced under the protective order entered or to be entered in this "
             "action. Log any document withheld on a claim of privilege as Rule 26(b)(5) requires."),
    ("HEADER", "REQUESTS FOR PRODUCTION"),
]
RFPS = [
    "Produce the raw input and raw output of National Sex Offender Database Search 496623723, including "
    "every name and identifier transmitted, the date and time, the vendor (including Tauxbe Data Inc.), "
    "the vendor's response, and any re-run after October 14, 2026. If there was no re-run, produce the "
    "record that shows the July 7, 2026 search is the search relied on in the revised Report.",
    "Produce the raw input and raw output of National Criminal Database Search 496623727, including the "
    "vendor's identity, every name searched, the date and time, and the vendor's response.",
    "Produce the record of the decision to report County Criminal search 496644200 (San Joaquin County) "
    "as \"NO RECORD FOUND,\" including the rule applied to case numbers STK-CR-FMISC-2020-0002397, "
    "STK-CR-FMISC-2020-0004747, and STK-CR-FMISC-2025-0004687; the vendor's transmission; and the search "
    "parameters the vendor was given. This request does not seek a new court pull of those cases.",
    "Produce the complete vendor file for County Criminal search 496644204 (Santa Clara County), including "
    "images and runner notes; the record showing why the principal name transmitted was first name "
    "\"NEWANSORBI\" and last name \"NGWA\"; and the record showing why Santa Clara County was selected.",
    "Produce every version of the Report saved on or after October 14, 2026, and the audit events that "
    "removed \"NEWANSORBI\" from the alias block and from each names-searched list, including whether any "
    "component was queried again; the event recorded as \"2026-10-19 09:42:29: Dispute has been "
    "initiated\"; and the assembly of the file disclosure that bears an October 27, 2026 cover and "
    "includes a letter dated October 28, 2026.",
    "Supplementing Request No. 8: produce the alias-generation, name-normalization, \"Provided by "
    "Applicant,\" and date-of-birth-only inclusion and exclusion rules for criminal-history, "
    "national-criminal, and sex-offender searches in employment reports, in the versions in effect on "
    "July 7, September 3, and October 14, 2026, and any version changed after May 26, 2023. This request "
    "is not limited to rules You contend were applied to the Screening Order.",
    "Produce the disclosure, authorization, and certification forms, and the e-signature audit trail, "
    "used for the Screening Order, and the FCRA and ICRAA notices actually sent to Plaintiff, with "
    "dispatch records. If a template contains \"[LINK]\" or \"[ENLACE],\" produce the destination those "
    "tokens resolved to in the notice sent to Plaintiff.",
    "Supplementing Request No. 16: produce the screening agreement, statement of work, and account "
    "configuration governing the Screening Order, package \"General Package,\" requestor \"Amazon HVH,\" "
    "including amendments in effect on July 7, 2026; the permissible-purpose and employment "
    "certifications then in effect; and the adjudication or eligibility rules for that package. Prices "
    "may be redacted. Compliance and adjudication terms may not.",
    "Supplementing Request No. 18: produce the ordinary-course dispute file for service request "
    "20261014-15421955, including vendor and furnisher communications, searches run or not run, the "
    "decision to remove the alias, and the transmittal of the revised Report to Amazon. Communications "
    "with Your counsel are excluded. Copying counsel on an ordinary-course dispute record does not exempt "
    "it.",
    "Supplementing Request No. 19: produce nonprivileged communications with Amazon.com Services, LLC or "
    "any Amazon affiliate about the Screening Order from July 1, 2026 through the date of production "
    "concerning status, pending status, eligibility, adjudication, furnishing, the October 14, 2026 "
    "Report, and the revised Report.",
    "Produce nonprivileged documents sufficient to identify changes made after May 26, 2023 to Your "
    "procedures for sex-offender or alias handling in employment reports, and documents sufficient to "
    "identify lawsuits or regulator matters from January 1, 2023 through July 7, 2026 alleging a false "
    "alias or registry information in an employment report. This request does not seek settlement "
    "agreements.",
    "Produce any insurance agreement under which an insurer may be liable to satisfy all or part of a "
    "judgment in this action, unless You have already produced it. Documents sufficient to show Your net "
    "worth may be produced on a schedule set by agreement or order after a showing on willfulness; that "
    "scheduling does not defer any other request.",
]

# ---------------------------------------------------------------- Interrogatories
ROG_INTRO = [
    TO_LINE,
    ("PARA", "Under Federal Rules of Civil Procedure 26 and 33, Plaintiff Brendan Ngehsi Newanforbi "
             "requests that Defendant Accurate Background, LLC answer each interrogatory below separately "
             "and fully in writing under oath within thirty (30) days of service."),
    ("HEADER", "DEFINITIONS AND INSTRUCTIONS"),
    ("PARA", "1. \"You\" and \"Accurate\" mean Defendant Accurate Background, LLC and its personnel, "
             "agents, vendors acting on its behalf, repositories, and systems. \"Amazon\" means "
             "Amazon.com Services, LLC and any affiliate that requested or received the Screening Order. "
             "\"Plaintiff\" means the plaintiff under the names and name variants used in the screening "
             "records."),
    ("PARA", "2. \"Screening Order\" means Accurate reference 496623722 and its component searches. "
             "\"Report\" means background report Y94611404, in every version. \"Reinvestigation\" means "
             "the reinvestigation of service request 20261014-15421955."),
    ("PARA", "3. \"Identify,\" for a person, means full name, title, employer, and last known business "
             "address; for an entity, its name and address; for a system or account, its name and "
             "identifier; for a document, its date, author, recipients, and Bates number if produced."),
    ("PARA", "4. State times with time zone. If You answer by reference to records under Rule 33(d), "
             "specify the records by Bates number in enough detail for Plaintiff to locate the answer."),
    ("PARA", "5. Each interrogatory addresses one subject. If You object to part of an interrogatory, "
             "answer the remainder. If You lack information, say so and describe the inquiry made."),
    ("HEADER", "INTERROGATORIES"),
]
ROGS = [
    "State the date and time You first made any result or status of the Screening Order accessible to "
    "Amazon, and identify the system and account.",
    "State whether You issued the Report that bears \"updated on 10/14/2026,\" and the date and time it "
    "was first furnished or made accessible to Amazon.",
    "Identify the original source of the string \"NEWANSORBI,\" and state whether the label \"Provided by "
    "Applicant\" means that Plaintiff typed it.",
    "State every name and identifier transmitted for search 496623723, the date and time of "
    "transmission, and the vendor.",
    "State whether search 496623723 was run again after July 7, 2026. If it was, state the date and "
    "result. If it was not, say so.",
    "Identify the vendor and every name and identifier used for search 496623727, and describe every "
    "result that search returned.",
    "State whether any component of the Screening Order was queried again after Plaintiff's October 2026 "
    "dispute. If any was, identify it and the date. If none was, say so.",
    "State the date and time the Reinvestigation was opened and the date and time it was completed.",
    "Identify each furnisher or vendor contacted in the Reinvestigation. If none was contacted, say so.",
    "State why the report enclosed with Your October 28, 2026 letter still bears \"updated on "
    "10/14/2026.\"",
    "For each of case numbers STK-CR-FMISC-2020-0002397, STK-CR-FMISC-2020-0004747, and "
    "STK-CR-FMISC-2025-0004687, state whether You included that case in the Report furnished to Amazon "
    "and, if not, the reason recorded in Your system. Do not describe the underlying offense.",
    "Identify the person or service account that completed package review 500363362, and state what "
    "Santa Clara County result, if any, was in the file at that time.",
    "State the reason recorded for Santa Clara County search 496644204 completing on October 14, 2026.",
    "State who or what set the principal name on the Santa Clara County request to first name "
    "\"NEWANSORBI\" and last name \"NGWA,\" and whether the value came from Amazon's intake data, an alias "
    "rule, or a manual entry.",
    "State why Santa Clara County was selected for a search on the Screening Order.",
    "Identify the Amazon entity and account certified to receive the Screening Order, the date of the "
    "certification in effect on July 7, 2026, and the title and date of the written agreement then in "
    "effect.",
    "State the adjudication or eligibility result, if any, You communicated to Amazon for the Screening "
    "Order, and the date. If none, say so.",
    "State the date, recipient, and channel of transmission of the revised report described in Your "
    "October 28, 2026 letter.",
    "State which alternative under 15 U.S.C. § 1681k(a) You contend You satisfied for the Santa Clara "
    "County public-record information in the Report, and identify the notice or procedure.",
    "Identify each change after May 26, 2023 to Your procedure for a national sex-offender database "
    "search in an employment report. If there was none, say so.",
    "State the fiscal year-end of Your latest financial statement that states net worth. An objection "
    "that net-worth discovery is premature does not excuse an answer to any other interrogatory.",
    "Identify any insurance agreement that may apply to a judgment in this action, to the extent You "
    "have not produced it.",
]

# ---------------------------------------------------------------- RFAs
RFA_INTRO = [
    TO_LINE,
    ("PARA", "Under Federal Rules of Civil Procedure 26 and 36, Plaintiff Brendan Ngehsi Newanforbi "
             "requests that Defendant Accurate Background, LLC admit the truth of each matter below, and "
             "the genuineness of the documents attached as Exhibits A and B, within thirty (30) days of "
             "service."),
    ("HEADER", "DEFINITIONS AND INSTRUCTIONS"),
    ("PARA", "1. \"You\" means Defendant Accurate Background, LLC. \"Amazon\" means Amazon.com Services, "
             "LLC and any affiliate that requested or received the Screening Order. \"Screening Order\" "
             "means Accurate reference 496623722. \"Report\" means background report Y94611404."),
    ("PARA", "2. Exhibit A is the consumer report bearing \"updated on 10/14/2026\" that You furnished to "
             "Plaintiff on October 14, 2026. Exhibit B is Your letter to Plaintiff dated October 28, 2026, "
             "with the report enclosed with it, as transmitted by Your counsel on October 28, 2026. "
             "Exhibit B contains Plaintiff's date of birth and is served on counsel only; it is not "
             "filed."),
    ("PARA", "3. Under Rule 36(a)(3), a matter is admitted unless, within thirty days after being served, "
             "You serve a written answer or objection addressed to the matter and signed by You or Your "
             "attorney. Under Rule 36(a)(4), an answer that does not admit must specifically deny the "
             "matter or state in detail why You cannot truthfully admit or deny it; a denial must fairly "
             "respond to the substance of the matter; and You may assert lack of knowledge or information "
             "only if You state that You have made reasonable inquiry and that the information You know or "
             "can readily obtain is insufficient to enable You to admit or deny."),
    ("PARA", "4. Under Rule 37(c)(2), if You fail to admit a matter that Plaintiff later proves, Plaintiff "
             "may move for the reasonable expenses incurred in making that proof."),
    ("HEADER", "REQUESTS FOR ADMISSION"),
]
RFAS = [
    "Admit that Amazon requested screening of Plaintiff under reference 496623722.",
    "Admit that You issued background report Y94611404, ordered on 07/07/2026.",
    "Admit that the Report bearing \"updated on 10/14/2026\" (Exhibit A) contains the alias \"NGWA NFORBI, "
    "NEWANSORBI\" labeled \"Provided by Applicant.\"",
    "Admit that Your October 28, 2026 letter (Exhibit B) states that the updated report removes that "
    "alias.",
    "Admit that the report enclosed with Your October 28, 2026 letter does not contain that alias line.",
    "Admit that the report enclosed with Your October 28, 2026 letter bears \"updated on 10/14/2026.\"",
    "Admit that the Report states the result of search 496623723 as \"NO RECORD FOUND\" with a "
    "completion date of 2026-07-07.",
    "Admit that the Report's entry for search 496623723 does not list the names searched.",
    "Admit that Your file disclosure to Plaintiff identifies Tauxbe Data Inc. as a source for the "
    "National Sex Offender Database Search on the Report.",
    "Admit that a Santa Clara County vendor request on the Screening Order uses first name "
    "\"NEWANSORBI\" and last name \"NGWA.\"",
    "Admit that the raw result for search 496644200 includes case numbers STK-CR-FMISC-2020-0002397, "
    "STK-CR-FMISC-2020-0004747, and STK-CR-FMISC-2025-0004687, each with \"identified_by_name\" false and "
    "\"identified_by_dob\" true.",
    "Admit that the Report states the San Joaquin County result as \"NO RECORD FOUND.\"",
    "Admit that the Santa Clara County component of the Report contains the text \"CURRENTLY ON "
    "PAROLE.\"",
    "Admit that Your October 28, 2026 letter states that Plaintiff's disputes were received on October "
    "15, 2026.",
    "Admit that Your October 28, 2026 letter states that a revised report was forwarded to the employer "
    "who requested it.",
    "Admit that package review 500363362 on the Screening Order is shown as completed on 2026-10-13.",
    "Admit that Santa Clara County search 496644204 is shown as completed on 2026-10-14.",
    "Admit that Exhibit A and Exhibit B are true and correct copies of documents You furnished to "
    "Plaintiff.",
]


def _numbered(label: str, items: list[str], start: int) -> list[tuple[str, str]]:
    out: list[tuple[str, str]] = []
    for i, t in enumerate(items, start):
        out.append(("SUBHEAD", f"{label} NO. {i}:"))
        out.append(("PARA", t))
    return out


def _pos(d: PleadingPaper, doc_titles: str, date: str) -> None:
    d.start_new_page()
    Z._render_body(d, [
        ("HEADER", "PROOF OF SERVICE"),
        ("PARA", "I am the Plaintiff in this action. My address is 1455 Cat Tail Drive, Stockton, CA 95204. "
                 f"On {date}, I served {doc_titles} on the following counsel by email and by first-class "
                 "mail, postage prepaid, deposited with the United States Postal Service at Stockton, "
                 "California, under Fed. R. Civ. P. 5(b)(2)(C) and (E):"),
    ] + [("LIST_ITEM", f"{i}. {t}") for i, t in enumerate(SERVICE_LIST, 1)])
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


def build(out_dir: Path, date: str, exa: Path | None, exb: Path | None) -> list[Path]:
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
        _pos(d, pos_title, date)
        d.save()
        final = out_dir / fname
        w = PdfWriter()
        w.append(str(body))
        if kind == "RFA":
            _exhibit(w, out_dir, "A", "Accurate Background consumer report, reference 496623722, requestor "
                     "\"Amazon HVH,\" bearing \"updated on 10/14/2026,\" furnished to Plaintiff October 14, 2026.",
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
    a = ap.parse_args()
    od = Path(a.out_dir)
    od.mkdir(parents=True, exist_ok=True)
    for p in build(od, a.date, a.exhibit_a, a.exhibit_b):
        print(p, len(PdfReader(str(p)).pages), "pp")


if __name__ == "__main__":
    main()
