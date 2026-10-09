/**
 * r68.cjs -- DSGN_AMGTV1 round 68 (issuer 2.0.0_SA_COO~D1): ONE SERVED FIELD PER MEASURE IN THE TILE AND THE PEERS SUBJECT ROW.
 *
 * Usage (repo root of the checkout under test): node <this file>    (portal/ under the cwd is the checkout under test)
 * CTO round-67 analysis @a06920d917 section 2 item 1 (FWD-27): the Enterprise Value tile and the Peers subject row read the SAME
 * served EV field with one rule; "--" only where that field is empty, and then in both places. The page already does this for
 * Mkt Cap (AV-zzr-1: the subject's cap is the header's CUR_MKT_CAP only). This check binds the same rule for every subject cell
 * whose measure the header also shows as a tile: Price (PX_LAST) and EV (CURR_ENTP_VAL). The 992 HK walk (round 67, shot 042)
 * showed the EV tile "--" and the subject row "60.91B currency not stated" -- the row fell back to the peer set's own subject EV.
 * Inputs: portal/src/pages/SecurityAnalysis/__harness__/tabsFixture.BA_US_Equity.json. The peer set's `subject` is given Price, EV
 * and P/E (NTM) figures (a member's own where one carries it, else fixed stand-ins), as 992 HK's peer set carries its own, so a
 * fallback is visible.
 * Render: round15/checks/_load.cjs (the real PeersTab with fixture hooks).
 * Arms:
 *   1  HEADER SERVED: with PX_LAST and CURR_ENTP_VAL served, the subject Price and EV cells read the tile's own strings
 *      (StatTile formatStatValue, 'price' and 'currency-millions', the figure's served currency -- null here, so "not stated").
 *   2  HEADER EMPTY: with the header serving neither figure while the peer set's subject carries both, both cells read "--".
 *   3  NO OVERLAY: with no overlay at all, both cells read "--".
 *   4  BOUNDED: a subject column with no header tile (the first such column the subject carries) still prints the table's value.
 *   5  PLANTED: the comparator rejects a figure where "--" is wanted and "--" where a figure is wanted; a correct row passes.
 * Prints one line per arm and "ROUND 68 ONE FIELD PER MEASURE: <k> of 5 arms"; exit 0 only at 5 of 5.
 */
const fs = require('fs');
const path = require('path');

const SA = 'src/pages/SecurityAnalysis/';
const L = require(path.join(__dirname, '..', '..', '..', '2.0.0_SA_COO~D', 'round15', 'checks', '_load.cjs'));
const FIX = JSON.parse(fs.readFileSync(path.join(L.base, SA + '__harness__/tabsFixture.BA_US_Equity.json'), 'utf8'));
const KEY = FIX.security_key;
const ST = L.source(SA + 'components/StatTile.tsx');
const CT = L.source(SA + 'cscTable.ts');

const fig = (ov, mn) => ((ov && ov.header_figures) || []).find((f) => f && f.mnemonic === mn);
const PX = fig(FIX.overlay, 'PX_LAST');
const EV = fig(FIX.overlay, 'CURR_ENTP_VAL');
const TILE = {
  Price: PX ? ST.formatStatValue(Number(PX.value), 'price', PX.currency || null) : null,
  EV: EV ? ST.formatStatValue(Number(EV.value), 'currency-millions', EV.currency || null) : null,
};

// The peer set with a subject that carries the members' own Price and EV fields (the 992 HK shape).
const columns = CT.buildCscTable(FIX.peers, null).columns;
const colBy = (code) => columns.find((c) => c.code === code && c.state === 'PRESENT_CARRIED' && c.memberField);
const setPath = (obj, dotted, v) => {
  const ks = dotted.split('.');
  let o = obj;
  for (const k of ks.slice(0, -1)) { if (typeof o[k] !== 'object' || o[k] === null) o[k] = {}; o = o[k]; }
  o[ks[ks.length - 1]] = v;
};
const getPath = (obj, dotted) => dotted.split('.').reduce((o, k) => (o == null ? undefined : o[k]), obj);
const PEERS = JSON.parse(JSON.stringify(FIX.peers));
const planted = [];
// The BA members carry no price or ev field, so fixed figures stand in (60910 is 992 HK's served subject EV, in millions).
const STAND_IN = { price: 111.11, ev: 60910, ey_ntm: 39.28 };
for (const code of ['price', 'ev', 'ey_ntm']) {
  const c = colBy(code);
  if (!c) continue;
  const donor = (PEERS.members || []).map((m) => getPath(m, c.memberField)).find((v) => typeof v === 'number');
  setPath(PEERS.subject, c.memberField, typeof donor === 'number' ? donor : STAND_IN[code]);
  if (code !== 'ey_ntm') planted.push(code);
}

