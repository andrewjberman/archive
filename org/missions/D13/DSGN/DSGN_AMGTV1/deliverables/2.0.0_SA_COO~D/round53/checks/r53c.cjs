/**
 * r53c.cjs -- DSGN_AMGTV1 round 53 issuer CHECK (2.0.0_SA_COO~D): THE BUILT ANALYSIS IS NEVER CALLED "THE RESEARCH PACK".
 *
 * Usage (from the directory whose portal/ is the checkout under test):
 *   cd "$(git rev-parse --show-toplevel)" && node "org/missions/D13/DSGN/DSGN_AMGTV1/deliverables/2.0.0_SA_COO~D/round53/checks/r53c.cjs"
 *
 * Why: PRD v0.18 SAUX-40 (FWD-27, two packs, two phrases) and the CTO's ruling msg 31721 (decomposition v52): "Research Pack" is
 * the research team's own document; the BUILT thing loses the word at the producer -- AMGT_RESAPP round 79 cc-6 serves its
 * source as "the analysis built for this name" (live since the cc-7 redeploy). Four sentences in postureCites.ts still call
 * the built analysis "the research pack".
 *
 * Arms (each prints its evidence; exit 0 only on all three):
 *   1 THE FOUR SENTENCES: postureCites.ts carries each of the four new sentence templates verbatim, and the words
 *     "research pack" appear nowhere in the file (code or comment).
 *   2 STILL A MODULE: postureCites.ts loads and still exports formatCiteValue, absentSourceSentence, plainReason and
 *     resolveCite; the research team's own pack keeps its words in the rest of the page (reasonWords.ts still reads
 *     "the research team's pack").
 *   3 PLANTED: the grader refuses a file keeping one "research pack" and a file missing one template.
 * Reads and loads the REAL source through round15/checks/_load.cjs; no network; writes nothing.
 */
'use strict';
const fs = require('fs');
const path = require('path');
const D = path.join(__dirname, '..', '..');
const L = require(path.join(D, 'round15', 'checks', '_load.cjs'));
const SA = 'src/pages/SecurityAnalysis/';
const read = (rel) => fs.readFileSync(path.join(L.base, SA + rel), 'utf8');

const TEMPLATES = [
  'a comparison measure the analysis built for this name calls ${fieldWords(name)}',
  'a figure the analysis built for this name calls ${words}',
  "the analysis built for this name does not say the comparable's ${",
  "a filing passage the analysis built for this name cites, which no drafted sentence on ${sideWords(side)}'s thesis quotes, so this page does not carry its text",
];
function faults(src) {
  const f = [];
  TEMPLATES.forEach((t, i) => { if (!src.includes(t)) f.push(`sentence ${i + 1} is not in the file: "${t.slice(0, 70)}"`); });
  const left = src.split(/\r?\n/).map((l, i) => [i + 1, l]).filter(([, l]) => /research pack/i.test(l));
  if (left.length) f.push(`"research pack" still on ${left.length} line(s): ${left.slice(0, 4).map(([n]) => n).join(', ')}`);
  return f;
}

const arms = [];
let src = '';
try { src = read('postureCites.ts'); } catch (e) { src = ''; }
{
  const f = src ? faults(src) : ['postureCites.ts not readable'];
  arms.push(['THE FOUR SENTENCES NAME THE BUILT ANALYSIS', f.length === 0, f.length ? f.join(' | ') : '4 of 4 templates present; 0 lines say "research pack"']);
}
{
  const f = [];
  try {
    const m = L.source(SA + 'postureCites.ts');
    for (const k of ['formatCiteValue', 'absentSourceSentence', 'plainReason', 'resolveCite']) if (typeof m[k] !== 'function') f.push(`${k} is not exported`);
  } catch (e) { f.push('LOADER: postureCites.ts ' + String(e.message).split('\n')[0]); }
  if (!/the research team's pack/.test(read('reasonWords.ts'))) f.push("reasonWords.ts no longer reads \"the research team's pack\"");
  arms.push(['STILL A MODULE; THE TEAM\'S PACK KEEPS ITS WORDS', f.length === 0, f.length ? f.join(' | ') : "4 of 4 exports load; reasonWords.ts still names the research team's pack"]);
}
{
  const f = [];
  const clean = TEMPLATES.join('\n');
  if (faults(clean).length) f.push('the clean form refused: ' + faults(clean)[0]);
  if (!faults(clean + '\n// the research pack').length) f.push('a kept "research pack" accepted');
  if (!faults(TEMPLATES.slice(1).join('\n')).length) f.push('a missing template accepted');
  arms.push(['PLANTED', f.length === 0, f.length ? f.join(' | ') : '2 of 2 faults refused; the clean form admitted']);
}

const TITLE = 'THE BUILT ANALYSIS IS NEVER CALLED THE RESEARCH PACK';
let pass = 0;
for (const [name, ok, ev] of arms) { if (ok) pass += 1; console.log(`ARM ${ok ? 'PASS' : 'FAIL'} ${name} :: ${ev}`); }
console.log(`${TITLE}: ${pass} of ${arms.length} arms`);
process.exit(pass === arms.length && arms.length === 3 ? 0 : 1);
