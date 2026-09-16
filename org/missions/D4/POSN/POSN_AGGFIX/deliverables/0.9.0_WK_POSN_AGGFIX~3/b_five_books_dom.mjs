/**
 * POSN_AGGFIX.TO-B1-1 (slot ~3) -- <FIVE_BOOKS_DOM_B>: THE FIVE MODEL VIEWS, READ FROM THE RENDERED DOM.
 *
 * Mechanism copied from POSN_ASTTAX ~26's w3_dom_read.mjs (system Edge, the stubbed /auth/refresh SESSION, the
 * longest-substring fixture router), with three changes, each stated:
 *   1. THE SESSION VARIES PER VIEWER CLASS (VIEWERS below), built from the Claims shape in
 *      src/contexts/AuthContext.context.ts and parseClaims in AuthContext.tsx.
 *   2. THE SERVER IS STARTED HERE, from THIS worktree's portal (`node node_modules/vite/bin/vite.js`), on a port
 *      checked free first, and stopped at the end -- so the page under the read is the tree at the printed HEAD,
 *      never a server some other worktree left running.
 *   3. EVERY UNFIXTURED /api/, /v1/ OR /auth/ REQUEST, AND EVERY REMOTE REQUEST, IS ANSWERED 404 AND LISTED.
 *      A pass-through would let a live vendor or CDN answer change between the BEFORE and AFTER runs, and the
 *      comparison would then measure the network, not the page.
 *
 * Modes (run from the workspace root):
 *   node <this> --capture-before --out <B_DOM_BEFORE.json>   advisor + client x UST ST INT LT ULT at HEAD == edf85ce503
 *   node <this> --network-arms                               opal-staff, advisor, client x Models, ETFs: aggregate request counts
 *   node <this> --compare-before <B_DOM_BEFORE.json>         the same 10 captures at HEAD, compared; plus a mutated-weight control
 *   [--port <p>]  default 5241
 *
 * TO-B2-1 (the same slot) changes --network-arms in two places and nothing else: (a) its bar is the one B2-AC11 states,
 * Opal staff in Models EXACTLY 1 request (it was >= 1); (b) at any portal HEAD other than TO-B1-1's 63edeeeb51 the
 * request record is written to network_arms_requests_<HEAD10>.json, so TO-B1-1's committed record is never overwritten.
 *
 * TO-B3-1 (the same slot) ADDS ONE MODE and changes nothing above it:
 *   node <this> --prior-vs-new <dir>   B3-AC2  advisor + client x UST ST INT LT ULT rendered TWICE at the portal
 *                                      branch HEAD -- once on the PRIOR served shared file and once on the NEW one
 *                                      (the two VersionIds TO-A3-1 recorded, written to <dir> by <LIVE_FIXTURES_B3>)
 *                                      -- compared per book, plus a mutated-weight control on the NEW fixture.
 * The other two feeds are the SAME PINNED objects in both arms, so the shared file is the only thing that differs.
 * The PRIOR arm carries NO aggregate fixture: at that VersionId the Opal-only key did not exist (TO-A3-1's BEFORE
 * head read 404), and answering it 404 is what the world did, not a convenience.
 */
import { createRequire } from 'node:module'
import { spawn, spawnSync } from 'node:child_process'
import { writeFileSync, existsSync, readFileSync, mkdirSync } from 'node:fs'
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

const BASE = 'edf85ce503'
const args = process.argv.slice(2)
const flag = (f) => args.includes(f)
const opt = (f, d = null) => (args.includes(f) ? args[args.indexOf(f) + 1] : d)
const PORT = Number(opt('--port', '5241'))
const ORIGIN = `http://localhost:${PORT}`
const EDGE = 'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe'
const MODEL_BOOKS = ['UST', 'ST', 'INT', 'LT', 'ULT']
const sleep = (ms) => new Promise((r) => setTimeout(r, ms))
const md5 = (s) => createHash('md5').update(s).digest('hex')
const CORS = {
  'Access-Control-Allow-Origin': ORIGIN,
  'Access-Control-Allow-Credentials': 'true',
  'Access-Control-Allow-Headers': '*',
  'Access-Control-Allow-Methods': '*',
  'Content-Type': 'application/json',
}

