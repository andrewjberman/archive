# ANNOUNCE MX-s-18 PHASE A -- the BD runner's own sentinel check, built and tested; NOT applied; ONE BLOCKING ROW

Worker: 0.9.0_WK_NFRA_MCPINDEX~24. Branch wk-nfra_mcpindex-r7-24. No upload, no apply, no ledger, no ad-hoc runner invocation, nothing under data/cot/ touched. Push state: LOCAL (no push).
Measured 2026-10-02 ~04:20Z.

## 0. READ THIS FIRST -- BLOCKING row NFRA_MCPINDEX-Z-W24-S11 (hold PHASE B)

The order's required read-back, `head_object` on `bronze/<date>/_BRONZE_COMPLETE.json`, is REFUSED by the live runner role.
- `iam simulate-principal-policy` (applied plane), role bd-49f-runner-role, one resource per call:
  - `s3:GetObject bronze/2026-10-02/_BRONZE_COMPLETE.json` -> **implicitDeny**
  - `s3:PutObject  bronze/2026-10-02/_BRONZE_COMPLETE.json` -> allowed
  - `s3:GetObject forwardfill_v2/transactions/_complete/2026-10-02.json` -> allowed; `.../TRANSACTIONS_DAILY_2026-10-02.xlsx` -> allowed
- DESIRED plane agrees: `bd-49f-interim.tf:216-246` grants `bronze/*` PutObject only (statement EmitBdBronzeSentinel).
- The order's preflight said the role "already reads and writes" bronze/. It writes; it does not read. HeadObject is authorized by s3:GetObject.
- Effect if PHASE B were applied as specified: the sentinel put succeeds first (so silver still fires), then the read-back 403s, the runner prints `ERROR:` and raises after the RESULT line, every night. The function has no EventInvokeConfig (`get-function-event-invoke-config` -> ResourceNotFoundException) and bd-49f-session-trigger invokes it with `InvocationType: Event`, so Lambda's default async retries (2) would re-run it. On a measured-empty transactions day each retry re-pulls the transactions window from Black Diamond, because `_already_landed` reads `has_data_rows==0` as not landed.
- I did NOT edit the policy (order: "a refusal at the read-back is a BLOCKING row, never a policy edit"). The code implements the read-back as specified. The offline tests use stub S3 and cannot see this.
- Issuer's decision needed before PHASE B: (a) a one-statement grant, `s3:GetObject` on `arn:aws:s3:::opal-data-bd/bronze/*/_BRONZE_COMPLETE.json` (bd-49f-interim.tf is in this order's `<paths>`), or (b) an alternative read-back. Disarm owner on the row: 2.0.0_SA_COO~MI.

## 1. The diff

`deliverables/.../MX-s-18/runner_and_deploy_script.diff` (re-cut after the key-form change): two files changed, one file added.

