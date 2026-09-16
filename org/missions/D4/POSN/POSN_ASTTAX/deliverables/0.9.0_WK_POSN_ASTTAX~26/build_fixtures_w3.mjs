// POSN_ASTTAX.TO-W3-1 / W3-AC5 + W3-AC6 (slot ~26) -- build the ui-smoke fixtures file
// from the SERVED bytes, and print the presence sets those bytes IMPLY before any render
// is read. MODELLED ON slot ~19's build_fixtures_v8.js (same manifest-driven shape, same
// md5 refusal, same shadow-pair check); ESM because this file lives OUTSIDE the portal
// package, and node resolves module type from the nearest package.json to the FILE.
//
// WHY THE EXPECTED SETS ARE COMPUTED HERE: W3-AC5/W3-AC6 ask for the rendered legend to be
// EXPLAINED from the fixture's allocations. Computed from the bytes BEFORE the screenshot
// is read, the expectation cannot be back-fitted to what the picture happened to show.
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

// ---- THE PRESENCE RULE, COMPUTED OVER THE SERVED BYTES -------------------------------
// The panel's five ratified classes and the served fields each one sums
// (PositioningSummary.tsx ASSET_CLASSES): class 1 is Fixed Income / Cash, ONE class over
// the two served names, which is why it sums rather than picks. `hedge` is read as zero
// and is NOT one of the five.
const ASSET_CLASSES = [
  ['fixedIncome', 'Fixed Income', ['fixed_income', 'cash']],
  ['equity', 'Equity', ['equity']],
  ['structured', 'Structured', ['structured']],
  ['commodities', 'Commodities', ['commodities']],
  ['alternatives', 'Alternatives', ['alternatives']],
]
const classValuesOf = (alloc) => Object.fromEntries(
  ASSET_CLASSES.map(([k, , served]) => [k, served.reduce((s, f) => s + (alloc?.[f] ?? 0), 0)]))
// The presence rule itself: the ASSET_CLASSES keys, IN ORDER, with a non-zero finite value
// in ANY column. Same rule as the panel's exported helper, written independently here --
// a second instrument, not a second call of the first.
const presentOver = (columns) => ASSET_CLASSES
  .filter(([k]) => columns.some((c) => Number.isFinite(c[k]) && c[k] !== 0))
  .map(([, label]) => label)

const fmt = (cv) => ASSET_CLASSES.map(([k]) => k + '=' + (Math.round(cv[k] * 100) / 100)).join(' ')

const models = fixtures['/api/general/positioning/positioning_data.json']
console.log('\nMODELS positioning_data.json: data_as_of=' + models.data_as_of +
            '  books=' + JSON.stringify(Object.keys(models.portfolios)))
const mPortfolio = [], mBenchmark = []
for (const [code, p] of Object.entries(models.portfolios)) {
  const cv = classValuesOf(p.allocation)
  mPortfolio.push(cv)
  console.log('   ' + code + '  portfolio  ' + fmt(cv))
  if (p.benchmark?.allocation) {
    const bv = classValuesOf(p.benchmark.allocation)
    mBenchmark.push(bv)
    console.log('   ' + code + '  benchmark  ' + fmt(bv))
  }
}
// THE DRAWN-COLUMNS RULE (TO-W3-1 act 1 as RE-CUT ~05:2xZ on row W26-S6): each view's
// presence set is computed over EXACTLY the columns that view draws -- portfolio values in
// the Portfolio view, BENCHMARK VALUES ONLY in the Benchmark view, the DELTAS in the
// Relative view. Computed here from the served bytes before any render is read.
const mRelative = mPortfolio.map((cv, i) => Object.fromEntries(
  ASSET_CLASSES.map(([k]) => [k, cv[k] - (mBenchmark[i] ? mBenchmark[i][k] : 0)])))
console.log('  EXPECTED MODELS presence (PORTFOLIO view, ' + mPortfolio.length +
            ' drawn columns = the books\' portfolio values): ' + JSON.stringify(presentOver(mPortfolio)))
console.log('  EXPECTED MODELS presence (BENCHMARK view, ' + mBenchmark.length +
            ' drawn columns = the benchmark values ONLY): ' + JSON.stringify(presentOver(mBenchmark)))
for (const [i, code] of Object.keys(models.portfolios).entries()) {
  console.log('     benchmark column ' + code + '  ' + fmt(mBenchmark[i]))
}
console.log('  EXPECTED MODELS presence (RELATIVE view, ' + mRelative.length +
            ' drawn columns = the deltas): ' + JSON.stringify(presentOver(mRelative)))
