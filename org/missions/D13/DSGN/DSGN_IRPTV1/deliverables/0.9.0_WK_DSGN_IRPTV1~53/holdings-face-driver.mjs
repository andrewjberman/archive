/**
 * TO-IV-e-96 SUPPLEMENTARY driver -- NOT the order's named instrument (scripts/ui-smoke.mjs). ui-smoke cannot type into the
 * header's role=combobox "Client search" (measured: `--fill "Client search=Sample"` times out, see smoke_fill_probe.txt in the
 * evidence folder), so it cannot pick a client, and therefore cannot reach the Holdings face with a client or an account
 * picked. This script replicates ui-smoke's own recipe (auth stub, CORS echo, --dist serving through scripts/ui-dist.mjs,
 * full-page screenshot, the body background as CANVAS) and adds what ui-smoke lacks: typing the search, choosing in the
 * Performance tab's Account select, and request-aware fixtures (a static --fixtures map answers every POST /selections with
 * one body, so a one-account read could not differ from the client read).
 *
 * Usage: node holdings-face-driver.mjs <mode> <out.png> <fixture.json> <dist dir>
 *   mode "client": the client is picked and the Holdings tab opened; no account is chosen anywhere.
 *   mode "picker": the client is picked, then the Performance tab's Account select is set to its SECOND account, then the
 *                  Holdings tab is opened.
 *   mode "back":   as "picker", then "Back to all accounts" is clicked on the Holdings tab.
 * Server model (synthetic): POST /selections with scope_kind CLIENT answers both accounts; scope_kind ACCOUNT answers the one
 * account named by scope_ids[0] (a node ref or an account id). Fixture bodies are synthetic (the files beside this one).
 * No dev server, no port, no network.
 */
import { readFileSync } from 'node:fs'
import { pathToFileURL } from 'node:url'
import { resolve } from 'node:path'

const PORTAL = 'C:/dev/wk-dsgn-irptv1-49/portal'
const { chromium } = await import(pathToFileURL(resolve(PORTAL, 'node_modules/playwright-core/index.mjs')).href)
const { serveFromDist } = await import(pathToFileURL(resolve(PORTAL, 'scripts/ui-dist.mjs')).href)

const [mode, out, fixturePath, dist] = process.argv.slice(2)
const PORT = '5199' // an origin string only; nothing listens (--dist routing answers every request)
const ORIGIN = `http://localhost:${PORT}`
const EDGE = 'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe'
const CORS = {
  'Access-Control-Allow-Origin': ORIGIN, 'Access-Control-Allow-Credentials': 'true', 'Access-Control-Allow-Headers': '*',
  'Access-Control-Allow-Methods': '*', 'Content-Type': 'application/json',
}
const SESSION = {
  accessToken: 'ui-smoke-token',
  user: { email: 'dev@opalcapital.com', name: 'Dev User', role: 'admin', userType: 'Dev', firmId: 'opal-capital', firmRole: null, advisorId: null, advisorRole: null, mustChangePassword: false },
}
const K = '/api/scoped/investor-reporting/'
const fixtures = JSON.parse(readFileSync(fixturePath, 'utf8'))
const HKEY = Object.keys(fixtures).find((key) => key.includes(K + 'holdings/'))
const ALL_ID = HKEY.split('/holdings/')[1]
const ALL_BODY = fixtures[HKEY]
const ACCOUNT_NODES = ALL_BODY.data.nodes.filter((n) => n.parent_node_id === null)
const oneId = (k) => ALL_ID.slice(0, -4) + 'a1a' + k // a well-formed set id per account
const oneBody = (k) => {
  const nodes = ALL_BODY.data.nodes
  const body = JSON.parse(JSON.stringify(ALL_BODY))
  const keep = new Set([ACCOUNT_NODES[k].node_id])
  for (let grew = true; grew;) { grew = false; for (const n of nodes) if (!keep.has(n.node_id) && keep.has(n.parent_node_id)) { keep.add(n.node_id); grew = true } }
  body.data.nodes = nodes.filter((n) => keep.has(n.node_id))
  body.data.scope.account_ids = [ACCOUNT_NODES[k].drill_refs[0].ref_id]
  const total = body.data.nodes[0].amount.value
  body.data.custody_totals.total_market_value.value = total
  body.data.custody_totals.unique_account_count = 1
  for (const n of body.data.nodes) { n.amount.denominator.value = total; n.percentages.of_total = n.amount.value / total }
  return body
}
const ONE_BODIES = ACCOUNT_NODES.map((_, k) => oneBody(k))
const accountIndexOf = (id) => Math.max(0, ACCOUNT_NODES.findIndex((n) => n.node_id === id || n.drill_refs[0].ref_id === id))
let selectionPosts = 0
const selectionKey = Object.keys(fixtures).find((key) => key.endsWith('/selections'))
const log = []

