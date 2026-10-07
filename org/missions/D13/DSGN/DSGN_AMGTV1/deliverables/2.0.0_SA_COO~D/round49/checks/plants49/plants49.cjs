#!/usr/bin/env node
/**
 * plants49.cjs -- DSGN_AMGTV1 round 49 issuer CHECK (2.0.0_SA_COO~D): EVERY CLAUSE OF THE RENDER CHECK FAILS ITS OWN PLANTED PAGE,
 * BESIDE A CLEAN CONTROL.
 *
 * Why: PRD v0.17 FWD-20 DONE WHEN: "the same instrument FAILS a planted page on each clause (one violation per clause, each beside a
 * clean control)". round35/checks/instrument/instrument35.cjs plants the band clause's two limbs only (two dark bands; light on dark).
 * CTO ruling msg 30858/30859 (2026-10-07): "each clause" means every clause, so FWD-20 is NOT_REALIZED until each has its pair. This
 * file plants the other eight clauses: tabPanelsWhite, fonts, weights, sizes, radii, shadows, lowContrastChars, purpleFills.
 * (The CTO allows a clause that failed on the real page and then passed after its fix to count -- the size clause; it is planted here
 * anyway, so no clause rests on history.)
 *
 * Usage (from the directory whose portal/ is the checkout under test; the portal's own scripts/ui-contract-check.mjs is the instrument):
 *   cd "$(git rev-parse --show-toplevel)" && node "org/missions/D13/DSGN/DSGN_AMGTV1/deliverables/2.0.0_SA_COO~D/round49/checks/plants49/plants49.cjs"
 *   DIST=<built dist>   reuse a build of the product bytes (the dist key excludes scripts/, as in instrument35.cjs)
 *   R35_SCRATCH=<dir>   scratch root (default C:/tmp/r35-scratch-c, instrument35's own)
 *
 * How: for each clause, a copy of the candidate dist with ONE injected script that adds one violating element to the Thesis state,
 * then one instrument run over state `thesis`. Read from <out>/grades.json states.thesis:
 *   - the planted clause's cell is FAIL;
 *   - the plant was seen ([data-r49-plant] present is implied by the FAIL; a PASS means the plant did not land or the clause is blind).
 * The CONTROL is the same copy with an injected element that violates nothing (Lato 14 px, weight 400, black on white, no radius, no
 * shadow): all eight clause cells read PASS on it. A clause whose control cell is not PASS proves nothing, so that pair is refused.
 * Prints one line per clause, then "EVERY CLAUSE FAILS ITS PLANTED PAGE BESIDE A CLEAN CONTROL: <k> of 8 clauses"; exit 0 only at 8 of 8
 * with the control clean. No network; writes only under the scratch root.
 */
'use strict'
const { spawnSync } = require('node:child_process')
const fs = require('node:fs')
const path = require('node:path')

const T0 = Date.now()
const ROOT = process.cwd()
const SCRATCH = path.resolve(process.env.R35_SCRATCH || 'C:/tmp/r35-scratch-c')
const UNDER_TEST = path.join(ROOT, 'portal')
const CHECK = path.join(UNDER_TEST, 'scripts', 'ui-contract-check.mjs')
const FIXTURES = path.join(UNDER_TEST, 'src', 'pages', 'SecurityAnalysis', '__harness__', 'tests', 'uiContractFixtures.json')
const STAMP = new Date().toISOString().replace(/[-:]/g, '').replace(/\.\d+Z$/, 'Z')
const OUT = path.join(SCRATCH, `plants49-${STAMP}`)
const secs = ms => `${(ms / 1000).toFixed(1)}s`
const hasIndex = d => fs.existsSync(path.join(d, 'index.html'))
const sh = (cmd, args, opts = {}) => { const t = Date.now(); const r = spawnSync(cmd, args, { encoding: 'utf8', maxBuffer: 256 * 1024 * 1024, ...opts }); return { status: r.status, stdout: r.stdout || '', stderr: r.stderr || '', error: r.error, ms: Date.now() - t } }

