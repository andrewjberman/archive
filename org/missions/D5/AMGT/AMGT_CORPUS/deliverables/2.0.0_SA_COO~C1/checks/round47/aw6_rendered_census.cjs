/**
 * AMGT_CORPUS round 47, CRPS-aw-6 -- the rendered census over every served name (FWD-12 and FWD-20): round 46's aw6_rendered_census.cjs
 * with the label census (no raw field code on the face), the team values' print by their own format, and the master arm. Issuer's file. READ-ONLY.
 *
 * RUN:  node aw6_rendered_census.cjs <portal root> <capture.json>
 *   <portal root> holds src/pages/SecurityAnalysis/{modelSheet.ts,figureIdentity.ts} AT THE BUILD UNDER READ (the DEV head with aw-2's
 *   three commits, 44ec7e70a9 or later); the capture is aw4_capture.py's output over the LIVE function, or aw6_preread_inject.py's PREDICTION with the stored /13
 *   field in place of `model.team_sheet`.
 *
 * METHOD (round 45's au3_rendered_rows.cjs, moved to the row classes). The REAL modelSheet.ts and figureIdentity.ts are transpiled and
 * run in a vm; per name `buildModelSheet` is called with the arguments ModelTab.tsx passes, the seventh being the served
 * `model.team_sheet`; the check face is read through the real `checkFor`. The sheet builder the page calls on served data, not a
 * browser DOM walk.
 *
 * Prints, per name: class, workbook file, the sheet's rows and FIGURE / HEADING / CONTROL (they must sum to the rows), the rendered rows,
 * and the FIGURE rows by source. Then the totals:
 *   aw6 classes  FIGURE <f> HEADING <h> CONTROL <c> sum <s> of rows <r>          (s must equal r)
 *   aw6 FIGURE by source  bloomberg <b> team <t> why <w> refused <x> unmapped <u> of <f>      (b+t+w+x+u == f; u must be 0)
 *   aw6 rendered rows <n>: heading rows <h>, control rows rendered <k> (must be 0), why-rows with a barred word <q> (must be 0)
 *   aw6 first group has as many rows as the sheet's non-CONTROL rows on <e> of <m> names with team rows
 *   aw6 names with a team sheet <m> of <N> served; master_absent <a>
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
const IDENT = /^[A-Z][A-Z0-9]*(_[A-Z0-9]+)+$/
const MASTER_WHY = "The research team keeps no workbook for this company; this row is from the team's template."
let rawLabels = 0
let rawHeadings = 0
const labelsBy = { held: 0, measured: 0, factset_line: 0, bloomberg_line: 0 }
let teamCells = 0
let teamBeyond4 = 0
let pctCells = 0
let pctPrinted = 0
let masterNames = 0
let masterRows = 0
let masterWhyExact = 0
let masterBloomberg = 0
let masterWithValue = 0
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
    // round 47: a code row's label is now served in words, so the labels no longer equal the sheet's raw labels; the ROW COUNT must
    if (first.length === want.length) firstEq += 1
    let fb = 0; let ft = 0; let fw = 0; let fr = 0; let fu = 0
    const isMaster = klass === 'master'
    if (isMaster) masterNames += 1
    const lab = (sheet.teamCensus || {}).labels || {}
    labelsBy.held += lab.held || 0; labelsBy.measured += lab.measured || 0
    labelsBy.factset_line += lab.factset_line || 0; labelsBy.bloomberg_line += lab.bloomberg_line || 0
    for (const r of first) {
      if (isMaster) masterRows += 1
      if (r.rowKind === 'heading') { headingRows += 1; if (IDENT.test(r.label)) rawHeadings += 1; continue }
      if (IDENT.test(r.label)) rawLabels += 1
      if (isMaster && r.source === 'why' && r.absentReason === MASTER_WHY) masterWhyExact += 1
      if (isMaster && r.source === 'bloomberg') masterBloomberg += 1
      if (isMaster && r.source === 'team') masterWithValue += 1
      if (r.source === 'team') {
        for (const cell of r.cells || []) {
          if (!cell) continue
          teamCells += 1
          const printed = sheetMod.formatTeamValue(cell.value, cell.format)
          const dec = (String(printed).split('.')[1] || '').replace(/[^0-9].*$/, '').length
          if (dec > 4) teamBeyond4 += 1
          if (typeof cell.format === 'string' && cell.format.includes('%')) { pctCells += 1; if (String(printed).includes('%')) pctPrinted += 1 }
        }
      }
      if (r.source === 'bloomberg') { if (refused(r, d.check_face)) fr += 1; else fb += 1 }
      else if (r.source === 'team') ft += 1
      else if (r.source === 'why') { fw += 1; if (!r.absentReason || BAR.test(String(r.absentReason))) barredWhy += 1 }
      else fu += 1
    }
    controlRendered += first.filter((r) => classes[rows.indexOf(r.label)] === 'CONTROL' && r.rowKind !== 'heading' && !r.source).length
    src.bloomberg += fb; src.team += ft; src.why += fw; src.refused += fr; src.unmapped += fu
    console.log('aw6 ' + key + ' class ' + klass + ' workbook ' + (t.workbook_key ? path.basename(String(t.workbook_key)) : 'None') + ' rows ' + rows.length +
      ' FIGURE ' + c.FIGURE + ' HEADING ' + c.HEADING + ' CONTROL ' + c.CONTROL + ' rendered ' + first.length + ' | bloomberg ' + fb + ' team ' + ft + ' why ' + fw + ' refused ' + fr + ' unmapped ' + fu)
  } else {
    console.log('aw6 ' + key + ' class ' + klass + ' rows ' + rows.length + ' (no row classes served: the page builds the base rows)')
  }
}
const f = cls.FIGURE
console.log('aw6 classes FIGURE ' + cls.FIGURE + ' HEADING ' + cls.HEADING + ' CONTROL ' + cls.CONTROL + ' sum ' + (cls.FIGURE + cls.HEADING + cls.CONTROL) + ' of rows ' + rowsTotal + (sumBroken ? ' SUM-BROKEN on ' + sumBroken + ' name(s)' : ''))
console.log('aw6 FIGURE by source bloomberg ' + src.bloomberg + ' team ' + src.team + ' why ' + src.why + ' refused ' + src.refused + ' unmapped ' + src.unmapped + ' of ' + f +
  ' (sum ' + (src.bloomberg + src.team + src.why + src.refused + src.unmapped) + ')')
console.log('aw6 rendered heading rows ' + headingRows + ', control rows rendered ' + controlRendered + ', why-rows with a barred word ' + barredWhy)
console.log('aw6 first group has as many rows as the sheet\'s non-CONTROL rows on ' + firstEq + ' of ' + withTeam + ' names with team rows')
console.log('aw6 labels by claim (rendered rows) held ' + labelsBy.held + ' measured ' + labelsBy.measured + ' factset_line ' + labelsBy.factset_line + ' bloomberg_line ' + labelsBy.bloomberg_line)
console.log('aw6 raw field codes visible: FIGURE-row labels ' + rawLabels + ', heading labels ' + rawHeadings + ' of ' + f + ' FIGURE rows (must be 0)')
console.log('aw6 team cells ' + teamCells + ', printed past 4 decimals ' + teamBeyond4 + ' (must be 0); percent-format cells ' + pctCells + ', printed as a percent ' + pctPrinted)
console.log('aw6 master names ' + masterNames + ', rendered rows ' + masterRows + ': Bloomberg ' + masterBloomberg + ', the template why ' + masterWhyExact + ', team value ' + masterWithValue + ' (must be 0)')
console.log('aw6 names with row classes served ' + withTeam + ' of ' + names.length + ' served; master_absent ' + masterAbsent)
