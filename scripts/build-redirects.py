#!/usr/bin/env python3
"""Generate redirects.json for the move off WordPress.

Two kinds of entry, and the difference matters:

  301  a real page that moved. The rankings and any inbound link follow it.
  410  template junk that was never meant to be public. There is nowhere
       honest to send it, and a 301 to the home page would be a soft-404 that
       Google eventually treats as one anyway. 410 tells it to drop the URL.

Nineteen of the ~22 URLs in the live sitemap are the second kind: WordPress
boilerplate, six demo pages carrying English lorem ipsum, four fabricated
testimonial pages dated 2014, and five theme footer fragments. The fabricated
testimonials are a Bar advertising exposure, not merely an SEO problem, so
they go first.

    python3 scripts/build-redirects.py
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "redirects.json"

# --- 301: real content that moved -------------------------------------------
MOVED = {
    # The four legal documents. The old slug says "privacy-policy" while the
    # document is actually terms + privacy + accessibility + cookies, and an
    # accessibility declaration buried under a privacy URL is a problem in
    # itself — the regulation expects it to be prominent and findable.
    "/privacy-policy/": "/terms-privacy-accessibility/",
    # The demand-letter post is on-topic and keeps its traffic. Its live slug is
    # cut mid-word, so it changes regardless.
    "/מכתב-התראה-מעורך-דין-מדריך-מקצועי-למי-ש/": "/articles/demand-letter-guide/",
    "/blog/": "/articles/",
}

# --- 410: never should have been public -------------------------------------
GONE = [
    "/sample-page/",
    # Theme demo pages, English lorem ipsum. One of them says "our experienced
    # attorneys" — plural, and untrue for a sole practitioner.
    "/practice-items/advisor-program/",
    "/practice-items/online-coaching/",
    "/practice-items/public-speaking/",
    "/practice-items/mentoring/",
    "/practice-items/1t1-consulting/",
    "/practice-items/training-coach/",
    # Fabricated testimonials, lastmod 2014. Advertising must not mislead.
    "/testimonials-list/testimonial-1/",
    "/testimonials-list/testimonial-2/",
    "/testimonials-list/testimonial-3/",
    "/testimonials-list/testimonial-4/",
    # Theme fragments that were never pages.
    "/section-builder/footer-1/",
    "/section-builder/footer-2/",
    "/section-builder/footer-3/",
    "/section-builder/footer-4/",
    "/section-builder/footer-5/",
    "/category/uncategorized/",
    # The National Insurance post. It cannot convert — the service is not sold —
    # and it teaches Google this is a personal injury practice, contradicting
    # the commercial-technology positioning. Decided 27 Jul 2026.
    "/התמודדות-רגשית-ובירוקרטית-מול-ביטוח-ל/",
]


def main() -> None:
    redirects: dict[str, object] = {}
    for src, dest in MOVED.items():
        redirects[src] = {"status": 301, "destination": dest}
    for src in GONE:
        redirects[src] = {"status": 410, "destination": "/"}

    OUT.write_text(
        json.dumps(redirects, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"wrote {OUT.name}: {len(MOVED)} moved (301), {len(GONE)} gone (410)")


if __name__ == "__main__":
    main()
