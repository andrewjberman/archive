# Cottonwood fact_transactions partitions overlap: what this seat measured (read by 2.0.0_SA_COO~F2, 2026-10-17 ~14:5xZ)

Read-only (S3 GET and LIST of the silver; parquet footers and the named columns). Counts, ratios and column NAMES only: no account id, figure, symbol or TransactionID value. Answers the CTO's msg 10588 (does the transaction producer assume the partition day?) and msg 10592 item 5 (do the 49 Financial and Inflection derives sum overlapping partitions?). Scripts (all in `tools/`): `cottonwood_partition_lag_census.py`, `cottonwood_dedup_probe.py`, `cottonwood_completeness_curve.py`, `cottonwood_key_columns_probe.py`, `silver_overlap_probe.py`; the 49 Financial check was a one-off count of each partition's `business_date`.

## 1. Cottonwood (blackdiamond/cottonwood/silver/fact_transactions/, 127 partitions, newest 2026-10-17)

| measure | reading |
|---|---|
| rows scanned / placed by the producer's own business-date rule | 1,114,603 / 1,114,603 (0 unreadable) |
| rows in the partition of their own business day (lag 0) | 21,693 (1.9 percent) |
| rows within 0 to 14 trading days of their business day | 1,112,050 (99.77 percent); beyond 14: 2,553; before the partition day: 0 |
| partitions the CURRENT producer would refuse (any row off the partition day) | 125 of 127 |
| partitions holding one business day's rows | mode 15; range 1 to 60 (120 business days seen) |
| raw rows against distinct TransactionID, window D..D+14 | 2026-08-19: 8,701 / 875; 2026-09-24: 8,502 / 917; 2026-09-25: 4,600 / 475; 2026-10-01: 12,467 / 1,276 |
| newest six partitions: sum of rows / union of distinct ids / ids in 2+ partitions | 72,051 / 18,727 / 16,056 (85.7 percent) |

**The producer's assumption (answer to msg 10588).** YES. `transaction_frame` reads the one partition `date=D` and `emit_transaction_day` refuses the whole day when any row's business date is not D. On this data that means `TRANSACTION_SKIPPED` for nearly every day, loudly, not a wrong write; the dry runs in the signed pair would have shown it. The window rule is needed for the Cottonwood transaction stage too.

**Completeness by lag** (34 business days whose full window D..D+14 exists; share of the day's final distinct TransactionIDs seen by lag k): lag 0 and 1 median 0.0000 (the vendor's pull lags a business day by about two trading days); lag 2 median 0.9327, min 0.4225; lag 3 median 0.9878; lag 4 median 1.0000, min 0.9199; lag 6 min 0.9821; lag 8 min 0.9924; lag 14 1.0000 for every day. TransactionIDs first seen after lag 9: 42 across the 34 days.

**The key.** Across partitions, the columns that differ for one TransactionID (3,058 ids seen with one line in 2+ partitions on the three sampled days): the two lineage columns (`_source_file`, `_source_as_of`, every id) and 19 attribute columns (for example `Last Dividend` 898, `Backdated Date` 481, `SEC Asset Type` 92, the portfolio and relationship columns, the client address columns); **none of the 14 columns the producer reads** (`AccountID`, `Trade Date`, `Settle Date`, `Transaction Type`, `Transaction Sub Type`, `Action`, `External Flow`, `Units`, `Price`, `Market Value`, `Symbol`, `Asset Name`, `Custodian`, `TransactionID`) differs. Within one partition, 106 (partition, TransactionID) pairs hold more than one row; they differ only in `PortfolioID` and `Portfolio Name` (and, in 30 pairs, the relationship columns): the same transaction listed under two portfolios. So dedup on `TransactionID` loses no line the producer reads and keeps the amounts; whichever row is kept, the producer's output is the same.

## 2. 49 Financial (schwab/08335338/silver/fact_trn/, 574 partitions, 2024-07-08 to 2026-10-16)

Daily custodian files, no transaction-id column. In each of the 12 newest partitions every row's `business_date` equals the partition day (12 of 12 partitions, 0 rows of another date). The 49 Financial stage reads the one partition `date=D` (`reporting-gold/handler.py` `transaction_frame`), which is correct for this layout. Not read: the 562 older partitions.

## 3. Inflection (orion/inflection/silver/fact_transactions/, 156 partitions, newest 2026-10-17)

Each partition is a full snapshot: 1,520,883, 1,521,095, 1,521,297 and 1,525,146 rows in the four newest, every row a distinct `id`, and 1,521,297 of the 1,525,146 ids (99.7 percent) present in all four. The transaction producer (cell DB-f-2602 and the launcher) reads ONE snapshot (the newest partition not after the run day) and keys on each line's own `transDate`, so it does not sum partitions. A reader that summed Inflection partition days would multiply every flow about four times in four partitions; **the repo's `adapters/inflection_account_return_daily.py` (flows summed over every partition day in a window) has no caller outside its own tests**. Not checked: any returns runner outside this repository.

## 4. What follows

A new cell, `DB-f-2706`, for the Cottonwood transaction stage (read D..D+14 trading days, keep the rows whose business date is D, dedup on `TransactionID`, write a day only when its full window exists), shipped as ONE code release with `2.0.0_SA_COO~D2`'s reader fix (CTO msg 10592). The signed Cottonwood pair is suspended until then and re-pinned by addendum. The surprise row is `IRPT_DASHBD-D2-S137` (filed by `2.0.0_SA_COO~D2` at 14:50Z from its own measurement of the returns path); this seat filed none, to avoid a duplicate ARMED row. This record adds the producer-side counts and the key census to it.

-- 2.0.0_SA_COO~F2
