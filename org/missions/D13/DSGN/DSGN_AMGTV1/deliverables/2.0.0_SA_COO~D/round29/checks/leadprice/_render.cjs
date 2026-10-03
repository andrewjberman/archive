/**
 * _render.cjs -- DSGN_AMGTV1 round 29, AV-zg-3 (cell-slug leadprice), the shared render helper of leadface.cjs and pricemovers.cjs
 * (issuer 2.0.0_SA_COO~D). Not a check: it prints nothing and grades nothing.
 *
 * Method: round15/checks/_load.cjs (the REAL page sources under <cwd>/portal transpiled with the installed typescript, rendered with
 * react-dom/server), with these stubs set before LeadPanel loads:
 *   - lucide-react: <svg data-icon=<name> aria-label>.
 *   - @/ui/components/Controls: Segmented -> <div role="group" aria-label> with one <button> per option; other controls pass through.
 *   - @/ui/components/panels: the REAL Panel, PanelContent, PanelHeader, PanelFooter, NestedCard, DarkCard and SectionCard sources (so a
 *     band-valued container renders its real `dark-band` / band background class); SmartPanelFooter, which wraps the band-valued
 *     PanelFooter, renders as a band; PanelGrid passes through.
 *   - @/ui/components/graphic/GraphicCard: the REAL source (the /philosophy card face); its GraphicPanel (the navy top) is the loader's
 *     stub, <div data-stub="GraphicPanel">, so the navy subtree is findable.
 *   - @/hooks/useAuth: a firm. ChatterBubbles (another cell's file): <div data-stub="ChatterBubbles"> recording whether it received a
 *     month and an onMonthChange function.
 *   - page hooks: useLeadPanelRankings -> the price fixture on PRICE; useCollectedChatter -> the chatter fixture; useStarredList -> [].
 * THE CLICK REPLAY (`clickThrough`): react-dom/server keeps no state, so a click is replayed. Every React.useState / useReducer call is
 * numbered in render order and its setter recorded; the `jsx` factory records the props of the element carrying `data-price-expand`.
 * A click calls that element's own onClick, collects the state writes it makes, and re-renders with those values in place of the
 * initial ones -- the same tree a browser would show after the click, for state held by useState/useReducer anywhere in the face.
 * When the control is a <summary>/<details>, the click opens every closed <details> in the markup instead.
 * Writes no file. No network, no AWS.
 */
const fs = require('fs');
const path = require('path');
const { createRequire } = require('module');

const L = require(path.join(__dirname, '..', '..', '..', 'round15', 'checks', '_load.cjs'));
const React = L.React;
const req = createRequire(path.join(L.base, 'package.json'));
const SA = 'src/pages/SecurityAnalysis/';

const FIX = {
  live: path.join(__dirname, '..', '..', 'fixtures', 'leadprice', 'rankings.trending.price.live.json'),
  r15a: path.join(__dirname, '..', '..', '..', 'round15', 'fixtures', 'r15a.rankings.TRENDING_PRICE.return30d.json'),
  chatter: path.join(__dirname, '..', '..', '..', 'round16', 'fixtures', 'r16g.collected.chatter.json'),
};
function loadFixture(name) {
  const d = JSON.parse(fs.readFileSync(FIX[name], 'utf8'));
  return d && d.payload && d._capture_note ? d.payload : d;
}

