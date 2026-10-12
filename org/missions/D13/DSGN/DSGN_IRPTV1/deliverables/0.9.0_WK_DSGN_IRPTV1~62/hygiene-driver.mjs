/**
 * TO-IV-e-96 SUPPLEMENTARY driver -- NOT the order's named instrument (scripts/ui-smoke.mjs). ui-smoke cannot type into the
 * header's role=combobox "Client search" (measured: `--fill "Client search=Sample"` times out, see smoke_fill_probe.txt in the
 * evidence folder), so it cannot pick a client, and therefore cannot reach the Holdings face with a client or an account
 * picked. This script replicates ui-smoke's own recipe (auth stub, CORS echo, --dist serving through scripts/ui-dist.mjs,
 * full-page screenshot, the body background as CANVAS) and adds what ui-smoke lacks: typing the search, choosing in the
 * Performance tab's Account select, and request-aware fixtures (a static --fixtures map answers every POST /selections with
 * one body, so a one-account read could not differ from the client read).
 *
 * Usage: node holdings-face-driver.mjs <mode> <out.png> <fixture.json> <dist dir>
 *   mode "client": the client is picked and the Holdings tab opened; no account is chosen anywhere.
 *   mode "picker": the client is picked, then the Performance tab's Account select is set to its SECOND account, then the
 *                  Holdings tab is opened.
 *   mode "back":   as "picker", then "Back to all accounts" is clicked on the Holdings tab.
 * Server model (synthetic): POST /selections with scope_kind CLIENT answers both accounts; scope_kind ACCOUNT answers the one
 * account named by scope_ids[0] (a node ref or an account id). Fixture bodies are synthetic (the files beside this one).
 * No dev server, no port, no network.
 */
import { readFileSync } from 'node:fs'
import { pathToFileURL } from 'node:url'
import { resolve } from 'node:path'

const PORTAL = 'C:/dev/wk-dsgn-irptv1-49/portal'
const { chromium } = await import(pathToFileURL(resolve(PORTAL, 'node_modules/playwright-core/index.mjs')).href)
const { serveFromDist } = await import(pathToFileURL(resolve(PORTAL, 'scripts/ui-dist.mjs')).href)

const [mode, out, fixturePath, dist, measureOut] = process.argv.slice(2)
const PORT = '5199' // an origin string only; nothing listens (--dist routing answers every request)
const ORIGIN = `http://localhost:${PORT}`
const EDGE = 'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe'
const CORS = {
  'Access-Control-Allow-Origin': ORIGIN, 'Access-Control-Allow-Credentials': 'true', 'Access-Control-Allow-Headers': '*',
  'Access-Control-Allow-Methods': '*', 'Content-Type': 'application/json',
}
const SESSION = {
  accessToken: 'ui-smoke-token',
  user: { email: 'dev@opalcapital.com', name: 'Dev User', role: 'admin', userType: 'Dev', firmId: 'opal-capital', firmRole: null, advisorId: null, advisorRole: null, mustChangePassword: false },
}
const K = '/api/scoped/investor-reporting/'
const fixtures = JSON.parse(readFileSync(fixturePath, 'utf8'))
const HKEY = Object.keys(fixtures).find((key) => key.includes(K + 'holdings/'))
const ALL_ID = HKEY.split('/holdings/')[1]
const ALL_BODY = fixtures[HKEY]
const ACCOUNT_NODES = ALL_BODY.data.nodes.filter((n) => n.parent_node_id === null)
const oneId = (k) => ALL_ID.slice(0, -4) + 'a1a' + k // a well-formed set id per account
const oneBody = (k) => {
  const nodes = ALL_BODY.data.nodes
  const body = JSON.parse(JSON.stringify(ALL_BODY))
  const keep = new Set([ACCOUNT_NODES[k].node_id])
  for (let grew = true; grew;) { grew = false; for (const n of nodes) if (!keep.has(n.node_id) && keep.has(n.parent_node_id)) { keep.add(n.node_id); grew = true } }
  body.data.nodes = nodes.filter((n) => keep.has(n.node_id)).map((n) => JSON.parse(JSON.stringify(n))) // W58: copy each node; the ~53 driver mutated ALL_BODY here
  body.data.scope.account_ids = [ACCOUNT_NODES[k].drill_refs[0].ref_id]
  const total = body.data.nodes[0].amount.value
  body.data.custody_totals.total_market_value.value = total
  body.data.custody_totals.unique_account_count = 1
  for (const n of body.data.nodes) { n.amount.denominator.value = total; n.percentages.of_total = n.amount.value / total }
  return body
}
const ONE_BODIES = ACCOUNT_NODES.map((_, k) => oneBody(k))
const accountIndexOf = (id) => Math.max(0, ACCOUNT_NODES.findIndex((n) => n.node_id === id || n.drill_refs[0].ref_id === id))
let selectionPosts = 0
const selectionKey = Object.keys(fixtures).find((key) => key.endsWith('/selections'))
const log = []

