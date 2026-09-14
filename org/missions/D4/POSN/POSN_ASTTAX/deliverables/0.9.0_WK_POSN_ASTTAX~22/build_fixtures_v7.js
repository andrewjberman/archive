'use strict';
// POSN_ASTTAX.TO-V7-1 / V7-AC5 -- build the ui-smoke fixtures file from the ARTIFACTS THE
// PLANE SERVES RIGHT NOW. Extends build_fixtures_v2.js (TO-V6-1) with the three SATELLITES
// keys, which live in the FIRM BUCKET (opal-data-cot) rather than in opal-data-portal-v2:
// the scoped route resolves firm -> bucket, and the key carries no firm segment.
//
// NEVER HAND-WRITTEN. Each row below names the s3 key, the VersionId and the LastModified
// of the bytes it read, and prints them beside an md5 of the raw file -- so the fixture a
// screenshot was taken against is identifiable later by content, not by filename.
//
// The transport is stubbed by ui-smoke; the BYTES are the served ones.
const fs = require('fs'), zlib = require('zlib'), crypto = require('crypto');

const src = [
  // [local raw, gzipped, bucket, s3 key, VersionId, LastModified, fixture URL key]
  ['.scratch/posn_served_v2.raw', true,  'opal-data-portal-v2', 'json/positioning/positioning_data.json',
   'OuevyO7kCIJdEqzGlJWd.z.8S8pqiXJk', '2026-09-14T21:21:33Z', '/api/general/positioning/positioning_data.json'],
  ['.scratch/etf_served_v2.raw',  false, 'opal-data-portal-v2', 'platinum/etfs/positioning_data.json',
   'MkASX8obEltFZpHHzNa81cuAVXKf7wR2', '2026-09-14T13:01:25Z', '/api/general/etfs/positioning_data.json'],
  ['.scratch/attr_served_v2.raw', false, 'opal-data-portal-v2', 'json/positioning/holdings_attribution_data.json',
   'mOBBmXhjOyNPM2ue_.3C9G1eR79lUrlk', '2026-09-04T13:51:29Z', '/api/general/positioning/holdings_attribution_data.json'],
  ['.scratch/sat_registry.raw',   false, 'opal-data-cot', 'platinum/satellites/registry.json',
   'XaX6zaVWH7ybXnRBu2jeF2PNABUhezuM', '2026-09-14T19:53:58Z', '/api/scoped/satellites/registry.json'],
  ['.scratch/sat_holdings.raw',   false, 'opal-data-cot', 'platinum/satellites/holdings.json',
   'BRjqyqnB0pIdLUHOvDY3B_Sh9b0EXIPw', '2026-09-14T19:53:59Z', '/api/scoped/satellites/holdings.json'],
  ['.scratch/sat_characteristics.raw', false, 'opal-data-cot', 'platinum/satellites/characteristics.json',
   'rt61ogajZQy79meUlsY1X_mIdPngxJTZ', '2026-09-14T21:45:13Z', '/api/scoped/satellites/characteristics.json'],
];

const fixtures = {};
for (const [p, gz, bucket, key, ver, lm, urlkey] of src) {
  const raw = fs.readFileSync(p);
  const md5 = crypto.createHash('md5').update(raw).digest('hex');
  const body = JSON.parse((gz ? zlib.gunzipSync(raw) : raw).toString('utf8'));
  fixtures[urlkey] = body;
  console.log('FIXTURE KEY ' + urlkey);
  console.log('   s3://' + bucket + '/' + key + '  VersionId=' + ver + '  LastModified=' + lm +
              '  bytes=' + raw.length + '  md5(raw)=' + md5 + '  gzip=' + gz);
}
const out = process.argv[2];
fs.writeFileSync(out, JSON.stringify(fixtures));
console.log('WROTE ' + out + '  keys=' + Object.keys(fixtures).length + '  bytes=' + fs.statSync(out).size);

