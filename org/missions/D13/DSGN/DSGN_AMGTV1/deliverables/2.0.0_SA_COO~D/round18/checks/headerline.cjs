/**
 * headerline.cjs -- DSGN_AMGTV1 round 18, AV-i-2 (issuer 2.0.0_SA_COO~D): THE HEADER'S CHATTER LINE READS THE MONTHLY ROUTE.
 *
 * Usage (repo root): node <this file>        (portal/ under the cwd is the checkout under test)
 * CTO msg 27762 (from AMGT_CORPUS ADJUDICATION_v36): the selected-name header's readings line printed "chatter: ranked October
 * 1st, 2026 (1 names)" -- the legacy chatter ranking (the dead input FWD-21's bubbles replace). Ruled: the line reads the monthly
 * route ("N of 95 covered names collected this month", matching the bubble denominator), the plural correct. Presentation only.
 * Inputs: round15/fixtures/r15c.overlay.BA_US_Equity.json (the served overlay); round15/fixtures/r15a.collected.chatter.json (the
 * CONTRACT s.1 payload: 22 rows; latest month 2026-10 partial with 9 names collected).
 * Render: round15/checks/_load.cjs; IdentityHeader with the page hooks stubbed (useCollectedChatter -> the r15a payload).
 * Arms:
 *   1  THE CHECKOUT: the [data-axis-footnote] text holds "9 of 22 covered names" and "collected"; it holds no "chatter: ranked" and
 *      no "(N names)" with N = 1 ("1 names"); GenerationCaption with generation_row_count 1 prints "1 name", never "1 names", and
 *      with 32 prints "32 names". With the monthly read unserved (useCollectedChatter undefined), the footnote prints no chatter
 *      count and no "chatter: ranked" (it says nothing about chatter or says it is not available yet).
 *   2  NEGATIVE: the base sources (portal 788afb2e: SecurityOverlay.tsx, GenerationCaption.tsx, via git show) still render the
 *      legacy "chatter" GenerationCaption in the footnote and the "names)" plural without a singular branch; HEADERLINE_BASE overrides.
 *   3  PLANTED: synthetic footnotes -- "chatter: ranked ... (1 names)" (LEGACY), "9 of 22 covered names" missing (COUNT), "1 names"
 *      (PLURAL) -- each rejected; a correct footnote passes.
 * Prints one line per arm and "THE HEADER CHATTER LINE READS THE MONTHLY ROUTE: <k> of 3 arms"; exit 0 only at 3 of 3. Seconds.
 */
const fs = require('fs');
const path = require('path');
const { spawnSync } = require('child_process');

