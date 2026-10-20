// run7_browser_leg.mjs -- the browser leg of run 7 (ADDENDUM 9 section 2, rows B1, B2, B3), proved offline.
//
// B1 reads the New Analysis Request form of the Ticket Center, B2 fills it, attaches the holdings file and presses
// File Analysis Request ONCE, B3 presses Open report on the ticket. The page's own controls are found by their
// accessible names (read from portal/src/pages/TicketCenter at the PROD tip, see PAGE_NOTES.md). Nothing is printed
// but closed lines: no URL, no token, no header, no file content. Keep is never pressed.
//
// Usage:
//   node run7_browser_leg.mjs --portal <portal worktree> (--origin <url> | --dist <build dir>)
//       [--fixtures <json>] [--token-file <path>] [--holdings <csv>] [--firm 49financial]
//       [--household "E2E7 SYNTHETIC"] [--title <text>] [--out <dir>] [--phase b1|b2|b3|all] [--ticket <id>]
//   node run7_browser_leg.mjs --offline --portal <dir> --dist <dir> --fixtures <json> --holdings <csv> --out <dir>
//
// Imports: playwright-core (resolved from --portal, which holds node_modules) and node: built-ins only.
// The --dist routing is a copy of portal/scripts/ui-dist.mjs (serveFromDist), not an import of it.

import { createRequire } from 'node:module'
import { existsSync, mkdirSync, readFileSync, statSync } from 'node:fs'
import { basename, extname, join, resolve, sep } from 'node:path'

const args = process.argv.slice(2)
const flag = name => {
  const i = args.indexOf(name)
  return i === -1 ? null : (args[i + 1] ?? null)
}
const has = name => args.includes(name)

const EDGE = 'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe'
const DIST_ORIGIN = 'http://localhost:5199'
const FIRM_CHOICE = 'Choose the firm this request is filed under'
const TITLE_PLACEHOLDER = 'Title (what is being requested?)'
const SUBMIT_NAME = 'File Analysis Request'
const TYPE_VALUE = 'analysis_request'
const VALUE_MARK = '12.5'

const OFFLINE = has('--offline')
const PORTAL = flag('--portal')
const DIST = flag('--dist') ? resolve(flag('--dist')) : null
const ORIGIN_ARG = flag('--origin')
const FIXTURES_PATH = flag('--fixtures')
const TOKEN_FILE = flag('--token-file')
const HOLDINGS = flag('--holdings')
const FIRM = flag('--firm') ?? '49financial'
const HOUSEHOLD = flag('--household') ?? 'E2E7 SYNTHETIC'
const TITLE = flag('--title') ?? 'E2E7 SYNTHETIC analysis request'
const OUT = resolve(flag('--out') ?? join(process.cwd(), '.scratch', 'run7_shots'))
const TICKET_ARG = flag('--ticket')
const PHASE_ARG = flag('--phase') ?? 'all'
const BAD_PREFIX = OFFLINE ? 'B-LEG-OFFLINE-BAD' : 'B-LEG-BAD'

// The API calls the filing makes, by name (method, exact pathname). ticket-report is the fourth step of I1.
const CALL_NAMES = [
  ['POST', /\/investor-reporting\/analysis\/inputs$/, 'analysis-input-upload'],
  ['POST', /^\/api\/scoped\/tickets$/, 'ticket-create'],
  ['POST', /\/investor-reporting\/analysis$/, 'analysis-request'],
  ['POST', /^\/api\/scoped\/tickets\/[^/]+\/report$/, 'ticket-report'],
]

class Bad extends Error {
  constructor(phase, why) {
    super(why)
    this.phase = phase
  }
}

