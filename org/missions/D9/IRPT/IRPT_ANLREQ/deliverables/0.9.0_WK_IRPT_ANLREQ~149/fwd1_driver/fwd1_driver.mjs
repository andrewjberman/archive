// IRPT_ANLREQ FWD-1 page driver (0.9.0_WK_IRPT_ANLREQ~149, AR-y-345). Derived from .claude/skills/ui-walk/walk.mjs:
// playwright-core from the portal's node_modules (walk.mjs:24-25), Microsoft Edge with a bundled-Chromium fallback
// (walk.mjs:1603-1605), the real sign-in form (walk.mjs:1645-1659), and a route guard. The walker itself is NOT edited
// and is read-only by construction; this is a separate script with its own allow-list.
//
//   node fwd1_driver.mjs --plan
//   node fwd1_driver.mjs --selftest                       (offline: no browser, no network, no AWS, no boto3)
//   node fwd1_driver.mjs --base http://localhost:5174 --firm <firm-id> --holdings <csv> --out <dir>
//                        [--poll-minutes 20] --go IRPT_ANLREQ.TO-RUN-FWD1.<id>
// Without --go the driver prints the plan and exits 0. The run is AQ2's order under a never-widen pair, not the worker's.
// The driver never writes the password, the hash, a token or a cookie to the console, the report or any file.
import { createRequire } from 'node:module'
import { spawnSync } from 'node:child_process'
import crypto from 'node:crypto'
import fs from 'node:fs'
import os from 'node:os'
import path from 'node:path'
import { fileURLToPath, pathToFileURL } from 'node:url'

const SELF = fileURLToPath(import.meta.url)
const HERE = path.dirname(SELF)
const MINT = path.join(HERE, 'fwd1_mint.py')
// The worktree root is eight levels above this folder (deliverables/<serial>/fwd1_driver); FWD1_PORTAL overrides.
const PORTAL = process.env.FWD1_PORTAL || path.resolve(HERE, '../../../../../../../../portal')
const PYTHON = process.env.FWD1_PYTHON || 'python'
const EMAIL = 'fwd1-staff-r41a@opal.invalid'
const FIRM_CHOICE_LABEL = 'Choose the firm this request is filed under'
const TITLE = 'SYNTHETIC IRPT_ANLREQ FWD-1 run r41, do not action'
const NEW_TICKET_LABEL = 'New Ticket'
const SUBMIT_LABEL = 'File Analysis Request'
const TABS = ['Open', 'In Progress', 'Completed']
const GO_RE = /^IRPT_ANLREQ\.TO-RUN-FWD1\.\S+$/
const ANALYTICS_RE = /\/analytics\/ingest$/
const POST_ALLOWED = [
  /^\/auth\/login$/,
  /^\/auth\/refresh$/,
  /^\/auth\/logout$/,
  /^\/api\/scoped\/investor-reporting\/analysis\/inputs$/,
  /^\/api\/scoped\/tickets$/,
  /^\/api\/scoped\/investor-reporting\/analysis$/,
  /^\/api\/scoped\/tickets\/[A-Za-z0-9_-]+\/report$/,
]
const STEPS = [
  'STEP-1 generate the password in memory (crypto.randomBytes 24, base64url); never written anywhere',
  'STEP-2 python fwd1_mint.py mint, the password on STDIN only (one users row, attribute_not_exists(PK))',
  'STEP-3 launch the browser behind the route guard; sign in through the real form (#email, #password, button[type=submit])',
  'STEP-4 /ticket-center: New Ticket, type Analysis Request, the firm, the form, setInputFiles on Holdings file, click File Analysis Request; take the ticket id from the POST /api/scoped/tickets answer',
  'STEP-4B from the Submit click on the driver only reads (waits and reads; no click, fill or post)',
  'STEP-5 poll the ticket page: reload every 60 s for --poll-minutes; record the four attachments present and openable; stop when all four are present',
  'STEP-6 finally: close the browser, python fwd1_mint.py remove, record its ABSENT GSI and ABSENT CONSISTENT lines',
  'STEP-7 write run_report.json (times, ticket id, polls, guard refusals, ABSENT lines, screenshot names; never a password, hash, token or cookie)',
]

const iso = () => new Date().toISOString()
const sleep = (ms) => new Promise((r) => setTimeout(r, ms))

