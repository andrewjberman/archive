/**
 * pick.cjs -- DSGN_AMGTV1 round 5, AV-v-2: THE HISTORY VIEW'S COLOURS, RIGHT EDGE AND PICK (round-4 analysis s.4 item 2;
 * FWD-3).
 *
 * Usage (repo root): node <this file>
 * Renders components/RankedChart.tsx on the SERVED 12-name payload (round5/fixtures/rankSeries.TRENDING_PRICE.12.json).
 * recharts is replaced by a stub that records each element's props, so the chart margin, the X axis and every line are
 * readable without a browser (pixels are the walk's).
 * Arms:
 *   1  distinct colours: the 12 lines' strokes are 12 opaque #RRGGBB hexes, and the MINIMUM CIE76 colour difference over
 *      all 66 pairs is >= 25 (sRGB D65 -> CIELAB; VLO US / WALMEX* MM read 18.1 on the round-4 walk; the base palette's
 *      own minimum is printed)
 *   2  the rightmost date tick has room: the space right of the last tick -- the LineChart `margin.right` plus the XAxis
 *      `padding.right` (0 when unset; a number or {right: n}) -- is >= 24 px (base 8: the angled last label runs past the
 *      chart's right edge and is clipped)
 *   3  one name can still be followed (round 4's pick, kept): with focusTicker="VLO US" the VLO line is full strength and
 *      every other line is muted (strokeOpacity < 1); with no pick every line is full strength
 * Prints one line per arm and "HISTORY PICK, EDGE AND COLOURS: <k> of 3 arms"; exit 0 only at 3 of 3.
 */
const L = require('./_load.cjs');
const React = L.React;

const seen = [];
function rechartsStub(name) {
  const C = (props) => {
    const p = props || {};
    seen.push({ name, props: p });
    return React.createElement('div', { 'data-rc': name }, p.children);
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
let chart;
try {
  chart = L.source('src/pages/SecurityAnalysis/components/RankedChart.tsx').RankedChart;
} catch (e) {
  console.log('load failed: ' + String(e.message).split('\n')[0]);
}
const render = (props) => {
  seen.length = 0;
  try {
    L.render(chart, { data, isLoading: false, ...props });
  } catch (e) {
    console.log('render failed: ' + String(e.message).split('\n')[0]);
  }
  return seen.slice();
};
const plain = render({});
const focus = render({ focusTicker: 'VLO US' });
const lines = (els) => els.filter((e) => e.name === 'Line');

// arm 1 -- CIE76 over sRGB (D65)
function lab(hex) {
  const m = /^#([0-9a-fA-F]{6})$/.exec(String(hex));
  if (!m) return null;
  const c = [0, 2, 4].map((i) => parseInt(m[1].slice(i, i + 2), 16) / 255).map((v) => (v <= 0.04045 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4)));
  const X = (c[0] * 0.4124 + c[1] * 0.3576 + c[2] * 0.1805) / 0.95047;
  const Y = c[0] * 0.2126 + c[1] * 0.7152 + c[2] * 0.0722;
  const Z = (c[0] * 0.0193 + c[1] * 0.1192 + c[2] * 0.9505) / 1.08883;
  const f = (t) => (t > 216 / 24389 ? Math.cbrt(t) : (24389 / 27 * t + 16) / 116);
  return [116 * f(Y) - 16, 500 * (f(X) - f(Y)), 200 * (f(Y) - f(Z))];
}
const lp = lines(plain);
const strokes = lp.map((l) => String(l.props.stroke));
const labs = strokes.map(lab);
let minDe = Infinity;
let minPair = '';
let pairs = 0;
for (let i = 0; i < labs.length; i += 1) {
  for (let j = i + 1; j < labs.length; j += 1) {
    if (!labs[i] || !labs[j]) continue;
    pairs += 1;
    const d = Math.hypot(labs[i][0] - labs[j][0], labs[i][1] - labs[j][1], labs[i][2] - labs[j][2]);
    if (d < minDe) { minDe = d; minPair = `${strokes[i]}/${strokes[j]}`; }
  }
}
const opaque = labs.every(Boolean);
const n = data.series.length;
const wantPairs = (n * (n - 1)) / 2;

// arm 2 -- room right of the last tick
const lc = plain.find((e) => e.name === 'LineChart');
const x = plain.find((e) => e.name === 'XAxis');
const mRight = lc && lc.props.margin && typeof lc.props.margin.right === 'number' ? lc.props.margin.right : 0;
const pad = x ? x.props.padding : undefined;
const pRight = typeof pad === 'number' ? pad : pad && typeof pad.right === 'number' ? pad.right : 0;
const room = mRight + pRight;

// arm 3 -- the pick
const op = (l) => (l.props.strokeOpacity === undefined ? 1 : Number(l.props.strokeOpacity));
const lf = lines(focus);
const vlo = lf.find((l) => l.props.dataKey === 'VLO US');
const others = lf.filter((l) => l.props.dataKey !== 'VLO US');
const plainAllFull = lp.length > 0 && lp.every((l) => op(l) === 1);
const focusOk = !!vlo && op(vlo) === 1 && others.length > 0 && others.every((l) => op(l) < 1);

const arms = [
  ['12 opaque strokes, minimum CIE76 dE >= 25 over every pair', lp.length === n && opaque && pairs === wantPairs && minDe >= 25,
    `${lp.length}/${n} lines; opaque hex ${opaque}; pairs ${pairs}/${wantPairs}; min dE ${Number.isFinite(minDe) ? minDe.toFixed(1) : 'n/a'} (${minPair})`],
  ['the rightmost date tick has room (>= 24 px right of the last tick)', !!lc && !!x && room >= 24,
    `LineChart margin.right ${mRight} + XAxis padding.right ${pRight} = ${room} px`],
  ['one name can still be followed', plainAllFull && focusOk,
    `unpicked all full=${plainAllFull}; picked VLO full=${vlo ? op(vlo) === 1 : 'no line'}, others muted=${others.length ? others.every((l) => op(l) < 1) : 'none'}`],
];
let pass = 0;
for (const [name, ok, detail] of arms) {
  if (ok) pass += 1;
  console.log(`${ok ? 'ARM PASS' : 'ARM FAIL'} ${name} :: ${detail}`);
}
console.log(`HISTORY PICK, EDGE AND COLOURS: ${pass} of ${arms.length} arms`);
process.exit(pass === arms.length ? 0 : 1);
