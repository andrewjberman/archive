/**
 * band.cjs -- DSGN_AMGTV1 round 3: A TAB'S PANEL HEADER IS NOT A SECOND DARK BAND (DESIGN.md C3: one band per page).
 *
 * Usage (repo root): node <this file> <thesis|model|posture>
 * The estate's PanelHeader resolves to the band (Panel.tsx; DSGN_REBRND W1-S9); round 2 gave the Thesis tab a white header
 * carrying data-thesis-panel-header. A tab passes when its render uses NO estate PanelHeader (in the stubbed render that is an
 * element carrying data-stub="PanelHeader") and carries its own white header marker data-<tab>-panel-header.
 * Prints "<TAB> PANEL HEADER: estate band headers=<n>, white header=<yes|no>"; exit 0 only at 0 and yes.
 */
const L = require('./_load.cjs');
const tab = process.argv[2];
const bundles = { VLO_US_Equity: L.fixture('thesisBundle.VLO_US_Equity.json'), WMB_US_Equity: L.fixture('thesisBundle.WMB_US_Equity.json') };
const peers = { VLO_US_Equity: L.fixture('peerSet.VLO_US_Equity.json'), WMB_US_Equity: L.fixture('peerSet.WMB_US_Equity.json') };
L.hookState.impl = { useThesisBundle: (k) => bundles[k], usePeerSet: (k) => peers[k] };
const FILES = { thesis: ['tabs/ThesisTab.tsx', 'ThesisTab'], model: ['tabs/ModelTab.tsx', 'ModelTab'], posture: ['tabs/PostureTab.tsx', 'PostureTab'] };
if (!FILES[tab]) {
  console.log('usage: band.cjs thesis|model|posture');
  process.exit(3);
}
const mod = L.source('src/pages/SecurityAnalysis/' + FILES[tab][0]);
const html = L.render(mod[FILES[tab][1]], { securityKey: 'VLO_US_Equity' });
const bandHeaders = (html.match(/data-stub="PanelHeader"/g) || []).length;
const white = html.includes(`data-${tab}-panel-header`);
console.log(`${tab.toUpperCase()} PANEL HEADER: estate band headers=${bandHeaders}, white header=${white ? 'yes' : 'no'}`);
process.exit(bandHeaders === 0 && white && html.length > 0 ? 0 : 1);
