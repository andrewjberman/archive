# IB-pr-443 -- the five one-day-off security-days against a third dated value (read only)

Worker 0.9.0_WK_IRPT_BCKEND~301, round 140. First witness = the Schwab anchor's closing_price by CUSIP; second = the reader's unadjusted Close (Yahoo Finance, one call, 4 tickers). The custodian mark is the holdings partition's own mark (not independent). Nothing is built, served or admitted by this cell; no class is admitted.

## SHM on 2026-06-30 (RIC/BDC / Not Available; exchange_traded)
- days: prior 2026-06-29, day 2026-06-30, next 2026-07-01
- first witness : 47.97 | 47.965 | 47.84
- second witness: 47.97 | 47.97 | 47.84
- custodian mark (not independent): 47.97 | 47.965 | 47.84
- third value: NONE. the silver transactions table beside the holdings table (every date partition, rows de-duplicated on TransactionID), rows of CUSIP 78468R739; Buy and Sale rows with a Price above 0 and a trade date from 2026-06-25 to 2026-07-06 (three trading days either side of 2026-06-30): 0. The table holds 21 row(s) of this security in all, 11 of them priced Buy or Sale rows; nearest priced Buy or Sale row: Sale 47.765 on 2026-08-13 (31 trading day(s) away)
- distribution on or beside the day: none within three trading days; nearest in the estate: {'trade_date': '2026-07-07', 'kind': 'Dividend', 'trading_days_from_the_day': 4}
- series, 2026-06-23 .. 2026-07-08: first [47.95, 47.94, 47.95, 47.98, 47.97, 47.965, 47.84, 47.9, 47.91, 47.83, 47.84]; second [47.95, 47.94, 47.95, 47.98, 47.97, 47.97, 47.84, 47.9, 47.91, 47.83, 47.84]
- VERDICT: CANNOT_BE_TOLD (claim inferred). neither witness is shown to be on the wrong day: the second witness's close is the first witness's sub-cent close rounded half-up to the cent, which here coincides with the prior day's close; the same rounding holds on all 6 sub-cent days of this series
- deciding evidence: none (no witness is named)

## SHM on 2026-07-20 (RIC/BDC / Not Available; exchange_traded)
- days: prior 2026-07-17, day 2026-07-20, next 2026-07-21
- first witness : 47.81 | 47.805 | 47.77
- second witness: 47.81 | 47.81 | 47.77
- custodian mark (not independent): 47.81 | 47.805 | 47.77
- third value: NONE. the silver transactions table beside the holdings table (every date partition, rows de-duplicated on TransactionID), rows of CUSIP 78468R739; Buy and Sale rows with a Price above 0 and a trade date from 2026-07-15 to 2026-07-23 (three trading days either side of 2026-07-20): 0. The table holds 21 row(s) of this security in all, 11 of them priced Buy or Sale rows; nearest priced Buy or Sale row: Sale 47.765 on 2026-08-13 (18 trading day(s) away)
- distribution on or beside the day: none within three trading days; nearest in the estate: {'trade_date': '2026-07-07', 'kind': 'Dividend', 'trading_days_from_the_day': -9}
- series, 2026-07-13 .. 2026-07-27: first [47.86, 47.87, 47.78, 47.74, 47.81, 47.805, 47.77, 47.7, 47.55, 47.605, 47.6]; second [47.86, 47.87, 47.78, 47.74, 47.81, 47.81, 47.77, 47.7, 47.55, 47.61, 47.6]
- VERDICT: CANNOT_BE_TOLD (claim inferred). neither witness is shown to be on the wrong day: the second witness's close is the first witness's sub-cent close rounded half-up to the cent, which here coincides with the prior day's close; the same rounding holds on all 6 sub-cent days of this series
- deciding evidence: none (no witness is named)

## MEIIX on 2026-07-02 (RIC/BDC / Inst; mutual_fund)
- days: prior 2026-07-01, day 2026-07-02, next 2026-07-06
- first witness : 53.75 | 54.46 | 54.61
- second witness: 53.75 | 53.75 | 54.61
- custodian mark (not independent): 53.75 | 54.46 | 54.61
- third value: NONE. the silver transactions table beside the holdings table (every date partition, rows de-duplicated on TransactionID), rows of CUSIP 552983694; Buy and Sale rows with a Price above 0 and a trade date from 2026-06-29 to 2026-07-08 (three trading days either side of 2026-07-02): 0. The table holds 6 row(s) of this security in all, 1 of them priced Buy or Sale rows; nearest priced Buy or Sale row: Sale 53.84 on 2026-10-09 (69 trading day(s) away)
- distribution on or beside the day: none within three trading days; nearest in the estate: {'trade_date': '2026-06-26', 'kind': 'Dividend', 'trading_days_from_the_day': -4}
- series, 2026-06-25 .. 2026-07-10: first [53.26, 53.16, 53.28, 53.41, 53.75, 54.46, 54.61, 54.75, 54.23, 54.39, 54.58]; second [53.26, 53.16, 53.28, 53.41, 53.75, 53.75, 54.61, 54.75, 54.23, 54.39, 54.58]
- VERDICT: SECOND_WITNESS_OFF (claim inferred). the second witness repeats its prior day's value at the day while the first witness moves to a value the second witness shows on no day
- deciding evidence: second witness 2026-07-01: 53.75 then 53.75 (repeated); first witness 2026-07-01: 53.75 then 54.46; the first's 54.46 appears in no day of the second's series

