/**
 * windowread.cjs -- DSGN_AMGTV1 round 31, AV-zi-1 (issuer 2.0.0_SA_COO~D): EACH WINDOW IS ITS OWN READ ON THE SERVED ROUTE (PRD FWD-26).
 *
 * Usage (from the directory whose portal/ is the checkout under test, e.g. C:/tmp/wk-dsgn-amgtv1-88): node <this file>
 * Why: the routes take `?days=30|90|365` (deployed opal-amgt-scoped-api KQSA62c3; COO~Z msgs 28860 / 28874). A window the client
 *   does not send is a window the page cannot show, and a window that shares the 30-day query key is served the 30-day cache.
 * THE CONTRACT (the worker face quotes it):
 *   - portal/src/api/endpoints/amgt-lead-panel.ts: `getCollectedChatter(days?: number)` and
 *     `getLeadPanelRankings(movement, subject, limit?, days?)` send `days` as the query parameter `days`; with `days` omitted each
 *     URL is byte-identical to today's.
 *   - hooks/useLeadPanelApi.ts: the collected-chatter query and the ranking query carry the window in their query keys, so 30, 90
 *     and 365 are three cache entries.
 * Render: ./_presets.cjs for the keys; the REAL amgt-lead-panel.ts loaded with `@/api/api-client` replaced by a recorder of the
 *   URL each call asks for.
 * Arms:
 *   1  THE ROUTE: getCollectedChatter() -> ".../timeseries/collected/chatter"; getCollectedChatter(90) -> "...chatter?days=90";
 *      getLeadPanelRankings('TRENDING','PRICE') -> ".../rankings/trending/price"; (..., 500) -> "...price?limit=500";
 *      (..., 500, 365) -> exactly the parameters limit=500 and days=365; (..., undefined, 90) -> exactly days=90.
 *   2  THREE CACHE ENTRIES: rendering the REAL LeadPanel at 30, 90 and 365 days (presets selected through onChange), the enabled
 *      query that reads collected chatter has three distinct keys on Chatter, and the enabled query that reads the price ranking
 *      has three distinct keys on Price.
 *   3  KEEP: the round-29 and round-30 checks over the same files still exit 0 -- collage/collage.cjs, collage/tone.cjs,
 *      leadprice/pricemovers.cjs, leadprice/leadface.cjs (AMENDMENT 1: no month cursor), universe/universe.cjs,
 *      universe/resolutionwords.cjs, repairs/chrome.cjs.
 *   4  PLANTED: the URL predicate rejects a missing days, days sent on the default call, a dropped limit and a doubled days, and
 *      accepts the reference URLs; the key predicate rejects one key reused across windows and accepts three.
 * Blind spots: a URL built outside these two functions is not seen; arm 2 reads keys, not react-query's cache.
 * Prints one line per arm and "EACH WINDOW IS ITS OWN READ: <k> of 4 arms"; exit 0 only at 4 of 4.
 */
const path = require('path');
const { spawnSync } = require('child_process');

const P = require('./_presets.cjs');
const { L } = P;
const DROOT = path.join(__dirname, '..', '..', '..');
const first = (e) => String(e && e.message ? e.message : e).split('\n')[0];

// ---------------- the route, with apiRequest recorded ----------------
const URLS = [];
L.stubSource('@/api/api-client', { apiRequest: (url) => { URLS.push(String(url)); return Promise.resolve({}); } });
L.stubSource('src/api/api-client', { apiRequest: (url) => { URLS.push(String(url)); return Promise.resolve({}); } });
L.stubSource('src/api/api-client.ts', { apiRequest: (url) => { URLS.push(String(url)); return Promise.resolve({}); } });
const BASE = '/api/scoped/amgt/lead-panel';
const CHAT_PATH = `${BASE}/timeseries/collected/chatter`;
const PRICE_PATH = `${BASE}/rankings/trending/price`;

