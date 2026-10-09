# Commonwealth mover causes (CB-u-1)

Why did the `neither` months graded MATCH (list `none`) and DIFF (list `sweeps-v1-20261008`) move? The class rule is stated first and was fixed in the script before any count was read.

## The rule

THE RULE (written here, before any count; every constant below is fixed in this file, not tuned to the run).
Per mover month and per arm, with V the account value, F the day's external flow (identical in both arms: a sweep buy or sell is
INTERNAL in both), r_t = (V_t - F_t)/V_(t-1) - 1 the daily return, in LOG-PERCENT points (100 x ln):
    month total   T   = 100 x sum ln(1 + r_t)                                   (the chained month: 100 x ln(1 + computed/100))
    value change  Cv  = 100 x ln(V_last / V_(first day - 1))                    (what the value did)
    flow taken out Cf = T - Cv = 100 x sum ln(1 - F_t / V_t)                    (what taking the flow out did)
D_t = V_after_t - V_before_t is the sweep balance the after arm carries and the before arm does not (the cash legs of the sweep
trades). A SWEEP-TRADE DAY is a day on which D changes (|D_t - D_(t-1)| > 0.005): the day the account traded a listed sweep.
    e_v = Cv_before - Cv_after,  e_f = Cf_before - Cf_after   (how far each before-state component is from the corrected path)
    s   = T_before - T_after = e_v + e_f                       (the move)
    s_bal   = the part of s from days with NO sweep trade;  s_trade = the part from sweep-trade days   (s = s_bal + s_trade)
Classes, tried IN THIS ORDER; the first that fits decides (the other tests are still printed as flags):
 1. unexplained (blank)  a day is blank or a value / return is not finite, or the arms' day values do not reproduce the persisted
                         grades: `other:unexplained`.
 2. unexplained (no move) |s| < 1e-9: the two arms' day values give the same month, so no sweep value moves it: `other:unexplained`.
 3. offsetting      e_v and e_f have opposite signs, EACH |e| >= OFFSET_MIN_PCT (the grade tolerance, 0.05: each alone would have
                    broken the match) and min(|e_v|, |e_f|) / max(|e_v|, |e_f|) >= OFFSET_RATIO (0.5: about the same amount):
                    the before-state's value change and flow taken out were each wrong, in opposite directions, so the match
                    was a cancellation.
 4. sweep_balance   |s_bal| > |s_trade|: the sweep balance now entering the daily value moves the month through days on which
                    the account made no sweep trade (the after-arm value differs from the before-arm value on those days).
 5. other:sweep_trade_day  |s_trade| > |s_bal|: the month's own sweep trade(s) carry the move (a named further cause).
 6. other:unexplained     |s_trade| == |s_bal| (a tie): no rule fits; never forced into a class.
A month satisfying rules 3 and 4 is counted once, as offsetting; the md prints how many months satisfy each test (the overlap).
Core months (the account holds 316067107) are put through the SAME rule and reported apart; they are never in the count of
the `neither` movers. A month with class other_mmf is out of scope here (none exist in the persisted classes; the count is printed).

## Counts

Persisted grades read: 82593 BEFORE rows, 82593 AFTER rows. Mover months in scope: 147 `neither` (the count), 16 `core` (apart); out of scope (other_mmf): 0.

### The `neither` movers (147)

| cause | months |
|---|---|
| other:sweep_trade_day | 75 |
| sweep_balance | 72 |
| total | 147 |

sweep_balance=72 offsetting=0 other=75 (sum 147 of 147: sum_ok=True)

Tests satisfied (a month can satisfy more than one; the class is the first that fits): offsetting test 0, balance-dominant 72, trade-dominant 75; offsetting test AND balance-dominant 0. Re-derived day values reproduce the persisted grade (recompute_ok): 147 of 147.

## The traces (one month per class, the largest |s| of the class)

### TRACE sweep_balance: account D49141714, month 2019-02 -- class `sweep_balance`

Rule reading: s_bal=-3.2159 from no-trade days exceeds s_trade=0.0000.

Components (log-pct points; before / after / before minus after): value change Cv 0.0416 / 3.2575 / e_v -3.2159; flow taken out Cf 0.0 / -0.0 / e_f 0.0; move s = -3.2159 (from no-trade days s_bal -3.2159, from sweep-trade days s_trade 0.0); 0 sweep-trade day(s) of 19.

Chained month: before 0.0416 pct (list `none`), after 3.3111 pct (list v1), reported 0.04 pct.

