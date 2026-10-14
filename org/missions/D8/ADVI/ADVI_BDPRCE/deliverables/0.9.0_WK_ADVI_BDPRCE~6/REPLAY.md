# BP-b-2 -- R1 replayed over the served prices (read-only, moves nothing)

Worker `0.9.0_WK_ADVI_BDPRCE~6`, cell BP-b-2, round 2. Record: `REPLAY.json`; list: `BEFORE_AFTER.csv` (1,657 lines, 298,088 bytes, under the 5 MB bound, committed); estimated rows: `ESTIMATED_ROWS.csv` (18,566 lines). Scripts: `replay_r1.py` (the replay; imports `data/black_diamond/scripts/silver/bd_price_rule.py`, read and not changed), `lookback_scan.py` (the carry-forward lookback). Claim: measured. No S3 write, no producer run, no served object or product file changed.

## What R1 is

The price for an asset on a date is the median of that date's distinct buy and sale trades, each `transaction_id` counted once, at its executed `price`. Dividends, cash, transfers and every other non-trade row are excluded. If an asset has no trade on the date, the last observed R1 price is carried forward and is labelled with its observation date. Interpolation is not used. Rows are keyed on `trade_date`, not on the partition file they sit in.

## Denominator

Window 2026-09-16..2026-10-13: 20 weekday dates. The re-read `canonical_prices.parquet` (ETag `0ba9bd51...`, modified 2026-10-13T12:48:05Z) holds 1,657 `transaction_observed` rows, the same count as round 1. Every row has a unique asset-date.

## Result (variant A, trades only)

| class | rows |
|---|---|
| UNCHANGED | 621 |
| CHANGED | 539 |
| NOW_CARRY_FORWARD | 285 |
| NOT_RECOMPUTABLE | 212 |
| sum (= served rows) | 1,657 |

- Prices that move: 811 (539 changed plus 285 carry-forwards, less 13 carry-forwards that happen to equal the served price). Of the 539 changed rows, 524 move up and 15 move down.
- Variant B (adds Dividend Reinvestment) is a sensitivity only. It changes 780 rows against the served price.
- 285 rows carry a price forward from an earlier date. 59 of those observations are dated before 2026. 212 rows have no R1 trade anywhere in the store from 2020-03-06 to the window, so they stay NOT_RECOMPUTABLE.
- Old price source: of the 285 carry-forwards, 240 have a served price that only non-trade row groups reproduce (153 Transfer In alone, 51 Dividend Reinvestment alone, 26 Income Reinvestment alone, and 10 mixed or other non-trade groups), and 45 reproduce from no group. Under variant B, 99 of the carry-forwards get a trade price on their own date.

## Three largest movers (absolute change)

1. WATSCO INC COM, 2026-09-17: 305.36 becomes 432.39. Carry-forward from 2026-04-28. The served price came from Transfer In rows.
2. MIAMI-DADE CNTY FLA EDL FACS A 5.25% 04/01/2031, 2026-10-09: 1.0419 becomes 104.19. This is a unit-scale difference, not a price move. The trade price is quoted per 100 of par; the served price is per 1.
3. MISSOURI ST HEALTH & EDL FACS 5% 05/01/2033, 2026-10-09: 1.0401 becomes 104.01. Same scale difference.

Eight changed rows are of this kind (flag `scale_100x`). Without them, the median absolute move of the changed rows is 0.00214.

## Named reasons

- Flags: `dividend_dominated` 92, `repeat_weighted` 106, `scale_100x` 8. `estimated_row` is 0 on every served row, because each served row is a trade-observed price. The estimated rows are listed separately.
- Old price types: where a row's old price reproduces from a single type group, the type is recorded per row. 680 served rows match no type group.
- File-day against trade-date keying: 33 served rows price differently when only the own-day partition is read. 9,409 trade rows in the window sit outside their trade-date partition.
- Round 1's 64 UNEXPLAINED rows become: 27 carry-forward, 20 changed, 16 not recomputable, 1 unchanged. The 19 rows that recomputed to 1.0 become: 10 carry-forward, 5 changed, 3 not recomputable, 1 unchanged.
- The round-1 thread asset, EXXONMOBIL HOLDINGS CORP COM SHS on 2026-10-09: served 168.94 comes from Transfer In rows. R1 carries forward 168.29 from 2026-10-08. This matches the rule probe.
- BLACKROCK INC COM on 2026-09-22: variant A carries forward 1078.04 from 2026-07-17. Variant B reads a trade price of 1074.9259 on the date. This matches the rule probe.

## Estimated rows (what R1 would show)

The window holds 18,566 linear_interpolation rows for the 886 assets that have a served row. R1 would show a last traded price for 15,554 of them under variant A (3,012 have no earlier trade in the history read), and for 16,233 under variant B (2,333 without). No carry_forward source value exists in the window.

## Lookback

The window alone cannot carry a price forward for most of the no-trade rows. The lookback scan walked partitions backwards from 2025-12-31 to 2020-03-06, for the 242 residual assets only. It found the latest earlier trade for 52 assets under variant A and 59 under variant B. The rest have no trade in the history read. 618 dates in that span have no partition in S3, 116 of them weekdays. Partitions are fetched by read verb only, into the worker's data folder outside the checkout (`LOOKBACK_FETCH.txt`, one line per date: FETCHED or NO_PARTITION). `lookback.csv` is the scan's output; `residual_assets.csv` is its input.

## Determinism

The full list was produced by three separate processes after the final code; each produced BEFORE_AFTER.csv with md5 `76d58c1e409f1072833fb547d7fbfa69`. The estimated list matches across processes at md5 `bb586828a92352625f4a2321d36872d0`. The past-date arm passed: for 20 changed rows, the result for the date uses only that date's trades and is the same when all later trades are removed (20 of 20).

## What stays unknown

- Which writer produced the served prices. R1 reproduces the served value on only 1 of round 1's 64 UNEXPLAINED rows.
- How bond prices should be scaled. The rule as written does not address percent-of-par quotes; the 8 `scale_100x` rows need a ruling before any move.
- Trades dated later than their partition beyond one day. The lookback reads partitions t and t+1 only.
- The 212 NOT_RECOMPUTABLE rows, whose assets have no trade in the store.
- Dollar effect on holdings and downstream readers. That is `BP-b-7`'s join and is not measured here.
