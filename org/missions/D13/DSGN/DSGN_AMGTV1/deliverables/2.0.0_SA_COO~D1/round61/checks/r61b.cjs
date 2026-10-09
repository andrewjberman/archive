/**
 * r61b.cjs -- DSGN_AMGTV1 round 61 issuer CHECK (2.0.0_SA_COO~D1): THE SPINE DRAWS THE SERVED PRICE LINE.
 *
 * Usage (from the directory whose portal/ is the checkout under test):
 *   cd "$(git rev-parse --show-toplevel)" && node "org/missions/D13/DSGN/DSGN_AMGTV1/deliverables/2.0.0_SA_COO~D1/round61/checks/r61b.cjs"
 *
 * Why (ledger/ROUND_ANALYSIS.round60.md @0b03adc339 section 3 item 3): AMGT_RESAPP round 82 (gg-5) serves, on the timeline range
 * route, `price_series` (date-ascending `{date, close}` points), `price_series_source`, and -- only when the series is empty --
 * `price_series_reason`. The spine draws none of it today.
 * Arms (exit 0 only on all three):
 *   1 PRICES PLACED BY DAY: components/timelinePrices.ts (a pure module with no page imports, so the loader can read it) exports
 *     withPrices(series, priceSeries). It returns the spine's own day entries in their order, each with `close` = the served close
 *     for that date, or null. No day is added or dropped, and no value is computed (loaded through the real module).
 *   2 DRAWN, OR SAID ONCE: TimelinePanel.tsx reads the served price_series, draws a line marked data-timeline-price-line, and when
 *     no series is served it draws one line marked data-timeline-price-absent that carries the served price_series_reason.
 *   3 PLANTED: the graders refuse the round-60 form and wrong answers, and admit the clean form.
 * Source read only; no network; writes nothing.
 */
'use strict';
const fs = require('fs');
const path = require('path');
const DD = path.join(__dirname, '..', '..', '..', '2.0.0_SA_COO~D');
const SA = path.join(process.cwd(), 'portal', 'src', 'pages', 'SecurityAnalysis');
const read = (rel) => { try { return fs.readFileSync(path.join(SA, rel), 'utf8'); } catch (e) { return null; } };

const SERIES = [
  { date: '2026-09-01', articles_total: 3 },
  { date: '2026-09-02', articles_total: 0 },
  { date: '2026-09-03', articles_total: 5 },
];
const PRICES = [
  { date: '2026-08-31', close: 9.5 },
  { date: '2026-09-01', close: 10 },
  { date: '2026-09-03', close: 12.5 },
];

const G = {
  placed: (fn) => {
    if (typeof fn !== 'function') return ['components/timelinePrices.ts exports no withPrices'];
    const f = [];
    let out; let none;
    try { out = fn(SERIES, PRICES); } catch (e) { return ['withPrices threw: ' + e.message]; }
    try { none = fn(SERIES, undefined); } catch (e) { f.push('withPrices(series, undefined) threw: ' + e.message); }
    if (!Array.isArray(out)) return ['withPrices returned no array'];
    const dates = out.map((d) => d && d.date).join(',');
    if (dates !== '2026-09-01,2026-09-02,2026-09-03') f.push(`the days moved, were added or dropped: ${dates}`);
    const closes = JSON.stringify(out.map((d) => (d ? d.close : 'missing')));
    if (closes !== '[10,null,12.5]') f.push(`closes ${closes} (wanted [10,null,12.5])`);
    if (out[0] && out[0].articles_total !== 3) f.push('the day entry lost its own fields');
    if (none && JSON.stringify(none.map((d) => d && d.close)) !== '[null,null,null]') f.push('with no served series, a close was invented');
    return f;
  },
  drawn: (t) => {
    if (t === null) return ['TimelinePanel.tsx missing'];
    const f = [];
    if (!/price_series\b/.test(t)) f.push('the panel does not read the served price_series');
    if (!/data-timeline-price-line/.test(t)) f.push('no line marked data-timeline-price-line');
    if (!/data-timeline-price-absent/.test(t)) f.push('no single line for a missing series (data-timeline-price-absent)');
    if (!/price_series_reason/.test(t)) f.push('the missing-series line does not carry the served price_series_reason');
    return f;
  },
};

const arms = [];
const push = (name, f) => arms.push([name, f.length === 0, f.length ? f.join(' | ') : 'holds']);
{
  let fn = null; let err = null;
  try {
    const L = require(path.join(DD, 'round15', 'checks', '_load.cjs'));
    fn = L.source('src/pages/SecurityAnalysis/components/timelinePrices.ts').withPrices;
  } catch (e) { err = 'LOADER: ' + String(e.message).split('\n')[0]; }
  push('PRICES PLACED BY DAY', err ? [err] : G.placed(fn));
}
push('DRAWN, OR SAID ONCE', G.drawn(read('components/TimelinePanel.tsx')));
{
  const p = [];
  const clean = (s, ps) => { const by = new Map((ps || []).map((x) => [x.date, x.close])); return s.map((d) => ({ ...d, close: by.has(d.date) ? by.get(d.date) : null })); };
  if (G.placed(clean).length) p.push('the clean withPrices refused');
  if (!G.placed(undefined).length) p.push('a missing export admitted');
  if (!G.placed((s, ps) => (ps || []).map((x) => ({ ...x }))).length) p.push('a series-shaped answer (days added and dropped) admitted');
  if (!G.placed((s) => s.map((d) => ({ ...d, close: 0 }))).length) p.push('an invented close admitted');
  if (!G.drawn('<BarChart data={series}><Bar dataKey="articles_total" /></BarChart>').length) p.push('the round-60 form admitted');
  if (G.drawn('range.price_series <Line data-timeline-price-line="" /> <p data-timeline-price-absent="">{range.price_series_reason}</p>').length) p.push('the clean form refused');
  push('PLANTED', p);
}
let pass = 0;
for (const [name, ok, ev] of arms) { if (ok) pass += 1; console.log(`ARM ${ok ? 'PASS' : 'FAIL'} ${name} :: ${ev}`); }
console.log(`ROUND 61 SPINE PRICE LINE: ${pass} of ${arms.length} arms`);
process.exit(pass === arms.length ? 0 : 1);
