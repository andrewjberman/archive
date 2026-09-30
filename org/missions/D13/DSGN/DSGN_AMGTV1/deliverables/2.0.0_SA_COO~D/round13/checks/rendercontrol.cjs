/**
 * rendercontrol.cjs -- DSGN_AMGTV1 round 12 (carried to round 13 as a bound), AV-m-1: THE CONTRACT'S RENDER CHECK CAN FAIL (FWD-20, with FWD-12 folded in; round-11
 * analysis ruling 5 and s.4 items 1 and 6).
 *
 * Usage (repo root): node <this file>
 * FWD-20 (PRD v0.4 :196-209): portal/scripts/ui-smoke.mjs (driven by ui-contract-check.mjs + ui-measure.mjs, the estate's
 * instrument since AMGT_RESAPP rounds 37-38) writes, per state, a PNG at 1440 and a DOM JSON reading one band, fonts {Lato},
 * weights {400,700}, no size below 11, radii {2,3,4,pill}, no shadow outside the focus ring, lowContrastChars 0, purpleFills per
 * FWD-18, the four designed states present, the drafting / tabs / posture harnesses green -- "AND the same instrument read against
 * the pre-redesign page FAILS each clause". FWD-12 (:131-138): the Security state has ONE dark band, the identity header is that
 * band, the tab panels are white hairline panels.
 * MEASURED AT THE CUT (an issuer-spawned helper, scratch r12-green-a @81a13fee): the pre-redesign page (portal 8fa7abde, the
 * project's round-1 base) PASSES bandContainersTopLevel, fonts, weights, sizes, radii, shadows, lowContrastChars and purpleFills in
 * every state -- AMGT_RESAPP rounds 37-38 fixed that chrome first. What it does NOT pass is the ONE-dark-container reading: its
 * navy title strips (rgb 10,23,51; the instrument's `stripContainers`) stand beside the band in thesis, exec, model and posture,
 * where DEV 846ecc6c shows none. So this check proves "can fail" two ways: on the REAL pre-redesign page for the clause that
 * discriminates (darkContainers = top-level band + strip containers inside main), and on a PLANTED page for every style clause
 * the old page already met, with a CLEAN planted page as its control.
 * THE OUTPUT CONTRACT (AV-m-1's face): `node portal/scripts/ui-contract-check.mjs --dist <built dir> --out <dir> [--states ...]`
 * serves the build from disk (no server) and writes `<out>/grades.json`:
 *   { "states": { "<state>": { "<clause>": { "grade": "PASS"|"FAIL"|"NOT_EXERCISED"|"N/A", "value": ... } } },
 *     "run": { "fourStates": { "grade": ..., "counts": {...} }, "harnesses": { "grade": ..., "drafting": {...}, "tabs": {...},
 *              "posture": {...} } },
 *     "result": { "PASS": n, "FAIL": n, "NOT_EXERCISED": n } }
 * with the ten per-state clauses darkContainers, bandIsIdentityHeader, tabPanelsWhite, fonts, weights, sizes, radii, shadows,
 * lowContrastChars, purpleFills; exit 0 only when every graded cell is PASS.
 * Inputs: C:/tmp/dsgn-r13-dist/pre (vite build of 8fa7abde) and C:/tmp/dsgn-r13-dist/dev (vite build of DEV 846ecc6c), both built
 * by the issuer at the cut; round13/checks/dists/{planted,clean,blank}/index.html (issuer-written static pages).
 * Arms:
 *   1  the real negative control: on the pre-redesign build darkContainers FAILS in thesis, exec, model and posture; on the DEV
 *      build darkContainers and bandIsIdentityHeader PASS in all five Security states; every state of both runs grades all ten
 *      clauses
 *   2  every style clause can fail: the planted page (list) FAILS darkContainers, fonts, weights, sizes, radii, shadows,
 *      lowContrastChars and purpleFills; the clean page (list) PASSES those eight (the control)
 *   3  a blind read is never a pass: the blank page grades every list clause NOT_EXERCISED (none PASS) and exits non-zero; on the
 *      DEV run the harness clause reads drafting, tabs and posture green
 * Prints one line per arm and "THE RENDER CHECK CAN FAIL: <k> of 3 arms"; exit 0 only at 3 of 3.
 */
const fs = require('fs');
const os = require('os');
const path = require('path');
const { spawnSync } = require('child_process');

const ROOT = process.cwd();
const PORTAL = path.join(ROOT, 'portal');
const CHECKS = path.join(ROOT, 'org/missions/D13/DSGN/DSGN_AMGTV1/deliverables/2.0.0_SA_COO~D/round13/checks');
const DIST = { pre: 'C:/tmp/dsgn-r13-dist/pre', dev: 'C:/tmp/dsgn-r13-dist/dev', planted: path.join(CHECKS, 'dists/planted'), clean: path.join(CHECKS, 'dists/clean'), blank: path.join(CHECKS, 'dists/blank') };
const CLAUSES = ['darkContainers', 'bandIsIdentityHeader', 'tabPanelsWhite', 'fonts', 'weights', 'sizes', 'radii', 'shadows', 'lowContrastChars', 'purpleFills'];
const STYLE = ['darkContainers', 'fonts', 'weights', 'sizes', 'radii', 'shadows', 'lowContrastChars', 'purpleFills'];
const SECURITY = ['thesis', 'exec', 'peers', 'model', 'posture'];
const OUT = fs.mkdtempSync(path.join(os.tmpdir(), 'r12-rendercontrol-'));