// THE CLAIM SETS. Claims (AuthContext.context.ts :31-43) = firmId, userType, advisorId, firmRole, advisorRole;
// parseClaims (AuthContext.tsx :110-142) keeps userType only when it is exactly 'Dev', firmRole only 'admin'|'user',
// advisorRole only one of the four RCU roles.
//   opal-staff : firmId 'opal-capital', userType null -- Opal staff WITHOUT the Dev type, so the internal arm is
//                admitted by isInternal alone and not by isDev.
//   advisor    : the partner-advisor shape devBypass(advisorRole) mints (AuthContext.tsx :686-697): a partner
//                firmId, userType null, an advisorId, firmRole 'user', an advisorRole.
//   client     : AuthContext has NO client class. The nearest shape the Claims type can carry: a partner firmId
//                with every other claim at its parseClaims deny-floor (no advisor mapping, no firm role, no RCU role).
// '49financial' is chosen because its FIRM_ALLOWED_PATHS entry includes '/positioning' (firmAccess.ts :45-54),
// so ProtectedRoute renders the page rather than bouncing to /market -- and the LOC line proves it per run.
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
  const base = git(['rev-parse', BASE + '^{commit}'], PORTAL).stdout.trim()
  const dirty = git(['status', '--porcelain', '--', 'src'], PORTAL).stdout.trim()
  const branch = git(['rev-parse', '--abbrev-ref', 'HEAD'], PORTAL).stdout.trim()
  return { head, base, branch, head_equals_base: head === base, src_dirty: dirty }
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

async function openViewer(browser, viewer, fixtures, family) {
  const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 } })
  // The mode the page OPENS in: the persisted book-family toggle (usePersistentToggle, key
  // positioning:book-family, prefix opal:toggle:v1:), set before any page script runs.
  await ctx.addInitScript(([k, v]) => { try { window.sessionStorage.setItem(k, v) } catch { /* none */ } },
    ['opal:toggle:v1:positioning:book-family', family])
  const page = await ctx.newPage()
  const requests = []
  const unfixtured = []
  const errors = []
  page.on('request', (r) => requests.push(r.method() + ' ' + r.url()))
  page.on('pageerror', (e) => errors.push(String(e).slice(0, 300)))
  const session = { accessToken: 'b-harness-token', user: VIEWERS[viewer] }
  const keys = Object.keys(fixtures).sort((a, b) => b.length - a.length)
  await page.route('**/*', (r) => {
    const req = r.request()
    const url = req.url()
    if (req.method() === 'OPTIONS' && !url.startsWith(ORIGIN)) return r.fulfill({ status: 204, headers: CORS, body: '' })
    const k = keys.find((key) => url.includes(key))
    if (k) return r.fulfill({ status: 200, headers: CORS, body: JSON.stringify(fixtures[k]) })
    if (url.includes('/auth/refresh')) return r.fulfill({ status: 200, headers: CORS, body: JSON.stringify(session) })
    const u = new URL(url)
    const api = /^\/(api|v1|auth)\//.test(u.pathname)
    if (url.startsWith(ORIGIN) && !api) return r.continue()
    unfixtured.push(req.method() + ' ' + url)
    return r.fulfill({ status: 404, headers: CORS, body: '{"error":"b-harness: not fixtured"}' })
  })
  await page.goto(ORIGIN + '/positioning', { waitUntil: 'domcontentloaded', timeout: 120000 })
  return { ctx, page, requests, unfixtured, errors }
}

