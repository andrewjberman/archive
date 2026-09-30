/**
 * DSGN_IRPTV1 FAST item 46 (Andrew-direct 2026-09-30 ~21:0xZ, "2yes"): FCASH folds into the one Cash row of the
 * Securities table. Fixture plane on the local dev build (same recipe as items 36-45; nothing reaches the live
 * backend): the Cottonwood holdings fixture gets a CASH line and an FCASH line in the Cash class beside its two
 * securities; the driver counts the table's rows and reads the Cash row.
 * Usage: node .runtmp/fcash-fold-driver.mjs <port> <out.png>
 */
import { chromium } from 'playwright-core'
import { readFileSync, writeFileSync, mkdirSync } from 'node:fs'
import { dirname } from 'node:path'
const PORT = process.argv[2] || '5174'
const OUT = process.argv[3] || '.runtmp/fcash.fast-run.png'
mkdirSync(dirname(OUT), { recursive: true })
const ORIGIN = `http://localhost:${PORT}`
const EDGE = 'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe'
const CORS = { 'Access-Control-Allow-Origin': ORIGIN, 'Access-Control-Allow-Credentials': 'true', 'Access-Control-Allow-Headers': '*', 'Access-Control-Allow-Methods': '*', 'Content-Type': 'application/json' }
const SESSION = { accessToken: 'ui-smoke-token', user: { email: 'dev@opalcapital.com', name: 'Dev User', role: 'admin', userType: 'Dev', firmId: 'opal-capital', firmRole: null, advisorId: null, advisorRole: null, mustChangePassword: false } }
const BASE = '/api/scoped/investor-reporting'
const cw = JSON.parse(readFileSync('src/pages/InvestorReporting/fixtures/smoke/dsgn-irptv1-cottonwood.json', 'utf8'))
const firmId = cw[`${BASE}/directory/resolve`].firm_id
const hk = Object.keys(cw).find((k) => k.includes('/holdings/'))
const h = JSON.parse(JSON.stringify(cw[hk]))
const sec = h.data.nodes.find((n) => n.node_kind === 'SECURITY')
const mk = (id, sym, value) => ({ ...JSON.parse(JSON.stringify(sec)), node_id: id, security_id: { namespace: 'TICKER', value: sym },
  asset_class: 'cash', display: { label: `${sym} -- ${sym === 'FCASH' ? 'Fidelity Cash Reserves' : 'Cash'}`, symbol: sym },
  amount: { ...sec.amount, value }, percentages: { of_parent: value / 200000, of_total: value / 200000 } })
h.data.nodes.push(mk('N-CW-CASH', 'CASH', 5000), mk('N-CW-FCASH', 'FCASH', 7000))
const fixtures = { ...cw, [hk]: h, [`${BASE}/directory/search`]: { contract_version: 'v1', operation: 'directory-search', firm_id: firmId, data: cw[`${BASE}/directory/browse`].data.entries, unprojected_grant: { count: 0, denominator: 1, kinds: {} } } }
const keys = Object.keys(fixtures).sort((a, b) => b.length - a.length)
const match = (u) => keys.find((k) => u.includes(k))
const browser = await chromium.launch({ executablePath: EDGE, headless: true })
const page = await browser.newPage({ viewport: { width: 1440, height: 900 } })
page.on('pageerror', (e) => console.log('PAGE-CRASH:', String(e).slice(0, 200)))
await page.route('**/*', async (r) => { const q = r.request(); const u = q.url()
  if (q.method() === 'OPTIONS' && !u.startsWith(ORIGIN)) return r.fulfill({ status: 204, headers: CORS, body: '' })
  const k = match(u); if (k) return r.fulfill({ status: 200, headers: CORS, body: JSON.stringify(fixtures[k]) })
  if (u.includes('/auth/refresh')) return r.fulfill({ status: 200, headers: CORS, body: JSON.stringify(SESSION) })
  return r.continue() })
await page.goto(ORIGIN + '/investor-reporting', { waitUntil: 'networkidle', timeout: 30000 }).catch((e) => console.log('goto:', e.message.split('\n')[0]))
await page.waitForTimeout(1500)
let ok = false
try { const c = page.getByRole('combobox', { name: 'Client search' }); await c.click(); await c.fill('Cottonwood'); await page.waitForTimeout(800)
  const o = page.getByRole('option', { name: /Cottonwood Trust/ }); await o.waitFor({ state: 'visible', timeout: 5000 }); await o.click(); ok = true } catch (e) { console.log('SELECT-FAIL:', e.message.split('\n')[0]) }
await page.waitForTimeout(3000)
try { await page.getByRole('button', { name: 'Holdings', exact: true }).or(page.getByRole('tab', { name: 'Holdings' })).first().click() } catch (e) { console.log('TAB:', e.message.split('\n')[0]) }
await page.waitForTimeout(2500)
const rows = await page.evaluate(() => [...document.querySelectorAll('[data-slot="security-list"] tbody tr')].map((tr) => tr.innerText.replace(/\s+/g, ' ').trim()))
console.log('TABLE ROWS:', JSON.stringify(rows))
const cashRows = rows.filter((r) => /\bCash\b|\bCASH\b|FCASH/.test(r))
console.log('CASH-LIKE ROWS:', cashRows.length, JSON.stringify(cashRows))
const verdict = ok && rows.length > 0 && cashRows.length === 1 && /\$12,000\.00/.test(cashRows[0] || '') ? 'VERDICT: FCASH-FOLD-REAL-OK' : 'VERDICT: FCASH-FOLD-REAL-FAIL'
console.log(verdict)
await page.locator('[data-slot="security-list"]').scrollIntoViewIfNeeded().catch(() => {})
await page.screenshot({ path: OUT, fullPage: true })
console.log('SAVED:', OUT)
await browser.close()
