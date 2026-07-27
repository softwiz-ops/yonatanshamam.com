#!/usr/bin/env python3
"""Derive every brand asset the site needs from the masters in brand-assets/.

Sources, and why each one:

  Google Gemini Image Preview.png       shield only, RGBA with real
                                        transparency. 677x369. The two
                                        "Generated Image" masters are 2816px
                                        but flat on a cream ground with no
                                        alpha, so they cannot be keyed out
                                        cleanly — the shield is line art with
                                        light highlights inside it.
  Google Gemini Generated Image (1).png full lockup at 2816px, on cream. Used
                                        for the share card, where a background
                                        is wanted anyway.

Aspect ratio is handled by trimming to the real ink bounds FIRST and then
composing onto a canvas of the intended size. Forcing a square width/height
onto a non-square PNG is what baked black bars into the transparent margins on
the other site; do not "simplify" this by resizing straight to a square.

    python3 scripts/build-brand-assets.py

Needs Pillow. Re-runnable; overwrites its outputs.
"""

from __future__ import annotations

import sys
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    sys.exit("Pillow is required:  pip3 install Pillow")

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "brand-assets"
OUT = ROOT / "public"

SHIELD = SRC / "Google Gemini Image Preview.png"
LOCKUP_HI = SRC / "Google Gemini Generated Image (1).png"

# The site's warm paper ground. The mark is gold line art: on pure white it
# looks washed out, and on a dark ground it loses the gradient entirely.
PAPER = (251, 250, 248, 255)


def trimmed(path: Path) -> Image.Image:
    """Open an RGBA master and crop to the actual ink."""
    im = Image.open(path).convert("RGBA")
    box = im.getchannel("A").getbbox()
    if box is None:
        sys.exit(f"{path.name} has no visible pixels — is it flattened?")
    return im.crop(box)


def contain(im: Image.Image, size: int, pad: float) -> Image.Image:
    """Fit `im` inside a square canvas, preserving its aspect ratio."""
    inner = int(size * (1 - pad))
    scaled = im.copy()
    scaled.thumbnail((inner, inner), Image.LANCZOS)
    canvas = Image.new("RGBA", (size, size), PAPER)
    canvas.paste(
        scaled,
        ((size - scaled.width) // 2, (size - scaled.height) // 2),
        scaled,
    )
    return canvas


def main() -> None:
    for p in (SHIELD, LOCKUP_HI):
        if not p.exists():
            sys.exit(f"missing master: {p}")

    OUT.mkdir(parents=True, exist_ok=True)
    shield = trimmed(SHIELD)
    print(f"shield ink bounds: {shield.size}")

    # --- header mark -------------------------------------------------------
    # Rendered at 34px tall in the header, so 3x covers every display.
    for scale in (1, 2, 3):
        h = 34 * scale
        w = max(1, round(shield.width * h / shield.height))
        out = OUT / (f"logo-shield@{scale}x.png" if scale > 1 else "logo-shield.png")
        shield.resize((w, h), Image.LANCZOS).save(out, optimize=True)
        print(f"  {out.name}  {w}x{h}")

    # --- favicons ----------------------------------------------------------
    # Square canvases, but the shield keeps its own proportions inside them.
    for size, name in ((32, "favicon-32.png"), (180, "apple-touch-icon.png")):
        contain(shield, size, pad=0.18).convert("RGB").save(OUT / name, optimize=True)
        print(f"  {name}  {size}x{size}")

    # --- share card --------------------------------------------------------
    # 1200x630. The live site serves a 197x246 image against a 1200x630
    # minimum, which is why its share cards render badly.
    card = Image.new("RGBA", (1200, 630), PAPER)
    lock = Image.open(LOCKUP_HI).convert("RGBA")
    lock.thumbnail((980, 500), Image.LANCZOS)
    card.paste(lock, ((1200 - lock.width) // 2, (630 - lock.height) // 2), lock)
    # JPEG, not PNG: the card is a gold gradient on flat paper, which PNG
    # stores at ~580KB and JPEG at a tenth of that with no visible difference.
    # Share-card crawlers accept JPEG, and the file is fetched on every share.
    card.convert("RGB").save(
        OUT / "og-image.jpg", quality=88, optimize=True, progressive=True
    )
    kb = (OUT / "og-image.jpg").stat().st_size // 1024
    print(f"  og-image.jpg  1200x630  {kb}KB")

    print("\nThe mark stays gold and is used ONLY as a logo.")
    print("Measured: the logo gold is 1.6:1-2.5:1 on the page background, and")
    print("reaching 4.5:1 needs a 36% darkening that lands on olive. WCAG")
    print("exempts logotypes from contrast, so the mark is fine as a mark —")
    print("but gold must never be used for text, icons or controls.")


if __name__ == "__main__":
    main()
