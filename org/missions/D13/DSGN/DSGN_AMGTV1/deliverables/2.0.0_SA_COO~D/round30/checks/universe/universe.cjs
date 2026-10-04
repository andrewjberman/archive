/**
 * universe.cjs -- DSGN_AMGTV1 round 30, AV-zh-1 ONE UNIVERSE PER FACE (cell-slug universe; issuer 2.0.0_SA_COO~D): EACH LEAD PANEL
 * FACE READS ONE SERVED UNIVERSE.
 *
 * Usage (from the directory whose portal/ is the checkout under test, e.g. C:/tmp/wk-dsgn-amgtv1-82): node <this file>
 * Grades: row AMGT_RESAPP-Z-W208-S1 (placed with the issuer; CTO msg 28772): "portal LeadPanel.tsx holds three universes in one
 *   component -- the price ranking (94 names), the monthly collected chatter (95 covered names) and the chatter ranking (1 name,
 *   read only to join starred names); the one served universe it should read is the covered universe" (INVESTIGATION_v1.md
 *   :16965), at base LeadPanel.tsx:420 (`useLeadPanelRankings(movement, subject)` on BOTH faces) and :438-443 (`starredKeys` built
 *   from `rankingQuery.data.rows`). RESAPP am-3 serves `ticker` on every collected row (95 of 95 in windows.chatter.30.json).
 * THE CONTRACT (the worker face quotes it):
 *   - PRICE reads the price ranking only: getLeadPanelRankings(<movement>, 'PRICE', ...) is read; no other ranking subject, no
 *     collected-chatter read, no rank series. The starred list (getStarred) may be read on either face.
 *   - CHATTER reads the collected chatter only: getCollectedChatter is read; NO getLeadPanelRankings read of any subject and no
 *     rank series (useLeadPanelRankings disabled -- `enabled: false` or skipToken -- or not called on Chatter).
 *   - CHATTER "Starred only" draws exactly the collected rows whose own served `ticker` is in the starred list (the starred join
 *     is taken from the collected rows, never from a ranking); "All names" draws every collected row.
 *   - PRICE "Starred only" keeps working off the price rows (the bars of the price rows whose ticker is starred).
 * Render: ./_universe.cjs -- the REAL LeadPanel.tsx and the REAL hooks/useLeadPanelApi.ts over a react-query recorder (a read =
 *   an endpoint call made by an ENABLED query's queryFn, react-query v5 enabled/skipToken semantics) and an endpoint recorder
 *   returning served-shape fixtures; ChatterBubbles is a stub drawing one data-stub-bubble per row it is handed; PriceBars is real.
 * Inputs: round30/fixtures/windows.price.30.json (94 rows), windows.chatter.30.json (95 rows); round30/fixtures/universe/
 *   universe.planted.json: starred [AMD US, ROG SW, 1299 HK, BA US, ZZPL US] (ROG SW is the one covered name the price ranking
 *   lacks; ZZPL US is on no list), the chatter ranking planted EMPTY (rows []) and DECOY (each starred ticker joined to a
 *   different covered key) on the served route shape (round14/fixtures/rankings.trending.chatter.json).
 * Arms:
 *   1  ONE READ PER FACE: on Chatter (All names and Starred only) no ranking read of any subject and no rank-series read is made
 *      and the collected-chatter read is; on Price (both) the price ranking read is made and no other ranking subject, no
 *      collected read and no rank series.
 *   2  CHATTER STARRED FROM THE COLLECTED TICKER: with the chatter ranking planted EMPTY and planted DECOY, Chatter "Starred only"
 *      hands ChatterBubbles exactly the 4 collected rows whose ticker is starred (AMD, ROG, 1299, BA), 0 missing, 0 extra, 0
 *      duplicate; "All names" hands all 95 collected rows.
 *   3  CONTROL (passes at base by design): Price "Starred only" draws exactly the bars of the 3 starred price rows (AMD, 1299, BA);
 *      "All names" draws more bars than that.
 *   4  PLANTED: the read predicate rejects the base Chatter read set (ranking CHATTER + collected), a Chatter face reading the
 *      PRICE ranking, a Price face reading collected chatter and a Price face with no price read, and accepts the reference sets;
 *      the recorder logs no read for `enabled: false`, `enabled: () => false` or skipToken and one read for an enabled query (sync
 *      and async queryFn); the set predicate accepts the exact set and rejects empty, decoy, one-missing, one-extra and duplicate.
 * Blind spots: a read issued from an effect (useEffect) does not run under static render and is not seen; a read through a hook
 *   file other than useLeadPanelApi.ts is the loader's proxy and is not seen (the cell owns only LeadPanel.tsx and
 *   useLeadPanelApi.ts); the bubbles are what LeadPanel HANDS ChatterBubbles, not ChatterBubbles' own drawing.
 * Prints one line per arm and "EACH LEAD PANEL FACE READS ONE SERVED UNIVERSE: <k> of 4 arms"; exit 0 only at 4 of 4.
 * Writes no file. No network, no AWS. Seconds.
 */
