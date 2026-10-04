/**
 * _universe.cjs -- DSGN_AMGTV1 round 30, AV-zh-1 ONE UNIVERSE PER FACE (cell-slug universe), the shared render helper of
 * universe.cjs and resolutionwords.cjs (issuer 2.0.0_SA_COO~D). Not a check: it prints nothing and grades nothing.
 *
 * Method: the round-29 lead/price harness (round29/checks/leadprice/_render.cjs, itself round15/checks/_load.cjs over the REAL
 * page sources under <cwd>/portal) for every estate stub (lucide-react, Controls, the real panels, the real GraphicCard, useAuth
 * firm "opal"), with THREE changes made before LeadPanel loads:
 *   1. THE HOOKS ARE REAL. hooks/useLeadPanelApi.ts is loaded from source (not the loader's hook proxy), so whatever the worker
 *      writes there -- an `enabled` flag, a skipToken, a new argument -- is what runs.
 *   2. THE READ LOG. @tanstack/react-query is a recorder: every useQuery call is logged with its key and whether it is ENABLED
 *      (`enabled` false, a function returning false, or `queryFn: skipToken` = disabled, react-query v5 semantics). An enabled
 *      query's queryFn is invoked at once; @/api/endpoints/amgt-lead-panel is a recorder too, so every endpoint function the
 *      queryFn calls is a READ, logged with its arguments, and returns the planted fixture synchronously. A disabled query makes
 *      no read and returns data undefined (status pending, isLoading false). An endpoint called outside any useQuery during
 *      render is logged as a direct read.
 *   3. ChatterBubbles (another cell's file) is a stub that draws one <span data-stub-bubble="<security_key>"> per row LeadPanel
 *      hands it in `data.rows` -- the bubbles the Chatter face would draw. PriceBars stays REAL (its bars carry data-price-bar).
 * Fixtures: round30/fixtures/windows.price.30.json (served price ranking, 94 rows, resolution CROSSED), windows.chatter.30.json
 *   (served collected chatter, 95 rows, every row with its ticker), round14/fixtures/rankings.trending.chatter.json (the served
 *   chatter-ranking shape) and round30/fixtures/universe/universe.planted.json (starred list, EMPTY and DECOY chatter rankings,
 *   a SUBJECT_ONLY_FALLBACK resolution).
 * Honours the loader's ISSUER GREEN ARM override (CHECK_SRC_OVERRIDE, see round15/checks/_load.cjs) for LeadPanel.tsx and
 * useLeadPanelApi.ts. Writes no file. No network, no AWS.
 */
const fs = require('fs');
const path = require('path');

const R = require(path.join(__dirname, '..', '..', '..', 'round29', 'checks', 'leadprice', '_render.cjs'));
const L = R.L;
const ce = R.origCreateElement;
const SA = R.SA;
const FIX = path.join(__dirname, '..', '..', 'fixtures');
const DELIV = path.join(__dirname, '..', '..', '..');

const readJson = (p) => JSON.parse(fs.readFileSync(p, 'utf8'));
const served = (p) => { const d = readJson(p); return d && d.payload && d._capture_note ? d.payload : d; };
const clone = (x) => JSON.parse(JSON.stringify(x));

const PRICE = served(path.join(FIX, 'windows.price.30.json'));
const COLLECTED = served(path.join(FIX, 'windows.chatter.30.json'));
const PLANT = readJson(path.join(FIX, 'universe', 'universe.planted.json'));
const CHAT_SHAPE = served(path.join(DELIV, PLANT.chatter_ranking_shape));

/** The planted chatter rankings, each on the served route's shape. */
const CHATTER_RANKING = {
  EMPTY: Object.assign(clone(CHAT_SHAPE), PLANT.chatter_ranking_empty),
  DECOY: (() => {
    const p = clone(CHAT_SHAPE);
    p.rows = PLANT.chatter_ranking_decoy_rows.map((d, i) => Object.assign(clone(CHAT_SHAPE.rows[0]), d, {
      rank: i + 1, rank_sort: String(i + 1).padStart(5, '0'), display_name: d.name,
    }));
    p.row_count = p.rows.length; p.rows_read = p.rows.length; p.generation_row_count = p.rows.length;
    return p;
  })(),
};
const PRICE_FALLBACK = Object.assign(clone(PRICE), { resolution: clone(PLANT.price_resolution_fallback) });
const STARRED = PLANT.starred;

// ---------------- the read log: react-query + endpoints recorders ----------------
const SKIP = Symbol.for('universe.skipToken');
const Q = { queries: [], direct: [], cur: null, price: PRICE, chatterRanking: CHATTER_RANKING.EMPTY, starred: STARRED, collected: COLLECTED };

function endpointReturn(fn, args) {
  if (fn === 'getLeadPanelRankings') return String(args[1]).toUpperCase() === 'PRICE' ? Q.price : Q.chatterRanking;
  if (fn === 'getCollectedChatter') return Q.collected;
  if (fn === 'getStarred') return Q.starred;
  if (fn === 'getRankTimeSeries') return { rows: [] };
  return undefined;
}
const epCache = {};
const endpoints = new Proxy({}, {
  get(_t, key) {
    if (key === '__esModule') return true;
    if (typeof key !== 'string' || key === 'then' || key === 'default') return undefined;
    if (!epCache[key]) {
      epCache[key] = (...args) => {
        const rec = { fn: key, args, ret: endpointReturn(key, args) };
        (Q.cur ? Q.cur.calls : Q.direct).push(rec);
        return rec.ret;
      };
    }
    return epCache[key];
  },
});

