/**
 * In-page accessibility audit for the design mockups.
 *
 * Checks the things regulation 35 / IS 5568 (WCAG AA) actually turn on and
 * that a static read of the markup cannot answer: heading order, target size,
 * the keyboard focus path under RTL, computed contrast of live text, and
 * whether anything relies on a bare colour cue.
 *
 * Paste into the console, or run through the browser tooling:
 *   javascript_tool -> the contents of this file
 */
(() => {
  const problems = [];
  const note = (level, msg) => problems.push(`${level}  ${msg}`);

  /* ---------- 1.3.1 heading order ---------- */
  const heads = [...document.querySelectorAll('h1,h2,h3,h4,h5,h6')];
  const h1s = heads.filter((h) => h.tagName === 'H1');
  if (h1s.length !== 1) note('FAIL', `expected exactly one h1, found ${h1s.length}`);
  let prev = 0;
  for (const h of heads) {
    const lvl = +h.tagName[1];
    if (prev && lvl > prev + 1) {
      note('FAIL', `heading jumps h${prev} -> h${lvl}: "${h.textContent.trim().slice(0, 40)}"`);
    }
    prev = lvl;
  }

  /* ---------- 2.5.8 target size (minimum 24x24; 44x44 is the comfortable bar) ---------- */
  const targets = [...document.querySelectorAll('a[href], button, summary, input, select, textarea')];
  const small = targets
    .map((el) => ({ el, r: el.getBoundingClientRect() }))
    .filter(({ r }) => r.width > 0 && (r.width < 24 || r.height < 24));
  for (const { el, r } of small) {
    note('FAIL', `target ${Math.round(r.width)}x${Math.round(r.height)} < 24px: "${(el.textContent || el.name || '').trim().slice(0, 30)}"`);
  }
  const under44 = targets
    .map((el) => ({ el, r: el.getBoundingClientRect() }))
    .filter(({ r }) => r.width > 0 && r.height >= 24 && r.height < 44);

  /* ---------- 2.4.3 focus order follows visual order under RTL ---------- */
  // In RTL the visual reading order is right-to-left, top-to-bottom. Tab order
  // must match: within a row, decreasing x; between rows, increasing y.
  const focusable = targets.filter((el) => {
    const r = el.getBoundingClientRect();
    return r.width > 0 && r.height > 0 && el.tabIndex >= 0 && !el.closest('[hidden]');
  });
  let outOfOrder = 0;
  for (let i = 1; i < focusable.length; i++) {
    const a = focusable[i - 1].getBoundingClientRect();
    const b = focusable[i].getBoundingClientRect();
    const sameRow = Math.abs(a.top - b.top) < 12;
    if (sameRow && b.right > a.right + 2) outOfOrder++;   // moved rightward = backwards in RTL
    if (!sameRow && b.top < a.top - 12) outOfOrder++;      // moved upward
  }
  if (outOfOrder) note('WARN', `${outOfOrder} focus transition(s) move backwards against RTL reading order`);

  /* ---------- 1.4.3 computed contrast of rendered text ---------- */
  const lin = (c) => (c <= 0.04045 ? c / 12.92 : ((c + 0.055) / 1.055) ** 2.4);
  const lum = (rgb) => {
    const [r, g, b] = rgb.map((v) => lin(v / 255));
    return 0.2126 * r + 0.7152 * g + 0.0722 * b;
  };
  /**
   * Parse a computed colour to [r, g, b, a] with channels on 0-255.
   *
   * Two forms have to be handled. rgb()/rgba() give 0-255 channels. But any
   * value that went through color-mix() — which the sticky headers use for
   * their translucent background — computes to `color(srgb 0.98 0.98 0.97/0.9)`
   * with channels on 0-1. Reading those as 0-255 makes a near-white background
   * look near-black, which is how this audit first reported 1.23:1 for text
   * that actually measures 16:1.
   */
  const parse = (s) => {
    const nums = (s.match(/[\d.]+(?:e-?\d+)?/g) || []).map(Number);
    if (!nums.length) return [255, 255, 255, 1];
    const scale = /^color\(/.test(s.trim()) ? 255 : 1;
    const [r, g, b] = nums.slice(0, 3).map((v) => v * scale);
    const a = nums.length > 3 ? nums[3] : 1;
    return [r, g, b, a];
  };
  const over = (fg, bg) => fg.slice(0, 3).map((c, i) => c * fg[3] + bg[i] * (1 - fg[3]));
  const bgOf = (el) => {
    // Composite every translucent layer down to the first opaque one, rather
    // than stopping at the first non-transparent colour and ignoring its alpha.
    const layers = [];
    let n = el;
    while (n && n !== document.documentElement) {
      const c = parse(getComputedStyle(n).backgroundColor);
      if (c[3] > 0) {
        layers.push(c);
        if (c[3] === 1) break;
      }
      n = n.parentElement;
    }
    let out = [255, 255, 255];
    for (let i = layers.length - 1; i >= 0; i--) out = over(layers[i], out);
    return out;
  };
  const ratio = (a, b) => {
    const [hi, lo] = [lum(a), lum(b)].sort((x, y) => y - x);
    return (hi + 0.05) / (lo + 0.05);
  };
  const textNodes = [...document.querySelectorAll('body *')].filter((el) =>
    [...el.childNodes].some((n) => n.nodeType === 3 && n.textContent.trim())
  );
  let worst = { r: 99, el: null };
  for (const el of textNodes) {
    const cs = getComputedStyle(el);
    if (cs.visibility === 'hidden' || cs.display === 'none') continue;
    const size = parseFloat(cs.fontSize);
    const weight = +cs.fontWeight || 400;
    const large = size >= 24 || (size >= 18.66 && weight >= 700);
    const need = large ? 3 : 4.5;
    const r = ratio(parse(cs.color).slice(0, 3), bgOf(el));
    if (r < need) {
      note('FAIL', `contrast ${r.toFixed(2)}:1 < ${need} at ${size}px/${weight}: "${el.textContent.trim().slice(0, 34)}"`);
    }
    if (r < worst.r) worst = { r, el };
  }

  /* ---------- 3.3.2 / 4.1.2 names on interactive elements ---------- */
  for (const el of targets) {
    const name = (el.getAttribute('aria-label') || el.textContent || '').trim();
    if (!name && el.getBoundingClientRect().width > 0) {
      note('FAIL', `interactive ${el.tagName.toLowerCase()} has no accessible name`);
    }
  }

  /* ---------- bidi: numeric ranges must be isolated ---------- */
  const bare = [];
  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  let n;
  while ((n = walker.nextNode())) {
    if (/\d+[–—]\d+/.test(n.textContent) && !n.parentElement.closest('bdi,[dir="ltr"]')) {
      bare.push(n.textContent.trim().slice(0, 40));
    }
  }
  for (const b of bare) note('FAIL', `numeric range not bidi-isolated (renders reversed in RTL): "${b}"`);

  return {
    url: location.pathname,
    headings: heads.map((h) => h.tagName).join(' '),
    focusableCount: focusable.length,
    targetsUnder44: under44.length,
    worstContrast: `${worst.r.toFixed(2)}:1  "${worst.el?.textContent.trim().slice(0, 30)}"`,
    problems: problems.length ? problems : ['none'],
  };
})()
