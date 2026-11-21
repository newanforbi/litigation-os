# ==========================================================
# N.D. Cal. pleading-paper style ("Agiliti style").
#
# Matches the format of the Nov. 18, 2026 Agiliti verified complaint
# (N.D. Cal.): Liberation Serif 12 pt throughout (body, line numbers,
# footer), a plain attorney block ending "Plaintiff, In Pro Per", a
# two-line bold court title, an open-box caption (top rule over the left
# cell plus a center rule), centered bold headings, hanging-indent list
# items, and a right-aligned sign-off with the name in bold.
#
# Built on the shared engine in pleading_paper.py. The geometry (rules,
# margins, 28 lines at 24 pt) is unchanged; only the styling differs.
#
#   from pleading_paper_ndcal import NDCalPaper
#   d = NDCalPaper(out, footer="TITLE -- NFORBI v. MEZA-GONZALEZ, et al.")
#   d.header(party_block=True)
#   d.caption(left_name, left_defendants, right_rows)
#   d.heading("INTRODUCTION"); d.para("..."); d.item("1. ...")
#   d.sign_off("November 24, 2026")
#   d.save()
# ==========================================================
from __future__ import annotations

import os

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from pleading_paper import (  # noqa: F401
    CONTENT_LEFT, CONTENT_RIGHT, CONTENT_WIDTH, FONT_SIZE, LINE_NUM_X,
    LINE_SPACING, NUM_LINES, PAGE_H, TEXT_END_Y, TEXT_START_Y,
    VERT_LINE_LEFT, VERT_LINE_RIGHT, PleadingPaper,
)

_FONT_DIR = "/usr/share/fonts/truetype/liberation"
_FACES = {
    "Times-Roman": "LiberationSerif-Regular.ttf",
    "Times-Bold": "LiberationSerif-Bold.ttf",
    "Times-Italic": "LiberationSerif-Italic.ttf",
    "Times-BoldItalic": "LiberationSerif-BoldItalic.ttf",
}
_registered = False


def _register_fonts() -> None:
    """Map the engine's Times face names to embedded Liberation Serif, so
    every write_line / write_wrapped call renders in the Agiliti face."""
    global _registered
    if _registered:
        return
    for name, fn in _FACES.items():
        path = os.path.join(_FONT_DIR, fn)
        if os.path.isfile(path):
            pdfmetrics.registerFont(TTFont(name, path))
    _registered = True


SERIF = "Times-Roman"
SERIF_B = "Times-Bold"

FOOTER_RULE_Y = 40
FOOTER_PAGE_Y = 30
FOOTER_TITLE_Y = 18

PARTY_BLOCK = [
    "BRENDAN NGWA NFORBI",
    "Plaintiff, In Pro Per",
    "1455 Cat Tail Drive",
    "Stockton, CA 95204",
    "Telephone: (209) 801-4442",
    "E-mail: bnn.cdl@gmail.com",
]
SIGNOFF_NAME = "BRENDAN NGWA NFORBI"
SIGNOFF_ROLE = "Plaintiff, In Pro Per"
SIG_LINE = "___________________________________"
MID_X = CONTENT_LEFT + 0.52 * CONTENT_WIDTH


