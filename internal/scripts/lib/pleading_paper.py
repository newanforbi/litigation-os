# ==========================================================
# Shared California pleading-paper rendering engine.
#
# This is the single source of truth for the portfolio's pleading-paper
# PDF generation. Document-specific scripts (one per filing) should
# import PleadingPaper from here rather than embedding their own copy
# of this class -- a bug fixed here (e.g. the footer auto-shrink and
# heading page-break-protection logic below) is then fixed for every
# document generated from it, past and future, instead of only the one
# script that happened to get patched.
#
# Usage pattern for a document-specific script:
#
#   import os, sys
#   sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "lib"))
#   from pleading_paper import (
#       PleadingPaper, CONTENT_LEFT, CONTENT_RIGHT, CONTENT_WIDTH,
#       PAGE_W, PAGE_H, FONT_SIZE,
#   )
#
#   d = PleadingPaper(out_path, doc_title_footer="MY DOCUMENT -- CASE NAME")
#   ... build the document using d.write_line / d.write_wrapped / d.draw_caption_block ...
#   d.save()
# ==========================================================
import os, sys, re

try:
    import reportlab  # noqa: F401  # availability probe; the real imports follow below
except ImportError:
    os.system(f"{sys.executable} -m pip install reportlab")

from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib.colors import black

PAGE_W, PAGE_H = letter
MARGIN_LEFT = 1.0 * inch
MARGIN_RIGHT = 0.5 * inch
LINE_SPACING = 24
NUM_LINES = 28
FONT_SIZE = 12

TEXT_START_Y = PAGE_H - 1.05 * inch
TEXT_END_Y = TEXT_START_Y - (NUM_LINES - 1) * LINE_SPACING

VERT_LINE_LEFT = MARGIN_LEFT + 0.30 * inch
VERT_LINE_RIGHT = MARGIN_LEFT + 0.35 * inch
LINE_NUM_X = VERT_LINE_LEFT - 0.08 * inch

CONTENT_LEFT = VERT_LINE_RIGHT + 0.10 * inch
CONTENT_RIGHT = PAGE_W - MARGIN_RIGHT
CONTENT_WIDTH = CONTENT_RIGHT - CONTENT_LEFT

FOOTER_RULE_Y = TEXT_END_Y - 12
FOOTER_PAGE_Y = FOOTER_RULE_Y - 16
FOOTER_TITLE_Y = FOOTER_PAGE_Y - 18

COURT_LINE1 = "SUPERIOR COURT OF THE STATE OF CALIFORNIA"


