/**
 * AMGT_CORPUS round 39, CRPS-ao-3 -- FWD-20's three page defects (round-38 analysis rulings 2-4). Issuer's file.
 *
 * RUN:  node ao3_check.cjs <arm> [<portal root>]      arm = currency | marks | words   (portal root default: <git toplevel>/portal)
 * The REAL `modelSheet.ts` and `components/StatTile.tsx` of that portal root are transpiled with the installed typescript and
 * called on `ao_fixture.json` (captured from the real read path at the cut: TSM_US_Equity, BA_US_Equity, ASML_NA_Equity):
 *   buildModelSheet(fiscal_year_figures, fiscal_years, null, forecast_figures, fiscal_unresolved, header_figures)
 *   formatStatValue(value, format, currency, unit, currencyBasis)
 * Each arm prints its lines, then ONE verdict line `ao3 <arm> build <p>/1 control <q>/1`.
 *
 *   currency  build:   every V3 header fact whose served header figure carries a currency exposes `currency` equal to it
 *                      (TSM CRNCY_ADJ_MKT_CAP USD, AVG_DAILY_VALUE_TRADED_3M USD; BA and ASML likewise); >= 1 graded.
 *             control: the V3 fact list (mnemonic, label, value) is unchanged against ao3_base_snapshot.json.
 *   marks     build:   TSM: every empty cell inside a row that shows >= 1 figure carries a cellReasons entry in words
 *                      (non-empty; no ABSENT / REFUSED / UNMEASURED / UNRESOLVED / "mnemonic" / UPPER_SNAKE token); > 0 gaps.
 *             control: the figure cells of every row on all three names are unchanged against ao3_base_snapshot.json.
 *   words     build:   TSM enterprise value (unit UNRESOLVED..., basis UNMEASURED...) and TSM net debt (basis UNMEASURED...)
 *                      formatted as the header tile formats them: no raw figure (no run of the value's integer digits, no
 *                      "raw figure"), no machine token (UNMEASURED / UNRESOLVED / CRPS- / census / UPPER_SNAKE); non-empty.
 *             control: BA enterprise value and net debt (resolved unit, USD) format exactly as at the base snapshot.
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
const positional = args.filter((a) => !a.startsWith('--'))
const arm = positional[0]
const portalRoot = path.resolve(positional[1] || path.join(top, 'portal'))
if (!snapshot && !['currency', 'marks', 'words'].includes(arm)) {
  console.log('usage: node ao3_check.cjs currency|marks|words [<portal root>]')
  process.exit(2)
}

function loadTypescript() {
  const roots = [portalRoot]
  try {
    const common = execSync('git rev-parse --path-format=absolute --git-common-dir', { encoding: 'utf8', cwd: top }).trim()
    roots.push(path.join(path.dirname(common), 'portal'))
  } catch (e) { /* optional */ }
  for (const root of roots) {
    try { return createRequire(path.join(root, 'package.json'))('typescript') } catch (e) { /* next */ }
  }
  throw new Error('typescript not resolvable from ' + roots.join(' or '))
}
const ts = loadTypescript()

function load(rel) {
  const src = fs.readFileSync(path.join(portalRoot, 'src', 'pages', 'SecurityAnalysis', rel), 'utf8')
  const out = ts.transpileModule(src, {
    compilerOptions: { module: ts.ModuleKind.CommonJS, target: ts.ScriptTarget.ES2020, jsx: ts.JsxEmit.React },
    fileName: rel,
  }).outputText
  const mod = { exports: {} }
  const stub = new Proxy(function () { return null }, { get: (t, k) => (k === '__esModule' ? true : stub) })
  vm.runInNewContext(out, { module: mod, exports: mod.exports, require: () => stub, console })
  return mod.exports
}
const sheetMod = load('modelSheet.ts')
const tileMod = load(path.join('components', 'StatTile.tsx'))

const fixture = JSON.parse(fs.readFileSync(path.join(HERE, 'ao_fixture.json'), 'utf8'))
const NAMES = ['TSM_US_Equity', 'BA_US_Equity', 'ASML_NA_Equity']
const sheets = {}
for (const key of NAMES) {
  const f = fixture[key]
  sheets[key] = sheetMod.buildModelSheet(f.fiscal_year_figures, f.fiscal_years, null, f.forecast_figures, f.fiscal_unresolved,
    f.header_figures)
}
const header = (key, mnemonic) => fixture[key].header_figures.find((h) => h && h.mnemonic === mnemonic)
const fmt = (key, mnemonic) => {
  const h = header(key, mnemonic)
  return tileMod.formatStatValue(h.value, 'currency-millions', h.currency ?? null, h.unit ?? null, h.currency_basis ?? null)
}
const factShape = (sheet) => sheet.v3Facts.map((f) => ({ mnemonic: f.mnemonic, label: f.label, value: f.value }))
const cellShape = (sheet) => sheet.groups.map((g) => g.rows.map((r) => r.cells.map((c) => (c === null ? null : c.value))))
const INTERNAL = /ABSENT|REFUSED|UNMEASURED|UNRESOLVED|not read|mnemonic|CRPS-|census|\b[A-Z][A-Z0-9]*_[A-Z0-9_]+\b/

