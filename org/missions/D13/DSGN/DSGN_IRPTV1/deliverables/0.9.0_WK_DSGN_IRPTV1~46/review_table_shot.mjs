/**
 * review_table_shot.mjs -- DSGN_IRPTV1 TO-IV-e-83 AMENDMENT 3 (worker 0.9.0_WK_DSGN_IRPTV1~46).
 *
 * A live screenshot of the upload review table, rendered from a vite BUILD (no dev server, no port bound, no network),
 * copying portal/scripts/ui-smoke.mjs's pattern: system Edge, a fresh headless profile (chromium.launch's own throwaway one), the stubbed /auth/refresh session exactly as ui-smoke builds it, the build served from
 * disk by portal/scripts/ui-dist.mjs, and every non-stubbed REMOTE request aborted and logged.
 *
 * Usage: node review_table_shot.mjs <dist dir> <out dir> <tag>
 *
 * Synthetic content only: three tickers (APPL, FBIFX, MSFT) and round synthetic dollars. Fixture bodies:
 *   - POST .../directory/resolve : portal/src/pages/InvestorReporting/tests/opal-scope/server-wire.json `context` (the actual
 *       Global wire the Entry served: context_kind GLOBAL, two READY firms), with the two tenant names (and registry_tenant)
 *       renamed to the synthetic firm-alpha / firm-beta so no real firm name reaches a PNG. Every other field is as sourced.
 *   - POST .../analysis/inputs   : the NORMALIZED envelope + portfolio skeleton of
 *       portal/src/pages/InvestorReporting/__tests__/mvp-upload/tests/producer-upload.json (normalized.response), with the rows,
 *       holdings and disclosures.corrections set to the shape the pin upload-review-corrected-holding.test.tsx builds.
 *   - POST .../auth/refresh      : ui-smoke's SESSION object (internal Dev admin).
 * Every other request the page makes gets no fixture: a same-origin API read answers 404 (ui-dist) and is logged.
 */
import { readFileSync, mkdirSync } from 'node:fs'
import { join } from 'node:path'
import { pathToFileURL } from 'node:url'

const PORTAL = 'C:/dev/wk-dsgn-irptv1-46/portal'
const { chromium } = await import(pathToFileURL(PORTAL + '/node_modules/playwright-core/index.mjs').href)
const { serveFromDist } = await import(pathToFileURL(PORTAL + '/scripts/ui-dist.mjs').href)

const [DIST, OUT, TAG = 'run'] = process.argv.slice(2)
if (!DIST || !OUT) { console.error('usage: node review_table_shot.mjs <dist dir> <out dir> <tag>'); process.exit(2) }
mkdirSync(OUT, { recursive: true })

const ORIGIN = 'http://localhost:5175' // never bound: every request to it is answered from disk
const ROUTE = '/investor-reporting'
const EDGE = 'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe'
const CORS = {
  'Access-Control-Allow-Origin': ORIGIN, 'Access-Control-Allow-Credentials': 'true',
  'Access-Control-Allow-Headers': '*', 'Access-Control-Allow-Methods': '*', 'Content-Type': 'application/json',
}
// ui-smoke's SESSION, verbatim (internal Dev admin; the route needs admin + internal + dev).
const SESSION = {
  accessToken: 'ui-smoke-token',
  user: { email: 'dev@opalcapital.com', name: 'Dev User', role: 'admin',
          userType: 'Dev', firmId: 'opal-capital', firmRole: null, advisorId: null,
          advisorRole: null, mustChangePassword: false },
}

const IR = PORTAL + '/src/pages/InvestorReporting'
const RESOLVE_BODY = JSON.parse(readFileSync(IR + '/tests/opal-scope/server-wire.json', 'utf8').split('49financial').join('firm-alpha').split('inflection').join('firm-beta')).context
const producer = JSON.parse(readFileSync(IR + '/__tests__/mvp-upload/tests/producer-upload.json', 'utf8'))

// The review result, built as the pin builds it (upload-review-corrected-holding.test.tsx): v2 rows, three of them.
const row = (symbol, securityId, dollars, n) => ({
  original: { symbol, amount: dollars, basis: 'USD', row: n, cells: { A: { text: symbol }, B: { text: dollars } } },
  security_id: securityId, analysis_dollars: dollars, price: null, provider_receipt_sha256: 'a'.repeat(64),
})
const response = JSON.parse(JSON.stringify(producer.normalized.response))
response.data.portfolio = {
  ...response.data.portfolio,
  schema_version: 'irpt-normalized-portfolio.v2', basis: 'USD', valuation_basis: 'INPUT_VALUES', reference_notional: null,
  rows: [row('APPL', 'AAPL', '5700', 2), row('FBIFX', 'SGOV', '900', 3), row('MSFT', 'MSFT', '250', 4)],
  holdings: { identity_kind: 'YCHARTS_SECURITY', unit: 'dollars', total_dollars: '6850', rows: [] }, findings: [],
  disclosures: { corrections: [
    { finding_code: 'TICKER_NOT_FOUND', from_value: 'APPL', to_value: 'AAPL', approved_by: 'principal-synthetic' },
    { finding_code: 'NO_PRICE_HISTORY', from_value: 'FBIFX', to_value: 'SGOV', approved_by: 'principal-synthetic' },
  ] },
}
const CSV = 'Ticker,Dollars\r\nAPPL,5700\r\nFBIFX,900\r\nMSFT,250\r\n'

