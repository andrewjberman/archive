/**
 * MDPF_REVAMP.S5 flip-gate CHECKPOINT-2 -- POST-flip verify-before-serve on the REAL distro.
 * PER-FIRM, PER-PROCESS (fresh page each invocation -> no multi-firm state churn; matches the
 * per-firm methodology that renders inflection's bell curve clean). Real token, real-distro
 * passthrough (dev proxy -> the post-flip live CF -> assets). Captures each /api/general URL's
 * status+content-type+parse (404-catch) AND waits until the Client-Holdings bell-curve area path
 * is POPULATED before screenshot (CTO's NAMED inflection must-render check).
 *
 * env: TEST_TOKEN=<accessToken>  OR  TEST_EMAIL/TEST_PASSWORD
 *      HEADED=1 (optional -> headed browser for the definitive real-browser confirmation)
 * usage: node checkpoint2.mjs <firm> <out.png> [--count] [--port 5175]
 */
import { chromium } from 'playwright-core'

const [firm, out] = process.argv.slice(2).filter(a => !a.startsWith('--'))
const count = process.argv.includes('--count')
const port = process.argv.includes('--port') ? process.argv[process.argv.indexOf('--port') + 1] : '5175'
const ORIGIN = `http://localhost:${port}`
const EDGE = 'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe'
const CF = 'https://d2n2nzpeqf34ge.cloudfront.net'  // real distro (public prod domain; dev proxy target)
const CORS = { 'Access-Control-Allow-Origin': ORIGIN, 'Access-Control-Allow-Credentials': 'true',
  'Access-Control-Allow-Headers': '*', 'Access-Control-Allow-Methods': '*' }

let TOKEN = process.env.TEST_TOKEN || '', USER = null
if (!TOKEN && process.env.TEST_EMAIL && process.env.TEST_PASSWORD) {
  const r = await fetch(`${CF}/auth/login`, { method: 'POST', headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email: process.env.TEST_EMAIL, password: process.env.TEST_PASSWORD }) })
  const t = await r.text()
  try { const d = JSON.parse(t); TOKEN = d.accessToken || d.access_token || ''; USER = d.user || null
        console.log('LOGIN:', r.status, TOKEN ? 'token acquired' : 'NO TOKEN: ' + t.slice(0,120)) }
  catch { console.log('LOGIN parse-fail:', r.status, t.slice(0,120)) }
}
if (!TOKEN) { console.log('NO TOKEN -- set TEST_TOKEN or TEST_EMAIL/TEST_PASSWORD. Aborting.'); process.exit(2) }
const SESSION = { accessToken: TOKEN, user: USER || { email: 'dev@opalinvest.dev', name: 'Dev User', role: 'admin',
  userType: 'Dev', firmId: 'opal-capital', firmRole: null, advisorId: null, advisorRole: null, mustChangePassword: false } }

const EXPECTED = [
  'mdpf/global/aggregate-aua-timeseries.json', 'mdpf/49financial/aggregate-aua-timeseries.json',
  'mdpf/inflection/aggregate-aua-timeseries.json', 'portfolios/aum-metrics.json',
  'portfolios/aum-timeseries.json', 'portfolios/non_model_assets.json',
  'portfolios/account-distribution.json', 'mdpf/49financial/account-distribution.json',
  'mdpf/inflection/account-distribution.json',
]
const seen = new Map()

const browser = await chromium.launch({ executablePath: EDGE, headless: !process.env.HEADED })
const page = await browser.newPage({ viewport: { width: 1440, height: 900 } })
page.on('pageerror', e => console.log('PAGE-CRASH:', String(e).slice(0, 300)))
await page.addInitScript(tok => { try { localStorage.setItem('accessToken', tok) } catch {} }, TOKEN)

await page.route('**/*', r => {
  const req = r.request(); const url = req.url()
  if (req.method() === 'OPTIONS' && !url.startsWith(ORIGIN)) return r.fulfill({ status: 204, headers: CORS, body: '' })
  if (url.includes('/auth/refresh') || url.endsWith('/auth/me'))
    return r.fulfill({ status: 200, headers: { ...CORS, 'Content-Type': 'application/json' }, body: JSON.stringify(SESSION) })
  return r.continue()  // /api/general/* -> dev proxy -> real post-flip CF, carrying the real Bearer
})
page.on('response', async resp => {
  const frag = EXPECTED.find(f => resp.url().includes(f)); if (!frag) return
  const ctype = (resp.headers()['content-type'] || '').split(';')[0]
  let parses = false, len = 0, head = ''
  try { const t = await resp.text(); len = t.length; head = t.slice(0,60).replace(/\s+/g,' '); try { JSON.parse(t); parses = true } catch {} } catch {}
  seen.set(frag, { status: resp.status(), ctype, parses, len, head })
})

await page.goto(ORIGIN + '/portfolios', { waitUntil: 'networkidle', timeout: 30000 }).catch(e => console.log('goto:', e.message.split('\n')[0]))
await page.waitForTimeout(2000)
// ALWAYS re-select the firm (incl global) + ALWAYS set the toggle explicitly.
try { await page.selectOption(`select:has(option[value="${firm}"])`, firm) } catch (e) { console.log('SELECT-FAIL', e.message.split('\n')[0]) }
await page.waitForTimeout(2500)
try { await page.getByRole('button', { name: count ? 'Count' : 'Value', exact: true }).first().click() } catch (e) { console.log('TOGGLE-FAIL', e.message.split('\n')[0]) }
await page.waitForLoadState('networkidle').catch(() => {})
// NAMED must-check (HINT -- my visual read of the screenshot is authoritative per CTO):
// wait until the CLIENT-HOLDINGS bell-curve area path is populated, SCOPED to that panel
// (the daily-trend is also an AreaChart, so an unscoped check would false-positive).
let bellPopulated = false
try {
  await page.waitForFunction(() => {
    // find the "Client Holdings" heading, climb to its panel, check for a populated area path within.
    const hdr = [...document.querySelectorAll('*')].find(e => e.childElementCount === 0 && /^\s*Client Holdings/i.test(e.textContent || ''))
    if (!hdr) return false
    let panel = hdr
    for (let i = 0; i < 10 && panel.parentElement; i++) { panel = panel.parentElement; if (panel.querySelector('svg.recharts-surface path.recharts-area-area, svg.recharts-surface path.recharts-area-curve')) break }
    const paths = [...panel.querySelectorAll('path.recharts-area-area, path.recharts-area-curve')]
    return paths.some(p => (p.getAttribute('d') || '').length > 60)
  }, { timeout: 12000 })
  bellPopulated = true
} catch { bellPopulated = false }
await page.waitForTimeout(2500)  // generous settle so the area finishes animating before screenshot
const loc = await page.evaluate(() => window.location.pathname)
console.log(`FIRM=${firm} MODE=${count ? 'count' : 'value'} LOC=${loc}${loc.includes('login') ? ' <-- AUTH REDIRECT' : ''} BELL_CURVE_POPULATED=${bellPopulated}`)
await page.screenshot({ path: out, fullPage: true }).catch(() => {})
console.log('SAVED', out)
for (const frag of EXPECTED) { const r = seen.get(frag); if (r) {
  const bad = r.status !== 200 || r.ctype !== 'application/json' || !r.parses
  console.log(`  ${bad ? 'FAIL' : 'OK  '} ${r.status} ${r.ctype} parse=${r.parses} bytes=${r.len} ${frag}${bad ? '  <<< ' + r.head : ''}`) } }
await browser.close()
