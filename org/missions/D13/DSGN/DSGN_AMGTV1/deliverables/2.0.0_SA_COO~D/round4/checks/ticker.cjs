/**
 * ticker.cjs -- DSGN_AMGTV1 round 4, AV-w-2: THE LEAD LIST PRINTS EACH TICKER AS BLOOMBERG WRITES IT
 * (round-3 analysis s.2 decision 2: "BP/ LN" and "WALMEX* MM" are the tickers themselves; only a KEY's own encoding --
 * "_" and the "_Equity" suffix -- is removed, and a served ticker is not a key).
 *
 * Usage (repo root): node <this file>
 * Renders the lead list (RankedList) on the served Trending x Price payload (round4/fixtures/rankings.TRENDING_PRICE.json,
 * 32 rows, three of them carrying a metacharacter) and reads its VISIBLE text. Arms:
 *   1-3  "BP/ LN", "WALMEX* MM" and "NG/ LN" each appear whole on the face
 *   4    none of their stripped forms ("BP LN", "WALMEX MM", "NG LN") appears -- the ticker is not rewritten
 *   5    no key encoding on the face: no "_Equity", and no ticker printed with "_" in place of a space
 * Prints one line per arm and "TICKERS AS WRITTEN: <k> of 5 arms"; exit 0 only at 5 of 5 over a non-empty render.
 */
const L = require('./_load.cjs');
const payload = L.fixture('rankings.TRENDING_PRICE.json');
let html = '';
try {
  const { RankedList } = L.source('src/pages/SecurityAnalysis/components/RankedList.tsx');
  html = L.render(RankedList, {
    rows: payload.rows,
    starredTickers: new Set(),
    resolution: payload.resolution,
    onToggleStar: () => {},
    onSelectSecurity: () => {},
    isLoading: false,
    readError: null,
    status: payload.status,
  });
} catch (e) {
  console.log('render failed: ' + String(e.message).split('\n')[0]);
}
const text = L.textOf(html);
const whole = ['BP/ LN', 'WALMEX* MM', 'NG/ LN'];
const stripped = ['BP LN', 'WALMEX MM', 'NG LN'];
const arms = [];
for (const t of whole) arms.push([`"${t}" on the face`, text.includes(t), `${text.split(t).length - 1} occurrence(s)`]);
const bad = stripped.filter((s) => new RegExp('(^|[^/*])\\b' + s.replace(/ /g, ' ') + '\\b').test(text.replace(/BP\/ LN|WALMEX\* MM|NG\/ LN/g, '')));
arms.push(['no stripped form', bad.length === 0, bad.length ? 'found ' + JSON.stringify(bad) : 'none']);
const enc = (text.match(/_Equity|\b[A-Z0-9*/]+_[A-Z]{2}\b/g) || []);
arms.push(['no key encoding', enc.length === 0, enc.length ? 'found ' + JSON.stringify(enc.slice(0, 3)) : 'none']);
let pass = 0;
for (const [name, ok, detail] of arms) {
  if (ok) pass += 1;
  console.log(`${ok ? 'ARM PASS' : 'ARM FAIL'} ${name} :: ${detail}`);
}
console.log(`TICKERS AS WRITTEN: ${pass} of ${arms.length} arms${text ? '' : ' -- EMPTY RENDER'}`);
process.exit(pass === arms.length && text ? 0 : 1);
