/**
 * AV-e-4 AC2 -- EVERY MODEL LINE STAYS, EACH MISSING LINE SAYS WHY IN ONE SENTENCE, AND THE TEAM'S BASE LEADS THE CASES.
 *
 * Input: Valero's and INTU's served /thesis bundles, captured at the cut. At the base the Model tab renders Valero's 37
 * lines (data-model-row), 18 of them refused (data-model-refused), each reading like
 * "REFUSED -- REVENUE_PER_SH: unit/sign convention is 'NOT-YET-BUILT', not MEASURED".
 *
 * Arms, all must hold:
 *   A  Valero: still 37 data-model-row and 18 data-model-refused -- no line is dropped to make the face clean.
 *   B  Valero: every refused line carries data-model-line-reason="DATA_MISSING" (the data is not there) or
 *      "NOT_SHOWN_YET" (the data is there and the page cannot yet show it), and its visible text is one sentence of at
 *      least five words carrying no vendor mnemonic and no NOT-YET-BUILT.
 *   C  INTU: an element carrying data-model-team-case="base" comes before the first data-model-case (the rule's cases), and
 *      its visible text carries the team's 2026E values as written (23.22, 16.0x, 371) and "as written in the team's pack".
 */
const L = require('./_load.cjs');
const b = { VLO_US_Equity: L.fixture('thesisBundle.VLO_US_Equity.json'), INTU_US_Equity: L.fixture('thesisBundle.INTU_US_Equity.json') };
L.hookState.impl = { useThesisBundle: (k) => b[k] };
const { ModelTab } = L.source('src/pages/SecurityAnalysis/tabs/ModelTab.tsx');
const MNEMONIC = /\b[A-Z][A-Z0-9]*_[A-Z0-9_]+\b/;
const results = [];
const hv = L.render(ModelTab, { securityKey: 'VLO_US_Equity' });
{
  const rows = L.attrValues(hv, 'data-model-row').length;
  const refused = L.attrValues(hv, 'data-model-refused').length;
  results.push(['A every line stays', rows === 37 && refused === 18, `rows=${rows}/37 refused=${refused}/18`]);
}
{
  const reasons = L.attrValues(hv, 'data-model-line-reason');
  const bad = [];
  for (const r of reasons) {
    const t = L.textOf(L.innerOf(hv.slice(hv.lastIndexOf('<', r.index)), 'data-model-line-reason', r.value) || '');
    const words = t.split(/\s+/).filter(Boolean).length;
    if (!['DATA_MISSING', 'NOT_SHOWN_YET'].includes(r.value) || words < 5 || MNEMONIC.test(t) || /NOT-YET-BUILT/.test(t)) bad.push(`${r.value}:${JSON.stringify(t.slice(0, 60))}`);
  }
  results.push(['B each missing line says why, in words', reasons.length === 18 && bad.length === 0, `reasons=${reasons.length}/18 bad=${bad.length} ${bad.slice(0, 2).join(' ; ')}`]);
}
{
  const hi = L.render(ModelTab, { securityKey: 'INTU_US_Equity' });
  const team = hi.indexOf('data-model-team-case="base"');
  const firstCase = hi.indexOf('data-model-case=');
  const t = team < 0 ? '' : L.textOf(L.innerOf(hi.slice(hi.lastIndexOf('<', team)), 'data-model-team-case', 'base') || '');
  const missing = ['23.22', '16.0x', '371'].filter((w) => !t.includes(w));
  const ok = team >= 0 && (firstCase < 0 || team < firstCase) && missing.length === 0 && /as written in the team's pack/i.test(t);
  results.push(['C the team Base leads the cases', ok, `team_at=${team} first_rule_case_at=${firstCase} missing=[${missing.join(',')}] as_written=${/as written in the team's pack/i.test(t)}`]);
}
let pass = 0;
for (const [n, ok, d] of results) {
  console.log(`ARM ${ok ? 'PASS' : 'FAIL'} ${n} :: ${d}`);
  if (ok) pass += 1;
}
console.log(`MODEL LINES AND CASES: ${pass} of ${results.length} arms`);
process.exit(pass === results.length ? 0 : 1);
