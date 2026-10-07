/**
 * r77_ba5_harness.cjs -- AMGT_RESAPP round 77, cell AMGT-ba-5 (CTO round-76 ruling 6; rows Z-W266-S2, Z-W266-S3).
 *
 * INSTRUMENT. The ACTUAL `ThesisDriverChart.tsx` and `SegmentBreakdown.tsx` of the portal checkout this runs in,
 * transpiled with the INSTALLED typescript, and walked as a React element tree. `useState` is a slot store this
 * file owns, so a press is a real call of the pressed element's own `onClick` followed by a second walk. recharts
 * is a stub that records each component's props; `@/ui/components/states` is a stub. No browser, no HTTP, no AWS;
 * this script writes no file.
 *
 * FIXTURE. `r77_groupB_fixture.json` beside this file: the DEPLOYED /thesis bytes of four names, captured from
 * opal-amgt-scoped-api (its CodeSha256 is in the fixture).
 *
 * THE CONTRACT THE PAGE KEEPS (the order states it):
 *   - the pressed element carries `data-driver-chart-passage-link` and an `onClick`;
 *   - every OPEN passage block carries `data-driver-chart-passage-source`;
 *   - a served `passage_table` is drawn as `<table data-driver-chart-passage-table>` with one `<th>` per column
 *     label and each row's label in the row;
 *   - the chart's `YAxis` receives a `tickFormatter`;
 *   - each segment heading carries `data-segment-heading`, each row `data-segment-row`.
 *
 *   node r77_ba5_harness.cjs --crit AC1|AC2|AC3
 * Run from the repository root. `R77_PORTAL_SRC` (a directory holding `src/`) and `R77_PORTAL_MODULES` (a
 * directory holding `package.json` + `node_modules`) override the default `<cwd>/portal` for a base dry-run.
 */
const fs = require('fs');
const path = require('path');
const vm = require('vm');
const { createRequire } = require('module');

const args = process.argv.slice(2);
const crit = args[args.indexOf('--crit') + 1];
if (!['AC1', 'AC2', 'AC3'].includes(crit)) {
  console.log('usage: node r77_ba5_harness.cjs --crit AC1|AC2|AC3');
  process.exit(2);
}
const portalDefault = path.resolve(process.cwd(), 'portal');
const srcRoot = path.resolve(process.env.R77_PORTAL_SRC || portalDefault);
const modRoot = path.resolve(process.env.R77_PORTAL_MODULES || portalDefault);
const COMPONENTS = path.join(srcRoot, 'src', 'pages', 'SecurityAnalysis', 'components');

let ok = true;
function clause(name, pass, detail) {
  console.log((pass ? 'PASS ' : 'FAIL ') + name + (detail === undefined ? '' : ' ' + detail));
  if (!pass) ok = false;
}
function verdict() {
  console.log('R77 BA5 ' + crit + ' SERVED: ' + (ok ? 'YES' : 'NO'));
  process.exit(ok ? 0 : 1);
}
function fatal(message) {
  console.log('FAIL the instrument could not run: ' + message);
  ok = false;
  verdict();
}

if (!fs.existsSync(path.join(modRoot, 'package.json')) || !fs.existsSync(path.join(modRoot, 'node_modules'))) {
  fatal('no package.json + node_modules under ' + modRoot);
}
const req = createRequire(path.join(modRoot, 'package.json'));
let ts;
let React;
try {
  ts = req('typescript');
  React = req('react');
} catch (err) {
  fatal('typescript or react is not installed under ' + modRoot + ': ' + err.message);
}

// ---------------------------------------------------------------------------------------------- the slot store
const slots = [];
let cursor = 0;
function useState(initial) {
  const index = cursor++;
  if (!(index in slots)) slots[index] = typeof initial === 'function' ? initial() : initial;
  return [slots[index], (next) => { slots[index] = typeof next === 'function' ? next(slots[index]) : next; }];
}
const fakeReact = Object.assign({}, React, {
  useState,
  useReducer: (reducer, initial) => {
    const [value, set] = useState(initial);
    return [value, (action) => set((prev) => reducer(prev, action))];
  },
  useMemo: (make) => make(),
  useCallback: (fn) => fn,
  useRef: (value) => ({ current: value }),
  useId: () => 'r77-id',
  useEffect: () => undefined,
  useLayoutEffect: () => undefined,
});
fakeReact.default = fakeReact;

// ------------------------------------------------------------------------------------------------- the stubs
const captured = { recharts: {} };
const rechartsStub = new Proxy({}, {
  get: (_target, name) => {
    if (name === '__esModule') return true;
    return function RechartsStub(props) {
      (captured.recharts[String(name)] = captured.recharts[String(name)] || []).push(props);
      return React.createElement('div', { 'data-recharts-stub': String(name) }, props && props.children);
    };
  },
});
const statesStub = {
  PanelEmpty: (props) => React.createElement('div', { 'data-panel-empty': '' }, props.message, props.detail),
};
const nullStub = new Proxy({}, { get: (_t, name) => (name === '__esModule' ? true : () => null) });

