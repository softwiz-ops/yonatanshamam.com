#!/usr/bin/env python3
"""Percent-encode the source paths in the built _redirects.

Astro writes the redirect sources exactly as they appear in redirects.json,
which for the WordPress URLs means raw UTF-8 Hebrew:

    /מכתב-התראה-מעורך-דין-מדריך-מקצועי-למי-ש/    /articles/demand-letter-guide/    301

Cloudflare matches _redirects rules against the **percent-encoded** request
path. A browser or crawler asking for that URL sends
`/%D7%9E%D7%9B%D7%AA%D7%91-...`, which never equals the raw form, so the rule
silently does nothing and the URL 404s. Verified against the live response, not
assumed: before this ran, that path returned 404 while the two ASCII redirects
in the same file returned 301.

This matters more than the other rules combined. It is the only URL moving off
WordPress that carries real ranking, and a 404 there throws it away rather than
passing it to the article that replaced it.

redirects.json deliberately keeps the readable form: it is what a person reads,
and the sitemap filter in astro.config.mjs compares against a *decoded*
pathname, so encoding at the source would quietly let redirect sources back into
the sitemap.

Runs as part of `npm run build`, so `npm run deploy` cannot ship without it.
"""

from __future__ import annotations

import sys
from pathlib import Path
from urllib.parse import quote

REDIRECTS = Path(__file__).resolve().parent.parent / "dist" / "client" / "_redirects"

# Everything legal in a path that must survive untouched. quote() already
# leaves unreserved characters alone; this keeps the separators too.
SAFE = "/-_.~!$&'()*+,;=:@%"


def main() -> None:
    if not REDIRECTS.exists():
        sys.exit(f"{REDIRECTS} not found — run `npm run build` first.")

    out: list[str] = []
    changed = 0

    for line in REDIRECTS.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            out.append(line)
            continue

        parts = line.split()
        if len(parts) < 2:
            out.append(line)
            continue

        source = parts[0]
        # Already encoded, or plain ASCII: nothing to do.
        if source.isascii():
            out.append(line)
            continue

        parts[0] = quote(source, safe=SAFE)
        changed += 1
        # Keep the columns readable; the format is whitespace-separated.
        out.append(f"{parts[0]}  {'  '.join(parts[1:])}")

    REDIRECTS.write_text("\n".join(out) + "\n", encoding="utf-8")

    if changed:
        print(f"[redirects] percent-encoded {changed} non-ASCII source path(s)")
    else:
        print("[redirects] all source paths already ASCII")


if __name__ == "__main__":
    main()
