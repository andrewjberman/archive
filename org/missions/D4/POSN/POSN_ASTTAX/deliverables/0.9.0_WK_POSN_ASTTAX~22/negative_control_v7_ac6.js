'use strict';
/**
 * POSN_ASTTAX.TO-V7-1 / V7-AC6 -- A FETCH FAILURE IS NOT AN EMPTY SATELLITE.
 *
 * Drives the Positioning page with `holdings.json` FORCED TO FAIL through ui-smoke's own
 * forced-failure route (ui-smoke.mjs:160-200: `--fail <substring>` is evaluated BEFORE the
 * fixture map, so a failed URL stays failed even when fixtured) and reads the DOM. The
 * body is never hand-edited: registry.json and characteristics.json keep serving the SAME
 * fixture bytes the passing run used, so the only thing that changed between the two arms
 * is whether the holdings read returned.
 *
 * THREE ARMS, because a notice on screen does not by itself prove WHERE the honest branch
 * lives, and an error notice that would appear anyway proves nothing at all:
 *
 *   ARM 1  DIRECT -- call `getSatelliteHoldings()` in the page with the URL forced to
 *          fail, and record whether it THROWS or returns. This is the seam the criterion
 *          is about; everything else is downstream of it.
 *   ARM 2  RENDERED, FORCED-FAIL -- the page under the same forced failure: which notice,
 *          and how many satellite holding rows are rendered. An EMPTY SATELLITE (a
 *          selectable satellite with zero rows and no notice) is the failure this arm
 *          exists to catch: the fallback removed @24a8435642 re-created one layer up.
 *   ARM 3  POSITIVE CONTROL, NO FORCED FAIL -- the same script, same fixtures, nothing
 *          forced. If arm 3 also showed the notice, arm 2 would be measuring the harness.
 *
 * ARM 4 runs the REAL `scripts/ui-smoke.mjs` with the same `--fail`, so the instrument the
 * criterion names is exercised rather than only reproduced, and its FORCED-FAIL line and
 * screenshot are on the record.
 *
 * Env (defaults are this run's): V7_PORT, V7_FIXTURES, V7_OUT.
 */
const path = require('path');
const fs = require('fs');
const { spawnSync } = require('child_process');

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
const PORTAL = path.join(ROOT, 'portal');
const { chromium } = require(path.join(PORTAL, 'node_modules', 'playwright-core'));

const PORT = process.env.V7_PORT || '5181';
const FIXTURES_PATH = process.env.V7_FIXTURES || path.join(ROOT, '.scratch', 'v7_fixtures.json');
const OUT = process.env.V7_OUT || path.join(ROOT, '.scratch', 'v7_ac6_negative_control.json');
const FAIL_SUBSTRING = '/api/scoped/satellites/holdings.json';

const fixtures = JSON.parse(fs.readFileSync(FIXTURES_PATH, 'utf8'));
const fixtureKeys = Object.keys(fixtures).sort((a, b) => b.length - a.length);
const ORIGIN = `http://localhost:${PORT}`;
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

const READ_DOM = () => {
  const txt = (el) => (el.textContent || '').replace(/\s+/g, ' ').trim();
  const tables = Array.from(document.querySelectorAll('table'));
  const table = tables.find((t) => {
    const h = txt(t.querySelector('thead') || t).toUpperCase();
    return h.includes('ASSET CLASS') && h.includes('TICKER');
  });
  let rows = 0;
  if (table) {
    for (const tr of Array.from(table.querySelectorAll('tbody tr'))) {
      const cells = Array.from(tr.querySelectorAll('td')).map(txt);
      if (cells.length < 4) continue;
      if (cells.join(' | ').toUpperCase().includes('TOTAL')) continue;
      rows++;
    }
  }
  const body = document.body.innerText.replace(/\s+/g, ' ');
  const notices = Array.from(document.querySelectorAll('div'))
    .map(txt)
    .filter((t) => t && t.length < 400 &&
      /could not be loaded|No satellites to show|could not be computed|not shown|Unresolved/i.test(t));
  const buttons = Array.from(document.querySelectorAll('button,[role=button],[role=tab]'))
    .map((e) => e.getAttribute('aria-label') || txt(e)).filter(Boolean);
  return {
    holdingRowsRendered: rows,
    notices: Array.from(new Set(notices)),
    satelliteTabs: buttons.filter((b) => /Opal Satellite/i.test(b)),
    saysCouldNotLoad: /could not be loaded/i.test(body),
    saysNoSatellites: /No satellites to show/i.test(body),
    saysNoHoldings: /no holdings/i.test(body),
    bodyLen: body.length,
  };
};

