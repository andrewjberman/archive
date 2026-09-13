/**
 * run_render_check.mjs -- the runner for AMGT-re-1's render check.
 *
 * WHY VITE AND NOT PLAIN `tsx`. `PrintExportAction` transitively imports
 * `@/api/api-client.ts`, which reads `import.meta.env` at module scope. Under plain
 * Node that is `undefined` and the import throws -- which is exactly why the previous
 * cut hand-copied the button instead of importing it. Vite's own SSR module loader
 * (`server.ssrLoadModule`) supplies `import.meta.env` and resolves the `@/` alias from
 * `vite.config.ts`, so the REAL module graph loads and the REAL component and the REAL
 * action can both be exercised. No new dependency: `vite` is already a devDependency
 * of the portal (build ladder rung 5).
 *
 * The two shims below are ENVIRONMENT shims -- a storage object and a location -- not
 * stand-ins for any component under test. Node has no `localStorage`; `api-client.ts`
 * reads one for the bearer token.
 *
 * Usage (from the portal directory):
 *   node <this file> <portal-root> <output-dir>
 */

import { mkdirSync, writeFileSync } from 'node:fs'
import { createRequire } from 'node:module'
import { resolve } from 'node:path'
import { pathToFileURL } from 'node:url'

const portalRoot = resolve(process.argv[2] ?? '.')
const outDir = resolve(process.argv[3] ?? '.')

// This runner lives in the cell's deliverables folder, not in the portal, so Node
// would resolve a bare `import 'vite'` against THIS directory and miss. Resolve it
// from the portal's own package.json instead -- the same vite the portal builds with.
const portalRequire = createRequire(resolve(portalRoot, 'package.json'))
const { createServer } = await import(pathToFileURL(portalRequire.resolve('vite')).href)

if (!globalThis.localStorage) {
  const store = new Map()
  globalThis.localStorage = {
    getItem: (key) => (store.has(key) ? store.get(key) : null),
    setItem: (key, value) => store.set(key, String(value)),
    removeItem: (key) => store.delete(key),
    clear: () => store.clear(),
    key: (index) => Array.from(store.keys())[index] ?? null,
    get length() {
      return store.size
    },
  }
  globalThis.localStorage.setItem('accessToken', 'render-check-token')
}

const server = await createServer({
  root: portalRoot,
  configFile: resolve(portalRoot, 'vite.config.ts'),
  appType: 'custom',
  logLevel: 'warn',
  server: { middlewareMode: true, hmr: false, watch: null },
})

let exitCode = 0
try {
  const mod = await server.ssrLoadModule(
    '/src/pages/SecurityAnalysis/__rendercheck__/renderCheck.tsx'
  )
  const report = await mod.runRenderCheck()
  const { markup, ...summary } = report

  mkdirSync(outDir, { recursive: true })
  writeFileSync(resolve(outDir, 'rendercheck_route.html'), markup.route, 'utf8')
  writeFileSync(resolve(outDir, 'rendercheck_report.json'), JSON.stringify(summary, null, 2), 'utf8')

  console.log('RENDER CHECK -- real route, real print action')
  for (const route of summary.routes) {
    console.log('  ROUTE', route.path)
    console.log('    markup bytes             :', route.markupLength)
    console.log('    real Print button        :', route.printButtonPresent)
    console.log('    persistent Lead Panel    :', route.persistentPanelPresent)
    console.log('    tabs found               :', route.tabLabelsFound.join(', '))
    console.log('    Movement control on page :', route.movementControlPresent)
    console.log('    Subject control on page  :', route.subjectControlPresent)
    console.log('    Model tab (must be false):', route.modelTabPresent)
  }
  console.log('  declared combinations      :', summary.cross.declaredCombinationCount)
  console.log('  rendered panel states      :', summary.cross.renderedStates)
  console.log('  DISTINCT combinations seen :', summary.cross.distinctCombinationSubtitles)
  console.log('  combination labels         :', summary.cross.subtitles.join(' | '))
  console.log('  chart is over time         :', summary.chart.timeSeriesCaptionPresent)
  console.log('  chart ticker category axis (must be false):', summary.chart.tickerCategoryAxisPresent)
  console.log('  print action requested URL :', summary.print.requestedUrl)
  console.log('  print action expected URL  :', summary.print.expectedUrl)
  console.log('  print URL matches          :', summary.print.requestedUrl === summary.print.expectedUrl)
  console.log('  print Authorization sent   :', summary.print.authorizationSent)
  console.log('  print returned a Blob      :', summary.print.returnedBlob)
  console.log('  print error                :', summary.print.error)
  console.log('COLOUR LAW READ (portal/CLAUDE.md, silver canvas)')
  console.log('  elements scanned           :', summary.colourLaw.elementsScanned)
  console.log('  dark containers found      :', summary.colourLaw.darkContainersFound)
  console.log('  light-idiom elements       :', summary.colourLaw.elementsCarryingLightTokens)
  console.log('  VIOLATIONS (outside dark)  :', summary.colourLaw.findings.length)
  for (const finding of summary.colourLaw.findings) {
    console.log('    -', finding.tag, finding.offendingTokens.join(','), '|', finding.classAttribute)
  }
  console.log('  INSTRUMENT CONTROL -- broken-world findings (must be > 0):', summary.colourLawControl.brokenWorldFindings)
  console.log('  INSTRUMENT CONTROL -- clean-world findings (must be 0)  :', summary.colourLawControl.cleanWorldFindings)
  console.log('  INSTRUMENT CONTROL -- discriminates                     :', summary.colourLawControl.discriminates)

  const failures = []
  for (const route of summary.routes) {
    if (!route.printButtonPresent) failures.push(`real Print button absent from ${route.path}`)
    if (!route.persistentPanelPresent) failures.push(`persistent Lead Panel absent from ${route.path}`)
    if (route.tabLabelsFound.length !== 3) failures.push(`expected three tab labels on ${route.path}`)
    if (route.modelTabPresent) failures.push(`Model tab is present on ${route.path} and must not be`)
  }
  const universeRoute = summary.routes.find((route) => route.path === '/security-analysis')
  if (!universeRoute?.movementControlPresent) failures.push('Movement control absent from the universe route')
  if (!universeRoute?.subjectControlPresent) failures.push('Subject control absent from the universe route')
  if (!summary.colourLawControl.discriminates) failures.push('colour-law reader cannot discriminate')
  if (summary.cross.distinctCombinationSubtitles !== summary.cross.declaredCombinationCount) {
    failures.push('distinct combinations rendered does not equal the declared combination count')
  }
  if (!summary.chart.timeSeriesCaptionPresent) failures.push('chart is not rendering a time-series state')
  if (summary.chart.tickerCategoryAxisPresent) failures.push('chart still has a ticker category axis')
  if (summary.print.requestedUrl !== summary.print.expectedUrl) failures.push('print action hit the wrong URL')
  if (!summary.print.authorizationSent) failures.push('print action sent no Authorization header')
  if (summary.colourLaw.findings.length > 0) failures.push('colour-law violations outside a dark container')

  console.log('RESULT:', failures.length === 0 ? 'OK: render check clean' : 'BLOCKED: ' + failures.join('; '))
  exitCode = failures.length === 0 ? 0 : 1
} catch (err) {
  console.log('ERROR:', err && err.stack ? err.stack : String(err))
  exitCode = 2
} finally {
  await server.close()
}

process.exit(exitCode)
