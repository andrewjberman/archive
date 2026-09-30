/**
 * labels.cjs -- DSGN_AMGTV1 round 8, AV-q-3: THE LEAD LISTS NAME EACH CLASSIFICATION FIELD WITH POSITIONING'S LABEL FOR THE SAME
 * KEY, AND THE FINER FIELD BY ITS GRAIN -- NEVER A SECOND "SECTOR" (round-7 analysis ruling 5; FWD-2).
 *
 * Usage (repo root): node <this file>
 * The served list rows carry classification {asset_class, sub_asset_class, sector}. For equities sub_asset_class is at the GICS
 * SECTOR grain ("Industrials", "Energy") and `sector` is a separate, finer field ("Banks" under "Financials";
 * lib/research/api/tests/test_list_rows_classification.py:56,:93). Round 7 labelled the columns "Asset class" / "Sub-asset class"
 * and named the unserved finer field "sector" -- a second "sector" beside a column of sector names. The Positioning holdings
 * breakdown (portal/src/components/holdings/HoldingsBreakdownTable.tsx) labels asset_class "Asset Class" and sub_asset_class
 * "Sub Asset", and shows its finer field (industry_group) UNLABELLED beneath the Sub Asset value. So: asset_class and
 * sub_asset_class take Positioning's labels, READ FROM THAT FILE HERE (never typed), and `sector` -- which Positioning does not
 * label -- is named by its grain, with the words "Industry group" and "finer than" the Sub Asset label.
 * Fixtures: the four SERVED lists (round8/fixtures/rankings.*.json) and ONE labelled ISSUER VARIANT (Trending x Price with one
 * row serving classification.sector) so a served finer field's column header is rendered.
 * Arms:
 *   1  Positioning's labels per key: on every served non-empty list the column header for asset_class reads Positioning's
 *      asset-class label and the header for sub_asset_class reads Positioning's sub-asset label
 *   2  the finer field by its grain, never "Sector": with the variant, the `sector` column header reads "Industry group" and
 *      "finer than" and Positioning's sub-asset label; no visible word "Sector"/"sector" anywhere in any rendered list
 *   3  the unserved note uses the same labels: on every served non-empty list the one note (data-list-unserved-columns keys
 *      unchanged: sector, places_moved) names the finer field with the same grain words, and "places moved since the last run"
 * Prints the label census (each key: the page's label beside Positioning's), one line per arm and
 * "CLASSIFICATION LABELS PER POSITIONING: <k> of 3 arms"; exit 0 only at 3 of 3.
 */
const fs = require('fs');
const path = require('path');
const L = require('./_load.cjs');
const clone = (x) => JSON.parse(JSON.stringify(x));
const safe = (f) => { try { return f(); } catch (e) { return 'RENDER FAILED ' + String(e.message).split('\n')[0]; } };
const LISTS = ['TRENDING_CHATTER', 'TRENDING_PRICE', 'BREAKOUT_CHATTER', 'BREAKOUT_PRICE'];
const lists = Object.fromEntries(LISTS.map((k) => [k, L.fixture(`rankings.${k}.json`)]));

