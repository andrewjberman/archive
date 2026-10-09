/**
 * r63a.cjs -- DSGN_AMGTV1 round 63 issuer CHECK (2.0.0_SA_COO~D1), prepared ahead of the round-62 analysis:
 * A TYPED NAME THAT MATCHES SEVERAL COMPANIES SHOWS THE SERVED CANDIDATES, NOT "NO SECURITY FOUND".
 *
 * Usage (from the directory whose portal/ is the checkout under test):
 *   cd "$(git rev-parse --show-toplevel)" && node "org/missions/D13/DSGN/DSGN_AMGTV1/deliverables/2.0.0_SA_COO~D1/round63/checks/r63a.cjs"
 *
 * Why (round63/PREP.md item 4; CTO msg 2285, ledger/CTO_RULING_ROUND57_R1A_R6_20261009.md ADDENDUM 2): for "ASML" the route answers 404
 * with {"refused": true, "reason": "2 companies match 'ASML'; type the ticker.", "candidates": [{"security_key", "name"}, ...]}
 * (lib/research/api/scoped_amgt.py:7076-7082). apiRequest throws Error("API request failed: 404 <statusText> - <body>"), and the page's
 * notFound.ts reads any 404 as not found, so it draws 'No security found for "ASML".' and drops the served list.
 * Arms (exit 0 only on all three):
 *   1 THE SERVED CHOICES ARE READ: notFound.ts exports servedChoices(error). For a 404 whose body carries two or more candidates it
 *     returns { reason, candidates: [{ security_key, name }] } exactly as served. It returns null for a 404 with no candidates, a
 *     non-404 error, a body that is not JSON, and a non-Error (loaded through the real module).
 *   2 THE CHOICES ARE DRAWN: SecurityAnalysis.tsx's not-found branch reads servedChoices. It draws the served reason and one control
 *     per candidate, marked data-security-choice, that opens that key through state.selectSecurity. The fixed not-found sentence
 *     stays for a 404 with no candidates.
 *   3 PLANTED: the graders refuse the round-62 form and wrong parses, and admit the clean form.
 * Source read only; no network; writes nothing.
 */
'use strict';
const fs = require('fs');
const path = require('path');
const DD = path.join(__dirname, '..', '..', '..', '2.0.0_SA_COO~D');
const SA = path.join(process.cwd(), 'portal', 'src', 'pages', 'SecurityAnalysis');
const read = (rel) => { try { return fs.readFileSync(path.join(SA, rel), 'utf8'); } catch (e) { return null; } };

const SERVED = { refused: true, reason: "2 companies match 'ASML'; type the ticker.", candidates: [
  { security_key: 'ASML_US_Equity', name: 'ASML Holding NV' }, { security_key: 'ASML_NA_Equity', name: 'ASML NA' }] };
const err = (status, text, body) => new Error(`API request failed: ${status} ${text} - ${body}`);

