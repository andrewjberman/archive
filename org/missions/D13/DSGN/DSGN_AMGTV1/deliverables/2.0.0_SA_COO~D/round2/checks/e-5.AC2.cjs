/**
 * AV-e-5 AC2 -- A BLOOMBERG TICKER WITH A LITERAL SLASH READS WITHOUT IT; EVERYTHING ELSE ABOUT THE ROW IS UNCHANGED.
 *
 * Input: the served Trending x Price payload (32 rows; "BP/ LN" and "NG/ LN" carry the slash). Renders RankedList.
 * Arms, all must hold:
 *   A  the BP row's data-row-lead reads "BP LN" and the NG row's reads "NG LN"; no lead contains "/".
 *   B  every other row's lead is its served ticker exactly (30 of 30), rows stay in producer order, and every row still
 *      carries data-row-name-state (32 of 32).
 *   C  a row carrying name "BP p.l.c." leads with the name and shows its ticker as "BP LN" (data-row-ticker).
 */
const L = require('./_load.cjs');
const served = L.fixture('rankings.TRENDING_PRICE.json');
const rows = served.rows;
const { RankedList } = L.source('src/pages/SecurityAnalysis/components/RankedList.tsx');
const render = (rs) => L.render(RankedList, { rows: rs, starredTickers: new Set(), resolution: served.resolution, onToggleStar: () => {}, onSelectSecurity: () => {}, isLoading: false, readError: null, rankingStatus: 'SERVED' });
const texts = (html, attr) => {
  const out = [];
  let from = 0;
  for (;;) {
    const at = html.indexOf(attr, from);
    if (at < 0) break;
    out.push(L.textOf(L.innerOf(html.slice(html.lastIndexOf('<', at)), attr) || ''));
    from = at + 1;
  }
  return out;
};
const results = [];
const h = render(rows);
const leads = texts(h, 'data-row-lead');
const iBP = rows.findIndex((x) => x.ticker === 'BP/ LN');
const iNG = rows.findIndex((x) => x.ticker === 'NG/ LN');
results.push(['A the slash does not reach the face', leads[iBP] === 'BP LN' && leads[iNG] === 'NG LN' && leads.every((t) => !t.includes('/')), `bp=${JSON.stringify(leads[iBP])} ng=${JSON.stringify(leads[iNG])} with_slash=${leads.filter((t) => t.includes('/')).length}`]);
{
  const others = rows.map((x, i) => [x, i]).filter(([x]) => !x.ticker.includes('/'));
  const same = others.filter(([x, i]) => leads[i] === x.ticker).length;
  const states = L.attrValues(h, 'data-row-name-state').length;
  results.push(['B every other row unchanged', same === others.length && leads.length === rows.length && states === rows.length, `unchanged=${same}/${others.length} leads=${leads.length}/${rows.length} name_states=${states}/${rows.length}`]);
}
{
  const hn = render(rows.map((x, i) => (i === iBP ? { ...x, name: 'BP p.l.c.' } : x)));
  const l = texts(hn, 'data-row-lead')[iBP];
  const tk = texts(hn, 'data-row-ticker');
  results.push(['C a named row shows its ticker without the slash', l === 'BP p.l.c.' && tk.includes('BP LN') && !tk.some((t) => t.includes('/')), `lead=${JSON.stringify(l)} tickers=${JSON.stringify(tk)}`]);
}
let pass = 0;
for (const [n, ok, d] of results) {
  console.log(`ARM ${ok ? 'PASS' : 'FAIL'} ${n} :: ${d}`);
  if (ok) pass += 1;
}
console.log(`SLASH KEY: ${pass} of ${results.length} arms`);
process.exit(pass === results.length ? 0 : 1);
