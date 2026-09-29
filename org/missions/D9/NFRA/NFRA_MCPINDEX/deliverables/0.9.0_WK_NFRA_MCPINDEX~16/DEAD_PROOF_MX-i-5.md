# DEAD_PROOF_MX-i-5 -- the 4 BD Playwright documents, per DOCUMENT, per STEP (worker 0.9.0_WK_NFRA_MCPINDEX~16)

Measured 2026-09-29 ~05:00-06:35Z, READ-ONLY (SSM list/get, S3 list-object-versions and get-object BY VersionId, EventBridge list-rules). Nothing was changed.
The method is worker ~11's `m1_a_*.py` (MEASURE_BATCH_ROUND3.md) with the log predicate unchanged: a line `^ERROR:` containing `fail`, `(Download|Merge) exit code: N` with N nonzero, or a line `FAILED`. This worker's scripts sit in its `.scratch/` (not committed).

## SUMMARY

VERDICT: LIVE for all 4 documents on the ruled predicate (issuer ruling ~06:2xZ: any step that writes since LAST_NON_FAILING makes the document LIVE). The download step (step 3) is dead in all 4; the merge step (step 4) is not. **The plan disables 0 rules; no Terraform was edited.**

| document / rule | download step 3 | merge step 4 writes since 2026-06-22 (own window: silver + manifest) | last ROW-BEARING own-window silver write | last own-window write of any kind |
|---|---|---|---|---|
| bd-allocation-pipeline-trigger | dead (70 of 70 dated logs failed, Download exit code 1) | silver 9 + manifest 4 = 13 | 2026-07-02T22:01Z (6,828 rows) | 2026-07-03T22:00:50Z |
| bd-realized-pipeline-trigger | dead (70 of 70 dated logs failed, Download exit code 1) | silver 35 + manifest 31 = 66 | 2026-09-28T21:46Z (11,298 rows) | 2026-09-28T21:46:05Z |
| bd-transaction-pipeline-trigger | dead (70 of 70 dated logs failed, Download exit code 1) | silver 35 + manifest 31 = 66 | 2026-07-17T21:54Z (3,696 rows) | 2026-09-28T21:54:43Z |
| bd-unrealized-pipeline-trigger | dead (70 of 70 dated logs failed, Download exit code 1) | silver 277 + manifest 50 = 327 | 2026-07-02T21:41Z (103,080 rows) | 2026-09-28T21:40:08Z |

Attribution is INFERRED, not principal-proven: an object counts as this document's when its LastModified time of day falls in [rule minute, rule minute + 45 min] UTC. The bronze producer for these prefixes lands objects at 00:00-01:30Z (bd-49f-session-daily cron(0 0 * * ? *), bd-49f-session-chain.tf:222); no S3 data-event trail was read. Bronze `forwardfill_v2/<leg>/` objects written in any leg's own window since 2026-06-22: 0 of 47 / 180 / 788 / 47 (allocations / realized / transactions / unrealized).

## bd-allocation-pipeline-trigger

Document `opal-bd-allocation-download` at `--document-version $LATEST` (version 4); trigger lambda `bd-allocation-trigger`; schedule `cron(0 22 ? * MON-FRI *)`; rule ENABLED at read time (`aws events list-rules --name-prefix bd-`, 2026-09-29 ~05:5xZ).

### (i) SSM-run grain -- N = 21 retained runs of `opal-bd-allocation-download` (`aws ssm list-commands`, all SSM retains), 2026-08-31 22:00Z .. 2026-09-28 22:00Z

Result: SSM Status Failed 21 of 21; log records failure 21 of 21; plugin ResponseCode {1: 21}.

