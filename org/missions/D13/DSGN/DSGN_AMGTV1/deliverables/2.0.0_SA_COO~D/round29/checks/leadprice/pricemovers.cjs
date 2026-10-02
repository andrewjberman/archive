/**
 * pricemovers.cjs -- DSGN_AMGTV1 round 29, AV-zg-3 LEAD PANEL + PRICE (issuer 2.0.0_SA_COO~D): THE PRICE FACE SHOWS THE TOP MOVERS
 * EACH SIDE, OPENS THE FULL LIST ON DEMAND AND NAMES ITS WINDOW.
 *
 * Usage (from the directory whose portal/ is the checkout under test, e.g. C:/tmp/wk-dsgn-amgtv1-70): node <this file>
 * Grades: PRD v0.10 FWD-22 v0.9 (DONE WHEN, :317-329): "at rest it shows the 10 largest gainers and the 10 largest losers, the full
 *   list opens on demand in the same panel, the face states its window in words, and no name is clipped without a hover revealing
 *   it"; "a DOM census of the price view reads 0 line charts and 0 view toggles". SAUX-20 (acceptance: "At rest the Price face shows
 *   the top movers each side (gainers and losers) with the full list on demand; no name is clipped without a title or hover
 *   revealing it"). SAUX-21 / FWD-26's price caption (acceptance: "The Price face states its window in words ('change over the last
 *   N days to <date>')"), cut now from the served row's `window_days` and the served `as_of_date`; the page never computes a window
 *   (decomposition v29: "FWD-26's price caption is cut now, in AV-zg-3 from the served window_days").
 * THE CONTRACT (the worker face quotes it):
 *   - The Price face is the REAL LeadPanel (components/LeadPanel.tsx, export LeadPanel) on subject PRICE. Every bar is an element
 *     carrying data-price-bar="<security_key>" (the served ticker when the key is null) and its own `title` holding the served name
 *     and the served ticker (the round-27 hover; a row with no served name: the ticker).
 *   - AT REST the face shows exactly the 10 largest gainers (served return_30d_pct > 0, largest first) and the 10 largest losers
 *     (served return_30d_pct < 0, most negative first); a side with fewer than 10 served shows all it has. Within each side the bars
 *     run longest first. A bar not shown at rest is not rendered, or sits inside a closed native <details>; a CSS-hidden bar counts
 *     as shown.
 *   - ONE control carries data-price-expand: a <button type="button"> with aria-expanded="false" at rest and "true" when open, and
 *     visible words; or a <summary> of a native <details>. Clicking it shows every served row's bar in the same panel (each side
 *     longest first, every bar titled); clicking it again returns to the rest set.
 *   - ONE element carries data-price-window; its text reads "change over the last <window_days> days to <as_of_date in words>"
 *     (any case; a date like "October 1st, 2026", "October 1, 2026" or "1 October 2026"), N read from the served rows' window_days and
 *     the date from the served as_of_date. With window_days not served the face prints no day count anywhere. No text or title on the
 *     face names a day count other than the served window_days (the hover's "over 30 days" included).
 *   - No line chart, no rank-chart marker and no List/Chart view toggle (the round-15 census).
 * Inputs: round29/fixtures/leadprice/rankings.trending.price.live.json (the served route, captured read-only 2026-10-02 by
 *   capture_price.py: 94 rows, 24 gainers / 70 losers, window_days 30, as_of_date 2026-10-01); round15/fixtures/
 *   r15a.rankings.TRENDING_PRICE.return30d.json (32 rows, 9 gainers / 23 losers -- the short-side case). The portal's
 *   __harness__/tests/uiContractFixtures.json carries the same 32-row round-7 set at the base, not 94 rows.
 * Render: ./_render.cjs (round15/_load.cjs over the real sources; the click replay re-renders with the state the control's own
 *   onClick writes).
 * Arms:
 *   1  AT REST: on both fixtures the face shows exactly the top 10 each side, longest first per side, every bar titled; 0 line
 *      charts, 0 view toggles.
 *   2  ON DEMAND: one data-price-expand control; a click shows all 94 bars (titled, longest first per side); a second click returns
 *      to the 20; the button's aria-expanded reads false / true.
 *   3  WINDOW IN WORDS: the live payload reads "change over the last 30 days to October 1st, 2026"; a planted payload (window_days
 *      90, as_of_date 2026-09-29 on the payload and every row, px dates untouched) reads 90 and September 29th with no "30 days" left
 *      anywhere on the face; a planted payload with no window_days prints no day count.
 *   4  PLANTED: the predicates accept a reference markup (and the same rest set with the rest of the list in a closed <details>) and
 *      reject five mutants by class: all 94 at rest (COUNT), the top 20 by absolute move (SET), a swapped pair (ORDER), a bar with
 *      no title (TITLE); a caption with no date, a caption with 30 where 90 is served, and a hover saying "30 days" (WINDOW).
 * Blind spots: a static render does not lay out, so bar length, colour and whether a label is visually clipped are not measured (the
 *   title is required on every bar instead); state held outside useState/useReducer is not replayed; a CSS-hidden bar counts as
 *   shown (so it fails the rest arm loudly rather than passing).
 * Prints one line per arm and "THE PRICE FACE SHOWS THE TOP MOVERS, OPENS ON DEMAND AND NAMES ITS WINDOW: <k> of 4 arms"; exit 0
 * only at 4 of 4. Writes no file. No network, no AWS.
 */
