/**
 * panelhead.cjs -- DSGN_AMGTV1 round 15, AV-n-3: THE LEAD PANEL HEADER LOOKS LIKE THE PORTAL (FWD-23; C-ESTATE-FIXTURES).
 *
 * Usage (repo root): cd "$(git rev-parse --show-toplevel)" && node <this file>
 * `portal/` under the working directory is the checkout under test; the base is portal commit b336b141 (DEV). The loader,
 * the probe and the markup helpers are cardface.cjs's (required, not run): the REAL sources of src/pages/**, src/lib/**
 * and src/ui/components/graphic/** (so the shared card face renders for real and is probed), every other estate piece a
 * named stub (`Panel`, `PanelHeader`, `PanelContent`, `Segmented` ... render <div data-stub="<Name>"> with their text
 * props, their options, their children and every element-valued prop as a slot -- a stub renders no <button> of its own).
 * The page's hooks are stubbed on round14/fixtures/rankings.TRENDING_PRICE.json (useLeadPanelRankings); the starred list
 * is empty, the rank series absent, any other hook returns no data.
 *
 * THE CONTRACT THE WORKER BUILDS TO (exact):
 *   - The Lead Panel's header is built from the /philosophy card face: LeadPanel renders its header through `GraphicCard`
 *     (portal/src/ui/components/graphic/GraphicCard.tsx, cardface.cjs's contract), measured by the check's probe
 *     <div data-probe-graphic-card> carrying the GraphicPanel face marker, BEFORE the panel body (the first `PanelContent`
 *     stub; all of the render when there is none).
 *   - THE HEADER REGION = every probed GraphicCard render before the body, plus every `PanelHeader` stub.
 *   - The Starred filter is a `Segmented` (stub name) in the header region INSIDE the probed header, recognised by its
 *     ariaLabel or one of its option values/labels matching /starred/i.
 *   - HAND-BUILT BUTTON = an intrinsic <button> element anywhere in the header region, except the shared face's own root
 *     element (a probe's direct child). Estate controls are stubs and render no <button>, so every <button> counted is one
 *     the page wrote. Want 0. (The search <input> is not counted: the estate has no input control to require.)
 *   - Visible text (every text node of the LeadPanel render, stub text spans included) never matches /lead[\s-]?panel/i.
 *   - COLOUR LINT: in portal/src/pages/SecurityAnalysis/components/{LeadPanel,PriceBars,ChatterBubbles}.tsx, transpiled with
 *     comments removed (a colour named in a comment is not a literal), 0 hex colour literals (#rgb, #rgba, #rrggbb,
 *     #rrggbbaa) and 0 raw Tailwind palette shades (text|bg|border|fill|stroke|ring|from|via|to|outline|decoration|divide|
 *     placeholder|accent|caret|shadow - <palette hue> - 50..950); colours come from lib/chartColors.ts or the CSS tokens. A
 *     file that does not exist is skipped and reported. RankedChart.tsx's count is printed for information, ungraded.
 * Arms:
 *   1  the criterion on the checkout: all five clauses above (no internal name, header through the face, Starred is a
 *      Segmented in it, 0 hand-built buttons, colour lint 0)
 *   2  the negative: the same predicate on the b336b141 sources FAILS for the stated reasons -- the visible title "Lead Panel"
 *      and the hand-built Starred <button> (data-starred-toggle) in the header region
 *   3  the planted controls: the checkout's LeadPanel.tsx with one hex literal appended (`'#ff00ff'`) and, separately, one
 *      raw Tailwind shade appended (`'text-red-500'`) are each rejected by the colour lint
 * Writes only under os.tmpdir() (the base source copies). No network, no AWS.
 * Wall time measured on site Z (2026-10-01): base checkout 2.1 s (2 of 3), green C:/tmp/dsgn-r15-green-b 2.0 s (3 of 3).
 * Prints one line per arm and "THE LEAD PANEL HEADER LOOKS LIKE THE PORTAL: <k> of 3 arms"; exit 0 only at 3 of 3.
 */
const fs = require('fs');
const os = require('os');
const path = require('path');
const C = require('./cardface.cjs');
const L = require('./_load.cjs'); // fixture lookup only (round 15 then round 14)

