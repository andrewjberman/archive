/**
 * repairs36.cjs -- DSGN_AMGTV1 round 36, the batched REPAIR CELL check (issuer 2.0.0_SA_COO~D): THE LIST READS AT 11PX, THE
 * TOOLTIP NAMES ITS HEADLINE, NO ZERO MOVE.
 *
 * Usage (from the directory whose portal/ is the checkout under test -- the repository root for a worker,
 *   `cd "$(git rev-parse --show-toplevel)" && node "org/missions/D13/DSGN/DSGN_AMGTV1/deliverables/2.0.0_SA_COO~D/round36/checks/
 *   repairs/repairs36.cjs"`; C:/tmp/wk-dsgn-amgtv1-92 for the issuer). Fixtures resolve from this file's own location; the portal
 *   resolves from the cwd (cwd/portal).
 *   ISSUER GREEN ARM: CHECK_SRC_OVERRIDE (round15/checks/_load.cjs) is honoured for every render and every source read here; the
 *   render child (_render36.cjs beside this file) and the KEEP children inherit the same environment. A worker never sets it.
 * Why (three faults, one batched repair cell):
 *   1 FWD-20 "no size below 11px; radii within {2,3,4,pill}": a render-instrument run on the Universe/list state of
 *     portal/src/pages/SecurityAnalysis (the Lead Panel) measured font sizes 8, 9 and 10 px and a 5px border radius. At base
 *     35a723bf the list state renders LeadPanel.tsx -> ChatterBubbles.tsx (Subject Chatter) or PriceBars.tsx (Subject Price); the
 *     bubble labels are SVG <text font-size={label.fs}> placed at 15..8 inside a bubble, 10/9/8 beside it and 8 as a last resort,
 *     and the no-tone legend swatch is style borderRadius 5 (a 10px box). The source lines print in the INFO census line.
 *   2 FWD-5: components/TimelinePanel.tsx DayTooltip prints `body?.articles?.[0]?.headline ?? covering?.lead_headline` under the
 *     label "Strongest headline": until the day route answers, the reader is told the coverage event's lead headline is the day's
 *     strongest headline, which it is not.
 *   3 components/model/WhatChangedPanel.tsx movement(): a percent move that rounds to zero at its printed precision prints with a
 *     sign, "-0.00%" / "+0.00%" (BA capital expenditure 2027 -3,979.67 -> -3,979.78; free cash flow 2027/2028).
 * Renders (all in the child _render36.cjs, one process per mode; the REAL page sources through round15/checks/_load.cjs):
 *   list     round31/checks/presets/_presets.cjs: the REAL LeadPanel, ChatterBubbles and PriceBars (round29 leadprice/_render.cjs
 *            stubs; the REAL shared Panel / PanelContent / GraphicCard), each window preset 30/90/365 selected through the control's
 *            own onChange, Subject CHATTER and PRICE, over round31/fixtures/windows.{chatter,price}.{30,90,365}.json.
 *   tip      round29/checks/timeline/_tl.cjs: the REAL TimelinePanel; its Tooltip `content` cloned with the day's served series
 *            entry and rendered (round29 timeline/chart.cjs's method); a day absent from the day map reads PENDING (isLoading).
 *   changed  the REAL tabs/ModelTab.tsx over round35/fixtures/{compare,thesis,versions}.BA_US_Equity.json (changed35's path).
 * Definitions:
 *   FONT SIZE of an element (arm 1): each Tailwind v4 class (variant prefixes such as md: / hover: stripped) text-xs 12, text-sm
 *     14, text-base 16, text-lg 18, text-xl 20, text-2xl..9xl; text-[N px|rem|em] (rem and em at 16); an inline style font-size in
 *     px/rem/em; an SVG font-size attribute (user units read as px, the size the instrument reports). Below 11 is a fault.
 *   RADIUS (arm 1): each rounded / rounded-<side> class (none 0, xs 2, sm 4, bare 4, md 6, lg 8, xl 12, 2xl 16, 3xl 24, 4xl 32,
 *     full PILL, [arbitrary]); an inline style border-radius / border-*-radius (each value); an SVG rx / ry attribute. Allowed:
 *     0 (no radius), 2, 3, 4 px, and PILL (>= 9999px, 50% or more, rounded-full, var(--radius-pill) / var(--radius-circle));
 *     var(--radius-hairline) 2, var(--radius-control) 3, var(--radius) 4 (portal/src/index.css). A <circle>'s r is not a radius.
 *   OWNERSHIP (arm 1): a CLASS offender is SHARED when its token appears in no page-owned source the list render loaded
 *     (src/pages/SecurityAnalysis/**) but in a shared one (src/ui/**, src/components/**, src/lib/**): reported, NOT graded. Every
 *     other class offender, and every inline-style and SVG-attribute offender, is graded as page-owned.
 *   PENDING (arm 2): the day route has not answered (the query stub reads isLoading). COVERING: every served event whose
 *     [first_day, last_day] holds the day. A "Strongest headline" row is a tooltip row whose label contains "strongest".
 *   ZERO MOVE (arm 3): a percent token whose digits are all zero printed with a sign: /[+-\u2212]\s*0(\.0+)?\s*%/ (so "-0.00%",
 *     "+0.00%", "-0.0%", "+0%"), in any of the row's four cells.
 * Arms:
 *   1  LIST AT 11PX, RADII IN THE SET: on CHATTER and PRICE at 30, 90 and 365 days, the rendered list state carries no page-owned
 *      font size below 11px and no page-owned radius outside {0,2,3,4,PILL}; every render exists, and the Chatter renders draw
 *      at least one bubble label (else NOT_EXERCISED, a FAIL). Prints the offenders per render and the SHARED ones.
 *   2  THE TOOLTIP NAMES ITS HEADLINE: BA 2026-09-28 and 2026-09-29 (round35 served range) and 2026-09-08 (round14 served range),
 *      each with articles and a covering event, rendered with the day read PENDING: the shared DataTooltip renders and no
 *      "Strongest headline" row carries a covering event's lead headline. KEEP the loaded behaviour: BA 2026-09-08 with the
 *      SERVED day read (round14/fixtures/timelineDay.BA_US_Equity.2026-09-08.json) and BA 2026-09-28 with a PLANTED day read
 *      (labelled, in _render36.cjs) each print the day route's first article headline under "Strongest headline".
 *   3  NO ZERO MOVE: all 37 served changed rows render and no cell prints a ZERO MOVE.
 *   4  KEEP: round35 changed35.cjs, cloud35.cjs, payload35.cjs; round34 labels34.cjs, repairs34.cjs; round29 timeline/chart.cjs
 *      exit 0 on the same tree.
 *   5  PLANTED: arm 1's grader flags a planted text-[9px], a planted rounded-[5px], an SVG font-size 8 and a style border-radius
 *      5px, and accepts a clean set (text-xs, rounded-[4px], rounded-full, border-radius 50%, rounded-b-[3px], md:text-sm, SVG
 *      font-size 11, rx 2); arm 1's ownership split reads a token found only in a shared source as SHARED; arm 2's grader flags a
 *      pending tooltip printing the event headline under "Strongest headline" and a loaded one printing the wrong headline, and
 *      accepts "loading" plus a labelled fallback row; arm 3's grader flags "-0.00%" and "+0.0%" and accepts "0.00%", "-0.05%"
 *      and "-<0.01%".
 * Blind spots: a static render, no CSS cascade: an INHERITED size (a parent's class) and the browser default 16px are not
 *   graded, and Tailwind sizes are read from the class name, not from computed style; em is read at 16. Shared estate components
 *   the loader stubs (Segmented, PanelEmpty/PanelLoading, PanelEyebrow, GraphicPanel, lucide icons) render no own styling, so their
 *   sizes and radii are not seen; recharts is stubbed, so a tick fontSize passed to it is not rendered (RankedChart.tsx is not
 *   mounted by the list state at base; its source lines print in the census only). Ownership is by literal token, so a shared
 *   component's inline style would be graded as page-owned (none at base). The PRICE face at 90/365 renders its served window
 *   reason only (the fixtures serve no rows there); the expanded price list and Starred-only are not rendered. Arm 2 grades the
 *   label's text, not its meaning beyond the lead headline; a day read that answers with an error is not graded.
 * Prints an INFO census line, one line per arm, and "THE LIST READS AT 11PX, THE TOOLTIP NAMES ITS HEADLINE, NO ZERO MOVE: <k>
 * of 5 arms"; exit 0 only at 5 of 5. Static renders only; no network, no AWS, writes no file.
 */
