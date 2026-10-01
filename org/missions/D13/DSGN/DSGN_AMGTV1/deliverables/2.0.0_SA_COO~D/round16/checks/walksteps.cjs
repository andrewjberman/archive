/**
 * walksteps.cjs -- DSGN_AMGTV1 round 16, AV-g-1 item 2 (issuer 2.0.0_SA_COO~D): THE WALKER WALKS THE FRIDAY FACES.
 *
 * Usage (repo root): node <this file>
 * The round-15 close walk (tmp/ui-walk/20261001T073050Z, site Z) still iterated Movement x Subject x View (walk.mjs:427-435):
 * 4 walker:control-missing findings ("Trending, List view", "Breakout, Chart view", ...), lead-lists.json read from a List view
 * that no longer exists (rulings R5/R6: Trending only, no List/Chart, chatter = bubbles, price = bars), and the --thread row
 * found by `[data-row-lead]` on "Trending x Price, List view" (walk.mjs:289-295).
 * Arms (a static read of `.claude/skills/ui-walk/walk.mjs` in the checkout under test; nothing is run):
 *   1  the checkout: `node --check` passes; the lead-panel walk names no 'List view' / 'Chart view' / 'Breakout' control label;
 *      it steps the two faces by their labels 'Chatter' and 'Price'; on Price it reads the bars by `data-price-bar` (into
 *      lead-lists.json); on Chatter it reads the bubbles (`data-bubble` or `data-chatter-bubble`) and presses the month cursor
 *      ('Earlier month'); the --thread / row selection finds a name by its price bar, not by `data-row-lead`
 *   2  the negative: the same predicates FAIL on the base walk.mjs (git show 8e87440071:.claude/skills/ui-walk/walk.mjs, the file
 *      before round 16; WALKSTEPS_BASE overrides the pin)
 *   3  planted control: the checkout's file with one 'List view' label re-inserted into the lead loop is rejected
 * Prints one line per arm and "THE WALKER WALKS THE FRIDAY FACES: <k> of 3 arms"; exit 0 only at 3 of 3. Under 1 second.
 */
const fs = require('fs');
const os = require('os');
const path = require('path');
const { spawnSync } = require('child_process');

const ROOT = process.cwd();
const REL = '.claude/skills/ui-walk/walk.mjs';
const PIN = process.env.WALKSTEPS_BASE || '8e87440071';

function faults(src) {
  const f = [];
  const strip = src.replace(/\/\/[^\n]*/g, '').replace(/\/\*[\s\S]*?\*\//g, '');
  for (const bad of ["'List view'", '"List view"', "'Chart view'", '"Chart view"', "'Breakout'", '"Breakout"']) {
    if (strip.includes(bad)) f.push(`STALE: the walk still names the removed control ${bad}`);
  }
  if (!/['"]Chatter['"]/.test(strip) || !/['"]Price['"]/.test(strip)) f.push("FACES: the walk does not step 'Chatter' and 'Price'");
  if (!/data-price-bar/.test(strip)) f.push('BARS: the walk never reads [data-price-bar]');
  if (!/data-(chatter-)?bubble/.test(strip)) f.push('BUBBLES: the walk never reads the bubbles');
  if (!/Earlier month/.test(strip)) f.push("CURSOR: the walk never presses the month cursor ('Earlier month')");
  if (/data-row-lead/.test(strip)) f.push('THREAD: the row is still found by [data-row-lead] (the list view is gone)');
  return f;
}

// arm 1
const file = path.join(ROOT, REL);
const f1 = [];
let src = '';
try { src = fs.readFileSync(file, 'utf8'); } catch (e) { f1.push(`MISSING: ${REL}`); }
if (src) {
  const chk = spawnSync(process.execPath, ['--check', file], { encoding: 'utf8' });
  if (chk.status !== 0) f1.push(`SYNTAX: node --check rc=${chk.status}: ${String(chk.stderr).trim().split('\n')[0]}`);
  f1.push(...faults(src));
}
const a1 = f1.length === 0;

// arm 2
const f2 = [];
const base = spawnSync('git', ['show', `${PIN}:${REL}`], { cwd: ROOT, encoding: 'utf8', maxBuffer: 1 << 26 });
if (base.status !== 0 || !base.stdout) f2.push(`INPUT MISSING: git show ${PIN}:${REL} rc=${base.status}`);
const bf = base.stdout ? faults(base.stdout) : [];
if (!f2.length && bf.length === 0) f2.push('the base walk.mjs passes arm 1 -- the check cannot fail');
const a2 = f2.length === 0;

// arm 3
const f3 = [];
let mf = [];
if (src) {
  const mutant = src.replace(/(['"])Chatter\1/, "'List view'");
  const tmp = path.join(fs.mkdtempSync(path.join(os.tmpdir(), 'walksteps-')), 'walk.mjs');
  fs.writeFileSync(tmp, mutant);
  mf = faults(fs.readFileSync(tmp, 'utf8'));
  if (!mf.some((x) => x.startsWith('STALE:'))) f3.push('a planted List view label was not rejected');
} else f3.push('no checkout file to mutate');
const a3 = f3.length === 0;

const arms = [
  ['the checkout walks Chatter and Price, reads bars and bubbles, presses the cursor, threads by a bar', a1, a1 ? `0 faults; node --check OK` : `${f1.length} fault(s); first: ${f1[0]}`],
  [`NEGATIVE: the base walk.mjs (${PIN}) fails arm 1`, a2, a2 ? `${bf.length} fault(s) at base; first: ${bf[0]}` : f2[0]],
  ['PLANTED: a re-inserted List view label is rejected', a3, a3 ? `rejected (${mf.filter((x) => x.startsWith('STALE:')).length} STALE fault)` : f3[0]],
];
let pass = 0;
for (const [name, ok, d] of arms) { if (ok) pass += 1; console.log(`${ok ? 'ARM PASS' : 'ARM FAIL'} ${name} :: ${d}`); }
console.log(`THE WALKER WALKS THE FRIDAY FACES: ${pass} of 3 arms`);
process.exit(pass === 3 ? 0 : 1);
