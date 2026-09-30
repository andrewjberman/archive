/**
 * DSGN_IRPTV1 FAST item 42 (W2-22 remainder) -- a model picked inside the card's breakdown scopes the map and the
 * table, which read it back. Fixture plane on the local dev build (same recipe as items 36-41; nothing reaches the
 * live backend). The Cottonwood holdings fixture carries no model layer, so the driver injects the served shape
 * IB-mr-202 publishes (ACCOUNT -> CATEGORY "Models" -> MODEL -> SECURITY) and reports what the page does with it.
 *
 * Usage: node .runtmp/w2-22-model-scope-driver.mjs <port> <out.png>
 */
import { chromium } from 'playwright-core'
import { readFileSync, writeFileSync, mkdirSync } from 'node:fs'
import { dirname } from 'node:path'

const PORT = process.argv[2] || '5174'
const OUT = process.argv[3] || '.runtmp/w2-22.fast-run.png'
mkdirSync(dirname(OUT), { recursive: true })
const ORIGIN = `http://localhost:${PORT}`
const EDGE = 'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe'
const CORS = {
  'Access-Control-Allow-Origin': ORIGIN, 'Access-Control-Allow-Credentials': 'true',
  'Access-Control-Allow-Headers': '*', 'Access-Control-Allow-Methods': '*', 'Content-Type': 'application/json',
}
const SESSION = {
  accessToken: 'ui-smoke-token',
  user: { email: 'dev@opalcapital.com', name: 'Dev User', role: 'admin', userType: 'Dev', firmId: 'opal-capital',
          firmRole: null, advisorId: null, advisorRole: null, mustChangePassword: false },
}
const BASE = '/api/scoped/investor-reporting'
const MODEL = 'Core Growth Model'
const cottonwood = JSON.parse(readFileSync('src/pages/InvestorReporting/fixtures/smoke/dsgn-irptv1-cottonwood.json', 'utf8'))
const firmId = cottonwood[`${BASE}/directory/resolve`].firm_id
const holdingsKey = Object.keys(cottonwood).find((k) => k.includes('/holdings/'))
const holdings = JSON.parse(JSON.stringify(cottonwood[holdingsKey]))
const nodes = holdings.data.nodes
const root = nodes.find((n) => n.node_kind === 'ACCOUNT')
const mk = (id, kind, parent, level, amount, label) => ({
  ...JSON.parse(JSON.stringify(root)), node_id: id, parent_node_id: parent, level, node_kind: kind,
  amount: { ...root.amount, value: amount }, percentages: { of_parent: amount / root.amount.value, of_total: amount / root.amount.value },
  display: { label },
})
const category = mk('N-CW-CAT', 'CATEGORY', root.node_id, 1, root.amount.value, 'Models')
const model = mk('N-CW-MODEL', 'MODEL', 'N-CW-CAT', 2, root.amount.value, MODEL)
for (const n of nodes) if (n.node_kind === 'SECURITY') { n.parent_node_id = 'N-CW-MODEL'; n.level = 3 }
holdings.data.nodes = [root, category, model, ...nodes.filter((n) => n.node_kind === 'SECURITY')]
console.log('INJECTED nodes:', holdings.data.nodes.map((n) => `${n.node_kind}:${n.node_id}<-${n.parent_node_id}`).join(' '))
const fixtures = {
  ...cottonwood,
  [holdingsKey]: holdings,
  [`${BASE}/directory/search`]: { contract_version: 'v1', operation: 'directory-search', firm_id: firmId,
    data: cottonwood[`${BASE}/directory/browse`].data.entries, unprojected_grant: { count: 0, denominator: 1, kinds: {} } },
}
const fixtureKeys = Object.keys(fixtures).sort((a, b) => b.length - a.length)
const matchFixture = (url) => fixtureKeys.find((key) => url.includes(key))

