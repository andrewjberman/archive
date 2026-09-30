/**
 * columns.cjs -- DSGN_AMGTV1 round 7, AV-s-4: THE LEAD LISTS SHOW OPAL'S SERVED CLASSIFICATION AS COLUMNS, NAME EVERY UNSERVED
 * COLUMN ONCE, AND THE "PASS" BADGE LEAVES THE FACE (round-6 analysis rulings 5 and 6; FWD-2, FWD-11).
 *
 * Usage (repo root): node <this file>
 * Renders components/RankedList.tsx on the four SERVED lead-panel lists captured at the cut from the deployed scoped API
 * (round7/fixtures/rankings.{TRENDING,BREAKOUT}_{CHATTER,PRICE}.json), and components/ThesisCards.tsx ThesisCardDetail on the
 * served VLO /thesis. It first PRINTS THE SERVED-COLUMN CENSUS (per list: rows, and how many rows serve asset class, sub-asset
 * class, sector, and a places-moved field). At the cut: asset class and sub-asset class 30 of 32 on each price list and 2 of 2
 * on Trending x Chatter; sector 0 on every list; NO places-moved field on any row; Breakout x Chatter serves 0 rows.
 * ISSUER VARIANTS (labelled): (a) Trending x Price with ONE row's classification.sector set, to prove a served sector renders
 * and leaves the not-served note; (b) the VLO /thesis with one drafted sentence's verbatim_check set to REFUSE (the control:
 * a refusal keeps its badge).
 * Arms:
 *   1  served columns render as served: for every served non-empty list, every row whose classification serves asset_class /
 *      sub_asset_class carries data-row-asset-class / data-row-sub-asset-class equal to the served value AND shows it in its
 *      visible text; a row that serves none carries no such attribute; the list carries a column header row
 *      (data-list-column="asset_class" and "sub_asset_class")
 *   2  unserved columns are named, never computed: each non-empty served list renders ONE note whose data-list-unserved-columns
 *      names "sector" and "places_moved" (neither served), and no row carries data-row-sector / data-row-places-moved; with
 *      variant (a) the served sector renders on its row and the note no longer names "sector"
 *   3  the PASS badge is off the face: in every served VLO Thesis window no visible "PASS" token remains and every drafted
 *      sentence carrying a served verbatim_check has data-verbatim-check equal to it; with variant (b) the REFUSE sentence
 *      still shows its REFUSED badge
 * Prints the census, one line per arm and "LEAD COLUMNS AND NO PASS BADGE: <k> of 3 arms"; exit 0 only at 3 of 3.
 */
const L = require('./_load.cjs');
const clone = (x) => JSON.parse(JSON.stringify(x));
const safe = (f) => { try { return f(); } catch (e) { return 'RENDER FAILED ' + String(e.message).split('\n')[0]; } };
const LISTS = ['TRENDING_CHATTER', 'TRENDING_PRICE', 'BREAKOUT_CHATTER', 'BREAKOUT_PRICE'];
const lists = Object.fromEntries(LISTS.map((k) => [k, L.fixture(`rankings.${k}.json`)]));
const MOVED_FIELDS = ['places_moved', 'rank_change', 'rank_delta', 'prior_rank', 'previous_rank', 'moved'];

// ---- the served-column census --------------------------------------------------------------------------------------------
for (const k of LISTS) {
  const rows = lists[k].rows || [];
  const c = (f) => rows.filter((r) => r.classification && typeof r.classification[f] === 'string' && r.classification[f].trim()).length;
  const moved = rows.filter((r) => MOVED_FIELDS.some((f) => r[f] !== undefined && r[f] !== null)).length;
  console.log(`CENSUS ${k}: rows ${rows.length}; asset_class ${c('asset_class')}/${rows.length}; sub_asset_class ${c('sub_asset_class')}/${rows.length}; sector ${c('sector')}/${rows.length}; places_moved ${moved}/${rows.length}`);
}

