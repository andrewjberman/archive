/**
 * face29.cjs -- AMGT_CORPUS round 29, CRPS-ae-1: THE MODEL SHEET READS LIKE THE ANALYST'S (round-28 analysis @bd50135e57 s.2
 * rulings 1-3, s.3 criteria 1-3).
 *
 * Usage (repo root): node <this file>
 * Method: STATIC, through DSGN's read-only loader (_load.cjs) on BA's served /thesis capture (DSGN round14 fixtures, read-only),
 * the round-28 checks re-run as the regression floor. Arms:
 *   1  CONSENSUS LABEL (ruling 1): the Model face carries no "nothing estimated" sentence; it reads "Reported figures and
 *      Bloomberg consensus estimates, from the model block"; the sheet header labels the E columns "Consensus (Bloomberg)"
 *   2  DECIMALS PER ROW TYPE (ruling 2), on every figure cell of BA's grid (history and E columns): millions rows
 *      (IS_SH_FOR_DILUTED_EPS, EBITDA, EBITDA_ADJUSTED) 0 dp with thousands separators; per-share rows (REVENUE_PER_SH, IS_EPS,
 *      BOOK_VAL_PER_SH, IS_DIV_PER_SHR) 2 dp; multiples (PE_RATIO, PX_TO_BOOK_RATIO) 1 dp with "x"; percent rows
 *      (EQY_DVD_YLD_IND, FREE_CASH_FLOW_YIELD, FREE_CASH_FLOW_MARGIN, RETURN_ON_ASSET, RETURN_COM_EQY,
 *      RETURN_ON_TANGIBLE_ASSETS, EBITDA_MARGIN, PROF_MARGIN) 1 dp with "%"
 *   3  FULL VALUES KEPT: every figure cell still carries its full served value in data-model-cell (BA: every fiscal figure on a
 *      sheet row, and BEST_EPS 2026 = -0.8280000000000001)
 *   4  CURRENCY ONCE (ruling 3): 0 visible "currency not stated"; no sheet row label carries "USD"; the Model face before the sheet
 *      states "USD" exactly once
 *   5  MARKED ROWS (ruling 3): at least one BA row label carries the mark "*" (BA's per-share and EBITDA rows have no measured
 *      currency) and exactly one footnote line reads "currency not stated by the source for marked rows"
 *   6  REGRESSION: round 28's face.cjs (9 of 9) and sheet.cjs (6 of 6) still pass
 * Prints one line per arm and "THE SHEET READS LIKE THE ANALYST'S: <k> of 6 arms"; exit 0 only at 6 of 6.
 * No network, no AWS, writes no file.
 */
const path = require('path');
const { spawnSync } = require('child_process');
const DSGN = path.join(process.cwd(), 'org/missions/D13/DSGN/DSGN_AMGTV1/deliverables/2.0.0_SA_COO~D/round14/checks');
const R28 = path.join(process.cwd(), 'org/missions/D5/AMGT/AMGT_CORPUS/deliverables/2.0.0_SA_COO~X/checks/round28');
const L = require(path.join(DSGN, '_load.cjs'));
const S = require(path.join(DSGN, 'surfaces.cjs'));

const K = 'BA_US_Equity';
const TYPES = {
  millions: { re: /^-?\d{1,3}(,\d{3})*$/, rows: ['IS_SH_FOR_DILUTED_EPS', 'EBITDA', 'EBITDA_ADJUSTED'] },
  perShare: { re: /^-?[\d,]+\.\d{2}$/, rows: ['REVENUE_PER_SH', 'IS_EPS', 'BOOK_VAL_PER_SH', 'IS_DIV_PER_SHR'] },
  multiple: { re: /^-?[\d,]+\.\d ?x$/, rows: ['PE_RATIO', 'PX_TO_BOOK_RATIO'] },
  percent: {
    re: /^-?[\d,]+\.\d ?%$/,
    rows: ['EQY_DVD_YLD_IND', 'FREE_CASH_FLOW_YIELD', 'FREE_CASH_FLOW_MARGIN', 'RETURN_ON_ASSET', 'RETURN_COM_EQY',
      'RETURN_ON_TANGIBLE_ASSETS', 'EBITDA_MARGIN', 'PROF_MARGIN'],
  },
};
const typeOf = {};
for (const [t, v] of Object.entries(TYPES)) for (const m of v.rows) typeOf[m] = t;

const thesis = S.unwrap(L.fixture('thesisBundle.BA_US_Equity.json'));
L.hookState.impl = Object.assign({}, L.hookState.impl, {
  useThesisBundle: (k) => (k === K ? thesis : (S.bundles[k] || undefined)),
  useModelVersions: () => undefined,
  useModelCompare: () => undefined,
  useInputLedger: () => undefined,
});
let html = '';
let err = '';
try { const MT = L.source('src/pages/SecurityAnalysis/tabs/ModelTab.tsx'); html = L.render(MT.ModelTab, { securityKey: K }); } catch (e) { err = e.message; }
const sheet = html ? (L.innerOf(html, 'data-model-sheet', '') || '') : '';
const allRows = [...sheet.matchAll(/<tr[^>]*data-model-row="([^"]*)"[^>]*>([\s\S]*?)<\/tr>/g)].map((m) => ({ mnemonic: m[1], body: m[2] }));
// A REFUSED row (the fixture is a capture from before ad-4, so BA's DPS and some P/E years still read refused) prints its
// refusal sentence and no figure; arms 2-3 grade the figures the face prints, so they read the non-refused rows.
const rows = allRows.filter((r) => !r.body.includes('data-model-refused'));
const refusedRows = allRows.filter((r) => r.body.includes('data-model-refused')).map((r) => r.mnemonic);
const labelOf = (body) => L.textOf((/<td[^>]*>([\s\S]*?)<\/td>/.exec(body) || [, ''])[1]);
const cellsOf = (body) => [...body.matchAll(/<td[^>]*data-model-cell="([^"]*)"[^>]*>([\s\S]*?)<\/td>/g)].map((m) => ({ full: m[1], text: L.textOf(m[2]) }));
const lead = (t) => ((t || '').trim().match(/^-?[\d,]*\.?\d+ ?[x%]?/) || [''])[0];

