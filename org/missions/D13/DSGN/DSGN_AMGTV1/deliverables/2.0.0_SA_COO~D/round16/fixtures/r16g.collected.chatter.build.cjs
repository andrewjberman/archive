/**
 * r16g.collected.chatter.build.cjs -- DSGN_AMGTV1 round 16 (cells g-3 / g-4): builds r16g.collected.chatter.json, the
 * `/api/scoped/amgt/lead-panel/timeseries/collected/chatter` fixture in the LIVE SHAPE (issuer 2.0.0_SA_COO~D).
 *
 * SOURCE OF THE SHAPE: AMGT_RESAPP's own handler, lib/research/api/monthly_chatter.py `read_monthly_chatter()` @45e4ac9009
 * (round 56, AMGT-af-1) and its tests lib/research/api/tests/test_monthly_chatter.py:
 *   { as_of, source: "harvest gold chatter_daily", months, partial_months, rows: [{ security_key, display_name, by_month }],
 *     vintage: [<daily snapshot key>, <mention snapshot key>] }
 *   - one row per COVERED name, rows in sorted security_key order (covered_security_keys() is sorted);
 *   - an empty month is ABSENT from by_month (never a zero cell); a name with nothing collected has by_month {};
 *   - by_publisher counts only publishers with >= 1 article (a defaultdict incremented per article);
 *   - display_name is the crosswalk name, else the key itself.
 * THE COUNTS (CTO round-15 analysis ruling 2; CONTRACT amendment 2; RESAPP v68): 95 rows, 73 with an empty by_month.
 *
 * KEYS, all REAL security keys from the repo (none invented):
 *   1. the 22 rows of round15/fixtures/r15a.collected.chatter.json, with their by_month (12 collected, 10 empty);
 *   2. then the rows of the served ranking fixtures (round15 r15a.rankings.TRENDING_PRICE.return30d.json, round14
 *      rankings.BREAKOUT_PRICE.json, rankings.TRENDING_CHATTER.json) not already present: the first 10 get a deterministic
 *      by_month (so 22 rows collect), the rest are empty;
 *   3. then the covered dossier names listed by AMGT_RESAPP's ad-2 dry run
 *      (org/missions/D5/AMGT/AMGT_RESAPP/deliverables/0.7.0_AE_CloudOps~A/evidence/ad2_dryrun.txt, 237 names), in file
 *      order, until 95 rows; all empty.
 * The synthesized counts are FIXTURE values (a hash of key and month), not measurements.
 *
 * Usage (repo root): node <this file>   -> writes r16g.collected.chatter.json beside it and prints the tallies.
 */
const fs = require('fs');
const path = require('path');

const ROOT = process.cwd();
const D = path.join(ROOT, 'org/missions/D13/DSGN/DSGN_AMGTV1/deliverables/2.0.0_SA_COO~D');
const AD2 = path.join(ROOT, 'org/missions/D5/AMGT/AMGT_RESAPP/deliverables/0.7.0_AE_CloudOps~A/evidence/ad2_dryrun.txt');
const N_ROWS = 95;
const N_EMPTY = 73;

const read = (f) => {
  const x = JSON.parse(fs.readFileSync(f, 'utf8'));
  return x && x.payload && x._capture_note ? x.payload : x;
};
const base = read(path.join(D, 'round15/fixtures/r15a.collected.chatter.json'));
const rows = new Map(base.rows.map((r) => [r.security_key, { security_key: r.security_key, display_name: r.display_name, by_month: r.by_month }]));

function hash(s) {
  let h = 2166136261;
  for (let i = 0; i < s.length; i++) h = Math.imul(h ^ s.charCodeAt(i), 16777619) >>> 0;
  return h;
}
const PUBLISHERS = ['sa', 'wsj', 'bbg', 'ft', 'barrons'];
function synthMonths(key) {
  const out = {};
  for (const m of base.months) {
    const h = hash(key + '#' + m);
    if (h % 3 === 0) continue; // an empty month is absent
    const collected = 1 + (h % 17);
    const by_publisher = {};
    let left = collected;
    for (let i = 0; i < PUBLISHERS.length && left > 0; i++) {
      const n = i === PUBLISHERS.length - 1 ? left : Math.min(left, 1 + ((h >>> (i * 3)) % 5));
      if ((h >>> (i + 7)) % 4 === 0 && i > 0) continue; // a publisher with nothing that month is not listed
      by_publisher[PUBLISHERS[i]] = n;
      left -= n;
    }
    out[m] = { collected, by_publisher };
  }
  return out;
}

let synthesized = 0;
for (const f of ['round15/fixtures/r15a.rankings.TRENDING_PRICE.return30d.json', 'round14/fixtures/rankings.BREAKOUT_PRICE.json', 'round14/fixtures/rankings.TRENDING_CHATTER.json']) {
  for (const r of read(path.join(D, f)).rows || []) {
    if (!r.security_key || rows.has(r.security_key) || rows.size >= N_ROWS) continue;
    const collect = synthesized < N_ROWS - N_EMPTY - base.rows.filter((x) => Object.keys(x.by_month).length).length;
    rows.set(r.security_key, {
      security_key: r.security_key,
      display_name: typeof r.name === 'string' && r.name ? r.name : r.security_key,
      by_month: collect ? synthMonths(r.security_key) : {},
    });
    if (collect) synthesized += 1;
  }
}
for (const line of fs.readFileSync(AD2, 'utf8').split(/\r?\n/)) {
  const m = /^(\S+_Equity):/.exec(line);
  if (!m || rows.has(m[1]) || rows.size >= N_ROWS) continue;
  rows.set(m[1], { security_key: m[1], display_name: m[1], by_month: {} });
}

const sorted = [...rows.values()].sort((a, b) => (a.security_key < b.security_key ? -1 : a.security_key > b.security_key ? 1 : 0));
const payload = {
  as_of: base.as_of,
  source: 'harvest gold chatter_daily',
  months: base.months,
  partial_months: base.partial_months,
  rows: sorted,
  vintage: [
    `amgt/harvest/gold/chatter_daily/date=${base.as_of}/part-0.parquet`,
    `amgt/harvest/gold/article_security_mention/date=${base.as_of}/part-0.parquet`,
  ],
};

const empty = sorted.filter((r) => Object.keys(r.by_month).length === 0).length;
let zeroCells = 0;
let zeroPublishers = 0;
for (const r of sorted) {
  for (const c of Object.values(r.by_month)) {
    if (!(c.collected > 0)) zeroCells += 1;
    for (const n of Object.values(c.by_publisher)) if (!(n > 0)) zeroPublishers += 1;
  }
}
const latest = base.months[base.months.length - 1];
const k = sorted.filter((r) => r.by_month[latest]).length;
if (sorted.length !== N_ROWS || empty !== N_EMPTY || zeroCells || zeroPublishers) {
  console.log(`ERROR: built ${sorted.length} rows, ${empty} empty, ${zeroCells} zero cells, ${zeroPublishers} zero publishers (want ${N_ROWS}, ${N_EMPTY}, 0, 0)`);
  process.exit(1);
}
const out = path.join(__dirname, 'r16g.collected.chatter.json');
fs.writeFileSync(out, JSON.stringify(payload, null, 1) + '\n');
console.log(`OK: ${out}: ${sorted.length} rows, ${empty} with an empty by_month, ${N_ROWS - empty} collected (${synthesized} synthesized), latest ${latest}: ${k} of ${sorted.length} covered names; 0 zero cells, 0 zero publishers`);
