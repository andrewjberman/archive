# ADVI_BDPRCE round 2 -- L5 ground truth (2.0.0_SA_COO~K1, 2026-10-13 ~19:5xZ, dell1)

Claims: MEASURED (a read this seat ran), READ (a file read at the cited line), CARRIED (stated in a record this seat read), NOT-READ (the worker's to establish).

| # | fact | claim | source |
|---|---|---|---|
| 1 | round 1 closed @c5c796789b; CVO compile @4d3a201022 (27 rows: 7 ARMED, 8 INERT graduated, 12 dismissed); analysis @9b241147f6 | MEASURED | `git log`; the analysis file |
| 2 | THE rule R1: median of DISTINCT trades (each `transaction_id` once), trades only at the executed `price` column, every non-trade row excluded, ties by `SOURCE_RANK` then a stable sort, no trade on the date -> carry-forward with its observation date; interpolation banned | CARRIED | `ledger/CTO_RULING_R1_THE_PRICE_RULE_20261013.md`; analysis section 2 |
| 3 | `silver/transactions/2026-10-09.parquet` columns include `transaction_id`, `transaction_type`, `price`, `units`, `market_value`, `trade_date`, `asset_name`, `account_id`; 6,278 rows, 1,271 distinct ids | MEASURED | read of the partition |
| 4 | transaction types on that partition (rows / distinct ids): Buy 2,138/430; Sale 1,955/357; Dividend 816/174 (price 1.0); Cash Deposit 346/83; Dividend Reinvestment 310/60; Transfer In 293/81; Transfer Out 145/29; Cash Withdrawal 145/30; Journal 56/12; Expense 42/11; Capital Gains 18/2; Interest 14/2 | MEASURED | the same read |
| 5 | `data/black_diamond/scripts/silver/` holds `bd_price_update.py`, `inject_scoped_overrides.py`, `merge-daily-incremental.py`, `lib/`, `tests/` (with `test_bd_silver_etag.py` and others) | MEASURED | `ls` |
| 6 | a path under `infra/` or an invocation with a deploy verb raises an order's risk floor to WORLD; a new file under `data/black_diamond/scripts/silver/` is LOCAL by the floor | READ | `.tools/to-pipeline-gate.py:1388-1399` |
| 7 | the thread object of round 1: `entities/clients/z08334146/detail.json` (normal client, 3 accounts, 110 lots); the catch-all `entities/clients/0/detail.json` holds 210 accounts, 3,052 lots | MEASURED | re-open by this seat |
| 8 | client objects total about 3,509 (the worker's sample was 120 of 3,509); the served `data_as_of` of the thread object is 2026-10-09 | CARRIED | W4 report |
| 9 | the six dates with no daily price file: 2026-09-21, 09-22, 09-28, 09-29, 10-05, 10-06 (Mon and Tue, each a trading day) | CARRIED | `REMEDIATION_v1.md` W3-S2 |
| 10 | the producer of the served platinum detail objects, the schedule of the daily price Lambda on the six dates, and the template's S3 VersionId at apply time | NOT-READ | BP-b-5, BP-b-6 |
| 11 | the three live rules before R1: T1 as written (1,148 of 1,657 served rows), JOB 2 price-first (`bd_price_update.py:677-706`, 169 rows), a dividend-excluding price-column median (62 rows, post-hoc) | CARRIED | `GAP.md` |
| 12 | no CloudOps lane is seated to this project; one lane holds one project, and `0.7.0_AE_CloudOps~DELL1` holds MDPF_CANON per the pivot packet | CARRIED | `DIRECTION_DELL1_20261013.md` section 4 |
