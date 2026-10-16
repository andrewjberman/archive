// IRPT_ANLREQ FWD-1 page driver (0.9.0_WK_IRPT_ANLREQ~149, AR-y-345). Derived from .claude/skills/ui-walk/walk.mjs:
// playwright-core from the portal's node_modules (walk.mjs:24-25), Microsoft Edge with a bundled-Chromium fallback
// (walk.mjs:1603-1605), the real sign-in form (walk.mjs:1645-1659), and a route guard. The walker itself is NOT edited
// and is read-only by construction; this is a separate script with its own allow-list.
//
//   node fwd1_driver.mjs --plan
//   node fwd1_driver.mjs --selftest                       (offline: no browser, no network, no AWS, no boto3)
//   node fwd1_driver.mjs --base http://localhost:5174 --firm <firm-id> --holdings <csv> --out <dir>
//                        [--poll-minutes 20] [--advisor-email <synthetic address at opal.invalid>] --go IRPT_ANLREQ.TO-RUN-FWD1.<id>
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
const EMAIL = 'fwd1-staff-r41b@opal.invalid'
const FIRM_CHOICE_LABEL = 'Choose the firm this request is filed under'
const TITLE = 'SYNTHETIC IRPT_ANLREQ FWD-1 run r41b, do not action'
const NEW_TICKET_LABEL = 'New Ticket'
const SUBMIT_LABEL = 'File Analysis Request'
const TABS = ['Open', 'In Progress', 'Completed']
// AR-y-366 (round 41, ZZ27): the Ticket Center prompt words the --decisions option presses or reads. Each is the candidate form's
// own text (portal 0ba0cb13: AnalysisRequestParts.tsx and analysisRequest.ts); labels_check.py reads these lines and checks each.
const PROMPT_YES = 'Yes'
const PROMPT_REPLACE = 'Replace'
const PROMPT_NO = 'No'
const PROMPT_CHECK = 'Check'
const REPLACE_INPUT_PREFIX = 'Replacement ticker for '
const FILED_AS_GIVEN_HEADING = 'These holdings were filed as given.'
const DID_YOU_MEAN_PREFIX = 'Did you mean '
const NOT_FOUND_SUFFIX = ' was not found.'
const NO_CHOICE_LINE = 'Opal Staff will manage the replacement.'
const DECISIONS_MAX = 20
const PROMPT_ROUNDS = 6
const PROMPT_SETTLE_MS = 20000
// AR-y-367 (round 41, ZZ28): the ticket-answer bound. 240 s as signed; with --decisions, 90 s more per allowed prompt round.
const TICKET_WAIT_MS = 240000
const ROUND_WAIT_MS = 90000
const PROMPT_POLL_MS = 1000
const TICKER_SHAPE = /^[A-Z0-9.-]{1,12}$/
const DECISION_KEYS = ['symbol', 'answer', 'replacement', 'fallback']
const DECISION_ANSWERS = ['yes', 'replace', 'no']
// AR-y-372 (round 43, ZZ33): the stated fall-through. A yes may carry fallback "no" (taken when its Yes button is not offered);
// the file may carry on_unplanned "no" (a prompt for a symbol no decision names takes No). Nothing else is admitted.
const TOP_KEYS = ['decisions', 'on_unplanned']
const FALLBACK_NO = 'no'
const ON_UNPLANNED_NO = 'no'
// AR-y-372: the reading-only diagnostics (a PNG and a page-text record after each press round and each 60 s of silence while no
// prompt is visible): at most DIAG_SHOTS_MAX files per run, the page text at most PAGE_TEXT_MAX characters, through redact.
const DIAG_SHOTS_MAX = 16
const WAIT_SHOT_MS = 60000
const PAGE_TEXT_MAX = 600
// AR-y-374 (round 43, ZZ35): the form's own still-checking sentence (portal fcbf2bce, analysisRequest.ts STILL_CHECKING_MESSAGE). When it is
// shown and no prompt is, the driver waits RESUBMIT_WAIT_MS and clicks the same Submit button again, at most RESUBMIT_MAX times.
const STILL_CHECKING_TEXT = 'The file is still being checked after several tries; nothing was filed, and you can submit it again later.'
const RESUBMIT_WAIT_MS = 60000
const RESUBMIT_MAX = 4
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
  // AR-y-352 (round 40, ZZ13): the Ticket Center's firm chooser reads the Global firms by this read-shaped POST (writes nothing).
  /^\/api\/scoped\/investor-reporting\/directory\/resolve$/,
]
const STEPS = [
  'STEP-1 generate the password in memory (crypto.randomBytes 24, base64url); never written anywhere',
  'STEP-2 python fwd1_mint.py mint, the password on STDIN only (one users row, attribute_not_exists(PK))',
  'STEP-3 launch the browser behind the route guard; sign in through the real form (#email, #password, button[type=submit])',
  'STEP-4 /ticket-center: New Ticket, type Analysis Request, the firm, the form, setInputFiles on Holdings file, click File Analysis Request; take the ticket id from the POST /api/scoped/tickets answer',
  'STEP-4B after the Submit click the driver presses only the decision buttons, and fills only the one replacement input, that the decisions file plans, until the ticket answer arrives; after the ticket answer it only reads (no other click, fill or post)',
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

// ---- the route guard: GET, HEAD, OPTIONS on the base origin; exactly eight POST shapes on the base origin (the seven, plus AR-y-352's read-shaped directory resolve) ----------
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
  const o = { base: 'http://localhost:5174', firm: null, holdings: null, out: null, pollMinutes: 20, plan: false, selftest: false, go: null, decisionsPath: null, advisorEmail: null }
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
    else if (a === '--decisions') o.decisionsPath = next() ?? null
    else if (a === '--advisor-email') o.advisorEmail = next() ?? ''
    else return { error: 'unknown argument ' + a }
  }
  return { o }
}

// ---- AR-y-379 (round 43, ZZ40): the advisor login email option. Pure parts first; only a synthetic opal.invalid address is admitted. ----
const ADVISOR_EMAIL_DOMAIN = 'opal.invalid'
const ADVISOR_EMAIL_LOCAL = /^[a-z0-9][a-z0-9._-]*$/
export function validateAdvisorEmail(s) {
  if (typeof s !== 'string') return { error: 'the address must be a string' }
  if (s.length < 6 || s.length > 80) return { error: 'the address must be 6 to 80 characters' }
  if (s !== s.toLowerCase()) return { error: 'the address must be lower-case' }
  const parts = s.split('@')
  if (parts.length !== 2) return { error: 'the address must carry exactly one @' }
  const [local, domain] = parts
  if (domain !== ADVISOR_EMAIL_DOMAIN) return { error: 'only a synthetic @' + ADVISOR_EMAIL_DOMAIN + ' address is admitted' }
  if (!ADVISOR_EMAIL_LOCAL.test(local)) return { error: 'the local part must match ^[a-z0-9][a-z0-9._-]*$' }
  return { ok: true, address: s }
}

// shown: whether the page carries the advisor login field. Shown and given: fill it. Shown and not given: the form asks, the run stops
// before the Submit click. Not shown: nothing is typed, whatever the option says.
export function advisorFillAction(shown, advisorEmail) {
  if (!shown) return { action: 'absent' }
  if (advisorEmail === null || advisorEmail === undefined) {
    return { action: 'needed', why: 'ADVISOR-EMAIL-NEEDED the form asks for the advisor login email and --advisor-email was not given' }
  }
  return { action: 'fill', value: advisorEmail }
}

function printPlan(base, advisorEmail = null) {
  console.log('PLAN IRPT_ANLREQ FWD-1 driver (AR-y-345); base ' + base + '; plan mode launches nothing')
  if (advisorEmail !== null) console.log('PLAN advisor-email option (AR-y-379): ' + advisorEmail + ', typed only where the form shows the field')
  for (const s of STEPS) console.log(s)
}

