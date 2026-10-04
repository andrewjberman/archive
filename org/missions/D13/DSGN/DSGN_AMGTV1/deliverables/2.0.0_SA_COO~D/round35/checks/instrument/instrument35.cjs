#!/usr/bin/env node
/**
 * instrument35.cjs -- DSGN_AMGTV1 round 35 issuer CHECK (2.0.0_SA_COO~D): the grader of the RE-ANCHORED render instrument
 * (portal/scripts/ui-contract-check.mjs + ui-measure.mjs + __harness__/tests/uiContractFixtures.json).
 *
 * PRD FWD-20 (v0.9): the band clause is "bandContainersTopLevel <= 1 and lightOnDark == 0" (FWD-12: no white panel, strip
 * or card inside a dark container); the instrument CAN FAIL -- on a planted page per clause beside a clean control, and on
 * the real pre-redesign page (portal 8fa7abde) on the band clause.
 *
 * RUN (repo root of the tree under test; cwd/portal = the portal under test):
 *   cd "$(git rev-parse --show-toplevel)" && node "org/missions/D13/DSGN/DSGN_AMGTV1/deliverables/2.0.0_SA_COO~D/round35/checks/instrument/instrument35.cjs"
 *
 * ENV (all optional):
 *   DIST            a built candidate dir (vite build of the tree under test). Default: build cwd/portal once into
 *                   <R35_SCRATCH>/dist-<HEAD8>[-dirty-<hash8>] (reused when present; ~20 s; product paths only -- scripts/
 *                   and __harness__/ do not enter the bundle, so an instrument-only change reuses the same dist).
 *   INSTRUMENT_DIR  the directory holding ui-contract-check.mjs / ui-measure.mjs / ui-smoke.mjs / ui-dist.mjs.
 *                   Default cwd/portal/scripts. Its parent is the instrument's portal root: the fixtures are read at
 *                   <parent>/src/pages/SecurityAnalysis/__harness__/tests/uiContractFixtures.json and every instrument
 *                   run takes cwd = <parent>. (The green proof points it at a reference re-anchor in scratch.)
 *   DIST_8FA7ABDE   the pre-redesign build. Default <R35_SCRATCH>/dist-8fa7abde; built once from `git archive 8fa7abde`
 *                   of cwd/portal when absent (never touches any checkout's HEAD).
 *   R35_SCRATCH     scratch root, default C:/tmp/r35-scratch-c. Every out dir lands under <R35_SCRATCH>/out-<stamp>/.
 *   R35_ARMS        e.g. "1,4" to run a subset while iterating; an arm not run counts as NOT RUN (never a pass).
 *
 * ARMS (each prints its evidence):
 *   1 CANDIDATE PASSES THE RE-ANCHORED CLAUSES: instrument --dist <candidate> --states-sweep; on all six states every
 *     re-anchored band clause (a state clause whose name or value names bandContainersTopLevel or lightOnDark) is PASS,
 *     lightOnDark is graded, and the graded measurement (<out>/<state>.json) reads bandContainersTopLevel <= 1 and
 *     lightOnDark == 0; run.faces.price PASS with visible == the page's own rest rule (PriceBars.tsx REST_PER_SIDE = 10:
 *     min(10, gainers) + min(10, losers) over the served return_30d_pct); run.faces.chatter PASS on the WINDOWED served
 *     shape (window_days + articles_total, RESAPP FWD-36) with visible == rows with articles_total > 0
 *     (ChatterBubbles.tsx buildCollage). Prints the grades.json result tally.
 *   2 THE BAND CLAUSE CAN FAIL ON THE REAL PRE-REDESIGN PAGE: the same instrument on dist-8fa7abde (six states, no
 *     sweep) grades a re-anchored band clause FAIL; prints the clause, its value and the measurement.
 *   3 EACH CLAUSE CAN FAIL ON A PLANTED PAGE: copies of the candidate dist with one injected script (state thesis):
 *     two dark top-level bands -> a re-anchored clause FAIL with bandContainersTopLevel >= 2; one band holding a white
 *     card and light ink -> a re-anchored clause FAIL with lightOnDark > 0 and bandContainersTopLevel <= 1; the clean
 *     control (ONE empty band, the PRD ceiling) -> every re-anchored clause PASS with bandContainersTopLevel >= 1 (the
 *     plant was seen) and lightOnDark == 0.
 *   4 NO STALE ANCHOR SURVIVES: arm 1's grades.json grades no clause named darkContainers or bandIsIdentityHeader FAIL.
 *
 * Prints "THE INSTRUMENT GRADES THE REDESIGN AND CAN FAIL: N of M arms"; exit 0 only on M of M. Runtime is printed per
 * instrument run and in total (a full run is ~13 min, dominated by arm 1's --states-sweep).
 * Writes nothing under any portal/ tree; all output goes under R35_SCRATCH.
 */
