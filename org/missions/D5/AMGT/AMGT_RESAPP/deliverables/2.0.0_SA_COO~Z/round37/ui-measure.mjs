/**
 * ui-measure.mjs -- DOM measurements for the AMGT_RESAPP frontend walk (4.0.0_SA_CRO~Z, 2026-09-24).
 * Same auth stub + fixture router as portal/scripts/ui-smoke.mjs (copied, not imported), then a
 * measurement pass instead of a screenshot. Prints ONE JSON object.
 *
 *   node ui-measure.mjs <route> [--port 5175] [--fixtures f.json] [--click "<name>"]... [--width 1440]
 */
import { chromium } from 'playwright-core'
import { readFileSync } from 'node:fs'

const args = process.argv.slice(2)
let route = args[0]
const msys = route.match(/^[A-Za-z]:.*?\/Git\/(.+)$/i)
if (msys) route = msys[1]
route = '/' + route.replace(/^\/+/, '')
const port = args.includes('--port') ? args[args.indexOf('--port') + 1] : '5175'
const fixturesPath = args.includes('--fixtures') ? args[args.indexOf('--fixtures') + 1] : null
const fixtures = fixturesPath ? JSON.parse(readFileSync(fixturesPath, 'utf8')) : {}
const widthArg = args.includes('--width') ? Number(args[args.indexOf('--width') + 1]) : 1440
const clicks = args.reduce((acc, a, i) => (a === '--click' && args[i + 1] ? [...acc, args[i + 1]] : acc), [])
const ORIGIN = `http://localhost:${port}`
const EDGE = 'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe'
const CORS = { 'Access-Control-Allow-Origin': ORIGIN, 'Access-Control-Allow-Credentials': 'true',
  'Access-Control-Allow-Headers': '*', 'Access-Control-Allow-Methods': '*', 'Content-Type': 'application/json' }
const SESSION = { accessToken: 'ui-smoke-token', user: { email: 'dev@opalcapital.com', name: 'Dev User', role: 'admin',
  userType: 'Dev', firmId: 'opal-capital', firmRole: null, advisorId: null, advisorRole: null, mustChangePassword: false } }
const fkeys = Object.keys(fixtures).sort((a, b) => b.length - a.length)
const matchFixture = url => fkeys.find(k => url.includes(k))

const browser = await chromium.launch({ executablePath: EDGE, headless: true })
const page = await browser.newPage({ viewport: { width: widthArg, height: 900 } })
const errors = []
page.on('pageerror', e => errors.push(String(e).slice(0, 200)))
await page.route('**/*', async r => {
  const req = r.request(); const url = req.url()
  if (req.method() === 'OPTIONS' && !url.startsWith(ORIGIN)) return r.fulfill({ status: 204, headers: CORS, body: '' })
  const fk = matchFixture(url)
  if (fk) return r.fulfill({ status: 200, headers: CORS, body: JSON.stringify(fixtures[fk]) })
  if (url.includes('/auth/refresh')) return r.fulfill({ status: 200, headers: CORS, body: JSON.stringify(SESSION) })
  return r.continue()
})
await page.goto(ORIGIN + route, { waitUntil: 'networkidle', timeout: 30000 }).catch(() => {})
await page.waitForTimeout(3000)
for (const name of clicks) {
  try { await page.getByRole('tab', { name, exact: true }).first().click({ timeout: 2000 }) }
  catch { try { await page.getByRole('button', { name, exact: true }).first().click({ timeout: 2000 }) } catch (e) { errors.push('click-fail:' + name) } }
  await page.waitForTimeout(2500)
}

