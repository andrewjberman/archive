/**
 * identity.cjs -- DSGN_AMGTV1 round 27, AV-ze-1 (issuer 2.0.0_SA_COO~D): EVERY BAR AND BUBBLE CARRIES ITS SERVED IDENTITY ONE HOVER AWAY.
 *
 * Usage (repo root): node <this file>        (portal/ under the cwd is the checkout under test)
 * CTO COMPLETION_GRADES.round26 @0c4c6d6368 FWD-2 NOT_REALIZED ("A PAGE cell (DSGN)"), on CVO~Z ADJUDICATION_v26 @07446385f1:
 * PriceBars.tsx and ChatterBubbles.tsx render only the name and the value -- no ticker, asset class, sub-asset class, sector or
 * places moved, and no hover surface -- though the served price rows carry them. FWD-2 v0.6: "The same identity -- name, ticker,
 * asset class, sub-asset class, sector, the period figure and places moved -- is read on each FWD-21 bubble and each FWD-22 bar
 * (its label, or one hover away)."
 * THE CONTRACT (one hover away = a native hover title: a `title` attribute on the bar's element, or an SVG `<title>` child of the
 * bubble's element):
 *   BAR (`[data-price-bar]`): the hover text carries the served name (or ticker), the ticker, asset class, sub-asset class, sector
 *     (a null sector is said in words, e.g. "sector not served"), the period figure (the served return_30d_pct, one decimal, sign),
 *     and places moved (the served number in words, e.g. "up 2 places" / "down 1 place" / "no change", or the served
 *     places_moved_reason in plain words when the number is null).
 *   BUBBLE (`[data-bubble]`): the hover text carries the served display name, the collected count for the month shown, and each
 *     identity field the chatter row SERVES (ticker, classification, places_moved / places_moved_reason, the same shape as a ranking
 *     row); a field the row does not serve is said in words ("classification not served"), never invented or joined from elsewhere.
 *   Neither hover text carries a code-shaped token (snake_case, `_Equity`, `.json`, UPPER_SNAKE).
 * Inputs: round15/fixtures/r15a.rankings.TRENDING_PRICE.return30d.json (32 served price rows, with places_moved planted on three);
 *   round16/fixtures/r16g.collected.chatter.json (95 served chatter rows; three planted with ticker/classification/places_moved).
 * Arms:
 *   1  BARS: the three largest-move bars carry every served identity field in their hover text.
 *   2  BUBBLES: the three planted bubbles carry every served field; a bubble on a bare row (today's shape) says classification is
 *      not served and invents no value.
 *   3  PLANTED: the comparator rejects a hover text missing the ticker and one carrying a code; it accepts a full one.
 * Prints one line per arm and "EVERY BAR AND BUBBLE CARRIES ITS SERVED IDENTITY: <k> of 3 arms"; exit 0 only at 3 of 3.
 */
const fs = require('fs');
const path = require('path');

