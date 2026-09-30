/**
 * DSGN_IRPTV1 FAST item 36 (W2-07) -- the Generate journey, exercised on the local dev build (5174) on the
 * FIXTURE PLANE: the same auth-stub + CORS + fixture-route recipe the prior real-run drivers use
 * (org/missions/D13/DSGN/DSGN_IRPTV1/deliverables/2.0.0_SA_COO~D/analysis-probe-driver.mjs), extended with
 * stubs for the five operations the press reaches (POST /analysis, GET /analysis/requests, GET
 * /analysis/requests/{id}, GET /status/{id}, GET /analysis/{id}/sections). NOTHING IS WRITTEN TO THE LIVE
 * BACKEND: every scoped route is fulfilled locally. The walk-2 brief's write guard (Generate never pressed
 * live) is kept; Andrew's own smoke is the live press.
 *
 * Usage: node .runtmp/w2-07-generate-journey-driver.mjs <port> <out.png>
 */
import { chromium } from 'playwright-core'
import { readFileSync, writeFileSync, mkdirSync } from 'node:fs'
import { dirname } from 'node:path'

const PORT = process.argv[2] || '5174'
const OUT = process.argv[3] || '.runtmp/w2-07.fast-run.png'
mkdirSync(dirname(OUT), { recursive: true })
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
const BASE = '/api/scoped/investor-reporting'
const cottonwood = JSON.parse(readFileSync('src/pages/InvestorReporting/fixtures/smoke/dsgn-irptv1-cottonwood.json', 'utf8'))
const defaults = JSON.parse(readFileSync('src/pages/InvestorReporting/fixtures/smoke/default.json', 'utf8'))
const firmId = cottonwood[`${BASE}/directory/resolve`].firm_id ?? defaults[`${BASE}/analysis`].firm_id

// The issued identity must satisfy the owned-request parser (`^REQ-[0-9a-f]{24}$`).
const REQ = 'REQ-0123456789abcdef01234567'
const acceptedAt = Math.floor(Date.now() / 1000)
const identity = { tenant_firm_id: firmId, request_id: REQ, revision: 1, immutable: true,
                   ingestion_gate_revision: 'gate-3', destination_policy_revision: 'fdp-11' }
const grant = { count: 0, denominator: 1, kinds: {} }
function env(operation, data, extra = {}) {
  return { contract_version: 'v1', operation, firm_id: firmId, data, unprojected_grant: grant, ...extra }
}
const readyStatus = {
  operation: { operation_id: 'OP-1', operation_kind: 'analysis_request', revision: '1' },
  state: 'READY',
  source_dates: { business_date: '2026-09-29', source_completion_date: '2026-09-29', as_of: '2026-09-30T12:00:00Z' },
  actions: [],
  public_reason_code: 'ANALYSIS_READY',
}
const submitted = JSON.parse(JSON.stringify(defaults[`${BASE}/analysis`]))
submitted.firm_id = firmId
submitted.data.identity = { ...identity }
// The submission envelope keeps the fixture's own `status` block and stage verbatim (the parser refused a hand-typed one: ENVELOPE_STATUS).
const sections = JSON.parse(JSON.stringify(defaults[`${BASE}/analysis/REQ-0001/sections`]))
sections.firm_id = firmId
sections.data.request_ref.request_id = REQ
sections.data.request_ref.request_revision = 1

const fixtures = {
  ...cottonwood,
  // AD-11: the header is search-only (options after typing); the fixture plane answers the search with the browse entries.
  [`${BASE}/directory/search`]: env('directory-search', cottonwood[`${BASE}/directory/browse`].data.entries),
  [`${BASE}/analysis/requests/${REQ}`]: env('analysis-request-read', { identity, accepted_at: acceptedAt }),
  [`${BASE}/analysis/${REQ}/sections`]: sections,
  [`${BASE}/analysis/requests`]: env('analysis-request-history', { items: [{ identity, accepted_at: acceptedAt }], next_cursor: null }),
  [`${BASE}/status/${REQ}`]: env('status-job', readyStatus),
  [`${BASE}/analysis`]: submitted,
}
const fixtureKeys = Object.keys(fixtures).sort((a, b) => b.length - a.length)
const matchFixture = (url) => fixtureKeys.find((key) => url.includes(key))

console.log('STEP: launching browser')
const browser = await chromium.launch({ executablePath: EDGE, headless: true })
const page = await browser.newPage({ viewport: { width: 1440, height: 900 } })
const netlog = []
let postBody = null
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
  if (fk) {
    if (req.method() === 'POST' && fk === `${BASE}/analysis`) postBody = req.postData()
    return r.fulfill({ status: 200, headers: CORS, body: JSON.stringify(fixtures[fk]) })
  }
  if (url.includes('/auth/refresh')) return r.fulfill({ status: 200, headers: CORS, body: JSON.stringify(SESSION) })
  return r.continue()
})

await page.goto(ORIGIN + '/investor-reporting', { waitUntil: 'networkidle', timeout: 30000 })
  .catch((e) => console.log('goto:', e.message.split('\n')[0]))
