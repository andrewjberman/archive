/**
 * timeline7.cjs -- DSGN_AMGTV1 round 7, AV-s-3 (page half): "NOT SEARCHED" IN WORDS, A CAPTION THAT NEVER CALLS AN UNSEARCHED
 * RANGE A ZERO, AND THE SERVED EVENTS MARKED WITH THEIR HEADLINES (round-6 analysis ruling 4 and s.4 item 3; AMGT_HARVST FWD-5 /
 * FWD-6).
 *
 * Usage (repo root): node <this file>
 * Renders components/TimelinePanel.tsx (useQuery and recharts stubbed, as round 6's timeline.cjs) on SERVED /timeline payloads
 * captured from the deployed scoped API: 992 HK (271 DENIED + 1 PARTIAL days, 21 days with articles, 3 served events), VLO
 * (272 DENIED, 0 articles, 0 events), ASML (198 DENIED + 74 PARTIAL, 2 days with articles), and the served /timeline/day body
 * for 992 HK 2026-08-13 (data_status DENIED, 2 articles). One ISSUER VARIANT (labelled): ASML with every articles_total set to 0,
 * to reach the mixed searched / not-searched caption.
 * By AMGT_HARVST's rule DENIED means no publisher's listing search reached that day -- not a failed retrieval, not a zero.
 * Arms:
 *   1  DENIED reads "Not searched on this day": the DayDissection for 992 HK 2026-08-13 says so and lists BOTH served articles
 *      in the served order under that line; the day tooltip of a DENIED day says "not searched"; the legend's words carry no
 *      "denied" (the state reads "not searched"); no visible "denied" / "retrieval" anywhere in these renders
 *   2  the all-quiet caption: VLO (every day DENIED) says the range was not searched and never "honest zero" / "real ... zero";
 *      the mixed variant states the SERVED counts (74 searched day(s), 198 not searched); 992 HK (articles served) shows no caption
 *   3  the event layer: the 992 HK render marks each of its 3 served events with a [data-timeline-event] element carrying the
 *      event's lead_headline in visible text; ASML (0 served events) renders none
 * Prints one line per arm and "TIMELINE NOT SEARCHED AND EVENTS: <k> of 3 arms"; exit 0 only at 3 of 3.
 */
const L = require('./_load.cjs');
const React = L.React;
const TL = 'src/pages/SecurityAnalysis/components/TimelinePanel.tsx';
const seen = [];
const rcCache = {};
L.stubSource('recharts', new Proxy({}, {
  get(_t, k) {
    if (k === '__esModule') return true;
    if (typeof k !== 'string') return undefined;
    if (!rcCache[k]) {
      const C = (p) => { seen.push({ name: k, props: p || {} }); return React.createElement('div', { 'data-rc': k }, (p || {}).children); };
      C.displayName = k;
      rcCache[k] = C;
    }
    return rcCache[k];
  },
}));
const q = { range: null, day: null };
L.stubSource('@tanstack/react-query', {
  __esModule: true,
  useQuery: (opts) => {
    const kind = opts && opts.queryKey ? opts.queryKey[1] : 'range';
    return { isLoading: false, isError: false, error: null, data: undefined, refetch: () => {}, ...(q[kind] || {}) };
  },
});
const api = { __esModule: true, apiRequest: () => Promise.resolve(undefined) };
L.stubSource('src/api/api-client.ts', api);
L.stubSource('src/api/api-client', api);
let mod = null;
try { mod = L.source(TL); } catch (e) { console.log('load failed: ' + String(e.message).split('\n')[0]); }
const render = (C, props) => { seen.length = 0; try { return C ? L.render(C, props) : ''; } catch (e) { return 'RENDER FAILED ' + String(e.message).split('\n')[0]; } };
const Panel = mod && mod.TimelinePanel;
const Dissection = mod && mod.DayDissection;

const hk = L.fixture('timeline.992_HK_Equity.json').payload;
const vlo = L.fixture('timeline.VLO_US_Equity.json').payload;
const asml = L.fixture('timeline.ASML_NA_Equity.json').payload;
const hkDay = L.fixture('timelineDay.992_HK_Equity.2026-08-13.json').payload;
const BAD = /\bdenied\b|retrieval/i;