'use strict'
const { spawnSync } = require('node:child_process')
const fs = require('node:fs')
const path = require('node:path')
const crypto = require('node:crypto')

const T0 = Date.now()
const ROOT = process.cwd()
const SCRATCH = path.resolve(process.env.R35_SCRATCH || 'C:/tmp/r35-scratch-c')
const UNDER_TEST = path.join(ROOT, 'portal')
const INSTRUMENT_DIR = path.resolve(process.env.INSTRUMENT_DIR || path.join(UNDER_TEST, 'scripts'))
const INSTR_ROOT = path.dirname(INSTRUMENT_DIR)
const CHECK = path.join(INSTRUMENT_DIR, 'ui-contract-check.mjs')
const FIXTURES = path.join(INSTR_ROOT, 'src', 'pages', 'SecurityAnalysis', '__harness__', 'tests', 'uiContractFixtures.json')
const PRE_SHA = '8fa7abde'
const DIST_PRE = path.resolve(process.env.DIST_8FA7ABDE || path.join(SCRATCH, `dist-${PRE_SHA}`))
const WINDOW_CAPTURE = path.join(__dirname, '..', '..', '..', 'round31', 'fixtures', 'windows.chatter.30.json')
const STAMP = new Date().toISOString().replace(/[-:]/g, '').replace(/\.\d+Z$/, 'Z')
const OUT = path.join(SCRATCH, `out-${STAMP}`)
const SIX = ['list', 'thesis', 'exec', 'peers', 'model', 'posture']
const STALE = ['darkContainers', 'bandIsIdentityHeader']
const REST_PER_SIDE = 10 // PriceBars.tsx
const ARMS = (process.env.R35_ARMS || '1,2,3,4').split(',').map(s => Number(s.trim())).filter(Boolean)
const secs = ms => `${(ms / 1000).toFixed(1)}s`

function sh(cmd, args, opts = {}) {
  const t = Date.now()
  const r = spawnSync(cmd, args, { encoding: 'utf8', maxBuffer: 256 * 1024 * 1024, ...opts })
  return { status: r.status, stdout: r.stdout || '', stderr: r.stderr || '', error: r.error, ms: Date.now() - t }
}
const git = (dir, args) => sh('git', ['-C', dir, ...args])
const hasIndex = d => fs.existsSync(path.join(d, 'index.html'))

function viteBuild(srcDir, outDir) {
  const vite = path.join(srcDir, 'node_modules', 'vite', 'bin', 'vite.js')
  if (!fs.existsSync(vite)) throw new Error(`no vite at ${vite} (node_modules not linked in ${srcDir})`)
  console.log(`BUILD: vite build ${srcDir} -> ${outDir}`)
  const r = sh(process.execPath, [vite, 'build', '--configLoader', 'runner', '--outDir', outDir, '--emptyOutDir', '--logLevel', 'warn'], { cwd: srcDir, timeout: 600000 })
  if (r.status !== 0 || !hasIndex(outDir)) throw new Error(`vite build failed rc=${r.status}: ${(r.stderr || r.stdout).slice(-600)}`)
  console.log(`BUILD: OK in ${secs(r.ms)}`)
}

function candidateDist() {
  if (process.env.DIST) {
    const d = path.resolve(process.env.DIST)
    if (!hasIndex(d)) throw new Error(`DIST=${d} has no index.html`)
    return { dist: d, how: 'DIST env' }
  }
  const head = git(UNDER_TEST, ['rev-parse', '--short=8', 'HEAD'])
  if (head.status !== 0) throw new Error(`cwd/portal is not a git checkout (${UNDER_TEST}): ${head.stderr.trim()}`)
  const sha = head.stdout.trim()
  const spec = ['--', '.', ':(exclude)scripts', ':(exclude)src/pages/SecurityAnalysis/__harness__']
  const st = git(UNDER_TEST, ['status', '--porcelain', ...spec]).stdout
  let key = sha
  if (st.trim()) key += '-dirty-' + crypto.createHash('sha1').update(st + git(UNDER_TEST, ['diff', 'HEAD', ...spec]).stdout).digest('hex').slice(0, 8)
  const d = path.join(SCRATCH, `dist-${key}`)
  if (hasIndex(d)) return { dist: d, how: `cached build of portal ${key}` }
  viteBuild(UNDER_TEST, d)
  return { dist: d, how: `fresh build of portal ${key}` }
}

