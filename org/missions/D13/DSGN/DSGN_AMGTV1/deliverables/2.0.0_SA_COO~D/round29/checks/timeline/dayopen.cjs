/**
 * dayopen.cjs -- DSGN_AMGTV1 round 29, AV-zg-1 TIMELINE, check 2 of 2 (issuer 2.0.0_SA_COO~D):
 * THE SELECTED DAY OPENS IN THE PAGE'S HERO DIALOG, ITS ROWS READ HEADLINE, PUBLISHER AND TIME, AND THE HEADER BRIEF IS THE
 * RECENT-NEWS CARD ABOVE THE ONE TIMELINE.
 *
 * Usage: cd <dir whose portal/ is the checkout under test> && node <this file>
 * Renders the real components/HeaderBrief.tsx and components/TimelinePanel.tsx through ./_tl.cjs, alone and as the overlay
 * mounts them (the issuer's round-29 ruling for AV-zg-2's SecurityOverlay.tsx: <HeaderBrief bundle /> with no postureLine, then
 * <TimelinePanel securityKey />). Read _tl.cjs's header for the stubs and for how a static render is pressed (a recorded onClick
 * is called and the page rendered again with the state it set). Writes no file.
 *
 * Grades PRD FWD-5 v0.9 DONE WHEN: "recent news is its own card ABOVE the timeline"; "the selected day opens in the page's shared
 *   HeroDialog, never inline under the chart"; "article rows read headline, publisher and time at rest"; markers "each opening
 *   that day". FWD-27 (its lines in this cell): "0 strings from the register's system-wording list"; "an unconnected field prints
 *   no line". The issuer's round-29 ruling (from AV-zg-2's findings): HeaderBrief no longer mounts TimelinePanel; HeaderBrief is
 *   the recent-news card, the company description sits in a closed native <details> with a reader-words <summary>, there is no
 *   posture slot (`postureLine` optional and ignored) and no Social / most-discussed line; TimelinePanel keeps its export name
 *   and its `securityKey` prop.
 * Register rows: SAUX-11 (news its own card above; the day in its own modal, never one column with the news), SAUX-13 (rows at
 *   rest = headline, publisher, time; mention count, headline/lead flags and tier open on demand), SAUX-14 (no status-coloured
 *   text), SAUX-15 (description not at rest), SAUX-30 ("day(s) rendered (no gap)"), SAUX-31 ("Social: no source measured",
 *   "MOST-DISCUSSED: NOT MEASURED").
 * Inputs: SERVED round14 fixtures: overlay.BA_US_Equity.json (description SERVED; 1 feed item; social status "no source measured
 *   (S13)", no social items), timeline.BA_US_Equity.json (event 2026-09-08), timeline.992_HK_Equity.json,
 *   timelineDay.BA_US_Equity.2026-09-08.json (5 articles, DENIED), timelineDay.992_HK_Equity.2026-08-13.json (2 articles, PARTIAL).
 * Arms:
 *   1  DIALOG: at rest no article row and no open dialog; pressing BA's 2026-09-08 bar, BA's 2026-09-08 event marker and 992 HK's
 *      2026-08-13 bar each opens the HeroDialog of `@/ui/components/graphic/HeroGraphic` holding every served article row of that
 *      day ([data-timeline-article=<article_key>]) in the served order, and no article row renders outside the dialog.
 *   2  ROWS AND INK: in BA's 2026-09-08 dialog each row's at-rest text carries the headline, the publisher's name and the ET clock
 *      (dateWords.longStamp's, e.g. "10:06a"), and none of: a mention count, "in headline", "in lead", "tier"; the mention count,
 *      the headline and lead flags and "Tier <letter>" sit in [data-article-detail=<article_key>], either inside a closed native
 *      <details> or drawn only after pressing [data-article-more=<article_key>]; and no element painted a status colour holds
 *      text -- at rest, in BA's dialog (a DENIED day) or in 992 HK's (a PARTIAL day).
 *   3  HEADER BRIEF AND WORDS: HeaderBrief alone mounts no timeline; a planted postureLine prop renders nothing; [data-header-feed]
 *      renders once; [data-header-description] sits inside a closed <details> whose <summary> has words and no code; in the overlay
 *      the news card comes before the one [data-timeline-panel] and neither holds the other; no visible "day(s) rendered" / "no
 *      gap" / "most-discussed" / "Social:" / "no source measured" / "not measured" / "press one to open" at rest (BA, 992 HK).
 *   4  PLANTED (control): the row, status-text, order and description predicates reject known-bad markup and accept known-good.
 * Prints one line per arm and "THE DAY OPENS IN THE HERO DIALOG AND THE HEADER BRIEF IS THE NEWS CARD ABOVE THE ONE TIMELINE:
 * <k> of 4 arms"; exit 0 only at 4 of 4.
 */
