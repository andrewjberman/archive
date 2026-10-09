# Commonwealth mover classes (CB-t-1)

The movers are the (account, month) rows graded MATCH in the persisted BEFORE grades (list `none`) and DIFF in the persisted AFTER grades (list `sweeps-v1-20261008`). Each is classed by its account's holdings on or before the month's last day: `core` holds 316067107 (Fidelity Government Cash Reserves); `other_mmf` holds another of the 22 CUSIPs `CANDIDATES_REJECTED` lists with class MMF (316067107 itself excepted); `neither`. Both core and other_mmf is core. Holding = a silver transaction row in the CUSIP with Trade_Date on or before the month's last day.

Persisted grades read: 82593 BEFORE rows, 82593 AFTER rows. Movers: 163.

| class | months |
|---|---|
| core | 16 |
| other_mmf | 0 |
| neither | 147 |
| total | 163 |

## Every mover, named

| account | month | before return (pct) | after return (pct) | reported (pct) | class | MMF CUSIPs held |
|---|---|---|---|---|---|---|
| acct#f6c79f45 | 2024-06 | -0.8874 | 1.2105 | -0.88 | core | 922906201 |
| acct#9727ac87 | 2024-07 | -0.0415 | -0.0234 | -0.08 | core |  |
| D49143350 | 2023-11 | -4.6175 | -5.3344 | -4.59 | core |  |
| D49143350 | 2026-02 | 2.0179 | -16.069 | 2.05 | core |  |
| acct#557ce060 | 2026-01 | 0.0118 | 0.0988 | 0.02 | core |  |
| acct#c0cea213 | 2024-10 | 0.0329 | 0.1609 | -0.0 | core |  |
| acct#7f62f16f | 2025-02 | 0.0995 | 0.1518 | 0.06 | core |  |
| acct#61ebda90 | 2025-04 | 0.0436 | 95.1114 | 0.09 | core |  |
| acct#ce1f487c | 2025-04 | 0.0436 | 95.1114 | 0.09 | core |  |
| acct#16bf540c | 2025-04 | 0.0436 | 95.1114 | 0.09 | core |  |
| acct#177b7e48 | 2025-04 | 0.0436 | 95.1114 | 0.09 | core |  |
| acct#aed810ab | 2025-04 | 0.0436 | 95.1116 | 0.09 | core |  |
| acct#781a748b | 2025-04 | 0.0436 | 95.1114 | 0.09 | core |  |
| acct#1b22f63a | 2025-04 | 0.0436 | 95.1114 | 0.09 | core |  |
| acct#744c9c00 | 2025-06 | 0.1042 | 99.2457 | 0.15 | core |  |
| acct#5fd6a5d4 | 2026-05 | 0.0283 | 0.265 | 0.03 | core |  |
| acct#aaeb760c | 2021-10 | 5.4855 | 6.0313 | 5.51 | neither |  |
| acct#aaeb760c | 2022-03 | 4.7791 | 5.0603 | 4.82 | neither |  |
| acct#aaeb760c | 2022-08 | -1.0435 | -1.3538 | -1.06 | neither |  |
| acct#aaeb760c | 2023-12 | 1.5886 | 1.6144 | 1.56 | neither |  |
| acct#aaeb760c | 2025-03 | -7.1874 | -7.4127 | -7.16 | neither |  |
| acct#b4db1f25 | 2020-01 | 0.0169 | 0.0835 | 0.02 | neither |  |
| acct#b4db1f25 | 2020-02 | 0.0158 | 0.0781 | 0.02 | neither |  |
| acct#b4db1f25 | 2020-11 | 0.0654 | 0.0034 | 0.08 | neither |  |
| acct#03836058 | 2022-04 | -1.3963 | -2.7833 | -1.41 | neither |  |
| acct#eea1157e | 2021-05 | 0.7731 | 1.3492 | 0.76 | neither |  |
| acct#eea1157e | 2022-12 | 0.0072 | -0.5123 | -0.04 | neither |  |
| acct#eea1157e | 2023-07 | -0.0182 | 0.0314 | -0.02 | neither |  |
| acct#eea1157e | 2024-09 | 0.1142 | -0.3309 | 0.13 | neither |  |
| acct#eea1157e | 2025-08 | 1.2591 | 1.974 | 1.22 | neither |  |
| acct#1c3da532 | 2017-08 | 0.0039 | 0.0503 | 0.0 | neither |  |
| acct#1c3da532 | 2017-10 | 0.0039 | 0.0502 | 0.0 | neither |  |
| acct#1c3da532 | 2017-12 | 0.0039 | 0.0502 | 0.0 | neither |  |
| acct#1c3da532 | 2018-01 | 0.0112 | 0.1447 | 0.01 | neither |  |
| acct#1c3da532 | 2018-02 | 0.0106 | 0.1363 | 0.01 | neither |  |
| acct#1c3da532 | 2018-03 | 0.013 | 0.1669 | 0.01 | neither |  |
| acct#5aa91f68 | 2017-07 | 0.002 | 0.093 | 0.0 | neither |  |
| acct#5aa91f68 | 2017-08 | 0.0042 | 0.1956 | 0.0 | neither |  |
| acct#5aa91f68 | 2017-09 | 0.0039 | 0.1854 | 0.0 | neither |  |
| acct#5aa91f68 | 2017-10 | 0.0042 | 0.1948 | 0.0 | neither |  |
| acct#5aa91f68 | 2017-12 | 0.0041 | 0.1892 | 0.0 | neither |  |
| acct#5aa91f68 | 2018-01 | 0.0119 | 0.5521 | 0.01 | neither |  |
| acct#5aa91f68 | 2018-02 | 0.0112 | 0.5201 | 0.01 | neither |  |
| acct#5aa91f68 | 2018-03 | 0.0137 | 0.6324 | 0.01 | neither |  |
| acct#5aa91f68 | 2018-04 | 0.0201 | 0.9189 | 0.02 | neither |  |
| acct#5aa91f68 | 2018-05 | 0.0207 | 0.9388 | 0.02 | neither |  |
| acct#5aa91f68 | 2018-06 | 0.0201 | 0.902 | 0.02 | neither |  |
| acct#04ebe1d1 | 2021-04 | -3.4508 | -3.4979 | -3.41 | neither |  |
| acct#04ebe1d1 | 2021-06 | -4.8644 | -4.9327 | -4.82 | neither |  |
| acct#04ebe1d1 | 2021-10 | -1.4342 | -1.4564 | -1.39 | neither |  |
| acct#04ebe1d1 | 2024-05 | 0.6758 | 0.6079 | 0.67 | neither |  |
| acct#015306a0 | 2023-04 | 1.2331 | 1.1523 | 1.23 | neither |  |
| acct#fa488a0b | 2021-04 | 2.2439 | 2.2794 | 2.21 | neither |  |
| acct#fa488a0b | 2021-08 | 1.0456 | 1.0615 | 1.0 | neither |  |
| acct#fa488a0b | 2021-10 | 2.5402 | 2.5791 | 2.52 | neither |  |
| acct#fa488a0b | 2023-04 | 1.0012 | 1.1639 | 1.0 | neither |  |
| acct#fa488a0b | 2023-07 | 2.9077 | 3.0773 | 2.9 | neither |  |
| acct#fa488a0b | 2024-01 | -0.9005 | -1.1563 | -0.95 | neither |  |
| acct#21515eb6 | 2025-04 | 0.5019 | 0.8003 | 0.53 | neither |  |
| acct#21515eb6 | 2025-05 | 8.2042 | 8.2754 | 8.21 | neither |  |
| acct#2d4385bf | 2022-03 | 4.9078 | 4.9714 | 4.92 | neither |  |
| acct#2d4385bf | 2023-04 | -1.0474 | -1.1362 | -1.04 | neither |  |
| acct#ab0c6781 | 2018-01 | 0.1777 | 0.5903 | 0.18 | neither |  |
| acct#ab0c6781 | 2018-02 | 0.0113 | 0.5544 | 0.01 | neither |  |
| acct#ab0c6781 | 2018-03 | 0.0138 | 0.6766 | 0.01 | neither |  |
| acct#92164e0d | 2017-03 | -0.0454 | 0.0008 | -0.09 | neither |  |
| acct#ebb31a1c | 2017-03 | -0.0465 | 0.0008 | -0.09 | neither |  |
| acct#dfa7a25c | 2017-06 | -0.051 | 0.0008 | -0.1 | neither |  |
| acct#4040a6ea | 2017-09 | -0.0372 | 0.0041 | -0.07 | neither |  |
| acct#0e2c97b9 | 2018-07 | -0.0404 | 0.0476 | -0.08 | neither |  |
| acct#de79caf1 | 2018-07 | -0.0404 | 0.0476 | -0.08 | neither |  |
| acct#25880078 | 2021-07 | -0.0173 | -0.7036 | -0.04 | neither |  |
| acct#25880078 | 2022-01 | -9.669 | -9.3296 | -9.71 | neither |  |
| acct#25880078 | 2023-04 | 0.6165 | 0.9938 | 0.65 | neither |  |
| acct#8680d8f4 | 2018-06 | -0.0406 | 0.044 | -0.08 | neither |  |
| acct#e29efebe | 2020-10 | -4.0428 | -3.7118 | -4.06 | neither |  |
| acct#e29efebe | 2020-12 | 4.1387 | 3.8748 | 4.15 | neither |  |
| acct#e29efebe | 2021-01 | 3.8931 | 4.262 | 3.93 | neither |  |
| acct#e29efebe | 2021-03 | 1.6982 | 1.45 | 1.7 | neither |  |
| acct#e29efebe | 2021-09 | -6.3785 | -6.5812 | -6.42 | neither |  |
| acct#e29efebe | 2021-12 | 1.913 | 1.7259 | 1.91 | neither |  |
| acct#e29efebe | 2022-03 | 3.3653 | 3.1712 | 3.37 | neither |  |
| acct#e29efebe | 2022-06 | -5.2245 | -5.5037 | -5.26 | neither |  |
| acct#e29efebe | 2022-12 | -5.6204 | -5.9713 | -5.66 | neither |  |
| acct#e29efebe | 2023-04 | 6.4297 | 6.5457 | 6.46 | neither |  |
| acct#e29efebe | 2023-12 | -0.5243 | -0.7259 | -0.55 | neither |  |
| acct#e29efebe | 2024-02 | 4.0017 | 4.0695 | 3.97 | neither |  |
| acct#e29efebe | 2024-12 | -0.2414 | -0.431 | -0.26 | neither |  |
| acct#79d02c2c | 2023-05 | 0.1307 | 0.0043 | 0.1 | neither |  |
| acct#79d02c2c | 2024-07 | 1.9751 | 1.8241 | 1.94 | neither |  |
| acct#79d02c2c | 2024-11 | 5.3014 | 5.5761 | 5.35 | neither |  |
| acct#79d02c2c | 2025-01 | 2.1652 | 2.4415 | 2.21 | neither |  |
| acct#4a890dd1 | 2023-05 | 0.1379 | 0.0153 | 0.11 | neither |  |
| acct#4a890dd1 | 2024-07 | 1.9836 | 1.8256 | 1.94 | neither |  |
| acct#4a890dd1 | 2025-01 | 2.1802 | 2.4546 | 2.23 | neither |  |
| acct#4a890dd1 | 2025-05 | 4.8549 | 5.0695 | 4.83 | neither |  |
| acct#3b89d062 | 2022-07 | -0.0493 | 0.0319 | -0.08 | neither |  |
| acct#3b89d062 | 2022-10 | -0.0518 | 0.0829 | -0.07 | neither |  |
| acct#3b89d062 | 2022-11 | 0.0247 | 0.0848 | 0.03 | neither |  |
| acct#3b89d062 | 2022-12 | 0.0452 | 0.1552 | 0.06 | neither |  |
| acct#3b89d062 | 2023-01 | -0.0259 | 0.1549 | -0.04 | neither |  |
| acct#3b89d062 | 2023-02 | 0.0409 | 0.1398 | 0.06 | neither |  |
| acct#6acbfb93 | 2021-06 | -0.0468 | 0.0008 | -0.09 | neither |  |
| acct#921b5169 | 2022-04 | -0.0299 | 0.0007 | -0.06 | neither |  |
| acct#921b5169 | 2022-07 | -0.0241 | 0.0118 | -0.05 | neither |  |
| acct#921b5169 | 2023-04 | -0.0002 | 0.0611 | -0.0 | neither |  |
| acct#921b5169 | 2023-07 | 0.0006 | 0.0631 | 0.0 | neither |  |
| acct#921b5169 | 2023-10 | -0.0011 | 0.063 | -0.0 | neither |  |
| acct#921b5169 | 2024-01 | -0.0002 | 0.0628 | -0.0 | neither |  |
| acct#921b5169 | 2024-04 | -0.0051 | 0.0605 | -0.01 | neither |  |
| acct#921b5169 | 2024-07 | -0.0052 | 0.0624 | -0.01 | neither |  |
| acct#921b5169 | 2024-10 | -0.0059 | 0.0618 | -0.01 | neither |  |
| acct#921b5169 | 2025-01 | -0.0178 | 0.0359 | -0.04 | neither |  |
| acct#921b5169 | 2025-04 | -0.0294 | 0.0172 | -0.06 | neither |  |
| acct#3345c43a | 2023-01 | -0.029 | 0.1934 | -0.06 | neither |  |
| acct#3345c43a | 2023-04 | -0.028 | 0.1797 | -0.06 | neither |  |
| acct#3345c43a | 2023-07 | -0.0366 | 0.1546 | -0.07 | neither |  |
| acct#3345c43a | 2023-10 | -0.0428 | 0.1575 | -0.09 | neither |  |
| acct#1f02bee1 | 2022-10 | 11.8922 | 11.5015 | 11.87 | neither |  |
| acct#1f02bee1 | 2022-11 | 18.2894 | 18.3535 | 18.29 | neither |  |
| acct#16f4eae3 | 2025-01 | 0.9233 | 1.3343 | 0.92 | neither |  |
| acct#16f4eae3 | 2026-01 | 1.6752 | 2.1165 | 1.68 | neither |  |
| acct#0f2d2c45 | 2024-01 | -0.2815 | 0.0268 | -0.3 | neither |  |
| acct#cce589ab | 2024-01 | -0.2804 | 0.028 | -0.3 | neither |  |
| acct#cce589ab | 2024-02 | 4.2779 | 4.813 | 4.32 | neither |  |
| acct#cce589ab | 2024-04 | -3.9239 | -4.0511 | -3.96 | neither |  |
| acct#cce589ab | 2024-08 | 1.7636 | 1.9586 | 1.79 | neither |  |
| acct#cce589ab | 2024-10 | -1.5618 | -1.4023 | -1.6 | neither |  |
| acct#cce589ab | 2024-11 | 5.213 | 5.7813 | 5.25 | neither |  |
| acct#cce589ab | 2025-01 | 2.481 | 3.0843 | 2.52 | neither |  |
| acct#cce589ab | 2025-02 | -1.5551 | -1.7189 | -1.55 | neither |  |
| acct#cce589ab | 2025-04 | -0.0504 | 0.2743 | -0.05 | neither |  |
| acct#cce589ab | 2025-07 | 1.2346 | 1.6808 | 1.24 | neither |  |
| acct#cce589ab | 2025-08 | 2.4854 | 2.7275 | 2.52 | neither |  |
| acct#cce589ab | 2025-10 | 1.4272 | 1.8756 | 1.44 | neither |  |
| acct#cce589ab | 2026-01 | 1.738 | 2.218 | 1.76 | neither |  |
| D49141608 | 2019-02 | 0.0412 | 2.2299 | 0.04 | neither |  |
| D49141608 | 2019-03 | 0.0457 | 2.4237 | 0.05 | neither |  |
| D49141608 | 2019-04 | 0.0443 | 2.2953 | 0.05 | neither |  |
| D49141608 | 2019-05 | 0.0457 | 2.3132 | 0.05 | neither |  |
| D49141608 | 2019-06 | 0.0443 | 2.1931 | 0.05 | neither |  |
| D49141608 | 2019-07 | 0.0456 | 2.2124 | 0.05 | neither |  |
| D49141608 | 2019-08 | 0.0374 | 1.7749 | 0.04 | neither |  |
| D49141608 | 2019-09 | 0.0315 | 1.4675 | 0.03 | neither |  |
| D49141714 | 2019-02 | 0.0416 | 3.3111 | 0.04 | neither |  |
| acct#a011b5f7 | 2025-04 | 0.4142 | 0.3581 | 0.41 | neither |  |
| acct#a011b5f7 | 2025-10 | 0.6038 | 1.0099 | 0.64 | neither |  |
| acct#a011b5f7 | 2026-01 | 1.5626 | 1.934 | 1.56 | neither |  |
| acct#cf292cea | 2024-07 | -7.7261 | -8.3764 | -7.76 | neither |  |
| acct#cf292cea | 2024-08 | 4.6488 | 4.6829 | 4.62 | neither |  |
| acct#cf292cea | 2024-10 | -8.9903 | -9.7576 | -9.03 | neither |  |
| acct#65b3b3ea | 2024-12 | -7.9838 | -8.8079 | -8.02 | neither |  |
| acct#65b3b3ea | 2025-03 | 7.684 | 6.8268 | 7.66 | neither |  |
| acct#65b3b3ea | 2025-04 | -11.0556 | -11.1826 | -11.06 | neither |  |
| acct#65b3b3ea | 2025-06 | 6.2553 | 5.3767 | 6.23 | neither |  |
| acct#65b3b3ea | 2025-07 | 3.4191 | 3.5626 | 3.42 | neither |  |
| acct#65b3b3ea | 2025-09 | -0.4562 | -1.3469 | -0.47 | neither |  |
| acct#65b3b3ea | 2025-10 | 1.3311 | 1.4283 | 1.33 | neither |  |
| acct#65b3b3ea | 2025-12 | 4.5619 | 3.813 | 4.56 | neither |  |
| acct#65b3b3ea | 2026-01 | 16.7871 | 17.4998 | 16.79 | neither |  |
| acct#65b3b3ea | 2026-03 | 11.5754 | 11.2522 | 11.58 | neither |  |
| acct#65b3b3ea | 2026-04 | -8.7931 | -9.0353 | -8.79 | neither |  |
| acct#ed5f47fe | 2026-01 | 2.7564 | 3.0739 | 2.76 | neither |  |

MOVER-CLASSES movers=163 core=16 other_mmf=0 neither=147 sum_ok=True
