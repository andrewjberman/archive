// One-pass /freshness render for AMGT-az-1. Own driver (the walker has a fixed 1440 viewport and no sort capture);
// uses the walker's own account mechanism (arm / secret / disarm) and its read-only network guard.
import { createRequire } from 'node:module'
import { execFileSync } from 'node:child_process'
import { mkdirSync, writeFileSync } from 'node:fs'
import path from 'node:path'

const ROOT = 'C:/tmp/r76-262'
const require = createRequire(path.join(ROOT, 'portal', 'package.json'))
const { chromium } = require('playwright-core')
const ACCOUNT = path.join(ROOT, '.claude', 'skills', 'ui-walk', 'ui_walker_account.py')
const OUT = path.join(ROOT, 'org/missions/D5/AMGT/AMGT_RESAPP/deliverables/0.9.0_WK_AMGT_RESAPP~262/captures')
mkdirSync(OUT, { recursive: true })
const BASE = 'http://localhost:5174'
const py = (cmd, extraEnv = {}, ...args) => execFileSync('python', [ACCOUNT, cmd, ...args], { encoding: 'utf8', env: { ...process.env, ...extraEnv }, stdio: ['ignore', 'pipe', 'pipe'] })
const ADMITTED_POST = [/\/auth\/login$/, /\/auth\/refresh$/, /\/auth\/logout$/]
const log = (...m) => console.log(new Date().toISOString().slice(11, 19), ...m)
const manifest = []
const guard = []
const apiLog = []
const pathOnly = (u) => { try { return new URL(u).pathname } catch { return u } }

