# Daily holdings per account (CB-l-1)

Rebuilt from the transactions: the signed quantity held of each security on each NYSE trading day, from each account's first to its last transaction date. No price is used. A transaction dated on a non-trading day takes effect on the next trading day. Cash securities (FDIC*, CFNCASH) are kept in the table; the snapshot comparison excludes them. A quantity within 1e-06 of zero is not stored.

- accounts: 1533
- account_days: 1691729
- holding_rows (non-zero account, date, cusip): 23226716
- daily_holdings.parquet: 18241175 bytes, sha256 88476c4a37a5acafbebd3a24a94acd3dde600100dc52a411d8e5423148281895
- accounts whose last daily state differs from the full rebuild: 0

## Snapshot check (2026-06-23, non-cash)

- snapshot_accounts: 83
- snapshot_pairs (the snapshot's pairs plus rebuilt-open pairs of those accounts): 394
- snapshot_equal (within 0.001): 381
- snapshot_diffs (every one is a row of snapshot_differences.csv): 13, over 3 accounts
- the crosswalk's REBUILD-CHECK basis (pairs the snapshot rows themselves hold): pairs=381 equal=381

Largest five differences by absolute delta (account, cusip, rebuilt, snapshot, delta):

- acct#3b5864a2, 56585A102, 1.014000, 0.000000, 1.014000
- acct#3b5864a2, 78462F103, 1.000000, 0.000000, 1.000000
- acct#3b5864a2, 037833100, 0.970000, 0.000000, 0.970000
- D49141617, 922908751, 0.837000, 0.000000, 0.837000
- D49141617, 30231G102, 0.825000, 0.000000, 0.825000

Blind spot: corporate actions the transactions do not record.
