/**
 * raw.cjs -- DSGN_AMGTV1 round 2: NO RAW CODE ON A SURFACE'S FACE (FWD-11 and the outcome each surface serves).
 *
 * Usage (from the repository root): node <this file> <surface>
 *   thesis   the Thesis tab at rest on Valero's served /thesis bundle
 *   header   the header's description / posture / feed block (HeaderBrief) on Valero's served /overlay
 *   model    the Model tab on Valero's served /thesis bundle
 *   posture  the Posture tab on Valero's served bundle; its comparable (WMB, whose thesis is ABSENT) read through the same hooks
 *   lead     the lead panel's source captions (sourceFooterContent, sourceDisclosureText, generationCaptionText) on the
 *            served Trending x Price payload
 * A raw code is, in VISIBLE text only (attributes are free): a vendor or system token like SALES_REV_TURN or
 * TRENDING_PRICE; a machine word (NOT-YET-BUILT, INTERFACE F-1, held_uncited, ABSENT_ON_OBJECT, crosswalk/v1, NoSuchKey);
 * a storage path (s3://..., org/missions/..., a *.json file name); a run of 15 or more digits.
 * Prints "<SURFACE> RAW CODE: <n> hit(s)" plus the count per class; exit 0 only when n == 0 AND the surface rendered
 * non-empty (a blank render is not a clean face).
 * Fixtures: deliverables/2.0.0_SA_COO~D/round2/fixtures/, captured from lib/research/api/scoped_amgt at the cut.
 */
const L = require('./_load.cjs');
const surface = process.argv[2];

const vlo = L.fixture('thesisBundle.VLO_US_Equity.json');
const wmb = L.fixture('thesisBundle.WMB_US_Equity.json');
const bundles = { VLO_US_Equity: vlo, WMB_US_Equity: wmb };
const peers = { VLO_US_Equity: L.fixture('peerSet.VLO_US_Equity.json'), WMB_US_Equity: L.fixture('peerSet.WMB_US_Equity.json') };
L.hookState.impl = {
  useThesisBundle: (key) => bundles[key],
  usePeerSet: (key) => peers[key],
};
L.stubSource('src/pages/SecurityAnalysis/components/IdentityLine.tsx', {
  IdentityLine: () => null,
  identityLabel: (i) => (i && i.display_ticker) || 'name',
  isResolvedIdentity: () => true,
});

let html = '';
if (surface === 'thesis') {
  const { ThesisTab } = L.source('src/pages/SecurityAnalysis/tabs/ThesisTab.tsx');
  html = L.render(ThesisTab, { securityKey: 'VLO_US_Equity' });
} else if (surface === 'header') {
  L.stubSource('src/pages/SecurityAnalysis/components/TimelinePanel.tsx', { TimelinePanel: () => null });
  const { HeaderBrief } = L.source('src/pages/SecurityAnalysis/components/HeaderBrief.tsx');
  html = L.render(HeaderBrief, { bundle: L.fixture('overlay.VLO_US_Equity.json'), postureLine: null });
} else if (surface === 'model') {
  const { ModelTab } = L.source('src/pages/SecurityAnalysis/tabs/ModelTab.tsx');
  html = L.render(ModelTab, { securityKey: 'VLO_US_Equity' });
} else if (surface === 'posture') {
  const { PostureTab } = L.source('src/pages/SecurityAnalysis/tabs/PostureTab.tsx');
  html = L.render(PostureTab, { securityKey: 'VLO_US_Equity' });
} else if (surface === 'lead') {
  const r = L.fixture('rankings.TRENDING_PRICE.json');
  const lp = L.source('src/pages/SecurityAnalysis/components/LeadPanel.tsx');
  const gc = L.source('src/pages/SecurityAnalysis/components/GenerationCaption.tsx');
  const parts = [
    typeof lp.sourceFooterContent === 'function' ? lp.sourceFooterContent(r) : '',
    typeof lp.sourceDisclosureText === 'function' ? lp.sourceDisclosureText(r) || '' : '',
    typeof gc.generationCaptionText === 'function' ? gc.generationCaptionText(r, 'price') || '' : '',
  ];
  html = parts.map((p) => '<p>' + String(p).replace(/</g, '&lt;') + '</p>').join('');
} else {
  console.log('usage: raw.cjs thesis|header|model|posture|lead');
  process.exit(3);
}

const c = L.rawCensus(html);
const rendered = L.textOf(html).length > 0;
const per = Object.keys(L.RAW_CLASSES).map((k) => `${k}=${c[k]}${c[k] ? ' e.g. ' + JSON.stringify(c[k + '_first']) : ''}`).join('; ');
console.log(`visible text: ${L.textOf(html).length} chars; ${per}`);
console.log(`${surface.toUpperCase()} RAW CODE: ${c.total} hit(s)${rendered ? '' : ' -- EMPTY RENDER'}`);
process.exit(c.total === 0 && rendered ? 0 : 1);
