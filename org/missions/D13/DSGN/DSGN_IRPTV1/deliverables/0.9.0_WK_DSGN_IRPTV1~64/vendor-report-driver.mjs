/**
 * TO-IV-e-101 SUPPLEMENTARY driver -- NOT the order's named instrument (scripts/ui-smoke.mjs). ui-smoke cannot type into the header's
 * role=combobox "Client search", so it cannot pick a client, and OwnedRequestHistory (the list whose Open shows the report) mounts
 * only when a client is picked (AnalysisTab.tsx: `hasClient ? ... <OwnedRequestHistory/>`). This script replicates ui-smoke's own
 * recipe (auth stub, CORS echo, --dist serving through scripts/ui-dist.mjs, full-page screenshot, the body background as CANVAS), the
 * same way the earlier holdings-face driver did, and adds: typing the search, opening the Analysis tab, pressing Open on one request
 * row of the history list, and expanding "Technical details".
 *
 * Usage: node opal-report-driver.mjs <portal root> <out.png> <fixture.json> <dist dir> <request id> [technical|closed]
 * The fixture is a url-substring -> body map like ui-smoke's --fixtures (longest substring wins). No dev server, no port, no network:
 * --dist routing answers every request. Fixture bodies are synthetic.
 */
import { readFileSync, writeFileSync } from 'node:fs'
import { pathToFileURL } from 'node:url'
import { resolve } from 'node:path'

const [PORTAL, out, fixturePath, dist, requestId, technical] = process.argv.slice(2)
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

process.on('uncaughtException', (e) => { for (const line of log) console.log('LOG   :', line); console.log('FAILED:', String(e).split(String.fromCharCode(10))[0]); process.exit(1) })
const browser = await chromium.launch({ executablePath: EDGE, headless: true })
const page = await browser.newPage({ viewport: { width: 1440, height: 1500 } })
page.on('console', (m) => { if (m.type() === 'error') log.push('CONSOLE-ERROR: ' + m.text().slice(0, 240)) })
page.on('pageerror', (e) => log.push('PAGE-CRASH: ' + String(e).slice(0, 200)))
await page.route('**/*', async (r) => {
  const req = r.request()
  const url = req.url()
  if (req.method() === 'OPTIONS' && !url.startsWith(ORIGIN)) return r.fulfill({ status: 204, headers: CORS, body: '' })
  const fk = keys.find((key) => url.includes(key))
  if (fk) { hits[fk] = (hits[fk] || 0) + 1; return r.fulfill({ status: 200, headers: CORS, body: JSON.stringify(fixtures[fk]) }) }
  if (url.includes('/auth/refresh')) return r.fulfill({ status: 200, headers: CORS, body: JSON.stringify(SESSION) })
  if (await serveFromDist(r, resolve(dist), ORIGIN)) return
  return r.continue()
})
await page.goto(ORIGIN + '/investor-reporting', { waitUntil: 'networkidle', timeout: 30000 }).catch((e) => log.push('goto: ' + e.message.split('\n')[0]))
await page.waitForTimeout(2000)
const box = page.getByRole('combobox', { name: 'Client search', exact: true })
await box.click()
await box.pressSequentially('Sample', { delay: 60 })
await page.waitForTimeout(1500)
await page.getByText('Sample Household').first().click({ timeout: 10000 })
log.push('PICKED the first search row')
await page.waitForTimeout(2500)
await page.getByRole('button', { name: 'Analysis', exact: true }).or(page.getByRole('tab', { name: 'Analysis', exact: true })).first().click()
log.push('OPENED the Analysis tab')
await page.waitForTimeout(3000)
const rows = await page.locator('li[data-row="owned-analysis-request"]').count()
log.push('history rows on the page: ' + rows)
await page.locator(`li[data-request-id="${requestId}"] button`).first().click({ timeout: 10000 })
log.push('PRESSED Open on ' + requestId)
await page.waitForTimeout(4000)
if (technical === 'technical') {
  await page.locator('[data-slot="report-technical-details"] summary').first().click({ timeout: 10000 })
  log.push('EXPANDED Technical details')
  await page.waitForTimeout(800)
}
const state = await page.evaluate(() => {
  const dlg = document.querySelector('[data-slot="owned-request-detail"]')
  const sec = document.querySelector('[data-slot="owned-report-sections"]')
  return {
    loc: location.pathname,
    canvas: getComputedStyle(document.body).backgroundColor,
    dialogOpen: !!dlg,
    sectionsMounted: !!sec,
    dialogText: dlg ? dlg.textContent.replace(/\s+/g, ' ').trim() : null,
    sectionsText: sec ? sec.textContent.replace(/\s+/g, ' ').trim() : null,
    sectionsInnerText: sec ? sec.innerText.replace(/\s+/g, ' ').trim() : null,
  }
})
await page.screenshot({ path: out, fullPage: true })
await browser.close()
console.log('LOC   :', state.loc)
console.log('CANVAS:', state.canvas)
console.log('DIALOG:', state.dialogOpen, ' SECTIONS-MOUNTED:', state.sectionsMounted)
console.log('SECTIONS-TEXT (textContent):', state.sectionsText)
console.log('SECTIONS-TEXT (visible innerText):', state.sectionsInnerText)
console.log('VENDOR-OR-EXTRACTION WORD IN THE REPORT (textContent, any case):', state.sectionsText === null ? 'n/a' : /vendor|extraction/i.test(state.sectionsText))
console.log('VENDOR-OR-EXTRACTION WORD IN THE WHOLE OPENED REQUEST DIALOG (textContent incl. collapsed details, any case):', state.dialogText === null ? 'n/a' : /vendor|extraction/i.test(state.dialogText))
console.log('DIALOG-TEXT (textContent):', state.dialogText)
for (const k of Object.keys(hits)) console.log('FIXTURE-HIT:', hits[k], k.replace('/api/scoped/investor-reporting/', '.../'))
for (const line of log) console.log('LOG   :', line)
writeFileSync(out + '.txt', JSON.stringify(state, null, 1))
console.log('SAVED :', out)
