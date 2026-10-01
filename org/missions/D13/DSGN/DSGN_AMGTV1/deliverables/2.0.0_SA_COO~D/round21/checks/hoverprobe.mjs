// hoverprobe.mjs -- DSGN_AMGTV1 round 21 (issuer 2.0.0_SA_COO~D): the live read of the figure tooltip that walk.mjs cannot make
// (walk.mjs never hovers; it only flags a tooltip left open by chance).
//
// Usage (repo root): node <this file> [--security "BA US"] [--base http://localhost:5174]
// CTO rulings 27914 + 27927: the Financials pop-up tooltip unclipped with no CURR_*-style code on its face, and one Model-tab figure the
// same. The probe HOVERS every figure row of the Financials and Market Features pop-ups, every header card, and the first Model-tab
// figures, and for each open tooltip measures:
//   CLIP  -- the tooltip box lies inside every ancestor whose overflow is not visible, and inside the viewport;
//   COVER -- of 9 sample points, none is covered by another element (walk.mjs's occluded-popover test);
//   CODE  -- the visible text holds no capitals_underscore token (CURR_ENTP_VAL);
//   CARRY -- the tooltip carries data-mnemonic.
// The walker account lease is walk.mjs's own: arm (HOLDER), secret, and a holder-only disarm in finally. Writes are blocked except
// login/refresh/logout; telemetry is answered locally. Prints one line per tooltip and "HOVER PROBE: <ok> of <n> tooltips clean".
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
const opt = { base: 'http://localhost:5174', security: 'BA US' }
for (let i = 0; i < argv.length; i++) {
  if (argv[i] === '--base') opt.base = argv[++i]
  else if (argv[i] === '--security') opt.security = argv[++i]
}
const stamp = new Date().toISOString().replace(/[-:]/g, '').replace(/\.\d+Z$/, 'Z')
const OUT = path.join(path.dirname(fileURLToPath(import.meta.url)), '..', 'walk', `hover-${stamp}`)
fs.mkdirSync(OUT, { recursive: true })
const py = (cmd, extraEnv = {}, ...args) => execFileSync('python', [ACCOUNT, cmd, ...args], { encoding: 'utf8', env: { ...process.env, ...extraEnv }, stdio: ['ignore', 'pipe', 'pipe'] })
const log = (...a) => console.log(new Date().toISOString().slice(11, 19), ...a)
const ADMITTED_POST = [/\/auth\/login$/, /\/auth\/refresh$/, /\/auth\/logout$/]
const settle = async (page, ms = 1200) => { await page.waitForLoadState('networkidle', { timeout: 35000 }).catch(() => {}); await page.waitForTimeout(ms) }

const MEASURE = (tip) => {
  const r = tip.getBoundingClientRect()
  const faults = []
  // <body> is skipped: its rect scrolls with the page (it reads negative once scrolled), and the viewport test below covers it.
  for (let e = tip.parentElement; e && e !== document.body && e !== document.documentElement; e = e.parentElement) {
    const s = getComputedStyle(e)
    if (s.overflow === 'visible' && s.overflowX === 'visible' && s.overflowY === 'visible') continue
    const a = e.getBoundingClientRect()
    if (r.top < a.top - 1 || r.bottom > a.bottom + 1 || r.left < a.left - 1 || r.right > a.right + 1) {
      faults.push(`CLIP: crosses a clipping ancestor <${e.tagName.toLowerCase()} class="${String(e.className).slice(0, 60)}"> (tip ${Math.round(r.top)}-${Math.round(r.bottom)}, box ${Math.round(a.top)}-${Math.round(a.bottom)})`)
      break
    }
  }
  if (r.top < 0 || r.left < 0 || r.bottom > innerHeight || r.right > innerWidth) faults.push(`CLIP: outside the viewport (${Math.round(r.top)},${Math.round(r.bottom)})`)
  // The tooltip is pointer-events-none, which elementFromPoint skips (walk.mjs's occluded-popover reads 9 of 9 on it for that reason).
  // Hit-test with pointer events on for the tooltip subtree only, then restore.
  const pe = document.createElement('style')
  pe.textContent = '[data-hoverprobe-tip], [data-hoverprobe-tip] * { pointer-events: auto !important; }'
  tip.setAttribute('data-hoverprobe-tip', '')
  document.head.appendChild(pe)
  let covered = 0
  for (const fx of [0.2, 0.5, 0.8]) for (const fy of [0.1, 0.5, 0.9]) {
    const x = r.left + r.width * fx; const y = r.top + r.height * fy
    if (x < 0 || y < 0 || x >= innerWidth || y >= innerHeight) continue
    const top = document.elementFromPoint(x, y)
    if (top && !tip.contains(top)) covered++
  }
  pe.remove(); tip.removeAttribute('data-hoverprobe-tip')
  if (covered) faults.push(`COVER: ${covered} of 9 sample points covered`)
  const text = tip.innerText.replace(/\s+/g, ' ').trim()
  const code = /\b[A-Z][A-Z0-9]*_[A-Z0-9_]+\b/.exec(text)
  if (code) faults.push(`CODE: "${code[0]}" on the face`)
  if (!tip.getAttribute('data-mnemonic')) faults.push('CARRY: no data-mnemonic')
  return { faults, text: text.slice(0, 140), box: [Math.round(r.left), Math.round(r.top), Math.round(r.width), Math.round(r.height)], mnemonic: tip.getAttribute('data-mnemonic') }
}