| requested (UTC) | SSM Status | plugin ResponseCode | log outcome |
|---|---|---|---|
| 2026-08-31 22:00Z | Failed | 1 | FAIL |
| 2026-09-01 22:00Z | Failed | 1 | FAIL |
| 2026-09-02 22:00Z | Failed | 1 | FAIL |
| 2026-09-03 22:00Z | Failed | 1 | FAIL |
| 2026-09-04 22:00Z | Failed | 1 | FAIL |
| 2026-09-07 22:00Z | Failed | 1 | FAIL |
| 2026-09-08 22:00Z | Failed | 1 | FAIL |
| 2026-09-09 22:00Z | Failed | 1 | FAIL |
| 2026-09-10 22:00Z | Failed | 1 | FAIL |
| 2026-09-11 22:00Z | Failed | 1 | FAIL |
| 2026-09-14 22:00Z | Failed | 1 | FAIL |
| 2026-09-15 22:00Z | Failed | 1 | FAIL |
| 2026-09-16 22:00Z | Failed | 1 | FAIL |
| 2026-09-17 22:00Z | Failed | 1 | FAIL |
| 2026-09-18 22:00Z | Failed | 1 | FAIL |
| 2026-09-21 22:00Z | Failed | 1 | FAIL |
| 2026-09-22 22:00Z | Failed | 1 | FAIL |
| 2026-09-23 22:00Z | Failed | 1 | FAIL |
| 2026-09-24 22:00Z | Failed | 1 | FAIL |
| 2026-09-25 22:00Z | Failed | 1 | FAIL |
| 2026-09-28 22:00Z | Failed | 1 | FAIL |

### (ii) S3 log-object grain -- latest version per key of `s3://opal-data-bd/logs/allocation-download-<date>.log` (`list-object-versions`, IsLatest), each read by VersionId

Log objects: 162, 2026-02-14 .. 2026-09-28; recording failure 70; not failing 92; dated after 2026-06-22: 70, of which failing 70. In all 70 of those, `Download exit code: 1` and `Merge exit code: 0`.

FIRST_FAILING: 2026-06-23
LAST_NON_FAILING: 2026-06-22

(contiguous: every log dated after LAST_NON_FAILING fails and none before it does.)

### (iii) Per-STEP writes, from the document's own commands (issuer ruling ~06:2xZ)

| step | what it does | writes | objects written since LAST_NON_FAILING, ALL writers | of which inside this document's own window | last own-window write |
|---|---|---|---|---|---|
| 1 | `aws secretsmanager get-secret-value --secret-id opal/bd/credentials` | nothing (a read) | - | - | - |
| 2 | `aws s3 sync s3://opal-data-bd/scripts/src/` to the host | nothing in S3 | - | - | - |
| 3 | `bun run src/stepwise/download-daily-allocation.ts` (Playwright) | `s3://opal-data-bd/forwardfill_v2/allocations/` | 47 versions (bronze) | **0** | none since 2026-06-22 |
| 4 | `python3 merge-daily-incremental.py --allocations` (consumes bronze written by ANOTHER producer) | `silver/allocations/YYYY-MM-DD.parquet` | 62 versions | **9** (rows>0: 3 of 9 read) | 2026-07-03T22:01Z |
| 4 | same step, its state file | `silver/incremental_allocation_manifest.json` | 28 versions | **4** | 2026-07-03T22:00:50+00:00 |
| 4a | `aws lambda invoke bd-price-update`, only if download rc and merge rc are both 0 | (Lambda) | - | 0 runs qualify: Download exit code 1 in 70 of 70 | never since 2026-06-22 |
| 5 | `aws s3 cp` log, unconditionally | `logs/allocation-download-<date>.log` | 70 log dates after 2026-06-22 | diagnostic log, not data | 2026-09-28 |

Input step 4 consumes from ANOTHER producer: it lists `forwardfill_v2/allocations/` and converts every file not in its manifest. Those objects since 2026-06-22: 47 versions, of which 31 written 00:00-01:30Z (the bd-49f session chain), 0 in this document's own window, 16 at other times. File name families: ALLOCATIONS_DAILY x34.

Row counts of the own-window silver objects (read BY VersionId, pyarrow `num_rows`; 9 of 9 own-window versions read): {'rows>0': 3, 'rows=0': 6}. Last row-bearing: 2026-07-02T22:01Z (6,828 rows).

OUTPUT_SINCE_LAST_NON_FAILING: 13  (own-window writes by steps 3-4: bronze 0 + silver 9 + manifest 4; denominators, all writers, since 2026-06-22: bronze `forwardfill_v2/allocations/` 47 versions, silver `silver/allocations/` 62 versions, manifest 28 versions)

VERDICT: LIVE (step 4 writes silver/allocations/ and silver/incremental_allocation_manifest.json; last row-bearing own write 2026-07-02T22:01Z (6,828 rows))

Note for the ruling: allocation's last own-window write of ANY kind is 2026-07-03T22:00:50Z (9 silver + 4 manifest, all dated 2026-06-25..07-03), 88 days before this read; it has written nothing since. It reads LIVE only because the window starts at 2026-06-22.

## bd-realized-pipeline-trigger

