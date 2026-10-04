/**
 * resolutionwords.cjs -- DSGN_AMGTV1 round 30, AV-zh-1 ONE UNIVERSE PER FACE (cell-slug universe; issuer 2.0.0_SA_COO~D): THE LEAD
 * PANEL PRINTS NO MOVEMENT-BASIS SYSTEM WORDS.
 *
 * Usage (from the directory whose portal/ is the checkout under test, e.g. C:/tmp/wk-dsgn-amgtv1-82): node <this file>
 * Grades: PRD v0.13 FWD-27 (:407, DONE WHEN "0 strings from the register's system-wording list"), on CTO msg 28833 from CVO~Z v33:
 *   the line "Showing the {axis} list (movement is measured)." (LeadPanel.tsx:220, ResolutionNote's CROSSED branch; quoted by
 *   SAUX-21 at PRD :546 as "Showing the Trending x Price list (movement is measured)") is system wording and must not render --
 *   replaced by reader words or dropped; the Price face's served window caption (data-price-window, round 29) already names the
 *   window. The issuer's arm: the string, or any "(movement is measured)" / "list (" system phrasing, is absent on both faces.
 * THE CONTRACT (the worker face quotes it): on the Price face and the Chatter face, the visible text and every title attribute of
 *   the REAL LeadPanel carry none of:
 *     - "Showing the <words> list" (the CROSSED sentence, with or without its parenthesis);
 *     - "(movement is measured)" or "(movement is not yet measured)";
 *     - "list (" (a list name followed by a parenthesised system note);
 *   on the served price payload (resolution CROSSED) AND on a planted SUBJECT_ONLY_FALLBACK resolution (ResolutionNote's other
 *   branch, whose sentence ends "... list (movement is not yet measured)."). data-* attributes may keep the machine values
 *   (data-resolution, data-served-axis). The Price face keeps its one data-price-window caption.
 * Render: ./_universe.cjs (the REAL LeadPanel.tsx over the REAL hooks/useLeadPanelApi.ts, the real PriceBars, served fixtures).
 * Inputs: round30/fixtures/windows.price.30.json (served, resolution CROSSED); its copy with the resolution block replaced by
 *   round30/fixtures/universe/universe.planted.json `price_resolution_fallback`; windows.chatter.30.json (the Chatter face).
 * Arms:
 *   1  NO SYSTEM WORDS: 0 matches of the three phrasings on Price (served CROSSED), Price (planted FALLBACK), Chatter (All names).
 *   2  CONTROL (passes at base by design): the Price face renders exactly one data-price-window caption of at least three words.
 *   3  PLANTED: the phrase predicate rejects the base CROSSED sentence, the base FALLBACK sentence, the CROSSED sentence without
 *      its parenthesis, a bare "(movement is measured)" and "the Price list (as served)", and accepts three reader sentences and
 *      a markup whose only resolution trace is a data-* attribute.
 * Blind spots: wording is read as text, not meaning -- a new system phrase in other words is the person's read of the PNG; the
 *   Chatter face is read on All names only.
 * Prints one line per arm and "THE LEAD PANEL PRINTS NO MOVEMENT-BASIS SYSTEM WORDS: <k> of 3 arms"; exit 0 only at 3 of 3.
 * Writes no file. No network, no AWS. Seconds.
 */
const U = require('./_universe.cjs');

