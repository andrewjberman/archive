// rb14-harness.mjs -- 0.9.0_WK_DSGN_REBRND~1, TO-RB-s-14. Ran from <WS>/.scratch/; the deliverables copy
// is committed as evidence and differs from the run only in this comment. It never contains extract.js.
// Drives the taste skill's extract.js (READ IN PLACE from the main workspace, never copied,
// never edited) inside portal routes at 1440x900 with the Playwright library ui-smoke uses.
// The auth stub, CORS echo and fixture routing are ui-smoke.mjs's, reproduced verbatim in intent.
import { readFileSync, writeFileSync } from 'node:fs'
import { createRequire } from 'node:module'
import { createHash } from 'node:crypto'

const require = createRequire('C:/tmp/wk-dsgn-1j/portal/package.json')
const { chromium } = require('playwright-core')

const EXTRACT = 'C:/Users/AndrewBerman/Desktop/ajb_workspace/.claude/skills/taste/references/extract.js'
const OUTDIR = 'C:/tmp/wk-dsgn-1j/org/missions/D13/DSGN/DSGN_REBRND/deliverables/0.9.0_WK_DSGN_REBRND~1'
const FIXDIR = 'C:/tmp/wk-dsgn-1j/portal/.frontend-dev/testing'
const PORT = process.argv[2] || '5190'
const ORIGIN = `http://localhost:${PORT}`
const EDGE = 'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe'

const src = readFileSync(EXTRACT, 'utf8')
const extractSha = createHash('sha256').update(src).digest('hex')
// Invocation, not an edit: the file is one arrow-function expression followed by ';'.
const expr = '(' + src.trim().replace(/;\s*$/, '') + ')()'
console.log('EXTRACTOR:', EXTRACT, 'bytes', Buffer.byteLength(src), 'sha256', extractSha)

const ROUTES = [
  { route: '/market', fixture: 'rb-s-9-market.json' },
  { route: '/positioning', fixture: 'rb-s-9-attribution.json' },
  { route: '/portfolio-management', fixture: null },
]

const CORS = {
  'Access-Control-Allow-Origin': ORIGIN,
  'Access-Control-Allow-Credentials': 'true',
  'Access-Control-Allow-Headers': '*',
  'Access-Control-Allow-Methods': '*',
  'Content-Type': 'application/json',
}
const SESSION = {
  accessToken: 'ui-smoke-token',
  user: { email: 'dev@opalcapital.com', name: 'Dev User', role: 'admin',
          userType: 'Dev', firmId: 'opal-capital', firmRole: null, advisorId: null,
          advisorRole: null, mustChangePassword: false },
}

