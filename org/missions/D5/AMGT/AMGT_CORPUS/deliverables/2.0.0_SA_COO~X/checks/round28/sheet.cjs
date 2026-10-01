/**
 * sheet.cjs -- AMGT_CORPUS round 28, CRPS-ad-1: THE SHEET IN THE SHAREPOINT SHAPE, WITH ITS FORECASTS
 * (PRD v0.7 Addendum B: FWD-12 amended, FWD-20 the five null rows, FWD-21 the served 2026E-2028E forecasts).
 *
 * Usage (repo root): node <this file>            -> grades
 *                    node <this file> --snapshot -> writes base_history.BA.json (the issuer's act at the cut; never the worker's)
 * Method: STATIC, through DSGN's read-only loader (_load.cjs: installed typescript + react-dom/server, the page hooks stubbed) on
 * BA's served /thesis capture (DSGN round14 fixtures, read-only). Arms:
 *   1  ROWS: the five sheet rows modelSheet.ts maps to no field today read the fields the block already pulls --
 *      Revenue/Sh REVENUE_PER_SH, FCF yield FREE_CASH_FLOW_YIELD, FCF margin FREE_CASH_FLOW_MARGIN, RoTA
 *      RETURN_ON_TANGIBLE_ASSETS, Earnings margin PROF_MARGIN -- each with at least one figure on BA
 *   2  SHAPE: no "Other lines" group (FWD-12: lines the team sheet does not carry are not rendered); the sheet's groups are the
 *      summary and the margin history only
 *   3  HISTORY BYTE-UNCHANGED: every history-year cell of the twelve rows already mapped equals the base snapshot
 *   4  FORECASTS: buildModelSheet given BA's served `model.forecast_figures` adds the columns 2026E, 2027E, 2028E after the history
 *      years, and the EPS / BVPS / DPS / Dividend yield / P/E / EBITDA rows carry BEST_EPS / BEST_BPS / BEST_DPS / BEST_DIV_YLD /
 *      BEST_PE_RATIO / BEST_EBITDA at those years, value for value as served (BA serves no BEST_PE_RATIO FY1: that one cell is empty)
 *   5  NEGATIVE: with no forecast figures there is no E column and the sheet still names the estimate years it lacks
 *   6  CENSUS: over every name with a block (names100.mnemonics.json), the page's row specs leave 0 rows hard-coded to no field
 *      (base: 5 rows x 100 names = 500); shown / absent / unmapped printed with the denominator
 * Arm 2 also holds the team sheet's groups, rows and order to the base snapshot (labels unchanged; Other lines gone).
 * ModelTab.tsx's wiring of the forecasts (the E columns on the page) is CRPS-ad-3's, graded by face.cjs.
 * Prints one line per arm and "THE SHEET IN THE SHAREPOINT SHAPE: <k> of 6 arms"; exit 0 only at 6 of 6.
 * No network, no AWS; writes no file unless --snapshot.
 */
const fs = require('fs');
const path = require('path');
const DSGN = path.join(process.cwd(), 'org/missions/D13/DSGN/DSGN_AMGTV1/deliverables/2.0.0_SA_COO~D/round14/checks');
const L = require(path.join(DSGN, '_load.cjs'));
const S = require(path.join(DSGN, 'surfaces.cjs'));

const K = 'BA_US_Equity';
const SNAP = path.join(__dirname, 'base_history.BA.json');
const NULL_ROWS = [
  ['Revenue/Sh', 'REVENUE_PER_SH'], ['FCF yield', 'FREE_CASH_FLOW_YIELD'], ['FCF margin', 'FREE_CASH_FLOW_MARGIN'],
  ['RoTA', 'RETURN_ON_TANGIBLE_ASSETS'], ['Earnings margin', 'PROF_MARGIN'],
];
const FC_ROWS = [
  ['EPS', 'BEST_EPS'], ['BVPS', 'BEST_BPS'], ['DPS', 'BEST_DPS'], ['Dividend yield', 'BEST_DIV_YLD'], ['P/E', 'BEST_PE_RATIO'],
  ['EBITDA', 'BEST_EBITDA'],
];
const E_YEARS = ['2026E', '2027E', '2028E'];

