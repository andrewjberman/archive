# NEVER-WIDEN PAIR PACKET v1 -- IRPT_BCKEND cell IB-pr-556: pair (a) the seven-day positions re-pull and pair (b) the scheduled Orion raw producer in the 6 AM New York fold (round 2, workstream ~PO)

Status: DESIGN ONLY. This packet proposes one never-widen pair with two halves. Nothing in it is built, changed, pulled, re-pulled, deployed, written to AWS, invoked, signed or sent. Both halves are UNSIGNED at these packet bytes (section 12). The design record is IB200-4_orion_pairs_design.json in the same folder; this packet quotes its numbers and does not add to them.

## 0. What the pair is, in one paragraph

The Orion raw producer for the three Inflection feeds (positions, transactions, performance) is a manual command-line pull today. Its flat bronze keys, s3://opal-data-inf/bronze/<feed>/<date>.jsonl.gz, are the mirror's read contract and are cited here as existing keys, not as new addresses. Pair (b) ports the three manual writes into one scheduled handler that runs at 06:00 America/New_York, retires the manual CLI bronze writes and the three 11:15 to 11:32 UTC rules in the same release, and keeps the same key shape. Pair (a) then re-pulls every absent trading day of the three feeds through pair (b)'s code path: 7 positions days, 7 transactions days and 22 performance days, 36 keys in all. The Scope account feed joins pair (b) by addendum with its fee basis NET (amendment 2 of the order, CTO msg 8049): the sample is one household with two fee-bearing accounts in Q3 2026, every Orion request of the feed keeps calcGrossOfFees false, and a missing account is ABSENT with NO_GROUP.

## 1. Change set

