#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Matter 43 — verified complaint, The Hertz Corporation (Palo Alto, req. 43711).

Santa Clara County Superior Court. Four causes of action, no administrative
exhaustion required for any of them:

  (1) Penal Code § 290.46(j)(2)(E), (j)(4)(A)-(B)  — load-bearing count
  (2) ICRAA, Civ. Code §§ 1786.16(a)(2)(B), 1786.50 — document defect
  (3) Labor Code § 432.7(a)(1), (c)                 — pleaded in the alternative
  (4) Bus. & Prof. Code §§ 16600, 16600.1, 16600.5; CCP § 1060 — non-compete

No Fair Employment and Housing Act / Gov. Code § 12952 count: Plaintiff has
elected not to file with the Civil Rights Department. The Nov. 2 notice's
defects are pleaded as facts only.

Default output is an UNSIGNED review draft with bracketed confirmation
notes. Plaintiff must clear every bracket (see FILING GATES in the NOTICE
block) before running with ``--execute``, which strips the brackets and
affixes the universal signature image.

    python3 internal/scripts/matter43-hertz-complaint.py
    python3 internal/scripts/matter43-hertz-complaint.py --exhibits
    python3 internal/scripts/matter43-hertz-complaint.py --execute --date "November 16, 2026" --city "Stockton"
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR / "lib"))
sys.path.insert(0, str(SCRIPT_DIR))

from pleading_paper import CONTENT_LEFT, COURT_LINE1, PleadingPaper  # noqa: E402
from signature_stamp import SIGNATURE_NATIVE_PX, SIGNATURE_PATH  # noqa: E402

ROOT = SCRIPT_DIR.parents[1]
OUT_DIR = ROOT / "internal/public/documents/matter-43"
DEFAULT_OUT = OUT_DIR / "Verified Complaint - Ngwa Nforbi v The Hertz Corporation (Nov 12 2026).pdf"
EXHIBITS_OUT = OUT_DIR / "Exhibits A-F to Verified Complaint - Ngwa Nforbi v The Hertz Corporation.pdf"
DOCS = ROOT / "documents/matter-43"

COURT_LINE2 = "COUNTY OF SANTA CLARA"
FOOTER = "BRENDAN NGWA NFORBI v. THE HERTZ CORPORATION \u2014 COMPLAINT"

_DRAFT_NOTE = re.compile(r"\s*\[\[[^\[\]]+\]\]")


def _filing_text(text: str, execute: bool) -> str:
    """Review-draft notes are written [[like this]] and removed on --execute."""
    if not execute:
        return text.replace("[[", "[").replace("]]", "]")
    return _DRAFT_NOTE.sub("", text).rstrip()


PLAINTIFF_BLOCK = [
    ("BRENDAN NGWA NFORBI", "Times-Bold", 12),
    ("Plaintiff, In Pro Per", "Times-Roman", 12),
    ("1455 Cat Tail Drive", "Times-Roman", 12),
    ("Stockton, CA 95204", "Times-Roman", 12),
    ("Telephone: (209) 801-4442", "Times-Roman", 12),
    ("E-mail: bnn.cdl@gmail.com", "Times-Roman", 12),
]

CAPTION_LEFT = [
    ("BRENDAN NGWA NFORBI, also known", True, False),
    ("as BRENDAN NGWANFORBI,", True, False),
    ("", False, False),
    ("", False, False),
    ("                          Plaintiff,", False, False),
    ("", False, False),
    ("       v.", False, False),
    ("", False, False),
    ("THE HERTZ CORPORATION, a Delaware", True, False),
    ("corporation; and DOES 1 through 25,", True, False),
    ("inclusive,", True, False),
    ("", False, False),
    ("                          Defendants.", False, False),
]

CAPTION_RIGHT = [
    ("Case No. _________________", False, False),
    ("", False, False),
    ("VERIFIED COMPLAINT FOR DAMAGES,", True, False),
    ("CIVIL PENALTY, AND DECLARATORY", True, False),
    ("AND INJUNCTIVE RELIEF", True, False),
    ("", False, False),
    ("(1) Penal Code § 290.46(j);", False, False),
    ("(2) Civ. Code §§ 1786.16, 1786.50", False, False),
    ("      (ICRAA);", False, False),
    ("(3) Labor Code § 432.7;", False, False),
    ("(4) Bus. & Prof. Code §§ 16600,", False, False),
    ("      16600.1, 16600.5; Code Civ.", False, False),
    ("      Proc. § 1060", False, False),
    ("", False, False),
    ("[Unlimited Civil Case]", False, True),
    ("[Jury Trial Demanded]", False, True),
]

SIGNOFF_NAME = "BRENDAN NGWA NFORBI"
SIGNOFF_ROLE = "Plaintiff, In Pro Per"
SIG_LINE = "___________________________________"

