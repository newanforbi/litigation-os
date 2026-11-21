#!/usr/bin/env python3
"""Matter 32 — Administrative Motion for Leave to File Sur-Reply Packet (Dkt. 33).

Renders four classic N.D. Cal. Civil L.R. 3-4 pleading-paper PDFs:
  1. Administrative Motion for Leave to File Sur-Reply (<= 5 pp., Civil L.R. 7-11(a))
  2. Declaration of Brendan Ngwa Nforbi ISO Administrative Motion (Civil L.R. 7-11(a))
  3. Exhibit A — [Proposed] Sur-Reply in Opposition to Motion to Dismiss and Motion to Strike
  4. [Proposed] Order Granting Administrative Motion for Leave to File Sur-Reply

Civil L.R. 3-4 compliance:
  * 8.5 x 11 letter, double vertical rule, 28 numbered lines per page.
  * Times-Roman 12 pt, double-spaced (24 pt), except caption, block quotes, and footnotes.
  * Lines 1-6 counsel/pro se identification, line 7 blank, court title commences on line 8.
  * Footer with document title and Page X of Y.
  * Unsigned blank signature lines for Plaintiff's execution.

Not an npm script. Run: python3 internal/scripts/matter32-surreply-motion.py
"""
from __future__ import annotations

import sys
from pathlib import Path

from pypdf import PdfReader
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

OUT_DIR = ROOT / "documents/matter-32/ndcal"
SIG_LINE = "___________________________________"
SIG_OFFSET = 20


class ClassicPleading(PleadingPaper):
    """Classic N.D. Cal. double-rule 28-line pleading paper (Civil L.R. 3-4)."""

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

    def draw_caption_block(self, left, right, caption_size=10.5, tight_lh=13, boxed=True):
        c = self.c
        box_left_x = pp.CONTENT_LEFT
        box_right_x = pp.CONTENT_LEFT + pp.CONTENT_WIDTH * 0.50
        right_col_x = box_right_x + 10
        start_line = self.current_line
        self._ensure_line()
        first_y = self._line_y(self.current_line)
        box_top = first_y + 13
        left_x_pad = 4
        rows = max(len(left), len(right))
        for i in range(rows):
            y = first_y - i * tight_lh
            if y < TEXT_END_Y + 2:
                break
            if i < len(left):
                self._caption_string(
                    left[i], box_left_x + left_x_pad, y, caption_size, box_right_x - box_left_x - 10
                )
            if i < len(right):
                self._caption_string(
                    right[i], right_col_x, y, caption_size, CONTENT_RIGHT - right_col_x - 4
                )
        if boxed:
            last_row_y = first_y - (rows - 1) * tight_lh
            box_bottom = last_row_y - 7
            c.setStrokeColorRGB(0, 0, 0)
            c.setLineWidth(0.75)
            c.line(box_left_x, box_top, box_right_x, box_top)
            c.line(box_left_x, box_bottom, box_right_x, box_bottom)
            c.line(box_right_x, box_top, box_right_x, box_bottom)
        consumed_height = (rows - 1) * tight_lh + 13 + 7
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
        sz = size
        while sz > 8 and self.c.stringWidth(text, fn, sz) > avail:
            sz -= 0.25
        self.c.setFont(fn, sz)
        self.c.drawString(x, y, text)

    def write_blockquote(self, text, indent=36, right_inset=36, size=11, leading=14):
        """Single-spaced indented block quotation per Civil L.R. 3-4(c)(2)."""
        avail = pp.CONTENT_WIDTH - indent - right_inset
        segs = self._parse_segments(text)
        lines = self._wrap_segments(segs, avail, 0, size)
        needed_slots = max(1, int((len(lines) * leading + 8) / LINE_SPACING) + 1)
        self.ensure_space(needed_slots)
        start_y = self._line_y(self.current_line)
        c = self.c
        for i, parts in enumerate(lines):
            y = start_y - i * leading
            x = pp.CONTENT_LEFT + indent
            for pt, ps in parts:
                if ps == "bi":
                    pfn = "Times-BoldItalic"
                elif ps == "b":
                    pfn = "Times-Bold"
                elif ps == "i":
                    pfn = "Times-Italic"
                else:
                    pfn = "Times-Roman"
                c.setFont(pfn, size)
                c.drawString(x, y, pt)
                x += c.stringWidth(pt, pfn, size)
        self.current_line += needed_slots

    def write_footnote_block(self, text, size=10, leading=12.5):
        """Single-spaced footnote with short horizontal rule per Civil L.R. 3-4(c)(2)."""
        avail = pp.CONTENT_WIDTH - 16
        segs = self._parse_segments(text)
        lines = self._wrap_segments(segs, avail, 18, size)
        needed_slots = max(2, int((len(lines) * leading + 16) / LINE_SPACING) + 1)
        self.ensure_space(needed_slots)
        rule_y = self._line_y(self.current_line) + 6
        c = self.c
        c.setLineWidth(0.5)
        c.line(pp.CONTENT_LEFT, rule_y, pp.CONTENT_LEFT + 144, rule_y)
        start_y = rule_y - 12
        for i, parts in enumerate(lines):
            y = start_y - i * leading
            x = pp.CONTENT_LEFT + (18 if i == 0 else 0)
            for pt, ps in parts:
                if ps == "bi":
                    pfn = "Times-BoldItalic"
                elif ps == "b":
                    pfn = "Times-Bold"
                elif ps == "i":
                    pfn = "Times-Italic"
                else:
                    pfn = "Times-Roman"
                c.setFont(pfn, size)
                c.drawString(x, y, pt)
                x += c.stringWidth(pt, pfn, size)
        self.current_line += needed_slots


