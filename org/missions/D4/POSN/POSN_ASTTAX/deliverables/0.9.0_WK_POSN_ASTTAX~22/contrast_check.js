// POSN_ASTTAX.TO-V5-1 / V5-AC8 -- the expansion of the placeholder <CONTRAST_CHECK>.
// For EACH sub-asset background this cell added or moved ('Metals', 'Commodities',
// 'Hedge') it prints the text colour the file's OWN getSubAssetTextColor returns and the
// WCAG 2.x contrast ratio of that text on that background, as a (key, background, text,
// ratio) table. Nothing is re-typed and nothing is re-implemented: the palette, the
// sub-asset map AND the text-colour function are all lifted out of
// portal/src/lib/chartColors.ts and executed, so a wrong binding cannot pass silently.
// Run from the worktree root:
//   node -e "require('./org/missions/D4/POSN/POSN_ASTTAX/deliverables/0.9.0_WK_POSN_ASTTAX~22/contrast_check.js')"
'use strict';
const fs = require('fs');

const SRC = 'portal/src/lib/chartColors.ts';
const text = fs.readFileSync(SRC, 'utf8');

function literal(name, terminator) {
  const head = 'export const ' + name;
  const i = text.indexOf(head);
  if (i < 0) { throw new Error('ABSENT: ' + name + ' not found in ' + SRC); }
  const open = text.indexOf('{', i);
  const end = text.indexOf(terminator, open);
  if (open < 0 || end < 0) { throw new Error('UNPARSEABLE: ' + name); }
  return text.slice(open, end + 2);
}

// The REAL function, lifted verbatim: from 'export function getSubAssetTextColor' to the
// first line that is a bare closing brace. TypeScript annotations are stripped so node
// can evaluate it; the BRANCH LOGIC and the lightBackgrounds membership are untouched.
function fnBody(name) {
  const i = text.indexOf('export function ' + name);
  if (i < 0) { throw new Error('ABSENT: function ' + name); }
  const end = text.indexOf('\n}', i);
  if (end < 0) { throw new Error('UNPARSEABLE: function ' + name); }
  return text.slice(i + 'export '.length, end + 2)
    .replace('(bgHex: string): string', '(bgHex)')
    .replace('const lightBackgrounds: string[] =', 'const lightBackgrounds =');
}

const PALETTE_SRC = literal('PALETTE', '\n} as const');
const SUB_SRC = literal('SUB_ASSET_COLORS', '\n}');
const FN_SRC = fnBody('getSubAssetTextColor');

const ev = new Function(
  'const PALETTE = ' + PALETTE_SRC + ';\n' +
  'const SUB_ASSET_COLORS = ' + SUB_SRC + ';\n' +
  FN_SRC + '\n' +
  'return { PALETTE, SUB_ASSET_COLORS, getSubAssetTextColor };'
);
const { PALETTE, SUB_ASSET_COLORS, getSubAssetTextColor } = ev();

// WCAG 2.x relative luminance + contrast ratio (sRGB), the published formula.
function luminance(hex) {
  const h = hex.trim().replace('#', '');
  if (!/^[0-9a-fA-F]{6}$/.test(h)) { throw new Error('NOT A 6-DIGIT HEX: ' + hex); }
  const c = [0, 2, 4].map(function (i) {
    const v = parseInt(h.slice(i, i + 2), 16) / 255;
    return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4);
  });
  return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2];
}
function ratio(a, b) {
  const la = luminance(a), lb = luminance(b);
  const hi = Math.max(la, lb), lo = Math.min(la, lb);
  return (hi + 0.05) / (lo + 0.05);
}

// hex -> PALETTE token(s), so the table names the token and not only the hex.
const byHex = {};
for (const [tok, hex] of Object.entries(PALETTE)) { (byHex[hex] = byHex[hex] || []).push(tok); }
const tok = (hex) => (byHex[hex] || ['<not-a-PALETTE-token>']).join('|');

console.log('SOURCE: ' + SRC);
console.log('PALETTE tokens parsed: ' + Object.keys(PALETTE).length +
            '; SUB_ASSET_COLORS keys parsed: ' + Object.keys(SUB_ASSET_COLORS).length);
console.log('getSubAssetTextColor lifted from the file and EXECUTED (not re-implemented).');
console.log('');

