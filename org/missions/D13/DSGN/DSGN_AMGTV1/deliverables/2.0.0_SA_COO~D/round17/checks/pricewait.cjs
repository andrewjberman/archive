/**
 * pricewait.cjs -- DSGN_AMGTV1 round 17, AV-h-1 (issuer 2.0.0_SA_COO~D): THE WALKER WAITS FOR THE PRICE BARS.
 *
 * Usage (repo root): node <this file>
 * CTO round-16 analysis ruling 1: the live price face is the one unproven demo face; the walk must WAIT on `[data-price-bar]` up to
 * 30 s after the route answers. Walk 20261001T090446Z settled 1.5 s after the Price click (walk.mjs settle) and read 0 bars.
 * Arms (a static read of `.claude/skills/ui-walk/walk.mjs` in the checkout under test; nothing is run):
 *   1  the checkout: `node --check` passes; the Price step waits for `[data-price-bar]` (a waitForSelector / locator.waitFor /
 *      waitForFunction naming `data-price-bar`) with a timeout of at least 30000 ms BEFORE it reads the bars or takes the Price shot;
 *      a wait that ends with no bar is recorded as a finding (a check name containing "price" and "wait" or "no-bars"), never
 *      silently; and the walk's chatter-label step flags a sized bubble whose visible label equals its `data-bubble` key (a check
 *      name containing "raw-key" or "label").
 *   2  the negative: the same predicates FAIL on the base walk.mjs (git show e41e28e641:.claude/skills/ui-walk/walk.mjs, round 16's
 *      AV-g-1; PRICEWAIT_BASE overrides the pin)
 *   3  planted control: the checkout's file with the wait's timeout cut to 1500 is rejected
 * Prints one line per arm and "THE WALKER WAITS FOR THE PRICE BARS: <k> of 3 arms"; exit 0 only at 3 of 3. Under 1 second.
 */
const fs = require('fs');
const os = require('os');
const path = require('path');
const { spawnSync } = require('child_process');

const ROOT = process.cwd();
const REL = '.claude/skills/ui-walk/walk.mjs';
const PIN = process.env.PRICEWAIT_BASE || 'e41e28e641';

function faults(src) {
  const f = [];
  const s = src.replace(/\/\/[^\n]*/g, '').replace(/\/\*[\s\S]*?\*\//g, '');
  const waitRe = /(waitForSelector|waitFor|waitForFunction)\s*\([^;]{0,200}data-price-bar[^;]{0,200}|data-price-bar[^;]{0,200}\.waitFor\s*\([^;]{0,120}/g;
  const waits = s.match(waitRe) || [];
  if (!waits.length) f.push('WAIT: the walk never waits for [data-price-bar]');
  else {
    const ok = waits.some((w) => {
      const n = (w.match(/timeout\s*:\s*([0-9_]+)/) || [])[1];
      return n && Number(n.replace(/_/g, '')) >= 30000;
    }) || /PRICE_WAIT_MS\s*=\s*([0-9_]+)/.test(s) && Number(s.match(/PRICE_WAIT_MS\s*=\s*([0-9_]+)/)[1].replace(/_/g, '')) >= 30000 && waits.some((w) => /PRICE_WAIT_MS/.test(w));
    if (!ok) f.push('TIMEOUT: no wait for [data-price-bar] carries a timeout of at least 30000 ms');
  }
  if (!/check\s*:\s*['"`][^'"`]*price[^'"`]*(wait|no-bars)[^'"`]*['"`]/i.test(s)) f.push('SILENT: a wait that ends with no bar is not recorded as a price wait/no-bars finding');
  if (!/check\s*:\s*['"`][^'"`]*(raw-key|label)[^'"`]*['"`]/i.test(s)) f.push('LABELS: the chatter step does not flag a bubble label equal to its key');
  return f;
}

const file = path.join(ROOT, REL);
const f1 = [];
let src = '';
try { src = fs.readFileSync(file, 'utf8'); } catch (e) { f1.push(`MISSING: ${REL}`); }
if (src) {
  const chk = spawnSync(process.execPath, ['--check', file], { encoding: 'utf8' });
  if (chk.status !== 0) f1.push(`SYNTAX: node --check rc=${chk.status}`);
  f1.push(...faults(src));
}
const a1 = f1.length === 0;

const f2 = [];
const base = spawnSync('git', ['show', `${PIN}:${REL}`], { cwd: ROOT, encoding: 'utf8', maxBuffer: 1 << 26 });
if (base.status !== 0 || !base.stdout) f2.push(`INPUT MISSING: git show ${PIN}:${REL} rc=${base.status}`);
const bf = base.stdout ? faults(base.stdout) : [];
if (!f2.length && !bf.length) f2.push('the base walk.mjs passes arm 1 -- the check cannot fail');
const a2 = f2.length === 0;

const f3 = [];
let mf = [];
if (src) {
  const mutant = src.replace(/(timeout\s*:\s*)([0-9_]{5,})/g, (m, a, n) => (Number(n.replace(/_/g, '')) >= 30000 ? `${a}1500` : m)).replace(/(PRICE_WAIT_MS\s*=\s*)([0-9_]+)/, '$11500');
  const tmp = path.join(fs.mkdtempSync(path.join(os.tmpdir(), 'pricewait-')), 'walk.mjs');
  fs.writeFileSync(tmp, mutant);
  mf = faults(fs.readFileSync(tmp, 'utf8'));
  if (!mf.some((x) => x.startsWith('TIMEOUT:') || x.startsWith('WAIT:'))) f3.push('a 1500 ms wait was not rejected');
} else f3.push('no checkout file to mutate');
const a3 = f3.length === 0;

const arms = [
  ['the checkout waits >= 30 s for [data-price-bar], records a no-bars finding, flags raw-key bubble labels', a1, a1 ? '0 faults; node --check OK' : `${f1.length} fault(s); first: ${f1[0]}`],
  [`NEGATIVE: the base walk.mjs (${PIN}) fails arm 1`, a2, a2 ? `${bf.length} fault(s) at base; first: ${bf[0]}` : f2[0]],
  ['PLANTED: the wait cut to 1500 ms is rejected', a3, a3 ? `rejected (${mf[0]})` : f3[0]],
];
let pass = 0;
for (const [name, ok, d] of arms) { if (ok) pass += 1; console.log(`${ok ? 'ARM PASS' : 'ARM FAIL'} ${name} :: ${d}`); }
console.log(`THE WALKER WAITS FOR THE PRICE BARS: ${pass} of 3 arms`);
process.exit(pass === 3 ? 0 : 1);
