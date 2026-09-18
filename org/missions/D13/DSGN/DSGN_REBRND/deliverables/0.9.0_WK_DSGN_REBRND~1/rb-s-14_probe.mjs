// rb14-probe.mjs -- attribution of three extractor findings (ran from <WS>/.scratch/; the deliverables copy is committed as evidence, comment-only difference):
// which elements render Inter, which carry an 8px radius (on the band or not), and what paints the
// most frequent green/red text on /market. Same stub/fixtures as rb14-harness.mjs.
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
  const res = await page.evaluate(() => {
    const rendered = (el) => { const s = getComputedStyle(el); if (s.display === 'none' || s.visibility === 'hidden' || s.opacity === '0') return false; const r = el.getBoundingClientRect(); return r.width > 0 && r.height > 0 }
    const label = (el) => el.tagName.toLowerCase() + (typeof el.className === 'string' && el.className.trim() ? '.' + el.className.trim().split(/\s+/).slice(0, 5).join('.') : (el.className && el.className.baseVal ? '.' + el.className.baseVal.split(/\s+/).slice(0, 3).join('.') : ''))
    const BAND = 'rgb(10, 23, 51)'
    const bandOf = (el) => { for (let n = el; n; n = n.parentElement) { const b = getComputedStyle(n).backgroundColor; if (b && b !== 'rgba(0, 0, 0, 0)' && b !== 'transparent') return b } return 'none' }
    const inter = new Map(), r8 = new Map(), txt = new Map()
    let r8Total = 0, r8OnBand = 0, r8Self = 0
    for (const el of document.body.querySelectorAll('*')) {
      if (!rendered(el)) continue
      const s = getComputedStyle(el)
      const fam = (s.fontFamily || '').split(',')[0].replace(/['"]/g, '').trim()
      if (fam === 'Inter') { const k = label(el) + ' | ' + (el.textContent || '').trim().slice(0, 24); inter.set(k, (inter.get(k) || 0) + 1) }
      if (/(^|\s)8px/.test(s.borderRadius)) {
        r8Total++
        const own = s.backgroundColor, ground = bandOf(el)
        if (own === BAND) r8Self++
        if (ground === BAND) r8OnBand++
        const k = label(el) + ' | bg ' + own + ' | ground ' + ground
        r8.set(k, (r8.get(k) || 0) + 1)
      }
      const t = Array.from(el.childNodes).filter(n => n.nodeType === 3).map(n => n.textContent).join('').trim()
      if (t && (s.color === 'rgb(45, 206, 137)' || s.color === 'rgb(245, 54, 92)')) {
        const k = s.color + ' | ' + label(el); txt.set(k, (txt.get(k) || 0) + 1)
      }
    }
    const top = (m, n) => Array.from(m.entries()).sort((a, b) => b[1] - a[1]).slice(0, n)
    return { inter: top(inter, 12), interTotal: Array.from(inter.values()).reduce((a, b) => a + b, 0),
      r8Total, r8Self, r8OnBand, r8: top(r8, 10), txt: top(txt, 6) }
  })
  console.log(`=== ${route}`)
  console.log(' INTER total', res.interTotal); for (const r of res.inter) console.log('   ', JSON.stringify(r))
  console.log(' RADIUS-8 total', res.r8Total, 'own-bg band', res.r8Self, 'nearest-ground band', res.r8OnBand); for (const r of res.r8) console.log('   ', JSON.stringify(r))
  console.log(' ARGON-TEXT'); for (const r of res.txt) console.log('   ', JSON.stringify(r))
  await page.close()
}
await browser.close()
