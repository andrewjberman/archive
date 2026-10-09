# Non-MATCH census (CB-z-2)

## The denominator

- graded account-months: 82593; MATCH 3098 (3.75% of the total); non-MATCH 79495 = DIFF 886 + UNGRADABLE 78609
- every non-MATCH month is classed once: the class counts below sum to 79495 (non-MATCH months: 79495) -- sum_ok=True
- re-derived daily returns reproduce the persisted grade: DIFF months 886 of 886 reproduce the persisted computed return (tolerance 1e-06 pct points); cash leg method_r26; sweep list v1

## The rules, fixed before the counts

UNGRADABLE: the class is the blank reason of the month's first blank day as the grade names it and as the re-derived daily returns give it (FIRST_DAY, UNPRICED, NON_POSITIVE_BASE, ...); a month with no blank day takes its reported-side reason (NO_DAILY_RETURNS, NO_REPORTED_RETURN, REPORTED_SPAN, REPORTED_NULL, REPORTED_NOT_FINITE, REPORTED_ROWS_DISAGREE). A reported-side reason beside a blank day is counted as `also`, not as a class.

DIFF: the class is the largest traced driver of D = computed - reported. A driver is a posting category whose treatment the method decides (CLIENT_FLOW, FEE_DRAG, CHARGE_FLOW, TAX, ASF_UNSOURCED, INCOME, SWEEP_CASH_LEG); its exposure in a month is the sum over the month's days of 100 x gross |Amount| of its rows / the previous day's value; it reaches the month when its exposure is at least |D|; the class is the reaching category of the largest exposure. A month where none reaches, or that holds no driver row, is `unexplained:` with what was checked. The value-neutral rows (trades, reinvestments, corporate actions) are not drivers.

