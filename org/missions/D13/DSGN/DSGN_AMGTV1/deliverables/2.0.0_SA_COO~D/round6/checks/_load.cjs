/**
 * _load.cjs -- DSGN_AMGTV1 round-6 check loader (a copy of round 5's, which stays frozen with its round) (issuer 2.0.0_SA_COO~D).
 *
 * Renders the REAL page sources under portal/src/pages/SecurityAnalysis with the INSTALLED
 * typescript and react-dom/server, the same method as the page's own __harness__ files.
 * Shared estate chrome (src/ui/**, src/components/**) and the chart/icon/dialog packages are
 * STUBBED: a stub renders its children, and a stub whose export name contains "Dialog" renders
 * its children ONLY when its `open` prop is truthy -- so a face render never contains a closed
 * dialog's body. The page's own hooks are stubbed to return the fixture the check sets.
 *
 * Paths resolve from the working directory: run every check from the repository root
 * (`cd "$(git rev-parse --show-toplevel)"`), whose `portal/` is the portal checkout under test.
 * No network, no AWS, writes no file.
 */
const fs = require('fs');
const path = require('path');
const vm = require('vm');
const { createRequire } = require('module');

const root = process.cwd();
const base = path.join(root, 'portal');
if (!fs.existsSync(path.join(base, 'package.json'))) {
  console.log('LOADER ERROR: no portal/package.json under ' + root + ' -- run from the repository root');
  process.exit(3);
}
const req = createRequire(path.join(base, 'package.json'));
const ts = req('typescript');
const React = req('react');
const { renderToStaticMarkup } = req('react-dom/server');

const FIXTURES = path.join(root, 'org/missions/D13/DSGN/DSGN_AMGTV1/deliverables/2.0.0_SA_COO~D/round6/fixtures');
function fixture(name) {
  return JSON.parse(fs.readFileSync(path.join(FIXTURES, name), 'utf8'));
}

function stubComponent(name) {
  const isDialog = /Dialog/.test(name);
  const C = (props) => {
    const p = props || {};
    if (isDialog && !p.open) return null;
    const attrs = { 'data-stub': name };
    if (typeof p.title === 'string') attrs['data-stub-title'] = p.title;
    if (typeof p.eyebrow === 'string') attrs['data-stub-eyebrow'] = p.eyebrow;
    const kids = [];
    // Round 2: a stub prints the TEXT props an estate state/panel shows on screen (PanelEmpty/PanelError message, detail,
    // hint, cause; a header's title/subtitle), so a raw-code census sees what a PM would read.
    for (const k of ['title', 'subtitle', 'message', 'detail', 'hint', 'cause', 'label']) {
      if (typeof p[k] === 'string' && p[k]) kids.push(React.createElement('span', { key: 'stub-' + k, 'data-stub-text': k }, p[k]));
    }
    if (p.children !== undefined) kids.push(p.children);
    if (p.footer !== undefined && p.footer !== null && typeof p.footer === 'object') kids.push(p.footer);
    return React.createElement('div', attrs, ...kids);
  };
  C.displayName = name;
  return C;
}
function proxyModule(label) {
  const cache = {};
  return new Proxy(
    {},
    {
      get(_t, key) {
        if (key === '__esModule') return true;
        if (typeof key !== 'string') return undefined;
        if (key === 'cn') return (...xs) => xs.filter(Boolean).join(' ');
        if (key === 'buttonClass') return () => '';
        if (!cache[key]) cache[key] = stubComponent(key);
        return cache[key];
      },
    }
  );
}

const PROXY_PACKAGES = new Set([
  'lucide-react', 'recharts', '@headlessui/react', '@visx/wordcloud', '@tanstack/react-query', 'framer-motion',
  'react-router-dom',
]);

const hookState = { data: undefined, isLoading: false, error: null, impl: null };
function hookModule() {
  return new Proxy(
    {},
    {
      get(_t, key) {
        if (key === '__esModule') return true;
        if (typeof key !== 'string') return undefined;
        // Per-hook fixtures: hookState.impl[name](...args) -> data; otherwise the one shared fixture.
        if (hookState.impl && typeof hookState.impl[key] === 'function') {
          return (...args) => ({ data: hookState.impl[key](...args), isLoading: false, isError: false, error: null, refetch: () => {} });
        }
        return () => ({ data: hookState.data, isLoading: hookState.isLoading, error: hookState.error, refetch: () => {} });
      },
    }
  );
}

const STUB_PREFIXES = ['src/ui/', 'src/components/'];
const extraStubs = {};
const loaded = {};

function resolveModule(fromRel, name) {
  let t;
  if (name.startsWith('@/')) t = 'src/' + name.slice(2);
  else if (name.startsWith('.')) t = path.posix.normalize(path.posix.join(path.posix.dirname(fromRel), name));
  else return null;
  for (const c of [t, t + '.tsx', t + '.ts', t + '/index.tsx', t + '/index.ts']) {
    if (overrides[c]) return c;
    const f = path.join(base, c);
    if (fs.existsSync(f) && fs.statSync(f).isFile()) return c;
  }
  return t; // unresolved: stubbed below if under a stub prefix, else an error
}

// ISSUER GREEN ARM ONLY: CHECK_SRC_OVERRIDE="<portal-relative path>=<absolute file>" loads a
// scratch reference implementation in place of one source, to prove a check CAN pass. A worker
// never sets it; the proof-of-spec invocations do not.
const overrides = {};
for (const pair of (process.env.CHECK_SRC_OVERRIDE || '').split(';').filter(Boolean)) {
  const i = pair.indexOf('=');
  overrides[pair.slice(0, i)] = pair.slice(i + 1);
}