`infra/aws/lambda/bd-pipeline/bd-49f-runner/lambda_function.py` (+109/-6): the runner decides completeness itself and no longer calls `mod.emit_bronze_sentinel`.
- `_measured_empty_sidecar(mod, table, as_of)`: True only for `transactions`, and only if the sidecar `forwardfill_v2/transactions/_complete/<as_of>.json` exists, is not `basis == content_probe_backfill` (inferred), and `has_data_rows` is an int equal to 0. Missing, unreadable, -1 and inferred are all False.
- `_table_state(mod, table, as_of)`: head_object on the bronze xlsx (absent -> `missing`); `mod._table_complete` True -> `complete` (the shared rule, floor and inferred-rejection unchanged); else the measured-empty exception -> `complete-empty`; else `incomplete`.
- `_emit_sentinel(mod, run_date, landed)`: any table not complete -> prints `WARN: bronze sentinel NOT emitted for <date> -- incomplete table(s): <t>(<state>)...` and returns `withheld` (never prints OK). All complete -> `put_object` the sentinel, then `head_object` it, then and only then prints `OK: bronze sentinel emitted ...`. A failed read raises `RuntimeError` (after an `ERROR:` line); a failed put keeps the old behaviour (`ERROR:` line, non-fatal, re-emits next run).
- Naming gate (LGIC_ENFORCE DEC-6, ENFORCE): my first form of the key literal, `bronze/%s/_BRONZE_COMPLETE.json`, was a NEW out-of-pattern S3 key and the commit was REFUSED (`NAMING REFUSE ...lambda_function.py:119`, commit aborted, files unstaged). The file's own docstring already carried this key as `bronze/{date}/_BRONZE_COMPLETE.json`, so I used that exact existing form (`SENTINEL_KEY_FMT.format(date=run_date)`); `naming-gate.py --diff` then grades it `EXISTING, touched, and OUT-OF-PATTERN as S3Key: WARN` (verdict `NAMING-GATE: WARN 2 graded`; the second WARN is the pre-existing `cot_bronze_ingest.py` carrier). No registry row and no R20 exception was added: the key is the live physical key the S3 notification prefix-matches, and moving it to the canonical `{source}/{scope}/bronze/...` form would break `BronzeCompleteSilverMerge`. That departure is a migration-project / R20 matter for the issuer, not a rider here.
- Key and body shape reproduced from `emit_bronze_sentinel` (`cot_bronze_ingest.py:1328`): key `bronze/<run_date>/_BRONZE_COMPLETE.json`; body `stage, run_date, completed_at, overall, artifacts{tables, count, as_of}, producer`. `test_sentinel_body_matches_shared_module_shape` runs the real shared function and compares field sets and values: no differing field.
- The handler's RESULT dict gains one key, `sentinel` (`emitted | withheld | put-failed | readback-failed | error | not-attempted`). The runner raises the read-back error after printing RESULT.
- `_already_landed` is UNCHANGED, so a second same-night invoke on a measured-empty transactions day still re-pulls transactions (as today).

`infra/aws/ec2/bd-gold-layer-runner/deploy-to-ec2.sh`: the bronze `aws s3 sync ... --delete` now carries `--exclude 'cot_bronze_ingest.py'` (bash -n clean; the eval re-parse prints the argument as `cot_bronze_ingest.py`). The silver and gold syncs are untouched. The script was not run. Live engine object read: `code/bronze/cot_bronze_ingest.py`, 80,599 B, 2026-08-21, so the hazard is real today.

`tests/test_runner_sentinel.py` (new, offline, stub S3, loads the unmodified shared module read-only): the three named tests plus six controls. Mutation check: emptying the exception set fails 2 tests; widening it to realized+allocations fails 2 tests.

## 2. Test output (verbatim deciding lines)

`deliverables/.../MX-s-18/pytest_output.txt`:
```
PASSED ...::test_period_empty_window_emits_sentinel
PASSED ...::test_snapshot_zero_rows_withholds
PASSED ...::test_ok_line_only_after_head_object_readback
(+6 control tests PASSED)
9 passed in 0.20s
```
Negative controls: (i) a snapshot table with 0 rows withholds -- `test_snapshot_zero_rows_withholds` and the `unrealized` 0-row case; also realized 0, transactions -1, missing sidecar, inferred sidecar, missing bronze object all withhold. (ii) `data/cot/` byte-unchanged: s18.AC2 = `data/cot/ files changed since cb234fbfa0: 0`.
Checks run from the worktree: s18.AC1 `pytest rc=0; named tests passed 3 of 3 -- RESULT: PASS`; s18.AC2 PASS; s18.AC3 `s3 sync statements=4; to code/bronze=1; deleting without excluding cot_bronze_ingest.py=0 -- RESULT: PASS`. s18.AC4 is the PHASE B ledger and is not gradable yet.

## 3. The saved plan -- NOT meaningful before the upload (row Z-W24-S12)

