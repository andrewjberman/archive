/**
 * _presets.cjs -- DSGN_AMGTV1 round 31, AV-zi-1 ROLLING WINDOWS (FWD-26), the shared render helper of presets.cjs and windowread.cjs
 * (issuer 2.0.0_SA_COO~D). Not a check: it prints nothing and grades nothing.
 *
 * Method: round29/checks/leadprice/_render.cjs (round15/checks/_load.cjs over the REAL page sources under <cwd>/portal, with the
 * estate stubs: lucide-react, panels, the real GraphicCard, useAuth firm "opal"), with FOUR changes made before LeadPanel loads:
 *   1. THE HOOKS ARE REAL. hooks/useLeadPanelApi.ts loads from source, so the worker's `days` argument and query keys are what run.
 *   2. THE READ LOG (as round30/checks/universe/_universe.cjs). @tanstack/react-query is a recorder: each useQuery is logged with its
 *      key and whether it is ENABLED (react-query v5 semantics: `enabled` false, a function returning false, or skipToken = no
 *      read). An enabled query's queryFn runs at once; @/api/endpoints/amgt-lead-panel is a recorder whose every call is a READ
 *      logged with its arguments, and it SERVES BY WINDOW: getCollectedChatter(days) returns windows.chatter.<days>.json and
 *      getLeadPanelRankings(movement, 'PRICE', limit, days) returns windows.price.<days>.json (days undefined serves the 30-day
 *      payload, the route's own default). Any other ranking subject returns an empty served list.
 *   3. THE PRESET CLICK. Segmented (@/ui/components/Controls) draws <div role="group" data-segmented aria-label> with one <button
 *      data-segment-value data-segment-active> per option and RECORDS its props, onChange included. Every React.useState /
 *      useReducer call is numbered in render order; a click calls the control's own onChange(<option value>), collects the state
 *      writes it makes, and re-renders with those values in place of the initial ones -- the tree a browser shows after the click,
 *      for state held anywhere in the LeadPanel tree.
 *   4. ChatterBubbles and PriceBars are REAL (round 29's stub of ChatterBubbles is replaced by the real module).
 * Fixtures: round31/fixtures/windows.{chatter,price}.{30,90,365}.json (captured on the deployed opal-amgt-scoped-api, code
 *   KQSA62c3, 2026-10-03T01:56Z).
 * Honours the loader's ISSUER GREEN ARM override (CHECK_SRC_OVERRIDE). Writes no file. No network, no AWS.
 */
const fs = require('fs');
const path = require('path');

const R = require(path.join(__dirname, '..', '..', '..', 'round29', 'checks', 'leadprice', '_render.cjs'));
const L = R.L;
const React = R.React;
const ce = R.origCreateElement;
const SA = R.SA;
const FIX = path.join(__dirname, '..', '..', 'fixtures');

const served = (f) => { const d = JSON.parse(fs.readFileSync(path.join(FIX, f), 'utf8')); return d && d.payload && d._capture_note ? d.payload : d; };
const WINDOWS = [30, 90, 365];
const CHATTER = {};
const PRICE = {};
for (const d of WINDOWS) { CHATTER[d] = served(`windows.chatter.${d}.json`); PRICE[d] = served(`windows.price.${d}.json`); }

/** The served window a call asked for: 30 / 90 / 365, 'default' for undefined, or the raw value. */
function daysOf(v) {
  if (v === undefined || v === null) return 'default';
  const n = Number(v);
  return WINDOWS.includes(n) ? n : String(v);
}