/** One URL against its want: `exact` a string, or `{ path, params }` with exactly those query parameters. */
function urlFaults(got, want) {
  if (typeof want === 'string') return got === want ? [] : [`"${got}" (want "${want}")`];
  const [p, q = ''] = String(got).split('?');
  const f = [];
  if (p !== want.path) f.push(`path "${p}" (want "${want.path}")`);
  const params = [...new URLSearchParams(q).entries()];
  const keys = params.map(([k]) => k);
  if (new Set(keys).size !== keys.length) f.push(`a doubled parameter in "${got}"`);
  const have = Object.fromEntries(params);
  const wantKeys = Object.keys(want.params).sort().join(',');
  if (Object.keys(have).sort().join(',') !== wantKeys) f.push(`parameters ${keys.join(',') || 'none'} (want ${wantKeys})`);
  for (const [k, v] of Object.entries(want.params)) if (have[k] !== undefined && have[k] !== v) f.push(`${k}=${have[k]} (want ${v})`);
  return f;
}
const CASES = [
  ['getCollectedChatter()', (m) => m.getCollectedChatter(), CHAT_PATH],
  ['getCollectedChatter(90)', (m) => m.getCollectedChatter(90), `${CHAT_PATH}?days=90`],
  ["getLeadPanelRankings('TRENDING','PRICE')", (m) => m.getLeadPanelRankings('TRENDING', 'PRICE'), PRICE_PATH],
  ["getLeadPanelRankings('TRENDING','PRICE',500)", (m) => m.getLeadPanelRankings('TRENDING', 'PRICE', 500), `${PRICE_PATH}?limit=500`],
  ["getLeadPanelRankings('TRENDING','PRICE',500,365)", (m) => m.getLeadPanelRankings('TRENDING', 'PRICE', 500, 365), { path: PRICE_PATH, params: { limit: '500', days: '365' } }],
  ["getLeadPanelRankings('TRENDING','PRICE',undefined,90)", (m) => m.getLeadPanelRankings('TRENDING', 'PRICE', undefined, 90), { path: PRICE_PATH, params: { days: '90' } }],
];

/** The distinct keys of the enabled queries that made a read of `fn` (and, for rankings, subject PRICE), one render per window. */
function keysPerWindow(renders, fn) {
  return renders.map((r) => {
    if (!r) return null;
    const q = r.queries.filter((x) => x.enabled && x.calls.some((c) => c.fn === fn && (fn !== 'getLeadPanelRankings' || String(c.args[1]).toUpperCase() === 'PRICE')));
    return q.length ? q.map((x) => x.key).join(' + ') : null;
  });
}
function keyFaults(keys, label) {
  const f = [];
  if (keys.some((k) => k === null)) f.push(`${label}: ${keys.filter((k) => k === null).length} window(s) with no ${label} query`);
  else if (new Set(keys).size !== keys.length) f.push(`${label}: ${new Set(keys).size} distinct key(s) across 3 windows (${keys[0].slice(0, 60)})`);
  return f;
}

