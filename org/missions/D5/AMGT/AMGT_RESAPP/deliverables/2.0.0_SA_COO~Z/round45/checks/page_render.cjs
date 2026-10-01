/**
 * page_render.cjs -- AMGT_RESAPP round 49, AMGT-xx-1. Renders the SecurityAnalysis page from a captured served fixture and
 * prints the HTML of every tab (thesis, model, exec_management, peers, posture) plus each header card's window and each thesis
 * card's window (a static render never opens a window), separated by newlines. It reads NOTHING out of the HTML: the grade's
 * page reader (sweep.py page_facts_from_html) keys on the page's data attributes. The loader (STUBS / SOURCE_STUBS / source /
 * resolveRelative) is exportCompare.harness.cjs's own, copied because that file is another project's and runs its own compare.
 * usage (cwd = portal/):  node <abs path>/page_render.cjs <fixture.json>   -> HTML on stdout
 */
const fs = require('fs');
const path = require('path');
const vm = require('vm');
const crypto = require('crypto');
const { createRequire } = require('module');

const base = process.cwd();
const req = createRequire(path.join(base, 'package.json'));
const ts = req('typescript');
const React = req('react');
const { renderToStaticMarkup } = req('react-dom/server');


const fixturePath = process.argv[2] ? path.resolve(process.cwd(), process.argv[2]) : null;
if (!fixturePath) {
  console.error('usage: node page_render.cjs <fixture.json>   (cwd = portal/)');
  process.exit(2);
}
const fixture = JSON.parse(fs.readFileSync(fixturePath, 'utf8'));

let current = fixture;
let tabState = 'thesis';

const box = ({ children }) => React.createElement('section', null, children);
const nothing = () => null;
const noop = () => {};
const loaded = {};

// ---------------------------------------------------------------------------
// THE LOADER -- copied verbatim (STUBS/SOURCE_STUBS/source/resolveRelative) from
// `tabs.harness.cjs`, this round's own harness (read-only, not this cell's to edit).
// ---------------------------------------------------------------------------
const STUBS = {
  '@/ui/components/panels': { Panel: box, PanelHeader: box, PanelContent: box, PanelFooter: box },
  '@/ui/components/Select': { Select: nothing },
  '@/ui/components/EmptyState': { EmptyState: ({ title }) => React.createElement('div', null, title) },
  '@/ui/components/states': {
    PanelEmpty: ({ message }) => React.createElement('div', { 'data-panel-state': 'empty' }, message),
    PanelLoading: ({ label }) => React.createElement('div', { 'data-panel-state': 'loading' }, label || 'Loading'),
    PanelError: ({ message, cause }) => React.createElement('div', { 'data-panel-state': 'error' }, [message, cause]),
    PanelNoPermission: () => null,
  },
  '@/ui/components/Controls': {
    buttonClass: () => '',
    Segmented: ({ options, value, ariaLabel }) =>
      React.createElement('div', { role: 'group', 'aria-label': ariaLabel, 'data-segmented-value': value },
        (options || []).map((o) => React.createElement('button', { key: String(o.value), type: 'button' }, o.label))),
  },
  '@/components/HelperTip': { HelperTip: ({ children }) => React.createElement('span', null, children) },
  '@/components/DataTooltip': {
    DataTooltip: ({ header, rows }) =>
      React.createElement('div', { 'data-data-tooltip': header }, (rows || []).map((r) => String(r.value)).join(' | ')),
  },
  '@/hooks/useAuth': { useAuth: () => ({ claims: { firmId: 'RL10-EXPORT-COMPARE' } }) },
  '@/lib/utils': { cn: (...xs) => xs.filter(Boolean).join(' ') },
  'react-router-dom': { useParams: () => ({ securityKey: current ? current.security_key : undefined }) },
  '@/contexts/PageThemeContext': { PageThemeProvider: box },
  '@/components/PageHeaderVariants': {
    PageHeaderCleanBadge: ({ title, actions }) => React.createElement('header', { 'data-page-header': title }, actions),
  },
  '@/hooks/useTabNavigation': {
    useTabNavigation: () => ({ activeTab: tabState, handleTabChange: noop, tabContentRef: null }),
  },
  '@/components/TabNavigation': {
    TabNavigation: ({ tabs }) =>
      React.createElement('nav', null, tabs.map((tab) => React.createElement('span', { key: tab.id, 'data-tab-id': tab.id }, tab.label))),
  },
  // AMGT-vv-5: ThesisCards.tsx mounts a HeroDialog (DSGN_AMGTV1), which imports `@/ui/components/graphic/HeroGraphic`
  // (no `@/` mapping here). A closed dialog (openId null) renders nothing, so a null stub drops nothing the page shows.
  '@/ui/components/graphic/HeroGraphic': { HeroDialog: nothing, DialogStamp: nothing },
  recharts: {
    ResponsiveContainer: box, LineChart: box, Line: nothing, XAxis: nothing, YAxis: nothing,
    CartesianGrid: nothing, Tooltip: nothing, Legend: nothing,
  },
};

