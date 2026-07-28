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

## The catalogue was rebuilt from scratch — 27 Jul 2026

The founder rejected the whole content approach: "לא רוצה להציע שירותים מהירים
כמו מפעל", not business-only, and start over. He is right on all three, and the
first point also resolves the commitments problem — a promised turnaround was
the one claim nobody could approve.

**What died.** Every timeline. The scoping-then-draft process. The process rail
component. The `/how-it-works/` page. The four step icons that illustrated it.
The "חדשנות משפטית לעסקים שרצים קדימה" hero, which was business-only and
speed-led. `SHELF_TIMELINE`, `FIRST_MEETING`, and every `scope` and `timeline`
field. `scripts/check-ethics.py` now BLOCKS if any of them reappear in the
source, which is where they would come back.

**What replaced it.** Sixteen services in five families, each built around a
query someone actually types. Depth is the whole strategy: what the instrument
does, what goes wrong without it, and a "מה כדאי לשים לב אליו" section of
concrete mistakes — that last one is what a generative engine can quote.

**Positioning:** משפט בגובה העיניים. It is the only differentiator left once
price and speed are both off the table, and it is true.

## Two qualification limits that shape the catalogue

Both confirmed by the founder, and both are the kind of thing that would be an
ethics problem if guessed:

- **He is not a notary.** That needs ten years' standing; he was admitted in
  2019. So `affidavit` covers affidavits and signature witnessing, which any
  lawyer may do, and the page states plainly when a notary IS required and that
  the firm does not provide notarial services. Do not let it drift.
- **He does not hold the Accountant General's certification** for a lasting
  power of attorney (ייפוי כוח מתמשך), which only specifically trained lawyers
  may draw up. It is absent from the catalogue by decision, not oversight.

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

## The accessibility preferences panel

Asked on 27 Jul 2026 for "an accessibility widget as required by law". The
premise is wrong and the correction matters: **Regulation 35 requires the site
itself to conform to IS 5568 at level AA, and an accessibility statement to be
displayed prominently. It does not require a toolbar.** Overlays cannot satisfy
criteria that need human judgement, and the FTC's final order against accessiBe
in April 2025 was about claiming otherwise.

What was built instead is a real preferences panel: text size in three steps,
a high-contrast palette, link underlining, and motion off. It sets data
attributes on `<html>` that the site's own stylesheet honours — so nothing is
injected, nothing is overridden, and it cannot fight the user's screen reader.

Verified in the browser: body text 17px to 22px at the largest step; ink to pure
black and the page to pure white in high contrast, with the worst measured pair
on the page at 7.41:1, which is AAA rather than AA; underlines applied to links
but not to buttons; preferences persisted and cleared correctly. Keyboard: focus
lands on the trigger, all eight controls are named and tabbable, the smallest
target is 29px, and Escape closes the panel and returns focus to the trigger.

The declaration lists the panel as an adaptation and then says, in terms, that
conformance rests on the code and not on the panel. That sentence is load
bearing — it is the difference between a convenience and a false claim.

## The legal documents were re-authored, not migrated

Done 27 Jul 2026 at the founder's request. `src/content/pages/legal.md` is now
a source document under version control; `scripts/migrate-legal.py` writes the
original to `reference/legal-original.md` for comparison and must never write
to `src/` again.

**Why they had to be rewritten rather than patched.** The migrated text made
two false statements about this build: it declared Cookies, pixels, tracking
technologies and targeted marketing that do not exist here, and its
accessibility section said only that access instructions would be supplied on
request. A privacy document that overstates is as wrong as one that
understates, and Amendment 13 put the civil limitation period at seven years.

**Every factual claim was checked against the built site before it was
written**, not after:

| Checked | Result |
|---|---|
| Cookies | none, on any page |
| Third-party requests | zero — every request is same-origin |
| Fonts | self-hosted; nothing from Google Fonts |
| Analytics / pixels / tag managers | none |
| Service workers, sessionStorage, IndexedDB | none |
| localStorage | one key, `a11y-prefs`, written only if the user changes an accessibility preference |

