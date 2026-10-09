/**
 * AMGT_CORPUS round 44 -- CRPS-at-2 (FWD-12 render half): the Model tab's rows are the served team sheet's rows, in its order and
 * labels. Issuer's file. Read-only unless --snapshot. Harness: transpile the REAL modelSheet.ts with the installed typescript and run
 * it in a vm (round 40/41's page_check harness shape); only pure functions are exercised, no React render.
 *
 * RUN:  node at2_check.cjs [<portal root>] [--snapshot]       (default portal root: <git toplevel>/portal)
 *
 * The build: `buildModelSheet(...)` takes a 7th optional argument `teamSheet` = {sheet, rows: string[]} (the served
 * `model.team_sheet` from CRPS-at-1; the API field shape is {class, workbook_key, sheet, rows, model_rows_beside, reason}).
 *   b1  given teamSheet, the sheet's rows (all groups, in order) carry EXACTLY the team sheet's labels in the team sheet's order --
 *       no hard-coded row the team sheet does not carry, none of its rows dropped (fixture: 6 labels, two of which match an existing
 *       row spec's label and four of which do not).
 *   b2  (graded only once b1 holds) every team-sheet row with no figure says why in words: a non-empty reason that is not "ABSENT", "REFUSED --" or "not read".
 *   b3  AMENDMENT 1 (CTO render review msg 3189): with teamSheet given, the team rows LEAD as the first group and every OTHER
 *       group the base builds (margin history, v3 lines) stays BELOW, unchanged; the forecast years (2026E-2028E) survive.
 *   control  with teamSheet absent (undefined), buildModelSheet's output is byte-equal to at2_base_snapshot.json taken at the base.
 * Prints `at2 build <b>/3 control <c>/1`.
 */
const fs = require('fs')
const path = require('path')
const vm = require('vm')
const { execSync } = require('child_process')
const { createRequire } = require('module')

const HERE = __dirname
const top = execSync('git rev-parse --show-toplevel', { encoding: 'utf8' }).trim()
const args = process.argv.slice(2)
const snapshot = args.includes('--snapshot')
const portalRoot = path.resolve(args.filter((a) => !a.startsWith('--'))[0] || path.join(top, 'portal'))

function installed(name) {
  const roots = [portalRoot]
  try {
    const common = execSync('git rev-parse --path-format=absolute --git-common-dir', { encoding: 'utf8', cwd: top }).trim()
    roots.push(path.join(path.dirname(common), 'portal'))
  } catch (e) { /* optional */ }
  for (const root of roots) {
    try { return createRequire(path.join(root, 'package.json'))(name) } catch (e) { /* next */ }
  }
  throw new Error(name + ' not resolvable')
}
const ts = installed('typescript')
const stub = new Proxy({}, { get: (_t, k) => (k === '__esModule' ? true : () => '') })

function load() {
  const file = path.join(portalRoot, 'src', 'pages', 'SecurityAnalysis', 'modelSheet.ts')
  const out = ts.transpileModule(fs.readFileSync(file, 'utf8'), {
    compilerOptions: { module: ts.ModuleKind.CommonJS, target: ts.ScriptTarget.ES2020 },
  }).outputText
  const mod = { exports: {} }
  vm.runInNewContext(out, { module: mod, exports: mod.exports, require: () => stub, console })
  return mod.exports
}

const FIGURES = [
  { mnemonic: 'SALES_REV_TURN', fiscal_year: 2024, value: 100, unit: 'USD' },
  { mnemonic: 'SALES_REV_TURN', fiscal_year: 2025, value: 110, unit: 'USD' },
  { mnemonic: 'EBITDA', fiscal_year: 2024, value: 30, unit: 'USD' },
  { mnemonic: 'EBITDA', fiscal_year: 2025, value: 33, unit: 'USD' },
]
const YEARS = ['2024', '2025']

const m = load()
const base = m.buildModelSheet(FIGURES, YEARS, null, null, null, null)
const baseText = JSON.stringify(base)
if (snapshot) {
  fs.writeFileSync(path.join(HERE, 'at2_base_snapshot.json'), JSON.stringify(JSON.parse(baseText), null, 1) + '\n')
  console.log('SNAPSHOT written at2_base_snapshot.json from ' + portalRoot)
  process.exit(0)
}
const specLabels = (m.FINANCIAL_SUMMARY_ROWS || []).map((r) => r.label).filter(Boolean)
const teamRows = [specLabels[0] || 'Revenue', 'Gross profit (team)', specLabels[1] || 'EBITDA', 'Capex intensity', 'Net cash / (debt)', 'Dividend cover']
let b1 = 0
let b2 = 0
let b3 = 0
try {
  const built = m.buildModelSheet(FIGURES, YEARS, null, null, null, null, { sheet: 'Model NEW VERSION', rows: teamRows })
  const rows = ((built.groups || [])[0] || {}).rows || []
  const labels = rows.map((r) => r.label)
  b1 = JSON.stringify(labels) === JSON.stringify(teamRows) ? 1 : 0
  console.log(`at2 b1 rows ${labels.length} of ${teamRows.length}; order-and-labels ${b1 === 1}`)
  if (b1 !== 1) console.log('at2 b1 labels ' + JSON.stringify(labels.slice(0, 12)))
  const bad = /^(ABSENT|REFUSED --|not read)/i
  const empty = rows.filter((r) => (r.cells || []).every((c) => c == null))
  const words = empty.filter((r) => typeof r.absentReason === 'string' && r.absentReason.trim() && !bad.test(r.absentReason.trim()))
  // b2 grades the TEAM-SHEET rendering only: it counts once b1 holds (the base's hard-coded rows already carry worded reasons)
  b2 = b1 === 1 && empty.length > 0 && words.length === empty.length ? 1 : 0
  console.log(`at2 b2 rows with no figure ${empty.length}; with a reason in words ${words.length}`)
  const FC = [2026, 2027, 2028].map((y) => ({ mnemonic: 'SALES_REV_TURN', fiscal_year: y, value: 100 + y - 2025, unit: 'USD' }))
  const baseF = m.buildModelSheet(FIGURES, YEARS, null, FC, null, null)
  const teamF = m.buildModelSheet(FIGURES, YEARS, null, FC, null, null, { sheet: 'Model NEW VERSION', rows: teamRows })
  const rest = JSON.stringify((baseF.groups || []).slice(1))
  const below = JSON.stringify((teamF.groups || []).slice(1))
  const yearsKept = JSON.stringify(teamF.years) === JSON.stringify(baseF.years) && (teamF.years || []).some((y) => /E$/.test(String(y)))
  b3 = b1 === 1 && (baseF.groups || []).length > 1 && below === rest && yearsKept ? 1 : 0
  console.log(`at2 b3 groups below the team rows ${(teamF.groups || []).length - 1} of ${(baseF.groups || []).length - 1} kept unchanged ${below === rest}; forecast years kept ${yearsKept}`)
} catch (e) {
  console.log('at2 build threw: ' + String(e && e.message).slice(0, 160))
}
const snap = path.join(HERE, 'at2_base_snapshot.json')
const control = fs.existsSync(snap) && JSON.stringify(JSON.parse(fs.readFileSync(snap, 'utf8'))) === baseText ? 1 : 0
console.log(`at2 build ${b1 + b2 + b3}/3 control ${control}/1`)
process.exit(b1 + b2 + b3 === 3 && control === 1 ? 0 : 1)