await page.waitForTimeout(2000)

let selectOk = false
try {
  const combo = page.getByRole('combobox', { name: 'Client search' })
  await combo.click()
  await combo.fill('Cottonwood')
  await page.waitForTimeout(800)
  const option = page.getByRole('option', { name: /Cottonwood Trust/ })
  await option.waitFor({ state: 'visible', timeout: 5000 })
  await option.click()
  selectOk = true
  console.log('SELECTED: Cottonwood Trust')
} catch (e) {
  console.log('SELECT-FAIL:', e.message.split('\n')[0])
}
await page.waitForTimeout(3000)

try {
  await page.getByRole('button', { name: 'Analysis', exact: true }).or(page.getByRole('tab', { name: 'Analysis' })).first().click()
  console.log('CLICKED: Analysis tab')
} catch (e) { console.log('ANALYSIS-CLICK-FAIL:', e.message.split('\n')[0]) }
await page.waitForTimeout(2000)

// Page 1 -> Client card -> page 2 -> Next -> page 3.
try {
  await page.locator('[data-slot="analysis-portfolio-card"][data-portfolio="client"]').click()
  await page.waitForTimeout(600)
  await page.locator('[data-slot="analysis-next"]').click()
  await page.waitForTimeout(600)
  console.log('CLICKED: Client card, Next')
} catch (e) { console.log('FLOW-CLICK-FAIL:', e.message.split('\n')[0]) }

const before = await page.evaluate(() => ({
  rowsBefore: document.querySelectorAll('[data-row="owned-analysis-request"]').length,
  dialogBefore: document.querySelectorAll('[data-slot="owned-request-detail"]').length,
  inlineBefore: (document.querySelector('[data-slot="no-job"], [data-slot="job-state"]') || {}).textContent || null,
}))
console.log('BEFORE:', JSON.stringify(before))

try {
  await page.locator('#ir-composer-recipient').fill('Internal test recipient')
  await page.waitForTimeout(300)
  await page.locator('[data-slot="generate-button"]').click()
  console.log('PRESSED: Generate')
} catch (e) { console.log('GENERATE-FAIL:', e.message.split('\n')[0]) }

// The journey: the dialog opens on the issued request, status in words, then the report sections.
let dialogSeen = false
try {
  await page.locator('[data-slot="owned-request-detail"]').waitFor({ state: 'visible', timeout: 10000 })
  dialogSeen = true
} catch (e) { console.log('DIALOG-WAIT-FAIL:', e.message.split('\n')[0]) }
await page.waitForTimeout(2500)

const after = await page.evaluate((REQ) => {
  const detail = document.querySelector('[data-slot="owned-request-detail"]')
  const status = detail ? detail.querySelector('[role="status"]') : null
  return {
    dialog: Boolean(detail),
    statusWords: status ? status.textContent : null,
    reportSections: detail ? detail.querySelectorAll('[data-slot="owned-report-sections"]').length : 0,
    detailText: detail ? detail.innerText.replace(/\s+/g, ' ').slice(0, 400) : null,
    rowsAfter: document.querySelectorAll('[data-row="owned-analysis-request"]').length,
    newRowListed: Boolean(document.querySelector(`[data-row="owned-analysis-request"][data-request-id="${REQ}"]`)),
    inlineAfter: (document.querySelector('[data-slot="no-job"], [data-slot="job-state"]') || {}).textContent || null,
    rawIdOnDialogFace: detail ? /REQ-[0-9a-f]{24}/.test((detail.innerText || '').replace(/Technical details[\s\S]*$/, '')) : null,
  }
}, REQ)
console.log('AFTER:', JSON.stringify(after))
console.log('POST-BODY:', postBody ? postBody.slice(0, 300) : null)

const hit = (k) => netlog.some((l) => l.split('\t')[2].includes(k))
const routes = {
  post_analysis: netlog.some((l) => l.startsWith('POST\t') && l.includes(`${BASE}/analysis`) && !l.includes('/analysis/')),
  history: hit(`${BASE}/analysis/requests?`) || hit(`${BASE}/analysis/requests`),
  read: hit(`${BASE}/analysis/requests/${REQ}`),
  status: hit(`${BASE}/status/${REQ}`),
  sections: hit(`${BASE}/analysis/${REQ}/sections`),
}
console.log('ROUTES-HIT:', JSON.stringify(routes))
const verdict = selectOk && dialogSeen && after.dialog && after.newRowListed && routes.post_analysis && routes.history && routes.read && routes.status
  ? 'VERDICT: GENERATE-JOURNEY-REAL-OK' : 'VERDICT: GENERATE-JOURNEY-REAL-FAIL'
console.log(verdict)
await page.screenshot({ path: OUT, fullPage: false })
console.log('SAVED:', OUT)
writeFileSync(OUT.replace(/\.png$/, '.netlog.tsv'), netlog.join('\n') + '\n')
await browser.close()
