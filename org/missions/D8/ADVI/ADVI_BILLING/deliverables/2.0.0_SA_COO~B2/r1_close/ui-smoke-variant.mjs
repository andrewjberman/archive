/**
 * ui-smoke.mjs -- headless screenshot of a portal route, no credentials needed.
 *
 * The visual-verification instrument behind the /frontend-dev skill (see portal/CLAUDE.md
 * "Verification law"). Renders a route against the local vite dev server with a stubbed
 * auth session and saves a full-page PNG for the agent to READ. A grep cannot see contrast;
 * this can.
 *
 * Usage:
 *   node scripts/ui-smoke.mjs <route> <outfile.png> [--port 5175] [--fixtures fixtures.json]
 *                            [--token <jwt|@file>] [--click <name>]... [--fill <aria-label>=<text>]...
 *
 *   --dist <dir>  (AV-m-1) serve a vite BUILD from disk through Playwright routing instead of a dev server:
 *                 no server, no port bound, no network; the auth stub and --fixtures still answer first, an
 *                 unknown non-asset route falls back to index.html (scripts/ui-dist.mjs).
 *   <route>       e.g. /ticket-center
 *   <outfile.png> where to save the screenshot
 *   --port        vite dev server port (default 5175)
 *   --fixtures    optional JSON file: { "<url-substring>": <response-body-object>, ... }
 *                 Any same-origin OR remote request whose URL contains the substring is
 *                 fulfilled with the mapped body (status 200). Lets a page render realistic
 *                 rows without live backend data. Longest matching substring wins.
 *   --hover-walk [N]  (DSGN_REBRND R4-3, FWD-13 PROOF) hover up to N (default 60) distinct clickable elements, read
 *                 each one's text ink and effective ground (composited up its ancestors) at rest and on hover, and print
 *                 every pair below 4.5:1 with the denominator; writes <out>.hover-walk.json.
 *                 With --hover-every (row S22): also every hover:-styled element (table rows included, not only
 *                 cursor:pointer), and every text descendant graded; the worst one stands for the element.
 *   --placeholders  (row S22 follow-up) grade every visible input/select/textarea's ::placeholder (or own text) ink against its composited
 *                 ground (opacity chain applied); prints PLACEHOLDER-BELOW for each pair under 4.5:1 with the denominator.
 *   --state-table <json>  (DSGN_REBRND R4-3, FWD-13 PROOF) resolve every token the table names on the rendered
 *                 page, composite overlays and opacity, and print each (ground, ink) pair's WCAG contrast against its
 *                 bar (text 4.5:1, SC 1.4.3; non-text 3:1, SC 1.4.11) with the denominator; writes <out>.state-table.json.
 *   --density     (DSGN_REBRND R4-2, FWD-10 PROOF) print one DENSITY line: the share of the viewport below the last
 *                 content element at the page's scroll end, the gaps between the page column's sections, the panel
 *                 inner padding (PanelContent, `.rounded-b-lg`) as a census, and the page end's own gap.
 *
 * Mechanism notes (hard-won, do not "simplify" away):
 *  - Auth: the app auth-bootstraps itself -- AuthContext.initAuth() POSTs /auth/refresh on
 *    mount. We stub that endpoint with a real-shaped session, so no login and no devBypass
 *    is needed, and the 401->refresh interceptor can never log the session back out.
 *  - CORS: the refresh fetch uses credentials:'include'; a credentialed CORS response REJECTS
 *    a wildcard origin, so we echo the dev origin exactly + Allow-Credentials.
 *  - Browser: system Edge with a fresh headless profile -- never the shared Playwright-MCP
 *    profile (it locks; two sessions collide).
 */
import { chromium } from 'file:///C:/dev/wk-advi-billing-2/portal/node_modules/playwright-core/index.mjs'
import { readFileSync } from 'node:fs'
import { distFromArgs, serveFromDist } from './ui-dist.mjs'

const args = process.argv.slice(2)
// AV-m-1: --dist <built dir> serves a vite build from disk through Playwright routing (no server, no
// port bound, no network) -- see ui-dist.mjs. Absent, routing is unchanged.
const DIST = distFromArgs(args)
// AMGT-rm-2: --route/--out flags, additive over the original positional form -- a flag, when
// present, wins; absent, the old <route> <outfile.png> positional reading is unchanged.
const routeFlagIdx = args.indexOf('--route')
const outFlagIdx = args.indexOf('--out')
let route = routeFlagIdx !== -1 ? args[routeFlagIdx + 1] : args[0]
const out = outFlagIdx !== -1 ? args[outFlagIdx + 1] : args[1]
if (!route || !out) {
  console.error('usage: node scripts/ui-smoke.mjs <route> <outfile.png> [--port 5175] [--fixtures f.json]')
  console.error('       or:  node scripts/ui-smoke.mjs --route <route> --out <outfile.png> [--port 5175] [--fixtures f.json]')
  console.error('       (pass the route WITHOUT a leading slash from git-bash -- MSYS mangles "/x" into a Git-install path)')
  process.exit(2)
}
// De-mangle MSYS path conversion: git-bash rewrites a leading-"/" arg to "<git-install>/x".
const msys = route.match(/^[A-Za-z]:.*?\/Git\/(.+)$/i)
if (msys) route = msys[1]
route = '/' + route.replace(/^\/+/, '')
const port = args.includes('--port') ? args[args.indexOf('--port') + 1] : '5175'
const fixturesPath = args.includes('--fixtures') ? args[args.indexOf('--fixtures') + 1] : null
const fixtures = fixturesPath ? JSON.parse(readFileSync(fixturesPath, 'utf8')) : {}
// 3F-P3a: --firm <id> renders the PARTNER-CLAIMS view (session firmId = the partner, not
// internal), the experience an actual firm user gets; --select <id> drives the internal
// Select-Partner dropdown (native select) after load. Both optional; default unchanged.
const firmOverride = args.includes('--firm') ? args[args.indexOf('--firm') + 1] : null
const selectFirm = args.includes('--select') ? args[args.indexOf('--select') + 1] : null
// 3F-P3a PROD live-render check: --origin renders a DEPLOYED site (e.g.
// https://opalinvest.dev) instead of the local vite server — the real served bundle.
const originOverride = args.includes('--origin') ? args[args.indexOf('--origin') + 1] : null
const ORIGIN = originOverride ?? `http://localhost:${port}`

const EDGE = 'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe'
const CORS = {
  'Access-Control-Allow-Origin': ORIGIN,
  'Access-Control-Allow-Credentials': 'true',
  'Access-Control-Allow-Headers': '*',
  'Access-Control-Allow-Methods': '*',
  'Content-Type': 'application/json',
}
// Real-shaped session for AuthContext.parseClaims (internal Dev admin).
const SESSION = {
  accessToken: 'ui-smoke-token',
  user: { email: 'dev@opalcapital.com', name: 'Dev User', role: 'admin',
          userType: 'Dev', firmId: 'opal-capital', firmRole: null, advisorId: null,
          advisorRole: null, mustChangePassword: false },
}
// --claim key=value (repeatable): set ANY field on the stubbed session user. Some pages gate
// CONTENT on IDENTITY rather than on data, and no fixture can reach that — a fixture supplies a
// response body; the gate reads a claim. Applied AFTER --firm so it can override what --firm sets.
//   e.g. --firm 49financial --claim firmRole=admin  -> a PARTNER admin, which is neither the
//        default internal admin (firmId opal-capital) nor a plain partner user.
const claimArgs = args.reduce((acc, a, i) => (a === '--claim' && args[i + 1] ? [...acc, args[i + 1]] : acc), [])
if (firmOverride) {
  SESSION.user.firmId = firmOverride
  SESSION.user.userType = 'Advisor'
  SESSION.user.role = 'user'
  SESSION.user.email = `ui-smoke@${firmOverride}.test`
}
// --token <jwt | @file> (D8_LIVEEDIT live half): send a REAL bearer -- a minted RS256 portal token --
// instead of the inert 'ui-smoke-token', so the page's API calls through the vite proxy reach the
// LIVE scoped routes (auth-validator-edge + the API authorizer verify it). The session user is
// DERIVED FROM THE TOKEN PAYLOAD (sub/name/role/userType/firmId/firmRole/advisorId/advisorRole),
// so the identity the client-side gate reads and the identity the API verifies are ONE plane --
// a stub claim that disagrees with the token would render an affordance the API then 403s, and
// that mismatch would be the instrument's, not the product's. --claim still applies AFTER this.
const tokenArg = args.includes('--token') ? args[args.indexOf('--token') + 1] : null
if (tokenArg) {
  const jwt = tokenArg.startsWith('@') ? readFileSync(tokenArg.slice(1), 'utf8').trim() : tokenArg
  const payload = JSON.parse(Buffer.from(jwt.split('.')[1], 'base64url').toString('utf8'))
  SESSION.accessToken = jwt
  if (payload.sub) SESSION.user.email = payload.sub
  for (const k of ['name', 'role', 'userType', 'firmId', 'firmRole', 'advisorId', 'advisorRole']) {
    if (payload[k] !== undefined) SESSION.user[k] = payload[k]
  }
  console.log('TOKEN : REAL bearer (sub=%s firmId=%s exp=%s) -- session claims derived from the payload',
    payload.sub, payload.firmId, payload.exp ? new Date(payload.exp * 1000).toISOString() : 'n/a')
}
for (const kv of claimArgs) {
  const i = kv.indexOf('=')
  if (i < 1) { console.log('CLAIM-BAD (expected key=value, ignored):', kv); continue }
  const k = kv.slice(0, i)
  const raw = kv.slice(i + 1)
  SESSION.user[k] = raw === 'null' ? null : raw === 'true' ? true : raw === 'false' ? false : raw
  console.log('CLAIM:', k, '=', JSON.stringify(SESSION.user[k]))
}
// The identity the capture actually ran as. An identity-gated page renders DIFFERENT CONTENT per
// claim set, so a capture that does not state its identity is an enumeration without its frame.
console.log('IDENTITY: firmId=%s userType=%s role=%s firmRole=%s',
  SESSION.user.firmId, SESSION.user.userType, SESSION.user.role, JSON.stringify(SESSION.user.firmRole))

