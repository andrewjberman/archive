/**
 * servedwords.cjs -- DSGN_AMGTV1 round 5, AV-v-7: THE MODEL READS THE SERVED WORDS (AMGT_RESAPP round-48 ask, msg 26588 from
 * 2.0.0_SA_COO~Z, placed by decomposition v4 "for the first round after ww-1 lands"; ww-1's NEVER-2 entry closed 19:56:55Z).
 *
 * Usage (repo root): node <this file>
 * The served /thesis now carries ONE definition of the Model words (AMGT_RESAPP ww-4): `model.line_names` (mnemonic -> the
 * line's name) and `model.cases.<case>.formula_words` (a served case's formula in words). The page must read THEM, keeping
 * its local copies (modelSheet.ts LINE_NAMES, ModelTab.tsx formulaInWords) only as the fallback when the payload omits
 * the field. The served AMD fixture (round5/fixtures/thesisBundle.AMD_US_Equity.json, extracted verbatim from AMGT_RESAPP
 * round48/captures/thesis_AMD_US_Equity_20260929T200344Z.json @8f50bcb837) carries both, EQUAL to the local copies today --
 * so a render of it cannot tell which one the page read. The arms therefore render DIFFERENCE variants built IN MEMORY
 * (the fixture file is never edited):
 *   1  served line names: every `model.line_names` value is replaced by "Served <value>"; every line name the page showed
 *      on the unmodified payload must now read "Served <that name>" (the page printed the payload's words, not its copy)
 *   2  served formula words: every served case's `formula_words` becomes "<value>, as served"; the served base case's
 *      line on the face carries "(<value>, as served)"
 *   3  the fallback: SAP GY (a payload with neither field) still names its Model lines from the local copy -- the same
 *      count of LINE_NAMES values visible as at the cut (the floor printed) -- and its base case still reads
 *      "Bloomberg consensus EPS (FY1) x adjusted trailing-median P/E" in words
 * Prints one line per arm and "MODEL READS THE SERVED WORDS: <k> of 3 arms"; exit 0 only at 3 of 3.
 */
const fs = require('fs');
const path = require('path');
const L = require('./_load.cjs');
const FLOOR_SAP_NAMES = Number(process.env.SERVEDWORDS_FLOOR || 25);

const amd = L.fixture('thesisBundle.AMD_US_Equity.json');
const sap = L.fixture('thesisBundle.SAP_GY_Equity.json');
const clone = (x) => JSON.parse(JSON.stringify(x));
const namesVar = clone(amd);
for (const k of Object.keys(namesVar.model.line_names || {})) namesVar.model.line_names[k] = 'Served ' + namesVar.model.line_names[k];
const wordsVar = clone(amd);
const served = [];  // the model block mirrors model_cases; both are varied the same way
for (const c of [wordsVar.model && wordsVar.model.cases, wordsVar.model_cases]) {
  for (const v of Object.values(c || {})) {
    if (v && typeof v === 'object' && v.formula_words) { v.formula_words = v.formula_words + ', as served'; served.push(v.formula_words); }
  }
}
const bundles = { AMD: amd, AMD_NAMES: namesVar, AMD_WORDS: wordsVar, SAP: sap };
L.hookState.impl = { useThesisBundle: (k) => bundles[k] };
function text(key) {
  try {
    return L.textOf(L.render(L.source('src/pages/SecurityAnalysis/tabs/ModelTab.tsx').ModelTab, { securityKey: key }));
  } catch (e) {
    console.log(`${key} render failed: ` + String(e.message).split('\n')[0]);
    return '';
  }
}
// The local copy, read from the page's own source (the fallback the page keeps).
const sheet = fs.readFileSync(path.join(L.base, 'src/pages/SecurityAnalysis/modelSheet.ts'), 'utf8');
const block = sheet.slice(sheet.indexOf('LINE_NAMES'), sheet.indexOf('UNNAMED_LINE'));
const localNames = [...block.matchAll(/^\s*[A-Z][A-Z0-9_]+:\s*'([^']*)'/gm)].map((m) => m[1]);

const amdText = text('AMD');
const shownNames = Object.values(amd.model.line_names || {}).filter((v) => amdText.includes(v));
const namesText = text('AMD_NAMES');
const readServed = shownNames.filter((v) => namesText.includes('Served ' + v));
const wordsText = text('AMD_WORDS');
const wordsShown = served.filter((w) => wordsText.includes('(' + w + ')'));
const sapText = text('SAP');
const sapNames = localNames.filter((v) => sapText.includes(v));
const sapWords = sapText.includes('Bloomberg consensus EPS (FY1) x adjusted trailing-median P/E');

const arms = [
  ['the page prints the served line names', shownNames.length > 0 && readServed.length === shownNames.length,
    `${readServed.length} of ${shownNames.length} named line(s) read the payload's words (${Object.keys(amd.model.line_names || {}).length} served names)`],
  ['the page prints the served formula words', served.length > 0 && wordsShown.length === served.length,
    `${wordsShown.length} of ${served.length} served case formula(s) printed from formula_words`],
  ['the fallback names SAP GY\'s lines from the local copy', sapNames.length >= FLOOR_SAP_NAMES && sapWords,
    `${sapNames.length} LINE_NAMES value(s) visible (floor ${FLOOR_SAP_NAMES}); base case in words ${sapWords}`],
];
let pass = 0;
for (const [name, ok, detail] of arms) {
  if (ok) pass += 1;
  console.log(`${ok ? 'ARM PASS' : 'ARM FAIL'} ${name} :: ${detail}`);
}
console.log(`MODEL READS THE SERVED WORDS: ${pass} of ${arms.length} arms`);
process.exit(pass === arms.length ? 0 : 1);
