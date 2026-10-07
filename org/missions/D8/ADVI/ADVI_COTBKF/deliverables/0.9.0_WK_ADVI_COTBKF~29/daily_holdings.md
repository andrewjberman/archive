# Daily holdings per account (CB-l-1)

Rebuilt from the transactions: the signed quantity held of each security on each NYSE trading day, from each account's first to its last transaction date. No price is used. A transaction dated on a non-trading day takes effect on the next trading day. Cash securities (FDIC*, CFNCASH) are kept in the table; the snapshot comparison excludes them. A quantity within 1e-06 of zero is not stored.

- accounts: 1533
- account_days: 1691729
- holding_rows (non-zero account, date, cusip): 22547096
- daily_holdings.parquet: 18191131 bytes, sha256 37f66c7e0d4981519acc3689813e4e3e8bab64d7e695cc39a3b74ae67c8e3198
- accounts whose last daily state differs from the full rebuild: 0

## Snapshot check (2026-06-23, non-cash)

- snapshot_accounts: 83
- snapshot_pairs (the snapshot's pairs plus rebuilt-open pairs of those accounts): 381
- snapshot_equal (within 0.001): 381
- snapshot_diffs (every one is a row of snapshot_differences.csv): 0, over 0 accounts
- the crosswalk's REBUILD-CHECK basis (pairs the snapshot rows themselves hold): pairs=381 equal=381

Largest five differences by absolute delta (account, cusip, rebuilt, snapshot, delta):

- none

## Fractional residuals (all accounts, non-cash)

- fractional_residuals (account-security pairs holding a non-zero quantity under one share after their last transaction; every one is a row of fractional_residuals.csv): 5
- fractional_accounts: 5

Blind spot: corporate actions the transactions do not record.
