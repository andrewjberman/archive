/**
 * labels34.cjs -- DSGN_AMGTV1 round 34, REPAIR CELL check 1 of 2 (issuer 2.0.0_SA_COO~D): NO CHATTER LABEL CLIPS OR OVERLAPS, AT
 * ANY WINDOW (PRD FWD-21: "every name of the window is visible in one panel at 1440x900 without scrolling, and no label clips or
 * overlaps").
 *
 * Usage (from the directory whose portal/ is the checkout under test, e.g. C:/tmp/wk-dsgn-amgtv1-92): node <this file>
 *   ISSUER GREEN ARM: CHECK_SRC_OVERRIDE (see round15/checks/_load.cjs) is honoured for every source read here.
 * Why: ledger/COMPLETION_GRADES.round32.json row FWD-21 (NOT_REALIZED) and ledger/ROUND_ANALYSIS.round33.md section 1: "at 90D,
 *   labels collide with bubbles and leader lines run through labels (TOKYO ELECTRON LTD, UnitedHealth Group Inc; verified on shot
 *   004 of walk 20261003T175905Z)"; enrichment list item 2, the repair cell: "FWD-21's 90D/365D label collisions (no label crossed
 *   by a leader line or overlapping a bubble)". components/ChatterBubbles.tsx at PROD dbd29c6320 places an outside label in a
 *   third stage that may sit OVER other circles (OUTSIDE_STAGES[2].overCircles = true), places a last-resort label anywhere in the
 *   box without a circle test, and draws each leader line with no test against any label.
 * Render: ../../../round31/checks/presets/_presets.cjs -- the REAL LeadPanel with the REAL ChatterBubbles in window mode (no
 *   `month`: LeadPanel's ChatterFace passes `data` and `onSelectSecurity` only), each preset selected through the control's own
 *   onChange, over round31/fixtures/windows.chatter.{30,90,365}.json (served by opal-amgt-scoped-api code KQSA62c3,
 *   2026-10-03T01:56Z). The walk's own 90D layout (65 names, 17:59Z) is not reproducible offline; the fixtures carry 55 / 64 / 70.
 * THE GEOMETRY (read from the collage <svg> markup, user units of its viewBox):
 *   - a MARK is every <circle> (cx, cy, r); its owner is its data-bubble key;
 *   - a LABEL is every <text> (owner: data-bubble-label); one LINE BOX per text line (<tspan x y dx dy>, else the text itself):
 *     width = 0.6 x font-size x characters -- the SAME estimator ChatterBubbles.tsx places labels with (CHAR_W = 0.6) -- placed by
 *     text-anchor (start default, middle, end); height 1.2 x font-size: [y - 0.6fs, y + 0.6fs] for dominant-baseline middle/central,
 *     [y, y + 1.2fs] for hanging/text-before-edge, [y - 0.9fs, y + 0.3fs] otherwise (round29 collage.cjs's published model);
 *     <title> text inside a <text> is a hover, never a line;
 *   - a LEADER is every <line> (x1 y1 x2 y2), <polyline points> and <path d> of absolute M/L commands in the svg; its owner is the
 *     label in its nearest <g> holding exactly one label, else the label whose line box is nearest one of its ends.
 *   - EPS 0.5 unit: two boxes collide when they share more than 0.5 on both axes; a box meets a circle when its nearest point lies
 *     more than 0.5 inside the radius; a leader crosses a box when it passes through the box shrunk by 0.5 on every side.
 * MEASURED (the brief's width question): on walk shot 004 (90D, 1440 px; the 840 x 520 viewBox draws at scale 1.0 inside a
 *   max-height 520px svg) the Lato label ink measures 0.45-0.51 em per character on mixed-case names ("UnitedHealth Group Inc" 22
 *   chars 100 px, "Spotify Technology SA" 21 chars 95 px) and 0.59 em on all-caps ("TOKYO ELECTRON LTD" 18 chars 106 px,
 *   "HERMES INTERNATIONAL" 20 chars 118 px), assuming the 10-unit first-choice size. The 0.6 estimate is at or above every sample,
 *   so it does not under-measure: the walk's collisions are the placement stages above, and this static geometry reproduces their
 *   class on the fixtures at all three windows.
 * Arms:
 *   1  NO LABEL CROSSES ANOTHER MARK, at 30, 90 and 365 days: no line box of one label meets a line box of another label; no line
 *      box meets a circle other than its own label's bubble (a label inside its own bubble is fine); no leader crosses any label's
 *      line box except its own label's, which it may only touch at its end (the last 1 unit is exempt). Every collision is named by
 *      label text; the collage svg carries no transform (positions are read as absolute).
 *   2  NO CLIPPED LABEL: at 30, 90 and 365 days every line box lies inside the svg viewBox (EPS 0.5), and every SHORTENED label
 *      (its text is not the served display name) carries the full served name in a <title> on the same mark -- a <title> child of
 *      the <text>, or a direct <title> child of the label's nearest <g> -- and the hover can reach it: neither the <text> nor any
 *      ancestor inside the svg is pointer-events none (attribute, inline style or class pointer-events-none).
 *   3  KEEP: round29 collage/collage.cjs and collage/tone.cjs, round31 presets/presets.cjs and round32 repairs/words32.cjs exit 0
 *      (same cwd, same environment).
 *   4  PLANTED: the arm-1 predicates reject a planted label/label overlap, label/bubble overlap and line-through-label, each for its
 *      own class, and the arm-2 predicates reject a clipped label, a shortened label with no hover and one whose hover sits behind
 *      pointer-events none; both accept a clean layout (a shortened label hovered by its group's <title>).
 * Blind spots: the box model is an estimate -- 0.6 em per character over-measures Lato mixed case (0.45-0.51 em measured), so a
 *   box-model collision can be a near-miss on screen, and kerning, a font fallback or a wider glyph set are not modelled; a leader
 *   crossing another BUBBLE is not graded (the brief's arm 1 names labels); the hover is read as markup (a static <title>), never a
 *   live hover; the fixtures are the 01:56Z capture, not the walk's 17:59Z data, so a layout reached only on other data is not seen.
 * Prints one line per arm (arm 1 and 2 then list every named fault on indented lines) and "NO CHATTER LABEL CLIPS OR OVERLAPS: <k>
 * of 4 arms"; exit 0 only at 4 of 4. Static renders only; no network, no AWS, writes no file.
 */
