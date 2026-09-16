// POSN_ASTTAX.TO-V5-1 / V5-AC3 -- the expansion of the placeholder <LOAD_ASSET_CLASS_MAP>.
// Loads the REAL ASSET_CLASS map out of portal/src/lib/chartColors.ts (no re-typing of any
// hex) and prints one colour per ratified class with its DENOMINATOR, so a collision cannot
// pass silently. Run from the worktree root:  node -e "require('./org/missions/D4/POSN/POSN_ASTTAX/deliverables/0.9.0_WK_POSN_ASTTAX~22/load_asset_class.js')"
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
  // the terminator begins with the newline, so the closing brace sits at end + 1
  return text.slice(open, end + 2);
}

// PALETTE and ASSET_CLASS both close on "} as const"; SUB_ASSET_COLORS closes on a bare "\n}".
const PALETTE_SRC = literal('PALETTE', '\n} as const');
const ASSET_SRC = literal('ASSET_CLASS', '\n} as const');
const SUB_SRC = literal('SUB_ASSET_COLORS', '\n}');

const ev = new Function(
  'const PALETTE = ' + PALETTE_SRC + ';\n' +
  'const ASSET_CLASS = ' + ASSET_SRC + ';\n' +
  'const SUB_ASSET_COLORS = ' + SUB_SRC + ';\n' +
  'return { PALETTE, ASSET_CLASS, SUB_ASSET_COLORS };'
);
const { PALETTE, ASSET_CLASS, SUB_ASSET_COLORS } = ev();

// hex -> every PALETTE token that carries it (an inversion can be many-to-one; print them all)
const byHex = {};
for (const [tok, hex] of Object.entries(PALETTE)) {
  (byHex[hex] = byHex[hex] || []).push(tok);
}
const tok = (hex) => (byHex[hex] || ['<not-a-PALETTE-token>']).join('|');

console.log('SOURCE: ' + SRC);
console.log('PALETTE tokens parsed: ' + Object.keys(PALETTE).length);
console.log('ASSET_CLASS keys parsed: ' + Object.keys(ASSET_CLASS).length +
            '  [' + Object.keys(ASSET_CLASS).join(', ') + ']');
console.log('SUB_ASSET_COLORS keys parsed: ' + Object.keys(SUB_ASSET_COLORS).length);
console.log('');

// The five ratified classes, PRD @99cc431075 s.3, in canonical order.
const RATIFIED = [
  ['1 Fixed Income / Cash', 'fixedIncome'],
  ['2 Equity', 'equity'],
  ['3 Structured', 'structured'],
  ['4 Commodities', 'commodities'],
  ['5 Alternatives', 'alternatives'],
];

console.log('THE FIVE RATIFIED CLASSES -- ASSET_CLASS.<key> -> PALETTE token -> hex');
const seen = new Map();
let missing = 0;
for (const [label, key] of RATIFIED) {
  const hex = ASSET_CLASS[key];
  if (hex === undefined) {
    console.log('  ' + label.padEnd(24) + ' ASSET_CLASS.' + key + ' -> ABSENT');
    missing += 1;
    continue;
  }
  console.log('  ' + label.padEnd(24) + ' ASSET_CLASS.' + key.padEnd(13) + ' -> ' +
              tok(hex).padEnd(14) + ' ' + hex);
  if (!seen.has(hex)) { seen.set(hex, []); }
  seen.get(hex).push(key);
}

const collisions = [...seen.entries()].filter(([, ks]) => ks.length > 1);
const distinct = seen.size;
console.log('');
console.log('DENOMINATOR: ' + RATIFIED.length + ' ratified classes; ' + missing + ' absent; ' +
            distinct + ' DISTINCT values across the ' + (RATIFIED.length - missing) + ' present.');
console.log('COLLISIONS AMONG THE RATIFIED FIVE: ' + collisions.length +
            (collisions.length ? ' -- ' + collisions.map(([h, ks]) => ks.join('+') + '=' + h).join(', ') : ''));

// The pre-existing alternatives / realEstate pair -- disclosed, NOT touched by this order.
console.log('');
console.log('PRE-EXISTING PAIR, DISCLOSED AND UNCHANGED BY TO-V5-1:');
console.log('  ASSET_CLASS.alternatives -> ' + tok(ASSET_CLASS.alternatives) + ' ' + ASSET_CLASS.alternatives);
console.log('  ASSET_CLASS.realEstate   -> ' + tok(ASSET_CLASS.realEstate) + ' ' + ASSET_CLASS.realEstate);
console.log('  SAME VALUE: ' + (ASSET_CLASS.alternatives === ASSET_CLASS.realEstate));
console.log('  realEstate is NOT one of the ratified five: PRD @99cc431075 s.3 row 5 holds');
console.log('  "real assets (not commodities), private equity, private credit, real estate" --');
console.log('  Real Estate is a SUB-ASSET of Alternatives (C-SUB-ASSET: `Real Estate` = VNQ),');
console.log('  so a class and its own sub-asset sharing orange500 is not a class-vs-class');
console.log('  collision. Pre-existing at the pin e85f6eb84f; this order changed neither line.');

// Negative control: the instrument must be able to SAY collision.
const fake = { a: '#111111', b: '#111111' };
const fseen = new Set(Object.values(fake));
console.log('');
console.log('NEGATIVE CONTROL (the collision detector on a known-colliding pair): 2 keys, ' +
            fseen.size + ' distinct, collision detected = ' + (fseen.size < 2));

// Non-zero exit if a ratified class is absent or two share a colour -- the criterion's bar.
if (missing > 0 || collisions.length > 0) {
  console.log('');
  console.log('VERDICT-BY-OUTPUT: FAIL (missing=' + missing + ', collisions=' + collisions.length + ')');
  process.exitCode = 1;
} else {
  console.log('');
  console.log('VERDICT-BY-OUTPUT: 5 of 5 ratified classes present, 5 of 5 DISTINCT, 0 collisions.');
}