// ---- AR-y-366 (round 41, ZZ27): the --decisions file and the Ticket Center prompts. Pure parts first. --------------------
// A decision is pressed only before the Submit click and only when its prompt is on the page; a prompt no decision names
// stops the run; nothing is guessed. The labels are the constants above (the candidate form's own words).
export function validateDecisions(doc) {
  if (!doc || typeof doc !== 'object' || Array.isArray(doc)) return { error: 'the file must be a JSON object' }
  for (const k of Object.keys(doc)) if (!TOP_KEYS.includes(k)) return { error: 'unknown key ' + k }
  if (!Array.isArray(doc.decisions)) return { error: 'decisions must be an array' }
  if (Object.prototype.hasOwnProperty.call(doc, 'on_unplanned') && doc.on_unplanned !== ON_UNPLANNED_NO) {
    return { error: 'on_unplanned may only be the value "no"' }
  }
  if (doc.decisions.length > DECISIONS_MAX) return { error: 'at most ' + DECISIONS_MAX + ' decisions' }
  const seen = new Set()
  const out = []
  for (const d of doc.decisions) {
    if (!d || typeof d !== 'object' || Array.isArray(d)) return { error: 'each decision must be an object' }
    for (const k of Object.keys(d)) if (!DECISION_KEYS.includes(k)) return { error: 'unknown key ' + k + ' in a decision' }
    if (typeof d.symbol !== 'string' || d.symbol.length < 1 || d.symbol.length > 40 || d.symbol !== d.symbol.trim()) {
      return { error: 'symbol must be the typed symbol as the form shows it (1 to 40 characters, no outer spaces)' }
    }
    if (seen.has(d.symbol)) return { error: 'more than one decision for symbol ' + d.symbol }
    seen.add(d.symbol)
    if (!DECISION_ANSWERS.includes(d.answer)) return { error: 'answer must be exactly yes, replace or no (symbol ' + d.symbol + ')' }
    if (Object.prototype.hasOwnProperty.call(d, 'fallback')) {
      if (d.answer !== 'yes') return { error: 'fallback is allowed only with answer yes (symbol ' + d.symbol + ')' }
      if (d.fallback !== FALLBACK_NO) return { error: 'fallback may only be the value "no" (symbol ' + d.symbol + ')' }
    }
    if (d.answer === 'replace') {
      if (typeof d.replacement !== 'string' || !TICKER_SHAPE.test(d.replacement)) {
        return { error: 'replace needs a replacement ticker of 1 to 12 upper-case letters, digits, . or - (symbol ' + d.symbol + ')' }
      }
      // AR-y-367: the form refuses a replacement equal to its symbol ("the same symbol ... is not sent"); the run stops here instead.
      if (d.replacement === d.symbol.toUpperCase()) return { error: 'the replacement equals the symbol, which the form refuses (symbol ' + d.symbol + ')' }
    } else if (Object.prototype.hasOwnProperty.call(d, 'replacement')) {
      return { error: 'replacement is allowed only with replace (symbol ' + d.symbol + ')' }
    }
    out.push({ symbol: d.symbol, answer: d.answer, replacement: d.answer === 'replace' ? d.replacement : null,
      fallback: d.answer === 'yes' && d.fallback === FALLBACK_NO ? FALLBACK_NO : null })
  }
  return { ok: true, decisions: out, on_unplanned: doc.on_unplanned === ON_UNPLANNED_NO ? ON_UNPLANNED_NO : null }
}

export function readDecisionsFile(file) {
  let text
  try { text = fs.readFileSync(file, 'utf8') } catch { return { error: 'the decisions file cannot be read' } }
  let doc
  try { doc = JSON.parse(text) } catch { return { error: 'the decisions file is not valid JSON' } }
  return validateDecisions(doc)
}

// The button names a prompt offers: with the door's suggestion Yes / Replace / No; without one Replace / No.
export function buttonNamesFor(promptText) {
  const t = String(promptText).trim()
  if (t.startsWith(DID_YOU_MEAN_PREFIX)) return [PROMPT_YES, PROMPT_REPLACE, PROMPT_NO]
  if (t.endsWith(NOT_FOUND_SUFFIX)) return [PROMPT_REPLACE, PROMPT_NO]
  return null
}

// The typed symbol a prompt line names: "Did you mean X? (row N: SYM)" or "(SYM)", and "SYM was not found.".
export function promptSymbol(promptText) {
  const t = String(promptText).trim()
  if (t.startsWith(DID_YOU_MEAN_PREFIX)) {
    const m = t.match(/\((?:row \d+: )?([^()]+)\)$/)
    return m ? m[1] : null
  }
  if (t.endsWith(NOT_FOUND_SUFFIX)) {
    const s = t.slice(0, t.length - NOT_FOUND_SUFFIX.length)
    return s.length > 0 ? s : null
  }
  return null
}

// The one press a decision plans for one prompt. ok:false names the symbol and the reason; the caller stops the run.
// AR-y-372: fell_through is "yes->no" (a planned yes with no Yes button takes its stated fallback No), "unplanned->no" (a symbol
// no decision names takes No under on_unplanned "no"), or null (the press is the one planned). A planned no or replace is unchanged.
export function planPrompt(promptText, decisions, onUnplanned = null) {
  const symbol = promptSymbol(promptText)
  const buttons = buttonNamesFor(promptText)
  if (symbol === null || buttons === null) return { ok: false, symbol: null, why: 'the line is not a prompt the driver knows' }
  const d = decisions.find((x) => x.symbol === symbol)
  if (!d) {
    if (onUnplanned === ON_UNPLANNED_NO && buttons.includes(PROMPT_NO)) {
      return { ok: true, symbol, button: PROMPT_NO, replacement: null, buttons, fell_through: 'unplanned->no' }
    }
    return { ok: false, symbol, why: 'no decision names ' + symbol }
  }
  const button = d.answer === 'yes' ? PROMPT_YES : d.answer === 'replace' ? PROMPT_REPLACE : PROMPT_NO
  if (!buttons.includes(button)) {
    if (d.answer === 'yes' && d.fallback === FALLBACK_NO && buttons.includes(PROMPT_NO)) {
      return { ok: true, symbol, button: PROMPT_NO, replacement: null, buttons, fell_through: 'yes->no' }
    }
    return { ok: false, symbol, why: 'the form offers no ' + button + ' for ' + symbol }
  }
  return { ok: true, symbol, button, replacement: d.answer === 'replace' ? d.replacement : null, buttons, fell_through: null }
}

// AR-y-372: the page text a diagnostic records: whitespace collapsed, redacted, at most PAGE_TEXT_MAX characters.
export function pageTextFrom(raw, secrets = []) {
  return redact(String(raw).replace(/\s+/g, ' ').trim(), secrets).slice(0, PAGE_TEXT_MAX)
}

// AR-y-367 (round 41, ZZ28): the decisions run AFTER the Submit click. The Ticket Center's prompts come only from the upload
// answer that the Submit click triggers, and each press re-posts that upload (a NORMALIZED answer files the ticket). So the
// driver presses only the decision buttons the decisions file plans, and fills only the one replacement input, until the ticket
// answer arrives; after the ticket answer it only reads. The ticket listener is set before the Submit click (run()).
// The bound is ticketWaitMs(true): 240 s plus 90 s per allowed round. At most PROMPT_ROUNDS rounds; an unplanned prompt stops
// the run; nothing is guessed. Every press and fill is recorded in report.form_decisions.
export function ticketWaitMs(withDecisions) {
  return withDecisions ? TICKET_WAIT_MS + ROUND_WAIT_MS * PROMPT_ROUNDS : TICKET_WAIT_MS
}

