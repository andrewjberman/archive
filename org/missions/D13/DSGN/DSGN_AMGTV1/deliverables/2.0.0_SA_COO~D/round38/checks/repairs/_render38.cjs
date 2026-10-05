/**
 * _render38.cjs -- the render child of repairs38.cjs, DSGN_AMGTV1 round 38 (issuer 2.0.0_SA_COO~D). NOT a check: it grades
 * nothing and prints ONE JSON line on stdout. repairs38.cjs spawns it once per mode (each mode installs its own process-wide stubs).
 *
 * Usage (cwd = the directory whose portal/ is the checkout under test): node _render38.cjs changed|page
 *   changed  round15/checks/_load.cjs: the REAL components/model/WhatChangedPanel.tsx, with the props tabs/ModelTab.tsx's
 *            ModelVersions hands it (securityKey, stamps = the served /versions stamps newest LAST, data = the served /thesis,
 *            latestAbsent = model_status !== 'SERVED') over round35/fixtures/{versions,thesis}.BA_US_Equity.json, and the page hook
 *            useModelCompare answering, per case:
 *              LOADING          every compare read pending (isLoading true, no data).
 *              ERROR            every compare read settled in error (isError true; error "API request failed: 500 Internal
 *                               Server Error -- {"message":"planted 500"}", failureCount 3), no data.
 *              ERROR, REMOUNTED the served walk's sequence (round37 walk read-20261005T054042Z, 06-fwd19-panels-BA-US.json: 20+
 *                               intercepted compare GETs on ONE pair within 15 s, the panel never settling): the FIRST observer of
 *                               a pair reads the settled error, and any LATER observer of the same pair in the same render reads
 *                               pending -- react-query v5 refetches an errored query with no data when a new observer mounts
 *                               (refetchOnMount; a query with no data is stale), and the fetch resets its status to pending.
 *              SERVED           every compare read answers round35/fixtures/compare.BA_US_Equity.json (sanity: the table renders).
 *            Shared chrome is the loader's stub: PanelLoading / PanelError render <div data-stub="PanelLoading|PanelError">.
 *   page     the REAL SecurityAnalysis.tsx (page shell, IdentityHeader, HeaderCards, HeaderBrief, TimelinePanel, TimelineWordCloud,
 *            LeadPanel, PriceBars, ChatterBubbles and every tab), rendered once per (name, tab) in Security mode -- MSFT and AMD
 *            (round37 overlay/thesis/peers + round35 timeline), BA (round35 thesis/versions/compare/timeline; no BA /overlay or
 *            /peers capture in round35/37, so those two reads answer nothing) -- and once per subject (PRICE: round29
 *            leadprice/rankings.trending.price.live.json; CHATTER: round37 chatter.30.json) in Universe mode. Stubs (only these):
 *              page hooks (hooks/useLeadPanelApi.ts)  answer the fixtures above by name and key (a comparable's read answers nothing).
 *              hooks/useSecurityAnalysisState.ts       the mode, the selected key and the subject of the render.
 *              src/hooks/useTabNavigation.ts           the active tab of the render.   src/hooks/useAuth.ts   a firm.
 *              src/contexts/PageThemeContext.tsx        PageThemeProvider renders its children.
 *              react-router-dom                         useParams -> {}; every other export is the loader's stub.
 *              @tanstack/react-query                    useQuery answers the /timeline range fixture on a key naming "timeline",
 *                                                       nothing otherwise (TimelinePanel's own read).
 *              src/ui/components/panels (index, PanelFooter.tsx, SmartPanelFooter.tsx) and src/ui/components/PageEnd.tsx: the
 *                                                       MARKERS described in _cards38.cjs around the REAL PanelFooter / PageEnd;
 *                                                       every other panels export is the loader's stub (data-stub="<name>").
 *            Returns per render: the markup, the served fields of every card (_cards38.cjs CARDS) and the page's served dates.
 * Honours the loader's CHECK_SRC_OVERRIDE. No network, no AWS, writes no file.
 */
