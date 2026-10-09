/**
 * r57a.cjs -- DSGN_AMGTV1 round 57 issuer CHECK (2.0.0_SA_COO~D1): A NAME NOT FOUND IS SAID AS NOT FOUND, NEVER AS A FEED OUTAGE.
 *
 * Usage (from the directory whose portal/ is the checkout under test):
 *   cd "$(git rev-parse --show-toplevel)" && node "org/missions/D13/DSGN/DSGN_AMGTV1/deliverables/2.0.0_SA_COO~D1/round57/checks/r57a.cjs"
 *
 * Why (round-56 analysis, ruling R1(b), ledger/ROUND_ANALYSIS.round56.md): on DEV 0008ddd3 a typed name pressed with Enter fetched
 * /api/scoped/amgt/security/<typed text>/... (404) and the page said "Try again; if it keeps failing, the feed is down."
 * apiRequest (src/api/api-client.ts) throws Error("API request failed: <status> <statusText> - <body>"); the status lives only in
 * the message, so the page-local helper reads it there.
 *
 * Arms (each prints its evidence; exit 0 only on all four):
 *   1 THE 404 IS KNOWN: notFound.ts isNotFound() is true for an apiRequest 404 error and false for 500, 401, a network error,
 *     a non-Error and null.
 *   2 THE WORDS: notFoundWords("Boeing") reads exactly 'No security found for "Boeing".' -- no "feed", no "down", no "Try again".
 *   3 THE PAGE USES THEM: SecurityAnalysis.tsx imports isNotFound and notFoundWords from './notFound' and draws an element
 *     carrying data-slot="security-not-found" (source read; the rendered branch is the cell's bun test, criterion AC2).
 *   4 PLANTED: the graders refuse a helper that calls every error a 404, words that blame the feed, and a page without the slot.
 * Loads the REAL modules through D's round15/checks/_load.cjs; no network; writes nothing.
 */
'use strict';
const fs = require('fs');
const path = require('path');
const DD = path.join(__dirname, '..', '..', '..', '2.0.0_SA_COO~D');
const L = require(path.join(DD, 'round15', 'checks', '_load.cjs'));
const ROOT = process.cwd();
const PAGE = path.join(ROOT, 'portal', 'src', 'pages', 'SecurityAnalysis', 'SecurityAnalysis.tsx');

const e404 = new Error('API request failed: 404 Not Found - {"error":"not found"}');
const cases = [
  [e404, true],
  [new Error('API request failed: 500 Internal Server Error - boom'), false],
  [new Error('API request failed: 401 Unauthorized - expired'), false],
  [new Error('Failed to fetch'), false],
  ['API request failed: 404 Not Found', false],
  [null, false],
];
function isNotFoundFaults(fn) {
  const f = [];
  for (const [e, want] of cases) { let got; try { got = fn(e); } catch (x) { got = 'THREW ' + x.message; } if (got !== want) f.push(`isNotFound(${e instanceof Error ? e.message.slice(0, 40) : JSON.stringify(e)}) = ${got} (wanted ${want})`); }
  return f;
}
function wordsFaults(fn) {
  const f = []; let w;
  try { w = fn('Boeing'); } catch (x) { return ['notFoundWords THREW ' + x.message]; }
  if (w !== 'No security found for "Boeing".') f.push(`notFoundWords("Boeing") = ${JSON.stringify(w)}`);
  if (/feed|down|try again/i.test(String(w))) f.push('the words blame the feed');
  return f;
}
function pageFaults(src) {
  const f = [];
  if (!/import\s*\{[^}]*\bisNotFound\b[^}]*\bnotFoundWords\b[^}]*\}\s*from\s*['"]\.\/notFound['"]|import\s*\{[^}]*\bnotFoundWords\b[^}]*\bisNotFound\b[^}]*\}\s*from\s*['"]\.\/notFound['"]/.test(src)) f.push('SecurityAnalysis.tsx does not import isNotFound and notFoundWords from ./notFound');
  if (!/data-slot=["']security-not-found["']/.test(src)) f.push('SecurityAnalysis.tsx draws no data-slot="security-not-found"');
  return f;
}

const arms = [];
let mod = null; const load = [];
try { mod = L.source('src/pages/SecurityAnalysis/notFound.ts'); } catch (e) { load.push('LOADER: notFound.ts ' + String(e.message).split('\n')[0]); }
{
  const f = mod && typeof mod.isNotFound === 'function' ? isNotFoundFaults(mod.isNotFound) : (load.length ? load.slice() : ['notFound.ts exports no isNotFound']);
  arms.push(['THE 404 IS KNOWN', f.length === 0, f.length ? f.join(' | ') : `${cases.length} of ${cases.length} cases (404 true; 500, 401, network, non-Error, null false)`]);
}
{
  const f = mod && typeof mod.notFoundWords === 'function' ? wordsFaults(mod.notFoundWords) : (load.length ? load.slice() : ['notFound.ts exports no notFoundWords']);
  arms.push(['THE WORDS', f.length === 0, f.length ? f.join(' | ') : 'notFoundWords("Boeing") reads \'No security found for "Boeing".\'']);
}
{
  let src = ''; try { src = fs.readFileSync(PAGE, 'utf8'); } catch (e) { src = null; }
  const f = src === null ? ['cannot read ' + PAGE] : pageFaults(src);
  arms.push(['THE PAGE USES THEM', f.length === 0, f.length ? f.join(' | ') : 'SecurityAnalysis.tsx imports both from ./notFound and draws data-slot="security-not-found"']);
}
{
  const f = [];
  if (!isNotFoundFaults(() => true).length) f.push('a helper calling every error a 404 accepted');
  if (isNotFoundFaults((e) => e instanceof Error && /^API request failed: 404\b/.test(e.message)).length) f.push('the clean helper refused');
  if (!wordsFaults(() => 'Boeing could not be loaded. If it keeps failing, the feed is down.').length) f.push('words blaming the feed accepted');
  if (wordsFaults((t) => `No security found for "${t}".`).length) f.push('the clean words refused');
  if (!pageFaults("import { isNotFound, notFoundWords } from './notFound'\n<p>x</p>").length) f.push('a page without the slot accepted');
  if (pageFaults("import { isNotFound, notFoundWords } from './notFound'\n<p data-slot=\"security-not-found\">x</p>").length) f.push('the clean page refused');
  arms.push(['PLANTED', f.length === 0, f.length ? f.join(' | ') : '3 of 3 faults refused; the clean forms admitted']);
}

const TITLE = 'A NAME NOT FOUND IS SAID AS NOT FOUND';
let pass = 0;
for (const [name, ok, ev] of arms) { if (ok) pass += 1; console.log(`ARM ${ok ? 'PASS' : 'FAIL'} ${name} :: ${ev}`); }
console.log(`${TITLE}: ${pass} of ${arms.length} arms`);
process.exit(pass === arms.length && arms.length === 4 ? 0 : 1);
