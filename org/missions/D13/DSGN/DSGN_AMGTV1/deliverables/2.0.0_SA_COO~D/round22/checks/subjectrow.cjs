/**
 * subjectrow.cjs -- DSGN_AMGTV1 round 22, AV-z-2 (issuer 2.0.0_SA_COO~D): THE PEERS SUBJECT ROW CARRIES THE HEADER'S SERVED PRICE AND EV.
 *
 * Usage (repo root): node <this file>        (portal/ under the cwd is the checkout under test)
 * CTO round-21 analysis @e14de1769c section 3A row A2 (FWD-8): the Peers subject row's Price and EV are filled from the header's
 * served values when the header carries them (it showed "--"). The header's served figures are the overlay's `header_figures`
 * (PX_LAST for Price; CURR_ENTP_VAL, in millions, for EV -- the header cards' own mnemonics, constants.ts HEADER_CARD_DEFS).
 * THE CONTRACT: in the row `data-csc-row="subject"`, the cell under the "Price" column reads formatValue(PX_LAST) and the cell under
 * the "EV" column reads formatValue(CURR_ENTP_VAL), where formatValue is the column's own rule in PeersTab.tsx (|v| >= 1000 ->
 * en-US grouping, 0 decimals; else 2 decimals) -- so the subject reads like its members. With no header figure served, both cells
 * stay "--" (the page invents nothing; C-PRESENTATION-ONLY).
 * Inputs: portal/src/pages/SecurityAnalysis/__harness__/tabsFixture.BA_US_Equity.json (peers + overlay; PX_LAST 204.8,
 * CURR_ENTP_VAL 193510.78 -> "204.80", "193,511").
 * Render: round15/checks/_load.cjs (the real PeersTab; hooks return the fixture: usePeerSet, useSecurityOverlay, useThesisBundle).
 * Arms:
 *   1  THE CHECKOUT: with the overlay served, the subject row's Price and EV cells read the two expected strings.
 *   2  NO INVENTION: with an overlay that carries no header_figures (and with no overlay at all), both cells read "--".
 *   3  PLANTED: the comparator rejects a "--" cell (MISSING) and a value 10% off (VALUE); a correct row passes.
 * Prints one line per arm and "THE PEERS SUBJECT ROW CARRIES THE HEADER'S PRICE AND EV: <k> of 3 arms"; exit 0 only at 3 of 3.
 */
const fs = require('fs');
const path = require('path');

const SA = 'src/pages/SecurityAnalysis/';
const L = require(path.join(__dirname, '..', '..', 'round15', 'checks', '_load.cjs'));
const FIX = JSON.parse(fs.readFileSync(path.join(L.base, SA + '__harness__/tabsFixture.BA_US_Equity.json'), 'utf8'));
const KEY = FIX.security_key;

const formatValue = (v) => (Math.abs(v) >= 1000 ? v.toLocaleString('en-US', { maximumFractionDigits: 0 }) : v.toFixed(2));
const fig = (ov, mn) => ((ov && ov.header_figures) || []).find((f) => f && f.mnemonic === mn);
const PX = fig(FIX.overlay, 'PX_LAST');
const EV = fig(FIX.overlay, 'CURR_ENTP_VAL');
// RE-ANCHOR (DSGN_AMGTV1 round 67, AV-zzr-1, row D1-W141-S1; issuer 2.0.0_SA_COO~D1): the page now prints the subject's money cells
// through StatTile's formatStatValue with the figure's own served currency ('price' for PX_LAST; 'currency-millions' for
// CURR_ENTP_VAL, served in millions), the same formatter the header tiles use (FWD-27, one format per measure). The claim is unchanged:
// the subject row carries the header's served Price and EV. Only the expected strings are derived through the page's one formatter.
// Was: formatValue(v) -> "204.80" / "193,511".
const ST = L.source(SA + 'components/StatTile.tsx');
const WANT = {
  Price: PX ? ST.formatStatValue(Number(PX.value), 'price', PX.currency || null) : null,
  EV: EV ? ST.formatStatValue(Number(EV.value), 'currency-millions', EV.currency || null) : null,
};
void formatValue;

