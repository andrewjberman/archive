# ANNOUNCE MX-s-17 PHASE A -- point opal-bd-transaction-download and opal-bd-realized-download at code/silver/

Worker: 0.9.0_WK_NFRA_MCPINDEX~24. Branch wk-nfra_mcpindex-r7-24. Nothing published, no ledger opened, no SSM command sent, no instance started.
Push state: LOCAL (no push). Measured 2026-10-02 ~03:20Z.

## 0. Preflight

- comp-schedule: RUN (ledger view; it reads the gate ledger, not the cron table). Result PARTIAL (budget 90 s, 1 of 5 carriers scanned), so it is NOT-DECIDABLE for the cron windows. The cron rules were read directly instead:
  `aws events describe-rule` -> bd-realized-pipeline-trigger `cron(45 21 ? * MON-FRI *)` ENABLED; bd-transaction-pipeline-trigger `cron(53 21 ? * MON-FRI *)` ENABLED; bd-49f-session-daily `cron(0 0 * * ? *)` ENABLED. Publish must stay outside 21:30-22:15Z.
- Served state: both documents are version 3, DefaultVersion 3 = LatestVersion 3, Status Active (`ssm describe-document`; `list-document-versions` shows v1 2026-03-30/02-19, v2, v3 created 2026-09-29 04:26 EDT).
- The served v3 content equals the repo JSON for both documents (parsed-JSON equality: True, True), so the edit below starts from the served bytes.

## 1. The diff -- scripts/ vs code/silver/ (step 1)

Files: `deliverables/.../MX-s-17/merge-daily-incremental.scripts_vs_code-silver.diff` (840 lines).
- `scripts/merge-daily-incremental.py` 43,492 bytes, LastModified 2026-06-29 11:16:30.
- `code/silver/merge-daily-incremental.py` 59,820 bytes, LastModified 2026-10-01 17:27:57 (the script bd-silver-merge runs).
- The two are NOT equivalent. Every hunk in the transactions and realized paths is one of three kinds:
  1. I/O layer: `aws s3 cp/ls` subprocess calls replaced by boto3 helpers (`_s3_download`, `_s3_upload`, `_s3_list_names`, `_s3_get_json`, `_s3_put_json`). The two hunks inside each table's processing function (download of the xlsx, upload of the parquet) are the only changes inside it; the column and dedup logic is byte-unchanged.
  2. The skip predicate: filename (`processed_files`) -> bronze ETag (`processed_etags`), with per-file log lines (`NEW`, `REPROCESS-etag-changed`, `SKIP-unchanged`). A same-name bronze re-land now REPLACES its partition (the 06-26..06-29 freeze fix).
  3. `run()` / `lambda_handler()` entry points and the allocations stub-reject and unrealized empty-stub skip. The documents do not run allocations or unrealized, so those two hunks do not execute on the document path.
- CLI contract unchanged for the two documents: no flag = transactions (`incremental_merge()`), `--realized` = `incremental_realized_merge()` (code/silver main(), read).
- Manifest keys unchanged: both versions use `silver/incremental_manifest.json` and `silver/incremental_realized_manifest.json`. One manifest per table, shared by both writers.
- lib: `scripts/lib/` holds `__init__.py` (0 B) and `config.py` (268 B, docstring says "gold layer"). `code/silver/lib/` holds `__init__.py`, `config.py` (136 B), `ticker_overrides.py` (63,680 B) and a `__pycache__` of cp312 .pyc. `code/silver/merge-daily-incremental.py` imports NO `lib` module (imports: `__future__`, os, subprocess, json, sys, argparse, datetime, io, pathlib, boto3 (guarded), pandas (guarded), re). So "code/silver/lib/ exists with every module the script imports" holds trivially (0 of 0 needed); the realized document's lib sync is kept as the cell directs.
- Third-party imports of the new script: boto3 and pandas. See row Z-W24-S9 (boto3 absent would read as a clean empty run).

## 2. The edited documents (step 3)

Repo files edited in this commit (not published): `infra/aws/ssm/opal-bd-transaction-download.json`, `infra/aws/ssm/opal-bd-realized-download.json`. Both parse as JSON. Diff: `MX-s-17/ssm_documents_repoint.diff`; full edited files and the served v3 files sit beside it in `MX-s-17/`.

```
transaction  :27  s3://opal-data-bd/scripts/merge-daily-incremental.py -> s3://opal-data-bd/code/silver/merge-daily-incremental.py
realized     :30  s3://opal-data-bd/scripts/merge-daily-incremental.py -> s3://opal-data-bd/code/silver/merge-daily-incremental.py
realized     :31  aws s3 sync s3://opal-data-bd/scripts/lib/ lib/       -> aws s3 sync s3://opal-data-bd/code/silver/lib/ lib/
```
The run lines (`python3 merge-daily-incremental.py` and `... --realized`, :29 and :33) name no path and are unchanged. After the edit, `grep -c 's3://opal-data-bd/scripts/'` = 0 in both files and `code/silver/merge-daily-incremental.py` appears 1 time in each (the AC1 predicate, applied to the repo files; AC1 itself reads the SERVED DEFAULT and LATEST, so it grades only after PHASE B).

