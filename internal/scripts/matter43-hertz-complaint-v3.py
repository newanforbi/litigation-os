#!/usr/bin/env python3
"""Verified Complaint v3 (unsigned) — Ngwa Nforbi v. The Hertz Corporation and HireRight, LLC.

Renders the five-count working copy, with the November 16, 2026 text
fixes, on classic double-rule pleading paper for the Northern District
of California, San Jose Division. Signature lines are left blank so
Plaintiff can execute the filing copy.

Civil L.R. 3-4 (current through the October 2, 2026 rules):
  * 8.5 x 11 paper, numbered lines, text on one side. 3-4(c)(1).
  * Double-spaced, no more than 28 lines per page, except counsel
    identification, the title of the case, footnotes, and quotations.
    3-4(c)(2).
  * Times face at 12 point. 3-4(c)(2)(A).
  * Court title begins on line 8. 3-4(a)(3).
  * Footer is the paper's title. No case number until the Court assigns
    one. 3-4(c)(3).

Not an npm script. Run: python3 internal/scripts/matter43-hertz-complaint-v3.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

from reportlab.lib.units import inch

SCRIPTS = Path(__file__).resolve().parent
ROOT = SCRIPTS.parents[1]
sys.path.insert(0, str(SCRIPTS))
sys.path.insert(0, str(SCRIPTS / "lib"))

import pleading_paper as pp

pp.CONTENT_LEFT = 1.82 * inch
pp.CONTENT_WIDTH = pp.CONTENT_RIGHT - pp.CONTENT_LEFT

from pleading_paper import (  # noqa: E402
    CONTENT_RIGHT,
    FONT_SIZE,
    FOOTER_RULE_Y,
    LINE_SPACING,
    NUM_LINES,
    TEXT_END_Y,
    TEXT_START_Y,
    PleadingPaper,
)

BODY_PATH = SCRIPTS / "matter43-hertz-complaint-v3-body.json"
OUT = (
    ROOT
    / "documents/matter-43/ndcal/to-file"
    / "Verified Complaint - Ngwa Nforbi v. The Hertz Corporation and HireRight, LLC (unsigned).pdf"
)
FOOTER = "Verified Complaint — Ngwa Nforbi v. The Hertz Corporation and HireRight, LLC"
SIG_LINE = "___________________________________"
SIG_OFFSET = 20

CENTERED_TITLES = {
    "Failure to Follow Reasonable Procedures to Assure Maximum Possible Accuracy",
    "Use of a Non-Conviction Arrest Record in Hiring",
    "Unlawful Non-Compete Condition; Declaratory and Injunctive Relief",
    "Nonstandalone Investigative Consumer Report Disclosure",
    "Unlawful Use of Megan's Law Information for Employment",
}


class ClassicPleading(PleadingPaper):
    """Double-rule letter paper: numbers in the channel, footer like the
    classic Staples paper (title left, page X of Y right). No right rule.
    """

    def __init__(self, filename, doc_title_footer="", page_total=0):
        self.page_total = page_total
        super().__init__(filename, doc_title_footer=doc_title_footer)

    def _draw_page_frame(self):
        c = self.c
        c.setStrokeColorRGB(0, 0, 0)
        rule_outer = 86
        rule_inner = 100
        c.setLineWidth(1.0)
        c.line(rule_outer, pp.PAGE_H, rule_outer, 0)
        c.setLineWidth(0.6)
        c.line(rule_inner, pp.PAGE_H, rule_inner, 0)
        c.setFont("Helvetica", 10)
        num_x = pp.CONTENT_LEFT - 8
        for i in range(NUM_LINES):
            y = TEXT_START_Y - i * LINE_SPACING
            c.drawRightString(num_x, y, str(i + 1))
        c.setLineWidth(0.6)
        c.line(pp.CONTENT_LEFT, FOOTER_RULE_Y, CONTENT_RIGHT, FOOTER_RULE_Y)
        page = (
            f"Page {self.page_num} of {self.page_total}"
            if self.page_total
            else f"Page {self.page_num}"
        )
        y = FOOTER_RULE_Y - 13
        c.setFont("Times-Roman", 9)
        page_w = c.stringWidth(page, "Times-Roman", 9)
        avail = CONTENT_RIGHT - pp.CONTENT_LEFT - page_w - 14
        size = 9
        title = self.doc_title_footer
        while size > 7 and c.stringWidth(title, "Times-Roman", size) > avail:
            size -= 0.5
        c.setFont("Times-Roman", size)
        c.drawString(pp.CONTENT_LEFT, y, title)
        c.setFont("Times-Roman", 9)
        c.drawRightString(CONTENT_RIGHT, y, page)

    def draw_caption_block(self, left, right, caption_size=12, tight_lh=15, boxed=True):
        c = self.c
        box_left_x = pp.CONTENT_LEFT
        box_right_x = pp.CONTENT_LEFT + pp.CONTENT_WIDTH * 0.50
        right_col_x = box_right_x + 10
        start_line = self.current_line
        self._ensure_line()
        first_y = self._line_y(self.current_line)
        box_top = first_y + 14
        left_x_pad = 6
        rows = max(len(left), len(right))
        for i in range(rows):
            y = first_y - i * tight_lh
            if y < TEXT_END_Y + 2:
                break
            if i < len(left):
                self._caption_string(
                    left[i], box_left_x + left_x_pad, y, caption_size, box_right_x - box_left_x - 14
                )
            if i < len(right):
                self._caption_string(
                    right[i], right_col_x, y, caption_size, CONTENT_RIGHT - right_col_x - 6
                )
        if boxed:
            last_row_y = first_y - (rows - 1) * tight_lh
            box_bottom = last_row_y - 8
            c.setStrokeColorRGB(0, 0, 0)
            c.setLineWidth(0.75)
            c.line(box_left_x, box_top, box_right_x, box_top)
            c.line(box_left_x, box_bottom, box_right_x, box_bottom)
            c.line(box_right_x, box_top, box_right_x, box_bottom)
        consumed_height = (rows - 1) * tight_lh + 14 + 8
        lines_consumed = int(consumed_height / LINE_SPACING) + 1
        self.current_line = start_line + lines_consumed

    def _caption_string(self, row, x, y, size, avail):
        text, bold, italic = row
        if not text:
            return
        if bold and italic:
            fn = "Times-BoldItalic"
        elif bold:
            fn = "Times-Bold"
        elif italic:
            fn = "Times-Italic"
        else:
            fn = "Times-Roman"
        if self.c.stringWidth(text, fn, size) > avail:
            raise SystemExit(f"Caption line exceeds 12-point width: {text!r}")
        self.c.setFont(fn, size)
        self.c.drawString(x, y, text)


def _center_bold(d: ClassicPleading, text: str) -> None:
    avail = pp.CONTENT_WIDTH - 12
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if d.c.stringWidth(trial, "Times-Bold", FONT_SIZE) <= avail:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    for line in lines:
        d.write_line(line, bold=True, center=True)


def _unsigned_block(d: ClassicPleading, respectfully: bool) -> None:
    """Blank signature lines. Plaintiff executes the filing original."""
    d.ensure_space(6)
    if respectfully:
        d.write_line("Respectfully submitted,", right=True, right_margin_offset=SIG_OFFSET)
        d.blank_line()
    d.write_line(SIG_LINE, right=True, right_margin_offset=SIG_OFFSET)
    d.write_line("BRENDAN NGWA NFORBI", bold=True, right=True, right_margin_offset=SIG_OFFSET)
    if respectfully:
        d.write_line(
            "Plaintiff, In Propria Persona",
            right=True,
            right_margin_offset=SIG_OFFSET,
        )


def _kind(item: dict) -> str:
    if item["text"] in CENTERED_TITLES:
        return "H"
    return item["kind"]


def _build(path: Path, page_total: int) -> None:
    body = json.loads(BODY_PATH.read_text())
    d = ClassicPleading(str(path), doc_title_footer=FOOTER, page_total=page_total)
    # Lines 1–6 counsel identification. Line 7 blank.
    # Court title commences on line 8. Civil L.R. 3-4(a)(3).
    d.write_line("BRENDAN NGWA NFORBI", bold=True)
    d.write_line("Plaintiff, In Propria Persona")
    d.write_line("1455 Cat Tail Drive")
    d.write_line("Stockton, California 95204")
    d.write_line("Telephone: (209) 801-4442")
    d.write_line("Email: bnn.cdl@gmail.com")
    d.blank_line()
    d.write_line("UNITED STATES DISTRICT COURT", bold=True, center=True)
    d.write_line("NORTHERN DISTRICT OF CALIFORNIA", bold=True, center=True)
    d.write_line("SAN JOSE DIVISION", bold=True, center=True)
    d.blank_line()
    d.draw_caption_block(
        [
            ("BRENDAN NGWA NFORBI,", True, False),
            ("", False, False),
            ("               Plaintiff,", False, False),
            ("", False, False),
            ("          v.", False, False),
            ("", False, False),
            ("THE HERTZ CORPORATION,", True, False),
            ("a Delaware corporation; and", False, False),
            ("HIRERIGHT, LLC,", True, False),
            ("a Delaware limited liability company,", False, False),
            ("", False, False),
            ("               Defendants.", False, False),
        ],
        [
            ("Case No. __________________", True, False),
            ("", False, False),
            ("VERIFIED COMPLAINT FOR", True, False),
            ("DAMAGES, CIVIL PENALTY,", True, False),
            ("DECLARATORY AND", True, False),
            ("INJUNCTIVE RELIEF", True, False),
            ("", False, False),
            ("(1) 15 U.S.C. § 1681e(b) (FCRA);", False, False),
            ("(2) Cal. Penal Code § 290.46(j);", False, False),
            ("(3) Cal. Civ. Code §§ 1786.16,", False, False),
            ("     1786.50 (ICRAA);", False, False),
            ("(4) Cal. Labor Code § 432.7;", False, False),
            ("(5) Cal. Bus. & Prof. Code", False, False),
            ("     §§ 16600–16600.5", False, False),
            ("", False, False),
            ("DEMAND FOR JURY TRIAL", True, False),
        ],
        caption_size=12,
        tight_lh=14,
    )
    d.blank_line()

    i = 0
    while i < len(body):
        item = body[i]
        kind = _kind(item)
        if kind == "DATE":
            d.blank_line()
            d.write_line("Dated: _______________")
            _unsigned_block(d, respectfully=True)
            d.ensure_space(5)
            d.blank_line()
            _center_bold(d, "VERIFICATION")
            i += 1
            continue
        if kind == "H":
            run = [item["text"]]
            i += 1
            while i < len(body) and _kind(body[i]) == "H":
                run.append(body[i]["text"])
                i += 1
            d.ensure_space(len(run) + 2)
            d.blank_line()
            for line in run:
                _center_bold(d, line)
            continue
        if kind == "S":
            d.ensure_space(3)
            d.blank_line()
            d.write_line(item["text"], bold=True)
            i += 1
            continue
        d.write_wrapped(item["text"], first_indent=36)
        if item["text"].startswith("Executed on"):
            _unsigned_block(d, respectfully=False)
        i += 1
    d.c.setTitle(
        "Verified Complaint — Ngwa Nforbi v. The Hertz Corporation and HireRight, LLC (unsigned)"
    )
    d.c.setAuthor("Brendan Ngwa Nforbi")
    d.save()


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    _build(OUT, page_total=0)
    import pymupdf

    total = pymupdf.open(OUT).page_count
    _build(OUT, page_total=total)
    total2 = pymupdf.open(OUT).page_count
    if total2 != total:
        raise SystemExit(f"Page count changed between passes: {total} then {total2}")
    print(f"Wrote {OUT} ({total2} pages)")


if __name__ == "__main__":
    main()
