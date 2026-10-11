/**
 * AMGT_CORPUS round 45 -- CRPS-au-3 (FWD-12 rendered read) and CRPS-au-4 (FWD-20 census of the rendered rows). Issuer's file. READ-ONLY.
 *
 * RUN:  node au3_rendered_rows.cjs <portal root> <capture.json>
 *   <portal root> holds src/pages/SecurityAnalysis/{modelSheet.ts,figureIdentity.ts} AT THE DEV HEAD under read (extracted with
 *   `git show <DEV sha>:<path>`); the capture is au3_capture.py's output over the LIVE function.
 *
 * METHOD. The REAL modelSheet.ts and figureIdentity.ts are transpiled with the installed typescript and run in a vm (round 40/44
 * harness shape). Per name, `buildModelSheet` is called with exactly the six-plus-one arguments ModelTab.tsx passes
 * (fiscal_year_figures, fiscal_years, model.line_names, model.forecast_figures, model.fiscal_unresolved, header_figures,
 * model.team_sheet), and the check face is read through the real `checkFor`, as ModelTab's `rowRefusal` does. It is the sheet
 * builder the page calls on served data, not a browser DOM walk; no React render is run.
 *
 * au-3  per name: workbook and sheet; for a name whose team sheet carries rows, the first rendered group's labels equal the team
 *       sheet's rows in order and labels; the class census (own_new / own_model / master / master_absent) sums to the names;
 *       `model_rows_beside` is printed where the workbook holds both sheets.
 * au-4  over every name with model_status SERVED, every rendered row of every group is one of: shown (a non-null cell, not
 *       refused), refused (a cell the check face REFUSES), absent (no figure, a reason in words), unmapped (no mnemonic: the row's
 *       label names no field the page reads). The denominator is printed; every absent/unmapped reason is checked against the
 *       bar words "ABSENT", "REFUSED --", "not read".
 * Controls: c1 a mutant (the first team row dropped) must read as a mismatch; c2 with team_sheet absent the output equals the base
 *       build with no seventh argument.
 */
const fs = require('fs')
const path = require('path')
const vm = require('vm')
const { execSync } = require('child_process')
const { createRequire } = require('module')

const portalRoot = path.resolve(process.argv[2])
const capturePath = path.resolve(process.argv[3])
const top = execSync('git rev-parse --show-toplevel', { encoding: 'utf8' }).trim()

function installed(name) {
  const roots = [path.join(top, 'portal')]
  for (const root of roots) {
    try { return createRequire(path.join(root, 'package.json'))(name) } catch (e) { /* next */ }
  }
  throw new Error(name + ' not resolvable')
}
const ts = installed('typescript')
const stub = new Proxy({}, { get: (_t, k) => (k === '__esModule' ? true : () => '') })

function load(rel, extra) {
  const file = path.join(portalRoot, 'src', 'pages', 'SecurityAnalysis', rel)
  const out = ts.transpileModule(fs.readFileSync(file, 'utf8'), {
    compilerOptions: { module: ts.ModuleKind.CommonJS, target: ts.ScriptTarget.ES2020 },
  }).outputText
  const mod = { exports: {} }
  vm.runInNewContext(out, { module: mod, exports: mod.exports, require: (n) => (extra && extra[n]) || stub, console })
  return mod.exports
}
const sheetMod = load('modelSheet.ts')
const identity = load('figureIdentity.ts')
const cap = JSON.parse(fs.readFileSync(capturePath, 'utf8'))
const BAR = /^(ABSENT|REFUSED --|not read)/i

function build(d, withTeam) {
  const model = d.model || {}
  const forecasts = Array.isArray(model.forecast_figures) ? model.forecast_figures : undefined
  const team = withTeam && model.team_sheet && typeof model.team_sheet === 'object' ? model.team_sheet : undefined
  return sheetMod.buildModelSheet(d.fiscal_year_figures || [], d.fiscal_years, model.line_names === '<KEY ABSENT>' ? undefined : model.line_names,
    forecasts, Array.isArray(model.fiscal_unresolved) ? model.fiscal_unresolved : undefined, d.header_figures, team)
}
function refusedRow(row, checks) {
  for (const figure of row.cells || []) {
    if (!figure) continue
    const c = identity.checkFor(checks || [], figure)
    if (c && c.verdict === 'REFUSE') return true
  }
  return false
}

