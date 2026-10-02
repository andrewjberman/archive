/**
 * _tl.cjs -- the shared instrument of DSGN_AMGTV1 round 29, AV-zg-1 TIMELINE (issuer 2.0.0_SA_COO~D). NOT a check: chart.cjs and
 * dayopen.cjs require it. Writes no file, no network, no AWS.
 *
 * WHAT IT RENDERS: the REAL page sources under <cwd>/portal (round15/checks/_load.cjs: installed typescript + react-dom/server):
 * components/TimelinePanel.tsx (export `TimelinePanel`, prop `securityKey`) and components/HeaderBrief.tsx (export `HeaderBrief`,
 * prop `bundle`), alone or as the overlay mounts them -- the issuer's round-29 ruling for AV-zg-2's SecurityOverlay.tsx:
 * <HeaderBrief bundle={bundle} /> with NO postureLine, then <TimelinePanel securityKey={bundle.security_key} />. Inputs: the served
 * overlay (round14/fixtures/overlay.BA_US_Equity.json) and the served /timeline + /timeline/day bodies, answered by a stubbed
 * `@tanstack/react-query` (a query key holding a YYYY-MM-DD is the day route; any other key is the range route).
 *
 * STUBS (only these; every other source is the real file):
 *   recharts               a serialising stub: a chart (BarChart/ComposedChart/...) renders <div data-rc="<Name>"><svg> around its
 *                          children and hands them its `data`; Bar renders one <div data-rc-bar-slot="<date>"> per data row holding the
 *                          bar's `shape` output (called as recharts calls it) or a <rect> painted with its Cell / Bar fill;
 *                          ReferenceDot/Line/Area render <div data-rc="Reference*" data-rc-x="<x>"> holding their `shape`
 *                          and `label` output; Scatter renders its `shape` per point; Customized renders its component;
 *                          Legend renders its `content`; XAxis/YAxis/Tooltip render nothing. Every call's props are recorded.
 *   src/components/DataTooltip   the estate's ONE shared tooltip, serialised: <div data-shared-tooltip="DataTooltip"> with its
 *                          header and one [data-tt-row][data-tt-label] per row (aggregate first).
 *   src/ui/components/graphic/HeroGraphic   HeroDialog renders <div data-hero-graphic="HeroDialog"> with its children ONLY
 *                          when `open` is truthy (a closed dialog renders nothing); its other exports render their children.
 *   @tanstack/react-query, src/api/api-client   as above / never called.
 *
 * PRESSING SOMETHING IN A STATIC RENDER (the one non-obvious part): react-dom/server runs no handlers, so this file
 *   (1) records every element created with an `onClick` that carries data-timeline-marker, data-day-bar or data-article-more
 *       (react/jsx-runtime's jsx/jsxs and React.createElement are wrapped; the element itself is untouched); and
 *   (2) replaces React.useState with a replayable store keyed by call order: a setter called after the render stores its value,
 *       and the next render returns it at the same call position.
 * press() calls the recorded handler, then renders again with the stored values -- one click, then what the page draws next.
 * A handler that sets no state (or none of these hooks carrying an onClick) leaves nothing to replay: press() returns null.
 */
const fs = require('fs');
const path = require('path');
const { createRequire } = require('module');

const DROOT = path.join(__dirname, '..', '..', '..'); // .../deliverables/2.0.0_SA_COO~D
const L = require(path.join(DROOT, 'round15', 'checks', '_load.cjs'));
const React = L.React;
const preq = createRequire(path.join(L.base, 'package.json'));
const JSXR = preq('react/jsx-runtime');
const h = React.createElement;

// ---- fixtures ---------------------------------------------------------------------------------------------------------
const R14 = path.join(DROOT, 'round14', 'fixtures');
const R29 = path.join(DROOT, 'round29', 'fixtures', 'timeline');
const readJson = (p) => JSON.parse(fs.readFileSync(p, 'utf8'));
const pay = (d) => (d && d.payload ? d.payload : d);
const FX = {
  overlayBA: pay(readJson(path.join(R14, 'overlay.BA_US_Equity.json'))),
  rangeBA: pay(readJson(path.join(R14, 'timeline.BA_US_Equity.json'))),
  rangeHK: pay(readJson(path.join(R14, 'timeline.992_HK_Equity.json'))),
  dayBA0908: pay(readJson(path.join(R14, 'timelineDay.BA_US_Equity.2026-09-08.json'))),
  dayHK0813: pay(readJson(path.join(R14, 'timelineDay.992_HK_Equity.2026-08-13.json'))),
  dayBA0907: pay(readJson(path.join(R29, 'timelineDay.BA_US_Equity.2026-09-07.PLANTED.json'))),
  markers: readJson(path.join(R29, 'markers.BA_US_Equity.PLANTED.json')),
};
const clone = (x) => JSON.parse(JSON.stringify(x));