def _header_and_caption(d: ClassicPleading, right_caption: list[tuple[str, bool, bool]], include_pro_se_block: bool = True):
    if include_pro_se_block:
        d.write_line("BRENDAN NGWA NFORBI", bold=True)
        d.write_line("Plaintiff, In Propria Persona")
        d.write_line("1455 Cat Tail Drive")
        d.write_line("Stockton, CA 95204")
        d.write_line("Telephone: (209) 801-4442")
        d.write_line("E-mail: bnn.cdl@gmail.com")
        d.blank_line()
    # Court title commences on line 8 for party filings (Civil L.R. 3-4(a)(3))
    d.write_line("UNITED STATES DISTRICT COURT", bold=True, center=True)
    d.write_line("FOR THE NORTHERN DISTRICT OF CALIFORNIA", bold=True, center=True)
    d.write_line("SAN FRANCISCO DIVISION", bold=True, center=True)
    d.blank_line()

    left_caption = [
        ("BRENDAN NGWA NFORBI,", True, False),
        ("", False, False),
        ("        Plaintiff,", False, False),
        ("", False, False),
        ("    v.", False, False),
        ("", False, False),
        ("SANTIAGO MEZA-GONZALEZ", True, False),
        ("(CHP Badge #023295), in his", False, False),
        ("individual capacity;", False, False),
        ("JOSE MELANO (CHP Badge #023054),", True, False),
        ("in his individual capacity; and", False, False),
        ("DOES 1 through 10, inclusive,", False, False),
        ("", False, False),
        ("        Defendants.", False, False),
    ]
    d.draw_caption_block(left_caption, right_caption, caption_size=10.5, tight_lh=13, boxed=True)


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
    d.ensure_space(len(lines) + 2)
    for line in lines:
        d.write_line(line, bold=True, center=True)


def _section_heading(d: ClassicPleading, text: str) -> None:
    d.ensure_space(4)
    d.write_wrapped(text, bold=True, first_indent=0)


def _plaintiff_signature(d: ClassicPleading, dated_line: str, respectfully: bool = True) -> None:
    d.ensure_space(6 if respectfully else 4)
    if dated_line:
        d.write_line(dated_line)
    if respectfully:
        d.write_line("Respectfully submitted,", right=True, right_margin_offset=SIG_OFFSET)
        d.blank_line()
    else:
        d.blank_line()
    d.write_line(SIG_LINE, right=True, right_margin_offset=SIG_OFFSET)
    d.write_line("BRENDAN NGWA NFORBI", bold=True, right=True, right_margin_offset=SIG_OFFSET)
    d.write_line("Plaintiff, In Propria Persona", right=True, right_margin_offset=SIG_OFFSET)


def _render_two_pass(out_path: Path, build_fn) -> int:
    build_fn(out_path, 0)
    total = len(PdfReader(str(out_path)).pages)
    build_fn(out_path, total)
    total2 = len(PdfReader(str(out_path)).pages)
    if total2 != total:
        raise SystemExit(f"Page count changed between passes for {out_path.name}: {total} -> {total2}")
    print(f"Wrote {out_path.name} ({total2} pages)")
    return total2


