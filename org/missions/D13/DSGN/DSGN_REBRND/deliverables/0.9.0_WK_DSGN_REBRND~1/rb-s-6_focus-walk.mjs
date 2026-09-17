// focus-walk.mjs -- RB-s-6 keyboard walk (RB6-AC5 / RB6-AC6 evidence: RECORDED, not graded).
// For each route: load with the ui-smoke auth stub (optionally with the BROWSER DEFAULT font size
// raised through CDP Page.setFontSizes -- the same setting as the browser's font-size preference),
// count the accent-painted elements the SHELL (<aside>) and the PAGE contribute, then walk the page
// with the Tab key. At every stop it records the focused element, whether it matches :focus-visible,
// its computed box-shadow/outline, and a clipped screenshot of the element and its ring. Then one
// REAL mouse click on a safe control (a segmented option, a tab, else a plain button) and, if one
// exists, a text input -- reporting whether :focus-visible matched and whether a ring painted.
// Usage: [REDUCE=1] node focus-walk.mjs <port> <outdir> <tag> <fontpx|0> <maxstops> <route>...
//   REDUCE=1 emulates prefers-reduced-motion: reduce for the whole context.
import { createRequire } from 'node:module'
import { mkdirSync, writeFileSync } from 'node:fs'
const require = createRequire('C:/tmp/wk-dsgn-1g/portal/package.json')
const { chromium } = require('playwright-core')

const [port, outdir, tag, fontArg, maxArg, ...routes] = process.argv.slice(2)
const FONT = Number(fontArg) || 0
const MAX = Number(maxArg) || 60
const REDUCE = process.env.REDUCE === '1'
const ORIGIN = `http://localhost:${port}`
const EDGE = 'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe'
const VW = 1440, VH = 900
const CORS = {
  'Access-Control-Allow-Origin': ORIGIN, 'Access-Control-Allow-Credentials': 'true',
  'Access-Control-Allow-Headers': '*', 'Access-Control-Allow-Methods': '*', 'Content-Type': 'application/json',
}
const SESSION = { accessToken: 'ui-smoke-token', user: { email: 'dev@opalcapital.com', name: 'Dev User', role: 'admin',
  userType: 'Dev', firmId: 'opal-capital', firmRole: null, advisorId: null, advisorRole: null, mustChangePassword: false } }
const ACC = 'rgb(95, 59, 227)'
// A RING is classified from the computed box-shadow by REGEX, never by an exact string: a control
// carrying transition-all interpolates the shadow (rgba alpha < 1, fractional spread) unless reduced
// motion holds, and the band ink --palette-white resolves through its HSL token to rgb(230, 234, 244),
// not the contract's #E8ECF5. FULL = the outer layer has reached its 4px spread at full opacity.
const RX = { accent: 'rgba?\\(95, 59, 227(, 1)?\\)', band: 'rgba?\\(23[0-2], 23[4-6], 24[4-5](, 1)?\\)',
  accentAny: 'rgba?\\(95, 59, 227', bandAny: 'rgba?\\(23[0-2], 23[4-6], 24[4-5]' }
const DENY = /upload|delete|remove|submit|save|log ?out|sign ?out|export|send|approve|reject|cancel|clear|reset/i

// runs IN THE PAGE: classify one computed box-shadow
const CLASSIFY = `(shadow, RX) => {
  const ring = new RegExp(RX.accentAny).test(shadow) ? 'ACCENT' : new RegExp(RX.bandAny).test(shadow) ? 'BAND' : 'NONE'
  const full = ring !== 'NONE' && new RegExp('(' + RX.accent + '|' + RX.band + ') 0px 0px 0px 4px').test(shadow)
  return { ring, full }
}`

mkdirSync(`${outdir}/clips_${tag}`, { recursive: true })
const browser = await chromium.launch({ executablePath: EDGE, headless: true })
const context = await browser.newContext({ viewport: { width: VW, height: VH }, reducedMotion: REDUCE ? 'reduce' : 'no-preference' })
const summary = []

