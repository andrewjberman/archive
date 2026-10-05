/**
 * access40.cjs -- DSGN_AMGTV1 round 40 issuer CHECK (2.0.0_SA_COO~D): SECURITY ANALYSIS IS OPEN TO EVERY OPAL EMPLOYEE.
 *
 * Usage (from the directory whose portal/ is the checkout under test):
 *   cd "$(git rev-parse --show-toplevel)" && node "org/missions/D13/DSGN/DSGN_AMGTV1/deliverables/2.0.0_SA_COO~D/round40/checks/access/access40.cjs"
 *
 * Why: Andrew-direct 2026-10-05 ~15:0xZ (org/tier1_exec/2.0.0_SA_COO/deliverables/
 * ANDREW_DIRECT_20261005_150xZ_SECURITY_ANALYSIS_ALL_OPAL_EMPLOYEES_REQUIREINTERNAL_LEADPANEL_LOAD_TO_COO_Z.md):
 * "It should be visible for all Opal Employees", "should not require admin access to see", "requireInternal is the correct approac".
 * The page was gated Dev + admin (App.tsx nav entry requiresDev/requiresAdmin; both routes ProtectedRoute requireDev requireAdmin).
 * The house pattern for Opal-only pages is ProtectedRoute requireInternal (claims.firmId === 'opal-capital', ProtectedRoute.tsx)
 * on the route, the internal tier on the nav entry (requiresTier: 'internal'), and the deny-by-default firm allowlist
 * (src/lib/firmAccess.ts) for partner firms.
 *
 * Arms (each prints its evidence; exit 0 only on 4 of 4):
 *   1 THE NAV ENTRY: the '/security-analysis' item carries requiresTier: 'internal' and neither requiresDev nor requiresAdmin.
 *   2 THE ROUTES: '/security-analysis' and '/security-analysis/:securityKey' each sit behind ProtectedRoute requireInternal, with
 *     neither requireDev nor requireAdmin.
 *   3 KEEP: Investor Reporting's gate is unchanged (nav requiresAdmin + requiresTier 'internal' + requiresDev; route requireAdmin
 *     requireInternal requireDev), ProtectedRoute's requireInternal predicate is still firmId === 'opal-capital', and no partner
 *     firm's allowlist in firmAccess.ts names /security-analysis.
 *   4 PLANTED: the graders flag a Dev gate left on the nav, an admin gate left on a route, a missing internal gate, and accept the
 *     intended lines.
 * Static source read only (the gate is configuration in two files); no network, writes nothing.
 */
'use strict';
const fs = require('fs');
const path = require('path');

const root = process.cwd();
const P = (rel) => path.join(root, 'portal', rel);
function read(rel) {
  if (!fs.existsSync(P(rel))) { console.log('LOADER ERROR: no ' + rel + ' under ' + path.join(root, 'portal')); process.exit(3); }
  return fs.readFileSync(P(rel), 'utf8').replace(/\r\n/g, '\n');
}
const app = read('src/App.tsx');
const guard = read('src/components/ProtectedRoute.tsx');
const firm = read('src/lib/firmAccess.ts');

function navLines(src, p) { return src.split('\n').filter((l) => l.includes(`path: '${p}'`) && /label:/.test(l)); }
function routeLines(src, p) { return src.split('\n').filter((l) => new RegExp(`<Route\\s+path="${p.replace(/[/:]/g, (c) => '\\' + c)}"`).test(l)); }

function gradeNav(line) {
  const f = [];
  if (!/requiresTier:\s*'internal'/.test(line)) f.push("no requiresTier: 'internal'");
  if (/requiresDev:\s*true/.test(line)) f.push('requiresDev still set');
  if (/requiresAdmin:\s*true/.test(line)) f.push('requiresAdmin still set');
  return f;
}
function gradeRoute(line) {
  const f = [];
  const m = /<ProtectedRoute([^>]*)>/.exec(line);
  if (!m) return ['no ProtectedRoute on the route'];
  const props = m[1];
  if (!/\brequireInternal\b/.test(props)) f.push('no requireInternal');
  if (/\brequireDev\b/.test(props)) f.push('requireDev still set');
  if (/\brequireAdmin\b/.test(props)) f.push('requireAdmin still set');
  return f;
}