process.on('uncaughtException', (e) => { for (const line of log) console.log('LOG   :', line); console.log('FAILED:', String(e).split(String.fromCharCode(10))[0]); process.exit(1) })
const browser = await chromium.launch({ executablePath: EDGE, headless: true })
const page = await browser.newPage({ viewport: { width: 1440, height: 900 } })
const consoleAll = []
page.on('console', (m) => { consoleAll.push({ type: m.type(), text: m.text() }); if (m.type() === 'error') log.push('CONSOLE-ERROR: ' + m.text().slice(0, 240)) })
page.on('pageerror', (e) => log.push('PAGE-CRASH: ' + String(e).slice(0, 200)))
await page.route('**/*', async (r) => {
  const req = r.request()
  const url = req.url()
  if (req.method() === 'OPTIONS' && !url.startsWith(ORIGIN)) return r.fulfill({ status: 204, headers: CORS, body: '' })
  if (req.method() === 'POST' && url.endsWith('/selections')) {
    selectionPosts += 1
    let sent = {}
    try { sent = JSON.parse(req.postData() || '{}') } catch { sent = {} }
    const kind = sent.scope_kind
    const k = kind === 'ACCOUNT' ? accountIndexOf((sent.scope_ids || [])[0]) : -1
    const body = JSON.parse(JSON.stringify(fixtures[selectionKey]))
    body.data.account_set_id = k < 0 ? ALL_ID : oneId(k)
    body.data.account_ids = body.data.selected_account_ids = k < 0 ? ALL_BODY.data.scope.account_ids : ONE_BODIES[k].data.scope.account_ids
    log.push(`POST /selections #${selectionPosts} scope_kind=${kind} -> ${k < 0 ? 'both accounts' : 'account #' + (k + 1)}`)
    return r.fulfill({ status: 200, headers: CORS, body: JSON.stringify(body) })
  }
  if (url.includes(K + 'holdings/')) {
    const k = ACCOUNT_NODES.findIndex((_, idx) => url.includes(oneId(idx)))
    log.push(`GET holdings -> ${k < 0 ? 'both accounts' : 'account #' + (k + 1)}`)
    return r.fulfill({ status: 200, headers: CORS, body: JSON.stringify(k < 0 ? ALL_BODY : ONE_BODIES[k]) })
  }
  const fk = Object.keys(fixtures).sort((a, b) => b.length - a.length).find((key) => url.includes(key))
  if (fk) return r.fulfill({ status: 200, headers: CORS, body: JSON.stringify(fixtures[fk]) })
  if (url.includes('/auth/refresh')) return r.fulfill({ status: 200, headers: CORS, body: JSON.stringify(SESSION) })
  if (await serveFromDist(r, resolve(dist), ORIGIN)) return
  return r.continue()
})
await page.goto(ORIGIN + '/investor-reporting', { waitUntil: 'networkidle', timeout: 30000 }).catch((e) => log.push('goto: ' + e.message.split('\n')[0]))
await page.waitForTimeout(2000)
const box = page.getByRole('combobox', { name: 'Client search', exact: true })
await box.click()
await box.pressSequentially('Sample', { delay: 60 })
await page.waitForTimeout(1500)
await page.getByText('Sample Household').first().click({ timeout: 10000 })
log.push('PICKED the first search row')
await page.waitForTimeout(2500)
if (mode === 'picker' || mode === 'back') {
  await page.locator('select[aria-label="Account"]').selectOption({ index: 1 })
  log.push('CHOSE the second account in the Performance tab Account select')
  await page.waitForTimeout(2000)
}
if (process.env.DRIVER_DEBUG) await page.screenshot({ path: process.env.DRIVER_DEBUG, fullPage: true })
await page.getByRole('button', { name: 'Holdings', exact: true }).or(page.getByRole('tab', { name: 'Holdings', exact: true })).first().click()
await page.waitForTimeout(4000)
if (mode === 'back') {
  await page.locator('[data-slot="holdings-all-accounts"]').first().click()
  log.push('CLICKED Back to all accounts')
  await page.waitForTimeout(1500)
}
const state = await page.evaluate(() => ({
  loc: location.pathname,
  canvas: getComputedStyle(document.body).backgroundColor,
  tiles: [...document.querySelectorAll('[data-slot="holdings-drill-tree"] button[aria-haspopup="dialog"]')].map((b) => b.getAttribute('aria-label')),
  backLink: !!document.querySelector('[data-slot="holdings-all-accounts"]'),
  opening: !!document.querySelector('[data-slot="holdings-account-opening"]'),
}))