| date | value before | value after | D = after - before | sweep-trade day | flow | return before | return after |
|---|---|---|---|---|---|---|---|
| 2019-02-01 | 4061.9 | 51.04 | -4010.86 |  | 0.0 | 0.0 | 0.0 |
| 2019-02-04 | 4061.9 | 51.04 | -4010.86 |  | 0.0 | 0.0 | 0.0 |
| 2019-02-05 | 4061.9 | 51.04 | -4010.86 |  | 0.0 | 0.0 | 0.0 |
| 2019-02-06 | 4061.9 | 51.04 | -4010.86 |  | 0.0 | 0.0 | 0.0 |
| 2019-02-07 | 4061.9 | 51.04 | -4010.86 |  | 0.0 | 0.0 | 0.0 |
| 2019-02-08 | 4061.9 | 51.04 | -4010.86 |  | 0.0 | 0.0 | 0.0 |
| 2019-02-11 | 4061.9 | 51.04 | -4010.86 |  | 0.0 | 0.0 | 0.0 |
| 2019-02-12 | 4061.9 | 51.04 | -4010.86 |  | 0.0 | 0.0 | 0.0 |
| 2019-02-13 | 4061.9 | 51.04 | -4010.86 |  | 0.0 | 0.0 | 0.0 |
| 2019-02-14 | 4061.9 | 51.04 | -4010.86 |  | 0.0 | 0.0 | 0.0 |
| 2019-02-15 | 4061.9 | 51.04 | -4010.86 |  | 0.0 | 0.0 | 0.0 |
| 2019-02-19 | 4061.9 | 51.04 | -4010.86 |  | 0.0 | 0.0 | 0.0 |
| 2019-02-20 | 4061.9 | 51.04 | -4010.86 |  | 0.0 | 0.0 | 0.0 |
| 2019-02-21 | 4061.9 | 51.04 | -4010.86 |  | 0.0 | 0.0 | 0.0 |
| 2019-02-22 | 4061.9 | 51.04 | -4010.86 |  | 0.0 | 0.0 | 0.0 |
| 2019-02-25 | 4061.9 | 51.04 | -4010.86 |  | 0.0 | 0.0 | 0.0 |
| 2019-02-26 | 4061.9 | 51.04 | -4010.86 |  | 0.0 | 0.0 | 0.0 |
| 2019-02-27 | 4061.9 | 51.04 | -4010.86 |  | 0.0 | 0.0 | 0.0 |
| 2019-02-28 | 4063.59 | 52.73 | -4010.86 |  | 0.0 | 0.000416 | 0.033111 |

### TRACE other:sweep_trade_day: account acct#65b3b3ea, month 2024-12 -- class `other:sweep_trade_day`

Rule reading: s_trade=0.8647 from sweep-trade days exceeds s_bal=0.0348.

Components (log-pct points; before / after / before minus after): value change Cv -8.3206 / -9.2201 / e_v 0.8995; flow taken out Cf -0.0 / -0.0 / e_f 0.0; move s = 0.8995 (from no-trade days s_bal 0.0348, from sweep-trade days s_trade 0.8647); 2 sweep-trade day(s) of 21.

Chained month: before -7.9838 pct (list `none`), after -8.8079 pct (list v1), reported -8.02 pct.

| date | value before | value after | D = after - before | sweep-trade day | flow | return before | return after |
|---|---|---|---|---|---|---|---|
| 2024-12-02 | 22810.89 | 22810.89 | 0.0 |  | 0.0 | -0.000933 | -0.000933 |
| 2024-12-03 | 22776.05 | 22776.05 | 0.0 |  | 0.0 | -0.001527 | -0.001527 |
| 2024-12-04 | 22119.88 | 22119.88 | 0.0 |  | 0.0 | -0.028809 | -0.028809 |
| 2024-12-05 | 22216.66 | 22216.66 | 0.0 |  | 0.0 | 0.004375 | 0.004375 |
| 2024-12-06 | 21982.46 | 21982.46 | 0.0 |  | 0.0 | -0.010542 | -0.010542 |
| 2024-12-09 | 21852.77 | 21852.77 | 0.0 |  | 0.0 | -0.005899 | -0.005899 |
| 2024-12-10 | 22008.23 | 21808.25 | -199.98 | yes | 0.0 | 0.007114 | -0.002037 |
| 2024-12-11 | 21851.22 | 21663.08 | -188.14 | yes | 0.0 | -0.007134 | -0.006657 |
| 2024-12-12 | 21831.87 | 21643.73 | -188.14 |  | 0.0 | -0.000886 | -0.000893 |
| 2024-12-13 | 21642.18 | 21454.04 | -188.14 |  | 0.0 | -0.008689 | -0.008764 |
| 2024-12-16 | 21183.45 | 20995.31 | -188.14 |  | 0.0 | -0.021196 | -0.021382 |
| 2024-12-17 | 21094.41 | 20906.27 | -188.14 |  | 0.0 | -0.004203 | -0.004241 |
| 2024-12-18 | 20786.65 | 20598.51 | -188.14 |  | 0.0 | -0.01459 | -0.014721 |
| 2024-12-19 | 20610.51 | 20422.37 | -188.14 |  | 0.0 | -0.008474 | -0.008551 |
| 2024-12-20 | 20680.19 | 20492.05 | -188.14 |  | 0.0 | 0.003381 | 0.003412 |
| 2024-12-23 | 20763.43 | 20575.29 | -188.14 |  | 0.0 | 0.004025 | 0.004062 |
| 2024-12-24 | 20782.78 | 20594.64 | -188.14 |  | 0.0 | 0.000932 | 0.000941 |
| 2024-12-26 | 20800.2 | 20612.06 | -188.14 |  | 0.0 | 0.000838 | 0.000846 |
| 2024-12-27 | 20798.26 | 20610.12 | -188.14 |  | 0.0 | -9.3e-05 | -9.4e-05 |
| 2024-12-30 | 20658.9 | 20470.76 | -188.14 |  | 0.0 | -0.006701 | -0.006762 |
| 2024-12-31 | 21009.29 | 20821.15 | -188.14 |  | 0.0 | 0.016961 | 0.017117 |

No `neither` month fell in: offsetting (nothing to trace).

## The `core` months, apart (same rule, never in the count above)

core months: 16. other:sweep_trade_day=15, sweep_balance=1