Document `opal-bd-realized-download` at `--document-version $LATEST` (version 2); trigger lambda `bd-realized-trigger`; schedule `cron(45 21 ? * MON-FRI *)`; rule ENABLED at read time (`aws events list-rules --name-prefix bd-`, 2026-09-29 ~05:5xZ).

### (i) SSM-run grain -- N = 21 retained runs of `opal-bd-realized-download` (`aws ssm list-commands`, all SSM retains), 2026-08-31 21:45Z .. 2026-09-28 21:45Z

Result: SSM Status Failed 21 of 21; log records failure 21 of 21; plugin ResponseCode {1: 21}.

| requested (UTC) | SSM Status | plugin ResponseCode | log outcome |
|---|---|---|---|
| 2026-08-31 21:45Z | Failed | 1 | FAIL |
| 2026-09-01 21:45Z | Failed | 1 | FAIL |
| 2026-09-02 21:45Z | Failed | 1 | FAIL |
| 2026-09-03 21:45Z | Failed | 1 | FAIL |
| 2026-09-04 21:45Z | Failed | 1 | FAIL |
| 2026-09-07 21:45Z | Failed | 1 | FAIL |
| 2026-09-08 21:45Z | Failed | 1 | FAIL |
| 2026-09-09 21:45Z | Failed | 1 | FAIL |
| 2026-09-10 21:45Z | Failed | 1 | FAIL |
| 2026-09-11 21:45Z | Failed | 1 | FAIL |
| 2026-09-14 21:45Z | Failed | 1 | FAIL |
| 2026-09-15 21:45Z | Failed | 1 | FAIL |
| 2026-09-16 21:45Z | Failed | 1 | FAIL |
| 2026-09-17 21:45Z | Failed | 1 | FAIL |
| 2026-09-18 21:45Z | Failed | 1 | FAIL |
| 2026-09-21 21:45Z | Failed | 1 | FAIL |
| 2026-09-22 21:45Z | Failed | 1 | FAIL |
| 2026-09-23 21:45Z | Failed | 1 | FAIL |
| 2026-09-24 21:45Z | Failed | 1 | FAIL |
| 2026-09-25 21:45Z | Failed | 1 | FAIL |
| 2026-09-28 21:45Z | Failed | 1 | FAIL |

### (ii) S3 log-object grain -- latest version per key of `s3://opal-data-bd/logs/realized-download-<date>.log` (`list-object-versions`, IsLatest), each read by VersionId

Log objects: 130, 2026-03-30 .. 2026-09-28; recording failure 79; not failing 51; dated after 2026-06-22: 70, of which failing 70. In all 70 of those, `Download exit code: 1` and `Merge exit code: 0`.

FIRST_FAILING: 2026-04-22
LAST_NON_FAILING: 2026-06-22

(FIRST_FAILING is an intermittent failure; failing and non-failing days interleave from FIRST_FAILING to LAST_NON_FAILING; every one of the 70 logs dated after LAST_NON_FAILING fails.)

### (iii) Per-STEP writes, from the document's own commands (issuer ruling ~06:2xZ)

| step | what it does | writes | objects written since LAST_NON_FAILING, ALL writers | of which inside this document's own window | last own-window write |
|---|---|---|---|---|---|
| 1 | `aws secretsmanager get-secret-value --secret-id opal/bd/credentials` | nothing (a read) | - | - | - |
| 2 | `aws s3 sync s3://opal-data-bd/scripts/src/` to the host | nothing in S3 | - | - | - |
| 3 | `bun run src/stepwise/download-daily-realized.ts` (Playwright) | `s3://opal-data-bd/forwardfill_v2/realized/` | 180 versions (bronze) | **0** | none since 2026-06-22 |
| 4 | `python3 merge-daily-incremental.py --realized` (consumes bronze written by ANOTHER producer) | `silver/realized/YYYY-MM-DD.parquet` | 177 versions | **35** (rows>0: 35 of 35 read) | 2026-09-28T21:46Z |
| 4 | same step, its state file | `silver/incremental_realized_manifest.json` | 90 versions | **31** | 2026-09-28T21:46:05+00:00 |
| 5 | `aws s3 cp` log, unconditionally | `logs/realized-download-<date>.log` | 70 log dates after 2026-06-22 | diagnostic log, not data | 2026-09-28 |

Input step 4 consumes from ANOTHER producer: it lists `forwardfill_v2/realized/` and converts every file not in its manifest. Those objects since 2026-06-22: 180 versions, of which 169 written 00:00-01:30Z (the bd-49f session chain), 0 in this document's own window, 11 at other times. File name families: REALIZED_DAILY x99.

