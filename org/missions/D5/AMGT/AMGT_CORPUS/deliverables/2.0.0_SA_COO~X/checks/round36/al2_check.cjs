/**
 * AMGT_CORPUS round 36, CRPS-al-2 -- the Model sheet carries the V3 rows. Issuer's file.
 *
 * RUN:  node al2_check.cjs [<portal root>]   (default: <git toplevel>/portal)
 * The REAL `modelSheet.ts` of that portal root is transpiled with the installed typescript (resolved from that root, else
 * from the shared checkout's portal) and called on `al2_fixture.json`, which was captured from the real read path at the
 * cut (BA_US_Equity, 1299_HK_Equity):
 *   buildModelSheet(fiscal_year_figures, fiscal_years, null, forecast_figures, fiscal_unresolved, header_figures)
 * Prints one line per arm, then `al2 build <p>/3 control <q>/1`.
 *   b1  the group titled V3_LINES_TITLE holds exactly one row for each of the 45 V3 sheet mnemonics (44 fiscal + BEST_CPS),
 *       on both names.
 *   b2  every V3 row with no figure in any column carries a non-empty `absentReason`, and every V3 row reason reads as words:
 *       none of ABSENT / REFUSED / "not read" / "mnemonic" / fye_join / HELD_OFF / an UPPER_SNAKE token. 1299 HK must
 *       have at least one such row (it has whole rows unresolved at the fiscal period end), so the arm discriminates.
 *   b3  `v3Facts` lists the 4 V3 header facts (SHORT_NAME, COUNTRY_FULL_NAME, AVG_DAILY_VALUE_TRADED_3M,
 *       CRNCY_ADJ_MKT_CAP), each with a non-empty label in words and the header figure's served value, on BA.
 *   c1  the 17 rows of the two existing groups are unchanged: same titles, labels, mnemonics and per-row figure counts as
 *       `al2_base_snapshot.json` (written by `--snapshot` at the cut, on the base).
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
const portalRoot = path.resolve(args.find((a) => !a.startsWith('--')) || path.join(top, 'portal'))

function loadTypescript() {
  const roots = [portalRoot]
  try {
    const common = execSync('git rev-parse --path-format=absolute --git-common-dir', { encoding: 'utf8', cwd: top }).trim()
    roots.push(path.join(path.dirname(common), 'portal'))
  } catch (e) { /* the shared checkout is optional */ }
  for (const root of roots) {
    try { return createRequire(path.join(root, 'package.json'))('typescript') } catch (e) { /* next */ }
  }
  throw new Error('typescript not resolvable from ' + roots.join(' or '))
}

const ts = loadTypescript()
const srcPath = path.join(portalRoot, 'src', 'pages', 'SecurityAnalysis', 'modelSheet.ts')
const out = ts.transpileModule(fs.readFileSync(srcPath, 'utf8'), {
  compilerOptions: { module: ts.ModuleKind.CommonJS, target: ts.ScriptTarget.ES2020 },
}).outputText
const mod = { exports: {} }
vm.runInNewContext(out, { module: mod, exports: mod.exports, require: () => ({}), console })
const sheetMod = mod.exports

const fixture = JSON.parse(fs.readFileSync(path.join(HERE, 'al2_fixture.json'), 'utf8'))
const V3_FISCAL = ['ARD_GOODWLL', 'ARD_OTHER_INTANGIBLE_ASSET', 'ARD_SHARES_OUTSTANDING', 'ARD_TOTAL_CURRENT_LIABILITIES',
  'ARD_TOT_ASSETS', 'AVERAGE_DIVIDEND_YIELD', 'AVERAGE_EV_TO_T12M_EBIT', 'AVERAGE_EV_TO_T12M_SALES',
  'AVERAGE_PRICE_EARNINGS_RATIO', 'AVERAGE_PRICE_TO_BOOK_RATIO', 'AVERAGE_PRICE_TO_FREE_CASH_FLOW', 'AVG_EV_TO_T12M_EBITDA',
  'CAPEX_ABSOLUTE_VALUE', 'CASH_AND_MARKETABLE_SECURITIES', 'CF_CASH_FROM_OPER', 'DIVIDEND_YIELD', 'EARN_FOR_COMMON',
  'EQY_FUND_YEAR', 'EV_TO_T12M_EBIT', 'EV_TO_T12M_EBITDA', 'EV_TO_T12M_SALES', 'FCF_MARGIN_AFTER_OPER_LEA_PYMT',
  'FREE_CASH_FLOW_PER_SH', 'HIGH_CLOSING_PRICE_TO_BOOK_RATIO', 'HIGH_DIVIDEND_YIELD', 'HIGH_EV_TO_T12M_EBIT',
  'HIGH_EV_TO_T12M_EBITDA', 'HIGH_EV_TO_T12M_SALES', 'HIGH_PRICE_TO_FREE_CASH_FLOW', 'HISTORICAL_MARKET_CAP',
  'LOW_CLOSING_PRICE_TO_BOOK_RATIO', 'LOW_DIVIDEND_YIELD', 'LOW_EV_TO_T12M_EBIT', 'LOW_EV_TO_T12M_EBITDA',
  'LOW_EV_TO_T12M_SALES', 'LOW_PRICE_TO_FREE_CASH_FLOW', 'MINORITY_NONCONTROLLING_INTEREST', 'NORMALIZED_ROA',
  'NORMALIZED_ROE', 'PX_ERN_RATIO_WITH_HIGH_CLOS_PX', 'PX_ERN_RATIO_WITH_LOW_CLOS_PX', 'SHORT_AND_LONG_TERM_DEBT',
  'TANG_BOOK_VAL_PER_SH', 'TOTAL_EQUITY']
