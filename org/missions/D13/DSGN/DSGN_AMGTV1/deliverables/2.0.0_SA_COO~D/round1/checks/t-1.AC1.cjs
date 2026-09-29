/**
 * AV-t-1 AC1 -- THE ROW LEADS WITH THE COMPANY NAME THE ROW CARRIES, OR WITH ITS SERVED TICKER.
 *
 * Input: the served Trending x Price generation 2026-09-25 (32 rows, VLO US at rank 3), captured
 * from lib/research/api/scoped_amgt.read_rankings('TRENDING','PRICE') at the cut. Rows carry no
 * name today (the ask is AMGT_RESAPP's), so the served-name arms add the field the ask names.
 *
 * Four arms, all must hold:
 *   A  as served: every <li> carries data-row-name-state="NOT_SERVED", its data-row-lead reads its
 *      own ticker, 32 of 32, in producer order (VLO US third).
 *   B  row 3 carries `name: "Valero Energy Corp"`: that row reads data-row-name-state="SERVED",
 *      its data-row-lead is the name and its data-row-ticker is "VLO US"; the other 31 unchanged.
 *   C  row 3 carries `classification: { name: "Valero Energy Corp" }` and no `name`: same as B.
 *   D  no arm's markup prints any row's security_key (the canonical key never shows on the face).
 */
const L = require('./_load.cjs');

const served = L.fixture('rankings.TRENDING_PRICE.json');
const rows = served.rows;
const { RankedList } = L.source('src/pages/SecurityAnalysis/components/RankedList.tsx');

function renderRows(rs) {
  return L.render(RankedList, {
    rows: rs,
    starredTickers: new Set(),
    resolution: served.resolution,
    onToggleStar: () => {},
    onSelectSecurity: () => {},
    isLoading: false,
    readError: null,
    rankingStatus: 'SERVED',
  });
}

function leadTexts(html) {
  const out = [];
  let from = 0;
  for (;;) {
    const at = html.indexOf('data-row-lead', from);
    if (at < 0) break;
    const inner = L.innerOf(html.slice(html.lastIndexOf('<', at)), 'data-row-lead');
    out.push(L.textOf(inner || ''));
    from = at + 1;
  }
  return out;
}
function tickerTexts(html) {
  const out = [];
  let from = 0;
  for (;;) {
    const at = html.indexOf('data-row-ticker', from);
    if (at < 0) break;
    const inner = L.innerOf(html.slice(html.lastIndexOf('<', at)), 'data-row-ticker');
    out.push(L.textOf(inner || ''));
    from = at + 1;
  }
  return out;
}

const results = [];

// A
{
  const html = renderRows(rows);
  const st = L.attrValues(html, 'data-row-name-state').map((a) => a.value);
  const leads = leadTexts(html);
  const ok =
    st.length === rows.length &&
    st.every((v) => v === 'NOT_SERVED') &&
    leads.length === rows.length &&
    leads.every((t, i) => t === rows[i].ticker) &&
    leads[2] === 'VLO US';
  results.push(['A as-served rows lead with their ticker', ok, `states=${st.length}/${rows.length} leads=${leads.length} third=${leads[2]}`]);
}

function namedArm(label, patch) {
  const rs = rows.map((r, i) => (i === 2 ? { ...r, ...patch } : r));
  const html = renderRows(rs);
  const st = L.attrValues(html, 'data-row-name-state').map((a) => a.value);
  const leads = leadTexts(html);
  const tick = tickerTexts(html);
  const others = st.filter((v, i) => i !== 2);
  const ok =
    st.length === rows.length &&
    st[2] === 'SERVED' &&
    leads[2] === 'Valero Energy Corp' &&
    tick.includes('VLO US') &&
    others.every((v) => v === 'NOT_SERVED') &&
    leads.every((t, i) => i === 2 || t === rows[i].ticker);
  results.push([label, ok, `third_state=${st[2]} third_lead=${leads[2]} ticker_shown=${tick.includes('VLO US')}`]);
  return html;
}
const htmlB = namedArm('B row.name leads', { name: 'Valero Energy Corp' });
const htmlC = namedArm('C row.classification.name leads', { classification: { name: 'Valero Energy Corp' } });

// D
{
  const htmlA = renderRows(rows);
  const keys = rows.map((r) => r.security_key).filter(Boolean);
  const leaked = keys.filter((k) => [htmlA, htmlB, htmlC].some((h) => L.textOf(h).includes(k)));
  results.push(['D no security_key on the face', leaked.length === 0, `leaked=${leaked.length} of ${keys.length}`]);
}

let pass = 0;
for (const [name, ok, detail] of results) {
  console.log(`ARM ${ok ? 'PASS' : 'FAIL'} ${name} :: ${detail}`);
  if (ok) pass += 1;
}
console.log(`ROW NAME RENDER: ${pass} of ${results.length} arms`);
process.exit(pass === results.length ? 0 : 1);
