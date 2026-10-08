/**
 * r51a.cjs -- DSGN_AMGTV1 round 51 issuer CHECK (2.0.0_SA_COO~D): ONE STATEMENT OF INPUTS; THE SERVED COVERAGE SENTENCE IS DRAWN.
 *
 * Usage (from the directory whose portal/ is the checkout under test):
 *   cd "$(git rev-parse --show-toplevel)" && node "org/missions/D13/DSGN/DSGN_AMGTV1/deliverables/2.0.0_SA_COO~D/round51/checks/r51a/r51a.cjs"
 *
 * Why: PRD v0.18 @9a07662460, SAUX-37 ("The page carries ONE statement of inputs, the one the function serves on /thesis, drawn
 * once; no second statement is computed in the page") and SAUX-39 ("Every absence sentence the function serves is drawn where its
 * value would be; none is dropped"). Read first: AMGT_RESAPP row Z-W303-S1 (BA: the block above the tabs has 4 rows and no filings
 * row; the Model tab's ledger is a second statement and disagrees on Seeking Alpha) and the round-78 walk (MSFT: the served
 * `research_coverage.sentence` is drawn nowhere). Served shapes, read from lib/research/api at the deployed pin fbb643923e:
 *   /thesis  input_provenance: [bloomberg, seekingalpha, serp, filings, pack]; the filings row also carries form, filing_date,
 *            used_for (lib/research/api/inputs_statement.py).
 *   /overlay and /thesis  research_coverage: {status: covered | outside_coverage | not_known, covered, sentence, covered_names}
 *            (lib/research/api/coverage_marker.py); sentence is null for a covered name.
 *
 * Arms (each prints its evidence; exit 0 only on all of them):
 *   1 THE FILINGS ROW: InputProvenance, given the five served rows, draws five rows in the served order; the filings row names
 *     the form, the filing date in words and every `used_for` item, and prints no raw ISO date; a never-read filings row prints
 *     its served reason.
 *   2 ONE STATEMENT: SecurityAnalysis.tsx no longer feeds the block from the overlay's `input_provenance`; ModelTab.tsx carries no
 *     input ledger (no `data-input-ledger`, no `useInputLedger`).
 *   3 THE COVERAGE SENTENCE: components/CoverageNote.tsx draws the served sentence once in ONE element
 *     [data-research-coverage="<status>"] for outside_coverage and for not_known, draws nothing for a covered name or a missing
 *     marker, and SecurityAnalysis.tsx mounts it.
 *   4 PLANTED: the graders refuse a missing filings row, a raw ISO date, a sentence drawn twice and a sentence on a covered name.
 * Renders the REAL components through round15/checks/_load.cjs; no network; writes nothing.
 */
