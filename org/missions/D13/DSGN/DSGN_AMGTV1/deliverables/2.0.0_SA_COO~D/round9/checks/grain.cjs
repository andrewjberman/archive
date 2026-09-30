/**
 * grain.cjs -- DSGN_AMGTV1 round 9, AV-p-1: A LEAD-LIST COLUMN IS HEADED BY WHAT ITS VALUES ARE ("Sector"), THE ASSET CLASS READS
 * IN DISPLAY CASE, AND NO CLASSIFICATION VALUE IS CUT SHORT (round-8 analysis ruling 1, which corrects round-7 ruling 5; FWD-2).
 *
 * Usage (repo root): node <this file>
 * The served single-name rows carry classification.sub_asset_class at the GICS-SECTOR grain ("Energy", "Information Technology").
 * Round 8 headed that column "Sub Asset", Positioning's label -- but Positioning's "Sub Asset" holds Opal's buckets ("Ultra Short
 * Duration", "High Yield", "Large"), so the same heading sat over values of a different grain. Ruled: a column is headed by what its
 * VALUES are -- sub_asset_class is headed "Sector", and the unserved finer field `sector` is "Industry group (finer than Sector)".
 * asset_class keeps "Asset Class" and shows its value in display case ("equity" -> "Equity"); a long value is shown whole.
 * Fixtures: the four SERVED lists (round9/fixtures/rankings.*.json) and ONE labelled ISSUER VARIANT (Trending x Price with one row
 * serving classification.sector) so a served finer field's column header is rendered.
 * Arms:
 *   1  the heading follows the grain: on every served non-empty list the sub_asset_class column header reads "Sector" and the
 *      asset_class header reads "Asset Class"; no visible "Sub Asset" anywhere in any rendered list (census: each header beside
 *      a sample of the values under it)
 *   2  the finer field and the note in the same words: the variant's `sector` header reads "Industry group (finer than Sector)";
 *      every served list's one unserved note names "Industry group (finer than Sector)" and "places moved since the last run",
 *      its keys unchanged (data-list-unserved-columns="sector,places_moved")
 *   3  values in display case and whole: every asset_class cell shows the served value with each word's first letter upper-cased
 *      while its data-row-asset-class attribute keeps the served value unchanged; no cell carrying a classification value has a
 *      truncating class (truncate / whitespace-nowrap / text-ellipsis / overflow-hidden); "Communication Services" reads whole
 * Prints the census, one line per arm and "COLUMN HEADED BY ITS GRAIN: <k> of 3 arms"; exit 0 only at 3 of 3.
 */
const L = require('./_load.cjs');
const clone = (x) => JSON.parse(JSON.stringify(x));
const safe = (f) => { try { return f(); } catch (e) { return 'RENDER FAILED ' + String(e.message).split('\n')[0]; } };
const LISTS = ['TRENDING_CHATTER', 'TRENDING_PRICE', 'BREAKOUT_CHATTER', 'BREAKOUT_PRICE'];
const lists = Object.fromEntries(LISTS.map((k) => [k, L.fixture(`rankings.${k}.json`)]));
const SECTOR = 'Sector';
const FINER = 'Industry group (finer than Sector)';

const RL = safe(() => L.source('src/pages/SecurityAnalysis/components/RankedList.tsx'));
const renderList = (payload) => safe(() => L.render(RL.RankedList, {
  rows: payload.rows || [], starredTickers: new Set(), resolution: payload.resolution, onToggleStar: () => {}, onSelectSecurity: () => {},
  isLoading: false, readError: null, rankingStatus: payload.ranking_status, rankingReason: null, emptyReason: null,
}));
const unesc = (s) => s.replace(/&amp;/g, '&').replace(/&quot;/g, '"').replace(/&#x27;/g, "'");
const headerText = (html, key) => {
  const m = new RegExp(`<[a-z]+[^>]*data-list-column="${key}"[^>]*>([\\s\\S]*?)</[a-z]+>`).exec(html || '');
  return m ? unesc(L.textOf(m[1])) : null;
};
const displayCase = (s) => s.replace(/(^|\s)([a-z])/g, (_m, sp, c) => sp + c.toUpperCase());
const CARRIERS = { asset_class: 'data-row-asset-class', sub_asset_class: 'data-row-sub-asset-class', sector: 'data-row-sector' };
/** Every element carrying a classification value: { key, served, cls, text }. */
function cells(html) {
  const out = [];
  // each opening tag that carries a classification attribute, and the text up to the next tag (a value cell holds plain text)
  const re = /<([a-z]+)\b([^>]*\bdata-row-(?:asset-class|sub-asset-class|sector)="[^"]*"[^>]*)>([^<]*)</g;
  let m;
  while ((m = re.exec(html || '')) !== null) {
    for (const [key, attr] of Object.entries(CARRIERS)) {
      const a = new RegExp(`(^|\\s)${attr}="([^"]*)"`).exec(m[2]);
      if (!a) continue;
      const cls = (/\bclass="([^"]*)"/.exec(m[2]) || [])[1] || '';
      out.push({ key, served: unesc(a[2]), cls, text: unesc(L.textOf(m[3])) });
    }
  }
  return out;
}
const TRUNC = /(^|\s)(truncate|whitespace-nowrap|text-ellipsis|overflow-hidden)(\s|$)/;

