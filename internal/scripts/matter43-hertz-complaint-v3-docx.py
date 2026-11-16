#!/usr/bin/env python3
"""Word copy of the unsigned Hertz/HireRight verified complaint.

Same body as matter43-hertz-complaint-v3.py. For Print → Save as PDF
when a PDF viewer or Google Docs re-export blanks pages. Signature
lines are blank.

Run: python3 internal/scripts/matter43-hertz-complaint-v3-docx.py
"""
from __future__ import annotations

import json
from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING, WD_TAB_ALIGNMENT
from docx.oxml.ns import qn
from docx.shared import Inches, Pt

SCRIPTS = Path(__file__).resolve().parent
ROOT = SCRIPTS.parents[1]
BODY_PATH = SCRIPTS / "matter43-hertz-complaint-v3-body.json"
OUT = (
    ROOT
    / "documents/matter-43/ndcal/to-file"
    / "Verified Complaint - Ngwa Nforbi v. The Hertz Corporation and HireRight, LLC (unsigned).docx"
)

CENTERED_TITLES = {
    "Failure to Follow Reasonable Procedures to Assure Maximum Possible Accuracy",
    "Use of a Non-Conviction Arrest Record in Hiring",
    "Unlawful Non-Compete Condition; Declaratory and Injunctive Relief",
    "Nonstandalone Investigative Consumer Report Disclosure",
    "Unlawful Use of Megan's Law Information for Employment",
}


def _set_run(run, *, size=12, bold=False, italic=False, name="Times New Roman"):
    run.font.name = name
    run._element.rPr.rFonts.set(qn("w:eastAsia"), name)
    run.font.size = Pt(size)
    run.bold = bold
    run.italic = italic


def _p(doc, text="", *, bold=False, italic=False, center=False, right=False,
       first_indent=None, space_after=0, size=12):
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.line_spacing_rule = WD_LINE_SPACING.DOUBLE
    pf.space_before = Pt(0)
    pf.space_after = Pt(space_after)
    if center:
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    elif right:
        p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    if first_indent is not None:
        pf.first_line_indent = Inches(first_indent)
    if text:
        run = p.add_run(text)
        _set_run(run, size=size, bold=bold, italic=italic)
    return p