# ---------------------------------------------------------------------------
# CONTENT. ("PARA", text, label) entries are auto-numbered; {name} in a later
# paragraph is replaced by the number of the paragraph labelled `name`.
# ---------------------------------------------------------------------------
CONTENT: list[tuple] = [
    ("PARA", "Plaintiff BRENDAN NGWA NFORBI, also known as Brendan Ngwanforbi "
             "(\"Plaintiff\"), alleges as follows:"),

    # ------------------------------------------------------------------ I
    ("HEADER", "I.\nINTRODUCTION"),
    ("PARA",
     "California permits the public to view its Megan's Law registry for one purpose: "
     "to protect a person at risk. It forbids anyone to use that information for "
     "purposes relating to employment. (Pen. Code, § 290.46, subd. (j)(1), (j)(2)(E).) "
     "This action arises because The Hertz Corporation built California registry "
     "status into the hiring standard it applied to Plaintiff, reviewed his registry "
     "results under that standard, and within hours issued a preliminary decision "
     "rescinding the job it had offered him and that he had accepted.", "intro1"),
    ("PARA",
     "On October 22, 2026, Hertz offered Plaintiff, in writing, a full-time Manager "
     "Trainee position at its Palo Alto branch at $23.00 per hour. Plaintiff accepted "
     "the same day. The offer stated that if Plaintiff's background check \"does not "
     "meet company standards, my contingent offer will be rescinded.\" Hertz then "
     "ordered a background report that included a \"National Sex Offender Registry\" "
     "search. Hertz's screening vendor graded each registry result against Hertz's "
     "\"Company Standards\": the result that found no registry entry was graded "
     "\"Meets Company Standards,\" and the two results that found Plaintiff's "
     "California registry entry were graded \"Client Review Required.\" The vendor "
     "printed on the report, directly beneath those entries, that California registry "
     "information \"may not be used for employment purposes except to protect a "
     "person at risk. See CA Penal Code Section 290.46.\""),
    ("PARA",
     "The completed report was delivered at 2:29 a.m. Pacific time on November 2, "
     "2026. At 10:19 a.m. the same morning, Hertz sent Plaintiff a notice stating "
     "that, \"[b]ased on a review of the results of your background report and "
     "Company's eligibility criteria,\" information in the report \"may result in "
     "Company deciding not to offer you\" employment, and referring to \"the "
     "Company's preliminary decision recinding the offer of employment.\" The notice "
     "listed, as information \"including\" the basis, a single line: \"[Criminal "
     "Information] Alcohols related offenses-Does not meet.\" The report Hertz "
     "reviewed contains no alcohol-related criminal conviction. Hertz had held the "
     "only alcohol-related information in the report, Plaintiff's Department of Motor "
     "Vehicles record, since October 23, 2026, and had continued to onboard him for "
     "ten days without objection. Hertz acted only after the registry results arrived."),
    ("PARA",
     "Plaintiff seeks the remedies the Legislature provided for that misuse, the "
     "statutory remedy for Hertz's defective California investigative-report "
     "disclosure, the remedy for Hertz's use of a non-conviction arrest record, and "
     "declaratory and injunctive relief against Hertz's requirement that a California "
     "applicant sign a non-competition agreement as a condition of employment."),

    # ------------------------------------------------------------------ II
    ("HEADER", "II.\nPARTIES"),
    ("PARA",
     "Plaintiff is an individual residing in Stockton, San Joaquin County, "
     "California. Hertz's documents identify him as Brendan Ngwa Nforbi (the offer "
     "letter and onboarding correspondence) and as Brendan Ngwanforbi (the background "
     "report and the November 2 notice). Each name refers to Plaintiff."),
    ("PARA",
     "Defendant The Hertz Corporation (\"Hertz\") is, on information and belief, a "
     "Delaware corporation with its principal place of business at 8501 Williams "
     "Road, Estero, Florida 33928. Hertz operates vehicle-rental branches in "
     "California, including the Hertz Local Edition branch at 816 San Antonio Road, "
     "Palo Alto, California 94303, and a location at 725 Ridder Park Drive, San Jose, "
     "California. Hertz issued the offer, procured the background report, adopted "
     "the adjudication rules applied to it, and issued the November 2 notice."),
    ("PARA",
     "Plaintiff does not know the true names or capacities of the defendants sued as "
     "DOES 1 through 25 and therefore sues them by fictitious names under Code of "
     "Civil Procedure section 474. On information and belief, they include persons "
     "and entities that participated in setting, applying, or ratifying the screening "
     "criteria and employment decision alleged here, including Hertz affiliates and "
     "agents. On information and belief, the job application at issue was processed "
     "in part in the name of Hertz's parent, Hertz Global Holdings, Inc.: on October "
     "22, 2026, Hertz's tax-credit screening vendor wrote to Plaintiff regarding \"your "
     "recently submitted job application with Hertz Global Holdings, Inc.\" Plaintiff "
     "will amend to state the true names and capacities of the DOE defendants when "
     "ascertained."),
    ("PARA",
     "On information and belief, each defendant was the agent, employee, or "
     "co-venturer of each other defendant and acted within the scope of that "
     "relationship, and each defendant authorized, ratified, or adopted the acts of "
     "the others alleged here."),

    # ------------------------------------------------------------------ III
    ("HEADER", "III.\nJURISDICTION AND VENUE"),
    ("PARA",
     "This Court has subject-matter jurisdiction under article VI, section 10 of the "
     "California Constitution. The amount in controversy exceeds the jurisdictional "
     "minimum for an unlimited civil case. Each cause of action arises under "
     "California law."),
    ("PARA",
     "This Court has personal jurisdiction over Hertz under Code of Civil Procedure "
     "section 410.10. Hertz operates branches in California, interviewed Plaintiff in "
     "San Jose, offered him a position in Palo Alto, procured a California "
     "investigative consumer report about a California resident for a California job, "
     "and directed the November 2 notice to him in California."),
    ("PARA",
     "Venue is proper in Santa Clara County under Code of Civil Procedure sections "
     "395(a) and 395.5. The position was to be performed in Palo Alto, the interview "
     "occurred in San Jose, and the obligations and liability at issue arose in "
     "connection with Hertz's Santa Clara County employment."),

    # ------------------------------------------------------------------ IV
    ("HEADER", "IV.\nFACTUAL ALLEGATIONS"),
    ("SUBHEAD", "A. Hertz Offers Plaintiff the Palo Alto Manager Trainee Position"),
    ("PARA",
     "On or about October 21 and 22, 2026, Hertz manager Kathleen Williams arranged "
     "for Plaintiff to interview at Hertz's Ridder Park location in San Jose. On "
     "October 22, 2026, at approximately 3:38 p.m., Hertz Talent Acquisition Partner "
     "Gloria Williams e-mailed Plaintiff: \"The team would like to extend an offer to "
     "you. Congratulations!\" At approximately 3:40 p.m., Kathleen Williams messaged "
     "Plaintiff that he should receive an offer for Manager Trainee at the Palo Alto "
     "location. At 4:49 p.m., Plaintiff replied that he \"happily accept[ed] the "
     "offer.\""),
    ("PARA",
     "Hertz's written offer letter, dated October 22, 2026, states: \"We are pleased "
     "to confirm our offer of employment with The Hertz Corporation for the position "
     "of Manager Trainee (Full time) based at 816 San Antonio Rd, Palo Alto, CA 94303 "
     "... This position reports to Kathleen Williams. Your base salary, paid on an "
     "hourly basis, will be $23.00.\" The letter describes the Branch Manager Trainee "
     "role as \"the entry position to our management career path.\" A true copy of "
     "the offer letter is attached as Exhibit A.", "offer"),
    ("PARA",
     "The offer letter defines the background checks on which the offer is "
     "contingent: \"Please understand this offer is contingent upon the successful "
     "completion of a pre-employment MVR check (as applicable), criminal, employment "
     "and education background checks ('Background Checks').\" The definition does "
     "not include a sex-offender registry search.", "contingency"),
    ("PARA",
     "The offer letter then states the standard that decides whether the offer "
     "survives: \"I acknowledge that if my background check does not meet company "
     "standards, my contingent offer will be rescinded, and my employment will be "
     "null and void.\"", "standards"),
    ("PARA",
     "The offer letter also states: \"It is a fundamental term and condition of your "
     "employment that you must execute and deliver to the undersigned the below "
     "details regarding Employee Confidentiality & Non-Competition.\"", "nc_offer"),
    ("PARA",
     "Plaintiff accepted the offer through Hertz's online portal. At 5:42 p.m. on "
     "October 22, 2026, the portal showed the Manager Trainee position, requisition "
     "43711, with the status \"Offer Accepted.\" On October 23, 2026, Gloria Williams "
     "sent Plaintiff a \"Pre-Boarding\" e-mail for \"43711 Manager Trainee\" stating, "
     "\"We are excited you are joining the winning team!\" and directing him to "
     "complete a background request from HireRight, LLC (\"HireRight\"). True copies "
     "of the October 22 and 23 e-mails are attached as Exhibit B.", "accepted"),

    ("SUBHEAD", "B. The California Investigative-Report Disclosure Packet"),
    ("PARA",
     "On October 23, 2026, at approximately 3:03 to 3:04 p.m. Pacific time, Plaintiff "
     "completed HireRight's electronic consent process for Hertz. The record HireRight "
     "preserved of that process includes a single twelve-page document titled, on its "
     "first page, \"Disclosure Regarding Investigative Consumer Report\" (the "
     "\"Disclosure Packet\"). A true copy of the Disclosure Packet is attached as "
     "Exhibit C.", "packet"),
    ("PARA",
     "The first page of the Disclosure Packet identifies the employer as \"The Herz "
     "Corporation.\" Pages one and two, before the packet's only signature block on "
     "page three, contain, in addition to the investigative-report disclosure: notices "
     "directed to residents of Massachusetts, Minnesota, New Jersey, New York, and "
     "Washington; a City of Los Angeles \"Fair Chance Initiative for Hiring "
     "Ordinance\" notice, reproduced in full in English and again in Spanish; and a "
     "checkbox for \"California, Minnesota and Oklahoma residents\" to request a copy "
     "of the report."),
    ("PARA",
     "The document headed \"(CALIFORNIA APPLICANTS/EMPLOYEES ONLY) CALIFORNIA "
     "DISCLOSURE\" appears on page eight of the Disclosure Packet, after the signature "
     "block. It bears no signature. It is bound in the same document as a four-page "
     "federal summary of rights, two pages of New York Correction Law article 23-A, "
     "and two pages of San Francisco Fair Chance Ordinance workplace posters.",
     "cadisclosure"),
    ("PARA",
     "The California Disclosure lists the \"specific types of information about you "
     "that may be obtained,\" including \"National Sex Offender Registry\" and \"MVR "
     "Express.\" It does not list employment or education verification."),
    ("PARA",
     "At 3:04 p.m. on October 23, 2026, Hertz's \"Pre Employment (Field)\" account "
     "submitted HireRight order OR-102326-NH87V, package \"Field (Driver Required),\" "
     "for requisition 43711. The report was requested by Kesha Nedio-Casey, Hertz "
     "Pre Employment (Field), 8501 Williams Road, Estero, Florida."),

    ("SUBHEAD", "C. Hertz Receives the Driving Record on October 23 and Continues to Onboard Plaintiff"),
    ("PARA",
     "HireRight completed the motor-vehicle-record (\"MVR\") component at 3:04 p.m. on "
     "October 23, 2026. At 3:05 p.m., HireRight notified Plaintiff that it had "
     "provided his MVR to \"Gloria Williams, The Hertz Corporation.\" HireRight's "
     "activity log records: \"Oct 23, 2026 3:07 PM -- MVR Express report provided to "
     "The Hertz Corporation.\" A true copy of the notice is attached as Exhibit D.",
     "mvr_time"),
    ("PARA",
     "The MVR shows Plaintiff's California Class C driver's license, issued July 21, "
     "2026 and expiring May 12, 2027, with the status \"VALID.\" It also shows two "
     "administrative actions by the Department of Motor Vehicles, both concluded "
     "before Hertz made its offer: a suspension for \"refusal or failure to complete "
     "chemical test\" with a privilege reinstatement date of May 19, 2026; and a "
     "commercial-vehicle disqualification for refusing to submit to a test, with a "
     "clear date of November 30, 2025. The only conviction in the MVR is an October "
     "2, 2024 infraction for an unregistered vehicle under Vehicle Code section "
     "4000(a), which carries zero points and is not alcohol-related.", "mvr"),
    ("PARA",
     "Neither DMV action is a criminal conviction. A chemical-test refusal action "
     "under the Vehicle Code follows a request by a peace officer to a person who has "
     "been arrested. "
     "The refusal action reflected in the MVR followed an arrest of Plaintiff, and that "
     "arrest did not result in a conviction. The background report reflects no "
     "alcohol-related conviction in any jurisdiction searched, including San Joaquin "
     "County, Santa Clara County, Sheridan County, Wyoming, the Eastern District of "
     "California, and the District of Wyoming.", "arrest"),
    ("PARA",
     "Hertz did not issue any adverse notice after receiving the MVR on October 23, "
     "2026. For the next ten days Hertz left Plaintiff's status at \"Offer Accepted\" "
     "and continued its onboarding process."),

    ("SUBHEAD", "D. The Registry Results and Hertz's \"Company Standards\""),
    ("PARA",
     "The California Department of Justice maintains an internet website, created by "
     "and operated under Penal Code section 290.46, that makes information from "
     "California's sex-offender registry available to the public (the \"Megan's Law "
     "Website\"). Plaintiff is a person whose information is displayed on the "
     "Megan's Law Website.", "listed"),
    ("PARA",
     "The United States Department of Justice operates two different sex-offender "
     "systems. The Dru Sjodin National Sex Offender Public Website (\"NSOPW\"), "
     "established by 34 U.S.C. section 20922, is open to the public. The United "
     "States Department of Justice describes NSOPW as a search portal that uses web "
     "services to search each jurisdiction's public registry website in real time, "
     "and states that an offender who is not displayed on a jurisdiction's public "
     "registry website will not appear on NSOPW. The National Sex Offender Registry "
     "(\"NSOR\"), established by 34 U.S.C. section 20921, is a file maintained by the "
     "Federal Bureau of Investigation and is accessible only to law-enforcement and "
     "other authorized criminal-justice agencies.", "nsopw"),
    ("PARA",
     "HireRight is a private consumer reporting agency. On information and belief, "
     "HireRight is not a law-enforcement or criminal-justice agency and has no access "
     "to NSOR. A private consumer reporting agency's sex-offender search \"performed "
     "through the United States Department of Justice\" is therefore, on information "
     "and belief, an NSOPW search. For a California registrant, an NSOPW search "
     "returns the information that California displays on the Megan's Law Website."),
    ("PARA",
     "Hertz's order included three \"National Sex Offender Registry\" subrequests, one "
     "for each of three forms of Plaintiff's name. Each subrequest bears the comment: "
     "\"National Sex Offender Registry search performed through the United States "
     "Department of Justice.\""),
    ("PARA",
     "The subrequest for \"Brendan Ngwa\" returned \"Not in Registry.\" HireRight "
     "graded it \"Meets Company Standards.\"", "meets"),
    ("PARA",
     "The two subrequests run on the other forms of Plaintiff's name returned \"In Registry\" on "
     "October 30, 2026, at 11:25 a.m. and 12:48 p.m. Pacific time. HireRight graded "
     "each \"Client Review Required.\" The returned entries listed aliases for "
     "Plaintiff, including \"NGWA-NFORBI, BRENDAN.\"", "crr"),
    ("PARA",
     "HireRight's researchers entered the following notes on those entries on October "
     "30, 2026: \"APPLICANT IS LISTED ON THE SEX OFFENDER REGISTRY IN THE STATE OF "
     "CA\"; \"Verified by Name and DOB\"; and \"Information from the California Sex "
     "Offenders' Registry may not be used for employment purposes except to protect "
     "a person at risk. See CA Penal Code Section 290.46. Only use this information "
     "to make an employment decision as expressly allowed by CA law.\"", "warning"),
    ("PARA",
     "The report states that the grades were assigned under adjudication rules named "
     "\"The Hertz Corporation (Shell) (GL-HTZ001-001) v1.7\" and \"AutoLibrarySet - "
     "Excl. MVR, EDU, EMP - Managed Adjudication 3.0.\" The phrase \"Meets Company "
     "Standards\" refers to Hertz's company standards: the same standards the offer "
     "letter makes the condition of Plaintiff's employment (paragraph {standards})."),
    ("PARA",
     "On information and belief, Hertz selected the \"National Sex Offender Registry\" "
     "product for its California \"Field (Driver Required)\" package and adopted "
     "adjudication rules under which a registry result of \"Not in Registry\" meets "
     "Hertz's company standards, and a registry result of \"In Registry\" does not meet "
     "them automatically but must be reviewed by Hertz personnel. Under those rules, "
     "California registry status is a criterion of Hertz's employment eligibility "
     "standard.", "design"),

    ("SUBHEAD", "E. The Report Is Completed and Hertz Acts Within Hours"),
    ("PARA",
     "The report also contained a Santa Clara County Superior Court record (case "
     "C1761642) reflecting felony convictions, with a disposition date of January 12, "
     "2018, for offenses arising on February 26, 2017, which require registration "
     "under Penal Code section 290. The report states a parole/release date of "
     "December 2, 2020. HireRight graded that record \"Client Review Required.\" "
     "Plaintiff pleads this fact because it is in the report; the November 2 notice "
     "did not identify it."),
    ("PARA",
     "HireRight's activity log records that it adjudicated the completed report at "
     "2:29 a.m. Pacific time on November 2, 2026, with the overall result \"Client "
     "Review Required.\" A true copy of the complete report is attached as Exhibit E."),
    ("PARA",
     "At 10:19 a.m. Pacific time on November 2, 2026, less than eight hours later, "
     "HireRight transmitted to Plaintiff, on Hertz's behalf, a letter from The Hertz "
     "Corporation dated November 2, 2026 (the \"Notice\"). A true copy of the Notice "
     "and its transmittal e-mail is attached as Exhibit F.", "notice"),
    ("PARA",
     "The Notice states: \"Based on a review of the results of your background report "
     "and Company's eligibility criteria, we are notifying you that there is "
     "information in your background report that may result in Company deciding not "
     "to offer you ... employment ... including the following specific information "
     "identified in your background report: [Criminal Information] Alcohols related "
     "offenses-Does not meet.\""),
    ("PARA",
     "The Notice refers to \"the Company's preliminary decision recinding the offer of "
     "employment,\" and invites \"evidence in mitigation of the specific criminal "
     "information identified above.\""),
    ("PARA",
     "The Notice does not state a deadline to respond. Where a date should appear, it "
     "reproduces an unfilled bracket: \"[Date (at least five business days from the "
     "date of receipt of the notice. ... (iii) If notice is transmitted through email, "
     "the notice shall be deemed received two business days after it is sent.)].\" "
     "Elsewhere the Notice states that Hertz will not make a final decision \"for at "
     "least five (5) business days from the date of this letter.\""),
    ("PARA",
     "The Notice does not mention the sex-offender registry, does not identify any "
     "person at risk, does not identify any statute authorizing Hertz to use registry "
     "information, and does not identify any criminal conviction."),
    ("PARA",
     "The report contains no alcohol-related criminal conviction. The only "
     "alcohol-related information in the report is the DMV administrative information "
     "described in paragraph {mvr}, which Hertz had possessed since October 23, 2026."),

    ("SUBHEAD", "F. Hertz Used the Registry Information for Employment Purposes"),
    ("PARA",
     "On information and belief, Hertz used the California registry information in "
     "Plaintiff's report for purposes relating to employment, in at least the "
     "following ways: (a) by configuring its California employment-screening package "
     "to retrieve California registry information about applicants; (b) by adopting "
     "and applying company standards under which Plaintiff's registry status "
     "determined whether his background check \"meet[s] company standards,\" the "
     "condition on which the offer letter states his employment depends; (c) by "
     "subjecting Plaintiff's \"In Registry\" results to \"Client Review\" by Hertz "
     "personnel for the purpose of deciding his employment; and (d) by issuing, after "
     "that review and \"[b]ased on a review of the results of [his] background report "
     "and Company's eligibility criteria,\" a preliminary decision rescinding his "
     "offer.", "use"),
    ("PARA",
     "The facts supporting that belief include: the offer letter's \"company "
     "standards\" rescission term (paragraph {standards}); the grading of Plaintiff's "
     "registry results against \"Company Standards\" (paragraphs {meets} and {crr}); "
     "the adjudication rules bearing Hertz's name; the ten days in which Hertz held "
     "the only alcohol-related information without acting (paragraph {mvr_time}); the "
     "issuance of the Notice within eight hours after the registry results were "
     "delivered in the completed report; the Notice's statement that the basis "
     "\"includ[es]\" the listed line, which on its face is not exclusive; and the "
     "absence of any alcohol-related criminal conviction to which the Notice's "
     "\"[Criminal Information]\" heading could refer."),
    ("PARA",
     "The decision-making records that would show precisely how Hertz applied its "
     "company standards to the registry results, including the rules in \"The Hertz "
     "Corporation (Shell) (GL-HTZ001-001) v1.7,\" the identity of the Hertz personnel "
     "who performed the \"Client Review,\" the screens they viewed, and their notes, "
     "are exclusively in the possession of Hertz and its vendor."),
    ("PARA",
     "Hertz knew, when it reviewed the report, that California prohibits use of "
     "registry information for employment. The prohibition was printed on the report "
     "beneath the registry entries (paragraph {warning})."),
    ("PARA",
     "No person at risk was identified in connection with the Palo Alto Manager "
     "Trainee position, and Hertz did not use the registry information to protect "
     "any identified person at risk. On information and belief, no statute authorized "
     "Hertz, a vehicle-rental company, to obtain or use California registry "
     "information for employment, and Hertz did not obtain the information through "
     "Penal Code section 11105 or 11105.3."),
    ("PARA",
     "Plaintiff's signature on the Disclosure Packet did not authorize Hertz to use "
     "registry information for employment. Penal Code section 290.46, subdivision "
     "(j), regulates use and serves a public purpose, and a law established for a "
     "public reason cannot be contravened by a private agreement. (Civ. Code, "
     "§ 3513.)"),

    ("SUBHEAD", "G. Plaintiff's Status and Harm"),
    ("PARA",
     "The Notice states no deadline to respond, identifies no conviction, and does "
     "not identify which of the items reviewed formed the basis of Hertz's "
     "preliminary decision. Hertz has not communicated with Plaintiff since it sent "
     "the Notice.", "status"),
    ("PARA",
     "As of the filing of this Complaint, Hertz has not withdrawn its preliminary "
     "decision, has not scheduled a start date, and has not permitted Plaintiff to "
     "begin work.", "status2"),
    ("PARA",
     "As a direct result of Hertz's conduct, Plaintiff has suffered and continues to "
     "suffer harm, including anxiety, humiliation, and emotional distress at being "
     "screened out of an accepted job on the basis of information the law forbids "
     "Hertz to use for that purpose; loss of the opportunity to begin the management "
     "career path the offer described; and, to the extent Hertz's decision becomes or "
     "has become final, loss of the wages and benefits of a full-time position at "
     "$23.00 per hour, in amounts according to proof."),

    # ------------------------------------------------------------------ V
    ("HEADER", "V.\nFIRST CAUSE OF ACTION"),
    ("SUBHEAD", "Unlawful Use of Megan's Law Information for Employment\n"
                "(Pen. Code, § 290.46, subd. (j)(2)(E), (j)(4)(A)-(B))\n"
                "(Against Hertz and DOES 1-25)"),
    ("PARA",
     "Plaintiff incorporates paragraphs {intro1} through {standards} and {packet} "
     "through the end of Part IV.G.", "c1start"),
    ("PARA",
     "Penal Code section 290.46, subdivision (j)(1), authorizes a person to use "
     "information disclosed pursuant to section 290.46 only to protect a person at "
     "risk. Subdivision (j)(2)(E) provides that, except as authorized under "
     "subdivision (j)(1) or any other provision of law, use of information disclosed "
     "pursuant to section 290.46 is prohibited for purposes relating to employment."),
    ("PARA",
     "The California registry information in Plaintiff's report was information "
     "disclosed pursuant to section 290.46. California disclosed it to the public "
     "through the Megan's Law Website, and on information and belief it reached Hertz "
     "through an NSOPW search that retrieved it from that website (paragraphs "
     "{listed} through {warning})."),
    ("PARA",
     "Hertz used that information for purposes relating to employment, as alleged in "
     "paragraphs {design} and {use}."),
    ("PARA",
     "Hertz's use was not to protect a person at risk and was not authorized by any "
     "other provision of law."),
    ("PARA",
     "Under subdivision (j)(4)(A), a person who uses information disclosed pursuant "
     "to section 290.46 in violation of subdivision (j)(2) is liable for (i) actual "
     "damages; (ii) an amount determined by the trier of fact not exceeding three "
     "times the actual damages and not less than $250; (iii) attorney's fees; and "
     "(iv) exemplary damages or a civil penalty not exceeding $25,000. Plaintiff "
     "seeks each of those remedies, pleading exemplary damages and the civil penalty "
     "in the alternative."),
    ("PARA",
     "Hertz acted with knowledge of the prohibition, which was printed on the report "
     "it reviewed, and with conscious disregard of Plaintiff's rights. The registry "
     "criterion was embedded in company-wide adjudication rules bearing Hertz's name, "
     "which on information and belief were adopted, authorized, or ratified by Hertz "
     "officers, directors, or managing agents. Plaintiff is entitled to exemplary "
     "damages under subdivision (j)(4)(A) and Civil Code section 3294."),
    ("PARA",
     "On information and belief, Hertz applies the same registry criterion to every "
     "California applicant screened under its \"Field (Driver Required)\" package. That "
     "is a pattern or practice of misuse of section 290.46 information. Plaintiff, as "
     "a person aggrieved by that misuse, seeks preventive relief under subdivision "
     "(j)(4)(B), including a permanent injunction prohibiting Hertz from retrieving, "
     "grading, or reviewing California Megan's Law information for employment "
     "purposes."),

    # ------------------------------------------------------------------ VI
    ("HEADER", "VI.\nSECOND CAUSE OF ACTION"),
    ("SUBHEAD", "Investigative Consumer Reporting Agencies Act --\n"
                "Non-Standalone Disclosure\n"
                "(Civ. Code, §§ 1786.16, subd. (a)(2)(B), 1786.50)\n"
                "(Against Hertz and DOES 1-25)"),
    ("PARA",
     "Plaintiff incorporates paragraphs {offer}, {contingency}, and {packet} through "
     "{notice}."),
    ("PARA",
     "The report Hertz procured is an \"investigative consumer report\" under Civil "
     "Code section 1786.2. Hertz's own disclosure acknowledges that in California the "
     "term \"includes background reports with or without information obtained from "
     "personal interviews.\""),
    ("PARA",
     "Civil Code section 1786.16, subdivision (a)(2)(B), requires a person procuring "
     "an investigative consumer report for employment purposes to provide, before the "
     "report is procured, a clear and conspicuous disclosure in writing \"in a "
     "document that consists solely of the disclosure.\""),
    ("PARA",
     "Hertz did not do so. The only document Plaintiff signed in the Disclosure Packet "
     "combined the investigative-report disclosure with notices for five other states "
     "and a Los Angeles municipal ordinance in two languages, and misidentified the "
     "employer as \"The Herz Corporation.\" The California-specific disclosure was not "
     "a separate signed document; it was bound, unsigned, into the same twelve-page "
     "document with federal, New York, and San Francisco materials (paragraphs "
     "{packet} through {cadisclosure})."),
    ("PARA",
     "Hertz procured the report on October 23, 2026, after providing that "
     "non-compliant disclosure, and used the report to issue the Notice."),
    ("PARA",
     "Under Civil Code section 1786.50, subdivision (a), Hertz is liable for actual "
     "damages or $10,000, whichever is greater, plus costs and reasonable attorney's "
     "fees."),
    ("PARA",
     "Hertz's violation was willful or grossly negligent. Hertz is a large, "
     "sophisticated national employer that procures investigative consumer reports "
     "on California applicants as a matter of routine, and the requirement that the "
     "disclosure stand alone has been settled and publicized since at least 2019. "
     "Plaintiff is entitled to punitive damages under section 1786.50, subdivision "
     "(b)."),

    # ------------------------------------------------------------------ VII
    ("HEADER", "VII.\nTHIRD CAUSE OF ACTION"),
    ("SUBHEAD", "Use of a Non-Conviction Arrest Record in Hiring\n"
                "(Lab. Code, § 432.7, subds. (a)(1), (c))\n"
                "(Against Hertz and DOES 1-25, in the Alternative)"),
    ("PARA",
     "Plaintiff incorporates paragraphs {offer}, {standards}, {mvr_time} through "
     "{arrest}, and {notice} through the end of Part IV.E."),
    ("PARA",
     "This cause of action is pleaded in the alternative to the First Cause of Action "
     "to the extent Hertz contends that its preliminary decision rested on the "
     "\"Alcohols related offenses\" identified in the Notice."),
    ("PARA",
     "Labor Code section 432.7, subdivision (a)(1), prohibits an employer from "
     "utilizing, as a factor in determining any condition of employment, including "
     "hiring, any record of arrest or detention that did not result in conviction."),
    ("PARA",
     "The only alcohol-related information in Plaintiff's report is the DMV "
     "chemical-test refusal information, which records the consequence of an arrest "
     "that did not result in a conviction (paragraph {arrest}). Hertz labeled that "
     "information \"[Criminal Information]\" and, by its own account, used it as a "
     "factor in its preliminary decision to rescind Plaintiff's offer."),
    ("PARA",
     "The use was not justified by any job requirement. Plaintiff's Class C license "
     "was valid, the refusal suspension had ended with reinstatement before the offer, "
     "and the commercial-vehicle disqualification had cleared before the offer and "
     "concerned a license class the Manager Trainee position did not require."),
    ("PARA",
     "Under Labor Code section 432.7, subdivision (c), Plaintiff is entitled to "
     "recover actual damages or $200, whichever is greater, plus costs and reasonable "
     "attorney's fees, and any enhanced amount the statute provides for an "
     "intentional violation. Hertz's violation was intentional."),

    # ------------------------------------------------------------------ VIII
    ("HEADER", "VIII.\nFOURTH CAUSE OF ACTION"),
    ("SUBHEAD", "Unlawful Non-Compete Condition; Declaratory and Injunctive Relief\n"
                "(Bus. & Prof. Code, §§ 16600, 16600.1, 16600.5; Code Civ. Proc., § 1060)\n"
                "(Against Hertz and DOES 1-25)"),
    ("PARA",
     "Plaintiff incorporates paragraphs {offer}, {nc_offer}, and {accepted}."),
    ("PARA",
     "Business and Professions Code section 16600 provides that every contract by "
     "which anyone is restrained from engaging in a lawful profession, trade, or "
     "business of any kind is to that extent void, and is to be read broadly to void "
     "noncompete agreements in the employment context. Section 16600.1 makes it "
     "unlawful to include a noncompete clause in an employment contract, or to require "
     "an employee to enter a noncompete agreement, that does not satisfy a statutory "
     "exception. Section 16600.5 provides that an employer shall not enter into a "
     "contract with an employee or prospective employee that includes a provision "
     "that is void under that chapter, and authorizes a prospective employee to bring "
     "a private action for injunctive relief, actual damages, or both, with "
     "reasonable attorney's fees and costs to a prevailing plaintiff."),
    ("PARA",
     "Plaintiff was a prospective employee. Hertz's offer letter, which Plaintiff "
     "accepted, made his execution of an \"Employee Confidentiality & Non-Competition\" "
     "agreement a \"fundamental term and condition\" of his employment. On information and "
     "belief, the Employee Confidentiality & Non-Competition agreement contains a "
     "covenant restraining Plaintiff from engaging in competing work after his "
     "employment ends, and no statutory exception applies.", "noncompete"),
    ("PARA",
     "By conditioning Plaintiff's employment on a non-competition agreement, Hertz "
     "entered into a contract with a prospective employee that includes a provision "
     "void under section 16600, in violation of sections 16600.1 and 16600.5. On "
     "information and belief, Hertz uses the same offer-letter term for California "
     "hires generally."),
    ("PARA",
     "An actual and present controversy exists between Plaintiff and Hertz concerning "
     "the validity and enforceability of the non-competition term. Plaintiff seeks a "
     "declaration under Code of Civil Procedure section 1060 that the term, and any "
     "non-competition covenant it requires, is void and unenforceable as to him; an "
     "injunction under section 16600.5 prohibiting Hertz from requiring or enforcing "
     "it; actual damages according to proof; and costs and any attorney's fees "
     "incurred."),

    # ------------------------------------------------------------------ IX
    ("HEADER", "IX.\nPRESERVATION OF EVIDENCE"),
    ("PARA",
     "Hertz is on notice of this action and must preserve all records concerning "
     "Plaintiff and requisition 43711, including: Oracle candidate 2847550 status "
     "history; HireRight order OR-102326-NH87V in every version; the adjudication "
     "rules \"The Hertz Corporation (Shell) (GL-HTZ001-001) v1.7\" and \"Managed "
     "Adjudication 3.0\" and their configuration for registry, MVR, and criminal "
     "results; the source, endpoint, and raw results of each registry subrequest; "
     "the identity, screens, notes, and communications of each person who performed "
     "the November 2 \"Client Review\"; the native electronic-consent records for the "
     "October 23 disclosures; and the Employee Confidentiality & Non-Competition "
     "agreement and its use for California hires."),

    # ------------------------------------------------------------------ X
    ("HEADER", "X.\nPRAYER FOR RELIEF"),
    ("PARA", "Plaintiff prays for judgment against Hertz and DOES 1 through 25 as follows:"),
    ("LIST_ITEM", "On the First Cause of Action:"),
    ("LIST_ITEM", "1. Actual damages, including emotional-distress damages and any lost "
                  "wages and benefits, according to proof;"),
    ("LIST_ITEM", "2. An additional amount determined by the trier of fact, not exceeding "
                  "three times actual damages and not less than $250 (Pen. Code, § 290.46, "
                  "subd. (j)(4)(A));"),
    ("LIST_ITEM", "3. Exemplary damages or, in the alternative, a civil penalty not "
                  "exceeding $25,000 (ibid.; Civ. Code, § 3294);"),
    ("LIST_ITEM", "4. Preventive relief, including a permanent injunction, under Penal "
                  "Code section 290.46, subdivision (j)(4)(B);"),
    ("LIST_ITEM", "On the Second Cause of Action:"),
    ("LIST_ITEM", "5. Actual damages or $10,000, whichever is greater (Civ. Code, "
                  "§ 1786.50, subd. (a));"),
    ("LIST_ITEM", "6. Punitive damages (Civ. Code, § 1786.50, subd. (b));"),
    ("LIST_ITEM", "On the Third Cause of Action:"),
    ("LIST_ITEM", "7. Actual damages or $200, whichever is greater, and any enhanced "
                  "amount for an intentional violation (Lab. Code, § 432.7, subd. (c));"),
    ("LIST_ITEM", "On the Fourth Cause of Action:"),
    ("LIST_ITEM", "8. A declaration that Hertz's non-competition term and any "
                  "non-competition covenant it requires are void and unenforceable as "
                  "to Plaintiff;"),
    ("LIST_ITEM", "9. An injunction prohibiting Hertz from requiring or enforcing that "
                  "term or covenant, and actual damages according to proof (Bus. & Prof. "
                  "Code, § 16600.5, subd. (e));"),
    ("LIST_ITEM", "On All Causes of Action:"),
    ("LIST_ITEM", "10. Costs of suit, and reasonable attorney's fees to the extent "
                  "incurred and authorized by statute;"),
    ("LIST_ITEM", "11. Prejudgment interest as permitted by law; and"),
    ("LIST_ITEM", "12. Such other relief as the Court deems just and proper."),

    # ------------------------------------------------------------------ XI
    ("HEADER", "XI.\nDEMAND FOR JURY TRIAL"),
    ("PARA", "Plaintiff demands a trial by jury on all issues so triable."),
]


