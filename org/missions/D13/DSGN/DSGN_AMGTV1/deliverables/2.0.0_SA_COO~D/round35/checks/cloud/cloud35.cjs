/**
 * cloud35.cjs -- DSGN_AMGTV1 round 35, check (issuer 2.0.0_SA_COO~D): THE WORD CLOUD RENDERS THE SERVED TERMS, SIZED BY THE SERVED
 * COUNT; AN EMPTY SERVED LIST RENDERS ITS SERVED REASON; THE PAGE COUNTS NOTHING (PRD FWD-5 v0.14).
 *
 * Usage (from the directory whose portal/ is the checkout under test -- the repository root for a worker,
 *   `cd "$(git rev-parse --show-toplevel)"`; C:/tmp/wk-dsgn-amgtv1-92 for the issuer): node <this file>
 *   ISSUER GREEN ARM: CHECK_SRC_OVERRIDE (round15/checks/_load.cjs) is honoured for every source read here, and for a NEW source
 *   file: the loader resolves an import against the override keys before the disk, so a new
 *   src/pages/SecurityAnalysis/components/TimelineWordCloud.tsx loads through
 *   CHECK_SRC_OVERRIDE="src/pages/SecurityAnalysis/components/TimelinePanel.tsx=<abs file>;src/pages/SecurityAnalysis/components/TimelineWordCloud.tsx=<abs file>".
 *   The KEEP children inherit the same environment.
 * Why: PRD FWD-5 v0.14: "The word cloud renders the terms AMGT_RESAPP FWD-39 serves (`word_cloud` on the timeline payload), sized by
 *   the served count; an empty served list renders its served reason. The page counts nothing." The served range route
 *   /api/scoped/amgt/security/<key>/timeline carries `word_cloud: {terms: [{term, count}], window: {from, to} | null, reason: string
 *   | null}`; count = the number of headlines carrying the term; terms ordered count desc then term asc, at most 40; reason is null
 *   only when terms is non-empty (lib/research/api/scoped_amgt.py _word_cloud_block). At base 055ba370 components/TimelinePanel.tsx
 *   renders the range read and ignores word_cloud.
 * Render: the REAL components/TimelinePanel.tsx (export `TimelinePanel`, prop `securityKey`) through round29/checks/timeline/_tl.cjs
 *   (its recharts recorder, query stub answering the range route with the fixture, DataTooltip and HeroDialog stubs) over
 *   round15/checks/_load.cjs. A word-cloud component the fix adds must live under src/pages/SecurityAnalysis/ (the loader STUBS
 *   src/components/** and src/ui/**: a cloud placed there renders as a stub and reads as no cloud).
 * THE DOM CONTRACT (graded exactly):
 *   - ONE container element carrying `data-word-cloud` whose value is "terms" (served list non-empty), "empty" (served list empty:
 *     the served reason prints verbatim inside it) or "absent" (the range payload has no word_cloud key: a designed sentence
 *     prints, no crash), rendered by TimelinePanel when the range read resolves.
 *   - Each served term is ONE element carrying data-term="<served term>" and data-count="<served count>", in served order, inside
 *     the container, with a hover name (a title attribute, or a <title> child) containing the term and its count, and an inline
 *     font-size in px (style font-size:Npx, or an SVG font-size="N[px]" attribute) on that element.
 *   - The container prints the served window in words (dateWords.longDate of window.from and of window.to) when window is non-null.
 * Inputs: SERVED round35/fixtures/timeline.{BA_US,VLO_US,AMD_US}_Equity.json ({_capture_note, payload}; captured read-only on the
 *   deployed scoped API FcVBPafw; each serves 40 terms, window 2026-01-01..2026-10-03). PLANTED in memory (labelled): BA with
 *   terms [] + window null + the inverted-window reason; BA with terms [] + the served window + "no coverage headlines in this
 *   window"; BA with terms [] + the served window + "no terms remain in this window after removing common words and the company's
 *   own name"; BA with the word_cloud key deleted.
 * Arms:
 *   1  EVERY SERVED TERM ONCE: on BA, VLO and AMD the [data-term] list inside the one data-word-cloud="terms" container equals the
 *      served terms (same terms, same order, 40 of 40), each data-count equals the served count (the page counts nothing), each
 *      carries a hover name with the term and its count, and no [data-term] renders outside the container. Prints "k of n" per name.
 *   2  SIZED BY THE SERVED COUNT: each term's inline font-size is in px; sizes are non-increasing along served order; the max-count
 *      term is strictly larger than the min-count term when their counts differ; no size is below 11px; every term declares the
 *      same colour (no per-term colour) and none is a status colour. Prints the size range per name.
 *   3  THE EMPTY AND ABSENT STATES: each planted empty payload renders data-word-cloud="empty", 0 [data-term] and its served
 *      reason verbatim (and, where the window is served, the window in words; where it is null, no "undefined"/"null"/"NaN"/
 *      "Invalid Date"); the deleted key renders data-word-cloud="absent", 0 [data-term] and a sentence in words (no code-shaped
 *      word); BA prints longDate(window.from) and longDate(window.to) inside its container, derived through the page's own
 *      dateWords.ts.
 *   4  KEEP: round29 timeline/chart.cjs and round34 repairs/repairs34.cjs exit 0 on the same tree.
 *   5  PLANTED: on a synthetic render of BA's served terms, arm 1's grader flags one term dropped and a data-count off by one;
 *      arm 2's grader flags a size increase and a status colour; arm 3's grader flags an empty state missing its reason; each for
 *      its own reason; the good synthetic renders (terms, empty, absent) are accepted.
 * Blind spots: a static render: no layout, so overlap, clipping and the cloud's measured footprint are not graded; a hover name in a
 *   <title> outside an <svg> may be hoisted by React 19's static renderer and then reads as missing (use a title attribute there);
 *   colour is compared as declared (inline color/fill, class text-[..]/fill-[..]/text-<named>-<n>): two different declarations of
 *   one hue read as two colours, and an inherited colour reads as "inherited" for every term.
 * Prints one line per arm and "THE WORD CLOUD RENDERS THE SERVED TERMS SIZED BY THE SERVED COUNT: <k> of 5 arms"; exit 0 only at
 * 5 of 5. Static renders only; no network, no AWS, writes no file.
 */
