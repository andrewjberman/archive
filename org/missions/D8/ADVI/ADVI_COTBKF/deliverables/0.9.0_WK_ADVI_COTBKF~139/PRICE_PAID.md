# CB-bx-2 -- the price-paid instrument over the whole table (round 76, 0.9.0_WK_ADVI_COTBKF~139)

Generated 2026-10-11T22:55Z. Counts, ratios, tickers and dates only; no account id, amount or quantity. Record: `PRICE_PAID.json`; per fund: `PRICE_PAID.csv`.

**Headline.** Of 14250 purchase and sale units of the 270 fund series that sit on a served close, 10523 (73.8%) are within 1 percent of the price paid and 3211 (22.5%) are more than 20 percent off, 3206 of those with the served close BELOW the price paid; the instrument reads only 14250 of 91040 units because 76790 trades pre-date the series' first stored close. The off units are the left-on-store funds: 3614 units of 61 funds, 112 within 1 percent (3.1%), 3205 over 20 percent (88.7%), median ratio 0.742; purchases 1574 over 20 of 1754, SALES 1631 over 20 of 1860 (a sale carries no front load). The 237 unreadable funds are sized for the first time: the 178 of them left on the store give 1736 units from 43 funds, 1563 over 20 percent (90.0%), median 0.749. The 73 substituted funds, the control, read 10411 of 10636 units within 1 percent (97.9%), median 1.000; the 14 validated-substituted read 4846 of 5026. The 19 moved: 1878 units, 11 within 1 percent. 178 fund series are not reached (no unit with a close); 372 of the 377 accounts with a priced day in the 19 funds have a read unit.

## Population (rows, then units)

| step | count | unit | dropped |
|---|---|---|---|
| fund series in the served table | 270 | series | |
| by + sl rows of those series, all accounts, all years (51232 by, 40301 sl) | 91533 | ROWS | (of 594771 rows of any type in the 270 series) |
| non-null non-zero Amount and Quantity | 91533 | ROWS | 0 |
| quantity guard abs(Quantity) >= 0.05 (3 decimals) | 91495 | ROWS | 38 |
| summed to (account, effective day, fund, kind) | 91040 | UNITS | 0 with a zero sum |
| with a served close on the effective day | 14250 | UNITS | 76790 (all 76790 before the series first stored close) |

Fund series with a row at each step: 247 (by/sl) -> 247 (amount, quantity) -> 247 (guard) -> 92 (read unit). Distinct accounts: 928 (first step) -> 928 -> 928 -> 928 (units) -> 544 (last step, read units). Day convention: round 75's (effective day = Trade_Date, next NYSE trading day when closed; 1 row moved). Year is the effective day's year.

## Control (positive): the 12 purchase days of round 75

Served close over amount per unit: median 0.75864, within 1 percent on 0 of 12 (round 75 record: median 0.75864, 0 of 12). Reproduced; 12 of 12 account-days matched.

## Four bands, all read units

| all | units | within 1 | 1-5 | 5-20 | over 20 | share within 1 | median ratio | below/above/equal |
|---|---|---|---|---|---|---|---|---|
| all read units | 14250 | 10523 | 213 | 303 | 3211 | 73.8% | 0.999999 | 8862/5367/21 |

## By kind

| kind | units | within 1 | 1-5 | 5-20 | over 20 | share within 1 | median ratio | below/above/equal |
|---|---|---|---|---|---|---|---|---|
| purchase | 7618 | 5821 | 94 | 126 | 1577 | 76.4% | 0.999999 | 4817/2789/12 |
| sale | 6632 | 4702 | 119 | 177 | 1634 | 70.9% | 0.999999 | 4045/2578/9 |

Kind x direction x band (units):

| kind | direction | within 1 | 1-5 | 5-20 | over 20 |
|---|---|---|---|---|---|
| purchase | below | 3026 | 89 | 125 | 1577 |
| purchase | above | 2783 | 5 | 1 | 0 |
| sale | below | 2237 | 26 | 153 | 1629 |
| sale | above | 2456 | 93 | 24 | 5 |

## By direction (below = served close under the price paid)