const fs = require('fs');
const path = require('path');
const { spawnSync } = require('child_process');

const DROOT = path.join(__dirname, '..', '..', '..');
const PORTAL = path.join(process.cwd(), 'portal');
const SA = 'src/pages/SecurityAnalysis/';
const TITLE = 'THE LIST READS AT 11PX, THE TOOLTIP NAMES ITS HEADLINE, NO ZERO MOVE';
const norm = (s) => String(s === null || s === undefined ? '' : s).replace(/\s+/g, ' ').trim();
const MIN_PX = 11;
const PILL = 'PILL';

if (!fs.existsSync(path.join(PORTAL, 'package.json'))) {
  console.log('LOADER ERROR: no portal/package.json under ' + process.cwd() + ' -- run from the directory whose portal/ is under test');
  process.exit(3);
}

// ---- sources (override-aware) ----------------------------------------------------------------------------------------------
const OVERRIDES = {};
for (const pair of (process.env.CHECK_SRC_OVERRIDE || '').split(';').filter(Boolean)) {
  const i = pair.indexOf('=');
  OVERRIDES[pair.slice(0, i)] = pair.slice(i + 1);
}
function readSource(rel) {
  const f = OVERRIDES[rel] || path.join(PORTAL, rel);
  try { return fs.readFileSync(f, 'utf8'); } catch (e) { return null; }
}