// ---------------- hook numbering + jsx capture (the click replay) ----------------
const H = { i: 0, override: new Map(), latest: new Map(), writes: [], captured: [] };
const origUseState = React.useState;
const origUseReducer = React.useReducer;
React.useState = function useStateNumbered(init) {
  const i = H.i++;
  const has = H.override.has(i);
  const pair = origUseState(has ? () => H.override.get(i) : init);
  const s = pair[0];
  const set = (next) => {
    const prev = H.latest.has(i) ? H.latest.get(i) : s;
    const v = typeof next === 'function' ? next(prev) : next;
    H.latest.set(i, v);
    H.writes.push([i, v]);
  };
  return [s, set];
};
React.useReducer = function useReducerNumbered(reducer, initArg, initFn) {
  const i = H.i++;
  const has = H.override.has(i);
  const pair = has ? origUseReducer(reducer, H.override.get(i)) : origUseReducer(reducer, initArg, initFn);
  const s = pair[0];
  const dispatch = (action) => {
    const prev = H.latest.has(i) ? H.latest.get(i) : s;
    const v = reducer(prev, action);
    H.latest.set(i, v);
    H.writes.push([i, v]);
  };
  return [s, dispatch];
};
const jr = req('react/jsx-runtime');
for (const k of ['jsx', 'jsxs']) {
  const orig = jr[k];
  jr[k] = function jsxCapture(type, props, key) {
    if (props && Object.prototype.hasOwnProperty.call(props, 'data-price-expand')) H.captured.push({ type: typeof type === 'string' ? type : (type && (type.displayName || type.name)) || 'component', props });
    return orig(type, props, key);
  };
}
const origCreateElement = React.createElement;
React.createElement = function createElementCapture(type, props, ...kids) {
  if (props && Object.prototype.hasOwnProperty.call(props, 'data-price-expand')) H.captured.push({ type: typeof type === 'string' ? type : (type && (type.displayName || type.name)) || 'component', props });
  return origCreateElement(type, props, ...kids);
};

// ---------------- stubs ----------------
const icons = {};
L.stubSource('lucide-react', new Proxy({}, {
  get(_t, key) {
    if (key === '__esModule') return true;
    if (typeof key !== 'string') return undefined;
    if (!icons[key]) { icons[key] = (p) => origCreateElement('svg', { 'data-icon': key, 'aria-label': (p || {})['aria-label'] }); icons[key].displayName = key; }
    return icons[key];
  },
}));
const ctl = {};
const Segmented = (p) => origCreateElement('div', { role: 'group', 'data-segmented': '', 'aria-label': p.ariaLabel },
  ...(p.options || []).map((o, i) => origCreateElement('button', { key: i, type: 'button', 'data-segment-value': String(o.value) }, o.label)));
const controls = new Proxy({}, {
  get(_t, key) {
    if (key === '__esModule') return true;
    if (typeof key !== 'string') return undefined;
    if (key === 'Segmented') return Segmented;
    if (!ctl[key]) ctl[key] = (p) => origCreateElement('div', { 'data-stub': key, 'aria-label': (p || {}).ariaLabel }, (p || {}).children);
    return ctl[key];
  },
});
const both = (rel, mod) => { for (const k of [rel, rel + '.ts', rel + '.tsx']) L.stubSource(k, mod); };
both('src/ui/components/Controls', controls);

const PANEL_DIR = 'src/ui/components/panels/';
const REAL_PANELS = ['Panel', 'PanelContent', 'PanelHeader', 'PanelFooter', 'NestedCard', 'DarkCard', 'SectionCard'];
const panelCache = {};
const slots = (q) => {
  const kids = [];
  for (const s of ['title', 'subtitle', 'eyebrow']) if (typeof q[s] === 'string' && q[s]) kids.push(origCreateElement('span', { key: s, 'data-stub-text': s }, q[s]));
  for (const s of ['actions', 'leftContent', 'children', 'footer', 'content']) if (q[s] !== undefined && q[s] !== null && q[s] !== false) kids.push(origCreateElement(React.Fragment, { key: s }, q[s]));
  return kids;
};
const panels = new Proxy({}, {
  get(_t, key) {
    if (key === '__esModule') return true;
    if (typeof key !== 'string') return undefined;
    if (panelCache[key]) return panelCache[key];
    if (REAL_PANELS.includes(key)) {
      panelCache[key] = L.source(PANEL_DIR + key + '.tsx')[key];
    } else if (key === 'SmartPanelFooter') {
      panelCache[key] = (p) => origCreateElement('div', { 'data-stub': key, className: 'dark-band bg-[hsl(var(--bg-header))]' }, ...slots(p || {}));
    } else {
      panelCache[key] = (p) => origCreateElement('div', { 'data-stub': key }, ...slots(p || {}));
    }
    return panelCache[key];
  },
});
both('src/ui/components/panels', panels);
both('src/ui/components/panels/index', panels);
const realGraphicCard = L.source('src/ui/components/graphic/GraphicCard.tsx');
both('src/ui/components/graphic/GraphicCard', realGraphicCard);
both('src/hooks/useAuth', { useAuth: () => ({ claims: { firmId: 'opal' } }) });
const bubbleSeen = { month: null, onMonthChange: null };
both(SA + 'components/ChatterBubbles', {
  ChatterBubbles: (p) => {
    bubbleSeen.month = p.month;
    bubbleSeen.onMonthChange = typeof p.onMonthChange;
    return origCreateElement('div', { 'data-stub': 'ChatterBubbles', 'data-stub-month': String(p.month), 'data-stub-month-change': typeof p.onMonthChange });
  },
});

