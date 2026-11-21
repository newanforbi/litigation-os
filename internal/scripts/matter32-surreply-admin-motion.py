#!/usr/bin/env python3
"""Matter 32 — Civil L.R. 7-11 administrative motion for leave to file a
sur-reply to Defendants' reply (Dkt. 33) in Nforbi v. Meza-Gonzalez,
N.D. Cal. No. 3:26-cv-08271-CRB.

Builds four papers on pleading paper with the universal signature image:
  1. Administrative motion
  2. Exhibit A — [Proposed] Sur-Reply
  3. Declaration (Civil L.R. 7-11(a))
  4. [Proposed] Order
plus a combined filing packet (1 + 2 + 3).

    python3 internal/scripts/matter32-surreply-admin-motion.py \\
        [--date "November 24, 2026"] [--place "Stockton, California"]

DRAFT until Plaintiff reviews it. Bracketed items in the declaration are
completed after the stipulation request to counsel is answered or lapses.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR / "lib"))
from pleading_paper_ndcal import NDCalPaper  # noqa: E402
from pypdf import PdfReader, PdfWriter  # noqa: E402
from signature_stamp import SIGNATURE_NATIVE_PX, SIGNATURE_PATH  # noqa: E402

ROOT = SCRIPT_DIR.parents[1]
OUT_DIR = ROOT / "documents/matter-32/ndcal"

CASE_NO = "3:26-cv-08271-CRB"
DEFAULT_DATE = "November ___, 2026"
DEFAULT_PLACE = "Stockton, California"

CAPTION = "NFORBI v. MEZA-GONZALEZ, et al."


# ---------------------------------------------------------------- motion
MOTION_CAPTION = ([
    "PLAINTIFF'S ADMINISTRATIVE",
    "MOTION FOR LEAVE TO FILE",
    "SUR-REPLY TO DEFENDANTS'",
    "REPLY (DKT. 33)",
])

MOTION = [
    ("HEADER", "ADMINISTRATIVE MOTION"),
    ("PARA",
     "Under Civil Local Rules 7-3(d) and 7-11, Plaintiff Brendan Ngwa Nforbi, "
     "appearing in propria persona, moves for leave to file the sur-reply "
     "attached as Exhibit A. It responds only to five matters that Defendants "
     "raised for the first time in their Reply in Support of Motion to Dismiss "
     "and Motion to Strike (Dkt. 33). The motion is supported by this "
     "memorandum, the accompanying declaration, Exhibit A, and the proposed "
     "order filed with it."),
    ("HEADER", "MEMORANDUM OF POINTS AND AUTHORITIES"),
    ("SUBHEAD", "I.  PROCEDURAL BACKGROUND"),
    ("PARA",
     "Defendants filed their motion to dismiss the First Amended Complaint and "
     "to strike on October 26, 2026 (Dkt. 22). Plaintiff filed his opposition "
     "on October 29, 2026 (Dkt. 27). The case was reassigned to this Court on "
     "October 30, 2026, with existing briefing schedules left unchanged "
     "(Dkt. 29), and the motion was set for hearing on Friday, December 18, "
     "2026, at 10:00 a.m. by Zoom webinar (Dkt. 31)."),
    ("PARA",
     "Under Civil L.R. 7-3(a) and (c), the opposition was due November 9, 2026, "
     "and the reply was due November 16, 2026. Defendants filed their reply on "
     "November 20, 2026, four days late, without a stipulation or an order "
     "under Civil L.R. 6-2 or 6-3. (Dkt. 33.) The reply's caption also lists "
     "the hearing as Saturday, “December 19, 2026,” in "
     "“Courtroom 4.” (Id. at 1.) Plaintiff does not ask the Court to "
     "strike the reply. He asks for a short opportunity to answer what is new "
     "in it."),
    ("SUBHEAD", "II.  LEGAL STANDARD"),
    ("PARA",
     "Once a reply is filed, no additional memoranda may be filed without prior "
     "Court approval. Civil L.R. 7-3(d). A court “need not consider "
     "arguments raised for the first time in a reply brief.” "
     "<<i:Zamani v. Carnes>>, 491 F.3d 990, 997 (9th Cir. 2007). If the Court "
     "is inclined to consider new reply arguments, the opposing party should "
     "have a fair opportunity to respond to them."),
    ("SUBHEAD", "III.  THE REPLY RAISES FIVE NEW MATTERS"),
    ("LIST_ITEM",
     "1.  <<b:Qualified immunity for opening the car door (Count IV).>> The "
     "motion's immunity argument addressed only probable cause to search and "
     "arrest. (Dkt. 22 at 12:7–13:21.) The opposition pointed that out. "
     "(Dkt. 27 at 17:24–27.) The reply argues for the first time that "
     "Defendants are immune for opening the door of a car occupied by an "
     "“unconscious” driver. (Dkt. 33 at 4:28–5:3, 8:5–8.)"),
    ("LIST_ITEM",
     "2.  <<b:New authority to bar amendment.>> The reply invokes "
     "<<i:Airs Aromatics, LLC v. Victoria's Secret Stores Brand Mgmt., Inc.>>, "
     "744 F.3d 595, 600 (9th Cir. 2014), which the motion did not cite, to "
     "argue that Plaintiff may not conform FAC ¶ 16 to the recording. "
     "(Dkt. 33 at 5:4–12, 9:21–24.)"),
    ("LIST_ITEM",
     "3.  <<b:A new basis for dismissing Counts II and VI with prejudice.>> The "
     "reply argues that Plaintiff's limited non-opposition requires denial of "
     "leave to amend, citing new authority, <<i:Argueta v. Walgreens Co.>>, "
     "760 F. Supp. 3d 1028, 1033 (2024). (Dkt. 33 at 2:1–13, "
     "9:25–10:4.)"),
    ("LIST_ITEM",
     "4.  <<b:Use of a form-label correction as an “odor” "
     "concession.>> The reply treats the opposition's correction of what a "
     "CHP form field says as support for probable cause and immunity. "
     "(Dkt. 33 at 6:7–9, 8:9–13.)"),
    ("LIST_ITEM",
     "5.  <<b:A new request for alternative relief on punitive damages.>> The "
     "reply asks the Court to treat the prayer for punitive damages “as a "
     "separate claim within the scope of” the Rule 12(b)(6) motion. "
     "(Dkt. 33 at 10:5–12.) The motion made no such request."),
    ("PARA",
     "Exhibit A addresses only these five matters. Leave will cause no "
     "prejudice or delay: the hearing is nearly four weeks away, Exhibit A is "
     "attached now, and the reply itself was filed late. As stated in the "
     "accompanying declaration, Plaintiff asked defense counsel to stipulate "
     "and could not obtain a stipulation."),
    ("SUBHEAD", "IV.  CONCLUSION"),
    ("PARA",
     "Plaintiff asks the Court to grant leave and deem Exhibit A filed. In the "
     "alternative, Plaintiff asks the Court to disregard the arguments and "
     "requests raised for the first time in Defendants' untimely reply "
     "(Dkt. 33)."),
]

# ------------------------------------------------------------ sur-reply
SUR_CAPTION = ([
    "EXHIBIT A — [PROPOSED]",
    "PLAINTIFF'S SUR-REPLY IN",
    "OPPOSITION TO MOTION TO",
    "DISMISS AND STRIKE",
])

SUR = [
    ("PARA",
     "Plaintiff submits this sur-reply, limited to the five matters raised for "
     "the first time in Defendants' reply (Dkt. 33)."),
    ("SUBHEAD", "I.  THE NEW DOOR-ENTRY IMMUNITY ARGUMENT RESTS ON A FACT\n"
                "     THE FAC DOES NOT PLEAD."),
    ("PARA",
     "The reply's immunity question assumes an “unconscious” driver. "
     "(Dkt. 33 at 4:28–5:3, 8:5–8.) The FAC alleges a fatigued "
     "driver who left the travel lanes to rest and was asleep in a normal "
     "resting posture in an undamaged car. (FAC ¶¶ 11, 14, 16, 56.) "
     "The Court accepts those facts and draws reasonable inferences in "
     "Plaintiff's favor; when both sides offer plausible explanations, the "
     "complaint survives. <<i:Starr v. Baca>>, 652 F.3d 1202, 1216 (9th Cir. "
     "2011)."),
    ("PARA",
     "On those facts, the law was clearly established in November 2024. "
     "Opening a car door and entering the interior is a search that requires "
     "probable cause or another particularized justification. "
     "<<i:United States v. Ngumezi>>, 980 F.3d 1285, 1288–89 (9th Cir. "
     "2020). The emergency-aid exception requires “an objectively "
     "reasonable basis for believing” that someone inside needs immediate "
     "aid. <<i:Brigham City v. Stuart>>, 547 U.S. 398, 406 (2006); "
     "<<i:Hopkins v. Bonvicino>>, 573 F.3d 752, 763–64 (9th Cir. 2009). "
     "The reply distinguishes <<i:Hopkins>> by asserting that the officers had "
     "“no information.” But the FAC alleges what they saw through "
     "the windows with their flashlights: an intact car and a person in a "
     "resting posture. (FAC ¶¶ 11, 14, 16.) Sleep in a parked car "
     "is not an emergency."),
    ("PARA",
     "The reply also relies on half of Plaintiff's proposed amendment: that he "
     "did not respond to “open the window” before the door was "
     "opened. (Dkt. 33 at 4:14–16.) The same proposed allegation states "
     "that Melano opened the door three seconds later, “before Plaintiff "
     "could comply,” and asked “Are you okay?” only after the "
     "door was open. (Dkt. 27 at 19:26–20:3 (recording at "
     "00:56:40–00:56:43).) An officer who is speaking to an awake driver "
     "showing no sign of distress has no objective basis for emergency aid. "
     "On either version of the facts, the new immunity argument fails."),
    ("SUBHEAD", "II.  <<i:AIRS AROMATICS>> DOES NOT BAR CONFORMING "
                "PARAGRAPH 16."),
    ("PARA",
     "“[T]here is nothing in the Federal Rules of Civil Procedure to "
     "prevent a party from filing successive pleadings that make inconsistent "
     "or even contradictory allegations.” <<i:PAE Gov't Servs., Inc. v. "
     "MPRI, Inc.>>, 514 F.3d 856, 860 (9th Cir. 2007). Only a sham pleading is "
     "barred, and inconsistency alone does not show one. <<i:Id.>> at "
     "858–60. The proposed correction conforms paragraph 16 to timestamps "
     "on the recording that both sides have. It is not a change of theory to "
     "escape dismissal, and it does not change the result: on either version, "
     "the officers lacked an objective basis to believe an emergency existed. "
     "Defendants cannot rely on the knock-and-command sequence to defend the "
     "entry (Dkt. 33 at 4:14–16) while arguing that Plaintiff may not "
     "plead it accurately."),
    ("SUBHEAD", "III.  LEAVE TO AMEND COUNT II SHOULD BE GRANTED; THE "
                "SPECIFIC\n       FACTS ARE THESE."),
    ("PARA",
     "The reply says Plaintiff identified no specific fabricated statement. "
     "(Dkt. 33 at 2:9–13.) Facts raised in opposition papers are "
     "considered in deciding whether to grant leave to amend. "
     "<<i:Broam v. Bogan>>, 320 F.3d 1023, 1026 n.2 (9th Cir. 2003). A "
     "deliberate-fabrication claim requires deliberate fabrication of evidence "
     "that caused a deprivation of liberty. <<i:Spencer v. Peters>>, 857 F.3d "
     "789, 798 (9th Cir. 2017). The FAC already pleads the facts that an "
     "amended Count II would set out element by element:"),
    ("LIST_ITEM",
     "(a)  <<b:Statements.>> Meza-Gonzalez's DS-367 and arrest report state "
     "that Plaintiff's speech was “slurred,” that he “seemed "
     "very confused and disoriented,” and that there was a “strong "
     "distinct odor of an alcoholic beverage.” (FAC ¶ 26(a)–(c).)"),
    ("LIST_ITEM",
     "(b)  <<b:Contrary record.>> The recording captures extended coherent "
     "conversation, Plaintiff spelling his surname, discussing the car's "
     "mechanics, and correctly identifying his location, and more than two "
     "hours of audio in which no officer remarks on any odor. (Id. "
     "¶¶ 20, 26(a)–(c).)"),
    ("LIST_ITEM",
     "(c)  <<b:Knowledge.>> Meza-Gonzalez was present for everything he "
     "described. (Id. ¶¶ 40–41, 46.) See <<i:Chism v. "
     "Washington State>>, 661 F.3d 380, 388 (9th Cir. 2011)."),
    ("LIST_ITEM",
     "(d)  <<b:Deprivation.>> The documents were used to obtain the warrant for "
     "a compelled blood draw (FAC ¶¶ 29, 36(b)), supported the parole "
     "hold that extended Plaintiff's confinement (id. ¶ 36(a)), and were "
     "the statutory basis for a one-year administrative suspension of his "
     "Class A commercial license (id. ¶¶ 36(d), 37). A criminal "
     "charge is not required where a fabrication causes the loss of a "
     "protected interest. <<i:Costanich v. Dep't of Soc. & Health Servs.>>, "
     "627 F.3d 1101, 1108 (9th Cir. 2010)."),
    ("PARA",
     "It is not “absolutely clear” that amendment could not cure "
     "any defect. <<i:Akhtar v. Mesa>>, 698 F.3d 1202, 1212 (9th Cir. 2012). "
     "As to Count VI, Plaintiff does not seek leave to amend at this time and "
     "asks only that any dismissal be without prejudice; the refusal of the "
     "voluntary preliminary alcohol screening test remains part of the "
     "probable-cause analysis under Count III."),
    ("SUBHEAD", "IV.  CORRECTING A FORM LABEL IS NOT A CONCESSION OF ODOR."),
    ("PARA",
     "The reply treats Plaintiff's statement that a CHP form field refers to "
     "“an odor of an alcoholic beverage, not to a container” as "
     "support for probable cause. (Dkt. 33 at 6:7–9, 8:9–13.) "
     "Plaintiff corrected what the form says, not whether the officer's entry "
     "was true. The FAC alleges that the odor entry is false. (FAC "
     "¶ 26(a).) “[I]t is improper to assume the truth of an "
     "incorporated document if such assumptions only serve to dispute facts "
     "stated in a well-pleaded complaint.” <<i:Khoja v. Orexigen "
     "Therapeutics, Inc.>>, 899 F.3d 988, 1003 (9th Cir. 2018)."),
    ("SUBHEAD", "V.  THE PUNITIVE-DAMAGES PRAYER IS NOT A CLAIM."),
    ("PARA",
     "The request to recast the motion to strike as a motion to dismiss the "
     "prayer is new and may be disregarded. <<i:Zamani>>, 491 F.3d at 997. "
     "<<i:Whittlestone, Inc. v. Handi-Craft Co.>>, 618 F.3d 970, 974–75 "
     "(9th Cir. 2010), does not permit the same result under another label. A "
     "prayer is a “demand for the relief sought,” Fed. R. Civ. P. "
     "8(a)(3), not a claim; its availability follows the claims that survive. "
     "Punitive damages under section 1983 require “reckless or callous "
     "indifference to the federally protected rights of others.” "
     "<<i:Smith v. Wade>>, 461 U.S. 30, 56 (1983). The reply's assertion that "
     "Melano could not both lack a justification and voice investigative "
     "suspicions (“Both cannot be true”) is mistaken: speculating "
     "aloud that a cup holds alcohol is not a lawful justification for a "
     "search, <<i:Ngumezi>>, 980 F.3d at 1288–89, and asking “Are "
     "you okay?” after the door is open does not make the entry lawful "
     "after the fact."),
    ("SUBHEAD", "VI.  CONCLUSION"),
    ("PARA",
     "The Court should disregard or reject the reply's new arguments, deny the "
     "motion as to Counts I, III, IV, and V and the motion to strike, dismiss "
     "Count II with leave to amend and Count VI without prejudice, and grant "
     "leave to amend as to any other defect the Court identifies."),
]

# ---------------------------------------------------------- declaration
DECL_CAPTION = ([
    "DECLARATION OF BRENDAN",
    "NGWA NFORBI ISO",
    "ADMINISTRATIVE MOTION FOR",
    "LEAVE TO FILE SUR-REPLY",
])

DECL = [
    ("PARA", "I, Brendan Ngwa Nforbi, declare:"),
    ("PARA",
     "1.  I am the plaintiff in this action and represent myself. I have "
     "personal knowledge of the facts in this declaration and could testify "
     "competently to them."),
    ("PARA",
     "2.  I submit this declaration under Civil Local Rule 7-11(a) in support "
     "of my Administrative Motion for Leave to File a Sur-Reply to Defendants' "
     "Reply (Dkt. 33)."),
    ("PARA",
     "3.  Defendants filed their motion to dismiss and strike on October 26, "
     "2026 (Dkt. 22). I filed my opposition on October 29, 2026 (Dkt. 27). On "
     "October 30, 2026, the case was reassigned to Judge Breyer with existing "
     "briefing schedules unchanged (Dkt. 29). The motion is set for hearing on "
     "December 18, 2026, at 10:00 a.m. by Zoom webinar (Dkt. 31)."),
    ("PARA",
     "4.  Defendants filed their reply on November 20, 2026 (Dkt. 33), four "
     "days after the November 16, 2026 reply deadline under Civil L.R. 7-3(c)."),
    ("PARA",
     "5.  On November [___], 2026, I emailed Deputy Attorney General Haiyang "
     "A. Li, counsel for Defendants, identified the new matters in the reply, "
     "and asked whether Defendants would stipulate to my filing a short "
     "sur-reply limited to those matters. I asked for a response by 5:00 p.m. "
     "on Monday, November 23, 2026. A true copy of my email is attached as "
     "Exhibit 1."),
    ("PARA",
     "6.  [COMPLETE ONE: On November [___], 2026, counsel responded that "
     "Defendants do not agree. / As of [time] on November 23, 2026, I had "
     "received no response.] I therefore could not obtain a stipulation."),
    ("PARA",
     "7.  Exhibit A to the motion is my proposed sur-reply. It addresses only "
     "the new matters identified in the motion."),
    ("PARA",
     "I declare under penalty of perjury under the laws of the United States "
     "of America that the foregoing is true and correct."),
]

# --------------------------------------------------------------- order
ORDER_CAPTION = ([
    "[PROPOSED] ORDER GRANTING",
    "PLAINTIFF'S ADMINISTRATIVE",
    "MOTION FOR LEAVE TO FILE",
    "SUR-REPLY",
])

ORDER = [
    ("PARA",
     "Plaintiff Brendan Ngwa Nforbi's Administrative Motion for Leave to File "
     "a Sur-Reply to Defendants' Reply in Support of Motion to Dismiss and "
     "Motion to Strike (Dkt. 33) came before the Court under Civil Local Rules "
     "7-3(d) and 7-11. Having considered the motion, the supporting "
     "declaration, the proposed sur-reply, and any response, and good cause "
     "appearing,"),
    ("PARA",
     "IT IS ORDERED that the motion is GRANTED. The sur-reply attached as "
     "Exhibit A to the motion is deemed filed as of the date of this order and "
     "will be considered with Defendants' Motion to Dismiss and Motion to "
     "Strike (Dkt. 22)."),
    ("LINE", "IT IS SO ORDERED."),
]


# ------------------------------------------------------------- render
def _right_rows(title_lines: list[str]) -> list[tuple[str, str]]:
    rows = [(f"Case No. {CASE_NO}", "r"), ("", "")]
    rows += [(t, "b") for t in title_lines]
    rows += [
        ("", ""),
        ("[Civil L.R. 7-3(d), 7-11]", "r"),
        ("", ""),
        ("Judge: Hon. Charles R. Breyer", "r"),
        ("Hearing: December 18, 2026", "r"),
        ("Time: 10:00 a.m. (Zoom webinar)", "r"),
        ("Action Filed: August 10, 2026", "r"),
    ]
    return rows


DEFENDANT_LINES = [
    "SANTIAGO MEZA-GONZALEZ (CHP Badge",
    "#023295), in his individual capacity;",
    "JOSE MELANO (CHP Badge #023054), in",
    "his individual capacity; and DOES 1",
    "through 10, inclusive,",
]


def build(out: Path, footer: str, title_lines: list[str], content: list,
          date: str, place: str | None = None, signed: bool = True,
          judge_block: bool = False, party_block: bool = True) -> Path:
    d = NDCalPaper(str(out), footer=f"{footer} -- {CAPTION}")
    d.header(party_block=party_block)
    d.caption("BRENDAN NGWA NFORBI,", DEFENDANT_LINES, _right_rows(title_lines))
    for kind, text in content:
        if kind in ("HEADER", "SUBHEAD"):
            d.heading(" ".join(x.strip() for x in text.split("\n")))
        elif kind == "PARA":
            d.para(text)
        elif kind == "LIST_ITEM":
            d.item(text)
        elif kind == "LINE":
            d.write_line(text, indent=36)
        else:
            raise ValueError(kind)
    if signed:
        d.sign_off(date, SIGNATURE_PATH, SIGNATURE_NATIVE_PX, executed_at=place)
    if judge_block:
        d.judge_block()
    d.save()
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", default=DEFAULT_DATE)
    ap.add_argument("--place", default=DEFAULT_PLACE)
    a = ap.parse_args()
    if not Path(SIGNATURE_PATH).is_file():
        raise SystemExit(f"Missing signature image: {SIGNATURE_PATH}")
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    tag = "(Nov 2026)"
    p = {
        "motion": OUT_DIR / f"DRAFT - Admin Motion for Leave to File Sur-Reply (Dkt 33) {tag}.pdf",
        "sur": OUT_DIR / f"DRAFT - Exhibit A - Proposed Sur-Reply (Dkt 33) {tag}.pdf",
        "decl": OUT_DIR / f"DRAFT - Declaration ISO Admin Motion for Sur-Reply {tag}.pdf",
        "order": OUT_DIR / f"DRAFT - Proposed Order Granting Leave to File Sur-Reply {tag}.pdf",
        "packet": OUT_DIR / f"DRAFT - Sur-Reply Admin Motion Filing Packet {tag}.pdf",
    }
    build(p["motion"], "ADMIN. MOTION FOR LEAVE TO FILE SUR-REPLY",
          MOTION_CAPTION, MOTION, a.date)
    build(p["sur"], "EX. A — [PROPOSED] SUR-REPLY", SUR_CAPTION, SUR,
          a.date)
    build(p["decl"], "DECLARATION ISO ADMIN. MOTION FOR SUR-REPLY",
          DECL_CAPTION, DECL, a.date, place=a.place)
    build(p["order"], "[PROPOSED] ORDER GRANTING LEAVE TO FILE SUR-REPLY",
          ORDER_CAPTION, ORDER, a.date, signed=False, judge_block=True,
          party_block=True)
    w = PdfWriter()
    for k in ("motion", "sur", "decl"):
        for pg in PdfReader(str(p[k])).pages:
            w.add_page(pg)
    with open(p["packet"], "wb") as fh:
        w.write(fh)
    for k, v in p.items():
        print(f"{k:7s} {len(PdfReader(str(v)).pages):2d} pp  {v.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