// ---------------- the read log: react-query + endpoint recorders ----------------
const SKIP = Symbol.for('presets.skipToken');
const Q = { queries: [], direct: [], cur: null };
function endpointReturn(fn, args) {
  if (fn === 'getCollectedChatter') { const d = daysOf(args[0]); return CHATTER[d === 'default' ? 30 : d]; }
  if (fn === 'getLeadPanelRankings') {
    if (String(args[1]).toUpperCase() !== 'PRICE') return { rows: [], ranking_status: 'EMPTY', ranking_reason: null };
    const d = daysOf(args[3]);
    return PRICE[d === 'default' ? 30 : d];
  }
  if (fn === 'getStarred') return [];
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

// ---------------- state numbering (the click replay) ----------------
const S = { i: 0, override: new Map(), latest: new Map(), writes: [] };
const prevUseState = React.useState;
const prevUseReducer = React.useReducer;
React.useState = function presetsUseState(init) {
  const i = S.i++;
  const pair = prevUseState(S.override.has(i) ? () => S.override.get(i) : init);
  const s = pair[0];
  const set = (next) => {
    const prev = S.latest.has(i) ? S.latest.get(i) : s;
    const v = typeof next === 'function' ? next(prev) : next;
    S.latest.set(i, v);
    S.writes.push([i, v]);
  };
  return [s, set];
};
React.useReducer = function presetsUseReducer(reducer, initArg, initFn) {
  const i = S.i++;
  const pair = S.override.has(i) ? prevUseReducer(reducer, S.override.get(i)) : prevUseReducer(reducer, initArg, initFn);
  const s = pair[0];
  const dispatch = (action) => {
    const prev = S.latest.has(i) ? S.latest.get(i) : s;
    const v = reducer(prev, action);
    S.latest.set(i, v);
    S.writes.push([i, v]);
  };
  return [s, dispatch];
};

// ---------------- Segmented that records its props ----------------
const SEGS = [];
const Segmented = (p) => {
  const q = p || {};
  SEGS.push(q);
  return ce('div', { role: 'group', 'data-segmented': '', 'aria-label': q.ariaLabel },
    ...(q.options || []).map((o, i) => ce('button', {
      key: i, type: 'button', 'data-segment-value': String(o.value),
      'data-segment-active': String(o.value) === String(q.value) ? 'true' : 'false',
    }, o.label)));
};
const ctlCache = {};
const controls = new Proxy({}, {
  get(_t, key) {
    if (key === '__esModule') return true;
    if (typeof key !== 'string') return undefined;
    if (key === 'Segmented') return Segmented;
    if (!ctlCache[key]) ctlCache[key] = (p) => ce('div', { 'data-stub': key, 'aria-label': (p || {}).ariaLabel }, (p || {}).children);
    return ctlCache[key];
  },
});
R.both('src/ui/components/Controls', controls);

// ---------------- the real hooks, the real bubbles ----------------
const HOOKS = L.source(SA + 'hooks/useLeadPanelApi.ts');
R.both(SA + 'hooks/useLeadPanelApi', HOOKS);
R.both(SA + 'components/ChatterBubbles', L.source(SA + 'components/ChatterBubbles.tsx'));

const noop = () => {};
function leadProps(subject) {
  return {
    movement: 'TRENDING', setMovement: noop, subject, setSubject: noop, starredOnly: false, setStarredOnly: noop,
    view: 'list', setView: noop, selectedSecurityKey: null, onSelectSecurity: noop, onClearSecuritySelection: noop,
    searchInput: '', setSearchInput: noop,
  };
}

const PRESET_LABEL = /^\s*(30D|90D|365D|1Y)\s*$/;
/** The window a preset option names: 30 / 90 / 365, or null. */
function optionDays(o) {
  const t = String(o && o.label).trim();
  return t === '30D' ? 30 : t === '90D' ? 90 : t === '365D' || t === '1Y' ? 365 : null;
}
/** The recorded Segmented controls whose every option is a window preset. */
function presetControls(segs) {
  return segs.filter((s) => Array.isArray(s.options) && s.options.length > 0 && s.options.every((o) => PRESET_LABEL.test(String(o && o.label))));
}

/** One render of `fn` (returns html) with replayed state `override`; the reads, queries and Segmented props it made. */
function renderWith(fn, override) {
  S.i = 0; S.override = new Map(override || []); S.latest = new Map(override || []); S.writes = [];
  SEGS.length = 0; Q.queries = []; Q.direct = []; Q.cur = null;
  const html = fn();
  const calls = [...Q.queries.filter((q) => q.enabled).flatMap((q) => q.calls), ...Q.direct];
  return { html, segs: SEGS.slice(), calls, queries: Q.queries.slice() };
}
const leadRender = (subject) => () => {
  const { LeadPanel } = L.source(SA + 'components/LeadPanel.tsx');
  return L.render(LeadPanel, leadProps(subject));
};
/** One render of the REAL LeadPanel on `subject` with replayed state `override`. */
function renderOnce(subject, override) {
  return renderWith(leadRender(subject), override);
}

/**
 * Render `fn` at rest, then select the preset naming `days` through the control's own onChange. Returns
 * { rest, at, stop }: `at` is the render after the click (for days 30 it is the rest render when 30D is already active);
 * `stop` names why no click could be replayed.
 */
function clickTo(fn, days) {
  const rest = renderWith(fn, []);
  const ctl = presetControls(rest.segs)[0];
  if (!ctl) return { rest, at: null, stop: 'no Segmented whose options are 30D / 90D / 365D (or 1Y)' };
  const opt = ctl.options.find((o) => optionDays(o) === days);
  if (!opt) return { rest, at: null, stop: `the preset control has no option naming ${days} days` };
  if (String(ctl.value) === String(opt.value)) return { rest, at: rest, stop: null };
  if (typeof ctl.onChange !== 'function') return { rest, at: null, stop: 'the preset control has no onChange' };
  S.writes = []; S.latest = new Map();
  ctl.onChange(opt.value);
  const writes = S.writes.slice();
  if (writes.length === 0) return { rest, at: null, stop: `selecting ${opt.label} wrote no state` };
  const m = new Map();
  for (const [i, v] of writes) m.set(i, v);
  return { rest, at: renderWith(fn, [...m.entries()]), stop: null };
}
/** clickTo over the REAL LeadPanel on `subject`. */
const renderAt = (subject, days) => clickTo(leadRender(subject), days);

const decode = (s) => String(s).replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&quot;/g, '"').replace(/&#x27;/g, "'").replace(/&#39;/g, "'").replace(/&nbsp;/g, ' ').replace(/&amp;/g, '&');
/** The visible text of an html string (tags dropped, entities decoded, whitespace collapsed); <title> text kept. */
const textOf = (html) => decode(String(html).replace(/<[^>]*>/g, ' ')).replace(/\s+/g, ' ').trim();
const attrAll = (html, attr) => [...String(html).matchAll(new RegExp(`\\s${attr}="([^"]*)"`, 'g'))].map((m) => decode(m[1]));

module.exports = {
  R, L, ce, React, SA, CHATTER, PRICE, WINDOWS, daysOf, Q, S, SKIP, endpoints, rq, Segmented,
  renderWith, renderOnce, clickTo, renderAt, presetControls, optionDays, textOf, attrAll, decode,
};
