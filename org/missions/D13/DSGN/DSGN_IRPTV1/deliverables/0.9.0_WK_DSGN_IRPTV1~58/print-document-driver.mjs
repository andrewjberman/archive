/**
 * TO-IV-e-105 SUPPLEMENTARY driver -- NOT the order's named instrument (scripts/ui-smoke.mjs). ui-smoke takes a route and a fixture map
 * but cannot read the printed document's text; this script replicates ui-smoke's own recipe (auth stub, CORS echo, --dist serving
 * through scripts/ui-dist.mjs, full-page screenshot, the body background as CANVAS) the way the ~57 opal-report-driver.mjs does, and
 * opens the PRINT route (/investor-reporting/print?kind=analysis&request=...), the page the render host prints and exports.
 *
 * Usage: node print-document-driver.mjs <portal root> <out.png> <fixture.json> <dist dir> <request id>
 * The fixture is a url-substring -> body map like ui-smoke's --fixtures (longest substring wins). No dev server, no port, no network:
 * --dist routing answers every request. Fixture bodies are synthetic.
 */
import { readFileSync, writeFileSync } from 'node:fs'
import { pathToFileURL } from 'node:url'
import { resolve } from 'node:path'

const [PORTAL, out, fixturePath, dist, requestId] = process.argv.slice(2)
const { chromium } = await import(pathToFileURL(resolve(PORTAL, 'node_modules/playwright-core/index.mjs')).href)
const { serveFromDist } = await import(pathToFileURL(resolve(PORTAL, 'scripts/ui-dist.mjs')).href)

const ORIGIN = 'http://localhost:5199' // an origin string only; nothing listens
const EDGE = 'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe'
const CORS = {
  'Access-Control-Allow-Origin': ORIGIN, 'Access-Control-Allow-Credentials': 'true', 'Access-Control-Allow-Headers': '*',
  'Access-Control-Allow-Methods': '*', 'Content-Type': 'application/json',
}
const SESSION = {
  accessToken: 'ui-smoke-token',
  user: { email: 'dev@opalcapital.com', name: 'Dev User', role: 'admin', userType: 'Dev', firmId: 'opal-capital', firmRole: null, advisorId: null, advisorRole: null, mustChangePassword: false },
}
const fixtures = JSON.parse(readFileSync(fixturePath, 'utf8'))
const keys = Object.keys(fixtures).sort((a, b) => b.length - a.length)
const log = []
const hits = {}
const misses = []

process.on('uncaughtException', (e) => { for (const line of log) console.log('LOG   :', line); console.log('FAILED:', String(e).split('\n')[0]); process.exit(1) })
const browser = await chromium.launch({ executablePath: EDGE, headless: true })
const page = await browser.newPage({ viewport: { width: 1000, height: 1300 } })
page.on('console', (m) => { if (m.type() === 'error') log.push('CONSOLE-ERROR: ' + m.text().slice(0, 240)) })
page.on('pageerror', (e) => log.push('PAGE-CRASH: ' + String(e).slice(0, 200)))
await page.route('**/*', async (r) => {
  const req = r.request()
  const url = req.url()
  if (req.method() === 'OPTIONS' && !url.startsWith(ORIGIN)) return r.fulfill({ status: 204, headers: CORS, body: '' })
  const fk = keys.find((key) => url.includes(key))
  if (fk) { hits[fk] = (hits[fk] || 0) + 1; return r.fulfill({ status: 200, headers: CORS, body: JSON.stringify(fixtures[fk]) }) }
  if (url.includes('/auth/refresh')) return r.fulfill({ status: 200, headers: CORS, body: JSON.stringify(SESSION) })
  if (url.includes('/api/')) misses.push(req.method() + ' ' + url.replace(ORIGIN, ''))
  if (await serveFromDist(r, resolve(dist), ORIGIN)) return
  return r.continue()
})
const url = ORIGIN + '/investor-reporting/print?bundle=BND-synthetic-1&kind=analysis&request=' + requestId + '&tenant=F-CW&scope=fp-synthetic&revision=rev-synthetic-1'
await page.goto(url, { waitUntil: 'networkidle', timeout: 30000 }).catch((e) => log.push('goto: ' + e.message.split('\n')[0]))
await page.waitForSelector('[data-print-state]', { timeout: 15000 }).catch(() => log.push('no [data-print-state] mounted'))
await page.waitForTimeout(2500)
const state = await page.evaluate(() => {
  const root = document.querySelector('[data-print-state]')
  const doc = document.querySelector('[data-document="analysis"]')
  return {
    loc: location.pathname + location.search,
    canvas: getComputedStyle(document.body).backgroundColor,
    printState: root ? root.getAttribute('data-print-state') : null,
    documentMounted: !!doc,
    pages: doc ? document.querySelectorAll('[data-document="analysis"] [data-page]').length : 0,
    coverageBlockDrawn: !!document.querySelector('[data-slot="extraction-coverage"]'),
    documentText: doc ? doc.innerText.replace(/\s+/g, ' ').trim() : (root ? root.innerText.replace(/\s+/g, ' ').trim() : null),
  }
})
await page.screenshot({ path: out, fullPage: true })
await browser.close()
console.log('LOC   :', state.loc)
console.log('CANVAS:', state.canvas)
console.log('PRINT-STATE:', state.printState, ' DOCUMENT-MOUNTED:', state.documentMounted, ' PAGES:', state.pages, ' COVERAGE-BLOCK-DRAWN:', state.coverageBlockDrawn)
console.log('VENDOR-OR-EXTRACTION WORD IN THE DOCUMENT (innerText, any case):', state.documentText === null ? 'n/a' : /vendor|extraction/i.test(state.documentText))
console.log('DOCUMENT-TEXT (visible innerText):', state.documentText)
for (const k of Object.keys(hits)) console.log('FIXTURE-HIT:', hits[k], k.replace('/api/scoped/investor-reporting/', '.../'))
for (const m of misses) console.log('API-NOT-IN-FIXTURE:', m)
for (const line of log) console.log('LOG   :', line)
writeFileSync(out + '.txt', JSON.stringify(state, null, 1))
console.log('SAVED :', out)
