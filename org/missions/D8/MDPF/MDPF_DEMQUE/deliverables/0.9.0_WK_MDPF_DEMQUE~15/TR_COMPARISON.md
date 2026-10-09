# TR_COMPARISON -- Bloomberg against Yahoo under the total-return method (MDPF_DEMQUE.TO-DQ-t17, DQ-t-17)

Author: 0.9.0_WK_MDPF_DEMQUE~15. Numbers: `TR_COMPARISON.json` (same folder), produced by
`data/mdpf/scripts/demque/tr_compare.py --names ED,BX,CSCO,BBY,DG,EXPD,PWR,META,GEV,BE,MRNA,LNVGY,DIVZ,IDVZ,PFDE,PFOE,FXFXX,SALXX`.
The finding sections are a JUDGMENT criterion: they are recorded here and graded at L9, not self-graded.

## Method and data

- Yahoo daily total return on trade date t = `(P_t + D_t) / (P_{t-1} / s_t) - 1` on the as-traded Close (never Adj Close), `D_t` the
  cash per share going ex on t, `s_t` the split ratio effective on t. Yahoo serves dividends split-adjusted, so the script undoes every
  split dated after the ex-date before use (no name in the window had a split, so this step was never exercised on real data).
- Bloomberg = `DAY_TO_DAY_TOT_RETURN_GROSS_DVDS / 100` (the field is percent). Ticker mapping: name `N` is the `security` column value
  `N US Equity`.
- Bloomberg union: 34 `bbg/<day>/history_topup.parquet` partitions (2026-08-20..2026-10-07). For the 18 names run, 3,272 rows in, 3,272
  rows out, 0 duplicate (security, date) rows, 0 conflicts -- the "later partition wins" rule was never needed for these names.
- Comparison on COMMON trade dates only (dates where both sides have a return). Differences are in basis points.
- Stored names with about a year (2025-09-30..2026-10-07): ED, BX, CSCO, BBY, DG (the five named) plus EXPD, PWR, META, GEV, BE, MRNA,
  LNVGY; all 12 run. Stored income-type names have only 23-34 days: DIVZ, IDVZ, PFDE, PFOE (equity-income ETFs) and FXFXX, SALXX
  (money-market funds); run on those short windows for the interest question, so their statistics are weaker than the year names'.
- Bloomberg is missing 2026-10-01, 10-02 and 10-05 for BX, CSCO and LNVGY (three days; ED, BBY, DG etc. have them). Those days are not
  common dates, so they enter neither side's compounding. CSCO's 2026-10-02 ex-date (cash 0.42) therefore falls on a date Bloomberg does
  not store: it is not compared (Bloomberg's 2026-10-06 CSCO return, +4.538%, equals 117.94/112.82 - 1, a one-day return over the stored
  gap, so the cash is not in doubt, but the ex-date row is "not shown" for CSCO).

## Per-name table (common dates; bp = basis points of daily return)

| name | days | median abs diff bp | p95 bp | max bp | cum TR Bloomberg | cum TR Yahoo | ex-dates | splits |
|---|---|---|---|---|---|---|---|---|
| ED | 257 | 0.002 | 0.005 | 0.046 | 0.0860 | 0.0860 | 4 | 0 |
| BX | 254 | 0.003 | 0.005 | 0.005 | -0.3372 | -0.3372 | 4 | 0 |
| CSCO | 254 | 0.002 | 0.005 | 0.738 | 0.6878 | 0.6878 | 5 | 0 |
| BBY | 257 | 0.002 | 0.005 | 0.005 | 0.1769 | 0.1769 | 4 | 0 |
| DG | 257 | 0.002 | 0.005 | 0.005 | 0.2164 | 0.2164 | 5 | 0 |
| EXPD | 257 | 0.003 | 0.005 | 0.005 | 0.5707 | 0.5707 | 2 | 0 |
| PWR | 257 | 0.002 | 0.005 | 0.006 | 0.7154 | 0.7154 | 5 | 0 |
| META | 257 | 0.003 | 0.005 | 0.082 | -0.0266 | -0.0266 | 4 | 0 |
| GEV | 257 | 0.003 | 0.005 | 0.006 | 0.6589 | 0.6589 | 4 | 0 |
| BE | 257 | 0.003 | 0.005 | 0.006 | 2.9578 | 2.9577 | 0 | 0 |
| MRNA | 257 | 0.002 | 0.005 | 0.006 | 6.7568 | 6.7568 | 0 | 0 |
| LNVGY | 254 | 0.003 | 1.389 | 85.837 | 1.9135 | 1.8882 | 1 | 0 |
| DIVZ | 34 | 0.050 | 0.224 | 12.480 | -0.0414 | -0.0426 | 1 | 0 |
| IDVZ | 34 | 0.062 | 0.194 | 21.824 | -0.0340 | -0.0361 | 1 | 0 |
| PFDE | 34 | 0.088 | 0.256 | 0.286 | 0.0068 | 0.0068 | 1 | 0 |
| PFOE | 34 | 0.132 | 0.317 | 0.341 | -0.0433 | -0.0433 | 1 | 0 |
| FXFXX | 24 | 1.030 | 3.119 | 3.950 | 0.0035 | 0.0000 | 0 | 0 |
| SALXX | 23 | 0.970 | 2.908 | 3.700 | 0.0032 | 0.0000 | 0 | 0 |

