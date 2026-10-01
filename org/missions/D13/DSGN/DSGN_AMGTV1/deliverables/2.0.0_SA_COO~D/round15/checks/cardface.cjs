/**
 * cardface.cjs -- DSGN_AMGTV1 round 15, AV-n-4: THE HEADER CARDS ARE THE PHILOSOPHY CARD FACE (FWD-23; C-ESTATE-FIXTURES).
 *
 * Usage (repo root): cd "$(git rev-parse --show-toplevel)" && node <this file>
 * `portal/` under the working directory is the checkout under test; the base is portal commit b336b141 (DEV), read with
 * `git -C portal show b336b141:<path>` into os.tmpdir().
 *
 * THE CONTRACT THE WORKER BUILDS TO (exact):
 *   - The /philosophy card face (PhilosophyPillars.tsx's pillar card: the bordered white card, its navy GraphicPanel and its
 *     white body) is EXTRACTED into ONE shared module: portal/src/ui/components/graphic/GraphicCard.tsx, exporting a React
 *     component named `GraphicCard`. The face's own classes live in that module (a mutant of one of them must move the
 *     /philosophy bytes), and it renders the face's navy panel through HeroGraphic's `GraphicPanel`.
 *   - PhilosophyPillars.tsx imports `GraphicCard` from that module and renders each of its five pillar cards through it, and
 *     the /philosophy card row renders BYTE-IDENTICALLY before and after (no normalisation of any kind).
 *   - HeaderCards.tsx renders each of its four cards through `GraphicCard`, keeps the `data-header-card="<key>"` attribute on
 *     each card (on the GraphicCard root or on a wrapper around it), and keeps each card's visible words.
 *   - "Through the shared card face" is measured by a PROBE this check adds, never by an attribute the worker writes: the
 *     check's loader wraps the module's `GraphicCard` export so every render of it sits inside
 *     <div data-probe-graphic-card="<n>">. A card is through the face when it pairs with a probe (the probe is its ancestor
 *     or its descendant) and that probe's subtree carries the face marker: an element whose style attribute equals the one
 *     the checkout's own GraphicPanel renders (HeroGraphic's GRAPHIC_PANEL_STYLE).
 *
 * Loader (own, modelled on _load.cjs; _load stubs all of src/ui/** and src/components/** and cannot render the face): the
 * installed typescript + react-dom/server render the REAL sources of src/pages/**, src/lib/**, src/ui/components/graphic/**
 * and the real packages react, lucide-react, clsx, tailwind-merge. Everything else under src/ (catalyst Dialog, panels,
 * Controls, src/components/**, src/api/**, src/hooks/**) and the packages @headlessui/react, recharts, framer-motion,
 * react-router-dom, @visx/wordcloud are STUBS: a stub renders <div data-stub="<Name>"> with its text props, its children and
 * every element-valued prop (a slot); a Dialog stub renders nothing unless `open`. @tanstack/react-query's useQuery returns
 * the check's query data (undefined = the repo copy). The page's SecurityAnalysis hooks return the check's fixtures.
 *
 * Inputs: <cwd>/portal (checkout), portal commit b336b141 (base), round14/fixtures/overlay.BA_US_Equity.json (the served
 * overlay; read through round15/checks/_load.cjs's fixture lookup, round 15 first then round 14).
 * Arms:
 *   1  extraction is byte-identical: the PhilosophyPillars card row rendered from the BASE sources and from the checkout is
 *      byte-identical on two inputs (the repo copy, and a served `philosophy_pillars` override); the module exists and exports
 *      a GraphicCard component; the checkout's PhilosophyPillars imports it; a probed render shows exactly 5 GraphicCard
 *      renders, each carrying the face marker
 *   2  HeaderCards on the served BA overlay renders exactly 4 `data-header-card` cards, each paired with a GraphicCard probe
 *      carrying the face marker; each card's visible words (tags stripped, the hover tooltip `role="tooltip"` subtree
 *      excluded -- hidden until hover, FWD-13's sanctioned mnemonic carrier) contain the base card's words IN ORDER, with at
 *      most 4 added chrome words per card and none carrying a digit (so no figure is added or lost); the raw-code census
 *      (_load.cjs RAW_CLASSES) over the four cards' visible words reads 0
 *   3  the controls: (a) on the BASE sources arm 2's "through the shared card face" predicate FAILS (0 cards paired with a
 *      probe: the base cards are outlined buttons); (b) a planted mutant of the module -- one face class that appears in the
 *      base /philosophy markup renamed everywhere in the module -- makes arm 1's byte-identity FAIL
 * Writes only under os.tmpdir() (the base source copies). No network, no AWS.
 * Wall time measured on site Z (2026-10-01): base checkout 1.8 s (0 of 3), green C:/tmp/dsgn-r15-green-b 1.7 s (3 of 3).
 * Prints one line per arm and "THE HEADER CARDS ARE THE PHILOSOPHY CARD FACE: <k> of 3 arms"; exit 0 only at 3 of 3.
 *
 * When required (not run), exports the loader and the markup helpers for panelhead.cjs.
 */
