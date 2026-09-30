/**
 * DSGN_IRPTV1 FAST item 38 (W2-19) -- every footer on the Holdings tab reads the same source words, no module or
 * function name on the face. Fixture plane on the local dev build (same recipe as item 36's driver; nothing reaches
 * the live backend). Reads every "Source:" line on the tab, opens the card's first tile to read the dialog's stamp,
 * screenshots, prints a verdict.
 *
 * Usage: node .runtmp/w2-19-footer-driver.mjs <port> <out.png>
 */
import { chromium } from 'playwright-core'
import { readFileSync, writeFileSync, mkdirSync } from 'node:fs'
import { dirname } from 'node:path'

const PORT = process.argv[2] || '5174'
const OUT = process.argv[3] || '.runtmp/w2-19.fast-run.png'
const TAB = process.argv[4] || 'Holdings'
mkdirSync(dirname(OUT), { recursive: true })
const ORIGIN = `http://localhost:${PORT}`
const EDGE = 'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe'
const CORS = {
  'Access-Control-Allow-Origin': ORIGIN, 'Access-Control-Allow-Credentials': 'true',
  'Access-Control-Allow-Headers': '*', 'Access-Control-Allow-Methods': '*', 'Content-Type': 'application/json',
}
const SESSION = {
  accessToken: 'ui-smoke-token',
  user: { email: 'dev@opalcapital.com', name: 'Dev User', role: 'admin', userType: 'Dev', firmId: 'opal-capital',
          firmRole: null, advisorId: null, advisorRole: null, mustChangePassword: false },
}
const BASE = '/api/scoped/investor-reporting'
const cottonwood = JSON.parse(readFileSync('src/pages/InvestorReporting/fixtures/smoke/dsgn-irptv1-cottonwood.json', 'utf8'))
const firmId = cottonwood[`${BASE}/directory/resolve`].firm_id
const fixtures = {
  ...cottonwood,
  [`${BASE}/directory/search`]: { contract_version: 'v1', operation: 'directory-search', firm_id: firmId,
    data: cottonwood[`${BASE}/directory/browse`].data.entries, unprojected_grant: { count: 0, denominator: 1, kinds: {} } },
}
const fixtureKeys = Object.keys(fixtures).sort((a, b) => b.length - a.length)
const matchFixture = (url) => fixtureKeys.find((key) => url.includes(key))
const holdingsKey = fixtureKeys.find((k) => k.includes('/holdings/'))
// FAST item 41: optional vendor keys injected into the holdings fixture (argv[5], comma list) so the served-words path renders.
const VENDOR_KEYS = (process.argv[5] || '').split(',').filter(Boolean)
if (VENDOR_KEYS.length > 0 && holdingsKey) { fixtures[holdingsKey] = JSON.parse(JSON.stringify(fixtures[holdingsKey])); fixtures[holdingsKey].data.source_vendor_keys = VENDOR_KEYS; console.log('INJECTED source_vendor_keys:', JSON.stringify(VENDOR_KEYS)) }
const servedCoordinates = [...new Set((fixtures[holdingsKey]?.data?.nodes ?? []).map((n) => n?.provenance?.source_coordinate).filter(Boolean))]
console.log('SERVED source_coordinate values on the fixture:', JSON.stringify(servedCoordinates), '| source_vendor_keys:', JSON.stringify(fixtures[holdingsKey]?.data?.source_vendor_keys ?? null))

const browser = await chromium.launch({ executablePath: EDGE, headless: true })
const page = await browser.newPage({ viewport: { width: 1440, height: 900 } })
const netlog = []
page.on('requestfinished', async (req) => {
  const res = await req.response().catch(() => null)
  netlog.push([req.method(), res ? res.status() : 'NO-RESPONSE', req.url()].join('\t'))
})
page.on('pageerror', (e) => console.log('PAGE-CRASH:', String(e).slice(0, 300)))
await page.route('**/*', async (r) => {
  const req = r.request(); const url = req.url()
  if (req.method() === 'OPTIONS' && !url.startsWith(ORIGIN)) return r.fulfill({ status: 204, headers: CORS, body: '' })
  const fk = matchFixture(url)
  if (fk) return r.fulfill({ status: 200, headers: CORS, body: JSON.stringify(fixtures[fk]) })
  if (url.includes('/auth/refresh')) return r.fulfill({ status: 200, headers: CORS, body: JSON.stringify(SESSION) })
  return r.continue()
})
await page.goto(ORIGIN + '/investor-reporting', { waitUntil: 'networkidle', timeout: 30000 }).catch((e) => console.log('goto:', e.message.split('\n')[0]))
await page.waitForTimeout(1500)
let selectOk = false
try {
  const combo = page.getByRole('combobox', { name: 'Client search' })
  await combo.click(); await combo.fill('Cottonwood'); await page.waitForTimeout(800)
  const option = page.getByRole('option', { name: /Cottonwood Trust/ })
  await option.waitFor({ state: 'visible', timeout: 5000 }); await option.click(); selectOk = true
  console.log('SELECTED: Cottonwood Trust')
} catch (e) { console.log('SELECT-FAIL:', e.message.split('\n')[0]) }
await page.waitForTimeout(3000)
try { await page.getByRole('button', { name: TAB, exact: true }).or(page.getByRole('tab', { name: TAB })).first().click(); console.log('CLICKED: ' + TAB + ' tab') } catch (e) { console.log('HOLDINGS-CLICK:', e.message.split('\n')[0]) }
await page.waitForTimeout(2500)

const readSources = () => page.evaluate(() => {
  const out = []
  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT)
  let node
  while ((node = walker.nextNode())) {
    const t = node.textContent.trim()
    if (/^Source:/.test(t)) out.push(t)
  }
  return out
})
const pageSources = await readSources()
console.log('SOURCE LINES ON THE TAB:', JSON.stringify(pageSources))

// The card: open the first tile so the dialog's stamp (footer) renders.
let dialogSources = []
try {
  const tile = page.locator('[data-slot="holdings-card"] [role="button"], [data-slot="category-view-tree"] [role="button"], [data-slot="holdings-card"] button').first()
  await tile.waitFor({ state: 'visible', timeout: 5000 }); await tile.click(); await page.waitForTimeout(1200)
  dialogSources = (await readSources()).filter((s) => !pageSources.includes(s))
  console.log('SOURCE LINES ADDED BY THE OPENED CARD DIALOG:', JSON.stringify(dialogSources), '(dialog sources equal to a page line are counted in the page set)')
} catch (e) { console.log('CARD-OPEN:', e.message.split('\n')[0]) }
const all = [...pageSources, ...dialogSources]
const distinct = [...new Set(all)]
const functionNamed = all.filter((s) => /\w+\.\w+\./.test(s) || /\bbuild_/.test(s))
const coordinateOnFace = all.filter((s) => servedCoordinates.some((c) => s.includes(c)))
console.log('DISTINCT SOURCE STRINGS:', JSON.stringify(distinct), '| function-named:', functionNamed.length, '| served coordinate on the face:', coordinateOnFace.length)
const verdict = selectOk && all.length >= (TAB === 'Holdings' ? 2 : 1) && distinct.length === 1 && functionNamed.length === 0 && coordinateOnFace.length === 0
  ? 'VERDICT: FOOTER-SOURCE-REAL-OK' : 'VERDICT: FOOTER-SOURCE-REAL-FAIL'
console.log(verdict)
await page.screenshot({ path: OUT, fullPage: true })
console.log('SAVED:', OUT)
writeFileSync(OUT.replace(/\.png$/, '.netlog.tsv'), netlog.join('\n') + '\n')
await browser.close()