const path = require('path');
const T = require(path.join(__dirname, '_tl.cjs'));
const { L, h, FX, renderOverlay, renderHeader, press, pressDay, pressMarker, byAttr, all, visible, within, inHero, parse, norm, CODE, STATUS } = T;

let publisherName = (c) => String(c);
try {
  publisherName = L.source('src/pages/SecurityAnalysis/components/publisherNames.ts').publisherName;
} catch (e) {
  /* the fault surfaces as a missing publisher */
}
const clockOf = (utc) => {
  const s = T.dateWords ? T.dateWords.longStamp(utc) : '';
  const m = /\b(\d{1,2}:\d{2}[ap])\b/i.exec(s);
  return m ? m[1] : null;
};
const BA = FX.rangeBA;
const HK = FX.rangeHK;
const DAYS_BA = { '2026-09-08': FX.dayBA0908, '2026-09-07': FX.dayBA0907 };
const DAYS_HK = { '2026-08-13': FX.dayHK0813 };

// ---- predicates --------------------------------------------------------------------------------------------------------
function dialogFaults(state, day) {
  if (!state) return ['pressing it set no state -- nothing opened'];
  if (/^RENDER FAILED/.test(state.html)) return [state.html.slice(0, 120)];
  const f = [];
  if (!byAttr(state.tree, 'data-hero-graphic').length) f.push('no HeroDialog opened');
  const rows = byAttr(state.tree, 'data-timeline-article');
  const outside = rows.filter((r) => !inHero(r));
  if (outside.length) f.push(`${outside.length} article row(s) drawn inline, outside the HeroDialog`);
  const keys = rows.filter((r) => inHero(r)).map((r) => r.attrs['data-timeline-article']);
  const want = day.articles.map((a) => a.article_key);
  const missing = want.filter((k) => !keys.includes(k));
  if (missing.length) f.push(`${missing.length} of ${want.length} served rows missing from the dialog`);
  else {
    const at = want.map((k) => keys.indexOf(k));
    if (!at.every((p, i) => i === 0 || p > at[i - 1])) f.push('rows not in the served order');
  }
  return f;
}
const META = /\bnamed\b|\bmention(s|ed)?\b|\bin (the )?headline\b|\bin (the )?lead\b|\btier\b|\bsignal\b/i;
const isDetail = (n) => n.attrs && n.attrs['data-article-detail'] !== undefined;
/** The at-rest faults of one row (the row's text with every [data-article-detail] subtree left out). */
function restFaults(tree, a, clock) {
  const row = byAttr(tree, 'data-timeline-article', a.article_key)[0];
  if (!row) return ['NO ROW'];
  const rest = visible(row, isDetail);
  const f = [];
  const head = norm(a.headline || '');
  if (!rest.includes(head)) f.push('headline not at rest');
  const pub = publisherName(a.publisher);
  if (!rest.includes(pub)) f.push(`publisher "${pub}" not at rest`);
  if (clock && !rest.toLowerCase().includes(clock.toLowerCase())) f.push(`time "${clock}" not at rest`);
  const m = rest.split(head).join(' ').match(META);
  if (m) f.push(`metadata at rest: "${m[0]}"`);
  return f;
}
function detailWordsFaults(node, a) {
  const t = visible(node);
  const f = [];
  if (!new RegExp(`(^|[^\\d])${a.mention_count}([^\\d]|$)`).test(t)) f.push(`mention count ${a.mention_count} not in the detail`);
  if (!/headline/i.test(t)) f.push('headline flag not in the detail');
  if (!/\blead\b/i.test(t)) f.push('lead flag not in the detail');
  if (a.signal_tier && !new RegExp(`\\btier\\W{0,3}${a.signal_tier}\\b`, 'i').test(t)) f.push(`"Tier ${a.signal_tier}" not in the detail`);
  return f;
}
const closedDetailsAround = (n) => {
  const det = within(n, (x) => x.tag === 'details');
  return det && det.attrs.open === undefined ? det : null;
};
/** At rest the detail is absent or inside a closed <details>; opened (natively, or by pressing [data-article-more]) it holds the
 * mention count, both flags and the tier. */
