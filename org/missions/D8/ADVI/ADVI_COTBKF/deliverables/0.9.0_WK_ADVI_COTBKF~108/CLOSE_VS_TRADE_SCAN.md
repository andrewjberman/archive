# CB-bq-3 -- every security's close against its traded price (round 69, 0.9.0_WK_ADVI_COTBKF~108)

A read-only measurement. No code, test, config or manifest changed; no AWS or network call. Records: `CLOSE_VS_TRADE_SCAN.json`
(the named keys plus `by_store`), `CLOSE_VS_TRADE_SCAN.csv` (the 7 CONSTANT_SCALE and STEP securities), and two supplements
(`CLOSE_VS_TRADE_SCAN_SUPPLEMENT.json`, `CLOSE_VS_TRADE_SCAN_TOO_FEW_BEYOND_10PCT.csv`).

## What was compared

- Close: `.scratch/advi_cotbkf/r34/after/security_day_price.parquet` (2,124,908 rows, 1,722 CUSIPs; the table holds a close on every calendar day of a security's span).
- Traded price: the silver transactions cache (1,416,497 rows), CUSIP stripped and upper-cased as `sw.norm` does. **Trades taken: `by` and `sl`** (the two trade types of `commonwealth_flows.py` INTERNAL that carry a market price), rows with non-zero Quantity and Amount (326,747 of 326,784). One price per (cusip, Trade_Date) = sum |Amount| / sum |Quantity|.
- **Not taken as trades:** `dvr` and `dv*` (reinvested and paid distributions), `li`, `lo` and their variants (in-kind movements), fee, interest and tax rows, and `cs` (24 rows), `ss` (26), `BYX` (1: short-side and cancel rows, 51 in all).
- **Kinds compared (share-priced):** Equity, ETF, Mutual Fund, Mutual Fund (Closed End), Unit Investment Trust. **Left out:** Cash and Cash Equivalent (sweep lines), Annuity (10,956 by/sl rows) and Alternative Investment (46): not a market share price. No option rows appear in the cache.
- **Fixed Income, separately:** 753 securities have by/sl rows; 180 appear in the build table; **0 (cusip, date) pairs** line up, so no unit (per 100 of par, or per unit) was established and no comparison is reported.

## Denominator

3,109 share-priced securities traded; 1,409 of them have any close in the build table; **720 securities and 7,979 (cusip, date) pairs** compared. Of the 34,810 trade dates of in-store securities, 26,821 fall before the security's first stored close (the store holds a security from its first held day in the served window), 6 after its last, 4 inside its span with no close; 7,979 compare.

## Class rules used (where the face left a choice)

ratio = close / traded price. TOO_FEW: fewer than 3 pairs. AGREES: median within 2 percent of 1 and no date beyond 10 percent. CONSTANT_SCALE: median beyond 10 percent from 1 and at least 90 percent of dates within 5 percent of the median (all 5 found also pass with all dates). STEP: best single break date over splits that leave 3 or more dates a side, each side with at least 90 percent of dates within 5 percent of its own median, one side's median within 2 percent of 1, the other beyond 10 percent from 1. ISOLATED: median within 2 percent of 1 and one or two dates beyond 10 percent. NOISY: the rest. The order is the face's.

## Counts (720 securities)

| class | count |
|---|---|
| AGREES | 315 |
| CONSTANT_SCALE | 5 |
| STEP | 2 |
| ISOLATED | 15 |
| NOISY | 37 |
| TOO_FEW | 346 |

By store (pairs; the same classer re-run on each store's pairs only): cottonwood-silver-canonical-prices 7,913 pairs / 695 securities (AGREES 314, CONSTANT_SCALE 5, STEP 2, ISOLATED 14, NOISY 37, TOO_FEW 323); cottonwood-gold-canonical-holdings 42 pairs / 37 securities (all TOO_FEW); etfs-bbg-testpull-ticker-history 24 pairs / 10 securities (AGREES 4, TOO_FEW 6). All 7 CONSTANT_SCALE and STEP securities have their mis-scaled dates in the silver store (T also has later pairs from the gold store, on the agreeing side). The mis-scales are in the silver store's series.

## CONSTANT_SCALE and STEP (all 7 hand-read: their ratio series printed and checked by eye)

| ticker | class | factor (close / trade) | comparable span | pairs | priced holding-days wrong | measured |
|---|---|---|---|---|---|---|
| BALCX | CONSTANT_SCALE | 0.759 | 2022-05-09..2023-03-01 | 11 | 428 | 426 |
| T | STEP | 0.757 until 2022-01-10, then 1.00 from 2022-06-02 | 2020-07-16..2022-01-10 wrong side (42 pairs in all) | 16 | 3,062 (588 more in the gap) | 28 |
| XLB | CONSTANT_SCALE | 0.502 | 2020-11-19..2023-11-22 | 4 | 608 | 16 |
| MMM | STEP | 0.842 until 2024-01-09, then 1.00 from 2025-02-18 | 2021-12-16..2024-01-09 wrong side (7 pairs in all) | 4 | 3,524 (1,384 more in the gap) | 0 |
| AMBFX | CONSTANT_SCALE | 0.766 | 2024-06-28..2024-11-27 | 3 | 504 | 0 |
| FDX | CONSTANT_SCALE | 0.811 | 2021-10-19..2025-10-10 | 5 | 170 | 0 |
| CTVA | CONSTANT_SCALE | 0.151 (a close 6.6 times below the trade) | 2020-07-23..2026-02-18 | 4 | 115 | 0 |

Reach (the served table): 8,411 priced holding-days on the wrong side; **470 measured account-days** (distinct; the per-security sum is also 470, no account-day holds two of them on a wrong side). A STEP's gap days (between its last comparable date on one side and the first on the other) are not counted either way; the break is in the gap and is not located.

By eye: T steps from 0.75-0.78 to 0.99-1.01 between 2022-01-10 and 2022-06-02 and stays there for 26 pairs; MMM from 0.83-0.84 to 1.00 between 2024-01-09 and 2025-02-18; the five CONSTANT_SCALE series sit within 2 percent of one value (FDX within 3 percent). XLB at 0.50 on four dates over three years is the shape of a 2-for-1 split taken into the close with no trade after it to show the other side. ABNFX (a mutual fund) was labelled STEP on a first run with a looser "about 1" bound; by eye its ratio is a smooth monthly ramp 0.85 -> 1.00 between 2022 and 2026, not a step, so the final rule (about 1 = within 2 percent) leaves it NOISY.

## The two known cases

- **CTVA: found, CONSTANT_SCALE**, factor 0.151 on all 4 priced trades (0.1506-0.1520), 2020-07-23 to 2026-02-18.
- **CHPT: found, class TOO_FEW.** One trade date (2025-05-23, 1,000 shares sold at 0.717) has a close (14.48): ratio 20.2. It is the only by/sl row of that CUSIP in the cache, so under the face's classes (3 dates needed) it cannot be CONSTANT_SCALE or STEP. The pair is surfaced in `known_cases` and in the TOO_FEW supplement. The scan does not say whether CHPT's whole pre-split series is mis-scaled; one pair cannot.

## What the TOO_FEW class hides

50 of the 346 TOO_FEW securities have a pair beyond 10 percent (`CLOSE_VS_TRADE_SCAN_TOO_FEW_BEYOND_10PCT.csv`): for example ORLY 0.067, SEAH 21.4, MJ 12.0, DM 2.42, IXN 0.168, SWPPX 0.167, AMC 10.3 on two dates, CHPT 20.2; many sit near 0.5 or 0.67. They are not classed; a single pair cannot tell a bad print from a scale. 13 of the 37 NOISY securities have a median within 10 percent of 1 (mutual funds with drifting ratios, e.g. ABNFX), 24 beyond; 2 fit a two-level shape with neither side near 1.

## Cross-reference with the split plan

`.scratch/advi_cotbkf/r34/after_out/repair_plan.md` (61 split rows: 38 APPLIED, 23 NOT APPLIED). **STEP securities in the plan: applied 0, not applied 0, not at all 2 (T and MMM)**. Neither is a split in the plan (both are spin-off shapes). None of the 5 CONSTANT_SCALE securities is in the plan, and CHPT (a reverse split) is not in it either.

## Not established

The cause of any ratio (an adjusted close, a spin-off back-adjustment, a split applied the wrong way, a wrong source); fixed income; the 1,700 traded securities with no close in the build table and the 689 in it with no same-date pair; whether CHPT's other dates are mis-scaled; the exact break date of a STEP; the effect on a return (reach is counted, not valued).