That posture is unusually clean, and the privacy policy now says so plainly
instead of hedging.

**Research the text rests on:** Amendment 13 in force 14 Aug 2025; the Privacy
Protection Authority's final position paper on consent, 25 Feb 2026; the
section 11 notice duty; Regulation 35 and IS 5568 at level AA.

**Three things the new text deliberately does NOT claim.** The migrated
declaration asserted support for NVDA, JAWS and VoiceOver. No screen-reader
testing has been done, so that claim was removed rather than repeated — it now
reads as a gap. Firefox and Safari are likewise marked untested. And the email
processor is named as missing rather than guessed.

**One fee reference was resolved rather than flagged.** The terms said a
defective document "יתוקן ללא תשלום נוסף". The clause now reads "יתוקן בידי
המשרד" — the client protection survives, the reference to payment does not.

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

## Live — 28 Jul 2026

`https://yonatanshamam.com` and `https://www.yonatanshamam.com`, both attached
to the `yonatanshamam-site` Worker as custom domains. 30 pages, all 200.

Three things had to be true before it would deploy, and none was obvious:

- **The Worker had nowhere to land.** The adapter-generated config carries no
  routes, and `wrangler deploy` refuses to guess — it asks you to register a
  workers.dev subdomain instead. A root `wrangler.jsonc` supplies the routes and
  is merged into the generated config on every build, so it cannot drift. No
  workers.dev subdomain was registered; a law firm site does not need a second
  public URL serving the same pages.
- **Custom domains will not displace hand-made DNS.** The attach failed with
  `100117 — Hostname already has externally managed DNS records`. The two A
  records still pointed at the deleted Cloudways box, `206.81.21.82`. They had
  to be deleted by hand first; the OAuth token wrangler gets has `zone (read)`
  only, so this cannot be automated from here. MX and TXT are untouched by the
  attach — the mailbox survived it.
- **Both hostnames are attached deliberately.** www already resolved publicly,
  and a www that fails to resolve is worse than one serving the same pages under
  a canonical pointing at the apex.

**When verifying DNS from this machine, always query the authoritative server**
(`dig … @emely.ns.cloudflare.com`). The local resolver held the pre-migration
answers — the Cloudways IP and all five dead `eforward` MX records — long after
the zone was correct, which reads exactly like a catastrophic regression.

## Cloudflare answers for you when you ship no robots.txt

With none in the project, Cloudflare served a managed robots.txt. It omitted the
`Sitemap:` directive and blocked every AI crawler — GPTBot, ClaudeBot,
Google-Extended and others. Neither was a decision made here, and the second
works directly against wanting to appear in generative answers.

Shipping `public/robots.txt` fixes the Sitemap directive immediately, because
that directive is global rather than group-scoped. **It does not lift the
crawler blocks.** Cloudflare *prepends* its managed text, and a per-agent group
(`User-agent: GPTBot`) is more specific than `User-agent: *`, so the block wins
no matter what the project file says. Turning it off is a dashboard action:
**AI Crawl Control → managed robots.txt**. Done 28 Jul 2026.

The file separates two things the default conflated: `ai-input=yes` so pages can
be read and cited in an answer, `ai-train=no` so they are not absorbed as
training data. A citation sends a potential client here; a training corpus does
not. The Article 4 reservation is kept because it is the part with legal weight.

## Search Console — 28 Jul 2026

Verified as a **Domain** property (DNS TXT), which covers apex, www, http and
https in one go rather than four separate properties. The verification TXT sits
alongside the SPF record; multiple TXT records at the apex are normal, and there
is still exactly one SPF, which is the rule that matters.

Sitemap submitted: `https://yonatanshamam.com/sitemap-index.xml`, 30 URLs.
Verified that no redirect source leaks into it — the filter in
`astro.config.mjs` compares against a decoded pathname, which is why
`redirects.json` must keep its readable Hebrew form.

## The Hebrew 301 was dead on arrival, and only the live site said so

