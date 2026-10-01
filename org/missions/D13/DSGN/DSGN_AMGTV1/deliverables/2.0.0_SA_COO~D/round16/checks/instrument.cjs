/**
 * instrument.cjs -- DSGN_AMGTV1 round 16, cell g-3: THE RENDER SEES THE DEMO FACES (CTO round-15 analysis ruling 2: the
 * render instrument must see the demo faces before any face is graded again) (issuer 2.0.0_SA_COO~D).
 *
 * THE CONTRACT the worker builds to (quote it in the task order). The render instrument is portal/scripts/
 * ui-contract-check.mjs (+ scripts/ui-measure.mjs) and its fixture set src/pages/SecurityAnalysis/__harness__/tests/
 * uiContractFixtures.json. Run as `ui-contract-check.mjs --dist <build> --out <dir> --states list --states-sweep`:
 *   - the fixtures serve `/api/scoped/amgt/lead-panel/timeseries/collected/chatter` with EXACTLY the payload of
 *     round16/fixtures/r16g.collected.chatter.json (AMGT_RESAPP's live shape: 95 covered names, 73 with an empty by_month,
 *     by_publisher only publishers with >= 1 article), and the trending price ranking the Price face reads;
 *   - the sweep writes, beside its other captures, `<out>/list-price.png` + `<out>/list-price.json` (the Price segment
 *     clicked; the JSON's `expectLine` is ui-smoke's `EXPECT[[data-price-bar]]: ... (<n> visible)`) and
 *     `<out>/list-chatter.png` + `<out>/list-chatter.json` (the default Chatter face; `expectLine` for `[data-bubble]`, and
 *     `denominator.line` ui-smoke's `EXPECT-TEXT[[data-chatter-denominator]::<k> of 95 covered names]: PASS`);
 *   - grades.json `states.list.fwd18_controls` reads PASS with the Movement clause retired (ruling R6: no Movement control)
 *     and `states.list.bandIsIdentityHeader` reads PASS, the band anchored to the new header card ([data-panel-header]);
 *   - grades.json `run.fwd19_designedStates.value.missing` names no `list/` entry (list's loading is the chatter read held).
 *
 * Usage (repo root): node <this file>        (portal/ under the cwd is the checkout under test; ~5 minutes)
 * Arms:
 *   1  THE CHECKOUT: vite-build portal/ into os.tmpdir(); run the checkout's own instrument on that build (--states list
 *      --states-sweep); every clause above holds: FIXTURE (the served chatter payload equals r16g), PRICE (a price-face PNG
 *      with >= 1 [data-price-bar] in its DOM capture), CHATTER (a chatter-face PNG whose DOM capture shows exactly the k
 *      bubbles r16g collects in its latest month, k >= 1, and the denominator "<k> of 95 covered names"), FWD18, BAND, FWD19.
 *   2  NEGATIVE: the BASE instrument (portal f4adf790: its scripts/ and src/ extracted to os.tmpdir(), node_modules a
 *      junction) on the SAME build fails arm 1's predicates, with the PRICE and CHATTER faces among the reasons; every
 *      failing class is named.
 *   3  PLANTED: the same build with five defects planted into its bytes (a 7px font on the Starred filter; the active
 *      Subject segment filled purple; the header card's data-panel-header attribute renamed; the price bars'
 *      data-price-bar attribute renamed; the denominator's "covered names" words changed) is graded by the CHECKOUT's
 *      instrument, which must FAIL each: sizes (7 in below11, absent in arm 1's run), fwd18 (Subject filled), band, the
 *      price face, the chatter face -- so the re-anchoring did not blind it.
 * Blind spots: only the Universe (list) state is run -- the five Security states are not re-graded here (the close render
 * and headerchrome.cjs grade them); the base instrument run (arm 2) has no chatter fixture, so its chatter read goes out to
 * the API host as at the round-15 close (no credentials; it fails, which is the point); the instrument's counts are read
 * from its own JSON (arm 3 is what shows they can fail); `renderCheck.tsx`'s 'Lead Panel' substring is not graded here.
 * Writes only under os.tmpdir() (the build, three renders, the base extract). No AWS.
 * Wall time measured on site Z (2026-10-01): see the WALL line.
 * Prints one line per arm and "THE RENDER SEES THE DEMO FACES: <k> of 3 arms"; exit 0 only at 3 of 3.
 */
