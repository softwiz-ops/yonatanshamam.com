# Prompt for generating the site's graphic elements

Copy everything below the line into Antigravity, with this repository open.

The prompt is in English on purpose: the deliverables are SVG files, not Hebrew
copy, and coding agents follow English instructions more reliably. Nothing it
produces should contain text in any language — see the constraints.

---

You are producing a small set of original SVG graphics for a Hebrew,
right-to-left website belonging to a boutique commercial-law firm in Tel Aviv.
The site is already built (Astro, static). Your job is the graphics only — do
not touch `src/`, do not edit any `.astro` file, and do not change the design
tokens. Someone else wires them in.

## Where the files go

Create the directory `public/graphics/` and write every file there. Reference
paths on the site will be `/graphics/<name>.svg`, so use exactly these names:

```
public/graphics/
  cat-business.svg      illustration for "חברות, שותפויות ועסקים"
  cat-digital.svg       illustration for "אינטרנט, אפליקציות ופרטיות"
  cat-property.svg      illustration for "נדל״ן, עבודה וניהול שוטף"
  step-inquiry.svg      process step 1 — first contact
  step-scoping.svg      process step 2 — scoping call
  step-draft.svg        process step 3 — drafting
  step-review.svg       process step 4 — review and signature
  texture-paper.svg     a very subtle full-bleed background texture
  divider-rule.svg      a decorative section divider
```

Do not create any other files. Do not add a build step, a dependency, or a
config file.

## The palette — use these values and nothing else

```
--page          #FBFAF8   warm paper, the page background
--surface       #FFFFFF   cards sit on this
--ink           #1B1D1F   near-black, the text colour
--muted         #5B615E   secondary text
--rule          #E6E4DF   hairlines and dividers
--accent        #1A5E4A   forest green, the single accent
--accent-wash   #EDF5F1   the accent at low intensity
```

**There is one accent on this site and it is the green.** Do not introduce a
second hue, a gradient between two hues, or a "complementary" colour.

**Gold is forbidden in these graphics.** The firm's logo is a gold shield, and
gold is reserved exclusively for that mark. Measured: the logo gold sits at
1.6:1 to 2.5:1 against the page background, so it can never carry meaning. If
gold appears anywhere in your output, the file is wrong.

## Hard constraints

1. **No text of any kind in any file.** No Hebrew, no English, no numerals, no
   lettering used as decoration. Text baked into an image is invisible to
   search engines and unreadable to screen readers, and this site is held to
   WCAG AA.
2. **No directional arrows, chevrons or pointing shapes.** The document is RTL.
   Direction is handled in CSS, and a baked-in arrow points the wrong way.
3. **Nothing that reads as a flag, a scale of justice, a gavel, a courthouse
   column, or a wax seal.** The whole positioning of this site is the opposite
   of the venerable-institution cliché. Aim for restraint and structure.
4. **Decorative only.** These graphics must never be the sole carrier of
   information. Assume each will be marked `aria-hidden="true"`.
5. **Flat vector line work.** No photographs, no raster embeds, no drop
   shadows, no glows, no bevels, no 3D.
6. **No external references.** No `<image href>`, no web fonts, no filters that
   depend on anything outside the file.

## Technical requirements for every SVG

- A `viewBox` on the root element, and **no hard-coded `width`/`height`** — the
  page sizes them.
- `fill="none"` plus `stroke="currentColor"` on the line work wherever possible,
  so a single CSS `color` can retint the graphic. Where a fill is genuinely
  needed, use `currentColor` with an `opacity` rather than a second colour.
- Stroke weights consistent across the set: `1.5` for the category and step
  icons at a 48×48 viewBox.
- `stroke-linecap="round"` and `stroke-linejoin="round"` throughout.
- Optimised by hand: no editor metadata, no `<title>` unless it is meaningful,
  no empty groups, no transforms that could be baked into the path data.
- Each file under 4KB.

## What each file should be

**Category illustrations** (`cat-*.svg`, 96×96 viewBox, more detailed than an
icon but still line work):

- `cat-business` — structure and relationships between parties. Think nested
  frames, connected nodes, a document with a defined boundary. Abstract.
- `cat-digital` — a bounded interface, a shield-like enclosure around a form,
  or a layered panel. Suggest privacy and containment without a padlock cliché.
- `cat-property` — massing and plan geometry: overlapping rectangles read as
  buildings from above, a plot boundary, a floor plate. Not a house-with-a-roof
  pictogram.

**Process step icons** (`step-*.svg`, 48×48 viewBox, simpler than the above):
four marks that read as a sequence when placed in a row, without any of them
containing an arrow. Distinguish them by internal structure — an open shape, a
partially filled shape, a shape with detail added, a completed shape.

**`texture-paper.svg`** — a tiling texture at very low contrast, intended to sit
behind `--page`. It must be barely perceptible: think a faint fibre grain at
around 2–3% opacity. If it is visible as a pattern, it is too strong.

**`divider-rule.svg`** — a horizontal element to separate major sections. A
single hairline with a small interruption or thickening near its centre. Must
be symmetrical, since it will appear in an RTL layout.

## Before you finish

For each file, confirm and report:

- it opens and renders standalone in a browser,
- it contains no text nodes, no gold, and no arrow shapes,
- it recolours correctly when its parent's CSS `color` changes,
- it is under 4KB,
- it reads clearly at the size it will actually appear (96px, 48px, or full
  width for the divider) — not just when zoomed in.

Then list the nine files with their byte sizes. Do not modify anything outside
`public/graphics/`.
