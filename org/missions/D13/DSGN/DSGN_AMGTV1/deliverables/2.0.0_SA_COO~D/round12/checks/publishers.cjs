/**
 * publishers.cjs -- DSGN_AMGTV1 round 12, AV-m-4: EVERY PUBLISHER THE ESTATE SERVES IS NAMED, A FOUND-ONLY ARTICLE IS NEVER
 * CREDITED TO A SEARCHED PUBLISHER, AND A NEVER-COLLECTED TIMELINE SAYS SO IN WORDS (round-11 analysis ruling 1; FWD-11;
 * AMGT_HARVST FWD-5 page half).
 *
 * Usage (repo root): node <this file>
 * Ruling 1 (HARVST PRD v0.4 `C-HV-COVERED-VS-FOUND`): `publishers_covered_codes` = the publishers whose listing for the name ran
 * that day (SEARCHED); `publishers_found_codes` = the publishers whose articles the day serves. "The page renders a publisher in
 * the FOUND set but not the COVERED set as 'found, listing not run'. Where the field is absent, the page says the day's search
 * record does not say how the articles were found. It never credits a covered publisher with them. The page's publisher-name
 * map names every code the estate serves (bbg included)." The estate's codes are read here from
 * lib/opal_data_harvest/article.schema.json (`publisher` enum).
 * Fixtures (round12/fixtures, SERVED, captured at the cut): 992 HK /timeline/day/2026-08-13 (PARTIAL, covered [bbg], 2 articles
 * from wsj and sa, no `publishers_found_codes` field yet); BA US /timeline/day/2026-09-08 (DENIED, 5 articles from barrons, sa,
 * bbg); BA US /overlay (the news list); 6501 JP /timeline (series [] -- never collected). ISSUER VARIANT (labelled, in memory):
 * the 992 HK day with `publishers_found_codes: ["wsj","sa"]` as HARVST q-5 will serve it.
 * Arms:
 *   1  every served publisher code reads as a name: each code of the estate's enum through `searchedLine` names it (none reads
 *      "no name for yet" or the raw code); the BA day's five article rows and the BA news list show publisher names, never a raw
 *      code (wsj / sa / bbg / barrons / ft) as a word of their own
 *   2  found vs searched: the served 992 HK day names Bloomberg as searched, does not credit it with the 2 articles, and says the
 *      day's search record does not say how they were found; the planted variant reads The Wall Street Journal and Seeking Alpha
 *      as "found, listing not run" and still names Bloomberg as searched
 *   3  the never-collected timeline (6501 JP) says so in words with no field or table name (no "chatter_daily", "security_key"
 *      or underscore token), and the control holds: the BA DENIED day still reads "Not searched for this company directly -- 5
 *      articles found in other searches"
 * Prints one line per arm and "PUBLISHERS NAMED, FOUND NEVER CREDITED: <k> of 3 arms"; exit 0 only at 3 of 3.
 */