def _number(content: list[tuple]) -> tuple[list[tuple], dict[str, int]]:
    labels: dict[str, int] = {}
    n = 0
    for entry in content:
        if entry[0] == "PARA" and not entry[1].startswith("Plaintiff BRENDAN"):
            n += 1
            if len(entry) > 2:
                labels[entry[2]] = n
    out, n = [], 0
    for entry in content:
        kind, text = entry[0], entry[1]
        if kind == "PARA" and not text.startswith("Plaintiff BRENDAN"):
            n += 1
            text = f"{n}. {text}"
        out.append((kind, text))
    return out, labels


def _resolve(text: str, labels: dict[str, int]) -> str:
    def sub(m: re.Match) -> str:
        key = m.group(1)
        if key not in labels:
            raise KeyError(f"unknown paragraph label: {key}")
        return str(labels[key])
    return re.sub(r"\{([a-z0-9_]+)\}", sub, text)


def _signature_block(d: PleadingPaper, exec_date: str, execute: bool) -> None:
    d.ensure_space(12)
    d.write_line(f"Dated: {exec_date}")
    d.blank_line()
    d.write_line("Respectfully submitted,", right=True, right_margin_offset=20)
    d.blank_line()
    d.blank_line()
    if execute:
        d.draw_signature_image(SIGNATURE_PATH, SIGNATURE_NATIVE_PX[0], SIGNATURE_NATIVE_PX[1], SIG_LINE)
    d.write_line(SIG_LINE, right=True, right_margin_offset=20)
    d.write_line(SIGNOFF_NAME, right=True, right_margin_offset=20)
    d.write_line(SIGNOFF_ROLE, right=True, right_margin_offset=20)