| account | month | cause | reported | before | after | e_v | e_f | s | s_bal | s_trade | reason |
|---|---|---|---|---|---|---|---|---|---|---|---|
| acct#f6c79f45 | 2024-06 | other:sweep_trade_day | -0.88 | -0.8874 | 1.2105 | -2.0946 | -0.0 | -2.0946 | 0.0511 | -2.1457 | s_trade=-2.1457 from sweep-trade days exceeds s_bal=0.0511 |
| acct#9727ac87 | 2024-07 | other:sweep_trade_day | -0.08 | -0.0415 | -0.0234 | -0.0181 | -0.0 | -0.0181 | 0.0002 | -0.0183 | s_trade=-0.0183 from sweep-trade days exceeds s_bal=0.0002 |
| D49143350 | 2023-11 | sweep_balance | -4.59 | -4.6175 | -5.3344 | 0.7545 | -0.0 | 0.7545 | 0.7545 | 0.0 | s_bal=0.7545 from no-trade days exceeds s_trade=0.0000 |
| D49143350 | 2026-02 | other:sweep_trade_day | 2.05 | 2.0179 | -16.069 | 19.546 | -0.0306 | 19.5154 | -1.2107 | 20.7261 | s_trade=20.7261 from sweep-trade days exceeds s_bal=-1.2107 |
| acct#557ce060 | 2026-01 | other:sweep_trade_day | 0.02 | 0.0118 | 0.0988 | -0.087 | -0.0 | -0.087 | -0.0264 | -0.0606 | s_trade=-0.0606 from sweep-trade days exceeds s_bal=-0.0264 |
| acct#c0cea213 | 2024-10 | other:sweep_trade_day | -0.0 | 0.0329 | 0.1609 | -0.1279 | 0.0 | -0.1279 | -0.0013 | -0.1266 | s_trade=-0.1266 from sweep-trade days exceeds s_bal=-0.0013 |
| acct#7f62f16f | 2025-02 | other:sweep_trade_day | 0.06 | 0.0995 | 0.1518 | -0.0547 | 0.0024 | -0.0523 | -0.0052 | -0.0471 | s_trade=-0.0471 from sweep-trade days exceeds s_bal=-0.0052 |
| acct#61ebda90 | 2025-04 | other:sweep_trade_day | 0.09 | 0.0436 | 95.1114 | -66.7964 | 0.0 | -66.7964 | -0.0019 | -66.7946 | s_trade=-66.7946 from sweep-trade days exceeds s_bal=-0.0019 |
| acct#ce1f487c | 2025-04 | other:sweep_trade_day | 0.09 | 0.0436 | 95.1114 | -66.7964 | 0.0 | -66.7964 | -0.0019 | -66.7946 | s_trade=-66.7946 from sweep-trade days exceeds s_bal=-0.0019 |
| acct#16bf540c | 2025-04 | other:sweep_trade_day | 0.09 | 0.0436 | 95.1114 | -66.7964 | 0.0 | -66.7964 | -0.0019 | -66.7946 | s_trade=-66.7946 from sweep-trade days exceeds s_bal=-0.0019 |
| acct#177b7e48 | 2025-04 | other:sweep_trade_day | 0.09 | 0.0436 | 95.1114 | -66.7964 | 0.0 | -66.7964 | -0.0019 | -66.7946 | s_trade=-66.7946 from sweep-trade days exceeds s_bal=-0.0019 |
| acct#aed810ab | 2025-04 | other:sweep_trade_day | 0.09 | 0.0436 | 95.1116 | -66.7965 | 0.0 | -66.7965 | -0.0019 | -66.7947 | s_trade=-66.7947 from sweep-trade days exceeds s_bal=-0.0019 |
| acct#781a748b | 2025-04 | other:sweep_trade_day | 0.09 | 0.0436 | 95.1114 | -66.7964 | 0.0 | -66.7964 | -0.0019 | -66.7946 | s_trade=-66.7946 from sweep-trade days exceeds s_bal=-0.0019 |
| acct#1b22f63a | 2025-04 | other:sweep_trade_day | 0.09 | 0.0436 | 95.1114 | -66.7964 | 0.0 | -66.7964 | -0.0019 | -66.7946 | s_trade=-66.7946 from sweep-trade days exceeds s_bal=-0.0019 |
| acct#744c9c00 | 2025-06 | other:sweep_trade_day | 0.15 | 0.1042 | 99.2457 | -68.8602 | 0.0275 | -68.8328 | -0.0003 | -68.8324 | s_trade=-68.8324 from sweep-trade days exceeds s_bal=-0.0003 |
| acct#5fd6a5d4 | 2026-05 | other:sweep_trade_day | 0.03 | 0.0283 | 0.265 | -0.2364 | -0.0 | -0.2364 | 0.0 | -0.2364 | s_trade=-0.2364 from sweep-trade days exceeds s_bal=0.0000 |

## Every `neither` mover, named

