/**
 * r63c.cjs -- DSGN_AMGTV1 round 63 issuer CHECK (2.0.0_SA_COO~D1): THE SPINE'S EVENT LABELS NEVER COLLIDE.
 *
 * Usage (from the directory whose portal/ is the checkout under test):
 *   cd "$(git rev-parse --show-toplevel)" && node "org/missions/D13/DSGN/DSGN_AMGTV1/deliverables/2.0.0_SA_COO~D1/round63/checks/r63c.cjs"
 *
 * Why (ledger/ROUND_ANALYSIS.round62.md @4b7ce964a2 section 2 item 5; round-62 walk shot 032, NVDA): components/TimelinePanel.tsx
 * makeMarkerShape draws each event marker's title in a fixed-width box (EVENT_LABEL_W) on one of two rows chosen by markerIndex % 2,
 * so markers close together draw their titles over each other; the titles are also 10px, under the 11px floor.
 * Arms (exit 0 only on all four):
 *   1 NO COLLISION: components/timelineLabels.ts (pure, no page imports) exports layoutEventLabels(items, labelWidth, rows). items are
 *     { x, alignEnd } in pixels, in day order. A label spans [x - 6, x - 6 + labelWidth], or [x + 6 - labelWidth, x + 6] when alignEnd.
 *     It returns one entry per item: a row in [0, rows) such that no two labels on one row overlap, or null when no row is free (that
 *     title is not drawn; the marker stays). It keeps the input order and length, and places every label that fits (loaded through
 *     the real module).
 *   2 USED: TimelinePanel.tsx lays the labels out with layoutEventLabels (no `% 2` row choice), and draws no label whose row is null.
 *   3 READABLE: the event label text is at least 11px (no text-[10px] on data-timeline-event-label).
 *   4 PLANTED.
 * Source read only; no network; writes nothing.
 */
'use strict';
const fs = require('fs');
const path = require('path');
const DD = path.join(__dirname, '..', '..', '..', '2.0.0_SA_COO~D');
const SA = path.join(process.cwd(), 'portal', 'src', 'pages', 'SecurityAnalysis');
const read = (rel) => { try { return fs.readFileSync(path.join(SA, rel), 'utf8'); } catch (e) { return null; } };

const span = (it, w) => (it.alignEnd ? [it.x + 6 - w, it.x + 6] : [it.x - 6, it.x - 6 + w]);

const G = {
  layout: (fn) => {
    if (typeof fn !== 'function') return ['components/timelineLabels.ts exports no layoutEventLabels'];
    const f = [];
    const W = 200;
    const cases = [
      // NVDA-like: a cluster of close markers, then a far one.
      { items: [{ x: 100, alignEnd: false }, { x: 140, alignEnd: false }, { x: 180, alignEnd: false }, { x: 220, alignEnd: false }, { x: 900, alignEnd: true }], rows: 3, mustPlace: [0, 1, 2, 4] },
      { items: [{ x: 50, alignEnd: false }, { x: 400, alignEnd: false }, { x: 800, alignEnd: false }], rows: 2, mustPlace: [0, 1, 2] },
      { items: [], rows: 2, mustPlace: [] },
    ];
    for (const c of cases) {
      let out;
      try { out = fn(c.items, W, c.rows); } catch (e) { f.push('layoutEventLabels threw: ' + e.message); continue; }
      if (!Array.isArray(out) || out.length !== c.items.length) { f.push(`returned ${JSON.stringify(out)} for ${c.items.length} items`); continue; }
      for (let i = 0; i < out.length; i += 1) {
        const r = out[i];
        if (r !== null && !(Number.isInteger(r) && r >= 0 && r < c.rows)) f.push(`item ${i} got row ${JSON.stringify(r)} outside [0, ${c.rows})`);
        for (let j = 0; j < i; j += 1) {
          if (r === null || out[j] !== r) continue;
          const a = span(c.items[i], W); const b = span(c.items[j], W);
          if (a[0] < b[1] && b[0] < a[1]) f.push(`items ${j} and ${i} share row ${r} and overlap`);
        }
      }
      for (const k of c.mustPlace) if (out[k] === null) f.push(`item ${k} (x=${c.items[k].x}) has a free row but was not placed`);
    }
    return f;
  },
  used: (t) => {
    if (t === null) return ['TimelinePanel.tsx missing'];
    const f = [];
    if (!/layoutEventLabels\s*\(/.test(t)) f.push('TimelinePanel.tsx does not lay labels out with layoutEventLabels');
    if (/markerIndex\s*%\s*2/.test(t)) f.push('the label row is still chosen by markerIndex % 2');
    return f;
  },
  readable: (t) => {
    if (t === null) return ['TimelinePanel.tsx missing'];
    const m = /<div[^>]*data-timeline-event-label[^>]*>/.exec(t) || /data-timeline-event-label[\s\S]{0,300}/.exec(t);
    if (!m) return ['no data-timeline-event-label element'];
    return /text-\[(?:[0-9]|10)(?:\.\d+)?px\]/.test(m[0]) ? ['the event label text is under 11px'] : [];
  },
};

const t = read('components/TimelinePanel.tsx');
const arms = [];
const push = (name, f) => arms.push([name, f.length === 0, f.length ? f.join(' | ') : 'holds']);
{
  let fn = null; let e2 = null;
  try {
    const L = require(path.join(DD, 'round15', 'checks', '_load.cjs'));
    fn = L.source('src/pages/SecurityAnalysis/components/timelineLabels.ts').layoutEventLabels;
  } catch (e) { e2 = 'LOADER: ' + String(e.message).split('\n')[0]; }
  push('NO COLLISION', e2 ? [e2] : G.layout(fn));
}
push('USED', G.used(t));
push('READABLE', G.readable(t));
{
  const p = [];
  const greedy = (items, w, rows) => {
    const ends = new Array(rows).fill(-Infinity);
    return items.map((it) => { const [s, e] = span(it, w); const r = ends.findIndex((end) => end <= s); if (r < 0) return null; ends[r] = e; return r; });
  };
  if (G.layout(greedy).length) p.push('the clean layout refused: ' + G.layout(greedy).join('; '));
  if (!G.layout((items) => items.map((_, i) => i % 2)).length) p.push('the round-62 alternation admitted');
  if (!G.layout((items) => items.map(() => null)).length) p.push('a layout that places nothing admitted');
  const r62 = "shape={makeMarkerShape(marker, setSelectedDay, markerIndex % 2, false)}\n<div data-timeline-event-label={marker.words} className=\"truncate text-[10px] leading-[14px]\">";
  if (!G.used(r62).length || !G.readable(r62).length) p.push('the round-62 form admitted');
  const clean = "const rows = layoutEventLabels(items, EVENT_LABEL_W, 3)\n<div data-timeline-event-label={marker.words} className=\"truncate text-[11px] leading-[14px]\">";
  if (G.used(clean).length || G.readable(clean).length) p.push('the clean form refused');
  push('PLANTED', p);
}
let pass = 0;
for (const [name, ok, ev] of arms) { if (ok) pass += 1; console.log(`ARM ${ok ? 'PASS' : 'FAIL'} ${name} :: ${ev}`); }
console.log(`ROUND 63 EVENT LABELS: ${pass} of ${arms.length} arms`);
process.exit(pass === arms.length ? 0 : 1);
