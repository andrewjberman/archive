/**
 * POSN_AGGFIX.TO-B2-1 (slot ~3) -- <AGG_DOM_B2>: THE HOLDINGS TAB'S AGGREGATE BOOK, READ FROM THE RENDERED DOM.
 *
 * The render mechanism is TO-B1-1's <FIVE_BOOKS_DOM_B> (b_five_books_dom.mjs), COPIED rather than imported because that
 * file runs its own main on import: system Edge, the stubbed /auth/refresh session per viewer class (same VIEWERS),
 * vite started from THIS worktree's portal on a port checked free, every unfixtured /api/ /v1/ /auth/ or remote request
 * answered 404 and listed. The fixtures are b_fixtures.mjs's (pinned by VersionId, md5-refused), with the aggregate
 * fixture OK by default and --aggregate-fixture unavailable selecting the contract 1.1 UNAVAILABLE payload.
 *
 * Arms (run from the workspace root; each prints what it reads and a verdict-inputs line; EXIT=0 only when the arm's
 * expectation is met):
 *   --viewer opal-staff --remembered none               B2-AC2  lands on Aggregate; entry first; counts; Model Breakdown
 *   --viewer opal-staff --remembered ST                 B2-AC3  lands on ST; then Aggregate renders both panels
 *   --viewer advisor-and-client --remembered AGG        B2-AC4  no entry, ordinary landing, 0 requests, no group
 *   --viewer opal-staff --legibility                    B2-AC6  WCAG ratios for the group's cells + a reference column
 *   --viewer opal-staff --aggregate-fixture unavailable B2-AC7  no entry, ordinary landing, no group, no page error
 *   [--port <p>] default 5242
 *
 * TO-B3-1 (the same slot) ADDS ONE OPTION and changes no arm above it: --fixtures <dir> replaces the VersionId-pinned
 * fixtures with the LIVE bytes <LIVE_FIXTURES_B3> wrote to <dir> -- the NEW shared file (the version TO-A3-1's run
 * produced) and the live opal_aggregate.json -- keeping the attribution and ETF feeds pinned. B3-AC3 runs the
 * --remembered none arm that way; its screenshot is written under its own name so TO-B2-1's is never overwritten.
 *
 * THE STORAGE KEY a remembered book is read from is usePersistentToggle's: prefix 'opal:toggle:v1:' + HoldingsTab's
 * `positioning:book:${bookMode}` -- set in sessionStorage once per tab, before any page script runs.
 */
import { createRequire } from 'node:module'
import { spawn, spawnSync } from 'node:child_process'
import { readFileSync } from 'node:fs'
import { createHash } from 'node:crypto'
import net from 'node:net'
import path from 'node:path'
import { fileURLToPath } from 'node:url'
import { buildFixtures, AGG_URLKEY } from './b_fixtures.mjs'

const HERE = path.dirname(fileURLToPath(import.meta.url))
const git = (args, cwd) => spawnSync('git', args, { cwd, encoding: 'utf8' })
const ROOT = git(['rev-parse', '--show-toplevel'], HERE).stdout.trim()
const PORTAL = path.join(ROOT, 'portal')
const require = createRequire(path.join(PORTAL, 'package.json'))
const { chromium } = require('playwright-core')

const args = process.argv.slice(2)
const flag = (f) => args.includes(f)
const opt = (f, d = null) => (args.includes(f) ? args[args.indexOf(f) + 1] : d)
const PORT = Number(opt('--port', '5242'))
const ORIGIN = `http://localhost:${PORT}`
const EDGE = 'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe'
const MB_CODES = ['UST', 'ST', 'INT', 'LT', 'ULT']
const BOOK_KEY = 'opal:toggle:v1:positioning:book:models'
const FAMILY_KEY = 'opal:toggle:v1:positioning:book-family'
const PREFERRED_DEFAULT_BOOK = 'INT'   // shared/bookSet.ts PREFERRED_DEFAULT_BOOK -- the ordinary default model
const sleep = (ms) => new Promise((r) => setTimeout(r, ms))
const CORS = {
  'Access-Control-Allow-Origin': ORIGIN,
  'Access-Control-Allow-Credentials': 'true',
  'Access-Control-Allow-Headers': '*',
  'Access-Control-Allow-Methods': '*',
  'Content-Type': 'application/json',
}