const arms = [];
// arm 1
{
  const lines = navLines(app, '/security-analysis');
  const f = [];
  if (lines.length !== 1) f.push(`${lines.length} nav entries for /security-analysis (1 wanted)`);
  for (const l of lines) f.push(...gradeNav(l).map((x) => `nav: ${x} :: ${l.trim()}`));
  arms.push(['THE NAV ENTRY: /security-analysis carries the internal tier and no Dev or admin gate', f.length === 0, f.length ? f.join(' | ') : lines[0].trim()]);
}
// arm 2
{
  const f = [];
  const shown = [];
  for (const p of ['/security-analysis', '/security-analysis/:securityKey']) {
    const lines = routeLines(app, p);
    if (lines.length !== 1) { f.push(`${lines.length} routes for ${p} (1 wanted)`); continue; }
    const g = gradeRoute(lines[0]);
    f.push(...g.map((x) => `${p}: ${x}`));
    shown.push(`${p}: ${(/<ProtectedRoute([^>]*)>/.exec(lines[0]) || [])[0]}`);
  }
  arms.push(['THE ROUTES: both Security Analysis routes sit behind ProtectedRoute requireInternal, no Dev or admin gate', f.length === 0, f.length ? f.join(' | ') : shown.join('; ')]);
}
// arm 3 KEEP
{
  const f = [];
  const irNav = navLines(app, '/investor-reporting');
  if (irNav.length !== 1 || !/requiresAdmin:\s*true/.test(irNav[0]) || !/requiresTier:\s*'internal'/.test(irNav[0]) || !/requiresDev:\s*true/.test(irNav[0])) f.push('Investor Reporting nav gate changed');
  const irRoute = routeLines(app, '/investor-reporting');
  if (irRoute.length !== 1 || !/requireAdmin/.test(irRoute[0]) || !/requireInternal/.test(irRoute[0]) || !/requireDev/.test(irRoute[0])) f.push('Investor Reporting route gate changed');
  if (!/requireInternal && claims\?\.firmId !== 'opal-capital'/.test(guard)) f.push("ProtectedRoute's requireInternal predicate is not firmId === 'opal-capital'");
  if (/['"]\/security-analysis['"]/.test(firm)) f.push('firmAccess.ts names /security-analysis (a partner firm could be allowlisted)');
  arms.push(['KEEP: Investor Reporting unchanged; requireInternal is firmId === opal-capital; no partner allowlist names /security-analysis', f.length === 0, f.length ? f.join(' | ') : 'IR nav + route unchanged; predicate holds; 0 allowlist mentions']);
}
// arm 4 PLANTED
{
  const f = [];
  const bad = [
    ["      { path: '/security-analysis', label: 'Security Analysis', icon: LayoutGrid, requiresTier: 'internal', requiresDev: true },", 'nav'],
    ["      { path: '/security-analysis', label: 'Security Analysis', icon: LayoutGrid },", 'nav'],
    ['<Route path="/security-analysis" element={<ProtectedRoute requireInternal requireAdmin><SecurityAnalysis /></ProtectedRoute>} />', 'route'],
    ['<Route path="/security-analysis" element={<ProtectedRoute><SecurityAnalysis /></ProtectedRoute>} />', 'route'],
  ];
  const good = [
    ["      { path: '/security-analysis', label: 'Security Analysis', icon: LayoutGrid, requiresTier: 'internal' },", 'nav'],
    ['<Route path="/security-analysis" element={<ProtectedRoute requireInternal><SecurityAnalysis /></ProtectedRoute>} />', 'route'],
  ];
  let rej = 0; let acc = 0;
  for (const [l, k] of bad) { if ((k === 'nav' ? gradeNav(l) : gradeRoute(l)).length) rej += 1; else f.push(`planted fault accepted: ${l.trim()}`); }
  for (const [l, k] of good) { if ((k === 'nav' ? gradeNav(l) : gradeRoute(l)).length === 0) acc += 1; else f.push(`good line refused: ${l.trim()}`); }
  arms.push(['PLANTED: the graders flag a Dev gate, an admin gate and a missing internal gate, and accept the intended lines', f.length === 0, f.length ? f.join(' | ') : `${rej} of ${bad.length} faults flagged; ${acc} of ${good.length} good lines accepted`]);
}

const TITLE = 'SECURITY ANALYSIS IS OPEN TO EVERY OPAL EMPLOYEE';
let pass = 0;
for (const [name, ok, ev] of arms) { if (ok) pass += 1; console.log(`ARM ${ok ? 'PASS' : 'FAIL'} ${name} :: ${ev}`); }
console.log(`${TITLE}: ${pass} of ${arms.length} arms`);
process.exit(pass === arms.length ? 0 : 1);