const fs = require('fs');
const os = require('os');
const path = require('path');
const vm = require('vm');
const { createRequire } = require('module');
const { execFileSync } = require('child_process');

const ROOT = process.cwd();
const PORTAL = path.join(ROOT, 'portal');
const BASE_REV = 'b336b141';
const MODULE_REL = 'src/ui/components/graphic/GraphicCard.tsx';
const MODULE_EXPORT = 'GraphicCard';
const HERO_REL = 'src/ui/components/graphic/HeroGraphic.tsx';
const PILLARS_REL = 'src/pages/CapitalMarketAssumptions/components/PhilosophyPillars.tsx';
const CARDS_REL = 'src/pages/SecurityAnalysis/components/HeaderCards.tsx';
const PROBE = 'data-probe-graphic-card';

// ------------------------------------------------------------------ source trees ------------------------------------------
function workingTree() {
  const seen = {};
  return {
    label: 'checkout',
    read(rel) {
      if (rel in seen) return seen[rel];
      const f = path.join(PORTAL, rel);
      seen[rel] = fs.existsSync(f) && fs.statSync(f).isFile() ? fs.readFileSync(f, 'utf8') : null;
      return seen[rel];
    },
  };
}
let baseList = null;
function baseTree(tmp) {
  if (!baseList) {
    baseList = new Set(
      execFileSync('git', ['-C', PORTAL, 'ls-tree', '-r', '--name-only', BASE_REV, '--', 'src'], { encoding: 'utf8', maxBuffer: 256 << 20 })
        .split('\n')
        .filter(Boolean)
    );
  }
  const dir = path.join(tmp, 'base-' + BASE_REV);
  return {
    label: 'base',
    dir,
    read(rel) {
      if (!baseList.has(rel)) return null;
      const out = path.join(dir, rel);
      if (!fs.existsSync(out)) {
        const text = execFileSync('git', ['-C', PORTAL, 'show', `${BASE_REV}:${rel}`], { encoding: 'utf8', maxBuffer: 64 << 20 });
        fs.mkdirSync(path.dirname(out), { recursive: true });
        fs.writeFileSync(out, text);
      }
      return fs.readFileSync(out, 'utf8');
    },
  };
}

// ------------------------------------------------------------------ the loader --------------------------------------------
const req = createRequire(path.join(PORTAL, 'package.json'));
const ts = req('typescript');
const React = req('react');
const { renderToStaticMarkup } = req('react-dom/server');

const REAL_PACKAGES = new Set(['react', 'react/jsx-runtime', 'react-dom', 'lucide-react', 'clsx', 'tailwind-merge']);
const isElem = (v) => React.isValidElement(v) || (Array.isArray(v) && v.some((x) => React.isValidElement(x)));

