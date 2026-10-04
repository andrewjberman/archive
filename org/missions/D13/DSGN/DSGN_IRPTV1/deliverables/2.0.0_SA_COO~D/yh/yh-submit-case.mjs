/**
 * Y-H -- the page-walk SUBMIT harness (1.0.0_SA_CTO batch 178, CTO_FOLD_IN_IRPT_THREE_BRIEFS_20261002.md section 2;
 * brief 2 section 5, org/tier1_exec/4.0.0_SA_CRO~X/deliverables/IRPT_BRIEF_2_ANALYSIS_VARIANTS_GATES_TEST_CASES_20261002.md).
 *
 * It uploads and submits ONE named case from the Investor Reporting Analysis tab, as a person would. It records every
 * page API hop in a Playwright HAR (response content embedded) for 2.0.0_SA_COO~Y's backend join
 * (`org/tier1_exec/2.0.0_SA_COO/deliverables/IRPT_MVP_Y/live_walk/backend_join.py <page.har> <out.json> [--journal]`),
 * plus a packet record with the case, the UP-/REQ- ids and the marks (upload, reviewed, submitted, READY, sections).
 *
 * `/ui-walk` stays read-only by its own contract; this is a separate script. It signs in with the same dormant UI-walker
 * account (arm -> one walk -> disarm in `finally`, the password read in-process and never printed), and its network
 * guard admits exactly what the case needs beyond reads:
 *   - POST .../analysis/inputs  -- the upload; the page re-posts the SAME body every 3 s while symbols resolve (cap 60);
 *   - POST .../analysis         -- the submission, ONCE (a second one is aborted and recorded);
 * plus the walker's own admitted POSTs (auth login/refresh/logout, directory resolve, selections). Everything else that
 * writes is aborted and logged in guard.tsv.
 *
 * HAZARDS (brief 2 section 5.4, and the vendor ruling in its section 6, "Yes one at a time with queue empty"): a live run
 * is ONE job at a time with the queue empty; nobody signs in to YCharts in a browser during it (row S233). A live run
 * therefore refuses unless the operator passes `--queue-empty`, asserting the solo gate. `--fixture` runs the same page
 * drive with both POSTs answered locally (the committed producer upload records), no account and no backend write.
 *
 * Usage (from anywhere in the repo; the dev build on 5174):
 *   node <this file> --case A|D|typo [--file <xlsx>] [--client "<name>"] [--prepared-for "<text>"] [--title "<text>"]
 *        [--queue-empty] [--fixture] [--ready-ceiling-min 30] [--base http://localhost:5174] [--headed]
 * Output: <repo>/tmp/yh-submit/<stamp>/ (gitignored): packet.json, page.har, guard.tsv, shots/.
 */
import { createRequire } from 'node:module'
import { execFileSync } from 'node:child_process'
import { createHash } from 'node:crypto'
import { mkdirSync, writeFileSync, readFileSync, readdirSync } from 'node:fs'
import { fileURLToPath } from 'node:url'
import path from 'node:path'
import os from 'node:os'

const HERE = path.dirname(fileURLToPath(import.meta.url))
const ROOT = execFileSync('git', ['rev-parse', '--show-toplevel'], { cwd: HERE, encoding: 'utf8' }).trim()
const require = createRequire(path.join(ROOT, 'portal', 'package.json'))
const { chromium } = require('playwright-core')
const ACCOUNT = path.join(ROOT, '.claude', 'skills', 'ui-walk', 'ui_walker_account.py')
const EMAIL = 'opal-ui-walker@opal.test'
const BASE_API = '/api/scoped/investor-reporting'