// AR-y-374: the pure rule for the still-checking sentence. The sentence is matched after whitespace is collapsed. A prompt always wins
// (wait), an answered run only reads (wait); the sentence alone re-clicks while resubmits is below RESUBMIT_MAX, and stops at it.
export function stillCheckingAction({ pageText, promptsVisible, answered, resubmits }) {
  const shown = String(pageText ?? '').replace(/\s+/g, ' ').includes(STILL_CHECKING_TEXT)
  if (!shown) return { action: 'wait' }
  if (Number(promptsVisible) > 0) return { action: 'wait' }
  if (answered) return { action: 'wait' }
  if (Number(resubmits) >= RESUBMIT_MAX) return { action: 'stop', why: 'STILL-CHECKING after ' + RESUBMIT_MAX + ' resubmits; the run stops, nothing is guessed' }
  return { action: 'resubmit' }
}

export async function answerAfterSubmit(page, decisions, answered, report, log, opts = {}) {
  const pollMs = opts.pollMs ?? PROMPT_POLL_MS
  const afterPressMs = opts.afterPressMs ?? 1000
  const deadline = Date.now() + (opts.waitMs ?? ticketWaitMs(true))
  const pressed = new Set()
  const done = (outcome) => ({ outcome, pressed: Array.from(pressed) })
  const hints = () => page.locator('[data-slot="analysis-filing-hint"]')
  const isUploadAnswer = (r) => r.request().method() === 'POST' && /\/analysis\/inputs$/.test(pathOf(r.url()))
  const visible = async () => {
    const texts = []
    const n = await hints().count()
    for (let i = 0; i < n; i++) texts.push(((await hints().nth(i).locator('p').first().textContent()) || '').trim())
    return texts.filter((t) => t !== NO_CHOICE_LINE)
  }
  // AR-y-372 (reading only): a PNG and one report.form_waits entry per diagnostic. Off without opts.outDir (run() passes it with
  // --decisions only); at most DIAG_SHOTS_MAX files; the page text is the filing area's visible text, redacted, bounded.
  const onUnplanned = opts.onUnplanned ?? null
  const waitShotMs = opts.waitShotMs ?? WAIT_SHOT_MS
  const secrets = opts.secrets ?? []
  const diagOn = Boolean(opts.outDir)
  let diagN = 0
  if (diagOn && !Array.isArray(report.form_waits)) report.form_waits = []
  const pageTextOf = async () => {
    try {
      let area = page.locator('xpath=//*[@data-slot="analysis-filing-hint"]/ancestor::*[.//button[normalize-space(.)="' + SUBMIT_LABEL + '"]][1]')
      if ((await area.count()) === 0) area = page.locator('main')
      return pageTextFrom(await area.first().innerText(), secrets)
    } catch { return '(unreadable)' }
  }
  const diagShot = async (kind, stem, prompts) => {
    if (!diagOn || diagN >= DIAG_SHOTS_MAX) return
    diagN += 1
    const name = stem + '-' + String(diagN).padStart(2, '0') + '.png'
    await page.screenshot({ path: path.join(opts.outDir, name), fullPage: true }).catch(() => {})
    const entry = { utc: iso(), kind, shot: name, prompts_visible: prompts.map((t) => redact(t, secrets)), page_text: await pageTextOf() }
    if (kind === 'wait') entry.last_upload = opts.lastUpload ? opts.lastUpload() : null
    report.form_waits.push(entry)
  }
  // AR-y-374: the re-click state. resubmitN counts the clicks made; stillSince is when the sentence was first seen (or null); the
  // records go to report.form_resubmits (only with an outDir, the --decisions path). A shot here takes one of the DIAG_SHOTS_MAX files.
  const resubmitWaitMs = opts.resubmitWaitMs ?? RESUBMIT_WAIT_MS
  let resubmitN = 0
  let stillSince = null
  if (diagOn && !Array.isArray(report.form_resubmits)) report.form_resubmits = []
  // The whole filing area's visible text, for the sentence test only: NOT cut to PAGE_TEXT_MAX (the sentence may lie past the cut).
  const filingFullText = async () => {
    try {
      let area = page.locator('xpath=//*[@data-slot="analysis-filing-hint"]/ancestor::*[.//button[normalize-space(.)="' + SUBMIT_LABEL + '"]][1]')
      if ((await area.count()) === 0) area = page.locator('main')
      return String(await area.first().innerText())
    } catch { return '' }
  }
  const reserveShot = async (stem) => {
    diagN += 1
    const name = stem + '-' + String(diagN).padStart(2, '0') + '.png'
    await page.screenshot({ path: path.join(opts.outDir, name), fullPage: true }).catch(() => {})
    return name
  }
  let nextWaitAt = Date.now() + waitShotMs
  for (let round = 1; round <= PROMPT_ROUNDS; round++) {
    let open = []
    for (;;) {
      if (answered()) { log('FORM-DECISIONS round ' + round + ': the ticket answer arrived; the driver only reads from here'); return done('answered') }
      open = await visible()
      if (open.length > 0) { nextWaitAt = Date.now() + waitShotMs; break }
      if (Date.now() >= deadline) throw new Error('NO-ANSWER neither the ticket answer nor a prompt within the wait bound (round ' + round + ')')
      if (Date.now() >= nextWaitAt) { nextWaitAt = Date.now() + waitShotMs; await diagShot('wait', 'wait', []) }
      if (diagOn) {
        // AR-y-374: the sentence shown, no prompt, not answered: after RESUBMIT_WAIT_MS since it was first seen (or since the last
        // click) one more click of the SAME Submit button, shot first. The click is the only new action; the file input is not touched.
        const act = stillCheckingAction({ pageText: await filingFullText(), promptsVisible: open.length, answered: answered(), resubmits: resubmitN })
        if (act.action === 'stop') throw new Error(act.why)
        if (act.action === 'wait') stillSince = null
        else {
          if (stillSince === null) stillSince = Date.now()
          if (Date.now() - stillSince >= resubmitWaitMs) {
            if (diagN >= DIAG_SHOTS_MAX) throw new Error('RESUBMIT-BUDGET the ' + DIAG_SHOTS_MAX + '-file screenshot bound is spent before resubmit ' + (resubmitN + 1) + '; the run stops, nothing is guessed')
            const shot = await reserveShot('resubmit-' + (resubmitN + 1))
            if (answered()) continue
            resubmitN += 1
            await page.getByRole('button', { name: SUBMIT_LABEL, exact: true }).click()
            stillSince = null
            await sleep(afterPressMs)
            report.form_resubmits.push({ utc: iso(), n: resubmitN, shot, after_text: await pageTextOf() })
            log('FORM-RESUBMIT ' + resubmitN + ' of ' + RESUBMIT_MAX + ': the still-checking sentence was shown with no prompt; the same Submit button was clicked again (shot ' + shot + ')')
          }
        }
      }
      await sleep(pollMs)
    }
    for (const text of open) {
      if (answered()) break
      const plan = planPrompt(text, decisions, onUnplanned)
      if (!plan.ok) throw new Error('UNPLANNED-PROMPT ' + plan.why + ' (round ' + round + '); the run stops, nothing is guessed')
      if ((await hints().filter({ hasText: text }).count()) === 0) continue
      const item = hints().filter({ hasText: text }).first()
      const uploadAnswer = page.waitForResponse(isUploadAnswer, { timeout: PROMPT_SETTLE_MS }).catch(() => null)
      if (plan.button === PROMPT_REPLACE) {
        // a Replace press opens the replacement input; a repeated round finds it open and presses only Check
        if ((await item.getByRole('button', { name: PROMPT_REPLACE, exact: true }).count()) > 0) {
          await item.getByRole('button', { name: PROMPT_REPLACE, exact: true }).click()
        }
        await item.getByLabel(REPLACE_INPUT_PREFIX + plan.symbol, { exact: true }).fill(plan.replacement)
        await item.getByRole('button', { name: PROMPT_CHECK, exact: true }).click()
      } else {
        await item.getByRole('button', { name: plan.button, exact: true }).click()
      }
      pressed.add(plan.symbol)
      const got = await uploadAnswer
      await sleep(afterPressMs)
      const still = (await hints().filter({ hasText: text }).count()) > 0
      const after = still ? ((await hints().filter({ hasText: text }).first().locator('p').first().textContent()) || '').trim() : 'the prompt is no longer shown'
      report.form_decisions.push({ round, symbol: plan.symbol, button: plan.button, replacement: plan.replacement,
        prompt_before: text, line_after: after, upload_answer_status: got ? got.status() : null, fell_through: plan.fell_through, utc: iso() })
      log('FORM-DECISIONS round ' + round + ' pressed ' + plan.button + ' for ' + plan.symbol + ' upload_answer=' + (got ? got.status() : 'none')
        + (plan.fell_through ? ' fell_through=' + plan.fell_through : ''))
    }
    await diagShot('press-round', 'form-r' + round, await visible())
  }
  if (answered()) return done('answered')
  if ((await visible()).length > 0) throw new Error('PROMPTS-REMAIN after ' + PROMPT_ROUNDS + ' rounds; the run stops with the ticket not yet answered')
  return done('bound-reached')
}