process.on('uncaughtException', (e) => { for (const line of log) console.log('LOG   :', line); console.log('FAILED:', String(e).split(String.fromCharCode(10))[0]); process.exit(1) })
const browser = await chromium.launch({ executablePath: EDGE, headless: true })
const page = await browser.newPage({ viewport: { width: 1440, height: 900 } })
page.on('console', (m) => { if (m.type() === 'error') log.push('CONSOLE-ERROR: ' + m.text().slice(0, 240)) })
page.on('pageerror', (e) => log.push('PAGE-CRASH: ' + String(e).slice(0, 200)))
await page.route('**/*', async (r) => {
  const req = r.request()
  const url = req.url()
  if (req.method() === 'OPTIONS' && !url.startsWith(ORIGIN)) return r.fulfill({ status: 204, headers: CORS, body: '' })
  if (req.method() === 'POST' && url.endsWith('/selections')) {
    selectionPosts += 1
    let sent = {}
    try { sent = JSON.parse(req.postData() || '{}') } catch { sent = {} }
    const kind = sent.scope_kind
    const k = kind === 'ACCOUNT' ? accountIndexOf((sent.scope_ids || [])[0]) : -1
    const body = JSON.parse(JSON.stringify(fixtures[selectionKey]))
    body.data.account_set_id = k < 0 ? ALL_ID : oneId(k)
    body.data.account_ids = body.data.selected_account_ids = k < 0 ? ALL_BODY.data.scope.account_ids : ONE_BODIES[k].data.scope.account_ids
    log.push(`POST /selections #${selectionPosts} scope_kind=${kind} -> ${k < 0 ? 'both accounts' : 'account #' + (k + 1)}`)
    return r.fulfill({ status: 200, headers: CORS, body: JSON.stringify(body) })
  }
  if (url.includes(K + 'holdings/')) {
    const k = ACCOUNT_NODES.findIndex((_, idx) => url.includes(oneId(idx)))
    log.push(`GET holdings -> ${k < 0 ? 'both accounts' : 'account #' + (k + 1)}`)
    return r.fulfill({ status: 200, headers: CORS, body: JSON.stringify(k < 0 ? ALL_BODY : ONE_BODIES[k]) })
  }
  const fk = Object.keys(fixtures).sort((a, b) => b.length - a.length).find((key) => url.includes(key))
  if (fk) return r.fulfill({ status: 200, headers: CORS, body: JSON.stringify(fixtures[fk]) })
  if (url.includes('/auth/refresh')) return r.fulfill({ status: 200, headers: CORS, body: JSON.stringify(SESSION) })
  if (await serveFromDist(r, resolve(dist), ORIGIN)) return
  return r.continue()
})
await page.goto(ORIGIN + '/investor-reporting', { waitUntil: 'networkidle', timeout: 30000 }).catch((e) => log.push('goto: ' + e.message.split('\n')[0]))
await page.waitForTimeout(2000)
const box = page.getByRole('combobox', { name: 'Client search', exact: true })
await box.click()
await box.pressSequentially('Sample', { delay: 60 })
await page.waitForTimeout(1500)
await page.getByText('Sample Household').first().click({ timeout: 10000 })
log.push('PICKED the first search row')
await page.waitForTimeout(2500)
if (mode === 'picker' || mode === 'back') {
  await page.locator('select[aria-label="Account"]').selectOption({ index: 1 })
  log.push('CHOSE the second account in the Performance tab Account select')
  await page.waitForTimeout(2000)
}
if (process.env.DRIVER_DEBUG) await page.screenshot({ path: process.env.DRIVER_DEBUG, fullPage: true })
await page.getByRole('button', { name: 'Holdings', exact: true }).or(page.getByRole('tab', { name: 'Holdings', exact: true })).first().click()
await page.waitForTimeout(4000)
if (mode === 'back') {
  await page.locator('[data-slot="holdings-all-accounts"]').first().click()
  log.push('CLICKED Back to all accounts')
  await page.waitForTimeout(1500)
}
const state = await page.evaluate(() => ({
  loc: location.pathname,
  canvas: getComputedStyle(document.body).backgroundColor,
  tiles: [...document.querySelectorAll('[data-slot="holdings-drill-tree"] button[aria-haspopup="dialog"]')].map((b) => b.getAttribute('aria-label')),
  backLink: !!document.querySelector('[data-slot="holdings-all-accounts"]'),
  opening: !!document.querySelector('[data-slot="holdings-account-opening"]'),
}))
await page.screenshot({ path: out, fullPage: true })
await browser.close()
console.log('MODE  :', mode)
console.log('LOC   :', state.loc)
console.log('CANVAS:', state.canvas)
console.log('TILES :', JSON.stringify(state.tiles))
console.log('BACK-LINK:', state.backLink, ' OPENING-LINE:', state.opening)
for (const line of log) console.log('LOG   :', line)
console.log('SAVED :', out)