const SOURCE_STUBS = {
  'src/pages/SecurityAnalysis/hooks/useLeadPanelApi.ts': {
    useThesisBundle: () => ({ data: current ? current.thesis : undefined, isLoading: false }),
    usePeerSet: () => ({ data: current ? current.peers : undefined, isLoading: false }),
    useSecurityOverlay: () => ({ data: current ? current.overlay : undefined, isLoading: false }),
    useCoverageSet: () => ({ data: undefined, isLoading: false }),
    useLeadPanelRankings: () => ({ data: undefined, isLoading: false, isError: false }),
    useRankTimeSeries: () => ({}),
    useStarredList: () => ({ data: [], isLoading: false, isError: false }),
    useSetStarred: () => ({ mutate: noop }),
    useRequestRefresh: () => ({ mutate: noop, isPending: false }),
    // round 52 close: DSGN_AMGTV1 round 12 (portal DEV 2c01af6a) mounts the versions / ledger / compare surfaces; the captured served
    // fixture carries none of them, so they render their empty state -- the export carries no line for them either
    useModelVersions: () => ({ data: undefined, isLoading: false, isError: false }),
    useInputLedger: () => ({ data: undefined, isLoading: false, isError: false }),
    useModelCompare: () => ({ data: undefined, isLoading: false, isError: false }),
  },
  // AMGT-uu-2: HeaderBrief.tsx mounts TimelinePanel (HVST-y-3), which imports `@/api/api-client`
  // (no `@/` mapping in this loader). CHOSEN: a SOURCE_STUB that renders nothing, not an `@/`->src
  // resolver -- the timeline is not part of the export, so the panel must add nothing to
  // FIGURES/CITES/ABSENCES/CASES; a real render would only add page text no export line carries.
  'src/pages/SecurityAnalysis/components/TimelinePanel.tsx': {
    TimelinePanel: nothing,
  },
  'src/pages/SecurityAnalysis/components/PrintExportAction.tsx': {
    PrintExportAction: () => React.createElement('button', { 'data-print-action': 'header' }, 'Print'),
  },
};

function resolveRelative(fromRel, name) {
  const joined = path.posix.normalize(path.posix.join(path.posix.dirname(fromRel), name));
  for (const candidate of [joined + '.tsx', joined + '.ts', joined]) {
    if (fs.existsSync(path.join(base, candidate)) && fs.statSync(path.join(base, candidate)).isFile()) return candidate;
  }
  throw new Error(`cannot resolve ${name} from ${fromRel}`);
}

function source(rel) {
  if (loaded[rel]) return loaded[rel];
  const file = path.join(base, rel);
  const bytes = fs.readFileSync(file);
  const js = ts.transpileModule(bytes.toString('utf8'), {
    compilerOptions: { module: ts.ModuleKind.CommonJS, jsx: ts.JsxEmit.ReactJSX, target: ts.ScriptTarget.ES2022 },
  }).outputText;
  const mod = { exports: {} };
  loaded[rel] = mod.exports;
  function load(name) {
    if (Object.prototype.hasOwnProperty.call(STUBS, name)) return STUBS[name];
    if (name.startsWith('.')) {
      const target = resolveRelative(rel, name);
      if (SOURCE_STUBS[target]) return SOURCE_STUBS[target];
      return source(target);
    }
    return req(name);
  }
  vm.runInThisContext('(function(require,module,exports){' + js + '\n})', { filename: file })(load, mod, mod.exports);
  loaded[rel] = mod.exports;
  return mod.exports;
}

const { SecurityAnalysis } = source('src/pages/SecurityAnalysis/SecurityAnalysis.tsx');
function renderPage(tab) {
  tabState = tab;
  return renderToStaticMarkup(React.createElement(SecurityAnalysis));
}

const parts = ['thesis', 'model', 'exec_management', 'peers', 'posture'].map(renderPage);
// each header card's window (HeaderCardDetail) and each thesis card's window (ThesisCardDetail), off the SAME payloads the
// page rendered from -- exportCompare.harness.cjs does the same (AMGT-vv-5, AV-r-3).
const { HeaderCardDetail } = source('src/pages/SecurityAnalysis/components/HeaderCards.tsx');
const { HEADER_CARD_DEFS } = source('src/pages/SecurityAnalysis/constants.ts');
if (current && current.overlay) {
  for (const c of HEADER_CARD_DEFS) {
    parts.push(renderToStaticMarkup(React.createElement(HeaderCardDetail, { cardKey: c.key, bundle: current.overlay })));
  }
}
const { ThesisCardDetail } = source('src/pages/SecurityAnalysis/components/ThesisCards.tsx');
if (current && current.thesis) {
  for (const id of ['investment_thesis', 'risks', 'recommendation']) {
    parts.push(renderToStaticMarkup(React.createElement(ThesisCardDetail, { sectionId: id, bundle: current.thesis })));
  }
}
process.stdout.write(parts.join(String.fromCharCode(10)));