const SA = 'src/pages/SecurityAnalysis/';
const ROUND = path.join(__dirname, '..', '..');
const L = require(path.join(ROUND, 'round15', 'checks', '_load.cjs'));
const load = (p) => { const d = JSON.parse(fs.readFileSync(p, 'utf8')); return d && d.payload ? d.payload : d; };
const PRICE = load(path.join(ROUND, 'round15', 'fixtures', 'r15a.rankings.TRENDING_PRICE.return30d.json'));
const CHAT = load(path.join(ROUND, 'round16', 'fixtures', 'r16g.collected.chatter.json'));
const CODE = /\b[a-z]+_[a-z0-9_]+\b|_Equity\b|\.json\b|\b[A-Z][A-Z0-9]*_[A-Z0-9_]+\b/;
const decode = (s) => String(s).replace(/&amp;/g, '&').replace(/&quot;/g, '"').replace(/&#x27;/g, "'").replace(/&lt;/g, '<').replace(/&gt;/g, '>');
const lc = (s) => String(s).toLowerCase();

function hoverOf(html, attr, key) {
  const at = html.indexOf(`${attr}="${key}"`);
  if (at < 0) return null;
  const open = html.lastIndexOf('<', at);
  const tag = /^<([a-zA-Z0-9]+)/.exec(html.slice(open))[1];
  const head = html.slice(open, html.indexOf('>', at) + 1);
  const t = /\btitle="([^"]*)"/.exec(head);
  if (t) return decode(t[1]);
  const end = html.indexOf(`</${tag}>`, at);
  const inner = html.slice(at, end < 0 ? at + 4000 : end);
  const st = /<title>([\s\S]*?)<\/title>/.exec(inner);
  return st ? decode(st[1]).replace(/\s+/g, ' ').trim() : null;
}
function movedWords(n) { return n === 0 ? /no change|unchanged|0 places/i : new RegExp(`\\b${Math.abs(n)}\\b`); }
function faults(hover, want) {
  const f = [];
  if (!hover) return ['NO HOVER: no title on the mark'];
  for (const [label, v] of Object.entries(want.fields)) {
    if (v === null || v === undefined || v === '') {
      if (!new RegExp(`${label.replace(/[-_]/g, '.')}.{0,40}not served|not served.{0,40}${label.replace(/[-_]/g, '.')}`, 'i').test(hover) &&
          !/not served/i.test(hover)) f.push(`MISSING-WORDS: ${label} is null but the hover does not say it is not served`);
    } else if (!lc(hover).includes(lc(v))) f.push(`MISSING: ${label} "${v}"`);
  }
  if (want.moved !== undefined) {
    if (want.moved === null) { if (want.reason && !lc(hover).includes(lc(want.reason).slice(0, 20))) f.push('MISSING: places_moved_reason'); }
    else if (!movedWords(want.moved).test(hover)) f.push(`MISSING: places moved ${want.moved}`);
  }
  if (CODE.test(hover)) f.push(`CODE: "${hover.match(CODE)[0]}"`);
  return f;
}