function detailFaults(state, a) {
  const at = byAttr(state.tree, 'data-article-detail', a.article_key);
  if (at.length) {
    const f = [];
    for (const d of at) if (!closedDetailsAround(d)) f.push('detail drawn open at rest (no closed <details> around it)');
    return f.concat(detailWordsFaults(at[0], a));
  }
  const more = state.captured.find((c) => c.props['data-article-more'] === a.article_key);
  if (!more) return ['no [data-article-detail] and no [data-article-more] to open it'];
  const next = press(state, () => more.props.onClick({ stopPropagation() {}, preventDefault() {} }));
  if (!next) return ['pressing [data-article-more] set no state'];
  const d = byAttr(next.tree, 'data-article-detail', a.article_key)[0];
  return d ? detailWordsFaults(d, a) : ['pressing [data-article-more] drew no [data-article-detail]'];
}
function styleProp(style, prop) {
  const m = new RegExp('(?:^|;)\\s*' + prop + '\\s*:\\s*([^;]+)', 'i').exec(style || '');
  return m ? m[1].trim() : undefined;
}
const STATUS_CLASS = /^(text|fill)-(\[.*--status-.*\]|status-[a-z]+|danger|warning|success|destructive|(red|orange|amber|yellow|green|emerald|rose)-\d+)/i;
/** Every element whose own ink is a status colour and that holds visible text. */
function statusTextFaults(tree) {
  const f = [];
  for (const n of all(tree, () => true)) {
    const ink = styleProp(n.attrs.style, 'color') || (n.tag === 'text' ? n.attrs.fill : undefined);
    const cls = (n.attrs.class || '').split(/\s+/).filter((c) => STATUS_CLASS.test(c));
    if ((ink && STATUS.test(ink)) || cls.length) {
      const t = visible(n);
      if (t) f.push(`"${t.slice(0, 50)}" in ${ink || cls[0]}`);
    }
  }
  return f;
}
function orderFaults(tree) {
  const feed = byAttr(tree, 'data-header-feed');
  const tl = byAttr(tree, 'data-timeline-panel');
  if (feed.length !== 1 || tl.length !== 1) return [`${feed.length} [data-header-feed] and ${tl.length} [data-timeline-panel] (1 and 1 wanted)`];
  const f = [];
  if (within(tl[0], (n) => n === feed[0]) || within(feed[0], (n) => n === tl[0])) f.push('the news card and the timeline are nested');
  if (feed[0].at > tl[0].at) f.push('recent news renders below the timeline');
  return f;
}
/** The description is inside a closed <details> whose own <summary> carries words and no code. */
function descriptionFaults(tree) {
  const d = byAttr(tree, 'data-header-description');
  if (d.length !== 1) return [`${d.length} [data-header-description] (1 wanted)`];
  const det = closedDetailsAround(d[0]);
  if (!det) return ['the company description is at rest (no closed <details> around it)'];
  const sum = (det.children || []).find((c) => c.tag === 'summary');
  const words = sum ? visible(sum) : '';
  if (!/[A-Za-z]{3,}/.test(words)) return [`the <details> around the description has no <summary> in words ("${words}")`];
  if (CODE.test(words)) return [`CODE in the description's <summary>: "${words.match(CODE)[0]}"`];
  return [];
}
const WORDS = /day\(s\) rendered|\bno gap\b|rendered count|most-discussed|\bsocial\s*:|no source measured|not measured|press one to open/i;

