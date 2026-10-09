# DIFF trace (CB-aa-1)

## The denominator

- the census's `unexplained:` DIFF months: 512; traced to a named cause 70; untraced 442; class kinds 2
- every month is read once: the class counts below sum to 512 (months: 512) -- sum_ok=True
- re-derived daily returns reproduce the persisted computed return (tolerance 1e-06 pct points): 512 of 512 months; cash leg method_r26; sweep list v1; Year rows read: 4054 account-years; confirmed splits: 14; price spikes: 17 securities

## The rules, fixed before the counts

THE RULES (written here, committed before the run; every constant below is fixed in this file, not tuned to the run).
A month is D = computed - reported (pct points). Its DAY PANEL is the month's trading days plus the day before; V is the account value,
F the day's external flow, A the day's owed-elsewhere fee numerator (recovered from the persisted returns), so that
`1 + ret = (V - F + A) / V(previous day)`. S is the value of the non-cash holdings (rebuilt quantity x the day's close), C = V - S the cash line.
A CAUSE is a named, evidence-backed REPAIR: a change to V (or F) on the panel's days that the evidence in the rows or the closes
asks for, made WITHOUT looking at the reported return. A cause TRACES the month when, with the repair applied and the month re-chained
from the repaired day values, the remainder D' = repaired month - reported REACHES: |D'| <= max(TOLERANCE_PCT, REACH_FRACTION x |D|) and
|D'| <= REACH_CAP_PCT, with TOLERANCE_PCT 0.05 (the grade's own MATCH band), REACH_FRACTION 0.10 (the cause carries at least 90% of the
difference) and REACH_CAP_PCT 0.5 (a remainder of half a percentage point is never a trace, however large D). The cause with the smallest |D'| is the
month's class; ties go in the order of CLASSES below. No repair is searched for, solved, or sized from the reported return, and repairs are
combined only within one cause (one kind and sub-cause across the month's securities): a month where no ONE cause reaches is `untraced:`
(the detail lists what was found and what each cause leaves), never forced into a class.

CLASSES (the first two are facts of the account and of Commonwealth's own series; the rest are repairs):
  partial_month      the account's last day of data is inside the month before its last trading day (the account closed mid-month, so the
                     computed month covers fewer days than the reported month). A fact; no repair.
  reported_outlier   Commonwealth's reported month disagrees with its own year: the account-year has a Year row (Jan 1 .. Dec 31, TWR net)
                     and all 12 reported months, the 12 chained months differ from the Year row by more than YEAR_TOL_PCT (0.05), and the
                     month implied by the Year row and the other 11 reported months (prod(1 + m/100) - 1) is within TOLERANCE_PCT of the computed
                     month while the reported month is not. Never fixed here, only named.
  price:<cusip>      the close of a security is not on the basis of the rebuilt quantity. Three sub-causes, each summed over the month's securities
                     and named by the security whose repair alone moves the month most:
                       split  the security has a split (a QA row whose quantity ratio is within 0.5% of an integer k in 2..50 or of 1/k, same
                              ratio in every account that shows it, the close continuous across the day: within 0.7..1.4 of the day before,
                              so the stored history is split-adjusted); every close before the split day is as-adjusted, so the position
                              on those days is re-valued x k: V += q x close x (k - 1), q the rebuilt quantity;
                       distribution  a `dvr` row adds shares on a non-cash CUSIP: the day's step in the position's value
                              (q x close less the day before's q x close) is taken out of V from that day on, the shares and the close
                              having both stepped for the one distribution;
                       spike  a close that moves by at least 15% from the day before and is back within 3% of that day-before close
                              within 5 rows of the price series: the spike closes are replaced by the day-before close.
  holding:<cusip>    the rebuilt quantity is not what the account's rows support. Two sub-causes (a) step, (b) short:  (a) a share-moving row with no cash leg (QA, CAF, CAE, lica,
                     licar, LICASU, loca) steps the quantity on a day that is not a split: the quantity step valued at the day's close is
                     taken out of V from that day on; (b) the rebuilt quantity is below -1e-6 (a short the rows cannot support): the negative
                     position's value is taken out of V on those days.
  flow_value:<cusip> an in-kind flow row (li, LISU, trfi, TRFIR, trci, TRCISU, lo, LIX, LOX, trfo, trco) of a non-cash CUSIP with a non-zero
                     Quantity and a non-zero Amount whose |Amount| differs from |Quantity| x the day's close by more than 5% (the vendor Amount
                     is a cost, not a value): F is changed by the flow's direction x (|Quantity| x close - |Amount|) on that day.
  carried_level      the cash line C runs below -1.00 on a day of the panel (a negative cash level carried in): V is lifted by the lowest level on
                     every day of the panel, so the lowest day sits at zero.
`untraced:` is every other month; its detail also gives the computed month's price part (sum of each day's held-quantity x close move /
the day before's value) and non-price part, so a month carried by ordinary close moves says so. `classes` counts the distinct class kinds (the part before `:`) among the traced months plus ONE for the
`untraced:` label, if any month carries it.


## Classes

| class | months | median |D| | max |D| |
|---|---|---|---|
| price:02079K107 | 7 | 2.7005 | 32.1353 |
| price:02079K305 | 1 | 34.5617 | 34.5617 |
| price:023135106 | 17 | 2.5656 | 36.8512 |
| price:316067107 | 1 | 0.0732 | 0.0732 |
| price:316071109 | 4 | 9.5648 | 9.6355 |
| price:32008F606 | 1 | 1.0010 | 1.0010 |
| price:360802102 | 1 | 0.9314 | 0.9314 |
| price:464288877 | 1 | 0.0532 | 0.0532 |
| price:64110L106 | 25 | 3.6424 | 279.4650 |
| price:808524102 | 6 | 1.0304 | 147.4985 |
| price:88160R101 | 1 | 12.9292 | 12.9292 |
| price:921937835 | 4 | 0.1113 | 0.2916 |
| price:922908744 | 1 | 0.3785 | 0.3785 |
| untraced | 442 | 0.4114 | 20.0503 |

## Causes (kind and sub-cause)

| kind | sub-cause | months |
|---|---|---|
| untraced |  | 442 |
| price | split | 57 |
| price | distribution | 13 |

## One traced month per cause, on its day values (the largest |D| of the cause)

### price:64110L106 -- acct#f0b52456 2025-11

price:split: split x10 (2025-11-17). computed 276.7950, reported -2.67, D +279.4650; cause price:split: with the repair the month is -2.5150 against reported -2.6700 (remainder +0.1550); D was +279.4650

| date | value | flow | return % | repaired value | repaired flow | repaired return % |
|---|---|---|---|---|---|---|
| 2025-11-03 | 23679.20 | 0.00 | -0.9194 | 91004.71 | 0.00 | -1.4814 <- |
| 2025-11-04 | 23719.68 | 0.00 | 0.1710 | 90608.83 | 0.00 | -0.4350 <- |
| 2025-11-05 | 23962.88 | 0.00 | 1.0253 | 91188.63 | 0.00 | 0.6399 <- |
| 2025-11-06 | 23967.79 | 0.00 | 0.0205 | 91105.42 | 0.00 | -0.0913 <- |
| 2025-11-07 | 24244.83 | 0.00 | 1.1559 | 91788.82 | 0.00 | 0.7501 <- |
| 2025-11-10 | 24582.82 | 0.00 | 1.3941 | 93131.11 | 0.00 | 1.4624 <- |
| 2025-11-11 | 24796.01 | 0.00 | 0.8672 | 94346.14 | 0.00 | 1.3046 <- |
| 2025-11-12 | 24838.70 | 0.00 | 0.1722 | 95677.70 | 0.00 | 1.4114 <- |
| 2025-11-13 | 24617.18 | 0.00 | -0.8918 | 95256.06 | 0.00 | -0.4407 <- |
| 2025-11-14 | 24498.23 | 0.00 | -0.4832 | 92563.03 | 0.00 | -2.8271 <- |
| 2025-11-17 | 91843.69 | 0.00 | 274.8993 | 91843.69 | 0.00 | -0.7771 <- |
| 2025-11-18 | 94498.07 | 0.00 | 2.8901 | 94498.07 | 0.00 | 2.8901 |
| 2025-11-19 | 91513.26 | 0.00 | -3.1586 | 91513.26 | 0.00 | -3.1586 |
| 2025-11-20 | 88427.62 | 0.00 | -3.3718 | 88427.62 | 0.00 | -3.3718 |
| 2025-11-21 | 87580.35 | 0.00 | -0.9582 | 87580.35 | 0.00 | -0.9582 |
| 2025-11-24 | 89449.14 | 0.00 | 2.1338 | 89449.14 | 0.00 | 2.1338 |
| 2025-11-25 | 87674.46 | 0.00 | -1.9840 | 87674.46 | 0.00 | -1.9840 |
| 2025-11-26 | 88982.91 | 0.00 | 1.4924 | 88982.91 | 0.00 | 1.4924 |
| 2025-11-28 | 90049.97 | 0.00 | 1.1992 | 90049.97 | 0.00 | 1.1992 |

### price:316071109 -- acct#a011b5f7 2025-12

price:distribution: distribution 2025-12-05 step 2088.16. computed 11.2855, reported 1.65, D +9.6355; cause price:distribution: with the repair the month is 1.5408 against reported 1.6500 (remainder -0.1092); D was +9.6355

| date | value | flow | return % | repaired value | repaired flow | repaired return % |
|---|---|---|---|---|---|---|
| 2025-12-01 | 21283.90 | 0.00 | -0.6751 | 21283.90 | 0.00 | -0.6751 |
| 2025-12-02 | 21368.99 | 0.00 | 0.3998 | 21368.99 | 0.00 | 0.3998 |
| 2025-12-03 | 21334.95 | 0.00 | -0.1593 | 21334.95 | 0.00 | -0.1593 |
| 2025-12-04 | 21437.07 | 0.00 | 0.4786 | 21437.07 | 0.00 | 0.4786 |
| 2025-12-05 | 23525.22 | 0.00 | 9.7409 | 21437.07 | 0.00 | 0.0000 <- |
| 2025-12-08 | 23807.86 | 0.00 | 1.2014 | 21719.70 | 0.00 | 1.3184 <- |
| 2025-12-09 | 23720.14 | 0.00 | -0.3684 | 21631.99 | 0.00 | -0.4038 <- |
| 2025-12-10 | 23817.60 | 0.00 | 0.4109 | 21729.45 | 0.00 | 0.4505 <- |
| 2025-12-11 | 23866.33 | 0.00 | 0.2046 | 21778.18 | 0.00 | 0.2243 <- |
| 2025-12-12 | 23564.21 | 0.00 | -1.2659 | 21476.05 | 0.00 | -1.3873 <- |
| 2025-12-15 | 23544.72 | 0.00 | -0.0827 | 21456.56 | 0.00 | -0.0908 <- |
| 2025-12-16 | 23534.97 | 0.00 | -0.0414 | 21446.81 | 0.00 | -0.0454 <- |
| 2025-12-17 | 23242.59 | 0.00 | -1.2423 | 21154.43 | 0.00 | -1.3633 <- |
| 2025-12-18 | 23515.48 | 0.00 | 1.1741 | 21427.32 | 0.00 | 1.2900 <- |
| 2025-12-19 | 23729.89 | 0.00 | 0.9118 | 21641.73 | 0.00 | 1.0007 <- |
| 2025-12-22 | 23885.83 | 0.00 | 0.6571 | 21797.67 | 0.00 | 0.7205 <- |
| 2025-12-23 | 24041.76 | 0.00 | 0.6528 | 21953.60 | 0.00 | 0.7154 <- |
| 2025-12-24 | 24100.24 | 0.00 | 0.2432 | 22012.08 | 0.00 | 0.2664 <- |
| 2025-12-26 | 24100.24 | 0.00 | 0.0000 | 22012.08 | 0.00 | 0.0000 |
| 2025-12-29 | 24002.78 | 0.00 | -0.4044 | 21914.62 | 0.00 | -0.4428 <- |
| 2025-12-30 | 24002.78 | 0.00 | 0.0000 | 21914.62 | 0.00 | 0.0000 |
| 2025-12-31 | 23846.88 | 0.00 | -0.6495 | 21758.72 | 0.00 | -0.7114 <- |

## Traced months: 70

