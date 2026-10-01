/**
 * face.cjs -- AMGT_CORPUS round 28, CRPS-ad-2: THE MODEL FACE CARRIES ONLY THE TEAM'S SHAPE, AND NEVER CONTRADICTS ITSELF
 * (PRD v0.7 Addendum B: FWD-12 amended -- the score tiles and Opal's rule-based upside/base/downside lines are NOT rendered; the
 * team's Upside/Base/Downside cases still render as the team's. CONTRACT amendment 1 @c7f9fa44fa moves DSGN round-14 analysis
 * ruling 1 here: "the face shows the figure with its label, or the empty sentence, never both" -- CVO v16 k-5 PARTIAL read
 * "No figure, case or estimate is shown in its place" beside "forward EPS (FY1) is -0.828".)
 *
 * Usage (repo root): node <this file>
 * Method: STATIC, through DSGN's read-only loader (_load.cjs) on BA's served /thesis capture (DSGN round14 fixtures, read-only),
 * and in-memory variants of it labelled below. Arms:
 *   1  SERVED face (BA): no score tile (no data-model-scores, no "Robustness score" / "Peer valuation score" / "Divergence from
 *      consensus forecast") and no rule line (no data-model-cases / data-model-case, no "Opal's rule-based", no "Opal's
 *      historical-multiple")
 *   2  ABSENT face (BA with model_status ABSENT): the same two absences
 *   3  TEAM CASES KEPT: both faces still render the three team cases (data-model-team-case base / upside / downside)
 *   4  ONE FACE, PLANTED (BA ABSENT with the team's Base case SERVED in memory: a two-line table): the team's figures show, and
 *      the face does NOT also claim "No figure, case or estimate is shown"; a model-empty sentence, if any, stays on the face
 *   5  ONE FACE, BARE (BA ABSENT with no team cases carried): an empty sentence saying there is no model is on the face and no figure is (no digit inside any data-model-team-case, data-model-case or data-model-score block)
 *   6  WORDS (FWD-20): on every face above, the visible text carries none of "ABSENT", "REFUSED", "not read"
 *   7  NO PRESUPPOSED PACK (COO~D msg 27552): BA's served reasons say there is no pack ("no landed model block for this name";
 *      the team cases' class-A report is missing), so the ABSENT and BARE faces never say a thing is missing "in the research
 *      pack" / "in this pack" -- the words follow the served reason
 *   8  WIRED (FWD-21): BA's served sheet header carries 2026E, 2027E, 2028E, and the served forecasts add at least 17 sheet
 *      cells over the same render with model.forecast_figures stripped
 * Prints one line per arm and "THE MODEL FACE IN THE TEAM'S SHAPE: <k> of 8 arms"; exit 0 only at 8 of 8.
 * No network, no AWS, writes no file.
 */
const path = require('path');
const DSGN = path.join(process.cwd(), 'org/missions/D13/DSGN/DSGN_AMGTV1/deliverables/2.0.0_SA_COO~D/round14/checks');
const L = require(path.join(DSGN, '_load.cjs'));
const S = require(path.join(DSGN, 'surfaces.cjs'));

const K = 'BA_US_Equity';
const EMPTY = /\bno model\b/i; // the empty sentence's subject; its wording is the cell's (arm 7 bars the presupposed pack)
const NO_FIGURE_CLAIM = /No figure, case or estimate is shown/i;
const SCORE_WORDS = /Robustness score|Peer valuation score|Divergence from consensus forecast/;
const RULE_WORDS = /Opal's rule-based|Opal's historical-multiple/;
const BAD_WORDS = /\bABSENT\b|\bREFUSED\b|\bnot read\b/i;
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
const render = (bundle) => { T = bundle; try { return MT ? L.render(MT.ModelTab, { securityKey: K }) : ''; } catch (e) { return 'RENDER FAILED ' + e.message; } };
const blocks = (html, attr) => [...html.matchAll(new RegExp(`<[a-z]+[^>]*\\b${attr}="[^"]*"[^>]*>[\\s\\S]*?</(p|section|div)>`, 'g'))].map((m) => m[0]);

const served = render(clone(thesis));
const absentB = Object.assign(clone(thesis), { model_status: 'ABSENT' });
const absent = render(absentB);
const planted = clone(absentB);
planted.model = planted.model || {};
planted.model.team_cases = Object.assign({}, planted.model.team_cases || {}, {
  base: { status: 'SERVED', table: { 'Revenue': { '2026E': '91,000' }, 'EPS': { '2026E': '4.10' } },
    citation: { report_key: 'research/BA/BA Model.xlsx' }, unit_as_written: 'USD m' },
});
const plantedH = render(planted);
const bare = clone(absentB);
if (bare.model) bare.model.team_cases = null;
const bareH = render(bare);

const results = [];
const arm = (n, name, fails) => { results.push(fails.length === 0); console.log(`ARM ${n} ${name}: ${fails.length === 0 ? 'PASS' : 'FAIL -- ' + fails.join('; ')}`); };
const rendered = (h, label, f) => { if (!h || /^RENDER FAILED/.test(h)) { f.push(`${label} did not render (${(h || 'no source').slice(0, 80)})`); return false; } return true; };
const noTilesNoRules = (h, label, f) => {
  if (!rendered(h, label, f)) return;
  if (/data-model-scores/.test(h) || SCORE_WORDS.test(L.textOf(h))) f.push(`${label}: a score tile is on the face`);
  if (/data-model-cases?\b/.test(h) || RULE_WORDS.test(L.textOf(h))) f.push(`${label}: an Opal rule line is on the face`);
};

