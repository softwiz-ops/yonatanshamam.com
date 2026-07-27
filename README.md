# yonatanshamam.com

Rebuild of the site of עו״ד יהונתן שמם — replacing WordPress + Elementor on
Cloudways with a static Astro site on Cloudflare Workers. Hebrew only, RTL
native.

> **Start here:** [`CLAUDE.md`](CLAUDE.md) is the operating manual (verification
> discipline, the Bar's advertising rules, RTL rules, URL constraints).
> [`PROJECT.md`](PROJECT.md) is the current factual state. This README covers
> the stack.
>
> **This project shares no accounts with any other.** Separate Cloudflare
> account, separate email sender, separate Search Console property. Free tiers
> are per-account.

## Running it

```bash
npm install
npm run dev      # http://localhost:4321
npm run build
npm run check
```

## Checks that must pass before any change lands

```bash
npx astro check && npm run build && python3 scripts/check-contrast.py
```

`scripts/audit-a11y.js` is pasted into the browser console (or run through the
browser tooling) on any page that changed visually. It checks heading order,
target size, the keyboard focus path under RTL, computed contrast of rendered
text, accessible names, and that every numeric range is bidi-isolated.

## Layout

```
src/
  content/pages/   migrated Markdown (the legal document)
  ...              views, copy and components land here once a direction is chosen
design/            the two design directions, as standalone HTML
  tokens-a.css     direction A — "לוח"
  tokens-b.css     direction B — "מסלול"
  {a,b}-home.html
  {a,b}-service.html
public/fonts/      self-hosted Assistant subsets + tabular digits
scripts/           migration and audit tooling — not part of the build
reference/         the design brief and a scraped copy of the live site
```

## Fonts

Self-hosted, 31.7KB total, split by `unicode-range`:

| File | Size | Covers |
|---|---|---|
| `assistant-hebrew.woff2` | 7.3KB | Hebrew |
| `assistant-latin.woff2` | 22KB | Latin |
| `digits-tabular.woff2` | 2.4KB | `U+0030-0039` |

The third file is not optional. Assistant has no `tnum` and its `1` is 434
units against 472 for every other digit, so figures never line up. The subset
is Source Sans 3 — the family Assistant's Latin derives from — which is tabular
at exactly 472 with the same 1000 UPM. Declared last so it wins the cascade.

To refresh them, re-download from Google Fonts and re-subset:

```bash
python3 -m fontTools.subset ss3.woff2 --unicodes="U+0030-0039" --flavor=woff2 --output-file=public/fonts/digits-tabular.woff2 --layout-features='' --no-hinting --desubroutinize
```

## Migration from WordPress

```bash
python3 scripts/migrate-legal.py     # the legal document -> src/content/pages/legal.md
python3 scripts/build-redirects.py   # regenerate redirects.json
```

`migrate-legal.py` overwrites; hand-edits to the generated Markdown are lost.
It has to slice the *second* of two nested HTML documents out of the response —
see the comment at the top of the file for why the live page is shaped that way.

### Redirects

21 entries: 3 × 301 for content that moved, 18 × 410 for template junk that was
never meant to be public. 410 rather than 301 on the junk because there is
nowhere honest to send it, and a redirect to the home page is a soft-404.

## Deploy

Not yet configured. `npm run deploy` points wrangler at the generated
`dist/server/wrangler.json`; the Cloudflare account has to be created first, and
it must be a new one, not shared with any other project.
