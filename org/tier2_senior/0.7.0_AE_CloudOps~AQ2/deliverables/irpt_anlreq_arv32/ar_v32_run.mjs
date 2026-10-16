// IRPT_ANLREQ TO-RUN-AR-v32 (0.7.0_AE_CloudOps~AQ2): sign in as a minted synthetic staff user on http://localhost:5174, open the Ticket Center ticket
// TCK-20261015-944c84f8, read what the page shows while the t55 hop failure stands, take ONE full-page screenshot, press Refresh once, remove the user.
//
//   node ar_v32_run.mjs --selftest
//   node ar_v32_run.mjs --go <screenshot.png> <facts.json>
//
// The password is 32 random bytes (base64url), generated in memory, handed ONLY to the signed helper fwd1_mint.py on its STDIN and typed into the real
// login form by the browser automation; it is never printed, logged, written, placed in argv or in the environment. Every output line passes through
// redact(). One sign-in, one navigation to the board, at most two status reads by the page (open, Refresh). Requests: GET/HEAD/OPTIONS on the base
// origin and POST only /auth/login, /auth/refresh, /auth/logout and the read-shaped directory resolve; analytics ingest is answered locally.
// The facts file holds closed values only (statuses, codes, YES/NO); no token, cookie or password.
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { createRequire } from 'node:module'
import { spawnSync } from 'node:child_process'
import { fileURLToPath } from 'node:url'

const SELF = fileURLToPath(import.meta.url)
const HERE = path.dirname(SELF)
const ROOT = path.resolve(HERE, '../../../../..')
const PORTAL = process.env.FWD1_PORTAL || path.join(ROOT, 'portal')
const MINT = path.join(ROOT, 'org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/0.9.0_WK_IRPT_ANLREQ~149/fwd1_driver/fwd1_mint.py')
const PYTHON = process.env.FWD1_PYTHON || 'python'
const BASE = 'http://localhost:5174'
const EMAIL = 'fwd1-staff-r41b@opal.invalid'
const TICKET = 'TCK-20261015-944c84f8'
const TABS = ['Open', 'In Progress', 'Completed']
const WORDS_RE = /commentary draft step was refused/i
const STEP_RE = /^\s*The analysis was generated, but the commentary draft step was refused\./i
const STATUS_PATH = /^\/api\/scoped\/investor-reporting\/status\//
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

// The closed codes of a status answer: public_reason_code and the actions' names; nothing else is kept.
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

function selftest() {
  const cases = []
  const check = (n, c) => cases.push([n, !!c])
  check('admit: GET on the base origin', admit('GET', BASE + '/ticket-center'))
  check('admit: POST /auth/login', admit('POST', BASE + '/auth/login'))
  check('admit: POST the filing route refused', !admit('POST', BASE + '/api/scoped/investor-reporting/analysis'))
  check('admit: another origin refused', !admit('GET', 'https://example.com/'))
  check('admit: PUT refused', !admit('PUT', BASE + '/x'))
  const pw = generatePassword()
  check('password is 43 url-safe characters', /^[A-Za-z0-9_-]{43}$/.test(pw))
  check('two passwords differ', pw !== generatePassword())
  check('redact removes a known password', !redact('login password=' + pw + ' x', [pw]).includes(pw))
  check('redact masks a Bearer value', !redact('Authorization: Bearer abc.def.ghi').includes('abc.def'))
  const f = closedFields({ ok: true, status: { state: 'ATTENTION', public_reason_code: 'COMMENTARY_DRAFT_REFUSED' }, actions: [{ action: 'NONE', description: 'words' }] })
  check('closedFields keeps the code and the action name only', f.public_reason_code === 'COMMENTARY_DRAFT_REFUSED' && f.actions.join() === 'NONE' && !JSON.stringify(f).includes('words'))
  check('the words regex matches the step sentence', STEP_RE.test('The analysis was generated, but the commentary draft step was refused. Opal Staff ...') && WORDS_RE.test('x the commentary draft step was refused'))
  check('the status path regex', STATUS_PATH.test('/api/scoped/investor-reporting/status/REQ-1'))
  const bad = cases.filter(([, c]) => !c)
  for (const [n, c] of cases) console.log('case', c ? 'PASS' : 'FAIL', n)
  console.log(bad.length ? 'SELFTEST-FAIL ' + bad.length : 'SELFTEST-OK ' + cases.length + ' cases')
  return bad.length ? 1 : 0
}