# ---------------------------------------------------------------------------
# Document 3 (built first so we know its exact page count for Docs 1 & 2)
# ---------------------------------------------------------------------------
def build_surreply(out_path: Path, page_total: int) -> None:
    footer = "Exhibit A — [Proposed] Sur-Reply ISO Opposition to Motion to Dismiss (3:26-cv-08271-CRB)"
    d = ClassicPleading(str(out_path), doc_title_footer=footer, page_total=page_total)
    right = [
        ("Case No. 3:26-cv-08271-CRB", True, False),
        ("", False, False),
        ("EXHIBIT A — [PROPOSED]", True, False),
        ("PLAINTIFF'S SUR-REPLY IN", True, False),
        ("OPPOSITION TO DEFENDANTS'", True, False),
        ("MOTION TO DISMISS AND", True, False),
        ("MOTION TO STRIKE", True, False),
        ("", False, False),
        ("Judge: Hon. Charles R. Breyer", False, False),
        ("Date: December 18, 2026", False, False),
        ("Time: 10:00 a.m. (Zoom Webinar)", False, False),
        ("Action Filed: August 10, 2026", False, False),
    ]
    _header_and_caption(d, right)

    d.write_wrapped(
        "Pursuant to leave of Court, Plaintiff Brendan Ngwa Nforbi submits this brief Sur-Reply "
        "limited strictly to four new arguments, procedural requests, and record mischaracterizations "
        "introduced for the first time in Defendants' Reply Brief (Dkt. 33)."
    )

    _section_heading(
        d,
        "I. DEFENDANTS' NEW RULE 12(b)(6) STANDARD CONTRADICTS NINTH CIRCUIT PRECEDENT",
    )
    d.write_wrapped(
        "Citing <<i:Bell Atlantic Corp. v. Twombly>>, 550 U.S. 544, 555 (2007), and <<i:Ashcroft "
        "v. Iqbal>>, 556 U.S. 662, 667 (2009), Defendants' Reply newly asserts that \"the Court "
        "is free to draw all reasonable inferences from the facts alleged, whether such inferences "
        "are 'for' or 'against' Plaintiff's theory of liability,\" and that a complaint fails "
        "whenever its allegations are \"also consistent with an innocent explanation.\" (Dkt. 33 "
        "at 2–3, 7.)"
    )
    d.write_wrapped(
        "Binding Ninth Circuit precedent holds the exact opposite on both points. First, \"[o]n a "
        "motion to dismiss for failure to state a claim, the court must presume all factual "
        "allegations of the complaint to be true and draw all reasonable inferences in favor of the "
        "nonmoving party.\" <<i:Usher v. City of Los Angeles>>, 828 F.2d 556, 561 (9th Cir. 1987). "
        "Second, <<i:Starr v. Baca>>, 652 F.3d 1202 (9th Cir. 2011), squarely rejected Defendants' "
        "reading of <<i:Twombly>> and <<i:Iqbal>>:"
    )
    d.write_blockquote(
        "If there are two alternative explanations, one advanced by defendant and the other "
        "advanced by plaintiff, both of which are plausible, plaintiff's complaint survives a "
        "motion to dismiss under Rule 12(b)(6). Plaintiff's complaint may be dismissed only "
        "when defendant's plausible alternative explanation is so convincing that plaintiff's "
        "explanation is <<i:implausible>>."
    )
    d.write_wrapped(
        "<<i:Id.>> at 1216 (emphasis in original).¹ Defendants' inverted standard drives their "
        "claim that Plaintiff's allegation of coherent speech on video (FAC ¶ 26) is \"not "
        "inconsistent with slurred speech\" (Dkt. 33 at 3, 6, 7), and their claim that silence on "
        "field sobriety test results supports an adverse inference of intoxication (<<i:id.>> at "
        "7). Under <<i:Usher>> and <<i:Starr>>, competing factual inferences cannot be resolved "
        "against Plaintiff at Rule 12(b)(6).",
        first_indent=0,
    )
    d.write_footnote_block(
        "¹ Defendants' repeated citation to page 667 of <<i:Iqbal>> (Dkt. 33 at 2, 3, 7) refers to "
        "the opinion's factual background rather than its pleading analysis (556 U.S. at 678–82). "
        "In any event, <<i:Starr>> states the binding Ninth Circuit synthesis of <<i:Iqbal>>'s "
        "\"obvious alternative explanation\" principle."
    )

    _section_heading(
        d,
        "II. AIRS AROMATICS DOES NOT BAR CONFORMING PARAGRAPH 16 TO THE DASHCAM VIDEO",
    )
    d.write_wrapped(
        "For the first time on reply, Defendants cite <<i:Airs Aromatics, LLC v. Victoria's Secret "
        "Stores Brand Mgmt., Inc.>>, 744 F.3d 595, 600 (9th Cir. 2014), to argue Plaintiff cannot "
        "amend FAC ¶ 16 to align with the CHP dashcam—that the officers' knock woke Plaintiff and "
        "Officer Melano opened the door three seconds after saying \"open the window.\" (Dkt. 33 "
        "at 5, 9.) Defendants overlook <<i:PAE Gov't Servs., Inc. v. MPRI, Inc.>>, 514 F.3d 856, "
        "860 (9th Cir. 2007): \"[t]here is nothing in the Federal Rules of Civil Procedure to "
        "prevent a party from filing successive pleadings that make inconsistent or even "
        "contradictory allegations.\" Good-faith factual refinement is not sham pleading. <<i:Id.>> "
        "at 858–60. Unlike the counseled plaintiff in <<i:Airs Aromatics>> who conceded seven "
        "years of non-use in appellate briefing, a <<i:pro se>> plaintiff conforming a three-word "
        "shorthand phrase (\"while still asleep\") to Defendants' own recording acts with candor. "
        "Defendants cannot invoke that knock-and-command sequence to defend the entry (Dkt. 33 at "
        "4) while claiming Plaintiff is barred from pleading it accurately."
    )

    _section_heading(
        d,
        "III. CLARIFYING A CHP FORM FIELD LABEL IS NOT A CONCESSION OF ALCOHOL ODOR",
    )
    d.write_wrapped(
        "Defendants' Reply twice treats Plaintiff's Opposition as admitting an \"odor of alcohol\" "
        "supporting probable cause to search and qualified immunity to arrest. (Dkt. 33 at 6, 8.) "
        "Plaintiff merely corrected what the pre-printed CHP form checkbox <<i:says>> (\"odor of "
        "an alcoholic beverage, not to a container\"), not whether the officer's assertion was "
        "true. FAC ¶ 26 expressly denies intoxication, alleges the cup contained urine rather than "
        "alcohol, and challenges Officer Meza-Gonzalez's warrant representations. Under <<i:Khoja "
        "v. Orexigen Therapeutics, Inc.>>, 899 F.3d 988, 1003 (9th Cir. 2018), \"it is improper to "
        "assume the truth of an incorporated document if such assumptions only serve to dispute "
        "facts stated in a well-pleaded complaint.\""
    )

    _section_heading(
        d,
        "IV. CONVERTING RULE 12(f) INTO A RULE 12(b)(6) DISMISSAL OF PUNITIVE DAMAGES FAILS",
    )
    d.write_wrapped(
        "Confronted with <<i:Whittlestone, Inc. v. Handi-Craft Co.>>, 618 F.3d 970, 974–75 (9th "
        "Cir. 2010), Defendants ask for the first time on reply to treat Plaintiff's punitive "
        "damages prayer as \"a separate claim\" under Rule 12(b)(6). (Dkt. 33 at 10.) Procedurally, "
        "new requests raised on reply may be disregarded, <<i:Zamani v. Carnes>>, 491 F.3d 990, "
        "997 (9th Cir. 2007), and punitive damages are a remedy, not a claim subject to Rule "
        "12(b)(6) dismissal, <<i:Saroya v. Univ. of the Pacific>>, 503 F. Supp. 3d 986, 1000 (N.D. "
        "Cal. 2020). On the merits, § 1983 punitive damages require only \"reckless or callous "
        "indifference to the federally protected rights of others,\" even when recklessness is also "
        "the underlying liability standard. <<i:Smith v. Wade>>, 461 U.S. 30, 51–56 (1983). Because "
        "Count I plausibly alleges deliberate or reckless material falsehoods and omissions in "
        "seeking a blood-draw warrant, punitive damages survive on the pleadings."
    )

    _section_heading(d, "V. CONCLUSION")
    d.write_wrapped(
        "The Court should reject the new arguments and misstated standards in Defendants' Reply "
        "(Dkt. 33), deny dismissal of Counts I, III, IV, and V and the motion to strike punitive "
        "damages, and grant targeted leave to amend as to any defect identified."
    )
    _plaintiff_signature(d, "Dated: November ___, 2026", respectfully=True)
    d.c.setTitle("Exhibit A — [Proposed] Sur-Reply in Opposition to Motion to Dismiss (3:26-cv-08271-CRB)")
    d.c.setAuthor("Brendan Ngwa Nforbi")
    d.save()


