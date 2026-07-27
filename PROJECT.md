# PROJECT.md — factual state of yonatanshamam.com

Last updated: 27 July 2026.

---

## What this is

A full rebuild of `yonatanshamam.com`, the site of עו״ד יהונתן שמם — a boutique
commercial and technology law firm in Tel Aviv. Moving off WordPress +
Elementor on Cloudways to a static Astro site on Cloudflare Workers.

Hebrew only, RTL native. The order of priorities the founder set is: **leads
first, positioning second, SEO third.**

**Status: direction B chosen and built.** 15 pages generate, all checks pass,
nothing is deployed. The gaps that remain are content the founder owes, not
engineering.

---

## Account separation — a hard constraint

The founder runs several unrelated projects and wants **no shared accounts
between them**. This is not tidiness; free tiers are per-account, so sharing
one would draw down another project's quota.

Everything below must be its own account, not the one used for softwiz.io:

| Thing | Status |
|---|---|
| Git repository | done — this directory, separate `git init` |
| Cloudflare account (Workers free tier: 100k req/day **per account**) | to open |
| Email provider for the contact form | to open |
| Google Search Console property | to open |
| Google Business Profile | to open — does not exist yet at all |

---

## Decisions taken, and why

**URLs are Latin, not Hebrew.** The existing Hebrew slugs percent-encode to
~230 characters of `%d7%`. Three reasons decided it: the primary CTA is
WhatsApp, where that reads as a broken link; both existing post slugs are cut
mid-word (`…למי-ש`, `…מול-ביטוח-ל` — the keyword itself truncated) so they must
change regardless; and with two posts and almost no inbound links the migration
cost is near zero now and only grows. The CTR benefit of Hebrew in the Israeli
SERP is real but smaller than the damage in the conversion channel.

**`/תהליך-העבודה/` is both a standalone page and a per-service module.** The
page is the linkable SEO asset; the module has to sit next to the conversion
point, because it is what replaces a price list and a price list is never one
click away.

**The two audiences split at the catalogue, with a single hero.** The
positioning line is the strongest asset on the page and a hero fork would
replace a statement with a menu. The three existing categories already do most
of the separating; the real-estate path gets its own service page, tone, and
conversion route (calendar rather than WhatsApp).

**Direction B, "מסלול", chosen 27 Jul 2026.** The bet: the process is the
product. Since the Bar's rules keep fees off the site entirely, transparency of
scope and process is the only substitute available, so it is the organising
system rather than a module inside one.

**Free font track.** Assistant only, self-hosted. Herzog Fox & Neeman — the
largest firm in Israel — runs Assistant from Google Fonts at 18px body, so a
carefully executed free stack meets the sector norm at zero cost.

**The National Insurance blog post comes down with a 410.** It cannot convert
because the service is not sold, and it teaches Google that this is a personal
injury practice, contradicting the commercial-technology positioning. 410 not
301 — there is nowhere honest to redirect it.

**Badge labels are all Hebrew.** The live site mixes `Essential` / `Must Have`
with `פופולרי` / `חובה חוקית` / `דחוף`. Latin badge words inside a Hebrew RTL
card grid create bidi boundary noise for no benefit. Mapped to:
`בסיס`, `פופולרי`, `נדרש`, `חובה חוקית`, `דחוף`.

---

## The line drawn through the service content

The founder asked for the service pages to be filled in from whatever ranks,
using the firms in the top results. That works for one half of the content and
not the other, and the split is enforced in `src/data/services.ts`:

- **What the legal instrument is and what it regulates** — what a founders
  agreement covers, what the Companies Registrar requires, what Regulation 35
  demands. General legal knowledge. Accurate, defensible, and it is what
  actually ranks. Written.
- **What this firm commits to** — how many revision rounds, how long a draft
  takes, what falls outside the engagement. Factual claims about this practice.
  Only the founder can make them, and advertising by a lawyer must not mislead.
  Copying a competitor's "up to 3 revision rounds" would invent an obligation he
  never agreed to. These render as visible `[[חסר]]` markers.

## Settled

**No client testimonials.** Decided 27 Jul 2026: the founder does not want them
at this stage. That closes the question of whether the permitting clause covers
a firm's own site or only ranking directories — it does not need asking. No
testimonials module was ever built, so nothing was removed.

