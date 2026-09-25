// Round-4 drain: where does the accepted client selection get lost? Logs selection requests and the identity WHO per step.
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
p.on('request', (r) => { if (/selections|resolve/.test(r.url()) && r.method() !== 'OPTIONS') console.log('REQ', r.method(), r.url().slice(-80)) })
await p.route('**/*', async (r) => { const u = r.request().url(); if (r.request().method() === 'OPTIONS' && !u.startsWith(ORIGIN)) return r.fulfill({ status: 204, headers: CORS, body: '' }); const k = keys.find((x) => u.includes(x)); if (k) return r.fulfill({ status: 200, headers: CORS, body: JSON.stringify(fixtures[k]) }); if (u.includes('/auth/refresh')) return r.fulfill({ status: 200, headers: CORS, body: JSON.stringify(SESSION) }); return r.continue() })
const who = async (tag) => console.log(tag, (await p.locator('[data-slot="identity-who"]').first().innerText().catch(() => 'none')).replace(/\s+/g, ' ').slice(0, 80))
await p.goto(ORIGIN + '/investor-reporting', { waitUntil: 'networkidle' }); await p.waitForTimeout(1500)
if (process.argv[3] === 'driver-order') { await p.getByRole('button', { name: 'Holdings', exact: true }).first().click(); await p.waitForTimeout(2000); console.log('PRE-VISIT Holdings (no client)') }
const i = p.locator('[data-slot="search-select-input"]').first(); await i.click(); await i.fill('Cottonwood'); await p.waitForTimeout(1000)
await p.locator('[data-slot="search-select-option"]', { hasText: 'Cottonwood Trust' }).first().click(); await p.waitForTimeout(3000)
await who('AFTER-SELECT')
for (const t of ['Performance', 'Holdings', 'Analysis', 'Performance']) {
  console.log('CLICK', t); await p.getByRole('button', { name: t, exact: true }).first().click(); await p.waitForTimeout(3000); await who('ON-' + t)
}
await b.close()
