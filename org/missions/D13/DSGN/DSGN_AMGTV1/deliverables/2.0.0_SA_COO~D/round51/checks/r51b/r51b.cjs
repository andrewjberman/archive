/**
 * r51b.cjs -- DSGN_AMGTV1 round 51 issuer CHECK (2.0.0_SA_COO~D): OFFICERS IN THE SERVED ORDER; TWO PACKS, TWO PHRASES.
 *
 * Usage (from the directory whose portal/ is the checkout under test):
 *   cd "$(git rev-parse --show-toplevel)" && node "org/missions/D13/DSGN/DSGN_AMGTV1/deliverables/2.0.0_SA_COO~D/round51/checks/r51b/r51b.cjs"
 *
 * Why: PRD v0.18 @9a07662460, SAUX-38 ("Officers are drawn in the served order on every listing; the page applies no sort of its
 * own") and SAUX-40 ("The research team's pack and the page's own build are named with two different phrases, each used for one
 * thing only"). Read first: AMGT_RESAPP rows Z-S372 (BP/ LN drawn CFO first while the function serves the chief executive first)
 * and Z-S373 (AMD: "the research pack built for this name ... Worked" beside "no research pack for this security").
 *
 * Arms (each prints its evidence; exit 0 only on all of them):
 *   1 SERVED ORDER: the Exec tab's officer rows equal the served `management.officers` order, name for name, on three bundles:
 *     BA as served, BA with the list reversed, and BA with the chief financial officer moved to the front.
 *   2 TWO PHRASES: the page's words for the research team's document never use the phrase "research pack" (that phrase is the
 *     served name of the pack this system builds). `reasonInWords` turns "class A" into "research-team report"; the Thesis tab's
 *     own sentence for an empty pillar list says "the research team's report".
 *   3 PLANTED: the graders refuse a re-sorted list, a dropped officer and the phrase "research pack"; clean forms pass.
 * Renders the REAL ExecManagementTab.tsx and ThesisTab.tsx through round15/checks/_load.cjs; no network; writes nothing.
 */
