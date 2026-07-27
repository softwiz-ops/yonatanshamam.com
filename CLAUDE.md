# CLAUDE.md — working rules for yonatanshamam.com

Read this before touching anything. It is the operating manual; `PROJECT.md`
is the factual state of the project, and `README.md` is the technical
reference for the stack.

**This project is separate from every other one. Nothing here shares a repo,
a Cloudflare account, an email sender, or a Search Console property with
softwiz.io or anything else.** Free tiers are per-account; sharing one would
draw down the other project's quota. If you find yourself reaching into
another directory for anything but reference, stop.

---

## The one rule that matters most

**Verify against the source. Never assert what you have not checked.**

This site carries a lawyer's professional exposure. It makes binding factual
claims, it is bound by the Bar's advertising rules, and its accessibility
declaration is a legal document. Three defects found in the first hour of
looking at the current site all *looked* fine:

- The entire visible site is a second, complete HTML document pasted inside an
  Elementor widget. Two `<!DOCTYPE>`, two `<title>`, two `<body>`. Google reads
  the first one, so the hand-written title and description are discarded.
- The accessibility declaration claims `ת"י 5568 – רמה AA` and
  `WCAG 2.1 – Level AA` while relying on an overlay that independent testing
  puts at 10–16% coverage. A false factual claim on a binding page.
- A numeric range written with a typographically correct en dash (`24–48`)
  **renders reversed** in an RTL paragraph. It shows as `48–24`. Nothing errors.

A green build is not evidence. Check the rendered output, the built HTML, or
the live response.

---

## Before you finish any change

1. `npx astro check` — must be 0 errors
2. `npm run build` — must be 0 errors
3. `python3 scripts/check-contrast.py` — must exit 0
4. If the change is visible, look at it in the browser at 1440px **and** 375px,
   and run `scripts/audit-a11y.js` in the page. Measure, do not assume.
5. If it touches content or URLs, re-run the link check

---

## Content rules

- **Never invent** clients, numbers, certifications, partnerships, years of
  experience, timelines or results. Every figure must be defensible from
  something real. Anything not yet supplied is marked `[[חסר: …]]` and stays
  visible until the founder fills it.
- The `24-48 שעות` figure applies to **standard shelf documents only** — NDAs,
  demand letters, website terms. Do not attach it to a founders agreement or a
  property transaction.
- `בעברית או באנגלית` belongs to the NDA copy. It is not a site-wide claim.
- The Hebrew is the founder's voice. When he supplies wording, **correct only
  punctuation, spelling and grammar** — do not rewrite his phrasing.
- **No em dashes (—) in user-facing content.** They read as machine-written.

## The Bar's advertising rules — these define what may appear on screen

The list of what a lawyer may advertise is a **closed list**. Anything not on
it is forbidden.

- **No reference to fees anywhere on the site, in any form.** Not a price, not
  a range, not "from ₪", not a free consultation, not a discount, and **not an
  explanation of why there are no prices** — that explanation is itself a
  reference to fees, and it was caught and removed once already. Nothing in the
  structured data either: no `priceRange`, no `offers`. Run
  `python3 scripts/check-ethics.py` after every build.
  **What replaces it: transparency of scope and process** — what is included,
  the steps, the expected timeline, what the client must supply. That is the
  legally safe substitute and it is a primary module, not a footnote.
- **No comparison to other lawyers, no self-aggrandisement, no promised
  outcomes.** "The best", "leading", "#1 expert", success rates — all out.
- **The word "מומחה" is not used.** There is no formal specialisation
  certification in Israel to justify it. The safe phrasing is **`תחומי עיסוק`**,
  which is the term the rules themselves use.
- **No third-party advertising**, direct or indirect. No ad slots, no banners,
  and think hard before any third-party marketing widget. No pop-up ads.
- **No client testimonials.** Decided by the founder, 27 Jul 2026. Do not add a
  testimonials section, a review carousel, or star ratings — and do not add
  `aggregateRating` to the structured data, which is the same claim in another
  form.