const arms = [];
const sBA = renderOverlay(BA, DAYS_BA);
const s1 = pressDay(sBA, '2026-09-08');
const sHK = renderOverlay(HK, DAYS_HK);
const sHKopen = pressDay(sHK, '2026-08-13');
// ---- arm 1: the dialog ---------------------------------------------------------------------------------------------------
{
  const f = [];
  if (/^RENDER FAILED/.test(sBA.html)) f.push(sBA.html.slice(0, 120));
  const restRows = byAttr(sBA.tree, 'data-timeline-article').length;
  if (restRows) f.push(`at rest: ${restRows} article row(s) drawn`);
  if (byAttr(sBA.tree, 'data-hero-graphic').length) f.push('at rest: a HeroDialog is open');
  f.push(...dialogFaults(s1, FX.dayBA0908).map((x) => `BA bar 2026-09-08: ${x}`));
  f.push(...dialogFaults(pressMarker(sBA, 'coverage_event', '2026-09-08'), FX.dayBA0908).map((x) => `BA event marker 2026-09-08: ${x}`));
  f.push(...dialogFaults(sHKopen, FX.dayHK0813).map((x) => `992 HK bar 2026-08-13: ${x}`));
  arms.push(['DIALOG: a pressed bar or event marker opens that day in the HeroDialog, never inline', f.length === 0, f.length === 0 ? '3 of 3 presses' : f.slice(0, 6).join(' | ')]);
}
// ---- arm 2: the rows and the ink -----------------------------------------------------------------------------------------
{
  const f = [];
  if (!s1) f.push('BA 2026-09-08 could not be opened (arm 1)');
  else {
    for (const a of FX.dayBA0908.articles) {
      const k = a.article_key.slice(0, 18);
      f.push(...restFaults(s1.tree, a, clockOf(a.published_utc)).map((x) => `${k}: ${x}`));
      f.push(...detailFaults(s1, a).map((x) => `${k}: ${x}`));
    }
  }
  for (const [name, s] of [['BA at rest', sBA], ['992 HK at rest', sHK], ['BA 2026-09-08 open', s1], ['992 HK 2026-08-13 open', sHKopen]]) {
    if (s) f.push(...statusTextFaults(s.tree).slice(0, 2).map((x) => `${name}: status-coloured text ${x}`));
  }
  arms.push(['ROWS AND INK: headline, publisher and time at rest; mention count, flags and tier only on demand; no status-coloured text', f.length === 0, f.length === 0 ? `${FX.dayBA0908.articles.length} of ${FX.dayBA0908.articles.length} rows; 4 renders free of status ink` : f.slice(0, 6).join(' | ')]);
}
// ---- arm 3: the header brief and the words -------------------------------------------------------------------------------
{
  const f = [];
  const hb = renderHeader(BA);
  if (/^RENDER FAILED/.test(hb.html)) f.push(`HeaderBrief: ${hb.html.slice(0, 100)}`);
  const own = byAttr(hb.tree, 'data-timeline-panel').length + byAttr(hb.tree, 'data-rc').length;
  if (own) f.push('HeaderBrief mounts a timeline of its own (the overlay mounts the one TimelinePanel)');
  const hp = renderHeader(BA, { postureLine: h('span', { 'data-planted-posture': '' }, 'Planted posture line') });
  if (byAttr(hp.tree, 'data-planted-posture').length || /Planted posture line/.test(visible(hp.tree))) f.push('HeaderBrief renders the postureLine prop (no posture slot wanted)');
  const feeds = byAttr(hb.tree, 'data-header-feed').length;
  if (feeds !== 1) f.push(`HeaderBrief: ${feeds} [data-header-feed] (the one recent-news card wanted)`);
  f.push(...descriptionFaults(hb.tree).map((x) => `HeaderBrief: ${x}`));
  f.push(...orderFaults(sBA.tree).map((x) => `overlay BA: ${x}`));
  for (const [name, s] of [['BA', sBA], ['992 HK', sHK]]) {
    const m = visible(s.tree).match(WORDS);
    if (m) f.push(`${name} at rest: "${m[0]}"`);
  }
  arms.push(['HEADER BRIEF AND WORDS: no own timeline, no posture slot, description behind a closed summary, news card above the one timeline, no system line', f.length === 0, f.length === 0 ? 'HeaderBrief alone, with a planted postureLine, and in the overlay (BA, 992 HK)' : f.slice(0, 6).join(' | ')]);
}
// ---- arm 4: planted controls ---------------------------------------------------------------------------------------------
{
  const f = [];
  const a = FX.dayBA0908.articles[0];
  const head = a.headline;
  const good = parse(`<li data-timeline-article="${a.article_key}"><span>${head}</span> <span>Barron&#x27;s</span> <span>September 8th, 2026, 10:06a ET</span><details><summary>More</summary><div data-article-detail="${a.article_key}">Named 15 times; in the headline: yes; in the lead: yes; Tier A</div></details></li>`);
  const gf = restFaults(good, a, '10:06a').concat(detailFaults({ tree: good, captured: [] }, a));
  if (gf.length) f.push(`row: a clean row rejected (${gf[0]})`);
  const meta = parse(`<li data-timeline-article="${a.article_key}"><div>${head}</div><span>A</span> <span>Barron&#x27;s</span> <span>named 15 times</span> <span>10:06a ET</span> <span>in headline: yes</span></li>`);
  if (!restFaults(meta, a, '10:06a').length) f.push('row: metadata at rest accepted');
  const nopub = parse(`<li data-timeline-article="${a.article_key}"><span>${head}</span> <span>10:06a ET</span></li>`);
  if (!restFaults(nopub, a, '10:06a').length) f.push('row: a row with no publisher accepted');
  const openDet = parse(`<li data-timeline-article="${a.article_key}"><span>${head}</span><div data-article-detail="${a.article_key}">Named 15 times; in the headline; in the lead; Tier A</div></li>`);
  if (!detailFaults({ tree: openDet, captured: [] }, a).length) f.push('row: a detail drawn open at rest accepted');
  if (!statusTextFaults(parse('<div style="color:hsl(var(--status-danger))">Not searched on this day</div>')).length) f.push('ink: red status text accepted');
  if (statusTextFaults(parse('<p><span class="text-[hsl(var(--status-danger))]"><svg></svg></span><span style="color:hsl(var(--palette-navy))">Not searched on this day</span></p>')).length) f.push('ink: navy text beside a red icon rejected');
  if (!orderFaults(parse('<div><div data-timeline-panel="SERVED"></div><div data-header-feed="SERVED"></div></div>')).length) f.push('order: news below the timeline accepted');
  if (!orderFaults(parse('<div><div data-header-feed="SERVED"></div><div data-timeline-panel="SERVED"></div><div data-timeline-panel="SERVED"></div></div>')).length) f.push('order: two timelines accepted');
  if (orderFaults(parse('<div><div data-header-feed="SERVED"></div><div data-timeline-panel="SERVED"></div></div>')).length) f.push('order: news above the one timeline rejected');
  if (!descriptionFaults(parse('<div><p data-header-description="SERVED">The Boeing Company operates as an aerospace company.</p></div>')).length) f.push('description: at rest accepted');
  if (descriptionFaults(parse('<details><summary>About the company</summary><p data-header-description="SERVED">The Boeing Company.</p></details>')).length) f.push('description: closed details with a summary rejected');
  arms.push(['PLANTED (control): row, status-text, order and description predicates reject bad markup and accept good markup', f.length === 0, f.length === 0 ? '7 of 7 rejected, 4 of 4 accepted' : f.join(' | ')]);
}

let pass = 0;
for (const [n, ok, d] of arms) {
  if (ok) pass += 1;
  console.log(`${ok ? 'ARM PASS' : 'ARM FAIL'} ${n} :: ${d}`);
}
console.log(`THE DAY OPENS IN THE HERO DIALOG AND THE HEADER BRIEF IS THE NEWS CARD ABOVE THE ONE TIMELINE: ${pass} of 4 arms`);
process.exit(pass === 4 ? 0 : 1);