const cellsOf = (tr) => Array.from(tr.matchAll(/<td\b[^>]*>([\s\S]*?)<\/td>/g)).map((m) => L.textOf(m[1]));
function subjectCells(html) {
  const thead = html.slice(html.indexOf('<thead'), html.indexOf('</thead>'));
  const heads = Array.from(thead.matchAll(/<th\b[^>]*>([\s\S]*?)<\/th>/g)).map((m) => L.textOf(m[1]));
  const at = html.indexOf('data-csc-row="subject"');
  if (at < 0) return { error: 'no data-csc-row="subject" row' };
  const tr = html.slice(html.lastIndexOf('<tr', at), html.indexOf('</tr>', at));
  const cells = cellsOf(tr);
  const out = {};
  for (const name of ['Price', 'EV']) {
    const i = heads.findIndex((h) => h === name || h.startsWith(name + ' '));
    out[name] = i < 0 ? undefined : cells[i];
  }
  return { out, heads };
}
function faults(got, want) {
  const f = [];
  for (const name of ['Price', 'EV']) {
    const g = got[name];
    if (g === undefined) { f.push(`HEAD: no "${name}" column`); continue; }
    if (want[name] === '--') { if (g !== '--') f.push(`INVENTED: ${name} reads "${g}" with nothing served`); continue; }
    if (g === '--' || g === '') f.push(`MISSING: ${name} reads "${g}" (want "${want[name]}")`);
    else if (g !== want[name]) f.push(`VALUE: ${name} reads "${g}" (want "${want[name]}")`);
  }
  return f;
}
function render(overlay) {
  L.hookState.impl = {
    usePeerSet: () => FIX.peers,
    useSecurityOverlay: () => overlay,
    useThesisBundle: () => FIX.thesis,
    useCollectedChatter: () => undefined,
  };
  const m = L.source(SA + 'tabs/PeersTab.tsx');
  return L.render(m.PeersTab, { securityKey: KEY });
}

const arms = [];
{
  const f = [];
  if (!WANT.Price || !WANT.EV) f.push('INPUT: the fixture overlay carries no PX_LAST or CURR_ENTP_VAL');
  else {
    try {
      const r = subjectCells(render(FIX.overlay));
      if (r.error) f.push(r.error); else f.push(...faults(r.out, WANT));
    } catch (e) { f.push('RENDER: ' + String(e.message).split('\n')[0]); }
  }
  arms.push([`the checkout: the subject row reads Price "${WANT.Price}" and EV "${WANT.EV}" from the header's served figures`, f.length === 0,
    f.length === 0 ? 'both cells filled' : f.join(' | ')]);
}
{
  const f = [];
  try {
    const bare = { ...FIX.overlay, header_figures: [] };
    for (const [label, ov] of [['empty header_figures', bare], ['no overlay', undefined]]) {
      const r = subjectCells(render(ov));
      if (r.error) f.push(`${label}: ${r.error}`); else f.push(...faults(r.out, { Price: '--', EV: '--' }).map((x) => `${label}: ${x}`));
    }
  } catch (e) { f.push('RENDER: ' + String(e.message).split('\n')[0]); }
  arms.push(['NO INVENTION: with no header figure served the subject Price and EV read "--"', f.length === 0,
    f.length === 0 ? '2 of 2 renders read "--"' : f.join(' | ')]);
}
{
  const f = [];
  const want = { Price: '204.80', EV: '193,511' };
  if (faults({ Price: '204.80', EV: '193,511' }, want).length) f.push('a correct row is rejected');
  const M = [['MISSING', { Price: '--', EV: '193,511' }], ['VALUE', { Price: '225.28', EV: '193,511' }]];
  let caught = 0;
  for (const [cls, got] of M) { if (faults(got, want).some((x) => x.startsWith(cls + ':'))) caught += 1; else f.push(`mutant ${cls} not rejected`); }
  arms.push(['PLANTED: a "--" cell and a 10%-off value are rejected; a correct row passes', f.length === 0,
    f.length === 0 ? `${caught} of ${M.length} rejected` : f.join(' | ')]);
}

let pass = 0;
for (const [n, ok, d] of arms) { if (ok) pass += 1; console.log(`${ok ? 'ARM PASS' : 'ARM FAIL'} ${n} :: ${d}`); }
console.log(`THE PEERS SUBJECT ROW CARRIES THE HEADER'S PRICE AND EV: ${pass} of 3 arms`);
process.exit(pass === 3 ? 0 : 1);