Row counts of the own-window silver objects (read BY VersionId, pyarrow `num_rows`; 35 of 35 own-window versions read): {'rows>0': 35}. Last row-bearing: 2026-09-28T21:46Z (11,298 rows).

OUTPUT_SINCE_LAST_NON_FAILING: 66  (own-window writes by steps 3-4: bronze 0 + silver 35 + manifest 31; denominators, all writers, since 2026-06-22: bronze `forwardfill_v2/realized/` 180 versions, silver `silver/realized/` 177 versions, manifest 90 versions)

VERDICT: LIVE (step 4 writes silver/realized/ and silver/incremental_realized_manifest.json; last row-bearing own write 2026-09-28T21:46Z (11,298 rows))

Note: realized is the clearest LIVE: 35 of 35 own-window silver objects carry rows and the latest (2026-09-28T21:46Z, 11,298 rows) is the partition for that date.

## bd-transaction-pipeline-trigger

Document `opal-bd-transaction-download` at `--document-version $LATEST` (version 2); trigger lambda `bd-transactions-trigger`; schedule `cron(53 21 ? * MON-FRI *)`; rule ENABLED at read time (`aws events list-rules --name-prefix bd-`, 2026-09-29 ~05:5xZ).

### (i) SSM-run grain -- N = 21 retained runs of `opal-bd-transaction-download` (`aws ssm list-commands`, all SSM retains), 2026-08-31 21:53Z .. 2026-09-28 21:53Z

Result: SSM Status Failed 21 of 21; log records failure 21 of 21; plugin ResponseCode {1: 21}.

| requested (UTC) | SSM Status | plugin ResponseCode | log outcome |
|---|---|---|---|
| 2026-08-31 21:53Z | Failed | 1 | FAIL |
| 2026-09-01 21:53Z | Failed | 1 | FAIL |
| 2026-09-02 21:53Z | Failed | 1 | FAIL |
| 2026-09-03 21:53Z | Failed | 1 | FAIL |
| 2026-09-04 21:53Z | Failed | 1 | FAIL |
| 2026-09-07 21:53Z | Failed | 1 | FAIL |
| 2026-09-08 21:53Z | Failed | 1 | FAIL |
| 2026-09-09 21:53Z | Failed | 1 | FAIL |
| 2026-09-10 21:53Z | Failed | 1 | FAIL |
| 2026-09-11 21:53Z | Failed | 1 | FAIL |
| 2026-09-14 21:53Z | Failed | 1 | FAIL |
| 2026-09-15 21:53Z | Failed | 1 | FAIL |
| 2026-09-16 21:53Z | Failed | 1 | FAIL |
| 2026-09-17 21:53Z | Failed | 1 | FAIL |
| 2026-09-18 21:53Z | Failed | 1 | FAIL |
| 2026-09-21 21:53Z | Failed | 1 | FAIL |
| 2026-09-22 21:53Z | Failed | 1 | FAIL |
| 2026-09-23 21:53Z | Failed | 1 | FAIL |
| 2026-09-24 21:53Z | Failed | 1 | FAIL |
| 2026-09-25 21:53Z | Failed | 1 | FAIL |
| 2026-09-28 21:53Z | Failed | 1 | FAIL |

### (ii) S3 log-object grain -- latest version per key of `s3://opal-data-bd/logs/transaction-download-<date>.log` (`list-object-versions`, IsLatest), each read by VersionId

Log objects: 169, 2026-02-05 .. 2026-09-28; recording failure 76; not failing 93; dated after 2026-06-22: 70, of which failing 70. In all 70 of those, `Download exit code: 1` and `Merge exit code: 0`.

FIRST_FAILING: 2026-02-21
LAST_NON_FAILING: 2026-06-22

(FIRST_FAILING is an intermittent failure; failing and non-failing days interleave from FIRST_FAILING to LAST_NON_FAILING; every one of the 70 logs dated after LAST_NON_FAILING fails.)

### (iii) Per-STEP writes, from the document's own commands (issuer ruling ~06:2xZ)