const thesis = S.unwrap(L.fixture('thesisBundle.BA_US_Equity.json'));
const model = thesis.model || {};
const forecast = model.forecast_figures || [];
const MS = (() => { try { return L.source('src/pages/SecurityAnalysis/modelSheet.ts'); } catch (e) { return null; } })();
const rows = (sheet) => sheet.groups.flatMap((g) => g.rows);
const rowOf = (sheet, label) => rows(sheet).find((r) => r.label === label);
const cellBytes = (c) => (c === null ? 'null' : JSON.stringify({ m: c.mnemonic, y: String(c.fiscal_year), v: c.value, u: c.unit, s: c.sign }));
const histYears = (sheet) => sheet.years.filter((y) => /^\d{4}$/.test(y));
function historyOf(sheet) {
  const out = {};
  const hy = histYears(sheet);
  for (const r of sheet.groups.filter((g) => !/other lines/i.test(g.title)).flatMap((g) => g.rows)) {
    if (!r.mnemonic || NULL_ROWS.some(([l]) => l === r.label)) continue;
    out[r.label] = hy.map((y) => cellBytes(r.cells[sheet.years.indexOf(y)]));
  }
  return out;
}

if (!MS || typeof MS.buildModelSheet !== 'function') {
  console.log('THE SHEET IN THE SHAREPOINT SHAPE: 0 of 6 arms (modelSheet.ts did not load)');
  process.exit(1);
}
const base = MS.buildModelSheet(thesis.fiscal_year_figures, thesis.fiscal_years, model.line_names);

if (process.argv.includes('--snapshot')) {
  const labels = base.groups.filter((g) => !/other lines/i.test(g.title)).map((g) => ({ title: g.title, labels: g.rows.map((r) => r.label) }));
  fs.writeFileSync(SNAP, JSON.stringify({ key: K, years: histYears(base), labels, rows: historyOf(base) }, null, 1) + '\n');
  console.log('SNAPSHOT ' + Object.keys(historyOf(base)).length + ' rows x ' + histYears(base).length + ' years -> ' + SNAP);
  process.exit(0);
}
let sheetF = null;
try { sheetF = MS.buildModelSheet(thesis.fiscal_year_figures, thesis.fiscal_years, model.line_names, forecast); } catch (e) { sheetF = null; }
const results = [];
const arm = (n, name, fails) => { results.push(fails.length === 0); console.log(`ARM ${n} ${name}: ${fails.length === 0 ? 'PASS' : 'FAIL -- ' + fails.join('; ')}`); };