// ---- the named cases (brief 2 section 4; files on the laptop's Downloads, cited by sha256 prefix) -------------------
const CASES = {
  A: { sha256: '500837992a3b9caa', variant: 'overview', comparisons: [], expect: 'READY', note: 'easy file, 99 rows, Overview (Y-1)' },
  typo: { sha256: '87afdc7db1c58b38', variant: 'overview', comparisons: [], expect: 'NEEDS_CORRECTION', note: 'easy file with AAPL -> APPL (Y-B baseline; Y-4 once the check gate is wired)' },
  D: { sha256: 'f0d344fa967504bd', variant: 'overview', comparisons: [], expect: 'NEEDS_CORRECTION', note: 'Stevens, 20 rows (Y-B baseline; Y-5 once the swap gate is wired)' },
  // Y-5 (2.0.0_SA_COO~Y 104499): Stevens' four untracked rows answered with the proxy Alyssa Keith chose (SGOV), named
  // on the page. Live once Y-5 serves; on the fixture plane the first answer offers NAME_PROXY and the re-post with
  // corrections answers NORMALIZED naming them.
  Dproxy: { sha256: 'f0d344fa967504bd', variant: 'overview', comparisons: [], proxies: { QKZAQ: 'SGOV', QBNYQ: 'SGOV', QUSBQ: 'SGOV', QBOKQ: 'SGOV' }, expect: 'READY', note: 'Stevens with user-named proxies (Y-5)' },
  // Y-5 V1 (2.0.0_SA_COO~Y 104651, ledger irpt-y5-20261003): the easy file's untracked TIMXX (row 100,
  // TICKER_DATA_NOT_ENTITLED) named SGOV on the page, like Dproxy; the re-post resolves NORMALIZED and the Overview READY.
  Aproxy: { sha256: '500837992a3b9caa', variant: 'overview', comparisons: [], proxies: { TIMXX: 'SGOV' }, expect: 'READY', note: 'easy file with TIMXX named SGOV (Y-5 V1)' },
  // Y-4 V1 (2.0.0_SA_COO~Y 104883, ledger irpt-y4-20261003): the typo file's APPL (row 2, TICKER_NOT_FOUND) carries a
  // provider-verified suggestion AAPL; the page's "Use AAPL" fills that correction, TIMXX is named SGOV, and the re-post
  // resolves NORMALIZED and the Overview READY. `accept` maps the file's ticker to the suggestion the case expects.
  typoAccept: { sha256: '87afdc7db1c58b38', variant: 'overview', comparisons: [], accept: { APPL: 'AAPL' }, proxies: { TIMXX: 'SGOV' }, expect: 'READY', note: 'typo file: accept AAPL for APPL, name SGOV for TIMXX (Y-4 V1)' },
  B: { sha256: '500837992a3b9caa', variant: 'comparison', comparisons: [{ kind: 'model', key: 'opal_ultra_long_term' }], expect: 'READY', note: 'easy file vs Opal Ultra Long-Term, Comparison (Y-2)' },
  C: { sha256: '500837992a3b9caa', variant: 'multicomp', comparisons: [{ kind: 'model', key: 'opal_ultra_long_term' }, { kind: 'etf', key: 'IWM' }], expect: 'READY', blocked: 'brief 2 item 2.3: a ticker admitted as a comparison (CTO batch 178 ruling 4) is 2.0.0_SA_COO~Y\'s half' },
}

// ---- args ---------------------------------------------------------------------------------------------------------
const argv = process.argv.slice(2)
const opt = { dryUpload: false, base: 'http://localhost:5174', case: null, file: null, client: null, preparedFor: 'Opal Capital (Y-H harness)', title: null, queueEmpty: false, fixture: false, readyCeilingMin: 30, headed: false }
for (let i = 0; i < argv.length; i++) {
  const a = argv[i]
  if (a === '--case') opt.case = argv[++i]
  else if (a === '--file') opt.file = argv[++i]
  else if (a === '--client') opt.client = argv[++i]
  else if (a === '--prepared-for') opt.preparedFor = argv[++i]
  else if (a === '--title') opt.title = argv[++i]
  else if (a === '--queue-empty') opt.queueEmpty = true
  else if (a === '--fixture') opt.fixture = true
  // --dry-upload: a live, signed-in drive that ABORTS the upload POST at the browser and records the URL and query it
  // carried -- no backend write, no vendor call. For checking what the page would send.
  else if (a === '--dry-upload') opt.dryUpload = true
  else if (a === '--ready-ceiling-min') opt.readyCeilingMin = Number(argv[++i])
  else if (a === '--base') opt.base = argv[++i]
  else if (a === '--headed') opt.headed = true
  else { console.error(`unknown argument ${a}`); process.exit(2) }
}
const kase = CASES[opt.case]
if (!kase) { console.error(`--case must be one of ${Object.keys(CASES).join(', ')}`); process.exit(2) }
if (kase.blocked) { console.error(`REFUSED: case ${opt.case} is blocked -- ${kase.blocked}`); process.exit(2) }
if (!/^http:\/\/localhost:\d+$/.test(opt.base)) { console.error('REFUSED: --base must be http://localhost:<port> (the local dev build)'); process.exit(2) }
if (!opt.fixture && !opt.queueEmpty && !opt.dryUpload) {
  console.error('REFUSED: a live run submits a real job. Pass --queue-empty to assert the solo gate (one job at a time, queue empty, nobody signed in to YCharts in a browser), or --fixture for the offline drive.')
  process.exit(2)
}