class NDCalPaper(PleadingPaper):
    def __init__(self, filename: str, footer: str = ""):
        _register_fonts()
        super().__init__(filename, doc_title_footer=footer)

    # -- frame: serif line numbers and serif footer, lower footer rule
    def _draw_page_frame(self):
        c = self.c
        c.setLineWidth(0.5)
        c.line(VERT_LINE_LEFT, PAGE_H, VERT_LINE_LEFT, 0)
        c.line(VERT_LINE_RIGHT, PAGE_H, VERT_LINE_RIGHT, 0)
        c.line(CONTENT_RIGHT, PAGE_H, CONTENT_RIGHT, 0)
        c.setFont(SERIF, 12)
        for i in range(NUM_LINES):
            c.drawRightString(LINE_NUM_X, TEXT_START_Y - i * LINE_SPACING,
                              str(i + 1))
        c.line(CONTENT_LEFT, FOOTER_RULE_Y, CONTENT_RIGHT, FOOTER_RULE_Y)
        cx = (CONTENT_LEFT + CONTENT_RIGHT) / 2
        c.setFont(SERIF, 10)
        c.drawCentredString(cx, FOOTER_PAGE_Y, f"Page {self.page_num}")
        if self.doc_title_footer:
            size = 8
            while size > 6 and c.stringWidth(self.doc_title_footer, SERIF,
                                             size) > CONTENT_WIDTH - 8:
                size -= 0.5
            c.setFont(SERIF, size)
            c.drawCentredString(cx, FOOTER_TITLE_Y, self.doc_title_footer)

    # -- page-one header
    def header(self, party_block: bool = True) -> None:
        c = self.c
        if party_block:
            top = self._line_y(0) + 6
            c.setFont(SERIF, 12)
            for i, txt in enumerate(PARTY_BLOCK):
                c.drawString(CONTENT_LEFT, top - i * 14, txt)
            self.current_line = 5
        self.write_line("UNITED STATES DISTRICT COURT", bold=True, center=True)
        self.write_line("NORTHERN DISTRICT OF CALIFORNIA", bold=True,
                        center=True)
        self.blank_line()

    def caption(self, plaintiff: str, defendants: list[str],
                right_rows: list[tuple[str, str]]) -> None:
        """Open-box caption. right_rows: (text, style) with style in
        {"r", "b", ""}; "" is a blank row. Right rows use 12-pt spacing."""
        c = self.c
        first = self.current_line
        rule_y = self._line_y(first) + 13
        left_x = CONTENT_LEFT + 6
        left_cx = (CONTENT_LEFT + MID_X) / 2
        # left cell
        y = self._line_y(first)
        c.setFont(SERIF_B, 10)
        c.drawString(left_x, y, plaintiff)
        c.setFont(SERIF, 10)
        c.drawCentredString(left_cx, self._line_y(first + 1), "Plaintiff,")
        c.drawCentredString(left_cx, self._line_y(first + 2), "v.")
        c.setFont(SERIF_B, 10)
        dy = self._line_y(first + 3)
        for i, line in enumerate(defendants):
            c.drawString(left_x, dy - i * 12, line)
        n_left = 3 + max(2, (len(defendants) * 12) // LINE_SPACING + 1)
        c.setFont(SERIF, 10)
        c.drawCentredString(left_cx, self._line_y(first + n_left), "Defendants.")
        # right cell
        ry = self._line_y(first)
        rx = MID_X + 8
        for text, style in right_rows:
            if text:
                c.setFont(SERIF_B if style == "b" else SERIF, 9.5)
                c.drawString(rx, ry, text)
            ry -= 12
        bottom_y = min(self._line_y(first + n_left) - 6, ry + 6)
        c.setLineWidth(0.6)
        c.line(CONTENT_LEFT, rule_y, MID_X, rule_y)
        c.line(MID_X, rule_y, MID_X, bottom_y)
        lines_used = int((rule_y - bottom_y) / LINE_SPACING) + 1
        self.current_line = first + lines_used

    # -- body
    def heading(self, text: str) -> None:
        segs = self._parse_segments(text)
        segs = [(t, "bi" if s == "i" else "b") for t, s in segs]
        lines = self._wrap_segments(segs, CONTENT_WIDTH - 60, 0, FONT_SIZE)
        self.ensure_space(len(lines) + 2)
        cx = CONTENT_LEFT + CONTENT_WIDTH / 2
        for parts in lines:
            self._ensure_line()
            y = self._line_y(self.current_line)
            w = sum(self.c.stringWidth(
                t, "Times-BoldItalic" if s == "bi" else SERIF_B, FONT_SIZE)
                for t, s in parts)
            x = cx - w / 2
            for t, s in parts:
                fn = "Times-BoldItalic" if s == "bi" else SERIF_B
                self.c.setFont(fn, FONT_SIZE)
                self.c.drawString(x, y, t)
                x += self.c.stringWidth(t, fn, FONT_SIZE)
            self.current_line += 1
        self.blank_line()

    def para(self, text: str, indent_first: bool = True) -> None:
        self.write_wrapped(text, first_indent=36 if indent_first else 0)
        self.blank_line()

    def item(self, text: str) -> None:
        """Hanging indent: first line flush, continuation 0.5 inch in."""
        self.write_wrapped(text, indent=36, first_indent=-36)
        self.blank_line()

    # -- sign-offs
    def sign_off(self, date: str, signature_path: str | None = None,
                 sig_px: tuple[int, int] | None = None,
                 executed_at: str | None = None) -> None:
        self.ensure_space(8)
        if executed_at:
            self.write_wrapped(f"Executed on {date}, at {executed_at}.",
                               first_indent=36)
        else:
            self.write_line(f"Dated: {date}")
            self.write_line("Respectfully submitted,", right=True,
                            right_margin_offset=26)
        if signature_path and sig_px:
            self.draw_signature_image(signature_path, sig_px[0], sig_px[1],
                                      SIG_LINE, width=210,
                                      right_margin_offset=26, x_offset=10)
        else:
            self.blank_line()
            self.blank_line()
        self.write_line(SIG_LINE, right=True, right_margin_offset=26)
        self.write_line(SIGNOFF_NAME, bold=True, right=True,
                        right_margin_offset=26)
        self.write_line(SIGNOFF_ROLE, right=True, right_margin_offset=26)

    def judge_block(self, judge: str = "HON. CHARLES R. BREYER",
                    title: str = "United States District Judge") -> None:
        self.ensure_space(3)
        self._ensure_line()
        y = self._line_y(self.current_line)
        self.c.setFont(SERIF, FONT_SIZE)
        self.c.drawString(CONTENT_LEFT, y, "Dated: _______________, 2026")
        self.c.drawRightString(CONTENT_RIGHT - 26, y, SIG_LINE)
        self.current_line += 1
        self.write_line(judge, bold=True, right=True, right_margin_offset=26)
        self.write_line(title, right=True, right_margin_offset=26)
