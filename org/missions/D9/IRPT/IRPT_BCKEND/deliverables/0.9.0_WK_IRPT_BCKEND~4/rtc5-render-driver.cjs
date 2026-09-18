/**
 * RTC5 across-inputs render driver -- IRPT_BCKEND.TO-IB-rtc-5, worker 0.9.0_WK_IRPT_BCKEND~4.
 *
 * NOT A NEW RENDERER. This is FE-s-31's print-driver.mjs mechanism (Playwright request
 * interception over the REAL local vite dev server, the same identity stub, the same Edge
 * binary), unmodified in its rendering half, with ONE addition: `page.pdf()` at settle time,
 * because FE-s-31 only needed DOM state and this cell needs the ARTIFACT BYTES. The subject
 * under test is unchanged: PrintEntry.tsx -> composeExportBundle -> resolveBundle ->
 * PerformanceDocument/AnalysisDocument, the REAL render/manifest.ts package, on the LOCAL DEV
 * PLANE (bun run dev / vite), auth-stubbed exactly as ui-smoke.mjs and print-driver.mjs stub
 * it -- NOT the deployed session-gated https://opalinvest.dev origin render_export.cjs uses.
 *
 * CommonJS (not FE-s-31's .mjs) so `require('playwright-core')` resolves via NODE_PATH set to
 * the portal checkout's node_modules -- this worker's worktree carries an empty portal/
 * gitlink and this file lives outside the portal tree entirely (worktree bound: never write
 * into ajb_workspace).
 *
 * INPUT  argv[2]=port, argv[3]=scenarios JSON (same shape as fe-s-31's:
 *        { "<name>": { "query": "...", "fixtures": { "<url-substr>": <v1 envelope>, ... } } }),
 *        argv[4]=output directory for one <name>.pdf per scenario.
 * OUTPUT one `RESULT {json}` line per scenario (print state, pages, pdf path, byte length),
 *        then `DRIVER OK`.
 */
const { chromium } = require('playwright-core')
const { readFileSync, writeFileSync } = require('node:fs')

const PORT = process.argv[2]
const MAP_PATH = process.argv[3]
const OUT_DIR = process.argv[4]
const ORIGIN = `http://localhost:${PORT}`
const EDGE = 'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe'

const CORS = {
  'Access-Control-Allow-Origin': ORIGIN,
  'Access-Control-Allow-Credentials': 'true',
  'Access-Control-Allow-Headers': '*',
  'Access-Control-Allow-Methods': '*',
  'Content-Type': 'application/json',
}

const SESSION = {
  accessToken: 'rtc5-driver',
  user: {
    email: 'dev@opalcapital.com', name: 'Dev User', role: 'admin', userType: 'Dev',
    firmId: 'opal-capital', firmRole: null, advisorId: null, advisorRole: null, mustChangePassword: false,
  },
}

const scenarios = JSON.parse(readFileSync(MAP_PATH, 'utf8'))
const SETTLED = '[data-print-state="ready"], [data-print-state="refused"], [data-print-state="no-bundle-id"]'

async function main() {
  const browser = await chromium.launch({ executablePath: EDGE, headless: true })

  for (const [name, scenario] of Object.entries(scenarios)) {
    const fixtures = scenario.fixtures
    const keys = Object.keys(fixtures).sort((a, b) => b.length - a.length)
    const page = await browser.newPage({ viewport: { width: 1440, height: 900 } })
    page.on('pageerror', (e) => console.log('PAGE-CRASH:', name, String(e).slice(0, 200)))
    const served = new Set()
    await page.route('**/*', (r) => {
      const req = r.request()
      const url = req.url()
      if (req.method() === 'OPTIONS' && !url.startsWith(ORIGIN)) return r.fulfill({ status: 204, headers: CORS, body: '' })
      const key = keys.find((k) => url.includes(k))
      if (key) {
        served.add(key)
        return r.fulfill({ status: 200, headers: CORS, body: JSON.stringify(fixtures[key]) })
      }
      if (url.includes('/auth/refresh')) return r.fulfill({ status: 200, headers: CORS, body: JSON.stringify(SESSION) })
      return r.continue()
    })

    await page.goto(`${ORIGIN}/investor-reporting/print?${scenario.query}`, { waitUntil: 'networkidle', timeout: 60000 })
    const settled = await page.waitForSelector(SETTLED, { timeout: 30000 }).then(() => true, () => false)
    const state = await page.evaluate(() => {
      const root = document.querySelector('[data-print-state]')
      const status = document.querySelector('.ir-print-status')
      return {
        printState: root ? root.getAttribute('data-print-state') : null,
        reportKind: root ? root.getAttribute('data-report-kind') : null,
        pages: document.querySelectorAll('section.ir-page').length,
        refusalText: status ? status.textContent.replace(/\s+/g, ' ').trim().slice(0, 200) : null,
      }
    })
    let pdfPath = null
    let pdfBytes = 0
    if (settled && state.printState === 'ready') {
      const pdf = await page.pdf({ preferCSSPageSize: true, printBackground: true })
      pdfPath = `${OUT_DIR}/${name}.pdf`
      writeFileSync(pdfPath, pdf)
      pdfBytes = pdf.length
    }
    console.log(`RESULT ${JSON.stringify({ name, settled, ...state, served: Array.from(served).sort(), pdfPath, pdfBytes })}`)
    await page.close()
  }

  await browser.close()
  console.log('DRIVER OK')
}

main().catch((err) => {
  console.error('DRIVER-FATAL:', err && err.stack ? err.stack : String(err))
  process.exit(1)
})
