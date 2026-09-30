/**
 * AV-e-2 AC2 -- WHERE THE TEAM'S CASE IS NOT SERVED, THE WINDOW SAYS SO IN WORDS AND INVENTS NOTHING.
 *
 * Input: Valero's served /thesis bundle (model.team_cases base/upside/downside ABSENT), captured at the cut.
 * Arms, all must hold:
 *   A  an element carrying data-team-case="base" and data-team-case-state="ABSENT" is present, and its visible text is a
 *      plain sentence naming the research team (contains "research team") with no figure (no digit).
 *   B  the machine draft still follows: the count of data-drafted-sentence equals the served recommendation's sentence
 *      count (5), and the machine-draft author line (data-recommendation-author="machine-draft") is kept.
 *   C  a bundle carrying no model.team_cases at all (the pre-vv-2 payload) still renders the window (no throw), with the
 *      same 5 sentences and the ABSENT sentence.
 */
const L = require('./_load.cjs');
const vlo = L.fixture('thesisBundle.VLO_US_Equity.json');
let ThesisCardDetail;
try {
  ({ ThesisCardDetail } = L.source('src/pages/SecurityAnalysis/components/ThesisCards.tsx'));
} catch (e) {
  console.log('LOAD FAIL components/ThesisCards.tsx :: ' + String(e && e.message).split('\n')[0]);
}
const render = (b) => {
  try {
    return typeof ThesisCardDetail === 'function' ? L.render(ThesisCardDetail, { sectionId: 'recommendation', bundle: b }) : '';
  } catch (e) {
    return 'THROW ' + String(e && e.message).split('\n')[0];
  }
};
const recCount = (vlo.drafted_sections.find((s) => s.section_id === 'recommendation') || { sentences: [] }).sentences.length;
const absentText = (html) => {
  const at = html.search(/data-team-case="base"[^>]*data-team-case-state="ABSENT"|data-team-case-state="ABSENT"[^>]*data-team-case="base"/);
  if (at < 0) return null;
  return L.textOf(L.innerOf(html.slice(html.lastIndexOf('<', at)), 'data-team-case', 'base') || '');
};
const results = [];
const h1 = render(vlo);
{
  const t = absentText(h1);
  results.push(['A ABSENT in words, no figure', t !== null && /research team/i.test(t) && !/\d/.test(t), `text=${JSON.stringify((t || '').slice(0, 120))}`]);
}
{
  const n = L.attrValues(h1, 'data-drafted-sentence').length;
  const author = L.attrValues(h1, 'data-recommendation-author').map((a) => a.value);
  results.push(['B the machine draft still follows', n === recCount && author.includes('machine-draft'), `sentences=${n}/${recCount} author=[${author.join(',')}]`]);
}
{
  const bare = JSON.parse(JSON.stringify(vlo));
  if (bare.model) delete bare.model.team_cases;
  const h2 = render(bare);
  const n = L.attrValues(h2, 'data-drafted-sentence').length;
  const t = absentText(h2);
  results.push(['C a payload without team_cases still renders', !h2.startsWith('THROW') && n === recCount && t !== null, `throw=${h2.startsWith('THROW')} sentences=${n} absent_sentence=${t !== null}`]);
}
let pass = 0;
for (const [n, ok, d] of results) {
  console.log(`ARM ${ok ? 'PASS' : 'FAIL'} ${n} :: ${d}`);
  if (ok) pass += 1;
}
console.log(`TEAM CASE ABSENT: ${pass} of ${results.length} arms`);
process.exit(pass === results.length ? 0 : 1);