| account | month | cause | reported | before | after | e_v | e_f | s | s_bal | s_trade |
|---|---|---|---|---|---|---|---|---|---|---|
| acct#aaeb760c | 2021-10 | sweep_balance | 5.51 | 5.4855 | 6.0313 | -0.5161 | 0.0 | -0.5161 | -0.5161 | 0.0 |
| acct#aaeb760c | 2022-03 | sweep_balance | 4.82 | 4.7791 | 5.0603 | -0.268 | 0.0 | -0.268 | -0.7994 | 0.5315 |
| acct#aaeb760c | 2022-08 | other:sweep_trade_day | -1.06 | -1.0435 | -1.3538 | 0.314 | 0.0 | 0.314 | 0.0914 | 0.2226 |
| acct#aaeb760c | 2023-12 | sweep_balance | 1.56 | 1.5886 | 1.6144 | -0.0254 | -0.0 | -0.0254 | -0.2263 | 0.201 |
| acct#aaeb760c | 2025-03 | other:sweep_trade_day | -7.16 | -7.1874 | -7.4127 | 0.243 | 0.0 | 0.243 | -0.0406 | 0.2836 |
| acct#b4db1f25 | 2020-01 | sweep_balance | 0.02 | 0.0169 | 0.0835 | -0.0665 | 0.0 | -0.0665 | -0.0665 | 0.0 |
| acct#b4db1f25 | 2020-02 | sweep_balance | 0.02 | 0.0158 | 0.0781 | -0.0622 | -0.0 | -0.0622 | -0.0622 | 0.0 |
| acct#b4db1f25 | 2020-11 | other:sweep_trade_day | 0.08 | 0.0654 | 0.0034 | 0.0619 | 0.0 | 0.0619 | -0.0028 | 0.0647 |
| acct#03836058 | 2022-04 | sweep_balance | -1.41 | -1.3963 | -2.7833 | 1.4166 | 0.0 | 1.4166 | 1.4166 | 0.0 |
| acct#eea1157e | 2021-05 | sweep_balance | 0.76 | 0.7731 | 1.3492 | -0.57 | -0.0 | -0.57 | -0.57 | 0.0 |
| acct#eea1157e | 2022-12 | other:sweep_trade_day | -0.04 | 0.0072 | -0.5123 | 0.5208 | 0.0 | 0.5208 | 0.0032 | 0.5175 |
| acct#eea1157e | 2023-07 | other:sweep_trade_day | -0.02 | -0.0182 | 0.0314 | -0.0496 | -0.0 | -0.0496 | 0.2916 | -0.3412 |
| acct#eea1157e | 2024-09 | other:sweep_trade_day | 0.13 | 0.1142 | -0.3309 | 0.4456 | 0.0 | 0.4456 | -0.6689 | 1.1145 |
| acct#eea1157e | 2025-08 | sweep_balance | 1.22 | 1.2591 | 1.974 | -0.7036 | -0.0 | -0.7036 | -0.7036 | 0.0 |
| acct#1c3da532 | 2017-08 | sweep_balance | 0.0 | 0.0039 | 0.0503 | -0.0464 | -0.0 | -0.0464 | -0.0464 | 0.0 |
| acct#1c3da532 | 2017-10 | sweep_balance | 0.0 | 0.0039 | 0.0502 | -0.0463 | -0.0 | -0.0463 | -0.0463 | 0.0 |
| acct#1c3da532 | 2017-12 | sweep_balance | 0.0 | 0.0039 | 0.0502 | -0.0463 | -0.0 | -0.0463 | -0.0463 | 0.0 |
| acct#1c3da532 | 2018-01 | sweep_balance | 0.01 | 0.0112 | 0.1447 | -0.1334 | 0.0 | -0.1334 | -0.1334 | 0.0 |
| acct#1c3da532 | 2018-02 | sweep_balance | 0.01 | 0.0106 | 0.1363 | -0.1256 | -0.0 | -0.1256 | -0.1256 | 0.0 |
| acct#1c3da532 | 2018-03 | sweep_balance | 0.01 | 0.013 | 0.1669 | -0.1538 | 0.0 | -0.1538 | -0.1538 | 0.0 |
| acct#5aa91f68 | 2017-07 | sweep_balance | 0.0 | 0.002 | 0.093 | -0.091 | 0.0 | -0.091 | -0.091 | 0.0 |
| acct#5aa91f68 | 2017-08 | sweep_balance | 0.0 | 0.0042 | 0.1956 | -0.1912 | 0.0 | -0.1912 | -0.1912 | 0.0 |
| acct#5aa91f68 | 2017-09 | sweep_balance | 0.0 | 0.0039 | 0.1854 | -0.1813 | -0.0 | -0.1813 | -0.1813 | 0.0 |
| acct#5aa91f68 | 2017-10 | sweep_balance | 0.0 | 0.0042 | 0.1948 | -0.1905 | -0.0 | -0.1905 | -0.1905 | 0.0 |
| acct#5aa91f68 | 2017-12 | sweep_balance | 0.0 | 0.0041 | 0.1892 | -0.185 | 0.0 | -0.185 | -0.185 | 0.0 |
| acct#5aa91f68 | 2018-01 | sweep_balance | 0.01 | 0.0119 | 0.5521 | -0.5387 | 0.0 | -0.5387 | -0.5387 | 0.0 |
| acct#5aa91f68 | 2018-02 | sweep_balance | 0.01 | 0.0112 | 0.5201 | -0.5075 | 0.0 | -0.5075 | -0.5075 | 0.0 |
| acct#5aa91f68 | 2018-03 | sweep_balance | 0.01 | 0.0137 | 0.6324 | -0.6167 | -0.0 | -0.6167 | -0.6167 | 0.0 |
| acct#5aa91f68 | 2018-04 | sweep_balance | 0.02 | 0.0201 | 0.9189 | -0.8946 | 0.0 | -0.8946 | -0.8946 | 0.0 |
| acct#5aa91f68 | 2018-05 | sweep_balance | 0.02 | 0.0207 | 0.9388 | -0.9137 | -0.0 | -0.9137 | -0.9137 | 0.0 |
| acct#5aa91f68 | 2018-06 | sweep_balance | 0.02 | 0.0201 | 0.902 | -0.8779 | -0.0 | -0.8779 | -0.8779 | 0.0 |
| acct#04ebe1d1 | 2021-04 | sweep_balance | -3.41 | -3.4508 | -3.4979 | 0.0488 | 0.0 | 0.0488 | 0.0488 | 0.0 |
| acct#04ebe1d1 | 2021-06 | sweep_balance | -4.82 | -4.8644 | -4.9327 | 0.0718 | -0.0 | 0.0718 | 0.0718 | 0.0 |
| acct#04ebe1d1 | 2021-10 | sweep_balance | -1.39 | -1.4342 | -1.4564 | 0.0225 | 0.0 | 0.0225 | 0.0225 | 0.0 |
| acct#04ebe1d1 | 2024-05 | other:sweep_trade_day | 0.67 | 0.6758 | 0.6079 | 0.0674 | 0.0 | 0.0674 | -0.0111 | 0.0785 |
| acct#015306a0 | 2023-04 | other:sweep_trade_day | 1.23 | 1.2331 | 1.1523 | 0.0799 | 0.0 | 0.0799 | -0.0219 | 0.1018 |
| acct#fa488a0b | 2021-04 | sweep_balance | 2.21 | 2.2439 | 2.2794 | -0.0347 | 0.0 | -0.0347 | -0.0347 | 0.0 |
| acct#fa488a0b | 2021-08 | sweep_balance | 1.0 | 1.0456 | 1.0615 | -0.0157 | -0.0 | -0.0157 | -0.0157 | 0.0 |
| acct#fa488a0b | 2021-10 | sweep_balance | 2.52 | 2.5402 | 2.5791 | -0.038 | 0.0 | -0.038 | -0.038 | 0.0 |
| acct#fa488a0b | 2023-04 | other:sweep_trade_day | 1.0 | 1.0012 | 1.1639 | -0.1609 | -0.0 | -0.1609 | -0.0079 | -0.153 |
| acct#fa488a0b | 2023-07 | other:sweep_trade_day | 2.9 | 2.9077 | 3.0773 | -0.1647 | -0.0 | -0.1647 | -0.0114 | -0.1533 |
| acct#fa488a0b | 2024-01 | other:sweep_trade_day | -0.95 | -0.9005 | -1.1563 | 0.2584 | 0.0 | 0.2584 | 0.0023 | 0.2562 |
| acct#21515eb6 | 2025-04 | other:sweep_trade_day | 0.53 | 0.5019 | 0.8003 | -0.2964 | 0.0 | -0.2964 | 0.1083 | -0.4048 |
| acct#21515eb6 | 2025-05 | sweep_balance | 8.21 | 8.2042 | 8.2754 | -0.0658 | -0.0 | -0.0658 | -0.0658 | 0.0 |
| acct#2d4385bf | 2022-03 | sweep_balance | 4.92 | 4.9078 | 4.9714 | -0.0607 | 0.0 | -0.0607 | -0.0607 | 0.0 |
| acct#2d4385bf | 2023-04 | other:sweep_trade_day | -1.04 | -1.0474 | -1.1362 | 0.0897 | -0.0 | 0.0897 | 0.0276 | 0.0621 |
| acct#ab0c6781 | 2018-01 | sweep_balance | 0.18 | 0.1777 | 0.5903 | -0.4111 | 0.0 | -0.4111 | -0.5767 | 0.1656 |
| acct#ab0c6781 | 2018-02 | sweep_balance | 0.01 | 0.0113 | 0.5544 | -0.5416 | 0.0 | -0.5416 | -0.5416 | 0.0 |
| acct#ab0c6781 | 2018-03 | sweep_balance | 0.01 | 0.0138 | 0.6766 | -0.6605 | -0.0 | -0.6605 | -0.6605 | 0.0 |
| acct#92164e0d | 2017-03 | other:sweep_trade_day | -0.09 | -0.0454 | 0.0008 | -0.0463 | -0.0 | -0.0463 | -0.0004 | -0.0458 |
| acct#ebb31a1c | 2017-03 | other:sweep_trade_day | -0.09 | -0.0465 | 0.0008 | -0.0473 | 0.0 | -0.0473 | -0.0004 | -0.0469 |
| acct#dfa7a25c | 2017-06 | other:sweep_trade_day | -0.1 | -0.051 | 0.0008 | -0.0518 | -0.0 | -0.0518 | -0.0004 | -0.0514 |
| acct#4040a6ea | 2017-09 | other:sweep_trade_day | -0.07 | -0.0372 | 0.0041 | -0.0413 | 0.0 | -0.0413 | -0.0021 | -0.0392 |
| acct#0e2c97b9 | 2018-07 | other:sweep_trade_day | -0.08 | -0.0404 | 0.0476 | -0.0881 | 0.0 | -0.0881 | -0.0238 | -0.0643 |
| acct#de79caf1 | 2018-07 | other:sweep_trade_day | -0.08 | -0.0404 | 0.0476 | -0.0881 | -0.0 | -0.0881 | -0.0238 | -0.0643 |
| acct#25880078 | 2021-07 | other:sweep_trade_day | -0.04 | -0.0173 | -0.7036 | 0.6887 | -0.0 | 0.6887 | 0.0007 | 0.688 |
| acct#25880078 | 2022-01 | other:sweep_trade_day | -9.71 | -9.669 | -9.3296 | -0.3755 | 0.0005 | -0.375 | 0.0158 | -0.3908 |
| acct#25880078 | 2023-04 | other:sweep_trade_day | 0.65 | 0.6165 | 0.9938 | -0.3743 | -0.0 | -0.3743 | 0.003 | -0.3772 |
| acct#8680d8f4 | 2018-06 | other:sweep_trade_day | -0.08 | -0.0406 | 0.044 | -0.0847 | -0.0 | -0.0847 | -0.022 | -0.0627 |
| acct#e29efebe | 2020-10 | other:sweep_trade_day | -4.06 | -4.0428 | -3.7118 | -0.3443 | -0.0 | -0.3443 | 0.0113 | -0.3556 |
| acct#e29efebe | 2020-12 | other:sweep_trade_day | 4.15 | 4.1387 | 3.8748 | 0.2537 | -0.0 | 0.2537 | -0.0226 | 0.2762 |
| acct#e29efebe | 2021-01 | other:sweep_trade_day | 3.93 | 3.8931 | 4.262 | -0.3544 | -0.0 | -0.3544 | 0.0 | -0.3544 |
| acct#e29efebe | 2021-03 | other:sweep_trade_day | 1.7 | 1.6982 | 1.45 | 0.2444 | 0.0 | 0.2444 | 0.0019 | 0.2425 |
| acct#e29efebe | 2021-09 | other:sweep_trade_day | -6.42 | -6.3785 | -6.5812 | 0.2167 | -0.0 | 0.2167 | 0.0209 | 0.1958 |
| acct#e29efebe | 2021-12 | other:sweep_trade_day | 1.91 | 1.913 | 1.7259 | 0.1838 | 0.0 | 0.1838 | -0.0092 | 0.193 |
| acct#e29efebe | 2022-03 | other:sweep_trade_day | 3.37 | 3.3653 | 3.1712 | 0.1879 | 0.0 | 0.1879 | -0.0398 | 0.2278 |
| acct#e29efebe | 2022-06 | other:sweep_trade_day | -5.26 | -5.2245 | -5.5037 | 0.295 | 0.0 | 0.295 | 0.039 | 0.256 |
| acct#e29efebe | 2022-12 | other:sweep_trade_day | -5.66 | -5.6204 | -5.9713 | 0.3725 | 0.0 | 0.3725 | 0.114 | 0.2585 |
| acct#e29efebe | 2023-04 | sweep_balance | 6.46 | 6.4297 | 6.5457 | -0.1089 | 0.0 | -0.1089 | -0.116 | 0.0071 |
| acct#e29efebe | 2023-12 | other:sweep_trade_day | -0.55 | -0.5243 | -0.7259 | 0.2028 | 0.0 | 0.2028 | -0.0285 | 0.2313 |
| acct#e29efebe | 2024-02 | sweep_balance | 3.97 | 4.0017 | 4.0695 | -0.0651 | 0.0 | -0.0651 | -0.0651 | 0.0 |
| acct#e29efebe | 2024-12 | other:sweep_trade_day | -0.26 | -0.2414 | -0.431 | 0.1902 | -0.0 | 0.1902 | 0.0212 | 0.169 |
| acct#79d02c2c | 2023-05 | sweep_balance | 0.1 | 0.1307 | 0.0043 | 0.1263 | 0.0 | 0.1263 | 0.1515 | -0.0252 |
| acct#79d02c2c | 2024-07 | other:sweep_trade_day | 1.94 | 1.9751 | 1.8241 | 0.1482 | 0.0 | 0.1482 | -0.2489 | 0.3971 |
| acct#79d02c2c | 2024-11 | sweep_balance | 5.35 | 5.3014 | 5.5761 | -0.2606 | -0.0 | -0.2606 | -0.2788 | 0.0183 |
| acct#79d02c2c | 2025-01 | sweep_balance | 2.21 | 2.1652 | 2.4415 | -0.27 | -0.0 | -0.27 | -0.23 | -0.0401 |
| acct#4a890dd1 | 2023-05 | sweep_balance | 0.11 | 0.1379 | 0.0153 | 0.1225 | -0.0 | 0.1225 | 0.1502 | -0.0277 |
| acct#4a890dd1 | 2024-07 | other:sweep_trade_day | 1.94 | 1.9836 | 1.8256 | 0.155 | -0.0 | 0.155 | -0.245 | 0.4 |
| acct#4a890dd1 | 2025-01 | sweep_balance | 2.23 | 2.1802 | 2.4546 | -0.2682 | -0.0 | -0.2682 | -0.2269 | -0.0413 |
| acct#4a890dd1 | 2025-05 | sweep_balance | 4.83 | 4.8549 | 5.0695 | -0.2045 | 0.0 | -0.2045 | -0.2473 | 0.0428 |
| acct#3b89d062 | 2022-07 | other:sweep_trade_day | -0.08 | -0.0493 | 0.0319 | -0.0813 | 0.0 | -0.0813 | -0.0192 | -0.0621 |
| acct#3b89d062 | 2022-10 | other:sweep_trade_day | -0.07 | -0.0518 | 0.0829 | -0.1346 | -0.0 | -0.1346 | -0.0587 | -0.0759 |
| acct#3b89d062 | 2022-11 | sweep_balance | 0.03 | 0.0247 | 0.0848 | -0.0601 | 0.0 | -0.0601 | -0.0601 | 0.0 |
| acct#3b89d062 | 2022-12 | sweep_balance | 0.06 | 0.0452 | 0.1552 | -0.1098 | -0.0 | -0.1098 | -0.1098 | 0.0 |
| acct#3b89d062 | 2023-01 | sweep_balance | -0.04 | -0.0259 | 0.1549 | -0.1807 | 0.0 | -0.1807 | -0.1096 | -0.0711 |
| acct#3b89d062 | 2023-02 | sweep_balance | 0.06 | 0.0409 | 0.1398 | -0.0988 | -0.0 | -0.0988 | -0.0988 | 0.0 |
| acct#6acbfb93 | 2021-06 | other:sweep_trade_day | -0.09 | -0.0468 | 0.0008 | -0.0476 | -0.0 | -0.0476 | -0.0004 | -0.0472 |
| acct#921b5169 | 2022-04 | other:sweep_trade_day | -0.06 | -0.0299 | 0.0007 | -0.0307 | -0.0 | -0.0307 | -0.0004 | -0.0303 |
| acct#921b5169 | 2022-07 | other:sweep_trade_day | -0.05 | -0.0241 | 0.0118 | -0.036 | 0.0 | -0.036 | -0.0057 | -0.0303 |
| acct#921b5169 | 2023-04 | other:sweep_trade_day | -0.0 | -0.0002 | 0.0611 | -0.0612 | 0.0 | -0.0612 | -0.0304 | -0.0309 |
| acct#921b5169 | 2023-07 | sweep_balance | 0.0 | 0.0006 | 0.0631 | -0.0624 | -0.0 | -0.0624 | -0.0313 | -0.0311 |
| acct#921b5169 | 2023-10 | other:sweep_trade_day | -0.0 | -0.0011 | 0.063 | -0.0641 | 0.0 | -0.0641 | -0.0313 | -0.0329 |
| acct#921b5169 | 2024-01 | other:sweep_trade_day | -0.0 | -0.0002 | 0.0628 | -0.063 | 0.0 | -0.063 | -0.0311 | -0.0319 |
| acct#921b5169 | 2024-04 | other:sweep_trade_day | -0.01 | -0.0051 | 0.0605 | -0.0656 | -0.0 | -0.0656 | -0.0298 | -0.0358 |
| acct#921b5169 | 2024-07 | other:sweep_trade_day | -0.01 | -0.0052 | 0.0624 | -0.0675 | -0.0 | -0.0675 | -0.0307 | -0.0369 |
| acct#921b5169 | 2024-10 | other:sweep_trade_day | -0.01 | -0.0059 | 0.0618 | -0.0676 | -0.0 | -0.0676 | -0.03 | -0.0376 |
| acct#921b5169 | 2025-01 | other:sweep_trade_day | -0.04 | -0.0178 | 0.0359 | -0.0537 | 0.0 | -0.0537 | -0.0148 | -0.0388 |
| acct#921b5169 | 2025-04 | other:sweep_trade_day | -0.06 | -0.0294 | 0.0172 | -0.0467 | -0.0 | -0.0467 | -0.0071 | -0.0396 |
| acct#3345c43a | 2023-01 | other:sweep_trade_day | -0.06 | -0.029 | 0.1934 | -0.2222 | -0.0 | -0.2222 | -0.0959 | -0.1263 |
| acct#3345c43a | 2023-04 | other:sweep_trade_day | -0.06 | -0.028 | 0.1797 | -0.2076 | -0.0 | -0.2076 | -0.0887 | -0.1188 |
| acct#3345c43a | 2023-07 | other:sweep_trade_day | -0.07 | -0.0366 | 0.1546 | -0.1911 | -0.0 | -0.1911 | -0.0761 | -0.115 |
| acct#3345c43a | 2023-10 | other:sweep_trade_day | -0.09 | -0.0428 | 0.1575 | -0.2001 | -0.0 | -0.2001 | -0.0772 | -0.1229 |
| acct#1f02bee1 | 2022-10 | other:sweep_trade_day | 11.87 | 11.8922 | 11.5015 | 0.3498 | -0.0 | 0.3498 | -0.0298 | 0.3796 |
| acct#1f02bee1 | 2022-11 | sweep_balance | 18.29 | 18.2894 | 18.3535 | -0.0542 | -0.0 | -0.0542 | -0.0542 | 0.0 |
| acct#16f4eae3 | 2025-01 | other:sweep_trade_day | 0.92 | 0.9233 | 1.3343 | -0.4065 | 0.0 | -0.4065 | -0.053 | -0.3535 |
| acct#16f4eae3 | 2026-01 | other:sweep_trade_day | 1.68 | 1.6752 | 2.1165 | -0.4331 | 0.0 | -0.4331 | -0.0591 | -0.374 |
| acct#0f2d2c45 | 2024-01 | other:sweep_trade_day | -0.3 | -0.2815 | 0.0268 | -0.3087 | 0.0 | -0.3087 | 0.1526 | -0.4613 |
| acct#cce589ab | 2024-01 | other:sweep_trade_day | -0.3 | -0.2804 | 0.028 | -0.3088 | -0.0 | -0.3088 | 0.1523 | -0.4611 |
| acct#cce589ab | 2024-02 | sweep_balance | 4.32 | 4.2779 | 4.813 | -0.5119 | -0.0 | -0.5119 | -0.5119 | 0.0 |
| acct#cce589ab | 2024-04 | sweep_balance | -3.96 | -3.9239 | -4.0511 | 0.1325 | -0.0 | 0.1325 | 0.4555 | -0.323 |
| acct#cce589ab | 2024-08 | sweep_balance | 1.79 | 1.7636 | 1.9586 | -0.1914 | -0.0 | -0.1914 | -0.1914 | 0.0 |
| acct#cce589ab | 2024-10 | other:sweep_trade_day | -1.6 | -1.5618 | -1.4023 | -0.1619 | -0.0 | -0.1619 | 0.1846 | -0.3465 |
| acct#cce589ab | 2024-11 | sweep_balance | 5.25 | 5.213 | 5.7813 | -0.5387 | -0.0 | -0.5387 | -0.4897 | -0.0491 |
| acct#cce589ab | 2025-01 | sweep_balance | 2.52 | 2.481 | 3.0843 | -0.5869 | 0.0 | -0.5869 | -0.4428 | -0.1441 |
| acct#cce589ab | 2025-02 | sweep_balance | -1.55 | -1.5551 | -1.7189 | 0.1664 | 0.0 | 0.1664 | 0.1328 | 0.0336 |
| acct#cce589ab | 2025-04 | other:sweep_trade_day | -0.05 | -0.0504 | 0.2743 | -0.3243 | -0.0 | -0.3243 | 0.9143 | -1.2387 |
| acct#cce589ab | 2025-07 | other:sweep_trade_day | 1.24 | 1.2346 | 1.6808 | -0.4397 | -0.0 | -0.4397 | -0.0938 | -0.346 |
| acct#cce589ab | 2025-08 | sweep_balance | 2.52 | 2.4854 | 2.7275 | -0.2359 | 0.0 | -0.2359 | -0.2359 | 0.0 |
| acct#cce589ab | 2025-10 | other:sweep_trade_day | 1.44 | 1.4272 | 1.8756 | -0.4411 | -0.0 | -0.4411 | -0.1941 | -0.247 |
| acct#cce589ab | 2026-01 | other:sweep_trade_day | 1.76 | 1.738 | 2.218 | -0.4707 | -0.0 | -0.4707 | -0.1336 | -0.3371 |
| D49141608 | 2019-02 | sweep_balance | 0.04 | 0.0412 | 2.2299 | -2.1643 | 0.0 | -2.1643 | -2.1643 | 0.0 |
| D49141608 | 2019-03 | sweep_balance | 0.05 | 0.0457 | 2.4237 | -2.349 | -0.0 | -2.349 | -2.349 | 0.0 |
| D49141608 | 2019-04 | sweep_balance | 0.05 | 0.0443 | 2.2953 | -2.225 | -0.0 | -2.225 | -2.225 | 0.0 |
| D49141608 | 2019-05 | sweep_balance | 0.05 | 0.0457 | 2.3132 | -2.2412 | -0.0 | -2.2412 | -2.2412 | 0.0 |
| D49141608 | 2019-06 | sweep_balance | 0.05 | 0.0443 | 2.1931 | -2.1251 | 0.0 | -2.1251 | -2.1251 | 0.0 |
| D49141608 | 2019-07 | sweep_balance | 0.05 | 0.0456 | 2.2124 | -2.1426 | -0.0 | -2.1426 | -2.1426 | 0.0 |
| D49141608 | 2019-08 | sweep_balance | 0.04 | 0.0374 | 1.7749 | -1.7219 | -0.0 | -1.7219 | -1.7219 | 0.0 |
| D49141608 | 2019-09 | sweep_balance | 0.03 | 0.0315 | 1.4675 | -1.4253 | -0.0 | -1.4253 | -1.4253 | 0.0 |
| D49141714 | 2019-02 | sweep_balance | 0.04 | 0.0416 | 3.3111 | -3.2159 | 0.0 | -3.2159 | -3.2159 | 0.0 |
| acct#a011b5f7 | 2025-04 | other:sweep_trade_day | 0.41 | 0.4142 | 0.3581 | 0.0558 | 0.0 | 0.0558 | 0.0007 | 0.0552 |
| acct#a011b5f7 | 2025-10 | other:sweep_trade_day | 0.64 | 0.6038 | 1.0099 | -0.4029 | -0.0 | -0.4029 | -0.0094 | -0.3935 |
| acct#a011b5f7 | 2026-01 | other:sweep_trade_day | 1.56 | 1.5626 | 1.934 | -0.365 | -0.0 | -0.365 | -0.0084 | -0.3566 |
| acct#cf292cea | 2024-07 | other:sweep_trade_day | -7.76 | -7.7261 | -8.3764 | 0.7072 | 0.0 | 0.7072 | 0.0719 | 0.6354 |
| acct#cf292cea | 2024-08 | sweep_balance | 4.62 | 4.6488 | 4.6829 | -0.0326 | 0.0 | -0.0326 | -0.0326 | 0.0 |
| acct#cf292cea | 2024-10 | other:sweep_trade_day | -9.03 | -8.9903 | -9.7576 | 0.8467 | -0.0 | 0.8467 | 0.1384 | 0.7083 |
| acct#65b3b3ea | 2024-12 | other:sweep_trade_day | -8.02 | -7.9838 | -8.8079 | 0.8995 | 0.0 | 0.8995 | 0.0348 | 0.8647 |
| acct#65b3b3ea | 2025-03 | other:sweep_trade_day | 7.66 | 7.684 | 6.8268 | 0.7992 | -0.0 | 0.7992 | -0.0847 | 0.8839 |
| acct#65b3b3ea | 2025-04 | sweep_balance | -11.06 | -11.0556 | -11.1826 | 0.1429 | -0.0 | 0.1429 | 0.2903 | -0.1474 |
| acct#65b3b3ea | 2025-06 | other:sweep_trade_day | 6.23 | 6.2553 | 5.3767 | 0.8303 | 0.0 | 0.8303 | -0.0593 | 0.8896 |
| acct#65b3b3ea | 2025-07 | sweep_balance | 3.42 | 3.4191 | 3.5626 | -0.1386 | -0.0 | -0.1386 | -0.0984 | -0.0402 |
| acct#65b3b3ea | 2025-09 | other:sweep_trade_day | -0.47 | -0.4562 | -1.3469 | 0.8988 | 0.0 | 0.8988 | 0.0709 | 0.8279 |
| acct#65b3b3ea | 2025-10 | sweep_balance | 1.33 | 1.3311 | 1.4283 | -0.0959 | -0.0 | -0.0959 | -0.0768 | -0.0191 |
| acct#65b3b3ea | 2025-12 | other:sweep_trade_day | 4.56 | 4.5619 | 3.813 | 0.7188 | -0.0 | 0.7188 | -0.0863 | 0.8051 |
| acct#65b3b3ea | 2026-01 | sweep_balance | 16.79 | 16.7871 | 17.4998 | -0.6084 | 0.0 | -0.6084 | -0.5091 | -0.0993 |
| acct#65b3b3ea | 2026-03 | other:sweep_trade_day | 11.58 | 11.5754 | 11.2522 | 0.29 | -0.0 | 0.29 | -0.4285 | 0.7186 |
| acct#65b3b3ea | 2026-04 | sweep_balance | -8.79 | -8.7931 | -9.0353 | 0.2659 | -0.0 | 0.2659 | 0.3737 | -0.1078 |
| acct#ed5f47fe | 2026-01 | other:sweep_trade_day | 2.76 | 2.7564 | 3.0739 | -0.3086 | 0.0 | -0.3086 | -0.0121 | -0.2965 |

MOVER-CAUSES movers=147 sweep_balance=72 offsetting=0 other=75 sum_ok=True core_separate=16