const va = clone(lists.TRENDING_PRICE);
va.rows[1].classification = Object.assign({}, va.rows[1].classification, { sector: 'Oil, Gas & Consumable Fuels' });
const vaHtml = renderList(va);
const htmls = Object.fromEntries(LISTS.map((k) => [k, renderList(lists[k])]));

// ---- census -----------------------------------------------------------------------------------------------------------------
for (const k of LISTS) {
  if (!(lists[k].rows || []).length) { console.log(`CENSUS ${k}: no rows served`); continue; }
  const cs = cells(htmls[k]);
  for (const key of ['asset_class', 'sub_asset_class']) {
    const sample = [...new Set(cs.filter((c) => c.key === key).map((c) => c.text))].slice(0, 4);
    console.log(`CENSUS ${k} ${key}: header "${headerText(htmls[k], key)}" over ${JSON.stringify(sample)}`);
  }
}
console.log(`CENSUS variant sector: header "${headerText(vaHtml, 'sector')}" over ${JSON.stringify(cells(vaHtml).filter((c) => c.key === 'sector').map((c) => c.text))}`);

// ---- arm 1 ------------------------------------------------------------------------------------------------------------------
const f1 = [];
let n1 = 0;
for (const k of LISTS) {
  if (!(lists[k].rows || []).length) continue;
  n1 += 1;
  if (headerText(htmls[k], 'sub_asset_class') !== SECTOR) f1.push(`${k}: sub_asset_class header "${headerText(htmls[k], 'sub_asset_class')}"`);
  if (headerText(htmls[k], 'asset_class') !== 'Asset Class') f1.push(`${k}: asset_class header "${headerText(htmls[k], 'asset_class')}"`);
}
for (const [k, html] of [...LISTS.map((k) => [k, htmls[k]]), ['variant', vaHtml]]) {
  if (/sub[\s-]*asset/i.test(unesc(L.textOf(html || '')))) f1.push(`${k}: a visible "Sub Asset" in the list`);
}
const a1 = f1.length === 0 && n1 > 0;
const a1d = a1 ? `${n1} served list(s): sub_asset_class headed "${SECTOR}", asset_class "Asset Class"; no visible "Sub Asset"` : `${f1.length} failing; first: ${f1[0]}`;

// ---- arm 2 ------------------------------------------------------------------------------------------------------------------
const f2 = [];
if (headerText(vaHtml, 'sector') !== FINER) f2.push(`variant: the finer field's header reads "${headerText(vaHtml, 'sector')}"`);
for (const k of LISTS) {
  if (!(lists[k].rows || []).length) continue;
  const html = htmls[k];
  const keys = [...html.matchAll(/data-list-unserved-columns="([^"]*)"/g)].map((m) => m[1]);
  const note = (/<p[^>]*data-list-unserved-columns="[^"]*"[^>]*>([\s\S]*?)<\/p>/.exec(html) || [])[1];
  const words = note ? unesc(L.textOf(note)) : '';
  if (keys.length !== 1 || keys[0] !== 'sector,places_moved') f2.push(`${k}: note keys ${JSON.stringify(keys)}`);
  if (!(words.includes(FINER) && /places moved since the last run/.test(words))) f2.push(`${k}: note reads "${words}"`);
}
const a2 = f2.length === 0;
const a2d = a2 ? `the finer field reads "${FINER}" in its header and in every served list's note; keys unchanged` : `${f2.length} failing; first: ${f2[0]}`;

// ---- arm 3 ------------------------------------------------------------------------------------------------------------------
const f3 = [];
let nAsset = 0;
let nCells = 0;
for (const [k, html] of [...LISTS.map((k) => [k, htmls[k]]), ['variant', vaHtml]]) {
  for (const c of cells(html)) {
    nCells += 1;
    if (TRUNC.test(c.cls)) f3.push(`${k}: ${c.key} "${c.served}" carries a truncating class ("${c.cls}")`);
    if (c.key === 'asset_class') {
      nAsset += 1;
      if (c.text !== displayCase(c.served)) f3.push(`${k}: asset_class served "${c.served}" shows "${c.text}" (expected "${displayCase(c.served)}")`);
    } else if (c.text !== c.served) f3.push(`${k}: ${c.key} served "${c.served}" shows "${c.text}"`);
  }
}
if (!unesc(L.textOf(htmls.TRENDING_PRICE || '')).includes('Communication Services')) f3.push('TRENDING_PRICE: "Communication Services" is not whole in the text');
const a3 = f3.length === 0 && nAsset > 0;
const a3d = a3 ? `${nCells} classification cell(s), ${nAsset} asset-class cell(s) in display case, none truncating; the served attribute unchanged` : `${f3.length} failing; first: ${f3[0]}`;

const arms = [
  ['the column is headed by its grain ("Sector")', a1, a1d],
  ['the finer field and the note name it in the same words', a2, a2d],
  ['values in display case and whole', a3, a3d],
];
let pass = 0;
for (const [name, ok, detail] of arms) { if (ok) pass += 1; console.log(`${ok ? 'ARM PASS' : 'ARM FAIL'} ${name} :: ${detail}`); }
console.log(`COLUMN HEADED BY ITS GRAIN: ${pass} of ${arms.length} arms`);
process.exit(pass === arms.length ? 0 : 1);
