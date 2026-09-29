/**
 * AV-e-3 AC1 -- EVERY MONEY FIGURE IN THE HEADER PRINTS ONE WAY: ITS OWN SERVED CURRENCY CODE, THEN THE AMOUNT.
 *
 * Input: Valero's served /overlay bundle (every money figure carries currency USD), captured at the cut. Renders the
 * header cards (HeaderCards) and each card's window (HeaderCardDetail) from components/HeaderCards.tsx.
 * Money figures: price (PX_LAST), market_cap (CUR_MKT_CAP), enterprise_value (CURR_ENTP_VAL), net_debt (NET_DEBT).
 *
 * Arms, all must hold:
 *   A  as served: every money figure's visible text (card lead and window row) matches "USD <amount>" (the code, a space,
 *      then the number with an optional K/M/B/T scale), and no "$" appears anywhere in the cards or windows.
 *   B  each money figure's currency set to HKD on the payload: every one prints "HKD <amount>" -- the code comes from the
 *      figure's OWN served currency, never a default.
 *   C  a money figure whose served currency is null prints its amount and the words "currency not stated", never a code
 *      or a symbol it was not served.
 */
const L = require('./_load.cjs');
const vlo = L.fixture('overlay.VLO_US_Equity.json');
let mod = {};
try {
  mod = L.source('src/pages/SecurityAnalysis/components/HeaderCards.tsx');
} catch (e) {
  console.log('LOAD FAIL components/HeaderCards.tsx :: ' + String(e && e.message).split('\n')[0]);
}
const MONEY = { PX_LAST: 'price', CUR_MKT_CAP: 'market_cap', CURR_ENTP_VAL: 'enterprise_value', NET_DEBT: 'net_debt' };
const CARD_OF = { price: 'price', market_cap: 'price', enterprise_value: 'financials', net_debt: 'financials' };
const withCurrency = (ccy) => ({
  ...vlo,
  header_figures: vlo.header_figures.map((f) => (MONEY[f.mnemonic] ? { ...f, currency: ccy } : f)),
});
const figureTexts = (bundle) => {
  const out = {};
  for (const key of Object.values(MONEY)) {
    const html = typeof mod.HeaderCardDetail === 'function' ? L.render(mod.HeaderCardDetail, { cardKey: CARD_OF[key], bundle }) : '';
    const inner = L.innerOf(html, 'data-card-figure', key);
    out[key] = inner === null ? null : L.textOf(inner);
  }
  const face = typeof mod.HeaderCards === 'function' ? L.render(mod.HeaderCards, { bundle }) : '';
  return { out, all: Object.values(out).join(' | ') + ' | ' + L.textOf(face) };
};
const amount = '[0-9][0-9.,]*\\s?[KMBT]?';
const results = [];
{
  const { out, all } = figureTexts(vlo);
  const bad = Object.entries(out).filter(([, t]) => t === null || !new RegExp('\\bUSD\\s' + amount).test(t));
  results.push(['A USD <amount> everywhere, no $', bad.length === 0 && !all.includes('$'), `bad=[${bad.map((b) => b[0] + ':' + JSON.stringify(b[1])).join(', ')}] dollar_sign=${all.includes('$')}`]);
}
{
  const { out } = figureTexts(withCurrency('HKD'));
  const bad = Object.entries(out).filter(([, t]) => t === null || !new RegExp('\\bHKD\\s' + amount).test(t) || /USD|\$/.test(t));
  results.push(['B the code is the figure\'s own', bad.length === 0, `bad=[${bad.map((b) => b[0] + ':' + JSON.stringify(b[1])).join(', ')}]`]);
}
{
  const { out } = figureTexts(withCurrency(null));
  const bad = Object.entries(out).filter(([, t]) => t === null || !/currency not stated/i.test(t) || /\bUSD\b|\bHKD\b|\$/.test(t));
  results.push(['C no currency served -> said in words', bad.length === 0, `bad=[${bad.map((b) => b[0] + ':' + JSON.stringify(b[1])).join(', ')}]`]);
}
let pass = 0;
for (const [n, ok, d] of results) {
  console.log(`ARM ${ok ? 'PASS' : 'FAIL'} ${n} :: ${d}`);
  if (ok) pass += 1;
}
console.log(`ONE MONEY FORMAT: ${pass} of ${results.length} arms`);
process.exit(pass === results.length ? 0 : 1);
