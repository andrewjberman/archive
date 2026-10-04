/**
 * repairs34.cjs -- DSGN_AMGTV1 round 34, REPAIR CELL check 2 of 2 (issuer 2.0.0_SA_COO~D): A MOVE NAMES ITS WINDOW, A CHANGE PRINTS
 * AT ITS ROW'S PRECISION, AND THE TIMELINE AXIS INK MEETS THE INK LAW (PRD FWD-27; FWD-20's contrast clause).
 *
 * Usage (from the directory whose portal/ is the checkout under test, e.g. C:/tmp/wk-dsgn-amgtv1-92): node <this file>
 *   ISSUER GREEN ARM: CHECK_SRC_OVERRIDE (see round15/checks/_load.cjs) is honoured for every source read here.
 * Why: ledger/COMPLETION_GRADES.round32.json row FWD-27 (NOT_REALIZED): "The header breakout move names no window beside the Price
 *   face's 30-day move, and What changed prints raw-precision changes that disagree with its rounded before/after" (FWD-26 row:
 *   "the header readings print 'BREAKOUT (PRICE) #62 | -3.78%' with no window named"; FWD-25 row: "'+0.1321', '-1.5278', '+0.0633'
 *   on a percent figure, '+0.0011', and a signed '-0.00'"); FWD-5 / FWD-20 rows: "the chart's tick labels are drawn rgb(168,176,192)
 *   = #A8B0C0 on white, measured contrast 2.18:1 (TimelinePanel.tsx:188 AXIS_TEXT_FILL '#A8B0C0')". ledger/ROUND_ANALYSIS.round33.md
 *   section 3 item 2 (the repair cell). PROD dbd29c6320: SecurityOverlay.tsx:476-483 prints `#rank | <pct_jump_pct>%` with no
 *   window; WhatChangedPanel.tsx:145-168 prints the change through groupedDigits (up to 4 places) or `toFixed(2) pts`;
 *   TimelinePanel.tsx:188 paints every axis text '#A8B0C0' inside the header's white nested Panel.
 * Render: round15/checks/_load.cjs (the REAL page sources) through round29/checks/timeline/_tl.cjs (its recharts recorder, query
 *   stubs, DataTooltip and HeroDialog stubs). The header is the REAL IdentityHeader (SecurityOverlay.tsx) with the REAL Panel
 *   (panels/Panel.tsx) and HeaderBrief / TimelinePanel as markers (round29 header/face.cjs's method).
 * THE SERVED WINDOW OF THE HEADER MOVE: the BREAKOUT/PRICE row (`axis_reads[BREAKOUT,PRICE].row`, else `breakout_price`) serves
 *   `window_days` (30 on every served /rankings/breakout/price row, round14/fixtures/rankings.BREAKOUT_PRICE.json; 30 on the
 *   r15c rows). The move is `pct_jump_pct`.
 * THE DISPLAY PRECISION OF A ROW (arm 2): a printed number's RESOLUTION is the place of its last printed digit times its magnitude
 *   suffix (T 1e12, B 1e9, M 1e6, K 1e3): "USD 162B" 1e9, "6.04M" 1e4, "2.90" 0.01, "23.5x" 0.1. Let r and R be the finer and the
 *   coarser resolution of the row's before and after cells. The change cell's value C is AT the row's precision when (a) C is a
 *   whole multiple of r (it carries no digit finer than the row) and (b) C is the served change rounded at R (|C - (to - from) x u|
 *   <= R/2, u the display scale the after cell implies, e.g. 1e6 for a currency-millions figure) or exactly after minus before as
 *   printed. "+0.1321" against "2.90 -> 3.04" fails (a); "+0.1" fails (b); "+0.13" and "+0.14" pass. A row whose before or after
 *   prints no number is not graded.
 * THE INK LAW (arm 3): WCAG 2.x contrast (sRGB relative luminance, (L1 + 0.05) / (L2 + 0.05)) >= 4.5:1 for every axis text paint:
 *   each XAxis / YAxis tick (tick.fill, else the axis stroke, else recharts 3.7's '#666' -- CartesianAxis paints tick text with the
 *   axis stroke) and each axis label (label.fill, else recharts Text's default '#808080'); a tick or label given as an element or
 *   function is rendered and its <text>/<tspan> fill read. The GROUND is the nearest painted ancestor of the chart: first inside
 *   TimelinePanel's own render, then above the TimelinePanel marker inside the rendered IdentityHeader, else the page canvas
 *   (--bg-page). A colour token resolves through portal/src/index.css (:root, then body) and portal/design/themes/opal-capital.css
 *   (:root[data-theme="opal-capital"], light mode), the files the page loads; a value that does not resolve is a fault.
 * Inputs: round15/fixtures/r15c.overlay.{BA_US,VLO_US,6501_JP}_Equity.json (BA and VLO with a served breakout row, 6501 truly
 *   absent); PLANTED in memory (labelled): BA with its breakout window_days 90 (the window must come from the served field) and BA
 *   with window_days removed (a move whose window is not served). round29/fixtures/model/served.BA_US_Equity.json (the 7 served
 *   changed header figures) plus round30 served.cjs's 6 PLANTED sheet lines, answered for every pair (as served.cjs). round14/
 *   fixtures/timeline.BA_US_Equity.json (the served /timeline range).
 * Arms:
 *   1  THE HEADER MOVE NAMES ITS WINDOW: on BA, VLO and the 90-day plant the Breakout (price) cell prints the served move with
 *      "over the last <window_days> days" in the same cell; on the no-window plant and on 6501 it prints no percent; every signed
 *      percent elsewhere in the header names a window ("over the last N days") in its element or that element's parent; and round29
 *      header/face.cjs still exits 0.
 *   2  WHAT CHANGED PRINTS ITS CHANGE AT DISPLAY PRECISION: on 13 changed lines (7 served + 6 planted) every change cell is at its
 *      row's display precision (above); and round30 repairs/served.cjs (which runs round29 whatchanged.cjs and etwords.cjs) still
 *      exits 0.
 *   3  THE TIMELINE AXIS LABELS MEET THE INK LAW: on the served BA range every axis tick and axis label paint reaches 4.5:1 on the
 *      timeline's ground; and round29 timeline/chart.cjs still exits 0.
 *   4  PLANTED: the move predicate rejects 4 bad cells and accepts 3 good ones; the precision predicate rejects 5 bad change cells
 *      and accepts 5 good ones; the ink predicate rejects 5 bad paints/grounds and accepts 3 good ones; each rejection is checked
 *      for its own reason (the fault text it must print).
 * Blind spots: arm 1 reads the header as markup, at rest and behind its <details> alike; a window named in a tooltip only is not
 *   seen. Arm 2 grades precision, not wording or sign style: a change that rounds to zero may still print "-0.00" (round29
 *   whatchanged.cjs grades direction). Arm 3 grades the attributes recharts is handed (no stylesheet rule overrides them at
 *   dbd29c6320: index.css holds no recharts fill rule); a custom tick that paints through CSS `color` or currentColor is read as
 *   the SVG default black; light mode only (the dark-mode theme block is not read).
 * Prints one line per arm and "A MOVE NAMES ITS WINDOW, A CHANGE ITS PRECISION, THE AXIS ITS INK: <k> of 4 arms"; exit 0 only at
 * 4 of 4. Static renders only; no network, no AWS, writes no file.
 */
