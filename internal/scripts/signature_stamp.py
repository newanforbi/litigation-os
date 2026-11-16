# Portfolio universal signature: brendan-newanforbi-signature.png
# Live stamp (November 2026): 445×106 black-ink loop on a transparent
# plate. The photographed-loops rebuild
# (process-signature-photo.py → *-v2-photo-loops.png) is archival only
# and must not overwrite this path. Do not revive
# extract-signature-scan.py onto this path. Older archives beside it:
# *-v2-photo-loops.png, *-v1-abstract-loops.png, *-4b-civ100.png. Do not
# use internal/scripts/assets/newanforbi-pen-signature.png.
#
# stamp_on_pdf_line defaults to whiteout=True so printed form rules under
# the stamp cannot show through. Pixel guards in signature_quality refuse
# house-scan paper-plate / form-rule junk before it is drawn.
import struct
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[2]
_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS / "lib") not in sys.path:
    sys.path.insert(0, str(_SCRIPTS / "lib"))
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from signature_quality import (  # noqa: E402
    assert_canonical_stamp,
    assert_house_assets_gone,
    validate_signature_file,
)

SIGNATURE_PATH = str(
    _REPO_ROOT / "internal/assets/signature/brendan-newanforbi-signature.png"
)

_BANNED_NAMES = {
    "brendan-newanforbi-signature-v3-bbox-crop.png",
    "brendan-newanforbi-signature-source.jpg",
    "newanforbi-pen-signature.png",
}


def _png_size(path: str) -> tuple[int, int]:
    with open(path, "rb") as fh:
        if fh.read(8) != b"\x89PNG\r\n\x1a\n":
            raise SystemExit(f"Not a PNG: {path}")
        length, typ = struct.unpack(">I4s", fh.read(8))
        if typ != b"IHDR" or length < 8:
            raise SystemExit(f"PNG missing IHDR: {path}")
        width, height = struct.unpack(">II", fh.read(8))
    return width, height


def _guard_canonical() -> None:
    """Refuse to stamp if the house lineage returned or the PNG is dirty."""
    try:
        assert_house_assets_gone()
        assert_canonical_stamp()
    except ValueError as exc:
        raise SystemExit(f"signature guard: {exc}") from exc


def _resolve_stamp_path(path: str) -> str:
    if Path(path).name in _BANNED_NAMES:
        raise SystemExit(
            f"refusing banned signature asset: {path}. "
            "Use the photographed loops canonical only."
        )
    try:
        validate_signature_file(path)
    except ValueError as exc:
        raise SystemExit(f"signature guard: {exc}") from exc
    return path


_guard_canonical()

SIGNATURE_NATIVE_PX = _png_size(SIGNATURE_PATH)
# Draw slightly taller than the PNG so the loops expand upward from the
# signature line without getting wider.
SIGNATURE_HEIGHT_SCALE = 1.15
SIGNATURE_ASPECT = (
    SIGNATURE_NATIVE_PX[1] / SIGNATURE_NATIVE_PX[0]
) * SIGNATURE_HEIGHT_SCALE

# Judicial Council SER-001 page 4, right-hand "Sign your name" line
# (PyMuPDF top-origin coords). Shared by every fill-*-ser001.py.
SER001_SIG_PAGE_INDEX = 3
SER001_SIG_WIDTH = 120.0
SER001_SIG_BASELINE = 645.0
SER001_SIG_X = 360.0


def affix_signature(canvas_obj, x, y, width=185, path=SIGNATURE_PATH):
    """Draws the canonical signature onto a reportlab canvas at (x, y),
    scaled to `width` points wide and slightly taller than native aspect
    so the loops expand upward from the line."""
    path = _resolve_stamp_path(path)
    height = width * SIGNATURE_ASPECT
    canvas_obj.drawImage(path, x, y, width=width, height=height, mask="auto")
    return height


def stamp_on_pdf_line(page, x0, x1, y_line, path=SIGNATURE_PATH, *, whiteout=True):
    """Stamp the canonical signature onto a PyMuPDF page, sitting on y_line.

    whiteout fills the stamp rect with white first so form rules under the
    mark do not show through. Pass whiteout=False only when the form line
    must remain visible through the transparent PNG (tight signature/name
    stacks). Default True — that is what keeps printed dashes from stacking
    under a clean stamp.
    """
    import fitz

    path = _resolve_stamp_path(path)
    width = x1 - x0
    height = width * SIGNATURE_ASPECT
    rect = fitz.Rect(x0, y_line - height, x1, y_line)
    if whiteout:
        page.draw_rect(rect, color=(1, 1, 1), fill=(1, 1, 1), width=0)
    page.insert_image(rect, filename=path, keep_proportion=False)
    return rect


def stamp_ser001_signature(path, *, page_index=SER001_SIG_PAGE_INDEX):
    """Stamp the canonical signature on SER-001 page 4's signature line."""
    import fitz

    path = Path(path)
    if not Path(SIGNATURE_PATH).is_file():
        raise SystemExit(f"Missing signature image: {SIGNATURE_PATH}")
    _guard_canonical()
    doc = fitz.open(path)
    try:
        page = doc[page_index]
        stamp_on_pdf_line(
            page,
            SER001_SIG_X,
            SER001_SIG_X + SER001_SIG_WIDTH,
            SER001_SIG_BASELINE,
        )
        tmp = path.with_name(path.stem + ".signed.pdf")
        doc.save(tmp, garbage=4, deflate=True, incremental=False)
    finally:
        doc.close()
    tmp.replace(path)
    return path
