/**
 * walkerbound.cjs -- DSGN_AMGTV1 round 8, AV-q-1's BOUND: the walker's earlier grading steps stay whole.
 *
 * Usage (repo root): node <this file>
 * Runs, unchanged, the three earlier walker checks this cell's edit must not undo (the walker was silently cut once by the
 * integrator merge 8b3f8e8833 and restored @4a0628755b, row DSGN_AMGTV1-Z-S4):
 *   round5/checks/pickstep.cjs   -- one legend button pressed per chart ("-Chart-picked")
 *   round6/checks/walkthread.cjs -- --thread by name, lead-lists.json, the timeline day / event steps
 *   round7/checks/walkday.cjs    -- --day "<security>=<YYYY-MM-DD>" and timeline-days.json
 * CHECK_SRC_OVERRIDE (issuer only) is passed through to each. Prints one line per check and
 * "WALKER BOUND: <k> of 3 checks green"; exit 0 only at 3 of 3.
 */
const path = require('path');
const { spawnSync } = require('child_process');
const base = path.join(process.cwd(), 'org/missions/D13/DSGN/DSGN_AMGTV1/deliverables/2.0.0_SA_COO~D');
const checks = [
  ['round5/checks/pickstep.cjs', /WALK PICKS A NAME: 3 of 3 arms/],
  ['round6/checks/walkthread.cjs', /WALK GRADES BY NAME: 3 of 3 arms/],
  ['round7/checks/walkday.cjs', /WALK OPENS A DAY BY DATE: 3 of 3 arms/],
];
let pass = 0;
for (const [rel, want] of checks) {
  const r = spawnSync(process.execPath, [path.join(base, rel)], { cwd: process.cwd(), encoding: 'utf8', timeout: 60000, env: process.env });
  const out = (r.stdout || '') + (r.stderr || '');
  const last = out.trim().split('\n').pop();
  const ok = r.status === 0 && want.test(out);
  if (ok) pass += 1;
  console.log(`${ok ? 'CHECK GREEN' : 'CHECK RED'} ${rel} :: ${last}`);
}
console.log(`WALKER BOUND: ${pass} of ${checks.length} checks green`);
process.exit(pass === checks.length ? 0 : 1);
