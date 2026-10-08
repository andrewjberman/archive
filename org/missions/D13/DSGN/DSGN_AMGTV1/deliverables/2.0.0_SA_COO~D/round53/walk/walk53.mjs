// closewalk35.mjs -- DSGN_AMGTV1 round 35 CLOSE WALK (issuer 2.0.0_SA_COO~D, 2026-10-04): round34/walk/gapread.mjs copied
// whole, with two changes. (a) FWD-24's sector/country control accepts the round-35 wording ("... are not in this security's
// data", AV-zm-2). (b) A new read per name, `r35-faces <name>`, probes the landing view and every tab: the word cloud
// ([data-word-cloud] state and [data-term] count, AV-zm-3), the What changed fixed phrase "a line this page has no name for
// yet" and table rows printing "-100.0%" (AV-zm-1), and any visible "payload" (AV-zm-2). PASS needs a cloud in state
// "terms" with >= 1 term, 0 fixed phrases, 0 "-100.0%" rows and 0 "payload". Everything else is gapread's, unchanged.
//
// gapread.mjs -- DSGN_AMGTV1 round 34 GAP READ (instrument for issuer 2.0.0_SA_COO~D, 2026-10-03). Built on
// ../../served-reread-20261002/servedread.mjs: the same walker lease, login, request guard and output conventions.
//
// Usage (repo root; a local build of portal PROD dbd29c6320 on the live API, `bun run dev:live --port 5174`):
//   node <this file> --no-officer "<TICKER>" [--base http://localhost:5174] [--names "BA US,VLO US,AMD US"]
//                    [--non-usd "ROG SW,1299 HK"]
//
// What it reads (ledger/ROUND_ANALYSIS.round33.md s.3; ledger/COMPLETION_GRADES.round32.json):
//   1. tabs-dialog-closed <name>    FWD-27 coverage (FWD-6..11, 14, 16, 17): each of the five tabs, Escape pressed until no
//                                    [role=dialog] is visible BEFORE the tab, then a full-page PNG and the tab's visible text.
//   2. nonusd-header                FWD-4, FWD-13: the first --non-usd name that opens with key figures in a non-USD
//                                    currency; a header PNG and each key-figure tile's label, value and as-of words.
//   3. no-officer-exec <ticker>     FWD-7: the Exec Management tab of --no-officer, its PNG and text.
//   4. fwd24-overlay-census <name>  FWD-24: "not served" / "Not supplied" / "unavailable" / "not carried" strings in the
//                                    overlay header DOM, each attributed to an overlay field; 0 must sit on a field the
//                                    payload CARRIES. Positive control: one field the payload lacks, rendered as its
//                                    designed empty state and not a number. fwd24-control-any-name: >= 1 name showed one.
//   5. display-names <name>         FWD-27 "one display name per security": every visible string naming the security on
//                                    the Lead Panel (bubbles 30/90/365D, all price bars) and on every tab, grouped.
//   6. fwd21-labels-<W>D, fwd21-no-clear-tone, fwd5-timeline-hover, fwd2-bubbles, fwd2-bars, fwd27-account-menu-escape.
// Each read writes OUT/<nn>-<read>.json (+ PNGs) and one line: PASS|FAIL|ERROR <read> :: <evidence> :: <detail>.
// ERROR = the read could not run (its cause is the detail). Exit 0 only when no read is ERROR, whatever the grades say.
// The walker account lease is walk.mjs's own (arm HOLDER, secret, holder-only disarm in finally). Only GET/HEAD/OPTIONS and
// login/refresh/logout pass; telemetry is answered locally. Nothing here clicks Refresh, a star, a day bar or Log Out.
import { createRequire } from 'module'
import { execFileSync } from 'child_process'
import fs from 'fs'
import path from 'path'
import { fileURLToPath } from 'url'

const ROOT = process.cwd()
const ACCOUNT = path.join(ROOT, '.claude', 'skills', 'ui-walk', 'ui_walker_account.py')
const EMAIL = 'opal-ui-walker@opal.test'
const argv = process.argv.slice(2)
const list = (s) => String(s || '').split(',').map((x) => x.trim()).filter(Boolean)
const opt = { base: 'http://localhost:5174', names: ['BA US', 'VLO US', 'AMD US'], nonUsd: ['ROG SW', '1299 HK'], noOfficer: null }
for (let i = 0; i < argv.length; i++) {
  if (argv[i] === '--base') opt.base = argv[++i] || opt.base
  else if (argv[i] === '--names') opt.names = list(argv[++i])
  else if (argv[i] === '--non-usd') opt.nonUsd = list(argv[++i])
  else if (argv[i] === '--no-officer') opt.noOfficer = String(argv[++i] || '').trim() || null
}
if (!opt.noOfficer || !opt.names.length || !opt.nonUsd.length || !fs.existsSync(ACCOUNT) || !fs.existsSync(path.join(ROOT, 'portal', 'package.json'))) {
  console.error('usage (repo root): node <gapread.mjs> --no-officer "<TICKER>" [--base URL] [--names "A,B,C"] [--non-usd "X,Y"]')
  if (!opt.noOfficer) console.error('ERROR: --no-officer <ticker> is required (a name whose filing lists no officers; the issuer supplies it)')
  if (!fs.existsSync(ACCOUNT)) console.error(`ERROR: ${ACCOUNT} not found -- run from the repo root`)
  process.exit(2)
}
const require = createRequire(path.join(ROOT, 'portal', 'package.json'))
const { chromium } = require('playwright-core')
const stamp = new Date().toISOString().replace(/[-:]/g, '').replace(/\.\d+Z$/, 'Z')
const OUT = path.join(path.dirname(fileURLToPath(import.meta.url)), `read-${stamp}`)
fs.mkdirSync(OUT, { recursive: true })
const py = (cmd, extraEnv = {}, ...args) => execFileSync('python', [ACCOUNT, cmd, ...args], { encoding: 'utf8', env: { ...process.env, ...extraEnv }, stdio: ['ignore', 'pipe', 'pipe'] })
const log = (...a) => console.log(new Date().toISOString().slice(11, 19), ...a)
const ADMITTED_POST = [/\/auth\/login$/, /\/auth\/refresh$/, /\/auth\/logout$/]
const CODE = /\b[a-z]+_[a-z0-9_]+\b|_Equity\b|\.json\b|\b[A-Z][A-Z0-9]*_[A-Z0-9_]+\b/
const lc = (s) => String(s ?? '').toLowerCase()
const unwrap = (d) => (d && d.payload ? d.payload : d)
const movedRe = (n) => (n === 0 ? /no change|unchanged/i : new RegExp(`\\b(up|down)\\s+${Math.abs(n)}\\s+place`, 'i'))

const LEASE_BUDGET_MS = 50 * 60 * 1000 // the lease lapses at 60 min (ui_walker_account.py MAX_ARMED_MINUTES)
const TABS = [
  { id: 'thesis', label: 'Thesis' },
  { id: 'exec_management', label: 'Exec Management' },
  { id: 'peers', label: 'Peers' },
  { id: 'model', label: 'Model' },
  { id: 'posture', label: 'Posture' },
]
const KEY_FIGURES = ['PX_LAST', 'CUR_MKT_CAP', 'CURR_ENTP_VAL', 'NET_DEBT', 'EQY_BETA', 'VOLUME_AVG_30D', 'SI_PERCENT_EQUITY_FLOAT']
const MONEY_FIGURES = ['PX_LAST', 'CUR_MKT_CAP', 'CURR_ENTP_VAL', 'NET_DEBT']
const ELLIPSIS = /(\.\.\.|\u2026)\s*$/
const NUMBERISH = /#\s?\d|\d[\d,]*\.\d+|\d\s*%|\b\d+(\.\d+)?\s?[KMBT]\b|\$/
const slug = (s) => String(s).replace(/[^A-Za-z0-9]+/g, '-').replace(/^-+|-+$/g, '') || 'x'
const firstLine = (e) => String((e && e.message) || e).split('\n')[0]
const cssStr = (s) => `"${String(s).replace(/["\\]/g, '\\$&')}"`
const hasTone = (t) => typeof t === 'number' && Number.isFinite(t)
const has = (v) => v !== null && v !== undefined && !(typeof v === 'string' && v.trim() === '')
const collapse = (s) => String(s ?? '').replace(/\s+/g, ' ').trim()
const png = (name) => path.join(OUT, name)

// servedread.mjs, verbatim: every served identity field present in the hover (null ones said "not served"); no code-shaped token.
function identityFaults(hover, row, figure) {
  const f = []
  if (!hover) return ['NO HOVER TEXT']
  const c = row.classification || {}
  const want = { name: row.name || row.display_name || row.ticker, ticker: row.ticker, 'asset class': c.asset_class, 'sub-asset class': c.sub_asset_class, sector: c.sector }
  if (figure !== undefined) want['period figure'] = figure
  for (const [k, v] of Object.entries(want)) {
    if (v === null || v === undefined || v === '') { if (!/not served/i.test(hover)) f.push(`${k} is not served but the hover does not say so`) }
    else if (!lc(hover).includes(lc(v))) f.push(`MISSING ${k} "${v}"`)
  }
  if (typeof row.places_moved === 'number') { if (!movedRe(row.places_moved).test(hover)) f.push(`MISSING places moved ${row.places_moved}`) }
  else if (!/not served|places moved/i.test(hover)) f.push('places moved is null and the hover says nothing about it')
  const m = hover.match(CODE); if (m) f.push(`CODE "${m[0]}"`)
  return f
}

// ---- served payloads, captured from the network log ----
const served = { collected: {}, price: {}, bySeg: {}, days: {} }
const payloadOf = (seg, surface) => (seg && served.bySeg[seg] ? served.bySeg[seg][surface] || null : null)
const overlayFor = (name) => payloadOf(name, 'overlay')
const scans = [] // { scope, opened (name or null), items | error }
const inflight = new Set()

