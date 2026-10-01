/**
 * strip.cjs -- DSGN_AMGTV1 round 13, AV-l-4: A STRIP INSIDE A BAND IS THAT BAND; A SEPARATE DARK CONTAINER STILL FAILS (round-12
 * analysis ruling 4; FWD-12, FWD-20).
 *
 * Usage (repo root): node <this file>
 * Ruling 4: "The `list` title strip is the instrument's error, not the page's (the CVO: not a C3 rejection). `darkContainers` counts
 * a strip INSIDE a band as that band. The AC plants a second, separate dark band, which must still FAIL." Round 12's close render
 * read list darkContainers 2 (band 1 + strip 1): the Lead Panel's own header bar on its band.
 * Inputs: C:/tmp/dsgn-r13-dist/dev (vite build of site-Z DEV ba62e945, built by the issuer at the cut) and the issuer's static
 * pages round13/checks/dists/{inband,outstrip,planted}/index.html -- inband: a band with its own darker header strip INSIDE it;
 * outstrip: a band plus a SEPARATE navy strip on a lower panel (the pre-redesign shape); planted: two separate bands.
 * The instrument: `node portal/scripts/ui-contract-check.mjs --dist <dir> --out <dir> [--states list]` writing <out>/grades.json
 * (round 12, AV-m-1).
 * Arms:
 *   1  the page: on the DEV build every state reads darkContainers PASS -- the list included (its Lead Panel header strip is part
 *      of the band)
 *   2  the rule: the inband page reads darkContainers PASS (1), and its value still names the strip it folded in
 *   3  the negative: the outstrip page (a separate strip) and the planted page (a second separate band) each read darkContainers
 *      FAIL
 * Prints one line per arm and "A STRIP IN ITS BAND IS THE BAND: <k> of 3 arms"; exit 0 only at 3 of 3.
 */
const fs = require('fs');
const os = require('os');
const path = require('path');
const { spawnSync } = require('child_process');

const ROOT = process.cwd();
const PORTAL = path.join(ROOT, 'portal');
const CHECKS = path.join(ROOT, 'org/missions/D13/DSGN/DSGN_AMGTV1/deliverables/2.0.0_SA_COO~D/round13/checks');
const DIST = { dev: 'C:/tmp/dsgn-r13-dist/dev', inband: path.join(CHECKS, 'dists/inband'), outstrip: path.join(CHECKS, 'dists/outstrip'), planted: path.join(CHECKS, 'dists/planted') };
const OUT = fs.mkdtempSync(path.join(os.tmpdir(), 'r13-strip-'));
function run(name, states) {
  const out = path.join(OUT, name);
  const args = ['scripts/ui-contract-check.mjs', '--dist', DIST[name], '--out', out];
  if (states) args.push('--states', states);
  const r = spawnSync(process.execPath, args, { cwd: PORTAL, encoding: 'utf8', timeout: 540000 });
  let grades = null;
  try { grades = JSON.parse(fs.readFileSync(path.join(out, 'grades.json'), 'utf8')); } catch (e) { grades = null; }
  return { rc: r.status, grades, tail: String(r.stdout || '').trim().split('\n').slice(-1).join('') };
}
const cell = (res, st) => (((res.grades || {}).states || {})[st] || {}).darkContainers || {};
for (const [k, d] of Object.entries(DIST)) if (!fs.existsSync(path.join(d, 'index.html'))) { console.log(`INPUT MISSING: ${k} at ${d}`); process.exit(3); }

const dev = run('dev');
const inband = run('inband', 'list');
const outstrip = run('outstrip', 'list');
const planted = run('planted', 'list');

const f1 = [];
if (!dev.grades) f1.push(`dev: no grades.json (rc=${dev.rc}; ${dev.tail.slice(0, 120)})`);
else for (const st of ['list', 'thesis', 'exec', 'peers', 'model', 'posture']) if (cell(dev, st).grade !== 'PASS') f1.push(`dev/${st}: darkContainers ${cell(dev, st).grade} ${JSON.stringify(cell(dev, st).value)}`);
const a1 = f1.length === 0;
const a1d = a1 ? 'the DEV build reads darkContainers PASS in all six states, the list included' : `${f1.length} failing; first: ${f1[0]}`;

const f2 = [];
const ib = cell(inband, 'list');
if (!inband.grades) f2.push(`inband: no grades.json (rc=${inband.rc}; ${inband.tail.slice(0, 120)})`);
else if (ib.grade !== 'PASS') f2.push(`inband: darkContainers ${ib.grade} ${JSON.stringify(ib.value)}`);
else if (!/strip/i.test(JSON.stringify(ib.value || {}))) f2.push(`inband: the value does not name the folded strip ${JSON.stringify(ib.value)}`);
const a2 = f2.length === 0;
const a2d = a2 ? `the inband page reads PASS ${JSON.stringify(ib.value)}` : `${f2.length} failing; first: ${f2[0]}`;

const f3 = [];
for (const [n, res] of [['outstrip', outstrip], ['planted', planted]]) {
  if (!res.grades) f3.push(`${n}: no grades.json (rc=${res.rc})`);
  else if (cell(res, 'list').grade !== 'FAIL') f3.push(`${n}: darkContainers ${cell(res, 'list').grade} ${JSON.stringify(cell(res, 'list').value)} (want FAIL)`);
}
const a3 = f3.length === 0;
const a3d = a3 ? `a separate strip (${JSON.stringify(cell(outstrip, 'list').value)}) and a second band (${JSON.stringify(cell(planted, 'list').value)}) each FAIL` : `${f3.length} failing; first: ${f3[0]}`;

console.log(`RUNS: dev rc=${dev.rc} inband rc=${inband.rc} outstrip rc=${outstrip.rc} planted rc=${planted.rc} (out ${OUT})`);
const arms = [
  ['the page: every state one dark container', a1, a1d],
  ['the rule: a strip inside its band is the band', a2, a2d],
  ['the negative: a separate dark container still FAILS', a3, a3d],
];
let pass = 0;
for (const [name, ok, detail] of arms) { if (ok) pass += 1; console.log(`${ok ? 'ARM PASS' : 'ARM FAIL'} ${name} :: ${detail}`); }
console.log(`A STRIP IN ITS BAND IS THE BAND: ${pass} of ${arms.length} arms`);
process.exit(pass === arms.length ? 0 : 1);
