/**
 * AV-t-3 AC1 -- THE THESIS TAB AT REST IS THE PRINCIPAL CHART, THEN THREE CARDS.
 *
 * Input: Valero's served Thesis bundle, captured from
 * lib/research/api/scoped_amgt.read_thesis_bundle('VLO_US_Equity') at the cut (drafting SERVED from
 * the 10-K filed 2026-02-25; investment_thesis 5 sentences, risks 3, recommendation 5).
 *
 * Arms, all must hold:
 *   A  an element carrying data-thesis-principal-chart comes first; after it, exactly 3 elements
 *      carry data-thesis-card, in the order investment_thesis, risks, recommendation, each with a
 *      data-thesis-card-lead whose visible text is non-empty.
 *   B  the face carries no <details> (the sentences and their evidence live in each card's window).
 *   C  the face's visible text carries no filing accession number (no run of 15 or more digits).
 */
const L = require('./_load.cjs');

const vlo = L.fixture('thesisBundle.VLO_US_Equity.json');
L.hookState.data = vlo;
L.hookState.isLoading = false;
L.stubSource('src/pages/SecurityAnalysis/components/IdentityLine.tsx', { IdentityLine: () => null });
const { ThesisTab } = L.source('src/pages/SecurityAnalysis/tabs/ThesisTab.tsx');

const html = L.render(ThesisTab, { securityKey: 'VLO_US_Equity' });
const results = [];
{
  const chart = html.indexOf('data-thesis-principal-chart');
  const cards = L.attrValues(html, 'data-thesis-card');
  const order = cards.map((c) => c.value);
  const want = ['investment_thesis', 'risks', 'recommendation'];
  const leads = [];
  let from = 0;
  for (;;) {
    const at = html.indexOf('data-thesis-card-lead', from);
    if (at < 0) break;
    leads.push(L.textOf(L.innerOf(html.slice(html.lastIndexOf('<', at)), 'data-thesis-card-lead') || ''));
    from = at + 1;
  }
  const ok =
    chart >= 0 &&
    cards.length === 3 &&
    want.every((k, i) => order[i] === k) &&
    cards.every((c) => c.index > chart) &&
    leads.length === 3 &&
    leads.every((t) => t.length > 0);
  results.push(['A chart first, then three cards in order', ok, `chart_at=${chart} cards=[${order.join(',')}] leads=${leads.length}`]);
}
{
  const n = (html.match(/<details\b/g) || []).length;
  results.push(['B no <details> on the face', n === 0, `details=${n}`]);
}
{
  const hit = (L.textOf(html).match(/\d{15,}/) || [])[0];
  results.push(['C no accession number on the face', !hit, `hit=${hit || 'none'}`]);
}

let pass = 0;
for (const [name, ok, detail] of results) {
  console.log(`ARM ${ok ? 'PASS' : 'FAIL'} ${name} :: ${detail}`);
  if (ok) pass += 1;
}
console.log(`THESIS THREE CARDS: ${pass} of ${results.length} arms`);
process.exit(pass === results.length ? 0 : 1);
