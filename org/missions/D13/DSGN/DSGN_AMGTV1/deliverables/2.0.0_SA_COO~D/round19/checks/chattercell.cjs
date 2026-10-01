/**
 * chattercell.cjs -- DSGN_AMGTV1 round 19, AV-j-1 (issuer 2.0.0_SA_COO~D): THE HEADER'S CHATTER CELL READS THE MONTHLY COUNT.
 *
 * Usage (repo root): node <this file>        (portal/ under the cwd is the checkout under test)
 * CTO ruling msg 27768: the selected-name header's chatter cell read the legacy ranking point ("TRENDING (CHATTER) #1 | 0/100" --
 * the dead input, read as "no chatter"). Ruled: the cell shows the name's collected count for the latest month from the monthly
 * route ("Collected this month: 20"), or the designed absent sentence when the name has no count that month; no legacy ranking read
 * anywhere on the face.
 * THE CONTRACT the worker builds to: the chatter cell of IdentityHeader (SecurityOverlay.tsx) carries data-header-reading="chatter";
 * its visible text holds the count (an integer) and the word "collected" when the monthly payload's latest month has a count for
 * this security_key, and otherwise ONE designed sentence with "collected" in it and no digit; never "#<rank>", never "/100", never
 * "Trending". Its data comes from useCollectedChatter (the same read as the bubbles).
 * Inputs (built here, CONTRACT s.1 shape): months [2026-09, 2026-10], partial [2026-10]; payload A has BA_US_Equity with 20 collected
 * in 2026-10; payload B has BA_US_Equity with only 2026-09 (no count in the latest month). The overlay: round15/fixtures/
 * r15c.overlay.BA_US_Equity.json. Render: round15/checks/_load.cjs with round15 headerread.cjs's stubs; the hook stub returns the
 * payload itself (the loader wraps it as { data }).
 * Arms:
 *   1  THE CHECKOUT on A: the [data-header-reading="chatter"] cell prints 20 with "collected", no "#", no "/100", no "Trending"; on B:
 *      one designed sentence with "collected", no digit; with the read unserved: no count, no "/100".
 *   2  NEGATIVE: the pinned base SecurityOverlay.tsx (portal 4c02f293; CHATTERCELL_BASE overrides) carries no
 *      data-header-reading="chatter" and still prints "/100".
 *   3  PLANTED: a legacy "#1 | 0/100" cell (LEGACY), a count of 19 for served 20 (VALUE), an absent cell printing "0" (ABSENT) --
 *      each rejected; correct cells pass.
 * Prints one line per arm and "THE HEADER CHATTER CELL READS THE MONTHLY COUNT: <k> of 3 arms"; exit 0 only at 3 of 3. Seconds.
 */
const fs = require('fs');
const path = require('path');
const { spawnSync } = require('child_process');

const ROOT = process.cwd();
const R15 = path.join(__dirname, '..', '..', 'round15');
const PIN = process.env.CHATTERCELL_BASE || '4c02f293';
const SA = 'src/pages/SecurityAnalysis/';
const rd = (n) => { const x = JSON.parse(fs.readFileSync(path.join(R15, 'fixtures', n), 'utf8')); return x && x.payload && x._capture_note ? x.payload : x; };
const OV = rd('r15c.overlay.BA_US_Equity.json');
const KEY = 'BA_US_Equity';
const base = { as_of: '2026-09-30', source: 'harvest gold chatter_daily', months: ['2026-09', '2026-10'], partial_months: ['2026-10'] };
const A = { ...base, rows: [{ security_key: KEY, display_name: 'The Boeing Co', by_month: { '2026-09': { collected: 7, by_publisher: { sa: 7 } }, '2026-10': { collected: 20, by_publisher: { sa: 14, wsj: 6 } } } },
  { security_key: 'VLO_US_Equity', display_name: 'Valero Energy Corp', by_month: { '2026-10': { collected: 3, by_publisher: { sa: 3 } } } }] };
const B = { ...base, rows: [{ security_key: KEY, display_name: 'The Boeing Co', by_month: { '2026-09': { collected: 7, by_publisher: { sa: 7 } } } },
  { security_key: 'VLO_US_Equity', display_name: 'Valero Energy Corp', by_month: { '2026-10': { collected: 3, by_publisher: { sa: 3 } } } }] };
