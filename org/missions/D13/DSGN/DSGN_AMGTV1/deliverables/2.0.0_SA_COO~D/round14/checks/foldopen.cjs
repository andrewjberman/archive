/**
 * foldopen.cjs -- DSGN_AMGTV1 round 14, AV-k-7: FWD-17'S COUNT IS PERSON-READABLE (round-13 analysis ruling 8, s.4 row 7; FWD-17,
 * FWD-20).
 *
 * Usage (repo root): node <this file>
 * Ruling 8: "fwd17's render run adds an OPENED-fold PNG, so its cite count is person-readable." Row 7's criterion: "the render run
 * writes `posture-cites-open.png`, and its count equals `grades.json`." The base instrument grades fwd17 on posture with
 * citesFolded 20 / unresolvedCites 8, but those cites sit inside folds the at-rest `posture.png` never opens, so no person can check
 * the count against a picture.
 * THE OUTPUT CONTRACT (AV-k-7's face): `node portal/scripts/ui-contract-check.mjs --dist <dir> --out <dir> --states-sweep` writes,
 * beside grades.json, `<out>/posture-cites-open.png` (every cite fold opened) and `<out>/posture-cites-open.json`
 * { grade: PASS|FAIL|NOT_EXERCISED, png, pngBytes, visibleCites, visibleUnresolved, fwd17: { citesFolded, unresolvedCites }, ... }
 * -- the cites VISIBLE in that shot. This check reads the counts from the sidecar and the fwd17 counts from grades.json itself.
 * Inputs: C:/tmp/dsgn-r13-dist/final (the page bytes of 118cd005 -- the BASE page; the cell changes only the instrument);
 * C:/tmp/dsgn-r13-close-render/{grades.json,posture.png} (the round-13 close run on the base, the reference for arm 2);
 * round14/checks/dists/blank (the issuer's blank page); a PLANTED posture page this check writes under os.tmpdir().
 * Arms:
 *   1  the opened-fold PNG is written and its count equals grades.json: on the base page the PNG exists (>= 10000 bytes, taller
 *      than the at-rest posture.png), the sidecar grades PASS, and its visible cites and visible UNRESOLVED cites equal grades.json
 *      fwd17's citesFolded and unresolvedCites, both > 0
 *   2  the at-rest run is unchanged in kind (a control -- passes on the base instrument by design): posture.png has the base close
 *      run's dimensions (folds closed), fwd17 is still graded PASS, every grades.json cell of the base close run is present and
 *      graded, no new cell appears, and the result tallies the same number of cells (issuer amendment at the cut: shape, not
 *      values -- the round's other cells move values by design)
 *   3  never a count equal by accident (NEGATIVE control): on the blank page the sidecar grades NOT_EXERCISED; on the planted page
 *      (3 folded cites, one hidden once its fold opens) the sidecar grades FAIL with 2 visible against citesFolded 3; neither PASS,
 *      and a missing sidecar fails the arm (the instrument must say so, not stay silent)
 * Prints one line per arm and "FWD-17'S COUNT IS PERSON-READABLE: <k> of 3 arms"; exit 0 only at 3 of 3.
 * No network, no AWS. Writes only under os.tmpdir() (the runs' --out dirs and the planted page).
 */
const fs = require('fs');
const os = require('os');
const path = require('path');
const { spawnSync } = require('child_process');

const ROOT = process.cwd();
const PORTAL = path.join(ROOT, 'portal');
const CHECKS = path.join(ROOT, 'org/missions/D13/DSGN/DSGN_AMGTV1/deliverables/2.0.0_SA_COO~D/round14/checks');
const BASE_RUN = 'C:/tmp/dsgn-r13-close-render';
const OUT = fs.mkdtempSync(path.join(os.tmpdir(), 'r14-foldopen-'));

// The planted posture page: two folded reasons, three cites; cite B is hidden once its fold opens, so the opened shot shows 2.
const PLANTED = path.join(OUT, 'planted-dist');
fs.mkdirSync(PLANTED, { recursive: true });
fs.writeFileSync(path.join(PLANTED, 'index.html'), `<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>PLANTED posture -- one cite hidden once opened (foldopen.cjs)</title>
<style>body{margin:0;background:#fff;font-family:Lato,sans-serif;color:rgb(10,23,51)} main{padding:16px}
details[open] li.gone{display:none} svg{width:12px;height:12px;stroke:rgb(217,119,6)}</style></head>
<body><main>
<button role="tab" type="button">Posture</button>
<div data-tab-panel="posture">
<section data-posture-verdict="hold"><p>HOLD -- planted verdict card for the opened-fold control.</p><p data-posture-comparable="DE_US_Equity">Comparable: Deere</p></section>
<ol>
<li data-posture-claim="1"><p>Planted reason one, resting on two cites.</p><details><summary>cites 2</summary><ul>
<li data-posture-cite="A" data-cite-resolved="true"><span>Planted resolved cite A.</span></li>
<li class="gone" data-posture-cite="B" data-cite-resolved="false"><svg></svg><span>Citation not resolved -- planted cite B.</span></li>
</ul></details></li>
<li data-posture-claim="2"><p>Planted reason two, resting on one cite.</p><details><summary>cites 1</summary><ul>
<li data-posture-cite="C" data-cite-resolved="false"><svg></svg><span>Citation not resolved -- planted cite C.</span></li>
</ul></details></li>
</ol></div></main></body></html>
`);