const fs = require('fs');
const path = require('path');
const { spawnSync } = require('child_process');

const SA = 'src/pages/SecurityAnalysis/';
const DROOT = path.join(__dirname, '..', '..', '..');
const T = require(path.join(DROOT, 'round29', 'checks', 'timeline', '_tl.cjs'));
const L = T.L;
const h = L.React.createElement;
const readJson = (p) => JSON.parse(fs.readFileSync(path.join(DROOT, p), 'utf8'));
const pay = (x) => (x && x.payload && (x._capture_note || x._capture) ? x.payload : x);
const clone = (x) => JSON.parse(JSON.stringify(x));
const first = (e) => String(e && e.message ? e.message : e).split('\n')[0];
const { parse, all, visible, norm } = T;
function keepsPassing(rels) {
  const faults = [];
  for (const rel of rels) {
    const r = spawnSync(process.execPath, [path.join(DROOT, rel)], { cwd: process.cwd(), encoding: 'utf8', timeout: 300000 });
    const last = ((r.stdout || '') + (r.stderr || '')).trim().split('\n').pop() || '';
    if (r.status !== 0) faults.push(`KEEP: ${rel} rc=${r.status} ("${last.slice(0, 100)}")`);
  }
  return faults;
}

// ==== arm 1: the header move ===================================================================================================
const ownText = (n) => norm((n.children || []).filter((c) => c.text !== undefined).map((c) => c.text).join(' '));
const axisRead = (ov, mv, sb) => (ov.axis_reads || []).find((e) => e.movement === mv && e.subject === sb);
const breakoutRow = (ov) => { const a = axisRead(ov, 'BREAKOUT', 'PRICE'); return (a && a.row) || ov.breakout_price || null; };
const windowOf = (row) => (row && typeof row.window_days === 'number' && Number.isFinite(row.window_days) && row.window_days > 0 ? row.window_days : null);
const windowWords = (n) => `over the last ${n} ${n === 1 ? 'day' : 'days'}`;
const ANY_WINDOW = /\bover the last (\d+) days?\b/g;
const PCT = /[-+\u2212]?\d+(?:\.\d+)?\s*%/g;
const SIGNED_PCT = /[-+\u2212]\d+(?:\.\d+)?\s*%/;
/** One rendered header (html) against its overlay payload: the breakout cell, then every signed percent in the header. */
function moveFaults(name, html, ov) {
  const f = [];
  const tree = parse(html);
  const els = all(tree, () => true);
  const label = els.find((n) => /^Breakout \(price\)/.test(ownText(n)));
  const row = breakoutRow(ov);
  const win = windowOf(row);
  const pct = row && typeof row.pct_jump_pct === 'number' ? row.pct_jump_pct : null;
  if (!label) f.push(`${name}: no element whose own text starts "Breakout (price)"`);
  else {
    const cell = visible(label.parent);
    const ps = cell.match(PCT) || [];
    const named = [...cell.matchAll(ANY_WINDOW)].map((m) => Number(m[1]));
    if (row && win !== null && pct !== null) {
      if (!ps.length) f.push(`${name}: the breakout cell prints no move (served pct_jump_pct ${pct}): "${cell.slice(0, 90)}"`);
      else if (!cell.includes(windowWords(win))) f.push(`${name}: the breakout move ${ps[0]} does not say "${windowWords(win)}" (served window_days ${win}): "${cell.slice(0, 90)}"`);
      const wrong = named.filter((n) => n !== win);
      if (wrong.length) f.push(`${name}: the breakout cell names a window of ${wrong[0]} days; the served window_days is ${win}`);
    } else if (ps.length) f.push(`${name}: the breakout cell prints ${ps[0]} although ${row ? 'the row serves no window_days' : 'no breakout row is served'}: "${cell.slice(0, 90)}"`);
  }
  // Every other signed percent in the header is a move too: a window named in its element or that element's parent.
  const cellNodes = new Set(label ? all(label.parent, () => true) : []);
  for (const n of els) {
    if (cellNodes.has(n)) continue;
    const t = ownText(n);
    if (!SIGNED_PCT.test(t)) continue;
    const near = [n, n.parent].filter((x) => x && x.tag && x.tag !== '#root').map((x) => visible(x));
    if (!near.some((s) => /\bover the last \d+ days?\b/.test(s))) f.push(`${name}: the move "${t.match(SIGNED_PCT)[0]}" names no window ("${visible(n.parent || n).slice(0, 80)}")`);
  }
  return [...new Set(f)];
}