// ---- THE READ ------------------------------------------------------------------------------------------------
const readView = (page) => page.evaluate(() => {
  const norm = (s) => (s || '').replace(/\u00a0/g, ' ').replace(/[ \t]+/g, ' ').trim()
  // An SVG element (the treemap's foreignObject) has NO innerText -- reading it returned undefined and every read
  // threw. The rendered text of any node is taken from its first HTML descendant, else textContent.
  const textOf = (el) => {
    if (!el) return ''
    if (typeof el.innerText === 'string') return el.innerText
    const html = el.querySelector && Array.from(el.querySelectorAll('*')).find((x) => typeof x.innerText === 'string')
    return html ? html.innerText : (el.textContent || '')
  }
  const leafTitled = (t) => Array.from(document.querySelectorAll('h1,h2,h3,h4,span,div,p'))
    .find((e) => e.childElementCount === 0 && norm(e.textContent) === t)
  // Each Holdings panel is a direct child of the tab's `space-y-6` root (HoldingsTab.tsx :1101).
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
  const tiles = svg ? Array.from(svg.querySelectorAll('foreignObject')).map((f) => norm(textOf(f).replace(/\n+/g, ' / '))) : []
  const legend = comp ? Array.from(comp.querySelectorAll('div.justify-center span')).map((s) => norm(s.textContent)) : []
  const compEmpty = comp && !svg ? norm(textOf(comp)).slice(0, 200) : null
  const table = brk ? brk.querySelector('table') : null
  const head = table ? Array.from(table.querySelectorAll('thead > tr')).map((tr) =>
    Array.from(tr.children).map((c) => norm(textOf(c).replace(/\n+/g, ' '))).join(' | ')) : []
  const rows = table ? Array.from(table.querySelectorAll('tbody > tr')).map((tr) => ({
    holding: (tr.getAttribute('class') || '').includes('hover:bg-white/5'),
    text: Array.from(tr.children).map((c) => norm(textOf(c).replace(/\n+/g, ' '))).join(' | '),
  })) : []
  const brkEmpty = brk && !table ? norm(textOf(brk)).slice(0, 200) : null
  return {
    loc: location.pathname,
    family: pressed('Book family'),
    book: pressed('Book'),
    composition: { tile_count: tiles.length, tiles, legend, empty: compEmpty },
    breakdown: { header: head, row_count: rows.length, holding_row_count: rows.filter((r) => r.holding).length,
      rows: rows.map((r) => r.text), empty: brkEmpty },
  }
})

async function settle(page, ok, what, timeout = 180000) {
  const t0 = Date.now()
  let last = null
  let stable = 0
  while (Date.now() - t0 < timeout) {
    let v = null
    try { v = await readView(page) } catch { v = null }   // a vite dependency re-optimise reloads the page mid-read
    if (v && ok(v)) {
      const sig = JSON.stringify(v)
      stable = sig === last ? stable + 1 : 0
      last = sig
      if (stable >= 2) return v
    }
    await sleep(700)
  }
  throw new Error('TIMEOUT waiting for ' + what + ' -- last read: ' + (last || 'none').slice(0, 400))
}

async function captureViewer(browser, viewer, fixtures) {
  const s = await openViewer(browser, viewer, fixtures, 'models')
  const out = {}
  try {
    await settle(s.page, (v) => v.family.selected === 'Models' && v.book.entries.length > 0, viewer + ' page load')
    for (const code of MODEL_BOOKS) {
      await s.page.getByRole('group', { name: 'Book' }).getByRole('button', { name: code, exact: true }).click()
      const v = await settle(s.page, (x) => x.book.selected === code &&
        (x.breakdown.row_count > 0 || x.breakdown.empty !== null), viewer + ' / ' + code)
      out[viewer + '/' + code] = v
      console.log('  CAPTURE ' + (viewer + '/' + code).padEnd(12) + ' loc=' + v.loc + ' family=' + v.family.selected +
        ' selector=' + JSON.stringify(v.book.entries) + ' selected=' + v.book.selected +
        ' composition tiles=' + v.composition.tile_count + ' legend=' + JSON.stringify(v.composition.legend) +
        ' breakdown rows=' + v.breakdown.row_count + ' (holding rows ' + v.breakdown.holding_row_count + ')')
    }
  } finally {
    console.log('  ' + viewer + ': requests=' + s.requests.length + ' unfixtured(404)=' + s.unfixtured.length +
      ' page errors=' + s.errors.length + (s.errors.length ? ' ' + JSON.stringify(s.errors) : ''))
    await s.ctx.close()
  }
  return { captures: out, unfixtured: [...new Set(s.unfixtured)], errors: s.errors }
}

const compared = (v) => ({ composition: v.composition, breakdown: v.breakdown })

function firstDiff(a, b, p = '') {
  if (JSON.stringify(a) === JSON.stringify(b)) return null
  if (a && b && typeof a === 'object' && typeof b === 'object') {
    for (const k of new Set([...Object.keys(a), ...Object.keys(b)])) {
      const d = firstDiff(a[k], b[k], p + '.' + k)
      if (d) return d
    }
  }
  return p + ': BEFORE=' + JSON.stringify(a)?.slice(0, 160) + '  NOW=' + JSON.stringify(b)?.slice(0, 160)
}