const results = [];
const arm = (n, name, fails) => { results.push(fails.length === 0); console.log(`ARM ${n} ${name}: ${fails.length === 0 ? 'PASS' : 'FAIL -- ' + fails.slice(0, 6).join('; ')}`); };
if (!html) { console.log('THE SHEET READS LIKE THE ANALYST\'S: 0 of 6 arms (ModelTab did not render: ' + err.slice(0, 80) + ')'); process.exit(1); }
const text = L.textOf(html);

{
  const f = [];
  if (/nothing estimated/i.test(text)) f.push('the face still says "nothing estimated"');
  if (!text.includes('Reported figures and Bloomberg consensus estimates, from the model block')) f.push('no header "Reported figures and Bloomberg consensus estimates, from the model block"');
  const head = (/<thead[^>]*>([\s\S]*?)<\/thead>/.exec(sheet) || [, ''])[1];
  if (!L.textOf(head).includes('Consensus (Bloomberg)')) f.push('the sheet header does not label the E columns "Consensus (Bloomberg)"');
  arm(1, 'the E columns are labelled consensus; no "nothing estimated"', f);
}
{
  const f = [];
  let graded = 0;
  for (const r of rows) {
    const t = typeOf[r.mnemonic];
    if (!t) { f.push(`row ${r.mnemonic} has no row type in this check`); continue; }
    for (const c of cellsOf(r.body)) {
      graded += 1;
      const v = lead(c.text);
      if (!TYPES[t].re.test(v)) f.push(`${r.mnemonic} (${t}) prints "${c.text.slice(0, 24)}"`);
    }
  }
  if (graded === 0) f.push('no figure cell graded');
  console.log(`DECIMALS cells graded ${graded} over ${rows.length} rows (refused rows skipped: ${refusedRows.join(',') || 'none'})`);
  arm(2, 'decimals per row type', f);
}
{
  const f = [];
  const fulls = new Set(rows.flatMap((r) => cellsOf(r.body).map((c) => `${r.mnemonic}|${c.full}`)));
  const fc = ((thesis.model || {}).forecast_figures || []).find((x) => x.mnemonic === 'BEST_EPS' && Number(x.fiscal_year) === 2026);
  if (!fc || !fulls.has(`IS_EPS|${String(fc.value)}`)) f.push('BEST_EPS 2026 full value not carried on the EPS row');
  const sheetMn = new Set(rows.map((r) => r.mnemonic));
  let missing = 0;
  for (const fig of thesis.fiscal_year_figures || []) {
    if (!sheetMn.has(fig.mnemonic) || fig.value == null) continue;
    if (!fulls.has(`${fig.mnemonic}|${String(fig.value)}`)) missing += 1;
  }
  if (missing) f.push(`${missing} fiscal figure(s) on sheet rows lost their full served value`);
  arm(3, 'full served values kept in data-model-cell', f);
}
{
  const f = [];
  const n1 = (text.match(/currency not stated(?! by the source for marked rows)/gi) || []).length;
  if (n1) f.push(`${n1} visible "currency not stated" phrase(s)`);
  const usdLabels = rows.filter((r) => /\bUSD\b/.test(labelOf(r.body))).map((r) => r.mnemonic);
  if (usdLabels.length) f.push(`row labels carry USD: ${usdLabels.join(',')}`);
  const before = L.textOf(html.slice(0, html.indexOf('data-model-sheet')));
  const nUsd = (before.match(/\bUSD\b/g) || []).length;
  if (nUsd !== 1) f.push(`the face before the sheet states USD ${nUsd} time(s), want exactly 1`);
  arm(4, 'the currency is stated once per name', f);
}
{
  const f = [];
  const marked = rows.filter((r) => labelOf(r.body).includes('*')).map((r) => r.mnemonic);
  if (marked.length === 0) f.push('no row label carries the "*" mark');
  const nFoot = (text.match(/currency not stated by the source for marked rows/gi) || []).length;
  if (nFoot !== 1) f.push(`${nFoot} footnote line(s) "currency not stated by the source for marked rows", want 1`);
  console.log(`MARKED rows ${marked.join(',') || 'none'}`);
  arm(5, 'unmeasured-currency rows are marked once, footnoted once', f);
}
{
  const f = [];
  for (const [file, want] of [['face.cjs', "THE MODEL FACE IN THE TEAM'S SHAPE: 9 of 9 arms"], ['sheet.cjs', 'THE SHEET IN THE SHAREPOINT SHAPE: 6 of 6 arms']]) {
    const r = spawnSync(process.execPath, [path.join(R28, file)], { encoding: 'utf8', cwd: process.cwd() });
    if (r.status !== 0 || !(r.stdout || '').includes(want)) f.push(`round-28 ${file} reads "${((r.stdout || '').trim().split('\n').pop() || '').slice(0, 70)}"`);
  }
  arm(6, "round 28's checks still pass", f);
}
const k = results.filter(Boolean).length;
console.log(`THE SHEET READS LIKE THE ANALYST'S: ${k} of 6 arms`);
process.exit(k === 6 ? 0 : 1);
