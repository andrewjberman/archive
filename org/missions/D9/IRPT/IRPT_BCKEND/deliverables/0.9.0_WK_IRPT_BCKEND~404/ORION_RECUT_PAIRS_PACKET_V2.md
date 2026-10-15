# NEVER-WIDEN PAIR PACKET v2 -- IRPT_BCKEND cell IB-pr-560: the Orion pairs RE-CUT

**Status: DESIGN ONLY. Both halves UNSIGNED at these packet bytes.** This packet SUPERSEDES the V1 packet
(`deliverables/0.9.0_WK_IRPT_BCKEND~400/ORION_PAIRS_PACKET_V1.md`) for the design of pair (b). It re-states pair (a) in full,
because V1's pair (a) is carried unchanged except where section 6 says otherwise. Nothing in this packet is built, changed,
pulled, re-pulled, deployed, written to AWS, invoked, signed or sent. No Orion request was made.

Record of the design: `deliverables/0.9.0_WK_IRPT_BCKEND~404/IB203-1_orion_recut_design.json` (base 519b5ccbfb). Ruling
that re-cut the pair: the CTO's round message 8127, "consolidate, never build alongside", on the located writer (IB-pr-559).

## 0. What the pair is now

Pair (b) is a **re-timing** of the existing trigger, not a new producer. The writer of the daily flat Orion keys is the gold
chain (`INF_API_PULL_TXN`, `INF_API_PULL_PERF`, `INF_API_PULL_POSITIONS_DAILY` in `orion-gold-dispatch.sh`, `chain:full`) on
the gold runner, started and sent its chain by `inf-gold-trigger` about 11:32Z, which the silver aggregator fires. The same
pulls feed the silver transactions and performance steps. So the pair moves the trigger into the 06:00 America/New_York fold
and leaves the chain whole. Pair (a) re-runs the absent trading days through the chain's own pull steps.

## 1. Change set (pair (b))

- `infra/aws/terraform/inf-pipeline/eventbridge.tf`: a NEW EventBridge Scheduler schedule, `irpt-inf-orion-gold-chain-daily`
  (the output of `lib/opal_naming.py name('irpt', 'inflection', 'orion-gold-chain', 'daily')`), `cron(0 6 * * ? *)` with
  `schedule_expression_timezone` America/New_York, invoking the EXISTING `inf-gold-trigger` with `mode` full and `source` cron.
  Beside it, unchanged: `opal-inf-bronze-runner-cron` (`cron(15 11 * * ? *)`, line 69), which keeps bronze and silver at 11:15Z.
- `infra/aws/terraform/inf-pipeline/lambdas.tf`: the silver aggregator's direct dispatch of `inf-gold-trigger`
  (`GOLD_TRIGGER_FUNCTION`, line 295) is retired in the same window, so the gold chain has one door. The release control
  `INF_GOLD_DISPATCH_RELEASE` (line 138) is NOT touched.
- The three manual CLIs (`data/inf/manual_api/pull_inflection_positions_daily.py` line 444, `pull_inflection_transactions_rest.py`
  line 584, `pull_inflection_performance_rest.py` line 638) lose their bronze write and exit with a message naming the chain.

**No new function. No port. The silver steps stay chained** inside the gold chain, after their pulls.

## 2. The re-timing and the order of the acts

The first scheduled link of the chain is `opal-inf-bronze-runner-cron`. EventBridge classic rules are UTC-only, so a 06:00
New York fold that holds across the EDT to EST change on 2026-11-01 needs a Scheduler schedule with a timezone (the precedent
is `inf-portal-publisher-floor.tf`). The order of the acts is fixed:

1. **(b) lands**: the Scheduler schedule and the aggregator retirement are applied in one window, by `safe-apply`, never a bare apply.
2. **One clean scheduled day**: the 06:00 run fires once, and its own read is the proof: the chain completes, the flat keys for
   the new day are present and read back, and no second dispatch appears in the aggregator's path.
3. **Only then (a)**: the 36 absent days are re-run through the chain's pull steps, one feed at a time, positions, then
   transactions, then performance, each key read ABSENT first.

Pair (a) is NOT run before (b) has landed and produced its clean day. Running (a) first would put a re-run of the same pulls
beside the scheduled writer: a shadow producer, which the CTO ruled out. There is no shadow path in this pair: one door, one
writer, and the retirement in the same window as the landing.

## 3. The never-widen rule

