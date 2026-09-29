# ANNOUNCE -- MX-s-14 PHASE A (amendments A1 + A2): strip the dead Playwright download from ALL FOUR BD daily documents, keep each merge

Worker: 0.9.0_WK_NFRA_MCPINDEX~17 (issuer 2.0.0_SA_COO~MI). Order (amended A2, CLOUD @1d62ade62e):
org/missions/D9/NFRA/NFRA_MCPINDEX/task-orders/NFRA_MCPINDEX.TO-MX-s-14.bd-transaction-rest-port.md

STATE: PHASE A only. The 4 documents are edited in the repo and NOT published. All 4 triggers stay as they are
(`bd-transaction-pipeline-trigger` reads ENABLED). Served versions, unchanged at the last read:

| document | trigger slot (UTC) | instance the trigger starts | Default | Latest (what the trigger runs) |
| --- | --- | --- | --- | --- |
| `opal-bd-unrealized-download` | 21:38 | i-0800437d1dbb0b5cc (bd-allocations) | 2 | 2 |
| `opal-bd-realized-download` | 21:45 | i-0800437d1dbb0b5cc | 2 | 2 |
| `opal-bd-transaction-download` | 21:53 | i-00c7568bc510f7423 (bd-transactions) | 1 | 2 |
| `opal-bd-allocation-download` | 22:00 | i-0800437d1dbb0b5cc | 3 | 4 |

CARRIER NOTE (row Z-W17-S7, BLOCKING): safe-commit refused the 3 A2 documents at their repo paths, because this branch's copy of
the order predates A2 and its `<paths>` do not grant them. The transaction document is committed (c93e1c4fa4). The other 3 are
edited in the worktree, uncommitted, and carried byte-identical (sha256 first 16: allocation 559048c8290150fc, realized
570538ea79ddfe59, unrealized b33bb4201627f2d8) under `deliverables/0.9.0_WK_NFRA_MCPINDEX~17/edited_documents/`.

Two documents carry Default != Latest today (transaction 1/2, allocation 3/4). PHASE B sets DEFAULT == LATEST on each
(row Z-S48). Test budget: 4 ad-hoc merge-only runs (plus one repeat, below), ZERO vendor calls.

## SUPERSEDED: the new REST module

`pull_bd_transaction_rest.py` (16d142659d) was removed from the branch by `git rm` in c93e1c4fa4; never published, never
run against the vendor. Rows Z-W17-S1/S2 lapsed with it (row Z-W17-S4).

## (1) The 4 SSM documents are the only writes

Files changed: `infra/aws/ssm/opal-bd-{transaction,allocation,realized,unrealized}-download.json`; nothing else in the
repo except this announcement, the proof and channel rows. Per document, REMOVED: the `opal/bd/credentials` fetch,
`BD_USERNAME`/`BD_PASSWORD`, the `aws s3 sync` of `scripts/src`, the chown, the `bun run ... download-daily-*.ts` step and
its `DOWNLOAD_RC`. KEPT: the merge step, the log upload, `shutdown -h +2 &` ARMED BEFORE the failure exit (the served
documents exit first and strand the instance), the honest exit on `MERGE_RC`; realized and unrealized also keep their
`shutdown -c` opener. Offline counts on each edited command list: `BD_PASSWORD` 0, `download-daily` 0, `secretsmanager` 0,
`merge-daily-incremental` 2, non-ASCII characters 0.

Untouched: the Terraform rules, the 4 trigger Lambdas, `merge-daily-incremental.py`, IAM, every bronze object, the
vendor. The test runs DID write served silver where the merge had a new file (realized only, below); that is what the
scheduled run does with the same command.

## (2) Each merge step is byte-unchanged (diff of served `$LATEST` against the edit)

The merge step is the block from `# Run <name> silver conversion` to `echo "Merge exit code: $MERGE_RC"`
(realized and unrealized include their `mkdir -p lib && aws s3 sync .../scripts/lib/` line).

| document | block lines | identical | difference |
| --- | --- | --- | --- |
| transaction | 8 | 7 | the first line, a COMMENT: served has a double-encoded em dash, the edit an ASCII hyphen |
| allocation | 8 | 7 | the same comment line |
| realized | 9 | 9 | none |
| unrealized | 9 | 9 | none |

