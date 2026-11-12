#!/usr/bin/env python3
"""Regenerate Matter 12 Diamond/Alpine default-judgment declarations.

Uses the same pleading-paper format as the Randstad complaint formatter
(pleading-paper-formatter-script.py): condensed attorney block, boxed caption,
HEADER / SUBHEAD / PARA / LIST_ITEM / SIGNATURE content types, and
right-aligned signature blocks with the portfolio universal signature.

Aug 4, 2026 compensatory-only filing (punitive damages omitted):
- Diamond / Alpine: $53,671.20 total; costs waived; execution August 4, 2026.
"""

from __future__ import annotations

import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(SCRIPT_DIR, "lib"))
from pleading_paper import (  # noqa: E402
    CONTENT_LEFT,
    COURT_LINE1,
    PleadingPaper,
)

REPO_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "..", ".."))
sys.path.insert(0, SCRIPT_DIR)
from signature_stamp import (  # noqa: E402
    SIGNATURE_NATIVE_PX,
    SIGNATURE_PATH,
)

# Portfolio universal signature (see signature_stamp.py).
SIGNATURE_IMG = SIGNATURE_PATH
SIG_IMG_W_PX, SIG_IMG_H_PX = SIGNATURE_NATIVE_PX
SIG_WIDTH = 140  # 445×106 (aspect ≈ 0.238) → ~38pt tall with 1.15 scale

# Set MATTER12_NO_SIGNATURE=1 to leave signature lines blank for wet signing.
NO_SIGNATURE = os.environ.get("MATTER12_NO_SIGNATURE", "") == "1"

OUT_DIR = os.environ.get("MATTER12_DECL_OUT_DIR", "/tmp/m12build")
COURT_LINE2 = "COUNTY OF SAN JOAQUIN"
CASE_NO = "STK-CV-UF-2026-0001094"
# Override with MATTER12_EXEC_DATE (e.g. "August 12, 2026") for hearing hand-ups.
EXEC_DATE = os.environ.get("MATTER12_EXEC_DATE", "August 4, 2026")
# Output filename stem tag; default keeps Aug-4 build names for back-compat.
DECL_TAG = os.environ.get("MATTER12_DECL_TAG", "Aug4_2026")


def party_block(d: PleadingPaper) -> None:
    """Randstad-style condensed attorney / court header."""
    c = d.c
    atty_y = d._line_y(0)
    atty_lh = 15
    lines = [
        ("BRENDAN NGWA NFORBI", "Times-Bold", 12),
        ("Plaintiff, In Pro Per", "Times-Roman", 12),
        ("1455 Cat Tail Drive", "Times-Roman", 12),
        ("Stockton, CA 95204", "Times-Roman", 12),
        ("Telephone: (209) 801-4442", "Times-Roman", 12),
        ("E-mail: bnn.cdl@gmail.com", "Times-Roman", 12),
    ]
    for i, (txt, fn, sz) in enumerate(lines):
        c.setFont(fn, sz)
        c.drawString(CONTENT_LEFT, atty_y - i * atty_lh, txt)
    d.current_line = 4
    d.blank_line()
    d.write_line(COURT_LINE1, bold=True, center=True)
    d.write_line(COURT_LINE2, bold=True, center=True)
    d.blank_line()


def caption_left() -> list[tuple[str, bool, bool]]:
    return [
        ("BRENDAN NGWA NFORBI,", True, False),
        ("", False, False),
        ("                          Plaintiff,", False, False),
        ("", False, False),
        ("       v.", False, False),
        ("", False, False),
        ("DIAMOND TRUCK SALES, INC.,", True, False),
        ("a California corporation;", True, False),
        ("ALPINE TRUCK SALES, INC.,", True, False),
        ("a California corporation; and", True, False),
        ("DOES 1 through 20, inclusive,", True, False),
        ("", False, False),
        ("                          Defendants.", False, False),
    ]


def render_content(d: PleadingPaper, content: list[tuple[str, str]]) -> None:
    """Render CONTENT tuples using the Randstad complaint loop."""
    for c_type, text in content:
        if c_type == "HEADER":
            d.ensure_space(3)
            d.write_line(text, bold=True, center=True)
            d.blank_line()
        elif c_type == "SUBHEAD":
            d.ensure_space(3)
            for line in text.split("\n"):
                d.write_line(line, bold=True, center=False)
            d.blank_line()
        elif c_type == "PARA":
            d.write_wrapped(text, first_indent=36)
            d.blank_line()
        elif c_type == "LIST_ITEM":
            d.write_wrapped(text, indent=36, first_indent=36)
            d.blank_line()
        elif c_type == "SIGNATURE":
            d.ensure_space(8)
            for line in text.split("\n"):
                if line.startswith("_") and not NO_SIGNATURE and os.path.isfile(SIGNATURE_IMG):
                    d.draw_signature_image(
                        SIGNATURE_IMG,
                        SIG_IMG_W_PX,
                        SIG_IMG_H_PX,
                        line,
                        width=SIG_WIDTH,
                        right_margin_offset=20,
                    )
                    d.write_line(line, right=True, right_margin_offset=20)
                else:
                    d.write_line(line, right=True, right_margin_offset=20)
            d.blank_line()
        elif c_type == "PAGEBREAK":
            d.start_new_page()


