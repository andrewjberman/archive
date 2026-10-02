/**
 * liveclass.cjs -- DSGN_AMGTV1 round 26, AV-zd-1 (issuer 2.0.0_SA_COO~D): THE LIVE SERVED ABSENT REASONS ARE CLASSED.
 *
 * Usage (repo root): node <this file>        (portal/ under the cwd is the checkout under test)
 * Found on the issuer's round-25 close walk 20261002T094604Z (VLO Peers): 5 of 12 absent columns render the generic `unmapped`
 * clause, because RESAPP AMGT-ak-3 (B2, lib/research/peers/csc_plain_reasons.py) now SERVES five reasons with registry labels in
 * place of factor codes, and AV-zc-2's class table keys the old served text. The five live strings are printed below exactly as
 * `plain_absent_reason(column)` returns them at CLOUD 4720f6975a+ (python, local registry). Each keeps its predecessor's class.
 * Arms:
 *   1  THE CHECKOUT, live strings: BA's fixture with the five columns' reasons replaced by the live strings -> 0 items `unmapped`,
 *      every item a reader clause (no bare "not available").
 *   2  SAME CLASS AS BEFORE: each live string's class equals the class the page gives that column's previous served string.
 *   3  THE GAP STILL SHOWS: an unknown served reason still renders `unmapped`.
 * Prints one line per arm and "THE LIVE SERVED ABSENT REASONS ARE CLASSED: <k> of 3 arms"; exit 0 only at 3 of 3.
 */
const fs = require('fs');
const path = require('path');

const SA = 'src/pages/SecurityAnalysis/';
const L = require(path.join(__dirname, '..', '..', 'round15', 'checks', '_load.cjs'));
const FIX = JSON.parse(fs.readFileSync(path.join(L.base, SA + '__harness__/tabsFixture.BA_US_Equity.json'), 'utf8'));
const LIVE = {
  'Cash': "'Cash to Market Value' is a ratio; no absolute cash level",
  'P/E 2027': "the value category carries trailing ('Earnings Yield') and NTM ('Earnings Yield NTM') only -- no second-forward-year estimate at any grain",
  'Debt/Equity': "the registry carries only 'Leverage' (category solvency) and states no numerator or denominator, so reading it AS debt/equity would be inferred, not measured; 'Debt to Assets' is debt to ASSETS",
  '5-yr growth EBIT': "no EBIT growth measure at any window ('EBIT to Enterprise Value' is a yield, 'EBIT Estimate Revisions (45D)' an estimate revision)",
  '5-yr growth FCF': "no FCF growth measure at any window ('Free Cash Flow Yield' and 'Free Cash Flow to Enterprise Value NTM' are yields)",
};
const BARE = /^\s*(is )?not available for these peers\.?\s*$/i;
const decode = (s) => String(s).replace(/&amp;/g, '&').replace(/&quot;/g, '"').replace(/&#x27;/g, "'").replace(/&lt;/g, '<').replace(/&gt;/g, '>');

function render(f) {
  L.hookState.impl = { usePeerSet: () => f.peers, useSecurityOverlay: () => f.overlay, useThesisBundle: () => f.thesis, useCollectedChatter: () => undefined };
  return L.render(L.source(SA + 'tabs/PeersTab.tsx').PeersTab, { securityKey: f.security_key });
}
function items(html) {
  const out = {};
  const re = /<li\b([^>]*\bdata-absent-column="([^"]*)"[^>]*)>([\s\S]*?)<\/li>/g;
  let m;
  while ((m = re.exec(html))) {
    const cls = /data-absent-reason-class="([^"]*)"/.exec(m[1]);
    const column = decode(m[2]);
    const text = L.textOf(m[3]);
    out[column] = { cls: cls ? decode(cls[1]) : null, clause: (text.startsWith(column) ? text.slice(column.length) : text).replace(/^[\s:.\-]+/, '').trim() };
  }
  return out;
}
const withReasons = (map) => {
  const f = JSON.parse(JSON.stringify(FIX));
  for (const a of f.peers.csc_columns.absent) if (Object.prototype.hasOwnProperty.call(map, a.column)) a.reason = map[a.column];
  return f;
};

const arms = [];
let live = null;
let before = null;
{
  const f = [];
  try {
    live = items(render(withReasons(LIVE)));
    before = items(render(FIX));
    for (const col of Object.keys(LIVE)) {
      const it = live[col];
      if (!it) { f.push(`${col}: no item`); continue; }
      if (it.cls === 'unmapped' || !it.cls) f.push(`${col}: class ${it.cls}`);
      if (!it.clause || BARE.test(it.clause)) f.push(`${col}: no reader clause`);
    }
    const unm = Object.values(live).filter((x) => x.cls === 'unmapped').length;
    if (unm) f.push(`${unm} item(s) unmapped over the whole list`);
  } catch (e) { f.push('RENDER: ' + String(e.message).split('\n')[0]); }
  arms.push(['the checkout: the five live served reasons are classed, 0 unmapped', f.length === 0, f.length === 0 ? '5 of 5 classed' : f.join(' | ')]);
}
{
  const f = [];
  if (!live || !before) f.push('no render');
  else for (const col of Object.keys(LIVE)) {
    if (!before[col] || !live[col]) { f.push(`${col}: missing`); continue; }
    if (live[col].cls !== before[col].cls) f.push(`${col}: live class ${live[col].cls} != previous ${before[col].cls}`);
  }
  arms.push(['SAME CLASS AS BEFORE: each live string keeps its predecessor\'s class', f.length === 0, f.length === 0 ? '5 of 5 equal' : f.join(' | ')]);
}
{
  const f = [];
  try {
    const it = items(render(withReasons({ 'Cash': 'a reason the producer has never served' }))).Cash;
    if (!it || it.cls !== 'unmapped') f.push(`an unknown reason reads class ${it && it.cls}`);
  } catch (e) { f.push('RENDER: ' + String(e.message).split('\n')[0]); }
  arms.push(['THE GAP STILL SHOWS: an unknown served reason renders unmapped', f.length === 0, f.length === 0 ? 'unmapped' : f.join(' | ')]);
}

let pass = 0;
for (const [n, ok, d] of arms) { if (ok) pass += 1; console.log(`${ok ? 'ARM PASS' : 'ARM FAIL'} ${n} :: ${d}`); }
console.log(`THE LIVE SERVED ABSENT REASONS ARE CLASSED: ${pass} of 3 arms`);
process.exit(pass === 3 ? 0 : 1);