def main() -> None:
    body = json.loads(BODY_PATH.read_text())
    doc = Document()
    for section in doc.sections:
        section.page_width = Inches(8.5)
        section.page_height = Inches(11)
        section.left_margin = Inches(1.25)
        section.right_margin = Inches(1)
        section.top_margin = Inches(1)
        section.bottom_margin = Inches(1)
        section.different_first_page_header_footer = False
        footer = section.footer
        footer.is_linked_to_previous = False
        fp = footer.paragraphs[0]
        fp.alignment = WD_ALIGN_PARAGRAPH.LEFT
        run = fp.add_run(
            "Verified Complaint — Ngwa Nforbi v. The Hertz Corporation and HireRight, LLC"
        )
        _set_run(run, size=9)
        fp.add_run("\t")
        # PAGE field
        from docx.oxml import OxmlElement

        def add_page_field(paragraph):
            run = paragraph.add_run("Page ")
            _set_run(run, size=9)
            fld1 = OxmlElement("w:fldChar")
            fld1.set(qn("w:fldCharType"), "begin")
            instr = OxmlElement("w:instrText")
            instr.set(qn("xml:space"), "preserve")
            instr.text = " PAGE "
            fld2 = OxmlElement("w:fldChar")
            fld2.set(qn("w:fldCharType"), "end")
            r = paragraph.add_run()
            _set_run(r, size=9)
            r._element.append(fld1)
            r2 = paragraph.add_run()
            _set_run(r2, size=9)
            r2._element.append(instr)
            r3 = paragraph.add_run()
            _set_run(r3, size=9)
            r3._element.append(fld2)
            run = paragraph.add_run(" of ")
            _set_run(run, size=9)
            fld1 = OxmlElement("w:fldChar")
            fld1.set(qn("w:fldCharType"), "begin")
            instr = OxmlElement("w:instrText")
            instr.set(qn("xml:space"), "preserve")
            instr.text = " NUMPAGES "
            fld2 = OxmlElement("w:fldChar")
            fld2.set(qn("w:fldCharType"), "end")
            r = paragraph.add_run()
            _set_run(r, size=9)
            r._element.append(fld1)
            r2 = paragraph.add_run()
            _set_run(r2, size=9)
            r2._element.append(instr)
            r3 = paragraph.add_run()
            _set_run(r3, size=9)
            r3._element.append(fld2)

        tab_stops = fp.paragraph_format.tab_stops
        tab_stops.add_tab_stop(Inches(6.25), WD_TAB_ALIGNMENT.RIGHT)
        add_page_field(fp)

    _p(doc, "BRENDAN NGWA NFORBI", bold=True)
    _p(doc, "Plaintiff, In Propria Persona")
    _p(doc, "1455 Cat Tail Drive")
    _p(doc, "Stockton, California 95204")
    _p(doc, "Telephone: (209) 801-4442")
    _p(doc, "Email: bnn.cdl@gmail.com")
    _p(doc)
    _p(doc, "UNITED STATES DISTRICT COURT", bold=True, center=True)
    _p(doc, "NORTHERN DISTRICT OF CALIFORNIA", bold=True, center=True)
    _p(doc, "SAN JOSE DIVISION", bold=True, center=True)
    _p(doc)

    table = doc.add_table(rows=1, cols=2)
    table.autofit = True
    left, right = table.rows[0].cells
    left_lines = [
        ("BRENDAN NGWA NFORBI,", True),
        ("", False),
        ("               Plaintiff,", False),
        ("", False),
        ("          v.", False),
        ("", False),
        ("THE HERTZ CORPORATION,", True),
        ("a Delaware corporation; and", False),
        ("HIRERIGHT, LLC,", True),
        ("a Delaware limited liability company,", False),
        ("", False),
        ("               Defendants.", False),
    ]
    right_lines = [
        ("Case No. __________________", True),
        ("", False),
        ("VERIFIED COMPLAINT FOR", True),
        ("DAMAGES, CIVIL PENALTY,", True),
        ("DECLARATORY AND", True),
        ("INJUNCTIVE RELIEF", True),
        ("", False),
        ("(1) 15 U.S.C. § 1681e(b) (FCRA);", False),
        ("(2) Cal. Penal Code § 290.46(j);", False),
        ("(3) Cal. Civ. Code §§ 1786.16,", False),
        ("     1786.50 (ICRAA);", False),
        ("(4) Cal. Labor Code § 432.7;", False),
        ("(5) Cal. Bus. & Prof. Code", False),
        ("     §§ 16600–16600.5", False),
        ("", False),
        ("DEMAND FOR JURY TRIAL", True),
    ]
    for cell, lines in ((left, left_lines), (right, right_lines)):
        cell.text = ""
        for i, (text, bold) in enumerate(lines):
            p = cell.paragraphs[0] if i == 0 else cell.add_paragraph()
            p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.SINGLE
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)
            run = p.add_run(text)
            _set_run(run, size=12, bold=bold)

    _p(doc)
    i = 0
    while i < len(body):
        item = body[i]
        kind = "H" if item["text"] in CENTERED_TITLES else item["kind"]
        if kind == "DATE":
            _p(doc, "Dated: _______________")
            _p(doc, "Respectfully submitted,", right=True)
            _p(doc)
            _p(doc, "___________________________________", right=True)
            _p(doc, "BRENDAN NGWA NFORBI", bold=True, right=True)
            _p(doc, "Plaintiff, In Propria Persona", right=True)
            _p(doc)
            _p(doc, "VERIFICATION", bold=True, center=True)
            i += 1
            continue
        if kind == "H":
            run = [item["text"]]
            i += 1
            while i < len(body) and (
                ("H" if body[i]["text"] in CENTERED_TITLES else body[i]["kind"]) == "H"
            ):
                run.append(body[i]["text"])
                i += 1
            _p(doc)
            for line in run:
                _p(doc, line, bold=True, center=True)
            continue
        if kind == "S":
            _p(doc)
            _p(doc, item["text"], bold=True)
            i += 1
            continue
        first = 0.5 if item["text"][:3].split(".")[0].isdigit() or item["text"].startswith("Plaintiff ") else 0.5
        _p(doc, item["text"], first_indent=first)
        if item["text"].startswith("Executed on"):
            _p(doc, "___________________________________", right=True)
            _p(doc, "BRENDAN NGWA NFORBI", bold=True, right=True)
        i += 1

    OUT.parent.mkdir(parents=True, exist_ok=True)
    doc.save(str(OUT))
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