const stubbed = []   // { url, source }
const aborted = []   // remote requests aborted
const unfixtured = [] // same-origin API reads with no fixture (answered 404 by ui-dist)
const served = { n: 0 }
let uploadBody = null

// As ui-smoke: chromium.launch gives a fresh, throwaway profile of its own (never a shared one).
const browser = await chromium.launch({ executablePath: EDGE, headless: true })
const page = await browser.newPage({ viewport: { width: 1440, height: 900 } })
page.on('pageerror', (e) => console.log('PAGE-CRASH:', String(e).slice(0, 300)))

await page.route('**/*', async (r) => {
  const req = r.request()
  const url = req.url()
  const method = req.method()
  if (method === 'OPTIONS' && !url.startsWith(ORIGIN)) return r.fulfill({ status: 204, headers: CORS, body: '' })
  if (!url.startsWith(ORIGIN)) { aborted.push(method + ' ' + url); return r.abort('blockedbyclient') }
  const path = new URL(url).pathname
  if (path.includes('/auth/refresh')) {
    stubbed.push({ url: method + ' ' + url, source: 'ui-smoke SESSION stub' })
    return r.fulfill({ status: 200, headers: CORS, body: JSON.stringify(SESSION) })
  }
  if (method === 'POST' && path.endsWith('/analysis/inputs')) {
    uploadBody = req.postData()
    stubbed.push({ url: method + ' ' + url, source: 'producer-upload.json normalized.response, rows/disclosures per the corrected-holding pin' })
    return r.fulfill({ status: 200, headers: CORS, body: JSON.stringify(response) })
  }
  if (method === 'POST' && path.endsWith('/directory/resolve')) {
    stubbed.push({ url: method + ' ' + url, source: 'tests/opal-scope/server-wire.json context (tenants renamed synthetic)' })
    return r.fulfill({ status: 200, headers: CORS, body: JSON.stringify(RESOLVE_BODY) })
  }
  if (/^\/(api|auth)\//.test(path)) unfixtured.push(method + ' ' + url)
  else served.n += 1
  if (await serveFromDist(r, DIST, ORIGIN)) return
  return r.continue()
})

async function names() {
  return page.locator('button,[role=button],[role=tab],select,input').evaluateAll((els) =>
    els.map((e) => e.getAttribute('aria-label') || (e.textContent || '').trim()).filter(Boolean).slice(0, 40))
}
let stoppedAt = null
async function stop(where, err) {
  stoppedAt = where + ': ' + String(err && err.message ? err.message : err).split('\n')[0]
  console.log('STOPPED-AT:', stoppedAt)
  console.log('  (control names on page:', JSON.stringify(await names().catch(() => [])), ')')
}

await page.goto(ORIGIN + ROUTE, { waitUntil: 'networkidle', timeout: 30000 }).catch((e) => console.log('goto:', e.message.split('\n')[0]))
await page.waitForTimeout(2500)
console.log('AFTER-LOAD LOC:', await page.evaluate(() => window.location.pathname))

try {
  await page.getByRole('tab', { name: 'Analysis', exact: true }).or(page.getByRole('button', { name: 'Analysis', exact: true })).first().click({ timeout: 10000 })
  await page.waitForTimeout(1200)
  console.log('CLICKED: Analysis tab')
} catch (e) { await stop('Analysis tab', e) }

if (!stoppedAt) {
  try {
    await page.locator('[data-slot="analysis-portfolio-card"][data-portfolio="prospect"]').click({ timeout: 10000 })
    await page.waitForTimeout(800)
    console.log('CLICKED: Prospect card')
  } catch (e) { await stop('Prospect card', e) }
}

if (!stoppedAt) {
  // An internal principal's card names its firm: choose the first firm offered, if the card is on "Choose a firm".
  const sel = page.locator('[data-slot="prospect-firm-select"]')
  if (await sel.count()) {
    const value = await sel.inputValue()
    const opts = await sel.locator('option').evaluateAll((os) => os.map((o) => [o.value, o.textContent]))
    console.log('FIRM-SELECT value=%s options=%s', JSON.stringify(value), JSON.stringify(opts))
    if (value === '') {
      const first = opts.find((o) => o[0] !== '')
      if (first) { await sel.selectOption(first[0]); console.log('PICKED firm:', first[0]); await page.waitForTimeout(500) }
      else console.log('FIRM-SELECT has no firm to choose')
    }
  } else console.log('FIRM-SELECT: not rendered (card is not in the internal firm-choice mode)')
}

if (!stoppedAt) {
  try {
    await page.locator('[data-slot="upload-dropzone"] input[type="file"]').setInputFiles({ name: 'holdings.csv', mimeType: 'text/csv', buffer: Buffer.from(CSV, 'utf8') })
    await page.waitForTimeout(600)
    await page.getByRole('button', { name: 'Review portfolio', exact: true }).click({ timeout: 10000 })
    console.log('UPLOADED synthetic CSV, pressed Review portfolio')
    await page.locator('[data-slot="prospect-review-rows"] tbody tr').first().waitFor({ state: 'visible', timeout: 15000 })
    await page.waitForTimeout(800)
  } catch (e) { await stop('upload / review table', e) }
}

const state = await page.evaluate(() => ({
  loc: window.location.pathname,
  canvas: getComputedStyle(document.body).backgroundColor,
  text: document.body.innerText.replace(/\s+/g, ' ').slice(0, 160),
}))
const full = join(OUT, `review_table_full_${TAG}.png`)
await page.screenshot({ path: full, fullPage: true })
console.log('SAVED full :', full)
let tablePng = null, regionPng = null
if (!stoppedAt) {
  // Document coordinates (rect + scroll offset): a fullPage clip is in the page's own frame, not the viewport's.
  const box = (sel) => page.evaluate((q) => { const r = document.querySelector(q).getBoundingClientRect(); return { x: r.left + window.scrollX, y: r.top + window.scrollY, width: r.width, height: r.height } }, sel)
  const a = await box('[data-slot="prospect-proxies-used"]')
  const b = await box('[data-slot="prospect-review-rows"]')
  tablePng = join(OUT, `review_table_crop_${TAG}.png`)
  await page.screenshot({ path: tablePng, fullPage: true, clip: { x: b.x - 12, y: b.y - 12, width: b.width + 24, height: b.height + 24 } })
  console.log('SAVED table:', tablePng)
  // The disclosure list sits above the total and the table: one crop from the list's top to the table's bottom.
  regionPng = join(OUT, `review_region_crop_${TAG}.png`)
  await page.screenshot({ path: regionPng, fullPage: true, clip: { x: Math.max(0, a.x - 16), y: a.y - 12, width: Math.max(a.width, b.width) + 32, height: b.y + b.height - a.y + 24 } })
  console.log('SAVED region:', regionPng)
}
const cells = stoppedAt ? [] : await page.locator('[data-slot="prospect-review-rows"] tbody tr').evaluateAll((trs) =>
  trs.map((tr) => [...tr.querySelectorAll('td')].map((td) => td.innerText.replace(/\s+/g, ' ').trim())))
const disclosures = stoppedAt ? [] : await page.locator('[data-slot="prospect-proxies-used"] li').allInnerTexts()
const styles = stoppedAt ? null : await page.evaluate(() => {
  const first = document.querySelector('[data-slot="prospect-review-rows"] tbody tr td')
  const span = first && first.querySelector('span')
  const dollars = document.querySelector('[data-slot="prospect-review-rows"] tbody tr td:nth-child(3)')
  const li = document.querySelector('[data-slot="prospect-proxies-used"] li')
  const g = (el) => el ? (() => { const c = getComputedStyle(el); return { color: c.color, fontSize: c.fontSize, fontVariantNumeric: c.fontVariantNumeric, fontFamily: c.fontFamily.slice(0, 40) } })() : null
  const ground = (el) => { for (let n = el; n; n = n.parentElement) { const bg = getComputedStyle(n).backgroundColor; if (bg && bg !== 'rgba(0, 0, 0, 0)' && bg !== 'transparent') return bg } return null }
  return { holdingCell: g(first), analysedAsSpan: g(span), dollarsCell: g(dollars), disclosureItem: g(li), groundOfCell: ground(first), groundOfDisclosure: ground(li) }
})

console.log('LOC   :', state.loc, state.loc === ROUTE ? '' : ' <-- DID NOT LAND (auth redirect? bad route?)')
console.log('CANVAS:', state.canvas, '(the page field; portal/DESIGN.md C3 = #F4F6FA = rgb(244, 246, 250))')
console.log('TEXT  :', state.text)
console.log('ROWS  :', JSON.stringify(cells))
console.log('DISCLOSURES:', JSON.stringify(disclosures))
console.log('STYLES:', JSON.stringify(styles))
console.log('UPLOAD-REQUEST-BODY-KEYS:', uploadBody ? Object.keys(JSON.parse(uploadBody)).join(',') : '(none sent)')
console.log('STUBBED (%d):', stubbed.length); for (const s of stubbed) console.log('  ', s.url, '<-', s.source)
console.log('ABORTED (%d):', aborted.length); for (const u of aborted) console.log('  ', u)
console.log('UNFIXTURED same-origin API reads, answered 404 by ui-dist (%d):', unfixtured.length); for (const u of unfixtured) console.log('  ', u)
console.log('SERVED FROM DISK (non-API same-origin requests):', served.n)
console.log('STOPPED:', stoppedAt === null ? 'no, review table reached' : stoppedAt)
await browser.close()