'use strict';
const fs = require('fs');
const path = require('path');
const D = path.join(__dirname, '..', '..', '..');
const L = require(path.join(D, 'round15', 'checks', '_load.cjs'));
const SA = 'src/pages/SecurityAnalysis/';
const decode = (s) => String(s).replace(/&amp;/g, '&').replace(/&quot;/g, '"').replace(/&#x27;/g, "'").replace(/&lt;/g, '<').replace(/&gt;/g, '>');
const text = (html) => decode(String(html).replace(/<[^>]+>/g, ' ')).replace(/\s+/g, ' ').trim();
const times = (hay, needle) => String(hay).split(needle).length - 1;
const src = (rel) => fs.readFileSync(path.join(L.base, SA + rel), 'utf8');

const USED = ['the filing passages', 'the written sections', 'the officer list'];
const FILED = { input: 'filings', source: 'company filings read for this name', last_run: '2026-01-30', outcome: 'landed',
  reason: 'This page uses the 10-K filed 2026-01-30 for the filing passages, the written sections and the officer list.',
  form: '10-K', filing_date: '2026-01-30', used_for: USED };
const NEVER_REASON = 'No company filing has been read for this name yet, so nothing on this page comes from one.';
const NOT_FILED = { input: 'filings', source: 'company filings read for this name', last_run: null, outcome: 'never read',
  reason: NEVER_REASON, form: null, filing_date: null, used_for: [] };
const four = () => [
  { input: 'bloomberg', source: 'Bloomberg data pulls stored for this name', last_run: '20261007T130241Z', outcome: 'landed', reason: 'the newest read of this input for this name is dated 20261007T130241Z' },
  { input: 'seekingalpha', source: 'Seeking Alpha articles and reports stored for this name', last_run: '20260911T040304Z', outcome: 'landed', reason: 'the newest read of this input for this name is dated 20260911T040304Z' },
  { input: 'serp', source: 'web search results stored for this name', last_run: 'NEVER', outcome: 'never read', reason: 'nothing has been read from this input for this name yet' },
  { input: 'pack', source: 'the research pack built for this name', last_run: '20261007T130100Z', outcome: 'landed', reason: 'the newest read of this input for this name is dated 20261007T130100Z' },
];
const five = (filings) => { const r = four(); r.splice(3, 0, filings); return r; };
const OUTSIDE = 'We do not cover this company yet, so we hold no company figures or research for it. Any news or comparable companies shown here come from our wider market data.';
const NOT_KNOWN = 'We could not check just now whether we cover this company.';

/** Rows of a rendered provenance block: [{n, text}]. */
function rows(html) {
  const out = [];
  const re = /<li[^>]*data-provenance-row="(\d+)"[^>]*>([\s\S]*?)<\/li>/g;
  let m;
  while ((m = re.exec(String(html))) !== null) out.push({ n: Number(m[1]), text: text(m[2]) });
  return out;
}
function filingsFaults(html, entries) {
  const f = [];
  const r = rows(html);
  if (r.length !== entries.length) f.push(`${r.length} row(s) drawn of ${entries.length} served`);
  const at = entries.findIndex((e) => e.input === 'filings');
  const row = r[at];
  if (!row) { f.push('no row is drawn at the filings entry\'s place'); return f; }
  const e = entries[at];
  if (!row.text.includes(e.source)) f.push(`the filings row does not carry its served source: "${row.text}"`);
  if (/\d{4}-\d{2}-\d{2}/.test(text(html))) f.push('a raw ISO date is printed');
  if (e.outcome === 'landed') {
    if (!row.text.includes(e.form)) f.push(`the filings row does not name the form ${e.form}: "${row.text}"`);
    if (!/January 30th, 2026/.test(row.text)) f.push(`the filings row does not print the filing date in words: "${row.text}"`);
    for (const u of e.used_for) if (!row.text.includes(u)) f.push(`the filings row does not say it was used for ${u}`);
  } else if (!row.text.includes(e.reason)) f.push(`a never-read filings row does not print its served reason: "${row.text}"`);
  return f;
}
function coverageFaults(html, status, sentence) {
  const f = [];
  const marks = (String(html).match(/data-research-coverage="/g) || []).length;
  if (sentence === null) {
    if (marks !== 0) f.push(`${marks} coverage element(s) drawn where no sentence is served`);
    if (text(html) !== '') f.push(`text drawn where no sentence is served: "${text(html).slice(0, 80)}"`);
    return f;
  }
  if (marks !== 1) f.push(`${marks} [data-research-coverage] element(s) (1 wanted)`);
  if (!new RegExp(`data-research-coverage="${status}"`).test(String(html))) f.push(`the element does not carry the served status ${status}`);
  const k = times(text(html), sentence);
  if (k !== 1) f.push(`the served sentence is printed ${k} time(s) (1 wanted)`);
  return f;
}

const arms = [];
{
  const f = [];
  let IP;
  try { IP = L.source(SA + 'components/InputProvenance.tsx'); } catch (e) { f.push('LOADER: InputProvenance.tsx ' + String(e.message).split('\n')[0]); }
  if (IP) {
    for (const [name, entries] of [['filed', five(FILED)], ['never read', five(NOT_FILED)]]) {
      let html;
      try { html = L.render(IP.InputProvenance, { entries }); } catch (e) { f.push(`${name}: RENDER FAILED ${String(e.message).split('\n')[0]}`); continue; }
      for (const x of filingsFaults(html, entries)) f.push(`${name}: ${x}`);
    }
  }
  arms.push(['THE FILINGS ROW SAYS WHAT THE PAGE USED', f.length === 0, f.length ? f.join(' | ') : 'five rows in the served order; form, date in words and 3 uses printed; no raw date; the never-read reason printed']);
}
{
  const f = [];
  const page = src('SecurityAnalysis.tsx');
  const model = src('tabs/ModelTab.tsx');
  if (/top\??\.input_provenance/.test(page)) f.push('SecurityAnalysis.tsx still feeds the block from the overlay\'s input_provenance');
  if (!/useThesisBundle/.test(page)) f.push('SecurityAnalysis.tsx does not read the thesis bundle');
  if (times(page, '<InputProvenance') !== 1) f.push(`SecurityAnalysis.tsx mounts InputProvenance ${times(page, '<InputProvenance')} time(s) (1 wanted)`);
  if (/data-input-ledger/.test(model)) f.push('ModelTab.tsx still draws [data-input-ledger]');
  if (/useInputLedger/.test(model)) f.push('ModelTab.tsx still reads useInputLedger');
  arms.push(['ONE STATEMENT OF INPUTS, FROM /thesis', f.length === 0, f.length ? f.join(' | ') : 'the block is fed from the thesis bundle, mounted once; the Model tab carries no input ledger']);
}
{
  const f = [];
  let CN;
  try { CN = L.source(SA + 'components/CoverageNote.tsx'); } catch (e) { f.push('LOADER: components/CoverageNote.tsx ' + String(e.message).split('\n')[0]); }
  if (CN && typeof CN.CoverageNote !== 'function') f.push('components/CoverageNote.tsx does not export CoverageNote');
  else if (CN) {
    const cases = [
      ['outside coverage', { status: 'outside_coverage', covered: false, sentence: OUTSIDE, covered_names: 95 }, 'outside_coverage', OUTSIDE],
      ['not known', { status: 'not_known', covered: null, sentence: NOT_KNOWN, covered_names: null }, 'not_known', NOT_KNOWN],
      ['covered', { status: 'covered', covered: true, sentence: null, covered_names: 95 }, 'covered', null],
      ['no marker', undefined, '', null],
    ];
    for (const [name, coverage, status, sentence] of cases) {
      let html;
      try { html = L.render(CN.CoverageNote, { coverage }); } catch (e) { f.push(`${name}: RENDER FAILED ${String(e.message).split('\n')[0]}`); continue; }
      for (const x of coverageFaults(html, status, sentence)) f.push(`${name}: ${x}`);
    }
  }
  if (times(src('SecurityAnalysis.tsx'), '<CoverageNote') !== 1) f.push('SecurityAnalysis.tsx does not mount CoverageNote exactly once');
  arms.push(['THE SERVED COVERAGE SENTENCE IS DRAWN ONCE', f.length === 0, f.length ? f.join(' | ') : 'outside coverage and not known each draw their served sentence once; a covered name and a missing marker draw nothing; mounted once']);
}
{
  const f = [];
  const li = (n, t) => `<li data-provenance-row="${n}">${t}</li>`;
  const good = five(FILED);
  const clean = good.map((e, i) => li(i + 1, e.input === 'filings' ? `${e.source} -- 10-K filed January 30th, 2026 -- used for ${USED.join(', ')}` : e.source)).join('');
  if (filingsFaults(clean, good).length) f.push('the clean provenance form refused: ' + filingsFaults(clean, good)[0]);
  if (!filingsFaults(four().map((e, i) => li(i + 1, e.source)).join(''), good).length) f.push('a missing filings row accepted');
  if (!filingsFaults(clean.replace('January 30th, 2026', '2026-01-30'), good).length) f.push('a raw ISO date accepted');
  const one = `<p data-research-coverage="outside_coverage">${OUTSIDE}</p>`;
  if (coverageFaults(one, 'outside_coverage', OUTSIDE).length) f.push('the clean coverage form refused');
  if (!coverageFaults(one + `<p>${OUTSIDE}</p>`, 'outside_coverage', OUTSIDE).length) f.push('a sentence drawn twice accepted');
  if (!coverageFaults(one, 'covered', null).length) f.push('a sentence on a covered name accepted');
  arms.push(['PLANTED', f.length === 0, f.length ? f.join(' | ') : '4 of 4 faults refused; 2 clean forms admitted']);
}

const TITLE = 'ONE STATEMENT OF INPUTS AND THE SERVED COVERAGE SENTENCE';
let pass = 0;
for (const [name, ok, ev] of arms) { if (ok) pass += 1; console.log(`ARM ${ok ? 'PASS' : 'FAIL'} ${name} :: ${ev}`); }
console.log(`${TITLE}: ${pass} of ${arms.length} arms`);
process.exit(pass === arms.length && arms.length === 4 ? 0 : 1);
