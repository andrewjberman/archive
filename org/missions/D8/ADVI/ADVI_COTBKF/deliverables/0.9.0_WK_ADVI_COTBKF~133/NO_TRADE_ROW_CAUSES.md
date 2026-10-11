# CB-bw-2: the 74 large changes with no trade row, by cause

Worker 0.9.0_WK_ADVI_COTBKF~133, round 75, risk LOCAL. A measurement on copies of the round-74 builds (baseline = served table, variant = 19 funds on an unadjusted close). Nothing served, fetched or changed. The closed list and its tests were written at 2026-10-11T22:04:50Z, before any of the 74 days was looked at (only the 96 / 22 / 74 count had run), and were not changed. No account id or account value is in this file.

Reproduced: 96 changes over 10 bp; 22 with a purchase, sale or reinvestment (by, sl, dvr) of FCNTX, BALCX, CWGIX, ANCFX or CAIBX that day (12 / 2 / 8); 74 without.

| cause (order tried) | days | higher | lower | median abs change (bp) | share of the 74 | share of their total abs change | days that fit the test (overlap) |
|---|---|---|---|---|---|---|---|
| reinvestment | 9 | 0 | 9 | 44.9 | 12.2% | 42.5% | 9 |
| transfer | 1 | 1 | 0 | 10.2 | 1.4% | 0.6% | 2 |
| distribution_date | 0 | 0 | 0 | - | 0.0% | 0.0% | 2 |
| price_step | 1 | 1 | 0 | 42.5 | 1.4% | 2.4% | 9 |
| days_dropped | 0 | 0 | 0 | - | 0.0% | 0.0% | 0 |
| weight_effect | 63 | 29 | 34 | 12.9 | 85.1% | 54.6% | 65 |
| trade_in_another_security | 0 | 0 | 0 | - | 0.0% | 0.0% | 3 |
| prior_day_trade | 0 | 0 | 0 | - | 0.0% | 0.0% | 2 |
| small_base | 0 | 0 | 0 | - | 0.0% | 0.0% | 0 |
| none_found | 0 | 0 | 0 | - | 0.0% | 0.0% | - |

Total absolute change of the 74: 1785.9 bp. none_found: 0 days, so no largest change; all ten tests were applied to every day.

**weight_effect** is the cause the formula allows with no trade: ret = (V_t - flow + adj) / V_s - 1. When an exposed fund price ratio k (variant over baseline) is flat but not 1, the fund value is scaled by k on both days, its own return is unchanged, its weight in the account is not, and the account return moves by the weight change times (fund return minus the rest of the account). The test holds each ratio at its previous-day value and keeps the day if that reproduces at least half the change in the same direction; on all 63 it reproduces at least 99.99%.

**price_step**: 9 of the 74 days fit (a held exposed fund whose ratio steps by over 10 bp between the base day and the day): 8 down, 1 up; 8 on a distribution date of the fund (BALCX 5, ANCFX 3, all down), 1 not (FCNTX 1, up, 2026-06-08). Eight of them are taken first by reinvestment (order), one by price_step.

**The same list over the 22, trade row ignored** (first fit): reinvestment 3, distribution_date 5, weight_effect 14, nothing else. The 12 purchase days and 2 sale days all read weight_effect and none reads price_step; the 8 reinvestment days read distribution_date (5) or reinvestment (3), and 4 of them also fit price_step (FCNTX down on a distribution date). The 22 have a total absolute change of 2466.6 bp; weight_effect holds 91.7% of it.

**Headline.** All 74 changes take a cause from the closed list written before the look; none_found is 0 of 74. One cause carries most of the days: weight_effect holds 63 of 74 days (85.1%) and 54.6% of their total absolute change (974 bp); on those days the counterfactual with each exposed fund price ratio held at its previous-day value reproduces the whole change (weight part at least 99.99% of it): the fund is valued on a different price level, so its weight in the account differs, and the account return differs with no trade and no price step. Reinvestment (a dvr row 1 to 3 days off) takes 9 days and 42.5% of the total absolute change, all lower, median 44.9 bp, and 8 of the 9 also fit a down step of the fund ratio over 10 bp on a distribution date (BALCX 5, ANCFX 3); transfer takes 1, price_step 1 (FCNTX up, 2026-06-08); distribution_date, days_dropped, trade_in_another_security, prior_day_trade and small_base take 0 by first fit. By year: 2022 69, 2023 4, 2026 1.

**Not established.**
- Whether the 63 weight_effect days are an error of the variant, of the baseline, or neither: the test shows that a flat price ratio different from 1 changes the weights and so the return, not which price level is the right one to weight by.
- The order decides the label where tests overlap: 8 of the 9 reinvestment days also fit price_step (and 2 also distribution_date); tried first, price_step would hold 9 days. The overlap counts per test are in price_step_detail.overlap_fits_of_the_74.
- The thresholds (3 calendar days, 10 bp ratio step, 50 percent counterfactual share, 10 percent of the median base) were fixed before the look; no sensitivity to them was run. small_base fit 0 of 74 and days_dropped 0 of 74.
- Custodian rows were matched on Trade_Date as the step 1 trade-row test does; a row dated on a non-trading day (which the return build moves to the next trading day) is not moved to that day in tests 1, 3, 7 and 8 (the transfer test also reads the build flow column, which is moved).
- Only the five funds with measured exposure; the other 14 moved funds have no measured-in-both account-day (round 74). No search for a cause outside the closed list was run, because no day read none_found.
- trade_in_another_security fits 3 of 74 days but takes none by first fit; by the return formula a trade at the end of day t changes no weight at the base of the return of day t, so no mechanism is claimed for it.
- Total absolute change of the 74: 1785.9 bp; median 13.24 bp; largest 216.24 bp.

Record: NO_TRADE_ROW_CAUSES.json (same directory). The closed list text and its timestamp are in its closed_list.