def _verification(d: PleadingPaper, exec_date: str, city: str, execute: bool) -> None:
    d.start_new_page()
    d.write_line("VERIFICATION", bold=True, center=True)
    d.blank_line()
    d.write_wrapped("I, BRENDAN NGWA NFORBI, declare:", first_indent=36)
    d.blank_line()
    d.write_wrapped(
        "I am the Plaintiff in this action. I have read the foregoing VERIFIED "
        "COMPLAINT and know its contents. The matters stated in it are true of my own "
        "knowledge, except those stated on information and belief, and as to those "
        "matters I believe them to be true.", first_indent=36)
    d.blank_line()
    d.write_wrapped(
        "I declare under penalty of perjury under the laws of the State of California "
        "that the foregoing is true and correct.", first_indent=36)
    d.blank_line()
    d.write_wrapped(f"Executed on {exec_date}, at {city}, California.", first_indent=36)
    d.ensure_space(8)
    d.blank_line()
    d.blank_line()
    if execute:
        d.draw_signature_image(SIGNATURE_PATH, SIGNATURE_NATIVE_PX[0], SIGNATURE_NATIVE_PX[1], SIG_LINE)
    d.write_line(SIG_LINE, right=True, right_margin_offset=20)
    d.write_line(SIGNOFF_NAME, right=True, right_margin_offset=20)