| account | month | class | computed | reported | D | remainder | events |
|---|---|---|---|---|---|---|---|
| acct#aaeb760c | 2021-12 | price:023135106 | 6.2452 | 5.52 | +0.7252 | +0.0242 | price:split: split x20 (2022-06-06) |
| acct#aaeb760c | 2022-04 | price:023135106 | -6.8315 | -7.82 | +0.9885 | +0.0610 | price:split: split x20 (2022-06-06) |
| acct#f6c79f45 | 2023-10 | price:316067107 | -9.0068 | -9.08 | +0.0732 | +0.0367 | price:distribution: distribution 2023-10-31 step 195.71 |
| acct#015306a0 | 2022-03 | price:360802102 | 4.1814 | 3.25 | +0.9314 | -0.0335 | price:distribution: distribution 2022-03-15 step 130.88, distribution 2022-03-17 step 442.48 |
| acct#fa488a0b | 2020-10 | price:921937835 | -0.6120 | -0.74 | +0.1280 | +0.0041 | price:distribution: distribution 2020-10-06 step 10.27 |
| acct#fa488a0b | 2021-02 | price:921937835 | 3.1040 | 3.01 | +0.0940 | +0.0283 | price:distribution: distribution 2021-02-04 step 6.11 |
| acct#fa488a0b | 2021-10 | price:921937835 | 2.6146 | 2.52 | +0.0946 | +0.0284 | price:distribution: distribution 2021-10-06 step 6.74 |
| acct#fa488a0b | 2022-01 | price:464288877 | -1.3432 | -1.29 | -0.0532 | -0.0483 | price:distribution: distribution 2022-01-05 step -0.52 |
| acct#fa488a0b | 2022-03 | price:921937835 | 0.4016 | 0.11 | +0.2916 | +0.0017 | price:distribution: distribution 2022-03-04 step 16.90, distribution 2022-03-24 step 4.25, distribution 2022-03-28 step -0.71, distribution 2022-03-28 step 9.59 |
| acct#fa488a0b | 2024-03 | price:922908744 | 4.0485 | 3.67 | +0.3785 | -0.0133 | price:distribution: distribution 2024-03-06 step 15.09, distribution 2024-03-20 step 4.39, distribution 2024-03-26 step 9.36, distribution 2024-03-26 step 16.03 |
| acct#2d4385bf | 2020-11 | price:023135106 | 8.4405 | 7.69 | +0.7505 | -0.0313 | price:split: split x20 (2022-07-18), split x20 (2022-06-06) |
| acct#2d4385bf | 2020-12 | price:02079K107 | 4.1553 | 3.36 | +0.7953 | +0.0534 | price:split: split x20 (2022-07-18), split x20 (2022-06-06) |
| acct#2d4385bf | 2021-01 | price:023135106 | 2.8523 | 2.19 | +0.6623 | +0.0264 | price:split: split x20 (2022-07-18), split x20 (2022-06-06) |
| acct#2d4385bf | 2021-03 | price:023135106 | 11.1771 | 6.84 | +4.3371 | +0.0900 | price:split: split x20 (2022-07-18), split x20 (2022-06-06) |
| acct#2d4385bf | 2021-04 | price:023135106 | -4.9002 | 2.26 | -7.1602 | -0.0530 | price:split: split x20 (2022-07-18), split x20 (2022-06-06) |
| acct#2d4385bf | 2021-05 | price:023135106 | 8.0908 | 2.89 | +5.2008 | +0.0308 | price:split: split x20 (2022-07-18), split x20 (2022-06-06) |
| acct#2d4385bf | 2021-06 | price:023135106 | -8.2665 | -2.82 | -5.4465 | -0.0142 | price:split: split x20 (2022-07-18), split x20 (2022-06-06) |
| acct#2d4385bf | 2021-07 | price:02079K107 | -1.8888 | -0.43 | -1.4588 | -0.0464 | price:split: split x20 (2022-07-18), split x20 (2022-06-06) |
| acct#2d4385bf | 2021-08 | price:02079K107 | -0.3905 | 2.31 | -2.7005 | -0.0207 | price:split: split x20 (2022-07-18), split x20 (2022-06-06) |
| acct#2d4385bf | 2021-09 | price:02079K107 | 0.2921 | -2.95 | +3.2421 | +0.0808 | price:split: split x20 (2022-07-18), split x20 (2022-06-06) |
| acct#2d4385bf | 2021-10 | price:02079K107 | -2.0851 | 1.69 | -3.7751 | -0.0653 | price:split: split x20 (2022-07-18), split x20 (2022-06-06) |
| acct#2d4385bf | 2021-11 | price:023135106 | -5.3156 | -2.75 | -2.5656 | -0.0192 | price:split: split x20 (2022-07-18), split x20 (2022-06-06) |
| acct#2d4385bf | 2021-12 | price:023135106 | 2.3120 | 0.27 | +2.0420 | +0.0125 | price:split: split x20 (2022-07-18), split x20 (2022-06-06) |
| acct#2d4385bf | 2022-01 | price:023135106 | -7.1236 | -7.68 | +0.5564 | -0.0254 | price:split: split x20 (2022-07-18), split x20 (2022-06-06) |
| acct#2d4385bf | 2022-04 | price:023135106 | -1.6768 | -10.37 | +8.6932 | +0.0007 | price:split: split x20 (2022-07-18), split x20 (2022-06-06) |
| acct#2d4385bf | 2022-05 | price:02079K107 | -3.2084 | -2.73 | -0.4784 | -0.0357 | price:split: split x20 (2022-07-18), split x20 (2022-06-06) |
| acct#2d4385bf | 2022-06 | price:023135106 | 8.6093 | -16.23 | +24.8393 | -0.0218 | price:split: split x20 (2022-07-18), split x20 (2022-06-06) |
| acct#2d4385bf | 2022-07 | price:02079K107 | 44.4153 | 12.28 | +32.1353 | +0.0451 | price:split: split x20 (2022-07-18) |
| acct#afda5d61 | 2023-12 | price:32008F606 | 1.8010 | 0.80 | +1.0010 | -0.0040 | price:distribution: distribution 2023-12-05 step 889.83 |
| acct#f0b52456 | 2022-12 | price:64110L106 | -6.0093 | -5.21 | -0.7993 | +0.0685 | price:split: split x10 (2025-11-17) |
| acct#f0b52456 | 2023-02 | price:64110L106 | 2.3206 | -1.63 | +3.9506 | -0.1963 | price:split: split x10 (2025-11-17) |
| acct#f0b52456 | 2023-03 | price:64110L106 | -5.9594 | -1.84 | -4.1194 | +0.3801 | price:split: split x10 (2025-11-17) |
| acct#f0b52456 | 2023-04 | price:64110L106 | 3.1643 | 0.28 | +2.8843 | +0.0421 | price:split: split x10 (2025-11-17) |
| acct#f0b52456 | 2023-06 | price:64110L106 | 6.2433 | 9.22 | -2.9767 | +0.2020 | price:split: split x10 (2025-11-17) |
| acct#f0b52456 | 2023-07 | price:64110L106 | 3.5785 | 1.29 | +2.2885 | -0.1506 | price:split: split x10 (2025-11-17) |
| acct#f0b52456 | 2023-09 | price:64110L106 | 0.9701 | -7.08 | +8.0501 | -0.4313 | price:split: split x10 (2025-11-17) |
| acct#f0b52456 | 2023-10 | price:64110L106 | -3.8756 | 3.09 | -6.9656 | +0.4461 | price:split: split x10 (2025-11-17) |
| acct#f0b52456 | 2024-01 | price:64110L106 | 1.3747 | 10.14 | -8.7653 | +0.4015 | price:split: split x10 (2025-11-17) |
| acct#f0b52456 | 2024-03 | price:64110L106 | 6.3224 | 2.68 | +3.6424 | -0.1230 | price:split: split x10 (2025-11-17) |
| acct#f0b52456 | 2024-04 | price:64110L106 | -1.1991 | -6.38 | +5.1809 | -0.2006 | price:split: split x10 (2025-11-17) |
| acct#f0b52456 | 2024-06 | price:64110L106 | -0.4463 | 3.17 | -3.6163 | +0.1575 | price:split: split x10 (2025-11-17) |
| acct#f0b52456 | 2024-07 | price:64110L106 | -2.8826 | -5.56 | +2.6774 | -0.0602 | price:split: split x10 (2025-11-17) |
| acct#f0b52456 | 2024-09 | price:64110L106 | -3.0145 | -0.25 | -2.7645 | +0.1122 | price:split: split x10 (2025-11-17) |
| acct#f0b52456 | 2024-10 | price:64110L106 | -1.2453 | 4.10 | -5.3453 | +0.1651 | price:split: split x10 (2025-11-17) |
| acct#f0b52456 | 2024-11 | price:64110L106 | 7.2106 | 14.05 | -6.8394 | +0.4109 | price:split: split x10 (2025-11-17) |
| acct#f0b52456 | 2025-01 | price:64110L106 | 5.7396 | 8.52 | -2.7804 | +0.0498 | price:split: split x10 (2025-11-17) |
| acct#f0b52456 | 2025-02 | price:64110L106 | 3.6074 | 1.08 | +2.5274 | +0.1370 | price:split: split x10 (2025-11-17) |
| acct#f0b52456 | 2025-03 | price:64110L106 | -1.1056 | -3.86 | +2.7544 | -0.0395 | price:split: split x10 (2025-11-17) |
| acct#f0b52456 | 2025-04 | price:64110L106 | -4.0307 | 14.18 | -18.2107 | +0.2997 | price:split: split x10 (2025-11-17) |
| acct#f0b52456 | 2025-06 | price:64110L106 | 7.1450 | 10.03 | -2.8850 | +0.0348 | price:split: split x10 (2025-11-17) |
| acct#f0b52456 | 2025-07 | price:64110L106 | -2.9401 | -11.04 | +8.0999 | -0.0578 | price:split: split x10 (2025-11-17) |
| acct#f0b52456 | 2025-08 | price:64110L106 | 7.3390 | 4.81 | +2.5290 | +0.1599 | price:split: split x10 (2025-11-17) |
| acct#f0b52456 | 2025-10 | price:64110L106 | -1.7346 | -5.44 | +3.7054 | -0.0071 | price:split: split x10 (2025-11-17) |
| acct#f0b52456 | 2025-11 | price:64110L106 | 276.7950 | -2.67 | +279.4650 | +0.1550 | price:split: split x10 (2025-11-17) |
| acct#79d02c2c | 2023-01 | price:808524102 | 4.4677 | 5.50 | -1.0323 | +0.0164 | price:split: split x3 (2024-10-11), split x2 (2024-10-11) |
| acct#79d02c2c | 2023-08 | price:808524102 | -1.1940 | -1.55 | +0.3560 | +0.0440 | price:split: split x3 (2024-10-11), split x2 (2024-10-11) |
| acct#79d02c2c | 2024-10 | price:808524102 | 145.4343 | -1.13 | +146.5643 | +0.0629 | price:split: split x3 (2024-10-11), split x2 (2024-10-11) |
| acct#4a890dd1 | 2023-01 | price:808524102 | 4.5015 | 5.53 | -1.0285 | +0.0134 | price:split: split x3 (2024-10-11), split x2 (2024-10-11) |
| acct#4a890dd1 | 2023-08 | price:808524102 | -1.2084 | -1.56 | +0.3516 | +0.0439 | price:split: split x3 (2024-10-11), split x2 (2024-10-11) |
| acct#4a890dd1 | 2024-10 | price:808524102 | 146.3785 | -1.12 | +147.4985 | +0.0584 | price:split: split x3 (2024-10-11), split x2 (2024-10-11) |
| acct#c753e42f | 2021-10 | price:88160R101 | 7.1908 | 20.12 | -12.9292 | -0.2089 | price:split: split x3 (2024-10-11), split x3 (2022-08-25) |
| acct#dba683c4 | 2022-04 | price:023135106 | -14.7900 | -18.71 | +3.9200 | +0.0078 | price:split: split x20 (2022-07-18), split x20 (2022-06-06) |
| acct#dba683c4 | 2022-06 | price:023135106 | 30.9912 | -5.86 | +36.8512 | +0.0043 | price:split: split x20 (2022-07-18), split x20 (2022-06-06) |
| acct#dba683c4 | 2022-07 | price:02079K305 | 45.2117 | 10.65 | +34.5617 | -0.0399 | price:split: split x20 (2022-07-18) |
| acct#eeab73e8 | 2022-04 | price:023135106 | -0.7690 | -2.58 | +1.8110 | -0.1525 | price:split: split x20 (2022-06-06) |
| acct#eeab73e8 | 2022-05 | price:023135106 | -2.3115 | -2.37 | +0.0585 | -0.0061 | price:split: split x20 (2022-06-06) |
| acct#a011b5f7 | 2025-12 | price:316071109 | 11.2855 | 1.65 | +9.6355 | -0.1092 | price:distribution: distribution 2025-12-05 step 2088.16 |
| acct#7f62f16f | 2025-12 | price:316071109 | 11.2247 | 1.64 | +9.5847 | -0.1074 | price:distribution: distribution 2025-12-05 step 1506.13 |
| acct#8148a2c4 | 2025-12 | price:316071109 | 11.1850 | 1.64 | +9.5450 | -0.1128 | price:distribution: distribution 2025-12-05 step 911.96 |
| acct#cce36d1f | 2025-12 | price:316071109 | 11.0976 | 1.62 | +9.4776 | -0.1046 | price:distribution: distribution 2025-12-05 step 220.66 |

## Untraced months: 442

`untraced:no single cause reaches the month (checked: partial_month, reported_outlier, price, holding, flow_value, carried_level)`

