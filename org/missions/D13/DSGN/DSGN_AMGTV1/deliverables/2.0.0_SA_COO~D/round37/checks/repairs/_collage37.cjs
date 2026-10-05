/**
 * _collage37.cjs -- the collage geometry grader of repairs37.cjs, DSGN_AMGTV1 round 37 (issuer 2.0.0_SA_COO~D). NOT a check: it
 * prints nothing; repairs37.cjs and its PLANTED arm call it.
 *
 * The model is round34/checks/collage/labels34.cjs's, copied (labels34 exports nothing and stays frozen with its round): read from
 * the collage <svg> markup in the user units of its viewBox,
 *   - a MARK is every <circle> (cx, cy, r); its owner is its data-bubble key;
 *   - a LABEL is every <text> (owner: data-bubble-label); one LINE BOX per text line (<tspan x y>, else the text itself): width
 *     0.6 x font-size x characters (the estimator ChatterBubbles.tsx places with, CHAR_W 0.6), placed by text-anchor; height
 *     1.2 x font-size, [y - 0.6fs, y + 0.6fs] for dominant-baseline middle/central; <title> text is a hover, never a line;
 *   - a LEADER is every <line> / <polyline> / absolute M/L <path>; its owner is the label in its nearest <g> holding exactly one
 *     label, else the label whose line box is nearest one of its ends;
 *   - EPS 0.5 unit.
 * ROUND 37 ADDS ONE PREDICATE, OWN OUTLINE: labels34 skipped a label's own bubble entirely, so a label drawn ACROSS its own
 *   bubble's outline (part inside, part outside) read clean. That is the live 365D fault (walk read-20261005T025451Z,
 *   fwd21-365D-face.png): "Kim..." (KMB_US_Equity) is drawn across its own red bubble's edge and "Synopsys Inc" (SNPS_US_Equity)
 *   across its own green bubble's edge -- ChatterBubbles.tsx's last-resort stage admits a slot "only this label's own bubble
 *   touches". A line box STRADDLES its own bubble when it meets the circle (nearest point more than EPS inside the radius) and is
 *   not wholly inside it (its farthest corner lies more than EPS outside the radius). A label wholly inside its own bubble, or
 *   wholly clear of it, is fine.
 * Exports: collageModel(html), collisionFaults(model, names), clipFaults(model), leaderBubbleCrossings(model, names) (INFO only).
 */
const CHAR_W = 0.6;
const EPS = 0.5;
const OWN_END = 1;

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
const readText = (n) => (n.text !== undefined ? n.text : n.tag === 'title' ? ' ' : (n.children || []).map(readText).join(''));
const num = (v) => (v === undefined || v === null || String(v).trim() === '' ? NaN : Number(String(v).trim().replace(/px$/, '')));
const styleOf = (s) => { const o = {}; for (const part of String(s || '').split(';')) { const i = part.indexOf(':'); if (i > 0) o[part.slice(0, i).trim().toLowerCase()] = part.slice(i + 1).trim(); } return o; };
const fontSizeOf = (n) => { const a = num(n.attrs['font-size']); if (Number.isFinite(a)) return a; return num(styleOf(n.attrs.style)['font-size']); };
const attrOrStyle = (n, k) => (n.attrs[k] !== undefined ? n.attrs[k] : styleOf(n.attrs.style)[k]);

/** { faults, box, marks:[{key,cx,cy,r}], labels:[{key,text,lines:[{text,x0,x1,y0,y1}]}], leaders:[{owner,segs}] } */
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
    let g = t.parent;
    while (g && g !== svg && g.tag !== 'g') g = g.parent;
    labels.push({ node: t, key: t.attrs['data-bubble-label'] === undefined ? null : t.attrs['data-bubble-label'], lines, text: lines.map((l) => l.text).join(' '), g });
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