const arms = [];
// Arm 1 -- bars.
{
  const f = [];
  const rows = JSON.parse(JSON.stringify(PRICE.rows));
  const sorted = [...rows].filter((r) => typeof r.return_30d_pct === 'number').sort((a, b) => Math.abs(b.return_30d_pct) - Math.abs(a.return_30d_pct));
  const plant = [[sorted[0], 2, null], [sorted[1], -1, null], [sorted[2], null, 'no previous complete generation to compare against']];
  for (const [r, n, why] of plant) { r.places_moved = n; r.places_moved_reason = why; }
  try {
    const m = L.source(SA + 'components/PriceBars.tsx');
    const h = L.render(m.PriceBars, { rows, onSelectSecurity: () => {} });
    for (const [r, n, why] of plant) {
      const key = r.security_key || r.ticker;
      const c = r.classification || {};
      const want = { fields: { name: r.name || r.ticker, ticker: r.ticker, 'asset class': c.asset_class, 'sub-asset class': c.sub_asset_class, sector: c.sector,
        'period figure': Math.abs(r.return_30d_pct).toFixed(1) }, moved: n, reason: why };
      f.push(...faults(hoverOf(h, 'data-price-bar', key), want).map((x) => `${r.ticker}: ${x}`));
    }
  } catch (e) { f.push('RENDER: ' + String(e.message).split('\n')[0]); }
  arms.push(['BARS: the three largest-move bars carry every served identity field one hover away', f.length === 0, f.length === 0 ? '3 of 3 bars' : f.slice(0, 5).join(' | ')]);
}
// Arm 2 -- bubbles.
{
  const f = [];
  const data = JSON.parse(JSON.stringify(CHAT));
  const month = (data.months || []).slice(-1)[0] || Object.keys(data.rows.find((r) => Object.keys(r.by_month).length).by_month)[0];
  // Rows whose served display_name is itself a raw key (captured before RESAPP B1 named them) are not planted on: the page prints
  // the served name as served, so a code there is the producer's, not this cell's.
  const lit = data.rows.filter((r) => r.by_month[month] && r.by_month[month].collected > 0 && !CODE.test(r.display_name));
  const planted = lit.slice(0, 3).map((r, i) => {
    r.ticker = r.security_key.replace(/_Equity$/, '').replace(/_/g, ' ');
    r.classification = { asset_class: 'equity', sub_asset_class: ['Energy', 'Industrials', 'Health Care'][i], sector: ['Oil & Gas Refining', null, 'Biotechnology'][i] };
    r.places_moved = [3, null, 0][i];
    r.places_moved_reason = [null, 'not ranked in the previous generation', null][i];
    return r;
  });
  const bare = lit[3];
  try {
    const m = L.source(SA + 'components/ChatterBubbles.tsx');
    const h = L.render(m.ChatterBubbles, { data, month, onSelectSecurity: () => {} });
    for (const r of planted) {
      const want = { fields: { name: r.display_name, ticker: r.ticker, 'asset class': r.classification.asset_class, 'sub-asset class': r.classification.sub_asset_class,
        sector: r.classification.sector, collected: String(r.by_month[month].collected) }, moved: r.places_moved, reason: r.places_moved_reason };
      f.push(...faults(hoverOf(h, 'data-bubble', r.security_key), want).map((x) => `${r.display_name}: ${x}`));
    }
    if (bare) {
      const hv = hoverOf(h, 'data-bubble', bare.security_key);
      if (!hv) f.push(`${bare.display_name}: NO HOVER on a bare row`);
      else {
        if (!lc(hv).includes(lc(bare.display_name))) f.push(`${bare.display_name}: bare hover lacks the name`);
        if (!/not served/i.test(hv)) f.push(`${bare.display_name}: bare hover does not say what is not served`);
        if (CODE.test(hv)) f.push(`${bare.display_name}: CODE in bare hover`);
      }
    } else f.push('INPUT: fewer than 4 lit bubbles in the month');
  } catch (e) { f.push('RENDER: ' + String(e.message).split('\n')[0]); }
  arms.push(['BUBBLES: served identity one hover away; a bare row says what is not served', f.length === 0, f.length === 0 ? '3 of 3 planted + 1 bare' : f.slice(0, 5).join(' | ')]);
}
// Arm 3 -- planted comparator.
{
  const f = [];
  const want = { fields: { name: 'Valero Energy Corp', ticker: 'VLO US', 'asset class': 'equity', 'sub-asset class': 'Energy', sector: 'Oil & Gas Refining', 'period figure': '0.8' }, moved: 2 };
  const good = 'Valero Energy Corp (VLO US) -- equity, Energy, Oil & Gas Refining; +0.8% over 30 days; up 2 places since the last run';
  if (faults(good, want).length) f.push(`a full hover is rejected: ${faults(good, want)[0]}`);
  const M = [['no ticker', good.replace(' (VLO US)', '')], ['a code', good + ' [VLO_US_Equity]']];
  let caught = 0;
  for (const [n, h] of M) { if (faults(h, want).length) caught += 1; else f.push(`mutant "${n}" accepted`); }
  arms.push(['PLANTED: a hover missing the ticker and one carrying a code are rejected; a full one passes', f.length === 0, f.length === 0 ? `${caught} of 2 rejected` : f.join(' | ')]);
}

let pass = 0;
for (const [n, ok, d] of arms) { if (ok) pass += 1; console.log(`${ok ? 'ARM PASS' : 'ARM FAIL'} ${n} :: ${d}`); }
console.log(`EVERY BAR AND BUBBLE CARRIES ITS SERVED IDENTITY: ${pass} of 3 arms`);
process.exit(pass === 3 ? 0 : 1);
