/**
 * r57b.cjs -- DSGN_AMGTV1 round 57 issuer CHECK (2.0.0_SA_COO~D1): THE REPAIRS -- A PRICE LABEL READS WHOLE ON FOCUS, AND A SERVED
 * REASON'S DAYS READ IN THE HOUSE FORM.
 *
 * Usage (from the directory whose portal/ is the checkout under test):
 *   cd "$(git rev-parse --show-toplevel)" && node "org/missions/D13/DSGN/DSGN_AMGTV1/deliverables/2.0.0_SA_COO~D1/round57/checks/r57b.cjs"
 *
 * Why (round-56 analysis, ledger/ROUND_ANALYSIS.round56.md):
 *   R5 -- a Price label is cut at w-36 ("Advanced Micro Devices ..."); it must carry its full text on hover AND focus. The row's
 *         title already holds the full words (hoverText); a keyboard reader cannot reach it, because the row takes no focus.
 *   R3 -- one date form on /security-analysis: served reason text printed verbatim on the Model card
 *         (WhatChangedPanel compare.reason, ModelTab "Lines with no figure: <reason>") can carry an ISO day. The page's own precedent,
 *         SecurityOverlay.tsx:96, rewrites ISO days inside a served reason with longDate.
 *
 * Arms (each prints its evidence; exit 0 only on all four):
 *   1 PRICE ROW TAKES FOCUS: PriceBars rendered with a long-named keyed row and an unkeyed row -> the keyed <li data-price-bar>
 *     carries tabindex="0", role="button" and aria-label equal to its title (the full words, label included); the unkeyed row
 *     carries no tabindex.
 *   2 DAYS IN A REASON: dateWords.ts daysInWords() turns every YYYY-MM-DD inside a text into longDate(day) and leaves other text
 *     as it came ("as of 2026-09-22." -> "as of September 22nd, 2026."; "no figure." unchanged; null -> '').
 *   3 THE CARD USES IT: WhatChangedPanel.tsx prints compare.reason through daysInWords, and ModelTab.tsx prints its no-figure
 *     reason through daysInWords (source read; behaviour is arm 2).
 *   4 PLANTED: the graders refuse an unfocusable keyed row, an aria-label that is not the title, a daysInWords that leaves ISO, and
 *     a card printing the raw reason.
 * Renders the REAL PriceBars through D's round15/checks/_load.cjs; no network; writes nothing.
 */
