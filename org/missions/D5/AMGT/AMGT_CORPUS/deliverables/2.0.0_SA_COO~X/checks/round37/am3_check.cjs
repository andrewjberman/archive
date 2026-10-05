/**
 * AMGT_CORPUS round 37, CRPS-am-3 -- the Model sheet says why a gap inside a showing row is empty, and names each money row's
 * currency. Issuer's file.
 *
 * RUN:  node am3_check.cjs [<portal root>] [--snapshot]   (default: <git toplevel>/portal)
 * The REAL `modelSheet.ts` of that portal root is transpiled with the installed typescript and called on `am3_fixture.json`
 * (captured from the real read path at the cut: TSM_US_Equity, 1299_HK_Equity):
 *   buildModelSheet(fiscal_year_figures, fiscal_years, null, forecast_figures, fiscal_unresolved, header_figures)
 * The contract (round-37 decomposition): every ModelSheetRow carries
 *   cellReasons: (string | null)[]  -- aligned with `cells`; a PM-words reason where the cell is empty and the served
 *                                      fiscal_unresolved names that (mnemonic, year); null otherwise
 *   currency:    string | null      -- the one currency every money figure of the row carries; null when none carries one
 * Prints one line per arm, then `am3 build <p>/2 control <q>/2`.
 *   b1  1299 HK: every GAP cell (empty, in a row with >= 1 figure, in a history year, with a served reason for that
 *       mnemonic and year) carries a non-empty cellReasons entry in words (none of ABSENT / REFUSED / "not read" /
 *       "mnemonic" / fye_join / HELD_OFF / an UPPER_SNAKE token); the gap count must be > 0.
 *   b2  TSM: every money row (a figure unit beginning MILLIONS, ABSOLUTE or PER SHARE, never a "(share count)" unit -- amended 2026-10-05, row Z-W1-S33)
 *       whose figures all carry ONE currency C exposes currency === C; a money row whose figures carry none exposes null.
 *       At least one row must carry a currency, so the arm discriminates.
 *   c1  the first two groups (17 rows) and the V3 group's row list are unchanged against am3_base_snapshot.json.
 *   c2  round 36's al2_check.cjs on the same portal root still reads `al2 build 3/3 control 1/1`.
 */
const fs = require('fs')
const path = require('path')
const vm = require('vm')
const { execSync, spawnSync } = require('child_process')
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
  } catch (e) { /* optional */ }
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

const fixture = JSON.parse(fs.readFileSync(path.join(HERE, 'am3_fixture.json'), 'utf8'))
const INTERNAL = /ABSENT|REFUSED|not read|mnemonic|fye_join|HELD_OFF|\b[A-Z][A-Z0-9]*_[A-Z0-9_]+\b/
const isMoney = (u) => {
  const s = String(u || '')
  if (s.includes('(share count)')) return false
  return s.startsWith('MILLIONS') || s.startsWith('ABSOLUTE') || s.startsWith('PER SHARE')
}

function build(key) {
  const f = fixture[key]
  return sheetMod.buildModelSheet(f.fiscal_year_figures, f.fiscal_years, null, f.forecast_figures, f.fiscal_unresolved,
    f.header_figures)
}
const sheets = { TSM_US_Equity: build('TSM_US_Equity'), '1299_HK_Equity': build('1299_HK_Equity') }
const shape = (sheet) => sheet.groups.map((g, gi) => ({
  title: g.title,
  rows: g.rows.map((r) => (gi < 2 ? { label: r.label, mnemonic: r.mnemonic, figures: r.cells.filter((c) => c !== null).length }
    : { mnemonic: r.mnemonic })),
}))

if (snapshot) {
  const snap = { TSM_US_Equity: shape(sheets.TSM_US_Equity), '1299_HK_Equity': shape(sheets['1299_HK_Equity']) }
  fs.writeFileSync(path.join(HERE, 'am3_base_snapshot.json'), JSON.stringify(snap, null, 1) + '\n')
  console.log('SNAPSHOT written from ' + srcPath)
  process.exit(0)
}

