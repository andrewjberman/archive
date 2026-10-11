/**
 * AMGT_CORPUS round 46, CRPS-av-10 -- the rendered census over every served name (FWD-12 and FWD-20). Issuer's file. READ-ONLY.
 *
 * RUN:  node av10_rendered_census.cjs <portal root> <capture.json>
 *   <portal root> holds src/pages/SecurityAnalysis/{modelSheet.ts,figureIdentity.ts} AT THE BUILD UNDER READ (the DEV head after the
 *   av-2 landing, f00c7b8ee8 or later); the capture is av_capture.py's output over the LIVE function (`model.team_sheet` served).
 *
 * METHOD (round 45's au3_rendered_rows.cjs, moved to the row classes). The REAL modelSheet.ts and figureIdentity.ts are transpiled and
 * run in a vm; per name `buildModelSheet` is called with the arguments ModelTab.tsx passes, the seventh being the served
 * `model.team_sheet`; the check face is read through the real `checkFor`. The sheet builder the page calls on served data, not a
 * browser DOM walk.
 *
 * Prints, per name: class, workbook file, the sheet's rows and FIGURE / HEADING / CONTROL (they must sum to the rows), the rendered rows,
 * and the FIGURE rows by source. Then the totals:
 *   av10 classes  FIGURE <f> HEADING <h> CONTROL <c> sum <s> of rows <r>          (s must equal r)
 *   av10 FIGURE by source  bloomberg <b> team <t> why <w> refused <x> unmapped <u> of <f>      (b+t+w+x+u == f; u must be 0)
 *   av10 rendered rows <n>: heading rows <h>, control rows rendered <k> (must be 0), why-rows with a barred word <q> (must be 0)
 *   av10 first group equals the sheet's non-CONTROL rows on <e> of <m> names with team rows
 *   av10 names with a team sheet <m> of <N> served; master_absent <a>
 * `refused` is a FIGURE row whose Bloomberg figure the check face REFUSES (it is Bloomberg's, shown as a refusal sentence).
 */
const fs = require('fs')
const path = require('path')
const vm = require('vm')
const { execSync } = require('child_process')
const { createRequire } = require('module')

const portalRoot = path.resolve(process.argv[2])
const cap = JSON.parse(fs.readFileSync(path.resolve(process.argv[3]), 'utf8'))
const top = execSync('git rev-parse --show-toplevel', { encoding: 'utf8' }).trim()

function installed(name) {
  for (const root of [portalRoot, path.join(top, 'portal')]) {
    try { return createRequire(path.join(root, 'package.json'))(name) } catch (e) { /* next */ }
  }
  throw new Error(name + ' not resolvable')
}
const ts = installed('typescript')
const stub = new Proxy({}, { get: (_t, k) => (k === '__esModule' ? true : () => '') })
function load(rel) {
  const file = path.join(portalRoot, 'src', 'pages', 'SecurityAnalysis', rel)
  const out = ts.transpileModule(fs.readFileSync(file, 'utf8'), {
    compilerOptions: { module: ts.ModuleKind.CommonJS, target: ts.ScriptTarget.ES2020 },
  }).outputText
  const mod = { exports: {} }
  vm.runInNewContext(out, { module: mod, exports: mod.exports, require: () => stub, console })
  return mod.exports
}
const sheetMod = load('modelSheet.ts')
const identity = load('figureIdentity.ts')
const BAR = /(^|\b)(ABSENT|REFUSED --|not read)\b/i

function build(d) {
  const model = d.model || {}
  const fc = Array.isArray(model.forecast_figures) ? model.forecast_figures : undefined
  const ln = model.line_names === '<KEY ABSENT>' ? undefined : model.line_names
  const unresolved = Array.isArray(model.fiscal_unresolved) ? model.fiscal_unresolved : undefined
  const team = model.team_sheet && typeof model.team_sheet === 'object' ? model.team_sheet : undefined
  return sheetMod.buildModelSheet(d.fiscal_year_figures || [], d.fiscal_years, ln, fc, unresolved, d.header_figures, team)
}
function refused(row, checks) {
  return (row.cells || []).some((fig) => fig && (identity.checkFor(checks || [], fig) || {}).verdict === 'REFUSE')
}

