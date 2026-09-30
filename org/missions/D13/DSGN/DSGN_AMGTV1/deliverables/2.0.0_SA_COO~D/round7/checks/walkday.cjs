/**
 * walkday.cjs -- DSGN_AMGTV1 round 7, AV-s-3 (walker half): THE WALK OPENS A NAMED DAY BY ITS DATE AND RECORDS ITS ARTICLES IN
 * THE ORDER THE PAGE LISTS THEM (round-6 analysis s.4 item 3: "the walker opens 992 HK 2026-08-13 (2 articles) and grades
 * 'strongest first' on pixels"; AMGT_HARVST FWD-5).
 *
 * Usage (repo root): node <this file>
 * A STATIC read of .claude/skills/ui-walk/walk.mjs (a live walk needs the walker account, which no check arms; the issuer's
 * round-7 walk is its live run, with --day "992 HK=2026-08-13"). The issuer-only CHECK_SRC_OVERRIDE may name
 * ".claude/skills/ui-walk/walk.mjs=<file>" to prove the check can pass; a worker never sets it.
 * Arms:
 *   1  walk.mjs parses (`node --check`) and takes a repeatable `--day "<security>=<YYYY-MM-DD>"` option
 *   2  the timeline function presses the bar for THAT date (a `[data-day-bar="${date}"]` selector), records a measured finding
 *      "timeline:day-not-found" when the bar is missing, and runs a checks step labelled with "timeline-day-" and the date --
 *      so the sign-in guard and the screenshot run on it
 *   3  the day's article rows are read from the page in their listed order and written to `timeline-days.json` in the walk's
 *      output folder (beside findings.json), so the CVO reads the order the page shows
 * Prints one line per arm and "WALK OPENS A DAY BY DATE: <k> of 3 arms"; exit 0 only at 3 of 3.
 */
const fs = require('fs');
const path = require('path');
const { spawnSync } = require('child_process');
const REL = '.claude/skills/ui-walk/walk.mjs';
const ov = (process.env.CHECK_SRC_OVERRIDE || '').split(';').filter(Boolean).map((p) => [p.slice(0, p.indexOf('=')), p.slice(p.indexOf('=') + 1)]).find(([k]) => k === REL);
const file = ov ? ov[1] : path.join(process.cwd(), REL);
if (!fs.existsSync(file)) {
  console.log('WALK OPENS A DAY BY DATE: 0 of 3 arms (walk.mjs absent: ' + file + ')');
  process.exit(1);
}
const src = fs.readFileSync(file, 'utf8');
const parse = spawnSync(process.execPath, ['--check', file], { encoding: 'utf8', timeout: 60000 });
const fns = [];
const heads = [...src.matchAll(/^(?:async\s+)?function\s+([A-Za-z0-9_]+)\s*\(/gm)].map((m) => ({ name: m[1], at: m.index }));
heads.forEach((h, i) => fns.push({ name: h.name, body: src.slice(h.at, i + 1 < heads.length ? heads[i + 1].at : src.length) }));

const dayOpt = /'--day'/.test(src) && /opt\.days/.test(src);
const a1 = parse.status === 0 && dayOpt;
const a1d = `node --check rc=${parse.status}; --day option ${dayOpt}`;

const tl = fns.find((f) => /data-day-bar="\$\{date\}"|data-day-bar=\\?"\$\{/.test(f.body));
const a2 = !!tl && /timeline:day-not-found/.test(tl.body) && /timeline-day-\$\{date\}|timeline-day-`|`\$\{sec\}-timeline-day-\$\{date\}`/.test(tl.body) && /checks\(page,/.test(tl.body);
const a2d = `function pressing a bar by date: ${tl ? tl.name : 'none'}; day-not-found finding ${tl ? /timeline:day-not-found/.test(tl.body) : false}; labelled checks step ${tl ? /timeline-day-/.test(tl.body) : false}`;

const a3 = /timeline-days\.json/.test(src) && /writeFileSync\([^)]*timeline-days/.test(src) && !!tl && /data-timeline-selected-day[^'"`]*li|allInnerTexts/.test(tl.body);
const a3d = `timeline-days.json written ${/writeFileSync\([^)]*timeline-days/.test(src)}; article rows read in page order ${!!tl && /allInnerTexts/.test(tl.body)}`;

const arms = [
  ['walk.mjs parses and takes --day "<security>=<YYYY-MM-DD>"', a1, a1d],
  ['the walk presses THAT date\'s bar (or records day-not-found) through a labelled checks step', a2, a2d],
  ['the day\'s article rows are recorded in page order to timeline-days.json', a3, a3d],
];
let pass = 0;
for (const [name, ok, detail] of arms) {
  if (ok) pass += 1;
  console.log(`${ok ? 'ARM PASS' : 'ARM FAIL'} ${name} :: ${detail}`);
}
console.log(`WALK OPENS A DAY BY DATE: ${pass} of ${arms.length} arms`);
process.exit(pass === arms.length ? 0 : 1);
