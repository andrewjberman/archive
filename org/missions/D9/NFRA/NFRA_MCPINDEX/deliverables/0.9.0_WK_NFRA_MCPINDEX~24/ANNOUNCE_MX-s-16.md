# ANNOUNCE -- NFRA_MCPINDEX MX-s-16 PHASE A, RE-ISSUED under amendment A2 (per-key ruling; supersedes the A1 re-plan; sections 0-2 are the A1 measurements, unchanged) (0.9.0_WK_NFRA_MCPINDEX~24)

Worktree branch `wk-nfra_mcpindex-6-24`, merged with CLOUD `fbc1afdecc` (carries A1 and A2). Push state: LOCAL (nothing pushed).
Re-issue measured 2026-10-01 ~09:55-10:45Z, read-only: S3 list/head/get on `opal-data-bd`, CloudWatch filter-log-events,
`aws events describe-rule`, `ssm list-commands`. No publish, no apply, no ledger, no S3 write, no SSM document version,
no Lambda invoke. Every read ran outside 21:30-22:15Z and 00:00-00:30Z.

Rows filed: Z-W24-S1..S3 (first issue), and under A1 `NFRA_MCPINDEX-Z-W24-S4` (the cause), `-S5` (runner log says
"emitted" after the shared module said "NOT emitted"), `-S6` (census contamination by MX-s-14 test runs). Row S2
(BLOCKING, ARMED) is unchanged: this document supplies the diagnosis the issuer asked for.

## 0. A1 DIAGNOSIS -- why `bronze/<date>/_BRONZE_COMPLETE.json` is absent on the gap dates

### 0.1 The producer chain (read from code and rules, live)

| link | what it is | evidence |
|---|---|---|
| `bd-49f-session-daily` | EventBridge `cron(0 0 * * ? *)`, ENABLED, EVERY day (not weekday-limited) | `aws events describe-rule` |
| `bd-49f-session-trigger` | session-refresh; with the cookie live it skips the mint and invokes `bd-49f-runner` async at 00:00:18Z (`Lever A: cookie POSITIVE-live ... direct-invoke`, status=202) | its logs: runner invoked 14 of 14 retained days (09-18..10-01); Lever A skip-mint on 13 of 14, 09-28 took the mint path |
| `bd-49f-session-complete` | EventBridge on SSM `opal-bd-49f-session-fetch` Success; only the mint path (not used while the cookie is live) | `describe-rule` pattern |
| `bd-49f-runner` | pulls transactions (5 x 3-day chunk sweep), allocations, realized, unrealized to `forwardfill_v2/`, then calls `mod.emit_bronze_sentinel(run_date, landed)` | `infra/aws/lambda/bd-pipeline/bd-49f-runner/lambda_function.py:181-189` |
| the WRITER of the sentinel | `emit_bronze_sentinel` in the shared script, deployed to `code/bronze/`: head_object each table, then `_table_complete()` = the completeness sidecar must say `has_data_rows == 1`; any table failing it makes the function print `WARN: bronze sentinel NOT emitted` and RETURN with nothing written | `data/cot/scripts/bronze/cot_bronze_ingest.py:1328-1370` and `:632-662` @92518d0d86 |
| `opal-assets-bd49f-daily-pull` rules | not the sentinel's producer (opal-assets TF root; fees/insurance legs). Not in the sentinel path: the session-trigger routes `main` to bd-49f-runner and `insurance` to opal-assets-bd49f-reporting-pull (04:35Z) | `bd-49f-session-trigger/lambda_function.py:60-75`; its 04:35Z log lines |

### 0.2 The cause (named from the producer's own log and code, not from the date pattern)

On a gap date the runner's NEWEST 3-day transactions window returns **0 data rows**. The ingest deliberately lands it
(`WARN: transactions @D export has 0 data rows (4356 bytes) -- PERIOD table, an empty increment is legitimate over a
non-trading window; landing.`) and writes a sidecar with `has_data_rows=0`. The sentinel writer then applies the
snapshot-table content rule (the CTO 2026-07-09 fix for header-only allocations stubs) to that PERIOD table and refuses:

> `WARN: bronze sentinel NOT emitted -- 1 object(s) present but NOT content-complete (no sidecar attesting >=1 data row): forwardfill_v2/transactions/TRANSACTIONS_DAILY_<D>.xlsx. Silver will NOT be advanced on unverified content`

