// POSN_ASTTAX.TO-V6-1 / V6-AC3 -- the expansion of <PRINT_ASSETCLASSORDER_LITERAL_EDITED>.
//
// Prints THREE orders side by side and compares them:
//   (A) the PRD s.3 canonical order, QUOTED from `git show 99cc431075:<prd>` -- never
//       retyped from the task order, which is what the cell forbids;
//   (B) the edited assetClassOrder literal in HoldingsTab.tsx;
//   (C) the Asset Class row order in PositioningSummary.tsx.
// Then it checks that the HoldingsTab colour map keys every one of the five to an F1
// ASSET_CLASS token that REALLY EXISTS in chartColors.ts, and that no value is a hex.
//
// Nothing is re-typed: every array is lifted out of the file that renders it and
// EVALUATED, so a literal that does not parse fails loudly instead of being described.
// Run from the worktree root:
//   node -e "require('./org/missions/D4/POSN/POSN_ASTTAX/deliverables/0.9.0_WK_POSN_ASTTAX~22/print_assetclassorder.js')"
'use strict';
const fs = require('fs');
const { execFileSync } = require('child_process');

const PRD_PIN = '99cc431075';
const PRD_PATH = 'org/missions/D4/POSN/POSN_ASTTAX/prd/POSN_ASTTAX_PRD.md';
const PRD_PIN_V08 = '709d7b4221';            // control only: the v0.8 bump
const HOLDINGS = 'portal/src/pages/Positioning/tabs/HoldingsTab.tsx';
const SUMMARY = 'portal/src/pages/Positioning/panels/PositioningSummary.tsx';
const REGISTRY = 'portal/src/lib/chartColors.ts';

// --- balanced-bracket slice: the only safe way to lift a literal that contains commas,
// --- comments and nested braces. A regex would stop at the first ']' inside a comment.
function slice(text, startIdx, open, close) {
  const i = text.indexOf(open, startIdx);
  if (i < 0) throw new Error('UNPARSEABLE: no ' + open + ' after index ' + startIdx);
  let depth = 0;
  for (let j = i; j < text.length; j++) {
    if (text[j] === open) depth++;
    else if (text[j] === close) { depth--; if (depth === 0) return text.slice(i, j + 1); }
  }
  throw new Error('UNPARSEABLE: unbalanced ' + open);
}

function anchor(text, needle, file) {
  const i = text.indexOf(needle);
  if (i < 0) throw new Error('ABSENT in ' + file + ': ' + needle);
  return i;
}

// Slice the VALUE of a declaration, anchored on the '=' and not on the declaration name.
// `const X: readonly string[] = [...]` has a '[' INSIDE ITS TYPE ANNOTATION, and anchoring
// on the name lifts that empty '[]' instead -- which is a silent wrong-object read: it
// parses, it evaluates, and it yields an empty array that then "disagrees" with the PRD.
function assigned(text, declName, open, close, file) {
  const i = anchor(text, declName, file);
  const j = text.indexOf('= ' + open, i);
  if (j < 0) throw new Error('UNPARSEABLE in ' + file + ': no "= ' + open + '" after ' + declName);
  return slice(text, j, open, close);
}

// --------------------------------------------------------------------------- (A) PRD
function prdOrder(pin) {
  const md = execFileSync('git', ['show', pin + ':' + PRD_PATH], {
    encoding: 'utf8', maxBuffer: 64 * 1024 * 1024,
  });
  const head = md.indexOf('## 3. The five classes');
  if (head < 0) throw new Error('ABSENT: PRD s.3 heading at ' + pin);
  const body = md.slice(head, md.indexOf('\n## ', head + 4));
  // Table rows are `| n | class | color | holds |`; take column 2 of the numbered rows.
  const rows = body.split('\n')
    .map((l) => l.trim())
    .filter((l) => /^\|\s*\d+\s*\|/.test(l))
    .map((l) => l.split('|').map((c) => c.trim()));
  return { classes: rows.map((c) => c[2]), colors: rows.map((c) => c[3]), raw: rows.length };
}

// --------------------------------------------------- (B) HoldingsTab.tsx order literal
const hold = fs.readFileSync(HOLDINGS, 'utf8');
const orderLiteralSrc = assigned(hold, 'const ASSET_CLASS_ORDER', '[', ']', HOLDINGS);
const holdingsOrder = new Function('return ' + orderLiteralSrc + ';')();

