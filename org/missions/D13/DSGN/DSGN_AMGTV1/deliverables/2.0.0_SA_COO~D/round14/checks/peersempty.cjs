/**
 * peersempty.cjs -- DSGN_AMGTV1 round 14, AV-k-3: PEERS HAS A DESIGNED EMPTY STATE (round-13 analysis ruling 4; FWD-19; s.4 row 3).
 *
 * Usage (repo root): node <this file>
 * Ruling 4: "Peers gets a designed EMPTY state." Criterion (s.4 row 3): "fwd19 `peers/empty` PASS on the render run, with the branch
 * reachable from a fixture." On the base the render run's run.fwd19_designedStates reads FAIL with missing
 * ["peers/empty (no designed branch is reachable)"]: PeersTab.tsx's only PanelEmpty guards `!securityKey`, and a served absent peer
 * set renders a bare paragraph; the instrument's --states-sweep has no empty patch for peers (`empty: null`).
 * Inputs: the portal checkout under <cwd>/portal (built here); the round-14 fixtures (peerSet.WMB_US_Equity.json = the served R-1
 * absent arm, read ABSENT; peers.BA_US_Equity.json = BA's served peer set; peerSet.VLO_US_Equity.json); the base page build
 * C:/tmp/dsgn-r13-dist/final (page bytes of portal 118cd005) and the issuer's blank page round14/checks/dists/blank.
 * Arms:
 *   1  the render run: vite-build <cwd>/portal, run `ui-contract-check.mjs --dist <build> --out <tmp> --states-sweep` from
 *      <cwd>/portal; grades.json run.fwd19_designedStates reads PASS, perPanel.peers.empty >= 1, no `peers/` entry in missing,
 *      peers-empty.png has bytes, and the sweep's patched fixture for peers is the SERVED absent shape (every key a key of the
 *      served absent object or `identity`; basis absent, read ABSENT, zero members) -- reachable from a served shape, not a flag
 *   2  the static face: PeersTab on the served absent peer set renders a PanelEmpty whose message is one sentence, with no
 *      "no data", no raw code, no contract code (R-1) and no status token (ABSENT / READ_FAILED) in visible text, and no CSC table;
 *      on BA's served peers it still renders the CSC table with members and no PanelEmpty; a READ_FAILED read is NOT rendered as
 *      the empty state (a failed read is not an empty set)
 *   3  the negative: the SAME instrument (<cwd>/portal/scripts) on the base page build, `--states peers --states-sweep`, reads
 *      fwd19 FAIL naming peers/empty; on the blank page it does not read PASS
 * Writes only under os.tmpdir() (the build and the run outputs). No network, no AWS.
 * Wall time measured on site Z (2026-09-30): base 866 s, green 928 s (build 13-22 s, full run ~585 s, peers-only runs 114-190 s);
 * worker timeout 1800 s.
 * Prints one line per arm and "PEERS HAS A DESIGNED EMPTY STATE: <k> of 3 arms"; exit 0 only at 3 of 3.
 */
const fs = require('fs');
const os = require('os');
const path = require('path');
const { spawnSync } = require('child_process');

const ROOT = process.cwd();
const PORTAL = path.join(ROOT, 'portal');
const CHECKS = __dirname;
const BASE_DIST = 'C:/tmp/dsgn-r13-dist/final';
const BLANK_DIST = path.join(CHECKS, 'dists/blank');
const TMP = fs.mkdtempSync(path.join(os.tmpdir(), 'r14-peersempty-'));
const secs = (t0) => Math.round((Date.now() - t0) / 1000);

function contract(dist, out, extra) {
  const t0 = Date.now();
  const r = spawnSync(process.execPath, ['scripts/ui-contract-check.mjs', '--dist', dist, '--out', out, '--states-sweep', ...(extra || [])], { cwd: PORTAL, encoding: 'utf8', timeout: 900000 });
  let grades = null;
  try { grades = JSON.parse(fs.readFileSync(path.join(out, 'grades.json'), 'utf8')); } catch (e) { grades = null; }
  const fwd19 = grades && grades.run ? grades.run.fwd19_designedStates || null : null;
  return { rc: r.status, secs: secs(t0), grades, fwd19, out };
}

