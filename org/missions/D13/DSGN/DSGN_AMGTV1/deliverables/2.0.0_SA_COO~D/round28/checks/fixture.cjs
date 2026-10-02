/**
 * fixture.cjs -- DSGN_AMGTV1 round 28, AV-zf-1 (issuer 2.0.0_SA_COO~D): THE CONTRACT FIXTURES SERVE NAMES AND AN ABSENT ROW.
 *
 * Usage (worktree root): node <this file>        (portal/ under the cwd is the checkout under test)
 * Fixture under test: portal/src/pages/SecurityAnalysis/__harness__/tests/uiContractFixtures.json (the render check's fixtures).
 * CTO msg 28537 + CVO~Z ADJUDICATION_v27: list.png shows raw security keys because 72 of 95 collected-chatter rows in the fixture
 * predate RESAPP B1's names; FWD-15's ABSENT footnote is never exercised because the BA model block carries every line.
 * The served names: round28/fixtures/served-names.collected-chatter.json, made by the issuer at the cut with the served route's own
 * resolver (lib/research/api/monthly_chatter.py `_display_names`), 95 of 95 resolved, 0 raw keys.
 * The base: the same fixture at portal ref 415f50db (remote DEV at the cut), read with `git -C portal show`.
 * Arms:
 *   1  NAMES: each of the 95 collected-chatter rows carries the producer-resolved display_name; 0 code-shaped names.
 *   2  UNCHANGED: the collected rows' keys and by_month, and every other payload key, deep-equal the base blob's.
 *   3  ABSENT: the BA thesis model block reads exactly ONE absent row in buildModelSheet, RoTA, with RETURN_ON_TANGIBLE_ASSETS
 *      dropped from BOTH figure lists (payload and model block) and every other figure deep-equal to the base blob's.
 * Prints one line per arm and "THE CONTRACT FIXTURES SERVE NAMES AND AN ABSENT ROW: <k> of 3 arms"; exit 0 only at 3 of 3.
 */
const fs = require('fs');
const path = require('path');
const { spawnSync } = require('child_process');

const ROUND = path.join(__dirname, '..', '..');
const L = require(path.join(ROUND, 'round15', 'checks', '_load.cjs'));
const REL = 'src/pages/SecurityAnalysis/__harness__/tests/uiContractFixtures.json';
const NAMES = JSON.parse(fs.readFileSync(path.join(ROUND, 'round28', 'fixtures', 'served-names.collected-chatter.json'), 'utf8')).names;
const COLLECTED = '/api/scoped/amgt/lead-panel/timeseries/collected/chatter';
const THESIS = '/api/scoped/amgt/security/BA_US_Equity/thesis';
const ROTA = 'RETURN_ON_TANGIBLE_ASSETS';
const BASE_REF = '415f50db';
const CODE = /_Equity\b|\b[A-Z0-9*/]+_[A-Z]{2}\b|\b[a-z]+_[a-z0-9_]+\b/;

const baseShow = spawnSync('git', ['-C', 'portal', 'show', `${BASE_REF}:${REL}`], { encoding: 'utf8', maxBuffer: 256 * 1024 * 1024 });
if (baseShow.status !== 0 || !baseShow.stdout) {
  console.log(`BASE READ FAILED: git show ${BASE_REF}:${REL} rc=${baseShow.status} ${String(baseShow.stderr).trim()}`);
  process.exit(2);
}
const BASE = JSON.parse(baseShow.stdout);
const fx = JSON.parse(fs.readFileSync(path.join('portal', ...REL.split('/')), 'utf8'));
const unwrap = (v) => (v && v.payload ? v.payload : v) || {};
const same = (a, b) => JSON.stringify(a) === JSON.stringify(b);
const arms = [];

// Arm 1 -- names.
{
  const f = [];
  const rows = unwrap(fx[COLLECTED]).rows || [];
  if (rows.length !== 95) f.push(`${rows.length} collected rows (want 95)`);
  let named = 0;
  for (const r of rows) {
    const want = NAMES[r.security_key];
    if (!want) { f.push(`${r.security_key}: not in the served-names file`); continue; }
    if (r.display_name !== want.display_name) f.push(`${r.security_key}: "${r.display_name}" (served "${want.display_name}")`);
    else named += 1;
    if (CODE.test(String(r.display_name))) f.push(`${r.security_key}: code-shaped name "${r.display_name}"`);
  }
  arms.push(['NAMES: every collected-chatter row carries its producer-resolved name; 0 code-shaped', f.length === 0,
    f.length ? `${f.length} fault(s): ${f.slice(0, 4).join(' | ')}` : `${named} of ${rows.length} named as served`]);
}
// Arm 2 -- nothing else in the collected payload moved.
{
  const f = [];
  const p = unwrap(fx[COLLECTED]);
  const b = unwrap(BASE[COLLECTED]);
  const body = (x) => (x.rows || []).map((r) => [r.security_key, r.by_month]);
  if (!same(body(p), body(b))) f.push("the rows' keys or by_month differ from the base");
  for (const k of Object.keys(b)) if (k !== 'rows' && !same(p[k], b[k])) f.push(`payload key ${k} differs from the base`);
  arms.push(["UNCHANGED: keys, by_month and the other payload keys are the base's", f.length === 0, f.length ? f.join(' | ') : `equal to portal ${BASE_REF}`]);
}
// Arm 3 -- one ABSENT row, RoTA.
{
  const f = [];
  const p = unwrap(fx[THESIS]);
  const bp = unwrap(BASE[THESIS]);
  const other = (x) => (x || []).filter((y) => y.mnemonic !== ROTA);
  const lists = [
    ['payload', p.fiscal_year_figures, bp.fiscal_year_figures],
    ['model block', p.model && p.model.fiscal_year_figures, bp.model && bp.model.fiscal_year_figures],
  ];
  for (const [n, list, base] of lists) {
    if (!Array.isArray(list)) { f.push(`${n}: no fiscal_year_figures list`); continue; }
    if (list.some((x) => x.mnemonic === ROTA)) f.push(`${n}: still carries ${ROTA}`);
    if (!same(other(list), other(base))) f.push(`${n}: another figure moved`);
  }
  try {
    const m = L.source('src/pages/SecurityAnalysis/modelSheet.ts');
    const sheet = m.buildModelSheet(p.fiscal_year_figures, p.fiscal_years, p.model && p.model.line_names);
    const absent = sheet.groups.flatMap((g) => g.rows).filter((r) => r.absentReason).map((r) => r.label);
    if (absent.length !== 1 || absent[0] !== 'RoTA') f.push(`absent rows [${absent.join(', ')}] (want exactly [RoTA])`);
  } catch (e) { f.push('buildModelSheet: ' + String(e.message).split('\n')[0]); }
  arms.push(['ABSENT: the BA model block reads exactly one absent row, RoTA; every other figure unchanged', f.length === 0, f.length ? f.join(' | ') : '1 absent row (RoTA)']);
}

let pass = 0;
for (const [n, ok, d] of arms) { if (ok) pass += 1; console.log(`${ok ? 'ARM PASS' : 'ARM FAIL'} ${n} :: ${d}`); }
console.log(`THE CONTRACT FIXTURES SERVE NAMES AND AN ABSENT ROW: ${pass} of 3 arms`);
process.exit(pass === 3 ? 0 : 1);
