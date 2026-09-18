// rb-s-13_capture.mjs -- RB-s-13 coverage harness (0.9.0_WK_DSGN_REBRND~3). One browser, one fresh context per job.
// Mechanism is ui-smoke.mjs's, unchanged in substance: system Edge headless, 1440x900 viewport, the /auth/refresh
// stub with ui-smoke's own SESSION, exact-origin credentialed CORS, full-page PNG, CANVAS printed from
// getComputedStyle(document.body).backgroundColor. It ADDS what ui-smoke cannot do, so each inventory STATE is
// constructed rather than hoped for:
//   mode default  -- the row's ui-smoke-shaped fixture if one exists, else the live dev plane (inert token)
//   mode empty    -- every data request (/api/*, /v1/*) answered 200 with its fixture body emptied (arrays -> [])
//                    or [] when no fixture exists
//   mode loading  -- every data request HELD (never answered); captured 2.5 s after load
//   mode error    -- every data request answered 503
//   auth none     -- /auth/refresh answered 401 (a signed-out visitor: the public auth routes)
//   respond       -- {substring: {status, body, hold}} for named endpoints (auth POSTs)
//   steps         -- click (role button|tab by exact name), clicktext, fill (#selector=text), press (key)
// and a KEYBOARD WALK for rows with keyboard_obligation: Tab from a blurred document, one clipped screenshot per
// stop, the focused element, :focus-visible and the painted ring recorded; then one contact sheet of every stop's
// screenshot rendered by the same browser. Usage: node rb-s-13_capture.mjs <port> <plan.json> <outdir> [probe]
import { createRequire } from 'node:module'
import { mkdirSync, writeFileSync, readFileSync } from 'node:fs'
const require = createRequire('C:/tmp/wk-dsgn-3b/portal/package.json')
const { chromium } = require('playwright-core')

const [port, planPath, outdir, probeFlag] = process.argv.slice(2)
const PROBE = probeFlag === 'probe'
const ORIGIN = `http://localhost:${port}`
const EDGE = 'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe'
const VW = 1440, VH = 900, MAXSTOPS = 60
const CORS = { 'Access-Control-Allow-Origin': ORIGIN, 'Access-Control-Allow-Credentials': 'true',
  'Access-Control-Allow-Headers': '*', 'Access-Control-Allow-Methods': '*', 'Content-Type': 'application/json' }
const baseSession = () => ({ accessToken: 'ui-smoke-token', user: { email: 'dev@opalcapital.com', name: 'Dev User',
  role: 'admin', userType: 'Dev', firmId: 'opal-capital', firmRole: null, advisorId: null, advisorRole: null,
  mustChangePassword: false } })
const plan = JSON.parse(readFileSync(planPath, 'utf8'))
mkdirSync(`${outdir}/walks`, { recursive: true })

const isData = (url) => {
  if (!url.startsWith(ORIGIN)) return false
  const p = new URL(url).pathname
  return p.startsWith('/api/') || p.startsWith('/v1/')
}
const emptied = (v) => Array.isArray(v) ? [] : (v && typeof v === 'object')
  ? Object.fromEntries(Object.entries(v).map(([k, x]) => [k, emptied(x)])) : v

