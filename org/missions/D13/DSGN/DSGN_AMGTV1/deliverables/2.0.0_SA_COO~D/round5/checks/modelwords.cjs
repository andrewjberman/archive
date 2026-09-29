/**
 * modelwords.cjs -- DSGN_AMGTV1 round 5, AV-v-4: THE MODEL FACE SAYS WHOSE BASE CASE EACH IS (round-4 analysis s.4 item 4 and
 * ruling 2; ruling 1's divergence tile name; FWD-6, FWD-11).
 *
 * Usage (repo root): node <this file>
 * Renders the Model tab (tabs/ModelTab.tsx) on SAP GY, served fixture under round5/fixtures. Visible text (tags stripped,
 * collapsed <details> included). Every current fixture's rule case carries the served label "Historical-multiple reference"
 * (AMGT-vv-1); the round-4 walk (19:15Z, before AMGT_RESAPP ww-1's redeploy) read a payload WITHOUT it, where the page's
 * fallback head printed a bare "Base case: 159.61 EUR ..." beside the team's "The research team's Base case ..." sentence.
 * So arm 1 renders that shape: the SAME fixture with the base case's `label` removed IN MEMORY (a difference arm; the file
 * is never edited). A served label is printed as served (C-PRESENTATION-ONLY) -- arm 3.
 * "Owned": immediately preceded by "research team's " or by "Opal's rule-based ".
 * Arms:
 *   1  no served label (the walk's shape): every visible "Base case" is owned, and both owners are said
 *   2  the divergence tile (the element carrying data-model-score="divergence") reads "Divergence from consensus forecast",
 *      and "Forecast divergence score" appears nowhere on the face
 *   3  as served (label present): the rule's line still prints the served label "Historical-multiple reference", and every
 *      visible "Base case" is owned
 * Prints one line per arm and "WHOSE BASE CASE: <k> of 3 arms"; exit 0 only at 3 of 3.
 */
const L = require('./_load.cjs');
const served = L.fixture('thesisBundle.SAP_GY_Equity.json');
const unlabelled = JSON.parse(JSON.stringify(served));
// the page's cases block reads the top-level `model_cases` (scoped_amgt._model_cases); `model.cases` mirrors it
for (const c of [unlabelled.model_cases, unlabelled.model && unlabelled.model.cases]) if (c && c.base) delete c.base.label;
const bundles = { SAP_GY_Equity: served, SAP_NOLABEL: unlabelled };
L.hookState.impl = { useThesisBundle: (k) => bundles[k] };
function render(key) {
  try {
    return L.render(L.source('src/pages/SecurityAnalysis/tabs/ModelTab.tsx').ModelTab, { securityKey: key });
  } catch (e) {
    console.log(`${key} render failed: ` + String(e.message).split('\n')[0]);
    return '';
  }
}
function owners(text) {
  const all = [...text.matchAll(/Base case/g)].map((m) => m.index);
  const team = all.filter((i) => text.slice(Math.max(0, i - 16), i) === "research team's ");
  const rule = all.filter((i) => text.slice(Math.max(0, i - 18), i) === "Opal's rule-based ");
  const bare = all.length - team.length - rule.length;
  return { all: all.length, team: team.length, rule: rule.length, bare };
}
const bareHtml = render('SAP_NOLABEL');
const sapHtml = render('SAP_GY_Equity');
const bare = owners(L.textOf(bareHtml));
const sap = owners(L.textOf(sapHtml));
const labelShown = /Historical-multiple reference: /.test(L.textOf(sapHtml));
const tile = L.innerOf(sapHtml, 'data-model-score', 'divergence');
const tileText = tile === null ? null : L.textOf(tile);
const oldName = /Forecast divergence score/.test(L.textOf(sapHtml));
const arms = [
  ['no served label: every Base case says whose, both owners said', bareHtml.length > 0 && bare.bare === 0 && bare.team > 0 && bare.rule > 0,
    `"Base case" x${bare.all}: team ${bare.team}, rule ${bare.rule}, unowned ${bare.bare}`],
  ['the divergence tile reads "Divergence from consensus forecast"', tileText !== null && /Divergence from consensus forecast/.test(tileText) && !oldName,
    `tile ${tileText === null ? 'absent' : `"${tileText.slice(0, 80)}"`}; "Forecast divergence score" on the face ${oldName}`],
  ['as served: the served label printed, every Base case owned', sapHtml.length > 0 && labelShown && sap.bare === 0,
    `served label shown ${labelShown}; "Base case" x${sap.all}: team ${sap.team}, rule ${sap.rule}, unowned ${sap.bare}`],
];
let pass = 0;
for (const [name, ok, detail] of arms) {
  if (ok) pass += 1;
  console.log(`${ok ? 'ARM PASS' : 'ARM FAIL'} ${name} :: ${detail}`);
}
console.log(`WHOSE BASE CASE: ${pass} of ${arms.length} arms`);
process.exit(pass === arms.length ? 0 : 1);