const browser = await chromium.launch({ executablePath: EDGE, headless: true })
// ETFS_SATELLITES.TO-10-DE: `--width <px>` overrides the capture viewport.
// WHY IT HAD TO EXIST: a criterion of the form "N columns fit without clipping" is
// ABOUT the viewport width, and an instrument pinned to one width cannot answer it --
// it reports the clipping of 1440px as though it were a property of the page. Default
// is UNCHANGED at 1440, so every existing caller's capture is byte-comparable.
const widthArg = args.includes('--width') ? Number(args[args.indexOf('--width') + 1]) : 1440
const VIEWPORT_W = Number.isFinite(widthArg) && widthArg >= 320 ? widthArg : 1440
const page = await browser.newPage({ viewport: { width: VIEWPORT_W, height: 900 } })
// --accept-dialogs: accept every window.confirm / alert (Playwright dismisses them by default, which silently cancels a flow such as
// Upload Portfolio's "Continue with upload?" and leaves its modal unopened).
if (args.includes('--accept-dialogs')) page.on('dialog', (d) => { console.log('DIALOG-ACCEPTED:', String(d.message()).replace(/\s+/g, ' ').slice(0, 80)); d.accept().catch(() => {}) })
console.log('VIEWPORT: %dx900', VIEWPORT_W)
page.on('pageerror', e => console.log('PAGE-CRASH:', String(e).slice(0, 300)))
// --console <substring> (repeatable) surfaces page console lines to stdout. Default keeps the
// historical BF2DEBUG filter. Needed to verify a claim about what an accessor RETURNS (not
// just what it paints) from the exercised run rather than from reading the source.
const consoleFilters = args.reduce(
  (acc, a, i) => (a === '--console' && args[i + 1] ? [...acc, args[i + 1]] : acc),
  ['BF2DEBUG']
)
page.on('console', m => {
  const t = m.text()
  if (consoleFilters.some(f => t.includes(f))) console.log('CONSOLE[' + m.type() + ']:', t.slice(0, 300))
})

// FE-s-65: THE INSTRUMENT's flag parsing (repeatable; the pass itself runs later, after the
// click steps, right before the existing state read -- see the block above `const state =`).
const expectSelectors = args.reduce((acc, a, i) => (a === '--expect' && args[i + 1] ? [...acc, args[i + 1]] : acc), [])
const expectTextArgs = args.reduce((acc, a, i) => (a === '--expect-text' && args[i + 1] ? [...acc, args[i + 1]] : acc), [])
const expectStyleArgs = args.reduce((acc, a, i) => (a === '--expect-style' && args[i + 1] ? [...acc, args[i + 1]] : acc), [])
const expectGroundArgs = args.reduce((acc, a, i) => (a === '--expect-ground' && args[i + 1] ? [...acc, args[i + 1]] : acc), [])
const injectCssArgs = args.reduce((acc, a, i) => (a === '--inject-css' && args[i + 1] ? [...acc, args[i + 1]] : acc), [])
const strict = args.includes('--strict')

const fixtureKeys = Object.keys(fixtures).sort((a, b) => b.length - a.length)
// Per-key hit accounting. At ~3 fixtures you can eyeball the map; at ~45 you cannot, and a
// SHADOWED fixture serves the wrong body while the page still renders — so you enumerate a state
// you did not construct, and nothing looks wrong. Counted here, reported at the end.
const fixtureHits = Object.fromEntries(fixtureKeys.map(k => [k, new Set()]))
// FE-s-65: set once FIXTURES-MATCH prints below; read by --strict's exit-code check at the end
// (declared here, at top level, so it is still in scope after `await browser.close()`).
let fixturesMatched = null
const matchFixture = url => {
  const k = fixtureKeys.find(key => url.includes(key))
  if (k) fixtureHits[k].add(url.split('?')[0])
  return k
}
// Static shadow risk: if key A is a substring of key B, every URL containing B also contains A.
// Longest-match resolves it (B wins), which is right — but the PAIR is worth surfacing, because
// it means A's intended scope is narrower than its author probably thinks.
const shadowPairs = []
for (const a of fixtureKeys) {
  for (const b of fixtureKeys) {
    if (a !== b && b.includes(a)) shadowPairs.push([a, b])
  }
}

// FE-s-74 (C-S147): KEY-VALIDITY -- do the fixture's declared URL-substring keys name REAL
// operation keys, per this client's own generated `contracts/wire/consumed.ts`? Read the
// file, never hand-maintain a duplicate list of routes (per the cell's own instruction).
// `WIRE_CONSUMED_ROUTE_KEYS` entries are `"METHOD /api/.../{param}/..."` templates; a
// fixture key is one of the URL SUBSTRINGS the router matches requests against.
//
// FE-s-80 (round 13, C-S166/C-S147): the original classifier treated EVERY template the same
// way -- truncate at the first `{` and require the fixture key to equal that truncated string
// EXACTLY (`candidates.has(k)`, an exact-set membership test). That is right for a route with
// NO `{param}` (its "candidate" IS its whole real path, so only an exact match is a real key),
// but wrong for a PARAMETERISED route: a fixture that carries a CONCRETE value after the
// prefix (e.g. `/holdings/A-0001`, satisfying `GET .../holdings/{accountSetId}`) is a MORE
// faithful fixture than the bare prefix, and the exact-match test rejected it. The round-13 fix
// split routes into two disjoint sets (`exact` vs `prefixes`) but used `k.startsWith(p)` for the
// parameterised branch, which is itself too loose: it accepts ANY key that merely starts with the
// template's static prefix, including one with an EXTRA, undeclared TRAILING segment past the
// template's own last segment (e.g. `holdings/A-0001/not-a-declared-operation` against
// `holdings/{accountSetId}` -- F80-AC6, round-13 CVO finding).
//
// FE-s-86 (round 14, C-S147, CTO round-13 analysis item 2): replaced with a SEGMENT-FOR-SEGMENT
// template matcher. A route with NO `{param}` still goes into the `exact` set and is valid only
// on whole-string equality (unchanged). A route WITH a `{param}` is split into its PATH SEGMENTS
// (kept as a template, not collapsed to a bare prefix string); a concrete key is valid against
// that template only when (a) the segment COUNT is identical -- so a key with an extra trailing
// segment is rejected however plausible it looks, (b) every LITERAL segment is byte-equal, and
// (c) every `{param}` segment lines up with exactly one NON-EMPTY concrete segment. Because
// `exact` and the parameterised templates are still populated from disjoint route shapes, a
// static route can NEVER be satisfied by template-matching -- only a route that actually
// declares a `{param}` contributes a template at all (same guard as round 13, preserved here).
const routeKeyCandidates = routeKeys => {
  const exact = new Set()
  const templates = []
  for (const full of routeKeys) {
    const sp = full.indexOf(' ')
    const path = sp === -1 ? full : full.slice(sp + 1)
    if (path.indexOf('{') === -1) {
      exact.add(path)
    } else {
      templates.push(path.split('/'))
    }
  }
  return { exact, templates }
}
const checkKeyValidity = (keys, referenceFixturesPath) => {
  if (!keys.length || !referenceFixturesPath) return null
  // Locate the owning page directory from the fixtures path actually passed in
  // (`src/pages/<PageName>/...`), so this is not hand-pinned to one page.
  const m = /(^|[\\/])src[\\/]pages[\\/]([^\\/]+)[\\/]/.exec(referenceFixturesPath)
  if (!m) return null
  const consumedRelPath = `src/pages/${m[2]}/contracts/wire/consumed.ts`
  let text
  try {
    text = readFileSync(consumedRelPath, 'utf8')
  } catch {
    return null
  }
  const arrayMatch = /WIRE_CONSUMED_ROUTE_KEYS[^=]*=\s*\[([\s\S]*?)\]/.exec(text)
  if (!arrayMatch) return null
  const routeKeys = [...arrayMatch[1].matchAll(/'([^']*)'/g)].map(mm => mm[1])
  const { exact, templates } = routeKeyCandidates(routeKeys)
  // Segment-for-segment: identical segment count, every literal segment byte-equal, every
  // `{param}` segment matched against exactly one non-empty concrete segment.
  const matchesTemplate = (keySegments, templateSegments) => {
    if (keySegments.length !== templateSegments.length) return false
    for (let i = 0; i < templateSegments.length; i += 1) {
      const t = templateSegments[i]
      const k = keySegments[i]
      if (t.length >= 2 && t[0] === '{' && t[t.length - 1] === '}') {
        if (!k || k.length === 0) return false
      } else if (t !== k) {
        return false
      }
    }
    return true
  }
  const valid = keys.filter(k => exact.has(k) || templates.some(t => matchesTemplate(k.split('/'), t))).length
  return { valid, total: keys.length }
}