// ---- press capture + replayable useState --------------------------------------------------------------------------------
const PRESS_HOOKS = ['data-timeline-marker', 'data-day-bar', 'data-article-more'];
const captured = [];
function note(type, props) {
  if (props && typeof props.onClick === 'function' && PRESS_HOOKS.some((a) => props[a] !== undefined)) captured.push({ type, props });
}
const wrap = (orig) =>
  function wrapped(type, props) {
    note(type, props);
    return orig.apply(this, arguments);
  };
JSXR.jsx = wrap(JSXR.jsx);
JSXR.jsxs = wrap(JSXR.jsxs);
React.createElement = wrap(React.createElement);

const S = { idx: 0, over: new Map(), seen: [], pending: new Map() };
React.useState = function replayableUseState(init) {
  const i = S.idx++;
  const v = S.over.has(i) ? S.over.get(i) : typeof init === 'function' ? init() : init;
  S.seen[i] = v;
  const set = (nv) => {
    const cur = S.pending.has(i) ? S.pending.get(i) : S.seen[i];
    S.pending.set(i, typeof nv === 'function' ? nv(cur) : nv);
  };
  return [v, set];
};

// ---- recharts serialising stub ------------------------------------------------------------------------------------------
const rcCalls = [];
const DataCtx = React.createContext(null);
const CHARTS = new Set(['BarChart', 'ComposedChart', 'LineChart', 'AreaChart', 'ScatterChart']);
const VB = { x: 0, y: 0, width: 12, height: 200 };
const rcCache = {};
function rc(name) {
  if (rcCache[name]) return rcCache[name];
  let C;
  if (CHARTS.has(name)) {
    // The children render inside an <svg>, as recharts draws them: React keeps an SVG <title> in place there (outside an
    // <svg> React 19 hoists <title> to the document head, so a marker's hover title would be lost from the marker).
    C = (p) => {
      rcCalls.push({ name, props: p });
      return h(DataCtx.Provider, { value: p.data || [] }, h('div', { 'data-rc': name, 'data-rc-height': p.height === undefined ? undefined : String(p.height) }, h('svg', { 'data-rc-surface': '' }, p.children)));
    };
  } else if (name === 'ResponsiveContainer') {
    C = (p) => {
      rcCalls.push({ name, props: p });
      return h('div', { 'data-rc': name, 'data-rc-height': p.height === undefined ? undefined : String(p.height) }, p.children);
    };
  } else if (name === 'Bar') {
    C = function BarStub(p) {
      rcCalls.push({ name, props: p });
      const data = React.useContext(DataCtx) || [];
      const cells = React.Children.toArray(p.children).filter((c) => c && c.type === rc('Cell'));
      const slots = data.map((entry, i) => {
        const value = typeof p.dataKey === 'function' ? p.dataKey(entry) : entry[p.dataKey];
        const hgt = (Number(value) || 0) * 10;
        const rp = { ...entry, x: i * 6, y: 200 - hgt, width: 4, height: hgt, value, payload: entry, index: i, dataKey: p.dataKey, fill: p.fill, fillOpacity: p.fillOpacity };
        let out;
        if (typeof p.shape === 'function') out = p.shape(rp);
        else if (React.isValidElement(p.shape)) out = React.cloneElement(p.shape, rp);
        else {
          const cell = cells[i] ? cells[i].props : {};
          out = h('rect', { fill: cell.fill !== undefined ? cell.fill : p.fill, fillOpacity: cell.fillOpacity !== undefined ? cell.fillOpacity : p.fillOpacity, stroke: cell.stroke !== undefined ? cell.stroke : p.stroke });
        }
        return h('div', { key: i, 'data-rc-bar-slot': entry && entry.date !== undefined ? String(entry.date) : String(i) }, out);
      });
      return h('div', { 'data-rc': name }, slots);
    };
  } else if (/^Reference(Dot|Line|Area)$/.test(name)) {
    C = (p) => {
      rcCalls.push({ name, props: p });
      const parts = [];
      const sp = { ...p, cx: 6, cy: 6, x: 6, y: 6, r: p.r || 4, viewBox: VB };
      if (typeof p.shape === 'function') parts.push(p.shape(sp));
      else if (React.isValidElement(p.shape)) parts.push(React.cloneElement(p.shape, sp));
      parts.push(labelOut(p.label));
      const x = p.x !== undefined ? p.x : p.x1;
      return h('div', { 'data-rc': name, 'data-rc-x': x === undefined || x === null ? undefined : String(x) }, ...parts.map((x2, i) => h(React.Fragment, { key: i }, x2)), p.children);
    };
  } else if (name === 'Scatter') {
    C = function ScatterStub(p) {
      rcCalls.push({ name, props: p });
      const ctx = React.useContext(DataCtx) || [];
      const pts = p.data || ctx;
      return h('div', { 'data-rc': name }, pts.map((pt, i) => {
        const sp = { ...pt, cx: i * 6, cy: 6, x: i * 6, y: 6, payload: pt, index: i, fill: p.fill };
        const out = typeof p.shape === 'function' ? p.shape(sp) : React.isValidElement(p.shape) ? React.cloneElement(p.shape, sp) : h('circle', { fill: p.fill });
        return h('div', { key: i, 'data-rc-point': String(i) }, out);
      }));
    };
  } else if (name === 'Customized') {
    C = (p) => {
      rcCalls.push({ name, props: p });
      const ctx = React.useContext(DataCtx) || [];
      const cp = { data: ctx, width: 600, height: 200, offset: { left: 0, top: 0, width: 600, height: 200 } };
      const out = React.isValidElement(p.component) ? React.cloneElement(p.component, cp) : typeof p.component === 'function' ? h(p.component, cp) : null;
      return h('div', { 'data-rc': name }, out);
    };
  } else if (name === 'Legend') {
    C = (p) => {
      rcCalls.push({ name, props: p });
      const lp = { payload: [] };
      const out = React.isValidElement(p.content) ? React.cloneElement(p.content, lp) : typeof p.content === 'function' ? h(p.content, lp) : null;
      return h('div', { 'data-rc': name }, out);
    };
  } else if (name === 'Label') {
    C = (p) => {
      rcCalls.push({ name, props: p });
      if (typeof p.content === 'function') return h('div', { 'data-rc': name }, p.content({ ...p, viewBox: VB }));
      return h('div', { 'data-rc': name }, p.value !== undefined ? String(p.value) : p.children);
    };
  } else if (['Rectangle', 'Dot', 'Symbols', 'Curve', 'Sector', 'Cross', 'Polygon', 'Trapezoid'].includes(name)) {
    // recharts' shape primitives: keep the paint and every data-* hook, so a shape drawn with them is read like an SVG one.
    C = (p) => {
      rcCalls.push({ name, props: p });
      const attrs = { 'data-rc': name, fill: p.fill, stroke: p.stroke, fillOpacity: p.fillOpacity };
      for (const k of Object.keys(p)) if (/^(data-|aria-)/.test(k) || k === 'title') attrs[k] = p[k];
      return h('div', attrs, p.children);
    };
  } else if (['XAxis', 'YAxis', 'Tooltip', 'Cell', 'CartesianGrid', 'LabelList', 'Brush', 'Line', 'Area', 'PolarGrid'].includes(name)) {
    C = (p) => {
      rcCalls.push({ name, props: p });
      return null;
    };
  } else {
    C = (p) => {
      rcCalls.push({ name, props: p || {} });
      return h('div', { 'data-rc': name }, (p || {}).children);
    };
  }
  C.displayName = name;
  rcCache[name] = C;
  return C;
}
function labelOut(label) {
  if (label === undefined || label === null || label === false) return null;
  if (typeof label === 'string' || typeof label === 'number') return h('span', { 'data-rc-label': '' }, String(label));
  if (typeof label === 'function') return label({ viewBox: VB, offset: 5 });
  if (React.isValidElement(label)) return React.cloneElement(label, { viewBox: VB });
  if (typeof label === 'object' && label.value !== undefined) return h('span', { 'data-rc-label': '' }, String(label.value));
  return null;
}
L.stubSource('recharts', new Proxy({}, {
  get(_t, k) {
    if (k === '__esModule') return true;
    if (typeof k !== 'string') return undefined;
    return rc(k);
  },
}));

