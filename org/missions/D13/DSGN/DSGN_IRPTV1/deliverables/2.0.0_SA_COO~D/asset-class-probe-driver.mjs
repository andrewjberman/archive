/**
 * IV-e-2 (DSGN_IRPTV1 round 2) -- a STANDALONE selection driver, NOT scripts/ui-smoke.mjs
 * (out of this order's <paths> grant, and its --fill/--click/--clicktext vocabulary cannot
 * reach a role="combobox" control -- measured: `getByRole('textbox', {name:'Client search'})`
 * times out; the accessible role is 'combobox', not 'textbox' -- precedent for this exact gap
 * at org/tier1_exec/3.0.0_SA_CVO/deliverables/IRPT_MVP_P/{mounted_selection_cases,
 * header_cases_dcf5}.mjs and org/missions/D9/IRPT/IRPT_FNTEND's FE-s-78, which built their own
 * standalone drivers for the identical reason).
 *
 * Replicates scripts/ui-smoke.mjs's own auth-stub + CORS + fixture-route recipe byte-for-byte
 * (read from that file's header comment and its route handler, unedited) so the state this
 * script reaches is the SAME state ui-smoke.mjs would reach given a --click step it cannot
 * express -- then drives the ONE extra step (selecting "Cottonwood Trust" from the
 * role=combobox "Client search" control) via `page.getByRole('combobox', ...)` directly, and
 * screenshots the result. AC2's own graded invocation (no --click steps) is unaffected; this
 * is ADDITIONAL evidence for AC4's judgment, cited in the result file.
 */
import { chromium } from 'playwright-core'
import { readFileSync, writeFileSync } from 'node:fs'

const PORT = process.argv[2] || '5181'
const OUT = process.argv[3] || 'iv-e-2-selected.png'
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
const FIXTURE_PATH = process.argv[4] || 'C:/tmp/wk-dsgn_irptv1-2-5/portal/src/pages/InvestorReporting/fixtures/smoke/dsgn-irptv1-cottonwood.json'
const fixtures = JSON.parse(readFileSync(FIXTURE_PATH, 'utf8'))
const fixtureKeys = Object.keys(fixtures).sort((a, b) => b.length - a.length)
const matchFixture = (url) => fixtureKeys.find((key) => url.includes(key))

console.log('STEP: launching browser')
const browser = await chromium.launch({ executablePath: EDGE, headless: true })
console.log('STEP: browser launched')
const page = await browser.newPage({ viewport: { width: 1440, height: 900 } })
const netlog = []
page.on('requestfinished', async (req) => {
  const res = await req.response().catch(() => null)
  netlog.push([req.method(), res ? res.status() : 'NO-RESPONSE', req.url()].join('\t'))
})
page.on('pageerror', (e) => console.log('PAGE-CRASH:', String(e).slice(0, 300)))

await page.route('**/*', async (r) => {
  const req = r.request()
  const url = req.url()
  if (req.method() === 'OPTIONS' && !url.startsWith(ORIGIN)) return r.fulfill({ status: 204, headers: CORS, body: '' })
  const fk = matchFixture(url)
  if (fk) return r.fulfill({ status: 200, headers: CORS, body: JSON.stringify(fixtures[fk]) })
  if (url.includes('/auth/refresh')) return r.fulfill({ status: 200, headers: CORS, body: JSON.stringify(SESSION) })
  return r.continue()
})

console.log('STEP: routing registered, navigating')
await page.goto(ORIGIN + '/investor-reporting', { waitUntil: 'networkidle', timeout: 30000 })
  .catch((e) => console.log('goto:', e.message.split('\n')[0]))
console.log('STEP: navigated')
await page.waitForTimeout(2000)
console.log('STEP: post-load wait done')

let selectOk = false
try {
  const combo = page.getByRole('combobox', { name: 'Client search' })
  await combo.click()
  await page.waitForTimeout(500)
  const option = page.getByRole('option', { name: /Cottonwood Trust/ })
  await option.waitFor({ state: 'visible', timeout: 5000 })
  await option.click()
  selectOk = true
  console.log('SELECTED: Cottonwood Trust')
} catch (e) {
  console.log('SELECT-FAIL:', e.message.split('\n')[0])
}
await page.waitForTimeout(3000)

let holdingsOk = false
try {
  await page.getByRole('button', { name: 'Holdings', exact: true }).or(page.getByRole('tab', { name: 'Holdings' })).first().click()
  holdingsOk = true
  console.log('CLICKED: Holdings tab')
} catch (e) {
  console.log('HOLDINGS-CLICK-FAIL:', e.message.split('\n')[0])
}
await page.waitForTimeout(2500)

const state = await page.evaluate(() => ({
  text: document.body.innerText.replace(/\s+/g, ' ').slice(0, 400),
  identityCard: document.querySelectorAll('[data-slot="identity-card"], [data-slot="identity-who"]').length,
  securityRows: document.querySelectorAll('[data-slot="security-row"]').length,
  headlineTiles: document.querySelectorAll('[data-slot="headline-tile"]').length,
}))
console.log('SELECT-OK:', selectOk)
console.log('STATE:', JSON.stringify(state))

const routesHit = new Set(netlog.map((l) => l.split('\t')[2]).filter((u) => fixtureKeys.some((k) => u.includes(k))))
const matched = fixtureKeys.filter((k) => [...routesHit].some((u) => u.includes(k)))
console.log(`DRIVER-FIXTURES-MATCH: matched ${matched.length} of ${fixtureKeys.length}`)
if (matched.length < fixtureKeys.length) {
  console.log('DRIVER-FIXTURE-DEAD:', fixtureKeys.filter((k) => !matched.includes(k)).join(' | '))
}

const ac = await page.evaluate(() => ({
  tiles: [...document.querySelectorAll('[data-slot="treemap-chart"] rect[data-slot="treemap-cell"]')].map((r) => r.getAttribute('fill')),
  legend: [...document.querySelectorAll('[data-slot="treemap-legend"] li')].map((li) => li.getAttribute('data-asset-class')),
  tickerCells: [...document.querySelectorAll('[data-slot="security-ticker"]')].map((td) => td.textContent + ':' + td.getAttribute('data-asset-class')),
}))
console.log('ASSET-CLASS:', JSON.stringify(ac))
await page.screenshot({ path: OUT, fullPage: true })
console.log('SAVED:', OUT)
writeFileSync(OUT.replace(/\.png$/, '.netlog.tsv'), netlog.join('\n') + '\n')

await browser.close()