const boxesMeet = (a, b) => Math.min(a.x1, b.x1) - Math.max(a.x0, b.x0) > EPS && Math.min(a.y1, b.y1) - Math.max(a.y0, b.y0) > EPS;
/** The circle-vs-rect test labels34 uses: the box's nearest point lies more than EPS inside the radius. */
function boxMeetsCircle(b, c) {
  const nx = Math.max(b.x0, Math.min(c.cx, b.x1)); const ny = Math.max(b.y0, Math.min(c.cy, b.y1));
  return Math.hypot(nx - c.cx, ny - c.cy) < c.r - EPS;
}
/** The box's farthest corner lies more than EPS outside the radius (so the box is not wholly inside the circle). */
function boxLeavesCircle(b, c) {
  const fx = Math.max(Math.abs(b.x0 - c.cx), Math.abs(b.x1 - c.cx)); const fy = Math.max(Math.abs(b.y0 - c.cy), Math.abs(b.y1 - c.cy));
  return Math.hypot(fx, fy) > c.r + EPS;
}
const straddles = (b, c) => boxMeetsCircle(b, c) && boxLeavesCircle(b, c);
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
/** Does the segment pass more than EPS inside the circle? */
function segCrossesCircle(s, c) {
  const dx = s.x2 - s.x1; const dy = s.y2 - s.y1; const L2 = dx * dx + dy * dy;
  const t = L2 === 0 ? 0 : Math.max(0, Math.min(1, ((c.cx - s.x1) * dx + (c.cy - s.y1) * dy) / L2));
  return Math.hypot(s.x1 + t * dx - c.cx, s.y1 + t * dy - c.cy) < c.r - EPS;
}
const q = (s) => `"${s}"`;

/** Every collision of one collage, named by label text: [{kind, text}]. names: Map key -> served display name. */
function collisionFaults(m, names) {
  const f = m.faults.filter((x) => /^TRANSFORM|^UNREAD|^NO COLLAGE|^NO FONT-SIZE/.test(x)).map((x) => ({ kind: 'MODEL', text: x }));
  const markName = (c) => (c.key === null ? 'an unlabelled circle' : `the bubble of ${q((names && names.get(c.key)) || c.key)}`);
  for (let i = 0; i < m.labels.length; i += 1) for (let j = i + 1; j < m.labels.length; j += 1) {
    const a = m.labels[i]; const b = m.labels[j];
    if (a.lines.some((p) => b.lines.some((r) => boxesMeet(p, r)))) f.push({ kind: 'LABEL OVER LABEL', text: `${q(a.text)} x ${q(b.text)}` });
  }
  for (const l of m.labels) for (const c of m.marks) {
    if (l.key !== null && c.key === l.key) {
      if (l.lines.some((b) => straddles(b, c))) f.push({ kind: 'LABEL ACROSS ITS OWN OUTLINE', text: `${q(l.text)} is drawn across the edge of its own bubble (part inside, part outside)` });
      continue;
    }
    if (l.lines.some((b) => boxMeetsCircle(b, c))) f.push({ kind: 'LABEL OVER BUBBLE', text: `${q(l.text)} over ${markName(c)}` });
  }
  for (const ld of m.leaders) for (const l of m.labels) {
    const own = ld.owner === l;
    const hit = ld.segs.some((s, k) => {
      const seg = own && k === ld.segs.length - 1 ? shortSeg(s, OWN_END) : s;
      return seg && l.lines.some((b) => segCrossesBox(seg, b));
    });
    if (hit && !own) f.push({ kind: 'LINE THROUGH LABEL', text: `the leader line of ${ld.owner ? q(ld.owner.text) : 'an unowned line'} runs through ${q(l.text)}` });
  }
  return f;
}
/** Every line box outside the viewBox (EPS 0.5). */
function clipFaults(m) {
  if (!m.box) return [{ kind: 'CLIPPED', text: 'NO VIEWBOX on the collage svg' }];
  const f = [];
  for (const l of m.labels) {
    const out = l.lines.filter((b) => b.x0 < m.box.x - EPS || b.y0 < m.box.y - EPS || b.x1 > m.box.x + m.box.w + EPS || b.y1 > m.box.y + m.box.h + EPS);
    if (out.length) f.push({ kind: 'CLIPPED', text: `${q(l.text)} leaves the viewBox (box ${out[0].x0.toFixed(1)}..${out[0].x1.toFixed(1)} x ${out[0].y0.toFixed(1)}..${out[0].y1.toFixed(1)})` });
  }
  return f;
}
/** INFO only (not graded): leaders passing through a bubble that is not their own label's. */
function leaderBubbleCrossings(m, names) {
  const out = [];
  for (const ld of m.leaders) for (const c of m.marks) {
    if (ld.owner && c.key === ld.owner.key) continue;
    if (ld.segs.some((s) => segCrossesCircle(s, c))) out.push(`${ld.owner ? q(ld.owner.text) : 'unowned'} x ${q((names && names.get(c.key)) || c.key)}`);
  }
  return out;
}

module.exports = { collageModel, collisionFaults, clipFaults, leaderBubbleCrossings, straddles, boxMeetsCircle, CHAR_W, EPS };
