/**
 * TO-IV-e-102 SUPPLEMENTARY driver -- NOT the order's named instrument (scripts/ui-smoke.mjs). ui-smoke has no way to choose a file for
 * the Prospect upload input and its fixture map ignores the HTTP method (the Prospect upload and submit are POSTs to routes that are
 * substrings of the GET ones), so it cannot reach "a Prospect upload generated, no client in the header". This script copies ui-smoke's
 * recipe (auth stub, CORS echo, --dist serving through scripts/ui-dist.mjs, full-page screenshot, the body background as CANVAS) and adds:
 * a method-aware fixture map (a key "POST <path>" matches only a POST to exactly that path), opening the Analysis tab WITHOUT picking a
 * client, choosing the Prospect card, choosing a synthetic holdings file, Review portfolio, filling "Prepared for", pressing Generate.
 *
 * Usage: node prospect-open-driver.mjs <portal root> <out.png> <fixture.json> <dist dir> [open]
 *   with the last argument "open", it then presses Open on the first row of "Your analysis requests" if that list is on the page.
 * No dev server, no port, no network: --dist routing answers every request. Fixture bodies are synthetic.
 */
import { readFileSync, writeFileSync } from 'node:fs'
import { pathToFileURL } from 'node:url'
import { resolve } from 'node:path'

const [PORTAL, out, fixturePath, dist, tail] = process.argv.slice(2)
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
const log = []
const hits = {}
const calls = []

