/**
 * posturecite.cjs -- DSGN_AMGTV1 round 5, AV-v-1: POSTURE CITES READ AS WORDS (round-4 analysis s.4 item 1; FWD-10, FWD-11).
 *
 * Usage (repo root): node <this file>
 * Renders the Posture tab on SAP GY (comparable ANET US) and on Valero (comparable WMB), served fixtures under
 * round5/fixtures, and reads the VISIBLE text of every cite line (`<li data-posture-cite=...>`), collapsed <details>
 * content included (the cites sit in a drawer a PM opens). The raw cite stays free on the `data-posture-cite` attribute.
 * The CODE classes read on the visible text:
 *   passage id   \bP\d{4}\b                       (E:P0102 -> "passage P0102")
 *   preset code  every fit-preset key and every membership book the posture object serves on that name
 *                (read from the fixture -- DIVZ, IDVZ, PFDE, PFOE today), as a whole word
 *   status word  ABSENT | SERVED | PRESENT | REFUSED | UNRESOLVED as a whole upper-case word
 * Arms:
 *   1  SAP GY: 0 passage ids on the cite lines, AND every cite still renders (the cite-line count equals the object's own
 *      cite count, so no cite was dropped to reach the zero)
 *   2  SAP GY: 0 preset codes and 0 status words on the cite lines
 *   3  Valero: 0 hits of all three classes on the cite lines, every cite still rendered
 * Prints one line per arm and "POSTURE CITES IN WORDS: <k> of 3 arms"; exit 0 only at 3 of 3.
 */
const L = require('./_load.cjs');
const bundles = {};
for (const k of ['VLO_US_Equity', 'SAP_GY_Equity', 'WMB_US_Equity']) bundles[k] = L.fixture(`thesisBundle.${k}.json`);
L.hookState.impl = { useThesisBundle: (k) => bundles[k], usePeerSet: () => undefined };

function render(key) {
  try {
    return L.render(L.source('src/pages/SecurityAnalysis/tabs/PostureTab.tsx').PostureTab, { securityKey: key });
  } catch (e) {
    console.log(`${key} render failed: ` + String(e.message).split('\n')[0]);
    return '';
  }
}
function citeLines(html) {
  const out = [];
  const re = /<li[^>]*data-posture-cite="[^"]*"[^>]*>([\s\S]*?)<\/li>/g;
  let m;
  while ((m = re.exec(html)) !== null) out.push(L.textOf(m[1]));
  return out;
}
function codesFor(key) {
  const p = bundles[key].posture || {};
  const set = new Set();
  for (const side of Object.values(p.fit || {})) for (const k of Object.keys((side && side.presets) || {})) set.add(k);
  for (const mem of [p.membership, p.comparable_membership]) for (const b of (mem && mem.books) || []) set.add(b);
  for (const mem of [p.membership, p.comparable_membership]) for (const b of Object.keys((mem && mem.holdings_source) || {})) set.add(b);
  return [...set];
}
function objectCites(key) {
  return ((bundles[key].posture || {}).basis || []).reduce((n, c) => n + ((c.cites || []).length), 0);
}
const PASSAGE = /\bP\d{4}\b/g;
const STATUS = /\b(ABSENT|SERVED|PRESENT|REFUSED|UNRESOLVED)\b/g;
function tally(key) {
  const html = render(key);
  const lines = citeLines(html);
  const text = lines.join(' | ');
  const codes = codesFor(key);
  const presetRe = codes.length ? new RegExp('\\b(' + codes.join('|') + ')\\b', 'g') : /$^/g;
  return {
    rendered: html.length > 0,
    lines: lines.length,
    expected: objectCites(key),
    passage: text.match(PASSAGE) || [],
    preset: text.match(presetRe) || [],
    status: text.match(STATUS) || [],
  };
}
const sap = tally('SAP_GY_Equity');
const vlo = tally('VLO_US_Equity');
const show = (xs) => `${xs.length}${xs.length ? ' ' + JSON.stringify(xs.slice(0, 6)) : ''}`;
const arms = [
  ['no passage id on the cite lines, every cite rendered (SAP GY)', sap.rendered && sap.passage.length === 0 && sap.lines === sap.expected,
    `passage ids ${show(sap.passage)}; cite lines ${sap.lines} of ${sap.expected}`],
  ['no preset code and no status word on the cite lines (SAP GY)', sap.rendered && sap.lines > 0 && sap.preset.length === 0 && sap.status.length === 0,
    `preset codes ${show(sap.preset)}; status words ${show(sap.status)}`],
  ['no passage id, preset code or status word, every cite rendered (Valero)',
    vlo.rendered && vlo.lines === vlo.expected && vlo.lines > 0 && vlo.passage.length + vlo.preset.length + vlo.status.length === 0,
    `passage ${show(vlo.passage)}; preset ${show(vlo.preset)}; status ${show(vlo.status)}; cite lines ${vlo.lines} of ${vlo.expected}`],
];
let pass = 0;
for (const [name, ok, detail] of arms) {
  if (ok) pass += 1;
  console.log(`${ok ? 'ARM PASS' : 'ARM FAIL'} ${name} :: ${detail}`);
}
console.log(`POSTURE CITES IN WORDS: ${pass} of ${arms.length} arms`);
process.exit(pass === arms.length ? 0 : 1);
