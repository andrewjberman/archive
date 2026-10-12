# PRICE_PAID_CAUSES (CB-bz-1, round 78, 0.9.0_WK_ADVI_COTBKF~148)

Reading: fails. On the 13,009 informative held-out units (P1 10,541, P2 2,468) 97.1% fit one of the seven figures, but 92.4% of the units are zero-gap (they fit 0 and carry no charge); on the 984 informative off-zero units, which are the real test, 604 (61.4%) fit one of the six nonzero figures against 0.41% for the best shifted set (P1 71.1% against 0.47%, P2 43.1% against 0.29%). The pre-registered bar (90 percent on each of P1 and P2, chance at most 20, below 50 is a fail) is missed: P1 not_established, P2 fails. The figures are not chance, they are an incomplete description: the left-over held-out units cluster near 12 dollars (post hoc). In sample the same figures fit 936 of 936 units, as round 76 read them off. Of 727 units still off, 592 are explained by the flat charge (order B) and 92 have no cause under either order; 161 change cause with the order.

## 1. The test, written first (2026-10-12T01:06:59Z)

Constants [0, 3, 10, 15, 19, 30, 34] dollars, window 0.15. Gap = |Amount| - |Quantity| x close for a purchase, |Quantity| x close - |Amount| for a sale (close = unadjusted). Rule per row; a unit fits when every row fits. Verdict rule: X = 90, Y = 20, fails below 50, on informative units (|Amount| over 100 dollars) of P1 and P2 separately. Full text: `test.text` in the JSON; kept unchanged.

## 2. Fit by population (informative units)

| population | units | zero-gap | off-zero | fit seven (S7) | best shifted seven | off-zero fit a nonzero figure (S6) | best shifted six | analytic seven/six | verdict |
|---|---|---|---|---|---|---|---|---|---|
| P1 | 10541 | 9898 | 643 | 10355 (98.24%) | 0.03% | 457 (71.07%) | 0.47% | 6.7% / 5.8% | not_established |
| P2 | 2468 | 2127 | 341 | 2274 (92.14%) | 0.04% | 147 (43.11%) | 0.29% | 23.3% / 20.0% | fails |
| HELD_OUT = P1 + P2 | 13009 | 12025 | 984 | 12629 (97.08%) | 0.03% | 604 (61.38%) | 0.41% | 6.7% / 5.8% | fails |
| P3 | 940 | 155 | 785 | 929 (98.83%) | 0.00% | 774 (98.6%) | 0.0% | 11.0% / 9.5% | holds (SEEN in round 76 (its sale note), not clean held-out; reported apart) |
| IN_SAMPLE | 935 | 112 | 823 | 935 (100.00%) | 0.00% | 823 (100.0%) | 0.0% | 11.0% / 9.4% | holds (in sample) |

Units fitting each figure (informative):

| population | 0 | 3 | 10 | 15 | 19 | 30 | 34 | none |
|---|---|---|---|---|---|---|---|---|
| P1 | 9898 | 98 | 31 | 13 | 101 | 158 | 56 | 186 |
| P2 | 2127 | 1 | 28 | 0 | 113 | 0 | 5 | 194 |
| HELD_OUT = P1 + P2 | 12025 | 99 | 59 | 13 | 214 | 158 | 61 | 380 |
| P3 | 155 | 0 | 10 | 72 | 17 | 485 | 190 | 11 |
| IN_SAMPLE | 112 | 34 | 2 | 60 | 24 | 502 | 201 | 0 |

Held-out constants seen (units fitting): {'3': 99, '10': 59, '15': 13, '19': 214, '30': 158, '34': 61}. All six nonzero figures are seen held out (>= 10 units each); the verdict rests on all of them.

By size of trade (fit of the seven / of the off-zero units to a nonzero figure / best shifted):

| band | P1 S7 | P1 S6 | P2 S7 | P2 S6 | held-out best shifted seven |
|---|---|---|---|---|---|
| lt100 | 100.0 | None | 88.89 | 0.0 | 0.0 |
| 100_1k | 97.49 | 67.78 | 93.41 | 41.74 | 0.02 |
| 1k_10k | 98.85 | 70.97 | 91.56 | 44.0 | 0.05 |
| gt10k | 97.82 | 76.92 | 90.24 | 43.14 | 0.0 |

