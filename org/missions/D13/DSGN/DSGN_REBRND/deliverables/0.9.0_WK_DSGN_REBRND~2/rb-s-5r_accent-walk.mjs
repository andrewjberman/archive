// rb-s-5r_accent-walk.mjs -- RB-s-5 Amendment 1 counterexample walk (RB5-AC5R / RB5-AC6 evidence,
// RECORDED, never graded). Adapted from round 1's rb-s-5_accent-walk.mjs (deliverables/~1):
// the portal root is an argument instead of a hard-coded worktree, border-image is probed,
// and every accent hit is CLASSIFIED against Andrew's budget (DESIGN.md C8 as amended 2026-09-14):
//   ACTION     a filled accent button outside the sidebar -- the ONE persistent primary action
//   SITE1..5   the five identity accents: page-title rule, header subtext, active tab (label+rule),
//              sidebar active item, avatar
//   TRANSIENT  the focused element (its :focus-visible ring) -- not counted
//   OTHER      any accent paint that is none of the above -- "and nowhere else" is graded on this list
// Hits inside <svg> or .recharts-wrapper are DATA (C6: a series in #5F3BE3 is not an accent spend).
// Per route: load with the ui-smoke auth stub, FOCUS a secondary control, SELECT the title text,
// then enumerate. The selection highlight is a pseudo-element and is outside any element's style.
// Usage: node rb-s-5r_accent-walk.mjs <portal root> <port> <outdir> <route>...
import { createRequire } from 'node:module'
import path from 'node:path'

const [portal, port, outdir, ...routes] = process.argv.slice(2)
const require = createRequire(path.join(portal, 'package.json'))
const { chromium } = require('playwright-core')
const ORIGIN = `http://localhost:${port}`
const EDGE = 'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe'
const CORS = {
  'Access-Control-Allow-Origin': ORIGIN, 'Access-Control-Allow-Credentials': 'true',
  'Access-Control-Allow-Headers': '*', 'Access-Control-Allow-Methods': '*', 'Content-Type': 'application/json',
}
const SESSION = { accessToken: 'ui-smoke-token', user: { email: 'dev@opalcapital.com', name: 'Dev User', role: 'admin',
  userType: 'Dev', firmId: 'opal-capital', firmRole: null, advisorId: null, advisorRole: null, mustChangePassword: false } }

function classify(c) {
  if (c.focused) return 'TRANSIENT'
  if (c.props.includes('border-image')) return 'OTHER'
  if (c.inAside && c.tag === 'a' && c.props.includes('background')) return 'SITE4 sidebar-active'
  if (c.inAside && /rounded-full/.test(c.cls) && c.props.includes('background')) return 'SITE5 avatar'
  if (c.tag === 'div' && /w-\[3px\]/.test(c.cls) && c.props.includes('background')) return 'SITE1 page-title-rule'
  if (c.tag === 'p' && c.props.includes('text') && c.nearH1) return 'SITE2 header-subtext'
  if (c.inTabButton) return 'SITE3 active-tab'
  if (c.tag === 'button' && !c.inAside && c.props.includes('background')) return 'ACTION'
  return 'OTHER'
}

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

  // 1. FOCUS a secondary control by KEYBOARD (so :focus-visible paints): an idle segmented
  //    option first, else a named secondary.
  let focusDesc = 'NONE'
  // A DISABLED control cannot take focus (the first run landed on <body> on /portfolio-management,
  // whose Resume is disabled without a fund loaded), so candidates are enabled-only and the
  // landing element is printed with its :focus-visible state.
  const idle = page.locator('[aria-pressed="false"]:not([disabled])').first()
  const sec = page.locator('button:not([disabled])').filter({ hasText: /Resume|Expand|Collapse/i }).first()
  const target = (await idle.count()) ? idle : ((await sec.count()) ? sec : null)
  if (target) {
    await target.focus()
    await page.keyboard.press('Shift+Tab')
    await page.keyboard.press('Tab')
    focusDesc = await page.evaluate(() => {
      const a = document.activeElement
      return `${a.tagName.toLowerCase()} ${JSON.stringify((a.innerText || a.getAttribute('aria-label') || '').trim().slice(0, 30))} focus-visible=${a.matches(':focus-visible')}`
    })
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
    const ACC_ANY = /rgba?\(95, 59, 227/
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
      if (cs.borderImageSource && cs.borderImageSource !== 'none' && ACC_ANY.test(cs.borderImageSource)) props.push('border-image')
      if (cs.fill === ACC) props.push('fill')
      if (cs.stroke === ACC && cs.stroke !== 'none') props.push('stroke')
      if (cs.boxShadow && cs.boxShadow.includes(ACC)) props.push('box-shadow')
      if (!props.length) continue
      const btn = el.closest('button')
      const h1 = el.parentElement && el.parentElement.querySelector(':scope > h1')
      const row = { tag: el.tagName.toLowerCase(), text: (el.innerText || el.getAttribute('aria-label') || '').trim().replace(/\s+/g, ' ').slice(0, 40),
        props: props.join('+'), at: `${Math.round(rc.x)},${Math.round(rc.y)} ${Math.round(rc.width)}x${Math.round(rc.height)}`,
        focused: el === active, inAside: !!el.closest('aside'), cls: String(el.className || '').slice(0, 200),
        inTabButton: !!(btn && /border-b-2/.test(btn.className) && !btn.closest('aside')), nearH1: !!h1 }
      if (el.closest('svg, .recharts-wrapper')) out.data.push(row); else out.chrome.push(row)
    }
    return out
  })
  const counts = {}
  for (const c of res.chrome) { c.kind = classify(c); counts[c.kind.split(' ')[0]] = (counts[c.kind.split(' ')[0]] || 0) + 1 }
  const sites = new Set(res.chrome.filter((c) => c.kind.startsWith('SITE')).map((c) => c.kind))
  console.log(`=== ROUTE ${route}`)
  console.log('FOCUSED   :', focusDesc)
  console.log('SELECTED  :', JSON.stringify(selected.slice(0, 60)))
  console.log('SCANNED   :', res.scanned, 'visible elements')
  console.log('CHROME-ACCENT:', res.chrome.length, 'painted elements', JSON.stringify(counts))
  for (const c of res.chrome) console.log('  ', c.kind.padEnd(22), c.tag, JSON.stringify(c.text), c.props, c.at)
  console.log('PERSISTENT-ACTIONS:', res.chrome.filter((c) => c.kind === 'ACTION').length)
  console.log('IDENTITY-SITES    :', sites.size, 'of 5 distinct', JSON.stringify([...sites].sort()))
  console.log('OTHER             :', res.chrome.filter((c) => c.kind === 'OTHER').length)
  console.log('DATA-ACCENT  :', res.data.length, '(inside svg/.recharts-wrapper -- C6 data use, not counted)')
  for (const d of res.data.slice(0, 10)) console.log('  DATA', d.tag, d.props, d.at)
  const png = path.join(outdir, `rb-s-5r_walk_${r.replace(/[^a-z0-9-]/gi, '_')}.png`)
  await page.screenshot({ path: png, fullPage: true })
  console.log('SAVED     :', png)
  await page.close()
}
await browser.close()