const DIST = { final: 'C:/tmp/dsgn-r13-dist/final', blank: path.join(CHECKS, 'dists/blank'), planted: PLANTED };
for (const [k, d] of Object.entries(DIST)) if (!fs.existsSync(path.join(d, 'index.html'))) { console.log(`INPUT MISSING: ${k} at ${d}`); process.exit(3); }
for (const f of ['grades.json', 'posture.png']) if (!fs.existsSync(path.join(BASE_RUN, f))) { console.log(`INPUT MISSING: ${BASE_RUN}/${f}`); process.exit(3); }

const readJson = (p) => { try { return JSON.parse(fs.readFileSync(p, 'utf8')); } catch (e) { return null; } };
const pngDims = (p) => { try { const b = fs.readFileSync(p); return b.length > 24 && b.toString('ascii', 12, 16) === 'IHDR' ? { w: b.readUInt32BE(16), h: b.readUInt32BE(20), bytes: b.length } : null; } catch (e) { return null; } };
function run(name, extra) {
  const out = path.join(OUT, name);
  const args = ['scripts/ui-contract-check.mjs', '--dist', DIST[name], '--out', out, ...extra];
  const r = spawnSync(process.execPath, args, { cwd: PORTAL, encoding: 'utf8', timeout: 840000 });
  return { rc: r.status, out, grades: readJson(path.join(out, 'grades.json')), side: readJson(path.join(out, 'posture-cites-open.json')), tail: String(r.stdout || '').trim().split('\n').slice(-1).join('') + String(r.stderr || '').trim().split('\n').slice(-1).join('') };
}
const f17 = (res) => ((((res.grades || {}).states || {}).posture || {}).fwd17_verdictComparable) || null;

const t0 = Date.now();
const fin = run('final', ['--states-sweep']);
const blank = run('blank', ['--states', 'posture']);
const planted = run('planted', ['--states', 'posture']);
const secs = Math.round((Date.now() - t0) / 1000);

// ---- arm 1 ------------------------------------------------------------------------------------------------------------------
const f1 = [];
const c17 = f17(fin);
const open = pngDims(path.join(fin.out, 'posture-cites-open.png'));
const rest = pngDims(path.join(fin.out, 'posture.png'));
if (!fin.grades) f1.push(`no grades.json (rc=${fin.rc}; ${fin.tail.slice(0, 160)})`);
else if (!c17 || typeof c17.value !== 'object') f1.push(`fwd17 not graded with counts (${JSON.stringify(c17).slice(0, 120)})`);
if (!open) f1.push('posture-cites-open.png was not written');
else if (open.bytes < 10000) f1.push(`posture-cites-open.png is trivial (${open.bytes} bytes)`);
else if (rest && !(open.h > rest.h)) f1.push(`the opened shot (${open.h}px) is not taller than the at-rest posture.png (${rest.h}px): the folds did not open`);
if (!fin.side) f1.push('posture-cites-open.json (the visible count) was not written');
else if (c17 && typeof c17.value === 'object') {
  const v = c17.value;
  if (!(v.citesFolded > 0) || !(v.unresolvedCites > 0)) f1.push(`grades.json fwd17 counts are not positive (citesFolded ${v.citesFolded}, unresolvedCites ${v.unresolvedCites})`);
  if (fin.side.visibleCites !== v.citesFolded) f1.push(`${fin.side.visibleCites} cites visible in the shot, grades.json citesFolded ${v.citesFolded}`);
  if (fin.side.visibleUnresolved !== v.unresolvedCites) f1.push(`${fin.side.visibleUnresolved} UNRESOLVED visible in the shot, grades.json unresolvedCites ${v.unresolvedCites}`);
  if (fin.side.grade !== 'PASS') f1.push(`the sidecar grades ${fin.side.grade} (${JSON.stringify(fin.side.failing || fin.side.unseen || '')})`);
}
const a1 = f1.length === 0;
const a1d = a1 ? `posture-cites-open.png ${open.bytes} bytes, ${open.w}x${open.h} (at rest ${rest ? rest.h : '?'}px); visible cites ${fin.side.visibleCites} == citesFolded ${c17.value.citesFolded}, visible UNRESOLVED ${fin.side.visibleUnresolved} == unresolvedCites ${c17.value.unresolvedCites}; sidecar PASS` : `${f1.length} failing; first: ${f1[0]}`;