The 0.005 bp floor is Bloomberg's own rounding (six decimals of a fractional return).

## Finding 1 -- Yahoo's ex-date cash against Bloomberg's gross return on ex-dates

Shown, for dividends Yahoo records. Across the 12 year names, 41 Yahoo ex-dates fall on a common date in the window (ED 4, BX 4,
CSCO 4 of 5, BBY 4, DG 5, EXPD 2, PWR 5, META 4, GEV 4, LNVGY 1) -- excluding LNVGY the 36 differences are all at most 0.075 bp (ED's
four ex-date days: 0.0001, 0.046, 0.045, 0.042 bp). On those days the cash is large against the return it sits in (ED about 78-83 bp of
the prior close, BBY 104-150 bp, BX 88-115 bp, CSCO 37-60 bp), so a price-only return would miss that much; the (P + D) / P_prev form
reproduces Bloomberg's number to rounding. Cumulative TR agrees to four decimals for 10 of the 12 year names; BE differs in the last
digit (2.9578 vs 2.9577; no ex-dates) and LNVGY differs by Finding 2. The only year-name ex-date difference above 0.1 bp is LNVGY 2026-08-06 at 0.55 bp (cash 0.86 on an
ADR; Bloomberg -1.5029%, Yahoo -1.4974%); the cause of that 0.55 bp is not shown.
Bloomberg's field is "gross" dividends; the numbers show it equals Yahoo's headline cash per share, with no withholding visible on the
one ADR payer (LNVGY). Whether Bloomberg's gross figure would differ from Yahoo's for a name whose dividend carries a tax-withheld or
foreign-currency component other than LNVGY is not shown.

## Finding 2 -- a missed ex-date: Yahoo's dividend list is not always complete (shown on three names)

On non-event days (no ex-date in Yahoo's list) the largest daily difference is at most 0.082 bp for 10 of the 12 year names; CSCO's
largest is 0.738 bp (2025-10-07/08, offsetting; Bloomberg PX_LAST 68.985 against Yahoo 68.99, a price-source difference, not cash) and
LNVGY's other days reach about 2 bp. Three names show a large non-event-day gap, each equal to a cash payment Bloomberg includes and Yahoo does not list:

| name | date | Bloomberg ret | Yahoo ret | diff bp | implied cash (diff x prior close) | Bloomberg PX_LAST change |
|---|---|---|---|---|---|---|
| LNVGY | 2025-12-11 | -2.8366% | -3.6950% | 85.84 | about 0.218 per ADR | -3.69% (24.50 / 25.44) |
| DIVZ | 2026-09-29 | -0.4008% | -0.5256% | 12.48 | about 0.046 | -0.526% (36.716 / 36.91) |
| IDVZ | 2026-09-29 | -0.5425% | -0.7607% | 21.82 | about 0.073 | -0.761% (33.2648 / 33.52) |

In each case Bloomberg's own `PX_LAST` moves by the Yahoo-style price return, and its total-return field sits above it by the implied
amount; Yahoo's dividend list for the name has no entry on that date (LNVGY: entries 2025-07-31 and 2026-08-06 only; DIVZ latest
2026-08-28; IDVZ latest 2026-08-28). The implied cash is the numbers' reading, inferred and not a quoted Bloomberg dividend. For
LNVGY the implied 0.218 equals Yahoo's 2024-11-27 entry of 0.218; that is an observation, the identity of the missing payment is not
shown. Whether Yahoo adds these dividends later (the DIVZ/IDVZ date is about ten days before the pull) is not shown. Consequence: a Yahoo
total return is understated by exactly the missing cash, which moves the cumulative figure (LNVGY 1.9135 vs 1.8882; DIVZ -0.0414 vs
-0.0426; IDVZ -0.0340 vs -0.0361).

