/**
 * render.cjs -- DSGN_AMGTV1 round 28, AV-zf-1 (issuer 2.0.0_SA_COO~D): THE RENDER CHECK READS FWD-15 AND FWD-16 ON THE RULED DESIGNS.
 *
 * Usage: node <this file> <worktree root>        (its portal/ is the checkout under test)
 * CTO msg 28537 + COMPLETION_GRADES.round26 @6fe6735934: FWD-20 NOT_EVALUATED on two stale instrument clauses (CVO~Z ADJUDICATION_v27
 * section 2): fwd15 counts the consensus `th` into the column count, so a REFUSED row that spans the table reads 14 against 15; fwd16
 * demands the served reason verbatim on the face, which the r22/r23 rulings replaced with reader words on the face and the served
 * reason on `data-absent-column-reason`. FWD-15 is NOT_EVALUATED because the contract fixture holds no ABSENT row.
 * What it does: a vite build of <root>/portal into a temp dir, then `scripts/ui-contract-check.mjs --dist <it> --states model,peers`,
 * then reads grades.json.
 * Arms:
 *   1  FWD-15: fwd15_modelTable grades PASS on the model state, with BOTH halves exercised: >= 1 REFUSED row, exactly 1 ABSENT
 *      footnote naming >= 1 row.
 *   2  FWD-16: fwd16_absentColumns grades PASS on the peers state.
 *   3  PLANTED: the fwd16 predicate in ui-contract-check.mjs (`const noReason = t.items.filter(i => ...)`, one expression) accepts
 *      a listed column carrying its served reason on the attribute and reader words on the face, and rejects one with no served
 *      reason and one whose face carries only the column's own name.
 * Prints one line per arm and "THE RENDER CHECK READS FWD-15 AND FWD-16 ON THE RULED DESIGNS: <k> of 3 arms"; exit 0 only at 3 of 3.
 */
const fs = require('fs');
const os = require('os');
const path = require('path');
const { spawnSync } = require('child_process');

const root = path.resolve(process.argv[2] || process.cwd());
const portal = path.join(root, 'portal');
const stamp = `${Date.now()}`;
const dist = path.join(os.tmpdir(), `dsgn-r28-dist-${stamp}`);
const out = path.join(os.tmpdir(), `dsgn-r28-render-${stamp}`);
const arms = [];

function find(obj, key, trail = []) {
  if (!obj || typeof obj !== 'object') return [];
  const hits = [];
  for (const [k, v] of Object.entries(obj)) {
    if (k === key) hits.push({ trail: [...trail, k].join('.'), v });
    hits.push(...find(v, key, [...trail, k]));
  }
  return hits;
}

let grades = null;
let runNote = '';
const b = spawnSync(process.execPath, [path.join('node_modules', 'vite', 'bin', 'vite.js'), 'build', '--configLoader', 'runner', '--outDir', dist, '--emptyOutDir'],
  { cwd: portal, encoding: 'utf8', timeout: 900000, maxBuffer: 64 * 1024 * 1024 });
if (b.status !== 0 || !fs.existsSync(path.join(dist, 'index.html'))) runNote = `BUILD rc=${b.status}: ${String(b.stderr || b.stdout).split('\n').filter(Boolean).slice(-2).join(' / ')}`;
else {
  const r = spawnSync(process.execPath, ['scripts/ui-contract-check.mjs', '--dist', dist, '--out', out, '--states', 'model,peers'],
    { cwd: portal, encoding: 'utf8', timeout: 900000, maxBuffer: 64 * 1024 * 1024 });
  const gp = path.join(out, 'grades.json');
  if (!fs.existsSync(gp)) runNote = `RUN rc=${r.status}: no grades.json (${String(r.stderr || r.stdout).split('\n').filter(Boolean).slice(-2).join(' / ')})`;
  else grades = JSON.parse(fs.readFileSync(gp, 'utf8'));
}

// Arm 1 -- FWD-15 graded PASS with both halves exercised.
{
  const f = [];
  if (!grades) f.push(runNote);
  else {
    const hits = find(grades, 'fwd15_modelTable').filter((h) => h.v && h.v.grade);
    const graded = hits.filter((h) => h.v.grade !== 'N/A');
    if (graded.length === 0) f.push(`fwd15_modelTable not graded on any state (${hits.length} entries)`);
    for (const h of graded) {
      const v = h.v.value || {};
      if (h.v.grade !== 'PASS') f.push(`${h.trail} ${h.v.grade}: ${JSON.stringify(h.v.fails || h.v.value).slice(0, 200)}`);
      if (!(v.refusedRows >= 1)) f.push(`${h.trail} refusedRows ${v.refusedRows} (the refusal half not exercised)`);
      if (v.footnotes !== 1 || !(v.absentNamed >= 1)) f.push(`${h.trail} footnotes ${v.footnotes}, absentNamed ${v.absentNamed} (the ABSENT half not exercised)`);
    }
  }
  arms.push(['FWD-15: fwd15 PASS with a REFUSED row and one ABSENT footnote both read', f.length === 0, f.length ? f.slice(0, 4).join(' | ') : 'PASS, both halves read']);
}
// Arm 2 -- FWD-16 graded PASS.
{
  const f = [];
  if (!grades) f.push(runNote);
  else {
    const graded = find(grades, 'fwd16_absentColumns').filter((h) => h.v && h.v.grade && h.v.grade !== 'N/A');
    if (graded.length === 0) f.push('fwd16_absentColumns not graded on any state');
    for (const h of graded) if (h.v.grade !== 'PASS') f.push(`${h.trail} ${h.v.grade}: ${JSON.stringify(h.v.fails || h.v.value).slice(0, 200)}`);
  }
  arms.push(['FWD-16: fwd16 PASS on the peers state', f.length === 0, f.length ? f.slice(0, 4).join(' | ') : 'PASS']);
}
// Arm 3 -- the fwd16 predicate, planted.
{
  const f = [];
  const src = fs.readFileSync(path.join(portal, 'scripts', 'ui-contract-check.mjs'), 'utf8');
  const m = /const noReason = t\.items\.filter\((i\s*=>[^\n]+)\)\s*\n/.exec(src);
  if (!m) f.push('no one-expression `const noReason = t.items.filter(i => ...)` in ui-contract-check.mjs');
  else {
    let pred = null;
    try { pred = eval(`(${m[1]})`); } catch (e) { f.push('the predicate does not evaluate: ' + e.message); }
    if (pred) {
      const good = { name: 'Shares', reason: 'no share-count code', text: 'Shares -- the pack carries no share count for this name' };
      const unserved = { name: 'Shares', reason: '', text: 'Shares -- the pack carries no share count for this name' };
      const bare = { name: 'Shares', reason: 'no share-count code', text: 'Shares' };
      if (pred(good)) f.push('a column with its served reason on the attribute and reader words on the face is flagged');
      if (!pred(unserved)) f.push('a column with no served reason is accepted');
      if (!pred(bare)) f.push("a column whose face reads only its own name is accepted");
    }
  }
  arms.push(['PLANTED: the fwd16 predicate accepts reader words + served reason, rejects no reason and a bare name', f.length === 0, f.length ? f.join(' | ') : '1 accepted, 2 rejected']);
}

let pass = 0;
for (const [n, ok, d] of arms) { if (ok) pass += 1; console.log(`${ok ? 'ARM PASS' : 'ARM FAIL'} ${n} :: ${d}`); }
console.log(`THE RENDER CHECK READS FWD-15 AND FWD-16 ON THE RULED DESIGNS: ${pass} of 3 arms`);
process.exit(pass === 3 ? 0 : 1);