const cellsOf = (tr) => Array.from(tr.matchAll(/<td\b[^>]*>([\s\S]*?)<\/td>/g)).map((m) => L.textOf(m[1]));
function subjectRow(html) {
  const thead = html.slice(html.indexOf('<thead'), html.indexOf('</thead>'));
  const heads = Array.from(thead.matchAll(/<th\b[^>]*>([\s\S]*?)<\/th>/g)).map((m) => L.textOf(m[1]));
  const at = html.indexOf('data-csc-row="subject"');
  if (at < 0) return { error: 'no data-csc-row="subject" row' };
  const tr = html.slice(html.lastIndexOf('<tr', at), html.indexOf('</tr>', at));
  return { heads, cells: cellsOf(tr) };
}
const cellUnder = (r, name) => {
  const i = r.heads.findIndex((h) => h === name || h.startsWith(name + ' '));
  return i < 0 ? undefined : r.cells[i];
};
function faults(got, want) {
  const f = [];
  for (const name of Object.keys(want)) {
    const g = got[name];
    if (g === undefined) { f.push(`HEAD: no "${name}" column`); continue; }
    if (want[name] === '--') { if (g !== '--') f.push(`FALLBACK: ${name} reads "${g}" where the header serves nothing (want "--")`); continue; }
    if (g === '--' || g === '') f.push(`MISSING: ${name} reads "${g}" (want "${want[name]}")`);
    else if (g !== want[name]) f.push(`VALUE: ${name} reads "${g}" (want the tile's "${want[name]}")`);
  }
  return f;
}
function render(overlay) {
  L.hookState.impl = {
    usePeerSet: () => PEERS,
    useSecurityOverlay: () => overlay,
    useThesisBundle: () => FIX.thesis,
    useCollectedChatter: () => undefined,
  };
  const m = L.source(SA + 'tabs/PeersTab.tsx');
  return subjectRow(L.render(m.PeersTab, { securityKey: KEY }));
}
const pick = (r) => ({ Price: cellUnder(r, 'Price'), EV: cellUnder(r, 'EV') });

const arms = [];
const arm = (name, fn) => {
  const f = [];
  let detail = '';
  try { detail = fn(f) || ''; } catch (e) { f.push('RENDER: ' + String(e.message).split('\n')[0]); }
  arms.push([name, f.length === 0, f.length === 0 ? detail || 'holds' : f.join(' | ')]);
};

arm(`HEADER SERVED: the subject Price and EV read the tiles' "${TILE.Price}" and "${TILE.EV}"`, (f) => {
  if (!TILE.Price || !TILE.EV) { f.push('INPUT: the fixture overlay carries no PX_LAST or CURR_ENTP_VAL'); return; }
  if (planted.length !== 2) f.push(`INPUT: the subject could not be given both fields (planted ${planted.join(',') || 'none'})`);
  const r = render(FIX.overlay);
  if (r.error) f.push(r.error); else f.push(...faults(pick(r), TILE));
});
arm('HEADER EMPTY: with the header serving neither figure, the subject Price and EV read "--" though the peer set carries both', (f) => {
  if (planted.length !== 2) { f.push(`INPUT: planted ${planted.join(',') || 'none'}`); return; }
  const ov = { ...FIX.overlay, header_figures: (FIX.overlay.header_figures || []).filter((x) => !['PX_LAST', 'CURR_ENTP_VAL'].includes(x.mnemonic)) };
  const r = render(ov);
  if (r.error) f.push(r.error); else f.push(...faults(pick(r), { Price: '--', EV: '--' }));
});
arm('NO OVERLAY: with no overlay, the subject Price and EV read "--"', (f) => {
  const r = render(undefined);
  if (r.error) f.push(r.error); else f.push(...faults(pick(r), { Price: '--', EV: '--' }));
});
arm('BOUNDED: a subject column with no header tile keeps the table\'s served value', (f) => {
  const TILED = new Set(['price', 'mkt_val_sec', 'ev', 'ey']);
  const shown = columns.filter((c) => c.state === 'PRESENT_CARRIED' && c.memberField && !TILED.has(c.code));
  const c = shown.find((x) => typeof getPath(PEERS.subject, x.memberField) === 'number');
  if (!c) return 'no untiled column carried by the subject in this fixture (arm vacuous by input, recorded)';
  const ov = { ...FIX.overlay, header_figures: [] };
  const r = render(ov);
  if (r.error) { f.push(r.error); return; }
  const label = c.displayLabel || c.column;
  const g = cellUnder(r, label);
  if (g === undefined) f.push(`HEAD: no "${label}" column`);
  else if (g === '--') f.push(`OVERREACH: "${label}" reads "--" though the subject carries it and no tile shows it`);
  return `"${label}" reads "${g}"`;
});
arm('PLANTED: a fallback figure and a missing tile figure are rejected; a correct row passes', (f) => {
  const want = { Price: 'USD 204.80', EV: '--' };
  if (faults({ Price: 'USD 204.80', EV: '--' }, want).length) f.push('a correct row is rejected');
  const M = [['FALLBACK', { Price: 'USD 204.80', EV: '60.91B currency not stated' }], ['MISSING', { Price: '--', EV: '--' }]];
  let caught = 0;
  for (const [cls, got] of M) { if (faults(got, want).some((x) => x.startsWith(cls + ':'))) caught += 1; else f.push(`mutant ${cls} not rejected`); }
  return `${caught} of ${M.length} rejected`;
});

let pass = 0;
for (const [n, ok, d] of arms) { if (ok) pass += 1; console.log(`${ok ? 'ARM PASS' : 'ARM FAIL'} ${n} :: ${d}`); }
console.log(`ROUND 68 ONE FIELD PER MEASURE: ${pass} of 5 arms`);
process.exit(pass === 5 ? 0 : 1);