const fs = require('fs');
const os = require('os');
const path = require('path');
const { spawnSync, execFileSync } = require('child_process');

const T0 = Date.now();
const ROOT = process.cwd();
const PORTAL = path.join(ROOT, 'portal');
const PIN = 'f4adf790';
const COLLECTED_KEY = '/api/scoped/amgt/lead-panel/timeseries/collected/chatter';
const FIXTURES_REL = 'src/pages/SecurityAnalysis/__harness__/tests/uiContractFixtures.json';
const R16G = path.join(__dirname, '..', 'fixtures', 'r16g.collected.chatter.json');

if (!fs.existsSync(path.join(PORTAL, 'package.json'))) {
  console.log('CHECK ERROR: no portal/package.json under ' + ROOT + ' -- run from the repository root');
  process.exit(3);
}
const WANT = JSON.parse(fs.readFileSync(R16G, 'utf8'));
const LATEST = WANT.months[WANT.months.length - 1];
const K = WANT.rows.filter((r) => r.by_month[LATEST]).length;
const N = WANT.rows.length;
const N_EMPTY = WANT.rows.filter((r) => Object.keys(r.by_month).length === 0).length;
const secs = (t) => ((Date.now() - t) / 1000).toFixed(0) + 's';
const TMP = fs.mkdtempSync(path.join(os.tmpdir(), 'r16g-instrument-'));

function canon(v) {
  if (Array.isArray(v)) return '[' + v.map(canon).join(',') + ']';
  if (v && typeof v === 'object') return '{' + Object.keys(v).sort().map((k) => JSON.stringify(k) + ':' + canon(v[k])).join(',') + '}';
  return JSON.stringify(v);
}
const readJson = (f) => { try { return JSON.parse(fs.readFileSync(f, 'utf8')); } catch (e) { return null; } };
const visibleOf = (line) => Number((/\((\d+) visible\)/.exec(line || '') || [])[1] || 0);

