// rb14-shadows.mjs -- which elements carry the box-shadows extract.js counted. Ran from <WS>/.scratch/; the deliverables copy is committed as evidence (comment-only difference).
// Same stub/fixtures as rb14-harness.mjs; lists every rendered element whose box-shadow paints (non-zero alpha).
import { readFileSync } from 'node:fs'
import { createRequire } from 'node:module'
const require = createRequire('C:/tmp/wk-dsgn-1j/portal/package.json')
const { chromium } = require('playwright-core')
const FIXDIR = 'C:/tmp/wk-dsgn-1j/portal/.frontend-dev/testing'
const ORIGIN = 'http://localhost:5190'
const CORS = { 'Access-Control-Allow-Origin': ORIGIN, 'Access-Control-Allow-Credentials': 'true',
  'Access-Control-Allow-Headers': '*', 'Access-Control-Allow-Methods': '*', 'Content-Type': 'application/json' }
const SESSION = { accessToken: 'ui-smoke-token', user: { email: 'dev@opalcapital.com', name: 'Dev User', role: 'admin',
  userType: 'Dev', firmId: 'opal-capital', firmRole: null, advisorId: null, advisorRole: null, mustChangePassword: false } }
const ROUTES = [['/market', 'rb-s-9-market.json'], ['/positioning', 'rb-s-9-attribution.json'], ['/portfolio-management', null]]
const browser = await chromium.launch({ executablePath: 'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe', headless: true })
for (const [route, fixture] of ROUTES) {
  const fx = fixture ? JSON.parse(readFileSync(`${FIXDIR}/${fixture}`, 'utf8')) : {}
  const keys = Object.keys(fx).sort((a, b) => b.length - a.length)
  const page = await browser.newPage({ viewport: { width: 1440, height: 900 } })
  await page.route('**/*', r => {
    const req = r.request(); const url = req.url()
    if (req.method() === 'OPTIONS' && !url.startsWith(ORIGIN)) return r.fulfill({ status: 204, headers: CORS, body: '' })
    const k = keys.find(key => url.includes(key))
    if (k) return r.fulfill({ status: 200, headers: CORS, body: JSON.stringify(fx[k]) })
    if (url.includes('/auth/refresh')) return r.fulfill({ status: 200, headers: CORS, body: JSON.stringify(SESSION) })
    return r.continue()
  })
  await page.goto(ORIGIN + route, { waitUntil: 'networkidle', timeout: 30000 }).catch(e => console.log('goto:', e.message.split('\n')[0]))
  await page.waitForTimeout(3000)
  const rows = await page.evaluate(() => {
    const out = []
    for (const el of document.body.querySelectorAll('*')) {
      const s = getComputedStyle(el)
      if (!s.boxShadow || s.boxShadow === 'none') continue
      const r = el.getBoundingClientRect(); if (!(r.width > 0 && r.height > 0)) continue
      // a layer paints if its colour alpha is non-zero
      const layers = s.boxShadow.split(/,(?![^()]*\))/).map(x => x.trim())
      const painting = layers.filter(l => !/rgba\([^)]*,\s*0\)/.test(l))
      if (!painting.length) continue
      const cls = typeof el.className === 'string' ? el.className.trim().split(/\s+/).slice(0, 6).join('.') : ''
      out.push({ el: el.tagName.toLowerCase() + (cls ? '.' + cls : ''), text: (el.textContent || '').trim().replace(/\s+/g, ' ').slice(0, 50),
        painting, box: [Math.round(r.width), Math.round(r.height)] })
    }
    return out
  })
  console.log(`=== ${route}: ${rows.length} rendered element(s) with a painting box-shadow`)
  for (const r of rows) console.log(' ', JSON.stringify(r))
  await page.close()
}
await browser.close()