What carries trust on this site instead: the previous legal positions, the
admission date and degree, the named accessibility coordinator, a real Tel Aviv
address, the substantive service content, and a visible LinkedIn profile. Worth
noting that referral is still the dominant channel in Israeli commercial law —
the site's job is to confirm a referral, not to build trust cold.

**Nothing on this site refers to fees, in any form.** Decided 27 Jul 2026:
"אל תרשום פשוט דברים שנוגעים לשכ״ט". So the second committee question is closed
too — the answer is to write nothing, rather than to find out what phrasing
would be permitted.

This is stronger than it first sounds and it is easy to breach by accident. It
rules out not only prices, but a note explaining why there are none, "no
obligation", "at no charge", a free first call, and any structured-data
`priceRange` or `offers`. `scripts/check-ethics.py` scans the built HTML for
all of it.

The single remaining fee reference on the site is inside the migrated terms of
service — a defective document "יתוקן ללא תשלום נוסף". That is the founder's own
drafting in a binding document rather than advertising copy, and removing it
would strip a client protection, so it has not been touched. The checker reports
it as REVIEW on every run.

**One registration, two unconnected activities.** עוסק מורשה 302910187 operates
both `משרד עו״ד יהונתן שמם` and the technology consultancy, from the same
address. Asked whether that raises an additional-occupation question under the
Bar's rules, the founder — a lawyer, ruling on his own practice — confirmed on
27 Jul 2026 that there is no issue and that the two services and activities are
unconnected. Closed.

**What that changed in the build.** An earlier draft of the about page called
the combination "נקודת המוצא של המשרד ולא נספח לה". That asserts a link between
the two services which, on the founder's own account, does not exist — and an
inaccurate claim on a lawyer's site is an exposure rather than a copy nit. The
paragraph was rewritten to describe a background that informs how he works,
which is biography. The rule that follows from it:

> Nothing on this site may present the legal service and the technology service
> as a combined offering. No link to the technology company, no shared contact
> form, no cross-selling, no wording implying the two are bought together.

## The logo, and why it is a mark and not an accent

The founder supplied a gold shield monogram plus a full lockup. Measured against
the page background: **the logo gold is 1.6:1 to 2.5:1**, and reaching the 4.5:1
that text needs requires darkening it 36% in lightness, which lands on
`#80681e` — olive, with the gold gone entirely.

So gold cannot be an accent. WCAG exempts logotypes from contrast requirements,
so the mark is fine as a mark; the single interactive accent stays green. Gold
must never be borrowed for text, icons or controls.

Note also that the brief explicitly ruled out the dark-gold "venerable
institution" idiom for this site. Keeping the gold confined to the mark is what
lets the logo coexist with that positioning instead of overriding it.

Only the two 677×369 preview PNGs have real transparency; the 2816px masters are
flat on cream and cannot be keyed cleanly, since the shield is line art with
light highlights inside it. The build script uses the preview for the mark and
the high-res lockup for the share card, where a background is wanted anyway.

## Identity facts, and where they came from

Supplied by the founder or taken from the LinkedIn profile he provided:

| Fact | Value |
|---|---|
| Address | מגדלי אלון, יגאל אלון 94, תל אביב |
| Hours | ראשון–חמישי, 09:00–19:00 |
| Admitted | 2019 |
| Languages | עברית, אנגלית |
| Previous legal roles | גולדפרב זליגמן (2019–2022); מתמחה, ש. הררי (2018–2019) |
| Licence number | not required — the founder's decision |
| Education | still missing |

**The address on the live site is wrong.** It says מגדלי הארבעה; the move to
Alon Towers is documented on the founder's own LinkedIn. Corrected here.

**What was deliberately left off the about page**, though it is all on the
LinkedIn profile: partner tier badges ("Elite Circle Platinum"), client counts
("dozens of SMBs"), and self-praise ("we punch above our weight"). The first
would be advertising for another business on a lawyer's site, which the rules
forbid outright. The technology company and the legal-tech venture appear as
biography — they are the entire basis of the positioning — but unlinked and
without promotional framing.

## The fee-explanation problem