function preDist() {
  if (hasIndex(DIST_PRE)) return { dist: DIST_PRE, how: 'existing build' }
  const src = path.join(SCRATCH, `src-${PRE_SHA}`)
  if (!fs.existsSync(path.join(src, 'package.json'))) {
    fs.mkdirSync(src, { recursive: true })
    const tarFile = path.join(SCRATCH, `src-${PRE_SHA}.tar`)
    const a = git(UNDER_TEST, ['archive', '-o', tarFile, PRE_SHA])
    if (a.status !== 0) throw new Error(`git archive ${PRE_SHA} failed: ${a.stderr.trim()}`)
    const sysTar = path.join(process.env.SystemRoot || 'C:/Windows', 'System32', 'tar.exe')
    sh(fs.existsSync(sysTar) ? sysTar : 'tar', ['-xf', tarFile, '-C', src]) // symlink members may refuse; package.json decides
    if (!fs.existsSync(path.join(src, 'package.json'))) throw new Error(`extract of ${PRE_SHA} into ${src} failed`)
  }
  const nm = path.join(src, 'node_modules')
  if (!fs.existsSync(nm)) {
    const target = fs.realpathSync(path.join(UNDER_TEST, 'node_modules'))
    try { fs.symlinkSync(target, nm, 'junction') } catch (e) { throw new Error(`cannot link node_modules into ${src}: ${e.message}`) }
  }
  viteBuild(src, DIST_PRE)
  return { dist: DIST_PRE, how: `fresh build of git archive ${PRE_SHA}` }
}

// One instrument run. The grades are read from <out>/grades.json; the instrument's own exit is printed, never graded.
function runInstrument(label, dist, states, extra, timeoutMs) {
  const out = path.join(OUT, label)
  fs.mkdirSync(out, { recursive: true })
  const args = [CHECK, '--dist', dist, '--out', out, '--fixtures', FIXTURES, ...(states ? ['--states', states.join(',')] : []), ...extra]
  const r = sh(process.execPath, args, { cwd: INSTR_ROOT, timeout: timeoutMs })
  fs.writeFileSync(path.join(OUT, `${label}.log`), r.stdout + '\n--- stderr ---\n' + r.stderr)
  const gp = path.join(out, 'grades.json')
  let grades = null
  try { grades = JSON.parse(fs.readFileSync(gp, 'utf8')) } catch { grades = null }
  const result = (r.stdout.split('\n').find(l => l.startsWith('RESULT:')) || '').trim()
  console.log(`RUN[${label}]: ${secs(r.ms)} instrument rc=${r.status}${r.error ? ' (' + (r.error.code || r.error.message) + ')' : ''} ${result || '(no RESULT line)'} grades.json ${grades ? 'read' : 'ABSENT'} -> ${out}`)
  return { out, grades, ms: r.ms }
}

const measurement = (out, state) => { try { return JSON.parse(fs.readFileSync(path.join(out, `${state}.json`), 'utf8')) } catch { return null } }
const REANCHOR = /lightOnDark|bandContainersTopLevel/
const reanchored = cells => Object.entries(cells || {}).filter(([n, c]) => REANCHOR.test(n) || REANCHOR.test(JSON.stringify(c && c.value !== undefined ? c.value : '')))
const short = v => { const s = JSON.stringify(v); return s && s.length > 220 ? s.slice(0, 220) + '...' : s }
const mline = m => (m ? `measured bandContainersTopLevel=${m.bandContainersTopLevel} lightOnDark=${m.lightOnDark}` : 'measurement ABSENT')

// The fixture the page reads for a route at rest (?days=30): the instrument router serves the LONGEST fixture key the
// request URL contains; a key with its own query must name days=30 to be the at-rest read.
function servedFixture(fx, base) {
  const keys = Object.keys(fx).filter(k => k.split('?')[0] === base && (!k.includes('?') || /[?&]days=30(&|$)/.test(k)))
  keys.sort((a, b) => b.length - a.length)
  return keys.length ? { key: keys[0], body: fx[keys[0]] } : null
}