// b1
const hk = sheets['1299_HK_Equity']
const hkFix = fixture['1299_HK_Equity']
const served = new Set(hkFix.fiscal_unresolved.map((u) => `${u.mnemonic}|${String(u.fiscal_year)}`))
const history = new Set((hkFix.fiscal_years || []).map(String))
let gaps = 0
let reasoned = 0
const badSamples = []
for (const g of hk.groups) {
  for (const r of g.rows) {
    if (!r.mnemonic || r.cells.every((c) => c === null)) continue
    hk.years.forEach((y, i) => {
      if (r.cells[i] !== null || !history.has(String(y)) || !served.has(`${r.mnemonic}|${y}`)) return
      gaps += 1
      const why = Array.isArray(r.cellReasons) ? r.cellReasons[i] : undefined
      if (typeof why === 'string' && why.trim() && !INTERNAL.test(why)) reasoned += 1
      else if (badSamples.length < 3) badSamples.push(`${r.mnemonic} ${y}: ${JSON.stringify(why)}`)
    })
  }
}
const b1 = gaps > 0 && reasoned === gaps
console.log(`ARM b1 ${b1 ? 'PASS' : 'FAIL'} 1299_HK gap cells ${gaps}, reasoned in words ${reasoned} ${JSON.stringify(badSamples)}`)

// b2
const tsm = sheets.TSM_US_Equity
let moneyRows = 0
let withCcy = 0
let wrong = 0
const wrongSamples = []
for (const g of tsm.groups) {
  for (const r of g.rows) {
    const figs = r.cells.filter((c) => c !== null)
    if (!figs.some((c) => isMoney(c.unit))) continue
    moneyRows += 1
    const ccys = new Set(figs.map((c) => (typeof c.currency === 'string' && c.currency.trim() ? c.currency : null)))
    const want = ccys.size === 1 ? Array.from(ccys)[0] : (ccys.has(null) && ccys.size > 1 ? undefined : null)
    if (want === undefined) continue // mixed labelled / unlabelled within one row: not graded here
    if (want) withCcy += 1
    if (r.currency !== want) {
      wrong += 1
      if (wrongSamples.length < 3) wrongSamples.push(`${r.mnemonic}: want ${want} got ${JSON.stringify(r.currency)}`)
    }
  }
}
const b2 = moneyRows > 0 && withCcy > 0 && wrong === 0
console.log(`ARM b2 ${b2 ? 'PASS' : 'FAIL'} TSM money rows ${moneyRows}, carrying a currency ${withCcy}, wrong ${wrong} ${JSON.stringify(wrongSamples)}`)

// c1
const snap = JSON.parse(fs.readFileSync(path.join(HERE, 'am3_base_snapshot.json'), 'utf8'))
let c1 = true
const c1Notes = []
for (const key of Object.keys(sheets)) {
  const same = JSON.stringify(shape(sheets[key])) === JSON.stringify(snap[key])
  if (!same) c1 = false
  c1Notes.push(`${key} ${same ? 'unchanged' : 'MOVED'}`)
}
console.log(`ARM c1 ${c1 ? 'PASS' : 'FAIL'} ${JSON.stringify(c1Notes)}`)

// c2
const al2 = spawnSync(process.execPath, [path.join(HERE, '..', 'round36', 'al2_check.cjs'), portalRoot], { encoding: 'utf8' })
const al2Line = String(al2.stdout || '').trim().split('\n').pop()
const c2 = al2Line === 'al2 build 3/3 control 1/1'
console.log(`ARM c2 ${c2 ? 'PASS' : 'FAIL'} round36 al2_check: ${al2Line}`)

console.log(`am3 build ${[b1, b2].filter(Boolean).length}/2 control ${[c1, c2].filter(Boolean).length}/2`)