Cross-check of the served close of P1 against the cache Close: {"P1_funds_with_a_read_unit": 31, "with_a_cache_file": 31, "units_compared": 10636, "units_agree_within_1_cent": 10633, "series_dates_compared": 37748, "series_dates_agree": 37677, "funds_fully_agreeing_on_every_date": 4, "funds_compared": 31}.
Close used for the nineteen: {"served_r34_after_vs_cache_close_for_the_nineteen": "6 of 1,878 units agree: the r34 after series for the nineteen is the stored (not unadjusted) series (round 77 left them on the store)", "round_76_unadjusted_close_w129_variant_vs_cache_close": "25,236 of 25,311 series dates agree", "used": "w129 variant security_day_price (round 76 close) for the nineteen, the served r34 after for the 73, the cache Close for P2"}.

## 3. The charge, from the rows

| figure | units | funds | accounts | years | purchases | sales | median size band | main funds |
|---|---|---|---|---|---|---|---|---|
| 3 | 133 | 5 | 9 | 2021:1, 2022:6, 2023:44, 2024:48, 2025:23, 2026:11 | 122 | 11 | 100_1k | VFIAX 87, VEIRX 34, VBIRX 10, PCBIX 1 |
| 10 | 71 | 4 | 15 | 2020:7, 2021:11, 2022:23, 2023:10, 2024:14, 2025:6 | 2 | 69 | 1k_10k | PCBIX 28, MISIX 18, PDBZX 13, PRILX 12 |
| 15 | 145 | 3 | 37 | 2022:5, 2023:69, 2024:68, 2025:2, 2026:1 | 68 | 77 | 1k_10k | VEIRX 132, VBIRX 8, VWIUX 5 |
| 19 | 255 | 11 | 67 | 2020:32, 2021:48, 2022:72, 2023:47, 2024:46, 2025:9, 2026:1 | 33 | 222 | 1k_10k | PCBIX 108, PDBZX 56, VEIRX 40, MISIX 26 |
| 30 | 1145 | 5 | 242 | 2021:10, 2022:43, 2023:540, 2024:491, 2025:44, 2026:17 | 598 | 547 | gt10k | VEIRX 987, VWIUX 126, VBIRX 27, VFIAX 4 |
| 34 | 452 | 7 | 128 | 2020:1, 2021:4, 2022:15, 2023:226, 2024:186, 2025:13, 2026:7 | 239 | 213 | gt10k | VEIRX 391, VWIUX 31, VBIRX 15, VFIAX 8 |

A figure goes with the fund family and the kind of row, and with the size of the trade: 3 is on Vanguard index/bond funds mostly as a purchase on trades of 100 to 1,000 dollars; 10 and 19 are on the Principal, PGIM, Victory and Parnassus funds, almost all SALES; 30 and 34 are on Vanguard funds in both kinds, on trades over 1,000 dollars, nearly all in 2023 and 2024; 15 is on Vanguard in 2022-2024. In the funds that carry a charge at all it is on nearly every unit (VEIRX: all but 12 of 1,596). It does not go with an account day: see account_day.

Account days: {"account_days_with_2plus_units": 4848, "one_nonzero_figure_plus_zero_gap_units": 1611, "all_units_zero_gap": 2917, "different_nonzero_figures": 69, "one_or_more_unit_fits_no_figure": 226, "same_nonzero_figure_on_all_units": 25, "account_days_all_informative": 6336, "reading": "the figure is per unit, not per account day: in 1611 account days a unit carries a nonzero figure beside a zero-gap unit, and where every unit of an account day is charged the same figure is on all in 25 and different figures in 69"}

On disk: Nothing on the unit rows names the charge: no fee column, no note word (fee, charge, commission, ticket) on any of the 14,998 unit rows that reads as a charge, and no fee- or expense-type row dated the same day in the same account for more charged units (13 of 2201, 0.59%) than for zero-gap units (66 of 12292, 0.54%). The only row text that names a ticket charge is the misc row "COMMISSION ADJ TICKET CHG" (15 rows); none of them sits on an account day of any unit tested. So the charge is not named on disk; what it is is not established.

## 4. Units still more than 1 percent off: 727

| cause | order A | order B |
|---|---|---|
| flat_dollar_charge | 431 | 592 |
| prior_day_close | 87 | 19 |
| next_day_close | 78 | 20 |
| reinvestment_or_exchange_recorded_as_purchase | 33 | 4 |
| adjusted_close | 6 | 0 |
| another_share_class | 0 | 0 |
| small_quantity | 0 | 0 |
| none_found | 92 | 92 |

Order A: small_quantity, prior_day_close, next_day_close, adjusted_close, another_share_class, reinvestment_or_exchange_recorded_as_purchase, flat_dollar_charge, none_found. Order B: small_quantity, flat_dollar_charge, prior_day_close, next_day_close, adjusted_close, another_share_class, reinvestment_or_exchange_recorded_as_purchase, none_found. Units that change cause with the order: 161 ({'adjusted_close -> flat_dollar_charge': 6, 'next_day_close -> flat_dollar_charge': 58, 'prior_day_close -> flat_dollar_charge': 68, 'reinvestment_or_exchange_recorded_as_purchase -> flat_dollar_charge': 29}).