const say = line => console.log(line)
// Words a line may carry: letters, digits and a few marks. No colon and no slash, so no URL can be built from them.
const clean = s => String(s ?? '').replace(/[^A-Za-z0-9 .,'()=\-]/g, '').replace(/\s+/g, ' ').trim().slice(0, 160)
const nowZ = () => new Date().toISOString().slice(11, 19) + 'Z'

const MIME = {
  '.html': 'text/html; charset=utf-8', '.js': 'text/javascript; charset=utf-8', '.mjs': 'text/javascript; charset=utf-8',
  '.css': 'text/css; charset=utf-8', '.json': 'application/json', '.svg': 'image/svg+xml', '.png': 'image/png',
  '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.gif': 'image/gif', '.webp': 'image/webp', '.ico': 'image/x-icon',
  '.ttf': 'font/ttf', '.otf': 'font/otf', '.woff': 'font/woff', '.woff2': 'font/woff2', '.map': 'application/json',
  '.txt': 'text/plain; charset=utf-8', '.webmanifest': 'application/manifest+json',
}
const ASSET_EXT = new Set(Object.keys(MIME).filter(e => e !== '.html'))

// Copy of portal/scripts/ui-dist.mjs serveFromDist: a build file, else index.html; /api and /auth answer 404; other origins abort.
async function serveFromDist(route, dist, origin) {
  const url = route.request().url()
  if (!url.startsWith(origin)) {
    await route.abort('blockedbyclient')
    return true
  }
  let pathname
  try {
    pathname = decodeURIComponent(new URL(url).pathname)
  } catch {
    pathname = new URL(url).pathname
  }
  if (/^\/(api|auth)\//.test(pathname)) {
    await route.fulfill({ status: 404, headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ error: 'run7: no fixture for this API read' }) })
    return true
  }
  const root = resolve(dist)
  const file = resolve(join(root, pathname))
  let target = null
  if ((file === root || file.startsWith(root + sep)) && existsSync(file) && statSync(file).isFile()) target = file
  if (!target) {
    if (ASSET_EXT.has(extname(pathname).toLowerCase())) {
      await route.fulfill({ status: 404, headers: { 'Content-Type': 'text/plain' }, body: 'run7: no such file in the build' })
      return true
    }
    target = join(root, 'index.html')
  }
  await route.fulfill({
    status: 200,
    headers: { 'Content-Type': MIME[extname(target).toLowerCase()] || 'application/octet-stream', 'Cache-Control': 'no-store' },
    body: readFileSync(target),
  })
  return true
}

function buildSession() {
  const session = {
    accessToken: 'run7-inert-stub',
    user: {
      email: 'dev@opalcapital.com', name: 'Dev User', role: 'admin', userType: 'Dev', firmId: 'opal-capital',
      firmRole: null, advisorId: null, advisorRole: null, mustChangePassword: false,
    },
  }
  if (TOKEN_FILE) {
    // The real bearer goes to the page as the session's accessToken (the way ui-smoke --token sends it); its claims are the payload's.
    const jwt = readFileSync(TOKEN_FILE, 'utf8').trim()
    const payload = JSON.parse(Buffer.from(jwt.split('.')[1], 'base64url').toString('utf8'))
    session.accessToken = jwt
    if (payload.sub) session.user.email = payload.sub
    for (const k of ['name', 'role', 'userType', 'firmId', 'firmRole', 'advisorId', 'advisorRole']) {
      if (payload[k] !== undefined) session.user[k] = payload[k]
    }
  }
  return session
}

function loadFixtures() {
  if (!FIXTURES_PATH) return {}
  return JSON.parse(readFileSync(FIXTURES_PATH, 'utf8'))
}

// One context per phase: a fresh page, the same router, a record of the /api calls the page makes, and the ids the answers carry.
async function openPage(browser, st) {
  const context = await browser.newContext({ viewport: { width: 1440, height: 900 } })
  const page = await context.newPage()
  const calls = []
  const answers = {}
  let pageErrors = 0
  page.on('pageerror', e => {
    pageErrors++
    if (process.env.RUN7_DEBUG) say(`DEBUG pageerror ${clean(e.message)}`)
  })
  if (process.env.RUN7_DEBUG) page.on('console', m => say(`DEBUG console ${clean(m.text())}`))
  page.on('request', q => {
    const u = new URL(q.url())
    if (u.origin === st.origin && u.pathname.startsWith('/api/')) calls.push({ method: q.method(), path: u.pathname })
  })
  page.on('response', async s => {
    const q = s.request()
    if (q.method() !== 'POST' || s.status() >= 300) return
    const p = new URL(q.url()).pathname
    if (p === '/api/scoped/tickets') {
      const j = await s.json().catch(() => null)
      answers.ticket = j?.ticket?.ticket_id ?? answers.ticket
    }
    if (p.endsWith('/investor-reporting/analysis')) {
      const j = await s.json().catch(() => null)
      answers.req = j?.data?.identity?.request_id ?? answers.req
    }
  })
  await page.route('**/*', async r => {
    const req = r.request()
    const url = req.url()
    if (req.method() === 'OPTIONS' && !url.startsWith(st.origin)) return r.fulfill({ status: 204, headers: st.cors, body: '' })
    const key = st.keys.find(k => url.includes(k))
    if (key !== undefined) return r.fulfill({ status: 200, headers: st.cors, body: JSON.stringify(st.fixtures[key]) })
    if (url.includes('/auth/refresh')) return r.fulfill({ status: 200, headers: st.cors, body: JSON.stringify(st.session) })
    if (st.dist && (await serveFromDist(r, st.dist, st.origin))) return
    return r.continue()
  })
  return { context, page, calls, answers, pageErrors: () => pageErrors }
}