const results = []
let n = 0
async function hoverAll(page, anchorSel, label, limit = 12, optional = false) {
  const anchors = page.locator(anchorSel)
  const k = Math.min(await anchors.count().catch(() => 0), limit)
  if (!k && optional) { log(`n/a ${label}: none on this name (${anchorSel})`); return }
  if (!k) { results.push({ where: label, faults: [`MISSING: no anchor ${anchorSel}`] }); return }
  for (let i = 0; i < k; i++) {
    const a = anchors.nth(i)
    await a.scrollIntoViewIfNeeded().catch(() => {})
    // Place the anchor mid-viewport (as a reader scrolls to it; an upward or a downward tooltip both fit); scrollIntoViewIfNeeded leaves it at the bottom edge,
    // where a downward tooltip reads as off-screen. Inside a pop-up the dialog does not scroll, so this is a no-op there.
    if (!label.endsWith('-popup')) await a.evaluate((el) => window.scrollBy(0, el.getBoundingClientRect().top - 420)).catch(() => {})
    await a.hover({ timeout: 3000 }).catch(() => {})
    await page.waitForTimeout(250)
    const tip = a.locator('[role=tooltip]').first()
    // A row whose figure is not carried renders no tooltip at all (HeaderCards tooltipOf returns null): nothing to grade.
    if (!(await tip.count().catch(() => 0))) { log(`n/a ${label} #${i + 1}: no tooltip in the markup (figure not carried)`); continue }
    if (!(await tip.isVisible().catch(() => false))) { results.push({ where: `${label} #${i + 1}`, faults: ['OPEN: no tooltip became visible on hover'] }); continue }
    const m = await tip.evaluate(MEASURE)
    n += 1
    const shot = `${String(n).padStart(2, '0')}-${label.replace(/\W+/g, '-')}-${i + 1}.png`
    await page.screenshot({ path: path.join(OUT, shot) })
    results.push({ where: `${label} #${i + 1}`, shot, ...m })
  }
}

let holder = null
let armed = false
let browser
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
  await page.goto(opt.base + '/login', { waitUntil: 'domcontentloaded', timeout: 30000 })
  await page.fill('#email', EMAIL); await page.fill('#password', password.trim()); await page.click('button[type=submit]')
  await page.waitForURL((u) => !/\/login/.test(u.pathname), { timeout: 30000 }).catch(() => {})
  if (/\/login/.test(new URL(page.url()).pathname)) throw new Error('login did not complete')
  log('LOGGED IN')
  await page.goto(opt.base + '/security-analysis', { waitUntil: 'domcontentloaded', timeout: 30000 }); await settle(page, 2500)
  const row = page.getByText(opt.security, { exact: true }).first()
  if (!(await row.click({ timeout: 4000 }).then(() => true).catch(() => false))) {
    const box = page.getByPlaceholder('Search any ticker'); await box.fill(opt.security); await box.press('Enter')
  }
  await settle(page, 2500)
  await page.mouse.move(5, 5)
  await hoverAll(page, 'div.group:has(> [data-header-card])', 'header-card', 4)
  for (const card of ['FINANCIALS', 'MARKET FEATURES']) {
    const opener = page.locator(`[aria-label^="${card.charAt(0) + card.slice(1).toLowerCase()} - open details" i]`).first()
    if (!(await opener.click({ timeout: 4000 }).then(() => true).catch(() => false))) { results.push({ where: `${card} pop-up`, faults: ['MISSING: the card did not open'] }); continue }
    await page.waitForTimeout(600)
    await hoverAll(page, '[role=dialog] .group', `${card}-popup`)
    await page.keyboard.press('Escape'); await page.waitForTimeout(400)
  }
  let tabbed = await page.getByRole('tab', { name: /^model$/i }).first().click({ timeout: 4000 }).then(() => true).catch(() => false)
  if (!tabbed) tabbed = await page.locator('button').filter({ hasText: /^\s*model\s*$/i }).first().click({ timeout: 4000 }).then(() => true).catch(() => false)
  if (!tabbed) results.push({ where: 'model tab', faults: ['MISSING: the Model tab did not open'] })
  await settle(page, 2000)
  await page.mouse.move(5, 5)
  // The sheet's figure cells (ModelTab.tsx:136-150) and the what-moved lines (:648-656, their own rows incl. a "mnemonic" row).
  // One cell per row, three rows (the first three anchors were all the first row's cells).
  await hoverAll(page, 'tr:nth-child(-n+3) > td.group:has(> [data-figure-tooltip]):first-of-type, tr:nth-child(-n+3) > td.group:has(> [data-figure-tooltip]):nth-of-type(2)', 'model-cell', 3)
  await hoverAll(page, 'li.group[data-model-change]', 'model-what-moved', 3, true)
} catch (e) {
  results.push({ where: 'probe', faults: [`ERROR: ${String(e.message).split('\n')[0]}`] })
} finally {
  if (browser) await browser.close().catch(() => {})
  if (armed) { try { log(py('disarm', {}, holder).trim().split('\n').slice(-3).join(' | ')) } catch (e) { log(`DISARM FAILED -- run: python .claude/skills/ui-walk/ui_walker_account.py disarm ${holder}`) } }
}
let ok = 0
for (const r of results) {
  const clean = r.faults.length === 0
  if (clean) ok += 1
  console.log(`${clean ? 'CLEAN' : 'FAULT'} ${r.where}${r.mnemonic ? ` [${r.mnemonic}]` : ''} :: ${clean ? r.text : r.faults.join(' | ')}${r.shot ? ` (${r.shot})` : ''}`)
}
fs.writeFileSync(path.join(OUT, 'hover.json'), JSON.stringify({ base: opt.base, security: opt.security, results }, null, 1))
console.log(`OUT ${OUT}`)
console.log(`HOVER PROBE: ${ok} of ${results.length} tooltips clean`)
process.exit(ok === results.length && results.length > 0 ? 0 : 1)