```
transaction and allocation, the whole diff:
< # Run <name> silver conversion <mojibake dash> capture exit code
> # Run <name> silver conversion - capture exit code
realized, unrealized: no diff
```

Nothing that executes moved in any of the four.

## (3) Baselines and tests

Baseline = the prior scheduled merge, 2026-09-28 (logs `logs/<name>-download-2026-09-28.log`; each shows
`Download exit code: 1` then a merge that ran and exited 0).

| document | prior scheduled merge (2026-09-28) | test run (2026-09-29, merge only, 0 vendor calls) |
| --- | --- | --- |
| transaction | processed 193, 1 new: `TRANSACTIONS_DAILY_2026-09-28.xlsx` -> `silver/transactions/2026-09-28.parquet`, 0 rows, partitions 194 | A1 run `cdb144c8-b4de-4ef1-b5d8-4c36509ca6fc` (on i-0e6f6dc014fdcf1cd, see row Z-W17-S6): 1 new, `TRANSACTIONS_DAILY_2026-09-29.xlsx` (4,355 bytes, empty) -> `silver/transactions/2026-09-29.parquet`, 0 rows, partitions 195. Repeat on the trigger's own instance `e3047e12-0cce-4098-8e96-93e429c918d1`: Success rc 0, processed 195, `No new files to process` |
| allocation | processed 131, `No new allocation files to process` | `84e569c5-ab30-4620-8540-e9b6d9311c43`: Success rc 0, processed 131, `No new allocation files to process`; no partition written |
| realized | processed 142, 1 new: `REALIZED_DAILY_2026-09-28.xlsx` -> `silver/realized/2026-09-28.parquet`, 11,298 rows (198 duplicates removed), partitions 143 | `ca1fdba2-14f8-42ff-b202-35d633f456db`: Success rc 0, processed 143, 1 new: `REALIZED_DAILY_2026-09-29.xlsx` -> `silver/realized/2026-09-29.parquet`, 10,915 rows (159 duplicates removed, parquet metadata 10,915, LastModified 2026-09-29T07:02:56Z), partitions 144 |
| unrealized | processed 68, 6 new (2026-07-03..07-09) each 0 rows, partitions 74 | `95a997c8-5d46-408c-9501-228dd28be442`: Success rc 0, processed 74, `No new unrealized files to process`; no partition written |

Every test run uploaded its log, armed the shutdown (the instance stopped itself) and printed `Done.`. The allocation test
list omits the `bd-price-update` invoke, so no downstream Lambda fired (row Z-W17-S5, ARMED, below).

Reading the baseline for the scheduled fires: transaction expects 195 partitions and any new `TRANSACTIONS_DAILY_*`;
allocation 131 processed; realized 144 partitions with 2026-09-29 already written (a new day's file is what it should
add); unrealized 74 processed. That the merge skips an object it has already processed is now MEASURED on transaction
(repeat run: `Previously processed: 195`, `No new files`).

Two things the tests showed, stated and not resolved:
- The transaction bronze for 2026-09-28 and 2026-09-29 are empty workbooks (last non-empty partition 2026-09-27, 7,637 rows),
  and allocation and unrealized had nothing new: the acceptance fires for those three prove the document's exit and
  the merge, not a non-empty partition. Only realized had data (10,915 rows).
- The transaction merge's enrichment line changed from `bd_assets_dim unavailable; skipping cusip join` (09-28) to
  `cusip: 0/0 non-null` (09-29): the dim join is no longer skipped on this path; its result on non-empty data is
  unmeasured (row Z-W11-S2).

ROW Z-W17-S5, ARMED, disarm owner 2.0.0_SA_COO~MI, DECIDE BEFORE PHASE B: the allocation document invokes the
`bd-price-update` Lambda (async) after a successful merge. That branch has been unreachable since 2026-06-23 (the
download always failed first). With the strip it fires on the first PHASE B fire. The edited file KEEPS the invoke; what
the Lambda does with a daily call after a 3-month gap is unmeasured.

## (4) Rollback

The triggers run `$LATEST`, so moving DEFAULT back changes nothing they run. Rollback per document is: read the prior
`$LATEST` content from its immutable version, re-publish it as the next version (`update-document`), and set DEFAULT to
that new version so Default == Latest again.

