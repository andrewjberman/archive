# FAILING_FUNDS (round 77, CB-by-2)

All 15 failing funds have an unadjusted Close held in the local vendor cache (none in the round-74 fetch folder, none missing). Read against the price paid with the round-76 rule as written, 14 of 15 held series pass and 1 (VGHAX, 5 trade units) is too_few; none fails. The plain within-1-percent share is 1.0 for 9 funds and between 0.62 and 0.98 for 5 (VEIRX 0.785, PCBIX 0.976, SGIIX 0.913, PRILX 0.615, AGTHX 0.700); VGHAX 0.2 of 5 units. Round-76 trade-unit counts are reproduced exactly for 15 of 15.

Nothing was fetched: no network, vendor or bucket call. Written 2026-10-11T23:53:42Z.

| ticker | units | failing | median ratio | held | covers | held-day share (all / trading) | within 1% | class | validated |
|---|---|---|---|---|---|---|---|---|---|
| VEIRX | 1596 | 1596 | 0.626575 | cache | 2020-06-29 to 2026-10-08 | 0.7018 / 1.0 | 0.7851 | passes | validated |
| PCBIX | 1453 | 1426 | 0.748864 | cache | 2020-06-29 to 2026-10-08 | 0.7007 / 1.0 | 0.9759 | passes | unreadable |
| ABNFX | 195 | 177 | 0.856716 | cache | 2020-06-29 to 2026-10-08 | 0.6992 / 1.0 | 1.0 | passes | validated |
| SGIIX | 46 | 40 | 0.742176 | cache | 2020-06-29 to 2026-10-08 | 0.6946 / 1.0 | 0.913 | passes | unreadable |
| GFFFX | 35 | 34 | 0.67923 | cache | 2020-06-29 to 2026-10-08 | 0.6995 / 1.0 | 1.0 | passes | unreadable |
| FOCPX | 25 | 25 | 0.639107 | cache | 2020-06-29 to 2026-10-08 | 0.6901 / 1.0 | 1.0 | passes | unreadable |
| FCNTX | 21 | 15 | 0.909629 | cache | 2020-06-29 to 2026-10-08 | 0.6942 / 1.0 | 1.0 | passes | validated |
| PRILX | 13 | 13 | 0.415777 | cache | 2020-06-29 to 2026-10-08 | 0.6865 / 1.0 | 0.6154 | passes | validated |
| BALCX | 12 | 12 | 0.75864 | cache | 2020-06-29 to 2026-10-08 | 0.6861 / 1.0 | 1.0 | passes | validated |
| AGTHX | 10 | 10 | 0.464906 | cache | 2020-06-29 to 2026-10-08 | 0.699 / 1.0 | 0.7 | passes | unreadable |
| DISVX | 6 | 6 | 0.810315 | cache | 2020-06-29 to 2026-10-08 | 0.6873 / 1.0 | 1.0 | passes | validated |
| DFLVX | 7 | 6 | 0.860662 | cache | 2020-06-29 to 2026-10-08 | 0.6867 / 1.0 | 1.0 | passes | validated |
| NFFFX | 6 | 6 | 0.804542 | cache | 2020-06-29 to 2026-10-08 | 0.7011 / 1.0 | 1.0 | passes | unreadable |
| MEIIX | 6 | 5 | 0.576683 | cache | 2020-06-29 to 2026-10-08 | 0.6991 / 1.0 | 1.0 | passes | validated |
| VGHAX | 5 | 5 | 0.661119 | cache | 2020-06-29 to 2026-10-08 | 0.6878 / 1.0 | 0.2 | too_few | unreadable |

Counts: held_in_cache=15 held_in_fetch_folder=0 none_held=0; held_series_passes=14 fails=0 too_few_trades=1. Served-close unit counts equal the record for 15 of 15.

Not established:
- Close was taken as the vendor's unadjusted close; the cache holds it beside Adj Close (the two differ in every one of the 15 files) but nothing here proves the vendor Close is free of dividend adjustment except that it reproduces the price paid on trades.
- VGHAX has 5 trade units and 4 of them fall in the 1-to-20 percent bands with the unadjusted close; the held series is neither shown to pass nor to fail; the rule's too_few class applies.
- The rule's charge-sized and front-load excuses take units with 1-to-20 percent deviation out of the failing count (VEIRX 47 units in 5-to-20, PCBIX 9, PRILX 3, VGHAX 2, AGTHX 1, SGIIX 1 in 5-to-20 plus 1 over 20); the class used is the rule as written; the plain within-1-percent share is reported beside it and is lower for those funds.
- The cache starts 2020-06-29 and ends 2026-10-08 (one pull dated 2026-10-09): build held days before that date are not covered. share_of_held_days_covered counts all build held days including non-trading days the build interpolates (about 0.69 to 0.70); over held TRADING days every fund's share is 1.0 (column share_of_held_trading_days_covered in the JSON).