for (const [i, code] of Object.keys(models.portfolios).entries()) {
  console.log('     delta column ' + code + '  ' + fmt(mRelative[i]))
}
console.log('  PORTFOLIO-ONLY CLASSES (non-zero in a portfolio column, ZERO in every ' +
            'benchmark column -- ABSENT from the Benchmark view under the re-cut rule, ' +
            'PRESENT under the superseded union rule): ' + JSON.stringify(
              presentOver(mPortfolio).filter((c) => !presentOver(mBenchmark).includes(c))))
console.log('  SUPERSEDED union rule would have listed (portfolio + benchmark, ' +
            (mPortfolio.length + mBenchmark.length) + ' columns): ' +
            JSON.stringify(presentOver([...mPortfolio, ...mBenchmark])))
console.log('  BENCHMARK-ONLY CLASSES (present in a benchmark column, absent from every ' +
            'portfolio column): ' + JSON.stringify(
              presentOver(mBenchmark).filter((c) => !presentOver(mPortfolio).includes(c))))

const etfs = fixtures['/api/general/etfs/positioning_data.json']
const eCols = []
console.log('\nETFS platinum/etfs/positioning_data.json: books=' +
            JSON.stringify(Object.keys(etfs.portfolios)))
for (const [code, p] of Object.entries(etfs.portfolios)) {
  const cv = classValuesOf(p.allocation)
  eCols.push(cv)
  console.log('   ' + code + '  portfolio  ' + fmt(cv) +
              '  served keys=' + JSON.stringify(Object.keys(p.allocation || {})))
}
console.log('  EXPECTED ETFS presence (' + eCols.length + ' columns): ' + JSON.stringify(presentOver(eCols)))

// SATELLITES: the adapter's arithmetic, re-derived here from the same served rows --
// allocation = sum of served weights per SERVED TOKEN (satelliteAdapter.ts :290-306),
// over the DISPLAYED registry codes only (Positioning.tsx :156 hides Satellite 98).
const reg = fixtures['/api/scoped/satellites/registry.json']
const hold = fixtures['/api/scoped/satellites/holdings.json']
const HIDDEN = new Set(['Opal Satellite 98'])
console.log('\nSATELLITES registry.json: as_of=' + reg.as_of + '  books=' + reg.books.length +
            '  hidden-from-display=' + JSON.stringify([...HIDDEN]))
console.log('SATELLITES holdings.json: as_of=' + hold.as_of + '  source=' + hold.source +
            '  satellites=' + Object.keys(hold.satellites).length)
const sCols = []
let rows = 0, unresolved = []
for (const b of reg.books) {
  if (HIDDEN.has(b.code)) continue
  const served = hold.satellites[b.code]
  if (!served || !served.holdings || served.holdings.length === 0) { unresolved.push(b.code); continue }
  const alloc = {}
  for (const r of served.holdings) {
    const k = r.asset_class
    if (k) alloc[k] = (alloc[k] ?? 0) + (Number(r.weight) || 0)
  }
  rows += served.holdings.length
  const cv = classValuesOf(alloc)
  sCols.push(cv)
  console.log('   ' + b.code + '  rows=' + served.holdings.length + '  ' + fmt(cv))
}
console.log('  SERVED ROW DENOMINATOR: ' + rows + ' rows across ' + sCols.length +
            ' displayed satellites; unresolved=' + JSON.stringify(unresolved))
console.log('  EXPECTED SATELLITES presence (' + sCols.length + ' columns): ' + JSON.stringify(presentOver(sCols)))
console.log('  SATELLITES footer as_of (holdings.json as_of -> data_as_of): ' + hold.as_of)

// THE POST-R2 LABEL WITNESSES the task order names, read from the bytes the capture uses.
for (const [code, ticker, ac, sac] of [
  ['Opal Satellite 15', 'GLD', 'commodities', 'Metals'],
  ['Opal Satellite 80', 'VXX', 'structured', 'Hedge']]) {
  const r = hold.satellites[code]?.holdings.find((h) => h.ticker === ticker)
  console.log('  R2 WITNESS ' + code + ' / ' + ticker + '  served=' +
              (r ? JSON.stringify([r.asset_class, r.sub_asset_class]) : 'ABSENT') +
              '  target=' + JSON.stringify([ac, sac]) +
              '  ' + (r && r.asset_class === ac && r.sub_asset_class === sac ? 'AT TARGET' : 'NOT AT TARGET'))
}