def signature_block_text() -> str:
    return (
        f"\nExecuted on {EXEC_DATE},\n"
        "at Stockton, California.\n"
        "\n"
        "___________________________________\n"
        "BRENDAN NGWA NFORBI\n"
        "Plaintiff, In Pro Per"
    )


EXHIBITS = [
    "Exhibit 1. Retail Buyer's Order dated April 4, 2023 (Diamond Truck Sales, Inc.; Customer: Brendan Ngwa Nforbi; Vehicle: 2014 Volvo VNL, VIN 4V4NC9EH6EN142206).",
    "Exhibit 2. California Department of Motor Vehicles \"Generated Fees\" printout dated May 8, 2023, reflecting Total Fees Due of $3,442.00, together with the corresponding DMV Report of Deposit of Fees and Application materials.",
    "Exhibit 3. GAP Addendum dated May 4, 2023, reflecting the $1,895.00 GAP enrollment charge.",
    "Exhibit 4. Lease-On Owner Operator Agreement between Gobbato Builders, LLC (MC #1357325) and Altamont Freight LLC, effective April 27, 2023, identifying VIN 4V4NC9EH6EN142206.",
    "Exhibit 5. Amazon Relay -- Driver Setup verification, dated April 27, 2023 9:22 AM PDT (digital verification code Y5RG-48F-25NG-P74W).",
    "Exhibit 6. Brannon Tire invoice dated April 28, 2023, in the amount of $1,197.34.",
    "Exhibit 7. Mobile Will's Truck/Auto Repair Shop invoice dated May 21, 2023, in the amount of $740.00.",
    "Exhibit 8. Golden Empire Towing, Inc. invoice dated May 26, 2023, in the amount of $562.50.",
    "Exhibit 9. Western Truck Center invoice dated June 23, 2023, in the amount of $36.71.",
    "Exhibit 10. Notice of Stored Vehicle issued under California Vehicle Code section 22852, dated May 23, 2023, by Commercial Towing, 2609 Texas Street, Bakersfield, California.",
]