// THE CLAIM SETS -- identical to b_five_books_dom.mjs VIEWERS (row POSN_AGGFIX-Z-W3-S2 for the constructed client).
const VIEWERS = {
  'opal-staff': { email: 'staff@opalcapital.com', name: 'Opal Staff', role: 'user', userType: null,
    firmId: 'opal-capital', firmRole: null, advisorId: null, advisorRole: null, mustChangePassword: false },
  advisor: { email: 'advisor@49financial.test', name: 'Partner Advisor', role: 'user', userType: null,
    firmId: '49financial', firmRole: 'user', advisorId: 'b-harness-advisor', advisorRole: 'architect',
    mustChangePassword: false },
  client: { email: 'client@49financial.test', name: 'Partner Client', role: 'user', userType: null,
    firmId: '49financial', firmRole: null, advisorId: null, advisorRole: null, mustChangePassword: false },
}

function portalState() {
  const head = git(['rev-parse', 'HEAD'], PORTAL).stdout.trim()
  const dirty = git(['status', '--porcelain', '--', 'src'], PORTAL).stdout.trim()
  const branch = git(['rev-parse', '--abbrev-ref', 'HEAD'], PORTAL).stdout.trim()
  return { head, branch, src_dirty: dirty }
}

function portFree(p) {
  return new Promise((res) => {
    const s = net.createServer()
    s.once('error', () => res(false))
    s.once('listening', () => s.close(() => res(true)))
    s.listen(p, 'localhost')
  })
}

async function startVite() {
  if (!(await portFree(PORT))) throw new Error('BLOCKED: port ' + PORT + ' is already in use')
  const vite = path.join(PORTAL, 'node_modules', 'vite', 'bin', 'vite.js')
  const child = spawn(process.execPath, [vite, '--configLoader', 'runner', '--port', String(PORT), '--strictPort'],
    { cwd: PORTAL, stdio: ['ignore', 'pipe', 'pipe'] })
  let log = ''
  child.stdout.on('data', (d) => { log += d })
  child.stderr.on('data', (d) => { log += d })
  const t0 = Date.now()
  while (Date.now() - t0 < 120000) {
    if (child.exitCode !== null) throw new Error('vite exited early: ' + log.slice(-800))
    try {
      const r = await fetch(ORIGIN + '/')
      if (r.ok) {
        console.log('SERVER: vite from ' + PORTAL + ' on ' + ORIGIN + ' ready in ' + (Date.now() - t0) + ' ms (pid ' + child.pid + ')')
        return child
      }
    } catch { /* not up yet */ }
    await sleep(500)
  }
  child.kill()
  throw new Error('vite did not answer within 120 s: ' + log.slice(-800))
}

async function stopVite(child) {
  if (!child || child.exitCode !== null) return
  child.kill()
  for (let i = 0; i < 40 && child.exitCode === null; i++) await sleep(250)
  console.log('SERVER: stopped (exitCode ' + child.exitCode + ', signal ' + child.signalCode + ')')
}

async function openViewer(browser, viewer, fixtures, remembered) {
  const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 } })
  const init = [[FAMILY_KEY, 'models']]
  if (remembered) init.push([BOOK_KEY, remembered])
  await ctx.addInitScript((pairs) => {
    // Once per TAB, not per navigation: a vite dependency re-optimise reloads the page, and re-seeding then would
    // overwrite what the page itself wrote (a selection) with the harness's starting value.
    try {
      if (!window.sessionStorage.getItem('b2-harness-seeded')) {
        for (const [k, v] of pairs) window.sessionStorage.setItem(k, v)
        window.sessionStorage.setItem('b2-harness-seeded', '1')
      }
    } catch { /* none */ }
  }, init)
  const page = await ctx.newPage()
  const requests = []
  const unfixtured = []
  const errors = []
  let aggServed = 0
  page.on('request', (r) => requests.push(r.method() + ' ' + r.url()))
  page.on('pageerror', (e) => errors.push(String(e).slice(0, 300)))
  const session = { accessToken: 'b-harness-token', user: VIEWERS[viewer] }
  const keys = Object.keys(fixtures).sort((a, b) => b.length - a.length)
  await page.route('**/*', (r) => {
    const req = r.request()
    const url = req.url()
    if (req.method() === 'OPTIONS' && !url.startsWith(ORIGIN)) return r.fulfill({ status: 204, headers: CORS, body: '' })
    const k = keys.find((key) => url.includes(key))
    if (k) {
      if (k === AGG_URLKEY) aggServed += 1
      return r.fulfill({ status: 200, headers: CORS, body: JSON.stringify(fixtures[k]) })
    }
    if (url.includes('/auth/refresh')) return r.fulfill({ status: 200, headers: CORS, body: JSON.stringify(session) })
    const u = new URL(url)
    const api = /^\/(api|v1|auth)\//.test(u.pathname)
    if (url.startsWith(ORIGIN) && !api) return r.continue()
    unfixtured.push(req.method() + ' ' + url)
    return r.fulfill({ status: 404, headers: CORS, body: '{"error":"b-harness: not fixtured"}' })
  })
  await page.goto(ORIGIN + '/positioning', { waitUntil: 'domcontentloaded', timeout: 120000 })
  return { ctx, page, requests, unfixtured, errors, aggServed: () => aggServed }
}

