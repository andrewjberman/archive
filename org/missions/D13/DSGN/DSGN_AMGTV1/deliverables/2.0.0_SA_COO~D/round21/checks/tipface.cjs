/**
 * tipface.cjs -- DSGN_AMGTV1 round 21, AV-y-1 (issuer 2.0.0_SA_COO~D): THE FIGURE TOOLTIP SHOWS NO RAW CODE.
 *
 * Usage (repo root): node <this file>        (portal/ under the cwd is the checkout under test)
 * CTO ruling msg 27914: "(2) it shows the field's plain-English label and definition, never the raw Bloomberg mnemonic" (on the face).
 * FWD-13 (PRD :155-161): "its tooltip carries the mnemonic and the full-precision value verbatim" -- reconciled by the issuer: the
 * mnemonic stays CARRIED in the tooltip's markup (`data-mnemonic="<MNEMONIC>"`), never in its VISIBLE text.
 * THE CONTRACT, on `FigureTooltip` (StatTile.tsx; the header cards' and the Model tab's figure tooltip) fed `figureTooltipRows(<figure>)`:
 *   - VISIBLE text holds the plain label ("Enterprise value"), the definition, and the full-precision value verbatim;
 *   - VISIBLE text holds no Bloomberg-style code (a token of capitals/digits joined by an underscore, e.g. CURR_ENTP_VAL, EQY_BETA) and
 *     no "mnemonic" row label;
 *   - the markup carries the mnemonic in a `data-mnemonic` attribute.
 * Arms:
 *   1  THE CHECKOUT: the contract on two figures (CURR_ENTP_VAL, EQY_BETA).
 *   2  NEGATIVE: the pinned base StatTile.tsx (portal da0b3bd7; TIPFACE_BASE overrides) puts the mnemonic in the tooltip header text.
 *   3  PLANTED: a face with "(CURR_ENTP_VAL)" (CODE), a "mnemonic" row (ROWLABEL), a face missing the definition (DEFINITION), markup with
 *      no data-mnemonic (CARRIER) -- each rejected; a correct face passes.
 * Clipping (ruling part 1) is graded by the issuer's live walk, not here: a static render has no layout.
 * Prints one line per arm and "THE FIGURE TOOLTIP SHOWS NO RAW CODE: <k> of 3 arms"; exit 0 only at 3 of 3. Seconds.
 */
const path = require('path');
const { spawnSync } = require('child_process');

