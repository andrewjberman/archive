/**
 * starredclaims.cjs -- DSGN_AMGTV1 round 22, AV-z-4 (issuer 2.0.0_SA_COO~D): ERROREMPTY'S STARRED CLAIMS GRADE A RENDERED STARRED FACE, OR ARE RETIRED.
 *
 * Usage (repo root): node <this file>        (portal/ under the cwd is the checkout under test)
 * CTO round-21 analysis @e14de1769c ruling 4 / section 3A row A4 (row DSGN_AMGTV1-Z-W56-S4, GRADUATED in ADJUDICATION_v19): the
 * harness's starred cases (`starred_successful_empty`, `starred_failed_request`) still render LeadPanel with `starredOnly`, but
 * StarredList left the Lead Panel, so `starred_error_differs_from_starred_empty` is met by the differing ranking footers, not by a
 * starred face. The repair: RETIRE the starred cases and their claim, or RE-POINT them at the price face's starred state (PriceBars
 * with `starredOnly`: "No starred names in this list." on a successful empty read) -- and the harness stays green.
 * Issuer reading at the cut: `unresolved_row_navigates`, `a_click_sent_a_ticker` and `error_claims_no_daily_row` read the RankedList
 * click tree and the failed_request render (denominator `ranked_row_click_handlers_found` true), so they are EXERCISED and stay.
 * Arms:
 *   1  THE CHECKOUT: errorEmpty.harness.cjs exits 0 with "CHECKS-OK k of k", AND its source either carries no starred case
 *      (`starred_successful_empty` / `starred_failed_request` both gone) or anchors a starred claim on "No starred names".
 *   2  NEGATIVE: the pinned base harness (portal 24646bca; STARRED_BASE overrides) carries the starred cases and no such anchor.
 *   3  KEEP: the checkout harness still prints ranked_row_click_handlers_found=true, unresolved_row_navigates=false,
 *      a_click_sent_a_ticker=false and error_claims_no_daily_row=false (the exercised checks are not retired).
 * Prints one line per arm and "ERROREMPTY'S STARRED CLAIMS GRADE A RENDERED FACE: <k> of 3 arms"; exit 0 only at 3 of 3. Seconds.
 */
const fs = require('fs');
const path = require('path');
const { spawnSync } = require('child_process');

const ROOT = process.cwd();
const PORTAL = path.join(ROOT, 'portal');
const REL = 'src/pages/SecurityAnalysis/__harness__/errorEmpty.harness.cjs';
const PIN = process.env.STARRED_BASE || '24646bca';
const CASES = /starred_successful_empty|starred_failed_request/;
const ANCHOR = /No starred names/;

const run = spawnSync(process.execPath, [path.join(PORTAL, REL)], { cwd: PORTAL, encoding: 'utf8', maxBuffer: 1 << 24, timeout: 110000 });
const out = (run.stdout || '') + (run.stderr || '');
const src = fs.existsSync(path.join(PORTAL, REL)) ? fs.readFileSync(path.join(PORTAL, REL), 'utf8') : '';

const arms = [];
{
  const f = [];
  const ok = /CHECKS-OK (\d+) of (\d+)/.exec(out);
  if (run.status !== 0 || !ok || ok[1] !== ok[2]) f.push(`the harness is not green (rc=${run.status}; ${ok ? ok[0] : 'no CHECKS-OK line'})`);
  const retired = !CASES.test(src);
  const anchored = ANCHOR.test(src);
  if (!retired && !anchored) f.push('the starred cases remain and no starred claim anchors on "No starred names" (the claim still grades nothing)');
  arms.push(['the checkout: the harness is green and its starred claims are retired or graded on the price face\'s starred state', f.length === 0,
    f.length === 0 ? `${ok[0]}; ${retired ? 'starred cases retired' : 'starred claim anchored on the starred face'}` : f.join(' | ')]);
}
{
  const f = [];
  const s = spawnSync('git', ['-C', PORTAL, 'show', `${PIN}:${REL}`], { encoding: 'utf8', maxBuffer: 1 << 24 });
  if (s.status !== 0 || !s.stdout) f.push(`INPUT MISSING: git show ${PIN} rc=${s.status}`);
  else {
    if (!CASES.test(s.stdout)) f.push(`the base at ${PIN} carries no starred case -- the check cannot tell base from fix`);
    if (ANCHOR.test(s.stdout)) f.push(`the base at ${PIN} already anchors on "No starred names"`);
  }
  arms.push([`NEGATIVE: the base harness (${PIN}) carries the starred cases with no starred-face anchor`, f.length === 0,
    f.length === 0 ? 'base is the vacuous form' : f.join(' | ')]);
}
{
  const f = [];
  const want = { ranked_row_click_handlers_found: 'true', unresolved_row_navigates: 'false', a_click_sent_a_ticker: 'false', error_claims_no_daily_row: 'false' };
  for (const [k, v] of Object.entries(want)) {
    const m = new RegExp(`CHECK ${k} = (true|false) \\(expected (true|false)\\)`).exec(out);
    if (!m) f.push(`${k} is no longer printed`);
    else if (m[1] !== v || m[2] !== v) f.push(`${k} reads ${m[1]} (expected ${m[2]}; want ${v})`);
  }
  arms.push(['KEEP: the four exercised RankedList checks still print at their values', f.length === 0,
    f.length === 0 ? '4 of 4 kept' : f.join(' | ')]);
}

let pass = 0;
for (const [n, ok, d] of arms) { if (ok) pass += 1; console.log(`${ok ? 'ARM PASS' : 'ARM FAIL'} ${n} :: ${d}`); }
console.log(`ERROREMPTY'S STARRED CLAIMS GRADE A RENDERED FACE: ${pass} of 3 arms`);
process.exit(pass === 3 ? 0 : 1);