class PleadingPaper:
    def __init__(self, filename, doc_title_footer="", style="classic", footer_right=""):
        """
        filename: output PDF path.
        doc_title_footer: the small centered footer line repeated on every
            page (e.g. "OPPOSITION TO DEMURRER -- NEWANFORBI v. CHP, ET AL.").
            Auto-shrinks if it would overflow the space between the two
            vertical border lines, so a long case caption can never print
            past the page edges the way it did before this fix existed.
        """
        self.c = canvas.Canvas(filename, pagesize=letter)
        self.page_num = 0
        self.current_line = 0
        self.doc_title_footer = doc_title_footer
        # style: "classic" (double rule left, single rule right -- default) or
        # "minimal" (one hairline rule between numbers and text, no right rule,
        # small gray numerals, framed caption, split footer). Text geometry is
        # identical in both, so a document reflows the same way either style.
        self.style = style
        self.footer_right = footer_right
        self.start_new_page()

    def start_new_page(self):
        if self.page_num > 0:
            self.c.showPage()
        self.page_num += 1
        self.current_line = 0
        self._draw_page_frame()

    def _draw_page_frame(self):
        if self.style == "minimal":
            return self._draw_page_frame_minimal()
        c = self.c
        c.setStrokeColor(black)
        c.setLineWidth(0.5)
        c.line(VERT_LINE_LEFT, PAGE_H, VERT_LINE_LEFT, 0)
        c.line(VERT_LINE_RIGHT, PAGE_H, VERT_LINE_RIGHT, 0)
        c.line(CONTENT_RIGHT, PAGE_H, CONTENT_RIGHT, 0)
        c.setFont("Helvetica", 10)
        for i in range(NUM_LINES):
            y = TEXT_START_Y - i * LINE_SPACING
            c.drawRightString(LINE_NUM_X, y, str(i + 1))
        c.setLineWidth(0.5)
        c.line(VERT_LINE_RIGHT, FOOTER_RULE_Y, CONTENT_RIGHT, FOOTER_RULE_Y)
        center_x = (VERT_LINE_LEFT + CONTENT_RIGHT) / 2
        c.setFont("Helvetica", 10)
        c.drawCentredString(center_x, FOOTER_PAGE_Y, f"Page {self.page_num}")
        if self.doc_title_footer:
            avail_footer_width = CONTENT_RIGHT - VERT_LINE_LEFT - 8
            footer_size = 9
            while footer_size > 6 and c.stringWidth(self.doc_title_footer, "Helvetica", footer_size) > avail_footer_width:
                footer_size -= 0.5
            c.setFont("Helvetica", footer_size)
            c.drawCentredString(center_x, FOOTER_TITLE_Y, self.doc_title_footer)

    def _draw_page_frame_minimal(self):
        from reportlab.lib.colors import Color
        c = self.c
        c.setStrokeColor(black)
        c.setLineWidth(0.4)
        c.line(VERT_LINE_RIGHT, PAGE_H, VERT_LINE_RIGHT, 0)
        c.setFillColor(Color(0.38, 0.38, 0.38))
        c.setFont("Helvetica", 9)
        for i in range(NUM_LINES):
            c.drawRightString(VERT_LINE_RIGHT - 8, TEXT_START_Y - i * LINE_SPACING, str(i + 1))
        c.setFillColor(black)
        c.line(CONTENT_LEFT, FOOTER_RULE_Y, CONTENT_RIGHT - 16, FOOTER_RULE_Y)
        center_x = (CONTENT_LEFT + CONTENT_RIGHT - 16) / 2
        c.setFont("Times-Roman", 10)
        c.drawCentredString(center_x, FOOTER_PAGE_Y, str(self.page_num))
        c.setFont("Times-Roman", 8.5)
        if self.doc_title_footer:
            c.drawString(CONTENT_LEFT, FOOTER_TITLE_Y, self.doc_title_footer)
        if self.footer_right:
            c.drawRightString(CONTENT_RIGHT - 16, FOOTER_TITLE_Y, self.footer_right)

    def _line_y(self, idx):
        return TEXT_START_Y - idx * LINE_SPACING

    def _ensure_line(self):
        if self.current_line >= NUM_LINES:
            self.start_new_page()

    def ensure_space(self, n):
        """Force a page break now if fewer than n lines remain, so a
        heading (or a signature block) can't get orphaned at the bottom
        of a page, split from the text that belongs with it."""
        if self.current_line + n > NUM_LINES:
            self.start_new_page()

    def write_line(self, text, bold=False, font="Times-Roman", size=FONT_SIZE,
                   italic=False, center=False, right=False, indent=0,
                   underline=False, right_margin_offset=0):
        if bold and italic: fn = "Times-BoldItalic"
        elif bold: fn = "Times-Bold"
        elif italic: fn = "Times-Italic"
        else: fn = font
        # Left-aligned long lines must wrap inside the right vertical rule.
        # Center/right lines are caller-controlled (captions, sign-off).
        if not center and not right and not underline:
            avail = CONTENT_WIDTH - indent - 16
            if self.c.stringWidth(text, fn, size) > avail:
                self.write_wrapped(
                    text, bold=bold, font=font, size=size, italic=italic,
                    indent=indent, first_indent=0, right_inset=16,
                )
                return
        self._ensure_line()
        y = self._line_y(self.current_line)
        c = self.c
        c.setFont(fn, size)
        x = CONTENT_LEFT + indent
        if center:
            cx = CONTENT_LEFT + CONTENT_WIDTH / 2
            c.drawCentredString(cx, y, text)
        elif right:
            c.drawRightString(CONTENT_RIGHT - right_margin_offset, y, text)
        else:
            c.drawString(x, y, text)
        if underline:
            tw = c.stringWidth(text, fn, size)
            if center: ux = cx - tw / 2
            elif right: ux = (CONTENT_RIGHT - right_margin_offset) - tw
            else: ux = x
            c.setLineWidth(0.5)
            c.line(ux, y - 1.5, ux + tw, y - 1.5)
        self.current_line += 1

    def blank_line(self):
        self._ensure_line()
        self.current_line += 1

    def write_wrapped(self, text, bold=False, font="Times-Roman", size=FONT_SIZE,
                      italic=False, indent=0, first_indent=36, right_inset=16):
        # right_inset keeps glyphs from visually kissing or crossing the right rule.
        avail = CONTENT_WIDTH - indent - right_inset
        segs = self._parse_segments(text)
        if bold or italic:
            default = "bi" if bold and italic else ("b" if bold else "i")
            segs = [(t, s if s != "r" else default) for t, s in segs]
        lines = self._wrap_segments(segs, avail, first_indent, size)
        c = self.c
        for i, parts in enumerate(lines):
            self._ensure_line()
            y = self._line_y(self.current_line)
            x = CONTENT_LEFT + indent
            if i == 0:
                x += first_indent
            for pt, ps in parts:
                if ps == "bi": pfn = "Times-BoldItalic"
                elif ps == "b": pfn = "Times-Bold"
                elif ps == "i": pfn = "Times-Italic"
                else: pfn = "Times-Roman"
                c.setFont(pfn, size)
                c.drawString(x, y, pt)
                x += c.stringWidth(pt, pfn, size)
            self.current_line += 1

    def _parse_segments(self, text):
        segs = []
        pat = r"<<(b|i|bi):([^>]*)>>"
        last = 0
        for m in re.finditer(pat, text):
            if m.start() > last:
                segs.append((text[last:m.start()], "r"))
            segs.append((m.group(2), m.group(1)))
            last = m.end()
        if last < len(text):
            segs.append((text[last:], "r"))
        return segs

    def _wrap_segments(self, segs, avail, fi, size):
        c = self.c
        lines, cur = [], []
        cw = fi
        def ffs(s):
            if s == "bi": return "Times-BoldItalic"
            elif s == "b": return "Times-Bold"
            elif s == "i": return "Times-Italic"
            return "Times-Roman"
        for st, ss in segs:
            fn = ffs(ss)
            words = st.split(" ")
            for wi, w in enumerate(words):
                if wi > 0:
                    w = " " + w
                ww = c.stringWidth(w, fn, size)
                if cw + ww > avail and cur:
                    lines.append(cur)
                    cur = []
                    cw = 0
                    if w.startswith(" "):
                        w = w[1:]
                        ww = c.stringWidth(w, fn, size)
                cur.append((w, ss))
                cw += ww
        if cur:
            lines.append(cur)
        return lines

    def draw_caption_block(self, left, right, caption_size=10, tight_lh=13, boxed=True):
        c = self.c
        box_left_x = CONTENT_LEFT
        box_right_x = CONTENT_LEFT + CONTENT_WIDTH * 0.52
        right_col_x = box_right_x + 12
        start_line = self.current_line
        self._ensure_line()
        first_y = self._line_y(self.current_line)
        box_top = first_y + 14
        left_x_pad = 8
        rows = max(len(left), len(right))
        for i in range(rows):
            y = first_y - i * tight_lh
            if y < TEXT_END_Y + 2:
                break
            if i < len(left):
                lt, lb, li = left[i]
                if lb and li: fn = "Times-BoldItalic"
                elif lb: fn = "Times-Bold"
                elif li: fn = "Times-Italic"
                else: fn = "Times-Roman"
                c.setFont(fn, caption_size)
                c.drawString(box_left_x + left_x_pad, y, lt)
            if i < len(right):
                rt, rb, ri = right[i]
                if rb and ri: fn = "Times-BoldItalic"
                elif rb: fn = "Times-Bold"
                elif ri: fn = "Times-Italic"
                else: fn = "Times-Roman"
                size = caption_size
                avail = CONTENT_RIGHT - right_col_x - 8
                while size > 7 and c.stringWidth(rt, fn, size) > avail:
                    size -= 0.25
                c.setFont(fn, size)
                c.drawString(right_col_x, y, rt)
        last_row_y = first_y - (max(len(left), len(right)) - 1) * tight_lh
        box_bottom = last_row_y - 8
        if boxed and self.style == "minimal":
            c.setLineWidth(0.6)
            c.rect(CONTENT_LEFT - 2, box_bottom, CONTENT_RIGHT - 16 - (CONTENT_LEFT - 2),
                   box_top - box_bottom)
            c.line(box_right_x, box_top, box_right_x, box_bottom)
        elif boxed:
            c.setLineWidth(0.75)
            c.line(VERT_LINE_RIGHT, box_top, box_right_x, box_top)
            c.line(VERT_LINE_RIGHT, box_bottom, box_right_x, box_bottom)
            c.line(box_right_x, box_top, box_right_x, box_bottom)
        max_rows = max(len(left), len(right))
        true_bottom_y = first_y - (max_rows - 1) * tight_lh - 8
        consumed_height = box_top - true_bottom_y
        lines_consumed = int(consumed_height / LINE_SPACING) + 1
        self.current_line = start_line + lines_consumed

    def write_respectfully_submitted(self, right_margin_offset=20):
        """Standard closer. ``draw_signature_image`` supplies the gap
        between this line and the stamp; do not add your own blank lines
        unless you want extra air."""
        self.write_line(
            "Respectfully submitted,",
            right=True,
            right_margin_offset=right_margin_offset,
        )

    def draw_signature_image(self, image_path, img_w_px, img_h_px, line_text,
                              width=210, right_margin_offset=20, x_offset=0,
                              height_scale=1.15, above_lines=2):
        """Draw the canonical signature centered over an underscore signature
        line at the current line position, then advance past it. Call this
        immediately before writing the underscore line itself with
        write_line(line_text, right=True, right_margin_offset=...).
        ``x_offset`` shifts the stamp right (positive) or left (negative)
        from geometric center, in points. ``height_scale`` stretches the
        stamp upward from the line without changing width.
        ``above_lines`` (default 2) leaves air between the preceding text
        — usually "Respectfully submitted," — and the stamp, which draws
        upward from the underscore."""
        extra = max(0, int(above_lines))
        self.ensure_space(extra + 4)
        for _ in range(extra):
            self.blank_line()
        self._ensure_line()
        y = self._line_y(self.current_line)
        img_h = width * (img_h_px / img_w_px) * height_scale
        line_right = CONTENT_RIGHT - right_margin_offset
        line_width = self.c.stringWidth(line_text, "Times-Roman", FONT_SIZE)
        line_center = line_right - line_width / 2
        img_x = line_center - width / 2 + x_offset
        self.c.drawImage(image_path, img_x, y + 3, width=width, height=img_h,
                          mask='auto', preserveAspectRatio=False)

    def save(self):
        self.c.save()