def build(out: Path, exec_date: str, city: str, execute: bool, style: str = "classic") -> Path:
    if execute and not Path(SIGNATURE_PATH).is_file():
        raise SystemExit(f"Missing universal signature: {SIGNATURE_PATH}")
    if execute:
        unresolved = [e[1][:70] for e in CONTENT if e[0] != "NOTICE" and "[[CONFORM" in e[1]]
        if unresolved:
            raise SystemExit("Refusing --execute: resolve CONFORM paragraphs first:\n  "
                             + "\n  ".join(unresolved))
    numbered, labels = _number(CONTENT)
    out.parent.mkdir(parents=True, exist_ok=True)
    if style == "minimal":
        d = PleadingPaper(str(out), doc_title_footer=FOOTER, style="minimal")
    else:
        d = PleadingPaper(str(out), doc_title_footer=FOOTER)
    c = d.c
    y0 = d._line_y(0)
    for i, (txt, font_name, size) in enumerate(PLAINTIFF_BLOCK):
        c.setFont(font_name, size)
        c.drawString(CONTENT_LEFT, y0 - i * 15, txt)
    d.current_line = 4
    d.blank_line()
    d.write_line(COURT_LINE1, bold=True, center=True)
    d.write_line(COURT_LINE2, bold=True, center=True)
    d.blank_line()
    d.draw_caption_block(CAPTION_LEFT, CAPTION_RIGHT, caption_size=8.2, tight_lh=10.5, boxed=True)
    d.blank_line()

    for kind, text in numbered:
        text = _resolve(text, labels)
        if kind == "NOTICE":
            if execute:
                continue
            d.ensure_space(8)
            d.write_wrapped(text, bold=True)
            d.blank_line()
        elif kind == "HEADER":
            lines = text.split("\n")
            d.ensure_space(len(lines) + 9)
            for line in lines:
                d.write_line(line, bold=True, center=True)
            d.blank_line()
        elif kind == "SUBHEAD":
            lines = text.split("\n")
            d.ensure_space(len(lines) + 3)
            for line in lines:
                d.write_line(line, bold=True, center="(" in line or "--" in line or len(lines) > 1)
            d.blank_line()
        elif kind == "PARA":
            d.write_wrapped(_filing_text(text, execute), first_indent=36)
            d.blank_line()
        elif kind == "LIST_ITEM":
            d.write_wrapped(_filing_text(text, execute), indent=36, first_indent=0)
            if text.startswith("12. "):
                d.blank_line()
        else:
            raise ValueError(kind)
    d.blank_line()
    _signature_block(d, exec_date, execute)
    _verification(d, exec_date, city, execute)
    d.save()
    return out


