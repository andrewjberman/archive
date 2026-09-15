/**
 * POSN_ASTTAX.TO-W3-1 (slot ~26) -- SUPPLEMENTARY DOM READ beside the W3-AC5 / W3-AC6
 * ui-smoke captures. It does NOT replace them: both named invocations were run as written
 * and their output recorded. This exists because two things the criteria ask for cannot
 * come out of `scripts/ui-smoke.mjs` as it stands:
 *
 *  1. THE TEXT DUMP IS 160 CHARACTERS. ui-smoke.mjs :334 slices body.innerText to
 *     `.slice(0, 160)`, which on this page is the left nav and nothing else -- so a regex
 *     count over it is 0 out of a denominator of 0 LABELS. That number cannot tell a page
 *     with no raw floats apart from a page full of them, and a control that cannot fail is
 *     not evidence. Here the labels are enumerated and the denominator is printed.
 *  2. THE ASSET CLASS ROWS AND THE SECTION COUNT ARE BEHIND "Expand Details", which
 *     neither criterion's invocation clicks, and W3-AC6 asks for the DOM's COLOUR TOKENS,
 *     which ui-smoke never prints.
 *
 * Mechanism copied from ui-smoke.mjs (system Edge, stubbed /auth/refresh session, the same
 * longest-substring fixture router) so the page under this read is the page under the
 * capture -- a second instrument on the same state, not a second state.
 *
 * Usage (from portal/): node <this> --port <p> --fixtures <f.json>
 */
import { createRequire } from 'node:module'
import { readFileSync } from 'node:fs'
// THIS FILE LIVES OUTSIDE THE PORTAL PACKAGE (it is a deliverable, and the task order's
// <paths> grant does not put scripts in the submodule), and node resolves node_modules
// from the IMPORTING FILE, never from cwd -- a bare `import 'playwright-core'` here fails
// with ERR_MODULE_NOT_FOUND even though the package is installed where the script runs.
// Resolve it from the CWD (portal/) instead, which is where the junctioned install is.
const require = createRequire(process.cwd() + '/package.json')
const { chromium } = require('playwright-core')

const args = process.argv.slice(2)
const port = args.includes('--port') ? args[args.indexOf('--port') + 1] : '5175'
const fixturesPath = args[args.indexOf('--fixtures') + 1]
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
const page = await browser.newPage({ viewport: { width: 1440, height: 900 } })
page.on('pageerror', (e) => console.log('PAGE-CRASH:', String(e).slice(0, 300)))
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

// THE RAW-FLOAT REGEX IS THE PRE-AMENDMENT CRITERION'S: [0-9]+\.[0-9]{2,}% -- two or more
// decimals. KEPT AND PRINTED because the pre-edit control dump is graded against it.
const RAW_FLOAT = /[0-9]+\.[0-9]{2,}%/
// THE AMENDED W3-AC5 LABEL CLAUSE (order @1b791c6a11, PRD v0.11 @ab2ee8052a): every
// single-bar percent label matches this, i.e. at most two decimals, trailing zeros dropped.
const LABEL_SHAPE = /^[0-9]+(\.[0-9]{1,2})?%$/

// ---- THE EXPECTED LABEL SEQUENCE, COMPUTED FROM THE SERVED BYTES ---------------------
// Independently of the render: the same five classes, the same presence rule, the same
// two-decimal trim, applied to the fixture. Joining this to the DOM's labels is what makes
// "the label is right" a comparison rather than an inspection -- and it carries the RAW sum
// beside each label, which is what W3-AC6 asks to see.
const CLS = [
  ['fixedIncome', 'Fixed Income', ['fixed_income', 'cash']],
  ['equity', 'Equity', ['equity']],
  ['structured', 'Structured', ['structured']],
  ['commodities', 'Commodities', ['commodities']],
  ['alternatives', 'Alternatives', ['alternatives']],
]
const cv = (a) => Object.fromEntries(CLS.map(([k, , s]) => [k, s.reduce((t, f) => t + (a?.[f] ?? 0), 0)]))
const presentOver = (cols) => CLS.filter(([k]) => cols.some((c) => Number.isFinite(c[k]) && c[k] !== 0))
// drawn = the columns whose values are DRAWN as labels; presenceCols = the columns the
// presence rule reads (portfolio always, benchmark when the benchmark numbers are drawn).
const expectedLabels = (drawn, presenceCols) => {
  const present = presentOver(presenceCols)
  const out = []
  for (const col of drawn) {
    for (const [k, label] of present) {
      const v = col.values[k]
      if (v > 0) out.push({ book: col.book, cls: label, raw: String(v), rendered: String(Number(v.toFixed(2))) + '%' })
    }
  }
  return out
}
const models = fixtures['/api/general/positioning/positioning_data.json']
const etfs = fixtures['/api/general/etfs/positioning_data.json']
const sats = fixtures['/api/scoped/satellites/holdings.json']
const registry = fixtures['/api/scoped/satellites/registry.json']
const mPort = Object.entries(models.portfolios).map(([book, p]) => ({ book, values: cv(p.allocation) }))
const mBench = Object.entries(models.portfolios).map(([book, p]) => ({ book, values: cv(p.benchmark?.allocation) }))
const ePort = Object.entries(etfs.portfolios).map(([book, p]) => ({ book, values: cv(p.allocation) }))
const sPort = registry.books
  .filter((b) => b.code !== 'Opal Satellite 98' && sats.satellites[b.code]?.holdings?.length)
  .map((b) => {
    const alloc = {}
    for (const r of sats.satellites[b.code].holdings) {
      if (r.asset_class) alloc[r.asset_class] = (alloc[r.asset_class] ?? 0) + (Number(r.weight) || 0)
    }
    return { book: b.code, values: cv(alloc) }
  })