const R = require('./_render.cjs');

const T0 = Date.now();
const LIVE = R.loadFixture('live');
const R15A = R.loadFixture('r15a');
const MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];

const esc = (s) => String(s).replace(/&/g, '&amp;').replace(/"/g, '&quot;').replace(/'/g, '&#x27;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
const unesc = (s) => String(s).replace(/&quot;/g, '"').replace(/&#x27;/g, "'").replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&amp;/g, '&');
const textOf = (html) => unesc(String(html).replace(/<[^>]*>/g, ' ')).replace(/\s+/g, ' ').trim();
const keyOf = (r) => (r.security_key === null || r.security_key === undefined ? r.ticker : r.security_key);
const ret = (r) => (typeof r.return_30d_pct === 'number' && Number.isFinite(r.return_30d_pct) ? r.return_30d_pct : null);
const nameOf = (r) => (typeof r.name === 'string' && r.name.trim() ? r.name.trim() : null);
const count = (html, re) => (html.match(re) || []).length;

// ---------------- the predicates (pure over html) ----------------
function expectedRest(rows) {
  const pos = rows.filter((r) => ret(r) !== null && ret(r) > 0).sort((a, b) => ret(b) - ret(a)).slice(0, 10);
  const neg = rows.filter((r) => ret(r) !== null && ret(r) < 0).sort((a, b) => ret(a) - ret(b)).slice(0, 10);
  return [...pos, ...neg];
}
const expectedAll = (rows) => rows.filter((r) => ret(r) !== null);

/** [start, end) ranges of every CLOSED <details> element (no `open` attribute). */
function closedDetailsRanges(html) {
  const out = [];
  const re = /<details\b([^>]*)>/g;
  let m;
  while ((m = re.exec(html)) !== null) {
    if (/\sopen(=|\s|$)/.test(' ' + m[1])) continue;
    let depth = 1;
    const r2 = /<(\/?)details\b[^>]*>/g;
    r2.lastIndex = m.index + m[0].length;
    let n;
    let end = html.length;
    while ((n = r2.exec(html)) !== null) {
      depth += n[1] === '/' ? -1 : 1;
      if (depth === 0) { end = n.index; break; }
    }
    out.push([m.index, end]);
  }
  return out;
}

/** Every bar shown: {key, title} in DOM order, bars inside a closed <details> left out. */
function shownBars(html) {
  const hidden = closedDetailsRanges(html);
  const out = [];
  const re = /data-price-bar="([^"]*)"/g;
  let m;
  while ((m = re.exec(html)) !== null) {
    if (hidden.some(([a, b]) => m.index > a && m.index < b)) continue;
    const open = html.lastIndexOf('<', m.index);
    const head = html.slice(open, html.indexOf('>', m.index) + 1);
    const t = /\stitle="([^"]*)"/.exec(head);
    out.push({ key: unesc(m[1]), title: t ? unesc(t[1]) : null });
  }
  return out;
}