function sha256Of(file) { return createHash('sha256').update(readFileSync(file)).digest('hex') }
function findCaseFile(prefix) {
  const dir = path.join(os.homedir(), 'Downloads')
  for (const name of readdirSync(dir)) {
    if (!/\.(xlsx|csv)$/i.test(name)) continue
    const full = path.join(dir, name)
    if (sha256Of(full).startsWith(prefix)) return full
  }
  return null
}
const file = opt.file ?? findCaseFile(kase.sha256)
if (!file) { console.error(`REFUSED: no file in ~/Downloads has sha256 prefix ${kase.sha256} (pass --file)`); process.exit(2) }
const fileSha = sha256Of(file)
if (!fileSha.startsWith(kase.sha256)) { console.error(`REFUSED: ${path.basename(file)} has sha256 ${fileSha.slice(0, 16)}, case ${opt.case} names ${kase.sha256}`); process.exit(2) }

const stamp = new Date().toISOString().replace(/[-:]/g, '').replace(/\.\d+Z$/, 'Z')
const OUT = path.join(ROOT, 'tmp', 'yh-submit', `${stamp}-${opt.case}${opt.fixture ? '-fixture' : ''}`)
mkdirSync(path.join(OUT, 'shots'), { recursive: true })
const t0 = Date.now()
const log = (...m) => console.log(new Date().toISOString().slice(11, 19), ...m)
const marks = {}
const mark = (name) => { marks[name] = { ms: Date.now() - t0, at: new Date().toISOString() }; log('MARK', name, marks[name].ms) }
const guard = []
const ids = { upload_ids: [], input_id: null, request_id: null }
const posts = { inputs: 0, submissions: 0 }
let shotN = 0
async function shot(page, label) {
  shotN += 1
  const name = `${String(shotN).padStart(3, '0')}-${label.replace(/[^A-Za-z0-9_-]+/g, '-').slice(0, 60)}.png`
  await page.screenshot({ path: path.join(OUT, 'shots', name), fullPage: true }).catch((e) => log('shot failed', e.message))
}
const pathOnly = (u) => { try { return new URL(u).pathname } catch { return u } }
const py = (cmd, extraEnv = {}, ...args) => execFileSync('python', [ACCOUNT, cmd, ...args], { encoding: 'utf8', env: { ...process.env, ...extraEnv }, stdio: ['ignore', 'pipe', 'pipe'] })

