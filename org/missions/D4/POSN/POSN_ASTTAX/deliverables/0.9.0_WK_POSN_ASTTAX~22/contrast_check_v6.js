// POSN_ASTTAX.TO-V6-1 / V6-AC9 -- the expansion of <CONTRAST_CHECK_V6>.
//
// EXTENDS TO-V5-1's contrast_check.js rather than re-implementing it: the WCAG 2.x
// luminance and ratio functions are LIFTED OUT OF THAT FILE'S SOURCE and evaluated here,
// so the two cells' numbers come from the same bytes. The file they measure --
// portal/src/lib/chartColors.ts -- is lifted the same way: PALETTE, ASSET_CLASS,
// SUB_ASSET_COLORS and BOTH text-colour functions are executed, never restated.
//
// Covers:
//   (i)  Volatility and Options Income on their new pink tokens, through the file's own
//        getSubAssetTextColor;
//   (ii) EVERY site under src/pages/Positioning that renders text over an ASSET_CLASS
//        value, through the file's own getAssetClassTextColor -- with the census printed
//        as a SUBTRACTION from a denominator, not as a list of what came to mind.
//
// Run from the worktree root:
//   node -e "require('./org/missions/D4/POSN/POSN_ASTTAX/deliverables/0.9.0_WK_POSN_ASTTAX~22/contrast_check_v6.js')"
'use strict';
const fs = require('fs');
const path = require('path');

const HERE = __dirname;
const V5_INSTRUMENT = path.join(HERE, 'contrast_check.js');
const SRC = 'portal/src/lib/chartColors.ts';
const PAGE_DIR = 'portal/src/pages/Positioning';
const FLOOR = 4.5;

// ---------------------------------------------------------------------------
// 1. The WCAG maths, LIFTED from the F1 instrument (not retyped).
// ---------------------------------------------------------------------------
const v5src = fs.readFileSync(V5_INSTRUMENT, 'utf8');
function liftFn(text, name, file) {
  const i = text.indexOf('function ' + name + '(');
  if (i < 0) throw new Error('ABSENT: function ' + name + ' in ' + file);
  const end = text.indexOf('\n}', i);
  if (end < 0) throw new Error('UNPARSEABLE: function ' + name + ' in ' + file);
  return text.slice(i, end + 2);
}
const { luminance, ratio } = new Function(
  liftFn(v5src, 'luminance', V5_INSTRUMENT) + '\n' +
  liftFn(v5src, 'ratio', V5_INSTRUMENT) + '\n' +
  'return { luminance, ratio };'
)();

// ---------------------------------------------------------------------------
// 2. The registry under test, lifted and EXECUTED.
// ---------------------------------------------------------------------------
const text = fs.readFileSync(SRC, 'utf8');
function slice(t, from, open, close) {
  const i = t.indexOf(open, from);
  let d = 0;
  for (let j = i; j < t.length; j++) {
    if (t[j] === open) d++;
    else if (t[j] === close) { d--; if (d === 0) return t.slice(i, j + 1); }
  }
  throw new Error('UNPARSEABLE: unbalanced ' + open + ' in ' + SRC);
}
// Anchored on the '=' so a '[]' or '{}' inside a TYPE ANNOTATION is never lifted instead.
function assigned(t, decl, open, close) {
  const i = t.indexOf(decl);
  if (i < 0) throw new Error('ABSENT in ' + SRC + ': ' + decl);
  const j = t.indexOf('= ' + open, i);
  if (j < 0) throw new Error('UNPARSEABLE in ' + SRC + ': no "= ' + open + '" after ' + decl);
  return slice(t, j, open, close);
}
function fnBody(name) {
  const i = text.indexOf('export function ' + name);
  if (i < 0) throw new Error('ABSENT: function ' + name + ' in ' + SRC);
  const end = text.indexOf('\n}', i);
  return text.slice(i + 'export '.length, end + 2)
    .replace('(bgHex: string): string', '(bgHex)')
    .replace('const lightBackgrounds: string[] =', 'const lightBackgrounds =');
}
const { PALETTE, ASSET_CLASS, SUB_ASSET_COLORS, getSubAssetTextColor, getAssetClassTextColor } =
  new Function(
    'const PALETTE = ' + assigned(text, 'export const PALETTE', '{', '}') + ';\n' +
    'const ASSET_CLASS = ' + assigned(text, 'export const ASSET_CLASS ', '{', '}') + ';\n' +
    'const SUB_ASSET_COLORS = ' + assigned(text, 'export const SUB_ASSET_COLORS', '{', '}') + ';\n' +
    fnBody('getSubAssetTextColor') + '\n' +
    fnBody('getAssetClassTextColor') + '\n' +
    'return { PALETTE, ASSET_CLASS, SUB_ASSET_COLORS, getSubAssetTextColor, getAssetClassTextColor };'
  )();