const G = {
  parsed: (fn) => {
    if (typeof fn !== 'function') return ['notFound.ts exports no servedChoices'];
    const f = [];
    const run = (label, arg) => { try { return fn(arg); } catch (e) { f.push(`${label} threw: ${e.message}`); return 'THREW'; } };
    const got = run('the multi-match 404', err(404, 'Not Found', JSON.stringify(SERVED)));
    const want = JSON.stringify({ reason: SERVED.reason, candidates: SERVED.candidates });
    if (!got || got === 'THREW' || JSON.stringify({ reason: got.reason, candidates: got.candidates }) !== want) f.push(`the multi-match 404 read as ${JSON.stringify(got)} (wanted ${want})`);
    const nulls = [
      ['a 404 with no candidates', err(404, 'Not Found', JSON.stringify({ error: "no security matches 'ZZZ'" }))],
      ['a 404 with one candidate', err(404, 'Not Found', JSON.stringify({ reason: 'x', candidates: [SERVED.candidates[0]] }))],
      ['a 500 carrying candidates', err(500, 'Server Error', JSON.stringify(SERVED))],
      ['a 404 whose body is not JSON', err(404, 'Not Found', '<html>gateway</html>')],
      ['a non-Error', 'API request failed: 404 Not Found - ' + JSON.stringify(SERVED)],
    ];
    for (const [label, arg] of nulls) { const r = run(label, arg); if (r !== null && r !== 'THREW') f.push(`${label} returned ${JSON.stringify(r)} (wanted null)`); }
    return f;
  },
  drawn: (t) => {
    if (t === null) return ['SecurityAnalysis.tsx missing'];
    const f = [];
    if (!/servedChoices\s*\(/.test(t)) f.push('the not-found branch does not read servedChoices');
    if (!/data-security-choice\b/.test(t)) f.push('no control per candidate (data-security-choice)');
    if (!/selectSecurity\s*\(\s*[A-Za-z_.]*security_key/.test(t)) f.push('a candidate does not open its key through selectSecurity(<candidate>.security_key)');
    if (!/\.reason\b/.test(t)) f.push('the served reason is not drawn');
    if (!/notFoundWords\s*\(/.test(t)) f.push('the fixed sentence for a 404 with no candidates is gone');
    return f;
  },
};

const arms = [];
const push = (name, f) => arms.push([name, f.length === 0, f.length ? f.join(' | ') : 'holds']);
{
  let fn = null; let e2 = null;
  try {
    const L = require(path.join(DD, 'round15', 'checks', '_load.cjs'));
    fn = L.source('src/pages/SecurityAnalysis/notFound.ts').servedChoices;
  } catch (e) { e2 = 'LOADER: ' + String(e.message).split('\n')[0]; }
  push('THE SERVED CHOICES ARE READ', e2 ? [e2] : G.parsed(fn));
}
push('THE CHOICES ARE DRAWN', G.drawn(read('SecurityAnalysis.tsx')));
{
  const p = [];
  const clean = (e) => {
    if (!(e instanceof Error)) return null;
    const m = /^API request failed: 404\b[^-]*- ([\s\S]*)$/.exec(e.message);
    if (!m) return null;
    let b; try { b = JSON.parse(m[1]); } catch (x) { return null; }
    const c = Array.isArray(b && b.candidates) ? b.candidates.filter((r) => r && typeof r.security_key === 'string') : [];
    return c.length >= 2 ? { reason: typeof b.reason === 'string' ? b.reason : null, candidates: c.map((r) => ({ security_key: r.security_key, name: r.name ?? null })) } : null;
  };
  if (G.parsed(clean).length) p.push('the clean parse refused: ' + G.parsed(clean).join('; '));
  if (!G.parsed(undefined).length) p.push('a missing export admitted');
  if (!G.parsed((e) => (e instanceof Error && /404/.test(e.message) ? { reason: null, candidates: [] } : null)).length) p.push('a parse that drops the list admitted');
  if (!G.parsed((e) => clean(e) || (e instanceof Error ? { reason: 'x', candidates: [] } : null)).length) p.push('a non-null for a plain 404 admitted');
  const r62 = "{nameNotFound ? (<div data-slot=\"security-not-found\"><PanelEmpty message={notFoundWords(state.selectedSecurityKey ?? '')} /></div>) : null}";
  if (!G.drawn(r62).length) p.push('the round-62 form admitted');
  const cleanTsx = "const choices = servedChoices(overlayQuery.error)\n{choices ? (<div><p>{choices.reason}</p>{choices.candidates.map((c) => (<button data-security-choice={c.security_key} onClick={() => state.selectSecurity(c.security_key)}>{c.name}</button>))}</div>) : (<PanelEmpty message={notFoundWords(key)} />)}";
  if (G.drawn(cleanTsx).length) p.push('the clean form refused: ' + G.drawn(cleanTsx).join('; '));
  push('PLANTED', p);
}
let pass = 0;
for (const [name, ok, ev] of arms) { if (ok) pass += 1; console.log(`ARM ${ok ? 'PASS' : 'FAIL'} ${name} :: ${ev}`); }
console.log(`ROUND 63 CANDIDATE LIST: ${pass} of ${arms.length} arms`);
process.exit(pass === arms.length ? 0 : 1);
