/**
 * gens.cjs -- DSGN_AMGTV1 round 5, AV-v-3: THE LEAD CHART'S GENERATIONS LINE IN WORDS, AND ONE DARK BAND ON THE LOAD VIEW
 * (round-4 analysis s.4 item 3; FWD-11).
 *
 * Usage (repo root): node <this file>
 * Renders components/RankedChart.tsx on the SERVED 12-name payload (round5/fixtures/rankSeries.TRENDING_PRICE.12.json:
 * 30 dates, 25 ABSENT and 5 SERVED generation pointers) with recharts stubbed, and components/LeadPanel.tsx on the served
 * Trending x Price ranking (round5/fixtures/rankings.TRENDING_PRICE.json) with the estate chrome stubbed (a stub prints
 * `data-stub="<export name>"`, so the panel's own header / content / footer parts are countable).
 * Arms:
 *   1  the generations line reads in words: the element carrying `data-generation-caption` in the drawn chart is present,
 *      still states the window's date count (the digits "30" appear), and its VISIBLE text carries no pointer-status word
 *      (ABSENT, SERVED, EMPTY, PENDING) and none of the fixture's served generation ids (an id may ride an attribute)
 *   2  the same line in the COMPLETE_EMPTY branch (the fixture with every series removed and read_completeness complete):
 *      present, no pointer-status word and no generation id in visible text
 *   3  one dark band on the lead panel: LeadPanel renders NO `PanelFooter` (the footer is the second #0A1733 band beside
 *      the panel header -- measured on the round-4 walk, shot 004: header rows and footer rows both rgb(10,23,51), the body
 *      rgb(25,38,67)), AND the source caption is still rendered (`data-source-caption="generation"` present, with its
 *      collapsed `data-source-caption="detail"` block)
 * Prints one line per arm and "GENERATIONS LINE AND ONE BAND: <k> of 3 arms"; exit 0 only at 3 of 3.
 */
const L = require('./_load.cjs');
const React = L.React;

const cache = {};
L.stubSource('recharts', new Proxy({}, {
  get(_t, key) {
    if (key === '__esModule') return true;
    if (typeof key !== 'string') return undefined;
    if (!cache[key]) cache[key] = (p) => React.createElement('div', { 'data-rc': key }, (p || {}).children);
    return cache[key];
  },
}));
L.stubSource('src/hooks/useAuth', { useAuth: () => ({ claims: { firmId: 'opal' } }) });
L.stubSource('src/hooks/useAuth.ts', { useAuth: () => ({ claims: { firmId: 'opal' } }) });
L.stubSource('src/hooks/useAuth.tsx', { useAuth: () => ({ claims: { firmId: 'opal' } }) });

const series = L.fixture('rankSeries.TRENDING_PRICE.12.json');
const rankings = L.fixture('rankings.TRENDING_PRICE.json');
const ids = new Set(
  (series.generations || []).map((g) => g.generation_id).concat([rankings.generation_id]).filter(Boolean)
);
const STATUS = /\b(ABSENT|SERVED|EMPTY|PENDING)\b/g;

function line(data) {
  let html = '';
  try {
    html = L.render(L.source('src/pages/SecurityAnalysis/components/RankedChart.tsx').RankedChart, { data, isLoading: false });
  } catch (e) {
    console.log('chart render failed: ' + String(e.message).split('\n')[0]);
  }
  const inner = L.innerOf(html, 'data-generation-caption');
  const text = inner === null ? null : L.textOf(inner);
  return { text, status: text ? text.match(STATUS) || [] : [], idHits: text ? [...ids].filter((id) => text.includes(id)) : [] };
}
const drawn = line(series);
const empty = line({
  ...series,
  series: [],
  read_completeness: { ...(series.read_completeness || {}), complete: true, unresolved_keys: 0 },
});

let lead = '';
try {
  L.hookState.impl = {
    useLeadPanelRankings: () => rankings,
    useRankTimeSeries: () => series,
    useStarredList: () => [],
    useSetStarred: () => undefined,
  };
  lead = L.render(L.source('src/pages/SecurityAnalysis/components/LeadPanel.tsx').LeadPanel, {
    movement: 'trending', setMovement: () => {}, subject: 'price', setSubject: () => {}, starredOnly: false,
    setStarredOnly: () => {}, view: 'list', setView: () => {}, selectedSecurityKey: null, onSelectSecurity: () => {},
    onClearSecuritySelection: () => {}, searchInput: '', setSearchInput: () => {},
  });
} catch (e) {
  console.log('lead panel render failed: ' + String(e.message).split('\n')[0]);
}
const footers = (lead.match(/data-stub="PanelFooter"/g) || []).length;
const caption = /data-source-caption="generation"/.test(lead);
const detail = /data-source-caption="detail"/.test(lead);

const show = (xs) => `${xs.length}${xs.length ? ' ' + JSON.stringify(xs.slice(0, 4)) : ''}`;
const arms = [
  ['the drawn chart\'s generations line reads in words', drawn.text !== null && /\b30\b/.test(drawn.text) && drawn.status.length === 0 && drawn.idHits.length === 0,
    `present ${drawn.text !== null}; states 30 dates ${drawn.text ? /\b30\b/.test(drawn.text) : false}; status words ${show(drawn.status)}; generation ids ${show(drawn.idHits)} :: "${(drawn.text || '').slice(0, 140)}"`],
  ['the empty chart\'s generations line reads in words', empty.text !== null && empty.status.length === 0 && empty.idHits.length === 0,
    `present ${empty.text !== null}; status words ${show(empty.status)}; generation ids ${show(empty.idHits)} :: "${(empty.text || '').slice(0, 140)}"`],
  ['one dark band: no PanelFooter, the source caption kept', lead.length > 0 && footers === 0 && caption && detail,
    `PanelFooter x${footers}; source caption ${caption}; collapsed detail ${detail}`],
];
let pass = 0;
for (const [name, ok, detail2] of arms) {
  if (ok) pass += 1;
  console.log(`${ok ? 'ARM PASS' : 'ARM FAIL'} ${name} :: ${detail2}`);
}
console.log(`GENERATIONS LINE AND ONE BAND: ${pass} of ${arms.length} arms`);
process.exit(pass === arms.length ? 0 : 1);