const fs = require('fs');
const path = require('path');

const DROOT = path.join(__dirname, '..', '..', '..');
const SA = 'src/pages/SecurityAnalysis/';
const X = require(path.join(__dirname, '_cards38.cjs'));
const pay = (x) => (x && x.payload && (x._capture_note || x._capture) ? x.payload : x);
const readAt = (rel) => pay(JSON.parse(fs.readFileSync(path.join(DROOT, rel), 'utf8')));
const first = (e) => String(e && e.message ? e.message : e).split('\n')[0];
const out = (o) => process.stdout.write(JSON.stringify(o) + '\n');

const mode = process.argv[2];
const L = require(path.join(DROOT, 'round15', 'checks', '_load.cjs'));
const React = L.React;
const h = React.createElement;

const ok = (data) => ({ data, isLoading: false, isPending: data === undefined, isError: false, error: null, isFetching: false, failureCount: 0, failureReason: null, status: data === undefined ? 'pending' : 'success', fetchStatus: 'idle', refetch: () => Promise.resolve() });
const pending = () => ({ data: undefined, isLoading: true, isPending: true, isError: false, error: null, isFetching: true, failureCount: 0, failureReason: null, status: 'pending', fetchStatus: 'fetching', refetch: () => Promise.resolve() });
const ERR = new Error('API request failed: 500 Internal Server Error - {"message":"planted 500 (repairs38, static render)"}');
const failed = () => ({ data: undefined, isLoading: false, isPending: false, isError: true, error: ERR, isFetching: false, failureCount: 3, failureReason: ERR, status: 'error', fetchStatus: 'idle', refetch: () => Promise.resolve() });

// The page hooks, answered from Q (set per render).
const Q = { key: null, overlay: undefined, thesis: undefined, peers: undefined, versions: undefined, compare: () => ok(undefined), rankings: undefined, chatter: undefined, timeline: undefined, state: null, tab: 'thesis' };
const mine = (k) => k && k === Q.key;
const HOOKS = {
  useSecurityOverlay: (k) => ok(mine(k) ? Q.overlay : undefined),
  useThesisBundle: (k) => ok(mine(k) ? Q.thesis : undefined),
  usePeerSet: (k) => ok(mine(k) ? Q.peers : undefined),
  useModelVersions: (k) => ok(mine(k) ? Q.versions : undefined),
  useModelCompare: (k, from, to) => (mine(k) && from && to ? Q.compare(k, from, to) : ok(undefined)),
  useInputLedger: () => ok(undefined),
  useCoverageSet: () => ok(undefined),
  useLeadPanelRankings: (movement, subject, enabled) => ok(enabled === false ? undefined : Q.rankings),
  useRankTimeSeries: () => ok(undefined),
  useCollectedChatter: (enabled) => ok(enabled === false ? undefined : Q.chatter),
  useStarredList: () => ok([]),
  useSetStarred: () => ({ mutate: () => {}, isPending: false }),
  useRequestRefresh: () => ({ mutate: () => {}, isPending: false }),
};
const hooksModule = new Proxy({}, {
  get(_t, k) {
    if (k === '__esModule') return true;
    if (typeof k !== 'string') return undefined;
    return HOOKS[k] || (() => ok(undefined));
  },
});
for (const s of ['hooks/useLeadPanelApi.ts', 'hooks/useLeadPanelApi']) L.stubSource(SA + s, hooksModule);

