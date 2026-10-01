/**
 * sweep.cjs -- DSGN_AMGTV1 round 13, AV-l-5: THE FOUR DESIGNED STATES ARE CAPTURED IN THE SAME GRADED RUN, NO-PERMISSION BY ITS
 * LEVER, AND LABELLED FOR WHAT IT IS (round-12 analysis ruling 5; FWD-19, FWD-20).
 *
 * Usage (repo root): node <this file>
 * Ruling 5: "FWD-19's no-permission state needs its lever: the `--states-sweep` path renders `PanelNoPermission`, so the
 * `fourStates` clause can pass." Today `--states-sweep` (AMGT-rl-9) is a separate mode: it prints its own matrix and RESULT and
 * writes no grades.json, while a plain run grades fourStates FAIL (no-permission 0). The contract here: ONE invocation
 * `node portal/scripts/ui-contract-check.mjs --dist <dir> --out <dir> --states-sweep` grades the six states AND folds the sweep's
 * captures into grades.json `run.fourStates`, which PASSES only when each of loading / error / empty / no-permission is captured at
 * least once, with no-permission labelled STANDALONE (it has no live route: PanelStates.tsx's docstring).
 * Inputs: C:/tmp/dsgn-r13-dist/dev (vite build of site-Z DEV ba62e945) and the issuer's blank page round13/checks/dists/blank.
 * Arms:
 *   1  the lever: on the DEV build, one --states-sweep run writes grades.json whose run.fourStates reads PASS with each of the four
 *      kinds counted at least once
 *   2  honesty: the no-permission capture is labelled standalone in run.fourStates, and its PNG exists with bytes; the six states
 *      are still graded in the same grades.json (all ten per-state clauses present in each)
 *   3  the negative: on the blank page, the same invocation does NOT read fourStates PASS
 * Prints one line per arm and "THE FOUR DESIGNED STATES, ONE GRADED RUN: <k> of 3 arms"; exit 0 only at 3 of 3.
 */
const fs = require('fs');
const os = require('os');
const path = require('path');
const { spawnSync } = require('child_process');

const ROOT = process.cwd();
const PORTAL = path.join(ROOT, 'portal');
const CHECKS = path.join(ROOT, 'org/missions/D13/DSGN/DSGN_AMGTV1/deliverables/2.0.0_SA_COO~D/round13/checks');
const DIST = { dev: 'C:/tmp/dsgn-r13-dist/dev', blank: path.join(CHECKS, 'dists/blank') };
const CLAUSES = ['darkContainers', 'bandIsIdentityHeader', 'tabPanelsWhite', 'fonts', 'weights', 'sizes', 'radii', 'shadows', 'lowContrastChars', 'purpleFills'];
const OUT = fs.mkdtempSync(path.join(os.tmpdir(), 'r13-sweep-'));
function run(name) {
  const out = path.join(OUT, name);
  const r = spawnSync(process.execPath, ['scripts/ui-contract-check.mjs', '--dist', DIST[name], '--out', out, '--states-sweep'], { cwd: PORTAL, encoding: 'utf8', timeout: 840000 });
  let grades = null;
  try { grades = JSON.parse(fs.readFileSync(path.join(out, 'grades.json'), 'utf8')); } catch (e) { grades = null; }
  const pngs = fs.existsSync(out) ? fs.readdirSync(out).filter((f) => /no-permission.*\.png$/i.test(f)).map((f) => fs.statSync(path.join(out, f)).size) : [];
  return { rc: r.status, grades, pngs, tail: String(r.stdout || '').trim().split('\n').slice(-1).join('') };
}
for (const [k, d] of Object.entries(DIST)) if (!fs.existsSync(path.join(d, 'index.html'))) { console.log(`INPUT MISSING: ${k} at ${d}`); process.exit(3); }

const dev = run('dev');
const blank = run('blank');
const fsOf = (res) => ((res.grades || {}).run || {}).fourStates || {};

const f1 = [];
const d4 = fsOf(dev);
if (!dev.grades) f1.push(`dev: no grades.json from --states-sweep (rc=${dev.rc}; ${dev.tail.slice(0, 120)})`);
else {
  if (d4.grade !== 'PASS') f1.push(`dev: run.fourStates ${d4.grade} ${JSON.stringify(d4.counts || d4.acrossRun || {})}`);
  const counts = d4.counts || d4.acrossRun || {};
  for (const k of ['loading', 'error', 'empty', 'no-permission']) if (!(Number(counts[k]) >= 1)) f1.push(`dev: ${k} counted ${counts[k]}`);
}
const a1 = f1.length === 0;
const a1d = a1 ? `one --states-sweep run: fourStates PASS ${JSON.stringify(d4.counts || d4.acrossRun)}` : `${f1.length} failing; first: ${f1[0]}`;

const f2 = [];
if (dev.grades) {
  if (!/standalone/i.test(JSON.stringify(d4))) f2.push('run.fourStates does not label the no-permission capture standalone');
  if (!dev.pngs.length || !dev.pngs.some((b) => b > 0)) f2.push('no no-permission PNG with bytes in the out folder');
  const states = dev.grades.states || {};
  for (const st of ['list', 'thesis', 'exec', 'peers', 'model', 'posture']) {
    const miss = CLAUSES.filter((c) => !(states[st] || {})[c]);
    if (miss.length) { f2.push(`state ${st} is missing clauses ${miss.join(', ')} in the sweep run`); break; }
  }
}
const a2 = f2.length === 0;
const a2d = a2 ? `no-permission labelled standalone, PNG ${dev.pngs.join('/')} bytes; all six states graded in the same file` : `${f2.length} failing; first: ${f2[0]}`;

const f3 = [];
const b4 = fsOf(blank);
if (b4.grade === 'PASS') f3.push(`blank: run.fourStates reads PASS ${JSON.stringify(b4)}`);
if (blank.rc === 0) f3.push('blank: the run exited 0');
const a3 = f3.length === 0;
const a3d = a3 ? `the blank page does not pass fourStates (${b4.grade || 'no grade'}; rc=${blank.rc})` : `${f3.length} failing; first: ${f3[0]}`;

console.log(`RUNS: dev rc=${dev.rc} blank rc=${blank.rc} (out ${OUT})`);
const arms = [
  ['the lever: the four designed states in one graded run', a1, a1d],
  ['honesty: no-permission labelled standalone; the six states still graded', a2, a2d],
  ['the negative: a blank page does not pass', a3, a3d],
];
let pass = 0;
for (const [name, ok, detail] of arms) { if (ok) pass += 1; console.log(`${ok ? 'ARM PASS' : 'ARM FAIL'} ${name} :: ${detail}`); }
console.log(`THE FOUR DESIGNED STATES, ONE GRADED RUN: ${pass} of ${arms.length} arms`);
process.exit(pass === arms.length ? 0 : 1);