# ---------------------------------------------------------------------------
# Exhibit packet
# ---------------------------------------------------------------------------
EXHIBITS = [
    ("A", "Offer Letter, The Hertz Corporation, October 22, 2026",
     ["R2:a52a25984f8cc1ce053701c60be586617daab014164b3b3e7a8af62733f53aeb"]),
    ("B", "Hertz E-mails of October 22 and 23, 2026 (Offer, Acceptance, Pre-Boarding)",
     ["Hertz Talent Acquisition - Offer Follow-Up (Oct 22 2026) - Nov 2 file copy.pdf",
      "Hertz - Pre-Boarding Instructions (Req 43711, Oct 23 2026) - Nov 2 file copy.pdf"]),
    ("C", "HireRight Disclosure Packet Signed October 23, 2026 (12 pages)",
     ["HireRight - Other Disclosures and Authorizations (Signed Oct 23 2026).pdf"]),
    ("D", "HireRight Notice: MVR Express Report Provided to The Hertz Corporation, October 23, 2026",
     ["HireRight - MVR Express Furnishing Notice to Hertz (Oct 23 2026) - Nov 2 file copy.pdf"]),
    ("E", "HireRight Complete Background Report, Order OR-102326-NH87V, November 2, 2026",
     ["HireRight - Complete Background Report to Hertz (OR-102326-NH87V, Nov 2 2026).pdf"]),
    ("F", "The Hertz Corporation Notice of November 2, 2026, and Transmittal E-mail",
     ["HireRight - Urgent Attention Email with Pre-Adverse Attachments (Nov 2 2026).pdf",
      "HireRight - CA Pre-Adverse Letter (Nov 2 2026).pdf"]),
]


