# Backfill plan packet IB-pr-522: account_activity_daily (census and design, nothing run)

Worker 0.9.0_WK_IRPT_BCKEND~369, order [IRPT_BCKEND.TO-IB-pr-522](file:///C:/dev/wk-IRPT_BCKEND-369/org/missions/D9/IRPT/IRPT_BCKEND/task-orders/IRPT_BCKEND.TO-IB-pr-522.activity-backfill-census-and-plan.md). Base commit f9138c4f06. Record: [IB186-2_activity_backfill_census.json](file:///C:/dev/wk-IRPT_BCKEND-369/org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~369/IB186-2_activity_backfill_census.json).

## Purpose

This packet plans a backfill of the gold table account_activity_daily for the one custody source the reporting-gold function declares. It is a design. Nothing was invoked, written or deployed. Its source is the CTO's round-186 analysis (item 3), under Andrew's floor: nothing earlier than an account's earliest record, cut at 2012-01-01.

## Premises as found (re-grounded at base f9138c4f06)

- The writer is not named irpt-reporting-gold. The live function and its log group are irpt-49f-reporting-gold-lambda, the name opal_name builds in [lambda.tf](file:///C:/dev/wk-IRPT_BCKEND-369/infra/aws/terraform/investor-reporting/reporting-gold/lambda.tf).
- The 49financial activity table holds 4 partitions, 2026-10-07 to 2026-10-12. This matches the relay.
- The producer declares one custody source. A second firm is refused by [handler.py](file:///C:/dev/wk-IRPT_BCKEND-369/infra/aws/lambda/investor-reporting/reporting-gold/handler.py) at lines 222-224. cottonwood and inflection cannot be backfilled by this function, so they are not planned here.

## 1. Writers (count 2)

| # | File | How |
|---|------|-----|
| 1 | [handler.py](file:///C:/dev/wk-IRPT_BCKEND-369/infra/aws/lambda/investor-reporting/reporting-gold/handler.py) | scheduled_and_backfill: the scheduled fire and the explicit backfill event both call the emit |
| 2 | [account_activity_lots.py](file:///C:/dev/wk-IRPT_BCKEND-369/data/assets/scripts/gold/irpt_reporting/account_activity_lots.py) | other: its emit_day (lines 1318-1353) is the write primitive, called only by the handler |

The search covered infra/, data/ and lib/ with the Grep tool. Test files were excluded because they use a fake S3. The live role policy grants PutObject on the activity prefix to the function role only. Other principals were not enumerated.

## 2. The three firms: table state and demand

| Firm | Activity partitions | Returns partitions | Demand |
|------|---------------------|--------------------|--------|
| 49financial | 4 (2026-10-07 to 2026-10-12) | 569 (2024-07-08 to 2026-10-12) | earliest_record 2024-07-08, start_day 2024-07-08, 565 trading days, 23 invocations |
| cottonwood | 0 | 3325 (2013-04-03 to 2026-06-22) | null: no source declared, not sourced, not estimated |
| inflection | 0 | 0 | null: no source declared, not sourced, not estimated |

The 2012 floor was applied to 49financial and is not binding there, because the source's first partition is 2024-07-08. The earliest record is the source's first partition day, which is a bound. The per-account first day needs object bodies and was not read.

The trading-day count uses the repository calendar's hardcoded NYSE fallback, which the module reported with a WARN. The chunk bound is MAX_BACKFILL_DAYS = 25 from handler.py line 119.

## 3. Rate and time

The observed rate is 216.7 seconds per trading day. It is the REPORT duration of the scheduled 1-day run for 2026-10-12 (upload True), read from the live log group. Current-stage 1-day runs since 2026-10-09 measured 96.4 to 389.1 seconds.

The time is derived, not measured. At the linear rate, 565 days take about 34 hours serial over 23 invocations. A 25-day chunk would take about 5,400 seconds, past the function's 900-second timeout. The lots stage is one producer call per invocation, so the linear figure may overstate. No 25-day chunk with the lots stage has run, so the chunk time is unmeasured. The 25-day chunks of 2026-10-03 took 21 to 63 seconds each, but they predate the lots stage.

## Timeout fact

- The function's timeout is 900 seconds (get-function-configuration, read at base f9138c4f06).
- The measured rate is 216.7 seconds per trading day: the REPORT duration of the scheduled 1-day run for 2026-10-12, with the lots stage. Five current-stage 1-day runs since 2026-10-09 measured 96.4 to 389.1 seconds.
- At 216.7 seconds a day, a 25-day chunk is about 5,400 seconds, six times the timeout. The largest chunk the timeout allows at that rate is about 4 trading days (900 divided by 216.7 is 4.15).
- So the 23 invocations counted from the 25-day chunk bound are a floor and not a runnable plan. At 4 trading days a chunk, the same 565 days would need about 142 invocations (derived from the measured rate, not measured).
- The linear rate is an extrapolation. The lots stage is one producer call per invocation, so the true chunk time is unmeasured.
- The 2026-10-03 passes do not change this. Twenty-three backfill invocations (22 chunks of 25 trading days and one of 12) over 2024-07-08 to 2026-10-01 logged 21 to 63 seconds each (median 37.8 seconds, about 1.51 seconds a day). No account_activity_daily line appears in their logs, so they predate the lots stage. They show what a returns-only run cost in that period, not what the current code costs, and they rewrote the returns days of their range.

## Two designs for the CTO

The CTO must choose one. Neither is run, and neither half is signed. The names (A) and (B) here are the designs; Branch A and Branch B below are the run order and the rollback.

**Design (A): the existing explicit backfill event, in timeout-sized chunks.** The function's backfill event as it stands, `{"backfill": {"start", "end"}, "accounts": "population"}`, run oldest-first in chunks of about 4 trading days, for the one custody source.

- Cost: no code change. About 142 invocations (derived), each preceded by a dry run. The serial wall time is about 34 hours at the linear rate (derived, not measured).
- What it puts at risk: run_backfill calls the returns emit for every day of the range, so the 565 landed returns days are rewritten as well as the class partitions. The range lies inside the 569 landed returns days, so served returns are touched.
- The activity stage is not idempotent: 2026-10-08 landed 6901 rows, and dry runs of the same day later logged 6904. A re-run changes the activity content.
- Undo: versioning is Enabled on the gold bucket, so a rewritten returns object can be restored by version id, but only by an operator identity with GetObjectVersion and PutObject. The function role cannot do it. A new activity partition can be removed only by a delete from an operator identity.
- A timeout mid-chunk leaves some days written and others not.

**Design (B): an activity-and-lots-only run.** A small change to the function so that a backfill event can select its stages, running the activity and lots stages and not the returns or class stages.

- Cost: a code change to the function, which needs its own code release and its own pair (COO half and CTO half, both unsigned here). The change is not written, tested or deployed by this census.
- What it keeps safe: the served returns and class partitions are not written by a run of this shape, so the rewrite in Design (A) does not arise.
- What it does not fix: the activity stage stays non-idempotent (6901 against 6904), so a re-run still changes activity content. The lots stage refused 2026-10-07 and 2026-10-08 on the realized-lot key check (LOTS_SKIPPED), and that cause was not read.
- Not measured: the wall time of an activity-and-lots chunk with no returns stage, so the 4-day chunk size is not verified for this design. Whether the activity and lots stages can run without the returns emit in the same pass was not read.
- Undo: versioning covers rewritten objects, and new activity and lots partitions can be removed only by an operator delete, as under Design (A).

## Branch A: run order

1. Re-list the activity and returns prefixes and record the counts before the first chunk.
2. Range: 2024-07-08 to 2026-10-06, oldest first, in chunks of at most 25 trading days (MAX_BACKFILL_DAYS). At the measured rate a 25-day chunk exceeds the 900-second timeout, so the 23 chunks are a floor; under Design (A) the chunk is about 4 trading days (see Timeout fact). The range end must not pass the newest returns day, 2026-10-12, and it does not.
3. For each chunk, send a dry_run invocation first: `{"backfill": {"start", "end"}, "accounts": "population", "dry_run": true}`. Read the printed row counts and any LOTS_SKIPPED or CLASS_SKIPPED line. Send the real chunk only when the dry run is clean.
4. Invoker and identity: the function role irpt-49f-reporting-gold-role executes the code. The invoker needs lambda:InvokeFunction and must be an operator identity, not the scheduler role. The invoker was not read.
5. After each chunk, verify three things. The new activity partitions are present for every trading day of the chunk. There are no LOTS_SKIPPED lines. The returns key count is still 569, since the keys do not change, although the bytes are rewritten.
6. Stop on any REFUSED line, any LOTS_SKIPPED line or any timeout, and file a row. A timeout mid-chunk can leave some days written and others not.
7. After the run, a person checks the default report on DEV. It must show contributions, withdrawals and income for a window longer than 4 days. That check is not performed here.

## Branch B: rollback

- Rewritten objects (returns, class and lot partitions of days already landed): restore the prior version by version id. Versioning is Enabled on the gold bucket. Record the prior version id of every key before its chunk runs, because the version list is the only undo path. This needs an operator identity with GetObjectVersion and PutObject. The function role cannot do it.
- New objects (activity partitions and lot partitions of days not landed before): removable only by a delete from an operator identity. The function role has no delete. A delete is destructive and needs Andrew's word.
- The status object _status/lots_not_computed.json is overwritten, not deleted.
- Not undoable by this plan: a new key cannot be returned to absent without a delete, and a rewritten key's new bytes cannot be reproduced exactly on a later re-run, because a re-run did not reproduce its bytes (see the census record).

## Blast radius

- Keys: the five gold prefixes of the 49financial gold bucket (returns, class, realized lots, unrealized lots, activity), for 565 trading days. Returns: 565 of 569 landed partitions are rewritten. Activity: 565 new partitions. Class and lot counts were not read.
- Firms: 49financial only. cottonwood and inflection are outside this function's reach.
- What a mis-run can overwrite: any landed day in the range, with rows computed from the source as it stands at run time. The census recorded 6901 activity rows for 2026-10-08 and later 6904 for the same day, so a re-run changes content.

## Red list

The red list at [IB117-1_red_list.json](file:///C:/dev/wk-IRPT_BCKEND-369/org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~278/IB117-1_red_list.json) names two target prefixes: infra/aws/lambda/investor-reporting/_contracts/ and docs/contracts/investor-reporting/. The backfill writes S3 keys under the gold prefixes and changes no repository file. Its write set does not intersect either target prefix. The red list operation (analysis-request-original) is not touched.

## The 2012 floor and Andrew's words

Source: the CTO's relay of Andrew's direction of 2026-10-07. "We don't need anything prior to the earliest record of a client ... any backfill is thereby cut at 2012." The floor is 2012-01-01. For 49financial it does not bind, since the source starts 2024-07-08. The producer cannot reach earlier days because its source does not hold them.

## The pair

- COO half (2.0.0_SA_COO~P2): UNSIGNED. This packet does not sign it.
- CTO half (1.0.0_SA_CTO~DELL2): UNSIGNED. This packet does not sign it.

Both halves must be signed against the plan's bytes before any chunk runs. The COO and CTO must also rule on the premises that failed here, which are listed in the surprise channel rows.

## What this census did not measure

- The per-account earliest positive-value day, which the producer reads from object bodies.
- The wall time of a 25-day chunk with the lots stage, or whether the lots stage amortizes across days.
- The class and lot partition counts, and their version history.
- The invoker's identity and the Lambda resource policy.
- The live Scheduler schedule (EventBridge Scheduler, not an events rule).
- Any source of cottonwood or inflection. Their demand is null.
- Whether the activity rows are correct. The census measured counts and dates only.
- The DEV after-read.
