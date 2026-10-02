// servedread.mjs -- DSGN_AMGTV1 served re-read (issuer 2.0.0_SA_COO~D, 2026-10-02): FWD-2 and FWD-24 on SERVED data, the read that
// walk.mjs cannot make (it never hovers and keeps no payloads).
//
// Usage (repo root): node <this file> [--base http://localhost:5174] [--names "BA US,VLO US,AMD US"]
// Why now: CTO msg 28577 ruled "the next DSGN act is the served re-read" once a producer cell lands. AMGT_RESAPP r63 AMGT-am-3
// (chatter rows serve ticker / classification / places_moved; AMENDMENT 1: the overlay breakout_price row serves places_moved) is in
// the code am-6 leg 1 deployed (4197279e67, NEVER-2 entry closed @6e67441488).
// What it reads, with the page at <base> (5174 = portal PROD's tree on the live backend):
//   FWD-2 BUBBLES -- the first 3 [data-bubble] marks: their SVG <title> against the served collected-chatter row (every served
//                    identity field present; a null one said "not served"; no code-shaped token).
//   FWD-2 BARS    -- the 3 largest-move [data-price-bar] marks: their title against the served price ranking row.
//   FWD-24 HEADER -- for each name: the "Breakout (price)" cell text against the served overlay's breakout_price.places_moved
//                    (a served number prints in words; a null is reported with its served reason).
// The walker account lease is walk.mjs's own (arm HOLDER, secret, holder-only disarm in finally). Only GET/HEAD/OPTIONS and
// login/refresh/logout pass; telemetry is answered locally. Prints one line per mark and three tallies; exit 0 only when all pass.
import { createRequire } from 'module'
import { execFileSync } from 'child_process'
import fs from 'fs'
import path from 'path'
import { fileURLToPath } from 'url'

const ROOT = process.cwd()
const require = createRequire(path.join(ROOT, 'portal', 'package.json'))
const { chromium } = require('playwright-core')
const ACCOUNT = path.join(ROOT, '.claude', 'skills', 'ui-walk', 'ui_walker_account.py')
const EMAIL = 'opal-ui-walker@opal.test'
const argv = process.argv.slice(2)
const opt = { base: 'http://localhost:5174', names: ['BA US', 'VLO US', 'AMD US'] }
for (let i = 0; i < argv.length; i++) {
  if (argv[i] === '--base') opt.base = argv[++i]
  else if (argv[i] === '--names') opt.names = argv[++i].split(',').map((s) => s.trim()).filter(Boolean)
}
const stamp = new Date().toISOString().replace(/[-:]/g, '').replace(/\.\d+Z$/, 'Z')
const OUT = path.join(path.dirname(fileURLToPath(import.meta.url)), `read-${stamp}`)
fs.mkdirSync(OUT, { recursive: true })
const py = (cmd, extraEnv = {}, ...args) => execFileSync('python', [ACCOUNT, cmd, ...args], { encoding: 'utf8', env: { ...process.env, ...extraEnv }, stdio: ['ignore', 'pipe', 'pipe'] })
const log = (...a) => console.log(new Date().toISOString().slice(11, 19), ...a)
const ADMITTED_POST = [/\/auth\/login$/, /\/auth\/refresh$/, /\/auth\/logout$/]
const settle = async (page, ms = 1200) => { await page.waitForLoadState('networkidle', { timeout: 35000 }).catch(() => {}); await page.waitForTimeout(ms) }
const CODE = /\b[a-z]+_[a-z0-9_]+\b|_Equity\b|\.json\b|\b[A-Z][A-Z0-9]*_[A-Z0-9_]+\b/
const lc = (s) => String(s ?? '').toLowerCase()
const unwrap = (d) => (d && d.payload ? d.payload : d)
const movedRe = (n) => (n === 0 ? /no change|unchanged/i : new RegExp(`\\b(up|down)\\s+${Math.abs(n)}\\s+place`, 'i'))

// Every served identity field present in the hover (null ones said "not served"); no code-shaped token.
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

