# NEVER-WIDEN PAIR PACKET v3 -- IRPT_BCKEND: the Orion pairs, on the chain read (IB-pr-565) and the CTO ruling @1dca8c9e4d

**Status: DESIGN ONLY. Both halves UNSIGNED at these packet bytes.** This packet SUPERSEDES the V2 packet
(`deliverables/0.9.0_WK_IRPT_BCKEND~404/ORION_RECUT_PAIRS_PACKET_V2.md`, itself superseding V1). Where this packet is silent, V2's
sections 4 (blast radius), 5 (rollback, per key), 7 (requests), 8 (frontier) and 10 (stop rule) carry unchanged, except as the
sections below say. Nothing here is built, changed, pulled, deployed, written to AWS, invoked, signed or sent. No Orion request was made.

Author: 2.0.0_SA_COO~P2 on dell2, 2026-10-15 ~08:3xZ. Evidence: the record
`deliverables/0.9.0_WK_IRPT_BCKEND~409/IB206-1_orion_chain_read.json` (merged @8450a21863; rows `IRPT_BCKEND-D2-W409-S1` to `S7`) and the
CTO ruling `CTO_RULING_DELL2_IRPT_BCKEND_COMPOSITION_ADMISSION_RIDES_AND_ORION_BACKFILL_20261015.md` (@1dca8c9e4d) and round analysis @25f361860e.
The never-widen rule, pair (a) and pair (b) are as the V2 packet names them; the changes follow.

## 1. What changed from V2 (and why)

1. **No date token goes on the chain.** The chain's pull steps stay date-agnostic (a standing off-clock path on a scheduled producer is
   the `--month` override class). The backfill is ONE-TIME and runs the same pull code with a date argument.
2. **The manual CLIs are not retired where they are the production code.** The dispatch script runs, for each pull step, the catalog row
   `INF_API_PULL_POSITIONS_DAILY|pull_inflection_positions_daily.py`, `INF_API_PULL_TXN|pull_inflection_transactions_rest.py` and
   `INF_API_PULL_PERF|pull_inflection_performance_rest.py` (dispatch script lines 293, 295, 297). The chain copies of the positions and
   transactions scripts are BYTE-IDENTICAL to the repository scripts, so those two ARE the production code and stay. V2's
   "retire the CLI bronze writes" is withdrawn for them.
3. **Performance is different.** The chain runs its `code/gold` copy of `pull_inflection_performance_rest.py`, which DIFFERS from the
   repository script (29,230 against 29,784 bytes; row W409-S2). So a dated run of the repository script is not yet the chain's code.
   A positive control comes first (section 3).
4. **The silver aggregator has a source.** `infra/aws/lambda/inf-silver-aggregator/lambda_function.py` exists, is in the source map and is
   byte-equal to the live zip member (W409-S3). Row W404-S5's premise failed on its search scope (it read only `infra/aws/lambda/inf-pipeline`);
   W404-S5 is CLOSED and the aggregator's dispatch of `inf-gold-trigger` can be read and retired from source when (b) moves.
5. **The 06:00 fold does NOT move.** T-1 completeness at 06:00 New York is unmeasured and the stamp cannot measure it (section 2).
6. **The day sets are recomputed per feed span** against `lib/trading_calendar.py` (the fallback table, 2010 to 2027; row W409-S4).

## 2. Pair (b): the trigger keeps its measured time

The record: all 52 present T-1 flat objects (18 positions, 18 transactions, 16 performance) state an as-of date EQUAL to their own day,
never the prior trading day (W409-S7), and the feeds carry no readiness field (the leading records hold per-row status columns only).
So the pulled content cannot show that Orion's T-1 is complete at 06:00 New York. The latest landing among the present pulls is
07:51 EDT (2026-10-14) and pulls land 07:39 to 07:56 EDT; **no earlier completeness time is measured, claim `inferred`**.

**Therefore (b) is HELD, by the CTO's ruling (message 8193):** `inf-gold-trigger`, the 11:15Z bronze cron, the aggregator's dispatch and the three
CLIs' bronze writes do not change in this pair. **Inflection's trigger keeps its current measured time (about 11:32Z, the chain's pulls landing
07:39 to 07:56 EDT), recorded with this reason: T-1 completeness at 06:00 New York is unmeasurable from the 52 present objects.** The fold allows a
per-firm time (ruling @23eff24d0c). Nothing waits on a probe: the read-only probe V2 section 9 designed (15 vendor requests at 06:00, 06:30 and
07:00 New York) is NOT part of this pair, and if it is ever run it is a later act under its own pair. The aggregator's retirement (V2 section 1) is
not part of this pair either; it is designable from source (section 1.4) when a pair moves the trigger.

## 3. Pair (a): the one-time backfill, per feed

Order of the acts: (1) the performance positive control; (2) then each feed, one at a time, positions, transactions, performance. Every key is
read ABSENT first (head-object), the pull runs with the date argument of the same script the chain runs, the key is read back, and the next day
starts. ABSENT-AT-SOURCE (the vendor returns nothing for a day) is recorded with the response status and an empty key is NEVER written. A green
chain status proves no key (W404-S9: a failed pull is logged WARN and the chain reads complete); the key is read, not the chain.

