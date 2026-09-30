/**
 * daystate.cjs -- DSGN_AMGTV1 round 8, AV-q-1: THE WALKER WAITS FOR THE OPENED DAY'S STATE, NOT FOR TIME (round-7 analysis
 * ruling 1; AMGT_HARVST FWD-5, FWD-6).
 *
 * Usage (repo root): node <this file>
 * Reads .claude/skills/ui-walk/walk.mjs (the issuer-only CHECK_SRC_OVERRIDE may name ".claude/skills/ui-walk/walk.mjs=<file>" to
 * prove the check can pass; a worker never sets it). The walker shot every opened day 1,500 ms after the press while the deployed
 * /timeline/day answers in ~5.5 s for a day with articles (CVO v9) -- so every shot was a skeleton.
 * The contract (AV-q-1's face): a top-level `const DAY_STATE_CEILING_MS = <n>` (n >= 15000) and a top-level
 * `async function waitForDayState(page, date)` that polls `page.locator(<sel>).count()` for the day's three designed states --
 *   rows    [data-timeline-selected-day="<date>"] [data-timeline-dissection="SERVED"] [data-timeline-article]
 *   empty   [data-timeline-selected-day="<date>"] [data-timeline-day-empty]
 *   failed  [data-timeline-selected-day="<date>"] [data-timeline-dissection="FAILED"]
 * sleeping between polls with `page.waitForTimeout(<= 500)` and timing with `Date.now()`, and returns
 * `{ state: 'rows' | 'empty' | 'failed' | 'ceiling', waited_ms }`.
 * Arms:
 *   1  BEHAVIOUR (the extracted function run against a stub page and a fake clock -- no browser, no network): rows served at
 *      once -> 'rows'; rows landing after 6,000 ms (the measured latency) -> 'rows' with waited_ms >= 5,500; an empty day ->
 *      'empty'; a failed day -> 'failed'; a HELD route (no state ever) -> 'ceiling' with waited_ms >= 15,000 (the negative arm:
 *      a held route never reads as rows); and DAY_STATE_CEILING_MS >= 15,000
 *   2  WIRING: in the --day step (the function pressing `[data-day-bar="${date}"]`) and in walkTimeline (the newest-day press
 *      AND the event open), waitForDayState runs AFTER the press and BEFORE that step's checks(page, ...) shot, with no
 *      settle(page, 1500) between the press and the shot; the --day step reads article rows only when the state is 'rows'
 *   3  RECORD: every opened day (via 'day', 'newest', 'event') is pushed to timelineDays with its state and waited_ms, and
 *      timeline-days.json is written whenever timelineDays is non-empty (not only when --day was given)
 * Prints one line per arm and "WALKER WAITS FOR DAY STATE: <k> of 3 arms"; exit 0 only at 3 of 3.
 */
