#!/usr/bin/env python3
"""Pre-launch check. Run against dist/ after a build.

Everything here is checked against the BUILT OUTPUT, not the source, because
the built output is what ships. A page can type-check, build cleanly, and still
link to something that does not exist.

    npm run build && python3 scripts/preflight.py

Exits non-zero if anything would be broken or missing on launch day.
"""

from __future__ import annotations

import json
import re
import sys
from html import unescape
from pathlib import Path
from urllib.parse import urldefrag, urlparse

ROOT = Path(__file__).resolve().parent.parent
DIST = ROOT / "dist" / "client"

fails: list[str] = []
warns: list[str] = []
gaps: list[str] = []


def fail(msg: str) -> None:
    fails.append(msg)


def warn(msg: str) -> None:
    warns.append(msg)


def pages() -> dict[str, str]:
    """Map of URL path -> HTML, for every built page."""
    out = {}
    for p in DIST.rglob("index.html"):
        rel = p.relative_to(DIST).parent.as_posix()
        url = "/" if rel == "." else f"/{rel}/"
        out[url] = p.read_text(encoding="utf-8")
    return out


def text_of(html: str) -> str:
    body = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", html, flags=re.S | re.I)
    return unescape(re.sub(r"<[^>]+>", " ", body))


def main() -> None:
    if not DIST.exists():
        sys.exit("dist/client not found — run `npm run build` first.")

    site = pages()
    print(f"{len(site)} page(s) built\n")

    # ---- 1. every page has the head elements that matter ------------------
    for url, html in sorted(site.items()):
        h1 = len(re.findall(r"<h1[\s>]", html))
        if h1 != 1:
            fail(f"{url}: {h1} <h1> elements (want exactly 1)")
        for label, pattern in (
            ("<title>", r"<title>[^<]{10,}</title>"),
            ("meta description", r'<meta name="description" content="[^"]{40,}"'),
            ("canonical", r'<link rel="canonical" href="https://'),
            ("og:image", r'<meta property="og:image" content="https://'),
            ("lang/dir", r'<html lang="he" dir="rtl"'),
        ):
            if not re.search(pattern, html):
                fail(f"{url}: missing or too short — {label}")

    # ---- 2. internal links all resolve ------------------------------------
    known = set(site)
    assets = {f"/{p.relative_to(DIST).as_posix()}" for p in DIST.rglob("*") if p.is_file()}
    for url, html in sorted(site.items()):
        for href in re.findall(r'href="([^"]+)"', html):
            if href.startswith(("http", "mailto:", "tel:", "#", "data:")):
                continue
            target, _ = urldefrag(href)
            if not target.startswith("/"):
                continue
            if target in known or target in assets:
                continue
            fail(f"{url}: broken internal link → {href}")

    # ---- 3. every in-page anchor target exists ----------------------------
    for url, html in sorted(site.items()):
        ids = set(re.findall(r'\sid="([^"]+)"', html))
        for href in re.findall(r'href="(#[^"]+|/[^"]*#[^"]+)"', html):
            frag = href.split("#", 1)[1]
            base = href.split("#", 1)[0] or url
            base = base if base.endswith("/") or base == "" else base
            target_html = html if base in ("", url) else site.get(base)
            if target_html is None:
                continue  # the broken-link check above already covers this
            target_ids = ids if target_html is html else set(
                re.findall(r'\sid="([^"]+)"', target_html)
            )
            if frag not in target_ids:
                fail(f"{url}: anchor → {href} has no matching id")

    # ---- 4. redirects and gone list ---------------------------------------
    redirects = json.loads((ROOT / "redirects.json").read_text(encoding="utf-8"))
    for src, cfg in redirects.items():
        dest = cfg["destination"]
        if dest not in known:
            fail(f"redirect {src} → {dest} points at a page that does not exist")
    gone = json.loads((ROOT / "gone.json").read_text(encoding="utf-8"))
    for g in gone:
        if g in known:
            fail(f"gone.json lists {g} but it is a real page")

    # ---- 5. content the founder still owes --------------------------------
    for url, html in sorted(site.items()):
        for m in re.finditer(r"\[\[חסר[^\]]*\]\]", text_of(html)):
            gaps.append(f"{url}: {m.group(0)[:70]}")

    # ---- 6. contact details are current and consistent --------------------
    firm = (ROOT / "src" / "data" / "firm.ts").read_text(encoding="utf-8")
    phone = re.search(r"display: '([^']+)'", firm).group(1)
    email = re.search(r"email: '([^']+)'", firm).group(1)
    for url, html in sorted(site.items()):
        body = text_of(html)
        for stale in ("054-244-8885", "shamam.net"):
            if stale in body:
                fail(f"{url}: stale contact detail “{stale}”")
    if "emailPending: true" in firm:
        fail(
            f"the mailbox {email} does not exist yet — it is published as the "
            "route for the statutory access and correction rights and as the "
            "accessibility coordinator's contact, and both must actually work"
        )

    # ---- 7. articles and services link both ways --------------------------
    art_dir = ROOT / "src" / "content" / "articles"
    for md in sorted(art_dir.glob("*.md")):
        slug = md.stem
        page = f"/articles/{slug}/"
        if page not in site:
            fail(f"article {slug} did not build")
            continue
        fm = md.read_text(encoding="utf-8").split("---")[1]
        svcs = re.findall(r"-?\s*([a-z-]+)", fm.split("relatedServices:")[1].split("\n")[0])
        for svc in [s for s in svcs if s]:
            svc_page = f"/practice-areas/{svc}/"
            if svc_page not in site:
                fail(f"article {slug} references a service that does not exist: {svc}")
            elif page not in site[svc_page]:
                fail(f"{svc_page} does not link back to the article {slug}")

    # ---- 8. assets referenced actually exist ------------------------------
    for url, html in sorted(site.items()):
        for src in re.findall(r'(?:src|href)="(/[^"]+\.(?:png|jpg|jpeg|svg|woff2|webp))"', html):
            if src not in assets:
                fail(f"{url}: missing asset → {src}")

    # ---- 9. sitemap covers everything -------------------------------------
    smaps = list(DIST.glob("sitemap*.xml"))
    if not smaps:
        fail("no sitemap generated")
    else:
        listed = set()
        for sm in smaps:
            for loc in re.findall(r"<loc>([^<]+)</loc>", sm.read_text(encoding="utf-8")):
                path = urlparse(loc).path
                listed.add(path)
        for url in known:
            if url not in listed and not any(url in s for s in listed):
                warn(f"{url} is not in the sitemap")

    # ---- report -----------------------------------------------------------
    for f in fails:
        print(f"FAIL     {f}")
    for w in warns:
        print(f"WARN     {w}")
    if gaps:
        print(f"\nCONTENT GAPS — visible [[חסר]] markers ({len(gaps)}):")
        for g in gaps:
            print(f"  {g}")

    print(f"\n{len(fails)} failure(s), {len(warns)} warning(s), {len(gaps)} content gap(s)")
    if fails:
        sys.exit(1)
    print("Nothing broken. Remaining gaps above are content, not code.")


if __name__ == "__main__":
    main()
