'use strict';
// POSN_ASTTAX.TO-V8-1 / V8-AC10 -- build the ui-smoke fixtures file from the ARTIFACTS THE
// PLANE SERVES RIGHT NOW, AFTER the driven refresh of V8-AC14/V8-AC15.
//
// EXTENDS slot ~22's build_fixtures_v7.js (which extended build_fixtures_v2.js). ONE
// structural change: v7 carried the VersionId and LastModified of each key as LITERALS in
// its source. After a driven refresh a typed VersionId is a stale claim about bytes that
// have moved, so this version reads .scratch/v8_fixture_manifest.json, written by
// fetch_served_v8.py at fetch time, and prints what that fetch actually saw.
//
// IT ALSO PRINTS EACH KEY'S VINTAGE. Today only positioning_data.json is POST-RETAG; the
// satellites trio and holdings_attribution_data.json are PRE-RETAG because their producers
// refused (rows W19-S15/S16/S17), and the ETF key is the publisher's, which this order does
// not invoke. A capture read without that line would be read as if the whole plane had
// refreshed.
const fs = require('fs'), zlib = require('zlib'), crypto = require('crypto');

const manifest = JSON.parse(fs.readFileSync('.scratch/v8_fixture_manifest.json', 'utf8'));
const fixtures = {};
for (const m of manifest) {
  const raw = fs.readFileSync(m.local);
  const md5 = crypto.createHash('md5').update(raw).digest('hex');
  const body = JSON.parse((m.gzip ? zlib.gunzipSync(raw) : raw).toString('utf8'));
  fixtures[m.urlkey] = body;
  console.log('FIXTURE KEY ' + m.urlkey);
  console.log('   s3://' + m.bucket + '/' + m.key + '  VersionId=' + m.VersionId +
              '  LastModified=' + m.LastModified + '  bytes=' + raw.length +
              '  md5(raw)=' + md5 + '  gzip=' + m.gzip);
  console.log('   VINTAGE: ' + m.vintage +
              (m.pre_retag_VersionId ? '  (pre-retag VersionId was ' + m.pre_retag_VersionId + ')' : ''));
  if (md5 !== m.md5) { console.log('   BLOCKED: md5 differs from the fetch manifest'); process.exit(1); }
}

const out = process.argv[2];
fs.writeFileSync(out, JSON.stringify(fixtures));
console.log('WROTE ' + out + '  keys=' + Object.keys(fixtures).length + '  bytes=' + fs.statSync(out).size);

// SHADOW CHECK (v7's, kept): ui-smoke resolves by LONGEST matching substring. No key may be
// a substring of another, or the shorter one only serves URLs the longer one misses.
const keys = Object.keys(fixtures);
const shadow = [];
for (const a of keys) for (const b of keys) if (a !== b && b.includes(a)) shadow.push(a + ' < ' + b);
console.log('SHADOW PAIRS among fixture keys: ' + (shadow.length ? shadow.join(' | ') : 'NONE (0 of ' + keys.length + ')'));

// ---- CONTROLS ON THE SERVED CONTENT (observations, never choices) --------------------
const models = fixtures['/api/general/positioning/positioning_data.json'];
console.log('\nMODELS positioning_data: data_as_of=' + models.data_as_of +
            '  books=' + JSON.stringify(Object.keys(models.portfolios)));
console.log('  ST allocation keys = ' + JSON.stringify(Object.keys(models.portfolios.ST.allocation)) +
            '  (five-class keys PRESENT = ' + ('commodities' in models.portfolios.ST.allocation) + ')');
const mClasses = {};
for (const book of Object.keys(models.current_holdings)) {
  for (const h of models.current_holdings[book].holdings) {
    mClasses[String(h.asset_class)] = (mClasses[String(h.asset_class)] || 0) + 1;
  }
}
console.log('  MODELS served asset_class vocabulary: ' + JSON.stringify(mClasses));

const etfs = fixtures['/api/general/etfs/positioning_data.json'];
const firstEtfBook = Object.keys(etfs.portfolios)[0];
const etfAllocKeys = Object.keys(etfs.portfolios[firstEtfBook].allocation || {});
console.log('ETFS platinum/etfs/positioning_data.json: allocation keys = ' + JSON.stringify(etfAllocKeys) +
            '  (five-class keys PRESENT = ' + etfAllocKeys.includes('commodities') + ')');