// --fail <url-substring> (repeatable): serve 503 for matching requests. Exercises a
// DEGRADED path for real -- an accessor's primary/fallback branch can only be verified by
// making the primary actually fail, and a claim about degraded UI read from source instead
// of rendered is the config-read-for-a-behaviour-claim class (CLAUDE.md Rule 22a).
// Evaluated BEFORE fixtures, so a failed URL stays failed even if also fixtured.
const failSubstrings = args.reduce((acc, a, i) => (a === '--fail' && args[i + 1] ? [...acc, args[i + 1]] : acc), [])
const matchFail = url => failSubstrings.find(k => url.includes(k))

// FE-s-65: --delay '<url-substring>=<ms>' (repeatable): holds a matching request for <ms>
// before it is fulfilled -- the tool it takes to construct an IN-FLIGHT state (a submit that
// has not yet resolved) deterministically, without a real backend. Evaluated ALONGSIDE --fail,
// same longest-substring-wins rule, checked right after the fail check and before fixtures --
// so a delayed URL still falls through to its fixture (or the auth stub, or the real network)
// once the hold elapses.
const delayArgs = args.reduce((acc, a, i) => (a === '--delay' && args[i + 1] ? [...acc, args[i + 1]] : acc), [])
const delaySpecs = delayArgs.map(kv => {
  const i = kv.lastIndexOf('=')
  return { key: kv.slice(0, i), ms: Number(kv.slice(i + 1)) }
}).filter(d => d.key && Number.isFinite(d.ms))
const matchDelay = url => delaySpecs.filter(d => url.includes(d.key)).sort((a, b) => b.key.length - a.key.length)[0]

// --netlog <file>: append every request this page makes, as `METHOD<TAB>STATUS<TAB>URL`.
// The non-structural ENUMERATION plane (OPAL_ANALYST PRD binding X): a structural read of the code
// can only find data paths that LOOK like data paths, so an enumeration that must be complete needs
// one plane that observes BEHAVIOUR instead. Records what actually fires, however it is written.
const netlogPath = args.includes('--netlog') ? args[args.indexOf('--netlog') + 1] : null
const netlog = []
if (netlogPath) {
  page.on('requestfinished', async req => {
    const res = await req.response().catch(() => null)
    netlog.push([req.method(), res ? res.status() : 'NO-RESPONSE', req.url()].join('\t'))
  })
  page.on('requestfailed', req => {
    netlog.push([req.method(), 'FAILED', req.url()].join('\t'))
  })
}

// One router for everything: forced failures, then a delay hold, then fixtures, then the auth
// stub, then through. The handler is async so the delay's hold is a real await, not a fire-and-forget.
await page.route('**/*', async r => {
  { const u = r.request().url(); if (u.includes('/api/') || u.includes('/auth/')) console.log('REQ:', u.replace(/^https?:\/\/[^/]+/, ''), Object.keys(fixtures).filter(k => u.includes(k)).sort((a,b)=>b.length-a.length)[0] || '(no fixture)') }
  const req = r.request()
  const url = req.url()
  if (req.method() === 'OPTIONS' && !url.startsWith(ORIGIN)) {
    return r.fulfill({ status: 204, headers: CORS, body: '' })
  }
  const failKey = matchFail(url)
  if (failKey) {
    console.log('FORCED-FAIL:', failKey)
    return r.fulfill({ status: 503, headers: CORS, body: JSON.stringify({ error: 'ui-smoke forced failure' }) })
  }
  const delaySpec = matchDelay(url)
  if (delaySpec) {
    console.log(`DELAYED: ${delaySpec.key} (${delaySpec.ms}ms)`)
    await new Promise(resolve => setTimeout(resolve, delaySpec.ms))
  }
  const fk = matchFixture(url)
  if (fk) return r.fulfill({ status: 200, headers: CORS, body: JSON.stringify(fixtures[fk]) })
  if (url.includes('/auth/refresh')) {
    return r.fulfill({ status: 200, headers: CORS, body: JSON.stringify(SESSION) })
  }
  if (await serveFromDist(r, DIST, ORIGIN)) return
  return r.continue()
})

await page.goto(ORIGIN + route, { waitUntil: 'networkidle', timeout: 30000 })
  .catch(e => console.log('goto:', e.message.split('\n')[0]))
// --wait / --clickwait (ms): the capture's OBSERVATION WINDOW. Defaults are the original 3000/2500,
// tuned on a 16-file 3-accessor page. On a larger page a request still IN FLIGHT at browser.close()
// fires NEITHER requestfinished NOR requestfailed, so it is recorded by nothing — and an absence
// recorded by nothing is indistinguishable from a request that never fired.
const WAIT = args.includes('--wait') ? Number(args[args.indexOf('--wait') + 1]) : 3000
const CLICKWAIT = args.includes('--clickwait') ? Number(args[args.indexOf('--clickwait') + 1]) : 2500
await page.waitForTimeout(WAIT)

if (selectFirm) {
  try {
    await page.selectOption('select', selectFirm)
    console.log('SELECTED:', selectFirm)
  } catch (e) {
    console.log('SELECT-FAIL:', e.message.split('\n')[0])
  }
  await page.waitForTimeout(3000)
}

