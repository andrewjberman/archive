/**
 * MDPF_REVAMP.S5 flip-gate LIVE-URL 404-catch against AE's THROWAWAY serving-target.
 * The app shell loads from the dev server (:5175); the 9 DATA URLs are intercepted and
 * fetched server-side from the THROWAWAY distro (real CF -> L@E /api/general->/json ->
 * assets/OAC), carrying the real Bearer. Each response's status + content-type + parse is
 * captured (the 404->CF-text/html->blank-chart seam), and the bytes are fulfilled to the
 * browser so we ALSO confirm it RENDERS clean through the real serving-path shape.
 *
 * env: THROWAWAY=https://<dist>.cloudfront.net  (AE-provided throwaway origin)
 *      TEST_TOKEN=<accessToken>   OR   TEST_EMAIL/TEST_PASSWORD (mints via THROWAWAY/auth/login)
 *      SHOTDIR=<dir> (optional; per-firm render PNGs)
 * usage: THROWAWAY=... TEST_TOKEN=... node catch404_throwaway.mjs [--port 5175]
 */
import { chromium } from 'playwright-core'

const port = process.argv.includes('--port') ? process.argv[process.argv.indexOf('--port') + 1] : '5175'
const ORIGIN = `http://localhost:${port}`
const EDGE = 'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe'
const THROWAWAY = (process.env.THROWAWAY || '').replace(/\/$/, '')
const SHOTDIR = process.env.SHOTDIR || '.'
if (!THROWAWAY) { console.log('NO THROWAWAY origin -- set THROWAWAY=https://<dist>.cloudfront.net. Aborting.'); process.exit(2) }
const CORS = { 'Access-Control-Allow-Origin': ORIGIN, 'Access-Control-Allow-Credentials': 'true',
  'Access-Control-Allow-Headers': '*', 'Access-Control-Allow-Methods': '*' }

// ---- real token ----
let TOKEN = process.env.TEST_TOKEN || '', USER = null
if (!TOKEN && process.env.TEST_EMAIL && process.env.TEST_PASSWORD) {
  const r = await fetch(`${THROWAWAY}/auth/login`, { method: 'POST', headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email: process.env.TEST_EMAIL, password: process.env.TEST_PASSWORD }) })
  const t = await r.text()
  try { const d = JSON.parse(t); TOKEN = d.accessToken || d.access_token || ''; USER = d.user || null
        console.log('LOGIN:', r.status, TOKEN ? 'token acquired' : 'NO TOKEN: ' + t.slice(0,120)) }
  catch { console.log('LOGIN parse-fail:', r.status, t.slice(0,120)) }
}
// Token OPTIONAL: the throwaway may have NO auth-edge (CTO 012310Z) -> unauthed GET returns JSON.
// If no real token, use a stub for the app SHELL only (so /portfolios loads) and node-fetch the
// throwaway WITHOUT a Bearer. A real token, if provided, is carried on the node-fetch too.
const SHELL_TOKEN = TOKEN || 'throwaway-shell-token'
console.log('AUTH MODE:', TOKEN ? 'real Bearer on throwaway fetch' : 'NO Bearer (throwaway unauthed) + stub app-shell session')
const SESSION = { accessToken: SHELL_TOKEN, user: USER || { email: 'dev@opalinvest.dev', name: 'Dev User', role: 'admin',
  userType: 'Dev', firmId: 'opal-capital', firmRole: null, advisorId: null, advisorRole: null, mustChangePassword: false } }

const EXPECTED = [
  'mdpf/global/aggregate-aua-timeseries.json', 'mdpf/49financial/aggregate-aua-timeseries.json',
  'mdpf/inflection/aggregate-aua-timeseries.json', 'portfolios/aum-metrics.json',
  'portfolios/aum-timeseries.json', 'portfolios/non_model_assets.json',
  'portfolios/account-distribution.json', 'mdpf/49financial/account-distribution.json',
  'mdpf/inflection/account-distribution.json',
]
const seen = new Map()

const browser = await chromium.launch({ executablePath: EDGE, headless: true })
const page = await browser.newPage({ viewport: { width: 1440, height: 900 } })
page.on('pageerror', e => console.log('PAGE-CRASH:', String(e).slice(0, 300)))
await page.addInitScript(tok => { try { localStorage.setItem('accessToken', tok) } catch {} }, SHELL_TOKEN)

