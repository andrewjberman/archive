/**
 * pricebars.cjs -- DSGN_AMGTV1 round 15, AV-n-1: PRICE IS RANKED BARS, ONE FORM (FWD-22; CONTRACT s.2; rulings: Trending
 * only through the demo, price ONLY horizontal bars, the List view / line chart / List-Chart toggle removed).
 *
 * Usage (repo root): node <this file>          (portal/ under the cwd is the checkout under test)
 *        node <this file> --grade-only     (internal: prints "GRADE-JSON {...}" for arm 1's predicates and exits; arm 2
 *                                           runs it with the cwd at the extracted base tree)
 *
 * THE ATTRIBUTE CONTRACT the worker builds to (quote it in the task order):
 *   - LeadPanel (components/LeadPanel.tsx, export `LeadPanel`) on subject PRICE renders ONE element per served row carrying
 *     data-price-bar="<row.security_key>" (the row's `ticker` when `security_key` is null). That element is the bar's ROW
 *     (a wrapper, not a void <rect/>): its visible text holds the bar's label and its printed value.
 *   - DOM order of the data-price-bar elements is descending by ABSOLUTE `return_30d_pct` (CONTRACT s.2: "sorts descending
 *     by its absolute value, longest bar first, sign shown by colour").
 *   - Each bar's visible text holds EXACTLY ONE percent token, the served `return_30d_pct` as served: an explicit sign
 *     ("+" for a positive, "-" or U+2212 for a negative), the served number (any trailing-zero form that parses to the
 *     served value, e.g. "-5.0%" or "-5%" for -5.0), then "%". Never x100, never unsigned.
 *   - Each bar's visible text holds the served company `name`, or the `ticker` when the name is not served.
 *   - The panel renders NO recharts LineChart/Line, no RankedChart marker (data-rank-legend / data-series-ticker), no element
 *     with aria-label "List view" / "Chart view" / "View" (the List-Chart toggle), no control with aria-label "Movement"
 *     (Trending only through the demo), and no RankedList table marker (data-list-columns / data-row-lead /
 *     data-list-unserved-columns).
 *
 * Inputs: round15/fixtures/r15a.rankings.TRENDING_PRICE.return30d.json -- the served TRENDING_PRICE payload (round-7 capture,
 * 32 rows, served signed order) with `return_30d_pct` added to every row (CONTRACT s.2 shape; 9 positive, 23 negative; the
 * largest absolute value is a negative, INTU -25.0, served LAST, so the served order is not the graded order).
 * Render method: round15/checks/_load.cjs (static react-dom/server over the real page source, estate chrome stubbed), with
 * three more stubs set here: lucide-react icons render <svg data-icon aria-label>, @/ui/components/Controls' Segmented
 * renders <div role="group" aria-label=<ariaLabel>> with one button per option, and useAuth returns a firm. Hooks: the
 * rankings hook returns the fixture for PRICE; every other hook returns no data.
 * Arms:
 *   1  LeadPanel (movement TRENDING, subject PRICE, starredOnly false, view 'list' passed for compile-compat) on the fixture
 *      meets every clause of the attribute contract above.
 *   2  NEGATIVE: arm 1's predicates on the BASE page source (portal b336b141) FAIL, with "no bars" among the reasons. The base
 *      tree (portal/src + package.json at the pin) is extracted with `git -C portal ls-tree` + `git cat-file --batch` into
 *      os.tmpdir()/dsgn-r15-base-b336b141 (cached; node_modules is a junction to <cwd>/portal/node_modules) and graded by
 *      this file's --grade-only child with that directory as its cwd.
 *   3  PLANTED controls: a reference bar markup built here from the fixture passes every arm-1 predicate; six mutants are each
 *      rejected for their named class -- two bars swapped (ORDER), one value x100 (VALUE), a positive printed unsigned
 *      (VALUE), a label dropped (LABEL), a recharts LineChart planted (LINE), a Movement control planted (MOVEMENT).
 * Blind spots: the hook is stubbed, so the READ is not graded -- a page whose rankings read keeps the list Limit
 * (constants LEAD_PANEL_LIST_TOP_N = 10, signed served order) would show only the ten biggest RISERS on the live route
 * while passing here; bar LENGTH and colour are not measured (a static render does not lay out); the toggle/Movement
 * census sees only aria-labels, so an unlabelled hand-built toggle passes.
 * Writes only under os.tmpdir(). No network, no AWS.
 * Wall time measured on site Z (2026-10-01): base run 2.7 s with a cold base extract (2.3 s of it), 1.0 s cached; green
 * run 1.0 s.
 * Prints one line per arm and "PRICE IS RANKED BARS, ONE FORM: <k> of 3 arms"; exit 0 only at 3 of 3.
 */
