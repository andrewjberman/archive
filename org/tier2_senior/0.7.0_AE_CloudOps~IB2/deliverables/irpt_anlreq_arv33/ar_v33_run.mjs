// IRPT_ANLREQ TO-RUN-AR-v33 (0.7.0_AE_CloudOps~IB2), SITTING 2: mint ONE staff-only synthetic user, sign in through the real login page on
// http://localhost:5174, open the Ticket Center by the sidebar link, read ARM A (TCK-20261015-944c84f8, In Progress, fixture report_ref + the standing
// hop_failure) and ARM B (TCK-20261014-2965a5e0, Open, packaged), one full-page screenshot each, then remove the user.
//
//   node ar_v33_run.mjs --go <dir_for_screenshots> <facts.json>
//
// Model: org/tier2_senior/0.7.0_AE_CloudOps~AQ2/deliverables/irpt_anlreq_arv32/ar_v32_run.mjs (same guard, same redaction, same password handling).
// The password is 32 random bytes (base64url) generated in memory, handed ONLY to the signed helper fwd1_mint.py on its STDIN and typed into the real
// login form by the browser automation; it is never printed, logged, written, placed in argv or in the environment. Every output line passes through
// redact(). Requests: GET/HEAD/OPTIONS on the base origin and POST only /auth/login, /auth/refresh, /auth/logout and the read-shaped directory resolve;
// analytics ingest is answered locally. No Retry or other button is pressed. The facts file holds closed values only.
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { createRequire } from 'node:module'
import { spawnSync } from 'node:child_process'
import { fileURLToPath } from 'node:url'

const SELF = fileURLToPath(import.meta.url)
const HERE = path.dirname(SELF)
const ROOT = path.resolve(HERE, '../../../../..')
const PORTAL = path.join(ROOT, 'portal')
const MINT = path.join(ROOT, 'org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/0.9.0_WK_IRPT_ANLREQ~149/fwd1_driver/fwd1_mint.py')
const PYTHON = 'python'
const BASE = 'http://localhost:5174'
const EMAIL = 'fwd1-staff-r41b@opal.invalid'
const TICKET_A = 'TCK-20261015-944c84f8'
const TICKET_B = 'TCK-20261014-2965a5e0'
const REQ_A = 'REQ-d47252fe74634d0c5cdd8067'
const REQ_B = 'REQ-28a5ca6be3b7f438a9ca8217'
const STEP_RE = /^\s*The analysis was generated, but the commentary draft step was refused\./i
const WORDS_RE = /commentary draft step was refused/i
const STATUS_PATH = /^\/api\/scoped\/investor-reporting\/status\/([A-Za-z0-9_-]+)/
const POST_ALLOWED = [/^\/auth\/login$/, /^\/auth\/refresh$/, /^\/auth\/logout$/, /^\/api\/scoped\/investor-reporting\/directory\/resolve$/]
const ANALYTICS_RE = /\/analytics\/ingest$/

export function admit(method, url, base = BASE) {
  const m = String(method).toUpperCase()
  let u, b
  try { u = new URL(url); b = new URL(base) } catch { return false }
  if (u.origin !== b.origin) return false
  if (m === 'GET' || m === 'HEAD' || m === 'OPTIONS') return true
  return m === 'POST' && POST_ALLOWED.some((re) => re.test(u.pathname))
}

export function redact(text, secrets = []) {
  let out = String(text)
  for (const s of secrets) if (typeof s === 'string' && s.length >= 6) out = out.split(s).join('[REDACTED]')
  out = out.replace(/(refresh_token|access_token|accessToken|passwordHash|password|token|cookie)(["'\s]*[:=]\s*["']?)[^\s"',;}&]+/gi, '$1$2[REDACTED]')
  return out.replace(/Bearer\s+[A-Za-z0-9._~+/=-]+/g, 'Bearer [REDACTED]')
}

export function closedFields(body) {
  const out = { public_reason_code: null, actions: [] }
  const walk = (x) => {
    if (Array.isArray(x)) { x.forEach(walk); return }
    if (x && typeof x === 'object') {
      if (typeof x.public_reason_code === 'string' && out.public_reason_code === null) out.public_reason_code = x.public_reason_code
      if (Array.isArray(x.actions)) for (const a of x.actions) if (a && typeof a.action === 'string') out.actions.push(a.action)
      Object.values(x).forEach(walk)
    }
  }
  walk(body)
  out.actions = [...new Set(out.actions)]
  return out
}

export function generatePassword() { return crypto.randomBytes(32).toString('base64url') }