// Reading only, after the filed outcome is visible: the notice heading and its lines (the not-covered holdings).
export async function readFormNotice(page, report, log) {
  const box = page.locator('[data-slot="analysis-filing-notice"]')
  await box.first().waitFor({ state: 'visible', timeout: 20000 }).catch(() => {})
  if ((await box.count()) === 0) { report.form_notice = null; log('FORM-NOTICE none shown'); return }
  const heading = ((await box.first().locator('p').first().textContent()) || '').trim()
  const lines = (await box.first().locator('li').allTextContents()).map((s) => s.trim())
  report.form_notice = { heading, heading_matches: heading === FILED_AS_GIVEN_HEADING, lines, utc: iso() }
  log('FORM-NOTICE shown, ' + lines.length + ' line(s)')
}

// ---- the run (never reached without --go, a localhost base and a valid order token) --------------------------------
async function run(o) {
  // AR-y-366: a bad --decisions file refuses the run here, before any directory, mint or browser.
  if (o.decisionsPath) {
    const loaded = readDecisionsFile(o.decisionsPath)
    if (!loaded.ok) { console.log('RUN-REFUSED decisions: ' + loaded.error); return 2 }
    o.decisions = loaded.decisions
    o.onUnplanned = loaded.on_unplanned
  }
  const secrets = []
  const steps = []
  const shots = []
  let shotN = 0
  const report = { schema: 'fwd1_run_report/1', base: o.base, firm: o.firm, started_utc: iso(), order: o.go, steps,
    polls: [], guard_refused: [], absent: [], screenshots: shots, ticket_id: null, errors: [], remove_rc: null }
  if (o.decisions) { report.form_decisions = []; report.form_notice = null; report.form_waits = [] }
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
    // AR-y-379 (round 43, ZZ40): the advisor login field is shown only to a staff filer whose profile lists the firm (portal AR-y-378). Shown and
    // given: one fill, before the Submit click. Shown and not given: the run stops here. Not shown: nothing is typed.
    const advisorField = page.locator('input[aria-label="Advisor login email"]')
    const advisorAct = advisorFillAction((await advisorField.count()) > 0, o.advisorEmail)
    if (advisorAct.action === 'needed') throw new Error(advisorAct.why)
    if (advisorAct.action === 'fill') {
      await advisorField.fill(advisorAct.value)
      log('STEP-4 the advisor login field took the synthetic advisor address ' + advisorAct.value)
    }
    report.advisor_email_field = advisorAct.action === 'fill' ? 'filled' : 'absent'
    const submit = page.getByRole('button', { name: SUBMIT_LABEL, exact: true })
    await submit.waitFor({ state: 'visible', timeout: 30000 })
    for (let i = 0; i < 30 && !(await submit.isEnabled()); i++) await sleep(1000)
    if (!(await submit.isEnabled())) throw new Error('the Submit control stayed disabled (a held reason)')
    await shot(page, 'before-submit')

    // AR-y-372: a passive listener (it sends nothing and reads no body) keeps the status and path of the last upload answer for the diagnostics.
    let lastUpload = null
    if (o.decisions) page.on('response', (r) => { if (r.request().method() === 'POST' && /\/analysis\/inputs$/.test(pathOf(r.url()))) lastUpload = { status: r.status(), path: pathOf(r.url()) } })
    // AR-y-367: the ticket-answer listener is set BEFORE the Submit click; its bound is 240 s, or ticketWaitMs(true) with --decisions.
    let ticketDone = false
    const ticketAnswer = page.waitForResponse((r) => r.request().method() === 'POST' && pathOf(r.url()) === '/api/scoped/tickets', { timeout: ticketWaitMs(Boolean(o.decisions)) })
    ticketAnswer.then(() => { ticketDone = true }, () => { ticketDone = true })
    await submit.click()
    log('STEP-4 Submit clicked; ' + (o.decisions ? 'the planned decisions are answered until the ticket answer, then the driver only reads' : 'from here the driver only reads'))
    if (o.decisions) {
      const loop = await answerAfterSubmit(page, o.decisions, () => ticketDone, report, log,
        { secrets, outDir: o.out, onUnplanned: o.onUnplanned, lastUpload: () => lastUpload })
      report.form_decisions_unused = o.decisions.map((d) => d.symbol).filter((s) => !loop.pressed.includes(s))
      log('FORM-DECISIONS ' + loop.outcome + '; symbols pressed: ' + loop.pressed.length + ' of ' + o.decisions.length + ' planned')
    }
    const resp = await ticketAnswer
    let body = null
    try { body = await resp.json() } catch { body = null }
    report.ticket_id = findTicketId(body)
    if (!report.ticket_id) throw new Error('no ticket_id in the POST /api/scoped/tickets answer (status ' + resp.status() + ')')
    log('STEP-4 ticket ' + report.ticket_id + ' filed (POST /api/scoped/tickets status ' + resp.status() + ')')
    if (o.decisions) await readFormNotice(page, report, log)

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

async function selftest() {
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
  // AR-y-352: the read-shaped directory resolve is admitted; its near-misses, the parent and a sibling are refused; the guard reads the path only
  check('admit POST /api/scoped/investor-reporting/directory/resolve', admit('POST', B + '/api/scoped/investor-reporting/directory/resolve', B))
  check('admit POST directory/resolve with a query suffix (the guard reads the path, as for the seven)', admit('POST', B + '/api/scoped/investor-reporting/directory/resolve?selected_tenant=global', B))
  check('refuse POST directory/resolve/x', !admit('POST', B + '/api/scoped/investor-reporting/directory/resolve/x', B))
  check('refuse POST directory/resolved', !admit('POST', B + '/api/scoped/investor-reporting/directory/resolved', B))
  check('refuse POST directory (the parent)', !admit('POST', B + '/api/scoped/investor-reporting/directory', B))
  check('refuse POST directory/resolve/ (trailing slash)', !admit('POST', B + '/api/scoped/investor-reporting/directory/resolve/', B))
  check('refuse POST directory/browse (a sibling read is not a POST shape)', !admit('POST', B + '/api/scoped/investor-reporting/directory/browse', B))
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
  // AR-y-359 (round 41b): the run address is the one constant the mint helper also holds (one address, both files); a driver
  // carrying a different address (the retired producer address among them) fails here. An unreadable mint file fails the case.
  const mintSrc = (() => { try { return fs.readFileSync(MINT, 'utf8') } catch (e) { return '' } })()
  const mintEmail = (mintSrc.match(/^EMAIL = "([^"]+)"/m) || [])[1]
  check('the run address equals the mint helper address (one address in both files)', mintEmail !== undefined && EMAIL === mintEmail)
  // AR-y-366 (round 41, ZZ27): the --decisions file, the prompt buttons, the unplanned stop, the round bound and the labels. Offline.
  const okDoc = { decisions: [{ symbol: 'ABCD', answer: 'yes' }, { symbol: 'EFGH', answer: 'replace', replacement: 'SPY' }, { symbol: 'IJKL', answer: 'no' }] }
  const vOk = validateDecisions(okDoc)
  check('decisions: a valid file of three answers is admitted', vOk.ok === true && vOk.decisions.length === 3)
  check('decisions: an answer outside yes / replace / no is refused', validateDecisions({ decisions: [{ symbol: 'ABCD', answer: 'maybe' }] }).error !== undefined)
  check('decisions: replace without a replacement is refused', validateDecisions({ decisions: [{ symbol: 'EFGH', answer: 'replace' }] }).error !== undefined)
  check('decisions: a replacement on yes is refused', validateDecisions({ decisions: [{ symbol: 'ABCD', answer: 'yes', replacement: 'SPY' }] }).error !== undefined)
  check('decisions: a lower-case replacement is refused', validateDecisions({ decisions: [{ symbol: 'EFGH', answer: 'replace', replacement: 'spy' }] }).error !== undefined)
  check('decisions: a 13-character replacement is refused', validateDecisions({ decisions: [{ symbol: 'EFGH', answer: 'replace', replacement: 'ABCDEFGHIJKLM' }] }).error !== undefined)
  check('decisions: more than 20 decisions are refused', validateDecisions({ decisions: Array.from({ length: 21 }, (_, i) => ({ symbol: 'S' + i, answer: 'no' })) }).error !== undefined)
  check('decisions: two decisions for one symbol are refused', validateDecisions({ decisions: [{ symbol: 'ABCD', answer: 'yes' }, { symbol: 'ABCD', answer: 'no' }] }).error !== undefined)
  check('decisions: an unknown key inside a decision is refused', validateDecisions({ decisions: [{ symbol: 'ABCD', answer: 'no', note: 'x' }] }).error !== undefined)
  check('decisions: an unknown top-level key is refused', validateDecisions({ decisions: [], extra: 1 }).error !== undefined)
  check('decisions: a file that is not an object with a decisions array is refused', validateDecisions([]).error !== undefined && validateDecisions({}).error !== undefined)
  check('decisions: a missing file is refused by the reader', readDecisionsFile(path.join(os.tmpdir(), 'no-such-fwd1-decisions-ar366.json')).error !== undefined)
  check('decisions: a prompt with a suggestion offers Yes, Replace, No', JSON.stringify(buttonNamesFor('Did you mean ABC? (row 3: ABCX)')) === JSON.stringify(['Yes', 'Replace', 'No']))
  check('decisions: a prompt without a suggestion offers Replace, No', JSON.stringify(buttonNamesFor('ABCX was not found.')) === JSON.stringify(['Replace', 'No']))
  check('decisions: a prompt for a symbol no decision names stops the plan (unplanned)', (() => { const p = planPrompt('Did you mean ABC? (row 3: ZZZZ)', vOk.decisions); return p.ok === false && p.symbol === 'ZZZZ' })())
  check('decisions: yes for a prompt without a suggestion is not offered (stop)', (() => { const p = planPrompt('MNOP was not found.', [{ symbol: 'MNOP', answer: 'yes', replacement: null }]); return p.ok === false })())
  check('decisions: a planned replace names the Replace button and its replacement', (() => { const p = planPrompt('EFGH was not found.', vOk.decisions); return p.ok === true && p.button === 'Replace' && p.replacement === 'SPY' })())
  check('decisions: the round bound is six', PROMPT_ROUNDS === 6)
  check('decisions: the prompt labels equal the form words named in the cell', PROMPT_YES === 'Yes' && PROMPT_REPLACE === 'Replace' && PROMPT_NO === 'No' && PROMPT_CHECK === 'Check' && REPLACE_INPUT_PREFIX === 'Replacement ticker for ' && FILED_AS_GIVEN_HEADING === 'These holdings were filed as given.')
  check('decisions: --decisions is read by the argument parser', parseArgs(['--decisions', 'd.json']).o.decisionsPath === 'd.json')
  const badDec = path.join(os.tmpdir(), 'fwd1_bad_decisions_ar366_' + process.pid + '.json')
  fs.writeFileSync(badDec, JSON.stringify({ decisions: [{ symbol: 'ABCD', answer: 'maybe' }] }))
  const badRun = spawnSync(process.execPath, [SELF, '--base', B, '--firm', '49financial', '--holdings', SELF, '--out', os.tmpdir(), '--go', 'IRPT_ANLREQ.TO-RUN-FWD1.x', '--decisions', badDec], { encoding: 'utf8', timeout: 60000 })
  fs.rmSync(badDec, { force: true })
  check('a bad decisions file refuses the run with rc 2 before any step', badRun.status === 2 && /RUN-REFUSED decisions/.test(badRun.stdout) && !/STEP-1 password generated/.test(badRun.stdout))
  // AR-y-367 (round 41, ZZ28): the after-Submit loop. Source checks read this file's own lines by line-start anchors; the loop runs
  // against a fake page (offline) that shows prompts, records presses and fills, and removes a prompt on its resolving press.
  check('decisions: a replacement equal to its own symbol is refused (the form refuses it)', validateDecisions({ decisions: [{ symbol: 'EFGH', answer: 'replace', replacement: 'EFGH' }] }).error !== undefined)
  check('decisions: the ticket bound is 240 s without --decisions and 240 s plus 90 s per round with them (780 s at six rounds)',
    ticketWaitMs(false) === 240000 && ticketWaitMs(true) === 240000 + 90000 * PROMPT_ROUNDS && ticketWaitMs(true) === 780000)
  const SRC_LINES = fs.readFileSync(SELF, 'utf8').split('\n')
  const iListen = SRC_LINES.findIndex((l) => /^    const ticketAnswer = page\.waitForResponse\(/.test(l))
  const iSubmit = SRC_LINES.findIndex((l) => /^    await submit\.click\(\)$/.test(l))
  const callIdx = SRC_LINES.map((l, i) => (/^      const loop = await answerAfterSubmit\(page, /.test(l) ? i : -1)).filter((i) => i >= 0)
  const awaitCalls = SRC_LINES.filter((l) => /^ {6}(const \w+ = )?await answerAfterSubmit\(/.test(l)).length
  check('the ticket-answer listener is created before the Submit click in source order', iListen > 0 && iSubmit > iListen)
  check('the decisions loop is called after the Submit click in source order', callIdx.length === 1 && callIdx[0] > iSubmit)
  check('without --decisions no press path is reachable: the one loop call sits behind if (o.decisions) and is the only await call',
    callIdx.length === 1 && SRC_LINES[callIdx[0] - 1] === '    if (o.decisions) {' && awaitCalls === 1)
  // AR-y-374: filing (optional) is { text(), onSubmit() }: the filing area's text, and a hook run on each Submit click; absent, the text is the AR-y-372 fake.
  const fakeFormPage = (hints, presses, shots = { n: 0 }, filing = null) => {
    const remove = (h) => { hints.splice(hints.indexOf(h), 1) }
    const itemOf = (h) => ({
      locator: () => ({ first: () => ({ textContent: async () => h.text }) }),
      getByRole: (role, o) => ({
        count: async () => (o.name === PROMPT_REPLACE && h.open ? 0 : 1),
        click: async () => {
          presses.push(o.name + ' ' + h.text)
          if (o.name === PROMPT_REPLACE) h.open = true
          else if (o.name === PROMPT_CHECK) { h.open = false; if (h.resolveOn === PROMPT_CHECK) remove(h) }
          else if (o.name === h.resolveOn) remove(h)
        },
      }),
      getByLabel: (label) => ({ fill: async (v) => { presses.push('fill ' + label + '=' + v) } }),
    })
    const view = (list) => ({
      count: async () => list().length,
      nth: (i) => itemOf(list()[i]),
      filter: (f) => view(() => list().filter((h) => h.text.includes(f.hasText))),
      first: () => itemOf(list()[0]),
    })
    const page = {
      locator: (sel) => (String(sel).startsWith('xpath=') ? { count: async () => 1, first: () => ({ innerText: async () => (filing ? filing.text() : 'FAKE FILING AREA') }) } : view(() => hints)),
      waitForResponse: () => Promise.resolve({ status: () => 200 }),
      getByRole: (role, o) => ({ click: async () => { presses.push('submit ' + o.name); if (filing) filing.onSubmit() } }),
      screenshot: async () => { shots.n += 1 },
    }
    return page
  }
  const quick = { waitMs: 2000, pollMs: 1, afterPressMs: 0, outDir: os.tmpdir() }
  const pr1 = []
  const r1 = await answerAfterSubmit(fakeFormPage([{ text: 'ZZZZ was not found.', buttons: ['Replace', 'No'], resolveOn: 'No', open: false }], pr1),
    [{ symbol: 'ABCD', answer: 'no', replacement: null }], () => false, { form_decisions: [] }, () => {}, quick).then(() => null, (e) => e.message)
  check('an unplanned prompt stops the loop, names its symbol, and presses nothing', typeof r1 === 'string' && r1.includes('UNPLANNED-PROMPT') && r1.includes('ZZZZ') && pr1.length === 0)
  const pr2 = []
  const r2 = await answerAfterSubmit(fakeFormPage([{ text: 'EFGH was not found.', buttons: ['Replace', 'No'], resolveOn: null, open: false }], pr2),
    [{ symbol: 'EFGH', answer: 'no', replacement: null }], () => false, { form_decisions: [] }, () => {}, quick).then(() => null, (e) => e.message)
  check('the loop presses at most six rounds, then stops with PROMPTS-REMAIN', pr2.length === 6 && typeof r2 === 'string' && /PROMPTS-REMAIN after 6 rounds/.test(r2))
  const pr3 = []
  const r3 = await answerAfterSubmit(fakeFormPage([{ text: 'EFGH was not found.', buttons: ['Replace', 'No'], resolveOn: 'No', open: false }], pr3),
    [{ symbol: 'EFGH', answer: 'no', replacement: null }], () => true, { form_decisions: [] }, () => {}, quick)
  check('once the ticket answer has arrived the loop presses nothing and only reads', r3.outcome === 'answered' && r3.pressed.length === 0 && pr3.length === 0)
  const pr4 = []
  const rep4 = { form_decisions: [] }
  const hints4 = [{ text: 'EFGH was not found.', buttons: ['Replace', 'No'], resolveOn: PROMPT_CHECK, open: false }]
  const r4 = await answerAfterSubmit(fakeFormPage(hints4, pr4), [{ symbol: 'EFGH', answer: 'replace', replacement: 'SPY' }],
    () => hints4.length === 0 && pr4.length > 0, rep4, () => {}, quick)
  check('a planned replace presses Replace, fills its replacement input, presses Check, and is recorded',
    JSON.stringify(pr4) === JSON.stringify(['Replace EFGH was not found.', 'fill Replacement ticker for EFGH=SPY', 'Check EFGH was not found.'])
    && rep4.form_decisions.length === 1 && rep4.form_decisions[0].replacement === 'SPY' && r4.outcome === 'answered')
  // AR-y-372 (round 43, ZZ33): the stated fall-through keys, the fall-through presses, and the reading-only diagnostics with their
  // bounds. The file with neither new key keeps its signed shape. The fakes show prompts and count presses; nothing is launched.
  const fbDoc = validateDecisions({ decisions: [{ symbol: 'ABCD', answer: 'yes', fallback: 'no' }] })
  check('decisions: a yes with fallback "no" is admitted and carries it', fbDoc.ok === true && fbDoc.decisions[0].fallback === 'no')
  check('decisions: fallback on a no decision is refused', validateDecisions({ decisions: [{ symbol: 'ABCD', answer: 'no', fallback: 'no' }] }).error !== undefined)
  check('decisions: fallback on a replace decision is refused', validateDecisions({ decisions: [{ symbol: 'EFGH', answer: 'replace', replacement: 'SPY', fallback: 'no' }] }).error !== undefined)
  check('decisions: fallback with any value other than "no" is refused', ['yes', 'NO', 'replace', null, 1].every((v) => validateDecisions({ decisions: [{ symbol: 'ABCD', answer: 'yes', fallback: v }] }).error !== undefined))
  check('decisions: on_unplanned "no" is admitted and carried', (() => { const v = validateDecisions({ decisions: [], on_unplanned: 'no' }); return v.ok === true && v.on_unplanned === 'no' })())
  check('decisions: on_unplanned with any value other than "no" is refused', ['yes', 'replace', 'NO', null, true].every((v) => validateDecisions({ decisions: [], on_unplanned: v }).error !== undefined))
  check('decisions: an unknown top-level key is still refused beside on_unplanned', validateDecisions({ decisions: [], on_unplanned: 'no', extra: 1 }).error !== undefined)
  check('decisions: a file with neither new key keeps the signed shape (on_unplanned null, fallback null)', (() => { const v = validateDecisions(okDoc); return v.ok === true && v.on_unplanned === null && v.decisions[0].fallback === null })())
  const pFb = planPrompt('MNOP was not found.', [{ symbol: 'MNOP', answer: 'yes', replacement: null, fallback: 'no' }])
  check('planPrompt: a planned yes with no Yes button and fallback "no" takes No (fell_through yes->no)', pFb.ok === true && pFb.button === 'No' && pFb.fell_through === 'yes->no')
  check('planPrompt: a planned yes with no Yes button and no fallback is ok:false', planPrompt('MNOP was not found.', [{ symbol: 'MNOP', answer: 'yes', replacement: null, fallback: null }]).ok === false)
  const pYes = planPrompt('Did you mean ABC? (row 3: ABCD)', [{ symbol: 'ABCD', answer: 'yes', replacement: null, fallback: 'no' }])
  check('planPrompt: a planned yes whose Yes button is offered is unchanged (button Yes, fell_through null)', pYes.ok === true && pYes.button === 'Yes' && pYes.fell_through === null)
  const pUn = planPrompt('ZZZZ was not found.', [], 'no')
  check('planPrompt: an unplanned symbol with on_unplanned "no" takes No (fell_through unplanned->no)', pUn.ok === true && pUn.button === 'No' && pUn.fell_through === 'unplanned->no')
  check('planPrompt: an unplanned symbol without on_unplanned is ok:false', planPrompt('ZZZZ was not found.', [], null).ok === false)
  check('planPrompt: a planned no and a planned replace are unchanged by on_unplanned', (() => {
    const n = planPrompt('EFGH was not found.', [{ symbol: 'EFGH', answer: 'no', replacement: null }], 'no')
    const r = planPrompt('EFGH was not found.', [{ symbol: 'EFGH', answer: 'replace', replacement: 'SPY', fallback: null }], 'no')
    return n.button === 'No' && n.fell_through === null && r.button === 'Replace' && r.fell_through === null
  })())
  const pr5 = []
  const rep5 = { form_decisions: [] }
  const hints5 = [{ text: 'MNOP was not found.', buttons: ['Replace', 'No'], resolveOn: 'No', open: false }]
  const r5 = await answerAfterSubmit(fakeFormPage(hints5, pr5), [{ symbol: 'MNOP', answer: 'yes', replacement: null, fallback: 'no' }],
    () => hints5.length === 0 && pr5.length > 0, rep5, () => {}, quick).catch((e) => ({ outcome: 'threw: ' + e.message, pressed: [] }))
  check('the loop presses the fall-through No, records fell_through yes->no, and reads on to the answer', r5.outcome === 'answered' && JSON.stringify(pr5) === JSON.stringify(['No MNOP was not found.']) && rep5.form_decisions[0].fell_through === 'yes->no')
  const pr6 = []
  const rep6 = { form_decisions: [] }
  const hints6 = [{ text: 'QQQQ was not found.', buttons: ['Replace', 'No'], resolveOn: 'No', open: false }]
  const r6 = await answerAfterSubmit(fakeFormPage(hints6, pr6), [], () => hints6.length === 0 && pr6.length > 0, rep6, () => {}, { ...quick, onUnplanned: 'no' })
    .catch((e) => ({ outcome: 'threw: ' + e.message, pressed: [] }))
  check('the loop presses No for an unplanned symbol under on_unplanned "no" and records unplanned->no', r6.outcome === 'answered' && rep6.form_decisions[0].symbol === 'QQQQ' && rep6.form_decisions[0].fell_through === 'unplanned->no')
  const shotsB = { n: 0 }
  const presB = []
  const repB = { form_decisions: [] }
  const rB = await answerAfterSubmit(fakeFormPage([], presB, shotsB), [], () => false, repB, () => {},
    { waitMs: 1000, pollMs: 1, afterPressMs: 0, waitShotMs: 1, outDir: os.tmpdir(), secrets: [], lastUpload: () => ({ status: 200, path: '/api/scoped/investor-reporting/analysis/inputs' }) })
    .then(() => null, (e) => e.message)
  check('the diagnostic files are bounded at 16 (DIAG_SHOTS_MAX) with no press or fill, and the wait stays NO-ANSWER',
    DIAG_SHOTS_MAX === 16 && shotsB.n === 16 && repB.form_waits.length === 16 && presB.length === 0 && typeof rB === 'string' && /NO-ANSWER/.test(rB))
  check('a wait entry carries the last upload status and path only (no body), and its page text', (() => {
    const w = repB.form_waits.find((e) => e.kind === 'wait')
    return !!w && JSON.stringify(w.last_upload) === JSON.stringify({ status: 200, path: '/api/scoped/investor-reporting/analysis/inputs' }) && w.page_text === 'FAKE FILING AREA'
  })())
  const SECRET_T = 'SAMPLE-SECRET-TEXT-4242'
  const pt = pageTextFrom(SECRET_T + ' token=SAMPLE-TOKEN-99887766 ' + 'y '.repeat(400), [SECRET_T])
  check('page text is redacted and at most 600 characters; whitespace is collapsed', pt.length <= 600 && !pt.includes(SECRET_T) && !pt.includes('SAMPLE-TOKEN-99887766')
    && pageTextFrom('z'.repeat(1000), []).length === 600 && pageTextFrom('a \n\n  b\tc  ', []) === 'a b c')
  const shotsC = { n: 0 }
  const repC = { form_decisions: [] }
  await answerAfterSubmit(fakeFormPage([{ text: 'EFGH was not found.', buttons: ['Replace', 'No'], resolveOn: 'No', open: false }], [], shotsC),
    [{ symbol: 'EFGH', answer: 'no', replacement: null }], () => false, repC, () => {}, { waitMs: 50, pollMs: 1 }).catch(() => null)
  check('without an outDir no diagnostic file or form_waits entry is written (the signed path)', shotsC.n === 0 && repC.form_waits === undefined)
  // AR-y-374 (round 43, ZZ35): the still-checking sentence. The pure rule first; then the loop against the fake page, where the sentence
  // stays shown until the fake Submit clicks change it. resubmitWaitMs is short here; the real bound is RESUBMIT_WAIT_MS (60000).
  const STILL_SENTENCE = 'The file is still being checked after several tries; nothing was filed, and you can submit it again later.'
  const sa = (o) => stillCheckingAction(o).action
  check('still-checking: the sentence absent is wait', sa({ pageText: 'FAKE FILING AREA', promptsVisible: 0, answered: false, resubmits: 0 }) === 'wait')
  check('still-checking: the sentence present with no prompt and 0 resubmits is resubmit', sa({ pageText: STILL_SENTENCE, promptsVisible: 0, answered: false, resubmits: 0 }) === 'resubmit')
  check('still-checking: the sentence present with a prompt visible is wait (a prompt always wins)', sa({ pageText: STILL_SENTENCE, promptsVisible: 1, answered: false, resubmits: 0 }) === 'wait')
  check('still-checking: the sentence present once answered is wait', sa({ pageText: STILL_SENTENCE, promptsVisible: 0, answered: true, resubmits: 0 }) === 'wait')
  check('still-checking: the sentence present at 3 resubmits is resubmit', sa({ pageText: STILL_SENTENCE, promptsVisible: 0, answered: false, resubmits: 3 }) === 'resubmit')
  check('still-checking: the sentence present at 4 resubmits is stop, with the error line', (() => {
    const s = stillCheckingAction({ pageText: STILL_SENTENCE, promptsVisible: 0, answered: false, resubmits: 4 })
    return s.action === 'stop' && s.why === 'STILL-CHECKING after 4 resubmits; the run stops, nothing is guessed'
  })())
  check('still-checking: the constants equal 60000 and 4', RESUBMIT_WAIT_MS === 60000 && RESUBMIT_MAX === 4)
  check('still-checking: STILL_CHECKING_TEXT equals the form sentence exactly', STILL_CHECKING_TEXT === STILL_SENTENCE)
  check('still-checking: a near miss (Nothing with a capital N) is not the sentence: wait', sa({ pageText: STILL_SENTENCE.replace('nothing', 'Nothing'), promptsVisible: 0, answered: false, resubmits: 0 }) === 'wait')
  check('still-checking: the match collapses whitespace in the page text', sa({ pageText: 'Upload\n\n ' + STILL_SENTENCE.replace(' after ', '  after '), promptsVisible: 0, answered: false, resubmits: 0 }) === 'resubmit')
  check('still-checking: an answered run at 4 resubmits reads on (answered wins over stop)', sa({ pageText: STILL_SENTENCE, promptsVisible: 0, answered: true, resubmits: 4 }) === 'wait')
  const stillCfg = { waitMs: 5000, pollMs: 1, afterPressMs: 0, resubmitWaitMs: 1, outDir: os.tmpdir(), waitShotMs: 600000 }
  const fL1 = { clicks: 0, text: () => (fL1.clicks >= 2 ? 'The ticket is filed.' : STILL_SENTENCE), onSubmit: () => { fL1.clicks += 1 } }
  const pL1 = []
  const shotsL1 = { n: 0 }
  const repL1 = { form_decisions: [] }
  const rL1 = await answerAfterSubmit(fakeFormPage([], pL1, shotsL1, fL1), [], () => fL1.clicks >= 2, repL1, () => {}, stillCfg)
    .catch((e) => ({ outcome: 'threw: ' + e.message, pressed: [] }))
  check('still-checking: two re-clicks of the same Submit button, each recorded and shot, then the answer is read',
    rL1.outcome === 'answered' && JSON.stringify(pL1) === JSON.stringify(['submit File Analysis Request', 'submit File Analysis Request'])
    && repL1.form_resubmits.length === 2 && repL1.form_resubmits[1].n === 2 && /^resubmit-1-\d\d\.png$/.test(repL1.form_resubmits[0].shot) && shotsL1.n === 2)
  const fL2 = { clicks: 0, text: () => STILL_SENTENCE, onSubmit: () => { fL2.clicks += 1 } }
  const pL2 = []
  const shotsL2 = { n: 0 }
  const repL2 = { form_decisions: [] }
  const rL2 = await answerAfterSubmit(fakeFormPage([], pL2, shotsL2, fL2), [], () => false, repL2, () => {}, stillCfg).then(() => null, (e) => e.message)
  check('still-checking: after 4 resubmits the sentence stops the run with the error line; no fifth click', rL2 === 'STILL-CHECKING after 4 resubmits; the run stops, nothing is guessed'
    && fL2.clicks === 4 && repL2.form_resubmits.length === 4 && shotsL2.n === 4)
  const hints3 = [{ text: 'EFGH was not found.', buttons: ['Replace', 'No'], resolveOn: 'No', open: false }]
  const fL3 = { clicks: 0, text: () => STILL_SENTENCE, onSubmit: () => { fL3.clicks += 1 } }
  const pL3 = []
  const repL3 = { form_decisions: [] }
  const rL3 = await answerAfterSubmit(fakeFormPage(hints3, pL3, { n: 0 }, fL3), [{ symbol: 'EFGH', answer: 'no', replacement: null }], () => fL3.clicks >= 1, repL3, () => {}, stillCfg)
    .catch((e) => ({ outcome: 'threw: ' + e.message, pressed: [] }))
  check('still-checking: a prompt shown with the sentence is pressed first; the re-click follows only once no prompt is shown',
    rL3.outcome === 'answered' && pL3.length === 2 && pL3[0] === 'No EFGH was not found.' && pL3[1] === 'submit File Analysis Request')
  const fL4 = { clicks: 0, text: () => STILL_SENTENCE, onSubmit: () => { fL4.clicks += 1 } }
  const shotsL4 = { n: 0 }
  const pL4 = []
  const repL4 = { form_decisions: [] }
  const rL4 = await answerAfterSubmit(fakeFormPage([], pL4, shotsL4, fL4), [], () => false, repL4, () => {},
    { waitMs: 10000, pollMs: 1, afterPressMs: 0, resubmitWaitMs: 2000, waitShotMs: 1, outDir: os.tmpdir() }).then(() => null, (e) => e.message)
  check('still-checking: the 16-file bound spent before a resubmit stops the run with RESUBMIT-BUDGET and no click',
    typeof rL4 === 'string' && /RESUBMIT-BUDGET/.test(rL4) && fL4.clicks === 0 && shotsL4.n === 16 && repL4.form_resubmits.length === 0)
  const fL5 = { clicks: 0, text: () => STILL_SENTENCE, onSubmit: () => { fL5.clicks += 1 } }
  const rL5 = await answerAfterSubmit(fakeFormPage([], [], { n: 0 }, fL5), [], () => false, { form_decisions: [] }, () => {}, { waitMs: 60, pollMs: 1 }).then(() => null, (e) => e.message)
  check('still-checking: without an outDir (the signed path) the sentence is not acted on: no click, NO-ANSWER', fL5.clicks === 0 && typeof rL5 === 'string' && /NO-ANSWER/.test(rL5))
  // AR-y-379 (round 43, ZZ40): the advisor login email option and its one fill. Offline: no browser, no mint, no network.
  const ADV_OK = 'irpt-w5-advisor-20261016@opal.invalid'
  check('advisor email: validateAdvisorEmail admits irpt-w5-advisor-20261016@opal.invalid', validateAdvisorEmail(ADV_OK).ok === true && validateAdvisorEmail(ADV_OK).address === ADV_OK)
  check('advisor email: a real-domain address is refused', validateAdvisorEmail('advisor@49financial.com').error !== undefined)
  check('advisor email: an upper-case address is refused', validateAdvisorEmail('Irpt-W5@opal.invalid').error !== undefined)
  check('advisor email: an address with two @ is refused', validateAdvisorEmail('a@b@opal.invalid').error !== undefined)
  check('advisor email: an empty string is refused', validateAdvisorEmail('').error !== undefined)
  check('advisor email: an overlong address (83 characters) is refused', validateAdvisorEmail('a'.repeat(70) + '@opal.invalid').error !== undefined)
  check('advisor email: a local part starting with a dot is refused', validateAdvisorEmail('.abc@opal.invalid').error !== undefined)
  check('advisor email: a subdomain of opal.invalid is refused (the domain is exact)', validateAdvisorEmail('x@mail.opal.invalid').error !== undefined)
  check('advisor email: a non-string is refused', validateAdvisorEmail(null).error !== undefined)
  check('advisor email: parseArgs reads --advisor-email into o.advisorEmail', parseArgs(['--advisor-email', 'a@opal.invalid']).o.advisorEmail === 'a@opal.invalid')
  check('advisor email: parseArgs without the option leaves o.advisorEmail null', parseArgs([]).o.advisorEmail === null)
  check('advisor email: the field shown and the option given fills the address', (() => { const a = advisorFillAction(true, ADV_OK); return a.action === 'fill' && a.value === ADV_OK })())
  check('advisor email: the field not shown fills nothing (absent), with or without the option', advisorFillAction(false, ADV_OK).action === 'absent' && advisorFillAction(false, null).action === 'absent')
  check('advisor email: the field shown and the option not given stops the run (needed, ADVISOR-EMAIL-NEEDED)', (() => { const a = advisorFillAction(true, null); return a.action === 'needed' && a.why.startsWith('ADVISOR-EMAIL-NEEDED') })())
  const badAdvRun = spawnSync(process.execPath, [SELF, '--base', B, '--firm', '49financial', '--holdings', SELF, '--out', os.tmpdir(), '--go', 'IRPT_ANLREQ.TO-RUN-FWD1.x', '--advisor-email', 'X@REAL.example'], { encoding: 'utf8', timeout: 60000 })
  check('advisor email: a bad option refuses the run with rc 2 before any step (RUN-REFUSED advisor-email)', badAdvRun.status === 2 && /RUN-REFUSED advisor-email/.test(badAdvRun.stdout) && !/STEP-1 password generated/.test(badAdvRun.stdout))
  const okAdvPlan = spawnSync(process.execPath, [SELF, '--base', B, '--firm', '49financial', '--holdings', SELF, '--out', os.tmpdir(), '--advisor-email', ADV_OK], { encoding: 'utf8', timeout: 60000 })
  check('advisor email: a valid option without --go is plan only (rc 0) and the plan names the option', okAdvPlan.status === 0 && /PLAN advisor-email option/.test(okAdvPlan.stdout) && /RUN-REFUSED no --go/.test(okAdvPlan.stdout))
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
  // AR-y-379: a bad --advisor-email refuses the run here, before the plan, any mint or any browser.
  if (o.advisorEmail !== null) {
    const adv = validateAdvisorEmail(o.advisorEmail)
    if (adv.error) { console.log('RUN-REFUSED advisor-email: ' + adv.error); return 2 }
  }
  if (o.plan || !o.go) {
    printPlan(o.base, o.advisorEmail)
    if (!o.plan) console.log('RUN-REFUSED no --go order token: plan only, nothing launched')
    return 0
  }
  const baseErr = checkBase(o.base)
  if (baseErr) { console.log('REFUSED base: ' + baseErr); return 2 }
  if (!GO_RE.test(o.go)) { console.log('RUN-REFUSED --go is not an IRPT_ANLREQ.TO-RUN-FWD1.<id> order token'); return 2 }
  if (!o.firm || !o.holdings || !o.out) { console.log('RUN-REFUSED --firm, --holdings and --out are required'); return 2 }
  if (!fs.existsSync(o.holdings)) { console.log('RUN-REFUSED the holdings file does not exist'); return 2 }
  if (!(o.pollMinutes > 0 && o.pollMinutes <= 60)) { console.log('RUN-REFUSED --poll-minutes must be in (0, 60]'); return 2 }
  printPlan(o.base, o.advisorEmail)
  return run(o)
}

if (import.meta.url === pathToFileURL(path.resolve(process.argv[1] || '')).href) {
  main(process.argv.slice(2)).then((rc) => { process.exitCode = rc }, (e) => {
    console.log('ERROR ' + String((e && e.message) || e).slice(0, 200))
    process.exitCode = 1
  })
}