// Measurements of IV.3 dimensions that extract.js does not take. Labelled separately in output.
const extras = () => {
  const cs = (el) => getComputedStyle(el)
  const fam = (s) => (s.fontFamily || '').split(',')[0].replace(/['"]/g, '').trim()
  const ownText = (el) => Array.from(el.childNodes).filter(n => n.nodeType === 3).map(n => n.textContent).join('').trim()
  const rendered = (el) => { const s = cs(el); if (s.display === 'none' || s.visibility === 'hidden') return false; const r = el.getBoundingClientRect(); return r.width > 0 && r.height > 0 }
  // numerals: every rendered element whose OWN text carries a digit
  const numFam = new Map(), numVar = new Map(); let numN = 0
  for (const el of document.body.querySelectorAll('*')) {
    const t = ownText(el)
    if (!t || !/\d/.test(t) || !rendered(el)) continue
    numN++
    const s = cs(el)
    numFam.set(fam(s), (numFam.get(fam(s)) || 0) + 1)
    numVar.set(s.fontVariantNumeric, (numVar.get(s.fontVariantNumeric) || 0) + 1)
  }
  // chart colours: fills/strokes of rendered svg shapes inside chart containers
  const chart = new Map(); let chartShapes = 0
  const chartRoots = document.querySelectorAll('.recharts-wrapper, .apexcharts-canvas, svg[role=application], [class*=nivo], .visx')
  for (const root of chartRoots) {
    for (const el of root.querySelectorAll('path, rect, circle, polygon, line, ellipse')) {
      const r = el.getBoundingClientRect(); if (!(r.width > 0 || r.height > 0)) continue
      const s = cs(el); chartShapes++
      for (const p of ['fill', 'stroke']) {
        const v = s[p]; if (!v || v === 'none' || v.startsWith('url')) continue
        const k = p + ' ' + v; chart.set(k, (chart.get(k) || 0) + 1)
      }
    }
  }
  // status + chart tokens as COMPUTED custom properties on :root
  const names = new Set()
  for (const sheet of document.styleSheets) {
    let rules; try { rules = sheet.cssRules } catch (_) { continue }
    for (const rule of rules || []) {
      if (!rule.style) continue
      for (let i = 0; i < rule.style.length; i++) { const n = rule.style[i]; if (n.startsWith('--')) names.add(n) }
    }
  }
  const root = cs(document.documentElement)
  const tok = (re) => Array.from(names).filter(n => re.test(n)).sort().slice(0, 80)
    .map(n => [n, root.getPropertyValue(n).trim()]).filter(([, v]) => v)
  const top = (m, n) => Array.from(m.entries()).sort((a, b) => b[1] - a[1]).slice(0, n).map(([value, count]) => ({ value, count }))
  // any stylesheet rule that suppresses focus outlines
  const outlineNone = []
  for (const sheet of document.styleSheets) {
    let rules; try { rules = sheet.cssRules } catch (_) { continue }
    for (const rule of rules || []) {
      const t = rule.cssText || ''
      if (/outline:\s*(none|0)[^;]*!important/.test(t)) outlineNone.push(t.slice(0, 160))
    }
  }
  return {
    colorScheme: { html: root.colorScheme, body: cs(document.body).colorScheme },
    htmlBackground: root.backgroundColor,
    bodyBackground: cs(document.body).backgroundColor,
    numerals: { elementsWithDigits: numN, families: top(numFam, 8), fontVariantNumeric: top(numVar, 6) },
    chart: { roots: chartRoots.length, shapes: chartShapes, colours: top(chart, 16) },
    statusTokens: tok(/status|success|error|danger|destructive|warning|positive|negative|info/i),
    chartTokens: tok(/^--(chart|series|data-)/i),
    radiusTokens: tok(/radius/i),
    outlineNoneImportantRules: outlineNone.slice(0, 10),
  }
}

const browser = await chromium.launch({ executablePath: EDGE, headless: true })
for (const { route, fixture } of ROUTES) {
  const fixtures = fixture ? JSON.parse(readFileSync(`${FIXDIR}/${fixture}`, 'utf8')) : {}
  const keys = Object.keys(fixtures).sort((a, b) => b.length - a.length)
  const hits = new Set(); let live = 0, liveNon2xx = 0
  const page = await browser.newPage({ viewport: { width: 1440, height: 900 } })
  page.on('pageerror', e => console.log('PAGE-CRASH:', route, String(e).slice(0, 200)))
  page.on('response', res => { const u = res.url(); if (u.includes('/api/') && !keys.some(k => u.includes(k))) { live++; if (res.status() >= 300) liveNon2xx++ } })
  await page.route('**/*', r => {
    const req = r.request(); const url = req.url()
    if (req.method() === 'OPTIONS' && !url.startsWith(ORIGIN)) return r.fulfill({ status: 204, headers: CORS, body: '' })
    const k = keys.find(key => url.includes(key))
    if (k) { hits.add(k); return r.fulfill({ status: 200, headers: CORS, body: JSON.stringify(fixtures[k]) }) }
    if (url.includes('/auth/refresh')) return r.fulfill({ status: 200, headers: CORS, body: JSON.stringify(SESSION) })
    return r.continue()
  })
  await page.goto(ORIGIN + route, { waitUntil: 'networkidle', timeout: 30000 }).catch(e => console.log('goto:', e.message.split('\n')[0]))
  await page.waitForTimeout(3000)
  const loc = await page.evaluate(() => location.pathname)
  const dom = await page.evaluate(expr)
  const ext = await page.evaluate(extras)
  const slug = route.replace(/^\//, '')
  const png = `${OUTDIR}/rb-s-14_${slug}_extract_1440.png`
  await page.screenshot({ path: png, fullPage: true })
  const height = await page.evaluate(() => document.documentElement.scrollHeight)
  // focus ring: first Tab stop from a blurred document, read as painted
  await page.evaluate(() => { document.activeElement && document.activeElement.blur && document.activeElement.blur(); window.scrollTo(0, 0) })
  await page.keyboard.press('Tab')
  await page.waitForTimeout(300)
  const focus = await page.evaluate(() => {
    const el = document.activeElement; if (!el || el === document.body) return { element: null }
    const s = getComputedStyle(el)
    return { element: el.tagName.toLowerCase() + (el.getAttribute('aria-label') ? `[aria-label="${el.getAttribute('aria-label')}"]` : ''),
      text: (el.textContent || '').trim().slice(0, 40), matchesFocusVisible: el.matches(':focus-visible'),
      outlineStyle: s.outlineStyle, outlineWidth: s.outlineWidth, outlineColor: s.outlineColor, outlineOffset: s.outlineOffset, boxShadow: s.boxShadow }
  })
  const out = { route, url: ORIGIN + route, landed: loc, fixture: fixture ? `portal/.frontend-dev/testing/${fixture}` : null,
    fixturesDeclared: keys.length, fixturesMatched: hits.size, liveApiResponses: live, liveApiNon2xx: liveNon2xx,
    documentHeightPx: height, screenshot: png,
    extractor: { path: EXTRACT, sha256: extractSha, pinnedRepo: 'senlindesign/taste-skill', pinnedSha: '6dce223f2f' },
    extract: dom, extras: { ...ext, focusFirstTabStop: focus } }
  const jf = `${OUTDIR}/rb-s-14_extract_${slug}.json`
  writeFileSync(jf, JSON.stringify(out, null, 2) + '\n')
  console.log(`ROUTE ${route} LOC ${loc} fixtures ${hits.size}/${keys.length} live-api ${live} (non-2xx ${liveNon2xx}) height ${height}`)
  console.log('  pageBackground', dom.colors && dom.colors.pageBackground, 'bg', JSON.stringify(dom.colors && dom.colors.backgroundColors))
  console.log('  families', JSON.stringify(dom.typography && dom.typography.uniqueFamilies))
  console.log('  radii', JSON.stringify(dom.effects && dom.effects.radii), 'shadows', JSON.stringify(dom.effects && dom.effects.shadows))
  console.log('  focusVisible', dom.focusVisible, 'reducedMotion', dom.reducedMotion, 'errors', JSON.stringify(dom.errors))
  console.log('  color-scheme', JSON.stringify(ext.colorScheme), 'focus', JSON.stringify(focus))
  console.log('  SAVED', jf, png)
  await page.close()
}
await browser.close()
