/**
 * POSN_ASTTAX.TO-W2-1 (slot ~25) -- SUPPLEMENTARY DOM READ beside the W2-AC5 / W2-AC6 /
 * W2-AC8 ui-smoke captures. It does NOT replace them: every named invocation is run as
 * written and its output recorded. This exists because what the criteria ask for cannot
 * come out of `scripts/ui-smoke.mjs` as it stands:
 *
 *  1. THE TEXT DUMP IS 160 CHARACTERS (ui-smoke.mjs :334 slices body.innerText), which on
 *     this page is the left nav and nothing else. A per-CELL comparison needs the cells.
 *  2. THE PERFORMANCE VIEW is behind a second toggle inside the Holdings panel, and the
 *     legend's COLOUR TOKENS and the two panel headers' timestamps are never printed.
 *
 * Mechanism copied from ui-smoke.mjs (system Edge, stubbed /auth/refresh session, the same
 * longest-substring fixture router) so the page under this read is the page under the
 * capture -- a second instrument on the same state, not a second state. Modelled on slot
 * ~26's w3_dom_read.mjs, itself modelled on slot ~19's v8_ac10_dom_read.
 *
 * Usage (from portal/):
 *   node <this> --port <p> --fixtures <f.json> --out <file.txt> [--mode satellites|models|etfs]
 *               [--book "Opal Satellite 15"] [--label "<title>"]
 *
 * The output file is JSON (indent 2) -- text a reader can read and a comparator can parse
 * without a second format to keep in step.
 */
import { createRequire } from 'node:module'
import { readFileSync, writeFileSync } from 'node:fs'
// THIS FILE LIVES OUTSIDE THE PORTAL PACKAGE (a deliverable; the task order's <paths>
// grant does not put scripts in the submodule), and node resolves node_modules from the
// IMPORTING FILE, never from cwd. Resolve playwright-core from the CWD (portal/) instead.
const require = createRequire(process.cwd() + '/package.json')
const { chromium } = require('playwright-core')

const args = process.argv.slice(2)
const argOf = (name, dflt) => (args.includes(name) ? args[args.indexOf(name) + 1] : dflt)
const port = argOf('--port', '5175')
const fixturesPath = argOf('--fixtures', null)
const outPath = argOf('--out', null)
const mode = argOf('--mode', 'satellites')
const book = argOf('--book', null)
const label = argOf('--label', mode + (book ? ' / ' + book : ''))
const fixtures = JSON.parse(readFileSync(fixturesPath, 'utf8'))
const ORIGIN = `http://localhost:${port}`
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
const fixtureKeys = Object.keys(fixtures).sort((a, b) => b.length - a.length)

const browser = await chromium.launch({ executablePath: EDGE, headless: true })
const page = await browser.newPage({ viewport: { width: 1600, height: 1000 } })
const crashes = []
page.on('pageerror', (e) => { crashes.push(String(e).slice(0, 300)); console.log('PAGE-CRASH:', String(e).slice(0, 300)) })
await page.route('**/*', (r) => {
  const url = r.request().url()
  if (r.request().method() === 'OPTIONS' && !url.startsWith(ORIGIN)) {
    return r.fulfill({ status: 204, headers: CORS, body: '' })
  }
  const k = fixtureKeys.find((key) => url.includes(key))
  if (k) return r.fulfill({ status: 200, headers: CORS, body: JSON.stringify(fixtures[k]) })
  if (url.includes('/auth/refresh')) {
    return r.fulfill({ status: 200, headers: CORS, body: JSON.stringify(SESSION) })
  }
  return r.continue()
})

const clickButton = async (name) => {
  try {
    await page.getByRole('button', { name, exact: true }).first().click()
    console.log('CLICKED:', JSON.stringify(name))
  } catch (e) {
    console.log('CLICK-FAIL:', JSON.stringify(name), '--', e.message.split('\n')[0])
    const names = await page.locator('button,[role=button],[role=tab]').evaluateAll((els) =>
      els.map((e) => (e.textContent || '').trim()).filter(Boolean).slice(0, 60))
    console.log('  (control names on page:', JSON.stringify(names), ')')
    // FALLBACK, stated rather than silent: click the nearest clickable ancestor of the text.
    try {
      const t = page.locator(`text=${JSON.stringify(name)}`).first()
      await t.waitFor({ state: 'visible', timeout: 8000 })
      const handle = await t.elementHandle()
      const clickable = await handle.evaluateHandle((el) => {
        let n = el
        for (let i = 0; i < 8 && n; i++) {
          const cs = window.getComputedStyle(n)
          if (n.onclick || cs.cursor === 'pointer' || n.getAttribute('role') === 'button') return n
          n = n.parentElement
        }
        return el
      })
      await clickable.asElement().click()
      console.log('CLICKED-TEXT (fallback):', JSON.stringify(name))
    } catch (e2) {
      console.log('CLICKTEXT-FAIL:', JSON.stringify(name), '--', e2.message.split('\n')[0])
    }
  }
  await page.waitForTimeout(2500)
}

