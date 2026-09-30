/**
 * AV-e-2 AC1 -- THE RECOMMENDATION WINDOW LEADS WITH THE RESEARCH TEAM'S CASE WHERE IT IS SERVED.
 *
 * Input: INTU's served /thesis bundle (model.team_cases base/upside/downside SERVED, currency null, "not stated in the
 * pack"), captured from lib/research/api/scoped_amgt.read_thesis_bundle('INTU_US_Equity') at the cut. Renders
 * ThesisCardDetail({ sectionId: 'recommendation', bundle }) from components/ThesisCards.tsx.
 *
 * Arms, all must hold:
 *   A  an element carrying data-team-case="base" and data-team-case-state="SERVED" comes BEFORE the first
 *      data-drafted-sentence (the team's case leads the machine draft).
 *   B  its visible text carries the team's Base table as written: every EPS / Multiple / Price / Return value of the served
 *      table for 2026E (23.22, 16.0x, 371, -4.7%), the words "as written in the team's pack", and "research team".
 *   C  the window's visible text carries no storage path and no run of 15+ digits (the citation's report_key and report_id
 *      are not printed), and no currency code or symbol is placed on the team's figures (the pack states none).
 */
const L = require('./_load.cjs');
const intu = L.fixture('thesisBundle.INTU_US_Equity.json');
let ThesisCardDetail;
try {
  ({ ThesisCardDetail } = L.source('src/pages/SecurityAnalysis/components/ThesisCards.tsx'));
} catch (e) {
  console.log('LOAD FAIL components/ThesisCards.tsx :: ' + String(e && e.message).split('\n')[0]);
}
const html = typeof ThesisCardDetail === 'function' ? L.render(ThesisCardDetail, { sectionId: 'recommendation', bundle: intu }) : '';
const results = [];
{
  const team = html.search(/data-team-case="base"[^>]*data-team-case-state="SERVED"|data-team-case-state="SERVED"[^>]*data-team-case="base"/);
  const firstSentence = html.indexOf('data-drafted-sentence');
  results.push(['A the team Base leads', team >= 0 && (firstSentence < 0 || team < firstSentence), `team_at=${team} first_sentence_at=${firstSentence}`]);
}
const teamInner = (() => {
  const at = html.indexOf('data-team-case="base"');
  if (at < 0) return '';
  return L.textOf(L.innerOf(html.slice(html.lastIndexOf('<', at)), 'data-team-case', 'base') || '');
})();
{
  const want = ['23.22', '16.0x', '371', '-4.7%'];
  const missing = want.filter((w) => !teamInner.includes(w));
  const text = L.textOf(html);
  const ok = missing.length === 0 && /as written in the team's pack/i.test(text) && /research team/i.test(text);
  results.push(['B the table as written, labelled as the team\'s', ok, `missing=[${missing.join(',')}] as_written=${/as written in the team's pack/i.test(text)} research_team=${/research team/i.test(text)}`]);
}
{
  const c = L.rawCensus(html);
  const currencyOnTeam = /\b(USD|EUR|GBP|GBp|HKD|JPY|CAD)\b|\$/.test(teamInner);
  results.push(['C no path, no id, no invented currency', html.length > 0 && c.storage_path === 0 && c.long_digits === 0 && !currencyOnTeam, `storage_path=${c.storage_path} ${JSON.stringify(c.storage_path_first)} long_digits=${c.long_digits} currency_on_team=${currencyOnTeam}`]);
}
let pass = 0;
for (const [n, ok, d] of results) {
  console.log(`ARM ${ok ? 'PASS' : 'FAIL'} ${n} :: ${d}`);
  if (ok) pass += 1;
}
console.log(`TEAM CASE LEADS: ${pass} of ${results.length} arms`);
process.exit(pass === results.length ? 0 : 1);
