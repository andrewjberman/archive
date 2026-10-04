/**
 * changed35.cjs -- DSGN_AMGTV1 round 35 (issuer 2.0.0_SA_COO~D): WHAT CHANGED READS IN WORDS.
 *
 * Usage (from the directory whose portal/ is the checkout under test, e.g. C:/tmp/wk-dsgn-amgtv1-92): node <this file>
 *   A worker runs it from its worktree root: cd "$(git rev-parse --show-toplevel)" && node "org/missions/D13/DSGN/DSGN_AMGTV1/
 *   deliverables/2.0.0_SA_COO~D/round35/checks/changed/changed35.cjs". Fixtures resolve from this file's own location; the portal
 *   resolves from the cwd (cwd/portal).
 *   ISSUER GREEN ARM: CHECK_SRC_OVERRIDE (see round15/checks/_load.cjs) is honoured for every source read here, and the KEEP checks
 *   are spawned with the same env, so a scratch reference fix is graded by them too. A worker never sets it.
 * Why: the served BA /compare (round35/fixtures/compare.BA_US_Equity.json, captured on opal-amgt-scoped-api FcVBPafw) serves 37
 *   changed figures: 32 scope "forecast" (BEST_* consensus lines, fiscal years 2026-2028) and 5 scope "header". At portal 055ba370
 *   components/model/WhatChangedPanel.tsx names a changed line from the served model.line_names, then the sheet's LINE_NAMES, then
 *   the header card / stat tile labels, then (header scope only) the served header figure's basis.definition, and otherwise prints
 *   the fixed phrase UNNAMED_CHANGED_LINE "a line this page has no name for yet". No map names a BEST_* mnemonic and the panel looks
 *   up a figure only for scope "header", so every forecast row prints the fixed phrase although the served
 *   model.forecast_figures[].basis.definition carries its meaning. And a row whose before and after print the same text (BEST_DIV_YLD
 *   2026 "0.0%" -> "0.0%") prints a move ("-0.0", "-100.0%") the reader cannot see in the two figures.
 * Render: round15/checks/_load.cjs (the REAL page sources, page hooks stubbed per hook) renders the REAL tabs/ModelTab.tsx, as
 *   round29 model/whatchanged.cjs does, with useThesisBundle / useModelVersions / useModelCompare answering the three round-35
 *   fixtures verbatim ({_capture_note, payload} -> payload) and useInputLedger answering nothing. The What-changed panel's rows are
 *   read by their hooks: [data-what-changed-row="<served figure>"], cells [data-what-changed-cell="before"|"after"|"change"|"pct"];
 *   a row's PRINTED NAME is its first <th>/<td> that is not a [data-what-changed-cell] (the row header).
 * Definitions:
 *   UNNAMED: a printed name that contains "has no name for yet" (the base's fixed phrase, any case) or carries no letter once the
 *     fiscal-year words are taken off.
 *   BASE NAME (arm 2): the printed name with "(fiscal year NNNN)", "FY NNNN" and any standalone year 19xx/20xx removed, whitespace
 *     collapsed, compared case-insensitively. One mnemonic in several fiscal years shares its base name; two mnemonics may not.
 *   VENDOR TOKEN: /\b[A-Z][A-Z0-9]*_[A-Z0-9_]+\b/ (the loader's mnemonic class) or the word "BEST" in capitals.
 *   EQUAL PRINT (arm 3): the before and after cells print the same visible text (whitespace collapsed).
 * Arms:
 *   1  NAMED: 0 of the 37 rendered changed rows print an UNNAMED name, and all 37 served rows are rendered.
 *   2  ONE NAME PER LINE: no base name is printed for two different mnemonics, and no printed name carries a vendor token.
 *   3  NO MOVE BETWEEN EQUAL PRINTS: on every equal-print row the change cell and the percent cell print no digit; at least one
 *      equal-print row exists in the served table (else NOT_EXERCISED, a FAIL -- so a fix that only prints more digits until no two
 *      prints are equal does not pass this arm; the rule is about what an equal pair prints).
 *   4  KEEP: round29 model/whatchanged.cjs, round29 model/etwords.cjs and round34 repairs/repairs34.cjs exit 0 on the same tree.
 *   5  PLANTED: arm 1's grader flags a planted row set with one fixed-phrase row and one blank name, and accepts a named set; arm
 *      2's grader flags two mnemonics given one name (in one fiscal year and across two), a name carrying "BEST_EPS" and a name
 *      carrying "BEST", and accepts one
 *      mnemonic named alike across three fiscal years; arm 3's grader flags an equal-print row printing "-0.0" / "-100.0%", reads
 *      NOT_EXERCISED on a set with no equal print, and accepts an equal-print row that prints no digit.
 * Blind spots: names are graded for presence, uniqueness and vendor tokens only -- not for being the RIGHT words (a reader-facing
 *   name that misstates the figure passes; the CVO's L9 read covers meaning). Arm 3 grades the two cells' digits only; a sentence
 *   such as "unchanged" is not graded for wording. One security (BA) and one served pair.
 * Prints one line per arm and "WHAT CHANGED READS IN WORDS: <k> of 5 arms"; exit 0 only at 5 of 5. Static renders only; no network,
 * no AWS, writes no file.
 */