async function guardPage(page) {
  page.on('response', (res) => { const p = pathOnly(res.url()); if (/\/api\//.test(p)) apiLog.push(`${res.request().method()} ${res.status()} ${p}`) })
  await page.route('**/*', (route) => {
    const req = route.request(); const m = req.method(); const p = pathOnly(req.url())
    if (m === 'GET' || m === 'HEAD' || m === 'OPTIONS') return route.continue()
    if (ADMITTED_POST.some((re) => re.test(p))) return route.continue()
    if (/\/analytics\/ingest$/.test(p)) return route.fulfill({ status: 204, body: '' })
    guard.push(`${m} ${p}`)
    return route.abort('blockedbyclient')
  })
}

async function shot(page, file, what, opts = {}) {
  const t = new Date().toISOString()
  await page.screenshot({ path: path.join(OUT, file), fullPage: true, ...opts })
  manifest.push({ file, what, time: t })
  log('SHOT', file)
}

async function firstFive(page) {
  return page.evaluate(() => [...document.querySelectorAll('[data-slot="freshness-table"] tbody tr')].slice(0, 5).map((r) => r.querySelector('td')?.innerText.trim()))
}

let holder = null
let browser
let exitCode = 0
const captions = []
try {
  const armOut = py('arm'); log(armOut.trim())
  holder = (armOut.match(/^HOLDER (\S+)/m) || [])[1] || null
  const password = py('secret', { UI_WALK_CHILD: '1' })
  try { browser = await chromium.launch({ channel: 'msedge', headless: true }) } catch { browser = await chromium.launch({ headless: true }) }

  // sign in once; keep the signed-in state, then every capture below opens in a FRESH context built from it
  const loginCtx = await browser.newContext({ viewport: { width: 1280, height: 900 } })
  const lp = await loginCtx.newPage()
  await guardPage(lp)
  await lp.goto(BASE + '/login', { waitUntil: 'domcontentloaded', timeout: 30000 })
  await lp.fill('#email', 'opal-ui-walker@opal.test')
  await lp.fill('#password', password)
  await lp.click('button[type=submit]')
  await lp.waitForURL((u) => !/\/login/.test(u.pathname), { timeout: 30000 })
  log('LOGGED IN at', lp.url())
  const state = await loginCtx.storageState()
  await loginCtx.close()

  async function freshContext(w, h) {
    const ctx = await browser.newContext({ viewport: { width: w, height: h }, storageState: state })
    const page = await ctx.newPage()
    await guardPage(page)
    return { ctx, page }
  }

  // 1. first visit, fresh context, 1280 wide, with the first-paint time
  {
    const { ctx, page } = await freshContext(1280, 900)
    await page.addInitScript(() => {
      window.__fp = { fp: null, fcp: null }
      new PerformanceObserver((l) => { for (const e of l.getEntries()) { if (e.name === 'first-paint') window.__fp.fp = e.startTime; if (e.name === 'first-contentful-paint') window.__fp.fcp = e.startTime } }).observe({ type: 'paint', buffered: true })
    })
    const t0 = Date.now()
    await page.goto(BASE + '/freshness', { waitUntil: 'domcontentloaded', timeout: 30000 })
    const tNav = Date.now() - t0
    let tHeading = null; let tRows = null
    try { await page.waitForSelector('h1, h2', { timeout: 30000 }); tHeading = Date.now() - t0 } catch {}
    try { await page.waitForSelector('[data-slot="freshness-table"] tbody tr', { timeout: 60000 }); tRows = Date.now() - t0 } catch {}
    const paint = await page.evaluate(() => window.__fp)
    const timing = { domcontentloaded_ms: tNav, heading_ms: tHeading, table_rows_painted_ms: tRows, browser_first_paint_ms: paint.fp && Math.round(paint.fp), browser_first_contentful_paint_ms: paint.fcp && Math.round(paint.fcp) }
    log('FIRST-PAINT', JSON.stringify(timing))
    writeFileSync(path.join(OUT, 'first-paint-time.json'), JSON.stringify({ url: BASE + '/freshness', viewport: '1280x900', fresh_context: true, ...timing }, null, 1))
    await page.waitForTimeout(1500)
    const info = await page.evaluate(() => ({ url: location.href, rows: document.querySelectorAll('[data-slot="freshness-table"] tbody tr').length, summary: document.querySelector('[data-slot="freshness-summary"]')?.innerText || null, note: document.querySelector('[data-slot="uncollected-note"]')?.innerText || null, body: document.body.innerText.slice(0, 300) }))
    log('PAGE', JSON.stringify(info))
    captions.push(`first-visit: url ${info.url}; rows ${info.rows}; summary: ${info.summary}; uncollected note: ${info.note}`)
    await shot(page, '01-first-visit-1280-full.png', `/freshness first visit, fresh context, full page, 1280 px wide; first paint ${timing.browser_first_paint_ms} ms, first contentful paint ${timing.browser_first_contentful_paint_ms} ms, table rows painted ${timing.table_rows_painted_ms} ms from navigation`)
    if (!info.rows) { log('NO ROWS: stopping after the first capture'); await ctx.close(); throw new Error('no table rows rendered: ' + info.body.replace(/\s+/g, ' ')) }

    // 2. each sort button, one capture per sort
    let n = 2
    for (const mode of ['stalest', 'freshest', 'name']) {
      await page.click(`button[data-sort="${mode}"]`)
      await page.waitForTimeout(600)
      const names = await firstFive(page)
      const pressed = await page.evaluate(() => [...document.querySelectorAll('button[data-sort]')].map((b) => `${b.dataset.sort}=${b.getAttribute('aria-pressed')}`).join(' '))
      const f = `0${n}-sort-${mode}-1280-full.png`
      await shot(page, f, `sort "${mode}" pressed (${pressed})`)
      captions.push(`${f}: sort ${mode}; first five rows: ${names.join(' | ')}`)
      n += 1
    }

    // 3. the stated never-collected input above the table, and one row's cells close up
    await page.click('button[data-sort="stalest"]')
    await page.waitForTimeout(400)
    const note = page.locator('[data-slot="uncollected-note"]')
    if (await note.count()) {
      const summary = page.locator('[data-slot="freshness-summary"]').locator('xpath=..')
      await summary.screenshot({ path: path.join(OUT, '05-uncollected-note-closeup.png') })
      manifest.push({ file: '05-uncollected-note-closeup.png', what: 'the summary and the stated never-collected input line above the table (element capture)', time: new Date().toISOString() })
      log('SHOT 05-uncollected-note-closeup.png')
    } else {
      log('NOTE ABSENT: no [data-slot=uncollected-note] on the page'); captions.push('05: uncollected-note element absent on the page')
      await page.locator('[data-slot="freshness-view"]').screenshot({ path: path.join(OUT, '05-uncollected-note-closeup.png') })
      manifest.push({ file: '05-uncollected-note-closeup.png', what: 'NO uncollected-note element on the page; the view container above the table instead', time: new Date().toISOString() })
    }
    const row = page.locator('[data-slot="freshness-table"] tbody tr').first()
    await row.screenshot({ path: path.join(OUT, '06-row-cells-closeup.png') })
    manifest.push({ file: '06-row-cells-closeup.png', what: 'first row (stalest first), cells close up for contrast', time: new Date().toISOString() })
    log('SHOT 06-row-cells-closeup.png')
    const contrast = await page.evaluate(() => {
      const lum = (c) => { const m = c.match(/[\d.]+/g).map(Number); const f = (v) => { v /= 255; return v <= 0.03928 ? v / 12.92 : ((v + 0.055) / 1.055) ** 2.4 }; return 0.2126 * f(m[0]) + 0.7152 * f(m[1]) + 0.0722 * f(m[2]) }
      const cv = document.createElement('canvas'); cv.width = cv.height = 1; const cx = cv.getContext('2d', { willReadFrequently: true })
      const rgb = (c) => { cx.clearRect(0, 0, 1, 1); cx.fillStyle = '#fff'; cx.fillRect(0, 0, 1, 1); cx.fillStyle = c; cx.fillRect(0, 0, 1, 1); const d = cx.getImageData(0, 0, 1, 1).data; return `rgb(${d[0]},${d[1]},${d[2]})` }
      const ground = (el) => { for (let e = el; e; e = e.parentElement) { const b = getComputedStyle(e).backgroundColor; const m = b.match(/[\d.]+/g); if (m && (m.length < 4 || Number(m[3]) > 0.99)) return rgb(b) } return 'rgb(255,255,255)' }
      const read = (el) => { if (!el) return null; const ink = rgb(getComputedStyle(el).color); const g = ground(el); const a = lum(ink); const b = lum(g); return { ink, ground: g, ratio: +((Math.max(a, b) + 0.05) / (Math.min(a, b) + 0.05)).toFixed(2) } }
      const r = document.querySelector('[data-slot="freshness-table"] tbody tr')
      const out = { first_row_name_cell: read(r?.querySelector('td')), first_row_input_cell: read(r?.querySelector('td[data-input]')), first_row_stale_cell: read(r?.querySelector('[data-slot="stale-flags"]')), uncollected_note: read(document.querySelector('[data-slot="uncollected-note"]')) }
      const unc = document.querySelector('td[data-state="uncollected"]'); out.uncollected_input_cell = read(unc)
      return out
    })
    log('CONTRAST', JSON.stringify(contrast))
    writeFileSync(path.join(OUT, 'contrast-readings.json'), JSON.stringify(contrast, null, 1))
    await ctx.close()
  }

  // 4. the page at 1280 and at 390, each in its own fresh context
  for (const [w, h, f] of [[1280, 800, '07-width-1280-full.png'], [390, 844, '08-width-390-full.png']]) {
    const { ctx, page } = await freshContext(w, h)
    await page.goto(BASE + '/freshness', { waitUntil: 'domcontentloaded', timeout: 30000 })
    await page.waitForSelector('[data-slot="freshness-table"] tbody tr', { timeout: 60000 }).catch(() => {})
    await page.waitForTimeout(1500)
    const m = await page.evaluate(() => ({ scrollW: document.documentElement.scrollWidth, innerW: innerWidth }))
    captions.push(`${f}: viewport ${w}; document scrollWidth ${m.scrollW} vs innerWidth ${m.innerW}${m.scrollW > m.innerW ? ' (HORIZONTAL OVERFLOW)' : ''}`)
    await shot(page, f, `/freshness full page at ${w} px wide (document scrollWidth ${m.scrollW}, innerWidth ${m.innerW})`)
    await ctx.close()
  }
  writeFileSync(path.join(OUT, '..', 'captions.txt'), captions.join('\n') + '\n')
  writeFileSync(path.join(OUT, '..', 'capture-manifest.json'), JSON.stringify({ manifest, guard_aborts: guard, api: apiLog }, null, 1))
} catch (e) {
  exitCode = 1
  console.log('ERROR', e.message)
  try { writeFileSync(path.join(OUT, '..', 'captions.txt'), captions.join('\n') + '\nERROR ' + e.message + '\n'); writeFileSync(path.join(OUT, '..', 'capture-manifest.json'), JSON.stringify({ manifest, guard_aborts: guard, api: apiLog, error: e.message }, null, 1)) } catch {}
} finally {
  if (browser) await browser.close().catch(() => {})
  if (holder) { try { log(py('disarm', {}, holder).trim()) } catch (e) { log('DISARM FAILED', String(e.stderr || e.message).slice(0, 300)); exitCode = 2 } }
  process.exitCode = exitCode
}
