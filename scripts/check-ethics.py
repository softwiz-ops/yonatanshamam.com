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


def scope_approved() -> bool:
    """Has the founder signed off the scope and timeline commitments?

    They were drafted to market norms on his instruction, but they are still
    statements about how HIS practice works — a turnaround he cannot meet is
    misleading advertising. The site must not go public until he has read them.
    """
    src = (ROOT / "src" / "data" / "services.ts").read_text(encoding="utf-8")
    return bool(re.search(r"SCOPE_APPROVED\s*=\s*true", src))


def cookies_section_accurate() -> tuple[bool, str]:
    """Does the cookies section describe what this site actually does?

    The migrated section declares Cookies, pixels, tracking technologies and
    targeted marketing. This build loads none of that — no analytics, no
    pixels, no third-party requests at all. It does now use localStorage for
    the accessibility preferences, which is first-party, functional, holds no
    personal data and is never transmitted, but the document says nothing
    about it.

    A privacy document that overstates is as wrong as one that understates, and
    under Amendment 13 the civil limitation period is seven years.
    """
    page = DIST / "terms-privacy-accessibility" / "index.html"
    if not page.exists():
        return True, ""
    text = visible_text(page.read_text(encoding="utf-8"))
    claims_pixels = "פיקסלים" in text and "שיווק ממוקד" in text
    mentions_local = "אחסון מקומי" in text or "localStorage" in text
    if claims_pixels:
        return False, (
            "the cookies section still declares pixels and targeted marketing, "
            "which this build does not use"
        )
    if not mentions_local:
        return False, (
            "the accessibility preferences are stored in localStorage and the "
            "cookies section does not mention it"
        )
    return True, ""


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

    if not scope_approved():
        print()
        print("BLOCKING  the scope and timeline commitments on the nine service")
        print("          pages were drafted to market norms and have NOT been")
        print("          approved by the founder. He must read every `scope` and")
        print("          `timeline` in src/data/services.ts, correct anything he")
        print("          cannot stand behind, then set SCOPE_APPROVED = true.")
        print("          Do not publish until then.")
        hits += 1

    ok, why = cookies_section_accurate()
    if not ok:
        print()
        print("BLOCKING  the legal document does not match the site's behaviour:")
        print(f"          {why}.")
        print("          Rewrite the Cookies section of the source document to")
        print("          describe what this build actually does — no analytics,")
        print("          no pixels, no third-party requests, and localStorage")
        print("          used only for the accessibility preferences.")
        hits += 1

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