`_redirects` is matched against the **percent-encoded** request path. Astro
writes the source exactly as it appears in `redirects.json`, which for the one
URL that matters is raw UTF-8 Hebrew, so the rule could never match: every
browser and crawler encodes the path before sending it.

This was invisible everywhere except the live response. The build was clean,
preflight passed, the file was present and correctly formatted, and the two
ASCII rules beside it worked. It is also the single most costly thing on the
site to get wrong — `/מכתב-התראה…/` is the only URL moving off WordPress that
carries real ranking, and a 404 there discards it instead of passing it to the
article written to replace it.

`scripts/encode-redirects.py` runs as part of `npm run build`, so `npm run
deploy` cannot ship without it. `redirects.json` keeps the readable form on
purpose: the sitemap filter in `astro.config.mjs` compares against a *decoded*
pathname, so encoding at the source would quietly let redirect sources back into
the sitemap.

**A trap worth remembering when testing this:** `curl` sends a raw UTF-8 path
verbatim, which no browser ever does. Testing the raw form reports 404 on a
redirect that is working perfectly. Encode the path in the test, or the test
lies in both directions.

## The portrait looked smeared, and the obvious diagnoses were all wrong

The founder reported it on 28 Jul 2026. Three plausible causes were measured
and each was excluded:

- **Upscaling?** No. It renders at 230 CSS px at most (`clamp(150px, 20vw,
  230px)`), so a 2× display needs 460 physical pixels and the source has 640.
- **Bad JPEG?** No. The quantisation table starts `[4,3,3,4,…]`, which is
  roughly q95.
- **Was the source itself upscaled from something smaller?** No. Laplacian
  variance 351 and a healthy 0.22 high-to-mid frequency ratio; an upscaled
  image has almost nothing left near Nyquist. `yonatan-wide.jpg` measured 0.26,
  the same photo from the same original.

The actual cause: **the browser was resampling 640 → 460 with its own cheap
filter**, because the file sat in `public/` and was therefore handed over
untouched, at one size, in one format.

Fixed by moving it to `src/assets/` and rendering it through `<Picture>`, which
makes sharp do the resize at build time and emits AVIF and WebP at 140/230/280/
460 (and 200/400 for the about page). The 460-wide AVIF is **12KB against the
original single 64KB JPEG**, and no resampling happens in the browser at all.

**`display: contents` on the `<picture>` is load-bearing.** `<Picture>` wraps
the `<img>`, which would otherwise become the flex/grid item and leave
`flex: none` and the `clamp()` width applying to an element that no longer
controls its own track. Removing the wrapper from layout keeps every existing
rule meaning exactly what it meant before.

Measured after the change: 230×288 CSS, aspect 0.8, unchanged from before.

### display:contents was the wrong fix, and it broke the about page

The first attempt promoted the `<img>` back into the layout with
`picture { display: contents }`. **Grid and flex blockify their items**, so the
two `<source>` elements inside `<picture>` became real layout items too. On the
about page they took the first two grid tracks, pushed the portrait into the
third, and forced the facts and roles onto a second row — a large empty gap
where the founder expected content. On the home page they were two extra flex
items.

Measured, not guessed: `grid-template-rows` read `300px 516.5px` — two rows for
a one-row layout — and the `<source>` elements reported `display: block`.

The right fix is to size the `<picture>` itself (`.firm-in > picture`, and the
200px grid track on the about page) and let the `<img>` fill it with
`width: 100%`. Never reach for `display: contents` on a `<picture>` inside a
grid or flex container.

Fixed while there: below 1000px the about grid drops to two tracks with three
items, so the roles list wrapped into the 170px portrait column. It now sits
under the facts.

### The photograph is soft, and downscaling made it softer

With the pipeline correct the founder still saw it as smeared, and he was right.
The remaining softness is in the photograph — visible at native 640×800 before
any code touches it.

`scripts/build-portrait.py` resamples to the delivered width and *then* applies
an unsharp mask, in that order: sharpening the 640px original and then resizing
to 460 throws most of the benefit away, because the resample removes exactly the
frequencies the mask just raised. Parameters were chosen by measurement (the
table is in the script) — radius 0.8 / 80% / threshold 3 lifts high-frequency
energy 25% for 30% more edge overshoot, where the next step up buys 1% more
sharpness for 10% more overshoot.