// SHADOW CHECK: ui-smoke resolves by LONGEST matching substring. No key below may be a
// substring of another, or the shorter one only ever serves URLs the longer one misses.
const keys = Object.keys(fixtures);
const shadow = [];
for (const a of keys) for (const b of keys) if (a !== b && b.includes(a)) shadow.push(a + ' < ' + b);
console.log('SHADOW PAIRS among fixture keys: ' + (shadow.length ? shadow.join(' | ') : 'NONE (0 of ' + keys.length + ')'));

// ---- CONTROLS ON THE SERVED CONTENT ITSELF (an observation, never a choice) ----------
const models = fixtures['/api/general/positioning/positioning_data.json'];
console.log('\nMODELS positioning_data: data_as_of=' + models.data_as_of + '  books=' + JSON.stringify(Object.keys(models.portfolios)));
console.log('  ST allocation keys = ' + JSON.stringify(Object.keys(models.portfolios.ST.allocation)) +
            '  (B1 five-class keys PRESENT = ' + ('commodities' in models.portfolios.ST.allocation) + ')');

const etfs = fixtures['/api/general/etfs/positioning_data.json'];
const etfAllocKeys = Object.keys(etfs.portfolios[Object.keys(etfs.portfolios)[0]].allocation || {});
console.log('ETFS platinum/etfs/positioning_data.json: allocation keys = ' + JSON.stringify(etfAllocKeys) +
            '  (B1 five-class keys PRESENT = ' + etfAllocKeys.includes('commodities') + ')');

const reg = fixtures['/api/scoped/satellites/registry.json'];
console.log('\nSATELLITES registry.json: as_of=' + reg.as_of + '  books=' + reg.books.length);

const hold = fixtures['/api/scoped/satellites/holdings.json'];
console.log('SATELLITES holdings.json: as_of=' + hold.as_of + '  satellites=' + Object.keys(hold.satellites).length +
            '  source=' + hold.source);
let totalRows = 0, unlabelled = 0;
const classCount = {};
for (const code of Object.keys(hold.satellites)) {
  const rows = hold.satellites[code].holdings;
  totalRows += rows.length;
  for (const r of rows) {
    classCount[String(r.asset_class)] = (classCount[String(r.asset_class)] || 0) + 1;
    if (r.asset_class === null || r.asset_class === undefined || r.asset_class === '') unlabelled++;
  }
  console.log('   ' + code + '  rows=' + rows.length + '  coverage=' + JSON.stringify(hold.satellites[code].coverage));
}
console.log('  SERVED ROW DENOMINATOR: ' + totalRows + ' rows across ' + Object.keys(hold.satellites).length + ' satellites');
console.log('  SERVED asset_class vocabulary (count per token): ' + JSON.stringify(classCount));
console.log('  ROWS WITH A NULL asset_class: ' + unlabelled + ' of ' + totalRows);

for (const [code, ticker] of [['Opal Satellite 15', 'GLD'], ['Opal Satellite 80', 'VXX'], ['Opal Satellite 80', 'GLD']]) {
  const r = hold.satellites[code].holdings.find(h => h.ticker === ticker);
  console.log('  R1 WITNESS  ' + code + ' / ' + ticker + '  weight=' + (r ? r.weight : 'ABSENT') +
              '  asset_class=' + (r ? JSON.stringify(r.asset_class) : '-') +
              '  sub_asset_class=' + (r ? JSON.stringify(r.sub_asset_class) : '-'));
}

const chars = fixtures['/api/scoped/satellites/characteristics.json'];
console.log('\nSATELLITES characteristics.json: as_of=' + chars.as_of + '  satellites=' + Object.keys(chars.satellites).length);
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
const s15 = chars.satellites['Opal Satellite 15'];
console.log('  Opal Satellite 15  fee=' + s15.fee + ' yield=' + s15.yield + ' duration=' + s15.duration + ' beta=' + s15.beta);
console.log('    coverage.weight_with_value = ' + JSON.stringify(s15.coverage.weight_with_value));
console.log('    coverage.weight_null       = ' + JSON.stringify(s15.coverage.weight_null));