The never-widen rule binds both pairs. Pair (b) changes WHEN one existing chain runs, and changes no served value in this
order. Pair (a) writes only the 36 keys named in section 6, each read ABSENT beforehand, through the chain's pull steps, and
touches no other date and no other key. Nothing is widened to the Scope account feed, which joins by a later addendum.

## 4. Blast radius

Writes (at the act only, none in this order): the 7 positions keys, the 7 transactions keys and the 22 performance keys listed in
section 6; the new Scheduler schedule and its execution role (new IAM, at (b) landing); the Terraform files in section 1.
Reads: the Orion API through the chain's pull steps (an estimated 2,240 + 871 + 315 requests at the act; zero sent here); the
bucket listings and HEAD reads of the 36 keys; the dispatch script in S3 (the catalog the gold trigger fetches at each
dispatch). Served values changed in this order: none. Other dates touched: none. The blast radius of (b) at its own landing
is when the gold chain runs, not what it computes, and that is measured on the clean day in step 2.

## 5. Rollback, per key

Pair (b): the schedule is removed and the aggregator's dispatch line is restored from the prior Terraform state; the three
CLI bronze writes are restored from git at the base commit. A schedule removal is a Terraform change, not a delete of data.
Pair (a): per key, the new version is removed so the prior state (absent) returns. The bucket is versioned, so the prior
state is recoverable. A delete is Andrew's act; no worker deletes a key. No other key is touched by a rollback.

## 6. Absent days and the ABSENT-AT-SOURCE policy (pair (a))

The order lists 7 positions days, 7 transactions days and 22 performance days. Measured against `lib/trading_calendar.py`
over 2026-05-03 to 2026-10-14 (114 trading days from 2026-05-04), the lists differ in two places, recorded as surprise rows
and kept as the order states because the check requires those counts:

- **Positions**: 2026-07-03, 2026-07-04 and 2026-07-05 are not NYSE trading days; each holds a `.parquet` key only. The
  calendar shows 4 trading days without a flat key: 2026-07-01, 2026-08-06, 2026-09-28 and 2026-09-29.
- **Transactions**: the calendar shows 13 trading days without a flat key, six of which (2026-05-04 to 2026-05-11) the order
  does not list. The seven listed days are measured absent.
- **Performance**: 22 listed, 22 measured, the same days.

The CTO rules the day set before any write. Until then no key is written for a day the calendar does not hold.

Positions keys (flat, `s3://opal-data-inf/bronze/positions/<date>.jsonl.gz`): 2026-07-01, 2026-07-03, 2026-07-04, 2026-07-05,
2026-08-06, 2026-09-28, 2026-09-29. Transactions (`bronze/transactions/`): 2026-07-01, 2026-07-13, 2026-07-14, 2026-07-15,
2026-08-06, 2026-09-28, 2026-09-29. Performance (`bronze/performance/`): 2026-05-04 to 2026-05-08, 2026-05-11, 2026-07-01,
2026-07-02, 2026-07-06, 2026-07-07, 2026-07-09, 2026-07-13 to 2026-07-15, 2026-07-21 to 2026-07-23, 2026-08-06, 2026-09-28 to
2026-09-30 and 2026-10-13.

**Through the chain's steps, with a precondition.** The catalog rows of the three pull steps carry no date token, and
`run_chain` refuses `--run-date` for date-agnostic steps. A past-day re-run through the steps therefore needs the catalog row
to carry a day argument. That is a change to the S3 object, which lives outside this repository. The act does not start until
it exists; this is a BLOCKING surprise row.

**ABSENT-AT-SOURCE policy.** Each key is read ABSENT before the act. Where the vendor returns nothing for a day, the day is
recorded ABSENT-AT-SOURCE with the response status, and an empty key is never written. A tolerated pull failure in the chain
is not a write, and a green chain status does not prove a key. The key is read, not the chain.

**Read-back.** After each write: head-object compares ContentLength with the local gzip size, ContentType with application/gzip,
and the object's row count and asOfDate with the pull's own log line. A mismatch fails the act for that key.

## 7. Pacing and requests

Requests are estimates from distinct identifiers in the 2026-10-14 objects: 320 clients for positions (7 days, 2,240),
871 accounts for transactions (871, one windowed call per account), 315 clients for performance (315, one windowed call per
client). The estimates are not measured against the mapping tables, and the windowing assumption is unverified. The read-back
counts the real requests. Pacing follows the scripts' own rate limiter; no pacing is set in this order.