| direction | units | within 1 | 1-5 | 5-20 | over 20 | share within 1 | median ratio | below/above/equal |
|---|---|---|---|---|---|---|---|---|
| below | 8862 | 5263 | 115 | 278 | 3206 | 59.4% | 0.999979 | 8862/0/0 |
| above | 5367 | 5239 | 98 | 25 | 5 | 97.6% | 1.000003 | 0/5367/0 |
| equal | 21 | 21 | 0 | 0 | 0 | 100.0% | 1.0 | 0/0/21 |

## By year

| year | units | within 1 | 1-5 | 5-20 | over 20 | share within 1 | median ratio | below/above/equal |
|---|---|---|---|---|---|---|---|---|
| 2020 | 130 | 113 | 0 | 1 | 16 | 86.9% | 1.0 | 75/53/2 |
| 2021 | 925 | 778 | 6 | 4 | 137 | 84.1% | 1.0 | 502/423/0 |
| 2022 | 2431 | 1167 | 32 | 190 | 1042 | 48.0% | 0.941178 | 1753/678/0 |
| 2023 | 2536 | 1257 | 33 | 27 | 1219 | 49.6% | 0.989935 | 1909/624/3 |
| 2024 | 3444 | 2560 | 55 | 32 | 797 | 74.3% | 0.999999 | 2132/1305/7 |
| 2025 | 3336 | 3244 | 50 | 42 | 0 | 97.2% | 1.0 | 1736/1595/5 |
| 2026 | 1448 | 1404 | 37 | 7 | 0 | 97.0% | 1.0 | 755/689/4 |

Left-on-store funds (197 series) by year: median ratio (units): 2020 0.5619 (16); 2021 0.6358 (138); 2022 0.7489 (1215); 2023 0.6178 (1231); 2024 0.7018 (840); 2025 0.9915 (105); 2026 1.0 (69).

## By group of fund

| group (series) [funds with a read unit] | units | within 1 | 1-5 | 5-20 | over 20 | share within 1 | median ratio | below/above/equal |
|---|---|---|---|---|---|---|---|---|
| the 19 moved (19) [18] | 1878 | 11 | 14 | 211 | 1642 | 0.6% | 0.678346 | 1876/2/0 |
| the 33 validated (33) [32] | 6904 | 4857 | 148 | 252 | 1647 | 70.4% | 0.999999 | 4444/2450/10 |
| - validated, left on the store (19 = the moved 19) [18] | 1878 | 11 | 14 | 211 | 1642 | 0.6% | 0.678346 | 1876/2/0 |
| - validated, substituted (14) [14] | 5026 | 4846 | 134 | 41 | 5 | 96.4% | 1.0 | 2568/2448/10 |
| the 237 unreadable (237) [60] | 7346 | 5666 | 65 | 51 | 1564 | 77.1% | 0.999999 | 4418/2917/11 |
| - unreadable, substituted (59) [17] | 5610 | 5565 | 40 | 4 | 1 | 99.2% | 1.0 | 2748/2851/11 |
| - unreadable, left on the store (178) [43] | 1736 | 101 | 25 | 47 | 1563 | 5.8% | 0.748865 | 1670/66/0 |
| ALL SUBSTITUTED, the control (73) [31] | 10636 | 10411 | 174 | 45 | 6 | 97.9% | 1.0 | 5316/5299/21 |
| ALL LEFT ON THE STORE (197) [61] | 3614 | 112 | 39 | 258 | 3205 | 3.1% | 0.741955 | 3546/68/0 |

By group and kind (units; within 1 / over 20; median):

| group | purchase | sale |
|---|---|---|
| the 19 moved (19) | 936; 3 / 841; 0.649063 | 942; 8 / 801; 0.703105 |
| the 33 validated (33) | 3922; 2875 / 844; 0.999999 | 2982; 1982 / 803; 0.999999 |
| - validated, left on the store (19 = the moved 19) | 936; 3 / 841; 0.649063 | 942; 8 / 801; 0.703105 |
| - validated, substituted (14) | 2986; 2872 / 3; 1.0 | 2040; 1974 / 2; 1.0 |
| the 237 unreadable (237) | 3696; 2946 / 733; 0.999999 | 3650; 2720 / 831; 0.999999 |
| - unreadable, substituted (59) | 2878; 2878 / 0; 1.0 | 2732; 2687 / 1; 1.0 |
| - unreadable, left on the store (178) | 818; 68 / 733; 0.748861 | 918; 33 / 830; 0.755725 |
| ALL SUBSTITUTED, the control (73) | 5864; 5750 / 3; 1.0 | 4772; 4661 / 3; 1.0 |
| ALL LEFT ON THE STORE (197) | 1754; 71 / 1574; 0.691719 | 1860; 41 / 1631; 0.748852 |