const U = require('./_universe.cjs');

const T0 = Date.now();
const STARRED_TICKERS = new Set(U.STARRED.map((s) => s.ticker));
const WANT_CHATTER = U.COLLECTED.rows.filter((r) => typeof r.ticker === 'string' && STARRED_TICKERS.has(r.ticker)).map((r) => r.security_key);
const WANT_ALL = U.COLLECTED.rows.map((r) => r.security_key);
const WANT_PRICE = U.PRICE.rows
  .filter((r) => STARRED_TICKERS.has(r.ticker) && typeof r.return_30d_pct === 'number' && Number.isFinite(r.return_30d_pct))
  .map((r) => r.security_key || r.ticker);
const short = (k) => String(k).replace(/_Equity$/, '');

// ---------------- predicates ----------------
const KNOWN = new Set(['getLeadPanelRankings', 'getRankTimeSeries', 'getCollectedChatter', 'getStarred']);
/** Faults of one face's read set ([{fn, subject}]). */
function readFaults(face, reads) {
  const f = [];
  const rank = reads.filter((r) => r.fn === 'getLeadPanelRankings');
  const series = reads.filter((r) => r.fn === 'getRankTimeSeries');
  const coll = reads.filter((r) => r.fn === 'getCollectedChatter');
  const other = reads.filter((r) => !KNOWN.has(r.fn));
  if (face === 'CHATTER') {
    if (rank.length) f.push(`RANKING: the Chatter face reads ${rank.length} ranking(s) (subject ${rank.map((r) => r.subject).join(', ')})`);
    if (!coll.length) f.push('COLLECTED: the Chatter face makes no collected-chatter read');
  } else {
    const p = rank.filter((r) => r.subject === 'PRICE');
    const np = rank.filter((r) => r.subject !== 'PRICE');
    if (!p.length) f.push('PRICE: the Price face makes no price ranking read');
    if (np.length) f.push(`RANKING: the Price face reads ${np.length} non-price ranking(s) (subject ${np.map((r) => r.subject).join(', ')})`);
    if (coll.length) f.push('COLLECTED: the Price face reads the collected chatter');
  }
  if (series.length) f.push(`SERIES: the ${face} face reads ${series.length} rank series`);
  if (other.length) f.push(`OTHER: the ${face} face reads ${other.map((r) => r.fn).join(', ')}`);
  return f;
}
/** Faults of a drawn key list against the wanted key list: missing, extra, duplicate. */
function setFaults(label, want, got) {
  const f = [];
  const w = new Set(want);
  const g = new Set(got);
  const missing = [...w].filter((k) => !g.has(k));
  const extra = [...g].filter((k) => !w.has(k));
  if (missing.length) f.push(`${label}: ${missing.length} missing (${missing.slice(0, 4).map(short).join(', ')})`);
  if (extra.length) f.push(`${label}: ${extra.length} extra (${extra.slice(0, 4).map(short).join(', ')})`);
  if (got.length !== g.size) f.push(`${label}: ${got.length - g.size} duplicate(s)`);
  return f;
}
const readTally = (reads) => {
  const n = {};
  for (const r of reads) { const k = r.fn.replace(/^get/, '') + (r.subject ? `/${r.subject}` : ''); n[k] = (n[k] || 0) + 1; }
  return Object.entries(n).map(([k, v]) => `${k} ${v}`).join(', ') || 'none';
};