const names = Object.keys(cap.keys).sort()
const classes = {}
let au3Match = 0
let au3Compared = 0
const mismatches = []
const rowTotals = { shown: 0, refused: 0, absent: 0, unmapped: 0 }
const unmappedLabels = {}
let barred = 0
let unmappedTeamSentence = 0
const teamSentence = sheetMod.TEAM_ROW_NO_FIGURE
let namesWithBlock = 0
let ctrlBaseEqual = 0
let ctrlBaseTried = 0
console.log('capture function CodeSha256 ' + cap.function.CodeSha256 + ' LastModified ' + cap.function.LastModified)
for (const key of names) {
  const d = cap.keys[key]
  const ts0 = (d.model || {}).team_sheet
  const cls = ts0 && typeof ts0 === 'object' ? ts0.class : 'KEY-ABSENT'
  classes[cls] = (classes[cls] || 0) + 1
  const sheet = build(d, true)
  const teamRows = ts0 && Array.isArray(ts0.rows) ? ts0.rows.filter((l) => typeof l === 'string' && l.trim()) : []
  let au3 = 'n/a'
  if (teamRows.length > 0) {
    au3Compared += 1
    const first = ((sheet.groups || [])[0] || {}).rows || []
    const labels = first.map((r) => r.label)
    const same = JSON.stringify(labels) === JSON.stringify(teamRows)
    if (same) au3Match += 1
    else mismatches.push(key)
    au3 = same ? 'EQUAL ' + teamRows.length : 'DIFFERENT rendered ' + labels.length + ' team ' + teamRows.length
  } else {
    // control c2: no team rows served -> output equals the build without the seventh argument
    ctrlBaseTried += 1
    const a = JSON.stringify(build(d, true))
    const b = JSON.stringify(sheetMod.buildModelSheet(d.fiscal_year_figures || [], d.fiscal_years, undefined,
      Array.isArray((d.model || {}).forecast_figures) ? d.model.forecast_figures : undefined,
      Array.isArray((d.model || {}).fiscal_unresolved) ? d.model.fiscal_unresolved : undefined, d.header_figures))
    if (a === b) ctrlBaseEqual += 1
  }
  const beside = ts0 && Array.isArray(ts0.model_rows_beside) ? ts0.model_rows_beside.length : null
  console.log('au3 ' + key + ' class ' + cls + ' workbook ' + (ts0 && ts0.workbook_key ? path.basename(String(ts0.workbook_key)) : 'None') +
    ' sheet ' + (ts0 && ts0.sheet) + ' rows_vs_team ' + au3 + (beside != null ? ' model_rows_beside ' + beside : ''))
  if (d.model_status === 'SERVED') {
    namesWithBlock += 1
    for (const group of sheet.groups || []) {
      for (const row of group.rows || []) {
        const refused = refusedRow(row, d.check_face)
        const hasFigure = (row.cells || []).some((c) => c !== null && c !== undefined)
        let state
        if (refused) state = 'refused'
        else if (hasFigure) state = 'shown'
        else if (!row.mnemonic) state = 'unmapped'
        else state = 'absent'
        rowTotals[state] += 1
        if (state === 'unmapped') {
          unmappedLabels[row.label] = (unmappedLabels[row.label] || 0) + 1
          if (row.absentReason === teamSentence) unmappedTeamSentence += 1
        }
        if ((state === 'absent' || state === 'unmapped') && (!row.absentReason || BAR.test(String(row.absentReason).trim()))) barred += 1
      }
    }
  }
}
// control c1: a mutant -- drop the first team row of the first name that carries rows; it must NOT read EQUAL
let c1 = 'n/a'
for (const key of names) {
  const d = JSON.parse(JSON.stringify(cap.keys[key]))
  const t = d.model.team_sheet
  if (t && Array.isArray(t.rows) && t.rows.length > 1) {
    const expected = t.rows.slice()
    t.rows = t.rows.slice(1)
    const labels = (((build(d, true).groups || [])[0] || {}).rows || []).map((r) => r.label)
    c1 = JSON.stringify(labels) !== JSON.stringify(expected) ? 'FIRED-AS-EXPECTED' : 'DID-NOT-FIRE'
    break
  }
}
const sum = Object.values(classes).reduce((a, b) => a + b, 0)
console.log('au3 classes ' + JSON.stringify(classes) + ' sum ' + sum + ' of ' + names.length + ' served names')
console.log('au3 compared ' + au3Compared + ' equal ' + au3Match + ' different ' + mismatches.length + (mismatches.length ? ' ' + mismatches.slice(0, 8).join(',') : ''))
console.log('au4 names with a model block ' + namesWithBlock + ' of ' + names.length)
const cells = rowTotals.shown + rowTotals.refused + rowTotals.absent + rowTotals.unmapped
console.log('au4 CENSUS shown ' + rowTotals.shown + ' refused ' + rowTotals.refused + ' absent ' + rowTotals.absent + ' unmapped ' + rowTotals.unmapped + ' of ' + cells + ' rendered rows')
console.log('au4 rows whose reason is missing or a barred word ' + barred)
console.log('au4 unmapped rows that read the team-row sentence (a team label with no field behind it) ' + unmappedTeamSentence + ' of ' + rowTotals.unmapped)
const top20 = Object.entries(unmappedLabels).sort((a, b) => b[1] - a[1]).slice(0, 20)
console.log('au4 unmapped distinct labels ' + Object.keys(unmappedLabels).length + (top20.length ? '; most common: ' + top20.map(([l, n]) => l + ' x' + n).join(' | ') : ''))
console.log('control c1 mutant (first team row dropped) ' + c1)
console.log('control c2 no team rows served: build equals the base build ' + ctrlBaseEqual + ' of ' + ctrlBaseTried)