// ---- the fixture plane (offline drive; the committed producer records) --------------------------------------------
const WIRE = path.join(ROOT, 'portal', 'src', 'pages', 'InvestorReporting', 'fixtures')
function fixturePlane() {
  const smoke = JSON.parse(readFileSync(path.join(WIRE, 'smoke', 'dsgn-irptv1-cottonwood.json'), 'utf8'))
  const producer = JSON.parse(readFileSync(path.join(ROOT, 'portal', 'src', 'pages', 'InvestorReporting', '__tests__', 'mvp-upload', 'tests', 'producer-upload.json'), 'utf8'))
  const request = JSON.parse(readFileSync(path.join(WIRE, 'wire', 'AnalysisRequest.valid.json'), 'utf8')).instance
  const status = JSON.parse(readFileSync(path.join(WIRE, 'wire', 'StatusEnvelope.valid.json'), 'utf8')).instance
  const firmId = smoke[`${BASE_API}/directory/resolve`].firm_id
  const upload = kase.expect === 'NEEDS_CORRECTION' || kase.proxies || kase.accept ? producer.correction.response : producer.normalized.response
  // Y-5 fixture: the first answer offers NAME_PROXY for each proxied ticker; the re-post with corrections answers the
  // producer's NORMALIZED record, its disclosures naming each proxy the page sent.
  // Y-4 fixture: an accepted ticker's finding is TICKER_NOT_FOUND with the provider-verified suggestion, ACCEPT_SUGGESTION first.
  const suggested = Object.entries(kase.accept ?? {}).map(([t, symbol], i) => ({ code: 'TICKER_NOT_FOUND', severity: 'ERROR', row: 2 + i, column: 'A',
    value: t, actions: ['ACCEPT_SUGGESTION', 'REPLACE_FILE', 'NAME_PROXY'], suggestion: { symbol, source: 'KIMI_CHECK_PROVIDER_VERIFIED', provider_receipt_sha256: 'f'.repeat(64) } }))
  const proxyFirst = kase.proxies || kase.accept ? { ...upload, data: { ...upload.data, state: 'NEEDS_CORRECTION', findings: [...suggested, ...Object.keys(kase.proxies ?? {}).map((t, i) => ({
    code: 'TICKER_DATA_NOT_ENTITLED', severity: 'ERROR', row: 14 + i, column: 'A', value: t, actions: ['NAME_PROXY'],
    description: `${t} is a real fund our data provider does not cover. Name a proxy to analyse it as.` }))] } } : null
  const proxyAnswer = (corrections) => ({ ...producer.normalized.response, firm_id: producer.normalized.response.firm_id ?? firmId,
    data: { ...producer.normalized.response.data, portfolio: { ...producer.normalized.response.data.portfolio, disclosures: { corrections } } } })
  const submission = { contract_version: 'v1', operation: 'analysis-requests', firm_id: firmId,
    data: { identity: { ...request.identity, tenant_firm_id: firmId, request_id: 'REQ-fixture-yh-0001' }, stage: 'QUEUED' },
    status: { ...status, state: 'PENDING', public_reason_code: 'QUEUED' }, unprojected_grant: { count: 0, denominator: 1, kinds: {} } }
  const catalogue = JSON.parse(readFileSync(path.join(WIRE, 'wire', 'ComparisonCatalogue.valid.json'), 'utf8')).instance
  const entries = [...catalogue.entries,
    { key: 'opal_ultra_long_term', label: 'Opal Ultra Long-Term', ticker: null, name_source: 'model_catalogue' },
    { key: 'IWM', label: 'iShares Russell 2000 ETF', ticker: 'IWM', name_source: 'etf_classifications' }]
  const reads = { ...smoke, [`${BASE_API}/analysis/comparisons`]: { contract_version: 'v1', operation: 'comparison-catalogue', firm_id: firmId, data: { ...catalogue, entries } },
    [`${BASE_API}/directory/search`]: { contract_version: 'v1', operation: 'directory-search', firm_id: firmId, data: smoke[`${BASE_API}/directory/browse`].data.entries, unprojected_grant: { count: 0, denominator: 1, kinds: {} } } }
  const keys = Object.keys(reads).sort((a, b) => b.length - a.length)
  return { upload: { ...(proxyFirst ?? upload), firm_id: upload.firm_id ?? firmId }, proxyAnswer, submission, reads, keys }
}
const SESSION = { accessToken: 'ui-smoke-token', user: { email: 'dev@opalcapital.com', name: 'Dev User', role: 'admin', userType: 'Dev', firmId: 'opal-capital', firmRole: null, advisorId: null, advisorRole: null, mustChangePassword: false } }

// ---- the network guard ---------------------------------------------------------------------------------------------
const ADMITTED_POST = [/\/auth\/login$/, /\/auth\/refresh$/, /\/auth\/logout$/, /\/api\/scoped\/investor-reporting\/directory\/resolve$/, /\/api\/scoped\/investor-reporting\/selections$/]
const INPUTS = /\/api\/scoped\/investor-reporting\/analysis\/inputs$/
const SUBMIT = /\/api\/scoped\/investor-reporting\/analysis$/
const INPUTS_CAP = 60

/** What the page itself sent: the variant and the comparison keys of the one submission (no client data). */
function noteSubmitted(req) {
  try { const b = req.postDataJSON(); packet.submitted = { variant: b.variant ?? null, comparison_keys: b.comparison_keys ?? null } } catch { packet.submitted = { unreadable: true } }
}
let armed = false
let holder = null
let browser
let context
var packet = { case: opt.case, note: kase.note, expect: kase.expect, file_sha256_prefix: fileSha.slice(0, 16), fixture: opt.fixture, base: opt.base,
  portal_head: execFileSync('git', ['-C', path.join(ROOT, 'portal'), 'rev-parse', '--short', 'HEAD'], { encoding: 'utf8' }).trim(), started_at: new Date(t0).toISOString() }