def diamond_content() -> list[tuple[str, str]]:
    content: list[tuple[str, str]] = [
        ("HEADER", "DECLARATION OF BRENDAN NGWA NFORBI"),
        ("HEADER", "IN SUPPORT OF REQUEST FOR DEFAULT JUDGMENT BY COURT"),
        ("SUBHEAD", "(Cal. Rules of Court, rule 3.1800; Code Civ. Proc. section 585(b))"),
        ("PARA", "I, <<b:BRENDAN NGWA NFORBI>>, declare:"),
        ("HEADER", "I.  PRELIMINARY STATEMENT"),
        (
            "PARA",
            "1. I am the Plaintiff in the above-entitled action and am over eighteen "
            "years of age. The matters set forth herein are within my personal "
            "knowledge unless stated on information and belief, and if called as a "
            "witness, I could and would competently testify to them. I submit this "
            "Declaration in support of my Request for Entry of Default Judgment by "
            "the Court (Judicial Council Form CIV-100) against Defendant "
            "<<b:DIAMOND TRUCK SALES, INC.>> (\"Diamond\"), pursuant to Code of Civil "
            "Procedure section 585, subdivision (b), and California Rules of Court, "
            "rule 3.1800.",
        ),
        (
            "PARA",
            "2. This Declaration is submitted together with the following companion "
            "documents constituting my prove-up package: (a) the Court's Notice to "
            "Filing Party on the prior default submission (returned with this "
            "resubmission as directed); (b) Plaintiff's Request for Entry of Default "
            "Judgment (Form CIV-100), including the Declaration of Nonmilitary Status "
            "at CIV-100 item 8; (c) Plaintiff's Request for Dismissal of Does 1 "
            "through 20 (Form CIV-110); (d) Plaintiff's [Proposed] Judgment by Court "
            "After Default (Form JUD-100); and (e) the documentary exhibits "
            "referenced herein and listed in the Index of Exhibits below. Plaintiff "
            "waives costs of suit on CIV-100 item 7f; no Memorandum of Costs (Form "
            "MC-010) is filed with this packet. Plaintiff seeks compensatory relief "
            "only and does not request punitive damages in this filing.",
        ),
        ("HEADER", "II.  PROCEDURAL POSTURE"),
        (
            "PARA",
            "3. The operative pleading in this action is the First Amended Complaint "
            "(\"FAC\"), which asserts eight causes of action against Defendant Diamond: "
            "(1) Fraudulent Concealment; (2) Intentional Misrepresentation; "
            "(3) Negligent Misrepresentation; (4) Breach of Contract; (5) Breach of "
            "Implied Warranty of Merchantability (Cal. Comm. Code section 2314); "
            "(6) Violation of the Unfair Competition Law (Bus. & Prof. Code section "
            "17200 et seq.); (7) Rescission and Restitution; and (8) Declaratory Relief.",
        ),
        (
            "PARA",
            "4. The FAC was personally served on Diamond on May 12, 2026, and the "
            "Proof of Service was filed with this Court on May 18, 2026. Diamond's "
            "deadline to respond to the FAC expired on June 11, 2026. Diamond filed "
            "no responsive pleading, demurrer, or other appearance. Plaintiff has "
            "requested entry of Diamond's default by Request for Entry of Default "
            "(Form CIV-100) submitted with this packet; the prior June 15, 2026 "
            "request was Not Entered, and no default against Diamond appears of "
            "record as of the execution of this Declaration.",
        ),
        (
            "PARA",
            "5. Upon entry of Diamond's default, the well-pleaded factual "
            "allegations of the FAC concerning liability are deemed admitted. "
            "(<<i:Steven M. Garber & Assocs. v. Eskandarian>> (2007) 150 Cal.App.4th "
            "813, 823; <<i:Kim v. Westmoore Partners, Inc.>> (2011) 201 Cal.App.4th "
            "267, 281.) The well-pleaded allegations include, without limitation: that "
            "Diamond knowingly sold to me a 2014 Volvo VNL diesel semi-truck (VIN "
            "4V4NC9EH6EN142206) that suffered from an undisclosed and material defect "
            "in its Diesel Exhaust Fluid (\"DEF\") and Selective Catalytic Reduction "
            "(\"SCR\") emissions systems; that the defect rendered the truck "
            "non-compliant with California emissions law and unsafe for highway "
            "operation; and that Diamond had pre-sale knowledge of the defect and "
            "concealed it.",
        ),
        (
            "PARA",
            "6. This Declaration addresses only the amount and proof of damages. I "
            "have made no effort to relitigate liability, which will be deemed "
            "established upon entry of Diamond's default.",
        ),
        ("HEADER", "III.  THE TRANSACTION AND THE FAILURE"),
        (
            "PARA",
            "7. On April 4, 2023, I purchased the subject truck (2014 Volvo VNL, VIN "
            "4V4NC9EH6EN142206) from Diamond. The transaction was documented by a "
            "Retail Buyer's Order reflecting a Cash Price of $26,900.00 and Total "
            "Charges of $27,092.75 after document and title fees. A true and correct "
            "copy of the Retail Buyer's Order is attached as Exhibit 1.",
        ),
        (
            "PARA",
            "8. I paid Diamond a deposit of $12,345.10 by certified funds at the time "
            "of sale. This amount appears in the \"DEPOSIT\" line and is reflected in "
            "the \"TOTAL CREDITS\" line of the Retail Buyer's Order (Exh. 1, p. 1).",
        ),
        (
            "PARA",
            "9. The remaining balance of $14,747.65 was financed through a third-party "
            "lender, Dakota Financial LLC, which was selected, arranged, or facilitated "
            "by Diamond in connection with the sale.",
        ),
        (
            "PARA",
            "10. In connection with titling the truck I was billed by the California "
            "Department of Motor Vehicles in the amount of $3,442.00 for use tax, "
            "weight, transfer, and related fees required to complete registration. The "
            "California DMV \"Generated Fees\" printout dated May 8, 2023 reflects Total "
            "Fees Due of $3,442.00. I have not yet paid this amount because the truck "
            "failed before registration could be completed, leaving me with an "
            "outstanding DMV obligation that continues to accrue penalties. The "
            "California DMV \"Generated Fees\" printout and the corresponding DMV Report "
            "of Deposit of Fees and Application materials are attached as Exhibit 2. I "
            "include this amount in my damages because it is a real, documented "
            "financial obligation owed to the State of California as a direct "
            "consequence of Diamond's sale to me of a defective and non-compliant truck.",
        ),
        (
            "PARA",
            "11. In connection with the sale Diamond also enrolled me in a GAP product, "
            "for which I was charged $1,895.00 under a separate GAP Addendum. A true "
            "and correct copy of the GAP Addendum is attached as Exhibit 3.",
        ),
        (
            "PARA",
            "12. I purchased the truck specifically to use it in commercial freight "
            "service under my own owner-operator authority. On April 27, 2023, "
            "twenty-three days after purchase, I executed a Lease-On Owner Operator "
            "Agreement with Gobbato Builders, LLC (MC #1357325) under which I would "
            "haul freight for compensation paid weekly by Friday settlement. The "
            "Lease-On Agreement specifically identifies my truck by VIN. A true and "
            "correct copy of the Lease-On Owner Operator Agreement is attached as "
            "Exhibit 4. On the same day, April 27, 2023, my Amazon Relay driver "
            "account was activated, providing me with access to dispatch hauling loads "
            "through the Amazon Relay platform. A true and correct copy of the Amazon "
            "Relay driver setup verification, bearing my signature and the platform's "
            "digital verification code of April 27, 2023 9:22 AM PDT, is attached as "
            "Exhibit 5.",
        ),
        (
            "PARA",
            "13. Within days of beginning operations the truck experienced exactly the "
            "failure mode characteristic of the DEF/SCR defect alleged in the FAC: it "
            "entered engine derate (\"limp mode\"), emitted excessive black smoke, lost "
            "power, and became incapable of exceeding approximately 35 miles per hour. "
            "The truck was thereby rendered commercially unusable and unsafe for "
            "highway operation. Despite my repeated attempts to repair it (described in "
            "Sections IV and V below), the truck never returned to lawful commercial "
            "service.",
        ),
        ("HEADER", "IV.  DOCUMENTED ECONOMIC LOSSES AND OUTSTANDING OBLIGATIONS"),
        (
            "PARA",
            "14. I have incurred the following documented economic losses and "
            "obligations, each of which flows directly from Diamond's wrongful conduct "
            "as alleged in the FAC. Items (a), (b), and (d) through (g) represent cash "
            "payments made from my own funds; item (c) represents an outstanding DMV "
            "obligation billed to me in connection with the transaction and not yet "
            "paid, as described in paragraph 10 above:",
        ),
        ("LIST_ITEM", "(a) 04/04/2023 -- Diamond deposit (Retail Buyer's Order) ........ $12,345.10 (Exh. 1);"),
        ("LIST_ITEM", "(b) 05/04/2023 -- GAP Addendum enrollment ....................... $1,895.00 (Exh. 3);"),
        ("LIST_ITEM", "(c) 05/08/2023 -- California DMV fees (billed; outstanding) ..... $3,442.00 (Exh. 2);"),
        ("LIST_ITEM", "(d) 04/28/2023 -- Brannon Tire (emergency tire/road service) .... $1,197.34 (Exh. 6);"),
        ("LIST_ITEM", "(e) 05/21/2023 -- Mobile Will's Truck/Auto Repair Shop .......... $740.00 (Exh. 7);"),
        ("LIST_ITEM", "(f) 05/26/2023 -- Golden Empire Towing, Inc. .................... $562.50 (Exh. 8);"),
        ("LIST_ITEM", "(g) 06/23/2023 -- Western Truck Center (lamp/parts) ............. $36.71 (Exh. 9)."),
        ("LIST_ITEM", "SUBTOTAL -- DOCUMENTED ECONOMIC LOSSES: $20,218.65."),
        (
            "PARA",
            "15. Each of Exhibits 1, 2, 3, 6, 7, 8, and 9 is a true and correct copy of "
            "the contemporaneous record of the corresponding charge or obligation. None "
            "of these losses would have been incurred but for Diamond's sale to me of "
            "the defective and non-compliant truck. With respect to item (c), the "
            "$3,442.00 DMV obligation is fully documented by Exhibit 2, remains "
            "outstanding, and continues to accrue penalties -- making it an ongoing and "
            "expanding consequence of the transaction.",
        ),
        ("HEADER", "V.  ADDITIONAL OUT-OF-POCKET LOSSES -- NO CONTEMPORANEOUS RECEIPT"),
        (
            "PARA",
            "16. In addition to the documented charges set forth above, I personally "
            "paid in cash, from my own funds, two further amounts for emergency "
            "services performed on the truck. Although I did not retain itemized "
            "written receipts -- despite having requested them at the time -- these "
            "payments are facts within my direct personal knowledge, and the "
            "surrounding contemporaneous record corroborates that the truck was in "
            "storage, released, transported, and delivered for repair during this "
            "period:",
        ),
        (
            "LIST_ITEM",
            "(a) Commercial Towing storage-release fee -- $750.00. On or about May 23, "
            "2023, the truck was towed and stored under California Vehicle Code section "
            "22852 by Commercial Towing, located at 2609 Texas Street, Bakersfield, "
            "California. The contemporaneous Notice of Stored Vehicle issued under "
            "Vehicle Code section 22852 is attached as Exhibit 10. I paid Commercial "
            "Towing $750.00 in cash to release the truck. I requested a written receipt "
            "but the operator did not provide one.",
        ),
        (
            "LIST_ITEM",
            "(b) Almaraz Diesel repair -- $5,000.00. After the truck was released from "
            "Commercial Towing, Golden Empire Towing transported it (under the invoice "
            "constituting Exh. 8) to Almaraz Diesel, which at that time was operating "
            "out of Diamond's Bakersfield, California location. Almaraz Diesel "
            "performed diagnostic and repair work on the DEF/SCR system. I paid "
            "approximately $5,000.00 for that work. I did not receive an itemized "
            "written receipt.",
        ),
        (
            "PARA",
            "17. The two undocumented amounts above total $5,750.00. I respectfully "
            "request that the Court consider them on the basis of my sworn testimony, "
            "in light of the corroborating documentary evidence -- specifically, the "
            "contemporaneous CVC section 22852 Notice (Exh. 10) and the Golden Empire "
            "Towing invoice (Exh. 8), which together establish the chain of custody "
            "between the storage release and Almaraz Diesel. To the extent the Court "
            "declines to award the undocumented amounts, my documented out-of-pocket "
            "subtotal of $20,218.65 (Section IV above) is fully supported by Exhibits "
            "1, 2, 3, 6, 7, 8, and 9.",
        ),
        ("HEADER", "VI.  LOST COMMERCIAL INCOME"),
        (
            "PARA",
            "18. Because of the truck's failure I was unable to perform under the "
            "Lease-On Owner Operator Agreement with Gobbato Builders, LLC (Exh. 4), "
            "and I was unable to dispatch any meaningful number of loads through the "
            "Amazon Relay platform (Exh. 5). The truck was operational for only a "
            "matter of days before catastrophic failure. By late May 2023 it had been "
            "towed and stored under Vehicle Code section 22852. By June 23, 2023 the "
            "final attempted repair (the Western Truck Center lamp work, Exh. 9) had "
            "failed to restore commercial operability. The truck was thereafter "
            "rendered permanently commercially unusable.",
        ),
        (
            "PARA",
            "19. Under the Lease-On Agreement with Gobbato Builders, LLC (Exh. 4, "
            "paragraph III), I was set up to operate at a 10% lease-on fee -- meaning I "
            "would have netted approximately 90% of gross load revenue, less fuel, "
            "insurance, and incidental expenses. Based on prevailing rates on the "
            "Amazon Relay platform in 2023 and my reasonable expectations at the time "
            "the FAC was filed, I had projected and pleaded approximately $1,800 in "
            "net weekly earnings had the truck been operational. (FAC, paragraph 31.)",
        ),
        (
            "PARA",
            "20. For purposes of this prove-up, and recognizing that I do not have "
            "month-by-month settlement statements documenting every load I would have "
            "hauled, I respectfully request lost commercial income on a deliberately "
            "conservative basis: 18 weeks of lost operation (conservative -- May "
            "through September 2023) at $1,300/week (well below the $1,800 pleaded in "
            "FAC paragraph 31), for a subtotal of $23,400.00.",
        ),
        (
            "PARA",
            "21. The $23,400.00 figure is approximately one half of the lower bound of "
            "lost income I pleaded in the FAC at paragraph 31, which alleged \"lost net "
            "commercial income of not less than approximately $46,800 to date, with "
            "continuing losses according to proof at trial.\" I have deliberately "
            "requested only a conservative fraction of the lost income I sustained, in "
            "recognition of the prove-up evidentiary posture and the absence of weekly "
            "settlement statements in my possession.",
        ),
        ("HEADER", "VII.  RESCISSION, RESTITUTION, AND DECLARATORY RELIEF"),
        (
            "PARA",
            "22. I gave notice of rescission within the FAC itself, as permitted by "
            "Civil Code sections 1691 and 1693. The truck has been irrecoverably "
            "damaged by the underlying defect and the storage process. Restoration of "
            "the truck to its original condition is impossible and is therefore excused "
            "under Civil Code section 1693, and this Court is authorized to adjust the "
            "equities between the parties under that statute.",
        ),
        (
            "PARA",
            "23. The $14,747.65 financed balance was originated through Dakota "
            "Financial LLC, which is not a party to this action. I do not seek in this "
            "Declaration a money judgment in the amount of the financed balance itself, "
            "because that obligation is between me and a non-party lender and "
            "recovering it from Diamond would risk a double recovery if I later resolve "
            "the financing separately.",
        ),
        (
            "PARA",
            "24. I reserve the right, after entry of judgment, to seek a separate "
            "determination of any indemnification or further restitution remedy as to "
            "the financed balance if and as appropriate under Civil Code section 1693 "
            "and the Court's continuing equitable jurisdiction over the rescission "
            "count.",
        ),
        (
            "PARA",
            "25. Specific Judgment Findings Requested. In addition to the monetary "
            "relief itemized in Sections IV through VIII of this Declaration, I "
            "respectfully request that the Court's Judgment include the following "
            "findings and declarations. Each falls squarely within the scope of the "
            "FAC's Seventh Cause of Action (Rescission and Restitution) and Eighth "
            "Cause of Action (Declaratory Relief), and each is supported by "
            "well-pleaded allegations of the FAC that are deemed admitted by Diamond's "
            "default: (a) That the April 4, 2023 purchase transaction between Plaintiff "
            "and Diamond Truck Sales, Inc. -- including the Retail Buyer's Order (Exh. "
            "1) and the GAP Addendum (Exh. 3) -- is rescinded pursuant to Civil Code "
            "section 1689, subdivision (b), and is of no further force or effect as "
            "between Plaintiff and Diamond, so that Diamond may not enforce any term "
            "of, or claim any continuing benefit under, that transaction. (b) That "
            "Diamond's conduct in connection with the sale of the subject truck "
            "constituted unlawful, unfair, and fraudulent business acts and practices "
            "within the meaning of California Business and Professions Code section "
            "17200 et seq., as pleaded in the FAC's Sixth Cause of Action.",
        ),
        ("HEADER", "VIII.  PREJUDGMENT INTEREST"),
        (
            "PARA",
            "26. The documented out-of-pocket losses set forth in Section IV are "
            "liquidated and certain, or capable of being made certain by calculation, "
            "and the right to recover them vested on the dates each charge was "
            "incurred. I am therefore entitled to prejudgment interest on those amounts "
            "at the legal rate of seven percent (7%) per annum (Cal. Const., art. XV, "
            "section 1) from the date of loss to the date of judgment, pursuant to "
            "Civil Code section 3287, subdivision (a). (See <<i:North Oakland Medical "
            "Clinic v. Rogers>> (1998) 65 Cal.App.4th 824, 828-830.)",
        ),
        (
            "PARA",
            "27. For purposes of this prove-up I have computed prejudgment interest "
            "using a single, conservative weighted-average start date of June 1, 2023 "
            "(the approximate midpoint of the dates on which the documented charges in "
            "Section IV were incurred, from April 4, 2023 through June 23, 2023), "
            "applied to the $20,218.65 documented out-of-pocket subtotal through June "
            "15, 2026: $20,218.65 x 7% x approximately 3.04 years (06/01/2023 to "
            "06/15/2026) = $4,302.55. I treat that $4,302.55 figure as a conservative "
            "fixed amount through June 15, 2026 and do not seek additional prejudgment "
            "interest for the period after that date in this request.",
        ),
        (
            "PARA",
            "28. I have not sought prejudgment interest on the lost-income component in "
            "Section VI, because lost income is not liquidated within the meaning of "
            "Civil Code section 3287, subdivision (a).",
        ),
        ("HEADER", "IX.  COSTS"),
        (
            "PARA",
            "29. Plaintiff has an approved court fee waiver in this action. Consistent "
            "with CIV-100 item 7f, Plaintiff waives costs and disbursements in "
            "connection with this request for court judgment. No Memorandum of Costs "
            "(Form MC-010) is submitted, and no costs amount is included in the "
            "judgment total requested below.",
        ),
        ("HEADER", "X.  SUMMARY OF JUDGMENT REQUESTED"),
        (
            "PARA",
            "30. Based on the foregoing, I respectfully request entry of Default "
            "Judgment by the Court against Defendant Diamond Truck Sales, Inc. in the "
            "compensatory amount of $53,671.20, with costs waived, together with the "
            "non-monetary findings and declarations specified in Section VII above. "
            "Plaintiff does not seek punitive damages in this filing. The components "
            "of the requested judgment are as follows:",
        ),
        ("LIST_ITEM", "$20,218.65    Documented out-of-pocket losses (Section IV; Exhs. 1-3, 6-9)"),
        ("LIST_ITEM", "$5,750.00    Undocumented out-of-pocket, by sworn testimony (Section V; Exhs. 8, 10)"),
        ("LIST_ITEM", "$23,400.00    Lost commercial income, conservative (Section VI; Exhs. 4-5)"),
        ("LIST_ITEM", "$4,302.55    Prejudgment interest through 06/15/2026 (Section VIII)"),
        ("LIST_ITEM", "$53,671.20    TOTAL MONETARY JUDGMENT REQUESTED"),
        ("LIST_ITEM", "$0.00    Costs of suit (Section IX; waived on CIV-100 item 7f)"),
        (
            "PARA",
            "31. The amounts requested are within the scope of the prayer for relief in "
            "the FAC and do not exceed the dollar-amount notice given to Diamond by the "
            "body of the FAC, as required by Code of Civil Procedure section 580 and "
            "<<i:Greenup v. Rodman>> (1986) 42 Cal.3d 822. Specifically: the "
            "out-of-pocket itemization in FAC paragraph 29 totals $25,129.44 (covering "
            "items (a) through (g) of that paragraph), and FAC paragraph 31 pleads lost "
            "commercial income \"of not less than approximately $46,800 to date, with "
            "continuing losses\" -- both substantially exceeding the conservative "
            "figures I request here.",
        ),
        (
            "PARA",
            "32. To the extent any of the figures stated in this Declaration differ from "
            "the preliminary estimates pleaded in the FAC, this Declaration provides the "
            "more precise and current calculation based on the documentary records and "
            "sworn testimony assembled for prove-up. I seek only those amounts that are "
            "supported by the attached exhibits or by sworn testimony based on personal "
            "knowledge, and the conservative figures in Sections IV through VIII of this "
            "Declaration are at or below the amounts pleaded in the FAC.",
        ),
        ("HEADER", "XI.  INDEX OF EXHIBITS"),
    ]
    for ex in EXHIBITS:
        content.append(("LIST_ITEM", ex))
    content.extend(
        [
            ("HEADER", "XII.  EXECUTION"),
            (
                "PARA",
                "I declare under penalty of perjury under the laws of the State of "
                "California that the foregoing is true and correct.",
            ),
            ("SIGNATURE", signature_block_text()),
        ]
    )
    return content