for (const r of routes) {
  const route = '/' + r.replace(/^\/+/, '')
  const slug = r.replace(/[^a-z0-9-]/gi, '_')
  const page = await context.newPage()
  await page.route('**/*', (rt) => {
    const req = rt.request(); const url = req.url()
    if (req.method() === 'OPTIONS' && !url.startsWith(ORIGIN)) return rt.fulfill({ status: 204, headers: CORS, body: '' })
    if (url.includes('/auth/refresh')) return rt.fulfill({ status: 200, headers: CORS, body: JSON.stringify(SESSION) })
    return rt.continue()
  })
  if (FONT > 0) {
    const cdp = await context.newCDPSession(page)
    await cdp.send('Page.enable')
    await cdp.send('Page.setFontSizes', { fontSizes: { standard: FONT, fixed: Math.round(FONT * 13 / 16) } })
  }
  await page.goto(ORIGIN + route, { waitUntil: 'networkidle', timeout: 30000 }).catch((e) => console.log('goto:', e.message.split('\n')[0]))
  await page.waitForTimeout(3000)

  const env = await page.evaluate(({ ACC }) => {
    const out = { loc: location.pathname, rootFont: getComputedStyle(document.documentElement).fontSize,
      bodyFont: getComputedStyle(document.body).fontSize, docW: document.documentElement.scrollWidth,
      reduced: matchMedia('(prefers-reduced-motion: reduce)').matches,
      shellFill: [], shellAny: [], pageFill: 0, focusables: 0, navActive: null }
    for (const el of document.querySelectorAll('body *')) {
      const rc = el.getBoundingClientRect()
      if (rc.width === 0 || rc.height === 0) continue
      const cs = getComputedStyle(el)
      if (cs.visibility === 'hidden' || cs.display === 'none' || Number(cs.opacity) === 0) continue
      if (el.closest('svg, .recharts-wrapper')) continue
      const fill = cs.backgroundColor === ACC
      const ownText = [...el.childNodes].some((n) => n.nodeType === 3 && n.textContent.trim())
      const any = fill || (ownText && cs.color === ACC) || cs.boxShadow.includes(ACC) ||
        ['Top', 'Right', 'Bottom', 'Left'].some((s) => parseFloat(cs['border' + s + 'Width']) > 0 && cs['border' + s + 'Color'] === ACC)
      const d = el.tagName.toLowerCase() + ' ' + JSON.stringify((el.innerText || el.getAttribute('aria-label') || '').trim().replace(/\s+/g, ' ').slice(0, 30))
      if (el.closest('aside')) { if (fill) out.shellFill.push(d); if (any) out.shellAny.push(d) }
      else if (fill) out.pageFill++
    }
    const act = document.querySelector('aside nav a.active, aside nav a[aria-current="page"]')
    if (act) {
      const cs = getComputedStyle(act)
      out.navActive = { text: (act.innerText || '').trim() || act.getAttribute('href'), fontWeight: cs.fontWeight, color: cs.color,
        background: cs.backgroundColor, borderLeft: cs.borderLeftWidth + ' ' + cs.borderLeftStyle + ' ' + cs.borderLeftColor, boxShadow: cs.boxShadow }
    }
    const sel = 'a[href],button:not([disabled]),input:not([disabled]):not([type=hidden]),select:not([disabled]),textarea:not([disabled]),[tabindex]:not([tabindex="-1"]),summary'
    out.focusables = [...document.querySelectorAll(sel)].filter((e) => { const rc = e.getBoundingClientRect(); return rc.width > 0 && rc.height > 0 && getComputedStyle(e).visibility !== 'hidden' }).length
    return out
  }, { ACC })

  // ---- keyboard walk ----
  await page.evaluate(() => { window.__seen = new Set(); if (document.activeElement) document.activeElement.blur() })
  const stops = []
  let wrapped = false
  for (let i = 1; i <= MAX; i++) {
    await page.keyboard.press('Tab')
    await page.waitForTimeout(140)
    const info = await page.evaluate(({ RX, CLASSIFY }) => {
      const classify = eval(CLASSIFY)
      const el = document.activeElement
      if (!el || el === document.body) return { body: true }
      if (window.__seen.has(el)) return { wrapped: true }
      window.__seen.add(el)
      const cs = getComputedStyle(el); const rc = el.getBoundingClientRect()
      const shadow = cs.boxShadow
      const { ring, full } = classify(shadow, RX)
      return { tag: el.tagName.toLowerCase(), role: el.getAttribute('role') || '', type: el.getAttribute('type') || '',
        text: (el.getAttribute('aria-label') || el.innerText || el.value || el.getAttribute('title') || '').trim().replace(/\s+/g, ' ').slice(0, 36),
        fv: el.matches(':focus-visible'), shadow: shadow.slice(0, 140), ring, full,
        outline: cs.outlineStyle + ' ' + cs.outlineWidth,
        inShell: !!el.closest('aside'), inBand: !!el.closest('.dark-band'),
        x: rc.x, y: rc.y, w: rc.width, h: rc.height }
    }, { RX, CLASSIFY })
    if (info.wrapped) { wrapped = true; break }
    if (info.body) { stops.push({ i, body: true }); continue }
    const pad = 14
    const x = Math.max(0, Math.floor(info.x - pad)), y = Math.max(0, Math.floor(info.y - pad))
    const w = Math.min(Math.ceil(info.w + 2 * pad), 700, VW - x), h = Math.min(Math.ceil(info.h + 2 * pad), 260, VH - y)
    let clip = null
    if (w > 4 && h > 4) {
      clip = `${outdir}/clips_${tag}/${slug}_${String(i).padStart(3, '0')}.png`
      await page.screenshot({ path: clip, clip: { x, y, width: w, height: h } }).catch(() => { clip = null })
    }
    stops.push({ ...info, i, clip })
  }

  // ---- mouse click test: a REAL pointer click, then read :focus-visible ----
  const clicks = []
  for (const kind of ['control', 'textinput']) {
    await page.evaluate(() => { if (document.activeElement) document.activeElement.blur() })
    const target = await page.evaluateHandle(({ kind, DENY_SRC }) => {
      const deny = new RegExp(DENY_SRC, 'i')
      const vis = (e) => { const rc = e.getBoundingClientRect(); return rc.width > 0 && rc.height > 0 && rc.top >= 0 && rc.bottom <= innerHeight }
      const main = document.querySelector('main') || document.body
      let list
      if (kind === 'control') list = [...main.querySelectorAll('[aria-pressed="false"],[role=tab],button')]
      else list = [...main.querySelectorAll('input[type=text],input[type=search],input[type=number],input[type=email],input[type=password],input:not([type]),textarea')]
      return list.find((e) => vis(e) && !e.disabled && !deny.test(e.innerText || e.getAttribute('aria-label') || '')) || null
    }, { kind, DENY_SRC: DENY.source })
    const el = target.asElement()
    if (!el) { clicks.push({ kind, none: true }); continue }
    const box = await el.boundingBox()
    await page.mouse.click(box.x + box.width / 2, box.y + box.height / 2)
    await page.waitForTimeout(400)
    const res = await page.evaluate(({ RX, CLASSIFY }) => {
      const classify = eval(CLASSIFY)
      const el = document.activeElement
      if (!el || el === document.body) return { focused: 'BODY', fv: false, ring: 'NONE', full: false }
      const cs = getComputedStyle(el)
      const { ring, full } = classify(cs.boxShadow, RX)
      return { focused: el.tagName.toLowerCase() + ' ' + JSON.stringify((el.innerText || el.getAttribute('aria-label') || el.getAttribute('placeholder') || '').trim().slice(0, 30)),
        fv: el.matches(':focus-visible'), ring, full }
    }, { RX, CLASSIFY })
    const shot = `${outdir}/clips_${tag}/${slug}_click_${kind}.png`
    const cx = Math.max(0, Math.floor(box.x - 14)), cy = Math.max(0, Math.floor(box.y - 14))
    await page.screenshot({ path: shot, clip: { x: cx, y: cy, width: Math.min(Math.ceil(box.width + 28), 700, VW - cx), height: Math.min(Math.ceil(box.height + 28), 260, VH - cy) } }).catch(() => {})
    clicks.push({ kind, ...res, shot })
  }

  const full = `${outdir}/${tag}_${slug}_full.png`
  await page.evaluate(() => { if (document.activeElement) document.activeElement.blur() })
  await page.screenshot({ path: full, fullPage: true })

  const walked = stops.filter((s) => !s.body)
  const fvN = walked.filter((s) => s.fv).length
  const ringN = walked.filter((s) => s.ring !== 'NONE').length
  const fullN = walked.filter((s) => s.full).length
  console.log(`=== ROUTE ${route}  [${tag}]`)
  console.log('LOC        :', env.loc, env.loc === route ? '' : '<-- DID NOT LAND')
  console.log('ROOT-FONT  :', env.rootFont, ' BODY-FONT:', env.bodyFont, ' DOC-SCROLL-WIDTH:', env.docW, '(viewport 1440)', ' REDUCED-MOTION:', env.reduced)
  console.log('SHELL-ACCENT-FILL:', env.shellFill.length, JSON.stringify(env.shellFill))
  console.log('SHELL-ACCENT-ANY :', env.shellAny.length, JSON.stringify(env.shellAny))
  console.log('PAGE-ACCENT-FILL :', env.pageFill)
  console.log('NAV-ACTIVE :', JSON.stringify(env.navActive))
  console.log('FOCUSABLE-VISIBLE:', env.focusables, ' TAB-STOPS-WALKED:', walked.length, wrapped ? '(WRAPPED -- the whole tab order was walked)' : `(cap ${MAX} reached)`)
  console.log('STOPS :FOCUS-VISIBLE:', fvN, 'of', walked.length, ' RING-PAINTED:', ringN, 'of', walked.length,
    ' (ACCENT', walked.filter((s) => s.ring === 'ACCENT').length, '/ BAND', walked.filter((s) => s.ring === 'BAND').length, ')',
    ' RING-AT-FULL-4PX:', fullN, 'of', walked.length)
  for (const s of walked.filter((s) => s.ring === 'NONE')) console.log('  NO-RING stop', s.i, s.tag, s.role, JSON.stringify(s.text), 'fv=' + s.fv, 'shadow=' + s.shadow, 'outline=' + s.outline)
  for (const s of walked.filter((s) => s.ring !== 'NONE' && !s.full)) console.log('  PARTIAL-RING stop', s.i, s.tag, JSON.stringify(s.text), 'shadow=' + s.shadow)
  for (const c of clicks) console.log('MOUSE-CLICK', c.kind, c.none ? 'NONE-FOUND' : `${c.focused} :focus-visible=${c.fv} ring=${c.ring}`)
  console.log('FULL-PAGE  :', full)
  summary.push({ route, tag, env, stops, clicks, wrapped, full })
  writeFileSync(`${outdir}/${tag}_${slug}.json`, JSON.stringify({ route, tag, env, stops, clicks, wrapped, full }, null, 1))
  await page.close()
}
await browser.close()
