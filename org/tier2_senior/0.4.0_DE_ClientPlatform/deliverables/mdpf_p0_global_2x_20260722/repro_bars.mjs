/**
 * P0 REPRO (no hover): measure the rendered Global Period-End bars.
 * Extracts each bar column's stacked pixel height + the YAxis tick scale -> implied $ value,
 * and dumps the x-axis tick labels. Answers: do the BARS render ~2x / misaligned, or are only
 * the LABELS/tooltip ambiguous (duplicate year-less category keys)?
 * usage: node repro_bars.mjs <fixtures.json> <outdir> [--port 5175]
 */
import { chromium } from 'playwright-core'
import { readFileSync } from 'node:fs'

const [fixturesPath, outdir] = process.argv.slice(2).filter(a => !a.startsWith('--'))
const port = process.argv.includes('--port') ? process.argv[process.argv.indexOf('--port') + 1] : '5175'
const ORIGIN = `http://localhost:${port}`
const fixtures = JSON.parse(readFileSync(fixturesPath, 'utf8'))
const EDGE = 'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe'
const CORS = { 'Access-Control-Allow-Origin': ORIGIN, 'Access-Control-Allow-Credentials': 'true',
  'Access-Control-Allow-Headers': '*', 'Access-Control-Allow-Methods': '*', 'Content-Type': 'application/json' }
const SESSION = { accessToken: 'repro-token', user: { email: 'dev@opalinvest.dev', name: 'Dev User', role: 'admin',
  userType: 'Dev', firmId: 'opal-capital', firmRole: null, advisorId: null, advisorRole: null, mustChangePassword: false } }

const browser = await chromium.launch({ executablePath: EDGE, headless: true })
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
await page.waitForTimeout(4000)

const out = await page.evaluate(() => {
  const surfaces = [...document.querySelectorAll('svg.recharts-surface')]
  let svg = null
  for (const s of surfaces) if (s.querySelectorAll('g.recharts-bar-rectangle').length > 5) { svg = s; break }
  if (!svg) return { err: 'no bar chart' }
  const sb = svg.getBoundingClientRect()

  // x-axis tick labels (the category keys as rendered)
  const xLabels = [...svg.querySelectorAll('g.recharts-xAxis text, g.recharts-cartesian-axis.recharts-xAxis text')]
    .map(t => t.textContent.trim()).filter(Boolean)

  // y-axis ticks -> pixel->value scale
  const yTicks = [...svg.querySelectorAll('g.recharts-yAxis text, g.recharts-cartesian-axis.recharts-yAxis text')]
    .map(t => ({ txt: t.textContent.trim(), y: t.getBoundingClientRect().y + t.getBoundingClientRect().height / 2 }))
    .filter(o => o.txt)

  // bar columns: group every bar rect by x-center; stacked total = (maxBottom - minTop)
  const rects = [...svg.querySelectorAll('g.recharts-bar-rectangle path, g.recharts-bar-rectangle rect')]
  const cols = new Map()
  for (const r of rects) {
    const b = r.getBoundingClientRect()
    if (b.width === 0 || b.height === 0) continue
    const cx = Math.round(b.x + b.width / 2)
    const p = cols.get(cx) || { cx, top: Infinity, bottom: -Infinity, segs: 0 }
    p.top = Math.min(p.top, b.y); p.bottom = Math.max(p.bottom, b.y + b.height); p.segs++
    cols.set(cx, p)
  }
  return { xLabels, yTicks, cols: [...cols.values()].sort((a, b) => a.cx - b.cx), svgTop: sb.y, svgH: sb.height }
})

if (out.err) { console.log(out.err); await browser.close(); process.exit(1) }

// build pixel->value scale from the two extreme y ticks
function parseVal(s) {
  const m = String(s).replace(/[$,]/g, '').match(/^([\d.]+)\s*([KMB])?$/i)
  if (!m) return null
  const n = parseFloat(m[1]); const u = (m[2] || '').toUpperCase()
  return n * (u === 'B' ? 1e9 : u === 'M' ? 1e6 : u === 'K' ? 1e3 : 1)
}
const ticks = out.yTicks.map(t => ({ v: parseVal(t.txt), y: t.y })).filter(t => t.v != null)
ticks.sort((a, b) => a.y - b.y)
const hi = ticks[0], lo = ticks[ticks.length - 1]
const perPx = (hi && lo && lo.y !== hi.y) ? (hi.v - lo.v) / (lo.y - hi.y) : null
console.log('Y ticks:', out.yTicks.map(t => t.txt).join(' | '))
console.log('X tick labels (%d):' % 0, out.xLabels.join(' | '))
const dupLabels = out.xLabels.filter((l, i) => out.xLabels.indexOf(l) !== i)
console.log('DUPLICATE x-axis labels rendered:', dupLabels.length ? [...new Set(dupLabels)].join(', ') : 'NONE')
console.log('\n=== rendered bar columns: implied stacked total ($) ===')
console.log('bars:', out.cols.length, ' perPx:', perPx ? perPx.toFixed(0) : 'n/a')
const vals = []
out.cols.forEach((c, i) => {
  const px = c.bottom - c.top
  const v = perPx ? px * perPx : null
  vals.push(v)
  console.log(`  bar[${String(i).padStart(2)}] x=${c.cx} segs=${c.segs} heightPx=${px.toFixed(0)} impliedTotal=${v ? '$' + (v / 1e6).toFixed(0) + 'M' : 'n/a'}`)
})
console.log('\nmonotonic ascending?', vals.every((v, i) => i === 0 || v == null || vals[i - 1] == null || v >= vals[i - 1] * 0.9))
await browser.close()
