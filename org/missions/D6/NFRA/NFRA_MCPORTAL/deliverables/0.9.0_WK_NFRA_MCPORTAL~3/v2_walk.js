// MP-v-2 walk (FWD-2 live arms). One node script, run in the background, prints statuses only.
// Headed Edge from the portal's own playwright-core; the profile dir is under this worktree's .scratch/ (ignored).
// No cookie, token, header or response body is printed or written to the repo; v2_run.json holds only t0 and t1.
const path = require('path');
const fs = require('fs');

const ROOT = path.resolve(__dirname, '..', '..', '..', '..', '..', '..', '..');
const PW = path.join(ROOT, 'portal', 'node_modules', 'playwright-core');
const { chromium } = require(PW);

const DELIV = __dirname;
const PROFILE = path.join(DELIV, '.scratch', 'profile-edge');
const BASE = 'https://mcp.opalinvest.dev';
const TID = '00000000-0000-4000-8000-0000000000e5';
const OID = '00000000-0000-4000-8000-0000000000f6';
const SIGNIN_MS = 10 * 60 * 1000;

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const isoSec = () => new Date().toISOString().replace(/\.\d{3}Z$/, 'Z');
const log = (msg) => console.log(new Date().toISOString() + ' ' + msg);

const ROUTES = [
  ['GET', '/'],
  ['GET', '/api/admin/whoami'],
  ['GET', `/api/admin/grants/${TID}/${OID}`],
  ['POST', `/api/admin/grants/${TID}/${OID}/narrow`],
  ['POST', `/api/admin/grants/${TID}/${OID}/widen`],
  ['GET', '/api/admin/changes'],
  ['GET', '/api/admin/fabric/boxes'],
  ['GET', '/api/admin/fabric/overlap'],
  ['GET', '/api/admin/fabric/gitstate'],
  ['GET', '/api/admin/fabric/calls'],
  ['POST', '/api/admin/fabric/calls/close'],
  ['GET', '/api/admin/gateway/breakdown'],
  ['GET', '/api/admin/people'],
];

function writeRun(t0, t1) {
  fs.writeFileSync(path.join(DELIV, 'v2_run.json'), JSON.stringify({ t0, t1 }, null, 2) + '\n', 'utf8');
}

(async () => {
  const t0 = isoSec();
  log('t0=' + t0);
  fs.mkdirSync(PROFILE, { recursive: true });

  const ctx = await chromium.launchPersistentContext(PROFILE, { channel: 'msedge', headless: false });
  const page = ctx.pages()[0] || (await ctx.newPage());
  page.on('response', (r) => {
    try {
      const u = new URL(r.url());
      if (r.request().isNavigation() && u.host === 'mcp.opalinvest.dev') {
        log('NAV ' + r.status() + ' ' + u.pathname);
      }
    } catch (e) { /* status-only logging */ }
  });

  try {
    await page.goto(BASE + '/sprint', { waitUntil: 'domcontentloaded', timeout: 60000 });
  } catch (e) {
    log('goto-error ' + (e && e.name));
  }
  log('SIGN-IN WAIT: sign in as Opal Bloomberg in the Edge window (up to 10 minutes)');

  // Step 3: poll until the page is back on mcp.opalinvest.dev/sprint.
  const deadline = Date.now() + SIGNIN_MS;
  let signedIn = false;
  let lastShown = '';
  while (Date.now() < deadline) {
    await sleep(3000);
    let where = 'unknown';
    try {
      const u = new URL(page.url());
      where = u.host + u.pathname;
      if (u.host === 'mcp.opalinvest.dev' && u.pathname.startsWith('/sprint')) {
        try { await page.waitForLoadState('load', { timeout: 15000 }); } catch (e) { /* load wait only */ }
        signedIn = true;
        break;
      }
    } catch (e) { /* url not parseable yet */ }
    if (where !== lastShown) { log('poll: on ' + where); lastShown = where; }
  }
  if (!signedIn) {
    log('BLOCKING G-2ND: nobody signed in as Opal Bloomberg (no return to mcp.opalinvest.dev/sprint within 10 minutes)');
    await ctx.close();
    process.exit(2);
  }
  log('signed-in page reached: mcp.opalinvest.dev/sprint');

  // Step 4: exactly one request per handler, from the page's own request context, then /sprint once.
  const req = page.request;
  let lastReq = null;
  let stopped = null;
  for (const [method, p] of ROUTES) {
    const opts = { method, maxRedirects: 0, failOnStatusCode: false, timeout: 30000 };
    if (method === 'POST') {
      opts.data = {};
      opts.headers = { 'content-type': 'application/json' };
    }
    let status = 'ERR';
    try {
      const r = await req.fetch(BASE + p, opts);
      status = String(r.status());
    } catch (e) {
      status = 'ERR:' + (e && e.name);
    }
    lastReq = new Date();
    log(method + ' ' + p + ' -> ' + status);
    if (status === '200') {
      stopped = method + ' ' + p;
      break;
    }
  }

  if (!stopped) {
    try {
      const r = await req.fetch(BASE + '/sprint', { method: 'GET', maxRedirects: 0, failOnStatusCode: false, timeout: 30000 });
      log('GET /sprint -> ' + r.status());
    } catch (e) {
      log('GET /sprint -> ERR:' + (e && e.name));
    }
    lastReq = new Date();
  } else {
    log('STOP: 200 on owner route ' + stopped + ' -- BLOCKING finding, no further requests');
  }

  // Step 5: t1 is 60 seconds after the last request.
  await sleep(60000);
  const t1 = isoSec();
  log('t1=' + t1);
  writeRun(t0, t1);
  log('WROTE v2_run.json t0=' + t0 + ' t1=' + t1 + (stopped ? ' STOPPED-AT=' + stopped : ' COMPLETE'));
  await ctx.close();
  process.exit(stopped ? 3 : 0);
})().catch((e) => {
  log('FATAL ' + (e && e.name));
  process.exit(1);
});
