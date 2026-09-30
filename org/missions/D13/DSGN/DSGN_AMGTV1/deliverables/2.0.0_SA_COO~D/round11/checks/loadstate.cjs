/**
 * loadstate.cjs -- DSGN_AMGTV1 round 11, AV-n-4: THE WALKER WAITS FOR A PICKED NAME AND EACH TAB TO FINISH LOADING, NOT FOR TIME,
 * SO THE NO-DOSSIER NAME IS ACTUALLY WALKED (round-10 analysis s.2, cell 4; AMGT_CORPUS FWD-10/11/15/16/18).
 *
 * Usage (repo root): node <this file>
 * Reads .claude/skills/ui-walk/walk.mjs (the issuer-only CHECK_SRC_OVERRIDE may name ".claude/skills/ui-walk/walk.mjs=<file>").
 * On walk I, 6501 JP (0 dossier objects of 287) was typed and submitted, the page issued /overlay, and every 6501 shot is "Loading
 * identity header": the walker's pick step and every tab step waited a FIXED 2.5-3 s (`settle`), and moved on while the first read
 * was still running. The estate's panel states carry `data-panel-state` = loading | error | empty | no-permission
 * (portal/src/ui/components/states/PanelStates.tsx); a loaded identity header carries `[data-bloomberg-session]`.
 * The contract (AV-n-4's face): a top-level `const LOAD_STATE_CEILING_MS = <n>` (n >= 30000) and a top-level
 * `async function waitForLoaded(page)` that polls `page.locator('[data-panel-state="loading"]').count()` and
 * `page.locator('[data-panel-state="error"]').count()`, sleeping with `page.waitForTimeout(<= 500)` and timing with `Date.now()`,
 * and returns `{ state: 'loaded' | 'error' | 'ceiling', waited_ms }` -- 'loaded' once no loading panel is on the page, 'error'
 * once an error panel is and no loading panel is, 'ceiling' when loading never clears.
 * Arms:
 *   1  BEHAVIOUR (the extracted function on a stub page and a fake clock -- no browser, no network): nothing loading -> 'loaded';
 *      a panel loading for 14,000 ms -> 'loaded' with waited_ms >= 13,500; an error panel after loading -> 'error'; a HELD read
 *      (loading never clears) -> 'ceiling' with waited_ms >= 30,000 (the negative arm: a held read never reads as loaded); and
 *      LOAD_STATE_CEILING_MS >= 30,000
 *   2  WIRING: in the --security loop, waitForLoaded runs after the pick (the search submit / row click) and BEFORE the
 *      `${sec}-overlay` shot, and after each tab click and BEFORE the `${sec}-${tab}` shot, with no fixed settle(page, 2500 or 3000)
 *      between the action and that shot
 *   3  RECORD: every such wait is pushed to `loadStates` with `security`, `step`, `state` and `waited_ms`, and `load-states.json`
 *      is written to the walk's output folder whenever loadStates is non-empty
 * Prints one line per arm and "WALKER WAITS FOR THE LOAD STATE: <k> of 3 arms"; exit 0 only at 3 of 3.
 */
const fs = require('fs');
const path = require('path');
const vm = require('vm');
const REL = '.claude/skills/ui-walk/walk.mjs';
const ov = (process.env.CHECK_SRC_OVERRIDE || '').split(';').filter(Boolean).map((p) => [p.slice(0, p.indexOf('=')), p.slice(p.indexOf('=') + 1)]).find(([k]) => k === REL);
const file = ov ? ov[1] : path.join(process.cwd(), REL);
if (!fs.existsSync(file)) { console.log('WALKER WAITS FOR THE LOAD STATE: 0 of 3 arms (walk.mjs absent)'); process.exit(1); }
const src = fs.readFileSync(file, 'utf8');

function fnSource(name) {
  const m = new RegExp('^async\\s+function\\s+' + name + '\\s*\\(', 'm').exec(src);
  if (!m) return null;
  let i = src.indexOf('{', m.index), depth = 0;
  for (let j = i; j < src.length; j++) {
    if (src[j] === '{') depth++;
    else if (src[j] === '}') { depth--; if (depth === 0) return src.slice(m.index, j + 1); }
  }
  return null;
}