async function run(forceFail) {
  const browser = await chromium.launch({ executablePath: EDGE, headless: true });
  const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
  const forced = [];
  const served = [];
  page.on('pageerror', (e) => console.log('   PAGE-CRASH:', String(e).slice(0, 200)));
  // ONE ROUTER, forced failures FIRST -- ui-smoke.mjs:160-200's order, verbatim in effect.
  await page.route('**/*', (r) => {
    const req = r.request();
    const url = req.url();
    if (req.method() === 'OPTIONS' && !url.startsWith(ORIGIN)) {
      return r.fulfill({ status: 204, headers: CORS, body: '' });
    }
    if (forceFail && url.includes(FAIL_SUBSTRING)) {
      forced.push(url);
      return r.fulfill({ status: 503, headers: CORS, body: JSON.stringify({ error: 'ui-smoke forced failure' }) });
    }
    const fk = fixtureKeys.find((k) => url.includes(k));
    if (fk) {
      if (url.includes('/api/scoped/satellites/')) served.push('200 ' + url);
      return r.fulfill({ status: 200, headers: CORS, body: JSON.stringify(fixtures[fk]) });
    }
    if (url.includes('/auth/refresh')) return r.fulfill({ status: 200, headers: CORS, body: JSON.stringify(SESSION) });
    return r.continue();
  });

  await page.goto(ORIGIN + '/positioning', { waitUntil: 'networkidle', timeout: 30000 })
    .catch((e) => console.log('   goto:', e.message.split('\n')[0]));
  await page.waitForTimeout(2500);

  // ARM 1 -- THE SEAM ITSELF.
  const direct = await page.evaluate(async () => {
    const reg = await import('/src/api/endpoints/satelliteRegistry.ts');
    const out = {};
    for (const fn of ['getSatelliteHoldings', 'getSatelliteRegistry']) {
      try {
        const v = await reg[fn]('cottonwood');
        out[fn] = { threw: false, returned: JSON.stringify(v).slice(0, 180) };
      } catch (e) {
        out[fn] = { threw: true, message: String(e && e.message ? e.message : e).slice(0, 220) };
      }
    }
    return out;
  });

  await page.getByRole('button', { name: 'Satellites', exact: true })
    .or(page.getByRole('tab', { name: 'Satellites', exact: true })).first().click()
    .catch((e) => console.log('   CLICK-FAIL:', e.message.split('\n')[0]));
  await page.waitForTimeout(3000);
  const dom = await page.evaluate(READ_DOM);
  await page.screenshot({ path: path.join(PORTAL, '.scratch', forceFail ? 'v7_ac6_forced_fail.png' : 'v7_ac6_control.png'), fullPage: true });
  await browser.close();
  return { forcedUrls: forced, servedScoped: served, direct, dom };
}