// THE READ. Everything is taken from the RENDERED DOM (innerText, computed styles), never
// from the app's state -- the bar is the served bytes against the rendered cells.
const readState = () => page.evaluate(() => {
  const clean = (s) => (s || '').replace(/\u00a0/g, ' ').replace(/\s+/g, ' ').trim()
  // PANELS: every Panel on the page, by its own header strip, with the header's full text
  // (title + the DataTimestamp) and its footer strip.
  const headers = Array.from(document.querySelectorAll('div.rounded-t-lg'))
    .map((d) => clean(d.innerText)).filter((t) => t.length > 0 && t.length < 400)
  const footers = Array.from(document.querySelectorAll('div.rounded-b-lg'))
    .map((d) => clean(d.innerText)).filter((t) => t.length > 0 && t.length < 300)
  // THE PORTFOLIO COMPOSITION LEGEND: the 12x12 swatches under the treemap, each with the
  // COMPUTED background colour (the DOM's token, not the source literal) and its label.
  const legend = Array.from(document.querySelectorAll('div.w-3.h-3')).map((sw) => {
    const row = sw.parentElement
    return { label: clean(row ? row.innerText : ''), color: getComputedStyle(sw).backgroundColor }
  })
  // THE SELECTED BOOK: the portfolio selector button that is painted as active (its inline
  // backgroundColor is the book colour rather than 'transparent').
  const bookButtons = Array.from(document.querySelectorAll('button'))
    .filter((b) => /^Opal Satellite|^(UST|ST|INT|LT|ULT|AGG|CSM)$/i.test(clean(b.textContent)))
    .map((b) => ({ text: clean(b.textContent), active: b.style.backgroundColor !== 'transparent' && b.style.backgroundColor !== '' }))
  // THE HOLDINGS BREAKDOWN TABLE: every tbody row, cell by cell, as rendered.
  const tables = Array.from(document.querySelectorAll('table')).map((t) => {
    const headRows = Array.from(t.querySelectorAll('thead tr')).map((tr) =>
      Array.from(tr.querySelectorAll('th')).map((th) => clean(th.innerText)))
    const rows = Array.from(t.querySelectorAll('tbody tr')).map((tr) =>
      Array.from(tr.querySelectorAll('td')).map((td) => clean(td.innerText)))
    return { headRows, rows }
  })
  const notices = Array.from(document.querySelectorAll('div[class*="amber-500/10"], div[class*="red-500/10"], div[class*="blue-500/10"]'))
    .map((d) => clean(d.innerText)).filter((t) => t.length > 0 && t.length < 400)
  return { headers, footers, legend, bookButtons, tables, notices,
           bodyChars: document.body.innerText.length }
})

await page.goto(ORIGIN + '/positioning', { waitUntil: 'networkidle', timeout: 30000 })
  .catch((e) => console.log('goto:', e.message.split('\n')[0]))
await page.waitForTimeout(3500)
if (mode === 'satellites') await clickButton('Satellites')
if (mode === 'etfs') await clickButton('ETFs')
if (book) await clickButton(book)

const characteristics = await readState()
// The Holdings panel's own view toggle -- the 8 performance windows live behind it.
await clickButton('Performance')
const performance = await readState()
await clickButton('Characteristics')

const out = { label, mode, book, port, fixtures: fixturesPath, crashes, characteristics, performance }
writeFileSync(outPath, JSON.stringify(out, null, 2))
console.log('\n================ ' + label + ' ================')
console.log('PANEL HEADERS (' + characteristics.headers.length + '):')
characteristics.headers.forEach((h, i) => console.log('   [' + i + '] ' + JSON.stringify(h)))
console.log('PANEL FOOTERS (' + characteristics.footers.length + '):')
characteristics.footers.forEach((f, i) => console.log('   [' + i + '] ' + JSON.stringify(f)))
console.log('PORTFOLIO COMPOSITION LEGEND (' + characteristics.legend.length + ' entries):')
characteristics.legend.forEach((e) => console.log('   ' + JSON.stringify(e.label) + '  ' + e.color))
console.log('BOOK BUTTONS: ' + JSON.stringify(characteristics.bookButtons))
console.log('NOTICES: ' + JSON.stringify(characteristics.notices))
for (const [view, st] of [['characteristics', characteristics], ['performance', performance]]) {
  const t = st.tables[st.tables.length - 1]
  console.log('TABLE (' + view + '): ' + st.tables.length + ' table(s) on the page; last has ' +
              (t ? t.rows.length : 0) + ' tbody rows')
  if (t) {
    t.headRows.forEach((hr, i) => console.log('   HEAD[' + i + '] ' + JSON.stringify(hr)))
    t.rows.forEach((r, i) => console.log('   ROW[' + i + '] ' + JSON.stringify(r)))
  }
}
console.log('WROTE ' + outPath)
await browser.close()