const browser = await chromium.launch({ executablePath: EDGE, headless: true })
const page = await browser.newPage({ viewport: { width: 1440, height: 900 } })
const netlog = []
page.on('requestfinished', async (req) => {
  const res = await req.response().catch(() => null)
  netlog.push([req.method(), res ? res.status() : 'NO-RESPONSE', req.url()].join('\t'))
})
page.on('pageerror', (e) => console.log('PAGE-CRASH:', String(e).slice(0, 300)))
await page.route('**/*', async (r) => {
  const req = r.request(); const url = req.url()
  if (req.method() === 'OPTIONS' && !url.startsWith(ORIGIN)) return r.fulfill({ status: 204, headers: CORS, body: '' })
  const fk = matchFixture(url)
  if (fk) return r.fulfill({ status: 200, headers: CORS, body: JSON.stringify(fixtures[fk]) })
  if (url.includes('/auth/refresh')) return r.fulfill({ status: 200, headers: CORS, body: JSON.stringify(SESSION) })
  return r.continue()
})
await page.goto(ORIGIN + '/investor-reporting', { waitUntil: 'networkidle', timeout: 30000 }).catch((e) => console.log('goto:', e.message.split('\n')[0]))
await page.waitForTimeout(1500)
let selectOk = false
try {
  const combo = page.getByRole('combobox', { name: 'Client search' })
  await combo.click(); await combo.fill('Cottonwood'); await page.waitForTimeout(800)
  const option = page.getByRole('option', { name: /Cottonwood Trust/ })
  await option.waitFor({ state: 'visible', timeout: 5000 }); await option.click(); selectOk = true
  console.log('SELECTED: Cottonwood Trust')
} catch (e) { console.log('SELECT-FAIL:', e.message.split('\n')[0]) }
await page.waitForTimeout(3000)
try { await page.getByRole('button', { name: 'Holdings', exact: true }).or(page.getByRole('tab', { name: 'Holdings' })).first().click(); console.log('CLICKED: Holdings tab') } catch (e) { console.log('HOLDINGS-CLICK:', e.message.split('\n')[0]) }
await page.waitForTimeout(2500)

const before = await page.evaluate(() => ({
  drillButtons: [...document.querySelectorAll('[data-slot="holdings-drill-tree"] button')].map((b) => b.textContent.trim().slice(0, 60)),
  chips: [...document.querySelectorAll('[data-slot="treemap-model-filter-option"]')].map((b) => ({ text: b.textContent.trim(), pressed: b.getAttribute('aria-pressed'), disabled: b.disabled })),
  sleeve: document.querySelector('[data-slot="security-filter-sleeve"]')?.value ?? null,
  refused: document.querySelectorAll('[data-slot="holdings-drill-refused"]').length,
  pageText: document.querySelector('[data-slot="holdings-drill-tree"]')?.innerText.replace(/\s+/g, ' ').slice(0, 300) ?? null,
}))
console.log('BEFORE:', JSON.stringify(before))

let picked = false
try {
  const tile = page.locator('[data-slot="holdings-drill-tree"] button').filter({ hasText: /Models|View breakdown|Core Growth/ }).first()
  await tile.waitFor({ state: 'visible', timeout: 5000 }); await tile.click(); await page.waitForTimeout(1200)
  console.log('OPENED: a card tile')
  const pick = page.locator('[data-slot="breakdown-row-scope"]').first()
  await pick.waitFor({ state: 'visible', timeout: 5000 })
  console.log('PICK CONTROL:', (await pick.textContent()).trim())
  await pick.click(); picked = true; await page.waitForTimeout(1200)
} catch (e) { console.log('PICK-FAIL:', e.message.split('\n')[0]) }

const after = await page.evaluate(() => ({
  scopeLine: document.querySelector('[data-slot="holdings-model-scope"]')?.textContent.trim() ?? null,
  scopeModel: document.querySelector('[data-slot="holdings-model-scope"]')?.getAttribute('data-model') ?? null,
  chips: [...document.querySelectorAll('[data-slot="treemap-model-filter-option"]')].map((b) => ({ text: b.textContent.trim(), pressed: b.getAttribute('aria-pressed'), disabled: b.disabled, locked: b.getAttribute('data-scope-locked') })),
  sleeve: document.querySelector('[data-slot="security-filter-sleeve"]')?.value ?? null,
  sleeveDisabled: document.querySelector('[data-slot="security-filter-sleeve"]')?.disabled ?? null,
  dialogOpen: document.querySelectorAll('[data-slot="breakdown-row-scope"]').length,
  tableRows: document.querySelectorAll('[data-slot="security-list"] tbody tr').length,
}))
console.log('AFTER:', JSON.stringify(after))
const ok = selectOk && picked && after.scopeModel === MODEL && after.chips.some((c) => c.pressed === 'true' && c.disabled) && after.sleeve === MODEL && after.sleeveDisabled === true
console.log(ok ? 'VERDICT: MODEL-SCOPE-REAL-OK' : 'VERDICT: MODEL-SCOPE-REAL-FAIL')
await page.screenshot({ path: OUT, fullPage: true })
console.log('SAVED:', OUT)
writeFileSync(OUT.replace(/\.png$/, '.netlog.tsv'), netlog.join('\n') + '\n')
await browser.close()
