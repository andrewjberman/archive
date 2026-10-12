/**
 * AMGT_CORPUS round 49, CRPS-ay-5 -- FWD-20's last rendered census over every served name: round 47's aw6_rendered_census.cjs moved to the
 * BLOCK class (CTO round-48 ADDENDUM 1: every value under the header of its own block). Issuer's file. READ-ONLY.
 *
 * RUN:  node ay5_rendered_census.cjs <portal root> <capture.json>
 *   <portal root> holds src/pages/SecurityAnalysis/{modelSheet.ts,figureIdentity.ts} AT THE BUILD UNDER READ (portal DEV 46926677c1 or later: CRPS-ay-2);
 *   the capture is aw4_capture.py's output over the LIVE function, or ay5_preread_inject.py's PREDICTION with the stored /15 field in place of `model.team_sheet`.
 *
 * METHOD (as aw6): the REAL modelSheet.ts and figureIdentity.ts are transpiled and run in a vm; per name `buildModelSheet` is called with the arguments
 * ModelTab.tsx passes, the seventh being the served `model.team_sheet`. The sheet builder the page calls on served data, not a browser DOM walk.
 *
 * Prints, per name: class, workbook, rows, FIGURE / HEADING / CONTROL / BLOCK (they must sum to the rows), the first group's rendered rows, the FIGURE rows
 * by source, the blocks by kind. Then the totals:
 *   ay5 classes FIGURE .. HEADING .. CONTROL .. BLOCK .. sum .. of rows ..                        (sum must equal rows)
 *   ay5 BLOCK rows split period p + case c + unread u = b (own .. / master ..) over <rows> rows, <n> blocks, withheld <w>
 *   ay5 values rendered under a header that is not their block's own: <v> (must be 0)               (a numeric body cell with no header-like cell above it in its column, in its block)
 *   ay5 unread blocks: <u> blocks, values printed <p> (must be 0)
 *   ay5 FIGURE by source bloomberg .. team .. why .. refused .. unmapped .. of <f>               (unmapped must be 0)
 *   ay5 text cells error .. word .. empty .. unclassed .. (unclassed must be 0)
 *   ay5 first group has as many rows as the sheet's non-CONTROL non-BLOCK rows on <e> of <m> names
 *   plus aw6's lines: raw field codes, team cells past their format, master names, labels by claim.
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
const IDENT = /^[A-Z][A-Z0-9]*(_[A-Z0-9]+)+$/
const MASTER_WHY = "The research team keeps no workbook for this company; this row is from the team's template."

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
// values under a header that is not their block's own: a numeric BODY cell with no header-like (title / years) cell above it in its column, in its block
function foreignValues(block) {
  if (block.kind === 'unread') return 0
  const headed = new Set()
  let n = 0
  for (const row of block.rows || []) {
    const cells = row.cells || []
    cells.forEach((cell, j) => {
      if (cell && 'value' in cell && row.kind === 'body' && !headed.has(j)) n += 1
    })
    if (row.kind === 'title' || row.kind === 'years') cells.forEach((cell, j) => { if (cell) headed.add(j) })
  }
  return n
}

const names = Object.keys(cap.keys).sort()
const cls = { FIGURE: 0, HEADING: 0, CONTROL: 0, BLOCK: 0 }
let rowsTotal = 0
const src = { bloomberg: 0, team: 0, why: 0, refused: 0, unmapped: 0 }
let headingRows = 0
let controlRendered = 0
let barredWhy = 0
let firstEq = 0
let withTeam = 0
let masterAbsent = 0
let sumBroken = 0
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
const kinds = { period: 0, case: 0, unread: 0 }
const side = { own: { period: 0, case: 0, unread: 0 }, master: { period: 0, case: 0, unread: 0 } }
let blocksTotal = 0
let withheld = 0
let foreign = 0
let unreadBlocks = 0
let unreadValues = 0
const text = { error: 0, word: 0, empty: 0, unclassed: 0 }
let blockRowsInGroup = 0
let rawTokens = 0
let errorWords = 0
let masterCellContent = 0
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
    const c = { FIGURE: 0, HEADING: 0, CONTROL: 0, BLOCK: 0 }
    classes.forEach((x) => { c[x] = (c[x] || 0) + 1 })
    for (const k of Object.keys(cls)) cls[k] += c[k] || 0
    rowsTotal += rows.length
    if (c.FIGURE + c.HEADING + c.CONTROL + c.BLOCK !== rows.length) sumBroken += 1
    const want = rows.filter((_l, i) => classes[i] !== 'CONTROL' && classes[i] !== 'BLOCK')
    if (first.length === want.length) firstEq += 1
    let fb = 0; let ft = 0; let fw = 0; let fr = 0; let fu = 0
    const isMaster = klass === 'master'
    if (isMaster) masterNames += 1
    const lab = (sheet.teamCensus || {}).labels || {}
    labelsBy.held += lab.held || 0; labelsBy.measured += lab.measured || 0
    labelsBy.factset_line += lab.factset_line || 0; labelsBy.bloomberg_line += lab.bloomberg_line || 0
    const tx = (sheet.teamCensus || {}).text || {}
    for (const k of Object.keys(text)) text[k] += tx[k] || 0
    const sb = sheet.sheetBlocks || []
    const kb = { period: 0, case: 0, unread: 0 }
    for (const block of sb) {
      blocksTotal += 1
      withheld += block.withheld || 0
      const nrows = (block.rows || []).filter((r) => r.blockRow).length
      kb[block.kind] += nrows
      kinds[block.kind] += nrows
      side[isMaster ? 'master' : 'own'][block.kind] += nrows
      foreign += foreignValues(block)
      for (const brow of block.rows || []) {
        for (const bcell of brow.cells || []) {
          if (!bcell) continue
          if (isMaster) masterCellContent += 1
          if ('text' in bcell && /^#/.test(String(bcell.text).trim())) { if (bcell.textKind === 'error') errorWords += 1; else rawTokens += 1 }
        }
      }
      if (block.kind === 'unread') {
        unreadBlocks += 1
        unreadValues += (block.rows || []).reduce((a, r) => a + (r.cells || []).filter((x) => x && 'value' in x).length, 0)
      }
    }
    // a BLOCK row must not be a row of the period grid: the first group's rows are the non-CONTROL, non-BLOCK rows only
    blockRowsInGroup += Math.max(0, first.length - want.length)
    for (const r of first) {
      if (isMaster) masterRows += 1
      if (r.rowKind === 'heading') { headingRows += 1; if (IDENT.test(r.label)) rawHeadings += 1; continue }
      if (IDENT.test(r.label)) rawLabels += 1
      if (isMaster && r.source === 'why' && r.absentReason === MASTER_WHY) masterWhyExact += 1
      if (isMaster && r.source === 'bloomberg') masterBloomberg += 1
      if (isMaster && r.source === 'team') masterWithValue += 1
      if (r.source === 'team') {
        for (const cell of r.cells || []) {
          if (!cell || cell.text !== undefined) continue
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
    console.log('ay5 ' + key + ' class ' + klass + ' workbook ' + (t.workbook_key ? path.basename(String(t.workbook_key)) : 'None') + ' rows ' + rows.length +
      ' FIGURE ' + c.FIGURE + ' HEADING ' + c.HEADING + ' CONTROL ' + c.CONTROL + ' BLOCK ' + c.BLOCK + ' rendered ' + first.length +
      ' | bloomberg ' + fb + ' team ' + ft + ' why ' + fw + ' refused ' + fr + ' unmapped ' + fu +
      ' | blocks ' + sb.length + ' period ' + kb.period + ' case ' + kb.case + ' unread ' + kb.unread)
  } else {
    console.log('ay5 ' + key + ' class ' + klass + ' rows ' + rows.length + ' (no row classes served: the page builds the base rows)')
  }
}
const f = cls.FIGURE
const bsum = kinds.period + kinds.case + kinds.unread
console.log('ay5 classes FIGURE ' + cls.FIGURE + ' HEADING ' + cls.HEADING + ' CONTROL ' + cls.CONTROL + ' BLOCK ' + cls.BLOCK + ' sum ' +
  (cls.FIGURE + cls.HEADING + cls.CONTROL + cls.BLOCK) + ' of rows ' + rowsTotal + (sumBroken ? ' SUM-BROKEN on ' + sumBroken + ' names' : ''))
console.log('ay5 BLOCK rows split period ' + kinds.period + ' + case ' + kinds.case + ' + unread ' + kinds.unread + ' = ' + bsum + ' (served BLOCK ' + cls.BLOCK + ') ; own ' +
  JSON.stringify(side.own) + ' master ' + JSON.stringify(side.master) + ' over ' + rowsTotal + ' rows, ' + blocksTotal + ' blocks, withheld ' + withheld)
console.log('ay5 values rendered under a header that is not their block\'s own: ' + foreign + ' (must be 0)')
console.log('ay5 block cells: raw error tokens printed ' + rawTokens + ' (must be 0); error tokens in words ' + errorWords + '; master block cells with content ' + masterCellContent + ' (must be 0)')
console.log('ay5 unread blocks ' + unreadBlocks + ', values printed ' + unreadValues + ' (must be 0); BLOCK rows found in the period grid ' + blockRowsInGroup + ' (must be 0)')
console.log('ay5 FIGURE by source bloomberg ' + src.bloomberg + ' team ' + src.team + ' why ' + src.why + ' refused ' + src.refused + ' unmapped ' + src.unmapped + ' of ' + f +
  ' (sum ' + (src.bloomberg + src.team + src.why + src.refused + src.unmapped) + ')')
console.log('ay5 text cells error ' + text.error + ' word ' + text.word + ' empty ' + text.empty + ' unclassed ' + text.unclassed + ' (unclassed must be 0)')
console.log('ay5 rendered heading rows ' + headingRows + ', control rows rendered ' + controlRendered + ', why-rows with a barred word ' + barredWhy)
console.log('ay5 first group has as many rows as the sheet\'s non-CONTROL non-BLOCK rows on ' + firstEq + ' of ' + withTeam + ' names with team rows')
console.log('ay5 labels by claim (rendered rows) held ' + labelsBy.held + ' measured ' + labelsBy.measured + ' factset_line ' + labelsBy.factset_line + ' bloomberg_line ' + labelsBy.bloomberg_line)
console.log('ay5 raw field codes visible: FIGURE-row labels ' + rawLabels + ', heading labels ' + rawHeadings + ' of ' + f + ' FIGURE rows (must be 0)')
console.log('ay5 team cells ' + teamCells + ', printed past 4 decimals ' + teamBeyond4 + ' (must be 0); percent-format cells ' + pctCells + ', printed as a percent ' + pctPrinted)
console.log('ay5 master names ' + masterNames + ', rendered rows ' + masterRows + ': Bloomberg ' + masterBloomberg + ', the template why ' + masterWhyExact + ', team value ' + masterWithValue + ' (must be 0)')
console.log('ay5 names with row classes served ' + withTeam + ' of ' + names.length + ' served; master_absent ' + masterAbsent)