function candidateDist() {
  if (process.env.DIST) { const d = path.resolve(process.env.DIST); if (!hasIndex(d)) throw new Error(`DIST=${d} has no index.html`); return { dist: d, how: 'DIST env' } }
  const head = sh('git', ['-C', UNDER_TEST, 'rev-parse', '--short=8', 'HEAD'])
  if (head.status !== 0) throw new Error(`cwd/portal is not a git checkout (${UNDER_TEST})`)
  const d = path.join(SCRATCH, `dist-${head.stdout.trim()}`)
  if (hasIndex(d)) return { dist: d, how: `cached build of portal ${head.stdout.trim()}` }
  const vite = path.join(UNDER_TEST, 'node_modules', 'vite', 'bin', 'vite.js')
  if (!fs.existsSync(vite)) throw new Error(`no vite at ${vite}`)
  const r = sh(process.execPath, [vite, 'build', '--configLoader', 'runner', '--outDir', d, '--emptyOutDir', '--logLevel', 'warn'], { cwd: UNDER_TEST, timeout: 600000 })
  if (r.status !== 0 || !hasIndex(d)) throw new Error(`vite build failed rc=${r.status}: ${(r.stderr || r.stdout).slice(-400)}`)
  return { dist: d, how: `fresh build of portal ${head.stdout.trim()}` }
}

// One violation per clause. `into` is the selector the element is appended to (default: main).
const BASE = 'font-family:Lato,sans-serif;font-size:14px;font-weight:400;color:rgb(0,0,0);background:rgb(255,255,255);'
const PLANTS = {
  fonts: { html: `<p style="${BASE}font-family:Georgia,serif">R49 planted serif sentence, not the page font</p>` },
  weights: { html: `<p style="${BASE}font-weight:600">R49 planted semibold sentence at weight 600</p>` },
  sizes: { html: `<p style="${BASE}font-size:9px">R49 planted nine pixel sentence under the floor</p>` },
  radii: { html: `<div style="${BASE}border:1px solid rgb(200,200,200);border-radius:12px;width:200px;height:30px">R49 planted rounded box</div>` },
  shadows: { html: `<div style="${BASE}box-shadow:0 2px 8px rgba(0,0,0,0.4);width:200px;height:30px">R49 planted shadow box</div>` },
  lowContrastChars: { html: `<p style="${BASE}color:rgb(205,205,205)">R49 planted pale grey sentence on white</p>` },
  purpleFills: { html: `<button type="button" style="${BASE}background:hsl(var(--semantic-action-primary));color:rgb(255,255,255);padding:4px 10px">R49 planted purple action</button>` },
  tabPanelsWhite: { into: '[data-tab-panel]', html: `<div class="border" style="${BASE}background:rgb(230,236,200);border:1px solid rgb(200,200,200);width:420px;height:60px">R49 planted tinted panel surface</div>` },
}
const CONTROL = `<p style="${BASE}">R49 control sentence in the page font at fourteen pixels</p>`
const ALL_CLAUSES = Object.keys(PLANTS)
// PLANTS49_ONLY=a,b limits the run to those clauses (the printed denominator shrinks with it; a full verdict needs no filter).
// The name `designedStates` selects the ninth pair below.
const ONLY = (process.env.PLANTS49_ONLY || '').split(',').map(s => s.trim()).filter(Boolean)
const CLAUSES = ONLY.length ? ALL_CLAUSES.filter(c => ONLY.includes(c)) : ALL_CLAUSES
const WITH_STATES = ONLY.length ? ONLY.includes('designedStates') : true