## Legal content

- `/terms-privacy-accessibility/` makes binding factual claims across four
  documents. **If the site's behaviour changes, this changes with it** — adding
  analytics, a cookie, a third-party script or a new processor makes it false
  the moment it ships.
- The four anchors `#terms` `#privacy` `#accessibility` `#cookies` are load
  bearing. The footer links point at them. Do not rename them.
- The accessibility declaration must state the level achieved, the standard,
  the accessibility coordinator's name and contact, the browsers and assistive
  technology tested, the physical accessibility of the office, known
  limitations, the declaration date and the date of last test.

## Accessibility

- Build **AA at the code level**. An overlay does not satisfy regulation 35 and
  the current declaration is false because of it.
- **The preferences panel is not an overlay and must never become one.** It sets
  data attributes on `<html>` that this stylesheet honours — text size, high
  contrast, link underlines, motion off. It does not inject ARIA, does not
  rewrite the DOM, and does not scan the page. The declaration says explicitly
  that conformance rests on the code and not on the panel; do not soften that
  sentence. Pointing at a widget as the basis for conformance is the claim the
  FTC fined accessiBe a million dollars for.
- **A toolbar is not required by law.** Regulation 35 requires the site itself
  to conform and an accessibility statement to be displayed prominently. It
  says nothing about a widget. The panel is a convenience, not compliance.
- IS 5568 part 1 (September 2023) still adopts **WCAG 2.0** level AA, with
  Israeli changes. Design to WCAG 2.1 AA — it is a superset and there is no
  harm in clearing more than required.
- A sole practitioner is **not exempt**. Exemptions are by turnover, and a new
  site launched now must conform immediately.

## RTL — native, not an override layer

- `<html lang="he" dir="rtl">`, and **logical properties everywhere**:
  `margin-inline-*`, `padding-inline-*`, `inset-inline-*`, `text-align: start`.
  Never the `body.rtl` pattern.
- `flex-direction: row` flips automatically. **`row-reverse` flips twice and
  breaks.** Explicit grid column placement does not flip.
- **Bidi boundaries are where Hebrew sites actually break.** Wrap every mixed
  run in `<bdi>` or a `dir="ltr"` span: phone numbers, IDs, prices with ₪,
  dates with punctuation, English product names, URLs, emails.
  **Every numeric range must be bidi-isolated** — see the en dash defect above.
- **Flip:** directional arrows, chevrons, breadcrumb separators, progress fill.
  **Do not flip:** search, check marks, close, settings, calendar, clock,
  logos, phone numbers.
- Israeli conventions: DD/MM/YYYY, 24-hour clock.

## Typography

- Assistant, self-hosted WOFF2, split by `unicode-range`. No third-party font
  CDN on a site subject to professional confidentiality.
- **Assistant has no `tnum`,** and its `1` is 434 units against 472 for every
  other digit, so figures never align in a column. A 2.4KB digit-only subset of
  Source Sans 3 — which is what Assistant's Latin derives from, and which is
  tabular at exactly 472 — is layered over `U+0030-0039` to fix it. Do not
  remove that `@font-face` without re-checking digit alignment.
- Hebrew has no capitals, no italics and no small caps. Hierarchy comes from
  **weight, size and width only**. Load real weight files; never synthesise bold.
- Body 17px with leading in the **1.6–1.8** range, not the Latin 1.4–1.5.
  Tracking stays at 0 in body copy; negative tracking only at display sizes.

## SEO and URLs

- Slugs are **Latin, not percent-encoded Hebrew**. The primary CTA is WhatsApp,
  where a `%d7%` wall reads as a broken link.
- Every changed URL gets a 301 in `scripts/build-redirects.py`. Template junk
  that never should have been public gets a **410**, not a 301 — there is
  nowhere honest to send it.

---

## Keeping the memory current

**Update `PROJECT.md` in the same commit as the change it describes.** A stale
project file is worse than none, because it is trusted.

Record the *why*, the constraints, and anything that cost time to discover.
Do not record what the code or git history already says.
