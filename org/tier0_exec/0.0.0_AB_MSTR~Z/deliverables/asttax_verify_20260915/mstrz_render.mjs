// 0.0.0_AB_MSTR~Z independent render of Positioning -> Satellites -> Holdings Breakdown.
// NOT scripts/ui-smoke.mjs: own fixtures (built from bytes this seat fetched by VersionId), own DOM
// extraction, own mutation arm. Usage:
//   node mstrz_render.mjs <port> "<satellite>" <outprefix> [--mutate]
import { createRequire } from 'node:module'
import { readFileSync, writeFileSync } from 'node:fs'
import { dirname, join } from 'node:path'
import { fileURLToPath } from 'node:url'

const require = createRequire('C:/tmp/mstrz-verify-portal/package.json')
const { chromium } = require('playwright-core')
const HERE = dirname(fileURLToPath(import.meta.url))
const [port, sat, prefix] = process.argv.slice(2)
const mutate = process.argv.includes('--mutate')
const ORIGIN = `http://localhost:${port}`

const fixtures = JSON.parse(readFileSync(join(HERE, 'fixtures_mstrz.json'), 'utf8'))
if (mutate) {
  const t = fixtures['/api/scoped/satellites/characteristics.json'].tickers
  console.log('MUTATE: GLD.fee', t.GLD.fee, '-> 0.55 ; GLD.returns.1Y', t.GLD.returns['1Y'], '-> 99.5 ; VGSH.yield', t.VGSH.yield, '-> 7.77')
  t.GLD.fee = 0.55
  t.GLD.returns['1Y'] = 99.5
  t.VGSH.yield = 7.77
}
const keys = Object.keys(fixtures).sort((a, b) => b.length - a.length)
const hits = Object.fromEntries(keys.map(k => [k, 0]))
const CORS = {
  'Access-Control-Allow-Origin': ORIGIN, 'Access-Control-Allow-Credentials': 'true',
  'Access-Control-Allow-Headers': '*', 'Access-Control-Allow-Methods': '*', 'Content-Type': 'application/json',
}
const SESSION = {
  accessToken: 'mstrz-inert-token',
  user: { email: 'verify@opalcapital.com', name: 'MSTR Z Verify', role: 'admin', userType: 'Dev',
          firmId: 'opal-capital', firmRole: null, advisorId: null, advisorRole: null, mustChangePassword: false },
}

const browser = await chromium.launch({ executablePath: 'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe', headless: true })
const page = await browser.newPage({ viewport: { width: 1600, height: 1000 } })
page.on('pageerror', e => console.log('PAGE-ERROR:', String(e).slice(0, 200)))
const unmatchedApi = new Set()
await page.route('**/*', r => {
  const req = r.request(); const url = req.url()
  if (req.method() === 'OPTIONS' && !url.startsWith(ORIGIN)) return r.fulfill({ status: 204, headers: CORS, body: '' })
  const k = keys.find(x => url.includes(x))
  if (k) { hits[k]++; return r.fulfill({ status: 200, headers: CORS, body: JSON.stringify(fixtures[k]) }) }
  if (url.includes('/auth/refresh')) return r.fulfill({ status: 200, headers: CORS, body: JSON.stringify(SESSION) })
  if (url.includes('/api/')) unmatchedApi.add(url.split('?')[0])
  return r.continue()
})

await page.goto(ORIGIN + '/positioning', { waitUntil: 'networkidle', timeout: 45000 }).catch(e => console.log('goto:', e.message.split('\n')[0]))
await page.waitForTimeout(3000)
console.log('LOC:', await page.evaluate(() => location.pathname))
await page.getByRole('button', { name: 'Satellites', exact: true }).first().click()
await page.waitForTimeout(2500)
const nSelect = await page.locator('select').count()
if (nSelect > 0) {
  const opts = await page.locator('select').first().evaluate(s => Array.from(s.options).map(o => o.value))
  console.log('SELECT options:', JSON.stringify(opts))
  await page.selectOption('select', sat)
  console.log('PICKED via select')
} else {
  const names = await page.locator('button,[role=button],[role=tab]').evaluateAll(els =>
    els.map(e => (e.getAttribute('aria-label') || e.textContent || '').trim()).filter(Boolean).slice(0, 80))
  console.log('NO <select>; controls on page:', JSON.stringify(names))
  const btn = page.getByRole('button', { name: sat, exact: true })
  if (await btn.count() > 0) { await btn.first().click(); console.log('PICKED via button', sat) }
  else {
    const short = sat.replace('Opal Satellite ', '')
    const alt = page.getByRole('button', { name: new RegExp(`(^|\\D)${short}(\\D|$)`) })
    console.log('button exact miss; regex candidates:', await alt.count())
    await alt.first().click(); console.log('PICKED via regex button', short)
  }
}
await page.waitForTimeout(2500)
await page.screenshot({ path: join(HERE, `${prefix}_after_pick.png`), fullPage: false })

const dump = { sat, mutate, views: {} }
for (const view of ['Characteristics', 'Performance']) {
  await page.getByRole('button', { name: view, exact: true }).first().click()
  await page.waitForTimeout(1500)
  dump.views[view] = await page.evaluate(() => {
    // the Holdings Breakdown table: the table under the panel whose header text says so
    const heads = Array.from(document.querySelectorAll('*')).filter(e => e.childElementCount === 0 && e.textContent.trim() === 'Holdings Breakdown')
    let panel = heads[0]
    while (panel && !panel.querySelector('table')) panel = panel.parentElement
    const table = panel ? panel.querySelector('table') : null
    if (!table) return { error: 'no Holdings Breakdown table' }
    const hdr = Array.from(table.querySelectorAll('thead tr')).map(tr => Array.from(tr.children).map(c => c.innerText.trim()))
    const rows = Array.from(table.querySelectorAll('tbody tr')).map(tr => Array.from(tr.children).map(c => c.innerText.replace(/\s+/g, ' ').trim()))
    const footers = Array.from(panel.querySelectorAll('*')).filter(e => e.childElementCount === 0 && /Source:/.test(e.textContent)).map(e => e.textContent.trim())
    return { hdr, rows, footers }
  })
  await page.screenshot({ path: join(HERE, `${prefix}_${view.toLowerCase()}.png`), fullPage: true })
}
dump.bodyUnrounded = await page.evaluate(() => (document.body.innerText.match(/-?\d+\.\d{3,}%?/g) || []))
dump.sources = await page.evaluate(() => Array.from(document.querySelectorAll('*')).filter(e => e.childElementCount === 0 && /Source:|as of/.test(e.textContent)).map(e => e.textContent.trim()).slice(0, 30))
dump.fixtureHits = hits
dump.unmatchedApi = [...unmatchedApi]
writeFileSync(join(HERE, `${prefix}_dom.json`), JSON.stringify(dump, null, 1))
console.log('FIXTURE HITS:', JSON.stringify(hits))
console.log('UNMATCHED /api/ (passed through, not fixtured):', JSON.stringify([...unmatchedApi]))
for (const v of Object.keys(dump.views)) console.log(v, 'rows', dump.views[v].rows ? dump.views[v].rows.length : dump.views[v].error)
console.log('UNROUNDED numbers in body text (3+ decimals):', JSON.stringify(dump.bodyUnrounded))
await browser.close()
