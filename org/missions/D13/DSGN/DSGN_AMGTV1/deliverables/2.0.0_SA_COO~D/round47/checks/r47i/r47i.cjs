/**
 * r47i.cjs -- DSGN_AMGTV1 round 47 issuer CHECK (2.0.0_SA_COO~D): THE RENDER CHECK'S PURPLE-FILL CLAUSE READS PRD v0.16's FWD-18 --
 * AT MOST ONE PURPLE FILL IN THE UNIVERSE VIEW, ZERO IN A SECURITY VIEW.
 *
 * Usage (from the directory whose portal/ is the checkout under test):
 *   cd "$(git rev-parse --show-toplevel)" && node "org/missions/D13/DSGN/DSGN_AMGTV1/deliverables/2.0.0_SA_COO~D/round47/checks/r47i/r47i.cjs"
 *
 * Why: PRD v0.17 FWD-18 DONE WHEN (changed at v0.16): "the rendered state reads purpleFills <= 1 in every view and == 0 in Security
 * mode". portal/scripts/ui-contract-check.mjs still grades the retired rule (1 in a Security state, and that one is Refresh; 0 in the
 * Universe state). The re-run control was removed in round 45, so the old rule fails on five states (round-46 and round-47 runs: 10
 * FAIL cells). ledger/CTO_COUNTERSIGN_COMPLETION_GRADES_ROUND46.md ruling 3 and ROUND 47 item 3; CTO msg 30831.
 *
 * How it reads the instrument WITHOUT running it: it lifts two pieces of source text out of ui-contract-check.mjs and evaluates each
 * alone -- the `purpleFills` predicate's `grade` function and the whole `gradeFwd18` function (with a recording `fwdCell`).
 *
 * Arms (each prints its evidence; exit 0 only on all of them):
 *   1 THE PREDICATE: Security state names (thesis, exec, peers, model, posture) pass at 0 and fail at 1; the Universe state (list)
 *     passes at 0 and at 1 and fails at 2.
 *   2 THE FWD-18 CELL IN A SECURITY STATE: gradeFwd18 returns no failure at purpleFills 0 and a failure at purpleFills 1; no failure
 *     text asks for the Refresh action.
 *   3 THE RETIRED WORDS ARE GONE: the file no longer says "want 1 in a Security state" or "is not the Refresh action".
 *   4 PLANTED: the same harness refuses the retired predicate and the retired cell grader, and admits a reference pair.
 * No network; writes nothing.
 */
'use strict';
const fs = require('fs');
const path = require('path');

const FILE = path.join(process.cwd(), 'portal', 'scripts', 'ui-contract-check.mjs');
const SECURITY = ['thesis', 'exec', 'peers', 'model', 'posture'];

function liftPredicate(src) {
  const at = src.indexOf("name: 'purpleFills',");
  if (at < 0) return { error: "no `name: 'purpleFills',` predicate" };
  const g = src.indexOf('grade:', at);
  if (g < 0) return { error: 'no grade: after the purpleFills predicate name' };
  // the arrow function runs from after "grade:" to the "}," that closes it at the predicate's indent
  const end = src.indexOf('\n    },', g);
  if (end < 0) return { error: 'cannot find the end of the purpleFills grade function' };
  const text = src.slice(g + 'grade:'.length, end + '\n    }'.length).trim();
  try { return { fn: new Function(`return (${text})`)() }; } catch (e) { return { error: 'predicate does not evaluate: ' + e.message }; }
}
function liftFwd18(src) {
  const at = src.indexOf('function gradeFwd18(');
  if (at < 0) return { error: 'no function gradeFwd18' };
  const end = src.indexOf('\nfunction ', at + 10);
  const text = src.slice(at, end < 0 ? src.length : end);
  try {
    const make = new Function('fwdCell', `${text}\nreturn gradeFwd18`);
    return { fn: make((fails, unseen, value) => ({ fails: fails.slice(), unseen: unseen.slice(), value })) };
  } catch (e) { return { error: 'gradeFwd18 does not evaluate: ' + e.message }; }
}

