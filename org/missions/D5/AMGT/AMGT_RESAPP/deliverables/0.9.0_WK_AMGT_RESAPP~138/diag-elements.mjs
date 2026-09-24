/**
 * diag-elements.mjs -- ONE-OFF diagnostic (not part of the contract check), to locate the
 * source of weight/size/radius/shadow/band/purple offenders on a given route. Prints element
 * tag, className, and a text sample for each offending element. Deleted before the cell closes
 * if not needed; kept under deliverables as working evidence.
 *
 *   node diag-elements.mjs <route> [--port 5182] [--click "<name>"]...
 */
import { chromium } from 'playwright-core'
import { readFileSync } from 'node:fs'

const args = process.argv.slice(2)
let route = args[0]
route = '/' + route.replace(/^\/+/, '')
const port = args.includes('--port') ? args[args.indexOf('--port') + 1] : '5182'
const fixturesPath = 'src/pages/SecurityAnalysis/__harness__/tests/uiContractFixtures.json'
const fixtures = JSON.parse(readFileSync(fixturesPath, 'utf8'))
const clicks = args.reduce((acc, a, i) => (a === '--click' && args[i + 1] ? [...acc, args[i + 1]] : acc), [])
const ORIGIN = `http://localhost:${port}`
const EDGE = 'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe'
const CORS = { 'Access-Control-Allow-Origin': ORIGIN, 'Access-Control-Allow-Credentials': 'true',
  'Access-Control-Allow-Headers': '*', 'Access-Control-Allow-Methods': '*', 'Content-Type': 'application/json' }
const SESSION = { accessToken: 'ui-smoke-token', user: { email: 'dev@opalcapital.com', name: 'Dev User', role: 'admin',
  userType: 'Dev', firmId: 'opal-capital', firmRole: null, advisorId: null, advisorRole: null, mustChangePassword: false } }
const fkeys = Object.keys(fixtures).sort((a, b) => b.length - a.length)
const matchFixture = url => fkeys.find(k => url.includes(k))

const browser = await chromium.launch({ executablePath: EDGE, headless: true })
const page = await browser.newPage({ viewport: { width: 1440, height: 900 } })
await page.route('**/*', async r => {
  const req = r.request(); const url = req.url()
  if (req.method() === 'OPTIONS' && !url.startsWith(ORIGIN)) return r.fulfill({ status: 204, headers: CORS, body: '' })
  const fk = matchFixture(url)
  if (fk) return r.fulfill({ status: 200, headers: CORS, body: JSON.stringify(fixtures[fk]) })
  if (url.includes('/auth/refresh')) return r.fulfill({ status: 200, headers: CORS, body: JSON.stringify(SESSION) })
  return r.continue()
})
await page.goto(ORIGIN + route, { waitUntil: 'networkidle', timeout: 30000 }).catch(() => {})
await page.waitForTimeout(3000)
for (const name of clicks) {
  try { await page.getByRole('tab', { name, exact: true }).first().click({ timeout: 2000 }) }
  catch { try { await page.getByRole('button', { name, exact: true }).first().click({ timeout: 2000 }) } catch {} }
  await page.waitForTimeout(2500)
}

const report = await page.evaluate(() => {
  const vis = el => { const r = el.getBoundingClientRect(); const cs = getComputedStyle(el); return r.width > 0 && r.height > 0 && cs.display !== 'none' && cs.visibility !== 'hidden' }
  const parse = s => { const x = /rgba?\(([^)]+)\)/.exec(s || ''); if (!x) return null; const p = x[1].split(',').map(v => parseFloat(v)); return { r: p[0], g: p[1], b: p[2], a: p.length > 3 ? p[3] : 1 } }
  const isBand = c => c && Math.abs(c.r - 10) < 3 && Math.abs(c.g - 23) < 3 && Math.abs(c.b - 51) < 3
  const all = Array.from(document.body.querySelectorAll('*')).filter(vis)
  const desc = el => {
    let cur = el; const chain = []
    for (let i = 0; i < 4 && cur; i++) { chain.unshift(cur.tagName + (cur.id ? '#' + cur.id : '') + (cur.className && typeof cur.className === 'string' ? '.' + cur.className.split(' ').slice(0, 2).join('.') : '')); cur = cur.parentElement }
    return chain.join(' > ')
  }
  const out = { weight300: [], weight500: [], weight600: [], size10: [], radius8: [], shadowHits: [], bandTop: [], purple: [] }
  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT)
  let n
  while ((n = walker.nextNode())) {
    const t = n.textContent.replace(/\s+/g, ' ').trim(); if (!t) continue
    const el = n.parentElement; if (!el || !vis(el)) continue
    const cs = getComputedStyle(el)
    const w = cs.fontWeight; const sz = Math.round(parseFloat(cs.fontSize))
    if (w === '300' && out.weight300.length < 15) out.weight300.push({ text: t.slice(0, 40), path: desc(el) })
    if (w === '500' && out.weight500.length < 15) out.weight500.push({ text: t.slice(0, 40), path: desc(el) })
    if (w === '600' && out.weight600.length < 15) out.weight600.push({ text: t.slice(0, 40), path: desc(el) })
    if (sz === 10 && out.size10.length < 15) out.size10.push({ text: t.slice(0, 40), path: desc(el) })
  }
  for (const el of all) {
    const cs = getComputedStyle(el)
    const r = cs.borderTopLeftRadius
    if (r === '8px' && out.radius8.length < 15) out.radius8.push({ path: desc(el), text: (el.innerText || '').slice(0, 30) })
    if (cs.boxShadow && cs.boxShadow !== 'none' && out.shadowHits.length < 10) out.shadowHits.push({ path: desc(el), shadow: cs.boxShadow.slice(0, 60) })
    const bg = parse(cs.backgroundColor)
    if (bg && bg.a > 0 && Math.abs(bg.r - 95) < 4 && Math.abs(bg.g - 59) < 4 && Math.abs(bg.b - 227) < 4 && out.purple.length < 10) out.purple.push({ path: desc(el), text: (el.innerText || '').slice(0, 30) })
  }
  const bandEls = all.filter(el => { const bg = parse(getComputedStyle(el).backgroundColor); return bg && bg.a > 0 && isBand(bg) })
  const bandTop = bandEls.filter(el => !bandEls.some(o => o !== el && o.contains(el)))
  out.bandTop = bandTop.slice(0, 10).map(el => ({ path: desc(el) }))
  return out
})
console.log(JSON.stringify(report, null, 1))
await browser.close()
