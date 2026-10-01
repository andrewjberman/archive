# ANNOUNCE -- NFRA_MCPINDEX MX-s-16 PHASE A, RE-ISSUED under amendment A1 (0.9.0_WK_NFRA_MCPINDEX~24)

Worktree branch `wk-nfra_mcpindex-6-24`, merged with CLOUD `0de93e672c` (carries A1). Push state: LOCAL (nothing pushed).
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

## 3. Saved Terraform plan (targeted, never applied) -- unchanged

`infra/aws/terraform/bd-pipeline`; files `mx-s-16.plan.txt` (tracked), `mx-s-16.tfplan` (gitignored, this worktree).
Negative control: `No changes`. With the edits: `Plan: 0 to add, 5 to change, 0 to destroy.` 4 rules `ENABLED -> DISABLED`;
`bd_data_bucket` in place, `ProcessAllocationFiles` block removed; no destroy. The plan covers all four rules, so a
subset GO needs the plan re-cut to exclude the held rules (item 4 below).

## 4. Documents -- unchanged

The four `infra/aws/ssm/opal-bd-*-download.json` are rewritten on the branch as a one-step no-op, NOT published. Live
versions: transaction 3, realized 3, unrealized 3, allocation 5 (Default == Latest). Since MX-s-14 the documents run
Success on 09-29 and 09-30 (download stripped) but still run the stale merge, which on those two days found "No new ...
files to process".

## 5. RE-PLAN PER KEY (A1 item 2) AND RECOMMENDATION

| key | plan | basis |
|---|---|---|
| unrealized | STANDS: DS leg first, then publish no-op document, disable `bd-unrealized-pipeline-trigger` | no sentinel dependence; 0 partitions added or removed |
| allocations | STANDS: publish no-op document, disable `bd-allocation-pipeline-trigger`, remove `ProcessAllocationFiles` block | 4 of 4 snapshot landings on sentinel days; 131 of 131 coverage |
| transactions | **(c) RETIRE, accepting the lag** (recommended) | the document's gap-day write is an empty placeholder on 8 of 8; real rows land on sentinel days either way; served-content DELTA 0 |
| realized | **(b) HOLD this round, cause carried to L10** (recommended), with **(a)** as the carried leg | the document is the only same-day real-rows writer on 9 of 9 gap dates; (c) costs +26.5 h every Monday, +2.5 h every Tuesday |

**Recommendation: split. Retire transactions now; HOLD realized.** The documents and rules are independent keys, so
this is separable.
- **Served-freshness consequence of retiring transactions (c):** none in content. An empty partition for a gap date
  appears at the next sentinel (24-72 h) instead of 21:54Z that day; real transaction rows land when the overlapping
  chunk re-pull is merged on a sentinel day, which today's document does not accelerate. UNMEASURED: whether a consumer
  tests that partition's existence.
- **Served-freshness consequence of holding realized (b):** none; today's behaviour stands. Realized and transactions
  keep two writers (AC1 refused as written for realized, 3 of 4 tables with 1 writer), carried to the round-6 slug with
  the cause in 0.2.
- **Why not (c) for realized:** `silver/realized/<D>.parquet` for a Monday run date would appear ~48 h after landing
  instead of ~21.6 h (measured, n=9 above); +26.5 h on served realized every Monday.
- **Why not (a) in this order:** the fix is a one-predicate change in the SHARED script
  `data/cot/scripts/bronze/cot_bronze_ingest.py` (`emit_bronze_sentinel`/`_table_complete`: accept a MEASURED
  `has_data_rows=0` sidecar for a PERIOD table such as transactions, keep the `>=1 row` rule for the snapshot tables the
  2026-07-09 ruling protects). That file is under `data/cot/` and outside this order's `<paths>`; it is shared with cot,
  so it must be table-scoped; it deploys as a DS leg to `code/bronze/`. Its negative control is a snapshot table with 0
  rows still refused. After it lands, the first sentinel on a Monday/Tuesday (next: 10-05, 10-06 00:0xZ) is the proof, and
  only then does the realized document's retirement carry DELTA 0 on timing as well. This is the round-7 enrichment.
  An alternative lives in the runner (exclude an empty PERIOD table from `landed` before the call), also outside
  `<paths>` (`infra/aws/lambda/...`, Terraform-deployed).
- Retiring both under (c) is a legal choice for the issuer: the transactions half is costless, the realized half is the
  +26.5 h.

**If the issuer takes the split:** the saved plan must be re-cut or applied with `-target` limited to
`bd_unrealized_pipeline_trigger`, `bd_allocation_pipeline_trigger`, `bd_transaction_pipeline_trigger` and the notification;
`bd_realized_pipeline_trigger` stays ENABLED and the realized document stays version 3. That re-cut is a Phase B act and
was NOT run here (no plan, no apply under A1).

DELTA and rollback per key (unchanged except as above): transactions, SSM `opal-bd-transaction-download` v4 /
`bd-transaction-pipeline-trigger`, rollback = default back to 3, rule ENABLED; unrealized and allocations as in the first
issue (allocations: default back to 5, rule ENABLED, re-add the notification block and re-plan; unrealized: default back to
3, rule ENABLED, re-deploy prior script bytes). Ledger `nfra-mcpindex-r6-bd-merge-retire` opens only on a GO; AC3 reads an
OPEN ledger as FAIL, so close it in the same session. Any act outside 21:30-22:15Z and 00:00-00:30Z.

## 6. Baseline of the order's checks at this base (from the first issue, not re-run)

s16.AC1 FAIL (0 of 4; transactions 2, realized 2, unrealized 2, allocations 3 writers); s16.AC2 PASS (3 of 3 clean
newest runs; unrealized `failures=6` printed, ungraded); s16.AC3 FAIL (no entry; scan denominator 18 of 18).
Grading under A1: if realized is held, AC1 is REFUSED as written for realized with this measurement.

## 7. Open for the issuer

1. Take the split (transactions retire under (c), realized HOLD under (b)), hold both, or retire both under (c).
2. Route the producer fix (0.2, item "Why not (a)") as a round-7 DS leg or a runner change; neither is in this order's paths.
3. Whether the 6 empty `silver/unrealized/2026-07-0x` partitions stay (they do under this plan).
4. Rows to disposition before GO: Z-W24-S2 (BLOCKING, ARMED), S4 (cause), S5 (runner log), S6 (test contamination).