'use strict';
const fs = require('fs');
const path = require('path');
const DD = path.join(__dirname, '..', '..', '..', '2.0.0_SA_COO~D');
const L = require(path.join(DD, 'round15', 'checks', '_load.cjs'));
const SA = path.join(process.cwd(), 'portal', 'src', 'pages', 'SecurityAnalysis');
const decode = (s) => String(s).replace(/&amp;/g, '&').replace(/&quot;/g, '"').replace(/&#x27;/g, "'").replace(/&lt;/g, '<').replace(/&gt;/g, '>');
const attr = (attrs, name) => { const m = new RegExp('\\s' + name + '="([^"]*)"').exec(attrs || ''); return m ? decode(m[1]) : null; };

const LONG = 'Advanced Micro Devices Incorporated Holdings';
const rows = [
  { ticker: 'AMD US', security_key: 'AMD_US_Equity', display_name: LONG, axis_date: '2026-10-07', return_30d_pct: 27.7, classification: { asset_class: 'Equity', sub_asset_class: 'Common', sector: 'Information Technology' } },
  { ticker: 'XYZ US', security_key: null, display_name: 'Unkeyed Co', axis_date: '2026-10-07', return_30d_pct: -3.2, classification: {} },
];
function liAttrs(html) { return (String(html).match(/<li[^>]*data-price-bar=[^>]*>/g) || []).map((t) => t); }
function focusFaults(html) {
  const f = []; const lis = liAttrs(html);
  if (lis.length !== 2) return [`${lis.length} price rows drawn (wanted 2)`];
  const [k, u] = lis;
  if (attr(k, 'tabindex') !== '0') f.push(`keyed row tabindex ${attr(k, 'tabindex')}`);
  if (attr(k, 'role') !== 'button') f.push(`keyed row role ${attr(k, 'role')}`);
  const t = attr(k, 'title'); const a = attr(k, 'aria-label');
  if (!t || a !== t) f.push(`keyed row aria-label ${JSON.stringify(a)} is not its title ${JSON.stringify(t)}`);
  if (a && !a.includes(LONG)) f.push('aria-label lacks the full label');
  if (attr(u, 'tabindex') !== null) f.push(`unkeyed row tabindex ${attr(u, 'tabindex')}`);
  return f;
}
function daysFaults(fn, longDate) {
  const f = [];
  const want = `as of ${longDate('2026-09-22')}.`;
  const got = fn('as of 2026-09-22.');
  if (got !== want) f.push(`daysInWords("as of 2026-09-22.") = ${JSON.stringify(got)} (wanted ${JSON.stringify(want)})`);
  if (fn('no figure.') !== 'no figure.') f.push('text without a day changed');
  const two = fn('from 2026-09-01 to 2026-09-22');
  if (/\d{4}-\d{2}-\d{2}/.test(two)) f.push(`two days not both rewritten: ${JSON.stringify(two)}`);
  if (fn(null) !== '') f.push('null does not read ""');
  return f;
}
function wiringFaults(wcp, mt) {
  const f = [];
  if (!/daysInWords\(\s*compare\.reason/.test(wcp)) f.push('WhatChangedPanel.tsx does not print compare.reason through daysInWords');
  if (!/Lines with no figure: \$\{daysInWords\(reason\)\}/.test(mt)) f.push('ModelTab.tsx does not print its no-figure reason through daysInWords');
  return f;
}

const arms = []; const load = [];
let PB = null; let DW = null;
L.stubSource('src/ui/components/states', { PanelEmpty: () => null, PanelError: () => null, PanelLoading: () => null });
try { DW = L.source('src/pages/SecurityAnalysis/dateWords.ts'); } catch (e) { load.push('LOADER: dateWords.ts ' + String(e.message).split('\n')[0]); }
try { PB = L.source('src/pages/SecurityAnalysis/components/PriceBars.tsx').PriceBars; } catch (e) { load.push('LOADER: PriceBars.tsx ' + String(e.message).split('\n')[0]); }
{
  let f;
  if (!PB) f = load.slice();
  else { try { f = focusFaults(L.render(PB, { rows, onSelectSecurity: () => {}, asOfDate: '2026-10-07' })); } catch (e) { f = ['RENDER FAILED ' + String(e.message).split('\n')[0]]; } }
  arms.push(['PRICE ROW TAKES FOCUS', f.length === 0, f.length ? f.join(' | ') : 'the keyed row: tabindex 0, role button, aria-label = its title with the full label; the unkeyed row takes no focus']);
}
{
  const f = DW && typeof DW.daysInWords === 'function' ? daysFaults(DW.daysInWords, DW.longDate) : (load.length && !DW ? load.slice() : ['dateWords.ts exports no daysInWords']);
  arms.push(['DAYS IN A REASON', f.length === 0, f.length ? f.join(' | ') : `"as of 2026-09-22." reads "as of ${DW.longDate('2026-09-22')}."; plain text unchanged; two days both rewritten`]);
}
{
  let wcp = null; let mt = null;
  try { wcp = fs.readFileSync(path.join(SA, 'components', 'model', 'WhatChangedPanel.tsx'), 'utf8'); mt = fs.readFileSync(path.join(SA, 'tabs', 'ModelTab.tsx'), 'utf8'); } catch (e) { /* read below */ }
  const f = wcp === null || mt === null ? ['cannot read WhatChangedPanel.tsx / ModelTab.tsx'] : wiringFaults(wcp, mt);
  arms.push(['THE CARD USES IT', f.length === 0, f.length ? f.join(' | ') : 'both served reasons print through daysInWords']);
}
{
  const f = [];
  const li = (k, extra) => `<li data-price-bar="${k}" title="${LONG} (AMD US)" ${extra}>x</li>`;
  const clean = li('AMD_US_Equity', `tabindex="0" role="button" aria-label="${LONG} (AMD US)"`) + li('XYZ', '');
  if (focusFaults(clean).length) f.push('the clean rows refused');
  if (!focusFaults(li('AMD_US_Equity', `role="button" aria-label="${LONG} (AMD US)"`) + li('XYZ', '')).length) f.push('an unfocusable keyed row accepted');
  if (!focusFaults(li('AMD_US_Equity', 'tabindex="0" role="button" aria-label="AMD"') + li('XYZ', '')).length) f.push('an aria-label that is not the title accepted');
  const ld = (d) => `LONGDAY${d.length}`;
  if (!daysFaults((t) => (t === null ? '' : String(t)), ld).length) f.push('a daysInWords that leaves ISO accepted');
  if (daysFaults((t) => (t === null ? '' : String(t).replace(/\d{4}-\d{2}-\d{2}/g, ld)), ld).length) f.push('the clean daysInWords refused');
  if (!wiringFaults('{compare.reason ?? "x"}', '`Lines with no figure: ${reason}`').length) f.push('a card printing the raw reason accepted');
  arms.push(['PLANTED', f.length === 0, f.length ? f.join(' | ') : '4 of 4 faults refused; the clean forms admitted']);
}

const TITLE = 'THE REPAIRS: A PRICE LABEL READS WHOLE ON FOCUS, A SERVED REASON READS ONE DATE FORM';
let pass = 0;
for (const [name, ok, ev] of arms) { if (ok) pass += 1; console.log(`ARM ${ok ? 'PASS' : 'FAIL'} ${name} :: ${ev}`); }
console.log(`${TITLE}: ${pass} of ${arms.length} arms`);
process.exit(pass === arms.length && arms.length === 4 ? 0 : 1);
