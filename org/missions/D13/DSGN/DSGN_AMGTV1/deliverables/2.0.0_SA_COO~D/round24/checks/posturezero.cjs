/**
 * posturezero.cjs -- DSGN_AMGTV1 round 24, AV-zc-3 (issuer 2.0.0_SA_COO~D): THE RE-ANCHORED POSTURE CHECK IS NAMED FOR WHAT IT GRADES
 * AND ITS ZERO-RESOLVED PATH IS PLANTED.
 *
 * Usage (repo root): node <this file>        (portal/ under the cwd is the checkout under test)
 * CTO round-23 analysis @876dfcadb8 ruling 3 (ADJUDICATION_v21 conditions on AV-zb-4's re-anchor): the check
 * `<KEY>:claims_with_resolved_cite_equal` is renamed to what it now grades (the page's STATED resolved count per claim), and one
 * plant exercises the 0-resolved path: "the plant reads red on the unfixed path and green on the fixed one".
 * THE CONTRACT in portal/src/pages/SecurityAnalysis/__harness__/posture.harness.cjs:
 *   - no CHECK named `*:claims_with_resolved_cite_equal` remains; the clean run prints the same number of CHECKs as before (32),
 *     so the check is renamed, not dropped;
 *   - POSTURE_HARNESS_PLANT=zero forces EVERY cite of one served claim to fail resolution (the 0-resolved path) before rendering
 *     and prints one "PLANT ACTIVE: ..." line; the fixed predicate credits it, so the run stays green (rc 0, CHECKS-OK);
 *   - POSTURE_HARNESS_LEGACY_PREDICATE=1 restores the pre-AV-zb-4 predicate (a claim counts only with >= 1 resolved cite); with the
 *     zero plant it reads RED (rc != 0, >= 1 CHECK off its expectation, no uncaught exception) -- the plant exercises the path;
 *   - POSTURE_HARNESS_PLANT=1 (round 23's blank-claims plant) still reads red (round23/checks/postureharness.cjs grades it).
 * Arms:
 *   1  CLEAN: rc 0, CHECKS-OK n of n with n = 32, and no CHECK named *:claims_with_resolved_cite_equal.
 *   2  ZERO PLANT, FIXED PREDICATE: PLANT=zero -> rc 0, CHECKS-OK, a "PLANT ACTIVE" line.
 *   3  ZERO PLANT, LEGACY PREDICATE: PLANT=zero + LEGACY_PREDICATE=1 -> rc != 0, >= 1 red CHECK, no crash.
 * Prints one line per arm and "THE ZERO-RESOLVED PATH IS NAMED AND PLANTED: <k> of 3 arms"; exit 0 only at 3 of 3.
 */
const path = require('path');
const { spawnSync } = require('child_process');

const PORTAL = path.join(process.cwd(), 'portal');
const H = path.join(PORTAL, 'src/pages/SecurityAnalysis/__harness__/posture.harness.cjs');
function run(env) {
  const e = { ...process.env };
  delete e.POSTURE_HARNESS_PLANT; delete e.POSTURE_HARNESS_LEGACY_PREDICATE;
  Object.assign(e, env);
  const r = spawnSync(process.execPath, [H], { cwd: PORTAL, env: e, encoding: 'utf8', maxBuffer: 1 << 26, timeout: 115000 });
  const out = (r.stdout || '') + (r.stderr || '');
  const checks = {};
  for (const m of out.matchAll(/^CHECK (\S+) (\S+) \(expected (\S+)\)/gm)) checks[m[1]] = { got: m[2], want: m[3] };
  const ok = /CHECKS-OK (\d+) of (\d+)/.exec(out);
  return { rc: r.status, out, checks, ok, crash: /\b(TypeError|ReferenceError|SyntaxError)\b/.test(out) };
}

const arms = [];
{
  const r = run({});
  const f = [];
  if (r.rc !== 0) f.push(`rc=${r.rc}`);
  if (r.crash) f.push('uncaught exception');
  if (!r.ok || r.ok[1] !== r.ok[2]) f.push(r.ok ? r.ok[0] : 'no CHECKS-OK');
  else if (Number(r.ok[1]) !== 32) f.push(`${r.ok[1]} checks (want 32: renamed, not dropped)`);
  const old = Object.keys(r.checks).filter((n) => /:claims_with_resolved_cite_equal$/.test(n));
  if (old.length) f.push(`old name still printed: ${old.join(', ')}`);
  arms.push(['CLEAN: green, 32 checks, the old name gone', f.length === 0, f.length === 0 ? r.ok[0] : f.join(' | ')]);
}
{
  const r = run({ POSTURE_HARNESS_PLANT: 'zero' });
  const f = [];
  if (r.rc !== 0) f.push(`rc=${r.rc}`);
  if (r.crash) f.push('uncaught exception');
  if (!/PLANT ACTIVE/.test(r.out)) f.push('no PLANT ACTIVE line');
  if (!r.ok || r.ok[1] !== r.ok[2]) f.push(r.ok ? r.ok[0] : 'no CHECKS-OK');
  arms.push(['ZERO PLANT, FIXED PREDICATE: green with the plant active', f.length === 0, f.length === 0 ? `${r.ok[0]} with the plant` : f.join(' | ')]);
}
{
  const r = run({ POSTURE_HARNESS_PLANT: 'zero', POSTURE_HARNESS_LEGACY_PREDICATE: '1' });
  const f = [];
  const red = Object.entries(r.checks).filter(([, c]) => c.got !== c.want).map(([n]) => n);
  if (r.rc === 0) f.push('rc=0 under the legacy predicate');
  if (r.crash) f.push('crashed instead of reading red');
  if (!red.length) f.push('no red CHECK under the legacy predicate');
  arms.push(['ZERO PLANT, LEGACY PREDICATE: red without a crash', f.length === 0, f.length === 0 ? `${red.length} red: ${red.slice(0, 2).join(', ')}` : f.join(' | ')]);
}

let pass = 0;
for (const [n, ok, d] of arms) { if (ok) pass += 1; console.log(`${ok ? 'ARM PASS' : 'ARM FAIL'} ${n} :: ${d}`); }
console.log(`THE ZERO-RESOLVED PATH IS NAMED AND PLANTED: ${pass} of 3 arms`);
process.exit(pass === 3 ? 0 : 1);