function stubComponent(name) {
  const isDialog = /Dialog/.test(name);
  const C = (props) => {
    const p = props || {};
    if (isDialog && !p.open) return null;
    const attrs = { 'data-stub': name };
    if (typeof p.title === 'string') attrs['data-stub-title'] = p.title;
    if (typeof p.eyebrow === 'string') attrs['data-stub-eyebrow'] = p.eyebrow;
    const aria = p.ariaLabel || p['aria-label'];
    if (typeof aria === 'string') attrs['data-stub-arialabel'] = aria;
    const kids = [];
    for (const k of ['title', 'subtitle', 'message', 'detail', 'hint', 'cause', 'label']) {
      if (typeof p[k] === 'string' && p[k]) kids.push(React.createElement('span', { key: 'stub-' + k, 'data-stub-text': k }, p[k]));
    }
    // A Segmented-like control: each option's value and label (a label may be an element).
    if (Array.isArray(p.options)) {
      p.options.forEach((o, i) => {
        if (o && typeof o === 'object') {
          kids.push(React.createElement('span', { key: 'opt-' + i, 'data-stub-option': String(o.value) }, typeof o.label === 'string' || isElem(o.label) ? o.label : null));
        }
      });
    }
    // Every element-valued prop (actions, footer, leftContent, panel, ...) renders as a slot, so nothing a stub is handed hides.
    for (const [k, v] of Object.entries(p)) {
      if (k === 'children') continue;
      if (isElem(v)) kids.push(React.createElement('div', { key: 'slot-' + k, 'data-stub-slot': k }, v));
    }
    if (p.children !== undefined && typeof p.children !== 'function') kids.push(p.children);
    return React.createElement('div', attrs, ...kids);
  };
  C.displayName = name;
  return C;
}
const hookResult = (data) => ({ data, isLoading: false, isError: false, error: null, refetch: () => {}, mutate: () => {}, mutateAsync: async () => {} });
function proxyModule(label, opts) {
  const cache = {};
  return new Proxy(
    {},
    {
      get(_t, key) {
        if (key === '__esModule') return true;
        if (typeof key !== 'string') return undefined;
        if (key === 'cn') return (...xs) => xs.filter(Boolean).join(' ');
        if (key === 'buttonClass') return () => '';
        if (key === 'useQuery') return () => hookResult(opts.queryData);
        if (key === 'useAuth') return () => ({ claims: null, user: null, isAuthenticated: true });
        if (/^use[A-Z]/.test(key)) return () => hookResult(undefined);
        if (!/^[A-Z]/.test(key)) return () => undefined;
        if (!cache[key]) cache[key] = stubComponent(key);
        return cache[key];
      },
    }
  );
}
function hookModule(opts) {
  return new Proxy(
    {},
    {
      get(_t, key) {
        if (key === '__esModule') return true;
        if (typeof key !== 'string') return undefined;
        const impl = (opts.hooks || {})[key];
        if (typeof impl === 'function') return (...args) => hookResult(impl(...args));
        if (/^use[A-Z]/.test(key)) return () => hookResult(undefined);
        return undefined;
      },
    }
  );
}

/**
 * makeLoader(tree, opts): opts.overrides {rel: text} (a mutant), opts.probe (wrap GraphicCard), opts.queryData (useQuery data),
 * opts.hooks {hookName: (...args) => data} for src/pages/SecurityAnalysis/hooks/**. Returns { load(rel), probes() }.
 */
function makeLoader(tree, opts) {
  opts = opts || {};
  const overrides = opts.overrides || {};
  const read = (rel) => (Object.prototype.hasOwnProperty.call(overrides, rel) ? overrides[rel] : tree.read(rel));
  const cache = {};
  let probeCount = 0;
  const isReal = (t) =>
    t === MODULE_REL || t.startsWith('src/ui/components/graphic/') || t.startsWith('src/lib/') || (t.startsWith('src/pages/') && !t.startsWith('src/pages/SecurityAnalysis/hooks/'));

  function resolve(fromRel, name) {
    let t;
    if (name.startsWith('@/')) t = 'src/' + name.slice(2);
    else if (name.startsWith('.')) t = path.posix.normalize(path.posix.join(path.posix.dirname(fromRel), name));
    else return null;
    for (const c of [t, t + '.tsx', t + '.ts', t + '/index.tsx', t + '/index.ts']) if (read(c) !== null) return c;
    return t;
  }
  function load(rel) {
    if (cache[rel]) return cache[rel];
    const text = read(rel);
    if (text === null) throw new Error(`${tree.label}: no source ${rel}`);
    const js = ts.transpileModule(text, {
      compilerOptions: { module: ts.ModuleKind.CommonJS, jsx: ts.JsxEmit.ReactJSX, target: ts.ScriptTarget.ES2022, esModuleInterop: true },
    }).outputText;
    const mod = { exports: {} };
    cache[rel] = mod.exports;
    function requireFrom(name) {
      if (REAL_PACKAGES.has(name)) return req(name);
      const target = resolve(rel, name);
      if (target === null) return proxyModule(name, opts); // every other package is a stub
      if (target.startsWith('src/pages/SecurityAnalysis/hooks/')) return hookModule(opts);
      if (!isReal(target)) return proxyModule(target, opts);
      if (read(target) === null) throw new Error(`${tree.label}: cannot resolve ${name} from ${rel}`);
      return load(target);
    }
    vm.runInThisContext('(function(require,module,exports){' + js + '\n})', { filename: path.join(PORTAL, rel) })(requireFrom, mod, mod.exports);
    let out = mod.exports;
    if (rel === MODULE_REL && opts.probe && typeof mod.exports[MODULE_EXPORT] === 'function') {
      const Real = mod.exports[MODULE_EXPORT];
      const Probed = (props) => React.createElement('div', { [PROBE]: String(++probeCount) }, React.createElement(Real, props));
      out = Object.assign({}, mod.exports, { [MODULE_EXPORT]: Probed });
    }
    cache[rel] = out;
    return out;
  }
  return { load, probes: () => probeCount, read };
}
const render = (C, props) => renderToStaticMarkup(React.createElement(C, props || {}));

