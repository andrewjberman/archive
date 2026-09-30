/**
 * surfaces.cjs -- DSGN_AMGTV1 round 10: renders every WALKED surface of the Security Analysis page on SERVED fixtures, for the
 * round's checks (issuer 2.0.0_SA_COO~D). Exports renderAll(names?) -> [{ surface, html }].
 *
 * Surfaces (the walk's routes over its four names, plus IMB / AZN for the round-10 cells):
 *   lead-<LIST>        the lead list (RankedList) for each served non-empty list, plus the footer lines (LeadPanel)
 *   chart              the lead rank-history chart (RankedChart)
 *   header-<NAME>      the identity header (SecurityOverlay IdentityHeader) on the served /overlay
 *   timeline-<NAME>    the mention timeline (TimelinePanel) on the served /timeline, and 992 HK's served day (DayDissection)
 *   thesis-/model-/posture-/exec-/peers-<NAME>   the five tabs on the served /thesis (and /peers where served)
 * useQuery is stubbed by queryKey (the timeline's 'range' / 'day'); the page's own hooks read the fixtures (_load.cjs hookState).
 * No network, no AWS, writes no file.
 */
const L = require('./_load.cjs');
const React = L.React;

const NAMES = {
  VLO: 'VLO_US_Equity', INTU: 'INTU_US_Equity', SAP: 'SAP_GY_Equity', HK: '992_HK_Equity', IMB: 'IMB_LN_Equity', AZN: 'AZN_LN_Equity', J6501: '6501_JP_Equity', TSM: 'TSM_US_Equity',
};
const tryFixture = (n) => { try { return L.fixture(n); } catch (e) { return null; } };
const unwrap = (x) => (x && x.payload && (x._capture_note || x._capture) ? x.payload : x);

const bundles = {};
const overlays = {};
for (const k of Object.values(NAMES)) {
  bundles[k] = unwrap(tryFixture(`thesisBundle.${k}.json`));
  overlays[k] = unwrap(tryFixture(`overlay.${k}.json`));
}
const peers = {};
for (const k of ['VLO_US_Equity', 'WMB_US_Equity', 'INTU_US_Equity']) peers[k] = unwrap(tryFixture(`peerSet.${k}.json`));
L.hookState.impl = { useThesisBundle: (k) => bundles[k], usePeerSet: (k) => peers[k], useManagement: (k) => (bundles[k] || {}).management };

const rcCache = {};
L.stubSource('recharts', new Proxy({}, {
  get(_t, k) {
    if (k === '__esModule') return true;
    if (typeof k !== 'string') return undefined;
    if (!rcCache[k]) { const C = (p) => React.createElement('div', { 'data-rc': k }, (p || {}).children); C.displayName = k; rcCache[k] = C; }
    return rcCache[k];
  },
}));
const q = { range: null, day: null };
L.stubSource('@tanstack/react-query', {
  __esModule: true,
  useQuery: (opts) => {
    const kind = opts && opts.queryKey ? opts.queryKey[1] : null;
    return { isLoading: false, isError: false, error: null, data: undefined, refetch: () => {}, ...((kind && q[kind]) || {}) };
  },
  useQueryClient: () => ({ invalidateQueries: () => {}, getQueryData: () => undefined }),
});
const api = { __esModule: true, apiRequest: () => Promise.resolve(undefined) };
L.stubSource('src/api/api-client.ts', api);
L.stubSource('src/api/api-client', api);

const safe = (f) => { try { return f(); } catch (e) { return `<p data-render-failed="1">RENDER FAILED ${String(e.message).split('\n')[0].replace(/</g, '&lt;')}</p>`; } };
const SA = 'src/pages/SecurityAnalysis/';

function renderAll(only) {
  const out = [];
  const push = (surface, fn) => { if (!only || only.some((o) => surface.startsWith(o))) out.push({ surface, html: safe(fn) }); };
  const RL = () => L.source(SA + 'components/RankedList.tsx');
  const LP = () => L.source(SA + 'components/LeadPanel.tsx');
  for (const list of ['TRENDING_CHATTER', 'TRENDING_PRICE', 'BREAKOUT_PRICE']) {
    push(`lead-${list}`, () => {
      const p = L.fixture(`rankings.${list}.json`);
      const lp = LP();
      const e = (x) => (x ? '<p>' + String(x).replace(/</g, '&lt;') + '</p>' : '');
      return L.render(RL().RankedList, {
        rows: p.rows || [], starredTickers: new Set(), resolution: p.resolution, onToggleStar: () => {}, onSelectSecurity: () => {},
        isLoading: false, readError: null, rankingStatus: p.ranking_status, rankingReason: null, emptyReason: null,
      }) + e(lp.sourceFooterContent(p)) + e(lp.sourceDisclosureText(p));
    });
  }
  push('chart', () => L.render(L.source(SA + 'components/RankedChart.tsx').RankedChart, { data: L.fixture('rankSeries.TRENDING_PRICE.12.json'), isLoading: false }));
  for (const [n, k] of Object.entries(NAMES)) {
    if (overlays[k]) push(`header-${n}`, () => { const m = L.source(SA + 'components/SecurityOverlay.tsx'); return L.render(m.IdentityHeader || m.SecurityOverlay, { bundle: overlays[k], onBack: () => {}, onRefresh: () => {} }); });
  }
  for (const [n, k] of [['HK', '992_HK_Equity'], ['VLO', 'VLO_US_Equity']]) {
    push(`timeline-${n}`, () => {
      q.range = { data: unwrap(L.fixture(`timeline.${k}.json`)) };
      const tl = L.source(SA + 'components/TimelinePanel.tsx');
      let html = L.render(tl.TimelinePanel, { securityKey: k });
      if (n === 'HK') {
        const day = unwrap(L.fixture('timelineDay.992_HK_Equity.2026-08-13.json'));
        q.day = { data: day };
        html += L.render(tl.DayDissection, { securityKey: k, date: '2026-08-13' });
      }
      return html;
    });
  }
  for (const [n, k] of Object.entries(NAMES)) {
    if (!bundles[k]) continue;
    push(`thesis-${n}`, () => L.render(L.source(SA + 'tabs/ThesisTab.tsx').ThesisTab, { securityKey: k }));
    push(`model-${n}`, () => L.render(L.source(SA + 'tabs/ModelTab.tsx').ModelTab, { securityKey: k }));
    push(`posture-${n}`, () => L.render(L.source(SA + 'tabs/PostureTab.tsx').PostureTab, { securityKey: k }));
    push(`exec-${n}`, () => L.render(L.source(SA + 'tabs/ExecManagementTab.tsx').ExecManagementTab, { securityKey: k }));
  }
  return out;
}

module.exports = { renderAll, NAMES, bundles, overlays, q, unwrap };
