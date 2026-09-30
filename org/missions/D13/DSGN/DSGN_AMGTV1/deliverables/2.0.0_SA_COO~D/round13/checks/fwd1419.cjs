/**
 * fwd1419.cjs -- DSGN_AMGTV1 round 13, AV-l-6: THE INSTRUMENT GRADES FWD-14..FWD-19, EACH CLAUSE WITH ITS VALUE, AND NEVER PASSES A
 * CLAUSE IT COULD NOT SEE (round-12 analysis s.4 item 6; PRD v0.5 FWD-14..19).
 *
 * Usage (repo root): node <this file>
 * Item 6: "The FWD-14..19 grading pass on the refreshed instrument. It prints each clause's value per state, and a NOT_EXERCISED
 * clause is never a PASS." The clauses (named here; each state's grades.json entry {grade, value}):
 *   thesis  fwd14_passagesFolded    passages carried in a native title= tooltip (must be 0) beside the "cites N passages" affordances
 *                                   counted and the nodes scanned (the positive control: FWD-14's addendum)
 *   model   fwd15_modelTable        the fiscal table's tabular cells, and each REFUSED row rendering one status icon and one sentence
 *   peers   fwd16_absentColumns     the table's columns are the PRESENT ones; an "Absent columns (N)" disclosure lists the others
 *   posture fwd17_verdictComparable the verdict card names its comparable; UNRESOLVED cites use an icon beside navy text, 0 amber text
 *   list + the five Security states  fwd18_controls  segmented controls (list), a "Source:" footer, purpleFills per mode
 *   run     fwd19_designedStates    the four designed states, per panel, from the run and its --states-sweep
 * The invocation: `node portal/scripts/ui-contract-check.mjs --dist <dir> --out <dir> --states-sweep`.
 * Inputs: C:/tmp/dsgn-r13-dist/dev (vite build of site-Z DEV ba62e945) and the issuer's blank page round13/checks/dists/blank.
 * Arms:
 *   1  every clause is there: on the DEV build each of fwd14..fwd18 is graded at its state(s) and fwd19 at run level, each with a
 *      grade in {PASS, FAIL, NOT_EXERCISED, N/A} and a non-empty value
 *   2  never a pass on nothing: on the blank page every fwd14..fwd19 clause reads NOT_EXERCISED (none PASS) and the run exits
 *      non-zero
 *   3  a PASS shows what it saw: on the DEV build every fwd clause that reads PASS carries a positive count in its value (nodes or
 *      elements scanned > 0), and grades.json `result` counts the fwd clauses with the rest
 * Prints one line per arm and "FWD-14..19 GRADED, NEVER BLIND: <k> of 3 arms"; exit 0 only at 3 of 3.
 */
const fs = require('fs');
const os = require('os');
const path = require('path');
const { spawnSync } = require('child_process');

const ROOT = process.cwd();
const PORTAL = path.join(ROOT, 'portal');
const CHECKS = path.join(ROOT, 'org/missions/D13/DSGN/DSGN_AMGTV1/deliverables/2.0.0_SA_COO~D/round13/checks');
const DIST = { dev: 'C:/tmp/dsgn-r13-dist/dev', blank: path.join(CHECKS, 'dists/blank') };
const AT = {
  fwd14_passagesFolded: ['thesis'],
  fwd15_modelTable: ['model'],
  fwd16_absentColumns: ['peers'],
  fwd17_verdictComparable: ['posture'],
  fwd18_controls: ['list', 'thesis', 'exec', 'peers', 'model', 'posture'],
};
const GRADES = new Set(['PASS', 'FAIL', 'NOT_EXERCISED', 'N/A']);
const OUT = fs.mkdtempSync(path.join(os.tmpdir(), 'r13-fwd1419-'));
function run(name, states) {
  const out = path.join(OUT, name);
  const args = ['scripts/ui-contract-check.mjs', '--dist', DIST[name], '--out', out, '--states-sweep'];
  if (states) args.push('--states', states);
  const r = spawnSync(process.execPath, args, { cwd: PORTAL, encoding: 'utf8', timeout: 840000 });
  let grades = null;
  try { grades = JSON.parse(fs.readFileSync(path.join(out, 'grades.json'), 'utf8')); } catch (e) { grades = null; }
  return { rc: r.status, grades, tail: String(r.stdout || '').trim().split('\n').slice(-1).join('') };
}
const nonEmpty = (v) => v !== undefined && v !== null && JSON.stringify(v) !== '{}' && JSON.stringify(v) !== '""';
const positive = (v) => /"(nodes|nodesScanned|elements|scanned|cells|columns|panels|affordances|count)[A-Za-z]*":\s*[1-9]/i.test(JSON.stringify(v || {}));
for (const [k, d] of Object.entries(DIST)) if (!fs.existsSync(path.join(d, 'index.html'))) { console.log(`INPUT MISSING: ${k} at ${d}`); process.exit(3); }