function printCalls(ctx) {
  for (const c of ctx.calls) say(`CALLS ${c.method} ${c.path}`)
}

async function openBoard(ctx, phase) {
  await ctx.page.goto(ctx.origin + '/ticket-center', { waitUntil: 'load', timeout: 60000 }).catch(() => {})
  const newTicket = ctx.page.getByRole('button', { name: 'New Ticket', exact: true })
  try {
    await newTicket.waitFor({ state: 'visible', timeout: 60000 })
  } catch {
    throw new Bad(phase, 'control "New Ticket" not found on the Ticket Center board')
  }
}

// Opens the New Ticket panel, chooses the Analysis Request type and waits for the Firm chooser the staff form shows.
async function openAnalysisForm(ctx, phase) {
  await openBoard(ctx, phase)
  await ctx.page.getByRole('button', { name: 'New Ticket', exact: true }).click()
  const typeSelect = ctx.page.locator(`select:has(option[value="${TYPE_VALUE}"])`)
  try {
    await typeSelect.first().waitFor({ state: 'visible', timeout: 15000 })
  } catch {
    throw new Bad(phase, 'control ticket type chooser (option "Analysis Request") not found')
  }
  await typeSelect.first().selectOption(TYPE_VALUE)
  const firm = ctx.page.getByLabel(FIRM_CHOICE, { exact: true })
  try {
    await firm.waitFor({ state: 'visible', timeout: 30000 })
  } catch {
    const words = await ctx.page.locator('[data-slot="firm-read-only"]').first().innerText().catch(() => '')
    throw new Bad(phase, `control "${FIRM_CHOICE}" not found; the firm line reads: ${clean(words) || 'nothing'}`)
  }
  return firm
}

async function phaseB1(ctx) {
  const phase = 'b1'
  const firm = await openAnalysisForm(ctx, phase)
  const firms = await firm.locator('option:not([value=""])').allTextContents()
  const root = ctx.page.locator('[data-slot="analysis-request-fields"]')
  const labels = (await root.locator('input, select, textarea').count()) +
    (await ctx.page.getByPlaceholder(TITLE_PLACEHOLDER).count())
  const advisorBox = ctx.page.getByLabel('Advisor', { exact: true })
  let advisor = 'absent'
  if ((await advisorBox.count()) > 0) {
    const ph = (await advisorBox.first().getAttribute('placeholder')) ?? ''
    advisor = /\(optional\)/i.test(ph) ? 'optional' : /\(required\)/i.test(ph) ? 'required' : 'unrecognised'
  }
  const reportTypeN = (await ctx.page.getByLabel(/report type/i).count()) +
    (await ctx.page.getByRole('combobox', { name: /report type/i }).count())
  const commentaryN = (await root.getByLabel(/commentary/i).count()) + (await root.getByText(/commentary/i).count())
  const models = await root.locator('[data-slot="comparables"] input[type="checkbox"]').count()
  const result = {
    labels, advisor, reportType: reportTypeN > 0 ? 'present' : 'absent', commentary: commentaryN > 0 ? 'present' : 'absent',
    firms: firms.map(clean), models,
  }
  say(`B1 form labels=${labels} advisor=${advisor} report_type=${result.reportType} commentary=${result.commentary} firms=${result.firms.join(',')} models=${models}`)
  await ctx.page.screenshot({ path: join(OUT, 'b1.png'), fullPage: true })
  printCalls(ctx)
  return result
}

// The words the form holds the submit with, read from the form's own text (never a URL, never a token).
async function heldWords(page) {
  const text = await page.evaluate(() => document.body.innerText)
  const line = text.split('\n').map(s => s.trim()).find(s => /required|Choose|Add a title|Loading|Wait for|cannot be filed|could not be loaded|Choose the holdings/i.test(s))
  return clean(line) || 'no words shown'
}