// 1 ROWS
{
  const f = [];
  for (const [label, mn] of NULL_ROWS) {
    const r = rowOf(base, label);
    if (!r) { f.push(`no "${label}" row`); continue; }
    if (r.mnemonic !== mn) f.push(`"${label}" reads ${r.mnemonic}, want ${mn}`);
    else if (!r.cells.some((c) => c !== null)) f.push(`"${label}" carries no figure on BA`);
  }
  arm(1, 'the five null rows read the pulled fields', f);
}
// 2 SHAPE
{
  const titles = base.groups.map((g) => g.title);
  const f = [];
  if (titles.some((t) => /other lines/i.test(t))) f.push(`groups ${JSON.stringify(titles)} still carry "Other lines"`);
  if (base.groups.length !== 2) f.push(`${base.groups.length} groups, want 2 (summary, margin history)`);
  let snap = null;
  try { snap = JSON.parse(fs.readFileSync(SNAP, 'utf8')); } catch (e) { f.push('no base snapshot ' + SNAP); }
  if (snap) {
    const now = base.groups.map((g) => ({ title: g.title, labels: g.rows.map((r) => r.label) }));
    if (JSON.stringify(now) !== JSON.stringify(snap.labels)) f.push(`the sheet's groups/rows/order ${JSON.stringify(now)} differ from the team sheet's ${JSON.stringify(snap.labels)}`);
  }
  arm(2, "no Other-lines group; the team sheet's rows in its order", f);
}
// 3 HISTORY
{
  const f = [];
  let snap = null;
  try { snap = JSON.parse(fs.readFileSync(SNAP, 'utf8')); } catch (e) { f.push('no base snapshot ' + SNAP); }
  if (snap) {
    const now = historyOf(base);
    if (JSON.stringify(histYears(base)) !== JSON.stringify(snap.years)) f.push(`history years ${histYears(base)} != base ${snap.years}`);
    for (const [label, cells] of Object.entries(snap.rows)) {
      if (JSON.stringify(now[label]) !== JSON.stringify(cells)) f.push(`"${label}" history cells changed`);
    }
    if (sheetF) {
      const withF = historyOf(sheetF);
      for (const [label, cells] of Object.entries(snap.rows)) {
        if (JSON.stringify(withF[label]) !== JSON.stringify(cells)) f.push(`"${label}" history cells changed when forecasts are passed`);
      }
    }
  }
  arm(3, 'history cells byte-unchanged', f);
}
// 4 FORECASTS
{
  const f = [];
  if (!sheetF) f.push('buildModelSheet(figures, years, names, forecast_figures) threw or did not run');
  else {
    const tail = sheetF.years.slice(-3);
    if (JSON.stringify(tail) !== JSON.stringify(E_YEARS)) f.push(`last columns ${JSON.stringify(tail)}, want ${JSON.stringify(E_YEARS)}`);
    for (const [label, mn] of FC_ROWS) {
      const r = rowOf(sheetF, label);
      if (!r) { f.push(`no "${label}" row`); continue; }
      for (const ey of E_YEARS) {
        const y = Number(ey.slice(0, 4));
        const want = forecast.find((x) => x.mnemonic === mn && Number(x.fiscal_year) === y);
        const cell = r.cells[sheetF.years.indexOf(ey)];
        const got = cell ? cell.value : null;
        const wantV = want ? want.value : null;
        if (JSON.stringify(got) !== JSON.stringify(wantV)) f.push(`"${label}" ${ey} reads ${JSON.stringify(got)}, served ${mn} ${JSON.stringify(wantV)}`);
      }
    }
  }
  arm(4, 'the served 2026E-2028E forecasts sit beside the history', f);
}
// 5 NEGATIVE
{
  const f = [];
  let s0 = null;
  try { s0 = MS.buildModelSheet(thesis.fiscal_year_figures, thesis.fiscal_years, model.line_names, []); } catch (e) { f.push('threw on an empty forecast list'); }
  if (s0) {
    if (s0.years.some((y) => /E$/.test(y))) f.push(`E columns without forecasts: ${s0.years}`);
    if (!(s0.estimateYearsAbsent || []).length) f.push('the sheet no longer names the estimate years it lacks');
  }
  arm(5, 'no forecast, no E column, the reason stays', f);
}
// 6 CENSUS over every name with a block (the issuer's capture names100.mnemonics.json: per key, the fiscal mnemonics the
// newest served block carries a value for), with the page's own row specs
{
  const f = [];
  const cap = JSON.parse(fs.readFileSync(path.join(__dirname, 'names100.mnemonics.json'), 'utf8')).keys;
  const specs = [...(MS.FINANCIAL_SUMMARY_ROWS || []), ...(MS.MARGIN_HISTORY_ROWS || [])];
  let shown = 0, absent = 0, unmapped = 0;
  for (const key of Object.keys(cap)) {
    const have = new Set(cap[key].fiscal_mnemonics);
    for (const sp of specs) {
      if (!sp.mnemonic) unmapped += 1;
      else if (have.has(sp.mnemonic)) shown += 1;
      else absent += 1;
    }
  }
  const nk = Object.keys(cap).length;
  console.log(`CENSUS keys ${nk} rows ${specs.length * nk} shown ${shown} absent ${absent} unmapped ${unmapped}`);
  if (!specs.length) f.push('modelSheet.ts exports no row specs');
  if (unmapped !== 0) f.push(`${unmapped} sheet rows over ${nk} names are hard-coded to no field`);
  arm(6, 'over every name, no sheet row is unmapped', f);
}
const k = results.filter(Boolean).length;
console.log(`THE SHEET IN THE SHAREPOINT SHAPE: ${k} of 6 arms`);
process.exit(k === 6 ? 0 : 1);
