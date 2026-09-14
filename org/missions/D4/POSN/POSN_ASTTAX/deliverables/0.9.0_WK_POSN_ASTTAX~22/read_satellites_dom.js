'use strict';
/**
 * POSN_ASTTAX.TO-V7-1 / V7-AC5 -- READ THE RENDERED SATELLITES MODE FROM THE DOM.
 *
 * The screenshot is the primary reading; this is the COUNTING instrument beside it.
 * A criterion of the form "served rows == rendered rows (count both)" cannot be answered
 * by looking at a PNG: a row scrolled out of frame and a row the renderer dropped look
 * identical there. This reads the table's own <tr>s.
 *
 * SAME ROUTE STUB AS ui-smoke.mjs:160-200 -- OPTIONS -> 204, forced failures BEFORE
 * fixtures, fixtures -> 200 by longest matching substring, /auth/refresh -> a real-shaped
 * session, everything else through. Reproduced rather than imported because ui-smoke.mjs
 * is a .mjs CLI with no exported surface and it is NOT in this TO's write grant, so it
 * could not be given one.
 *
 * usage: node read_satellites_dom.js --port <p> --fixtures <f.json> [--fail <substr>]...
 *                                    [--tab "<satellite name>"]... [--json <out>]
 */
const path = require('path');
const fs = require('fs');

// Device-neutral: walk up from this file to the workspace root (the directory that
// carries `portal/`), then resolve the browser driver out of portal's node_modules.
// Never a baked drive path -- CLAUDE.md "DERIVE, don't hardcode".
function findWorkspaceRoot(start) {
  let d = start;
  for (let i = 0; i < 12; i++) {
    if (fs.existsSync(path.join(d, 'portal', 'package.json'))) return d;
    const up = path.dirname(d);
    if (up === d) break;
    d = up;
  }
  throw new Error('could not locate the workspace root (a directory containing portal/package.json) from ' + start);
}
const ROOT = findWorkspaceRoot(__dirname);
const PORTAL = path.join(ROOT, 'portal');
const { chromium } = require(path.join(PORTAL, 'node_modules', 'playwright-core'));

const args = process.argv.slice(2);
const argOf = (n, d) => (args.includes(n) ? args[args.indexOf(n) + 1] : d);
const allOf = (n) => args.reduce((a, x, i) => (x === n && args[i + 1] ? [...a, args[i + 1]] : a), []);
const port = argOf('--port', '5175');
const fixturesPath = argOf('--fixtures', null);
const jsonOut = argOf('--json', null);
const failSubstrings = allOf('--fail');
const tabs = allOf('--tab');
const fixtures = fixturesPath ? JSON.parse(fs.readFileSync(fixturesPath, 'utf8')) : {};
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
  user: { email: 'dev@opalcapital.com', name: 'Dev User', role: 'admin',
          userType: 'Dev', firmId: 'opal-capital', firmRole: null, advisorId: null,
          advisorRole: null, mustChangePassword: false },
};

const fixtureKeys = Object.keys(fixtures).sort((a, b) => b.length - a.length);
const matchFixture = (url) => fixtureKeys.find((k) => url.includes(k));
const matchFail = (url) => failSubstrings.find((k) => url.includes(k));

// The DOM read, run in the page. Returns the holdings table as DATA, plus every
// canvas-level notice and every satellite tab name.
const READ = () => {
  const txt = (el) => (el.textContent || '').replace(/\s+/g, ' ').trim();
  const tables = Array.from(document.querySelectorAll('table'));
  // The holdings table is the one whose header row carries ASSET CLASS + TICKER.
  const table = tables.find((t) => {
    const h = txt(t.querySelector('thead') || t).toUpperCase();
    return h.includes('ASSET CLASS') && h.includes('TICKER');
  });
  const rows = [];
  const totals = [];
  if (table) {
    for (const tr of Array.from(table.querySelectorAll('tbody tr'))) {
      const cells = Array.from(tr.querySelectorAll('td')).map(txt);
      if (cells.length < 4) continue;
      const joined = cells.join(' | ').toUpperCase();
      if (joined.includes('TOTAL')) { totals.push(cells.filter(Boolean).join(' | ')); continue; }
      rows.push({ assetClass: cells[0], subAsset: cells[1], ticker: cells[2], name: cells[3], weight: cells[4] });
    }
  }
  const notices = Array.from(document.querySelectorAll('div'))
    .map(txt)
    .filter((t) => t && t.length < 400 && /could not be loaded|not shown|Unresolved|Producer defect|no satellites|not published|unavailable|error/i.test(t));
  const buttons = Array.from(document.querySelectorAll('button,[role=button],[role=tab]'))
    .map((e) => e.getAttribute('aria-label') || txt(e))
    .filter(Boolean);
  const body = document.body.innerText.replace(/\s+/g, ' ');
  const asOfMatches = (body.match(/(as of|As of|AS OF)[^.|]{0,40}/g) || []).slice(0, 10);
  const dateMatches = Array.from(new Set(body.match(/20\d\d-\d\d-\d\d|\b\d{1,2}\/\d{1,2}\/20\d\d\b|\b[A-Z][a-z]{2} \d{1,2}, 20\d\d\b/g) || []));
  return {
    tableFound: Boolean(table),
    rows,
    totals,
    notices: Array.from(new Set(notices)),
    satelliteTabs: buttons.filter((b) => /Satellite/i.test(b)),
    controlNames: buttons.slice(0, 60),
    asOfMatches,
    dateMatches,
    bodyHead: body.slice(0, 400),
    // The WHOLE body text. A criterion of the form "the as-of SHOWN is X" is answered by
    // the absence of any date as much as by the presence of one, and a narrow regex cannot
    // tell "no date rendered" from "a date in a format I did not anticipate".
    bodyFull: body,
  };
};