// ---- the base: exactly localhost -----------------------------------------------------------------------------------
export function checkBase(base) {
  let u
  try { u = new URL(base) } catch { return 'not a URL' }
  if (u.protocol !== 'http:') return 'scheme must be http'
  if (u.hostname !== 'localhost') return 'host must be exactly localhost'
  if (u.username || u.password) return 'no credentials in the base'
  if (u.pathname !== '/' || u.search || u.hash) return 'the base is an origin with no path'
  return null
}

// ---- the route guard: GET, HEAD, OPTIONS on the base origin; exactly seven POST shapes on the base origin ----------
export function admit(method, url, base) {
  const m = String(method).toUpperCase()
  let u
  let b
  try { u = new URL(url); b = new URL(base) } catch { return false }
  if (u.origin !== b.origin) return false
  if (m === 'GET' || m === 'HEAD' || m === 'OPTIONS') return true
  if (m === 'POST') return POST_ALLOWED.some((re) => re.test(u.pathname))
  return false
}

// ---- secrets never reach a log line, the report or a file ----------------------------------------------------------
export function redact(text, secrets = []) {
  let out = String(text)
  for (const s of secrets) if (typeof s === 'string' && s.length >= 6) out = out.split(s).join('[REDACTED]')
  out = out.replace(/(refresh_token|access_token|accessToken|passwordHash|password|token|cookie)(["'\s]*[:=]\s*["']?)[^\s"',;}&]+/gi,
    '$1$2[REDACTED]')
  out = out.replace(/Bearer\s+[A-Za-z0-9._~+/=-]+/g, 'Bearer [REDACTED]')
  return out
}

export function generatePassword() {
  return crypto.randomBytes(24).toString('base64url')
}

export function findTicketId(node, depth = 0) {
  if (!node || typeof node !== 'object' || depth > 6) return null
  if (typeof node.ticket_id === 'string' && /^[A-Za-z0-9_-]+$/.test(node.ticket_id)) return node.ticket_id
  for (const v of Object.values(node)) {
    const f = findTicketId(v, depth + 1)
    if (f) return f
  }
  return null
}

const pathOf = (url) => { try { return new URL(url).pathname } catch { return '(unparsed)' } }

export function parseArgs(argv) {
  const o = { base: 'http://localhost:5174', firm: null, holdings: null, out: null, pollMinutes: 20, plan: false, selftest: false, go: null }
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i]
    const next = () => argv[++i]
    if (a === '--base') o.base = next()
    else if (a === '--firm') o.firm = next()
    else if (a === '--holdings') o.holdings = next()
    else if (a === '--out') o.out = next()
    else if (a === '--poll-minutes') o.pollMinutes = Number(next())
    else if (a === '--go') o.go = next() ?? null
    else if (a === '--plan') o.plan = true
    else if (a === '--selftest') o.selftest = true
    else return { error: 'unknown argument ' + a }
  }
  return { o }
}

function printPlan(base) {
  console.log('PLAN IRPT_ANLREQ FWD-1 driver (AR-y-345); base ' + base + '; plan mode launches nothing')
  for (const s of STEPS) console.log(s)
}

