/**
 * presets.cjs -- DSGN_AMGTV1 round 31, AV-zi-1 (issuer 2.0.0_SA_COO~D): A PM PICKS THE LAST 30, 90 OR 365 DAYS AND READS WHICH
 * WINDOW IS SHOWN (PRD FWD-26; FWD-21 / FWD-22 read through the window; SAUX-21, SAUX-27, SAUX-28).
 *
 * Usage (from the directory whose portal/ is the checkout under test, e.g. C:/tmp/wk-dsgn-amgtv1-88): node <this file>
 * Why: FWD-26 DONE WHEN -- "Chatter and Price each offer 30D / 90D / 365D presets in the shared Segmented control (the in-pattern
 *   IndexPerformanceModal labels), default 30D, replacing 'Earlier month' / 'Later month'; each face's caption names its window
 *   ending at the served as-of date; where the store is shorter than the window, the face states the served window start ('since
 *   <date>') and never extrapolates. v0.11: Price's 90D/365D render the served 'not produced yet' reason as a designed empty state".
 *   The routes serve every window on the deployed opal-amgt-scoped-api (code KQSA62c3): chatter ?days=30|90|365 with window_days,
 *   window_start, window_end (and window_note on 365); trending/price ?days=30 94 rows, ?days=90|365 0 rows with window_reason.
 * Render: ./_presets.cjs -- the REAL LeadPanel, hooks, ChatterBubbles and PriceBars over a react-query recorder and an endpoint
 *   recorder that serves windows.<route>.<days>.json by the `days` the call carries; the preset is selected through the control's
 *   own onChange and the tree re-rendered with the state it wrote.
 * Inputs: round31/fixtures/windows.{chatter,price}.{30,90,365}.json.
 * Arms:
 *   1  PRESETS: on Chatter and on Price there is exactly ONE Segmented whose options are 30D, 90D and 365D (or 1Y), in that order,
 *      30D active at rest; selecting 90D and 365D through its onChange makes that option active; at every window neither face
 *      prints "Earlier month", "Later month", "partial month" or "per month", and no [data-chatter-cursor] is drawn.
 *   2  CHATTER WINDOW: at 30, 90 and 365 days the collected-chatter read carries that window (getCollectedChatter(days)); the
 *      bubbles drawn ([data-bubble]) are exactly the served rows with articles_total > 0 (0 missing, 0 extra, 0 duplicate); Boeing's
 *      bubble names its served window count ("<n> article(s) collected", n = 71 / 143 / the 365 total); the face names "<N> days"
 *      and the served window_end in words, and at 365 "since <served window_start in words>" (the store begins after the start).
 *   3  PRICE WINDOW: at 30 days the price read carries days 30 (getLeadPanelRankings(movement, 'PRICE', limit, 30)), bars are drawn
 *      and the [data-price-window] caption names "30 days"; at 90 and 365 the read carries that window, NO bar is drawn, the face
 *      prints the served window_reason in words, and neither "30 days" nor "No price moves ranked yet" appears on the face.
 *   4  PLANTED: the preset predicate rejects 2 options, a 7D label, 90D active at rest and a face printing "Earlier month"; the
 *      chatter predicate rejects a missing bubble, the 30-day count under 90 days and a 365 caption with no "since"; the price
 *      predicate rejects 30-day bars under 90 days, a 90-day face naming "30 days" and one with no served reason; each accepts its
 *      good shape; the click replay flips a toy useState('30D') control to 90D and reports a control whose onChange writes nothing.
 * Blind spots: a static render does not lay out, so a clipped label or a caption off-screen is the close walk's to see; a preset
 *   held in state that a click replay cannot reach (a ref, an effect, the URL) reads as "wrote no state".
 * Prints one line per arm and "ROLLING WINDOWS, NAMED: <k> of 4 arms"; exit 0 only at 4 of 4.
 */
const path = require('path');

const P = require('./_presets.cjs');
const { L, SA, CHATTER, PRICE, textOf, attrAll, presetControls, optionDays, daysOf } = P;
const first = (e) => String(e && e.message ? e.message : e).split('\n')[0];
let longDate = (s) => String(s);
try { longDate = L.source(SA + 'dateWords.ts').longDate; } catch (e) { /* reported by arm 2 */ }
const esc = (s) => String(s).replace(/[.*+?^${}()|[\]\\]/g, '\\$&');