const browser = await chromium.launch({ executablePath: EDGE, headless: true })
const results = []
for (const job of plan) {
  const context = await browser.newContext({ viewport: { width: VW, height: VH } })
  const page = await context.newPage()
  const crashes = []
  page.on('pageerror', (e) => crashes.push(String(e).slice(0, 200)))
  const fixtures = job.fixtures ? JSON.parse(readFileSync(job.fixtures, 'utf8')) : {}
  const fkeys = Object.keys(fixtures).sort((a, b) => b.length - a.length)
  const respond = job.respond || {}
  const session = baseSession()
  Object.assign(session.user, job.claims || {})
  const counts = { data: 0, fixtured: 0, held: 0, failed: 0, emptied: 0, live: 0 }
  await page.route('**/*', (r) => {
    const req = r.request(); const url = req.url()
    if (req.method() === 'OPTIONS' && !url.startsWith(ORIGIN)) return r.fulfill({ status: 204, headers: CORS, body: '' })
    for (const [k, spec] of Object.entries(respond)) {
      if (url.includes(k)) {
        if (spec.hold) { counts.held++; return }
        return r.fulfill({ status: spec.status || 200, headers: CORS, body: JSON.stringify(spec.body ?? {}) })
      }
    }
    if (url.includes('/auth/refresh')) {
      if (job.auth === 'hold') { counts.held++; return }
      if (job.auth === 'none') return r.fulfill({ status: 401, headers: CORS, body: JSON.stringify({ error: 'no session' }) })
      return r.fulfill({ status: 200, headers: CORS, body: JSON.stringify(session) })
    }
    if (isData(url)) {
      counts.data++
      const fk = fkeys.find((k) => url.includes(k))
      if (job.mode === 'loading') { counts.held++; return }
      if (job.mode === 'error') { counts.failed++; return r.fulfill({ status: 503, headers: CORS, body: JSON.stringify({ error: 'rb-s-13 forced failure' }) }) }
      if (job.mode === 'empty') { counts.emptied++; return r.fulfill({ status: 200, headers: CORS, body: JSON.stringify(fk ? emptied(fixtures[fk]) : []) }) }
      if (fk) { counts.fixtured++; return r.fulfill({ status: 200, headers: CORS, body: JSON.stringify(fixtures[fk]) }) }
      counts.live++
    }
    return r.continue()
  })
  const loading = job.mode === 'loading' || job.auth === 'hold'
  await page.goto(ORIGIN + job.route, { waitUntil: loading ? 'load' : 'networkidle', timeout: 30000 })
    .catch((e) => console.log('goto:', e.message.split('\n')[0]))
  await page.waitForTimeout(loading ? 2500 : 3000)

  if (PROBE) {
    const ctl = await page.evaluate(() => {
      const main = document.querySelector('main') || document.body
      return [...main.querySelectorAll('[role=tab],button,[aria-pressed]')].filter((e) => {
        const rc = e.getBoundingClientRect(); return rc.width > 0 && rc.height > 0 })
        .map((e) => (e.getAttribute('role') || e.tagName.toLowerCase()) + ':' + (e.getAttribute('aria-label') || (e.textContent || '').trim()).replace(/\s+/g, ' ').slice(0, 30)).slice(0, 45)
    })
    console.log('PROBE', job.route, '| LOC', new URL(page.url()).pathname, '|', JSON.stringify(ctl))
    await context.close(); continue
  }

  const stepLog = []
  for (const s of job.steps || []) {
    try {
      if (s.kind === 'click') {
        const byName = { name: s.arg, exact: true }
        await page.getByRole('button', byName).or(page.getByRole('tab', byName)).first().click({ timeout: 8000 })
      } else if (s.kind === 'clicktext') {
        await page.locator(`text=${JSON.stringify(s.arg)}`).first().click({ timeout: 8000 })
      } else if (s.kind === 'fill') {
        const i = s.arg.indexOf('='); await page.fill(s.arg.slice(0, i), s.arg.slice(i + 1), { timeout: 8000 })
      } else if (s.kind === 'press') {
        await page.keyboard.press(s.arg)
      }
      stepLog.push('OK ' + s.kind + ' ' + s.arg)
    } catch (e) { stepLog.push('FAIL ' + s.kind + ' ' + s.arg + ' -- ' + e.message.split('\n')[0]) }
    await page.waitForTimeout(s.wait ?? 1500)
  }

  const st = await page.evaluate(() => ({
    loc: location.pathname + location.search,
    canvas: getComputedStyle(document.body).backgroundColor,
    text: document.body.innerText.replace(/\s+/g, ' ').slice(0, 220),
    busy: document.querySelectorAll('[aria-busy="true"],[role=status]').length,
    alerts: document.querySelectorAll('[role=alert]').length,
    charts: document.querySelectorAll('.recharts-wrapper,.apexcharts-canvas,svg[role=img]').length,
  }))
  const png = `${outdir}/${job.png}`
  await page.screenshot({ path: png, fullPage: true })
  const rec = { key: job.key, route: job.route, state: job.state, mode: job.mode, fixtures: job.fixtures || null,
    counts, steps: stepLog, crashes, ...st, png: job.png }
  const landed = st.loc.split('?')[0] === job.route.split('?')[0]
  console.log(`=== ${job.key}  -> ${job.png}`)
  console.log('LOC   :', st.loc, landed ? '' : '<-- DID NOT LAND')
  console.log('CANVAS:', st.canvas)
  console.log('NET   :', JSON.stringify(counts), '| busy', st.busy, '| alerts', st.alerts, '| charts', st.charts, '| crashes', crashes.length)
  if (stepLog.length) console.log('STEPS :', stepLog.join(' ; '))
  console.log('TEXT  :', st.text)

  if (job.kb) {
    const slug = job.png.replace(/\.png$/, '')
    await page.evaluate(() => { window.scrollTo(0, 0); window.__seen = new Set(); if (document.activeElement) document.activeElement.blur() })
    const stops = []; let wrapped = false; let segRun = 0; let segTotal = 0
    for (let i = 1; i <= MAXSTOPS; i++) {
      await page.keyboard.press('Tab'); await page.waitForTimeout(120)
      // WRAP RULE (revised after the first read of the sheets): only a return to the FIRST stop is a wrap. A Tab that
      // leaves focus on the SAME element as the previous stop is a segment move inside a composite control (a native
      // date input tabs mm -> dd -> yyyy without changing document.activeElement) and is skipped, capped at 8 in a row.
      // The first run treated any re-seen element as a wrap, which ended four walks at their first date input.
      const info = await page.evaluate(() => {
        const el = document.activeElement
        if (!el || el === document.body) return { body: true }
        if (el === window.__last) return { segment: true }
        if (el === window.__first) return { wrapped: true }
        if (window.__seen.has(el)) return { wrapped: true, anomaly: true }
        window.__seen.add(el)
        if (!window.__first) window.__first = el
        window.__last = el
        const cs = getComputedStyle(el); const rc = el.getBoundingClientRect()
        const ring = (cs.boxShadow && cs.boxShadow !== 'none') || (cs.outlineStyle !== 'none' && parseFloat(cs.outlineWidth) > 0)
        return { tag: el.tagName.toLowerCase(), role: el.getAttribute('role') || '',
          text: (el.getAttribute('aria-label') || el.innerText || el.value || el.getAttribute('placeholder') || '').trim().replace(/\s+/g, ' ').slice(0, 34),
          fv: el.matches(':focus-visible'), ring, inShell: !!el.closest('aside'),
          x: rc.x, y: rc.y, w: rc.width, h: rc.height }
      })
      if (info.wrapped) { wrapped = true; if (info.anomaly) console.log('KBD-ANOMALY: a non-first element was re-seen at press', i); break }
      if (info.segment) { segRun++; segTotal++; if (segRun > 8) { console.log('KBD-SEGMENT-CAP at press', i); break } continue }
      segRun = 0
      if (info.body) { stops.push({ i, body: true }); continue }
      const pad = 14
      const x = Math.max(0, Math.floor(info.x - pad)), y = Math.max(0, Math.floor(info.y - pad))
      const w = Math.min(Math.ceil(info.w + 2 * pad), 460, VW - x), h = Math.min(Math.ceil(info.h + 2 * pad), 160, VH - y)
      let clip = null
      if (w > 4 && h > 4 && y < VH) {
        const buf = await page.screenshot({ clip: { x, y, width: w, height: h } }).catch(() => null)
        if (buf) clip = buf.toString('base64')
      }
      stops.push({ ...info, i, clip })
    }
    const walked = stops.filter((s) => !s.body)
    const tiles = walked.map((s) => `<div class=t><div class=c>#${s.i} ${s.tag}${s.role ? '[' + s.role + ']' : ''} ${s.inShell ? 'SHELL' : 'PAGE'} fv=${s.fv ? 'Y' : 'N'} ring=${s.ring ? 'Y' : 'N'}<br>${(s.text || '').replace(/[<&]/g, '')}</div>` +
      (s.clip ? `<img src="data:image/png;base64,${s.clip}">` : '<div class=n>offscreen / no clip</div>') + '</div>').join('')
    const html = `<html><body style="margin:0;background:#ddd;font:11px Arial"><div style="padding:6px;font-weight:bold">${job.key} -- keyboard walk: ${walked.length} stops ${wrapped ? '(WRAPPED: whole tab order)' : '(cap ' + MAXSTOPS + ')'}</div><div style="display:flex;flex-wrap:wrap;gap:4px;padding:4px">${tiles}</div>` +
      '<style>.t{background:#fff;border:1px solid #999;width:230px;padding:2px}.t img{max-width:226px;max-height:90px;display:block}.c{height:30px;overflow:hidden}.n{color:#a00}</style></body></html>'
    const sheetPage = await context.newPage()
    await sheetPage.setContent(html)
    const sheet = `${outdir}/walks/${slug}_kbd-sheet.png`
    await sheetPage.screenshot({ path: sheet, fullPage: true })
    await sheetPage.close()
    const log = walked.map(({ clip, ...rest }) => rest)
    writeFileSync(`${outdir}/walks/${slug}_kbd.json`, JSON.stringify({ key: job.key, wrapped, cap: MAXSTOPS, stops: log }, null, 1))
    const fvN = walked.filter((s) => s.fv).length, ringN = walked.filter((s) => s.ring).length
    const pageN = walked.filter((s) => !s.inShell).length
    console.log('KBD   :', walked.length, 'stops', wrapped ? '(WRAPPED)' : `(cap ${MAXSTOPS})`, '| page stops', pageN, '| focus-visible', fvN, 'of', walked.length, '| ring painted', ringN, 'of', walked.length, '| sheet', sheet)
    rec.kbd = { stops: walked.length, wrapped, pageStops: pageN, fv: fvN, ring: ringN, sheet: `walks/${slug}_kbd-sheet.png` }
  }
  results.push(rec)
  await context.close()
}
if (!PROBE) writeFileSync(`${outdir}/rb-s-13_capture-log_${plan.length}_${Date.now()}.json`, JSON.stringify(results, null, 1))
await browser.close()
