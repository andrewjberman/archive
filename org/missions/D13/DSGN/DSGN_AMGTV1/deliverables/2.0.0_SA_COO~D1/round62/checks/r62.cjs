/**
 * r62.cjs -- DSGN_AMGTV1 round 62 issuer CHECK (2.0.0_SA_COO~D1), prepared ahead of the round-61 analysis:
 * THE SPINE'S PRICE LINE READS AS ONE LINE, AND ITS AXIS SAYS WHAT IT IS.
 *
 * Usage (from the directory whose portal/ is the checkout under test):
 *   cd "$(git rev-parse --show-toplevel)" && node "org/missions/D13/DSGN/DSGN_AMGTV1/deliverables/2.0.0_SA_COO~D1/round62/checks/r62.cjs"
 *
 * Why (ledger/ROUND_ANALYSIS.round61.md @3e33baad5b section 3 items 1 and 3): TimelinePanel.tsx draws the served closes with
 * connectNulls={false}, and the spine has a day for every calendar day, so the line breaks at every weekend and holiday and reads as
 * dashes; the right-hand price axis has no label. Row Z-W87-S1: types.ts still types CoverageItem.url as `string` (the served feed carries
 * null) and constants.ts still exports HEADER_FEED_VISIBLE_COUNT = 3, which nothing reads since round 60 (News opens ten at rest).
 * Arms (exit 0 only on all six):
 *   1 ONE LINE: the price Line joins across days with no close (connectNulls true), and is still drawn only from served closes.
 *   2 NOTHING INVENTED: components/timelinePrices.ts withPrices still leaves a day with no served close at null (loaded through the
 *     real module): the join is drawn by the chart, never a value placed on the day.
 *   3 THE AXIS SAYS WHAT IT IS: the price YAxis (yAxisId="price") carries a label naming the closing price.
 *   4 THE JOIN IS STATED: the legend's price item (data-timeline-legend-price) says the line is joined across days with no close.
 *   5 THE CURRENT CONTRACT: types.ts CoverageItem.url is `string | null`, and constants.ts no longer exports HEADER_FEED_VISIBLE_COUNT.
 *   6 PLANTED: the graders refuse the round-61 form and admit the clean form.
 * Source read only; no network; writes nothing.
 */
'use strict';
const fs = require('fs');
const path = require('path');
const DD = path.join(__dirname, '..', '..', '..', '2.0.0_SA_COO~D');
const SA = path.join(process.cwd(), 'portal', 'src', 'pages', 'SecurityAnalysis');
const read = (rel) => { try { return fs.readFileSync(path.join(SA, rel), 'utf8'); } catch (e) { return null; } };

// The price <Line ...> and price <YAxis ...> elements, by their yAxisId.
const element = (t, tag) => {
  const re = new RegExp(`<${tag}\\b[^>]*?yAxisId="price"[\\s\\S]*?\\/>`);
  const m = re.exec(t || '');
  return m ? m[0] : '';
};