const measured = await page.evaluate(() => {
  const parse = (c) => { const m = c.match(/rgba?\(([^)]+)\)/); if (!m) return null; const p = m[1].split(/[ ,/]+/).filter(Boolean).map(Number); return { r: p[0], g: p[1], b: p[2], a: p.length > 3 ? p[3] : 1 } }
  const lin = (v) => { v /= 255; return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4) }
  const lum = (c) => 0.2126 * lin(c.r) + 0.7152 * lin(c.g) + 0.0722 * lin(c.b)
  const ratio = (a, b) => { const la = lum(a), lb = lum(b); return (Math.max(la, lb) + 0.05) / (Math.min(la, lb) + 0.05) }
  const over = (top, under) => ({ r: top.r * top.a + under.r * (1 - top.a), g: top.g * top.a + under.g * (1 - top.a), b: top.b * top.a + under.b * (1 - top.a), a: 1 })
  const hex = (c) => '#' + [c.r, c.g, c.b].map((v) => Math.round(v).toString(16).padStart(2, '0')).join('').toUpperCase()
  const bgOf = (el) => { // effective background: composite ancestors' backgrounds down to the first opaque one
    const stack = []
    let hasImage = false
    for (let n = el; n; n = n.parentElement) {
      const cs = getComputedStyle(n)
      if (cs.backgroundImage && cs.backgroundImage !== 'none') hasImage = true
      const c = parse(cs.backgroundColor)
      if (c && c.a > 0) { stack.push(c); if (c.a >= 1) break }
    }
    let acc = { r: 255, g: 255, b: 255, a: 1 }
    for (let i = stack.length - 1; i >= 0; i--) acc = over(stack[i], acc)
    return { c: acc, hasImage }
  }
  const effOpacity = (el) => { let o = 1; for (let n = el; n; n = n.parentElement) o *= parseFloat(getComputedStyle(n).opacity || '1'); return o }
  const sel = (el) => { const slot = el.closest('[data-slot]'); return (el.tagName.toLowerCase() + (el.getAttribute('data-slot') ? '[' + el.getAttribute('data-slot') + ']' : '') + ' in ' + (slot ? slot.getAttribute('data-slot') : '-')) }
  const texts = []
  const w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT)
  const seen = new Set()
  for (let t = w.nextNode(); t; t = w.nextNode()) {
    const s = (t.nodeValue || '').trim()
    if (!s) continue
    const el = t.parentElement
    if (!el || seen.has(el) || ['SCRIPT', 'STYLE', 'NOSCRIPT'].includes(el.tagName)) continue
    const r = el.getBoundingClientRect()
    const cs = getComputedStyle(el)
    if (cs.visibility === 'hidden' || cs.display === 'none' || r.width === 0 || r.height === 0) continue
    seen.add(el)
    const fg = parse(cs.color); if (!fg) continue
    const { c: bg, hasImage } = bgOf(el)
    const op = effOpacity(el)
    if (op < 0.05) continue
    const fgEff = over({ ...fg, a: fg.a * op }, bg)
    const rg = document.createRange(); rg.selectNodeContents(t); const tr = rg.getBoundingClientRect()
    texts.push({ rect: { x: Math.round(tr.x + scrollX), y: Math.round(tr.y + scrollY), w: Math.round(tr.width), h: Math.round(tr.height) }, fgRaw: { ...fg, a: fg.a * op }, text: s.slice(0, 40), el: sel(el), fg: hex(fgEff), bg: hex(bg), ratio: Math.round(ratio(fgEff, bg) * 100) / 100, bgDark: lum(bg) < 0.18, hasImage, size: cs.fontSize, weight: cs.fontWeight, cls: (el.getAttribute('class') || '').slice(0, 90) })
  }
  const bands = []
  const main = document.querySelector('main') || document.body
  const mw = main.getBoundingClientRect().width
  for (const el of document.body.querySelectorAll('*')) {
    const cs = getComputedStyle(el)
    const c = parse(cs.backgroundColor)
    if (!c || c.a < 0.99 || lum(c) > 0.05) continue
    const r = el.getBoundingClientRect()
    if (r.width < 200 || r.height < 8) continue
    const slot = el.closest('[data-slot]')
    bands.push({ tag: el.tagName.toLowerCase(), bg: hex(c), w: Math.round(r.width), h: Math.round(r.height), x: Math.round(r.x), y: Math.round(r.y + scrollY), slot: el.getAttribute('data-slot') || (slot ? 'in:' + slot.getAttribute('data-slot') : '-'), cls: (el.getAttribute('class') || '').slice(0, 120), text: (el.textContent || '').trim().slice(0, 50), fullWidthOfMain: r.width >= mw * 0.98 })
  }
  const colgroupText = [...document.querySelectorAll('colgroup')].map((cg) => ({ children: cg.childNodes.length, textNodes: [...cg.childNodes].filter((n) => n.nodeType === 3).length }))
  return { texts, bands, mainWidth: Math.round(mw), colgroupText, tokens: { bgBand: getComputedStyle(document.documentElement).getPropertyValue('--bg-band'), bgPage: getComputedStyle(document.documentElement).getPropertyValue('--bg-page'), bgSurface: getComputedStyle(document.documentElement).getPropertyValue('--bg-surface'), bgHeader: getComputedStyle(document.documentElement).getPropertyValue('--bg-header') } }
})
await page.screenshot({ path: out, fullPage: true })