## MISIX on 2026-10-09 (RIC/BDC / Inst; mutual_fund)
- days: prior 2026-10-08, day 2026-10-09, next None
- first witness : 21.51 | 21.75 | None
- second witness: 21.51 | 21.51 | None
- custodian mark (not independent): 21.51 | 21.75 | None
- third value: NONE. the silver transactions table beside the holdings table (every date partition, rows de-duplicated on TransactionID), rows of CUSIP 92647K309; Buy and Sale rows with a Price above 0 and a trade date from 2026-10-06 to 2026-10-09 (three trading days either side of 2026-10-09): 0. The table holds 3 row(s) of this security in all, 1 of them priced Buy or Sale rows; nearest priced Buy or Sale row: Sale 21.64 on 2026-07-14 (62 trading day(s) away)
- distribution on or beside the day: none within three trading days; nearest in the estate: None
- series, 2026-10-02 .. 2026-10-09: first [21.69, 21.91, 21.97, 21.68, 21.51, 21.75]; second [21.92, 21.91, 21.97, 21.68, 21.51, 21.51]
- VERDICT: SECOND_WITNESS_OFF (claim inferred). the second witness repeats its prior day's value at the day while the first witness moves to a value the second witness shows on no day
- deciding evidence: second witness 2026-10-08: 21.51 then 21.51 (repeated); first witness 2026-10-08: 21.51 then 21.75; the first's 21.75 appears in no day of the second's series

## PZA on 2026-07-31 (RIC/BDC / Not Available; exchange_traded)
- days: prior 2026-07-30, day 2026-07-31, next 2026-08-03
- first witness : 22.87 | 22.865 | 22.87
- second witness: 22.87 | 22.87 | 22.87
- custodian mark (not independent): 22.87 | 22.865 | 22.87
- third value: NONE. the silver transactions table beside the holdings table (every date partition, rows de-duplicated on TransactionID), rows of CUSIP 46138E537; Buy and Sale rows with a Price above 0 and a trade date from 2026-07-28 to 2026-08-05 (three trading days either side of 2026-07-31): 0. The table holds 4 row(s) of this security in all, 1 of them priced Buy or Sale rows; nearest priced Buy or Sale row: Sale 23.125 on 2026-08-13 (9 trading day(s) away)
- distribution on or beside the day: none within three trading days; nearest in the estate: {'trade_date': '2026-07-24', 'kind': 'Dividend', 'trading_days_from_the_day': -5}
- series, 2026-07-24 .. 2026-08-07: first [None, None, None, 22.885, 22.87, 22.865, 22.87, 22.98, 22.99, 22.97, 23.07]; second [22.85, 22.91, 22.95, 22.89, 22.87, 22.87, 22.87, 22.98, 22.99, 22.97, 23.07]
- VERDICT: CANNOT_BE_TOLD (claim inferred). neither witness is shown to be on the wrong day: the second witness's close is the first witness's sub-cent close rounded half-up to the cent, which here coincides with the prior day's close; the same rounding holds on all 2 sub-cent days of this series
- deciding evidence: none (no witness is named)

## The last day (2026-10-09)
- is_the_prior_days: None (claim absent); compared 0; equal same day 0; equal prior day 0; first witness's partition last modified 2026-10-10T09:46:43+00:00 UTC
- NOT COUNTED. The per-security, per-day classification for 2026-10-09 over the 894 securities needs the second witness's bars for the 890 tickers this cell may not ask the reader for again; IB-pr-441's output (IB138-2_type_overlap_and_fund_check.json) holds counts by type and the five detail lines, not the per-security, per-day values, and no scratch cache of that cell is on this box (its scratch folder under C:/dev is absent). So the three counts are 0 because nothing was compared, not because nothing matched. What is read without a fetch: the first witness's partition object for 2026-10-09 was last modified at the time given (UTC); IB-pr-441 found, over all the securities that had a value on that day, ONE security one-day-off on 2026-10-09 (MISIX; its type table shows 2026-10-09 with count 1 in the Inst column and in no other) - that cell's own finding, held here, not re-measured.

Verdict counts: {'FIRST_WITNESS_OFF': 0, 'SECOND_WITNESS_OFF': 2, 'CANNOT_BE_TOLD': 3}. Fetch: 1 call(s), 4 tickers, 0 asked more than once. Control: planted True, read ['FIRST_WITNESS_OFF', 'SECOND_WITNESS_OFF', 'CANNOT_BE_TOLD', 'SECOND_WITNESS_OFF', 'FIRST_WITNESS_OFF', 'CANNOT_BE_TOLD'].