async function phaseB2(ctx) {
  const phase = 'b2'
  const { page } = ctx
  const firm = await openAnalysisForm(ctx, phase)
  const ids = await firm.locator('option:not([value=""])').evaluateAll(os => os.map(o => o.value))
  if (!ids.includes(FIRM)) throw new Bad(phase, `the firm given by --firm is not in the chooser (${ids.length} firms listed)`)
  await firm.selectOption(FIRM)
  await page.getByLabel('Household', { exact: true }).fill(HOUSEHOLD)
  await page.getByPlaceholder(TITLE_PLACEHOLDER).fill(TITLE)
  if (!HOLDINGS || !existsSync(HOLDINGS)) throw new Bad(phase, '--holdings file not found')
  const holdingsBox = page.locator('input[aria-label="Holdings file"]')
  if ((await holdingsBox.count()) === 0) throw new Bad(phase, 'control "Holdings file" (file input) not found')
  await holdingsBox.setInputFiles({ name: basename(HOLDINGS), mimeType: 'text/csv', buffer: readFileSync(HOLDINGS) })
  const submit = page.getByRole('button', { name: SUBMIT_NAME, exact: true })
  try {
    await submit.waitFor({ state: 'visible', timeout: 15000 })
  } catch {
    throw new Bad(phase, `control "${SUBMIT_NAME}" not found`)
  }
  try {
    await page.waitForFunction(name => {
      const b = [...document.querySelectorAll('button')].find(x => x.textContent.trim() === name)
      return !!b && !b.disabled
    }, SUBMIT_NAME, { timeout: 15000 })
  } catch {
    throw new Bad(phase, `submit held: ${await heldWords(page)}`)
  }
  // ONE press. Keep is never pressed; a second File press is never made.
  await submit.click()
  let outcome
  try {
    await page.waitForFunction(() => {
      const t = document.body.innerText
      return /Analysis request TCK-[0-9A-Za-z-]+ filed/.test(t) || /Nothing (was|is known to be) filed|Review required:/.test(t)
    }, null, { timeout: 120000 })
    outcome = 'settled'
  } catch {
    outcome = 'timeout'
  }
  const at = nowZ()
  await page.waitForTimeout(1500)
  const text = await page.evaluate(() => document.body.innerText)
  const filed = /Analysis request (TCK-[0-9A-Za-z-]+) filed/.exec(text)
  await page.screenshot({ path: join(OUT, 'b2.png'), fullPage: true })
  const names = ctx.calls.map(c => CALL_NAMES.find(([m, re]) => m === c.method && re.test(c.path))?.[2]).filter(Boolean)
  printCalls(ctx)
  if (!filed) {
    const words = /(Nothing (was|is known to be) filed[^.]*\.|Review required:[^.]*\.)/.exec(text)?.[1] ?? (outcome === 'timeout' ? 'no answer from the page within the wait' : 'the page showed no filing')
    say(`B2 filed REFUSED ${clean(words)}`)
    throw new Bad(phase, 'filing refused; nothing confirmed as filed')
  }
  const ticket = filed[1]
  const creates = names.filter(n => n === 'ticket-create').length
  const submits = names.filter(n => n === 'analysis-request').length
  const analysisSent = submits === 1
  const req = analysisSent ? (/(REQ-[0-9a-f]{24})/.exec(text)?.[1] ?? ctx.answers.req ?? 'none') : 'none'
  say(`B2 filed ok ticket=${ticket} req=${req} at=${at}`)
  if (creates !== 1) throw new Bad(phase, `expected one ticket create, saw ${creates}`)
  if (submits > 1) throw new Bad(phase, `a second analysis submit was sent (${submits})`)
  if (!analysisSent) {
    // The ticket is filed but the page never sent the analysis POST: the page's own words say so.
    const said = /(the analysis did not start|Analysis: FAILED[^.]*)/.exec(text)?.[1] ?? 'no words shown'
    throw new Bad(phase, `the ticket is filed but the analysis request was not sent; the page showed: ${clean(said)}`)
  }
  return { ticket, req, calls: names.join(',') }
}

