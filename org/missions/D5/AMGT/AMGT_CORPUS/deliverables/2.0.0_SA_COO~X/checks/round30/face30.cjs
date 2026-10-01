/**
 * face30.cjs -- AMGT_CORPUS round 30, CRPS-af-1 (issuer direct act): THE MODEL FOOTER READS AS A NEUTRAL COUNT
 * (round-29 analysis @499e53e2bf ruling 1: replace "147 of 342 fiscal figure(s) on the block rendered; 0 sheet row(s) not in the
 * pack" with "Showing 147 fiscal figures from the model block"; nothing says "not in the pack" or reads as a loss).
 *
 * Usage (repo root): node <this file>
 * Method: STATIC, DSGN's read-only loader on BA's served /thesis capture, plus in-memory variants. Arms:
 *   1  BA SERVED face: "Showing N fiscal figures from the model block" with N = the data-model-fiscal-cells count; no "of N ...
 *      rendered" phrasing; no "not in the pack"
 *   2  NO-FORECAST variant (model.forecast_figures stripped): the estimate-years line has no "not in the pack"
 *   3  ABSENT-ROW variant (BA's PROF_MARGIN figures removed): the absent-rows footnote still names "Earnings margin", is still
 *      marked data-model-absent-footnote, and presupposes no pack ("the pack does not carry")
 *   4  REGRESSION: round 29's face29.cjs still reads 6 of 6
 * Prints one line per arm and "THE MODEL FOOTER READS NEUTRAL: <k> of 4 arms"; exit 0 only at 4 of 4. No network, writes nothing.
 */
const path = require('path');
const { spawnSync } = require('child_process');
const DSGN = path.join(process.cwd(), 'org/missions/D13/DSGN/DSGN_AMGTV1/deliverables/2.0.0_SA_COO~D/round14/checks');
const R29 = path.join(process.cwd(), 'org/missions/D5/AMGT/AMGT_CORPUS/deliverables/2.0.0_SA_COO~X/checks/round29/face29.cjs');
const L = require(path.join(DSGN, '_load.cjs'));
const S = require(path.join(DSGN, 'surfaces.cjs'));
const K = 'BA_US_Equity';
const clone = (x) => JSON.parse(JSON.stringify(x));
const thesis = S.unwrap(L.fixture('thesisBundle.BA_US_Equity.json'));
let T = thesis;
L.hookState.impl = Object.assign({}, L.hookState.impl, {
  useThesisBundle: (k) => (k === K ? T : (S.bundles[k] || undefined)),
  useModelVersions: () => undefined,
  useModelCompare: () => undefined,
  useInputLedger: () => undefined,
});
const MT = (() => { try { return L.source('src/pages/SecurityAnalysis/tabs/ModelTab.tsx'); } catch (e) { return null; } })();
const render = (b) => { T = b; try { return MT ? L.render(MT.ModelTab, { securityKey: K }) : ''; } catch (e) { return 'RENDER FAILED ' + e.message; } };
const results = [];
const arm = (n, name, fails) => { results.push(fails.length === 0); console.log(`ARM ${n} ${name}: ${fails.length === 0 ? 'PASS' : 'FAIL -- ' + fails.join('; ')}`); };
const LOSS = /\bof \d+ fiscal figure\(s\)|\brendered;|not in the pack|the pack does not carry/i;

{
  const f = [];
  const h = render(clone(thesis));
  if (!h || /^RENDER FAILED/.test(h)) f.push('did not render');
  else {
    const t = L.textOf(h);
    const n = Number(L.attrValues(h, 'data-model-fiscal-cells').map((a) => a.value)[0]);
    if (!t.includes(`Showing ${n} fiscal figures from the model block`)) f.push(`no "Showing ${n} fiscal figures from the model block"`);
    const m = t.match(LOSS);
    if (m) f.push(`the face reads "${m[0]}"`);
  }
  arm(1, 'BA footer is a neutral count', f);
}
{
  const f = [];
  const v = clone(thesis);
  if (v.model) v.model.forecast_figures = [];
  const h = render(v);
  const t = L.textOf(h);
  if (!/2026E/.test(t)) f.push('the no-forecast variant does not name the missing estimate years');
  if (/not in the pack/i.test(t)) f.push('the estimate-years line says "not in the pack"');
  arm(2, 'no-forecast variant: the estimate-years line presupposes no pack', f);
}
{
  const f = [];
  const v = clone(thesis);
  v.fiscal_year_figures = (v.fiscal_year_figures || []).filter((x) => x.mnemonic !== 'PROF_MARGIN');
  const h = render(v);
  const foot = L.innerOf(h, 'data-model-absent-footnote');
  if (foot === null) f.push('no data-model-absent-footnote element');
  else {
    if (!L.textOf(foot).includes('Earnings margin')) f.push('the absent-rows footnote does not name Earnings margin');
    if (/the pack does not carry|not in the pack/i.test(L.textOf(foot))) f.push(`the footnote reads "${L.textOf(foot).slice(0, 60)}"`);
  }
  arm(3, 'absent-row variant: the footnote names the row without presupposing a pack', f);
}
{
  const f = [];
  const r = spawnSync(process.execPath, [R29], { encoding: 'utf8', cwd: process.cwd() });
  if (r.status !== 0 || !(r.stdout || '').includes("THE SHEET READS LIKE THE ANALYST'S: 6 of 6 arms")) f.push(`face29.cjs reads "${((r.stdout || '').trim().split('\n').pop() || '').slice(0, 70)}"`);
  arm(4, "round 29's check still passes", f);
}
const k = results.filter(Boolean).length;
console.log(`THE MODEL FOOTER READS NEUTRAL: ${k} of 4 arms`);
process.exit(k === 4 ? 0 : 1);
