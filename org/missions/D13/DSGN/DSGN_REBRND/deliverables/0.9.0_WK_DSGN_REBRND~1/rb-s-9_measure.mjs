/**
 * rb9-measure.mjs -- RB-s-9 measurement instrument (scratch; not shipped).
 *
 * Same auth stub + fixture router as scripts/ui-smoke.mjs, then measures, at 1440x900:
 *   - page column: the element under <main> holding the page's sections
 *   - lastContentBottom: max bottom (document coords) of any rendered box inside the column
 *   - docHeight, and SHARE OF VIEWPORT BELOW THE LAST CONTENT ELEMENT
 *       = (max(docHeight, 900) - lastContentBottom) / 900, the canvas after the work ends,
 *         expressed in viewport heights
 *   - gaps between consecutive top-level sections of the column (px)
 *   - inner padding of every panel content box (px), read by computed style
 *   - terminator: the element carrying data-page-end, if any, and whether it is the LAST box
 *   - with --collision: every divergence-bar label vs the centre ornament, overlap_px each
 *
 * Usage: node .scratch/rb9-measure.mjs <route> <fixtures.json> <port> <out.json> [--collision] [--png f]
 */
import { chromium } from 'playwright-core'
import { readFileSync, writeFileSync } from 'node:fs'

const [routeArg, fixturesPath, port, outPath] = process.argv.slice(2)
const collision = process.argv.includes('--collision')
const pngIdx = process.argv.indexOf('--png')
const png = pngIdx > 0 ? process.argv[pngIdx + 1] : null
const route = '/' + String(routeArg).replace(/^.*\/Git\//i, '').replace(/^\/+/, '')
const ORIGIN = `http://localhost:${port}`
const fixtures = JSON.parse(readFileSync(fixturesPath, 'utf8'))
const keys = Object.keys(fixtures).sort((a, b) => b.length - a.length)
const hits = Object.fromEntries(keys.map(k => [k, 0]))
const CORS = {
  'Access-Control-Allow-Origin': ORIGIN, 'Access-Control-Allow-Credentials': 'true',
  'Access-Control-Allow-Headers': '*', 'Access-Control-Allow-Methods': '*', 'Content-Type': 'application/json',
}
const SESSION = { accessToken: 'ui-smoke-token', user: { email: 'dev@opalcapital.com', name: 'Dev User', role: 'admin',
  userType: 'Dev', firmId: 'opal-capital', firmRole: null, advisorId: null, advisorRole: null, mustChangePassword: false } }

const browser = await chromium.launch({ executablePath: 'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe', headless: true })
const page = await browser.newPage({ viewport: { width: 1440, height: 900 } })
await page.route('**/*', r => {
  const req = r.request(); const url = req.url()
  if (req.method() === 'OPTIONS' && !url.startsWith(ORIGIN)) return r.fulfill({ status: 204, headers: CORS, body: '' })
  const k = keys.find(key => url.includes(key))
  if (k) { hits[k]++; return r.fulfill({ status: 200, headers: CORS, body: JSON.stringify(fixtures[k]) }) }
  if (url.includes('/auth/refresh')) return r.fulfill({ status: 200, headers: CORS, body: JSON.stringify(SESSION) })
  return r.continue()
})
await page.goto(ORIGIN + route, { waitUntil: 'networkidle', timeout: 30000 }).catch(e => console.log('goto:', e.message.split('\n')[0]))
await page.waitForTimeout(3500)

const layout = () => page.evaluate(() => {
  const main = document.querySelector('main')
  if (!main) return { error: 'no <main>' }
  // Descend single-child wrappers until the element that holds the page's sections.
  let col = main
  for (let i = 0; i < 8; i++) {
    const kids = Array.from(col.children).filter(c => c.getBoundingClientRect().height > 0)
    if (kids.length === 1) col = kids[0]; else break
  }
  const sy = window.scrollY
  const boxes = Array.from(col.querySelectorAll('*')).map(el => el.getBoundingClientRect()).filter(b => b.width > 0 && b.height > 0)
  const lastContentBottom = Math.max(...boxes.map(b => b.bottom + sy))
  const docHeight = Math.max(document.documentElement.scrollHeight, document.body.scrollHeight)
  const sections = Array.from(col.children).filter(c => c.getBoundingClientRect().height > 0)
  const gaps = []
  for (let i = 1; i < sections.length; i++) {
    gaps.push(Math.round((sections[i].getBoundingClientRect().top - sections[i - 1].getBoundingClientRect().bottom) * 100) / 100)
  }
  const pads = Array.from(document.querySelectorAll('main .rounded-b-lg, main [data-panel-content]'))
    .filter(el => el.getBoundingClientRect().height > 0)
    .map(el => { const cs = getComputedStyle(el); return [cs.paddingTop, cs.paddingRight, cs.paddingBottom, cs.paddingLeft].join(' ') })
  const padCounts = pads.reduce((a, p) => { a[p] = (a[p] || 0) + 1; return a }, {})
  const end = document.querySelector('[data-page-end]')
  const endBox = end ? end.getBoundingClientRect() : null
  const mainCs = getComputedStyle(main)
  return {
    viewport: [window.innerWidth, window.innerHeight],
    column: col.tagName + '.' + String(col.className).slice(0, 80),
    sectionCount: sections.length,
    docHeight, lastContentBottom: Math.round(lastContentBottom),
    mainPaddingBottom: mainCs.paddingBottom,
    shareOfViewportBelowLastContent: Math.round(((Math.max(docHeight, window.innerHeight) - lastContentBottom) / window.innerHeight) * 1000) / 1000,
    sectionGapsPx: gaps,
    panelContentPadding: padCounts,
    terminator: end ? { present: true, top: Math.round(endBox.top + sy), bottom: Math.round(endBox.bottom + sy),
      isLastBox: Math.round(endBox.bottom + sy) >= Math.round(lastContentBottom) - 1, text: end.innerText.trim().slice(0, 80) } : { present: false },
  }
})

const measureCollision = (caseName) => page.evaluate((caseName) => {
  const out = []
  const rows = Array.from(document.querySelectorAll('[data-divergence-row]')).length
    ? Array.from(document.querySelectorAll('[data-divergence-row]'))
    : Array.from(document.querySelectorAll('div.relative.h-16')).filter(r => r.querySelector('.z-20 svg'))
  rows.forEach((row, i) => {
    const orn = row.querySelector('[data-divergence-ornament]') || row.querySelector('.z-20 > div')
    if (!orn) return
    const ob = orn.getBoundingClientRect()
    const labels = row.querySelectorAll('[data-divergence-label]').length
      ? Array.from(row.querySelectorAll('[data-divergence-label]'))
      : Array.from(row.querySelectorAll('span')).filter(s => /%$/.test(s.textContent.trim()))
    labels.forEach(lab => {
      const lb = lab.getBoundingClientRect()
      const xo = Math.max(0, Math.min(lb.right, ob.right) - Math.max(lb.left, ob.left))
      const yo = Math.max(0, Math.min(lb.bottom, ob.bottom) - Math.max(lb.top, ob.top))
      const bar = lab.closest('[data-divergence-bar]') || lab.parentElement
      const barBox = bar.getBoundingClientRect()
      out.push({
        case: caseName, row: i, label: lab.textContent.trim(),
        label_box: [lb.left, lb.top, lb.right, lb.bottom].map(v => Math.round(v * 10) / 10),
        ornament_box: [ob.left, ob.top, ob.right, ob.bottom].map(v => Math.round(v * 10) / 10),
        bar_width_px: Math.round(barBox.width * 10) / 10,
        overlap_px: yo > 0 ? Math.round(xo * 10) / 10 : 0,
        label_clipped_by_bar: lb.left < barBox.left - 0.5 || lb.right > barBox.right + 0.5,
      })
    })
  })
  return out
}, caseName)

const result = { route, fixtures: fixturesPath, fixtureHits: hits, layout: await layout() }
if (collision) {
  const pairs = [...await measureCollision('QTD')]
  for (const p of ['YTD', '1Y', 'SI']) {
    const btn = page.getByRole('button', { name: p, exact: true }).first()
    if (await btn.count()) { await btn.click(); await page.waitForTimeout(1200); pairs.push(...await measureCollision(p)) }
  }
  result.pairs = pairs
}
if (png) await page.screenshot({ path: png, fullPage: true })
writeFileSync(outPath, JSON.stringify(result, null, 2))
console.log(JSON.stringify({ route, fixtureHits: hits, layout: result.layout, pairs: result.pairs?.length }, null, 1))
await browser.close()
