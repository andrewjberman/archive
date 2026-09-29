/**
 * named.cjs -- DSGN_AMGTV1 round 3: THE MACHINE STRINGS THE CVO NAMED (ADJUDICATION_v3; round-2 analysis s.1) ARE OFF THE FACE.
 *
 * Usage (repo root): node <this file>
 * Renders four surfaces on the served fixtures (round3/fixtures, captured from the adapter at the cut) and searches their
 * VISIBLE text for each named string. Text inside a collapsed <details> element is not on the face (the ruling admits "behind
 * a details affordance a PM opens on purpose"), so it is removed before the search; attributes are free.
 *   header   the identity header (IdentityHeader) on Valero's /overlay, HeaderBrief and GenerationCaption real
 *   lead     the lead panel's caption, disclosure and resolution note on the Trending x Price payload
 *   thesis   the Thesis tab on Valero's /thesis (its identity line real)
 *   posture  the Posture tab on Valero's /thesis, its comparable WMB read through the same hooks
 * Named strings: "(S13)", "crosswalk/v1", "generation: none", "generation 2026", "state COMPLETE", "127.0.0.1", "blp_client",
 * "WMB_US_Equity", "claude-opus", "BLOOMBERG SESSION", "NOT REPORTED".
 * Prints one line per surface and "NAMED MACHINE STRINGS: <n> hit(s) over 4 surfaces"; exit 0 only at n == 0 with all four
 * surfaces rendered non-empty.
 */
const L = require('./_load.cjs');
const NAMED = ['(S13)', 'crosswalk/v1', 'generation: none', 'generation 2026', 'state COMPLETE', '127.0.0.1', 'blp_client', 'WMB_US_Equity', 'claude-opus', 'BLOOMBERG SESSION', 'NOT REPORTED'];

const bundles = { VLO_US_Equity: L.fixture('thesisBundle.VLO_US_Equity.json'), WMB_US_Equity: L.fixture('thesisBundle.WMB_US_Equity.json') };
const peers = { VLO_US_Equity: L.fixture('peerSet.VLO_US_Equity.json'), WMB_US_Equity: L.fixture('peerSet.WMB_US_Equity.json') };
L.hookState.impl = { useThesisBundle: (k) => bundles[k], usePeerSet: (k) => peers[k] };
L.stubSource('src/pages/SecurityAnalysis/components/TimelinePanel.tsx', { TimelinePanel: () => null });

const stripClosedDetails = (html) => html.replace(/<details(?![^>]*\sopen)[^>]*>[\s\S]*?<\/details>/g, '');
const renders = {};
try {
  const m = L.source('src/pages/SecurityAnalysis/components/SecurityOverlay.tsx');
  renders.header = L.render(m.IdentityHeader || m.SecurityOverlay, { bundle: L.fixture('overlay.VLO_US_Equity.json'), onBack: () => {}, onRefresh: () => {} });
} catch (e) { renders.header = ''; console.log('header render failed: ' + String(e.message).split('\n')[0]); }
try {
  const r = L.fixture('rankings.TRENDING_PRICE.json');
  const lp = L.source('src/pages/SecurityAnalysis/components/LeadPanel.tsx');
  const esc = (s) => '<p>' + String(s || '').replace(/</g, '&lt;') + '</p>';
  renders.lead = esc(lp.sourceFooterContent(r)) + esc(lp.sourceDisclosureText(r)) + (typeof lp.ResolutionNote === 'function' ? L.render(lp.ResolutionNote, { resolution: r.resolution }) : '');
} catch (e) { renders.lead = ''; console.log('lead render failed: ' + String(e.message).split('\n')[0]); }
try {
  const { ThesisTab } = L.source('src/pages/SecurityAnalysis/tabs/ThesisTab.tsx');
  renders.thesis = L.render(ThesisTab, { securityKey: 'VLO_US_Equity' });
} catch (e) { renders.thesis = ''; console.log('thesis render failed: ' + String(e.message).split('\n')[0]); }
try {
  const { PostureTab } = L.source('src/pages/SecurityAnalysis/tabs/PostureTab.tsx');
  renders.posture = L.render(PostureTab, { securityKey: 'VLO_US_Equity' });
} catch (e) { renders.posture = ''; console.log('posture render failed: ' + String(e.message).split('\n')[0]); }

let total = 0;
let empty = 0;
for (const [surface, html] of Object.entries(renders)) {
  const text = L.textOf(stripClosedDetails(html));
  if (!text) empty += 1;
  const hits = NAMED.map((n) => [n, text.split(n).length - 1]).filter(([, c]) => c > 0);
  const n = hits.reduce((a, [, c]) => a + c, 0);
  total += n;
  console.log(`${surface}: ${n} hit(s) over ${text.length} visible chars ${hits.length ? JSON.stringify(hits) : ''}`);
}
console.log(`NAMED MACHINE STRINGS: ${total} hit(s) over 4 surfaces${empty ? ' -- ' + empty + ' EMPTY RENDER(S)' : ''}`);
process.exit(total === 0 && empty === 0 ? 0 : 1);