function barFaults(html, rows, want) {
  const f = [];
  const byKey = new Map(rows.map((r) => [keyOf(r), r]));
  const bars = shownBars(html);
  const wantKeys = want.map(keyOf);
  if (bars.length !== want.length) f.push(`COUNT: ${bars.length} bars shown, want ${want.length}`);
  const keys = bars.map((b) => b.key);
  const dup = keys.filter((k, i) => keys.indexOf(k) !== i);
  if (dup.length) f.push(`SET: duplicate bars ${dup.slice(0, 3).join(', ')}`);
  const extra = keys.filter((k) => !wantKeys.includes(k));
  if (extra.length) f.push(`SET: ${extra.length} bar(s) shown that are not in the set (first ${extra.slice(0, 3).join(', ')})`);
  const missing = wantKeys.filter((k) => !keys.includes(k));
  if (missing.length) f.push(`SET: ${missing.length} bar(s) of the set not shown (first ${missing.slice(0, 3).join(', ')})`);
  for (const [side, test, cmp] of [['gainers', (v) => v > 0, (a, b) => b > a], ['losers', (v) => v < 0, (a, b) => b < a]]) {
    const seq = keys.filter((k, i) => keys.indexOf(k) === i && byKey.has(k) && ret(byKey.get(k)) !== null && test(ret(byKey.get(k))));
    for (let i = 1; i < seq.length; i += 1) {
      const a = ret(byKey.get(seq[i - 1]));
      const b = ret(byKey.get(seq[i]));
      if (cmp(a, b)) { f.push(`ORDER: ${side}: ${seq[i]} (${b.toFixed(1)}) sits below ${seq[i - 1]} (${a.toFixed(1)})`); break; }
    }
  }
  let tf = 0;
  for (const b of bars) {
    const r = byKey.get(b.key);
    if (!r) continue;
    const lc = (s) => String(s).toLowerCase();
    const why = !b.title ? 'no title' : !lc(b.title).includes(lc(r.ticker.trim())) ? 'title lacks the ticker'
      : nameOf(r) && !lc(b.title).includes(lc(nameOf(r))) ? 'title lacks the full served name' : null;
    if (why && tf++ < 2) f.push(`TITLE: ${b.key}: ${why}`);
  }
  if (tf > 2) f.push(`TITLE: ${tf} bars in all`);
  return f;
}

function oneFormFaults(html) {
  const f = [];
  const lines = count(html, /data-stub="(?:LineChart|Line)"/g) + count(html, /data-(?:rank-legend|series-ticker)\b/g);
  if (lines) f.push(`LINE: ${lines} line-chart element(s)`);
  const toggles = count(html, /aria-label="(?:List view|Chart view|View)"/g);
  if (toggles) f.push(`TOGGLE: ${toggles} List/Chart view toggle element(s)`);
  return f;
}

function dateSrc(iso) {
  const [y, mo, d] = iso.split('-').map(Number);
  const M = MONTHS[mo - 1];
  const S = M.slice(0, 3);
  return `(?:(?:${M}|${S}\\.?)\\s+${d}(?:st|nd|rd|th)?,?\\s+${y}|${d}(?:st|nd|rd|th)?\\s+(?:${M}|${S}\\.?),?\\s+${y})`;
}
const dateWordsRe = (iso) => new RegExp(dateSrc(iso), 'i');
/** Every day count named on the face: visible text and every title attribute. */
function dayCounts(html) {
  const titles = [...html.matchAll(/\stitle="([^"]*)"/g)].map((m) => unesc(m[1])).join(' | ');
  const all = textOf(html) + ' | ' + titles;
  return [...all.matchAll(/\b(\d+)[- ]days?\b/gi)].map((m) => Number(m[1]));
}

function windowFaults(html, want) {
  const f = [];
  const n = count(html, /data-price-window(?:=|\s|>)/g);
  if (n !== 1) f.push(`WINDOW: ${n} element(s) carry data-price-window, want 1`);
  const at = html.indexOf('data-price-window');
  let text = '';
  if (at >= 0) {
    const open = html.lastIndexOf('<', at);
    const tag = /^<([a-zA-Z0-9]+)/.exec(html.slice(open))[1];
    const start = html.indexOf('>', at) + 1;
    const end = html.indexOf(`</${tag}>`, start);
    text = textOf(html.slice(start, end < 0 ? start + 2000 : end));
  }
  if (n >= 1) {
    if (!dateWordsRe(want.asOf).test(text)) f.push(`WINDOW: the caption does not name ${want.asOf} in words ("${text.slice(0, 120)}")`);
    if (want.days !== null) {
      const re = new RegExp(`change over the last ${want.days} days to ${dateSrc(want.asOf)}`, 'i');
      if (!re.test(text)) f.push(`WINDOW: the caption does not read "change over the last ${want.days} days to <${want.asOf} in words>" ("${text.slice(0, 120)}")`);
    } else if (/\b\d+[- ]days?\b/i.test(text)) f.push(`WINDOW: window_days is not served but the caption names one ("${text.slice(0, 120)}")`);
  }
  const counts = dayCounts(html);
  const wrong = counts.filter((c) => c !== want.days);
  if (wrong.length) f.push(`WINDOW: the face names ${wrong.length} day count(s) other than the served window_days ${want.days} (first: ${wrong[0]} days)`);
  return f;
}

