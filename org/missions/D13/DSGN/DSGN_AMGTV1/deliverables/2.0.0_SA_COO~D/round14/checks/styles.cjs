/**
 * styles.cjs -- DSGN_AMGTV1 round 14, AV-k-6: SIZES AND RADII MEET C1 AND C11 (round-13 analysis ruling 8; FWD-20).
 *
 * Usage (repo root): node <this file>
 * Ruling 8: "`sizes` and `radii` (10px YAxis, 9999px badge, 12 dots) are graded against C1 and C11 as round-14 styling." The
 * CTO's criterion (section 4 row 6): `sizes` and `radii` PASS on the render run. The instrument's clauses (portal/scripts/
 * ui-contract-check.mjs PREDICATES): `sizes` rejects any rendered text below 11px (DESIGN.md's smallest type token, footnote
 * 0.6875rem = 11px); `radii` accepts 2px / 3px / 4px and a pill (>= 9999px) and rejects everything else (C11: "Radii are 2, 3 and
 * 4px -- or a pill"). On the base the rejected values are the header timeline's Y-axis ticks at 10px and its three legend
 * swatches at 1px; the pills (a 3px page rule, the Exec confirmed dots) are accepted by the clause.
 * Inputs: <cwd>/portal (built here into os.tmpdir() by `vite build --configLoader runner`), its uiContractFixtures.json, and the
 * base page build C:/tmp/dsgn-r13-dist/final (the page bytes of 118cd005).
 * Arms:
 *   1  the criterion: one `ui-contract-check.mjs --dist <this build> --states-sweep` run grades `sizes` and `radii` PASS in all six
 *      states (list, thesis, exec, peers, model, posture) of grades.json
 *   2  nothing was deleted, and the shapes are C11's: on the same build (ui-smoke.mjs) the timeline's Y-axis tick labels are
 *      visible at >= 11px; its three legend swatches are visible at 2/3/4px; the Thesis window's MACHINE chip is visible at
 *      2/3/4px (C11: chips take rounded.xs, the pill is for status dots and avatars only); the Exec confirmed dots are visible
 *      and still a pill (status dots)
 *   3  the negative: the base build, graded by the same instrument (thesis and exec), reads `sizes` FAIL with 10 below 11 and
 *      `radii` FAIL, so the clauses can say no on the named defects
 * The base run (arm 3) runs concurrently with the build and the graded run. Writes only under os.tmpdir() (the build and the
 * instrument's out folders). No network, no AWS.
 * Prints one line per arm and "SIZES AND RADII MEET C1 AND C11: <k> of 3 arms"; exit 0 only at 3 of 3.
 */
const fs = require('fs');
const os = require('os');
const path = require('path');
const { spawn } = require('child_process');

const ROOT = process.cwd();
const PORTAL = path.join(ROOT, 'portal');
const BASE = 'C:/tmp/dsgn-r13-dist/final';
const FIX = 'src/pages/SecurityAnalysis/__harness__/tests/uiContractFixtures.json';
const ROUTE = '/security-analysis/BA_US_Equity';
const STATES = ['list', 'thesis', 'exec', 'peers', 'model', 'posture'];
const OUT = fs.mkdtempSync(path.join(os.tmpdir(), 'r14-styles-'));
const T0 = Date.now();

function run(args, timeoutMs) {
  return new Promise((resolve) => {
    const p = spawn(process.execPath, args, { cwd: PORTAL, windowsHide: true });
    let out = '';
    p.stdout.on('data', (d) => { out += d; });
    p.stderr.on('data', (d) => { out += d; });
    const t = setTimeout(() => { try { p.kill(); } catch (e) { /* gone */ } }, timeoutMs);
    p.on('close', (code) => { clearTimeout(t); resolve({ rc: code, out }); });
    p.on('error', (e) => { clearTimeout(t); resolve({ rc: -1, out: String(e.message) }); });
  });
}
const readGrades = (dir) => { try { return JSON.parse(fs.readFileSync(path.join(dir, 'grades.json'), 'utf8')); } catch (e) { return null; } };
const tail = (s) => String(s || '').trim().split('\n').slice(-1).join('').slice(0, 140);

