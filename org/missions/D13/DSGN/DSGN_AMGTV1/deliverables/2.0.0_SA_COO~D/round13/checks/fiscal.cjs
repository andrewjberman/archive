/**
 * fiscal.cjs -- DSGN_AMGTV1 round 13, AV-l-2: EVERY FISCAL FIGURE ON THE MODEL TAB CARRIES ITS UNIT, TABULAR NUMERALS AND A TOOLTIP
 * WITH ITS MNEMONIC AND FULL VALUE, EXACTLY AS THE HEADER DOES (round-12 analysis ruling 2; FWD-13, FWD-15).
 *
 * Usage (repo root): node <this file>
 * Ruling 2: "FWD-13 binds the Model tab's fiscal cells: each fiscal figure carries its unit and tabular numerals, and a tooltip with
 * its mnemonic and full-precision value, exactly as the header does." The header's contract (round 12, AV-m-3): an element with
 * `data-figure-tooltip="<MNEMONIC>"` and the served value verbatim (String(value)) in `data-full-value`, holding the estate
 * DataTooltip. Each served fiscal figure (the /thesis bundle's `fiscal_year_figures`) carries `unit` (MILLIONS, PERCENT, PER SHARE
 * ..., RATIO ..., PRICE ..., MILLIONS (share count)) and a `currency`.
 * Fixtures (round13/fixtures, SERVED, captured at the cut): BA US /thesis (342 fiscal figures). ISSUER VARIANT (labelled, in
 * memory): Opal's base-case reason set to "no cases on the landed block (derived before C-MODEL-WINDOW-AND-ROWS (5))" -- the
 * contract-code token the round-12 render PNG showed.
 * Arms:
 *   1  every served fiscal cell of BA's sheet (`[data-model-cell]` in a `[data-model-row]`) is tabular and carries a tooltip
 *      element naming its row's mnemonic, with the served value verbatim in data-full-value
 *   2  every served fiscal row says its unit in words (millions / per cent / per share / multiple / the price's currency), from the
 *      served unit -- no row of figures without its unit
 *   3  no raw number or code on the Model tab: 0 visible numbers with more than 4 fractional digits, and the planted
 *      "C-MODEL-WINDOW-AND-ROWS" reason shows no contract-code token (the served reason may ride a data- attribute)
 * Prints one line per arm and "FISCAL FIGURES CARRY UNIT AND TOOLTIP: <k> of 3 arms"; exit 0 only at 3 of 3.
 */