## 8. Trading-day frontier

The 06:00 run takes its frontier from `lib/trading_calendar.py` `expected_last_trading_day(now)`, which is T-1 on a trading day.
The freshness basis is trading-day-frontier. A run on a non-trading day is not a failure. Any new schedule name is the builder's
output: `irpt-inf-orion-gold-chain-daily`. The builder refuses a clock time as a cadence, so the time lives in the expression.

## 9. T-1 completeness: the result

**Claim: inferred. Not measured complete at 06:00 New York** (10:00Z while EDT holds). The earliest pull on record is the flat
write at 07:39 EDT (11:39Z) on 2026-10-10 to 2026-10-14. Every pull starts after the 11:32Z trigger, not on a vendor-readiness
signal. The earliest measured-complete time is therefore not established, and 06:00 is unproven, 1 hour 39 minutes before the
earliest pull.

Evidence read without a vendor call: the 2026-10-14 positions object carries 37,008 rows, asOfDate 2026-10-14 on every row,
and a maximum editedDate of 2026-10-13, so T-1 edits were present in the 07:51 EDT pull. The 2026-10-13 object's maximum
editedDate is 2026-10-10, the prior trading day. The 2026-10-14 performance object carries 315 rows for each of 2026-10-12,
2026-10-13 and 2026-10-14, and the performance pull's own comment says the most recent factors are provisional, with a
SETTLE_DAYS re-pull of 7 days.

**Probe (for a later order, not this one).** At 06:00, 06:30 and 07:00 New York, five client-assets requests per probe (15
vendor requests), compared with the 07:39 EDT pull of the same day. T-1 is complete at 06:00 only if the 06:00 probe equals that
pull for every probed client. If it does not, the earliest probe that equals it is the earliest measured-complete time, and the
schedule moves to that time before (b) lands.

## 10. Stop rule

Stop, file a row, and change nothing more, on any of: a need to start, stop, invoke, pull or write anything; a need to read a
secret value; a re-run whose key is not read ABSENT first; a key written as empty; a dispatch that appears in the aggregator's
path after the retirement; a 06:00 run that does not match the probe in section 9 once the probe exists; a request to delete
a key, which is Andrew's act.

## 11. Surprise rows that bear on this packet

Filed in `surprise-channel/investigations/INVESTIGATION_v1.md` as `IRPT_BCKEND-D2-W404-S1` to `S10`: the positions day list
against the calendar (S1); the transactions day list (S2); the catalog's missing date token, BLOCKING (S3); the dispatch
script's S3-only home with no repository copy (S4); the aggregator's source absent from the tree, BLOCKING for its retirement
(S5); the unmeasured T-1 at 06:00, ARMED (S6); stale timing comments (S7); the stale HOLD text against the release control (S8);
tolerated pull failures, ARMED (S9); and a stale docstring on the positions CLI (S10).

## 12. Signatures

**COO half** (the change set, the blast radius, the stop rule and the order of the acts): 2.0.0_SA_COO~P2 -- UNSIGNED at these
packet bytes. The sha256 of the COO half is LEFT for the signer to compute at signing; it is not computed here.

**CTO half** (the never-widen scope, the retirement of the manual CLI writes, the naming of the new schedule through
`opal_naming`, and the trading-day frontier): 1.0.0_SA_CTO -- UNSIGNED at these packet bytes. The sha256 of the CTO half is
LEFT for the signer; it is not computed here.

Neither half is signed by this packet, and neither signature is implied by the presence of this file.

## 13. Build slices (LOCAL, proposed, after both halves are signed)

- `schedule-0600ny-fold`: `infra/aws/terraform/inf-pipeline/eventbridge.tf` (the schedule and its role). LOCAL.
- `cli-bronze-write-retirement`: the three manual CLIs under `data/inf/manual_api/`. LOCAL.
- `aggregator-dispatch-retirement`: `infra/aws/terraform/inf-pipeline/lambdas.tf`, after `schedule-0600ny-fold`. LOCAL.

The dispatch script's catalog change is an S3 object outside this repository and is not a build slice here; it is the precondition
named in section 6.

## 14. What this packet does not measure

It does not measure the 06:00 completeness (section 9 is inferred). It does not measure the request counts (section 7 is an
estimate). It does not read the silver aggregator's source, which is not in the tree. It does not read the household or account
mapping tables. It does not sign, build, deploy or request anything from the vendor.
