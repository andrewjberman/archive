/**
 * shadow-check.mjs -- AMGT-rm-2 AC2 C11 shadow-limb determination.
 * Launches the same stubbed-session route ui-smoke.mjs uses, then prints
 * getComputedStyle(el).boxShadow for one PanelHeader strip and one PanelFooter strip
 * on the merged /security-analysis page (list state), plus the sidebar <aside> for contrast.
 *
 *   node shadow-check.mjs --port 5183
 *
 * Run from portal/ (module resolution for playwright-core).
 */
import { chromium } from 'playwright-core'

const args = process.argv.slice(2)
const port = args.includes('--port') ? args[args.indexOf('--port') + 1] : '5183'
const ORIGIN = `http://localhost:${port}`
const EDGE = 'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe'

const CORS = {
  'Access-Control-Allow-Origin': ORIGIN,
  'Access-Control-Allow-Credentials': 'true',
  'Access-Control-Allow-Headers': '*',
  'Access-Control-Allow-Methods': '*',
  'Content-Type': 'application/json',
}
const SESSION = {
  accessToken: 'shadow-check-token',
  user: { email: 'dev@opalcapital.com', name: 'Dev User', role: 'admin',
          userType: 'Dev', firmId: 'opal-capital', firmRole: null, advisorId: null,
          advisorRole: null, mustChangePassword: false },
}

const browser = await chromium.launch({ executablePath: EDGE, headless: true })
const context = await browser.newContext({ viewport: { width: 1440, height: 1000 } })
const page = await context.newPage()

await page.route('**/auth/refresh*', route =>
  route.fulfill({ status: 200, headers: CORS, body: JSON.stringify(SESSION) }))

await page.goto(`${ORIGIN}/security-analysis`, { waitUntil: 'networkidle' })
await page.waitForTimeout(500)

const result = await page.evaluate(() => {
  const out = {}
  const headerEl = document.querySelector('main h3.uppercase')?.closest('div')
  // PanelHeader strip: the ancestor div carrying bg-[hsl(var(--bg-header))] / rounded-t-[4px]
  const allDivs = Array.from(document.querySelectorAll('main div'))
  const headerStrip = allDivs.find(d => {
    const cs = getComputedStyle(d)
    return d.querySelector('h3') && cs.borderTopLeftRadius !== '0px'
  })
  const footerStrip = allDivs.find(d => {
    const cs = getComputedStyle(d)
    return cs.borderBottomLeftRadius !== '0px' && !d.querySelector('h3')
  })
  const sidebar = document.querySelector('aside')
  out.headerStripFound = !!headerStrip
  out.headerStripBoxShadow = headerStrip ? getComputedStyle(headerStrip).boxShadow : null
  out.headerStripClass = headerStrip ? headerStrip.className : null
  out.footerStripFound = !!footerStrip
  out.footerStripBoxShadow = footerStrip ? getComputedStyle(footerStrip).boxShadow : null
  out.footerStripClass = footerStrip ? footerStrip.className : null
  out.sidebarFound = !!sidebar
  out.sidebarBoxShadow = sidebar ? getComputedStyle(sidebar).boxShadow : null
  out.sidebarClass = sidebar ? sidebar.className : null
  return out
})

console.log(JSON.stringify(result, null, 2))
await browser.close()