const L = require('./_load.cjs');
const S = require('./surfaces.cjs');
const clone = (x) => JSON.parse(JSON.stringify(x));
const unesc = (s) => String(s).replace(/&amp;/g, '&').replace(/&quot;/g, '"').replace(/&#x27;/g, "'");
const attrs = (tag) => Object.fromEntries([...tag.matchAll(/([a-zA-Z-]+)="([^"]*)"/g)].map((m) => [m[1], unesc(m[2])]));
const K = 'BA_US_Equity';
const thesis = S.unwrap(L.fixture('thesisBundle.BA_US_Equity.json'));
let T = thesis;
L.hookState.impl = Object.assign({}, L.hookState.impl, {
  useThesisBundle: (k) => (k === K ? T : (S.bundles[k] || undefined)),
  useModelVersions: () => undefined,
  useModelCompare: () => undefined,
  useInputLedger: () => undefined,
});
const MT = (() => { try { return L.source('src/pages/SecurityAnalysis/tabs/ModelTab.tsx'); } catch (e) { return null; } })();
const render = () => { try { return MT ? L.render(MT.ModelTab, { securityKey: K }) : ''; } catch (e) { return 'RENDER FAILED ' + e.message; } };
const figs = thesis.fiscal_year_figures || (thesis.model || {}).fiscal_year_figures || [];
const byKey = {};
for (const f of figs) byKey[`${f.mnemonic}|${f.fiscal_year}`] = f;
const unitWord = (u) => {
  const s = String(u || '').toUpperCase();
  if (s.startsWith('PERCENT')) return /%|per ?cent/i;
  if (s.startsWith('PER SHARE')) return /per share/i;
  if (s.startsWith('RATIO')) return /\bx\b|multiple|ratio|times/i;
  if (s.startsWith('PRICE')) return /price|USD|EUR|GBP|JPY|HKD|per share/i;
  if (s.startsWith('MILLIONS')) return /million|\bmm\b|\bM\b/i;
  return null;
};

const html = render();
const rows = [...html.matchAll(/<tr[^>]*data-model-row="([^"]+)"[^>]*>([\s\S]*?)<\/tr>/g)];

// ---- arm 1 ------------------------------------------------------------------------------------------------------------------
const f1 = [];
let cells = 0;
for (const [, mn, body] of rows) {
  for (const m of body.matchAll(/<td[^>]*data-model-cell="([^"]*)"[^>]*data-model-year="([^"]*)"[^>]*>([\s\S]*?)<\/td>|<td[^>]*data-model-year="([^"]*)"[^>]*data-model-cell="([^"]*)"[^>]*>([\s\S]*?)<\/td>/g)) {
    const year = m[2] || m[4];
    const served = byKey[`${mn}|${year}`];
    if (!served) continue;
    cells += 1;
    const td = m[0];
    const tips = [...td.matchAll(/<[a-z]+[^>]*data-figure-tooltip="[^"]*"[^>]*>/g)].map((t) => attrs(t[0])).filter((a) => a['data-figure-tooltip'] === mn);
    if (!/tabular-nums/.test(td)) f1.push(`${mn} ${year}: not tabular`);
    if (tips.length === 0) f1.push(`${mn} ${year}: no tooltip naming ${mn}`);
    else if (tips[0]['data-full-value'] !== String(served.value)) f1.push(`${mn} ${year}: tooltip value "${tips[0]['data-full-value']}", want "${String(served.value)}"`);
    if (f1.length > 5) break;
  }
}
if (cells === 0) f1.push('no served fiscal cell rendered');
const a1 = f1.length === 0;
const a1d = a1 ? `${cells} served fiscal cells, each tabular with a tooltip naming its mnemonic and the served value verbatim` : `${f1.length}+ failing over ${cells} cells; first: ${f1[0]}`;

// ---- arm 2 ------------------------------------------------------------------------------------------------------------------
const f2 = [];
let unitRows = 0;
for (const [, mn, body] of rows) {
  const one = figs.find((f) => f.mnemonic === mn);
  if (!one || !/data-model-cell="[^"]+"/.test(body)) continue;
  const re = unitWord(one.unit);
  if (!re) continue;
  unitRows += 1;
  const visible = unesc(L.textOf(body.replace(/<[a-z]+[^>]*role="tooltip"[\s\S]*?<\/div>/g, '')));
  if (!re.test(visible)) f2.push(`${mn} (${one.unit}): the row does not say its unit -- "${visible.slice(0, 80)}"`);
}
if (unitRows === 0) f2.push('no served fiscal row with a unit rendered');
const a2 = f2.length === 0;
const a2d = a2 ? `${unitRows} served fiscal rows each say their unit in words` : `${f2.length} of ${unitRows} rows failing; first: ${f2[0]}`;

// ---- arm 3 ------------------------------------------------------------------------------------------------------------------
const f3 = [];
const raw = unesc(L.textOf(html)).match(/-?\d[\d,]*\.\d{5,}/g) || [];
if (raw.length) f3.push(`${raw.length} visible number(s) with more than 4 fractional digits; first "${raw[0]}"`);
T = clone(thesis);
const planted = 'no cases on the landed block (derived before C-MODEL-WINDOW-AND-ROWS (5))';
let plantedAt = 0;
for (const box of [T.model_cases, (T.model || {}).cases]) {
  if (box && box.base) { box.base = { status: 'ABSENT', reason: planted }; plantedAt += 1; }
}
const h3 = unesc(L.textOf(render()));
T = thesis;
if (plantedAt === 0) f3.push('the issuer could not plant the reason (no case reason in the served bundle)');
else if (/\bC-[A-Z]+(-[A-Z]+)+\b/.test(h3)) f3.push(`a contract-code token is visible: "${(/[^.]*\bC-[A-Z]+(-[A-Z]+)+\b[^.]*/.exec(h3) || [''])[0].trim().slice(0, 100)}"`);
const a3 = f3.length === 0;
const a3d = a3 ? `0 raw floats on BA's Model tab; the planted C-MODEL reason (${plantedAt} site(s)) shows no contract code` : `${f3.length} failing; first: ${f3[0]}`;

const arms = [
  ['every fiscal cell tabular with its mnemonic and full value one hover away', a1, a1d],
  ['every fiscal row says its unit', a2, a2d],
  ['no raw float, no contract code on the Model tab', a3, a3d],
];
let pass = 0;
for (const [name, ok, detail] of arms) { if (ok) pass += 1; console.log(`${ok ? 'ARM PASS' : 'ARM FAIL'} ${name} :: ${detail}`); }
console.log(`FISCAL FIGURES CARRY UNIT AND TOOLTIP: ${pass} of ${arms.length} arms`);
process.exit(pass === arms.length ? 0 : 1);
