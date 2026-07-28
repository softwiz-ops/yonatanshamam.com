#!/usr/bin/env python3
"""Derive the portrait master that Astro's image pipeline consumes.

    python3 scripts/build-portrait.py

Reads   reference/photos/yonatan-portrait-original.jpg   (never modified)
Writes  src/assets/yonatan-portrait.jpg

Why this exists
---------------
The founder reported the portrait as smeared. Three plausible causes were
measured and excluded: it is not upscaled (230 CSS px display, so 460 physical
on a 2x screen, against a 640px original), the JPEG is not over-compressed
(q~95 by its quantisation table), and the original is not itself an upscale
(Laplacian variance 351, high-to-mid frequency ratio 0.22 — an upscaled image
keeps almost nothing near Nyquist).

What remained is that the photograph is simply soft, and that every downscale
softens further. Downscaling discards high-frequency detail; compensating with
a measured unsharp mask is the ordinary remedy, not a trick.

The mask is applied AT the delivered size, not to the original. Sharpening a
640px image and then resizing it to 460 throws most of the benefit away — the
resample removes exactly the frequencies the mask just raised. So this script
resamples first, then sharpens, and Astro's largest variant is then a 1:1 copy
of this file rather than another resize.

The parameters were chosen by measurement, not taste. Against the unsharpened
460px downscale:

    setting                     hi/mid freq    edge overshoot (p99.9)
    none                           0.2451                       152.0
    radius 0.8 / 80% / thr 3       0.3072                       197.1   <- used
    radius 1.0 / 100% / thr 3      0.3107                       218.0

The next step up buys 1% more sharpness for 10% more overshoot, which is where
sharpening starts to look cheap. Threshold 3 keeps the mask off flat skin and
sky, so it lifts edges without raising JPEG noise.

MASTER_WIDTH is 460 because the largest slot on the site is 230 CSS px (the
home page, `clamp(150px, 20vw, 230px)`), and 2x covers every current display.
Raise it only if a layout starts showing the portrait larger — and note that
the original is 640px wide, so 640 is the hard ceiling until the founder
supplies the photographer's full-resolution file. Nothing here can invent
detail that was never captured.
"""

from __future__ import annotations

import sys
from pathlib import Path

try:
    from PIL import Image, ImageFilter
except ImportError:
    sys.exit("Pillow is required:  pip3 install Pillow")

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "reference" / "photos" / "yonatan-portrait-original.jpg"
TARGET = ROOT / "src" / "assets" / "yonatan-portrait.jpg"

MASTER_WIDTH = 460
UNSHARP = dict(radius=0.8, percent=80, threshold=3)
QUALITY = 92  # the pipeline re-encodes to AVIF/WebP; this master stays generous


def main() -> None:
    if not SOURCE.exists():
        sys.exit(f"missing original: {SOURCE}")

    original = Image.open(SOURCE).convert("RGB")
    if original.width < MASTER_WIDTH:
        sys.exit(
            f"original is only {original.width}px wide — refusing to upscale to "
            f"{MASTER_WIDTH}px. Lower MASTER_WIDTH or supply a larger photo."
        )

    height = round(original.height * MASTER_WIDTH / original.width)
    resized = original.resize((MASTER_WIDTH, height), Image.LANCZOS)
    sharpened = resized.filter(ImageFilter.UnsharpMask(**UNSHARP))

    TARGET.parent.mkdir(parents=True, exist_ok=True)
    sharpened.save(TARGET, "JPEG", quality=QUALITY, subsampling=0, optimize=True)

    print(
        f"{SOURCE.name} {original.width}x{original.height}"
        f"  ->  {TARGET.name} {MASTER_WIDTH}x{height}"
        f"  ({TARGET.stat().st_size:,}B, unsharp {UNSHARP['radius']}/"
        f"{UNSHARP['percent']}%/{UNSHARP['threshold']})"
    )


if __name__ == "__main__":
    main()