const fs = require('fs');
const path = require('path');
const L = require('./_load.cjs');
const S = require('./surfaces.cjs');
const clone = (x) => JSON.parse(JSON.stringify(x));
const unesc = (s) => String(s).replace(/&amp;/g, '&').replace(/&quot;/g, '"').replace(/&#x27;/g, "'");
const TL = 'src/pages/SecurityAnalysis/components/TimelinePanel.tsx';
const HB = 'src/pages/SecurityAnalysis/components/HeaderBrief.tsx';
const codes = JSON.parse(fs.readFileSync(path.join(process.cwd(), 'lib/opal_data_harvest/article.schema.json'), 'utf8')).properties.publisher.enum;
const RAWCODE = new RegExp(`(^|[^A-Za-z])(${codes.join('|')})([^A-Za-z]|$)`);

let tl = null;
try { tl = L.source(TL); } catch (e) { console.log('load failed: ' + String(e.message).split('\n')[0]); }
let hb = null;
try { hb = L.source(HB); } catch (e) { console.log('load failed: ' + String(e.message).split('\n')[0]); }
const hkDay = S.unwrap(L.fixture('timelineDay.992_HK_Equity.2026-08-13.json'));
const baDay = S.unwrap(L.fixture('timelineDay.BA_US_Equity.2026-09-08.json'));
const baOverlay = S.unwrap(L.fixture('overlay.BA_US_Equity.json'));
const never = S.unwrap(L.fixture('timeline.6501_JP_Equity.json'));
const renderDay = (key, body) => { S.q.day = { data: body }; try { return L.render(tl.DayDissection, { securityKey: key, date: body.date }); } catch (e) { return 'RENDER FAILED ' + e.message; } };

// ---- arm 1 ------------------------------------------------------------------------------------------------------------------
const f1 = [];
for (const c of codes) {
  let line = '';
  try { line = tl.searchedLine([c], 1); } catch (e) { line = 'searchedLine failed'; }
  if (/no name for yet/i.test(line) || RAWCODE.test(line.replace(/^Searched:/, ''))) f1.push(`code ${c} reads "${line}"`);
}
const baHtml = renderDay('BA_US_Equity', baDay);
const rows = [...baHtml.matchAll(/<li[^>]*data-timeline-article="[^"]*"[^>]*>([\s\S]*?)<\/li>/g)].map((m) => unesc(L.textOf(m[1])));
if (rows.length !== baDay.articles.length) f1.push(`${rows.length} BA article rows, want ${baDay.articles.length}`);
for (const r of rows) if (RAWCODE.test(r)) { f1.push(`a BA article row shows a raw publisher code: "${r.slice(0, 100)}"`); break; }
let news = '';
try { news = L.render(hb.HeaderBrief, { bundle: baOverlay, isLoading: false }); } catch (e) { news = 'RENDER FAILED ' + e.message; }
const items = [...news.matchAll(/<li[^>]*data-feed-item="[^"]*"[^>]*>([\s\S]*?)<\/li>/g)].map((m) => unesc(L.textOf(m[1])));
if (items.length === 0) f1.push('the BA news list rendered no item');
for (const r of items) if (RAWCODE.test(r)) { f1.push(`a BA news item shows a raw publisher code: "${r.slice(0, 100)}"`); break; }
const a1 = f1.length === 0;
const a1d = a1 ? `all ${codes.length} served codes (${codes.join(', ')}) read as names; ${rows.length} BA day rows and ${items.length} BA news item(s) name their publisher` : `${f1.length} failing; first: ${f1[0]}`;

// ---- arm 2 ------------------------------------------------------------------------------------------------------------------
const f2 = [];
const t2 = unesc(L.textOf(renderDay('992_HK_Equity', hkDay)));
if (!/Bloomberg/.test(t2)) f2.push(`the served day does not name Bloomberg as searched: "${t2.slice(0, 160)}"`);
if (/Searched:[^.]*Bloomberg[^.]*--\s*\d+\s*found/i.test(t2)) f2.push('the served day credits Bloomberg with the articles ("Searched: Bloomberg -- 2 found")');
if (!/does not say how/i.test(t2)) f2.push('the served day (no found set) does not say its search record does not say how the articles were found');
const planted = clone(hkDay); planted.publishers_found_codes = ['wsj', 'sa'];
const tp = unesc(L.textOf(renderDay('992_HK_Equity', planted)));
if (!/found, listing not run/i.test(tp)) f2.push(`the planted found set does not read "found, listing not run": "${tp.slice(0, 160)}"`);
if (!/Wall Street Journal/.test(tp) || !/Seeking Alpha/.test(tp)) f2.push('the planted found-only publishers are not named');
if (!/Bloomberg/.test(tp)) f2.push('the planted variant no longer names Bloomberg as searched');
if (/Searched:[^.]*(Wall Street Journal|Seeking Alpha)/i.test(tp)) f2.push('a found-only publisher is listed as searched');
const a2 = f2.length === 0;
const a2d = a2 ? 'the served day names Bloomberg as searched and says the record does not say how the 2 were found; the planted found set reads "found, listing not run" for the WSJ and Seeking Alpha' : `${f2.length} failing; first: ${f2[0]}`;

// ---- arm 3 ------------------------------------------------------------------------------------------------------------------
const f3 = [];
S.q.range = { data: never };
let n3 = '';
try { n3 = unesc(L.textOf(L.render(tl.TimelinePanel, { securityKey: '6501_JP_Equity' }))); } catch (e) { n3 = 'RENDER FAILED ' + e.message; }
if (/chatter_daily|security_key|\b[a-z]+_[a-z_]+\b/.test(n3)) f3.push(`the never-collected state shows a field or table name: "${n3.slice(0, 160)}"`);
if (!/not (been )?collected|no articles have been collected|not collected/i.test(n3)) f3.push(`the never-collected state does not say so: "${n3.slice(0, 160)}"`);
const t3 = unesc(L.textOf(baHtml));
if (!/not searched for this company directly -- 5 articles found in other searches/i.test(t3)) f3.push('the BA DENIED day wording moved');
const a3 = f3.length === 0;
const a3d = a3 ? 'the never-collected timeline says so in words with no field name; the BA DENIED day wording is unchanged' : `${f3.length} failing; first: ${f3[0]}`;

const arms = [
  ['every served publisher code reads as a name', a1, a1d],
  ['a found-only article is never credited to a searched publisher', a2, a2d],
  ['the never-collected timeline in words (and the control)', a3, a3d],
];
let pass = 0;
for (const [name, ok, detail] of arms) { if (ok) pass += 1; console.log(`${ok ? 'ARM PASS' : 'ARM FAIL'} ${name} :: ${detail}`); }
console.log(`PUBLISHERS NAMED, FOUND NEVER CREDITED: ${pass} of ${arms.length} arms`);
process.exit(pass === arms.length ? 0 : 1);