const fs = require('fs');
const path = require('path');
const { spawnSync } = require('child_process');

const DROOT = path.join(__dirname, '..', '..', '..');
const T = require(path.join(DROOT, 'round29', 'checks', 'timeline', '_tl.cjs'));
const { parse, all, byAttr, visible, norm, clone, CODE, STATUS, within } = T;
const readJson = (p) => JSON.parse(fs.readFileSync(path.join(DROOT, p), 'utf8'));
const pay = (x) => (x && x.payload && (x._capture_note || x._capture) ? x.payload : x);
const longDate = T.dateWords && typeof T.dateWords.longDate === 'function' ? T.dateWords.longDate : null;

function keepsPassing(rels) {
  const faults = [];
  for (const rel of rels) {
    const r = spawnSync(process.execPath, [path.join(DROOT, rel)], { cwd: process.cwd(), encoding: 'utf8', timeout: 300000 });
    const last = ((r.stdout || '') + (r.stderr || '')).trim().split('\n').pop() || '';
    if (r.status !== 0) faults.push(`KEEP: ${rel} rc=${r.status} ("${last.slice(0, 100)}")`);
  }
  return faults;
}

// ==== inputs ===================================================================================================================
const SERVED = {};
for (const k of ['BA_US_Equity', 'VLO_US_Equity', 'AMD_US_Equity']) SERVED[k] = pay(readJson(`round35/fixtures/timeline.${k}.json`));
const BA = SERVED.BA_US_Equity;
const REASON_INVERTED = 'the requested window ends before the first day of the store (2026-01-01): no headlines to count';
const REASON_NO_HEADLINES = 'no coverage headlines in this window';
const REASON_NO_TERMS = "no terms remain in this window after removing common words and the company's own name";
const withCloud = (range, wc) => { const x = clone(range); if (wc === undefined) delete x.word_cloud; else x.word_cloud = wc; return x; };
// PLANTED (labelled): the producer's three empty shapes and the absent key, grafted onto BA's served range.
const PLANTS = [
  ['BA PLANTED inverted window', withCloud(BA, { terms: [], window: null, reason: REASON_INVERTED }), 'empty'],
  ['BA PLANTED no coverage headlines', withCloud(BA, { terms: [], window: clone(BA.word_cloud.window), reason: REASON_NO_HEADLINES }), 'empty'],
  ['BA PLANTED no terms remain', withCloud(BA, { terms: [], window: clone(BA.word_cloud.window), reason: REASON_NO_TERMS }), 'empty'],
  ['BA PLANTED word_cloud key deleted', withCloud(BA, undefined), 'absent'],
];

