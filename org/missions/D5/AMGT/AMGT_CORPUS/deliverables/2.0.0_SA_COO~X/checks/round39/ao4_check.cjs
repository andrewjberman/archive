/**
 * AMGT_CORPUS round 39, CRPS-ao-4 -- FWD-21: the Model sheet fits FY+3 at 1440 px, history byte-unchanged (round-38 analysis
 * ruling 5). Issuer's file. The fit itself is graded on the issuer's real 1440 px walk (the cell's judgment criterion); this
 * file is the CONTROL: the fit must not move a figure.
 *
 * RUN:  node ao4_check.cjs [<portal root>] [--snapshot]   (default: <git toplevel>/portal)
 * The REAL `modelSheet.ts` is transpiled and called on round 39's `ao_fixture.json` (TSM, BA, ASML), history only and with the
 * forecasts. Prints `ao4 control <q>/2`:
 *   c1  the history-only sheet (years, every row's label and figure values) is unchanged against ao4_base_snapshot.json;
 *   c2  the full sheet's year columns (history + 2026E..2028E) and every forecast cell value are unchanged likewise.
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
  } catch (e) { /* optional */ }
  for (const root of roots) {
    try { return createRequire(path.join(root, 'package.json'))('typescript') } catch (e) { /* next */ }
  }
  throw new Error('typescript not resolvable from ' + roots.join(' or '))
}
const ts = loadTypescript()
const src = fs.readFileSync(path.join(portalRoot, 'src', 'pages', 'SecurityAnalysis', 'modelSheet.ts'), 'utf8')
const out = ts.transpileModule(src, { compilerOptions: { module: ts.ModuleKind.CommonJS, target: ts.ScriptTarget.ES2020 } }).outputText
const mod = { exports: {} }
vm.runInNewContext(out, { module: mod, exports: mod.exports, require: () => ({}), console })
const sheetMod = mod.exports

const fixture = JSON.parse(fs.readFileSync(path.join(HERE, 'ao_fixture.json'), 'utf8'))
const NAMES = ['TSM_US_Equity', 'BA_US_Equity', 'ASML_NA_Equity']
const shape = (sheet) => ({
  years: sheet.years,
  rows: sheet.groups.map((g) => g.rows.map((r) => [r.label, r.cells.map((c) => (c === null ? null : c.value))])),
})
const now = {}
for (const key of NAMES) {
  const f = fixture[key]
  now[key] = {
    history: shape(sheetMod.buildModelSheet(f.fiscal_year_figures, f.fiscal_years, null)),
    full: shape(sheetMod.buildModelSheet(f.fiscal_year_figures, f.fiscal_years, null, f.forecast_figures, f.fiscal_unresolved,
      f.header_figures)),
  }
}
const snapPath = path.join(HERE, 'ao4_base_snapshot.json')
if (snapshot) {
  fs.writeFileSync(snapPath, JSON.stringify(now, null, 1) + '\n')
  console.log('SNAPSHOT written from ' + portalRoot)
  process.exit(0)
}
const base = JSON.parse(fs.readFileSync(snapPath, 'utf8'))
const c1diff = NAMES.filter((key) => JSON.stringify(now[key].history) !== JSON.stringify(base[key].history))
const c2diff = NAMES.filter((key) => JSON.stringify(now[key].full) !== JSON.stringify(base[key].full))
console.log(`ARM c1 ${c1diff.length === 0 ? 'PASS' : 'FAIL'} history sheet changed on ${JSON.stringify(c1diff)}`)
console.log(`ARM c2 ${c2diff.length === 0 ? 'PASS' : 'FAIL'} full sheet changed on ${JSON.stringify(c2diff)}`)
console.log(`ao4 control ${(c1diff.length === 0 ? 1 : 0) + (c2diff.length === 0 ? 1 : 0)}/2`)
