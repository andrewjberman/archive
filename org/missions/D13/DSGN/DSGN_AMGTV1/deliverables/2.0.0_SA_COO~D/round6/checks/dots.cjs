/**
 * dots.cjs -- DSGN_AMGTV1 round 6, AV-u-3: THE HISTORY VIEW -- AN UNPICKED LINE'S DOTS MUTE WITH IT, AND A SERVED NAME LABELS
 * THE LINE (round-5 analysis s.4 item 3, ruling 6; FWD-3).
 *
 * Usage (repo root): node <this file>
 * Renders components/RankedChart.tsx with recharts replaced by a prop-recording stub (pixels are the walk's), on the SERVED
 * 12-name payload (round6/fixtures/rankSeries.TRENDING_PRICE.12.json -- no series carries a name today) and on an ISSUER
 * VARIANT of it where each series carries `name` "Company named <ticker>" (rankSeries.TRENDING_PRICE.12.named.VARIANT.json:
 * NOT served -- AMGT_RESAPP xx-2, which serves the name, is merged but not deployed at the cut; the variant proves the label
 * path only, and the walk grades a label only on a served name).
 * Arms:
 *   1  a picked name's line and dots are full; every OTHER line's dots are muted with it: with focusTicker "VLO US", each
 *      unpicked Line's `dot` is an object carrying fillOpacity, strokeOpacity or opacity < 1 (a dot drawn at full strength
 *      beside a muted stroke is the round-5 walk's "columns of bright dots"), and the picked line's dot is not muted
 *   2  with no pick, every line and every dot is full strength (the control; no dot removed: `dot` is never false)
 *   3  labels: on the named variant every Line's `name` and every legend button's text lead with the served name; on the
 *      served payload (no name) they read the ticker exactly as written ("BP/ LN", "WALMEX* MM") -- never looked up
 * Prints one line per arm and "HISTORY DOTS AND NAMES: <k> of 3 arms"; exit 0 only at 3 of 3.
 */
const L = require('./_load.cjs');
const React = L.React;

const seen = [];
function rc(name) {
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
  get(_t, k) {
    if (k === '__esModule') return true;
    if (typeof k !== 'string') return undefined;
    if (!cache[k]) cache[k] = rc(k);
    return cache[k];
  },
}));
const served = L.fixture('rankSeries.TRENDING_PRICE.12.json');
const named = L.fixture('rankSeries.TRENDING_PRICE.12.named.VARIANT.json');
let chart;
try {
  chart = L.source('src/pages/SecurityAnalysis/components/RankedChart.tsx').RankedChart;
} catch (e) {
  console.log('load failed: ' + String(e.message).split('\n')[0]);
}
function render(data, props) {
  seen.length = 0;
  let html = '';
  try {
    html = L.render(chart, { data, isLoading: false, ...props });
  } catch (e) {
    console.log('render failed: ' + String(e.message).split('\n')[0]);
  }
  return { html, lines: seen.filter((e) => e.name === 'Line') };
}
const num = (v) => (v === undefined || v === null ? 1 : Number(v));
const dotOp = (l) => {
  const d = l.props.dot;
  if (d === false) return -1; // removed, not muted
  if (!d || typeof d !== 'object') return 1;
  return Math.min(num(d.fillOpacity), num(d.strokeOpacity), num(d.opacity));
};
const strokeOp = (l) => num(l.props.strokeOpacity);

const focus = render(served, { focusTicker: 'VLO US' });
const picked = focus.lines.find((l) => l.props.dataKey === 'VLO US');
const others = focus.lines.filter((l) => l.props.dataKey !== 'VLO US');
const a1 = !!picked && dotOp(picked) === 1 && others.length === 11 && others.every((l) => strokeOp(l) < 1 && dotOp(l) >= 0 && dotOp(l) < 1);
const plain = render(served, {});
const a2 = plain.lines.length === 12 && plain.lines.every((l) => strokeOp(l) === 1 && dotOp(l) === 1);

const legendTexts = (html) => {
  const out = [];
  const re = /<button[^>]*data-series-ticker="([^"]*)"[^>]*>([\s\S]*?)<\/button>/g;
  let m;
  while ((m = re.exec(html)) !== null) out.push({ ticker: m[1].replace(/&amp;/g, '&'), text: L.textOf(m[2]) });
  return out;
};
const nv = render(named, {});
const nvLegend = legendTexts(nv.html);
const namedOk = nv.lines.length === 12 && nv.lines.every((l) => l.props.name === `Company named ${l.props.dataKey}`) &&
  nvLegend.length === 12 && nvLegend.every((b) => b.text.startsWith(`Company named ${b.ticker}`));
const svLegend = legendTexts(plain.html);
const tickerOk = plain.lines.every((l) => l.props.name === l.props.dataKey) && svLegend.length === 12 && svLegend.every((b) => b.text.startsWith(b.ticker));
const a3 = namedOk && tickerOk;

const arms = [
  ['an unpicked line\'s dots mute with it; the picked line stays full', a1,
    `picked VLO dot ${picked ? dotOp(picked) : 'no line'}; unpicked ${others.length} -- stroke muted ${others.filter((l) => strokeOp(l) < 1).length}, dot muted ${others.filter((l) => dotOp(l) >= 0 && dotOp(l) < 1).length}, dot removed ${others.filter((l) => dotOp(l) < 0).length}`],
  ['no pick: every line and dot full strength', a2, `${plain.lines.length} lines; full ${plain.lines.filter((l) => strokeOp(l) === 1 && dotOp(l) === 1).length}`],
  ['a served name labels the line and legend; else the ticker as written', a3, `named variant ${namedOk} (legend ${nvLegend.length}); served ticker labels ${tickerOk}`],
];
let pass = 0;
for (const [name, ok, detail] of arms) {
  if (ok) pass += 1;
  console.log(`${ok ? 'ARM PASS' : 'ARM FAIL'} ${name} :: ${detail}`);
}
console.log(`HISTORY DOTS AND NAMES: ${pass} of ${arms.length} arms`);
process.exit(pass === arms.length ? 0 : 1);
