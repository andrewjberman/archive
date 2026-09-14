'use strict';
/**
 * POSN_ASTTAX.TO-V7-1 / V7-AC5 + V7-AC8 -- READ THE ADAPTER'S OWN OUTPUT, IN THE PAGE.
 *
 * WHY THIS EXISTS BESIDE THE DOM READ. Two of the criterion's readings are NOT on screen:
 * the payload's `as_of` (the page renders no date in ANY mode -- measured, both arms), and
 * the five-class allocation totals. Reading them off the source would be a config-read for
 * a behaviour claim; reading them off a re-implementation would measure the
 * re-implementation. So this imports THE MODULES THE RUNNING PAGE IS RUNNING, through the
 * dev server, inside the same stubbed-network page the screenshot was taken in, and calls
 * them. The bytes under test are the bytes the render used.
 *
 * Same route stub as ui-smoke.mjs:160-200 (see read_satellites_dom.js's note).
 *
 * usage: node probe_adapter_output.js --port <p> --fixtures <f.json> [--json <out>]
 */
const path = require('path');
const fs = require('fs');

function findWorkspaceRoot(start) {
  let d = start;
  for (let i = 0; i < 12; i++) {
    if (fs.existsSync(path.join(d, 'portal', 'package.json'))) return d;
    const up = path.dirname(d);
    if (up === d) break;
    d = up;
  }
  throw new Error('could not locate the workspace root from ' + start);
}
const ROOT = findWorkspaceRoot(__dirname);
const { chromium } = require(path.join(ROOT, 'portal', 'node_modules', 'playwright-core'));

const args = process.argv.slice(2);
const argOf = (n, d) => (args.includes(n) ? args[args.indexOf(n) + 1] : d);
const port = argOf('--port', '5175');
const fixtures = JSON.parse(fs.readFileSync(argOf('--fixtures'), 'utf8'));
const jsonOut = argOf('--json', null);
const ORIGIN = `http://localhost:${port}`;
const EDGE = 'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe';
const CORS = {
  'Access-Control-Allow-Origin': ORIGIN,
  'Access-Control-Allow-Credentials': 'true',
  'Access-Control-Allow-Headers': '*',
  'Access-Control-Allow-Methods': '*',
  'Content-Type': 'application/json',
};
const SESSION = {
  accessToken: 'ui-smoke-token',
  user: { email: 'dev@opalcapital.com', name: 'Dev User', role: 'admin', userType: 'Dev',
          firmId: 'opal-capital', firmRole: null, advisorId: null, advisorRole: null,
          mustChangePassword: false },
};
const fixtureKeys = Object.keys(fixtures).sort((a, b) => b.length - a.length);

