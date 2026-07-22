/**
 * STANDING GATE (CTO ask #2, P0 2026-07-22): no two rendered trend bars may resolve to the
 * same category. BEHAVIORAL assertion -- hovers every bar and asserts each resolves to a
 * DISTINCT tooltip date. This is stronger than a DOM key check: it exercises the actual
 * recharts bar<->row binding, which is what broke (a year-less monthly category key over
 * Global's 21-month since-inception window collided 2025/2026 -> the 2026 bar reported the
 * 2025 row: "April 30, 2025 $988M" on a $1.59B bar).
 *
 * usage: node assert_unique_categories.mjs <fixtures.json> [--firm global] [--count] [--port 5175]
 * exit 0 = PASS (all distinct), exit 1 = FAIL (collision)  -> wire into the render-check.
 */
import { chromium } from 'playwright-core'
import { readFileSync } from 'node:fs'

const args = process.argv.slice(2)
const fixturesPath = args.filter(a => !a.startsWith('--'))[0]
const firm = args.includes('--firm') ? args[args.indexOf('--firm') + 1] : 'global'
const count = args.includes('--count')
const port = args.includes('--port') ? args[args.indexOf('--port') + 1] : '5175'
const ORIGIN = `http://localhost:${port}`
const fixtures = JSON.parse(readFileSync(fixturesPath, 'utf8'))
const EDGE = 'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe'
const CORS = { 'Access-Control-Allow-Origin': ORIGIN, 'Access-Control-Allow-Credentials': 'true',
  'Access-Control-Allow-Headers': '*', 'Access-Control-Allow-Methods': '*', 'Content-Type': 'application/json' }
const SESSION = { accessToken: 'gate-token', user: { email: 'dev@opalinvest.dev', name: 'Dev User', role: 'admin',
  userType: 'Dev', firmId: 'opal-capital', firmRole: null, advisorId: null, advisorRole: null, mustChangePassword: false } }

const browser = await chromium.launch({ executablePath: EDGE, headless: !process.env.HEADED })
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
if (firm !== 'global') { try { await page.selectOption(`select:has(option[value="${firm}"])`, firm) } catch {} ; await page.waitForTimeout(2500) }
try { await page.getByRole('button', { name: count ? 'Count' : 'Value', exact: true }).first().click() } catch {}
await page.waitForTimeout(2500)
await page.evaluate(() => {
  for (const svg of document.querySelectorAll('svg.recharts-surface'))
    if (svg.querySelectorAll('g.recharts-bar-rectangle').length > 5) { svg.scrollIntoView({ block: 'center' }); return }
})
await page.waitForTimeout(1200)

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

const seen = []
for (let i = 0; i < bars.length; i++) {
  const b = bars[i], cy = (b.top + b.bottom) / 2
  // multi-candidate read: the custom DataTooltip renders its own class; the bare
  // .recharts-tooltip-wrapper innerText is often EMPTY (this is why the first gate build
  // measured nothing and, before fail-closed, falsely PASSED).
  const readTip = () => page.evaluate(() => {
    const w = document.querySelector('.recharts-tooltip-wrapper')
    const cands = [w, ...document.querySelectorAll('[class*="tooltip"],[class*="Tooltip"]')].filter(Boolean)
    for (const el of cands) {
      const t = (el.innerText || '').replace(/\s+/g, ' ').trim()
      if (t) return t
    }
    return ''
  })
  let txt = ''
  // up to 2 attempts: a single bar occasionally misses the hover (transient). Retry reduces
  // false-INCONCLUSIVE WITHOUT weakening fail-closed -- a genuinely unresolvable bar still FAILs.
  for (let attempt = 0; attempt < 2 && !txt; attempt++) {
    await page.mouse.move(10, cy);        await page.waitForTimeout(80)   // leave the chart
    await page.mouse.move(b.cx - 3, cy);  await page.waitForTimeout(140)
    await page.mouse.move(b.cx, cy);      await page.waitForTimeout(500)
    txt = await readTip()
  }
  const date = (txt.match(/^([A-Z][a-z]+ \d{1,2}, \d{4})/) || [])[1] || `(unresolved@${i})`
  seen.push({ i, cx: b.cx, date })
}
await browser.close()

console.log(`GATE unique-category-key | firm=${firm} mode=${count ? 'count' : 'value'} bars=${seen.length}`)
for (const s of seen) console.log(`   bar[${String(s.i).padStart(2)}] -> ${s.date}`)

// FAIL-CLOSED (doctrine: an instrument that cannot fail is not an instrument).
// Unresolved tooltips are NOT "distinct" -- they mean the gate COULD NOT MEASURE. Never PASS on
// them. (Caught by the pre-fix negative control: headless never fires the recharts tooltip, so
// unique "(unresolved@i)" placeholders made the gate report PASS on a KNOWN-BROKEN build.)
const unresolved = seen.filter(s => s.date.startsWith('(unresolved'))
if (!seen.length || unresolved.length) {
  console.log(`\nFAIL (INCONCLUSIVE): ${unresolved.length}/${seen.length} bars did not resolve a tooltip -- the gate could not measure.`)
  console.log('   -> run HEADED (HEADED=1): the recharts tooltip does not fire in headless.')
  process.exit(1)
}
const byDate = {}
for (const s of seen) (byDate[s.date] ||= []).push(s.i)
const collisions = Object.entries(byDate).filter(([, v]) => v.length > 1)
if (collisions.length) {
  console.log('\nFAIL: bars sharing a resolved category/date (recharts binding collision):')
  for (const [d, idxs] of collisions) console.log(`   "${d}" <- bars ${idxs.join(', ')}`)
  process.exit(1)
}
console.log(`\nPASS: all ${seen.length} bars resolved + DISTINCT -- no category-key collision.`)
