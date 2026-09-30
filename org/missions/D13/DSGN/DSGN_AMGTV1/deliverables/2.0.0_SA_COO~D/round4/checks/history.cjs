/**
 * history.cjs -- DSGN_AMGTV1 round 4, AV-w-6: THE HISTORY VIEW READS WITH TEN OR MORE NAMES (FWD-3; CTO ruling F1 @ac5433b35b:
 * the lead panel's chart is the highlight chart with legend toggles -- the ModelTiltTimeSeriesView pattern).
 *
 * Usage (repo root): node <this file>
 * Renders the lead panel's rank-history chart (components/RankedChart.tsx) on a SERVED 12-name payload
 * (round4/fixtures/rankSeries.TRENDING_PRICE.12.json: the scoped adapter's read_rank_series over the head 12 rows of the
 * Trending x Price list, 5 landed dates, read complete 60 of 60 keys). recharts is replaced by a stub that writes each
 * element's props into data attributes, so the axis, every line and any recharts legend are readable in static markup.
 * The chart is rendered twice: with no name picked, and with `focusTicker="VLO US"` (the prop that seeds the picked name).
 * Arms:
 *   1  the page asks for ten or more names: constants.ts RANK_SERIES_TOP_N >= 10
 *   2  the dates do not overlap: the X axis does not force every tick (interval is not 0) and carries a minTickGap
 *   3  ONE legend: no recharts <Legend>, and exactly one element carrying data-rank-legend holding one entry per series
 *      (data-series-ticker), each entry a <button> with aria-pressed
 *   4  every line is labelled: each <Line>'s name is the series' served name when one is carried, else the ticker as
 *      written (so "BP/ LN" labels its line whole)
 *   5  one name can be followed: with focusTicker="VLO US" the VLO line is drawn at full strength (strokeOpacity 1 or
 *      unset) and every other line is muted (strokeOpacity < 1); with no name picked every line is full strength; the
 *      12 lines use 12 distinct strokes
 * Prints one line per arm and "HISTORY VIEW: <k> of 5 arms"; exit 0 only at 5 of 5.
 */
const fs = require('fs');
const path = require('path');
const L = require('./_load.cjs');
const React = L.React;

const seen = [];
function rechartsStub(name) {
  const C = (props) => {
    const p = props || {};
    const attrs = { 'data-rc': name };
    for (const k of ['dataKey', 'name', 'stroke', 'strokeOpacity', 'strokeWidth', 'interval', 'minTickGap', 'angle']) {
      if (p[k] !== undefined && typeof p[k] !== 'function' && typeof p[k] !== 'object') attrs['data-rc-' + k.toLowerCase()] = String(p[k]);
    }
    seen.push({ name, props: p });
    return React.createElement('div', attrs, p.children);
  };
  C.displayName = name;
  return C;
}
const cache = {};
L.stubSource('recharts', new Proxy({}, {
  get(_t, key) {
    if (key === '__esModule') return true;
    if (typeof key !== 'string') return undefined;
    if (!cache[key]) cache[key] = rechartsStub(key);
    return cache[key];
  },
}));

const data = L.fixture('rankSeries.TRENDING_PRICE.12.json');
const names = new Map(data.series.map((s) => [s.ticker, s.name || s.company_name || null]));
let chart;
try {
  chart = L.source('src/pages/SecurityAnalysis/components/RankedChart.tsx').RankedChart;
} catch (e) {
  console.log('load failed: ' + String(e.message).split('\n')[0]);
}
const render = (props) => {
  seen.length = 0;
  try {
    const html = L.render(chart, { data, isLoading: false, ...props });
    return { html, els: seen.slice() };
  } catch (e) {
    console.log('render failed: ' + String(e.message).split('\n')[0]);
    return { html: '', els: [] };
  }
};
const plain = render({});
const focus = render({ focusTicker: 'VLO US' });
const lines = (r) => r.els.filter((e) => e.name === 'Line');

// arm 1 -- the page's own constant
const constants = fs.readFileSync(path.join(L.base, 'src/pages/SecurityAnalysis/constants.ts'), 'utf8');
const topN = Number((/RANK_SERIES_TOP_N\s*=\s*(\d+)/.exec(constants) || [])[1] || 0);

// arm 2 -- the X axis
const x = plain.els.find((e) => e.name === 'XAxis');
const xi = x ? x.props.interval : undefined;
const xgap = x ? x.props.minTickGap : undefined;

// arm 3 -- one legend
const rcLegends = plain.els.filter((e) => e.name === 'Legend').length;
const legendCount = (plain.html.match(/data-rank-legend(=|\s|>)/g) || []).length;
const legendInner = L.innerOf(plain.html, 'data-rank-legend') || '';
const entries = (legendInner.match(/data-series-ticker="/g) || []).length;
const buttons = (legendInner.match(/<button[^>]*aria-pressed="(true|false)"[^>]*data-series-ticker=|<button[^>]*data-series-ticker="[^"]*"[^>]*aria-pressed="(true|false)"/g) || []).length;

// arm 4 -- line labels
const lp = lines(plain);
const badLabels = lp.filter((l) => {
  const t = l.props.dataKey;
  const want = names.get(t) || t;
  return l.props.name !== want;
}).map((l) => `${l.props.dataKey}->${l.props.name}`);

// arm 5 -- follow one name
const op = (l) => (l.props.strokeOpacity === undefined ? 1 : Number(l.props.strokeOpacity));
const lf = lines(focus);
const vlo = lf.find((l) => l.props.dataKey === 'VLO US');
const others = lf.filter((l) => l.props.dataKey !== 'VLO US');
const plainAllFull = lp.length > 0 && lp.every((l) => op(l) === 1);
const focusOk = vlo && op(vlo) === 1 && others.length > 0 && others.every((l) => op(l) < 1);
const strokes = new Set(lp.map((l) => String(l.props.stroke)));

const n = data.series.length;
const arms = [
  ['ten or more names requested', topN >= 10, `RANK_SERIES_TOP_N=${topN}`],
  ['dates do not overlap', !!x && xi !== 0 && xi !== '0' && typeof xgap === 'number' && xgap > 0, `XAxis interval=${JSON.stringify(xi)} minTickGap=${JSON.stringify(xgap)}`],
  ['one legend, one button per name', rcLegends === 0 && legendCount === 1 && entries === n && buttons === n, `recharts Legend x${rcLegends}; data-rank-legend x${legendCount}; entries ${entries}/${n}; aria-pressed buttons ${buttons}/${n}`],
  ['every line labelled by name or ticker as written', lp.length === n && badLabels.length === 0, `${lp.length}/${n} lines; mislabelled ${badLabels.length ? JSON.stringify(badLabels.slice(0, 4)) : 'none'}`],
  ['one name can be followed', plainAllFull && !!focusOk && strokes.size === n, `unpicked all full=${plainAllFull}; picked VLO full=${vlo ? op(vlo) === 1 : 'no line'}, others muted=${others.length ? others.every((l) => op(l) < 1) : 'none'}; distinct strokes ${strokes.size}/${n}`],
];
let pass = 0;
for (const [name, ok, detail] of arms) {
  if (ok) pass += 1;
  console.log(`${ok ? 'ARM PASS' : 'ARM FAIL'} ${name} :: ${detail}`);
}
console.log(`HISTORY VIEW: ${pass} of ${arms.length} arms (series ${n})`);
process.exit(pass === arms.length ? 0 : 1);