const T0 = Date.now();
const unesc = (s) => String(s).replace(/&quot;/g, '"').replace(/&#x27;/g, "'").replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&amp;/g, '&');
const textOf = (html) => unesc(String(html).replace(/<[^>]*>/g, ' ')).replace(/\s+/g, ' ').trim();
const titlesOf = (html) => [...String(html).matchAll(/\stitle="([^"]*)"/g)].map((m) => unesc(m[1]));

const PHRASES = [
  ['CROSSED-SENTENCE', /\bShowing the [A-Za-z][A-Za-z ]{0,60}? list\b/i],
  ['MOVEMENT-BASIS', /\(\s*movement is (?:not yet )?measured\s*\)/i],
  ['LIST-PAREN', /\blist \(/i],
];
/** Faults of a reader-visible string: one per phrasing matched, quoting the match. */
function phraseFaults(text) {
  const f = [];
  for (const [cls, re] of PHRASES) { const m = re.exec(text); if (m) f.push(`${cls}: "${m[0]}"`); }
  return f;
}
const visible = (html) => [textOf(html), ...titlesOf(html)].join(' | ');

const arms = [];
// ---------------- arm 1: no system words on either face ----------------
{
  const f = [];
  const tally = [];
  const cases = [
    ['Price (served CROSSED)', 'PRICE', { price: U.PRICE }],
    ['Price (planted FALLBACK)', 'PRICE', { price: U.PRICE_FALLBACK }],
    ['Chatter', 'CHATTER', {}],
  ];
  for (const [n, face, opt] of cases) {
    try {
      const r = U.renderFace(face, false, opt);
      const fx = phraseFaults(visible(r.html));
      f.push(...fx.map((x) => `${n}: ${x}`));
      tally.push(`${n} ${fx.length}`);
    } catch (e) { f.push(`${n}: RENDER: ${String(e.message).split('\n')[0]}`); }
  }
  arms.push(['NO SYSTEM WORDS: no "Showing the <words> list", "(movement is measured)" or "list (" on Price (served, planted fallback) or Chatter',
    f.length === 0, f.length === 0 ? `matches per face: ${tally.join('; ')}` : f.slice(0, 5).join(' | ')]);
}
// ---------------- arm 2: control -- the window caption stays ----------------
{
  const f = [];
  let d = '';
  try {
    const r = U.renderFace('PRICE', false, { price: U.PRICE });
    const caps = [...r.html.matchAll(/<([a-zA-Z0-9]+)\b[^>]*\sdata-price-window="[^"]*"[^>]*>([\s\S]*?)<\/\1>/g)].map((m) => textOf(m[2]));
    if (caps.length !== 1) f.push(`${caps.length} element(s) carry data-price-window, want 1`);
    else if (caps[0].split(/\s+/).filter((w) => /[A-Za-z]/.test(w)).length < 3) f.push(`the window caption is under three words ("${caps[0]}")`);
    d = caps.length ? `"${caps[0]}"` : 'none';
  } catch (e) { f.push('RENDER: ' + String(e.message).split('\n')[0]); }
  arms.push(['CONTROL (passes at base by design): the Price face keeps one data-price-window caption in words',
    f.length === 0, f.length === 0 ? d : f.join(' | ')]);
}
// ---------------- arm 3: planted ----------------
{
  const f = [];
  const caught = [];
  const BAD = [
    ['base CROSSED sentence', 'Showing the Trending x Price list (movement is measured).', 'CROSSED-SENTENCE'],
    ['base FALLBACK sentence', 'No producer has written the Breakout x Price list yet -- these rows are the Price list (movement is not yet measured). The combination you picked is the one that will be served the day that list lands.', 'MOVEMENT-BASIS'],
    ['CROSSED sentence, parenthesis dropped', 'Showing the Trending x Price list.', 'CROSSED-SENTENCE'],
    ['bare parenthesis', 'Trending x Price (movement is measured)', 'MOVEMENT-BASIS'],
    ['list with a parenthesised note', 'These rows are the Price list (as served).', 'LIST-PAREN'],
  ];
  for (const [n, s, cls] of BAD) {
    const x = phraseFaults(s);
    if (x.some((y) => y.startsWith(cls + ':'))) caught.push(`${n}->${cls}`); else f.push(`"${n}" not rejected as ${cls} (${x[0] || 'no fault'})`);
  }
  const GOOD = [
    'Change over the last 30 days to October 1st, 2026.',
    'Prices from Bloomberg, as of October 1st, 2026; the list is ranked by the size of each move.',
    'Articles collected per month, from the harvest. As of 2026-10-02.',
  ];
  for (const s of GOOD) { const x = phraseFaults(s); if (x.length) f.push(`reader sentence rejected: "${s}" (${x[0]})`); }
  const ATTR_ONLY = '<div class="text-xs" data-resolution="CROSSED" data-served-axis="TRENDING_PRICE"><p data-price-window="">Change over the last 30 days to October 1st, 2026</p></div>';
  const xa = phraseFaults(visible(ATTR_ONLY));
  if (xa.length) f.push(`a data-attribute-only resolution is rejected (${xa[0]})`);
  arms.push(['PLANTED: the phrase predicate rejects the base CROSSED and FALLBACK sentences and three variants, and accepts three reader sentences and a data-attribute-only trace',
    f.length === 0, f.length === 0 ? `${GOOD.length + 1} references 0 faults; ${caught.length} of ${BAD.length} mutants rejected (${caught.join(', ')})` : f.join(' | ')]);
}

let pass = 0;
for (const [n, ok, d] of arms) { if (ok) pass += 1; console.log(`${ok ? 'ARM PASS' : 'ARM FAIL'} ${n} :: ${d}`); }
console.log(`WALL: ${((Date.now() - T0) / 1000).toFixed(1)}s`);
console.log(`THE LEAD PANEL PRINTS NO MOVEMENT-BASIS SYSTEM WORDS: ${pass} of ${arms.length} arms`);
process.exit(pass === arms.length ? 0 : 1);
