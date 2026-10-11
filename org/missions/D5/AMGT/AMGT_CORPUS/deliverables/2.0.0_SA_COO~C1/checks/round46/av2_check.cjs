/**
 * AMGT_CORPUS round 46 -- CRPS-av-2 (FWD-12 / FWD-20 render half): the Model tab's sheet builder honours the served ROW CLASS and the
 * team's own period values, with Bloomberg first. Issuer's file. Read-only unless --snapshot. Same harness shape as round 44's
 * at2_check.cjs: the REAL modelSheet.ts is transpiled with the installed typescript and run in a vm; only pure functions run.
 *
 * RUN:  node av2_check.cjs [<portal root>] [--snapshot]        (default portal root: <git toplevel>/portal)
 *
 * The seventh argument of `buildModelSheet` (`teamSheet`) now MAY carry, besides `{sheet, rows}` (round 44), the fields the reader serves:
 *   workbook_key        'amgt/.../Team Book.xlsx'            row_numbers   [9, 10, ...]  1-based sheet row, aligned with rows
 *   row_classes         'FIGURE' | 'HEADING' | 'CONTROL', aligned with rows
 *   periods             [{label: '2024', column: 'E'}, ...]   row_values   null | [value per period], aligned with rows
 * With `row_classes` present the builder returns, for the first group (the team rows):
 *   b1  CONTROL rows are NOT rows; HEADING rows are rows in sheet order with `rowKind: 'heading'`, no figure cell and no absentReason;
 *       and (round 44's AMENDMENT 1, kept) every OTHER group the base builds stays below the team rows, unchanged;
 *   b2  `sheet.teamCensus = {classes: {FIGURE, HEADING, CONTROL}, bySource: {bloomberg, team, why}, unmapped}` over the team rows, with
 *       unmapped 0 (a FIGURE row always has a source), and classes summing to `rows.length`;
 *   b3  PRECEDENCE: a FIGURE row whose label matches a row spec AND whose mnemonic the served figures carry shows BLOOMBERG's cells
 *       (`source: 'bloomberg'`), even when the team's own values exist;
 *   b4  a FIGURE row with no Bloomberg figure and a readable team value shows the team's value VERBATIM per sheet year (a period label
 *       YYYY fills the year 'YYYY' and the forecast column 'YYYYE'), `source: 'team'`, `sourceLabel: 'team model'`, and
 *       `teamCite: {workbook: <file name>, sheet, row: <row number>, label}`;
 *   b5  a FIGURE row with neither says why in words a PM reads (`source: 'why'`, a non-empty `absentReason` that is not "ABSENT",
 *       "REFUSED --" or "not read", and names no vendor mnemonic).
 * control c1: a teamSheet WITHOUT `row_classes` builds exactly as the base does (round 44's rows-only branch, snapshot);
 * control c2: no teamSheet builds exactly as the base does (snapshot). Prints `av2 build <b>/5 control <c>/2`.
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
  const roots = [portalRoot, path.join(top, 'portal')]
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

const m = load()
const specs = m.FINANCIAL_SUMMARY_ROWS || []
const epsSpec = specs.find((s) => s.mnemonic && s.label === 'EPS') || specs.find((s) => s.mnemonic)
const FIGURES = [
  { mnemonic: epsSpec.mnemonic, fiscal_year: 2024, value: 5, unit: 'PER SHARE' },
  { mnemonic: epsSpec.mnemonic, fiscal_year: 2025, value: 6, unit: 'PER SHARE' },
]
const YEARS = ['2024', '2025']
const FC = [2026, 2027, 2028].map((y) => ({ mnemonic: 'SALES_REV_TURN', fiscal_year: y, value: 100 + y - 2025, unit: 'USD' }))

const TEAM_BASE = {
  class: 'own_new',
  workbook_key: 'amgt/harvest/bronze/research-report/security_key=X_US_Equity/abc123/Team Book.xlsx',
  sheet: 'Model NEW VERSION',
  rows: ['Financial Summary', 'BEST_FPERIOD_OVERRIDE', epsSpec.label, 'Tobocco Volume', 'Mystery line', 'Year'],
}
const TEAM_CLASSED = {
  ...TEAM_BASE,
  row_classes: ['HEADING', 'CONTROL', 'FIGURE', 'FIGURE', 'FIGURE', 'HEADING'],
  row_numbers: [9, 10, 11, 12, 13, 14],
  periods: [2024, 2025, 2026, 2027, 2028].map((y, i) => ({ label: String(y), column: 'EFGHI'[i] })),
  row_values: [null, null, [1, 2, 3, 4, 5], [-0.03, 0.04, 0.05, 0.06, 0.07], ['#VALUE!', null, null, null, null], null],
}

function build(team) {
  return m.buildModelSheet(FIGURES, YEARS, null, FC, null, null, team)
}

const snap = path.join(HERE, 'av2_base_snapshot.json')
if (snapshot) {
  const base = { rowsOnly: JSON.parse(JSON.stringify(build(TEAM_BASE))), noTeam: JSON.parse(JSON.stringify(build(undefined))) }
  fs.writeFileSync(snap, JSON.stringify(base, null, 1) + '\n')
  console.log('SNAPSHOT written av2_base_snapshot.json from ' + portalRoot)
  process.exit(0)
}

let b1 = 0
let b2 = 0
let b3 = 0
let b4 = 0
let b5 = 0
try {
  const built = build(TEAM_CLASSED)
  const rows = ((built.groups || [])[0] || {}).rows || []
  const labels = rows.map((r) => r.label)
  const wantLabels = ['Financial Summary', epsSpec.label, 'Tobocco Volume', 'Mystery line', 'Year']
  const headings = rows.filter((r) => r.label === 'Financial Summary' || r.label === 'Year')
  const baseNoTeam = build(undefined)
  const belowKept = (built.groups || []).length === (baseNoTeam.groups || []).length
    && JSON.stringify((built.groups || []).slice(1)) === JSON.stringify((baseNoTeam.groups || []).slice(1))
  b1 = JSON.stringify(labels) === JSON.stringify(wantLabels)
    && belowKept
    && headings.length === 2
    && headings.every((r) => r.rowKind === 'heading' && (r.cells || []).every((c) => c === null || c === undefined) && !r.absentReason) ? 1 : 0
  console.log(`av2 b1 labels ${JSON.stringify(labels)}; headings ${headings.length}; other groups kept ${belowKept}; ok ${b1 === 1}`)

  const c = built.teamCensus || {}
  const cl = c.classes || {}
  const bs = c.bySource || {}
  b2 = cl.FIGURE === 3 && cl.HEADING === 2 && cl.CONTROL === 1 && bs.bloomberg === 1 && bs.team === 1 && bs.why === 1 && c.unmapped === 0
    && cl.FIGURE + cl.HEADING + cl.CONTROL === TEAM_CLASSED.rows.length ? 1 : 0
  console.log(`av2 b2 teamCensus ${JSON.stringify(c)}; ok ${b2 === 1}`)

  const eps = rows.find((r) => r.label === epsSpec.label) || {}
  b3 = eps.source === 'bloomberg' && (eps.cells || [])[0] && eps.cells[0].value === 5 && eps.cells[1] && eps.cells[1].value === 6 ? 1 : 0
  console.log(`av2 b3 EPS source ${eps.source}; first cells ${JSON.stringify((eps.cells || []).slice(0, 2).map((x) => x && x.value))}; ok ${b3 === 1}`)

  const tv = rows.find((r) => r.label === 'Tobocco Volume') || {}
  const tvVals = (tv.cells || []).map((x) => (x ? x.value : null))
  const cite = tv.teamCite || {}
  b4 = tv.source === 'team' && tv.sourceLabel === 'team model'
    && JSON.stringify(tvVals) === JSON.stringify([-0.03, 0.04, 0.05, 0.06, 0.07])
    && JSON.stringify((built.years || []).slice(-3)) === JSON.stringify(['2026E', '2027E', '2028E'])
    && cite.workbook === 'Team Book.xlsx' && cite.sheet === 'Model NEW VERSION' && cite.row === 12 && cite.label === 'Tobocco Volume' ? 1 : 0
  console.log(`av2 b4 team row source ${tv.source}; label ${tv.sourceLabel}; values ${JSON.stringify(tvVals)}; cite ${JSON.stringify(cite)}; ok ${b4 === 1}`)

  const why = rows.find((r) => r.label === 'Mystery line') || {}
  const reason = String(why.absentReason || '')
  b5 = why.source === 'why' && reason.trim().length > 12 && !/^(ABSENT|REFUSED --|not read)/i.test(reason.trim())
    && !/[A-Z]{3,}_[A-Z_]+/.test(reason) ? 1 : 0
  console.log(`av2 b5 why source ${why.source}; reason "${reason.slice(0, 90)}"; ok ${b5 === 1}`)
} catch (e) {
  console.log('av2 build threw: ' + String(e && e.message).slice(0, 160))
}
let c1 = 0
let c2 = 0
if (fs.existsSync(snap)) {
  const base = JSON.parse(fs.readFileSync(snap, 'utf8'))
  c1 = JSON.stringify(JSON.parse(JSON.stringify(build(TEAM_BASE)))) === JSON.stringify(base.rowsOnly) ? 1 : 0
  c2 = JSON.stringify(JSON.parse(JSON.stringify(build(undefined)))) === JSON.stringify(base.noTeam) ? 1 : 0
}
console.log(`av2 build ${b1 + b2 + b3 + b4 + b5}/5 control ${c1 + c2}/2`)
process.exit(b1 + b2 + b3 + b4 + b5 === 5 && c1 + c2 === 2 ? 0 : 1)
