'use strict';
// Build the ui-smoke fixtures file from the ARTIFACTS THE PLANE SERVES RIGHT NOW,
// pulled with s3api get-object from s3://opal-data-portal-v2 (the origin behind the
// CloudFront /api/general/* behaviour). The transport is stubbed; the BYTES are served.
const fs = require('fs'), zlib = require('zlib'), crypto = require('crypto');
const src = [
  ['.scratch/posn_served_v2.raw', true,  'json/positioning/positioning_data.json',           'OuevyO7kCIJdEqzGlJWd.z.8S8pqiXJk', '2026-09-14T21:21:33Z', '/api/general/positioning/positioning_data.json'],
  ['.scratch/etf_served_v2.raw',  false, 'platinum/etfs/positioning_data.json',              'MkASX8obEltFZpHHzNa81cuAVXKf7wR2', '2026-09-14T13:01:25Z', '/api/general/etfs/positioning_data.json'],
  ['.scratch/attr_served_v2.raw', false, 'json/positioning/holdings_attribution_data.json',  'mOBBmXhjOyNPM2ue_.3C9G1eR79lUrlk', '2026-09-04T13:51:29Z', '/api/general/positioning/holdings_attribution_data.json'],
];
const fixtures = {};
for (const [p, gz, key, ver, lm, urlkey] of src) {
  const raw = fs.readFileSync(p);
  const md5 = crypto.createHash('md5').update(raw).digest('hex');
  const body = JSON.parse((gz ? zlib.gunzipSync(raw) : raw).toString('utf8'));
  fixtures[urlkey] = body;
  console.log('FIXTURE KEY ' + urlkey);
  console.log('   s3 key=' + key + '  VersionId=' + ver + '  LastModified=' + lm +
              '  bytes=' + raw.length + '  md5(raw)=' + md5 + '  gzip=' + gz);
}
const out = process.argv[2];
fs.writeFileSync(out, JSON.stringify(fixtures));
console.log('WROTE ' + out + '  keys=' + Object.keys(fixtures).length + '  bytes=' + fs.statSync(out).size);

// CONTROLS on the served content itself (post-B1 or pre-B1 is an observation, not a choice).
const models = fixtures['/api/general/positioning/positioning_data.json'];
const books = Object.keys(models.portfolios || {});
console.log('MODELS books: ' + JSON.stringify(books));
for (const b of books) {
  const a = models.portfolios[b].allocation;
  const sum = Object.values(a).reduce((s, x) => s + x, 0);
  console.log('  ' + b + ' allocation=' + JSON.stringify(a) + '  sum=' + sum.toFixed(3));
}
const bm = (models.benchmarks && models.benchmarks.etf) || {};
console.log('BENCHMARKS etf keys: ' + JSON.stringify(Object.keys(bm)));
for (const k of ['structured', 'commodities', 'alternatives']) {
  console.log('  benchmarks.etf.' + k + ' = ' + JSON.stringify(bm[k]));
}
const etfs = fixtures['/api/general/etfs/positioning_data.json'];
console.log('ETFS top keys: ' + JSON.stringify(Object.keys(etfs)).slice(0, 200));
const attr = fixtures['/api/general/positioning/holdings_attribution_data.json'];
console.log('ATTR top keys: ' + JSON.stringify(Object.keys(attr)).slice(0, 200));
