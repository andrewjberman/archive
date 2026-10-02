/**
 * peerwords.cjs -- DSGN_AMGTV1 round 23, AV-zb-1 (issuer 2.0.0_SA_COO~D): THE PEERS ABSENT-COLUMN REASONS ARE IN READER WORDS.
 *
 * Usage (repo root): node <this file>        (portal/ under the cwd is the checkout under test)
 * CTO round-22 analysis @eee9380be7 ruling 1 / section 3 row 1 (FWD-8): the Peers face never says "factor code", "row field",
 * "registry", "comparison map", "R-1" or a category in capitals; each absent column's reason says what the reader is missing and why,
 * in one plain clause (e.g. "Shares outstanding is not reported for these peers"). The served reason may ride a data- attribute.
 * Inputs: the five captured payloads portal/src/pages/SecurityAnalysis/__harness__/tabsFixture.{BA,BABA,COST,HD,SAP}_*.json (peers).
 * Render: round15/checks/_load.cjs (the real PeersTab; hooks return the fixture).
 * Census over the Peers face's VISIBLE text (attributes are not text):
 *   TERMS     /factor code|row field|registr(y|ies)|comparison map|\bR-1\b/i   (anywhere on the Peers face)
 *   CAPITALS  /\b[A-Z]{4,}\b/ in each absent item's reason clause, after the column name (EBIT, EBITDA allowed): RATIOS, THREE
 * Arms:
 *   1  THE CHECKOUT: over 5 fixtures, TERMS 0 and CAPITALS 0, and every served absent column still renders one item
 *      (`data-absent-column`) whose text carries a clause after the column's name.
 *   2  POSITIVE CONTROL: the census reads >= 1 on each planted system phrase (6 of 6) and 0 on a reader-words line.
 *   3  THE SERVED REASON RIDES THE ITEM: each absent item's `data-absent-column-reason` equals the served reason.
 * Prints one line per arm and "THE PEERS ABSENT-COLUMN REASONS ARE IN READER WORDS: <k> of 3 arms"; exit 0 only at 3 of 3.
 */
const fs = require('fs');
const path = require('path');

const SA = 'src/pages/SecurityAnalysis/';
const L = require(path.join(__dirname, '..', '..', 'round15', 'checks', '_load.cjs'));
const KEYS = ['BA_US_Equity', 'BABA_US_Equity', 'COST_US_Equity', 'HD_US_Equity', 'SAP_GY_Equity'];
const FIX = Object.fromEntries(KEYS.map((k) => [k, JSON.parse(fs.readFileSync(path.join(L.base, SA + `__harness__/tabsFixture.${k}.json`), 'utf8'))]));

const TERMS = /factor code|row field|registr(?:y|ies)|comparison map|\bR-1\b/gi;
const CAPS = /\b[A-Z]{4,}\b/g;
// Finance acronyms a reader knows are words, not a category in capitals; CAPITALS reads the reason clause, never the column name.
const ACRONYMS = new Set(['EBIT', 'EBITDA']);
const decode = (s) => String(s).replace(/&amp;/g, '&').replace(/&quot;/g, '"').replace(/&#x27;/g, "'").replace(/&lt;/g, '<').replace(/&gt;/g, '>');

function render(f) {
  L.hookState.impl = { usePeerSet: () => f.peers, useSecurityOverlay: () => f.overlay, useThesisBundle: () => f.thesis, useCollectedChatter: () => undefined };
  return L.render(L.source(SA + 'tabs/PeersTab.tsx').PeersTab, { securityKey: f.security_key });
}
function items(html) {
  const out = [];
  const re = /<li\b([^>]*\bdata-absent-column="([^"]*)"[^>]*)>([\s\S]*?)<\/li>/g;
  let m;
  while ((m = re.exec(html))) {
    const attrs = m[1];
    const r = /data-absent-column-reason="([^"]*)"/.exec(attrs);
    out.push({ column: decode(m[2]), reasonAttr: r ? decode(r[1]) : null, text: L.textOf(m[3]) });
  }
  return out;
}

const arms = [];
let renders = {};
{
  const f = [];
  let nItems = 0;
  for (const k of KEYS) {
    try { renders[k] = render(FIX[k]); } catch (e) { f.push(`${k} RENDER: ${String(e.message).split('\n')[0]}`); continue; }
    const text = L.textOf(renders[k]);
    const t = text.match(TERMS) || [];
    if (t.length) f.push(`${k}: TERMS ${t.length} [${[...new Set(t)].slice(0, 4).join(', ')}]`);
    const served = ((FIX[k].peers.csc_columns || {}).absent || []);
    const its = items(renders[k]);
    nItems += its.length;
    if (its.length !== served.length) f.push(`${k}: ${its.length} absent item(s) for ${served.length} served`);
    for (const it of its) {
      const rest = it.text.startsWith(it.column) ? it.text.slice(it.column.length) : it.text;
      const caps = (rest.match(CAPS) || []).filter((w) => !ACRONYMS.has(w));
      if (caps.length) f.push(`${k} ${it.column}: CAPITALS [${caps.join(', ')}]`);
      if (rest.replace(/[\s:.\-]/g, '').length < 8) f.push(`${k} ${it.column}: no reason clause ("${it.text}")`);
    }
  }
  arms.push(['the checkout: no system term on the Peers face and no capitals in a reason; every absent column keeps a reason', f.length === 0,
    f.length === 0 ? `5 fixtures, ${nItems} absent items, 0 terms` : `${f.length} fault(s): ${f.slice(0, 6).join(' | ')}`]);
}
{
  const f = [];
  const planted = ['no share-count factor code', 'no share-count row field', 'among the 289 registry factors', 'not in the comparison map',
    "R-1's map names this column", 'the solvency category carries only RATIOS'];
  let caught = 0;
  for (const p of planted) {
    const n = (p.match(TERMS) || []).length + (p.match(CAPS) || []).length;
    if (n >= 1) caught += 1; else f.push(`not caught: "${p}"`);
  }
  const clean = 'Shares outstanding is not reported for these peers.';
  if ((clean.match(TERMS) || []).length + (clean.match(CAPS) || []).length) f.push('a reader-words line was flagged');
  arms.push(['POSITIVE CONTROL: each planted system phrase reads >= 1; a reader-words line reads 0', f.length === 0,
    f.length === 0 ? `${caught} of ${planted.length} caught; clean 0` : f.join(' | ')]);
}
{
  const f = [];
  let n = 0;
  for (const k of KEYS) {
    if (!renders[k]) { f.push(`${k}: no render`); continue; }
    const served = Object.fromEntries(((FIX[k].peers.csc_columns || {}).absent || []).map((c) => [c.column, c.reason]));
    for (const it of items(renders[k])) {
      n += 1;
      if ((served[it.column] || null) !== it.reasonAttr) f.push(`${k} ${it.column}: data-absent-column-reason "${it.reasonAttr}" != served "${served[it.column]}"`);
    }
  }
  arms.push(['THE SERVED REASON RIDES THE ITEM: data-absent-column-reason equals the served reason', f.length === 0,
    f.length === 0 ? `${n} of ${n} items carry it` : `${f.length} fault(s): ${f.slice(0, 3).join(' | ')}`]);
}

let pass = 0;
for (const [n, ok, d] of arms) { if (ok) pass += 1; console.log(`${ok ? 'ARM PASS' : 'ARM FAIL'} ${n} :: ${d}`); }
console.log(`THE PEERS ABSENT-COLUMN REASONS ARE IN READER WORDS: ${pass} of 3 arms`);
process.exit(pass === 3 ? 0 : 1);
