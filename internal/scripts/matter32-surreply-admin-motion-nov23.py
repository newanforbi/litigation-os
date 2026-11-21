#!/usr/bin/env python3
"""Matter 32 — Nov. 23, 2026 text of the Civil L.R. 7-11 sur-reply packet
(Plaintiff's revised drafts), laid out in the N.D. Cal. "Agiliti" style.

Nforbi v. Meza-Gonzalez, N.D. Cal. No. 3:26-cv-08271-CRB; responds to
Defendants' reply, Dkt. 33.

Dates and signatures are left blank by default.

    python3 internal/scripts/matter32-surreply-admin-motion-nov23.py \\
        [--date "November 24, 2026"] [--sign]

Changes from the Nov. 23 drafts: Dutta v. State Farm removed (does not
support the 7-3(d) proposition); Exhibit A heading I made singular ("A
FACT"), since only "unconscious" is unpleaded; "four-page" references
changed to five pages (Exhibit A runs five pages in this format).
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR / "lib"))
sys.path.insert(0, str(SCRIPT_DIR))
from pleading_paper_ndcal import NDCalPaper  # noqa: E402
from pypdf import PdfReader, PdfWriter  # noqa: E402
from signature_stamp import SIGNATURE_NATIVE_PX, SIGNATURE_PATH  # noqa: E402

ROOT = SCRIPT_DIR.parents[1]
OUT_DIR = ROOT / "documents/matter-32/ndcal"
CASE_NO = "3:26-cv-08271-CRB"
BLANK_DATE = "_______________, 2026"
PLACE = "Stockton, California"
CAPTION = "NFORBI v. MEZA-GONZALEZ, et al."

DEFENDANT_LINES = [
    "SANTIAGO MEZA-GONZALEZ (CHP Badge",
    "#023295), in his individual capacity;",
    "JOSE MELANO (CHP Badge #023054), in",
    "his individual capacity; and DOES 1",
    "through 10, inclusive,",
]


def _right_rows(title_lines: list[str], rule: str) -> list[tuple[str, str]]:
    rows = [(f"Case No. {CASE_NO}", "r"), ("", "")]
    rows += [(t, "b") for t in title_lines]
    rows += [
        ("", ""),
        (rule, "r"),
        ("", ""),
        ("Judge: Hon. Charles R. Breyer", "r"),
        ("Hearing: December 18, 2026", "r"),
        ("Time: 10:00 a.m. (Zoom Webinar)", "r"),
        ("Action Filed: August 10, 2026", "r"),
    ]
    return rows


# ------------------------------------------------------------------ motion
MOTION_TITLE = ["PLAINTIFF'S ADMINISTRATIVE", "MOTION FOR LEAVE TO FILE",
                "SUR-REPLY TO DEFENDANTS'", "REPLY (DKT. 33)"]
MOTION = [
    ("H", "ADMINISTRATIVE MOTION"),
    ("P", "Under Civil Local Rules 7-3(d) and 7-11, Plaintiff Brendan Ngwa "
          "Nforbi, appearing in propria persona, moves for leave to file the "
          "five-page sur-reply attached as Exhibit A. It responds solely to "
          "five matters that Defendants raised for the first time in their "
          "Reply in Support of Motion to Dismiss and Motion to Strike "
          "(Dkt. 33). This Motion is supported by the Memorandum below, the "
          "accompanying Declaration under Civil L.R. 7-11(a), Exhibit A, and "
          "the [Proposed] Order submitted concurrently herewith."),
    ("H", "MEMORANDUM OF POINTS AND AUTHORITIES"),
    ("H", "I. PROCEDURAL BACKGROUND"),
    ("P", "Defendants filed their Motion to Dismiss the First Amended "
          "Complaint and Motion to Strike on October 26, 2026 (Dkt. 22). "
          "Plaintiff filed his Opposition on October 29, 2026 (Dkt. 27). On "
          "October 30, 2026, the action was reassigned to this Court with "
          "existing briefing schedules left unchanged (Dkt. 29), and on "
          "November 3, 2026, the Clerk set the hearing for Friday, December "
          "18, 2026, at 10:00 a.m. by Zoom webinar (Dkt. 31)."),
    ("P", "Under Civil L.R. 7-3(a) and (c), the opposition deadline was "
          "November 9, 2026, and the reply was due November 16, 2026. "
          "Defendants filed their Reply on November 20, 2026—four days "
          "late, without a stipulation or order under Civil L.R. 6-2 or 6-3 "
          "(Dkt. 33)—with a caption listing Saturday, “December 19, "
          "2026,” in “Courtroom 4” and a superseded magistrate "
          "suffix in the footer. (Id. at 1.) Plaintiff does not ask to strike "
          "the Reply; he requests a brief opportunity to answer what is new."),
    ("H", "II. LEGAL STANDARD"),
    ("P", "Once a reply is filed, no additional memoranda may be filed "
          "without prior Court approval. Civil L.R. 7-3(d). A court “need "
          "not consider arguments raised for the first time in a reply "
          "brief.” <<i:Zamani v. Carnes>>, 491 F.3d 990, 997 (9th Cir. "
          "2007). Where the Court may consider new reply matter, good cause "
          "exists to permit a short sur-reply so the opposing party has a "
          "fair opportunity to respond."),
    ("H", "III. THE REPLY RAISES FIVE NEW MATTERS"),
    ("I", "1. <<b:Qualified immunity for opening the car door (Count IV).>> "
          "The opening motion's immunity argument addressed only probable "
          "cause to search and arrest. (Dkt. 22 at 12:7–13:21; Dkt. 27 "
          "at 17:24–27.) The reply argues for the first time that "
          "Defendants are immune for opening the door of a car occupied by an "
          "“unconscious” driver. (Dkt. 33 at 4:28–5:3, "
          "8:5–8.)"),
    ("I", "2. <<b:New authority to bar amendment.>> The reply invokes "
          "<<i:Airs Aromatics, LLC v. Victoria's Secret Stores Brand Mgmt., "
          "Inc.>>, 744 F.3d 595, 600 (9th Cir. 2014)—uncited in the "
          "opening motion—to argue Plaintiff may not conform FAC ¶ 16 "
          "to the recording. (Dkt. 33 at 5:4–12, 9:21–24.)"),
    ("I", "3. <<b:New basis to dismiss Counts II and VI with prejudice.>> The "
          "reply argues Plaintiff's limited non-opposition requires denial of "
          "leave to amend, citing new authority, <<i:Argueta v. Walgreens "
          "Co.>>, 760 F. Supp. 3d 1028, 1033 (E.D. Cal. 2024). (Dkt. 33 at "
          "2:1–13, 9:25–10:4.)"),
    ("I", "4. <<b:Use of a form-label correction as an “odor” "
          "concession.>> The reply treats Plaintiff's correction of what a CHP "
          "form field says as factual support for probable cause and "
          "immunity. (Dkt. 33 at 6:7–9, 8:9–13.)"),
    ("I", "5. <<b:New request for Rule 12(b)(6) dismissal of punitive "
          "damages.>> For the first time on reply, Defendants ask the Court to "
          "treat the punitive-damages prayer “as a separate claim within "
          "the scope of” Rule 12(b)(6). (Dkt. 33 at 10:5–12.)"),
    ("P", "Exhibit A addresses only these five matters. Granting leave causes "
          "no prejudice or delay: the hearing is nearly four weeks away, "
          "Exhibit A is attached now, and the reply itself was filed late. As "
          "stated in the accompanying Declaration under Civil L.R. 7-11(a), "
          "Plaintiff requested a stipulation from defense counsel and could "
          "not obtain one."),
    ("H", "IV. CONCLUSION"),
    ("P", "Plaintiff respectfully requests that the Court grant leave and "
          "deem Exhibit A filed, or, alternatively, disregard the arguments "
          "and requests raised for the first time in Defendants' untimely "
          "Reply (Dkt. 33)."),
]

# --------------------------------------------------------------- exhibit A
SUR_TITLE = ["EXHIBIT A — [PROPOSED]", "PLAINTIFF'S SUR-REPLY IN",
             "OPPOSITION TO MOTION TO", "DISMISS AND STRIKE"]
SUR = [
    ("P", "Plaintiff Brendan Ngwa Nforbi submits this Sur-Reply, limited "
          "strictly to five matters raised for the first time in Defendants' "
          "Reply (Dkt. 33)."),
    ("H", "I. THE NEW DOOR-ENTRY IMMUNITY THEORY ASSUMES A FACT THE FAC "
          "DOES NOT PLEAD."),
    ("P", "The reply's immunity question assumes an “unconscious” "
          "driver. (Dkt. 33 at 4:28–5:3, 8:5–8.) The FAC alleges a "
          "fatigued driver resting asleep in a normal posture in an undamaged "
          "car off the travel lanes. (FAC ¶¶ 11, 14, 16, 56.) The "
          "Court accepts those facts and draws inferences in Plaintiff's "
          "favor; where both sides offer plausible explanations, the claim "
          "survives. <<i:Starr v. Baca>>, 652 F.3d 1202, 1216 (9th Cir. "
          "2011)."),
    ("P", "On those facts, the law was clearly established in November 2024. "
          "Opening a car door and entering the interior is a search requiring "
          "probable cause or another particularized justification. "
          "<<i:United States v. Ngumezi>>, 980 F.3d 1285, 1288–89 (9th "
          "Cir. 2020). The emergency-aid exception requires “an "
          "objectively reasonable basis for believing” someone inside "
          "needs immediate aid. <<i:Brigham City v. Stuart>>, 547 U.S. 398, "
          "406 (2006); <<i:Hopkins v. Bonvicino>>, 573 F.3d 752, 763–64 "
          "(9th Cir. 2009). The reply distinguishes <<i:Hopkins>> by "
          "asserting the officers had “no information,” yet the FAC "
          "alleges what they saw through the windows with flashlights: an "
          "intact car and a person in a resting posture. (FAC ¶¶ 11, "
          "14, 16.) Sleep in a parked car is not an emergency."),
    ("P", "The reply also relies on half of Plaintiff's proposed amendment: "
          "that he did not respond to “open the window” before the "
          "door opened. (Dkt. 33 at 4:14–16.) The same proposed "
          "allegation states that the officers' knock woke Plaintiff, Officer "
          "Melano said “open the window,” and Melano opened the door "
          "three seconds later, “before Plaintiff could comply,” "
          "asking “Are you okay?” only after the door was open. "
          "(Dkt. 27 at 19:26–20:3 (recording at "
          "00:56:40–00:56:43).) An officer speaking to an awake driver "
          "just roused by a knock who shows no sign of distress has no "
          "objective basis for emergency aid. On either version of the facts, "
          "the new immunity argument fails."),
    ("H", "II. <<i:AIRS AROMATICS>> DOES NOT BAR CONFORMING PARAGRAPH 16."),
    ("P", "“[T]here is nothing in the Federal Rules of Civil Procedure to "
          "prevent a party from filing successive pleadings that make "
          "inconsistent or even contradictory allegations.” <<i:PAE Gov't "
          "Servs., Inc. v. MPRI, Inc.>>, 514 F.3d 856, 860 (9th Cir. 2007). "
          "Only a sham pleading is barred, and inconsistency alone does not "
          "show one. <<i:Id.>> at 858–60. The proposed correction "
          "conforms paragraph 16 to timestamps on the recording both sides "
          "possess—reflecting that the knock woke Plaintiff before Melano "
          "pulled the door open. It is not a change of theory to escape "
          "dismissal and does not change the result: on either version, the "
          "officers lacked an objective basis for emergency aid. Defendants "
          "cannot rely on the knock-and-command sequence to defend the entry "
          "(Dkt. 33 at 4:14–16) while arguing Plaintiff may not plead it "
          "accurately."),
    ("H", "III. LEAVE TO AMEND COUNT II IS WARRANTED ON SPECIFIC FACTS."),
    ("P", "The reply contends Plaintiff identified no specific fabricated "
          "statement. (Dkt. 33 at 2:9–13.) Facts raised in opposition "
          "papers are considered when deciding leave to amend. <<i:Broam v. "
          "Bogan>>, 320 F.3d 1023, 1026 n.2 (9th Cir. 2003). Deliberate "
          "fabrication requires deliberate fabrication of evidence causing a "
          "deprivation of liberty. <<i:Spencer v. Peters>>, 857 F.3d 789, 798 "
          "(9th Cir. 2017). The FAC already pleads the facts an amended Count "
          "II would set out element by element:"),
    ("I", "(a) <<b:Statements.>> Meza-Gonzalez's DS-367 and arrest report "
          "state that Plaintiff's speech was “slurred,” that he "
          "“seemed very confused and disoriented,” and that there "
          "was a “strong distinct odor of an alcoholic beverage.” "
          "(FAC ¶ 26(a)–(c).)"),
    ("I", "(b) <<b:Contrary record.>> The recording captures extended "
          "coherent conversation—Plaintiff spelling his surname, "
          "discussing the car's mechanics, and correctly identifying his "
          "location—and over two hours of audio with no officer remarking "
          "on any odor. (Id. ¶¶ 20, 26(a)–(c).)"),
    ("I", "(c) <<b:Knowledge.>> Meza-Gonzalez was present for everything he "
          "described. (Id. ¶¶ 40–41, 46.) See <<i:Chism v. "
          "Washington State>>, 661 F.3d 380, 388 (9th Cir. 2011)."),
    ("I", "(d) <<b:Deprivation.>> The documents were used to obtain the "
          "blood-draw warrant (FAC ¶¶ 29, 36(b)), supported the "
          "parole hold extending Plaintiff's confinement (id. ¶ 36(a)), "
          "and formed the statutory basis for a one-year administrative "
          "suspension of his Class A commercial license (id. ¶¶ "
          "36(d), 37). No criminal charge is required where fabrication "
          "causes the loss of a protected interest. <<i:Costanich v. Dep't of "
          "Soc. & Health Servs.>>, 627 F.3d 1101, 1108 (9th Cir. 2010)."),
    ("P", "It is not “absolutely clear” amendment cannot cure any "
          "defect. <<i:Akhtar v. Mesa>>, 698 F.3d 1202, 1212 (9th Cir. 2012). "
          "As to Count VI, Plaintiff does not seek leave to amend at this time "
          "and asks only that any dismissal be without prejudice; the refusal "
          "of the voluntary preliminary alcohol screening test remains part "
          "of Count III."),
    ("H", "IV. CORRECTING A FORM LABEL IS NOT A CONCESSION OF ODOR."),
    ("P", "The reply treats Plaintiff's statement that a CHP form field "
          "refers to “an odor of an alcoholic beverage, not to a "
          "container” as support for probable cause and immunity. "
          "(Dkt. 33 at 6:7–9, 8:9–13.) Plaintiff corrected what the "
          "form says, not whether the entry was true; FAC ¶ 26(a) alleges "
          "it is false. “[I]t is improper to assume the truth of an "
          "incorporated document” to dispute well-pleaded facts. "
          "<<i:Khoja v. Orexigen Therapeutics, Inc.>>, 899 F.3d 988, 1003 "
          "(9th Cir. 2018)."),
    ("H", "V. THE PUNITIVE-DAMAGES PRAYER IS NOT A CLAIM."),
    ("P", "Recasting the Rule 12(f) strike as a Rule 12(b)(6) dismissal is new "
          "and may be disregarded. <<i:Zamani v. Carnes>>, 491 F.3d 990, 997 "
          "(9th Cir. 2007). <<i:Whittlestone, Inc. v. Handi-Craft Co.>>, 618 "
          "F.3d 970, 974–75 (9th Cir. 2010), bars the same result under "
          "another label. A prayer is a “demand for the relief "
          "sought,” Fed. R. Civ. P. 8(a)(3), not a claim; its "
          "availability follows the surviving claims. Under § 1983, "
          "punitive damages require “reckless or callous indifference to "
          "the federally protected rights of others.” <<i:Smith v. "
          "Wade>>, 461 U.S. 30, 56 (1983). The reply's “Both cannot be "
          "true” point fails: speculating aloud that a cup holds alcohol "
          "does not justify entry, <<i:Ngumezi>>, 980 F.3d at 1288–89, "
          "and asking “Are you okay?” afterward cannot validate it."),
    ("H", "VI. CONCLUSION"),
    ("P", "The Court should disregard or reject the reply's new arguments, "
          "deny dismissal of Counts I, III, IV, and V and the motion to "
          "strike, dismiss Count II with leave to amend and Count VI without "
          "prejudice, and grant leave to amend as to any other defect."),
]

# ------------------------------------------------------------- declaration
DECL_TITLE = ["DECLARATION OF BRENDAN", "NGWA NFORBI IN SUPPORT OF",
              "ADMINISTRATIVE MOTION FOR", "LEAVE TO FILE SUR-REPLY"]
DECL = [
    ("P", "I, Brendan Ngwa Nforbi, declare as follows:", False),
    ("P", "1. I am the Plaintiff in the above-captioned action, appearing in "
          "propria persona. I have personal knowledge of the facts stated in "
          "this declaration and, if called as a witness, could and would "
          "competently testify to them."),
    ("P", "2. I submit this declaration pursuant to Civil Local Rule 7-11(a) "
          "in support of my Administrative Motion for Leave to File a "
          "Sur-Reply to Defendants' Reply Brief (Dkt. 33)."),
    ("P", "3. Defendants filed their Motion to Dismiss and Motion to Strike on "
          "October 26, 2026 (Dkt. 22). I filed my Opposition on October 29, "
          "2026 (Dkt. 27). On October 30, 2026, this action was reassigned to "
          "Judge Breyer with existing briefing schedules unchanged (Dkt. 29). "
          "On November 3, 2026, the Clerk set the motion hearing for December "
          "18, 2026, at 10:00 a.m. by Zoom webinar (Dkt. 31)."),
    ("P", "4. On November 20, 2026, Defendants filed their Reply "
          "(Dkt. 33)—four days after the November 16, 2026 reply deadline "
          "under Civil L.R. 7-3(c) and Dkt. 29."),
    ("P", "5. Pursuant to Civil Local Rule 7-11(a), on [November ___, 2026], "
          "I e-mailed Deputy Attorney General Haiyang A. Li "
          "(Haiyang.Li@doj.ca.gov), counsel for Defendants, identified the "
          "five new matters in the Reply, and asked whether Defendants would "
          "stipulate to my filing a sur-reply of five pages or fewer limited "
          "strictly to those matters. I requested a response by 5:00 p.m. Pacific on "
          "Monday, November 23, 2026. A true and correct copy of my e-mail is "
          "attached hereto as Exhibit 1."),
    ("P", "6. [COMPLETE ONE: On November ___, 2026, counsel responded that "
          "Defendants do not agree. / As of ___ on November 23, 2026, I had "
          "received no response.] Accordingly, a stipulation could not be "
          "obtained."),
    ("P", "7. Attached to the accompanying Administrative Motion as Exhibit A "
          "is my proposed five-page Sur-Reply, which addresses solely the "
          "five new matters identified in the Motion."),
    ("P", "I declare under penalty of perjury under the laws of the United "
          "States of America that the foregoing is true and correct."),
]

# ------------------------------------------------------------------- order
ORDER_TITLE = ["[PROPOSED] ORDER GRANTING", "PLAINTIFF'S ADMINISTRATIVE",
               "MOTION FOR LEAVE TO FILE", "SUR-REPLY"]
ORDER = [
    ("P", "Plaintiff Brendan Ngwa Nforbi's Administrative Motion for Leave to "
          "File a Sur-Reply to Defendants' Reply in Support of Motion to "
          "Dismiss and Motion to Strike (Dkt. 33) came before the Court under "
          "Civil Local Rules 7-3(d) and 7-11. Having considered the Motion, "
          "the supporting Declaration of Brendan Ngwa Nforbi, the proposed "
          "Sur-Reply attached as Exhibit A, and any response thereto, and good "
          "cause appearing,"),
    ("P", "IT IS HEREBY ORDERED that the Administrative Motion is GRANTED. "
          "The Sur-Reply attached as Exhibit A to the Motion is deemed filed "
          "as of the date of this Order and will be considered in connection "
          "with Defendants' Motion to Dismiss and Motion to Strike (Dkt. 22), "
          "set for hearing on December 18, 2026, at 10:00 a.m."),
    ("L", "IT IS SO ORDERED."),
]


def build(out: Path, footer: str, title: list[str], rule: str, content: list,
          date: str, sign: bool, executed: bool = False,
          judge: bool = False, party_block: bool = True) -> Path:
    d = NDCalPaper(str(out), footer=f"{footer} -- {CAPTION}")
    d.header(party_block=party_block)
    d.caption("BRENDAN NGWA NFORBI,", DEFENDANT_LINES, _right_rows(title, rule))
    for i, entry in enumerate(content):
        kind, text = entry[0], entry[1]
        if executed and i == len(content) - 1:
            d.ensure_space(12)
        if kind == "H":
            d.heading(text)
        elif kind == "P":
            d.para(text, indent_first=entry[2] if len(entry) > 2 else True)
        elif kind == "I":
            d.item(text)
        elif kind == "L":
            d.write_line(text, indent=36)
    if judge:
        d.judge_block("HONORABLE CHARLES R. BREYER", "UNITED STATES DISTRICT JUDGE")
    else:
        d.sign_off(date,
                   SIGNATURE_PATH if sign else None,
                   SIGNATURE_NATIVE_PX if sign else None,
                   executed_at=PLACE if executed else None)
    d.save()
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", default=BLANK_DATE)
    ap.add_argument("--sign", action="store_true",
                    help="stamp the signature image (default: blank line)")
    a = ap.parse_args()
    tag = "(Nov 23 2026)"
    p = {
        "motion": OUT_DIR / f"DRAFT - Admin Motion for Leave to File Sur-Reply (Dkt 33) {tag}.pdf",
        "sur": OUT_DIR / f"DRAFT - Exhibit A - Proposed Sur-Reply (Dkt 33) {tag}.pdf",
        "decl": OUT_DIR / f"DRAFT - Declaration ISO Admin Motion for Sur-Reply {tag}.pdf",
        "order": OUT_DIR / f"DRAFT - Proposed Order Granting Leave to File Sur-Reply {tag}.pdf",
        "packet": OUT_DIR / f"DRAFT - Sur-Reply Admin Motion Filing Packet {tag}.pdf",
    }
    build(p["motion"], "ADMIN. MOTION FOR LEAVE TO FILE SUR-REPLY",
          MOTION_TITLE, "[Civil L.R. 7-3(d), 7-11]", MOTION, a.date, a.sign)
    build(p["sur"], "EX. A — [PROPOSED] SUR-REPLY", SUR_TITLE,
          "[Civil L.R. 7-3(d), 7-11]", SUR, a.date, a.sign)
    build(p["decl"], "DECLARATION ISO ADMIN. MOTION FOR SUR-REPLY",
          DECL_TITLE, "[Civil L.R. 7-3(d), 7-11(a)]", DECL, a.date, a.sign,
          executed=True)
    build(p["order"], "[PROPOSED] ORDER GRANTING LEAVE TO FILE SUR-REPLY",
          ORDER_TITLE, "[Civil L.R. 7-3(d), 7-11]", ORDER, a.date, False,
          judge=True, party_block=False)
    w = PdfWriter()
    for k in ("motion", "sur", "decl"):
        for pg in PdfReader(str(p[k])).pages:
            w.add_page(pg)
    with open(p["packet"], "wb") as fh:
        w.write(fh)
    for k, v in p.items():
        print(f"{k:7s} {len(PdfReader(str(v)).pages):2d} pp  {v.name}")


if __name__ == "__main__":
    main()
