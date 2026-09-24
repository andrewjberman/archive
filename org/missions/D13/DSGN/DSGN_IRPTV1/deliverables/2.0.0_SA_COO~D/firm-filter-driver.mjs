/**
 * FIRM FILTER real run (Andrew-direct 2026-09-24 ~18:4xZ; CTO 100850): on the Global view an Opal user sees every
 * firm's directory rows; choosing a firm in the Firm dropdown NARROWS the list to that firm, with no FIRM_BINDING
 * refusal. Auth stub, CORS and page setup are the pinned IVE2 driver's recipe (0.9.0_WK_DSGN_IRPTV1~5/
 * iv-e-2-selection-driver.mjs). The IR routes are served from the server-captured wire the client's own contract test
 * reads (src/pages/InvestorReporting/tests/opal-scope/server-wire.json): resolve `selected_tenant=global` answers the
 * Global context; resolve for a registry tenant answers that firm's own scope (the same reshaping context.test.ts
 * does); anything else (an opaque firm id) answers FIRM_BINDING, as the server did in Andrew's HAR; browse answers
 * the page for its `selected_tenant`.
 *
 * Usage (cwd = the portal checkout): node --input-type=module - <port> <out.png> < firm-filter-driver.mjs
 */
import { chromium } from 'playwright-core'
import { readFileSync } from 'node:fs'

const PORT = process.argv[2] || '5174'
const OUT = process.argv[3] || 'firm-filter.png'
const ORIGIN = `http://localhost:${PORT}`
const EDGE = 'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe'
const CORS = {
  'Access-Control-Allow-Origin': ORIGIN,
  'Access-Control-Allow-Credentials': 'true',
  'Access-Control-Allow-Headers': '*',
  'Access-Control-Allow-Methods': '*',
  'Content-Type': 'application/json',
}
const SESSION = {
  accessToken: 'ui-smoke-token',
  user: { email: 'dev@opalcapital.com', name: 'Dev User', role: 'admin',
          userType: 'Dev', firmId: 'opal-capital', firmRole: null, advisorId: null,
          advisorRole: null, mustChangePassword: false },
}
const wire = JSON.parse(readFileSync('src/pages/InvestorReporting/tests/opal-scope/server-wire.json', 'utf8'))
const firmScopes = Object.fromEntries(wire.context.data.firms.map((f) => [f.tenant, f.scope]))

const resolveTenants = []
const browseTenants = []
function resolveAnswer(tenant) {
  if (tenant === 'global') return { status: 200, body: wire.context }
  const scope = firmScopes[tenant]
  if (scope) return { status: 200, body: { ...wire.context, firm_id: scope.verified_request_firm_id, data: scope } }
  return { status: 200, body: { contract_version: wire.context.contract_version, operation: 'resolve-scope', ok: false,
    status: 'UNAVAILABLE', reason: 'FIRM_BINDING' } }
}

const browser = await chromium.launch({ executablePath: EDGE, headless: true })
const page = await browser.newPage({ viewport: { width: 1440, height: 900 } })
page.on('pageerror', (e) => console.log('PAGE-CRASH:', String(e).slice(0, 300)))
await page.route('**/*', async (r) => {
  const req = r.request()
  const url = req.url()
  if (req.method() === 'OPTIONS' && !url.startsWith(ORIGIN)) return r.fulfill({ status: 204, headers: CORS, body: '' })
  if (url.includes('/auth/refresh')) return r.fulfill({ status: 200, headers: CORS, body: JSON.stringify(SESSION) })
  if (url.includes('/investor-reporting/directory/resolve') && req.method() === 'POST') {
    let tenant = null
    try { tenant = JSON.parse(req.postData() || '{}').selected_tenant ?? null } catch { tenant = 'unparsed' }
    resolveTenants.push(tenant)
    const a = resolveAnswer(tenant)
    return r.fulfill({ status: a.status, headers: CORS, body: JSON.stringify(a.body) })
  }
  if (url.includes('/investor-reporting/directory/browse')) {
    const tenant = new URL(url).searchParams.get('selected_tenant')
    browseTenants.push(tenant)
    const pageBody = wire.pages[tenant]
    if (pageBody) return r.fulfill({ status: 200, headers: CORS, body: JSON.stringify(pageBody) })
    return r.fulfill({ status: 404, headers: CORS, body: '{}' })
  }
  return r.continue()
})

async function countOptions(label) {
  const combo = page.getByRole('combobox', { name: 'Client search' })
  if (!(await combo.isEnabled().catch(() => false))) {
    console.log(`${label}: 0 directory row(s): client search DISABLED`)
    return 0
  }
  await combo.click()
  await page.waitForTimeout(800)
  const names = await page.getByRole('option').allInnerTexts()
  console.log(`${label}: ${names.length} directory row(s): ${JSON.stringify(names.map((n) => n.replace(/\s+/g, ' ').trim()))}`)
  await page.keyboard.press('Escape')
  return names.length
}

await page.goto(ORIGIN + '/investor-reporting', { waitUntil: 'networkidle', timeout: 30000 }).catch((e) => console.log('goto:', e.message.split('\n')[0]))
await page.waitForTimeout(2500)
const firmSelect = page.getByLabel('Select Firm')
const firmOptions = await firmSelect.locator('option').allInnerTexts().catch(() => [])
console.log('FIRM OPTIONS:', JSON.stringify(firmOptions))
const before = await countOptions('GLOBAL')
const pick = firmOptions.find((o) => o !== 'Global (All)')
await firmSelect.selectOption({ label: pick })
console.log('SELECTED FIRM:', pick)
await page.waitForTimeout(3000)
const after = await countOptions('AFTER FIRM')
const refusal = await page.getByText(/out of scope/i).count()
console.log('OUT-OF-SCOPE TEXT ON PAGE:', refusal)
console.log('RESOLVE-SELECTED-TENANTS:', JSON.stringify(resolveTenants))
console.log('BROWSE-SELECTED-TENANTS:', JSON.stringify(browseTenants))
console.log(`FIRM-FILTER: global ${before} -> ${pick} ${after}; ${after > 0 && after < before && refusal === 0 ? 'NARROWS' : 'DOES-NOT-NARROW'}`)
await page.screenshot({ path: OUT, fullPage: true })
console.log('SAVED:', OUT)
await browser.close()
