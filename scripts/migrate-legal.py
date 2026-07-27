#!/usr/bin/env python3
"""Pull the legal document off the live WordPress site and write it as Markdown.

This is the one piece of content on yonatanshamam.com worth migrating rather
than rewriting: ~1,750 words of real Hebrew legal drafting, updated February
2026, already carrying the Amendment 13 changes to the Privacy Protection Law.

The page it lives on is broken in a specific way that shapes this script. The
whole visible document was pasted as a *complete HTML document* inside an
Elementor HTML widget, so the response contains two nested documents:

    byte     0  <!DOCTYPE html> ... the real WordPress page
    byte 39895  <!DOCTYPE html> ... the pasted document, which holds the content

Google reads the first one, which is why the hand-written title and description
are thrown away. We want the second. The split point is found by locating the
second DOCTYPE rather than hard-coding the offset, since the wrapper's weight
changes whenever a plugin updates.

Re-runnable. Writes to reference/legal-original.md for comparison only — the
live documents are authored in src/content/pages/legal.md and are NOT generated.

    python3 scripts/migrate-legal.py
"""

from __future__ import annotations

import html
import re
import sys
import urllib.request
from pathlib import Path

SOURCE = "https://yonatanshamam.com/privacy-policy/"
ROOT = Path(__file__).resolve().parent.parent
CACHE = ROOT / "reference" / "scrape" / "privacy.html"
# Writes to reference/, NOT to src/. The legal documents were re-authored on
# 27 Jul 2026 to match what this build actually does — the migrated text
# declared pixels and tracking the site does not use, and its accessibility
# section was thinner than Regulation 35 expects. src/content/pages/legal.md is
# now a source document under version control. This script exists to reproduce
# the ORIGINAL for comparison, and must never overwrite the authored version.
OUT = ROOT / "reference" / "legal-original.md"

# The four sections, keyed by the anchor id the live page already uses. These
# anchors are kept verbatim in the rebuild: the footer links point at them, and
# any inbound link that ever worked pointed at them too.
SECTIONS = ["terms", "privacy", "accessibility", "cookies"]