// ---- THE READ ------------------------------------------------------------------------------------------------
const readView = (page) => page.evaluate(() => {
  const norm = (s) => (s || '').replace(/\u00a0/g, ' ').replace(/[ \t]+/g, ' ').trim()
  const textOf = (el) => {
    if (!el) return ''
    if (typeof el.innerText === 'string') return el.innerText
    const html = el.querySelector && Array.from(el.querySelectorAll('*')).find((x) => typeof x.innerText === 'string')
    return html ? html.innerText : (el.textContent || '')
  }
  const leafTitled = (t) => Array.from(document.querySelectorAll('h1,h2,h3,h4,span,div,p'))
    .find((e) => e.childElementCount === 0 && norm(e.textContent) === t)
  const panelOf = (t) => { const e = leafTitled(t); return e ? e.closest('div.space-y-6 > *') : null }
  const pressed = (label) => {
    const g = document.querySelector('[role="group"][aria-label="' + label + '"]')
    if (!g) return { entries: [], selected: null }
    const bs = Array.from(g.querySelectorAll('button'))
    const sel = bs.find((b) => b.getAttribute('aria-pressed') === 'true')
    return { entries: bs.map((b) => norm(b.textContent)), selected: sel ? norm(sel.textContent) : null }
  }
  const comp = panelOf('Portfolio Composition')
  const brk = panelOf('Holdings Breakdown')
  const svg = comp ? comp.querySelector('svg.recharts-surface') : null
  const table = brk ? brk.querySelector('table') : null
  const headRows = table ? Array.from(table.querySelectorAll('thead > tr')).map((tr) =>
    Array.from(tr.children).map((c) => norm(c.textContent))) : []
  const bodyRows = table ? Array.from(table.querySelectorAll('tbody > tr'))
    .filter((tr) => (tr.getAttribute('class') || '').includes('hover:bg-white/5'))
    .map((tr) => Array.from(tr.children).map((c) => norm(c.textContent))) : []
  return {
    loc: location.pathname,
    family: pressed('Book family'),
    book: pressed('Book'),
    composition: {
      // A treemap ENTRY is a data node recharts lays out (one depth-1 layer per holding); a node too small for its
      // content draws nothing, so the drawn rects and the labelled tiles are printed beside it, never substituted.
      nodes: svg ? svg.querySelectorAll('g.recharts-treemap-depth-1').length : 0,
      rects: svg ? svg.querySelectorAll('g.recharts-treemap-depth-1 rect').length : 0,
      labelled: svg ? svg.querySelectorAll('foreignObject').length : 0,
      empty: comp && !svg ? norm(textOf(comp)).slice(0, 200) : null,
    },
    breakdown: { head: headRows, holding_rows: bodyRows.length, rows: bodyRows,
      empty: brk && !table ? norm(textOf(brk)).slice(0, 200) : null },
    thead_text: table ? norm(table.querySelector('thead').textContent) : '',
    body_text_has_mb: /model breakdown/i.test(document.body.textContent || ''),
  }
})

// Settle: the condition holds on three consecutive identical reads.
async function settle(page, ok, what, timeout = 180000) {
  const t0 = Date.now()
  let last = null
  let stable = 0
  while (Date.now() - t0 < timeout) {
    let v = null
    try { v = await readView(page) } catch { v = null }
    if (v && ok(v)) {
      const sig = JSON.stringify(v)
      stable = sig === last ? stable + 1 : 0
      last = sig
      if (stable >= 2) return v
    } else { stable = 0; last = null }
    await sleep(700)
  }
  throw new Error('TIMEOUT waiting for ' + what + ' -- last read: ' + (last || 'none').slice(0, 400))
}