// ---- round 35: the faces probe (runs in the page) and its per-name store ----
function R35_PROBE() {
  const vis = (e) => e.getClientRects().length > 0
  const text = document.body ? document.body.innerText || '' : ''
  const clouds = [...document.querySelectorAll('[data-word-cloud]')].filter(vis).map((e) => ({
    state: e.getAttribute('data-word-cloud'), terms: e.querySelectorAll('[data-term]').length,
    first: [...e.querySelectorAll('[data-term]')].slice(0, 5).map((t) => `${t.getAttribute('data-term')}:${t.getAttribute('data-count')}`),
    text: (e.innerText || '').replace(/\s+/g, ' ').slice(0, 200),
  }))
  const rows = [...document.querySelectorAll('tr')].filter(vis).map((r) => (r.innerText || '').replace(/\s+/g, ' ').trim())
  return {
    clouds,
    unnamed: (text.match(/a line this page has no name for yet/g) || []).length,
    payload: (text.match(/[^\n]{0,60}payload[^\n]{0,60}/gi) || []),
    minus100: rows.filter((t) => /-100\.0%/.test(t)),
  }
}
const R35 = {}

// ---- reads and their evidence ----
const reads = []
let seq = 0
let armedAt = null
function record(id, verdict, detail, data = {}) {
  seq += 1
  const file = `${String(seq).padStart(2, '0')}-${slug(id)}.json`
  try { fs.writeFileSync(path.join(OUT, file), JSON.stringify({ read: id, verdict, detail, ...data }, null, 1)) } catch (e) { detail = `${detail} (evidence not written: ${firstLine(e)})` }
  const evidence = `${path.basename(OUT)}/${file}`
  reads.push({ id, verdict, detail, evidence })
  log(`${verdict} ${id} :: ${evidence} :: ${detail}`)
}
async function read(id, fn, { budget = true } = {}) {
  if (budget && armedAt !== null && Date.now() - armedAt > LEASE_BUDGET_MS) {
    record(id, 'ERROR', 'not run: the walker lease (60 min) is nearly spent', {})
    return null
  }
  try {
    const r = await fn()
    record(id, r.verdict, r.detail, r.data || {})
    return r
  } catch (e) {
    record(id, 'ERROR', `cause: ${firstLine(e)}`, { cause: String((e && e.stack) || e) })
    return null
  }
}

// ---- page-side functions (each self-contained: Playwright serializes them into the page) ----
function DIALOG_OPEN() {
  return [...document.querySelectorAll('[role="dialog"]')].some((d) => d.getClientRects().length > 0 && getComputedStyle(d).visibility !== 'hidden')
}

function HEADER_ROOT() {
  let r = document.querySelector('[data-identity-card]')
  while (r && !r.querySelector('[data-header-more]')) r = r.parentElement
  return r || null
}

// The tab-bar button for a label: the div whose direct buttons carry all five tab labels (TabNavigation renders plain buttons).
function BAR_BUTTON(label) {
  const want = ['thesis', 'exec management', 'peers', 'model', 'posture']
  const norm = (s) => String(s || '').replace(/\s+/g, ' ').trim().toLowerCase()
  for (const d of document.querySelectorAll('div')) {
    const kids = [...d.children].filter((c) => c.tagName === 'BUTTON' || c.getAttribute('role') === 'tab')
    if (kids.length < 5) continue
    const ts = kids.map((b) => norm(b.textContent))
    if (!want.every((w) => ts.includes(w))) continue
    return kids[ts.indexOf(norm(label))] || null
  }
  return null
}

// The tab content: the element after the tab bar's sticky wrapper (SecurityAnalysis.tsx `tabContentRef`).
function TAB_TEXT(id) {
  const want = ['thesis', 'exec management', 'peers', 'model', 'posture']
  const norm = (s) => String(s || '').replace(/\s+/g, ' ').trim().toLowerCase()
  let bar = null
  for (const d of document.querySelectorAll('div')) {
    const ts = [...d.children].filter((c) => c.tagName === 'BUTTON' || c.getAttribute('role') === 'tab').map((b) => norm(b.textContent))
    if (ts.length >= 5 && want.every((w) => ts.includes(w))) { bar = d; break }
  }
  const content = bar && bar.parentElement ? bar.parentElement.nextElementSibling : null
  const panel = document.querySelector(`[data-tab-panel="${id}"]`)
  const el = content || panel
  return {
    panel_present: !!panel,
    loading: !!(panel && panel.querySelector('[data-panel-state="loading"]')),
    panel_states: panel ? [...panel.querySelectorAll('[data-panel-state]')].map((e) => e.getAttribute('data-panel-state')) : [],
    container: content ? 'the element after the tab bar' : panel ? `[data-tab-panel="${id}"]` : 'none',
    text: el ? el.innerText : null,
  }
}

function LABELS() {
  return [...document.querySelectorAll('text[data-bubble-label]')].map((t) => {
    const spans = t.querySelectorAll('tspan')
    const text = (spans.length ? [...spans].map((s) => s.textContent).join(' ') : t.textContent || '').replace(/\s+/g, ' ').trim()
    return { key: t.getAttribute('data-bubble-label'), text, lines: spans.length || 1 }
  })
}

// servedread.mjs's bubble read, verbatim.
function BUBBLES() {
  return [...document.querySelectorAll('[data-bubble]')].map((el) => {
    const t = el.querySelector('title') || (el.parentElement && el.parentElement.querySelector(':scope > title'))
    return { key: el.getAttribute('data-bubble'), hover: (el.getAttribute('title') || (t ? t.textContent : '') || '').replace(/\s+/g, ' ').trim() }
  })
}

function BUBBLE_TITLE(key) {
  const el = document.querySelector(`[data-bubble="${CSS.escape(key)}"]`)
  if (!el) return null
  const t = el.querySelector('title')
  return (el.getAttribute('title') || (t ? t.textContent : '') || '').replace(/\s+/g, ' ').trim()
}

function TOOLTIP_DAY(date) {
  const t = document.querySelector(`[data-timeline-tooltip-day="${CSS.escape(date)}"]`)
  if (!t || t.getClientRects().length === 0) return null
  const box = t.firstElementChild
  const header = box && box.firstElementChild ? box.firstElementChild.textContent.replace(/\s+/g, ' ').trim() : null
  const rows = box ? [...box.querySelectorAll('.space-y-1 > div')].map((r) => {
    const s = r.querySelectorAll('span')
    return { label: s.length ? s[0].textContent.trim() : '', value: s.length ? s[s.length - 1].textContent.trim() : '' }
  }) : []
  return { header, rows, text: (t.innerText || '').replace(/\s+/g, ' ').trim() }
}

function TILES() {
  const row = document.querySelector('[data-key-figures]')
  if (!row) return { present: false, tiles: [], empty: null }
  const empty = row.querySelector('[data-panel-state]') ? row.innerText.replace(/\s+/g, ' ').trim() : null
  const tiles = [...row.querySelectorAll('[data-card-figure]')].map((t) => {
    const spans = [...t.children].filter((c) => c.tagName === 'SPAN')
    const tip = t.querySelector('[data-figure-tooltip]')
    const box = tip ? tip.firstElementChild : null
    const rows = box ? [...box.querySelectorAll('.space-y-1 > div')].map((r) => {
      const s = r.querySelectorAll('span')
      return { label: s.length ? s[0].textContent.trim() : '', value: s.length ? s[s.length - 1].textContent.trim() : '' }
    }) : []
    const valueEl = spans[1] || null
    const asOf = spans.slice(2).map((s) => s.textContent.replace(/\s+/g, ' ').trim()).find((s) => /^as of\b/i.test(s)) || null
    const tipAsOf = rows.find((r) => /^as of$/i.test(r.label))
    return {
      key: t.getAttribute('data-card-figure'),
      mnemonic: t.getAttribute('data-card-figure-mnemonic'),
      label: spans[0] ? spans[0].textContent.trim() : null,
      label_rendered: spans[0] ? spans[0].innerText.trim() : null,
      value: valueEl ? valueEl.textContent.replace(/\s+/g, ' ').trim() : null,
      as_of_at_rest: asOf,
      tooltip_header: box && box.firstElementChild ? box.firstElementChild.textContent.trim() : null,
      tooltip_rows: rows,
      tooltip_as_of: tipAsOf ? tipAsOf.value : null,
      full_value: tip ? tip.getAttribute('data-full-value') : null,
      numerals: valueEl ? getComputedStyle(valueEl).fontVariantNumeric : null,
    }
  })
  return { present: true, tiles, empty }
}

function MENU_OPEN() {
  return [...document.querySelectorAll('button')].some((b) => /^\s*log out\s*$/i.test(b.textContent || '') && b.getClientRects().length > 0)
}

// Every visible short string under <main>, at the deepest element that carries it whole (SVG <title> hovers excluded).
function SCAN() {
  const collapse = (s) => String(s || '').replace(/\s+/g, ' ').trim()
  const LIMIT = 300
  const memo = new Map()
  const textOf = (el) => {
    if (memo.has(el)) return memo.get(el)
    const tag = el.tagName.toLowerCase()
    let out = ''
    if (tag === 'title' || tag === 'script' || tag === 'style' || tag === 'noscript') { memo.set(el, ''); return '' }
    for (const n of el.childNodes) {
      let piece = ''
      if (n.nodeType === 3) piece = n.nodeValue
      else if (n.nodeType === 1) {
        piece = textOf(n)
        if (piece === null) { out = null; break }
        if (tag === 'text') piece = ` ${piece} `
      }
      out += piece
      if (out.length > LIMIT) { out = null; break }
    }
    memo.set(el, out)
    return out
  }
  const dataAttr = (e) => {
    for (const a of e.attributes) if (a.name.startsWith('data-')) return `${a.name}="${String(a.value).slice(0, 40)}"`
    return null
  }
  const pathOf = (el) => {
    const chain = []
    let e = el
    while (e && e !== document.body && chain.length < 8) {
      const d = dataAttr(e)
      chain.unshift(d ? `${e.tagName.toLowerCase()}[${d}]` : e.tagName.toLowerCase())
      if (d && e !== el) break
      e = e.parentElement
    }
    return chain.join(' > ')
  }
  let header = document.querySelector('[data-identity-card]')
  while (header && !header.querySelector('[data-header-more]')) header = header.parentElement
  const want = ['thesis', 'exec management', 'peers', 'model', 'posture']
  let bar = null
  for (const d of document.querySelectorAll('div')) {
    const ts = [...d.children].filter((c) => c.tagName === 'BUTTON' || c.getAttribute('role') === 'tab').map((b) => collapse(b.textContent).toLowerCase())
    if (ts.length >= 5 && want.every((w) => ts.includes(w))) { bar = d; break }
  }
  const tabContent = bar && bar.parentElement ? bar.parentElement.nextElementSibling : null
  const root = document.querySelector('main') || document.body
  const items = []
  for (const el of root.querySelectorAll('*')) {
    const tag = el.tagName.toLowerCase()
    if (tag === 'tspan' || tag === 'title' || tag === 'script' || tag === 'style' || el.closest('title')) continue
    const raw = textOf(el)
    if (raw === null) continue
    const t = collapse(raw)
    if (!t || t.length > 100 || !/[A-Za-z]/.test(t) || t.split(' ').length > 12) continue
    let deeper = false
    for (const c of el.children) { const ct = textOf(c); if (ct !== null && collapse(ct) === t) { deeper = true; break } }
    if (deeper) continue
    if (!el.getClientRects || el.getClientRects().length === 0) continue
    const cs = getComputedStyle(el)
    if (cs.visibility === 'hidden' || cs.display === 'none' || cs.opacity === '0') continue
    const rendered = typeof el.innerText === 'string' ? collapse(el.innerText) : t
    const region = header && header.contains(el) ? 'header' : tabContent && tabContent.contains(el) ? 'tab' : el.closest('[data-chatter-bubbles],[data-price-bars]') ? 'lead-panel' : 'page'
    items.push({ text: t, rendered, region, sel: pathOf(el) })
  }
  return items
}