const G = {
  oneLine: (t) => {
    if (t === null) return ['TimelinePanel.tsx missing'];
    const line = element(t, 'Line');
    if (!line) return ['no price <Line yAxisId="price">'];
    const f = [];
    if (/connectNulls=\{false\}/.test(line) || !/connectNulls(=\{true\})?(\s|\/|$)/.test(line)) f.push('the price line does not join across days with no close (connectNulls)');
    if (!/dataKey="close"/.test(line)) f.push('the price line no longer draws dataKey="close"');
    return f;
  },
  invented: (fn) => {
    if (typeof fn !== 'function') return ['components/timelinePrices.ts exports no withPrices'];
    let out;
    try { out = fn([{ date: '2026-09-04' }, { date: '2026-09-05' }, { date: '2026-09-08' }], [{ date: '2026-09-04', close: 10 }, { date: '2026-09-08', close: 12 }]); } catch (e) { return ['withPrices threw: ' + e.message]; }
    const closes = JSON.stringify((out || []).map((d) => (d ? d.close : 'missing')));
    return closes === '[10,null,12]' ? [] : [`closes ${closes} (wanted [10,null,12]: a weekend day stays null)`];
  },
  axis: (t) => {
    if (t === null) return ['TimelinePanel.tsx missing'];
    const axis = element(t, 'YAxis');
    if (!axis) return ['no price <YAxis yAxisId="price">'];
    return /label=\{\{[^}]*value:\s*'[^']*(closing price|close)[^']*'/i.test(axis) ? [] : ['the price axis carries no label naming the closing price'];
  },
  stated: (t) => {
    if (t === null) return ['TimelinePanel.tsx missing'];
    const m = /data-timeline-legend-price[\s\S]{0,400}?<\/span>\s*<\/span>/.exec(t);
    if (!m) return ['no price legend item (data-timeline-legend-price)'];
    return /no close/i.test(m[0]) ? [] : ['the price legend item does not say the line is joined across days with no close'];
  },
  contract: (types, consts) => {
    const f = [];
    const ci = /interface CoverageItem\s*\{[\s\S]*?\r?\n\}/.exec(types || '');
    if (!ci) f.push('types.ts has no CoverageItem');
    else if (!/\burl\??:\s*string\s*\|\s*null\b/.test(ci[0])) f.push('CoverageItem.url is not typed string | null');
    if (consts === null) f.push('constants.ts missing');
    else if (/HEADER_FEED_VISIBLE_COUNT/.test(consts)) f.push('constants.ts still exports HEADER_FEED_VISIBLE_COUNT');
    return f;
  },
};

const t = read('components/TimelinePanel.tsx');
const arms = [];
const push = (name, f) => arms.push([name, f.length === 0, f.length ? f.join(' | ') : 'holds']);
push('ONE LINE', G.oneLine(t));
{
  let fn = null; let err = null;
  try {
    const L = require(path.join(DD, 'round15', 'checks', '_load.cjs'));
    fn = L.source('src/pages/SecurityAnalysis/components/timelinePrices.ts').withPrices;
  } catch (e) { err = 'LOADER: ' + String(e.message).split('\n')[0]; }
  push('NOTHING INVENTED', err ? [err] : G.invented(fn));
}
push('THE AXIS SAYS WHAT IT IS', G.axis(t));
push('THE JOIN IS STATED', G.stated(t));
push('THE CURRENT CONTRACT', G.contract(read('types.ts'), read('constants.ts')));
{
  const p = [];
  const r61 = '<YAxis\n yAxisId="price"\n orientation="right"\n width={48}\n />\n<Line\n yAxisId="price"\n dataKey="close"\n connectNulls={false}\n />';
  const clean = '<YAxis\n yAxisId="price"\n orientation="right"\n label={{ value: \'Closing price\', angle: 90, position: \'insideRight\' }}\n />\n<Line\n yAxisId="price"\n dataKey="close"\n connectNulls\n />';
  if (!G.oneLine(r61).length || !G.axis(r61).length) p.push('the round-61 form admitted');
  if (G.oneLine(clean).length || G.axis(clean).length) p.push('the clean form refused');
  if (G.oneLine(clean.replace('connectNulls\n', 'connectNulls={true}\n')).length) p.push('connectNulls={true} refused');
  if (!G.invented((s) => s.map((d) => ({ ...d, close: 11 }))).length) p.push('a filled weekend admitted');
  const leg61 = '<span data-timeline-legend-price="" className="x">\n<span aria-hidden="true" />\n<span>Price</span>\n</span>\n</span>';
  if (!G.stated(leg61).length) p.push('the round-61 legend admitted');
  if (G.stated(leg61.replace('<span>Price</span>', '<span>Closing price, joined across days with no close</span>')).length) p.push('the clean legend refused');
  const ty = 'export interface CoverageItem {\n  publisher: string | null\n  url: string\n}';
  if (!G.contract(ty, 'export const HEADER_FEED_VISIBLE_COUNT = 3').length) p.push('the old contract admitted');
  if (G.contract(ty.replace('url: string', 'url: string | null'), 'export const OTHER = 1').length) p.push('the current contract refused');
  push('PLANTED', p);
}
let pass = 0;
for (const [name, ok, ev] of arms) { if (ok) pass += 1; console.log(`ARM ${ok ? 'PASS' : 'FAIL'} ${name} :: ${ev}`); }
console.log(`ROUND 62 PRICE LINE: ${pass} of ${arms.length} arms`);
process.exit(pass === arms.length ? 0 : 1);