// ---------------- arm 1: build <cwd>/portal and run the render check ----------------
const f1 = [];
let a1d = '';
const t0 = Date.now();
const DIST = path.join(TMP, 'dist');
const build = spawnSync(process.execPath, [path.join(PORTAL, 'node_modules/vite/bin/vite.js'), 'build', '--configLoader', 'runner', '--outDir', DIST, '--emptyOutDir'], { cwd: PORTAL, encoding: 'utf8', timeout: 480000 });
const buildSecs = secs(t0);
let main = null;
if (build.status !== 0 || !fs.existsSync(path.join(DIST, 'index.html'))) {
  f1.push(`the page build failed (rc=${build.status}, ${buildSecs}s): ${String(build.stderr || build.stdout || '').trim().split('\n').slice(-1)[0]}`);
} else {
  main = contract(DIST, path.join(TMP, 'run'));
  const v = main.fwd19 ? main.fwd19.value || {} : {};
  if (!main.fwd19) f1.push(`no run.fwd19_designedStates in grades.json (rc=${main.rc})`);
  else {
    if (main.fwd19.grade !== 'PASS') f1.push(`fwd19 ${main.fwd19.grade}, missing ${JSON.stringify(v.missing || v.reason)}`);
    const pe = ((v.perPanel || {}).peers || {}).empty;
    if (!(Number(pe) >= 1)) f1.push(`perPanel.peers.empty = ${pe}`);
    const pm = (v.missing || []).filter((m) => /^peers\//.test(m));
    if (pm.length) f1.push(`missing names ${pm.join('; ')}`);
  }
  const png = path.join(main.out, 'peers-empty.png');
  const pngBytes = fs.existsSync(png) ? fs.statSync(png).size : 0;
  if (!(pngBytes > 0)) f1.push('no peers-empty.png with bytes');
  // reachable from a SERVED shape: the patched fixture's peers entry is the served absent arm, keyed to BA.
  let served = null;
  let patched = null;
  try { served = JSON.parse(fs.readFileSync(path.join(ROOT, 'org/missions/D13/DSGN/DSGN_AMGTV1/deliverables/2.0.0_SA_COO~D/round14/fixtures/peerSet.WMB_US_Equity.json'), 'utf8')); } catch (e) { served = null; }
  try {
    const fx = JSON.parse(fs.readFileSync(path.join(main.out, '_fixtures/peers-empty.json'), 'utf8'));
    patched = fx[Object.keys(fx).find((k) => /\/security\/BA_US_Equity\/peers$/.test(k))];
  } catch (e) { patched = null; }
  if (!served) f1.push('the served absent fixture peerSet.WMB_US_Equity.json is missing');
  else if (!patched) f1.push('the sweep wrote no patched peers fixture (_fixtures/peers-empty.json with the BA peers key)');
  else {
    const allowed = new Set([...Object.keys(served), 'identity']);
    const extra = Object.keys(patched).filter((k) => !allowed.has(k));
    if (extra.length) f1.push(`the patched peers fixture carries keys the served absent shape does not: ${extra.join(', ')}`);
    const pr = patched.peer_read || {};
    if (patched.basis !== served.basis || pr.status !== (served.peer_read || {}).status || !Array.isArray(patched.members) || patched.members.length !== 0) {
      f1.push(`the patched peers fixture is not the served absent arm (basis ${patched.basis}, read ${pr.status}, members ${(patched.members || []).length})`);
    }
  }
  a1d = `build ${buildSecs}s, run ${main.secs}s rc=${main.rc}; fwd19 ${main.fwd19 ? main.fwd19.grade : 'none'} perPanel.peers ${JSON.stringify(((main.fwd19 || {}).value || {}).perPanel ? main.fwd19.value.perPanel.peers : null)}; peers-empty.png ${pngBytes} bytes; patched fixture basis ${patched ? patched.basis : 'none'} read ${patched && patched.peer_read ? patched.peer_read.status : 'none'}`;
}
const a1 = f1.length === 0;
if (!a1) a1d = `${f1.length} failing; first: ${f1[0]}${a1d ? ' || ' + a1d : ''}`;

// ---------------- arm 2: the static face ----------------
const L = require('./_load.cjs');
const unwrap = (x) => (x && x.payload && (x._capture_note || x._capture) ? x.payload : x);
let current = null;
L.hookState.impl = { usePeerSet: () => current };
const f2 = [];
let a2d = '';
try {
  const { PeersTab } = L.source('src/pages/SecurityAnalysis/tabs/PeersTab.tsx');
  const absent = unwrap(L.fixture('peerSet.WMB_US_Equity.json'));
  const ba = unwrap(L.fixture('peers.BA_US_Equity.json'));
  const renderOn = (obj, key) => { current = obj; return L.render(PeersTab, { securityKey: key }); };

  const eHtml = renderOn(absent, 'WMB_US_Equity');
  const eText = L.textOf(L.innerOf(eHtml, 'data-tab-panel', 'peers') || '');
  const empties = (eHtml.match(/data-stub="PanelEmpty"/g) || []).length;
  const msg = (/data-stub-text="message">([^<]*)</.exec(eHtml) || [])[1] || '';
  const raw = L.rawCensus(eHtml);
  if (!eText) f2.push('absent: the Peers panel did not render');
  if (empties !== 1) f2.push(`absent: ${empties} PanelEmpty (want 1)`);
  if (!/^[A-Z][^.]*\.$/.test(msg.trim()) || msg.trim().split(/\s+/).length < 4) f2.push(`absent: the empty message is not one sentence: "${msg}"`);
  if (/no data/i.test(eText)) f2.push('absent: visible text says "no data"');
  if (raw.total) f2.push(`absent: raw code in visible text ${JSON.stringify(raw)}`);
  const codes = eText.match(/\b[A-Z]{1,2}-\d+\b|\b(?:ABSENT|READ_FAILED|SERVED)\b/g) || [];
  if (codes.length) f2.push(`absent: contract code or status token in visible text: ${codes.join(', ')}`);
  if (eHtml.includes('data-csc-table')) f2.push('absent: a CSC table rendered');

  const tHtml = renderOn(ba, 'BA_US_Equity');
  const members = (tHtml.match(/data-csc-row="member"/g) || []).length;
  if (!tHtml.includes('data-csc-table')) f2.push('BA: no CSC table');
  if (members < 1) f2.push('BA: no member rows');
  if (tHtml.includes('data-stub="PanelEmpty"')) f2.push('BA: a PanelEmpty rendered on a served peer set');

  const failed = { ...absent, peer_read: { ...(absent.peer_read || {}), status: 'READ_FAILED', read_completed: false } };
  const fHtml = renderOn(failed, 'WMB_US_Equity');
  if (fHtml.includes('data-stub="PanelEmpty"')) f2.push('READ_FAILED: a failed read renders as the empty state');
  if (fHtml === eHtml) f2.push('READ_FAILED: renders the same bytes as ABSENT');

  a2d = `absent: ${empties} PanelEmpty, message "${msg}", raw ${raw.total}, codes ${codes.length}; BA: table ${tHtml.includes('data-csc-table') ? 1 : 0}, ${members} member rows; READ_FAILED as empty ${fHtml.includes('data-stub="PanelEmpty"') ? 1 : 0}`;
} catch (e) {
  f2.push('render threw: ' + String(e.message).split('\n')[0]);
}
const a2 = f2.length === 0;
if (!a2) a2d = `${f2.length} failing; first: ${f2[0]} || ${a2d}`;

// ---------------- arm 3: the negative ----------------
const f3 = [];
let a3d = '';
if (!fs.existsSync(path.join(BASE_DIST, 'index.html'))) f3.push(`INPUT MISSING: the base page build at ${BASE_DIST}`);
if (!fs.existsSync(path.join(BLANK_DIST, 'index.html'))) f3.push(`INPUT MISSING: the blank page at ${BLANK_DIST}`);
if (!f3.length) {
  const base = contract(BASE_DIST, path.join(TMP, 'neg-base'), ['--states', 'peers'])
  const blank = contract(BLANK_DIST, path.join(TMP, 'neg-blank'), ['--states', 'peers'])
  const bm = base.fwd19 ? (base.fwd19.value || {}).missing || [] : [];
  if (!base.fwd19) f3.push(`base page: no fwd19 in grades.json (rc=${base.rc})`);
  else if (base.fwd19.grade !== 'FAIL' || !bm.some((m) => /^peers\/empty/.test(m))) f3.push(`base page: fwd19 ${base.fwd19.grade}, missing ${JSON.stringify(bm)} -- the page without the branch is not caught`);
  if (blank.fwd19 && blank.fwd19.grade === 'PASS') f3.push('blank page: fwd19 reads PASS');
  if (blank.rc === 0) f3.push('blank page: the run exited 0');
  a3d = `base page (peers only, ${base.secs}s): fwd19 ${base.fwd19 ? base.fwd19.grade : 'none'} missing ${JSON.stringify(bm)}; blank page (${blank.secs}s): fwd19 ${blank.fwd19 ? blank.fwd19.grade : 'none'} rc=${blank.rc}`;
}
const a3 = f3.length === 0;
if (!a3) a3d = `${f3.length} failing; first: ${f3[0]} || ${a3d}`;

console.log(`RUNS: out ${TMP}; total ${secs(t0)}s`);
const arms = [
  ['the render run: fwd19 peers/empty PASS from the served absent shape', a1, a1d],
  ['the static face: a designed empty sentence on the absent set, the table on BA, READ_FAILED not empty', a2, a2d],
  ['the negative: the base page reads fwd19 FAIL on peers/empty; the blank page does not pass', a3, a3d],
];
let pass = 0;
for (const [name, ok, detail] of arms) { if (ok) pass += 1; console.log(`${ok ? 'ARM PASS' : 'ARM FAIL'} ${name} :: ${detail}`); }
console.log(`PEERS HAS A DESIGNED EMPTY STATE: ${pass} of ${arms.length} arms`);
process.exit(pass === arms.length ? 0 : 1);
