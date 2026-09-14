/**
 * POSN_ASTTAX.TO-V6-1 / V6-AC6 -- the expansion of <RENDERED_DOM_UI_SMOKE>.
 *
 * Reads the RENDERED DOM's per-class swatch colours and prints a (class, expected,
 * observed) table. "Expected" is lifted from portal/src/lib/chartColors.ts -- the F1
 * registry -- and "observed" is window.getComputedStyle() on the element the browser
 * actually painted, so the two sides of the comparison come from different planes. A
 * screenshot cannot be diffed against a hex; this can.
 *
 * THROUGH THE UI-SMOKE BROWSER: the launch (system Edge, headless, playwright-core), the
 * CORS headers, the stubbed /auth/refresh SESSION and the fixture router are taken from
 * portal/scripts/ui-smoke.mjs -- same browser, same identity, same transport. Only the
 * OBSERVATION differs: ui-smoke saves a PNG, this reads computed styles.
 *
 * Usage (from the portal directory):
 *   node ../org/.../rendered_dom_swatches.mjs --port <PORT> [--fixtures <f.json>] [--mode etfs]
 */
'use strict';
const { readFileSync } = require('node:fs')
const { createRequire } = require('node:module')
const path = require('path')

// playwright-core is resolved FROM THE PORTAL PACKAGE, not from this file's directory.
// This instrument lives in the deliverables tree, so a bare import would resolve against
// org/.../deliverables/node_modules -- which does not exist. It is also UNDECLARED in
// portal/package.json (row W22-S9): present in the estate's install, absent from a fresh
// worktree, which is why the resolution is explicit and fails with a named reason.
const PORTAL_PKG = path.resolve(__dirname, '../../../../../../../portal/package.json')
let chromium
try {
  chromium = createRequire(PORTAL_PKG)('playwright-core').chromium
} catch (e) {
  console.log('BLOCKED: cannot resolve playwright-core from ' + PORTAL_PKG);
  console.log('  ' + String(e.message).split(/\r?\n/)[0]);
  process.exit(2)
}

// Anchored on the FIRST FLAG, not on a fixed offset: `node script.js --port N` and
// `node -e "...require(...)"` with the flags pushed onto argv have DIFFERENT argv shapes
// (the -e form carries no script path), and slice(2) silently dropped '--port' on the
// second -- so the run went to the default 5175, got ERR_CONNECTION_REFUSED, and printed
// a full table of NOT FOUND that read exactly like a render failure.
const flagAt = process.argv.findIndex((a) => a.startsWith('--'))
const args = flagAt >= 0 ? process.argv.slice(flagAt) : []
const port = args.includes('--port') ? args[args.indexOf('--port') + 1] : '5175'
const fixturesPath = args.includes('--fixtures') ? args[args.indexOf('--fixtures') + 1] : null
const mode = args.includes('--mode') ? args[args.indexOf('--mode') + 1] : 'models'
const fixtures = fixturesPath ? JSON.parse(readFileSync(fixturesPath, 'utf8')) : {}
const ORIGIN = `http://localhost:${port}`
const EDGE = 'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe'
const REGISTRY = '../portal/src/lib/chartColors.ts'

// --- EXPECTED: lifted from the registry, never retyped -------------------------------
const regPath = ['src/lib/chartColors.ts', REGISTRY, 'portal/src/lib/chartColors.ts']
  .find((p) => { try { readFileSync(p); return true } catch { return false } })
