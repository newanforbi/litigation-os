#!/usr/bin/env python3
"""Matter 29 — Civil L.R. 7-11 administrative motion for leave to appear by
Zoom webinar at the November 18, 2026 hearing on Amazon's Dkt. 19 motion to
dismiss. Newanforbi v. Amazon.com Services, LLC, et al., N.D. Cal.
No. 4:26-cv-09249-ASK (Hon. Ajay S. Krishnan).

Builds, on the portfolio pleading paper (lib/pleading_paper.py):
  1. Administrative motion
  2. Declaration of Brendan Ngehsi Newanforbi (Civil L.R. 7-11(a): why no
     stipulation was obtained)
  3. [Proposed] order
  4. Combined filing packet (motion + declaration + proposed order)

Signature: the 20%-stretched signature Plaintiff supplied on Nov. 8, 2026
(internal/assets/signature/brendan-newanforbi-signature-stretched-120.png).

    python3 internal/scripts/matter29-zoom-appearance-admin-motion.py \\
        --out-dir <dir> [--date "November 9, 2026"] [--place "San Jose, California"]

Not filed until Plaintiff files it. Served on defense counsel through CM/ECF.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR / "lib"))
from pleading_paper import CONTENT_LEFT, PleadingPaper  # noqa: E402
from pypdf import PdfWriter  # noqa: E402

ROOT = SCRIPT_DIR.parents[1]
SIGNATURE = ROOT / "internal/assets/signature/brendan-newanforbi-signature-stretched-120.png"

CASE_NO = "4:26-cv-09249-ASK"
CASE_FILE = CASE_NO.replace(":", "-")
JUDGE = "Hon. Ajay S. Krishnan"
DEFAULT_DATE = "November 9, 2026"
DEFAULT_PLACE = "San Jose, California"

PLAINTIFF_BLOCK = [
    ("BRENDAN NGEHSI NEWANFORBI", "Times-Bold", 12),
    ("Plaintiff, In Propria Persona", "Times-Roman", 12),
    ("1455 Cat Tail Drive", "Times-Roman", 12),
    ("Stockton, CA 95204", "Times-Roman", 12),
    ("Telephone: (209) 801-4442", "Times-Roman", 12),
    ("E-mail: bnn.cdl@gmail.com", "Times-Roman", 12),
]
COURT_LINE1 = "UNITED STATES DISTRICT COURT"
COURT_LINE2 = "NORTHERN DISTRICT OF CALIFORNIA"

CAPTION_LEFT = [
    ("BRENDAN NGEHSI NEWANFORBI,", True, False),
    ("", False, False),
    ("                          Plaintiff,", False, False),
    ("", False, False),
    ("       v.", False, False),
    ("", False, False),
    ("AMAZON.COM SERVICES, LLC;", True, False),
    ("ACCURATE BACKGROUND LLC; and", True, False),
    ("DOES 1-10, inclusive,", True, False),
    ("", False, False),
    ("                          Defendants.", False, False),
]

SIGNOFF_NAME = "BRENDAN NGEHSI NEWANFORBI"
SIGNOFF_ROLE = "Plaintiff, In Propria Persona"
SIG_LINE = "___________________________________"

MOTION_FOOTER = "ADMIN. MOTION — ZOOM APPEARANCE (DKT. 19) -- NEWANFORBI v. AMAZON"
DECL_FOOTER = "DECL. ISO ADMIN. MOTION — ZOOM APPEARANCE (DKT. 19) -- NEWANFORBI v. AMAZON"
ORDER_FOOTER = "[PROPOSED] ORDER — ZOOM APPEARANCE (DKT. 19) -- NEWANFORBI v. AMAZON"


def _caption_right(title_lines: list[str], hearing: bool = True) -> list[tuple[str, bool, bool]]:
    rows: list[tuple[str, bool, bool]] = [(f"Case No. {CASE_NO}", True, False), ("", False, False)]
    rows += [(t, True, False) for t in title_lines]
    rows.append(("", False, False))
    rows.append(("[Civil L.R. 7-11]", False, False))
    if hearing:
        rows += [
            ("Hearing: Nov. 18, 2026, 1:30 p.m.", False, False),
            ("Courtroom 4, 3rd Floor", False, False),
            ("1301 Clay St., Oakland", False, False),
        ]
    rows.append((f"Judge: {JUDGE}", False, False))
    return rows


MOTION_CAPTION_RIGHT = _caption_right([
    "ADMINISTRATIVE MOTION FOR",
    "LEAVE TO APPEAR BY ZOOM",
    "WEBINAR AT THE NOVEMBER 18,",
    "2026 HEARING ON DKT. 19",
])
DECL_CAPTION_RIGHT = _caption_right([
    "DECLARATION OF BRENDAN NGEHSI",
    "NEWANFORBI IN SUPPORT OF",
    "ADMINISTRATIVE MOTION FOR",
    "LEAVE TO APPEAR BY ZOOM",
    "WEBINAR (DKT. 19 HEARING)",
])
ORDER_CAPTION_RIGHT = _caption_right([
    "[PROPOSED] ORDER GRANTING",
    "PLAINTIFF'S ADMINISTRATIVE",
    "MOTION FOR LEAVE TO APPEAR",
    "BY ZOOM WEBINAR AT THE",
    "NOVEMBER 18, 2026 HEARING",
    "ON DKT. 19",
], hearing=False)

MOTION_CONTENT = [
    ("SUBHEAD", "TO THE COURT AND TO AMAZON.COM SERVICES, LLC, AND ACCURATE\nBACKGROUND LLC, THROUGH COUNSEL:"),
    ("PARA", "Plaintiff Brendan Ngehsi Newanforbi, appearing in propria persona, moves under Civil "
             "Local Rule 7-11 and this Court's Civil Standing Order (August 20, 2026) for leave to appear "
             "by Zoom webinar at the hearing on Defendant Amazon.com Services, LLC's Motion to Dismiss "
             "(Dkt. 19), set for Wednesday, November 18, 2026, at 1:30 p.m. in Courtroom 4, 3rd Floor, "
             "1301 Clay Street, Oakland, California."),
    ("HEADER", "I.\nREQUEST"),
    ("PARA", "The Standing Order provides that, unless the Court orders otherwise, all law and motion "
             "hearings except discovery disputes will be conducted in person, and that a request for a "
             "Zoom webinar appearance must be made at least three business days before the scheduled "
             "hearing and will be granted only upon a showing of good cause. This request is made more "
             "than three business days before November 18, 2026."),
    ("HEADER", "II.\nGOOD CAUSE"),
    ("PARA", "Plaintiff currently relies on public transportation to reach the Oakland courthouse. A "
             "service delay or missed connection on the day of the hearing could prevent Plaintiff from "
             "arriving by the scheduled 1:30 p.m. start. Appearing by Zoom would allow Plaintiff to "
             "participate on time without delaying the hearing or affecting how Defendants appear. "
             "(Newanforbi Decl. ¶ 2.)"),
    ("HEADER", "III.\nRELIEF REQUESTED"),
    ("PARA", "Plaintiff respectfully asks the Court to permit Plaintiff to appear by Zoom webinar at the "
             "November 18, 2026, 1:30 p.m. hearing on Dkt. 19, and to direct the courtroom deputy to "
             "provide Plaintiff the Zoom webinar credentials for that hearing."),
    ("HEADER", "IV.\nCIVIL L.R. 7-11 STATEMENT"),
    ("PARA", "Plaintiff is filing this motion electronically through CM/ECF. Counsel of record who are "
             "registered CM/ECF users will be served through the Notice of Electronic Filing. As required "
             "by Civil Local Rule 7-11(a), this motion is accompanied by a proposed order and by the "
             "Declaration of Brendan Ngehsi Newanforbi explaining why a stipulation was not obtained. "
             "Plaintiff does not seek to change the hearing date or to limit how Defendants may appear."),
]

DECL_CONTENT = [
    ("PARA", "I, Brendan Ngehsi Newanforbi, declare:"),
    ("PARA", "1. I am the Plaintiff in this action, appearing in propria persona. I have personal "
             "knowledge of the facts stated in this declaration and, if called as a witness, could and "
             "would testify competently to them."),
    ("PARA", "2. I currently rely on public transportation to reach the Ronald V. Dellums Federal "
             "Building, 1301 Clay Street, Oakland, California. A service delay or missed connection on "
             "November 18, 2026 could prevent me from arriving in Courtroom 4 by the scheduled 1:30 p.m. "
             "start of the hearing on Defendant Amazon.com Services, LLC's Motion to Dismiss (Dkt. 19). "
             "Appearing by Zoom webinar would allow me to participate on time without delaying the "
             "hearing."),
    ("PARA", "3. I did not seek a stipulation from Defendants before filing this motion. The motion "
             "concerns only the manner of my own appearance at the November 18, 2026 hearing; it does "
             "not change the hearing date, the briefing, or how any Defendant may appear, and it does "
             "not affect any Defendant's rights. Obtaining a written stipulation would have required the "
             "signatures of counsel from two separate law firms, and an automatic email reply I received "
             "on November 6, 2026 from Jasmine J. Stanzick, counsel for Defendant Accurate Background, "
             "LLC, states that she is out of the office through November 17, 2026, the day before the "
             "hearing."),
    ("PARA", "4. Defendants will receive notice of this motion through CM/ECF and may file an opposition "
             "within four days under Civil Local Rule 7-11(b), which allows the Court to resolve the motion "
             "before the November 18, 2026 hearing. Proceeding without a stipulation therefore does not "
             "deprive any Defendant of an opportunity to be heard."),
    ("PARA", "5. I do not seek to change the hearing date or to limit how any Defendant may appear."),
    # The perjury clause and execution line are written with the signature block (build_declaration)
    # so they can never be separated from it by a page break.
]

PERJURY = ("I declare under penalty of perjury under the laws of the United States of America that the "
           "foregoing is true and correct. Executed on {date}, at {place}.")

ORDER_CONTENT = [
    ("PARA", "Plaintiff Brendan Ngehsi Newanforbi's Administrative Motion for Leave to Appear by Zoom "
             "Webinar at the November 18, 2026 hearing on Defendant Amazon.com Services, LLC's Motion to "
             "Dismiss (Dkt. 19) came on for consideration."),
    ("PARA", "Good cause appearing, IT IS HEREBY ORDERED that:"),
    ("LIST_ITEM", "1. The Administrative Motion is GRANTED."),
    ("LIST_ITEM", "2. Plaintiff may appear by Zoom webinar at the hearing on Dkt. 19 set for "
                  "November 18, 2026, at 1:30 p.m."),
    ("LIST_ITEM", "3. The courtroom deputy shall provide Plaintiff the Zoom webinar credentials for "
                  "that hearing."),
    ("PARA", "IT IS SO ORDERED."),
]


def _png_size(path: Path) -> tuple[int, int]:
    import struct
    with open(path, "rb") as fh:
        fh.read(16)
        return struct.unpack(">II", fh.read(8))


def _header_block(d: PleadingPaper, right_caption: list) -> None:
    c = d.c
    y0 = d._line_y(0)
    for i, (txt, fn, sz) in enumerate(PLAINTIFF_BLOCK):
        c.setFont(fn, sz)
        c.drawString(CONTENT_LEFT, y0 - i * 15, txt)
    d.current_line = 4
    d.blank_line()
    d.write_line(COURT_LINE1, bold=True, center=True)
    d.write_line(COURT_LINE2, bold=True, center=True)
    d.blank_line()
    d.draw_caption_block(CAPTION_LEFT, right_caption, caption_size=9, tight_lh=12, boxed=True)
    d.blank_line()


def _render_body(d: PleadingPaper, content: list[tuple[str, str]]) -> None:
    for kind, text in content:
        if kind == "HEADER":
            lines = text.split("\n")
            d.ensure_space(len(lines) + 2)
            for line in lines:
                d.write_line(line, bold=True, center=True)
            d.blank_line()
        elif kind == "SUBHEAD":
            lines = text.split("\n")
            d.ensure_space(len(lines) + 2)
            for line in lines:
                d.write_line(line, bold=True)
            d.blank_line()
        elif kind == "PARA":
            d.write_wrapped(text, first_indent=36)
            d.blank_line()
        elif kind == "LIST_ITEM":
            d.write_wrapped(text, indent=18, first_indent=0)
            d.blank_line()
        else:
            raise ValueError(kind)


def _signature(d: PleadingPaper, date: str | None, *, closer: bool = True) -> None:
    d.ensure_space(10 if (date or closer) else 6)
    if date:
        d.write_line(f"Dated: {date}")
        d.blank_line()
    if closer:
        d.write_line("Respectfully submitted,", right=True, right_margin_offset=20)
    w, h = _png_size(SIGNATURE)
    d.draw_signature_image(str(SIGNATURE), w, h, SIG_LINE, width=185, x_offset=0,
                           height_scale=1.0)
    d.write_line(SIG_LINE, right=True, right_margin_offset=20)
    d.write_line(SIGNOFF_NAME, right=True, right_margin_offset=20)
    d.write_line(SIGNOFF_ROLE, right=True, right_margin_offset=20)


def build_motion(out: Path, date: str) -> Path:
    d = PleadingPaper(str(out), doc_title_footer=MOTION_FOOTER)
    _header_block(d, MOTION_CAPTION_RIGHT)
    _render_body(d, MOTION_CONTENT)
    _signature(d, date)
    d.save()
    return out


def build_declaration(out: Path, date: str, place: str) -> Path:
    d = PleadingPaper(str(out), doc_title_footer=DECL_FOOTER)
    _header_block(d, DECL_CAPTION_RIGHT)
    _render_body(d, DECL_CONTENT)
    d.ensure_space(9)  # perjury clause (2) + blank + signature block (6) stay on one page
    d.write_wrapped(PERJURY.format(date=date, place=place), first_indent=36)
    d.blank_line()
    _signature(d, None, closer=False)
    d.save()
    return out


def build_order(out: Path) -> Path:
    d = PleadingPaper(str(out), doc_title_footer=ORDER_FOOTER)
    _header_block(d, ORDER_CAPTION_RIGHT)
    _render_body(d, ORDER_CONTENT)
    d.ensure_space(6)
    d.write_line("Dated: _______________, 2026")
    d.blank_line()
    d.blank_line()
    d.write_line("___________________________________________")
    d.write_line("HON. AJAY S. KRISHNAN")
    d.write_line("United States Magistrate Judge")
    d.save()
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--date", default=DEFAULT_DATE)
    ap.add_argument("--place", default=DEFAULT_PLACE)
    a = ap.parse_args()
    if not SIGNATURE.is_file():
        raise SystemExit(f"Missing signature: {SIGNATURE}")
    od = Path(a.out_dir)
    od.mkdir(parents=True, exist_ok=True)
    m = build_motion(od / f"Administrative Motion - Zoom Appearance (Dkt 19) - {CASE_FILE}.pdf", a.date)
    dl = build_declaration(od / f"Declaration ISO Admin Motion - Zoom Appearance - {CASE_FILE}.pdf", a.date, a.place)
    o = build_order(od / f"Proposed Order - Zoom Appearance - {CASE_FILE}.pdf")
    w = PdfWriter()
    for p in (m, dl, o):
        w.append(str(p))
    packet = od / f"FILING PACKET - Admin Motion + Declaration + Proposed Order - Zoom Appearance - {CASE_FILE}.pdf"
    w.write(str(packet))
    for p in (m, dl, o, packet):
        print(p)


if __name__ == "__main__":
    main()