// ---- arm 2 ------------------------------------------------------------------------------------------------------------------
const f2 = [];
const base = readJson(path.join(BASE_RUN, 'grades.json'));
const baseRest = pngDims(path.join(BASE_RUN, 'posture.png'));
if (!rest) f2.push('posture.png was not written');
else if (!baseRest || rest.w !== baseRest.w || rest.h !== baseRest.h) f2.push(`posture.png is ${rest.w}x${rest.h}, the base close run's is ${baseRest ? baseRest.w + 'x' + baseRest.h : 'unreadable'}`);
if (!c17 || c17.grade !== 'PASS') f2.push(`fwd17 reads ${c17 ? c17.grade : 'MISSING'}, the base close run's PASS`);
// Issuer amendment at the cut (queue-aware bases): the at-rest run is compared with the base close run by its SHAPE -- the set of
// graded cells, every one still carrying a grade -- never by VALUES, since the round's other cells (k-2's standalone capture, k-3's
// peers empty patch) move grade values by design once they drain. The opened-fold count lives in the sidecar, so no new cell appears.
let cells = 0;
if (fin.grades && base) {
  const diffs = [];
  for (const st of Object.keys(base.states)) for (const c of Object.keys(base.states[st])) {
    cells += 1;
    const cell = ((fin.grades.states || {})[st] || {})[c];
    if (cell === undefined) diffs.push(`${st}/${c}: cell missing`);
    else if (cell && typeof cell === 'object' && 'grade' in (base.states[st][c] || {}) && !cell.grade) diffs.push(`${st}/${c}: no grade`);
  }
  for (const st of Object.keys(fin.grades.states || {})) for (const c of Object.keys(fin.grades.states[st])) if (!(base.states[st] && c in base.states[st])) diffs.push(`${st}/${c}: new cell`);
  for (const k of ['fourStates', 'fwd19_designedStates']) { cells += 1; if (!((fin.grades.run || {})[k])) diffs.push(`run.${k} missing`); }
  const tally = fin.grades.result || {};
  const total = ['PASS', 'FAIL', 'NOT_EXERCISED', 'N/A'].reduce((s, k) => s + (Number(tally[k]) || 0), 0);
  const baseTotal = ['PASS', 'FAIL', 'NOT_EXERCISED', 'N/A'].reduce((s, k) => s + (Number((base.result || {})[k]) || 0), 0);
  if (total !== baseTotal) diffs.push(`result counts ${total} graded cells, the base close run ${baseTotal}`);
  f2.push(...diffs);
} else f2.push(`grades.json unreadable (run ${!!fin.grades}, base ${!!base})`);
const a2 = f2.length === 0;
const a2d = a2 ? `posture.png ${rest.w}x${rest.h} == base; fwd17 PASS; ${cells} grades.json cells present and graded, no new cell, result totals ${JSON.stringify(fin.grades.result)} over the base's cell count` : `${f2.length} failing; first: ${f2[0]}`;

// ---- arm 3 ------------------------------------------------------------------------------------------------------------------
const f3 = [];
if (!blank.side) f3.push(`blank: no posture-cites-open.json (rc=${blank.rc}) -- the instrument is silent on a blind read`);
else if (blank.side.grade !== 'NOT_EXERCISED') f3.push(`blank: the sidecar grades ${blank.side.grade}, want NOT_EXERCISED`);
if (!planted.side) f3.push(`planted: no posture-cites-open.json (rc=${planted.rc})`);
else {
  const pv = (f17(planted) || {}).value || {};
  if (planted.side.grade !== 'FAIL') f3.push(`planted: the sidecar grades ${planted.side.grade} (visible ${planted.side.visibleCites}, citesFolded ${pv.citesFolded}), want FAIL`);
  if (!(planted.side.visibleCites === 2 && pv.citesFolded === 3)) f3.push(`planted: visible ${planted.side.visibleCites} / citesFolded ${pv.citesFolded}, want 2 / 3 (the plant did not read as planted)`);
}
const a3 = f3.length === 0;
const a3d = a3 ? `blank sidecar NOT_EXERCISED (${JSON.stringify(blank.side.unseen || '').slice(0, 80)}); planted sidecar FAIL, visible ${planted.side.visibleCites} vs citesFolded 3 (${JSON.stringify(planted.side.failing || '').slice(0, 90)})` : `${f3.length} failing; first: ${f3[0]}`;

console.log(`RUNS: final rc=${fin.rc} blank rc=${blank.rc} planted rc=${planted.rc} in ${secs}s (out ${OUT})`);
const arms = [
  ['the opened-fold PNG is written and its count equals grades.json', a1, a1d],
  ['the at-rest run is unchanged (control)', a2, a2d],
  ['never a count equal by accident (blank, planted)', a3, a3d],
];
let pass = 0;
for (const [name, ok, detail] of arms) { if (ok) pass += 1; console.log(`${ok ? 'ARM PASS' : 'ARM FAIL'} ${name} :: ${detail}`); }
console.log(`FWD-17'S COUNT IS PERSON-READABLE: ${pass} of ${arms.length} arms`);
process.exit(pass === arms.length ? 0 : 1);