// A copy of the loader's stub component (data-stub="<name>", text props printed, children rendered).
const stubCache = {};
function stubComponent(name) {
  if (stubCache[name]) return stubCache[name];
  const isDialog = /Dialog/.test(name);
  const C = (props) => {
    const p = props || {};
    if (isDialog && !p.open) return null;
    const attrs = { 'data-stub': name };
    if (typeof p.title === 'string') attrs['data-stub-title'] = p.title;
    if (typeof p.eyebrow === 'string') attrs['data-stub-eyebrow'] = p.eyebrow;
    const kids = [];
    for (const k of ['title', 'subtitle', 'message', 'detail', 'hint', 'cause', 'label']) {
      if (typeof p[k] === 'string' && p[k]) kids.push(h('span', { key: 'stub-' + k, 'data-stub-text': k }, p[k]));
    }
    if (p.children !== undefined) kids.push(p.children);
    if (p.footer !== undefined && p.footer !== null && typeof p.footer === 'object') kids.push(p.footer);
    return h('div', attrs, ...kids);
  };
  C.displayName = name;
  stubCache[name] = C;
  return C;
}
const stubProxy = (overrides) => new Proxy({}, {
  get(_t, k) {
    if (k === '__esModule') return true;
    if (typeof k !== 'string') return undefined;
    if (overrides && overrides[k]) return overrides[k];
    if (k === 'cn') return (...xs) => xs.filter(Boolean).join(' ');
    if (k === 'buttonClass') return () => '';
    return stubComponent(k);
  },
});

