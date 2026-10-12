# CB-bx-1 (round 76): the 26 percent -- the purchase rows that miss the unadjusted close, each given a cause from a closed list written first

Worker 0.9.0_WK_ADVI_COTBKF~138. Record: `PURCHASE_ROWS_OFF.json`. Closed list written 2026-10-11T22:52:32Z (read from the clock), before any off row was looked at; its full text is `closed_list.text` in the record. No code, no fetch, no bucket; counts, ratios, tickers and dates only.

## Headline

Of the 246 purchase rows off the unadjusted close, the closed list written first gives 122 a benign cause under either order and leaves 124 as none_found; 41 rows change cause with the order. 243 of the 246 are one fund (VEIRX) and every off row has the price paid ABOVE the close (ratio below 1, median 0.980). The load-rate test fits at chance level (51 real vs 66 and 52 shifted), the cache has no fee column, and the sales of the same funds are off too (10.8 percent, all with the price received BELOW the close). With the benign rows set aside the close reproduces the price on 84.8 percent of purchase rows (86.8 percent explained). POST HOC, not in the list: on all 936 rows the Amount exceeds shares x close by a flat dollar figure from a short list (0, 3, 10, 15, 19, 30, 34), so rows fall outside 1 percent where the amount is small.

## 1. Round 75, reproduced

1,119 purchase rows of the 19 funds, 936 with an unadjusted close on the row's effective day, 690 within 1 percent (73.7 percent), 246 off. Day convention as round 75: close of the effective day (Trade_Date, next trading day when NYSE is closed); ratio = |Quantity| x close / |Amount| (close over price paid); a row is the rows of one account, day and fund summed (here 1,119 rows = 1,119 groups, no group holds two custodian rows). Median 0.997191.

## 2. The closed list (written first; kept)

Causes in the order run (a row takes the first that fits), with their tests (full thresholds in the record):
1. small_quantity: |Quantity| < 0.05 shares (three decimals) or |Amount| < 0.50 dollars (cents). 2. prior_day_close, 3. next_day_close: the previous / next trading day's unadjusted close within 1 percent of the price paid. 4. settle_date_close (added before the look; the schema carries Settle_Date). 5. adjusted_close: the Yahoo Adj Close that day within 1 percent. 6. another_share_class: the Yahoo Close that day of a sibling class on disk within 1 percent. 7. reinvestment_or_exchange_recorded_as_purchase: a dividend/reinvestment row of the same account in the fund or sibling within 5 days, or a sale within 1 day, with an amount within 1 percent. 8. fee_inside_amount: price paid above the close by a share within 0.10 points of 5.75, 5.00, 4.50, 4.25, 3.75, 3.50, 2.50, 2.00, 1.00 percent (from memory of class-A breakpoints; no fee schedule is on disk). 9. fee_constant_excess: the same shortfall (within 0.10 points) on another row of the same account and fund. 10. none_found.

Why this order: least to most coincidence-prone; the rate-based fee last because nine rates 0.2 points wide cover about a third of the 1-6 percent range by chance. **Alternative order:** 1, then 8 and 9 moved to second and third, then 2, 3, 4, 5, 6, 7, 10.

**Schema:** the cache has NO fee, commission, load, net-vs-gross or price column (Advisor_ID, Account_Number, Transaction_Type, Transaction_Description, Cusip, FundCode, Symbol, Quantity, Amount, AI, Trade_Date, Cost_Date, Settle_Date, Asset_Type, CA_Event_Id, LongShort_Indicator, Position_Type, Security_Description, Transaction_Note, AsOfDate, lineage). On the purchases AI is 0, Cost_Date equals Trade_Date, the note never says reinvest or exchange.

Benign (the close is not shown wrong): small_quantity, prior/next/settle-date close, another_share_class, reinvestment_or_exchange, both fee causes. Not benign: adjusted_close, none_found.

## 3. The 246 off rows by cause

**Stated order (A)**

