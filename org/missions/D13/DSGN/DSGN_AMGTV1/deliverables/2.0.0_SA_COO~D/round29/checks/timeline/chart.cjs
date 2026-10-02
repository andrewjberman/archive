/**
 * chart.cjs -- DSGN_AMGTV1 round 29, AV-zg-1 TIMELINE, check 1 of 2 (issuer 2.0.0_SA_COO~D):
 * THE TIMELINE IS A RECHARTS CHART OF ARTICLES PER DAY, IN ONE HUE, WITH THE SHARED TOOLTIP AND ITS MARKERS ON THE CHART.
 *
 * Usage: cd <dir whose portal/ is the checkout under test> && node <this file>
 * Renders the real components/TimelinePanel.tsx (export `TimelinePanel`, prop `securityKey`) through ./_tl.cjs -- read its header
 * for the stubs and for how a static render is pressed. Writes no file.
 *
 * Grades PRD FWD-5 v0.9 DONE WHEN (prd/DSGN_AMGTV1_PRD.md, the v0.9 block under FWD-5):
 *   "the timeline is a recharts chart at a readable height, with a labelled y-axis (articles per day) and dated ticks";
 *   "bars use one data-family hue, and no status colour paints a bar (search state is a non-status cue or a tooltip line)";
 *   "hovering a day shows its articles, distinct publishers, mention count and strongest headline in the shared tooltip";
 *   "coverage events and earnings releases are markers ON the chart at their dates"; "Earnings markers render the served marker,
 *   or its designed empty state while the producer has none".
 * Register rows (docs/briefs/amgt-security-analysis-ui-findings-20261002.json): SAUX-06 (labelled y-axis, dated ticks, the
 * library), SAUX-07 (one hue, no status colour on a bar), SAUX-08 (the hover), SAUX-09 (events as markers with a headline label,
 * no text list); decomposition v29 ruling (c) (earnings_release not served -> the designed empty state in words).
 * Inputs: SERVED /timeline bodies round14/fixtures/timeline.BA_US_Equity.json (273 days, all DENIED, 26 days with articles,
 *   1 served event 2026-09-08) and timeline.992_HK_Equity.json (273 days, all PARTIAL, 3 served events); SERVED /timeline/day
 *   bodies BA 2026-09-08 (5 articles) and 992 HK 2026-08-13 (2 articles); the served overlay BA (round14). ISSUER VARIANTS,
 *   labelled: BA with its day statuses cycled COMPLETE / PARTIAL / DENIED (the mixed case no capture holds); BA with a `markers`
 *   array grafted from round29/fixtures/timeline/markers.BA_US_Equity.PLANTED.json (FWD-37's shape; not served today); the
 *   planted day body round29/fixtures/timeline/timelineDay.BA_US_Equity.2026-09-07.PLANTED.json (a non-event day).
 * Arms:
 *   1  CHART: a recharts chart with ONE Bar, plotting `articles_total`, drawn for every served day (the chart's data is the whole
 *      served series); the YAxis label reads "articles per day"; the XAxis ticks are
 *      dates in words or M/D (never tick={false}, never the raw ISO); the chart is at least 200px tall; every bar of BA, 992 HK
 *      and the mixed variant is painted ONE colour (opacity ignored; a url(#pattern) fill resolves to its pattern's colours) and
 *      none is a status colour.
 *   2  TOOLTIP: the Tooltip's content renders the estate's shared DataTooltip, and for BA 2026-09-08, BA 2026-09-07 (planted, no
 *      event) and 992 HK 2026-08-13 it states the date, the article count, the distinct publishers, the mention count and the
 *      strongest headline (the first article the day route serves, or the lead headline of a served event covering the day), with
 *      no code-shaped word.
 *   3  MARKERS: every served event is a [data-timeline-marker="coverage_event"][data-marker-day=<first_day>] drawn INSIDE the
 *      chart and carrying its lead headline (visible, <title>, title= or aria-label=); no event list outside the chart; while no
 *      earnings date is served (today's payload, and the interim reason row) a [data-timeline-earnings-empty] says so in words
 *      and no earnings marker is drawn; with a served earnings_release it is a marker at its date with its label, the empty state
 *      is gone, and the event served in both `events` and `markers` is drawn once.
 *   4  PLANTED (control): the paint, tooltip and marker predicates reject known-bad inputs and accept known-good ones.
 * Prints one line per arm and "THE TIMELINE IS A RECHARTS CHART OF ARTICLES PER DAY WITH THE SHARED TOOLTIP AND MARKERS ON IT:
 * <k> of 4 arms"; exit 0 only at 4 of 4.
 */