// ---- the run (never reached without --go, a localhost base and a valid order token) --------------------------------
async function run(o) {
  const secrets = []
  const steps = []
  const shots = []
  let shotN = 0
  const report = { schema: 'fwd1_run_report/1', base: o.base, firm: o.firm, started_utc: iso(), order: o.go, steps,
    polls: [], guard_refused: [], absent: [], screenshots: shots, ticket_id: null, errors: [], remove_rc: null }
  const log = (line) => {
    const text = `${iso()} ${redact(line, secrets)}`
    console.log(text)
    steps.push(text)
  }
  fs.mkdirSync(o.out, { recursive: true })
  const shot = async (page, name) => {
    shotN += 1
    const f = `${String(shotN).padStart(2, '0')}-${name}.png`
    await page.screenshot({ path: path.join(o.out, f), fullPage: true }).catch(() => {})
    shots.push(f)
    return f
  }
  let password = null
  let browser = null
  try {
    password = generatePassword()
    secrets.push(password)
    log('STEP-1 password generated in memory (' + password.length + ' characters, never written)')

    const mint = spawnSync(PYTHON, [MINT, 'mint'], { input: JSON.stringify({ password }), encoding: 'utf8', timeout: 180000, windowsHide: true })
    log('STEP-2 mint rc=' + mint.status + ' ' + String(mint.stdout || '').trim())
    if (mint.status !== 0) throw new Error('mint did not return OK')

    const portalRequire = createRequire(path.join(PORTAL, 'package.json'))
    const { chromium } = portalRequire('playwright-core')
    try { browser = await chromium.launch({ channel: 'msedge', headless: true }) } catch { browser = await chromium.launch({ headless: true }) }
    const context = await browser.newContext({ viewport: { width: 1440, height: 900 } })
    const page = await context.newPage()
    await page.route('**/*', (route) => {
      const r = route.request()
      const m = r.method()
      const url = r.url()
      if (ANALYTICS_RE.test(pathOf(url))) return route.fulfill({ status: 204, body: '' }) // portal telemetry answered locally, never sent
      if (admit(m, url, o.base)) return route.continue()
      report.guard_refused.push(m + ' ' + pathOf(url))
      return route.abort('blockedbyclient')
    })

    await page.goto(o.base + '/login', { waitUntil: 'domcontentloaded', timeout: 30000 })
    await page.fill('#email', EMAIL)
    await page.fill('#password', password)
    await page.click('button[type=submit]')
    await page.waitForURL((u) => !/\/login/.test(u.pathname), { timeout: 30000 }).catch(() => {})
    if (/\/login/.test(pathOf(page.url()))) throw new Error('sign-in did not leave /login')
    log('STEP-3 signed in through the real form, now at ' + pathOf(page.url()))
    await shot(page, 'signed-in')

    await page.goto(o.base + '/ticket-center', { waitUntil: 'domcontentloaded', timeout: 30000 })
    await page.getByRole('button', { name: NEW_TICKET_LABEL, exact: true }).click()
    await page.locator('select:has(option[value="analysis_request"])').selectOption('analysis_request')
    await page.getByPlaceholder('Title (what is being requested?)').fill(TITLE)
    await page.locator('input[aria-label="Advisor"]').fill('SYNTHETIC FWD-1 advisor')
    await page.locator('input[aria-label="Household"]').fill('SYNTHETIC FWD-1 household')
    const firmSel = page.getByLabel(FIRM_CHOICE_LABEL, { exact: true })
    await firmSel.waitFor({ state: 'visible', timeout: 30000 })
    await firmSel.selectOption(o.firm)
    if ((await firmSel.inputValue()) !== o.firm) throw new Error('the firm control did not take the chosen firm id')
    await page.locator('select[aria-label="Report type"]').selectOption('Overview')
    await page.locator('input[aria-label="Holdings file"]').setInputFiles(o.holdings)
    const submit = page.getByRole('button', { name: SUBMIT_LABEL, exact: true })
    await submit.waitFor({ state: 'visible', timeout: 30000 })
    for (let i = 0; i < 30 && !(await submit.isEnabled()); i++) await sleep(1000)
    if (!(await submit.isEnabled())) throw new Error('the Submit control stayed disabled (a held reason)')
    await shot(page, 'before-submit')

    const ticketAnswer = page.waitForResponse((r) => r.request().method() === 'POST' && pathOf(r.url()) === '/api/scoped/tickets', { timeout: 240000 })
    await submit.click()
    log('STEP-4 Submit clicked; from here the driver only reads')
    const resp = await ticketAnswer
    let body = null
    try { body = await resp.json() } catch { body = null }
    report.ticket_id = findTicketId(body)
    if (!report.ticket_id) throw new Error('no ticket_id in the POST /api/scoped/tickets answer (status ' + resp.status() + ')')
    log('STEP-4 ticket ' + report.ticket_id + ' filed (POST /api/scoped/tickets status ' + resp.status() + ')')

    const deadline = Date.now() + o.pollMinutes * 60000
    let n = 0
    while (Date.now() < deadline) {
      await sleep(Math.min(60000, Math.max(0, deadline - Date.now())))
      n += 1
      await page.reload({ waitUntil: 'domcontentloaded', timeout: 60000 })
      const rec = await readPackage(page, report.ticket_id)
      rec.n = n
      rec.utc = iso()
      report.polls.push(rec)
      await shot(page, 'poll-' + n)
      log('STEP-5 poll ' + n + ' tab=' + rec.tab + ' row_found=' + rec.row_found + ' all_four_present=' + rec.all_four_present)
      if (rec.all_four_present) break
    }
  } catch (e) {
    report.errors.push(redact(String((e && e.message) || e), secrets))
    log('ERROR ' + redact(String((e && e.message) || e), secrets))
  } finally {
    try { if (browser) await browser.close() } catch { /* the browser is gone; the removal below still runs */ }
    const rm = spawnSync(PYTHON, [MINT, 'remove'], { encoding: 'utf8', timeout: 420000, windowsHide: true })
    report.remove_rc = rm.status
    report.absent = String(rm.stdout || '').split(/\r?\n/).filter((l) => /^(ABSENT|PRESENT) (GSI|CONSISTENT) /.test(l))
    log('STEP-6 remove rc=' + rm.status + ' ' + report.absent.join(' | '))
  }
  report.ended_utc = iso()
  log('STEP-7 run_report.json written')
  fs.writeFileSync(path.join(o.out, 'run_report.json'), redact(JSON.stringify(report, null, 2), secrets) + '\n')
  return report.errors.length === 0 && report.absent.length === 2 && report.remove_rc === 0 ? 0 : 1
}

