/**
 * AMGT_CORPUS round 46, CRPS-av-9 -- FWD-21's two missing reads (PRD:615-618). Issuer's file. READ-ONLY.
 *
 * RUN:  node av9_forecast_reads.cjs <portal root> <capture.json>      (capture: av_capture.py over the LIVE function)
 *
 * DONE WHEN: for a name whose block carries forecast years, the tab renders 2026E, 2027E and 2028E beside the history columns from the
 * served object, and a name without them reads the reason; the history columns are byte-unchanged.
 * Per name the REAL modelSheet.ts `buildModelSheet` is called twice with the arguments ModelTab.tsx passes: with the served forecast
 * figures, and with none (the history-only build). Then:
 *   history   the history year columns of every row of every group are JSON-equal between the two builds (and the history year list is
 *             the same), counted over all names;
 *   forecast  a name with served forecast figures renders E years; a name without reads a served `forecast_reason` (a non-empty
 *             sentence) -- named, with the wrong-sentence check the round-41 finding asked for (UNVGY);
 * Prints `av9 history equal <h> of <n>`, `av9 forecast names <f> render E years <e>`, `av9 no forecast <k> reason served <r>`, then the
 * UNVGY line and every name that has neither forecast years nor a reason.
 */
const fs = require('fs')
const path = require('path')
const vm = require('vm')
const { execSync } = require('child_process')
const { createRequire } = require('module')

const top = execSync('git rev-parse --show-toplevel', { encoding: 'utf8' }).trim()
const portalRoot = path.resolve(process.argv[2])
const cap = JSON.parse(fs.readFileSync(path.resolve(process.argv[3]), 'utf8'))

function installed(name) {
  for (const root of [portalRoot, path.join(top, 'portal')]) {
    try { return createRequire(path.join(root, 'package.json'))(name) } catch (e) { /* next */ }
  }
  throw new Error(name + ' not resolvable')
}
const ts = installed('typescript')
const stub = new Proxy({}, { get: (_t, k) => (k === '__esModule' ? true : () => '') })
const file = path.join(portalRoot, 'src', 'pages', 'SecurityAnalysis', 'modelSheet.ts')
const out = ts.transpileModule(fs.readFileSync(file, 'utf8'), {
  compilerOptions: { module: ts.ModuleKind.CommonJS, target: ts.ScriptTarget.ES2020 },
}).outputText
const mod = { exports: {} }
vm.runInNewContext(out, { module: mod, exports: mod.exports, require: () => stub, console })
const m = mod.exports

const names = Object.keys(cap.keys).sort()
let histEqual = 0
let fcNames = 0
let fcRender = 0
let noFc = 0
let noFcReason = 0
const neither = []
const diff = []
console.log('capture function CodeSha256 ' + cap.function.CodeSha256 + ' LastModified ' + cap.function.LastModified + '; modelSheet.ts at ' + portalRoot)
for (const key of names) {
  const d = cap.keys[key]
  const model = d.model || {}
  const fc = Array.isArray(model.forecast_figures) ? model.forecast_figures : []
  const ln = model.line_names === '<KEY ABSENT>' ? undefined : model.line_names
  const unresolved = Array.isArray(model.fiscal_unresolved) ? model.fiscal_unresolved : undefined
  const none = m.buildModelSheet(d.fiscal_year_figures || [], d.fiscal_years, ln, undefined, unresolved, d.header_figures)
  const withF = m.buildModelSheet(d.fiscal_year_figures || [], d.fiscal_years, ln, fc.length ? fc : undefined, unresolved, d.header_figures)
  const histIdx = (withF.years || []).map((y, i) => (String(y).endsWith('E') ? -1 : i)).filter((i) => i >= 0)
  const sameYears = JSON.stringify(histIdx.map((i) => withF.years[i])) === JSON.stringify(none.years)
  let sameCells = (withF.groups || []).length === (none.groups || []).length
  if (sameCells) {
    for (let g = 0; g < withF.groups.length && sameCells; g += 1) {
      const a = withF.groups[g].rows
      const b = none.groups[g].rows
      if (a.length !== b.length) { sameCells = false; break }
      for (let r = 0; r < a.length; r += 1) {
        const ha = histIdx.map((i) => a[r].cells[i])
        if (JSON.stringify(ha) !== JSON.stringify(b[r].cells)) { sameCells = false; break }
      }
    }
  }
  if (sameYears && sameCells) histEqual += 1
  else diff.push(key)
  const hasE = (withF.years || []).some((y) => String(y).endsWith('E'))
  if (fc.length > 0) {
    fcNames += 1
    if (hasE) fcRender += 1
  } else {
    noFc += 1
    const reason = model.forecast_reason
    if (typeof reason === 'string' && reason.trim()) noFcReason += 1
    else neither.push(key)
  }
}
console.log('av9 history equal ' + histEqual + ' of ' + names.length + (diff.length ? ' differing: ' + diff.slice(0, 8).join(',') : ''))
console.log('av9 forecast names ' + fcNames + ' render E years ' + fcRender)
console.log('av9 no forecast ' + noFc + ' reason served ' + noFcReason + (neither.length ? ' WITHOUT a reason: ' + neither.join(',') : ''))
for (const key of names.filter((k) => /^UNVGY/.test(k))) {
  const model = cap.keys[key].model || {}
  console.log('av9 ' + key + ' forecast_figures ' + ((model.forecast_figures || []).length) + ' forecast_periods ' + JSON.stringify(model.forecast_periods) + ' forecast_reason ' + JSON.stringify(model.forecast_reason))
}
