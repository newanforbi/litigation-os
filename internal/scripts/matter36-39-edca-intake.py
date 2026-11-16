#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""E.D. Cal. intake packet for Matters 36–39 (Sacramento Division).

Companion filings to the federal complaints in PRs 802 / 804 / 803 / 799:

- JS 44 Civil Cover Sheet (Rev. 03/24) — Title Case names; plaintiff is
  Last Name, First Name
- AO 440 Summons in a Civil Action — one named defendant per suit
- AO 239 Application to Proceed Without Prepaying Fees or Costs (Long Form)

Employment suits. IFP tracks the $0 / no-household answers on the September 8
San Joaquin FW-001s that produced automatic UPS / FedEx / Randstad grants, with
an employment-loss justification at item 11.

Walk-up order (IFP original proceeding):

  1. JS 44
  2. AO 239
  3. AO 440
  4. Complaint (v4 E.D. Cal. pleading; not the San Joaquin verified complaint)

Left blank for the clerk / process server: civil action number, JS 44 office-use
strip, AO 440 clerk date and deputy-clerk signature, and the AO 440 proof-of-
service page except the "summons for" line.

Confirm each California registered-agent listing on the Secretary of State
record the morning of service. Do not serve a store, warehouse, or terminal.

    python3 internal/scripts/matter36-39-edca-intake.py
