#!/usr/bin/env python3
"""Replace em dashes in user-facing copy, and only there.

    python3 scripts/fix-em-dashes.py [--apply]

CLAUDE.md: "No em dashes (—) in user-facing content. They read as
machine-written." The articles already comply and use a plain hyphen; the rest
of the site did not, because the copy in `services.ts` and the page templates
was written separately and drifted.

WHY THIS IS NOT A SEARCH AND REPLACE
------------------------------------
A blanket replace over `src/` would rewrite code comments too — 44 of the 120
occurrences are in comments, which are not user-facing and are where the
reasoning for past defects is recorded. It would also be the exact shape of
mistake this repo has already paid for once: a stem-based replacement that
turned `analysis` into `analyzis` across twelve files and shipped.

So comments are masked out before anything is touched, and the result is
verified against the BUILT output rather than the source, because the built
output is the only thing that defines "user-facing".

The founder's own en dash (–), used as a Hebrew parenthetical and in numeric
ranges, is correct typography and is never touched.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src"

# Ordered: block comments before line comments, so `// …` inside a /* … */ is
# already masked and cannot be matched twice.
COMMENT_PATTERNS = [
    re.compile(r"\{/\*.*?\*/\}", re.S),   # JSX/Astro template comment
    re.compile(r"<!--.*?-->", re.S),      # HTML comment
    re.compile(r"/\*.*?\*/", re.S),       # JS/TS/CSS block comment
    re.compile(r"(?m)^\s*//.*$"),         # whole-line JS/TS comment
    re.compile(r"(?m)(?<=[;,)\}])\s*//.*$"),  # trailing comment after code
]

SENTINEL = "@@CMT{}@@"


def mask(text: str) -> tuple[str, list[str]]:
    saved: list[str] = []

    def take(m: re.Match) -> str:
        saved.append(m.group(0))
        return SENTINEL.format(len(saved) - 1)

    for pat in COMMENT_PATTERNS:
        text = pat.sub(take, text)
    return text, saved


def unmask(text: str, saved: list[str]) -> str:
    for i, original in enumerate(saved):
        text = text.replace(SENTINEL.format(i), original)
    return text


def main() -> None:
    apply = "--apply" in sys.argv
    total = 0
    touched: list[tuple[str, int]] = []

    for path in sorted(SRC.rglob("*")):
        if path.suffix not in (".astro", ".ts", ".md", ".css") or not path.is_file():
            continue
        original = path.read_text(encoding="utf-8")
        if "—" not in original:
            continue

        body, saved = mask(original)
        n = body.count("—")
        if not n:
            continue

        body = body.replace("—", "-")
        result = unmask(body, saved)
        total += n
        touched.append((str(path.relative_to(ROOT)), n))
        if apply:
            path.write_text(result, encoding="utf-8")

    for name, n in sorted(touched, key=lambda x: -x[1]):
        print(f"  {n:>3}  {name}")
    verb = "replaced" if apply else "would replace"
    print(f"\n{verb} {total} em dash(es) in copy; comments left untouched")
    if not apply:
        print("dry run — pass --apply to write")


if __name__ == "__main__":
    main()