// ---- the shared tooltip, the dialog, the queries -------------------------------------------------------------------------
function DataTooltipStub({ header, aggregate, rows }) {
  const out = [h('div', { key: 'h', 'data-tt-header': '' }, header)];
  if (aggregate) out.push(h('div', { key: 'a', 'data-tt-row': 'aggregate', 'data-tt-label': String(aggregate.label) }, aggregate.label, ': ', aggregate.value));
  (rows || []).forEach((r, i) => out.push(h('div', { key: i, 'data-tt-row': String(i), 'data-tt-label': String(r.label) }, r.label, ': ', r.value)));
  return h('div', { 'data-shared-tooltip': 'DataTooltip' }, out);
}
const dataTooltipModule = { __esModule: true, DataTooltip: DataTooltipStub, default: DataTooltipStub };
L.stubSource('src/components/DataTooltip.tsx', dataTooltipModule);
L.stubSource('src/components/DataTooltip', dataTooltipModule);

function HeroDialogStub(p) {
  if (!p.open) return null;
  return h('div', { 'data-hero-graphic': 'HeroDialog' }, p.title ? h('div', { 'data-hero-title': '' }, p.title) : null, p.children, p.footer || null);
}
const heroCache = {};
const heroModule = new Proxy({}, {
  get(_t, k) {
    if (k === '__esModule') return true;
    if (typeof k !== 'string') return undefined;
    if (k === 'HeroDialog') return HeroDialogStub;
    if (!heroCache[k]) {
      heroCache[k] = (p) => h('div', { 'data-stub': k }, (p || {}).children);
      heroCache[k].displayName = k;
    }
    return heroCache[k];
  },
});
L.stubSource('src/ui/components/graphic/HeroGraphic.tsx', heroModule);
L.stubSource('src/ui/components/graphic/HeroGraphic', heroModule);

