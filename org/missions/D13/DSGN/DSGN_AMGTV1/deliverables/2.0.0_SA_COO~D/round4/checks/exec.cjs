/**
 * exec.cjs -- DSGN_AMGTV1 round 4, AV-w-4: EXEC MANAGEMENT -- THE LAST DARK BAND AND ITS RAW "READ DETAIL"
 * (round-3 analysis s.4 item 4; FWD-7, FWD-11).
 *
 * Usage (repo root): node <this file>
 * Renders the Exec Management tab on INTU (management ABSENT, ZERO_OFFICERS, roster UNRESOLVED-SOURCE) and on Valero
 * (roster RESOLVED), served fixtures under round4/fixtures. Visible text includes collapsed <details> content: the CVO
 * read the drawer ("Read detail") and graded its field names as raw. Arms:
 *   1  no second band: the render uses no estate PanelHeader (data-stub="PanelHeader" x0) and carries its own white
 *      header marker data-exec-panel-header
 *   2  INTU, face AND drawer: no field name or status code -- roster_status, roster_reason, source_item, source_accession,
 *      UNRESOLVED-SOURCE, ZERO_OFFICERS, or an upper-case ABSENT/RESOLVED used as a label
 *   3  Valero, face AND drawer: the same, 0 hits
 * The served state is not asserted gone: it may ride data attributes (data-exec-status and the like), which are free.
 * Prints one line per arm and "EXEC BAND AND DETAIL: <k> of 3 arms"; exit 0 only at 3 of 3.
 */
const L = require('./_load.cjs');
const bundles = {};
for (const k of ['VLO_US_Equity', 'INTU_US_Equity']) bundles[k] = L.fixture(`thesisBundle.${k}.json`);
L.hookState.impl = { useThesisBundle: (k) => bundles[k], useManagement: (k) => (bundles[k] || {}).management, usePeerSet: () => undefined };
const RAW = /\broster_status\b|\broster_reason\b|\bsource_item\b|\bsource_accession\b|UNRESOLVED-SOURCE|\bZERO_OFFICERS\b|\bABSENT\b|\bRESOLVED\b/g;
function exec(key) {
  try {
    return L.render(L.source('src/pages/SecurityAnalysis/tabs/ExecManagementTab.tsx').ExecManagementTab, { securityKey: key });
  } catch (e) {
    console.log(`${key} render failed: ` + String(e.message).split('\n')[0]);
    return '';
  }
}
const intu = exec('INTU_US_Equity');
const vlo = exec('VLO_US_Equity');
const bands = (intu.match(/data-stub="PanelHeader"/g) || []).length + (vlo.match(/data-stub="PanelHeader"/g) || []).length;
const white = intu.includes('data-exec-panel-header') && vlo.includes('data-exec-panel-header');
const hi = L.textOf(intu).match(RAW) || [];
const hv = L.textOf(vlo).match(RAW) || [];
const arms = [
  ['no second band', intu.length > 0 && vlo.length > 0 && bands === 0 && white, `estate band headers=${bands}, white header=${white ? 'yes' : 'no'}`],
  ['INTU face and drawer in words', intu.length > 0 && hi.length === 0, `${hi.length} raw hit(s) ${hi.length ? JSON.stringify(hi.slice(0, 6)) : ''}`],
  ['Valero face and drawer in words', vlo.length > 0 && hv.length === 0, `${hv.length} raw hit(s) ${hv.length ? JSON.stringify(hv.slice(0, 6)) : ''}`],
];
let pass = 0;
for (const [name, ok, detail] of arms) {
  if (ok) pass += 1;
  console.log(`${ok ? 'ARM PASS' : 'ARM FAIL'} ${name} :: ${detail}`);
}
console.log(`EXEC BAND AND DETAIL: ${pass} of ${arms.length} arms`);
process.exit(pass === arms.length ? 0 : 1);