// ---------------- predicates (pure) ----------------
const FORBIDDEN = [/Earlier month/i, /Later month/i, /partial month/i, /\bper month\b/i];
/** The preset control on one render: one control, 30 / 90 / 365 in order, `want` active; no month cursor words. */
function presetFaults(segs, html, want) {
  const f = [];
  const ctls = presetControls(segs);
  if (ctls.length !== 1) f.push(`${ctls.length} window preset control(s) (want 1)`);
  const c = ctls[0];
  if (c) {
    const days = c.options.map(optionDays);
    if (days.join(',') !== '30,90,365') f.push(`options name ${c.options.map((o) => o.label).join('/')} (want 30D / 90D / 365D or 1Y)`);
    const act = c.options.find((o) => String(o.value) === String(c.value));
    if (!act || optionDays(act) !== want) f.push(`active option ${act ? act.label : c.value} (want the ${want}-day option)`);
  }
  const t = textOf(html);
  for (const re of FORBIDDEN) if (re.test(t)) f.push(`prints "${t.match(re)[0]}"`);
  if (/\sdata-chatter-cursor=/.test(html)) f.push('draws [data-chatter-cursor]');
  return f;
}
/** The text of one bubble's markup: from its data-bubble attribute to the next bubble. */
function bubbleText(html, key) {
  const at = html.indexOf(`data-bubble="${key}"`);
  if (at < 0) return null;
  const next = html.indexOf(' data-bubble="', at + 12);
  return textOf('<x ' + html.slice(at, next < 0 ? html.length : next));
}
/** The Chatter face at one window: the read, the bubble set, one named count, the caption. */
function chatterFaults(html, calls, w) {
  const f = [];
  const reads = calls.filter((c) => c.fn === 'getCollectedChatter');
  if (reads.length === 0) f.push('no collected-chatter read');
  for (const r of reads) if (daysOf(r.args[0]) !== w.days) f.push(`collected-chatter read asks days ${daysOf(r.args[0])} (want ${w.days})`);
  const drawn = attrAll(html, 'data-bubble');
  const set = new Set(drawn);
  const missing = [...w.keys].filter((k) => !set.has(k));
  const extra = [...set].filter((k) => !w.keys.has(k));
  if (missing.length) f.push(`${missing.length} served name(s) with articles in the window draw no bubble (${missing.slice(0, 3).join(', ')})`);
  if (extra.length) f.push(`${extra.length} bubble(s) for a name with no article in the window (${extra.slice(0, 3).join(', ')})`);
  if (drawn.length !== set.size) f.push(`${drawn.length - set.size} duplicate bubble(s)`);
  if (w.named) {
    const bt = bubbleText(html, w.named.key);
    if (bt === null) f.push(`no bubble for ${w.named.key}`);
    else if (!new RegExp(`\\b${w.named.n} articles? collected\\b`, 'i').test(bt)) f.push(`${w.named.key}'s bubble does not name its ${w.days}-day count "${w.named.n} articles collected" ("${bt.slice(0, 70)}")`);
  }
  const t = textOf(html);
  if (!new RegExp(`\\b${w.days} days\\b`).test(t)) f.push(`the face does not name "${w.days} days"`);
  if (w.end && !t.includes(w.end)) f.push(`the face does not name the served window end "${w.end}"`);
  if (w.since && !new RegExp(`since ${esc(w.since)}`, 'i').test(t)) f.push(`the face does not state "since ${w.since}"`);
  return f;
}
/** The Price face at one window. */
function priceFaults(html, calls, w) {
  const f = [];
  const reads = calls.filter((c) => c.fn === 'getLeadPanelRankings' && String(c.args[1]).toUpperCase() === 'PRICE');
  if (reads.length === 0) f.push('no price ranking read');
  for (const r of reads) if (daysOf(r.args[3]) !== w.days) f.push(`price read asks days ${daysOf(r.args[3])} (want ${w.days})`);
  const bars = attrAll(html, 'data-price-bar').length;
  const t = textOf(html);
  if (w.rows > 0) {
    if (bars === 0) f.push('no bar drawn on a served window');
    const cap = /<p[^>]*\sdata-price-window="[^"]*"[^>]*>([\s\S]*?)<\/p>/.exec(html);
    if (!cap || !new RegExp(`\\b${w.days} days\\b`).test(textOf(cap[1]))) f.push(`the [data-price-window] caption does not name "${w.days} days"`);
  } else {
    if (bars > 0) f.push(`${bars} bar(s) drawn for a window the route does not serve`);
    if (!w.reason || !t.includes(w.reason)) f.push('the served window_reason is not printed');
    if (/\b30 days\b/.test(t)) f.push('names "30 days" on a 90/365 face');
    if (/No price moves ranked yet/i.test(t)) f.push('prints "No price moves ranked yet"');
  }
  return f;
}