const m = await page.evaluate(() => {
  const lum = (r, g, b) => { const f = v => { v /= 255; return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4) }; return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b) }
  const parse = s => { const x = /rgba?\(([^)]+)\)/.exec(s || ''); if (!x) return null; const p = x[1].split(',').map(v => parseFloat(v)); return { r: p[0], g: p[1], b: p[2], a: p.length > 3 ? p[3] : 1 } }
  const contrast = (a, b) => { const l1 = lum(a.r, a.g, a.b), l2 = lum(b.r, b.g, b.b); return (Math.max(l1, l2) + 0.05) / (Math.min(l1, l2) + 0.05) }
  const ground = el => { let e = el; while (e) { const bg = parse(getComputedStyle(e).backgroundColor); if (bg && bg.a > 0) return { c: bg, el: e }; e = e.parentElement } return { c: { r: 244, g: 246, b: 250, a: 1 }, el: null } }
  const vis = el => { const r = el.getBoundingClientRect(); const cs = getComputedStyle(el); return r.width > 0 && r.height > 0 && cs.display !== 'none' && cs.visibility !== 'hidden' }
  const isBand = c => c && Math.abs(c.r - 10) < 3 && Math.abs(c.g - 23) < 3 && Math.abs(c.b - 51) < 3
  const all = Array.from(document.querySelectorAll('body *')).filter(vis)
  // 1. dark containers (band-valued backgrounds) -- count distinct top-level ones
  const bandEls = all.filter(el => { const bg = parse(getComputedStyle(el).backgroundColor); return bg && bg.a > 0 && isBand(bg) })
  const bandTop = bandEls.filter(el => !bandEls.some(o => o !== el && o.contains(el)))
  // 2. text nodes: contrast vs ground, font family/weight, size
  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT)
  let n; const texts = []
  while ((n = walker.nextNode())) { const t = n.textContent.replace(/\s+/g, ' ').trim(); if (!t) continue; const el = n.parentElement; if (!el || !vis(el)) continue; texts.push({ el, t }) }
  let low = 0, lowSamples = [], fonts = {}, weights = {}, sizes = {}, chars = 0, onBandChars = 0, onLightChars = 0, monospace = 0
  for (const { el, t } of texts) {
    const cs = getComputedStyle(el); const fg = parse(cs.color); const g = ground(el)
    chars += t.length; if (isBand(g.c)) onBandChars += t.length; else onLightChars += t.length
    const fam = cs.fontFamily.split(',')[0].replace(/"/g, ''); fonts[fam] = (fonts[fam] || 0) + t.length
    weights[cs.fontWeight] = (weights[cs.fontWeight] || 0) + t.length
    const sz = Math.round(parseFloat(cs.fontSize)); sizes[sz] = (sizes[sz] || 0) + t.length
    if (/mono/i.test(cs.fontFamily)) monospace += t.length
    if (fg) { const eff = fg.a < 1 ? { r: fg.r * fg.a + g.c.r * (1 - fg.a), g: fg.g * fg.a + g.c.g * (1 - fg.a), b: fg.b * fg.a + g.c.b * (1 - fg.a) } : fg
      const ratio = contrast(eff, g.c); if (ratio < 4.5 && t.length > 1) { low += t.length; if (lowSamples.length < 12) lowSamples.push({ text: t.slice(0, 50), ratio: +ratio.toFixed(2), fg: cs.color, bg: `rgb(${Math.round(g.c.r)},${Math.round(g.c.g)},${Math.round(g.c.b)})`, size: sz }) } }
  }
  // 3. paragraphs (block-ish elements) by length -- walls of text
  const blocks = all.filter(el => ['P', 'LI', 'TD', 'DIV', 'SPAN', 'H1', 'H2', 'H3'].includes(el.tagName) && el.children.length === 0 && el.innerText && el.innerText.trim().length > 0)
  const longBlocks = blocks.map(el => ({ tag: el.tagName, len: el.innerText.trim().length, w: Math.round(el.getBoundingClientRect().width), text: el.innerText.trim().slice(0, 60) })).filter(b => b.len >= 240).sort((a, b) => b.len - a.len)
  // 4. radii, shadows, opacity idioms
  const radii = {}; let shadows = 0; let translucent = 0
  for (const el of all) { const cs = getComputedStyle(el); const r = cs.borderTopLeftRadius; if (r && r !== '0px') radii[r] = (radii[r] || 0) + 1; if (cs.boxShadow && cs.boxShadow !== 'none') shadows++; const bg = parse(cs.backgroundColor); if (bg && bg.a > 0 && bg.a < 1) translucent++; const fg = parse(cs.color); if (fg && fg.a < 1 && el.innerText && el.innerText.trim()) translucent++ }
  // 5. overlaps between visible sibling elements with text (a crude "overlapping chaos" signal)
  let overlaps = 0; const overlapSamples = []
  const cands = all.filter(el => el.children.length === 0 && el.innerText && el.innerText.trim().length > 3)
  for (let i = 0; i < cands.length; i++) { const a = cands[i].getBoundingClientRect(); for (let j = i + 1; j < cands.length; j++) { if (cands[i].contains(cands[j]) || cands[j].contains(cands[i])) continue; const b = cands[j].getBoundingClientRect(); const ix = Math.min(a.right, b.right) - Math.max(a.left, b.left); const iy = Math.min(a.bottom, b.bottom) - Math.max(a.top, b.top); if (ix > 4 && iy > 4) { overlaps++; if (overlapSamples.length < 6) overlapSamples.push([cands[i].innerText.trim().slice(0, 30), cands[j].innerText.trim().slice(0, 30)]) } } }
  // 6. panels + purple spend + tables
  const panels = all.filter(el => el.className && typeof el.className === 'string' && /\bborder\b/.test(el.className) && parse(getComputedStyle(el).backgroundColor) && parse(getComputedStyle(el).backgroundColor).a > 0 && el.getBoundingClientRect().width > 300)
  const purple = all.filter(el => { const bg = parse(getComputedStyle(el).backgroundColor); return bg && bg.a > 0 && Math.abs(bg.r - 95) < 4 && Math.abs(bg.g - 59) < 4 && Math.abs(bg.b - 227) < 4 })
  const tables = document.querySelectorAll('table').length
  const tabs = Array.from(document.querySelectorAll('[role=tab]')).map(t => t.innerText.trim())
  return { loc: location.pathname, canvas: getComputedStyle(document.body).backgroundColor, pageHeight: document.documentElement.scrollHeight,
    visibleElements: all.length, bandContainersTopLevel: bandTop.length, bandContainersAll: bandEls.length, panelsOver300px: panels.length,
    textChars: chars, onBandChars, onLightChars, lowContrastChars: low, lowContrastSamples: lowSamples, fonts, weights, sizes, monospaceChars: monospace,
    longBlocksOver240: longBlocks.length, longestBlocks: longBlocks.slice(0, 8), radii, shadows, translucentPaints: translucent, overlaps, overlapSamples,
    purpleFills: purple.length, tables, tabs, bodyTextHead: document.body.innerText.replace(/\s+/g, ' ').slice(0, 200) }
})
m.errors = errors
console.log(JSON.stringify(m))
await browser.close()