await page.route('**/*', async r => {
  const req = r.request(); const url = req.url()
  if (req.method() === 'OPTIONS' && !url.startsWith(ORIGIN)) return r.fulfill({ status: 204, headers: CORS, body: '' })
  if (url.includes('/auth/refresh') || url.endsWith('/auth/me'))
    return r.fulfill({ status: 200, headers: { ...CORS, 'Content-Type': 'application/json' }, body: JSON.stringify(SESSION) })
  const frag = EXPECTED.find(f => url.includes(f))
  if (frag) {
    // server-side fetch from the THROWAWAY real serving path (CF -> L@E -> assets), with Bearer.
    try {
      const resp = await fetch(`${THROWAWAY}/api/general/${frag}`, { headers: TOKEN ? { 'Authorization': `Bearer ${TOKEN}` } : {} })
      const ctype = (resp.headers.get('content-type') || '').split(';')[0]
      const body = await resp.text()
      let parses = false; try { JSON.parse(body); parses = true } catch {}
      if (!seen.has(frag)) seen.set(frag, { status: resp.status, ctype, parses, len: body.length, head: body.slice(0, 60).replace(/\s+/g,' ') })
      return r.fulfill({ status: resp.status, headers: { ...CORS, 'Content-Type': ctype || 'application/json' }, body })
    } catch (e) {
      if (!seen.has(frag)) seen.set(frag, { status: 0, ctype: 'ERR', parses: false, len: 0, head: String(e).slice(0,60) })
      return r.fulfill({ status: 502, headers: { ...CORS, 'Content-Type': 'application/json' }, body: '{}' })
    }
  }
  return r.continue()
})

async function drive(firm, count, tag) {
  if (firm !== 'global') { try { await page.selectOption(`select:has(option[value="${firm}"])`, firm) } catch {} }
  await page.waitForTimeout(3000)                                   // per-firm node-fetch (throwaway CF) + paint
  await page.waitForLoadState('networkidle').catch(() => {})
  // ALWAYS set the toggle explicitly (segmented Value|Count) -- do not rely on prior state.
  try { await page.getByRole('button', { name: count ? 'Count' : 'Value', exact: true }).first().click() } catch (e) { console.log('TOGGLE-FAIL', tag, e.message.split('\n')[0]) }
  await page.waitForTimeout(3000)
  await page.waitForLoadState('networkidle').catch(() => {})
  await page.screenshot({ path: `${SHOTDIR}/tw_${tag}.png`, fullPage: true }).catch(() => {})
}

await page.goto(ORIGIN + '/portfolios', { waitUntil: 'networkidle', timeout: 30000 }).catch(e => console.log('goto:', e.message.split('\n')[0]))
await page.waitForTimeout(2500)
const loc = await page.evaluate(() => window.location.pathname)
console.log('LOC   :', loc, loc.includes('login') ? ' <-- AUTH REDIRECT (token rejected by throwaway)' : '')
// inflection FIRST (freshest network state -> its bell-curve area chart settles before screenshot).
await drive('inflection', false, 'inflection_value'); await drive('inflection', true, 'inflection_count')
await drive('49financial', false, '49f_value'); await drive('49financial', true, '49f_count')
await drive('global', false, 'global_value'); await drive('global', true, 'global_count')
await page.waitForTimeout(1000)

console.log('\n===== LIVE-URL 404-CATCH vs THROWAWAY', THROWAWAY, '=====')
let fail = 0
for (const frag of EXPECTED) {
  const r = seen.get(frag)
  if (!r) { console.log(`  MISS  (never fetched)  ${frag}`); fail++; continue }
  const bad = r.status !== 200 || r.ctype !== 'application/json' || !r.parses
  if (bad) fail++
  console.log(`  ${bad ? 'FAIL' : 'OK  '}  ${r.status} ${r.ctype} parse=${r.parses} bytes=${r.len}  ${frag}${bad ? '  <<< ' + r.head : ''}`)
}
console.log(`\nVERDICT: ${fail === 0 ? 'PASS -- all 9 throwaway URLs resolve to revamp JSON (200 application/json parseable); render PNGs in ' + SHOTDIR : 'FAIL -- ' + fail + ' url(s) 404/HTML/miss (CF-error-mask)'}`)
await browser.close()