Verbatim from the runner logs, run_date 2026-09-21 (00:06:57Z), 09-22 (00:11:55Z), 09-28 (00:10:21Z), 09-29 (00:08:13Z);
4 of 4 gap dates inside the 14-day log retention. Nothing failed: `RESULT ... 'failed': [], 'auth_dead': False` on all four.
Two producers disagree on one fact: the ingest says an empty period increment is legitimate and lands it; the sentinel
writer treats the same empty increment as an unverified stub. Silver is withheld by the second.

For the 5 gap dates older than the log retention (09-07, 09-08, 09-09, 09-14, 09-15; the log group keeps 14 days, first
retained event 09-18) the SAME decisive input is still readable: S3 is versioned, and the FIRST version of
`forwardfill_v2/transactions/_complete/<D>.json` is the sidecar the sentinel writer read at run time.

### 0.3 The sentinel table (every date 2026-09-03..2026-10-01, 29 days; first-version sidecar read from S3 versions)

Columns: sentinel object (LastModified UTC) | transactions sidecar at first write (`has_data_rows`, bytes) | producer evidence.
Dates in the retained window carry the runner's own line; older dates carry the sidecar only.

| date | dow | sentinel | txn first sidecar | producer evidence |
|---|---|---|---|---|
| 09-03 | Thu | 00:11:26Z | 1 / 8,473,619 | sidecar rows>=1 (log expired) |
| 09-04 | Fri | 00:11:14Z | 1 / 1,075,052 | same |
| 09-05 | Sat | 00:11:32Z | 1 / 18,956,501 | same |
| 09-06 | Sun | 00:13:22Z | 1 / 32,132,430 | same (4 tables landed) |
| **09-07** | Mon | **absent** | **0 / 4,355** | sidecar rows=0 (log expired); US holiday |
| **09-08** | Tue | **absent** | **0 / 4,355** | sidecar rows=0 (log expired) |
| **09-09** | Wed | **absent** | **0 / 4,355** | sidecar rows=0 (log expired) |
| 09-10 | Thu | 00:10:29Z | 1 / 1,466,472 | sidecar rows>=1 |
| 09-11 | Fri | 00:08:03Z | 1 / 872,636 | same |
| 09-12 | Sat | 00:10:48Z | 1 / 3,859,756 | same |
| 09-13 | Sun | 00:13:01Z | 1 / 699,880 | same (4 tables) |
| **09-14** | Mon | **absent** | **0 / 4,357** | sidecar rows=0 (log expired) |
| **09-15** | Tue | **absent** | **0 / 4,354** | sidecar rows=0 (log expired) |
| 09-16 | Wed | 00:07:56Z | 1 / 1,356,306 | sidecar rows>=1 |
| 09-17 | Thu | 00:09:40Z | 1 / 13,915,852 | same |
| 09-18 | Fri | 00:09:29Z | 1 / 3,892,450 | log: `OK: bronze sentinel ... (tables=2, content-verified)` |
| 09-19 | Sat | 00:07:26Z | 1 / 2,558,981 | log: OK, content-verified |
| 09-20 | Sun | 00:10:51Z | 1 / 12,029,668 | log: OK (tables=4) |
| **09-21** | Mon | **absent** | **0 / 4,356** | log 00:06:57Z: `WARN: bronze sentinel NOT emitted ... TRANSACTIONS_DAILY_2026-09-21.xlsx` |
| **09-22** | Tue | **absent** | **0 / 4,356** | log 00:11:55Z: WARN NOT emitted ... `_2026-09-22.xlsx` |
| 09-23 | Wed | 00:07:15Z | 1 / 995,007 | log: OK (tables=2) |
| 09-24 | Thu | 00:08:43Z | 1 / 14,599,781 | log: OK |
| 09-25 | Fri | 00:09:21Z | 1 / 1,452,839 | log: OK |
| 09-26 | Sat | 00:08:58Z | 1 / 6,946,332 | log: OK |
| 09-27 | Sun | 00:11:40Z | 1 / 2,102,770 | log: OK (tables=4) |
| **09-28** | Mon | **absent** | **0 / 4,356** | log 00:10:21Z: WARN NOT emitted ... `_2026-09-28.xlsx` |
| **09-29** | Tue | **absent** | **0 / 4,355** | log 00:08:13Z: WARN NOT emitted ... `_2026-09-29.xlsx` |
| 09-30 | Wed | 00:08:54Z | 1 / 2,097,543 | log: OK (tables=2) |
| 10-01 | Thu | 00:11:05Z | 1 / 29,856,727 | log: OK (tables=2) |

