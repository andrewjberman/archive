/**
 * P0 EXERCISE (CTO ask #1): HEADED hover of the two colliding "Apr 30" bars on the Global
 * Period-End (Value, Monthly) chart. Confirms/refutes the INFERRED recharts mis-binding:
 * does hovering the 2026 bar resolve a 2025 tooltip date (and/or a summed Total)?
 *
 * usage: HEADED=1 node hover_apr30.mjs <fixtures.json> <outdir> [--port 5175] [--bars 5,17]
 */
import { chromium } from 'playwright-core'
import { readFileSync } from 'node:fs'

const args = process.argv.slice(2)
const [fixturesPath, outdir] = args.filter(a => !a.startsWith('--'))
const port = args.includes('--port') ? args[args.indexOf('--port') + 1] : '5175'
const targets = (args.includes('--bars') ? args[args.indexOf('--bars') + 1] : '5,17').split(',').map(Number)
const ORIGIN = `http://localhost:${port}`
const fixtures = JSON.parse(readFileSync(fixturesPath, 'utf8'))
const EDGE = 'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe'
const CORS = { 'Access-Control-Allow-Origin': ORIGIN, 'Access-Control-Allow-Credentials': 'true',
  'Access-Control-Allow-Headers': '*', 'Access-Control-Allow-Methods': '*', 'Content-Type': 'application/json' }
const SESSION = { accessToken: 'repro-token', user: { email: 'dev@opalinvest.dev', name: 'Dev User', role: 'admin',
  userType: 'Dev', firmId: 'opal-capital', firmRole: null, advisorId: null, advisorRole: null, mustChangePassword: false } }

const browser = await chromium.launch({ executablePath: EDGE, headless: !process.env.HEADED })
console.log('MODE:', process.env.HEADED ? 'HEADED (real visible browser)' : 'headless')
const page = await browser.newPage({ viewport: { width: 1600, height: 1000 } })
const keys = Object.keys(fixtures).sort((a, b) => b.length - a.length)
await page.route('**/*', r => {
  const req = r.request(); const url = req.url()
  if (req.method() === 'OPTIONS' && !url.startsWith(ORIGIN)) return r.fulfill({ status: 204, headers: CORS, body: '' })
  const k = keys.find(k => url.includes(k))
  if (k) return r.fulfill({ status: 200, headers: CORS, body: JSON.stringify(fixtures[k]) })
  if (url.includes('/auth/refresh')) return r.fulfill({ status: 200, headers: CORS, body: JSON.stringify(SESSION) })
  return r.continue()
})
await page.goto(ORIGIN + '/portfolios', { waitUntil: 'networkidle', timeout: 30000 }).catch(() => {})
await page.waitForTimeout(4500)

await page.evaluate(() => {
  for (const svg of document.querySelectorAll('svg.recharts-surface'))
    if (svg.querySelectorAll('g.recharts-bar-rectangle').length > 5) { svg.scrollIntoView({ block: 'center' }); return }
})
await page.waitForTimeout(1500)

const bars = await page.evaluate(() => {
  let svg = null
  for (const s of document.querySelectorAll('svg.recharts-surface'))
    if (s.querySelectorAll('g.recharts-bar-rectangle').length > 5) { svg = s; break }
  if (!svg) return []
  const cols = new Map()
  for (const r of svg.querySelectorAll('g.recharts-bar-rectangle path, g.recharts-bar-rectangle rect')) {
    const b = r.getBoundingClientRect()
    if (!b.width || !b.height) continue
    const cx = Math.round(b.x + b.width / 2)
    const p = cols.get(cx) || { cx, top: Infinity, bottom: -Infinity }
    p.top = Math.min(p.top, b.y); p.bottom = Math.max(p.bottom, b.y + b.height)
    cols.set(cx, p)
  }
  return [...cols.values()].sort((a, b) => a.cx - b.cx)
})
console.log('bar columns:', bars.length)

async function readTip() {
  return await page.evaluate(() => {
    const w = document.querySelector('.recharts-tooltip-wrapper')
    const cands = [w, ...document.querySelectorAll('[class*="tooltip"],[class*="Tooltip"]')].filter(Boolean)
    for (const el of cands) {
      const t = (el.innerText || '').replace(/\s+/g, ' ').trim()
      if (t) return { text: t, cls: el.className?.toString?.().slice(0, 60) }
    }
    return w ? { text: '', cls: 'wrapper-empty', html: w.outerHTML.slice(0, 200) } : null
  })
}

for (const idx of targets) {
  const b = bars[idx]
  if (!b) { console.log(`bar[${idx}] MISSING`); continue }
  const cy = (b.top + b.bottom) / 2
  // jiggle so recharts registers a real mousemove
  await page.mouse.move(b.cx - 3, cy); await page.waitForTimeout(120)
  await page.mouse.move(b.cx, cy);     await page.waitForTimeout(450)
  const tip = await readTip()
  console.log(`\n--- hovered bar[${idx}] x=${b.cx} ---`)
  console.log('   tooltip:', tip ? (tip.text || `(empty) ${tip.html || ''}`) : '(no tooltip element)')
  await page.screenshot({ path: `${outdir}/hover_bar${idx}.png` }).catch(() => {})
}
await page.waitForTimeout(500)
await browser.close()