`src/assets/yonatan-portrait.jpg` is therefore **generated**, 460×575.
`reference/photos/yonatan-portrait-original.jpg` is the untouched 640×800.
Re-run the script after changing the parameters or the original.

### Smaller and circular — 28 Jul 2026

Three rounds of pipeline work did not satisfy the founder, and he was right to
keep pushing: the photograph is soft and no encoder setting changes that. The
display was cut instead, on his instruction.

The portrait is now a **160px circle** on both pages, cropped to head and
shoulders. This is not only hiding the problem. Cropping means every delivered
pixel is face rather than suit, window and skyline, which raises apparent
sharpness at the same byte count — the crop is 340px of the original for a
320px master, so it is a real downscale, not an upscale.

`CROP` in `scripts/build-portrait.py` describes **this photograph only**. Swap
the original and those four numbers mean nothing; re-derive them by previewing
through the same circular mask the site applies.

`border-radius: 50%` is a true circle only because the master is square. Never
apply it to the 4:5 original.

**The ceiling is the source.** 640×800 is the largest original in the repo —
`yonatan-wide.jpg` is 1024×683, and a 4:5 crop from it would be 546 wide, i.e.
worse. Displaying the portrait any larger than 230 CSS px needs a
higher-resolution original from the founder; nothing in the pipeline can invent
detail. `yonatan-wide.jpg` was unused and has been moved to `reference/photos/`
so it is not served.

## The sticky header would have broken outside Chromium

Found while auditing the shipped CSS for the accessibility declaration, not by
looking at the page — in Chromium it looked perfect.

`.site-head` set its background **only** through `color-mix()`. A browser that
does not know the function does not approximate it; it discards the whole
declaration. The header would have had no background at all, and page text
would have scrolled straight through the navigation. Safari below 16.2 and
Firefox below 113.

Fixed by declaring the opaque colour first and the `color-mix()` second, so the
cascade keeps the fallback where the function is unknown. The two other
`color-mix()` uses — both `border-color` on tags — need no fallback, because
each inherits a visible `1px solid var(--rule)` from the rule above it. That
was checked, not assumed.

The audit found no `:dir()`, `:has()`, `@container` or `subgrid` anywhere in the
output. The one `text-wrap: balance` degrades to ordinary line breaking.

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

## The mailbox — 28 Jul 2026

`office@yonatanshamam.com` is live. Cloudflare Email Routing accepts it and
forwards to a Google mailbox. **It is receive-only** — nothing can be sent
*from* the address, so replies leave from the destination mailbox under its own
name. Deciding whether that is acceptable for a firm address is the founder's
call; making it send would mean adding a mail provider, and that provider would
have to be added to the processor list in the same change.

Getting there cost two false alarms, both worth not repeating:

- Enabling refused with **"Non-Cloudflare MX records exist"**. Five
  `eforward*.registrar-servers.com` MX records and a Namecheap SPF TXT survived
  the nameserver move. They were already dead — the service stopped the moment
  the nameservers changed — but Cloudflare will not enable routing alongside
  them. A single leftover MX at priority 10 is enough, and would also have
  outranked one of Cloudflare's own three.
- The first test message **did not arrive, then arrived ~30 minutes later**.
  Not a fault: the sender had cached "this domain has no MX" from an attempt
  made before the records existed. Negative caching here is bounded by the SOA
  minimum, 1800s. Wait it out rather than changing anything.

Verified by SMTP probe against `route3.mx.cloudflare.net` (`RCPT TO` answered
`250 2.1.0 Ok`) and by a real message delivered end to end. The dashboard
showing *Enabled* is not evidence — it showed that while mail was still
vanishing.

**The privacy policy names both legs:** Cloudflare routes, Google stores. Naming
only Cloudflare would be false, because the enquiries come to rest in a Google
mailbox and that is the processor a data subject needs to know about.

## Open — blocking or shaping work

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