# ---------------------------------------------------------------------------
# Document 1 — Administrative Motion (Civil L.R. 7-3(d), 7-11 — max 5 pages)
# ---------------------------------------------------------------------------
def make_admin_motion_builder(surreply_pages: int):
    page_word = {1: "one", 2: "two", 3: "three", 4: "four", 5: "five"}.get(
        surreply_pages, str(surreply_pages)
    )

    def build_admin_motion(out_path: Path, page_total: int) -> None:
        footer = "Plaintiff's Administrative Motion for Leave to File Sur-Reply (3:26-cv-08271-CRB)"
        d = ClassicPleading(str(out_path), doc_title_footer=footer, page_total=page_total)
        right = [
            ("Case No. 3:26-cv-08271-CRB", True, False),
            ("", False, False),
            ("PLAINTIFF'S ADMINISTRATIVE", True, False),
            ("MOTION FOR LEAVE TO FILE", True, False),
            ("SUR-REPLY IN OPPOSITION TO", True, False),
            ("MOTION TO DISMISS AND STRIKE", True, False),
            ("[Civil L.R. 7-3(d), 7-11]", False, False),
            ("", False, False),
            ("Judge: Hon. Charles R. Breyer", False, False),
            ("MTD Hearing: December 18, 2026", False, False),
            ("Time: 10:00 a.m. (Zoom Webinar)", False, False),
            ("Action Filed: August 10, 2026", False, False),
        ]
        _header_and_caption(d, right)

        _center_bold(d, "ADMINISTRATIVE MOTION")
        d.write_wrapped(
            f"Pursuant to Civil Local Rules 7-3(d) and 7-11, Plaintiff Brendan Ngwa Nforbi, "
            f"appearing <<i:in propria persona>>, respectfully moves for leave to file a short "
            f"{page_word}-page Sur-Reply—attached hereto as <<b:Exhibit A>>—responding solely to "
            f"new legal arguments, a new request for relief, and material mischaracterizations "
            f"raised for the first time in Defendants Santiago Meza-Gonzalez and Jose Melano's "
            f"Reply Brief in Support of Motion to Dismiss and Motion to Strike (Dkt. 33, filed "
            f"November 20, 2026). This Motion is supported by the following Memorandum of Points "
            f"and Authorities, the accompanying Declaration of Brendan Ngwa Nforbi under Civil "
            f"L.R. 7-11(a), the proposed Sur-Reply (Exhibit A), and the [Proposed] Order filed "
            f"concurrently herewith."
        )

        _center_bold(d, "MEMORANDUM OF POINTS AND AUTHORITIES")
        _section_heading(d, "I. PROCEDURAL BACKGROUND")
        d.write_wrapped(
            "On October 26, 2026, Defendants filed their Motion to Dismiss the First Amended "
            "Complaint (\"FAC,\" Dkt. 5) and Motion to Strike Plaintiff's prayers for punitive "
            "damages and attorney's fees under Federal Rules of Civil Procedure 12(b)(6) and 12(f). "
            "(Dkt. 22.) Plaintiff filed his Opposition on October 29, 2026 (Dkt. 27); under Civil "
            "L.R. 7-3(a), the opposition deadline was November 9, 2026. On October 30, 2026, this "
            "case was reassigned to Judge Charles R. Breyer in an order expressly directing that "
            "\"existing briefing schedules for motions remain unchanged.\" (Dkt. 29.) On November 3, "
            "2026, the Clerk noticed the Motion hearing for Friday, December 18, 2026, at 10:00 a.m. "
            "via Zoom webinar. (Dkt. 31.)"
        )
        d.write_wrapped(
            "Under Civil L.R. 7-3(c) and Dkt. 29, Defendants' reply was due November 16, 2026—"
            "seven days after the November 9 opposition deadline. Four days late, without seeking "
            "a stipulation or leave of Court under Civil L.R. 6-2 or 6-3, Defendants filed their "
            "Reply on November 20, 2026. (Dkt. 33.)¹ Plaintiff does not ask the Court to strike "
            "Defendants' untimely Reply; instead, Plaintiff seeks leave to file a concise "
            f"{page_word}-page Sur-Reply limited strictly to four new matters introduced on reply."
        )
        d.write_footnote_block(
            "¹ Defendants' Reply caption also lists the hearing as Saturday, \"December 19, 2026,\" "
            "in \"Courtroom 4,\" and retains a superseded magistrate judge suffix in the footer "
            "(3:26-cv-08271 PHK). (Dkt. 33 at 1.) Per Dkt. 31, the hearing is set for Friday, "
            "December 18, 2026, at 10:00 a.m. via Zoom webinar before Judge Breyer."
        )

        _section_heading(d, "II. LEGAL STANDARD")
        d.write_wrapped(
            "Under Civil L.R. 7-3(d), no supplemental brief may be filed after a reply without "
            "prior Court approval. The Ninth Circuit recognizes Civil L.R. 7-3(d) as the proper "
            "mechanism to seek leave to file a sur-reply when a reply injects new matter. "
            "<<i:Dutta v. State Farm Mut. Auto. Ins. Co.>>, 895 F.3d 1166, 1171–72 (9th Cir. 2018); "
            "<<i:see also Zamani v. Carnes>>, 491 F.3d 990, 997 (9th Cir. 2007) (district court need "
            "not consider arguments raised for the first time on reply). Courts in this District "
            "find good cause for a brief sur-reply \"where defendants have raised a new argument "
            "or evidence in a reply brief\" to which the opposing party has had no opportunity to "
            "respond. <<i:In re Cloudera, Inc. Sec. Litig.>>, No. 19-CV-03221-LHK, 2021 WL 2115303, "
            "at *8 n.2 (N.D. Cal. May 25, 2021)."
        )

        _section_heading(d, "III. GOOD CAUSE EXISTS FOR A NARROW SUR-REPLY")
        d.write_wrapped(
            "Plaintiff does not seek to re-argue his Opposition. Rather, Defendants' Reply injects "
            "four specific new arguments, procedural requests, and record mischaracterizations not "
            "present in Defendants' opening brief (Dkt. 22):"
        )
        d.write_wrapped(
            "<<b:1. New Rule 12(b)(6) Standard Inverting Ninth Circuit Law (Dkt. 33 at 2–3, 7).>> "
            "For the first time on reply, Defendants assert that on a Rule 12(b)(6) motion the "
            "Court may draw inferences \"against\" Plaintiff and must dismiss whenever allegations "
            "are \"also consistent with an innocent explanation\"—directly contrary to <<i:Usher v. "
            "City of Los Angeles>>, 828 F.2d 556, 561 (9th Cir. 1987), and <<i:Starr v. Baca>>, "
            "652 F.3d 1202, 1216 (9th Cir. 2011)."
        )
        d.write_wrapped(
            "<<b:2. New Airs Aromatics Bar to Amendment (Dkt. 33 at 5, 9).>> For the first time on "
            "reply, Defendants invoke <<i:Airs Aromatics, LLC v. Victoria's Secret Stores Brand "
            "Mgmt., Inc.>>, 744 F.3d 595, 600 (9th Cir. 2014), to argue Plaintiff is barred from "
            "conforming FAC ¶ 16 to the CHP dashcam sequence. Plaintiff has had no chance to "
            "address <<i:Airs Aromatics>> or cite <<i:PAE Gov't Servs., Inc. v. MPRI, Inc.>>, "
            "514 F.3d 856, 860 (9th Cir. 2007)."
        )
        d.write_wrapped(
            "<<b:3. New Mischaracterization of a CHP Form-Label Clarification as a Concession of "
            "Alcohol Odor (Dkt. 33 at 6, 8).>> Defendants convert Plaintiff's candid correction of "
            "a pre-printed CHP form checkbox label into an affirmative factual concession of "
            "alcohol odor supporting probable cause and qualified immunity, contrary to FAC ¶ 26 "
            "and <<i:Khoja v. Orexigen Therapeutics, Inc.>>, 899 F.3d 988, 1003 (9th Cir. 2018)."
        )
        d.write_wrapped(
            "<<b:4. New Request to Convert Rule 12(f) Strike into Rule 12(b)(6) Dismissal of "
            "Punitive Damages (Dkt. 33 at 10).>> Confronted with <<i:Whittlestone, Inc. v. "
            "Handi-Craft Co.>>, 618 F.3d 970, 974–75 (9th Cir. 2010), Defendants ask for the first "
            "time on reply that the Court treat punitive damages as a \"separate claim\" under "
            "Rule 12(b)(6), warranting a brief response under <<i:Saroya v. Univ. of the Pacific>>, "
            "503 F. Supp. 3d 986, 1000 (N.D. Cal. 2020), and <<i:Smith v. Wade>>, 461 U.S. 30, "
            "51–56 (1983)."
        )
        d.write_wrapped(
            "Granting leave causes no prejudice and no delay: the December 18, 2026 hearing is "
            f"nearly four weeks away, Exhibit A is attached now and limited to {page_word} pages, "
            "and Defendants themselves filed their Reply four days late without leave. As detailed "
            "in Plaintiff's Declaration under Civil L.R. 7-11(a), Plaintiff requested a stipulation "
            "from defense counsel on [DATE]; [defendants declined / no response was received]."
        )

        _section_heading(d, "IV. CONCLUSION")
        d.write_wrapped(
            "Plaintiff respectfully requests that the Court grant leave and deem Exhibit A filed "
            "of record, or, alternatively, decline to consider the new arguments and requests "
            "raised for the first time in Defendants' Reply (Dkt. 33)."
        )
        _plaintiff_signature(d, "Dated: November ___, 2026", respectfully=True)
        d.c.setTitle("Plaintiff's Administrative Motion for Leave to File Sur-Reply (3:26-cv-08271-CRB)")
        d.c.setAuthor("Brendan Ngwa Nforbi")
        d.save()

    return build_admin_motion