function run(name, states) {
  const out = path.join(OUT, name);
  const args = ['scripts/ui-contract-check.mjs', '--dist', DIST[name], '--out', out];
  if (states) args.push('--states', states);
  const r = spawnSync(process.execPath, args, { cwd: PORTAL, encoding: 'utf8', timeout: 540000 });
  let grades = null;
  try { grades = JSON.parse(fs.readFileSync(path.join(out, 'grades.json'), 'utf8')); } catch (e) { grades = null; }
  return { rc: r.status, grades, tail: String(r.stdout || '').trim().split('\n').slice(-2).join(' | ') + String(r.stderr || '').trim().split('\n').slice(-1).join('') };
}
const g = (res, state, clause) => (((res.grades || {}).states || {})[state] || {})[clause] || {};
const grade = (res, state, clause) => g(res, state, clause).grade || 'MISSING';

for (const [k, d] of Object.entries(DIST)) if (!fs.existsSync(path.join(d, 'index.html'))) { console.log(`INPUT MISSING: ${k} build at ${d}`); process.exit(3); }

const pre = run('pre');
const dev = run('dev');
const planted = run('planted', 'list');
const clean = run('clean', 'list');
const blank = run('blank', 'list');

// ---- arm 1 ------------------------------------------------------------------------------------------------------------------
const f1 = [];
for (const [label, res] of [['pre', pre], ['dev', dev]]) {
  if (!res.grades) { f1.push(`${label}: no grades.json (rc=${res.rc}; ${res.tail.slice(0, 160)})`); continue; }
  for (const st of ['list', ...SECURITY]) for (const c of CLAUSES) {
    if (grade(res, st, c) === 'MISSING') { f1.push(`${label}/${st}: clause ${c} is not graded`); break; }
  }
}
for (const st of ['thesis', 'exec', 'model', 'posture']) if (pre.grades && grade(pre, st, 'darkContainers') !== 'FAIL') f1.push(`pre/${st}: darkContainers reads ${grade(pre, st, 'darkContainers')} (value ${JSON.stringify(g(pre, st, 'darkContainers').value)}), want FAIL`);
for (const st of SECURITY) for (const c of ['darkContainers', 'bandIsIdentityHeader']) if (dev.grades && grade(dev, st, c) !== 'PASS') f1.push(`dev/${st}: ${c} reads ${grade(dev, st, c)} (value ${JSON.stringify(g(dev, st, c).value)}), want PASS`);
const a1 = f1.length === 0;
const a1d = a1 ? 'the pre-redesign build FAILS darkContainers in thesis, exec, model and posture; DEV passes it and bandIsIdentityHeader in all five Security states; all ten clauses graded in every state of both runs' : `${f1.length} failing; first: ${f1[0]}`;

// ---- arm 2 ------------------------------------------------------------------------------------------------------------------
const f2 = [];
if (!planted.grades) f2.push(`planted: no grades.json (rc=${planted.rc}; ${planted.tail.slice(0, 160)})`);
if (!clean.grades) f2.push(`clean: no grades.json (rc=${clean.rc}; ${clean.tail.slice(0, 160)})`);
for (const c of STYLE) {
  if (planted.grades && grade(planted, 'list', c) !== 'FAIL') f2.push(`planted: ${c} reads ${grade(planted, 'list', c)} (value ${JSON.stringify(g(planted, 'list', c).value)}), want FAIL`);
  if (clean.grades && grade(clean, 'list', c) !== 'PASS') f2.push(`clean: ${c} reads ${grade(clean, 'list', c)} (value ${JSON.stringify(g(clean, 'list', c).value)}), want PASS`);
}
const a2 = f2.length === 0;
const a2d = a2 ? `the planted page FAILS all ${STYLE.length} style clauses; the clean page PASSES all ${STYLE.length}` : `${f2.length} failing; first: ${f2[0]}`;

// ---- arm 3 ------------------------------------------------------------------------------------------------------------------
const f3 = [];
if (!blank.grades) f3.push(`blank: no grades.json (rc=${blank.rc}; ${blank.tail.slice(0, 160)})`);
else {
  for (const c of CLAUSES) { const gr = grade(blank, 'list', c); if (gr === 'PASS' || gr === 'MISSING') f3.push(`blank: ${c} reads ${gr}, want NOT_EXERCISED`); }
  if (blank.rc === 0) f3.push('blank: the run exited 0');
}
const h = ((dev.grades || {}).run || {}).harnesses || {};
for (const n of ['drafting', 'tabs', 'posture']) if (!h[n] || h[n].grade !== 'PASS') f3.push(`dev: harness ${n} reads ${h[n] ? h[n].grade : 'MISSING'} (${h[n] ? JSON.stringify(h[n]).slice(0, 80) : ''})`);
const a3 = f3.length === 0;
const a3d = a3 ? 'the blank page reads NOT_EXERCISED on every list clause and exits non-zero; on DEV the drafting, tabs and posture harnesses read green' : `${f3.length} failing; first: ${f3[0]}`;

console.log(`RUNS: pre rc=${pre.rc} dev rc=${dev.rc} planted rc=${planted.rc} clean rc=${clean.rc} blank rc=${blank.rc} (out ${OUT})`);
const arms = [
  ['the real negative control: the pre-redesign page fails the one-dark-container clause', a1, a1d],
  ['every style clause can fail (planted) and pass (clean)', a2, a2d],
  ['a blind read is never a pass; the harnesses are graded', a3, a3d],
];
let pass = 0;
for (const [name, ok, detail] of arms) { if (ok) pass += 1; console.log(`${ok ? 'ARM PASS' : 'ARM FAIL'} ${name} :: ${detail}`); }
console.log(`THE RENDER CHECK CAN FAIL: ${pass} of ${arms.length} arms`);
process.exit(pass === arms.length ? 0 : 1);