// ---------------- the predicates over one render directory ----------------
function gradeRender(out, fixturesFile) {
  const faults = [];
  const info = {};
  const fx = readJson(fixturesFile);
  const served = fx ? fx[COLLECTED_KEY] : null;
  if (!served) faults.push(`FIXTURE: the instrument's fixtures serve no ${COLLECTED_KEY}`);
  else if (canon(served) !== canon(WANT)) faults.push(`FIXTURE: the served chatter payload is not r16g (${(served.rows || []).length} rows served)`);
  if (N !== 95 || N_EMPTY !== 73) faults.push(`FIXTURE: r16g itself is not the live shape (${N} rows, ${N_EMPTY} empty)`);
  const grades = readJson(path.join(out, 'grades.json'));
  if (!grades) {
    faults.push('RENDER: no grades.json written');
    return { faults, info };
  }
  const price = readJson(path.join(out, 'list-price.json'));
  const pricePng = path.join(out, 'list-price.png');
  info.priceBars = price ? visibleOf(price.expectLine) : 0;
  if (!fs.existsSync(pricePng) || !(fs.statSync(pricePng).size > 0)) faults.push('PRICE: no price-face PNG (list-price.png)');
  if (!price) faults.push('PRICE: no price-face DOM capture (list-price.json)');
  else if (!(info.priceBars >= 1)) faults.push(`PRICE: the price-face capture shows ${info.priceBars} [data-price-bar] (${String(price.expectLine || '').slice(0, 80)})`);
  const chat = readJson(path.join(out, 'list-chatter.json'));
  const chatPng = path.join(out, 'list-chatter.png');
  info.bubbles = chat ? visibleOf(chat.expectLine) : 0;
  if (!fs.existsSync(chatPng) || !(fs.statSync(chatPng).size > 0)) faults.push('CHATTER: no chatter-face PNG (list-chatter.png)');
  if (!chat) faults.push('CHATTER: no chatter-face DOM capture (list-chatter.json)');
  else {
    if (!/\[data-bubble\]/.test(chat.expectLine || '')) faults.push('CHATTER: the capture did not count [data-bubble]');
    else if (info.bubbles !== K) faults.push(`CHATTER: ${info.bubbles} bubbles visible, r16g collects ${K} names in ${LATEST}`);
    const line = chat.denominator && chat.denominator.line ? chat.denominator.line : '';
    info.denominator = line;
    if (!line.includes(`${K} of ${N} covered names`) || !/: PASS/.test(line)) faults.push(`CHATTER: the denominator "${K} of ${N} covered names" is not read on the face (${line.slice(0, 90) || 'no line'})`);
  }
  const list = (grades.states || {}).list || {};
  const f18 = list.fwd18_controls || {};
  info.fwd18 = f18.grade;
  if (f18.grade !== 'PASS') faults.push(`FWD18: list.fwd18_controls ${f18.grade || 'absent'} ${JSON.stringify((f18.value || {}).failing || f18.value || null).slice(0, 140)}`);
  const band = list.bandIsIdentityHeader || {};
  info.band = band.grade;
  if (band.grade !== 'PASS') faults.push(`BAND: list.bandIsIdentityHeader ${band.grade || 'absent'} ${JSON.stringify(band.value || null).slice(0, 120)}`);
  const f19 = ((grades.run || {}).fwd19_designedStates) || {};
  const missing = f19.value && Array.isArray(f19.value.missing) ? f19.value.missing : null;
  info.fwd19 = f19.grade;
  if (!missing) faults.push(`FWD19: run.fwd19_designedStates carries no missing list (${f19.grade || 'absent'})`);
  else if (missing.some((m) => /^list\//.test(m))) faults.push(`FWD19: missing ${missing.filter((m) => /^list\//.test(m)).join(', ')}`);
  info.sizesBelow11 = ((list.sizes || {}).value || {}).below11 || null;
  return { faults, info };
}
const classesOf = (faults) => { const c = {}; for (const x of faults) { const k = x.split(':')[0]; c[k] = (c[k] || 0) + 1; } return c; };

function build(dist) {
  const vite = path.join(PORTAL, 'node_modules', 'vite', 'bin', 'vite.js');
  return spawnSync(process.execPath, [vite, 'build', '--configLoader', 'runner', '--outDir', dist, '--emptyOutDir'], { cwd: PORTAL, encoding: 'utf8', timeout: 15 * 60 * 1000, maxBuffer: 256 << 20 });
}
function instrument(portalDir, dist, out) {
  return spawnSync(process.execPath, ['scripts/ui-contract-check.mjs', '--dist', dist, '--out', out, '--states', 'list', '--states-sweep'], { cwd: portalDir, encoding: 'utf8', timeout: 30 * 60 * 1000, maxBuffer: 256 << 20 });
}

// ---------------- arm 1: the checkout ----------------
const DIST = path.join(TMP, 'dist');
const head = (() => { try { return execFileSync('git', ['-C', PORTAL, 'rev-parse', '--short', 'HEAD'], { encoding: 'utf8' }).trim(); } catch (e) { return '?'; } })();
let a1 = false;
let a1d = '';
let g1 = null;
const tb = Date.now();
const b = build(DIST);
const buildSecs = secs(tb);
const built = b.status === 0 && fs.existsSync(path.join(DIST, 'index.html'));
if (!built) a1d = `vite build rc=${b.status}: ${String(b.stderr || b.stdout || '').trim().split('\n').slice(-2).join(' ')}`;
else {
  const t = Date.now();
  instrument(PORTAL, DIST, path.join(TMP, 'checkout'));
  g1 = gradeRender(path.join(TMP, 'checkout'), path.join(PORTAL, FIXTURES_REL));
  a1 = g1.faults.length === 0;
  a1d = a1
    ? `portal ${head} built in ${buildSecs}, rendered in ${secs(t)}: price face ${g1.info.priceBars} [data-price-bar]; chatter face ${g1.info.bubbles} bubbles from r16g (${N} rows, ${N_EMPTY} empty) and "${K} of ${N} covered names"; fwd18 ${g1.info.fwd18}, band ${g1.info.band}, fwd19 ${g1.info.fwd19} with no list/ missing -> ${path.join(TMP, 'checkout')}`
    : `portal ${head} (render ${secs(t)}): ${g1.faults.length} faults ${JSON.stringify(classesOf(g1.faults))}; ${g1.faults.slice(0, 4).join(' | ')}`;
}

// ---------------- arm 2: the base instrument on the same build ----------------
function prepareBase() {
  const dir = path.join(os.tmpdir(), `dsgn-r16g-base-${PIN}`);
  if (fs.existsSync(path.join(dir, '.complete'))) return { dir, fresh: false };
  const ls = spawnSync('git', ['-C', PORTAL, 'ls-tree', '-r', '-z', PIN, '--', 'src', 'scripts', 'package.json'], { encoding: 'utf8', maxBuffer: 64 << 20 });
  if (ls.status !== 0) throw new Error(`git ls-tree ${PIN} rc=${ls.status}: ${String(ls.stderr).trim()}`);
  const entries = ls.stdout.split('\0').filter(Boolean).map((line) => {
    const tab = line.indexOf('\t');
    const [mode, type, sha] = line.slice(0, tab).split(' ');
    return { mode, type, sha, p: line.slice(tab + 1) };
  }).filter((e) => e.type === 'blob' && e.mode !== '120000');
  if (!entries.some((e) => e.p === 'scripts/ui-contract-check.mjs')) throw new Error(`scripts/ui-contract-check.mjs is not in ${PIN}`);
  const cat = spawnSync('git', ['-C', PORTAL, 'cat-file', '--batch'], { input: entries.map((e) => e.sha).join('\n') + '\n', maxBuffer: 512 << 20 });
  if (cat.status !== 0) throw new Error(`git cat-file rc=${cat.status}`);
  const stage = fs.mkdtempSync(path.join(os.tmpdir(), `dsgn-r16g-base-${PIN}-stage-`));
  const buf = cat.stdout;
  let off = 0;
  for (const e of entries) {
    const nl = buf.indexOf(10, off);
    const header = buf.slice(off, nl).toString();
    if (/ missing$/.test(header)) throw new Error('object missing: ' + header);
    const size = Number(header.split(' ')[2]);
    const out = path.join(stage, 'portal', e.p);
    fs.mkdirSync(path.dirname(out), { recursive: true });
    fs.writeFileSync(out, buf.slice(nl + 1, nl + 1 + size));
    off = nl + 1 + size + 1;
  }
  fs.symlinkSync(fs.realpathSync(path.join(PORTAL, 'node_modules')), path.join(stage, 'portal', 'node_modules'), 'junction');
  fs.writeFileSync(path.join(stage, '.complete'), `portal ${PIN}: ${entries.length} files (src + scripts + package.json)\n`);
  try {
    fs.renameSync(stage, dir);
  } catch (e) {
    if (!fs.existsSync(path.join(dir, '.complete'))) throw e; // another check built it first: use theirs
  }
  return { dir, fresh: true };
}
let a2 = false;
let a2d = '';
if (!built) a2d = 'not run: no build';
else {
  try {
    const t = Date.now();
    const { dir, fresh } = prepareBase();
    const basePortal = path.join(dir, 'portal');
    instrument(basePortal, DIST, path.join(TMP, 'base'));
    const g = gradeRender(path.join(TMP, 'base'), path.join(basePortal, FIXTURES_REL));
    const cls = classesOf(g.faults);
    const why = [];
    if (g.faults.length === 0) why.push('the base instrument PASSES arm 1 on this build -- the predicates do not see the defect');
    if (!cls.PRICE) why.push('the base fails, but not on the PRICE face');
    if (!cls.CHATTER) why.push('the base fails, but not on the CHATTER face');
    a2 = why.length === 0;
    a2d = `${why.length ? why.join('; ') + ' || ' : ''}base instrument ${PIN} (${fresh ? 'extracted' : 'cached'}) on the same build, ${secs(t)}: ${g.faults.length} faults ${JSON.stringify(cls)}; ${g.faults.join(' | ').slice(0, 900)}`;
  } catch (e) {
    a2d = 'base extract/run failed: ' + String(e.message).split('\n')[0];
  }
}

// ---------------- arm 3: planted defects, the checkout's instrument ----------------
const PLANTS = [
  { id: 'size7', cls: 'SIZES', css: '[role="group"][aria-label="Starred filter"] button{font-size:7px!important}' },
  { id: 'fill', cls: 'FWD18', css: '[role="group"][aria-label="Subject"] button[aria-pressed="true"]{background-color:rgb(95,59,227)!important}' },
  { id: 'header', cls: 'BAND', js: ['"data-panel-header"', '"data-panel-headex"'] },
  { id: 'pricebar', cls: 'PRICE', js: ['"data-price-bar"', '"data-price-baz"'] },
  { id: 'denominator', cls: 'CHATTER', js: ['covered names have collected', 'covered nameX have collected'] },
];
let a3 = false;
let a3d = '';
if (!built || !g1) a3d = 'not run: no build or no arm-1 render';
else {
  try {
    const t = Date.now();
    const P = path.join(TMP, 'planted-dist');
    fs.cpSync(DIST, P, { recursive: true });
    const assets = path.join(P, 'assets');
    const files = fs.readdirSync(assets);
    const hits = {};
    for (const f of files) {
      const file = path.join(assets, f);
      if (f.endsWith('.css')) {
        fs.appendFileSync(file, '\n' + PLANTS.filter((p) => p.css).map((p) => p.css).join('\n') + '\n');
        for (const p of PLANTS) if (p.css) hits[p.id] = (hits[p.id] || 0) + 1;
      } else if (f.endsWith('.js')) {
        let s = fs.readFileSync(file, 'utf8');
        for (const p of PLANTS.filter((x) => x.js)) {
          const n = s.split(p.js[0]).length - 1;
          if (n) { s = s.split(p.js[0]).join(p.js[1]); hits[p.id] = (hits[p.id] || 0) + n; }
        }
        fs.writeFileSync(file, s);
      }
    }
    const unplanted = PLANTS.filter((p) => !hits[p.id]).map((p) => p.id);
    if (unplanted.length) throw new Error(`could not plant ${unplanted.join(', ')} into the build`);
    const out = path.join(TMP, 'planted');
    instrument(PORTAL, P, out);
    const g = gradeRender(out, path.join(PORTAL, FIXTURES_REL));
    const cls = classesOf(g.faults);
    const below = g.info.sizesBelow11 || [];
    const caught = [];
    const missed = [];
    for (const p of PLANTS) {
      let ok;
      if (p.cls === 'SIZES') ok = below.includes(7) && !(g1.info.sizesBelow11 || []).includes(7);
      else if (p.cls === 'FWD18') ok = g.faults.some((x) => x.startsWith('FWD18:') && /Subject/.test(x) && /filled/.test(x));
      else ok = !!cls[p.cls];
      (ok ? caught : missed).push(`${p.id}->${p.cls}`);
    }
    a3 = missed.length === 0;
    a3d = `${missed.length ? 'NOT caught: ' + missed.join(', ') + ' || ' : ''}${caught.length} of ${PLANTS.length} planted defects caught (${caught.join(', ')}); planted in ${JSON.stringify(hits)}; sizes below11 ${JSON.stringify(below)} (arm 1 ${JSON.stringify(g1.info.sizesBelow11)}); ${secs(t)} -> ${out}`;
  } catch (e) {
    a3d = 'planted run failed: ' + String(e.message).split('\n')[0];
  }
}

const arms = [
  ['THE CHECKOUT: its instrument on its build captures the price face and the chatter face from the live-shape fixture, fwd18 and the band PASS, fwd19 misses no list/ state', a1, a1d],
  [`NEGATIVE: the base instrument (portal ${PIN}) on the same build fails arm 1, the price and chatter faces among the reasons`, a2, a2d],
  ['PLANTED: a 7px text, a filled Subject segment, the header anchor, the price bars and the denominator, each planted into the build, each FAILS the checkout instrument', a3, a3d],
];
let pass = 0;
for (const [name, ok, detail] of arms) { if (ok) pass += 1; console.log(`${ok ? 'ARM PASS' : 'ARM FAIL'} ${name} :: ${detail}`); }
console.log(`WALL: ${((Date.now() - T0) / 1000).toFixed(1)}s (build ${buildSecs}); renders under ${TMP}`);
console.log(`THE RENDER SEES THE DEMO FACES: ${pass} of ${arms.length} arms`);
process.exit(pass === arms.length ? 0 : 1);
