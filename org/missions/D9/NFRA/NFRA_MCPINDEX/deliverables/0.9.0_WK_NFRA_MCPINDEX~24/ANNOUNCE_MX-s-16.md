# ANNOUNCE -- NFRA_MCPINDEX MX-s-16 PHASE A (0.9.0_WK_NFRA_MCPINDEX~24)

Worktree branch `wk-nfra_mcpindex-6-24`, base CLOUD `f797d8594a`. Measured 2026-10-01 ~09:15-09:50Z. Push state: LOCAL (nothing pushed).
PHASE A only: no publish, no apply, no ledger, no S3 write, no SSM document version. Preflight: the four trigger rules
fire 21:38/21:45/21:53/22:00Z MON-FRI and bd-silver-merge fires on `_BRONZE_COMPLETE.json` (~00:08-00:15Z); every read
here ran at ~09:15-09:50Z, outside 21:30-22:15Z and 00:00-00:30Z. `comp-schedule` is the gate ledger, not a job
schedule, so the rules were read live with `aws events describe-rule` (all four ENABLED, crons as above).

**Rows filed:** `NFRA_MCPINDEX-Z-W24-S1` (AC1 reads document content, so the plan does both options), `-S2` (BLOCKING,
ARMED: the documents are the only same-day writer on sentinel-less days), `-S3` (documents run a stale script copy).

## 1. Census (applied plane; the last 10 document runs 2026-09-17..09-30 per leg, bd-silver-merge 20 days = 10 invocations)

| table | writers today (s16.AC1 live: 0 of 4 tables with 1 writer) | document inputs processed (last 10 runs) | also processed by bd-silver-merge |
|---|---|---|---|
| transactions | document + bd-silver-merge | 3 (TRANSACTIONS_DAILY 09-21, 09-22, 09-28), each written as a **0-row** partition at 21:54Z | 3 of 3: 09-21 and 09-22 on 09-23 00:07Z, 09-28 on 09-30 00:08Z; later runs replaced the 0-row partitions with real rows (52,776 / 3,967 / 7,643) |
| realized | document + bd-silver-merge | 3 (REALIZED_DAILY 09-21, 09-22, 09-28), real rows 9,330 / 9,350 / 11,298 | 3 of 3, same rows: 09-21 and 09-22 on 09-23 00:07Z, 09-28 on 09-30 00:15Z |
| unrealized | document + bd-silver-merge | 48 = the same 6 empty stubs (UNREALIZED_DAILY 07-03..07-07, 07-09) x 8 runs, each a 0-row partition | 0 of 6: bd-silver-merge reads each as NEW every night and writes nothing (row Z-S72) |
| allocations | document + bd-silver-merge + bd-allocation-processor | 0 (no new allocation file in 10 runs) | n/a; processor ran twice in 60 days (09-20 00:10Z for 09-18, 09-27 00:11Z for 09-25) and bd-silver-merge re-wrote both keys 2-3 min later |

