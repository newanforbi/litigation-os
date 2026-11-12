"""Guards for the portfolio canonical signature PNG.

The August 26 wet-ink / "house" stamp put printed form-rule dashes and
crop plate into brendan-newanforbi-signature.png. Those pixels then
appeared on every stamped page. This module refuses a bad stamp before
it becomes canonical or gets drawn.

The live stamp (November 2026) is a 445×106 black-ink loop on a
transparent plate. The photographed-loops archive beside it
(*-v2-photo-loops.png, 5544×820) is historical only.
"""
from __future__ import annotations

import struct
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
SIGNATURE_DIR = REPO / "internal/assets/signature"
CANONICAL = SIGNATURE_DIR / "brendan-newanforbi-signature.png"
V2_ARCHIVE = SIGNATURE_DIR / "brendan-newanforbi-signature-v2-photo-loops.png"

# Live wet-ink loop is 445×106 → aspect ≈ 0.238.
# Photographed loops archive (v2) is 5544×820 → aspect ≈ 0.148.
CANONICAL_PX = (445, 106)
ASPECT_MIN = 0.10
ASPECT_MAX = 0.28
# Opaque ink should be charcoal, not a near-white paper plate or pure-black
# flood that hides dashes inside the stamp.
NEAR_WHITE = 230
MAX_NEAR_WHITE_OPAQUE = 0
MIN_OPAQUE_FRACTION = 0.01
MAX_OPAQUE_FRACTION = 0.55
INK_RGB_MAX = 80  # charcoal; house plate leaked paper / rule pixels


def _png_size(path: Path) -> tuple[int, int]:
    with path.open("rb") as fh:
        if fh.read(8) != b"\x89PNG\r\n\x1a\n":
            raise ValueError(f"Not a PNG: {path}")
        length, typ = struct.unpack(">I4s", fh.read(8))
        if typ != b"IHDR" or length < 8:
            raise ValueError(f"PNG missing IHDR: {path}")
        width, height = struct.unpack(">II", fh.read(8))
    return width, height


def _load_rgba(path: Path):
    from PIL import Image
    import numpy as np

    im = Image.open(path)
    if im.mode != "RGBA":
        raise ValueError(f"{path.name} must be RGBA, got {im.mode}")
    return np.asarray(im.convert("RGBA"))


def validate_signature_rgba(arr, *, label: str = "signature") -> None:
    """Raise ValueError if pixel stats look like paper plate / form-rule junk."""
    import numpy as np

    if arr.ndim != 3 or arr.shape[2] != 4:
        raise ValueError(f"{label}: expected HxWx4 RGBA array")
    h, w, _ = arr.shape
    if w < 100 or h < 20:
        raise ValueError(f"{label}: stamp too small ({w}×{h})")
    aspect = h / w
    if aspect < ASPECT_MIN or aspect > ASPECT_MAX:
        raise ValueError(
            f"{label}: aspect {aspect:.4f} outside [{ASPECT_MIN}, {ASPECT_MAX}] "
            "(refuses tall crop plates and house-scan leftovers)"
        )
    alpha = arr[..., 3]
    opaque = alpha > 10
    opaque_n = int(opaque.sum())
    total = h * w
    frac = opaque_n / total if total else 0.0
    if frac < MIN_OPAQUE_FRACTION or frac > MAX_OPAQUE_FRACTION:
        raise ValueError(
            f"{label}: opaque fraction {frac:.3f} outside "
            f"[{MIN_OPAQUE_FRACTION}, {MAX_OPAQUE_FRACTION}]"
        )
    rgb = arr[..., :3].astype(np.int16)
    near_white = opaque & (rgb.min(axis=2) >= NEAR_WHITE)
    nw = int(near_white.sum())
    if nw > MAX_NEAR_WHITE_OPAQUE:
        raise ValueError(
            f"{label}: {nw} near-white opaque pixels — form-rule / paper "
            "plate artifact (house stamp failure mode)"
        )
    mean_rgb = float(rgb[opaque].mean()) if opaque_n else 0.0
    if mean_rgb > INK_RGB_MAX:
        raise ValueError(
            f"{label}: mean opaque RGB {mean_rgb:.1f} too light "
            f"(max {INK_RGB_MAX}) — paper plate leak"
        )


def validate_signature_file(path: Path | str, *, label: str | None = None) -> None:
    path = Path(path)
    if not path.is_file():
        raise ValueError(f"missing signature file: {path}")
    _png_size(path)  # structural check before PIL
    validate_signature_rgba(_load_rgba(path), label=label or path.name)


def assert_canonical_stamp() -> None:
    """Canonical must be the live 445×106 stamp and pass pixel guards."""
    validate_signature_file(CANONICAL, label="canonical")
    width, height = _png_size(CANONICAL)
    if (width, height) != CANONICAL_PX:
        raise ValueError(
            f"canonical signature is {width}×{height}, expected "
            f"{CANONICAL_PX[0]}×{CANONICAL_PX[1]}"
        )


def assert_canonical_is_photo_loops(*, allow_force_mismatch: bool = False) -> None:
    """Back-compat alias — the live stamp is no longer the v2 photo-loops."""
    del allow_force_mismatch
    assert_canonical_stamp()


def banned_paths() -> list[Path]:
    """Assets that must never become SIGNATURE_PATH again."""
    return [
        SIGNATURE_DIR / "brendan-newanforbi-signature-v3-bbox-crop.png",
        SIGNATURE_DIR / "brendan-newanforbi-signature-source.jpg",
        REPO / "internal/scripts/assets/newanforbi-pen-signature.png",
        REPO / "internal/scripts/assets/_retired/newanforbi-pen-signature.png",
    ]


def assert_house_assets_gone() -> None:
    for p in banned_paths()[:2]:
        if p.exists():
            raise ValueError(
                f"house / wet-ink asset still on disk: {p}. Delete it."
            )