const fs = require('fs');
const os = require('os');
const path = require('path');
const { spawnSync } = require('child_process');

const T0 = Date.now();
const ROOT = process.cwd();
const PIN = 'b336b141';
const LP_PATH = 'src/pages/SecurityAnalysis/components/LeadPanel.tsx';
const FIXTURE = 'r15a.rankings.TRENDING_PRICE.return30d.json';

function readFixture(name) {
  const own = path.join(__dirname, '..', 'fixtures', name);
  const r14 = path.join(__dirname, '..', '..', 'round14', 'fixtures', name);
  const x = JSON.parse(fs.readFileSync(fs.existsSync(own) ? own : r14, 'utf8'));
  return x && x.payload && x._capture_note ? x.payload : x;
}
const esc = (s) => String(s).replace(/&/g, '&amp;').replace(/"/g, '&quot;').replace(/'/g, '&#x27;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
const unesc = (s) => String(s).replace(/&quot;/g, '"').replace(/&#x27;/g, "'").replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&amp;/g, '&');
const keyOf = (r) => (r.security_key === null || r.security_key === undefined ? r.ticker : r.security_key);
const count = (html, re) => (html.match(re) || []).length;

const priceSet = readFixture(FIXTURE);
const ROWS = priceSet.rows;

// ---------------- the predicates (pure over html; shared by arms 1, 2 and 3) ----------------
const textOf = (html) =>
  html.replace(/<[^>]*>/g, ' ').replace(/&amp;/g, '&').replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&quot;/g, '"').replace(/&#x27;/g, "'").replace(/\s+/g, ' ').trim();
function innerOf(html, attr, value) {
  const needle = attr + '="' + value + '"';
  const at = html.indexOf(needle);
  if (at < 0) return null;
  const open = html.lastIndexOf('<', at);
  const tag = /^<([a-zA-Z0-9]+)/.exec(html.slice(open))[1];
  const start = html.indexOf('>', at) + 1;
  if (html[start - 2] === '/') return '';
  let depth = 1;
  const re = new RegExp('<(/?)' + tag + '\\b[^>]*?(/?)>', 'g');
  re.lastIndex = start;
  let m;
  while ((m = re.exec(html)) !== null) {
    if (m[2] === '/') continue;
    depth += m[1] === '/' ? -1 : 1;
    if (depth === 0) return html.slice(start, m.index);
  }
  return html.slice(start);
}

function oneFormFaults(html) {
  const f = [];
  const lines = count(html, /data-stub="(?:LineChart|Line)"/g) + count(html, /data-(?:rank-legend|series-ticker)\b/g);
  if (lines) f.push(`LINE: ${lines} line-chart element(s) (recharts LineChart/Line or a RankedChart marker)`);
  const toggles = count(html, /aria-label="(?:List view|Chart view|View)"/g);
  if (toggles) f.push(`TOGGLE: ${toggles} List/Chart view toggle element(s)`);
  const movement = count(html, /aria-label="Movement"/g);
  if (movement) f.push(`MOVEMENT: ${movement} Movement control(s)`);
  const list = count(html, /data-(?:list-columns|row-lead|list-unserved-columns)\b/g);
  if (list) f.push(`LIST: ${list} RankedList table marker(s)`);
  return f;
}

function priceFaults(html, rows) {
  const f = [];
  const byKey = new Map(rows.map((r) => [keyOf(r), r]));
  const bars = [];
  const re = /data-price-bar="([^"]*)"/g;
  let m;
  while ((m = re.exec(html)) !== null) bars.push(unesc(m[1]));
  if (bars.length !== rows.length) f.push(`COUNT: ${bars.length} bars for ${rows.length} served rows`);
  const dup = bars.filter((k, i) => bars.indexOf(k) !== i);
  if (dup.length) f.push(`COUNT: duplicate bars ${dup.slice(0, 3).join(', ')}`);
  const unknown = bars.filter((k) => !byKey.has(k));
  if (unknown.length) f.push(`COUNT: bars for keys the payload does not serve: ${unknown.slice(0, 3).join(', ')}`);
  const missing = rows.map(keyOf).filter((k) => !bars.includes(k));
  if (missing.length) f.push(`COUNT: no bar for ${missing.length} served row(s), first ${missing.slice(0, 3).join(', ')}`);
  const seq = bars.filter((k, i) => byKey.has(k) && bars.indexOf(k) === i);
  for (let i = 1; i < seq.length; i += 1) {
    const a = Math.abs(byKey.get(seq[i - 1]).return_30d_pct);
    const b = Math.abs(byKey.get(seq[i]).return_30d_pct);
    if (b > a) {
      f.push(`ORDER: bar ${i + 1} ${seq[i]} (|${b}|) sits below bar ${i} ${seq[i - 1]} (|${a}|) -- not descending by absolute return`);
      break;
    }
  }
  let valueFaults = 0;
  let labelFaults = 0;
  for (const k of seq) {
    const r = byKey.get(k);
    const text = textOf(innerOf(html, 'data-price-bar', esc(k)) || '');
    const toks = [...text.matchAll(/([+\-\u2212]?)\s?(\d+(?:\.\d+)?)\s?%/g)];
    const v = r.return_30d_pct;
    if (toks.length !== 1) {
      if (valueFaults++ < 2) f.push(`VALUE: bar ${k} prints ${toks.length} percent tokens ("${text.slice(0, 80)}")`);
    } else {
      const [tok, sign, num] = toks[0];
      const printed = sign === '' ? NaN : (sign === '+' ? 1 : -1) * Number(num);
      if (!(Math.abs(printed - v) < 1e-9) && valueFaults++ < 2) f.push(`VALUE: bar ${k} prints "${tok}" for served ${v}`);
    }
    const labelled = (r.name && text.includes(r.name)) || (r.ticker && text.includes(r.ticker));
    if (!labelled && labelFaults++ < 2) f.push(`LABEL: bar ${k} shows neither the served name nor the ticker ("${text.slice(0, 80)}")`);
  }
  if (valueFaults > 2) f.push(`VALUE: ${valueFaults} bars in all print a value not as served`);
  if (labelFaults > 2) f.push(`LABEL: ${labelFaults} bars in all carry no name or ticker`);
  return { faults: f, bars: seq.length };
}