// The ninth pair: FWD-20's "the three states of FWD-19 present" (grades.json run.fwd19_designedStates). The plant is a page whose
// error state is NOT the designed one: a script strips the marker `data-panel-state="error"` the moment it appears, so the sweep
// captures no designed error state on any panel. The control is the same full run on an untouched copy. Both are FULL six-state
// runs with --states-sweep (about nine minutes each): a one-state run reads NOT_EXERCISED on the control, which proves nothing.
const STRIP_ERROR_JS = `(function(){function strip(n){if(n&&n.nodeType===1){if(n.getAttribute('data-panel-state')==='error'){n.setAttribute('data-r49-stripped','error');n.removeAttribute('data-panel-state')}var k=n.querySelectorAll?n.querySelectorAll('[data-panel-state="error"]'):[];for(var i=0;i<k.length;i++){k[i].setAttribute('data-r49-stripped','error');k[i].removeAttribute('data-panel-state')}}}new MutationObserver(function(ms){for(var i=0;i<ms.length;i++){var m=ms[i];if(m.type==='attributes')strip(m.target);for(var j=0;j<m.addedNodes.length;j++)strip(m.addedNodes[j])}}).observe(document.documentElement,{subtree:true,childList:true,attributes:true,attributeFilter:['data-panel-state']});strip(document.documentElement)})();\n`
function scriptedDist(cand, label, js) {
  const d = path.join(SCRATCH, `dist-plant49-${label}`)
  fs.rmSync(d, { recursive: true, force: true })
  fs.cpSync(cand, d, { recursive: true })
  const ip = path.join(d, 'index.html')
  const idx = fs.readFileSync(ip, 'utf8')
  if (js) {
    if (!idx.includes('<head>')) throw new Error('index.html has no <head>')
    fs.writeFileSync(path.join(d, 'r49-strip.js'), js)
    fs.writeFileSync(ip, idx.replace('<head>', '<head><script src="/r49-strip.js"></script>'))
  }
  return d
}
function runFull(label, dist) {
  const out = path.join(OUT, label)
  fs.mkdirSync(out, { recursive: true })
  const r = sh(process.execPath, [CHECK, '--dist', dist, '--out', out, '--fixtures', FIXTURES, '--states-sweep'], { cwd: UNDER_TEST, timeout: 1500000 })
  fs.writeFileSync(path.join(OUT, `${label}.log`), r.stdout + '\n--- stderr ---\n' + r.stderr)
  let g = null
  try { g = JSON.parse(fs.readFileSync(path.join(out, 'grades.json'), 'utf8')) } catch { g = null }
  const cell = g && g.run ? g.run.fwd19_designedStates : null
  console.log(`RUN[${label}]: ${secs(r.ms)} instrument rc=${r.status} grades.json ${g ? 'read' : 'ABSENT'} -> ${out}`)
  return cell
}

function plantedDist(cand, label, html, into) {
  const d = path.join(SCRATCH, `dist-plant49-${label}`)
  fs.rmSync(d, { recursive: true, force: true })
  fs.cpSync(cand, d, { recursive: true })
  const js = `(function(){var H=${JSON.stringify(html)};var S=${JSON.stringify(into || 'main')};function put(){var m=document.querySelector(S);if(!m||m.querySelector('[data-r49-plant]'))return;var w=document.createElement('div');w.setAttribute('data-r49-plant',${JSON.stringify(label)});w.innerHTML=H;m.appendChild(w)}setInterval(put,100)})();\n`
  fs.writeFileSync(path.join(d, 'r49-plant.js'), js)
  const ip = path.join(d, 'index.html')
  const idx = fs.readFileSync(ip, 'utf8')
  if (!idx.includes('</body>')) throw new Error('index.html has no </body>')
  fs.writeFileSync(ip, idx.replace('</body>', '<script src="/r49-plant.js"></script></body>'))
  return d
}
function run(label, dist) {
  const out = path.join(OUT, label)
  fs.mkdirSync(out, { recursive: true })
  const r = sh(process.execPath, [CHECK, '--dist', dist, '--out', out, '--fixtures', FIXTURES, '--states', 'thesis'], { cwd: UNDER_TEST, timeout: 360000 })
  fs.writeFileSync(path.join(OUT, `${label}.log`), r.stdout + '\n--- stderr ---\n' + r.stderr)
  let g = null
  try { g = JSON.parse(fs.readFileSync(path.join(out, 'grades.json'), 'utf8')) } catch { g = null }
  const cells = g && g.states && g.states.thesis ? g.states.thesis : null
  console.log(`RUN[${label}]: ${secs(r.ms)} instrument rc=${r.status} grades.json ${cells ? 'read' : 'ABSENT'} -> ${out}`)
  return cells
}
const cellStr = c => (c ? `${c.grade} ${JSON.stringify(c.value).slice(0, 150)}` : 'cell ABSENT')