const Q = { range: null, days: {} };
const DAY = /^\d{4}-\d{2}-\d{2}$/;
function flat(x, out) {
  if (Array.isArray(x)) x.forEach((y) => flat(y, out));
  else if (x && typeof x === 'object') Object.values(x).forEach((y) => flat(y, out));
  else out.push(x);
  return out;
}
function useQueryStub(opts) {
  const o = opts || {};
  const base = { error: null, isError: false, isFetching: false, refetch: () => Promise.resolve(), fetchStatus: 'idle' };
  if (o.enabled === false) return { ...base, data: undefined, isLoading: false, isPending: true, isSuccess: false, status: 'pending' };
  const keys = flat(o.queryKey || [], []);
  const date = keys.find((k) => typeof k === 'string' && DAY.test(k));
  let data;
  if (date) {
    data = Q.days[date];
    if (data === undefined) return { ...base, data: undefined, isLoading: true, isPending: true, isSuccess: false, status: 'pending' };
  } else data = Q.range;
  if (typeof o.select === 'function' && data !== undefined) data = o.select(data);
  return { ...base, data, isLoading: false, isPending: false, isSuccess: true, status: 'success' };
}
L.stubSource('@tanstack/react-query', {
  __esModule: true,
  useQuery: useQueryStub,
  useSuspenseQuery: useQueryStub,
  useQueries: (o) => ((o && o.queries) || []).map(useQueryStub),
  useQueryClient: () => ({ prefetchQuery: () => Promise.resolve(), fetchQuery: () => Promise.resolve(), getQueryData: () => undefined, invalidateQueries: () => Promise.resolve() }),
  keepPreviousData: (x) => x,
  QueryClient: function QueryClient() {},
  QueryClientProvider: (p) => p.children,
});
const api = { __esModule: true, apiRequest: () => Promise.resolve(undefined) };
L.stubSource('src/api/api-client.ts', api);
L.stubSource('src/api/api-client', api);

// ---- render + press ----------------------------------------------------------------------------------------------------
let HB = null;
let TP = null;
let loadError = null;
try {
  HB = L.source('src/pages/SecurityAnalysis/components/HeaderBrief.tsx').HeaderBrief;
  TP = L.source('src/pages/SecurityAnalysis/components/TimelinePanel.tsx').TimelinePanel;
  if (typeof HB !== 'function') loadError = 'HeaderBrief.tsx exports no HeaderBrief';
  else if (typeof TP !== 'function') loadError = 'TimelinePanel.tsx exports no TimelinePanel';
} catch (e) {
  loadError = String(e.message).split('\n')[0];
}
/** The overlay's order as the issuer ruled it for AV-zg-2's SecurityOverlay.tsx (round 29): <HeaderBrief bundle /> (no
 * postureLine) and then <TimelinePanel securityKey={bundle.security_key} /> -- this cell's two components as the page mounts them. */