{ const f = []; noTilesNoRules(served, 'SERVED face', f); arm(1, 'served face: no score tiles, no rule lines', f); }
{ const f = []; noTilesNoRules(absent, 'ABSENT face', f); arm(2, 'absent face: no score tiles, no rule lines', f); }
{
  const f = [];
  for (const [h, label] of [[served, 'SERVED face'], [absent, 'ABSENT face']]) {
    if (!rendered(h, label, f)) continue;
    const sides = L.attrValues(h, 'data-model-team-case').map((a) => a.value).sort().join(',');
    if (sides !== 'base,downside,upside') f.push(`${label}: team cases ${sides || 'none'}, want base,downside,upside`);
  }
  arm(3, "the team's three cases still render", f);
}
{
  const f = [];
  if (rendered(plantedH, 'PLANTED face', f)) {
    const t = L.textOf(plantedH);
    if (!t.includes('91,000') || !t.includes('4.10')) f.push("the planted team Base figures are not on the face");
    if (NO_FIGURE_CLAIM.test(t)) f.push('the face shows a team figure AND claims "No figure, case or estimate is shown"');
  }
  arm(4, 'one face: a shown figure is never beside the no-figure claim', f);
}
{
  const f = [];
  if (rendered(bareH, 'BARE face', f)) {
    if (!EMPTY.test(L.textOf(bareH))) f.push('no empty sentence ("no model ...") on the bare face');
    for (const attr of ['data-model-team-case', 'data-model-case', 'data-model-score']) {
      for (const b of blocks(bareH, attr)) if (/\d/.test(L.textOf(b))) f.push(`a figure inside ${attr} on the bare face: "${L.textOf(b).slice(0, 60)}"`);
    }
  }
  arm(5, 'bare absent face: the empty sentence and no figure', f);
}
{
  const f = [];
  for (const [h, label] of [[served, 'SERVED'], [absent, 'ABSENT'], [plantedH, 'PLANTED'], [bareH, 'BARE']]) {
    if (!h || /^RENDER FAILED/.test(h)) continue;
    const m = L.textOf(h).match(BAD_WORDS);
    if (m) f.push(`${label} face reads "${m[0]}"`);
  }
  arm(6, 'no internal state words on any face', f);
}
{
  const f = [];
  for (const [h, label] of [[absent, 'ABSENT'], [bareH, 'BARE']]) {
    if (!h || /^RENDER FAILED/.test(h)) { f.push(`${label} face did not render`); continue; }
    const m = L.textOf(h).match(/\bin (the research|this) pack\b/i);
    if (m) f.push(`${label} face presupposes a pack: "${m[0]}"`);
  }
  arm(7, 'the absent faces follow the served reason, not a presupposed pack', f);
}
{
  const f = [];
  if (rendered(served, 'SERVED face', f)) {
    const sheetHtml = L.innerOf(served, 'data-model-sheet', '') || '';
    const head = (/<thead[^>]*>([\s\S]*?)<\/thead>/.exec(sheetHtml) || [, ''])[1];
    for (const ey of ['2026E', '2027E', '2028E']) if (!L.textOf(head).includes(ey)) f.push(`the sheet header lacks ${ey}`);
    // BA serves 17 forecast figures on sheet rows (EPS, BVPS, DPS, Dividend yield, EBITDA x 3; P/E x 2): the same render with
    // the forecasts stripped must carry at least that many fewer sheet cells
    const noF = clone(thesis);
    if (noF.model) noF.model.forecast_figures = [];
    const bare0 = render(noF);
    const cells = (h) => ((L.innerOf(h, 'data-model-sheet', '') || '').match(/data-model-cell/g) || []).length;
    const d = cells(served) - cells(bare0);
    if (d < 17) f.push(`the served forecasts add ${d} sheet cells, want at least 17`);
  }
  arm(8, "BA's sheet shows the served 2026E-2028E columns", f);
}
// 9 READABLE FORECASTS (added at the drain after the real run, issuer direct act): the served consensus figures carry float
// noise ("-0.8280000000000001", "4342.833333333333"), which pushed BA's sheet past the page edge. No number visible in the sheet
// carries more than 4 decimals, and each forecast cell still carries its full served value in data-full-value.
{
  const f = [];
  if (rendered(served, 'SERVED face', f)) {
    const sheetHtml = L.innerOf(served, 'data-model-sheet', '') || '';
    const long = (L.textOf(sheetHtml).match(/-?\d+\.\d{5,}/g) || []);
    if (long.length) f.push(`${long.length} sheet number(s) print more than 4 decimals, e.g. ${long.slice(0, 3).join(', ')}`);
    const fc = (thesis.model && thesis.model.forecast_figures || []).find((x) => x.mnemonic === 'BEST_EPS' && Number(x.fiscal_year) === 2026);
    if (fc && !sheetHtml.includes(`data-full-value="${String(fc.value)}"`)) f.push(`BEST_EPS 2026's full value ${fc.value} is not carried in data-full-value`);
  }
  arm(9, 'forecast cells read at the sheet\'s precision, full value kept', f);
}
const k = results.filter(Boolean).length;
console.log(`THE MODEL FACE IN THE TEAM'S SHAPE: ${k} of 9 arms`);
process.exit(k === 9 ? 0 : 1);