// ==== reading the cloud ========================================================================================================
const containersOf = (tree) => byAttr(tree, 'data-word-cloud');
const termsOf = (tree) => byAttr(tree, 'data-term');
/** The hover name of one term element: its title attribute and the text of any <title> inside it. */
function hoverOf(n) {
  const parts = [];
  if (n.attrs.title) parts.push(n.attrs.title);
  for (const t of all(n, (x) => x.tag === 'title')) parts.push(visible({ children: t.children }));
  return norm(parts.join(' '));
}
const numberIn = (s, v) => new RegExp(`(^|[^\\d.])${v}([^\\d.]|$)`).test(s);
/** The element's own inline font size in px, or null. */
function fontPx(n) {
  const sm = /(?:^|;)\s*font-size\s*:\s*([\d.]+)px\s*(?:;|$)/i.exec(n.attrs.style || '');
  if (sm) return Number(sm[1]);
  const a = /^([\d.]+)(px)?$/.exec(String(n.attrs['font-size'] || '').trim());
  return a ? Number(a[1]) : null;
}
/** Every colour the term element (and its descendants) declares, as one signature string. */
function colourOf(n) {
  const out = [];
  for (const x of [n, ...all(n, () => true)]) {
    const st = x.attrs.style || '';
    for (const prop of ['color', 'fill']) {
      const m = new RegExp(`(?:^|;)\\s*${prop}\\s*:\\s*([^;]+)`, 'i').exec(st);
      if (m) out.push(m[1].trim());
    }
    if (x.attrs.fill !== undefined && x.attrs.fill !== 'none') out.push(x.attrs.fill);
    for (const t of String(x.attrs.class || '').split(/\s+/)) {
      if (/^(text|fill)-\[(?!\d)[^\]]+\]$/.test(t) && !/^text-\[\d/.test(t)) out.push(t);
      else if (/^(text|fill)-(red|orange|amber|yellow|green|emerald|rose|lime|teal|cyan|sky|blue|indigo|violet|purple|fuchsia|pink|slate|gray|zinc|neutral|stone)-\d+$/.test(t)) out.push(t);
    }
  }
  return out.length ? [...new Set(out.map((c) => c.toLowerCase().replace(/\s+/g, '')))].sort().join(' + ') : 'inherited';
}

