/**
 * reasonclass.cjs -- DSGN_AMGTV1 round 24, AV-zc-2 (issuer 2.0.0_SA_COO~D): EACH ABSENT COLUMN STATES ITS REASON IN READER WORDS.
 *
 * Usage (repo root): node <this file>        (portal/ under the cwd is the checkout under test)
 * CTO round-23 analysis @876dfcadb8 ruling 1 / section 3 row 1 (FWD-16 with FWD-8): the "Absent columns (N)" disclosure gives each
 * column its REASON in reader words -- one plain clause per reason class of R-1's served absent reasons -- never the bare
 * "<Column> is not available for these peers", and never system vocabulary. Examples from the ruling: "the data source does not
 * report share counts for these peers"; "this measure is not computed for banks"; "not yet matched to a data field".
 * THE CONTRACT on each `<li data-absent-column=...>` item:
 *   - it carries `data-absent-reason-class="<class>"`, the page's class for the served reason; a served reason the page has no
 *     class for carries `unmapped` and a generic reader clause (so a new R-1 reason shows up as a gap, never as a code);
 *   - its visible text after the column name is ONE clause for its class: two items of one class read the same clause;
 *   - the clause is not "is not available for these peers" alone, carries none of the system terms (peerwords TERMS: factor code,
 *     row field, registry, comparison map, R-1), no capitals word of 4+ letters other than EBIT/EBITDA, and none of round 22's
 *     code classes (snake_case, _Equity, .json, ABSENT/UNMAPPED, UPPER_SNAKE);
 *   - `data-absent-column-reason` keeps the served reason.
 * Inputs: the five captured payloads __harness__/tabsFixture.{BA,BABA,COST,HD,SAP}_*.json; their served absent reasons are one
 * global map (11 distinct reasons over 12 columns, identical in all five).
 * Arms:
 *   1  THE CHECKOUT: 60 items over 5 fixtures; 0 `unmapped`; every distinct served reason has a class; one clause per class; no
 *      bare "not available" and no system term or code in a clause.
 *   2  THE GAP SHOWS: a planted unknown served reason ("a reason R-1 has never served") renders class `unmapped` with a non-empty
 *      reader clause carrying no system term.
 *   3  PLANTED: the comparator rejects a bare "not available" clause, a clause with "registry", and two clauses for one class.
 * Prints one line per arm and "EACH ABSENT COLUMN STATES ITS REASON IN READER WORDS: <k> of 3 arms"; exit 0 only at 3 of 3.
 */
const fs = require('fs');
const path = require('path');

const SA = 'src/pages/SecurityAnalysis/';
const L = require(path.join(__dirname, '..', '..', 'round15', 'checks', '_load.cjs'));
const KEYS = ['BA_US_Equity', 'BABA_US_Equity', 'COST_US_Equity', 'HD_US_Equity', 'SAP_GY_Equity'];
const FIX = Object.fromEntries(KEYS.map((k) => [k, JSON.parse(fs.readFileSync(path.join(L.base, SA + `__harness__/tabsFixture.${k}.json`), 'utf8'))]));

const TERMS = /factor code|row field|registr(?:y|ies)|comparison map|\bR-1\b/i;
const CODES = /\b[a-z]+_[a-z0-9_]+\b|_Equity\b|\.json\b|\b(?:ABSENT|UNMAPPED)\b|\b[A-Z][A-Z0-9]*_[A-Z0-9_]+\b/;
const ACRONYMS = new Set(['EBIT', 'EBITDA']);
const BARE = /^\s*(is )?not available for these peers\.?\s*$/i;
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
    const a = m[1];
    const cls = /data-absent-reason-class="([^"]*)"/.exec(a);
    const rsn = /data-absent-column-reason="([^"]*)"/.exec(a);
    const column = decode(m[2]);
    const text = L.textOf(m[3]);
    const clause = (text.startsWith(column) ? text.slice(column.length) : text).replace(/^[\s:.\-]+/, '').trim();
    out.push({ column, cls: cls ? decode(cls[1]) : null, reason: rsn ? decode(rsn[1]) : null, clause });
  }
  return out;
}
function clauseFaults(it) {
  const f = [];
  if (!it.clause || it.clause.replace(/[\s.]/g, '').length < 8) f.push(`${it.column}: no reason clause`);
  else if (BARE.test(it.clause)) f.push(`${it.column}: bare "not available"`);
  if (TERMS.test(it.clause)) f.push(`${it.column}: system term in "${it.clause.slice(0, 70)}"`);
  if (CODES.test(it.clause)) f.push(`${it.column}: code in "${it.clause.slice(0, 70)}"`);
  const caps = (it.clause.match(/\b[A-Z]{4,}\b/g) || []).filter((w) => !ACRONYMS.has(w));
  if (caps.length) f.push(`${it.column}: capitals [${caps.join(', ')}]`);
  return f;
}
function classFaults(all) {
  const f = [];
  const byClass = new Map();
  for (const it of all) {
    if (!it.cls) { f.push(`${it.column}: no data-absent-reason-class`); continue; }
    if (!byClass.has(it.cls)) byClass.set(it.cls, new Set());
    byClass.get(it.cls).add(it.clause);
  }
  for (const [c, s] of byClass) if (s.size > 1) f.push(`class ${c}: ${s.size} different clauses`);
  return { f, classes: byClass.size };
}

