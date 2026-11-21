#!/usr/bin/env python3
"""Matter 32 — Administrative Motion for Leave to File Sur-Reply Packet (Dkt. 33).

Renders four separate, CM/ECF-ready classic N.D. Cal. Civil L.R. 3-4 pleading-paper PDFs
dated November 23, 2026, with unsigned blank signature lines:
  1. Administrative Motion for Leave to File Sur-Reply (<= 5 pp., Civil L.R. 7-11(a))
  2. Declaration of Brendan Ngwa Nforbi ISO Administrative Motion (Civil L.R. 7-11(a))
  3. Exhibit A — [Proposed] Sur-Reply in Opposition to Motion to Dismiss and Motion to Strike
  4. [Proposed] Order Granting Administrative Motion for Leave to File Sur-Reply

Civil L.R. 3-4 compliance:
  * 8.5 x 11 letter, double vertical rule, 28 numbered lines per page.
  * Times-Roman 12 pt, double-spaced (24 pt), except caption, block quotes, and footnotes.
  * Lines 1-6 pro se identification, line 7 blank, court title commences on line 8.
  * Footer with document title and Page X of Y.
  * Unsigned blank signature lines dated November 23, 2026.

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


def _header_and_caption(
    d: ClassicPleading,
    right_caption: list[tuple[str, bool, bool]],
    include_pro_se_block: bool = True,
):
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
# Document 3 — Exhibit A: [Proposed] Sur-Reply (built first for page count)
# ---------------------------------------------------------------------------
def build_surreply(out_path: Path, page_total: int) -> None:
    footer = "Exhibit A — [Proposed] Sur-Reply ISO Opposition to Motion to Dismiss (3:26-cv-08271-CRB)"
    d = ClassicPleading(str(out_path), doc_title_footer=footer, page_total=page_total)
    right = [
        ("Case No. 3:26-cv-08271-CRB", True, False),
        ("", False, False),
        ("EXHIBIT A — [PROPOSED]", True, False),
        ("PLAINTIFF'S SUR-REPLY IN", True, False),
        ("OPPOSITION TO MOTION TO", True, False),
        ("DISMISS AND STRIKE", True, False),
        ("[Civil L.R. 7-3(d), 7-11]", False, False),
        ("", False, False),
        ("Judge: Hon. Charles R. Breyer", False, False),
        ("Hearing: December 18, 2026", False, False),
        ("Time: 10:00 a.m. (Zoom Webinar)", False, False),
        ("Action Filed: August 10, 2026", False, False),
    ]
    _header_and_caption(d, right)

    d.write_wrapped(
        "Plaintiff Brendan Ngwa Nforbi submits this Sur-Reply, limited strictly to five matters "
        "raised for the first time in Defendants' Reply (Dkt. 33)."
    )

    _section_heading(
        d,
        "I. THE NEW DOOR-ENTRY IMMUNITY THEORY ASSUMES UNPLEADED FACTS.",
    )
    d.write_wrapped(
        "The reply's immunity question assumes an \"unconscious\" driver. (Dkt. 33 at 4:28–5:3, "
        "8:5–8.) The FAC alleges a fatigued driver resting asleep in a normal posture in an "
        "undamaged car off the travel lanes. (FAC ¶¶ 11, 14, 16, 56.) The Court accepts those "
        "facts and draws inferences in Plaintiff's favor; where both sides offer plausible "
        "explanations, the claim survives. <<i:Starr v. Baca>>, 652 F.3d 1202, 1216 (9th Cir. "
        "2011)."
    )
    d.write_wrapped(
        "On those facts, the law was clearly established in November 2024. Opening a car door "
        "and entering the interior is a search requiring probable cause or another particularized "
        "justification. <<i:United States v. Ngumezi>>, 980 F.3d 1285, 1288–89 (9th Cir. 2020). "
        "The emergency-aid exception requires \"an objectively reasonable basis for believing\" "
        "someone inside needs immediate aid. <<i:Brigham City v. Stuart>>, 547 U.S. 398, 406 "
        "(2006); <<i:Hopkins v. Bonvicino>>, 573 F.3d 752, 763–64 (9th Cir. 2009). The reply "
        "distinguishes <<i:Hopkins>> by asserting the officers had \"no information,\" yet the "
        "FAC alleges what they saw through the windows with flashlights: an intact car and a "
        "person in a resting posture. (FAC ¶¶ 11, 14, 16.) Sleep in a parked car is not an "
        "emergency."
    )
    d.write_wrapped(
        "The reply also relies on half of Plaintiff's proposed amendment: that he did not respond "
        "to \"open the window\" before the door opened. (Dkt. 33 at 4:14–16.) The same proposed "
        "allegation states that the officers' knock woke Plaintiff, Officer Melano said \"open "
        "the window,\" and Melano opened the door three seconds later, \"before Plaintiff could "
        "comply,\" asking \"Are you okay?\" only after the door was open. (Dkt. 27 at 19:26–20:3 "
        "(recording at 00:56:40–00:56:43).) An officer speaking to an awake driver just roused by "
        "a knock who shows no sign of distress has no objective basis for emergency aid. On "
        "either version of the facts, the new immunity argument fails."
    )

    _section_heading(d, "II. AIRS AROMATICS DOES NOT BAR CONFORMING PARAGRAPH 16.")
    d.write_wrapped(
        "\"[T]here is nothing in the Federal Rules of Civil Procedure to prevent a party from "
        "filing successive pleadings that make inconsistent or even contradictory allegations.\" "
        "<<i:PAE Gov't Servs., Inc. v. MPRI, Inc.>>, 514 F.3d 856, 860 (9th Cir. 2007). Only a "
        "sham pleading is barred, and inconsistency alone does not show one. <<i:Id.>> at 858–60. "
        "The proposed correction conforms paragraph 16 to timestamps on the recording both sides "
        "possess—reflecting that the knock woke Plaintiff before Melano pulled the door open. It "
        "is not a change of theory to escape dismissal and does not change the result: on either "
        "version, the officers lacked an objective basis for emergency aid. Defendants cannot "
        "rely on the knock-and-command sequence to defend the entry (Dkt. 33 at 4:14–16) while "
        "arguing Plaintiff may not plead it accurately."
    )

    _section_heading(
        d,
        "III. LEAVE TO AMEND COUNT II IS WARRANTED ON SPECIFIC FACTS.",
    )
    d.write_wrapped(
        "The reply contends Plaintiff identified no specific fabricated statement. (Dkt. 33 at "
        "2:9–13.) Facts raised in opposition papers are considered when deciding leave to amend. "
        "<<i:Broam v. Bogan>>, 320 F.3d 1023, 1026 n.2 (9th Cir. 2003). Deliberate fabrication "
        "requires deliberate fabrication of evidence causing a deprivation of liberty. "
        "<<i:Spencer v. Peters>>, 857 F.3d 789, 798 (9th Cir. 2017). The FAC already pleads the "
        "facts an amended Count II would set out element by element:"
    )
    d.write_wrapped(
        "<<b:(a) Statements.>> Meza-Gonzalez's DS-367 and arrest report state that Plaintiff's "
        "speech was \"slurred,\" that he \"seemed very confused and disoriented,\" and that there "
        "was a \"strong distinct odor of an alcoholic beverage.\" (FAC ¶ 26(a)–(c).)",
        indent=24,
        first_indent=0,
    )
    d.write_wrapped(
        "<<b:(b) Contrary record.>> The recording captures extended coherent conversation—Plaintiff "
        "spelling his surname, discussing the car's mechanics, and correctly identifying his "
        "location—and over two hours of audio with no officer remarking on any odor. (<<i:Id.>> "
        "¶¶ 20, 26(a)–(c).)",
        indent=24,
        first_indent=0,
    )
    d.write_wrapped(
        "<<b:(c) Knowledge.>> Meza-Gonzalez was present for everything he described. (<<i:Id.>> "
        "¶¶ 40–41, 46.) <<i:See Chism v. Washington State>>, 661 F.3d 380, 388 (9th Cir. 2011).",
        indent=24,
        first_indent=0,
    )
    d.write_wrapped(
        "<<b:(d) Deprivation.>> The documents were used to obtain the blood-draw warrant (FAC "
        "¶¶ 29, 36(b)), supported the parole hold extending Plaintiff's confinement (<<i:id.>> "
        "¶ 36(a)), and formed the statutory basis for a one-year administrative suspension of his "
        "Class A commercial license (<<i:id.>> ¶¶ 36(d), 37). No criminal charge is required "
        "where fabrication causes the loss of a protected interest. <<i:Costanich v. Dep't of "
        "Soc. & Health Servs.>>, 627 F.3d 1101, 1108 (9th Cir. 2010).",
        indent=24,
        first_indent=0,
    )
    d.write_wrapped(
        "It is not \"absolutely clear\" amendment cannot cure any defect. <<i:Akhtar v. Mesa>>, "
        "698 F.3d 1202, 1212 (9th Cir. 2012). As to Count VI, Plaintiff does not seek leave to "
        "amend at this time and asks only that any dismissal be without prejudice; the refusal of "
        "the voluntary preliminary alcohol screening test remains part of Count III."
    )

    _section_heading(d, "IV. CORRECTING A FORM LABEL IS NOT A CONCESSION OF ODOR.")
    d.write_wrapped(
        "The reply treats Plaintiff's statement that a CHP form field refers to \"an odor of an "
        "alcoholic beverage, not to a container\" as support for probable cause and immunity. "
        "(Dkt. 33 at 6:7–9, 8:9–13.) Plaintiff corrected what the form says, not whether the "
        "entry was true; FAC ¶ 26(a) alleges it is false. \"[I]t is improper to assume the truth "
        "of an incorporated document\" to dispute well-pleaded facts. <<i:Khoja v. Orexigen "
        "Therapeutics, Inc.>>, 899 F.3d 988, 1003 (9th Cir. 2018)."
    )

    _section_heading(d, "V. THE PUNITIVE-DAMAGES PRAYER IS NOT A CLAIM.")
    d.write_wrapped(
        "Recasting the Rule 12(f) strike as a Rule 12(b)(6) dismissal is new and may be "
        "disregarded. <<i:Zamani v. Carnes>>, 491 F.3d 990, 997 (9th Cir. 2007). "
        "<<i:Whittlestone, Inc. v. Handi-Craft Co.>>, 618 F.3d 970, 974–75 (9th Cir. 2010), "
        "bars the same result under another label. A prayer is a \"demand for the relief "
        "sought,\" Fed. R. Civ. P. 8(a)(3), not a claim; its availability follows the surviving "
        "claims. Under § 1983, punitive damages require \"reckless or callous indifference to "
        "the federally protected rights of others.\" <<i:Smith v. Wade>>, 461 U.S. 30, 56 "
        "(1983). The reply's \"Both cannot be true\" point fails: speculating aloud that a cup "
        "holds alcohol does not justify entry, <<i:Ngumezi>>, 980 F.3d at 1288–89, and asking "
        "\"Are you okay?\" afterward cannot validate it."
    )

    _section_heading(d, "VI. CONCLUSION")
    d.write_wrapped(
        "The Court should disregard or reject the reply's new arguments, deny dismissal of Counts "
        "I, III, IV, and V and the motion to strike, dismiss Count II with leave to amend and "
        "Count VI without prejudice, and grant leave to amend as to any other defect."
    )
    _plaintiff_signature(d, "Dated: November 23, 2026", respectfully=True)
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
            ("SUR-REPLY TO DEFENDANTS'", True, False),
            ("REPLY (DKT. 33)", True, False),
            ("[Civil L.R. 7-3(d), 7-11]", False, False),
            ("", False, False),
            ("Judge: Hon. Charles R. Breyer", False, False),
            ("Hearing: December 18, 2026", False, False),
            ("Time: 10:00 a.m. (Zoom Webinar)", False, False),
            ("Action Filed: August 10, 2026", False, False),
        ]
        _header_and_caption(d, right)

        _center_bold(d, "ADMINISTRATIVE MOTION")
        d.write_wrapped(
            f"Under Civil Local Rules 7-3(d) and 7-11, Plaintiff Brendan Ngwa Nforbi, appearing "
            f"<<i:in propria persona>>, moves for leave to file the {page_word}-page sur-reply "
            f"attached as <<b:Exhibit A>>. It responds solely to five matters that Defendants "
            f"raised for the first time in their Reply in Support of Motion to Dismiss and Motion "
            f"to Strike (Dkt. 33). This Motion is supported by the Memorandum below, the "
            f"accompanying Declaration under Civil L.R. 7-11(a), Exhibit A, and the [Proposed] "
            f"Order submitted concurrently herewith."
        )

        _center_bold(d, "MEMORANDUM OF POINTS AND AUTHORITIES")
        _section_heading(d, "I. PROCEDURAL BACKGROUND")
        d.write_wrapped(
            "Defendants filed their Motion to Dismiss the First Amended Complaint and Motion to "
            "Strike on October 26, 2026 (Dkt. 22). Plaintiff filed his Opposition on October 29, "
            "2026 (Dkt. 27). On October 30, 2026, the action was reassigned to this Court with "
            "existing briefing schedules left unchanged (Dkt. 29), and on November 3, 2026, the "
            "Clerk set the hearing for Friday, December 18, 2026, at 10:00 a.m. by Zoom webinar "
            "(Dkt. 31)."
        )
        d.write_wrapped(
            "Under Civil L.R. 7-3(a) and (c), the opposition deadline was November 9, 2026, and "
            "the reply was due November 16, 2026. Defendants filed their Reply on November 20, "
            "2026—four days late, without a stipulation or order under Civil L.R. 6-2 or 6-3 "
            "(Dkt. 33)—with a caption listing Saturday, \"December 19, 2026,\" in \"Courtroom 4\" "
            "and a superseded magistrate suffix in the footer. (<<i:Id.>> at 1.) Plaintiff does "
            "not ask to strike the Reply; he requests a brief opportunity to answer what is new."
        )

        _section_heading(d, "II. LEGAL STANDARD")
        d.write_wrapped(
            "Once a reply is filed, no additional memoranda may be filed without prior Court "
            "approval. Civil L.R. 7-3(d); <<i:Dutta v. State Farm Mut. Auto. Ins. Co.>>, 895 F.3d "
            "1166, 1171–72 (9th Cir. 2018). A court \"need not consider arguments raised for the "
            "first time in a reply brief.\" <<i:Zamani v. Carnes>>, 491 F.3d 990, 997 (9th Cir. "
            "2007). Where the Court may consider new reply matter, good cause exists to permit a "
            "short sur-reply so the opposing party has a fair opportunity to respond."
        )

        _section_heading(d, "III. THE REPLY RAISES FIVE NEW MATTERS")
        d.write_wrapped(
            "<<b:1. Qualified immunity for opening the car door (Count IV).>> The opening motion's "
            "immunity argument addressed only probable cause to search and arrest. (Dkt. 22 at "
            "12:7–13:21; Dkt. 27 at 17:24–27.) The reply argues for the first time that Defendants "
            "are immune for opening the door of a car occupied by an \"unconscious\" driver. "
            "(Dkt. 33 at 4:28–5:3, 8:5–8.)",
            indent=18,
            first_indent=0,
        )
        d.write_wrapped(
            "<<b:2. New authority to bar amendment.>> The reply invokes <<i:Airs Aromatics, LLC "
            "v. Victoria's Secret Stores Brand Mgmt., Inc.>>, 744 F.3d 595, 600 (9th Cir. 2014)—"
            "uncited in the opening motion—to argue Plaintiff may not conform FAC ¶ 16 to the "
            "recording. (Dkt. 33 at 5:4–12, 9:21–24.)",
            indent=18,
            first_indent=0,
        )
        d.write_wrapped(
            "<<b:3. New basis to dismiss Counts II and VI with prejudice.>> The reply argues "
            "Plaintiff's limited non-opposition requires denial of leave to amend, citing new "
            "authority, <<i:Argueta v. Walgreens Co.>>, 760 F. Supp. 3d 1028, 1033 (E.D. Cal. "
            "2024). (Dkt. 33 at 2:1–13, 9:25–10:4.)",
            indent=18,
            first_indent=0,
        )
        d.write_wrapped(
            "<<b:4. Use of a form-label correction as an \"odor\" concession.>> The reply treats "
            "Plaintiff's correction of what a CHP form field says as factual support for probable "
            "cause and immunity. (Dkt. 33 at 6:7–9, 8:9–13.)",
            indent=18,
            first_indent=0,
        )
        d.write_wrapped(
            "<<b:5. New request for Rule 12(b)(6) dismissal of punitive damages.>> For the first "
            "time on reply, Defendants ask the Court to treat the punitive-damages prayer \"as a "
            "separate claim within the scope of\" Rule 12(b)(6). (Dkt. 33 at 10:5–12.)",
            indent=18,
            first_indent=0,
        )
        d.write_wrapped(
            "Exhibit A addresses only these five matters. Granting leave causes no prejudice or "
            "delay: the hearing is nearly four weeks away, Exhibit A is attached now, and the "
            "reply itself was filed late. As stated in the accompanying Declaration under Civil "
            "L.R. 7-11(a), Plaintiff requested a stipulation from defense counsel and could not "
            "obtain one."
        )

        _section_heading(d, "IV. CONCLUSION")
        d.write_wrapped(
            "Plaintiff respectfully requests that the Court grant leave and deem Exhibit A filed, "
            "or, alternatively, disregard the arguments and requests raised for the first time in "
            "Defendants' untimely Reply (Dkt. 33)."
        )
        _plaintiff_signature(d, "Dated: November 23, 2026", respectfully=True)
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
            ("Hearing: December 18, 2026", False, False),
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
            "2. I submit this declaration pursuant to Civil Local Rule 7-11(a) in support of my "
            "Administrative Motion for Leave to File a Sur-Reply to Defendants' Reply Brief (Dkt. 33)."
        )
        d.write_wrapped(
            "3. Defendants filed their Motion to Dismiss and Motion to Strike on October 26, 2026 "
            "(Dkt. 22). I filed my Opposition on October 29, 2026 (Dkt. 27). On October 30, 2026, "
            "this action was reassigned to Judge Breyer with existing briefing schedules unchanged "
            "(Dkt. 29). On November 3, 2026, the Clerk set the motion hearing for December 18, 2026, "
            "at 10:00 a.m. by Zoom webinar (Dkt. 31)."
        )
        d.write_wrapped(
            "4. On November 20, 2026, Defendants filed their Reply (Dkt. 33)—four days after the "
            "November 16, 2026 reply deadline under Civil L.R. 7-3(c) and Dkt. 29."
        )
        d.write_wrapped(
            "5. Pursuant to Civil Local Rule 7-11(a), on [November ___, 2026], I e-mailed Deputy "
            "Attorney General Haiyang A. Li (Haiyang.Li@doj.ca.gov), counsel for Defendants, "
            "identified the five new matters in the Reply, and asked whether Defendants would "
            f"stipulate to my filing a short {page_word}-page sur-reply limited strictly to those "
            "matters. I requested a response by 5:00 p.m. Pacific on Monday, November 23, 2026. A "
            "true and correct copy of my e-mail is attached hereto as <<b:Exhibit 1>>."
        )
        d.write_wrapped(
            "6. [COMPLETE ONE: On November ___, 2026, counsel responded that Defendants do not "
            "agree. / As of ___ on November 23, 2026, I had received no response.] Accordingly, a "
            "stipulation could not be obtained."
        )
        d.write_wrapped(
            f"7. Attached to the accompanying Administrative Motion as <<b:Exhibit A>> is my "
            f"proposed {page_word}-page Sur-Reply, which addresses solely the five new matters "
            "identified in the Motion."
        )
        d.write_wrapped(
            "I declare under penalty of perjury under the laws of the United States of America that "
            "the foregoing is true and correct.",
            first_indent=0,
        )
        _plaintiff_signature(
            d, "Executed on November 23, 2026, at Stockton, California.", respectfully=False
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
        ("[Civil L.R. 7-3(d), 7-11]", False, False),
        ("", False, False),
        ("Judge: Hon. Charles R. Breyer", False, False),
        ("Hearing: December 18, 2026", False, False),
        ("Time: 10:00 a.m. (Zoom Webinar)", False, False),
    ]
    _header_and_caption(d, right, include_pro_se_block=False)

    d.write_wrapped(
        "Plaintiff Brendan Ngwa Nforbi's Administrative Motion for Leave to File a Sur-Reply to "
        "Defendants' Reply in Support of Motion to Dismiss and Motion to Strike (Dkt. 33) came "
        "before the Court under Civil Local Rules 7-3(d) and 7-11. Having considered the Motion, "
        "the supporting Declaration of Brendan Ngwa Nforbi, the proposed Sur-Reply attached as "
        "Exhibit A, and any response thereto, and good cause appearing,"
    )
    d.write_wrapped(
        "<<b:IT IS HEREBY ORDERED>> that the Administrative Motion is <<b:GRANTED>>. The "
        "Sur-Reply attached as Exhibit A to the Motion is deemed filed as of the date of this "
        "Order and will be considered in connection with Defendants' Motion to Dismiss and Motion "
        "to Strike (Dkt. 22), set for hearing on December 18, 2026, at 10:00 a.m."
    )
    d.write_wrapped("<<b:IT IS SO ORDERED.>>", first_indent=0)
    d.write_line("Dated: _______________________, 2026")
    d.blank_line()
    d.write_line(SIG_LINE, right=True, right_margin_offset=SIG_OFFSET)
    d.write_line("HONORABLE CHARLES R. BREYER", bold=True, right=True, right_margin_offset=SIG_OFFSET)
    d.write_line("UNITED STATES DISTRICT JUDGE", right=True, right_margin_offset=SIG_OFFSET)

    d.c.setTitle("[Proposed] Order Granting Administrative Motion for Leave to File Sur-Reply (3:26-cv-08271-CRB)")
    d.c.setAuthor("Brendan Ngwa Nforbi")
    d.save()


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    p_surreply = OUT_DIR / "DRAFT - Exhibit A - Proposed Sur-Reply in Opposition to Motion to Dismiss (Dkt 33) (Nov 23 2026).pdf"
    p_motion = OUT_DIR / "DRAFT - Administrative Motion for Leave to File Sur-Reply (Dkt 33) (Nov 23 2026).pdf"
    p_decl = OUT_DIR / "DRAFT - Declaration ISO Administrative Motion for Leave to File Sur-Reply (Nov 23 2026).pdf"
    p_order = OUT_DIR / "DRAFT - Proposed Order Granting Leave to File Sur-Reply (Nov 23 2026).pdf"

    surreply_pages = _render_two_pass(p_surreply, build_surreply)
    motion_pages = _render_two_pass(p_motion, make_admin_motion_builder(surreply_pages))
    if motion_pages > 5:
        raise SystemExit(f"Administrative Motion exceeds Civil L.R. 7-11(a) 5-page cap: {motion_pages} pages")
    _render_two_pass(p_decl, make_declaration_builder(surreply_pages))
    _render_two_pass(p_order, build_proposed_order)


if __name__ == "__main__":
    main()