(async () => {
  const browser = await chromium.launch({ executablePath: EDGE, headless: true });
  const page = await browser.newPage({ viewport: { width: 1600, height: 900 } });
  page.on('pageerror', (e) => console.log('PAGE-CRASH:', String(e).slice(0, 300)));
  const seen = [];
  page.on('requestfinished', async (req) => {
    const r = await req.response().catch(() => null);
    if (req.url().includes('/api/')) seen.push((r ? r.status() : '???') + ' ' + req.url());
  });

  await page.route('**/*', (r) => {
    const req = r.request();
    const url = req.url();
    if (req.method() === 'OPTIONS' && !url.startsWith(ORIGIN)) {
      return r.fulfill({ status: 204, headers: CORS, body: '' });
    }
    const failKey = matchFail(url);
    if (failKey) {
      console.log('FORCED-FAIL:', failKey, '->', url);
      return r.fulfill({ status: 503, headers: CORS, body: JSON.stringify({ error: 'forced failure (negative control)' }) });
    }
    const fk = matchFixture(url);
    if (fk) return r.fulfill({ status: 200, headers: CORS, body: JSON.stringify(fixtures[fk]) });
    if (url.includes('/auth/refresh')) {
      return r.fulfill({ status: 200, headers: CORS, body: JSON.stringify(SESSION) });
    }
    return r.continue();
  });

  await page.goto(ORIGIN + '/positioning', { waitUntil: 'networkidle', timeout: 30000 })
    .catch((e) => console.log('goto:', e.message.split('\n')[0]));
  await page.waitForTimeout(3000);
  // --mode <name> picks the mode button; default Satellites. A CONTROL arm needs the
  // OTHER modes reachable through the same instrument, or a difference between modes
  // cannot be told from a property of the instrument.
  const modeName = argOf('--mode', 'Satellites');
  await page.getByRole('button', { name: modeName, exact: true })
    .or(page.getByRole('tab', { name: modeName, exact: true })).first().click();
  console.log('CLICKED:', modeName);
  await page.waitForTimeout(3000);

  const out = { port, fixtures: fixtureKeys, forcedFail: failSubstrings, reads: {} };
  const targets = tabs.length ? tabs : [null];
  for (const t of targets) {
    if (t) {
      try {
        await page.getByRole('button', { name: t, exact: true })
          .or(page.getByRole('tab', { name: t, exact: true })).first().click();
        console.log('CLICKED TAB:', t);
      } catch (e) {
        console.log('TAB-CLICK-FAIL:', t, '--', e.message.split('\n')[0]);
      }
      await page.waitForTimeout(2500);
    }
    const read = await page.evaluate(READ);
    const label = t || '(default tab)';
    out.reads[label] = read;
    console.log('\n===== RENDERED READ: ' + label + ' =====');
    console.log('  holdings table found : ' + read.tableFound);
    console.log('  RENDERED ROWS        : ' + read.rows.length);
    for (const r of read.rows) {
      console.log('     %-14s %-22s %-8s %-10s %s', r.assetClass, r.subAsset, r.ticker, r.name, r.weight);
    }
    console.log('  TOTAL ROWS RENDERED  : ' + JSON.stringify(read.totals));
    console.log('  SATELLITE TABS       : ' + read.satelliteTabs.length + ' -> ' + JSON.stringify(read.satelliteTabs));
    console.log('  NOTICES              : ' + JSON.stringify(read.notices));
    console.log('  DATE STRINGS ON PAGE : ' + JSON.stringify(read.dateMatches));
    console.log('  "as of" PHRASES      : ' + JSON.stringify(read.asOfMatches));
  }

  console.log('\nAPI REQUESTS OBSERVED (' + seen.length + '):');
  for (const s of Array.from(new Set(seen))) console.log('   ' + s);
  if (jsonOut) { fs.writeFileSync(jsonOut, JSON.stringify(out, null, 1)); console.log('JSON: ' + jsonOut); }
  await browser.close();
})();