const textOf = (h) => h.replace(/<[^>]*>/g, ' ').replace(/&amp;/g, '&').replace(/&#x27;/g, "'").replace(/&quot;/g, '"').replace(/\s+/g, ' ').trim();
function cell(html) {
  const at = html.indexOf('data-header-reading="chatter"');
  if (at < 0) return null;
  const open = html.lastIndexOf('<', at);
  const tag = /^<([a-zA-Z0-9]+)/.exec(html.slice(open))[1];
  const start = html.indexOf('>', at) + 1;
  let depth = 1; const re = new RegExp('<(/?)' + tag + '\\b[^>]*?(/?)>', 'g'); re.lastIndex = start; let m;
  while ((m = re.exec(html)) !== null) { if (m[2] === '/') continue; depth += m[1] === '/' ? -1 : 1; if (depth === 0) return textOf(html.slice(start, m.index)); }
  return textOf(html.slice(start));
}
function cellFaults(t, want) {
  const f = [];
  if (t === null) return ['MISSING: no [data-header-reading="chatter"] cell'];
  if (/#\d|\/100|\btrending\b/i.test(t)) f.push(`LEGACY: the cell prints a ranking read ("${t.slice(0, 80)}")`);
  if (want === 'unserved') { if (/\d/.test(t.replace(/\b20\d\d\b/g, ''))) f.push(`ABSENT: the unserved cell prints a number ("${t.slice(0, 80)}")`); return f; }
  if (!/collected/i.test(t)) f.push(`WORDS: the cell does not say "collected" ("${t.slice(0, 80)}")`);
  if (typeof want === 'number') {
    const nums = (t.match(/\b\d+\b/g) || []).map(Number).filter((n) => n < 1900);
    if (!nums.includes(want)) f.push(`VALUE: the cell does not print ${want} ("${t.slice(0, 80)}")`);
    if (nums.some((n) => n !== want)) f.push(`VALUE: the cell prints another number than ${want} ("${t.slice(0, 80)}")`);
  } else if (/\d/.test(t.replace(/\b20\d\d\b/g, ''))) f.push(`ABSENT: the absent cell prints a number ("${t.slice(0, 80)}")`);
  return f;
}

let L;
function render(payload) {
  if (!L) {
    L = require(path.join(R15, 'checks', '_load.cjs'));
    const api = { __esModule: true, apiRequest: () => Promise.resolve(undefined) };
    L.stubSource('src/api/api-client.ts', api);
    L.stubSource('src/api/api-client', api);
    L.stubSource('@tanstack/react-query', { __esModule: true,
      useQuery: () => ({ isLoading: false, isError: false, error: null, data: undefined, refetch: () => {} }),
      useQueryClient: () => ({ invalidateQueries: () => {}, getQueryData: () => undefined }) });
  }
  L.hookState.impl = { useCollectedChatter: () => payload, useThesisBundle: () => undefined, usePeerSet: () => undefined, useManagement: () => undefined };
  const m = L.source(SA + 'components/SecurityOverlay.tsx');
  return L.render(m.IdentityHeader || m.SecurityOverlay, { bundle: OV, onBack: () => {}, onRefresh: () => {} });
}

const f1 = [];
try {
  f1.push(...cellFaults(cell(render(A)), 20).map((x) => 'A ' + x));
  f1.push(...cellFaults(cell(render(B)), 'absent').map((x) => 'B ' + x));
  f1.push(...cellFaults(cell(render(undefined)), 'unserved').map((x) => 'UNSERVED ' + x));
} catch (e) { f1.push('RENDER: ' + String(e.message).split('\n')[0]); }
const a1 = f1.length === 0;

const f2 = [];
const s = spawnSync('git', ['-C', path.join(ROOT, 'portal'), 'show', `${PIN}:${SA}components/SecurityOverlay.tsx`], { encoding: 'utf8', maxBuffer: 1 << 24 });
if (s.status !== 0 || !s.stdout) f2.push(`INPUT MISSING: git show ${PIN} rc=${s.status}`);
else if (/data-header-reading="chatter"/.test(s.stdout) && !/\/100/.test(s.stdout)) f2.push(`the base at ${PIN} already carries the monthly chatter cell -- the check cannot tell base from fix`);
const a2 = f2.length === 0;

const f3 = [];
const C = (t) => `<div data-header-reading="chatter"><div>Chatter</div><div>${t}</div></div>`;
const goods = [[C('Collected this month: 20'), 20], [C('No articles collected for this name this month.'), 'absent']];
for (const [h, w] of goods) if (cellFaults(cell(h), w).length) f3.push(`a correct cell is rejected: ${cellFaults(cell(h), w)[0]}`);
const M = [['legacy', C('#1 | 0/100'), 20, 'LEGACY'], ['wrong count', C('Collected this month: 19'), 20, 'VALUE'], ['absent prints 0', C('Collected this month: 0'), 'absent', 'ABSENT']];
const caught = [];
for (const [n, h, w, cls] of M) { if (cellFaults(cell(h), w).some((x) => x.startsWith(cls + ':'))) caught.push(n); else f3.push(`mutant "${n}" not rejected as ${cls}`); }
const a3 = f3.length === 0;

const arms = [
  ['the checkout: the chatter cell prints the monthly count (20, "collected"), a designed absent sentence, nothing when unserved, no ranking read', a1, a1 ? '0 faults (A, B, unserved)' : `${f1.length} faults; first: ${f1[0]}`],
  [`NEGATIVE: the base SecurityOverlay.tsx (${PIN}) has no monthly chatter cell and prints "/100"`, a2, a2 ? 'base carries the legacy cell' : f2[0]],
  ['PLANTED: a legacy cell, a wrong count and an absent cell printing 0 are rejected; correct cells pass', a3, a3 ? `${caught.length} of ${M.length} rejected` : f3[0]],
];
let pass = 0;
for (const [n, ok, d] of arms) { if (ok) pass += 1; console.log(`${ok ? 'ARM PASS' : 'ARM FAIL'} ${n} :: ${d}`); }
console.log(`THE HEADER CHATTER CELL READS THE MONTHLY COUNT: ${pass} of 3 arms`);
process.exit(pass === 3 ? 0 : 1);
