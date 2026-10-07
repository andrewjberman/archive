/**
 * r47b.cjs -- DSGN_AMGTV1 round 47 issuer CHECK (2.0.0_SA_COO~D): A NAME WITH NO STORED FIGURES SAYS SO ONCE, NOT ON SEVEN TILES.
 *
 * Usage (from the directory whose portal/ is the checkout under test):
 *   cd "$(git rev-parse --show-toplevel)" && node "org/missions/D13/DSGN/DSGN_AMGTV1/deliverables/2.0.0_SA_COO~D/round47/checks/r47b/r47b.cjs"
 *
 * Why: ledger/CTO_COUNTERSIGN_COMPLETION_GRADES_ROUND46.md, section CORRECTION @50e71b5b8d, round-47 item 5: "a name the firm does
 * not cover says so ONCE, in plain words, where its header figures would be, in place of seven tiles repeating one sentence."
 * Read first, as the item orders (walk read-20261007T093016Z/17-fwd24-overlay-census-MSFT-US.json): MSFT US draws 7 tiles, each
 * reading "We hold no stored company data for this name yet."; the served payload carries no coverage marker, only the seven
 * header_figures entries with value null and that one reason. So the page rule is keyed on the served shape: NO key figure carries
 * a value AND every reasoned entry carries the SAME reason.
 *
 * Arms (each prints its evidence; exit 0 only on all of them):
 *   1 ONE SENTENCE: on the uncovered-shaped bundle the row draws 0 key-figure tiles and ONE element [data-key-figures-state="ALL_ABSENT"]
 *     whose text holds the served reason exactly once; the reason appears once in the whole rendered header.
 *   2 KEEP: a bundle with 3 served figures and 4 reasons (ROG SW-shaped) still draws 7 tiles; a bundle whose seven are null with
 *     DIFFERENT reasons still draws its reason tiles (no collapse); a bundle with no figures and no reasons still reads the existing
 *     empty state and draws no ALL_ABSENT element.
 *   3 PLANTED: the grader refuses seven repeated tiles, a reason printed twice and a missing ALL_ABSENT element; a clean form passes.
 * Renders the REAL HeaderCards.tsx through round15/checks/_load.cjs (DataTooltip stubbed); no network; writes nothing.
 */
'use strict';
const path = require('path');
const L = require(path.join(__dirname, '..', '..', '..', 'round15', 'checks', '_load.cjs'));
const React = L.React;
const DT = { DataTooltip: ({ header, rows }) => React.createElement('div', { 'data-tt': '' },
  React.createElement('span', { 'data-tt-header': '' }, header),
  ...(rows || []).map((r, i) => React.createElement('span', { key: i, 'data-tt-row': r.label }, `${r.label}: ${r.value}`))) };
L.stubSource('src/components/DataTooltip', DT);
L.stubSource('src/components/DataTooltip.tsx', DT);

const VINT = '2026-10-06T13:30:00Z';
const fig = (mnemonic, value, unit, currency, extra) => Object.assign({ scope: 'HEADER', fiscal_year: null, mnemonic, value, unit,
  sign: null, basis: { mnemonic, definition: '' }, vintage: VINT, source: 'bloomberg', currency }, extra || {});
const SEVEN = ['PX_LAST', 'CUR_MKT_CAP', 'CURR_ENTP_VAL', 'NET_DEBT', 'EQY_BETA', 'VOLUME_AVG_30D', 'SHORT_INT_RATIO'];
const ONE = 'We hold no stored company data for this name yet.';
const UNCOVERED = { header_figures: SEVEN.map((m) => fig(m, null, null, null, { reason: ONE, source: null })) };
const DIFFERENT = { header_figures: SEVEN.map((m, i) => fig(m, null, null, null, { reason: `Reason number ${i + 1} for this figure.`, source: null })) };
const ROG = { header_figures: [
  fig('CRNCY', 'CHF', 'TEXT (string field)', null),
  fig('CUR_MKT_CAP', 280836583190, 'ABSOLUTE (full currency units)', 'CHF'),
  fig('NET_DEBT', 17715, 'MILLIONS', 'CHF'),
  fig('CURR_ENTP_VAL', 306930.58319, 'MILLIONS', 'CHF'),
  fig('PX_LAST', null, null, null, { reason: 'Bloomberg returned no value for price for this name in the latest stored pull.', source: null }),
  fig('EQY_BETA', null, null, null, { reason: 'Bloomberg returned no value for beta for this name in the latest stored pull.', source: null }),
  fig('VOLUME_AVG_30D', null, null, null, { reason: 'Average volume is not in the latest stored pull for this name.', source: null }),
  fig('SHORT_INT_RATIO', null, null, null, { reason: 'Short interest is not in the latest stored pull for this name.', source: null }),
] };
const EMPTY = { header_figures: [] };