// ==== arm 1 grader: every served term once, its served count, its hover name ==================================================
function termListFaults(name, tree, wc) {
  const f = [];
  const served = (wc && wc.terms) || [];
  const cs = containersOf(tree);
  if (cs.length !== 1) return { faults: [`${name}: ${cs.length} [data-word-cloud] container(s) (1 wanted)`], k: 0, n: served.length };
  const c = cs[0];
  if (c.attrs['data-word-cloud'] !== 'terms') f.push(`${name}: data-word-cloud="${c.attrs['data-word-cloud']}" ("terms" wanted: ${served.length} terms served)`);
  const els = termsOf(tree);
  const outside = els.filter((n) => !within(n, (x) => x === c));
  if (outside.length) f.push(`${name}: ${outside.length} [data-term] rendered outside the [data-word-cloud] container`);
  const inside = els.filter((n) => within(n, (x) => x === c));
  if (inside.length !== served.length) f.push(`${name}: ${inside.length} [data-term] rendered, ${served.length} served`);
  let k = 0;
  let orderNoted = false;
  for (let i = 0; i < served.length; i += 1) {
    const s = served[i];
    const n = inside[i];
    if (!n) continue;
    let ok = true;
    if (n.attrs['data-term'] !== s.term) {
      ok = false;
      if (!orderNoted) { f.push(`${name}: position ${i + 1} renders "${n.attrs['data-term']}", served "${s.term}" (same terms in served order wanted)`); orderNoted = true; }
    } else if (n.attrs['data-count'] !== String(s.count)) {
      ok = false;
      f.push(`${name}: "${s.term}" data-count="${n.attrs['data-count']}", served count ${s.count} (the page counts nothing)`);
    } else {
      const hv = hoverOf(n);
      if (!hv.toLowerCase().includes(String(s.term).toLowerCase()) || !numberIn(hv, s.count)) {
        ok = false;
        f.push(`${name}: "${s.term}" hover name "${hv.slice(0, 60)}" (the term and its count ${s.count} wanted)`);
      }
    }
    if (ok) k += 1;
  }
  const missing = served.filter((s) => !inside.some((n) => n.attrs['data-term'] === s.term));
  if (missing.length) f.push(`${name}: ${missing.length} served term(s) not rendered (first "${missing[0].term}")`);
  const seen = new Map();
  for (const n of inside) seen.set(n.attrs['data-term'], (seen.get(n.attrs['data-term']) || 0) + 1);
  const dup = [...seen].filter(([, v]) => v > 1);
  if (dup.length) f.push(`${name}: "${dup[0][0]}" rendered ${dup[0][1]} times (each served term once)`);
  return { faults: [...new Set(f)], k, n: served.length };
}

// ==== arm 2 grader: sized by the served count, one colour =====================================================================
const MIN_PX = 11;
function sizeFaults(name, tree, wc) {
  const f = [];
  const served = (wc && wc.terms) || [];
  const c = containersOf(tree)[0];
  const els = c ? termsOf(tree).filter((n) => within(n, (x) => x === c)) : [];
  if (!els.length) return { faults: [`${name}: no [data-term] rendered inside a [data-word-cloud] container (${served.length} served)`], range: '-' };
  const sizes = els.map(fontPx);
  const countOf = (n) => { const s = served.find((x) => x.term === n.attrs['data-term']); return s ? s.count : null; };
  const noSize = els.filter((n, i) => sizes[i] === null);
  if (noSize.length) f.push(`${name}: ${noSize.length} term(s) carry no inline font-size in px (first "${noSize[0].attrs['data-term']}")`);
  for (let i = 1; i < els.length; i += 1) {
    if (sizes[i] === null || sizes[i - 1] === null) continue;
    if (sizes[i] > sizes[i - 1] + 1e-9) { f.push(`${name}: "${els[i].attrs['data-term']}" (${sizes[i]}px) is larger than the term before it "${els[i - 1].attrs['data-term']}" (${sizes[i - 1]}px) (non-increasing along served order wanted)`); break; }
  }
  const counted = els.map((n, i) => ({ n, px: sizes[i], count: countOf(n) })).filter((x) => x.px !== null && x.count !== null);
  if (counted.length) {
    const maxC = Math.max(...counted.map((x) => x.count));
    const minC = Math.min(...counted.map((x) => x.count));
    const top = counted.find((x) => x.count === maxC);
    const low = counted.filter((x) => x.count === minC).pop();
    if (maxC !== minC && !(top.px > low.px)) f.push(`${name}: the max-count term "${top.n.attrs['data-term']}" (${maxC}, ${top.px}px) is not larger than the min-count term "${low.n.attrs['data-term']}" (${minC}, ${low.px}px)`);
  }
  const small = els.filter((n, i) => sizes[i] !== null && sizes[i] < MIN_PX);
  if (small.length) f.push(`${name}: ${small.length} term(s) below ${MIN_PX}px (first "${small[0].attrs['data-term']}" ${fontPx(small[0])}px)`);
  const colours = els.map(colourOf);
  const hues = [...new Set(colours)];
  if (hues.length > 1) f.push(`${name}: ${hues.length} colours across the terms (one wanted): ${hues.slice(0, 3).join(' | ')}`);
  const st = hues.filter((x) => STATUS.test(x));
  if (st.length) f.push(`${name}: a status colour on a term: ${st[0]}`);
  const px = sizes.filter((x) => x !== null);
  const range = px.length ? `${Math.min(...px)}-${Math.max(...px)}px, colour ${hues[0]}` : '-';
  return { faults: f, range };
}