// ==== arm 2: the change at display precision ===================================================================================
const SCALE = { T: 1e12, B: 1e9, M: 1e6, K: 1e3 };
/** The first number a cell prints: signed value (suffix applied), its resolution, or null. */
function numOf(text) {
  const t = String(text === null || text === undefined ? '' : text).replace(/\u2212/g, '-');
  const m = /(\d[\d,]*)(?:\.(\d+))?(?:([TBMK])(?![A-Za-z]))?/.exec(t);
  if (!m) return null;
  const neg = /-\s*(?:[A-Z]{3}\s*)?$/.test(t.slice(0, m.index));
  const scale = SCALE[m[3]] || 1;
  const digits = m[2] ? m[2].length : 0;
  const v = Number(m[1].replace(/,/g, '') + (m[2] ? '.' + m[2] : '')) * scale * (neg ? -1 : 1);
  return { v, res: Math.pow(10, -digits) * scale, raw: m[0] };
}
const fmtNum = (x) => (Math.abs(x) >= 1e3 || x === 0 ? x.toExponential(2).replace('e+0', '').replace(/e\+?/, 'e') : String(Number(x.toPrecision(6))));
const numeric = (v) => { if (v === null || v === undefined) return null; const n = typeof v === 'number' ? v : String(v).trim() === '' ? NaN : Number(v); return Number.isFinite(n) ? n : null; };
/** rows: [{ change, before, after, chg }] (cell texts). Returns { faults, graded }. */
function precisionFaults(rows) {
  const f = [];
  let graded = 0;
  for (const r of rows) {
    const nm = r.change.mnemonic;
    const B = numOf(r.before); const A = numOf(r.after);
    if (!B || !A) continue;
    graded += 1;
    const C = numOf(r.chg);
    if (!C) { f.push(`${nm}: the change cell "${norm(r.chg || '')}" prints no number`); continue; }
    const fine = Math.min(B.res, A.res); const coarse = Math.max(B.res, A.res);
    const k = C.v / fine;
    if (Math.abs(k - Math.round(k)) > 1e-6) { f.push(`${nm}: change "${norm(r.chg)}" prints a digit finer than its row ("${norm(r.before)}" -> "${norm(r.after)}", resolution ${fmtNum(fine)})`); continue; }
    const from = numeric(r.change.from); const to = numeric(r.change.to);
    let ok = Math.abs(C.v - (A.v - B.v)) <= fine * 1e-6;
    if (!ok && from !== null && to !== null) {
      const ref = to !== 0 ? A.v / to : from !== 0 ? B.v / from : 1;
      const u = ref > 0 ? Math.pow(10, Math.round(Math.log10(ref))) : 1;
      ok = Math.abs(C.v - (to - from) * u) <= coarse / 2 + coarse * 1e-9;
    }
    if (!ok) f.push(`${nm}: change "${norm(r.chg)}" is not the change at the row's precision ("${norm(r.before)}" -> "${norm(r.after)}")`);
  }
  return { faults: f, graded };
}