def alpine_content() -> list[tuple[str, str]]:
    content: list[tuple[str, str]] = [
        ("HEADER", "DECLARATION OF BRENDAN NGWA NFORBI"),
        ("HEADER", "IN SUPPORT OF REQUEST FOR DEFAULT JUDGMENT"),
        ("HEADER", "AGAINST ALPINE TRUCK SALES, INC."),
        ("SUBHEAD", "(Cal. Rules of Court, rule 3.1800; Code Civ. Proc. section 585(b))"),
        ("PARA", "I, <<b:BRENDAN NGWA NFORBI>>, declare:"),
        ("HEADER", "I.  PRELIMINARY STATEMENT"),
        (
            "PARA",
            "1. I am the Plaintiff in the above-entitled action and am over eighteen "
            "years of age. The matters set forth herein are within my personal "
            "knowledge unless stated on information and belief, and if called as a "
            "witness, I could and would competently testify to them. I submit this "
            "Declaration in support of my Request for Entry of Default Judgment by the "
            "Court (Judicial Council Form CIV-100) against Defendant "
            "<<b:ALPINE TRUCK SALES, INC.>> (\"Alpine\"), pursuant to Code of Civil "
            "Procedure section 585, subdivision (b), and California Rules of Court, "
            "rule 3.1800.",
        ),
        (
            "PARA",
            "2. This Declaration is submitted together with the following companion "
            "documents constituting my prove-up package as to Alpine: (a) the Court's "
            "Notice to Filing Party on the prior default submission (returned with this "
            "resubmission as directed); (b) Plaintiff's Request for Entry of Default "
            "and Court Judgment (Form CIV-100), including the Declaration of "
            "Nonmilitary Status at CIV-100 item 8; (c) Plaintiff's Request for "
            "Dismissal of Does 1 through 20 (Form CIV-110); (d) this Declaration; "
            "(e) Plaintiff's [Proposed] Judgment by Court After Default (Form "
            "JUD-100); and (f) the exhibits attached hereto, which are the same "
            "documentary exhibits previously submitted in support of the default "
            "judgment prove-up against co-defendant Diamond Truck Sales, Inc. "
            "(\"Diamond\"), attached again here so that this filing is complete and "
            "self-contained as to Alpine. Plaintiff waives costs of suit on CIV-100 "
            "item 7f; no Memorandum of Costs (Form MC-010) is filed with this packet. "
            "Plaintiff seeks compensatory relief only and does not request punitive "
            "damages in this filing.",
        ),
        ("HEADER", "II.  PROCEDURAL POSTURE"),
        (
            "PARA",
            "3. The operative pleading in this action is the First Amended Complaint "
            "(\"FAC\"), which names Alpine as a defendant on the theory that Alpine is "
            "Diamond's successor in interest, mere continuation, de facto merger, "
            "and/or alter ego, and/or a participant in a fraudulent transfer under the "
            "Uniform Voidable Transactions Act (Civ. Code section 3439 et seq.).",
        ),
        (
            "PARA",
            "4. Alpine was personally served with the Amended Summons, the First "
            "Amended Complaint, and the Notice of Case Assignment and Notice of Hearing "
            "on July 1, 2026, at 9:00 a.m., by delivery to Mustaqem Usmani, Manager, "
            "at 1201 S Soderquist Road, Turlock, California 95380, by Stanislaus County "
            "Sheriff's Deputy T. Caldwell, under Code of Civil Procedure section "
            "416.10. Proof of Service (Form POS-010, Levying Officer File No. "
            "2026002577) was signed July 2, 2026 by the Sheriff's Authorized Agent and "
            "is on file with this Court.",
        ),
        (
            "PARA",
            "5. Alpine's deadline to respond to the FAC expired thirty (30) days after "
            "service, on July 31, 2026. Alpine filed no responsive pleading, demurrer, "
            "or other appearance, and no meet-and-confer contact was received from "
            "Alpine at any time before or after that deadline. Plaintiff has requested "
            "entry of Alpine's default by Request for Entry of Default (Form CIV-100) "
            "submitted with this packet; no default against Alpine appears of record "
            "as of the execution of this Declaration.",
        ),
        (
            "PARA",
            "6. Upon entry of Alpine's default, the well-pleaded factual allegations of "
            "the FAC concerning Alpine's liability are deemed admitted. "
            "(<<i:Steven M. Garber & Assocs. v. Eskandarian>> (2007) 150 Cal.App.4th "
            "813, 823; <<i:Kim v. Westmoore Partners, Inc.>> (2011) 201 Cal.App.4th "
            "267, 281.) The well-pleaded allegations include, without limitation: that "
            "Diamond rebranded to Alpine during the pendency of this action; that "
            "Alpine has operated from the same locations as Diamond, including 1201 S "
            "Soderquist Road, Turlock, California, under the same Osmani family "
            "ownership and management; and that Alpine is therefore liable for "
            "Diamond's obligations in this action as its successor in interest, mere "
            "continuation, de facto merger, and/or alter ego, and/or by reason of a "
            "fraudulent transfer of Diamond's business and assets to Alpine.",
        ),
        (
            "PARA",
            "7. This Declaration addresses only the amount and proof of damages as "
            "against Alpine. I have made no effort to relitigate liability, which will "
            "be deemed established upon entry of Alpine's default, nor to relitigate "
            "the underlying fraud and misrepresentation claims against Diamond, which "
            "were proved up "
            "separately -- and on the same exhibits reattached hereto -- in the default "
            "judgment package previously submitted as to Diamond.",
        ),
        ("HEADER", "III.  SUCCESSOR LIABILITY IS DERIVATIVE, NOT ADDITIONAL"),
        (
            "PARA",
            "8. Alpine's liability in this action is derivative of Diamond's liability. "
            "Alpine is not sued for independently committing fraud, misrepresentation, "
            "or breach of contract in the underlying vehicle sale transaction; rather, "
            "Alpine is sued as the entity that has, by operation of the "
            "successor-liability and alter-ego doctrines pleaded in the FAC, become "
            "answerable for the single judgment obligation that Diamond itself already "
            "owes to Plaintiff by reason of Diamond's own default.",
        ),
        (
            "PARA",
            "9. Accordingly, Plaintiff does NOT seek, and this Declaration does NOT "
            "request, an additional or duplicative award of damages against Alpine on "
            "top of the judgment sought against Diamond. Plaintiff instead requests "
            "that judgment be entered against Alpine in the same total amount requested "
            "against Diamond, on a joint and several basis, so that Plaintiff may "
            "recover the single judgment sum from either or both defendants, without "
            "any double recovery. This is consistent with the [Proposed] Judgment (Form "
            "JUD-100) submitted with this packet, which at item 8 expressly provides "
            "that Alpine Truck Sales, Inc. is jointly and severally liable with Diamond "
            "Truck Sales, Inc. as Diamond's successor, mere continuation, alter ego, "
            "and/or fraudulent transferee.",
        ),
        ("HEADER", "IV.  DAMAGES (SAME SUM AS THE DIAMOND JUDGMENT)"),
        (
            "PARA",
            "10. The itemized calculation of damages is set forth in full in the "
            "Declaration in Support of Request for Default Judgment previously filed "
            "against Diamond, and in Attachment 4b to Plaintiff's Case Management "
            "Statement (Form CM-110) filed July 20, 2026, both of which are "
            "incorporated herein by reference. The supporting documentary exhibits "
            "(Exhibits 1 through 10) are attached to this Declaration for completeness. "
            "In summary: documented out-of-pocket losses of $20,218.65; additional "
            "sworn, undocumented out-of-pocket losses of $5,750.00; conservatively "
            "calculated lost commercial income of $23,400.00 (18 weeks x $1,300/week); "
            "and prejudgment interest under Civil Code section 3287(a) (7%, "
            "approximately 3.04 years through June 15, 2026) of $4,302.55 -- for a "
            "total compensatory judgment of $53,671.20. Plaintiff does not seek "
            "punitive damages in this filing.",
        ),
        (
            "PARA",
            "11. The resulting total default judgment amount requested -- as against "
            "Diamond, and, jointly and severally on the same sum, as against Alpine -- "
            "is $53,671.20. Consistent with CIV-100 item 7f and Plaintiff's approved "
            "fee waiver, costs of suit are waived; no costs amount is included in the "
            "judgment total.",
        ),
        ("HEADER", "V.  INDEX OF EXHIBITS"),
        (
            "PARA",
            "12. The following exhibits, previously submitted in support of the default "
            "judgment prove-up against Diamond, are attached hereto as Exhibits 1 "
            "through 10 and incorporated herein by reference:",
        ),
    ]
    for ex in EXHIBITS:
        content.append(("LIST_ITEM", ex))
    content.extend(
        [
            ("HEADER", "VI.  CONCLUSION"),
            (
                "PARA",
                "13. For the foregoing reasons, Plaintiff respectfully requests that the "
                "Court enter default judgment against Defendant ALPINE TRUCK SALES, INC. "
                "in the amount of $53,671.20, jointly and severally with the default "
                "judgment sought against Diamond Truck Sales, Inc., with costs of suit "
                "waived.",
            ),
            (
                "PARA",
                "I declare under penalty of perjury under the laws of the State of "
                "California that the foregoing is true and correct.",
            ),
            ("SIGNATURE", signature_block_text()),
        ]
    )
    return content


