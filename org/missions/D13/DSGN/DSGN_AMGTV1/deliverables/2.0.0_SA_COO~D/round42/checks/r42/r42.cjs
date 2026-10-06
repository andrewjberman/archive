/**
 * r42.cjs -- DSGN_AMGTV1 round 42 issuer CHECK (2.0.0_SA_COO~D): THE HEADER SHOWS A MISSING FIGURE'S REASON, ITS TOOLTIP CARRIES THE
 * FULL VALUE, AND THE EXEC EMPTY STATE READS IN PLAIN WORDS.
 *
 * Usage (from the directory whose portal/ is the checkout under test):
 *   cd "$(git rev-parse --show-toplevel)" && node "org/missions/D13/DSGN/DSGN_AMGTV1/deliverables/2.0.0_SA_COO~D/round42/checks/r42/r42.cjs"
 *
 * Why: ledger/CTO_COUNTERSIGN_COMPLETION_GRADES_ROUND41.md @f5d6919117, ROUND 42 items 1-3:
 *   1 FWD-4: a missing header figure prints the producer's served reason in its place, in words (rulings 2; FWD-27 permits it).
 *     The producer (lib/research/api/scoped_amgt.py `_header_figures`) serves, for each of the seven with no stored value, an entry
 *     {mnemonic, value: null, reason: "<sentence>"}; short interest's reasoned entry uses SHORT_INT_RATIO.
 *   2 FWD-13: the tooltip carries the full-precision value, formatted with separators and its unit, with no float noise
 *     (ruling 3: "for example USD 161,867,780,096").
 *   3 FWD-27: the Exec tab's "No officer list has been published for this name yet:No officer list could be shown ..." becomes
 *     plain words (a missing space, a run-on and a repeated sentence today).
 *
 * Arms (each prints its evidence; exit 0 only on all of them):
 *   1 MISSING FIGURES SHOW THEIR SERVED REASON: HeaderCards on a ROG SW-shaped bundle (3 served, 4 served as null + reason) renders
 *     7 key-figure tiles; each of price, beta, average volume and short interest is a tile holding its label and its served reason
 *     verbatim, with data-card-figure-state other than SERVED and no figure printed.
 *   2 THE TOOLTIP CARRIES THE FULL VALUE: on a USD bundle the market-cap tooltip reads "USD 161,867,780,096" (served
 *     161867780096.00003, ABSOLUTE); the enterprise-value tooltip reads "CHF 306,930.58319 million" (served 306930.58319, MILLIONS);
 *     the price tooltip reads "USD 193.56"; no rendered text carries the float noise "00003".
 *   3 THE EXEC EMPTY STATE IS PLAIN WORDS: in tabs/ExecManagementTab.tsx no "yet:" survives, the "No officer list has been published
 *     for this name yet" message carries no interpolated reason in the same sentence, and the served reason is still shown.
 *   4 KEEP: a served figure still prints its short face value (ROG market cap "CHF 281B" with "as of"); a figure served as null with
 *     NO reason prints no tile (FWD-27, an unconnected field prints no line); every tooltip keeps data-full-value and data-mnemonic;
 *     no vendor mnemonic appears in rendered text.
 *   5 PLANTED: the graders refuse a missing tile, a reason rendered as a number, a noisy full value, and an Exec "yet:" line.
 * Renders the REAL HeaderCards.tsx through round15/checks/_load.cjs (DataTooltip stubbed to print its rows); no network; writes nothing.
 */
'use strict';
const fs = require('fs');
const path = require('path');
const L = require(path.join(__dirname, '..', '..', '..', 'round15', 'checks', '_load.cjs'));

const React = L.React;
const DT = { DataTooltip: ({ header, rows }) => React.createElement('div', { 'data-tt': '' },
  React.createElement('span', { 'data-tt-header': '' }, header),
  ...(rows || []).map((r, i) => React.createElement('span', { key: i, 'data-tt-row': r.label }, `${r.label}: ${r.value}`))) };
L.stubSource('src/components/DataTooltip', DT);
L.stubSource('src/components/DataTooltip.tsx', DT);

