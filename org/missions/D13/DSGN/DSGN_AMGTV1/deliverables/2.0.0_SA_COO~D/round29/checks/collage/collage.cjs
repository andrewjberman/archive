/**
 * collage.cjs -- DSGN_AMGTV1 round 29, AV-zg-4 CHATTER COLLAGE (issuer 2.0.0_SA_COO~D): THE CHATTER FACE IS ONE PACKED COLLAGE
 * WITH CLEAR LABELS.
 *
 * Usage: cd C:/tmp/wk-dsgn-amgtv1-70 && node <this file>     (portal/ under the cwd is the checkout under test)
 * Grades PRD v0.10 FWD-21 (DSGN_AMGTV1_PRD.md ~291-315), the layout limbs: "the bubbles form a collage, largest at the centre
 *   and smaller outward, by a deterministic spiral placement with no new dependency; every name of the window is visible in
 *   one panel at 1440x900 without scrolling, and no label clips or overlaps"; SAUX-16 and SAUX-17 of
 *   docs/briefs/amgt-security-analysis-ui-findings-20261002.json. The fill limb is tone.cjs beside this file.
 * Inputs (round29/fixtures/collage/, built by r29c.build.cjs): r29c.chatter.toned.json (the 95 served rows of
 *   round16 r16g, 17 collected in 2026-09) and r29c.chatter.dense.json (the same 95 keys ALL collected in one month, counts
 *   60 -> 1: the whole covered universe at once); base.json (the BASE package.json sha256).
 * THE CONTRACT READ FROM THE RENDER (react-dom/server through round15/checks/_load.cjs):
 *   - every bubble is ONE `<circle data-bubble="<security_key>" cx cy r>` (absolute numbers; no `transform` anywhere inside the
 *     collage svg), all inside ONE `<svg viewBox="minX minY W H">`;
 *   - every bubble has ONE `<text data-bubble-label="<security_key>" x y font-size>` (optional `<tspan x y dy>` lines; dy in
 *     units or em); its text is the served display name in full, or a leading part of at least 3 characters ending in "..."
 *     or U+2026, the full name then being in the bubble's hover `<title>`;
 *   - TEXT BOX MODEL (published to the worker): a line is 0.6 x font-size per character wide, placed by text-anchor (start
 *     default, middle, end), and 1.2 x font-size tall: [y - 0.9fs, y + 0.3fs] for the default baseline, [y - 0.6fs, y + 0.6fs]
 *     for dominant-baseline middle/central, [y, y + 1.2fs] for hanging/text-before-edge.
 * Arms:
 *   1  PACKED (SAUX-16): on both inputs, one bubble per collected name and none other; no two circles overlap; every circle is
 *      inside the viewBox; area tracks the served count (r^2 / collected within 2% across the render); the viewBox centre lies
 *      inside the largest bubble; sizes fall outward (Spearman rho of radius against the BOX-RELATIVE distance from the centre,
 *      hypot(dx / (W/2), dy / (H/2)), <= -0.5; calibrated: BASE grid -0.19..+0.25 on 8 inputs, a spiral reference -0.79..-0.94); ONE
 *      panel: the 95-name viewBox equals the 17-name viewBox (the box never grows with the count) and the svg's drawn height
 *      is bounded (a numeric `height` attribute, or an inline style height/max-height in px, <= 520).
 *   2  LABELS (SAUX-17): on both inputs, every bubble carries exactly one label of the full name or a >= 3-character shortening
 *      (full name in its hover); every `<text>` in the collage svg has a font-size, sits inside the viewBox, and no two text
 *      lines overlap.
 *   3  CONTROL (passes at BASE by design): deterministic (two renders byte-equal; no Math.random / Date.now / performance.now /
 *      new Date / crypto in ChatterBubbles.tsx); no new dependency (portal/package.json sha256 = BASE; ChatterBubbles' bare
 *      imports within react + motion/react); the month cursor stays ([data-chatter-cursor] with onMonthChange; stepMonth
 *      exported and clamped); the round-27 identity hover check ($D/round27/checks/identity.cjs) exits 0.
 *   4  PLANTED: the arm-1/arm-2 predicates reject 8 known-bad collages, EACH FOR ITS OWN FAULT CLASS (overlapping circles, a
 *      circle over the edge, the largest off-centre, sizes rising outward, two overlapping labels, a clipped label, a growing
 *      box, an unbounded drawn height), and accept a known-good one.
 * Prints one line per arm and "THE CHATTER FACE IS ONE PACKED COLLAGE WITH CLEAR LABELS: <k> of 4 arms"; exit 0 only at 4 of 4.
 * Reads only; writes no file. ISSUER GREEN ARM: CHECK_SRC_OVERRIDE (see _load.cjs) is honoured for every source read here.
 */
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const { spawnSync } = require('child_process');