Category of every transaction type (61 of 61 types of the flow table's universe; a listed-sweep buy or sell is SWEEP_CASH_LEG):

- CLIENT_FLOW: li, LISU, lo, LIX, LOX, trfi, TRFIR, trci, TRCISU, trfo, trco, si, so, ci
- FEE_DRAG: man, ManAltT, ManCheck, 12b1
- CHARGE_FLOW: fch, genmain, fee, misc, csltfee, pcf, ManAltF, cbf, bcf, stp, term, fco
- TAX: ftax, stax, frntax
- ASF_UNSOURCED: ASF
- INCOME: dv, dvlt, dvst, int, roy, ac, ileu, DVX, INTX, leu, pyd
- NEUTRAL: by, sl, cs, ss, BYX, dvr, DVRX, lica, licar, LICASU, loca, QA, CAF, CAE, acca, accal

## Classes

| class | grade | months | share of non-MATCH | share of total |
|---|---|---|---|---|
| unexplained | DIFF | 512 | 0.64% | 0.62% |
| diff:driver:SWEEP_CASH_LEG | DIFF | 190 | 0.24% | 0.23% |
| diff:driver:INCOME | DIFF | 154 | 0.19% | 0.19% |
| diff:driver:CLIENT_FLOW | DIFF | 30 | 0.04% | 0.04% |
| ungradable:UNPRICED | UNGRADABLE | 74846 | 94.15% | 90.62% |
| ungradable:FIRST_DAY | UNGRADABLE | 1533 | 1.93% | 1.86% |
| ungradable:NON_POSITIVE_BASE | UNGRADABLE | 1173 | 1.48% | 1.42% |
| ungradable:NO_REPORTED_RETURN | UNGRADABLE | 878 | 1.10% | 1.06% |
| ungradable:NO_DAILY_RETURNS | UNGRADABLE | 116 | 0.15% | 0.14% |
| ungradable:REPORTED_SPAN | UNGRADABLE | 63 | 0.08% | 0.08% |

The largest class is `ungradable:UNPRICED` (74846 of 79495 non-MATCH months, 94.2%). A cause that spans every month equally shows as one large class; it is named here and not split further.

## UNGRADABLE months that also carry a reported-side reason (`also`, not a second class)

3848 of 78609 UNGRADABLE months.

- REPORTED_SPAN: 2802
- NO_REPORTED_RETURN: 1023
- REPORTED_ROWS_DISAGREE: 15
- REPORTED_NOT_FINITE: 8

## DIFF months by driver

| class | months | median |D| | max |D| | median top exposure |
|---|---|---|---|---|
| diff:driver:CLIENT_FLOW | 30 | 0.4933 | 110.6667 | 48.6743 |
| diff:driver:INCOME | 154 | 0.1816 | 2.2384 | 0.4756 |
| diff:driver:SWEEP_CASH_LEG | 190 | 0.2007 | 71.4771 | 4.9130 |
| unexplained | 478 | 0.5029 | 279.4650 | 0.0664 |
| unexplained | 34 | 0.2305 | 24.8393 | 0.0000 |

## Unexplained months: 512

| what was checked | grade | months |
|---|---|---|
| unexplained:no driver category reaches |D| (7 categories checked) | DIFF | 478 |
| unexplained:the month holds no row of any of the 7 driver categories | DIFF | 34 |

| account | month | grade | what was checked | detail |
|---|---|---|---|---|
| 0QF878956 | 2021-10 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0001 against |D| 0.1289 pct points |
| 0QF878956 | 2021-11 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.1439 against |D| 0.7391 pct points |
| 0QF878956 | 2021-12 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0937 against |D| 0.7252 pct points |
| 0QF878956 | 2022-01 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0218 against |D| 0.2512 pct points |
| 0QF878956 | 2022-02 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.1154 against |D| 0.5362 pct points |
| 0QF878956 | 2022-04 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0001 against |D| 0.9885 pct points |
| 0QF878956 | 2022-05 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.2194 against |D| 0.3005 pct points |
| 0QF878956 | 2022-06 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.1267 against |D| 5.4844 pct points |
| 0QF878956 | 2022-07 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0014 against |D| 0.3002 pct points |
| 0QF878956 | 2022-09 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.1246 against |D| 0.3696 pct points |
| 0QF878956 | 2022-10 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0026 against |D| 1.3161 pct points |
| 0QF878956 | 2022-12 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.1266 against |D| 0.2139 pct points |
| 0QF878956 | 2023-01 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0298 against |D| 0.1984 pct points |
| 0QF878956 | 2023-02 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.1240 against |D| 0.3000 pct points |
| 0QF878956 | 2023-03 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest SWEEP_CASH_LEG at 0.2886 against |D| 0.4023 pct points |
| 0QF878956 | 2023-04 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest SWEEP_CASH_LEG at 0.0560 against |D| 0.2310 pct points |
| 0QF878956 | 2023-05 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.1412 against |D| 0.5531 pct points |
| 0QF878956 | 2023-07 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest SWEEP_CASH_LEG at 0.0507 against |D| 0.2731 pct points |
| 0QF878956 | 2023-08 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.1334 against |D| 0.3051 pct points |
| 0QF878956 | 2023-10 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest SWEEP_CASH_LEG at 0.0566 against |D| 0.1583 pct points |
| 0QF878956 | 2023-11 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.1832 against |D| 0.4542 pct points |
| 0QF878956 | 2024-01 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest SWEEP_CASH_LEG at 0.0769 against |D| 0.1064 pct points |
| 0QF878956 | 2024-03 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.1808 against |D| 0.3192 pct points |
| 0QF878956 | 2024-04 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest SWEEP_CASH_LEG at 0.1076 against |D| 0.3336 pct points |
| 0QF878956 | 2024-06 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.1236 against |D| 0.1792 pct points |
| 0QF878956 | 2024-07 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest SWEEP_CASH_LEG at 0.0529 against |D| 0.0648 pct points |
| 0QF878956 | 2024-09 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.1193 against |D| 0.2407 pct points |
| 0QF878956 | 2024-10 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest SWEEP_CASH_LEG at 0.0529 against |D| 0.0678 pct points |
| 0QF878956 | 2024-11 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.1181 against |D| 0.1817 pct points |
| 0QF878956 | 2024-12 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0916 against |D| 0.1190 pct points |
| 0QF878956 | 2025-02 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0765 against |D| 0.1208 pct points |
| 0QF878956 | 2025-08 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0840 against |D| 0.1959 pct points |
| 0QF878956 | 2025-11 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0735 against |D| 0.1568 pct points |
| 0QF878956 | 2026-02 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0560 against |D| 0.1332 pct points |
| 0QF878979 | 2020-08 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0003 against |D| 0.1463 pct points |
| 0QF878979 | 2020-09 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.4215 against |D| 0.5038 pct points |
| 0QF878979 | 2020-10 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0004 against |D| 0.0594 pct points |
| 0QF878979 | 2020-11 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest SWEEP_CASH_LEG at 0.1945 against |D| 0.4154 pct points |
| 0QF878979 | 2021-02 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0003 against |D| 0.1479 pct points |
| 0QF878979 | 2021-04 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0003 against |D| 0.1012 pct points |
| 0QF878980 | 2022-07 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest SWEEP_CASH_LEG at 0.0362 against |D| 0.3962 pct points |
| 0QF878980 | 2022-08 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0136 against |D| 0.5243 pct points |
| 0QF878981 | 2020-08 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0001 against |D| 1.7832 pct points |
| 0QF878981 | 2020-10 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0001 against |D| 0.1317 pct points |
| 0QF878981 | 2020-11 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest SWEEP_CASH_LEG at 0.0203 against |D| 1.9137 pct points |
| 0QF878981 | 2021-01 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0001 against |D| 0.2083 pct points |
| 0QF878981 | 2021-02 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0001 against |D| 1.3154 pct points |
| 0QF878981 | 2021-05 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0001 against |D| 1.2756 pct points |
| 0QF878981 | 2021-07 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0001 against |D| 0.1550 pct points |
| 0QF878981 | 2021-08 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0001 against |D| 1.3435 pct points |
| 0QF878981 | 2021-10 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0001 against |D| 0.1726 pct points |
| 0QF878981 | 2021-11 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest SWEEP_CASH_LEG at 0.0114 against |D| 1.2050 pct points |
| 0QF878981 | 2022-01 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0001 against |D| 0.4244 pct points |
| 0QF878981 | 2022-02 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0001 against |D| 0.9613 pct points |
| 0QF878981 | 2022-05 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0001 against |D| 0.8420 pct points |
| 0QF878981 | 2022-07 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0049 against |D| 0.3027 pct points |
| 0QF878981 | 2022-08 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0068 against |D| 0.7777 pct points |
| 0QF878981 | 2022-10 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0070 against |D| 0.5680 pct points |
| 0QF878981 | 2022-11 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0071 against |D| 0.6289 pct points |
| 0QF878981 | 2023-01 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0067 against |D| 0.0748 pct points |
| 0QF878981 | 2023-02 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0062 against |D| 0.6901 pct points |
| 0QF878981 | 2023-05 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0602 against |D| 0.8185 pct points |
| 0QF878981 | 2023-10 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0407 against |D| 0.0732 pct points |
| 0QF878981 | 2023-11 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0403 against |D| 0.8202 pct points |
| 0QF878981 | 2024-02 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0383 against |D| 0.8300 pct points |
| 0QF878981 | 2024-05 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0384 against |D| 0.7240 pct points |
| 0QF878981 | 2024-08 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0471 against |D| 0.7110 pct points |
| 0QF878981 | 2024-11 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0402 against |D| 0.7249 pct points |
| 0QF878981 | 2025-02 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0067 against |D| 0.9017 pct points |
| 0QF878981 | 2025-05 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0476 against |D| 0.7734 pct points |
| 0QF878981 | 2025-08 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0027 against |D| 0.9425 pct points |
| 0QF878981 | 2025-11 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest SWEEP_CASH_LEG at 0.0074 against |D| 0.8763 pct points |
| 0QF878981 | 2026-02 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0016 against |D| 0.7070 pct points |
| 0QF879143 | 2020-08 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.3494 against |D| 1.1340 pct points |
| 0QF879143 | 2020-10 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0001 against |D| 0.1913 pct points |
| 0QF879143 | 2020-11 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest SWEEP_CASH_LEG at 0.4721 against |D| 0.7433 pct points |
| 0QF879143 | 2021-01 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0001 against |D| 0.1625 pct points |
| 0QF879143 | 2021-02 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.3132 against |D| 0.9337 pct points |
| 0QF879143 | 2021-04 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0001 against |D| 0.1273 pct points |
| 0QF879143 | 2021-05 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.2737 against |D| 0.8922 pct points |
| 0QF879143 | 2021-07 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0001 against |D| 0.3227 pct points |
| 0QF879143 | 2021-08 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.2704 against |D| 0.9949 pct points |
| 0QF879143 | 2021-11 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest SWEEP_CASH_LEG at 0.3767 against |D| 1.0028 pct points |
| 0QF879143 | 2022-01 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0001 against |D| 0.0896 pct points |
| 0QF879143 | 2022-02 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.2459 against |D| 0.8930 pct points |
| 0QF879143 | 2022-04 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0003 against |D| 0.2172 pct points |
| 0QF879143 | 2022-08 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.2085 against |D| 0.5424 pct points |
| 0QF879143 | 2022-09 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.5441 against |D| 0.6118 pct points |
| 0QF879143 | 2023-02 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.2114 against |D| 0.4675 pct points |
| 0QF879143 | 2023-05 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.2349 against |D| 0.5613 pct points |
| 0QF879143 | 2023-08 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.2236 against |D| 0.5800 pct points |
| 0QF879143 | 2023-11 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest SWEEP_CASH_LEG at 0.3519 against |D| 0.5808 pct points |
| 0QF879143 | 2024-01 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.4332 against |D| 0.6569 pct points |
| 0QF879143 | 2024-02 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.2473 against |D| 0.5663 pct points |
| 0QF879143 | 2024-05 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.2343 against |D| 0.5944 pct points |
| 0QF879143 | 2024-08 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.2451 against |D| 0.6598 pct points |
| 0QF879143 | 2024-09 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.6275 against |D| 2.7616 pct points |
| 0QF879143 | 2025-01 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0030 against |D| 0.5657 pct points |
| 0QF879143 | 2025-02 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.5805 against |D| 0.6617 pct points |
| 0QF879143 | 2025-04 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0017 against |D| 0.5409 pct points |
| 0QF879143 | 2025-05 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.5741 against |D| 0.6359 pct points |
| 0QF879143 | 2025-07 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0019 against |D| 0.5552 pct points |
| 0QF879143 | 2025-08 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.5403 against |D| 0.6221 pct points |
| 0QF879143 | 2026-01 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0002 against |D| 0.6010 pct points |
| 0QF879143 | 2026-02 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.5171 against |D| 0.6325 pct points |
| 0QF879181 | 2020-08 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0006 against |D| 0.7728 pct points |
| 0QF879181 | 2020-10 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0006 against |D| 0.2171 pct points |
| 0QF879181 | 2020-11 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0006 against |D| 0.0927 pct points |
| 0QF879181 | 2021-01 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0006 against |D| 0.3821 pct points |
| 0QF879181 | 2021-02 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0005 against |D| 0.3541 pct points |
| 0QF879181 | 2021-04 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0005 against |D| 0.1105 pct points |
| 0QF879181 | 2021-05 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0005 against |D| 0.4228 pct points |
| 0QF879181 | 2021-07 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0005 against |D| 0.3617 pct points |
| 0QF879181 | 2021-08 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0005 against |D| 0.7106 pct points |
| 0QF879181 | 2021-10 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0005 against |D| 0.3648 pct points |
| 0QF879181 | 2021-11 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0005 against |D| 0.7364 pct points |
| 0QF879181 | 2022-01 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0005 against |D| 0.8446 pct points |
| 0QF879181 | 2022-02 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0004 against |D| 0.3535 pct points |
| 0QF879181 | 2022-04 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0004 against |D| 0.1075 pct points |
| 0QF879181 | 2022-05 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0004 against |D| 0.0763 pct points |
| 0QF879181 | 2022-07 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0068 against |D| 0.4147 pct points |
| 0QF879181 | 2022-08 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0114 against |D| 0.5012 pct points |
| 0QF879181 | 2022-10 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0126 against |D| 0.7894 pct points |
| 0QF879181 | 2022-11 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0127 against |D| 0.3933 pct points |
| 0QF879181 | 2023-01 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0207 against |D| 0.1413 pct points |
| 0QF879181 | 2023-02 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0189 against |D| 0.5204 pct points |
| 0QF879181 | 2023-04 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest SWEEP_CASH_LEG at 0.0514 against |D| 0.2008 pct points |
| 0QF879181 | 2023-05 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0324 against |D| 0.7383 pct points |
| 0QF879181 | 2023-08 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0314 against |D| 0.3401 pct points |
| 0QF879181 | 2023-10 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest SWEEP_CASH_LEG at 0.0543 against |D| 0.2073 pct points |
| 0QF879181 | 2023-11 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0316 against |D| 0.5020 pct points |
| 0QF879181 | 2024-01 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest SWEEP_CASH_LEG at 0.0512 against |D| 0.0570 pct points |
| 0QF879181 | 2024-02 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0303 against |D| 0.4245 pct points |
| 0QF879181 | 2024-05 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0310 against |D| 0.4352 pct points |
| 0QF879181 | 2024-08 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0304 against |D| 0.4217 pct points |
| 0QF879181 | 2024-11 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0296 against |D| 0.4181 pct points |
| 0QF879181 | 2025-02 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0129 against |D| 0.4171 pct points |
| 0QF879181 | 2025-04 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest SWEEP_CASH_LEG at 0.0553 against |D| 0.0932 pct points |
| 0QF879181 | 2025-05 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0109 against |D| 0.4638 pct points |
| 0QF879181 | 2025-08 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0104 against |D| 0.4657 pct points |
| 0QF879181 | 2025-11 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0047 against |D| 0.4421 pct points |
| 0QF879181 | 2026-02 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0016 against |D| 0.3921 pct points |
| 0QF879353 | 2021-01 | DIFF | unexplained:the month holds no row of any of the 7 driver categories | |D| 0.0587 pct points |
| 0QF879353 | 2021-02 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest SWEEP_CASH_LEG at 0.0660 against |D| 0.2591 pct points |
| 0QF879353 | 2021-03 | DIFF | unexplained:the month holds no row of any of the 7 driver categories | |D| 0.0830 pct points |
| 0QF879353 | 2021-04 | DIFF | unexplained:the month holds no row of any of the 7 driver categories | |D| 0.0978 pct points |
| 0QF879353 | 2021-05 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest SWEEP_CASH_LEG at 0.0662 against |D| 0.1619 pct points |
| 0QF879353 | 2021-06 | DIFF | unexplained:the month holds no row of any of the 7 driver categories | |D| 0.1235 pct points |
| 0QF879353 | 2021-07 | DIFF | unexplained:the month holds no row of any of the 7 driver categories | |D| 0.0608 pct points |
| 0QF879353 | 2021-09 | DIFF | unexplained:the month holds no row of any of the 7 driver categories | |D| 0.0543 pct points |
| 0QF879353 | 2021-10 | DIFF | unexplained:the month holds no row of any of the 7 driver categories | |D| 0.0689 pct points |
| 0QF879353 | 2022-02 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest SWEEP_CASH_LEG at 0.0602 against |D| 0.1200 pct points |
| 0QF879353 | 2022-04 | DIFF | unexplained:the month holds no row of any of the 7 driver categories | |D| 0.0682 pct points |
| 0QF879353 | 2022-06 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0001 against |D| 0.0981 pct points |
| 0QF879353 | 2022-07 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0002 against |D| 0.0557 pct points |
| 0QF879353 | 2023-01 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0007 against |D| 0.0622 pct points |
| 0QF879353 | 2023-03 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0008 against |D| 0.0690 pct points |
| 0QF879353 | 2023-05 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0749 against |D| 0.0869 pct points |
| 0QF879353 | 2024-02 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0723 against |D| 0.0971 pct points |
| 0QF879353 | 2025-05 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0777 against |D| 0.1002 pct points |
| 0QF879353 | 2025-08 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0705 against |D| 0.0812 pct points |
| 0QF879518 | 2021-01 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0001 against |D| 0.2524 pct points |
| 0QF880373 | 2022-03 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.2669 against |D| 0.9314 pct points |
| 0QF880373 | 2022-04 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest SWEEP_CASH_LEG at 0.1177 against |D| 0.3637 pct points |
| 0QF880373 | 2022-05 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0003 against |D| 0.9809 pct points |
| 0QF880373 | 2022-06 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 2.8986 against |D| 3.1356 pct points |
| 0QF880373 | 2022-08 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0007 against |D| 0.4582 pct points |
| 0QF880373 | 2022-10 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest SWEEP_CASH_LEG at 0.1170 against |D| 0.4361 pct points |
| 0QF880373 | 2022-11 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest SWEEP_CASH_LEG at 0.0594 against |D| 0.4895 pct points |
| 0QF880373 | 2023-01 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest SWEEP_CASH_LEG at 0.1059 against |D| 0.2146 pct points |
| 0QF880373 | 2023-02 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0046 against |D| 0.2211 pct points |
| 0QF880373 | 2023-03 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.2823 against |D| 0.3155 pct points |
| 0QF880382 | 2021-05 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0001 against |D| 0.0921 pct points |
| 0QF880382 | 2021-06 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.2914 against |D| 0.4130 pct points |
| 0QF880382 | 2021-10 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0000 against |D| 0.0838 pct points |
| 0QF880382 | 2021-11 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0000 against |D| 0.0684 pct points |
| 0QF880382 | 2022-01 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0008 against |D| 0.0986 pct points |
| 0QF880382 | 2022-03 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.2633 against |D| 0.3119 pct points |
| 0QF880382 | 2022-04 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0000 against |D| 0.0776 pct points |
| 0QF880382 | 2022-07 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0005 against |D| 0.0865 pct points |
| 0QF880382 | 2022-11 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0011 against |D| 0.1159 pct points |
| 0QF880382 | 2023-03 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.3510 against |D| 0.4098 pct points |
| 0QF880382 | 2023-05 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0013 against |D| 0.0965 pct points |
| 0QF880382 | 2023-06 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.3693 against |D| 0.4458 pct points |
| 0QF880382 | 2023-09 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.1320 against |D| 0.4239 pct points |
| 0QF880382 | 2023-12 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.5934 against |D| 0.6237 pct points |
| 0QF880382 | 2024-06 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.3190 against |D| 0.3977 pct points |
| 0QF880382 | 2024-09 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.3021 against |D| 0.3301 pct points |
| 0QF880382 | 2024-12 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.5346 against |D| 0.5364 pct points |
| 0QF880382 | 2025-06 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.3518 against |D| 0.3768 pct points |
| 0QF880382 | 2025-09 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.3084 against |D| 0.3202 pct points |
| 0QF880382 | 2025-12 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.5376 against |D| 0.5384 pct points |
| 0QF880505 | 2020-10 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0803 against |D| 0.1280 pct points |
| 0QF880505 | 2021-02 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0666 against |D| 0.0940 pct points |
| 0QF880505 | 2021-03 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.2762 against |D| 0.2879 pct points |
| 0QF880505 | 2021-04 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0876 against |D| 0.1018 pct points |
| 0QF880505 | 2021-08 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0605 against |D| 0.0760 pct points |
| 0QF880505 | 2021-10 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0581 against |D| 0.0946 pct points |
| 0QF880505 | 2022-01 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0482 against |D| 0.0532 pct points |
| 0QF880505 | 2022-02 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0601 against |D| 0.0886 pct points |
| 0QF880505 | 2022-03 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.2865 against |D| 0.2916 pct points |
| 0QF880505 | 2022-07 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0734 against |D| 0.1239 pct points |
| 0QF880505 | 2022-08 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0727 against |D| 0.0732 pct points |
| 0QF880505 | 2022-10 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0790 against |D| 0.1632 pct points |
| 0QF880505 | 2023-12 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 1.0321 against |D| 1.0595 pct points |
| 0QF880505 | 2024-02 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0927 against |D| 0.1166 pct points |
| 0QF880505 | 2024-03 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.3604 against |D| 0.3785 pct points |
| 0QF880505 | 2024-06 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.5169 against |D| 0.6583 pct points |
| 0QF883352 | 2020-08 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0002 against |D| 1.5479 pct points |
| 0QF883352 | 2020-10 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0003 against |D| 0.2651 pct points |
| 0QF883352 | 2020-11 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0002 against |D| 0.8511 pct points |
| 0QF883352 | 2021-01 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0002 against |D| 0.3876 pct points |
| 0QF883352 | 2021-02 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0002 against |D| 0.4949 pct points |
| 0QF883352 | 2021-04 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0002 against |D| 0.0928 pct points |
| 0QF883352 | 2021-05 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0002 against |D| 1.0101 pct points |
| 0QF883352 | 2021-07 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0002 against |D| 0.2800 pct points |
| 0QF883352 | 2021-08 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0002 against |D| 1.2170 pct points |
| 0QF883352 | 2021-10 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0002 against |D| 0.3053 pct points |
| 0QF883352 | 2021-11 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0002 against |D| 1.1351 pct points |
| 0QF883352 | 2022-01 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0002 against |D| 0.6984 pct points |
| 0QF889506 | 2022-05 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0003 against |D| 0.1006 pct points |
| 0QF889506 | 2022-06 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.6605 against |D| 1.2369 pct points |
| 0QF889506 | 2022-07 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0044 against |D| 0.2654 pct points |
| 0QF889506 | 2022-08 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0077 against |D| 0.1853 pct points |
| 0QF889506 | 2022-09 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.1443 against |D| 0.5274 pct points |
| 0QF889506 | 2022-10 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0091 against |D| 0.3175 pct points |
| 0QF889506 | 2022-11 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest SWEEP_CASH_LEG at 0.2045 against |D| 0.3367 pct points |
| 0QF889506 | 2022-12 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.3987 against |D| 0.4561 pct points |
| 0QF889506 | 2023-01 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0146 against |D| 0.2363 pct points |
| 0QF899639 | 2023-10 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest SWEEP_CASH_LEG at 0.1492 against |D| 2.5278 pct points |
| 0QF899639 | 2023-11 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0013 against |D| 1.1801 pct points |
| 0QF899639 | 2024-02 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0017 against |D| 1.0103 pct points |
| 0QF899639 | 2024-04 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest SWEEP_CASH_LEG at 0.2932 against |D| 2.9841 pct points |
| 0QF899639 | 2024-05 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0800 against |D| 2.0138 pct points |
| 0QF899639 | 2024-06 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.3881 against |D| 0.4002 pct points |
| 0QF899639 | 2024-07 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest SWEEP_CASH_LEG at 0.1445 against |D| 0.2344 pct points |
| 0QF899639 | 2024-08 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0870 against |D| 0.9267 pct points |
| 0QF899639 | 2024-09 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest SWEEP_CASH_LEG at 1.2779 against |D| 2.2764 pct points |
| 0QF899639 | 2024-10 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest SWEEP_CASH_LEG at 0.1562 against |D| 1.4612 pct points |
| 0QF899639 | 2024-11 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.1025 against |D| 0.1297 pct points |
| 0QF911558 | 2020-11 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0003 against |D| 0.7505 pct points |
| 0QF911558 | 2020-12 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0003 against |D| 0.7953 pct points |
| 0QF911558 | 2021-01 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0647 against |D| 0.6623 pct points |
| 0QF911558 | 2021-03 | DIFF | unexplained:the month holds no row of any of the 7 driver categories | |D| 4.3371 pct points |
| 0QF911558 | 2021-04 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest SWEEP_CASH_LEG at 0.0851 against |D| 7.1602 pct points |
| 0QF911558 | 2021-05 | DIFF | unexplained:the month holds no row of any of the 7 driver categories | |D| 5.2008 pct points |
| 0QF911558 | 2021-06 | DIFF | unexplained:the month holds no row of any of the 7 driver categories | |D| 5.4465 pct points |
| 0QF911558 | 2021-07 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest SWEEP_CASH_LEG at 0.0904 against |D| 1.4588 pct points |
| 0QF911558 | 2021-08 | DIFF | unexplained:the month holds no row of any of the 7 driver categories | |D| 2.7005 pct points |
| 0QF911558 | 2021-09 | DIFF | unexplained:the month holds no row of any of the 7 driver categories | |D| 3.2421 pct points |
| 0QF911558 | 2021-10 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest SWEEP_CASH_LEG at 0.0988 against |D| 3.7751 pct points |
| 0QF911558 | 2021-11 | DIFF | unexplained:the month holds no row of any of the 7 driver categories | |D| 2.5656 pct points |
| 0QF911558 | 2021-12 | DIFF | unexplained:the month holds no row of any of the 7 driver categories | |D| 2.0420 pct points |
| 0QF911558 | 2022-01 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest SWEEP_CASH_LEG at 0.1307 against |D| 0.5564 pct points |
| 0QF911558 | 2022-02 | DIFF | unexplained:the month holds no row of any of the 7 driver categories | |D| 0.4592 pct points |
| 0QF911558 | 2022-03 | DIFF | unexplained:the month holds no row of any of the 7 driver categories | |D| 0.1304 pct points |
| 0QF911558 | 2022-04 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest SWEEP_CASH_LEG at 0.0960 against |D| 8.6932 pct points |
| 0QF911558 | 2022-05 | DIFF | unexplained:the month holds no row of any of the 7 driver categories | |D| 0.4784 pct points |
| 0QF911558 | 2022-06 | DIFF | unexplained:the month holds no row of any of the 7 driver categories | |D| 24.8393 pct points |
| 0QF911558 | 2022-07 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0781 against |D| 32.1353 pct points |
| 0QF911558 | 2022-09 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0002 against |D| 0.0718 pct points |
| 0QF911558 | 2023-01 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0906 against |D| 0.1252 pct points |
| 0QF911558 | 2023-06 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0010 against |D| 0.1078 pct points |
| 0QF911558 | 2023-09 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0011 against |D| 0.0846 pct points |
| 0QF911558 | 2023-12 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0011 against |D| 0.1208 pct points |
| 0QF911558 | 2024-03 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0010 against |D| 0.0871 pct points |
| 0QF911558 | 2024-06 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0408 against |D| 0.1509 pct points |
| 0QF911558 | 2024-09 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0418 against |D| 0.1416 pct points |
| 0QF911558 | 2024-12 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0354 against |D| 0.1616 pct points |
| 0QF911558 | 2025-03 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0393 against |D| 0.0984 pct points |
| 0QF924197 | 2022-05 | DIFF | unexplained:the month holds no row of any of the 7 driver categories | |D| 1.1127 pct points |
| 0QF924197 | 2022-08 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0005 against |D| 0.9358 pct points |
| 0QF924197 | 2022-10 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0006 against |D| 0.1005 pct points |
| 0QF924197 | 2022-11 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0007 against |D| 0.7816 pct points |
| 0QF925881 | 2023-06 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0479 against |D| 0.2537 pct points |
| 0QF925881 | 2023-08 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0493 against |D| 0.1406 pct points |
| 0QF925881 | 2023-09 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0481 against |D| 0.2044 pct points |
| 0QF925881 | 2023-12 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.9448 against |D| 1.0010 pct points |
| 0QF925881 | 2024-02 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0478 against |D| 0.0630 pct points |
| 0QF925881 | 2024-03 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0507 against |D| 0.1749 pct points |
| 0QF925881 | 2024-05 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0505 against |D| 0.1402 pct points |
| 0QF925881 | 2024-08 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0498 against |D| 0.1238 pct points |
| 0QF925881 | 2024-09 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0479 against |D| 0.1037 pct points |
| B3S605610 | 2022-12 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.3624 against |D| 0.7993 pct points |
| B3S605610 | 2023-01 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest SWEEP_CASH_LEG at 0.3911 against |D| 2.3928 pct points |
| B3S605610 | 2023-02 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.5215 against |D| 3.9506 pct points |
| B3S605610 | 2023-03 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.3826 against |D| 4.1194 pct points |
| B3S605610 | 2023-04 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest SWEEP_CASH_LEG at 0.4044 against |D| 2.8843 pct points |
| B3S605610 | 2023-06 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.8400 against |D| 2.9767 pct points |
| B3S605610 | 2023-07 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest SWEEP_CASH_LEG at 0.6451 against |D| 2.2885 pct points |
| B3S605610 | 2023-08 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0971 against |D| 0.8949 pct points |
| B3S605610 | 2023-09 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.8811 against |D| 8.0501 pct points |
| B3S605610 | 2023-10 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest SWEEP_CASH_LEG at 0.6041 against |D| 6.9656 pct points |
| B3S605610 | 2023-11 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0974 against |D| 6.0948 pct points |
| B3S605610 | 2024-01 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest SWEEP_CASH_LEG at 0.6448 against |D| 8.7653 pct points |
| B3S605610 | 2024-02 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0918 against |D| 2.8189 pct points |
| B3S605610 | 2024-03 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.7909 against |D| 3.6424 pct points |
| B3S605610 | 2024-04 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest SWEEP_CASH_LEG at 0.6739 against |D| 5.1809 pct points |
| B3S605610 | 2024-05 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0858 against |D| 8.1786 pct points |
| B3S605610 | 2024-06 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.7807 against |D| 3.6163 pct points |
| B3S605610 | 2024-07 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest SWEEP_CASH_LEG at 0.7207 against |D| 2.6774 pct points |
| B3S605610 | 2024-08 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0961 against |D| 6.4651 pct points |
| B3S605610 | 2024-09 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.8855 against |D| 2.7645 pct points |
| B3S605610 | 2024-10 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest SWEEP_CASH_LEG at 0.7502 against |D| 5.3453 pct points |
| B3S605610 | 2024-11 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0935 against |D| 6.8394 pct points |
| B3S605610 | 2025-01 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest SWEEP_CASH_LEG at 0.8440 against |D| 2.7804 pct points |
| B3S605610 | 2025-02 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0772 against |D| 2.5274 pct points |
| B3S605610 | 2025-03 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.7554 against |D| 2.7544 pct points |
| B3S605610 | 2025-04 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest SWEEP_CASH_LEG at 0.9848 against |D| 18.2107 pct points |
| B3S605610 | 2025-05 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0785 against |D| 0.4405 pct points |
| B3S605610 | 2025-06 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.7073 against |D| 2.8850 pct points |
| B3S605610 | 2025-07 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest SWEEP_CASH_LEG at 0.9958 against |D| 8.0999 pct points |
| B3S605610 | 2025-08 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0763 against |D| 2.5290 pct points |
| B3S605610 | 2025-10 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest SWEEP_CASH_LEG at 0.8459 against |D| 3.7054 pct points |
| B3S605610 | 2025-11 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0733 against |D| 279.4650 pct points |
| B3S605610 | 2026-02 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0262 against |D| 0.2423 pct points |
| B3S605713 | 2024-08 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.3026 against |D| 0.4869 pct points |
| B3S605733 | 2024-12 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.2592 against |D| 0.3669 pct points |
| B3S670862 | 2021-06 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 1.1159 against |D| 1.1548 pct points |
| B3S670862 | 2021-11 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest SWEEP_CASH_LEG at 0.1266 against |D| 0.1409 pct points |
| B3S670862 | 2021-12 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 9.9775 against |D| 15.3359 pct points |
| B3S670862 | 2022-03 | DIFF | unexplained:the month holds no row of any of the 7 driver categories | |D| 0.2640 pct points |
| B3S670862 | 2022-05 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0001 against |D| 0.0974 pct points |
| B3S670862 | 2022-06 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 2.0073 against |D| 2.6234 pct points |
| B3S670862 | 2022-08 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0003 against |D| 0.0652 pct points |
| B3S670862 | 2022-11 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest SWEEP_CASH_LEG at 0.1502 against |D| 0.1741 pct points |
| B3S670862 | 2022-12 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 2.5325 against |D| 3.0055 pct points |
| B3S670862 | 2023-03 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0003 against |D| 0.1835 pct points |
| B3S670865 | 2021-06 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 1.1004 against |D| 1.1385 pct points |
| B3S670865 | 2021-12 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 10.0052 against |D| 15.4401 pct points |
| B3S670865 | 2022-03 | DIFF | unexplained:the month holds no row of any of the 7 driver categories | |D| 0.2769 pct points |
| B3S670865 | 2022-05 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0002 against |D| 0.1013 pct points |
| B3S670865 | 2022-06 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 1.9776 against |D| 2.6034 pct points |
| B3S670865 | 2022-08 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0004 against |D| 0.0743 pct points |
| B3S670865 | 2022-12 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 2.4945 against |D| 2.9713 pct points |
| B3S670865 | 2023-03 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0014 against |D| 0.1943 pct points |
| B3S691865 | 2022-11 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0027 against |D| 0.0506 pct points |
| B3S691865 | 2023-01 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.4839 against |D| 0.6409 pct points |
| B3S691865 | 2023-04 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.5528 against |D| 0.6215 pct points |
| B3S691865 | 2023-05 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0043 against |D| 0.0645 pct points |
| B3S691865 | 2023-08 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0042 against |D| 0.0893 pct points |
| B3S691865 | 2023-09 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0235 against |D| 0.1104 pct points |
| B3S691865 | 2023-11 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0048 against |D| 0.1691 pct points |
| B3S691865 | 2024-01 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.4811 against |D| 0.5244 pct points |
| B3S691865 | 2024-02 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0023 against |D| 0.0895 pct points |
| B3S691865 | 2024-05 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0029 against |D| 0.0554 pct points |
| B3S691865 | 2024-07 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.4981 against |D| 0.5002 pct points |
| B3S691865 | 2024-10 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.4303 against |D| 0.4513 pct points |
| B3S691865 | 2025-01 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.3973 against |D| 0.4313 pct points |
| B3S691865 | 2025-10 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.3624 against |D| 0.3647 pct points |
| B3S691865 | 2026-04 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.3131 against |D| 0.3855 pct points |
| B3S703388 | 2020-08 | DIFF | unexplained:the month holds no row of any of the 7 driver categories | |D| 0.2646 pct points |
| B3S703388 | 2020-11 | DIFF | unexplained:the month holds no row of any of the 7 driver categories | |D| 0.2743 pct points |
| B3S703388 | 2021-02 | DIFF | unexplained:the month holds no row of any of the 7 driver categories | |D| 0.2314 pct points |
| B3S703388 | 2021-05 | DIFF | unexplained:the month holds no row of any of the 7 driver categories | |D| 0.2296 pct points |
| B3S703388 | 2021-08 | DIFF | unexplained:the month holds no row of any of the 7 driver categories | |D| 0.1978 pct points |
| B3S703388 | 2021-11 | DIFF | unexplained:the month holds no row of any of the 7 driver categories | |D| 0.1822 pct points |
| B3S703388 | 2022-02 | DIFF | unexplained:the month holds no row of any of the 7 driver categories | |D| 0.1995 pct points |
| B3S703388 | 2022-05 | DIFF | unexplained:the month holds no row of any of the 7 driver categories | |D| 0.2276 pct points |
| B3S703388 | 2022-08 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0002 against |D| 0.1941 pct points |
| B3S703388 | 2022-11 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0002 against |D| 0.2959 pct points |
| B3S703388 | 2023-02 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0006 against |D| 0.2470 pct points |
| B3S703388 | 2023-05 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0009 against |D| 0.2285 pct points |
| B3S703388 | 2023-08 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0010 against |D| 0.2051 pct points |
| B3S703388 | 2023-11 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0010 against |D| 0.2205 pct points |
| B3S703388 | 2024-02 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0009 against |D| 0.1891 pct points |
| B3S703388 | 2024-08 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0013 against |D| 0.1739 pct points |
| B3S703388 | 2024-11 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0012 against |D| 0.2023 pct points |
| B3S703388 | 2025-02 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0005 against |D| 0.1869 pct points |
| B3S728504 | 2022-11 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.1345 against |D| 0.3862 pct points |
| B3S728504 | 2022-12 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 1.1396 against |D| 1.7714 pct points |
| B3S728504 | 2023-01 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest SWEEP_CASH_LEG at 0.4564 against |D| 1.0323 pct points |
| B3S728504 | 2023-02 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.1550 against |D| 0.3428 pct points |
| B3S728504 | 2023-08 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.1503 against |D| 0.3560 pct points |
| B3S728504 | 2023-09 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.8764 against |D| 1.3444 pct points |
| B3S728504 | 2023-11 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.1667 against |D| 0.9105 pct points |
| B3S728504 | 2024-02 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.1728 against |D| 0.5602 pct points |
| B3S728504 | 2024-05 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.1562 against |D| 0.3948 pct points |
| B3S728504 | 2024-10 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest SWEEP_CASH_LEG at 0.4562 against |D| 146.5643 pct points |
| B3S728504 | 2024-11 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0635 against |D| 0.0913 pct points |
| B3S728504 | 2025-05 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0627 against |D| 0.0863 pct points |
| B3S728506 | 2022-11 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.1318 against |D| 0.3766 pct points |
| B3S728506 | 2022-12 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 1.1455 against |D| 1.7755 pct points |
| B3S728506 | 2023-01 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest SWEEP_CASH_LEG at 0.4582 against |D| 1.0285 pct points |
| B3S728506 | 2023-02 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.1519 against |D| 0.3360 pct points |
| B3S728506 | 2023-08 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.1472 against |D| 0.3516 pct points |
| B3S728506 | 2023-09 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.8820 against |D| 1.3463 pct points |
| B3S728506 | 2023-11 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.1632 against |D| 0.9048 pct points |
| B3S728506 | 2024-02 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.1691 against |D| 0.5569 pct points |
| B3S728506 | 2024-05 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.1528 against |D| 0.3921 pct points |
| B3S728506 | 2024-10 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest SWEEP_CASH_LEG at 0.4544 against |D| 147.4985 pct points |
| B3S728506 | 2024-11 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0618 against |D| 0.0820 pct points |
| B3S728506 | 2025-05 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0606 against |D| 0.0852 pct points |
| B3S728793 | 2021-10 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest SWEEP_CASH_LEG at 6.4354 against |D| 12.9292 pct points |
| B3S762431 | 2021-10 | DIFF | unexplained:the month holds no row of any of the 7 driver categories | |D| 0.1030 pct points |
| B3S763288 | 2022-04 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest SWEEP_CASH_LEG at 1.0259 against |D| 3.9200 pct points |
| B3S763288 | 2022-06 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0041 against |D| 36.8512 pct points |
| B3S763288 | 2022-07 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest SWEEP_CASH_LEG at 10.3273 against |D| 34.5617 pct points |
| B3S777026 | 2022-04 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest SWEEP_CASH_LEG at 0.3583 against |D| 1.8110 pct points |
| B3S777026 | 2022-05 | DIFF | unexplained:the month holds no row of any of the 7 driver categories | |D| 0.0585 pct points |
| B3S786844 | 2022-09 | DIFF | unexplained:the month holds no row of any of the 7 driver categories | |D| 0.2279 pct points |
| B3S786844 | 2022-12 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.3063 against |D| 0.3493 pct points |
| B3S793726 | 2025-06 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0104 against |D| 0.2009 pct points |
| B3S793726 | 2025-09 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0215 against |D| 0.0651 pct points |
| B3S793726 | 2025-10 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.2139 against |D| 0.2573 pct points |
| B3S793726 | 2025-11 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest CLIENT_FLOW at 5.5015 against |D| 10.3632 pct points |
| B3S793726 | 2026-02 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest CLIENT_FLOW at 16.2883 against |D| 20.0503 pct points |
| B3S798436 | 2024-08 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.1404 against |D| 0.1442 pct points |
| B3S798436 | 2024-09 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.2356 against |D| 0.2408 pct points |
| B3S798436 | 2024-11 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.1379 against |D| 0.1675 pct points |
| B3S798436 | 2025-05 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.1456 against |D| 0.1630 pct points |
| B3S798436 | 2025-06 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.5066 against |D| 0.5307 pct points |
| B3S798436 | 2025-08 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.1376 against |D| 0.1466 pct points |
| B3S798436 | 2025-09 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.2134 against |D| 0.2280 pct points |
| B3S798436 | 2025-12 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.7192 against |D| 0.7252 pct points |
| B3S798436 | 2026-02 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.1244 against |D| 0.1315 pct points |
| B3S804864 | 2023-09 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.1607 against |D| 0.3919 pct points |
| B3S804888 | 2023-09 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.1606 against |D| 0.3989 pct points |
| B3S804888 | 2024-06 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.3202 against |D| 0.3690 pct points |
| B3S804888 | 2024-09 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.2875 against |D| 0.2935 pct points |
| B3S804888 | 2024-12 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.5442 against |D| 0.5443 pct points |
| B3S804888 | 2025-06 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.2971 against |D| 0.3091 pct points |
| B3S804888 | 2025-09 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.2641 against |D| 0.2717 pct points |
| B3S804888 | 2025-12 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.5492 against |D| 0.5511 pct points |
| D49141619 | 2022-06 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.3947 against |D| 12.1533 pct points |
| D49141619 | 2022-07 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0002 against |D| 4.6619 pct points |
| D49141619 | 2022-08 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0003 against |D| 0.2207 pct points |
| D49141619 | 2022-09 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 1.0647 against |D| 4.7346 pct points |
| D49141619 | 2022-10 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0005 against |D| 14.4884 pct points |
| D49141619 | 2022-11 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest SWEEP_CASH_LEG at 0.0546 against |D| 0.5622 pct points |
| D49141619 | 2022-12 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.4178 against |D| 1.9816 pct points |
| D49141619 | 2023-02 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest SWEEP_CASH_LEG at 0.0365 against |D| 1.2368 pct points |
| D49141619 | 2023-03 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.4519 against |D| 2.1329 pct points |
| D49141619 | 2023-04 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest SWEEP_CASH_LEG at 0.5650 against |D| 3.6920 pct points |
| D49141619 | 2023-05 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0066 against |D| 2.9600 pct points |
| D49141619 | 2023-07 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest SWEEP_CASH_LEG at 0.0527 against |D| 3.0676 pct points |
| D49141619 | 2023-08 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0052 against |D| 2.4018 pct points |
| D49141619 | 2023-10 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest SWEEP_CASH_LEG at 0.0549 against |D| 2.4513 pct points |
| D49141619 | 2023-11 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest SWEEP_CASH_LEG at 0.0584 against |D| 1.1232 pct points |
| D49141619 | 2024-01 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest SWEEP_CASH_LEG at 0.0538 against |D| 1.7791 pct points |
| D49141619 | 2024-02 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0035 against |D| 1.1239 pct points |
| D49141619 | 2024-03 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.4446 against |D| 2.5440 pct points |
| D49141619 | 2024-04 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest SWEEP_CASH_LEG at 0.5735 against |D| 3.4699 pct points |
| D49141619 | 2024-05 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0027 against |D| 1.9910 pct points |
| D49141619 | 2024-07 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest SWEEP_CASH_LEG at 0.0529 against |D| 0.2173 pct points |
| D49141619 | 2024-08 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0007 against |D| 0.5970 pct points |
| D49141619 | 2024-09 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.8081 against |D| 2.1193 pct points |
| D49141619 | 2024-10 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest SWEEP_CASH_LEG at 0.0512 against |D| 1.8099 pct points |
| D49141619 | 2026-02 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0034 against |D| 0.4259 pct points |
| D49143349 | 2022-07 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0002 against |D| 4.4095 pct points |
| D49143349 | 2022-08 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0003 against |D| 0.6747 pct points |
| D49143349 | 2022-09 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.7056 against |D| 5.0168 pct points |
| D49143349 | 2022-10 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0006 against |D| 14.7389 pct points |
| D49143349 | 2022-11 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest SWEEP_CASH_LEG at 0.0399 against |D| 0.5670 pct points |
| D49143349 | 2023-02 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest SWEEP_CASH_LEG at 0.0392 against |D| 1.3655 pct points |
| D49143349 | 2023-03 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.2011 against |D| 3.8265 pct points |
| D49143349 | 2023-04 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest SWEEP_CASH_LEG at 1.8582 against |D| 4.2672 pct points |
| D49143349 | 2023-05 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0176 against |D| 3.5275 pct points |
| D49143349 | 2023-07 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest SWEEP_CASH_LEG at 0.0535 against |D| 4.1678 pct points |
| D49143349 | 2023-08 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0127 against |D| 3.9296 pct points |
| D49143349 | 2023-10 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest SWEEP_CASH_LEG at 0.0551 against |D| 3.3048 pct points |
| D49143349 | 2023-11 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest SWEEP_CASH_LEG at 0.2363 against |D| 0.6996 pct points |
| D49143349 | 2023-12 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.2103 against |D| 0.2396 pct points |
| D49143349 | 2024-01 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest SWEEP_CASH_LEG at 0.0564 against |D| 2.2566 pct points |
| D49143349 | 2024-02 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0078 against |D| 1.1484 pct points |
| D49143349 | 2024-03 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.2087 against |D| 2.0372 pct points |
| D49143349 | 2024-04 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest SWEEP_CASH_LEG at 1.9326 against |D| 5.0239 pct points |
| D49143349 | 2024-05 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0057 against |D| 3.0466 pct points |
| D49143349 | 2024-06 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.1827 against |D| 0.5551 pct points |
| D49143349 | 2024-07 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest SWEEP_CASH_LEG at 0.0530 against |D| 0.3422 pct points |
| D49143349 | 2024-08 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0014 against |D| 0.2822 pct points |
| D49143349 | 2024-09 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 1.4438 against |D| 2.5498 pct points |
| D49143349 | 2024-10 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest SWEEP_CASH_LEG at 0.0536 against |D| 1.5013 pct points |
| D49143349 | 2026-02 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0025 against |D| 0.5260 pct points |
| D49143350 | 2023-10 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest SWEEP_CASH_LEG at 0.1504 against |D| 2.8691 pct points |
| D49143350 | 2023-11 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0064 against |D| 1.1533 pct points |
| D49143350 | 2024-01 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.2230 against |D| 2.1647 pct points |
| D49143350 | 2024-02 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest SWEEP_CASH_LEG at 0.0061 against |D| 1.1775 pct points |
| D49143350 | 2024-04 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.2092 against |D| 4.1471 pct points |
| D49143350 | 2024-05 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0534 against |D| 2.4716 pct points |
| D49143350 | 2024-06 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.4322 against |D| 0.5124 pct points |
| D49143350 | 2024-07 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest SWEEP_CASH_LEG at 0.1593 against |D| 0.3091 pct points |
| D49143350 | 2024-08 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0566 against |D| 1.1104 pct points |
| D49143350 | 2024-09 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.4456 against |D| 2.5737 pct points |
| D49143350 | 2024-10 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest SWEEP_CASH_LEG at 0.1569 against |D| 1.7039 pct points |
| D49143350 | 2024-11 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0444 against |D| 0.0983 pct points |
| D49143350 | 2025-11 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0627 against |D| 0.3444 pct points |
| RGY004120 | 2025-12 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 4.7566 against |D| 9.6355 pct points |
| RGY004120 | 2026-02 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.1737 against |D| 0.3456 pct points |
| RGY004222 | 2024-05 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.2969 against |D| 3.0939 pct points |
| RGY004222 | 2024-06 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.3003 against |D| 1.1512 pct points |
| RGY004222 | 2024-07 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.2975 against |D| 6.3598 pct points |
| RGY004222 | 2024-08 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.3053 against |D| 2.3655 pct points |
| RGY004222 | 2024-09 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.2945 against |D| 5.3309 pct points |
| RGY004222 | 2024-10 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.2956 against |D| 1.4392 pct points |
| RGY004222 | 2024-12 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.2816 against |D| 1.4971 pct points |
| RGY004222 | 2025-02 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.2660 against |D| 3.1694 pct points |
| RGY004222 | 2025-03 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.2986 against |D| 0.6150 pct points |
| RGY004256 | 2024-06 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0234 against |D| 0.5807 pct points |
| RGY004256 | 2024-09 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0266 against |D| 0.6225 pct points |
| RGY005018 | 2024-11 | DIFF | unexplained:the month holds no row of any of the 7 driver categories | |D| 0.8305 pct points |
| RGY005018 | 2025-02 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0002 against |D| 0.9209 pct points |
| RGY005018 | 2025-05 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0003 against |D| 0.8791 pct points |
| RGY005018 | 2025-08 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0005 against |D| 0.9251 pct points |
| RGY005018 | 2025-11 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0003 against |D| 0.8598 pct points |
| RGY005018 | 2026-02 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.0001 against |D| 0.6947 pct points |
| RGY005498 | 2025-12 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 4.7311 against |D| 9.5847 pct points |
| RGY005498 | 2026-02 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.1728 against |D| 0.3394 pct points |
| RGY005715 | 2025-12 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 4.7144 against |D| 9.5450 pct points |
| RGY005715 | 2026-02 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.1721 against |D| 0.3417 pct points |
| RGY006999 | 2025-12 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 4.6777 against |D| 9.4776 pct points |
| RGY006999 | 2026-02 | DIFF | unexplained:no driver category reaches |D| (7 categories checked) | largest INCOME at 0.1709 against |D| 0.3360 pct points |

NONMATCH-CENSUS total=82593 match=3098 diff=886 ungradable=78609 classes=10 unexplained=512