function Overlay({ bundle }) {
  return h('div', { 'data-check-overlay': '' }, h(HB, { bundle }), h(TP, { securityKey: bundle.security_key }));
}
let dateWords = null;
try {
  dateWords = L.source('src/pages/SecurityAnalysis/dateWords.ts');
} catch (e) {
  dateWords = null;
}

function renderState(Component, props, over) {
  S.idx = 0;
  S.over = new Map(over || []);
  S.seen = [];
  S.pending = new Map();
  captured.length = 0;
  rcCalls.length = 0;
  let html;
  try {
    html = Component ? L.render(Component, props) : 'RENDER FAILED: ' + (loadError || 'no component');
  } catch (e) {
    html = 'RENDER FAILED: ' + String(e.message).split('\n')[0];
  }
  return { html, tree: parse(html), captured: captured.slice(), rc: rcCalls.slice(), over: new Map(S.over), Component, props, q: { range: Q.range, days: Q.days } };
}
const fakeEvent = () => ({ stopPropagation() {}, preventDefault() {}, currentTarget: {}, target: {} });
/** Call fire() (which invokes a handler recorded in `state`), then render again with what the handler stored. */
function press(state, fire) {
  // The state's own served bodies answer the next render, whatever was rendered in between.
  Q.range = state.q.range;
  Q.days = state.q.days;
  S.pending = new Map();
  try {
    fire();
  } catch (e) {
    return null;
  }
  if (S.pending.size === 0) return null;
  const over = new Map([...state.over, ...S.pending]);
  return renderState(state.Component, state.props, over);
}
function bundleFor(range) {
  const bundle = clone(FX.overlayBA);
  bundle.security_key = range && range.security_key ? range.security_key : bundle.security_key;
  return bundle;
}
/** The overlay (HeaderBrief, then TimelinePanel) on the BA overlay, the given range payload and day bodies. */
function renderOverlay(range, days) {
  Q.range = range;
  Q.days = days || {};
  return renderState(HB && TP ? Overlay : null, { bundle: bundleFor(range) });
}
/** TimelinePanel alone, as the overlay mounts it. */
function renderPanel(range, days) {
  Q.range = range;
  Q.days = days || {};
  return renderState(TP, { securityKey: bundleFor(range).security_key });
}
/** HeaderBrief alone, with the props the overlay passes (and, to prove it is ignored, a planted postureLine). */
function renderHeader(range, extraProps) {
  Q.range = range;
  Q.days = {};
  return renderState(HB, { bundle: bundleFor(range), ...(extraProps || {}) });
}
/** Press the day bar for `date`: the element carrying data-day-bar="<date>" and an onClick; else the Bar's own onClick; else the
 * chart's onClick (recharts' three click surfaces), each called as recharts calls it. Returns the next state or null. */
function pressDay(state, date) {
  const el = state.captured.find((c) => c.props['data-day-bar'] === date);
  if (el) {
    const next = press(state, () => el.props.onClick(fakeEvent()));
    if (next) return next;
  }
  const chart = state.rc.find((c) => CHARTS.has(c.name));
  const data = (chart && chart.props.data) || [];
  const i = data.findIndex((e) => e && e.date === date);
  const entry = data[i];
  const bar = state.rc.find((c) => c.name === 'Bar' && typeof c.props.onClick === 'function');
  if (bar && entry) {
    const next = press(state, () => bar.props.onClick({ ...entry, payload: entry, value: entry.articles_total }, i, fakeEvent()));
    if (next) return next;
  }
  if (chart && typeof chart.props.onClick === 'function' && entry) {
    const st = { activeLabel: date, activeIndex: i, activeTooltipIndex: i, activePayload: [{ payload: entry }], activeCoordinate: { x: 0, y: 0 } };
    const next = press(state, () => chart.props.onClick(st, fakeEvent()));
    if (next) return next;
  }
  return null;
}
/** Press the marker for `date` of `kind`: the element carrying data-timeline-marker="<kind>" data-marker-day="<date>" and an
 * onClick; else a Reference* whose x is that date and which carries its own onClick. */
