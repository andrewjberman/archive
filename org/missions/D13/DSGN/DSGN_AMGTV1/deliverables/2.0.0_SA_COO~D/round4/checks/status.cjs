/**
 * status.cjs -- DSGN_AMGTV1 round 4, AV-w-3: NO STATUS WORD ON THE MODEL FACE (round-3 analysis s.4 item 3, FWD-11).
 *
 * Usage (repo root): node <this file>
 * Renders the Model tab on SAP GY (EUR listing; 18 refused lines at the base) and on Valero, served fixtures under
 * round4/fixtures, and reads the VISIBLE text, collapsed <details> content included (a status word behind a details
 * affordance is still a status word a PM reads). Status-word hits counted per surface:
 *   - an upper-case status word used as a label: REFUSED, ABSENT, SERVED, NOT_SERVED, UNRESOLVED, PRESENT
 *   - the "not read" placeholder, and the letter-coded score labels "Peers V" / "Divergence D"
 * Arms:
 *   1  SAP GY Model: 0 status-word hits
 *   2  Valero Model: 0 status-word hits
 *   3  the facts stay: SAP GY still carries every refused line on the element (data-model-line-refusal count >= 18,
 *      its base count), so the words changed and no refusal was dropped
 * Prints one line per arm and "MODEL STATUS WORDS: <k> of 3 arms"; exit 0 only at 3 of 3.
 */
const L = require('./_load.cjs');
const bundles = {};
for (const k of ['VLO_US_Equity', 'SAP_GY_Equity', 'WMB_US_Equity']) bundles[k] = L.fixture(`thesisBundle.${k}.json`);
L.hookState.impl = { useThesisBundle: (k) => bundles[k], usePeerSet: () => undefined };
L.stubSource('src/pages/SecurityAnalysis/components/TimelinePanel.tsx', { TimelinePanel: () => null });
const STATUS = /\b(REFUSED|ABSENT|SERVED|NOT_SERVED|UNRESOLVED|PRESENT)\b|\bnot read\b|\bPeers V\b|\bDivergence D\b/g;
const REFUSAL_FLOOR = 18;
function model(key) {
  try {
    return L.render(L.source('src/pages/SecurityAnalysis/tabs/ModelTab.tsx').ModelTab, { securityKey: key });
  } catch (e) {
    console.log(`${key} render failed: ` + String(e.message).split('\n')[0]);
    return '';
  }
}
const sap = model('SAP_GY_Equity');
const vlo = model('VLO_US_Equity');
const hits = (html) => L.textOf(html).match(STATUS) || [];
const tally = (h) => JSON.stringify(Object.entries(h.reduce((a, w) => ((a[w] = (a[w] || 0) + 1), a), {})));
const sapHits = hits(sap);
const vloHits = hits(vlo);
const refusals = (sap.match(/data-model-line-refusal=/g) || []).length;
const arms = [
  ['SAP GY Model: no status word', sap.length > 0 && sapHits.length === 0, `${sapHits.length} hit(s) ${sapHits.length ? tally(sapHits) : ''}`],
  ['Valero Model: no status word', vlo.length > 0 && vloHits.length === 0, `${vloHits.length} hit(s) ${vloHits.length ? tally(vloHits) : ''}`],
  ['SAP GY refusals kept on the element', refusals >= REFUSAL_FLOOR, `data-model-line-refusal x${refusals} (floor ${REFUSAL_FLOOR})`],
];
let pass = 0;
for (const [name, ok, detail] of arms) {
  if (ok) pass += 1;
  console.log(`${ok ? 'ARM PASS' : 'ARM FAIL'} ${name} :: ${detail}`);
}
console.log(`MODEL STATUS WORDS: ${pass} of ${arms.length} arms`);
process.exit(pass === arms.length ? 0 : 1);