if (!regPath) throw new Error('ABSENT: chartColors.ts not found from ' + process.cwd())
const regSrc = readFileSync(regPath, 'utf8')
function sliceBalanced(t, from, open, close) {
  const i = t.indexOf(open, from)
  let d = 0
  for (let j = i; j < t.length; j++) {
    if (t[j] === open) d++
    else if (t[j] === close) { d--; if (d === 0) return t.slice(i, j + 1) }
  }
  throw new Error('UNPARSEABLE: unbalanced ' + open)
}
function assigned(t, decl, open, close) {
  const i = t.indexOf(decl)
  if (i < 0) throw new Error('ABSENT in the registry: ' + decl)
  const j = t.indexOf('= ' + open, i)
  return sliceBalanced(t, j, open, close)
}
const { ASSET_CLASS } = new Function(
  'const PALETTE = ' + assigned(regSrc, 'export const PALETTE', '{', '}') + ';\n' +
  'const ASSET_CLASS = ' + assigned(regSrc, 'export const ASSET_CLASS ', '{', '}') + ';\n' +
  'return { ASSET_CLASS };'
)()

// The five ratified classes as the page LABELS them, mapped to their registry token.
// Class 1 is "Fixed Income / Cash" and the page labels it "Fixed Income".
const CLASSES = [
  ['Fixed Income', 'fixedIncome'],
  ['Equity', 'equity'],
  ['Structured', 'structured'],
  ['Commodities', 'commodities'],
  ['Alternatives', 'alternatives'],
]
const hex = (h) => h.toLowerCase()
const rgbToHex = (rgb) => {
  const m = /rgba?\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)/.exec(rgb || '')
  if (!m) return null
  return '#' + [1, 2, 3].map((i) => Number(m[i]).toString(16).padStart(2, '0')).join('')
}