| account | month | computed | reported | D | events found | detail |
|---|---|---|---|---|---|---|
| acct#aaeb760c | 2021-10 | 5.3811 | 5.51 | -0.1289 | price:split: split x20 (2022-06-06) | causes found: price:split; best single cause price:split leaves -0.3068; all causes together leave -0.3068; computed month = price part 5.3810 + non-price part 0.0001 |
| acct#aaeb760c | 2021-11 | 5.8491 | 5.11 | +0.7391 | price:split: split x20 (2022-06-06) | causes found: price:split; best single cause price:split leaves +0.6206; all causes together leave +0.6206; computed month = price part 5.6973 + non-price part 0.1439 |
| acct#aaeb760c | 2022-01 | 0.2712 | 0.02 | +0.2512 | price:split: split x20 (2022-06-06) | causes found: price:split; best single cause price:split leaves -0.3454; all causes together leave -0.3454; computed month = price part 0.2494 + non-price part 0.0218 |
| acct#aaeb760c | 2022-02 | -3.7862 | -3.25 | -0.5362 | price:split: split x20 (2022-06-06) | causes found: price:split; best single cause price:split leaves -0.2079; all causes together leave -0.2079; computed month = price part -3.8984 + non-price part 0.1154 |
| acct#aaeb760c | 2022-05 | -0.6305 | -0.33 | -0.3005 | price:split: split x20 (2022-06-06) | causes found: price:split; best single cause price:split leaves -0.4204; all causes together leave -0.4204; computed month = price part -0.8471 + non-price part 0.2196 |
| acct#aaeb760c | 2022-06 | -4.1056 | -9.59 | +5.4844 | price:split: split x20 (2022-06-06) | causes found: price:split; best single cause price:split leaves +1.2501; all causes together leave +1.2501; computed month = price part -8.6261 + non-price part 4.9826 |
| acct#aaeb760c | 2022-07 | 13.4098 | 13.71 | -0.3002 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 13.4082 + non-price part 0.0014 |
| acct#aaeb760c | 2022-09 | -8.5504 | -8.92 | +0.3696 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part -8.6637 + non-price part 0.1246 |
| acct#aaeb760c | 2022-10 | 8.9539 | 10.27 | -1.3161 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 8.9511 + non-price part 0.0026 |
| acct#aaeb760c | 2022-12 | -8.9061 | -9.12 | +0.2139 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part -9.0200 + non-price part 0.1266 |
| acct#aaeb760c | 2023-01 | 8.2416 | 8.44 | -0.1984 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 8.2100 + non-price part 0.0298 |
| acct#aaeb760c | 2023-02 | 0.4500 | 0.15 | +0.3000 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 0.3247 + non-price part 0.1241 |
| acct#aaeb760c | 2023-03 | 8.2523 | 7.85 | +0.4023 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 8.1038 + non-price part 0.1373 |
| acct#aaeb760c | 2023-04 | 0.9890 | 1.22 | -0.2310 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 1.0406 + non-price part -0.0507 |
| acct#aaeb760c | 2023-05 | 1.3731 | 0.82 | +0.5531 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 1.2311 + non-price part 0.1412 |
| acct#aaeb760c | 2023-07 | 3.1769 | 3.45 | -0.2731 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 3.2245 + non-price part -0.0458 |
| acct#aaeb760c | 2023-08 | -2.0449 | -2.35 | +0.3051 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part -2.1763 + non-price part 0.1334 |
| acct#aaeb760c | 2023-10 | -0.3183 | -0.16 | -0.1583 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part -0.2680 + non-price part -0.0511 |
| acct#aaeb760c | 2023-11 | 7.5042 | 7.05 | +0.4542 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 7.3079 + non-price part 0.1833 |
| acct#aaeb760c | 2024-01 | -0.7836 | -0.89 | +0.1064 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part -0.7557 + non-price part -0.0292 |
| acct#aaeb760c | 2024-03 | 1.3408 | 1.66 | -0.3192 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 1.1581 + non-price part 0.1809 |
| acct#aaeb760c | 2024-04 | -3.2864 | -3.62 | +0.3336 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part -3.2677 + non-price part -0.0195 |
| acct#aaeb760c | 2024-06 | 6.1492 | 5.97 | +0.1792 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 6.0170 + non-price part 0.1236 |
| acct#aaeb760c | 2024-07 | 3.6448 | 3.58 | +0.0648 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 3.6992 + non-price part -0.0526 |
| acct#aaeb760c | 2024-09 | 0.7007 | 0.46 | +0.2407 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 0.5807 + non-price part 0.1193 |
| acct#aaeb760c | 2024-10 | -2.9578 | -2.89 | -0.0678 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part -2.9075 + non-price part -0.0525 |
| acct#aaeb760c | 2024-11 | 7.0417 | 6.86 | +0.1817 | holding:step: quantity step 2024-11-22 +255, quantity step 2024-11-22 -1000 | causes found: holding:step; best single cause holding:step leaves +0.1804; all causes together leave +0.1804; computed month = price part 6.9144 + non-price part 0.1193 |
| acct#aaeb760c | 2024-12 | 1.6690 | 1.55 | +0.1190 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 1.5758 + non-price part 0.0916 |
| acct#aaeb760c | 2025-02 | -0.2092 | -0.33 | +0.1208 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part -0.2847 + non-price part 0.0765 |
| acct#aaeb760c | 2025-08 | 8.1059 | 7.91 | +0.1959 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 8.0151 + non-price part 0.0840 |
| acct#aaeb760c | 2025-11 | 1.5868 | 1.43 | +0.1568 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 1.5114 + non-price part 0.0735 |
| acct#aaeb760c | 2026-02 | 1.4032 | 1.27 | +0.1332 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 1.3440 + non-price part 0.0560 |
| acct#48f4ec93 | 2020-08 | 2.2237 | 2.37 | -0.1463 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 2.2233 + non-price part 0.0003 |
| acct#48f4ec93 | 2020-09 | -0.7862 | -1.29 | +0.5038 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part -1.2006 + non-price part 0.4215 |
| acct#48f4ec93 | 2020-10 | -0.9706 | -1.03 | +0.0594 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part -0.9709 + non-price part 0.0004 |
| acct#48f4ec93 | 2020-11 | 6.7546 | 7.17 | -0.4154 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 6.7543 + non-price part 0.0003 |
| acct#48f4ec93 | 2021-02 | 2.8221 | 2.97 | -0.1479 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 2.8218 + non-price part 0.0003 |
| acct#48f4ec93 | 2021-04 | 2.0288 | 2.13 | -0.1012 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 2.0285 + non-price part 0.0003 |
| acct#3ea38af4 | 2022-07 | 6.8138 | 7.21 | -0.3962 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 6.8353 + non-price part -0.0197 |
| acct#3ea38af4 | 2022-08 | -0.3457 | -0.87 | +0.5243 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part -0.3593 + non-price part 0.0136 |
| acct#f6c79f45 | 2020-08 | -2.8768 | -4.66 | +1.7832 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part -2.8769 + non-price part 0.0001 |
| acct#f6c79f45 | 2020-10 | -4.2483 | -4.38 | +0.1317 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part -4.2484 + non-price part 0.0001 |
| acct#f6c79f45 | 2020-11 | 16.6837 | 14.77 | +1.9137 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 16.6836 + non-price part 0.0001 |
| acct#f6c79f45 | 2021-01 | 7.5317 | 7.74 | -0.2083 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 7.5316 + non-price part 0.0001 |
| acct#f6c79f45 | 2021-02 | 20.2254 | 18.91 | +1.3154 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 20.2253 + non-price part 0.0001 |
| acct#f6c79f45 | 2021-05 | 3.0456 | 1.77 | +1.2756 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 3.0455 + non-price part 0.0001 |
| acct#f6c79f45 | 2021-07 | -7.6750 | -7.83 | +0.1550 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part -7.6751 + non-price part 0.0001 |
| acct#f6c79f45 | 2021-08 | -3.3565 | -4.70 | +1.3435 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part -3.3566 + non-price part 0.0001 |
| acct#f6c79f45 | 2021-10 | 8.2574 | 8.43 | -0.1726 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 8.2573 + non-price part 0.0001 |
| acct#f6c79f45 | 2021-11 | -5.1650 | -6.37 | +1.2050 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part -5.1651 + non-price part 0.0001 |
| acct#f6c79f45 | 2022-01 | 20.6056 | 21.03 | -0.4244 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 20.6054 + non-price part 0.0001 |
| acct#f6c79f45 | 2022-02 | 3.8513 | 2.89 | +0.9613 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 3.8512 + non-price part 0.0001 |
| acct#f6c79f45 | 2022-05 | 12.1420 | 11.30 | +0.8420 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 12.1419 + non-price part 0.0001 |
| acct#f6c79f45 | 2022-07 | 9.9373 | 10.24 | -0.3027 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 9.9321 + non-price part 0.0049 |
| acct#f6c79f45 | 2022-08 | -0.3223 | -1.10 | +0.7777 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part -0.3291 + non-price part 0.0068 |
| acct#f6c79f45 | 2022-10 | 20.2520 | 20.82 | -0.5680 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 20.2436 + non-price part 0.0070 |
| acct#f6c79f45 | 2022-11 | 1.0289 | 0.40 | +0.6289 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 1.0218 + non-price part 0.0071 |
| acct#f6c79f45 | 2023-01 | 4.3452 | 4.42 | -0.0748 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 4.3384 + non-price part 0.0067 |
| acct#f6c79f45 | 2023-02 | -3.8199 | -4.51 | +0.6901 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part -3.8258 + non-price part 0.0062 |
| acct#f6c79f45 | 2023-05 | -10.8115 | -11.63 | +0.8185 | price:distribution: distribution 2023-05-31 step 301.53 | causes found: price:distribution; best single cause price:distribution leaves +0.7657; all causes together leave +0.7657; computed month = price part -10.8660 + non-price part 0.0602 |
| acct#f6c79f45 | 2023-11 | -1.7998 | -2.62 | +0.8202 | price:distribution: distribution 2023-11-30 step 189.59 | causes found: price:distribution; best single cause price:distribution leaves +0.7813; all causes together leave +0.7813; computed month = price part -1.8392 + non-price part 0.0403 |
| acct#f6c79f45 | 2024-02 | 2.3500 | 1.52 | +0.8300 | price:distribution: distribution 2024-02-29 step 184.26 | causes found: price:distribution; best single cause price:distribution leaves +0.7920; all causes together leave +0.7920; computed month = price part 2.3109 + non-price part 0.0383 |
| acct#f6c79f45 | 2024-05 | -0.0060 | -0.73 | +0.7240 | price:distribution: distribution 2024-05-31 step 200.51 | causes found: price:distribution; best single cause price:distribution leaves +0.6880; all causes together leave +0.6880; computed month = price part -0.0434 + non-price part 0.0384 |
| acct#f6c79f45 | 2024-08 | 0.2710 | -0.44 | +0.7110 | price:distribution: distribution 2024-08-30 step 267.62 | causes found: price:distribution; best single cause price:distribution leaves +0.6639; all causes together leave +0.6639; computed month = price part 0.2237 + non-price part 0.0471 |
| acct#f6c79f45 | 2024-11 | 1.6549 | 0.93 | +0.7249 | price:distribution: distribution 2024-11-29 step 228.35 | causes found: price:distribution; best single cause price:distribution leaves +0.6848; all causes together leave +0.6848; computed month = price part 1.6141 + non-price part 0.0402 |
| acct#f6c79f45 | 2025-02 | 4.9917 | 4.09 | +0.9017 | price:distribution: distribution 2025-02-28 step 31.95 | causes found: price:distribution; best single cause price:distribution leaves +0.8950; all causes together leave +0.8950; computed month = price part 4.9847 + non-price part 0.0067 |
| acct#f6c79f45 | 2025-05 | -1.8866 | -2.66 | +0.7734 | price:distribution: distribution 2025-05-30 step 222.93 | causes found: price:distribution; best single cause price:distribution leaves +0.7267; all causes together leave +0.7267; computed month = price part -1.9334 + non-price part 0.0476 |
| acct#f6c79f45 | 2025-08 | 3.3025 | 2.36 | +0.9425 | price:distribution: distribution 2025-08-29 step 11.99 | causes found: price:distribution; best single cause price:distribution leaves +0.9398; all causes together leave +0.9398; computed month = price part 3.2998 + non-price part 0.0027 |
| acct#f6c79f45 | 2025-11 | 2.2163 | 1.34 | +0.8763 | price:distribution: distribution 2025-11-28 step 10.69 | causes found: price:distribution; best single cause price:distribution leaves +0.8739; all causes together leave +0.8739; computed month = price part 2.2138 + non-price part 0.0024 |
| acct#f6c79f45 | 2026-02 | 8.3970 | 7.69 | +0.7070 | price:distribution: distribution 2026-02-27 step 9.22 | causes found: price:distribution; best single cause price:distribution leaves +0.7054; all causes together leave +0.7054; computed month = price part 8.3953 + non-price part 0.0016 |
| acct#03836058 | 2020-08 | -0.0260 | -1.16 | +1.1340 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part -0.3700 + non-price part 0.3494 |
| acct#03836058 | 2020-10 | 0.2313 | 0.04 | +0.1913 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 0.2312 + non-price part 0.0001 |
| acct#03836058 | 2020-11 | 15.2233 | 14.48 | +0.7433 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 14.8267 + non-price part 0.3393 |
| acct#03836058 | 2021-01 | 1.7325 | 1.57 | +0.1625 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 1.7325 + non-price part 0.0001 |
| acct#03836058 | 2021-02 | 8.1137 | 7.18 | +0.9337 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 7.7729 + non-price part 0.3132 |
| acct#03836058 | 2021-04 | 0.8273 | 0.70 | +0.1273 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 0.8272 + non-price part 0.0001 |
| acct#03836058 | 2021-05 | 1.6822 | 0.79 | +0.8922 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 1.4041 + non-price part 0.2737 |
| acct#03836058 | 2021-07 | -0.3273 | -0.65 | +0.3227 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part -0.3274 + non-price part 0.0001 |
| acct#03836058 | 2021-08 | -1.5951 | -2.59 | +0.9949 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part -1.8610 + non-price part 0.2704 |
| acct#03836058 | 2021-11 | -1.4772 | -2.48 | +1.0028 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part -1.7425 + non-price part 0.2703 |
| acct#03836058 | 2022-01 | 7.7296 | 7.64 | +0.0896 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 7.7296 + non-price part 0.0001 |
| acct#03836058 | 2022-02 | 6.1230 | 5.23 | +0.8930 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 5.8665 + non-price part 0.2459 |
| acct#03836058 | 2022-04 | -1.1928 | -1.41 | +0.2172 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part -1.1931 + non-price part 0.0003 |
| acct#03836058 | 2022-08 | -2.5976 | -3.14 | +0.5424 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part -2.7986 + non-price part 0.2085 |
| acct#03836058 | 2022-09 | -10.5582 | -11.17 | +0.6118 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part -11.0427 + non-price part 0.5448 |
| acct#03836058 | 2023-02 | -5.2225 | -5.69 | +0.4675 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part -5.4221 + non-price part 0.2114 |
| acct#03836058 | 2023-05 | -8.3087 | -8.87 | +0.5613 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part -8.5234 + non-price part 0.2349 |
| acct#03836058 | 2023-08 | -3.4500 | -4.03 | +0.5800 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part -3.6661 + non-price part 0.2236 |
| acct#03836058 | 2023-11 | 4.2308 | 3.65 | +0.5808 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 3.9634 + non-price part 0.2650 |
| acct#03836058 | 2024-01 | -3.2631 | -3.92 | +0.6569 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part -3.6792 + non-price part 0.4332 |
| acct#03836058 | 2024-02 | 2.2463 | 1.68 | +0.5663 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 1.9959 + non-price part 0.2473 |
| acct#03836058 | 2024-05 | 3.2944 | 2.70 | +0.5944 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 3.0538 + non-price part 0.2343 |
| acct#03836058 | 2024-08 | -3.7502 | -4.41 | +0.6598 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part -3.9844 + non-price part 0.2451 |
| acct#03836058 | 2024-09 | 3.1416 | 0.38 | +2.7616 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 0.3066 + non-price part 2.8214 |
| acct#03836058 | 2025-01 | 2.9157 | 2.35 | +0.5657 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 2.9126 + non-price part 0.0030 |
| acct#03836058 | 2025-02 | 6.7017 | 6.04 | +0.6617 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 6.0879 + non-price part 0.5813 |
| acct#03836058 | 2025-04 | -8.1991 | -8.74 | +0.5409 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part -8.2007 + non-price part 0.0017 |
| acct#03836058 | 2025-05 | 0.7259 | 0.09 | +0.6359 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 0.1479 + non-price part 0.5749 |
| acct#03836058 | 2025-07 | 3.0052 | 2.45 | +0.5552 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 3.0032 + non-price part 0.0019 |
| acct#03836058 | 2025-08 | 4.4121 | 3.79 | +0.6221 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 3.8496 + non-price part 0.5411 |
| acct#03836058 | 2026-01 | 9.4910 | 8.89 | +0.6010 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 9.4908 + non-price part 0.0002 |
| acct#03836058 | 2026-02 | 8.9025 | 8.27 | +0.6325 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 8.3418 + non-price part 0.5177 |
| acct#eea1157e | 2020-08 | -0.8672 | -1.64 | +0.7728 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part -0.8678 + non-price part 0.0006 |
| acct#eea1157e | 2020-10 | -1.1629 | -1.38 | +0.2171 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part -1.1636 + non-price part 0.0006 |
| acct#eea1157e | 2020-11 | 4.4273 | 4.52 | -0.0927 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 4.4267 + non-price part 0.0006 |
| acct#eea1157e | 2021-01 | 2.3779 | 2.76 | -0.3821 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 2.3773 + non-price part 0.0006 |
| acct#eea1157e | 2021-02 | 6.7059 | 7.06 | -0.3541 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 6.7054 + non-price part 0.0005 |
| acct#eea1157e | 2021-04 | 0.8495 | 0.96 | -0.1105 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 0.8490 + non-price part 0.0005 |
| acct#eea1157e | 2021-05 | 1.1828 | 0.76 | +0.4228 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 1.1823 + non-price part 0.0005 |
| acct#eea1157e | 2021-07 | -3.1883 | -3.55 | +0.3617 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part -3.1888 + non-price part 0.0005 |
| acct#eea1157e | 2021-08 | -1.3294 | -2.04 | +0.7106 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part -1.3300 + non-price part 0.0005 |
| acct#eea1157e | 2021-10 | 3.3652 | 3.73 | -0.3648 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 3.3646 + non-price part 0.0005 |
| acct#eea1157e | 2021-11 | -2.2036 | -2.94 | +0.7364 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part -2.2041 + non-price part 0.0005 |
| acct#eea1157e | 2022-01 | 8.6954 | 9.54 | -0.8446 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 8.6949 + non-price part 0.0005 |
| acct#eea1157e | 2022-02 | 1.8035 | 1.45 | +0.3535 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 1.8031 + non-price part 0.0004 |
| acct#eea1157e | 2022-04 | 1.3925 | 1.50 | -0.1075 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 1.3920 + non-price part 0.0004 |
| acct#eea1157e | 2022-05 | 6.0563 | 5.98 | +0.0763 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 6.0559 + non-price part 0.0004 |
| acct#eea1157e | 2022-07 | 5.8253 | 6.24 | -0.4147 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 5.8182 + non-price part 0.0068 |
| acct#eea1157e | 2022-08 | -0.1888 | -0.69 | +0.5012 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part -0.2003 + non-price part 0.0114 |
| acct#eea1157e | 2022-10 | 12.0206 | 12.81 | -0.7894 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 12.0065 + non-price part 0.0126 |
| acct#eea1157e | 2022-11 | 0.6633 | 0.27 | +0.3933 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 0.6505 + non-price part 0.0127 |
| acct#eea1157e | 2023-01 | 2.6287 | 2.77 | -0.1413 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 2.6077 + non-price part 0.0207 |
| acct#eea1157e | 2023-02 | -2.3196 | -2.84 | +0.5204 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part -2.3381 + non-price part 0.0189 |
| acct#eea1157e | 2023-04 | 3.9492 | 4.15 | -0.2008 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 3.9721 + non-price part -0.0217 |
| acct#eea1157e | 2023-05 | -6.6917 | -7.43 | +0.7383 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part -6.7222 + non-price part 0.0324 |
| acct#eea1157e | 2023-08 | 2.2801 | 1.94 | +0.3401 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 2.2480 + non-price part 0.0314 |
| acct#eea1157e | 2023-10 | -5.1927 | -5.40 | +0.2073 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part -5.1713 + non-price part -0.0221 |
| acct#eea1157e | 2023-11 | -0.9780 | -1.48 | +0.5020 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part -1.0093 + non-price part 0.0316 |
| acct#eea1157e | 2024-01 | 1.3330 | 1.39 | -0.0570 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 1.3522 + non-price part -0.0188 |
| acct#eea1157e | 2024-02 | 1.2945 | 0.87 | +0.4245 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 1.2639 + non-price part 0.0303 |
| acct#eea1157e | 2024-05 | 0.0052 | -0.43 | +0.4352 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part -0.0253 + non-price part 0.0310 |
| acct#eea1157e | 2024-08 | 0.1617 | -0.26 | +0.4217 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 0.1312 + non-price part 0.0304 |
| acct#eea1157e | 2024-11 | 0.9781 | 0.56 | +0.4181 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 0.9483 + non-price part 0.0296 |
| acct#eea1157e | 2025-02 | 2.5471 | 2.13 | +0.4171 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 2.5340 + non-price part 0.0129 |
| acct#eea1157e | 2025-04 | -5.8468 | -5.94 | +0.0932 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part -5.8057 + non-price part -0.0450 |
| acct#eea1157e | 2025-05 | -1.0962 | -1.56 | +0.4638 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part -1.1070 + non-price part 0.0109 |
| acct#eea1157e | 2025-08 | 1.6857 | 1.22 | +0.4657 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 1.6752 + non-price part 0.0104 |
| acct#eea1157e | 2025-11 | 1.1521 | 0.71 | +0.4421 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 1.1474 + non-price part 0.0047 |
| acct#eea1157e | 2026-02 | 4.8221 | 4.43 | +0.3921 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 4.8204 + non-price part 0.0016 |
| acct#04ebe1d1 | 2021-01 | 4.5587 | 4.50 | +0.0587 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 4.5587 + non-price part -0.0000 |
| acct#04ebe1d1 | 2021-02 | 9.0791 | 8.82 | +0.2591 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 9.0061 + non-price part 0.0660 |
| acct#04ebe1d1 | 2021-03 | 9.1630 | 9.08 | +0.0830 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 9.1630 + non-price part -0.0000 |
| acct#04ebe1d1 | 2021-04 | -3.5078 | -3.41 | -0.0978 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part -3.5078 + non-price part -0.0000 |
| acct#04ebe1d1 | 2021-05 | 5.4119 | 5.25 | +0.1619 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 5.3436 + non-price part 0.0662 |
| acct#04ebe1d1 | 2021-06 | -4.9435 | -4.82 | -0.1235 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part -4.9435 + non-price part -0.0000 |
| acct#04ebe1d1 | 2021-07 | 0.1092 | 0.17 | -0.0608 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 0.1092 + non-price part 0.0000 |
| acct#04ebe1d1 | 2021-09 | -1.2157 | -1.27 | +0.0543 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part -1.2157 + non-price part -0.0000 |
| acct#04ebe1d1 | 2021-10 | -1.4589 | -1.39 | -0.0689 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part -1.4589 + non-price part -0.0000 |
| acct#04ebe1d1 | 2022-02 | -0.3600 | -0.48 | +0.1200 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part -0.4208 + non-price part 0.0602 |
| acct#04ebe1d1 | 2022-04 | -3.1818 | -3.25 | +0.0682 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part -3.1818 + non-price part -0.0000 |
| acct#04ebe1d1 | 2022-06 | -19.3181 | -19.22 | -0.0981 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part -19.3181 + non-price part 0.0001 |
| acct#04ebe1d1 | 2022-07 | 13.3643 | 13.42 | -0.0557 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 13.3641 + non-price part 0.0002 |
| acct#04ebe1d1 | 2023-01 | 18.5622 | 18.50 | +0.0622 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 18.5614 + non-price part 0.0007 |
| acct#04ebe1d1 | 2023-03 | 1.5910 | 1.66 | -0.0690 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 1.5902 + non-price part 0.0008 |
| acct#04ebe1d1 | 2023-05 | 6.2569 | 6.17 | +0.0869 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 6.1782 + non-price part 0.0749 |
| acct#04ebe1d1 | 2024-02 | 3.4371 | 3.34 | +0.0971 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 3.3624 + non-price part 0.0723 |
| acct#04ebe1d1 | 2025-05 | 1.1102 | 1.01 | +0.1002 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 1.0313 + non-price part 0.0777 |
| acct#04ebe1d1 | 2025-08 | 13.3412 | 13.26 | +0.0812 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 13.2606 + non-price part 0.0705 |
| acct#06873f0a | 2021-01 | -2.5176 | -2.77 | +0.2524 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part -2.5177 + non-price part 0.0001 |
| acct#015306a0 | 2022-04 | -8.3463 | -8.71 | +0.3637 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part -8.3699 + non-price part 0.0257 |
| acct#015306a0 | 2022-05 | 3.3309 | 2.35 | +0.9809 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 3.3306 + non-price part 0.0003 |
| acct#015306a0 | 2022-06 | -6.4644 | -9.60 | +3.1356 | price:distribution: distribution 2022-06-14 step -2.13, distribution 2022-06-16 step -241.40, distribution 2022-06-16 step 198.27 | causes found: price:distribution; best single cause price:distribution leaves +3.2127; all causes together leave +3.2127; computed month = price part -8.1818 + non-price part 1.8070 |
| acct#015306a0 | 2022-08 | -1.9318 | -2.39 | +0.4582 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part -1.9325 + non-price part 0.0007 |
| acct#015306a0 | 2022-10 | 8.0961 | 7.66 | +0.4361 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 7.9695 + non-price part 0.1180 |
| acct#015306a0 | 2022-11 | 5.2205 | 5.71 | -0.4895 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 5.2167 + non-price part 0.0037 |
| acct#015306a0 | 2023-01 | 6.7354 | 6.95 | -0.2146 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 6.6185 + non-price part 0.1114 |
| acct#015306a0 | 2023-02 | -3.4511 | -3.23 | -0.2211 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part -3.4556 + non-price part 0.0046 |
| acct#015306a0 | 2023-03 | 3.3655 | 3.05 | +0.3155 | price:distribution: distribution 2023-03-14 step 152.35, distribution 2023-03-16 step 488.87 | causes found: price:distribution; best single cause price:distribution leaves -0.7449; all causes together leave -0.7449; computed month = price part 3.1729 + non-price part 0.1901 |
| acct#8b1d7784 | 2021-05 | 0.4479 | 0.54 | -0.0921 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 0.4478 + non-price part 0.0001 |
| acct#8b1d7784 | 2021-06 | 2.7230 | 2.31 | +0.4130 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 2.4245 + non-price part 0.2916 |
| acct#8b1d7784 | 2021-10 | 5.4838 | 5.40 | +0.0838 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 5.4838 + non-price part 0.0000 |
| acct#8b1d7784 | 2021-11 | -2.4716 | -2.54 | +0.0684 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part -2.4716 + non-price part 0.0000 |
| acct#8b1d7784 | 2022-01 | -5.5986 | -5.50 | -0.0986 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part -5.5994 + non-price part 0.0008 |
| acct#8b1d7784 | 2022-03 | 2.4619 | 2.15 | +0.3119 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 2.1918 + non-price part 0.2634 |
| acct#8b1d7784 | 2022-04 | -8.0176 | -7.94 | -0.0776 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part -8.0176 + non-price part 0.0000 |
| acct#8b1d7784 | 2022-07 | 7.7465 | 7.66 | +0.0865 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 7.7460 + non-price part 0.0005 |
| acct#8b1d7784 | 2022-11 | 6.5541 | 6.67 | -0.1159 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 6.5530 + non-price part 0.0011 |
| acct#8b1d7784 | 2023-03 | 1.9298 | 1.52 | +0.4098 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 1.5772 + non-price part 0.3511 |
| acct#8b1d7784 | 2023-05 | -0.7435 | -0.84 | +0.0965 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part -0.7448 + non-price part 0.0013 |
| acct#8b1d7784 | 2023-06 | 6.8158 | 6.37 | +0.4458 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 6.4224 + non-price part 0.3696 |
| acct#8b1d7784 | 2023-09 | -4.5761 | -5.00 | +0.4239 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part -4.7040 + non-price part 0.1320 |
| acct#8b1d7784 | 2023-12 | 6.5637 | 5.94 | +0.6237 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 5.9386 + non-price part 0.5943 |
| acct#8b1d7784 | 2024-06 | 2.0877 | 1.69 | +0.3977 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 1.7642 + non-price part 0.3192 |
| acct#8b1d7784 | 2024-09 | 2.5401 | 2.21 | +0.3301 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 2.2319 + non-price part 0.3023 |
| acct#8b1d7784 | 2024-12 | -2.9436 | -3.48 | +0.5364 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part -3.4558 + non-price part 0.5354 |
| acct#8b1d7784 | 2025-06 | 4.8168 | 4.44 | +0.3768 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 4.4499 + non-price part 0.3521 |
| acct#8b1d7784 | 2025-09 | 3.1102 | 2.79 | +0.3202 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 2.7929 + non-price part 0.3086 |
| acct#8b1d7784 | 2025-12 | 0.8484 | 0.31 | +0.5384 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 0.3109 + non-price part 0.5383 |
| acct#fa488a0b | 2021-03 | 2.7879 | 2.50 | +0.2879 | price:distribution: distribution 2021-03-04 step -5.50, distribution 2021-03-25 step 1.42, distribution 2021-03-30 step 35.60, distribution 2021-03-30 step 9.90 | causes found: price:distribution; best single cause price:distribution leaves -0.1441; all causes together leave -0.1441; computed month = price part 2.5383 + non-price part 0.2437 |
| acct#fa488a0b | 2021-04 | 2.3118 | 2.21 | +0.1018 | price:distribution: distribution 2021-04-07 step 3.59 | causes found: price:distribution; best single cause price:distribution leaves +0.0654; all causes together leave +0.0654; computed month = price part 2.2350 + non-price part 0.0750 |
| acct#fa488a0b | 2021-08 | 1.0760 | 1.00 | +0.0760 | price:distribution: distribution 2021-08-05 step -2.50 | causes found: price:distribution; best single cause price:distribution leaves +0.1003; all causes together leave +0.1003; computed month = price part 1.0234 + non-price part 0.0522 |
| acct#fa488a0b | 2022-02 | -1.0014 | -1.09 | +0.0886 | price:distribution: distribution 2022-02-04 step -15.07 | causes found: price:distribution; best single cause price:distribution leaves +0.2327; all causes together leave +0.2327; computed month = price part -1.0527 + non-price part 0.0517 |
| acct#fa488a0b | 2022-07 | 4.2839 | 4.16 | +0.1239 | price:distribution: distribution 2022-07-07 step -2.53 | causes found: price:distribution; best single cause price:distribution leaves +0.1505; all causes together leave +0.1505; computed month = price part 4.2175 + non-price part 0.0643 |
| acct#fa488a0b | 2022-08 | -2.9168 | -2.99 | +0.0732 | price:distribution: distribution 2022-08-04 step 14.18 | causes found: price:distribution; best single cause price:distribution leaves -0.0696; all causes together leave -0.0696; computed month = price part -2.9795 + non-price part 0.0645 |
| acct#fa488a0b | 2022-10 | 5.9632 | 5.80 | +0.1632 | price:distribution: distribution 2022-10-06 step -4.71 | causes found: price:distribution; best single cause price:distribution leaves +0.2157; all causes together leave +0.2157; computed month = price part 5.8883 + non-price part 0.0700 |
| acct#fa488a0b | 2023-12 | 6.5395 | 5.48 | +1.0595 | price:distribution: distribution 2023-12-06 step 18.34, distribution 2023-12-21 step 19.07, distribution 2023-12-27 step 16.64, distribution 2023-12-27 step 22.94, distribution 2023-12-27 step 59.74, distribution 2023-12-28 step 1.35 | causes found: price:distribution; best single cause price:distribution leaves -0.2347; all causes together leave -0.2347; computed month = price part 5.5238 + non-price part 0.9660 |
| acct#fa488a0b | 2024-02 | 1.7166 | 1.60 | +0.1166 | price:distribution: distribution 2024-02-06 step 24.90 | causes found: price:distribution; best single cause price:distribution leaves -0.1045; all causes together leave -0.1045; computed month = price part 1.6299 + non-price part 0.0858 |
| acct#fa488a0b | 2024-06 | -0.0417 | -0.70 | +0.6583 | price:distribution: distribution 2024-06-05 step 19.33, distribution 2024-06-17 step 83.99, distribution 2024-06-25 step 0.48 | causes found: price:distribution; best single cause price:distribution leaves +0.0975; all causes together leave +0.0975; computed month = price part -0.5266 + non-price part 0.4886 |
| acct#2f705c61 | 2020-08 | -2.2021 | -3.75 | +1.5479 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part -2.2023 + non-price part 0.0002 |
| acct#2f705c61 | 2020-10 | -3.1449 | -3.41 | +0.2651 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part -3.1453 + non-price part 0.0003 |
| acct#2f705c61 | 2020-11 | 12.2111 | 11.36 | +0.8511 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 12.2108 + non-price part 0.0002 |
| acct#2f705c61 | 2021-01 | 5.8524 | 6.24 | -0.3876 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 5.8522 + non-price part 0.0002 |
| acct#2f705c61 | 2021-02 | 15.9649 | 15.47 | +0.4949 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 15.9647 + non-price part 0.0002 |
| acct#2f705c61 | 2021-04 | 1.8272 | 1.92 | -0.0928 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 1.8270 + non-price part 0.0002 |
| acct#2f705c61 | 2021-05 | 2.5201 | 1.51 | +1.0101 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 2.5199 + non-price part 0.0002 |
| acct#2f705c61 | 2021-07 | -6.4700 | -6.75 | +0.2800 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part -6.4702 + non-price part 0.0002 |
| acct#2f705c61 | 2021-08 | -2.7930 | -4.01 | +1.2170 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part -2.7932 + non-price part 0.0002 |
| acct#2f705c61 | 2021-10 | 6.9247 | 7.23 | -0.3053 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 6.9245 + non-price part 0.0002 |
| acct#2f705c61 | 2021-11 | -4.3849 | -5.52 | +1.1351 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part -4.3851 + non-price part 0.0002 |
| acct#2f705c61 | 2022-01 | 17.4416 | 18.14 | -0.6984 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 17.4414 + non-price part 0.0002 |
| acct#43c388bc | 2022-05 | 0.9994 | 1.10 | -0.1006 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 0.9991 + non-price part 0.0003 |
| acct#43c388bc | 2022-06 | -3.2131 | -4.45 | +1.2369 | price:distribution: distribution 2022-06-14 step 22.38 | causes found: price:distribution; best single cause price:distribution leaves +1.1087; all causes together leave +1.1087; computed month = price part -3.6944 + non-price part 0.4980 |
| acct#43c388bc | 2022-07 | 2.8646 | 3.13 | -0.2654 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 2.8601 + non-price part 0.0044 |
| acct#43c388bc | 2022-08 | -2.0447 | -2.23 | +0.1853 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part -2.0523 + non-price part 0.0077 |
| acct#43c388bc | 2022-09 | -4.5326 | -5.06 | +0.5274 | price:distribution: distribution 2022-09-13 step -282.52 | causes found: price:distribution; best single cause price:distribution leaves +2.1864; all causes together leave +2.1864; computed month = price part -4.6381 + non-price part 0.1089 |
| acct#43c388bc | 2022-10 | 3.2525 | 3.57 | -0.3175 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 3.2431 + non-price part 0.0091 |
| acct#43c388bc | 2022-11 | 3.5433 | 3.88 | -0.3367 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 3.5341 + non-price part 0.0090 |
| acct#43c388bc | 2022-12 | -1.5239 | -1.98 | +0.4561 | price:distribution: distribution 2022-12-14 step 31.31 | causes found: price:distribution; best single cause price:distribution leaves +0.2756; all causes together leave +0.2756; computed month = price part -1.8256 + non-price part 0.3070 |
| acct#43c388bc | 2023-01 | 2.5837 | 2.82 | -0.2363 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 2.5689 + non-price part 0.0146 |
| acct#f74da374 | 2023-10 | -6.0078 | -3.48 | -2.5278 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part -6.0428 + non-price part 0.0368 |
| acct#f74da374 | 2023-11 | -1.0299 | -2.21 | +1.1801 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part -1.0312 + non-price part 0.0013 |
| acct#f74da374 | 2024-02 | 4.5003 | 3.49 | +1.0103 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 4.4986 + non-price part 0.0017 |
| acct#f74da374 | 2024-04 | -1.9359 | -4.92 | +2.9841 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part -1.5424 + non-price part -0.4052 |
| acct#f74da374 | 2024-05 | -0.0238 | 1.99 | -2.0138 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part -0.1043 + non-price part 0.0800 |
| acct#f74da374 | 2024-06 | -1.1098 | -1.51 | +0.4002 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part -1.4904 + non-price part 0.3883 |
| acct#f74da374 | 2024-07 | -0.5156 | -0.75 | +0.2344 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part -0.5562 + non-price part 0.0421 |
| acct#f74da374 | 2024-08 | -3.4567 | -2.53 | -0.9267 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part -3.5412 + non-price part 0.0870 |
| acct#f74da374 | 2024-09 | -0.9536 | -3.23 | +2.2764 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part -1.3655 + non-price part 0.4136 |
| acct#f74da374 | 2024-10 | 0.1788 | 1.64 | -1.4612 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 0.1324 + non-price part 0.0468 |
| acct#f74da374 | 2024-11 | 2.4897 | 2.36 | +0.1297 | holding:step: quantity step 2024-11-22 -3176, quantity step 2024-11-22 +809 | causes found: holding:step; best single cause holding:step leaves +0.1511; all causes together leave +0.1511; computed month = price part 2.4050 + non-price part 0.0818 |
| acct#2d4385bf | 2022-02 | 2.0092 | 1.55 | +0.4592 | price:split: split x20 (2022-07-18), split x20 (2022-06-06) | causes found: price:split; best single cause price:split leaves +0.0571; all causes together leave +0.0571; computed month = price part 2.0092 + non-price part -0.0000 |
| acct#2d4385bf | 2022-03 | 5.0504 | 4.92 | +0.1304 | price:split: split x20 (2022-07-18), split x20 (2022-06-06) | causes found: price:split; best single cause price:split leaves +0.0741; all causes together leave +0.0741; computed month = price part 5.0504 + non-price part -0.0000 |
| acct#2d4385bf | 2022-09 | -9.5282 | -9.60 | +0.0718 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part -9.5284 + non-price part 0.0002 |
| acct#2d4385bf | 2023-01 | 18.4052 | 18.28 | +0.1252 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 18.2997 + non-price part 0.0906 |
| acct#2d4385bf | 2023-06 | 3.9778 | 3.87 | +0.1078 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 3.9768 + non-price part 0.0010 |
| acct#2d4385bf | 2023-09 | -5.5154 | -5.60 | +0.0846 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part -5.5164 + non-price part 0.0011 |
| acct#2d4385bf | 2023-12 | 4.5008 | 4.38 | +0.1208 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 4.4997 + non-price part 0.0011 |
| acct#2d4385bf | 2024-03 | 4.4871 | 4.40 | +0.0871 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 4.4861 + non-price part 0.0010 |
| acct#2d4385bf | 2024-06 | 6.4109 | 6.26 | +0.1509 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 6.3676 + non-price part 0.0408 |
| acct#2d4385bf | 2024-09 | 2.7016 | 2.56 | +0.1416 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 2.6587 + non-price part 0.0418 |
| acct#2d4385bf | 2024-12 | 5.2716 | 5.11 | +0.1616 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 5.2351 + non-price part 0.0354 |
| acct#2d4385bf | 2025-03 | -8.4616 | -8.56 | +0.0984 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part -8.4978 + non-price part 0.0393 |
| acct#d96c877d | 2022-05 | 13.5627 | 12.45 | +1.1127 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 13.5627 + non-price part -0.0000 |
| acct#d96c877d | 2022-08 | -0.4142 | -1.35 | +0.9358 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part -0.4146 + non-price part 0.0005 |
| acct#d96c877d | 2022-10 | 25.9595 | 26.06 | -0.1005 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 25.9587 + non-price part 0.0006 |
| acct#d96c877d | 2022-11 | 1.2516 | 0.47 | +0.7816 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 1.2508 + non-price part 0.0007 |
| acct#afda5d61 | 2023-06 | 1.0463 | 1.30 | -0.2537 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 0.9981 + non-price part 0.0479 |
| acct#afda5d61 | 2023-08 | -0.4994 | -0.64 | +0.1406 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part -0.5485 + non-price part 0.0493 |
| acct#afda5d61 | 2023-09 | -0.7756 | -0.98 | +0.2044 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part -0.8233 + non-price part 0.0481 |
| acct#afda5d61 | 2024-02 | 0.3670 | 0.43 | -0.0630 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 0.3191 + non-price part 0.0478 |
| acct#afda5d61 | 2024-03 | 0.9351 | 1.11 | -0.1749 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 0.8840 + non-price part 0.0507 |
| acct#afda5d61 | 2024-05 | 0.7298 | 0.87 | -0.1402 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 0.6790 + non-price part 0.0505 |
| acct#afda5d61 | 2024-08 | 0.6962 | 0.82 | -0.1238 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 0.6461 + non-price part 0.0498 |
| acct#afda5d61 | 2024-09 | 0.5863 | 0.69 | -0.1037 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 0.5382 + non-price part 0.0479 |
| acct#f0b52456 | 2023-01 | 11.2072 | 13.60 | -2.3928 | price:split: split x10 (2025-11-17) | causes found: price:split; best single cause price:split leaves +0.6841; all causes together leave +0.6841; computed month = price part 11.6409 + non-price part -0.3897 |
| acct#f0b52456 | 2023-08 | -0.1951 | -1.09 | +0.8949 | price:split: split x10 (2025-11-17) | causes found: price:split; best single cause price:split leaves +0.2763; all causes together leave +0.2763; computed month = price part -0.2932 + non-price part 0.0971 |
| acct#f0b52456 | 2023-11 | 3.8452 | 9.94 | -6.0948 | price:split: split x10 (2025-11-17) | causes found: price:split; best single cause price:split leaves +0.7296; all causes together leave +0.7296; computed month = price part 3.7444 + non-price part 0.0974 |
| acct#f0b52456 | 2024-02 | 2.0311 | 4.85 | -2.8189 | price:split: split x10 (2025-11-17) | causes found: price:split; best single cause price:split leaves +0.3968; all causes together leave +0.3968; computed month = price part 1.9386 + non-price part 0.0918 |
| acct#f0b52456 | 2024-05 | 2.7914 | 10.97 | -8.1786 | price:split: split x10 (2025-11-17) | causes found: price:split; best single cause price:split leaves +0.6370; all causes together leave +0.6370; computed month = price part 2.7032 + non-price part 0.0858 |
| acct#f0b52456 | 2024-08 | 1.2549 | 7.72 | -6.4651 | price:split: split x10 (2025-11-17) | causes found: price:split; best single cause price:split leaves +0.5105; all causes together leave +0.5105; computed month = price part 1.1585 + non-price part 0.0961 |
| acct#f0b52456 | 2025-05 | 7.0205 | 6.58 | +0.4405 | price:split: split x10 (2025-11-17) | causes found: price:split; best single cause price:split leaves +0.1713; all causes together leave +0.1713; computed month = price part 6.9370 + non-price part 0.0786 |
| acct#f0b52456 | 2026-02 | 11.9323 | 11.69 | +0.2423 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 11.9033 + non-price part 0.0262 |
| acct#3192493b | 2024-08 | 1.1369 | 0.65 | +0.4869 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 0.8275 + non-price part 0.3030 |
| acct#67c40ffb | 2024-12 | -6.3731 | -6.74 | +0.3669 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part -6.6173 + non-price part 0.2595 |
| acct#5944e1e8 | 2021-06 | 3.5148 | 2.36 | +1.1548 | price:distribution: distribution 2021-06-17 step 175.86 | causes found: price:distribution; best single cause price:distribution leaves +0.4646; all causes together leave +0.4646; computed month = price part 2.8876 + non-price part 0.6109 |
| acct#5944e1e8 | 2021-11 | -3.6409 | -3.50 | -0.1409 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part -3.6409 + non-price part -0.0000 |
| acct#5944e1e8 | 2021-12 | 17.2859 | 1.95 | +15.3359 | price:distribution: distribution 2021-12-16 step 48.43, distribution 2021-12-17 step 621.54, distribution 2021-12-17 step 352.21, distribution 2021-12-17 step 393.36, distribution 2021-12-20 step 337.05 | causes found: price:distribution; best single cause price:distribution leaves +8.6854; all causes together leave +8.6854; computed month = price part 9.4758 + non-price part 7.1923 |
| acct#5944e1e8 | 2022-03 | 0.9060 | 1.17 | -0.2640 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 0.9060 + non-price part -0.0000 |
| acct#5944e1e8 | 2022-05 | -0.9726 | -1.07 | +0.0974 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part -0.9727 + non-price part 0.0001 |
| acct#5944e1e8 | 2022-06 | -5.9566 | -8.58 | +2.6234 | price:distribution: distribution 2022-06-16 step 142.74 | causes found: price:distribution; best single cause price:distribution leaves +2.0323; all causes together leave +2.0323; computed month = price part -7.2059 + non-price part 1.2986 |
| acct#5944e1e8 | 2022-08 | -3.6248 | -3.69 | +0.0652 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part -3.6251 + non-price part 0.0003 |
| acct#5944e1e8 | 2022-11 | 7.3841 | 7.21 | +0.1741 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 7.3832 + non-price part 0.0008 |
| acct#5944e1e8 | 2022-12 | -1.7845 | -4.79 | +3.0055 | price:distribution: distribution 2022-12-16 step 145.86, distribution 2022-12-16 step 7.70, distribution 2022-12-19 step 110.29 | causes found: price:distribution; best single cause price:distribution leaves +1.9054; all causes together leave +1.9054; computed month = price part -3.4343 + non-price part 1.6990 |
| acct#5944e1e8 | 2023-03 | 2.4965 | 2.68 | -0.1835 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 2.4962 + non-price part 0.0003 |
| acct#25880078 | 2021-06 | 3.5285 | 2.39 | +1.1385 | price:distribution: distribution 2021-06-17 step 134.51 | causes found: price:distribution; best single cause price:distribution leaves +0.4578; all causes together leave +0.4578; computed month = price part 2.9098 + non-price part 0.6024 |
| acct#25880078 | 2021-12 | 17.3601 | 1.92 | +15.4401 | price:distribution: distribution 2021-12-16 step 37.04, distribution 2021-12-17 step 512.20, distribution 2021-12-17 step 273.67, distribution 2021-12-17 step 275.33, distribution 2021-12-20 step 273.48 | causes found: price:distribution; best single cause price:distribution leaves +8.7353; all causes together leave +8.7353; computed month = price part 9.5036 + non-price part 7.2359 |
| acct#25880078 | 2022-03 | 0.8831 | 1.16 | -0.2769 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 0.8831 + non-price part -0.0000 |
| acct#25880078 | 2022-05 | -0.9687 | -1.07 | +0.1013 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part -0.9689 + non-price part 0.0002 |
| acct#25880078 | 2022-06 | -5.9366 | -8.54 | +2.6034 | price:distribution: distribution 2022-06-16 step 109.17 | causes found: price:distribution; best single cause price:distribution leaves +2.0210; all causes together leave +2.0210; computed month = price part -7.1676 + non-price part 1.2794 |
| acct#25880078 | 2022-08 | -3.5857 | -3.66 | +0.0743 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part -3.5861 + non-price part 0.0004 |
| acct#25880078 | 2022-12 | -1.7987 | -4.77 | +2.9713 | price:distribution: distribution 2022-12-16 step 5.98, distribution 2022-12-16 step 108.26, distribution 2022-12-19 step 86.25 | causes found: price:distribution; best single cause price:distribution leaves +1.8934; all causes together leave +1.8934; computed month = price part -3.4218 + non-price part 1.6712 |
| acct#25880078 | 2023-03 | 2.4557 | 2.65 | -0.1943 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 2.4543 + non-price part 0.0014 |
| acct#0c8de232 | 2022-11 | 7.5694 | 7.62 | -0.0506 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 7.5666 + non-price part 0.0027 |
| acct#0c8de232 | 2023-01 | 6.1709 | 5.53 | +0.6409 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 5.6608 + non-price part 0.4840 |
| acct#0c8de232 | 2023-04 | -4.4785 | -5.10 | +0.6215 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part -5.0082 + non-price part 0.5528 |
| acct#0c8de232 | 2023-05 | 2.6355 | 2.70 | -0.0645 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 2.6310 + non-price part 0.0043 |
| acct#0c8de232 | 2023-08 | 6.2507 | 6.34 | -0.0893 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 6.2463 + non-price part 0.0042 |
| acct#0c8de232 | 2023-09 | -5.5296 | -5.64 | +0.1104 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part -5.5517 + non-price part 0.0235 |
| acct#0c8de232 | 2023-11 | -1.6409 | -1.81 | +0.1691 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part -1.6456 + non-price part 0.0048 |
| acct#0c8de232 | 2024-01 | 1.5644 | 1.04 | +0.5244 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 1.0757 + non-price part 0.4811 |
| acct#0c8de232 | 2024-02 | -0.3805 | -0.47 | +0.0895 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part -0.3828 + non-price part 0.0023 |
| acct#0c8de232 | 2024-05 | 0.9454 | 0.89 | +0.0554 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 0.9426 + non-price part 0.0029 |
| acct#0c8de232 | 2024-07 | 2.5402 | 2.04 | +0.5002 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 2.0292 + non-price part 0.4981 |
| acct#0c8de232 | 2024-10 | 2.9513 | 2.50 | +0.4513 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 2.5075 + non-price part 0.4303 |
| acct#0c8de232 | 2025-01 | 3.8713 | 3.44 | +0.4313 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 3.4631 + non-price part 0.3974 |
| acct#0c8de232 | 2025-10 | 5.3347 | 4.97 | +0.3647 | price:distribution: distribution 2025-10-31 step 83.34 | causes found: price:distribution; best single cause price:distribution leaves +0.3505; all causes together leave +0.3505; computed month = price part 4.9535 + non-price part 0.3624 |
| acct#0c8de232 | 2026-04 | 15.1355 | 14.75 | +0.3855 | price:distribution: distribution 2026-04-30 step 71.62 | causes found: price:distribution; best single cause price:distribution leaves +0.3742; all causes together leave +0.3742; computed month = price part 14.7774 + non-price part 0.3131 |
| acct#e29efebe | 2020-08 | 10.2446 | 9.98 | +0.2646 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 10.2446 + non-price part -0.0000 |
| acct#e29efebe | 2020-11 | 5.9943 | 5.72 | +0.2743 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 5.9943 + non-price part -0.0000 |
| acct#e29efebe | 2021-02 | 0.4114 | 0.18 | +0.2314 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 0.4114 + non-price part 0.0000 |
| acct#e29efebe | 2021-05 | -0.7604 | -0.99 | +0.2296 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part -0.7604 + non-price part -0.0000 |
| acct#e29efebe | 2021-08 | 6.1478 | 5.95 | +0.1978 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 6.1478 + non-price part -0.0000 |
| acct#e29efebe | 2021-11 | -0.1278 | -0.31 | +0.1822 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part -0.1278 + non-price part -0.0000 |
| acct#e29efebe | 2022-02 | -3.7005 | -3.90 | +0.1995 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part -3.7005 + non-price part -0.0000 |
| acct#e29efebe | 2022-05 | -1.7924 | -2.02 | +0.2276 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part -1.7924 + non-price part -0.0000 |
| acct#e29efebe | 2022-08 | -6.5959 | -6.79 | +0.1941 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part -6.5961 + non-price part 0.0002 |
| acct#e29efebe | 2022-11 | 10.0659 | 9.77 | +0.2959 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 10.0657 + non-price part 0.0002 |
| acct#e29efebe | 2023-02 | 0.8870 | 0.64 | +0.2470 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 0.8865 + non-price part 0.0006 |
| acct#e29efebe | 2023-05 | 6.9985 | 6.77 | +0.2285 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 6.9975 + non-price part 0.0009 |
| acct#e29efebe | 2023-08 | -2.1849 | -2.39 | +0.2051 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part -2.1859 + non-price part 0.0010 |
| acct#e29efebe | 2023-11 | 12.0705 | 11.85 | +0.2205 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 12.0694 + non-price part 0.0010 |
| acct#e29efebe | 2024-02 | 4.1591 | 3.97 | +0.1891 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 4.1581 + non-price part 0.0009 |
| acct#e29efebe | 2024-08 | -0.1061 | -0.28 | +0.1739 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part -0.1073 + non-price part 0.0013 |
| acct#e29efebe | 2024-11 | 4.3223 | 4.12 | +0.2023 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 4.3210 + non-price part 0.0012 |
| acct#e29efebe | 2025-02 | -4.0631 | -4.25 | +0.1869 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part -4.0635 + non-price part 0.0005 |
| acct#79d02c2c | 2022-11 | 4.2238 | 4.61 | -0.3862 | price:split: split x3 (2024-10-11), split x2 (2024-10-11) | causes found: price:split; best single cause price:split leaves +0.0548; all causes together leave +0.0548; computed month = price part 4.0845 + non-price part 0.1345 |
| acct#79d02c2c | 2022-12 | -2.5786 | -4.35 | +1.7714 | price:split: split x3 (2024-10-11), split x2 (2024-10-11) | causes found: price:split; best single cause price:split leaves +0.3884; all causes together leave +0.3884; computed month = price part -3.6731 + non-price part 1.1422 |
| acct#79d02c2c | 2023-02 | -1.9272 | -2.27 | +0.3428 | price:split: split x3 (2024-10-11), split x2 (2024-10-11) | causes found: price:split; best single cause price:split leaves +0.0769; all causes together leave +0.0769; computed month = price part -2.0780 + non-price part 0.1550 |
| acct#79d02c2c | 2023-09 | -2.6856 | -4.03 | +1.3444 | price:split: split x3 (2024-10-11), split x2 (2024-10-11) | causes found: price:split; best single cause price:split leaves +0.3173; all causes together leave +0.3173; computed month = price part -3.5316 + non-price part 0.8776 |
| acct#79d02c2c | 2023-11 | 6.8895 | 7.80 | -0.9105 | price:split: split x3 (2024-10-11), split x2 (2024-10-11) | causes found: price:split; best single cause price:split leaves +0.1005; all causes together leave +0.1005; computed month = price part 6.7121 + non-price part 0.1667 |
| acct#79d02c2c | 2024-02 | 3.1598 | 3.72 | -0.5602 | price:split: split x3 (2024-10-11), split x2 (2024-10-11) | causes found: price:split; best single cause price:split leaves +0.1210; all causes together leave +0.1210; computed month = price part 2.9825 + non-price part 0.1728 |
| acct#79d02c2c | 2024-05 | 3.5452 | 3.94 | -0.3948 | price:split: split x3 (2024-10-11), split x2 (2024-10-11) | causes found: price:split; best single cause price:split leaves +0.0771; all causes together leave +0.0771; computed month = price part 3.3839 + non-price part 0.1562 |
| acct#79d02c2c | 2024-11 | 5.4413 | 5.35 | +0.0913 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 5.3749 + non-price part 0.0635 |
| acct#79d02c2c | 2025-05 | 4.9263 | 4.84 | +0.0863 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 4.8608 + non-price part 0.0627 |
| acct#4a890dd1 | 2022-11 | 4.2434 | 4.62 | -0.3766 | price:split: split x3 (2024-10-11), split x2 (2024-10-11) | causes found: price:split; best single cause price:split leaves +0.0585; all causes together leave +0.0585; computed month = price part 4.1069 + non-price part 0.1318 |
| acct#4a890dd1 | 2022-12 | -2.6145 | -4.39 | +1.7755 | price:split: split x3 (2024-10-11), split x2 (2024-10-11) | causes found: price:split; best single cause price:split leaves +0.3955; all causes together leave +0.3955; computed month = price part -3.7141 + non-price part 1.1481 |
| acct#4a890dd1 | 2023-02 | -1.9340 | -2.27 | +0.3360 | price:split: split x3 (2024-10-11), split x2 (2024-10-11) | causes found: price:split; best single cause price:split leaves +0.0747; all causes together leave +0.0747; computed month = price part -2.0817 + non-price part 0.1519 |
| acct#4a890dd1 | 2023-09 | -2.7037 | -4.05 | +1.3463 | price:split: split x3 (2024-10-11), split x2 (2024-10-11) | causes found: price:split; best single cause price:split leaves +0.3211; all causes together leave +0.3211; computed month = price part -3.5549 + non-price part 0.8832 |
| acct#4a890dd1 | 2023-11 | 6.9352 | 7.84 | -0.9048 | price:split: split x3 (2024-10-11), split x2 (2024-10-11) | causes found: price:split; best single cause price:split leaves +0.0955; all causes together leave +0.0955; computed month = price part 6.7615 + non-price part 0.1632 |
| acct#4a890dd1 | 2024-02 | 3.2031 | 3.76 | -0.5569 | price:split: split x3 (2024-10-11), split x2 (2024-10-11) | causes found: price:split; best single cause price:split leaves +0.1183; all causes together leave +0.1183; computed month = price part 3.0296 + non-price part 0.1691 |
| acct#4a890dd1 | 2024-05 | 3.5679 | 3.96 | -0.3921 | price:split: split x3 (2024-10-11), split x2 (2024-10-11) | causes found: price:split; best single cause price:split leaves +0.0750; all causes together leave +0.0750; computed month = price part 3.4101 + non-price part 0.1528 |
| acct#4a890dd1 | 2024-11 | 5.4720 | 5.39 | +0.0820 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 5.4073 + non-price part 0.0618 |
| acct#4a890dd1 | 2025-05 | 4.9152 | 4.83 | +0.0852 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 4.8518 + non-price part 0.0606 |
| acct#e9c58478 | 2021-10 | 5.6330 | 5.53 | +0.1030 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 5.6330 + non-price part -0.0000 |
| acct#1f02bee1 | 2022-09 | -21.6921 | -21.92 | +0.2279 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part -21.6921 + non-price part -0.0000 |
| acct#1f02bee1 | 2022-12 | 7.3093 | 6.96 | +0.3493 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 6.9743 + non-price part 0.3063 |
| acct#f78e8ecd | 2025-06 | 2.7809 | 2.58 | +0.2009 | price:distribution: distribution 2025-06-30 step 5.67 | causes found: price:distribution; best single cause price:distribution leaves +0.1909; all causes together leave +0.1909; computed month = price part 2.7703 + non-price part 0.0104 |
| acct#f78e8ecd | 2025-09 | 5.0851 | 5.02 | +0.0651 | price:distribution: distribution 2025-09-30 step 4.96 | causes found: price:distribution; best single cause price:distribution leaves +0.0599; all causes together leave +0.0599; computed month = price part 5.0626 + non-price part 0.0215 |
| acct#f78e8ecd | 2025-10 | -0.8727 | -1.13 | +0.2573 | price:distribution: distribution 2025-10-31 step 5.01 | causes found: price:distribution; best single cause price:distribution leaves +0.2523; all causes together leave +0.2523; computed month = price part -1.0820 + non-price part 0.2140 |
| acct#f78e8ecd | 2025-11 | 12.5832 | 2.22 | +10.3632 | flow_value: li 2025-11-20 amount 5302.48 vs shares worth 14452.87; price:distribution: distribution 2025-11-28 step 4.65 | causes found: flow_value, price:distribution; best single cause flow_value leaves +0.7746; all causes together leave +0.7705; computed month = price part 2.2074 + non-price part 10.0571 |
| acct#f78e8ecd | 2026-02 | 23.1503 | 3.10 | +20.0503 | flow_value: li 2026-02-23 amount 5282.60 vs shares worth 16729.65, li 2026-02-23 amount 14436.70 vs shares worth 25301.95; price:distribution: distribution 2026-02-27 step 4.01; price:spike: spike 2026-02-05..2026-02-08 | causes found: flow_value, price:distribution, price:spike; best single cause flow_value leaves +1.0427; all causes together leave +1.0402; computed month = price part 3.3602 + non-price part 19.3018 |
| acct#16f4eae3 | 2024-08 | 1.3742 | 1.23 | +0.1442 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 1.2322 + non-price part 0.1404 |
| acct#16f4eae3 | 2024-09 | 1.7708 | 1.53 | +0.2408 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 1.5304 + non-price part 0.2358 |
| acct#16f4eae3 | 2024-11 | 2.4475 | 2.28 | +0.1675 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 2.3063 + non-price part 0.1379 |
| acct#16f4eae3 | 2025-05 | 1.9530 | 1.79 | +0.1630 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 1.8047 + non-price part 0.1456 |
| acct#16f4eae3 | 2025-06 | 2.4907 | 1.96 | +0.5307 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 1.9728 + non-price part 0.5074 |
| acct#16f4eae3 | 2025-08 | 2.3566 | 2.21 | +0.1466 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 2.2162 + non-price part 0.1376 |
| acct#16f4eae3 | 2025-09 | 2.4480 | 2.22 | +0.2280 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 2.2301 + non-price part 0.2135 |
| acct#16f4eae3 | 2025-12 | 1.5452 | 0.82 | +0.7252 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 0.8194 + non-price part 0.7211 |
| acct#16f4eae3 | 2026-02 | 2.1515 | 2.02 | +0.1315 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 2.0241 + non-price part 0.1244 |
| acct#0f2d2c45 | 2023-09 | -3.9181 | -4.31 | +0.3919 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part -4.0745 + non-price part 0.1607 |
| acct#cce589ab | 2023-09 | -3.9211 | -4.32 | +0.3989 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part -4.0773 + non-price part 0.1606 |
| acct#cce589ab | 2024-06 | 1.9890 | 1.62 | +0.3690 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 1.6645 + non-price part 0.3204 |
| acct#cce589ab | 2024-09 | 2.3335 | 2.04 | +0.2935 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 2.0407 + non-price part 0.2876 |
| acct#cce589ab | 2024-12 | -2.4657 | -3.01 | +0.5443 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part -2.9899 + non-price part 0.5449 |
| acct#cce589ab | 2025-06 | 4.7491 | 4.44 | +0.3091 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 4.4393 + non-price part 0.2973 |
| acct#cce589ab | 2025-09 | 3.2417 | 2.97 | +0.2717 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 2.9695 + non-price part 0.2643 |
| acct#cce589ab | 2025-12 | 0.8711 | 0.32 | +0.5511 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 0.3220 + non-price part 0.5498 |
| D49141619 | 2022-06 | -7.4767 | -19.63 | +12.1533 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part -7.8466 + non-price part 0.3947 |
| D49141619 | 2022-07 | 4.6981 | 9.36 | -4.6619 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 4.6980 + non-price part 0.0002 |
| D49141619 | 2022-08 | -0.0407 | 0.18 | -0.2207 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part -0.0410 + non-price part 0.0003 |
| D49141619 | 2022-09 | -4.4654 | -9.20 | +4.7346 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part -5.4725 + non-price part 1.0678 |
| D49141619 | 2022-10 | 10.7016 | 25.19 | -14.4884 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 10.7010 + non-price part 0.0005 |
| D49141619 | 2022-11 | 3.1578 | 3.72 | -0.5622 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 3.1572 + non-price part 0.0005 |
| D49141619 | 2022-12 | -3.5084 | -5.49 | +1.9816 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part -3.9100 + non-price part 0.4181 |
| D49141619 | 2023-02 | -5.5732 | -6.81 | +1.2368 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part -5.5429 + non-price part -0.0324 |
| D49141619 | 2023-03 | -1.0571 | -3.19 | +2.1329 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part -1.5067 + non-price part 0.4519 |
| D49141619 | 2023-04 | -1.5420 | 2.15 | -3.6920 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part -2.0078 + non-price part 0.4685 |
| D49141619 | 2023-05 | -6.0100 | -8.97 | +2.9600 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part -6.0163 + non-price part 0.0066 |
| D49141619 | 2023-07 | 2.0424 | 5.11 | -3.0676 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 2.0896 + non-price part -0.0465 |
| D49141619 | 2023-08 | 0.9718 | -1.43 | +2.4018 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 0.9666 + non-price part 0.0052 |
| D49141619 | 2023-10 | -6.5613 | -4.11 | -2.4513 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part -6.5170 + non-price part -0.0471 |
| D49141619 | 2023-11 | 0.5332 | -0.59 | +1.1232 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 0.5276 + non-price part 0.0056 |
| D49141619 | 2024-01 | -0.2709 | -2.05 | +1.7791 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part -0.2235 + non-price part -0.0474 |
| D49141619 | 2024-02 | 4.7739 | 3.65 | +1.1239 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 4.7703 + non-price part 0.0035 |
| D49141619 | 2024-03 | 7.0960 | 9.64 | -2.5440 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 6.6213 + non-price part 0.4446 |
| D49141619 | 2024-04 | 2.2999 | -1.17 | +3.4699 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 1.8187 + non-price part 0.4743 |
| D49141619 | 2024-05 | 0.4590 | 2.45 | -1.9910 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 0.4564 + non-price part 0.0027 |
| D49141619 | 2024-07 | -0.5627 | -0.78 | +0.2173 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part -0.5123 + non-price part -0.0503 |
| D49141619 | 2024-08 | -1.7770 | -1.18 | -0.5970 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part -1.7777 + non-price part 0.0007 |
| D49141619 | 2024-09 | 3.9793 | 1.86 | +2.1193 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 3.1410 + non-price part 0.8097 |
| D49141619 | 2024-10 | 5.2899 | 3.48 | +1.8099 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 2.0006 + non-price part 3.2010 |
| D49141619 | 2026-02 | 5.0959 | 4.67 | +0.4259 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 5.0924 + non-price part 0.0034 |
| D49143349 | 2022-07 | 3.3205 | 7.73 | -4.4095 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 3.3203 + non-price part 0.0002 |
| D49143349 | 2022-08 | -1.4647 | -0.79 | -0.6747 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part -1.4651 + non-price part 0.0003 |
| D49143349 | 2022-09 | -4.8332 | -9.85 | +5.0168 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part -5.5034 + non-price part 0.7071 |
| D49143349 | 2022-10 | 5.4111 | 20.15 | -14.7389 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 5.4105 + non-price part 0.0006 |
| D49143349 | 2022-11 | 4.3030 | 4.87 | -0.5670 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 4.3024 + non-price part 0.0005 |
| D49143349 | 2023-02 | -8.5045 | -9.87 | +1.3655 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part -8.4791 + non-price part -0.0274 |
| D49143349 | 2023-03 | 1.1765 | -2.65 | +3.8265 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 0.9727 + non-price part 0.2011 |
| D49143349 | 2023-04 | -5.7172 | -1.45 | -4.2672 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part -7.3838 + non-price part 1.7698 |
| D49143349 | 2023-05 | -3.7325 | -7.26 | +3.5275 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part -3.7495 + non-price part 0.0176 |
| D49143349 | 2023-07 | 3.7322 | 7.90 | -4.1678 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 3.7723 + non-price part -0.0386 |
| D49143349 | 2023-08 | 1.1696 | -2.76 | +3.9296 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 1.1568 + non-price part 0.0127 |
| D49143349 | 2023-10 | -1.9048 | 1.40 | -3.3048 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part -1.8681 + non-price part -0.0378 |
| D49143349 | 2023-11 | 0.9796 | 0.28 | +0.6996 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 0.9670 + non-price part 0.0125 |
| D49143349 | 2023-12 | 1.6604 | 1.90 | -0.2396 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 1.4451 + non-price part 0.2104 |
| D49143349 | 2024-01 | -3.4834 | -5.74 | +2.2566 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part -3.4421 + non-price part -0.0428 |
| D49143349 | 2024-02 | 0.0584 | -1.09 | +1.1484 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 0.0506 + non-price part 0.0078 |
| D49143349 | 2024-03 | 4.6328 | 6.67 | -2.0372 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 4.4147 + non-price part 0.2087 |
| D49143349 | 2024-04 | 7.2139 | 2.19 | +5.0239 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 5.2789 + non-price part 1.8382 |
| D49143349 | 2024-05 | 1.8434 | 4.89 | -3.0466 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 1.8376 + non-price part 0.0057 |
| D49143349 | 2024-06 | -2.4249 | -2.98 | +0.5551 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part -2.6026 + non-price part 0.1827 |
| D49143349 | 2024-07 | -1.1778 | -1.52 | +0.3422 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part -1.1306 + non-price part -0.0477 |
| D49143349 | 2024-08 | -0.6222 | -0.34 | -0.2822 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part -0.6235 + non-price part 0.0014 |
| D49143349 | 2024-09 | 6.1198 | 3.57 | +2.5498 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 4.6318 + non-price part 1.4462 |
| D49143349 | 2024-10 | -4.0513 | -2.55 | -1.5013 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part -4.0020 + non-price part -0.0512 |
| D49143349 | 2026-02 | 6.2060 | 5.68 | +0.5260 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 6.2034 + non-price part 0.0025 |
| D49143350 | 2023-10 | -5.1391 | -2.27 | -2.8691 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part -5.1856 + non-price part 0.0490 |
| D49143350 | 2023-11 | -3.4367 | -4.59 | +1.1533 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part -3.4429 + non-price part 0.0064 |
| D49143350 | 2024-01 | -0.9653 | -3.13 | +2.1647 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part -1.0247 + non-price part 0.0607 |
| D49143350 | 2024-02 | 4.3275 | 3.15 | +1.1775 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 4.3228 + non-price part 0.0045 |
| D49143350 | 2024-04 | -0.1629 | -4.31 | +4.1471 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part -0.2842 + non-price part 0.1216 |
| D49143350 | 2024-05 | -0.1516 | 2.32 | -2.4716 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part -0.2052 + non-price part 0.0534 |
| D49143350 | 2024-06 | -0.0276 | -0.54 | +0.5124 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part -0.4558 + non-price part 0.4324 |
| D49143350 | 2024-07 | 0.3391 | 0.03 | +0.3091 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 0.2819 + non-price part 0.0583 |
| D49143350 | 2024-08 | -2.5204 | -1.41 | -1.1104 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part -2.5758 + non-price part 0.0566 |
| D49143350 | 2024-09 | -1.4163 | -3.99 | +2.5737 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part -1.8587 + non-price part 0.4459 |
| D49143350 | 2024-10 | -0.5339 | 1.17 | -1.7039 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part -0.5946 + non-price part 0.0615 |
| D49143350 | 2024-11 | 2.1183 | 2.02 | +0.0983 | holding:step: quantity step 2024-11-22 -7024, quantity step 2024-11-22 +1791 | causes found: holding:step; best single cause holding:step leaves +0.0788; all causes together leave +0.0788; computed month = price part 2.0538 + non-price part 0.0632 |
| D49143350 | 2025-11 | -9.1456 | -9.49 | +0.3444 | price:distribution: distribution 2025-11-28 step 303.09 | causes found: price:distribution; best single cause price:distribution leaves +0.2885; all causes together leave +0.2885; computed month = price part -9.2017 + non-price part 0.0627 |
| acct#a011b5f7 | 2026-02 | -0.6544 | -1.00 | +0.3456 | price:distribution: distribution 2026-02-06 step 475.31 | causes found: price:distribution; best single cause price:distribution leaves -1.6169; all causes together leave -1.6169; computed month = price part -0.8236 + non-price part 0.1737 |
| acct#6834d5a2 | 2024-05 | 6.2939 | 3.20 | +3.0939 | price:distribution: distribution 2024-05-31 step 594.65 | causes found: price:distribution; best single cause price:distribution leaves +2.7790; all causes together leave +2.7790; computed month = price part 6.2225 + non-price part 0.0628 |
| acct#6834d5a2 | 2024-06 | -4.0112 | -2.86 | -1.1512 | price:distribution: distribution 2024-06-28 step 577.45 | causes found: price:distribution; best single cause price:distribution leaves -1.4389; all causes together leave -1.4389; computed month = price part -4.2997 + non-price part 0.3003 |
| acct#6834d5a2 | 2024-07 | 7.3798 | 1.02 | +6.3598 | price:distribution: distribution 2024-07-31 step 601.30 | causes found: price:distribution; best single cause price:distribution leaves +6.0477; all causes together leave +6.0477; computed month = price part 7.2959 + non-price part 0.0848 |
| acct#6834d5a2 | 2024-08 | -3.8455 | -1.48 | -2.3655 | price:distribution: distribution 2024-08-30 step 603.86 | causes found: price:distribution; best single cause price:distribution leaves -2.6573; all causes together leave -2.6573; computed month = price part -4.1377 + non-price part 0.3053 |
| acct#6834d5a2 | 2024-09 | -2.7509 | 2.58 | -5.3309 | price:distribution: distribution 2024-09-30 step 567.81 | causes found: price:distribution; best single cause price:distribution leaves -5.6163; all causes together leave -5.6163; computed month = price part -3.0364 + non-price part 0.2945 |
| acct#6834d5a2 | 2024-10 | -3.1292 | -1.69 | -1.4392 | price:distribution: distribution 2024-10-31 step 555.46 | causes found: price:distribution; best single cause price:distribution leaves -1.7264; all causes together leave -1.7264; computed month = price part -3.2003 + non-price part 0.0717 |
| acct#6834d5a2 | 2024-12 | -1.6071 | -0.11 | -1.4971 | price:distribution: distribution 2024-12-31 step 520.62 | causes found: price:distribution; best single cause price:distribution leaves -1.7728; all causes together leave -1.7728; computed month = price part -1.8855 + non-price part 0.2816 |
| acct#6834d5a2 | 2025-02 | -3.5094 | -0.34 | -3.1694 | price:distribution: distribution 2025-02-28 step 448.33 | causes found: price:distribution; best single cause price:distribution leaves -3.4248; all causes together leave -3.4248; computed month = price part -3.7652 + non-price part 0.2660 |
| acct#6834d5a2 | 2025-03 | -1.5250 | -0.91 | -0.6150 | price:distribution: distribution 2025-03-31 step 497.15 | causes found: price:distribution; best single cause price:distribution leaves -0.9085; all causes together leave -0.9085; computed month = price part -1.8185 + non-price part 0.2986 |
| acct#cf292cea | 2024-06 | -0.8093 | -1.39 | +0.5807 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part -0.8327 + non-price part 0.0234 |
| acct#cf292cea | 2024-09 | -3.6475 | -4.27 | +0.6225 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part -3.6730 + non-price part 0.0266 |
| acct#65b3b3ea | 2024-11 | 1.8405 | 1.01 | +0.8305 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 1.8405 + non-price part 0.0000 |
| acct#65b3b3ea | 2025-02 | 5.1009 | 4.18 | +0.9209 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 5.1007 + non-price part 0.0002 |
| acct#65b3b3ea | 2025-05 | -2.2209 | -3.10 | +0.8791 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part -2.2212 + non-price part 0.0003 |
| acct#65b3b3ea | 2025-08 | 3.2451 | 2.32 | +0.9251 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 3.2446 + non-price part 0.0005 |
| acct#65b3b3ea | 2025-11 | 2.1798 | 1.32 | +0.8598 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 2.1795 + non-price part 0.0003 |
| acct#65b3b3ea | 2026-02 | 8.2947 | 7.60 | +0.6947 | no step event on the panel | causes found: none; best single cause none found; all causes together none found; computed month = price part 8.2946 + non-price part 0.0001 |
| acct#7f62f16f | 2026-02 | -0.6506 | -0.99 | +0.3394 | price:distribution: distribution 2026-02-06 step 342.82 | causes found: price:distribution; best single cause price:distribution leaves -1.6117; all causes together leave -1.6117; computed month = price part -0.8188 + non-price part 0.1727 |
| acct#8148a2c4 | 2026-02 | -0.6483 | -0.99 | +0.3417 | price:distribution: distribution 2026-02-06 step 207.58 | causes found: price:distribution; best single cause price:distribution leaves -1.6025; all causes together leave -1.6025; computed month = price part -0.8159 + non-price part 0.1721 |
| acct#cce36d1f | 2026-02 | -0.6440 | -0.98 | +0.3360 | price:distribution: distribution 2026-02-06 step 50.23 | causes found: price:distribution; best single cause price:distribution leaves -1.5959; all causes together leave -1.5959; computed month = price part -0.8107 + non-price part 0.1711 |


## At the committed cap 0.5 (CB-ab-3; hand-appended after the run, the generated text above is unchanged)

- traced 70 of 512 at cap 0.5 (round 27 at cap 1.0: 73). Classes: price 70. The `flow_value` class DROPPED: its only month does not hold at 0.5.
- The 3 months traced only at 1.0, each now `untraced:` (all other 509 months keep their round-27 class):
  - acct#f0b52456 2024-05: price:64110L106 (split) at 1.0; at 0.5 the split leaves +0.6370, untraced.
  - acct#f0b52456 2024-08: price:64110L106 (split) at 1.0; at 0.5 the split leaves +0.5105, untraced.
  - acct#f78e8ecd 2025-11: flow_value:02079K305 at 1.0; at 0.5 flow_value leaves +0.7746, untraced.
- No cap change is proposed.

DIFF-TRACE months=512 traced=70 untraced=442 classes=2 cap=0.5
