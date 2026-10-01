/**
 * dossier.cjs -- DSGN_AMGTV1 round 10, AV-o-2: THE SERVED `dossier_fields` ON THE PAGE -- the thesis pillars with their citation,
 * the management passage beside the roster, the fund of record and the last stated position on the posture line and the Posture
 * tab, and a name whose block is empty shows its reason (round-9 analysis ruling 2; AMGT_CORPUS FWD-10, 11, 15, 16, 18).
 *
 * Usage (repo root): node <this file>
 * `/thesis` serves `dossier_fields` = { thesis_pillars: [{ pillar, text, terms, citation }], management: { status, value,
 * citation }, fund_of_record: { status, value, citation | reason }, last_stated_position: { status, value: { fund, size_pct,
 * text }, citation | reason } }, or { status, reason } when the name has no dossier. Fixtures (round10/fixtures, SERVED, captured
 * at the cut): IMB LN (every field SERVED, 6 pillars), AZN LN (every field SERVED, 5 pillars), TSM US (pillars and management
 * SERVED, fund of record and last stated position ABSENT with reasons), 6501 JP (the block is { status: READ_FAILED, reason }).
 * A citation reads in words: the report's file name (the last path segment of report_key, extension off) -- never an s3://
 * path, an extract.json or a key, which may ride a data- attribute only.
 * Arms:
 *   1  the pillars on the Thesis tab: for IMB, AZN and TSM every served pillar's `pillar` and `text` are in the visible text, in
 *      the served order, with its report's file name; no "s3://" or "extract.json" in any visible text of this check
 *   2  the management passage on the Exec Management tab: for IMB and TSM the served `management.value` (its first 60
 *      characters) is in the visible text with its report's file name
 *   3  fund of record and last stated position: for IMB and AZN the Posture tab AND the header posture line carry the fund of
 *      record `value` and the last stated position's `value.text`; for TSM (both ABSENT) the Posture tab says in words that no
 *      fund of record is stated, and prints no fund code
 *   4  an empty block shows its reason: for 6501 the Thesis tab carries the served reason ("no research dossier for this name")
 *      in words, and no pillar heading
 * Prints one line per arm and "DOSSIER FIELDS ON THE PAGE: <k> of 4 arms"; exit 0 only at 4 of 4.
 */
const L = require('./_load.cjs');
const S = require('./surfaces.cjs');