if (mode === 'changed') {
  const cases = [];
  let error = null;
  try {
    const thesis = readAt('round35/fixtures/thesis.BA_US_Equity.json');
    const versions = readAt('round35/fixtures/versions.BA_US_Equity.json');
    const compare = readAt('round35/fixtures/compare.BA_US_Equity.json');
    const stamps = (versions.versions || []).map((v) => v.stamp);
    const W = L.source(SA + 'components/model/WhatChangedPanel.tsx').WhatChangedPanel;
    if (typeof W !== 'function') throw new Error('WhatChangedPanel.tsx exports no WhatChangedPanel');
    Q.key = 'BA_US_Equity';
    const CASES = [
      ['LOADING', () => () => pending()],
      ['ERROR', () => () => failed()],
      ['ERROR, REMOUNTED', () => { const seen = new Map(); return (k, f, t) => { const id = `${f}|${t}`; const n = seen.get(id) || 0; seen.set(id, n + 1); return n === 0 ? failed() : pending(); }; }],
      ['SERVED', () => () => ok(compare)],
    ];
    for (const [name, make] of CASES) {
      Q.compare = make();
      const rec = { name, html: null, stop: null };
      try { rec.html = L.render(W, { securityKey: 'BA_US_Equity', stamps, data: thesis, latestAbsent: thesis.model_status !== 'SERVED' }); } catch (e) { rec.stop = 'RENDER FAILED: ' + first(e); }
      cases.push(rec);
    }
  } catch (e) { error = 'LOAD FAILED: ' + first(e); }
  out({ mode, error, cases });
} else if (mode === 'page') {
  const renders = [];
  let error = null;
  let pubs = X.DEFAULT_PUBLISHERS;
  try {
    // ---- stubs ----
    const markProps = (p, keys) => { const o = {}; for (const k of keys) if (p[k] !== undefined) o[k] = p[k]; return JSON.stringify(o); };
    const realFooter = L.source('src/ui/components/panels/PanelFooter.tsx').PanelFooter;
    const realEnd = L.source('src/ui/components/PageEnd.tsx').PageEnd;
    const PanelFooter = (p) => h('div', { 'data-check-shared': 'PanelFooter', 'data-check-props': markProps(p || {}, ['content', 'timestamp', 'dataAsOf', 'frequency']) }, h(realFooter, p));
    const SmartPanelFooter = (p) => h('div', { 'data-check-shared': 'SmartPanelFooter', 'data-check-props': markProps(p || {}, ['content', 'sourceKey']) }, h('div', null, `<the data manifest's time> | ${p && p.content}`));
    const PageEnd = (p) => h('div', { 'data-check-shared': 'PageEnd', 'data-check-props': markProps(p || {}, ['pageName', 'dataAsOf']) }, h(realEnd, p));
    const panels = stubProxy({ PanelFooter, SmartPanelFooter });
    for (const s of ['index.ts', 'index']) L.stubSource('src/ui/components/panels/' + s, panels);
    L.stubSource('src/ui/components/panels/PanelFooter.tsx', { __esModule: true, PanelFooter });
    L.stubSource('src/ui/components/panels/SmartPanelFooter.tsx', { __esModule: true, SmartPanelFooter });
    L.stubSource('src/ui/components/PageEnd.tsx', { __esModule: true, PageEnd });
    L.stubSource('src/pages/Positioning/shared/PageEnd.tsx', { __esModule: true, PageEnd });
    L.stubSource(SA + 'hooks/useSecurityAnalysisState.ts', { __esModule: true, useSecurityAnalysisState: () => Q.state });
    L.stubSource('src/hooks/useTabNavigation.ts', { __esModule: true, useTabNavigation: () => ({ activeTab: Q.tab, handleTabChange: () => {}, tabContentRef: { current: null } }) });
    L.stubSource('src/hooks/useAuth.ts', { __esModule: true, useAuth: () => ({ claims: { firmId: 'opal' }, user: null, isAuthenticated: true }) });
    L.stubSource('src/contexts/PageThemeContext.tsx', { __esModule: true, PageThemeProvider: (p) => h(React.Fragment, null, p.children), usePageTheme: () => ({}) });
    L.stubSource('react-router-dom', stubProxy({ useParams: () => ({}), useNavigate: () => () => {}, useLocation: () => ({ pathname: '/security-analysis', search: '' }), useSearchParams: () => [new URLSearchParams(), () => {}] }));
    const flat = (x, acc) => { if (Array.isArray(x)) x.forEach((y) => flat(y, acc)); else if (x && typeof x === 'object') Object.values(x).forEach((y) => flat(y, acc)); else acc.push(x); return acc; };
    const useQueryStub = (o) => {
      const keys = flat((o && o.queryKey) || [], []).map(String);
      if (o && o.enabled === false) return ok(undefined);
      if (keys.some((k) => /timeline/i.test(k)) && !keys.some((k) => /^\d{4}-\d{2}-\d{2}$/.test(k))) {
        const d = Q.timeline;
        return ok(d !== undefined && o && typeof o.select === 'function' ? o.select(d) : d);
      }
      return ok(undefined);
    };
    L.stubSource('@tanstack/react-query', {
      __esModule: true,
      useQuery: useQueryStub,
      useQueries: (o) => ((o && o.queries) || []).map(useQueryStub),
      useMutation: () => ({ mutate: () => {}, isPending: false }),
      useQueryClient: () => ({ invalidateQueries: () => Promise.resolve(), prefetchQuery: () => Promise.resolve(), getQueryData: () => undefined }),
      keepPreviousData: (x) => x,
    });
    // The API clients read import.meta (Vite) and are never called by a static render.
    const api = new Proxy({}, { get(_t, k) { if (k === '__esModule') return true; if (typeof k !== 'string') return undefined; return () => Promise.resolve(undefined); } });
    for (const s of ['src/api/api-client.ts', 'src/api/portal-proxy.ts', 'src/api/endpoints/amgt-lead-panel.ts', 'src/lib/dataLoader.ts']) L.stubSource(s, api);
    try { pubs = L.source(SA + 'components/publisherNames.ts').PUBLISHER_NAMES || pubs; } catch (e) { /* the default map */ }

    const Page = L.source(SA + 'SecurityAnalysis.tsx').SecurityAnalysis;
    if (typeof Page !== 'function') throw new Error('SecurityAnalysis.tsx exports no SecurityAnalysis');
    const R37 = 'round37/fixtures/';
    const R35 = 'round35/fixtures/';
    const NAMES = [
      { key: 'MSFT_US_Equity', overlay: R37 + 'overlay.MSFT_US_Equity.json', thesis: R37 + 'thesis.MSFT_US_Equity.json', peers: R37 + 'peers.MSFT_US_Equity.json', timeline: R35 + 'timeline.MSFT_US_Equity.json' },
      { key: 'AMD_US_Equity', overlay: R37 + 'overlay.AMD_US_Equity.json', thesis: R37 + 'thesis.AMD_US_Equity.json', peers: R37 + 'peers.AMD_US_Equity.json', timeline: R35 + 'timeline.AMD_US_Equity.json' },
      { key: 'BA_US_Equity', thesis: R35 + 'thesis.BA_US_Equity.json', versions: R35 + 'versions.BA_US_Equity.json', compare: R35 + 'compare.BA_US_Equity.json', timeline: R35 + 'timeline.BA_US_Equity.json' },
    ];
    const TABS = ['thesis', 'exec_management', 'peers', 'model', 'posture'];
    const baseState = { movement: 'TRENDING', setMovement: () => {}, setSubject: () => {}, starredOnly: false, setStarredOnly: () => {}, view: 'list', setView: () => {}, selectSecurity: () => {}, clearSecuritySelection: () => {}, searchInput: '', setSearchInput: () => {} };
    const doRender = (label, extra) => {
      const rec = Object.assign({ label, html: null, stop: null }, extra);
      try { rec.html = L.render(Page, {}); } catch (e) { rec.stop = 'RENDER FAILED: ' + first(e); }
      return rec;
    };
    for (const n of NAMES) {
      const payloads = {};
      for (const k of ['overlay', 'thesis', 'peers', 'versions', 'compare', 'timeline']) payloads[k] = n[k] ? readAt(n[k]) : undefined;
      Object.assign(Q, { key: n.key, overlay: payloads.overlay, thesis: payloads.thesis, peers: payloads.peers, versions: payloads.versions, timeline: payloads.timeline, rankings: undefined, chatter: undefined });
      Q.compare = () => ok(payloads.compare);
      Q.state = Object.assign({}, baseState, { isSecurityMode: true, selectedSecurityKey: n.key, subject: 'PRICE' });
      const fields = {};
      for (const id of ['K', 'N', 'T', ...TABS, 'W']) fields[id] = X.cardFields(id, payloads);
      const dates = X.pageDates('security', payloads).values;
      for (const tab of TABS) {
        Q.tab = tab;
        renders.push(doRender(`${n.key.split('_')[0]} ${tab}`, { mode: 'security', key: n.key, tab, fields, dates, served: Object.keys(payloads).filter((k) => payloads[k] !== undefined) }));
      }
    }
    const rankings = readAt('round29/fixtures/leadprice/rankings.trending.price.live.json');
    const chatter = readAt(R37 + 'chatter.30.json');
    for (const subject of ['PRICE', 'CHATTER']) {
      Object.assign(Q, { key: null, overlay: undefined, thesis: undefined, peers: undefined, versions: undefined, timeline: undefined, rankings, chatter, tab: 'thesis' });
      Q.compare = () => ok(undefined);
      Q.state = Object.assign({}, baseState, { isSecurityMode: false, selectedSecurityKey: null, subject });
      const payloads = { rankings, chatter };
      const fields = { LEAD: X.cardFields(subject === 'PRICE' ? 'LEAD_PRICE' : 'LEAD_CHATTER', payloads), thesis: X.cardFields('thesis', {}) };
      renders.push(doRender(`universe ${subject}`, { mode: 'universe', key: null, tab: 'thesis', subject, fields, dates: X.pageDates('universe', subject === 'PRICE' ? { rankings } : { chatter }).values, served: [subject === 'PRICE' ? 'rankings' : 'chatter'] }));
    }
  } catch (e) { error = 'LOAD FAILED: ' + first(e); }
  out({ mode, error, renders, pubs });
} else {
  out({ mode, error: 'unknown mode (changed | page)' });
  process.exitCode = 2;
}
