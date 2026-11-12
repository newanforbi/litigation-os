#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Matter 43 — verified complaint, N.D. Cal. (San Jose Division).

Ngwa Nforbi v. The Hertz Corporation and HireRight, LLC.

  (1) FCRA, 15 U.S.C. § 1681e(b), §§ 1681n, 1681o       — HireRight (federal question)
  (2) Penal Code § 290.46(j)(2)(E), (j)(4)(A)-(B)        — Hertz
  (3) ICRAA, Civ. Code §§ 1786.16(a)(2)(B), 1786.50      — Hertz
  (4) Labor Code § 432.7(a)(1), (c) (alternative)        — Hertz
  (5) Bus. & Prof. Code §§ 16600, 16600.1, 16600.5;
      28 U.S.C. §§ 2201-2202                             — Hertz

Jurisdiction: 28 U.S.C. § 1331 (Count 1), § 1367(a), and independently
§ 1332(a). No DOE defendants (diversity). HireRight is sued on the federal
count only, which keeps California's anti-SLAPP statute out of the case
against it. Incorporates the Nov. 12 opposing-counsel stress-test fixes
(internal/src/data/matters/43/STRESS_TEST_2026-11-12.md).

    python3 internal/scripts/matter43-hertz-federal-complaint.py --execute
"""
from __future__ import annotations

import argparse
import importlib.util
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
_spec = importlib.util.spec_from_file_location("m43state", SCRIPT_DIR / "matter43-hertz-complaint.py")
S = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(S)

from pleading_paper import CONTENT_LEFT, PleadingPaper  # noqa: E402

OUT = S.OUT_DIR / "Complaint - Ngwa Nforbi v The Hertz Corporation and HireRight LLC (N.D. Cal., Nov 12 2026).pdf"
FOOTER = "BRENDAN NGWA NFORBI v. THE HERTZ CORPORATION, et al. — COMPLAINT"
COURT = ["UNITED STATES DISTRICT COURT", "NORTHERN DISTRICT OF CALIFORNIA", "SAN JOSE DIVISION"]

CAPTION_LEFT = [
    ("BRENDAN NGWA NFORBI, also known", True, False),
    ("as BRENDAN NGWANFORBI,", True, False),
    ("", False, False),
    ("                          Plaintiff,", False, False),
    ("", False, False),
    ("       v.", False, False),
    ("", False, False),
    ("THE HERTZ CORPORATION, a Delaware", True, False),
    ("corporation; and HIRERIGHT, LLC, a", True, False),
    ("Delaware limited liability company,", True, False),
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
    ("(1) 15 U.S.C. § 1681e(b) (FCRA);", False, False),
    ("(2) Cal. Penal Code § 290.46(j);", False, False),
    ("(3) Cal. Civ. Code §§ 1786.16,", False, False),
    ("      1786.50 (ICRAA);", False, False),
    ("(4) Cal. Labor Code § 432.7;", False, False),
    ("(5) Cal. Bus. & Prof. Code §§ 16600,", False, False),
    ("      16600.1, 16600.5", False, False),
    ("", False, False),
    ("DEMAND FOR JURY TRIAL", True, False),
]

CONTENT: list[tuple] = [
    ("PARA", "Plaintiff BRENDAN NGWA NFORBI, also known as Brendan Ngwanforbi "
             "(\"Plaintiff\"), alleges as follows:"),

    ("HEADER", "I.\nINTRODUCTION"),
    ("PARA",
     "California permits the public to view its Megan's Law registry for one purpose: to "
     "protect a person at risk. It forbids anyone to use that information for purposes "
     "relating to employment. Cal. Penal Code § 290.46(j)(1), (j)(2)(E). This action "
     "arises because Defendant The Hertz Corporation chose to buy California registry "
     "information about Plaintiff for a California job, routed his registry results into "
     "its employment-eligibility review, and within hours issued a preliminary decision "
     "rescinding the job it had offered him and that he had accepted.", "intro1"),
    ("PARA",
     "On October 22, 2026, Hertz offered Plaintiff, in writing, a full-time Manager "
     "Trainee position at its Palo Alto branch at $23.00 per hour. Plaintiff accepted the "
     "same day. The offer stated that if his background check \"does not meet company "
     "standards, my contingent offer will be rescinded.\" Hertz then ordered from "
     "Defendant HireRight, LLC a background report that included a separately itemized "
     "\"National Sex Offender Registry\" product. HireRight returned two results reflecting "
     "Plaintiff's California registry entry, graded them \"Client Review Required\" under "
     "rules bearing Hertz's name, and printed beneath them that California registry "
     "information \"may not be used for employment purposes except to protect a person at "
     "risk. See CA Penal Code Section 290.46.\""),
    ("PARA",
     "HireRight delivered the completed report at 2:29 a.m. Pacific time on November 2, "
     "2026. At 10:19 a.m. the same morning, Hertz sent Plaintiff a notice referring to "
     "\"the Company's preliminary decision recinding the offer of employment,\" made "
     "\"[b]ased on a review of the results of your background report and Company's "
     "eligibility criteria.\" The notice listed, as information \"including\" the basis, "
     "a single line: \"[Criminal Information] Alcohols related offenses-Does not meet.\" "
     "Plaintiff has no alcohol-related criminal conviction, and the report shows none. "
     "The only alcohol-related information in the report is a Department of Motor "
     "Vehicles administrative record that Hertz had held since October 23, 2026, while it "
     "continued to onboard Plaintiff for ten days without objection. Hertz acted only "
     "after the registry results arrived."),
    ("PARA",
     "Plaintiff seeks: damages under the Fair Credit Reporting Act against HireRight for "
     "reporting non-criminal DMV information as \"Criminal Information\" and "
     "\"offenses\"; the remedies California provides against Hertz for misuse of Megan's "
     "Law information, for a defective investigative-report disclosure, and for use of a "
     "non-conviction arrest record; and declaratory and injunctive relief against Hertz's "
     "requirement that a California applicant sign a non-competition agreement."),

    ("HEADER", "II.\nPARTIES"),
    ("PARA",
     "Plaintiff is an individual who resides in Stockton, San Joaquin County, California, "
     "and is a citizen of California. Defendants' documents identify him as Brendan Ngwa "
     "Nforbi and as Brendan Ngwanforbi. Each name refers to Plaintiff."),
    ("PARA",
     "Defendant The Hertz Corporation (\"Hertz\") is, on information and belief, a "
     "Delaware corporation with its principal place of business at 8501 Williams Road, "
     "Estero, Florida 33928, and is a citizen of Delaware and Florida. Hertz operates "
     "vehicle-rental branches in California, including the Hertz Local Edition branch at "
     "816 San Antonio Road, Palo Alto, California 94303, and a location at 725 Ridder "
     "Park Drive, San Jose, California. Hertz issued the offer, procured the background "
     "report, and issued the November 2 notice."),
    ("PARA",
     "Defendant HireRight, LLC (\"HireRight\") is, on information and belief, a Delaware "
     "limited liability company headquartered in Nashville, Tennessee, whose consumer "
     "department operates from Tulsa, Oklahoma. HireRight is a \"consumer reporting "
     "agency\" within the meaning of 15 U.S.C. § 1681a(f) that assembles and furnishes "
     "consumer reports to employers for employment purposes in exchange for fees. On "
     "information and belief, each of HireRight's members is a citizen of a State other "
     "than California, and no member of HireRight is a citizen of California. The "
     "identity and citizenship of HireRight's members are peculiarly within HireRight's "
     "knowledge and are not publicly disclosed.", "hireright_party"),
    ("PARA",
     "On information and belief, Hertz processed the application at issue in part in the "
     "name of its parent, Hertz Global Holdings, Inc. On October 22, 2026, Hertz's "
     "tax-credit screening vendor wrote to Plaintiff regarding \"your recently submitted "
     "job application with Hertz Global Holdings, Inc.\" Plaintiff reserves the right to "
     "seek leave to add Hertz Global Holdings, Inc. if discovery shows it participated in "
     "the conduct alleged."),

    ("HEADER", "III.\nJURISDICTION, VENUE, AND DIVISIONAL ASSIGNMENT"),
    ("PARA",
     "This Court has subject-matter jurisdiction over the First Cause of Action under 28 "
     "U.S.C. § 1331 and 15 U.S.C. § 1681p, because it arises under the Fair Credit "
     "Reporting Act. The Court has supplemental jurisdiction over the remaining causes of "
     "action under 28 U.S.C. § 1367(a), because they arise from the same background "
     "report, the same employment decision, and the same nucleus of operative fact."),
    ("PARA",
     "Independently, this Court has diversity jurisdiction over the entire action under "
     "28 U.S.C. § 1332(a)(1). Plaintiff is a citizen of California. Hertz is a citizen of "
     "Delaware and Florida. On information and belief, no member of HireRight is a "
     "citizen of California. The amount in controversy exceeds $75,000, exclusive of "
     "interest and costs, taking into account Plaintiff's actual damages, including the "
     "wages and benefits of a full-time management-track position and emotional "
     "distress; the statutory amounts, civil penalty of up to $25,000, and exemplary "
     "damages available under Cal. Penal Code § 290.46(j)(4)(A); the $10,000 statutory "
     "alternative and punitive damages available under Cal. Civ. Code § 1786.50; and the "
     "statutory and punitive damages available under 15 U.S.C. § 1681n."),
    ("PARA",
     "Plaintiff has standing under Article III as to each cause of action. Each rests on "
     "concrete harm: the use of information about Plaintiff to deny or withhold an "
     "accepted job; the communication to a prospective employer of materially misleading "
     "information labeling Plaintiff's driving record as criminal offenses, which bears a "
     "close relationship to the harm redressed by defamation; the procurement of a "
     "registry search under an authorization that did not disclose it, which deprived Plaintiff "
     "of the opportunity to contest or address that search before Hertz used it to announce "
     "a preliminary rescission of his accepted job; and the condition, "
     "imposed on Plaintiff's employment, that he surrender his right to work for "
     "competitors."),
    ("PARA",
     "This Court has personal jurisdiction over each Defendant. Hertz interviewed "
     "Plaintiff in San Jose, offered him a position in Palo Alto, and procured and used a "
     "consumer report about a California resident for a California job. HireRight "
     "prepared that report for a California job, applied California-specific "
     "disclosures, researched California court and registry records, and transmitted the "
     "report and Hertz's notice to Plaintiff in California."),
    ("PARA",
     "Venue is proper in this District under 28 U.S.C. § 1391(b)(2), because a "
     "substantial part of the events giving rise to the claims occurred here. The "
     "position was located in Palo Alto, and the interview occurred in San Jose, both in "
     "Santa Clara County."),
    ("PARA",
     "Under Civil Local Rule 3-2(c) and (e), assignment to the San Jose Division is "
     "proper, because a substantial part of the events giving rise to the claims occurred "
     "in Santa Clara County."),

    ("HEADER", "IV.\nFACTUAL ALLEGATIONS"),
    ("SUBHEAD", "A. Hertz Offers Plaintiff the Palo Alto Manager Trainee Position"),
    ("PARA",
     "On or about October 21 and 22, 2026, Hertz manager Kathleen Williams arranged for "
     "Plaintiff to interview at Hertz's Ridder Park location in San Jose. On October 22, "
     "2026, at approximately 3:38 p.m., Hertz Talent Acquisition Partner Gloria Williams "
     "e-mailed Plaintiff: \"The team would like to extend an offer to you. "
     "Congratulations!\" At approximately 3:40 p.m., Kathleen Williams messaged Plaintiff "
     "that he should receive an offer for Manager Trainee at the Palo Alto location. At "
     "4:49 p.m., Plaintiff replied that he \"happily accept[ed] the offer.\""),
    ("PARA",
     "Hertz's written offer letter, dated October 22, 2026, states: \"We are pleased to "
     "confirm our offer of employment with The Hertz Corporation for the position of "
     "Manager Trainee (Full time) based at 816 San Antonio Rd, Palo Alto, CA 94303 ... "
     "This position reports to Kathleen Williams. Your base salary, paid on an hourly "
     "basis, will be $23.00.\" The letter describes the role as \"the entry position to "
     "our management career path.\" A true copy is attached as Exhibit A.", "offer"),
    ("PARA",
     "The offer letter defines the checks on which the offer is contingent: \"Please "
     "understand this offer is contingent upon the successful completion of a "
     "pre-employment MVR check (as applicable), criminal, employment and education "
     "background checks ('Background Checks').\" The definition does not include a "
     "sex-offender registry search.", "contingency"),
    ("PARA",
     "The offer letter states the standard that decides whether the offer survives: \"I "
     "acknowledge that if my background check does not meet company standards, my "
     "contingent offer will be rescinded, and my employment will be null and void.\"",
     "standards"),
    ("PARA",
     "The offer letter also states: \"It is a fundamental term and condition of your "
     "employment that you must execute and deliver to the undersigned the below details "
     "regarding Employee Confidentiality & Non-Competition.\"", "nc_offer"),
    ("PARA",
     "Plaintiff accepted the offer through Hertz's online portal. At 5:42 p.m. on October "
     "22, 2026, the portal showed the Manager Trainee position, requisition 43711, with "
     "the status \"Offer Accepted.\" On October 23, 2026, Gloria Williams sent Plaintiff a "
     "\"Pre-Boarding\" e-mail for \"43711 Manager Trainee\" stating, \"We are excited you "
     "are joining the winning team!\" and directing him to complete a background request "
     "from HireRight. True copies of these e-mails are attached as Exhibit B.", "accepted"),

    ("SUBHEAD", "B. The California Investigative-Report Disclosure Packet"),
    ("PARA",
     "On October 23, 2026, at approximately 3:03 to 3:04 p.m. Pacific time, Plaintiff "
     "completed HireRight's electronic consent process for Hertz. HireRight's record of "
     "that process includes a single twelve-page document titled, on its first page, "
     "\"Disclosure Regarding Investigative Consumer Report\" (the \"Disclosure Packet\"). "
     "A true copy is attached as Exhibit C.", "packet"),
    ("PARA",
     "The first page of the Disclosure Packet identifies the employer as \"The Herz "
     "Corporation.\" Pages one and two, before the packet's only signature block on page "
     "three, combine the investigative-report disclosure with notices directed to "
     "residents of Massachusetts, Minnesota, New Jersey, New York, and Washington; a City "
     "of Los Angeles \"Fair Chance Initiative for Hiring Ordinance\" notice reproduced in "
     "full in English and again in Spanish; and a checkbox for \"California, Minnesota and "
     "Oklahoma residents.\" The signed pages do not identify the types of information to "
     "be obtained and do not mention a sex-offender registry search.", "signed_pages"),
    ("PARA",
     "The document headed \"(CALIFORNIA APPLICANTS/EMPLOYEES ONLY) CALIFORNIA "
     "DISCLOSURE\" appears on page eight, after the signature block. It bears no "
     "signature. It is bound in the same document as a four-page federal summary of "
     "rights, two pages of New York Correction Law article 23-A, and two pages of San "
     "Francisco workplace posters. It is the only page in the packet that lists the "
     "\"specific types of information about you that may be obtained,\" including "
     "\"National Sex Offender Registry\" and \"MVR Express.\" It does not list employment "
     "or education verification.", "cadisclosure"),
    ("PARA",
     "At 3:04 p.m. on October 23, 2026, Hertz's \"Pre Employment (Field)\" account "
     "submitted HireRight order OR-102326-NH87V, package \"Field (Driver Required),\" for "
     "requisition 43711. The order included the separately itemized \"National Sex "
     "Offender Registry\" product. The report was requested by Kesha Nedio-Casey, Hertz "
     "Pre Employment (Field), Estero, Florida.", "order"),

    ("SUBHEAD", "C. Hertz Receives the Driving Record on October 23 and Continues to Onboard Plaintiff"),
    ("PARA",
     "HireRight completed the motor-vehicle-record (\"MVR\") component at 3:04 p.m. on "
     "October 23, 2026, and at 3:05 p.m. notified Plaintiff that it had provided his MVR "
     "to \"Gloria Williams, The Hertz Corporation.\" HireRight's activity log records: "
     "\"Oct 23, 2026 3:07 PM -- MVR Express report provided to The Hertz Corporation.\" A "
     "true copy of the notice is attached as Exhibit D.", "mvr_time"),
    ("PARA",
     "The MVR shows Plaintiff's California Class C driver's license, issued July 21, 2026 "
     "and expiring May 12, 2027, with the status \"VALID.\" It also shows two "
     "administrative actions by the Department of Motor Vehicles, both concluded before "
     "Hertz made its offer: a suspension for \"refusal or failure to complete chemical "
     "test,\" with a privilege reinstatement date of May 19, 2026; and a commercial-vehicle "
     "disqualification for refusing to submit to a test, with a clear date of November "
     "30, 2025. The only conviction in the MVR is an October 2, 2024 infraction for an "
     "unregistered vehicle under California Vehicle Code § 4000(a), which carries zero "
     "points and is not alcohol-related. The MVR section of the report does not label "
     "any entry as criminal.", "mvr"),
    ("PARA",
     "Neither DMV action is a criminal conviction or a criminal offense. Under California "
     "law, the chemical-test obligation arises only for a person who has been lawfully "
     "arrested, and a refusal action follows the arresting officer's report. Cal. Veh. "
     "Code §§ 23612(a)(1)(A), 13353. The refusal action reflected in the MVR followed an "
     "arrest of Plaintiff, and that arrest did not result in a conviction. The background "
     "report reflects no alcohol-related conviction in any jurisdiction searched, "
     "including San Joaquin County, Santa Clara County, Sheridan County, Wyoming, the "
     "Eastern District of California, and the District of Wyoming.", "arrest"),
    ("PARA",
     "Hertz did not issue any adverse notice after receiving the MVR on October 23, 2026. "
     "For the next ten days Hertz left Plaintiff's status at \"Offer Accepted\" and "
     "continued its onboarding process."),

    ("SUBHEAD", "D. The Registry Results and Hertz's Eligibility Review"),
    ("PARA",
     "The California Department of Justice maintains an internet website, created by and "
     "operated under Cal. Penal Code § 290.46, that makes information from California's "
     "sex-offender registry available to the public (the \"Megan's Law Website\"). "
     "Plaintiff is a person whose information is displayed on the Megan's Law Website.",
     "listed"),
    ("PARA",
     "The United States Department of Justice operates two different sex-offender "
     "systems. The National Sex Offender Registry (\"NSOR\"), 34 U.S.C. § 20921, is a file "
     "maintained by the Federal Bureau of Investigation and accessible only to "
     "law-enforcement and other authorized criminal-justice agencies. The Dru Sjodin "
     "National Sex Offender Public Website (\"NSOPW\"), 34 U.S.C. § 20922, is open to the "
     "public. The Department of Justice describes NSOPW as a search portal that does not "
     "maintain its own registry data. NSOPW uses web services to search each "
     "jurisdiction's public registry website in real time, and an offender who is not "
     "displayed on a jurisdiction's public website does not appear on NSOPW.", "nsopw"),
    ("PARA",
     "For a California registrant, therefore, an NSOPW result is the Megan's Law "
     "Website's own record, retrieved from that website at the moment of the search. "
     "California, acting under Cal. Penal Code § 290.46, is the entity that discloses the "
     "information. NSOPW is only the conduit through which it is displayed.", "conduit"),
    ("PARA",
     "HireRight is a private consumer reporting agency. On information and belief, it is "
     "not a law-enforcement or criminal-justice agency and has no access to NSOR. A "
     "private consumer reporting agency's sex-offender search \"performed through the "
     "United States Department of Justice\" is therefore, on information and belief, an "
     "NSOPW search that returns the Megan's Law Website's records."),
    ("PARA",
     "Hertz's order included three \"National Sex Offender Registry\" subrequests, one for "
     "each of three forms of Plaintiff's name. Each subrequest bears the comment: "
     "\"National Sex Offender Registry search performed through the United States "
     "Department of Justice.\""),
    ("PARA",
     "The subrequest run on \"Brendan Ngwa\" returned \"Not in Registry.\" Like every "
     "search in the report that found no record, it was graded \"Meets Company "
     "Standards.\"", "meets"),
    ("PARA",
     "The two subrequests run on the other forms of Plaintiff's name returned \"In "
     "Registry\" on October 30, 2026, at 11:25 a.m. and 12:48 p.m. Pacific time. Each was "
     "graded \"Client Review Required.\" The returned entries listed aliases for "
     "Plaintiff, including \"NGWA-NFORBI, BRENDAN.\"", "crr"),
    ("PARA",
     "HireRight's researchers entered the following notes on those entries on October 30, "
     "2026: \"APPLICANT IS LISTED ON THE SEX OFFENDER REGISTRY IN THE STATE OF CA\"; "
     "\"Verified by Name and DOB\"; and \"Information from the California Sex Offenders' "
     "Registry may not be used for employment purposes except to protect a person at "
     "risk. See CA Penal Code Section 290.46. Only use this information to make an "
     "employment decision as expressly allowed by CA law.\"", "warning"),
    ("PARA",
     "The report states that the grades were assigned under adjudication rules named "
     "\"The Hertz Corporation (Shell) (GL-HTZ001-001) v1.7\" and \"AutoLibrarySet - Excl. "
     "MVR, EDU, EMP - Managed Adjudication 3.0.\" The grade \"Client Review Required\" "
     "means that Hertz's rules required Hertz personnel to review the result in deciding "
     "whether Plaintiff's background check met Hertz's company standards, the same "
     "standards the offer letter makes the condition of his employment (paragraph "
     "{standards})."),
    ("PARA",
     "The National Sex Offender Registry search was not part of the \"Background Checks\" "
     "Hertz's offer letter described (paragraph {contingency}). It was a separately "
     "itemized product that Hertz selected for a California \"Field (Driver Required)\" "
     "package (paragraph {order}). On information and belief, Hertz configured that "
     "package, and adopted the adjudication rules applied to it, so that a California "
     "registry hit would be routed to Hertz's eligibility review rather than "
     "disregarded.", "design"),

    ("SUBHEAD", "E. The Report Is Completed and Hertz Acts Within Hours"),
    ("PARA",
     "The report also contained a Santa Clara County Superior Court record (case "
     "C1761642) reflecting felony convictions, with a disposition date of January 12, "
     "2018, for offenses arising on February 26, 2017, which require registration under "
     "Cal. Penal Code § 290. The report states a parole/release date of December 2, 2020. "
     "That record was graded \"Client Review Required.\" The November 2 notice did not "
     "identify it."),
    ("PARA",
     "HireRight's activity log records that HireRight adjudicated the completed report at "
     "2:29 a.m. Pacific time on November 2, 2026, with the overall result \"Client Review "
     "Required.\" The log explains that HireRight's adjudication entries \"indicate "
     "whether an initial determination was made regarding whether the report satisfied "
     "the company's hiring criteria ... including any preliminary status Result of "
     "'Meets' or 'Does Not Meet' company standards.\" A true copy of the complete report "
     "is attached as Exhibit E.", "adjudicated"),
    ("PARA",
     "At 10:19 a.m. Pacific time on November 2, 2026, less than eight hours later, "
     "HireRight transmitted to Plaintiff, through HireRight's applicant portal as a "
     "HireRight \"special processing\" file, a letter from The Hertz Corporation dated "
     "November 2, 2026 (the \"Notice\"). A true copy of the Notice and its transmittal "
     "e-mail is attached as Exhibit F.", "notice"),
    ("PARA",
     "The Notice states: \"Based on a review of the results of your background report and "
     "Company's eligibility criteria, we are notifying you that there is information in "
     "your background report that may result in Company deciding not to offer you ... "
     "employment ... including the following specific information identified in your "
     "background report: [Criminal Information] Alcohols related offenses-Does not "
     "meet.\"", "notice_text"),
    ("PARA",
     "The Notice refers to \"the Company's preliminary decision recinding the offer of "
     "employment,\" and invites \"evidence in mitigation of the specific criminal "
     "information identified above.\""),
    ("PARA",
     "The Notice does not state a deadline to respond. Where a date should appear, it "
     "reproduces an unfilled bracket: \"[Date (at least five business days from the date "
     "of receipt of the notice. ... (iii) If notice is transmitted through email, the "
     "notice shall be deemed received two business days after it is sent.)].\" Elsewhere "
     "it states that Hertz will not make a final decision \"for at least five (5) business "
     "days from the date of this letter.\""),
    ("PARA",
     "The Notice does not mention the sex-offender registry, identify any person at risk, "
     "identify any statute authorizing Hertz to use registry information, or identify any "
     "criminal conviction."),
    ("PARA",
     "The designation \"[Criminal Information] Alcohols related offenses-Does not meet\" "
     "uses the vocabulary of HireRight's adjudication service (\"Does Not Meet\") and a "
     "HireRight letter template, including bracketed template instructions. It applies "
     "the heading \"Criminal Information\" and the word \"offenses\" to information that "
     "HireRight's own MVR section does not label as criminal. On information and belief, "
     "the designation was generated by HireRight's adjudication service applying the "
     "Hertz adjudication rules, and HireRight communicated it to Hertz as part of the "
     "consumer report and its adjudication of that report.", "label"),

    ("SUBHEAD", "F. Hertz Used the Registry Information for Employment Purposes"),
    ("PARA",
     "On information and belief, Hertz used the California registry information in "
     "Plaintiff's report for purposes relating to employment, in at least the following "
     "ways: (a) it selected the registry product for a California job, outside the checks "
     "its offer letter described; (b) it adopted and applied rules under which "
     "Plaintiff's registry hits were routed to Hertz's eligibility review under the "
     "company standards on which his employment depended; (c) its personnel reviewed "
     "those results for the purpose of deciding his employment; and (d) after that review, "
     "and \"[b]ased on a review of the results of [his] background report and Company's "
     "eligibility criteria,\" it made and announced a preliminary decision rescinding his "
     "offer. Hertz thus used the registry information as a basis for an employment "
     "decision.", "use"),
    ("PARA",
     "Count 2 concerns Hertz's use of information disclosed pursuant to Cal. Penal Code "
     "§ 290.46, not the existence of a court file. The Santa Clara County court record "
     "described in Part IV.E does not supply an independent basis for the preliminary "
     "decision. The Notice did not cite it. Hertz's rules routed the registry results to "
     "review as a separate product with its own grades. Hertz acted within hours of "
     "receiving the registry results, not after any separate investigation of court "
     "records. On information and belief, no Hertz decision-maker made the preliminary "
     "decision without having seen the registry results, which were flagged for that same "
     "review.", "independent"),
    ("PARA",
     "The facts supporting that belief include: the registry search lay outside the "
     "offer's defined checks and was separately selected (paragraph {design}); the "
     "routing of Plaintiff's registry hits to \"Client Review\" under rules bearing "
     "Hertz's name (paragraph {crr}); the ten days in which Hertz held the only "
     "alcohol-related information without acting (paragraph {mvr_time}); the issuance of "
     "the Notice within eight hours after the registry results were delivered in the "
     "completed report; the Notice's statement that the basis \"includ[es]\" the listed "
     "line, which on its face is not exclusive; and the absence of any alcohol-related "
     "criminal conviction to which the Notice's \"[Criminal Information]\" heading could "
     "refer."),
    ("PARA",
     "The decision-making records that would show precisely how Hertz applied its rules "
     "to the registry results, including the rule set \"The Hertz Corporation (Shell) "
     "(GL-HTZ001-001) v1.7,\" the identity of the personnel who performed the \"Client "
     "Review,\" the screens they viewed, and their notes, are exclusively in Defendants' "
     "possession."),
    ("PARA",
     "Hertz knew when it reviewed the report that California prohibits use of registry "
     "information for employment. The prohibition was printed beneath the registry "
     "entries (paragraph {warning})."),
    ("PARA",
     "Hertz did not use the registry information to protect any person at risk. The "
     "exception in Cal. Penal Code § 290.46(j)(1) permits use only to protect a person at "
     "risk. Hertz's screening applies to applicants as a category, before any assignment "
     "to particular customers or co-workers, and the Notice identifies no person whom "
     "Hertz sought to protect. On information and belief, no statute authorized Hertz, a "
     "vehicle-rental company, to obtain or use California registry information for "
     "employment, and Hertz did not obtain it through Cal. Penal Code § 11105 or "
     "§ 11105.3."),
    ("PARA",
     "Plaintiff's signature on the Disclosure Packet did not authorize Hertz to use "
     "registry information for employment. Section 290.46(j) regulates use and serves a "
     "public purpose, and a law established for a public reason cannot be contravened by "
     "private agreement. Cal. Civ. Code § 3513."),

    ("SUBHEAD", "G. Plaintiff's Status and Harm"),
    ("PARA",
     "The Notice states no deadline to respond, identifies no conviction, and does not "
     "identify which of the items reviewed formed the basis of Hertz's preliminary "
     "decision. The five business days Hertz itself specified ended on November 9, 2026. "
     "Hertz has not communicated with Plaintiff since it sent the Notice.", "status"),
    ("PARA",
     "As of the filing of this Complaint, Hertz has not withdrawn its preliminary "
     "decision, has not scheduled a start date, and has not permitted Plaintiff to begin "
     "work. Plaintiff remains ready, willing, and able to begin work as a Manager "
     "Trainee. Hertz's preliminary decision and its continued refusal to allow Plaintiff "
     "to start have excluded him from the job he accepted.", "status2"),
    ("PARA",
     "The preliminary decision and its effects are centered in California. It concerned a "
     "California resident, recruited and interviewed in California, for a position at a "
     "California branch, supervised by a California branch manager, Kathleen Williams. "
     "Hertz's onboarding of Plaintiff was managed by its Western Region Talent Acquisition "
     "Partner, Gloria Williams, whose listed telephone number bears a California area code. "
     "The decision withholds employment that was to be performed only in California. The "
     "report was ordered through a Hertz pre-employment account associated with Estero, "
     "Florida. On information and belief, Hertz's California branch and regional personnel "
     "participated in, were consulted on, or carried out the preliminary decision. The "
     "identity and location of each person who made it are peculiarly within Hertz's "
     "knowledge.", "location"),
    ("PARA",
     "As a direct result of Defendants' conduct, Plaintiff has suffered and continues to "
     "suffer harm, including: anxiety, humiliation, and emotional distress at being "
     "screened out of an accepted job on the basis of information the law forbids Hertz "
     "to use for that purpose, and at being described to a prospective employer as having "
     "committed criminal offenses he did not commit; loss of the opportunity to begin the "
     "management career path the offer described; and loss of the wages and benefits of "
     "a full-time position at $23.00 per hour, in amounts according to proof."),

    # ------------------------------------------------------------------ COUNT 1
    ("HEADER", "V.\nFIRST CAUSE OF ACTION"),
    ("SUBHEAD", "Failure to Follow Reasonable Procedures to Assure Maximum Possible Accuracy\n"
                "(Fair Credit Reporting Act, 15 U.S.C. §§ 1681e(b), 1681n, 1681o)\n"
                "(Against HireRight)"),
    ("PARA",
     "Plaintiff incorporates paragraphs {offer}, {accepted}, {order} through {arrest}, "
     "{adjudicated} through {notice_text}, {label}, and {status} through the end of Part "
     "IV.G."),
    ("PARA",
     "Plaintiff is a \"consumer\" under 15 U.S.C. § 1681a(c). The report and adjudication "
     "HireRight prepared about him and furnished to Hertz are a \"consumer report\" under "
     "15 U.S.C. § 1681a(d), furnished for employment purposes."),
    ("PARA",
     "Section 1681e(b) requires a consumer reporting agency, whenever it prepares a "
     "consumer report, to follow reasonable procedures to assure maximum possible "
     "accuracy of the information concerning the individual about whom the report "
     "relates."),
    ("PARA",
     "HireRight reported to Hertz that Plaintiff's background presented \"[Criminal "
     "Information]\" consisting of \"Alcohols related offenses\" that \"Does not meet\" "
     "Hertz's standards (paragraph {label}). That information is inaccurate. It is "
     "patently incorrect, because Plaintiff has no alcohol-related criminal record and "
     "has committed no alcohol-related offense, and it is materially misleading, because "
     "it recasts concluded DMV licensing actions as criminal offenses in a way that can "
     "be expected to, and did, adversely affect an employment decision."),
    ("PARA",
     "HireRight failed to follow reasonable procedures to assure maximum possible "
     "accuracy. Its own MVR section reported the same entries as licensing actions, not "
     "criminal matters, and its criminal searches found no alcohol-related record in any "
     "jurisdiction. A reasonable procedure would not classify DMV administrative entries "
     "under a \"Criminal Information\" heading as \"offenses.\" On information and belief, "
     "HireRight's adjudication service is configured to do so as a matter of routine."),
    ("PARA",
     "HireRight's violation was willful, or at minimum reckless, within the meaning of 15 "
     "U.S.C. § 1681n. HireRight is among the largest employment-screening agencies in the "
     "United States and knows the difference between a licensing action and a criminal "
     "offense, as its own report reflects. In the alternative, the violation was "
     "negligent under 15 U.S.C. § 1681o."),
    ("PARA",
     "HireRight's inaccurate report was communicated to Hertz, a third party, and was "
     "followed within hours by Hertz's preliminary decision rescinding Plaintiff's offer, "
     "which identified the inaccurate designation as its basis. Plaintiff suffered the "
     "harm alleged in Part IV.G."),
    ("PARA",
     "Plaintiff is entitled to actual damages, or statutory damages of not less than $100 "
     "and not more than $1,000, together with punitive damages, costs, and reasonable "
     "attorney's fees for a willful violation, 15 U.S.C. § 1681n(a); or actual damages, "
     "costs, and reasonable attorney's fees for a negligent violation, 15 U.S.C. "
     "§ 1681o(a)."),

    # ------------------------------------------------------------------ COUNT 2
    ("HEADER", "VI.\nSECOND CAUSE OF ACTION"),
    ("SUBHEAD", "Unlawful Use of Megan's Law Information for Employment\n"
                "(Cal. Penal Code § 290.46(j)(2)(E), (j)(4)(A)-(B))\n"
                "(Against Hertz)"),
    ("PARA",
     "Plaintiff incorporates paragraphs {intro1} through {standards} and {packet} through "
     "the end of Part IV.G, except paragraph {label}."),
    ("PARA",
     "Section 290.46(j)(1) authorizes a person to use information disclosed pursuant to "
     "section 290.46 only to protect a person at risk. Section 290.46(j)(2)(E) provides "
     "that, except as authorized under subdivision (j)(1) or any other provision of law, "
     "use of information disclosed pursuant to section 290.46 is prohibited for purposes "
     "relating to employment."),
    ("PARA",
     "The California registry information in Plaintiff's report was information disclosed "
     "pursuant to section 290.46. California disclosed it to the public through the "
     "Megan's Law Website, and on information and belief it reached Hertz through an "
     "NSOPW search that retrieved it from that website in real time (paragraphs {listed} "
     "through {warning})."),
    ("PARA",
     "Hertz used that information for purposes relating to employment, as alleged in "
     "paragraphs {design} through {independent}: it used the information as a basis for an "
     "employment decision. Hertz's preliminary decision rescinding Plaintiff's "
     "offer is itself a use for purposes relating to employment. The statute prohibits "
     "use, not only final decisions."),
    ("PARA",
     "Hertz's use was not to protect a person at risk and was not authorized by any other "
     "provision of law."),
    ("PARA",
     "Under section 290.46(j)(4)(A), Hertz is liable for actual damages; an amount "
     "determined by the trier of fact not exceeding three times actual damages and not "
     "less than $250; attorney's fees; and exemplary damages or a civil penalty not "
     "exceeding $25,000. Plaintiff seeks each remedy, pleading exemplary damages and the "
     "civil penalty in the alternative."),
    ("PARA",
     "Hertz acted with knowledge of the prohibition, which was printed on the report it "
     "reviewed, and with conscious disregard of Plaintiff's rights. The registry routing "
     "was embedded in company-wide adjudication rules bearing Hertz's name, which on "
     "information and belief were adopted, authorized, or ratified by Hertz officers, "
     "directors, or managing agents. Plaintiff is entitled to exemplary damages under "
     "section 290.46(j)(4)(A) and Cal. Civ. Code § 3294."),
    ("PARA",
     "On information and belief, Hertz applies the same registry product and rules to "
     "California applicants screened under its \"Field (Driver Required)\" package "
     "generally. That is a pattern or practice of misuse. As a person aggrieved by the "
     "misuse, Plaintiff seeks preventive relief under section 290.46(j)(4)(B), including "
     "an injunction prohibiting Hertz from procuring, routing, or reviewing California "
     "Megan's Law information for employment purposes."),

    # ------------------------------------------------------------------ COUNT 3
    ("HEADER", "VII.\nTHIRD CAUSE OF ACTION"),
    ("SUBHEAD", "Investigative Consumer Reporting Agencies Act -- Non-Standalone Disclosure\n"
                "(Cal. Civ. Code §§ 1786.16(a)(2)(B), 1786.50)\n"
                "(Against Hertz)"),
    ("PARA",
     "Plaintiff incorporates paragraphs {offer}, {contingency}, {packet} through {order}, "
     "{crr}, and {notice} through {notice_text}."),
    ("PARA",
     "The report Hertz procured is an \"investigative consumer report\" under Cal. Civ. "
     "Code § 1786.2. Hertz's own disclosure acknowledges that in California the term "
     "\"includes background reports with or without information obtained from personal "
     "interviews.\""),
    ("PARA",
     "Section 1786.16(a)(2)(B) requires a person procuring an investigative consumer "
     "report for employment purposes to provide, before the report is procured, a clear "
     "and conspicuous disclosure in writing \"in a document that consists solely of the "
     "disclosure,\" including the nature and scope of the investigation requested."),
    ("PARA",
     "Hertz did not do so. The only document Plaintiff signed combined the "
     "investigative-report disclosure with notices for five other States and a Los "
     "Angeles ordinance in two languages, and misidentified the employer. The "
     "California-specific disclosure, the only page describing the nature and scope of "
     "the investigation, was not a separate signed document. It was bound, unsigned, into "
     "the same twelve-page document with federal, New York, and San Francisco materials "
     "(paragraphs {packet} through {cadisclosure})."),
    ("PARA",
     "The violation caused Plaintiff concrete harm. The document he signed did not "
     "disclose that Hertz would procure a sex-offender registry search, a search outside "
     "the checks the offer letter described. Hertz procured that search under the "
     "resulting authorization and used its results against him in the Notice. The defect "
     "deprived Plaintiff of notice of that search, and with it the opportunity to address "
     "or contest it before Hertz acted on it and announced a preliminary rescission of his "
     "accepted job."),
    ("PARA",
     "Under section 1786.50(a), Hertz is liable for actual damages or $10,000, whichever "
     "is greater, plus costs and reasonable attorney's fees. Hertz's violation was "
     "willful or grossly negligent. Hertz is a large, sophisticated national employer "
     "that procures investigative consumer reports on California applicants as a matter "
     "of routine, and the standalone requirement has been settled and publicized since "
     "at least 2019. Plaintiff is entitled to punitive damages under section "
     "1786.50(b)."),

    # ------------------------------------------------------------------ COUNT 4
    ("HEADER", "VIII.\nFOURTH CAUSE OF ACTION"),
    ("SUBHEAD", "Use of a Non-Conviction Arrest Record in Hiring\n"
                "(Cal. Labor Code § 432.7(a)(1), (c))\n"
                "(Against Hertz, in the Alternative)"),
    ("PARA",
     "Plaintiff incorporates paragraphs {offer}, {standards}, {mvr_time} through "
     "{arrest}, {notice} through the end of Part IV.E except paragraph {label}, and "
     "{status} through {location}."),
    ("PARA",
     "This cause of action is pleaded in the alternative to the Second Cause of Action, "
     "under Federal Rule of Civil Procedure 8(d)(2)-(3), to the extent Hertz contends that "
     "its preliminary decision rested on the \"Alcohols related offenses\" identified in "
     "the Notice."),
    ("PARA",
     "Labor Code § 432.7(a)(1) prohibits an employer from utilizing, as a factor in "
     "determining any condition of employment, including hiring, any record of arrest or "
     "detention that did not result in conviction."),
    ("PARA",
     "The only alcohol-related information in Plaintiff's report is the DMV chemical-test "
     "refusal entry. That entry exists only because Plaintiff was arrested, and it "
     "records the consequence of an arrest that did not result in a conviction (paragraph "
     "{arrest}). It is a record of that arrest. Hertz labeled the entry \"[Criminal "
     "Information]\" and, by its own account, used it as a factor in its preliminary "
     "decision to rescind Plaintiff's offer. Even if Hertz was permitted to obtain a driving record, section "
     "432.7(a)(1) separately prohibits an employer from utilizing a record of arrest that did "
     "not result in conviction as a factor in hiring. Permission to seek a record is not "
     "permission to use it to reject an applicant."),
    ("PARA",
     "No job requirement justified that use. Plaintiff's Class C license was valid. The "
     "refusal suspension had ended with reinstatement before the offer, and the "
     "commercial-vehicle disqualification had cleared before the offer and concerned a "
     "license class the Manager Trainee position did not require."),
    ("PARA",
     "Plaintiff is an applicant for employment within the meaning of Labor Code § 432.7(c). "
     "He accepted Hertz's offer but was never permitted to begin work. Under section "
     "432.7(c), he is entitled to actual damages or $200, whichever is greater, plus costs "
     "and reasonable attorney's fees. Because Hertz's violation was intentional, he is "
     "entitled to treble actual damages or $500, whichever is greater, plus costs and "
     "reasonable attorney's fees."),

    # ------------------------------------------------------------------ COUNT 5
    ("HEADER", "IX.\nFIFTH CAUSE OF ACTION"),
    ("SUBHEAD", "Unlawful Non-Compete Condition; Declaratory and Injunctive Relief\n"
                "(Cal. Bus. & Prof. Code §§ 16600, 16600.1, 16600.5; 28 U.S.C. §§ 2201-2202)\n"
                "(Against Hertz)"),
    ("PARA",
     "Plaintiff incorporates paragraphs {offer}, {nc_offer}, {accepted}, and {status} "
     "through {status2}."),
    ("PARA",
     "Business and Professions Code § 16600 provides that every contract by which anyone "
     "is restrained from engaging in a lawful profession, trade, or business of any kind "
     "is to that extent void, and is to be read broadly to void noncompete agreements in "
     "the employment context. The section \"shall not be limited to contracts where the "
     "person being restrained ... is a party to the contract.\" Cal. Bus. & Prof. Code "
     "§ 16600(c). Section 16600.1 makes it unlawful to include a noncompete "
     "clause in an employment contract, or to require an employee to enter a noncompete "
     "agreement, that does not satisfy a statutory exception. Section 16600.5 provides "
     "that an employer shall not enter into a contract with an employee or prospective "
     "employee that includes a provision that is void under that chapter, and authorizes "
     "a prospective employee to bring a private action for injunctive relief, actual "
     "damages, or both, with reasonable attorney's fees and costs to a prevailing "
     "plaintiff."),
    ("PARA",
     "Plaintiff was a prospective employee. The offer letter Hertz issued and Plaintiff "
     "accepted is a contract with a prospective employee. It includes a provision making "
     "Plaintiff's execution of an \"Employee Confidentiality & Non-Competition\" agreement "
     "\"a fundamental term and condition\" of his employment. That provision requires "
     "Plaintiff to enter a non-competition agreement as the price of the job. No "
     "statutory exception applies.", "noncompete"),
    ("PARA",
     "By including that provision, Hertz entered into a contract with a prospective "
     "employee that includes a provision void under section 16600, and required "
     "Plaintiff to enter a noncompete agreement, in violation of sections 16600.1 and "
     "16600.5. On information and belief, Hertz uses the same offer-letter provision for "
     "California hires generally."),
    ("PARA",
     "An actual and present controversy exists. Hertz has made the non-competition "
     "requirement a condition of the job Plaintiff accepted and seeks to begin, so he "
     "cannot take the position without submitting to a restraint California declares "
     "void. Plaintiff seeks a declaration under 28 U.S.C. §§ 2201-2202 that the provision, "
     "and any non-competition covenant it requires, is void and unenforceable as to him; "
     "an injunction under section 16600.5 prohibiting Hertz from requiring or enforcing "
     "it; actual damages according to proof; and costs and any attorney's fees "
     "incurred."),

    ("HEADER", "X.\nPRESERVATION OF EVIDENCE"),
    ("PARA",
     "Defendants are on notice of this action and must preserve all records concerning "
     "Plaintiff and requisition 43711, including: Oracle candidate 2847550 status history; "
     "HireRight order OR-102326-NH87V in every version; the adjudication rules \"The Hertz "
     "Corporation (Shell) (GL-HTZ001-001) v1.7\" and \"Managed Adjudication 3.0\" and their "
     "configuration for registry, MVR, and criminal results, including every reason code "
     "and category label; the source, endpoint, and raw results of each registry "
     "subrequest; the identity, screens, notes, and communications of each person who "
     "performed the November 2 \"Client Review\"; the generation history of the Notice; "
     "the native electronic-consent records for the October 23 disclosures; and the "
     "Employee Confidentiality & Non-Competition agreement and its use for California "
     "hires."),

    ("HEADER", "XI.\nPRAYER FOR RELIEF"),
    ("PARA", "Plaintiff prays for judgment as follows:"),
    ("LIST_ITEM", "On the First Cause of Action, against HireRight:"),
    ("LIST_ITEM", "1. Actual damages, or statutory damages of not less than $100 and not more "
                  "than $1,000, and punitive damages (15 U.S.C. § 1681n(a)); or, in the "
                  "alternative, actual damages (15 U.S.C. § 1681o(a));"),
    ("LIST_ITEM", "On the Second Cause of Action, against Hertz:"),
    ("LIST_ITEM", "2. Actual damages, including emotional-distress damages and lost wages and "
                  "benefits, according to proof;"),
    ("LIST_ITEM", "3. An additional amount determined by the trier of fact, not exceeding three "
                  "times actual damages and not less than $250 (Cal. Penal Code "
                  "§ 290.46(j)(4)(A));"),
    ("LIST_ITEM", "4. Exemplary damages or, in the alternative, a civil penalty not exceeding "
                  "$25,000 (id.; Cal. Civ. Code § 3294);"),
    ("LIST_ITEM", "5. Preventive relief, including an injunction, under Cal. Penal Code "
                  "§ 290.46(j)(4)(B);"),
    ("LIST_ITEM", "On the Third Cause of Action, against Hertz:"),
    ("LIST_ITEM", "6. Actual damages or $10,000, whichever is greater, and punitive damages "
                  "(Cal. Civ. Code § 1786.50);"),
    ("LIST_ITEM", "On the Fourth Cause of Action, against Hertz:"),
    ("LIST_ITEM", "7. Actual damages or $200, whichever is greater; for an intentional "
                  "violation, treble actual damages or $500, whichever is greater (Cal. Labor "
                  "Code § 432.7(c));"),
    ("LIST_ITEM", "On the Fifth Cause of Action, against Hertz:"),
    ("LIST_ITEM", "8. A declaration that Hertz's non-competition provision and any "
                  "non-competition covenant it requires are void and unenforceable as to "
                  "Plaintiff;"),
    ("LIST_ITEM", "9. An injunction prohibiting Hertz from requiring or enforcing that "
                  "provision or covenant, and actual damages according to proof (Cal. Bus. & "
                  "Prof. Code § 16600.5(e));"),
    ("LIST_ITEM", "On All Causes of Action:"),
    ("LIST_ITEM", "10. Costs of suit, and reasonable attorney's fees to the extent incurred and "
                  "authorized by statute;"),
    ("LIST_ITEM", "11. Prejudgment and post-judgment interest as permitted by law; and"),
    ("LIST_ITEM", "12. Such other relief as the Court deems just and proper."),

    ("HEADER", "XII.\nDEMAND FOR JURY TRIAL"),
    ("PARA", "Under Federal Rule of Civil Procedure 38(b) and Civil Local Rule 3-6, Plaintiff "
             "demands a trial by jury on all issues so triable."),
]


def _verification(d: PleadingPaper, exec_date: str, city: str, execute: bool) -> None:
    d.start_new_page()
    d.write_line("VERIFICATION", bold=True, center=True)
    d.blank_line()
    d.write_wrapped("I, BRENDAN NGWA NFORBI, declare:", first_indent=36)
    d.blank_line()
    d.write_wrapped(
        "I am the Plaintiff in this action. I have read the foregoing Verified Complaint and "
        "know its contents. The matters stated in it are true of my own knowledge, except "
        "those stated on information and belief, and as to those matters I believe them to "
        "be true.", first_indent=36)
    d.blank_line()
    d.write_wrapped(
        "I declare under penalty of perjury under the laws of the United States of America "
        "that the foregoing is true and correct. 28 U.S.C. § 1746.", first_indent=36)
    d.blank_line()
    d.write_wrapped(f"Executed on {exec_date}, at {city}, California.", first_indent=36)
    d.ensure_space(8)
    d.blank_line()
    d.blank_line()
    if execute:
        d.draw_signature_image(S.SIGNATURE_PATH, S.SIGNATURE_NATIVE_PX[0], S.SIGNATURE_NATIVE_PX[1],
                               S.SIG_LINE, width=225, height_scale=1.0)
    d.write_line(S.SIG_LINE, right=True, right_margin_offset=20)
    d.write_line(S.SIGNOFF_NAME, right=True, right_margin_offset=20)


def build(out: Path, exec_date: str, city: str, execute: bool) -> Path:
    numbered, labels = S._number(CONTENT)
    out.parent.mkdir(parents=True, exist_ok=True)
    d = PleadingPaper(str(out), doc_title_footer=FOOTER, style="minimal")
    c = d.c
    y0 = d._line_y(0)
    for i, (txt, font_name, size) in enumerate(S.PLAINTIFF_BLOCK):
        c.setFont(font_name, size)
        c.drawString(CONTENT_LEFT, y0 - i * 15, txt)
    d.current_line = 4
    d.blank_line()
    for line in COURT:
        d.write_line(line, bold=True, center=True)
    d.draw_caption_block(CAPTION_LEFT, CAPTION_RIGHT, caption_size=8.2, tight_lh=10.5, boxed=True)
    d.blank_line()
    for kind, text in numbered:
        text = S._resolve(text, labels)
        if kind == "HEADER":
            lines = text.split("\n")
            d.ensure_space(len(lines) + 5)
            for line in lines:
                d.write_line(line, bold=True, center=True)
            d.blank_line()
        elif kind == "SUBHEAD":
            lines = text.split("\n")
            d.ensure_space(len(lines) + 3)
            for line in lines:
                d.write_line(line, bold=True, center=len(lines) > 1)
            d.blank_line()
        elif kind == "PARA":
            d.write_wrapped(text, first_indent=36)
            d.blank_line()
        elif kind == "LIST_ITEM":
            d.write_wrapped(text, indent=36, first_indent=0)
            if text.startswith("12. "):
                d.blank_line()
    d.blank_line()
    d.ensure_space(12)
    d.write_line(f"Dated: {exec_date}")
    d.blank_line()
    d.write_line("Respectfully submitted,", right=True, right_margin_offset=20)
    d.blank_line()
    d.blank_line()
    if execute:
        d.draw_signature_image(S.SIGNATURE_PATH, S.SIGNATURE_NATIVE_PX[0], S.SIGNATURE_NATIVE_PX[1],
                               S.SIG_LINE, width=225, height_scale=1.0)
    d.write_line(S.SIG_LINE, right=True, right_margin_offset=20)
    d.write_line(S.SIGNOFF_NAME, right=True, right_margin_offset=20)
    d.write_line(S.SIGNOFF_ROLE, right=True, right_margin_offset=20)
    _verification(d, exec_date, city, execute)
    d.save()
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("out", nargs="?", default=str(OUT))
    ap.add_argument("--date", default="November 12, 2026")
    ap.add_argument("--city", default="Stockton")
    ap.add_argument("--execute", action="store_true", help="Affix signature")
    a = ap.parse_args()
    print("Generated:", build(Path(a.out).resolve(), a.date, a.city, a.execute))


if __name__ == "__main__":
    main()