const get = (s) => (S.renderAll([s])[0] || {}).html || '';
const vis = (s) => L.textOf(get(s)).replace(/&amp;/g, '&').replace(/&quot;/g, '"').replace(/&#x27;/g, "'");
const reportName = (key) => (key ? String(key).split('/').pop().replace(/\.[A-Za-z0-9]{2,4}$/, '').trim() : null);
const df = (k) => (S.bundles[k] || {}).dossier_fields || null;
const norm = (s) => String(s || '').replace(/\s+/g, ' ').trim();
const allText = [];

// ---- arm 1 ------------------------------------------------------------------------------------------------------------------
const f1 = [];
let pillars = 0;
for (const [n, k] of [['IMB', 'IMB_LN_Equity'], ['AZN', 'AZN_LN_Equity'], ['TSM', 'TSM_US_Equity']]) {
  const d = df(k);
  const t = norm(vis(`thesis-${n}`));
  allText.push(t);
  let last = -1;
  for (const p of (d && d.thesis_pillars) || []) {
    pillars += 1;
    const at = t.indexOf(norm(p.pillar));
    if (at < 0) { f1.push(`${n}: pillar "${p.pillar}" not shown`); continue; }
    if (at < last) f1.push(`${n}: pillar "${p.pillar}" out of the served order`);
    last = at;
    if (!t.includes(norm(p.text).slice(0, 60))) f1.push(`${n}: the text of "${p.pillar}" not shown`);
    const rn = reportName(p.citation && p.citation.report_key);
    if (rn && !t.includes(rn)) f1.push(`${n}: pillar "${p.pillar}" has no citation in words ("${rn}")`);
  }
}
const a1 = f1.length === 0 && pillars > 0;
const a1d = a1 ? `${pillars} served pillar(s) over IMB / AZN / TSM shown in order, each with its report named` : `${f1.length} failing of ${pillars} pillar(s); first: ${f1[0]}`;

// ---- arm 2 ------------------------------------------------------------------------------------------------------------------
const f2 = [];
for (const [n, k] of [['IMB', 'IMB_LN_Equity'], ['TSM', 'TSM_US_Equity']]) {
  const m = (df(k) || {}).management;
  const t = norm(vis(`exec-${n}`));
  allText.push(t);
  if (!m || m.status !== 'SERVED') { f2.push(`${n}: fixture management not SERVED`); continue; }
  if (!t.includes(norm(m.value).slice(0, 60))) f2.push(`${n}: the management passage is not on the Exec Management tab`);
  const rn = reportName(m.citation && m.citation.report_key);
  if (rn && !t.includes(rn)) f2.push(`${n}: the management passage has no citation in words ("${rn}")`);
}
const a2 = f2.length === 0;
const a2d = a2 ? 'IMB and TSM show the served management passage on Exec Management, with its report named' : `${f2.length} failing; first: ${f2[0]}`;

// ---- arm 3 ------------------------------------------------------------------------------------------------------------------
const f3 = [];
for (const [n, k] of [['IMB', 'IMB_LN_Equity'], ['AZN', 'AZN_LN_Equity']]) {
  const d = df(k) || {};
  const fund = d.fund_of_record && d.fund_of_record.value;
  const lsp = d.last_stated_position && d.last_stated_position.value && d.last_stated_position.value.text;
  const pt = norm(vis(`posture-${n}`));
  const ht = norm(vis(`header-${n}`));
  allText.push(pt, ht);
  for (const [where, t] of [['Posture tab', pt], ['header posture line', ht]]) {
    if (!fund || !t.includes(fund)) f3.push(`${n}: fund of record "${fund}" not on the ${where}`);
    if (!lsp || !t.includes(norm(lsp))) f3.push(`${n}: last stated position "${lsp}" not on the ${where}`);
  }
}
{
  const t = norm(vis('posture-TSM'));
  allText.push(t);
  if (!/no fund of record/i.test(t)) f3.push('TSM: the Posture tab does not say that no fund of record is stated');
  if (/\b(IDVZ|PFOE|DIVZ)\b/.test(t)) f3.push('TSM: a fund code on the Posture tab where none is served');
}
const a3 = f3.length === 0;
const a3d = a3 ? 'IMB and AZN carry fund of record and last stated position on the Posture tab and the header posture line; TSM says none is stated' : `${f3.length} failing; first: ${f3[0]}`;

// ---- arm 4 ------------------------------------------------------------------------------------------------------------------
const f4 = [];
{
  const d = df('6501_JP_Equity') || {};
  const t = norm(vis('thesis-J6501'));
  allText.push(t);
  if (!d.reason || !t.toLowerCase().includes(String(d.reason).toLowerCase())) f4.push(`6501: the served reason "${d.reason}" is not on the Thesis tab`);
}
for (const t of allText) if (/s3:\/\/|extract\.json/.test(t)) { f4.push('a storage path or extract.json in visible text'); break; }
const a4 = f4.length === 0;
const a4d = a4 ? '6501 shows "no research dossier for this name" in words; no storage path is visible anywhere' : `${f4.length} failing; first: ${f4[0]}`;

const arms = [
  ['the thesis pillars, cited, on the Thesis tab', a1, a1d],
  ['the management passage beside the roster', a2, a2d],
  ['fund of record and last stated position on the posture line and the Posture tab', a3, a3d],
  ['an empty block shows its reason; no storage path on the face', a4, a4d],
];
let pass = 0;
for (const [name, ok, detail] of arms) { if (ok) pass += 1; console.log(`${ok ? 'ARM PASS' : 'ARM FAIL'} ${name} :: ${detail}`); }
console.log(`DOSSIER FIELDS ON THE PAGE: ${pass} of ${arms.length} arms`);
process.exit(pass === arms.length ? 0 : 1);