| cause | rows | median close/paid | p10 | p90 | funds | accounts | tickers | by year |
|---|---|---|---|---|---|---|---|---|
| small_quantity | 0 | - | - | - | 0 | 0 | - | - |
| prior_day_close | 31 | 0.9888 | 0.9844 | 0.9897 | 2 | 30 | VEIRX 30, PRILX 1 | 2022 1, 2023 10, 2024 20 |
| next_day_close | 15 | 0.9846 | 0.9846 | 0.9884 | 1 | 8 | VEIRX 15 | 2023 5, 2024 10 |
| settle_date_close | 0 | - | - | - | 0 | 0 | - | - |
| adjusted_close | 0 | - | - | - | 0 | 0 | - | - |
| another_share_class | 0 | - | - | - | 0 | 0 | - | - |
| reinvestment_or_exchange_recorded_as_purchase | 21 | 0.9845 | 0.9754 | 0.9847 | 1 | 13 | VEIRX 21 | 2023 6, 2024 15 |
| fee_inside_amount | 35 | 0.9647 | 0.9526 | 0.9796 | 1 | 35 | VEIRX 35 | 2023 9, 2024 26 |
| fee_constant_excess | 20 | 0.9845 | 0.9789 | 0.9862 | 1 | 5 | VEIRX 20 | 2023 13, 2024 7 |
| none_found | 124 | 0.9719 | 0.9132 | 0.9867 | 2 | 111 | VEIRX 122, PRILX 2 | 2022 2, 2023 22, 2024 100 |
| **total** | 246 | | | | | | | |

**Alternative order (B)**

| cause | rows | median close/paid | p10 | p90 | funds | accounts | tickers | by year |
|---|---|---|---|---|---|---|---|---|
| small_quantity | 0 | - | - | - | 0 | 0 | - | - |
| fee_inside_amount | 51 | 0.9745 | 0.9558 | 0.9896 | 1 | 50 | VEIRX 51 | 2023 11, 2024 40 |
| fee_constant_excess | 45 | 0.9846 | 0.9844 | 0.9876 | 1 | 6 | VEIRX 45 | 2023 22, 2024 23 |
| prior_day_close | 13 | 0.9879 | 0.9836 | 0.9888 | 2 | 13 | VEIRX 12, PRILX 1 | 2022 1, 2023 7, 2024 5 |
| next_day_close | 4 | 0.9866 | 0.9828 | 0.9887 | 1 | 4 | VEIRX 4 | 2023 1, 2024 3 |
| settle_date_close | 0 | - | - | - | 0 | 0 | - | - |
| adjusted_close | 0 | - | - | - | 0 | 0 | - | - |
| another_share_class | 0 | - | - | - | 0 | 0 | - | - |
| reinvestment_or_exchange_recorded_as_purchase | 9 | 0.9834 | 0.9709 | 0.9878 | 1 | 9 | VEIRX 9 | 2023 2, 2024 7 |
| none_found | 124 | 0.9719 | 0.9132 | 0.9867 | 2 | 111 | VEIRX 122, PRILX 2 | 2022 2, 2023 22, 2024 100 |
| **total** | 246 | | | | | | | |

Rows that change cause with the order: **41** (A to B: 14 prior-day to fee, 11 next-day to constant-excess, 4 prior-day to constant-excess, 10 reinvestment to constant-excess, 2 reinvestment to fee). Every off row has ratio below 1 (price paid above the close). Zero-row causes: small_quantity (no row is below 0.05 shares or 0.50 dollars), settle_date_close (18 rows fit it, and each of them is given an earlier cause under both orders), adjusted_close, another_share_class. By fund every cause is VEIRX except 1 prior-day and 2 none_found rows of PRILX.

**none_found: 124 rows** in both orders (VEIRX 122, PRILX 2); close/paid spread min 0.8333, p10 0.9132, median 0.9719, p90 0.9867. Looked at: the list above.

**Fee by rate is at chance:** of the 246 off rows (all with price above the close) 51 fit the nine-rate test; the same test shifted by +0.35 and by -0.35 points fits 66 and 52.

## 4. Fit after the benign causes