const cache = {};
function resolveRelative(fromFile, spec) {
  const baseName = path.resolve(path.dirname(fromFile), spec);
  for (const candidate of [baseName + '.tsx', baseName + '.ts', path.join(baseName, 'index.tsx'), path.join(baseName, 'index.ts')]) {
    if (fs.existsSync(candidate)) return candidate;
  }
  return null;
}
function load(file) {
  if (cache[file]) return cache[file].exports;
  const source = fs.readFileSync(file, 'utf8');
  const out = ts.transpileModule(source, {
    compilerOptions: { module: ts.ModuleKind.CommonJS, jsx: ts.JsxEmit.ReactJSX, target: ts.ScriptTarget.ES2019, esModuleInterop: true },
    fileName: file,
  }).outputText;
  const mod = { exports: {} };
  cache[file] = mod;
  const localRequire = (spec) => {
    if (spec === 'react') return fakeReact;
    if (spec === 'recharts') return rechartsStub;
    if (spec === '@/ui/components/states') return statesStub;
    if (spec.startsWith('@/')) return nullStub;
    if (spec.startsWith('.')) {
      const found = resolveRelative(file, spec);
      return found ? load(found) : nullStub;
    }
    return req(spec);
  };
  vm.runInNewContext(out, { module: mod, exports: mod.exports, require: localRequire, console, process }, { filename: file });
  return mod.exports;
}

// ---------------------------------------------------------------------------------------------- the tree walk
function walk(node, out, inside) {
  if (node === null || node === undefined || typeof node === 'boolean') return;
  if (typeof node === 'string' || typeof node === 'number') {
    out.texts.push({ text: String(node), inside: inside.slice() });
    return;
  }
  if (Array.isArray(node)) {
    node.forEach((child) => walk(child, out, inside));
    return;
  }
  if (typeof node !== 'object' || !node.props) return;
  if (typeof node.type === 'function') {
    walk(node.type(node.props), out, inside);
    return;
  }
  if (typeof node.type === 'string') {
    const host = { type: node.type, props: node.props, texts: [] };
    out.hosts.push(host);
    const nextInside = inside.concat([host]);
    walk(node.props.children, out, nextInside);
    return;
  }
  walk(node.props.children, out, inside); // a fragment or another exotic wrapper
}
function render(Component, props) {
  cursor = 0;
  captured.recharts = {};
  const out = { hosts: [], texts: [] };
  walk(React.createElement(Component, props), out, []);
  for (const entry of out.texts) for (const host of entry.inside) host.texts.push(entry.text);
  return out;
}
function textOf(host) {
  return host.texts.join('').replace(/\s+/g, ' ').trim();
}
function withAttr(tree, attr) {
  return tree.hosts.filter((h) => Object.prototype.hasOwnProperty.call(h.props, attr));
}
function resetState() {
  slots.length = 0;
}

// --------------------------------------------------------------------------------------------------- inputs
const fixture = JSON.parse(fs.readFileSync(path.join(__dirname, 'r77_groupB_fixture.json'), 'utf8'));
const names = fixture.names;
const chartFile = path.join(COMPONENTS, 'ThesisDriverChart.tsx');
const segmentFile = path.join(COMPONENTS, 'SegmentBreakdown.tsx');
console.log('   portal source ' + srcRoot + '; fixture ' + fixture.function_code_sha256.slice(0, 8) + ' captured ' + fixture.captured_at);

function chartProps(key) {
  return { chart: names[key].thesis_driver_chart, driver: names[key].thesis_driver, sections: [] };
}
function loadChart() {
  if (!fs.existsSync(chartFile)) fatal('no ' + chartFile);
  const mod = load(chartFile);
  if (typeof mod.ThesisDriverChart !== 'function') fatal('ThesisDriverChart is not exported by ' + chartFile);
  return mod.ThesisDriverChart;
}
function press(Component, props, index) {
  const before = render(Component, props);
  const links = withAttr(before, 'data-driver-chart-passage-link');
  if (!links[index] || typeof links[index].props.onClick !== 'function') return null;
  links[index].props.onClick({ preventDefault() {}, stopPropagation() {} });
  return render(Component, props);
}