const fs = require('fs');
const path = require('path');
const vm = require('vm');
const REL = '.claude/skills/ui-walk/walk.mjs';
const ov = (process.env.CHECK_SRC_OVERRIDE || '').split(';').filter(Boolean).map((p) => [p.slice(0, p.indexOf('=')), p.slice(p.indexOf('=') + 1)]).find(([k]) => k === REL);
const file = ov ? ov[1] : path.join(process.cwd(), REL);
if (!fs.existsSync(file)) { console.log('WALKER WAITS FOR DAY STATE: 0 of 3 arms (walk.mjs absent)'); process.exit(1); }
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
const heads = [...src.matchAll(/^(?:async\s+)?function\s+([A-Za-z0-9_]+)\s*\(/gm)].map((m) => ({ name: m[1], at: m.index }));
const fns = heads.map((h, i) => ({ name: h.name, body: src.slice(h.at, i + 1 < heads.length ? heads[i + 1].at : src.length) }));

// ---- arm 1: behaviour on a stub page + fake clock -----------------------------------------------------------------------
const ceilM = /^const\s+DAY_STATE_CEILING_MS\s*=\s*([0-9_]+)/m.exec(src);
const ceiling = ceilM ? Number(ceilM[1].replace(/_/g, '')) : null;
const fsrc = fnSource('waitForDayState');
const f1 = [];
async function runScenario(name, whenReady, expectState, minWait) {
  let clock = 1000000;
  const FakeDate = function () { return new Date(clock); };
  FakeDate.now = () => clock;
  const date = '2026-08-13';
  const page = {
    locator(sel) {
      const self = {
        async count() {
          const s = String(sel);
          if (!s.includes(`data-timeline-selected-day="${date}"`)) return 0;
          const at = whenReady.at;
          if (clock < 1000000 + at) return 0;
          if (whenReady.state === 'rows' && /data-timeline-dissection="SERVED"\]\s*\[data-timeline-article\]/.test(s)) return 2;
          if (whenReady.state === 'empty' && /\[data-timeline-day-empty\]/.test(s)) return 1;
          if (whenReady.state === 'failed' && /data-timeline-dissection="FAILED"/.test(s)) return 1;
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
  const ctx = vm.createContext({ Date: FakeDate, DAY_STATE_CEILING_MS: ceiling, console, log: () => {}, findings: [], setTimeout, Promise });
  let fn;
  try { fn = vm.runInContext('(' + fsrc.replace(/^async\s+function\s+waitForDayState/, 'async function') + ')', ctx); }
  catch (e) { f1.push(`${name}: the function does not compile standalone (${String(e.message).split('\n')[0]})`); return; }
  try {
    const r = await Promise.race([fn(page, date), new Promise((_, rej) => setTimeout(() => rej(new Error('real-time timeout 10 s')), 10000))]);
    if (!r || r.state !== expectState) f1.push(`${name}: state ${r && r.state}, want ${expectState}`);
    else if (typeof r.waited_ms !== 'number' || r.waited_ms < minWait) f1.push(`${name}: waited_ms ${r && r.waited_ms}, want >= ${minWait}`);
  } catch (e) { f1.push(`${name}: threw ${String(e.message).split('\n')[0]}`); }
}
async function arm1() {
  if (!fsrc) { f1.push('no top-level async function waitForDayState'); return; }
  if (!(ceiling >= 15000)) { f1.push(`DAY_STATE_CEILING_MS ${ceiling}, want >= 15000`); return; }
  await runScenario('rows at once', { state: 'rows', at: 0 }, 'rows', 0);
  await runScenario('rows after 6000 ms', { state: 'rows', at: 6000 }, 'rows', 5500);
  await runScenario('empty day', { state: 'empty', at: 0 }, 'empty', 0);
  await runScenario('failed day', { state: 'failed', at: 1500 }, 'failed', 0);
  await runScenario('HELD route (negative arm)', { state: 'none', at: 0 }, 'ceiling', 15000);
}

(async () => {
  await arm1();
  const a1 = f1.length === 0;
  const a1d = a1 ? `5 of 5 scenarios (ceiling ${ceiling} ms; a held route reads "ceiling", never rows)` : `${f1.length} failing; first: ${f1[0]}`;

  // ---- arm 2: wiring --------------------------------------------------------------------------------------------------
  const f2 = [];
  const dayFn = fns.find((f) => /data-day-bar="\$\{date\}"/.test(f.body));
  const tl = fns.find((f) => f.name === 'walkTimeline');
  const between = (body, pressRe, shotRe) => {
    const p = body.search(pressRe);
    if (p < 0) return null;
    const rest = body.slice(p);
    const s = rest.search(shotRe);
    return s < 0 ? null : rest.slice(0, s);
  };
  if (!dayFn) f2.push('no function presses [data-day-bar="${date}"]');
  else {
    const seg = between(dayFn.body, /data-day-bar="\$\{date\}"/, /checks\(page,\s*`\$\{sec\}-timeline-day-\$\{date\}`/);
    if (!seg || !/waitForDayState\(page,/.test(seg)) f2.push(`${dayFn.name}: waitForDayState not between the press and the day shot`);
    else if (/settle\(page,\s*1500\)/.test(seg)) f2.push(`${dayFn.name}: a fixed 1500 ms settle still precedes the day shot`);
    if (!/state\s*===\s*'rows'/.test(dayFn.body)) f2.push(`${dayFn.name}: rows are not read only on state 'rows'`);
  }
  if (!tl) f2.push('no walkTimeline');
  else {
    const segN = between(tl.body, /bars\.last\(\)|\[data-day-bar\]/, /checks\(page,\s*`\$\{sec\}-timeline-day`/);
    if (!segN || !/waitForDayState\(page,/.test(segN)) f2.push('walkTimeline: the newest-day shot is not preceded by waitForDayState');
    else if (/settle\(page,\s*1500\)/.test(segN)) f2.push('walkTimeline: a fixed 1500 ms settle still precedes the newest-day shot');
    const segE = between(tl.body, /\[data-timeline-event\]/, /checks\(page,\s*`\$\{sec\}-timeline-event`/);
    if (!segE || !/waitForDayState\(page,/.test(segE)) f2.push('walkTimeline: the event shot is not preceded by waitForDayState');
    else if (/settle\(page,\s*1500\)/.test(segE)) f2.push('walkTimeline: a fixed 1500 ms settle still precedes the event shot');
  }
  const a2 = f2.length === 0;
  const a2d = a2 ? `the --day step (${dayFn.name}), the newest day and the event open each wait for the day's state before the shot; rows read only on 'rows'` : `${f2.length} failing; first: ${f2[0]}`;

  // ---- arm 3: record ----------------------------------------------------------------------------------------------------
  const f3 = [];
  const pushes = [...src.matchAll(/timelineDays\.push\(\{([^}]*)\}\)/g)].map((m) => m[1]);
  for (const via of ['day', 'newest', 'event']) {
    if (!pushes.some((p) => new RegExp(`via:\\s*'${via}'`).test(p) && /\bstate\b/.test(p) && /\bwaited_ms\b/.test(p))) f3.push(`no timelineDays record via '${via}' carrying state and waited_ms`);
  }
  const w = /if\s*\(([^)]*)\)\s*writeFileSync\(path\.join\(OUT,\s*'timeline-days\.json'\)/.exec(src);
  if (!w) f3.push('timeline-days.json is not written');
  else if (/opt\.days/.test(w[1]) || !/timelineDays\.length/.test(w[1])) f3.push(`timeline-days.json is written under "${w[1].trim()}", not whenever timelineDays is non-empty`);
  const a3 = f3.length === 0;
  const a3d = a3 ? `${pushes.length} timelineDays record site(s) carrying via, state and waited_ms; written whenever non-empty` : `${f3.length} failing; first: ${f3[0]}`;

  const arms = [
    ['the day wait resolves on the page\'s state, and a held route reads "ceiling"', a1, a1d],
    ['every day and event shot waits for the day\'s state, not a fixed settle', a2, a2d],
    ['every opened day is recorded with its state and wait in timeline-days.json', a3, a3d],
  ];
  let pass = 0;
  for (const [name, ok, detail] of arms) { if (ok) pass += 1; console.log(`${ok ? 'ARM PASS' : 'ARM FAIL'} ${name} :: ${detail}`); }
  console.log(`WALKER WAITS FOR DAY STATE: ${pass} of ${arms.length} arms`);
  process.exit(pass === arms.length ? 0 : 1);
})();