const byHex = {};
for (const [tok, hex] of Object.entries(PALETTE)) { (byHex[hex] = byHex[hex] || []).push(tok); }
const tok = (hex) => (byHex[hex] || ['<not-a-PALETTE-token>']).join('|');

console.log('SOURCE UNDER TEST : ' + SRC);
console.log('WCAG MATHS LIFTED FROM: ' + path.relative(process.cwd(), V5_INSTRUMENT).replace(/\\/g, '/') +
            '  (TO-V5-1 instrument -- extended, not re-implemented)');
console.log('PALETTE tokens: ' + Object.keys(PALETTE).length +
            ' | ASSET_CLASS keys: ' + Object.keys(ASSET_CLASS).length +
            ' | SUB_ASSET_COLORS keys: ' + Object.keys(SUB_ASSET_COLORS).length);
console.log('BOTH text-colour functions lifted from the file and EXECUTED.');
console.log('');

const t1 = ratio('#ffffff', '#000000'), t2 = ratio('#ffffff', '#ffffff');
console.log('INSTRUMENT SELF-TEST: white/black = ' + t1.toFixed(3) + ' (spec 21.000), white/white = ' +
            t2.toFixed(3) + ' (spec 1.000) -- ' +
            (Math.abs(t1 - 21) < 0.001 && Math.abs(t2 - 1) < 0.001 ? 'BOTH MATCH' : 'MISMATCH'));
console.log('');

let below = 0, absent = 0;
const rows = [];
const emit = (site, key, bg, fg, note) => {
  const r = ratio(fg, bg);
  if (r < FLOOR) below++;
  rows.push({ site, key, bg, fg, r, note });
  return r;
};

// ---------------------------------------------------------------------------
// 3. (i) The Structured-family sub-assets this cell re-bound or minted.
// ---------------------------------------------------------------------------
console.log('(i) STRUCTURED-FAMILY SUB-ASSETS -- text from getSubAssetTextColor(background)');
const SUB_SUBJECTS = [
  ['Volatility', 'RE-BOUND off PALETTE.blue900 to pink700 by this cell (Andrew ~19:5xZ)'],
  ['Options Income', 'MINTED on pink800 by this cell (PRD v0.8 C-COLOURS, Andrew ~20:2xZ)'],
  ['Hedge', 'unchanged by this cell -- carried for the family comparison'],
];
for (const [key, note] of SUB_SUBJECTS) {
  const bg = SUB_ASSET_COLORS[key];
  if (bg === undefined) {
    console.log('  ' + key.padEnd(16) + 'ABSENT from SUB_ASSET_COLORS');
    absent++;
    continue;
  }
  emit('SUB_ASSET_COLORS chip', key, bg, getSubAssetTextColor(bg), note);
}

// ---------------------------------------------------------------------------
// 4. (ii) THE CENSUS. Denominator first, then the subtraction.
// ---------------------------------------------------------------------------
function walk(dir) {
  const out = [];
  for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
    const p = path.join(dir, e.name);
    if (e.isDirectory()) out.push(...walk(p));
    else out.push(p.replace(/\\/g, '/'));
  }
  return out;
}
const allFiles = walk(PAGE_DIR);
const codeFiles = allFiles.filter((f) => /\.(ts|tsx)$/.test(f));
const importers = codeFiles.filter((f) => {
  const t = fs.readFileSync(f, 'utf8');
  return /import\s*\{[^}]*\bASSET_CLASS\b[^}]*\}\s*from\s*'@\/lib\/chartColors'/.test(t);
});