(async () => {
  const browser = await chromium.launch({ executablePath: EDGE, headless: true });
  const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
  page.on('pageerror', (e) => console.log('PAGE-CRASH:', String(e).slice(0, 300)));
  await page.route('**/*', (r) => {
    const req = r.request();
    const url = req.url();
    if (req.method() === 'OPTIONS' && !url.startsWith(ORIGIN)) return r.fulfill({ status: 204, headers: CORS, body: '' });
    const fk = fixtureKeys.find((k) => url.includes(k));
    if (fk) return r.fulfill({ status: 200, headers: CORS, body: JSON.stringify(fixtures[fk]) });
    if (url.includes('/auth/refresh')) return r.fulfill({ status: 200, headers: CORS, body: JSON.stringify(SESSION) });
    return r.continue();
  });
  await page.goto(ORIGIN + '/positioning', { waitUntil: 'networkidle', timeout: 30000 })
    .catch((e) => console.log('goto:', e.message.split('\n')[0]));
  await page.waitForTimeout(2500);

  const out = await page.evaluate(async () => {
    const reg = await import('/src/api/endpoints/satelliteRegistry.ts');
    const ad = await import('/src/pages/Positioning/shared/satelliteAdapter.ts');
    const r = await reg.getSatelliteRegistry('cottonwood');
    const res = ad.satellitesToPositioningShape(null, r.books);
    const codes = Object.keys(res.data ? res.data.portfolios : {});
    return {
      registryAsOf: r.as_of,
      registryBooks: r.books.map((b) => b.code),
      booksWithServed: r.books.filter((b) => b.served).map((b) => b.code),
      endpoints: [reg.SATELLITE_REGISTRY_ENDPOINT, reg.SATELLITE_HOLDINGS_ENDPOINT, reg.SATELLITE_CHARACTERISTICS_ENDPOINT],
      exportedReads: ['getSatelliteRegistry', 'getSatelliteHoldings', 'getSatelliteCharacteristics']
        .map((n) => n + '=' + typeof reg[n]),
      dataAsOf: res.data ? res.data.data_as_of : null,
      dataDate: res.data ? res.data.data_date : null,
      generatedAt: res.data ? res.data.generated_at : null,
      problems: res.problems,
      unresolved: res.unresolved,
      coverage: res.coverage,
      portfolioCodes: codes,
      perSatellite: codes.map((c) => {
        const p = res.data.portfolios[c];
        const ch = res.data.current_holdings[c];
        const alloc = p.allocation;
        const sum = Object.values(alloc).reduce((a, v) => a + (v || 0), 0);
        return {
          code: c,
          as_of_date: p.as_of_date,
          prior_date: p.prior_date,
          num_holdings: p.num_holdings,
          currentHoldingRows: ch ? ch.holdings.length : 0,
          allocation: alloc,
          allocationSum: Number(sum.toFixed(4)),
          characteristics: p.characteristics,
          gld: (ch ? ch.holdings : []).filter((h) => h.ticker === 'GLD')
            .map((h) => ({ ticker: h.ticker, weight: h.weight, asset_class: h.asset_class, sub_asset_class: h.sub_asset_class })),
          vxx: (ch ? ch.holdings : []).filter((h) => h.ticker === 'VXX')
            .map((h) => ({ ticker: h.ticker, weight: h.weight, asset_class: h.asset_class, sub_asset_class: h.sub_asset_class })),
        };
      }),
    };
  });

  console.log('ENDPOINT CONSTANTS   : ' + JSON.stringify(out.endpoints));
  console.log('EXPORTED READS       : ' + JSON.stringify(out.exportedReads));
  console.log('REGISTRY as_of       : ' + out.registryAsOf + '   books=' + out.registryBooks.length);
  console.log('BOOKS WITH served{}  : ' + out.booksWithServed.length + ' of ' + out.registryBooks.length);
  console.log('ADAPTER data_as_of   : ' + out.dataAsOf + '   data_date=' + out.dataDate + '   generated_at=' + out.generatedAt);
  console.log('problems             : ' + JSON.stringify(out.problems));
  console.log('unresolved           : ' + JSON.stringify(out.unresolved));
  console.log('portfolios rendered  : ' + out.portfolioCodes.length + ' -> ' + JSON.stringify(out.portfolioCodes));
  console.log('');
  for (const s of out.perSatellite) {
    console.log('--- ' + s.code);
    console.log('    as_of_date=' + s.as_of_date + '  prior_date=' + s.prior_date +
                '  num_holdings=' + s.num_holdings + '  current_holdings rows=' + s.currentHoldingRows);
    console.log('    allocation=' + JSON.stringify(s.allocation) + '  sum=' + s.allocationSum);
    console.log('    characteristics=' + JSON.stringify(s.characteristics));
    if (s.gld.length) console.log('    GLD row (adapter output)=' + JSON.stringify(s.gld));
    if (s.vxx.length) console.log('    VXX row (adapter output)=' + JSON.stringify(s.vxx));
  }
  console.log('');
  console.log('RENDER COVERAGE (servedRows / unlabelledRows / offRatified):');
  for (const c of out.coverage) {
    console.log('    %-20s served=%-4s unlabelled=%-3s offRatified=%s',
      c.code, c.servedRows, c.unlabelledRows, JSON.stringify(c.offRatified));
  }
  const totalServed = out.coverage.reduce((a, c) => a + c.servedRows, 0);
  const totalOff = out.coverage.reduce((a, c) => a + c.offRatified.length, 0);
  console.log('    DENOMINATOR: ' + totalServed + ' served rows; ' + totalOff +
              ' outside the ratified five (the holdings table excludes these); ' +
              out.coverage.reduce((a, c) => a + c.unlabelledRows, 0) + ' unlabelled');

  if (jsonOut) { fs.writeFileSync(jsonOut, JSON.stringify(out, null, 1)); console.log('JSON: ' + jsonOut); }
  await browser.close();
})();