let outcome = 'NOT_STARTED'
try {
  let password = null
  if (!opt.fixture) {
    const armOut = py('arm'); log(armOut.trim()); holder = (armOut.match(/^HOLDER (\S+)/m) || [])[1] || null; armed = true
    password = py('secret', { UI_WALK_CHILD: '1' })
  }
  try { browser = await chromium.launch({ channel: 'msedge', headless: !opt.headed }) } catch { browser = await chromium.launch({ headless: !opt.headed }) }
  context = await browser.newContext({ viewport: { width: 1440, height: 1000 }, recordHar: { path: path.join(OUT, 'page.har'), content: 'embed', urlFilter: /\/(api|auth)\// } })
  const page = await context.newPage()
  const plane = opt.fixture ? fixturePlane() : null
  const json = (obj, status = 200) => ({ status, headers: { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': opt.base, 'Access-Control-Allow-Credentials': 'true', 'Access-Control-Allow-Headers': '*', 'Access-Control-Allow-Methods': '*' }, body: JSON.stringify(obj) })

  page.on('response', async (res) => {
    const p = pathOnly(res.url()); const m = res.request().method()
    if (m !== 'POST' || !(INPUTS.test(p) || SUBMIT.test(p))) return
    try {
      const j = await res.json(); const d = j && j.data
      if (INPUTS.test(p)) packet.upload_answer = { http: res.status(), ok: j?.ok ?? null, state: d?.state ?? j?.status?.state ?? null, reason: j?.status?.public_reason_code ?? null }
      if (INPUTS.test(p) && j?.ok === false) log('UPLOAD REFUSED', res.status(), j?.status?.state, j?.status?.public_reason_code)
      if (INPUTS.test(p) && d) { if (d.upload_id && !ids.upload_ids.includes(d.upload_id)) ids.upload_ids.push(d.upload_id); if (d.input_id) ids.input_id = d.input_id; log('UPLOAD', res.status(), d.state, d.upload_id) }
      if (SUBMIT.test(p)) { ids.request_id = d?.identity?.request_id ?? null; log('SUBMIT', res.status(), ids.request_id, d?.stage) }
    } catch { log('POST answer not JSON', p, res.status()) }
  })
  await page.route('**/*', (route) => {
    const req = route.request(); const m = req.method(); const url = req.url(); const p = pathOnly(url)
    if (plane) {
      if (m === 'OPTIONS' && !url.startsWith(opt.base)) return route.fulfill({ status: 204, headers: json({}).headers, body: '' })
      if (p.startsWith('/auth/refresh')) return route.fulfill(json(SESSION))
      if (m === 'POST' && INPUTS.test(p)) {
        posts.inputs += 1
        let sent = null; try { sent = req.postDataJSON() } catch { /* not JSON */ }
        if (sent && Array.isArray(sent.corrections)) { packet.corrections_sent = sent.corrections; return route.fulfill(json(plane.proxyAnswer(sent.corrections))) }
        return route.fulfill(json(plane.upload))
      }
      if (m === 'POST' && SUBMIT.test(p)) { noteSubmitted(req); posts.submissions += 1; if (posts.submissions > 1) { guard.push(['second-submit', m, p].join('\t')); return route.abort('blockedbyclient') } return route.fulfill(json(plane.submission)) }
      const key = p.startsWith('/api/') ? plane.keys.find((k) => url.includes(k)) : undefined
      if (key) return route.fulfill(json(plane.reads[key]))
      if (p.startsWith('/api/') || p.startsWith('/auth/') || p.startsWith('/v1/')) return route.fulfill(json({ error: 'no fixture (yh)' }, 404))
      return route.continue()
    }
    if (m === 'GET' || m === 'HEAD' || m === 'OPTIONS') return route.continue()
    if (ADMITTED_POST.some((re) => re.test(p))) return route.continue()
    if (m === 'POST' && INPUTS.test(p) && opt.dryUpload) { const q = new URL(url).searchParams; packet.dry_upload = { query: [...q.keys()], selected_tenant_present: q.has('selected_tenant') }; log('DRY UPLOAD (aborted)', JSON.stringify(packet.dry_upload)); return route.abort('blockedbyclient') }
    if (m === 'POST' && INPUTS.test(p) && posts.inputs < INPUTS_CAP) { posts.inputs += 1; return route.continue() }
    if (m === 'POST' && SUBMIT.test(p) && posts.submissions === 0) { noteSubmitted(req); posts.submissions += 1; return route.continue() }
    if (/\/analytics\/ingest$/.test(p)) return route.fulfill({ status: 204, body: '' })
    guard.push([new Date().toISOString(), m, p].join('\t'))
    return route.abort('blockedbyclient')
  })

  if (!opt.fixture) {
    await page.goto(opt.base + '/login', { waitUntil: 'domcontentloaded', timeout: 30000 })
    await page.fill('#email', EMAIL)
    await page.fill('#password', password)
    await page.click('button[type=submit]')
    await page.waitForURL((u) => !/\/login/.test(u.pathname), { timeout: 30000 }).catch(() => {})
    if (/\/login/.test(new URL(page.url()).pathname)) throw new Error('login did not complete')
    mark('signed_in')
  }
  await page.goto(opt.base + '/investor-reporting', { waitUntil: 'networkidle', timeout: 45000 }).catch(() => {})
  await page.waitForTimeout(1500)
  const client = opt.client ?? (opt.fixture ? 'Cottonwood Trust' : null)
  if (client) {
    const combo = page.getByRole('combobox', { name: 'Client search' })
    await combo.click(); await combo.fill(client)
    const option = page.getByRole('option', { name: new RegExp(client.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'i') }).first()
    await option.waitFor({ state: 'visible', timeout: 30000 })
    // The page's selected scope (and its tenant) exists only once POST /selections is answered: wait for it, so the
    // upload never races the selection (Case A dry drives 23:06Z and 23:11Z read the tenant absent, then present).
    const accepted = page.waitForResponse((r) => r.request().method() === 'POST' && /\/investor-reporting\/selections$/.test(pathOnly(r.url())), { timeout: 45000 }).catch(() => null)
    await option.click()
    packet.selection_answered = Boolean(await accepted)
    await page.waitForTimeout(2000)
  }
  await page.getByRole('button', { name: 'Analysis', exact: true }).or(page.getByRole('tab', { name: 'Analysis' })).first().click()
  await page.waitForTimeout(1500)
  await page.locator('[data-slot="analysis-portfolio-card"][data-portfolio="prospect"]').click()
  await page.locator('[data-slot="prospect-upload-button"]').click()
  await page.locator('[data-slot="upload-choose-trigger"] input[type=file]').setInputFiles(file)
  await page.locator('[data-slot="upload-proceed"]').click()
  await page.locator('[data-slot="prospect-composer"]').getByLabel('I confirm amounts without a currency label are US dollars').check().catch(() => {})
  await shot(page, 'file-chosen')
  packet.tenant_known_at_upload = await page.locator('[data-slot="prospect-composer"]').getAttribute('data-tenant-known').catch(() => null)
  if (opt.dryUpload) packet.react_props = await page.evaluate(() => {
    // Dry drives only: what the composer and the Analysis tab actually hold (keys and presence, never values).
    const el = document.querySelector('[data-slot="prospect-composer"]')
    const fk = el && Object.keys(el).find((k) => k.startsWith('__reactFiber'))
    let f = fk ? el[fk] : null
    const out = {}
    while (f) {
      const pr = f.memoizedProps
      if (pr && typeof pr === 'object' && 'api' in pr && !out.composer) out.composer = { keys: Object.keys(pr), selectedTenant_present: Boolean(pr.selectedTenant) }
      if (pr && typeof pr === 'object' && 'selectedScopeRef' in pr) { const r = pr.selectedScopeRef; out.analysis_tab = { selectedScopeRef: r ? Object.keys(r) : null, selectedTenant_present: Boolean(r && r.selectedTenant), tenant_present: Boolean(r && r.tenant) }; break }
      f = f.return
    }
    return out
  }).catch((e) => ({ error: String(e.message).slice(0, 120) }))
  mark('upload_pressed')
  await page.locator('[data-slot="prospect-composer"]').getByRole('button', { name: /Review portfolio/ }).click()
  let uploadState = null
  for (const start = Date.now(); Date.now() - start < 240000;) {
    uploadState = await page.locator('[data-slot="upload-state"]').getAttribute('data-state').catch(() => null)
    if (uploadState === 'NORMALIZED' || uploadState === 'NEEDS_CORRECTION') break
    if (await page.locator('[data-slot="prospect-composer"] [role=alert]').count()) break
    await page.waitForTimeout(500)
  }
  mark('upload_answered')
  packet.upload_state = uploadState
  packet.upload_alert = (await page.locator('[data-slot="prospect-composer"] [role=alert]').first().innerText().catch(() => null)) || null
  packet.upload_findings = await page.locator('[data-slot="upload-findings"] li').allInnerTexts().catch(() => [])
  await shot(page, `upload-${uploadState ?? 'no-state'}`)
  if ((kase.proxies || kase.accept) && uploadState === 'NEEDS_CORRECTION') {
    // Y-4: press the page's "Use <suggestion>" for each ticker the case accepts, and record what it filled.
    const accepted = []
    for (const [ticker, symbol] of Object.entries(kase.accept ?? {})) {
      const use = page.locator(`[data-slot="upload-accept-suggestion"][data-suggestion-for="${ticker}"]`)
      if (await use.count()) {
        await use.click()
        const filled = await page.locator(`[data-slot="upload-proxy-row"][data-proxy-for="${ticker}"] input`).inputValue().catch(() => null)
        accepted.push({ ticker, offered: symbol, filled })
      } else accepted.push({ ticker, offered: symbol, filled: null, missing: true })
    }
    packet.suggestions_accepted = accepted
    // Y-5: name each proxy the case states, then re-post with them through the page's own button.
    const named = []
    for (const [ticker, proxy] of Object.entries(kase.proxies ?? {})) {
      const row = page.locator(`[data-slot="upload-proxy-row"][data-proxy-for="${ticker}"] input`)
      if (await row.count()) { await row.fill(proxy); named.push(ticker) }
    }
    packet.proxies_named = named
    mark('proxies_pressed')
    await page.locator('[data-slot="upload-proxy-submit"]').click().catch(() => {})
    for (const start = Date.now(); Date.now() - start < 240000;) {
      uploadState = await page.locator('[data-slot="upload-state"]').getAttribute('data-state').catch(() => null)
      if (uploadState === 'NORMALIZED' || (uploadState === 'NEEDS_CORRECTION' && Date.now() - start > 5000)) break
      await page.waitForTimeout(500)
    }
    mark('proxies_answered')
    packet.upload_state_after_proxies = uploadState
    packet.proxies_shown = await page.locator('[data-slot="prospect-proxies-used"] li').allInnerTexts().catch(() => [])
    await shot(page, `proxies-${uploadState ?? 'no-state'}`)
  }
  if (opt.dryUpload) {
    outcome = packet.dry_upload ? `DRY_UPLOAD selected_tenant ${packet.dry_upload.selected_tenant_present ? 'PRESENT' : 'ABSENT'}` : 'DRY_UPLOAD_NOT_SENT'
  } else if (uploadState !== 'NORMALIZED') {
    outcome = uploadState === 'NEEDS_CORRECTION' ? 'NEEDS_CORRECTION'
      : packet.upload_answer?.ok === false ? `UPLOAD_REFUSED: ${packet.upload_answer.state ?? '?'} / ${packet.upload_answer.reason ?? '?'}` : 'UPLOAD_NOT_ANSWERED'
  } else {
    const prospect = page.locator('[data-slot="prospect-composer"]')
    if (kase.comparisons.length > 0) {
      await prospect.locator(`[data-slot="variant-card"][data-variant="${kase.variant}"]`).click()
      await page.locator('[data-slot="comparison-picker"]').waitFor({ state: 'visible', timeout: 30000 })
      for (const pick of kase.comparisons) {
        if (pick.kind === 'etf') await page.locator('[data-slot="picker-search"]').fill(pick.key)
        await page.locator(`[data-slot="picker-${pick.kind === 'etf' ? 'etf' : 'model'}"][data-key="${pick.key}"]`).click()
      }
      await page.locator('[data-slot="picker-done"]').click()
      packet.picked_on_page = await prospect.locator('[data-slot="comparison-key-list"] [data-comparison-key]').evaluateAll((els) => els.map((e) => e.getAttribute('data-comparison-key')))
      await shot(page, 'comparisons-picked')
    }
    await prospect.getByLabel('Report title (optional)').fill(opt.title ?? `Y-H case ${opt.case} ${stamp}`)
    await prospect.getByLabel('Prepared for').fill(opt.preparedFor)
    mark('submit_pressed')
    await prospect.getByRole('button', { name: /^Generate (Overview|Comparison|Multi-Comp)$/ }).click()
    for (const start = Date.now(); Date.now() - start < 60000 && !ids.request_id;) await page.waitForTimeout(250)
    mark('submit_answered')
    await page.locator('[data-slot="prospect-job-status"]').first().waitFor({ state: 'visible', timeout: 30000 }).catch(() => {})
    await shot(page, 'submitted')
    outcome = ids.request_id ? 'SUBMITTED' : 'SUBMIT_NOT_ANSWERED'
    if (ids.request_id && !opt.fixture) {
      // READY is read from the page's own owned-request history row, re-read once a minute up to the ceiling.
      const row = () => page.locator(`[data-row="owned-analysis-request"][data-request-id="${ids.request_id}"] [data-slot="owned-request-state"]`).first()
      let state = null
      for (const start = Date.now(); Date.now() - start < opt.readyCeilingMin * 60000;) {
        await page.waitForTimeout(60000)
        await page.reload({ waitUntil: 'networkidle', timeout: 45000 }).catch(() => {})
        if (client) {
          const combo = page.getByRole('combobox', { name: 'Client search' })
          await combo.click().catch(() => {}); await combo.fill(client).catch(() => {})
          await page.getByRole('option', { name: new RegExp(client.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'i') }).first().click({ timeout: 30000 }).catch(() => {})
        }
        await page.getByRole('button', { name: 'Analysis', exact: true }).or(page.getByRole('tab', { name: 'Analysis' })).first().click().catch(() => {})
        // The row reads "loading" until its own status read answers: wait for that answer (up to 30 s), not a flat 3 s.
        for (const t0 = Date.now(); Date.now() - t0 < 30000;) {
          state = await row().getAttribute('data-state').catch(() => null)
          if (state && state !== 'loading') break
          await page.waitForTimeout(500)
        }
        log('ROW STATE', state)
        // Terminal for this driver: the request's own end states, or the row's status read refused ('unavailable').
        if (['READY', 'NEEDS_CORRECTION', 'FAILED', 'ATTENTION', 'unavailable'].includes(state)) break
      }
      packet.final_state = state
      if (state === 'READY') {
        mark('ready_seen')
        await page.locator(`[data-row="owned-analysis-request"][data-request-id="${ids.request_id}"] button`).first().click()
        await page.locator('[data-row="native-section"]').first().waitFor({ state: 'visible', timeout: 90000 }).catch(() => {})
        mark('sections_shown')
        packet.section_cards = await page.locator('[data-row="native-section"]').count()
        await shot(page, 'report-open')
        outcome = 'READY'
      } else outcome = state ? `ENDED_${state}` : 'READY_CEILING'
    }
  }
} catch (e) {
  outcome = `ERROR: ${String(e.message).slice(0, 200)}`
  log('ERROR', e.message)
} finally {
  if (context) await context.close().catch((e) => log('HAR close failed', e.message))
  if (browser) await browser.close().catch(() => {})
  if (armed) {
    try { log(py('disarm', {}, holder).trim()) } catch (e) { log('DISARM FAILED -- run: python .claude/skills/ui-walk/ui_walker_account.py disarm', holder, e.message) }
  }
  Object.assign(packet, { outcome, ids, posts, marks, guard_aborts: guard.length, finished_at: new Date().toISOString() })
  writeFileSync(path.join(OUT, 'packet.json'), JSON.stringify(packet, null, 1))
  writeFileSync(path.join(OUT, 'guard.tsv'), guard.join('\n'))
  log('OUTCOME', outcome, '| posts', JSON.stringify(posts), '| guard aborts', guard.length)
  log('OUT', OUT)
}