function gradePredicate(fn) {
  const f = [];
  for (const s of SECURITY) {
    if (fn({ purpleFills: 0 }, s).pass !== true) f.push(`${s}: 0 purple fills does not pass`);
    if (fn({ purpleFills: 1 }, s).pass !== false) f.push(`${s}: 1 purple fill is not refused`);
  }
  if (fn({ purpleFills: 0 }, 'list').pass !== true) f.push('list: 0 purple fills does not pass');
  if (fn({ purpleFills: 1 }, 'list').pass !== true) f.push('list: 1 purple fill does not pass (PRD: at most one per view)');
  if (fn({ purpleFills: 2 }, 'list').pass !== false) f.push('list: 2 purple fills are not refused');
  return f;
}
function gradeCell(fn) {
  const f = [];
  for (const s of SECURITY) {
    const zero = fn({ name: s }, { purpleFills: 0, purpleRefresh: 0, nodesScanned: 900 });
    const one = fn({ name: s }, { purpleFills: 1, purpleRefresh: 1, nodesScanned: 900 });
    if (!zero || !Array.isArray(zero.fails)) { f.push(`${s}: gradeFwd18 returned no cell`); continue; }
    if (zero.fails.length) f.push(`${s}: 0 purple fills fails ("${zero.fails[0]}")`);
    if (!one.fails.length) f.push(`${s}: 1 purple fill is not refused`);
    if ([...zero.fails, ...one.fails].some((x) => /Refresh/i.test(x))) f.push(`${s}: a failure still asks for the Refresh action`);
  }
  return f;
}

const src = fs.existsSync(FILE) ? fs.readFileSync(FILE, 'utf8') : null;
const arms = [];
if (src === null) {
  arms.push(['READ', false, `cannot read ${FILE}`]);
} else {
  const p = liftPredicate(src);
  { const f = p.error ? [p.error] : gradePredicate(p.fn);
    arms.push(['THE PREDICATE: ZERO IN A SECURITY VIEW, AT MOST ONE IN THE UNIVERSE VIEW', f.length === 0, f.length ? `${f.length} failing; first: ${f[0]}` : '5 Security states pass at 0 and fail at 1; list passes at 0 and 1, fails at 2']); }
  const c = liftFwd18(src);
  { const f = c.error ? [c.error] : gradeCell(c.fn);
    arms.push(['THE FWD-18 CELL IN A SECURITY STATE', f.length === 0, f.length ? `${f.length} failing; first: ${f[0]}` : '5 Security states: no failure at 0, a failure at 1, no Refresh demand']); }
  { const f = [];
    if (src.includes('want 1 in a Security state')) f.push('"want 1 in a Security state" survives');
    if (src.includes('is not the Refresh action')) f.push('"is not the Refresh action" survives');
    arms.push(['THE RETIRED WORDS ARE GONE', f.length === 0, f.length ? f.join(' | ') : 'neither retired failure text is in the file']); }
}
{
  const f = [];
  const oldPred = (j, stateName) => { const expected = stateName === 'list' ? 0 : 1; const v = j.purpleFills; return { pass: v === expected, value: String(v) }; };
  const newPred = (j, stateName) => { const v = j.purpleFills; return { pass: stateName === 'list' ? v <= 1 : v === 0, value: String(v) }; };
  if (!gradePredicate(oldPred).length) f.push('the retired predicate is admitted');
  if (gradePredicate(newPred).length) f.push('the reference predicate is refused: ' + gradePredicate(newPred)[0]);
  const cell = (fails) => ({ fails, unseen: [], value: null });
  const oldCell = (state, m) => { const fails = []; if (m.purpleFills !== 1) fails.push('purpleFills, want 1 in a Security state'); else if (m.purpleRefresh !== 1) fails.push('the one purple fill is not the Refresh action'); return cell(fails); };
  const newCell = (state, m) => cell(m.purpleFills !== 0 ? [`purpleFills ${m.purpleFills}, want 0 in a Security state`] : []);
  if (!gradeCell(oldCell).length) f.push('the retired cell grader is admitted');
  if (gradeCell(newCell).length) f.push('the reference cell grader is refused: ' + gradeCell(newCell)[0]);
  arms.push(['PLANTED', f.length === 0, f.length ? f.join(' | ') : '2 retired forms refused, 2 reference forms admitted']);
}

const TITLE = 'THE RENDER CHECK READS ZERO PURPLE FILLS IN A SECURITY VIEW AND AT MOST ONE IN THE UNIVERSE VIEW';
let pass = 0;
for (const [name, ok, ev] of arms) { if (ok) pass += 1; console.log(`ARM ${ok ? 'PASS' : 'FAIL'} ${name} :: ${ev}`); }
console.log(`${TITLE}: ${pass} of ${arms.length} arms`);
process.exit(pass === arms.length && arms.length === 4 ? 0 : 1);