"""

from __future__ import annotations

import io
import runpy
import shutil
import sys
from pathlib import Path

import pymupdf
from pypdf import PdfReader, PdfWriter

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
sys.path.insert(0, str(SCRIPT_DIR / "lib"))
from short_link import publish_short_link  # noqa: E402
from signature_stamp import (  # noqa: E402
    SIGNATURE_NATIVE_PX,
    SIGNATURE_PATH,
    stamp_on_pdf_line,
)

ROOT = SCRIPT_DIR.parents[1]
DOCS = ROOT / "internal/public/documents"
FORMS = DOCS / "_form-library"

JS44_TEMPLATE = FORMS / "js44-civil-cover-sheet-blank-template.pdf"
AO440_TEMPLATE = FORMS / "ao440-blank-template.pdf"
AO239_TEMPLATE = FORMS / "ao239-blank-template.pdf"

EXEC_DATE = "September 16, 2026"
EXEC_DATE_SHORT = "09/16/2026"
PLAINTIFF_PRINT = "Brendan Ngwa Nforbi"
# JS 44 I.(a) — Last Name, First Name, Title Case (not ALL CAPS).
PLAINTIFF_JS44 = "Ngwa Nforbi, Brendan"
PLAINTIFF_COUNTY = "San Joaquin"
STREET = "1455 Cat Tail Drive"
CITY_LINE = "Stockton, CA 95204"
PHONE = "(209) 801-4442"
EMAIL = "bnn.cdl@gmail.com"
RESIDENCE = "Stockton, California"

# Exact /Opt string from ao440-blank-template.pdf and ao239 Dist.Info.
EDCA_DISTRICT = "         Eastern District of California"

# Pending same-cluster EDCA employment actions (Drozd, Sacramento).
RELATED_JUDGE = "Hon. Dale A. Drozd (Sacramento)"
RELATED_DOCKET = "2:26-cv-02847; 2:26-cv-02881"

# Nature of suit 442 Employment is q4 on_state 37 (JS 44 Rev. 03/24).
NOS_EMPLOYMENT = 37
# II. Basis: q2 on_state 2 = Federal Question; 3 = Diversity.
JURIS_FED_Q = 2
JURIS_DIVERSITY = 3
# V. Origin: 0 = 1 Original Proceeding.
ORIGIN_ORIGINAL = 0
# VII. Jury demand: 0 = Yes.
JURY_YES = 0

CASES = [
    {
        "number": 36,
        "stem": "Ngwa Nforbi v. AT&T Mobility Services LLC",
        "packet_stem": "Ngwa Nforbi v. AT&T",
        "slug": "edca-att",
        "defendant_js44": "AT&T Mobility Services LLC",
        "defendant_block": (
            "AT&T Mobility Services LLC, a Delaware limited liability company"
        ),
        "jurisdiction": JURIS_FED_Q,
        "diversity": False,
        "statute": (
            "15 U.S.C. § 1681b(b)(3)(A) (jurisdiction: 28 U.S.C. §§ 1331, 1367)"
        ),
        "cause": (
            "Employment consumer-report adverse action without a pre-adverse "
            "copy; unauthorized employment use of Penal Code § 290.46 information."
        ),
        "demand": "According to proof",
        "service": [
            "AT&T Mobility Services LLC",
            "c/o CSC-Lawyers Incorporating Service",
            "2710 Gateway Oaks Drive, Suite 150N",
            "Sacramento, CA 95833",
        ],
        "ifp_why": (
            "I am unemployed and cannot pay the $405 filing fee. This is an "
            "employment action. On May 28, 2026 I accepted AT&T's written Lodi "
            "Retail Sales Consultant offer; AT&T rescinded it the same day after "
            "a First Advantage screen. I have no wages from that job."
        ),
    },
    {
        "number": 37,
        "stem": "Ngwa Nforbi v. Home Depot U.S.A., Inc.",
        "packet_stem": "Ngwa Nforbi v. Home Depot",
        "slug": "edca-home-depot",
        "defendant_js44": "Home Depot U.S.A., Inc.",
        "defendant_block": "Home Depot U.S.A., Inc., a Delaware corporation",
        "jurisdiction": JURIS_DIVERSITY,
        "diversity": True,
        "defendant_citizenship": "corp_other_state",
        "statute": (
            "Cal. Penal Code § 290.46(j)(2)(E) (jurisdiction: 28 U.S.C. § 1332)"
        ),
        "cause": (
            "Unauthorized employment use of Megan's Law website information "
            "after an accepted Tracy warehouse / distribution hire."
        ),
        "demand": "Exceeds $75,000",
        "service": [
            "Home Depot U.S.A., Inc.",
            "c/o CSC Lawyers Incorporating Service",
            "2710 Gateway Oaks Drive, Suite 150N",
            "Sacramento, CA 95833",
        ],
        "ifp_why": (
            "I am unemployed and cannot pay the $405 filing fee. This is an "
            "employment action. I accepted a Home Depot Tracy warehouse / "
            "distribution hire, began onboarding, and the employment stopped "
            "after the background screen. I have no wages from that job."
        ),
    },
    {
        "number": 38,
        "stem": "Ngwa Nforbi v. Swift Transportation Co. of Arizona LLC",
        "packet_stem": "Ngwa Nforbi v. Swift",
        "slug": "edca-swift",
        "defendant_js44": "Swift Transportation Co. of Arizona LLC",
        "defendant_block": (
            "Swift Transportation Co. of Arizona LLC, a Delaware limited "
            "liability company"
        ),
        "jurisdiction": JURIS_DIVERSITY,
        "diversity": True,
        "defendant_citizenship": "citizen_other_state",
        "statute": (
            "Cal. Penal Code § 290.46(j)(2)(E); Civ. Code §§ 1786.40, 1786.50 "
            "(jurisdiction: 28 U.S.C. §§ 1332, 1367)"
        ),
        "cause": (
            "Unauthorized employment use of Penal Code § 290.46 information in "
            "a Class A Driver denial; ICRAA adverse-action advice; UCL."
        ),
        "demand": "Exceeds $75,000",
        "service": [
            "Swift Transportation Co. of Arizona LLC",
            "c/o National Registered Agents, Inc.",
            "330 N Brand Blvd, Suite 700",
            "Glendale, CA 91203",
        ],
        "ifp_why": (
            "I am unemployed and cannot pay the $405 filing fee. This is an "
            "employment action. Swift denied my Class A Driver application on "
            "October 5, 2023 after consumer-report screening. I have no wages "
            "from that job."
        ),
    },
    {
        "number": 39,
        "stem": "Ngwa Nforbi v. Best Buy Co., Inc.",
        "packet_stem": "Ngwa Nforbi v. Best Buy",
        "slug": "edca-best-buy",
        "defendant_js44": "Best Buy Co., Inc.",
        "defendant_block": "Best Buy Co., Inc., a Minnesota corporation",
        "jurisdiction": JURIS_DIVERSITY,
        "diversity": True,
        "defendant_citizenship": "corp_other_state",
        "statute": (
            "Cal. Penal Code § 290.46(j)(2)(E) (jurisdiction: 28 U.S.C. § 1332)"
        ),
        "cause": (
            "Unauthorized employment use of Megan's Law website information "
            "after an accepted Tracy warehouse hire at $22.60 per hour."
        ),
        "demand": "Exceeds $75,000",
        "service": [
            "Best Buy Co., Inc.",
            "c/o C T Corporation System",
            "330 N Brand Blvd, Suite 700",
            "Glendale, CA 91203",
        ],
        "ifp_why": (
            "I am unemployed and cannot pay the $405 filing fee. This is an "
            "employment action. On October 17, 2023 I accepted Best Buy's "
            "Tracy warehouse offer at $22.60 per hour; Best Buy then ceased "
            "communication after screening. I have no wages from that job."
        ),
    },
]


def _leaf(name: str) -> str:
    return (name or "").split(".")[-1]


def _set_text(widget, text: str) -> None:
    widget.field_value = text
    widget.update()


def _turn_on(widget) -> None:
    on = widget.on_state()
    if on is None:
        return
    widget.field_value = on
    widget.update()


def _check_radio(page: pymupdf.Page, leaf: str, on_state) -> None:
    want = str(on_state)
    for w in page.widgets() or []:
        if _leaf(w.field_name or "") == leaf and str(w.on_state()) == want:
            _turn_on(w)
            return
    raise SystemExit(f"Radio {leaf} on_state={on_state!r} not found")


def _check_box(page: pymupdf.Page, leaf: str) -> None:
    for w in page.widgets() or []:
        if _leaf(w.field_name or "") == leaf:
            _turn_on(w)
            return
    raise SystemExit(f"Checkbox {leaf} not found")


def _set_named(page: pymupdf.Page, leaf: str, text: str) -> None:
    for w in page.widgets() or []:
        if _leaf(w.field_name or "") == leaf and w.field_type_string == "Text":
            _set_text(w, text)
            return
    raise SystemExit(f"Text field {leaf} not found")


def _widget(page: pymupdf.Page, leaf: str):
    for w in page.widgets() or []:
        if _leaf(w.field_name or "") == leaf:
            return w
    return None


def _draw_lines(
    page: pymupdf.Page,
    rect: pymupdf.Rect,
    lines: list[str],
    fontsize: float = 7.0,
) -> None:
    page.draw_rect(rect, color=(1, 1, 1), fill=(1, 1, 1), width=0)
    y = rect.y0 + fontsize + 1.2
    for line in lines:
        page.insert_text(
            (rect.x0 + 1.0, y),
            line,
            fontsize=fontsize,
            fontname="helv",
            color=(0, 0, 0),
        )
        y += fontsize + 1.6


def _set_combo(page: pymupdf.Page, text: str) -> None:
    for w in page.widgets() or []:
        if w.field_type_string == "ComboBox":
            _set_text(w, text)
            return
    raise SystemExit("ComboBox not found")


def _stamp_js44_signature(page: pymupdf.Page) -> None:
    """Sit a native-aspect mark on the signature rule, right of the caption.

    JS 44 sig widget is Rect(219, 726.58, 594.50, 737.38). The printed
    "SIGNATURE OF ATTORNEY OF RECORD" occupies x=219.6–350.3, y=715.2–724.6.
    stamp_on_pdf_line's 1.15 height scale plus an 85-pt width still pokes
    the loops into that caption. The 5544×820 photo-loops plate needed
    62 pt to keep the top at ~y=728; the live 445×106 stamp (aspect
    ≈ 0.238) needs ~38.5 pt for the same clearance.
    """
    sw, sh = SIGNATURE_NATIVE_PX
    width = 38.5
    height = width * (sh / sw)
    x0 = 358.0
    y_line = 737.2
    rect = pymupdf.Rect(x0, y_line - height, x0 + width, y_line)
    page.insert_image(rect, filename=SIGNATURE_PATH, keep_proportion=False)


def _save(doc: pymupdf.Document, path: Path) -> None:
    tmp = path.with_suffix(path.suffix + ".tmp")
    doc.save(str(tmp), garbage=4, deflate=True)
    doc.close()
    tmp.replace(path)


def _out_dir(number: int) -> Path:
    path = DOCS / f"matter-{number}" / "edca"
    path.mkdir(parents=True, exist_ok=True)
    return path


def build_js44(case: dict, out: Path) -> Path:
    shutil.copy2(JS44_TEMPLATE, out)
    doc = pymupdf.open(str(out))
    page = doc[0]
    _set_named(page, "plaintiffs[0]", PLAINTIFF_JS44)
    _set_named(page, "defendants[0]", case["defendant_js44"])
    _set_named(page, "plCty[0]", PLAINTIFF_COUNTY)
    atty = _widget(page, "attorneysPL[0]")
    if atty is None:
        raise SystemExit("attorneysPL[0] not found")
    _set_text(atty, "")
    _draw_lines(
        page,
        pymupdf.Rect(atty.rect),
        [
            f"{PLAINTIFF_PRINT}, Plaintiff, In Propria Persona",
            f"{STREET}, {CITY_LINE}",
            f"Tel: {PHONE}; E-mail: {EMAIL}",
        ],
        fontsize=6.6,
    )
    _check_radio(page, "q2[0]", case["jurisdiction"])
    if case["diversity"]:
        _check_box(page, "S3P1[0]")
        if case["defendant_citizenship"] == "corp_other_state":
            _check_box(page, "S3D5[0]")
        else:
            _check_box(page, "S3D2[0]")
    _check_radio(page, "q4[0]", NOS_EMPLOYMENT)
    _check_radio(page, "q5[0]", ORIGIN_ORIGINAL)
    _set_named(page, "S6stat[0]", case["statute"])
    _set_named(page, "S6cause[0]", case["cause"])
    _set_named(page, "S7demand[0]", case["demand"])
    _check_radio(page, "jury[0]", JURY_YES)
    _set_named(page, "S8judge[0]", RELATED_JUDGE)
    _set_named(page, "S8docket[0]", RELATED_DOCKET)
    _set_named(page, "date[0]", EXEC_DATE_SHORT)
    _stamp_js44_signature(page)
    _save(doc, out)
    print(f"Wrote {out}")
    return out


def build_ao440(case: dict, out: Path) -> Path:
    shutil.copy2(AO440_TEMPLATE, out)
    doc = pymupdf.open(str(out))
    page0, page1 = doc[0], doc[1]
    _set_combo(page0, EDCA_DISTRICT)
    _set_named(page0, "Plaintiff", PLAINTIFF_PRINT)
    _set_named(page0, "Defendant", case["defendant_block"])
    _set_named(page0, "Defendant address", "\n".join(case["service"]))
    _set_named(
        page0,
        "Plaintiff address",
        "\n".join(
            [
                PLAINTIFF_PRINT,
                "Plaintiff, In Propria Persona",
                STREET,
                CITY_LINE,
                f"Telephone: {PHONE} — E-mail: {EMAIL}",
            ]
        ),
    )
    _set_named(page1, "Defendant2", case["defendant_js44"])
    _save(doc, out)
    print(f"Wrote {out}")
    return out


def _ifp_fill_grid(doc: pymupdf.Document, case: dict) -> None:
    """Fill AO 239: named specials first, then leftover blanks with 0 / N/A."""
    special_text = {
        "Plaintiff": PLAINTIFF_PRINT,
        "Defendant": case["defendant_js44"],
        "Employment History_Employer_Name": "Unemployed",
        "Employment History_Employer_Address": "N/A",
        "Employment History_Employment_Dates": "N/A",
        "Employment History_Monthly_Salary": "0",
        "Employment History_Employer_Name_2": "N/A",
        "Employment History_Employer_Address_2": "N/A",
        "Employment History_Employment_Dates_2": "N/A",
        "Employment History_Monthly_Salary_2": "0",
        "Spouse_Employment History_Employer_Name": "N/A",
        "Spouse Employment History_Employer_Address": "N/A",
        "Spouse Employment History_Employment_Dates": "N/A",
        "Spouse Employment History_Monthly_Salary": "0",
        "Spouse_Employment History_Employer_Name_2": "N/A",
        "Spouse Employment History_Employer_Address_2": "N/A",
        "Spouse Employment History_Employment_Dates_2": "N/A",
        "Spouse Employment History_Monthly_Salary_2": "0",
        "Spouse_Employment History_Employer_Name_3": "N/A",
        "Spouse Employment History_Employer_Address_3": "N/A",
        "Spouse Employment History_Employment_Dates_3": "N/A",
        "Spouse Employment History_Monthly_Salary_3": "0",
        "Total_Cash_You_Both_Have": "0",
        "Other_Expense": "N/A",
        "Total Estimate_Monthly_Expense_You": "0",
        "Total Estimate_Monthly_Expense_Spouse": "0",
        "Have_You_Paid_Attorney": "N/A",
        "Why_you_can't_pay": case["ifp_why"],
        "City_State_of_residence": RESIDENCE,
        "Phone_Number": PHONE,
        "Age": "N/A",
        "Years_of_School": "N/A",
        "Social Security": "N/A",
    }
    skip_names = {"Case_Num", "Civil action number"}
    for page in doc:
        for w in page.widgets() or []:
            if w.field_type_string != "Text":
                continue
            name = w.field_name or ""
            leaf = _leaf(name)
            if leaf in skip_names or name in skip_names:
                continue
            # Signed / Date widgets on page 0 — stamp and date handle these.
            if page.number == 0 and abs(w.rect.y0 - 395.0) < 6:
                continue
            if name in special_text:
                _set_text(w, special_text[name])
                continue
            if leaf in special_text:
                _set_text(w, special_text[leaf])
                continue
            current = (w.field_value or "").strip()
            if current and current not in ("0", "0.00"):
                continue
            # Amount columns sit to the right of ~250; name/specify boxes sit left.
            _set_text(w, "0" if w.rect.x0 >= 250 else "N/A")


def _ifp_checkboxes(doc: pymupdf.Document) -> None:
    """No home, so taxes/insurance = No. Q9 and Q10 = No."""
    wanted = {
        ("Check Box", "No"),
        ("Check Box2", "No"),
        ("Check Box3", "No"),
        ("Check Box4", "No"),
    }
    for page in doc:
        for w in page.widgets() or []:
            if w.field_type_string != "CheckBox":
                continue
            key = (w.field_name or "", w.on_state())
            if key in wanted:
                _turn_on(w)


def build_ao239(case: dict, out: Path) -> Path:
    shutil.copy2(AO239_TEMPLATE, out)
    doc = pymupdf.open(str(out))
    _set_combo(doc[0], EDCA_DISTRICT)
    _ifp_fill_grid(doc, case)
    _ifp_checkboxes(doc)
    for w in doc[0].widgets() or []:
        if w.field_type_string != "Text":
            continue
        if abs(w.rect.y0 - 395.0) < 4 and w.rect.x0 < 200:
            _set_text(w, "")  # ink stamp is the signature
        elif abs(w.rect.y0 - 395.0) < 4 and w.rect.x0 > 300:
            _set_text(w, EXEC_DATE)
    stamp_on_pdf_line(doc[0], 88.0, 230.0, 412.0, whiteout=True)
    last = doc[-1]
    for w in list(last.widgets() or []):
        leaf = _leaf(w.field_name or "")
        if leaf in {"Print1", "SaveAs", "AttachFile", "Reset"}:
            last.delete_widget(w)
    last.draw_rect(
        pymupdf.Rect(20, 478, 592, 505), color=(1, 1, 1), fill=(1, 1, 1), width=0
    )
    _save(doc, out)
    print(f"Wrote {out}")
    return out


def flatten_packet(sources: list[Path], out: Path) -> Path:
    import pypdfium2 as pdfium

    writer = PdfWriter()
    for source in sources:
        pdf = pdfium.PdfDocument(str(source))
        try:
            pdf.init_forms()
            for page in pdf:
                page.flatten()
            buffer = io.BytesIO()
            pdf.save(buffer)
            buffer.seek(0)
            writer.append(PdfReader(buffer))
        except RuntimeError:
            # Reportlab pleadings have no AcroForm; append as-is.
            writer.append(str(source))
    with open(out, "wb") as fh:
        writer.write(fh)
    print(f"Wrote {out} ({len(writer.pages)} pages)")
    return out


def main() -> None:
    for template in (JS44_TEMPLATE, AO440_TEMPLATE, AO239_TEMPLATE):
        if not template.is_file():
            raise SystemExit(f"Missing template: {template}")
    if not Path(SIGNATURE_PATH).is_file():
        raise SystemExit(f"Missing signature: {SIGNATURE_PATH}")

    complaints = runpy.run_path(
        str(SCRIPT_DIR / "matter36-39-edca-complaints.py")
    )

    for case in CASES:
        out_dir = _out_dir(case["number"])
        date = "Sep 16 2026"
        js44 = build_js44(
            case,
            out_dir
            / f"JS 44 Civil Cover Sheet - {case['stem']} (E.D. Cal.) ({date}).pdf",
        )
        ifp = build_ao239(
            case,
            out_dir
            / f"AO 239 IFP Application - {case['stem']} (E.D. Cal.) ({date}).pdf",
        )
        summons = build_ao440(
            case,
            out_dir
            / f"AO 440 Summons - {case['defendant_js44']} (E.D. Cal.) ({date}).pdf",
        )
        complaint = complaints["build_complaint"](case["number"], out_dir)
        packet = flatten_packet(
            [js44, ifp, summons, complaint],
            out_dir
            / (
                "E.D. Cal. Intake Packet (print copy) - "
                f"{case['packet_stem']} ({date}).pdf"
            ),
        )
        short = publish_short_link(packet, case["slug"])
        print(f"  short-link /{case['slug']} -> {short.name}")


if __name__ == "__main__":
    main()