let HC;
try { HC = L.source('src/pages/SecurityAnalysis/components/HeaderCards.tsx'); }
catch (e) { console.log('LOADER ERROR: HeaderCards.tsx :: ' + String(e && e.message).split('\n')[0]); process.exit(3); }

const decode = (s) => s.replace(/&amp;/g, '&').replace(/&quot;/g, '"').replace(/&#x27;/g, "'").replace(/&lt;/g, '<').replace(/&gt;/g, '>');
const text = (html) => decode(String(html).replace(/<[^>]+>/g, ' ')).replace(/\s+/g, ' ').trim();
const tileCount = (html) => (String(html).match(/<div[^>]*data-card-figure="[^"]+"/g) || []).length;
const times = (hay, needle) => String(hay).split(needle).length - 1;
const render = (bundle) => { try { return L.render(HC.HeaderCards, { bundle }); } catch (e) { return 'RENDER FAILED ' + String(e.message).split('\n')[0]; } };

function gradeOnce(html, reason) {
  const f = [];
  if (/^RENDER FAILED/.test(html)) return [html];
  const n = tileCount(html);
  if (n !== 0) f.push(`${n} key-figure tile(s) drawn (0 wanted)`);
  const marks = (html.match(/data-key-figures-state="ALL_ABSENT"/g) || []).length;
  if (marks !== 1) f.push(`${marks} [data-key-figures-state="ALL_ABSENT"] element(s) (1 wanted)`);
  const k = times(text(html), reason);
  if (k !== 1) f.push(`the reason is printed ${k} time(s) (1 wanted)`);
  return f;
}

const arms = [];
const unHtml = render(UNCOVERED);
{
  const f = gradeOnce(unHtml, ONE);
  arms.push(['ONE SENTENCE FOR A NAME WITH NO STORED FIGURES', f.length === 0, f.length ? f.join(' | ') : '0 tiles; one ALL_ABSENT element; the served reason printed once']);
}
{
  const f = [];
  const rog = render(ROG); const dif = render(DIFFERENT); const emp = render(EMPTY);
  for (const [name, h] of [['ROG', rog], ['DIFFERENT', dif], ['EMPTY', emp]]) if (/^RENDER FAILED/.test(h)) f.push(`${name}: ${h}`);
  if (tileCount(rog) !== 7) f.push(`ROG-shaped bundle: ${tileCount(rog)} tiles (7 wanted)`);
  if (/data-key-figures-state="ALL_ABSENT"/.test(rog)) f.push('ROG-shaped bundle collapsed');
  if (tileCount(dif) !== 7) f.push(`seven different reasons: ${tileCount(dif)} tiles (7 wanted)`);
  if (/data-key-figures-state="ALL_ABSENT"/.test(dif)) f.push('seven different reasons collapsed');
  if (/data-key-figures-state="ALL_ABSENT"/.test(emp)) f.push('a bundle with no figures and no reasons drew ALL_ABSENT');
  if (!/No key figures have been published for this name yet/.test(text(emp))) f.push('the existing empty state is gone');
  arms.push(['KEEP: mixed and differing-reason rows keep their tiles; the empty state is unchanged', f.length === 0, f.length ? f.join(' | ') : 'ROG-shaped 7 tiles; seven different reasons 7 tiles; empty state kept']);
}
{
  const f = [];
  const seven = SEVEN.map((m) => `<div data-card-figure="${m}" data-card-figure-state="ABSENT"><p>${ONE}</p></div>`).join('');
  if (!gradeOnce(seven, ONE).length) f.push('seven repeated tiles accepted');
  if (!gradeOnce(`<p data-key-figures-state="ALL_ABSENT">${ONE}</p><p>${ONE}</p>`, ONE).length) f.push('a reason printed twice accepted');
  if (!gradeOnce(`<p>${ONE}</p>`, ONE).length) f.push('a missing ALL_ABSENT element accepted');
  if (gradeOnce(`<p data-key-figures-state="ALL_ABSENT">${ONE}</p>`, ONE).length) f.push('the clean form refused');
  arms.push(['PLANTED', f.length === 0, f.length ? f.join(' | ') : '3 of 3 faults refused; the clean form admitted']);
}

const TITLE = 'A NAME WITH NO STORED FIGURES SAYS SO ONCE';
let pass = 0;
for (const [name, ok, ev] of arms) { if (ok) pass += 1; console.log(`ARM ${ok ? 'PASS' : 'FAIL'} ${name} :: ${ev}`); }
console.log(`${TITLE}: ${pass} of ${arms.length} arms`);
process.exit(pass === arms.length && arms.length === 3 ? 0 : 1);
