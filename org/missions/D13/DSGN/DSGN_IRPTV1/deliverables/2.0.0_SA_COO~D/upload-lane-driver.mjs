/**
 * TEMPLATE UPLOAD LANE real run (2.0.0_SA_COO~Y BLOCKER 100869; spec
 * org/tier1_exec/2.0.0_SA_COO/deliverables/IRPT_MVP_Y/D_UPLOAD_TEMPLATE_LANE_SPEC_20260924.md): the Analysis tab's
 * prospect upload sends file_base64 + file_type, shows "Resolving symbols..." on the first RESOLVING answer, re-POSTs
 * the IDENTICAL body as the poll, and renders the NORMALIZED review. Auth stub, CORS and the dsgn-irptv1 smoke routes are
 * the pinned IVE2 driver's recipe; POST analysis/inputs answers RESOLVING on call 1 and the producer's own normalized
 * fixture (src/pages/InvestorReporting/__tests__/mvp-upload/tests/producer-upload.json) on call 2+.
 *
 * Usage (cwd = the portal checkout): node --input-type=module - <port> <out.png> < upload-lane-driver.mjs
 */
import { chromium } from 'playwright-core'
import { readFileSync, readdirSync } from 'node:fs'

const PORT = process.argv[2] || '5174'
const OUT = process.argv[3] || 'upload-lane.png'
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
const SMOKE_DIR = 'src/pages/InvestorReporting/fixtures/smoke/'
const smokeFile = readdirSync(SMOKE_DIR).find((f) => f.startsWith('dsgn-irptv1-') && f.endsWith('.json'))
const fixtures = JSON.parse(readFileSync(SMOKE_DIR + smokeFile, 'utf8'))
const fixtureKeys = Object.keys(fixtures).sort((a, b) => b.length - a.length)
const producer = JSON.parse(readFileSync('src/pages/InvestorReporting/__tests__/mvp-upload/tests/producer-upload.json', 'utf8'))
const normalized = producer.normalized.response
const resolving = { ...normalized, data: { upload_id: normalized.data.upload_id, input_id: null, state: 'RESOLVING' } }
normalized.data.portfolio.source = { ...(normalized.data.portfolio.source ?? {}), upload_id: normalized.data.upload_id }

const uploadBodies = []
const browser = await chromium.launch({ executablePath: EDGE, headless: true })
const page = await browser.newPage({ viewport: { width: 1440, height: 900 } })
page.on('pageerror', (e) => console.log('PAGE-CRASH:', String(e).slice(0, 300)))
await page.route('**/*', async (r) => {
  const req = r.request()
  const url = req.url()
  if (req.method() === 'OPTIONS' && !url.startsWith(ORIGIN)) return r.fulfill({ status: 204, headers: CORS, body: '' })
  if (url.includes('/auth/refresh')) return r.fulfill({ status: 200, headers: CORS, body: JSON.stringify(SESSION) })
  if (url.includes('/investor-reporting/analysis/inputs') && req.method() === 'POST') {
    uploadBodies.push(req.postData() || '')
    const answer = uploadBodies.length === 1 ? resolving : normalized
    return r.fulfill({ status: 200, headers: CORS, body: JSON.stringify(answer) })
  }
  const fk = fixtureKeys.find((key) => url.includes(key))
  if (fk) return r.fulfill({ status: 200, headers: CORS, body: JSON.stringify(fixtures[fk]) })
  return r.continue()
})

await page.goto(ORIGIN + '/investor-reporting', { waitUntil: 'networkidle', timeout: 30000 }).catch((e) => console.log('goto:', e.message.split('\n')[0]))
await page.waitForTimeout(2000)
await page.getByRole('button', { name: 'Analysis', exact: true }).or(page.getByRole('tab', { name: 'Analysis' })).first().click()
await page.waitForTimeout(1500)
await page.locator('[data-slot="prospect-composer"] input[type="file"]').setInputFiles({
  name: 'template-12.03.csv', mimeType: 'text/csv', buffer: Buffer.from('Ticker,Dollars\nAAPL,10.01\nVNQ,2.02\n'),
})
await page.waitForTimeout(300)
await page.getByRole('button', { name: 'Review portfolio' }).click()
await page.waitForTimeout(800)
const sawResolving = await page.locator('[data-slot="upload-resolving"]').count()
console.log('RESOLVING SHOWN:', sawResolving > 0)
await page.waitForTimeout(4500)
const review = await page.locator('[data-slot="prospect-review"]').count()
const first = uploadBodies[0] ? JSON.parse(uploadBodies[0]) : {}
console.log('UPLOAD CALLS:', uploadBodies.length)
console.log('BODY KEYS:', JSON.stringify(Object.keys(first).sort()), 'file_type:', first.file_type)
console.log('POLL BODY IDENTICAL:', uploadBodies.length >= 2 && uploadBodies[0] === uploadBodies[1])
console.log('NORMALIZED REVIEW SHOWN:', review > 0)
await page.locator('[data-slot="prospect-composer"]').screenshot({ path: OUT })
console.log('SAVED:', OUT)
await browser.close()