// ==== arm 3 grader: the empty and absent states, and the window in words ======================================================
function windowFaults(name, c, wc) {
  const f = [];
  const t = visible(c);
  if (wc && wc.window) {
    if (!longDate) return [`${name}: the page's dateWords.longDate did not load`];
    for (const end of ['from', 'to']) {
      const w = longDate(wc.window[end]);
      if (!w || !t.includes(norm(w))) f.push(`${name}: the window ${end} "${w}" (longDate of ${wc.window[end]}) is not printed in the container`);
    }
  } else if (/\bundefined\b|\bnull\b|\bNaN\b|Invalid Date/.test(t)) f.push(`${name}: the container prints "${t.match(/\bundefined\b|\bnull\b|\bNaN\b|Invalid Date/)[0]}" (no window served)`);
  return f;
}
function stateFaults(name, html, wc, want) {
  if (/^RENDER FAILED/.test(html)) return [`${name}: ${html.slice(0, 120)}`];
  const f = [];
  const tree = parse(html);
  const cs = containersOf(tree);
  if (cs.length !== 1) return [`${name}: ${cs.length} [data-word-cloud] container(s) (1 wanted)`];
  const c = cs[0];
  if (c.attrs['data-word-cloud'] !== want) f.push(`${name}: data-word-cloud="${c.attrs['data-word-cloud']}" ("${want}" wanted)`);
  const n = termsOf(tree).length;
  if (want !== 'terms' && n) f.push(`${name}: ${n} [data-term] rendered (0 wanted)`);
  const t = visible(c);
  if (want === 'empty' && !t.includes(norm(wc.reason))) f.push(`${name}: the served reason "${wc.reason.slice(0, 60)}" is not printed verbatim in the container ("${t.slice(0, 80)}")`);
  if (want === 'absent') {
    if (t.split(' ').filter((w) => /[A-Za-z]/.test(w)).length < 4) f.push(`${name}: the absent container prints no sentence ("${t.slice(0, 60)}")`);
    if (CODE.test(t)) f.push(`${name}: a code-shaped word in the absent sentence: "${t.match(CODE)[0]}"`);
  }
  if (want !== 'absent') f.push(...windowFaults(name, c, wc));
  return f;
}

// ==== renders ==================================================================================================================
const RENDERS = {};
for (const [k, range] of Object.entries(SERVED)) RENDERS[k] = T.renderPanel(range, {});