# ---------------------------------------------------------------------------
# Document 2 — Declaration ISO Administrative Motion (Civil L.R. 7-11(a))
# ---------------------------------------------------------------------------
def make_declaration_builder(surreply_pages: int):
    page_word = {1: "one", 2: "two", 3: "three", 4: "four", 5: "five"}.get(
        surreply_pages, str(surreply_pages)
    )

    def build_declaration(out_path: Path, page_total: int) -> None:
        footer = "Declaration of Brendan Ngwa Nforbi ISO Administrative Motion for Sur-Reply (3:26-cv-08271-CRB)"
        d = ClassicPleading(str(out_path), doc_title_footer=footer, page_total=page_total)
        right = [
            ("Case No. 3:26-cv-08271-CRB", True, False),
            ("", False, False),
            ("DECLARATION OF BRENDAN", True, False),
            ("NGWA NFORBI IN SUPPORT OF", True, False),
            ("ADMINISTRATIVE MOTION FOR", True, False),
            ("LEAVE TO FILE SUR-REPLY", True, False),
            ("[Civil L.R. 7-3(d), 7-11(a)]", False, False),
            ("", False, False),
            ("Judge: Hon. Charles R. Breyer", False, False),
            ("MTD Hearing: December 18, 2026", False, False),
            ("Time: 10:00 a.m. (Zoom Webinar)", False, False),
            ("Action Filed: August 10, 2026", False, False),
        ]
        _header_and_caption(d, right)

        d.write_wrapped("I, Brendan Ngwa Nforbi, declare as follows:", first_indent=0)
        d.write_wrapped(
            "1. I am the Plaintiff in the above-captioned action, appearing <<i:in propria persona>>. "
            "I have personal knowledge of the facts stated in this declaration and, if called as a "
            "witness, could and would competently testify to them."
        )
        d.write_wrapped(
            "2. I submit this declaration pursuant to Civil Local Rule 7-11(a) in support of "
            "Plaintiff's Administrative Motion for Leave to File a Sur-Reply to Defendants' Reply "
            "Brief in Support of Motion to Dismiss and Motion to Strike (Dkt. 33)."
        )
        d.write_wrapped(
            "3. On October 26, 2026, Defendants filed their Motion to Dismiss and Motion to Strike "
            "(Dkt. 22). On October 29, 2026, I filed my Opposition (Dkt. 27)."
        )
        d.write_wrapped(
            "4. On October 30, 2026, this action was reassigned to the Honorable Charles R. Breyer "
            "(Dkt. 29). The Reassignment Order expressly provided that existing briefing schedules "
            "remained unchanged. On November 3, 2026, the Clerk set the hearing on Defendants' "
            "Motion to Dismiss for December 18, 2026, at 10:00 a.m. via Zoom webinar (Dkt. 31)."
        )
        d.write_wrapped(
            "5. On November 20, 2026, at 4:40 p.m. PST—four days after the November 16, 2026 reply "
            "deadline under Civil L.R. 7-3(c) and Dkt. 29—Defendants filed their Reply Brief (Dkt. 33)."
        )
        d.write_wrapped(
            "6. Upon reviewing Defendants' Reply (Dkt. 33), I identified four new arguments, "
            "procedural requests, and record mischaracterizations not raised in Defendants' opening "
            "motion (Dkt. 22): (a) Defendants' new assertion that Rule 12(b)(6) allows drawing "
            "inferences against Plaintiff whenever an innocent explanation exists; (b) Defendants' "
            "new reliance on <<i:Airs Aromatics>> to bar conforming FAC ¶ 16 to the CHP dashcam "
            "recording; (c) Defendants' conversion of my Opposition's clarification of a CHP form "
            "field label into an affirmative factual concession of alcohol odor; and (d) Defendants' "
            "new request to convert their Rule 12(f) motion to strike punitive damages into a "
            "Rule 12(b)(6) motion to dismiss."
        )
        d.write_wrapped(
            "7. Pursuant to Civil Local Rule 7-11(a), on [November ___, 2026], I sent an e-mail to "
            "Deputy Attorney General Haiyang A. Li (Haiyang.Li@doj.ca.gov), counsel of record for "
            "Defendants, identifying those new reply issues and asking whether Defendants would "
            f"stipulate to leave for Plaintiff to file a short {page_word}-page sur-reply limited "
            "strictly to those points. I requested a response by Monday, November 23, 2026, at "
            "12:00 p.m. Pacific. A true and correct copy of that correspondence is attached hereto "
            "as <<b:Exhibit 1>>."
        )
        d.write_wrapped(
            "8. [COMPLETE AFTER MEET-AND-CONFER: On November ___, 2026, Mr. Li responded that "
            "Defendants oppose the request / As of ___ on November 23, 2026, I have received no "
            "response from defense counsel. Accordingly, a stipulation could not be obtained.]"
        )
        d.write_wrapped(
            f"9. Attached to the accompanying Administrative Motion as <<b:Exhibit A>> is Plaintiff's "
            f"proposed Sur-Reply, which is {page_word} pages in length and addresses solely the "
            "four new issues identified above."
        )
        d.write_wrapped(
            "I declare under penalty of perjury under the laws of the United States of America that "
            "the foregoing is true and correct.",
            first_indent=0,
        )
        _plaintiff_signature(
            d, "Executed on November ___, 2026, at Stockton, California.", respectfully=False
        )
        d.c.setTitle("Declaration of Brendan Ngwa Nforbi ISO Administrative Motion for Sur-Reply (3:26-cv-08271-CRB)")
        d.c.setAuthor("Brendan Ngwa Nforbi")
        d.save()

    return build_declaration


