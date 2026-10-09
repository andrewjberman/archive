/**
 * r61.cjs -- DSGN_AMGTV1 round 61 issuer CHECK (2.0.0_SA_COO~D1), prepared ahead of the round-60 analysis:
 * A BLANK PEERS AVERAGE ALWAYS SAYS WHY.
 *
 * Usage (from the directory whose portal/ is the checkout under test):
 *   cd "$(git rev-parse --show-toplevel)" && node "org/missions/D13/DSGN/DSGN_AMGTV1/deliverables/2.0.0_SA_COO~D1/round61/checks/r61.cjs"
 *
 * Why (round-60 close @aa9b9463a7; prep round61/PREP.md @255ea8df55): cscTable.ts blanks the Average for a column whose currency kind is
 * MIXED or UNSTATED, but PeersTab.tsx's fold line (data-mixed-currency) covers MIXED only. On Lenovo 992 HK the price column is
 * UNSTATED: the cell is blank and nothing says why.
 * Arms (exit 0 only on all three):
 *   1 BOTH BLANK KINDS ARE EXPLAINED: PeersTab.tsx draws a fold line for UNSTATED columns (data-unstated-currency) beside the MIXED line,
 *     both inside the data-absence-fold.
 *   2 THE WORDS: the UNSTATED line says the figures carry no stated currency, and does not claim the currencies differ.
 *   3 PLANTED: the graders refuse the round-60 form (MIXED only) and admit the clean form.
 * Source read only; no network; writes nothing.
 */
'use strict';
const fs = require('fs');
const path = require('path');
const read = (rel) => { try { return fs.readFileSync(path.join(process.cwd(), 'portal', 'src', 'pages', 'SecurityAnalysis', rel), 'utf8'); } catch (e) { return null; } };

const G = {
  both: (t) => {
    if (t === null) return ['PeersTab.tsx missing'];
    const f = [];
    if (!/data-absence-fold/.test(t)) f.push('no data-absence-fold');
    if (!/data-mixed-currency/.test(t)) f.push('the MIXED line (data-mixed-currency) is gone');
    if (!/data-unstated-currency/.test(t)) f.push('no line for UNSTATED columns (data-unstated-currency)');
    return f;
  },
  words: (t) => {
    if (t === null) return ['PeersTab.tsx missing'];
    const m = /data-unstated-currency[^>]*>\s*\{?`?([^`}<]*)/.exec(t);
    const w = m ? m[1] : '';
    const f = [];
    if (!/no stated currency|currency is not stated|without a stated currency/i.test(w)) f.push(`the UNSTATED line does not say the figures carry no stated currency: "${w.slice(0, 120)}"`);
    if (/different currencies/i.test(w)) f.push('the UNSTATED line claims the currencies differ');
    return f;
  },
};

const t = read('tabs/PeersTab.tsx');
const arms = [];
const push = (name, f) => arms.push([name, f.length === 0, f.length ? f.join(' | ') : 'holds']);
push('BOTH BLANK KINDS ARE EXPLAINED', G.both(t));
push('THE WORDS', G.words(t));
{
  const p = [];
  const base = '<details data-absence-fold><p data-mixed-currency="">x</p></details>';
  const clean = '<details data-absence-fold><p data-mixed-currency="">x</p><p data-unstated-currency="">{`The Average row shows no figure for Price: these peers report it with no stated currency.`}</p></details>';
  if (!G.both(base).length) p.push('the round-60 form admitted');
  if (G.both(clean).length || G.words(clean).length) p.push('the clean form refused');
  if (!G.words('<p data-unstated-currency="">{`these peers report it in different currencies.`}</p>').length) p.push('wrong words admitted');
  push('PLANTED', p);
}
let pass = 0;
for (const [name, ok, ev] of arms) { if (ok) pass += 1; console.log(`ARM ${ok ? 'PASS' : 'FAIL'} ${name} :: ${ev}`); }
console.log(`ROUND 61 PEERS AVERAGE: ${pass} of ${arms.length} arms`);
process.exit(pass === arms.length ? 0 : 1);