const arms = [];
// ---- arm 1 ----
{
  const f = [];
  const tally = [];
  for (const [k, range] of Object.entries(SERVED)) {
    const name = k.replace(/_Equity$/, '').replace('_', ' ');
    const s = RENDERS[k];
    if (/^RENDER FAILED/.test(s.html)) { f.push(`${name}: ${s.html.slice(0, 120)}`); tally.push(`${name} 0 of ${range.word_cloud.terms.length}`); continue; }
    const r = termListFaults(name, s.tree, range.word_cloud);
    f.push(...r.faults);
    tally.push(`${name} ${r.k} of ${r.n}`);
  }
  arms.push(['EVERY SERVED TERM ONCE: the [data-term] list equals the served terms in served order, each data-count the served count, each with a hover name', f.length === 0,
    f.length ? `${tally.join('; ')} -- ${f.length} fault(s): ${f.slice(0, 6).join(' | ')}` : tally.join('; ')]);
}
// ---- arm 2 ----
{
  const f = [];
  const tally = [];
  for (const [k, range] of Object.entries(SERVED)) {
    const name = k.replace(/_Equity$/, '').replace('_', ' ');
    const s = RENDERS[k];
    if (/^RENDER FAILED/.test(s.html)) { f.push(`${name}: ${s.html.slice(0, 120)}`); continue; }
    const r = sizeFaults(name, s.tree, range.word_cloud);
    f.push(...r.faults);
    tally.push(`${name} ${r.range}`);
  }
  arms.push(['SIZED BY THE SERVED COUNT: px font-size non-increasing along served order, max > min, none below 11px, one non-status colour', f.length === 0,
    f.length ? `${f.length} fault(s): ${f.slice(0, 6).join(' | ')}` : tally.join('; ')]);
}
// ---- arm 3 ----
{
  const f = [];
  const tally = [];
  for (const [name, range, want] of PLANTS) {
    const s = T.renderPanel(range, {});
    const x = stateFaults(name, s.html, range.word_cloud, want);
    f.push(...x);
    if (!x.length) tally.push(`${name.replace('BA PLANTED ', '')} -> ${want}`);
  }
  const sBA = RENDERS.BA_US_Equity;
  const cBA = /^RENDER FAILED/.test(sBA.html) ? null : containersOf(sBA.tree)[0];
  if (!cBA) f.push('BA: no [data-word-cloud] container, so the served window is not printed');
  else {
    const w = windowFaults('BA', cBA, BA.word_cloud);
    f.push(...w);
    if (!w.length) tally.push(`BA window "${longDate(BA.word_cloud.window.from)}" .. "${longDate(BA.word_cloud.window.to)}"`);
  }
  arms.push(['THE EMPTY AND ABSENT STATES: an empty served list prints its served reason verbatim, a missing key a designed sentence, 0 terms; the window prints in words', f.length === 0,
    f.length ? `${f.length} fault(s): ${f.slice(0, 6).join(' | ')}` : tally.join('; ')]);
}
// ---- arm 4: KEEP ----
{
  const rels = ['round29/checks/timeline/chart.cjs', 'round34/checks/repairs/repairs34.cjs'];
  const f = keepsPassing(rels);
  arms.push(['KEEP: round29 timeline/chart.cjs and round34 repairs/repairs34.cjs exit 0 on the same tree', f.length === 0, f.length ? f.join(' | ') : `${rels.length} of ${rels.length} exit 0`]);
}
// ---- arm 5: PLANTED ----
{
  const f = [];
  let bad = 0; let rej = 0; let good = 0; let acc = 0;
  const R = (label, faults, why) => { bad += 1; if (faults.some((x) => why.test(x))) rej += 1; else f.push(`"${label}" not rejected for its reason (${faults.length ? faults[0] : 'accepted'})`); };
  const A = (label, faults) => { good += 1; if (!faults.length) acc += 1; else f.push(`"${label}" rejected: ${faults[0]}`); };
  const esc = (s) => String(s).replace(/&/g, '&amp;').replace(/"/g, '&quot;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  const wc = BA.word_cloud;
  const maxC = wc.terms[0].count;
  const minC = wc.terms[wc.terms.length - 1].count;
  const pxOf = (count) => (maxC === minC ? 18 : Math.round((12 + ((count - minC) / (maxC - minC)) * 20) * 10) / 10);
  const INK = 'hsl(var(--semantic-action-primary))';
  const windowLine = longDate ? `<p>Headlines from ${esc(longDate(wc.window.from))} to ${esc(longDate(wc.window.to))}</p>` : '<p>no window</p>';
  const synth = (terms, opts) => {
    const o = opts || {};
    const spans = terms.map((t, i) => {
      const count = o.countAt === i ? t.count + 1 : t.count;
      const px = o.sizeAt === i ? pxOf(terms[0].count) + 4 : pxOf(t.count);
      const ink = o.inkAt === i ? 'hsl(var(--status-danger))' : INK;
      return `<span data-term="${esc(t.term)}" data-count="${count}" title="${esc(t.term)}: in ${t.count} headlines" style="font-size:${px}px;color:${ink}">${esc(t.term)}</span>`;
    }).join(' ');
    return `<div data-timeline-panel="SERVED"><div data-word-cloud="terms">${windowLine}<div>${spans}</div></div></div>`;
  };
  const goodHtml = synth(wc.terms);
  A('the synthetic BA cloud (arm 1)', termListFaults('synthetic', parse(goodHtml), wc).faults);
  A('the synthetic BA cloud (arm 2)', sizeFaults('synthetic', parse(goodHtml), wc).faults);
  A('the synthetic BA cloud window (arm 3)', windowFaults('synthetic', containersOf(parse(goodHtml))[0], wc));
  R('one term dropped', termListFaults('p', parse(synth(wc.terms.filter((_, i) => i !== 5))), wc).faults, /39 \[data-term\] rendered, 40 served|not rendered/);
  R('a data-count off by one', termListFaults('p', parse(synth(wc.terms, { countAt: 3 })), wc).faults, new RegExp(`"${wc.terms[3].term}" data-count="${wc.terms[3].count + 1}", served count ${wc.terms[3].count}`));
  R('a size increase along served order', sizeFaults('p', parse(synth(wc.terms, { sizeAt: 10 })), wc).faults, /is larger than the term before it/);
  R('a status colour on one term', sizeFaults('p', parse(synth(wc.terms, { inkAt: 7 })), wc).faults, /a status colour on a term|colours across the terms/);
  const emptyWc = { terms: [], window: null, reason: REASON_INVERTED };
  R('an empty state missing its reason', stateFaults('p', '<div><div data-word-cloud="empty"><p>No words to show.</p></div></div>', emptyWc, 'empty'), /is not printed verbatim/);
  A('an empty state with its reason', stateFaults('p', `<div><div data-word-cloud="empty"><p>${esc(REASON_INVERTED)}</p></div></div>`, emptyWc, 'empty'));
  A('an absent state with its sentence', stateFaults('p', '<div><div data-word-cloud="absent"><p>The headline word cloud is not served for this company yet.</p></div></div>', undefined, 'absent'));
  arms.push(['PLANTED: the term-list, size and state graders flag their planted faults, each for its own reason, and accept the good synthetic renders', f.length === 0,
    f.length ? f.join(' | ') : `${rej} of ${bad} planted faults flagged for their reason (term dropped, count off by one, size increase, status colour, reason missing); ${acc} of ${good} good renders accepted`]);
}

let pass = 0;
for (const [n, ok, d] of arms) { if (ok) pass += 1; console.log(`${ok ? 'ARM PASS' : 'ARM FAIL'} ${n} :: ${d}`); }
console.log(`THE WORD CLOUD RENDERS THE SERVED TERMS SIZED BY THE SERVED COUNT: ${pass} of 5 arms`);
process.exit(pass === 5 ? 0 : 1);
