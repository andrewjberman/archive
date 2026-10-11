/**
 * firm-choice-driver.mjs -- driver copied from the launch-and-auth-stub pattern of portal/scripts/ui-smoke.mjs
 * (system Edge, fresh headless profile, the /auth/refresh stub, fixture routing by longest URL substring, --dist
 * serving through scripts/ui-dist.mjs). It does ONE thing ui-smoke.mjs cannot: after the same steps ui-smoke runs
 * (click "New Ticket", pick "analysis_request" in the ticket-type select) it sets size=3 on the Firm <select>, so the
 * native option list is drawn in the screenshot (a closed native select shows only its selected option, and a headless
 * capture does not draw the popup). It prints the Firm control's option texts read from the DOM, and the same LOC and
 * CANVAS lines ui-smoke prints.
 *
 * Usage (run from the portal worktree):
 *   node <this file> <route-without-leading-slash> <out.png> --dist dist --fixtures <file.json>
 */
import { readFileSync } from 'node:fs'
import { resolve } from 'node:path'
import { pathToFileURL } from 'node:url'

const portal = process.cwd()
const { chromium } = await import(pathToFileURL(resolve(portal, 'node_modules/playwright-core/index.mjs')).href)
const { distFromArgs, serveFromDist } = await import(pathToFileURL(resolve(portal, 'scripts/ui-dist.mjs')).href)

const args = process.argv.slice(2)
const DIST = distFromArgs(args)
const route = '/' + args[0].replace(/^\/+/, '')
const out = args[1]
const fixtures = JSON.parse(readFileSync(args[args.indexOf('--fixtures') + 1], 'utf8'))
const ORIGIN = 'http://localhost:5175'
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
const fixtureKeys = Object.keys(fixtures).sort((a, b) => b.length - a.length)

const browser = await chromium.launch({ executablePath: EDGE, headless: true })
const page = await browser.newPage({ viewport: { width: 1440, height: 900 } })
page.on('pageerror', e => console.log('PAGE-CRASH:', String(e).slice(0, 300)))
await page.route('**/*', async r => {
  const req = r.request()
  const url = req.url()
  if (req.method() === 'OPTIONS' && !url.startsWith(ORIGIN)) return r.fulfill({ status: 204, headers: CORS, body: '' })
  const fk = fixtureKeys.find(k => url.includes(k))
  if (fk) return r.fulfill({ status: 200, headers: CORS, body: JSON.stringify(fixtures[fk]) })
  if (url.includes('/auth/refresh')) return r.fulfill({ status: 200, headers: CORS, body: JSON.stringify(SESSION) })
  if (await serveFromDist(r, DIST, ORIGIN)) return
  return r.continue()
})
await page.goto(ORIGIN + route, { waitUntil: 'networkidle', timeout: 30000 }).catch(e => console.log('goto:', e.message.split('\n')[0]))
await page.waitForTimeout(1500)
await page.getByRole('button', { name: 'New Ticket', exact: true }).first().click()
console.log('CLICKED: New Ticket')
await page.waitForTimeout(1500)
await page.selectOption('select', 'analysis_request')
console.log('PICKED : "analysis_request"')
await page.waitForTimeout(2500)
const firm = page.locator('select[aria-label="Firm"]')
const options = await firm.locator('option').allInnerTexts()
const disabled = await firm.isDisabled()
console.log('FIRM-OPTIONS:', JSON.stringify(options), 'disabled=' + disabled)
await firm.evaluate(el => { el.size = Math.min(el.options.length, 4) })
console.log('FIRM-SIZE: set size=' + Math.min(options.length, 4) + ' so the option list is drawn')
await page.waitForTimeout(500)
const state = await page.evaluate(() => ({ loc: window.location.pathname, canvas: getComputedStyle(document.body).backgroundColor }))
console.log('LOC   :', state.loc, state.loc === new URL(ORIGIN + route).pathname ? '' : ' <-- DID NOT LAND')
console.log('CANVAS:', state.canvas)
await page.screenshot({ path: out, fullPage: true })
console.log('SAVED :', out)
await browser.close()