const T0 = Date.now();
const TMP = fs.mkdtempSync(path.join(os.tmpdir(), 'r15-panelhead-'));
const LEAD_REL = 'src/pages/SecurityAnalysis/components/LeadPanel.tsx';
const LINT_FILES = ['LeadPanel', 'PriceBars', 'ChatterBubbles'].map((n) => `src/pages/SecurityAnalysis/components/${n}.tsx`);
const INFO_FILES = ['src/pages/SecurityAnalysis/components/RankedChart.tsx'];
const HEX = /#(?:[0-9a-fA-F]{8}|[0-9a-fA-F]{6}|[0-9a-fA-F]{3,4})(?![0-9a-zA-Z_])/g;
const SHADE = /(?<![\w-])(?:text|bg|border(?:-[trblxyse])?|fill|stroke|ring(?:-offset)?|from|via|to|outline|decoration|divide|placeholder|accent|caret|shadow)-(?:slate|gray|zinc|neutral|stone|red|orange|amber|yellow|lime|green|emerald|teal|cyan|sky|blue|indigo|violet|purple|fuchsia|pink|rose)-(?:50|[1-9]00|950)(?:\/\d+)?(?![\w-])/g;
const unwrap = (x) => (x && x.payload && (x._capture_note || x._capture) ? x.payload : x);
const rankings = unwrap(L.fixture('rankings.TRENDING_PRICE.json'));
const noop = () => {};
const PROPS = {
  movement: 'TRENDING', setMovement: noop, subject: 'PRICE', setSubject: noop, starredOnly: false, setStarredOnly: noop,
  view: 'list', setView: noop, selectedSecurityKey: null, onSelectSecurity: noop, onClearSecuritySelection: noop,
  searchInput: '', setSearchInput: noop,
};
const HOOKS = { useLeadPanelRankings: () => rankings, useStarredList: () => [], useSetStarred: () => undefined, useRankTimeSeries: () => undefined };

function lint(text) {
  const js = C.ts.transpileModule(text, {
    compilerOptions: { module: C.ts.ModuleKind.CommonJS, jsx: C.ts.JsxEmit.ReactJSX, target: C.ts.ScriptTarget.ES2022, removeComments: true },
  }).outputText;
  return { hex: js.match(HEX) || [], shade: js.match(SHADE) || [] };
}
function lintTree(tree, overrides) {
  const per = [];
  for (const rel of LINT_FILES) {
    const text = overrides && overrides[rel] !== undefined ? overrides[rel] : tree.read(rel);
    if (text === null) { per.push({ rel, skipped: true }); continue; }
    per.push(Object.assign({ rel }, lint(text)));
  }
  return per;
}
const lintTotal = (per) => per.reduce((n, p) => n + (p.skipped ? 0 : p.hex.length + p.shade.length), 0);
const lintWords = (per) => per.map((p) => `${path.basename(p.rel, '.tsx')} ${p.skipped ? 'absent, skipped' : `hex ${p.hex.length}${p.hex.length ? ` [${p.hex.slice(0, 3).join(' ')}]` : ''} shade ${p.shade.length}${p.shade.length ? ` [${p.shade.slice(0, 3).join(' ')}]` : ''}`}`).join('; ');

/** The full predicate on one source tree. Returns { fails: [...], facts: {...} }. */
function grade(tree, label) {
  const fails = [];
  const facts = {};
  let html;
  try {
    const ld = C.makeLoader(tree, { probe: true, hooks: HOOKS });
    const { LeadPanel } = ld.load(LEAD_REL);
    html = C.render(LeadPanel, PROPS);
    facts.marker = C.faceMarker(ld);
  } catch (e) {
    fails.push(`${label}: the LeadPanel render threw: ${String(e.message).split('\n')[0]}`);
    return { fails, facts };
  }
  const t = C.parse(html);
  const text = C.words(t).join(' ');
  const internal = text.match(/lead[\s-]?panel/gi) || [];
  facts.internal = internal.length;
  if (internal.length) fails.push(`visible text carries the internal name: "${internal[0]}" (${internal.length}x)`);

  const content = C.all(t, (n) => C.attr(n, 'data-stub') === 'PanelContent')[0];
  const contentAt = content ? content.start : Infinity;
  const headProbes = C.probesOf(t).filter((p) => p.start < contentAt);
  const faced = headProbes.filter((p) => C.hasMarker(p, facts.marker));
  const panelHeaders = C.all(t, (n) => C.attr(n, 'data-stub') === 'PanelHeader');
  const roots = [...headProbes, ...panelHeaders].filter((r, _i, arr) => !C.ancestors(r).some((a) => arr.includes(a)));
  facts.headerProbes = headProbes.length;
  facts.faced = faced.length;
  facts.panelHeaders = panelHeaders.length;
  if (!faced.length) fails.push(`the header is not built from the card face (${headProbes.length} GraphicCard renders before the body, ${faced.length} with the GraphicPanel face)`);

  const segs = [];
  for (const r of roots) segs.push(...[r, ...C.all(r, () => true)].filter((n) => C.attr(n, 'data-stub') === 'Segmented'));
  const isStarred = (s) => /starred/i.test(C.attr(s, 'data-stub-arialabel') || '') || C.all(s, (n) => C.attr(n, 'data-stub-option') !== null).some((o) => /starred/i.test(C.attr(o, 'data-stub-option') + ' ' + C.words(o).join(' ')));
  const starredSegs = segs.filter(isStarred);
  const starredInFace = starredSegs.filter((s) => C.ancestors(s).some((a) => faced.includes(a)));
  facts.segmented = segs.length;
  facts.starredSegmented = starredSegs.length;
  if (!starredSegs.length) fails.push(`the Starred filter is not a Segmented in the header (${segs.length} Segmented in the header region, none starred)`);
  else if (!starredInFace.length) fails.push('the Starred Segmented sits outside the card-face header');

  const faceRoots = new Set(headProbes.map((p) => p.children.find((c) => c.tag)).filter(Boolean));
  const buttons = [];
  for (const r of roots) for (const b of [r, ...C.all(r, () => true)]) if (b.tag === 'button' && !faceRoots.has(b) && !buttons.includes(b)) buttons.push(b);
  facts.handButtons = buttons.length;
  facts.handButtonWords = buttons.map((b) => `${C.attr(b, 'data-starred-toggle') !== null ? '[data-starred-toggle] ' : ''}"${C.words(b).join(' ')}"`);
  if (buttons.length) fails.push(`${buttons.length} hand-built <button> in the header region: ${facts.handButtonWords.join(', ')}`);

  const per = lintTree(tree);
  facts.lint = lintWords(per);
  facts.lintTotal = lintTotal(per);
  if (facts.lintTotal) fails.push(`hard-coded colour in the panel files: ${facts.lint}`);
  return { fails, facts };
}
const factLine = (f) => `internal-name hits ${f.internal}; header GraphicCard renders ${f.headerProbes} (${f.faced} with the face), PanelHeader stubs ${f.panelHeaders}; Segmented in header ${f.segmented} (starred ${f.starredSegmented}); hand-built buttons ${f.handButtons}; lint: ${f.lint}`;