// The overlay header's "not served"-class strings, each attributed to the field that printed it, plus the control renderings.
function HEADER_CENSUS() {
  const collapse = (s) => String(s || '').replace(/\s+/g, ' ').trim()
  let root = document.querySelector('[data-identity-card]')
  while (root && !root.querySelector('[data-header-more]')) root = root.parentElement
  if (!root) return { error: 'the overlay header did not render (no [data-identity-card] inside a header with details[data-header-more])' }
  const TERMS = /not served|not supplied|unavailable|not carried/gi
  const MAP = [
    ['[data-chatter-monthly]', () => 'ROUTE:/lead-panel/timeseries/collected/chatter'],
    ['div[data-generation-caption]', () => 'axis_reads:TRENDING/PRICE.generation_id'],
    ['[data-card-figure-mnemonic]', (a) => `header_figures:${a.getAttribute('data-card-figure-mnemonic')}`],
    ['[data-key-figures]', () => 'header_figures'],
    ['[data-identity-name]', () => 'display_name'],
    ['[data-identity-sector],[data-identity-country]', () => 'header_figures:GICS_SECTOR_NAME|CNTRY_OF_DOMICILE'],
    ['[data-bloomberg-session]', () => 'bloomberg_session_state'],
    ['[data-identity-card]', () => 'identity'],
    ['[data-header-description]', () => 'description'],
    ['[data-header-feed]', () => 'feed'],
    ['[data-header-posture]', () => 'posture'],
    ['[data-header-dossier-position]', () => 'ROUTE:/thesis dossier_fields'],
    ['[data-header-reading="chatter"]', () => 'ROUTE:/lead-panel/timeseries/collected/chatter'],
    ['[data-timeline-panel]', () => 'ROUTE:/timeline'],
    ['[data-axis-footnote]', () => 'axis_reads'],
  ]
  const PROSE = '[data-feed-item], [data-header-description="SERVED"], [data-timeline-article], [data-timeline-tooltip-day]'
  const dataAttr = (e) => {
    for (const a of e.attributes) if (a.name.startsWith('data-')) return `${a.name}="${String(a.value).slice(0, 40)}"`
    return null
  }
  const pathOf = (el) => {
    const chain = []
    let e = el
    while (e && e !== document.body && chain.length < 8) {
      const d = dataAttr(e)
      chain.unshift(d ? `${e.tagName.toLowerCase()}[${d}]` : e.tagName.toLowerCase())
      if (d && e !== el) break
      e = e.parentElement
    }
    return chain.join(' > ')
  }
  const breakoutCell = [...root.querySelectorAll('div')].find((d) => d.firstElementChild && d.firstElementChild.textContent.trim() === 'Breakout (price)') || null
  const hits = []
  const w = document.createTreeWalker(root, NodeFilter.SHOW_TEXT)
  let n
  while ((n = w.nextNode())) {
    const el = n.parentElement
    if (!el || el.closest('title,script,style')) continue
    const text = n.nodeValue || ''
    const m = text.match(TERMS)
    if (!m) continue
    let field = null
    let via = null
    if (/^\s*sector\/country not carried/i.test(text)) { field = 'header_figures:GICS_SECTOR_NAME|CNTRY_OF_DOMICILE'; via = 'the sector/country line' }
    for (const [sel, f] of MAP) {
      if (field) break
      const a = el.closest(sel)
      if (a && root.contains(a)) { field = f(a); via = sel }
    }
    if (!field && breakoutCell && breakoutCell.contains(el)) { field = 'breakout_price'; via = 'the Breakout (price) cell' }
    hits.push({ text: collapse(text), terms: m.map((x) => x.toLowerCase()), field: field || 'UNATTRIBUTED', via, prose: !!el.closest(PROSE), visible: el.getClientRects().length > 0, sel: pathOf(el) })
  }
  const card = root.querySelector('[data-identity-card]')
  const sectorEl = card ? (card.querySelector('[data-identity-sector],[data-identity-country]') || [...card.querySelectorAll('div')].find((d) => d.children.length === 0 && /sector\/country not carried/i.test(d.textContent || ''))) : null
  const tiles = {}
  for (const t of root.querySelectorAll('[data-card-figure-mnemonic]')) { const k = t.getAttribute('data-card-figure-mnemonic'); tiles[k] = (tiles[k] || 0) + 1 }
  const desc = root.querySelector('[data-header-description]')
  const post = root.querySelector('[data-header-posture]')
  const gen = root.querySelector('[data-axis-footnote] div[data-generation-caption]')
  const keyRow = root.querySelector('[data-key-figures]')
  return {
    hits,
    controls: {
      breakout: breakoutCell ? collapse([...breakoutCell.children].slice(1).map((c) => c.textContent).join(' ')) : null,
      sector: sectorEl ? collapse(sectorEl.textContent) : null,
      identity_name_count: root.querySelectorAll('[data-identity-name]').length,
      tiles,
      key_figures_text: keyRow ? collapse(keyRow.textContent) : null,
      description: desc ? { state: desc.getAttribute('data-header-description'), text: collapse(desc.textContent) } : null,
      posture: post ? { state: post.getAttribute('data-header-posture'), text: collapse(post.textContent) } : null,
      generation: gen ? collapse(gen.textContent) : null,
    },
  }
}

// ---- Node-side helpers ----
async function quiet(page, maxMs = 15000) {
  const t0 = Date.now()
  let calm = null
  while (Date.now() - t0 < maxMs) {
    if (inflight.size === 0) { if (calm === null) calm = Date.now(); if (Date.now() - calm >= 800) return true } else calm = null
    await page.waitForTimeout(200)
  }
  return false
}
const settle = async (page, ms = 1200) => { await page.waitForLoadState('networkidle', { timeout: 35000 }).catch(() => {}); await quiet(page); await page.waitForTimeout(ms) }
async function waitFor(page, fn, ms = 30000) {
  const t0 = Date.now()
  for (;;) {
    const v = fn()
    if (v) return v
    if (Date.now() - t0 > ms) return null
    await page.waitForTimeout(400)
  }
}

async function closeDialogs(page) {
  const initially = await page.evaluate(DIALOG_OPEN)
  let pressed = 0
  for (let i = 0; i < 6 && (await page.evaluate(DIALOG_OPEN)); i++) { await page.keyboard.press('Escape'); pressed += 1; await page.waitForTimeout(500) }
  return { initially, pressed, open: await page.evaluate(DIALOG_OPEN) }
}

async function clickTab(page, label) {
  const re = new RegExp(`^\\s*${label.replace(/\s+/g, '\\s+')}\\s*$`, 'i')
  const roleTab = page.getByRole('tab', { name: re })
  if (await roleTab.count()) { await roleTab.first().click({ timeout: 5000 }); return '[role=tab]' }
  const el = (await page.evaluateHandle(BAR_BUTTON, label)).asElement()
  if (!el) throw new Error(`tab "${label}" not found: no [role=tab] and no tab-bar button with that text`)
  await el.click({ timeout: 5000 })
  return 'tab-bar button (this build renders no [role=tab])'
}

async function waitTabReady(page, id) {
  await page.waitForSelector(`[data-tab-panel="${id}"]`, { timeout: 15000 }).catch(() => {})
  await page.waitForFunction((tid) => {
    const p = document.querySelector(`[data-tab-panel="${tid}"]`)
    return !!p && !p.querySelector('[data-panel-state="loading"]')
  }, id, { timeout: 30000 }).catch(() => {})
  await settle(page, 1500)
}

async function pressSegment(page, group, label) {
  const loc = page.locator(`[role="group"][aria-label="${group}"] button`).filter({ hasText: new RegExp(`^\\s*${label}\\s*$`, 'i') })
  if (await loc.count()) { await loc.first().click({ timeout: 5000 }); return }
  const alt = page.getByRole('button', { name: new RegExp(`^${label}$`, 'i') })
  if (await alt.count()) { await alt.first().click({ timeout: 5000 }); return }
  throw new Error(`the ${group} control has no "${label}" option on the page`)
}

async function scan(page, scope, opened) {
  try { scans.push({ scope, opened, items: await page.evaluate(SCAN) }) } catch (e) { scans.push({ scope, opened, error: firstLine(e), items: [] }) }
}

const searchBox = (page) => page.getByPlaceholder('Search any ticker')
async function toUniverse(page) {
  await closeDialogs(page)
  const back = page.locator('[data-header-action="back"]')
  if (await back.count()) { await back.first().click({ timeout: 5000 }).catch(() => {}); await settle(page, 1500) }
  if (!(await searchBox(page).count())) { await page.goto(opt.base + '/security-analysis', { waitUntil: 'domcontentloaded', timeout: 30000 }); await settle(page, 3000) }
  if (!(await searchBox(page).count())) throw new Error('the ticker search box is not on the page (could not return to all names)')
}

