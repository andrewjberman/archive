/**
 * r61c.cjs -- DSGN_AMGTV1 round 61 issuer CHECK (2.0.0_SA_COO~D1): THE NEWS LIST IS RANKED BY THE SERVED MENTIONS.
 *
 * Usage (from the directory whose portal/ is the checkout under test):
 *   cd "$(git rev-parse --show-toplevel)" && node "org/missions/D13/DSGN/DSGN_AMGTV1/deliverables/2.0.0_SA_COO~D1/round61/checks/r61c.cjs"
 *
 * Why (ledger/ROUND_ANALYSIS.round60.md @0b03adc339 section 3 item 4): AMGT_RESAPP round 82 (gg-4) serves `mentions` on each /overlay
 * feed item (from the gold row's mention_count; null when none is counted). Today HeaderBrief.tsx's mergeNews ranks only the top-band
 * items by mentions and gives every feed row `mentions: null`.
 * Arms (exit 0 only on all three):
 *   1 RANKED BY SERVED MENTIONS: mergeNews(top, feed) returns one list in descending served mentions, top-band and feed items
 *     together; an item with no served mentions follows every mentioned one, in served order (top band, then feed); each row
 *     carries its served mentions; a headline is still kept once (loaded through the real module).
 *   2 NOTHING COMPUTED: the same call with no served mentions anywhere keeps today's served order (top band, then feed), and no row
 *     gets a mentions value.
 *   3 PLANTED: the graders refuse the round-60 form and wrong orders, and admit the clean form.
 * Source read only; no network; writes nothing.
 */
'use strict';
const path = require('path');
const DD = path.join(__dirname, '..', '..', '..', '2.0.0_SA_COO~D');

const item = (k, m, extra) => ({ article_key: k, url: `https://x.test/${k}`, title: `T ${k}`, publisher: 'wsj', published_at: '2026-10-08T12:00:00Z', ...(m === undefined ? {} : { mentions: m }), ...(extra || {}) });
const top = (k, m) => ({ title: `T ${k}`, url: `https://x.test/${k}`, publisher: 'Bloomberg', published_utc: '2026-10-08T12:00:00Z', mentions: m });
const TOP = [top('t1', 4), top('t2', null)];
const FEED = [item('a', 1), item('b', 7), item('c', null), item('d', 3), item('t1', 4)];
const WANT = 'b:7,t1:4,d:3,a:1,t2:null,c:null';
const PLAIN_TOP = [top('t1', null), top('t2', null)];
const PLAIN_FEED = [item('a'), item('b'), item('c')];
const WANT_PLAIN = 't1:null,t2:null,a:null,b:null,c:null';

const words = (rows) => rows.map((r) => `${(r.url || '').split('/').pop()}:${r.mentions === undefined ? 'undef' : r.mentions}`).join(',');

const G = {
  ranked: (fn) => {
    if (typeof fn !== 'function') return ['HeaderBrief exports no mergeNews'];
    let out;
    try { out = fn(TOP, FEED); } catch (e) { return ['mergeNews threw: ' + e.message]; }
    const got = words(out);
    return got === WANT ? [] : [`order ${got} (wanted ${WANT})`];
  },
  plain: (fn) => {
    if (typeof fn !== 'function') return ['HeaderBrief exports no mergeNews'];
    let out;
    try { out = fn(PLAIN_TOP, PLAIN_FEED); } catch (e) { return ['mergeNews threw: ' + e.message]; }
    const got = words(out);
    return got === WANT_PLAIN ? [] : [`with no served mentions the order or values moved: ${got} (wanted ${WANT_PLAIN})`];
  },
};

const row = (x) => ({ url: x.url, mentions: typeof x.mentions === 'number' ? x.mentions : null });
const dedupe = (rows) => { const s = new Set(); return rows.filter((r) => (s.has(r.url) ? false : (s.add(r.url), true))); };
const clean = (t, f) => dedupe([...(t || []), ...(f || [])].map((x, i) => ({ r: row(x), i }))
  .sort((x, y) => (x.r.mentions === null) - (y.r.mentions === null) || (y.r.mentions ?? 0) - (x.r.mentions ?? 0) || x.i - y.i)
  .map((x) => x.r));
const round60 = (t, f) => dedupe([...[...(t || [])].map((x, i) => ({ x, i })).sort((p, q) => (q.x.mentions ?? 0) - (p.x.mentions ?? 0) || p.i - q.i).map((p) => row(p.x)),
  ...(f || []).map((x) => ({ url: x.url, mentions: null }))]);

const arms = [];
const push = (name, f) => arms.push([name, f.length === 0, f.length ? f.join(' | ') : 'holds']);
{
  let fn = null; let err = null;
  try {
    const L = require(path.join(DD, 'round15', 'checks', '_load.cjs'));
    fn = L.source('src/pages/SecurityAnalysis/components/HeaderBrief.tsx').mergeNews;
  } catch (e) { err = 'LOADER: ' + String(e.message).split('\n')[0]; }
  push('RANKED BY SERVED MENTIONS', err ? [err] : G.ranked(fn));
  push('NOTHING COMPUTED', err ? [err] : G.plain(fn));
}
{
  const p = [];
  if (G.ranked(clean).length || G.plain(clean).length) p.push('the clean form refused');
  if (!G.ranked(round60).length) p.push('the round-60 form admitted');
  if (!G.plain((t, f) => clean(t, f).map((r) => ({ ...r, mentions: 0 }))).length) p.push('an invented mentions value admitted');
  if (!G.ranked((t, f) => [...(t || []), ...(f || [])].map(row)).length) p.push('served order without ranking admitted');
  push('PLANTED', p);
}
let pass = 0;
for (const [name, ok, ev] of arms) { if (ok) pass += 1; console.log(`ARM ${ok ? 'PASS' : 'FAIL'} ${name} :: ${ev}`); }
console.log(`ROUND 61 NEWS RANKED BY MENTIONS: ${pass} of ${arms.length} arms`);
process.exit(pass === arms.length ? 0 : 1);