| document | prior `$LATEST` content to re-publish | read it with |
| --- | --- | --- |
| transaction | version 2 (2026-02-23) | `aws ssm get-document --name opal-bd-transaction-download --document-version 2` |
| allocation | version 4 | `... opal-bd-allocation-download --document-version 4` |
| realized | version 2 | `... opal-bd-realized-download --document-version 2` |
| unrealized | version 2 | `... opal-bd-unrealized-download --document-version 2` |

Each restores a document whose download fails at the login (70 of 70 dated logs) with the same merge after it. In the repo
the served `$LATEST` equals the pre-edit file for realized, unrealized and allocation; for transaction it differs by two
comment lines (the double-encoded dashes).

## Criteria at this cut

AC1-AC3 grade the transaction document as written; the amended checks read from CLOUD: AC1 FAIL (served `$LATEST`:
playwright refs 1, BD_PASSWORD refs 2, merge refs 2; Default 1, Latest 2), AC2 PASS (rule ENABLED, 1 target), AC3 FAIL (no
PHASE B GO). AC1 and AC3 need PHASE B by construction. The same predicates on the other 3 documents are per-document
rows in the proof, and are graded at L9.

## PHASE B RECORD (amendment A3, GO by 2.0.0_SA_COO~MI; halves SIGNED for 3 legs, allocation carved out)

Published 2026-09-29T08:25-08:27Z, outside 21:30-22:15Z, with the NEVER-2 ledger `nfra-mcpindex-bd-playwright-strip` open first
(commit 8cd7d48a4c). Per leg, `update-document --document-version '$LATEST'` from the repo file, then
`update-document-default-version`, then a `get-document` read-back:

| leg | document | version before (Default/Latest) | version after | read-back content sha256 first-16 == repo file | Default/Latest after |
| --- | --- | --- | --- | --- | --- |
| L2 | opal-bd-unrealized-download | 2/2 | 3 | b33bb4201627f2d8, bytes equal | 3/3 |
| L3 | opal-bd-realized-download | 2/2 | 3 | 570538ea79ddfe59, bytes equal | 3/3 |
| L4 | opal-bd-transaction-download | 1/2 | 3 | af59a64d5ca315b0, bytes equal | 3/3 |

`s14.AC1` reads PASS (Default 3, Latest 3; playwright refs 0, BD_PASSWORD refs 0, merge refs 2), `s14.AC2` PASS (rule ENABLED).
Rollback per leg is section (4) above: re-publish v2 (content hashes e2bbc0febde98668 unrealized, cd2bf147c44653f7 realized,
18f27fcdf008975b transaction) as the next version and set DEFAULT to it. The ledger stays OPEN: L5 is tonight's 21:38, 21:45
and 21:53Z scheduled fires; L6 is the git leg.

ALLOCATION (re-cut per the CTO ruling in A3, NOT published; served stays Default 3, Latest 4): the `bd-price-update` invoke block is
removed and one log line says it is not invoked. Offline: `lambda invoke` 0, `aws lambda` 0, `bd-price-update` appears once
(that log line), BD_PASSWORD 0, download-daily 0, secretsmanager 0, merge-daily-incremental 2; the merge block is 7 of 8
lines identical to served v4 (the 8th the comment dash). Content sha256 first-16 `66431932a7ad0f55`, committed at a1a912c90a.
This supersedes the allocation hash 559048c8290150fc above and the row Z-W17-S5 hazard for the re-asked leg.

## ALLOCATION LEG RECORD (GO ec43dd0e33; halves SIGNED on content 66431932a7ad0f55: CTO @5e553da893, CVO @ae5e48d41c)

Published 2026-09-29T09:15Z, outside 21:30-22:15Z, after ledger legs L7-L9 were committed (138ed30f0a). `opal-bd-allocation-download`:
version before Default 3 / Latest 4, after v5, Default 5 / Latest 5. `get-document` `$LATEST` content sha256 first-16
`66431932a7ad0f55` equals the repo file byte for byte; `lambda invoke` 0, `BD_PASSWORD` 0. The other 3 documents were not touched
(3/3 each). Rollback: re-publish the v4 content (sha256 first-16 `3c17e61812af49f7`) as the next version and set DEFAULT to
it. L9 (the 22:00Z acceptance fire) stays OPEN.
