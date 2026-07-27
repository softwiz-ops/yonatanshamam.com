#!/usr/bin/env python3
"""Scan the built site against the Bar's advertising rules.

The rule that shapes this file: the list of what a lawyer MAY publish is a
closed list, opening with "פרסומת מסוג, בצורה או בדרך כמפורט להלן בלבד מותרת
לעורך דין". Anything not enumerated there is forbidden. This script cannot
prove compliance — a closed list is not machine-checkable — but it does catch
the four categories that a copy edit is most likely to reintroduce.

Run against dist/ after every build:

    npm run build && python3 scripts/check-ethics.py

Exits non-zero on any hit, so it can be wired into CI later.
"""

from __future__ import annotations

import html
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DIST = ROOT / "dist" / "client"

# (label, pattern, why). Patterns run against visible text, not markup.
CHECKS: list[tuple[str, str, str]] = [
    (
        "שכר טרחה",
        # The permitted free text is defined as one "שאינו כולל כל התייחסות
        # לשכר הטרחה" — so any figure, any "from ₪", any free-consultation
        # offer is out, wherever it appears.
        r"₪\s*\d|\d+\s*(?:ש״ח|שח|שקל)|החל מ-?\s*\d|מחירון|הצעת מחיר|"
        r"ללא\s+(?:עלות|תשלום)|בחינם|חינם|שכר\s*טרחה\s*(?:של|מ-|החל)",
        "any reference to fees is forbidden, including 'free consultation'",
    ),
    (
        "מומחיות",
        # No formal specialisation certification exists in Israel to justify
        # the word. The rules' own term is "תחומי עיסוק".
        r"\bמומח(?:ה|ית|ים)\b|\bהתמחות ב|\bספציאליסט",
        "use 'תחומי עיסוק' — there is no specialisation certification in Israel",
    ),
    (
        "התגדלות והשוואה",
        r"הטוב ביותר|המוביל|מספר\s*1|הגדול ביותר|ללא תחרות|"
        r"טוב יותר מ|בניגוד למשרדים|שיעור הצלחה|אחוזי הצלחה",
        "comparison to other lawyers and self-aggrandisement are forbidden",
    ),
    (
        "הבטחת תוצאה",
        r"מובטח|אנו מבטיחים|תוצאה מובטחת|נצחון|בטוח שתזכו|100%\s*הצלחה",
        "promising outcomes is forbidden",
    ),
]

# Known matches that are NOT violations. Every entry needs a reason, and the
# reason has to survive being read out loud to the founder.
#
# `review=True` means it is not cleared — it stays printed on every run and does
# not fail the build, because it is the founder's call rather than a copy bug.
ALLOW: list[dict] = [
    {
        "pattern": r"100,000 ש״ח",
        "why": (
            "the statutory accessibility exemption threshold — content about "
            "the CLIENT's obligations under the regulations, not this firm's fee"
        ),
        "review": False,
    },
    {
        "pattern": r"ללא תשלום נוסף",
        "why": (
            "inside the migrated terms of service, describing how a defective "
            "document is corrected. It sits in a binding legal document rather "
            "than in advertising copy, and it is the founder's own drafting — "
            "so it is NOT edited here. He should confirm it with the ethics "
            "committee alongside the wording-near-fees question."
        ),
        "review": True,
    },
]


def allowance(fragment: str) -> dict | None:
    for entry in ALLOW:
        if re.search(entry["pattern"], fragment):
            return entry
    return None


# Text inside these tags is not visible copy.
STRIP = re.compile(
    r"<script[^>]*>.*?</script>|<style[^>]*>.*?</style>|<!--.*?-->", re.S | re.I
)
TAGS = re.compile(r"<[^>]+>")


def visible_text(markup: str) -> str:
    return html.unescape(TAGS.sub(" ", STRIP.sub(" ", markup)))


def main() -> None:
    if not DIST.exists():
        sys.exit(f"{DIST} not found — run `npm run build` first.")

    pages = sorted(DIST.rglob("*.html"))
    if not pages:
        sys.exit("No built pages found.")

    hits = 0
    reviews = 0
    for page in pages:
        text = visible_text(page.read_text(encoding="utf-8"))
        rel = page.relative_to(DIST)
        for label, pattern, why in CHECKS:
            for m in re.finditer(pattern, text):
                start = max(0, m.start() - 45)
                context = " ".join(text[start : m.end() + 45].split())
                # Match the allowance against the surrounding context, not the
                # captured group: "\d+\s*ש״ח" captures "000 ש״ח" out of
                # "100,000 ש״ח", which no sensible allowance pattern can match.
                allowed = allowance(context)
                if allowed and not allowed["review"]:
                    continue
                if allowed:
                    print(f"REVIEW  {rel}\n        [{label}] {allowed['why']}\n        …{context}…\n")
                    reviews += 1
                    continue
                print(f"FAIL  {rel}\n      [{label}] {why}\n      …{context}…\n")
                hits += 1

    print(f"scanned {len(pages)} page(s)")
    if reviews:
        print(f"{reviews} item(s) awaiting the founder's decision (not blocking).")
    if hits:
        print(f"{hits} possible violation(s) — review each before shipping.")
        sys.exit(1)
    print("No fee references, specialisation claims, comparisons or guarantees found.")
    print("Note: this checks four failure modes. The permitted list is closed —")
    print("anything genuinely novel on the site still needs a human read.")


if __name__ == "__main__":
    main()