let pass = 0
let total = CLAUSES.length
let controlClean = false
try {
  if (!fs.existsSync(CHECK)) throw new Error(`no instrument at ${CHECK}`)
  fs.mkdirSync(OUT, { recursive: true })
  const cand = candidateDist()
  console.log(`plants49: candidate dist ${cand.dist} (${cand.how}); instrument ${CHECK}`)
  const control = run('control', plantedDist(cand.dist, 'control', CONTROL, 'main'))
  const controlBad = CLAUSES.filter(c => !control || !control[c] || control[c].grade !== 'PASS')
  controlClean = controlBad.length === 0
  console.log(`CONTROL ${controlClean ? 'CLEAN' : 'NOT CLEAN'}: ${controlClean ? '8 of 8 clause cells PASS on the control page' : controlBad.map(c => `${c}=${cellStr(control && control[c])}`).join(' | ')}`)
  for (const clause of CLAUSES) {
    const p = PLANTS[clause]
    const cells = run(`plant-${clause}`, plantedDist(cand.dist, clause, p.html, p.into))
    const cell = cells && cells[clause]
    const failed = !!cell && cell.grade === 'FAIL'
    const ctl = !!control && !!control[clause] && control[clause].grade === 'PASS'
    const others = cells ? CLAUSES.filter(c => c !== clause && cells[c] && cells[c].grade === 'FAIL') : []
    const ok = failed && ctl
    if (ok) pass += 1
    console.log(`CLAUSE ${ok ? 'PASS' : 'FAIL'} ${clause} :: planted page ${cellStr(cell)}; control ${ctl ? 'PASS' : 'not PASS'}${others.length ? `; also failed on this plant: ${others.join(',')}` : ''}`)
  }
  if (WITH_STATES) {
    total += 1
    const ctl = runFull('states-control', scriptedDist(cand.dist, 'states-control', null))
    const planted = runFull('states-plant', scriptedDist(cand.dist, 'states-plant', STRIP_ERROR_JS))
    const ctlOk = !!ctl && ctl.grade === 'PASS'
    const failed = !!planted && planted.grade === 'FAIL'
    const missing = planted && planted.value && Array.isArray(planted.value.missing) ? planted.value.missing : []
    const onlyError = missing.length > 0 && missing.every(m => /\/error\b/.test(m))
    const ok = ctlOk && failed && onlyError
    if (ok) pass += 1
    console.log(`CLAUSE ${ok ? 'PASS' : 'FAIL'} designedStates :: planted page ${planted ? planted.grade : 'cell ABSENT'}, missing ${JSON.stringify(missing).slice(0, 200)}; control ${ctl ? ctl.grade : 'cell ABSENT'}`)
  }
} catch (e) {
  console.log('PLANTS49 ERROR: ' + String(e && e.message).split('\n')[0])
}
console.log(`RUNTIME: ${secs(Date.now() - T0)} total; out ${OUT}`)
console.log(`EVERY CLAUSE FAILS ITS PLANTED PAGE BESIDE A CLEAN CONTROL: ${pass} of ${total} clauses${ONLY.length ? ` (FILTERED run: ${ONLY.join(',')}; the full set is 9)` : ''}`)
process.exit(pass === total && controlClean ? 0 : 1)
