/**
 * DSGN_IRPTV1 FAST item 43 probe (W2-16): is the analysis-type step's 'Next' clipped, and does the page scroll
 * sideways, at narrower viewports? Fixture plane on the local dev build (same recipe as items 36-42; nothing reaches
 * the live backend). Measures, per viewport width: the Back/Next bounding boxes against the viewport, the document's
 * horizontal overflow, and which element (if any) is the widest offender.
 *
 * Usage: node .runtmp/w2-16-next-clip-driver.mjs <port> <out-dir>
 */
import { chromium } from 'playwright-core'
import { readFileSync, writeFileSync, mkdirSync } from 'node:fs'

const PORT = process.argv[2] || '5174'
const OUTDIR = process.argv[3] || '.runtmp/w2-16'
mkdirSync(OUTDIR, { recursive: true })
const ORIGIN = `http://localhost:${PORT}`
const EDGE = 'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe'
const CORS = {
  'Access-Control-Allow-Origin': ORIGIN, 'Access-Control-Allow-Credentials': 'true',
  'Access-Control-Allow-Headers': '*', 'Access-Control-Allow-Methods': '*', 'Content-Type': 'application/json',
}
const SESSION = {
  accessToken: 'ui-smoke-token',
  user: { email: 'dev@opalcapital.com', name: 'Dev User', role: 'admin', userType: 'Dev', firmId: 'opal-capital',
          firmRole: null, advisorId: null, advisorRole: null, mustChangePassword: false },
}
const BASE = '/api/scoped/investor-reporting'
const cottonwood = JSON.parse(readFileSync('src/pages/InvestorReporting/fixtures/smoke/dsgn-irptv1-cottonwood.json', 'utf8'))
const firmId = cottonwood[`${BASE}/directory/resolve`].firm_id
const fixtures = {
  ...cottonwood,
  [`${BASE}/directory/search`]: { contract_version: 'v1', operation: 'directory-search', firm_id: firmId,
    data: cottonwood[`${BASE}/directory/browse`].data.entries, unprojected_grant: { count: 0, denominator: 1, kinds: {} } },
}
const fixtureKeys = Object.keys(fixtures).sort((a, b) => b.length - a.length)
const matchFixture = (url) => fixtureKeys.find((key) => url.includes(key))
const WIDTHS = [1440, 1180, 1024, 820, 390]

const browser = await chromium.launch({ executablePath: EDGE, headless: true })
const results = []
for (const width of WIDTHS) {
  const page = await browser.newPage({ viewport: { width, height: 900 } })
  page.on('pageerror', (e) => console.log('PAGE-CRASH:', String(e).slice(0, 200)))
  await page.route('**/*', async (r) => {
    const req = r.request(); const url = req.url()
    if (req.method() === 'OPTIONS' && !url.startsWith(ORIGIN)) return r.fulfill({ status: 204, headers: CORS, body: '' })
    const fk = matchFixture(url)
    if (fk) return r.fulfill({ status: 200, headers: CORS, body: JSON.stringify(fixtures[fk]) })
    if (url.includes('/auth/refresh')) return r.fulfill({ status: 200, headers: CORS, body: JSON.stringify(SESSION) })
    return r.continue()
  })
  await page.goto(ORIGIN + '/investor-reporting', { waitUntil: 'networkidle', timeout: 30000 }).catch((e) => console.log('goto:', e.message.split('\n')[0]))
  await page.waitForTimeout(1200)
  try {
    const combo = page.getByRole('combobox', { name: 'Client search' })
    await combo.click(); await combo.fill('Cottonwood'); await page.waitForTimeout(700)
    const option = page.getByRole('option', { name: /Cottonwood Trust/ })
    await option.waitFor({ state: 'visible', timeout: 5000 }); await option.click()
  } catch (e) { console.log(`[${width}] SELECT-FAIL:`, e.message.split('\n')[0]) }
  await page.waitForTimeout(2500)
  try {
    await page.getByRole('button', { name: 'Analysis', exact: true }).or(page.getByRole('tab', { name: 'Analysis' })).first().click()
    await page.waitForTimeout(1200)
    await page.locator('[data-slot="analysis-portfolio-card"][data-portfolio="client"]').click()
    await page.waitForTimeout(800)
  } catch (e) { console.log(`[${width}] FLOW-FAIL:`, e.message.split('\n')[0]) }
  const m = await page.evaluate(() => {
    const rect = (sel) => { const el = document.querySelector(sel); if (!el) return null; const r = el.getBoundingClientRect(); return { left: Math.round(r.left), right: Math.round(r.right), width: Math.round(r.width) } }
    const doc = document.documentElement
    // the widest offender: the element whose right edge reaches furthest past the viewport
    let worst = null
    for (const el of document.querySelectorAll('body *')) {
      const r = el.getBoundingClientRect()
      if (r.right > doc.clientWidth + 1 && (!worst || r.right > worst.right)) worst = { right: Math.round(r.right), tag: el.tagName, slot: el.getAttribute('data-slot'), cls: (el.className || '').toString().slice(0, 80) }
    }
    return { viewport: doc.clientWidth, scrollWidth: doc.scrollWidth, overflow: doc.scrollWidth > doc.clientWidth, back: rect('[data-slot="analysis-back"]'), next: rect('[data-slot="analysis-next"]'), worst }
  })
  const nextClipped = m.next !== null && m.next.right > m.viewport
  results.push({ width, ...m, nextClipped })
  console.log(`[${width}] viewport=${m.viewport} scrollWidth=${m.scrollWidth} overflow=${m.overflow} back=${JSON.stringify(m.back)} next=${JSON.stringify(m.next)} nextClipped=${nextClipped} worst=${JSON.stringify(m.worst)}`)
  await page.screenshot({ path: `${OUTDIR}/analysis-step2-${width}.png`, fullPage: false })
  await page.close()
}
const anyClip = results.some((r) => r.nextClipped || r.overflow)
console.log(anyClip ? 'VERDICT: NEXT-CLIP-REPRODUCED' : 'VERDICT: NEXT-CLIP-NOT-REPRODUCED')
writeFileSync(`${OUTDIR}/measurements.json`, JSON.stringify(results, null, 2) + '\n')
await browser.close()