// ---- arm 1 ------------------------------------------------------------------------------------------------------------
q.day = { data: hkDay };
const dis = L.textOf(render(Dissection, { securityKey: '992_HK_Equity', date: '2026-08-13' }));
const heads = hkDay.articles.map((a) => a.headline);
const pos = heads.map((h) => dis.indexOf(h));
const inOrder = pos.every((p) => p >= 0) && pos.every((p, i) => i === 0 || p > pos[i - 1]);
const notSearchedAt = dis.indexOf('Not searched on this day');
const disOk = notSearchedAt >= 0 && inOrder && notSearchedAt < pos[0] && !BAD.test(dis);
q.range = { data: hk };
const hkHtml = render(Panel, { securityKey: '992_HK_Equity' });
const tip = seen.find((e) => e.name === 'Tooltip');
const Content = tip && tip.props.content && tip.props.content.type;
const deniedEntry = hk.series.find((d) => d.date === '2026-08-13');
let tipText = '';
try { tipText = Content ? L.textOf(L.render(Content, { active: true, payload: [{ payload: deniedEntry }] })) : 'no tooltip'; } catch (e) { tipText = 'render failed'; }
const tipOk = /not searched/i.test(tipText) && !BAD.test(tipText);
const legend = L.textOf(L.innerOf(hkHtml, 'data-timeline-legend') || '');
const legendOk = /not searched/i.test(legend) && !BAD.test(legend);
const a1 = disOk && tipOk && legendOk && !BAD.test(L.textOf(hkHtml));
const a1d = `dissection: "Not searched on this day" ${notSearchedAt >= 0}, ${heads.length} served articles in order ${inOrder}, under the line ${notSearchedAt >= 0 && notSearchedAt < pos[0]}, no denied/retrieval ${!BAD.test(dis)}; tooltip "${tipText.slice(0, 90)}"; legend "${legend}"`;

// ---- arm 2 ------------------------------------------------------------------------------------------------------------
const caption = (html) => L.textOf(L.innerOf(html, 'data-timeline-no-articles') || '');
q.range = { data: vlo };
const vloCap = caption(render(Panel, { securityKey: 'VLO_US_Equity' }));
const ZERO = /honest zero|real,? honest|real zero/i;
const vloOk = /not searched/i.test(vloCap) && !ZERO.test(vloCap);
// ISSUER VARIANT (not served): ASML with every day's articles_total set to 0.
const quiet = JSON.parse(JSON.stringify(asml));
for (const d of quiet.series) d.articles_total = 0;
const nDenied = quiet.series.filter((d) => d.data_status === 'DENIED').length;
const nSearched = quiet.series.length - nDenied;
q.range = { data: quiet };
const mixCap = caption(render(Panel, { securityKey: 'ASML_NA_Equity' }));
const mixOk = mixCap.includes(String(nSearched)) && mixCap.includes(String(nDenied)) && /not searched/i.test(mixCap) && !ZERO.test(mixCap);
q.range = { data: hk };
const hkCap = caption(render(Panel, { securityKey: '992_HK_Equity' }));
const a2 = vloOk && mixOk && hkCap === '';
const a2d = `VLO "${vloCap.slice(0, 110)}"; mixed (${nSearched} searched / ${nDenied} not) "${mixCap.slice(0, 110)}"; 992 HK caption ${hkCap ? 'SHOWN' : 'none'}`;

// ---- arm 3 ------------------------------------------------------------------------------------------------------------
const evCount = (html) => (html.match(/data-timeline-event="/g) || []).length;
q.range = { data: hk };
const hkEv = render(Panel, { securityKey: '992_HK_Equity' });
const hkText = L.textOf(hkEv);
const headlinesShown = (hk.events || []).filter((e) => hkText.includes(e.lead_headline)).length;
q.range = { data: asml };
const asmlEv = evCount(render(Panel, { securityKey: 'ASML_NA_Equity' }));
const a3 = (hk.events || []).length === 3 && evCount(hkEv) === 3 && headlinesShown === 3 && asmlEv === 0;
const a3d = `992 HK: ${evCount(hkEv)} [data-timeline-event] of ${(hk.events || []).length} served, ${headlinesShown} headlines visible; ASML: ${asmlEv} of 0 served`;

const arms = [
  ['DENIED reads "Not searched on this day"; a day with articles lists them under it; legend and tooltip say not searched', a1, a1d],
  ['the all-quiet caption says an unsearched range was not searched, never a zero; counts are served', a2, a2d],
  ['each served event is marked with its headline ([data-timeline-event])', a3, a3d],
];
let pass = 0;
for (const [name, ok, detail] of arms) {
  if (ok) pass += 1;
  console.log(`${ok ? 'ARM PASS' : 'ARM FAIL'} ${name} :: ${detail}`);
}
console.log(`TIMELINE NOT SEARCHED AND EVENTS: ${pass} of ${arms.length} arms`);
process.exit(pass === arms.length ? 0 : 1);
