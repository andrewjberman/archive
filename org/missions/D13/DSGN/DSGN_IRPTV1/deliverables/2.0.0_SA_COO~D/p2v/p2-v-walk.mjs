/**
 * P-2 window leg V (2.0.0_SA_COO~P 104694; ledger irpt-p2-window-20261003): the P-1 walk, signed in, on one 49 Financial
 * account outside the original six -- the Performance tab, the print (the export modal's preview renders the print
 * document), and ONE export, whose receipt names the frozen as_of. Every investor-reporting answer is logged (path,
 * status, state, reason code; never a body), so a PATH A 49F refusal is recorded if the page still calls PATH A.
 *
 * Signs in with the dormant UI-walker account exactly as yh-submit-case.mjs does (arm -> one walk -> disarm in `finally`,
 * the password read in-process, never printed). The network guard admits the walker's own POSTs plus ONE
 * POST .../investor-reporting/export; every other write is aborted and logged.
 *
 * Usage: node <this file> --client "<search text>" [--no-export] [--base http://localhost:5174] [--headed]
 * `--no-export` stops after the print preview: no write is sent at all.
 * Output: <repo>/tmp/p2-v/<stamp>/ (gitignored): packet.json, netlog.tsv, guard.tsv, shots/. Client data stays local.
 */
import { createRequire } from 'node:module'
import { execFileSync } from 'node:child_process'
import { mkdirSync, writeFileSync } from 'node:fs'
import { fileURLToPath } from 'node:url'
import path from 'node:path'

const HERE = path.dirname(fileURLToPath(import.meta.url))
const ROOT = execFileSync('git', ['rev-parse', '--show-toplevel'], { cwd: HERE, encoding: 'utf8' }).trim()
const require = createRequire(path.join(ROOT, 'portal', 'package.json'))
const { chromium } = require('playwright-core')
const ACCOUNT = path.join(ROOT, '.claude', 'skills', 'ui-walk', 'ui_walker_account.py')
const EMAIL = 'opal-ui-walker@opal.test'

const argv = process.argv.slice(2)
const opt = { base: 'http://localhost:5174', client: null, headed: false, noExport: false, tabOnly: false, failHoldings: false }
for (let i = 0; i < argv.length; i++) {
  if (argv[i] === '--client') opt.client = argv[++i]
  else if (argv[i] === '--base') opt.base = argv[++i]
  else if (argv[i] === '--headed') opt.headed = true
  else if (argv[i] === '--no-export') opt.noExport = true
  else if (argv[i] === '--tab-only') { opt.tabOnly = true; opt.noExport = true }
  // CTO batch 238's real run: the holdings read answered locally with a bare 503, then the Holdings tab looked at. No
  // request leaves for that read; nothing is written.
  else if (argv[i] === '--fail-holdings') { opt.failHoldings = true; opt.noExport = true }
}
if (!opt.client) { console.error('--client "<search text>" is required'); process.exit(2) }
if (!/^http:\/\/localhost:\d+$/.test(opt.base)) { console.error('REFUSED: --base must be http://localhost:<port>'); process.exit(2) }

const stamp = new Date().toISOString().replace(/[-:]/g, '').replace(/\.\d+Z$/, 'Z')
const OUT = path.join(ROOT, 'tmp', 'p2-v', stamp)
mkdirSync(path.join(OUT, 'shots'), { recursive: true })
const t0 = Date.now()
const log = (...m) => console.log(new Date().toISOString().slice(11, 19), ...m)
const pathOnly = (u) => { try { return new URL(u).pathname } catch { return u } }
const py = (cmd, extraEnv = {}, ...args) => execFileSync('python', [ACCOUNT, cmd, ...args], { encoding: 'utf8', env: { ...process.env, ...extraEnv }, stdio: ['ignore', 'pipe', 'pipe'] })
let shotN = 0
async function shot(page, label) {
  shotN += 1
  await page.screenshot({ path: path.join(OUT, 'shots', `${String(shotN).padStart(3, '0')}-${label}.png`), fullPage: true }).catch((e) => log('shot failed', e.message))
}

const ADMITTED_POST = [/\/auth\/login$/, /\/auth\/refresh$/, /\/auth\/logout$/, /\/api\/scoped\/investor-reporting\/directory\/resolve$/, /\/api\/scoped\/investor-reporting\/selections$/]
const EXPORT = /\/api\/scoped\/investor-reporting\/export$/
const IR = /\/api\/scoped\/investor-reporting\//
const guard = []
const netlog = []
let exportPosts = 0
let armed = false
let holder = null
let browser
const packet = { leg: 'V', ledger: 'irpt-p2-window-20261003', base: opt.base, started_at: new Date(t0).toISOString(),
  portal_head: execFileSync('git', ['-C', path.join(ROOT, 'portal'), 'rev-parse', '--short', 'HEAD'], { encoding: 'utf8' }).trim() }