def fetch() -> str:
    """Return the raw page, from cache if it is already there."""
    if CACHE.exists():
        return CACHE.read_text(encoding="utf-8")
    req = urllib.request.Request(SOURCE, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        body = resp.read().decode("utf-8")
    CACHE.parent.mkdir(parents=True, exist_ok=True)
    CACHE.write_text(body, encoding="utf-8")
    return body


def inner_document(page: str) -> str:
    """Slice out the pasted document — everything from the second DOCTYPE on."""
    doctypes = [m.start() for m in re.finditer(r"<!DOCTYPE", page, re.I)]
    if len(doctypes) < 2:
        sys.exit(
            "Expected two nested documents and found "
            f"{len(doctypes)}. The live page has changed shape; re-read it "
            "before trusting this script."
        )
    inner = page[doctypes[1] :]
    end = inner.find("</html>")
    return inner[: end + len("</html>")] if end != -1 else inner


def text_of(fragment: str) -> str:
    """Flatten an HTML fragment to Markdown-ish inline text."""
    out = fragment
    out = re.sub(r"<br\s*/?>", "\n", out, flags=re.I)
    out = re.sub(r"<strong[^>]*>(.*?)</strong>", r"**\1**", out, flags=re.S | re.I)
    out = re.sub(r"<b[^>]*>(.*?)</b>", r"**\1**", out, flags=re.S | re.I)
    out = re.sub(r"<em[^>]*>(.*?)</em>", r"*\1*", out, flags=re.S | re.I)
    out = re.sub(
        r'<a[^>]*href="([^"]*)"[^>]*>(.*?)</a>', r"[\2](\1)", out, flags=re.S | re.I
    )
    out = re.sub(r"<[^>]+>", "", out)
    out = html.unescape(out)
    # Collapse the newlines the source's pretty-printing leaves behind, but keep
    # the ones <br> produced.
    out = re.sub(r"[ \t]+", " ", out)
    out = re.sub(r" *\n *", "\n", out)
    return out.strip()


def convert_section(fragment: str) -> list[str]:
    """Walk one <section> in document order and emit Markdown blocks."""
    lines: list[str] = []
    # badge-row and contact-bar are div-only constructs that carry legally
    # required content: the conformance level claimed, and the accessibility
    # coordinator's name and contact details. Regulation 35 requires both, so
    # they cannot be treated as decoration and skipped.
    pattern = re.compile(
        r'<h2[^>]*class="section-title"[^>]*>(?P<h2>.*?)</h2>'
        r'|<div[^>]*class="subsection-title"[^>]*>(?P<h3>.*?)</div>'
        r'|<div[^>]*class="badge-row"[^>]*>(?P<badges>.*?)</div>\s*</div>'
        # Counting closing divs to find the end of contact-bar silently drops
        # its last field. Run to the next subsection or the end of the section
        # instead and let the label/value pair regex do the selecting.
        r'|<div[^>]*class="contact-bar"[^>]*>(?P<contact>.*?)'
        # \Z matters: convert_section is handed the *inside* of the section, so
        # the closing </section> has already been consumed as the delimiter and
        # a contact-bar that ends the section has nothing else to anchor on.
        r'(?=<div[^>]*class="subsection-title"|</section>|\Z)'
        r"|<p[^>]*>(?P<p>.*?)</p>"
        r"|<ul[^>]*>(?P<ul>.*?)</ul>"
        r"|<ol[^>]*>(?P<ol>.*?)</ol>",
        re.S | re.I,
    )
    for m in pattern.finditer(fragment):
        if m.group("h2") is not None:
            lines.append(f"## {text_of(m.group('h2'))}")
        elif m.group("h3") is not None:
            lines.append(f"### {text_of(m.group('h3'))}")
        elif m.group("p") is not None:
            body = text_of(m.group("p"))
            if body:
                lines.append(body)
        elif m.group("badges") is not None:
            badges = re.findall(r"<span[^>]*>(.*?)</span>", m.group("badges"), re.S | re.I)
            block = [f"- {text_of(b).lstrip('✓ ')}" for b in badges if text_of(b)]
            if block:
                lines.append("\n".join(block))
        elif m.group("contact") is not None:
            raw = m.group("contact")
            pairs = re.findall(
                r'<div[^>]*class="label"[^>]*>(.*?)</div>\s*'
                r'<div[^>]*class="value"[^>]*>(.*?)</div>',
                raw,
                re.S | re.I,
            )
            block = [
                f"- **{text_of(k)}:** {text_of(v)}"
                for k, v in pairs
                if text_of(k) and text_of(v)
            ]
            if block:
                lines.append("\n".join(block))
        elif m.group("ul") is not None or m.group("ol") is not None:
            raw = m.group("ul") or m.group("ol")
            ordered = m.group("ol") is not None
            items = re.findall(r"<li[^>]*>(.*?)</li>", raw, re.S | re.I)
            block = []
            for i, item in enumerate(items, 1):
                body = text_of(item)
                if not body:
                    continue
                marker = f"{i}." if ordered else "-"
                block.append(f"{marker} {body}")
            if block:
                lines.append("\n".join(block))
    return lines


def main() -> None:
    inner = inner_document(fetch())

    title_m = re.search(r"<h1[^>]*>(.*?)</h1>", inner, re.S | re.I)
    title = text_of(title_m.group(1)) if title_m else "תנאי שימוש, פרטיות ונגישות"

    pill = re.search(r'<div[^>]*class="update-pill"[^>]*>(.*?)</div>', inner, re.S | re.I)
    updated = text_of(pill.group(1)) if pill else ""

    blocks: list[str] = []
    found: list[str] = []
    for anchor in SECTIONS:
        m = re.search(
            rf'<section[^>]*id="{anchor}"[^>]*>(.*?)</section>', inner, re.S | re.I
        )
        if not m:
            print(f"  ! section #{anchor} not found", file=sys.stderr)
            continue
        found.append(anchor)
        # The anchor is carried into the Markdown so the footer links keep
        # working. Astro's Markdown renderer will not invent these ids: the
        # headings are Hebrew, and slugifying Hebrew gives percent-encoded
        # nonsense that no link can be written against.
        blocks.append(f'<span id="{anchor}"></span>')
        blocks.extend(convert_section(m.group(1)))

    if len(found) != len(SECTIONS):
        sys.exit(f"Expected {len(SECTIONS)} sections, extracted {len(found)}: {found}")

    # Quote every value. The "updated" line contains ": " inside its text
    # ("עודכן לאחרונה: פברואר 2026"), which an unquoted YAML scalar parses as a
    # mapping and the frontmatter then fails to load.
    def q(v: str) -> str:
        return '"' + v.replace('"', '\\"') + '"'

    front = [
        "---",
        f"title: {q(title)}",
        "description: " + q(
            "תנאי השימוש, מדיניות הפרטיות, הצהרת הנגישות ומדיניות ה-Cookies "
            "של משרד עו״ד יהונתן שמם."
        ),
        # The live URL, so build-redirects.py can emit the 301. The new path is
        # Hebrew-free and describes all four documents, not just privacy.
        "legacyPath: " + q("/privacy-policy/"),
        f"updated: {q(updated)}" if updated else "",
        "---",
        "",
    ]
    body = "\n\n".join(b for b in blocks if b)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(l for l in front if l != "") + "\n" + body + "\n", encoding="utf-8")

    words = len(body.split())
    print(f"wrote {OUT.relative_to(ROOT)} — {len(found)} sections, ~{words} words")


if __name__ == "__main__":
    main()