// ---------------- the render (arm 1, and arm 2's child) ----------------
function renderLeadPrice() {
  const L = require('./_load.cjs');
  const React = L.React;
  const icons = {};
  L.stubSource('lucide-react', new Proxy({}, {
    get(_t, key) {
      if (key === '__esModule') return true;
      if (typeof key !== 'string') return undefined;
      if (!icons[key]) { icons[key] = (p) => React.createElement('svg', { 'data-icon': key, 'aria-label': (p || {})['aria-label'] }); icons[key].displayName = key; }
      return icons[key];
    },
  }));
  const ctl = {};
  const Segmented = (p) => React.createElement('div', { role: 'group', 'data-segmented': '', 'aria-label': p.ariaLabel },
    ...(p.options || []).map((o, i) => React.createElement('button', { key: i, type: 'button', 'data-segment-value': String(o.value) }, o.label)));
  const controls = new Proxy({}, {
    get(_t, key) {
      if (key === '__esModule') return true;
      if (typeof key !== 'string') return undefined;
      if (key === 'Segmented') return Segmented;
      if (!ctl[key]) ctl[key] = (p) => React.createElement('div', { 'data-stub': key, 'aria-label': (p || {}).ariaLabel }, (p || {}).children);
      return ctl[key];
    },
  });
  for (const k of ['src/ui/components/Controls', 'src/ui/components/Controls.tsx', 'src/ui/components/Controls.ts']) L.stubSource(k, controls);
  // The loader's generic stub drops PanelHeader's `actions` slot, where the controls live: render every node slot.
  const pan = {};
  const panels = new Proxy({}, {
    get(_t, key) {
      if (key === '__esModule') return true;
      if (typeof key !== 'string') return undefined;
      if (!pan[key]) {
        pan[key] = (p) => {
          const q = p || {};
          const kids = [];
          for (const s of ['title', 'subtitle', 'eyebrow']) if (typeof q[s] === 'string' && q[s]) kids.push(React.createElement('span', { key: s, 'data-stub-text': s }, q[s]));
          for (const s of ['actions', 'leftContent', 'children', 'footer']) if (q[s] !== undefined && q[s] !== null) kids.push(React.createElement(React.Fragment, { key: s }, q[s]));
          return React.createElement('div', { 'data-stub': key }, ...kids);
        };
      }
      return pan[key];
    },
  });
  for (const k of ['src/ui/components/panels', 'src/ui/components/panels/index.ts', 'src/ui/components/panels/index.tsx']) L.stubSource(k, panels);
  for (const k of ['src/hooks/useAuth', 'src/hooks/useAuth.ts', 'src/hooks/useAuth.tsx']) L.stubSource(k, { useAuth: () => ({ claims: { firmId: 'opal' } }) });
  L.hookState.impl = {
    useLeadPanelRankings: (_movement, subject) => (String(subject).toUpperCase() === 'PRICE' ? priceSet : undefined),
    useRankTimeSeries: () => undefined,
    useStarredList: () => [],
    useSetStarred: () => undefined,
  };
  L.hookState.data = undefined;
  const noop = () => {};
  const { LeadPanel } = L.source(LP_PATH);
  return L.render(LeadPanel, {
    movement: 'TRENDING', setMovement: noop, subject: 'PRICE', setSubject: noop, starredOnly: false, setStarredOnly: noop,
    view: 'list', setView: noop, selectedSecurityKey: null, onSelectSecurity: noop, onClearSecuritySelection: noop,
    searchInput: '', setSearchInput: noop,
  });
}