// ---- MAIN ----------------------------------------------------------------------------------------------------
const st = portalState()
console.log('PORTAL: ' + PORTAL + '  branch ' + st.branch + '  HEAD ' + st.head)
console.log('BASE  : ' + BASE + ' = ' + st.base + '  HEAD == BASE: ' + st.head_equals_base +
  '  src working-tree changes: ' + (st.src_dirty ? JSON.stringify(st.src_dirty) : 'NONE'))
for (const [k, v] of Object.entries(VIEWERS)) {
  console.log('CLAIMS ' + k.padEnd(10) + ': firmId=' + JSON.stringify(v.firmId) + ' userType=' + JSON.stringify(v.userType) +
    ' advisorId=' + JSON.stringify(v.advisorId) + ' firmRole=' + JSON.stringify(v.firmRole) +
    ' advisorRole=' + JSON.stringify(v.advisorRole) + ' role=' + v.role)
}

let exit = 1
let server = null
let browser = null
try {
  if (flag('--capture-before')) {
    const out = opt('--out')
    if (!out) throw new Error('usage: --capture-before --out <file>')
    if (existsSync(path.resolve(out))) throw new Error('BLOCKED: ' + out + ' exists -- B_DOM_BEFORE is captured ONCE and never re-captured')
    if (!st.head_equals_base || st.src_dirty) throw new Error('BLOCKED: the BEFORE capture runs only at HEAD == ' + BASE + ' with no src edits')
    const fx = buildFixtures(ROOT)
    fx.lines.forEach((l) => console.log(l))
    server = await startVite()
    browser = await chromium.launch({ executablePath: EDGE, headless: true })
    const all = {}
    const meta = { captured_at: new Date().toISOString(), portal: st, viewport: '1440x900', port: PORT,
      fixtures: fx.lines, viewers: { advisor: VIEWERS.advisor, client: VIEWERS.client }, unfixtured: {}, page_errors: {} }
    for (const viewer of ['advisor', 'client']) {
      const r = await captureViewer(browser, viewer, fx.fixtures)
      Object.assign(all, r.captures)
      meta.unfixtured[viewer] = r.unfixtured
      meta.page_errors[viewer] = r.errors
    }
    const good = Object.entries(all).filter(([k, v]) => v.book.selected === k.split('/')[1] &&
      v.breakdown.holding_row_count > 0 && v.composition.tile_count > 0 && v.loc === '/positioning')
    console.log('UNFIXTURED (answered 404, identical in every run): ' + JSON.stringify(meta.unfixtured))
    // WRITTEN ONLY ON 10 OF 10: the file is captured once and never again, so a short capture goes to scratch
    // with a non-zero exit rather than becoming the permanent baseline.
    const complete = good.length === 10 && Object.keys(all).length === 10
    const dest = complete ? path.resolve(out) : path.join(ROOT, '.scratch', 'B_DOM_BEFORE.REJECTED.json')
    mkdirSync(path.dirname(dest), { recursive: true })
    writeFileSync(dest, JSON.stringify({ meta, captures: all }, null, 1) + '\n')
    console.log((complete ? 'WROTE ' : 'NOT WRITTEN TO ' + out + ' -- short capture kept at ') + path.relative(ROOT, dest) +
      ' md5=' + md5(readFileSync(dest)))
    console.log('CAPTURED ' + good.length + ' of ' + Object.keys(all).length + ' (10 expected: advisor and client x ' +
      MODEL_BOOKS.join(' ') + '; each with its book selected, >0 composition tiles, >0 breakdown holding rows, on /positioning)')
    exit = good.length === 10 && Object.keys(all).length === 10 ? 0 : 1
  } else if (flag('--compare-before')) {
    const beforePath = opt('--compare-before')
    const before = JSON.parse(readFileSync(path.resolve(beforePath), 'utf8'))
    console.log('BEFORE: ' + beforePath + ' captured at portal ' + before.meta.portal.head + ' on ' + before.meta.captured_at)
    const fx = buildFixtures(ROOT)
    fx.lines.forEach((l) => console.log(l))
    const beforeFx = JSON.stringify(before.meta.fixtures.filter((l) => !l.startsWith('FETCHED')))
    const nowFx = JSON.stringify(fx.lines.filter((l) => !l.startsWith('FETCHED')))
    console.log('SAME FIXTURES AS THE BEFORE RUN: ' + (beforeFx === nowFx))
    server = await startVite()
    browser = await chromium.launch({ executablePath: EDGE, headless: true })
    const now = {}
    for (const viewer of ['advisor', 'client']) Object.assign(now, (await captureViewer(browser, viewer, fx.fixtures)).captures)
    let same = 0
    const keys = Object.keys(before.captures)
    for (const k of keys) {
      const d = now[k] ? firstDiff(compared(before.captures[k]), compared(now[k])) : 'MISSING NOW'
      if (!d) same += 1
      console.log('  ' + k.padEnd(12) + ' ' + (d ? 'DIFFERENT -- ' + d : 'IDENTICAL'))
    }
    console.log('IDENTICAL ' + same + ' of ' + keys.length)
    // THE CONTROL: one fixture weight mutated, one advisor capture on that book, compared the same way.
    const ctl = buildFixtures(ROOT, { mutate: (f) => {
      const h = f['/api/general/positioning/positioning_data.json'].current_holdings.UST.holdings[0]
      const was = h.weight
      h.weight = Math.round((h.weight + 0.05) * 10000) / 10000
      return 'shared-file current_holdings.UST.holdings[0] ' + h.ticker + ' weight ' + was + ' -> ' + h.weight
    } })
    ctl.lines.filter((l) => l.startsWith('MUTATED')).forEach((l) => console.log(l))
    const s = await openViewer(browser, 'advisor', ctl.fixtures, 'models')
    let ctlVerdict = 'NOT RUN'
    try {
      await settle(s.page, (v) => v.family.selected === 'Models' && v.book.entries.length > 0, 'control load')
      await s.page.getByRole('group', { name: 'Book' }).getByRole('button', { name: 'UST', exact: true }).click()
      const v = await settle(s.page, (x) => x.book.selected === 'UST' && x.breakdown.row_count > 0, 'control UST')
      const d = firstDiff(compared(before.captures['advisor/UST']), compared(v))
      ctlVerdict = d ? 'DIFFERENT -- ' + d : 'IDENTICAL'
    } finally { await s.ctx.close() }
    console.log('CONTROL advisor/UST with the mutated weight: ' + ctlVerdict)
    const rec = path.join(path.dirname(path.resolve(beforePath)), 'B_DOM_COMPARE_' + st.head.slice(0, 10) + '.json')
    writeFileSync(rec, JSON.stringify({ portal: st, identical: same, of: keys.length, control: ctlVerdict, captures: now }, null, 1) + '\n')
    console.log('WROTE ' + path.relative(ROOT, rec))
    exit = same === keys.length && keys.length === 10 && ctlVerdict.startsWith('DIFFERENT') ? 0 : 1
  } else if (flag('--network-arms')) {
    const fx = buildFixtures(ROOT)
    fx.lines.forEach((l) => console.log(l))
    server = await startVite()
    browser = await chromium.launch({ executablePath: EDGE, headless: true })
    const table = []
    const record = { portal: st, arms: {} }
    for (const family of ['models', 'etfs']) {
      for (const viewer of ['opal-staff', 'advisor', 'client']) {
        const s = await openViewer(browser, viewer, fx.fixtures, family)
        const label = family === 'models' ? 'Models' : 'ETFs'
        try {
          const v = await settle(s.page, (x) => x.family.selected === label && x.book.entries.length > 0 &&
            (x.breakdown.row_count > 0 || x.breakdown.empty !== null), viewer + ' ' + label)
          await sleep(4000)   // every query the mount enables has fired by now; count after the settle, not at it
          const agg = s.requests.filter((u) => u.includes('opal_aggregate.json'))
          table.push({ family: label, viewer, aggregate_requests: agg.length, total_requests: s.requests.length,
            loc: v.loc, family_selected: v.family.selected, selector: v.book.entries })
          record.arms[label + '/' + viewer] = { requests: s.requests, unfixtured: [...new Set(s.unfixtured)], errors: s.errors }
        } finally { await s.ctx.close() }
      }
    }
    console.log('\nREQUESTS TO ' + AGG_URLKEY)
    console.log('  mode    viewer      count   (total requests, loc, family pressed, selector)')
    for (const t of table) {
      console.log('  ' + t.family.padEnd(7) + ' ' + t.viewer.padEnd(11) + ' ' + String(t.aggregate_requests).padEnd(7) +
        ' (' + t.total_requests + ', ' + t.loc + ', ' + t.family_selected + ', ' + JSON.stringify(t.selector) + ')')
    }
    const rec = path.join(HERE, st.head.startsWith('63edeeeb51') ? 'b1_ac5_network_arms_requests.json'
      : 'network_arms_requests_' + st.head.slice(0, 10) + '.json')
    writeFileSync(rec, JSON.stringify(record, null, 1) + '\n')
    console.log('EVERY REQUEST URL RECORDED: ' + path.relative(ROOT, rec))
    const get = (f, v) => table.find((t) => t.family === f && t.viewer === v)?.aggregate_requests
    const want = get('Models', 'opal-staff') === 1 && get('Models', 'advisor') === 0 && get('Models', 'client') === 0 &&
      get('ETFs', 'opal-staff') === 0 && get('ETFs', 'advisor') === 0 && get('ETFs', 'client') === 0
    console.log('EXPECTATION (Models: staff exactly 1, advisor 0, client 0; ETFs: 0, 0, 0): ' + (want ? 'MET' : 'NOT MET'))
    exit = want ? 0 : 1
  } else if (flag('--prior-vs-new')) {
    // ---- B3-AC2: the five model views on the PRIOR and on the NEW shared file, at the portal branch HEAD ----
    const dirArg = opt('--prior-vs-new')
    if (!dirArg) throw new Error('usage: --prior-vs-new <fixture dir>')
    const dir = path.resolve(dirArg)
    const rd = (n) => {
      const p = path.join(dir, n)
      const b = readFileSync(p)
      console.log('FIXTURE FILE ' + path.relative(ROOT, p) + ' bytes=' + b.length + ' md5=' + md5(b))
      return JSON.parse(b.toString('utf8'))
    }
    const priorShared = rd('prior_shared.json')
    const newShared = rd('new_shared.json')
    const aggregate = rd('aggregate.json')
    console.log('PRIOR shared file: current_holdings ' + JSON.stringify(Object.keys(priorShared.current_holdings)) +
      '  generated_at ' + priorShared.generated_at)
    console.log('NEW   shared file: current_holdings ' + JSON.stringify(Object.keys(newShared.current_holdings)) +
      '  generated_at ' + newShared.generated_at)
    console.log('AGGREGATE (NEW arm only): status=' + aggregate.status + ' AGG holdings=' +
      aggregate.current_holdings.AGG.holdings.length)
    const posnKey = '/api/general/positioning/positioning_data.json'
    const attrKey = '/api/general/positioning/holdings_attribution_data.json'
    const etfKey = '/api/general/etfs/positioning_data.json'
    // The attribution and ETF feeds are the PINNED objects, identical in both arms, so they cannot be the source
    // of a difference; only the shared file changes between the arms.
    const base = buildFixtures(ROOT)
    base.lines.filter((l) => l.includes(attrKey) || l.includes(etfKey)).forEach((l) => console.log('PINNED ' + l))
    const priorFx = { [posnKey]: priorShared, [attrKey]: base.fixtures[attrKey], [etfKey]: base.fixtures[etfKey] }
    const newFx = { [posnKey]: newShared, [attrKey]: base.fixtures[attrKey], [etfKey]: base.fixtures[etfKey],
      [AGG_URLKEY]: aggregate }
    console.log('PRIOR arm fixture keys: ' + JSON.stringify(Object.keys(priorFx)) + ' (no ' + AGG_URLKEY +
      ' -- absent at that VersionId, so it is answered 404 and listed)')
    console.log('NEW   arm fixture keys: ' + JSON.stringify(Object.keys(newFx)))
    server = await startVite()
    browser = await chromium.launch({ executablePath: EDGE, headless: true })
    const arms = {}
    for (const [arm, fixtures] of [['PRIOR', priorFx], ['NEW', newFx]]) {
      console.log('== ARM ' + arm + ' ==')
      const caps = {}
      for (const viewer of ['advisor', 'client']) {
        const r = await captureViewer(browser, viewer, fixtures)
        Object.assign(caps, r.captures)
        console.log('  ' + arm + '/' + viewer + ' unfixtured(404): ' + JSON.stringify(r.unfixtured) +
          ' page errors: ' + r.errors.length)
      }
      arms[arm] = caps
    }
    let same = 0
    const keys = Object.keys(arms.PRIOR)
    console.log('COMPARED PER BOOK (composition labels and breakdown rows; PRIOR is BEFORE, NEW is NOW):')
    for (const k of keys) {
      const d = arms.NEW[k] ? firstDiff(compared(arms.PRIOR[k]), compared(arms.NEW[k])) : 'MISSING IN THE NEW ARM'
      if (!d) same += 1
      console.log('  ' + k.padEnd(12) + ' ' + (d ? 'DIFFERENT -- ' + d : 'IDENTICAL'))
    }
    console.log('IDENTICAL ' + same + ' of ' + keys.length)
    // THE CONTROL: the NEW fixture with ONE holding weight mutated, rendered and compared the same way.
    const ctlShared = JSON.parse(JSON.stringify(newShared))
    const ch = ctlShared.current_holdings.UST.holdings[0]
    const was = ch.weight
    ch.weight = Math.round((ch.weight + 0.05) * 10000) / 10000
    console.log('CONTROL (NEW fixture, one weight mutated): current_holdings.UST.holdings[0] ' + ch.ticker +
      ' weight ' + was + ' -> ' + ch.weight)
    const ctlFx = { ...newFx, [posnKey]: ctlShared }
    const cs = await openViewer(browser, 'advisor', ctlFx, 'models')
    let ctlVerdict = 'NOT RUN'
    try {
      await settle(cs.page, (v) => v.family.selected === 'Models' && v.book.entries.length > 0, 'control load')
      await cs.page.getByRole('group', { name: 'Book' }).getByRole('button', { name: 'UST', exact: true }).click()
      const v = await settle(cs.page, (x) => x.book.selected === 'UST' && x.breakdown.row_count > 0, 'control UST')
      const d = firstDiff(compared(arms.NEW['advisor/UST']), compared(v))
      ctlVerdict = d ? 'DIFFERENT -- ' + d : 'IDENTICAL'
    } finally { await cs.ctx.close() }
    console.log('CONTROL advisor/UST, the NEW arm vs the mutated NEW fixture: ' + ctlVerdict)
    const rec = path.join(HERE, 'b3_ac2_prior_vs_new_' + st.head.slice(0, 10) + '.json')
    writeFileSync(rec, JSON.stringify({ portal: st, fixture_dir: path.relative(ROOT, dir), identical: same,
      of: keys.length, control: ctlVerdict, arms }, null, 1) + '\n')
    console.log('WROTE ' + path.relative(ROOT, rec))
    exit = same === keys.length && keys.length === 10 && ctlVerdict.startsWith('DIFFERENT') ? 0 : 1
  } else if (flag('--probe')) {
    // DIAGNOSTIC ONLY (not a criterion invocation): open one viewer, wait, print what the read returns or throws.
    const viewer = opt('--probe', 'advisor')
    const fx = buildFixtures(ROOT)
    server = await startVite()
    browser = await chromium.launch({ executablePath: EDGE, headless: true })
    const s = await openViewer(browser, viewer, fx.fixtures, opt('--family', 'models'))
    for (let i = 0; i < 6; i++) {
      await sleep(10000)
      let r
      try { r = JSON.stringify(await readView(s.page)).slice(0, 1500) } catch (e) { r = 'READ THREW: ' + String(e).slice(0, 600) }
      const body = await s.page.evaluate(() => document.body.innerText.replace(/\s+/g, ' ').slice(0, 400)).catch((e) => 'BODY THREW ' + e)
      console.log('t+' + (i + 1) * 10 + 's url=' + s.page.url() + '\n  READ ' + r + '\n  BODY ' + body)
    }
    await s.page.screenshot({ path: path.join(ROOT, '.scratch', 'probe_' + viewer + '.png'), fullPage: true })
    console.log('requests=' + s.requests.length + ' unfixtured=' + JSON.stringify([...new Set(s.unfixtured)]).slice(0, 1500) + ' errors=' + JSON.stringify(s.errors))
    await s.ctx.close()
    exit = 0
  } else {
    console.log('usage: --capture-before --out <f> | --network-arms | --compare-before <f> | --prior-vs-new <dir>')
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
