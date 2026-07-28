#!/usr/bin/env python3
"""Check the Hebrew copy against the rules in the hebrew-content-writer skill.

Covers only what can be measured mechanically. Register, flow and whether a
sentence actually sounds like a person still need a human read — this catches
the errors that survive one.

    python3 scripts/check-hebrew.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src"

# Title tags: 50-60 Hebrew characters, primary keyword near the beginning.
# Meta descriptions: 120-150 characters.
TITLE_MIN, TITLE_MAX = 40, 60
DESC_MIN, DESC_MAX = 120, 160

# Calques and register slips the skill calls out by name.
CALQUES: list[tuple[str, str, str]] = [
    (r"\bבכדי\b", "כדי", "overused as a fancier כדי; default to plain כדי"),
    (r"\bאתה צריך\b", "יש ל…", "impersonal 'you' — use יש ל / אפשר / ניתן"),
    (r"\bאתה יכול\b", "אפשר / ניתן", "impersonal 'you'"),
    (r"\bאת יכולה\b", "אפשר / ניתן", "impersonal 'you'"),
    (r"בסוף היום", "בסופו של דבר", "literal 'at the end of the day'"),
    (r"עושה סנס|עושה שכל", "הגיוני / מסתדר", "literal 'makes sense'"),
    (r"\bנשמח אם\b", "direct phrasing", "English-style softener; dugri drops it"),
    (r"\bייתכן שכדאי\b", "direct phrasing", "softener stack"),
]

# Ktiv maleh: the deficient spelling on the left is wrong in modern copy.
KTIV: list[tuple[str, str]] = [
    (r"\bתכנה\b", "תוכנה"),
    (r"\bשרות\b", "שירות"),
    (r"\bתכנית\b", "תוכנית"),
    (r"\bאמנם\b", "אומנם"),
]

# Words the Bar's rules put out of bounds, re-checked here because a content
# pass is exactly when one slips back in.
FORBIDDEN = [
    (r"\bמומח(?:ה|ית|ים)\b", "no specialisation certification exists in Israel"),
    (r"\bהטוב ביותר\b|\bהמוביל\b", "comparison and self-aggrandisement"),
    (r"\bמובטח\b|\bאנו מבטיחים\b", "promising an outcome"),
]


# Comments explain the rules; they are not copy. Scanning them flagged the very
# note that says never to use "מומחה", which is the opposite of a finding.
# Two patterns, and they must NOT share re.DOTALL. A line comment matched with
# re.S has "." spanning newlines, so `^\s*\*.*$` runs greedily to the end of the
# file — which blanked 59,000 of 60,900 characters of services.ts and made the
# whole check pass on an empty string. If this ever reports zero problems on a
# large file, verify what survived before believing it.
BLOCK_COMMENTS = re.compile(r"/\*.*?\*/|\{/\*.*?\*/\}|<!--.*?-->", re.S)
LINE_COMMENTS = re.compile(r"^[ \t]*(?://|\*).*$", re.M)


def strip_comments(text: str) -> str:
    """Blank out comments, preserving offsets so contexts stay meaningful."""
    blank = lambda m: " " * len(m.group(0))
    return LINE_COMMENTS.sub(blank, BLOCK_COMMENTS.sub(blank, text))


def hebrew_files() -> list[Path]:
    return sorted(
        [p for p in SRC.rglob("*.astro")]
        + [p for p in SRC.rglob("*.ts") if p.name != "config.ts"]
        + [p for p in SRC.rglob("*.md")]
    )


def main() -> None:
    problems: list[str] = []
    notes: list[str] = []

    for path in hebrew_files():
        text = strip_comments(path.read_text(encoding="utf-8"))
        rel = path.relative_to(ROOT)

        # --- SEO field lengths -------------------------------------------
        for label, pattern, lo, hi in (
            ("seoTitle", r"seoTitle:\s*\n?\s*'([^']+)'", TITLE_MIN, TITLE_MAX),
            ("title", r'\btitle="([^"]+)"', TITLE_MIN, TITLE_MAX),
            ("seoDescription", r"seoDescription:\s*\n?\s*'([^']+)'", DESC_MIN, DESC_MAX),
            ("description", r'\bdescription="([^"]+)"', DESC_MIN, DESC_MAX),
        ):
            for m in re.finditer(pattern, text):
                val = m.group(1)
                n = len(val)
                if n < lo or n > hi:
                    problems.append(
                        f"{rel}: {label} is {n} chars (want {lo}-{hi})\n"
                        f"      {val[:90]}…"
                    )

        # --- calques and register ----------------------------------------
        for pattern, better, why in CALQUES:
            for m in re.finditer(pattern, text):
                ctx = " ".join(text[max(0, m.start() - 40) : m.end() + 40].split())
                problems.append(f"{rel}: “{m.group(0)}” → {better} ({why})\n      …{ctx}…")

        # --- ktiv maleh ---------------------------------------------------
        for pattern, better in KTIV:
            for m in re.finditer(pattern, text):
                problems.append(f"{rel}: ktiv chaser “{m.group(0)}” → “{better}”")

        # --- the Bar's rules ----------------------------------------------
        for pattern, why in FORBIDDEN:
            for m in re.finditer(pattern, text):
                ctx = " ".join(text[max(0, m.start() - 40) : m.end() + 40].split())
                problems.append(f"{rel}: FORBIDDEN “{m.group(0)}” — {why}\n      …{ctx}…")

    # --- paragraph length, advisory ---------------------------------------
    # The skill asks for 2-3 sentence paragraphs: Hebrew reads denser than
    # English, and a long block is harder to scan and worse for extraction.
    services = (SRC / "data" / "services.ts").read_text(encoding="utf-8")
    for m in re.finditer(r"^\s{6}'([^']{200,})',$", services, re.M):
        para = m.group(1)
        sentences = len(re.findall(r"[.!?]\s", para)) + 1
        if sentences > 4:
            notes.append(f"  {sentences} sentences, {len(para)} chars: {para[:70]}…")

    for p in problems:
        print(f"FAIL  {p}")
    if notes:
        print(f"\nADVISORY — paragraphs over four sentences ({len(notes)}):")
        for n in notes[:8]:
            print(n)
        if len(notes) > 8:
            print(f"  …and {len(notes) - 8} more")

    print(f"\n{len(problems)} problem(s), {len(notes)} advisory")
    if problems:
        sys.exit(1)
    print("Hebrew copy passes the mechanical checks.")
    print("Register, rhythm and whether it sounds human still need a read.")


if __name__ == "__main__":
    main()