// Open a name the way the page does: LeadPanel.tsx's search form submits the typed ticker (Enter on its one input).
async function openName(page, name) {
  await toUniverse(page)
  const box = searchBox(page).first()
  await box.fill(name)
  await box.press('Enter')
  await page.waitForFunction(() => !document.querySelector('input[placeholder="Search any ticker"]'), null, { timeout: 15000 }).catch(() => {})
  await page.waitForSelector('[data-identity-card], [data-panel-state="error"], [data-panel-state="empty"]', { timeout: 30000 }).catch(() => {})
  await settle(page, 2500)
  if (await searchBox(page).count()) throw new Error(`the search for "${name}" did not open the security view`)
  await waitFor(page, () => overlayFor(name), 20000)
  await page.waitForFunction(() => !document.querySelector('[data-timeline-panel="LOADING"]'), null, { timeout: 20000 }).catch(() => {})
  return overlayFor(name)
}

const axisOf = (ov, movement, subject) => (Array.isArray(ov.axis_reads) ? ov.axis_reads : []).find((a) => a && a.movement === movement && a.subject === subject)
const breakoutRowOf = (ov) => { const a = axisOf(ov, 'BREAKOUT', 'PRICE'); return (a && a.row) || ov.breakout_price || null }
const figOf = (ov, m) => (Array.isArray(ov.header_figures) ? ov.header_figures : []).find((f) => f && f.mnemonic === m)

// Does the overlay payload CARRY the field? true / false; null = not an overlay field (another route) or unknown.
function carriedOf(ov, field) {
  if (field.startsWith('ROUTE:') || field === 'UNATTRIBUTED') return null
  if (field.startsWith('header_figures:')) return field.slice('header_figures:'.length).split('|').some((m) => { const f = figOf(ov, m); return !!f && has(f.value) })
  switch (field) {
    case 'header_figures': return (Array.isArray(ov.header_figures) ? ov.header_figures : []).some((f) => f && has(f.value))
    case 'display_name': return has(ov.display_name)
    case 'identity': return !!ov.identity && ov.identity.identity_status === 'MEASURED' && has(ov.identity.display_ticker)
    case 'bloomberg_session_state': return has(ov.bloomberg_session_state)
    case 'description': return !!ov.description && ov.description.status === 'SERVED' && has(ov.description.text)
    case 'feed': return !!ov.feed
    case 'posture': return !!ov.posture
    case 'axis_reads': return Array.isArray(ov.axis_reads) && ov.axis_reads.length > 0
    case 'axis_reads:TRENDING/PRICE.generation_id': { const a = axisOf(ov, 'TRENDING', 'PRICE'); return !!a && 'generation_id' in a }
    case 'breakout_price': return !!breakoutRowOf(ov)
    default: return null
  }
}
const CENSUS_FIELDS = ['display_name', 'identity', 'bloomberg_session_state', ...KEY_FIGURES.map((m) => `header_figures:${m}`),
  'header_figures:GICS_SECTOR_NAME', 'header_figures:CNTRY_OF_DOMICILE', 'header_figures:CRNCY', 'description', 'feed', 'posture',
  'axis_reads', 'axis_reads:TRENDING/PRICE.generation_id', 'breakout_price']

