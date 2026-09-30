/**
 * strength.cjs -- DSGN_AMGTV1 round 9, AV-p-2: EACH ARTICLE ROW OF AN OPENED DAY SHOWS THE STRENGTH THAT ORDERS IT ("named N
 * times") AND ITS TIME IN THE ESTATE'S ONE FORM (round-8 analysis rulings 2 and 3; AMGT_HARVST FWD-5, FWD-11).
 *
 * Usage (repo root): node <this file>
 * The served /timeline/day rows are ordered by the server (tier, then mention_count DESC, then time; timeline_api.py:132-139) and
 * the page never re-sorts them. On walk G both 992 HK days showed two rows with the same visible marks (A, in headline yes, in
 * lead yes), so the order had no visible reason; mention_count (8 and 5 on 2026-08-13) is served and was not shown. The time
 * printed as the raw ISO string plus "(instant)". Ruled: the row shows its mention_count in words, and its time in the estate's
 * one form. Renders components/TimelinePanel.tsx DayDissection (useQuery stubbed, as round 7's timeline7.cjs) on the SERVED
 * /timeline/day body for 992 HK 2026-08-13 (round9/fixtures), plus labelled ISSUER VARIANTS built in memory: one row
 * mention_count 1, one row mention_count null, one row published_precision "day", one row published_utc null.
 * Expected times come from the ESTATE'S OWN formatter (src/lib/dateUtils.ts formatPanelTimestamp, loaded here), never typed.
 * Arms:
 *   1  the strength in words: each served row's visible text carries "named <mention_count> times" (8, 5); the variant with 1
 *      reads "named once"; the variant with null carries "not counted" and no "named null" / "named undefined" / "NaN"
 *   2  the time in the one form: an "instant" row shows formatPanelTimestamp(published_utc); a "day" row shows the long date only
 *      (no clock); a null time reads "time not carried"; no row shows an ISO timestamp, "+00:00" or "(instant)" / "(day)"
 *   3  the served order stands: the rendered [data-timeline-article] keys equal the served order, and each row still carries
 *      its tier mark and its in-headline / in-lead words
 * Prints one line per row, one line per arm and "ARTICLE ROWS SHOW STRENGTH AND TIME: <k> of 3 arms"; exit 0 only at 3 of 3.
 */
const L = require('./_load.cjs');
const clone = (x) => JSON.parse(JSON.stringify(x));
const TL = 'src/pages/SecurityAnalysis/components/TimelinePanel.tsx';
const rcCache = {};
L.stubSource('recharts', new Proxy({}, {
  get(_t, k) {
    if (k === '__esModule') return true;
    if (typeof k !== 'string') return undefined;
    if (!rcCache[k]) { const C = (p) => L.React.createElement('div', { 'data-rc': k }, (p || {}).children); C.displayName = k; rcCache[k] = C; }
    return rcCache[k];
  },
}));
const q = { day: null };
L.stubSource('@tanstack/react-query', {
  __esModule: true,
  useQuery: () => ({ isLoading: false, isError: false, error: null, data: undefined, refetch: () => {}, ...(q.day || {}) }),
});
const api = { __esModule: true, apiRequest: () => Promise.resolve(undefined) };
L.stubSource('src/api/api-client.ts', api);
L.stubSource('src/api/api-client', api);
let mod = null;
try { mod = L.source(TL); } catch (e) { console.log('load failed: ' + String(e.message).split('\n')[0]); }
const DU = (() => { try { return L.source('src/lib/dateUtils.ts'); } catch (e) { return {}; } })();
const fmt = DU.formatPanelTimestamp;
const longDate = (d) => String(fmt(null, d) || '').replace(/,\s*\d{1,2}:\d{2}[ap]\s*ET$/i, '');
const Dissection = mod && mod.DayDissection;

const served = L.fixture('timelineDay.992_HK_Equity.2026-08-13.json').payload;
const variant = clone(served);
variant.articles = [
  Object.assign(clone(served.articles[0]), { article_key: 'variant:once', mention_count: 1 }),
  Object.assign(clone(served.articles[1]), { article_key: 'variant:null-count', mention_count: null }),
  Object.assign(clone(served.articles[0]), { article_key: 'variant:day', published_utc: '2026-08-13T00:00:00+00:00', published_precision: 'day' }),
  Object.assign(clone(served.articles[1]), { article_key: 'variant:no-time', published_utc: null, published_precision: null }),
];

