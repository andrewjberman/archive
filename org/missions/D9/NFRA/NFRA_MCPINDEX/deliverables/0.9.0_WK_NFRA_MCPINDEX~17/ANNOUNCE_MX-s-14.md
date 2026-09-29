# ANNOUNCE -- MX-s-14 PHASE A (as amended A1): strip the dead Playwright step from `opal-bd-transaction-download`, keep the merge

Worker: 0.9.0_WK_NFRA_MCPINDEX~17 (issuer 2.0.0_SA_COO~MI). Order (amended A1, CLOUD @a56cbfd460):
org/missions/D9/NFRA/NFRA_MCPINDEX/task-orders/NFRA_MCPINDEX.TO-MX-s-14.bd-transaction-rest-port.md

STATE: PHASE A only. The document is edited in the repo and NOT published; the rule stays ENABLED; DefaultVersion 1,
LatestVersion 2, unchanged at the last read. One ad-hoc run of the edited command list was made as the test
(merge only, ZERO vendor calls).

## SUPERSEDED: the new REST module

The first cut of this order built `pull_bd_transaction_rest.py` (commit 16d142659d). Amendment A1 drops it: a live
`bd-49f-session-daily` REST chain already lands `TRANSACTIONS_DAILY_*`, and a second writer of `TXN_DAILY_*` would be a
shadow pipeline (row Z-W17-S3). The module is REMOVED from this branch by a `git rm` commit, so the drain carries no
unused writer. It was never published and never ran against the vendor. Rows Z-W17-S1 and Z-W17-S2 lapse with it
(row Z-W17-S4 records that).

## (1) The SSM document is the only write

| what | state |
| --- | --- |
| `infra/aws/ssm/opal-bd-transaction-download.json` | the only file changed; not yet published |
| removed from it | the `opal/bd/credentials` fetch, `BD_USERNAME`/`BD_PASSWORD`, the `aws s3 sync` of `scripts/src`, the chown, the `bun run ...download-daily-transaction.ts` step and its `DOWNLOAD_RC` |
| kept | the merge step, the log upload, `shutdown -h +2 &` armed BEFORE the failure branch (the served version exits first and strands the instance), the honest exit on `MERGE_RC` |
| offline counts on the edited commands | `BD_PASSWORD` 0, `download-daily-transaction.ts` 0, `secretsmanager` 0, `merge-daily-incremental` 2 |
| not touched | the Terraform rule, the Lambda trigger, `download-daily-transaction.ts` (retired later, if at all), `merge-daily-incremental.py`, IAM, any bronze object, the vendor |

The test run DID write served silver: the merge wrote the one partition below. That is what the scheduled 21:53Z run
does with the same command; it is a write of the merge, not of this order's edit.

## (2) The merge step is byte-unchanged

The merge step is the 8 lines from `# Run transaction silver conversion` to `echo "Merge exit code: $MERGE_RC"`.
Diff of that block, served `$LATEST` (version 2, read live) against the edited document:

```
1c1
< # Run transaction silver conversion <mojibake dash> capture exit code
> # Run transaction silver conversion - capture exit code
```

The other 7 lines (`echo`, the `aws s3 cp` of `scripts/merge-daily-incremental.py`, `set +e`, `python3 merge-daily-incremental.py`,
`MERGE_RC=${PIPESTATUS[0]}`, `set -e`, `echo "Merge exit code"`) are identical. The one difference is a COMMENT: the served
version carries a double-encoded em dash, and the edited one an ASCII hyphen (the only non-ASCII in the file). Nothing
that executes moved. Same block, repo `120ff9b27f` against edited: the same single comment line.

## (3) Baseline for the next scheduled merge

Prior scheduled run, 2026-09-28 21:54Z (log `logs/transaction-download-2026-09-28.log`): the Playwright step failed at
the login (`Download exit code: 1`), then the merge ran: `Previously processed: 193 files`, `Found 1 new files`,
`TRANSACTIONS_DAILY_2026-09-28.xlsx -> silver/transactions/2026-09-28.parquet (0 rows)`, `Rows added: 0`,
`Total partitions: 194`, `Merge exit code: 0`. Partition `2026-09-28.parquet`: 0 rows, 34,882 bytes.

Rows in the previous six partitions (parquet metadata, read live): 09-22 52,776; 09-23 5,268; 09-24 25,098;
09-25 5,268; 09-26 25,098; 09-27 7,637.

The step-3 TEST run (2026-09-29T06:36:52Z, command `cdb144c8-b4de-4ef1-b5d8-4c36509ca6fc`, Status Success, rc 0):
- merge input: `Previously processed: 194 files`, `Found 1 new files`: `TRANSACTIONS_DAILY_2026-09-29.xlsx` (4,355 bytes,
  the vendor's empty workbook, landed by the REST chain at 00:02Z);
- it wrote `silver/transactions/2026-09-29.parquet`: 0 rows, 35,269 bytes, LastModified 2026-09-29T06:37:01Z;
- `Rows added: 0`, `Total partitions: 195`, `Merge exit code: 0`; the log was uploaded, shutdown armed, the instance is `stopped`;
- vendor calls: 0.

So the next scheduled merge is compared with: partitions 195; last partition 2026-09-29 at 0 rows; and any
`TRANSACTIONS_DAILY_*` the REST chain lands after 00:02Z tomorrow is what it should pick up as new. That the
merge skips an unchanged object under the manifest is expected from the merge's own ETag rule; I did not measure it.

Two things the test showed, stated and not resolved:
- Both new bronze files for 2026-09-28 and 2026-09-29 are empty workbooks, so this merge run has nothing to convert;
  the acceptance fire proves the document's exit and the merge, not a non-empty partition. The last non-empty
  partition is 2026-09-27 (7,637 rows).
- The enrichment line changed from `[enrich] bd_assets_dim unavailable; skipping cusip join` (2026-09-28) to
  `[enrich] cusip: 0/0 non-null (0.00%)` (2026-09-29): the dim join is no longer skipped on this path (0 rows, so 0/0).
  That bears on row Z-W11-S2; the join's result on non-empty data is unmeasured.

## (4) Rollback to the prior document version

`opal-bd-transaction-download` today: DefaultVersion 1 (2026-02-19), LatestVersion 2 (2026-02-23, what the trigger
runs). Both carry the Playwright download. Versions are immutable, so the prior content is always readable:
`aws ssm get-document --name opal-bd-transaction-download --document-version 2`.

PHASE B publishes version 3 and sets DEFAULT to it. Because the trigger runs `$LATEST` (row Z-S48), rolling back
means re-publishing version 2's content as the next version (`update-document`, then `update-document-default-version`
to it) so that DefaultVersion == LatestVersion again; moving DEFAULT back to 2 alone changes nothing the trigger runs.
The rollback restores a document that fails at the login (21 of 21), whose merge step still runs.

## Criteria at this cut (amended checks read from CLOUD)

AC1 FAIL (served `$LATEST`: playwright refs 1, BD_PASSWORD refs 2, merge refs 2; Default 1, Latest 2), AC2 PASS (rule
ENABLED, 1 target), AC3 FAIL (no PHASE B GO). AC1 and AC3 need PHASE B by construction.