/** The import specifiers of a source, resolved to portal-relative paths (from the transpiled require calls). */
function importsOf(tree, rel) {
  const text = tree.read(rel);
  if (text === null) return [];
  const js = ts.transpileModule(text, { compilerOptions: { module: ts.ModuleKind.CommonJS, jsx: ts.JsxEmit.ReactJSX, target: ts.ScriptTarget.ES2022 } }).outputText;
  const out = [];
  const re = /require\("([^"]+)"\)/g;
  let m;
  while ((m = re.exec(js)) !== null) {
    const n = m[1];
    let t = n.startsWith('@/') ? 'src/' + n.slice(2) : n.startsWith('.') ? path.posix.normalize(path.posix.join(path.posix.dirname(rel), n)) : n;
    for (const c of [t + '.tsx', t + '.ts', t]) if (tree.read(c) !== null) { t = c; break; }
    out.push(t);
  }
  return out;
}

// ------------------------------------------------------------------ markup helpers ----------------------------------------
const VOID = new Set(['area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'source', 'track', 'wbr']);
const decode = (s) => s.replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&quot;/g, '"').replace(/&#x27;/g, "'").replace(/&#39;/g, "'").replace(/&amp;/g, '&');
/** A tree of the static markup: {tag, attrs, children, start, parent}; text nodes {text}. */
function parse(html) {
  const root = { tag: '#root', attrs: '', children: [], start: 0, parent: null };
  const stack = [root];
  const re = /<!--[\s\S]*?-->|<(\/?)([a-zA-Z][\w:.-]*)((?:\s[^>]*?)?)(\/?)>|([^<]+)/g;
  let m;
  while ((m = re.exec(html)) !== null) {
    if (m[0].startsWith('<!--')) continue;
    if (m[5] !== undefined) {
      stack[stack.length - 1].children.push({ text: decode(m[5]) });
      continue;
    }
    const tag = m[2].toLowerCase();
    if (m[1]) {
      for (let i = stack.length - 1; i > 0; i -= 1) if (stack[i].tag === tag) { stack.length = i; break; }
      continue;
    }
    const node = { tag, attrs: m[3] || '', children: [], start: m.index, parent: stack[stack.length - 1] };
    stack[stack.length - 1].children.push(node);
    if (!m[4] && !VOID.has(tag)) stack.push(node);
  }
  return root;
}
function attr(node, name) {
  if (!node || !node.attrs) return null;
  const m = new RegExp('(?:^|\\s)' + name.replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + '="([^"]*)"').exec(node.attrs);
  return m ? decode(m[1]) : null;
}
function all(node, pred, out) {
  out = out || [];
  for (const c of node.children || []) {
    if (c.tag === undefined) continue;
    if (pred(c)) out.push(c);
    all(c, pred, out);
  }
  return out;
}
const ancestors = (n) => { const a = []; for (let p = n.parent; p; p = p.parent) a.push(p); return a; };
/** Visible words of a subtree; a subtree for which skip(node) is true contributes none. */
function words(node, skip) {
  const out = [];
  (function walk(n) {
    for (const c of n.children || []) {
      if (c.tag === undefined) { out.push(...c.text.split(/\s+/).filter(Boolean)); continue; }
      if (skip && skip(c)) continue;
      walk(c);
    }
  })(node);
  return out;
}
const isTooltip = (n) => attr(n, 'role') === 'tooltip';
/** The face marker: the style attribute the checkout's own GraphicPanel renders. */
function faceMarker(loader) {
  const hero = loader.load(HERO_REL);
  if (typeof hero.GraphicPanel !== 'function') return null;
  const tree = parse(render(hero.GraphicPanel, {}));
  const el = (tree.children || []).find((c) => c.tag);
  return el ? attr(el, 'style') : null;
}
const hasMarker = (node, marker) => Boolean(marker) && all(node, (c) => attr(c, 'style') === marker).length > 0;
const probesOf = (tree) => all(tree, (c) => attr(c, PROBE) !== null);
/** Pair each card with a probe: the probe is the card's ancestor, or a descendant of the card. */
function pairProbe(card) {
  const up = ancestors(card).find((a) => attr(a, PROBE) !== null);
  if (up) return up;
  return probesOf(card)[0] || null;
}
function isSubsequence(needle, hay) {
  let i = 0;
  for (const w of hay) if (i < needle.length && w === needle[i]) i += 1;
  return i === needle.length;
}

module.exports = {
  ROOT, PORTAL, BASE_REV, MODULE_REL, MODULE_EXPORT, HERO_REL, PROBE, React, ts,
  workingTree, baseTree, makeLoader, render, importsOf, parse, attr, all, ancestors, words, isTooltip, faceMarker, hasMarker,
  probesOf, pairProbe,
};

// ================================================================== the check =============================================
if (require.main === module) {
  const T0 = Date.now();
  const TMP = fs.mkdtempSync(path.join(os.tmpdir(), 'r15-cardface-'));
  const L = require('./_load.cjs'); // fixture lookup (round 15 then round 14) and the raw-code classes; it renders nothing here
  const BASE = baseTree(TMP);
  const WORK = workingTree();
  const unwrap = (x) => (x && x.payload && (x._capture_note || x._capture) ? x.payload : x);
  const SERVED_PILLARS = {
    philosophy_pillars: [
      { id: 'long-term-perspective', title: 'Invest for the Long Run', tagline: '', body: '' },
      { id: 'after-tax-outcomes', title: '', tagline: 'What the investor keeps is what counts.', body: '' },
      { id: 'not-a-pillar', title: 'Ignored row', tagline: 'Unknown ids are ignored.', body: '' },
    ],
  };
  const INPUTS = [['repo copy', undefined], ['served override', SERVED_PILLARS]];
  const pillarsRow = (tree, queryData, extra) => {
    const ld = makeLoader(tree, Object.assign({ queryData }, extra || {}));
    const { PhilosophyPillars } = ld.load(PILLARS_REL);
    return { html: render(PhilosophyPillars), ld };
  };
  const tryOr = (fn) => { try { return { v: fn() }; } catch (e) { return { err: String(e.message).split('\n')[0] }; } };

  // ---------------- arm 1: the extraction is byte-identical ----------------
  const f1 = [];
  const n1 = [];
  const baseRows = {};
  for (const [label, q] of INPUTS) {
    const b = tryOr(() => pillarsRow(BASE, q).html);
    const c = tryOr(() => pillarsRow(WORK, q).html);
    if (b.err) { f1.push(`${label}: the base render threw: ${b.err}`); continue; }
    baseRows[label] = b.v;
    if (c.err) { f1.push(`${label}: the checkout render threw: ${c.err}`); continue; }
    if (b.v !== c.v) {
      let i = 0;
      while (i < b.v.length && b.v[i] === c.v[i]) i += 1;
      f1.push(`${label}: NOT byte-identical (base ${b.v.length} B, checkout ${c.v.length} B; first difference at byte ${i}: base "${b.v.slice(i, i + 60)}" vs checkout "${c.v.slice(i, i + 60)}")`);
    } else n1.push(`${label} ${b.v.length} B identical`);
  }
  const modText = WORK.read(MODULE_REL);
  let marker = null;
  if (modText === null) f1.push(`no shared module ${MODULE_REL}`);
  else {
    const m = tryOr(() => makeLoader(WORK).load(MODULE_REL));
    if (m.err) f1.push(`the module does not load: ${m.err}`);
    else if (typeof m.v[MODULE_EXPORT] !== 'function') f1.push(`the module exports no ${MODULE_EXPORT} component`);
  }
  if (!importsOf(WORK, PILLARS_REL).includes(MODULE_REL)) f1.push(`PhilosophyPillars.tsx does not import ${MODULE_REL}`);
  const pr = tryOr(() => {
    const r = pillarsRow(WORK, undefined, { probe: true });
    marker = faceMarker(r.ld);
    const t = parse(r.html);
    const probes = probesOf(t);
    return { n: probes.length, withFace: probes.filter((p) => hasMarker(p, marker)).length };
  });
  if (pr.err) f1.push(`the probed render threw: ${pr.err}`);
  else {
    if (pr.v.n !== 5) f1.push(`${pr.v.n} GraphicCard renders on /philosophy (want 5, one per pillar)`);
    if (pr.v.withFace !== pr.v.n) f1.push(`${pr.v.n - pr.v.withFace} pillar GraphicCard renders carry no GraphicPanel face`);
    n1.push(`probed: ${pr.v.n} GraphicCard renders, ${pr.v.withFace} with the face`);
  }
  const a1 = f1.length === 0;
  const a1d = a1 ? n1.join('; ') : `${f1.length} failing; first: ${f1[0]}${n1.length ? ' || ' + n1.join('; ') : ''}`;

  // ---------------- arm 2: the four header cards through the face ----------------
  const bundle = unwrap(L.fixture('overlay.BA_US_Equity.json'));
  function headerCards(tree) {
    const ld = makeLoader(tree, { probe: true });
    const { HeaderCards } = ld.load(CARDS_REL);
    const html = render(HeaderCards, { bundle });
    const mk = faceMarker(ld);
    const t = parse(html);
    const cards = all(t, (c) => attr(c, 'data-header-card') !== null);
    return {
      html,
      cards: cards.map((c) => {
        const p = pairProbe(c);
        return { key: attr(c, 'data-header-card'), words: words(c, isTooltip), probe: Boolean(p), face: Boolean(p) && hasMarker(p, mk) };
      }),
    };
  }
  const f2 = [];
  let a2d = '';
  const G2 = tryOr(() => headerCards(WORK));
  const B2 = tryOr(() => headerCards(BASE));
  if (G2.err) f2.push(`the checkout HeaderCards render threw: ${G2.err}`);
  if (B2.err) f2.push(`the base HeaderCards render threw: ${B2.err}`);
  if (!G2.err && !B2.err) {
    const g = G2.v.cards;
    const b = B2.v.cards;
    if (g.length !== 4) f2.push(`${g.length} data-header-card cards (want exactly 4)`);
    const through = g.filter((c) => c.probe && c.face).length;
    if (through !== g.length) f2.push(`${g.length - through} of ${g.length} cards are not through the shared card face (${g.filter((c) => !c.probe).map((c) => c.key).join(', ') || 'paired but no GraphicPanel face'})`);
    const textF = [];
    for (const bc of b) {
      const gc = g.find((c) => c.key === bc.key);
      if (!gc) { textF.push(`${bc.key}: missing`); continue; }
      if (!isSubsequence(bc.words, gc.words)) textF.push(`${bc.key}: base words "${bc.words.join(' ')}" not in order in "${gc.words.join(' ')}"`);
      const extra = gc.words.length - bc.words.length;
      const added = [...gc.words];
      for (const w of bc.words) { const i = added.indexOf(w); if (i >= 0) added.splice(i, 1); }
      if (extra > 4) textF.push(`${bc.key}: ${extra} added words (max 4 chrome words)`);
      if (added.some((w) => /\d/.test(w))) textF.push(`${bc.key}: an added word carries a digit (${added.filter((w) => /\d/.test(w)).join(' ')})`);
    }
    if (textF.length) f2.push(`visible words changed: ${textF[0]}${textF.length > 1 ? ` (+${textF.length - 1} more)` : ''}`);
    const allWords = g.map((c) => c.words.join(' ')).join(' ');
    let raw = 0;
    const rawFirst = [];
    for (const [k, re] of Object.entries(L.RAW_CLASSES)) {
      const hits = allWords.match(new RegExp(re.source, re.flags)) || [];
      raw += hits.length;
      if (hits.length) rawFirst.push(`${k}: ${hits.slice(0, 2).join(', ')}`);
    }
    if (raw) f2.push(`raw code in the cards' visible words: ${rawFirst.join('; ')}`);
    a2d = `${g.length} cards, ${through} through the face; words ${g.map((c) => `${c.key}="${c.words.join(' ')}"`).join(' | ')}; raw ${raw}`;
  }
  const a2 = f2.length === 0;
  const a2dd = a2 ? a2d : `${f2.length} failing; first: ${f2[0]}${a2d ? ' || ' + a2d : ''}`;

  // ---------------- arm 3: the controls ----------------
  const f3 = [];
  const n3 = [];
  if (B2.err) f3.push(`(a) the base render threw: ${B2.err}`);
  else {
    const through = B2.v.cards.filter((c) => c.probe && c.face).length;
    if (through === B2.v.cards.length && B2.v.cards.length > 0) f3.push(`(a) at base, ${through} of ${B2.v.cards.length} cards read as through the shared face -- the predicate cannot say no`);
    else n3.push(`(a) base: ${through} of ${B2.v.cards.length} cards through the face (the predicate says no)`);
  }
  if (modText === null) f3.push(`(b) no module ${MODULE_REL} to mutate`);
  else if (!baseRows['repo copy']) f3.push('(b) no base /philosophy render to compare against');
  else {
    const baseClasses = new Set();
    for (const m of baseRows['repo copy'].matchAll(/class="([^"]*)"/g)) for (const c of m[1].split(/\s+/)) if (c) baseClasses.add(c);
    const esc = (s) => s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    const has = (tok) => new RegExp(`(?<![\\w-])${esc(tok)}(?![\\w-])`).test(modText);
    const preferred = ['border-black', 'rounded-[4px]', 'overflow-hidden', 'bg-white', 'p-4'];
    const tok = preferred.find((t) => baseClasses.has(t) && has(t)) || [...baseClasses].find((t) => t.length > 3 && has(t));
    if (!tok) f3.push('(b) the module carries none of the /philosophy card face classes -- the face was not extracted into it');
    else {
      const mutant = modText.replace(new RegExp(`(?<![\\w-])${esc(tok)}(?![\\w-])`, 'g'), tok + '-r15bmutant');
      const r = tryOr(() => pillarsRow(WORK, undefined, { overrides: { [MODULE_REL]: mutant } }).html);
      if (r.err) f3.push(`(b) the mutant render threw: ${r.err}`);
      else if (r.v === baseRows['repo copy']) f3.push(`(b) the mutant (class "${tok}" renamed) still renders byte-identical -- arm 1 cannot say no`);
      else n3.push(`(b) mutant "${tok}" -> "${tok}-r15bmutant": /philosophy bytes differ (${r.v.length} B vs ${baseRows['repo copy'].length} B), arm 1 FAILS on it`);
    }
  }
  const a3 = f3.length === 0;
  const a3d = a3 ? n3.join('; ') : `${f3.length} failing; first: ${f3[0]}${n3.length ? ' || ' + n3.join('; ') : ''}`;

  console.log(`RUNS: base ${BASE_REV} sources in ${BASE.dir}; wall ${Math.round((Date.now() - T0) / 100) / 10}s`);
  const arms = [
    ['the /philosophy card row renders byte-identically through the extracted module', a1, a1d],
    ['the four header cards render through the shared card face, words kept, no raw code', a2, a2dd],
    ['the controls: the base cards are not through the face; a module mutant breaks byte-identity', a3, a3d],
  ];
  let pass = 0;
  for (const [name, ok, detail] of arms) { if (ok) pass += 1; console.log(`${ok ? 'ARM PASS' : 'ARM FAIL'} ${name} :: ${detail}`); }
  console.log(`THE HEADER CARDS ARE THE PHILOSOPHY CARD FACE: ${pass} of ${arms.length} arms`);
  process.exit(pass === arms.length ? 0 : 1);
}