// Reads only: the four attachment items of the ticket's row in the board (the package row follows the ticket row).
async function readPackage(page, ticketId) {
  const out = { tab: null, row_found: false, items: {}, all_four_present: false }
  for (const tab of TABS) {
    if (tab !== 'Open') await page.getByRole('button', { name: tab, exact: true }).click()
    await page.waitForLoadState('networkidle', { timeout: 20000 }).catch(() => {})
    const cell = page.getByRole('cell', { name: ticketId, exact: true })
    if ((await cell.count()) === 0) continue
    out.tab = tab
    out.row_found = true
    const pkg = cell.locator('xpath=ancestor::tr[1]/following-sibling::tr[1]')
    for (const [k, slot] of [['original', 'open-package-original'], ['report', 'open-package-report'], ['commentary', 'open-package-commentary']]) {
      const el = pkg.locator(`[data-slot="${slot}"]`)
      const present = (await el.count()) > 0
      out.items[k] = { present, openable: present ? await el.first().isEnabled() : false }
    }
    out.items.form = { present: (await pkg.locator('[data-slot="form-as-filled"]').count()) > 0, openable: null }
    break
  }
  out.all_four_present = ['original', 'form', 'report', 'commentary'].every((k) => out.items[k] && out.items[k].present)
  return out
}

