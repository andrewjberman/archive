# BP-a-3 -- the served-versus-recomputed gap, classified (read-only)

Worker `0.9.0_WK_ADVI_BDPRCE~3`, cell BP-a-3, read at 2026-10-13T14:11:53Z. Record: `GAP.json`; one row per served
row: `GAP_ROWS.csv` (1,657 lines). Scripts: `gap_manifest.py`, `gap_fetch.sh` (read verbs only), `gap_measure.py`.
Claim: measured. No object was written, no producer ran, no product file was edited.

## Denominator

Window 2026-09-16..2026-10-13 (20 weekday dates; newest `silver/prices/<date>.parquet` is 2026-10-13).
Served `transaction_observed` rows in the current `canonical_prices.parquet` (V7JNX.Gm..., 12:48:05 UTC): **1,657**, not
1,610. The count is 1,657 on every canonical version checked (2026-10-12 23:03, 2026-10-13 00:15, 04:03, 09:49,
12:47, 12:48). The 1,610 of the task framing is not reproduced; not forced.

## Classes (the spec's ladder; first match takes the row)

| class | rows |
|---|---|
| EQUAL (current partition, T1 rule) | 1,148 |
| EXPLAINED_BY_VERSION_AT_WRITE | 0 |
| EXPLAINED_BY_MULTIDAY_WINDOW | 197 |
| EXPLAINED_OTHER | 232 |
| UNEXPLAINED | 64 |
| NOT_RECOMPUTABLE | 16 |
| **sum (= served_rows)** | **1,657** |

## Cause or causes

- **Version at write: not a cause.** The T1 rule over all 74 versions of the window-date partitions reproduces none of
  the 509 non-equal rows. The write-time version is one of those versions, so the class is empty. The daily
  `silver/prices/<date>.parquet` is absent for 6 window dates, so write-time was not resolved and not needed.
- **Multi-day windows: 197 rows.** The rule over a contiguous window of 2+ partitions containing the day reproduces
  them, read per asset or per (asset, trade_date) (the backfill path), raw or de-duplicated by transaction_id. 160 of
  197 need only a 2-partition window; 153 windows end on the day. Overlap: 123 of these 197 are also reproduced by the
  own-day de-duplicated T1 rule, and 63 by the own-day JOB 2 rule. The class follows the spec's order.
- **JOB 2 observed-price rule, own day: 169 rows** (`extract_observed_prices`, price column first). Trailing
  concatenations give the identical set.
- **Median of the price column excluding cash dividends, own day: 62 rows.** Not a rule in the code read. Found
  after the other rules by testing named variants on the residue; chance agreement is not excluded. Re-read before reliance.
- **Neighbouring trade-date partition: 1 row.**
- **De-duplication:** the own-day T1 rule after de-duplication by transaction_id reproduces 1,266 of 1,657 served rows,
  against 1,148 under the raw rule as written (`bd_price_update.py:263-271` does no de-duplication). The writers that
  produced served values are not known to this read; that gap is the open question behind the 118 extra matches.

## Bound

64 rows stay UNEXPLAINED. Largest absolute difference: 1,072.162298 (BLACKROCK INC COM, 2026-09-22; served
1,073.162298, own-day T1 recompute 1.000000). The relative difference is the same on that row (recomputed is 1.0). 19 of
the 64 recompute to exactly 1.000000 because the own-day T1 median is dominated by cash-dividend rows whose units equal
the cash amount; their recompute is not a reliable reference. No version reproduces any of the 64.

## What read would close the residue

1. The writer's code at the write time of each served row (git history of `bd_price_update.py`, and
   `build_canonical_prices_v2.py` line 660 named by PRICING_QUANT), to test the price-column rules on a path that
   was actually running.
2. The canonical object's version history for the 64 rows (about 650 versions; a ranged read of row group 11 per
   version would make it feasible), to date the first version that carries each served value.
3. The daily price file versions for the 6 dates without one, if they exist under another key.
