/**
 * MODELS DIALOG real run (Andrew-direct 2026-09-24 ~19:4xZ design notes, Holdings): the Total Assets -> model dialog
 * lists its securities in ONE column with each dot the canonical asset-class colour. Auth stub, CORS and fixture routing
 * are the pinned IVE2 driver's recipe; the fixture path is argv[4].
 *
 * Usage (cwd = the portal checkout): node --input-type=module - <port> <out.png> <fixture.json> < models-dialog-probe-driver.mjs
 */
import { chromium } from 'playwright-core'
import { readFileSync } from 'node:fs'

const PORT = process.argv[2] || '5174'
const OUT = process.argv[3] || 'models-dialog.png'
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
const fixtures = JSON.parse(readFileSync(process.argv[4], 'utf8'))
const fixtureKeys = Object.keys(fixtures).sort((a, b) => b.length - a.length)

const browser = await chromium.launch({ executablePath: EDGE, headless: true })
const page = await browser.newPage({ viewport: { width: 1440, height: 900 } })
page.on('pageerror', (e) => console.log('PAGE-CRASH:', String(e).slice(0, 300)))
await page.route('**/*', async (r) => {
  const req = r.request()
  const url = req.url()
  if (req.method() === 'OPTIONS' && !url.startsWith(ORIGIN)) return r.fulfill({ status: 204, headers: CORS, body: '' })
  if (url.includes('/auth/refresh')) return r.fulfill({ status: 200, headers: CORS, body: JSON.stringify(SESSION) })
  const fk = fixtureKeys.find((key) => url.includes(key))
  if (fk) return r.fulfill({ status: 200, headers: CORS, body: JSON.stringify(fixtures[fk]) })
  return r.continue()
})

await page.goto(ORIGIN + '/investor-reporting', { waitUntil: 'networkidle', timeout: 30000 }).catch((e) => console.log('goto:', e.message.split('\n')[0]))
await page.waitForTimeout(2000)
await page.getByRole('combobox', { name: 'Client search' }).click()
await page.waitForTimeout(500)
await page.getByRole('option', { name: /Cottonwood Trust/ }).first().click()
await page.waitForTimeout(2500)
await page.getByRole('button', { name: 'Holdings', exact: true }).or(page.getByRole('tab', { name: 'Holdings' })).first().click()
await page.waitForTimeout(2500)
const drill = await page.evaluate(() => ({
  legend: [...document.querySelectorAll('.recharts-legend-item-text')].map((e) => e.textContent),
  rows: [...document.querySelectorAll('[data-slot="slice-row"]')].map((tr) => tr.querySelector('[data-slot="slice-label"]')?.textContent),
  affordances: document.querySelectorAll('[data-slot="slice-drill-affordance"]').length,
  crumbs: (document.querySelector('[data-slot="holdings-breadcrumbs"]') || {}).innerText || null,
}))
console.log('DRILL:', JSON.stringify(drill))
await page.screenshot({ path: OUT, fullPage: true })
console.log('SAVED:', OUT)
await browser.close()
