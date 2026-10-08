# RELEASE_LOCAL_RUN -- IRPT_DASHBD.TO-DB-b-41 (counts only)

Local runs only: S3 reads, nothing written to S3. The record is `RELEASE_LOCAL_RUN.json` (built by `release_local_run.py`); the window
key check is `KEY_UNIQUENESS_WINDOW.json` (built by `key_uniqueness_window.py`).

## A. The extended handler against the round-25 handler (`handler.py --local`, 2026-10-05, 20 accounts)

The before side is the round-25 handler AND that commit's declaration (`git show 5ffd7b740d:` of `handler.py` and of `sources.json`), so
the equality below also covers the `lot_source` object added to the declaration. The after side is the handler and the declaration at
this branch, with `--class-out` and `--lots-out-dir`. The 20 accounts are the first 20 of the 100-account list in
`deliverables/0.9.0_WK_IRPT_DASHBD~20/ACTIVITY_LOTS_LOCAL_RUN.json` (row IRPT_DASHBD-W23-S4).

| Quantity | Count |
|---|---|
| accounts requested | 20 |
| `account_return_daily` rows, before / after | 18 / 18 |
| sha256 of the returns parquet, before | `8d18f775a8400d76dd16b8d0dd708664b73d8da72b39106be45e9903c13f073e` |
| sha256 of the returns parquet, after | `8d18f775a8400d76dd16b8d0dd708664b73d8da72b39106be45e9903c13f073e` |
| returns table byte-identical (DELTA) | 0 bytes |
| `account_class_daily` rows, before / after | 67 / 67 |
| sha256 of the class parquet, before | `199c636225c1db5e129229e28af7e9df4fb61b74b94f93a43058807933ecaa5e` |
| sha256 of the class parquet, after | `199c636225c1db5e129229e28af7e9df4fb61b74b94f93a43058807933ecaa5e` |
| class table byte-identical (DELTA) | 0 bytes |
| `account_activity_daily` rows (all MEASURED) | 18 |
| `account_lot_realized` rows | 0 |
| `account_lot_unrealized_daily` rows | 1,330 |
| unrealized rows by `basis_source`: CUSTODIAN / WASH_SALE_EXCLUDED_BASIS | 1,291 / 39 |
| repeated primary keys, activity / realized / unrealized | 0 / 0 / 0 |
| wall time, before / after | 34.6 s / 69.5 s |
| peak working set, before / after | 228.4 MB / 992.2 MB |

## B. The primary keys over the window the one-day run cannot show (same 20 accounts, 2026-09-01..2026-10-05, 24 trading days)

The one-day run closes no realized lot for these accounts (0 rows), so the realized key was also checked over the window with the
producer's own `compute_local`, then `emit_day(upload=False)` on every table-day (it refuses a repeated key).

| Table | Rows | Days with rows | Distinct keys | Repeated keys | Table-days dry-emitted / refused |
|---|---|---|---|---|---|
| `account_activity_daily` | 432 | 24 | 432 | 0 | 24 / 0 |
| `account_lot_realized` | 30 | 2 | 30 | 0 | 2 / 0 |
| `account_lot_unrealized_daily` | 30,183 | 24 | 30,183 | 0 | 24 / 0 |

Rows outside the window's days: 0 in each table. Realized rows by `basis_source`: CUSTODIAN 24, WASH_SALE_EXCLUDED_BASIS 6.
Unrealized rows: CUSTODIAN 29,204, WASH_SALE_EXCLUDED_BASIS 974, IN_KIND_TRANSFER_VALUE 5.

## C. Not measured here

Population scale (7,597 accounts, 380 times this sample): rows, wall time and memory of the lots stage (row IRPT_DASHBD-W23-S2).