const VINT = '2026-10-05T13:34:39Z';
const fig = (mnemonic, value, unit, currency, extra) => Object.assign({ scope: 'HEADER', fiscal_year: null, mnemonic, value, unit,
  sign: null, basis: { mnemonic, definition: '' }, vintage: VINT, source: 'bloomberg', currency }, extra || {});
const R = {
  PX_LAST: 'Bloomberg returned no value for price for this name in the latest stored pull.',
  EQY_BETA: 'Bloomberg returned no value for beta for this name in the latest stored pull.',
  VOLUME_AVG_30D: 'Average volume is not in the latest stored pull for this name.',
  SHORT_INT_RATIO: 'Short interest is not in the latest stored pull for this name.',
};
const ROG = { header_figures: [
  fig('CRNCY', 'CHF', 'TEXT (string field)', null),
  fig('CUR_MKT_CAP', 280836583190, 'ABSOLUTE (full currency units)', 'CHF'),
  fig('NET_DEBT', 17715, 'MILLIONS', 'CHF'),
  fig('CURR_ENTP_VAL', 306930.58319, 'MILLIONS', 'CHF'),
  fig('PX_LAST', null, null, null, { reason: R.PX_LAST, source: null }),
  fig('EQY_BETA', null, null, null, { reason: R.EQY_BETA, source: null }),
  fig('VOLUME_AVG_30D', null, null, null, { reason: R.VOLUME_AVG_30D, source: null }),
  fig('SHORT_INT_RATIO', null, null, null, { reason: R.SHORT_INT_RATIO, source: null }),
] };
const USD = { header_figures: [
  fig('PX_LAST', 193.56, 'USD', 'USD'),
  fig('CUR_MKT_CAP', 161867780096.00003, 'ABSOLUTE (full currency units)', 'USD'),
  fig('CURR_ENTP_VAL', 306930.58319, 'MILLIONS', 'CHF'),
  fig('NET_DEBT', 26960, 'MILLIONS', 'USD'),
  fig('EQY_BETA', 1.36, 'RATIO', null),
  fig('VOLUME_AVG_30D', null, null, null),   // null with NO reason: prints no tile (KEEP)
] };

const portal = path.join(process.cwd(), 'portal');
let HC;
try { HC = L.source('src/pages/SecurityAnalysis/components/HeaderCards.tsx'); }
catch (e) { console.log('LOADER ERROR: HeaderCards.tsx :: ' + String(e && e.message).split('\n')[0]); process.exit(3); }

const decode = (s) => s.replace(/&amp;/g, '&').replace(/&quot;/g, '"').replace(/&#x27;/g, "'").replace(/&lt;/g, '<').replace(/&gt;/g, '>');
const text = (html) => decode(html.replace(/<[^>]+>/g, ' ')).replace(/\s+/g, ' ').trim();
function tiles(html) {
  // each top-level key-figure tile: <div ... data-card-figure="key" ...> ... up to the next tile or the end
  const out = [];
  const re = /<div[^>]*data-card-figure="([^"]+)"[^>]*>/g;
  const idx = [];
  let m;
  while ((m = re.exec(html))) idx.push({ key: m[1], at: m.index, open: m[0] });
  for (let i = 0; i < idx.length; i += 1) {
    const body = html.slice(idx[i].at, i + 1 < idx.length ? idx[i + 1].at : html.length);
    const st = /data-card-figure-state="([^"]+)"/.exec(idx[i].open);
    out.push({ key: idx[i].key, state: st ? st[1] : null, body, text: text(body) });
  }
  return out;
}
const LABEL = { PX_LAST: /price/i, EQY_BETA: /beta/i, VOLUME_AVG_30D: /average volume/i, SHORT_INT_RATIO: /short interest/i };