Denominator: 29 dates; 20 with a sentinel, 9 without. **9 of 9 sentinel-less dates have a first-write transactions
sidecar with `has_data_rows=0`; 0 of 20 sentinel dates do.** Realized sidecars are `has_data_rows=1` on 29 of 29 dates
(realized never blocks). Allocations and unrealized are not in the sentinel list on most days (`rejected`, header-only
snapshot) and do not block it (`failed: []`, rejects do not count as failures).
Why the newest window is empty on exactly Mon, Tue (and Wed after a Monday holiday) is INFERRED, not measured: the same
dates re-pulled by later overlapping chunks carry real rows (silver 09-21: 35,269 B at 09-23, 248,885 B at 09-24;
09-22: 2,988,821 B at 09-25), so BD appears to post a trading day's transactions about two days late, leaving a
Sat..Mon / Sun..Tue window empty at 00:0xZ. The measured fact needing no inference is the sidecar.

### 0.4 What the missing sentinel costs (silver written same day by the document vs next sentinel by bd-silver-merge)

bd-silver-merge fires only on a sentinel (S3 event) and then merges every new input, so a gap date's inputs wait for
the NEXT sentinel. Gap-date table (UTC; "now" = the document's silver write; "no-doc" = the next merge write):

| gap date | dow | realized bronze landed | document silver write | bd-silver-merge silver write (next sentinel) | lag now (h) | lag no-doc (h) | extra (h) |
|---|---|---|---|---|---|---|---|
| 09-07 | Mon (holiday) | 00:09 | 09-07 21:46 | 09-10 00:21 | 21.6 | 72.2 | +50.6 |
| 09-08 | Tue | 00:09 | 09-08 21:46 | 09-10 00:21 | 21.6 | 48.2 | +26.6 |
| 09-09 | Wed | 00:07 | 09-09 21:46 | 09-10 00:21 | 21.6 | 24.2 | +2.6 |
| 09-14 | Mon | 00:08 | 09-14 21:46 | 09-16 00:17 | 21.6 | 48.1 | +26.5 |
| 09-15 | Tue | 00:08 | 09-15 21:46 | 09-16 00:17 | 21.6 | 24.1 | +2.5 |
| 09-21 | Mon | 00:06 | 09-21 21:46 | 09-23 00:11 | 21.7 | 48.1 | +26.4 |
| 09-22 | Tue | 00:11 | 09-22 21:46 | 09-23 00:11 | 21.6 | 24.0 | +2.4 |
| 09-28 | Mon | 00:10 | 09-28 21:46 | 09-30 00:15 | 21.6 | 48.1 | +26.5 |
| 09-29 | Tue | 00:07 | (slot a no-op, see row S6) | 09-30 00:15 | n/a | 24.1 | +2.5 est. |

**Measured lag distribution if the realized document is retired (c), n=9 gap dates, hours from bronze landing to
silver:** 24.0, 24.1, 24.1, 24.2, 48.1, 48.1, 48.1, 48.2, 72.2 (median 48.1). Baseline on the 20 sentinel dates: 1.8 to
10.7 minutes (median 3.3 min). Extra vs today: +2.4..+2.6 h on 4 Tue/Wed dates, +26.4..+26.6 h on 4 Mon/Tue dates,
+50.6 h on the holiday Monday. Every Monday run date is +26.5 h; every Tuesday +2.5 h.

**Transactions are a different case.** On every gap date the document's transactions write is an EMPTY placeholder:
silver/transactions/<D>.parquet first version = 34,882 B at 21:54Z on 8 of 8 document-written gap dates (09-07, 08, 09,
14, 15, 21, 22, 28); bd-silver-merge's first write at the next sentinel is the same empty shape (35,269 B, 9 of 9); the
REAL rows land later, by the overlapping chunk re-pull, through the merge on a SENTINEL day (e.g. 09-08: 330,823 B on
09-11; 09-15: 2,890,918 B on 09-18). The document adds no content and no real-row timing to transactions; retiring it
only removes an empty partition for up to 24-72 h. Whether any consumer checks existence of that empty partition was
not traced (UNMEASURED).

Not traced either: when gold/served reads silver/realized relative to 21:46Z (the "D_02 EC2 chain"), so the served
consequence below is stated at the SILVER plane only.

## 1. Census (applied plane; the last 10 document runs 2026-09-17..09-30 per leg, bd-silver-merge 20 days = 10 invocations)

| table | writers today (s16.AC1 live: 0 of 4 tables with 1 writer) | document inputs processed (last 10 runs) | also processed by bd-silver-merge |
|---|---|---|---|
| transactions | document + bd-silver-merge | 3 (TRANSACTIONS_DAILY 09-21, 09-22, 09-28), each written as a **0-row** partition at 21:54Z | 3 of 3 (later the real rows, per 0.4) |
| realized | document + bd-silver-merge | 3 (REALIZED_DAILY 09-21, 09-22, 09-28), real rows 9,330 / 9,350 / 11,298 | 3 of 3, same rows |
| unrealized | document + bd-silver-merge | 48 = the same 6 empty stubs (07-03..07-07, 07-09) x 8 runs, each a 0-row partition | 0 of 6 (row Z-S72) |
| allocations | document + bd-silver-merge + bd-allocation-processor | 0 | n/a; processor ran twice in 60 days and bd-silver-merge re-wrote both keys 2-3 min later |

Allocation coverage proof: `forwardfill_v2/allocations/` holds 131 xlsx; the merge manifest holds 131 processed_etags;
131 of 131 current etags equal the recorded etags; 0 xlsx missing.
**Unrealized and allocations do not depend on the sentinel gap (A1 item 2):** in the 29-day window the snapshot
landings (allocations and unrealized `_complete` sidecars) are 4 of 4 on Sundays 09-06, 09-13, 09-20, 09-27, and all four
Sundays carry a sentinel (the 4-table runs), so bd-silver-merge sees every real snapshot input. Their plan stands.

## 2. Z-S72 diagnosis (unchanged from the first issue)

- **Why the 6 fail:** the six source files `forwardfill_v2/unrealized/UNREALIZED_DAILY_2026-07-{03,04,05,06,07,09}.xlsx`
  are 3,745-3,748 byte empty templates: Sheet1 has 15 columns and **0 data rows**. The current script's
  `process_unrealized_xlsx_to_parquet` deliberately SKIPs a 0-row file (ADVI_BREAKS TO-3) and returns `(None, 0)`;
  `incremental_unrealized_merge` counts every `None` as a failure and never records the etag, so the file is NEW again
  next run (`SUMMARY: 6 processed | new=6 ... | failures=6 | rows_added=0`). A mislabelled skip, not a read error.
- **Why the document wrote them:** the document runs the STALE script `s3://opal-data-bd/scripts/merge-daily-incremental.py`
  (43,492 B, 2026-06-29; no empty-stub skip, no etag manifest) and writes six 8,016-byte 0-row partitions each cycle.
- **Are they correct?** They faithfully mirror empty sources; contrary to TO-3 but they shadow nothing. They stay.
- **Source fix (in `<paths>`, committed, NOT deployed):** `data/black_diamond/scripts/silver/merge-daily-incremental.py`
  returns an `_EMPTY_STUB` sentinel for a 0-row file, records the etag, writes no partition, counts no failure, prints
  `empty_stub=N`. Offline harness: run 1 `failures=0 rows_added=0 empty_stub=2`; run 2 `No new or re-landed ... skip=2`.
- **DS deploy leg (separate act, `.tools/safe-deploy.sh`):** that file -> `s3://opal-data-bd/code/silver/merge-daily-incremental.py`
  (today md5 `c54d07908c69e2d9a9035050e0367f40`, 59,077 B). Rollback: re-deploy `git show f797d8594a:<that path>`.

## 3. Saved Terraform plan -- RE-CUT under A2 (never applied)

`infra/aws/terraform/bd-pipeline`; `TF_DATA_DIR` = the worktree's `.scratch/tfdata`, `-lock=false`, `-input=false`, state
read-only; the same method as the first plan, with `-target` now limited to FOUR resources:
`aws_s3_bucket_notification.bd_data_bucket`, `aws_cloudwatch_event_rule.bd_unrealized_pipeline`,
`aws_cloudwatch_event_rule.bd_transaction_pipeline`, `aws_cloudwatch_event_rule.bd_allocation_pipeline`.
`bd_realized_pipeline` is NOT a target and its `state = "ENABLED"` line is restored on the branch (the diff of
`eventbridge.tf` against CLOUD carries 0 realized lines).

- **Summary line, verbatim:** `Plan: 0 to add, 4 to change, 0 to destroy.`
- 3 rules `state "ENABLED" -> "DISABLED"` (unrealized, transaction, allocation); `bd_data_bucket` updated in place.
  The notification diff prints as index shifts across three `lambda_function` blocks; the net is the
  `ProcessAllocationFiles` block removed, `GoldLayerPricesTrigger` and `BronzeCompleteSilverMerge` unchanged,
  `eventbridge = true` unchanged. No destroy. The processor, its lambda permission, and the rules' targets and
  permissions stay.
- Files: `mx-s-16.plan.txt` (tracked render; sha256 `eef7b17d3f224611ea864bc1ee532cc4b954c8c8bc096329bfcf924180c49a69`);
  `mx-s-16.tfplan` (binary, gitignored `**/*.tfplan`, local to this worktree, 182,235 B).
- **Plan binary sha256: `af1537fdf47099c50f47c7d16d1e95afc1705591d949a728bedfed2b5fc1e214`.** It replaces the
  5-resource A1 plan (moved aside to `.scratch/`, also local). The 5-resource plan must not be applied.
- The negative control from the first issue still stands (same targets before the edits: `No changes`).

## 4. Documents (branch state, NOT published) and live state

The unrealized, transaction and allocation documents (`infra/aws/ssm/opal-bd-{unrealized,transaction,allocation}-download.json`)
are one-step no-ops on the branch. **`opal-bd-realized-download.json` is restored to the CLOUD bytes** (the no-op
rewrite is reverted, HOLD).

Live at about 10:17Z 2026-10-01 (read-only):
- `describe-document` DefaultVersion / LatestVersion: transaction 3 / 3, unrealized 3 / 3, allocation 5 / 5, realized 3 / 3.
- `describe-rule`: all four trigger rules ENABLED.
- `get-bucket-notification-configuration` lambda IDs: ProcessAllocationFiles, GoldLayerPricesTrigger, BronzeCompleteSilverMerge.
- Served `code/silver/merge-daily-incremental.py`: ETag/md5 `c54d07908c69e2d9a9035050e0367f40`, 59,077 B, VersionId
  `gDNvsypwihDy3Rd6KfZ0CosUiD.MM3ma`, LastModified 2026-07-02T20:49:25Z. These are the bytes of CLOUD's copy; the branch
  fix is md5 `91eaf2486fc56ece76db2f0d862096f7`.

## 5. THE A2 PER-KEY PLAN

PHASE B runs only on the issuer's GO after both halves. Every act is outside 21:30-22:15Z and 00:00-00:30Z.

### unrealized (GO, DS leg first)

1. **DS deploy leg.** `.tools/safe-deploy.sh` of `data/black_diamond/scripts/silver/merge-daily-incremental.py` to
   `s3://opal-data-bd/code/silver/merge-daily-incremental.py` (S3 cp + SHA verify). If safe-deploy refuses the worker
   serial (the DS lane), file a BLOCKING row naming the refusal and STOP this key; the issuer routes the leg to a DS seat.
2. **Document retire.** Publish the no-op `opal-bd-unrealized-download` as the next version (v4 at today's read), set
   DEFAULT, read back Default == Latest; `bd-unrealized-pipeline-trigger` ENABLED -> DISABLED (saved plan).
- **Expected served DELTA: 0.** No partition added or removed, no row changed: the six
  `silver/unrealized/2026-07-0{3,4,5,6,7,9}.parquet` 0-row partitions (8,016 B each) stay, and the document's only writes were
  those same six. The visible effect is `bd-silver-merge` unrealized `failures=6` reading `failures=0 ... empty_stub=6`
  on its next sentinel run, with the six etags recorded.
- **Rollback:** the script: re-deploy the prior bytes (S3 VersionId `gDNvsypwihDy3Rd6KfZ0CosUiD.MM3ma`, md5 `c54d0790...`,
  or `git show f797d8594a:data/black_diamond/scripts/silver/merge-daily-incremental.py`); the document: default back to 3;
  the rule: ENABLED (revert the `state` line and `safe-apply`, ledger-recorded).

### allocations (GO)

Publish the no-op `opal-bd-allocation-download` (v6 at today's read), set DEFAULT, Default == Latest;
`bd-allocation-pipeline-trigger` DISABLED; the `ProcessAllocationFiles` block removed (all by the saved plan except the
document).
- **Expected served DELTA: 0.** `bd-silver-merge` already holds every input: 131 of 131 current etags equal the manifest
  etags, 0 xlsx missing. The processor's `bd-price-update` invoke (2 in 60 days) stops; the transactions merge still
  invokes it.
- **Rollback:** document default back to 5; rule ENABLED; re-add the block in `s3-notifications.tf` and re-plan/apply.

### transactions (GO on one precondition, option (c))

1. **Read-only consumer trace FIRST.** Question: does any consumer key on the same-day existence of
   `s3://opal-data-bd/silver/transactions/<date>.parquet`? Instruments: `comp-estate --resource silver/transactions`;
   `comp-pipescript io` on each bd gold script that reads it; the gold/served readers; `comp-freshness` entries naming it.
   A hit is a reader that needs the partition for a given date to exist (not a latest-available read). Writes nothing.
2. **Only if 0 hits: retire.** Publish the no-op `opal-bd-transaction-download` (v4 at today's read), set DEFAULT, Default
   == Latest; `bd-transaction-pipeline-trigger` DISABLED (saved plan).
3. **If any hit:** file a BLOCKING row naming the consumer and HOLD transactions. The saved plan then holds a rule that
   must not move, so it is NOT applied as saved: re-cut a 3-resource plan (`bd_unrealized_pipeline`,
   `bd_allocation_pipeline`, the notification) first and report its sha256.
- **Expected served DELTA: content 0.** On gap days the document writes only an empty 34,882 B placeholder (8 of 8); real
  rows land on sentinel days either way. What moves: that empty partition's existence, from 21:54Z the same day to the
  next sentinel (24-72 h, table in 0.4).
- **Rollback:** document default back to 3; rule ENABLED.

### realized (HOLD this round)

No act: the realized document stays v3 and `bd-realized-pipeline-trigger` stays ENABLED. **Expected served DELTA: 0**
(nothing changes). Carried to the round-6 slug with the producer fix (section 7, item 2).

### Apply order and acceptance

One `safe-apply` of the saved plan (3 rules plus the notification move together), AFTER the DS leg and the transactions
trace, then the three document publishes. Nothing is deleted.
- s16.AC1 is REFUSED as written for realized (2 writers by design this round); the other 3 tables must read 1 writer.
- s16.AC2: the next scheduled `bd-silver-merge` run clean on 3 of 3 graded tables (unrealized printed).
- s16.AC3: entry at HEAD, sentinel removed, nothing OPEN/HELD.
- The ledger `nfra-mcpindex-r6-bd-merge-retire` opens only on the GO, naming BOTH the entry and the `.open_deploys/`
  sentinel paths, and closes in the same session.

### BASE-MOVED CLAUSE (applies at the GO, before any act)

This ANNOUNCE is a snapshot at about 10:17Z 2026-10-01. At the GO, re-read:
1. each SSM document's `DefaultVersion` and `LatestVersion` (today: transaction 3/3, unrealized 3/3, allocation 5/5,
   realized 3/3), and set each new version number from that read;
2. each trigger rule's `State` and schedule (today: four ENABLED) and the bucket notification IDs (today: three);
3. the served script's ETag (today `c54d0790...`) and the bucket's `eventbridge` flag.
If any differs, the saved plan is stale: re-cut it with the same four-target command and re-issue its sha256 before
apply. Terraform refuses a stale saved plan at apply, but an SSM document-version drift is not a Terraform fact, so the
document read is the guard for it.

## 6. Baseline of the order's checks (first issue, not re-run)

s16.AC1 FAIL (0 of 4; transactions 2, realized 2, unrealized 2, allocations 3 writers); s16.AC2 PASS (3 of 3 clean
newest runs; unrealized `failures=6` printed, ungraded); s16.AC3 FAIL (no entry; scan denominator 18 of 18). Under A2,
AC1 is expected to read 3 of 4 with realized refused.

## 7. Open for the issuer / carried

1. Both never-widen halves on the A2 per-key plan (the GO).
2. Route the realized producer fix (0.2, "Why not (a)": a table-scoped accept of a MEASURED `has_data_rows=0` for the
   transactions PERIOD table in `data/cot/scripts/bronze/cot_bronze_ingest.py`) to the round-6 slug; the realized
   retirement waits on its proof (the first Monday/Tuesday sentinel after it lands).
3. Rows carried: Z-W24-S2 (BLOCKING, ARMED; cause supplied in 0.2), S4 (cause), S5 (the runner prints "OK ... emitted"
   after the module said "NOT emitted"), S6 (test contamination), S7 (merge committed outside safe-commit; INERT).
4. The 6 empty `silver/unrealized/2026-07-0x` partitions stay under this plan.
