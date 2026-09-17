// accent-walk.mjs -- RB-s-5 counterexample walk (RB5-AC6 evidence, recorded, not graded).
// For each route: load with the ui-smoke auth stub, FOCUS a secondary control, SELECT
// text, then enumerate every visible element whose computed colour resolves to the
// accent rgb(95, 59, 227). Hits inside an <svg> or .recharts-wrapper are listed as DATA
// (DESIGN.md C6: a series in #5F3BE3 is not an accent spend); the rest are CHROME.
// The focused element and the selection are TRANSIENT and are reported, not counted.
// Usage: node accent-walk.mjs <port> <outdir> <route>...
import { createRequire } from 'node:module'
const require = createRequire('C:/tmp/wk-dsgn-1f/portal/package.json')
const { chromium } = require('playwright-core')

const [port, outdir, ...routes] = process.argv.slice(2)
const ORIGIN = `http://localhost:${port}`
const EDGE = 'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe'
const CORS = {
  'Access-Control-Allow-Origin': ORIGIN, 'Access-Control-Allow-Credentials': 'true',
  'Access-Control-Allow-Headers': '*', 'Access-Control-Allow-Methods': '*', 'Content-Type': 'application/json',
}
const SESSION = { accessToken: 'ui-smoke-token', user: { email: 'dev@opalcapital.com', name: 'Dev User', role: 'admin',
  userType: 'Dev', firmId: 'opal-capital', firmRole: null, advisorId: null, advisorRole: null, mustChangePassword: false } }

const browser = await chromium.launch({ executablePath: EDGE, headless: true })
for (const r of routes) {
  const route = '/' + r.replace(/^\/+/, '')
  const page = await browser.newPage({ viewport: { width: 1440, height: 900 } })
  await page.route('**/*', (rt) => {
    const req = rt.request(); const url = req.url()
    if (req.method() === 'OPTIONS' && !url.startsWith(ORIGIN)) return rt.fulfill({ status: 204, headers: CORS, body: '' })
    if (url.includes('/auth/refresh')) return rt.fulfill({ status: 200, headers: CORS, body: JSON.stringify(SESSION) })
    return rt.continue()
  })
  await page.goto(ORIGIN + route, { waitUntil: 'networkidle', timeout: 30000 }).catch((e) => console.log('goto:', e.message.split('\n')[0]))
  await page.waitForTimeout(3000)

  // 1. FOCUS a secondary control: an idle segmented option first, else a named secondary.
  let focusDesc = 'NONE'
  const idle = page.locator('[aria-pressed="false"]').first()
  if (await idle.count()) { await idle.focus(); focusDesc = 'aria-pressed=false: ' + (await idle.innerText()).trim() }
  else {
    const sec = page.getByRole('button', { name: /Resume|Expand/ }).first()
    if (await sec.count()) { await sec.focus(); focusDesc = 'button: ' + (await sec.innerText()).trim() }
  }
  // 2. SELECT text: the page title.
  const selected = await page.evaluate(() => {
    const h = document.querySelector('h1'); if (!h) return ''
    const rg = document.createRange(); rg.selectNodeContents(h)
    const s = window.getSelection(); s.removeAllRanges(); s.addRange(rg); return s.toString()
  })
  // 3. ENUMERATE accent-painted elements.
  const res = await page.evaluate(() => {
    const ACC = 'rgb(95, 59, 227)'
    const out = { chrome: [], data: [], scanned: 0 }
    const active = document.activeElement
    for (const el of document.querySelectorAll('body *')) {
      const rc = el.getBoundingClientRect()
      if (rc.width === 0 || rc.height === 0) continue
      const cs = getComputedStyle(el)
      if (cs.visibility === 'hidden' || cs.display === 'none' || Number(cs.opacity) === 0) continue
      out.scanned++
      const props = []
      if (cs.backgroundColor === ACC) props.push('background')
      const ownText = [...el.childNodes].some((n) => n.nodeType === 3 && n.textContent.trim())
      if (ownText && cs.color === ACC) props.push('text')
      for (const side of ['Top', 'Right', 'Bottom', 'Left']) {
        if (parseFloat(cs['border' + side + 'Width']) > 0 && cs['border' + side + 'Color'] === ACC) { props.push('border-' + side.toLowerCase()); break }
      }
      if (cs.fill === ACC) props.push('fill')
      if (cs.stroke === ACC && cs.stroke !== 'none') props.push('stroke')
      if (cs.boxShadow && cs.boxShadow.includes(ACC)) props.push('box-shadow')
      if (!props.length) continue
      const row = { tag: el.tagName.toLowerCase(), text: (el.innerText || el.getAttribute('aria-label') || '').trim().replace(/\s+/g, ' ').slice(0, 40),
        props: props.join('+'), at: `${Math.round(rc.x)},${Math.round(rc.y)} ${Math.round(rc.width)}x${Math.round(rc.height)}`,
        focused: el === active }
      if (el.closest('svg, .recharts-wrapper')) out.data.push(row); else out.chrome.push(row)
    }
    return out
  })
  console.log(`=== ROUTE ${route}`)
  console.log('FOCUSED   :', focusDesc)
  console.log('SELECTED  :', JSON.stringify(selected.slice(0, 60)))
  console.log('SCANNED   :', res.scanned, 'visible elements')
  console.log('CHROME-ACCENT:', res.chrome.length)
  for (const c of res.chrome) console.log('  CHROME', c.tag, JSON.stringify(c.text), c.props, c.at, c.focused ? '(FOCUSED -- transient)' : '')
  console.log('DATA-ACCENT  :', res.data.length, '(inside svg/.recharts-wrapper -- C6 data use, not counted)')
  for (const d of res.data.slice(0, 10)) console.log('  DATA', d.tag, d.props, d.at)
  const png = `${outdir}/walk_${r.replace(/[^a-z0-9-]/gi, '_')}.png`
  await page.screenshot({ path: png, fullPage: true })
  console.log('SAVED     :', png)
  await page.close()
}
await browser.close()
