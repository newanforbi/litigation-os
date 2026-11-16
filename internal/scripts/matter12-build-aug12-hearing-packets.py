#!/usr/bin/env python3
"""Build Matter 12 Aug 12, 2026 hearing hand-up default judgment packets.

Clean compensatory-only packets for Dept. 11B prove-up (Hon. Waters), fixing
defects from the Aug 3/4 submissions:
  - CIV-100 item 6b(2): named defendant only (no Mustagem Usmani ghost text)
  - Alpine item 1c/1d: full amended-summons caption (alter-ego language)
  - CIV-100 item 5 parent checkbox checked with the three "is not" answers
  - Item 2 money filled; punitive omitted; costs waived
  - All execution / mailing dates = August 12, 2026
  - Signature lines left BLANK for wet signature at the hearing

Packet order (each defendant):
  1. Notice to Filing Party (014b)
  2. Defendant's Proof of Service cover
  3. Civil ROA Summary (FullCourt)
  4. CIV-100 (clean Judicial Council fill; signed)
  5. JUD-100 proposed judgment ($53,671.20; no punitive)
  6. CIV-110 Request for Dismissal of Does 1–20
  7. Declaration ISO Default Judgment (Aug 12; no punitive; signed)
  8. Exhibits 1–10
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path

import fitz

ROOT = Path(__file__).resolve().parents[2]
SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
from signature_stamp import (  # noqa: E402
    SIGNATURE_PATH,
    stamp_on_pdf_line,
)

OUT_DIR = ROOT / "internal/public/documents/matter-12"
BUILD_DIR = Path("/tmp/m12build")
FORMS_DIR = Path("/tmp/m12forms")
UPLOADS = Path("/home/ubuntu/.cursor/projects/workspace/uploads")

# Portfolio universal signature (internal/assets/signature/…).
SIGNATURE_IMG = Path(SIGNATURE_PATH)
# Prefer portfolio copy; fall back to uploads mirror used by the Aug 4 builder.
NOTICE_PDF = OUT_DIR / "014b Notice to Filing Party.pdf"
if not NOTICE_PDF.is_file():
    NOTICE_PDF = UPLOADS / "Notice_to_Filing_Party_e500.pdf"
ROA_PDF = OUT_DIR / "FullCourt Enterprise - Civil ROA Summary (as of Aug 2 2026).pdf"
BLANK_CIV100 = FORMS_DIR / "civ100.pdf"
BLANK_JUD100 = FORMS_DIR / "jud100.pdf"
BLANK_CIV110 = FORMS_DIR / "civ110.pdf"

DIAMOND_SRC = BUILD_DIR / "backup_Diamond_packet_pre_fix.pdf"
ALPINE_SRC = BUILD_DIR / "backup_Alpine_packet_pre_fix.pdf"

DIAMOND_OUT = OUT_DIR / (
    "1094 Diamond Default Judgment Packet "
    "(Compensatory Only, Hearing Hand-Up Aug 12 2026).pdf"
)
ALPINE_OUT = OUT_DIR / (
    "1094 Alpine Default Judgment Packet "
    "(Compensatory Only, Hearing Hand-Up Aug 12 2026).pdf"
)
CIV110_OUT = OUT_DIR / (
    "1094 CIV-110 Request for Dismissal of Does 1-20 "
    "(Without Prejudice, Executed Aug 12 2026).pdf"
)
ARTIFACTS_DIR = Path("/opt/cursor/artifacts")

CASE_NO = "STK-CV-UF-2026-0001094"
PLAINTIFF = "BRENDAN NGWA NFORBI"
PLAINTIFF_PRINT = "Brendan Ngwa Nforbi"
DATE_SHORT = "08/12/2026"
DATE_LONG = "August 12, 2026"
FAC_FILED = "05/11/2026"

# Exact defendant names as on the Amended Summons (clerk-issued June 11, 2026).
DIAMOND_AS_SUED = "DIAMOND TRUCK SALES, INC., a California corporation"
ALPINE_AS_SUED = (
    "ALPINE TRUCK SALES, INC., a California corporation "
    "(sued individually and as the successor in interest, mere continuation, "
    "and/or alter ego of Diamond Truck Sales, Inc.)"
)

DEMAND = "49,368.65"
INTEREST = "4,302.55"
COSTS = "0.00"
TOTAL = "53,671.20"
ZERO = "0.00"
RATE = "7"

# Backups rebuilt from Aug 4 packets: page 0 = POS cover; pages 1..end = exhibits.
DIAMOND_RANGES = {"pos": (0, 1), "exhibits": (1, 35)}
ALPINE_RANGES = {"pos": (0, 1), "exhibits": (1, 35)}

PARTY = {
    "name": PLAINTIFF_PRINT,
    "street": "1455 Cat Tail Drive",
    "city": "Stockton",
    "state": "CA",
    "zip": "95204",
    "phone": "(209) 801-4442",
    "email": "bnn.cdl@gmail.com",
    "atty_for": "Plaintiff, In Pro Per",
}
COURT = {
    "county": "SAN JOAQUIN",
    "street": "180 E. Weber Avenue",
    "mailing": "180 E. Weber Avenue",
    "cityzip": "Stockton, CA 95202",
    "branch": "Stockton Courthouse",
}


def _endswith(name: str, *suffixes: str) -> bool:
    return any(name.endswith(s) for s in suffixes)


def set_text(doc: fitz.Document, suffix: str, value: str) -> int:
    n = 0
    for page in doc:
        for w in page.widgets() or []:
            if w.field_type_string == "Text" and _endswith(w.field_name or "", suffix):
                w.field_value = value
                w.update()
                n += 1
    return n


def set_text_exact(doc: fitz.Document, full_suffix: str, value: str) -> int:
    """Match widgets whose field_name ends with the given path suffix."""
    n = 0
    for page in doc:
        for w in page.widgets() or []:
            if w.field_type_string == "Text" and (w.field_name or "").endswith(full_suffix):
                w.field_value = value
                w.update()
                n += 1
    return n


def check_by_label(
    doc: fitz.Document,
    label_substr: str,
    on: bool = True,
    *,
    exact: bool = False,
) -> int:
    n = 0
    target = label_substr.lower()
    for page in doc:
        for w in page.widgets() or []:
            if w.field_type_string not in ("CheckBox", "RadioButton"):
                continue
            lab = (w.field_label or "").strip()
            lab_l = lab.lower()
            if exact:
                match = lab_l == target
            else:
                match = target in lab_l
            if match:
                w.field_value = w.on_state() if on else "Off"
                w.update()
                n += 1
    return n


def check_widget(doc: fitz.Document, name_endswith: str, on_state: str | int | None = None) -> int:
    n = 0
    for page in doc:
        for w in page.widgets() or []:
            if not (w.field_name or "").endswith(name_endswith):
                continue
            if w.field_type_string not in ("CheckBox", "RadioButton"):
                continue
            val = on_state if on_state is not None else w.on_state()
            w.field_value = val
            w.update()
            n += 1
    return n


def check_radio_choice(doc: fitz.Document, name_contains: str, on_value) -> int:
    """Check the widget in a radio/checkbox group whose on_state equals on_value."""
    n = 0
    for page in doc:
        for w in page.widgets() or []:
            name = w.field_name or ""
            if name_contains not in name:
                continue
            if w.field_type_string not in ("CheckBox", "RadioButton"):
                continue
            if w.on_state() == on_value or str(w.on_state()) == str(on_value):
                w.field_value = w.on_state()
                w.update()
                n += 1
    return n


# Wet-signature build: leave every signature line blank for hand signing.
WET_SIGNATURE = True


def stamp_sig(page: fitz.Page, x0: float, x1: float, y_line: float) -> None:
    """Stamp the portfolio universal signature on the form line."""
    if WET_SIGNATURE:
        return
    stamp_on_pdf_line(page, x0, x1, y_line, path=str(SIGNATURE_IMG))


def force_off(doc: fitz.Document, pred) -> int:
    """Force matching checkboxes Off so bake does not treat blank as checked."""
    n = 0
    for page in doc:
        for w in page.widgets() or []:
            if w.field_type_string not in ("CheckBox", "RadioButton"):
                continue
            if pred(w):
                w.field_value = "Off"
                w.update()
                n += 1
    return n


def fill_caption_common(doc: fitz.Document, defendant_caption: str) -> None:
    set_text(doc, "AttyName[0]", PARTY["name"])
    set_text(doc, "Name[0]", PARTY["name"])  # CIV-110 uses Name[0]
    set_text(doc, "AttyStreet[0]", PARTY["street"])
    set_text(doc, "Street[0]", PARTY["street"])
    set_text(doc, "AttyCity[0]", PARTY["city"])
    set_text(doc, "City[0]", PARTY["city"])
    set_text(doc, "AttyState[0]", PARTY["state"])
    set_text(doc, "State[0]", PARTY["state"])
    set_text(doc, "AttyZip[0]", PARTY["zip"])
    set_text(doc, "Zip[0]", PARTY["zip"])
    set_text(doc, "Phone[0]", PARTY["phone"])
    set_text(doc, "Email[0]", PARTY["email"])
    set_text(doc, "AttyFor[0]", PARTY["atty_for"])
    set_text(doc, "CrtCounty[0]", COURT["county"])
    # CIV-100 court street field is Street[0] under CourtInfo — already set above
    # may collide; set specific court fields by longer suffix where needed.
    set_text_exact(doc, "CourtInfo[0].Street[0]", COURT["street"])
    set_text_exact(doc, "CourtInfo[0].CrtStreet[0]", COURT["street"])
    set_text_exact(doc, "CourtInfo[0].MailingAdd[0]", COURT["mailing"])
    set_text_exact(doc, "CourtInfo[0].CrtMailingAdd[0]", COURT["mailing"])
    set_text_exact(doc, "CourtInfo[0].CityZip[0]", COURT["cityzip"])
    set_text_exact(doc, "CourtInfo[0].CrtCityZip[0]", COURT["cityzip"])
    set_text_exact(doc, "CourtInfo[0].Branch[0]", COURT["branch"])
    set_text_exact(doc, "CourtInfo[0].CrtBranch[0]", COURT["branch"])
    set_text(doc, "CaseNumber[0]", CASE_NO)
    set_text(doc, "Party1[0]", PLAINTIFF)
    set_text(doc, "Party2[0]", defendant_caption)


def _set_text_fontsize(doc: fitz.Document, suffix: str, size: float) -> None:
    for page in doc:
        for w in page.widgets() or []:
            if (w.field_name or "").endswith(suffix) and w.field_type_string == "Text":
                w.text_fontsize = size
                w.update()


def fill_civ100(
    defendant_name: str,
    mail_name: str,
    *,
    caption_defendant: str | None = None,
) -> fitz.Document:
    doc = fitz.open(BLANK_CIV100)
    # Caption Party2 can stay short; items 1c/1d carry the as-sued language.
    fill_caption_common(doc, caption_defendant or defendant_name)

    # Title checkboxes: Entry of Default + Court Judgment
    check_by_label(doc, "Entry of Default")
    check_by_label(doc, "Court Judgment")

    # Item 1
    set_text_exact(doc, "Lia[0].DateField1[0]", FAC_FILED)
    set_text_exact(doc, "Lib[0].FillText99[0]", PLAINTIFF_PRINT)
    check_by_label(doc, "Enter default of defendant")
    # Alpine's amended-summons caption is long; shrink 1c/1d so the full
    # "sued individually and as the successor…" language fits the single-line field.
    if len(defendant_name) > 90:
        _set_text_fontsize(doc, "Lic[0].TextField6[0]", 5.5)
        _set_text_fontsize(doc, "Lid[0].TextField6[0]", 5.5)
    set_text_exact(doc, "Lic[0].TextField6[0]", defendant_name)
    check_by_label(doc, "I request a court judgment")
    set_text_exact(doc, "Lid[0].TextField6[0]", defendant_name)

    # Item 2 money
    set_text_exact(doc, "SubLia[0].FillText68[0]", DEMAND)
    set_text_exact(doc, "SubLia[0].FillText67[0]", ZERO)
    set_text_exact(doc, "SubLia[0].FillText66[0]", DEMAND)
    set_text_exact(doc, "SubLic[0].FillText59[0]", INTEREST)
    set_text_exact(doc, "SubLic[0].FillText58[0]", ZERO)
    set_text_exact(doc, "SubLic[0].FillText57[0]", INTEREST)
    set_text_exact(doc, "SubLid[0].FillText56[0]", COSTS)
    set_text_exact(doc, "SubLid[0].FillText55[0]", ZERO)
    set_text_exact(doc, "SubLid[0].FillText54[0]", COSTS)
    set_text_exact(doc, "SubLif[0].FillText73[0]", TOTAL)  # amount col
    set_text_exact(doc, "SubLif[0].FillText72[0]", ZERO)  # credits col
    set_text_exact(doc, "SubLif[0].FillText71[0]", TOTAL)  # balance col

    # Page 1 signature block
    set_text_exact(doc, "Signature[0].sigDate[0]", DATE_SHORT)
    set_text_exact(doc, "Signature[0].signame[0]", PLAINTIFF)

    # Item 4 — did not receive LDA/UDA help (on_state=2 for "did not")
    check_radio_choice(doc, "UDAsst[", 2)

    # Item 6 — mailed to named defendant (mailStatus on=2)
    check_radio_choice(doc, "List6[0].lib[0].mailStatus[0]", 2)
    # Also try generic mailStatus mailed choice
    for page in doc:
        for w in page.widgets() or []:
            lab = (w.field_label or "").lower()
            if "mailed first-class" in lab:
                w.field_value = w.on_state()
                w.update()
    set_text_exact(doc, "li1[0].FillText129[0]", DATE_LONG)
    set_text_exact(
        doc,
        "li2[0].FillText130[0]",
        f"{mail_name}\n1201 S. Soderquist Road\nTurlock, CA 95380",
    )

    # Item 4/5/6 declaration date+name
    set_text_exact(doc, "Declaration1[0].sigDate[0]", DATE_SHORT)
    set_text_exact(doc, "Declaration1[0].sigName[0]", PLAINTIFF)

    # Item 5 — CCP §585.5 parent + all three "is not" (Unruh / Rees-Levering / §395(b)).
    check_by_label(doc, "Declaration under Code Civ. Proc., § 585.5")
    check_radio_choice(doc, "P2Li5a[0].Contract_cb[", 2)
    check_radio_choice(doc, "P2Li5b[0].ConditionalContract_cb[", 2)
    check_radio_choice(doc, "P2Li5c[0].Obligaition_cb[", 2)

    # Item 7f costs waived
    check_by_label(doc, "Costs and disbursements are waived")
    set_text_exact(doc, "Declaration2[0].sigDate[0]", DATE_SHORT)
    set_text_exact(doc, "Declaration2[0].sigName[0]", PLAINTIFF)

    # Item 8 — business entity
    check_by_label(doc, "a business entity")
    # Also check parent "not eligible... because they are"
    for page in doc:
        for w in page.widgets() or []:
            lab = (w.field_label or "").lower()
            if "not eligible to serve in the u.s. military because" in lab:
                w.field_value = w.on_state()
                w.update()
    set_text_exact(doc, "Declaration3[0].sigDate[0]", DATE_SHORT)
    set_text_exact(doc, "Declaration3[0].sigName[0]", PLAINTIFF)

    # Force Off on unused Yes-state / optional boxes so bake stays clean.
    # Do NOT force off the item-5 §585.5 parent — it must stay checked.
    force_off(
        doc,
        lambda w: any(
            s in (w.field_label or "").lower()
            for s in (
                "clerk's judgment",
                "enter clerk",
                "restitution of the premises",
                "under code of civil procedure section 585(a)",
                "for default previously entered",
                "unlawful detainer case",
            )
        )
        or (w.field_label or "").strip() in ("is", "did", "incarcerated", "other"),
    )
    # Re-assert the intended choices after force_off.
    check_by_label(doc, "Declaration under Code Civ. Proc., § 585.5")
    check_radio_choice(doc, "UDAsst[", 2)
    check_radio_choice(doc, "P2Li5a[0].Contract_cb[", 2)
    check_radio_choice(doc, "P2Li5b[0].ConditionalContract_cb[", 2)
    check_radio_choice(doc, "P2Li5c[0].Obligaition_cb[", 2)
    for page in doc:
        for w in page.widgets() or []:
            lab = (w.field_label or "").lower()
            if "mailed first-class" in lab:
                w.field_value = w.on_state()
                w.update()
            if lab.strip() == "a business entity":
                w.field_value = w.on_state()
                w.update()
            if "not eligible to serve in the u.s. military because" in lab:
                w.field_value = w.on_state()
                w.update()
    check_by_label(doc, "Costs and disbursements are waived")

    # Stamp pen signatures (right of printed-name fields)
    # Universal signature on each CIV-100 signature line (width ~110 → ~30pt tall).
    stamp_sig(doc[0], 400, 510, 680)  # p1 plaintiff signature
    stamp_sig(doc[1], 400, 510, 448)  # p2 items 4–6 declarant
    stamp_sig(doc[1], 400, 510, 645)  # p2 item 7 declarant
    stamp_sig(doc[2], 400, 510, 698)  # p3 item 8 declarant

    doc.bake(annots=True, widgets=True)
    return doc


def fill_jud100(defendant_short: str, defendant_against: str, other_text: str) -> fitz.Document:
    doc = fitz.open(BLANK_JUD100)
    # JUD-100 caption fields
    set_text(doc, "CaseNumber[0]", CASE_NO)
    set_text(doc, "Party1[0]", PLAINTIFF_PRINT)
    set_text(doc, "Party2[0]", f"{defendant_short}, a California corporation, et al.")
    set_text_exact(doc, "AttyInfo[0].AttyName[0]", PARTY["name"])
    set_text_exact(doc, "AttyInfo[0].AttyStreet[0]", PARTY["street"])
    set_text_exact(doc, "AttyInfo[0].AttyCity[0]", PARTY["city"])
    set_text_exact(doc, "AttyInfo[0].AttyState[0]", PARTY["state"])
    set_text_exact(doc, "AttyInfo[0].AttyZip[0]", PARTY["zip"])
    set_text_exact(doc, "AttyInfo[0].Phone[0]", PARTY["phone"])
    set_text_exact(doc, "AttyInfo[0].Email[0]", PARTY["email"])
    set_text_exact(doc, "AttyInfo[0].AttyFor[0]", PARTY["atty_for"])
    set_text_exact(doc, "CourtInfo[0].CrtCounty[0]", COURT["county"])
    set_text_exact(doc, "CourtInfo[0].Street[0]", COURT["street"])
    set_text_exact(doc, "CourtInfo[0].MailingAdd[0]", COURT["mailing"])
    set_text_exact(doc, "CourtInfo[0].CityZip[0]", COURT["cityzip"])
    set_text_exact(doc, "CourtInfo[0].Branch[0]", COURT["branch"])

    # Form title: By Court + By Default (never After Court Trial — default prove-up).
    check_by_label(doc, "By Court", exact=True)
    check_by_label(doc, "By Default", exact=True)

    # Item 1 BY DEFAULT + court judgment on declaration
    check_by_label(doc, "BY DEFAULT", exact=True)
    check_by_label(doc, "Court Judgment (Code of Civil Procedure Section 585(b)")
    check_by_label(doc, "plaintiff's written declaration")

    # Page 2: judgment by THE COURT (exact — "the court" also appears in item 3).
    check_by_label(doc, "THE COURT", exact=True)

    # Item 5a for plaintiff / against defendant (only 5a — never 5b).
    check_by_label(doc, "for plaintiff", exact=True)
    set_text_exact(doc, "Lia[0].FillText20[0]", PLAINTIFF_PRINT)
    set_text_exact(doc, "Lia[0].FillText21[0]", defendant_against)
    # Item 5b must stay blank/unchecked when no 5b defendant is named.
    check_by_label(doc, "for defendant", on=False, exact=True)
    set_text_exact(doc, "Lib[0].FillText13[0]", "")

    # Item 6a amounts — no "Other"/punitive
    check_by_label(doc, "Defendant named in item 5a above must")
    for page in doc:
        for w in page.widgets() or []:
            name = w.field_name or ""
            if "List6[0].Lia[0].Table1[0]" not in name:
                continue
            lab = (w.field_label or "").lower()
            if w.field_type_string == "CheckBox":
                if lab.strip() in ("damages", "costs") or "prejudgment interest" in lab:
                    w.field_value = w.on_state()
                    w.update()
            elif w.field_type_string == "Text":
                if name.endswith("EXPN[0]"):
                    w.field_value = DEMAND
                    w.update()
                elif name.endswith("NumericField2[0]"):
                    w.field_value = RATE
                    w.update()
                elif name.endswith("EXPN1[0]"):
                    w.field_value = INTEREST
                    w.update()
                elif name.endswith("EXPN3[0]"):
                    w.field_value = COSTS
                    w.update()
                elif name.endswith("EXPN5[0]"):
                    w.field_value = TOTAL
                    w.update()

    # Item 8 other findings (non-punitive) — only List8, not amount-table "Other"
    for page in doc:
        for w in page.widgets() or []:
            name = w.field_name or ""
            if name.endswith("RB2Choices87[0]"):
                w.field_value = w.on_state()
                w.update()
            if name.endswith("item8[0].FillText88[0]"):
                w.field_value = other_text
                w.update()
            # Keep amount-table Other lines clear (no punitive)
            if name.endswith("Table1[0].RB2Choices14[0]") or name.endswith(
                "Table2[0].RB2Choices99[0]"
            ):
                w.field_value = "Off"
                w.update()
            if any(
                name.endswith(s)
                for s in (
                    "Table1[0].FillText51[0]",
                    "Table1[0].EXPN4[0]",
                    "Table2[0].FillText111[0]",
                    "Table2[0].EXPN4[0]",
                )
            ):
                w.field_value = ""
                w.update()

    # Force Off incompatible / unused judgment paths before bake.
    force_off(
        doc,
        lambda w: any(
            s in (w.field_label or "").lower()
            for s in (
                "by clerk",
                "after court trial",
                "defendant did not appear at trial",
                "on stipulation",
                "clerk's judgment",
                "plaintiff's testimony and other evidence",
                "plaintiff to receive nothing from defendant",
                "defendant named in item 5b to recover",
                "for cross-complainant",
                "for cross-defendant",
            )
        )
        or (w.field_label or "").strip() == "for defendant"
        or (
            (w.field_label or "").strip() == "Other"
            and "item8" not in (w.field_name or "").lower()
        )
        or (w.field_name or "").endswith("List5[0].Lib[0].CheckBox34[0]")
        or (w.field_name or "").endswith("List6[0].Lib[0].CBChoice41[0]"),
    )
    # Re-assert the intended checks after force_off.
    check_by_label(doc, "By Court", exact=True)
    check_by_label(doc, "By Default", exact=True)
    check_by_label(doc, "BY DEFAULT", exact=True)
    check_by_label(doc, "Court Judgment (Code of Civil Procedure Section 585(b)")
    check_by_label(doc, "plaintiff's written declaration")
    check_by_label(doc, "THE COURT", exact=True)
    check_by_label(doc, "for plaintiff", exact=True)
    check_by_label(doc, "Defendant named in item 5a above must")
    for page in doc:
        for w in page.widgets() or []:
            name = w.field_name or ""
            lab = (w.field_label or "").lower()
            if "List6[0].Lia[0].Table1[0]" in name and w.field_type_string == "CheckBox":
                if lab.strip() in ("damages", "costs") or "prejudgment interest" in lab:
                    w.field_value = w.on_state()
                    w.update()
            if name.endswith("RB2Choices87[0]"):
                w.field_value = w.on_state()
                w.update()

    # Final guard: Item 5b / 6b off, 5b name blank — only 5a carries the debtor.
    check_by_label(doc, "for defendant", on=False, exact=True)
    check_by_label(doc, "Plaintiff to receive nothing from defendant", on=False)
    set_text_exact(doc, "Lib[0].FillText13[0]", "")
    for page in doc:
        for w in page.widgets() or []:
            name = w.field_name or ""
            if name.endswith("List5[0].Lib[0].CheckBox34[0]") or name.endswith(
                "List6[0].Lib[0].CBChoice41[0]"
            ):
                w.field_value = "Off"
                w.update()

    doc.bake(annots=True, widgets=True)
    return doc


def fill_civ110() -> fitz.Document:
    doc = fitz.open(BLANK_CIV110)
    defendant_caption = "DIAMOND TRUCK SALES, INC., et al."
    fill_caption_common(doc, defendant_caption)
    # CIV-110 uses Name[0] not AttyName — ensure set
    set_text_exact(doc, "AttyPartyInfo[0].Name[0]", PARTY["name"])
    set_text_exact(doc, "AttyPartyInfo[0].Street[0]", PARTY["street"])
    set_text_exact(doc, "AttyPartyInfo[0].City[0]", PARTY["city"])
    set_text_exact(doc, "AttyPartyInfo[0].State[0]", PARTY["state"])
    set_text_exact(doc, "AttyPartyInfo[0].Zip[0]", PARTY["zip"])
    set_text_exact(doc, "AttyPartyInfo[0].Phone[0]", PARTY["phone"])
    set_text_exact(doc, "AttyPartyInfo[0].Email[0]", PARTY["email"])
    set_text_exact(doc, "AttyPartyInfo[0].AttyFor[0]", PARTY["atty_for"])

    # 1a(2) Without prejudice (on_state=2)
    check_radio_choice(doc, "li1a2[0].RB1Choices[0]", 2)
    # 1b(1) Complaint only (exact — do not match "Cross-complaint")
    check_by_label(doc, "Complaint", exact=True)
    # 1b(6) Other — Does only
    check_radio_choice(doc, "li1b6[0].RB2Choices[0]", 2)
    set_text_exact(
        doc,
        "li1b6[0].FillText109[0]",
        "Does 1 through 20, inclusive, only",
    )
    # Blank Yes-state widgets can bake as checked — force Off on unused boxes.
    force_off(
        doc,
        lambda w: (w.field_label or "").strip().lower().startswith("cross-complaint")
        or (w.field_label or "").strip() in ("Petition", "With prejudice")
        or "retaining jurisdiction" in (w.field_label or "").lower()
        or "Entire action" in (w.field_label or ""),
    )

    # Item 2: court DID waive fees
    check_radio_choice(doc, "CheckBox2D[", 1)  # did
    set_text_exact(doc, "List2[0].DateTimeField1[0]", DATE_SHORT)
    set_text_exact(doc, "List2[0].Sig1Name[0]", PLAINTIFF)
    check_radio_choice(doc, "List2[0].CheckBox2A[", 2)  # party without attorney
    # Plaintiff/Petitioner
    for page in doc:
        for w in page.widgets() or []:
            name = w.field_name or ""
            lab = (w.field_label or "").strip()
            if "List2[0]" in name and lab == "Plaintiff/Petitioner":
                w.field_value = w.on_state()
                w.update()

    # Item 2 signature: right of printed name, on the line above "(SIGNATURE)".
    stamp_sig(doc[0], 430, 530, 469)  # ~100pt wide → ~27pt tall

    # Page 2 — Declaration Concerning Waived Court Fees
    set_text_exact(doc, "Item1[0].FillText109[0]", PLAINTIFF_PRINT)
    check_radio_choice(doc, "li2c[0].CBCourtFee[0]", 3)  # recovering $10,000+
    # Item 3: waived fees paid? No (on_state=2, oddly named Yes[0])
    for page in doc:
        for w in page.widgets() or []:
            name = w.field_name or ""
            lab = (w.field_label or "").strip()
            if "Item3[0].Yes[" in name and lab == "No":
                w.field_value = w.on_state()
                w.update()
    set_text_exact(doc, "PoP[0].DateTimeField1[0]", DATE_SHORT)
    set_text_exact(doc, "PoP[0].YourName2[0]", PLAINTIFF)
    check_radio_choice(doc, "PoP[0].CheckBox4A[", 2)  # party making declaration
    # Page 2 signature: on the line above "(SIGNATURE)".
    stamp_sig(doc[1], 430, 530, 370)

    doc.bake(annots=True, widgets=True)
    return doc


def run_declarations() -> tuple[Path, Path]:
    BUILD_DIR.mkdir(parents=True, exist_ok=True)
    env = dict(os.environ)
    env["MATTER12_DECL_OUT_DIR"] = str(BUILD_DIR)
    env["MATTER12_EXEC_DATE"] = DATE_LONG
    env["MATTER12_DECL_TAG"] = "Aug12_2026"
    if WET_SIGNATURE:
        env["MATTER12_NO_SIGNATURE"] = "1"
    subprocess.check_call(
        [sys.executable, str(SCRIPT_DIR / "matter12-default-declaration-formatter.py")],
        env=env,
    )
    diamond = BUILD_DIR / "_build_Diamond_Declaration_ISO_Default_Judgment_Aug12_2026.pdf"
    alpine = BUILD_DIR / "_build_Alpine_Declaration_ISO_Default_Judgment_Aug12_2026.pdf"
    if not diamond.is_file() or not alpine.is_file():
        raise SystemExit("Declaration build outputs missing")
    return diamond, alpine


def ensure_forms() -> None:
    FORMS_DIR.mkdir(parents=True, exist_ok=True)
    urls = {
        BLANK_CIV100: "https://www.courts.ca.gov/documents/civ100.pdf",
        BLANK_JUD100: "https://www.courts.ca.gov/documents/jud100.pdf",
        BLANK_CIV110: "https://www.courts.ca.gov/documents/civ110.pdf",
    }
    for path, url in urls.items():
        if path.is_file() and path.stat().st_size > 10_000:
            continue
        subprocess.check_call(
            ["curl", "-fsSL", "-A", "Mozilla/5.0", "-L", url, "-o", str(path)]
        )


def assemble(
    src_path: Path,
    ranges: dict[str, tuple[int, int]],
    civ100: fitz.Document,
    civ110: fitz.Document,
    decl_path: Path,
    jud100: fitz.Document,
    out_path: Path,
) -> None:
    src = fitz.open(src_path)
    notice = fitz.open(NOTICE_PDF)
    roa = fitz.open(ROA_PDF)
    decl = fitz.open(decl_path)

    out = fitz.open()
    out.insert_pdf(notice)
    out.insert_pdf(src, from_page=ranges["pos"][0], to_page=ranges["pos"][1] - 1)
    out.insert_pdf(roa)
    out.insert_pdf(civ100)
    out.insert_pdf(jud100)
    out.insert_pdf(civ110)
    out.insert_pdf(decl)
    out.insert_pdf(src, from_page=ranges["exhibits"][0], to_page=ranges["exhibits"][1] - 1)

    tmp = out_path.with_suffix(".tmp.pdf")
    out.save(tmp, garbage=4, deflate=True)
    out.close()
    src.close()
    notice.close()
    roa.close()
    decl.close()
    shutil.move(str(tmp), str(out_path))
    print(f"Wrote {out_path.name} ({fitz.open(out_path).page_count} pages)")


def _first_exhibit_page(doc: fitz.Document) -> int:
    for i in range(5, doc.page_count):
        text = doc[i].get_text() or ""
        if "EXHIBIT" in text and "SAN JOAQUIN COUNTY SUPERIOR COURT" in text:
            return i
    return doc.page_count


def verify(path: Path) -> None:
    doc = fitz.open(path)
    full = "\n".join(page.get_text() for page in doc)
    checks = {
        "has_notice": "NOTICE TO FILING PARTY" in full,
        "has_roa": "ROA Summary" in full or "CIVIL ROA SUMMARY" in full,
        "roa_alpine_served": "Alpine Truck Sales" in full and "07/01/2026" in full,
        "demand_49368": DEMAND in full,
        "interest": INTEREST in full,
        "total_53671": TOTAL in full,
        "no_78671": "78,671.20" not in full,
        "no_25000_punitive": "25,000.00" not in full,
        "exec_aug12": ("August 12, 2026" in full) or ("08/12/2026" in full),
        "no_aug3_exec": "August 3, 2026" not in full,
        "no_aug4_exec": "August 4, 2026" not in full and "08/04/2026" not in full,
        "has_civ110": "REQUEST FOR DISMISSAL" in full and "Does 1 through 20" in full,
        "costs_waived": "waived" in full.lower(),
        # Wet-signature build: CIV-100 / JUD-100 / CIV-110 / declaration pages
        # must carry no stamped signature image (exhibit scans excluded; the
        # blank Judicial Council forms embed a tiny 15x28 ornament — ignore it).
        "form_pages_unsigned": not any(
            img[2] > 100
            for i in range(5, _first_exhibit_page(doc))
            for img in doc[i].get_images()
        ),
        "no_usmani_mail_ghost": "Mustagem Usmani" not in full and "Sonderquist" not in full,
        "item5_parent": "Declaration under Code Civ. Proc., § 585.5" in full,
    }
    if "Alpine" in path.name:
        checks["osmani_family"] = "Osmani family" in full
        checks["usmani_served"] = "Mustaqem Usmani" in full
        checks["stanislaus"] = "Stanislaus County" in full
        checks["alpine_1c_full_summons"] = "successor in interest" in full.lower()
    if "Diamond" in path.name:
        checks["diamond_named"] = "DIAMOND TRUCK SALES" in full.upper()
    print(f"Verify {path.name}:")
    fails = 0
    for k, ok in checks.items():
        print(f"  {'OK' if ok else 'FAIL'}: {k}")
        if not ok:
            fails += 1
    # Spot-check CIV-100 page (after notice + POS + 3-page ROA = index 5)
    if doc.page_count > 5:
        civ_txt = doc[5].get_text()
        print(f"  CIV-100 contains 1a date {FAC_FILED}: {FAC_FILED in civ_txt}")
        print(f"  CIV-100 contains demand: {DEMAND in civ_txt}")
        # 6b2 clean named defendant on mailing page (index 6)
        mail_words = " ".join(w[4] for w in doc[6].get_text("words"))
        print(f"  6b2 has Mustagem: {'Mustagem' in mail_words}")
        print(f"  6b2 has Soderquist: {'Soderquist' in mail_words}")
    print(f"  pages={doc.page_count}")
    doc.close()
    if fails:
        raise SystemExit(f"Verification failed ({fails} checks) for {path.name}")


def main() -> None:
    if not SIGNATURE_IMG.is_file():
        raise SystemExit(f"Missing signature image: {SIGNATURE_IMG}")
    if not NOTICE_PDF.is_file():
        raise SystemExit(f"Missing Notice to Filing Party: {NOTICE_PDF}")
    if not ROA_PDF.is_file():
        raise SystemExit(f"Missing Civil ROA Summary: {ROA_PDF}")
    if not DIAMOND_SRC.is_file() or not ALPINE_SRC.is_file():
        raise SystemExit("Missing pre-fix packet backups in /tmp/m12build")

    ensure_forms()
    diamond_decl, alpine_decl = run_declarations()

    civ110 = fill_civ110()
    # Save standalone CIV-110 for convenience / download
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    civ110.save(CIV110_OUT, garbage=4, deflate=True)
    print(f"Wrote {CIV110_OUT.name}")

    diamond_civ = fill_civ100(DIAMOND_AS_SUED, "Diamond Truck Sales, Inc.")
    alpine_civ = fill_civ100(
        ALPINE_AS_SUED,
        "Alpine Truck Sales, Inc.",
        caption_defendant="ALPINE TRUCK SALES, INC., a California corporation",
    )

    diamond_jud = fill_jud100(
        "Diamond Truck Sales, Inc.",
        DIAMOND_AS_SUED,
        (
            "The April 4, 2023 purchase transaction between Plaintiff and Diamond "
            "Truck Sales, Inc. is rescinded, and the contractual \"as-is\" disclaimer "
            "is unenforceable."
        ),
    )
    alpine_jud = fill_jud100(
        "Alpine Truck Sales, Inc.",
        ALPINE_AS_SUED,
        (
            "Alpine Truck Sales, Inc. is jointly and severally liable with Diamond "
            "Truck Sales, Inc. as Diamond's successor, mere continuation, alter ego, "
            "and/or fraudulent transferee. April 4, 2023 purchase rescinded; as-is "
            "disclaimer unenforceable."
        ),
    )

    # CIV-110 is baked once; reopen for second insert
    civ110_diamond = fitz.open(CIV110_OUT)
    civ110_alpine = fitz.open(CIV110_OUT)

    assemble(
        DIAMOND_SRC,
        DIAMOND_RANGES,
        diamond_civ,
        civ110_diamond,
        diamond_decl,
        diamond_jud,
        DIAMOND_OUT,
    )
    assemble(
        ALPINE_SRC,
        ALPINE_RANGES,
        alpine_civ,
        civ110_alpine,
        alpine_decl,
        alpine_jud,
        ALPINE_OUT,
    )

    diamond_civ.close()
    alpine_civ.close()
    diamond_jud.close()
    alpine_jud.close()
    civ110.close()
    civ110_diamond.close()
    civ110_alpine.close()

    verify(DIAMOND_OUT)
    verify(ALPINE_OUT)

    # Publish print-ready copies for download.
    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
    for src in (DIAMOND_OUT, ALPINE_OUT, CIV110_OUT):
        dest = ARTIFACTS_DIR / src.name
        shutil.copy2(src, dest)
        print(f"Artifact: {dest}")


if __name__ == "__main__":
    main()