function source(rel) {
  if (loaded[rel]) return loaded[rel];
  const file = overrides[rel] || path.join(base, rel);
  const text = fs.readFileSync(file, 'utf8');
  const js = ts.transpileModule(text, {
    compilerOptions: { module: ts.ModuleKind.CommonJS, jsx: ts.JsxEmit.ReactJSX, target: ts.ScriptTarget.ES2022, esModuleInterop: true },
  }).outputText;
  const mod = { exports: {} };
  loaded[rel] = mod.exports;
  function load(name) {
    if (name === 'react' || name === 'react/jsx-runtime' || name === 'react-dom') return req(name);
    // round 4: a check may replace a whole PACKAGE (history.cjs serialises recharts props into attributes).
    if (extraStubs[name]) return extraStubs[name];
    if (PROXY_PACKAGES.has(name)) return proxyModule(name);
    const target = resolveModule(rel, name);
    if (target === null) return req(name);
    if (extraStubs[target]) return extraStubs[target];
    if (target.startsWith('src/pages/SecurityAnalysis/hooks/')) return hookModule();
    if (STUB_PREFIXES.some((p) => target.startsWith(p))) return proxyModule(target);
    if (!overrides[target] && !fs.existsSync(path.join(base, target))) throw new Error('cannot resolve ' + name + ' from ' + rel);
    return source(target);
  }
  vm.runInThisContext('(function(require,module,exports){' + js + '\n})', { filename: file })(load, mod, mod.exports);
  loaded[rel] = mod.exports;
  return mod.exports;
}

function stubSource(rel, exportsObj) {
  extraStubs[rel] = exportsObj;
}

function render(Component, props) {
  return renderToStaticMarkup(React.createElement(Component, props || {}));
}

/** Visible text: tags stripped, entities decoded, attributes gone. */
function textOf(html) {
  return html
    .replace(/<[^>]*>/g, ' ')
    .replace(/&amp;/g, '&')
    .replace(/&lt;/g, '<')
    .replace(/&gt;/g, '>')
    .replace(/&quot;/g, '"')
    .replace(/&#x27;/g, "'")
    .replace(/\s+/g, ' ')
    .trim();
}

/** Every element opening tag carrying attr="value"; returns [{value, index}]. */
function attrValues(html, attr) {
  const out = [];
  const re = new RegExp(attr + '="([^"]*)"', 'g');
  let m;
  while ((m = re.exec(html)) !== null) out.push({ value: m[1], index: m.index });
  return out;
}

/** The inner HTML of the first element whose opening tag carries attr (optionally ="value"). */
function innerOf(html, attr, value) {
  const needle = value === undefined ? attr + '="' : attr + '="' + value + '"';
  const at = html.indexOf(needle);
  if (at < 0) return null;
  const open = html.lastIndexOf('<', at);
  const tag = /^<([a-zA-Z0-9]+)/.exec(html.slice(open))[1];
  const start = html.indexOf('>', at) + 1;
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

function runHarness(file) {
  const { spawnSync } = require('child_process');
  const r = spawnSync(process.execPath, [path.join(base, 'src/pages/SecurityAnalysis/__harness__', file)], {
    cwd: path.join(base, 'src/pages/SecurityAnalysis/__harness__'),
    encoding: 'utf8',
    timeout: 110000,
  });
  const out = (r.stdout || '') + (r.stderr || '');
  // round 4: the Exec harnesses print "EXECTEXT CHECKS 5/5" -- read that form too (N/N green; the tally names the count).
  // round 5: timelineFourStates prints a JSON report whose verdict is an empty "failures" array -- read that form too.
  const green = r.status === 0 && /CHECKS-OK (\d+) of \1\b|^OK:|"result":"PASS"| CHECKS (\d+)\/\2\b|"failures": \[\]/m.test(out);
  const tally = (/CHECKS-OK (\d+) of (\d+)/.exec(out) || / CHECKS (\d+)\/(\d+)/.exec(out) || [])[0] || (r.status === 0 ? 'rc=0' : 'rc=' + r.status);
  return { file, green, tally };
}

/** RAW-CODE CENSUS over visible text, by class. A face with none reads all zeros. */
const RAW_CLASSES = {
  mnemonic: /\b[A-Z][A-Z0-9]*_[A-Z0-9_]+\b/g,
  machine_word: /NOT-YET-BUILT|INTERFACE [A-Z]-\d|held_uncited|ABSENT_ON_OBJECT|crosswalk\/v1|NoSuchKey/g,
  storage_path: /s3:\/\/\S+|org[\/]missions[\/]\S+|\b[\w.-]+\.json\b/g,
  long_digits: /\d{15,}/g,
};
function rawCensus(html) {
  const text = textOf(html);
  const out = {};
  let total = 0;
  for (const [k, re] of Object.entries(RAW_CLASSES)) {
    const hits = text.match(re) || [];
    out[k] = hits.length;
    out[k + '_first'] = hits.slice(0, 3);
    total += hits.length;
  }
  out.total = total;
  return out;
}

module.exports = { rawCensus, RAW_CLASSES, React, source, stubSource, render, textOf, attrValues, innerOf, fixture, hookState, runHarness, base };