## Finding 3 -- a variable distribution (BX)

BX's four stored ex-dates carry four different amounts: 2025-11-03 1.29, 2026-02-09 1.49, 2026-05-04 1.16, 2026-08-03 1.29 (88, 115, 92
and 101 bp of the prior close). Yahoo's cash matches Bloomberg's gross return on each (differences 0.0007, 0.0040, 0.0052, 0.0037 bp),
and the whole-window cumulative TR is identical (-0.3372 both). So a variable amount is handled the same as a fixed one: Yahoo records
the amount per ex-date and the formula needs nothing else. Whether Yahoo or Bloomberg labels any of these as a "special" versus a
regular distribution is not shown -- neither source's stored fields carry a type, and the window holds one row per quarter, no
second same-quarter row.

## Finding 4 -- splits

Not shown on real data. None of the 18 names has a split inside the window (`splits_in_window` is 0 for all). The formula's split
handling is exercised only by the synthetic test `test_split_day_is_not_a_return` (a 4-for-1 day reads 0.0%, not -75%).
`yahoo_pull` stores Yahoo's own split history (e.g. LNVGY's 2000-03-08 4.0 ratio is outside the window).

## Finding 5 -- interest-type income

Two cases are in the stored names.
- Equity-income ETFs (DIVZ, IDVZ, PFDE, PFOE) pay a distribution that appears as an ordinary Yahoo dividend: one ex-date each in the
  window (DIVZ 0.115 and IDVZ 0.12 on 2026-08-28, PFDE 0.02 and PFOE 0.01 on 2026-09-28), matching Bloomberg to 0.03, 0.001, 0.035 and
  0.085 bp. The exceptions are the missed September payments in Finding 2. These funds are distributions of dividends and income,
  so the numbers cannot separate "interest" from "dividend" for them -- not shown.
- Money-market funds (FXFXX, SALXX): Bloomberg's total return is positive every day (about 1.0 bp on a weekday, about 3.0-4.0 bp on a
  Friday, i.e. the weekend accrual; FXFXX 2026-09-04 3.95 bp spans the Labor Day weekend), cumulative +0.35% (FXFXX, 24 days) and
  +0.32% (SALXX, 23 days). Yahoo shows a $1.00 close on every date and no dividend, so its total return is exactly 0.0000 in both.
  The interest is invisible to the Yahoo method: median abs difference 1.03 bp (FXFXX) and 0.97 bp (SALXX), all of it Bloomberg's accrual.
  Whether Yahoo's money-market series ever records the yield elsewhere (a separate field, a different symbol) is not shown.

## Recommended method for the TR column

1. Compute the daily TR from stored price and cash kept apart, `(P_t + D_t) / (P_{t-1} / s_t) - 1`, on the as-traded close and
   ex-date cash. For a Yahoo dividend payer with a complete dividend list this reproduces Bloomberg's gross total return to rounding
   (Finding 1): 36 of 36 comparable year-name ex-dates (LNVGY excluded) within 0.075 bp, 10 of 12 year names equal in cumulative TR. This is the method for the
   TR column and it needs no dividend-type logic for variable amounts (Finding 3).
2. The method's accuracy is the completeness of the cash list, not the formula. Where the Bloomberg TR field is stored for the same
   name and date it is the reference, and a difference larger than rounding on a day with no Yahoo ex-date is a missing cash row
   (Finding 2: 3 of the 18 names, each with one missed payment in its window). Because the TR is recomputed from the stored cash, a late-added dividend
   corrects the series on the next pass without touching prices.
3. Money-market and other interest-accruing names cannot take their interest from Yahoo (Finding 5): their TR must come from
   Bloomberg's field or an explicit accrual; the Yahoo method returns 0.
4. Not shown, so not recommended on this evidence: any split rule beyond the tested formula (Finding 4), and any special-versus-regular
   treatment (Finding 3).
5. The 6-name extension (KO, JNJ, T, VZ, MO, XOM) re-runs this script when the queued draw lands; only 30-34 stored days exist for them
   now.