// W62 measurement step 2: a text inside an ancestor that paints a background-image (the Total Assets hero's gradient) has no
// computed background-color to read, so its backdrop is SAMPLED: every text goes transparent, a full-page screenshot is taken,
// and the pixels under the text's own box are read back on a canvas. Both the lightest and darkest sampled pixel are scored
// against the text colour and the LOWER ratio is kept (worst case).
const gradItems = measured.texts.map((t, i) => ({ t, i })).filter(({ t }) => t.hasImage)
if (gradItems.length) {
  await page.addStyleTag({ content: '* { color: transparent !important; -webkit-text-fill-color: transparent !important; text-shadow: none !important; }' })
  const shot = await page.screenshot({ fullPage: true })
  const b64 = shot.toString('base64')
  const rects = gradItems.map(({ t }) => t.rect)
  const sampled = await page.evaluate(async ({ b64, rects }) => {
    const img = new Image(); img.src = 'data:image/png;base64,' + b64; await img.decode()
    const cv = document.createElement('canvas'); cv.width = img.width; cv.height = img.height
    const cx = cv.getContext('2d'); cx.drawImage(img, 0, 0)
    return rects.map((r) => {
      const x = Math.max(0, r.x), y = Math.max(0, r.y), w = Math.max(1, Math.min(r.w, img.width - x)), h = Math.max(1, Math.min(r.h, img.height - y))
      const d = cx.getImageData(x, y, w, h).data
      let lo = null, hi = null, lloLum = 1e9, hhiLum = -1
      for (let k = 0; k < d.length; k += 4) {
        const L = 0.2126 * d[k] + 0.7152 * d[k + 1] + 0.0722 * d[k + 2]
        if (L < lloLum) { lloLum = L; lo = [d[k], d[k + 1], d[k + 2]] }
        if (L > hhiLum) { hhiLum = L; hi = [d[k], d[k + 1], d[k + 2]] }
      }
      return { lo, hi }
    })
  }, { b64, rects })
  const lin = (v) => { v /= 255; return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4) }
  const lumOf = (c) => 0.2126 * lin(c[0]) + 0.7152 * lin(c[1]) + 0.0722 * lin(c[2])
  const hexOf = (c) => '#' + c.map((v) => Math.round(v).toString(16).padStart(2, '0')).join('').toUpperCase()
  gradItems.forEach(({ t }, k) => {
    const sm = sampled[k]; const f = t.fgRaw
    let worst = null
    for (const bgc of [sm.lo, sm.hi]) {
      const eff = [0, 1, 2].map((q) => [f.r, f.g, f.b][q] * f.a + bgc[q] * (1 - f.a))
      const l1 = lumOf(eff), l2 = lumOf(bgc)
      const ra = (Math.max(l1, l2) + 0.05) / (Math.min(l1, l2) + 0.05)
      if (!worst || ra < worst.ratio) worst = { ratio: Math.round(ra * 100) / 100, fg: hexOf(eff), bg: hexOf(bgc) }
    }
    t.sampled = true; t.ratio = worst.ratio; t.fg = worst.fg; t.bg = worst.bg; t.bgDark = lumOf(sm.hi) < 0.18
  })
}
import('node:fs').then((fs) => fs.writeFileSync(measureOut, JSON.stringify({ measured, consoleAll }, null, 1)))
await browser.close()
console.log('MODE  :', mode)
console.log('LOC   :', state.loc)
console.log('CANVAS:', state.canvas)
console.log('TILES :', JSON.stringify(state.tiles))
console.log('BACK-LINK:', state.backLink, ' OPENING-LINE:', state.opening)
for (const line of log) console.log('LOG   :', line)
console.log('SAVED :', out)