async function phaseB3(ctx, ticket) {
  const phase = 'b3'
  const { page } = ctx
  await openBoard(ctx, phase)
  const rows = ticket
    ? page.locator('tr', { hasText: ticket })
    : page.locator('tr').filter({ has: page.locator('button[data-slot="open-report"]') })
  try {
    await rows.first().waitFor({ state: 'visible', timeout: 30000 })
  } catch {
    throw new Bad(phase, `ticket row ${ticket ?? '(first with a report)'} not found on the board`)
  }
  const openBtn = rows.first().locator('button[data-slot="open-report"]')
  if ((await openBtn.count()) === 0) throw new Bad(phase, 'control "Open report" not found on the ticket row')
  await openBtn.first().click()
  const panel = page.locator('[data-slot="opened-report"]').first()
  await panel.waitFor({ state: 'attached', timeout: 30000 }).catch(() => {})
  let face = 'no'
  let headings = 0
  let value = 'no'
  if ((await page.locator('[data-slot="opened-report"]').count()) > 0) {
    const state = await panel.getAttribute('data-state')
    face = state === 'ready' ? 'yes' : 'no'
    headings = await panel.locator('h1, h2, h3, h4, h5, h6, [role="heading"]').count()
    value = (await panel.innerText()).includes(VALUE_MARK) ? 'yes' : 'no'
  }
  if (process.env.RUN7_DEBUG) {
    const dbgText = await page.evaluate(() => document.body.innerText)
    say(`DEBUG b3 panels=${await page.locator('[data-slot="opened-report"]').count()} words=${clean(dbgText.slice(-700))}`)
  }
  say(`B3 report face=${face} headings=${headings} value=${value}`)
  await page.screenshot({ path: join(OUT, 'b3.png'), fullPage: true })
  printCalls(ctx)
  return { face, headings, value }
}

async function main() {
  if (!PORTAL) throw new Bad('setup', '--portal <dir> is required (playwright-core lives there)')
  if (!OFFLINE && !ORIGIN_ARG && !DIST) throw new Bad('setup', 'give --origin <url> or --dist <dir>')
  if (OFFLINE && (!DIST || !FIXTURES_PATH)) throw new Bad('setup', '--offline needs --dist and --fixtures')
  mkdirSync(OUT, { recursive: true })
  const origin = DIST ? DIST_ORIGIN : ORIGIN_ARG
  const fixtures = loadFixtures()
  const st = {
    origin,
    dist: DIST,
    fixtures,
    keys: Object.keys(fixtures).sort((a, b) => b.length - a.length),
    session: buildSession(),
    cors: {
      'Access-Control-Allow-Origin': origin, 'Access-Control-Allow-Credentials': 'true',
      'Access-Control-Allow-Headers': '*', 'Access-Control-Allow-Methods': '*', 'Content-Type': 'application/json',
    },
  }
  const require = createRequire(join(resolve(PORTAL), 'package.json'))
  const { chromium } = require('playwright-core')
  const browser = await chromium.launch({ executablePath: EDGE, headless: true })
  const boardOf = ctx => { ctx.origin = origin; return ctx }
  try {
    if (OFFLINE) {
      const b1 = await phaseB1(boardOf(await openPage(browser, st)))
      if (b1.advisor !== 'optional') throw new Bad('b1', `advisor is ${b1.advisor}, not optional`)
      if (b1.reportType !== 'absent') throw new Bad('b1', 'a report type control is present on the form')
      if (b1.commentary !== 'absent') throw new Bad('b1', 'a commentary control is present on the form')
      if (b1.firms.length !== 3) throw new Bad('b1', `the firm chooser lists ${b1.firms.length} firms, not 3`)
      if (b1.models !== 5) throw new Bad('b1', `the form shows ${b1.models} models, not 5`)
      const b2 = await phaseB2(boardOf(await openPage(browser, st)))
      const b3 = await phaseB3(boardOf(await openPage(browser, st)), TICKET_ARG ?? b2.ticket)
      if (b3.face !== 'yes') throw new Bad('b3', `face=${b3.face} headings=${b3.headings} value=${b3.value}`)
      if (b3.value !== 'yes') throw new Bad('b3', `face=${b3.face} but the VALUE section did not show`)
      say(`B-LEG-OFFLINE-OK b1_labels=${b1.labels} advisor=optional report_type=absent commentary=absent firms=3 models=5 b2_calls=${b2.calls} b3_face=yes`)
      return
    }
    const want = PHASE_ARG === 'all' ? ['b1', 'b2', 'b3'] : [PHASE_ARG]
    let ticket = TICKET_ARG
    for (const phase of want) {
      if (phase === 'b1') await phaseB1(boardOf(await openPage(browser, st)))
      else if (phase === 'b2') ticket = (await phaseB2(boardOf(await openPage(browser, st)))).ticket
      else if (phase === 'b3') {
        const b3 = await phaseB3(boardOf(await openPage(browser, st)), ticket)
        if (b3.face !== 'yes') throw new Bad('b3', `face=${b3.face}`)
      } else throw new Bad('setup', `unknown --phase ${clean(phase)}`)
    }
  } finally {
    await browser.close()
  }
}

main().catch(e => {
  if (e instanceof Bad) say(`${BAD_PREFIX} ${e.phase} ${clean(e.message)}`)
  else say(`${BAD_PREFIX} run unexpected error (${clean(e && e.name)})`)
  process.exitCode = 1
})