const served = { collected: null, price: null, overlay: {} }
const results = { bubbles: [], bars: [], header: [] }
let holder = null; let armed = false; let browser
try {
  const armOut = py('arm'); log(armOut.trim().split('\n').slice(-2).join(' | '))
  holder = (armOut.match(/^HOLDER (\S+)/m) || [])[1] || null; armed = true
  const password = py('secret', { UI_WALK_CHILD: '1' })
  try { browser = await chromium.launch({ channel: 'msedge', headless: true }) } catch { browser = await chromium.launch({ headless: true }) }
  const page = await (await browser.newContext({ viewport: { width: 1440, height: 900 } })).newPage()
  await page.route('**/*', (route) => {
    const req = route.request(); const m = req.method(); const p = new URL(req.url()).pathname
    if (m === 'GET' || m === 'HEAD' || m === 'OPTIONS' || ADMITTED_POST.some((re) => re.test(p))) return route.continue()
    if (/\/analytics\/ingest$/.test(p)) return route.fulfill({ status: 204, body: '' })
    return route.abort('blockedbyclient')
  })
  page.on('response', async (resp) => {
    const p = new URL(resp.url()).pathname
    if (!/\/api\/scoped\/amgt\//.test(p) || resp.status() !== 200) return
    const body = await resp.json().catch(() => null); if (!body) return
    if (/\/lead-panel\/timeseries\/collected\/chatter$/.test(p)) served.collected = unwrap(body)
    else if (/\/lead-panel\/rankings\/trending\/price$/.test(p)) served.price = unwrap(body)
    else { const k = p.match(/\/security\/([^/]+)\/overlay$/); if (k) served.overlay[decodeURIComponent(k[1])] = unwrap(body) }
  })
  await page.goto(opt.base + '/login', { waitUntil: 'domcontentloaded', timeout: 30000 })
  await page.fill('#email', EMAIL); await page.fill('#password', password.trim()); await page.click('button[type=submit]')
  await page.waitForURL((u) => !/\/login/.test(u.pathname), { timeout: 30000 }).catch(() => {})
  if (/\/login/.test(new URL(page.url()).pathname)) throw new Error('login did not complete')
  log('LOGGED IN')
  await page.goto(opt.base + '/security-analysis', { waitUntil: 'domcontentloaded', timeout: 30000 }); await settle(page, 3000)

  // FWD-2 BUBBLES (the default Chatter face).
  const bubbles = await page.evaluate(() => [...document.querySelectorAll('[data-bubble]')].map((el) => {
    const t = el.querySelector('title') || (el.parentElement && el.parentElement.querySelector(':scope > title'))
    return { key: el.getAttribute('data-bubble'), hover: (el.getAttribute('title') || (t ? t.textContent : '') || '').replace(/\s+/g, ' ').trim() }
  }))
  await page.screenshot({ path: path.join(OUT, '01-chatter.png') })
  const crow = new Map(((served.collected && served.collected.rows) || []).map((r) => [r.security_key, r]))
  for (const b of bubbles.filter((x) => crow.has(x.key)).slice(0, 3)) {
    results.bubbles.push({ key: b.key, hover: b.hover, faults: identityFaults(b.hover, crow.get(b.key)) })
  }
  if (bubbles.length === 0) results.bubbles.push({ key: '-', hover: '', faults: ['no [data-bubble] mark drawn'] })

  // FWD-2 BARS (the Price face).
  const seg = await page.getByRole('button', { name: /^price$/i }).first().click({ timeout: 4000 }).then(() => true)
    .catch(() => page.getByText('Price', { exact: true }).first().click({ timeout: 4000 }).then(() => true).catch(() => false))
  if (!seg) results.bars.push({ key: '-', hover: '', faults: ['the Price segment did not open'] })
  await settle(page, 2500)
  // The Price face's read can land after network-idle: wait for the drawn bars AND the captured payload (up to 30 s).
  await page.waitForSelector('[data-price-bar]', { timeout: 30000 }).catch(() => {})
  for (let i = 0; i < 30 && !(served.price && served.price.rows && served.price.rows.length); i++) await page.waitForTimeout(1000)
  const bars = await page.evaluate(() => [...document.querySelectorAll('[data-price-bar]')].map((el) => ({ key: el.getAttribute('data-price-bar'), hover: (el.getAttribute('title') || '').replace(/\s+/g, ' ').trim() })))
  await page.screenshot({ path: path.join(OUT, '02-price.png') })
  // The served period figure: the fixture's `return_30d_pct`, else the first numeric *_pct field the live row carries.
  const figOf = (r) => (typeof r.return_30d_pct === 'number' ? r.return_30d_pct
    : Object.entries(r).filter(([k, v]) => /_pct$/.test(k) && typeof v === 'number').map(([, v]) => v)[0])
  served.priceRowKeys = served.price && served.price.rows && served.price.rows[0] ? Object.keys(served.price.rows[0]) : []
  const prows = ((served.price && served.price.rows) || []).filter((r) => typeof figOf(r) === 'number')
  const byKey = new Map(prows.map((r) => [r.security_key || r.ticker, r]))
  const top = [...prows].sort((a, b) => Math.abs(figOf(b)) - Math.abs(figOf(a))).slice(0, 3)
  for (const r of top) {
    const k = r.security_key || r.ticker; const bar = bars.find((x) => x.key === k)
    results.bars.push({ key: k, hover: bar ? bar.hover : '', faults: bar ? identityFaults(bar.hover, byKey.get(k), Math.abs(figOf(r)).toFixed(1)) : ['no bar for this served row'] })
  }

  // FWD-24 HEADER: the Breakout (price) cell for each name.
  for (const name of opt.names) {
    const box = page.getByPlaceholder('Search any ticker'); await box.fill(name); await box.press('Enter'); await settle(page, 3500)
    const text = await page.evaluate(() => {
      const lab = [...document.querySelectorAll('div')].find((d) => d.textContent && d.textContent.trim() === 'Breakout (price)' && d.children.length === 0)
      return lab && lab.parentElement ? lab.parentElement.innerText.replace(/\s+/g, ' ').trim() : null
    })
    await page.screenshot({ path: path.join(OUT, `03-header-${name.replace(/\W+/g, '-')}.png`) })
    const key = name
    const ov = served.overlay[name] || served.overlay[name.replace(/ /g, '_') + '_Equity'] // the live route is keyed by the ticker ("BA US")
    const findRow = (o) => { if (!o || typeof o !== 'object') return null; if (o.breakout_price) return o.breakout_price; for (const v of Object.values(o)) { const r = findRow(v); if (r) return r } return null }
    const row = findRow(ov)
    const f = []
    if (!text) f.push('no Breakout (price) cell read')
    if (!ov) f.push('no overlay payload captured')
    else if (!row) f.push('the overlay serves no breakout_price row')
    else if (typeof row.places_moved === 'number') { if (!movedRe(row.places_moved).test(text || '')) f.push(`served places_moved ${row.places_moved} not printed`) }
    else f.push(`served places_moved null (reason: ${row.places_moved_reason ?? 'none served'})`)
    results.header.push({ key, text, served: row ? { rank: row.rank, places_moved: row.places_moved, places_moved_reason: row.places_moved_reason } : null, faults: f })
    // An open name replaces the universe panel (and its search box); go back before the next name.
    await page.getByRole('button', { name: /back to universe/i }).first().click({ timeout: 5000 }).catch(() => {})
    await settle(page, 2000)
  }
} catch (e) {
  results.header.push({ key: 'probe', text: null, faults: [`ERROR: ${String(e.message).split('\n')[0]}`] })
} finally {
  if (browser) await browser.close().catch(() => {})
  if (armed) { try { log(py('disarm', {}, holder).trim().split('\n').slice(-3).join(' | ')) } catch (e) { log(`DISARM FAILED -- run: python .claude/skills/ui-walk/ui_walker_account.py disarm ${holder}`) } }
}
const census = (rows, f) => `${rows.filter(f).length} of ${rows.length}`
const crows = (served.collected && served.collected.rows) || []
console.log(`SERVED collected-chatter rows carrying ticker: ${census(crows, (r) => r.ticker)}; classification: ${census(crows, (r) => r.classification)}; places_moved number: ${census(crows, (r) => typeof r.places_moved === 'number')}`)
let all = true
for (const [k, list] of Object.entries(results)) {
  for (const r of list) console.log(`${r.faults.length ? 'FAULT' : 'CLEAN'} ${k} ${r.key} :: ${r.faults.length ? r.faults.join(' | ') : (r.hover || r.text)}`)
  const ok = list.filter((r) => r.faults.length === 0).length
  if (ok !== list.length || list.length === 0) all = false
  console.log(`${k.toUpperCase()}: ${ok} of ${list.length} clean`)
}
fs.writeFileSync(path.join(OUT, 'servedread.json'), JSON.stringify({ base: opt.base, names: opt.names, results, served: { collected_rows: crows.length, price_rows: ((served.price && served.price.rows) || []).length, overlays: Object.keys(served.overlay), price_row_keys: served.priceRowKeys || [] } }, null, 1))
console.log(`OUT ${OUT}`)
process.exit(all ? 0 : 1)
