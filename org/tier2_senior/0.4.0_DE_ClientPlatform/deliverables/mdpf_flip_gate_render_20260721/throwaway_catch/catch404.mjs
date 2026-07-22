/**
 * MDPF_REVAMP.S5 flip-gate LIVE-URL 404-catch (real-token render-through).
 * Renders /portfolios with a REAL session token so the 9 data URLs reach the REAL
 * CloudFront serving-target; captures per-URL status + content-type + JSON-parseable,
 * catching the repoint seam (404 -> CF text/html -> silent JSON.parse -> blank chart).
 * Drives all 3 firms x Value/Count so every data URL is exercised.
 *
 * TOKEN (pick one; AE-provided):
 *   TEST_TOKEN=<accessToken>                       # contract-free, preferred
 *   TEST_EMAIL=<e> TEST_PASSWORD=<p>               # harness mints via POST /api/auth/login
 * usage: TEST_TOKEN=... node catch404.mjs [--port 5175]
 */
import { chromium } from 'playwright-core'

const port = process.argv.includes('--port') ? process.argv[process.argv.indexOf('--port') + 1] : '5175'
const ORIGIN = `http://localhost:${port}`
const EDGE = 'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe'
const CORS = { 'Access-Control-Allow-Origin': ORIGIN, 'Access-Control-Allow-Credentials': 'true',
  'Access-Control-Allow-Headers': '*', 'Access-Control-Allow-Methods': '*', 'Content-Type': 'application/json' }

// ---- obtain a REAL access token ----
let TOKEN = process.env.TEST_TOKEN || ''
let USER = null
if (!TOKEN && process.env.TEST_EMAIL && process.env.TEST_PASSWORD) {
  const r = await fetch(`https://d2n2nzpeqf34ge.cloudfront.net/auth/login`, {
    method: 'POST', headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email: process.env.TEST_EMAIL, password: process.env.TEST_PASSWORD }),
  })
  const t = await r.text()
  try { const d = JSON.parse(t); TOKEN = d.accessToken || d.access_token || ''; USER = d.user || null
        console.log('LOGIN:', r.status, TOKEN ? 'token acquired' : 'NO TOKEN in response: ' + t.slice(0,120)) }
  catch { console.log('LOGIN parse-fail:', r.status, t.slice(0,120)) }
}
if (!TOKEN) { console.log('NO TOKEN -- set TEST_TOKEN or TEST_EMAIL/TEST_PASSWORD. Aborting.'); process.exit(2) }
const SESSION = { accessToken: TOKEN, user: USER || { email: 'dev@opalinvest.dev', name: 'Dev User', role: 'admin',
  userType: 'Dev', firmId: 'opal-capital', firmRole: null, advisorId: null, advisorRole: null, mustChangePassword: false } }

const EXPECTED = [
  'mdpf/global/aggregate-aua-timeseries.json',
  'mdpf/49financial/aggregate-aua-timeseries.json',
  'mdpf/inflection/aggregate-aua-timeseries.json',
  'portfolios/aum-metrics.json',
  'portfolios/aum-timeseries.json',
  'portfolios/non_model_assets.json',
  'portfolios/account-distribution.json',
  'mdpf/49financial/account-distribution.json',
  'mdpf/inflection/account-distribution.json',
]

const seen = new Map()
const browser = await chromium.launch({ executablePath: EDGE, headless: true })
const page = await browser.newPage({ viewport: { width: 1440, height: 900 } })
page.on('pageerror', e => console.log('PAGE-CRASH:', String(e).slice(0, 300)))
// Seed the REAL token into localStorage before any app script runs.
await page.addInitScript(tok => { try { localStorage.setItem('accessToken', tok) } catch {} }, TOKEN)

// Stub ONLY auth (refresh/me) with the REAL session so mount-refresh (no cookie) can't
// log us out; let every /api/general data URL hit the real proxy carrying the real Bearer.
await page.route('**/*', r => {
  const req = r.request(); const url = req.url()
  if (req.method() === 'OPTIONS' && !url.startsWith(ORIGIN)) return r.fulfill({ status: 204, headers: CORS, body: '' })
  if (url.includes('/auth/refresh') || url.endsWith('/auth/me')) return r.fulfill({ status: 200, headers: CORS, body: JSON.stringify(SESSION) })
  return r.continue()
})

page.on('response', async resp => {
  const url = resp.url()
  const frag = EXPECTED.find(f => url.includes(f))
  if (!frag) return
  const ctype = (resp.headers()['content-type'] || '').split(';')[0]
  let bodyHead = '', parses = false, len = 0
  try { const t = await resp.text(); len = t.length; bodyHead = t.slice(0, 60).replace(/\s+/g, ' '); try { JSON.parse(t); parses = true } catch {} } catch {}
  seen.set(frag, { status: resp.status(), ctype, bodyHead, parses, len })
})

async function drive(firm, count) {
  if (firm !== 'global') { try { await page.selectOption(`select:has(option[value="${firm}"])`, firm) } catch {} ; await page.waitForTimeout(2000) }
  if (count) { try { await page.getByRole('button', { name: 'Count', exact: true }).first().click() } catch {} ; await page.waitForTimeout(1500) }
}

await page.goto(ORIGIN + '/portfolios', { waitUntil: 'networkidle', timeout: 30000 }).catch(e => console.log('goto:', e.message.split('\n')[0]))
await page.waitForTimeout(2500)
const loc = await page.evaluate(() => window.location.pathname)
console.log('LOC   :', loc, loc.includes('login') ? ' <-- AUTH REDIRECT (token rejected)' : '')
for (const firm of ['global', '49financial', 'inflection']) { await drive(firm, false); await drive(firm, true) }
await page.waitForTimeout(1500)

console.log('\n===== LIVE-URL 404-CATCH (serving-target) =====')
let fail = 0
for (const frag of EXPECTED) {
  const r = seen.get(frag)
  if (!r) { console.log(`  MISS  (never fetched)  ${frag}`); fail++; continue }
  const bad = r.status !== 200 || r.ctype !== 'application/json' || !r.parses
  if (bad) fail++
  console.log(`  ${bad ? 'FAIL' : 'OK  '}  ${r.status} ${r.ctype} parse=${r.parses} bytes=${r.len}  ${frag}${bad ? '  <<< ' + r.bodyHead : ''}`)
}
console.log(`\nVERDICT: ${fail === 0 ? 'PASS -- all 9 serving URLs 200 application/json parseable via real token' : 'FAIL -- ' + fail + ' url(s) 404/HTML/miss (CF-error-mask risk)'}`)
await page.screenshot({ path: process.env.SHOT || 'catch404_final.png', fullPage: true }).catch(() => {})
await browser.close()
