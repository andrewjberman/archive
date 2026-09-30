/**
 * denied.cjs -- DSGN_AMGTV1 round 11, AV-n-3: A "NOT SEARCHED" DAY THAT CARRIES SERVED ARTICLES SAYS HOW THEY WERE FOUND (round-10
 * analysis ruling 4; AMGT_HARVST FWD-5, FWD-11).
 *
 * Usage (repo root): node <this file>
 * 992 HK 2026-02-12 (walk J shot 117) read "NOT SEARCHED ON THIS DAY" above two served articles. The data is honest -- no collection
 * run searched 992 HK that day, and the articles surfaced from other names' searches -- but the page contradicts itself. Ruled: a
 * DENIED day that carries served articles reads "not searched for this company directly -- N articles found in other searches",
 * from served fields only; the coverage state stays AMGT_HARVST's and nothing is re-derived. Renders
 * components/TimelinePanel.tsx (useQuery stubbed, as round 10's surfaces.cjs) on the SERVED 992 HK /timeline and its 2026-08-13
 * /timeline/day (DENIED, 2 articles), plus labelled ISSUER VARIANTS: the same day with 1 article, and with 0 articles.
 * Arms:
 *   1  the day heading: the DENIED day with 2 served articles reads "Not searched for this company directly -- 2 articles found in
 *      other searches" (any case) above its rows; the 1-article variant reads "-- 1 article found in other searches"; neither reads
 *      a bare "Not searched on this day"
 *   2  the day tooltip says the same: the chart tooltip for a DENIED day with articles_total N > 0 reads "not searched for this
 *      company directly -- N article(s) found in other searches", and never "found anyway"
 *   3  nothing else moves (the control): the 0-article DENIED variant still reads "Not searched on this day" with "No articles this
 *      day"; the served rows, their order and their data-dissection-status="DENIED" are unchanged; the legend still reads "not
 *      searched"
 * Prints one line per arm and "A NOT-SEARCHED DAY SAYS HOW ITS ARTICLES WERE FOUND: <k> of 3 arms"; exit 0 only at 3 of 3.
 */