const fs = require('fs');
const path = require('path');
const { spawnSync } = require('child_process');

const SA = 'src/pages/SecurityAnalysis/';
const DROOT = path.join(__dirname, '..', '..', '..');
const FXDIR = path.join(__dirname, '..', '..', 'fixtures');
const L = require(path.join(DROOT, 'round15', 'checks', '_load.cjs'));
const first = (e) => String(e && e.message ? e.message : e).split('\n')[0];
const norm = (s) => String(s === null || s === undefined ? '' : s).replace(/\s+/g, ' ').trim();
const pay = (x) => (x && x.payload && (x._capture_note || x._capture) ? x.payload : x);
const readFx = (name) => pay(JSON.parse(fs.readFileSync(path.join(FXDIR, name), 'utf8')));
const KEY = 'BA_US_Equity';

const COMPARE = readFx(`compare.${KEY}.json`);
const THESIS = readFx(`thesis.${KEY}.json`);
const VERSIONS = readFx(`versions.${KEY}.json`);
const CHANGED = (COMPARE.compared && COMPARE.compared.changed) || [];
const UNNAMED = /has no name for yet/i;
const VENDOR = /\b[A-Z][A-Z0-9]*_[A-Z0-9_]+\b|\bBEST\b/;

// ---- reading the rendered rows --------------------------------------------------------------------------------------------
const esc = (s) => String(s).replace(/&/g, '&amp;').replace(/"/g, '&quot;');
/** The inner HTML of the element whose opening tag starts at `at`. */
function innerAt(html, at) {
  const tag = /^<([a-zA-Z0-9]+)/.exec(html.slice(at))[1];
  const start = html.indexOf('>', at) + 1;
  const re = new RegExp('<(/?)' + tag + '\\b[^>]*?(/?)>', 'g');
  re.lastIndex = start;
  let depth = 1;
  let m;
  while ((m = re.exec(html)) !== null) {
    if (m[2] === '/') continue;
    depth += m[1] === '/' ? -1 : 1;
    if (depth === 0) return html.slice(start, m.index);
  }
  return html.slice(start);
}
/** A row's header: its first <th>/<td> that is not a [data-what-changed-cell]. */
function rowName(row) {
  const re = /<(th|td)\b([^>]*)>/g;
  let m;
  while ((m = re.exec(row)) !== null) if (!/data-what-changed-cell=/.test(m[2])) return L.textOf(innerAt(row, m.index));
  return null;
}
function renderRows() {
  L.hookState.data = undefined;
  L.hookState.impl = { useThesisBundle: () => THESIS, useModelVersions: () => VERSIONS, useModelCompare: () => COMPARE, useInputLedger: () => undefined };
  const MT = L.source(SA + 'tabs/ModelTab.tsx');
  const html = L.render(MT.ModelTab, { securityKey: KEY });
  const inner = L.innerOf(html, 'data-what-changed');
  if (inner === null) throw new Error('no [data-what-changed] panel in the rendered Model tab');
  const rows = [];
  const missing = [];
  for (const c of CHANGED) {
    const r = L.innerOf(inner, 'data-what-changed-row', esc(c.figure));
    if (r === null) { missing.push(c.figure); continue; }
    const cell = (k) => { const x = L.innerOf(r, 'data-what-changed-cell', k); return x === null ? null : L.textOf(x); };
    rows.push({ figure: c.figure, mnemonic: c.mnemonic, fiscal_year: c.fiscal_year, scope: c.scope, name: rowName(r), before: cell('before'), after: cell('after'), chg: cell('change'), pct: cell('pct') });
  }
  return { rows, missing };
}
const label = (r) => `${r.mnemonic}${r.fiscal_year !== null && r.fiscal_year !== undefined ? ' ' + r.fiscal_year : ''}`;

// ---- graders (pure over row records; arm 5 feeds them planted rows) -------------------------------------------------------
const baseName = (name) => norm(String(name || '')
  .replace(/\(\s*fiscal year\s+\d{4}\s*\)/gi, ' ')
  .replace(/\bfiscal year\s+\d{4}\b/gi, ' ')
  .replace(/\bFY\s?\d{2,4}\b/g, ' ')
  .replace(/\b(?:19|20)\d{2}\b/g, ' ')
  .replace(/\(\s*\)/g, ' ')).replace(/[\s,;:-]+$/, '');
/** Arm 1: rows whose printed name is the fixed phrase or carries no letter. */
function unnamedRows(rows) {
  return rows.filter((r) => r.name === null || UNNAMED.test(r.name) || !/[A-Za-z]/.test(baseName(r.name)));
}
/** Arm 2: faults for a shared base name across mnemonics and for vendor tokens in a name. */
function nameFaults(rows) {
  const f = [];
  const by = new Map();
  for (const r of rows) {
    if (r.name === null) continue;
    const k = baseName(r.name).toLowerCase();
    if (!by.has(k)) by.set(k, new Set());
    by.get(k).add(r.mnemonic);
    const v = VENDOR.exec(r.name);
    if (v) f.push(`${label(r)}: the name "${norm(r.name)}" carries the vendor token "${v[0]}"`);
  }
  for (const [k, set] of by) if (set.size > 1) f.push(`${set.size} mnemonics share the name "${k}" (${[...set].slice(0, 5).join(', ')}${set.size > 5 ? ', ...' : ''})`);
  return f;
}
/** Arm 3: { equal: rows whose before and after print the same text, faults: those printing a digit in change or percent }. */
function equalPrintFaults(rows) {
  const equal = rows.filter((r) => r.before !== null && r.after !== null && norm(r.before) === norm(r.after));
  const faults = equal.filter((r) => /\d/.test(r.chg || '') || /\d/.test(r.pct || ''))
    .map((r) => `${label(r)}: "${norm(r.before)}" -> "${norm(r.after)}" prints change "${norm(r.chg)}" and percent "${norm(r.pct)}"`);
  if (equal.length === 0) faults.push('NOT_EXERCISED: no row prints the same before and after');
  return { equal, faults };
}
function keepsPassing(rels) {
  const faults = [];
  for (const rel of rels) {
    const r = spawnSync(process.execPath, [path.join(DROOT, rel)], { cwd: process.cwd(), env: process.env, encoding: 'utf8', timeout: 900000 });
    const last = ((r.stdout || '') + (r.stderr || '')).trim().split('\n').pop() || '';
    if (r.status !== 0) faults.push(`KEEP: ${rel} rc=${r.status} ("${last.slice(0, 100)}")`);
  }
  return faults;
}

// ---- the render ----------------------------------------------------------------------------------------------------------
let R = { rows: [], missing: [] };
let renderError = null;
if (CHANGED.length !== 37) renderError = `FIXTURE: compare.${KEY}.json serves ${CHANGED.length} changed rows (want 37)`;
else { try { R = renderRows(); } catch (e) { renderError = 'RENDER: ' + first(e); } }

const arms = [];
// ---- arm 1 ----
{
  const f = [];
  if (renderError) f.push(renderError);
  if (R.missing.length) f.push(`${R.missing.length} of ${CHANGED.length} served changed rows not rendered (first ${R.missing[0]})`);
  const bad = unnamedRows(R.rows);
  if (bad.length) f.push(`${bad.length} of ${CHANGED.length} rows print no name (first: ${bad.slice(0, 4).map((r) => `${label(r)} "${norm(r.name)}"`).join('; ')})`);
  const fc = R.rows.filter((r) => r.scope === 'forecast').slice(0, 1).concat(R.rows.filter((r) => r.scope === 'header').slice(0, 1));
  arms.push(['NAMED: 0 of the 37 rendered changed rows print "a line this page has no name for yet" or a blank name', f.length === 0,
    f.length ? f.join(' | ') : `0 of ${R.rows.length} rows unnamed (e.g. ${fc.map((r) => `${label(r)} "${norm(r.name)}"`).join('; ')})`]);
}
// ---- arm 2 ----
{
  const f = renderError ? [renderError] : nameFaults(R.rows);
  const names = new Set(R.rows.map((r) => baseName(r.name).toLowerCase()));
  arms.push(['ONE NAME PER LINE: no printed name shared by two mnemonics, no vendor mnemonic token or "BEST" in a name', f.length === 0,
    f.length ? `${f.length} fault(s): ${f.slice(0, 6).join(' | ')}` : `${names.size} distinct names for ${new Set(R.rows.map((r) => r.mnemonic)).size} mnemonics over ${R.rows.length} rows; 0 vendor tokens`]);
}
// ---- arm 3 ----
{
  const r = equalPrintFaults(R.rows);
  const f = renderError ? [renderError] : r.faults;
  const shown = r.equal.map((x) => `${label(x)} "${norm(x.before)}" -> "${norm(x.after)}": change "${norm(x.chg)}", percent "${norm(x.pct)}"`);
  arms.push(['NO MOVE BETWEEN EQUAL PRINTS: where before and after print the same text, the change and percent cells print no digit', f.length === 0,
    f.length ? `${r.equal.length} equal-print row(s), ${f.length} fault(s): ${f.join(' | ')}` : `${r.equal.length} equal-print row(s), each prints no move: ${shown.join('; ')}`]);
}
// ---- arm 4 ----
{
  const KEEP = ['round29/checks/model/whatchanged.cjs', 'round29/checks/model/etwords.cjs', 'round34/checks/repairs/repairs34.cjs'];
  const f = keepsPassing(KEEP);
  arms.push(['KEEP: round29 whatchanged.cjs, round29 etwords.cjs and round34 repairs34.cjs exit 0 on the same tree', f.length === 0,
    f.length ? f.join(' | ') : `${KEEP.length} of ${KEEP.length} exit 0`]);
}
// ---- arm 5: PLANTED ----
{
  const f = [];
  const row = (mnemonic, fy, name, before, after, chg, pct) => ({ mnemonic, fiscal_year: fy, name, before, after, chg, pct });
  // arm 1's grader
  const p1 = [row('BEST_EPS', 2026, 'a line this page has no name for yet (fiscal year 2026)', '-0.83', '-0.83', '-0.01', '-0.7%'),
    row('PX_LAST', null, 'Share price (last close)', 'USD 196.80', 'USD 193.56', '-USD 3.24', '-1.6%')];
  const u1 = unnamedRows(p1);
  if (u1.length !== 1 || u1[0].mnemonic !== 'BEST_EPS') f.push(`arm 1 grader flagged ${u1.length} of a set with one fixed-phrase row`);
  if (unnamedRows([row('BEST_BPS', 2027, ' (fiscal year 2027)', '1', '2', '+1', '+100.0%')]).length !== 1) f.push('arm 1 grader accepted a blank name');
  if (unnamedRows([row('BEST_EPS', 2026, 'Consensus earnings per share (fiscal year 2026)', '1', '2', '+1', '+100.0%')]).length !== 0) f.push('arm 1 grader rejected a named row');
  // arm 2's grader
  const shared = nameFaults([row('BEST_EPS', 2026, 'Consensus estimate (fiscal year 2026)'), row('BEST_BPS', 2026, 'Consensus estimate (fiscal year 2026)')]);
  if (!shared.some((x) => /2 mnemonics share the name "consensus estimate"/.test(x))) f.push(`arm 2 grader did not flag two mnemonics given one name (${shared[0] || 'accepted'})`);
  const acrossYears = nameFaults([row('BEST_EPS', 2026, 'Consensus estimate (fiscal year 2026)'), row('BEST_BPS', 2027, 'Consensus estimate (fiscal year 2027)')]);
  if (!acrossYears.some((x) => /share the name/.test(x))) f.push('arm 2 grader did not flag two mnemonics given one name in different years');
  if (!nameFaults([row('BEST_EPS', 2026, 'Consensus BEST_EPS (fiscal year 2026)')]).some((x) => /vendor token "BEST_EPS"/.test(x))) f.push('arm 2 grader did not flag "BEST_EPS" in a name');
  if (!nameFaults([row('BEST_EPS', 2026, 'Bloomberg consensus (BEST) estimate of earnings per share')]).some((x) => /vendor token "BEST"/.test(x))) f.push('arm 2 grader did not flag "BEST" in a name');
  const sameLine = nameFaults([2026, 2027, 2028].map((y) => row('BEST_EPS', y, `Consensus earnings per share (fiscal year ${y})`)));
  if (sameLine.length) f.push(`arm 2 grader rejected one mnemonic named alike across three years (${sameLine[0]})`);
  // arm 3's grader
  const eq = equalPrintFaults([row('BEST_DIV_YLD', 2026, 'Consensus dividend yield', '0.0%', '0.0%', '-0.0', '-100.0%'), row('BEST_EPS', 2027, 'Consensus earnings per share', '3.91', '3.85', '-0.06', '-1.5%')]);
  if (!(eq.faults.length === 1 && /BEST_DIV_YLD 2026: "0\.0%" -> "0\.0%" prints change "-0\.0" and percent "-100\.0%"/.test(eq.faults[0]))) f.push(`arm 3 grader did not flag the planted "-100.0%" equal-print row (${eq.faults[0] || 'accepted'})`);
  if (!equalPrintFaults([row('BEST_EPS', 2027, 'x', '3.91', '3.85', '-0.06', '-1.5%')]).faults.some((x) => /^NOT_EXERCISED/.test(x))) f.push('arm 3 grader did not read NOT_EXERCISED on a set with no equal print');
  if (equalPrintFaults([row('BEST_DIV_YLD', 2026, 'x', '0.0%', '0.0%', 'unchanged as printed', '--')]).faults.length) f.push('arm 3 grader rejected an equal-print row that prints no digit');
  arms.push(['PLANTED: the three graders flag their planted faults (a fixed-phrase row, a blank name, a shared name, "BEST_EPS", "BEST", an equal print with "-100.0%", no equal print) and accept the good shapes', f.length === 0,
    f.length ? f.join(' | ') : '8 of 8 planted faults flagged (2 arm-1, 4 arm-2, 2 arm-3); 3 of 3 good shapes accepted']);
}

let pass = 0;
for (const [n, ok, d] of arms) { if (ok) pass += 1; console.log(`${ok ? 'ARM PASS' : 'ARM FAIL'} ${n} :: ${d}`); }
console.log(`WHAT CHANGED READS IN WORDS: ${pass} of ${arms.length} arms`);
process.exit(pass === arms.length ? 0 : 1);