const snapPath = path.join(HERE, 'ao3_base_snapshot.json')
if (snapshot) {
  const snap = {}
  for (const key of NAMES) snap[key] = { facts: factShape(sheets[key]), cells: cellShape(sheets[key]) }
  snap.words = { BA_EV: fmt('BA_US_Equity', 'CURR_ENTP_VAL'), BA_ND: fmt('BA_US_Equity', 'NET_DEBT') }
  fs.writeFileSync(snapPath, JSON.stringify(snap, null, 1) + '\n')
  console.log('SNAPSHOT written from ' + portalRoot)
  process.exit(0)
}
const base = JSON.parse(fs.readFileSync(snapPath, 'utf8'))
let build = false
let control = false

if (arm === 'currency') {
  let graded = 0
  let right = 0
  const bad = []
  for (const key of NAMES) {
    for (const fact of sheets[key].v3Facts) {
      const h = header(key, fact.mnemonic)
      if (!h || typeof h.currency !== 'string' || !h.currency.trim()) continue
      graded += 1
      if (fact.currency === h.currency) right += 1
      else if (bad.length < 4) bad.push(`${key} ${fact.mnemonic}: ${JSON.stringify(fact.currency)} want ${h.currency}`)
    }
  }
  build = graded > 0 && right === graded
  console.log(`ARM currency-build ${build ? 'PASS' : 'FAIL'} facts with a served currency ${graded}, carrying it ${right} ${JSON.stringify(bad)}`)
  const diff = NAMES.filter((key) => JSON.stringify(factShape(sheets[key])) !== JSON.stringify(base[key].facts))
  control = diff.length === 0
  console.log(`ARM currency-control ${control ? 'PASS' : 'FAIL'} fact list changed on ${JSON.stringify(diff)}`)
}

if (arm === 'marks') {
  const s = sheets.TSM_US_Equity
  let gaps = 0
  let reasoned = 0
  const bad = []
  for (const g of s.groups) {
    for (const r of g.rows) {
      if (!r.mnemonic || r.cells.every((c) => c === null)) continue
      r.cells.forEach((c, i) => {
        if (c !== null) return
        gaps += 1
        const why = Array.isArray(r.cellReasons) ? r.cellReasons[i] : undefined
        if (typeof why === 'string' && why.trim() && !INTERNAL.test(why)) reasoned += 1
        else if (bad.length < 4) bad.push(`${r.mnemonic} ${s.years[i]}: ${JSON.stringify(why)}`)
      })
    }
  }
  build = gaps > 0 && reasoned === gaps
  console.log(`ARM marks-build ${build ? 'PASS' : 'FAIL'} TSM gap cells in showing rows ${gaps}, reasoned in words ${reasoned} ${JSON.stringify(bad)}`)
  const diff = NAMES.filter((key) => JSON.stringify(cellShape(sheets[key])) !== JSON.stringify(base[key].cells))
  control = diff.length === 0
  console.log(`ARM marks-control ${control ? 'PASS' : 'FAIL'} figure cells changed on ${JSON.stringify(diff)}`)
}

if (arm === 'words') {
  const cases = [
    ['TSM enterprise value', fmt('TSM_US_Equity', 'CURR_ENTP_VAL'), header('TSM_US_Equity', 'CURR_ENTP_VAL').value],
    ['TSM net debt', fmt('TSM_US_Equity', 'NET_DEBT'), header('TSM_US_Equity', 'NET_DEBT').value],
  ]
  let ok = 0
  for (const [label, text, value] of cases) {
    const digits = String(Math.trunc(Math.abs(Number(value))))
    const grouped = Math.trunc(Math.abs(Number(value))).toLocaleString('en-US')
    const isUnresolved = label.includes('enterprise')
    const rawShown = isUnresolved && (String(text).includes(digits) || String(text).includes(grouped) || /raw figure/i.test(String(text)))
    const pass = typeof text === 'string' && text.trim() !== '' && !rawShown && !INTERNAL.test(text)
    if (pass) ok += 1
    console.log(`  ${label}: ${pass ? 'OK' : 'BAD'} ${JSON.stringify(text)}`)
  }
  build = ok === cases.length
  console.log(`ARM words-build ${build ? 'PASS' : 'FAIL'} ${ok} of ${cases.length} in words with no raw figure`)
  const now = { BA_EV: fmt('BA_US_Equity', 'CURR_ENTP_VAL'), BA_ND: fmt('BA_US_Equity', 'NET_DEBT') }
  control = now.BA_EV === base.words.BA_EV && now.BA_ND === base.words.BA_ND
  console.log(`ARM words-control ${control ? 'PASS' : 'FAIL'} BA ${JSON.stringify(now)} base ${JSON.stringify(base.words)}`)
}

console.log(`ao3 ${arm} build ${build ? 1 : 0}/1 control ${control ? 1 : 0}/1`)