// One ui-smoke capture; returns { visible: {sel: n}, style: {"sel::prop": value|null} }.
async function smoke(dist, name, clicks, visibleSels, styleSpecs) {
  const args = ['scripts/ui-smoke.mjs', '--dist', dist, '--route', ROUTE, '--out', path.join(OUT, `smoke-${name}.png`), '--fixtures', FIX];
  for (const c of clicks) args.push('--click', c);
  for (const s of visibleSels) args.push('--expect', s);
  for (const s of styleSpecs) args.push('--expect-style', s);
  const r = await run(args, 180000);
  const visible = {};
  const style = {};
  for (const line of r.out.split('\n')) {
    let m = /^EXPECT\[(.*)\]: (?:PASS|FAIL) \((\d+) visible\)/.exec(line.trim());
    if (m) { visible[m[1]] = Number(m[2]); continue; }
    m = /^EXPECT-STYLE\[(.*)\]: (PASS|FAIL|UNMEASURABLE) ?(.*)$/.exec(line.trim());
    if (m) style[m[1]] = m[2] === 'UNMEASURABLE' ? null : m[3].trim();
  }
  return { rc: r.rc, visible, style, clicked: clicks.every((c) => r.out.includes(`CLICKED: ${c}`)), tail: tail(r.out) };
}

async function greenSide() {
  const dist = path.join(OUT, 'dist');
  const b = await run(['node_modules/vite/bin/vite.js', 'build', '--configLoader', 'runner', '--outDir', dist], 600000);
  if (!fs.existsSync(path.join(dist, 'index.html'))) return { build: b, dist: null };
  const gOut = path.join(OUT, 'green');
  const g = await run(['scripts/ui-contract-check.mjs', '--dist', dist, '--out', gOut, '--states-sweep'], 900000);
  const TICK = '[data-timeline-panel] svg text';
  const SW = '[data-timeline-legend-swatch]';
  const CHIP = '[data-drafted-sentence] > p > span:first-child';
  const DOT = '[data-exec-confirmed-dot]';
  const [thesis, chip, exec] = await Promise.all([
    smoke(dist, 'thesis', [], [TICK, SW], [`${TICK}::font-size`, `${SW}::border-top-left-radius`]),
    smoke(dist, 'chip', ['Investment thesis - read more'], [CHIP], [`${CHIP}::border-top-left-radius`, `${CHIP}::text-transform`]),
    smoke(dist, 'exec', ['Exec Management'], [DOT], [`${DOT}::border-top-left-radius`]),
  ]);
  return { build: b, dist, g, grades: readGrades(gOut), thesis, chip, exec, sel: { TICK, SW, CHIP, DOT } };
}
async function baseSide() {
  if (!fs.existsSync(path.join(BASE, 'index.html'))) return { missing: true };
  const bOut = path.join(OUT, 'base');
  const r = await run(['scripts/ui-contract-check.mjs', '--dist', BASE, '--out', bOut, '--states', 'thesis,exec'], 600000);
  return { r, grades: readGrades(bOut) };
}