// Positioning's labels, read from the breakdown table's own header cells.
const hbt = fs.readFileSync(path.join(L.base, 'src/components/holdings/HoldingsBreakdownTable.tsx'), 'utf8');
const heads = [...hbt.matchAll(/<th\b[^>]*>\s*<span[^>]*>([^<{]+)<\/span>\s*<\/th>/g)].map((m) => m[1].trim());
const POS = { asset_class: heads.find((h) => /^asset\s*class$/i.test(h)) || null, sub_asset_class: heads.find((h) => /^sub[\s-]*asset/i.test(h)) || null };

const RL = safe(() => L.source('src/pages/SecurityAnalysis/components/RankedList.tsx'));
const renderList = (payload) => safe(() => L.render(RL.RankedList, {
  rows: payload.rows || [], starredTickers: new Set(), resolution: payload.resolution, onToggleStar: () => {}, onSelectSecurity: () => {},
  isLoading: false, readError: null, rankingStatus: payload.ranking_status, rankingReason: null, emptyReason: null,
}));
const headerText = (html, key) => {
  const m = new RegExp(`<[a-z]+[^>]*data-list-column="${key}"[^>]*>([\\s\\S]*?)</[a-z]+>`).exec(html || '');
  return m ? L.textOf(m[1]) : null;
};
const unesc = (s) => s.replace(/&amp;/g, '&').replace(/&quot;/g, '"').replace(/&#x27;/g, "'");

const va = clone(lists.TRENDING_PRICE);
va.rows[1].classification = Object.assign({}, va.rows[1].classification, { sector: 'Oil, Gas & Consumable Fuels' });
const vaHtml = renderList(va);

// ---- census -----------------------------------------------------------------------------------------------------------------
const tpHtml = renderList(lists.TRENDING_PRICE);
console.log(`CENSUS LABEL asset_class: page "${headerText(tpHtml, 'asset_class')}" | Positioning "${POS.asset_class}"`);
console.log(`CENSUS LABEL sub_asset_class: page "${headerText(tpHtml, 'sub_asset_class')}" | Positioning "${POS.sub_asset_class}"`);
console.log(`CENSUS LABEL sector: page "${headerText(vaHtml, 'sector')}" | Positioning (none: its finer field sits unlabelled under "${POS.sub_asset_class}")`);

// ---- arm 1 ------------------------------------------------------------------------------------------------------------------
const f1 = [];
if (!POS.asset_class || !POS.sub_asset_class) f1.push(`Positioning labels not read (asset ${POS.asset_class}, sub ${POS.sub_asset_class})`);
let lists1 = 0;
for (const k of LISTS) {
  const p = lists[k];
  if (!(p.rows || []).length) continue;
  const html = renderList(p);
  lists1 += 1;
  if (headerText(html, 'asset_class') !== POS.asset_class) f1.push(`${k}: asset_class header "${headerText(html, 'asset_class')}"`);
  if (headerText(html, 'sub_asset_class') !== POS.sub_asset_class) f1.push(`${k}: sub_asset_class header "${headerText(html, 'sub_asset_class')}"`);
}
const a1 = f1.length === 0 && lists1 > 0;
const a1d = a1 ? `${lists1} served list(s): "${POS.asset_class}" and "${POS.sub_asset_class}", as Positioning labels them` : `${f1.length} failing; first: ${f1[0]}`;

// ---- arm 2 ------------------------------------------------------------------------------------------------------------------
const f2 = [];
const sh = headerText(vaHtml, 'sector') || '';
if (!(/industry group/i.test(sh) && /finer than/i.test(sh) && POS.sub_asset_class && sh.includes(POS.sub_asset_class))) f2.push(`variant: the finer field's header reads "${sh}"`);
for (const [k, html] of [...LISTS.map((k) => [k, renderList(lists[k])]), ['variant', vaHtml]]) {
  if (/\bsectors?\b/i.test(L.textOf(html || ''))) f2.push(`${k}: a visible "sector" in the list`);
}
const a2 = f2.length === 0;
const a2d = a2 ? `the finer field reads "${sh}"; no visible "sector" in any list` : `${f2.length} failing; first: ${f2[0]}`;

// ---- arm 3 ------------------------------------------------------------------------------------------------------------------
const f3 = [];
for (const k of LISTS) {
  const p = lists[k];
  if (!(p.rows || []).length) continue;
  const html = renderList(p);
  const keys = [...html.matchAll(/data-list-unserved-columns="([^"]*)"/g)].map((m) => m[1]);
  const note = (/<p[^>]*data-list-unserved-columns="[^"]*"[^>]*>([\s\S]*?)<\/p>/.exec(html) || [])[1];
  const words = note ? unesc(L.textOf(note)) : '';
  if (keys.length !== 1 || keys[0] !== 'sector,places_moved') f3.push(`${k}: note keys ${JSON.stringify(keys)}`);
  if (!(/industry group/i.test(words) && /finer than/i.test(words) && /places moved since the last run/.test(words))) f3.push(`${k}: note reads "${words}"`);
}
const a3 = f3.length === 0;
const a3d = a3 ? 'every served list names the unserved finer field by its grain and "places moved since the last run", keys unchanged' : `${f3.length} failing; first: ${f3[0]}`;

const arms = [
  ["the columns carry Positioning's label for the same key", a1, a1d],
  ['the finer field is named by its grain, never a second "sector"', a2, a2d],
  ['the unserved note uses the same labels', a3, a3d],
];
let pass = 0;
for (const [name, ok, detail] of arms) { if (ok) pass += 1; console.log(`${ok ? 'ARM PASS' : 'ARM FAIL'} ${name} :: ${detail}`); }
console.log(`CLASSIFICATION LABELS PER POSITIONING: ${pass} of ${arms.length} arms`);
process.exit(pass === arms.length ? 0 : 1);
