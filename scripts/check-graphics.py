#!/usr/bin/env python3
"""Verify every SVG in public/graphics/ against the brief's constraints.

The brief exists because these constraints are easy to breach without noticing,
and the first attempt at generating these files breached nearly all of them.
This script is the check that a report of "done" cannot substitute for.

    python3 scripts/check-graphics.py
"""

from __future__ import annotations

import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DIR = ROOT / "public" / "graphics"

EXPECTED = [
    "cat-business.svg",
    "cat-digital.svg",
    "cat-property.svg",
    "step-inquiry.svg",
    "step-scoping.svg",
    "step-draft.svg",
    "step-review.svg",
    "texture-paper.svg",
    "divider-rule.svg",
]

MAX_BYTES = 4096
# Anything in the yellow-through-amber band. Gold belongs to the logo alone;
# measured, it sits at 1.6:1 to 2.5:1 on the page background.
GOLD = re.compile(r"#(?:[cdef][89ab][0-9a-f]{2}[0-9a-f]{2}|b[89a][8-9a-f]|c9a2)", re.I)


def check(path: Path) -> list[str]:
    raw = path.read_text(encoding="utf-8")
    errs: list[str] = []

    try:
        root = ET.fromstring(raw)
    except ET.ParseError as e:
        return [f"does not parse as XML: {e}"]

    # 1. no text of any kind
    if root.iter("{http://www.w3.org/2000/svg}text") and any(
        root.iter("{http://www.w3.org/2000/svg}text")
    ):
        errs.append("contains <text> — forbidden, invisible to screen readers")
    for tag in ("tspan", "textPath", "foreignObject"):
        if any(root.iter(f"{{http://www.w3.org/2000/svg}}{tag}")):
            errs.append(f"contains <{tag}> — forbidden")

    # 2. sized by the page, not by the file
    if "viewBox" not in root.attrib:
        errs.append("no viewBox on the root element")
    for attr in ("width", "height"):
        if attr in root.attrib:
            errs.append(f'root has hard-coded {attr}="{root.attrib[attr]}"')

    # 3. retintable
    if "currentColor" not in raw:
        errs.append("never uses currentColor — cannot be retinted by CSS")

    # 4. gold is the logo's alone
    hit = GOLD.search(raw)
    if hit:
        errs.append(f"contains a gold-band colour ({hit.group(0)})")

    # 5. no second hue, no gradients
    if "Gradient" in raw:
        errs.append("contains a gradient — one flat accent only")

    # 6. self-contained
    for bad in ("http://www.w3.org/1999/xlink", "xlink:href", "<image"):
        if bad in raw and "href" in raw:
            errs.append(f"contains an external reference ({bad})")
    if re.search(r'href\s*=\s*"(?!#)', raw):
        errs.append("contains an href to something other than a local id")

    # 7. no editor leftovers
    for junk in ("inkscape", "sodipodi", "Adobe", "<metadata", "<!--"):
        if junk.lower() in raw.lower():
            errs.append(f"contains editor metadata or comments ({junk})")

    # 8. weight
    size = len(raw.encode("utf-8"))
    if size > MAX_BYTES:
        errs.append(f"{size} bytes, over the {MAX_BYTES} limit")

    return errs


def main() -> None:
    if not DIR.exists():
        sys.exit(f"{DIR} does not exist.")

    present = sorted(p.name for p in DIR.glob("*.svg"))
    missing = [n for n in EXPECTED if n not in present]
    extra = [n for n in present if n not in EXPECTED]

    failures = 0
    for name in EXPECTED:
        path = DIR / name
        if not path.exists():
            continue
        errs = check(path)
        size = len(path.read_bytes())
        if errs:
            failures += 1
            print(f"FAIL  {name}  ({size}B)")
            for e in errs:
                print(f"      - {e}")
        else:
            print(f"ok    {name:22} {size:>5}B")

    if missing:
        print(f"\nMISSING: {', '.join(missing)}")
        failures += len(missing)
    if extra:
        print(f"\nUNEXPECTED (not in the brief): {', '.join(extra)}")

    total = sum(p.stat().st_size for p in DIR.glob("*.svg"))
    print(f"\n{len(present)} file(s), {total} bytes total")

    if failures:
        sys.exit(1)
    print("All constraints met: no text, no gold, no gradients, no external")
    print("references, viewBox-sized, retintable via currentColor.")


if __name__ == "__main__":
    main()