const reg = fixtures['/api/scoped/satellites/registry.json'];
console.log('\nSATELLITES registry.json: as_of=' + reg.as_of + '  books=' + reg.books.length);

const hold = fixtures['/api/scoped/satellites/holdings.json'];
console.log('SATELLITES holdings.json: as_of=' + hold.as_of +
            '  satellites=' + Object.keys(hold.satellites).length + '  source=' + hold.source);
let totalRows = 0, unlabelled = 0;
const classCount = {};
const satTotals = {};
for (const code of Object.keys(hold.satellites)) {
  const rows = hold.satellites[code].holdings;
  totalRows += rows.length;
  let sum = 0;
  for (const r of rows) {
    classCount[String(r.asset_class)] = (classCount[String(r.asset_class)] || 0) + 1;
    if (r.asset_class === null || r.asset_class === undefined || r.asset_class === '') unlabelled++;
    sum += r.weight;
  }
  satTotals[code] = Math.round(sum * 100) / 100;
  console.log('   ' + code + '  rows=' + rows.length + '  weight total=' + satTotals[code] +
              '  coverage=' + JSON.stringify(hold.satellites[code].coverage));
}
console.log('  SERVED ROW DENOMINATOR: ' + totalRows + ' rows across ' +
            Object.keys(hold.satellites).length + ' satellites');
console.log('  SERVED asset_class vocabulary (count per token): ' + JSON.stringify(classCount));
console.log('  ROWS WITH A NULL asset_class: ' + unlabelled + ' of ' + totalRows);

// THE R1 WITNESSES THE CRITERION NAMES, read from the bytes the capture will use.
for (const [code, ticker, targetAc, targetSac] of [
  ['Opal Satellite 15', 'GLD', 'commodities', 'Metals'],
  ['Opal Satellite 80', 'VXX', 'structured', 'Hedge'],
  ['Opal Satellite 80', 'GLD', 'commodities', 'Metals']]) {
  const r = hold.satellites[code].holdings.find(h => h.ticker === ticker);
  const ok = r && r.asset_class === targetAc && r.sub_asset_class === targetSac;
  console.log('  R1 WITNESS  ' + code + ' / ' + ticker + '  weight=' + (r ? r.weight : 'ABSENT') +
              '  served=' + (r ? JSON.stringify([r.asset_class, r.sub_asset_class]) : '-') +
              '  target=' + JSON.stringify([targetAc, targetSac]) +
              '  ' + (r ? (ok ? 'AT TARGET' : 'NOT AT TARGET (producer has not re-run)') : ''));
}

const chars = fixtures['/api/scoped/satellites/characteristics.json'];
console.log('\nSATELLITES characteristics.json: as_of=' + chars.as_of +
            '  satellites=' + Object.keys(chars.satellites).length);
console.log('  inputs=' + JSON.stringify(chars.inputs));
let nullScalars = 0, scalarCells = 0;
for (const code of Object.keys(chars.satellites)) {
  const c = chars.satellites[code];
  for (const f of ['fee', 'yield', 'duration', 'beta']) {
    scalarCells++;
    if (c[f] === null || c[f] === undefined) nullScalars++;
  }
}
console.log('  NULL SCALAR CHARACTERISTICS: ' + nullScalars + ' of ' + scalarCells +
            ' (4 fields x ' + Object.keys(chars.satellites).length + ' satellites)');
console.log('  COVERAGE PAIRS (the nine, for the V8-AC15 unchanged-comparison):');
for (const code of Object.keys(chars.satellites)) {
  const c = chars.satellites[code];
  console.log('    ' + code + '  weight_with_value=' + JSON.stringify(c.coverage.weight_with_value) +
              '  weight_null=' + JSON.stringify(c.coverage.weight_null));
}
fs.writeFileSync('.scratch/v8_sat_weight_totals.json', JSON.stringify(satTotals, null, 2));
console.log('\nWROTE .scratch/v8_sat_weight_totals.json (per-satellite served weight totals)');