// The positive control: lacking fields, in the order tried; each with its designed empty state and the check of it.
function controlCandidates(ov, c) {
  const out = []
  const lacking = (f) => carriedOf(ov, f) === false
  if (lacking('breakout_price')) out.push({ field: 'breakout_price', designed: 'a sentence saying why there is no reading (no rank, no %)', observed: c.breakout, ok: !!c.breakout && !NUMBERISH.test(c.breakout) })
  if (lacking('header_figures:GICS_SECTOR_NAME|CNTRY_OF_DOMICILE')) out.push({ field: 'header_figures:GICS_SECTOR_NAME|CNTRY_OF_DOMICILE', designed: '"sector and country are not in this security\'s data" (round 35)', observed: c.sector, ok: !!c.sector && /sector and country are not in this security's data/i.test(c.sector) && !NUMBERISH.test(c.sector) })
  if (lacking('axis_reads:TRENDING/PRICE.generation_id')) out.push({ field: 'axis_reads:TRENDING/PRICE.generation_id', designed: '"price: ranking details are not carried with this list"', observed: c.generation, ok: !!c.generation && /not carried/i.test(c.generation) && !NUMBERISH.test(c.generation) })
  if (lacking('posture')) out.push({ field: 'posture', designed: '"Posture: not carried on this payload." ([data-header-posture="NOT_READ"])', observed: c.posture, ok: !!c.posture && c.posture.state === 'NOT_READ' })
  if (lacking('display_name')) out.push({ field: 'display_name', designed: 'no [data-identity-name] line (the card shows the ticker only)', observed: `${c.identity_name_count} [data-identity-name] element(s)`, ok: c.identity_name_count === 0 })
  if (lacking('description')) out.push({ field: 'description', designed: 'an empty [data-header-description="ABSENT"|"NOT_READ"] element (prints nothing)', observed: c.description, ok: !!c.description && c.description.state !== 'SERVED' && c.description.text === '' })
  for (const m of KEY_FIGURES) {
    if (lacking(`header_figures:${m}`)) out.push({ field: `header_figures:${m}`, designed: 'no tile at all (a figure with no source prints nothing, SAUX-31)', observed: `${c.tiles[m] || 0} [data-card-figure-mnemonic="${m}"] tile(s)`, ok: !c.tiles[m] })
  }
  return out
}

async function overlayCensus(page, name, ov) {
  if (!ov) throw new Error(`no /overlay payload was captured for "${name}"`)
  const wasOpen = await page.evaluate(() => { const d = document.querySelector('details[data-header-more]'); return d ? d.open : null })
  if (wasOpen === null) throw new Error('the overlay header did not render (no details[data-header-more])')
  const summary = page.locator('details[data-header-more] > summary').first()
  if (!wasOpen) { await summary.click({ timeout: 5000 }); await page.waitForTimeout(400) }
  const dom = await page.evaluate(HEADER_CENSUS)
  if (dom.error) throw new Error(dom.error)
  const shot = `fwd24-${slug(name)}-header.png`
  const h = (await page.evaluateHandle(HEADER_ROOT)).asElement()
  if (h) await h.screenshot({ path: png(shot) }); else await page.screenshot({ path: png(shot), fullPage: true })
  if (!wasOpen) { await summary.click({ timeout: 5000 }).catch(() => {}); await page.waitForTimeout(300) }
  const hits = dom.hits.map((x) => {
    const c = carriedOf(ov, x.field)
    const cls = x.prose ? 'SERVED_PROSE' : x.field.startsWith('ROUTE:') ? 'OTHER_ROUTE' : c === true ? 'ON_CARRIED_FIELD' : c === false ? 'ON_LACKING_FIELD' : 'UNATTRIBUTED'
    return { ...x, class: cls }
  })
  const carried = CENSUS_FIELDS.filter((f) => carriedOf(ov, f) === true)
  const lackingFields = CENSUS_FIELDS.filter((f) => carriedOf(ov, f) === false)
  const onCarried = hits.filter((x) => x.class === 'ON_CARRIED_FIELD')
  const unattributed = hits.filter((x) => x.class === 'UNATTRIBUTED')
  const candidates = controlCandidates(ov, dom.controls)
  const control = candidates[0] || null
  const faults = []
  if (onCarried.length) faults.push(`${onCarried.length} string(s) on carried fields: ${onCarried.map((x) => `${x.field} "${x.text}"`).join('; ')}`)
  if (unattributed.length) faults.push(`${unattributed.length} string(s) not attributable to a field: ${unattributed.map((x) => `"${x.text}" at ${x.sel}`).join('; ')}`)
  if (control && !control.ok) faults.push(`control ${control.field} renders "${typeof control.observed === 'string' ? control.observed : JSON.stringify(control.observed)}", not its designed empty state`)
  const br = breakoutRowOf(ov)
  return {
    verdict: faults.length ? 'FAIL' : 'PASS',
    detail: `${onCarried.length} on carried fields (${carried.length} carried); ${control ? `control ${control.field}: ${control.ok ? 'designed empty state, no number' : 'WRONG'}` : 'control: none on this name (every checked field carried)'}${faults.length ? ` -- ${faults.join(' | ')}` : ''}`,
    data: {
      name, png: shot, security_key: ov.security_key ?? null,
      carried_fields: carried, lacking_fields: lackingFields,
      not_served_strings: hits,
      counts: { on_carried_field: onCarried.length, on_lacking_field: hits.filter((x) => x.class === 'ON_LACKING_FIELD').length, other_route: hits.filter((x) => x.class === 'OTHER_ROUTE').length, served_prose: hits.filter((x) => x.class === 'SERVED_PROSE').length, unattributed: unattributed.length },
      control, control_candidates: candidates, dom_controls: dom.controls,
      served_excerpt: {
        display_name: ov.display_name ?? null,
        identity: ov.identity ? { display_ticker: ov.identity.display_ticker, company_name: ov.identity.company_name ?? null, identity_status: ov.identity.identity_status } : null,
        header_figures: (Array.isArray(ov.header_figures) ? ov.header_figures : []).filter((f) => f && [...KEY_FIGURES, 'GICS_SECTOR_NAME', 'CNTRY_OF_DOMICILE', 'CRNCY'].includes(f.mnemonic)).map((f) => ({ mnemonic: f.mnemonic, value: f.value, currency: f.currency ?? null, unit: f.unit ?? null, vintage: f.vintage ?? null })),
        description_status: ov.description ? ov.description.status : null,
        feed_status: ov.feed ? ov.feed.coverage_status : null,
        posture_status: ov.posture ? ov.posture.status : null,
        breakout_price: br ? { rank: br.rank ?? null, pct_jump_pct: br.pct_jump_pct ?? null, places_moved: br.places_moved ?? null } : null,
      },
      terms: 'not served | not supplied | unavailable (the brief) + not carried (this build\'s own empty-state words)',
    },
  }
}

async function tabsRead(page, name) {
  const tabs = []
  const faults = []
  for (let i = 0; i < TABS.length; i++) {
    const t = TABS[i]
    const esc = await closeDialogs(page)
    const via = await clickTab(page, t.label)
    await waitTabReady(page, t.id)
    const shot = `tabs-${slug(name)}-${i + 1}-${slug(t.label)}.png`
    const atShot = await page.evaluate(DIALOG_OPEN)
    await page.screenshot({ path: png(shot), fullPage: true })
    const tx = await page.evaluate(TAB_TEXT, t.id)
    ;(R35[name] = R35[name] || []).push({ where: `tab ${t.label}`, png: shot, ...(await page.evaluate(R35_PROBE)) })
    await scan(page, `${name} / ${t.label}`, name)
    tabs.push({ tab: t.label, found_by: via, dialog_open_initially: esc.initially, escapes_pressed: esc.pressed, dialog_open_before_tab: esc.open, dialog_open_at_shot: atShot, png: shot, panel_present: tx.panel_present, still_loading_at_shot: tx.loading, panel_states: tx.panel_states, text_container: tx.container, text: tx.text })
    if (esc.open) faults.push(`${t.label}: a dialog was still open after ${esc.pressed} Escape press(es)`)
    if (atShot) faults.push(`${t.label}: a dialog stood over the tab at the shot`)
    if (!tx.panel_present) faults.push(`${t.label}: no [data-tab-panel="${t.id}"] rendered`)
    if (tx.loading) faults.push(`${t.label}: still loading after 30 s`)
  }
  return {
    verdict: faults.length ? 'FAIL' : 'PASS',
    detail: faults.length ? faults.join(' | ') : `5 of 5 tabs read; dialog_open_before_tab false on all 5 (Escape presses: ${tabs.map((x) => x.escapes_pressed).join('/')})`,
    data: { name, tabs },
  }
}

async function fwd21Window(page, w, state) {
  await pressSegment(page, 'Subject', 'Chatter')
  await pressSegment(page, 'Window', `${w}D`)
  const set = await waitFor(page, () => served.collected[String(w)], 30000)
  if (!set) throw new Error(`no collected-chatter payload for days=${w} was captured within 30 s`)
  await page.waitForSelector('[data-bubble], [data-chatter-none]', { timeout: 30000 }).catch(() => {})
  if (typeof set.window_days === 'number') await page.waitForSelector(`[data-chatter-bubbles][data-chatter-window="${set.window_days}"]`, { timeout: 15000 }).catch(() => {})
  await settle(page, 1500)
  const shot = `fwd21-${w}D-face.png`
  await page.screenshot({ path: png(shot), fullPage: true })
  const labels = await page.evaluate(LABELS)
  await scan(page, `Lead Panel / Chatter ${w}D`, null)
  const rows = new Map(((set && set.rows) || []).map((r) => [r.security_key, r]))
  const drawn = new Set(labels.map((l) => l.key))
  state.noToneCandidates[w] = [...rows.values()].filter((r) => !hasTone(r.tone) && drawn.has(r.security_key)).map((r) => r.security_key)
  const marks = []
  for (const l of labels.filter((x) => ELLIPSIS.test(x.text))) {
    await page.locator(`circle[data-bubble=${cssStr(l.key)}]`).first().hover({ force: true, timeout: 4000 }).catch(() => {})
    await page.waitForTimeout(150)
    const hover = await page.evaluate(BUBBLE_TITLE, l.key)
    const row = rows.get(l.key)
    const full = row ? collapse(row.display_name) : null
    const lead = l.text.replace(ELLIPSIS, '').trim()
    const faults = []
    if (!hover) faults.push('no hover text')
    else if (!full) faults.push('no served row for this bubble')
    else if (!hover.includes(full)) faults.push(`the hover lacks the full served name "${full}"`)
    if (full && !full.startsWith(lead)) faults.push(`the label "${l.text}" is not a leading part of "${full}"`)
    marks.push({ key: l.key, label: l.text, full_name: full, hover, faults })
  }
  await page.mouse.move(2, 2)
  const bad = marks.filter((m) => m.faults.length)
  return {
    verdict: bad.length ? 'FAIL' : 'PASS',
    detail: `${labels.length} bubble labels, ${marks.length} shortened; ${marks.length - bad.length} of ${marks.length} hovers carry the full name${marks.length ? '' : ' (nothing to hover)'}${bad.length ? ` -- ${bad.map((m) => `${m.label}: ${m.faults.join(', ')}`).join(' | ')}` : ''}`,
    data: { window_days_requested: w, window_days_served: set.window_days ?? null, window_end: set.window_end ?? null, png: shot, hover_carrier: 'the bubble\'s SVG <title> (a native tooltip; a headless PNG does not draw it)', labels, shortened: marks },
  }
}

async function noToneRead(page, w, key) {
  const set = served.collected[String(w)]
  const row = ((set && set.rows) || []).find((r) => r.security_key === key)
  await page.locator(`circle[data-bubble=${cssStr(key)}]`).first().hover({ force: true, timeout: 4000 }).catch(() => {})
  await page.waitForTimeout(150)
  const hover = await page.evaluate(BUBBLE_TITLE, key)
  await page.mouse.move(2, 2)
  const ok = !!hover && /no clear tone/i.test(hover)
  return {
    verdict: ok ? 'PASS' : 'FAIL',
    detail: `${row ? row.display_name : key} at ${w}D (served tone ${row && 'tone' in row ? JSON.stringify(row.tone) : 'absent'}): ${ok ? 'the hover says "no clear tone"' : `the hover does not say "no clear tone": "${hover}"`}`,
    data: { window_days: w, key, display_name: row ? row.display_name : null, served_tone: row && 'tone' in row ? row.tone : 'absent', hover },
  }
}

async function fwd2Bubbles(page) {
  const set = await waitFor(page, () => served.collected['30'] || served.collected.default, 30000)
  if (!set) throw new Error('no collected-chatter payload was captured for the 30D face')
  await page.waitForSelector('[data-bubble]', { timeout: 30000 }).catch(() => {})
  await settle(page, 1000)
  const bubbles = await page.evaluate(BUBBLES)
  const shot = 'fwd2-chatter-30D.png'
  await page.screenshot({ path: png(shot) })
  const crow = new Map(((set && set.rows) || []).map((r) => [r.security_key, r]))
  const marks = []
  for (const b of bubbles.filter((x) => crow.has(x.key)).slice(0, 3)) {
    await page.locator(`circle[data-bubble=${cssStr(b.key)}]`).first().hover({ force: true, timeout: 4000 }).catch(() => {})
    const hover = (await page.evaluate(BUBBLE_TITLE, b.key)) || b.hover
    marks.push({ key: b.key, hover, faults: identityFaults(hover, crow.get(b.key)) })
  }
  await page.mouse.move(2, 2)
  if (bubbles.length === 0) marks.push({ key: '-', hover: '', faults: ['no [data-bubble] mark drawn'] })
  else if (marks.length === 0) marks.push({ key: '-', hover: '', faults: ['no drawn bubble matches a served row'] })
  const crows = (set && set.rows) || []
  const census = (f) => `${crows.filter(f).length} of ${crows.length}`
  const bad = marks.filter((m) => m.faults.length)
  return {
    verdict: bad.length ? 'FAIL' : 'PASS',
    detail: `${marks.length - bad.length} of ${marks.length} bubble hovers clean${bad.length ? ` -- ${bad.map((m) => `${m.key}: ${m.faults.join(', ')}`).join(' | ')}` : ''}`,
    data: { png: shot, marks, served_census: `collected-chatter rows carrying ticker: ${census((r) => r.ticker)}; classification: ${census((r) => r.classification)}; places_moved number: ${census((r) => typeof r.places_moved === 'number')}` },
  }
}

async function fwd2Bars(page) {
  await pressSegment(page, 'Window', '30D')
  await page.waitForTimeout(500)
  await pressSegment(page, 'Subject', 'Price').catch(async () => {
    const ok = await page.getByText('Price', { exact: true }).first().click({ timeout: 4000 }).then(() => true).catch(() => false)
    if (!ok) throw new Error('the Price segment did not open')
  })
  await settle(page, 2500)
  // The Price face's read can land after network-idle: wait for the drawn bars AND the captured payload (up to 30 s).
  await page.waitForSelector('[data-price-bar]', { timeout: 30000 }).catch(() => {})
  const set = await waitFor(page, () => { const p = served.price['30'] || served.price.default; return p && p.rows && p.rows.length ? p : null }, 30000)
  if (!set) throw new Error('no trending price payload with rows was captured within 30 s')
  const bars = await page.evaluate(() => [...document.querySelectorAll('[data-price-bar]')].map((el) => ({ key: el.getAttribute('data-price-bar'), hover: (el.getAttribute('title') || '').replace(/\s+/g, ' ').trim() })))
  const shot = 'fwd2-price.png'
  await page.screenshot({ path: png(shot) })
  // The served period figure: the fixture's `return_30d_pct`, else the first numeric *_pct field the live row carries.
  const figOfRow = (r) => (typeof r.return_30d_pct === 'number' ? r.return_30d_pct
    : Object.entries(r).filter(([k, v]) => /_pct$/.test(k) && typeof v === 'number').map(([, v]) => v)[0])
  const prows = (set.rows || []).filter((r) => typeof figOfRow(r) === 'number')
  const byKey = new Map(prows.map((r) => [r.security_key || r.ticker, r]))
  const top = [...prows].sort((a, b) => Math.abs(figOfRow(b)) - Math.abs(figOfRow(a))).slice(0, 3)
  const marks = []
  for (const r of top) {
    const k = r.security_key || r.ticker
    const bar = bars.find((x) => x.key === k)
    if (bar) await page.locator(`[data-price-bar=${cssStr(k)}]`).first().hover({ force: true, timeout: 4000 }).catch(() => {})
    marks.push({ key: k, hover: bar ? bar.hover : '', faults: bar ? identityFaults(bar.hover, byKey.get(k), Math.abs(figOfRow(r)).toFixed(1)) : ['no bar for this served row'] })
  }
  await page.mouse.move(2, 2)
  if (!marks.length) marks.push({ key: '-', hover: '', faults: ['no served price row carries a figure'] })
  // Every bar, for the display-name census (the face shows 20 at rest; "Show all" is a local toggle, no request).
  const expand = page.locator('[data-price-expand][aria-expanded="false"]')
  if (await expand.count()) { await expand.first().click({ timeout: 5000 }).catch(() => {}); await page.waitForTimeout(800) }
  const allShot = 'fwd2-price-all-names.png'
  await page.screenshot({ path: png(allShot), fullPage: true })
  await scan(page, 'Lead Panel / Price (all names)', null)
  const bad = marks.filter((m) => m.faults.length)
  return {
    verdict: bad.length ? 'FAIL' : 'PASS',
    detail: `${marks.length - bad.length} of ${marks.length} bar hovers clean (the 3 largest moves)${bad.length ? ` -- ${bad.map((m) => `${m.key}: ${m.faults.join(', ')}`).join(' | ')}` : ''}`,
    data: { png: shot, png_all_names: allShot, marks, price_rows: (set.rows || []).length, price_row_keys: set.rows && set.rows[0] ? Object.keys(set.rows[0]) : [] },
  }
}

async function fwd5Read(page, name, ov, days) {
  const key = ov.security_key
  const bars = []
  for (const d of days) {
    const loc = page.locator(`rect[data-day-bar=${cssStr(d.date)}]`).first()
    if (!(await loc.count())) { bars.push({ date: d.date, served_articles: d.articles_total, faults: ['no bar drawn for this served day'] }); continue }
    await loc.hover({ force: true, timeout: 5000 })
    let tip = null
    const t0 = Date.now()
    while (Date.now() - t0 < 12000) {
      tip = await page.evaluate(TOOLTIP_DAY, d.date)
      const head = tip && tip.rows.find((r) => /strongest headline/i.test(r.label))
      if (head && !/^loading/i.test(head.value)) break
      await page.waitForTimeout(400)
    }
    const shot = `fwd5-${slug(name)}-${d.date}.png`
    await page.screenshot({ path: png(shot) })
    const faults = []
    const row = (label) => (tip ? tip.rows.find((r) => r.label.toLowerCase() === label.toLowerCase()) : null)
    if (!tip) faults.push('no tooltip shown on hover')
    else {
      for (const l of ['Articles', 'Distinct publishers', 'Mentions', 'Strongest headline']) if (!row(l)) faults.push(`no "${l}" row`)
      const a = row('Articles')
      if (a && a.value !== String(d.articles_total)) faults.push(`Articles reads "${a.value}", served ${d.articles_total}`)
      const hl = row('Strongest headline')
      if (hl && /^(loading|not available)/i.test(hl.value)) faults.push(`the headline reads "${hl.value}"`)
      const day = unwrap(served.days[`${key}|${d.date}`])
      const servedHead = day && Array.isArray(day.articles) && day.articles[0] ? day.articles[0].headline : null
      if (hl && servedHead && collapse(hl.value) !== collapse(servedHead)) faults.push(`the headline is not the day route's first (strongest) article "${servedHead}"`)
    }
    bars.push({ date: d.date, served_articles: d.articles_total, served_publishers: d.publishers_distinct ?? null, served_mentions: d.mention_count_total ?? null, tooltip: tip, png: shot, faults })
  }
  await page.mouse.move(2, 2)
  await page.waitForTimeout(300)
  const dialogAfter = await page.evaluate(DIALOG_OPEN)
  if (dialogAfter) await closeDialogs(page)
  const bad = bars.filter((b) => b.faults.length)
  const faults = bad.map((b) => `${b.date}: ${b.faults.join(', ')}`)
  if (dialogAfter) faults.push('a day dialog opened during the hovers (a hover must not open the day)')
  return {
    verdict: faults.length || !bars.length ? 'FAIL' : 'PASS',
    detail: `${name}: ${bars.length - bad.length} of ${bars.length} hovered bars show articles, publishers, mentions and the headline${faults.length ? ` -- ${faults.join(' | ')}` : ''}`,
    data: { name, security_key: key, bars },
  }
}

function nonUsdProblem(ov) {
  if (!ov) return 'no /overlay payload captured'
  if (!ov.identity || ov.identity.identity_status !== 'MEASURED') return `identity ${ov.identity ? ov.identity.identity_status : 'absent'}`
  if (!KEY_FIGURES.some((m) => { const f = figOf(ov, m); return !!f && has(f.value) })) return 'no key figure served'
  const cur = servedCurrency(ov)
  if (cur === 'USD') return 'served currency is USD'
  return null
}
function servedCurrency(ov) {
  const c = figOf(ov, 'CRNCY')
  if (c && typeof c.value === 'string' && c.value.trim()) return c.value.trim()
  for (const m of MONEY_FIGURES) { const f = figOf(ov, m); if (f && typeof f.currency === 'string' && f.currency.trim()) return f.currency.trim() }
  return null
}

async function nonUsdRead(page) {
  const attempts = []
  for (const name of opt.nonUsd) {
    let ov = null
    try { ov = await openName(page, name) } catch (e) { attempts.push({ name, used: false, why: `did not open: ${firstLine(e)}` }); continue }
    const why = nonUsdProblem(ov)
    if (why) { attempts.push({ name, used: false, why }); continue }
    attempts.push({ name, used: true })
    const tiles = await page.evaluate(TILES)
    const shot = `nonusd-${slug(name)}-header.png`
    const h = (await page.evaluateHandle(HEADER_ROOT)).asElement()
    if (h) await h.screenshot({ path: png(shot) }); else await page.screenshot({ path: png(shot), fullPage: true })
    const fullShot = `nonusd-${slug(name)}-page.png`
    await page.screenshot({ path: png(fullShot), fullPage: true })
    let hoverShot = null
    const first = page.locator('[data-key-figures] [data-card-figure]').first()
    if (await first.count()) {
      await first.hover({ timeout: 4000 }).catch(() => {})
      await page.waitForTimeout(300)
      hoverShot = `nonusd-${slug(name)}-tile-hover.png`
      if (h) await h.screenshot({ path: png(hoverShot) }); else await page.screenshot({ path: png(hoverShot) })
      await page.mouse.move(2, 2)
    }
    const faults = []
    if (!tiles.present) faults.push('no [data-key-figures] row')
    if (!tiles.tiles.length) faults.push(`no key-figure tile rendered${tiles.empty ? ` ("${tiles.empty}")` : ''}`)
    for (const t of tiles.tiles) {
      const fig = figOf(ov, t.mnemonic)
      if (MONEY_FIGURES.includes(t.mnemonic)) {
        const cur = fig && typeof fig.currency === 'string' && fig.currency.trim() ? fig.currency.trim() : null
        if (cur && !String(t.value || '').startsWith(`${cur} `)) faults.push(`${t.label}: "${t.value}" does not lead with its served currency ${cur}`)
        if (!cur && !/currency not stated/i.test(String(t.value || ''))) faults.push(`${t.label}: "${t.value}" has no served currency and does not say so`)
      }
      if (/\$/.test(String(t.value || ''))) faults.push(`${t.label}: prints a "$"`)
      if (!/tabular-nums/.test(String(t.numerals || ''))) faults.push(`${t.label}: numerals are "${t.numerals}", not tabular-nums`)
      if (!t.tooltip_as_of || /not stated/i.test(t.tooltip_as_of)) faults.push(`${t.label}: no as-of words (tooltip as-of "${t.tooltip_as_of}")`)
    }
    return {
      verdict: faults.length ? 'FAIL' : 'PASS',
      detail: `${name} (served currency ${servedCurrency(ov) ?? 'not served'}): ${tiles.tiles.length} tiles${faults.length ? ` -- ${faults.join(' | ')}` : '; every money tile leads with its served currency, tabular numerals, as-of words on each'}`,
      data: {
        name, attempts, png_header: shot, png_page: fullShot, png_tile_hover: hoverShot, served_currency: servedCurrency(ov),
        tiles: tiles.tiles,
        served_figures: (Array.isArray(ov.header_figures) ? ov.header_figures : []).filter((f) => f && [...KEY_FIGURES, 'CRNCY'].includes(f.mnemonic)).map((f) => ({ mnemonic: f.mnemonic, value: f.value, currency: f.currency ?? null, unit: f.unit ?? null, vintage: f.vintage ?? null })),
      },
    }
  }
  throw new Error(`no non-USD name opened with key figures (${attempts.map((a) => `${a.name}: ${a.why}`).join('; ')})`)
}

async function noOfficerRead(page, ticker) {
  const ov = await openName(page, ticker)
  const esc = await closeDialogs(page)
  const via = await clickTab(page, 'Exec Management')
  await waitTabReady(page, 'exec_management')
  const atShot = await page.evaluate(DIALOG_OPEN)
  const shot = `no-officer-${slug(ticker)}-exec.png`
  await page.screenshot({ path: png(shot), fullPage: true })
  const tx = await page.evaluate(TAB_TEXT, 'exec_management')
  const dom = await page.evaluate(() => {
    const p = document.querySelector('[data-tab-panel="exec_management"]')
    const s = p ? p.querySelector('[data-exec-status]') : null
    return { exec_status: s ? s.getAttribute('data-exec-status') : null, absent_because: s ? s.getAttribute('data-exec-absent-because') : null, officer_rows: p ? p.querySelectorAll('[data-exec-officer]').length : 0 }
  })
  // The response handler stores payloads asynchronously: wait for the /thesis body the tab rendered from.
  const th = await waitFor(page, () => payloadOf(ticker, 'thesis') || (ov && payloadOf(ov.security_key, 'thesis')), 15000)
  if (!th) throw new Error(`no /thesis payload was captured for "${ticker}"`)
  const m = th.management || null
  const officers = m && Array.isArray(m.officers) ? m.officers : []
  const fallback = !!m && m.roster_source === 'BLOOMBERG_FALLBACK'
  const faults = []
  if (esc.open || atShot) faults.push('a dialog stood over the tab')
  if (!m) faults.push('the /thesis payload carries no management block')
  else if (officers.length > 0 && !fallback) faults.push(`the filing lists ${officers.length} officer(s): not a no-officer filing (supply another --no-officer name)`)
  if (!dom.exec_status) faults.push('no [data-exec-status] rendered on the tab')
  if (fallback && /officer\(s\) from the filing/i.test(tx.text || '')) faults.push('a fallback roster says "from the filing"')
  return {
    verdict: faults.length ? 'FAIL' : 'PASS',
    detail: `${ticker}: management ${m ? m.management_status : 'absent'}${m && m.absent_because ? ` (${m.absent_because})` : ''}, ${officers.length} served officer(s)${fallback ? ', Bloomberg fallback roster' : ''}; tab shows [data-exec-status="${dom.exec_status}"]${faults.length ? ` -- ${faults.join(' | ')}` : ''}`,
    data: {
      ticker, png: shot, tab_found_by: via, dialog_open_before_tab: esc.open, dialog_open_at_shot: atShot, dom,
      served_management: m ? { management_status: m.management_status ?? null, absent_because: m.absent_because ?? null, roster_status: m.roster_status ?? null, roster_source: m.roster_source ?? null, source_item: m.source_item ?? null, officers: officers.length, reason: m.reason ?? null } : null,
      text: tx.text,
    },
  }
}

async function accountMenuRead(page) {
  await closeDialogs(page)
  let btn = page.locator('aside button[title="User settings"]')
  let via = 'aside button[title="User settings"]'
  if (!(await btn.count())) { btn = page.locator('aside > div:last-child > button'); via = 'aside > div:last-child > button' }
  if (!(await btn.count())) throw new Error('the account menu button was not found in the sidebar')
  const before = await page.evaluate(MENU_OPEN)
  await btn.first().click({ timeout: 5000 })
  await page.waitForTimeout(500)
  const opened = await page.evaluate(MENU_OPEN)
  const openShot = 'fwd27-account-menu-open.png'
  await page.screenshot({ path: png(openShot) })
  if (!opened) throw new Error(`the account menu did not open on a press of ${via}`)
  await page.keyboard.press('Escape')
  await page.waitForTimeout(600)
  const afterEscape = await page.evaluate(MENU_OPEN)
  const closedShot = 'fwd27-account-menu-after-escape.png'
  await page.screenshot({ path: png(closedShot) })
  let restored = null
  if (afterEscape) { await btn.first().click({ timeout: 5000 }).catch(() => {}); await page.waitForTimeout(400); restored = !(await page.evaluate(MENU_OPEN)) } // toggle shut; never "Log Out"
  return {
    verdict: afterEscape ? 'FAIL' : 'PASS',
    detail: afterEscape ? 'the account menu stayed open after Escape' : 'the account menu opened and Escape closed it',
    data: { button: via, open_before: before, opened, open_after_escape: afterEscape, closed_by_toggle_after_fail: restored, png_open: openShot, png_after_escape: closedShot },
  }
}

// ---- the display-name census (pure: runs on the scans after the browser closes) ----
const SUFFIX = new Set(['the', 'inc', 'incorporated', 'corp', 'corporation', 'co', 'company', 'companies', 'ltd', 'limited', 'plc', 'sa', 'ag', 'nv', 'se', 'spa', 'holdings', 'holding', 'group', 'lp', 'llc', 'cl', 'class', 'a', 'b', 'adr', 'ads', 'sponsored', 'spon', 'ord', 'shs', 'com', 'subject'])
const coreOf = (s) => String(s || '').toLowerCase().replace(/\(subject\)/g, ' ').replace(ELLIPSIS, ' ').split(/[^a-z0-9]+/).filter((t) => t && !SUFFIX.has(t)).join(' ')
const displayOf = (s) => collapse(s).replace(/\s*\(subject\)\s*$/i, '')

function knownNames(name) {
  const ov = overlayFor(name)
  const key = ov ? ov.security_key : null
  const src = []
  const add = (where, v) => { if (typeof v === 'string' && v.trim() && !src.some((x) => x.where === where && x.name === v.trim())) src.push({ where, name: v.trim() }) }
  if (ov) { add('overlay.display_name', ov.display_name); add('overlay.identity.company_name', ov.identity && ov.identity.company_name) }
  const th = payloadOf(name, 'thesis') || payloadOf(key, 'thesis')
  if (th) add('thesis.identity.company_name', th.identity && th.identity.company_name)
  const pe = payloadOf(name, 'peers') || payloadOf(key, 'peers')
  if (pe) { add('peers.subject.name', pe.subject && pe.subject.name); add('peers.identity.company_name', pe.identity && pe.identity.company_name) }
  const mine = (r) => (key && r.security_key === key) || (typeof r.ticker === 'string' && r.ticker.trim() === name)
  for (const [d, set] of Object.entries(served.collected)) for (const r of (set && set.rows) || []) if (mine(r)) add(`collected-chatter[days=${d}].display_name`, r.display_name)
  for (const [d, set] of Object.entries(served.price)) {
    for (const r of (set && set.rows) || []) if (mine(r)) { add(`price[days=${d}].name`, r.name); add(`price[days=${d}].classification.name`, r.classification && r.classification.name) }
  }
  return { key, src }
}

function namesSecurity(text, cores, rawNames) {
  const k = coreOf(text)
  if (!k) return false
  if (cores.has(k)) return true
  if (ELLIPSIS.test(text)) {
    const lead = collapse(text.replace(ELLIPSIS, '')).toLowerCase()
    if (lead.length >= 3 && rawNames.some((n) => n.startsWith(lead))) return true
    if (k.length >= 3) for (const c of cores) if (c.startsWith(k)) return true
  }
  return false
}

function displayNames(name) {
  const { key, src } = knownNames(name)
  if (!src.length) throw new Error(`no served name for "${name}" was captured (overlay, thesis, peers, chatter and price payloads carry none)`)
  const cores = new Set(src.map((s) => coreOf(s.name)).filter(Boolean))
  const rawNames = src.map((s) => collapse(s.name).toLowerCase())
  const pool = scans.filter((s) => s.opened === null || s.opened === name)
  if (!pool.some((s) => s.opened === name && !s.error)) throw new Error(`no tab of "${name}" was scanned`)
  const groups = new Map()
  const shortened = []
  const seen = new Set()
  for (const s of pool) {
    for (const it of s.items || []) {
      if (!namesSecurity(it.text, cores, rawNames)) continue
      const where = { scope: s.scope, region: it.region, selector: it.sel, dom_text: it.text, rendered: it.rendered }
      const id = JSON.stringify(where)
      if (seen.has(id)) continue
      seen.add(id)
      if (ELLIPSIS.test(it.text)) { shortened.push(where); continue }
      const d = displayOf(it.text)
      if (!groups.has(d)) groups.set(d, [])
      groups.get(d).push(where)
    }
  }
  const distinct = [...groups.entries()].map(([display, where]) => ({ display, occurrences: where.length, where }))
  const ci = new Set(distinct.map((x) => x.display.toLowerCase()))
  const rendered = new Set(distinct.flatMap((x) => x.where.map((w) => displayOf(w.rendered))))
  const scopes = pool.map((s) => `${s.scope}${s.error ? ` (scan failed: ${s.error})` : ''}`)
  if (!distinct.length) throw new Error(`0 visible strings matched the served names ${JSON.stringify(src.map((s) => s.name))} across ${pool.length} scans -- check the matcher`)
  return {
    verdict: distinct.length > 1 ? 'FAIL' : 'PASS',
    detail: `${distinct.length} distinct display string(s) for ${name}: ${distinct.map((x) => `"${x.display}" x${x.occurrences} (${[...new Set(x.where.map((w) => w.scope))].join(', ')})`).join(' / ')}${shortened.length ? `; ${shortened.length} shortened label(s) listed apart` : ''}`,
    data: {
      name, security_key: key, served_names: src, cores: [...cores], distinct, distinct_case_insensitive: ci.size,
      distinct_as_rendered: [...rendered], shortened_labels: shortened, scopes_scanned: scopes,
      rule: 'a visible string names the security when its tokens, less corporate suffixes and "(subject)", equal a served name\'s; "..." labels are listed apart',
    },
  }
}

// ---- the walk (round 53) ----
// walk53.mjs = round35/walk/closewalk35.mjs's head (options, lease, login, request guard, page helpers; unchanged, lines above
// its "the walk" marker) + this tail. Built by round53/walk/build_walk53.py. The ONE REAL RUN of round 53: a local build of the
// round-53 candidate against the live function. Reads:
//   r53-segment <name>    SAUX-43: on the Thesis tab, ONE [data-segment-table]; a served table draws one head cell per served
//                         period label in order and one body row per served row in order, with its source line; a served reason
//                         draws that reason once and no table.
//   r53-sections <name>   SAUX-42: on the Thesis tab, ONE [data-dossier-sections] with the five served fields in order, each
//                         carrying its served state; a served section prints its text and holds one closed opener; an absent
//                         one prints its served reason.
//   r53-freshness         SAUX-41: on /freshness, every Seeking Alpha cell carries the served state and prints the served
//                         sentence; no cell prints "Not collected"; no checked or no-record row is flagged stale.
// Usage (repo root): node <this file> --names "AMD US,ASML NA,NU US" [--base http://localhost:5174]
function R53_PROBE() {
  const clean = (s) => String(s || '').replace(/\s+/g, ' ').trim()
  const seg = [...document.querySelectorAll('[data-segment-table]')].map((e) => ({
    state: e.getAttribute('data-segment-table'),
    head: [...e.querySelectorAll('table[data-segment-table-revenue] thead th')].map((th) => clean(th.innerText)),
    rows: [...e.querySelectorAll('table[data-segment-table-revenue] tbody tr')].map((tr) => clean((tr.querySelector('td') || {}).innerText)),
    operating_rows: e.querySelectorAll('table[data-segment-table-operating] tbody tr').length,
    source: clean((e.querySelector('[data-segment-table-source]') || {}).innerText),
    text: clean(e.innerText).slice(0, 2000),
  }))
  const ds = [...document.querySelectorAll('[data-dossier-sections]')].map((e) => ({
    sections: [...e.querySelectorAll('[data-dossier-section]')].map((s) => ({
      field: s.getAttribute('data-dossier-section'),
      state: s.getAttribute('data-dossier-section-state'),
      openers: s.querySelectorAll('details[data-dossier-section-open]').length,
      open_now: s.querySelectorAll('details[data-dossier-section-open][open]').length,
      text: clean(s.innerText).slice(0, 4000),
    })),
  }))
  return { seg, ds }
}
function FRESH_PROBE() {
  const clean = (s) => String(s || '').replace(/\s+/g, ' ').trim()
  return [...document.querySelectorAll('[data-slot="freshness-table"] tbody tr')].map((tr) => {
    const td = tr.querySelector('td[data-input="seekingalpha"]')
    return {
      name: clean((tr.querySelector('td') || {}).innerText),
      sa_state: td ? td.getAttribute('data-sa-state') : null,
      data_state: td ? td.getAttribute('data-state') : null,
      text: td ? clean(td.innerText) : null,
      sa_flagged: !!tr.querySelector('[data-stale-input="seekingalpha"]'),
    }
  })
}
const norm = (s) => String(s || '').replace(/\s+/g, ' ').trim()

const PLANNED = [...opt.names.flatMap((n) => [`r53-segment ${n}`, `r53-sections ${n}`]), 'r53-freshness']
let holder = null; let armed = false; let browser; let fatal = null
let freshBody = null
try {
  let armOut
  try { armOut = py('arm') } catch (e) {
    const so = e && e.stdout ? String(e.stdout) : ''
    holder = (so.match(/^HOLDER (\S+)/m) || [])[1] || null; armed = !!holder
    throw new Error(`arm failed: ${firstLine((e && e.stderr && String(e.stderr).trim()) || e)}`)
  }
  log(armOut.trim().split('\n').slice(-2).join(' | '))
  holder = (armOut.match(/^HOLDER (\S+)/m) || [])[1] || null; armed = true; armedAt = Date.now()
  const password = py('secret', { UI_WALK_CHILD: '1' })
  try { browser = await chromium.launch({ channel: 'msedge', headless: true }) } catch { browser = await chromium.launch({ headless: true }) }
  const page = await (await browser.newContext({ viewport: { width: 1440, height: 900 } })).newPage()
  page.setDefaultTimeout(30000)
  await page.route('**/*', (route) => {
    const req = route.request(); const m = req.method(); const p = new URL(req.url()).pathname
    if (m === 'GET' || m === 'HEAD' || m === 'OPTIONS' || ADMITTED_POST.some((re) => re.test(p))) return route.continue()
    if (/\/analytics\/ingest$/.test(p)) return route.fulfill({ status: 204, body: '' })
    return route.abort('blockedbyclient')
  })
  page.on('request', (r) => { if (/\/api\/scoped\//.test(r.url())) inflight.add(r) })
  page.on('requestfinished', (r) => inflight.delete(r))
  page.on('requestfailed', (r) => inflight.delete(r))
  page.on('response', async (resp) => {
    let u
    try { u = new URL(resp.url()) } catch { return }
    const p = u.pathname
    if (!/\/api\/scoped\/amgt\//.test(p) || resp.status() !== 200) return
    const body = await resp.json().catch(() => null); if (!body) return
    const data = unwrap(body)
    if (/\/freshness$/.test(p) && u.searchParams.get('view') === 'page') { freshBody = data; return }
    const k = p.match(/\/security\/([^/]+)\/([a-z-]+)$/)
    if (k) { const seg = decodeURIComponent(k[1]); (served.bySeg[seg] = served.bySeg[seg] || {})[k[2]] = data }
  })
  await page.goto(opt.base + '/login', { waitUntil: 'domcontentloaded', timeout: 30000 })
  await page.fill('#email', EMAIL); await page.fill('#password', password.trim()); await page.click('button[type=submit]')
  await page.waitForURL((u) => !/\/login/.test(u.pathname), { timeout: 30000 }).catch(() => {})
  if (/\/login/.test(new URL(page.url()).pathname)) throw new Error('login did not complete')
  log('LOGGED IN')
  await page.goto(opt.base + '/security-analysis', { waitUntil: 'domcontentloaded', timeout: 30000 }); await settle(page, 3000)

  for (const name of opt.names) {
    let ov = null; let openErr = null; let seg = null; let view = null
    try {
      ov = await openName(page, name)
      seg = Object.keys(served.bySeg).find((k) => served.bySeg[k].overlay === ov) || null
      await waitFor(page, () => seg && served.bySeg[seg] && served.bySeg[seg].thesis, 30000).catch(() => {})
      await closeDialogs(page)
      await clickTab(page, 'Thesis')
      await waitTabReady(page, 'thesis')
      await settle(page, 2000)
      await page.screenshot({ path: png(`r53-${slug(name)}-thesis.png`), fullPage: true })
      view = await page.evaluate(R53_PROBE)
    } catch (e) { openErr = e }
    const thesis = seg && served.bySeg[seg] ? served.bySeg[seg].thesis : null
    const base = { name, security_key: seg }

    await read(`r53-segment ${name}`, async () => {
      if (openErr) throw openErr
      if (!thesis) throw new Error('no /thesis response was captured for this name')
      const st = thesis.segment_table
      if (!st) throw new Error('the live /thesis carries no segment_table')
      const f = []
      if (view.seg.length !== 1) f.push(`${view.seg.length} [data-segment-table] element(s) (1 wanted)`)
      const d = view.seg[0] || {}
      if (st.status === 'served') {
        const want = ['Segment', ...st.periods.map((p) => p.label)]
        if (JSON.stringify(d.head) !== JSON.stringify(want)) f.push(`head ${JSON.stringify(d.head)} (served ${JSON.stringify(want)})`)
        if (JSON.stringify(d.rows) !== JSON.stringify(st.rows.map((r) => norm(r.segment)))) f.push(`rows ${JSON.stringify(d.rows)} (served ${JSON.stringify(st.rows.map((r) => r.segment))})`)
        if ((st.operating_income_rows || []).length !== d.operating_rows) f.push(`${d.operating_rows} operating row(s) of ${(st.operating_income_rows || []).length}`)
        if (!d.source || !d.source.includes(st.source.label)) f.push(`source line "${d.source}"`)
      } else if (d.state !== 'none' || !norm(d.text).includes(norm(st.reason))) f.push(`a served reason is not drawn: state ${d.state}, text "${(d.text || '').slice(0, 120)}"`)
      return {
        verdict: f.length ? 'FAIL' : 'PASS',
        detail: f.length ? f.join(' | ') : (st.status === 'served' ? `${d.rows.length} rows x ${d.head.length - 1} columns as served, ${d.operating_rows} operating rows; "${d.source}"` : `the served reason is drawn: "${norm(st.reason)}"`),
        data: { ...base, served_status: st.status, drawn: d },
      }
    })
    await read(`r53-sections ${name}`, async () => {
      if (openErr) throw openErr
      if (!thesis) throw new Error('no /thesis response was captured for this name')
      const ds = thesis.dossier_sections
      if (!Array.isArray(ds)) throw new Error('the live /thesis carries no dossier_sections')
      const f = []
      if (view.ds.length !== 1) f.push(`${view.ds.length} [data-dossier-sections] element(s) (1 wanted)`)
      const got = (view.ds[0] || { sections: [] }).sections
      if (JSON.stringify(got.map((s) => s.field)) !== JSON.stringify(ds.map((e) => e.field))) f.push(`fields ${JSON.stringify(got.map((s) => s.field))}`)
      ds.forEach((e, i) => {
        const s = got[i]; if (!s) return
        if (s.state !== e.status) f.push(`${e.field}: state ${s.state} (served ${e.status})`)
        if (e.status === 'served') {
          if (s.openers !== 1 || s.open_now !== 0) f.push(`${e.field}: ${s.openers} opener(s), ${s.open_now} open`)
          if (!s.text.includes(norm(e.text).slice(0, 200))) f.push(`${e.field}: the served text is not on screen`)
        } else if (!s.text.includes(norm(e.reason))) f.push(`${e.field}: the served reason is not on screen`)
      })
      return {
        verdict: f.length ? 'FAIL' : 'PASS',
        detail: f.length ? f.join(' | ') : `5 of 5 in order (${ds.map((e) => `${e.field}:${e.status}`).join(', ')})`,
        data: { ...base, drawn: got.map((s) => ({ ...s, text: s.text.slice(0, 400) })) },
      }
    })
  }

  await page.goto(opt.base + '/freshness', { waitUntil: 'domcontentloaded', timeout: 30000 })
  await waitFor(page, () => !!freshBody, 60000).catch(() => {})
  await page.waitForSelector('[data-slot="freshness-table"] tbody tr', { timeout: 60000 }).catch(() => {})
  await settle(page, 2000)
  await page.screenshot({ path: png('r53-freshness.png'), fullPage: true })
  const cells = await page.evaluate(FRESH_PROBE)
  await read('r53-freshness', async () => {
    if (!freshBody) throw new Error('no /freshness?view=page response was captured')
    const rows = (freshBody.rows || []).filter((r) => r.covered === true)
    const byName = new Map(cells.map((c) => [c.name, c]))
    const f = []; const tally = {}
    for (const r of rows) {
      const sa = r.seeking_alpha || {}
      const c = byName.get(r.name || r.security_key || 'Unnamed company')
      if (!c) { f.push(`${r.name}: no row drawn`); continue }
      tally[c.sa_state] = (tally[c.sa_state] || 0) + 1
      if (c.sa_state !== sa.state) f.push(`${r.name}: data-sa-state ${c.sa_state} (served ${sa.state})`)
      if (c.text !== norm(sa.sentence)) f.push(`${r.name}: "${c.text}"`)
      if (sa.state !== 'read' && (c.sa_flagged || c.data_state === 'stale')) f.push(`${r.name}: ${sa.state} drawn stale`)
    }
    const nc = cells.filter((c) => /not collected/i.test(c.text || '')).length
    if (nc) f.push(`${nc} cell(s) print Not collected`)
    const examples = ['read', 'checked', 'no_record'].map((s) => { const r = rows.find((x) => (x.seeking_alpha || {}).state === s); return r ? `${r.name}: "${norm(r.seeking_alpha.sentence)}"` : `${s}: none served` })
    return {
      verdict: f.length ? 'FAIL' : 'PASS',
      detail: f.length ? `${f.length} fault(s): ` + f.slice(0, 5).join(' | ') : `${rows.length} of ${rows.length} rows carry the served state and sentence ${JSON.stringify(tally)}; 0 Not collected; e.g. ${examples.join(' // ')}`,
      data: { snapshot: freshBody.snapshot || null, drawn: cells, tally },
    }
  })
} catch (e) {
  fatal = firstLine(e)
  log(`FATAL: ${fatal}`)
} finally {
  if (browser) await browser.close().catch(() => {})
  if (armed) { try { log(py('disarm', {}, holder).trim().split('\n').slice(-3).join(' | ')) } catch (e) { log(`DISARM FAILED -- run: python .claude/skills/ui-walk/ui_walker_account.py disarm ${holder} :: ${firstLine(e)}`) } }
}
for (const id of PLANNED) if (!reads.some((r) => r.id === id)) record(id, 'ERROR', `cause: not reached${fatal ? ` (${fatal})` : ''}`, {})

console.log('')
for (const r of reads) console.log(`${r.verdict} ${r.id} :: ${r.evidence} :: ${r.detail}`)
const n = (v) => reads.filter((r) => r.verdict === v).length
console.log(`READS: ${reads.length} (PASS ${n('PASS')}, FAIL ${n('FAIL')}, ERROR ${n('ERROR')})${fatal ? `; FATAL ${fatal}` : ''}`)
fs.writeFileSync(path.join(OUT, 'walk53.json'), JSON.stringify({ base: opt.base, names: opt.names, fatal, reads }, null, 1))
console.log(`OUT ${OUT}`)
process.exit(n('ERROR') === 0 ? 0 : 1)