const noop = () => {};
function leadProps(subject) {
  return {
    movement: 'TRENDING', setMovement: noop, subject, setSubject: noop, starredOnly: false, setStarredOnly: noop,
    view: 'list', setView: noop, selectedSecurityKey: null, onSelectSecurity: noop, onClearSecuritySelection: noop,
    searchInput: '', setSearchInput: noop,
  };
}

/** Render the REAL LeadPanel on `subject` over the given price payload (and chatter payload). */
function renderLead(subject, price, chatter) {
  L.hookState.impl = {
    useLeadPanelRankings: (_m, s) => (String(s).toUpperCase() === 'PRICE' ? price : undefined),
    useCollectedChatter: () => chatter,
    useRankTimeSeries: () => undefined,
    useStarredList: () => [],
    useSetStarred: () => undefined,
  };
  L.hookState.data = undefined;
  const { LeadPanel } = L.source(SA + 'components/LeadPanel.tsx');
  return L.render(LeadPanel, leadProps(subject));
}

/** Render with the replayed state; returns html and the data-price-expand elements seen in it. */
function renderState(fn, override) {
  H.i = 0;
  H.override = new Map(override || []);
  H.latest = new Map(override || []);
  H.writes = [];
  H.captured = [];
  const html = fn();
  return { html, controls: H.captured.slice() };
}

/**
 * Render, then click the data-price-expand control `clicks` times. Returns [{html, controls, how}] for the rest state and each
 * click, or stops early with `stop` naming why (no control, a dead control, a click that writes no state).
 */
function clickThrough(fn, clicks) {
  const states = [];
  let override = [];
  let cur = renderState(fn, override);
  states.push({ ...cur, how: 'rest' });
  for (let c = 0; c < clicks; c += 1) {
    const ctls = cur.controls;
    if (ctls.length === 0) return { states, stop: 'no element carries data-price-expand' };
    const el = ctls[0];
    if (el.type === 'summary' || el.type === 'details') {
      const opened = cur.html.replace(/<details(?![^>]*\sopen=)/g, '<details open=""');
      cur = { html: opened, controls: ctls };
      states.push({ ...cur, how: 'details opened' });
      continue;
    }
    if (typeof el.props.onClick !== 'function') return { states, stop: `the data-price-expand element (<${el.type}>) has no onClick` };
    H.writes = [];
    H.latest = new Map(override);
    el.props.onClick({ preventDefault: noop, stopPropagation: noop, currentTarget: {}, target: {} });
    const writes = H.writes.slice();
    if (writes.length === 0) return { states, stop: 'clicking data-price-expand wrote no state' };
    const m = new Map(override);
    for (const [i, v] of writes) m.set(i, v);
    override = [...m.entries()];
    cur = renderState(fn, override);
    states.push({ ...cur, how: `click ${c + 1}: ${writes.length} state write(s)` });
  }
  return { states, stop: null };
}

module.exports = { L, React, SA, loadFixture, renderLead, clickThrough, renderState, bubbleSeen, both, origCreateElement };