process.on('uncaughtException', (e) => { for (const line of log) console.log('LOG   :', line); for (const c of calls) console.log('CALL  :', c); for (const k of Object.keys(hits)) console.log('FIXTURE-HIT:', hits[k], k); console.log('FAILED:', String(e).split(String.fromCharCode(10))[0]); process.exit(1) })
const browser = await chromium.launch({ executablePath: EDGE, headless: true })
const page = await browser.newPage({ viewport: { width: 1440, height: 1500 } })
page.on('console', (m) => { if (m.type() === 'error') log.push('CONSOLE-ERROR: ' + m.text().slice(0, 240)) })
page.on('pageerror', (e) => log.push('PAGE-CRASH: ' + String(e).slice(0, 200)))
await page.route('**/*', async (r) => {
  const req = r.request()
  const url = req.url()
  const method = req.method()
  if (method === 'OPTIONS' && !url.startsWith(ORIGIN)) return r.fulfill({ status: 204, headers: CORS, body: '' })
  const body = req.postData() || ''
  if (url.includes('/api/scoped/')) calls.push(method + ' ' + (new URL(url).pathname + new URL(url).search).replace('/api/scoped/investor-reporting/', '.../') + (body ? '  BODY: ' + body.slice(0, 140) : ''))
  // A fixture key is "<url-substring>" (any method, longest wins, as ui-smoke) or "POST <path>" (a POST to exactly that path) or
  // "POST <path> ~<text>" (the same, only when the request body contains <text>; the more specific key wins).
  const parsed = Object.keys(fixtures).map((key) => {
    const m = /^POST (\S+)(?: ~(.*))?$/.exec(key)
    return m ? { key, post: true, path: m[1], needle: m[2] ?? null } : { key, post: false }
  })
  let chosen = null
  if (method === 'POST') {
    const path = new URL(url).pathname
    const cands = parsed.filter((c) => c.post && path.endsWith(c.path.replace('/api/scoped/investor-reporting', '')) && (c.needle === null || body.includes(c.needle)))
    chosen = cands.sort((a, b) => (b.needle ? 1 : 0) - (a.needle ? 1 : 0))[0]?.key ?? null
  }
  if (chosen === null) chosen = parsed.filter((c) => !c.post && url.includes(c.key)).sort((a, b) => b.key.length - a.key.length)[0]?.key ?? null
  if (chosen !== null) { hits[chosen] = (hits[chosen] || 0) + 1; return r.fulfill({ status: 200, headers: CORS, body: JSON.stringify(fixtures[chosen]) }) }
  if (url.includes('/auth/refresh')) return r.fulfill({ status: 200, headers: CORS, body: JSON.stringify(SESSION) })
  if (await serveFromDist(r, resolve(dist), ORIGIN)) return
  return r.continue()
})
await page.goto(ORIGIN + '/investor-reporting', { waitUntil: 'networkidle', timeout: 30000 }).catch((e) => log.push('goto: ' + e.message.split('\n')[0]))
await page.waitForTimeout(2000)
log.push('LANDED: ' + (await page.evaluate(() => location.pathname + ' | ' + document.body.innerText.replace(/\s+/g, ' ').slice(0, 300))))
// NO client is picked: the header's Client search is left untouched.
await page.getByRole('button', { name: 'Analysis', exact: true }).or(page.getByRole('tab', { name: 'Analysis', exact: true })).first().click()
log.push('OPENED the Analysis tab (no client picked)')
await page.waitForTimeout(2500)
const beforeUpload = await page.evaluate(() => ({
  history: !!document.querySelector('[data-slot="owned-request-history"]'),
  clientCardDisabled: document.querySelector('[data-portfolio="client"]')?.disabled ?? null,
}))
log.push('BEFORE any upload: history section mounted=' + beforeUpload.history + ', Client card disabled=' + beforeUpload.clientCardDisabled)
await page.locator('button[data-portfolio="prospect"]').click()
log.push('CHOSE the Prospect card')
await page.waitForTimeout(800)
// An Opal-internal viewer's Prospect card must name its firm before it will review (R18); choose the one firm the catalogue lists.
const firmSelect = page.locator('[data-slot="prospect-firm-select"]')
log.push('FIRM SELECT: ' + (await firmSelect.count() ? await firmSelect.evaluate((el) => el.outerHTML.slice(0, 400)) : 'absent'))
if (await firmSelect.count()) { await firmSelect.selectOption('sample-firm'); log.push('CHOSE the Prospect card firm in its own select (no client)') }
await page.waitForTimeout(500)
const csv = Buffer.from('Ticker,Dollars\nAAPL,600\nMSFT,400\n', 'utf8')
await page.locator('[data-slot="upload-dropzone"] input[type="file"]').setInputFiles({ name: 'prospect.csv', mimeType: 'text/csv', buffer: csv })
log.push('CHOSE a synthetic holdings file (2 rows)')
await page.waitForTimeout(500)
const composer = await page.evaluate(() => ({
  reviewDisabled: Array.from(document.querySelectorAll('[data-slot="prospect-composer"] button')).find((b) => /Review portfolio/.test(b.textContent))?.disabled ?? 'no such button',
  firmSelectPresent: !!document.querySelector('[data-slot="prospect-firm-select"]'),
  firmRefusal: document.querySelector('[data-slot="prospect-firm-refusal"]')?.textContent ?? null,
  uploadState: document.querySelector('[data-slot="upload-state"]')?.textContent ?? null,
}))
log.push('COMPOSER before Review: ' + JSON.stringify(composer))
await page.getByRole('button', { name: 'Review portfolio', exact: true }).click({ timeout: 8000 })
log.push('PRESSED Review portfolio')
await page.waitForSelector('[data-slot="prospect-review"]', { timeout: 15000 })
await page.locator('[data-slot="prospect-composer"]').getByLabel('Prepared for').fill('Sample Prospect')
await page.locator('[data-slot="prospect-composer"]').getByRole('button', { name: /^Generate/ }).click()
log.push('PRESSED Generate')
await page.waitForTimeout(4000)
if (tail === 'open') {
  const opener = page.locator('[data-slot="owned-request-history"] li[data-row="owned-analysis-request"] button').first()
  if (await opener.count()) { await opener.click(); log.push('PRESSED Open on the first history row'); await page.waitForTimeout(3500) } else log.push('NO opener to press')
}
const state = await page.evaluate(() => {
  const txt = (el) => (el ? el.textContent.replace(/\s+/g, ' ').trim() : null)
  const hist = document.querySelector('[data-slot="owned-request-history"]')
  const tab = document.querySelector('[data-slot="analysis-tab"]')
  const buttons = tab ? Array.from(tab.querySelectorAll('button, a[href]')).filter((b) => b.offsetParent !== null).map((b) => (b.getAttribute('aria-label') || b.textContent).replace(/\s+/g, ' ').trim()) : []
  const headerSearch = document.querySelector('[role="combobox"]')
  return {
    loc: location.pathname,
    canvas: getComputedStyle(document.body).backgroundColor,
    headerClientSearchValue: headerSearch ? headerSearch.value : null,
    historySectionMounted: !!hist,
    historyHeading: hist ? txt(hist.querySelector('h2')) : null,
    historyRows: hist ? hist.querySelectorAll('li[data-row="owned-analysis-request"]').length : 0,
    historyText: txt(hist),
    jobStatusText: txt(document.querySelector('[data-slot="prospect-job-status"]')),
    generateButtonText: txt(Array.from(document.querySelectorAll('[data-slot="prospect-review"] button')).find((b) => /Request accepted|Generate/.test(b.textContent))),
    dialogOpen: !!document.querySelector('[data-slot="owned-request-detail"]'),
    sectionsMounted: !!document.querySelector('[data-slot="owned-report-sections"]'),
    visibleButtonsAndLinksInAnalysisTab: buttons,
  }
})
await page.screenshot({ path: out, fullPage: true })
await browser.close()
console.log('LOC   :', state.loc)
console.log('CANVAS:', state.canvas)
console.log('HEADER-CLIENT-SEARCH value:', JSON.stringify(state.headerClientSearchValue))
console.log('GENERATE BUTTON:', state.generateButtonText)
console.log('JOB STATUS:', state.jobStatusText)
console.log('HISTORY-SECTION-MOUNTED:', state.historySectionMounted, ' HEADING:', state.historyHeading, ' ROWS:', state.historyRows)
console.log('DIALOG-OPEN:', state.dialogOpen, ' REPORT-SECTIONS-MOUNTED:', state.sectionsMounted)
console.log('VISIBLE BUTTONS/LINKS IN THE ANALYSIS TAB:', JSON.stringify(state.visibleButtonsAndLinksInAnalysisTab))
for (const c of calls) console.log('CALL  :', c)
for (const k of Object.keys(hits)) console.log('FIXTURE-HIT:', hits[k], k.replace('/api/scoped/investor-reporting/', '.../'))
for (const line of log) console.log('LOG   :', line)
writeFileSync(out + '.txt', JSON.stringify(state, null, 1))
console.log('SAVED :', out)
