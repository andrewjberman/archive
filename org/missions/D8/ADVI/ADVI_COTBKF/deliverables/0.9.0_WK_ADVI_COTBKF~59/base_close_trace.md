# CB-af-1 base close trace (round 32)

READ-ONLY. Class rule written in the script before its first run (TOL 0.5%, SHARE 80%). Yahoo: yfinance 1.2.0, one history call per symbol, auto_adjust=False.

## Source the chain reads (all CUSIPs)

- store id: `cottonwood-silver-canonical-prices` (commonwealth_price_census.STORES[0]); object `s3://opal-data-cot/silver/prices/canonical_prices.parquet`
- series key: column `ticker` (key_cols={'ticker': 'ticker'}); date column `date`; FIELD read: column `price`; label column `source`
- pricing: security_day_prices() takes the stored row dated the SAME day only (no carry-forward); first store wins.

## 808524102 SCHB

- stored row(s) for 2022-10-12: series date 2022-10-12 price 13.330209 source yahoo_finance
- stored rows for the ticker: 2165; source labels: {'yahoo_finance': 1487, 'linear_interpolation': 678}
- informational: nearest earlier Yahoo bar (<=10 bars) whose Close the 2022-10-12 chain price matches within 0.5%: none
- sampled days skipped (no Yahoo bar or no stored same-day row): 2021-01-01, 2022-01-01, 2022-10-01, 2023-01-01, 2023-04-01, 2023-07-01, 2023-10-01, 2024-01-01, 2025-01-01, 2026-01-01

| day | chain (r26 stored) | r28 scaled | Yahoo Close | Yahoo Adj Close | chain/Close | chain/AdjClose |
|---|---|---|---|---|---|---|
| 2020-07-06 | 11.5661 | 69.3968 | 12.5533 | 11.5044 | 0.9214 | 1.0054 |
| 2020-10-01 | 12.4166 | 74.4993 | 13.3933 | 12.3503 | 0.9271 | 1.0054 |
| 2021-04-01 | 15.2229 | 91.3376 | 16.3050 | 15.1417 | 0.9336 | 1.0054 |
| 2021-07-01 | 16.3622 | 98.1733 | 17.4717 | 16.2749 | 0.9365 | 1.0054 |
| 2021-10-01 | 16.4599 | 98.7591 | 17.5200 | 16.3720 | 0.9395 | 1.0054 |
| 2022-04-01 | 16.8845 | 50.6534 | 17.8533 | 16.7943 | 0.9457 | 1.0054 |
| 2022-07-01 | 14.1362 | 42.4086 | 14.8867 | 14.0607 | 0.9496 | 1.0054 |
| 2022-10-12 | 13.3302 | 39.9906 | 13.9800 | 13.2590 | 0.9535 | 1.0054 |
| 2024-04-01 | 19.8048 | 59.4143 | 20.2967 | 19.6990 | 0.9758 | 1.0054 |
| 2024-07-01 | 20.5441 | 61.6324 | 20.9867 | 20.4344 | 0.9789 | 1.0054 |
| 2024-10-01 | 21.5642 | 64.6925 | 21.9600 | 21.4490 | 0.9820 | 1.0054 |
| 2025-04-01 | 21.3582 | 21.3582 | 21.6100 | 21.2441 | 0.9883 | 1.0054 |
| 2025-07-01 | 23.6128 | 23.6128 | 23.8200 | 23.4867 | 0.9913 | 1.0054 |
| 2025-10-01 | 25.6494 | 25.6494 | 25.8000 | 25.5125 | 0.9942 | 1.0054 |
| 2026-04-01 | 25.3000 | 25.3000 | 25.3000 | 25.1649 | 1.0000 | 1.0054 |

**class: other_source** -- other_source:yahoo_finance (adj matches 0/15, stale matches 4/15; chain/Close 0.9214..1.0000, chain/AdjClose 1.0054..1.0054)

## 808524839 SCHZ

- stored row(s) for 2022-10-12: series date 2022-10-12 price 19.718094 source yahoo_finance
- stored rows for the ticker: 1337; source labels: {'yahoo_finance': 914, 'linear_interpolation': 423}
- informational: nearest earlier Yahoo bar (<=10 bars) whose Close the 2022-10-12 chain price matches within 0.5%: none
- sampled days skipped (no Yahoo bar or no stored same-day row): 2023-01-01, 2023-04-01, 2023-07-01, 2023-10-01, 2024-01-01, 2025-01-01, 2026-01-01

| day | chain (r26 stored) | r28 scaled | Yahoo Close | Yahoo Adj Close | chain/Close | chain/AdjClose |
|---|---|---|---|---|---|---|
| 2022-10-12 | 19.7181 | 39.4362 | 22.4650 | 19.3014 | 0.8777 | 1.0216 |
| 2024-04-01 | 21.0005 | 42.0010 | 22.7650 | 20.5567 | 0.9225 | 1.0216 |
| 2024-07-01 | 21.0526 | 42.1052 | 22.6000 | 20.6077 | 0.9315 | 1.0216 |
| 2024-10-01 | 22.3516 | 44.7031 | 23.7650 | 21.8792 | 0.9405 | 1.0216 |
| 2025-04-01 | 22.2532 | 22.2532 | 23.1800 | 21.7830 | 0.9600 | 1.0216 |
| 2025-07-01 | 22.4537 | 22.4537 | 23.1500 | 21.9792 | 0.9699 | 1.0216 |
| 2025-10-01 | 22.9788 | 22.9788 | 23.4500 | 22.4932 | 0.9799 | 1.0216 |
| 2026-04-01 | 23.1600 | 23.1600 | 23.1600 | 22.6706 | 1.0000 | 1.0216 |

**class: other_source** -- other_source:yahoo_finance (adj matches 0/8, stale matches 0/8; chain/Close 0.8777..1.0000, chain/AdjClose 1.0216..1.0216)

BASE-TRACE cusips=2 adj_close_base=0 stale_carry=0 other_source=2 untraced=0
