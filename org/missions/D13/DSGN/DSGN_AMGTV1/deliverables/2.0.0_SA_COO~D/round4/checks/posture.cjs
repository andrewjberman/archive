/**
 * posture.cjs -- DSGN_AMGTV1 round 4, AV-w-5: POSTURE EVIDENCE IN WORDS (round-3 analysis s.4 item 5; FWD-10).
 *
 * Usage (repo root): node <this file>
 * Renders the Posture tab on SAP GY (comparable ANET US, whose pack is missing 3 sources; reasons cite fiscal figures)
 * and on Valero (comparable WMB), served fixtures under round4/fixtures. Visible text includes collapsed <details>
 * content (the cites the CVO read sit in a drawer). Arms:
 *   1  the comparable's missing sources are said ONCE: on SAP GY, each distinct sentence "No <what> for ANET US yet" appears
 *      exactly once on the tab, and all three are still said (the base prints each twice: bullets, then a run-on line).
 *      A rewording that drops the "No <what> for ANET US yet" shape fails the floor -- keep that shape for each source.
 *   2  no raw figure code in a cite, SAP GY: no mnemonic (A_B shape: OPER_MARGIN, CF_FREE_CASH_FLOW) and no upper-case
 *      unit word (PERCENT, MILLIONS, BILLIONS, THOUSANDS) in visible text
 *   3  the same on Valero, 0 hits
 * Prints one line per arm and "POSTURE EVIDENCE IN WORDS: <k> of 3 arms"; exit 0 only at 3 of 3.
 */
const L = require('./_load.cjs');
const bundles = {};
for (const k of ['VLO_US_Equity', 'SAP_GY_Equity', 'WMB_US_Equity']) bundles[k] = L.fixture(`thesisBundle.${k}.json`);
L.hookState.impl = { useThesisBundle: (k) => bundles[k], usePeerSet: () => undefined };
const CODE = /\b[A-Z][A-Z0-9]*_[A-Z0-9_]+\b|\b(PERCENT|MILLIONS|BILLIONS|THOUSANDS)\b/g;
function posture(key) {
  try {
    return L.render(L.source('src/pages/SecurityAnalysis/tabs/PostureTab.tsx').PostureTab, { securityKey: key });
  } catch (e) {
    console.log(`${key} render failed: ` + String(e.message).split('\n')[0]);
    return '';
  }
}
const sap = posture('SAP_GY_Equity');
const vlo = posture('VLO_US_Equity');
const sapText = L.textOf(sap);
// The comparable's missing sources, as the page words them at the base: "No drafted thesis for ANET US yet", "No executive
// management record for ANET US yet", "No financial model block for ANET US yet" (the pack's `absent` list has 3 entries).
// Each distinct missing-source sentence the tab prints must appear once; the base prints each twice (bullets, then run-on).
const missingRe = /No [a-z][a-z -]+? for ANET US yet/g;
const counts = {};
for (const m of sapText.match(missingRe) || []) counts[m] = (counts[m] || 0) + 1;
const missing = Object.keys(counts);
const repeats = Object.entries(counts).filter(([, n]) => n > 1);
const hs = sapText.match(CODE) || [];
const hv = L.textOf(vlo).match(CODE) || [];
const arms = [
  ['missing sources said once (SAP GY)', sap.length > 0 && missing.length >= 3 && repeats.length === 0, `${missing.length} distinct missing-source sentence(s) (floor 3); repeated: ${repeats.length ? JSON.stringify(repeats) : 'none'}`],
  ['no raw figure code (SAP GY)', sap.length > 0 && hs.length === 0, `${hs.length} hit(s) ${hs.length ? JSON.stringify(hs.slice(0, 6)) : ''}`],
  ['no raw figure code (Valero)', vlo.length > 0 && hv.length === 0, `${hv.length} hit(s) ${hv.length ? JSON.stringify(hv.slice(0, 6)) : ''}`],
];
let pass = 0;
for (const [name, ok, detail] of arms) {
  if (ok) pass += 1;
  console.log(`${ok ? 'ARM PASS' : 'ARM FAIL'} ${name} :: ${detail}`);
}
console.log(`POSTURE EVIDENCE IN WORDS: ${pass} of ${arms.length} arms`);
process.exit(pass === arms.length ? 0 : 1);
