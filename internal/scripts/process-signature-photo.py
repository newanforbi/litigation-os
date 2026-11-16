#!/usr/bin/env python3
"""Photographed loops mark → archive PNG only.

Archive copy: *-v2-photo-loops.png
Source photo: *-source-v2-photo.jpg

The live canonical (brendan-newanforbi-signature.png) is the November 2026
445×106 wet-ink stamp. This script must not overwrite it. Pixel guards
still refuse paper-plate / form-rule junk in the archive rebuild.

Does not restamp any already-filed PDF.

    python3 internal/scripts/process-signature-photo.py
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR / "lib"))
sys.path.insert(0, str(SCRIPT_DIR))

from signature_quality import (  # noqa: E402
    assert_house_assets_gone,
    validate_signature_rgba,
)

REPO = Path(__file__).resolve().parents[2]
SRC_JPG = (
    REPO / "internal/assets/signature/brendan-newanforbi-signature-source-v2-photo.jpg"
)
OUT_PNG = (
    REPO / "internal/assets/signature/brendan-newanforbi-signature-v2-photo-loops.png"
)
CANONICAL_PNG = REPO / "internal/assets/signature/brendan-newanforbi-signature.png"
PREVIEW_PNG = (
    REPO / "internal/assets/signature/brendan-newanforbi-signature-preview.png"
)

INK_MAX = 210
CROP_PAD = 6
SCALE = 12
CLOSE_SIZE = 3
ERODE_SIZE = 5
BLUR = 3.0
CORE_T = 212
ALPHA_FLOOR = 22
INK_RGB = 40
TRIM_PAD = 12


def _crop_ink(gray: Image.Image) -> Image.Image:
    g = np.array(gray, dtype=np.uint8)
    ys, xs = np.where(g < INK_MAX)
    if ys.size == 0:
        raise SystemExit("no ink found in source JPEG")
    y0 = max(0, int(ys.min()) - CROP_PAD)
    y1 = min(g.shape[0], int(ys.max()) + CROP_PAD + 1)
    x0 = max(0, int(xs.min()) - CROP_PAD)
    x1 = min(g.shape[1], int(xs.max()) + CROP_PAD + 1)
    return gray.crop((x0, y0, x1, y1))


def _mask(hi: Image.Image) -> Image.Image:
    g = np.array(hi, dtype=np.uint8)
    core = Image.fromarray(((g < 185).astype(np.uint8) * 255), "L")
    closed = core.filter(ImageFilter.MaxFilter(CLOSE_SIZE)).filter(
        ImageFilter.MinFilter(CLOSE_SIZE)
    )
    thinned = closed.filter(ImageFilter.MinFilter(ERODE_SIZE))
    return thinned.filter(ImageFilter.GaussianBlur(radius=BLUR))


def _to_rgba(alpha_img: Image.Image) -> Image.Image:
    a = np.array(alpha_img, dtype=np.float32)
    solid = a >= CORE_T
    fringe = np.clip((a - ALPHA_FLOOR) / (CORE_T - ALPHA_FLOOR), 0.0, 1.0)
    alpha = np.where(solid, 1.0, fringe)
    alpha_u8 = (alpha * 255.0).astype(np.uint8)
    ys, xs = np.where(alpha_u8 > 8)
    y0 = max(0, int(ys.min()) - TRIM_PAD)
    y1 = min(alpha_u8.shape[0], int(ys.max()) + TRIM_PAD + 1)
    x0 = max(0, int(xs.min()) - TRIM_PAD)
    x1 = min(alpha_u8.shape[1], int(xs.max()) + TRIM_PAD + 1)
    alpha_u8 = alpha_u8[y0:y1, x0:x1]
    rgba = np.zeros((alpha_u8.shape[0], alpha_u8.shape[1], 4), dtype=np.uint8)
    rgba[..., 0] = INK_RGB
    rgba[..., 1] = INK_RGB
    rgba[..., 2] = INK_RGB
    rgba[..., 3] = alpha_u8
    return Image.fromarray(rgba, "RGBA")


def _write_preview(rgba: Image.Image) -> None:
    bg = Image.new("RGBA", rgba.size, (255, 255, 255, 255))
    rgb = Image.alpha_composite(bg, rgba).convert("RGB")
    draw = ImageDraw.Draw(rgb)
    w, h = rgb.size
    y = h - max(8, h // 20)
    draw.line(
        (int(w * 0.05), y, int(w * 0.95), y),
        fill=(0, 0, 0),
        width=max(2, h // 200),
    )
    rgb.save(PREVIEW_PNG, optimize=True)


def main() -> None:
    try:
        assert_house_assets_gone()
    except ValueError as exc:
        raise SystemExit(str(exc)) from exc

    if not SRC_JPG.is_file():
        raise SystemExit(f"Missing photo source: {SRC_JPG}")
    gray = Image.open(SRC_JPG).convert("L")
    crop = _crop_ink(gray)
    hi = crop.resize(
        (crop.size[0] * SCALE, crop.size[1] * SCALE), Image.Resampling.LANCZOS
    )
    rgba = _to_rgba(_mask(hi))
    try:
        validate_signature_rgba(np.asarray(rgba), label="rebuild")
    except ValueError as exc:
        raise SystemExit(f"rebuild failed quality gate: {exc}") from exc

    rgba.save(OUT_PNG, optimize=True)
    _write_preview(rgba)
    print(
        f"wrote archive {OUT_PNG.name} "
        f"{rgba.size[0]}×{rgba.size[1]}  "
        f"aspect={rgba.size[1]/rgba.size[0]:.4f}  "
        f"from crop {crop.size}"
    )
    print(f"preview: {PREVIEW_PNG}")
    print(
        f"left live stamp untouched: {CANONICAL_PNG.name} "
        "(November 2026 445×106 wet-ink)"
    )


if __name__ == "__main__":
    main()