/** Render the dissection for one body; return [{ key, text }] per article row in page order. */
function rows(body) {
  q.day = { data: body };
  let html = '';
  try { html = Dissection ? L.render(Dissection, { securityKey: body.security_key, date: body.date }) : ''; } catch (e) { html = ''; }
  const out = [];
  for (const m of html.matchAll(/data-timeline-article="([^"]*)"/g)) {
    const inner = L.innerOf(html.slice(html.lastIndexOf('<', m.index)), 'data-timeline-article', m[1]);
    out.push({ key: m[1].replace(/&amp;/g, '&'), text: L.textOf(inner || '').replace(/&amp;/g, '&') });
  }
  return out;
}
const sRows = rows(served);
const vRows = rows(variant);
for (const r of [...sRows, ...vRows]) console.log(`ROW ${r.key}: "${r.text}"`);
const vBy = Object.fromEntries(vRows.map((r) => [r.key, r.text]));

// ---- arm 1 ------------------------------------------------------------------------------------------------------------------
const f1 = [];
served.articles.forEach((a, i) => {
  const t = (sRows[i] || {}).text || '';
  if (!t.includes(`named ${a.mention_count} times`)) f1.push(`${a.article_key}: no "named ${a.mention_count} times"`);
});
if (!(vBy['variant:once'] || '').includes('named once')) f1.push('variant mention_count 1: no "named once"');
const nt = vBy['variant:null-count'] || '';
if (!nt.includes('not counted') || /named (null|undefined)|NaN/.test(nt)) f1.push(`variant mention_count null reads "${nt}"`);
const a1 = f1.length === 0 && sRows.length === served.articles.length;
const a1d = a1 ? `${sRows.length} served row(s) name their count (${served.articles.map((a) => a.mention_count).join(', ')}); once and not-counted read in words` : `${f1.length || 'rows'} failing; first: ${f1[0] || `rendered ${sRows.length} of ${served.articles.length}`}`;

// ---- arm 2 ------------------------------------------------------------------------------------------------------------------
const f2 = [];
if (!fmt) f2.push('estate formatter not loaded');
served.articles.forEach((a, i) => {
  const t = (sRows[i] || {}).text || '';
  const want = fmt ? fmt(a.published_utc) : null;
  if (!want || !t.includes(want)) f2.push(`${a.article_key}: no "${want}"`);
});
const dayWant = fmt ? longDate('2026-08-13') : null;
const dt = vBy['variant:day'] || '';
if (!dayWant || !dt.includes(dayWant) || /\d{1,2}:\d{2}[ap]\s*ET/i.test(dt)) f2.push(`variant precision day reads "${dt}" (want "${dayWant}", no clock)`);
if (!(vBy['variant:no-time'] || '').includes('time not carried')) f2.push('variant null time: no "time not carried"');
for (const r of [...sRows, ...vRows]) {
  if (/\d{4}-\d{2}-\d{2}T\d{2}:\d{2}|\+00:00|\((instant|day)\)/.test(r.text)) f2.push(`${r.key}: a raw time or precision word in "${r.text}"`);
}
const a2 = f2.length === 0;
const a2d = a2 ? `served times read "${served.articles.map((a) => fmt(a.published_utc)).join('", "')}"; a day-precision row reads "${dayWant}"; no ISO, no precision word` : `${f2.length} failing; first: ${f2[0]}`;

// ---- arm 3 ------------------------------------------------------------------------------------------------------------------
const f3 = [];
const wantKeys = served.articles.map((a) => a.article_key);
if (JSON.stringify(sRows.map((r) => r.key)) !== JSON.stringify(wantKeys)) f3.push(`order ${JSON.stringify(sRows.map((r) => r.key))} vs served ${JSON.stringify(wantKeys)}`);
served.articles.forEach((a, i) => {
  const t = (sRows[i] || {}).text || '';
  if (!t.includes(a.signal_tier) || !/in headline: (yes|no)/.test(t) || !/in lead: (yes|no)/.test(t)) f3.push(`${a.article_key}: tier or headline/lead words missing`);
});
const a3 = f3.length === 0 && sRows.length > 0;
const a3d = a3 ? `served order kept (${wantKeys.length} rows); tier and in-headline / in-lead words kept` : `${f3.length} failing; first: ${f3[0] || 'no rows rendered'}`;

const arms = [
  ['each row shows the strength that orders it, in words', a1, a1d],
  ["each row's time in the estate's one form", a2, a2d],
  ['the served order and the row marks stand', a3, a3d],
];
let pass = 0;
for (const [name, ok, detail] of arms) { if (ok) pass += 1; console.log(`${ok ? 'ARM PASS' : 'ARM FAIL'} ${name} :: ${detail}`); }
console.log(`ARTICLE ROWS SHOW STRENGTH AND TIME: ${pass} of ${arms.length} arms`);
process.exit(pass === arms.length ? 0 : 1);