const arms = [];
{
  const f = [];
  const all = [];
  const served = new Set();
  for (const k of KEYS) {
    for (const a of (FIX[k].peers.csc_columns || {}).absent || []) served.add(a.reason);
    let h;
    try { h = render(FIX[k]); } catch (e) { f.push(`${k} RENDER: ${String(e.message).split('\n')[0]}`); continue; }
    const its = items(h);
    const want = ((FIX[k].peers.csc_columns || {}).absent || []).length;
    if (its.length !== want) f.push(`${k}: ${its.length} items for ${want} served`);
    for (const it of its) {
      all.push(it);
      f.push(...clauseFaults(it).map((x) => `${k} ${x}`));
      if (it.cls === 'unmapped') f.push(`${k} ${it.column}: class unmapped for "${(it.reason || '').slice(0, 50)}"`);
      if (it.reason === null) f.push(`${k} ${it.column}: data-absent-column-reason missing`);
    }
  }
  const { f: cf, classes } = classFaults(all);
  f.push(...cf);
  const classed = new Set(all.filter((it) => it.cls && it.cls !== 'unmapped').map((it) => it.reason));
  const unclassed = [...served].filter((r) => !classed.has(r));
  if (unclassed.length) f.push(`${unclassed.length} served reason(s) with no class`);
  arms.push(['the checkout: every absent column states its reason in reader words, one clause per class, 0 unmapped', f.length === 0,
    f.length === 0 ? `${all.length} items, ${served.size} served reasons, ${classes} classes, 0 unmapped` : `${f.length} fault(s): ${f.slice(0, 6).join(' | ')}`]);
}
{
  const f = [];
  const fx = JSON.parse(JSON.stringify(FIX.BA_US_Equity));
  const UNKNOWN = 'a reason R-1 has never served before';
  fx.peers.csc_columns.absent[0].reason = UNKNOWN;
  try {
    const it = items(render(fx)).find((x) => x.reason === UNKNOWN);
    if (!it) f.push('the planted item is missing');
    else {
      if (it.cls !== 'unmapped') f.push(`class "${it.cls}" for an unknown reason (want unmapped)`);
      if (!it.clause || it.clause.replace(/[\s.]/g, '').length < 8) f.push('no reader clause');
      if (TERMS.test(it.clause) || CODES.test(it.clause)) f.push(`system word in "${it.clause}"`);
    }
  } catch (e) { f.push('RENDER: ' + String(e.message).split('\n')[0]); }
  arms.push(['THE GAP SHOWS: an unknown served reason renders class unmapped with a plain clause', f.length === 0, f.length === 0 ? 'unmapped, plain' : f.join(' | ')]);
}
{
  const f = [];
  const ok = { column: 'Shares', cls: 'not-reported', reason: 'x', clause: 'the data source does not report share counts for these peers.' };
  if (clauseFaults(ok).length) f.push('a reader clause is rejected');
  const M = [
    ['bare', { ...ok, clause: 'is not available for these peers.' }],
    ['registry', { ...ok, clause: 'no preferred-equity code among the 289 registry factors' }],
  ];
  let caught = 0;
  for (const [n, it] of M) { if (clauseFaults(it).length) caught += 1; else f.push(`mutant ${n} accepted`); }
  const two = classFaults([ok, { ...ok, column: 'Debt', clause: 'something else entirely for these peers.' }]).f;
  if (two.length) caught += 1; else f.push('two clauses for one class accepted');
  arms.push(['PLANTED: a bare clause, a registry clause and two clauses for one class are rejected', f.length === 0,
    f.length === 0 ? `${caught} of 3 rejected` : f.join(' | ')]);
}

let pass = 0;
for (const [n, ok, d] of arms) { if (ok) pass += 1; console.log(`${ok ? 'ARM PASS' : 'ARM FAIL'} ${n} :: ${d}`); }
console.log(`EACH ABSENT COLUMN STATES ITS REASON IN READER WORDS: ${pass} of 3 arms`);
process.exit(pass === 3 ? 0 : 1);
