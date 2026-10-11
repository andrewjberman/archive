/**
 * AMGT_CORPUS round 47 -- CRPS-aw-2 (FWD-20 render half): the Model tab's sheet builder prints a field-code row by the served
 * label in words, never by the code, and prints a team value by its own Excel number format. Issuer's file. Read-only unless
 * --snapshot. Same harness as round 46's av2_check.cjs: the REAL modelSheet.ts is transpiled with the installed typescript and
 * run in a vm; only pure functions run.
 *
 * RUN:  node aw2_check.cjs [<portal root>] [--snapshot]        (default portal root: <git toplevel>/portal)
 *
 * The seventh argument of `buildModelSheet` (`teamSheet`) MAY now carry, besides round 46's fields, two more aligned with `rows`:
 *   row_labels   null | {text, source: 'bloomberg'|'factset', claim: 'held'|'absent', cite: string|null, code, why: string|null}
 *   row_formats  null | [<the cell's Excel number format string, or null>, ... per period]      (non-null only for a FIGURE row)
 * Round 47 asserts, on the first group (the team rows):
 *   d1  a FIGURE row whose `row_labels[i]` is present prints `label` = its `text`, never the raw code; the row's `labelTitle` carries
 *       the code, and, when the claim is `absent`, the served `why`; a row with no `row_labels[i]` keeps its sheet label;
 *   d2  a team row whose label source is `factset` says `sourceLabel: 'FactSet, via team model'`; every other team row keeps
 *       'team model'; `teamCite.label` stays the sheet's own label (the code, as read);
 *   d3  `formatTeamValue(value, excelFormat)` is exported and prints by the format (table below), and a team cell carries its
 *       `format`; the cell's `value` stays the saved value (the full value rides the title);
 *   d4  `teamCensus.labels = {held, factset_line, bloomberg_line, raw}` over the rendered FIGURE rows, with `raw` (a rendered row
 *       label that still has the identifier form) 0; the round-46 census keys are unchanged.
 *   d5  (AMENDMENT 1, claim `measured`: the team's own label read from the workbook) a row whose `row_labels[i]` has `claim: 'measured'`
 *       prints `label` = its `text`; its `labelTitle` carries the code, the word `measured` and the `cite`; a `factset` source keeps
 *       `sourceLabel: 'FactSet, via team model'`; `teamCensus.labels` gains `measured` (the rendered rows whose entry is measured), and the
 *       measured rows are NOT counted in `held`, `factset_line` or `bloomberg_line`; `raw` stays 0.
 * control c1: a classed teamSheet WITHOUT row_labels / row_formats builds exactly as the base does (snapshot);
 * control c2: no teamSheet builds exactly as the base does (snapshot). Prints `aw2 build <b>/5 control <c>/2`.
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

const HELD_TEXT = 'Bloomberg adjusted EBITDA, millions of the reporting currency.'
const FS_WHY = 'FactSet data item; no published FactSet description was found; the meaning is not inferred from the name.'
const BB_WHY = 'Bloomberg field name; the estate field metadata does not describe it.'
const TEAM_BASE = {
  class: 'own_new',
  workbook_key: 'amgt/harvest/bronze/research-report/security_key=X_US_Equity/abc123/Team Book.xlsx',
  sheet: 'Model NEW VERSION',
  rows: ['Financial Summary', 'BEST_FPERIOD_OVERRIDE', epsSpec.label, 'EBITDA_ADJUSTED', 'FF_SALES', 'BS_TOT_LOAN', 'Mystery line', 'Year'],
}
const TEAM_CLASSED = {
  ...TEAM_BASE,
  row_classes: ['HEADING', 'CONTROL', 'FIGURE', 'FIGURE', 'FIGURE', 'FIGURE', 'FIGURE', 'HEADING'],
  row_numbers: [9, 10, 11, 12, 13, 14, 15, 16],
  periods: [2024, 2025, 2026, 2027, 2028].map((y, i) => ({ label: String(y), column: 'EFGHI'[i] })),
  row_values: [
    null, null,
    [1, 2, 3, 4, 5],
    [20885, 21417.4, 22933, 25138, 23982],
    [9000.456, 9100.5, 9200, 9300, 9400],
    [0.087, 0.003, 0.036, -0.028, 0.05],
    ['#VALUE!', null, null, null, null],
    null,
  ],
}
const TEAM_NEW = {
  ...TEAM_CLASSED,
  row_labels: [
    null, null, null,
    { text: HELD_TEXT, source: 'bloomberg', claim: 'held', cite: 'integrations/bloomberg/research/field_map.json', code: 'EBITDA_ADJUSTED', why: null },
    { text: 'FactSet line', source: 'factset', claim: 'absent', cite: null, code: 'FF_SALES', why: FS_WHY },
    { text: 'Bloomberg line', source: 'bloomberg', claim: 'absent', cite: null, code: 'BS_TOT_LOAN', why: BB_WHY },
    null, null,
  ],
  row_formats: [
    null, null,
    ['General', 'General', 'General', 'General', 'General'],
    ['#,##0', '#,##0', '#,##0', '#,##0', '#,##0'],
    ['#,##0.0', '#,##0.0', '#,##0.0', '#,##0.0', '#,##0.0'],
    ['0.0%', '0.0%', '0.0%', '0.0%', '0.0%'],
    null, null,
  ],
}

const TEAM_MEASURED = {
  ...TEAM_BASE,
  rows: ['Financial Summary', 'FF_SALES', 'FE_ESTIMATE'],
  row_classes: ['HEADING', 'FIGURE', 'FIGURE'],
  row_numbers: [9, 12, 13],
  periods: TEAM_CLASSED.periods,
  row_values: [null, [100, 110, 120, 130, 140], [200, 210, 220, 230, 240]],
  row_labels: [
    null,
    { text: 'Revenue', source: 'factset', claim: 'measured', cite: 'Model NEW VERSION!D4', code: 'FF_SALES', why: null },
    { text: 'Sales', source: 'factset', claim: 'measured', cite: 'Model NEW VERSION!B13', code: 'FE_ESTIMATE', why: null },
  ],
  row_formats: [null, ['#,##0', '#,##0', '#,##0', '#,##0', '#,##0'], ['General', 'General', 'General', 'General', 'General']],
}

function build(team) {
  return m.buildModelSheet(FIGURES, YEARS, null, FC, null, null, team)
}

const snap = path.join(HERE, 'aw2_base_snapshot.json')
if (snapshot) {
  const base = { classedOld: JSON.parse(JSON.stringify(build(TEAM_CLASSED))), noTeam: JSON.parse(JSON.stringify(build(undefined))) }
  fs.writeFileSync(snap, JSON.stringify(base, null, 1) + '\n')
  console.log('SNAPSHOT written aw2_base_snapshot.json from ' + portalRoot)
  process.exit(0)
}

const IDENT = /^[A-Z][A-Z0-9]*(_[A-Z0-9]+)+$/
let d1 = 0
let d2 = 0
let d3 = 0
let d4 = 0
let d5 = 0
try {
  const built = build(TEAM_NEW)
  const rows = ((built.groups || [])[0] || {}).rows || []
  const labels = rows.map((r) => r.label)
  const want = ['Financial Summary', epsSpec.label, HELD_TEXT, 'FactSet line', 'Bloomberg line', 'Mystery line', 'Year']
  const byCode = (code) => rows.find((r) => r.teamCite && r.teamCite.label === code) || {}
  const fsRow = byCode('FF_SALES')
  const heldRow = byCode('EBITDA_ADJUSTED')
  d1 = JSON.stringify(labels) === JSON.stringify(want)
    && !labels.some((l) => IDENT.test(l))
    && String(fsRow.labelTitle || '').includes('FF_SALES') && /no published/i.test(String(fsRow.labelTitle || ''))
    && String(heldRow.labelTitle || '').includes('EBITDA_ADJUSTED') ? 1 : 0
  console.log(`aw2 d1 labels ${JSON.stringify(labels)}; ok ${d1 === 1}`)

  const bbRow = byCode('BS_TOT_LOAN')
  d2 = fsRow.sourceLabel === 'FactSet, via team model' && heldRow.sourceLabel === 'team model' && bbRow.sourceLabel === 'team model'
    && fsRow.teamCite && fsRow.teamCite.label === 'FF_SALES' && fsRow.source === 'team' ? 1 : 0
  console.log(`aw2 d2 sourceLabels FF_SALES "${fsRow.sourceLabel}", EBITDA_ADJUSTED "${heldRow.sourceLabel}", BS_TOT_LOAN "${bbRow.sourceLabel}"; ok ${d2 === 1}`)

  const fmt = m.formatTeamValue
  const table = [
    [1234.567, '#,##0', '1,235'],
    [0.087, '0.0%', '8.7%'],
    [1.2345, '0.00', '1.23'],
    [-1234.5, '#,##0;(#,##0)', '(1,235)'],
    [28.066938033222375, 'General', '28.0669'],
    [100, 'General', '100'],
    [-0.028, '0.0%', '-2.8%'],
    [0.5, '0%', '50%'],
    [1234.5, '#,##0.00', '1,234.50'],
    [7, null, '7'],
    [1234.5, '"$"#,##0.00', '$1,234.50'],
  ]
  const got = typeof fmt === 'function' ? table.map(([v, f]) => String(fmt(v, f))) : []
  const tableOk = typeof fmt === 'function' && got.every((g, i) => g === table[i][2])
  const cell = (fsRow.cells || []).find((c) => c) || {}
  d3 = tableOk && cell.format === '#,##0.0' && cell.value === 9000.456 ? 1 : 0
  console.log(`aw2 d3 formatTeamValue ${typeof fmt}; table ${tableOk}${tableOk ? '' : ' got ' + JSON.stringify(got)}; cell.format ${cell.format}; value ${cell.value}; ok ${d3 === 1}`)

  const c = built.teamCensus || {}
  const lab = c.labels || {}
  const cl = c.classes || {}
  const bs = c.bySource || {}
  d4 = lab.held === 1 && lab.factset_line === 1 && lab.bloomberg_line === 1 && lab.raw === 0
    && cl.FIGURE === 5 && cl.HEADING === 2 && cl.CONTROL === 1 && bs.bloomberg === 1 && bs.team === 3 && bs.why === 1 && c.unmapped === 0 ? 1 : 0
  console.log(`aw2 d4 teamCensus ${JSON.stringify(c)}; ok ${d4 === 1}`)
  const bm = build(TEAM_MEASURED)
  const mrows = ((bm.groups || [])[0] || {}).rows || []
  const mlabels = mrows.map((r) => r.label)
  const rev = mrows.find((r) => r.teamCite && r.teamCite.label === 'FF_SALES') || {}
  const mc = (bm.teamCensus || {}).labels || {}
  d5 = JSON.stringify(mlabels) === JSON.stringify(['Financial Summary', 'Revenue', 'Sales'])
    && String(rev.labelTitle || '').includes('FF_SALES') && String(rev.labelTitle || '').includes('measured')
    && String(rev.labelTitle || '').includes('Model NEW VERSION!D4')
    && rev.sourceLabel === 'FactSet, via team model'
    && mc.measured === 2 && mc.held === 0 && mc.factset_line === 0 && mc.bloomberg_line === 0 && mc.raw === 0 ? 1 : 0
  console.log(`aw2 d5 measured labels ${JSON.stringify(mlabels)}; title "${String(rev.labelTitle || '')}"; census ${JSON.stringify(mc)}; ok ${d5 === 1}`)
} catch (e) {
  console.log('aw2 build threw: ' + String(e && e.message).slice(0, 160))
}
let c1 = 0
let c2 = 0
if (fs.existsSync(snap)) {
  const base = JSON.parse(fs.readFileSync(snap, 'utf8'))
  c1 = JSON.stringify(JSON.parse(JSON.stringify(build(TEAM_CLASSED)))) === JSON.stringify(base.classedOld) ? 1 : 0
  c2 = JSON.stringify(JSON.parse(JSON.stringify(build(undefined)))) === JSON.stringify(base.noTeam) ? 1 : 0
}
console.log(`aw2 build ${d1 + d2 + d3 + d4 + d5}/5 control ${c1 + c2}/2`)
process.exit(d1 + d2 + d3 + d4 + d5 === 5 && c1 + c2 === 2 ? 0 : 1)