const ceilM = /^const\s+LOAD_STATE_CEILING_MS\s*=\s*([0-9_]+)/m.exec(src);
const ceiling = ceilM ? Number(ceilM[1].replace(/_/g, '')) : null;
const fsrc = fnSource('waitForLoaded');
const f1 = [];
async function runScenario(name, plan, expectState, minWait) {
  let clock = 1000000;
  const FakeDate = function () { return new Date(clock); };
  FakeDate.now = () => clock;
  const page = {
    locator(sel) {
      const self = {
        async count() {
          const s = String(sel);
          const t = clock - 1000000;
          const loading = plan.loadingUntil === Infinity || t < plan.loadingUntil;
          if (/data-panel-state="loading"/.test(s)) return loading ? 1 : 0;
          if (/data-panel-state="error"/.test(s)) return !loading && plan.error ? 1 : 0;
          return 0;
        },
        first() { return self; },
      };
      return self;
    },
    async waitForTimeout(ms) {
      if (!(ms > 0 && ms <= 500)) throw new Error('poll sleep ' + ms + ' ms outside (0, 500]');
      clock += ms;
    },
  };
  const ctx = vm.createContext({ Date: FakeDate, LOAD_STATE_CEILING_MS: ceiling, console, log: () => {}, findings: [], setTimeout, Promise });
  let fn;
  try { fn = vm.runInContext('(' + fsrc.replace(/^async\s+function\s+waitForLoaded/, 'async function') + ')', ctx); }
  catch (e) { f1.push(`${name}: the function does not compile standalone (${String(e.message).split('\n')[0]})`); return; }
  try {
    const r = await Promise.race([fn(page), new Promise((_, rej) => setTimeout(() => rej(new Error('real-time timeout 10 s')), 10000))]);
    if (!r || r.state !== expectState) f1.push(`${name}: state ${r && r.state}, want ${expectState}`);
    else if (typeof r.waited_ms !== 'number' || r.waited_ms < minWait) f1.push(`${name}: waited_ms ${r && r.waited_ms}, want >= ${minWait}`);
  } catch (e) { f1.push(`${name}: threw ${String(e.message).split('\n')[0]}`); }
}
async function arm1() {
  if (!fsrc) { f1.push('no top-level async function waitForLoaded'); return; }
  if (!(ceiling >= 30000)) { f1.push(`LOAD_STATE_CEILING_MS ${ceiling}, want >= 30000`); return; }
  await runScenario('nothing loading', { loadingUntil: 0 }, 'loaded', 0);
  await runScenario('loading for 14000 ms', { loadingUntil: 14000 }, 'loaded', 13500);
  await runScenario('error after loading', { loadingUntil: 3000, error: true }, 'error', 2500);
  await runScenario('HELD read (negative arm)', { loadingUntil: Infinity }, 'ceiling', 30000);
}

(async () => {
  await arm1();
  const a1 = f1.length === 0;
  const a1d = a1 ? `4 of 4 scenarios (ceiling ${ceiling} ms; a held read reads "ceiling", never loaded)` : `${f1.length} failing; first: ${f1[0]}`;

  // ---- arm 2: wiring in the --security loop ---------------------------------------------------------------------------------
  const f2 = [];
  const loopAt = src.search(/for\s*\(const sec of opt\.securities\)/);
  let loop = null;
  if (loopAt >= 0) {
    let i = src.indexOf('{', loopAt), depth = 0;
    for (let j = i; j < src.length; j++) {
      if (src[j] === '{') depth++;
      else if (src[j] === '}') { depth--; if (depth === 0) { loop = src.slice(loopAt, j + 1); break; } }
    }
  }
  const between = (body, fromRe, toRe) => {
    const p = body.search(fromRe);
    if (p < 0) return null;
    const rest = body.slice(p);
    const s = rest.search(toRe);
    return s < 0 ? null : rest.slice(0, s);
  };
  if (!loop) f2.push('no `for (const sec of opt.securities)` loop');
  else {
    const segP = between(loop, /box\.press\('Enter'\)|getPlaceholder\('Search any ticker'\)/, /checks\(page,\s*`\$\{sec\}-overlay`/);
    if (!segP || !/waitForLoaded\(page\)/.test(segP)) f2.push('the pick step: waitForLoaded not between the submit and the overlay shot');
    else if (/settle\(page,\s*(2500|3000)\)/.test(segP)) f2.push('the pick step: a fixed settle still precedes the overlay shot');
    const segT = between(loop, /clickLabel\(page,\s*tab\)/, /checks\(page,\s*`\$\{sec\}-\$\{tab\}`/);
    if (!segT || !/waitForLoaded\(page\)/.test(segT)) f2.push('each tab: waitForLoaded not between the tab click and the tab shot');
    else if (/settle\(page,\s*(2500|3000)\)/.test(segT)) f2.push('each tab: a fixed settle still precedes the tab shot');
  }
  const a2 = f2.length === 0;
  const a2d = a2 ? 'the pick and every tab wait for the load state before their shot, with no fixed settle between' : `${f2.length} failing; first: ${f2[0]}`;

  // ---- arm 3: record ----------------------------------------------------------------------------------------------------------
  const f3 = [];
  const pushes = [...src.matchAll(/loadStates\.push\(\{([^}]*)\}\)/g)].map((m) => m[1]);
  if (!pushes.some((p) => /\bsecurity\b/.test(p) && /\bstep\b/.test(p) && /\bstate\b/.test(p) && /\bwaited_ms\b/.test(p))) f3.push('no loadStates record carrying security, step, state and waited_ms');
  const w = /if\s*\(([^)]*)\)\s*writeFileSync\(path\.join\(OUT,\s*'load-states\.json'\)/.exec(src);
  if (!w) f3.push('load-states.json is not written');
  else if (!/loadStates\.length/.test(w[1])) f3.push(`load-states.json is written under "${w[1].trim()}", not whenever loadStates is non-empty`);
  const a3 = f3.length === 0;
  const a3d = a3 ? `${pushes.length} loadStates record site(s) carrying security, step, state and waited_ms; written whenever non-empty` : `${f3.length} failing; first: ${f3[0]}`;

  const arms = [
    ['the load wait resolves on the page\'s panel state, and a held read reads "ceiling"', a1, a1d],
    ['the pick and every tab shot wait for the load state, not a fixed settle', a2, a2d],
    ['every wait is recorded in load-states.json', a3, a3d],
  ];
  let pass = 0;
  for (const [name, ok, detail] of arms) { if (ok) pass += 1; console.log(`${ok ? 'ARM PASS' : 'ARM FAIL'} ${name} :: ${detail}`); }
  console.log(`WALKER WAITS FOR THE LOAD STATE: ${pass} of ${arms.length} arms`);
  process.exit(pass === arms.length ? 0 : 1);
})();
