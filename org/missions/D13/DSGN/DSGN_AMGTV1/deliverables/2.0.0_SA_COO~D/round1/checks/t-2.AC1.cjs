/**
 * AV-t-2 AC1 -- THE HEADER READS AS FOUR CARDS.
 *
 * Input: Valero's served /overlay bundle, captured from
 * lib/research/api/scoped_amgt.read_security_overlay('VLO_US_Equity') at the cut (18 header figures).
 * HeaderBrief and GenerationCaption are stubbed (not this cell's surface).
 *
 * Arms, all must hold:
 *   A  VLO as served: exactly 4 elements carry data-header-card, in the order price, financials,
 *      market_features, trading_technicals; each carries a data-header-card-lead whose visible text
 *      is non-empty; no data-stat-tile remains on the face (the seven tiles are retired).
 *   B  VLO with every header figure removed except the identity scalars (NAME, CRNCY,
 *      CNTRY_OF_DOMICILE, GICS_SECTOR_NAME): still 4 cards, each carrying
 *      data-header-card-state="NOT_CARRIED" and a non-empty lead in words.
 *   C  in both renders, the visible text carries no vendor mnemonic (no token like CURR_ENTP_VAL).
 */
const L = require('./_load.cjs');

const vlo = L.fixture('overlay.VLO_US_Equity.json');
const nothing = () => null;
L.stubSource('src/pages/SecurityAnalysis/components/HeaderBrief.tsx', { HeaderBrief: nothing });
L.stubSource('src/pages/SecurityAnalysis/components/GenerationCaption.tsx', { GenerationCaption: nothing });
const mod = L.source('src/pages/SecurityAnalysis/components/SecurityOverlay.tsx');
const Header = mod.IdentityHeader || mod.SecurityOverlay;

const ORDER = ['price', 'financials', 'market_features', 'trading_technicals'];
const MNEMONIC = /\b[A-Z][A-Z0-9]*_[A-Z0-9_]+\b/;

function leads(html) {
  const out = [];
  let from = 0;
  for (;;) {
    const at = html.indexOf('data-header-card-lead', from);
    if (at < 0) break;
    out.push(L.textOf(L.innerOf(html.slice(html.lastIndexOf('<', at)), 'data-header-card-lead') || ''));
    from = at + 1;
  }
  return out;
}

const results = [];
const htmlA = L.render(Header, { bundle: vlo, onBack: () => {}, onRefresh: () => {} });
{
  const cards = L.attrValues(htmlA, 'data-header-card').map((a) => a.value);
  const ls = leads(htmlA);
  const tiles = L.attrValues(htmlA, 'data-stat-tile').length;
  const ok = cards.length === 4 && ORDER.every((k, i) => cards[i] === k) && ls.length === 4 && ls.every((t) => t.length > 0) && tiles === 0;
  results.push(['A four cards in order, each with a lead, no stat tiles', ok, `cards=[${cards.join(',')}] leads=${ls.length} stat_tiles=${tiles}`]);
}

const KEEP = new Set(['NAME', 'CRNCY', 'CNTRY_OF_DOMICILE', 'GICS_SECTOR_NAME']);
const bare = { ...vlo, header_figures: (vlo.header_figures || []).filter((f) => KEEP.has(f.mnemonic)) };
const htmlB = L.render(Header, { bundle: bare, onBack: () => {}, onRefresh: () => {} });
{
  const cards = L.attrValues(htmlB, 'data-header-card').map((a) => a.value);
  const states = L.attrValues(htmlB, 'data-header-card-state').map((a) => a.value);
  const ls = leads(htmlB);
  const ok = cards.length === 4 && states.length === 4 && states.every((s) => s === 'NOT_CARRIED') && ls.length === 4 && ls.every((t) => t.length > 0);
  results.push(['B no figures carried: four designed not-carried cards', ok, `cards=${cards.length} states=[${states.join(',')}] leads=${ls.length}`]);
}

{
  const hitA = (L.textOf(htmlA).match(MNEMONIC) || [])[0];
  const hitB = (L.textOf(htmlB).match(MNEMONIC) || [])[0];
  results.push(['C no vendor mnemonic in visible text', !hitA && !hitB, `A=${hitA || 'none'} B=${hitB || 'none'}`]);
}

let pass = 0;
for (const [name, ok, detail] of results) {
  console.log(`ARM ${ok ? 'PASS' : 'FAIL'} ${name} :: ${detail}`);
  if (ok) pass += 1;
}
console.log(`HEADER FOUR CARDS: ${pass} of ${results.length} arms`);
process.exit(pass === results.length ? 0 : 1);