const RL = safe(() => L.source('src/pages/SecurityAnalysis/components/RankedList.tsx'));
const renderList = (payload) => safe(() => L.render(RL.RankedList, {
  rows: payload.rows || [], starredTickers: new Set(), resolution: payload.resolution, onToggleStar: () => {}, onSelectSecurity: () => {},
  isLoading: false, readError: null, rankingStatus: payload.ranking_status, rankingReason: null, emptyReason: null,
}));
const rowsOf = (html) => [...html.matchAll(/<li[\s\S]*?<\/li>/g)].map((m) => m[0]);
const attr = (h, n) => ((new RegExp(n + '="([^"]*)"')).exec(h) || [])[1];
const unesc = (s) => (s === undefined ? undefined : s.replace(/&amp;/g, '&').replace(/&quot;/g, '"').replace(/&#x27;/g, "'"));

// ---- arm 1 ------------------------------------------------------------------------------------------------------------
const f1 = [];
let checked = 0;
for (const k of LISTS) {
  const p = lists[k];
  if (!(p.rows || []).length) continue;
  const html = renderList(p);
  if (/^RENDER FAILED/.test(html)) { f1.push(`${k}: ${html}`); continue; }
  if (!/data-list-column="asset_class"/.test(html) || !/data-list-column="sub_asset_class"/.test(html)) f1.push(`${k}: no column header row`);
  const lis = rowsOf(html);
  p.rows.forEach((r, i) => {
    const li = lis[i] || '';
    const text = L.textOf(li);
    for (const [f, a] of [['asset_class', 'data-row-asset-class'], ['sub_asset_class', 'data-row-sub-asset-class']]) {
      const v = r.classification && r.classification[f];
      const got = unesc(attr(li, a));
      checked += 1;
      if (typeof v === 'string' && v.trim()) { if (got !== v || !text.includes(v)) f1.push(`${k} #${r.rank} ${f}: attr ${got}, visible ${text.includes(v)} (served "${v}")`); }
      else if (got !== undefined) f1.push(`${k} #${r.rank} ${f}: attribute "${got}" on a row that serves none`);
    }
  });
}
const a1 = f1.length === 0 && checked > 0;
const a1d = `${checked} served-column readings, ${f1.length} failing` + (f1.length ? `; first: ${f1[0]}` : '');

// ---- arm 2 ------------------------------------------------------------------------------------------------------------
const f2 = [];
for (const k of LISTS) {
  const p = lists[k];
  if (!(p.rows || []).length) continue;
  const html = renderList(p);
  const notes = [...html.matchAll(/data-list-unserved-columns="([^"]*)"/g)].map((m) => m[1]);
  if (notes.length !== 1 || !/\bsector\b/.test(notes[0] || '') || !/\bplaces_moved\b/.test(notes[0] || '')) f2.push(`${k}: notes ${JSON.stringify(notes)}`);
  if (/data-row-sector=|data-row-places-moved=/.test(html)) f2.push(`${k}: a row carries a sector / places-moved value no row serves`);
}
// ISSUER VARIANT (a): one served sector
const va = clone(lists.TRENDING_PRICE);
va.rows[1].classification = Object.assign({}, va.rows[1].classification, { sector: 'Oil, Gas & Consumable Fuels' });
const vaHtml = renderList(va);
const vaNote = (/data-list-unserved-columns="([^"]*)"/.exec(vaHtml) || [])[1] || '';
const vaRow = rowsOf(vaHtml)[1] || '';
if (!(unesc(attr(vaRow, 'data-row-sector')) === 'Oil, Gas & Consumable Fuels' && L.textOf(vaRow).includes('Oil, Gas & Consumable Fuels') && !/\bsector\b/.test(vaNote) && /places_moved/.test(vaNote))) {
  f2.push(`variant (a): row sector ${attr(vaRow, 'data-row-sector')}, note "${vaNote}"`);
}
const a2 = f2.length === 0;
const a2d = f2.length ? `${f2.length} failing; first: ${f2[0]}` : 'every served list names sector and places moved once as not served; a served sector renders and leaves the note';

// ---- arm 3 ------------------------------------------------------------------------------------------------------------
const TC = safe(() => L.source('src/pages/SecurityAnalysis/components/ThesisCards.tsx'));
const vlo = L.fixture('thesisBundle.VLO_US_Equity.json');
const f3 = [];
let sentences = 0;
for (const id of ['investment_thesis', 'risks', 'recommendation']) {
  const html = safe(() => L.render(TC.ThesisCardDetail, { sectionId: id, bundle: vlo }));
  if (/^RENDER FAILED/.test(html)) { f3.push(`${id}: ${html}`); continue; }
  if (/\bPASS\b/.test(L.textOf(html))) f3.push(`${id}: a visible PASS`);
  for (const m of html.matchAll(/<div data-drafted-sentence="\d+"([^>]*)>/g)) {
    sentences += 1;
    if (!/data-verbatim-check="PASS"/.test(m[1])) f3.push(`${id}: a drafted sentence without data-verbatim-check="PASS" (${m[1].slice(0, 60)})`);
  }
}
// ISSUER VARIANT (b): one REFUSE sentence keeps its badge
const vb = clone(vlo);
const sec = (vb.drafted_sections || []).find((s) => (s.sentences || []).length);
if (sec) sec.sentences[0].verbatim_check = 'REFUSE';
const vbHtml = sec ? safe(() => L.render(TC.ThesisCardDetail, { sectionId: sec.section_id || sec.id || 'investment_thesis', bundle: vb })) : '';
const refusedShown = /REFUSED/.test(L.textOf(vbHtml)) && /data-verbatim-check="REFUSE"/.test(vbHtml);
const a3 = f3.length === 0 && sentences > 0 && refusedShown;
const a3d = `${sentences} drafted sentence(s) read, ${f3.length} failing${f3.length ? ` (first: ${f3[0]})` : ''}; variant (b) REFUSED badge kept ${refusedShown}`;

const arms = [
  ['served classification renders as columns, value for value', a1, a1d],
  ['unserved columns are named once, never computed', a2, a2d],
  ['the PASS badge leaves the face; a refusal keeps its badge', a3, a3d],
];
let pass = 0;
for (const [name, ok, detail] of arms) {
  if (ok) pass += 1;
  console.log(`${ok ? 'ARM PASS' : 'ARM FAIL'} ${name} :: ${detail}`);
}
console.log(`LEAD COLUMNS AND NO PASS BADGE: ${pass} of ${arms.length} arms`);
process.exit(pass === arms.length ? 0 : 1);
