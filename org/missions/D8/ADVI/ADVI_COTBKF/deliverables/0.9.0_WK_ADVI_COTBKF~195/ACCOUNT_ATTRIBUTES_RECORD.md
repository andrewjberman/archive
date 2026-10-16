# ACCOUNT_ATTRIBUTES_RECORD -- CB-db-1 (round 105, worker 0.9.0_WK_ADVI_COTBKF~195)

Counts, file names and roles only. No account identifier, name or dollar value.

## Objects measured (read-only S3, opal-data-cot)

- Silver, stale: `silver/account_attributes/2026-08-19.parquet` (943 rows, 942 accounts).
- Bronze, newest pull: `forwardfill_v2/account_attributes/ACCOUNT_ATTRIBUTES_DAILY_2026-10-15.xlsx`, sheet `Sheet1` (1127 rows, 1004 accounts).
- The bronze listing ends at the 2026-10-15 file; the silver prefix holds one partition.

## Drift (silver 2026-08-19 to bronze 2026-10-15)

- Accounts added 62, removed 0, shared 942.
- Changed among shared accounts: billable 45, portfolio group 130, supervised 0, position-only 0, any column 171.
- Multi-book accounts: 1 in silver, 122 in bronze; 0 bronze multi-book accounts disagree on a flag.

## The rule the step releases

- `A_00.accounts_dimension.py` (load_account_attributes, lines 371-432) asserts the three flags agree across a multi-book account's rows, and keeps the first row's portfolio group in partition order.
- Partition order is bronze row order (`cot_silver_merge.py` lines 489 and 498), so the gold book choice at a multi-book account follows the bronze file's row order.

## Gold readers and writers

- Scripts scanned: 97 `.py` files under `data/cot/scripts/gold/` (recursive).
- Matched the four column names: 5 files.
- Readers: `D_05.supervised_split.py` (dimension supervised flag; latest silver portfolio-group pairs); `test_cot_supervised_tieout.py` (a test; the same two reads).
- Writer: `A_00.accounts_dimension.py` (the four columns into the dimension).
- Name matches that are neither readers nor writers of the dimension: `B_00.canonical_holdings.py` carries an `account_supervised` column read from the silver holdings snapshot and written into canonical holdings; `A_02.fee_rate_history.py` maps a source column name for billable.
- `gold_validate_config.yaml` (a config, not a script) checks the four columns are present on the dimension.

## Not established

- One bronze day only; no later day and no served output was read.
- The live SSM document was not read; the plan check reads one in-place change against the held Terraform copy.
- Multi-book counts are by raw bronze rows per account, not by distinct portfolio group.
