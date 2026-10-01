/**
 * modelhistory.cjs -- DSGN_AMGTV1 round 14, AV-k-5: AN ABSENT MODEL AND ITS HISTORY AGREE ON ONE FACE
 * (round-13 analysis ruling 6; FWD-15, FWD-19).
 *
 * Usage (repo root): node <this file>
 * Ruling 6: "the compare block, when the latest model is ABSENT, is headed as history ('Earlier versions of the pack held these
 * figures'). It is not hidden: the history is information a PM may want." The round-13 close render (model-empty.png, the
 * states-sweep payload = BA's /thesis with model_status ABSENT and the served /versions + /compare untouched) shows "No model in
 * the research pack for this name yet ..." beside "WHAT MOVED BETWEEN TWO VERSIONS ... 212 figures added": both true, read as a
 * contradiction.
 * Method: STATIC -- ModelTab.tsx rendered with the installed react-dom/server (loader _load.cjs), the page hooks stubbed:
 * useThesisBundle -> BA's served /thesis (or a labelled in-memory ABSENT variant), useModelVersions -> the served /versions,
 * useModelCompare -> the served /compare for the page's DEFAULT pair (oldest -> newest of the 16 versions:
 * compare.BA_US_Equity.oldest-latest.json, the pair model-empty.png shows), useInputLedger -> undefined.
 * Fixtures (round14/fixtures, SERVED, read-only captures): thesisBundle / versions / compare.*.oldest-latest for BA_US_Equity.
 * Arms:
 *   1  latest ABSENT + history served: the empty sentence is on the face AND the compare block is present, headed as history
 *      (earlier / previous versions, history) -- never the bare current "What moved between two versions" -- and still carries
 *      the served figures (the counts line and every changed line; not hidden)
 *   2  CONTROL, latest SERVED (BA's served bundle): the compare block keeps its current heading, no history heading, no empty
 *      sentence, and the figures are the served denominators and the SAME counts line and changed lines as arm 1's
 *   3  NEGATIVE, latest ABSENT and NO history (versions read ABSENT, 0 versions, no compare): only the empty sentence -- no
 *      compare block, no "figures added"; plus a detector probe: the history test rejects the planted current heading
 * Prints one line per arm and "AN ABSENT MODEL AND ITS HISTORY AGREE ON ONE FACE: <k> of 3 arms"; exit 0 only at 3 of 3.
 * No network, no AWS, writes no file.
 */
const L = require('./_load.cjs');
const S = require('./surfaces.cjs');
const clone = (x) => JSON.parse(JSON.stringify(x));
const K = 'BA_US_Equity';
const EMPTY = 'No model in the research pack for this name yet';
const CURRENT = 'What moved between two versions';
const HISTORY_RE = /\b(earlier|previous|prior|past|older)\b[^.]*\bversions?\b|\bhistory\b|\bhistorical\b/i;

const thesis = S.unwrap(L.fixture('thesisBundle.BA_US_Equity.json'));
const versions = S.unwrap(L.fixture('versions.BA_US_Equity.json'));
const compare = S.unwrap(L.fixture('compare.BA_US_Equity.oldest-latest.json'));
const den = compare.denominators || {};
const nChanged = ((compare.compared || {}).changed || []).length;

let T = thesis;
let V = versions;
let C = compare;
L.hookState.impl = Object.assign({}, L.hookState.impl, {
  useThesisBundle: (k) => (k === K ? T : (S.bundles[k] || undefined)),
  useModelVersions: () => V,
  useModelCompare: () => C,
  useInputLedger: () => undefined,
});
const MT = (() => { try { return L.source('src/pages/SecurityAnalysis/tabs/ModelTab.tsx'); } catch (e) { return null; } })();
const render = () => { try { return MT ? L.render(MT.ModelTab, { securityKey: K }) : ''; } catch (e) { return 'RENDER FAILED ' + e.message; } };

/** The face's compare block: heading (first <p>), counts line, changed lines; null when no compare block is rendered. */
function readCompare(html) {
  const inner = L.innerOf(html, 'data-model-compare', '');
  if (inner === null) return null;
  const head = /<p[^>]*>([\s\S]*?)<\/p>/.exec(inner);
  const countsInner = L.innerOf(inner, 'data-model-compare-counts', '');
  const lis = [...inner.matchAll(/<li[^>]*>([\s\S]*?)<\/li>/g)].map((m) => L.textOf(m[1]));
  return { heading: head ? L.textOf(head[1]) : '', counts: countsInner === null ? '' : L.textOf(countsInner), lis, text: L.textOf(inner) };
}
const wantCounts = `${den.added} figures added, ${den.removed} removed, ${den.changed} changed, ${den.unchanged} unchanged.`;