// 3F None-count exercise: --click "<button text>" clicks a visible button (e.g. the
// Count toggle) after load/selection, then waits for re-render.
// D8_LIVEEDIT live half: --click is REPEATABLE and --fill "<aria-label>=<text>" fills a textbox by
// its accessible name; the combined step list runs IN ARGV ORDER, each step followed by CLICKWAIT,
// so a multi-step state (tab -> modal -> edit mode -> save) is reachable in the ONE instrument
// instead of a second script. A button OR a tab matches (some tab strips are role=tab).
//
// ADVI_PERFRP (DE~D 2026-08-25): --clicktext "<visible text>" clicks the nearest CLICKABLE
// ANCESTOR of an element containing that text, for rows that carry an onClick on a bare
// <div> with NO ARIA ROLE. --click above resolves role=button|tab ONLY, so it is
// STRUCTURALLY UNABLE to reach such a row -- the Books advisor row and the L3 client row are
// both `<div onClick>` (AdvisorsTab LeaderboardRow), which is why the Books L2->L3 drill had
// never been reachable in this harness and the L3 screenshot oracle had never been runnable.
// ADDITIVE: --click is untouched. Prefer --click when a real button exists; an unrolled
// clickable div is an accessibility defect this flag WORKS AROUND and does not bless.
// ETFS_SATELLITES.TO-9-DE: `--pick <value>` is `--select` AS AN ORDERED STEP.
// WHY A SECOND FLAG RATHER THAN MOVING `--select`: `--select` fires BEFORE this list
// (line ~206), which is correct for a dropdown present at load -- every existing
// caller depends on that. But a dropdown that only EXISTS after a click (the
// satellites firm selector appears only in satellites mode) is unreachable that way:
// the selectOption runs against a page where the control does not yet exist. Moving
// `--select` would silently re-order every existing caller's run, so this is
// ADDITIVE and `--select` is untouched.
const steps = args.reduce((acc, a, i) => (
  (a === '--click' || a === '--fill' || a === '--clicktext' || a === '--clickrole' || a === '--clicksel' || a === '--hoversel' || a === '--pick') && args[i + 1]
    ? [...acc, { kind: a.slice(2), arg: args[i + 1] }]
    : acc
), [])
let stepFailures = 0
for (const step of steps) {
  try {
    if (step.kind === 'click') {
      const byName = { name: step.arg, exact: true }
      await page.getByRole('button', byName).or(page.getByRole('tab', byName)).first().click()
      console.log('CLICKED:', step.arg)
    } else if (step.kind === 'clicktext') {
      // Walk UP from the text node to the nearest ancestor with a click handler or a
      // pointer cursor, then click THAT. Clicking the text node itself often lands on an
      // inner <span> whose parent holds the handler -- which does fire via bubbling, but
      // only when the span is not overlapped; the ancestor walk removes that coin-flip.
      // "<text>#<n>" selects the Nth (0-based) occurrence. WITHOUT this, .first() is a
      // SILENT WRONG CLICK, not a miss: the L2 client name appears in the "Largest
      // Relationship" TILE before the client-list ROW, and the Fee Summary "Max" appears
      // after the Assets Overview "Max" -- both cases clicked something real and reported
      // success while the intended state was never entered.
      const m = /^(.*)#(\d+)$/.exec(step.arg)
      const text = m ? m[1] : step.arg
      const nth = m ? Number(m[2]) : 0
      const target = page.locator(`text=${JSON.stringify(text)}`).nth(nth)
      await target.waitFor({ state: 'visible', timeout: 15000 })
      const handle = await target.elementHandle()
      const clickable = await handle.evaluateHandle(el => {
        let n = el
        for (let i = 0; i < 8 && n; i++) {
          const cs = window.getComputedStyle(n)
          if (n.onclick || cs.cursor === 'pointer' || n.getAttribute('role') === 'button') return n
          n = n.parentElement
        }
        return el
      })
      await clickable.asElement().click()
      console.log('CLICKED-TEXT:', text, nth ? `(occurrence #${nth})` : '')
    } else if (step.kind === 'clickrole') {
      // --clickrole <role>:<accessible name>[#n] -- any ARIA role (a checkbox, a menuitem, a row); #n selects the nth (0-based) match.
      const m = /^([a-z]+):(.*?)(?:#(\d+))?$/.exec(step.arg)
      if (!m) throw new Error('--clickrole wants <role>:<name>[#n]')
      await page.getByRole(m[1], { name: m[2], exact: true }).nth(m[3] ? Number(m[3]) : 0).click()
      console.log('CLICKED-ROLE:', step.arg)
    } else if (step.kind === 'clicksel') {
      // --clicksel <css selector>[#n] -- click the Nth (0-based) element a CSS selector matches: for a target with no role and no text of its own (an SVG chart bar
      // with an onClick, a recharts rect). Additive: --click / --clicktext / --clickrole are untouched.
      const m = /^(.*?)(?:#(\d+))?$/.exec(step.arg)
      await page.locator(m[1]).nth(m[2] ? Number(m[2]) : 0).click({ force: true })
      console.log('CLICKED-SEL:', step.arg)
    } else if (step.kind === 'hoversel') {
      // --hoversel <css selector>[#n] -- hover the Nth (0-based) element a CSS selector matches and leave the pointer there for the screenshot (a highlighted row).
      const m = /^(.*?)(?:#(\d+))?$/.exec(step.arg)
      await page.locator(m[1]).nth(m[2] ? Number(m[2]) : 0).hover({ force: true })
      console.log('HOVERED-SEL:', step.arg)
    } else if (step.kind === 'pick') {
      await page.selectOption('select', step.arg)
      console.log('PICKED :', JSON.stringify(step.arg))
    } else {
      const i = step.arg.indexOf('=')
      const label = step.arg.slice(0, i)
      const text = step.arg.slice(i + 1)
      await page.getByRole('textbox', { name: label, exact: true }).first().fill(text)
      console.log('FILLED :', label, '<-', JSON.stringify(text).slice(0, 80))
    }
  } catch (e) {
    stepFailures++
    console.log(step.kind.toUpperCase() + '-FAIL:', step.arg, '--', e.message.split('\n')[0])
    // The names that WERE on the page, so a miss is diagnosable from this run, not by re-running.
    const names = await page.locator('button,[role=button],[role=tab],textarea,input').evaluateAll(els =>
      els.map(e => e.getAttribute('aria-label') || (e.textContent || '').trim()).filter(Boolean).slice(0, 40))
    console.log('  (control names on page:', JSON.stringify(names), ')')
  }
  await page.waitForTimeout(CLICKWAIT)
}

// P1 close: --hoverlast hovers the LAST rendered chart's right-edge area to raise the
// recharts tooltip, then prints its text — the DOM read of the tooltip Total.
if (args.includes('--hoverlast')) {
  try {
    const charts = await page.locator('.recharts-wrapper').all()
    const target = charts[charts.length - 1]
    await target.scrollIntoViewIfNeeded()
    await page.waitForTimeout(400)
    const box = await target.boundingBox()
    if (box) {
      // Aim at the FRONTIER (rightmost data point): recharts snaps to the nearest
      // point, so land just inside the plot's right edge.
      await page.mouse.move(box.x + box.width - 60, box.y + box.height / 2)
      await page.waitForTimeout(300)
      await page.mouse.move(box.x + box.width - 42, box.y + box.height / 2 - 8)
      await page.waitForTimeout(300)
      await page.mouse.move(box.x + box.width - 31, box.y + box.height / 2)
      await page.waitForTimeout(900)
      const tip = await page.locator('.recharts-tooltip-wrapper').last().innerText().catch(() => '')
      console.log('TOOLTIP:', tip.replace(/\s+/g, ' ').slice(0, 300))
    }
  } catch (e) {
    console.log('HOVER-FAIL:', e.message.split('\n')[0])
  }
}

// FE-s-65: THE INSTRUMENT -- content, style and ground assertions, with controls that can fail.
// Round 10's CANVAS/TEXT lines above read `document.body` on the PAGE FIELD, never a route's own
// container, so a capture could read the right colour over the wrong page (the CTO's round-10
// criterion rule). These flags let a cell assert against a SPECIFIC element and prove the
// assertion can say no: --expect (visibility), --expect-text (rendered text), --expect-style
// (computed style, `=`/`!=`), --expect-ground (the nearest NON-TRANSPARENT background walking up
// from the element -- the actual container, not the page). --inject-css builds a WRONG-STATE
// control (paints a container silver) and nothing else; it runs first so every expectation below
// sees it. All four are repeatable. Grammar: the FIRST `::` in an --expect-text/--expect-style
// argument separates selector from the rest (a selector containing `::` is not supported); the
// LAST `=` in an --expect-ground argument separates selector from the `rgb(...)` value, because a
// CSS attribute selector (`[data-slot="x"]`) itself contains `=` and an rgb(...) value never does.
// Runs AFTER the click steps and the observation wait, BEFORE the existing state read below, so an
// expectation observes the post-interaction DOM. Old flags/lines above are untouched (F65-AC2).
if (injectCssArgs.length) {
  for (const css of injectCssArgs) {
    await page.addStyleTag({ content: css })
    console.log('INJECT-CSS:', css)
  }
}

// "Visible" = a non-empty bounding box AND computed display != none AND visibility != hidden.
const countVisible = async selector => page.evaluate(sel => (
  Array.from(document.querySelectorAll(sel)).filter(el => {
    const rect = el.getBoundingClientRect()
    const cs = getComputedStyle(el)
    return rect.width > 0 && rect.height > 0 && cs.display !== 'none' && cs.visibility !== 'hidden'
  }).length
), selector)

// The FIRST match's innerText -- AFTER CSS text-transform, which is what innerText always reflects.
const firstInnerText = async selector => page.evaluate(sel => {
  const el = document.querySelector(sel)
  return el ? el.innerText : null
}, selector)

// The FIRST match's computed style value for an arbitrary (possibly kebab-case) property.
const firstComputedStyle = async (selector, property) => page.evaluate(({ sel, prop }) => {
  const el = document.querySelector(sel)
  return el ? getComputedStyle(el).getPropertyValue(prop) : null
}, { sel: selector, prop: property })

// Ground = the first ancestor-or-self (starting at the FIRST match) whose computed
// background-color has non-zero alpha.
// FE-s-74 HARDENING (W20-S2): the pre-existing walker read ONLY backgroundColor and
// regex-parsed it as rgba?(...) -- a composited/gradient paint (backgroundImage != none)
// left backgroundColor transparent, and an unparseable-but-opaque value (oklch(...)/
// lab(...)/color(...)) never matched the regex either, so BOTH classes fell through
// silently and the walk climbed PAST the real element to whatever solid ancestor it
// eventually found, misreporting that ancestor's colour as the target's own ground.
// Fixed here: at EVERY element the walk visits (not just the first), a non-'none'
// backgroundImage, or a backgroundColor that fails the rgba?(...) parse while being
// non-empty/non-transparent, STOPS THE WALK on that element and returns an
// { state: 'unmeasurable', raw } result instead of continuing past it. A selector that
// resolves to nothing at all is a SEPARATE, distinguishable state ('absent') so an
// absent-selector control and a real-but-unmeasurable-paint control both fail closed,
// legibly, rather than both silently returning null.
const groundColor = async selector => page.evaluate(sel => {
  let el = document.querySelector(sel)
  if (!el) return { state: 'absent' }
  while (el) {
    const cs = getComputedStyle(el)
    const bgImage = cs.backgroundImage
    if (bgImage && bgImage !== 'none') {
      return { state: 'unmeasurable', raw: bgImage }
    }
    const bg = cs.backgroundColor
    const m = /rgba?\(([^)]+)\)/.exec(bg)
    if (m) {
      const parts = m[1].split(',').map(s => parseFloat(s.trim()))
      const alpha = parts.length > 3 ? parts[3] : 1
      if (alpha > 0) return { state: 'ok', value: bg }
      // alpha 0 (genuinely transparent): keep climbing, unchanged behaviour.
    } else if (bg && bg !== 'transparent') {
      // Non-empty, not the transparent keyword, and NOT rgba?(...)-parseable -- an
      // opaque composited/unsupported colour space (oklch/lab/color()). Stop here.
      return { state: 'unmeasurable', raw: bg }
    }
    el = el.parentElement
  }
  return { state: 'none' }
}, selector)

// FE-s-74: set true the moment ANY --expect-style or --expect-ground assertion prints
// UNMEASURABLE. Read after browser.close() to force a non-zero exit UNCONDITIONALLY --
// not gated behind --strict -- because a false PASS/FAIL on an unmeasurable read is the
// exact defect being fixed here; the fix must fail closed on its own, not only when the
// caller opted into --strict.
let anyUnmeasurable = false

const contentResults = []
for (const css of expectSelectors) {
  const n = await countVisible(css)
  const pass = n > 0
  console.log(`EXPECT[${css}]: ${pass ? 'PASS' : 'FAIL'} (${n} visible)`)
  contentResults.push(pass)
}
for (const spec of expectTextArgs) {
  const sep = spec.indexOf('::')
  const css = sep === -1 ? spec : spec.slice(0, sep)
  const needle = sep === -1 ? '' : spec.slice(sep + 2)
  const text = await firstInnerText(css)
  const pass = text !== null && text.includes(needle)
  console.log(`EXPECT-TEXT[${spec}]: ${pass ? 'PASS' : 'FAIL'}`)
  contentResults.push(pass)
}

const styleResults = []
for (const spec of expectStyleArgs) {
  const sep = spec.indexOf('::')
  const css = sep === -1 ? spec : spec.slice(0, sep)
  const rest = sep === -1 ? '' : spec.slice(sep + 2)
  const bangIdx = rest.indexOf('!=')
  const op = bangIdx !== -1 ? '!=' : '='
  const opIdx = bangIdx !== -1 ? bangIdx : rest.indexOf('=')
  const property = opIdx === -1 ? rest : rest.slice(0, opIdx)
  const value = opIdx === -1 ? '' : rest.slice(opIdx + op.length)
  const actual = await firstComputedStyle(css, property)
  // FE-s-74 HARDENING (C-S146): firstComputedStyle returns null ONLY when the selector
  // resolved to nothing (querySelector found no element). The pre-existing `!=` branch
  // computed `null !== value` as true, so an absent selector read a false PASS on the
  // inequality operator. Both operators now print UNMEASURABLE on a null actual, never a
  // PASS/FAIL computed from it.
  if (actual === null) {
    console.log(`EXPECT-STYLE[${css}::${property}]: UNMEASURABLE (selector matched nothing)`)
    styleResults.push(null)
    anyUnmeasurable = true
  } else {
    const pass = op === '!=' ? actual !== value : actual === value
    console.log(`EXPECT-STYLE[${css}::${property}]: ${pass ? 'PASS' : 'FAIL'} ${actual}`)
    styleResults.push(pass)
  }
}

const groundResults = []
for (const spec of expectGroundArgs) {
  const idx = spec.lastIndexOf('=')
  const css = idx === -1 ? spec : spec.slice(0, idx)
  const value = idx === -1 ? '' : spec.slice(idx + 1)
  const result = await groundColor(css)
  if (result.state === 'absent' || result.state === 'unmeasurable') {
    const raw = result.state === 'absent' ? '(selector matched nothing)' : result.raw
    console.log(`EXPECT-GROUND[${css}]: UNMEASURABLE ${raw}`)
    groundResults.push(null)
    anyUnmeasurable = true
  } else {
    const actual = result.state === 'ok' ? result.value : null
    const pass = actual === value
    console.log(`EXPECT-GROUND[${css}]: ${pass ? 'PASS' : 'FAIL'} ${actual}`)
    groundResults.push(pass)
  }
}

if (contentResults.length) {
  console.log(`ASSERT-CONTENT: ${contentResults.filter(Boolean).length} of ${contentResults.length} met`)
}
if (styleResults.length) {
  console.log(`ASSERT-STYLE: ${styleResults.filter(Boolean).length} of ${styleResults.length} met`)
}
if (groundResults.length) {
  console.log(`ASSERT-GROUND: ${groundResults.filter(Boolean).length} of ${groundResults.length} met`)
}

const state = await page.evaluate(() => ({
  loc: window.location.pathname,
  canvas: getComputedStyle(document.body).backgroundColor,
  text: document.body.innerText.replace(/\s+/g, ' ').slice(0, 160),
  // diagnostic: recharts overlay elements per chart surface (3F-BF2 band debugging)
  refAreas: Array.from(document.querySelectorAll('.recharts-reference-area')).length,
  charts: Array.from(document.querySelectorAll('.recharts-wrapper')).map(w =>
    (w.querySelectorAll('.recharts-reference-area').length) + 'ra'
  ).join(','),
}))
console.log('LOC   :', state.loc, state.loc === new URL(ORIGIN + route).pathname ? '' : ' <-- DID NOT LAND (auth redirect? bad route?)')
console.log('CANVAS:', state.canvas, '(the page field; contract portal/DESIGN.md C3 = #F4F6FA = rgb(244, 246, 250) -- light fg on this is the footgun)')
console.log("TEXT  :", state.text)
console.log("REFAREAS:", state.refAreas, "per-chart:", state.charts)
if (args.includes('--hover-walk')) {
  const nArg = Number(args[args.indexOf('--hover-walk') + 1])
  const cap = Number.isFinite(nArg) && nArg > 0 ? nArg : 60
  // One element per distinct class signature, so a 40-row table counts once; tagged for Playwright's own hover.
  // --hover-every (row S22): also every element styled with a hover: utility (rows are not cursor:pointer), the nested
  // pointer rule lifted, and every text descendant graded rather than the first.
  const every = args.includes('--hover-every')
  // --text-all: also sweep EVERY visible element that carries its own text, interactive or not, at rest (static text).
  const textAll = args.includes('--text-all')
  const pickedInfo = await page.evaluate(({ max, every, textAll }) => {
    const seen = new Set(); const out = []; let extras = 0; let viaSheet = 0
    // Row S24 gap 2: hover is also read from the compiled stylesheet. Every rule whose selector holds :hover gives a base
    // selector (the :hover stripped); an element matching one is hover-reactive though no class token says `hover:`
    // (variant-prefixed tokens, group-hover, index.css rules such as .card-hover:hover).
    // HOVER-READER-BEGIN (scripts/ui-smoke-hover-control.cjs runs this exact block against a synthetic page)
    const hoverBases = []
    if (every) {
      // Tailwind v4 emits nested rules (.hover\:x { &:hover { ... } }): a child selector resolves against its parent's.
      const gather = (rules, parentSel) => { for (const r of rules) { try {
        let sel = null
        if (r.selectorText) sel = parentSel ? (r.selectorText.includes('&') ? r.selectorText.replace(/&/g, parentSel) : parentSel + ' ' + r.selectorText) : r.selectorText
        if (sel && sel.includes(':hover')) for (const part of sel.split(',')) if (part.includes(':hover')) { const base = part.replace(/:hover/g, '').trim(); if (base && base !== '*') hoverBases.push(base) }
        if (r.cssRules) gather(r.cssRules, sel || parentSel)
      } catch { /* a rule the browser will not read */ } } }
      for (const sh of document.styleSheets) { try { gather(sh.cssRules, null) } catch { /* cross-origin sheet */ } }
    }
    const sheetHover = (el) => { for (const sel of hoverBases) { try { if (el.matches(sel)) return true } catch { /* selector the matcher rejects */ } } return false }
    // HOVER-READER-END
    for (const el of document.querySelectorAll('body *')) {
      if (out.length >= max && !every) break
      const cs = getComputedStyle(el); const r = el.getBoundingClientRect()
      const tokenHover = every && /(^|\s)(group-)?hover:/.test(el.getAttribute('class') || '')
      const hoverStyled = tokenHover || (every && cs.cursor !== 'pointer' && r.width >= 8 && r.height >= 8 && sheetHover(el))
      if (hoverStyled && !tokenHover) viaSheet++
      const nonInteractive = cs.cursor !== 'pointer' && !hoverStyled
      if (nonInteractive && textAll && r.width >= 1 && r.height >= 1 && cs.visibility !== 'hidden' && extras < 4000 && Array.from(el.childNodes).some((n) => n.nodeType === 3 && (n.textContent || '').trim())) { el.setAttribute('data-hx', String(extras++)); continue }
      if (nonInteractive || r.width < 8 || r.height < 8 || cs.visibility === 'hidden') continue
      if (!every && el.parentElement && getComputedStyle(el.parentElement).cursor === 'pointer') continue
      if (!(el.innerText || '').trim()) continue
      const sig = el.tagName + '|' + (el.getAttribute('class') || '')
      // Same-signature siblings (44 rows of one class) are not hovered but ARE read at rest below (row S24).
      if (seen.has(sig)) { if (every && extras < (textAll ? 4000 : 1000)) el.setAttribute('data-hx', String(extras++)); continue }
      if (out.length >= max) continue
      seen.add(sig); el.setAttribute('data-hw', String(out.length)); out.push(out.length)
    }
    return { n: out.length, extras, viaSheet, hoverRules: hoverBases.length }
  }, { max: cap, every, textAll })
  const picked = pickedInfo.n
  // Ink: the first text-bearing node's color, composited by the opacity chain; ground: background layers composited
  // from the element up to the first opaque one.
  const readPair = (i, attr = 'data-hw') => page.evaluate(({ idx, every, attr }) => {
    const el = document.querySelector(`[${attr}="${idx}"]`); if (!el) return null
    // Any CSS colour (rgb, oklab, color-mix ...) to straight RGBA through a 1x1 canvas.
    const cv = (window.__hwCanvas ||= Object.assign(document.createElement('canvas'), { width: 1, height: 1 })).getContext('2d', { willReadFrequently: true })
    const rgba = (v) => { if (!v || v === 'transparent') return [0, 0, 0, 0]; cv.clearRect(0, 0, 1, 1); cv.fillStyle = '#000'; cv.fillStyle = v; cv.fillRect(0, 0, 1, 1); const d = cv.getImageData(0, 0, 1, 1).data; return [d[0], d[1], d[2], d[3] / 255] }
    const walker = document.createTreeWalker(el, NodeFilter.SHOW_TEXT, { acceptNode: (n) => (n.textContent || '').trim() ? NodeFilter.FILTER_ACCEPT : NodeFilter.FILTER_SKIP })
    const textEls = []
    for (let t = walker.nextNode(); t; t = walker.nextNode()) {
      if (t.parentElement && !textEls.includes(t.parentElement)) textEls.push(t.parentElement)
      if (!every) break
    }
    if (!textEls.length) textEls.push(el)
    const lum = (c) => { const [r, g, b] = c.map((x) => { x /= 255; return x <= 0.03928 ? x / 12.92 : ((x + 0.055) / 1.055) ** 2.4 }); return 0.2126 * r + 0.7152 * g + 0.0722 * b }
    const hex = (c) => '#' + c.map((x) => Math.round(x).toString(16).padStart(2, '0')).join('').toUpperCase()
    const readOne = (textEl) => {
      // Visible text only (row S24, the CVO's over-report note): scroll it into view, then the element painted at its centre must be
      // the text, one of its descendants or one of its ancestors. A row clipped by a scroll container, or a node under a modal
      // backdrop, paints something else (or nothing) there and is not graded.
      try { textEl.scrollIntoView({ block: 'center', inline: 'nearest' }) } catch { /* detached */ }
      const vr = textEl.getBoundingClientRect()
      const painted = document.elementFromPoint(vr.left + vr.width / 2, vr.top + vr.height / 2)
      // An ANCESTOR painted at the centre passes only when the text ignores pointer events (an overlay label); otherwise a clipped
      // row whose centre lands on the shared panel would pass. Skips are counted and printed (VISIBILITY-SKIPPED).
      const ignoresPointer = getComputedStyle(textEl).pointerEvents === 'none'
      if (!painted || !(textEl.contains(painted) || (ignoresPointer && painted.contains(textEl)))) { window.__hwSkip = (window.__hwSkip || 0) + 1; return null }
      const layers = []; let opq = false; let imageGround = false
      // The ground is what is PAINTED beneath the text at its centre, in paint order: the text element's own fill, then every
      // element under it at that point -- ancestors AND siblings (a tile or badge painted by a sibling element, a label that
      // overhangs its bar). The ancestor chain is the fallback when the text is not in the point's stack.
      const tr = textEl.getBoundingClientRect(); const cx = tr.left + tr.width / 2; const cy = tr.top + tr.height / 2
      const pointStack = document.elementsFromPoint(cx, cy); const at = pointStack.indexOf(textEl)
      let chain = at >= 0 ? pointStack.slice(at) : []
      if (!chain.length) for (let n = textEl; n && n.nodeType === 1; n = n.parentElement) chain.push(n)
      for (const n of chain) {
        const st = getComputedStyle(n); if (st.backgroundImage && st.backgroundImage !== 'none') imageGround = true
        // An SVG shape (a treemap tile, a bar rect) paints with `fill`, not a CSS background.
        const isShape = typeof SVGGeometryElement !== 'undefined' && n instanceof SVGGeometryElement
        const c = isShape ? (st.fill && st.fill !== 'none' ? rgba(st.fill) : [0, 0, 0, 0]) : rgba(st.backgroundColor)
        if (isShape) c[3] *= Number(st.fillOpacity === '' ? 1 : st.fillOpacity) * Number(st.opacity === '' ? 1 : st.opacity)
        if (c[3] > 0) { layers.push(c); if (c[3] >= 1) { opq = true; break } }
      }
      let ground = opq ? layers.pop().slice(0, 3) : [255, 255, 255]
      while (layers.length) { const c = layers.pop(); ground = ground.map((g, k) => c[k] * c[3] + g * (1 - c[3])) }
      let alpha = 1; for (let n = textEl; n && n.nodeType === 1; n = n.parentElement) alpha *= Number(getComputedStyle(n).opacity)
      // SVG text is painted with `fill`; `color` is only the value it would inherit (row S26).
      const cst = getComputedStyle(textEl); const isSvg = typeof SVGElement !== 'undefined' && textEl instanceof SVGElement
      const ic = rgba(isSvg ? cst.fill : cst.color); const a = ic[3] * alpha * (isSvg ? Number(cst.fillOpacity === '' ? 1 : cst.fillOpacity) : 1)
      if (a < 0.05) return null
      const ink = ground.map((g, k) => ic[k] * a + g * (1 - a))
      const [h, l] = [lum(ground), lum(ink)].sort((p, q) => q - p)
      return { imageGround, ratio: +((h + 0.05) / (l + 0.05)).toFixed(2), ground: hex(ground), ink: hex(ink), text: (textEl.innerText || textEl.textContent || '').trim().replace(/\s+/g, ' ').slice(0, 20), node: textEl.tagName.toLowerCase() + '.' + String(textEl.getAttribute('class') || textEl.getAttribute('fill') || '').slice(0, 60) }
    }
    // The worst text descendant stands for the element; `texts` is the denominator.
    const reads = textEls.map(readOne).filter(Boolean)
    if (!reads.length) return { hidden: true }
    const worst = reads.reduce((p, q) => (q.ratio < p.ratio ? q : p))
    return { imageGround: reads.some((x) => x.imageGround), ratio: worst.ratio, ground: worst.ground, ink: worst.ink, texts: reads.length,
      label: `${el.tagName.toLowerCase()} "${(el.innerText || '').trim().replace(/\s+/g, ' ').slice(0, 28)}"${every && reads.length > 1 ? ` [worst of ${reads.length}: "${worst.text}" <${worst.node}>]` : ''}`, cls: (el.getAttribute('class') || '').slice(0, 90) }
  }, { idx: i, every, attr })
  const walked = []
  for (let i = 0; i < picked; i++) {
    const rest = await readPair(i); if (!rest || rest.hidden) continue
    const loc = page.locator(`[data-hw="${i}"]`)
    await loc.scrollIntoViewIfNeeded({ timeout: 3000 }).catch(() => {})
    const hovered = await loc.hover({ timeout: 3000 }).then(() => true).catch(() => false)
    await page.waitForTimeout(250)
    const hoverRead = hovered ? await readPair(i) : null
    const hover = hoverRead && !hoverRead.hidden ? hoverRead : null
    walked.push({ i, label: rest.label, cls: rest.cls, image_ground: rest.imageGround || Boolean(hover && hover.imageGround), rest: { ratio: rest.ratio, ground: rest.ground, ink: rest.ink }, hover: hover && { ratio: hover.ratio, ground: hover.ground, ink: hover.ink }, hovered })
    await page.mouse.move(0, 0).catch(() => {})
  }
  // Same-signature siblings (row S24): read at rest, never hovered; the worst stands for the sweep.
  const sibBelow = []; let sibRead = 0
  for (let j = 0; j < pickedInfo.extras; j++) {
    const r = await readPair(j, 'data-hx'); if (!r || r.hidden) continue
    sibRead++
    if (!r.imageGround && r.ratio < 4.5) sibBelow.push(r)
  }
  if (every) console.log(`HOVER-DETECT: ${pickedInfo.hoverRules} :hover rule selectors read from the stylesheets; ${pickedInfo.viaSheet} element(s) matched one with no hover: class token (counted before the signature dedupe)`)
  if (pickedInfo.extras) console.log(`ROW-SWEEP: ${sibRead} same-signature siblings read at rest (not hovered, ${pickedInfo.extras} tagged); below 4.5:1 ${sibBelow.length}`)
  // Grouped by (ink, ground, class): 44 rows of one defect print once with a count.
  const groups = new Map()
  for (const r of sibBelow) { const key = `${r.ink}/${r.ground}|${r.node || ''}|${r.cls}`; const g = groups.get(key); if (g) g.n++; else groups.set(key, { n: 1, r }) }
  for (const { n, r } of [...groups.values()].slice(0, 30)) console.log(`ROW-BELOW x${n} ${r.label} | rest ${r.ink}/${r.ground} ${r.ratio}:1 | ${r.cls}`)
  const skippedReads = await page.evaluate(() => window.__hwSkip || 0)
  console.log(`VISIBILITY-SKIPPED: ${skippedReads} text read(s) not visible at their centre (clipped, covered or under a backdrop), ungraded`)
  if (stepFailures) { console.log(`HOVER-WALK-INVALID: ${stepFailures} click/fill step(s) FAILED; the page is not in the state asked for and the numbers below are for the wrong page`); process.exitCode = 2 }
  // A ground painted by a background image (a gradient, a hero graphic) has no single colour: counted, never graded.
  const graded = walked.filter((w) => !w.image_ground)
  const below = graded.filter((w) => w.rest.ratio < 4.5 || (w.hover && w.hover.ratio < 4.5))
  console.log(`HOVER-WALK: ${walked.length} distinct clickable elements walked (cap ${cap}); ${walked.length - graded.length} on an image ground (not graded); hovered ${walked.filter((w) => w.hovered).length}; below 4.5:1 at rest ${graded.filter((w) => w.rest.ratio < 4.5).length}, on hover ${graded.filter((w) => w.hover && w.hover.ratio < 4.5).length}`)
  for (const w of below) console.log(`HOVER-BELOW ${w.label} | rest ${w.rest.ink}/${w.rest.ground} ${w.rest.ratio}:1 | hover ${w.hover ? `${w.hover.ink}/${w.hover.ground} ${w.hover.ratio}:1` : 'not hovered'} | ${w.cls}`)
  const { writeFileSync } = await import('node:fs')
  writeFileSync(out.replace(/\.png$/i, '') + '.hover-walk.json', JSON.stringify({ route, walked }, null, 1))
}
if (args.includes('--placeholders')) {
  // ::placeholder is not a text node, so --hover-walk never grades it. Ink: the pseudo-element's own colour, composited by
  // the field's opacity chain and the placeholder's own opacity; ground: the field's background layers up to the first
  // opaque one.
  const pairs = await page.evaluate(() => {
    const cv = document.createElement('canvas'); cv.width = cv.height = 1
    const cx = cv.getContext('2d', { willReadFrequently: true })
    const rgba = (v) => { if (!v || v === 'transparent') return [0, 0, 0, 0]; cx.clearRect(0, 0, 1, 1); cx.fillStyle = '#000'; cx.fillStyle = v; cx.fillRect(0, 0, 1, 1); const d = cx.getImageData(0, 0, 1, 1).data; return [d[0], d[1], d[2], d[3] / 255] }
    const lum = (c) => { const [r, g, b] = c.map((x) => { x /= 255; return x <= 0.03928 ? x / 12.92 : ((x + 0.055) / 1.055) ** 2.4 }); return 0.2126 * r + 0.7152 * g + 0.0722 * b }
    const out = []
    for (const el of document.querySelectorAll('input, select, textarea')) {
      if (el.matches('input[type=checkbox], input[type=radio], input[type=hidden], input[type=file], input[type=button], input[type=submit], input[type=reset], input[type=image], input[type=range], input[type=color]')) continue
      const r = el.getBoundingClientRect(); const cs = getComputedStyle(el)
      if (r.width < 8 || r.height < 8 || cs.visibility === 'hidden' || cs.display === 'none') continue
      const layers = []; let opq = false; let alpha = 1
      for (let n = el; n && n.nodeType === 1; n = n.parentElement) {
        alpha *= Number(getComputedStyle(n).opacity)
        if (!opq) { const c = rgba(getComputedStyle(n).backgroundColor); if (c[3] > 0) { layers.push(c); if (c[3] >= 1) opq = true } }
      }
      let ground = opq ? layers.pop().slice(0, 3) : [255, 255, 255]
      while (layers.length) { const c = layers.pop(); ground = ground.map((g, k) => c[k] * c[3] + g * (1 - c[3])) }
      const usePh = Boolean(el.getAttribute('placeholder')) && !el.value
      const ps = usePh ? getComputedStyle(el, '::placeholder') : cs; const ic = rgba(ps.color); const a = ic[3] * alpha * (usePh ? Number(ps.opacity === '' ? 1 : ps.opacity) : 1)
      const ink = ground.map((g, k) => ic[k] * a + g * (1 - a))
      const [h, l] = [lum(ground), lum(ink)].sort((p, q) => q - p)
      const hex = (c) => '#' + c.map((x) => Math.round(x).toString(16).padStart(2, '0')).join('').toUpperCase()
      out.push({ ratio: +((h + 0.05) / (l + 0.05)).toFixed(2), ink: hex(ink), ground: hex(ground), placeholder: (usePh ? 'placeholder ' + String(el.getAttribute('placeholder')) : el.tagName.toLowerCase() + (el.type ? '[' + el.type + ']' : '') + ' ' + String(el.tagName === 'SELECT' ? (el.options[el.selectedIndex]?.text ?? '') : el.value || '(empty)')).slice(0, 40), cls: (el.getAttribute('class') || '').slice(0, 100) })
    }
    return out
  })
  const bad = pairs.filter((x) => x.ratio < 4.5)
  if (stepFailures) { console.log(`PLACEHOLDERS-INVALID: ${stepFailures} click/fill step(s) FAILED; the page is not in the state asked for`); process.exitCode = 2 }
  console.log(`PLACEHOLDERS: ${pairs.length} visible input/select/textarea fields graded; below 4.5:1 ${bad.length}`)
  for (const x of bad) console.log(`PLACEHOLDER-BELOW "${x.placeholder}" | ${x.ink}/${x.ground} ${x.ratio}:1 | ${x.cls}`)
}
if (args.includes('--state-table')) {
  // FWD-13: the table names tokens (`--name`) or literal hex; a ground may carry an `overlay` [color, alpha] painted over
  // it, and a pair an `opacity` (the whole element at that alpha over the world's base). Resolution is live, on body.
  const table = JSON.parse(readFileSync(args[args.indexOf('--state-table') + 1], 'utf8'))
  const names = new Set()
  const collect = (v) => { if (typeof v === 'string' && v.startsWith('--')) names.add(v) }
  for (const w of Object.values(table.worlds)) collect(w.base)
  for (const role of Object.values(table.roles)) for (const world of Object.values(role)) for (const pair of Object.values(world)) {
    collect(pair.ground); collect(pair.ink); if (pair.overlay) collect(pair.overlay[0])
  }
  const raw = await page.evaluate((list) => Object.fromEntries(list.map((n) => [n, getComputedStyle(document.body).getPropertyValue(n).trim()])), [...names])
  const hsl2rgb = (h, s, l) => { s /= 100; l /= 100; const k = (n) => (n + h / 30) % 12; const a = s * Math.min(l, 1 - l)
    const f = (n) => l - a * Math.max(-1, Math.min(k(n) - 3, 9 - k(n), 1)); return [f(0), f(8), f(4)].map((x) => Math.round(x * 255)) }
  const parse = (v) => {
    let m
    if ((m = /^#([0-9a-f]{6})$/i.exec(v))) return [0, 2, 4].map((i) => parseInt(m[1].slice(i, i + 2), 16))
    if ((m = /^(-?[\d.]+)(?:deg)?\s+([\d.]+)%\s+([\d.]+)%$/.exec(v))) return hsl2rgb(+m[1], +m[2], +m[3])
    if ((m = /^rgba?\(\s*(\d+)[ ,]+(\d+)[ ,]+(\d+)/.exec(v))) return [+m[1], +m[2], +m[3]]
    return null
  }
  const color = (v) => parse(typeof v === 'string' && v.startsWith('--') ? raw[v] : v)
  const mix = (top, under, a) => top.map((c, i) => Math.round(c * a + under[i] * (1 - a)))
  const lum = (rgb) => { const [r, g, b] = rgb.map((c) => { c /= 255; return c <= 0.03928 ? c / 12.92 : ((c + 0.055) / 1.055) ** 2.4 }); return 0.2126 * r + 0.7152 * g + 0.0722 * b }
  const ratio = (x, y) => { const [a, b] = [lum(x), lum(y)].sort((p, q) => q - p); return (a + 0.05) / (b + 0.05) }
  const hex = (rgb) => '#' + rgb.map((c) => c.toString(16).padStart(2, '0')).join('').toUpperCase()
  const rows = []; const unresolved = new Set()
  const roles = Object.keys(table.roles); const states = table.states; const worlds = Object.keys(table.worlds)
  for (const role of roles) for (const world of worlds) for (const state of states) {
    const pair = table.roles[role][world]?.[state]
    if (!pair) { rows.push({ role, world, state, verdict: 'n/a' }); continue }
    const base = color(table.worlds[world].base)
    let ground = color(pair.ground === 'base' ? table.worlds[world].base : pair.ground); let ink = color(pair.ink)
    if (!base || !ground || !ink) { [table.worlds[world].base, pair.ground, pair.ink].forEach((t) => { if (typeof t === 'string' && t.startsWith('--') && !color(t)) unresolved.add(t) }); rows.push({ role, world, state, verdict: 'UNRESOLVED' }); continue }
    if (pair.overlay) { const o = color(pair.overlay[0]); if (o) ground = mix(o, ground, pair.overlay[1]) }
    if (pair.opacity !== undefined) { ground = mix(ground, base, pair.opacity); ink = mix(ink, ground, pair.opacity) }
    const restPair = table.roles[role][world]?.rest
    let restGround = null
    if (restPair && state !== 'rest') { restGround = color(restPair.ground === 'base' ? table.worlds[world].base : restPair.ground); if (restGround && restPair.overlay) { const o = color(restPair.overlay[0]); if (o) restGround = mix(o, restGround, restPair.overlay[1]) } }
    const bar = pair.kind === 'nonText' ? 3 : 4.5
    const r = ratio(ground, ink)
    rows.push({ role, world, state, ground: hex(ground), ink: hex(ink), ratio: +r.toFixed(2), bar, verdict: r >= bar ? 'PASS' : 'FAIL',
      separation_from_rest: restGround ? +ratio(ground, restGround).toFixed(2) : null, ground_token: pair.ground, ink_token: pair.ink, note: pair.note ?? null })
  }
  const declared = rows.filter((r) => r.verdict !== 'n/a')
  console.log(`STATE-TABLE: ${roles.length} roles x ${states.length} states x ${worlds.length} worlds = ${rows.length} cells; ${declared.length} declared, ${rows.length - declared.length} n/a; FAIL ${declared.filter((r) => r.verdict === 'FAIL').length}; UNRESOLVED ${declared.filter((r) => r.verdict === 'UNRESOLVED').length}${unresolved.size ? ' (' + [...unresolved].join(', ') + ')' : ''}`)
  for (const r of declared) console.log(`STATE ${r.role} | ${r.world} | ${r.state} | ${r.ground ?? '-'} / ${r.ink ?? '-'} | ${r.ratio ?? '-'}:1 vs ${r.bar ?? '-'} | ${r.verdict}${r.separation_from_rest !== null && r.separation_from_rest !== undefined ? ` | sep ${r.separation_from_rest}:1` : ''}`)
  const { writeFileSync } = await import('node:fs')
  writeFileSync(out.replace(/\.png$/i, '') + '.state-table.json', JSON.stringify({ table: args[args.indexOf('--state-table') + 1], resolved: raw, rows }, null, 1))
}
if (args.includes('--density')) {
  // The page column is the page end's parent; with no page end, the first element under <main> holding more than one
  // child. Sections are its non-empty children other than the page end.
  const d = await page.evaluate(() => {
    const main = document.querySelector('main')
    if (!main) return null
    const end = main.querySelector('[data-page-end]')
    let col = end ? end.parentElement : main
    while (!end && col.children.length === 1) col = col.children[0]
    const top = (el) => el.getBoundingClientRect().top + window.scrollY
    const bottom = (el) => el.getBoundingClientRect().bottom + window.scrollY
    const sections = [...col.children].filter((el) => !el.hasAttribute('data-page-end') && el.getBoundingClientRect().height > 0)
    const last = sections.length ? Math.max(...sections.map(bottom)) : null
    const docH = Math.max(document.documentElement.scrollHeight, window.innerHeight)
    const pads = {}
    for (const el of main.querySelectorAll('.rounded-b-lg')) { const p = getComputedStyle(el).paddingTop; pads[p] = (pads[p] ?? 0) + 1 }
    return {
      vh: window.innerHeight, docH, last: last === null ? null : Math.round(last), sections: sections.length,
      gaps: sections.slice(1).map((el, i) => Math.round(top(el) - bottom(sections[i]))), pads,
      endGap: end && last !== null ? Math.round(top(end) - last) : null, end: end ? end.textContent : null,
    }
  })
  if (!d) console.log('DENSITY: no <main> on the page')
  else {
    const below = d.last === null ? null : Math.min(1, Math.max(0, (d.docH - d.last) / d.vh))
    console.log(`DENSITY: below-last-content ${below === null ? 'n/a' : (below * 100).toFixed(1) + '%'} of the ${d.vh}px viewport (doc ${d.docH}px, last content ${d.last}px, ${d.sections} sections); between-section gaps ${JSON.stringify(d.gaps)}; panel inner padding census ${JSON.stringify(d.pads)}; page end ${d.end === null ? 'none' : `gap ${d.endGap}px "${d.end}"`}`)
  }
}
await page.screenshot({ path: out, fullPage: true })
console.log('SAVED :', out)
if (netlogPath) {
  const { writeFileSync } = await import('node:fs')
  writeFileSync(netlogPath, netlog.join('\n') + '\n')
  // Print the DENOMINATOR beside the artifact: a netlog is an enumeration, and an enumeration
  // reported without its count invites the reader to supply one.
  console.log('NETLOG:', netlogPath, '--', netlog.length,
    `requests recorded WITHIN a ${WAIT}ms post-load` + (steps.length ? ` + ${steps.length}x${CLICKWAIT}ms post-step` : '') + ' window')
  console.log('NETLOG-WINDOW: an absence here is an absence WITHIN THAT WINDOW only --',
    'a request still in flight at close fires neither handler and is recorded by nothing.')
}
console.log('NOW READ THE PNG against portal/DESIGN.md. Check: light text/buttons only on the ONE inverted band (--bg-band; check DESIGN.md/index.css for the header/strip vs body rung values), never on the canvas or a white panel; panel headers carry the actions; canvas-level errors are navy text beside a status icon. A rejection cites the clause NUMBER (C3, C5.8, ...).')
if (fixtureKeys.length) {
  const dead = fixtureKeys.filter(k => fixtureHits[k].size === 0)
  const multi = fixtureKeys.filter(k => fixtureHits[k].size > 1)
  console.log('FIXTURES:', fixtureKeys.length, 'declared;', fixtureKeys.length - dead.length, 'matched >=1 URL')
  fixturesMatched = fixtureKeys.length - dead.length
  // FE-s-65: WIRE MATCH (the CTO's round-10 criterion rule, part (a)) -- the fixture's keys equal
  // the operation keys the run actually exercised. Plain, no colour codes (a template literal),
  // so a strict-mode consumer can grep it without stripping ANSI.
  console.log(`FIXTURES-MATCH: matched ${fixturesMatched} of ${fixtureKeys.length}`)
  // FE-s-74 (C-S147): FIXTURES-MATCH above answers FULFILMENT -- which declared URLs were
  // actually hit at runtime. It never asks VALIDITY -- whether those URL keys are real
  // operation keys this client's own contract names -- so an arbitrary invalid key could
  // read fully "matched" while naming an endpoint the client does not call. This is a
  // SEPARATE, additive line answering the second question; FIXTURES-MATCH is untouched.
  const keyValidity = checkKeyValidity(fixtureKeys, fixturesPath)
  if (keyValidity) {
    console.log(`KEY-VALIDITY: ${keyValidity.valid} of ${keyValidity.total} valid consumed.ts operation keys`)
  } else {
    console.log('KEY-VALIDITY: UNMEASURABLE (no contracts/wire/consumed.ts found for this fixture\'s page)')
  }
  if (dead.length) {
    console.log('FIXTURE-DEAD (declared, NEVER matched -- a state you did not actually construct):',
      dead.join(' | '))
  }
  for (const k of multi) {
    console.log(`FIXTURE-MULTI: '${k}' served ${fixtureHits[k].size} distinct URLs ` +
      '(intentional for a family; a DEFECT if these are different endpoints)')
  }
  for (const [a, b] of shadowPairs) {
    console.log(`FIXTURE-SHADOW-RISK: '${a}' is a substring of '${b}' ` +
      '-- longest-match gives B, so A only ever serves URLs that do NOT contain B')
  }
}
await browser.close()

// FE-s-74 HARDENING: an UNMEASURABLE style/ground read is not a plain FAIL -- it means the
// assertion COULD NOT be evaluated at all, and reporting it as though the run merely
// "failed" (exit 0, business as usual) is exactly the silent-wrong-value failure mode this
// TO exists to close. So this exits non-zero UNCONDITIONALLY, never gated behind --strict.
if (anyUnmeasurable) process.exitCode = 1

// FE-s-65: --strict -- process.exitCode = 1 after the browser closes when any expectation
// (content, style or ground) failed, OR FIXTURES-MATCH read M below N.
if (strict) {
  const anyExpectationFailed = [...contentResults, ...styleResults, ...groundResults].some(p => !p)
  const fixturesShort = fixturesMatched !== null && fixturesMatched < fixtureKeys.length
  if (anyExpectationFailed || fixturesShort) process.exitCode = 1
}