const ROOT = process.cwd();
const R15 = path.join(__dirname, '..', '..', 'round15');
const PIN = process.env.TIPFACE_BASE || 'da0b3bd7';
const FILE = 'src/pages/SecurityAnalysis/components/StatTile.tsx';
const CODE = /\b[A-Z][A-Z0-9]*_[A-Z0-9_]+\b/;
const textOf = (h) => h.replace(/<[^>]*>/g, ' ').replace(/&amp;/g, '&').replace(/&#x27;/g, "'").replace(/&quot;/g, '"').replace(/\s+/g, ' ').trim();
const FIGS = [
  { label: 'Enterprise value', fig: { value: 1020652.73573646, unit: 'MILLIONS', mnemonic: 'CURR_ENTP_VAL',
    basis: { definition: 'Current enterprise value (market cap + net debt + minority interest - equity affiliates), millions of the reporting currency.' },
    vintage: '2026-09-29', source: 'Bloomberg' } },
  { label: 'Beta', fig: { value: 1.5312, unit: 'RATIO', mnemonic: 'EQY_BETA',
    basis: { definition: 'Adjusted beta against the local index, two years of weekly returns.' }, vintage: '2026-09-29', source: 'Bloomberg' } },
];
function faults(html, label, fig) {
  const f = [];
  const t = textOf(html);
  const code = CODE.exec(t);
  if (code) f.push(`CODE: the visible face shows "${code[0]}"`);
  if (/\bmnemonic\b/i.test(t)) f.push('ROWLABEL: the visible face shows a "mnemonic" row');
  if (!t.includes(label)) f.push(`LABEL: the face lacks the plain label "${label}"`);
  if (!t.includes(fig.basis.definition)) f.push('DEFINITION: the face lacks the definition');
  if (!t.includes(String(fig.value))) f.push(`VALUE: the face lacks the full-precision value ${fig.value}`);
  if (!new RegExp(`data-mnemonic="${fig.mnemonic}"`).test(html)) f.push(`CARRIER: no data-mnemonic="${fig.mnemonic}" in the markup`);
  return f;
}

let L;
const f1 = [];
try {
  L = require(path.join(R15, 'checks', '_load.cjs'));
  // _load stubs every src/components/ import empty; this stub renders what DataTooltip.tsx renders as text: the header, the
  // optional aggregate, and each row's label then value.
  const h = L.React.createElement;
  const DataTooltip = ({ header, aggregate, rows }) => h('div', { 'data-stub': 'DataTooltip' },
    h('div', null, header),
    aggregate ? h('div', null, h('span', null, aggregate.label), h('span', null, aggregate.value)) : null,
    h('div', null, (rows || []).map((r, i) => h('div', { key: i }, h('span', null, r.label), h('span', null, r.value)))));
  for (const k of ['src/components/DataTooltip.tsx', 'src/components/DataTooltip']) L.stubSource(k, { __esModule: true, DataTooltip });
  const m = L.source(FILE);
  for (const { label, fig } of FIGS) {
    const html = L.render(m.FigureTooltip, { mnemonic: fig.mnemonic, label, rows: m.figureTooltipRows(fig) });
    f1.push(...faults(html, label, fig).map((x) => `${fig.mnemonic} ${x}`));
  }
} catch (e) { f1.push('RENDER: ' + String(e.message).split('\n')[0]); }
const a1 = f1.length === 0;

const f2 = [];
const s = spawnSync('git', ['-C', path.join(ROOT, 'portal'), 'show', `${PIN}:${FILE}`], { encoding: 'utf8', maxBuffer: 1 << 24 });
if (s.status !== 0 || !s.stdout) f2.push(`INPUT MISSING: git show ${PIN} rc=${s.status}`);
else if (!/header=\{`\$\{label\} \(\$\{mnemonic\}\)`\}/.test(s.stdout)) f2.push(`the base at ${PIN} does not put the mnemonic in the tooltip header -- the check cannot tell base from fix`);
const a2 = f2.length === 0;

const f3 = [];
const { label: L0, fig: F0 } = FIGS[0];
const face = ({ head = L0, rows = [['value', String(F0.value)], ['unit', 'MILLIONS'], ['definition', F0.basis.definition]], carrier = true } = {}) =>
  `<div role="tooltip"${carrier ? ` data-mnemonic="${F0.mnemonic}"` : ''}><div>${head}</div>${rows.map(([k, v]) => `<div><span>${k}</span><span>${v}</span></div>`).join('')}</div>`;
if (faults(face(), L0, F0).length) f3.push(`a correct face is rejected: ${faults(face(), L0, F0)[0]}`);
const M = [
  ['the code in the header', face({ head: `${L0} (${F0.mnemonic})` }), 'CODE'],
  ['a mnemonic row', face({ rows: [['value', String(F0.value)], ['mnemonic', 'enterprise value code'], ['definition', F0.basis.definition]] }), 'ROWLABEL'],
  ['no definition', face({ rows: [['value', String(F0.value)]] }), 'DEFINITION'],
  ['no carrier', face({ carrier: false }), 'CARRIER'],
];
const caught = [];
for (const [n, h, cls] of M) { if (faults(h, L0, F0).some((x) => x.startsWith(cls + ':'))) caught.push(n); else f3.push(`mutant "${n}" not rejected as ${cls}`); }
const a3 = f3.length === 0;

const arms = [
  ['the checkout: the label, definition and full value on the face; no raw code; the mnemonic carried in data-mnemonic', a1, a1 ? `0 faults (${FIGS.length} figures)` : `${f1.length} faults: ${f1.join(' | ')}`],
  [`NEGATIVE: the base StatTile.tsx (${PIN}) puts the mnemonic in the tooltip header`, a2, a2 ? 'base header carries "(mnemonic)"' : f2[0]],
  ['PLANTED: the code, a mnemonic row, a missing definition, a missing carrier are rejected; a correct face passes', a3, a3 ? `${caught.length} of ${M.length} rejected` : f3[0]],
];
let pass = 0;
for (const [n, ok, d] of arms) { if (ok) pass += 1; console.log(`${ok ? 'ARM PASS' : 'ARM FAIL'} ${n} :: ${d}`); }
console.log(`THE FIGURE TOOLTIP SHOWS NO RAW CODE: ${pass} of 3 arms`);
process.exit(pass === 3 ? 0 : 1);
