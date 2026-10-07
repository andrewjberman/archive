/**
 * r50.cjs -- DSGN_AMGTV1 round 50 issuer CHECK (2.0.0_SA_COO~D): THE RENDER CHECK REQUIRES THE THREE DESIGNED STATES OF FWD-19, NOT FOUR.
 *
 * Usage (from the directory whose portal/ is the checkout under test):
 *   cd "$(git rev-parse --show-toplevel)" && node "org/missions/D13/DSGN/DSGN_AMGTV1/deliverables/2.0.0_SA_COO~D/round50/checks/r50/r50.cjs"
 *
 * Why: PRD v0.17 FWD-19 reads three designed states (empty, loading, error); PanelNoPermission was removed on Andrew's 2026-10-05
 * word, and FWD-20's DONE WHEN reads "the three states of FWD-19 present". portal/scripts/ui-contract-check.mjs still REQUIRES a
 * fourth: its run cell `fourStates` fails unless a no-permission state was counted, and `gradeFwd19` fails unless the standalone
 * no-permission capture was taken. It passes today only because that capture is still taken (round49/ROUND49_CLOSE.md; CTO msg 30918).
 *
 * How it reads the instrument WITHOUT running it: it lifts two pieces of the script's text and evaluates each alone with planted
 * inputs -- the whole `gradeFwd19` function, and the block that builds the run cell (from `const combined = { ...acrossRun }` to the
 * `if (sweepSummary) {` that follows the cell). The order names the one constant the block may use: REQUIRED_PANEL_KINDS.
 *
 * Arms (each prints its evidence; exit 0 only on all of them):
 *   1 THE PER-PANEL CELL DOES NOT NEED A NO-PERMISSION CAPTURE: gradeFwd19, with empty, loading and error seen on six of six panels
 *     and the standalone capture NOT taken, reads PASS.
 *   2 THE RUN CELL NEEDS THREE KINDS: with loading, error and empty counted and no-permission at zero the run cell reads PASS; with
 *     error at zero it reads FAIL and names error.
 *   3 KEEP: gradeFwd19 still FAILS when one panel shows no error state (naming that panel), and still reads NOT_EXERCISED without a
 *     sweep; the run cell still reads NOT_EXERCISED when no state showed application DOM.
 *   4 PLANTED: the same harness refuses a four-state grader and a four-kind run cell, and admits a three-state pair.
 * No network; writes nothing.
 */
'use strict';
const fs = require('fs');
const path = require('path');

const FILE = path.join(process.cwd(), 'portal', 'scripts', 'ui-contract-check.mjs');
const SIX = ['list', 'thesis', 'exec', 'peers', 'model', 'posture'];
const STATES = SIX.map((name) => ({ name }));
const THREE = ['empty', 'loading', 'error'];
const PANEL_KINDS = ['loading', 'error', 'empty', 'no-permission'];

function liftFwd19(src) {
  const at = src.indexOf('function gradeFwd19(');
  if (at < 0) return { error: 'no function gradeFwd19' };
  const end = src.indexOf('\n}\n', at);
  if (end < 0) return { error: 'cannot find the end of gradeFwd19' };
  const text = src.slice(at, end + 2);
  return {
    run: (panelStateCounts, sweepSummary, anyExercised) => {
      const combined = {};
      return new Function('STATES', 'panelStateCounts', 'anyExercised', 'sweepSummary', 'combined', 'REACHABLE_KINDS', 'REQUIRED_PANEL_KINDS', 'PANEL_KINDS',
        `${text}\nreturn gradeFwd19()`)(STATES, panelStateCounts, anyExercised, sweepSummary, combined, THREE, THREE, PANEL_KINDS);
    },
  };
}
function liftRunCell(src) {
  const a = src.indexOf('const combined = { ...acrossRun }');
  if (a < 0) return { error: 'no `const combined = { ...acrossRun }` line' };
  const b = src.indexOf('if (sweepSummary) {', src.indexOf('const fourStates', a));
  if (src.indexOf('const fourStates', a) < 0 || b < 0) return { error: 'cannot find the run cell (`const fourStates`) and the `if (sweepSummary) {` after it' };
  const text = src.slice(a, b);
  return {
    run: (acrossRun, sweepSummary, anyExercised) => new Function('PANEL_KINDS', 'REQUIRED_PANEL_KINDS', 'acrossRun', 'sweepSummary', 'anyExercised', 'panelStateCounts',
      `${text}\nreturn fourStates`)(PANEL_KINDS, ['loading', 'error', 'empty'], acrossRun, sweepSummary, anyExercised, {}),
  };
}

const allThree = () => Object.fromEntries(SIX.map((s) => [s, { empty: 0, loading: 0, error: 0 }]));
const sweepAll = (captured) => ({ perState: Object.fromEntries(SIX.map((s) => [s, { empty: 1, loading: 1, error: 1 }])), byKind: { empty: 6, loading: 6, error: 6, 'no-permission': captured ? 1 : 0 }, standalone: { captured } });

