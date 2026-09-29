/**
 * AV-t-2 AC2 -- EACH HEADER CARD'S WINDOW LISTS ITS FIGURES, SERVED OR NAMED AS NOT CARRIED.
 *
 * Input: Valero's served /overlay bundle (as AC1). Renders the named export
 * `HeaderCardDetail` of portal/src/pages/SecurityAnalysis/components/HeaderCards.tsx -- the body
 * the card's window shows -- with props { cardKey, bundle }.
 *
 * Arms, all must hold:
 *   A  financials: data-card-figure="enterprise_value" and ="net_debt", both
 *      data-card-figure-state="SERVED", each with non-empty visible text.
 *   B  market_features: beta SERVED; volatility NOT_CARRIED (VLO's payload carries no volatility).
 *   C  trading_technicals: trend NOT_CARRIED; avg_volume and short_interest SERVED.
 *   D  price: price, market_cap, avg_volume all SERVED.
 *   E  no window's visible text carries a vendor mnemonic.
 */
const L = require('./_load.cjs');

const vlo = L.fixture('overlay.VLO_US_Equity.json');
let HeaderCardDetail;
try {
  ({ HeaderCardDetail } = L.source('src/pages/SecurityAnalysis/components/HeaderCards.tsx'));
} catch (e) {
  console.log('LOAD FAIL components/HeaderCards.tsx :: ' + String(e && e.message).split('\n')[0]);
}
const MNEMONIC = /\b[A-Z][A-Z0-9]*_[A-Z0-9_]+\b/;

function figures(html) {
  const keys = L.attrValues(html, 'data-card-figure').map((a) => a.value);
  const states = L.attrValues(html, 'data-card-figure-state').map((a) => a.value);
  const map = {};
  keys.forEach((k, i) => {
    const inner = L.innerOf(html, 'data-card-figure', k);
    map[k] = { state: states[i], text: L.textOf(inner || '') };
  });
  return map;
}

const want = {
  financials: { enterprise_value: 'SERVED', net_debt: 'SERVED' },
  market_features: { beta: 'SERVED', volatility: 'NOT_CARRIED' },
  trading_technicals: { trend: 'NOT_CARRIED', avg_volume: 'SERVED', short_interest: 'SERVED' },
  price: { price: 'SERVED', market_cap: 'SERVED', avg_volume: 'SERVED' },
};

const results = [];
const htmls = {};
for (const [card, figs] of Object.entries(want)) {
  const html = typeof HeaderCardDetail === 'function' ? L.render(HeaderCardDetail, { cardKey: card, bundle: vlo }) : '';
  htmls[card] = html;
  const got = figures(html);
  const bad = Object.entries(figs).filter(([k, st]) => !got[k] || got[k].state !== st || got[k].text.length === 0);
  results.push([`${card} window`, html.length > 0 && bad.length === 0, `figures=[${Object.keys(got).map((k) => k + ':' + got[k].state).join(',')}] wrong=[${bad.map((b) => b[0]).join(',')}]`]);
}
{
  const hits = Object.entries(htmls)
    .map(([c, h]) => [c, (L.textOf(h).match(MNEMONIC) || [])[0]])
    .filter(([, m]) => m);
  results.push(['no vendor mnemonic in any window', hits.length === 0 && Object.values(htmls).every((h) => h.length > 0), `hits=[${hits.map((h) => h.join(':')).join(',')}]`]);
}

let pass = 0;
for (const [name, ok, detail] of results) {
  console.log(`ARM ${ok ? 'PASS' : 'FAIL'} ${name} :: ${detail}`);
  if (ok) pass += 1;
}
console.log(`CARD WINDOWS: ${pass} of ${results.length} arms`);
process.exit(pass === results.length ? 0 : 1);
