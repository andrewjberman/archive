/**
 * AMGT_CORPUS round 39, CRPS-ao-7 (amendment v39.1) -- a header money figure whose currency basis is UNMEASURED shows NO
 * number (CTO render review of portal e1ee93a9, msg 30286: the Net debt tile read "-2.00T (currency not confirmed by
 * Bloomberg)" beside "USD 2.52T"). Issuer's file.
 *
 * RUN:  node ao7_check.cjs [<portal root>]      (default: <git toplevel>/portal)
 * The REAL `components/StatTile.tsx` of that portal root is transpiled and `formatStatValue(value, format, currency, unit,
 * currencyBasis)` is called on round 39's `ao_fixture.json` header figures (TSM, BA, ASML). Prints `ao7 build <p>/1 control <q>/1`.
 *   build    every header MONEY figure (unit beginning MILLIONS, ABSOLUTE or PER SHARE and not a share count, or an
 *            UNRESOLVED unit) whose `currency_basis` begins "UNMEASURED", formatted as 'currency-millions' AND as
 *            'currency-abs': the text is non-empty, carries NO digit, and carries no machine token (UNMEASURED / UNRESOLVED /
 *            CRPS- / census / UPPER_SNAKE). At least one such figure must exist (TSM net debt and enterprise value at the cut).
 *   control  every header money figure with a served currency and a resolved unit formats exactly as in ao7_base_snapshot.json
 *            (written from the portal root with --snapshot at the cut).
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
const src = fs.readFileSync(path.join(portalRoot, 'src', 'pages', 'SecurityAnalysis', 'components', 'StatTile.tsx'), 'utf8')
const out = ts.transpileModule(src, {
  compilerOptions: { module: ts.ModuleKind.CommonJS, target: ts.ScriptTarget.ES2020, jsx: ts.JsxEmit.React },
  fileName: 'StatTile.tsx',
}).outputText
const mod = { exports: {} }
const stub = new Proxy(function () { return null }, { get: (t, k) => (k === '__esModule' ? true : stub) })
vm.runInNewContext(out, { module: mod, exports: mod.exports, require: () => stub, console })
const fmt = mod.exports.formatStatValue

const fixture = JSON.parse(fs.readFileSync(path.join(HERE, 'ao_fixture.json'), 'utf8'))
const NAMES = ['TSM_US_Equity', 'BA_US_Equity', 'ASML_NA_Equity']
const FORMATS = ['currency-millions', 'currency-abs']
const INTERNAL = /UNMEASURED|UNRESOLVED|CRPS-|census|\b[A-Z][A-Z0-9]*_[A-Z0-9_]+\b/
const isMoney = (u) => {
  const s = String(u || '')
  if (s.includes('(share count)')) return false
  return s.startsWith('MILLIONS') || s.startsWith('ABSOLUTE') || s.startsWith('PER SHARE') || s.startsWith('UNRESOLVED')
}
const numeric = (v) => typeof v === 'number' && Number.isFinite(v)

const unmeasured = []
const resolved = {}
for (const key of NAMES) {
  for (const h of fixture[key].header_figures) {
    if (!h || !numeric(h.value) || !isMoney(h.unit)) continue
    const basis = String(h.currency_basis || '')
    if (basis.startsWith('UNMEASURED')) unmeasured.push([key, h])
    else if (typeof h.currency === 'string' && h.currency.trim() && !String(h.unit).startsWith('UNRESOLVED')) {
      for (const f of FORMATS) resolved[`${key}|${h.mnemonic}|${f}`] = fmt(h.value, f, h.currency, h.unit, h.currency_basis ?? null)
    }
  }
}
const snapPath = path.join(HERE, 'ao7_base_snapshot.json')
if (snapshot) {
  fs.writeFileSync(snapPath, JSON.stringify(resolved, null, 1) + '\n')
  console.log('SNAPSHOT written from ' + portalRoot + ' (' + Object.keys(resolved).length + ' rows)')
  process.exit(0)
}

let ok = 0
let graded = 0
const bad = []
for (const [key, h] of unmeasured) {
  for (const f of FORMATS) {
    graded += 1
    const text = fmt(h.value, f, h.currency ?? null, h.unit ?? null, h.currency_basis ?? null)
    const pass = typeof text === 'string' && text.trim() !== '' && !/[0-9]/.test(text) && !INTERNAL.test(text)
    if (pass) ok += 1
    else if (bad.length < 4) bad.push(`${key} ${h.mnemonic} ${f}: ${JSON.stringify(text)}`)
  }
}
const build = unmeasured.length > 0 && ok === graded
console.log(`ARM build ${build ? 'PASS' : 'FAIL'} UNMEASURED-basis header money figures ${unmeasured.length}, renders ${graded}, with no number ${ok} ${JSON.stringify(bad)}`)

const base = JSON.parse(fs.readFileSync(snapPath, 'utf8'))
const keys = Object.keys(base)
const moved = keys.filter((k) => resolved[k] !== base[k])
const control = keys.length > 0 && moved.length === 0 && Object.keys(resolved).length === keys.length
console.log(`ARM control ${control ? 'PASS' : 'FAIL'} resolved money renders ${keys.length}, changed ${moved.length} ${JSON.stringify(moved.slice(0, 3))}`)
console.log(`ao7 build ${build ? 1 : 0}/1 control ${control ? 1 : 0}/1`)