# ---------------------------------------------------------------------------
# Document 4 — [Proposed] Order Granting Leave to File Sur-Reply (1 page)
# ---------------------------------------------------------------------------
def build_proposed_order(out_path: Path, page_total: int) -> None:
    footer = "[Proposed] Order Granting Administrative Motion for Leave to File Sur-Reply (3:26-cv-08271-CRB)"
    d = ClassicPleading(str(out_path), doc_title_footer=footer, page_total=page_total)
    right = [
        ("Case No. 3:26-cv-08271-CRB", True, False),
        ("", False, False),
        ("[PROPOSED] ORDER GRANTING", True, False),
        ("PLAINTIFF'S ADMINISTRATIVE", True, False),
        ("MOTION FOR LEAVE TO FILE", True, False),
        ("SUR-REPLY", True, False),
        ("", False, False),
        ("Judge: Hon. Charles R. Breyer", False, False),
        ("MTD Hearing: December 18, 2026", False, False),
        ("Time: 10:00 a.m. (Zoom Webinar)", False, False),
    ]
    _header_and_caption(d, right, include_pro_se_block=False)

    d.write_wrapped(
        "Before the Court is Plaintiff Brendan Ngwa Nforbi's Administrative Motion pursuant to "
        "Civil Local Rules 7-3(d) and 7-11 for Leave to File a Sur-Reply in Opposition to "
        "Defendants' Motion to Dismiss and Motion to Strike (Dkts. 22, 33). Having considered "
        "the Administrative Motion, the accompanying Declaration of Brendan Ngwa Nforbi, the "
        "proposed Sur-Reply attached as Exhibit A, and any response thereto, and good cause "
        "appearing,"
    )
    d.write_wrapped(
        "<<b:IT IS HEREBY ORDERED>> that Plaintiff's Administrative Motion is <<b:GRANTED>>. "
        "The proposed Sur-Reply attached as Exhibit A to the Administrative Motion is deemed "
        "filed as of the date of this Order and will be considered in connection with "
        "Defendants' Motion to Dismiss and Motion to Strike (Dkt. 22), noticed for hearing on "
        "December 18, 2026, at 10:00 a.m."
    )
    d.write_wrapped("<<b:IT IS SO ORDERED.>>", first_indent=0)
    d.ensure_space(4)
    d.write_line("Dated: _______________________, 2026")
    d.write_line(SIG_LINE, right=True, right_margin_offset=SIG_OFFSET)
    d.write_line("HONORABLE CHARLES R. BREYER", bold=True, right=True, right_margin_offset=SIG_OFFSET)
    d.write_line("UNITED STATES DISTRICT JUDGE", right=True, right_margin_offset=SIG_OFFSET)

    d.c.setTitle("[Proposed] Order Granting Administrative Motion for Leave to File Sur-Reply (3:26-cv-08271-CRB)")
    d.c.setAuthor("Brendan Ngwa Nforbi")
    d.save()


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    p_surreply = OUT_DIR / "DRAFT - Exhibit A - Proposed Sur-Reply in Opposition to Motion to Dismiss (Dkt 33) (Nov 20 2026).pdf"
    p_motion = OUT_DIR / "DRAFT - Administrative Motion for Leave to File Sur-Reply (Dkt 33) (Nov 20 2026).pdf"
    p_decl = OUT_DIR / "DRAFT - Declaration ISO Administrative Motion for Leave to File Sur-Reply (Nov 20 2026).pdf"
    p_order = OUT_DIR / "DRAFT - Proposed Order Granting Leave to File Sur-Reply (Nov 20 2026).pdf"

    surreply_pages = _render_two_pass(p_surreply, build_surreply)
    motion_pages = _render_two_pass(p_motion, make_admin_motion_builder(surreply_pages))
    if motion_pages > 5:
        raise SystemExit(f"Administrative Motion exceeds Civil L.R. 7-11(a) 5-page cap: {motion_pages} pages")
    _render_two_pass(p_decl, make_declaration_builder(surreply_pages))
    _render_two_pass(p_order, build_proposed_order)


if __name__ == "__main__":
    main()