Pair (b), by file (each site read at base 8110ace2ee; line and identifier as recorded in the design's pair_b.files):

- data/inf/manual_api/pull_inflection_positions_daily.py line 445, bronze_key: the manual positions write is removed; the file exits with a message naming the scheduled handler.
- infra/aws/lambda/inf-pipeline/inf-api-positions/pull_inflection_positions_daily.py line 437, bronze_key: the deployed parquet write becomes the flat .jsonl.gz shape the mirror reads.
- infra/aws/lambda/inf-pipeline/inf-api-positions/lambda_function.py line 65, pull_main: the two-step run is replaced by the one scheduled handler; the silver convert step stays after the positions write.
- infra/aws/terraform/inf-pipeline/inf-api-positions.tf lines 179 and 182: the rule inf_api_positions_schedule (cron(22 11)) is disabled in the same release.
- infra/aws/terraform/inf-pipeline/inf-api-txn.tf line 169: the rule for the transactions writer (cron(32 11)) is disabled in the same release.
- data/inf/manual_api/pull_inflection_transactions_rest.py line 585 and data/inf/manual_api/pull_inflection_performance_rest.py line 639, bronze_key: the manual flat writes are removed and each file exits with a message naming the scheduled handler.
- The opal-inf-bronze-runner-cron rule (cron(15 11)) in infra/aws/terraform/inf-pipeline/eventbridge.tf is disabled in the same release.

New names, each from lib/opal_naming.py: the schedule orion-inf-raw-producer-daily (name('orion','inflection','raw-producer','daily'), grade SCHEDULE CONFORMANT) with expression cron(0 6 * * ? *) and timezone America/New_York; the function orion-inf-raw-producer-lambda (name('orion','inflection','raw-producer','lambda'), grade LAMBDA CONFORMANT). No registry row is needed for either name; the builder does not refuse a cadence schedule.

Pair (a), by data: 7 positions keys, 7 transactions keys and 22 performance keys, listed in the design's pair_a block, each read ABSENT before the write and written through the scheduled handler.

Scope addendum: the one-account limit at infra/aws/lambda/investor-reporting/performance/orion_account_mapping.py line 84 (members != 1) is lifted by the pair. The attribution that replaces it is a build-slice decision, not decided here.

## 2. The order of the acts

1. Pair (b) is built first, with its tests, on the worker's own branch, and deployed first: the scheduled handler, the retirement of the manual writes and the rule changes go out in one release.
2. Only after pair (b) is deployed and its first scheduled run is read back, pair (a) runs, and it runs through pair (b)'s code path, never through the manual CLI.
3. The rules that the fold replaces are disabled in the same release as the fold is enabled. The fold and the old rules never run side by side, so there is no second producer.

## 3. The never-widen rule

The pair may write only the 36 keys of pair (a), the one new schedule and the one new function, and the silver convert output for the snapshot date that the existing handler already writes. It may not write any other date, any other prefix, any served value or any firm's data. The Scope feed is a source addendum and writes nothing that a served page reads until its own act. A change outside this list is a widening and is refused at the pair's review, not absorbed into the build.

## 4. Blast radius

Writes: 36 flat keys under s3://opal-data-inf/bronze/ (7 positions, 7 transactions, 22 performance); one schedule; one function; the silver positions_mv partition for the snapshot date, as the existing handler writes it today.

Reads: the Orion API per household and per account per date (no request is made by this packet); the household and account lists from the silver api_dims partitions; the session credential, read and never printed; lib/trading_calendar.py.

IAM: new_iam is false. The function reuses the role inf-api-positions-role declared at infra/aws/terraform/inf-pipeline/inf-api-positions.tf line 28; the rule uses a Lambda resource policy, not a role.

Served values: served_values_changed is false. Pair (a) writes bronze only and does not run the silver convert for the 36 keys. Other dates: other_dates_touched is false for the re-pull. The fold itself writes one new flat key per day from its first run; that is the designed effect and is named here so it is not read as re-pull scope.

Request volume, per the design: positions 2240 (320 households x 7 days); transactions up to 6041 (863 accounts x 7 dates, an upper bound); performance 7040 (320 households x 22 dates, a lower bound). All are arithmetic on recorded counts, not vendor measurements.

## 5. Rollback, per key

Each of the 36 keys is new and is written once. Rollback per key is delete-object of that exact key, and only if its read-back fails. The read-back compares ContentLength and ETag with the gzip body length and md5 recorded before the put. No other key, date or prefix is listed, read for deletion or touched. The schedule and the function roll back by disabling the rule and removing the function in the same release that created them; the retired rules are re-enabled in that rollback, never before it.

## 6. Absent days and the ABSENT-AT-SOURCE policy

A vendor response that holds no rows for a day is recorded ABSENT-AT-SOURCE with the response status in the run record. An empty key is never written. The day is listed for review. The transactions list is the feed's own span from its first key on 2026-05-12; the performance list is its span from 2026-05-03. Both lists follow the spans the order states.

## 7. Pacing

Every request goes through AdaptiveRateLimiter.throttle() (data/inf/scripts/bronze/rate_limiter.py lines 251 to 254) at the 2.0 req/s safe floor (line 112), with one request in flight and DEFAULT_RETRIES 3 with a doubling backoff. The docstring's 0.5 req/s figure is stale and is not used.

## 8. Trading-day frontier

The producer stamps the frontier with lib/trading_calendar.py expected_last_trading_day(now): today on a trading day, else the prior trading day. The trading-day pull date is prev_trading_day(now). On a non-trading day the 06:00 fire still runs; it pulls the calendar day it owes and stamps the frontier at the last trading day. Freshness is read as trading_days_behind against that stamp, never against a calendar day.

## 9. Stop rule

The stop rule for pair (a): stop at the first key whose read-back fails, whose ABSENT check finds the key already present, or whose vendor response is not a clean 200 after the retries. Stop the whole run at the first breach. A stopped run leaves its written keys in place, lists them, and rolls back only the failed key. A rerun starts from the recorded list and never re-writes a present key. Pair (b)'s schedule stops the same way: a failed fire writes no key and raises an alarm only if the standing moratorium permits it; none is built by this packet.

## 10. The releasing seat's NEVER-2 ledger

Before pair (b) is deployed, the releasing seat opens an entry in org/critical_paths/change_management/ naming the scheduled function, the schedule, the three retired rules and the manual files. The entry is closed at completion. Pair (a) is a bronze write and opens its own entry naming the 36 keys. An image or code act that reaches any task family pulling the same tag is named in that entry. If a deploy is half-landed, the releasing seat finishes it in the session or rolls back and escalates; it does not leave the fold half on.

## 11. What the packet does not measure, and what it does not touch

It does not measure the vendor's answers for any day: no Orion request was made. It does not verify the request counts (households and accounts were counted in IB199-4). It does not identify the live writer of the daily flat keys; the search and its result are recorded in the design's live_writer block as absent. It does not touch the mirror, the silver chain beyond the existing positions convert, any portal page, any firm's bucket other than the Inflection feed's, or the Scope feed's served output. The fee basis of the Scope feed is NET under amendment 2; the sample behind it is one household with two fee-bearing accounts in Q3 2026, so it is not proof for every account. The round-116 account-performance read is not in this tree and is not inferred here.

## 12. Signatures

COO half: 2.0.0_SA_COO~P2 -- UNSIGNED at these packet bytes. The COO half covers the change set, the blast radius, the stop rule and the order of the acts.

CTO half: 1.0.0_SA_CTO -- UNSIGNED at these packet bytes. The CTO half covers the never-widen scope, the retirement of the manual CLI writes, the naming of the new schedule and function through opal_naming, and the trading-day frontier.

The packet's own sha256 is left for the signers and is not computed here. Neither half is signed by the worker, and no signature is implied by this document.

## 13. Build slices (after both halves are signed)

Three LOCAL cells, each naming the files it writes: port-producer-into-scheduled-handler (the scheduled handler and the manual writes it retires); schedule-declaration (the Terraform rules and the disabled rules); scope-account-addendum (the one-account limit at orion_account_mapping.py line 84). The port is built and tested before the schedule declaration, and the addendum after the port. No shadow pipeline is built beside any of them.