try {
  if (crit === 'AC1') {
    const Chart = loadChart();
    // The specimen: ASML NA's three points share ONE passage id (the deployed bytes).
    const shared = chartProps('ASML_NA_Equity');
    const ids = (shared.chart.points || []).map((p) => p.passage_id);
    console.log('   ASML_NA_Equity: ' + ids.length + ' points, passage ids ' + JSON.stringify(ids));
    resetState();
    const rest = render(Chart, shared);
    const links = withAttr(rest, 'data-driver-chart-passage-link');
    clause('C1 at rest: one link per point and no open passage', links.length === ids.length && withAttr(rest, 'data-driver-chart-passage-source').length === 0,
      'links ' + links.length + ' open ' + withAttr(rest, 'data-driver-chart-passage-source').length);
    const first = press(Chart, shared, 0);
    const open1 = first ? withAttr(first, 'data-driver-chart-passage-source').length : -1;
    clause('C2 one press on the first point opens the passage ONCE where three points share its id', open1 === 1, 'open ' + open1);
    const second = press(Chart, shared, 1);
    const open2 = second ? withAttr(second, 'data-driver-chart-passage-source').length : -1;
    const expanded = second ? withAttr(second, 'data-driver-chart-passage-link').map((h) => h.props['aria-expanded'] === true) : [];
    clause('C3 a press on the second point leaves ONE open passage, and it is the second point', open2 === 1 && expanded[1] === true && expanded.filter(Boolean).length === 1,
      'open ' + open2 + ' expanded ' + JSON.stringify(expanded));
    const third = press(Chart, shared, 1);
    const open3 = third ? withAttr(third, 'data-driver-chart-passage-source').length : -1;
    clause('C4 pressing the open point again closes it', open3 === 0, 'open ' + open3);
    // The control: BA's three points carry three DIFFERENT ids; one press opens one passage there too.
    resetState();
    const control = press(Chart, chartProps('BA_US_Equity'), 0);
    const openControl = control ? withAttr(control, 'data-driver-chart-passage-source').length : -1;
    clause('C5 control, three different ids (BA): one press opens one passage', openControl === 1, 'open ' + openControl);
  } else if (crit === 'AC2') {
    const Chart = loadChart();
    const props = chartProps('BA_US_Equity');
    const table = props.chart.points[0].passage_table;
    console.log('   BA_US_Equity point 1 serves passage_table columns ' + JSON.stringify(table.columns) + ', rows ' + table.rows.map((r) => r.label).join(' | '));
    resetState();
    const opened = press(Chart, props, 0);
    const tables = opened ? withAttr(opened, 'data-driver-chart-passage-table').filter((h) => h.type === 'table') : [];
    clause('C1 a served table passage is drawn as a table', tables.length === 1, 'tables ' + tables.length);
    const heads = opened ? opened.hosts.filter((h) => h.type === 'th').map(textOf) : [];
    const missingColumns = table.columns.filter((c) => !heads.includes(String(c)));
    clause('C2 every served column label is a column header', tables.length === 1 && missingColumns.length === 0, 'missing ' + JSON.stringify(missingColumns));
    const tableText = tables.length ? textOf(tables[0]) : '';
    const missingRows = table.rows.filter((r) => !tableText.includes(r.label)).map((r) => r.label);
    const missingValues = table.rows.flatMap((r) => r.values).filter((v) => !tableText.includes(String(v)));
    clause('C3 every served row label and figure is in the table', tables.length === 1 && missingRows.length === 0 && missingValues.length === 0,
      'rows missing ' + JSON.stringify(missingRows) + ' figures missing ' + missingValues.length);
    const blockText = opened ? withAttr(opened, 'data-driver-chart-passage-source').map(textOf).join(' ') : '';
    clause('C4 the served note about uneven rows is shown when the table carries one', !table.note || blockText.includes(String(table.note).slice(0, 40)), table.note ? 'note served' : 'no note served');
    clause('C5 the cite line is still shown', blockText.includes('From the filing'), '');
    // The control: ASML NA's passage serves NO table; its text is still shown and no table is drawn.
    resetState();
    const flat = press(Chart, chartProps('ASML_NA_Equity'), 0);
    const flatTables = flat ? withAttr(flat, 'data-driver-chart-passage-table').length : -1;
    const flatText = flat ? withAttr(flat, 'data-driver-chart-passage-source').map(textOf).join(' ') : '';
    clause('C6 control, no served table (ASML NA): no table is drawn and the passage text is shown', flatTables === 0 && flatText.includes('393,421,721'), 'tables ' + flatTables);
    // The axis: the y ticks are formatted, short, and exact for a small figure.
    resetState();
    render(Chart, chartProps('ASML_NA_Equity'));
    const axis = (captured.recharts.YAxis || [])[0] || {};
    const format = axis.tickFormatter;
    let big = null;
    let small = null;
    if (typeof format === 'function') {
      big = String(format(393421721, 0));
      small = String(format(528, 0));
    }
    clause('C7 the y axis formats its ticks: a nine-digit figure reads in 7 characters or fewer with no run of zeros', typeof format === 'function' && big.length <= 7 && !/0{5}/.test(big) && /\d/.test(big),
      'tick(393421721) = ' + JSON.stringify(big));
    clause('C8 a small figure is not rounded away', typeof format === 'function' && small.replace(/,/g, '') === '528', 'tick(528) = ' + JSON.stringify(small));
    // A chart the producer refuses serves ABSENT with a `plain_reason`; the page shows that sentence, not its default.
    resetState();
    const plant = 'R77 PLANT this figure counts shares, so no chart is shown.';
    const refused = render(Chart, { chart: { status: 'ABSENT', reason: 'r77 plant system text', plain_reason: plant, points: [], points_count: 0 }, driver: names.ASML_NA_Equity.thesis_driver, sections: [] });
    const refusedText = refused.texts.map((t) => t.text).join(' ');
    clause('C9 an ABSENT chart that serves a plain reason shows that sentence, and not the system text', refusedText.includes(plant) && !refusedText.includes('r77 plant system text'), '');
    resetState();
    const absent = render(Chart, { chart: { status: 'ABSENT', reason: 'r77 plant system text', points: [], points_count: 0 }, driver: names.BABA_US_Equity.thesis_driver, sections: [] });
    const absentText = absent.texts.map((t) => t.text).join(' ').trim();
    clause('C10 control: an ABSENT chart with no plain reason keeps a sentence of its own', absentText.length > 20 && !absentText.includes('r77 plant system text') && !absentText.includes('undefined'), '');
  } else {
    if (!fs.existsSync(segmentFile)) fatal('no ' + segmentFile);
    const mod = load(segmentFile);
    if (typeof mod.SegmentBreakdown !== 'function') fatal('SegmentBreakdown is not exported by ' + segmentFile);
    const grade = (key) => {
      const breakdown = names[key].segment_breakdown;
      const labels = [];
      for (const row of breakdown.rows) if (!labels.includes(row.segment)) labels.push(row.segment);
      resetState();
      const tree = render(mod.SegmentBreakdown, { breakdown });
      const headings = withAttr(tree, 'data-segment-heading').map(textOf);
      const rows = withAttr(tree, 'data-segment-row');
      const exact = labels.map((label) => tree.texts.filter((t) => t.text.trim() === label).length);
      return { labels, headings, rows: rows.length, served: breakdown.rows.length, exact, tree };
    };
    const ba = grade('BA_US_Equity');
    console.log('   BA_US_Equity serves ' + ba.served + ' rows under ' + ba.labels.length + ' labels: ' + ba.labels.join(' | '));
    clause('C1 one heading per segment, in the order the filing first names them', JSON.stringify(ba.headings) === JSON.stringify(ba.labels), 'headings ' + JSON.stringify(ba.headings));
    clause('C2 every served row is still drawn', ba.rows === ba.served, ba.rows + ' of ' + ba.served);
    clause('C3 a segment name stands alone once, as its heading, not on every row', ba.exact.every((n) => n === 1), 'label alone counts ' + JSON.stringify(ba.exact));
    // Rows sit under their own heading: walking the hosts in order, each row follows the heading of its segment.
    let current = null;
    let misplaced = 0;
    let rowIndex = 0;
    const order = names.BA_US_Equity.segment_breakdown.rows.map((r) => r.segment);
    const perLabel = {};
    for (const host of ba.tree.hosts) {
      if (Object.prototype.hasOwnProperty.call(host.props, 'data-segment-heading')) current = textOf(host);
      if (Object.prototype.hasOwnProperty.call(host.props, 'data-segment-row')) {
        perLabel[current] = (perLabel[current] || 0) + 1;
        rowIndex += 1;
      }
    }
    for (const label of ba.labels) if ((perLabel[label] || 0) !== order.filter((s) => s === label).length) misplaced += 1;
    clause('C4 each heading holds exactly its own rows', rowIndex === ba.served && misplaced === 0, JSON.stringify(perLabel));
    const pbr = grade('PBR_US_Equity');
    clause('C5 control, one label on every row (PBR): one heading', pbr.headings.length === 1 && pbr.rows === pbr.served, 'headings ' + pbr.headings.length + ' rows ' + pbr.rows);
    resetState();
    const reason = 'R77 PLANT no segment breakdown is shown for this plant.';
    const empty = render(mod.SegmentBreakdown, { breakdown: { rows: [], reason, source: null } });
    clause('C6 control, no rows: the served reason is still shown and no heading is drawn', empty.texts.some((t) => t.text.includes(reason)) && withAttr(empty, 'data-segment-heading').length === 0, '');
  }
} catch (err) {
  clause('the instrument ran to the end', false, err && err.stack ? String(err.stack).split('\n').slice(0, 3).join(' | ') : String(err));
}
verdict();
