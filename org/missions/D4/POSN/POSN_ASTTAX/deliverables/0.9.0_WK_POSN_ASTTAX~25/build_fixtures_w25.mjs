// POSN_ASTTAX.TO-W2-1 / W2-AC5 + W2-AC6 (slot ~25) -- build the ui-smoke fixtures file
// from the SERVED bytes, and print what those bytes IMPLY for the Holdings Breakdown
// BEFORE any render is read. MODELLED ON slot ~19's build_fixtures_v8.js by way of slot
// ~26's build_fixtures_w3.mjs (same manifest-driven shape, same md5 refusal, same
// shadow-pair check); ESM because this file lives OUTSIDE the portal package, and node
// resolves module type from the nearest package.json to the FILE.
//
// WHY THE EXPECTATION IS COMPUTED HERE: W2-AC5 asks whether every rendered cell EQUALS
// the served value. Computed from the bytes before the screenshot exists, the expectation
// cannot be back-fitted to what the picture happened to show.
//
// Usage (from portal/): node <this> <manifest.json> <out-fixtures.json>
import { readFileSync, writeFileSync, statSync } from 'node:fs'
import { gunzipSync } from 'node:zlib'
import { createHash } from 'node:crypto'

const manifest = JSON.parse(readFileSync(process.argv[2], 'utf8'))
const out = process.argv[3]
const fixtures = {}
for (const m of manifest) {
  const raw = readFileSync(m.local)
  const md5 = createHash('md5').update(raw).digest('hex')
  if (md5 !== m.md5) {
    console.log('BLOCKED: ' + m.key + ' md5 ' + md5 + ' differs from the manifest ' + m.md5)
    process.exit(1)
  }
  fixtures[m.urlkey] = JSON.parse((m.gzip ? gunzipSync(raw) : raw).toString('utf8'))
  console.log('FIXTURE KEY ' + m.urlkey)
  console.log('   s3://' + m.bucket + '/' + m.key + '  VersionId=' + m.VersionId +
              '  LastModified=' + m.LastModified + '  bytes=' + raw.length +
              '  md5(raw)=' + md5 + '  gzip=' + m.gzip)
}
writeFileSync(out, JSON.stringify(fixtures))
console.log('WROTE ' + out + '  keys=' + Object.keys(fixtures).length +
            '  bytes=' + statSync(out).size)

// SHADOW CHECK (slot ~19's, kept): ui-smoke resolves by LONGEST matching substring, so a
// key that is a substring of another only ever serves URLs the longer one misses.
const keys = Object.keys(fixtures)
const shadow = []
for (const a of keys) for (const b of keys) if (a !== b && b.includes(a)) shadow.push(a + ' < ' + b)
console.log('SHADOW PAIRS among fixture keys: ' +
            (shadow.length ? shadow.join(' | ') : 'NONE (0 of ' + keys.length + ')'))

// ---- THE TICKERS BLOCK, READ FROM THE SERVED BYTES -----------------------------------
const reg = fixtures['/api/scoped/satellites/registry.json']
const hold = fixtures['/api/scoped/satellites/holdings.json']
const chars = fixtures['/api/scoped/satellites/characteristics.json']
const HIDDEN = new Set(['Opal Satellite 98'])  // Positioning.tsx:156 hides it from display
const tickers = chars.tickers || {}
console.log('\nCHARACTERISTICS as_of=' + chars.as_of + '  tickers=' + Object.keys(tickers).length +
            '  satellites=' + Object.keys(chars.satellites || {}).length)
const bySource = {}
const byStyle = {}
for (const [t, v] of Object.entries(tickers)) {
  bySource[v.source] = (bySource[v.source] ?? 0) + 1
  byStyle[String(v.management_style)] = (byStyle[String(v.management_style)] ?? 0) + 1
}
console.log('  sources: ' + JSON.stringify(bySource) + '   management_style: ' + JSON.stringify(byStyle))
console.log('  entries carrying a non-null name: ' +
            Object.values(tickers).filter((v) => v.name != null).length + ' of ' + Object.keys(tickers).length)
console.log('HOLDINGS as_of=' + hold.as_of + '  satellites=' + Object.keys(hold.satellites).length)

// COVERAGE: every ticker any DISPLAYED satellite holds, against the served tickers block.
// A ticker the block does not carry renders every measure blank and is COUNTED (the
// adapter's `coverage`), never guessed -- so the denominator is printed here first.
const heldTickers = new Set()
let rows = 0
for (const b of reg.books) {
  if (HIDDEN.has(b.code)) continue
  const served = hold.satellites[b.code]
  if (!served || !served.holdings) continue
  rows += served.holdings.length
  for (const r of served.holdings) heldTickers.add(r.ticker)
}
const missing = [...heldTickers].filter((t) => !(t in tickers))
console.log('  DISPLAYED satellites hold ' + heldTickers.size + ' distinct tickers across ' + rows +
            ' served rows; carried by the tickers block: ' + (heldTickers.size - missing.length) +
            ' of ' + heldTickers.size + '; NOT carried: ' + JSON.stringify(missing))

// The two satellites W2-AC5 names, row by row, straight off the served bytes.
for (const code of ['Opal Satellite 15', 'Opal Satellite 80']) {
  const served = hold.satellites[code]
  if (!served) { console.log('\n' + code + ': ABSENT from holdings.json'); continue }
  console.log('\n' + code + ': ' + served.holdings.length + ' served rows')
  for (const r of [...served.holdings].sort((a, b) => b.weight - a.weight)) {
    const t = tickers[r.ticker]
    console.log('   ' + r.ticker.padEnd(6) + ' w=' + String(r.weight).padEnd(8) +
                ' class=' + String(r.asset_class).padEnd(13) +
                (t ? ' name=' + JSON.stringify(t.name) + ' style=' + t.management_style +
                     ' fee=' + t.fee + ' aum=' + t.aum + ' active=' + t.active +
                     ' yield=' + t.yield + ' dur=' + t.duration + ' credit=' + t.credit +
                     ' beta=' + t.beta + ' returns=' + (t.returns ? Object.keys(t.returns).length : 'null') +
                     ' src=' + t.source
                   : ' NOT IN TICKERS BLOCK'))
  }
}