const SA = 'src/pages/SecurityAnalysis/';
const CB = SA + 'components/ChatterBubbles.tsx';
const D = path.join(__dirname, '..', '..', '..');
const FX = path.join(D, 'round29', 'fixtures', 'collage');
const L = require(path.join(D, 'round15', 'checks', '_load.cjs'));
const unwrap = (x) => (x && x.payload ? x.payload : x);
const fx = (n) => unwrap(JSON.parse(fs.readFileSync(path.join(FX, n), 'utf8')));
const TONED = fx('r29c.chatter.toned.json');
const DENSE = fx('r29c.chatter.dense.json');
const BASE = fx('base.json');
const MONTH = '2026-09';
const MAX_DRAWN_H = 520;
const CHAR_W = 0.6;
const EPS = 0.5;

const OV = {};
for (const pair of (process.env.CHECK_SRC_OVERRIDE || '').split(';').filter(Boolean)) { const i = pair.indexOf('='); OV[pair.slice(0, i)] = pair.slice(i + 1); }
const srcText = (rel) => { const f = OV[rel] || path.join(L.base, rel); return fs.existsSync(f) ? fs.readFileSync(f, 'utf8').replace(/\r\n/g, '\n') : null; };
const decode = (s) => String(s).replace(/&amp;/g, '&').replace(/&quot;/g, '"').replace(/&#x27;/g, "'").replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&#39;/g, "'");
const norm = (s) => decode(s).replace(/\s+/g, ' ').trim();

// ---------- parsing ----------
function attrsOf(s) { const o = {}; const re = /([^\s=\/]+)(?:="([^"]*)")?/g; let m; while ((m = re.exec(s)) !== null) o[m[1]] = m[2] === undefined ? '' : decode(m[2]); return o; }
function openTags(html, from, to) {
  const out = []; const re = /<([a-zA-Z][a-zA-Z0-9.]*)((?:\s+[^\s=>\/]+(?:="[^"]*")?)*)\s*(\/?)>/g; re.lastIndex = from || 0; let m;
  while ((m = re.exec(html)) !== null && (to === undefined || m.index < to)) out.push({ tag: m[1].toLowerCase(), attrs: attrsOf(m[2]), index: m.index, end: re.lastIndex, self: m[3] === '/' });
  return out;
}
function closeOf(html, tag, from) { // index of the matching </tag> for an element opened before `from`
  let depth = 1; const re = new RegExp('<(/?)' + tag + '\\b[^>]*?(/?)>', 'g'); re.lastIndex = from; let m;
  while ((m = re.exec(html)) !== null) { if (m[2] === '/') continue; depth += m[1] === '/' ? -1 : 1; if (depth === 0) return m.index; }
  return html.length;
}
const num = (v) => (v === undefined || v === null || String(v).trim() === '' ? NaN : Number(String(v).replace(/px$/, '')));
function lenOf(v, fs) { if (v === undefined) return 0; const s = String(v).trim(); if (/em$/.test(s)) return Number(s.slice(0, -2)) * fs; return num(s); }
function styleOf(s) { const o = {}; for (const part of String(s || '').split(';')) { const i = part.indexOf(':'); if (i > 0) o[part.slice(0, i).trim().toLowerCase()] = part.slice(i + 1).trim(); } return o; }

/** The collage model: {faults, box:{x,y,w,h,raw}, drawnH, bubbles:[{key,cx,cy,r,hover}], texts:[{key,lines:[{text,x0,x1,y0,y1}]}]} */
function parseCollage(html) {
  const faults = [];
  const first = html.search(/\sdata-bubble="/);
  if (first < 0) return { faults: ['NO BUBBLES: no [data-bubble] element'], bubbles: [], texts: [] };
  const svgAt = html.lastIndexOf('<svg', first);
  if (svgAt < 0) return { faults: ['NO SVG around the bubbles'], bubbles: [], texts: [] };
  const svgOpen = openTags(html, svgAt)[0];
  const svgEnd = closeOf(html, 'svg', svgOpen.end);
  const vb = String(svgOpen.attrs.viewBox || '').trim().split(/[\s,]+/).map(Number);
  const box = vb.length === 4 && vb.every(Number.isFinite) ? { x: vb[0], y: vb[1], w: vb[2], h: vb[3], raw: vb.join(' ') } : null;
  if (!box) faults.push('NO VIEWBOX on the collage svg');
  const st = styleOf(svgOpen.attrs.style);
  const hs = [num(svgOpen.attrs.height), num(st.height), num(st['max-height'])].filter((x) => Number.isFinite(x) && !/%|vh|em/.test(String(x)));
  const drawnH = hs.length ? Math.min(...hs) : null;
  const tags = openTags(html, svgOpen.end, svgEnd);
  for (const t of tags) if (t.attrs.transform !== undefined || /transform\s*:/.test(t.attrs.style || '')) { faults.push(`TRANSFORM inside the collage svg on <${t.tag}>: positions must be absolute`); break; }
  const all = (html.match(/\sdata-bubble="/g) || []).length;
  const bubbles = [];
  for (const t of tags) {
    if (t.attrs['data-bubble'] === undefined) continue;
    if (t.tag !== 'circle') { faults.push(`BUBBLE NOT A CIRCLE: [data-bubble="${t.attrs['data-bubble']}"] is a <${t.tag}>`); continue; }
    const end = t.self ? t.end : closeOf(html, 'circle', t.end);
    const ti = /<title>([\s\S]*?)<\/title>/.exec(html.slice(t.end, end));
    bubbles.push({ key: t.attrs['data-bubble'], cx: num(t.attrs.cx), cy: num(t.attrs.cy), r: num(t.attrs.r), fill: t.attrs.fill, hover: ti ? norm(ti[1]) : '' });
  }
  if (bubbles.length !== all) faults.push(`SPLIT: ${all - bubbles.length} [data-bubble] element(s) outside the collage svg`);
  const texts = [];
  const tre = /<text\b([^>]*)>([\s\S]*?)<\/text>/g; tre.lastIndex = svgOpen.end; let m;
  while ((m = tre.exec(html)) !== null && m.index < svgEnd) {
    const a = attrsOf(m[1]); const fs0 = num(a['font-size']); const anchor = a['text-anchor'] || 'start'; const base = a['dominant-baseline'] || '';
    const lines = []; let cx = num(a.x); let cy = num(a.y);
    if (!Number.isFinite(cx)) cx = 0; if (!Number.isFinite(cy)) cy = 0;
    const parts = /<tspan\b/.test(m[2]) ? [...m[2].matchAll(/<tspan\b([^>]*)>([\s\S]*?)<\/tspan>/g)].map((x) => [attrsOf(x[1]), x[2]]) : [[{}, m[2]]];
    for (const [ta, body] of parts) {
      const fs = Number.isFinite(num(ta['font-size'])) ? num(ta['font-size']) : fs0;
      if (ta.x !== undefined) cx = num(ta.x); if (ta.y !== undefined) cy = num(ta.y);
      cx += lenOf(ta.dx, fs); cy += lenOf(ta.dy, fs);
      const text = norm(body.replace(/<[^>]*>/g, ''));
      if (!text) continue;
      if (!Number.isFinite(fs) || fs <= 0) { faults.push(`NO FONT-SIZE on a text "${text.slice(0, 24)}"`); continue; }
      const w = CHAR_W * fs * text.length;
      const x0 = anchor === 'middle' ? cx - w / 2 : anchor === 'end' ? cx - w : cx;
      const [u, d] = /middle|central/.test(base) ? [0.6, 0.6] : /hanging|text-before-edge/.test(base) ? [0, 1.2] : [0.9, 0.3];
      lines.push({ text, x0, x1: x0 + w, y0: cy - u * fs, y1: cy + d * fs });
    }
    texts.push({ key: a['data-bubble-label'] === undefined ? null : a['data-bubble-label'], lines, joined: lines.map((l) => l.text) });
  }
  return { faults, box, drawnH, bubbles, texts };
}

// ---------- predicates ----------
function spearman(xs, ys) {
  const rank = (v) => { const idx = v.map((x, i) => [x, i]).sort((a, b) => a[0] - b[0]); const r = new Array(v.length); let i = 0;
    while (i < idx.length) { let j = i; while (j + 1 < idx.length && idx[j + 1][0] === idx[i][0]) j++; for (let k = i; k <= j; k++) r[idx[k][1]] = (i + j) / 2 + 1; i = j + 1; } return r; };
  const a = rank(xs); const b = rank(ys); const n = xs.length; const ma = a.reduce((s, x) => s + x, 0) / n; const mb = b.reduce((s, x) => s + x, 0) / n;
  let num_ = 0; let da = 0; let db = 0; for (let i = 0; i < n; i++) { num_ += (a[i] - ma) * (b[i] - mb); da += (a[i] - ma) ** 2; db += (b[i] - mb) ** 2; }
  return da && db ? num_ / Math.sqrt(da * db) : 0;
}
/** collected: Map key -> served count for the month shown. */
function geomFaults(c, collected) {
  const f = [...c.faults.filter((x) => !/^NO FONT-SIZE/.test(x))];
  if (!c.box) return f;
  const keys = c.bubbles.map((b) => b.key);
  const dup = keys.filter((k, i) => keys.indexOf(k) !== i);
  if (dup.length) f.push(`DUPLICATE bubbles: ${dup.slice(0, 3).join(', ')}`);
  const miss = [...collected.keys()].filter((k) => !keys.includes(k));
  const extra = keys.filter((k) => !collected.has(k));
  if (miss.length) f.push(`MISSING ${miss.length} bubble(s), e.g. ${miss.slice(0, 2).join(', ')}`);
  if (extra.length) f.push(`EXTRA ${extra.length} bubble(s) for names not collected, e.g. ${extra.slice(0, 2).join(', ')}`);
  const B = c.bubbles.filter((b) => collected.has(b.key));
  for (const b of B) if (![b.cx, b.cy, b.r].every(Number.isFinite) || b.r <= 0) f.push(`BAD GEOMETRY on ${b.key}: cx=${b.cx} cy=${b.cy} r=${b.r}`);
  const G = B.filter((b) => [b.cx, b.cy, b.r].every(Number.isFinite) && b.r > 0);
  let over = 0; let ex = '';
  for (let i = 0; i < G.length; i++) for (let j = i + 1; j < G.length; j++) {
    const d = Math.hypot(G[i].cx - G[j].cx, G[i].cy - G[j].cy);
    if (d < G[i].r + G[j].r - EPS) { over += 1; if (!ex) ex = `${G[i].key} x ${G[j].key} (gap ${(d - G[i].r - G[j].r).toFixed(1)})`; }
  }
  if (over) f.push(`OVERLAP: ${over} circle pair(s), e.g. ${ex}`);
  const out = G.filter((b) => b.cx - b.r < c.box.x - EPS || b.cy - b.r < c.box.y - EPS || b.cx + b.r > c.box.x + c.box.w + EPS || b.cy + b.r > c.box.y + c.box.h + EPS);
  if (out.length) f.push(`OUTSIDE THE BOX: ${out.length} circle(s), e.g. ${out[0].key}`);
  if (G.length) {
    const ratios = G.map((b) => (b.r * b.r) / collected.get(b.key)).sort((a, b) => a - b);
    const med = ratios[Math.floor(ratios.length / 2)];
    const bad = G.filter((b) => Math.abs((b.r * b.r) / collected.get(b.key) / med - 1) > 0.02);
    if (bad.length) f.push(`AREA LAW: ${bad.length} bubble(s) whose area is not proportional to the collected count, e.g. ${bad[0].key}`);
    const cx = c.box.x + c.box.w / 2; const cy = c.box.y + c.box.h / 2;
    const top = Math.max(...G.map((b) => collected.get(b.key)));
    const largest = G.filter((b) => collected.get(b.key) === top);
    if (!largest.some((b) => Math.hypot(b.cx - cx, b.cy - cy) <= b.r + EPS)) f.push(`NOT CENTRED: the box centre (${cx.toFixed(0)},${cy.toFixed(0)}) is outside the largest bubble ${largest[0].key} at (${largest[0].cx.toFixed(0)},${largest[0].cy.toFixed(0)})`);
    if (G.length >= 5) {
      // Distance in box-relative units (dx / half-width, dy / half-height): "outward" in a wide panel is elliptical.
      const rho = spearman(G.map((b) => b.r), G.map((b) => Math.hypot((b.cx - cx) / (c.box.w / 2), (b.cy - cy) / (c.box.h / 2))));
      if (!(rho <= -0.5)) f.push(`NOT FALLING OUTWARD: Spearman rho(radius, box-relative distance from centre) = ${rho.toFixed(2)} (needs <= -0.50)`);
    }
  }
  if (c.drawnH === null) f.push('UNBOUNDED HEIGHT: the collage svg has no numeric height (attribute or inline style height/max-height in px)');
  else if (c.drawnH > MAX_DRAWN_H) f.push(`TOO TALL: drawn height ${c.drawnH} > ${MAX_DRAWN_H}`);
  return f;
}
function boxFault(a, b) { return a.box && b.box && a.box.raw === b.box.raw ? null : `BOX GROWS: viewBox "${a.box && a.box.raw}" at ${a.n} names vs "${b.box && b.box.raw}" at ${b.n} names`; }
/** names: Map key -> served display name. */
function labelFaults(c, names) {
  const f = [...c.faults.filter((x) => /^NO FONT-SIZE|^TRANSFORM/.test(x))];
  if (!c.box) return f.concat(['NO VIEWBOX']);
  const byKey = new Map();
  for (const t of c.texts) if (t.key !== null) byKey.set(t.key, (byKey.get(t.key) || []).concat([t]));
  let missing = 0; let bad = 0; let ex = '';
  for (const b of c.bubbles) {
    const ls = byKey.get(b.key) || [];
    if (ls.length !== 1) { missing += 1; if (!ex) ex = `${b.key}: ${ls.length} labels`; continue; }
    const name = norm(names.get(b.key) || '');
    const shown = [ls[0].joined.join(' '), ls[0].joined.join('')].map((s) => s.replace(/\s+/g, ' ').trim());
    if (shown.includes(name)) continue;
    const short = shown.map((s) => /(\.\.\.|\u2026)$/.exec(s) ? s.replace(/(\.\.\.|\u2026)$/, '').trim() : null).filter((s) => s !== null);
    const okShort = short.some((s) => s.length >= Math.min(3, name.length) && (name.startsWith(s) || name.replace(/\s+/g, '').startsWith(s.replace(/\s+/g, ''))));
    if (!okShort) { bad += 1; if (!ex) ex = `${b.key}: label "${shown[0]}" is neither the name "${name}" nor a >=3-character shortening`; }
    else if (!b.hover.includes(name)) { bad += 1; if (!ex) ex = `${b.key}: shortened label but the hover lacks the full name`; }
  }
  const orphan = [...byKey.keys()].filter((k) => !c.bubbles.some((b) => b.key === k));
  if (missing) f.push(`LABEL COUNT: ${missing} bubble(s) without exactly one [data-bubble-label], e.g. ${ex}`);
  if (bad) f.push(`LABEL TEXT: ${bad} label(s) wrong, e.g. ${ex}`);
  if (orphan.length) f.push(`ORPHAN LABEL(S): ${orphan.slice(0, 2).join(', ')}`);
  const lines = []; c.texts.forEach((t, ti) => t.lines.forEach((l) => lines.push({ ...l, ti, key: t.key })));
  const clip = lines.filter((l) => l.x0 < c.box.x - EPS || l.y0 < c.box.y - EPS || l.x1 > c.box.x + c.box.w + EPS || l.y1 > c.box.y + c.box.h + EPS);
  if (clip.length) f.push(`CLIPPED: ${clip.length} text line(s) leave the box, e.g. "${clip[0].text}"`);
  let over = 0; let oex = '';
  for (let i = 0; i < lines.length; i++) for (let j = i + 1; j < lines.length; j++) {
    const p = lines[i]; const q = lines[j];
    if (Math.min(p.x1, q.x1) - Math.max(p.x0, q.x0) > EPS && Math.min(p.y1, q.y1) - Math.max(p.y0, q.y0) > EPS) { over += 1; if (!oex) oex = `"${p.text}" x "${q.text}"`; }
  }
  if (over) f.push(`LABELS OVERLAP: ${over} text-line pair(s), e.g. ${oex}`);
  return f;
}

// ---------- inputs ----------
function litOf(data, month) {
  const collected = new Map(); const names = new Map();
  for (const r of data.rows) { names.set(r.security_key, r.display_name); const e = r.by_month[month]; if (e && e.collected > 0) collected.set(r.security_key, e.collected); }
  return { collected, names };
}
let M = null; let loadErr = null;
try { M = L.source(CB); } catch (e) { loadErr = 'RENDER: ' + String(e.message).split('\n')[0]; }
const renderOf = (data, extra) => L.render(M.ChatterBubbles, { data, month: MONTH, onSelectSecurity: () => {}, ...(extra || {}) });
const SETS = [['17-name month', TONED], ['95-name month', DENSE]];
const renders = [];
for (const [label, data] of SETS) {
  const r = { label, data, ...litOf(data, MONTH) };
  try { r.html = M ? renderOf(data, { onMonthChange: () => {} }) : null; } catch (e) { r.err = 'RENDER: ' + String(e.message).split('\n')[0]; }
  if (r.html) { r.c = parseCollage(r.html); r.c.n = r.collected.size; }
  renders.push(r);
}

const arms = [];
// Arm 1 -- PACKED.
{
  const f = [];
  if (loadErr) f.push(loadErr);
  for (const r of renders) {
    if (r.err) { f.push(`${r.label}: ${r.err}`); continue; }
    if (!r.c) continue;
    f.push(...geomFaults(r.c, r.collected).map((x) => `${r.label}: ${x}`));
  }
  if (renders.every((r) => r.c)) { const bf = boxFault(renders[0].c, renders[1].c); if (bf) f.push(bf); }
  arms.push(['PACKED: one bubble per collected name, no overlap, inside one fixed bounded box, largest at the centre, smaller outward', f.length === 0,
    f.length === 0 ? renders.map((r) => `${r.label}: ${r.c.bubbles.length} bubbles in ${r.c.box.raw}`).join('; ') : f.slice(0, 5).join(' | ')]);
}
// Arm 2 -- LABELS.
{
  const f = [];
  if (loadErr) f.push(loadErr);
  for (const r of renders) {
    if (r.err) { f.push(`${r.label}: ${r.err}`); continue; }
    if (!r.c) continue;
    f.push(...labelFaults(r.c, r.names).map((x) => `${r.label}: ${x}`));
  }
  arms.push(['LABELS: one full-or-shortened label per bubble; no text line clips the box or overlaps another', f.length === 0,
    f.length === 0 ? renders.map((r) => `${r.label}: ${r.c.texts.length} texts clear`).join('; ') : f.slice(0, 5).join(' | ')]);
}
// Arm 3 -- CONTROL.
{
  const f = [];
  const src = srcText(CB) || '';
  if (!M) f.push(loadErr || 'NO MODULE');
  else {
    for (const r of renders) { try { if (renderOf(r.data, { onMonthChange: () => {} }) !== r.html) f.push(`NOT DETERMINISTIC: two renders of the ${r.label} differ`); } catch (e) { f.push('RENDER: ' + e.message); } }
    const hits = src.match(/Math\.random|Date\.now|performance\.now|new Date\(|crypto\./g);
    if (hits) f.push(`NONDETERMINISTIC SOURCE: ${[...new Set(hits)].join(', ')} in ChatterBubbles.tsx`);
    try { if (!/data-chatter-cursor=/.test(renderOf(TONED, { onMonthChange: () => {} }))) f.push('CURSOR GONE: no [data-chatter-cursor] with onMonthChange'); } catch (e) { f.push('RENDER: ' + e.message); }
    const sm = M.stepMonth;
    if (typeof sm !== 'function' || sm(['a', 'b', 'c'], 'b', 1) !== 'c' || sm(['a', 'b', 'c'], 'a', -1) !== 'a' || sm(['a', 'b', 'c'], 'c', 1) !== 'c') f.push('CURSOR: stepMonth not exported or not clamped');
  }
  const pkg = fs.readFileSync(path.join(L.base, 'package.json'));
  const sha = crypto.createHash('sha256').update(pkg).digest('hex');
  if (sha !== BASE.package_json_sha256) f.push(`NEW DEPENDENCY?: portal/package.json sha256 ${sha.slice(0, 12)} != BASE ${BASE.package_json_sha256.slice(0, 12)}`);
  const bare = [...src.matchAll(/(?:from|import)\s*['"]([^'"]+)['"]/g)].map((x) => x[1]).filter((p) => !p.startsWith('.') && !p.startsWith('@/'));
  const foreign = bare.filter((p) => !['react', 'motion/react'].includes(p));
  if (foreign.length) f.push(`FOREIGN IMPORT(S) in ChatterBubbles.tsx: ${foreign.join(', ')}`);
  const id = spawnSync(process.execPath, [path.join(D, 'round27', 'checks', 'identity.cjs')], { cwd: process.cwd(), encoding: 'utf8', timeout: 120000 });
  const idLast = ((id.stdout || '') + (id.stderr || '')).trim().split('\n').pop();
  if (id.status !== 0) f.push(`IDENTITY (round 27) rc=${id.status}: ${idLast}`);
  arms.push(['CONTROL: deterministic, no new dependency, the month cursor stays, the round-27 identity hover still passes', f.length === 0,
    f.length === 0 ? `2 renders byte-equal x 2 inputs; package.json = BASE; imports react + motion/react only; identity: ${idLast}` : f.slice(0, 5).join(' | ')]);
}
// Arm 4 -- PLANTED.
{
  const f = [];
  const people = [['A', 'Alpha Co', 16], ['B', 'Beta', 4], ['C', 'Gamma', 4], ['D', 'Delta Holdings Group', 1], ['E', 'Epsilon', 1], ['F', 'Phi', 1]];
  const collected = new Map(people.map((p) => [p[0], p[2]])); const names = new Map(people.map((p) => [p[0], p[1]]));
  const good = {
    vb: '0 0 400 300', h: 'height="300"',
    c: { A: [200, 150, 40], B: [265, 150, 20], C: [135, 150, 20], D: [200, 80, 10], E: [200, 220, 10], F: [300, 220, 10] },
    t: { A: [200, 154, 10, 'Alpha Co'], B: [265, 153, 8, 'Beta'], C: [135, 153, 8, 'Gamma'], D: [200, 82, 6, 'Del...'], E: [200, 222, 6, 'Epsilon'], F: [300, 222, 6, 'Phi'] },
  };
  const svg = (s) => `<div><svg viewBox="${s.vb}" ${s.h} width="100%">` +
    people.map(([k, n]) => `<g><circle data-bubble="${k}" cx="${s.c[k][0]}" cy="${s.c[k][1]}" r="${s.c[k][2]}"><title>${n}; ${collected.get(k)} articles collected</title></circle>` +
      `<text data-bubble-label="${k}" x="${s.t[k][0]}" y="${s.t[k][1]}" font-size="${s.t[k][2]}" text-anchor="middle">${s.t[k][3]}</text></g>`).join('') + '</svg></div>';
  const mut = (fn) => { const s = JSON.parse(JSON.stringify(good)); fn(s); return s; };
  const judge = (s, other) => { const c = parseCollage(svg(s)); c.n = 6; const x = [...geomFaults(c, collected), ...labelFaults(c, names)]; if (other) { const o = parseCollage(svg(other)); o.n = 60; const bf = boxFault(c, o); if (bf) x.push(bf); } return x; };
  const g = judge(good, good);
  if (g.length) f.push(`the good collage is rejected: ${g[0]}`);
  // Each mutant must be rejected FOR ITS OWN REASON (the fault class named beside it), not merely rejected.
  const M8 = [
    ['overlapping circles', /^OVERLAP/, mut((s) => { s.c.B[0] = 240; s.t.B[0] = 240; })],
    ['a circle over the edge', /^OUTSIDE THE BOX/, mut((s) => { s.c.F[0] = 395; s.t.F[0] = 380; })],
    ['the largest off-centre', /^NOT CENTRED/, mut((s) => { s.vb = '0 0 600 300'; })],
    ['sizes rising outward', /^NOT FALLING OUTWARD/, mut((s) => {
      s.c.B = [330, 240, 20]; s.t.B = [330, 243, 8, 'Beta']; s.c.C = [70, 240, 20]; s.t.C = [70, 243, 8, 'Gamma'];
      s.c.D = [200, 95, 10]; s.t.D = [200, 97, 6, 'Del...']; s.c.E = [200, 205, 10]; s.t.E = [200, 207, 6, 'Epsilon']; s.c.F = [300, 150, 10]; s.t.F = [300, 152, 6, 'Phi'];
    })],
    ['two overlapping labels', /^LABELS OVERLAP/, mut((s) => { s.t.B[0] = 215; })],
    ['a clipped label', /^CLIPPED/, mut((s) => { s.t.F = [398, 222, 6, 'Phi']; })],
    ['a growing box', /^BOX GROWS/, null],
    ['an unbounded drawn height', /^UNBOUNDED HEIGHT/, mut((s) => { s.h = ''; })],
  ];
  let caught = 0;
  for (const [n, why, s] of M8) {
    const x = s === null ? judge(good, mut((o) => { o.vb = '0 0 400 900'; })) : judge(s);
    if (x.some((y) => why.test(y))) caught += 1; else f.push(`mutant "${n}" not rejected for its reason (${x.length ? x[0] : 'accepted'})`);
  }
  arms.push(['PLANTED: the collage and label predicates reject 8 known-bad collages, each for its own reason, and accept a known-good one', f.length === 0,
    f.length === 0 ? `${caught} of 8 rejected for their reason; the good one accepted` : f.join(' | ')]);
}

let pass = 0;
for (const [n, ok, d] of arms) { if (ok) pass += 1; console.log(`${ok ? 'ARM PASS' : 'ARM FAIL'} ${n} :: ${d}`); }
console.log(`THE CHATTER FACE IS ONE PACKED COLLAGE WITH CLEAR LABELS: ${pass} of 4 arms`);
process.exit(pass === 4 ? 0 : 1);