const verdicts = {}
const say = (n, pass, line) => { verdicts[n] = pass; console.log(`ARM ${n}: ${pass ? 'PASS' : 'FAIL'} -- ${line}`) }

console.log(`instrument35: cwd ${ROOT}`)
console.log(`instrument35: INSTRUMENT_DIR ${INSTRUMENT_DIR} (instrument root ${INSTR_ROOT})`)
console.log(`instrument35: fixtures ${FIXTURES}`)
console.log(`instrument35: out ${OUT}`)
if (!fs.existsSync(CHECK)) { console.log(`ERROR: no ui-contract-check.mjs at ${CHECK}`); process.exit(2) }
if (!fs.existsSync(FIXTURES)) { console.log(`ERROR: no fixtures at ${FIXTURES}`); process.exit(2) }
fs.mkdirSync(OUT, { recursive: true })

let cand
try { cand = candidateDist() } catch (e) { console.log(`ERROR: candidate dist: ${e.message}`); process.exit(2) }
console.log(`instrument35: candidate dist ${cand.dist} (${cand.how})`)

// ---- ARM 2: the real pre-redesign page fails the band clause --------------------------------------------------------
if (ARMS.includes(2)) {
  let pre = null
  try { pre = preDist() } catch (e) { say(2, false, `no ${PRE_SHA} build: ${e.message}`) }
  if (pre) {
    console.log(`instrument35: ${PRE_SHA} dist ${pre.dist} (${pre.how})`)
    const r = runInstrument(`pre-${PRE_SHA}`, pre.dist, SIX, [], 360000)
    const fails = []
    for (const s of SIX) {
      const cells = r.grades && r.grades.states && r.grades.states[s]
      for (const [n, c] of reanchored(cells)) if (c.grade === 'FAIL') fails.push(`${s}.${n} FAIL ${short(c.value)} (${mline(measurement(r.out, s))})`)
    }
    for (const f of fails) console.log(`  ${PRE_SHA}: ${f}`)
    const staleFails = SIX.flatMap(s => STALE.filter(n => r.grades && r.grades.states && r.grades.states[s] && r.grades.states[s][n] && r.grades.states[s][n].grade === 'FAIL').map(n => `${s}.${n}`))
    if (staleFails.length) console.log(`  ${PRE_SHA}: stale-anchor FAILs (not counted): ${staleFails.join(', ')}`)
    say(2, fails.length > 0, !r.grades ? 'no grades.json from the 8fa7abde run'
      : fails.length ? `${fails.length} re-anchored band-clause FAIL(s) on portal ${PRE_SHA}; first: ${fails[0]}`
        : `portal ${PRE_SHA} grades NO re-anchored band clause FAIL (re-anchored clauses seen: ${SIX.map(s => reanchored(r.grades.states[s]).map(([n, c]) => `${s}.${n}=${c.grade}`).join(' ')).join(' ') || 'none'})`)
  }
}