| step | what it does | writes | objects written since LAST_NON_FAILING, ALL writers | of which inside this document's own window | last own-window write |
|---|---|---|---|---|---|
| 1 | `aws secretsmanager get-secret-value --secret-id opal/bd/credentials` | nothing (a read) | - | - | - |
| 2 | `aws s3 sync s3://opal-data-bd/scripts/src/` to the host | nothing in S3 | - | - | - |
| 3 | `bun run src/stepwise/download-daily-transaction.ts` (Playwright) | `s3://opal-data-bd/forwardfill_v2/transactions/` | 788 versions (bronze) | **0** | none since 2026-06-22 |
| 4 | `python3 merge-daily-incremental.py (no flag = transactions)` (consumes bronze written by ANOTHER producer) | `silver/transactions/YYYY-MM-DD.parquet` | 589 versions | **35** (rows>0: 11 of 35 read) | 2026-09-28T21:54Z |
| 4 | same step, its state file | `silver/incremental_manifest.json` | 91 versions | **31** | 2026-09-28T21:54:43+00:00 |
| 4a | merge invokes `bd-price-update` (async) when it added rows (`total_rows > 0`) | `silver/prices/` (all writers: 700 versions since 2026-06-22, 4 at UTC hour 21; not attributable to this document) | 700 | not measured (the Lambda has its own principal) | - |
| 5 | `aws s3 cp` log, unconditionally | `logs/transaction-download-<date>.log` | 70 log dates after 2026-06-22 | diagnostic log, not data | 2026-09-28 |

Input step 4 consumes from ANOTHER producer: it lists `forwardfill_v2/transactions/` and converts every file not in its manifest. Those objects since 2026-06-22: 788 versions, of which 751 written 00:00-01:30Z (the bd-49f session chain), 0 in this document's own window, 37 at other times. File name families: TRANSACTIONS_DAILY x426.

Row counts of the own-window silver objects (read BY VersionId, pyarrow `num_rows`; 35 of 35 own-window versions read): {'rows>0': 11, 'rows=0': 24}. Last row-bearing: 2026-07-17T21:54Z (3,696 rows).

The zero-row objects since 2026-07-17 are 34,882 B date-keyed partitions (e.g. `silver/transactions/2026-09-28.parquet`, 21:54Z).

OUTPUT_SINCE_LAST_NON_FAILING: 66  (own-window writes by steps 3-4: bronze 0 + silver 35 + manifest 31; denominators, all writers, since 2026-06-22: bronze `forwardfill_v2/transactions/` 788 versions, silver `silver/transactions/` 589 versions, manifest 91 versions)

VERDICT: LIVE (step 4 writes silver/transactions/ and silver/incremental_manifest.json; last row-bearing own write 2026-07-17T21:54Z (3,696 rows))

Note: the issuer's fact stands (the REST-produced `TRANSACTIONS_DAILY_*.xlsx` land ~00:02Z and this document's merge consumes them). This read finds the own-window silver writes zero-row since 2026-07-17; real-row transaction silver lands from writers in the 00:00-01:30Z window (504 versions since 2026-06-22).

## bd-unrealized-pipeline-trigger

Document `opal-bd-unrealized-download` at `--document-version $LATEST` (version 2); trigger lambda `bd-unrealized-trigger`; schedule `cron(38 21 ? * MON-FRI *)`; rule ENABLED at read time (`aws events list-rules --name-prefix bd-`, 2026-09-29 ~05:5xZ).

### (i) SSM-run grain -- N = 21 retained runs of `opal-bd-unrealized-download` (`aws ssm list-commands`, all SSM retains), 2026-08-31 21:39Z .. 2026-09-28 21:39Z

Result: SSM Status Failed 21 of 21; log records failure 21 of 21; plugin ResponseCode {1: 21}.

| requested (UTC) | SSM Status | plugin ResponseCode | log outcome |
|---|---|---|---|
| 2026-08-31 21:39Z | Failed | 1 | FAIL |
| 2026-09-01 21:39Z | Failed | 1 | FAIL |
| 2026-09-02 21:39Z | Failed | 1 | FAIL |
| 2026-09-03 21:39Z | Failed | 1 | FAIL |
| 2026-09-04 21:39Z | Failed | 1 | FAIL |
| 2026-09-07 21:39Z | Failed | 1 | FAIL |
| 2026-09-08 21:39Z | Failed | 1 | FAIL |
| 2026-09-09 21:39Z | Failed | 1 | FAIL |
| 2026-09-10 21:39Z | Failed | 1 | FAIL |
| 2026-09-11 21:39Z | Failed | 1 | FAIL |
| 2026-09-14 21:39Z | Failed | 1 | FAIL |
| 2026-09-15 21:39Z | Failed | 1 | FAIL |
| 2026-09-16 21:39Z | Failed | 1 | FAIL |
| 2026-09-17 21:39Z | Failed | 1 | FAIL |
| 2026-09-18 21:39Z | Failed | 1 | FAIL |
| 2026-09-21 21:39Z | Failed | 1 | FAIL |
| 2026-09-22 21:39Z | Failed | 1 | FAIL |
| 2026-09-23 21:39Z | Failed | 1 | FAIL |
| 2026-09-24 21:39Z | Failed | 1 | FAIL |
| 2026-09-25 21:39Z | Failed | 1 | FAIL |
| 2026-09-28 21:39Z | Failed | 1 | FAIL |

