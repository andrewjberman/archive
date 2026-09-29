/**
 * walkthread.cjs -- DSGN_AMGTV1 round 6, AV-u-4: THE WALK THAT GRADES FWD-1, FWD-2, FWD-5 (and AMGT_HARVST's FWD-5 / FWD-6) BY
 * NAME (round-5 analysis s.4 item 4; CTO~Z msg 26751, AMGT_HARVST ROUND_ANALYSIS.round19.md ruling 5).
 *
 * Usage (repo root): node <this file>
 * A STATIC read of .claude/skills/ui-walk/walk.mjs (a live walk needs the walker account, which no check arms; the issuer's
 * round-6 walk is its live run). The issuer-only CHECK_SRC_OVERRIDE may name ".claude/skills/ui-walk/walk.mjs=<file>" to
 * prove the check can pass; a worker never sets it.
 * Arms:
 *   1  FWD-1's thread, hop by hop, picked BY NAME: walk.mjs parses (`node --check`); it takes `--thread "<company name>"`
 *      (into opt.thread); one function carries the thread -- it finds the lead-list row by the company name the row prints
 *      (a `[data-row-lead]` read), never through "Search any ticker", and runs FIVE labelled steps thread-1 .. thread-5 (the
 *      list with the row found; the name opened, header as cards; the Financials card's window; the Thesis tab; the
 *      Recommendation card's window), each through `checks(page, ...)` so the sign-in guard runs on every hop
 *   2  FWD-2's four lists, read: on each List view the walk reads every row's `data-row-lead`, `data-row-ticker` and
 *      `data-row-name-state` (plus the row's visible text) and writes them to `lead-lists.json` in the walk's output folder
 *   3  the timeline's states (DSGN FWD-5; HARVST FWD-5 / FWD-6): for each opened name the walk presses one day on the
 *      timeline (a `[data-day-bar]`), runs a checks step labelled with "timeline-day", and looks for an event span
 *      (`[data-timeline-event]`): it opens the first when one exists (a step labelled with "timeline-event"), else records a
 *      measured finding with check "timeline:no-event-element" -- so an absent event layer is a finding, never a silent pass
 * Prints one line per arm and "WALK GRADES BY NAME: <k> of 3 arms"; exit 0 only at 3 of 3.
 */
const fs = require('fs');
const path = require('path');
const { spawnSync } = require('child_process');
const REL = '.claude/skills/ui-walk/walk.mjs';
const ov = (process.env.CHECK_SRC_OVERRIDE || '').split(';').filter(Boolean).map((p) => [p.slice(0, p.indexOf('=')), p.slice(p.indexOf('=') + 1)]).find(([k]) => k === REL);
const file = ov ? ov[1] : path.join(process.cwd(), REL);
if (!fs.existsSync(file)) {
  console.log('WALK GRADES BY NAME: 0 of 3 arms (walk.mjs absent: ' + file + ')');
  process.exit(1);
}
const src = fs.readFileSync(file, 'utf8');
const parse = spawnSync(process.execPath, ['--check', file], { encoding: 'utf8', timeout: 60000 });

// the body of each top-level function (from its `function` line to the next top-level function or EOF)
const fns = [];
const re = /^(?:async\s+)?function\s+([A-Za-z0-9_]+)\s*\(/gm;
const heads = [...src.matchAll(re)].map((m) => ({ name: m[1], at: m.index }));
heads.forEach((h, i) => fns.push({ name: h.name, body: src.slice(h.at, i + 1 < heads.length ? heads[i + 1].at : src.length) }));

// arm 1
const optThread = /--thread['"]\)?\s*\)?\s*opt\.thread\s*=|opt\.thread\s*=\s*argv\[/.test(src) || (/'--thread'/.test(src) && /opt\.thread/.test(src));
const thread = fns.find((f) => /thread-1/.test(f.body) && /\[data-row-lead\]|data-row-lead/.test(f.body));
const hops = thread ? [1, 2, 3, 4, 5].filter((n) => new RegExp('thread-' + n + '\\b').test(thread.body)) : [];
const checksIn = thread ? (thread.body.match(/checks\(page,/g) || []).length : 0;
const noSearch = thread ? !/Search any ticker/.test(thread.body) : false;
const a1 = parse.status === 0 && optThread && !!thread && hops.length === 5 && checksIn >= 5 && noSearch;
const a1d = `node --check rc=${parse.status}; --thread option ${optThread}; thread function ${thread ? thread.name : 'none'}; hops ${JSON.stringify(hops)}; checks() calls in it ${checksIn}; no ticker search ${noSearch}`;

// arm 2
const lists = /lead-lists\.json/.test(src) && /data-row-lead/.test(src) && /data-row-ticker/.test(src) && /data-row-name-state/.test(src) && /writeFileSync\([^)]*lead-lists|lead-lists[\s\S]{0,200}writeFileSync|writeFileSync[\s\S]{0,200}lead-lists/.test(src);
const a2 = parse.status === 0 && lists;
const a2d = `lead-lists.json ${/lead-lists\.json/.test(src)}; reads data-row-lead ${/data-row-lead/.test(src)}, data-row-ticker ${/data-row-ticker/.test(src)}, data-row-name-state ${/data-row-name-state/.test(src)}; written ${lists}`;

// arm 3
const tl = fns.find((f) => /data-day-bar/.test(f.body));
const dayStep = tl ? /timeline-day/.test(tl.body) && /\.click\(/.test(tl.body) && /checks\(page,/.test(tl.body) : false;
const eventStep = tl ? /data-timeline-event/.test(tl.body) && /timeline-event/.test(tl.body.replace(/data-timeline-event/g, '')) && /timeline:no-event-element/.test(tl.body) : false;
const called = tl ? new RegExp('\\b' + tl.name + '\\(page').test(src.replace(tl.body, '')) : false;
const a3 = parse.status === 0 && !!tl && dayStep && eventStep && called;
const a3d = `timeline function ${tl ? tl.name : 'none'}; day pressed + checked ${dayStep}; event opened or "timeline:no-event-element" recorded ${eventStep}; called from the walk ${called}`;

const arms = [
  ["FWD-1's thread, hop by hop, picked by name", a1, a1d],
  ["FWD-2's four lists read into lead-lists.json", a2, a2d],
  ['the timeline: a day opened, an event opened or its absence recorded', a3, a3d],
];
let pass = 0;
for (const [name, ok, detail] of arms) {
  if (ok) pass += 1;
  console.log(`${ok ? 'ARM PASS' : 'ARM FAIL'} ${name} :: ${detail}`);
}
console.log(`WALK GRADES BY NAME: ${pass} of ${arms.length} arms`);
process.exit(pass === arms.length ? 0 : 1);