function pressMarker(state, kind, date) {
  const el = state.captured.find((c) => c.props['data-timeline-marker'] === kind && c.props['data-marker-day'] === date);
  if (el) {
    const next = press(state, () => el.props.onClick(fakeEvent()));
    if (next) return next;
  }
  const ref = state.rc.find((c) => /^Reference/.test(c.name) && (c.props.x === date || c.props.x1 === date) && typeof c.props.onClick === 'function');
  if (ref) return press(state, () => ref.props.onClick(fakeEvent()));
  return null;
}

// ---- a small HTML tree (react-dom/server markup is well formed) ----------------------------------------------------------
const VOID = new Set(['area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'source', 'track', 'wbr']);
function decode(s) {
  return String(s).replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&quot;/g, '"').replace(/&#x27;/g, "'").replace(/&#39;/g, "'").replace(/&nbsp;/g, ' ').replace(/&amp;/g, '&');
}
function parse(html) {
  const root = { tag: '#root', attrs: {}, children: [], parent: null, at: 0 };
  let cur = root;
  const re = /<!--[\s\S]*?-->|<\/([a-zA-Z][\w:-]*)\s*>|<([a-zA-Z][\w:-]*)((?:\s+[^\s=>\/]+(?:="[^"]*")?)*)\s*(\/?)>|([^<]+)/g;
  let m;
  while ((m = re.exec(html)) !== null) {
    if (m[1]) {
      let n = cur;
      while (n && n.tag !== m[1].toLowerCase()) n = n.parent;
      if (n && n.parent) cur = n.parent;
    } else if (m[2]) {
      const attrs = {};
      const ar = /([^\s=>\/]+)(?:="([^"]*)")?/g;
      let a;
      while ((a = ar.exec(m[3] || '')) !== null) attrs[a[1]] = a[2] === undefined ? '' : decode(a[2]);
      const node = { tag: m[2].toLowerCase(), attrs, children: [], parent: cur, at: m.index };
      cur.children.push(node);
      if (!m[4] && !VOID.has(node.tag)) cur = node;
    } else if (m[5]) {
      cur.children.push({ text: decode(m[5]), parent: cur, at: m.index });
    }
  }
  return root;
}
function all(node, pred, out) {
  out = out || [];
  for (const c of node.children || []) {
    if (c.tag) {
      if (pred(c)) out.push(c);
      all(c, pred, out);
    }
  }
  return out;
}
const byAttr = (tree, attr, value) => all(tree, (n) => n.attrs[attr] !== undefined && (value === undefined || n.attrs[attr] === value));
function text(node, skip) {
  if (node.text !== undefined) return node.text;
  if (skip && skip(node)) return ' ';
  if (node.tag === 'title') return ' ';
  return (node.children || []).map((c) => text(c, skip)).join(' ');
}
const norm = (s) => String(s).replace(/\s+/g, ' ').trim();
const visible = (node, skip) => norm(text(node, skip));
/** Every word a person can read on or over the node: visible text, <title> children, title= and aria-label= attributes. */
function readable(node) {
  const parts = [visible(node)];
  for (const n of [node, ...all(node, () => true)]) {
    if (n.attrs.title) parts.push(n.attrs.title);
    if (n.attrs['aria-label']) parts.push(n.attrs['aria-label']);
    if (n.tag === 'title') parts.push(norm(text({ children: n.children })));
  }
  return norm(parts.join(' '));
}
function within(node, pred) {
  for (let n = node.parent; n; n = n.parent) if (n.tag && pred(n)) return n;
  return null;
}
const inChart = (node) => within(node, (n) => CHARTS.has(n.attrs['data-rc']));
const inHero = (node) => within(node, (n) => n.attrs['data-hero-graphic'] !== undefined);

// ---- shared words ------------------------------------------------------------------------------------------------------
const CODE = /\b[a-z]+_[a-z0-9_]+\b|_Equity\b|\.json\b|\b[A-Z][A-Z0-9]*_[A-Z0-9_]+\b|\b(DENIED|PARTIAL|COMPLETE)\b/;
const STATUS = /--status-|--(danger|warning|success|info)\b|#be2d36|#d37c17|#257e55|#2970a3|rgb\(\s*190\s*,\s*45\s*,\s*54\s*\)|\b(text|bg|fill|stroke)-(red|orange|amber|yellow|green|emerald|rose)-\d/i;

module.exports = {
  L, React, h, FX, Q, clone, renderOverlay, renderPanel, renderHeader, renderState, press, pressDay, pressMarker, parse, all, byAttr,
  text, visible, readable, within, inChart, inHero, norm, decode, CODE, STATUS, CHARTS, dateWords, loadError: () => loadError,
};