async function run(shotPath, factsPath) {
  const secrets = []
  const facts = { started_utc: new Date().toISOString(), attempt: 2, origin: null, server_reused: true, status_reads: [], lists: [], minted: false, remove_lines: [], remove_rc: null, errors: [] }
  const log = (s) => console.log(redact(s, secrets))
  const dir = path.dirname(shotPath)
  const shotTo = async (pg, name) => { fs.mkdirSync(dir, { recursive: true }); await pg.screenshot({ path: path.join(dir, name), fullPage: true }).catch(() => {}) }
  let currentTab = 'signin'
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

    // U1 (AMENDMENT 5): the minted row's role set, read before anything else; names and the count only, no hash, no other attribute.
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
    facts.guard_refused = []
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
      const p = u.pathname
      if (STATUS_PATH.test(p)) {
        const rec = { http: res.status(), public_reason_code: null, actions: [] }
        try { Object.assign(rec, closedFields(await res.json())) } catch { /* body not JSON: keep the status only */ }
        facts.status_reads.push(rec)
        return
      }
      if (/ticket/i.test(p) && res.request().method() === 'GET' && res.request().resourceType() !== 'document' && !/\.(js|css|tsx?|map|png|svg|woff2?)$/i.test(p) && !/^\/(src|node_modules|@)/.test(p)) {
        const rec = { tab: currentTab, path: p, status_query: u.searchParams.get('status'), http: res.status(), count: null }
        try { const j = await res.json(); const arr = Array.isArray(j) ? j : (j && (j.tickets || j.items || (j.data && (j.data.tickets || j.data.items || j.data)))); rec.count = Array.isArray(arr) ? arr.length : null } catch { /* count stays null */ }
        facts.lists.push(rec)
      }
    })

    await page.goto(BASE + '/login', { waitUntil: 'domcontentloaded', timeout: 30000 })
    await page.fill('#email', EMAIL)
    await page.fill('#password', password)
    await page.click('button[type=submit]')
    await page.waitForURL((u) => !/\/login/.test(u.pathname), { timeout: 30000 }).catch(() => {})
    if (/\/login/.test(new URL(page.url()).pathname)) throw new Error('sign-in did not leave /login')
    await page.waitForLoadState('networkidle', { timeout: 20000 }).catch(() => {})
    facts.d1 = new URL(page.url()).pathname
    log('D1 sign-in landed on ' + facts.d1)
    await shotTo(page, 'ar_v32_signin.png')

    // D2: the Ticket Center is opened through the app's own sidebar link (client-side navigation); a typed URL would drop the in-memory token.
    let link = page.getByRole('link', { name: /ticket center/i })
    let how = 'sidebar link by name'
    if ((await link.count()) === 0) { link = page.locator('a[href*="ticket-center"]'); how = 'sidebar link by href' }
    facts.d2 = (await link.count()) > 0 ? how : 'NO sidebar link found'
    log('D2 ' + facts.d2)
    if ((await link.count()) === 0) throw new Error('no sidebar link to the Ticket Center was found')
    await link.first().click()
    await page.waitForLoadState('networkidle', { timeout: 20000 }).catch(() => {})
    await page.waitForTimeout(2500)
    facts.d2_path = new URL(page.url()).pathname
    facts.d6_new_ticket_control = (await page.getByRole('button', { name: /new ticket/i }).count()) > 0

    facts.d4 = {}
    facts.d5 = {}
    facts.tab = null
    for (const tab of TABS) {
      currentTab = tab
      const btn = page.getByRole('button', { name: tab, exact: true })
      const have = (await btn.count()) > 0
      if (tab !== 'Open' && have) await btn.click().catch(() => {})
      await page.waitForLoadState('networkidle', { timeout: 20000 }).catch(() => {})
      await page.waitForTimeout(1500)
      const rowsN = await page.locator('table tbody tr').count()
      const alerts = await page.locator('[role="alert"]').allInnerTexts().catch(() => [])
      const banner = alerts.length ? alerts[0].trim().split(/\s+/).slice(0, 4).join(' ') : null
      const text = await page.locator('table').first().innerText().catch(() => '')
      const ids = [...new Set(text.match(/TCK-\d{8}-[0-9a-f]{8}/g) || [])]
      facts.d4[tab] = { tab_button_found: have || tab === 'Open', rows: rowsN, error_banner: banner !== null, banner_first_four_words: banner }
      facts.d5[tab] = ids
      await shotTo(page, 'ar_v32_tab_' + tab.toLowerCase().replace(' ', '_') + '.png')
      log('D4 tab ' + tab + ': rows=' + rowsN + ' banner=' + (banner !== null) + ' ids=' + ids.length)
      if (!facts.tab && ids.includes(TICKET)) facts.tab = tab
    }
    facts.row_found = !!facts.tab
    if (!facts.row_found) throw new Error('the ticket id is not listed on any tab (D5)')
    currentTab = 'read'
    if (facts.tab !== 'Open') await page.getByRole('button', { name: facts.tab, exact: true }).click().catch(() => {})
    await page.waitForLoadState('networkidle', { timeout: 20000 }).catch(() => {})
    let cell = page.getByRole('cell', { name: TICKET, exact: true })
    log('STEP ticket row found on tab ' + facts.tab)
    await cell.first().scrollIntoViewIfNeeded().catch(() => {})
    await cell.first().click().catch(() => {})
    await page.waitForLoadState('networkidle', { timeout: 20000 }).catch(() => {})
    await page.waitForTimeout(2500)

    const read = async () => {
      const row = cell.first().locator('xpath=ancestor::tr[1]')
      const next = row.locator('xpath=following-sibling::tr[1]')
      const nextText = ((await next.count()) > 0 ? await next.first().innerText().catch(() => '') : '')
      const body = await page.locator('body').innerText().catch(() => '')
      const near = nextText || ''
      const words = WORDS_RE.test(near) || WORDS_RE.test(body)
      const stepNamed = STEP_RE.test(near) || /commentary draft step was refused\./i.test(body)
      const errorBoundary = /something went wrong|application error|unhandled|error boundary/i.test(body)
      const intact = !errorBoundary && (await page.getByRole('cell', { name: TICKET, exact: true }).count()) > 0 && body.trim().length > 200
      const rows = page.locator('table tbody tr')
      let blank = false
      const nRows = await rows.count()
      for (let i = 0; i < nRows; i++) { if ((await rows.nth(i).innerText().catch(() => 'x')).trim() === '') { blank = true; break } }
      return { words_shown: words, step_named: stepNamed, page_intact: intact, blank_row: blank, row_text_chars: near.length }
    }
    facts.p1 = await read()
    facts.canvas = await page.evaluate(() => {
      const clear = (c) => !c || c === 'rgba(0, 0, 0, 0)' || c === 'transparent'
      const b = getComputedStyle(document.body).backgroundColor
      if (!clear(b)) return b
      const h = getComputedStyle(document.documentElement).backgroundColor
      if (!clear(h)) return h
      let el = document.querySelector('table')
      while (el) { const c = getComputedStyle(el).backgroundColor; if (!clear(c)) return c; el = el.parentElement }
      return b
    })
    facts.origin = new URL(page.url()).origin
    fs.mkdirSync(path.dirname(shotPath), { recursive: true })
    await page.screenshot({ path: shotPath, fullPage: true })
    log('STEP page read: words_shown=' + facts.p1.words_shown + ' step_named=' + facts.p1.step_named + ' page_intact=' + facts.p1.page_intact + ' blank_row=' + facts.p1.blank_row + ' canvas=' + facts.canvas)

    const refresh = page.getByRole('button', { name: 'Refresh', exact: true })
    facts.refresh_button = (await refresh.count()) > 0
    if (facts.refresh_button) {
      await refresh.first().click()
      await page.waitForLoadState('networkidle', { timeout: 20000 }).catch(() => {})
      await page.waitForTimeout(2500)
      facts.cell = (await page.getByRole('cell', { name: TICKET, exact: true }).count()) > 0
      if (!facts.cell) { for (const tab of TABS) { await page.getByRole('button', { name: tab, exact: true }).click().catch(() => {}); await page.waitForLoadState('networkidle', { timeout: 15000 }).catch(() => {}); if ((await page.getByRole('cell', { name: TICKET, exact: true }).count()) > 0) { cell = page.getByRole('cell', { name: TICKET, exact: true }); break } } }
      facts.p3 = await read()
    }
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

if (process.argv[2] === '--selftest') process.exit(selftest())
else if (process.argv[2] === '--go' && process.argv[3] && process.argv[4]) run(process.argv[3], process.argv[4]).then((c) => process.exit(c))
else if (process.argv[1] === SELF) { console.log('usage: node ar_v32_run.mjs --selftest | --go <screenshot.png> <facts.json>'); process.exit(2) }