// The consuming line: the grouping must USE that one literal, not a second copy.
const consumerLine = (hold.split('\n').find((l) => l.includes('const assetClassOrder =')) || '').trim();

// ------------------------------------------------- HoldingsTab.tsx colour map, verbatim
const mapSrc = assigned(hold, 'const ASSET_CLASS_COLORS', '{', '}', HOLDINGS);
const mapEntries = [];
for (const line of mapSrc.split('\n')) {
  const m = line.match(/^\s*'([^']+)'\s*:\s*([A-Za-z_.]+)\s*,/);
  if (m) mapEntries.push({ key: m[1], value: m[2] });
}
const hexInMap = mapSrc.split('\n').filter((l) => /#[0-9a-fA-F]{3,8}\b/.test(l) && !/^\s*\/\//.test(l));

// ------------------------------------------- the F1 registry, to prove the tokens exist
const reg = fs.readFileSync(REGISTRY, 'utf8');
const paletteSrc = assigned(reg, 'export const PALETTE', '{', '}', REGISTRY);
const assetClassSrc = assigned(reg, 'export const ASSET_CLASS ', '{', '}', REGISTRY);
const { PALETTE, ASSET_CLASS } = new Function(
  'const PALETTE = ' + paletteSrc + ';\n' +
  'const ASSET_CLASS = ' + assetClassSrc + ';\n' +
  'return { PALETTE, ASSET_CLASS };'
)();

// ------------------------------------------- (C) PositioningSummary.tsx Asset Class rows
const summ = fs.readFileSync(SUMMARY, 'utf8');
const classesSrc = assigned(summ, 'const ASSET_CLASSES', '[', ']', SUMMARY);
const summaryRows = [];
for (const entrySrc of classesSrc.split('\n')) {
  const label = entrySrc.match(/\blabel:\s*'([^']+)'/);
  const rowLabel = entrySrc.match(/\browLabel:\s*'([^']+)'/);
  const color = entrySrc.match(/\bcolor:\s*(ASSET_CLASS\.[A-Za-z]+)/);
  if (label && rowLabel && color) {
    summaryRows.push({ label: label[1], rowLabel: rowLabel[1], color: color[1] });
  }
}

// --------------------------------------------------------------------------------- print
// PRD class 1 is the single ratified class "Fixed Income / Cash" -- ONE class carrying two
// served names. The page renders it as "Fixed Income" and keeps 'Cash' as a DISPLAY ALIAS
// in the colour map only. That is the ONLY normalisation applied here, and it is declared
// rather than hidden inside a comparison.
const ALIAS = { 'Fixed Income / Cash': 'Fixed Income' };
const norm = (s) => ALIAS[s] || s;

const prd = prdOrder(PRD_PIN);
const prdCanonical = prd.classes.map(norm);

console.log('V6-AC3 -- ONE ORDER, ONE COLOUR SOURCE, ON BOTH POSITIONING READERS');
console.log('');
console.log('(A) PRD s.3 @' + PRD_PIN + ' -- ' + prd.raw + ' numbered rows read from the table');
prd.classes.forEach((c, i) => {
  console.log('    ' + (i + 1) + '. ' + c.padEnd(22) + 'colour: ' + prd.colors[i]);
});
console.log('    normalised for the page (declared alias ' + JSON.stringify(ALIAS) + '):');
console.log('      ' + JSON.stringify(prdCanonical));
console.log('');

// CONTROL: the order at the CURRENT PRD version, to show the criterion's pin is not stale.
try {
  const v08 = prdOrder(PRD_PIN_V08);
  const same = JSON.stringify(v08.classes) === JSON.stringify(prd.classes);
  console.log('    CONTROL, s.3 at the LATER pin @' + PRD_PIN_V08 + ' (PRD v0.8): ' +
              JSON.stringify(v08.classes));
  console.log('    s.3 unchanged between the criterion pin and the current PRD: ' + same);
} catch (e) {
  console.log('    CONTROL at @' + PRD_PIN_V08 + ' UNAVAILABLE: ' + e.message);
}
console.log('');