const dev = run('dev');
const blank = run('blank', 'list,thesis,model,peers,posture');
const cellOf = (res, st, c) => (((res.grades || {}).states || {})[st] || {})[c];
const runOf = (res) => ((res.grades || {}).run || {}).fwd19_designedStates;

const f1 = [];
let seen = 0;
if (!dev.grades) f1.push(`dev: no grades.json (rc=${dev.rc}; ${dev.tail.slice(0, 120)})`);
else {
  for (const [c, sts] of Object.entries(AT)) for (const st of sts) {
    const g = cellOf(dev, st, c);
    if (!g) f1.push(`dev/${st}: no ${c}`);
    else if (!GRADES.has(g.grade) || !nonEmpty(g.value)) f1.push(`dev/${st}: ${c} ${JSON.stringify(g).slice(0, 100)}`);
    else seen += 1;
  }
  const r19 = runOf(dev);
  if (!r19 || !GRADES.has(r19.grade) || !nonEmpty(r19.value || r19.counts || r19.perPanel)) f1.push(`dev: run.fwd19_designedStates ${JSON.stringify(r19).slice(0, 100)}`);
  else seen += 1;
}
const a1 = f1.length === 0;
const a1d = a1 ? `${seen} FWD-14..19 clause cells graded on the DEV build, each with a grade and a value` : `${f1.length} failing; first: ${f1[0]}`;

const f2 = [];
if (!blank.grades) f2.push(`blank: no grades.json (rc=${blank.rc}; ${blank.tail.slice(0, 120)})`);
else {
  for (const [c, sts] of Object.entries(AT)) for (const st of sts) {
    const g = cellOf(blank, st, c);
    if (g && g.grade === 'PASS') f2.push(`blank/${st}: ${c} reads PASS`);
    else if (g && g.grade !== 'NOT_EXERCISED' && g.grade !== 'N/A') f2.push(`blank/${st}: ${c} reads ${g.grade} (want NOT_EXERCISED)`);
  }
  const r19 = runOf(blank);
  if (r19 && r19.grade === 'PASS') f2.push('blank: run.fwd19_designedStates reads PASS');
  if (blank.rc === 0) f2.push('blank: the run exited 0');
}
const a2 = f2.length === 0;
const a2d = a2 ? `the blank page reads NOT_EXERCISED on every FWD-14..19 clause it grades and exits ${blank.rc}` : `${f2.length} failing; first: ${f2[0]}`;

const f3 = [];
let passes = 0;
if (dev.grades) {
  for (const [c, sts] of Object.entries(AT)) for (const st of sts) {
    const g = cellOf(dev, st, c);
    if (g && g.grade === 'PASS') { passes += 1; if (!positive(g.value)) f3.push(`dev/${st}: ${c} PASS without a positive count ${JSON.stringify(g.value).slice(0, 100)}`); }
  }
  const res = dev.grades.result || {};
  const total = ['PASS', 'FAIL', 'NOT_EXERCISED', 'N/A'].reduce((a, k) => a + (Number(res[k]) || 0), 0);
  let cells = 0;
  for (const st of Object.values(dev.grades.states || {})) cells += Object.keys(st).length;
  if (total < cells) f3.push(`result counts ${total} cells but the states carry ${cells} (the fwd clauses are not counted)`);
}
const a3 = f3.length === 0;
const a3d = a3 ? `${passes} FWD PASS cell(s), each with a positive count; result counts every graded cell` : `${f3.length} failing; first: ${f3[0]}`;

console.log(`RUNS: dev rc=${dev.rc} blank rc=${blank.rc} (out ${OUT})`);
const arms = [
  ['every FWD-14..19 clause is graded with its value', a1, a1d],
  ['never a pass on nothing (blank page)', a2, a2d],
  ['a PASS shows what it saw; result counts it', a3, a3d],
];
let pass = 0;
for (const [name, ok, detail] of arms) { if (ok) pass += 1; console.log(`${ok ? 'ARM PASS' : 'ARM FAIL'} ${name} :: ${detail}`); }
console.log(`FWD-14..19 GRADED, NEVER BLIND: ${pass} of ${arms.length} arms`);
process.exit(pass === arms.length ? 0 : 1);