// ---- arm 1: latest ABSENT + history served ----------------------------------------------------------------------------------
T = Object.assign(clone(thesis), { model_status: 'ABSENT' }); // ISSUER VARIANT (in memory): the states-sweep model-empty payload
const h1 = render();
const c1 = readCompare(h1);
const f1 = [];
if (!h1 || /^RENDER FAILED/.test(h1)) f1.push(`the Model tab did not render (${h1.slice(0, 80) || 'no source'})`);
else {
  if (!L.textOf(h1).includes(EMPTY)) f1.push('the empty sentence is not on the face');
  if (!c1) f1.push('no compare block rendered (the history is hidden)');
  else {
    if (!HISTORY_RE.test(c1.heading)) f1.push(`the compare block is headed "${c1.heading}", not as history`);
    if (c1.heading.trim().toLowerCase() === CURRENT.toLowerCase()) f1.push('the compare block keeps the bare current heading');
    if (c1.counts !== wantCounts) f1.push(`counts line "${c1.counts}", want "${wantCounts}"`);
    if (c1.lis.length !== nChanged) f1.push(`${c1.lis.length} changed lines, want ${nChanged}`);
  }
}
const a1 = f1.length === 0;
const a1d = a1
  ? `empty sentence on the face; compare block headed "${c1.heading}"; ${c1.counts} ${c1.lis.length} of ${nChanged} changed lines shown`
  : `${f1.length} failing; first: ${f1[0]}`;

// ---- arm 2: CONTROL, latest SERVED ------------------------------------------------------------------------------------------
T = thesis;
const h2 = render();
const c2 = readCompare(h2);
const f2 = [];
if (thesis.model_status !== 'SERVED') f2.push(`the served bundle reads model_status ${thesis.model_status}, not SERVED`);
if (!h2 || /^RENDER FAILED/.test(h2)) f2.push('the Model tab did not render');
else if (!c2) f2.push('no compare block rendered on the served model');
else {
  if (c2.heading.trim().toLowerCase() !== CURRENT.toLowerCase()) f2.push(`heading "${c2.heading}", want "${CURRENT}"`);
  if (HISTORY_RE.test(c2.heading)) f2.push('the heading reads as history while the latest model is SERVED');
  if (L.textOf(h2).includes(EMPTY)) f2.push('the empty sentence shows on a served model');
  if (c2.counts !== wantCounts) f2.push(`counts line "${c2.counts}", want "${wantCounts}"`);
  if (c2.lis.length !== nChanged) f2.push(`${c2.lis.length} changed lines, want ${nChanged}`);
  if (c1 && (c1.counts !== c2.counts || JSON.stringify(c1.lis) !== JSON.stringify(c2.lis))) f2.push('the figures differ between the history and the current frame');
}
const a2 = f2.length === 0;
const a2d = a2
  ? `served model: heading "${c2.heading}", no history framing, no empty sentence; ${c2.counts} ${c2.lis.length} changed lines, identical to arm 1's`
  : `${f2.length} failing; first: ${f2[0]}`;

// ---- arm 3: NEGATIVE, latest ABSENT and NO history --------------------------------------------------------------------------
T = Object.assign(clone(thesis), { model_status: 'ABSENT' });
V = Object.assign(clone(versions), { versions: [], read: Object.assign({}, versions.read, { status: 'ABSENT', objects_listed: 0 }) });
C = undefined;
const h3 = render();
const t3 = L.textOf(h3);
T = thesis; V = versions; C = compare;
const f3 = [];
if (!h3 || /^RENDER FAILED/.test(h3)) f3.push('the Model tab did not render');
else {
  if (!t3.includes(EMPTY)) f3.push('the empty sentence is not on the face');
  if (readCompare(h3)) f3.push('a compare block renders with no history served');
  if (/figures? added/i.test(t3)) f3.push('"figures added" shows with no history served');
}
if (HISTORY_RE.test(CURRENT)) f3.push('detector probe: the planted current heading reads as history');
if (!HISTORY_RE.test('Earlier versions of the pack held these figures')) f3.push("detector probe: ruling 6's own heading does not read as history");
const a3 = f3.length === 0;
const a3d = a3
  ? 'no history served: the empty sentence alone, 0 compare blocks, 0 "figures added"; the probe rejects the planted current heading'
  : `${f3.length} failing; first: ${f3[0]}`;

const arms = [
  ['latest ABSENT: empty sentence beside a compare block headed as history', a1, a1d],
  ['control, latest SERVED: current heading and the same figures', a2, a2d],
  ['negative, latest ABSENT and no history: no compare block', a3, a3d],
];
let pass = 0;
for (const [name, ok, detail] of arms) { if (ok) pass += 1; console.log(`${ok ? 'ARM PASS' : 'ARM FAIL'} ${name} :: ${detail}`); }
console.log(`AN ABSENT MODEL AND ITS HISTORY AGREE ON ONE FACE: ${pass} of ${arms.length} arms`);
process.exit(pass === arms.length ? 0 : 1);
