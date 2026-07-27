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

- **Education** — degree, institution, year. Permitted to publish and a real
  E-E-A-T signal; it was not in the LinkedIn content supplied.
- **Per service:** what is included in the engagement, what is explicitly out of
  scope, how many rounds of comments, the expected timeline, and what the client
  must bring. This is the substance of the transparency that replaces a price
  list, and it is the largest remaining hole.
- **What happens in the first meeting**, and how long it takes.
- **Physical accessibility of the office:** parking, approach, entrance, lift,
  accessible toilets, meeting rooms. Required by the regulation.
- Whether the logo is redesigned. The current one is
  `cropped-Google-Gemini-Image-Preview.png`.
- An `og:image` at 1200×630. None exists.

**Three questions for the Bar's ethics committee, in writing, before anything
is built around them:**

1. May client testimonials appear on the firm's own site, or only in ranking
   directories? The permitting clause reads "המלצות, מכתבי תודה ודירוג
   **במדריכי דירוג**", which one reading limits to directories. Until answered,
   the testimonials section stays a removable module. The safe alternative is a
   client logo wall with written consent plus a link to a Google Business
   Profile.
2. Is any wording near fees permitted at all — even "introductory call at no
   charge"? This is not hypothetical: the first build carried an explanation of
   *why* there is no pricing, and that explanation is itself a reference to
   fees. It was removed. A permitted phrasing would let the page answer an
   obvious visitor question instead of staying silent.

3. **The law practice and the technology consultancy are one registration.**
   Confirmed by the founder on 27 Jul 2026: עוסק מורשה 302910187 operates both
   `משרד עו״ד יהונתן שמם` and `SoftWiz.io`, from the same address. Both sites
   name the same registered person in their legal documents.

   That fact, not the website, is what needs checking. The Bar's rules restrict
   a lawyer from carrying on an additional occupation in a way that is
   incompatible with the profession or that channels clients from the business
   into the practice — and the whole positioning of this site rests on the two
   being connected. The site is currently built conservatively: the technology
   company appears as biography on the about page only, unlinked, with no
   partner badges, no client counts and no call to action. But conservative
   drafting does not answer the underlying question.

   Until it is answered, do not add: a link to the technology company, a shared
   contact form, any cross-selling between the two, or any wording implying the
   legal service and the technology service are bought together.

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