Note on the cp line: `|| echo 'WARNING: Script download failed'` still lets the run continue on whatever `merge-daily-incremental.py` is already in /opt/bd-exporter. On a failed download the instance would run its stale local copy, not fail. Unchanged by this cell.

## 3. Expected served DELTA (step 2)

Measured against the live manifests and bronze at ~03:20Z, applying the code/silver predicate (`_should_skip`: known prior ETag equal to the current bronze ETag):

| table | forwardfill xlsx listed | manifest processed_etags | would SKIP-unchanged | NEW | ETAG-CHANGED |
|---|---|---|---|---|---|
| silver/transactions | 198 | 198 (0 null) | 198 | 0 | 0 |
| silver/realized | 147 | 147 (0 null) | 147 | 0 | 0 |

Both manifests were last written 2026-10-02 00:14:29Z / 00:14:49Z, i.e. by bd-silver-merge's 00:11Z run (the code/silver script). So the next 21:45Z / 21:53Z document run, if no bronze changes in between, writes 0 rows to `silver/transactions/` and `silver/realized/`: **DELTA = 0 on both tables**.
Where bronze did change before a run (a same-name re-land), the new document REPLACES that date's partition with the same transform bd-silver-merge applies; the old script would have skipped it. That is a correction, not a widening, and it is the identical write bd-silver-merge makes for the same file. The 49F runner lands bronze at 00:00Z, so the 21:45Z-21:53Z window normally sees no new bronze.
The manifest is the one shared writer-state: the old script saved `processed_files` and left `processed_etags` stale; moving both documents to the new script removes that skew.

## 4. Rollback per document (re-set the prior version DEFAULT)

Prior version read from `ssm list-document-versions`: **version 3** for BOTH documents (current DEFAULT, created 2026-09-29).
```
aws ssm update-document-default-version --name opal-bd-transaction-download --document-version 3
aws ssm update-document-default-version --name opal-bd-realized-download   --document-version 3
```
Then read back `describe-document ... DefaultVersion` = 3. The new version (4) stays as Latest; AC1 would then read STALE on DEFAULT (expected after a rollback).
PHASE B publish plan: `aws ssm update-document --name <doc> --content file://... --document-version '$LATEST'` for each, then `update-document-default-version` to the returned version, then Default == Latest read-back for both, then s17.AC1, then close ledger `nfra-mcpindex-r7-bd-doc-repoint`.

## 5. Census line only (not in this cell)

`s3://opal-data-bd/scripts/` is still named by: `force-alloc-download.json:17` (cp merge script) and `:12` (sync scripts/src/); `force-txn-download.json:17` (cp merge script) and `:12` (sync scripts/src/); `opal-bd-fees-download.json:28` (sync scripts/src/). Also `infra/aws/ec2/bd-exporter/deploy-merge-daily-incremental.sh` publishes to `scripts/merge-daily-incremental.py` (row Z-W24-S10). Census over `infra/aws/ssm/` : 5 line(s) in 3 files besides the two documents in this cell.

## 6. Rows filed (INVESTIGATION_v1.md)

- NFRA_MCPINDEX-Z-W24-S9 -- OBSERVATION, ARMED (disarm_owner 2.0.0_SA_COO~MI): code/silver script no-ops silently if boto3 is missing; the instance's boto3 is declared in user-data, not measured. Disarm at PHASE B before publish.
- NFRA_MCPINDEX-Z-W24-S10 -- OBSERVATION, INERT: the exporter deploy script and force-* documents still use `scripts/`.

## 7. For the never-widen halves

Blast radius: two SSM document versions; the documents write only `silver/transactions/`, `silver/realized/`, their two manifests and `logs/`; rollback per key above. No role, policy, schedule or Terraform change.

## 8. ADDENDUM (written during MX-s-18 PHASE A; corrects section 3's last paragraph)

Section 3's "DELTA = 0" holds for a day whose bronze bd-silver-merge has already merged (a sentinel day). It does NOT hold for a sentinel-withheld day. On such a day (9 of 29 dates in 2026-09-03..10-01: 09-07, 09-08, 09-09, 09-14, 09-15, 09-21, 09-22, 09-28, 09-29) the day's bronze is still unmerged at 21:45Z, so the repointed documents will MERGE it: NEW files, the same column and dedup transform as the old script, written to `silver/transactions/<data-date>.parquet` and `silver/realized/<data-date>.parquet`. That is what the documents write on those days today (the gap-day write of row Z-W24-S8); the repoint changes the code version, not the set of keys written. Measured partitions on the gap dates (rows): transactions 0, 5,274, 3,194, 4,873, 50,191, 3,967, 52,792, 7,643, 110,689; realized 7,889, 6,432, 5,785, 7,746, 7,173, 9,330, 9,350, 11,298, 10,915. So the expected DELTA is: 0 on sentinel days; on a gap day, the day's new partitions, identical in transform to the old script's, with one behavioural difference: the ETag skip re-processes a same-name re-landed file (replaces its partition) where the old filename skip would not.
Once MX-s-18 lands, Mon/Tue stop being gap days (bd-silver-merge merges them at ~00:1xZ) and the documents revert to the 0-delta case. MX-s-18 is held by row Z-W24-S11.