// ---- the render child --------------------------------------------------------------------------------------------------------
function child(mode) {
  const r = spawnSync(process.execPath, [path.join(__dirname, '_render36.cjs'), mode], { cwd: process.cwd(), env: process.env, encoding: 'utf8', timeout: 600000, maxBuffer: 256 * 1024 * 1024 });
  const lines = String(r.stdout || '').split('\n').filter((x) => x.startsWith('{'));
  if (!lines.length) return { error: `the ${mode} render child printed no result (rc=${r.status}; ${norm(String(r.stderr || r.stdout || '')).slice(0, 160)})` };
  try { return JSON.parse(lines[lines.length - 1]); } catch (e) { return { error: `the ${mode} render child printed unreadable JSON` }; }
}

// ---- a small markup tree (react-dom/server output is well formed) -----------------------------------------------------------
const VOID = new Set(['area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'source', 'track', 'wbr']);
const decode = (s) => String(s).replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&quot;/g, '"').replace(/&#x27;/g, "'").replace(/&#39;/g, "'").replace(/&nbsp;/g, ' ').replace(/&amp;/g, '&');
function parse(html) {
  const root = { tag: '#root', attrs: {}, children: [], parent: null };
  let cur = root;
  const re = /<!--[\s\S]*?-->|<\/([a-zA-Z][\w:.-]*)\s*>|<([a-zA-Z][\w:.-]*)((?:\s+[^\s=>\/]+(?:="[^"]*")?)*)\s*(\/?)>|([^<]+)/g;
  let m;
  while ((m = re.exec(html)) !== null) {
    if (m[1]) { let n = cur; while (n && n.tag !== m[1].toLowerCase()) n = n.parent; if (n && n.parent) cur = n.parent; }
    else if (m[2]) {
      const attrs = {};
      const ar = /([^\s=>\/]+)(?:="([^"]*)")?/g;
      let a;
      while ((a = ar.exec(m[3] || '')) !== null) attrs[a[1]] = a[2] === undefined ? '' : decode(a[2]);
      const node = { tag: m[2].toLowerCase(), attrs, children: [], parent: cur };
      cur.children.push(node);
      if (!m[4] && !VOID.has(node.tag)) cur = node;
    } else if (m[5]) cur.children.push({ text: decode(m[5]), parent: cur });
  }
  return root;
}
function all(node, pred, out) {
  out = out || [];
  for (const c of node.children || []) if (c.tag) { if (pred(c)) out.push(c); all(c, pred, out); }
  return out;
}
const textOf = (node) => (node.text !== undefined ? node.text : (node.children || []).map(textOf).join(' '));

// ==== arm 1 grader: sizes and radii of a rendered markup ======================================================================
const TW_TEXT = { xs: 12, sm: 14, base: 16, lg: 18, xl: 20, '2xl': 24, '3xl': 30, '4xl': 36, '5xl': 48, '6xl': 60, '7xl': 72, '8xl': 96, '9xl': 128 };
const TW_RADIUS = { none: 0, xs: 2, sm: 4, '': 4, md: 6, lg: 8, xl: 12, '2xl': 16, '3xl': 24, '4xl': 32, full: PILL };
const RADIUS_VARS = { '--radius-hairline': 2, '--radius-control': 3, '--radius': 4, '--radius-pill': PILL, '--radius-circle': PILL };
/** The utility of a class token with its variant prefixes (md:, hover:, ...) removed; colons inside [...] are kept. */
function utility(tok) {
  let depth = 0;
  let cut = 0;
  for (let i = 0; i < tok.length; i += 1) {
    const ch = tok[i];
    if (ch === '[') depth += 1;
    else if (ch === ']') depth -= 1;
    else if (ch === ':' && depth === 0) cut = i + 1;
  }
  return tok.slice(cut).replace(/^!/, '');
}
/** A CSS length as px, PILL, or null when it does not resolve. */
function lengthPx(v) {
  const s = String(v).trim().toLowerCase().replace(/\s+/g, '');
  let m;
  if ((m = /^var\((--[a-z0-9-]+)\)$/.exec(s)) && RADIUS_VARS[m[1]] !== undefined) return RADIUS_VARS[m[1]];
  if (/^calc\(infinity\*1px\)$/.test(s)) return PILL;
  if ((m = /^(-?[\d.]+)px$/.exec(s))) return Number(m[1]) >= 9999 ? PILL : Number(m[1]);
  if ((m = /^(-?[\d.]+)(rem|em)$/.exec(s))) return Number(m[1]) * 16 >= 9999 ? PILL : Number(m[1]) * 16;
  if ((m = /^(-?[\d.]+)%$/.exec(s))) return Number(m[1]) >= 50 ? PILL : `${m[1]}%`;
  if ((m = /^(-?[\d.]+)$/.exec(s))) return Number(m[1]) >= 9999 ? PILL : Number(m[1]);
  return null;
}
const radiusOk = (px) => px === PILL || px === 0 || px === 2 || px === 3 || px === 4;
const fmt = (px) => (px === PILL ? 'pill' : typeof px === 'number' ? `${px}px` : String(px));
/** Every size/radius declaration an element carries: [{kind: 'font'|'radius', via, token, px}]. */
function declsOf(n) {
  const out = [];
  for (const raw of String(n.attrs.class || '').split(/\s+/).filter(Boolean)) {
    const u = utility(raw);
    let m;
    if ((m = /^text-(xs|sm|base|lg|xl|[2-9]xl)(?:\/.*)?$/.exec(u))) out.push({ kind: 'font', via: 'class', token: raw, px: TW_TEXT[m[1]] });
    else if ((m = /^text-\[(?:length:)?([^\]]+)\](?:\/.*)?$/.exec(u))) {
      const px = lengthPx(m[1]);
      if (typeof px === 'number') out.push({ kind: 'font', via: 'class', token: raw, px });
    } else if ((m = /^rounded(?:-(t|r|b|l|s|e|tl|tr|br|bl|ss|se|es|ee))?(?:-(.+))?$/.exec(u))) {
      const size = m[2] === undefined ? '' : m[2];
      let px;
      if (TW_RADIUS[size] !== undefined) px = TW_RADIUS[size];
      else if (/^\[.*\]$/.test(size)) px = lengthPx(size.slice(1, -1));
      else px = null;
      out.push({ kind: 'radius', via: 'class', token: raw, px: px === null ? `unresolved "${size}"` : px });
    }
  }
  const style = String(n.attrs.style || '');
  for (const d of style.split(';')) {
    const i = d.indexOf(':');
    if (i < 0) continue;
    const prop = d.slice(0, i).trim().toLowerCase();
    const val = d.slice(i + 1).trim();
    if (prop === 'font-size') {
      const px = lengthPx(val);
      if (typeof px === 'number') out.push({ kind: 'font', via: 'style', token: `font-size:${val}`, px });
    } else if (/^border(-(top|bottom)-(left|right)|-(start|end)-(start|end))?-radius$/.test(prop)) {
      for (const part of val.split('/').join(' ').split(/\s+/).filter(Boolean)) {
        const px = lengthPx(part);
        out.push({ kind: 'radius', via: 'style', token: `${prop}:${val}`, px: px === null ? `unresolved "${part}"` : px });
      }
    }
  }
  if (n.attrs['font-size'] !== undefined) {
    const px = lengthPx(n.attrs['font-size']);
    if (typeof px === 'number') out.push({ kind: 'font', via: 'svg', token: `<${n.tag} font-size="${n.attrs['font-size']}">`, px });
  }
  for (const a of ['rx', 'ry']) {
    if (n.attrs[a] !== undefined && n.tag !== 'ellipse') {
      const px = lengthPx(n.attrs[a]);
      out.push({ kind: 'radius', via: 'svg', token: `<${n.tag} ${a}="${n.attrs[a]}">`, px: px === null ? `unresolved "${n.attrs[a]}"` : px });
    }
  }
  return out;
}
/** Offenders of one markup: [{kind, via, token, px, text}]. */
function offendersOf(html) {
  const off = [];
  for (const n of all(parse(html), () => true)) {
    for (const d of declsOf(n)) {
      const bad = d.kind === 'font' ? d.px < MIN_PX : !radiusOk(d.px);
      if (bad) off.push({ ...d, text: norm(textOf(n)).slice(0, 40) });
    }
  }
  return off;
}
/** Splits class offenders into page-owned and SHARED by where their token is written. sources = {page: {rel: text}, shared: {...}}. */
function ownerOf(o, sources) {
  if (o.via !== 'class') return 'page';
  const tok = utility(o.token);
  const inAny = (set) => Object.values(set).some((t) => t && t.includes(tok));
  if (inAny(sources.page)) return 'page';
  if (inAny(sources.shared)) return 'shared';
  return 'page';
}
/** Arm 1 grader over one render: { graded: [...], shared: [...] }. */
function listFaults(html, sources) {
  const graded = [];
  const shared = [];
  for (const o of offendersOf(html)) (ownerOf(o, sources) === 'shared' ? shared : graded).push(o);
  return { graded, shared };
}
/** "svg <text font-size> 8px x4 ("Name"), ..." */
function summarise(offs) {
  const by = new Map();
  for (const o of offs) {
    const k = `${o.kind === 'font' ? 'size' : 'radius'} ${fmt(o.px)} via ${o.via === 'svg' ? o.token.replace(/="[^"]*"/, '') : o.via === 'style' ? o.token.split(':')[0] : o.token}`;
    if (!by.has(k)) by.set(k, { n: 0, text: o.text });
    by.get(k).n += 1;
  }
  return [...by].map(([k, v]) => `${k} x${v.n}${v.text ? ` (e.g. "${v.text}")` : ''}`).join(', ');
}

// ==== the INFO census: the page-owned source lines that write a size below 11 or a radius outside the set ====================
const CENSUS = [
  [/text-\[(\d+(?:\.\d+)?)px\]/g, (v) => Number(v) < MIN_PX],
  [/rounded(?:-(?:t|r|b|l|s|e|tl|tr|br|bl))?-\[([^\]]+)\]/g, (v) => !radiusOk(lengthPx(v))],
  [/\brounded(?:-(?:t|r|b|l|s|e|tl|tr|br|bl))?-(md|lg|xl|2xl|3xl|4xl)\b/g, () => true],
  [/fontSize\s*[=:]\s*\{?\s*(\d+(?:\.\d+)?)/g, (v) => Number(v) < MIN_PX],
  [/font-size\s*[=:]\s*["']?(\d+(?:\.\d+)?)/g, (v) => Number(v) < MIN_PX],
  [/borderRadius\s*:\s*(\d+(?:\.\d+)?)/g, (v) => !radiusOk(Number(v))],
  [/\brx=\{?\s*["']?(\d+(?:\.\d+)?)/g, (v) => !radiusOk(Number(v))],
  [/\bfs\s*(?::|=|>=)\s*(\d+(?:\.\d+)?)/g, (v) => Number(v) < MIN_PX],
  [/\bfs of \[([\d.,\s]+)\]/g, (v) => v.split(',').some((x) => Number(x) < MIN_PX)],
];
function census(rel, text) {
  const hits = [];
  String(text || '').split(/\r?\n/).forEach((line, i) => {
    if (/^\s*(\*|\/\/|\/\*)/.test(line)) return;
    for (const [re, bad] of CENSUS) {
      re.lastIndex = 0;
      let m;
      while ((m = re.exec(line)) !== null) if (bad(m[1])) hits.push(`${rel.replace(SA, '')}:${i + 1} ${m[0].trim()}`);
    }
  });
  return hits;
}

// ==== arm 2 grader: the tooltip's strongest-headline row =====================================================================
/** c = {name, pending, rows: [{label, value}] | null, covering: [lead headlines], want, stop}. */
function tipFaults(c) {
  if (c.stop) return [`${c.name}: ${c.stop}`];
  if (!c.rows) return [`${c.name}: no shared DataTooltip rendered`];
  const strong = c.rows.filter((r) => /strongest/i.test(r.label));
  const f = [];
  if (c.pending) {
    if (!c.covering || !c.covering.length) return [`${c.name}: NOT_EXERCISED (no served event covers the day)`];
    for (const r of strong) {
      const lead = c.covering.find((h) => norm(r.value).toLowerCase().includes(norm(h).toLowerCase()));
      if (lead) f.push(`${c.name}: "${r.label}" prints the coverage event's lead headline "${norm(lead).slice(0, 60)}" while the day read is pending`);
    }
  } else {
    if (!strong.length) f.push(`${c.name}: no "Strongest headline" row once the day read answered`);
    else if (!strong.some((r) => norm(r.value).toLowerCase().includes(norm(c.want).toLowerCase()))) f.push(`${c.name}: "${strong[0].label}" prints "${norm(strong[0].value).slice(0, 60)}", the day route's first headline "${norm(c.want).slice(0, 60)}" wanted`);
  }
  return f;
}
const tipShown = (c) => {
  const s = (c.rows || []).filter((r) => /strongest/i.test(r.label)).map((r) => `"${r.label}: ${norm(r.value).slice(0, 50)}"`);
  const other = (c.rows || []).filter((r) => !/strongest|^articles$|publishers|mentions|^search$/i.test(r.label)).map((r) => `"${r.label}: ${norm(r.value).slice(0, 40)}"`);
  return `${c.name.replace(/ \(round \d+ served range\)/, '')} -> ${s.join(' ') || 'no strongest row'}${other.length ? ' + ' + other.join(' ') : ''}`;
};

// ==== arm 3 grader: no signed zero percent ====================================================================================
const ZERO = /(^|[^\d.,])([+\-\u2212]\s*0(?:\.0+)?\s*%)/;
const CELLS = ['before', 'after', 'chg', 'pct'];
const rowLabel = (r) => `${r.mnemonic}${r.fiscal_year !== null && r.fiscal_year !== undefined ? ' ' + r.fiscal_year : ''}`;
function zeroMoveFaults(rows) {
  const f = [];
  for (const r of rows) for (const k of CELLS) {
    const m = ZERO.exec(norm(r[k]));
    if (m) f.push(`${rowLabel(r)} ${norm(r.before)} -> ${norm(r.after)}: ${k === 'chg' ? 'change' : k} cell prints "${m[2]}"`);
  }
  return f;
}

function keepsPassing(rels) {
  const faults = [];
  for (const rel of rels) {
    const r = spawnSync(process.execPath, [path.join(DROOT, rel)], { cwd: process.cwd(), env: process.env, encoding: 'utf8', timeout: 900000 });
    const last = ((r.stdout || '') + (r.stderr || '')).trim().split('\n').pop() || '';
    if (r.status !== 0) faults.push(`KEEP: ${rel} rc=${r.status} ("${last.slice(0, 100)}")`);
  }
  return faults;
}

// ==== renders ===================================================================================================================
const LIST = child('list');
const TIP = child('tip');
const CHG = child('changed');

// The sources the list render loaded, split page-owned / shared, plus the named Lead Panel files (census only).
const NAMED = ['LeadPanel.tsx', 'RankedList.tsx', 'RankedChart.tsx', 'StarredList.tsx', 'ChatterBubbles.tsx', 'PriceBars.tsx'].map((f) => SA + 'components/' + f);
const reads = (LIST.reads || []).filter((r) => /\.(tsx?|jsx?)$/.test(r));
const SOURCES = { page: {}, shared: {} };
for (const rel of reads) {
  if (rel.startsWith(SA)) SOURCES.page[rel] = readSource(rel);
  else if (/^src\/(ui|components|lib)\//.test(rel)) SOURCES.shared[rel] = readSource(rel);
}
{
  const hits = [];
  const notLoaded = NAMED.filter((r) => !reads.includes(r));
  for (const rel of [...new Set([...Object.keys(SOURCES.page), ...NAMED])]) {
    const h = census(rel, SOURCES.page[rel] !== undefined ? SOURCES.page[rel] : readSource(rel));
    hits.push(...h.map((x) => (reads.includes(rel) ? x : `${x} [not loaded by the list render]`)));
  }
  console.log(`INFO list-state source census (not graded; ${Object.keys(SOURCES.page).length} page-owned and ${Object.keys(SOURCES.shared).length} shared sources loaded; named but not loaded: ${notLoaded.map((r) => r.replace(SA + 'components/', '')).join(', ') || 'none'}): ${hits.length} line(s)${hits.length ? ': ' + hits.join(' | ') : ''}`);
}

const arms = [];
// ---- arm 1 ----
{
  const f = [];
  const tally = [];
  const sharedAll = [];
  if (LIST.error) f.push(LIST.error);
  const renders = LIST.renders || [];
  if (!LIST.error && renders.length !== 6) f.push(`${renders.length} of 6 list renders`);
  for (const r of renders) {
    if (!r.html) { f.push(`${r.name}: no render (${r.stop})`); continue; }
    const g = listFaults(r.html, SOURCES);
    if (r.subject === 'CHATTER' && !/<text\b[^>]*data-bubble-label=/.test(r.html)) f.push(`${r.name}: NOT_EXERCISED (no bubble label drawn)`);
    if (g.graded.length) f.push(`${r.name}: ${g.graded.length} offender(s): ${summarise(g.graded)}`);
    sharedAll.push(...g.shared.map((o) => `${o.token} (${fmt(o.px)})`));
    const fonts = all(parse(r.html), () => true).flatMap(declsOf).filter((d) => d.kind === 'font').map((d) => d.px);
    tally.push(`${r.name} ${fonts.length ? Math.min(...fonts) : '-'}px min`);
  }
  const sh = [...new Set(sharedAll)];
  const shared = sh.length ? `; SHARED (not graded): ${sh.join(', ')} in ${Object.keys(SOURCES.shared).filter((rel) => sh.some((t) => SOURCES.shared[rel] && SOURCES.shared[rel].includes(utility(t.split(' ')[0])))).map((x) => x.replace(/^src\//, '')).join(', ')}` : '; SHARED: none';
  arms.push(['LIST AT 11PX, RADII IN THE SET: the rendered Chatter and Price list state at 30/90/365 days carries no page-owned size below 11px and no radius outside {0,2,3,4,pill}', f.length === 0,
    (f.length ? `${f.length} fault(s): ${f.join(' | ')}` : `0 page-owned offenders over ${renders.length} renders (${tally.join('; ')})`) + shared]);
}
// ---- arm 2 ----
{
  const f = [];
  if (TIP.error) f.push(TIP.error);
  const cases = TIP.cases || [];
  if (!TIP.error && cases.length !== 5) f.push(`${cases.length} of 5 tooltip cases rendered`);
  for (const c of cases) f.push(...tipFaults(c));
  arms.push(['THE TOOLTIP NAMES ITS HEADLINE: while the day read is pending no "Strongest headline" carries the coverage event\'s lead headline; once answered it carries the day route\'s first headline', f.length === 0,
    f.length ? `${f.length} fault(s): ${f.join(' | ')}` : `${cases.length} of ${cases.length} cases: ${cases.map(tipShown).join('; ')}`]);
}
// ---- arm 3 ----
{
  const f = [];
  if (CHG.error) f.push(CHG.error);
  const rows = CHG.rows || [];
  if (!CHG.error && CHG.served !== 37) f.push(`FIXTURE: compare.BA_US_Equity.json serves ${CHG.served} changed rows (want 37)`);
  if ((CHG.missing || []).length) f.push(`${CHG.missing.length} of ${CHG.served} served changed rows not rendered (first ${CHG.missing[0]})`);
  if (!CHG.error && rows.length === 0) f.push('NOT_EXERCISED: no changed row rendered');
  const z = zeroMoveFaults(rows);
  if (z.length) f.push(`${z.length} zero move(s): ${z.join(' | ')}`);
  const small = rows.filter((r) => { const v = Number(String(r.pct || '').replace(/[^\d.]/g, '')); return /\d/.test(r.pct || '') && v < 0.01; }).map((r) => `${rowLabel(r)} "${norm(r.pct)}"`);
  arms.push(['NO ZERO MOVE: all 37 served changed rows render and no cell prints "-0.00%", "+0.00%", "-0.0%" or "+0.0%"', f.length === 0,
    f.length ? f.join(' | ') : `0 of ${rows.length} rows print a signed zero percent; the rows that round to zero print ${small.join(', ') || '(none)'}`]);
}
// ---- arm 4: KEEP ----
{
  const KEEP = ['round35/checks/changed/changed35.cjs', 'round35/checks/cloud/cloud35.cjs', 'round35/checks/words/payload35.cjs',
    'round34/checks/collage/labels34.cjs', 'round34/checks/repairs/repairs34.cjs', 'round29/checks/timeline/chart.cjs'];
  const f = keepsPassing(KEEP);
  arms.push(['KEEP: round35 changed35/cloud35/payload35, round34 labels34/repairs34 and round29 timeline/chart.cjs exit 0 on the same tree', f.length === 0,
    f.length ? f.join(' | ') : `${KEEP.length} of ${KEEP.length} exit 0`]);
}
// ---- arm 5: PLANTED ----
{
  const f = [];
  let bad = 0; let rej = 0; let good = 0; let acc = 0;
  const R = (label, faults, why) => { bad += 1; if (faults.some((x) => why.test(x))) rej += 1; else f.push(`"${label}" not flagged for its reason (${faults.length ? faults[0] : 'accepted'})`); };
  const A = (label, faults) => { good += 1; if (!faults.length) acc += 1; else f.push(`"${label}" rejected: ${faults[0]}`); };
  const NOSRC = { page: {}, shared: {} };
  const asText = (html, src) => listFaults(html, src || NOSRC).graded.map((o) => `${o.kind} ${fmt(o.px)} ${o.token}`);
  const CLEAN = '<div class="rounded-[4px] text-xs"><span class="rounded-full">a</span><span style="border-radius:50%;font-size:11px">b</span>'
    + '<svg viewBox="0 0 10 10"><circle r="3" cx="5" cy="5"></circle><text font-size="11">c</text><rect rx="2" ry="2"></rect></svg>'
    + '<div class="rounded-b-[3px] md:text-sm hover:rounded-sm">d</div><p class="text-[hsl(var(--palette-navy))]">e</p></div>';
  A('a clean list markup (arm 1)', asText(CLEAN));
  R('a planted text-[9px]', asText(CLEAN.replace('<p class="', '<p class="text-[9px] ')), /^font 9px text-\[9px\]/);
  R('a planted rounded-[5px]', asText(CLEAN.replace('<p class="', '<p class="rounded-[5px] ')), /^radius 5px rounded-\[5px\]/);
  R('a planted SVG font-size 8', asText(CLEAN.replace('<text font-size="11">', '<text font-size="8">')), /^font 8px <text font-size="8">/);
  R('a planted style border-radius 5px', asText(CLEAN.replace('border-radius:50%', 'border-radius:5px')), /^radius 5px border-radius:5px/);
  {
    const html = CLEAN.replace('<p class="', '<p class="rounded-b-lg ');
    const g = listFaults(html, { page: { 'src/pages/SecurityAnalysis/x.tsx': 'className="text-xs"' }, shared: { 'src/ui/components/panels/PanelContent.tsx': "'p-[30px] rounded-b-lg'" } });
    good += 1;
    if (g.graded.length === 0 && g.shared.length === 1 && g.shared[0].token === 'rounded-b-lg') acc += 1;
    else f.push(`ownership: a token written only in a shared source did not read as SHARED (${g.graded.length} graded, ${g.shared.length} shared)`);
    const g2 = listFaults(html, { page: { 'src/pages/SecurityAnalysis/x.tsx': 'className="rounded-b-lg"' }, shared: { 'src/ui/components/panels/PanelContent.tsx': "'p-[30px] rounded-b-lg'" } });
    bad += 1;
    if (g2.graded.length === 1) rej += 1;
    else f.push('ownership: a token written in a page-owned source was not graded');
  }
  // arm 2's grader
  const LEAD = 'China moves closer to finalizing 200-jet Boeing order';
  const base = [{ label: 'Articles', value: '7' }, { label: 'Distinct publishers', value: '3' }, { label: 'Mentions', value: '68' }];
  const tc = (pending, rows, want) => ({ name: 'planted', pending, rows: [...base, ...rows], covering: [LEAD], want: want || null, stop: null });
  R('a pending tooltip printing the event headline under "Strongest headline"', tipFaults(tc(true, [{ label: 'Strongest headline', value: LEAD }])), /prints the coverage event's lead headline/);
  A('a pending tooltip printing "loading" and a labelled fallback', tipFaults(tc(true, [{ label: 'Strongest headline', value: 'loading' }, { label: 'Lead headline of the coverage event', value: LEAD }])));
  R('a loaded tooltip printing the event headline, not the day route\'s', tipFaults(tc(false, [{ label: 'Strongest headline', value: LEAD }], 'Day headline one')), /the day route's first headline/);
  A('a loaded tooltip printing the day route\'s first headline', tipFaults(tc(false, [{ label: 'Strongest headline', value: 'Day headline one' }], 'Day headline one')));
  // arm 3's grader
  const zr = (pct, chg) => ({ mnemonic: 'BEST_CAPEX', fiscal_year: 2027, before: '-3,979.67', after: '-3,979.78', chg: chg || '-0.11', pct });
  R('a planted "-0.00%"', zeroMoveFaults([zr('-0.00%')]), /pct cell prints "-0\.00%"/);
  R('a planted "+0.0%"', zeroMoveFaults([zr('+0.0%')]), /pct cell prints "\+0\.0%"/);
  A('"0.00%", "-0.05%" and "-<0.01%"', zeroMoveFaults([zr('0.00%'), zr('-0.05%'), zr('-<0.01%')]));
  arms.push(['PLANTED: the three graders flag their planted faults (text-[9px], rounded-[5px], SVG font-size 8, border-radius 5px, a shared/page token, the event headline under "Strongest headline", a wrong loaded headline, "-0.00%", "+0.0%") and accept the good shapes', f.length === 0,
    f.length ? f.join(' | ') : `${rej} of ${bad} planted faults flagged for their reason; ${acc} of ${good} good shapes accepted`]);
}

let pass = 0;
for (const [n, ok, d] of arms) { if (ok) pass += 1; console.log(`${ok ? 'ARM PASS' : 'ARM FAIL'} ${n} :: ${d}`); }
console.log(`${TITLE}: ${pass} of ${arms.length} arms`);
process.exit(pass === arms.length ? 0 : 1);
