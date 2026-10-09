/**
 * r60.cjs -- DSGN_AMGTV1 round 60 issuer CHECK (2.0.0_SA_COO~D1): the round-59 repair list plus the spine's search lines.
 *
 * Usage (from the directory whose portal/ is the checkout under test):
 *   cd "$(git rev-parse --show-toplevel)" && node "org/missions/D13/DSGN/DSGN_AMGTV1/deliverables/2.0.0_SA_COO~D1/round60/checks/r60.cjs"
 *
 * Why: ledger/ROUND_ANALYSIS.round59.md @3ce363b8b2 section 3 (items 2-7; item 1, the battery29 re-anchor, is graded by battery29 itself).
 * Arms (each prints its evidence; exit 0 only on all seven):
 *   1 SPINE DAY DETAIL WITHOUT COLLECTION BOOKKEEPING: TimelinePanel.tsx prints no "Not searched on this day", no "Searched:" and no
 *     "had no search run"; an empty day says "No articles on this day".
 *   2 NEWS OPENS TEN AT REST: HeaderBrief.tsx sets FEED_OPEN_AT_REST to at least 10 and no longer caps it with HEADER_FEED_VISIBLE_COUNT.
 *   3 THE DESCRIPTION ONCE, IN THE HEADER: SecurityOverlay.tsx draws one short description line (data-identity-description);
 *     HeaderBrief.tsx no longer draws "About the company".
 *   4 THE MIXED-CURRENCY REASON IN THE PEERS FOLD: PeersTab.tsx carries data-mixed-currency inside its data-absence-fold.
 *   5 WHAT CHANGED IN DISPLAY UNITS: WhatChangedPanel.tsx exports displayAmount(value, unit); displayAmount(1060161.94, 'millions')
 *     reads "1.06T" and displayAmount(12276538360, null) reads "12.28B" (loaded through the real module).
 *   6 ONE AS-OF PER CARD: WhatChangedPanel.tsx (a panel inside the Model card) mounts no CardFooter of its own.
 *   7 PLANTED: the graders refuse each base form and admit a clean form.
 * Reads source text, plus one real module load (arm 5) through D's round15/checks/_load.cjs. No network; writes nothing.
 */
'use strict';
const fs = require('fs');
const path = require('path');
const DD = path.join(__dirname, '..', '..', '..', '2.0.0_SA_COO~D');
const SA = path.join(process.cwd(), 'portal', 'src', 'pages', 'SecurityAnalysis');
const read = (rel) => { try { return fs.readFileSync(path.join(SA, rel), 'utf8'); } catch (e) { return null; } };

const G = {
  spine: (t) => {
    if (t === null) return ['TimelinePanel.tsx missing'];
    const f = ['Not searched on this day', 'Searched:', 'had no search run'].filter((w) => t.includes(w)).map((w) => `"${w}" still printed`);
    if (!t.includes('No articles on this day')) f.push('an empty day does not say "No articles on this day"');
    return f;
  },
  newsOpen: (t) => {
    if (t === null) return ['HeaderBrief.tsx missing'];
    const m = /FEED_OPEN_AT_REST\s*=\s*(\d+)/.exec(t);
    const f = [];
    if (!m || Number(m[1]) < 10) f.push(`FEED_OPEN_AT_REST is ${m ? m[1] : 'absent'} (wanted >= 10)`);
    if (/Math\.min\([^)]*HEADER_FEED_VISIBLE_COUNT/.test(t)) f.push('the open count is still capped by HEADER_FEED_VISIBLE_COUNT');
    return f;
  },
  description: (so, hb) => {
    const f = [];
    if (!so || !/data-identity-description/.test(so)) f.push('the identity header draws no description line (data-identity-description)');
    if (hb && /About the company/.test(hb)) f.push('HeaderBrief still draws "About the company"');
    return f;
  },
  mixed: (t) => (t && /data-mixed-currency/.test(t) && /data-absence-fold/.test(t) ? [] : ['PeersTab carries no data-mixed-currency line in its fold']),
  amount: (fn) => {
    if (typeof fn !== 'function') return ['WhatChangedPanel exports no displayAmount'];
    const f = [];
    let a; let b;
    try { a = fn(1060161.94, 'millions'); } catch (e) { a = 'THREW ' + e.message; }
    try { b = fn(12276538360, null); } catch (e) { b = 'THREW ' + e.message; }
    if (a !== '1.06T') f.push(`displayAmount(1060161.94, 'millions') = ${JSON.stringify(a)} (wanted "1.06T")`);
    if (b !== '12.28B') f.push(`displayAmount(12276538360, null) = ${JSON.stringify(b)} (wanted "12.28B")`);
    return f;
  },
  oneFooter: (t) => (t && /<CardFooter/.test(t) ? ['WhatChangedPanel still mounts its own CardFooter inside the Model card'] : []),
};

const arms = [];
const push = (name, f) => arms.push([name, f.length === 0, f.length ? f.join(' | ') : 'holds']);
push('SPINE DAY DETAIL WITHOUT COLLECTION BOOKKEEPING', G.spine(read('components/TimelinePanel.tsx')));
push('NEWS OPENS TEN AT REST', G.newsOpen(read('components/HeaderBrief.tsx')));
push('THE DESCRIPTION ONCE, IN THE HEADER', G.description(read('components/SecurityOverlay.tsx'), read('components/HeaderBrief.tsx')));
push('THE MIXED-CURRENCY REASON IN THE PEERS FOLD', G.mixed(read('tabs/PeersTab.tsx')));
{
  let fn = null; let err = null;
  try {
    const L = require(path.join(DD, 'round15', 'checks', '_load.cjs'));
    fn = L.source('src/pages/SecurityAnalysis/components/model/WhatChangedPanel.tsx').displayAmount;
  } catch (e) { err = 'LOADER: ' + String(e.message).split('\n')[0]; }
  push('WHAT CHANGED IN DISPLAY UNITS', err ? [err] : G.amount(fn));
}
push('ONE AS-OF PER CARD', G.oneFooter(read('components/model/WhatChangedPanel.tsx')));
{
  const p = [];
  if (!G.spine('Not searched on this day').length || G.spine('No articles on this day').length) p.push('spine grader wrong');
  if (!G.newsOpen('const FEED_OPEN_AT_REST = 1; Math.min(FEED_OPEN_AT_REST, HEADER_FEED_VISIBLE_COUNT)').length || G.newsOpen('const FEED_OPEN_AT_REST = 10').length) p.push('news grader wrong');
  if (!G.description('<HeaderCards />', 'About the company').length || G.description('<p data-identity-description>', '<ul>').length) p.push('description grader wrong');
  if (!G.mixed('<td></td>').length || G.mixed('<details data-absence-fold><p data-mixed-currency>').length) p.push('mixed-currency grader wrong');
  if (!G.amount((v) => String(v)).length || G.amount((v, u) => (u === 'millions' ? '1.06T' : '12.28B')).length) p.push('amount grader wrong');
  if (!G.oneFooter('<CardFooter />').length || G.oneFooter('<table>').length) p.push('footer grader wrong');
  push('PLANTED', p);
}

let pass = 0;
for (const [name, ok, ev] of arms) { if (ok) pass += 1; console.log(`ARM ${ok ? 'PASS' : 'FAIL'} ${name} :: ${ev}`); }
console.log(`ROUND 60 REPAIRS: ${pass} of ${arms.length} arms`);
process.exit(pass === arms.length ? 0 : 1);
