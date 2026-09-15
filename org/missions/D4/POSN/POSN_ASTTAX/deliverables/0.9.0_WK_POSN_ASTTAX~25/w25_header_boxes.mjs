/**
 * POSN_ASTTAX.TO-W2-1 (slot ~25) -- MEASURE THE TWO PANEL HEADERS' LAYOUT.
 *
 * Reading the PNG showed the Portfolio Composition header's left block squeezed against
 * the eight-satellite button strip. A screenshot shows THAT something is wrong; this
 * prints the BOXES, so the claim is a number rather than an impression: the left block's
 * width, the timestamp's box, the actions' box, and whether the two rectangles intersect.
 *
 * Usage (from portal/): node <this> --port <p> --fixtures <f.json> [--mode satellites]
 */
import { createRequire } from 'node:module'
import { readFileSync } from 'node:fs'
const require = createRequire(process.cwd() + '/package.json')
const { chromium } = require('playwright-core')

const args = process.argv.slice(2)
const argOf = (n, d) => (args.includes(n) ? args[args.indexOf(n) + 1] : d)
const port = argOf('--port', '5175')
const mode = argOf('--mode', 'satellites')
const fixtures = JSON.parse(readFileSync(argOf('--fixtures', null), 'utf8'))
const ORIGIN = `http://localhost:${port}`
const EDGE = 'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe'
const CORS = {
  'Access-Control-Allow-Origin': ORIGIN, 'Access-Control-Allow-Credentials': 'true',
  'Access-Control-Allow-Headers': '*', 'Access-Control-Allow-Methods': '*',
  'Content-Type': 'application/json',
}
const SESSION = { accessToken: 'ui-smoke-token',
  user: { email: 'dev@opalcapital.com', name: 'Dev User', role: 'admin', userType: 'Dev',
          firmId: 'opal-capital', firmRole: null, advisorId: null, advisorRole: null,
          mustChangePassword: false } }
const keys = Object.keys(fixtures).sort((a, b) => b.length - a.length)
const browser = await chromium.launch({ executablePath: EDGE, headless: true })
const page = await browser.newPage({ viewport: { width: 1440, height: 900 } })
await page.route('**/*', (r) => {
  const url = r.request().url()
  if (r.request().method() === 'OPTIONS' && !url.startsWith(ORIGIN)) return r.fulfill({ status: 204, headers: CORS, body: '' })
  const k = keys.find((key) => url.includes(key))
  if (k) return r.fulfill({ status: 200, headers: CORS, body: JSON.stringify(fixtures[k]) })
  if (url.includes('/auth/refresh')) return r.fulfill({ status: 200, headers: CORS, body: JSON.stringify(SESSION) })
  return r.continue()
})
await page.goto(ORIGIN + '/positioning', { waitUntil: 'networkidle', timeout: 30000 }).catch(() => {})
await page.waitForTimeout(3500)
if (mode === 'satellites') {
  await page.getByRole('button', { name: 'Satellites', exact: true }).first().click()
  await page.waitForTimeout(2500)
}
const boxes = await page.evaluate(() => {
  const clean = (s) => (s || '').replace(/\s+/g, ' ').trim()
  return Array.from(document.querySelectorAll('div.rounded-t-lg')).map((h) => {
    const kids = Array.from(h.children)
    const left = kids[0], right = kids[1]
    const r = (e) => (e ? e.getBoundingClientRect() : null)
    const stamp = h.querySelector('div.text-\\[10px\\]') || null
    const box = (e) => { const b = r(e); return b ? { x: Math.round(b.x), w: Math.round(b.width), right: Math.round(b.right), h: Math.round(b.height) } : null }
    const lb = box(left), rb = box(right), sb = box(stamp)
    return {
      text: clean(h.innerText).slice(0, 90),
      headerHeight: Math.round(r(h).height),
      left: lb, actions: rb, timestamp: sb,
      timestampText: clean(stamp ? stamp.innerText : ''),
      overlapLeftActions: lb && rb ? Math.max(0, lb.right - rb.x) : null,
      overlapStampActions: sb && rb ? Math.max(0, sb.right - rb.x) : null,
    }
  })
})
console.log('MODE:', mode)
for (const b of boxes) console.log(JSON.stringify(b))
await browser.close()