async function run(shotDir, factsPath) {
  const secrets = []
  const facts = { started_utc: new Date().toISOString(), origin: null, status_reads: [], minted: false, remove_lines: [], remove_rc: null, errors: [], guard_refused: [] }
  const log = (s) => console.log(redact(s, secrets))
  fs.mkdirSync(shotDir, { recursive: true })
  let browser = null
  let password = null
  try {
    password = generatePassword()
    secrets.push(password)
    log('STEP password generated in memory (' + password.length + ' characters, never written)')
    const mint = spawnSync(PYTHON, [MINT, 'mint'], { input: JSON.stringify({ password }), encoding: 'utf8', timeout: 180000, windowsHide: true })
    const mintOut = String(mint.stdout || '').trim()
    log('STEP mint rc=' + mint.status + ' ' + mintOut)
    facts.mint_line = mintOut
    if (mint.status !== 0 || !/MINT-OK READBACK-OK/.test(mintOut)) throw new Error('mint did not return MINT-OK READBACK-OK')
    facts.minted = true

    const u1py = 'import boto3,sys\n' +
      'c=boto3.client("dynamodb",region_name="us-east-1")\n' +
      'pk="USER#"+sys.argv[1]\n' +
      'r=c.get_item(TableName="opal-users-v2",Key={"PK":{"S":pk},"SK":{"S":"PROFILE"}},ConsistentRead=True).get("Item") or {}\n' +
      'q=c.query(TableName="opal-users-v2",KeyConditionExpression="PK = :p",ExpressionAttributeValues={":p":{"S":pk}},ConsistentRead=True)\n' +
      'g=lambda k:(r.get(k) or {}).get("S","ABSENT")\n' +
      'print("U1 users_row role=%s userType=%s firmId=%s entitlement_rows=%d status=%s"%(g("role"),g("userType"),g("firmId"),q["Count"]-(1 if r else 0),g("status")))\n'
    const u1 = spawnSync(PYTHON, ['-I', '-c', u1py, EMAIL], { encoding: 'utf8', timeout: 60000, windowsHide: true })
    facts.u1 = String(u1.stdout || '').trim()
    log(facts.u1 || 'U1 read failed rc=' + u1.status)
    if (!/^U1 users_row role=user userType=test-filer firmId=opal-capital entitlement_rows=0 status=active$/.test(facts.u1)) throw new Error('U1 is not the expected staff-only row: STOP')

    const portalRequire = createRequire(path.join(PORTAL, 'package.json'))
    const { chromium } = portalRequire('playwright-core')
    try { browser = await chromium.launch({ channel: 'msedge', headless: true }) } catch { browser = await chromium.launch({ headless: true }) }
    const context = await browser.newContext({ viewport: { width: 1440, height: 900 } })
    const page = await context.newPage()
    await page.route('**/*', (route) => {
      const r = route.request()
      const url = r.url()
      let p = ''
      try { p = new URL(url).pathname } catch { /* ignore */ }
      if (ANALYTICS_RE.test(p)) return route.fulfill({ status: 204, body: '' })
      if (admit(r.method(), url)) return route.continue()
      facts.guard_refused.push(r.method() + ' ' + p)
      return route.abort('blockedbyclient')
    })
    page.on('response', async (res) => {
      let u
      try { u = new URL(res.url()) } catch { return }
      const m = STATUS_PATH.exec(u.pathname)
      if (!m) return
      const rec = { request_id: m[1], http: res.status(), public_reason_code: null, actions: [] }
      try { Object.assign(rec, closedFields(await res.json())) } catch { /* not JSON: keep the status only */ }
      facts.status_reads.push(rec)
    })

    await page.goto(BASE + '/login', { waitUntil: 'domcontentloaded', timeout: 30000 })
    await page.fill('#email', EMAIL)
    await page.fill('#password', password)
    await page.click('button[type=submit]')
    await page.waitForURL((u) => !/\/login/.test(u.pathname), { timeout: 30000 }).catch(() => {})
    if (/\/login/.test(new URL(page.url()).pathname)) throw new Error('sign-in did not leave /login')
    await page.waitForLoadState('networkidle', { timeout: 20000 }).catch(() => {})
    log('D1 sign-in landed on ' + new URL(page.url()).pathname)

    let link = page.getByRole('link', { name: /ticket center/i })
    let how = 'sidebar link by name'
    if ((await link.count()) === 0) { link = page.locator('a[href*="ticket-center"]'); how = 'sidebar link by href' }
    facts.d2 = (await link.count()) > 0 ? how : 'NO sidebar link found'
    log('D2 ' + facts.d2)
    if ((await link.count()) === 0) throw new Error('no sidebar link to the Ticket Center was found')
    await link.first().click()
    await page.waitForLoadState('networkidle', { timeout: 20000 }).catch(() => {})
    await page.waitForTimeout(2500)

    const canvas = async () => page.evaluate(() => {
      const clear = (c) => !c || c === 'rgba(0, 0, 0, 0)' || c === 'transparent'
      const b = getComputedStyle(document.body).backgroundColor
      if (!clear(b)) return b
      const h = getComputedStyle(document.documentElement).backgroundColor
      if (!clear(h)) return h
      let el = document.querySelector('table')
      while (el) { const c = getComputedStyle(el).backgroundColor; if (!clear(c)) return c; el = el.parentElement }
      return b
    })
    const openTicket = async (tab, ticket) => {
      const btn = page.getByRole('button', { name: tab, exact: true })
      if ((await btn.count()) > 0 && tab !== 'Open') await btn.click().catch(() => {})
      await page.waitForLoadState('networkidle', { timeout: 20000 }).catch(() => {})
      await page.waitForTimeout(1500)
      const cell = page.getByRole('cell', { name: ticket, exact: true })
      const found = (await cell.count()) > 0
      if (found) {
        await cell.first().scrollIntoViewIfNeeded().catch(() => {})
        await cell.first().click().catch(() => {})
        await page.waitForLoadState('networkidle', { timeout: 20000 }).catch(() => {})
        await page.waitForTimeout(3000)
      }
      return { found, cell }
    }
    const read = async (ticket, cell) => {
      const body = await page.locator('body').innerText().catch(() => '')
      const block = page.locator('[data-slot="hop-failure"]')
      const blockTexts = await block.allInnerTexts().catch(() => [])
      const words = blockTexts.some((t) => WORDS_RE.test(t))
      const stepNamed = blockTexts.some((t) => STEP_RE.test(t))
      const container = page.locator('[data-slot="analysis-draft-and-package"]')
      const containerN = await container.count()
      const containerText = containerN > 0 ? (await container.first().innerText().catch(() => '')) : ''
      const errorBoundary = /something went wrong|application error|unhandled|error boundary/i.test(body)
      const intact = !errorBoundary && (await page.getByRole('cell', { name: ticket, exact: true }).count()) > 0 && body.trim().length > 200
      const rows = page.locator('table tbody tr')
      let blank = false
      const nRows = await rows.count()
      for (let i = 0; i < nRows; i++) { if ((await rows.nth(i).innerText().catch(() => 'x')).trim() === '') { blank = true; break } }
      return { words_shown: words, step_named: stepNamed, page_intact: intact, blank_row: blank, details_container: containerN > 0, details_text_chars: containerText.length,
               package_block: containerN > 0 && blockTexts.length === 0 && containerText.trim().length > 0, hop_failure_blocks: blockTexts.length }
    }

    // ARM A
    const a = await openTicket('In Progress', TICKET_A)
    facts.arm_a_found = a.found
    if (!a.found) throw new Error('TICKET_A not listed on In Progress')
    facts.a = await read(TICKET_A, a.cell)
    facts.a_canvas = await canvas()
    facts.origin = new URL(page.url()).origin
    await page.screenshot({ path: path.join(shotDir, 'ar_v33_a_page.png'), fullPage: true })
    log('ARM A: words_shown=' + facts.a.words_shown + ' step_named=' + facts.a.step_named + ' page_intact=' + facts.a.page_intact + ' blank_row=' + facts.a.blank_row + ' canvas=' + facts.a_canvas)
    facts.reads_after_arm_a = facts.status_reads.length

    // ARM B (partial)
    const b = await openTicket('Open', TICKET_B)
    facts.arm_b_found = b.found
    if (!b.found) throw new Error('TICKET_B not listed on Open')
    facts.b = await read(TICKET_B, b.cell)
    await page.screenshot({ path: path.join(shotDir, 'ar_v33_b_page.png'), fullPage: true })
    log('ARM B: words_shown=' + facts.b.words_shown + ' package_block=' + facts.b.package_block + ' page_intact=' + facts.b.page_intact)
  } catch (e) {
    facts.errors.push(redact(String(e && e.message ? e.message : e), secrets).slice(0, 300))
    log('ERROR ' + facts.errors[facts.errors.length - 1])
  } finally {
    if (browser) await browser.close().catch(() => {})
    if (facts.minted || password) {
      const rm = spawnSync(PYTHON, [MINT, 'remove'], { encoding: 'utf8', timeout: 420000, windowsHide: true })
      facts.remove_rc = rm.status
      facts.remove_lines = String(rm.stdout || '').split(/\r?\n/).filter((l) => /^(ABSENT|PRESENT) (GSI|CONSISTENT) /.test(l))
      log('STEP remove rc=' + rm.status + ' ' + facts.remove_lines.join(' | '))
    }
    facts.ended_utc = new Date().toISOString()
    fs.writeFileSync(factsPath, redact(JSON.stringify(facts, null, 1), secrets) + '\n')
  }
  return facts.errors.length === 0 && facts.remove_rc === 0 ? 0 : 1
}

if (process.argv[2] === '--go' && process.argv[3] && process.argv[4]) run(process.argv[3], process.argv[4]).then((c) => process.exit(c))
else if (process.argv[1] === SELF) { console.log('usage: node ar_v33_run.mjs --go <screenshot_dir> <facts.json>'); process.exit(2) }
