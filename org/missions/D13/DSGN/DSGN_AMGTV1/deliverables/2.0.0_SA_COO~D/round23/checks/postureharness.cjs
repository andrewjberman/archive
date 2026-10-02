/**
 * postureharness.cjs -- DSGN_AMGTV1 round 23, AV-zb-4 (issuer 2.0.0_SA_COO~D): POSTURE.HARNESS RUNS GREEN AND GRADES SOMETHING.
 *
 * Usage (repo root): node <this file>        (portal/ under the cwd is the checkout under test)
 * CTO round-22 analysis @eee9380be7 ruling 6 / section 3 row 4 (row DSGN_AMGTV1-Z-W69-S1): `posture.harness.cjs` throws
 * `useCollectedChatter is not a function` (a stale hook stub) and grades nothing. Repaired, it runs rc 0 with its checks green, and
 * a planted posture fault reads red. The plant is the harness's own knob: with POSTURE_HARNESS_PLANT=1 in the environment the harness
 * corrupts ONE posture input it grades (for example blanks every served claim or flips a verdict) and must then print at least one
 * CHECK whose value differs from its expectation, and exit non-zero -- WITHOUT an uncaught exception.
 * The harness reads the two O-1 posture objects with its own read-only S3 fetch (rl-7) into <workspace>/.scratch/ (Opal infra).
 * Harness line format: "CHECK <name> <value> (expected <value>)", then "CHECKS-OK <n> of <n>" on green.
 * Arms:
 *   1  CLEAN RUN: `node posture.harness.cjs` exits 0 and prints "CHECKS-OK n of n" with n >= 1, no uncaught exception.
 *   2  PLANTED RUN: with POSTURE_HARNESS_PLANT=1 it exits non-zero, prints >= 1 CHECK whose value differs from its expectation,
 *      and no "TypeError" / "ReferenceError" / "SyntaxError" (a crash is not a red check).
 *   3  SAME DENOMINATOR: the planted run prints the same set of CHECK names as the clean run.
 * Prints one line per arm and "POSTURE.HARNESS RUNS GREEN AND GRADES SOMETHING: <k> of 3 arms"; exit 0 only at 3 of 3.
 */
const path = require('path');
const { spawnSync } = require('child_process');

const PORTAL = path.join(process.cwd(), 'portal');
const H = path.join(PORTAL, 'src/pages/SecurityAnalysis/__harness__/posture.harness.cjs');
function run(plant) {
  const env = { ...process.env };
  if (plant) env.POSTURE_HARNESS_PLANT = '1'; else delete env.POSTURE_HARNESS_PLANT;
  const r = spawnSync(process.execPath, [H], { cwd: PORTAL, env, encoding: 'utf8', maxBuffer: 1 << 26, timeout: 115000 });
  const out = (r.stdout || '') + (r.stderr || '');
  const checks = {};
  for (const m of out.matchAll(/^CHECK (\S+) (\S+) \(expected (\S+)\)/gm)) checks[m[1]] = { got: m[2], want: m[3] };
  return { rc: r.status, out, checks, crash: /\b(TypeError|ReferenceError|SyntaxError)\b/.test(out) };
}

const clean = run(false);
const planted = run(true);
const arms = [];
{
  const ok = /CHECKS-OK (\d+) of (\d+)/.exec(clean.out);
  const f = [];
  if (clean.rc !== 0) f.push(`rc=${clean.rc}`);
  if (clean.crash) f.push('uncaught exception: ' + (clean.out.match(/(TypeError|ReferenceError|SyntaxError)[^\n]*/) || [''])[0].slice(0, 120));
  if (!ok || ok[1] !== ok[2] || Number(ok[1]) < 1) f.push(ok ? ok[0] : 'no CHECKS-OK line');
  arms.push(['CLEAN RUN: rc 0, CHECKS-OK n of n, no uncaught exception', f.length === 0, f.length === 0 ? ok[0] : f.join(' | ')]);
}
{
  const f = [];
  const red = Object.entries(planted.checks).filter(([, c]) => c.got !== c.want).map(([n]) => n);
  if (planted.rc === 0) f.push('rc=0 with the plant');
  if (planted.crash) f.push('the planted run crashed instead of reading red');
  if (red.length === 0) f.push('no CHECK reads red with the plant');
  arms.push(['PLANTED RUN: POSTURE_HARNESS_PLANT=1 reads red without a crash', f.length === 0,
    f.length === 0 ? `${red.length} check(s) red: ${red.slice(0, 3).join(', ')}` : f.join(' | ')]);
}
{
  const a = Object.keys(clean.checks).sort().join(',');
  const b = Object.keys(planted.checks).sort().join(',');
  const n = Object.keys(clean.checks).length;
  const ok = n > 0 && a === b;
  arms.push(['SAME DENOMINATOR: the planted run prints the clean run\'s CHECK names', ok,
    ok ? `${n} of ${n} names` : `clean ${n} name(s), planted ${Object.keys(planted.checks).length}`]);
}

let pass = 0;
for (const [n, ok, d] of arms) { if (ok) pass += 1; console.log(`${ok ? 'ARM PASS' : 'ARM FAIL'} ${n} :: ${d}`); }
console.log(`POSTURE.HARNESS RUNS GREEN AND GRADES SOMETHING: ${pass} of 3 arms`);
process.exit(pass === 3 ? 0 : 1);