const path = require('path');
const T = require(path.join(__dirname, '_tl.cjs'));
const { React, h, FX, clone, renderPanel, renderState, byAttr, all, visible, readable, inChart, parse, norm, CODE, STATUS, CHARTS } = T;

// ---- inputs ------------------------------------------------------------------------------------------------------------
const BA = FX.rangeBA;
const HK = FX.rangeHK;
const MIXED = clone(BA); // ISSUER VARIANT: the three day states side by side
MIXED.series.forEach((e, i) => {
  e.data_status = ['COMPLETE', 'PARTIAL', 'DENIED'][i % 3];
  if (e.data_status === 'PARTIAL') e.publishers_covered_codes = ['wsj'];
});
const withMarkers = (arr) => Object.assign(clone(BA), { markers: clone(arr) });
const DAYS_BA = { '2026-09-08': FX.dayBA0908, '2026-09-07': FX.dayBA0907 };
const DAYS_HK = { '2026-08-13': FX.dayHK0813 };

// ---- predicates --------------------------------------------------------------------------------------------------------
const NOT_PAINT = new Set(['', 'none', 'transparent', 'white', '#fff', '#ffffff', 'hsl(var(--palette-white))', 'currentcolor', 'undefined']);
function normColour(c) {
  return String(c)
    .toLowerCase()
    .replace(/\s+/g, '')
    .replace(/\/[\d.]+%?\)$/, ')')
    .replace(/^rgba\((\d+),(\d+),(\d+),[\d.]+\)$/, 'rgb($1,$2,$3)')
    .replace(/^(#[0-9a-f]{6})[0-9a-f]{2}$/, '$1');
}
function styleProp(style, prop) {
  const m = new RegExp('(?:^|;)\\s*' + prop + '\\s*:\\s*([^;]+)', 'i').exec(style || '');
  return m ? m[1].trim() : undefined;
}
/** The colours one bar slot paints with: the first element carrying a fill, its fill and stroke, a url(#id) fill resolved to
 * every fill/stroke inside that <pattern>. */
function slotColours(tree, slot) {
  const nodes = [slot, ...all(slot, () => true)];
  const el = nodes.find((n) => n.attrs && (n.attrs.fill !== undefined || styleProp(n.attrs.style, 'fill') !== undefined));
  if (!el) return [];
  const out = [];
  for (const raw of [el.attrs.fill, styleProp(el.attrs.style, 'fill'), el.attrs.stroke, styleProp(el.attrs.style, 'stroke')]) {
    if (raw === undefined) continue;
    const m = /^url\(#([^)]+)\)$/.exec(raw.trim());
    if (m) {
      const pat = all(tree, (n) => n.tag === 'pattern' && n.attrs.id === m[1])[0];
      if (!pat) out.push('UNRESOLVED ' + raw);
      else for (const n of all(pat, () => true)) for (const v of [n.attrs.fill, n.attrs.stroke]) if (v !== undefined) out.push(v);
    } else out.push(raw);
  }
  return out.filter((c) => !NOT_PAINT.has(normColour(c)));
}
function paintFaults(colours) {
  const f = [];
  if (colours.length === 0) return ['NO PAINT: no bar declares a colour'];
  const st = colours.filter((c) => STATUS.test(c));
  if (st.length) f.push(`STATUS COLOUR on a bar: ${[...new Set(st)].slice(0, 2).join(', ')}`);
  const hues = [...new Set(colours.map(normColour))];
  if (hues.length > 1) f.push(`${hues.length} colours across the bars (one hue wanted): ${hues.slice(0, 3).join(', ')}`);
  return f;
}
function labelWords(v) {
  if (v === undefined || v === null || v === false) return '';
  if (typeof v === 'string' || typeof v === 'number') return String(v);
  if (React.isValidElement(v)) return labelWords(v.props.value) || labelWords(v.props.children);
  if (Array.isArray(v)) return v.map(labelWords).join(' ');
  if (typeof v === 'object') return labelWords(v.value) || labelWords(v.children);
  return '';
}
const MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
function tickWords(xaxis) {
  const p = xaxis.props;
  if (p.tick === false) return { faults: ['XAxis tick={false}: no dated ticks'] };
  let out;
  try {
    if (typeof p.tickFormatter === 'function') out = String(p.tickFormatter('2026-03-01', 0));
    else if (React.isValidElement(p.tick) || typeof p.tick === 'function') {
      const tp = { x: 0, y: 0, index: 0, payload: { value: '2026-03-01', coordinate: 0, index: 0 } };
      const el = React.isValidElement(p.tick) ? React.cloneElement(p.tick, tp) : p.tick(tp);
      out = visible(parse(T.L.render(() => el)));
    } else out = '2026-03-01';
  } catch (e) {
    return { faults: ['tick formatter threw: ' + String(e.message).split('\n')[0]] };
  }
  const dated = new RegExp(`\\b(${MONTHS.map((m) => m.slice(0, 3)).join('|')})[a-z]*\\b|\\b\\d{1,2}/\\d{1,2}\\b`).test(out) && out !== '2026-03-01';
  return { out, faults: dated ? [] : [`a tick for 2026-03-01 reads "${out}" (a month word or M/D wanted, never the ISO)`] };
}
function chartHeight(tree) {
  const node = byAttr(tree, 'data-rc', 'ResponsiveContainer')[0] || all(tree, (n) => CHARTS.has(n.attrs['data-rc']))[0];
  if (!node) return 0;
  const hs = [];
  for (const n of [node, ...all(node, (x) => CHARTS.has(x.attrs['data-rc']))]) {
    const v = Number(n.attrs['data-rc-height']);
    if (Number.isFinite(v) && v > 0) hs.push(v);
  }
  for (let n = node.parent; n && n.tag !== '#root'; n = n.parent) {
    const cls = n.attrs.class || '';
    const px = /(?:^|\s)h-\[(\d+)px\]/.exec(cls);
    const tw = /(?:^|\s)h-(\d+)(?:\s|$)/.exec(cls);
    const st = /(?:^|;)\s*height\s*:\s*(\d+)px/.exec(n.attrs.style || '');
    const v = px ? Number(px[1]) : tw ? Number(tw[1]) * 4 : st ? Number(st[1]) : null;
    if (v) {
      hs.push(v);
      break;
    }
  }
  return hs.length ? Math.max(...hs) : 0;
}
/** tt = { header, rows: [{label, value}], text }; want = { date, articles, publishers, mentions, headlines[] }. */
function tooltipFaults(tt, want) {
  if (!tt) return ['NOT THE SHARED TOOLTIP: the content renders no DataTooltip'];
  const f = [];
  const all2 = norm([tt.header, ...tt.rows.map((r) => `${r.label}: ${r.value}`)].join(' '));
  const [y, mo, d] = want.date.split('-').map(Number);
  const month = MONTHS[mo - 1];
  const dated = (new RegExp(`\\b${month.slice(0, 3)}[a-z]*\\.?\\s+${d}(st|nd|rd|th)?\\b`, 'i').test(all2) || new RegExp(`\\b${mo}/${d}\\b`).test(all2));
  if (!dated) f.push(`NO DATE: "${month} ${d}" not stated`);
  const row = (re) => tt.rows.find((r) => re.test(r.label));
  const num = (r, n) => r && new RegExp(`(^|[^\\d.])${n}([^\\d.]|$)`).test(r.value);
  if (!num(row(/article/i), want.articles)) f.push(`ARTICLES: no "article" row stating ${want.articles}`);
  if (!num(row(/publisher/i), want.publishers)) f.push(`PUBLISHERS: no "publisher" row stating ${want.publishers}`);
  if (!num(row(/mention/i), want.mentions)) f.push(`MENTIONS: no "mention" row stating ${want.mentions}`);
  const hr = row(/headline/i);
  if (!hr || !want.headlines.some((x) => norm(hr.value).includes(norm(x)))) f.push(`HEADLINE: no "headline" row carrying "${want.headlines[0].slice(0, 40)}"`);
  if (CODE.test(all2)) f.push(`CODE: "${all2.match(CODE)[0]}"`);
  return f;
}
function readTooltip(tree) {
  const tt = byAttr(tree, 'data-shared-tooltip')[0];
  if (!tt) return null;
  const hd = byAttr(tt, 'data-tt-header')[0];
  const rows = byAttr(tt, 'data-tt-row').map((r) => {
    const label = r.attrs['data-tt-label'] || '';
    const v = visible(r);
    return { label, value: v.startsWith(label) ? v.slice(label.length).replace(/^\s*:\s*/, '') : v };
  });
  return { header: hd ? visible(hd) : '', rows };
}
/** Faults for one marker: exactly `count` (default 1) [data-timeline-marker=kind][data-marker-day=date], each inside the chart,
 * each carrying `words` in its readable text. */
function markerFaults(tree, kind, date, words, count) {
  const ms = all(tree, (n) => n.attrs['data-timeline-marker'] === kind && n.attrs['data-marker-day'] === date);
  const want = count === undefined ? 1 : count;
  const f = [];
  if (ms.length !== want) f.push(`${kind} ${date}: ${ms.length} marker(s), ${want} wanted`);
  for (const m of ms) {
    if (!inChart(m)) f.push(`${kind} ${date}: marker drawn outside the chart`);
    if (words && !readable(m).includes(norm(words))) f.push(`${kind} ${date}: marker does not carry "${words.slice(0, 40)}"`);
  }
  return f;
}
function earningsEmptyFaults(tree) {
  const f = [];
  const e = byAttr(tree, 'data-timeline-earnings-empty');
  if (e.length !== 1) f.push(`${e.length} [data-timeline-earnings-empty] (1 wanted while no earnings date is served)`);
  else {
    const t = visible(e[0]);
    if (!/earnings/i.test(t)) f.push(`the earnings empty state does not say "earnings": "${t.slice(0, 60)}"`);
    if (CODE.test(t)) f.push(`CODE in the earnings empty state: "${t.match(CODE)[0]}"`);
  }
  const em = all(tree, (n) => n.attrs['data-timeline-marker'] === 'earnings_release');
  if (em.length) f.push(`${em.length} earnings marker(s) drawn while none is served`);
  return f;
}

const arms = [];
// ---- arm 1: the chart ----------------------------------------------------------------------------------------------------
{
  const f = [];
  for (const [name, range] of [['BA', BA], ['992 HK', HK], ['MIXED (variant)', MIXED]]) {
    const s = renderPanel(range, {});
    if (/^RENDER FAILED/.test(s.html)) { f.push(`${name}: ${s.html.slice(0, 120)}`); continue; }
    const chart = s.rc.find((c) => CHARTS.has(c.name));
    if (!chart) { f.push(`${name}: no recharts chart rendered`); continue; }
    const bars = s.rc.filter((c) => c.name === 'Bar');
    const sample = range.series.find((e) => e.articles_total > 0);
    const plotsArticles = (b) => {
      const dk = b.props.dataKey;
      return dk === 'articles_total' || (typeof dk === 'function' && !!sample && dk(sample) === sample.articles_total);
    };
    if (bars.length !== 1 || !plotsArticles(bars[0])) {
      const dks = bars.map((b) => (typeof b.props.dataKey === 'function' ? 'a function' : JSON.stringify(b.props.dataKey))).join(', ');
      f.push(`${name}: ${bars.length} Bar(s) plotting ${dks || 'nothing'} (one Bar of articles_total wanted)`);
    }
    const slots = byAttr(s.tree, 'data-rc-bar-slot');
    const drawn = new Set(slots.map((sl) => sl.attrs['data-rc-bar-slot']));
    const undrawn = range.series.filter((e) => !drawn.has(e.date)).length;
    if (undrawn) f.push(`${name}: ${undrawn} of ${range.series.length} served days have no bar (the chart's data is the whole served series)`);
    const colours = [];
    for (const sl of slots) colours.push(...slotColours(s.tree, sl));
    f.push(...paintFaults(colours).map((x) => `${name}: ${x}`));
    if (name === 'BA') {
      const ya = s.rc.find((c) => c.name === 'YAxis');
      const lw = ya ? norm([labelWords(ya.props.label), ...React.Children.toArray(ya.props.children).map((c) => labelWords(c.props))].join(' ')) : '';
      if (!(/article/i.test(lw) && /\bper day\b|\ba day\b|\bdaily\b/i.test(lw))) f.push(`YAxis label reads "${lw}" ("articles per day" wanted)`);
      const xa = s.rc.find((c) => c.name === 'XAxis');
      if (!xa) f.push('no XAxis');
      else f.push(...tickWords(xa).faults);
      const ht = chartHeight(s.tree);
      if (ht < 200) f.push(`chart height ${ht}px (at least 200px wanted)`);
    }
  }
  arms.push(['CHART: a recharts chart of articles per day, labelled y-axis, dated ticks, >= 200px, every bar one non-status hue', f.length === 0, f.length === 0 ? 'BA, 992 HK and the mixed variant' : f.slice(0, 6).join(' | ')]);
}
// ---- arm 2: the hover ----------------------------------------------------------------------------------------------------
{
  const f = [];
  const cases = [
    ['BA', BA, DAYS_BA, '2026-09-08', [BA.events[0].lead_headline, FX.dayBA0908.articles[0].headline]],
    ['BA (planted day)', BA, DAYS_BA, '2026-09-07', [FX.dayBA0907.articles[0].headline]],
    ['992 HK', HK, DAYS_HK, '2026-08-13', [HK.events[2].lead_headline, FX.dayHK0813.articles[0].headline]],
  ];
  for (const [name, range, days, date, heads] of cases) {
    const s = renderPanel(range, days);
    const tip = s.rc.find((c) => c.name === 'Tooltip');
    const c = tip && tip.props.content;
    if (!c) { f.push(`${name}: the Tooltip has no content (the shared DataTooltip wanted)`); continue; }
    const entry = range.series.find((e) => e.date === date);
    const tp = { active: true, label: date, coordinate: { x: 0, y: 0 }, payload: [{ payload: entry, value: entry.articles_total, dataKey: 'articles_total', name: 'articles_total' }] };
    const el = React.isValidElement(c) ? React.cloneElement(c, tp) : typeof c === 'function' ? h(c, tp) : null;
    const r = renderState(() => el, {});
    if (/^RENDER FAILED/.test(r.html)) { f.push(`${name} ${date}: ${r.html.slice(0, 100)}`); continue; }
    const want = { date, articles: entry.articles_total, publishers: entry.publishers_distinct, mentions: entry.mention_count_total, headlines: heads };
    f.push(...tooltipFaults(readTooltip(r.tree), want).map((x) => `${name} ${date}: ${x}`));
  }
  arms.push(['TOOLTIP: the shared DataTooltip states date, articles, distinct publishers, mention count and strongest headline', f.length === 0, f.length === 0 ? '3 of 3 days' : f.slice(0, 6).join(' | ')]);
}
// ---- arm 3: the markers --------------------------------------------------------------------------------------------------
{
  const f = [];
  const sBA = renderPanel(BA, {});
  f.push(...markerFaults(sBA.tree, 'coverage_event', '2026-09-08', BA.events[0].lead_headline).map((x) => `BA: ${x}`));
  f.push(...earningsEmptyFaults(sBA.tree).map((x) => `BA (served): ${x}`));
  const list = byAttr(sBA.tree, 'data-timeline-event').filter((n) => !inChart(n));
  if (list.length) f.push(`BA: ${list.length} [data-timeline-event] element(s) listed outside the chart`);
  if (/press one to open/i.test(visible(sBA.tree))) f.push('BA: the "press one to open its first day" list still renders');
  const sHK = renderPanel(HK, {});
  for (const ev of HK.events) f.push(...markerFaults(sHK.tree, 'coverage_event', ev.first_day, ev.lead_headline).map((x) => `992 HK: ${x}`));
  const sW = renderPanel(withMarkers(FX.markers.with_earnings), {});
  const er = FX.markers.with_earnings[0];
  f.push(...markerFaults(sW.tree, 'earnings_release', er.date, er.label).map((x) => `BA+earnings (variant): ${x}`));
  if (byAttr(sW.tree, 'data-timeline-earnings-empty').length) f.push('BA+earnings (variant): the earnings empty state renders beside a served earnings marker');
  f.push(...markerFaults(sW.tree, 'coverage_event', '2026-09-08', null, 1).map((x) => `BA+earnings (variant): ${x}`));
  const sI = renderPanel(withMarkers(FX.markers.interim), {});
  f.push(...earningsEmptyFaults(sI.tree).map((x) => `BA interim reason row (variant): ${x}`));
  f.push(...markerFaults(sI.tree, 'coverage_event', '2026-09-08', null, 1).map((x) => `BA interim (variant): ${x}`));
  arms.push(['MARKERS: served events and earnings releases are markers inside the chart at their dates; no earnings date = the empty state in words', f.length === 0, f.length === 0 ? 'BA 1 event, 992 HK 3 events, earnings served / interim / absent' : f.slice(0, 6).join(' | ')]);
}
// ---- arm 4: planted controls ---------------------------------------------------------------------------------------------
{
  const f = [];
  if (!paintFaults(['hsl(var(--status-danger))']).length) f.push('paint: a status-red bar accepted');
  if (!paintFaults(['#5F3BE3', '#11CDEF']).length) f.push('paint: two hues accepted');
  if (paintFaults(['hsl(var(--data-chart-purple))', 'hsl(var(--data-chart-purple) / 0.4)']).length) f.push('paint: one hue at two opacities rejected');
  const want = { date: '2026-09-08', articles: 5, publishers: 3, mentions: 39, headlines: ['Boeing Delivers 51 Jets in August, Lowest in Four Months'] };
  const good = { header: 'September 8th, 2026', rows: [{ label: 'Articles', value: '5' }, { label: 'Distinct publishers', value: '3' }, { label: 'Mentions', value: '39' }, { label: 'Strongest headline', value: 'Boeing Delivers 51 Jets in August, Lowest in Four Months' }] };
  if (tooltipFaults(good, want).length) f.push(`tooltip: a full one rejected (${tooltipFaults(good, want)[0]})`);
  const noMention = { header: good.header, rows: good.rows.filter((r) => !/Mention/.test(r.label)) };
  if (!tooltipFaults(noMention, want).length) f.push('tooltip: one without the mention count accepted');
  const coded = { header: good.header + ' DENIED', rows: good.rows };
  if (!tooltipFaults(coded, want).length) f.push('tooltip: one carrying a served code accepted');
  if (!tooltipFaults(null, want).length) f.push('tooltip: a non-shared tooltip accepted');
  const head = 'Boeing Delivers 51 Jets in August, Lowest in Four Months';
  const on = parse(`<div data-rc="BarChart"><div data-rc="ReferenceDot"><g data-timeline-marker="coverage_event" data-marker-day="2026-09-08" aria-label="${head}"><circle></circle></g></div></div>`);
  if (markerFaults(on, 'coverage_event', '2026-09-08', head).length) f.push('marker: one inside the chart rejected');
  const off = parse(`<div data-rc="BarChart"></div><ul><li><button data-timeline-marker="coverage_event" data-marker-day="2026-09-08">${head}</button></li></ul>`);
  if (!markerFaults(off, 'coverage_event', '2026-09-08', head).length) f.push('marker: one listed outside the chart accepted');
  arms.push(['PLANTED (control): paint, tooltip and marker predicates reject bad inputs and accept good ones', f.length === 0, f.length === 0 ? '6 of 6 rejected, 3 of 3 accepted' : f.join(' | ')]);
}

let pass = 0;
for (const [n, ok, d] of arms) {
  if (ok) pass += 1;
  console.log(`${ok ? 'ARM PASS' : 'ARM FAIL'} ${n} :: ${d}`);
}
console.log(`THE TIMELINE IS A RECHARTS CHART OF ARTICLES PER DAY WITH THE SHARED TOOLTIP AND MARKERS ON IT: ${pass} of 4 arms`);
process.exit(pass === 4 ? 0 : 1);
