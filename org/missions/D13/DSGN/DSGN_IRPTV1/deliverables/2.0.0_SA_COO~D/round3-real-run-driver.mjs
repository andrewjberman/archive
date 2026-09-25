/**
 * DSGN_IRPTV1 round 3 -- the COO's real run of the round's outcomes at the drain (/dispatch Step 5).
 * The same auth-stub + CORS + fixture-route recipe as analysis-probe-driver.mjs, with the selection step moved to the
 * shared SearchSelect (IV-e-9): type into [data-slot="search-select-input"], click the option by its label.
 * CLAIM CLASS: driver-scripted on localhost:5174 against a fixture file, never the signed-in live thread (FWD-1).
 * Usage: node round3-real-run-driver.mjs <port> <out-prefix> <fixture.json> [client label]
 */
import { chromium } from 'playwright-core'
import { readFileSync } from 'node:fs'

const PORT = process.argv[2] || '5174'
const PREFIX = process.argv[3] || 'r3'
const FIXTURE_PATH = process.argv[4]
const CLIENT = process.argv[5] || 'Cottonwood Trust'
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
  accessToken: 'ui-smoke-token',
  user: { email: 'dev@opalcapital.com', name: 'Dev User', role: 'admin',
          userType: 'Dev', firmId: 'opal-capital', firmRole: null, advisorId: null,
          advisorRole: null, mustChangePassword: false },
}
const fixtures = JSON.parse(readFileSync(FIXTURE_PATH, 'utf8'))
const fixtureKeys = Object.keys(fixtures).sort((a, b) => b.length - a.length)
const matchFixture = (url) => fixtureKeys.find((key) => url.includes(key))

const browser = await chromium.launch({ executablePath: EDGE, headless: true })
const page = await browser.newPage({ viewport: { width: 1440, height: 900 } })
const hit = new Set()
page.on('pageerror', (e) => console.log('PAGE-CRASH:', String(e).slice(0, 300)))
page.on('console', (m) => { if (m.type() === 'error') console.log('CONSOLE-ERROR:', m.text().slice(0, 240)) })
page.on('response', (res) => { if (res.url().includes('/directory/search')) console.log('SEARCH-RESPONSE:', res.status(), res.url().slice(-120)) })
await page.route('**/*', async (r) => {
  const req = r.request()
  const url = req.url()
  if (req.method() === 'OPTIONS' && !url.startsWith(ORIGIN)) return r.fulfill({ status: 204, headers: CORS, body: '' })
  const fk = matchFixture(url)
  if (fk) { hit.add(fk); return r.fulfill({ status: 200, headers: CORS, body: JSON.stringify(fixtures[fk]) }) }
  if (url.includes('/auth/refresh')) return r.fulfill({ status: 200, headers: CORS, body: JSON.stringify(SESSION) })
  return r.continue()
})

async function tab(name) {
  await page.getByRole('button', { name, exact: true }).or(page.getByRole('tab', { name })).first().click()
  await page.waitForTimeout(2500)
}
async function shot(name) {
  const path = `${PREFIX}.${name}.png`
  await page.screenshot({ path, fullPage: true })
  console.log('SAVED:', path)
}
const probe = () => page.evaluate(() => {
  const text = document.body.innerText
  const q = (s) => document.querySelectorAll(s).length
  return {
    tabs: [...document.querySelectorAll('[data-slot="tab-shell"] button, [role="tab"]')].map((b) => b.innerText.trim()).filter(Boolean).slice(0, 3),
    headerExport: q('[data-slot="export-target"]'),
    perTabExport: q('[data-slot="export-button"]'),
    sampleBadges: q('[data-slot="sample-badge"]'),
    choosePrompts: q('[data-slot="sample-choose-client-prompt"]'),
    accountFilter: q('[data-slot="holdings-account-filter"]'),
    variantCards: q('[data-slot="variant-card"]'),
    composerClient: document.querySelector('[data-slot="composer-client"]')?.innerText ?? null,
    selectAClient: /select a client/i.test(text),
    unavailableWord: /\bUNAVAILABLE\b/.test(text),
    rawIso: /\d{4}-\d{2}-\d{2}T\d{2}:\d{2}/.test(text),
    accIds: (text.match(/\bacc_[0-9a-z]{4,}/gi) || []).length,
    darkClassNodes: q('[class*="dark:"]'),
  }
})

await page.goto(ORIGIN + '/investor-reporting', { waitUntil: 'networkidle', timeout: 30000 }).catch((e) => console.log('goto:', e.message.split('\n')[0]))
await page.waitForTimeout(2000)
console.log('NO-CLIENT performance:', JSON.stringify(await probe()))
await shot('01-sample-performance')
await tab('Holdings')
console.log('NO-CLIENT holdings:', JSON.stringify(await probe()))
await shot('02-sample-holdings')

let selectOk = false
try {
  const input = page.locator('[data-slot="search-select-input"]').first()
  await input.click()
  await input.fill(CLIENT.split(' ')[0])
  await page.waitForTimeout(1200)
  const option = page.locator('[data-slot="search-select-option"]', { hasText: CLIENT }).first()
  await option.waitFor({ state: 'visible', timeout: 6000 })
  await option.click()
  selectOk = true
} catch (e) { console.log('SELECT-FAIL:', e.message.split('\n')[0]) }
console.log('SELECT-OK:', selectOk)
await page.waitForTimeout(3500)

await tab('Performance')
console.log('CLIENT performance:', JSON.stringify(await probe()))
await shot('03-performance')
await tab('Holdings')
console.log('CLIENT holdings:', JSON.stringify(await probe()))
await page.locator('[data-slot="identity-card"] summary').first().click().catch(() => {})
console.log('IDENTITY:', (await page.locator('[data-slot="identity-card"]').first().innerText().catch(() => 'none')).replace(/\s+/g, ' ').slice(0, 300))
await shot('04-holdings')
await tab('Analysis')
console.log('CLIENT analysis:', JSON.stringify(await probe()))
await shot('05-analysis')

console.log(`DRIVER-FIXTURES-MATCH: matched ${hit.size} of ${fixtureKeys.length}`)
await browser.close()
