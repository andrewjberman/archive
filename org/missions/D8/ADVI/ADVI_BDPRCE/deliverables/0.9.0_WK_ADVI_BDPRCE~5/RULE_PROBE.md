# BP-b-1 RULE_PROBE -- R1 run over the real silver/transactions partitions

Worker `0.9.0_WK_ADVI_BDPRCE~5`, branch `wk-ADVI_BDPRCE-5`, cut from `73a2b77c3c`. Record: `RULE_PROBE.json` (same folder).

## Reads (claim: measured)

- Four partitions via `aws s3api get-object --bucket opal-data-bd --key silver/transactions/<date>.parquet` (READ only, no write):
  2026-09-22 (52,792 rows), 2026-10-08 (84,533), 2026-10-09 (6,278), 2026-10-12 (0 rows, 74 columns).
- Local MD5 equals the S3 ETag for all four partitions.
- Determinism: the probe ran in two separate processes. Both outputs are MD5 `9f139dfd1ec5936e899902472dda4069`, byte-equal.

## R1 as built (`data/black_diamond/scripts/silver/bd_price_rule.py`)

- Variant A = {Buy, Sale} (the ruling as written). Variant B = A + Dividend Reinvestment (sensitivity only).
- Price = the executed `price` column. `market_value` and `units` are never read.
- Each `transaction_id` counts once (first row by file order). The price is the median of the distinct trades.
- The date key is `trade_date`. The file a row sits in does not decide it.
- An asset with no qualifying trade is ABSENT. `carry_forward` returns its observation date.

## Named assets

- **EXXONMOBIL HOLDINGS CORP COM SHS, 2026-10-09:** A absent, B absent. Its only rows that day are 4 Transfer In rows (1 id, price 168.94), excluded by clause 1. The task order's expected 168.94 is that non-trade row. Clause 5 carry-forward: 168.29, observed 2026-10-08 (Sale, id 744808349).
- **BLACKROCK INC COM, 2026-09-22:** A absent (no Buy or Sale rows; only Dividend and Dividend Reinvestment rows). B = 1074.9259, the median of 4 distinct Dividend Reinvestment ids. The task order expected a trade price under R1; under variant A there is none.
- Control: EXXONMOBIL HOLDINGS CORP COM SHS, 2026-09-22: A = B = 158.6701 (1 Sale id, 5 rows). `rows_used` 5 against 1 distinct id shows clause 2.

## Variant totals (four dates, asset-dates)

- A: 687 priced, 187 absent.
- B: 715 priced, 159 absent. 28 assets are priced under B only.
- No trade row lacked a valid price (`no_price_excluded` 0 under both variants).
- 5 Buy rows on 2026-09-22 carry no asset_name (one id, price 1.0). They name no asset, so they are counted and not priced.

## Excluded by type, variant A (rows on the four dates)

Dividend 50,597; Dividend Reinvestment 31,424; Transfer In 637; Cash Deposit 793; Cash Withdrawal 375; Transfer Out 221; Expense 403; Income Reinvestment 81; Journal 52; Interest 24; Capital Gains 18. Total 84,625 excluded, against 58,743 Buy and Sale rows (Sale 39,656 and Buy 19,087, which includes the 5 null-asset Buy rows counted under `no_asset_excluded`). Denominator 143,368 rows on the four dates = 84,625 + 58,743.

## Types seen (raw rows whose trade_date is one of the four dates)

Sale 39,656; Dividend 50,597; Buy 19,087; Dividend Reinvestment 31,424; Cash Deposit 793; Cash Withdrawal 375; Transfer In 637; Transfer Out 221; Expense 403; Journal 52; Interest 24; Income Reinvestment 81; Capital Gains 18. Thirteen types, with 143,368 rows (each type's count in the JSON `types_seen`).

- Unclassified: none. Every type seen is in `KNOWN_TYPES`.
- Judgment for the CTO: Income Reinvestment is excluded by name as a non-trade (it is not in B).
- Valuation appears in the 2026-09-22 file (33 rows), dated 2026-08-31, not on a target date. It is named non-trade in the module.

## DEC-6 seam

- 10 rows dated 2026-10-08 sit in the 2026-10-09 partition. The probe reads the union, so they count toward 2026-10-08. Per-file counts are in the JSON `per_date`. Trade ids shared across files: 0.
- The 2026-10-12 partition holds zero rows. R1 yields no price for any asset on that date.