const names = Object.keys(cap.keys).sort()
const cls = { FIGURE: 0, HEADING: 0, CONTROL: 0 }
let rowsTotal = 0
const src = { bloomberg: 0, team: 0, why: 0, refused: 0, unmapped: 0 }
let headingRows = 0
let controlRendered = 0
let barredWhy = 0
let firstEq = 0
let withTeam = 0
let masterAbsent = 0
let sumBroken = 0
console.log('capture function CodeSha256 ' + cap.function.CodeSha256 + ' LastModified ' + cap.function.LastModified + '; modelSheet.ts at ' + portalRoot)
for (const key of names) {
  const d = cap.keys[key]
  const t = (d.model || {}).team_sheet
  const klass = t && typeof t === 'object' ? t.class : 'KEY-ABSENT'
  if (klass === 'master_absent') masterAbsent += 1
  const rows = t && Array.isArray(t.rows) ? t.rows : []
  const classes = t && Array.isArray(t.row_classes) ? t.row_classes : []
  const sheet = build(d)
  const first = ((sheet.groups || [])[0] || {}).rows || []
  if (rows.length > 0 && classes.length === rows.length) {
    withTeam += 1
    const c = { FIGURE: 0, HEADING: 0, CONTROL: 0 }
    classes.forEach((x) => { c[x] = (c[x] || 0) + 1 })
    cls.FIGURE += c.FIGURE; cls.HEADING += c.HEADING; cls.CONTROL += c.CONTROL
    rowsTotal += rows.length
    if (c.FIGURE + c.HEADING + c.CONTROL !== rows.length) sumBroken += 1
    const want = rows.filter((_l, i) => classes[i] !== 'CONTROL')
    if (JSON.stringify(first.map((r) => r.label)) === JSON.stringify(want)) firstEq += 1
    let fb = 0; let ft = 0; let fw = 0; let fr = 0; let fu = 0
    for (const r of first) {
      if (r.rowKind === 'heading') { headingRows += 1; continue }
      if (r.source === 'bloomberg') { if (refused(r, d.check_face)) fr += 1; else fb += 1 }
      else if (r.source === 'team') ft += 1
      else if (r.source === 'why') { fw += 1; if (!r.absentReason || BAR.test(String(r.absentReason))) barredWhy += 1 }
      else fu += 1
    }
    controlRendered += first.filter((r) => classes[rows.indexOf(r.label)] === 'CONTROL' && r.rowKind !== 'heading' && !r.source).length
    src.bloomberg += fb; src.team += ft; src.why += fw; src.refused += fr; src.unmapped += fu
    console.log('av10 ' + key + ' class ' + klass + ' workbook ' + (t.workbook_key ? path.basename(String(t.workbook_key)) : 'None') + ' rows ' + rows.length +
      ' FIGURE ' + c.FIGURE + ' HEADING ' + c.HEADING + ' CONTROL ' + c.CONTROL + ' rendered ' + first.length + ' | bloomberg ' + fb + ' team ' + ft + ' why ' + fw + ' refused ' + fr + ' unmapped ' + fu)
  } else {
    console.log('av10 ' + key + ' class ' + klass + ' rows ' + rows.length + ' (no row classes served: the page builds the base rows)')
  }
}
const f = cls.FIGURE
console.log('av10 classes FIGURE ' + cls.FIGURE + ' HEADING ' + cls.HEADING + ' CONTROL ' + cls.CONTROL + ' sum ' + (cls.FIGURE + cls.HEADING + cls.CONTROL) + ' of rows ' + rowsTotal + (sumBroken ? ' SUM-BROKEN on ' + sumBroken + ' name(s)' : ''))
console.log('av10 FIGURE by source bloomberg ' + src.bloomberg + ' team ' + src.team + ' why ' + src.why + ' refused ' + src.refused + ' unmapped ' + src.unmapped + ' of ' + f +
  ' (sum ' + (src.bloomberg + src.team + src.why + src.refused + src.unmapped) + ')')
console.log('av10 rendered heading rows ' + headingRows + ', control rows rendered ' + controlRendered + ', why-rows with a barred word ' + barredWhy)
console.log('av10 first group equals the sheet\'s non-CONTROL rows on ' + firstEq + ' of ' + withTeam + ' names with team rows')
console.log('av10 names with row classes served ' + withTeam + ' of ' + names.length + ' served; master_absent ' + masterAbsent)