// ---- ARM 3: planted pages, one per clause limb, beside a clean control ---------------------------------------------
if (ARMS.includes(3)) {
  const BAND = inner => `<div class="dark-band" data-r35-band="" style="background:rgb(25,38,67);width:640px;min-height:48px;margin:8px 0;padding:8px">${inner}</div>`
  const PLANTS = {
    'two-bands': BAND('') + BAND(''),
    'light-on-dark': BAND('<div style="background:#ffffff;color:rgb(10,23,51);padding:6px;width:240px">R35 planted white card</div><span style="color:#ffffff">R35 planted light ink</span>'),
    'control': BAND(''),
  }
  const res = {}
  for (const [kind, html] of Object.entries(PLANTS)) {
    const d = path.join(SCRATCH, `dist-plant-${kind}`)
    fs.rmSync(d, { recursive: true, force: true })
    fs.cpSync(cand.dist, d, { recursive: true })
    const js = `(function(){var H=${JSON.stringify(html)};function put(){var m=document.querySelector('main');if(!m||m.querySelector('[data-r35-plant]'))return;var w=document.createElement('div');w.setAttribute('data-r35-plant',${JSON.stringify(kind)});w.innerHTML=H;m.appendChild(w)}setInterval(put,100)})();\n`
    fs.writeFileSync(path.join(d, 'r35-plant.js'), js)
    const ip = path.join(d, 'index.html')
    const idx = fs.readFileSync(ip, 'utf8')
    if (!idx.includes('</body>')) { res[kind] = { ok: false, line: 'index.html has no </body>' }; continue }
    fs.writeFileSync(ip, idx.replace('</body>', '<script src="/r35-plant.js"></script></body>'))
    const r = runInstrument(`plant-${kind}`, d, ['thesis'], [], 360000)
    const cells = r.grades && r.grades.states && r.grades.states.thesis
    const re = reanchored(cells)
    const m = measurement(r.out, 'thesis')
    const failed = re.filter(([, c]) => c.grade === 'FAIL')
    const desc = `${re.map(([n, c]) => `${n}=${c.grade}${c.grade === 'PASS' ? '' : ' ' + short(c.value)}`).join('; ') || 'no re-anchored clause'}; ${mline(m)}`
    let ok
    if (!cells || !m) ok = false
    else if (kind === 'two-bands') ok = failed.length > 0 && m.bandContainersTopLevel >= 2
    else if (kind === 'light-on-dark') ok = failed.length > 0 && m.lightOnDark > 0 && m.bandContainersTopLevel <= 1
    else ok = re.length > 0 && failed.length === 0 && re.every(([, c]) => c.grade === 'PASS') && m.bandContainersTopLevel >= 1 && m.lightOnDark === 0
    res[kind] = { ok, line: desc }
    console.log(`  plant ${kind}: ${ok ? 'AS EXPECTED' : 'NOT AS EXPECTED'} -- ${desc}`)
  }
  const all = ['two-bands', 'light-on-dark', 'control'].every(k => res[k] && res[k].ok)
  say(3, all, `two bands -> FAIL ${res['two-bands'] && res['two-bands'].ok ? 'yes' : 'NO'}; light card + light ink on a band -> FAIL ${res['light-on-dark'] && res['light-on-dark'].ok ? 'yes' : 'NO'}; clean control (one empty band) -> PASS ${res.control && res.control.ok ? 'yes' : 'NO'}`)
}

// ---- ARM 1 (and 4 off the same grades): the candidate, full six-state run with --states-sweep -----------------------
let candRun = null
if (ARMS.includes(1) || ARMS.includes(4)) candRun = runInstrument('candidate', cand.dist, null, ['--states-sweep'], 1500000)