const plant = (payload, mut) => {
  const p = JSON.parse(JSON.stringify(payload));
  mut(p);
  return p;
};
const render = (p) => () => R.renderLead('PRICE', p, undefined);

const arms = [];
// ---------------- arm 1: at rest ----------------
{
  const f = [];
  const tally = [];
  for (const [label, p] of [['live', LIVE], ['r15a', R15A]]) {
    try {
      const html = R.renderState(render(p)).html;
      const want = expectedRest(p.rows);
      const fx = [...barFaults(html, p.rows, want), ...oneFormFaults(html)];
      const g = want.filter((r) => ret(r) > 0).length;
      tally.push(`${label} ${shownBars(html).length} shown (want ${g} + ${want.length - g})`);
      f.push(...fx.map((x) => `${label}: ${x}`));
    } catch (e) { f.push(`${label}: RENDER: ${String(e.message).split('\n')[0]}`); }
  }
  arms.push(['AT REST: the 10 largest gainers and 10 largest losers, longest first per side, every bar titled; 0 line charts, 0 view toggles',
    f.length === 0, f.length === 0 ? tally.join('; ') : `${tally.join('; ')} || ${f.slice(0, 4).join(' | ')}`]);
}
// ---------------- arm 2: on demand ----------------
{
  const f = [];
  let detail = '';
  try {
    const run = R.clickThrough(render(LIVE), 2);
    const [rest, open, back] = run.states;
    const nCtl = count(rest.html, /data-price-expand(?:=|\s|>)/g);
    if (nCtl !== 1) f.push(`EXPAND: ${nCtl} element(s) carry data-price-expand at rest, want 1`);
    if (run.stop) f.push(`EXPAND: ${run.stop}`);
    const el = rest.controls[0];
    if (el && el.type !== 'summary' && el.type !== 'details') {
      if (el.type !== 'button') f.push(`EXPAND: the control is <${el.type}>, want <button> (or a <summary>)`);
      if (String(el.props['aria-expanded']) !== 'false') f.push(`EXPAND: aria-expanded at rest is ${el.props['aria-expanded']}, want false`);
      if (open && open.controls[0] && String(open.controls[0].props['aria-expanded']) !== 'true') f.push(`EXPAND: aria-expanded when open is ${open.controls[0].props['aria-expanded']}, want true`);
    }
    if (el) {
      const at = rest.html.indexOf('data-price-expand');
      const tag = /^<([a-zA-Z0-9]+)/.exec(rest.html.slice(rest.html.lastIndexOf('<', at)))[1];
      const inner = rest.html.slice(rest.html.indexOf('>', at) + 1, rest.html.indexOf(`</${tag}>`, at));
      if (!/[A-Za-z]{2,}/.test(textOf(inner))) f.push('EXPAND: the control carries no visible words');
    }
    if (open) {
      f.push(...barFaults(open.html, LIVE.rows, expectedAll(LIVE.rows)).map((x) => `open: ${x}`), ...oneFormFaults(open.html).map((x) => `open: ${x}`));
    }
    if (back) f.push(...barFaults(back.html, LIVE.rows, expectedRest(LIVE.rows)).map((x) => `closed again: ${x}`));
    detail = run.states.map((s) => `${s.how} -> ${shownBars(s.html).length} bars`).join('; ');
  } catch (e) { f.push(`RENDER: ${String(e.message).split('\n')[0]}`); }
  arms.push(['ON DEMAND: one data-price-expand control; a click shows every served bar in the same panel, a second click returns to the top movers',
    f.length === 0, f.length === 0 ? detail : `${detail ? detail + ' || ' : ''}${f.slice(0, 4).join(' | ')}`]);
}
// ---------------- arm 3: the window in words ----------------
{
  const f = [];
  const asOf = (p) => p.as_of_date || (p.rows[0] || {}).as_of_date;
  const cases = [
    ['live', LIVE, { days: LIVE.rows[0].window_days, asOf: asOf(LIVE) }],
    ['planted 90 days to 2026-09-29', plant(LIVE, (p) => { p.as_of_date = '2026-09-29'; for (const r of p.rows) { r.window_days = 90; r.as_of_date = '2026-09-29'; } }), { days: 90, asOf: '2026-09-29' }],
    ['planted window_days not served', plant(LIVE, (p) => { for (const r of p.rows) delete r.window_days; }), { days: null, asOf: asOf(LIVE) }],
  ];
  for (const [label, p, want] of cases) {
    try {
      const html = R.renderState(render(p)).html;
      f.push(...windowFaults(html, want).map((x) => `${label}: ${x}`));
    } catch (e) { f.push(`${label}: RENDER: ${String(e.message).split('\n')[0]}`); }
  }
  arms.push(['WINDOW IN WORDS: "change over the last <served window_days> days to <served as_of_date>", never a computed or stale window',
    f.length === 0, f.length === 0 ? `3 of 3 payloads (30 / planted 90 / planted not served)` : f.slice(0, 4).join(' | ')]);
}
// ---------------- arm 4: planted controls ----------------
{
  const f = [];
  const rows = LIVE.rows;
  const rest = expectedRest(rows);
  const absSorted = [...expectedAll(rows)].sort((a, b) => Math.abs(ret(b)) - Math.abs(ret(a)));
  const bar = (r, noTitle) => `<li data-price-bar="${esc(keyOf(r))}"${noTitle ? '' : ` title="${esc(`${nameOf(r) || r.ticker} (${r.ticker})`)}"`}><span class="truncate">${esc(nameOf(r) || r.ticker)}</span><span>${ret(r) > 0 ? '+' : '-'}${Math.abs(ret(r)).toFixed(1)}%</span></li>`;
  const synth = (shown, hidden) => `<div><ol>${shown.map((r) => bar(r)).join('')}</ol>${hidden ? `<details><summary data-price-expand="">Show every name</summary><ol>${hidden.map((r) => bar(r)).join('')}</ol></details>` : ''}<p data-price-window="">Change over the last 30 days to October 1st, 2026</p></div>`;
  const grade = (html) => barFaults(html, rows, rest);
  const good = grade(synth(rest));
  if (good.length) f.push(`the reference markup fails: ${good[0]}`);
  const goodDetails = grade(synth(rest, expectedAll(rows).filter((r) => !rest.includes(r))));
  if (goodDetails.length) f.push(`the reference with the rest in a closed <details> fails: ${goodDetails[0]}`);
  const swapped = [...rest];
  [swapped[1], swapped[2]] = [swapped[2], swapped[1]];
  const MUT = [
    ['all94', synth(absSorted), 'COUNT'],
    ['abs20', synth(absSorted.slice(0, 20)), 'SET'],
    ['swap', synth(swapped), 'ORDER'],
    ['notitle', synth(rest).replace(/ title="[^"]*"/, ''), 'TITLE'],
  ];
  const caught = [];
  for (const [n, html, cls] of MUT) {
    const fx = grade(html);
    if (fx.some((x) => x.startsWith(cls + ':'))) caught.push(`${n}->${cls}`); else f.push(`mutant ${n} not rejected as ${cls} (${fx[0] || 'no fault'})`);
  }
  const w30 = { days: 30, asOf: '2026-10-01' };
  const okW = windowFaults(synth(rest), w30);
  if (okW.length) f.push(`the reference caption fails: ${okW[0]}`);
  const WMUT = [
    ['no date', synth(rest).replace(' to October 1st, 2026', ''), w30],
    ['30 where 90 is served', synth(rest), { days: 90, asOf: '2026-10-01' }],
    ['stale hover', synth(rest).replace('<p data-price-window="">Change over the last 30 days', '<p data-price-window="">Change over the last 90 days').replace(/ title="([^"]*)"/, ' title="$1; +1.0% over 30 days"'), { days: 90, asOf: '2026-10-01' }],
  ];
  for (const [n, html, want] of WMUT) {
    const fx = windowFaults(html, want);
    if (fx.some((x) => x.startsWith('WINDOW:'))) caught.push(`${n}->WINDOW`); else f.push(`mutant "${n}" not rejected as WINDOW`);
  }
  arms.push(['PLANTED: the reference (and the same set with the rest in a closed <details>) passes; all-94, top-20-by-size, a swap, a missing title, an undated, a wrong-N and a stale-hover caption are each rejected',
    f.length === 0, f.length === 0 ? `reference 0 faults, details variant 0 faults; ${caught.length} of ${MUT.length + WMUT.length} mutants rejected (${caught.join(', ')})` : f.join(' | ')]);
}

let pass = 0;
for (const [n, ok, d] of arms) { if (ok) pass += 1; console.log(`${ok ? 'ARM PASS' : 'ARM FAIL'} ${n} :: ${d}`); }
console.log(`WALL: ${((Date.now() - T0) / 1000).toFixed(1)}s`);
console.log(`THE PRICE FACE SHOWS THE TOP MOVERS, OPENS ON DEMAND AND NAMES ITS WINDOW: ${pass} of ${arms.length} arms`);
process.exit(pass === arms.length ? 0 : 1);