def build_diamond() -> str:
    out_path = os.path.join(
        OUT_DIR,
        f"_build_Diamond_Declaration_ISO_Default_Judgment_{DECL_TAG}.pdf",
    )
    d = PleadingPaper(
        out_path,
        doc_title_footer=(
            "DECLARATION ISO DEFAULT JUDGMENT -- "
            "NGWA NFORBI v. DIAMOND TRUCK SALES, ET AL."
        ),
    )
    party_block(d)
    right = [
        (f"Case No. {CASE_NO}", False, False),
        ("", False, False),
        ("DECLARATION OF BRENDAN NGWA", True, False),
        ("NFORBI IN SUPPORT OF REQUEST", True, False),
        ("FOR DEFAULT JUDGMENT BY COURT", True, False),
        ("(Cal. Rules of Court, rule 3.1800;", False, False),
        ("Code Civ. Proc. section 585(b))", False, False),
        ("", False, False),
        ("Assigned to: Hon. Waters, Dept. 11B", False, False),
        ("CMC: August 12, 2026", False, False),
        (f"[Date Executed: {EXEC_DATE}]", False, False),
    ]
    d.draw_caption_block(caption_left(), right, caption_size=10, tight_lh=13, boxed=True)
    d.blank_line()
    render_content(d, diamond_content())
    d.save()
    print(f"Generated: {out_path}")
    return out_path


