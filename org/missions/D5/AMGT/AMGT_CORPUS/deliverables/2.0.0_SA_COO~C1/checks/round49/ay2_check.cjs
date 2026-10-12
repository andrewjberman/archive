/**
 * AMGT_CORPUS round 49 -- CRPS-ay-2 (FWD-20 render half, C-S64 and C-S65; decomposition v49.1): the Model tab's sheet builder (a) carries
 * the team's BLOCKS (period, case, unread) as their own small tables under the sheet's own headers and never prints a BLOCK row under a
 * period header, and (b) carries a text cell of a figure row by what it is (an error token, or the team's own word). Issuer's file.
 * Read-only unless --snapshot. Same harness as round 47's aw2_check.cjs: the REAL modelSheet.ts is transpiled with the installed
 * typescript and run in a vm; only pure functions run; ModelTab.tsx is read as text (arm d6).
 *
 * RUN:  node ay2_check.cjs [<portal root>] [--snapshot]        (default portal root: <git toplevel>/portal)
 *
 * The seventh argument of `buildModelSheet` (`teamSheet`) MAY now carry, besides round 46-47's fields:
 *   row_classes  may hold 'BLOCK' (a block row: row_values[i] and row_formats[i] are null; it prints in its block only)
 *   blocks       [{first_row, last_row, kind:'period'|'case'|'unread', why:string|null, withheld:int, columns:[letter],
 *                  rows:[{row_number, kind:'title'|'years'|'body', block_row:bool, cells:[null | {v: number|string, f: <Excel format>|null}]}]}]
 *                (present only when there is a BLOCK row; an UNREAD block has columns [] and every row's cells [])
 * Asserted:
 *   d1  `sheetBlocks` (present ONLY with a non-empty `blocks`): per block `firstRow, lastRow, kind, why, withheld, columns, rows[{rowNumber,
 *       kind, blockRow, cells}]`; a number cell is `{value, format, display}` with `display` = formatTeamValue(value, format) except an
 *       integer 1990..2100 in a title or years row, which prints as the plain integer ("2026", never "2,026"); a text cell is `{text}`
 *       verbatim; an empty cell stays null. A served 'BLOCK' class is in NO group's rows and no BLOCK value is printed under any period;
 *       `teamCensus.classes.BLOCK` counts them (the key exists only when one is served), the classes still sum to the sheet's row count,
 *       and `teamCensus.blocks = {period:{blocks,rows}, case:{...}, unread:{...}, withheld}` (rows = rows with blockRow true).
 *   d2  a string cell of a team FIGURE row (one that also holds a number) is carried: a string starting with `#` -> `text` + `textKind:
 *       'error'`; any other non-empty string -> `text` + `textKind:'word'`; blank/null stays null. A row with NO number keeps its row-level
 *       why, unchanged. `teamCensus.text = {error, word, empty, unclassed}` over the rendered team FIGURE rows' cells for the displayed
 *       years, `unclassed` 0. A text cell is not a figure: `renderedFigureCount` does not count it.
 *   d3  a FIGURE row of numbers plus 'NA', '#N/A' and '2.5%-3.1%' stays a FIGURE row of the period grid, source 'team', its text cells
 *       carried (NA and the range as words, '#N/A' as an error); it is NOT a BLOCK row and no block is made.
 *   d4  a classed payload with no `blocks` and no text cell: no `sheetBlocks`, no `BLOCK` key in `teamCensus.classes`, no `teamCensus.blocks`,
 *       `teamCensus.text` all zeros, and everything except `teamCensus.text` byte-equal to the base (snapshot).
 *   d5  `blocks` present beside a payload whose row classes are all FIGURE/HEADING/CONTROL (inconsistent): no throw, `sheetBlocks` built,
 *       groups unchanged.
 *   d6  ModelTab.tsx (text): carries `data-sheet-block`, `unread`, the visible words `error in team sheet`, and `textKind`.
 *   d7  an UNREAD block (a header-less one-row block): kind 'unread', `why` served, `withheld` carried, columns [] and every row's cells
 *       [], no value printed (not even when a payload wrongly carries cells on it), the row is in no group, `census.blocks.unread.rows` 1.
 *   d8  a block headed by TEXT period labels (1Q26..4Q26) is kind 'period' and is carried aligned to its own labels (the label cell and
 *       the figure of one column sit at one index; the label text is not turned into a number).
 * control c1: the classed round-47 payload builds as the base does (snapshot) except the added `teamCensus.text`;
 * control c2: no teamSheet builds exactly as the base does (snapshot).
 * Prints `ay2 build <b>/8 control <c>/2`.
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
  rows: ['Financial Summary', 'BEST_FPERIOD_OVERRIDE', epsSpec.label, 'EBITDA_ADJUSTED', 'FF_SALES', 'BS_TOT_LOAN', 'Mystery line', 'Year'],
}
const PERIODS = [2024, 2025, 2026, 2027, 2028].map((y, i) => ({ label: String(y), column: 'EFGHI'[i] }))
// The round-47 classed payload: the same bytes aw2_check.cjs used for its control c1.
const TEAM_CLASSED = {
  ...TEAM_BASE,
  row_classes: ['HEADING', 'CONTROL', 'FIGURE', 'FIGURE', 'FIGURE', 'FIGURE', 'FIGURE', 'HEADING'],
  row_numbers: [9, 10, 11, 12, 13, 14, 15, 16],
  periods: PERIODS,
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

// ---- d1: a ROG-like block (title row, years row, four body rows, four label columns) and a BABA-like block (no separator cell) ----
const COLS_A = 'BCDEFGHIJKLMNOPQ'.split('')
const cellsAt = (map) => COLS_A.map((c) => (map[c] === undefined ? null : map[c]))
const n = (v, f) => ({ v, f })
const t = (v) => ({ v, f: null })
const BLOCK_A = {
  first_row: 45,
  last_row: 50,
  kind: 'case',
  why: null,
  withheld: 0,
  columns: COLS_A,
  rows: [
    { row_number: 45, kind: 'title', block_row: false, cells: cellsAt({ B: t('Upside Case'), F: t('Base Case'), J: t('Downside Case'), N: t('Upside / Downside') }) },
    { row_number: 46, kind: 'years', block_row: false, cells: cellsAt({ C: n(2026, '#,##0'), D: n(2027, 'General'), E: n(2028, 'General'), G: n(2026, 'General'), H: n(2027, 'General'), I: n(2028, 'General'), K: n(2026, 'General'), L: n(2027, 'General'), M: n(2028, 'General'), O: n(2026, 'General'), P: n(2027, 'General'), Q: n(2028, 'General') }) },
    { row_number: 47, kind: 'body', block_row: true, cells: cellsAt({ B: t('Case EPS'), C: n(24.01652054794521, '0.00'), D: n(4242.4242, '0.00'), E: n(29.059989863013705, '0.00'), F: t('Case EPS'), G: n(20.429, '0.00'), H: n(21.719, '0.00'), I: n(23.412, '0.00'), J: t('Case EPS'), K: n(15.77758991111401, '0.00'), L: n(14.639417348350534, '0.00'), M: n(13.58335091142286, '0.00'), N: t('Ratio'), O: n(1.2790020010996404, '0.00'), P: n(1.5002216634349494, '0.00'), Q: n(1.7324597584055672, '0.00') }) },
    { row_number: 48, kind: 'body', block_row: true, cells: cellsAt({ B: t('Case Multiple'), C: n(25, '0.0'), D: n(25, '0.0'), E: n(25, '0.0'), F: t('Case Multiple'), G: n(17.5, '0.0'), H: n(17.5, '0.0'), I: n(17.5, '0.0'), J: t('Case Multiple'), K: n(10, '0.0'), L: n(10, '0.0'), M: n(10, '0.0'), N: t('Tgt'), O: n(452.86, '0.0'), P: n(489.1, '0.0'), Q: n(529.6, '0.0') }) },
    { row_number: 49, kind: 'body', block_row: true, cells: cellsAt({ B: t('Case Price'), C: n(600.41, '#,##0.00'), D: n(660.4543150684933, '#,##0.00'), E: n(726.5, '#,##0.00'), F: t('Case Price'), G: n(357.5, '#,##0.00'), H: n(380.08, '#,##0.00'), I: n(409.71, '#,##0.00'), J: t('Case Price'), K: n(157.78, '#,##0.00'), L: n(146.39, '#,##0.00'), M: n(135.83, '#,##0.00'), N: t('Multiple'), O: n(22.17, '#,##0.00'), P: n(22.52, '#,##0.00'), Q: n(22.62, '#,##0.00') }) },
    { row_number: 50, kind: 'body', block_row: true, cells: cellsAt({ B: t('Case Return'), C: n(0.7057187889165633, '0.0%'), D: n(0.8762906678082196, '0.0%'), E: n(1.0639, '0.0%'), F: t('Case Return'), G: n(0.0156, '0.0%'), H: n(0.0798, '0.0%'), I: n(0.1639, '0.0%'), J: t('Case Return'), K: n(-0.5518, '0.0%'), L: n(-0.5841, '0.0%'), M: n(-0.6141, '0.0%'), N: t('Return'), O: n(0.2866, '0.0%'), P: n(0.3895, '0.0%'), Q: n(0.5046, '0.0%') }) },
  ],
}
const BLOCK_B = {
  first_row: 53,
  last_row: 55,
  kind: 'case',
  why: null,
  withheld: 0,
  columns: ['B', 'C', 'D', 'E', 'F'],
  rows: [
    { row_number: 53, kind: 'title', block_row: false, cells: [t('Upside Case'), null, null, t('Base Case'), null] },
    { row_number: 54, kind: 'years', block_row: false, cells: [t('Year'), n(2026, 'General'), n(2027, 'General'), n(2026, 'General'), n(2027, 'General')] },
    { row_number: 55, kind: 'body', block_row: true, cells: [t('Case Rev Growth'), n(0.0713, '0.0%'), n(0.0911, '0.0%'), n(0.0521, '0.0%'), n(0.0433, '0.0%')] },
  ],
}
const TEAM_BLOCK = {
  ...TEAM_BASE,
  rows: ['Financial Summary', epsSpec.label, 'Case EPS', 'Case Multiple', 'Case Price', 'Case Return', 'Case Rev Growth', 'FF_SALES'],
  row_classes: ['HEADING', 'FIGURE', 'BLOCK', 'BLOCK', 'BLOCK', 'BLOCK', 'BLOCK', 'FIGURE'],
  row_numbers: [9, 11, 47, 48, 49, 50, 55, 60],
  periods: PERIODS,
  row_values: [null, [1, 2, 3, 4, 5], null, null, null, null, null, [100, 110, 120, 130, 140]],
  row_formats: [null, ['General', 'General', 'General', 'General', 'General'], null, null, null, null, null, ['#,##0', '#,##0', '#,##0', '#,##0', '#,##0']],
  blocks: [BLOCK_A, BLOCK_B],
}

// ---- d7: an unread block (no header-like cell above its numbers; the reader withheld them) ----
const UNREAD_WHY = "The research team's sheet holds numbers here with no header above them, so none is shown."
const BLOCK_U = {
  first_row: 70,
  last_row: 70,
  kind: 'unread',
  why: UNREAD_WHY,
  withheld: 3,
  columns: [],
  rows: [{ row_number: 70, kind: 'body', block_row: true, cells: [] }],
}
const TEAM_UNREAD = {
  ...TEAM_BASE,
  rows: ['Financial Summary', epsSpec.label, 'Orphan line'],
  row_classes: ['HEADING', 'FIGURE', 'BLOCK'],
  row_numbers: [9, 11, 70],
  periods: PERIODS,
  row_values: [null, [1, 2, 3, 4, 5], null],
  row_formats: [null, ['General', 'General', 'General', 'General', 'General'], null],
  blocks: [BLOCK_U],
}
// the same, with a payload that wrongly carries cells on the unread block: the portal still prints no value
const TEAM_UNREAD_DIRTY = {
  ...TEAM_UNREAD,
  blocks: [{ ...BLOCK_U, columns: ['B', 'C'], rows: [{ row_number: 70, kind: 'body', block_row: true, cells: [t('Orphan line'), n(9999.9876, '0.00')] }] }],
}

// ---- d8: a block headed by text period labels ----
const BLOCK_P = {
  first_row: 80,
  last_row: 82,
  kind: 'period',
  why: null,
  withheld: 0,
  columns: ['B', 'C', 'D', 'E', 'F'],
  rows: [
    { row_number: 80, kind: 'title', block_row: false, cells: [t('Quarterly'), t('1Q26'), t('2Q26'), t('3Q26'), t('4Q26')] },
    { row_number: 81, kind: 'body', block_row: true, cells: [t('Qtr Revenue'), n(1250.5, '#,##0.0'), n(1310.25, '#,##0.0'), n(1402, '#,##0.0'), n(1488.75, '#,##0.0')] },
    { row_number: 82, kind: 'body', block_row: true, cells: [t('Qtr Margin'), n(0.211, '0.0%'), n(0.219, '0.0%'), n(0.224, '0.0%'), n(0.231, '0.0%')] },
  ],
}
const TEAM_PERIOD = {
  ...TEAM_BASE,
  rows: ['Financial Summary', 'Qtr Revenue', 'Qtr Margin'],
  row_classes: ['HEADING', 'BLOCK', 'BLOCK'],
  row_numbers: [9, 81, 82],
  periods: PERIODS,
  row_values: [null, null, null],
  row_formats: [null, null, null],
  blocks: [BLOCK_P],
}

// ---- d2 / d3: text cells ----
const TEAM_TEXT = {
  ...TEAM_BASE,
  rows: ['Financial Summary', 'Mix line', 'Text only line'],
  row_classes: ['HEADING', 'FIGURE', 'FIGURE'],
  row_numbers: [9, 12, 13],
  periods: PERIODS,
  row_values: [null, [1, '#N/A', 'NM', null, 2.5], ['#VALUE!', 'NA', null, null, null]],
}
const TEAM_TEXT_NULLS = {
  ...TEAM_TEXT,
  row_values: [null, [1, null, null, null, 2.5], ['#VALUE!', 'NA', null, null, null]],
}
const TEAM_NUMTEXT = {
  ...TEAM_BASE,
  rows: ['Financial Summary', 'Range line'],
  row_classes: ['HEADING', 'FIGURE'],
  row_numbers: [9, 12],
  periods: PERIODS,
  row_values: [null, [0.1, 'NA', '#N/A', '2.5%-3.1%', 0.2]],
}

function build(team) {
  return m.buildModelSheet(FIGURES, YEARS, null, FC, null, null, team)
}
const clone = (v) => JSON.parse(JSON.stringify(v))
const firstGroupRows = (built) => ((built.groups || [])[0] || {}).rows || []

const snap = path.join(HERE, 'ay2_base_snapshot.json')
if (snapshot) {
  const base = { classedOld: clone(build(TEAM_CLASSED)), noTeam: clone(build(undefined)) }
  fs.writeFileSync(snap, JSON.stringify(base, null, 1) + '\n')
  console.log('SNAPSHOT written ay2_base_snapshot.json from ' + portalRoot)
  process.exit(0)
}

let d1 = 0
let d2 = 0
let d3 = 0
let d4 = 0
let d5 = 0
let d6 = 0
let d7 = 0
let d8 = 0
try {
  const built = build(TEAM_BLOCK)
  const cb = built.sheetBlocks || []
  const a = cb[0] || {}
  const b = cb[1] || {}
  const col = (block, letter) => (block.columns || []).indexOf(letter)
  const rowOf = (block, rn) => (block.rows || []).find((r) => r.rowNumber === rn) || { cells: [] }
  const c47 = rowOf(a, 47).cells
  const c46 = rowOf(a, 46).cells
  const c50 = rowOf(a, 50).cells
  const allRows = (built.groups || []).flatMap((g) => g.rows || [])
  const labels = allRows.map((r) => r.label)
  const teamRowNumbers = allRows.map((r) => (r.teamCite ? r.teamCite.row : null))
  const printed = JSON.stringify(built.groups || [])
  const cl = (built.teamCensus || {}).classes || {}
  const blockLabels = ['Case EPS', 'Case Multiple', 'Case Price', 'Case Return', 'Case Rev Growth']
  const shapeOk = cb.length === 2 && a.firstRow === 45 && a.lastRow === 50 && (a.columns || []).length === 16
    && JSON.stringify((a.rows || []).map((r) => r.kind)) === JSON.stringify(['title', 'years', 'body', 'body', 'body', 'body'])
    && JSON.stringify((a.rows || []).map((r) => r.blockRow)) === JSON.stringify([false, false, true, true, true, true])
    && a.kind === 'case' && a.why === null && a.withheld === 0 && b.kind === 'case'
    && b.firstRow === 53 && b.lastRow === 55 && (b.rows || []).length === 3
    && rowOf(b, 55).blockRow === true && (rowOf(b, 55).cells[1] || {}).display === '7.1%'
  const cellsOk = (c47[col(a, 'C')] || {}).display === '24.02' && (c47[col(a, 'C')] || {}).format === '0.00'
    && (c47[col(a, 'C')] || {}).value === 24.01652054794521
    && (c47[col(a, 'F')] || {}).text === 'Case EPS' && (c47[col(a, 'N')] || {}).text === 'Ratio'
    && (c50[col(a, 'C')] || {}).display === '70.6%' && (c50[col(a, 'K')] || {}).display === '-55.2%'
    && c46[col(a, 'F')] === null && (c46[col(a, 'C')] || {}).display === '2026'
    && (rowOf(a, 45).cells[col(a, 'J')] || {}).text === 'Downside Case'
    && (rowOf(b, 54).cells[2] || {}).display === '2027'
  const outOfGridOk = blockLabels.every((l) => !labels.includes(l))
    && [47, 48, 49, 50, 55].every((r) => !teamRowNumbers.includes(r))
    && !printed.includes('4242.4242') && !printed.includes('660.4543150684933') && !printed.includes('24.01652054794521')
    && labels.includes(epsSpec.label) && labels.includes('FF_SALES')
  const bl = (built.teamCensus || {}).blocks || {}
  const censusOk = cl.BLOCK === 5 && cl.FIGURE === 2 && cl.HEADING === 1 && cl.CONTROL === 0
    && cl.BLOCK + cl.FIGURE + cl.HEADING + cl.CONTROL === TEAM_BLOCK.rows.length
    && JSON.stringify(bl) === JSON.stringify({ period: { blocks: 0, rows: 0 }, case: { blocks: 2, rows: 5 }, unread: { blocks: 0, rows: 0 }, withheld: 0 })
  d1 = shapeOk && cellsOk && outOfGridOk && censusOk ? 1 : 0
  console.log(`ay2 d1 sheetBlocks ${cb.length} shape ${shapeOk} cells ${cellsOk} outOfGrid ${outOfGridOk} census ${JSON.stringify(cl)} blocks ${JSON.stringify(bl)} ok ${censusOk}; d1 ${d1 === 1}`)

  const tx = build(TEAM_TEXT)
  const mix = firstGroupRows(tx).find((r) => r.teamCite && r.teamCite.row === 12) || {}
  const only = firstGroupRows(tx).find((r) => r.teamCite === undefined && r.label === 'Text only line') || {}
  const mc = mix.cells || []
  const tc = (tx.teamCensus || {}).text
  const nullBuild = build(TEAM_TEXT_NULLS)
  d2 = mc.length === 5 && mc[0] && mc[0].value === 1 && mc[0].text === undefined
    && mc[1] && mc[1].text === '#N/A' && mc[1].textKind === 'error'
    && mc[2] && mc[2].text === 'NM' && mc[2].textKind === 'word'
    && mc[3] === null && mc[4] && mc[4].value === 2.5
    && only.source === 'why' && String(only.absentReason || '').includes('"#VALUE!"')
    && tc && tc.error === 1 && tc.word === 1 && tc.empty === 1 && tc.unclassed === 0
    && tx.renderedFigureCount === nullBuild.renderedFigureCount ? 1 : 0
  console.log(`ay2 d2 mix cells ${JSON.stringify(mc.map((c) => (c ? (c.text !== undefined ? c.text + ':' + c.textKind : c.value) : null)))}; why-row source ${only.source}; text census ${JSON.stringify(tc)}; rendered ${tx.renderedFigureCount} vs ${nullBuild.renderedFigureCount}; ok ${d2 === 1}`)

  const nt = build(TEAM_NUMTEXT)
  const rng = firstGroupRows(nt).find((r) => r.teamCite && r.teamCite.row === 12) || {}
  const rc = rng.cells || []
  const nc = (nt.teamCensus || {}).classes || {}
  d3 = rng.source === 'team' && rc.length === 5 && rc[0] && rc[0].value === 0.1 && rc[4] && rc[4].value === 0.2
    && rc[1] && rc[1].text === 'NA' && rc[1].textKind === 'word'
    && rc[2] && rc[2].text === '#N/A' && rc[2].textKind === 'error'
    && rc[3] && rc[3].text === '2.5%-3.1%' && rc[3].textKind === 'word'
    && nc.FIGURE === 1 && nc.BLOCK === undefined && nt.sheetBlocks === undefined ? 1 : 0
  console.log(`ay2 d3 range row source ${rng.source}; cells ${JSON.stringify(rc.map((c) => (c ? (c.text !== undefined ? c.text + ':' + c.textKind : c.value) : null)))}; classes ${JSON.stringify(nc)}; sheetBlocks ${nt.sheetBlocks === undefined ? 'absent' : 'present'}; ok ${d3 === 1}`)

  const plain = clone(build(TEAM_CLASSED))
  const pc = plain.teamCensus || {}
  const stripped = clone(plain)
  if (stripped.teamCensus) delete stripped.teamCensus.text
  const baseSnap = fs.existsSync(snap) ? JSON.parse(fs.readFileSync(snap, 'utf8')) : null
  d4 = plain.sheetBlocks === undefined && pc.blocks === undefined && pc.classes && pc.classes.BLOCK === undefined
    && pc.text && pc.text.error === 0 && pc.text.word === 0 && pc.text.empty === 0 && pc.text.unclassed === 0
    && baseSnap && JSON.stringify(stripped) === JSON.stringify(baseSnap.classedOld) ? 1 : 0
  console.log(`ay2 d4 no blocks: sheetBlocks ${plain.sheetBlocks === undefined ? 'absent' : 'present'}; classes ${JSON.stringify(pc.classes)}; text ${JSON.stringify(pc.text)}; equals base except text ${!!baseSnap && JSON.stringify(stripped) === JSON.stringify(baseSnap.classedOld)}; ok ${d4 === 1}`)

  let threw = false
  let inc = null
  try {
    inc = build({ ...TEAM_CLASSED, blocks: [BLOCK_A] })
  } catch (e) {
    threw = true
  }
  const ref = clone(build(TEAM_CLASSED))
  d5 = !threw && inc && Array.isArray(inc.sheetBlocks) && inc.sheetBlocks.length === 1
    && JSON.stringify(clone(inc.groups)) === JSON.stringify(ref.groups) ? 1 : 0
  console.log(`ay2 d5 inconsistent payload: threw ${threw}; sheetBlocks ${inc && inc.sheetBlocks ? inc.sheetBlocks.length : 'absent'}; groups unchanged ${!!inc && JSON.stringify(clone(inc.groups)) === JSON.stringify(ref.groups)}; ok ${d5 === 1}`)

  // d7: an unread block prints no value
  const ub = build(TEAM_UNREAD)
  const us = (ub.sheetBlocks || [])[0] || {}
  const ugroups = JSON.stringify(ub.groups || [])
  const ucl = (ub.teamCensus || {}).classes || {}
  const ubl = (ub.teamCensus || {}).blocks || {}
  const dirty = build(TEAM_UNREAD_DIRTY)
  const ds = (dirty.sheetBlocks || [])[0] || {}
  const noValueOk = JSON.stringify(ub.sheetBlocks || []).match(/"value"|"display"|"text"/) === null
    && !JSON.stringify(dirty.sheetBlocks || []).includes('9999.9876') && !JSON.stringify(dirty.groups || []).includes('9999.9876')
    && (ds.columns || []).length === 0 && (ds.rows || []).every((r) => (r.cells || []).length === 0)
  d7 = (ub.sheetBlocks || []).length === 1 && us.kind === 'unread' && us.why === UNREAD_WHY && us.withheld === 3
    && (us.columns || []).length === 0 && (us.rows || []).length === 1 && us.rows[0].rowNumber === 70 && us.rows[0].blockRow === true
    && (us.rows[0].cells || []).length === 0 && noValueOk
    && !(ub.groups || []).flatMap((g) => g.rows || []).some((r) => r.label === 'Orphan line') && !ugroups.includes('Orphan line')
    && ucl.BLOCK === 1 && ubl.unread && ubl.unread.blocks === 1 && ubl.unread.rows === 1 && ubl.withheld === 3
    && ubl.period.rows === 0 && ubl.case.rows === 0 ? 1 : 0
  console.log(`ay2 d7 unread: kind ${us.kind}; why ${us.why === UNREAD_WHY}; withheld ${us.withheld}; cells ${JSON.stringify(((us.rows || [])[0] || {}).cells)}; no value printed ${noValueOk}; census blocks ${JSON.stringify(ubl)}; ok ${d7 === 1}`)

  // d8: a block headed by text period labels is a period block, carried aligned to its own labels
  const pb = build(TEAM_PERIOD)
  const ps = (pb.sheetBlocks || [])[0] || {}
  const prow = (rn) => (ps.rows || []).find((r) => r.rowNumber === rn) || { cells: [] }
  const labelRow = prow(80).cells
  const revRow = prow(81).cells
  const marRow = prow(82).cells
  const idxD = (ps.columns || []).indexOf('D')
  const pbl = (pb.teamCensus || {}).blocks || {}
  d8 = ps.kind === 'period' && ps.why === null && ps.withheld === 0 && (ps.columns || []).join('') === 'BCDEF'
    && JSON.stringify(labelRow.map((c) => (c ? c.text : null))) === JSON.stringify(['Quarterly', '1Q26', '2Q26', '3Q26', '4Q26'])
    && idxD === 2 && labelRow[idxD].text === '2Q26' && revRow[idxD].display === '1,310.3' && marRow[idxD].display === '21.9%'
    && labelRow.every((c) => c && c.value === undefined)
    && (pb.groups || []).flatMap((g) => g.rows || []).every((r) => r.label !== 'Qtr Revenue' && r.label !== 'Qtr Margin')
    && pbl.period && pbl.period.blocks === 1 && pbl.period.rows === 2 && pbl.case.blocks === 0 && pbl.unread.blocks === 0 ? 1 : 0
  console.log(`ay2 d8 period block: kind ${ps.kind}; labels ${JSON.stringify(labelRow.map((c) => (c ? c.text : null)))}; D column "${labelRow[idxD] && labelRow[idxD].text}" over "${revRow[idxD] && revRow[idxD].display}" and "${marRow[idxD] && marRow[idxD].display}"; census ${JSON.stringify(pbl)}; ok ${d8 === 1}`)
} catch (e) {
  console.log('ay2 build threw: ' + String(e && e.stack).slice(0, 300))
}
try {
  const tab = fs.readFileSync(path.join(portalRoot, 'src', 'pages', 'SecurityAnalysis', 'tabs', 'ModelTab.tsx'), 'utf8')
  d6 = tab.includes('data-sheet-block') && tab.includes('unread') && tab.includes('error in team sheet') && tab.includes('textKind') ? 1 : 0
  console.log(`ay2 d6 ModelTab.tsx: data-sheet-block ${tab.includes('data-sheet-block')}; unread ${tab.includes('unread')}; "error in team sheet" ${tab.includes('error in team sheet')}; textKind ${tab.includes('textKind')}; ok ${d6 === 1}`)
} catch (e) {
  console.log('ay2 d6 threw: ' + String(e && e.message).slice(0, 160))
}
let c1 = 0
let c2 = 0
if (fs.existsSync(snap)) {
  const base = JSON.parse(fs.readFileSync(snap, 'utf8'))
  const got = clone(build(TEAM_CLASSED))
  if (got.teamCensus) delete got.teamCensus.text
  c1 = JSON.stringify(got) === JSON.stringify(base.classedOld) ? 1 : 0
  c2 = JSON.stringify(clone(build(undefined))) === JSON.stringify(base.noTeam) ? 1 : 0
}
console.log(`ay2 build ${d1 + d2 + d3 + d4 + d5 + d6 + d7 + d8}/8 control ${c1 + c2}/2`)
process.exit(d1 + d2 + d3 + d4 + d5 + d6 + d7 + d8 === 8 && c1 + c2 === 2 ? 0 : 1)