try {
  const armOut = py('arm'); log(armOut.trim().split('\n').filter((l) => !/password/i.test(l)).join(' | ')); holder = (armOut.match(/^HOLDER (\S+)/m) || [])[1] || null; armed = true
  const password = py('secret', { UI_WALK_CHILD: '1' })
  try { browser = await chromium.launch({ channel: 'msedge', headless: !opt.headed }) } catch { browser = await chromium.launch({ headless: !opt.headed }) }
  const context = await browser.newContext({ viewport: { width: 1440, height: 1000 } })
  const page = await context.newPage()
  context.on('page', (p) => log('POPUP', pathOnly(p.url())))

  // Send times too: the netlog's own time is the ANSWER's arrival, so a request that left before another answer
  // can read as after it.
  page.on('request', (req) => {
    const p = pathOnly(req.url())
    if (IR.test(p)) netlog.push([new Date().toISOString(), 'SENT ' + req.method(), p, '', '', '', '', ''].join('	'))
  })
  page.on('response', async (res) => {
    const p = pathOnly(res.url())
    if (!IR.test(p)) return
    const req = res.request()
    let state = '', reason = '', phases = ''
    try {
      const j = await res.json()
      state = j?.status?.state ?? j?.data?.state ?? ''
      reason = j?.status?.public_reason_code ?? j?.public_reason_code ?? ''
      phases = JSON.stringify(j?.status?.phases ?? j?.phases ?? '').slice(0, 300)
      // The export's own id (the receipt id), from the submit answer or a receipt read: an id, never a body.
      if (/\/export(\/[^/]+)?$/.test(p)) {
        const id = j?.data?.export_ref?.export_id ?? (j?.status?.state === 'QUEUED' || j?.status?.state === 'RUNNING' ? j?.status?.operation?.revision : null)
        if (id) packet.export_id = id
        if (j?.data?.facts?.frozen_as_of) packet.receipt_frozen_as_of = j.data.facts.frozen_as_of
        if (j?.data?.job_state) packet.receipt_job_state = j.data.job_state
      }
    } catch { /* not JSON */ }
    const keys = [...new URL(res.url()).searchParams.keys()].join(',')
    netlog.push([new Date().toISOString(), req.method(), p, keys, res.status(), state, reason, phases].join('\t'))
  })
  await page.route('**/*', (route) => {
    const req = route.request(); const m = req.method(); const p = pathOnly(req.url())
    if (opt.failHoldings && m === 'GET' && /\/investor-reporting\/holdings\//.test(p)) return route.fulfill({ status: 503, body: '' })
    if (m === 'GET' || m === 'HEAD' || m === 'OPTIONS') return route.continue()
    if (ADMITTED_POST.some((re) => re.test(p))) return route.continue()
    if (m === 'POST' && EXPORT.test(p) && exportPosts === 0 && !opt.noExport) { exportPosts += 1; return route.continue() }
    if (/\/analytics\/ingest$/.test(p)) return route.fulfill({ status: 204, body: '' })
    guard.push([new Date().toISOString(), m, p].join('\t'))
    return route.abort('blockedbyclient')
  })

  await page.goto(opt.base + '/login', { waitUntil: 'domcontentloaded', timeout: 30000 })
  await page.fill('#email', EMAIL)
  await page.fill('#password', password)
  await page.click('button[type=submit]')
  await page.waitForURL((u) => !/\/login/.test(u.pathname), { timeout: 30000 }).catch(() => {})
  if (/\/login/.test(new URL(page.url()).pathname)) throw new Error('login did not complete')
  log('signed in')

  await page.goto(opt.base + '/investor-reporting', { waitUntil: 'networkidle', timeout: 45000 }).catch(() => {})
  const combo = page.getByRole('combobox', { name: 'Client search' })
  await combo.click(); await combo.fill(opt.client)
  const option = page.getByRole('option').filter({ hasText: opt.client }).first()
  await option.waitFor({ timeout: 30000 })
  await option.click()
  log('client picked')

  if (opt.failHoldings) {
    await page.getByRole('button', { name: 'Holdings', exact: true }).or(page.getByRole('tab', { name: 'Holdings' })).first().click().catch(() => {})
    const panel = page.locator('[data-slot="status-panel"][data-tab="holdings"]').first()
    await panel.waitFor({ timeout: 30000 }).catch(() => {})
    packet.holdings_failed = {
      drawn: await panel.count() > 0,
      reason_code_attr: await panel.getAttribute('data-reason-code').catch(() => null),
      face_text: (await panel.evaluate((el) => { const c = el.cloneNode(true); c.querySelectorAll('details').forEach((d) => d.remove()); return c.textContent })
        .catch(() => '')).replace(/\s+/g, ' ').trim(),
      details_closed: await panel.locator('details').evaluate((d) => !d.open).catch(() => null),
    }
    await shot(page, 'holdings-failed')
    await panel.locator('details summary').click().catch(() => {})
    packet.holdings_failed.details_text = (await panel.locator('details').innerText().catch(() => '')).replace(/\s+/g, ' ').trim()
    await shot(page, 'holdings-failed-details-open')
    log('holdings', JSON.stringify(packet.holdings_failed))
    throw Object.assign(new Error('fail-holdings'), { tabOnly: true })
  }
  // 1. the Performance tab, waited on its own state
  const perf = page.getByRole('tab', { name: /performance/i }).first()
  if (await perf.count()) await perf.click().catch(() => {})
  const stateStart = Date.now()
  let tabState = 'ceiling'
  for (; Date.now() - stateStart < 45000;) {
    if (await page.locator('[data-slot="reporting-body"]').count()) { tabState = 'body'; break }
    if (await page.locator('[data-slot="reporting-refusal-words"]').count()) { tabState = 'refusal'; break }
    await page.waitForTimeout(500)
  }
  packet.tab = { state: tabState, waited_ms: Date.now() - stateStart }
  if (tabState === 'refusal') packet.tab.refusal = (await page.locator('[data-slot="reporting-refusal-words"]').first().innerText().catch(() => '')).slice(0, 300)
  await shot(page, 'performance-tab')
  log('tab', JSON.stringify(packet.tab))

  if (opt.tabOnly) throw Object.assign(new Error('tab-only'), { tabOnly: true })
  // 2. the print: the export modal's preview renders the print document
  await page.locator('[data-slot="export-button-control"]').first().click()
  const pvStart = Date.now()
  let phase = 'ceiling'
  for (; Date.now() - pvStart < 60000;) {
    const ph = await page.locator('[data-slot="preview"]').first().getAttribute('data-phase').catch(() => null)
    if (ph && ph !== 'loading') { phase = ph; break }
    await page.waitForTimeout(500)
  }
  packet.print = { preview_phase: phase, waited_ms: Date.now() - pvStart,
    report_kind: await page.locator('[data-slot="preview"]').first().getAttribute('data-report-kind').catch(() => null) }
  if (phase === 'refused') packet.print.refusal = (await page.locator('[data-slot="preview-refusal"]').first().innerText().catch(() => '')).slice(0, 300)
  await shot(page, 'print-preview')
  log('print', JSON.stringify(packet.print))

  // 3. ONE export; the receipt names the frozen as_of
  const submit = page.locator('[data-slot="submit-export"]').first()
  if (opt.noExport) {
    packet.export = { skipped: '--no-export' }
  } else if (await submit.count()) {
    await submit.click()
    const exStart = Date.now()
    let asOf = null
    for (; Date.now() - exStart < 120000;) {
      asOf = await page.locator('[data-slot="export-frozen-as-of"]').first().getAttribute('data-as-of').catch(() => null)
      const refused = await page.locator('[data-slot="export-refusal"]').count()
      if (asOf || refused) break
      await page.waitForTimeout(1000)
    }
    packet.export = {
      posts: exportPosts,
      job_state: await page.locator('[data-slot="receipt-panel"]').first().getAttribute('data-job-state').catch(() => null),
      frozen_as_of: asOf,
      frozen_as_of_words: (await page.locator('[data-slot="export-frozen-as-of"]').first().innerText().catch(() => '')).slice(0, 200),
      refusal: (await page.locator('[data-slot="export-refusal"]').first().innerText().catch(() => '')).slice(0, 300) || null,
      waited_ms: Date.now() - exStart,
    }
  } else {
    packet.export = { posts: 0, refusal: (await page.locator('[data-slot="export-refusal"]').first().innerText().catch(() => '')).slice(0, 300) || 'no submit control offered' }
  }
  await shot(page, 'export-receipt')
  log('export', JSON.stringify(packet.export))
} catch (e) {
  if (e && e.tabOnly) { packet.stopped = '--tab-only' } else {
  packet.error = String(e && e.message ? e.message : e).slice(0, 400)
  log('ERROR', packet.error)
  }
} finally {
  if (browser) await browser.close().catch(() => {})
  if (armed) {
    try { log(py('disarm', {}, holder).trim()) } catch (e) { log('DISARM FAILED -- run: python .claude/skills/ui-walk/ui_walker_account.py disarm', holder, e.message) }
  }
  packet.finished_at = new Date().toISOString()
  packet.path_a_calls = netlog.filter((l) => /\/performance(\/|\t|$)/.test(l.split('\t')[2]) && !/\/reporting\//.test(l.split('\t')[2])).length
  writeFileSync(path.join(OUT, 'packet.json'), JSON.stringify(packet, null, 2))
  writeFileSync(path.join(OUT, 'netlog.tsv'), netlog.join('\n') + '\n')
  writeFileSync(path.join(OUT, 'guard.tsv'), guard.join('\n') + (guard.length ? '\n' : ''))
  log('OUT', OUT)
}
