#!/usr/bin/env python3
"""Measure WCAG contrast for every colour pair the design system actually uses.

Regulation 35 points at IS 5568, which adopts WCAG at level AA. The thresholds
that matter here:

    4.5:1  normal text
    3.0:1  large text (>=18.66px bold, or >=24px) and UI component boundaries

Run it whenever a token changes. It exits non-zero on a failure so it can be
wired into the build later.

    python3 scripts/check-contrast.py
"""

from __future__ import annotations

import sys


def srgb_to_lin(c: float) -> float:
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def luminance(hex_colour: str) -> float:
    h = hex_colour.lstrip("#")
    r, g, b = (int(h[i : i + 2], 16) / 255 for i in (0, 2, 4))
    return 0.2126 * srgb_to_lin(r) + 0.7152 * srgb_to_lin(g) + 0.0722 * srgb_to_lin(b)


def ratio(fg: str, bg: str) -> float:
    a, b = luminance(fg), luminance(bg)
    hi, lo = max(a, b), min(a, b)
    return (hi + 0.05) / (lo + 0.05)


# (label, foreground, background, minimum required)
DIRECTIONS: dict[str, dict[str, str]] = {
    "A — לוח": {
        "page": "#FFFFFF",
        "ink": "#14171A",
        "muted": "#5A6169",
        "faint": "#6A7179",
        "rule": "#E4E6E9",
        # #8B9199 clears 3:1 on white but lands at 2.99:1 on the grey surface.
        # One step darker, same hue, clears both.
        "line-control": "#888E96",
        "accent": "#1F4FA3",
        "accent-ink": "#FFFFFF",
        "surface": "#F7F8F9",
    },
    "B — מסלול": {
        "page": "#FBFAF8",
        "ink": "#1B1D1F",
        "muted": "#5B615E",
        "faint": "#6C716E",
        "rule": "#E6E4DF",
        "line-control": "#8A8F8B",
        "accent": "#1B3A6B",
        "accent-ink": "#FFFFFF",
        "surface": "#FFFFFF",
    },
}

# Which pairs get checked, and at what threshold. "3.0" covers large display
# text and the non-text contrast of borders and focus rings.
PAIRS = [
    ("ink on page", "ink", "page", 4.5),
    ("ink on surface", "ink", "surface", 4.5),
    ("muted on page", "muted", "page", 4.5),
    ("muted on surface", "muted", "surface", 4.5),
    # --faint is used for 12-13px legal fine print, so it is held to the
    # normal-text threshold, not the large-text one.
    ("faint on page", "faint", "page", 4.5),
    ("faint on surface", "faint", "surface", 4.5),
    ("accent on page", "accent", "page", 4.5),
    ("accent on surface", "accent", "surface", 4.5),
    ("accent-ink on accent (button)", "accent-ink", "accent", 4.5),
    # 1.4.11 covers borders that *identify a control*. A hairline dividing two
    # sections is decoration and is exempt, which is why --rule is deliberately
    # not listed here: holding a section divider to 3:1 would force a grey dark
    # enough to read as a table border and would wreck the restraint the whole
    # design depends on. Input and card-control borders are a different token
    # and do get held to 3:1.
    ("control border on page", "line-control", "page", 3.0),
    ("control border on surface", "line-control", "surface", 3.0),
    ("accent as focus ring on page", "accent", "page", 3.0),
    ("accent as focus ring on surface", "accent", "surface", 3.0),
]


def main() -> None:
    failures = 0
    for name, tokens in DIRECTIONS.items():
        print(f"\n{name}")
        print("  " + "-" * 62)
        for label, fg_key, bg_key, need in PAIRS:
            fg, bg = tokens[fg_key], tokens[bg_key]
            r = ratio(fg, bg)
            ok = r >= need
            mark = "PASS" if ok else "FAIL"
            if not ok:
                failures += 1
            print(f"  {mark}  {r:5.2f}:1  (needs {need})  {label}  {fg} on {bg}")

    print()
    if failures:
        print(f"{failures} pair(s) below threshold.")
        sys.exit(1)
    print("All pairs meet their threshold.")


if __name__ == "__main__":
    main()