The first build carried lines like "אין באתר מחירון — כללי לשכת עורכי הדין
אוסרים על פרסום שכר טרחה". `scripts/check-ethics.py` flagged them, correctly:
the permitted free text is defined as text "שאינו כולל כל התייחסות לשכר הטרחה",
and an explanation of why fees are absent is itself a reference to fees.

All of them were removed. The pages now state what is there and explain nothing.
Whether any wording near fees is permitted at all is one of the two questions
open with the ethics committee.

One instance remains and was **not** edited: the migrated terms of service says
a defective document "יתוקן ללא תשלום נוסף". It sits in a binding legal document
rather than in advertising copy, and it is the founder's own drafting. The
checker reports it as REVIEW on every run.

## Defects in the live site, verified against the response

- **The home page and `/privacy-policy/` each contain two nested HTML
  documents.** Verified: 2× `<!DOCTYPE`, 2× `<title>`, 2× `<body>` on the
  privacy page, with the second document starting at byte 39895. The visible
  site was pasted whole into an Elementor HTML widget. Google reads the first
  document, so the hand-written title and description are discarded and it
  shows `Home - Adv. Yonatan Shamam` with an auto-generated description.
- **The H1 reads `חדשנות משפטיתלעסקים שרצים קדימה`** — a missing space where a
  `<br>` was lost. Crawlers read `משפטיתלעסקים` as one word.
- **Every blog post and testimonial page has `מאמרים משפטיים` as its H1**
  instead of its own title. One template bug across all posts.
- **An empty `בקרוב` H2 is publicly visible** on the home page.
- **The accessibility overlay injects an English H2 and ~17 English H3s** into
  the bottom of every page. Every page has more English headings than Hebrew.
- 19 of ~22 sitemap URLs are junk actively served to Google: `/sample-page/`
  (WordPress boilerplate), 6 `/practice-items/…` demo pages with **English
  lorem ipsum**, 4 `/testimonials-list/…` **fabricated testimonials** with
  `lastmod` 2014, 5 `/section-builder/footer-*/` fragments, and
  `/category/uncategorized/`. The fabricated testimonials are a Bar
  advertising exposure, not just an SEO problem.
- `og:type` is `article` on the home page; `og:image` is 197×246 against a
  1200×630 minimum.
- Schema is the AIOSEO default only. No `Attorney`, no `LegalService`, no
  `LocalBusiness`, no `FAQPage` — despite five real Q&As sitting in the markup.
  `Organization` carries only name, description, url, logo.
- Cache headers contradict: `max-age=0, s-maxage=2592000` with an `expires`
  in the past relative to `date`. `max-age=0` defeats browser caching on a
  264KB page.

## What was worth keeping

**The legal document.** ~1,485 words of real Hebrew legal drafting, updated
February 2026, already carrying the Amendment 13 changes. Not boilerplate.
Migrated to `src/content/pages/legal.md` by `scripts/migrate-legal.py`, with
all four anchors preserved.

Two things about it that must be fixed in the rebuild:

1. **All four footer links point at the top of the page** rather than at the
   matching anchor. The anchors exist. One-line fix.
2. **The slug and title are English** (`privacy-policy` / `Privacy Policy`)
   while the content is `תנאי שימוש, פרטיות ונגישות`. An accessibility
   declaration buried under a privacy-policy URL is a problem in itself — the
   regulation expects it to be prominent and findable.

**Two false statements found inside it**, both of which the rebuild changes:

- It claims `ת"י 5568 – רמה AA` and `WCAG 2.1 – Level AA`. Today that rests on
  an overlay. Building AA in code makes the claim true.
- The cookies section declares pixels and targeted marketing. If the new site
  ships with no analytics and no pixels, that statement is false in the other
  direction and must be rewritten to match actual behaviour.

**Facts recovered from it** that the brief had marked as missing: the
accessibility coordinator is עו״ד יהונתן שמם, and the stated response time for
accessibility enquiries is 5 business days.

---

## Typography — measured, not assumed

Assistant, self-hosted, three subsets totalling **31.7KB**:

| File | Size | Range |
|---|---|---|
| `assistant-hebrew.woff2` | 7.3KB | Hebrew |
| `assistant-latin.woff2` | 22KB | Latin |
| `digits-tabular.woff2` | 2.4KB | `U+0030-0039` |

Verified in the binaries with fontTools:

- Assistant is variable `wght` **200–800**. Its feature list is
  `kern, mark, mkmk` only — **no `tnum`, no `lnum`.**
- Its digit advances are 472 for every digit **except `1`, which is 434**. So
  figures never line up in a column.
- Source Sans 3 — the family Assistant's Latin derives from — has all ten
  digits at **472**, tabular by default, same 1000 UPM, ascender 1024 vs 1021.
  A digit-only subset of it is layered over `U+0030-0039`.
- Confirmed in the browser: all ten digits render at an identical 49.7px.

## Colour — every pair measured

`scripts/check-contrast.py` holds both palettes and exits non-zero on any
failure. Two findings worth keeping:

- **`--rule` and `--line-control` are separate tokens on purpose.** WCAG 1.4.11
  applies to borders that identify a *control*; a hairline dividing two
  sections is decoration and is exempt. Holding a section divider to 3:1 would
  force a grey dark enough to read as a table border and would wreck the
  restraint the design depends on.
- **`--faint` was originally scoped to display sizes at 3:1, then used for
  12–13px legal fine print** — including the "this is not legal advice" line.
  It measured 4.43:1. Both palettes' faint tokens were darkened to clear 4.5:1
  on both surfaces, so the token is safe wherever it is used.

## The en dash defect — the one that would have shipped silently

A numeric range written with a typographically correct en dash renders
**reversed** in an RTL paragraph. Measured in the browser by reading back the
visual order of the glyph runs:

| Source | Renders as |
|---|---|
| `24–48` (en dash, U+2013) | **`48–24`** |
| `24-48` (hyphen-minus, U+002D) | `24-48` |
| `24–48` inside `<bdi dir="ltr">` | `24–48` |

U+2013 is bidi class Other Neutral, so between two numbers in an RTL paragraph
it separates them instead of joining them and the two runs lay out
right-to-left. U+002D is a European Separator and joins them.

The live site is correct only by accident, because it uses a hyphen. An editor
"improving" the typography would have flipped every range on the site with no
error anywhere. **Every numeric range is bidi-isolated regardless of which
dash is used.**

---

## Open — blocking or shaping work

**Content the founder must supply.** All of it renders as a visible
`[[חסר: …]]` marker on the built pages:

- **Sign off the scope and timelines.** They were drafted to market norms on the
  founder's instruction of 27 Jul 2026 and are NOT approved. He must read every
  `scope` and `timeline` in `src/data/services.ts`, correct anything he cannot
  stand behind, and set `SCOPE_APPROVED = true`. `scripts/check-ethics.py`
  blocks while it is false. A turnaround he cannot meet is misleading
  advertising, which is exactly what the rules forbid.
- **Entrance and lift accessibility.** He supplied parking (none), approach,
  toilets and meeting rooms; these two were not stated and render as gaps in the
  declaration. Also worth confirming whether the building has accessible parking
  even if the office does not — the distinction matters in the declaration.

Supplied since:

- Education: הקריה האקדמית אונו, 2018. Stated as LL.B, which is an entailment of
  admission rather than a guess — correct it if he holds something else.
- Physical accessibility, in part (above).
- Logo masters, in `brand-assets/`. `scripts/build-brand-assets.py` derives the
  header mark, favicons and a 1200×630 share card from them.
- `og:image` now exists at 1200×630, 54KB.

*(Both questions that stood open for the ethics committee were closed by the
founder on 27 Jul 2026 — see "Settled".)*

**Privacy — the contact form design depends on this.** Under Amendment 13, a
database holding **only name, address and contact details** for ≤100,000 people
is not a database and is exempt from the whole regime. **The moment a "tell me
what this is about" field is added, that relief disappears** — and because
lawyer-client confidentiality is a statutory duty, enquiry data is arguably
"information of special sensitivity", which doubles the penalties. Both form
variants need to be put to the founder before the form is built.

**Analytics.** Whether to run GA4 at all. It determines whether the cookies
section of the legal document is rewritten to say "none" or kept. No Israeli
law requires a cookie banner; the binding constraint is the Authority's final
opinion on consent (25 February 2026), which requires recipients to be named
with concrete specificity and active opt-in for any non-service profiling or
direct marketing.

**Not required for this firm:** database registration, notification to the
Authority, a privacy officer, an information security officer, or a cookie
banner as such.