// ---------------- the served expectations ----------------
const BA = 'BA_US_Equity';
function chatterWant(days) {
  const p = CHATTER[days];
  const keys = new Set(p.rows.filter((r) => typeof r.articles_total === 'number' && r.articles_total > 0).map((r) => r.security_key));
  const ba = p.rows.find((r) => r.security_key === BA);
  const since = p.window_start && p.window_start_requested && p.window_start !== p.window_start_requested ? longDate(p.window_start) : null;
  return { days, keys, named: ba ? { key: BA, n: ba.articles_total } : null, end: longDate(p.window_end), since };
}
function priceWant(days) {
  const p = PRICE[days];
  return { days, rows: (p.rows || []).length, reason: p.window_reason || p.ranking_reason || null };
}

const arms = [];
const at = {};
const stops = [];
for (const subject of ['CHATTER', 'PRICE']) for (const d of P.WINDOWS) {
  try {
    const r = P.renderAt(subject, d);
    if (r.stop) stops.push(`${subject} ${d}: ${r.stop}`);
    at[`${subject}:${d}`] = r.at;
    if (d === 30) at[`${subject}:rest`] = r.rest;
  } catch (e) { stops.push(`${subject} ${d}: RENDER ${first(e)}`); }
}

// Arm 1 -- presets.
{
  const f = [...stops];
  for (const subject of ['CHATTER', 'PRICE']) for (const d of P.WINDOWS) {
    const r = at[`${subject}:${d}`];
    if (r) f.push(...presetFaults(r.segs, r.html, d).map((x) => `${subject.toLowerCase()} ${d}: ${x}`));
  }
  arms.push(['PRESETS: one 30D / 90D / 365D control on each face, 30D at rest, each preset selectable; no month cursor words', f.length === 0,
    f.length ? [...new Set(f)].slice(0, 6).join(' | ') : 'Chatter and Price: 30D at rest, 90D and 365D selected through onChange']);
}
// Arm 2 -- chatter window.
{
  const f = [];
  const tally = [];
  for (const d of P.WINDOWS) {
    const r = at[`CHATTER:${d}`];
    const w = chatterWant(d);
    if (!r) { f.push(`${d}: not reached`); continue; }
    f.push(...chatterFaults(r.html, r.calls, w).map((x) => `${d}: ${x}`));
    tally.push(`${d}d ${w.keys.size} bubbles, Boeing ${w.named ? w.named.n : '-'}`);
  }
  arms.push(['CHATTER WINDOW: the read carries the window; one bubble per name with articles in it; the count and the window are named', f.length === 0,
    f.length ? f.slice(0, 6).join(' | ') : tally.join('; ') + '; 365 states "since"']);
}
// Arm 3 -- price window.
{
  const f = [];
  const tally = [];
  for (const d of P.WINDOWS) {
    const r = at[`PRICE:${d}`];
    const w = priceWant(d);
    if (!r) { f.push(`${d}: not reached`); continue; }
    f.push(...priceFaults(r.html, r.calls, w).map((x) => `${d}: ${x}`));
    tally.push(`${d}d ${w.rows ? attrAll(r.html, 'data-price-bar').length + ' bars' : 'reason printed, 0 bars'}`);
  }
  arms.push(['PRICE WINDOW: 30 days draws the served bars; 90 and 365 print the served reason, no bar, no 30-day words', f.length === 0,
    f.length ? f.slice(0, 6).join(' | ') : tally.join('; ')]);
}
// Arm 4 -- planted.
{
  const f = [];
  const opt = (l, v) => ({ label: l, value: v });
  const good3 = [opt('30D', 'd30'), opt('90D', 'd90'), opt('365D', 'd365')];
  const cap30 = '<p>Articles collected over the last 30 days to October 2nd, 2026</p>';
  if (presetFaults([{ options: good3, value: 'd30' }], cap30, 30).length) f.push('good presets rejected: ' + presetFaults([{ options: good3, value: 'd30' }], cap30, 30)[0]);
  if (presetFaults([{ options: [opt('30D', 'a'), opt('1Y', 'b'), opt('90D', 'c')], value: 'a' }], cap30, 30).length === 0) f.push('"30D / 1Y / 90D order" accepted');
  for (const [n, segs, html] of [
    ['2 options', [{ options: good3.slice(0, 2), value: 'd30' }], cap30],
    ['a 7D label', [{ options: [opt('7D', 'd7'), opt('30D', 'd30'), opt('90D', 'd90')], value: 'd30' }], cap30],
    ['90D active at rest', [{ options: good3, value: 'd90' }], cap30],
    ['"Earlier month"', [{ options: good3, value: 'd30' }], cap30 + '<button>Earlier month</button>'],
  ]) if (presetFaults(segs, html, 30).length === 0) f.push(`presets: ${n} accepted`);

  const bub = (k, n) => `<g data-bubble="${k}"><title>Name ${k}; ${n} articles collected in the last 90 days</title><circle r="3"></circle></g>`;
  const w90 = { days: 90, keys: new Set(['A', 'B', BA]), named: { key: BA, n: 143 }, end: 'October 2nd, 2026', since: null };
  const read90 = [{ fn: 'getCollectedChatter', args: [90] }];
  const chatGood = `<div><p>Articles collected over the last 90 days to October 2nd, 2026</p>${bub('A', 4)}${bub(BA, 143)}${bub('B', 2)}</div>`;
  if (chatterFaults(chatGood, read90, w90).length) f.push('good chatter rejected: ' + chatterFaults(chatGood, read90, w90)[0]);
  for (const [n, html, calls, w] of [
    ['a missing bubble', chatGood.replace(bub('B', 2), ''), read90, w90],
    ['the 30-day count under 90 days', chatGood.replace(bub(BA, 143), bub(BA, 71)), read90, w90],
    ['a read asking days 30', chatGood, [{ fn: 'getCollectedChatter', args: [30] }], w90],
    ['a 365 caption with no "since"', chatGood.replace(/90 days/g, '365 days'), [{ fn: 'getCollectedChatter', args: [365] }],
      { ...w90, days: 365, named: null, since: 'January 1st, 2026' }],
  ]) if (chatterFaults(html, calls, w).length === 0) f.push(`chatter: ${n} accepted`);

  const reason = "the 90- and 365-day price windows are not produced yet: they need a longer price-history pull, which waits on Andrew's word";
  const p90 = { days: 90, rows: 0, reason };
  const pread90 = [{ fn: 'getLeadPanelRankings', args: ['TRENDING', 'PRICE', 500, 90] }];
  const priceGood = `<div><p data-price-empty="">${reason.replace(/'/g, '&#x27;')}</p></div>`;
  if (priceFaults(priceGood, pread90, p90).length) f.push('good price 90 rejected: ' + priceFaults(priceGood, pread90, p90)[0]);
  const bars30 = '<p data-price-window="">Change over the last 30 days to October 1st, 2026</p><div data-price-bar="AMD_US_Equity">AMD +34.0%</div>';
  if (priceFaults(bars30, [{ fn: 'getLeadPanelRankings', args: ['TRENDING', 'PRICE', 500, 30] }], { days: 30, rows: 94, reason: null }).length) f.push('good price 30 rejected');
  for (const [n, html] of [
    ['30-day bars under 90 days', bars30],
    ['a 90-day face naming "30 days"', priceGood + '<p>Change over the last 30 days</p>'],
    ['no served reason', '<div><p>No price moves ranked yet.</p></div>'],
  ]) if (priceFaults(html, pread90, p90).length === 0) f.push(`price: ${n} accepted`);

  // The click replay on a toy control.
  const R = P.React;
  const Toy = () => {
    const [v, setV] = R.useState('d30');
    return P.ce('div', null, P.ce(P.Segmented, { ariaLabel: 'Window', options: good3, value: v, onChange: setV }), P.ce('span', { 'data-shown': v }));
  };
  const Dead = () => P.ce(P.Segmented, { ariaLabel: 'Window', options: good3, value: 'd30', onChange: () => {} });
  try {
    const t = P.clickTo(() => L.render(Toy), 90);
    if (t.stop || !t.at || !/data-shown="d90"/.test(t.at.html)) f.push(`replay: the toy did not flip to 90D (${t.stop || 'shown ' + (/data-shown="([^"]*)"/.exec(t.at.html) || [])[1]})`);
    const dd = P.clickTo(() => L.render(Dead), 90);
    if (!dd.stop || !/wrote no state/.test(dd.stop)) f.push('replay: a dead control was not reported');
  } catch (e) { f.push('replay: ' + first(e)); }
  arms.push(['PLANTED: each predicate rejects its planted faults and accepts its good shape; the click replay flips a toy control', f.length === 0,
    f.length ? f.join(' | ') : '4 + 4 + 3 rejected, 4 good accepted; toy 30D -> 90D, dead control reported']);
}

let pass = 0;
for (const [n, ok, d] of arms) { if (ok) pass += 1; console.log(`${ok ? 'ARM PASS' : 'ARM FAIL'} ${n} :: ${d}`); }
console.log(`ROLLING WINDOWS, NAMED: ${pass} of 4 arms`);
process.exit(pass === 4 ? 0 : 1);