const path = require('path');
const { spawnSync } = require('child_process');

const DROOT = path.join(__dirname, '..', '..', '..');
const P = require(path.join(DROOT, 'round31', 'checks', 'presets', '_presets.cjs'));
const { CHATTER, WINDOWS } = P;
const first = (e) => String(e && e.message ? e.message : e).split('\n')[0];

const CHAR_W = 0.6;
const EPS = 0.5;
const OWN_END = 1;

// ---- a small markup tree (react-dom/server output is well formed) -----------------------------------------------------------
const VOID = new Set(['area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'source', 'track', 'wbr']);
const decode = (s) => String(s).replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&quot;/g, '"').replace(/&#x27;/g, "'").replace(/&#39;/g, "'").replace(/&nbsp;/g, ' ').replace(/&amp;/g, '&');
function parse(html) {
  const root = { tag: '#root', attrs: {}, children: [], parent: null };
  let cur = root;
  const re = /<!--[\s\S]*?-->|<\/([a-zA-Z][\w:-]*)\s*>|<([a-zA-Z][\w:.-]*)((?:\s+[^\s=>\/]+(?:="[^"]*")?)*)\s*(\/?)>|([^<]+)/g;
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
function all(node, pred, out = []) { for (const c of node.children || []) if (c.tag) { if (pred(c)) out.push(c); all(c, pred, out); } return out; }
const norm = (s) => String(s).replace(/\s+/g, ' ').trim();
/** Text a person reads in the node: <title> subtrees are hovers, not text. */
const readText = (n) => (n.text !== undefined ? n.text : n.tag === 'title' ? ' ' : (n.children || []).map(readText).join(''));
const titleText = (n) => norm((n.children || []).map((c) => (c.text !== undefined ? c.text : readText(c))).join(' '));
const num = (v) => (v === undefined || v === null || String(v).trim() === '' ? NaN : Number(String(v).trim().replace(/px$/, '')));
const styleOf = (s) => { const o = {}; for (const part of String(s || '').split(';')) { const i = part.indexOf(':'); if (i > 0) o[part.slice(0, i).trim().toLowerCase()] = part.slice(i + 1).trim(); } return o; };
const fontSizeOf = (n) => { const a = num(n.attrs['font-size']); if (Number.isFinite(a)) return a; return num(styleOf(n.attrs.style)['font-size']); };
const attrOrStyle = (n, k) => (n.attrs[k] !== undefined ? n.attrs[k] : styleOf(n.attrs.style)[k]);

// ---- the collage model --------------------------------------------------------------------------------------------------------
/** { faults, box, marks:[{key,cx,cy,r}], labels:[{key,text,lines:[{text,x0,x1,y0,y1}],hovers:[...],reachable}], leaders:[{owner,segs}] } */
function collageModel(html) {
  const faults = [];
  const tree = parse(html);
  const svg = all(tree, (n) => n.tag === 'svg' && all(n, (c) => c.attrs['data-bubble'] !== undefined).length > 0)[0];
  if (!svg) return { faults: ['NO COLLAGE: no <svg> holding a [data-bubble] element'], box: null, marks: [], labels: [], leaders: [] };
  const vb = String(svg.attrs.viewBox || svg.attrs.viewbox || '').trim().split(/[\s,]+/).map(Number);
  const box = vb.length === 4 && vb.every(Number.isFinite) ? { x: vb[0], y: vb[1], w: vb[2], h: vb[3] } : null;
  if (!box) faults.push('NO VIEWBOX on the collage svg');
  const inside = all(svg, () => true);
  const tf = inside.find((n) => n.attrs.transform !== undefined || /transform\s*:/.test(n.attrs.style || ''));
  if (tf) faults.push(`TRANSFORM on a <${tf.tag}> inside the collage svg: positions must be absolute`);
  const marks = inside.filter((n) => n.tag === 'circle').map((n) => ({ key: n.attrs['data-bubble'] === undefined ? null : n.attrs['data-bubble'], cx: num(n.attrs.cx), cy: num(n.attrs.cy), r: num(n.attrs.r) }))
    .filter((c) => [c.cx, c.cy, c.r].every(Number.isFinite) && c.r > 0);
  const labels = [];
  for (const t of inside.filter((n) => n.tag === 'text')) {
    const fs0 = fontSizeOf(t);
    const anchor0 = attrOrStyle(t, 'text-anchor') || 'start';
    const base = String(attrOrStyle(t, 'dominant-baseline') || '');
    let cx = num(t.attrs.x); let cy = num(t.attrs.y);
    if (!Number.isFinite(cx)) cx = 0;
    if (!Number.isFinite(cy)) cy = 0;
    const lines = [];
    const addLine = (raw, fs, anchor) => {
      const text = norm(raw);
      if (!text) return;
      if (!Number.isFinite(fs) || fs <= 0) { faults.push(`NO FONT-SIZE on the label "${text.slice(0, 30)}"`); return; }
      const w = CHAR_W * fs * text.length;
      const x0 = anchor === 'middle' ? cx - w / 2 : anchor === 'end' ? cx - w : cx;
      const [u, d] = /middle|central/.test(base) ? [0.6, 0.6] : /hanging|text-before-edge/.test(base) ? [0, 1.2] : [0.9, 0.3];
      lines.push({ text, x0, x1: x0 + w, y0: cy - u * fs, y1: cy + d * fs });
    };
    for (const c of t.children) {
      if (c.text !== undefined) { addLine(c.text, fs0, anchor0); continue; }
      if (c.tag !== 'tspan') continue;
      const fs = Number.isFinite(fontSizeOf(c)) ? fontSizeOf(c) : fs0;
      if (c.attrs.x !== undefined) cx = num(c.attrs.x);
      if (c.attrs.y !== undefined) cy = num(c.attrs.y);
      const em = (v) => (/em$/.test(String(v).trim()) ? Number(String(v).trim().slice(0, -2)) * fs : num(v));
      if (c.attrs.dx !== undefined) cx += em(c.attrs.dx);
      if (c.attrs.dy !== undefined) cy += em(c.attrs.dy);
      addLine(readText(c), fs, attrOrStyle(c, 'text-anchor') || anchor0);
    }
    const hovers = t.children.filter((c) => c.tag === 'title').map(titleText);
    let g = t.parent;
    while (g && g !== svg && g.tag !== 'g') g = g.parent;
    if (g && g.tag === 'g') hovers.push(...g.children.filter((c) => c.tag === 'title').map(titleText));
    let reachable = true;
    for (let n = t; n && n !== svg.parent; n = n.parent) {
      if (!n.attrs) continue;
      const pe = attrOrStyle(n, 'pointer-events');
      if (String(pe || '').trim() === 'none' || String(n.attrs.class || n.attrs.className || '').split(/\s+/).includes('pointer-events-none')) reachable = false;
    }
    labels.push({ node: t, key: t.attrs['data-bubble-label'] === undefined ? null : t.attrs['data-bubble-label'], lines, text: lines.map((l) => l.text).join(' '), joinedTight: lines.map((l) => l.text).join(''), hovers, reachable, g });
  }
  const leaders = [];
  for (const n of inside) {
    let pts = null;
    if (n.tag === 'line') pts = [[num(n.attrs.x1 || 0), num(n.attrs.y1 || 0)], [num(n.attrs.x2 || 0), num(n.attrs.y2 || 0)]];
    else if (n.tag === 'polyline') { const v = String(n.attrs.points || '').trim().split(/[\s,]+/).map(Number); pts = []; for (let i = 0; i + 1 < v.length; i += 2) pts.push([v[i], v[i + 1]]); }
    else if (n.tag === 'path') {
      const d = String(n.attrs.d || '').trim();
      const tok = d.match(/[A-Za-z]|-?(?:\d+\.?\d*|\.\d+)(?:e[-+]?\d+)?/g) || [];
      if (tok[0] !== 'M' || tok.some((x) => /^[A-Za-z]$/.test(x) && !['M', 'L', 'Z'].includes(x))) { faults.push(`UNREAD <path d="${d.slice(0, 30)}">: only absolute M/L paths are read`); continue; }
      const v = tok.filter((x) => !/^[A-Za-z]$/.test(x)).map(Number); pts = []; for (let i = 0; i + 1 < v.length; i += 2) pts.push([v[i], v[i + 1]]);
    } else continue;
    if (!pts || pts.length < 2 || pts.flat().some((x) => !Number.isFinite(x))) { faults.push(`UNREAD <${n.tag}> geometry`); continue; }
    const segs = []; for (let i = 0; i + 1 < pts.length; i += 1) segs.push({ x1: pts[i][0], y1: pts[i][1], x2: pts[i + 1][0], y2: pts[i + 1][1] });
    let g = n.parent; while (g && g !== svg && g.tag !== 'g') g = g.parent;
    let owner = null;
    if (g && g.tag === 'g') { const own = labels.filter((l) => l.g === g || all(g, (c) => c === l.node).length > 0); if (own.length === 1) owner = own[0]; }
    if (!owner && labels.length) {
      let best = Infinity;
      for (const l of labels) for (const b of l.lines) for (const [px, py] of [pts[0], pts[pts.length - 1]]) {
        const dx = Math.max(b.x0 - px, 0, px - b.x1); const dy = Math.max(b.y0 - py, 0, py - b.y1); const dd = Math.hypot(dx, dy);
        if (dd < best) { best = dd; owner = l; }
      }
    }
    leaders.push({ owner, segs });
  }
  return { faults, box, marks, labels, leaders };
}

// ---- predicates ---------------------------------------------------------------------------------------------------------------
const boxesMeet = (a, b) => Math.min(a.x1, b.x1) - Math.max(a.x0, b.x0) > EPS && Math.min(a.y1, b.y1) - Math.max(a.y0, b.y0) > EPS;
function boxMeetsCircle(b, c) {
  const nx = Math.max(b.x0, Math.min(c.cx, b.x1)); const ny = Math.max(b.y0, Math.min(c.cy, b.y1));
  return Math.hypot(nx - c.cx, ny - c.cy) < c.r - EPS;
}
/** Liang-Barsky: does segment s pass through box b shrunk by EPS on every side? */
function segCrossesBox(s, b) {
  const x0 = b.x0 + EPS; const x1 = b.x1 - EPS; const y0 = b.y0 + EPS; const y1 = b.y1 - EPS;
  if (x0 >= x1 || y0 >= y1) return false;
  let t0 = 0; let t1 = 1; const dx = s.x2 - s.x1; const dy = s.y2 - s.y1;
  for (const [p, q] of [[-dx, s.x1 - x0], [dx, x1 - s.x1], [-dy, s.y1 - y0], [dy, y1 - s.y1]]) {
    if (p === 0) { if (q < 0) return false; continue; }
    const t = q / p;
    if (p < 0) { if (t > t1) return false; if (t > t0) t0 = t; } else { if (t < t0) return false; if (t < t1) t1 = t; }
  }
  return t0 < t1;
}
const shortSeg = (s, cut) => { const L = Math.hypot(s.x2 - s.x1, s.y2 - s.y1); if (L <= cut) return null; const k = (L - cut) / L; return { x1: s.x1, y1: s.y1, x2: s.x1 + (s.x2 - s.x1) * k, y2: s.y1 + (s.y2 - s.y1) * k }; };
const q = (s) => `"${s}"`;
/** Arm 1: every collision named by label text. names: Map key -> served display name. */
function collisionFaults(m, names) {
  const f = [...m.faults.filter((x) => /^TRANSFORM|^UNREAD|^NO COLLAGE/.test(x))];
  const markName = (c) => (c.key === null ? 'an unlabelled circle' : `the bubble of ${q(names.get(c.key) || c.key)}`);
  for (let i = 0; i < m.labels.length; i += 1) for (let j = i + 1; j < m.labels.length; j += 1) {
    const a = m.labels[i]; const b = m.labels[j];
    if (a.lines.some((p) => b.lines.some((r) => boxesMeet(p, r)))) f.push(`LABEL OVER LABEL: ${q(a.text)} x ${q(b.text)}`);
  }
  for (const l of m.labels) for (const c of m.marks) {
    if (l.key !== null && c.key === l.key) continue;
    if (l.lines.some((b) => boxMeetsCircle(b, c))) f.push(`LABEL OVER BUBBLE: ${q(l.text)} over ${markName(c)}`);
  }
  for (const ld of m.leaders) for (const l of m.labels) {
    const own = ld.owner === l;
    const hit = ld.segs.some((s, k) => {
      const seg = own && k === ld.segs.length - 1 ? shortSeg(s, OWN_END) : s;
      return seg && l.lines.some((b) => segCrossesBox(seg, b));
    });
    if (hit) f.push(`LINE THROUGH LABEL: the leader line of ${ld.owner ? q(ld.owner.text) : 'an unowned line'} runs through ${own ? 'its own label' : q(l.text)}`);
  }
  return f;
}
/** Arm 2: clipped boxes and shortened labels without a reachable full-name hover. */
function clipHoverFaults(m, names) {
  const f = [];
  if (!m.box) return ['NO VIEWBOX on the collage svg'];
  for (const l of m.labels) {
    const out = l.lines.filter((b) => b.x0 < m.box.x - EPS || b.y0 < m.box.y - EPS || b.x1 > m.box.x + m.box.w + EPS || b.y1 > m.box.y + m.box.h + EPS);
    if (out.length) f.push(`CLIPPED: ${q(l.text)} leaves the viewBox (box ${out[0].x0.toFixed(1)}..${out[0].x1.toFixed(1)} x ${out[0].y0.toFixed(1)}..${out[0].y1.toFixed(1)})`);
    const name = l.key === null ? null : norm(names.get(l.key) || '');
    if (!name) continue;
    if (norm(l.text) === name || l.joinedTight.replace(/\s+/g, '') === name.replace(/\s+/g, '')) continue;
    if (!l.hovers.some((h) => h.includes(name))) f.push(`NO HOVER: the shortened label ${q(l.text)} carries no <title> naming ${q(name)} on its <text> or its <g>`);
    else if (!l.reachable) f.push(`HOVER UNREACHABLE: the shortened label ${q(l.text)} is pointer-events none, so its hover never shows`);
  }
  return f;
}

// ---- the served windows ---------------------------------------------------------------------------------------------------------
const NAMES = new Map();
for (const d of WINDOWS) for (const r of CHATTER[d].rows) NAMES.set(r.security_key, r.display_name);
const renders = {};
const stops = [];
for (const d of WINDOWS) {
  try {
    const r = P.renderAt('CHATTER', d);
    if (r.stop) stops.push(`${d}D: ${r.stop}`);
    if (r.at) renders[d] = collageModel(r.at.html);
  } catch (e) { stops.push(`${d}D: RENDER ${first(e)}`); }
}

const arms = [];
// Arm 1 -- NO LABEL CROSSES ANOTHER MARK.
{
  const f = [...stops];
  const tally = [];
  for (const d of WINDOWS) {
    const m = renders[d];
    if (!m) { f.push(`${d}D: not rendered`); continue; }
    const x = collisionFaults(m, NAMES);
    const n = (re) => x.filter((y) => re.test(y)).length;
    tally.push(`${d}D ${m.labels.length} labels, ${m.leaders.length} leaders: ${n(/^LABEL OVER LABEL/)} label/label, ${n(/^LABEL OVER BUBBLE/)} label/bubble, ${n(/^LINE THROUGH/)} line/label`);
    f.push(...x.map((y) => `${d}D: ${y}`));
  }
  arms.push(['NO LABEL CROSSES ANOTHER MARK: at 30/90/365 no label meets another label, a bubble not its own, or a leader line not its own', f.length === 0, tally.join('; ') || 'no render', f]);
}
// Arm 2 -- NO CLIPPED LABEL.
{
  const f = [...stops];
  const tally = [];
  for (const d of WINDOWS) {
    const m = renders[d];
    if (!m) { f.push(`${d}D: not rendered`); continue; }
    const x = clipHoverFaults(m, NAMES);
    const shortened = m.labels.filter((l) => l.key !== null && NAMES.has(l.key) && norm(l.text) !== norm(NAMES.get(l.key)) && l.joinedTight.replace(/\s+/g, '') !== norm(NAMES.get(l.key)).replace(/\s+/g, '')).length;
    tally.push(`${d}D ${m.labels.length} labels in the viewBox check, ${shortened} shortened`);
    f.push(...x.map((y) => `${d}D: ${y}`));
  }
  arms.push(['NO CLIPPED LABEL: every label box inside the viewBox; a shortened label carries its full name in a reachable <title> on its own mark', f.length === 0, tally.join('; ') || 'no render', f]);
}
// Arm 3 -- KEEP.
{
  const f = [];
  const KEEP = ['round29/checks/collage/collage.cjs', 'round29/checks/collage/tone.cjs', 'round31/checks/presets/presets.cjs', 'round32/checks/repairs/words32.cjs'];
  for (const rel of KEEP) {
    const r = spawnSync(process.execPath, [path.join(DROOT, rel)], { cwd: process.cwd(), encoding: 'utf8', timeout: 300000 });
    const last = ((r.stdout || '') + (r.stderr || '')).trim().split('\n').pop() || '';
    if (r.status !== 0) f.push(`KEEP: ${rel} rc=${r.status} ("${last.slice(0, 100)}")`);
  }
  arms.push(['KEEP: round29 collage.cjs and tone.cjs, round31 presets.cjs and round32 words32.cjs exit 0', f.length === 0, f.length ? `${f.length} of ${KEEP.length} fail` : `${KEEP.length} of ${KEEP.length} exit 0`, f]);
}
// Arm 4 -- PLANTED.
{
  const f = [];
  const names = new Map([['A', 'Alpha'], ['B', 'Beta Holdings'], ['C', 'Gamma Group'], ['D', 'Delta Co']]);
  const g = (k, circle, label, extra) => `<g><circle data-bubble="${k}" cx="${circle[0]}" cy="${circle[1]}" r="${circle[2]}"><title>${names.get(k)}; 3 articles collected</title></circle>${extra || ''}` +
    `<text data-bubble-label="${k}" x="${label[0]}" y="${label[1]}" font-size="${label[2]}" text-anchor="middle" dominant-baseline="central"${label[4] || ''}>${label[3]}</text>${label[5] || ''}</g>`;
  const S = (parts) => `<div><svg viewBox="0 0 400 300" width="100%">${parts.join('')}</svg></div>`;
  const CLEAN = {
    A: [[100, 100, 40], [100, 100, 10, 'Alpha']],
    B: [[220, 100, 20], [220, 140, 10, 'Beta Holdings'], '<line x1="220" y1="120" x2="220" y2="134"></line>'],
    C: [[330, 100, 10], [330, 125, 8, 'Gam...', '', '<title>Gamma Group</title>']],
    D: [[330, 200, 10], [330, 225, 8, 'Delta Co']],
  };
  const build = (over) => { const s = JSON.parse(JSON.stringify(CLEAN)); (over || (() => {}))(s); return S(Object.keys(s).map((k) => g(k, s[k][0], s[k][1], s[k][2]))); };
  const judge = (html) => { const m = collageModel(html); return [...collisionFaults(m, names), ...clipHoverFaults(m, names)]; };
  const good = judge(build());
  if (good.length) f.push(`the clean layout is rejected: ${good[0]}`);
  const PLANTS = [
    ['a label/label overlap', /^LABEL OVER LABEL/, build((s) => { s.C[1][1] = 222; s.C[1][0] = 334; })],
    ['a label/bubble overlap', /^LABEL OVER BUBBLE: "Gam\.\.\." over the bubble of "Alpha"/, build((s) => { s.C[1][0] = 100; s.C[1][1] = 135; })],
    ['a line through a label', /^LINE THROUGH LABEL: the leader line of "Beta Holdings" runs through "Delta Co"/, build((s) => { s.B[2] = '<line x1="220" y1="120" x2="330" y2="228"></line>'; })],
    ['a clipped label', /^CLIPPED/, build((s) => { s.D[1][0] = 398; })],
    ['a shortened label with no hover', /^NO HOVER/, build((s) => { s.C[1][5] = ''; })],
    ['a shortened label behind pointer-events none', /^HOVER UNREACHABLE/, build((s) => { s.C[1][4] = ' pointer-events="none"'; })],
  ];
  let caught = 0;
  for (const [n, why, html] of PLANTS) { const x = judge(html); if (x.some((y) => why.test(y))) caught += 1; else f.push(`"${n}" not rejected for its reason (${x.length ? x[0] : 'accepted'})`); }
  const inText = judge(build((s) => { s.C[1][3] = 'Gam...<title>Gamma Group</title>'; s.C[1][5] = ''; }));
  if (inText.length) f.push(`a shortened label hovered by its own <text>'s <title> is rejected: ${inText[0]}`);
  arms.push(['PLANTED: the geometry and hover predicates reject 6 planted faults, each for its own class, and accept 2 clean layouts', f.length === 0,
    f.length ? f.join(' | ') : `${caught} of ${PLANTS.length} rejected for their reason (label/label, label/bubble, line/label, clipped, no hover, unreachable hover); 2 clean layouts accepted`, []]);
}

let pass = 0;
for (const [n, ok, d, list] of arms) {
  if (ok) pass += 1;
  console.log(`${ok ? 'ARM PASS' : 'ARM FAIL'} ${n} :: ${d}${!ok && list.length ? ` -- ${list.length} fault(s):` : ''}`);
  if (!ok) for (const x of list) console.log(`  - ${x}`);
}
console.log(`NO CHATTER LABEL CLIPS OR OVERLAPS: ${pass} of 4 arms`);
process.exit(pass === 4 ? 0 : 1);