const arms = [];
// Arm 1 -- the route.
{
  const f = [];
  let m = null;
  try { m = L.source('src/api/endpoints/amgt-lead-panel.ts'); } catch (e) { f.push('LOAD: ' + first(e)); }
  if (m) for (const [name, call, want] of CASES) {
    URLS.length = 0;
    try { const r = call(m); if (r && typeof r.catch === 'function') r.catch(() => {}); } catch (e) { f.push(`${name}: THREW ${first(e)}`); continue; }
    if (URLS.length !== 1) { f.push(`${name}: ${URLS.length} request(s)`); continue; }
    f.push(...urlFaults(URLS[0], want).map((x) => `${name}: ${x}`));
  }
  arms.push(['THE ROUTE: days rides the query string on both reads; with days omitted each URL is unchanged', f.length === 0,
    f.length ? f.slice(0, 5).join(' | ') : `${CASES.length} of ${CASES.length} URLs as wanted`]);
}
// Arm 2 -- three cache entries.
{
  const f = [];
  const got = {};
  for (const subject of ['CHATTER', 'PRICE']) {
    got[subject] = P.WINDOWS.map((d) => {
      try { const r = P.renderAt(subject, d); if (r.stop) f.push(`${subject} ${d}: ${r.stop}`); return r.at; } catch (e) { f.push(`${subject} ${d}: RENDER ${first(e)}`); return null; }
    });
  }
  f.push(...keyFaults(keysPerWindow(got.CHATTER, 'getCollectedChatter'), 'collected-chatter'));
  f.push(...keyFaults(keysPerWindow(got.PRICE, 'getLeadPanelRankings'), 'price ranking'));
  arms.push(['THREE CACHE ENTRIES: 30, 90 and 365 days are three query keys on each face', f.length === 0,
    f.length ? [...new Set(f)].slice(0, 5).join(' | ') : 'collected chatter 3 keys, price ranking 3 keys']);
}
// Arm 3 -- keep.
{
  const f = [];
  const KEEP = ['round29/checks/collage/collage.cjs', 'round29/checks/collage/tone.cjs', 'round29/checks/leadprice/pricemovers.cjs',
    'round29/checks/leadprice/leadface.cjs', 'round30/checks/universe/universe.cjs', 'round30/checks/universe/resolutionwords.cjs',
    'round30/checks/repairs/chrome.cjs'];
  for (const rel of KEEP) {
    const r = spawnSync(process.execPath, [path.join(DROOT, rel)], { cwd: process.cwd(), encoding: 'utf8', timeout: 600000 });
    const last = ((r.stdout || '') + (r.stderr || '')).trim().split('\n').pop() || '';
    if (r.status !== 0) f.push(`${rel} rc=${r.status} ("${last.slice(0, 90)}")`);
  }
  arms.push(['KEEP: the round-29/30 checks over the same files exit 0 (leadface.cjs as amended: no month cursor)', f.length === 0,
    f.length ? f.join(' | ') : `${KEEP.length} of ${KEEP.length} exit 0`]);
}
// Arm 4 -- planted.
{
  const f = [];
  const goods = [
    [CHAT_PATH, CHAT_PATH], [`${CHAT_PATH}?days=90`, `${CHAT_PATH}?days=90`],
    [`${PRICE_PATH}?days=365&limit=500`, { path: PRICE_PATH, params: { limit: '500', days: '365' } }],
    [`${PRICE_PATH}?days=90`, { path: PRICE_PATH, params: { days: '90' } }],
  ];
  for (const [g, w] of goods) if (urlFaults(g, w).length) f.push(`good "${g}" rejected`);
  for (const [n, g, w] of [
    ['a missing days', CHAT_PATH, `${CHAT_PATH}?days=90`],
    ['days on the default call', `${CHAT_PATH}?days=30`, CHAT_PATH],
    ['a dropped limit', `${PRICE_PATH}?days=365`, { path: PRICE_PATH, params: { limit: '500', days: '365' } }],
    ['a doubled days', `${PRICE_PATH}?days=90&days=90`, { path: PRICE_PATH, params: { days: '90' } }],
  ]) if (urlFaults(g, w).length === 0) f.push(`url: ${n} accepted`);
  if (keyFaults(['["a",30]', '["a",30]', '["a",30]'], 'k').length === 0) f.push('key: one key reused across windows accepted');
  if (keyFaults(['["a",30]', '["a",90]', '["a",365]'], 'k').length) f.push('key: three distinct keys rejected');
  if (keyFaults(['["a",30]', null, '["a",365]'], 'k').length === 0) f.push('key: a window with no query accepted');
  arms.push(['PLANTED: the URL predicate rejects 4 planted URLs and accepts 4 references; the key predicate rejects reuse and a gap', f.length === 0,
    f.length ? f.join(' | ') : '4 + 2 rejected, 4 + 1 good accepted']);
}

let pass = 0;
for (const [n, ok, d] of arms) { if (ok) pass += 1; console.log(`${ok ? 'ARM PASS' : 'ARM FAIL'} ${n} :: ${d}`); }
console.log(`EACH WINDOW IS ITS OWN READ: ${pass} of 4 arms`);
process.exit(pass === 4 ? 0 : 1);