const ROOT = process.cwd();
const R15 = path.join(__dirname, '..', '..', 'round15');
const PIN = process.env.HEADERLINE_BASE || '788afb2e';
const SA = 'src/pages/SecurityAnalysis/';
const rd = (n) => { const x = JSON.parse(fs.readFileSync(path.join(R15, 'fixtures', n), 'utf8')); return x && x.payload && x._capture_note ? x.payload : x; };
const OV = rd('r15c.overlay.BA_US_Equity.json');
const CH = rd('r15a.collected.chatter.json');
const LATEST = CH.months[CH.months.length - 1];
const K = CH.rows.filter((r) => r.by_month && r.by_month[LATEST]).length;
const N = CH.rows.length;
const textOf = (h) => h.replace(/<[^>]*>/g, ' ').replace(/&amp;/g, '&').replace(/&#x27;/g, "'").replace(/&quot;/g, '"').replace(/\s+/g, ' ').trim();
function foot(html) {
  const at = html.indexOf('data-axis-footnote=');
  if (at < 0) return null;
  const open = html.lastIndexOf('<', at);
  const tag = /^<([a-zA-Z0-9]+)/.exec(html.slice(open))[1];
  const start = html.indexOf('>', at) + 1;
  let depth = 1; const re = new RegExp('<(/?)' + tag + '\\b[^>]*?(/?)>', 'g'); re.lastIndex = start; let m;
  while ((m = re.exec(html)) !== null) { if (m[2] === '/') continue; depth += m[1] === '/' ? -1 : 1; if (depth === 0) return textOf(html.slice(start, m.index)); }
  return textOf(html.slice(start));
}
function footFaults(t, served) {
  const f = [];
  if (t === null) return ['MISSING: no [data-axis-footnote]'];
  if (/chatter:\s*ranked/i.test(t)) f.push(`LEGACY: the footnote still prints the chatter ranking caption ("${t.slice(0, 90)}")`);
  if (/\b1 names\b/.test(t)) f.push(`PLURAL: "1 names" in "${t.slice(0, 90)}"`);
  if (served) {
    if (!t.includes(`${K} of ${N} covered names`) || !/collected/i.test(t)) f.push(`COUNT: the footnote does not print "${K} of ${N} covered names ... collected" ("${t.slice(0, 120)}")`);
  } else if (/\d+ of \d+ covered names/.test(t)) f.push(`COUNT: an unserved monthly read still prints a count ("${t.slice(0, 90)}")`);
  return f;
}

let L;
function render(collected) {
  if (!L) {
    L = require(path.join(R15, 'checks', '_load.cjs'));
    // the stubs round15/checks/headerread.cjs sets (the api client reads import.meta; react-query is not mounted)
    const api = { __esModule: true, apiRequest: () => Promise.resolve(undefined) };
    L.stubSource('src/api/api-client.ts', api);
    L.stubSource('src/api/api-client', api);
    L.stubSource('@tanstack/react-query', { __esModule: true,
      useQuery: () => ({ isLoading: false, isError: false, error: null, data: undefined, refetch: () => {} }),
      useQueryClient: () => ({ invalidateQueries: () => {}, getQueryData: () => undefined }) });
  }
  L.hookState.impl = { useCollectedChatter: () => (collected ? { data: collected, isLoading: false, isError: false } : { data: undefined, isLoading: false, isError: true, error: new Error('404') }),
    useThesisBundle: () => undefined, usePeerSet: () => undefined, useManagement: () => undefined };
  const m = L.source(SA + 'components/SecurityOverlay.tsx');
  return L.render(m.IdentityHeader || m.SecurityOverlay, { bundle: OV, onBack: () => {}, onRefresh: () => {} });
}
function captionText(n) {
  const m = L.source(SA + 'components/GenerationCaption.tsx');
  const fn = m.generationCaptionWords || m.generationCaptionText;
  return fn ? String(fn({ generation_row_count: n, generation_state: 'COMMITTED', as_of_date: '2026-09-29', source: 'bloomberg' })) : '';
}

// arm 1
const f1 = [];
try {
  f1.push(...footFaults(foot(render(CH)), true));
  f1.push(...footFaults(foot(render(null)), false).map((x) => 'UNSERVED ' + x));
  const one = captionText(1); const many = captionText(32);
  if (/\b1 names\b/.test(one)) f1.push(`PLURAL: GenerationCaption with 1 row prints "${one}"`);
  if (!/\b32 names\b/.test(many) && /names?\b/.test(many)) f1.push(`PLURAL: GenerationCaption with 32 rows prints "${many}"`);
} catch (e) { f1.push('RENDER: ' + String(e.message).split('\n')[0]); }
const a1 = f1.length === 0;

// arm 2
const f2 = [];
const show = (p) => spawnSync('git', ['-C', path.join(ROOT, 'portal'), 'show', `${PIN}:${p}`], { encoding: 'utf8', maxBuffer: 1 << 24 });
const so = show('src/pages/SecurityAnalysis/components/SecurityOverlay.tsx');
const gc = show('src/pages/SecurityAnalysis/components/GenerationCaption.tsx');
if (so.status !== 0 || gc.status !== 0) f2.push(`INPUT MISSING: git show at ${PIN}`);
else {
  const legacy = /GenerationCaption[^>]*label="chatter"/.test(so.stdout);
  const pluralBug = /names\)/.test(gc.stdout) && !/=== 1 \? ['"`]name/.test(gc.stdout);
  if (!legacy && !pluralBug) f2.push(`the base at ${PIN} has neither the legacy chatter caption nor the plural bug -- the check cannot tell base from fix`);
}
const a2 = f2.length === 0;

// arm 3
const f3 = [];
const good = `Readings of September 30th, 2026. chatter: ${K} of ${N} covered names collected this month; price: ranked September 29th, 2026 from Bloomberg (32 names)`;
if (footFaults(good, true).length) f3.push(`the correct footnote is rejected: ${footFaults(good, true)[0]}`);
const M = [
  ['legacy caption', 'Readings of September 30th, 2026. chatter: ranked October 1st, 2026 (1 names) price: ranked (32 names)', 'LEGACY'],
  ['no monthly count', 'Readings of September 30th, 2026. price: ranked (32 names)', 'COUNT'],
  ['plural', `chatter: ${K} of ${N} covered names collected this month; price: ranked (1 names)`, 'PLURAL'],
];
const caught = [];
for (const [n, t, cls] of M) { if (footFaults(t, true).some((x) => x.startsWith(cls + ':'))) caught.push(n); else f3.push(`mutant "${n}" not rejected as ${cls}`); }
const a3 = f3.length === 0;

const arms = [
  [`the checkout's footnote reads the monthly route ("${K} of ${N} covered names" collected), no legacy chatter caption, no "1 names"`, a1, a1 ? '0 faults (served and unserved)' : `${f1.length} faults; first: ${f1[0]}`],
  [`NEGATIVE: the base (${PIN}) still has the legacy chatter caption and/or the plural bug`, a2, a2 ? 'base carries the defect' : f2[0]],
  ['PLANTED: a legacy caption, a missing count and "1 names" are rejected; a correct footnote passes', a3, a3 ? `${caught.length} of ${M.length} rejected` : f3[0]],
];
let pass = 0;
for (const [n, ok, d] of arms) { if (ok) pass += 1; console.log(`${ok ? 'ARM PASS' : 'ARM FAIL'} ${n} :: ${d}`); }
console.log(`THE HEADER CHATTER LINE READS THE MONTHLY ROUTE: ${pass} of 3 arms`);
process.exit(pass === 3 ? 0 : 1);
