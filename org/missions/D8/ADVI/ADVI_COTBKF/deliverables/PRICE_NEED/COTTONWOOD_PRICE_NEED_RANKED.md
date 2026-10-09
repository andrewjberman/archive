# Cottonwood price need, ranked (CB-aa-2)

Every non-cash security held on at least one account-day with no price in the default run's day prices (`<data-dir>/after`). Key: Commonwealth 9-character CUSIP as delivered. Full list: `COTTONWOOD_PRICE_NEED_RANKED.csv`.

- securities: 4372 (P1 2155, P2 195, P3 2022; the three sum to 4372)
- covered by the MDPF_DEMQUE store (in the index and its valid range holds the whole held span): 32, ranked last
- unpriced holding days (one per account, day, security): 15986926
- reconcile against the run's account_day_value: 1691729 account-days compared, 0 differ (holdings - priced_holdings vs the unpriced holdings rebuilt here)
- holding accounts not listed by the crosswalk (read P3, nothing invented): 0 security rows touch at least one
- weight_basis: BUY 2832, INBOUND 1428, NONE 112 (NONE = no purchase and no inbound amount: weight 1.0)

Tier (CRO, RESEARCH_20261008 section 6): P1 any holding account MATCHED to a current Cottonwood account; P2 none MATCHED but one AMBIGUOUS or AWAITING_PERSON; P3 otherwise. Holders are the accounts with an unpriced held day on the security. Score = held_days (distinct days held unpriced) x accounts x weight (largest single `by` amount; INBOUND then 1.0 as stated above). BLIND: the crosswalk matches by account, so a living client matched only by name reads P3 (CRO recommendation 4).

## Top 20

| rank | cusip | symbol | tier | score | accounts | unpriced days | first | last | in index | covered |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 13161T401 | CDSIX | P1 | 2,325,210,000,000.00 | 433 | 375936 | 2018-07-16 | 2026-06-05 | False | False |
| 2 | 31617H508 | FZAXX | P1 | 1,140,429,150,322.00 | 25 | 34778 | 2016-01-22 | 2026-06-22 | False | False |
| 3 | 31423A689 | PIUIX | P1 | 301,773,279,570.00 | 383 | 266019 | 2019-11-18 | 2026-05-15 | False | False |
| 4 | 316175108 | FIGXX | P1 | 290,880,000,000.00 | 36 | 7194 | 2023-03-17 | 2026-06-05 | False | False |
| 5 | 31635V729 | FSPGX | P1 | 268,548,567,000.00 | 465 | 266708 | 2018-11-09 | 2026-06-05 | False | False |
| 6 | 31635V679 | FLCOX | P1 | 268,373,767,160.48 | 464 | 264296 | 2018-11-09 | 2026-06-05 | False | False |
| 7 | 464287457 | SHY | P1 | 256,189,572,164.04 | 74 | 22475 | 2013-04-11 | 2020-07-06 | False | False |
| 8 | 921937702 | VBIRX | P1 | 237,985,355,790.00 | 63 | 46643 | 2016-07-07 | 2022-07-07 | False | False |
| 9 | 746745405 | PEIYX | P1 | 157,038,199,500.00 | 415 | 158978 | 2024-08-13 | 2026-06-05 | False | False |
| 10 | 149498107 | CEMIX | P1 | 149,092,442,300.00 | 458 | 394428 | 2021-06-18 | 2026-06-05 | False | False |
| 11 | 277902698 | EISMX | P1 | 122,203,205,280.00 | 403 | 207145 | 2023-02-17 | 2026-05-20 | False | False |
| 12 | 302544101 | FPNIX | P1 | 60,785,572,032.00 | 348 | 273900 | 2019-01-15 | 2023-07-28 | False | False |
| 13 | 38147X705 | GPPIX | P1 | 57,560,000,000.00 | 20 | 6109 | 2020-09-10 | 2026-06-03 | False | False |
| 14 | 92206C409 | VCSH | P1 | 56,830,330,545.82 | 13 | 5120 | 2014-09-16 | 2020-06-29 | False | False |
| 15 | 464287598 | IWD | P1 | 56,459,049,807.70 | 107 | 43915 | 2015-09-25 | 2020-11-25 | False | False |
| 16 | 921937827 | BSV | P1 | 43,783,244,098.00 | 88 | 8337 | 2015-09-25 | 2016-07-11 | False | False |
| 17 | 131649774 | CVMIX | P1 | 40,852,071,000.00 | 306 | 140490 | 2019-01-15 | 2023-11-20 | False | False |
| 18 | 316146315 | FSGGX | P1 | 40,107,802,500.00 | 425 | 238425 | 2023-08-15 | 2026-06-05 | False | False |
| 19 | 46434V407 | SHYG | P1 | 37,467,701,443.20 | 42 | 23993 | 2017-06-23 | 2021-01-07 | False | False |
| 20 | 31617L798 | FBKWX | P1 | 34,437,852,000.00 | 72 | 5026 | 2021-05-06 | 2026-06-03 | False | False |
