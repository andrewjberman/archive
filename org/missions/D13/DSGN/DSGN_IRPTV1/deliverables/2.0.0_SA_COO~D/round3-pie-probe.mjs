import { chromium } from 'playwright-core'
import { readFileSync } from 'node:fs'
const ORIGIN = 'http://localhost:5174'
const fixtures = JSON.parse(readFileSync(process.argv[2], 'utf8'))
const keys = Object.keys(fixtures).sort((a, b) => b.length - a.length)
const CORS = { 'Access-Control-Allow-Origin': ORIGIN, 'Access-Control-Allow-Credentials': 'true', 'Access-Control-Allow-Headers': '*', 'Access-Control-Allow-Methods': '*', 'Content-Type': 'application/json' }
const SESSION = { accessToken: 'ui-smoke-token', user: { email: 'dev@opalcapital.com', name: 'Dev User', role: 'admin', userType: 'Dev', firmId: 'opal-capital', firmRole: null, advisorId: null, advisorRole: null, mustChangePassword: false } }
const b = await chromium.launch({ executablePath: 'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe', headless: true })
const p = await b.newPage({ viewport: { width: 1440, height: 900 } })
p.on('pageerror', (e) => console.log('PAGE-CRASH:', String(e).slice(0, 300)))
p.on('console', (m) => { if (m.type() === 'error' && !/401|portal-proxy/.test(m.text())) console.log('CONSOLE-ERROR:', m.text().slice(0, 300)) })
await p.route('**/*', async (r) => { const u = r.request().url(); if (r.request().method() === 'OPTIONS' && !u.startsWith(ORIGIN)) return r.fulfill({ status: 204, headers: CORS, body: '' }); const k = keys.find((x) => u.includes(x)); if (k) return r.fulfill({ status: 200, headers: CORS, body: JSON.stringify(fixtures[k]) }); if (u.includes('/auth/refresh')) return r.fulfill({ status: 200, headers: CORS, body: JSON.stringify(SESSION) }); return r.continue() })
await p.goto(ORIGIN + '/investor-reporting', { waitUntil: 'networkidle' })
await p.waitForTimeout(1500)
if (process.argv[3] === 'driver-order') { await p.getByRole('button', { name: 'Holdings', exact: true }).first().click(); await p.waitForTimeout(1500) }
const i = p.locator('[data-slot="search-select-input"]').first(); await i.click(); await i.fill('Cottonwood'); await p.waitForTimeout(1000)
await p.locator('[data-slot="search-select-option"]', { hasText: 'Cottonwood Trust' }).first().click(); await p.waitForTimeout(3000)
if (process.argv[3] === 'driver-order') { await p.getByRole('button', { name: 'Performance', exact: true }).first().click(); await p.waitForTimeout(3000) }
await p.getByRole('button', { name: 'Holdings', exact: true }).first().click(); await p.waitForTimeout(6000); await p.screenshot({ path: 'C:/tmp/pie6s.png', fullPage: true })
console.log(JSON.stringify(await p.evaluate(() => ({
  sectors: [...document.querySelectorAll('.recharts-pie-sector path, .recharts-pie-sector')].map((s) => (s.getAttribute('fill') || 'NOFILL') + ':' + (s.getAttribute('d') || '').length).slice(0, 8),
  surfaces: [...document.querySelectorAll('.recharts-surface')].map((s) => `${s.getAttribute('width')}x${s.getAttribute('height')}`),
  wrappers: [...document.querySelectorAll('.recharts-responsive-container')].map((w) => `${w.clientWidth}x${w.clientHeight}`),
  select: [...document.querySelectorAll('[data-slot="holdings-account-filter"] select')].map((e) => ({ value: e.value, options: [...e.options].map((o) => o.value + '=' + o.text + ':' + getComputedStyle(o).color), color: getComputedStyle(e).color, bg: getComputedStyle(e).backgroundColor })),
}))))
await b.close()