function queryResult(data, enabled) {
  return {
    data, error: null, isError: false, isLoading: false, isFetching: false, isPending: !enabled, isSuccess: !!enabled,
    status: enabled ? 'success' : 'pending', fetchStatus: 'idle', refetch: () => {},
  };
}
function useQuery(opts) {
  const o = opts || {};
  let enabled = true;
  if (o.enabled === false || o.queryFn === SKIP) enabled = false;
  else if (typeof o.enabled === 'function') enabled = o.enabled({ queryKey: o.queryKey, state: {} }) !== false;
  const q = { key: JSON.stringify(o.queryKey === undefined ? null : o.queryKey), enabled, calls: [] };
  Q.queries.push(q);
  if (!enabled) return queryResult(undefined, false);
  Q.cur = q;
  let out;
  try {
    out = typeof o.queryFn === 'function' ? o.queryFn({ queryKey: o.queryKey, meta: o.meta, signal: undefined }) : undefined;
  } finally { Q.cur = null; }
  let data = out && typeof out.then === 'function' ? (q.calls.length ? q.calls[q.calls.length - 1].ret : undefined) : out;
  if (typeof o.select === 'function' && data !== undefined) data = o.select(data);
  return queryResult(data, true);
}
const rqKnown = {
  useQuery,
  useSuspenseQuery: useQuery,
  useQueries: (o) => ((o && o.queries) || []).map(useQuery),
  useMutation: () => ({ mutate: () => {}, mutateAsync: async () => {}, isPending: false, isError: false }),
  useQueryClient: () => ({ invalidateQueries: () => {}, setQueryData: () => {}, getQueryData: () => undefined, prefetchQuery: async () => {} }),
  skipToken: SKIP,
  keepPreviousData: (x) => x,
  queryOptions: (x) => x,
};
const rq = new Proxy({}, {
  get(_t, key) {
    if (key === '__esModule') return true;
    if (typeof key !== 'string') return undefined;
    if (Object.prototype.hasOwnProperty.call(rqKnown, key)) return rqKnown[key];
    return () => undefined;
  },
});
L.stubSource('@tanstack/react-query', rq);
L.stubSource('@/api/endpoints/amgt-lead-panel', endpoints);
for (const k of ['src/api/endpoints/amgt-lead-panel', 'src/api/endpoints/amgt-lead-panel.ts', 'src/api/endpoints/amgt-lead-panel.tsx',
  'src/api/endpoints/amgt-lead-panel/index.ts', 'src/api/endpoints/amgt-lead-panel/index.tsx']) L.stubSource(k, endpoints);

// ---------------- the real hooks, and the bubbles stub ----------------
const HOOKS = L.source(SA + 'hooks/useLeadPanelApi.ts');
R.both(SA + 'hooks/useLeadPanelApi', HOOKS);
R.both(SA + 'components/ChatterBubbles', {
  ChatterBubbles: (p) => {
    const rows = p && p.data && Array.isArray(p.data.rows) ? p.data.rows : [];
    return ce('div', { 'data-stub': 'ChatterBubbles', 'data-stub-month': String(p && p.month) },
      ...rows.map((r, i) => ce('span', { key: i, 'data-stub-bubble': String(r && r.security_key) })));
  },
});

const noop = () => {};
function leadProps(subject, starredOnly) {
  return {
    movement: 'TRENDING', setMovement: noop, subject, setSubject: noop, starredOnly: !!starredOnly, setStarredOnly: noop,
    view: 'list', setView: noop, selectedSecurityKey: null, onSelectSecurity: noop, onClearSecuritySelection: noop,
    searchInput: '', setSearchInput: noop,
  };
}
const attrAll = (html, attr) => [...html.matchAll(new RegExp(`\\s${attr}="([^"]*)"`, 'g'))].map((m) => m[1]);

/**
 * Render the REAL LeadPanel on `subject` with `starredOnly`, over the price payload `price` (default the served one) and the
 * planted chatter ranking `chatterRanking` ('EMPTY' | 'DECOY'). Returns the html, the READS made (endpoint calls from enabled
 * queries plus direct calls), the queries seen, the bubbles handed to ChatterBubbles and the price bars drawn.
 */
function renderFace(subject, starredOnly, opt) {
  const o = opt || {};
  Q.queries = []; Q.direct = []; Q.cur = null;
  Q.price = o.price || PRICE;
  Q.chatterRanking = CHATTER_RANKING[o.chatterRanking || 'EMPTY'];
  const { LeadPanel } = L.source(SA + 'components/LeadPanel.tsx');
  const html = L.render(LeadPanel, leadProps(subject, starredOnly));
  const calls = [...Q.queries.filter((q) => q.enabled).flatMap((q) => q.calls), ...Q.direct];
  const reads = calls.map((c) => ({ fn: c.fn, subject: c.fn === 'getLeadPanelRankings' || c.fn === 'getRankTimeSeries' ? String(c.args[1]).toUpperCase() : null }));
  return {
    html, reads, queries: Q.queries.slice(), direct: Q.direct.length,
    bubbles: attrAll(html, 'data-stub-bubble'),
    bars: attrAll(html, 'data-price-bar'),
  };
}

module.exports = { R, L, ce, SA, PRICE, PRICE_FALLBACK, COLLECTED, STARRED, CHATTER_RANKING, Q, rq, endpoints, SKIP, renderFace, attrAll };
