/**
 * Per-firm ModelPortfolios render for the MDPF_REVAMP.S5 render-check.
 * Based on portal/scripts/ui-smoke.mjs; adds a firm-selector drive (native <select>).
 * usage: node render_firm.mjs <firmId> <out.png> <fixtures.json> [--port 5175]
 */
import { chromium } from 'playwright-core'
import { readFileSync } from 'node:fs'

const [firmId, out, fixturesPath] = process.argv.slice(2)
const port = process.argv.includes('--port') ? process.argv[process.argv.indexOf('--port') + 1] : '5175'
const ORIGIN = `http://localhost:${port}`
const fixtures = JSON.parse(readFileSync(fixturesPath, 'utf8'))
const EDGE = 'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe'
const CORS = {
  'Access-Control-Allow-Origin': ORIGIN, 'Access-Control-Allow-Credentials': 'true',
  'Access-Control-Allow-Headers': '*', 'Access-Control-Allow-Methods': '*', 'Content-Type': 'application/json',
}
const SESSION = { accessToken: 'ui-smoke-token', user: { email: 'dev@opalinvest.dev', name: 'Dev User', role: 'admin',
  userType: 'Dev', firmId: 'opal-capital', firmRole: null, advisorId: null, advisorRole: null, mustChangePassword: false } }

const browser = await chromium.launch({ executablePath: EDGE, headless: true })
const page = await browser.newPage({ viewport: { width: 1440, height: 900 } })
page.on('pageerror', e => console.log('PAGE-CRASH:', String(e).slice(0, 300)))
const fixtureKeys = Object.keys(fixtures).sort((a, b) => b.length - a.length)
await page.route('**/*', r => {
  const req = r.request(); const url = req.url()
  if (req.method() === 'OPTIONS' && !url.startsWith(ORIGIN)) return r.fulfill({ status: 204, headers: CORS, body: '' })
  const fk = fixtureKeys.find(k => url.includes(k))
  if (fk) return r.fulfill({ status: 200, headers: CORS, body: JSON.stringify(fixtures[fk]) })
  if (url.includes('/auth/refresh')) return r.fulfill({ status: 200, headers: CORS, body: JSON.stringify(SESSION) })
  return r.continue()
})
await page.goto(ORIGIN + '/portfolios', { waitUntil: 'networkidle', timeout: 30000 }).catch(e => console.log('goto:', e.message.split('\n')[0]))
await page.waitForTimeout(2000)
// Drive the firm selector (native <select> that carries the firm option).
if (firmId && firmId !== 'global') {
  try {
    await page.selectOption(`select:has(option[value="${firmId}"])`, firmId)
    console.log('SELECTED firm:', firmId)
  } catch (e) { console.log('SELECT-FAIL:', e.message.split('\n')[0]) }
  await page.waitForTimeout(2500)
}
if (process.argv.includes('--count')) {
  try {
    await page.getByRole('button', { name: 'Count', exact: true }).first().click()
    console.log('CLICKED Count toggle')
  } catch (e) { console.log('COUNT-CLICK-FAIL:', e.message.split('\n')[0]) }
  await page.waitForTimeout(2500)
}
await page.waitForTimeout(2000)
const state = await page.evaluate(() => ({ loc: window.location.pathname,
  text: document.body.innerText.replace(/\s+/g, ' ').slice(0, 200) }))
console.log('LOC   :', state.loc)
console.log('TEXT  :', state.text)
await page.screenshot({ path: out, fullPage: true })
console.log('SAVED :', out)
await browser.close()