// Every LINE in an importer that touches an ASSET_CLASS-derived colour. This is the
// DENOMINATOR the population is subtracted from -- it is a sweep of the files, not a
// list of the sites the author remembered.
// WIDENED after a measured miss: the first version anchored on `ASSET_CLASS.` and
// `ASSET_CLASS_COLORS`, and a line reading `ASSET_CLASS_HEXES.has(subBg)` matched NEITHER
// -- so a site that DOES route a class background to the class rule sat outside the
// denominator and the census reported 3 sites while the file had 4. An aperture that
// cannot see a site reports it as absent, not as a failure. Both text-colour functions
// and both background helpers are now in the sweep, which widens the denominator and
// pushes the judgement into the printed bands where it can be read.
const COLOUR_REF = /ASSET_CLASS\.|ASSET_CLASS_COLORS|ASSET_CLASS_HEXES|getAssetClassBgColor|getAssetClassTextColor|getSubAssetTextColor|subAssetBg|COLORS\[|COLORS\.|c\.color|cellColor|getRowColor|getCellColor/;
const hits = [];
for (const f of importers) {
  const lines = fs.readFileSync(f, 'utf8').split('\n');
  lines.forEach((l, i) => {
    if (COLOUR_REF.test(l) && !/^\s*(\/\/|\*|\/\*)/.test(l)) {
      hits.push({ file: f, line: i + 1, src: l.trim() });
    }
  });
}

// Classify every hit. TEXT_OVER_CLASS is the population V6-AC9 grades; the other bands
// are the SUBTRACTION, each printed with its count so nothing leaves the denominator
// silently.
const band = (h) => {
  const s = h.src;
  // Checked BEFORE the text-colour band: an import line names the function without being
  // a render site, and counting it would inflate the population with two rows that draw
  // nothing. It stays in the denominator and is subtracted here, in the open.
  if (/^import /.test(s)) return 'IMPORT_DECLARATION';
  if (/getAssetClassTextColor/.test(s)) return 'TEXT_OVER_CLASS';
  if (/backgroundColor|fill=|background:/.test(s)) return 'BACKGROUND_ONLY';
  if (/\bcolor:\s*(c\.color|COLORS\.|COLORS\[)/.test(s)) return 'CLASS_COLOUR_AS_TEXT';
  if (/const |=>|return |interface |type |import /.test(s)) return 'DECLARATION_OR_LOOKUP';
  return 'OTHER';
};
const banded = {};
for (const h of hits) { (banded[band(h)] = banded[band(h)] || []).push(h); }

console.log('');
console.log('(ii) CENSUS -- ASSET_CLASS consumers under ' + PAGE_DIR);
console.log('  DENOMINATOR, files      : ' + allFiles.length + ' files under the page (' +
            codeFiles.length + ' .ts/.tsx)');
console.log('  ASSET_CLASS importers   : ' + importers.length + ' of ' + codeFiles.length +
            ' -> ' + importers.map((f) => path.basename(f)).join(', '));
console.log('  DENOMINATOR, colour refs: ' + hits.length + ' lines across those ' + importers.length + ' files');
console.log('  SUBTRACTION (every band printed; the population is what is LEFT):');
for (const [b, list] of Object.entries(banded).sort()) {
  console.log('    ' + b.padEnd(24) + String(list.length).padStart(3) + '  ' +
              (b === 'TEXT_OVER_CLASS' ? '<- THE POPULATION V6-AC9 GRADES' : 'excluded: draws no text over a class colour'));
}
const population = banded['TEXT_OVER_CLASS'] || [];
const popFiles = [...new Set(population.map((h) => h.file))];
console.log('  POPULATION: ' + population.length + ' sites across ' + popFiles.length + ' files');
population.forEach((h) => {
  console.log('    ' + h.file.replace(PAGE_DIR + '/', '') + ':' + h.line + '  ' + h.src.slice(0, 96));
});
console.log('');

// Every site in the population takes its text from getAssetClassTextColor, so the ratio
// question is: for EVERY background that function can be handed on this page, does it
// clear the floor? The backgrounds are the ASSET_CLASS registry itself -- all of them,
// not the five, because the map carries display aliases and an unmapped fallback.
console.log('  PER-SITE x PER-CLASS -- text from getAssetClassTextColor(background)');
console.log('  ' + 'site'.padEnd(46) + 'key'.padEnd(14) + 'background'.padEnd(26) + 'text'.padEnd(22) + 'ratio');
for (const h of population) {
  const site = (h.file.replace('portal/src/pages/Positioning/', '') + ':' + h.line);
  for (const [key, bg] of Object.entries(ASSET_CLASS)) {
    emit(site, key, bg, getAssetClassTextColor(bg), '');
  }
}
for (const row of rows.filter((r) => r.site.includes(':'))) {
  console.log('  ' + row.site.padEnd(46) + row.key.padEnd(14) +
              (tok(row.bg) + ' ' + row.bg).padEnd(26) +
              (tok(row.fg) + ' ' + row.fg).padEnd(22) +
              row.r.toFixed(3) + '  ' + (row.r >= FLOOR ? 'PASS' : 'BELOW FLOOR'));
}
console.log('');

console.log('  (i) TABLE -- the sub-asset chips');
console.log('  ' + 'site'.padEnd(46) + 'key'.padEnd(14) + 'background'.padEnd(26) + 'text'.padEnd(22) + 'ratio');
for (const row of rows.filter((r) => !r.site.includes(':'))) {
  console.log('  ' + row.site.padEnd(46) + row.key.padEnd(14) +
              (tok(row.bg) + ' ' + row.bg).padEnd(26) +
              (tok(row.fg) + ' ' + row.fg).padEnd(22) +
              row.r.toFixed(3) + '  ' + (row.r >= FLOOR ? 'PASS' : 'BELOW FLOOR') + '  [' + row.note + ']');
}
console.log('');

// ---------------------------------------------------------------------------
// 5. Negative controls -- the readings that made the class rule necessary.
// ---------------------------------------------------------------------------
console.log('NEGATIVE CONTROLS -- what WHITE text would have read on the class bases');
console.log('  white #ffffff on pink500  ' + PALETTE.pink500 + ' (Structured)   = ' +
            ratio('#ffffff', PALETTE.pink500).toFixed(3) + '  BELOW ' + FLOOR.toFixed(1));
console.log('  white #ffffff on yellow500 ' + PALETTE.yellow500 + ' (Commodities) = ' +
            ratio('#ffffff', PALETTE.yellow500).toFixed(3) + '  BELOW ' + FLOOR.toFixed(1));
console.log('  white #ffffff on blue500  ' + PALETTE.blue500 + ' (Equity)       = ' +
            ratio('#ffffff', PALETTE.blue500).toFixed(3) + '  BELOW ' + FLOOR.toFixed(1) +
            '  <- the pre-existing reading this cell also fixes');
console.log('  so getAssetClassTextColor returns gray900 for all three: ' +
            [PALETTE.pink500, PALETTE.yellow500, PALETTE.blue500]
              .every((c) => getAssetClassTextColor(c) === PALETTE.gray900));
console.log('');
console.log('THE pink700/pink800 CONDITIONAL the cell scopes ("enters lightBackgrounds ONLY if');
console.log('white text measures below ' + FLOOR.toFixed(1) + '"):');
for (const t of ['pink700', 'pink800']) {
  const r = ratio('#ffffff', PALETTE[t]);
  console.log('  white on ' + t + ' ' + PALETTE[t] + ' = ' + r.toFixed(3) +
              (r >= FLOOR ? '  >= floor -> correctly NOT added to lightBackgrounds'
                          : '  BELOW floor -> MUST be added to lightBackgrounds'));
  console.log('    ' + t + ' currently in lightBackgrounds: ' +
              (getSubAssetTextColor(PALETTE[t]) === PALETTE.gray900));
}
console.log('');

// ---------------------------------------------------------------------------
const graded = rows.length;
console.log('DENOMINATOR: ' + graded + ' (site, key) readings graded -- ' +
            population.length + ' class sites x ' + Object.keys(ASSET_CLASS).length +
            ' ASSET_CLASS backgrounds + ' + SUB_SUBJECTS.length + ' sub-asset chips; ' +
            absent + ' absent; ' + below + ' below the ' + FLOOR.toFixed(1) + ' floor.');
if (absent > 0 || below > 0 || population.length === 0) {
  console.log('VERDICT-BY-OUTPUT: FAIL (absent=' + absent + ', below_floor=' + below +
              ', population=' + population.length + ')');
  process.exitCode = 1;
} else {
  console.log('VERDICT-BY-OUTPUT: PASS -- ' + graded + ' of ' + graded + ' at or above ' +
              FLOOR.toFixed(1) + ':1, across ' + population.length + ' sites in ' +
              popFiles.length + ' files.');
}