// SELF-TEST of the contrast instrument on two pairs whose answer is fixed by the spec.
const t1 = ratio('#ffffff', '#000000'), t2 = ratio('#ffffff', '#ffffff');
console.log('INSTRUMENT SELF-TEST: white/black = ' + t1.toFixed(3) + ' (spec 21.000), ' +
            'white/white = ' + t2.toFixed(3) + ' (spec 1.000) -- ' +
            (Math.abs(t1 - 21) < 0.001 && Math.abs(t2 - 1) < 0.001 ? 'BOTH MATCH' : 'MISMATCH'));
console.log('');

// The subjects: every sub-asset background TO-V5-1 added or moved.
const SUBJECTS = [
  ['Metals', 'ADDED by this cell'],
  ['Commodities', 'MOVED off PALETTE.blue950 by this cell'],
  ['Hedge', 'RE-BOUND off PALETTE.green900 by this cell'],
];
const FLOOR = 4.5;

console.log('(key, background, text, ratio) -- text colour from getSubAssetTextColor(background)');
console.log('  ' + 'key'.padEnd(13) + 'background'.padEnd(26) + 'text'.padEnd(22) + 'ratio   floor ' + FLOOR.toFixed(1));
let below = 0, absent = 0;
for (const [key, note] of SUBJECTS) {
  const bg = SUB_ASSET_COLORS[key];
  if (bg === undefined) {
    console.log('  ' + key.padEnd(13) + 'ABSENT from SUB_ASSET_COLORS');
    absent += 1;
    continue;
  }
  const fg = getSubAssetTextColor(bg);
  const r = ratio(fg, bg);
  if (r < FLOOR) { below += 1; }
  console.log('  ' + key.padEnd(13) +
              (tok(bg) + ' ' + bg).padEnd(26) +
              (tok(fg) + ' ' + fg).padEnd(22) +
              r.toFixed(3) + '  ' + (r >= FLOOR ? 'PASS' : 'BELOW FLOOR') + '   [' + note + ']');
}

console.log('');
console.log('NEGATIVE CONTROL -- the pre-amendment reading the amendment fixed:');
console.log('  white #ffffff on yellow500 ' + PALETTE.yellow500 + ' = ' +
            ratio('#ffffff', PALETTE.yellow500).toFixed(3) +
            '  (what Metals/Commodities rendered at before PALETTE.yellow500 entered');
console.log('   lightBackgrounds -- BELOW the ' + FLOOR.toFixed(1) + ' floor, which is why it moved)');
console.log('  yellow500 in lightBackgrounds now: ' +
            (getSubAssetTextColor(PALETTE.yellow500) === PALETTE.gray900));
console.log('');
console.log('THE PINK CONDITIONAL the cell scopes ("white-on-pink only if it measures >= 4.5"):');
console.log('  white   #ffffff on pink600 ' + PALETTE.pink600 + ' = ' +
            ratio('#ffffff', PALETTE.pink600).toFixed(3) + '  <- the binding chosen, >= ' + FLOOR.toFixed(1));
console.log('  gray900 ' + PALETTE.gray900 + ' on pink600 ' + PALETTE.pink600 + ' = ' +
            ratio(PALETTE.gray900, PALETTE.pink600).toFixed(3) +
            '  <- what adding pink600 to lightBackgrounds WOULD have given: BELOW the floor.');
console.log('  So pink600 is correctly NOT in lightBackgrounds. pink600 in lightBackgrounds: ' +
            (getSubAssetTextColor(PALETTE.pink600) === PALETTE.gray900));
console.log('  (class base, for the record: white on pink500 ' + PALETTE.pink500 + ' = ' +
            ratio('#ffffff', PALETTE.pink500).toFixed(3) + ' -- ASSET_CLASS.structured is not a chip background,');
console.log('   it is not read by getSubAssetTextColor, and this cell did not change it.)');

console.log('');
console.log('DENOMINATOR: ' + SUBJECTS.length + ' of ' + SUBJECTS.length +
            ' backgrounds this cell added or moved were read; ' + absent + ' absent; ' +
            below + ' below the ' + FLOOR.toFixed(1) + ' floor.');
if (absent > 0 || below > 0) {
  console.log('VERDICT-BY-OUTPUT: FAIL (absent=' + absent + ', below_floor=' + below + ')');
  process.exitCode = 1;
} else {
  console.log('VERDICT-BY-OUTPUT: ' + SUBJECTS.length + ' of ' + SUBJECTS.length +
              ' at or above ' + FLOOR.toFixed(1) + ':1.');
}