**Controls.** Substituted (negative control): 10411 of 10636 units within 1 percent (97.9%), median 1.0, 6 over 20 percent. The 33 validated split as expected: the 19 left on the store read 11 of 1878 within 1 percent (0.6%); the 14 substituted read 4846 of 5026 (96.4%).

## Not reached (fund series with no read unit)

178 of 270 series: 23 have no by/sl row at all; 155 have by/sl rows, all of them before the series first stored close.

Mutually exclusive four labels: moved_19 1 (ACTDX), validated_substituted 0, unreadable_substituted 42, unreadable_left_on_store 135. Cross-cut: moved_19 1 of 19 (no by/sl row 0); validated_33 1 of 33 (no by/sl row 0); unreadable_237_substituted 42 of 59 (no by/sl row 2); unreadable_237_left_on_store 135 of 178 (no by/sl row 21); substituted_73 42 of 73 (no by/sl row 2); left_on_store_197 136 of 197 (no by/sl row 21).

Holders of the 19: 377 accounts have a priced day in one of the 19 (round 75's 377; 452 hold one on some day with a nonzero quantity); 372 of the 377 have at least one read unit in one of the 19.

Held (account, fund) pairs, 270 series: 12640; with a read unit 2664; with by/sl rows but none read 9642; no by/sl row at all (arrived by transfer, never traded) 334. For the 19: 579 / 466 / 98 / 15.

## Not established

- WHY any unit is off. The instrument sets the served close beside amount per unit and reports the gap; it does not say the series is dividend-adjusted, a fee, a rounding or a mis-scale. Another cell explains.
- The 76790 units (84.3% of 91040) that pre-date the series' first stored close are not read at all, and 178 of the 270 series (23 with no purchase or sale row, 155 with rows but none after the first close) are not reached; the defect on those trades, and in the years before each series' first held day, is unsized by this instrument.
- The read units are weighted to recent days (the served table starts at a security's first held day); a by-year median is a mix of different funds in different years, so a trend in it is not the shrink of one adjustment toward the present. The within-1-percent left-on-store funds are mostly 1 to 2 trades in June 2026 (series first stored in June 2026) or two commodity trusts (PHYS, PSLV).
- Price paid is Amount over Quantity as the custodian records it; a purchase carries a front load of up to 5.75 percent (ratio below 1) and a sale may be net of a redemption fee; the 1-to-5 and 5-to-20 bands are reported by kind and direction, not explained. In the 1-to-5 band 89 purchase units and 26 sale units sit below 1; 5 purchase and 93 sale units sit above 1.
- The substituted control reads within 1 percent on 97.9% of units; the 225 units outside it (the 73 funds) are not explained: they include VBIRX (60 units, 16 within 1 percent) and the single SWPPX unit at 0.167.
- Day convention is round 75's (effective day close); a one-day shift was NOT rerun here (round 75 found the same reading at the previous and next trading day on the 12 days). The quantity guard is applied to ROWS (|Quantity| >= 0.05; 38 rows dropped); a guard on the summed unit, and another guard value, were not tested. Units whose rows net to zero: 0.
- Only by and sl rows are read. Reinvestment (dvr), transfer and corporate-action rows are not priced here. Holdings that arrived by transfer or in kind and were never bought or sold: 334 of 12640 held (account, fund) pairs have no purchase or sale row at all (15 of 579 for the 19); their price is not seen by this instrument.
- Holders: round 75's 377 is the accounts with a priced (non-null value) day in one of the 19 funds; 452 accounts hold one of them on some day with a nonzero quantity. 372 of the 377 priced holders have a read unit; the weight of the trades and of the holdings in money is not measured (counts only).
- The unadjusted vendor close (yahoo_census) was not read: the substituted funds' served close already IS the unadjusted close, and the instrument needs no vendor data. Whether a within-1-percent left-on-store unit is a correct close or an unadjusted stretch of the series is not distinguished.