### (ii) S3 log-object grain -- latest version per key of `s3://opal-data-bd/logs/unrealized-download-<date>.log` (`list-object-versions`, IsLatest), each read by VersionId

Log objects: 130, 2026-03-30 .. 2026-09-28; recording failure 80; not failing 50; dated after 2026-06-22: 70, of which failing 70. In all 70 of those, `Download exit code: 1` and `Merge exit code: 0`.

FIRST_FAILING: 2026-04-22
LAST_NON_FAILING: 2026-06-22

(FIRST_FAILING is an intermittent failure; failing and non-failing days interleave from FIRST_FAILING to LAST_NON_FAILING; every one of the 70 logs dated after LAST_NON_FAILING fails.)

### (iii) Per-STEP writes, from the document's own commands (issuer ruling ~06:2xZ)

| step | what it does | writes | objects written since LAST_NON_FAILING, ALL writers | of which inside this document's own window | last own-window write |
|---|---|---|---|---|---|
| 1 | `aws secretsmanager get-secret-value --secret-id opal/bd/credentials` | nothing (a read) | - | - | - |
| 2 | `aws s3 sync s3://opal-data-bd/scripts/src/` to the host | nothing in S3 | - | - | - |
| 3 | `bun run src/stepwise/download-daily-unrealized.ts` (Playwright) | `s3://opal-data-bd/forwardfill_v2/unrealized/` | 47 versions (bronze) | **0** | none since 2026-06-22 |
| 4 | `python3 merge-daily-incremental.py --unrealized` (consumes bronze written by ANOTHER producer) | `silver/unrealized/YYYY-MM-DD.parquet` | 304 versions | **277** (rows>0: 2 of 106 read) | 2026-09-28T21:40Z |
| 4 | same step, its state file | `silver/incremental_unrealized_manifest.json` | 113 versions | **50** | 2026-09-28T21:40:08+00:00 |
| 5 | `aws s3 cp` log, unconditionally | `logs/unrealized-download-<date>.log` | 70 log dates after 2026-06-22 | diagnostic log, not data | 2026-09-28 |

Input step 4 consumes from ANOTHER producer: it lists `forwardfill_v2/unrealized/` and converts every file not in its manifest. Those objects since 2026-06-22: 47 versions, of which 31 written 00:00-01:30Z (the bd-49f session chain), 0 in this document's own window, 16 at other times. File name families: UNREALIZED_DAILY x34.

Row counts of the own-window silver objects (read BY VersionId, pyarrow `num_rows`; 106 of 277 own-window versions read): {'rows>0': 2, 'rows=0': 104}. Last row-bearing: 2026-07-02T21:41Z (103,080 rows).

The zero-row objects are daily rewrites of six stale partitions (2026-07-03, -04, -05, -06, -07, -09), 8,016 B each, up to 2026-09-28T21:40Z.

OUTPUT_SINCE_LAST_NON_FAILING: 327  (own-window writes by steps 3-4: bronze 0 + silver 277 + manifest 50; denominators, all writers, since 2026-06-22: bronze `forwardfill_v2/unrealized/` 47 versions, silver `silver/unrealized/` 304 versions, manifest 113 versions)

VERDICT: LIVE (step 4 writes silver/unrealized/ and silver/incremental_unrealized_manifest.json; last row-bearing own write 2026-07-02T21:41Z (103,080 rows))

Note for the ruling: unrealized has written no row-bearing silver in its own window since 2026-07-02T21:41Z; what it writes daily is zero-row partitions and its manifest. Whether that is 'live output' is the issuer's call.

## NEGATIVE CONTROL

`bd-asset-dim-pipeline-trigger` reads ENABLED, `cron(10 22 ? * MON-FRI *)` (`aws events list-rules --name-prefix bd-`, 2026-09-29 ~05:5xZ). Not touched.

