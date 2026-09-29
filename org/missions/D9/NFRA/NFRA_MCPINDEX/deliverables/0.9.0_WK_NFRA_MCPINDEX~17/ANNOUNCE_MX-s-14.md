# ANNOUNCE -- MX-s-14 PHASE A, the BD transaction leg ported to the REST pull (steps 1-2 built, steps 3-4 blocked on a DS-lane publish)

Worker: 0.9.0_WK_NFRA_MCPINDEX~17 (issuer 2.0.0_SA_COO~MI). Order:
org/missions/D9/NFRA/NFRA_MCPINDEX/task-orders/NFRA_MCPINDEX.TO-MX-s-14.bd-transaction-rest-port.md

STATE: PHASE A stopped at the publish. Nothing was deployed, no ledger was opened, no SSM document version was
created, no rule was touched, nothing was uploaded to S3, and NO VENDOR CALL was made (count 0).
AWS contact was read-only: `s3 ls` of the transaction bronze prefix, `comp-pipescript deployed --firm bd`, and the
three `s14.AC*.sh` reads (ssm describe/get-document, events describe-rule/list-targets).

## STEP 1 -- the REST pull (built, not yet run)

`data/black_diamond/scripts/bronze/pull_bd_transaction_rest.py`, on the MX-s-9 pattern (`pull_bd_asset_dim_rest.py`):

| property | value |
| --- | --- |
| session | bearer minted from `blackdiamond/49f/session`; read-only; 49F only; refuses before any network call if secret or bucket is not 49F's |
| template | the persisted `Transactions_OpalCapital_Daily` (the name `download-daily-transaction.ts` ran), found in the roster by exact name; 0 or 2+ matches refuses |
| vendor writes | none: GET template, inline run, status poll, export |
| bronze key | `forwardfill_v2/transactions/TXN_DAILY_<data date>.xlsx`, the export workbook unchanged, the key the Playwright leg wrote and `merge-daily-incremental.py` reads |
| data date | the export's Timestamps-sheet `Start Date`, as `extract-as-of-date.ts` read it |
| first landing wins | an existing object at the key is kept (`SKIP-EXISTS`), as the Playwright leg did |
| output | `OUTPUT_KEY=s3://<bucket>/<key>`, then `ROWS= COLS= DATE_MIN= DATE_MAX= RUN_ID= GUID= VENDOR_CALLS=` |
| honest exit | non-zero on: no bearer, template not found once, failed or timed-out run, truncated export, 0 data rows, columns != 71 |
| test flag | `--stage` lands the object under `staging/mx-s-14/transactions/` so a test moves nothing the merge reads |

Two departures from the order, both stated in the module and filed as rows:
- `_transaction_rest_pin.py` was NOT written. A generated pin needs a `lib/opal_naming.py` target; `lib/` is not in
  this cell's paths. The module reads scope/vendor/bucket from the already-published generated `_asset_dim_rest_pin.py`
  (comp-pipescript: MATCH) and carries the two legacy literals (prefix, `TXN_DAILY_`). Row Z-W17-S1.
- An export with 0 data rows is refused rather than written (the vendor's empty workbook is well formed, about 4.4 KB;
  the bronze prefix holds two such stubs for 2026-09-28/29 under the other producer's name). Row Z-W17-S3 has the
  census.

The discovery read of the export template was NOT performed (it needs the instance; see step 3). `discover` mode
prints the roster count, the name-match count, and the template's id, queryTypeId, dateRangeType and window: one
roster GET plus one template GET, two counted calls.

## STEP 2 -- the document (edited, not published)

`infra/aws/ssm/opal-bd-transaction-download.json`, on the shape of `opal-bd-asset-dim-download.json`:
- Playwright step, `BD_USERNAME`/`BD_PASSWORD` and the `opal/bd/credentials` read: REMOVED (0 refs each in the JSON).
- stages exactly two objects into `$RUNROOT/data/black_diamond/scripts/bronze/`: `code/bronze/pull_bd_transaction_rest.py`
  and `code/bronze/_asset_dim_rest_pin.py`; the module needs no `lib/` closure (no `opal_naming`, no trading calendar).
- runs the pull as ec2-user, captures `PULL_RC`, then the SAME merge step as before (`scripts/merge-daily-incremental.py`,
  captured `MERGE_RC`); the merge runs whatever the pull did, as it did when the download failed.
- log upload, then `shutdown -h +2 &` ARMED BEFORE the `exit 1` branch (the old document exited first and stranded the
  instance on every failure), then the honest exit on either RC.
- offline: JSON parses; the run commands carry `pull_bd_transaction_rest` 2 times, `download-daily-transaction.ts` 0,
  `BD_PASSWORD` 0.

## STEP 3 -- the test run: BLOCKED (row Z-W17-S2)

The edited commands stage a module that is not published. Publishing `code/bronze/pull_bd_transaction_rest.py` is the
DS lane's safe-deploy. Unblock: one publish of that one object from this branch's bytes; then re-issue step 3 as
`ssm send-command` with the edited commands (with `--stage`, then optionally once without). Expected budget: about 6
counted vendor calls per pull (token, roster, template, run, status poll(s), export).

Not measured, so not claimed: the template's `dateRangeType` and stored window; whether the export carries 71 columns;
whether the instance role may write `staging/mx-s-14/`; whether the discovered template id is unique in the roster.

## STEP 4 -- what the issuer asks

Offline checks run on the module (synthetic 71-column workbooks, no vendor): the key is byte-equal to the Playwright
form; a duplicate roster name is refused; the run body normalises ISO dates and adds the five required nulls; the data
date is read from `Start Date`; a 0-row workbook is detected.

Criteria at this cut (run from the worktree, live reads): AC1 FAIL (served document version 2 of 2 still Playwright;
DefaultVersion 1, LatestVersion 2), AC2 PASS (rule ENABLED, 1 target), AC3 FAIL (no PHASE B GO). AC1 and AC3 need
PHASE B by construction. NOTE for the never-widen halves: AC2 reads ENABLED because MX-i-5 had not yet disabled the
rule at this read; MX-i-5's PHASE B disables it and this order's PHASE B re-enables it.

Rows: NFRA_MCPINDEX-Z-W17-S1 (BLOCKING, INERT: pin target), -S2 (BLOCKING, INERT: DS publish), -S3 (OBSERVATION,
INERT: `TRANSACTIONS_DAILY_*` names beside `TXN_DAILY_*`). Disarm owner `2.0.0_SA_COO~MI` on the two BLOCKING rows.

DO NOT publish the document or re-enable the rule until the step-3 run reads a row count and a date range.