const arms = [];
// ---------------- arm 1: one read per face ----------------
{
  const f = [];
  const tally = [];
  for (const face of ['CHATTER', 'PRICE']) {
    for (const st of [false, true]) {
      try {
        const r = U.renderFace(face, st, { chatterRanking: 'EMPTY' });
        f.push(...readFaults(face, r.reads).map((x) => `${face}${st ? ' starred' : ''}: ${x}`));
        tally.push(`${face}${st ? ' starred' : ''} [${readTally(r.reads)}]`);
      } catch (e) { f.push(`${face}${st ? ' starred' : ''}: RENDER: ${String(e.message).split('\n')[0]}`); }
    }
  }
  arms.push(['ONE READ PER FACE: Chatter makes no ranking read of any subject and reads the collected chatter; Price reads the price ranking and no collected chatter',
    f.length === 0, f.length === 0 ? tally.join('; ') : f.slice(0, 4).join(' | ') + ` || reads: ${tally.join('; ')}`]);
}
// ---------------- arm 2: chatter starred from the collected ticker ----------------
{
  const f = [];
  const tally = [];
  for (const plant of ['EMPTY', 'DECOY']) {
    try {
      const r = U.renderFace('CHATTER', true, { chatterRanking: plant });
      const fx = setFaults(`starred (ranking ${plant})`, WANT_CHATTER, r.bubbles);
      f.push(...fx);
      tally.push(`ranking ${plant}: ${r.bubbles.length} bubble(s) [${r.bubbles.map(short).join(', ')}]`);
    } catch (e) { f.push(`starred (ranking ${plant}): RENDER: ${String(e.message).split('\n')[0]}`); }
  }
  try {
    const r = U.renderFace('CHATTER', false, { chatterRanking: 'EMPTY' });
    f.push(...setFaults('all names', WANT_ALL, r.bubbles));
    tally.push(`all names ${r.bubbles.length} of ${WANT_ALL.length}`);
  } catch (e) { f.push(`all names: RENDER: ${String(e.message).split('\n')[0]}`); }
  arms.push([`CHATTER STARRED FROM THE COLLECTED TICKER: "Starred only" draws exactly the ${WANT_CHATTER.length} starred covered names (${WANT_CHATTER.map(short).join(', ')}) with the ranking EMPTY and DECOY; "All names" draws all ${WANT_ALL.length}`,
    f.length === 0, f.length === 0 ? tally.join('; ') : f.slice(0, 5).join(' | ') + ` || ${tally.join('; ')}`]);
}
// ---------------- arm 3: control -- the price face's starred filter ----------------
{
  const f = [];
  let tally = '';
  try {
    const s = U.renderFace('PRICE', true, { chatterRanking: 'DECOY' });
    f.push(...setFaults('price starred', WANT_PRICE, s.bars));
    const a = U.renderFace('PRICE', false, { chatterRanking: 'DECOY' });
    if (a.bars.length <= WANT_PRICE.length) f.push(`price all names: ${a.bars.length} bar(s), not more than the ${WANT_PRICE.length} starred (the filter is not narrowing)`);
    tally = `starred ${s.bars.length} bar(s) [${s.bars.map(short).join(', ')}]; all names ${a.bars.length} bar(s)`;
  } catch (e) { f.push('RENDER: ' + String(e.message).split('\n')[0]); }
  arms.push([`CONTROL (passes at base by design): Price "Starred only" draws exactly the ${WANT_PRICE.length} starred price rows (${WANT_PRICE.map(short).join(', ')}); "All names" draws more`,
    f.length === 0, f.length === 0 ? tally : f.join(' | ') + (tally ? ` || ${tally}` : '')]);
}
// ---------------- arm 4: planted ----------------
{
  const f = [];
  const caught = [];
  const rd = (fn, subject) => ({ fn, subject: subject || null });
  const GOOD = [
    ['Chatter reference', 'CHATTER', [rd('getCollectedChatter'), rd('getStarred')]],
    ['Price reference', 'PRICE', [rd('getLeadPanelRankings', 'PRICE'), rd('getStarred')]],
  ];
  for (const [n, face, reads] of GOOD) { const x = readFaults(face, reads); if (x.length) f.push(`${n} rejected: ${x[0]}`); }
  const BAD = [
    ['base Chatter reads', 'CHATTER', [rd('getLeadPanelRankings', 'CHATTER'), rd('getCollectedChatter'), rd('getStarred')], 'RANKING'],
    ['Chatter reads the price ranking', 'CHATTER', [rd('getLeadPanelRankings', 'PRICE'), rd('getCollectedChatter')], 'RANKING'],
    ['Chatter with no collected read', 'CHATTER', [rd('getStarred')], 'COLLECTED'],
    ['Price reads collected chatter', 'PRICE', [rd('getLeadPanelRankings', 'PRICE'), rd('getCollectedChatter')], 'COLLECTED'],
    ['Price with no price read', 'PRICE', [rd('getLeadPanelRankings', 'CHATTER'), rd('getStarred')], 'PRICE'],
  ];
  for (const [n, face, reads, cls] of BAD) {
    const x = readFaults(face, reads);
    if (x.some((y) => y.startsWith(cls + ':'))) caught.push(`${n}->${cls}`); else f.push(`"${n}" not rejected as ${cls} (${x[0] || 'no fault'})`);
  }
  // the recorder: disabled queries make no read; an enabled one makes one, sync or async
  const probe = (opts) => {
    U.Q.queries = []; U.Q.direct = []; U.Q.chatterRanking = U.CHATTER_RANKING.EMPTY;
    const res = U.rq.useQuery(Object.assign({ queryKey: ['planted'] }, opts));
    const n = U.Q.queries.filter((q) => q.enabled).flatMap((q) => q.calls).length + U.Q.direct.length;
    return { n, data: res.data };
  };
  const fn = () => U.endpoints.getLeadPanelRankings('TRENDING', 'CHATTER', 25);
  const rec = [
    ['enabled false', probe({ queryFn: fn, enabled: false }), 0],
    ['enabled () => false', probe({ queryFn: fn, enabled: () => false }), 0],
    ['skipToken', probe({ queryFn: U.SKIP }), 0],
    ['enabled (sync)', probe({ queryFn: fn }), 1],
    ['enabled (async)', probe({ queryFn: async () => fn() }), 1],
  ];
  for (const [n, r, want] of rec) {
    if (r.n !== want) f.push(`recorder: ${n} logged ${r.n} read(s), want ${want}`);
    else caught.push(`recorder ${n}=${want}`);
  }
  if (!rec[4][1].data || !Array.isArray(rec[4][1].data.rows)) f.push('recorder: the async queryFn returned no payload');
  // the set predicate
  const W = WANT_CHATTER;
  const DECOY = U.CHATTER_RANKING.DECOY.rows.map((r) => r.security_key);
  if (setFaults('ref', W, W.slice().reverse()).length) f.push('the exact set (reordered) is rejected');
  const SB = [
    ['empty', []],
    ['decoy', DECOY],
    ['one missing', W.slice(1)],
    ['one extra', W.concat(['SNPS_US_Equity'])],
    ['duplicate', W.concat([W[0]])],
  ];
  for (const [n, got] of SB) { if (setFaults('p', W, got).length) caught.push(`set ${n}`); else f.push(`set "${n}" accepted`); }
  arms.push(['PLANTED: the read predicate, the read recorder and the set predicate each reject the known-bad input and accept the reference',
    f.length === 0, f.length === 0 ? `2 reference read sets 0 faults; ${caught.length} of ${BAD.length + rec.length + SB.length} planted cases decided right (${caught.join(', ')})` : f.join(' | ')]);
}

let pass = 0;
for (const [n, ok, d] of arms) { if (ok) pass += 1; console.log(`${ok ? 'ARM PASS' : 'ARM FAIL'} ${n} :: ${d}`); }
console.log(`WALL: ${((Date.now() - T0) / 1000).toFixed(1)}s`);
console.log(`EACH LEAD PANEL FACE READS ONE SERVED UNIVERSE: ${pass} of ${arms.length} arms`);
process.exit(pass === arms.length ? 0 : 1);
