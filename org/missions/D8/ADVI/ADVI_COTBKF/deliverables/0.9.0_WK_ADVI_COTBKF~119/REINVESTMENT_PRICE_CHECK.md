# ADVI_COTBKF round 72, CB-bt-1: the build's close beside the custodian's reinvestment price

Worker 0.9.0_WK_ADVI_COTBKF~119, 2026-10-11. Read only; no code changed; no vendor data in the reading. Record: `REINVESTMENT_PRICE_CHECK.json`; table: `REINVESTMENT_PRICE_CHECK.csv` (270 fund series); per-security detail incl. ETF and Equity: `REINVESTMENT_PRICE_CHECK_DETAIL.csv`.

## 1. The reviewer's nine, reproduced

AMCPX, AMRMX, CWGIX, WGIFX, CPXIX, FINFX, NEWFX, AWSHX, WMFFX: 1,121 `dvr` rows in 221 (fund, date) events; **92** with a same-date close; close below the reinvestment price by more than 0.5 percent on **87**; above on 1; within 0.5 percent on 4; **9 of 9** funds; lowest ratio **0.47** (AWSHX). Reviewer: 9 / 92 / 87 / 0.47. No difference. (No row in the nine is under 0.05 shares; no cell has a wide spread.)

## 2. The rule (written 2026-10-11T18:37:42Z, before the whole-table run, kept)

Full text in the JSON `rule` key. In short: `dvr` rows, at least 0.05 shares, pooled amount over shares per (fund, date); a cell with more than 5 percent spread across accounts is dropped (none was); same-date close only; ratio = close over price. Confirmed adjusted: at least 5 usable dates, at least 60 percent below 0.98, and the later half's median ratio above the earlier half's. Confirmed not: at least 5 usable dates, at least 80 percent within 2 percent of 1, and at least 3 of them 730 or more days before the series' last close. Everything else is `nothing_to_test_on` with a reason; too few dates is never `confirmed_not`.

## 3. Three counts, 270 fund series

| | series |
|---|---|
| confirmed_adjusted | **19** |
| confirmed_not | **15** |
| nothing_to_test_on | **236** (72 no reinvestment row; 129 rows but none on a date the table has a close; 32 under 5 dates; 3 at 1 but too recent) |

Total 270, equal to round 71's 270. At the stricter guard (1 share): 19 / 12 / 239, the adjusted set identical. Of the 4,568 fund reinvestment dates the table holds a close on 796; 3 more fall within one trading day and are not read.

## 4. Against round 71

| round 71 group | series | confirmed_adjusted | confirmed_not | nothing_to_test_on |
|---|---|---|---|---|
| read adjusted | 72 | 19 | 0 | 53 |
| read not adjusted (left on store) | 1 | 0 | 0 | 1 |
| untested | 124 | 0 | 0 | 124 |
| substituted (control) | 73 | 0 | 15 | 58 |

**Disagreements (both readings definite and opposite): none.** The control holds: no substituted series reads adjusted; the 15 that can be read all read at 1. Of the 53 round-71-adjusted series this instrument cannot read, 16 lean adjusted on 1 to 4 dates (all below 0.98) and are not counted: AGTHX, AMBFX, AMCPX, AMECX, ANEFX, ANWPX, BALCX, FBALX, FOCPX, JGVVX, JLGMX, NEWFX, NRGSX, OIEJX, SMCWX, VGHAX. A 3-date minimum instead of 5 would read 27 adjusted / 17 not / 226 nothing (adds AGTHX, AMCPX, BALCX, FOCPX, GFFFX, NEWFX, NFFFX, VGHAX as adjusted); reported, not adopted. AMCPX (4 dates) and NEWFX (3 dates), two of the reviewer's nine, are among them under the rule as written.

## 5. ETF and Equity

ETF 276: 0 adjusted / 26 not / 250 nothing. Equity 934: 0 / 5 / 929. Round 71's 9 that read adjusted (VNM, XAR; GEHC, KGC, PWR, PYPL, RNG, TXT, WDC) have no reinvestment row: untested here.

## 6. Reach (confirmed_adjusted fund series, on or before the last date the ratio is below 0.98)

| | this round | round 71 |
|---|---|---|
| priced holding account-days | **261,182** (250,213 distinct account-days) | 287,912 |
| measured account-days (distinct) | **712** (1,030 summed over series) | 3,187 |

Ratio over the account-days (carried forward from the latest paired date): priced, below 0.9: 259,952; below 0.75: 233,427; below 0.5: 1,470 (30,256 lie before a fund's first paired date, where the ratio is an upper bound). Measured (distinct): below 0.9: 712; below 0.75: 459; below 0.5: 0.

## 7. Headline

Of 270 fund series, 19 are confirmed dividend-adjusted by the custodian's reinvestment price, 15 are confirmed not adjusted, and 236 have nothing to test on.

## 8. Not established

The 72 of round 71 are not cleared beyond the 19 (the table holds a close on 796 of 4,568 dates); the 124 untested stay untested; cause and serve are not examined; no return was recomputed; between paired dates the ratio is carried forward. See the JSON `not_established`.