function gradeMissing(ts) {
  const f = [];
  if (ts.length !== 7) f.push(`${ts.length} tiles (7 wanted: 3 served + 4 with a served reason)`);
  for (const [mn, reason] of Object.entries(R)) {
    const t = ts.find((x) => x.text.includes(reason));
    if (!t) { f.push(`${mn}: no tile carries its served reason`); continue; }
    if (!LABEL[mn].test(t.text)) f.push(`${mn}: the reason's tile has no plain label`);
    if (t.state === 'SERVED') f.push(`${mn}: tile marked SERVED`);
    const rest = t.text.replace(reason, '');
    if (/\d/.test(rest.replace(/\b\d{1,2}(st|nd|rd|th)\b|\b20\d\d\b/g, ''))) f.push(`${mn}: a figure is printed beside the reason (${rest.slice(0, 60)})`);
  }
  return f;
}
function gradeFull(html) {
  const f = [];
  const tt = text(html);
  for (const want of ['USD 161,867,780,096', 'CHF 306,930.58319 million', 'USD 193.56']) if (!tt.includes(want)) f.push(`tooltip lacks "${want}"`);
  if (/00003/.test(tt)) f.push('float noise "00003" is rendered');
  return f;
}
function gradeExec(src) {
  const f = [];
  if (/yet:/.test(src)) f.push('"yet:" survives');
  const msgLines = src.split('\n').filter((l) => l.includes('No officer list has been published for this name yet'));
  if (msgLines.length === 0) f.push('the "No officer list has been published for this name yet" message is gone');
  for (const l of msgLines) if (/\$\{/.test(l)) f.push('the message interpolates a reason into the same sentence');
  if (!/dossierReasonWords\(/.test(src)) f.push('the served reason is no longer shown');
  return f;
}

const arms = [];
let rogHtml = ''; let usdHtml = '';
try { rogHtml = L.render(HC.HeaderCards, { bundle: ROG }); } catch (e) { rogHtml = ''; arms.push(['RENDER', false, 'ROG render threw: ' + String(e.message).split('\n')[0]]); }
try { usdHtml = L.render(HC.HeaderCards, { bundle: USD }); } catch (e) { usdHtml = ''; arms.push(['RENDER', false, 'USD render threw: ' + String(e.message).split('\n')[0]]); }
const rogTiles = tiles(rogHtml);
{
  const f = gradeMissing(rogTiles);
  arms.push(['MISSING FIGURES SHOW THEIR SERVED REASON (FWD-4)', f.length === 0, f.length ? f.join(' | ') : `7 tiles; 4 of 4 reasons in place, each with its label, none SERVED, no figure`]);
}
{
  const f = gradeFull(usdHtml);
  arms.push(['THE TOOLTIP CARRIES THE FULL VALUE, FORMATTED (FWD-13)', f.length === 0, f.length ? f.join(' | ') : 'USD 161,867,780,096; CHF 306,930.58319 million; USD 193.56; no float noise']);
}
const execRel = 'src/pages/SecurityAnalysis/tabs/ExecManagementTab.tsx';
// The issuer's green arm only: CHECK_SRC_OVERRIDE (the loader's own variable) may point this read at a scratch reference.
const execOv = (process.env.CHECK_SRC_OVERRIDE || '').split(';').filter(Boolean).map((p) => [p.slice(0, p.indexOf('=')), p.slice(p.indexOf('=') + 1)])
  .find(([rel]) => rel === execRel);
const execFile = execOv ? execOv[1] : path.join(portal, execRel);
const execSrc = fs.existsSync(execFile) ? fs.readFileSync(execFile, 'utf8') : '';
{
  const f = execSrc ? gradeExec(execSrc) : ['ExecManagementTab.tsx not found'];
  arms.push(['THE EXEC EMPTY STATE IS PLAIN WORDS (FWD-27)', f.length === 0, f.length ? f.join(' | ') : 'no "yet:"; the message is its own sentence; the served reason is still shown']);
}
{
  const f = [];
  const mc = rogTiles.find((t) => /CHF 281B/.test(t.text));
  if (!mc) f.push('ROG market cap face "CHF 281B" missing'); else if (!/as of/i.test(mc.text)) f.push('market cap lost its "as of"');
  const usdTiles = tiles(usdHtml);
  if (usdTiles.some((t) => /average volume/i.test(t.text))) f.push('a null figure with no reason printed a tile');
  if (usdTiles.length !== 5) f.push(`USD bundle: ${usdTiles.length} tiles (5 wanted)`);
  const served = (rogHtml.match(/data-full-value=/g) || []).length;
  if (served < 3) f.push(`data-full-value on ${served} tooltip(s) (3 served figures)`);
  if ((rogHtml.match(/data-mnemonic=/g) || []).length < 3) f.push('data-mnemonic lost');
  const vis = text(rogHtml) + ' ' + text(usdHtml);
  const leaked = ['PX_LAST', 'CUR_MKT_CAP', 'CURR_ENTP_VAL', 'NET_DEBT', 'EQY_BETA', 'VOLUME_AVG_30D', 'SHORT_INT_RATIO'].filter((m) => vis.includes(m));
  if (leaked.length) f.push('vendor mnemonic in rendered text: ' + leaked.join(','));
  arms.push(['KEEP: served faces, no tile for an unreasoned null, data attributes, no mnemonic on the face', f.length === 0, f.length ? f.join(' | ') : 'CHF 281B as of ...; 5 USD tiles; data-full-value + data-mnemonic kept; 0 mnemonics visible']);
}
{
  const f = [];
  const goodTile = (key, txt) => ({ key, state: 'ABSENT', body: '', text: txt });
  const good = [
    goodTile('a', 'MARKET CAP CHF 281B'), goodTile('b', 'ENTERPRISE VALUE CHF 307B'), goodTile('c', 'NET DEBT CHF 17.71B'),
    goodTile('PX_LAST', 'PRICE ' + R.PX_LAST), goodTile('EQY_BETA', 'BETA ' + R.EQY_BETA),
    goodTile('VOLUME_AVG_30D', 'AVERAGE VOLUME ' + R.VOLUME_AVG_30D), goodTile('SHORT_INT_RATIO', 'SHORT INTEREST ' + R.SHORT_INT_RATIO),
  ];
  if (gradeMissing(good).length) f.push('good tiles refused: ' + gradeMissing(good).join(';'));
  if (!gradeMissing(good.slice(0, 6)).length) f.push('a missing tile accepted');
  const numbered = good.map((t) => (t.key === 'EQY_BETA' ? Object.assign({}, t, { text: 'BETA 0.00 ' + R.EQY_BETA }) : t));
  if (!gradeMissing(numbered).length) f.push('a number beside a reason accepted');
  if (!gradeFull('<span>USD 161,867,780,096.00003</span><span>CHF 306,930.58319 million</span><span>USD 193.56</span>').length) f.push('noisy full value accepted');
  if (gradeFull('<span>USD 161,867,780,096</span><span>CHF 306,930.58319 million</span><span>USD 193.56</span>').length) f.push('clean full values refused');
  if (!gradeExec("message={`No officer list has been published for this name yet:${dossierReasonWords(r)}`}").length) f.push('an Exec "yet:" line accepted');
  if (gradeExec("message=\"No officer list has been published for this name yet.\"\ndetail={dossierReasonWords(r, 'x')}").length) f.push('a plain Exec line refused');
  arms.push(['PLANTED: the graders refuse a missing tile, a number beside a reason, a noisy full value and a "yet:" line, and accept the intended forms', f.length === 0, f.length ? f.join(' | ') : '4 of 4 faults refused; 3 of 3 good forms accepted']);
}

const TITLE = 'THE HEADER SHOWS A MISSING FIGURE\'S REASON, ITS TOOLTIP CARRIES THE FULL VALUE, THE EXEC EMPTY STATE READS PLAINLY';
let pass = 0;
for (const [name, ok, ev] of arms) { if (ok) pass += 1; console.log(`ARM ${ok ? 'PASS' : 'FAIL'} ${name} :: ${ev}`); }
console.log(`${TITLE}: ${pass} of ${arms.length} arms`);
process.exit(pass === arms.length && arms.length === 5 ? 0 : 1);