const vals = (cols) => cols.map((c) => c.values)
const EXPECTED = {
  'MODELS / Portfolio view (Expand Details open)': expectedLabels(mPort, vals(mPort)),
  // THE BENCHMARK VIEW DRAWS BENCHMARK VALUES, but the presence set unions the portfolio
  // columns too (the order's act 1) -- so the two arguments differ here and only here.
  'MODELS / Benchmark view': expectedLabels(mBench, vals([...mPort, ...mBench])),
  'ETFS / Portfolio view': expectedLabels(ePort, vals(ePort)),
  'SATELLITES / Portfolio view': expectedLabels(sPort, vals(sPort)),
}

const readState = () => page.evaluate(() => {
  // THE POSITIONING SUMMARY PANEL, found by CONTENT rather than by header text: the header
  // renders 'POSITIONING SUMMARY' through a CSS `uppercase`, so the DOM string is
  // 'Positioning Summary' and an exact-text match silently finds nothing. The panel is the
  // SMALLEST div carrying both the legend heading and its own footer.
  // innerText IS THE RENDERED TEXT, so a CSS `uppercase` reaches it: the legend heading
  // reads 'ASSET CLASSES' here while its textContent is 'Asset Classes'. Matched
  // case-insensitively rather than picking one of the two and being silently wrong.
  const candidates = Array.from(document.querySelectorAll('div'))
    .filter((d) => d.innerText &&
      d.innerText.toUpperCase().includes('ASSET CLASSES') &&
      d.innerText.toUpperCase().includes('SOURCE:'))
  const panel = candidates.sort((a, b) => a.innerText.length - b.innerText.length)[0]
  if (!panel) return { error: 'PANEL NOT FOUND' }
  const txt = (e) => (e ? e.innerText.replace(/\u00a0/g, ' ') : '')
  // LEGEND: every 32x32 swatch inside the panel, with its COMPUTED background colour (the
  // DOM's colour token, not the source literal) and the label beside it.
  const legend = Array.from(panel.querySelectorAll('div.w-8.h-8')).map((sw) => {
    const row = sw.parentElement
    const label = row ? row.innerText.split('\n')[0] : ''
    return { label, color: getComputedStyle(sw).backgroundColor }
  })
  // BAR + MATRIX LABELS: every span in the panel whose text ends in '%' or is a signed
  // number (the relative labels), with its computed colour.
  const labels = Array.from(panel.querySelectorAll('span'))
    .map((s) => ({ text: s.textContent.trim(), color: getComputedStyle(s).color }))
    .filter((s) => /^[+-]?[0-9][0-9.]*%$/.test(s.text) || /^[+-][0-9][0-9.]*$/.test(s.text))
  // SECTION HEADERS with their counts, as rendered: "ASSET CLASS" + "(3)".
  const sections = Array.from(panel.querySelectorAll('span.uppercase'))
    .map((s) => s.textContent.trim())
  const sectionCounts = Array.from(panel.querySelectorAll('span'))
    .filter((s) => /^\([0-9]+\)$/.test(s.textContent.trim()))
    .map((s) => ({
      section: s.parentElement ? s.parentElement.innerText.replace(/\s+/g, ' ').trim() : '',
    }))
  // MATRIX ROW LABELS: the first grid column of the detail matrix (pl-16 indent).
  const rowLabels = Array.from(panel.querySelectorAll('div.pl-16')).map((d) => d.innerText.trim())
  // FOOTERS: every PanelFooter strip ON THE PAGE, in document order, with the panel it
  // belongs to named by that panel's header. Read at DOCUMENT level rather than inside the
  // summary panel: a panel-scoped query returned the panel's body instead of its footer,
  // and a footer read that can silently return the wrong node is not a footer read.
  const footers = Array.from(document.querySelectorAll('div.rounded-b-lg'))
    .map((d) => d.innerText.replace(/\s+/g, ' ').trim())
    .filter((t) => t.length > 0 && t.length < 200)
  const footer = txt(panel.querySelector('div.rounded-b-lg'))
  // PAGE-LEVEL COPY, outside the panel: the subtitle and every canvas notice.
  const subtitle = (() => {
    const h = Array.from(document.querySelectorAll('h1'))
      .find((e) => e.textContent.trim().toUpperCase() === 'POSITIONING')
    return h && h.parentElement ? h.parentElement.innerText.replace(/\s+/g, ' ').trim() : ''
  })()
  const notices = Array.from(document.querySelectorAll('div[class*="amber-500/10"], div[class*="red-500/10"], div[class*="blue-500/10"]'))
    .map((d) => d.innerText.replace(/\s+/g, ' ').trim())
  const mode = Array.from(document.querySelectorAll('button'))
    .filter((b) => ['MODELS', 'ETFS', 'SATELLITES'].includes(b.textContent.trim().toUpperCase()))
    .map((b) => b.textContent.trim() + (b.className.includes('shadow') || b.getAttribute('aria-pressed') === 'true' ? '*' : ''))
  return { legend, labels, sections, sectionCounts, rowLabels, footer, footers, subtitle, notices, mode,
           panelText: panel.innerText.replace(/\u00a0/g, ' ') }
})