def _slip_sheet(path: Path, letter_: str, title: str) -> None:
    from reportlab.lib.pagesizes import letter
    from reportlab.pdfgen import canvas
    c = canvas.Canvas(str(path), pagesize=letter)
    w, h = letter
    c.setFont("Times-Bold", 28)
    c.drawCentredString(w / 2, h / 2 + 30, f"EXHIBIT {letter_}")
    c.setFont("Times-Roman", 13)
    c.drawCentredString(w / 2, h / 2 - 10, title)
    c.save()


def build_exhibits(out: Path, r2_cache: Path) -> Path:
    import tempfile
    from pypdf import PdfReader, PdfWriter
    w = PdfWriter()
    tmp = Path(tempfile.mkdtemp())
    for letter_, title, sources in EXHIBITS:
        slip = tmp / f"slip_{letter_}.pdf"
        _slip_sheet(slip, letter_, title)
        for p in PdfReader(str(slip)).pages:
            w.add_page(p)
        for src in sources:
            path = (r2_cache / f"{src[3:]}.pdf") if src.startswith("R2:") else (DOCS / src)
            if not path.is_file():
                raise SystemExit(f"Missing exhibit source: {path}")
            for p in PdfReader(str(path)).pages:
                w.add_page(p)
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "wb") as f:
        w.write(f)
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("out", nargs="?", default=str(DEFAULT_OUT))
    ap.add_argument("--date", default="November 12, 2026")
    ap.add_argument("--city", default="Stockton")
    ap.add_argument("--execute", action="store_true", help="Strip review notes and affix signature")
    ap.add_argument("--style", choices=["classic", "minimal"], default="classic",
                    help="Pleading-paper style (see lib/pleading_paper.py)")
    ap.add_argument("--exhibits", action="store_true", help="Also build the Exhibit A-F packet")
    ap.add_argument("--r2-cache", default=str(ROOT / ".cache/r2"),
                    help="Directory holding <sha256>.pdf for R2-only exhibits (offer letter)")
    a = ap.parse_args()
    out = Path(a.out).resolve()
    if a.style != "classic" and a.out == str(DEFAULT_OUT):
        out = out.with_name(out.stem + f" - {a.style.title()} Style.pdf")
    print("Generated:", build(out, a.date, a.city, a.execute, a.style))
    if a.exhibits:
        print("Generated:", build_exhibits(EXHIBITS_OUT, Path(a.r2_cache)))


if __name__ == "__main__":
    main()