const L = require('./_load.cjs');
const S = require('./surfaces.cjs');
const clone = (x) => JSON.parse(JSON.stringify(x));
const unesc = (s) => String(s).replace(/&amp;/g, '&').replace(/&quot;/g, '"').replace(/&#x27;/g, "'");
const TL = 'src/pages/SecurityAnalysis/components/TimelinePanel.tsx';
const seen = [];
// surfaces.cjs stubs recharts; capture the Tooltip's content element here
const React = L.React;
const rcCache = {};
L.stubSource('recharts', new Proxy({}, {
  get(_t, k) {
    if (k === '__esModule') return true;
    if (typeof k !== 'string') return undefined;
    if (!rcCache[k]) { const C = (p) => { seen.push({ name: k, props: p || {} }); return React.createElement('div', { 'data-rc': k }, (p || {}).children); }; C.displayName = k; rcCache[k] = C; }
    return rcCache[k];
  },
}));
let mod = null;
try { mod = L.source(TL); } catch (e) { console.log('load failed: ' + String(e.message).split('\n')[0]); }
const hk = S.unwrap(L.fixture('timeline.992_HK_Equity.json'));
const day = S.unwrap(L.fixture('timelineDay.992_HK_Equity.2026-08-13.json'));
const renderDay = (body) => { S.q.day = { data: body }; try { return unesc(L.textOf(L.render(mod.DayDissection, { securityKey: '992_HK_Equity', date: body.date }))); } catch (e) { return 'RENDER FAILED ' + e.message; } };

// ---- arm 1 ------------------------------------------------------------------------------------------------------------------
const f1 = [];
const t2 = renderDay(day);
if (!/not searched for this company directly -- 2 articles found in other searches/i.test(t2)) f1.push(`2 articles: reads "${t2.slice(0, 140)}"`);
const one = clone(day); one.articles = one.articles.slice(0, 1);
const t1 = renderDay(one);
if (!/not searched for this company directly -- 1 article found in other searches/i.test(t1)) f1.push(`1 article: reads "${t1.slice(0, 140)}"`);
for (const [n, t] of [['2', t2], ['1', t1]]) if (/not searched on this day/i.test(t)) f1.push(`${n} article(s): still a bare "Not searched on this day"`);
const a1 = f1.length === 0;
const a1d = a1 ? 'the DENIED day with articles says they were found in other searches (2 and 1), never a bare "not searched"' : `${f1.length} failing; first: ${f1[0]}`;

// ---- arm 2 ------------------------------------------------------------------------------------------------------------------
const f2 = [];
S.q.range = { data: hk };
seen.length = 0;
try { L.render(mod.TimelinePanel, { securityKey: '992_HK_Equity' }); } catch (e) { f2.push('panel render failed: ' + e.message); }
const tip = seen.find((e) => e.name === 'Tooltip');
const Content = tip && tip.props.content && tip.props.content.type;
const withArticles = hk.series.find((d) => d.data_status === 'DENIED' && d.articles_total > 0);
let tipText = '';
try { tipText = Content && withArticles ? unesc(L.textOf(L.render(Content, { active: true, payload: [{ payload: withArticles }] }))) : ''; } catch (e) { tipText = 'render failed'; }
const n = withArticles ? withArticles.articles_total : null;
const want = new RegExp(`not searched for this company directly -- ${n} articles? found in other searches`, 'i');
if (!withArticles) f2.push('no DENIED day with articles in the served series');
else if (!want.test(tipText)) f2.push(`tooltip for ${withArticles.date}: "${tipText.slice(0, 140)}"`);
if (/found anyway/i.test(tipText)) f2.push('the tooltip still says "found anyway"');
const a2 = f2.length === 0;
const a2d = a2 ? `the tooltip of a DENIED day with ${n} article(s) says they were found in other searches` : `${f2.length} failing; first: ${f2[0]}`;

// ---- arm 3 ------------------------------------------------------------------------------------------------------------------
const f3 = [];
const none = clone(day); none.articles = [];
const t0 = renderDay(none);
if (!/not searched on this day/i.test(t0) || !/no articles this day/i.test(t0)) f3.push(`0 articles: reads "${t0.slice(0, 120)}"`);
S.q.day = { data: day };
let html = '';
try { html = L.render(mod.DayDissection, { securityKey: '992_HK_Equity', date: day.date }); } catch (e) { html = ''; }
const keys = [...html.matchAll(/data-timeline-article="([^"]*)"/g)].map((m) => m[1].replace(/&amp;/g, '&'));
if (JSON.stringify(keys) !== JSON.stringify(day.articles.map((a) => a.article_key))) f3.push('the served rows or their order changed');
if (!/data-dissection-status="DENIED"/.test(html)) f3.push('data-dissection-status="DENIED" is gone');
S.q.range = { data: hk };
const panel = (() => { try { return unesc(L.textOf(L.render(mod.TimelinePanel, { securityKey: '992_HK_Equity' }))); } catch (e) { return ''; } })();
if (!/not searched/i.test(panel)) f3.push('the legend no longer reads "not searched"');
const a3 = f3.length === 0;
const a3d = a3 ? 'a 0-article DENIED day still reads "Not searched on this day"; rows, order, status and legend unchanged' : `${f3.length} failing; first: ${f3[0]}`;

const arms = [
  ['the day heading says how its articles were found', a1, a1d],
  ['the tooltip says the same, never "found anyway"', a2, a2d],
  ['nothing else moves (control)', a3, a3d],
];
let pass = 0;
for (const [name, ok, detail] of arms) { if (ok) pass += 1; console.log(`${ok ? 'ARM PASS' : 'ARM FAIL'} ${name} :: ${detail}`); }
console.log(`A NOT-SEARCHED DAY SAYS HOW ITS ARTICLES WERE FOUND: ${pass} of ${arms.length} arms`);
process.exit(pass === arms.length ? 0 : 1);