// --- the ui-smoke browser, verbatim in mechanism -------------------------------------
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
async function main() {
const browser = await chromium.launch({ executablePath: EDGE, headless: true })
const page = await browser.newPage({ viewport: { width: 1440, height: 900 } })
page.on('pageerror', (e) => console.log('PAGE-CRASH:', String(e).slice(0, 200)))
await page.route('**/*', (r) => {
  const url = r.request().url()
  if (r.request().method() === 'OPTIONS' && !url.startsWith(ORIGIN)) {
    return r.fulfill({ status: 204, headers: CORS, body: '' })
  }
  const fk = fixtureKeys.find((k) => url.includes(k))
  if (fk) return r.fulfill({ status: 200, headers: CORS, body: JSON.stringify(fixtures[fk]) })
  if (url.includes('/auth/refresh')) {
    return r.fulfill({ status: 200, headers: CORS, body: JSON.stringify(SESSION) })
  }
  return r.continue()
})
await page.goto(ORIGIN + '/positioning', { waitUntil: 'networkidle', timeout: 30000 })
  .catch((e) => console.log('goto:', e.message.split('\n')[0]))
await page.waitForTimeout(3000)
console.log('LOC   : ' + page.url().replace(ORIGIN, ''))
if (/\/login/.test(page.url())) {
  console.log('BOUNCED TO /login -- the auth stub did not hold. REFUSED, not retried.')
  await browser.close()
  process.exit(1)
}
if (mode === 'etfs') {
  try {
    await page.getByRole('button', { name: 'ETFs', exact: true }).first().click()
    console.log('CLICKED: ETFs')
    await page.waitForTimeout(3000)
  } catch (e) { console.log('MODE-CLICK-FAIL:', e.message.split('\n')[0]) }
}
try {
  await page.getByRole('button', { name: 'Expand Details', exact: true }).first().click()
  await page.waitForTimeout(2000)
  console.log('CLICKED: Expand Details')
} catch (e) { console.log('EXPAND-FAIL (rows may be collapsed):', e.message.split('\n')[0]) }

// --- OBSERVED: computed styles off the painted DOM -----------------------------------
// Two INDEPENDENT readings per class, because they are two different surfaces and a
// single one could agree with the registry while the other does not:
//   (a) the legend SWATCH  -- the 8x8 rounded div beside the class name;
//   (b) the summary ROW    -- the value cell's background on that class's row.
const observed = await page.evaluate(() => {
  const out = {}
  const norm = (s) => (s || '').trim()
  // (a) legend swatches: find the label, take the swatch div in the same flex row.
  for (const el of document.querySelectorAll('div')) {
    const t = norm(el.textContent)
    const cls = el.className || ''
    if (typeof cls === 'string' && cls.includes('text-sm font-semibold text-white') && t) {
      const row = el.closest('div.flex.items-center')
      if (!row) continue
      const sw = row.querySelector('div.rounded')
      if (sw) out['legend:' + t] = getComputedStyle(sw).backgroundColor
    }
  }
  // (b) summary rows: the label cell carries "<Class> (%)"; its sibling value cells
  //     carry the row background.
  const labels = [...document.querySelectorAll('span')].filter((s) => /\(%\)$/.test(norm(s.textContent)))
  for (const s of labels) {
    const cell = s.closest('div')
    const grid = cell && cell.parentElement
    if (!grid) continue
    const idx = [...grid.children].indexOf(cell)
    const valueCell = grid.children[idx + 1]
    if (valueCell) {
      out['row:' + norm(s.textContent)] = getComputedStyle(valueCell).backgroundColor
      const span = valueCell.querySelector('span')
      if (span) out['rowtext:' + norm(s.textContent)] = getComputedStyle(span).color
    }
  }
  return out
})

console.log('')
console.log('V6-AC6 -- THE COLOUR ON SCREEN EQUALS THE REGISTRY, PER CLASS   (mode=' + mode + ')')
console.log('  expected: ' + regPath + ' (ASSET_CLASS, lifted and evaluated)')
console.log('  observed: window.getComputedStyle() on the painted element')
console.log('')
console.log('  ' + 'class'.padEnd(15) + 'surface'.padEnd(10) + 'expected'.padEnd(12) +
            'observed'.padEnd(24) + 'observed(hex)'.padEnd(15) + 'match')
let mismatches = 0, missing = 0, n = 0
for (const [label, token] of CLASSES) {
  const expect = hex(ASSET_CLASS[token])
  for (const [surface, key] of [['legend', 'legend:' + label], ['row', 'row:' + label + ' (%)']]) {
    const raw = observed[key]
    n++
    if (raw === undefined) {
      missing++
      console.log('  ' + label.padEnd(15) + surface.padEnd(10) + expect.padEnd(12) +
                  'NOT FOUND IN DOM'.padEnd(24) + ''.padEnd(15) + 'MISSING')
      continue
    }
    const got = rgbToHex(raw)
    const ok = got === expect
    if (!ok) mismatches++
    console.log('  ' + label.padEnd(15) + surface.padEnd(10) + expect.padEnd(12) +
                String(raw).padEnd(24) + String(got).padEnd(15) + (ok ? 'MATCH' : 'MISMATCH'))
  }
}
console.log('')
console.log('  DISTINCT observed colours across the five classes: ' +
            new Set(CLASSES.map(([l]) => rgbToHex(observed['legend:' + l])).filter(Boolean)).size +
            ' (five distinct expected)')
const textRows = Object.entries(observed).filter(([k]) => k.startsWith('rowtext:'))
if (textRows.length) {
  console.log('  class-row TEXT colour actually painted (V6-AC9 applied, read off the DOM):')
  for (const [k, v] of textRows) console.log('    ' + k.replace('rowtext:', '').padEnd(20) + v)
}
console.log('')
console.log('DENOMINATOR: ' + n + ' readings (' + CLASSES.length + ' classes x 2 surfaces); ' +
            missing + ' not found; ' + mismatches + ' mismatched.')
console.log('VERDICT-BY-OUTPUT: ' + (mismatches === 0 && missing === 0 ? 'PASS' : 'FAIL') +
            ' -- ' + (n - missing - mismatches) + ' of ' + n + ' equal to the registry.')
await browser.close()
process.exitCode = mismatches === 0 && missing === 0 ? 0 : 1
}

main().catch((e) => { console.log('INSTRUMENT-ERROR: ' + e.message); process.exitCode = 2 })