function gradeCheckout() {
  let html = '';
  try {
    html = renderLeadPrice();
  } catch (e) {
    return { faults: ['RENDER: LeadPanel on PRICE threw: ' + String(e.message).split('\n')[0]], bars: 0, html: '' };
  }
  const p = priceFaults(html, ROWS);
  return { faults: [...p.faults, ...oneFormFaults(html)], bars: p.bars, html };
}

if (process.argv.includes('--grade-only')) {
  const g = gradeCheckout();
  console.log('GRADE-JSON ' + JSON.stringify({ faults: g.faults, bars: g.bars }));
  process.exit(0);
}

// ---------------- arm 1 ----------------
const g1 = gradeCheckout();
const a1 = g1.faults.length === 0;
const pos = ROWS.filter((r) => r.return_30d_pct > 0).length;
const a1d = a1
  ? `${g1.bars} bars in descending |return| order (first ${keyOf([...ROWS].sort((a, b) => Math.abs(b.return_30d_pct) - Math.abs(a.return_30d_pct))[0])}), ${ROWS.length} of ${ROWS.length} values signed and as served (${pos} +, ${ROWS.length - pos} -), every bar labelled; 0 line chart, 0 view toggle, 0 Movement control, 0 list table`
  : `${g1.faults.length} faults; ${g1.faults.slice(0, 3).join(' | ')}`;

