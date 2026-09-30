/**
 * DSGN_IRPTV1 FAST item 40 (W2-01 front residue) -- on the Performance tab a served DEPENDENCY_UNAVAILABLE refusal
 * that carries a business date names the missing upstream day, and the picker option reads 'unavailable', never
 * 'pending', once the figure has answered. Fixture plane on the local dev build (same recipe as items 36-39; nothing
 * reaches the live backend): the Cottonwood performance fixture's status block is rewritten to the walk's COT shape
 * (UNAVAILABLE / DEPENDENCY_UNAVAILABLE / business_date 2026-09-22).
 *
 * Usage: node .runtmp/w2-01-refusal-driver.mjs <port> <out.png>
 */
import { chromium } from 'playwright-core'
import { readFileSync, writeFileSync, mkdirSync } from 'node:fs'
import { dirname } from 'node:path'

const PORT = process.argv[2] || '5174'
const OUT = process.argv[3] || '.runtmp/w2-01.fast-run.png'
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
const MISSING_DAY = '2026-09-22'
const cottonwood = JSON.parse(readFileSync('src/pages/InvestorReporting/fixtures/smoke/dsgn-irptv1-cottonwood.json', 'utf8'))
const firmId = cottonwood[`${BASE}/directory/resolve`].firm_id
const perfKey = Object.keys(cottonwood).find((k) => k.includes('/performance/'))
const refused = JSON.parse(JSON.stringify(cottonwood[perfKey]))
refused.status = { ...refused.status, state: 'UNAVAILABLE', public_reason_code: 'DEPENDENCY_UNAVAILABLE',
  source_dates: { ...(refused.status.source_dates ?? {}), business_date: MISSING_DAY } }
const fixtures = {
  ...cottonwood,
  [perfKey]: refused,
  [`${BASE}/directory/search`]: { contract_version: 'v1', operation: 'directory-search', firm_id: firmId,
    data: cottonwood[`${BASE}/directory/browse`].data.entries, unprojected_grant: { count: 0, denominator: 1, kinds: {} } },
}
const fixtureKeys = Object.keys(fixtures).sort((a, b) => b.length - a.length)
const matchFixture = (url) => fixtureKeys.find((key) => url.includes(key))
console.log('PERFORMANCE FIXTURE status ->', JSON.stringify(refused.status))

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
try { await page.getByRole('button', { name: 'Performance', exact: true }).or(page.getByRole('tab', { name: 'Performance' })).first().click(); console.log('CLICKED: Performance tab') } catch (e) { console.log('PERF-CLICK:', e.message.split('\n')[0]) }
await page.waitForTimeout(4000)

const read = await page.evaluate(() => {
  const texts = []
  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT)
  let node
  while ((node = walker.nextNode())) { const t = node.textContent.trim(); if (t.length > 0) texts.push(t) }
  const refusal = texts.filter((t) => /temporarily unavailable/i.test(t))
  const options = [...document.querySelectorAll('select option')].map((o) => o.textContent.trim())
  return { refusal, options, pendingOptions: options.filter((o) => /pending/i.test(o)), unavailableOptions: options.filter((o) => /unavailable/i.test(o)) }
})
console.log('REFUSAL LINES:', JSON.stringify(read.refusal))
console.log('PICKER OPTIONS:', JSON.stringify(read.options))
const namesDay = read.refusal.some((t) => /September 22nd, 2026/.test(t))
const verdict = selectOk && read.refusal.length >= 1 && namesDay && read.pendingOptions.length === 0 && read.unavailableOptions.length >= 1
  ? 'VERDICT: NAMED-MISSING-DAY-REAL-OK' : 'VERDICT: NAMED-MISSING-DAY-REAL-FAIL'
console.log(`names the day=${namesDay}; pending options=${read.pendingOptions.length}; unavailable options=${read.unavailableOptions.length}`)
console.log(verdict)
await page.screenshot({ path: OUT, fullPage: false })
console.log('SAVED:', OUT)
writeFileSync(OUT.replace(/\.png$/, '.netlog.tsv'), netlog.join('\n') + '\n')
await browser.close()