const V3_SHEET = V3_FISCAL.concat(['BEST_CPS'])
const V3_HEADER = ['SHORT_NAME', 'COUNTRY_FULL_NAME', 'AVG_DAILY_VALUE_TRADED_3M', 'CRNCY_ADJ_MKT_CAP']
const INTERNAL = /ABSENT|REFUSED|not read|mnemonic|fye_join|HELD_OFF|\b[A-Z][A-Z0-9]*_[A-Z0-9_]+\b/

function build(key) {
  const f = fixture[key]
  return sheetMod.buildModelSheet(f.fiscal_year_figures, f.fiscal_years, null, f.forecast_figures, f.fiscal_unresolved,
    f.header_figures)
}

const sheets = { BA_US_Equity: build('BA_US_Equity'), '1299_HK_Equity': build('1299_HK_Equity') }
const baseGroups = (sheet) => sheet.groups.slice(0, 2).map((g) => ({
  title: g.title,
  rows: g.rows.map((r) => ({ label: r.label, mnemonic: r.mnemonic, figures: r.cells.filter((c) => c !== null).length })),
}))

if (snapshot) {
  const snap = { BA_US_Equity: baseGroups(sheets.BA_US_Equity), '1299_HK_Equity': baseGroups(sheets['1299_HK_Equity']) }
  fs.writeFileSync(path.join(HERE, 'al2_base_snapshot.json'), JSON.stringify(snap, null, 1) + '\n')
  console.log('SNAPSHOT written from ' + srcPath)
  process.exit(0)
}

const v3Title = sheetMod.V3_LINES_TITLE
const v3Group = (sheet) => (v3Title ? sheet.groups.find((g) => g.title === v3Title) : undefined)

// b1
let b1 = true
const b1Notes = []
for (const [key, sheet] of Object.entries(sheets)) {
  const g = v3Group(sheet)
  const rows = g ? g.rows : []
  const counts = {}
  for (const r of rows) counts[r.mnemonic] = (counts[r.mnemonic] || 0) + 1
  const once = V3_SHEET.filter((m) => counts[m] === 1).length
  const extra = rows.filter((r) => !V3_SHEET.includes(r.mnemonic)).length
  if (once !== V3_SHEET.length || extra !== 0) b1 = false
  b1Notes.push(`${key} once ${once}/${V3_SHEET.length} extra ${extra}`)
}
console.log(`ARM b1 ${b1 ? 'PASS' : 'FAIL'} ${JSON.stringify(b1Notes)}`)

// b2
let b2 = true
const b2Notes = []
for (const [key, sheet] of Object.entries(sheets)) {
  const g = v3Group(sheet)
  const rows = g ? g.rows : []
  const empty = rows.filter((r) => r.cells.every((c) => c === null))
  const unreasoned = empty.filter((r) => !(typeof r.absentReason === 'string' && r.absentReason.trim()))
  const internal = rows.filter((r) => typeof r.absentReason === 'string' && INTERNAL.test(r.absentReason))
  if (rows.length === 0 || unreasoned.length || internal.length) b2 = false
  if (key === '1299_HK_Equity' && empty.length === 0) b2 = false
  b2Notes.push(`${key} rows ${rows.length} empty ${empty.length} unreasoned ${unreasoned.length} internal_words ${internal.length}` +
    (internal.length ? ` e.g. "${internal[0].absentReason}"` : ''))
}
console.log(`ARM b2 ${b2 ? 'PASS' : 'FAIL'} ${JSON.stringify(b2Notes)}`)

// b3
const ba = sheets.BA_US_Equity
const facts = Array.isArray(ba.v3Facts) ? ba.v3Facts : []
const header = fixture.BA_US_Equity.header_figures
let b3 = true
const b3Notes = []
for (const m of V3_HEADER) {
  const fact = facts.find((x) => x && x.mnemonic === m)
  const served = header.find((x) => x.mnemonic === m)
  const ok = !!fact && typeof fact.label === 'string' && fact.label.trim() && !INTERNAL.test(fact.label) &&
    !!served && JSON.stringify(fact.value) === JSON.stringify(served.value)
  if (!ok) b3 = false
  b3Notes.push(`${m} ${ok ? 'ok' : 'missing'}`)
}
console.log(`ARM b3 ${b3 ? 'PASS' : 'FAIL'} ${JSON.stringify(b3Notes)}`)

// c1
const snap = JSON.parse(fs.readFileSync(path.join(HERE, 'al2_base_snapshot.json'), 'utf8'))
let c1 = true
const c1Notes = []
for (const key of Object.keys(sheets)) {
  const same = JSON.stringify(baseGroups(sheets[key])) === JSON.stringify(snap[key])
  if (!same) c1 = false
  c1Notes.push(`${key} ${same ? 'unchanged' : 'MOVED'}`)
}
console.log(`ARM c1 ${c1 ? 'PASS' : 'FAIL'} ${JSON.stringify(c1Notes)}`)
console.log(`al2 build ${[b1, b2, b3].filter(Boolean).length}/3 control ${c1 ? 1 : 0}/1`)
