/**
 * AV-e-5 AC1 -- THE LEAD PANEL'S CAPTIONS AND EMPTY STATES CARRY NO PARTITION NAME OR OTHER RAW CODE.
 *
 * Input: the served Trending x Price payload (generation 2026-09-25, resolution CROSSED, served_axis TRENDING_PRICE),
 * captured at the cut. The walk hit "Served by the producer partition TRENDING_PRICE" and
 * "No committed ranking for BREAKOUT_CHATTER on this date." on the face.
 *
 * Renders, and censuses together (raw-code classes as raw.cjs):
 *   - components/LeadPanel.tsx: sourceFooterContent(payload), sourceDisclosureText(payload), and the named export
 *     ResolutionNote (exported by this cell) for the served resolution AND for an uncrossed one
 *     {resolution: 'FALLBACK', requested_axis: 'BREAKOUT_CHATTER', served_axis: 'CHATTER'};
 *   - components/RankedList.tsx: the ABSENT, EMPTY and no-rows states with resolution served_axis BREAKOUT_CHATTER.
 * Passes when every one renders non-empty and the combined visible text carries 0 raw codes.
 */
const L = require('./_load.cjs');
const r = L.fixture('rankings.TRENDING_PRICE.json');
const lp = L.source('src/pages/SecurityAnalysis/components/LeadPanel.tsx');
const { RankedList } = L.source('src/pages/SecurityAnalysis/components/RankedList.tsx');
const parts = [];
const missing = [];
const push = (name, html) => {
  if (!html || L.textOf(html).length === 0) missing.push(name);
  parts.push(html || '');
};
const esc = (s) => '<p>' + String(s || '').replace(/</g, '&lt;') + '</p>';
push('sourceFooterContent', esc(lp.sourceFooterContent(r)));
push('sourceDisclosureText', esc(lp.sourceDisclosureText(r) || 'none'));
if (typeof lp.ResolutionNote === 'function') {
  push('ResolutionNote CROSSED', L.render(lp.ResolutionNote, { resolution: r.resolution }));
  push('ResolutionNote FALLBACK', L.render(lp.ResolutionNote, { resolution: { resolution: 'FALLBACK', requested_axis: 'BREAKOUT_CHATTER', served_axis: 'CHATTER' } }));
} else {
  missing.push('ResolutionNote (not exported)');
}
const res = { resolution: 'CROSSED', requested_axis: 'BREAKOUT_CHATTER', served_axis: 'BREAKOUT_CHATTER' };
const base = { starredTickers: new Set(), resolution: res, onToggleStar: () => {}, onSelectSecurity: () => {}, isLoading: false, readError: null };
push('RankedList ABSENT', L.render(RankedList, { ...base, rows: [], rankingStatus: 'ABSENT' }));
push('RankedList EMPTY', L.render(RankedList, { ...base, rows: [], rankingStatus: 'EMPTY' }));
push('RankedList no rows', L.render(RankedList, { ...base, rows: [], rankingStatus: 'SERVED' }));
const c = L.rawCensus(parts.join(''));
const per = Object.keys(L.RAW_CLASSES).map((k) => `${k}=${c[k]}${c[k] ? ' e.g. ' + JSON.stringify(c[k + '_first']) : ''}`).join('; ');
console.log(`rendered ${parts.length - missing.length} of ${parts.length + (typeof lp.ResolutionNote === 'function' ? 0 : 1)} parts; missing=[${missing.join(', ')}]`);
console.log(per);
console.log(`LEAD CAPTIONS RAW CODE: ${c.total} hit(s)${missing.length ? ' -- ' + missing.length + ' part(s) missing' : ''}`);
process.exit(c.total === 0 && missing.length === 0 ? 0 : 1);