// ==== arm 3: colour, tokens, contrast ==========================================================================================
const OVR = {};
for (const pair of (process.env.CHECK_SRC_OVERRIDE || '').split(';').filter(Boolean)) { const i = pair.indexOf('='); OVR[pair.slice(0, i)] = pair.slice(i + 1); }
const srcText = (rel) => { const p = OVR[rel] || path.join(L.base, rel); return fs.existsSync(p) ? fs.readFileSync(p, 'utf8') : null; };
/** Custom-property declarations of the rule blocks whose selector is one of `selectors` (comments stripped, @-blocks entered). */
function declsOf(css, selectors) {
  const out = [];
  const s = String(css || '').replace(/\/\*[\s\S]*?\*\//g, '');
  const walk = (from, to) => {
    let i = from; let pre = from;
    while (i < to) {
      const ch = s[i];
      if (ch === '{') {
        let depth = 1; let j = i + 1;
        while (j < to && depth > 0) { if (s[j] === '{') depth += 1; else if (s[j] === '}') depth -= 1; j += 1; }
        const sel = s.slice(pre, i).replace(/\s+/g, ' ').trim();
        const body = s.slice(i + 1, j - 1);
        if (/^@/.test(sel)) walk(i + 1, j - 1);
        else if (sel.split(',').map((x) => x.trim()).some((x) => selectors.includes(x))) {
          for (const m of body.matchAll(/(--[\w-]+)\s*:\s*([^;{}]+);/g)) out.push([m[1], m[2].trim()]);
        }
        i = j; pre = j;
      } else if (ch === ';' || ch === '}') { i += 1; pre = i; } else i += 1;
    }
  };
  walk(0, s.length);
  return out;
}
function tokenMap() {
  const vars = new Map();
  const idx = srcText('src/index.css');
  const themeFile = path.join(L.base, 'design', 'themes', 'opal-capital.css');
  const theme = fs.existsSync(themeFile) ? fs.readFileSync(themeFile, 'utf8') : '';
  for (const [k, v] of declsOf(idx, [':root'])) vars.set(k, v);
  for (const [k, v] of declsOf(theme, [':root[data-theme="opal-capital"]'])) vars.set(k, v);
  for (const [k, v] of declsOf(idx, ['body'])) vars.set(k, v);
  return vars;
}
const TOKENS = tokenMap();
function resolveVars(v, vars, depth) {
  let s = String(v);
  for (let d = 0; d < (depth || 12) && /var\(/.test(s); d += 1) {
    s = s.replace(/var\(\s*(--[\w-]+)\s*(?:,\s*([^()]*))?\)/g, (all_, name, fb) => (vars.has(name) ? vars.get(name) : fb !== undefined ? fb : `UNRESOLVED(${name})`));
  }
  return s;
}
const NAMED = { white: [255, 255, 255, 1], black: [0, 0, 0, 1], transparent: [0, 0, 0, 0] };
function hslToRgb(h, s, l) {
  h = ((h % 360) + 360) % 360; s /= 100; l /= 100;
  const c = (1 - Math.abs(2 * l - 1)) * s; const x = c * (1 - Math.abs(((h / 60) % 2) - 1)); const m = l - c / 2;
  const [r, g, b] = h < 60 ? [c, x, 0] : h < 120 ? [x, c, 0] : h < 180 ? [0, c, x] : h < 240 ? [0, x, c] : h < 300 ? [x, 0, c] : [c, 0, x];
  return [(r + m) * 255, (g + m) * 255, (b + m) * 255];
}
/** A CSS colour (after token resolution) as [r, g, b, a], or null. */
function parseColour(raw, vars) {
  const s = resolveVars(String(raw).trim(), vars || TOKENS).trim().toLowerCase();
  if (/unresolved/.test(s)) return null;
  if (NAMED[s]) return NAMED[s].slice();
  let m = /^#([0-9a-f]{3,8})$/.exec(s);
  if (m) {
    const x = m[1];
    if (x.length === 3 || x.length === 4) return [...x.split('').map((c) => parseInt(c + c, 16)).slice(0, 3), x.length === 4 ? parseInt(x[3] + x[3], 16) / 255 : 1];
    if (x.length === 6 || x.length === 8) return [parseInt(x.slice(0, 2), 16), parseInt(x.slice(2, 4), 16), parseInt(x.slice(4, 6), 16), x.length === 8 ? parseInt(x.slice(6, 8), 16) / 255 : 1];
    return null;
  }
  m = /^(rgba?|hsla?)\((.*)\)$/.exec(s);
  if (!m) return null;
  const parts = m[2].replace(/\//g, ' / ').split(/[\s,]+/).filter(Boolean);
  const slash = parts.indexOf('/');
  const ch = (slash >= 0 ? parts.slice(0, slash) : parts.slice(0, 3));
  let alpha = slash >= 0 ? parts[slash + 1] : parts[3];
  alpha = alpha === undefined ? 1 : /%$/.test(alpha) ? Number(alpha.slice(0, -1)) / 100 : Number(alpha);
  if (ch.length !== 3 || !Number.isFinite(alpha)) return null;
  if (m[1].startsWith('rgb')) {
    const v = ch.map((c) => (/%$/.test(c) ? Number(c.slice(0, -1)) * 2.55 : Number(c)));
    return v.every(Number.isFinite) ? [...v, alpha] : null;
  }
  const hh = Number(ch[0].replace(/deg$/, '')); const ss = Number(ch[1].replace(/%$/, '')); const ll = Number(ch[2].replace(/%$/, ''));
  if (![hh, ss, ll].every(Number.isFinite)) return null;
  return [...hslToRgb(hh, ss, ll), alpha];
}
const over = (fg, bg) => [0, 1, 2].map((i) => fg[i] * fg[3] + bg[i] * (1 - fg[3])).concat([1]);
const lum = (c) => { const [r, g, b] = c.slice(0, 3).map((v) => { const x = v / 255; return x <= 0.04045 ? x / 12.92 : Math.pow((x + 0.055) / 1.055, 2.4); }); return 0.2126 * r + 0.7152 * g + 0.0722 * b; };
const contrast = (a, b) => { const la = lum(a); const lb = lum(b); return (Math.max(la, lb) + 0.05) / (Math.min(la, lb) + 0.05); };
const hex = (c) => '#' + c.slice(0, 3).map((v) => Math.round(v).toString(16).padStart(2, '0')).join('').toUpperCase();

const NON_COLOUR_BG = /^bg-(cover|contain|center|no-repeat|repeat(-[xy])?|fixed|local|scroll|none|auto|left|right|top|bottom|clip-.*|origin-.*|gradient-.*|blend-.*|opacity-.*|linear-.*)$/;
const SHADCN = new Set(['card', 'background', 'muted', 'popover', 'primary', 'secondary', 'accent', 'surface']);
/** An element's own ground: { colour, raw } | { unresolved } | null (none painted). */
function ownGround(n) {
  if (!n || !n.attrs) return null;
  const st = String(n.attrs.style || '');
  const sm = /(?:^|;)\s*background(?:-color)?\s*:\s*([^;]+)/i.exec(st);
  if (sm) { const c = parseColour(sm[1]); if (c) return { colour: c, raw: sm[1].trim() }; }
  const tokens = String(n.attrs.class || '').split(/\s+/).filter((t) => t && !/^[^[]*:/.test(t));
  for (const t of tokens) {
    if (!/^bg-/.test(t) || NON_COLOUR_BG.test(t) || t === 'bg-transparent') continue;
    let m = /^bg-\[(?:color:)?(.+)\](?:\/(\d+))?$/.exec(t);
    let raw = null; let alpha = 1;
    if (m) { raw = m[1].replace(/_/g, ' '); if (m[2]) alpha = Number(m[2]) / 100; }
    else if ((m = /^bg-(white|black)(?:\/(\d+))?$/.exec(t))) { raw = m[1]; if (m[2]) alpha = Number(m[2]) / 100; }
    else if ((m = /^bg-([a-z]+)(?:\/(\d+))?$/.exec(t)) && SHADCN.has(m[1])) { raw = `hsl(var(--${m[1]}))`; if (m[2]) alpha = Number(m[2]) / 100; }
    else return { unresolved: t };
    if (/^url\(|^\d/.test(raw)) continue;
    const c = parseColour(raw);
    if (!c) return { unresolved: t };
    c[3] *= alpha;
    return { colour: c, raw: t };
  }
  return null;
}
/** The ground of the first element of `chain` (innermost first), alpha composited down to the page canvas. */
function groundOf(chain) {
  const canvasRaw = 'hsl(var(--bg-page))';
  const canvas = parseColour(canvasRaw);
  if (!canvas) return { unresolved: 'the page canvas --bg-page' };
  const layers = [];
  for (const n of chain) {
    const g = ownGround(n);
    if (!g) continue;
    if (g.unresolved) return { unresolved: g.unresolved };
    layers.push(g);
    if (g.colour[3] >= 1) break;
  }
  let c = canvas; let raw = 'the page canvas (--bg-page)';
  for (let i = layers.length - 1; i >= 0; i -= 1) { c = over(layers[i].colour, c); raw = layers[i].raw; }
  return { colour: c, raw };
}
/** Every axis text paint the chart is handed: [{ what, raw }]. */
function axisPaints(rc) {
  const out = [];
  const renderFill = (opt, props, fallback) => {
    let html = '';
    try { html = React.isValidElement(opt) ? L.render(() => React.cloneElement(opt, props)) : L.render(opt, props); } catch (e) { return { raw: null, err: first(e) }; }
    const tree = parse(`<svg>${html}</svg>`);
    for (const n of all(tree, (x) => x.tag === 'text' || x.tag === 'tspan')) {
      if (n.attrs.fill) return { raw: n.attrs.fill };
      const sm = /(?:^|;)\s*fill\s*:\s*([^;]+)/.exec(n.attrs.style || '');
      if (sm) return { raw: sm[1].trim() };
      const ct = String(n.attrs.class || '').split(/\s+/).map((t) => /^fill-\[(.+)\]$/.exec(t)).find(Boolean);
      if (ct) return { raw: ct[1].replace(/_/g, ' ') };
    }
    return { raw: fallback === undefined ? '#000000' : fallback };
  };
  const React = L.React;
  for (const c of rc.filter((x) => x.name === 'XAxis' || x.name === 'YAxis')) {
    const p = c.props || {};
    const axisStroke = p.stroke !== undefined ? p.stroke : '#666';
    const tick = p.tick;
    if (tick === false || p.hide) out.push({ what: `${c.name} ticks`, none: true });
    else if (tick === undefined || tick === true) out.push({ what: `${c.name} tick`, raw: axisStroke });
    else if (React.isValidElement(tick) || typeof tick === 'function') {
      const r = renderFill(tick, { x: 10, y: 10, payload: { value: '2026-09-08', coordinate: 10, index: 0 }, index: 0, fill: axisStroke, stroke: 'none', textAnchor: 'middle', fontSize: 11, visibleTicksCount: 5 }, undefined);
      out.push({ what: `${c.name} tick (custom)`, raw: r.raw, err: r.err });
    } else out.push({ what: `${c.name} tick`, raw: tick.fill !== undefined ? tick.fill : axisStroke });
    const lb = p.label;
    if (lb === undefined || lb === null || lb === false) continue;
    if (typeof lb === 'string' || typeof lb === 'number') out.push({ what: `${c.name} label`, raw: '#808080' });
    else if (React.isValidElement(lb) || typeof lb === 'function') { const r = renderFill(lb, { viewBox: { x: 0, y: 0, width: 48, height: 200 }, value: 'Articles per day' }, '#808080'); out.push({ what: `${c.name} label (custom)`, raw: r.raw, err: r.err }); }
    else out.push({ what: `${c.name} label "${lb.value === undefined ? '' : lb.value}"`, raw: lb.fill !== undefined ? lb.fill : '#808080' });
  }
  return out;
}
const MIN = 4.5;
/** paints: [{what, raw}] against one ground; faults name each paint below 4.5:1. */
function inkFaults(paints, ground) {
  const f = [];
  if (!ground || ground.unresolved) return [`GROUND: the timeline ground does not resolve (${ground ? ground.unresolved : 'none'})`];
  const drawn = paints.filter((p) => !p.none);
  if (!drawn.length) f.push('no axis text paint was handed to the chart');
  for (const p of drawn) {
    if (p.err) { f.push(`${p.what}: RENDER ${p.err}`); continue; }
    const c = p.raw === null || p.raw === undefined ? null : parseColour(p.raw);
    if (!c) { f.push(`${p.what}: the paint "${p.raw}" does not resolve to a colour`); continue; }
    const ink = c[3] < 1 ? over(c, ground.colour) : c;
    const k = contrast(ink, ground.colour);
    if (k < MIN) f.push(`${p.what}: "${p.raw}" (${hex(ink)}) on ${ground.raw} (${hex(ground.colour)}) is ${k.toFixed(2)}:1 (needs ${MIN}:1)`);
  }
  return f;
}

// ==== the header render (arm 1, and arm 3's ground) ===========================================================================
let setupError = null;
try {
  const realPanel = L.source('src/ui/components/panels/Panel.tsx').Panel;
  const cache = {};
  const panels = new Proxy({}, { get(_t, k) {
    if (k === '__esModule') return true;
    if (k === 'Panel') return realPanel;
    if (typeof k !== 'string') return undefined;
    if (!cache[k]) { const C = (p) => h('div', { 'data-stub': k }, (p || {}).children); C.displayName = k; cache[k] = C; }
    return cache[k];
  } });
  for (const k of ['src/ui/components/panels/index.ts', 'src/ui/components/panels']) L.stubSource(k, panels);
  L.stubSource(SA + 'components/TimelinePanel.tsx', { __esModule: true, TimelinePanel: (p) => h('div', { 'data-check-stub': 'TimelinePanel', 'data-security-key': (p || {}).securityKey || '' }) });
  const realBrief = L.source(SA + 'components/HeaderBrief.tsx');
  L.stubSource(SA + 'components/HeaderBrief.tsx', Object.assign({}, realBrief, { HeaderBrief: () => h('div', { 'data-check-stub': 'HeaderBrief' }) }));
} catch (e) { setupError = 'STUB SETUP: ' + first(e); }
const header = (bundle) => {
  L.hookState.impl = { useThesisBundle: () => undefined, useCollectedChatter: () => undefined, usePeerSet: () => undefined, useManagement: () => undefined };
  const m = L.source(SA + 'components/SecurityOverlay.tsx');
  return L.render(m.IdentityHeader || m.SecurityOverlay, { bundle, onBack: () => {}, onRefresh: () => {} });
};
const OVL = {};
for (const k of ['BA_US_Equity', 'VLO_US_Equity', '6501_JP_Equity']) OVL[k] = pay(readJson(`round15/fixtures/r15c.overlay.${k}.json`));
const withWindow = (ov, w) => {
  const x = clone(ov);
  const a = axisRead(x, 'BREAKOUT', 'PRICE');
  for (const row of [a && a.row, x.breakout_price]) if (row) { if (w === undefined) delete row.window_days; else row.window_days = w; }
  return x;
};
const HEADERS = [['BA', OVL.BA_US_Equity], ['VLO', OVL.VLO_US_Equity], ['6501', OVL['6501_JP_Equity']],
  ['BA PLANTED window_days 90', withWindow(OVL.BA_US_Equity, 90)], ['BA PLANTED no window_days', withWindow(OVL.BA_US_Equity, undefined)]];

const arms = [];
// ---- arm 1 ----
let baHeaderHtml = null;
{
  const f = [];
  const tally = [];
  if (setupError) f.push(setupError);
  for (const [name, ov] of HEADERS) {
    let html = null;
    try { html = header(ov); } catch (e) { f.push(`${name}: RENDER ${first(e)}`); continue; }
    if (name === 'BA') baHeaderHtml = html;
    const x = moveFaults(name, html, ov);
    f.push(...x);
    const lab = all(parse(html), (n) => /^Breakout \(price\)/.test(ownText(n)))[0];
    tally.push(`${name}: "${lab ? visible(lab.parent).replace(/^Breakout \(price\)\s*/, '').slice(0, 60) : '-'}"`);
  }
  f.push(...keepsPassing(['round29/checks/header/face.cjs']));
  arms.push(['THE HEADER MOVE NAMES ITS WINDOW: a printed breakout move says "over the last <served window_days> days"; no served window, no number; round29 face.cjs exits 0', f.length === 0,
    f.length ? `${f.length} fault(s): ${f.join(' | ')}` : `${tally.join('; ')}; round29 face.cjs exits 0`]);
}
// ---- arm 2 ----
const MODEL = readJson('round29/fixtures/model/served.BA_US_Equity.json');
const STAMPS = MODEL.versions.versions.map((v) => v.stamp);
const SERVED_CHANGED = MODEL.compare.compared.changed;
// PLANTED (labelled, round30 served.cjs's own 6 lines): sheet-scope lines with long fractions.
const PLANTED_CHANGED = [
  { figure: 'fiscal_year_line_item|2025|IS_EPS', mnemonic: 'IS_EPS', fiscal_year: 2025, scope: 'fiscal_year_line_item', from: 3.456789, to: 3.51234 },
  { figure: 'fiscal_year_line_item|2025|PE_RATIO', mnemonic: 'PE_RATIO', fiscal_year: 2025, scope: 'fiscal_year_line_item', from: 23.456789, to: 24.104321 },
  { figure: 'fiscal_year_line_item|2025|EBITDA_MARGIN', mnemonic: 'EBITDA_MARGIN', fiscal_year: 2025, scope: 'fiscal_year_line_item', from: 12.345678, to: 11.98765 },
  { figure: 'fiscal_year_line_item|2025|EBITDA', mnemonic: 'EBITDA', fiscal_year: 2025, scope: 'fiscal_year_line_item', from: 1234567.891234, to: 1301234.56789 },
  { figure: 'forecast|2027|BEST_EPS', mnemonic: 'BEST_EPS', fiscal_year: 2027, scope: 'forecast', from: 4.123456, to: 4.209871 },
  { figure: 'fiscal_year_line_item|2025|BS_CASH_NEAR_CASH_ITEM', mnemonic: 'BS_CASH_NEAR_CASH_ITEM', fiscal_year: 2025, scope: 'fiscal_year_line_item', from: 13801.123456, to: 12345.987654 },
];
const CHANGED = [...SERVED_CHANGED, ...PLANTED_CHANGED];
const COMPARE = {
  security_key: 'BA_US_Equity', available_stamps: STAMPS.slice(), read: MODEL.compare.read, reason: null,
  denominators: { versions: STAMPS.length, figures_from: 179, figures_to: 179, added: 0, removed: 0, changed: CHANGED.length, unchanged: 172 },
  compared: { from_stamp: STAMPS[STAMPS.length - 2], to_stamp: STAMPS[STAMPS.length - 1], added: [], removed: [], changed: CHANGED },
};
{
  const f = [];
  let n = 0;
  let html = '';
  try {
    L.hookState.impl = { useModelCompare: () => COMPARE, useThesisBundle: () => MODEL.thesis, useModelVersions: () => MODEL.versions, useInputLedger: () => MODEL.ledger };
    const W = L.source(SA + 'components/model/WhatChangedPanel.tsx').WhatChangedPanel;
    html = L.render(W, { securityKey: 'BA_US_Equity', stamps: STAMPS, data: MODEL.thesis, latestAbsent: false });
  } catch (e) { f.push('RENDER: ' + first(e)); }
  const ex = [];
  if (html) {
    const esc = (s) => s.replace(/&/g, '&amp;').replace(/"/g, '&quot;');
    const rows = [];
    for (const c of CHANGED) {
      const row = L.innerOf(html, 'data-what-changed-row', esc(c.figure));
      if (row === null) { f.push(`${c.mnemonic}: no [data-what-changed-row]`); continue; }
      const cell = (k) => { const x = L.innerOf(row, 'data-what-changed-cell', k); return x === null ? null : L.textOf(x); };
      rows.push({ change: c, before: cell('before'), after: cell('after'), chg: cell('change') });
    }
    const r = precisionFaults(rows);
    f.push(...r.faults);
    n = r.graded;
    for (const x of rows.filter((y) => ['SHORT_INT_RATIO', 'CUR_MKT_CAP', 'VOLUME_AVG_30D'].includes(y.change.mnemonic))) ex.push(`${x.change.mnemonic} ${x.before} -> ${x.after}: ${x.chg}`);
  }
  f.push(...keepsPassing(['round30/checks/repairs/served.cjs']));
  arms.push(["WHAT CHANGED PRINTS ITS CHANGE AT DISPLAY PRECISION: each change cell carries no digit finer than its row's before/after and is the change rounded there; round30 served.cjs exits 0", f.length === 0,
    f.length ? `${f.length} fault(s): ${f.join(' | ')}` : `${n} of ${CHANGED.length} rows at their row's precision (${ex.join('; ')}); round30 served.cjs exits 0`]);
}
// ---- arm 3 ----
function timelineGround(state, headerHtml) {
  const chart = all(state.tree, (n) => T.CHARTS.has(n.attrs['data-rc']))[0];
  if (!chart) return { unresolved: 'no recharts chart in the TimelinePanel render' };
  const chain = [];
  for (let n = chart; n && n.tag !== '#root'; n = n.parent) chain.push(n);
  if (headerHtml) {
    const mk = all(parse(headerHtml), (n) => n.attrs['data-check-stub'] === 'TimelinePanel')[0];
    if (!mk) return { unresolved: 'no TimelinePanel in the rendered IdentityHeader' };
    for (let n = mk.parent; n && n.tag !== '#root'; n = n.parent) chain.push(n);
  }
  return groundOf(chain);
}
{
  const f = [];
  let detail = '';
  const st = T.renderPanel(T.FX.rangeBA, {});
  if (/^RENDER FAILED/.test(st.html)) f.push(st.html.slice(0, 120));
  else {
    const ground = timelineGround(st, baHeaderHtml);
    const paints = axisPaints(st.rc);
    f.push(...inkFaults(paints, ground));
    if (!baHeaderHtml) f.push('the header did not render, so the ground above the timeline is unread');
    if (ground && ground.colour) {
      detail = paints.filter((p) => !p.none).map((p) => { const c = parseColour(p.raw); return c ? `${p.what} ${p.raw} ${contrast(c[3] < 1 ? over(c, ground.colour) : c, ground.colour).toFixed(2)}:1` : `${p.what} ${p.raw}`; }).join(', ') + ` on ${ground.raw} (${hex(ground.colour)})`;
    }
  }
  f.push(...keepsPassing(['round29/checks/timeline/chart.cjs']));
  arms.push(['THE TIMELINE AXIS LABELS MEET THE INK LAW: every axis tick and label paint reaches 4.5:1 on the timeline ground; round29 chart.cjs exits 0', f.length === 0,
    f.length ? `${f.length} fault(s): ${f.join(' | ')}` : `${detail}; round29 chart.cjs exits 0`]);
}
// ---- arm 4: PLANTED ----
{
  const f = [];
  let bad = 0; let rej = 0; let good = 0; let acc = 0;
  const R = (name, faults, why) => { bad += 1; if (faults.some((x) => why.test(x))) rej += 1; else f.push(`"${name}" not rejected for its reason (${faults.length ? faults[0] : 'accepted'})`); };
  const A = (name, faults) => { good += 1; if (!faults.length) acc += 1; else f.push(`"${name}" rejected: ${faults[0]}`); };
  // move predicate
  const ov = (w) => ({ axis_reads: [{ movement: 'BREAKOUT', subject: 'PRICE', row: Object.assign({ rank: 4, pct_jump_pct: 6.6503, places_moved: 3 }, w === undefined ? {} : { window_days: w }) }] });
  const hdr = (cell, extra) => `<div><div class="grid"><div><div class="text-[11px]">Breakout (price)</div><div class="text-sm">${cell}</div></div>${extra || ''}</div></div>`;
  R('a move with no window named', moveFaults('p', hdr('#4 | +6.65%, up 3 places'), ov(30)), /does not say "over the last 30 days"/);
  R('a hard-coded 30 days under a served 90', moveFaults('p', hdr('#4 | +6.65% over the last 30 days, up 3 places'), ov(90)), /names a window of 30 days; the served window_days is 90/);
  R('a move printed with no served window', moveFaults('p', hdr('#4 | +6.65%, up 3 places'), ov(undefined)), /serves no window_days/);
  R('a stray signed move elsewhere in the header', moveFaults('p', hdr('#4 | +6.65% over the last 30 days, up 3 places', '<div><span>Change</span><span>-1.20%</span></div>'), ov(30)), /the move "-1.20%" names no window/);
  A('the move with its served window', moveFaults('p', hdr('#4 | +6.65% over the last 30 days, up 3 places'), ov(30)));
  A('a 90-day window named from the field', moveFaults('p', hdr('#4 | +6.65% over the last 90 days, up 3 places'), ov(90)));
  A('no window served, no number', moveFaults('p', hdr('#4, up 3 places'), ov(undefined)));
  // precision predicate
  const row = (mn, from, to, before, after, chg) => ({ change: { mnemonic: mn, from, to }, before, after, chg });
  const SIR = ['SHORT_INT_RATIO', 2.903939, 3.036011, '2.90', '3.04'];
  const MCAP = ['CUR_MKT_CAP', 161867780096.00003, 155544819936, 'USD 162B', 'USD 156B'];
  const VOL = ['VOLUME_AVG_30D', 5518752.5, 6035900.5, '5.52M', '6.04M'];
  const SIP = ['SI_PERCENT_EQUITY_FLOAT', 2.016643, 1.800129, '2.0%', '1.8%'];
  R('"+0.1321" against 2.90 -> 3.04', precisionFaults([row(...SIR, '+0.1321')]).faults, /digit finer/);
  R('"+0.1" (coarser) against 2.90 -> 3.04', precisionFaults([row(...SIR, '+0.1')]).faults, /not the change at the row's precision/);
  R('"-USD 6.32B" against USD 162B -> USD 156B', precisionFaults([row(...MCAP, '-USD 6.32B')]).faults, /digit finer/);
  R('"+517K" against 5.52M -> 6.04M', precisionFaults([row(...VOL, '+517K')]).faults, /digit finer/);
  R('"-0.22 pts" against 2.0% -> 1.8%', precisionFaults([row(...SIP, '-0.22 pts')]).faults, /digit finer/);
  A('"+0.13" (the change rounded)', precisionFaults([row(...SIR, '+0.13')]).faults);
  A('"+0.14" (after minus before as printed)', precisionFaults([row(...SIR, '+0.14')]).faults);
  A('"-USD 6B"', precisionFaults([row(...MCAP, '-USD 6B')]).faults);
  A('"+0.52M"', precisionFaults([row(...VOL, '+0.52M')]).faults);
  A('"-0.2 pts"', precisionFaults([row(...SIP, '-0.2 pts')]).faults);
  // ink predicate
  const surface = groundOf([{ attrs: { class: 'w-full rounded-[4px] border bg-[hsl(var(--bg-surface))]' } }]);
  const band = groundOf([{ attrs: { class: 'w-full dark-band bg-[hsl(var(--bg-band))]' } }]);
  const tickP = (raw) => [{ what: 'XAxis tick', raw }];
  R('#A8B0C0 ticks on the white surface', inkFaults(tickP('#A8B0C0'), surface), /is 2\.1\d:1 \(needs 4\.5:1\)/);
  R('the palette-mediumGray token on the white surface', inkFaults(tickP('hsl(var(--palette-mediumGray))'), surface), /:1 \(needs 4\.5:1\)/);
  R("recharts' default label grey #808080 on the white surface", inkFaults([{ what: 'YAxis label', raw: '#808080' }], surface), /is 3\.9\d:1/);
  R('navy ink on the band ground', inkFaults(tickP('hsl(var(--palette-navy))'), band), /:1 \(needs 4\.5:1\)/);
  R('a token that does not resolve', inkFaults(tickP('hsl(var(--no-such-token))'), surface), /does not resolve to a colour/);
  A('navy ink on the white surface', inkFaults(tickP('hsl(var(--palette-navy))'), surface));
  A("recharts' default tick #666 on the white surface", inkFaults(tickP('#666'), surface));
  A('the darkGray token on the white surface', inkFaults(tickP('hsl(var(--palette-darkGray))'), surface));
  arms.push(['PLANTED: the move, precision and ink predicates reject their planted faults, each for its own reason, and accept the good shapes', f.length === 0,
    f.length ? f.join(' | ') : `${rej} of ${bad} bad inputs rejected for their reason (4 move, 5 precision, 5 ink); ${acc} of ${good} good inputs accepted (3 + 5 + 3)`]);
}

let pass = 0;
for (const [n, ok, d] of arms) { if (ok) pass += 1; console.log(`${ok ? 'ARM PASS' : 'ARM FAIL'} ${n} :: ${d}`); }
console.log(`A MOVE NAMES ITS WINDOW, A CHANGE ITS PRECISION, THE AXIS ITS INK: ${pass} of 4 arms`);
process.exit(pass === 4 ? 0 : 1);