console.log('(B) ' + HOLDINGS);
console.log('    ASSET_CLASS_ORDER literal, lifted and evaluated:');
console.log('      ' + JSON.stringify(holdingsOrder));
console.log('    the consuming line at the grouping site: ' + consumerLine);
console.log('    (one literal, one hop -- a second array would show up here as a second literal)');
console.log('');

console.log('(C) ' + SUMMARY);
console.log('    ASSET_CLASSES rows, in file order:');
summaryRows.forEach((r, i) => {
  console.log('      ' + (i + 1) + '. label=' + r.label.padEnd(14) +
              ' rowLabel=' + r.rowLabel.padEnd(20) + ' colour=' + r.color);
});
console.log('      ' + JSON.stringify(summaryRows.map((r) => r.label)));
console.log('');

// --------------------------------------------------------------------------- comparisons
const bOrder = holdingsOrder.slice();
const cOrder = summaryRows.map((r) => r.label);
const eqAB = JSON.stringify(bOrder) === JSON.stringify(prdCanonical);
const eqAC = JSON.stringify(cOrder) === JSON.stringify(prdCanonical);
const eqBC = JSON.stringify(bOrder) === JSON.stringify(cOrder);

console.log('COMPARISON');
console.log('  (B) HoldingsTab   == (A) PRD s.3 : ' + eqAB);
console.log('  (C) Summary rows  == (A) PRD s.3 : ' + eqAC);
console.log('  (B) == (C)                       : ' + eqBC);
console.log('');

// ------------------------------------------------- colour map: five keys, all F1 tokens
console.log('HOLDINGSTAB COLOUR MAP -- every ratified class keyed to an F1 token');
console.log('  denominator: ' + mapEntries.length + ' entries in ASSET_CLASS_COLORS');
let mapFail = 0;
for (const cls of prdCanonical) {
  const hit = mapEntries.find((e) => e.key === cls);
  if (!hit) {
    console.log('  ' + cls.padEnd(16) + 'MISSING from ASSET_CLASS_COLORS');
    mapFail++;
    continue;
  }
  const tokenName = hit.value.startsWith('ASSET_CLASS.') ? hit.value.slice('ASSET_CLASS.'.length) : null;
  const resolved = tokenName ? ASSET_CLASS[tokenName] : undefined;
  const ok = tokenName !== null && resolved !== undefined;
  if (!ok) mapFail++;
  console.log('  ' + cls.padEnd(16) + hit.value.padEnd(28) +
              (resolved ? '-> ' + resolved : '-> UNRESOLVED') + '  ' + (ok ? 'F1 TOKEN' : 'NOT AN F1 TOKEN'));
}
const extras = mapEntries.filter((e) => !prdCanonical.includes(e.key));
console.log('  non-class entries (display aliases), stated not hidden: ' +
            (extras.length ? extras.map((e) => e.key + '=' + e.value).join(', ') : 'none'));
console.log('  literal hex values in the map: ' + hexInMap.length +
            (hexInMap.length ? ' -> ' + JSON.stringify(hexInMap) : ' (none -- registry is the only colour source)'));
console.log('');

// summary colours must be F1 tokens too
let summFail = 0;
for (const r of summaryRows) {
  const tokenName = r.color.slice('ASSET_CLASS.'.length);
  if (ASSET_CLASS[tokenName] === undefined) { summFail++; }
}
console.log('SUMMARY ROW COLOURS -- ' + (summaryRows.length - summFail) + ' of ' + summaryRows.length +
            ' resolve to a live ASSET_CLASS token');
console.log('');

const pass = eqAB && eqAC && eqBC && mapFail === 0 && summFail === 0 &&
             hexInMap.length === 0 && bOrder.length === 5 && cOrder.length === 5;
console.log('DENOMINATOR: 5 ratified classes; HoldingsTab order carries ' + bOrder.length +
            ', Summary rows carry ' + cOrder.length + '.');
console.log('VERDICT-BY-OUTPUT: ' + (pass ? 'PASS' : 'FAIL') +
            ' (order match A=B=C: ' + (eqAB && eqAC && eqBC) +
            '; colour-map failures: ' + mapFail + '; summary colour failures: ' + summFail +
            '; literal hex: ' + hexInMap.length + ')');
if (!pass) process.exitCode = 1;
