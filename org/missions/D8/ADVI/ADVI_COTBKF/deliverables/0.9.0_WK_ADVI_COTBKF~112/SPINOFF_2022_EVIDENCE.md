# SPINOFF_2022_EVIDENCE -- CUSIP 00206R102 (T), event 2022-04-11, store factor 1.324 (TO CB-br-2, round 70)

Worker 0.9.0_WK_ADVI_COTBKF~112. Read-only. Every number below is derived in this cell from the data; the two earlier records are compared with only at the end.
Record: `SPINOFF_2022_EVIDENCE.json`; pairs: `SPINOFF_2022_PAIRS.csv` (42 rows, no account column).

## 1. The traded price is the custodian's

The cache `.scratch/advi_cotbkf/tx_cache` holds 1,416,497 rows (= the PRD's record count, line 200) and its marker `_complete.json` names
`s3://opal-data-assets/commonwealth/cottonwood/silver/transactions/date=2026-06-23` (14 objects). That silver table is written by
`data/assets/scripts/silver/commonwealth_transactions.py` (docstring lines 1-22) from the inner zip's `..._Historical_Transactions_<stamp>.txt`.
All 1,416 rows of this CUSIP carry one `source_zip` (`Cottonwood Capital Advisors_Portfolio_Accounting_Performance_ClientDelivery.zip`), one
`source_zip_sha256` (`a3a2772e...d658b`, equal to the PRD v0.4 addendum line 199, which says the same member was read directly from Andrew's `Files.zip`),
and one `source_file` (`CFN_SCTASK0548380_Portfolio_Accounting_Performance/CFN_SCTASK0548380_Historical_Transactions_20260623_102751.txt`).
Chain: Andrew's `Files.zip` -> inner client-delivery zip -> bronze object -> silver `transactions` partition -> the cache.
Shown: zip name and hash, member name, the silver writer and partition, the row count. NOT shown: the bronze object key and bytes (the script takes `--source`
and names none), `Files.zip` itself, and the cache-to-silver copy (taken from the marker and the lineage columns).

## 2. The pairs

217 buy/sell rows (`by` 90, `sl` 127), all with non-zero quantity and amount, on 149 trade dates (2013-05-03..2026-06-08); per date the traded price is
sum(|Amount|)/sum(|Quantity|). All 149 are weekdays. The served closes (`r34/after/security_day_price.parquet`) start 2020-07-01 for this CUSIP.
- Before the event (123 dates): **16 comparable** (2020-07-16..2022-01-10); **107 not comparable** (2013-05-03..2020-05-11), all before the table starts.
- On or after (26 dates, all comparable; 2022-06-02..2026-06-08; 25 on the silver-prices store, the last (2026-06-08) on the gold-holdings store). No trade falls on 2022-04-11, and none between 2022-01-10 and 2022-06-02.

## 3. The four comparisons (ratio = served close / traded; WITH = close x 1.324 / traded; within = |ratio-1| <= tol)

| | n | within 0.5% | within 2% | median | worst (farthest from 1) |
|---|---|---|---|---|---|
| WITHOUT, before | 16 | 0 | 0 | 0.7573 | 0.7491 |
| WITH, before | 16 | 9 | 15 | 1.0027 | 1.0304 (2021-03-19) |
| WITHOUT, on/after | 26 | 19 | 26 | 0.9993 | 0.9880 |
| WITH, on/after (hypothetical) | 26 | 0 | 0 | 1.3231 | 1.3317 |

Tolerance: 2 percent is the test (a quantity-weighted fill price during a day against a close can differ by that much); 0.5 percent is reported as the tight reading.
The negative arm reads as predicted: after the event the close needs no factor (26 of 26) and the factor would break every one of them.

## 4. The factor at its source

`load_store_splits(s3, {00206R102}, 2026-10-11T11:55:40Z)` (141 partitions listed; pin sha256 `d9a2e0fa...23d3b4`; address `s3://opal-data-assets/yahoo/global/silver/price_history/`)
returns four entries for this CUSIP: 1987-05-26 x3.0, 1993-05-26 x2.0, 1998-03-20 x2.0, **2022-04-11 x1.324**, version id **`xg.cvNW5eQATofYD3zuGh1f2uy5xS7oH`**.
The 2022 one is the spin-off; the other three precede the first transaction row (2013-04-09) and the first close (2020-07-01), so `split_plan` (store events after the first row) keeps only 2022.
Application (`apply_splits`, daily_valuation.py lines 663-677): the close of every day strictly BEFORE the split day is multiplied by the ratio (`days < d`); the split day and later days are untouched. "With the factor" is therefore close x 1.324 for dates < 2022-04-11.

## 5. Reading by the rule

**APPLY.** Before the event the WITH reconstruction reproduces the traded price (15 of 16 within 2 percent, median 1.0027) and the WITHOUT one does not (0 of 16, median 0.7573);
after the event the WITHOUT one does (26 of 26). One before-date (2021-03-19) is at 1.0304 with the factor; the rule as worded does not ask for every date, and no cause is asserted.
Supplementary, not used in the reading: the served close itself steps 1.0766 from 2022-04-08 to 2022-04-11 (1.0243 against the previous calendar row, a weekend interpolation); the build's continuity band is 0.7..1.4, so by reading the code it would confirm and apply the entry (not executed).
Reinvested distributions (`dvr`, NOT trades): 95 rows on 31 dates (2013-08-01..2021-05-03, none after the event); the 4 dates with a served close (2020-08-03, 2020-11-02, 2021-02-01, 2021-05-03) imply close/price ratios 0.756, 0.771, 0.741, 0.760 -- the same basis, no decision rests on them.

## 6. Reach on the served table (`fwd3_serve_r34`)

- Dates before the event on which any account holds the security: 2,269 (35,531 holding account-days, from 2013-04-09). Of these, dates with a priced holding (a close exists to move): **448** (2020-07-01..2022-04-08), **3,434 priced holding account-days**.
- **Measured** (non-null return) among those: **28** account-days, one account, 2020-10-12..2020-11-18. Every other priced day is blank (3,401 UNPRICED, 5 FIRST_DAY).
- Where the price LEVEL enters the return (the day has a flow, an in-kind row of this security, or a trade of this security): flow **1** (2020-10-13), in-kind 0, trade 0 -> **1 of 28**. The security is 40-43 percent of the account on all 28 days.
  Consistency with 28: the earlier round's 28 (ADDED_SPLITS.json) is that record's number, not mine. It equals my count of ALL measured days, not my count of level days (1): the other 27 can only move through the security's weight in the account (a constant scale changes the weight), which I did not compute. The three other store entries for this CUSIP predate every close, so all 28 are this event's. The 2 blank reasons are not measured here.

## 7. Differences from the two earlier records

- Agree, re-derived: 16 compared dates 2020-07-16..2022-01-10, 123 pre-event trade dates, 20 trades on the compared dates, counts 0/0 and 9/15, medians 0.7573 and 1.0027, worst 0.7491 and 1.0304, 448 priced dates, 2,269 held dates, 28 measured, steps 1.0243 and 1.0766.
- Different: (a) the scan's `holding_days_affected` 3,062 is the priced account-days only through 2022-01-10 (I reproduce 3,062 at that cut); every day the factor scales is through 2022-04-08: 3,434 (the 372 more are 2022-01-11..2022-04-08). (b) The scan's `factor` 0.7573 is the median ratio, not the store's 1.324 (1/1.324 = 0.7553). (c) The earlier records give no after-event counts; here: 26 pairs, 26 of 26 within 2 percent (19 within 0.5) without the factor, 0 with it. (d) The round-68 claim for this CUSIP was UNAPPLIED_NO_HELD_DATE under the gold-holdings print and APPLY only "if admitted"; this record reads the delivered trade rows and the rule gives APPLY. (e) New here: the custodian chain, the version id and all four store entries, the application rule (strictly before), the level-day count (1 of 28).

## 8. Not established

Where the step sits (no trade between 2022-01-10 and 2022-06-02; the date is the store's); the basis before 2020-07-01 (107 dates with no close); why the served series sits at 0.757 (not traced); the returns that move (not computed); the bronze object and the zip (not opened); the cause of the 2021-03-19 miss.