// ---------------- arm 2: the base tree, graded by this file's child ----------------
function prepareBase() {
  const dir = path.join(os.tmpdir(), `dsgn-r15-base-${PIN}`);
  if (fs.existsSync(path.join(dir, '.complete'))) return { dir, fresh: false };
  const portalGit = path.join(ROOT, 'portal');
  const ls = spawnSync('git', ['-C', portalGit, 'ls-tree', '-r', '-z', PIN, '--', 'src', 'package.json'], { encoding: 'utf8', maxBuffer: 64 << 20 });
  if (ls.status !== 0) throw new Error(`git ls-tree ${PIN} rc=${ls.status}: ${String(ls.stderr).trim()}`);
  const entries = ls.stdout.split('\0').filter(Boolean).map((line) => {
    const tab = line.indexOf('\t');
    const [mode, type, sha] = line.slice(0, tab).split(' ');
    return { mode, type, sha, p: line.slice(tab + 1) };
  }).filter((e) => e.type === 'blob' && e.mode !== '120000');
  if (!entries.some((e) => e.p === LP_PATH)) throw new Error(`${LP_PATH} is not in ${PIN}`);
  const cat = spawnSync('git', ['-C', portalGit, 'cat-file', '--batch'], { input: entries.map((e) => e.sha).join('\n') + '\n', maxBuffer: 512 << 20 });
  if (cat.status !== 0) throw new Error(`git cat-file rc=${cat.status}`);
  const stage = fs.mkdtempSync(path.join(os.tmpdir(), `dsgn-r15-base-${PIN}-stage-`));
  const buf = cat.stdout;
  let off = 0;
  for (const e of entries) {
    const nl = buf.indexOf(10, off);
    const header = buf.slice(off, nl).toString();
    if (/ missing$/.test(header)) throw new Error('object missing: ' + header);
    const size = Number(header.split(' ')[2]);
    const out = path.join(stage, 'portal', e.p);
    fs.mkdirSync(path.dirname(out), { recursive: true });
    fs.writeFileSync(out, buf.slice(nl + 1, nl + 1 + size));
    off = nl + 1 + size + 1;
  }
  fs.symlinkSync(fs.realpathSync(path.join(portalGit, 'node_modules')), path.join(stage, 'portal', 'node_modules'), 'junction');
  fs.writeFileSync(path.join(stage, '.complete'), `portal ${PIN}: ${entries.length} files (src + package.json)\n`);
  try {
    fs.renameSync(stage, dir);
  } catch (e) {
    if (!fs.existsSync(path.join(dir, '.complete'))) throw e; // another check built it first: use theirs
  }
  return { dir, fresh: true };
}
const f2 = [];
let a2d = '';
try {
  const t = Date.now();
  const { dir, fresh } = prepareBase();
  const env = { ...process.env };
  delete env.CHECK_SRC_OVERRIDE;
  const r = spawnSync(process.execPath, [__filename, '--grade-only'], { cwd: dir, encoding: 'utf8', env, timeout: 120000 });
  const line = (r.stdout || '').split(/\r?\n/).find((x) => x.startsWith('GRADE-JSON '));
  if (!line) f2.push(`the base child printed no grade (rc=${r.status}): ${String(r.stderr || r.stdout).trim().split('\n').slice(-1)[0]}`);
  else {
    const g = JSON.parse(line.slice('GRADE-JSON '.length));
    const classes = {};
    for (const x of g.faults) { const c = x.split(':')[0]; classes[c] = (classes[c] || 0) + 1; }
    if (g.faults.length === 0) f2.push('the base page source PASSES arm 1 -- the predicates do not see the defect');
    else if (!g.faults.some((x) => /^COUNT: 0 bars/.test(x)) && !g.faults.some((x) => /^RENDER:/.test(x))) f2.push(`the base fails, but not on "no bars": ${g.faults[0]}`);
    a2d = `base portal ${PIN} (${fresh ? 'extracted' : 'cached'} at ${dir}, ${((Date.now() - t) / 1000).toFixed(1)}s): ${g.faults.length} faults by class ${JSON.stringify(classes)}; first: ${g.faults.slice(0, 4).join(' | ')}`;
  }
} catch (e) {
  f2.push('base extract/grade failed: ' + String(e.message).split('\n')[0]);
}
const a2 = f2.length === 0;
if (!a2) a2d = `${f2[0]}${a2d ? ' || ' + a2d : ''}`;