The flat-dollar test on the same 727 units: real set 592; each shifted set {'plus_1.50': 0, 'minus_1.50': 0, 'plus_0.75': 0, 'minus_0.75': 0}.

none_found by fund (units; years):

- AGTHX: 1 (2021:1)
- MISIX: 11 (2024:10, 2025:1)
- PCBIX: 55 (2020:24, 2021:22, 2022:8, 2023:1)
- PDBZX: 13 (2021:2, 2022:8, 2023:2, 2025:1)
- SGIIX: 1 (2023:1)
- SWPPX: 1 (2024:1)
- VFIAX: 9 (2024:2, 2025:7)
- VTSAX: 1 (2022:1)

Looked at: small_quantity (units under 0.05 shares or 0.50 dollars: none), the previous and next day close of the fund own series, the Yahoo Adj Close (funds with a cache file: all of them have one), a sibling class (round 76 table: the nineteen only; none of the none_found funds is in it), a dividend/reinvestment row (+/-5 days, amount within 1 percent) and an opposite-kind row (+/-1 day, amount within 1 percent) of the same account, and the flat-dollar figures (the gap fits no figure, or fits one and leaves the unit outside 1 percent).

## 5. VEIRX

VEIRX carries a flat-dollar gap on 1,584 of its 1,596 units (purchases and sales), so a unit is off by more than 1 percent exactly when the gap exceeds 1 percent of the amount: 243 of its 827 purchases, none of them over 10,000 dollars. The other 18 funds of the nineteen carry a zero gap on 257 of 282 units. Of the 299 purchases on 2024-02-16 (one per account) 245 are under 10,000 dollars (the median band that day is 1,000 to 10,000, against over 10,000 on other days) and 141 are off: the same charge-over-1-percent condition, on a day of many small buys.

## 6. What the rule may say

H does not hold, so the plain shares stand: the rule (price paid = unadjusted close) reproduces 73.72% of purchase units of the nineteen funds, 87.07% for the 15 failing funds, 98.06% for the 73 substituted funds, and 89.17% / 89.57% / 97.67% of the sales; the rule still has the remainder (the units outside 1 percent) against it.

| | 19 funds | 15 failing funds | 73 substituted |
|---|---|---|---|
| purchases plain share | 690 of 936 (73.72%) | 1683 of 1933 (87.07%) | 5750 of 5864 (98.06%) |
| sales plain share | 840 of 942 (89.17%) | 2190 of 2445 (89.57%) | 4661 of 4772 (97.67%) |

## 7. POST HOC (in no count)

POST HOC, in no count: a gap near 12 dollars is the most common value among the units that fit no figure (round 76 sale note also listed 10 units at 12 outside the seven); a better set would add it, and 14. It is read off the same units, so it is a description, not a test.

## 8. Not established

- What the charge is and who takes it: no row says so. The only row text that names a ticket charge sits on no account day of any unit tested.
- Why the figures differ by fund family and kind (3 on Vanguard purchases, 10 and 19 on sales of Principal, PGIM, Victory and Parnassus funds, 30 and 34 on Vanguard in both kinds): a fee schedule is not on disk.
- The 380 informative held-out units that fit no figure: P2 is PCBIX (183 of 194; 171 of the 194 have a gap within 0.15 of 12 dollars), P1 is PDBZX 80, VFIAX 57 and MISIX 26 of 186 (101 within 0.15 of 12); 12 dollars is a post hoc candidate only.
- The 92 none_found units (PCBIX 55, PDBZX 13, MISIX 11, VFIAX 9, 4 others) have no cause on the list: the closed list holds no entry for them.
- Whether the unadjusted close the nineteen funds are tested against (round 76 w129 variant) is the vendor close for every date: it agrees with the cache Close on 25,236 of 25,311 series dates, not all.
- Only 31 of the 73 substituted funds have a unit in the custodian rows; 42 are not tested. Units with no Yahoo Close (before 2020-06-29) are not read in P2 (1,923 of 4,407).
- The 0.15 window, the seven figures, X=90, Y=20 and the per-row rule are fixed by the test as written; a different window or a unit-sum rule was not run. Every unit has one row, so the per-row rule and the sum rule agree on this data.
- The informative-unit cut (|Amount| over 100 dollars) removes 114 of 14998 units; the fit by size band is in by_population.
- The sale rows (P3) were looked at by round 76; the P1 sale units are held out. A sale carries the same figure set only as shown here, not as a cause.
