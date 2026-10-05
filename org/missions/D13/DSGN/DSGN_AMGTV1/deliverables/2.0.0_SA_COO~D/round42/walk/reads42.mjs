// reads42.mjs -- DSGN_AMGTV1 round 42 ISSUER READ (issuer 2.0.0_SA_COO~D, 2026-10-05): the Security Analysis SIDEBAR read Andrew
// set for FWD-19's permission limb (record org/tier1_exec/2.0.0_SA_COO/deliverables/ANDREW_DIRECT_20261005_163xZ_SECURITY_ANALYSIS_
// NO_NO_PERMISSION_SCREEN_SIDEBAR_INVISIBLE_FOR_NON_OPAL.md; CTO msgs 29703, 29704): "you dont see a sidebar element for Security
// Analysis if you are not an opal user". No route, redirect or URL-blocking read is graded. reads37.mjs COPIED whole (lease, login,
// request guard, output folder, per-read record discipline); its reads are replaced by two:
//   sidebar-opal-control   the walker as itself (firmId opal-capital): the sidebar shows a 'Security Analysis' link to
//                          /security-analysis (the positive control: the probe can see the item when it is there).
//   sidebar-non-opal       the walker's own /auth/refresh and /auth/me responses rewritten in THIS browser only, user.firmId
//                          -> 'inflection' (a partner firm in src/lib/firmAccess.ts); the portal reloaded on /market: the
//                          sidebar holds >= 1 link (it rendered) and NO link to /security-analysis and no 'Security Analysis'
//                          text. No server write; the rewrite is page.route on the walker's own responses.
// Usage: node <this file> [--base http://localhost:5174]
//
// reads37.mjs -- DSGN_AMGTV1 round 37 ISSUER WALK (issuer 2.0.0_SA_COO~D, 2026-10-05): the reads of FWD-5, FWD-11 and FWD-19
// that rounds 34-36 never reached (round36/COMPLETION_GRADES.round36.json rows FWD-5, FWD-11, FWD-19, all NOT_EVALUATED).
// Built on ../../round35/walk/closewalk35.mjs (itself round34/walk/gapread.mjs + a probe), COPIED, not imported: the same walker
// lease (arm HOLDER, secret by name, holder-only disarm in finally, the login-REFUSED line after disarm), login, request guard
// (GET/HEAD/OPTIONS and login/refresh/logout only; telemetry answered locally), output folder (read-<UTC stamp>/ beside this
// file), per-read record/ERROR discipline and 50-minute lease budget. Its reads are dropped; four new ones replace them.
//
// Usage (repo root; a local build of portal DEV on the live API, `cd portal && bun run dev:live --port 5174`):
//   node <this file> [--base http://localhost:5174] [--names "BA US,AMD US"]
//
// What it reads (PRD prd/DSGN_AMGTV1_PRD.md FWD-5 v0.9 + v0.14, FWD-11, FWD-19):
//   1. fwd5-markers-<name>    press ONE coverage-event marker and ONE earnings marker (if any is drawn) on the timeline
//                             (TimelinePanel.tsx g[data-timeline-marker]); the shared HeroDialog opens on THAT day; its
//                             article rows read headline, publisher and time at rest, with mention count / flags / tier
//                             only behind the closed "More" <details>; Escape closes it; a PNG of the open dialog. Every
//                             request issued between the press and the close is logged: any non-GET (other than the
//                             admitted background /auth/refresh) or any request the guard refused is a FAIL with its URL.
//   2. fwd5-own-first-<name>  "the firm's own harvested publications come first" = brief O5 "Opal Data Harvest publications
//                             lead and the News Scanner supplements". Opens the busiest multi-publisher day by its bar, and
//                             records the served row order (/timeline/day) against the shown order (li[data-timeline-article]),
//                             every served row field that could name an origin, and the publisher codes. Context: the
//                             recent-news card's served feed (overlay `feed`) against its shown [data-feed-item] order.
//   3. fwd11-side-by-side     /security-analysis/<first name>, /market, /positioning, /philosophy on the same build: a full-page
//                             PNG at 1440 each and one JSON of the shared-pattern facts a person compares (panel chrome,
//                             panel header and footer, chart library and the hovered tooltip, empty-state components, type
//                             sizes/weights, ink tokens). CAPTURE ONLY: the person's side-by-side read grades FWD-11.
//   4. fwd19-panels-<name>    the loading and error designed states of the three panels round 32 named -- the timeline, the
//                             identity header, What changed on the Model tab -- ON THE LIVE ROUTE, by intercepting ONLY that
//                             panel's GET (held for loading; a planted 500 for error). Each capture names the component that
//                             rendered: PanelLoading/PanelError/PanelEmpty/PanelNoPermission (the states Frame: data-panel-state
//                             + the Frame's rounded-[4px] w-full bg-surface classes), LOOKALIKE (data-panel-state without the
//                             Frame), or NONE.
//      fwd19-no-permission    PanelNoPermission on a real route: ProtectedRoute.tsx renders RouteNoPermission for a viewer
//                             whose role misses a route gate; /security-analysis is requireDev + requireAdmin (App.tsx:470).
//                             The walker IS admin / opal-capital / Dev, so it clears every gate; the capture rewrites userType
//                             to null in the walker's OWN /auth/refresh and /auth/me responses, in this browser only (no
//                             write anywhere), then opens /security-analysis. Runs LAST.
// Each read writes OUT/<nn>-<read>.json (+ PNGs) and one line: PASS|FAIL|ERROR <read> :: <evidence> :: <detail>.
// ERROR = the read could not run (its cause is the detail). Exit 0 only when no read is ERROR, whatever the grades say.
// Nothing here clicks Refresh, a star, Log Out or any control that writes; the only presses are timeline markers and bars,
// a "More" <details> summary, the Model tab and Escape.
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
const opt = { base: 'http://localhost:5174', names: ['BA US', 'AMD US'] }
for (let i = 0; i < argv.length; i++) {
  if (argv[i] === '--base') opt.base = argv[++i] || opt.base
  else if (argv[i] === '--names') opt.names = list(argv[++i])
}
if (!opt.names.length || !fs.existsSync(ACCOUNT) || !fs.existsSync(path.join(ROOT, 'portal', 'package.json'))) {
  console.error('usage (repo root): node <reads37.mjs> [--base URL] [--names "A,B"]')
  if (!opt.names.length) console.error('ERROR: --names is empty')
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
const unwrap = (d) => (d && d.payload ? d.payload : d)

const LEASE_BUDGET_MS = 50 * 60 * 1000 // the lease lapses at 60 min (ui_walker_account.py MAX_ARMED_MINUTES)
const QUERY_CACHE_KEY = 'OPAL_PORTAL_QUERY_CACHE_v1' // portal src/lib/queryPersister.ts:3 (React Query cache persisted to localStorage)
const HARVEST_PUBLISHERS = ['sa', 'ft', 'wsj', 'bbg', 'barrons'] // publisherNames.ts:2-3, the article.schema.json publisher enum
const SERVED_ARTICLE_FIELDS = ['article_key', 'headline', 'publisher', 'signal_tier', 'mention_count', 'mention_in_title', 'mention_in_lead', 'published_utc', 'published_precision'] // timeline_api.py:125-128
const ORIGIN_LIKE = /source|origin|harvest|scanner|own|provider|channel|feed|house/i
const STATE_COMPONENT = { empty: 'PanelEmpty', loading: 'PanelLoading', error: 'PanelError', 'no-permission': 'PanelNoPermission' }
const slug = (s) => String(s).replace(/[^A-Za-z0-9]+/g, '-').replace(/^-+|-+$/g, '') || 'x'
const firstLine = (e) => String((e && e.message) || e).split('\n')[0]
const cssStr = (s) => `"${String(s).replace(/["\\]/g, '\\$&')}"`
const collapse = (s) => String(s ?? '').replace(/\s+/g, ' ').trim()
const png = (name) => path.join(OUT, name)

// The source lines each read rests on (portal origin/DEV 56b71adb unless named; repo paths otherwise).
const CODE_EVIDENCE = {
  marker_press_is_get_only: [
    'portal src/pages/SecurityAnalysis/components/TimelinePanel.tsx:314-325 -- the marker <g data-timeline-marker data-marker-day role=button> calls onSelectDay(marker.day) on click/Enter/Space',
    'TimelinePanel.tsx:524 -- onSelectDay is setSelectedDay (local state)',
    'TimelinePanel.tsx:666-679 -- selectedDay opens the shared HeroDialog holding <DayDissection> under [data-timeline-selected-day]',
    'TimelinePanel.tsx:450-451, 175-183 -- DayDissection reads useTimelineDay -> apiRequest(timelineDayPath) with NO options',
    'portal src/api/api-client.ts:141-166 -- apiRequest fetch(url, {...options, headers}): no method given, so GET',
    'TimelinePanel.tsx:257-268 -- a day bar rect[data-day-bar] presses the same onSelectDay',
  ],
  day_dialog: [
    'portal src/ui/components/graphic/HeroGraphic.tsx:121-148 -- HeroDialog: the catalyst Dialog (Headless UI, role=dialog, Escape closes) + button[aria-label="Close"]',
    'TimelinePanel.tsx:420-438 -- ArticleRow: headline div, span[data-publisher] -- time span at rest; mention count, title/lead flags and tier inside a closed <details> "More" ([data-article-detail])',
    'TimelinePanel.tsx:660-664 -- [data-timeline-earnings-empty] while no earnings marker is drawn',
  ],
  own_first: [
    'docs/briefs/dsgn-amgtv1-security-analysis-frontend-brief-20260928.md:86-87 (O5) -- "Opal Data Harvest publications lead and the News Scanner supplements"',
    'lib/research/harvest/timeline_api.py:125-128 -- ARTICLE_FIELDS: no origin / own-publication field on a served day row',
    'lib/research/harvest/timeline_api.py:133-140 -- the day order is (tier, mention_count desc, published_utc), the server\'s; TimelinePanel.tsx:403 "never re-sorted here"',
    'portal src/pages/SecurityAnalysis/components/publisherNames.ts:2-3 -- the harvest publisher enum: sa, ft, wsj, bbg, barrons',
  ],
  fwd19_panels: [
    'portal src/ui/components/states/PanelStates.tsx:92-110 -- the Frame every designed state renders: data-panel-state + "flex w-full flex-col rounded-[4px]" + bg-[hsl(var(--bg-surface))]',
    'TimelinePanel.tsx:535-563 -- timeline loading = PanelLoading under [data-timeline-panel="LOADING"]; error = PanelError under [data-timeline-panel="ERROR"] (retry 0, :170)',
    'portal src/pages/SecurityAnalysis/components/SecurityOverlay.tsx:321-351 -- identity header loading = PanelLoading "Loading identity header"; error = PanelError (retry 2, hooks/useLeadPanelApi.ts:136-144)',
    'portal src/pages/SecurityAnalysis/components/model/WhatChangedPanel.tsx:398-408, 473-483 -- What changed loading is a hand-rolled div[data-panel-state="loading"]; its error is a bare <p> (no data-panel-state)',
    'portal src/pages/SecurityAnalysis/tabs/ModelTab.tsx:103-124 -- ModelLoadingState / ModelErrorState: local look-alikes, not the states components',
  ],
  no_permission: [
    'portal src/components/ProtectedRoute.tsx:115-122 -- a signed-in viewer failing requireAdmin / requireInternal / requireDev gets <RouteNoPermission />',
    'ProtectedRoute.tsx:128-136 -- RouteNoPermission = div[data-slot="route-no-permission"] > <PanelNoPermission surface="panel" subject="this page" ...>',
    'portal src/App.tsx:470-471 -- /security-analysis and /security-analysis/:securityKey are requireDev requireAdmin',
    '.claude/skills/ui-walk/ui_walker_account.py:14, 113-114 -- the walker row is role admin, firmId opal-capital, userType Dev: it clears every gate',
    'portal src/contexts/AuthContext.tsx:243-253, 170-201, 109-140 -- on load: POST /auth/refresh; claims from its `user` (else GET /auth/me); userType is "Dev" or null',
    'PanelStates.tsx:41-45 says NO-PERMISSION HAS NO LIVE CONSUMER; ProtectedRoute.tsx:2,131 now consumes it (the header comment is stale)',
  ],
}

// ---- served payloads, captured from the network log ----
const served = { bySeg: {}, days: {} }
const payloadOf = (seg, surface) => (seg && served.bySeg[seg] ? served.bySeg[seg][surface] || null : null)
const overlayFor = (name) => payloadOf(name, 'overlay')
const inflight = new Set()
const refused = [] // every request the guard refused: { method, url, at }
const reqWindow = { on: false, items: [] } // requests issued while a press is being read

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

// closewalk35.mjs, verbatim: the tab-bar button for a label (TabNavigation renders plain buttons).
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

// The markers drawn on the timeline (TimelinePanel.tsx:314-325).
function MARKERS() {
  return [...document.querySelectorAll('g[data-timeline-marker]')].map((g) => ({
    kind: g.getAttribute('data-timeline-marker'),
    day: g.getAttribute('data-marker-day'),
    label: g.getAttribute('aria-label'),
    title: (g.querySelector('title') || {}).textContent || null,
    visible: g.getClientRects().length > 0,
  }))
}

// The open day dialog: the [role=dialog] holding [data-timeline-selected-day=<day>], its hero chrome and every article row.
function DAY_DIALOG(day) {
  const collapse = (s) => String(s || '').replace(/\s+/g, ' ').trim()
  const dlg = [...document.querySelectorAll('[role="dialog"]')].find((d) => d.querySelector(`[data-timeline-selected-day="${CSS.escape(day)}"]`))
  if (!dlg) return null
  const sel = dlg.querySelector('[data-timeline-selected-day]')
  const dis = dlg.querySelector('[data-timeline-dissection]')
  const titleEl = dlg.querySelector('[id^="headlessui-dialog-title"]') || dlg.querySelector('h2')
  const ON_DEMAND = /named once|named \d+ times|mention count not counted|in the headline:|in the lead:|\btier [A-D]\b|\bno tier\b/i
  const rows = [...dlg.querySelectorAll('li[data-timeline-article]')].map((li) => {
    const head = li.querySelector(':scope > div')
    const pub = li.querySelector('span[data-publisher]')
    const meta = pub ? pub.parentElement : null
    const spans = meta ? [...meta.querySelectorAll(':scope > span')] : []
    const det = li.querySelector('details')
    const detail = li.querySelector('[data-article-detail]')
    const atRest = collapse(li.innerText)
    return {
      key: li.getAttribute('data-timeline-article'),
      headline: head ? collapse(head.textContent) : null,
      publisher: pub ? collapse(pub.textContent) : null,
      publisher_code: pub ? pub.getAttribute('data-publisher') : null,
      time: spans.length > 1 ? collapse(spans[spans.length - 1].textContent) : null,
      details_present: !!det,
      details_open_at_rest: det ? det.open : null,
      // Chromium keeps layout boxes inside a closed <details>, so getClientRects() reads non-empty there; checkVisibility() does not.
      detail_visible_at_rest: detail ? (typeof detail.checkVisibility === 'function' ? detail.checkVisibility() : !(det && !det.open)) : null,
      on_demand_text_at_rest: (atRest.match(ON_DEMAND) || [null])[0],
      signal_tier_attr: detail ? detail.getAttribute('data-signal-tier') : null,
      text_at_rest: atRest.slice(0, 300),
    }
  })
  return {
    selected_day: sel ? sel.getAttribute('data-timeline-selected-day') : null,
    dissection: dis ? dis.getAttribute('data-timeline-dissection') : null,
    dissection_day: dis ? dis.getAttribute('data-dissection-day') : null,
    dissection_status: dis ? dis.getAttribute('data-dissection-status') : null,
    dissection_error_cause: dis ? dis.getAttribute('data-timeline-error-cause') : null,
    hero: {
      title: titleEl ? collapse(titleEl.textContent) : null,
      eyebrow_has_opal_capital: /opal capital/i.test(dlg.innerText || ''),
      eyebrow_has_news_timeline: /news timeline/i.test(dlg.innerText || ''),
      close_button: !!dlg.querySelector('button[aria-label="Close"]'),
      text_head: collapse(dlg.innerText).slice(0, 240),
    },
    rows,
    empty_day: !!dlg.querySelector('[data-timeline-day-empty]'),
  }
}

function ROW_DETAIL(key) {
  const li = document.querySelector(`li[data-timeline-article="${CSS.escape(key)}"]`)
  if (!li) return null
  const det = li.querySelector('details')
  const d = li.querySelector('[data-article-detail]')
  const visible = d ? (typeof d.checkVisibility === 'function' ? d.checkVisibility() : !(det && !det.open)) : null
  return { open: det ? det.open : null, visible, text: d ? d.textContent.replace(/\s+/g, ' ').trim() : null }
}

function FEED_ORDER() {
  return [...document.querySelectorAll('[data-feed-item]')].map((e) => e.getAttribute('data-feed-item'))
}

// FWD-19: the designed state(s) inside one panel's scope, each fingerprinted against the states Frame (PanelStates.tsx:92-110).
function STATE_PROBE(scope) {
  const collapse = (s) => String(s || '').replace(/\s+/g, ' ').trim()
  const NAMES = { empty: 'PanelEmpty', loading: 'PanelLoading', error: 'PanelError', 'no-permission': 'PanelNoPermission' }
  let el = null
  let attr = null
  if (scope === 'timeline') { el = document.querySelector('[data-timeline-panel]'); attr = el ? el.getAttribute('data-timeline-panel') : null }
  else if (scope === 'identity') {
    const hit = [...document.querySelectorAll('[data-panel-state]')].find((e) => /identity header/i.test(`${e.getAttribute('aria-label') || ''} ${e.innerText || ''}`))
    el = hit ? hit.parentElement : null
    attr = document.querySelector('[data-identity-card]') ? 'LOADED' : hit ? hit.getAttribute('data-panel-state') : null
  } else if (scope === 'what-changed') {
    // round 39 (CTO list @222ecd916c item 3): round 38 renders a failed probe as its own section[data-what-changed-failed]
    el = document.querySelector('[data-what-changed-probing]') || document.querySelector('section[data-what-changed-failed]') || document.querySelector('section[data-what-changed]')
    attr = el ? (el.hasAttribute('data-what-changed-probing') ? 'PROBING' : el.hasAttribute('data-what-changed-failed') ? 'FAILED' : 'PAIR') : null
  } else if (scope === 'no-permission') {
    el = document.querySelector('[data-slot="route-no-permission"]'); attr = el ? 'route-no-permission' : null
  }
  if (!el) return { scope_found: false, scope_attr: attr, states: [], text: null, page_states: [...document.querySelectorAll('[data-panel-state]')].map((e) => e.getAttribute('data-panel-state')) }
  const stateEls = [...(el.matches('[data-panel-state]') ? [el] : []), ...el.querySelectorAll('[data-panel-state]')]
  const states = stateEls.map((e) => {
    const toks = String(e.getAttribute('class') || '').split(/\s+/)
    const frame = toks.includes('rounded-[4px]') && toks.includes('w-full') && toks.some((t) => t.includes('--bg-surface'))
    const kind = e.getAttribute('data-panel-state')
    return {
      kind,
      component: frame ? (NAMES[kind] || `UNKNOWN_KIND(${kind})`) : 'LOOKALIKE',
      frame_classes: frame,
      class: String(e.getAttribute('class') || '').slice(0, 200),
      role: e.getAttribute('role'),
      aria_label: e.getAttribute('aria-label'),
      skeletons: e.querySelectorAll('.state-skeleton').length,
      retry_button: !!e.querySelector('[data-state-retry]'),
      cause_attr: e.getAttribute('data-state-cause'),
      text: collapse(e.innerText).slice(0, 200),
      visible: e.getClientRects().length > 0,
    }
  })
  return { scope_found: true, scope_attr: attr, states, text: collapse(el.innerText).slice(0, 400) }
}

// FWD-11: the shared-pattern facts of one page, read from computed styles (class signatures from the DEV sources:
// Panel.tsx:89-96, PanelHeader.tsx:59-62, PanelFooter.tsx:87-93, PanelStates.tsx:99-107, DataTooltip.tsx:26).
function STYLE_FACTS() {
  const collapse = (s) => String(s || '').replace(/\s+/g, ' ').trim()
  const root = document.querySelector('main') || document.body
  const cls = (e) => String(e.getAttribute('class') || '')
  const toks = (e) => cls(e).split(/\s+/)
  const vis = (e) => e.getClientRects().length > 0 && getComputedStyle(e).visibility !== 'hidden'
  const pick = (e, props) => { const cs = getComputedStyle(e); const o = {}; for (const p of props) o[p] = cs[p]; return o }
  const BOX = ['backgroundColor', 'borderTopWidth', 'borderTopStyle', 'borderTopColor', 'borderRadius', 'boxShadow', 'paddingTop', 'paddingLeft']
  const TYPE = ['fontFamily', 'fontSize', 'fontWeight', 'letterSpacing', 'textTransform', 'color']
  const all = [...root.querySelectorAll('*')]
  const isPanel = (e) => !e.hasAttribute('data-panel-state') && toks(e).includes('w-full') && toks(e).includes('rounded-[4px]') && /bg-\[hsl\(var\(--bg-(band|surface)\)\)\]/.test(cls(e))
  const isHeader = (e) => toks(e).includes('px-[30px]') && toks(e).includes('py-4') && toks(e).includes('rounded-t-[4px]')
  const isFooter = (e) => toks(e).includes('px-[30px]') && toks(e).includes('py-2') && toks(e).includes('rounded-b-[4px]')
  const panels = all.filter((e) => isPanel(e) && vis(e))
  const headers = all.filter((e) => isHeader(e) && vis(e))
  const footers = all.filter((e) => isFooter(e) && vis(e))
  const area = (e) => { const r = e.getBoundingClientRect(); return r.width * r.height }
  const bigPanels = [...panels].sort((a, b) => area(b) - area(a)).slice(0, 8)
  // Cards that are NOT the shared Panel: bordered, rounded, sizeable boxes.
  const otherCards = all.filter((e) => {
    if (isPanel(e) || e.hasAttribute('data-panel-state') || !vis(e)) return false
    const cs = getComputedStyle(e)
    const r = e.getBoundingClientRect()
    return parseFloat(cs.borderTopWidth) > 0 && parseFloat(cs.borderTopLeftRadius) > 0 && r.width >= 280 && r.height >= 100
  })
  const tuple = (e) => { const cs = getComputedStyle(e); return `${cs.borderTopLeftRadius} | ${cs.borderTopWidth} ${cs.borderTopStyle} ${cs.borderTopColor} | ${cs.backgroundColor} | shadow ${cs.boxShadow}` }
  const hist = (arr) => { const m = new Map(); for (const k of arr) m.set(k, (m.get(k) || 0) + 1); return [...m.entries()].sort((a, b) => b[1] - a[1]).map(([k, n]) => ({ value: k, n })) }
  // Text-bearing leaves: an element with a non-empty direct text node.
  const texty = all.filter((e) => vis(e) && [...e.childNodes].some((n) => n.nodeType === 3 && n.nodeValue.trim()))
  const tokens = {}
  const rootCs = getComputedStyle(document.documentElement)
  for (const t of ['--palette-navy', '--palette-indigo', '--palette-white', '--palette-darkGray', '--palette-mediumGray', '--palette-lightGray', '--bg-surface', '--bg-band', '--bg-header', '--hairline', '--semantic-action-primary', '--status-danger', '--status-warning']) tokens[t] = rootCs.getPropertyValue(t).trim() || null
  const states = [...root.querySelectorAll('[data-panel-state]')].filter(vis).map((e) => {
    const frame = toks(e).includes('rounded-[4px]') && toks(e).includes('w-full') && toks(e).some((t) => t.includes('--bg-surface'))
    return { kind: e.getAttribute('data-panel-state'), frame_classes: frame, text: collapse(e.innerText).slice(0, 120), ...pick(e, ['backgroundColor', 'color', 'borderRadius']) }
  })
  const svgs = [...root.querySelectorAll('svg')].filter((s) => vis(s) && s.getBoundingClientRect().width >= 200 && s.getBoundingClientRect().height >= 80)
  const codeLike = collapse(root.innerText).split(/(?<=[.!?])\s+|\s{2,}/).map((s) => s.trim()).filter(Boolean)
  return {
    url: location.pathname,
    canvas: { body_background: getComputedStyle(document.body).backgroundColor, root_background: rootCs.backgroundColor },
    tokens,
    panels: { count: panels.length, bands: panels.filter((e) => /--bg-band/.test(cls(e))).length, surfaces: panels.filter((e) => /--bg-surface/.test(cls(e))).length,
      largest: bigPanels.map((e) => ({ variant_classes: toks(e).filter((t) => /^bg-|^border|^rounded|^dark-band$/.test(t)).join(' '), ...pick(e, BOX), size: `${Math.round(e.getBoundingClientRect().width)}x${Math.round(e.getBoundingClientRect().height)}` })) },
    panel_headers: { count: headers.length, first: headers.slice(0, 4).map((h) => { const t = h.querySelector('h3'); return { ...pick(h, ['backgroundColor', 'borderBottomWidth', 'borderBottomColor', 'paddingTop', 'paddingLeft', 'borderTopLeftRadius']), title: t ? { text: collapse(t.textContent).slice(0, 60), ...pick(t, TYPE) } : null } }) },
    panel_footers: { count: footers.length, all: footers.slice(0, 12).map((f) => ({ text: collapse(f.innerText).slice(0, 160), time_and_source: /\|/.test(f.innerText || ''), ...pick(f, ['backgroundColor', 'fontSize', 'color', 'paddingLeft']) })) },
    other_cards: { count: otherCards.length, tuples: hist(otherCards.map(tuple)).slice(0, 10) },
    charts: {
      recharts_surfaces: root.querySelectorAll('svg.recharts-surface').length,
      recharts_tooltip_wrappers: root.querySelectorAll('.recharts-tooltip-wrapper').length,
      canvas: root.querySelectorAll('canvas').length,
      highcharts: root.querySelectorAll('.highcharts-container').length,
      plotly: root.querySelectorAll('.js-plotly-plot').length,
      echarts: root.querySelectorAll('[_echarts_instance_]').length,
      other_large_svgs: svgs.filter((s) => !s.classList.contains('recharts-surface')).length,
    },
    empty_states: { count: states.length, designed_frame: states.filter((s) => s.frame_classes).length, lookalike: states.filter((s) => !s.frame_classes).length, all: states.slice(0, 12) },
    type: { families: hist(texty.map((e) => getComputedStyle(e).fontFamily)).slice(0, 4), size_weight: hist(texty.map((e) => `${getComputedStyle(e).fontSize} / ${getComputedStyle(e).fontWeight}`)).slice(0, 14), text_elements: texty.length },
    ink: hist(texty.map((e) => getComputedStyle(e).color)).slice(0, 10),
    code_like_on_face: codeLike.filter((s) => /\b[a-z]+_[a-z0-9_]+\b|_Equity\b|\.json\b|\b[A-Z][A-Z0-9]*_[A-Z0-9_]+\b|s3:\/\//.test(s)).slice(0, 20).map((s) => s.slice(0, 160)),
  }
}

// The tooltip a hover over the page's first recharts chart shows, fingerprinted against DataTooltip (DataTooltip.tsx:26).
function TOOLTIP_FACTS() {
  const collapse = (s) => String(s || '').replace(/\s+/g, ' ').trim()
  const w = [...document.querySelectorAll('.recharts-tooltip-wrapper')].find((e) => e.getClientRects().length > 0 && getComputedStyle(e).visibility !== 'hidden' && (e.innerText || '').trim())
  if (!w) return { shown: false }
  const box = w.querySelector('div[class*="--palette-indigo"]') || w.firstElementChild
  const toks = box ? String(box.getAttribute('class') || '').split(/\s+/) : []
  const cs = box ? getComputedStyle(box) : null
  return {
    shown: true,
    data_tooltip_signature: toks.some((t) => t.includes('--palette-indigo')) && toks.includes('rounded-[4px]') && toks.includes('px-4') && toks.includes('py-3'),
    class: box ? String(box.getAttribute('class') || '').slice(0, 160) : null,
    backgroundColor: cs ? cs.backgroundColor : null, borderRadius: cs ? cs.borderRadius : null, fontFamily: cs ? cs.fontFamily : null,
    text: collapse(w.innerText).slice(0, 200),
  }
}

// ---- Node-side helpers (closewalk35.mjs, verbatim where named) ----
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

async function timelineServed(page, name) {
  await page.waitForSelector('[data-timeline-panel]', { timeout: 30000 }).catch(() => {})
  await page.waitForFunction(() => !document.querySelector('[data-timeline-panel="LOADING"]'), null, { timeout: 30000 }).catch(() => {})
  const st = await page.evaluate(() => { const e = document.querySelector('[data-timeline-panel]'); return e ? e.getAttribute('data-timeline-panel') : null })
  if (st !== 'SERVED') throw new Error(`the timeline of "${name}" is not drawn ([data-timeline-panel="${st}"])`)
}

// Press one marker or bar, read the HeroDialog it opens, open one row's "More", close with Escape. Every request issued between
// the press and the close is kept; the guard's refusals in that window are kept apart.
async function pressAndRead(page, { locator, day, what, key, shot }) {
  reqWindow.items = []; reqWindow.on = true
  const refusedBefore = refused.length
  const t0 = Date.now()
  let via = 'click'
  try {
    await locator.scrollIntoViewIfNeeded({ timeout: 5000 }).catch(() => {})
    await locator.click({ timeout: 5000 }).catch(async () => { via = 'click (force: the hit-test found another element on top)'; await locator.click({ force: true, timeout: 5000 }) })
    const opened = await page.waitForFunction((d) => [...document.querySelectorAll('[role="dialog"]')].some((x) => x.querySelector(`[data-timeline-selected-day="${CSS.escape(d)}"]`)), day, { timeout: 15000 }).then(() => true).catch(() => false)
    let dom = null
    let detailOpened = null
    let pngDialog = null
    if (opened) {
      await page.waitForFunction((d) => { const x = [...document.querySelectorAll('[role="dialog"]')].find((y) => y.querySelector(`[data-timeline-selected-day="${CSS.escape(d)}"]`)); const s = x && x.querySelector('[data-timeline-dissection]'); return !!s && s.getAttribute('data-timeline-dissection') !== 'LOADING' }, day, { timeout: 30000 }).catch(() => {})
      await page.waitForTimeout(700)
      dom = await page.evaluate(DAY_DIALOG, day)
      pngDialog = `${shot}-dialog.png`
      const dlg = page.locator('[role="dialog"]').filter({ has: page.locator(`[data-timeline-selected-day=${cssStr(day)}]`) }).first()
      await dlg.screenshot({ path: png(pngDialog) }).catch(async () => { await page.screenshot({ path: png(pngDialog) }) })
      await page.screenshot({ path: png(`${shot}-page.png`) })
      // On demand: open the first row's "More" (a native <details>, no request), read it, close it again.
      const first = dom && dom.rows[0] ? dom.rows[0].key : null
      if (first) {
        const sum = page.locator(`li[data-timeline-article=${cssStr(first)}] details > summary`).first()
        if (await sum.count()) {
          await sum.click({ timeout: 4000 }).catch(() => {})
          await page.waitForTimeout(300)
          detailOpened = await page.evaluate(ROW_DETAIL, first)
          await page.screenshot({ path: png(`${shot}-more-open.png`) }).catch(() => {})
          await sum.click({ timeout: 4000 }).catch(() => {})
          await page.waitForTimeout(200)
        }
      }
    }
    await page.keyboard.press('Escape')
    await page.waitForTimeout(900)
    const openAfterEscape = await page.evaluate(DIALOG_OPEN)
    if (openAfterEscape) await closeDialogs(page)
    reqWindow.on = false
    const reqs = reqWindow.items.slice()
    const refusedHere = refused.slice(refusedBefore)
    const servedDay = unwrap(served.days[`${key}|${day}`]) || null
    return { what, day, via, opened, dom, png_dialog: pngDialog, png_page: opened ? `${shot}-page.png` : null, detail_on_demand: detailOpened, open_after_escape: openAfterEscape, requests: reqs, refused: refusedHere, served_day: servedDay, ms: Date.now() - t0 }
  } finally { reqWindow.on = false }
}

// The grade of one press: the HeroDialog on that day, rows at rest, the detail on demand, Escape, GET-only.
function pressFaults(p) {
  const f = []
  if (!p.opened) { f.push(`pressing the ${p.what} on ${p.day} opened no dialog on that day`); return f }
  const d = p.dom
  if (!d) { f.push('the dialog could not be read'); return f }
  if (d.selected_day !== p.day) f.push(`the dialog holds day ${d.selected_day}, not ${p.day}`)
  if (!(d.hero.close_button && d.hero.eyebrow_has_opal_capital && d.hero.eyebrow_has_news_timeline)) f.push(`not the shared HeroDialog (Close button ${d.hero.close_button}, "Opal Capital" eyebrow ${d.hero.eyebrow_has_opal_capital}, "News timeline" ${d.hero.eyebrow_has_news_timeline})`)
  if (d.dissection === 'FAILED') f.push(`the day's articles failed to load (${d.dissection_error_cause})`)
  else if (d.dissection !== 'SERVED') f.push(`the day's articles never loaded ([data-timeline-dissection="${d.dissection}"])`)
  for (const r of d.rows) {
    const miss = []
    if (!r.headline || r.headline === '[no headline]') miss.push('headline')
    if (!r.publisher || /unknown publisher|no name for yet/i.test(r.publisher)) miss.push(`publisher ("${r.publisher}")`)
    if (!r.time || /not carried/i.test(r.time)) miss.push(`time ("${r.time}")`)
    if (miss.length) f.push(`row ${r.key}: at rest lacks ${miss.join(', ')}`)
    if (r.details_open_at_rest || r.detail_visible_at_rest) f.push(`row ${r.key}: the mention/flags/tier detail is open at rest`)
    if (r.on_demand_text_at_rest) f.push(`row ${r.key}: "${r.on_demand_text_at_rest}" shows at rest`)
  }
  if (d.rows.length && (!p.detail_on_demand || !p.detail_on_demand.visible)) f.push('the first row\'s "More" did not show the mention/flags/tier detail on demand')
  if (p.open_after_escape) f.push('the dialog stayed open after Escape')
  const nonGet = p.requests.filter((r) => !['GET', 'HEAD', 'OPTIONS'].includes(r.method) && !/\/auth\/refresh$/.test(r.path))
  if (nonGet.length) f.push(`${nonGet.length} non-GET request(s): ${nonGet.map((r) => `${r.method} ${r.url}`).join('; ')}`)
  if (p.refused.length) f.push(`${p.refused.length} request(s) refused by the guard: ${p.refused.map((r) => `${r.method} ${r.url}`).join('; ')}`)
  return f
}

// ---- READ 1: fwd5-markers-<name> ----
async function fwd5Markers(page, name, ov) {
  if (!ov) throw new Error(`no /overlay payload was captured for "${name}"`)
  await closeDialogs(page)
  await timelineServed(page, name)
  const key = ov.security_key
  const tl = unwrap(payloadOf(key, 'timeline') || payloadOf(name, 'timeline'))
  const markers = await page.evaluate(MARKERS)
  const earningsEmpty = await page.evaluate(() => { const e = document.querySelector('[data-timeline-earnings-empty]'); return e ? e.textContent.replace(/\s+/g, ' ').trim() : null })
  const cov = markers.find((m) => m.kind === 'coverage_event' && m.visible)
  const ern = markers.find((m) => m.kind === 'earnings_release' && m.visible)
  const servedEvents = tl && Array.isArray(tl.events) ? tl.events.length : null
  const servedMarkers = tl && Array.isArray(tl.markers) ? tl.markers.map((m) => ({ kind: m.kind, date: m.date, label: m.label ?? null, reason: m.reason ?? null })) : null
  if (!cov && !ern) throw new Error(`no marker is drawn on ${name}'s timeline (served events ${servedEvents}, served markers ${servedMarkers ? servedMarkers.length : 'absent'}; earnings empty state ${earningsEmpty ? `"${earningsEmpty}"` : 'absent'})`)
  const presses = []
  for (const [m, what] of [[cov, 'coverage-event marker'], [ern, 'earnings marker']]) {
    if (!m) continue
    const loc = page.locator(`g[data-timeline-marker=${cssStr(m.kind)}][data-marker-day=${cssStr(m.day)}]`).first()
    const p = await pressAndRead(page, { locator: loc, day: m.day, what, key, shot: `fwd5-${slug(name)}-${m.kind === 'earnings_release' ? 'earnings' : 'coverage'}-${m.day}` })
    p.marker = m
    p.faults = pressFaults(p)
    presses.push(p)
  }
  const faults = presses.flatMap((p) => p.faults.map((x) => `${p.what} ${p.day}: ${x}`))
  const earningsWords = ern ? 'earnings marker pressed' : `no earnings marker drawn${earningsEmpty ? ` (designed empty state: "${earningsEmpty}")` : ' and NO designed empty state'}`
  if (!ern && !earningsEmpty) faults.push('no earnings marker and no [data-timeline-earnings-empty] line')
  return {
    verdict: faults.length ? 'FAIL' : 'PASS',
    detail: `${name}: ${presses.map((p) => `${p.what} ${p.day} -> ${p.opened ? `HeroDialog "${p.dom && p.dom.hero.title}" ${p.dom ? p.dom.rows.length : 0} row(s), ${p.requests.length} request(s), ${p.refused.length} refused` : 'NO DIALOG'}`).join('; ')}; ${earningsWords}${faults.length ? ` -- ${faults.join(' | ')}` : ''}`,
    data: {
      name, security_key: key, markers_drawn: markers, served_event_count: servedEvents, served_markers: servedMarkers, earnings_empty_state: earningsEmpty,
      presses: presses.map((p) => ({ ...p, served_day: p.served_day ? { date: p.served_day.date, data_status: p.served_day.data_status, articles: (p.served_day.articles || []).map((a) => ({ article_key: a.article_key, publisher: a.publisher, headline: a.headline, published_utc: a.published_utc })) } : null })),
      code_evidence: [...CODE_EVIDENCE.marker_press_is_get_only, ...CODE_EVIDENCE.day_dialog],
      rule: 'PASS = each pressed marker opens the shared HeroDialog on its own day; every row shows headline, publisher and time at rest with the mention/flags/tier detail closed; "More" shows it on demand; Escape closes; only GET/HEAD/OPTIONS (or the admitted background /auth/refresh) were issued and the guard refused nothing',
    },
  }
}

// ---- READ 2: fwd5-own-first-<name> ----
async function fwd5OwnFirst(page, name, ov) {
  if (!ov) throw new Error(`no /overlay payload was captured for "${name}"`)
  await closeDialogs(page)
  await timelineServed(page, name)
  const key = ov.security_key
  const tl = unwrap(payloadOf(key, 'timeline') || payloadOf(name, 'timeline'))
  const series = tl && Array.isArray(tl.series) ? tl.series : []
  const withArticles = series.filter((d) => typeof d.articles_total === 'number' && d.articles_total > 0)
  const ranked = [...withArticles].sort((a, b) => (b.publishers_distinct ?? 0) - (a.publishers_distinct ?? 0) || b.articles_total - a.articles_total || (a.date < b.date ? 1 : -1))
  const pickDay = ranked.find((d) => d.articles_total >= 2) || ranked[0]
  if (!pickDay) throw new Error(`${name}'s served timeline has no day with articles (${series.length} served days)`)
  const day = pickDay.date
  const loc = page.locator(`rect[data-day-bar=${cssStr(day)}]`).first()
  if (!(await loc.count())) throw new Error(`no bar is drawn for the served day ${day}`)
  const p = await pressAndRead(page, { locator: loc, day, what: 'day bar', key, shot: `fwd5-ownfirst-${slug(name)}-${day}` })
  const servedDay = p.served_day || unwrap(await waitFor(page, () => served.days[`${key}|${day}`], 10000))
  const servedRows = servedDay && Array.isArray(servedDay.articles) ? servedDay.articles : null
  const shown = p.dom ? p.dom.rows.map((r) => r.key) : []
  const servedOrder = servedRows ? servedRows.map((a) => a.article_key) : []
  const sameOrder = servedRows !== null && shown.length === servedOrder.length && shown.every((k, i) => k === servedOrder[i])
  const fieldsSeen = servedRows ? [...new Set(servedRows.flatMap((a) => Object.keys(a || {})))] : []
  const extraFields = fieldsSeen.filter((f) => !SERVED_ARTICLE_FIELDS.includes(f))
  const originFields = fieldsSeen.filter((f) => ORIGIN_LIKE.test(f))
  const codes = servedRows ? servedRows.map((a) => a.publisher) : []
  const outsideEnum = codes.filter((c) => !HARVEST_PUBLISHERS.includes(c))
  const faults = []
  let basis
  let ownFirst = null
  if (!p.opened || !p.dom) faults.push(`pressing the day bar for ${day} opened no dialog on that day`)
  if (servedRows === null) faults.push(`no /timeline/day payload was captured for ${day}`)
  else if (!sameOrder) faults.push(`shown order differs from served order (shown ${JSON.stringify(shown)}, served ${JSON.stringify(servedOrder)})`)
  if (originFields.length) {
    basis = 'ORIGIN_FIELD'
    const own = (a) => originFields.some((f) => /harvest|own|opal|house/i.test(String(a[f])))
    const flags = servedRows.map(own)
    const firstOther = flags.indexOf(false)
    ownFirst = firstOther === -1 || flags.slice(firstOther).every((x) => !x)
    if (!ownFirst) faults.push(`a non-own row precedes an own row by ${originFields.join('/')} (${JSON.stringify(servedRows.map((a) => originFields.map((f) => a[f]).join('/')))})`)
  } else if (outsideEnum.length) {
    basis = 'UNKNOWN_PUBLISHER'
    faults.push(`no origin field is served and ${outsideEnum.length} row(s) carry a publisher outside the harvest enum (${[...new Set(outsideEnum.map(String))].join(', ')}): own and not-own cannot be told apart`)
  } else {
    basis = 'SINGLE_SOURCE_VACUOUS'
    ownFirst = true
  }
  // Context: the recent-news card's served feed and its shown order.
  const feed = ov.feed || null
  const feedShown = await page.evaluate(FEED_ORDER)
  const feedServed = feed && Array.isArray(feed.items) ? feed.items.map((i) => i.article_key) : []
  const detailBasis = basis === 'SINGLE_SOURCE_VACUOUS'
    ? 'own-first holds only VACUOUSLY: the day route serves Opal Data Harvest rows only (no origin field; every publisher in the harvest enum), so no News Scanner row exists to order'
    : basis === 'ORIGIN_FIELD' ? `own-first by served ${originFields.join('/')}: ${ownFirst ? 'own rows lead' : 'NOT own-first'}` : 'own-first NOT READABLE'
  return {
    verdict: faults.length ? 'FAIL' : 'PASS',
    detail: `${name} ${day} (${servedRows ? servedRows.length : '?'} served rows, publishers ${[...new Set(codes.map(String))].join('/') || 'none'}): shown order ${sameOrder ? '==' : '!='} served order; ${detailBasis}${faults.length ? ` -- ${faults.join(' | ')}` : ''}`,
    data: {
      name, security_key: key, day, day_choice: 'the served day with the most distinct publishers, then the most articles (>= 2 where any)', day_series_row: pickDay,
      own_first_basis: basis, own_first: ownFirst,
      served_order: servedRows ? servedRows.map((a) => ({ article_key: a.article_key, publisher: a.publisher, signal_tier: a.signal_tier, mention_count: a.mention_count, published_utc: a.published_utc, headline: a.headline })) : null,
      shown_order: p.dom ? p.dom.rows.map((r) => ({ key: r.key, publisher: r.publisher, publisher_code: r.publisher_code, headline: r.headline, time: r.time })) : null,
      same_order: sameOrder, served_row_fields: fieldsSeen, fields_beyond_timeline_api: extraFields, origin_like_fields: originFields, publisher_codes_outside_harvest_enum: outsideEnum,
      press: { via: p.via, opened: p.opened, png_dialog: p.png_dialog, png_page: p.png_page, requests: p.requests, refused: p.refused, open_after_escape: p.open_after_escape },
      recent_news_card: feed ? { source: feed.source ?? null, order: feed.order ?? null, coverage_status: feed.coverage_status ?? null, served_items: (feed.items || []).map((i) => ({ article_key: i.article_key, publisher: i.publisher, published_at: i.published_at })), shown_order: feedShown, same_order: feedShown.length === feedServed.length && feedShown.every((k, i) => k === feedServed[i]) } : null,
      meaning: 'the PRD ACCEPT "the firm\'s own harvested publications come first" (FWD-5) traces to brief O5: "Opal Data Harvest publications lead and the News Scanner supplements"',
      code_evidence: CODE_EVIDENCE.own_first,
    },
  }
}

// ---- READ 3: fwd11-side-by-side ----
async function fwd11Read(page) {
  const name = opt.names[0]
  const pages = [
    { id: 'security-analysis', path: `/security-analysis/${encodeURIComponent(name)}`, label: `Security Analysis (${name})` },
    { id: 'market', path: '/market', label: 'Market' },
    { id: 'positioning', path: '/positioning', label: 'Positioning' },
    { id: 'philosophy', path: '/philosophy', label: 'Philosophy' },
  ]
  const out = []
  for (const pg of pages) {
    const row = { page: pg.label, path: pg.path }
    try {
      await page.goto(opt.base + pg.path, { waitUntil: 'domcontentloaded', timeout: 30000 })
      await settle(page, 3000)
      if (pg.id === 'security-analysis') { await page.waitForSelector('[data-identity-card]', { timeout: 30000 }).catch(() => {}); await page.waitForFunction(() => !document.querySelector('[data-timeline-panel="LOADING"]'), null, { timeout: 30000 }).catch(() => {}); await settle(page, 1500) }
      await closeDialogs(page)
      row.landed_at = new URL(page.url()).pathname
      row.png = `fwd11-${pg.id}-1440.png`
      await page.screenshot({ path: png(row.png), fullPage: true })
      row.facts = await page.evaluate(STYLE_FACTS)
      const chart = page.locator('main .recharts-wrapper').first()
      if (await chart.count()) {
        const box = await chart.boundingBox().catch(() => null)
        if (box) {
          await chart.scrollIntoViewIfNeeded({ timeout: 4000 }).catch(() => {})
          const b2 = (await chart.boundingBox().catch(() => null)) || box
          await page.mouse.move(b2.x + b2.width * 0.6, b2.y + b2.height * 0.5)
          await page.waitForTimeout(700)
          row.tooltip = await page.evaluate(TOOLTIP_FACTS)
          if (row.tooltip.shown) { row.png_tooltip = `fwd11-${pg.id}-tooltip.png`; await page.screenshot({ path: png(row.png_tooltip) }) }
          await page.mouse.move(2, 2)
        }
      } else row.tooltip = { shown: false, why: 'no recharts chart on the page' }
    } catch (e) { row.error = firstLine(e) }
    out.push(row)
  }
  const ok = out.filter((r) => !r.error && r.png)
  if (!ok.length) throw new Error(`no page captured (${out.map((r) => `${r.page}: ${r.error}`).join('; ')})`)
  // The compared facts: each one's value per page, and which facts differ.
  const per = (f) => Object.fromEntries(ok.map((r) => [r.page, f(r)]))
  const compared = {
    panel_radius: per((r) => [...new Set(r.facts.panels.largest.map((p) => p.borderRadius))]),
    panel_border: per((r) => [...new Set(r.facts.panels.largest.map((p) => `${p.borderTopWidth} ${p.borderTopStyle} ${p.borderTopColor}`))]),
    panel_background: per((r) => [...new Set(r.facts.panels.largest.map((p) => p.backgroundColor))]),
    panel_shadow: per((r) => [...new Set(r.facts.panels.largest.map((p) => p.boxShadow))]),
    panel_counts: per((r) => `${r.facts.panels.count} Panel (${r.facts.panels.bands} band, ${r.facts.panels.surfaces} surface); ${r.facts.other_cards.count} other bordered card(s)`),
    header_title_type: per((r) => [...new Set(r.facts.panel_headers.first.map((h) => (h.title ? `${h.title.fontSize}/${h.title.fontWeight} ${h.title.textTransform} ${h.title.letterSpacing}` : 'no h3')))]),
    footers: per((r) => `${r.facts.panel_footers.count} footer(s), ${r.facts.panel_footers.all.filter((f) => f.time_and_source).length} read "time | source"`),
    chart_library: per((r) => Object.entries(r.facts.charts).filter(([, n]) => n > 0).map(([k, n]) => `${k} ${n}`).join(', ') || 'none'),
    tooltip: per((r) => (r.tooltip && r.tooltip.shown ? `${r.tooltip.data_tooltip_signature ? 'DataTooltip' : 'NOT DataTooltip'} ${r.tooltip.backgroundColor}` : 'none shown')),
    empty_states: per((r) => `${r.facts.empty_states.count} state(s): ${r.facts.empty_states.designed_frame} designed Frame, ${r.facts.empty_states.lookalike} look-alike`),
    type_top: per((r) => r.facts.type.size_weight.slice(0, 5).map((x) => x.value)),
    font_family: per((r) => r.facts.type.families.map((x) => x.value)),
    ink_top: per((r) => r.facts.ink.slice(0, 4).map((x) => x.value)),
    canvas: per((r) => r.facts.canvas.body_background),
    code_like_on_face: per((r) => r.facts.code_like_on_face.length),
  }
  const differs = Object.entries(compared).filter(([k, v]) => !['panel_counts', 'footers', 'code_like_on_face', 'type_top', 'ink_top'].includes(k) && new Set(Object.values(v).map((x) => JSON.stringify(x))).size > 1).map(([k]) => k)
  return {
    verdict: ok.length === pages.length ? 'PASS' : 'ERROR',
    detail: `CAPTURE ONLY -- the person's side-by-side read grades FWD-11: ${ok.length} of ${pages.length} pages captured at 1440 (${ok.map((r) => r.png).join(', ')}); facts that differ across pages: ${differs.join(', ') || 'none'}${out.some((r) => r.error) ? `; failed: ${out.filter((r) => r.error).map((r) => `${r.page}: ${r.error}`).join('; ')}` : ''}`,
    data: { viewport: '1440x900, full-page PNG', pages: out, compared, differs, note: 'class signatures: Panel.tsx:89-96, PanelHeader.tsx:59-62, PanelFooter.tsx:87-93, PanelStates.tsx:99-107, DataTooltip.tsx:26 (portal origin/DEV 56b71adb)' },
  }
}

// ---- READ 4: fwd19-panels-<name> ----
const PANELS = [
  { id: 'timeline', label: 'the timeline', re: /\/api\/scoped\/amgt\/security\/[^/]+\/timeline$/, tab: null, scope: 'timeline' },
  { id: 'identity-header', label: 'the identity header', re: /\/api\/scoped\/amgt\/security\/[^/]+\/overlay$/, tab: null, scope: 'identity' },
  { id: 'what-changed', label: 'What changed (Model tab)', re: /\/api\/scoped\/amgt\/security\/[^/]+\/compare$/, tab: 'Model', scope: 'what-changed' },
]

// Intercept ONLY the panel's GET: 'loading' holds it until the capture is taken, then lets it through; 'error' answers a 500.
// Anything else (another path, or a non-GET on that path) falls back to the request guard.
async function withIntercept(page, re, mode, fn) {
  let release
  const held = new Promise((r) => { release = r })
  const hits = []
  const match = (url) => re.test(url.pathname)
  const handler = async (route) => {
    const req = route.request()
    if (req.method() !== 'GET') return route.fallback()
    hits.push({ url: req.url(), mode, at: new Date().toISOString() })
    if (mode === 'error') return route.fulfill({ status: 500, contentType: 'application/json', body: JSON.stringify({ message: 'reads37 planted 500 (walk intercept, no server call made)' }) })
    await Promise.race([held, new Promise((r) => setTimeout(r, 60000))])
    return route.continue().catch(() => {})
  }
  await page.route(match, handler)
  try { return await fn(hits) } finally { release(); await page.unroute(match, handler).catch(() => {}) }
}

async function captureState(page, name, panel, mode) {
  return withIntercept(page, panel.re, mode, async (hits) => {
    // A fresh document with the persisted query cache dropped (init script), so the panel's GET is really issued.
    await page.goto(`${opt.base}/security-analysis/${encodeURIComponent(name)}?r37_fresh=1`, { waitUntil: 'domcontentloaded', timeout: 30000 })
    if (panel.scope !== 'identity') await page.waitForSelector('[data-identity-card]', { timeout: 40000 }).catch(() => {})
    let tabVia = null
    if (panel.tab) { await page.waitForTimeout(800); tabVia = await clickTab(page, panel.tab) }
    const want = (pr) => {
      if (!pr.scope_found) return false
      if (mode === 'loading') return pr.states.some((s) => s.kind === 'loading')
      return pr.states.some((s) => s.kind === 'error') || /could not be loaded/i.test(pr.text || '')
    }
    let probe = null
    const t0 = Date.now()
    while (Date.now() - t0 < 45000) {
      probe = await page.evaluate(STATE_PROBE, panel.scope)
      if (want(probe)) break
      await page.waitForTimeout(400)
    }
    const shot = `fwd19-${slug(name)}-${panel.id}-${mode}`
    const h = (await page.evaluateHandle((scope) => {
      if (scope === 'timeline') return document.querySelector('[data-timeline-panel]')
      if (scope === 'identity') { const x = [...document.querySelectorAll('[data-panel-state]')].find((e) => /identity header/i.test(`${e.getAttribute('aria-label') || ''} ${e.innerText || ''}`)); return x ? x.parentElement : null }
      return document.querySelector('[data-what-changed-probing]') || document.querySelector('section[data-what-changed-failed]') || document.querySelector('section[data-what-changed]')
    }, panel.scope)).asElement()
    let pngPanel = null
    if (h) { pngPanel = `${shot}-panel.png`; await h.screenshot({ path: png(pngPanel) }).catch(() => { pngPanel = null }) }
    await page.screenshot({ path: png(`${shot}-page.png`), fullPage: true })
    const match = probe ? probe.states.find((s) => s.kind === mode) : null
    let grade
    if (!hits.length) grade = 'NOT_EXERCISED'
    else if (match && match.component === STATE_COMPONENT[mode]) grade = 'DESIGNED'
    else if (match) grade = 'LOOKALIKE'
    else grade = 'NONE'
    const seg = name
    const versions = unwrap(payloadOf(seg, 'versions'))
    return {
      panel: panel.label, mode, grade, component: match ? match.component : null, intercepted: hits, tab_found_by: tabVia,
      probe, png_panel: pngPanel, png_page: `${shot}-page.png`,
      model_versions_served: panel.id === 'what-changed' ? (versions && Array.isArray(versions.versions) ? versions.versions.length : null) : undefined,
    }
  })
}

async function fwd19Panels(page, name) {
  const caps = []
  for (const panel of PANELS) {
    for (const mode of ['loading', 'error']) {
      try { caps.push(await captureState(page, name, panel, mode)) } catch (e) { caps.push({ panel: panel.label, mode, grade: 'NOT_EXERCISED', error: firstLine(e) }) }
    }
  }
  const notRun = caps.filter((c) => c.grade === 'NOT_EXERCISED')
  const bad = caps.filter((c) => c.grade === 'LOOKALIKE' || c.grade === 'NONE')
  const line = caps.map((c) => `${c.panel} ${c.mode}: ${c.grade}${c.component ? ` (${c.component})` : ''}`).join('; ')
  return {
    verdict: notRun.length ? 'ERROR' : bad.length ? 'FAIL' : 'PASS',
    detail: `${name}: ${line}${notRun.length ? ` -- not exercised: ${notRun.map((c) => `${c.panel} ${c.mode}${c.error ? ` (${c.error})` : c.model_versions_served !== undefined ? ` (the intercepted GET never fired; versions served: ${c.model_versions_served})` : ' (the intercepted GET never fired)'}`).join('; ')}` : ''}`,
    data: {
      name, captures: caps,
      method: 'each capture is a fresh load of /security-analysis/<name>?r37_fresh=1 (an init script drops the persisted query cache) with ONE page.route on that panel\'s GET: loading = the request held until the PNG is taken, then continued; error = route.fulfill status 500. No other request is touched; a non-GET falls back to the request guard.',
      grades: 'DESIGNED = the src/ui/components/states component for that state (data-panel-state + the Frame classes); LOOKALIKE = data-panel-state without the Frame; NONE = no data-panel-state of that kind in the panel; NOT_EXERCISED = the intercepted GET never fired',
      code_evidence: CODE_EVIDENCE.fwd19_panels,
    },
  }
}

// ---- READ 5: fwd19-no-permission (LAST: it rewrites the walker's own auth responses in this browser) ----
async function noPermRead(page) {
  const name = opt.names[0]
  const rewrites = []
  const match = (url) => /\/auth\/(refresh|me)$/.test(url.pathname)
  const handler = async (route) => {
    const req = route.request()
    const m = req.method()
    const p = new URL(req.url()).pathname
    if (!(m === 'GET' || (m === 'POST' && /\/auth\/refresh$/.test(p)))) return route.fallback()
    const resp = await route.fetch()
    const text = await resp.text()
    let body = null
    try { body = JSON.parse(text) } catch { body = null }
    const headers = { ...resp.headers() }
    delete headers['content-length']; delete headers['content-encoding']
    if (body && body.user && typeof body.user === 'object') {
      rewrites.push({ method: m, path: p, status: resp.status(), userType_before: body.user.userType ?? null, userType_after: null, role: body.user.role ?? null, firmId: body.user.firmId ?? null })
      body.user = { ...body.user, userType: null }
      return route.fulfill({ status: resp.status(), headers, body: JSON.stringify(body) })
    }
    rewrites.push({ method: m, path: p, status: resp.status(), note: 'no user object in the body; passed through unchanged' })
    return route.fulfill({ status: resp.status(), headers, body: text })
  }
  await page.route(match, handler)
  try {
    await page.goto(`${opt.base}/security-analysis/${encodeURIComponent(name)}`, { waitUntil: 'domcontentloaded', timeout: 30000 })
    await page.waitForSelector('[data-slot="route-no-permission"], [data-identity-card]', { timeout: 40000 }).catch(() => {})
    await page.waitForTimeout(1000)
    const probe = await page.evaluate(STATE_PROBE, 'no-permission')
    const shot = 'fwd19-no-permission-security-analysis'
    await page.screenshot({ path: png(`${shot}-page.png`), fullPage: true })
    const el = page.locator('[data-slot="route-no-permission"]').first()
    let pngPanel = null
    if (await el.count()) { pngPanel = `${shot}-panel.png`; await el.screenshot({ path: png(pngPanel) }).catch(() => { pngPanel = null }) }
    const landed = new URL(page.url()).pathname
    const identityRendered = await page.evaluate(() => !!document.querySelector('[data-identity-card]'))
    const st = probe.states.find((s) => s.kind === 'no-permission')
    const rewrote = rewrites.filter((r) => 'userType_before' in r)
    if (!rewrote.length) throw new Error(`no /auth/refresh or /auth/me response carried a user object to rewrite (${rewrites.length} auth response(s) seen) -- the simulated viewer was never set up`)
    const faults = []
    if (!st) faults.push(`no [data-panel-state="no-permission"] on ${landed} (identity card rendered: ${identityRendered}; page states: ${JSON.stringify(probe.page_states || probe.states.map((s) => s.kind))})`)
    else if (st.component !== 'PanelNoPermission') faults.push(`the no-permission state is a ${st.component}, not PanelNoPermission`)
    return {
      verdict: faults.length ? 'FAIL' : 'PASS',
      detail: `${landed}: ${st ? `${st.component} "${st.text}"` : 'NO no-permission state'} for a SIMULATED non-Dev viewer (userType rewritten to null in ${rewrote.length} of the walker's own auth response(s), this browser only); the walker itself (admin, opal-capital, Dev) clears every gate${faults.length ? ` -- ${faults.join(' | ')}` : ''}`,
      data: { route: '/security-analysis/:securityKey (App.tsx:471, requireDev requireAdmin)', landed, rewrites, probe, png_page: `${shot}-page.png`, png_panel: pngPanel, identity_rendered: identityRendered, code_evidence: CODE_EVIDENCE.no_permission,
        why_simulated: 'no page path shows PanelNoPermission to the walker: its row is role admin, firmId opal-capital, userType Dev (ui_walker_account.py:14, 113-114), which clears requireAdmin, requireInternal and requireDev (ProtectedRoute.tsx:118-120). The state IS reachable on a real route for a viewer lacking a gate; the capture stands in that viewer by rewriting userType in the walker\'s own auth responses, in-browser only.' },
    }
  } finally { await page.unroute(match, handler).catch(() => {}) }
}

// ---- round 42: the sidebar read (Andrew 2026-10-05 ~16:3xZ) ----
const SIDEBAR_PROBE = () => {
  const navs = Array.from(document.querySelectorAll('nav, aside'))
  const links = navs.flatMap((n) => Array.from(n.querySelectorAll('a[href]')))
  const hrefs = links.map((a) => new URL(a.getAttribute('href'), location.href).pathname)
  const texts = navs.map((n) => n.innerText || '').join(' | ')
  return { link_count: links.length, hrefs, sa_links: hrefs.filter((h) => h.startsWith('/security-analysis')).length,
    sa_text: /Security Analysis/i.test(texts), path: location.pathname }
}
async function sidebarRead(page, asFirm) {
  const rewrites = []
  const match = (url) => /\/auth\/(refresh|me)$/.test(url.pathname)
  const handler = async (route) => {
    const req = route.request(); const m = req.method(); const p = new URL(req.url()).pathname
    if (!(m === 'GET' || (m === 'POST' && /\/auth\/refresh$/.test(p)))) return route.fallback()
    const resp = await route.fetch(); const text = await resp.text()
    let body = null; try { body = JSON.parse(text) } catch { body = null }
    const headers = { ...resp.headers() }; delete headers['content-length']; delete headers['content-encoding']
    if (body && body.user && typeof body.user === 'object') {
      rewrites.push({ method: m, path: p, status: resp.status(), firmId_before: body.user.firmId ?? null, firmId_after: asFirm })
      body.user = { ...body.user, firmId: asFirm }
      return route.fulfill({ status: resp.status(), headers, body: JSON.stringify(body) })
    }
    rewrites.push({ method: m, path: p, status: resp.status(), note: 'no user object in the body; passed through unchanged' })
    return route.fulfill({ status: resp.status(), headers, body: text })
  }
  if (asFirm) await page.route(match, handler)
  try {
    await page.goto(`${opt.base}/market`, { waitUntil: 'domcontentloaded', timeout: 30000 })
    await page.waitForSelector('nav a[href], aside a[href]', { timeout: 40000 }).catch(() => {})
    await page.waitForTimeout(2000)
    const probe = await page.evaluate(SIDEBAR_PROBE)
    const shot = asFirm ? 'sidebar-non-opal' : 'sidebar-opal-control'
    await page.screenshot({ path: png(`${shot}.png`), fullPage: false })
    const faults = []
    if (asFirm) {
      const rewrote = rewrites.filter((r) => 'firmId_before' in r)
      if (!rewrote.length) throw new Error(`no /auth/refresh or /auth/me response carried a user object to rewrite (${rewrites.length} seen) -- the simulated viewer was never set up`)
      if (probe.link_count === 0) faults.push('the sidebar rendered no link (no positive evidence it rendered)')
      if (probe.sa_links) faults.push(`${probe.sa_links} sidebar link(s) to /security-analysis`)
      if (probe.sa_text) faults.push('"Security Analysis" text in the sidebar')
    } else {
      if (!probe.sa_links) faults.push('the control shows NO Security Analysis link (the probe cannot see the item)')
    }
    return {
      verdict: faults.length ? 'FAIL' : 'PASS',
      detail: asFirm
        ? `firmId rewritten to '${asFirm}' in ${rewrites.filter((r) => 'firmId_before' in r).length} auth response(s), this browser only; on ${probe.path} the sidebar holds ${probe.link_count} link(s), ${probe.sa_links} to /security-analysis, Security Analysis text: ${probe.sa_text}${faults.length ? ' -- ' + faults.join(' | ') : ''}`
        : `the walker as itself (opal-capital) on ${probe.path}: ${probe.link_count} sidebar link(s), ${probe.sa_links} to /security-analysis${faults.length ? ' -- ' + faults.join(' | ') : ''}`,
      data: { as_firm: asFirm, rewrites, probe, png: `${shot}.png`,
        code_evidence: ['portal src/App.tsx nav entry /security-analysis requiresTier internal (round 40)', 'App.tsx nav filter: isPathAllowedForFirm(claims?.firmId, item.path), then hasAccess(item.requiresTier)', 'src/lib/firmAccess.ts: no partner allowlist names /security-analysis'] },
    }
  } finally { if (asFirm) await page.unroute(match, handler).catch(() => {}) }
}

async function rogHeaderRead(page, name) {
  await page.goto(`${opt.base}/security-analysis`, { waitUntil: 'domcontentloaded', timeout: 30000 }); await settle(page, 3000)
  await openName(page, name)
  await page.waitForSelector('[data-key-figures]', { timeout: 30000 })
  const tiles = await page.evaluate(() => Array.from(document.querySelectorAll('[data-key-figures] [data-card-figure]')).map((t) => ({
    key: t.getAttribute('data-card-figure'), state: t.getAttribute('data-card-figure-state'),
    text: (t.innerText || '').replace(/\s+/g, ' ').trim(),
    tooltip: (t.querySelector('[role=tooltip]') || {}).textContent || null })))
  await page.locator('[data-key-figures]').first().screenshot({ path: png('rog-header.png') }).catch(() => {})
  const absent = tiles.filter((t) => t.state === 'ABSENT')
  const faults = []
  if (tiles.length < 7) faults.push(`${tiles.length} tiles (7 wanted)`)
  if (absent.some((t) => /\d{2,}/.test(t.text.replace(/\b(19|20)\d\d\b/g, '')))) faults.push('a number in an absent tile')
  return { verdict: faults.length ? 'FAIL' : 'PASS',
    detail: `${name}: ${tiles.length} tiles, ${absent.length} with a served reason: ${absent.map((t) => t.text).join(' / ')}${faults.length ? ' -- ' + faults.join(' | ') : ''}`,
    data: { tiles, png: 'rog-header.png' } }
}

// ---- the walk ----
const PLANNED = ['rog-header', 'sidebar-opal-control', 'sidebar-non-opal']
let holder = null; let armed = false; let browser; let fatal = null; let disarmOut = null; let loginRefused = null
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
  // fwd19 only: a document opened with ?r37_fresh drops the persisted React Query cache before the app reads it.
  await page.addInitScript((k) => { try { if (new URLSearchParams(location.search).has('r37_fresh')) window.localStorage.removeItem(k) } catch (e) { /* storage blocked: the read then finds the GET never fired */ } }, QUERY_CACHE_KEY)
  await page.route('**/*', (route) => {
    const req = route.request(); const m = req.method(); const p = new URL(req.url()).pathname
    if (m === 'GET' || m === 'HEAD' || m === 'OPTIONS' || ADMITTED_POST.some((re) => re.test(p))) return route.continue()
    if (/\/analytics\/ingest$/.test(p)) return route.fulfill({ status: 204, body: '' })
    refused.push({ method: m, url: req.url(), at: new Date().toISOString() })
    return route.abort('blockedbyclient')
  })
  page.on('request', (r) => {
    if (/\/api\/scoped\//.test(r.url())) inflight.add(r)
    if (reqWindow.on) { let p = ''; try { p = new URL(r.url()).pathname } catch { /* not a URL */ } if (!/\/analytics\/ingest$/.test(p)) reqWindow.items.push({ method: r.method(), url: r.url(), path: p, at: new Date().toISOString() }) }
  })
  page.on('requestfinished', (r) => inflight.delete(r))
  page.on('requestfailed', (r) => inflight.delete(r))
  page.on('response', async (resp) => {
    let u
    try { u = new URL(resp.url()) } catch { return }
    const p = u.pathname
    if (!/\/api\/scoped\/amgt\//.test(p) || resp.status() !== 200) return
    const body = await resp.json().catch(() => null); if (!body) return
    const data = unwrap(body)
    let k = p.match(/\/security\/([^/]+)\/timeline\/day\/([^/]+)$/)
    if (k) { served.days[`${decodeURIComponent(k[1])}|${decodeURIComponent(k[2])}`] = data; return }
    k = p.match(/\/security\/([^/]+)\/([a-z-]+)$/)
    if (k) { const seg = decodeURIComponent(k[1]); (served.bySeg[seg] = served.bySeg[seg] || {})[k[2]] = data }
  })
  await page.goto(opt.base + '/login', { waitUntil: 'domcontentloaded', timeout: 30000 })
  await page.fill('#email', EMAIL); await page.fill('#password', password.trim()); await page.click('button[type=submit]')
  await page.waitForURL((u) => !/\/login/.test(u.pathname), { timeout: 30000 }).catch(() => {})
  if (/\/login/.test(new URL(page.url()).pathname)) throw new Error('login did not complete')
  log('LOGGED IN')
  await page.goto(opt.base + '/security-analysis', { waitUntil: 'domcontentloaded', timeout: 30000 }); await settle(page, 3000)

  // Round 42: the sidebar, as the walker (control) and then as a simulated partner-firm viewer.
  await read('rog-header', () => rogHeaderRead(page, 'ROG SW'))
  await read('sidebar-opal-control', () => sidebarRead(page, null))
  await read('sidebar-non-opal', () => sidebarRead(page, 'inflection'))
} catch (e) {
  fatal = firstLine(e)
  log(`FATAL: ${fatal}`)
} finally {
  if (browser) await browser.close().catch(() => {})
  if (armed) {
    try {
      disarmOut = py('disarm', {}, holder)
      log(disarmOut.trim().split('\n').slice(-3).join(' | '))
    } catch (e) {
      disarmOut = `${e && e.stdout ? String(e.stdout) : ''}${e && e.stderr ? String(e.stderr) : ''}`
      log(`DISARM FAILED -- run: python .claude/skills/ui-walk/ui_walker_account.py disarm ${holder}`)
    }
    const m = String(disarmOut || '').match(/LOGIN WITH THE WALK PASSWORD AFTER DISARM:.*->\s*(NOT REFUSED|REFUSED)/)
    loginRefused = m ? m[1] === 'REFUSED' : null
    log(`LEASE: login after disarm ${loginRefused === true ? 'REFUSED' : loginRefused === false ? 'NOT REFUSED -- ESCALATE' : 'UNREAD (no REFUSED line in the disarm output)'}`)
  }
}

for (const id of PLANNED) if (!reads.some((r) => r.id === id)) record(id, 'ERROR', `cause: not reached${fatal ? ` (${fatal})` : ''}`, {})

console.log('')
for (const r of reads) console.log(`${r.verdict} ${r.id} :: ${r.evidence} :: ${r.detail}`)
const n = (v) => reads.filter((r) => r.verdict === v).length
console.log(`READS: ${reads.length} (PASS ${n('PASS')}, FAIL ${n('FAIL')}, ERROR ${n('ERROR')})${fatal ? `; FATAL ${fatal}` : ''}`)
fs.writeFileSync(path.join(OUT, 'reads37.json'), JSON.stringify({
  base: opt.base, names: opt.names, fatal, reads,
  lease: { holder, armed, login_refused_after_disarm: loginRefused, disarm_tail: disarmOut ? String(disarmOut).trim().split('\n').slice(-3) : null },
  guard_refused: refused,
  served: { security_segments: Object.fromEntries(Object.entries(served.bySeg).map(([k, v]) => [k, Object.keys(v)])), timeline_days: Object.keys(served.days).length },
}, null, 1))
console.log(`OUT ${OUT}`)
process.exit(n('ERROR') === 0 ? 0 : 1)