// ---------------- arm 3: planted controls ----------------
const sorted = [...ROWS].sort((a, b) => Math.abs(b.return_30d_pct) - Math.abs(a.return_30d_pct));
const fmt = (v) => `${v > 0 ? '+' : '-'}${Math.abs(v)}%`;
function synth(rows, mut) {
  const rs = rows.map((r) => ({ key: keyOf(r), label: r.name || r.ticker, value: fmt(r.return_30d_pct) }));
  if (mut === 'swap') [rs[1], rs[4]] = [rs[4], rs[1]];
  if (mut === 'x100') { const r = rows[2]; rs[2].value = fmt(r.return_30d_pct * 100); }
  if (mut === 'unsigned') { const i = rows.findIndex((r) => r.return_30d_pct > 0); rs[i].value = `${rows[i].return_30d_pct}%`; }
  if (mut === 'nolabel') rs[3].label = '';
  let html = '<div data-stub="Panel"><ol>' + rs.map((r) => `<li data-price-bar="${esc(r.key)}"><span>${esc(r.label)}</span><div style="width:50%"></div><span>${esc(r.value)}</span></li>`).join('') + '</ol>';
  if (mut === 'line') html += '<div data-stub="LineChart"><div data-stub="Line"></div></div>';
  if (mut === 'movement') html += '<div role="group" aria-label="Movement"><button>Trending</button><button>Breakout</button></div>';
  return html + '</div>';
}
const grade3 = (html) => [...priceFaults(html, ROWS).faults, ...oneFormFaults(html)];
const f3 = [];
const ctl3 = grade3(synth(sorted));
if (ctl3.length) f3.push(`the reference markup fails: ${ctl3[0]}`);
const MUTANTS = [['swap', 'ORDER'], ['x100', 'VALUE'], ['unsigned', 'VALUE'], ['nolabel', 'LABEL'], ['line', 'LINE'], ['movement', 'MOVEMENT']];
const caught = [];
for (const [mut, cls] of MUTANTS) {
  const fx = grade3(synth(sorted, mut));
  if (fx.some((x) => x.startsWith(cls + ':'))) caught.push(`${mut}->${cls}`);
  else f3.push(`mutant ${mut} not rejected as ${cls} (faults: ${fx.slice(0, 2).join(' | ') || 'none'})`);
}
const a3 = f3.length === 0;
const a3d = a3
  ? `reference markup 0 faults; ${caught.length} of ${MUTANTS.length} mutants rejected (${caught.join(', ')})`
  : `${f3.length} failing; first: ${f3[0]}`;

const arms = [
  ['LeadPanel on PRICE: one bar per row, |return| order, values as served with sign, labelled, one form', a1, a1d],
  [`NEGATIVE: the base page source (portal ${PIN}) fails arm 1 on "no bars"`, a2, a2d],
  ['PLANTED controls: the reference passes; swap, x100, unsigned, no label, line chart and Movement are each rejected', a3, a3d],
];
let pass = 0;
for (const [name, ok, detail] of arms) { if (ok) pass += 1; console.log(`${ok ? 'ARM PASS' : 'ARM FAIL'} ${name} :: ${detail}`); }
console.log(`WALL: ${((Date.now() - T0) / 1000).toFixed(1)}s`);
console.log(`PRICE IS RANKED BARS, ONE FORM: ${pass} of ${arms.length} arms`);
process.exit(pass === arms.length ? 0 : 1);