function selftest() {
  const B = 'http://localhost:5174'
  const cases = []
  const check = (name, cond) => cases.push([name, !!cond])
  const POSTS = ['/auth/login', '/auth/refresh', '/auth/logout',
    '/api/scoped/investor-reporting/analysis/inputs?selected_tenant=49financial', '/api/scoped/tickets',
    '/api/scoped/investor-reporting/analysis?selected_tenant=49financial', '/api/scoped/tickets/TKT-abc_1/report']
  for (const p of POSTS) check('admit POST ' + p.split('?')[0], admit('POST', B + p, B))
  check('admit GET on the base', admit('GET', B + '/ticket-center', B))
  check('admit HEAD on the base', admit('HEAD', B + '/', B))
  check('admit OPTIONS on the base', admit('OPTIONS', B + '/api/scoped/tickets', B))
  check('refuse POST /api/scoped/tickets/abc/claim', !admit('POST', B + '/api/scoped/tickets/abc/claim', B))
  check('refuse POST /api/scoped/tickets/abc/complete', !admit('POST', B + '/api/scoped/tickets/abc/complete', B))
  check('refuse PUT', !admit('PUT', B + '/api/scoped/tickets/abc/report', B))
  check('refuse DELETE', !admit('DELETE', B + '/api/scoped/tickets', B))
  check('refuse POST to another host', !admit('POST', 'http://example.com/auth/login', B))
  check('refuse GET to another host', !admit('GET', 'http://example.com/', B))
  check('base refuses http://example.com', checkBase('http://example.com') !== null)
  check('base refuses https://localhost.evil.com', checkBase('https://localhost.evil.com') !== null)
  check('base refuses http://localhost:5174.evil', checkBase('http://localhost:5174.evil') !== null)
  check('base admits http://localhost:5174', checkBase(B) === null)
  const p1 = generatePassword()
  const p2 = generatePassword()
  check('two generated passwords differ', p1 !== p2)
  check('generated passwords are at least 24 characters', p1.length >= 24 && p2.length >= 24)
  const PW = 'SAMPLE-PASSWORD-xyz-987'
  const RT = 'SAMPLE-REFRESH-VALUE-123456'
  const red = redact('step=login password=' + PW + ' refresh_token=' + RT + ' Authorization: Bearer abc.def.ghi', [PW, RT])
  check('redactor removes a known password and a known refresh_token value', !red.includes(PW) && !red.includes(RT))
  // plan mode with boto3 poisoned: the plan prints the steps in order and exits 0
  const poison = fs.mkdtempSync(path.join(os.tmpdir(), 'fwd1_poison_'))
  fs.mkdirSync(path.join(poison, 'boto3'))
  fs.writeFileSync(path.join(poison, 'boto3', '__init__.py'), 'raise ImportError("boto3 must not be imported in plan mode")\n')
  const plan = spawnSync(process.execPath, [SELF, '--plan'], { encoding: 'utf8', env: { ...process.env, PYTHONPATH: poison }, timeout: 60000 })
  const pos = STEPS.map((s) => plan.stdout.indexOf(s.split(' ')[0]))
  check('plan mode exits 0 with boto3 poisoned', plan.status === 0)
  check('plan lists STEP-1 to STEP-7 in order', pos.every((p) => p >= 0) && pos.every((p, i) => i === 0 || p > pos[i - 1]))
  fs.rmSync(poison, { recursive: true, force: true })
  // no --go: the run is refused, the plan is printed, nothing is launched
  const noGo = spawnSync(process.execPath, [SELF, '--base', B, '--firm', '49financial', '--holdings', SELF, '--out', os.tmpdir()], { encoding: 'utf8', timeout: 60000 })
  check('without --go the run phase is refused (exit 0, plan only)', noGo.status === 0 && /RUN-REFUSED no --go/.test(noGo.stdout))
  const badGo = spawnSync(process.execPath, [SELF, '--base', B, '--firm', '49financial', '--holdings', SELF, '--out', os.tmpdir(), '--go', 'IRPT_ANLREQ.TO-RUN-FWD1.'], { encoding: 'utf8', timeout: 60000 })
  check('an empty order token is refused (exit 2)', badGo.status === 2 && /RUN-REFUSED/.test(badGo.stdout))
  const wrongGo = spawnSync(process.execPath, [SELF, '--base', B, '--firm', '49financial', '--holdings', SELF, '--out', os.tmpdir(), '--go', 'IRPT_ANLREQ.TO-AR-y-345'], { encoding: 'utf8', timeout: 60000 })
  check('a token outside the TO-RUN-FWD1 form is refused (exit 2)', wrongGo.status === 2)
  const badBase = spawnSync(process.execPath, [SELF, '--base', 'http://example.com', '--firm', '49financial', '--holdings', SELF, '--out', os.tmpdir(), '--go', 'IRPT_ANLREQ.TO-RUN-FWD1.x'], { encoding: 'utf8', timeout: 60000 })
  check('a non-localhost base is refused even with a token (exit 2)', badBase.status === 2)
  const failed = cases.filter(([, ok]) => !ok).map(([n]) => n)
  for (const [n, ok] of cases) console.log((ok ? 'case PASS ' : 'case FAIL ') + n)
  if (failed.length === 0) {
    console.log('SELFTEST-OK ' + cases.length + ' cases')
    return 0
  }
  console.log('SELFTEST-BAD ' + failed.join('; '))
  return 1
}

export async function main(argv) {
  if (argv.includes('--selftest')) return selftest()
  const parsed = parseArgs(argv)
  if (parsed.error) { console.log('REFUSED ' + parsed.error); return 2 }
  const o = parsed.o
  if (o.plan || !o.go) {
    printPlan(o.base)
    if (!o.plan) console.log('RUN-REFUSED no --go order token: plan only, nothing launched')
    return 0
  }
  const baseErr = checkBase(o.base)
  if (baseErr) { console.log('REFUSED base: ' + baseErr); return 2 }
  if (!GO_RE.test(o.go)) { console.log('RUN-REFUSED --go is not an IRPT_ANLREQ.TO-RUN-FWD1.<id> order token'); return 2 }
  if (!o.firm || !o.holdings || !o.out) { console.log('RUN-REFUSED --firm, --holdings and --out are required'); return 2 }
  if (!fs.existsSync(o.holdings)) { console.log('RUN-REFUSED the holdings file does not exist'); return 2 }
  if (!(o.pollMinutes > 0 && o.pollMinutes <= 60)) { console.log('RUN-REFUSED --poll-minutes must be in (0, 60]'); return 2 }
  printPlan(o.base)
  return run(o)
}

if (import.meta.url === pathToFileURL(path.resolve(process.argv[1] || '')).href) {
  main(process.argv.slice(2)).then((rc) => { process.exitCode = rc }, (e) => {
    console.log('ERROR ' + String((e && e.message) || e).slice(0, 200))
    process.exitCode = 1
  })
}