const report = (title, s) => {
  console.log('\n================ ' + title + ' ================')
  console.log('SUBTITLE : ' + s.subtitle.replace(/\n/g, ' | '))
  console.log('LEGEND   : ' + s.legend.length + ' entries')
  for (const e of s.legend) console.log('   ' + JSON.stringify(e.label) + '  ' + e.color)
  console.log('SECTIONS : ' + JSON.stringify(s.sections))
  console.log('COUNTS   : ' + JSON.stringify(s.sectionCounts.map((c) => c.section)))
  console.log('ROWS(' + s.rowLabels.length + ') : ' + JSON.stringify(s.rowLabels))
  console.log('FOOTERS ON THE PAGE (' + s.footers.length + ', in document order -- the first is the ' +
              'Positioning Summary panel\'s):')
  s.footers.forEach((f, i) => console.log('   [' + i + '] ' + JSON.stringify(f)))
  console.log('NOTICES  : ' + JSON.stringify(s.notices))
  const raw = s.labels.filter((l) => RAW_FLOAT.test(l.text))
  console.log('LABELS(' + s.labels.length + ' denominator): ' +
              JSON.stringify(s.labels.map((l) => l.text)))
  console.log('RAW-FLOAT LABELS matching /[0-9]+\\.[0-9]{2,}%/ : ' + raw.length +
              ' of ' + s.labels.length + (raw.length ? ' -- ' + JSON.stringify(raw) : ''))
  // THE AMENDED LABEL CLAUSE, with both counts printed so they can be compared.
  const shaped = s.labels.filter((l) => LABEL_SHAPE.test(l.text))
  console.log('LABEL SHAPE ^[0-9]+(\\.[0-9]{1,2})?%$ : ' + shaped.length + ' match of ' +
              s.labels.length + ' labels' +
              (shaped.length === s.labels.length ? '  EQUAL' : '  NOT EQUAL -- ' +
               JSON.stringify(s.labels.filter((l) => !LABEL_SHAPE.test(l.text)).map((l) => l.text))))
  // THE JOIN: each rendered label beside the RAW served sum it came from, computed from the
  // fixture by a second implementation of the same rule.
  const exp = EXPECTED[title] || []
  console.log('LABEL JOIN (rendered vs the served sum, ' + exp.length + ' expected of ' +
              s.labels.length + ' rendered):')
  const n = Math.max(exp.length, s.labels.length)
  let mismatch = 0
  for (let i = 0; i < n; i++) {
    const e = exp[i]
    const got = s.labels[i] ? s.labels[i].text : '(none)'
    const want = e ? e.rendered : '(none)'
    if (got !== want) mismatch += 1
    console.log('   ' + (got === want ? 'OK  ' : 'DIFF') + '  ' +
                (e ? (e.book + ' / ' + e.cls).padEnd(34) : '(unexpected label)'.padEnd(34)) +
                ' raw=' + (e ? e.raw : '-').padEnd(22) + ' expected=' + want.padEnd(10) + ' rendered=' + got)
  }
  console.log('LABEL JOIN RESULT: ' + (n - mismatch) + ' of ' + n + ' agree')
  const panelRaw = (s.panelText.match(/[0-9]+\.[0-9]{2,}%/g) || [])
  console.log('RAW-FLOAT anywhere in the panel text (' + s.panelText.length + ' chars): ' +
              panelRaw.length + (panelRaw.length ? ' -- ' + JSON.stringify(panelRaw) : ''))
  console.log('LABEL COLOURS: ' + JSON.stringify([...new Set(s.labels.map((l) => l.text + '=' + l.color))]))
}

const click = async (name) => {
  await page.getByRole('button', { name, exact: true }).first().click()
  await page.waitForTimeout(2500)
}

await page.goto(ORIGIN + '/positioning', { waitUntil: 'networkidle', timeout: 30000 })
  .catch((e) => console.log('goto:', e.message.split('\n')[0]))
await page.waitForTimeout(3000)
await click('Expand Details')
report('MODELS / Portfolio view (Expand Details open)', await readState())

await click('Benchmark')
report('MODELS / Benchmark view', await readState())

await click('Portfolio')
await click('ETFs')
report('ETFS / Portfolio view', await readState())

await click('Satellites')
report('SATELLITES / Portfolio view', await readState())

await browser.close()
