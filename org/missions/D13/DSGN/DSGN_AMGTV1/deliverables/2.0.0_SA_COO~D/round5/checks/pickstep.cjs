/**
 * pickstep.cjs -- DSGN_AMGTV1 round 5, AV-v-2: THE WALK PICKS ONE NAME ON THE HISTORY VIEW (round-4 analysis s.4 item 2:
 * "a walker step clicks one data-series-ticker button and screenshots the picked line"; the CVO could not grade the pick
 * in round 4 because no walk ever pressed a legend button).
 *
 * Usage (repo root): node <this file>
 * A STATIC read of .claude/skills/ui-walk/walk.mjs (a live walk needs the walker account, which no check arms). Arms:
 *   1  the walker still parses: `node --check walk.mjs` exits 0
 *   2  it presses a legend button: the file carries a `[data-series-ticker]` selector and a `.click(` within 12 lines of
 *      it, and a step label containing "picked" within 12 lines of that click (the step whose screenshot shows the line)
 *   3  the picked step is still graded: the "picked" label reaches the walker's page checks -- a `checks(page, ` call
 *      within 12 lines of the label (so the sign-in guard of round 4 runs on it too)
 * Prints one line per arm and "WALK PICKS A NAME: <k> of 3 arms"; exit 0 only at 3 of 3.
 */
const fs = require('fs');
const path = require('path');
const { spawnSync } = require('child_process');
const file = path.join(process.cwd(), '.claude/skills/ui-walk/walk.mjs');
if (!fs.existsSync(file)) {
  console.log('WALK PICKS A NAME: 0 of 3 arms (walk.mjs absent under ' + process.cwd() + ')');
  process.exit(1);
}
const lines = fs.readFileSync(file, 'utf8').split(/\r?\n/);
const parse = spawnSync(process.execPath, ['--check', file], { encoding: 'utf8', timeout: 60000 });
const at = (re) => lines.map((l, i) => (re.test(l) ? i : -1)).filter((i) => i >= 0);
const near = (a, b, span) => a.some((i) => b.some((j) => Math.abs(i - j) <= span));
const sel = at(/data-series-ticker/);
const click = at(/\.click\(/);
const picked = at(/picked/i);
const checks = at(/checks\(page,/);
const clickNearSel = click.filter((i) => sel.some((j) => Math.abs(i - j) <= 12));
const pickedNearClick = picked.filter((i) => clickNearSel.some((j) => Math.abs(i - j) <= 12));
const arms = [
  ['walk.mjs parses', parse.status === 0, `node --check rc=${parse.status}${parse.status ? ' ' + String(parse.stderr).split('\n')[0] : ''}`],
  ['a legend button is pressed and the step is labelled "picked"', clickNearSel.length > 0 && pickedNearClick.length > 0,
    `selector lines ${sel.length}; click near it ${clickNearSel.length}; "picked" label near the click ${pickedNearClick.length}`],
  ['the picked step reaches the page checks', pickedNearClick.length > 0 && near(pickedNearClick, checks, 12),
    `checks(page, ...) calls ${checks.length}; one near the picked label: ${near(pickedNearClick, checks, 12)}`],
];
let pass = 0;
for (const [name, ok, detail] of arms) {
  if (ok) pass += 1;
  console.log(`${ok ? 'ARM PASS' : 'ARM FAIL'} ${name} :: ${detail}`);
}
console.log(`WALK PICKS A NAME: ${pass} of ${arms.length} arms`);
process.exit(pass === arms.length ? 0 : 1);