function gradePerPanel(run) {
  const f = [];
  let r;
  try { r = run(allThree(), sweepAll(false), true); } catch (e) { return ['gradeFwd19 threw: ' + e.message]; }
  if (!r || r.grade !== 'PASS') f.push(`three kinds on 6 of 6 panels with no standalone capture reads ${r ? r.grade : 'nothing'}${r && r.value && r.value.missing ? ' missing ' + JSON.stringify(r.value.missing) : ''}`);
  return f;
}
function gradeRunCell(run) {
  const f = [];
  try {
    const ok = run({ loading: 0, error: 0, empty: 0, 'no-permission': 0 }, sweepAll(false), true);
    if (!ok || ok.grade !== 'PASS') f.push(`three kinds counted and no-permission at zero reads ${ok ? ok.grade : 'nothing'}${ok && ok.counts ? ' missing ' + JSON.stringify(ok.counts.missing) : ''}`);
    const sw = sweepAll(false); sw.byKind.error = 0;
    const bad = run({ loading: 0, error: 0, empty: 0, 'no-permission': 0 }, sw, true);
    if (!bad || bad.grade !== 'FAIL') f.push(`error at zero reads ${bad ? bad.grade : 'nothing'}, want FAIL`);
    else if (!JSON.stringify(bad.counts && bad.counts.missing).includes('error')) f.push('the FAIL does not name error');
  } catch (e) { f.push('the run cell threw: ' + e.message); }
  return f;
}
function gradeKeep(perPanel, runCell) {
  const f = [];
  try {
    const sw = sweepAll(true); sw.perState.model = { empty: 1, loading: 1, error: 0 };
    const r = perPanel(allThree(), sw, true);
    if (!r || r.grade !== 'FAIL') f.push(`a panel with no error state reads ${r ? r.grade : 'nothing'}, want FAIL`);
    else if (!JSON.stringify(r.value.missing).includes('model/error')) f.push('the FAIL does not name model/error');
    const n = perPanel(allThree(), null, true);
    if (!n || n.grade !== 'NOT_EXERCISED') f.push(`no sweep reads ${n ? n.grade : 'nothing'}, want NOT_EXERCISED`);
    const blank = runCell({ loading: 0, error: 0, empty: 0, 'no-permission': 0 }, sweepAll(true), false);
    if (!blank || blank.grade !== 'NOT_EXERCISED') f.push(`a run with no application DOM reads ${blank ? blank.grade : 'nothing'}, want NOT_EXERCISED`);
  } catch (e) { f.push('KEEP threw: ' + e.message); }
  return f;
}

const src = fs.existsSync(FILE) ? fs.readFileSync(FILE, 'utf8').replace(/\r\n/g, '\n') : null;
const arms = [];
if (src === null) {
  arms.push(['READ', false, `cannot read ${FILE}`]);
} else {
  const p = liftFwd19(src); const c = liftRunCell(src);
  { const f = p.error ? [p.error] : gradePerPanel(p.run);
    arms.push(['THE PER-PANEL CELL DOES NOT NEED A NO-PERMISSION CAPTURE', f.length === 0, f.length ? `${f.length} failing; first: ${f[0]}` : 'three kinds on 6 of 6 panels, standalone capture not taken: PASS']); }
  { const f = c.error ? [c.error] : gradeRunCell(c.run);
    arms.push(['THE RUN CELL NEEDS THREE KINDS', f.length === 0, f.length ? `${f.length} failing; first: ${f[0]}` : 'no-permission at zero: PASS; error at zero: FAIL naming error']); }
  { const f = p.error || c.error ? [p.error || c.error] : gradeKeep(p.run, c.run);
    arms.push(['KEEP: a missing error state still fails; no sweep and no DOM still read NOT_EXERCISED', f.length === 0, f.length ? `${f.length} failing; first: ${f[0]}` : 'model/error missing: FAIL; no sweep: NOT_EXERCISED; no DOM: NOT_EXERCISED']); }
}
{
  const f = [];
  const perPanelWith = (needStandalone) => (counts, sw, any) => {
    if (!any) return { grade: 'NOT_EXERCISED', value: {} };
    if (!sw) return { grade: 'NOT_EXERCISED', value: {} };
    const missing = [];
    for (const s of SIX) for (const k of THREE) if (((counts[s] || {})[k] || 0) + ((sw.perState[s] || {})[k] || 0) === 0) missing.push(`${s}/${k}`);
    if (needStandalone && !sw.standalone.captured) missing.push('no-permission');
    return { grade: missing.length ? 'FAIL' : 'PASS', value: { missing } };
  };
  const runCellWith = (kinds) => (across, sw, any) => {
    const combined = { ...across };
    for (const k of PANEL_KINDS) combined[k] += sw.byKind[k] || 0;
    const missing = kinds.filter((k) => combined[k] === 0);
    return { grade: !any ? 'NOT_EXERCISED' : missing.length ? 'FAIL' : 'PASS', counts: { missing } };
  };
  if (!gradePerPanel(perPanelWith(true)).length) f.push('a four-state per-panel grader is admitted');
  if (gradePerPanel(perPanelWith(false)).length) f.push('a three-state per-panel grader is refused');
  if (!gradeRunCell(runCellWith(PANEL_KINDS)).length) f.push('a four-kind run cell is admitted');
  if (gradeRunCell(runCellWith(['loading', 'error', 'empty'])).length) f.push('a three-kind run cell is refused: ' + gradeRunCell(runCellWith(['loading', 'error', 'empty']))[0]);
  if (gradeKeep(perPanelWith(false), runCellWith(['loading', 'error', 'empty'])).length) f.push('the reference pair fails KEEP: ' + gradeKeep(perPanelWith(false), runCellWith(['loading', 'error', 'empty']))[0]);
  arms.push(['PLANTED', f.length === 0, f.length ? f.join(' | ') : '2 four-state forms refused, the three-state pair admitted and it keeps KEEP']);
}

const TITLE = 'THE RENDER CHECK REQUIRES THREE DESIGNED STATES, NOT FOUR';
let pass = 0;
for (const [name, ok, ev] of arms) { if (ok) pass += 1; console.log(`ARM ${ok ? 'PASS' : 'FAIL'} ${name} :: ${ev}`); }
console.log(`${TITLE}: ${pass} of ${arms.length} arms`);
process.exit(pass === arms.length && arms.length === 4 ? 0 : 1);