(async () => {
  const [G, B] = await Promise.all([greenSide(), baseSide()]);
  const px = (v) => (v == null ? NaN : parseFloat(v));
  const c11 = (v) => ['2px', '3px', '4px'].includes(v);

  // ---- arm 1: sizes and radii PASS in all six states ----------------------------------------------------------------------
  const f1 = [];
  if (!G.dist) f1.push(`the page did not build (rc=${G.build.rc}; ${tail(G.build.out)})`);
  else if (!G.grades) f1.push(`no grades.json from the graded run (rc=${G.g.rc}; ${tail(G.g.out)})`);
  const seen = [];
  if (G.grades) {
    const st = G.grades.states || {};
    for (const s of STATES) {
      const c = st[s] || {};
      for (const k of ['sizes', 'radii']) {
        if (!c[k]) f1.push(`${s}: no ${k} clause`);
        else if (c[k].grade !== 'PASS') f1.push(`${s}: ${k} ${c[k].grade} ${JSON.stringify(c[k].value)}`);
      }
      if (c.sizes && c.radii) seen.push(`${s} smallest ${((c.sizes.value || {}).smallest)}px radii ${JSON.stringify(c.radii.value)}`);
    }
  }
  const a1 = f1.length === 0;
  const a1d = a1 ? `12 of 12 cells PASS (sizes, radii x 6 states); ${seen.slice(0, 3).join('; ')}; ...` : `${f1.length} failing; first: ${f1[0]}`;

  // ---- arm 2: the axis, the swatches, the chip and the dots still render, at C11 shapes -----------------------------------------
  const f2 = [];
  let a2d = '';
  if (!G.dist) f2.push('no build');
  else {
    const { TICK, SW, CHIP, DOT } = G.sel;
    const tickN = G.thesis.visible[TICK] || 0;
    const tickPx = px(G.thesis.style[`${TICK}::font-size`]);
    const swN = G.thesis.visible[SW] || 0;
    const swR = G.thesis.style[`${SW}::border-top-left-radius`];
    const chipN = G.chip.visible[CHIP] || 0;
    const chipR = G.chip.style[`${CHIP}::border-top-left-radius`];
    const chipUp = G.chip.style[`${CHIP}::text-transform`];
    const dotN = G.exec.visible[DOT] || 0;
    const dotR = px(G.exec.style[`${DOT}::border-top-left-radius`]);
    if (tickN < 1) f2.push(`the timeline Y axis renders no tick label (${tickN} visible; ${G.thesis.tail})`);
    else if (!(tickPx >= 11)) f2.push(`the Y-axis tick labels render at ${G.thesis.style[`${TICK}::font-size`]}`);
    if (swN !== 3) f2.push(`${swN} legend swatches visible, expected 3`);
    else if (!c11(swR)) f2.push(`the legend swatch radius is ${swR}`);
    if (!G.chip.clicked) f2.push('the Thesis card could not be opened');
    else if (chipN < 1 || chipUp !== 'uppercase') f2.push(`the MACHINE chip is not seen in the opened window (${chipN} visible, text-transform ${chipUp})`);
    else if (!c11(chipR)) f2.push(`the MACHINE chip radius is ${chipR} (C11: a chip takes rounded.xs 2px)`);
    if (!G.exec.clicked) f2.push('the Exec Management tab could not be opened');
    else if (dotN < 1) f2.push('no Exec confirmed dot is visible');
    else if (!(dotR >= 9999)) f2.push(`the Exec confirmed dot radius is ${G.exec.style[`${DOT}::border-top-left-radius`]}, not a pill`);
    a2d = `Y-axis ticks ${tickN} visible at ${G.thesis.style[`${TICK}::font-size`]}; swatches ${swN} at ${swR}; MACHINE chip ${chipN} at ${chipR}; Exec dots ${dotN} at ${G.exec.style[`${DOT}::border-top-left-radius`]}`;
  }
  const a2 = f2.length === 0;
  const a2dd = a2 ? a2d : `${f2.length} failing; first: ${f2[0]}${a2d ? ` (${a2d})` : ''}`;

  // ---- arm 3: the negative -- the base reads sizes FAIL (10) and radii FAIL -------------------------------------------------------
  const f3 = [];
  const n3 = [];
  if (B.missing) f3.push(`the base build is missing at ${BASE}`);
  else if (!B.grades) f3.push(`no grades.json from the base run (rc=${B.r.rc}; ${tail(B.r.out)})`);
  else {
    for (const s of ['thesis', 'exec']) {
      const c = (B.grades.states || {})[s] || {};
      const sz = c.sizes || {};
      const rd = c.radii || {};
      if (sz.grade !== 'FAIL' || !((sz.value || {}).below11 || []).includes(10)) f3.push(`base ${s}: sizes ${sz.grade} ${JSON.stringify(sz.value)}`);
      if (rd.grade !== 'FAIL') f3.push(`base ${s}: radii ${rd.grade} ${JSON.stringify(rd.value)}`);
      n3.push(`${s} sizes ${sz.grade} ${JSON.stringify((sz.value || {}).below11)} radii ${rd.grade}`);
    }
  }
  const a3 = f3.length === 0;
  const a3d = a3 ? `the base is caught: ${n3.join('; ')}` : `${f3.length} failing; first: ${f3[0]}`;

  console.log(`RUNS: build rc=${G.build.rc} graded rc=${G.g ? G.g.rc : 'n/a'} base rc=${B.r ? B.r.rc : 'n/a'}; wall ${Math.round((Date.now() - T0) / 1000)}s (out ${OUT})`);
  const arms = [
    ['the criterion: sizes and radii PASS in all six states of the graded run', a1, a1d],
    ['nothing deleted: axis ticks, swatches, MACHINE chip and Exec dots render at C1/C11 shapes', a2, a2dd],
    ['the negative: the base build reads sizes and radii FAIL', a3, a3d],
  ];
  let pass = 0;
  for (const [name, ok, detail] of arms) { if (ok) pass += 1; console.log(`${ok ? 'ARM PASS' : 'ARM FAIL'} ${name} :: ${detail}`); }
  console.log(`SIZES AND RADII MEET C1 AND C11: ${pass} of ${arms.length} arms`);
  process.exit(pass === arms.length ? 0 : 1);
})();