(async () => {
  console.log('V7-AC6 NEGATIVE CONTROL -- forced-fail substring: ' + FAIL_SUBSTRING);
  console.log('  port=' + PORT + '  fixtures=' + FIXTURES_PATH + '  keys=' + fixtureKeys.length);
  console.log('');

  console.log('===== ARM 2/1: FORCED FAILURE ON holdings.json =====');
  const failArm = await run(true);
  console.log('  FORCED-FAIL fired on ' + failArm.forcedUrls.length + ' request(s): ' + JSON.stringify(failArm.forcedUrls));
  console.log('  scoped satellites URLs still served 200: ' + JSON.stringify(failArm.servedScoped));
  console.log('  ARM 1 getSatelliteHoldings  -> ' + JSON.stringify(failArm.direct.getSatelliteHoldings));
  console.log('  ARM 1 getSatelliteRegistry  -> ' + JSON.stringify(failArm.direct.getSatelliteRegistry));
  console.log('  ARM 2 holding rows rendered : ' + failArm.dom.holdingRowsRendered);
  console.log('  ARM 2 satellite tabs        : ' + failArm.dom.satelliteTabs.length + ' ' + JSON.stringify(failArm.dom.satelliteTabs));
  console.log('  ARM 2 notices               : ' + JSON.stringify(failArm.dom.notices));
  console.log('  ARM 2 "could not be loaded" : ' + failArm.dom.saysCouldNotLoad +
              '   "No satellites to show": ' + failArm.dom.saysNoSatellites +
              '   "no holdings": ' + failArm.dom.saysNoHoldings);
  console.log('');

  console.log('===== ARM 3: POSITIVE CONTROL, NOTHING FORCED =====');
  const okArm = await run(false);
  console.log('  FORCED-FAIL fired on ' + okArm.forcedUrls.length + ' request(s)');
  console.log('  ARM 1 getSatelliteHoldings  -> ' + JSON.stringify(okArm.direct.getSatelliteHoldings));
  console.log('  ARM 3 holding rows rendered : ' + okArm.dom.holdingRowsRendered);
  console.log('  ARM 3 satellite tabs        : ' + okArm.dom.satelliteTabs.length);
  console.log('  ARM 3 notices               : ' + JSON.stringify(okArm.dom.notices));
  console.log('  ARM 3 "could not be loaded" : ' + okArm.dom.saysCouldNotLoad);
  console.log('');

  console.log('===== ARM 4: THE REAL scripts/ui-smoke.mjs WITH --fail =====');
  const r = spawnSync(process.execPath, [
    'scripts/ui-smoke.mjs', 'positioning', '.scratch/v7_ac6_uismoke.png',
    '--port', PORT, '--fixtures', FIXTURES_PATH,
    '--fail', FAIL_SUBSTRING, '--click', 'Satellites',
  ], { cwd: PORTAL, encoding: 'utf8', timeout: 180000 });
  console.log((r.stdout || '').trim().split('\n').map((l) => '  ' + l).join('\n'));
  if (r.stderr && r.stderr.trim()) console.log('  STDERR: ' + r.stderr.trim().slice(0, 500));
  console.log('  ui-smoke exit code: ' + r.status);
  console.log('');

  const verdict = {
    readThrows: failArm.direct.getSatelliteHoldings.threw === true,
    registryAlsoThrows: failArm.direct.getSatelliteRegistry.threw === true,
    errorNoticeShown: failArm.dom.saysCouldNotLoad === true,
    noEmptySatelliteRendered: failArm.dom.holdingRowsRendered === 0 && failArm.dom.satelliteTabs.length === 0,
    noMisleadingEmptyCopy: failArm.dom.saysNoSatellites === false && failArm.dom.saysNoHoldings === false,
    controlRendersRows: okArm.dom.holdingRowsRendered > 0,
    controlShowsNoNotice: okArm.dom.saysCouldNotLoad === false,
  };
  console.log('===== READINGS =====');
  for (const [k, v] of Object.entries(verdict)) console.log('  ' + k.padEnd(26) + ' : ' + v);
  fs.writeFileSync(OUT, JSON.stringify({ failArm, okArm, verdict }, null, 1));
  console.log('JSON: ' + OUT);
})();