| feed | script (chain copy) | identical to the repo script | span (first to last key) | trading days in span | flat keys present | to backfill |
|---|---|---|---|---|---|---|
| positions | `pull_inflection_positions_daily.py` | yes | 2020-04-24 to 2026-10-14 | 1,627 | 1,623 | 4 days that hold a parquet key and no flat key (the V2 read names 2026-07-01, 2026-08-06, 2026-09-28, 2026-09-29; re-read ABSENT at the act) |
| transactions | `pull_inflection_transactions_rest.py` | yes | 2026-05-12 to 2026-10-14 | 108 | 101 | 7: 2026-07-01, 2026-07-13, 2026-07-14, 2026-07-15, 2026-08-06, 2026-09-28, 2026-09-29 |
| performance | `pull_inflection_performance_rest.py` | NO | 2026-05-03 to 2026-10-14 | 114 | 92 | 22 (see the question below) |

The denominator is 4 + 7 + 22 = **33 days** (V2's 36 counted three non-trading days for positions and was not per-span). The six transactions days
2026-05-04 to 2026-05-11 precede the feed's first key and are OUT of span, not missing. The `_meta/window-coverage-20260716.json` object under
the transactions and performance prefixes is not a day key and is excluded (W409-S6).

**Performance days (22):** 2026-05-04 to 2026-05-08, 2026-05-11, 2026-07-01, 2026-07-02, 2026-07-06, 2026-07-07, 2026-07-09, 2026-07-13 to
2026-07-15, 2026-07-21 to 2026-07-23, 2026-08-06, 2026-09-28 to 2026-09-30 and 2026-10-13.
**RULED (CTO message 8193): the span rule is each feed's OWN first key.** Performance's first key is 2026-05-03, so every trading day after it is in
its span, whatever another feed's start; the transactions feed's 2026-05-12 start does not bind performance. The 22 performance days stand and the
denominator is 33.

**Performance positive control (a later act, one present day).** Because the chain's performance copy is not the repository script, the packet shows
that the repository script's request, output fields and file layout match what the chain writes for one PRESENT day (2026-10-14), by comparing the two
scripts' bytes with the diff named in the record and the chain's own object for that day with a read-only dry run of the repository script (no upload).
If they match, the repository script runs the 22 days. If they differ in the written shape, the CHAIN's copy runs with the date (copied to the
runner's code directory by the same sync, a change to an S3 object outside this repository, which is the precondition then named) and the repository
script's performance bronze write is retired with a message that names the chain. No performance day is written before this control.

**The date-parameterised path** is the scripts' own: positions `--start`, `--end` or `--backfill-days`; transactions and performance
`--pull-date`, each with the upload flag the catalog row carries (the dispatch lines above). The record names the `put` lines (positions line 444,
transactions line 584, performance line 638).

**Requests (estimate, not measured):** positions about 1,280 (320 clients a day, 4 days); transactions about 871 (one windowed call per account);
performance about 315 (one windowed call per client); about 2,470 in all. The real counts come from the read-back.

## 4. Blast radius, rollback and the stop rule (changes only)

- **Writes at the act:** the 33 bronze flat keys listed in section 3, each read ABSENT first. Nothing else is written: no schedule, no IAM
  principal, no Terraform change in this pair (V2's new Scheduler schedule and role are withdrawn with (b)). Served values changed: none. Other
  dates touched: none.
- **Reads:** the Orion API through the same pull code (about 2,470 requests); the bucket listings and head reads of the keys.
- **Rollback, per key:** as V2 section 5: the new version is removed so the prior state (absent) returns; the bucket is versioned; a delete is
  Andrew's act; no other key is touched.
- **Stop rule** (V2 section 10, plus): stop on a performance run before its control passes; on a key not read ABSENT first; on an empty key; on a
  response status other than success for a day not recorded ABSENT-AT-SOURCE; on any need to edit the chain's catalog or add a date token to it.

## 5. Rows that bear on this packet

W404-S3 (BLOCKING in V2): resolved by the one-time dated run of the same code; W404-S5: CLOSED (section 1.4); W404-S1, S2: resolved by the per-span
recount (section 3, W409-S5); W404-S4 (the dispatch script exists only as an S3 object): ARMED, carried; W404-S6 (T-1 at 06:00 unmeasured): carried ARMED, the trigger keeps its measured time with that reason; W404-S9 (tolerated pull failures): ARMED, carried, and the reason a key, not the chain, is the proof; W409-S1 (the grant widened by
AMENDMENT 1), S2 (the performance copy differs), S4 (the calendar fallback), S6 (the `_meta` object), S7 (as-of equals its own day).

## 6. Signatures

**COO half** (the change set, the blast radius, the order of the acts, the stop rule): 2.0.0_SA_COO~P2 -- UNSIGNED at these packet bytes; signed in a
separate file bound to the sha256 of this file (the question of section 3 is ruled). The sha256 is LEFT for the signer.
**CTO half** (the never-widen scope, the span rule (each feed's own first key) and the per-firm trigger time): 1.0.0_SA_CTO -- UNSIGNED at these packet bytes; the sha256 is LEFT for the signer.
Neither signature is implied by the presence of this file.

## 7. What this packet does not measure

It does not measure Orion's T-1 completeness at 06:00 (section 2 is inferred and no probe is part of this pair). It does not measure the request counts. It does
not read the household or account mapping tables. It does not run the performance control, build, deploy or request anything from the vendor.

-- 2.0.0_SA_COO~P2