'use strict';
const fs = require('fs');
const path = require('path');
const D = path.join(__dirname, '..', '..', '..');
const L = require(path.join(D, 'round15', 'checks', '_load.cjs'));
const SA = 'src/pages/SecurityAnalysis/';
const FX = path.join(D, 'round29', 'fixtures', 'tabs');
const load = (name) => { const d = JSON.parse(fs.readFileSync(path.join(FX, name), 'utf8')); return d && d.payload ? d.payload : d; };
const decode = (s) => String(s).replace(/&amp;/g, '&').replace(/&quot;/g, '"').replace(/&#x27;/g, "'").replace(/&lt;/g, '<').replace(/&gt;/g, '>');
const clone = (o) => JSON.parse(JSON.stringify(o));

function renderExec(bundle) {
  L.hookState.impl = { useThesisBundle: () => bundle };
  const m = L.source(SA + 'tabs/ExecManagementTab.tsx');
  return L.render(m.ExecManagementTab, { securityKey: bundle.security_key || 'BA_US_Equity' });
}
function renderThesis(bundle) {
  L.hookState.impl = { useThesisBundle: () => bundle };
  const m = L.source(SA + 'tabs/ThesisTab.tsx');
  return L.render(m.ThesisTab, { securityKey: bundle.security_key || 'BA_US_Equity' });
}
const rowNames = (html) => L.attrValues(html, 'data-exec-officer').map((a) => decode(a.value));

/** Faults of a drawn name list against the served one: same names, same order. */
function orderFaults(drawn, served) {
  const f = [];
  if (drawn.length !== served.length) f.push(`drew ${drawn.length} of ${served.length} served officers`);
  const at = served.findIndex((n, i) => drawn[i] !== n);
  if (at !== -1) f.push(`row ${at + 1} is "${drawn[at]}", the served row ${at + 1} is "${served[at]}"`);
  return f;
}
/** Faults of page text that names the research team's document. */
function phraseFaults(text) {
  const f = [];
  if (/research pack/i.test(text)) f.push(`the phrase "research pack" is used: "${String(text).slice(0, 140)}"`);
  return f;
}

const arms = [];
const BA = load('thesis.BA_US_Equity.json');
{
  const f = [];
  const served = clone(BA);
  const reversed = clone(BA); reversed.management.officers.reverse();
  const cfoFirst = clone(BA);
  const list = cfoFirst.management.officers;
  const cfoAt = list.findIndex((o) => /chief financial officer/i.test(o.role || ''));
  if (cfoAt < 0) f.push('INPUT: the BA fixture names no chief financial officer');
  else list.unshift(list.splice(cfoAt, 1)[0]);
  for (const [name, bundle] of [['BA as served', served], ['BA reversed', reversed], ['BA, CFO first', cfoFirst]]) {
    let html;
    try { html = renderExec(bundle); } catch (e) { f.push(`${name}: RENDER FAILED ${String(e.message).split('\n')[0]}`); continue; }
    const want = bundle.management.officers.map((o) => o.name);
    const got = rowNames(html);
    if (want.length < 3) f.push(`${name}: INPUT has ${want.length} officers`);
    for (const x of orderFaults(got, want)) f.push(`${name}: ${x}`);
  }
  arms.push(['OFFICERS ARE DRAWN IN THE SERVED ORDER', f.length === 0, f.length ? f.join(' | ') : '3 of 3 bundles drawn name for name in the served order']);
}
{
  const f = [];
  let RW;
  try { RW = L.source(SA + 'reasonWords.ts'); } catch (e) { f.push('LOADER: reasonWords.ts ' + String(e.message).split('\n')[0]); }
  if (RW) {
    const cases = [
      'no class A report for this security',
      'thesis pillars absent in class A missing or class B missing',
      'the class-A report carries no RECOMMENDATION line',
    ];
    for (const c of cases) {
      const out = RW.reasonInWords(c);
      for (const x of phraseFaults(out)) f.push(`reasonInWords("${c}") -> ${x}`);
      if (!/research-team report/.test(out)) f.push(`reasonInWords("${c}") -> "${out}" does not say "research-team report"`);
    }
    const b = RW.reasonInWords('no class B report for this security');
    if (!/earnings update/.test(b)) f.push(`class B no longer reads "earnings update": "${b}"`);
  }
  // The Thesis tab's own sentence for a dossier that is served with no pillar, no status and no reason.
  const bundle = clone(BA);
  bundle.dossier_fields = { thesis_pillars: [] };
  let html = '';
  try { html = renderThesis(bundle); } catch (e) { f.push('ThesisTab RENDER FAILED ' + String(e.message).split('\n')[0]); }
  const m = /<p[^>]*data-dossier-pillars="[^"]*"[^>]*>([\s\S]*?)<\/p>/.exec(html);
  if (!m) f.push('the Thesis tab drew no [data-dossier-pillars] sentence for a dossier with no pillars');
  else {
    const line = decode(m[1].replace(/<[^>]+>/g, ' ')).replace(/\s+/g, ' ').trim();
    if (!/the research team's report/.test(line)) f.push(`the empty-pillars sentence does not say "the research team's report": "${line}"`);
    if (/research team's pack/.test(line)) f.push(`the empty-pillars sentence still says "the research team's pack": "${line}"`);
  }
  arms.push(['THE RESEARCH TEAM\'S DOCUMENT IS NEVER CALLED "RESEARCH PACK"', f.length === 0, f.length ? f.join(' | ') : '3 class-A reasons read "research-team report"; class B reads "earnings update"; the empty-pillars sentence reads "the research team\'s report"']);
}
{
  const f = [];
  if (!orderFaults(['B', 'A', 'C'], ['A', 'B', 'C']).length) f.push('a re-sorted list accepted');
  if (!orderFaults(['A', 'B'], ['A', 'B', 'C']).length) f.push('a dropped officer accepted');
  if (orderFaults(['A', 'B', 'C'], ['A', 'B', 'C']).length) f.push('the served order refused');
  if (!phraseFaults('no research pack for this security').length) f.push('the phrase "research pack" accepted');
  if (phraseFaults('no research-team report for this security').length) f.push('the clean phrase refused');
  arms.push(['PLANTED', f.length === 0, f.length ? f.join(' | ') : '3 of 3 faults refused; 2 clean forms admitted']);
}

const TITLE = 'OFFICERS IN THE SERVED ORDER AND TWO PHRASES FOR TWO PACKS';
let pass = 0;
for (const [name, ok, ev] of arms) { if (ok) pass += 1; console.log(`ARM ${ok ? 'PASS' : 'FAIL'} ${name} :: ${ev}`); }
console.log(`${TITLE}: ${pass} of ${arms.length} arms`);
process.exit(pass === arms.length && arms.length === 3 ? 0 : 1);
