/**
 * datecontrast.cjs -- DSGN_AMGTV1 round 5, AV-v-6: ONE DATE FORM FOR THE PAGE'S OWN DATES, AND THE TIMELINE LEGEND READABLE ON
 * THE BAND (round-4 analysis s.4 item 6; FWD-11).
 *
 * Usage (repo root): node <this file>
 * SCOPE, measured at the cut: the page PRINTS dates in two forms of its own -- ISO "2026-02-26" (every served as_of / filed
 * date) and a short month form "Sep 29, 2026" (ThesisTab.tsx and ModelTab.tsx panel headers, `toLocaleDateString`), both on
 * ONE header line. The walker's long form ("December 31, 2025") is SERVED PROSE (filing passages, drafted sentences), which
 * C-PRESENTATION-ONLY forbids the page to rewrite -- out of scope, like "$1,234". The walker's low-contrast samples: "DENIED"
 * (the Mention timeline legend on the identity band) at 2.59:1, rgb(190,45,54) on rgb(25,38,67); its dialog samples (the
 * HeroDialog title / eyebrow on the gradient hero) are the check reading the white body under a dark hero -- the estate's
 * fixture, out of scope.
 * Renders ThesisTab and ModelTab on SAP GY (served fixture) and reads the TimelinePanel legend's colour expressions from its
 * source (the legend is `<span data-timeline-legend>` holding one span per state word).
 * Arms:
 *   1  the page's own panel-header dates are ONE form: the Thesis and Model panel headers (data-thesis-panel-header,
 *      data-model-panel-header) carry no month-name date (Jan..Dec + day + year) and each carries an ISO YYYY-MM-DD date
 *   2  the timeline legend's state words read on the band: every colour the legend's words use resolves (through the file's
 *      own constants) to `currentColor` or to a BAND-SCOPED token -- hsl(var(--danger|--warning|--success|--info|
 *      --palette-white|--palette-mediumGray)) -- which index.css's `.dark-band` block lightens for the band (danger 4.80:1,
 *      warning 5.27:1 on rgb(25,38,67)); never the light-canvas `--status-*` family (danger 2.59:1 there)
 *   3  the chart keeps its colours: the timeline's DENIED / PARTIAL day fills are unchanged (the file still defines
 *      DENIED_BASE / PARTIAL_BASE as the status-danger / status-warning fills it had at the cut) -- only the legend's words move
 * Prints one line per arm and "ONE DATE FORM AND A READABLE LEGEND: <k> of 3 arms"; exit 0 only at 3 of 3.
 */
const fs = require('fs');
const path = require('path');
const L = require('./_load.cjs');
const b = { SAP_GY_Equity: L.fixture('thesisBundle.SAP_GY_Equity.json') };
L.hookState.impl = { useThesisBundle: (k) => b[k], usePeerSet: () => undefined };
const MONTH = /\b(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.? \d{1,2}(st|nd|rd|th)?,? \d{4}\b/;
function header(file, exp, attr) {
  try {
    const h = L.render(L.source('src/pages/SecurityAnalysis/' + file)[exp], { securityKey: 'SAP_GY_Equity' });
    const inner = L.innerOf(h, attr);
    return inner === null ? null : L.textOf(inner);
  } catch (e) {
    console.log(`${exp} render failed: ` + String(e.message).split('\n')[0]);
    return null;
  }
}
const th = header('tabs/ThesisTab.tsx', 'ThesisTab', 'data-thesis-panel-header');
const mh = header('tabs/ModelTab.tsx', 'ModelTab', 'data-model-panel-header');
const oneForm = (t) => t !== null && !MONTH.test(t) && /\b\d{4}-\d{2}-\d{2}\b/.test(t);

// the same issuer-only CHECK_SRC_OVERRIDE the loader honours (a worker never sets it)
const TL = 'src/pages/SecurityAnalysis/components/TimelinePanel.tsx';
const ov = (process.env.CHECK_SRC_OVERRIDE || '').split(';').filter(Boolean).map((p) => [p.slice(0, p.indexOf('=')), p.slice(p.indexOf('=') + 1)]).find(([k]) => k === TL);
const src = fs.readFileSync(ov ? ov[1] : path.join(L.base, TL), 'utf8');
const consts = {};
for (const m of src.matchAll(/^const ([A-Z_]+) = '([^']*)'/gm)) consts[m[1]] = m[2];
const legend = L.innerOf(src.replace(/\{' -- '\}/g, ''), 'data-timeline-legend') || '';
const colours = [...legend.matchAll(/color:\s*([^}]+?)\s*\}/g)].map((m) => m[1].trim());
const resolve = (e) => (/^'.*'$/.test(e) ? e.slice(1, -1) : consts[e] !== undefined ? consts[e] : e);
const resolved = colours.map(resolve);
const BAND = /^(currentColor|hsl\(var\(--(danger|warning|success|info|palette-white|palette-mediumGray)\)\))$/;
const bad = resolved.filter((c) => !BAND.test(c));
const fillsKept = consts.DENIED_BASE === 'hsl(var(--status-danger))' && consts.PARTIAL_BASE === 'hsl(var(--status-warning))';

const arms = [
  ['the page\'s own panel-header dates are one ISO form', oneForm(th) && oneForm(mh),
    `thesis header ${th === null ? 'absent' : `"${(th.match(MONTH) || [''])[0] || 'no month form'}"`}; model header ${mh === null ? 'absent' : `"${(mh.match(MONTH) || [''])[0] || 'no month form'}"`}`],
  ['the timeline legend\'s words use band-scoped ink', colours.length >= 3 && bad.length === 0,
    `${colours.length} legend colour(s): ${JSON.stringify(resolved)}; off-band ${bad.length}`],
  ['the chart\'s DENIED / PARTIAL fills unchanged', fillsKept, `DENIED_BASE=${consts.DENIED_BASE}; PARTIAL_BASE=${consts.PARTIAL_BASE}`],
];
let pass = 0;
for (const [name, ok, detail] of arms) {
  if (ok) pass += 1;
  console.log(`${ok ? 'ARM PASS' : 'ARM FAIL'} ${name} :: ${detail}`);
}
console.log(`ONE DATE FORM AND A READABLE LEGEND: ${pass} of ${arms.length} arms`);
process.exit(pass === arms.length ? 0 : 1);