// A page load is SETTLED for these arms when Models is pressed, the selector has entries and the breakdown shows rows or
// its empty state; then 4 s more (every query the mount enables has answered, and the landing that follows the
// aggregate's arrival has run); then the same condition on three identical reads.
async function settleLoad(s, label) {
  const ready = (v) => v.family.selected === 'Models' && v.book.entries.length > 0 &&
    (v.breakdown.holding_rows > 0 || v.breakdown.empty !== null)
  await settle(s.page, ready, label + ' first paint')
  await sleep(4000)
  return settle(s.page, ready, label + ' after the aggregate window')
}

const shot = async (page, name) => {
  const p = path.join(HERE, name)
  await page.screenshot({ path: p, fullPage: true })
  console.log('SCREENSHOT: ' + path.relative(ROOT, p))
}

const aggReqs = (s) => s.requests.filter((u) => u.includes('opal_aggregate.json')).length

// ---- MAIN ----------------------------------------------------------------------------------------------------
const st = portalState()
console.log('PORTAL: ' + PORTAL + '  branch ' + st.branch + '  HEAD ' + st.head + '  src working-tree changes: ' +
  (st.src_dirty ? JSON.stringify(st.src_dirty) : 'NONE'))
console.log('ARGS: ' + args.join(' '))

let exit = 1
let server = null
let browser = null
try {
  const unavailable = opt('--aggregate-fixture') === 'unavailable'
  if (opt('--aggregate-fixture') && !unavailable) throw new Error('usage: --aggregate-fixture unavailable')
  const liveDir = opt('--fixtures')
  let fx
  if (liveDir) {
    // ---- B3-AC3: the NEW shared file and the LIVE aggregate bytes, as <LIVE_FIXTURES_B3> wrote them ----
    if (unavailable) throw new Error('usage: --fixtures and --aggregate-fixture unavailable are exclusive')
    const dir = path.resolve(liveDir)
    const rd = (n) => {
      const p = path.join(dir, n)
      const b = readFileSync(p)
      console.log('LIVE FIXTURE FILE ' + path.relative(ROOT, p) + ' bytes=' + b.length +
        ' md5=' + createHash('md5').update(b).digest('hex'))
      return JSON.parse(b.toString('utf8'))
    }
    const newShared = rd('new_shared.json')
    const aggregate = rd('aggregate.json')
    const posnKey = '/api/general/positioning/positioning_data.json'
    const attrKey = '/api/general/positioning/holdings_attribution_data.json'
    const etfKey = '/api/general/etfs/positioning_data.json'
    const base = buildFixtures(ROOT)
    base.lines.filter((l) => l.includes(attrKey) || l.includes(etfKey)).forEach((l) => console.log('PINNED ' + l))
    fx = { fixtures: { [posnKey]: newShared, [attrKey]: base.fixtures[attrKey], [etfKey]: base.fixtures[etfKey],
      [AGG_URLKEY]: aggregate }, lines: [] }
    console.log('SHARED FILE (live, NEW): current_holdings ' + JSON.stringify(Object.keys(newShared.current_holdings)) +
      ' generated_at ' + newShared.generated_at)
    console.log('AGGREGATE (live bytes): status=' + aggregate.status + ' generated_at=' + aggregate.generated_at +
      ' AGG holdings=' + aggregate.current_holdings.AGG.holdings.length)
  } else {
    fx = buildFixtures(ROOT, unavailable ? { aggregate: 'unavailable' } : {})
    fx.lines.forEach((l) => console.log(l))
  }
  // The OK payload's holdings are the reference count for every arm; the UNAVAILABLE arm reads its own (empty) block.
  const okFx = unavailable ? buildFixtures(ROOT).fixtures[AGG_URLKEY] : fx.fixtures[AGG_URLKEY]
  const fxHoldings = okFx.current_holdings.AGG.holdings
  const classes = {}
  fxHoldings.forEach((h) => { classes[h.asset_class] = (classes[h.asset_class] || 0) + 1 })
  console.log('FIXTURE AGG (status OK payload): holdings=' + fxHoldings.length + ' asset_class histogram=' + JSON.stringify(classes))
  server = await startVite()
  browser = await chromium.launch({ executablePath: EDGE, headless: true })
  const viewerArg = opt('--viewer')
  const remembered = opt('--remembered')

  if (viewerArg === 'opal-staff' && remembered === 'none' && !flag('--legibility') && !unavailable) {
    // ---- B2-AC2 ----
    const s = await openViewer(browser, 'opal-staff', fx.fixtures, null)
    try {
      const v = await settleLoad(s, 'opal-staff fresh')
      console.log('LOC: ' + v.loc + '  FAMILY PRESSED: ' + v.family.selected)
      console.log('SELECTOR ENTRIES: ' + JSON.stringify(v.book.entries))
      console.log('SELECTOR FIRST ENTRY: ' + JSON.stringify(v.book.entries[0]))
      console.log('SELECTED BOOK LABEL (the landing): ' + JSON.stringify(v.book.selected))
      console.log('REQUESTS TO opal_aggregate.json: ' + aggReqs(s) + ' (served ' + s.aggServed() + ')')
      console.log('COMPOSITION: data nodes=' + v.composition.nodes + ' drawn rects=' + v.composition.rects +
        ' labelled tiles=' + v.composition.labelled + '  (fixture AGG holdings=' + fxHoldings.length + ')')
      console.log('BREAKDOWN: holding rows=' + v.breakdown.holding_rows + '  (fixture AGG holdings=' + fxHoldings.length + ')')
      v.breakdown.head.forEach((cells, i) => console.log('  THEAD row ' + (i + 1) + ': ' + JSON.stringify(cells)))
      const groupRow = v.breakdown.head[0] || []
      const colRow = v.breakdown.head[1] || []
      const wi = colRow.indexOf('Weight')
      const afterWeight = colRow.slice(wi + 1, wi + 1 + 5)
      console.log('COLUMN GROUP AFTER BASIC INFO: ' + JSON.stringify(groupRow[1]))
      console.log('COLUMNS AFTER Weight: ' + JSON.stringify(afterWeight))
      const labelPresent = /all of opal/i.test(v.thead_text)
      console.log('"All of Opal" label in the table header: ' + labelPresent)
      // Three sampled tickers: the fixture's first, middle and last holding (fixture order, fixed by VersionId).
      const idx = [0, Math.floor(fxHoldings.length / 2), fxHoldings.length - 1]
      let sampleOk = 0
      for (const i of idx) {
        const h = fxHoldings[i]
        const want = MB_CODES.map((c) => { const x = h.model_breakdown?.[c]; return x ? (x * 100).toFixed(1) : '-' })
        const row = v.breakdown.rows.find((r) => r[2] === h.ticker)
        const got = row ? row.slice(5, 10) : null
        const same = !!got && JSON.stringify(got) === JSON.stringify(want)
        if (same) sampleOk += 1
        console.log('  SAMPLE ' + h.ticker.padEnd(6) + ' model_breakdown=' + JSON.stringify(h.model_breakdown) +
          '  expected ' + JSON.stringify(want) + '  rendered ' + JSON.stringify(got) + '  ' + (same ? 'EQUAL' : 'DIFFERENT'))
      }
      console.log('SAMPLES EQUAL: ' + sampleOk + ' of ' + idx.length)
      console.log('PAGE ERRORS: ' + s.errors.length + (s.errors.length ? ' ' + JSON.stringify(s.errors) : '') +
        '  UNFIXTURED(404) distinct: ' + new Set(s.unfixtured).size)
      await shot(s.page, liveDir ? 'b3_ac3_opal_staff_live_aggregate.png' : 'b2_ac2_opal_staff_lands_on_aggregate.png')
      const ok = v.book.selected === 'Aggregate' && v.book.entries[0] === 'Aggregate' &&
        v.composition.nodes === fxHoldings.length && v.breakdown.holding_rows === fxHoldings.length &&
        JSON.stringify(afterWeight) === JSON.stringify(MB_CODES) && /model breakdown/i.test(groupRow[1] || '') &&
        labelPresent && sampleOk === 3 && s.errors.length === 0
      console.log('VERDICT INPUTS MET: ' + ok)
      exit = ok ? 0 : 1
    } finally { await s.ctx.close() }
  } else if (viewerArg === 'opal-staff' && remembered === 'ST') {
    // ---- B2-AC3 ----
    const s = await openViewer(browser, 'opal-staff', fx.fixtures, 'ST')
    try {
      const v = await settleLoad(s, 'opal-staff remembered ST')
      console.log('SEEDED sessionStorage ' + BOOK_KEY + ' = "ST" before load')
      console.log('SELECTOR ENTRIES: ' + JSON.stringify(v.book.entries))
      console.log('SELECTED BOOK LABEL (the landing): ' + JSON.stringify(v.book.selected))
      console.log('REQUESTS TO opal_aggregate.json: ' + aggReqs(s) + ' (served ' + s.aggServed() + ')')
      await shot(s.page, 'b2_ac3_opal_staff_remembered_st.png')
      await s.page.getByRole('group', { name: 'Book' }).getByRole('button', { name: 'Aggregate', exact: true }).click()
      const a = await settle(s.page, (x) => x.book.selected === 'Aggregate' && x.breakdown.holding_rows > 0, 'Aggregate after click')
      console.log('AFTER SELECTING Aggregate: selected=' + JSON.stringify(a.book.selected) + ' composition data nodes=' +
        a.composition.nodes + ' (drawn rects ' + a.composition.rects + ', labelled ' + a.composition.labelled + ')' +
        ' breakdown holding rows=' + a.breakdown.holding_rows + '  (fixture AGG holdings=' + fxHoldings.length + ')')
      await shot(s.page, 'b2_ac3_opal_staff_then_aggregate.png')
      console.log('PAGE ERRORS: ' + s.errors.length)
      const ok = v.book.selected === 'ST' && a.composition.nodes === fxHoldings.length && a.breakdown.holding_rows === fxHoldings.length
      console.log('VERDICT INPUTS MET: ' + ok)
      exit = ok ? 0 : 1
    } finally { await s.ctx.close() }
  } else if (viewerArg === 'advisor-and-client' && remembered === 'AGG') {
    // ---- B2-AC4 ----
    let allOk = true
    for (const viewer of ['advisor', 'client']) {
      const s = await openViewer(browser, viewer, fx.fixtures, 'AGG')
      try {
        const v = await settleLoad(s, viewer + ' remembered AGG')
        const stored = await s.page.evaluate((k) => window.sessionStorage.getItem(k), BOOK_KEY)
        const hasEntry = v.book.entries.some((e) => /aggregate|^agg$/i.test(e))
        const n = aggReqs(s)
        console.log(viewer.toUpperCase() + ': SEEDED ' + BOOK_KEY + ' = "AGG" before load; after load it reads ' + JSON.stringify(stored))
        console.log('  SELECTOR ENTRIES: ' + JSON.stringify(v.book.entries) + '  Aggregate entry present: ' + hasEntry)
        console.log('  SELECTED BOOK LABEL (the landing): ' + JSON.stringify(v.book.selected) + '  ordinary default model: ' + PREFERRED_DEFAULT_BOOK)
        console.log('  REQUESTS TO opal_aggregate.json: ' + n + ' (of ' + s.requests.length + ' requests)')
        console.log('  MODEL BREAKDOWN GROUP IN THE DOM: ' + v.body_text_has_mb + '  "All of Opal" in the table header: ' + /all of opal/i.test(v.thead_text))
        console.log('  PAGE ERRORS: ' + s.errors.length)
        await shot(s.page, 'b2_ac4_' + viewer + '_remembered_agg.png')
        const ok = !hasEntry && v.book.selected === PREFERRED_DEFAULT_BOOK && n === 0 && !v.body_text_has_mb
        console.log('  VERDICT INPUTS MET (' + viewer + '): ' + ok)
        allOk = allOk && ok
      } finally { await s.ctx.close() }
    }
    exit = allOk ? 0 : 1
  } else if (viewerArg === 'opal-staff' && flag('--legibility')) {
    // ---- B2-AC6 ----
    const s = await openViewer(browser, 'opal-staff', fx.fixtures, null)
    try {
      const v = await settleLoad(s, 'opal-staff legibility')
      console.log('SELECTED BOOK LABEL: ' + JSON.stringify(v.book.selected) + '  (the measurement needs the group on screen)')
      const m = await s.page.evaluate((codes) => {
        // ANY CSS colour -> sRGB rgba, through a 1x1 canvas. Computed styles here are not all rgb(): Tailwind v4 classes
        // serialize as oklch()/oklab() (the first run's rgb-only parser returned null on the reference column and threw).
        // A value CSS itself does not accept as a colour is refused (null), never painted as the canvas's previous fill.
        const cv = document.createElement('canvas')
        cv.width = 1
        cv.height = 1
        const cx = cv.getContext('2d', { willReadFrequently: true })
        const toRgba = (css) => {
          if (!css || css === 'transparent') return { r: 0, g: 0, b: 0, a: 0 }
          if (!CSS.supports('color', css)) return null
          cx.clearRect(0, 0, 1, 1)
          cx.fillStyle = css
          cx.fillRect(0, 0, 1, 1)
          const d = cx.getImageData(0, 0, 1, 1).data
          return { r: d[0], g: d[1], b: d[2], a: Math.round((d[3] / 255) * 1000) / 1000 }
        }
        const COLOR_TOKEN = /(rgba?\([^)]*\)|hsla?\([^)]*\)|oklch\([^)]*\)|oklab\([^)]*\)|color\([^)]*\)|#[0-9a-fA-F]{3,8})/
        // For a background-image, the FIRST colour of a gradient (every gradient on these cells is single-colour).
        const parse = (c) => {
          if (!c) return null
          if (/gradient\(/.test(c)) {
            const t = c.match(COLOR_TOKEN)
            return t ? toRgba(t[1]) : null
          }
          return toRgba(c)
        }
        const lum = ({ r, g, b }) => {
          const f = (v) => { v /= 255; return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4) }
          return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b)
        }
        const ratio = (a, b) => { const la = lum(a); const lb = lum(b); return (Math.max(la, lb) + 0.05) / (Math.min(la, lb) + 0.05) }
        const over = (top, base) => ({ r: top.r * top.a + base.r * (1 - top.a), g: top.g * top.a + base.g * (1 - top.a),
          b: top.b * top.a + base.b * (1 - top.a), a: 1 })
        const hex = (c) => '#' + [c.r, c.g, c.b].map((v) => Math.round(v).toString(16).padStart(2, '0')).join('')
        const measure = (label, textEl) => {
          const ink = parse(getComputedStyle(textEl).color)
          // THE CRITERION'S MEASURE: the computed background of the nearest ancestor whose background-color is opaque.
          let el = textEl
          const chain = []
          let opaque = null
          while (el && el.nodeType === 1) {
            const s2 = getComputedStyle(el)
            const bg = parse(s2.backgroundColor)
            const img = s2.backgroundImage && s2.backgroundImage !== 'none' ? s2.backgroundImage : null
            chain.push({ bg, img })
            if (bg && bg.a === 1) { opaque = { el, bg }; break }
            el = el.parentElement
          }
          // BESIDE IT, THE EFFECTIVE GROUND: from that opaque ancestor inward, every gradient tint and translucent
          // background-color composited over it (a single-colour linear-gradient is read as its colour).
          let eff = opaque ? { ...opaque.bg } : { r: 255, g: 255, b: 255, a: 1 }
          for (let i = chain.length - 1; i >= 0; i--) {
            const c = chain[i]
            if (i < chain.length - 1 && c.bg && c.bg.a > 0 && c.bg.a < 1) eff = over(c.bg, eff)
            if (c.img) { const t = parse(c.img); if (t) eff = over(t, eff) }
          }
          const inkEff = ink.a < 1 ? over(ink, eff) : ink
          return {
            label, text: (textEl.textContent || '').trim(), ink: hex(ink) + (ink.a < 1 ? ' a=' + ink.a : ''),
            opaque_ancestor: opaque ? opaque.el.tagName.toLowerCase() + ' ' + hex(opaque.bg) : 'NONE',
            ratio_opaque: opaque ? Math.round(ratio(inkEff, opaque.bg) * 100) / 100 : null,
            effective_ground: hex(eff), ratio_effective: Math.round(ratio(inkEff, eff) * 100) / 100,
          }
        }
        const table = Array.from(document.querySelectorAll('table')).find((t) => /model breakdown/i.test(t.querySelector('thead')?.textContent || ''))
        if (!table) return { error: 'no table carries a Model Breakdown group' }
        const ths = Array.from(table.querySelectorAll('thead > tr')[1].children)
        const bodyRow = Array.from(table.querySelectorAll('tbody > tr')).find((tr) => (tr.getAttribute('class') || '').includes('hover:bg-white/5'))
        const tds = Array.from(bodyRow.children)
        const ticker = (tds[2]?.textContent || '').trim()
        const out = { group: [], reference: [] }
        const wi = ths.findIndex((t) => (t.textContent || '').trim() === 'Weight')
        codes.forEach((code, k) => {
          const th = ths[wi + 1 + k]
          out.group.push(measure('header ' + code, th.querySelector('span') || th))
          const td = tds[wi + 1 + k]
          out.group.push(measure('body ' + code + ' (' + ticker + ')', td.querySelector('span') || td))
        })
        const yi = ths.findIndex((t) => (t.textContent || '').trim() === 'Yield')
        out.reference.push(measure('REFERENCE header Yield', ths[yi].querySelector('span') || ths[yi]))
        out.reference.push(measure('REFERENCE body Yield (' + ticker + ')', tds[yi].querySelector('span') || tds[yi]))
        const g = table.querySelector('thead > tr').children[1]
        out.group_label = measure('group label', g.querySelector('span') || g)
        return out
      }, MB_CODES)
      if (m.error) throw new Error(m.error)
      const line = (x) => '  ' + x.label.padEnd(26) + ' text=' + JSON.stringify(x.text).padEnd(8) + ' ink ' + x.ink +
        '  nearest opaque ancestor ' + x.opaque_ancestor + '  ratio ' + x.ratio_opaque +
        '  | effective ground ' + x.effective_ground + '  ratio ' + x.ratio_effective
      console.log('MODEL BREAKDOWN -- five header cells and one body cell per column (WCAG 2.1 contrast):')
      m.group.forEach((x) => console.log(line(x)))
      console.log('GROUP LABEL (not in the criterion, printed):')
      console.log(line(m.group_label))
      console.log('REFERENCE -- one existing column beside them:')
      m.reference.forEach((x) => console.log(line(x)))
      const min = Math.min(...m.group.map((x) => Math.min(x.ratio_opaque ?? 0, x.ratio_effective)))
      console.log('MODEL BREAKDOWN CELLS MEASURED: ' + m.group.length + ' of 10; minimum ratio (either ground) ' + min +
        '; cells at or above 4.5 on both grounds: ' +
        m.group.filter((x) => (x.ratio_opaque ?? 0) >= 4.5 && x.ratio_effective >= 4.5).length + ' of ' + m.group.length)
      await shot(s.page, 'b2_ac6_legibility.png')
      const ok = v.book.selected === 'Aggregate' && m.group.length === 10 && min >= 4.5
      console.log('VERDICT INPUTS MET: ' + ok)
      exit = ok ? 0 : 1
    } finally { await s.ctx.close() }
  } else if (viewerArg === 'opal-staff' && unavailable) {
    // ---- B2-AC7 ----
    const s = await openViewer(browser, 'opal-staff', fx.fixtures, null)
    try {
      const v = await settleLoad(s, 'opal-staff unavailable')
      const hasEntry = v.book.entries.some((e) => /aggregate|^agg$/i.test(e))
      console.log('SELECTOR ENTRIES: ' + JSON.stringify(v.book.entries) + '  Aggregate entry present: ' + hasEntry)
      console.log('SELECTED BOOK LABEL (the landing): ' + JSON.stringify(v.book.selected) + '  ordinary default model: ' + PREFERRED_DEFAULT_BOOK)
      console.log('REQUESTS TO opal_aggregate.json: ' + aggReqs(s) + ' (served the UNAVAILABLE payload ' + s.aggServed() + ')')
      console.log('MODEL BREAKDOWN GROUP IN THE DOM: ' + v.body_text_has_mb)
      console.log('BREAKDOWN: holding rows=' + v.breakdown.holding_rows + ' empty=' + JSON.stringify(v.breakdown.empty))
      console.log('PAGE ERRORS: ' + s.errors.length + (s.errors.length ? ' ' + JSON.stringify(s.errors) : ''))
      await shot(s.page, 'b2_ac7_opal_staff_unavailable.png')
      const ok = !hasEntry && v.book.selected === PREFERRED_DEFAULT_BOOK && !v.body_text_has_mb && s.errors.length === 0 && s.aggServed() >= 1
      console.log('VERDICT INPUTS MET: ' + ok)
      exit = ok ? 0 : 1
    } finally { await s.ctx.close() }
  } else {
    console.log('usage: see the header of this file')
    exit = 2
  }
} catch (e) {
  console.log(String(e && e.stack ? e.stack : e).slice(0, 2000))
  exit = 1
} finally {
  if (browser) await browser.close()
  await stopVite(server)
}
console.log('EXIT=' + exit)
process.exit(exit)