Purchases (936 with a close, 690 within 1 percent): off rows given a benign cause 122 (A) / 122 (B). Within 1 percent plus benign = 812 of 936, explained share **0.8675**; with the benign rows set aside the close reproduces the price on 690 of 814 = **0.8477**. If reinvestment/exchange is not benign: explained 0.8451 (A) / 0.8579 (B). The 124 none_found rows are not explained by the list.

Sales (`sl` rows of the 19 funds, same unit and ratio): 942 with a close (202 without), 840 within 1 percent = **0.8917**, median 1.001289. 102 off, **all 102 with ratio above 1 (price received below the close)**, none below; off median 1.0186; by fund {"VEIRX": 100, "PRILX": 2}. Reading: sales are not at about 99 percent; they are off too, in the opposite direction to purchases, and in the same fund. The rate-based fee story does not hold (chance-level fit); the discrete pattern below is the post-hoc lead.

## 5. The 183 purchase rows with no close that day

All 183 are before the first close the served series holds for their fund: 158 before 2020-06-29 (start of the Yahoo cache) and 25 later but before the fund's first served close (BALCX 22, PRILX 2, DFREX 1). None is inside a series on a non-trading day or without a bar. By year: {"2013": 29, "2014": 43, "2015": 42, "2016": 6, "2017": 13, "2018": 10, "2019": 5, "2020": 17, "2021": 14, "2022": 4}. By fund: {"CPXIX": 99, "BALCX": 49, "PRILX": 9, "MEIIX": 8, "ACTDX": 5, "DFLVX": 3, "CWGIX": 3, "DISVX": 2, "DFREX": 1, "AWSHX": 1, "ANCFX": 1, "WMFFX": 1, "FINFX": 1}.

## 6. POST HOC (after the look; not in the list; not in any count above)

On every one of the 936 purchase rows with a close, Amount minus |Quantity| x unadjusted close, in dollars, lands within 0.15 of 0, 3, 10, 15, 19, 30 or 34 (counts 112, 34, 3, 60, 24, 502, 201; 502 + 201 + 60 + 34 + 24 are VEIRX). The sale rows with a close show the same set (157, 0 at 3, 10 at 10, 10 at 12, 72, 17, 485, 190, 1 at 122) with the sign reversed (proceeds below shares x close). 241 of the 246 off purchase rows and 121 of the 124 none_found rows sit at 3, 15, 30 or 34. A flat dollar charge inside the Amount reads as a ratio off the 1 percent band exactly where the amount is small. A better list would hold `fixed_dollar_charge_inside_amount`. The constants were read off the rows, so this is a description, not a test the rows passed. What the charge is and who takes it is not established.

Where the off rows sit: 243 of 246 are VEIRX (PRILX 3); 141 of the 299 VEIRX purchases on 2024-02-16 are off.

## What is not established

- What the flat dollar excess is (a transaction charge, a custodian fee, a ticket or postage charge) and who takes it: the cache has no fee column and no fee schedule is on disk.
- Whether the front-load rate set (from memory) is right for any of the 19 funds: the rate test fits at chance, which says the set does not find a load, not that no load exists; VEIRX Admiral shares are a no-load class (general knowledge, not on disk).
- Whether the effective-day convention (next trading day when closed) is the day the custodian priced; prior, next and settle-day closes were tested and fit 31, 18 and 18 off rows before ordering.
- The sale rows' cause: they were measured (ratio, direction) but not run through the closed list.
- Why 141 of 299 purchases on 2024-02-16 are off and nearly all of the 2023-02-17/21 purchases are not (post hoc, one day).
- Whether the 183 rows before each fund's first served close would fit: the served series does not reach them (158 are before the start of the Yahoo cache, 25 are later than it).
- Nine of the 19 funds have a sibling class on disk; ABNFX, CAIBX, CPXIX, DISVX, DFLVX, DFREX, FCNTX, PRILX, VEIRX, ACTDX have none, so another_share_class could not fire for them (it fired for none).
- The reinvestment/exchange test needs an amount match within 1 percent: a reinvestment or exchange booked with a different amount is not found.