Allocation coverage proof (the order's gate for the processor): `forwardfill_v2/allocations/` holds 131 xlsx; the merge
manifest holds 131 processed_etags; 131 of 131 current etags equal the recorded etags; 0 xlsx missing.
bd-silver-merge therefore processes every allocation input the processor does. `silver/allocations/2026-09-18.parquet`
(LastModified 09-20 00:12:59Z) and `2026-09-25.parquet` (09-27 00:14:56Z) are the merge's writes, after the processor's.

Sentinel gap (row Z-W24-S2): `bronze/<date>/_BRONZE_COMPLETE.json` is absent for 09-07..09-09, 09-14, 09-15, 09-21, 09-22,
09-28, 09-29; bd-silver-merge did not run on those days; the document was the only same-day writer.

## 2. Z-S72 diagnosis

- **Why the 6 fail:** the six source files `forwardfill_v2/unrealized/UNREALIZED_DAILY_2026-07-{03,04,05,06,07,09}.xlsx`
  are 3,745-3,748 byte empty templates: Sheet1 has 15 columns and **0 data rows** (read locally with pandas; Timestamps
  sheet Start Date 6/19..6/25/2026). The current script's `process_unrealized_xlsx_to_parquet` deliberately SKIPs a
  0-row file (the ADVI_BREAKS TO-3 ruling: never write an empty partition that could shadow the last good one) and
  returns `(None, 0)`; `incremental_unrealized_merge` counts every `None` as a failure and never records the etag, so
  the file is NEW again next run. Lambda line, every run: `SKIP: ... 0 data rows ... not writing an empty silver
  partition` then `SUMMARY: 6 processed | new=6 ... | failures=6 | rows_added=0`. It is a **mislabelled skip, not a
  read or schema error**; the invocation still returns ok (failures do not raise).
- **Why the document wrote them:** the document runs the STALE script `s3://opal-data-bd/scripts/merge-daily-incremental.py`
  (43,492 B, 2026-06-29), which has no empty-stub skip and no etag manifest. Each cycle the Lambda's 00:1xZ manifest
  write resets `processed_files` to its 68 etag keys; the next 21:39Z document run sees 6 "new" files and writes 6 x
  8,016-byte 0-row partitions (`silver/unrealized/2026-07-0{3,4,5,6,7,9}.parquet`, LastModified 09-30 21:39Z). The
  document logs show the ping-pong: "Previously processed" 68 (09-28), 74 (09-29), 68 (09-30). Current manifest:
  processed_files 68, processed_etags 68, daily_partitions 74.
- **Are the 0-row partitions correct?** They faithfully mirror empty source files (no data lost: the dates 07-03..07-07
  and 07-09 have no data anywhere), but they are contrary to the TO-3 ruling and are written only by the stale script.
  They are not the newest partitions (newest is 2026-09-25), so they shadow nothing. They stay (nothing is deleted).
- **Source fix (in `<paths>`, committed on the branch, NOT deployed):**
  `data/black_diamond/scripts/silver/merge-daily-incremental.py` -- `process_unrealized_xlsx_to_parquet` returns an
  `_EMPTY_STUB` sentinel for a 0-row file; `incremental_unrealized_merge` records the etag, writes no partition, does not
  count a failure, and prints `empty_stub=N`. A later re-land with data changes the etag and is reprocessed. Offline
  harness (boto3 helpers stubbed, the real stub files): run 1 `failures=0 rows_added=0 empty_stub=2`, 0 partitions, 2
  etags recorded, upload never called; run 2 `No new or re-landed ... skip=2`.
- **DS deploy leg (separate act, `.tools/safe-deploy.sh`):** `data/black_diamond/scripts/silver/merge-daily-incremental.py`
  -> `s3://opal-data-bd/code/silver/merge-daily-incremental.py` (the key bd-silver-merge loads; today md5
  `c54d07908c69e2d9a9035050e0367f40`, 59,077 B). Rollback: re-deploy `git show f797d8594a:<that path>`.

## 3. Saved Terraform plan (targeted, never applied)

`infra/aws/terraform/bd-pipeline`, `TF_DATA_DIR` in the worktree `.scratch`, `-lock=false`, state read-only.
Files: `mx-s-16.plan.txt` (tracked), `mx-s-16.tfplan` (binary, gitignored `**/*.tfplan`, local to this worktree).
Targets: `aws_s3_bucket_notification.bd_data_bucket` and the four `aws_cloudwatch_event_rule.bd_{unrealized,realized,transaction,allocation}_pipeline`.
- **Negative control** (same targets, edits not yet made): `No changes. Your infrastructure matches the configuration.` (no drift).
- **With the edits: `Plan: 0 to add, 5 to change, 0 to destroy.`** No destroy of any resource.
  - 4 rules `state = "ENABLED" -> "DISABLED"` (rule, target and lambda permission all stay).
  - `bd_data_bucket` in place: 3 `lambda_function` blocks -> 2. The diff prints as index shifts; the net is
    `ProcessAllocationFiles` removed, `GoldLayerPricesTrigger` and `BronzeCompleteSilverMerge` unchanged,
    `eventbridge = true` unchanged. `aws_lambda_permission.s3_allocation_processor` and the processor stay (unreferenced).

## 4. Documents (the other half of the retirement; row Z-W24-S1)

The four `infra/aws/ssm/opal-bd-*-download.json` are rewritten on the branch as a one-step no-op ("RETIRED ... Nothing
to do", `exit 0`), text free of the merge-script name (AC1 greps for it) and of the word error. Live versions today:
transaction 3, realized 3, unrealized 3 (Default == Latest), allocation 5 (Default == Latest). NOT published.

## 5. Per-table plan, DELTA and rollback per key

| table | act | independent key | expected served DELTA | rollback per key |
|---|---|---|---|---|
| transactions | publish no-op document; disable `bd-transaction-pipeline-trigger` | SSM `opal-bd-transaction-download` v4; rule | content 0. Timing: 0-row interim partition no longer written 21:54Z; real rows land at the next sentinel (row S2) | `update-document-default-version` back to 3; rule `state="ENABLED"` |
| realized | same | SSM `opal-bd-realized-download` v4; `bd-realized-pipeline-trigger` | content 0 (same rows). Timing: up to ~26h later on sentinel-less days (row S2) | default back to 3; rule ENABLED |
| unrealized | same, after the DS leg | SSM `opal-bd-unrealized-download` v4; `bd-unrealized-pipeline-trigger` | 0 partitions added/removed; the 6 empty partitions stay; manifest processed_etags 68 -> 74 (not served). First run after the DS leg reads `failures=0 ... empty_stub=6`, then `No new` | default back to 3; rule ENABLED; script re-deploy of the prior bytes |
| allocations | publish no-op document; disable `bd-allocation-pipeline-trigger`; remove the `ProcessAllocationFiles` block (plan) | SSM `opal-bd-allocation-download` v6; rule; notification | 0 (merge already owns every key: 131 of 131). The processor's `bd-price-update` invoke (2 in 60 days) stops; the transactions merge still invokes it each run | default back to 5; rule ENABLED; re-add the block and re-plan |

Never half-landed: the four rows are independent, so the issuer can GO a subset (row S2 option c: unrealized and
allocations only). Recommended order if all four go: (1) DS leg, (2) publish the four documents, (3) `safe-apply` the
saved plan, (4) read back s16.AC1 (expect 4 of 4 with 1 writer) and s16.AC2. Any act outside 21:30-22:15Z and
00:00-00:30Z. Ledger `nfra-mcpindex-r6-bd-merge-retire` opens only on the GO; AC3 reads an OPEN ledger as FAIL, so close it
in the same session.

## 6. Baseline of the order's checks at this base (live)

s16.AC1 FAIL (0 of 4; transactions 2, realized 2, unrealized 2, allocations 3 writers); s16.AC2 PASS (3 of 3 clean newest
runs; unrealized `failures=6` printed, ungraded); s16.AC3 FAIL (no entry; scan denominator 18 of 18).

## 7. Open for the never-widen halves

1. Row Z-W24-S2 (BLOCKING, ARMED, disarm owner 2.0.0_SA_COO~MI): accept the sentinel-less-day lag, or hold
   transactions and realized, or go unrealized and allocations only.
2. Whether the 6 empty `silver/unrealized/2026-07-0x` partitions stay (they do under this plan).
3. The runner's all-table-success rule that withholds the sentinel on those days was not diagnosed here.