def build_alpine() -> str:
    out_path = os.path.join(
        OUT_DIR,
        f"_build_Alpine_Declaration_ISO_Default_Judgment_{DECL_TAG}.pdf",
    )
    d = PleadingPaper(
        out_path,
        doc_title_footer=(
            "DECLARATION ISO DEFAULT JUDGMENT -- "
            "NGWA NFORBI v. ALPINE TRUCK SALES, INC."
        ),
    )
    party_block(d)
    right = [
        (f"Case No. {CASE_NO}", False, False),
        ("", False, False),
        ("DECLARATION OF BRENDAN NGWA", True, False),
        ("NFORBI IN SUPPORT OF REQUEST", True, False),
        ("FOR DEFAULT JUDGMENT AGAINST", True, False),
        ("ALPINE TRUCK SALES, INC.", True, False),
        ("(Cal. Rules of Court, rule 3.1800;", False, False),
        ("Code Civ. Proc. section 585(b))", False, False),
        ("", False, False),
        ("Assigned to: Hon. Robert T. Waters,", False, False),
        ("Dept. 11B", False, False),
        ("CMC: August 12, 2026", False, False),
        (f"[Date Executed: {EXEC_DATE}]", False, False),
    ]
    d.draw_caption_block(caption_left(), right, caption_size=10, tight_lh=13, boxed=True)
    d.blank_line()
    render_content(d, alpine_content())
    d.save()
    print(f"Generated: {out_path}")
    return out_path


def main() -> None:
    os.makedirs(OUT_DIR, exist_ok=True)
    paths = [build_diamond(), build_alpine()]
    print(f"Done — {len(paths)} declarations (execution date {EXEC_DATE}).")


if __name__ == "__main__":
    main()