if (ARMS.includes(1)) {
  const g = candRun.grades
  const why = []
  if (!g) why.push('no grades.json from the candidate run')
  else {
    for (const s of SIX) {
      const cells = g.states && g.states[s]
      const re = reanchored(cells)
      const m = measurement(candRun.out, s)
      const ldGraded = re.some(([n, c]) => /lightOnDark/.test(n + JSON.stringify(c.value)))
      const okM = !!m && typeof m.bandContainersTopLevel === 'number' && m.bandContainersTopLevel <= 1 && m.lightOnDark === 0
      const okC = re.length > 0 && re.every(([, c]) => c.grade === 'PASS') && ldGraded
      console.log(`  candidate ${s}: ${re.map(([n, c]) => `${n}=${c.grade}${c.grade === 'PASS' ? '' : ' ' + short(c.value)}`).join('; ') || 'NO re-anchored band clause'}; lightOnDark graded ${ldGraded ? 'yes' : 'NO'}; ${mline(m)}`)
      if (!cells) why.push(`${s} not graded`)
      else if (!okC) why.push(`${s} band clause not PASS (or lightOnDark not graded)`)
      if (cells && !okM) why.push(`${s} measurement not bandContainersTopLevel<=1 and lightOnDark==0`)
    }
    let fx = null
    try { fx = JSON.parse(fs.readFileSync(FIXTURES, 'utf8')) } catch (e) { why.push(`fixtures unreadable: ${e.message}`) }
    const faces = (g.run && g.run.faces) || {}
    if (fx) {
      const price = servedFixture(fx, '/api/scoped/amgt/lead-panel/rankings/trending/price')
      const pv = price && price.body && Array.isArray(price.body.rows) ? price.body.rows.map(r => r && r.return_30d_pct).filter(v => typeof v === 'number' && Number.isFinite(v)) : null
      const rest = pv ? Math.min(REST_PER_SIDE, pv.filter(v => v > 0).length) + Math.min(REST_PER_SIDE, pv.filter(v => v < 0).length) : null
      const fp = faces.price || {}
      const fpv = fp.value || {}
      console.log(`  faces.price: ${fp.grade} visible ${fpv.visible} expected(instrument) ${fpv.served}; page rule from fixture ${price ? price.key : 'NONE'}: ${pv ? `${pv.filter(v => v > 0).length} gainers, ${pv.filter(v => v < 0).length} losers -> rest ${rest}` : 'no served rows'}`)
      if (fp.grade !== 'PASS') why.push(`faces.price ${fp.grade}${fpv.failing ? ' ' + short(fpv.failing) : ''}`)
      else if (rest === null || fpv.visible !== rest) why.push(`faces.price visible ${fpv.visible} != the page's rest count ${rest}`)

      const chat = servedFixture(fx, '/api/scoped/amgt/lead-panel/timeseries/collected/chatter')
      const cb = chat && chat.body
      const windowed = !!cb && typeof cb.window_days === 'number' && Array.isArray(cb.rows) && cb.rows.some(r => r && typeof r.articles_total === 'number')
      const k = windowed ? cb.rows.filter(r => r && typeof r.articles_total === 'number' && Number.isFinite(r.articles_total) && r.articles_total > 0).length : null
      let cap = null
      try { cap = JSON.parse(fs.readFileSync(WINDOW_CAPTURE, 'utf8')).payload } catch { cap = null }
      const capLine = cap && cb ? `round31 capture window_days ${cap.window_days} as_of ${cap.as_of} rows ${cap.rows.length}; fixture window_days ${cb.window_days} as_of ${cb.as_of} rows ${Array.isArray(cb.rows) ? cb.rows.length : 'none'}` : 'round31 capture not read'
      const fc = faces.chatter || {}
      const fcv = fc.value || {}
      console.log(`  faces.chatter: ${fc.grade} visible ${fcv.visible} expected(instrument) ${fcv.served}; fixture ${chat ? chat.key : 'NONE'} ${windowed ? `WINDOWED, ${k} rows with articles_total > 0` : 'NOT the windowed shape (no window_days/articles_total)'}; ${capLine}`)
      if (!windowed) why.push('the chatter fixture is not the windowed served shape')
      if (fc.grade !== 'PASS') why.push(`faces.chatter ${fc.grade}${fcv.failing ? ' ' + short(fcv.failing) : ''}`)
      else if (windowed && fcv.visible !== k) why.push(`faces.chatter visible ${fcv.visible} != rows with articles_total > 0 (${k})`)
    }
    console.log(`  candidate result tally: ${JSON.stringify(g.result)}`)
  }
  say(1, why.length === 0, why.length ? why.join('; ') : `band clause PASS on ${SIX.length} of 6 states with bandContainersTopLevel <= 1 and lightOnDark == 0 measured; faces price + chatter PASS at the page's rule; tally ${JSON.stringify(g.result)}`)
}

if (ARMS.includes(4)) {
  const g = candRun && candRun.grades
  if (!g || !g.states) say(4, false, 'no candidate grades.json to read')
  else {
    const present = [], failing = []
    for (const s of Object.keys(g.states)) for (const n of STALE) {
      const c = g.states[s][n]
      if (!c) continue
      present.push(`${s}.${n}=${c.grade}`)
      if (c.grade === 'FAIL') failing.push(`${s}.${n} ${short(c.value)}`)
    }
    const graded = SIX.every(s => g.states[s])
    say(4, graded && failing.length === 0, !graded ? `the candidate run graded ${Object.keys(g.states).length} of 6 states`
      : failing.length ? `${failing.length} stale-anchor FAIL(s): ${failing.slice(0, 3).join(' | ')}`
        : `0 stale-anchor FAILs (${present.length ? 'present: ' + present.join(' ') : 'darkContainers / bandIsIdentityHeader no longer graded'})`)
  }
}

for (const n of [1, 2, 3, 4]) if (!(n in verdicts)) say(n, false, 'NOT RUN (R35_ARMS)')
const N = [1, 2, 3, 4].filter(n => verdicts[n]).length
console.log(`RUNTIME: ${secs(Date.now() - T0)} total`)
console.log(`THE INSTRUMENT GRADES THE REDESIGN AND CAN FAIL: ${N} of 4 arms`)
process.exit(N === 4 ? 0 : 1)