`terraform -chdir=infra/aws/terraform/bd-pipeline plan -target=module.bd_49f_runner -out=...` (terraform v1.15.8): `No changes. Your infrastructure matches the configuration.` rc=0. Log: `MX-s-18/terraform_plan_targeted_pre_upload.log`. No destroy, nothing to apply.
Reason: `modules/yang-lambda` reads the zip's S3 version id and `content-sha256` metadata at plan time, so a change exists in a plan only after the new zip is in S3. I did not upload in PHASE A: a new latest version at the live key would be deployed by any other plan/apply on the bd-pipeline root, without the never-widen halves.
Built artifact (not uploaded): `MX-s-18/bd-49f-runner.zip`, 6,936 B, deterministic (fixed 2020-01-01 mtimes, one entry `lambda_function.py`, rebuild is byte-identical, content equals the committed source), sha256 base64 `9PbO1/mVokBTWGNn8NjjTyjkhWvBdZ6pZk2zcCE0/eY=` (hex f4f6ced7f995a24053586367f0d8e34f28e4856bc1759ea9664db3702134fde6). The deployed CodeSha256 today is `q37ovM/F07p39ObyY6bML9tmIEXDN1S/OhyJv1oDH00=`.
Expected plan after the upload (inferred from the module's attributes, not a plan output): `Plan: 0 to add, 1 to change, 0 to destroy`, the one change being `module.bd_49f_runner.aws_lambda_function.this` in place (`s3_object_version`, `source_code_hash`). PHASE B should be: upload with `--metadata content-sha256=<sha>` and verify size + metadata, cut the saved plan, read the plan line (any destroy is BLOCKING), `safe-apply` the saved plan, compare `CodeSha256` to the sha above.

## 4. Served effect when it lands (read from code)

On a Monday/Tuesday where the newest transactions tile is a measured empty window and the other three tables are complete, the runner writes `bronze/<run_date>/_BRONZE_COMPLETE.json`; the S3 notification `BronzeCompleteSilverMerge` fires bd-silver-merge, whose `lambda_handler` runs all four tables (`tables` absent -> all). From `code/silver/merge-daily-incremental.py`:
- transactions: every new or ETag-changed `forwardfill_v2/transactions/TRANSACTIONS_DAILY_*.xlsx` becomes `silver/transactions/<data-date>.parquet`, wholesale per file. The empty tile has no empty-skip on this path, so it writes a 0-row partition (74 columns). Precedent: `silver/transactions/2026-09-07.parquet` is 0 rows, 74 columns, 35,269 B (read 2026-10-02). The manifest `silver/incremental_manifest.json` is updated. `bd-price-update` is invoked only when the run's `total_rows > 0`, which the older non-empty tiles normally give.
- allocations, realized, unrealized: processed exactly as on a sentinel day (ETag-new files; allocations stub-reject and unrealized empty-stub skip apply).
- Net served change: on Mon/Tue the same-day silver write moves from the SSM documents (21:46Z / 21:53Z, the gap-day writer of row Z-W24-S8) to bd-silver-merge at ~00:1xZ. Measured gap: 9 sentinel-less dates in 2026-09-03..10-01 (09-07, 09-08, 09-09, 09-14, 09-15, 09-21, 09-22, 09-28, 09-29) of 29.
- The first live exercise is the scheduled 00:00Z run. It cannot show an OK line while Z-W24-S11 stands.

## 5. Rollback

- Artifact: the prior zip is `s3://opal-313476888478-lambda-artifacts/bd-pipeline/bd-49f-runner.zip` VersionId `AVNCLX4FqgXkDQwMLgoYD86veMQzY8mQ` (2026-07-09, 5,199 B, content-sha256 `q37ovM/F07p39ObyY6bML9tmIEXDN1S/OhyJv1oDH00=`; older versions hGyzcA4z..., 6Xbsiy1a..., PwdAOe7X...). It equals the deployed CodeSha256 now, so it is the live code. Rollback act: copy that version back to the key (`aws s3api copy-object --copy-source ...?versionId=AVNCLX4F... --metadata-directive COPY`), cut a plan, `safe-apply` it, read CodeSha256 = q37ovM... . Never `update-function-code`.
- Script: `deploy-to-ec2.sh` is repo-only; revert the commit.

## 6. Other measurements

- `bd-49f-session-daily` `cron(0 0 * * ? *)` ENABLED (`events describe-rule`). `comp-schedule` is the gate ledger and ended PARTIAL (budget 90 s, 1 of 5 carriers), so the apply window 23:45-00:45Z was read from the rule directly.
- Python 3.14 locally, runtime python3.12 in the function; the runner adds only stdlib `json`.

## 7. Rows filed (INVESTIGATION_v1.md)

- NFRA_MCPINDEX-Z-W24-S11 -- BLOCKING, ARMED (disarm_owner 2.0.0_SA_COO~MI): the read-back is refused by the live role.
- NFRA_MCPINDEX-Z-W24-S12 -- OBSERVATION, INERT: a saved plan before the upload says "No changes".