const WORK = C.workingTree();
const BASE = C.baseTree(TMP);

// ---------------- arm 1: the criterion on the checkout ----------------
const G = grade(WORK, 'checkout');
const a1 = G.fails.length === 0;
const a1d = (a1 ? '' : `${G.fails.length} failing; first: ${G.fails[0]} || `) + (G.facts.internal !== undefined ? factLine(G.facts) : '');

// ---------------- arm 2: the negative at base ----------------
const B = grade(BASE, 'base');
const f2 = [];
if (B.facts.internal === undefined) f2.push(`the base did not render: ${B.fails[0]}`);
else {
  if (!(B.facts.internal > 0)) f2.push('the base title "Lead Panel" is not caught');
  if (!(B.facts.handButtons > 0) || !B.facts.handButtonWords.some((w) => w.includes('[data-starred-toggle]'))) f2.push('the base hand-built Starred button is not caught');
  if (B.fails.length === 0) f2.push('the base passes the predicate');
}
const a2 = f2.length === 0;
const a2d = (a2 ? `the base FAILS ${B.fails.length} clauses: ${B.fails.join(' | ')}` : `${f2.length} failing; first: ${f2[0]}`) + (B.facts.internal !== undefined ? ` || ${factLine(B.facts)}` : '');

// ---------------- arm 3: the planted colour mutants ----------------
const f3 = [];
const n3 = [];
const leadText = WORK.read(LEAD_REL);
if (leadText === null) f3.push('no checkout LeadPanel.tsx to mutate');
else {
  const before = lintTotal(lintTree(WORK));
  for (const [name, lit] of [['hex', "'#ff00ff'"], ['shade', "'text-red-500'"]]) {
    const mutant = `${leadText}\nexport const R15B_MUTANT_COLOUR = ${lit}\n`;
    const after = lintTotal(lintTree(WORK, { [LEAD_REL]: mutant }));
    if (after !== before + 1) f3.push(`the ${name} mutant ${lit} is not rejected (lint ${before} -> ${after})`);
    else n3.push(`${name} mutant ${lit}: lint ${before} -> ${after}, rejected`);
  }
}
const info = INFO_FILES.map((rel) => { const tx = WORK.read(rel); if (tx === null) return `${path.basename(rel)} absent`; const r = lint(tx); return `${path.basename(rel)} hex ${r.hex.length} shade ${r.shade.length} (ungraded)`; }).join('; ');
const a3 = f3.length === 0;
const a3d = (a3 ? n3.join('; ') : `${f3.length} failing; first: ${f3[0]}`) + `; info: ${info}`;

console.log(`RUNS: base b336b141 sources in ${BASE.dir}; wall ${Math.round((Date.now() - T0) / 100) / 10}s`);
const arms = [
  ['the checkout: no internal name, header through the card face, Starred a Segmented, 0 hand-built buttons, 0 hard-coded colours', a1, a1d],
  ['the negative: the b336b141 panel fails for its "Lead Panel" title and hand-built Starred button', a2, a2d],
  ['the planted controls: a hex literal and a raw Tailwind shade in LeadPanel.tsx are rejected', a3, a3d],
];
let pass = 0;
for (const [name, ok, detail] of arms) { if (ok) pass += 1; console.log(`${ok ? 'ARM PASS' : 'ARM FAIL'} ${name} :: ${detail}`); }
console.log(`THE LEAD PANEL HEADER LOOKS LIKE THE PORTAL: ${pass} of ${arms.length} arms`);
process.exit(pass === arms.length ? 0 : 1);
