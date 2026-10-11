# AMGT_RESAPP round 90 -- AMGT-oo-1, the whole-page read (FWD-8, FWD-38)

Live function `opal-amgt-scoped-api`, GET only, read 2026-10-11 by `2.0.0_SA_COO~R1`; trading-day distance from `lib/trading_calendar.trading_days_behind` (NYSE).

## ASML_NA_Equity

route status: thesis 200, peers 200 | header figures 24, header vintage date(s): {'2026-10-10': 24}

**FWD-8 peer identity** -- subject key equal on thesis and peers: True; crosswalk vintage equal: True (2026-10-09)
- members 12 | United States alphabetic 9 | resolvable (`<T> US`, or an all-digit ticker by its Japan code or a unique held name) 6 | served MEASURED 6
- served a key the pool does not hold under that form (leaked): 0 [] | resolvable but not served (missing): 0 [] | served a different key (wrong): 0 [] | rows with no identity.resolution: 0
- **agrees: YES**

**FWD-38 vintages** -- figure vintages within one trading day of the header's: 1675 of 1687; object as-of dates within one trading day: 2 of 11

| kind | route and path | date | header date | n | trading days behind | within 1 |
|---|---|---|---|---|---|---|
| object | `peers` `//as_of` | 2026-10-11 | 2026-10-10 | 1 | 0 | yes |
| object | `peers` `//universe_vintage` | 2026-10-02 | 2026-10-10 | 1 | 5 | NO |
| figure | `peers` `//vintage` | 2026-10-11 | 2026-10-10 | 1 | 0 | yes |
| figure | `peers` `/members[]/cap_vintage` | 2026-10-02 | 2026-10-10 | 12 | 5 | NO |
| object | `peers` `/peer_read/as_of` | 2026-10-11 | 2026-10-10 | 1 | 0 | yes |
| figure | `peers` `/subject/cap_vintage` | 2026-10-10 | 2026-10-10 | 1 | 0 | yes |
| figure | `peers` `/subject/market_cap_vintage` | 2026-10-10 | 2026-10-10 | 1 | 0 | yes |
| figure | `thesis` `/fiscal_year_figures[]/vintage` | 2026-10-10 | 2026-10-10 | 799 | 0 | yes |
| figure | `thesis` `/header_figures[]/vintage` | 2026-10-10 | 2026-10-10 | 24 | 0 | yes |
| object | `thesis` `/management/as_of` | 2026-10-02 | 2026-10-10 | 1 | 5 | NO |
| object | `thesis` `/management/object_as_of` | 2026-10-02 | 2026-10-10 | 1 | 5 | NO |
| object | `thesis` `/management/management_read/as_of` | 2026-10-02 | 2026-10-10 | 1 | 5 | NO |
| figure | `thesis` `/model/cases/base/px_last/vintage` | 2026-10-10 | 2026-10-10 | 1 | 0 | yes |
| figure | `thesis` `/model/fiscal_year_figures[]/vintage` | 2026-10-10 | 2026-10-10 | 799 | 0 | yes |
| figure | `thesis` `/model/forecast_figures[]/vintage` | 2026-10-10 | 2026-10-10 | 48 | 0 | yes |
| figure | `thesis` `/model_cases/base/px_last/vintage` | 2026-10-10 | 2026-10-10 | 1 | 0 | yes |
| object | `thesis` `/posture/as_of` | 2026-09-16 | 2026-10-10 | 1 | 17 | NO |
| object | `thesis` `/posture/membership/as_of` | 2026-09-16 | 2026-10-10 | 1 | 17 | NO |
| object | `thesis` `/posture/posture_read/as_of` | 2026-09-16 | 2026-10-10 | 1 | 17 | NO |
| object | `thesis` `/scores/as_of` | 2026-09-17 | 2026-10-10 | 1 | 16 | NO |
| object | `thesis` `/scores/scores_read/as_of` | 2026-09-17 | 2026-10-10 | 1 | 16 | NO |

page states the cross-vintage itself (`peers.subject.cross_vintage_caveat`): yes -- the subject's scalars carry the model block's own vintage (2026-10-10T13:01:55Z); every candidate carries the scanner's asOf -- the band is graded ACROSS those two vintages and neither is re-dated

## BA_US_Equity

route status: thesis 200, peers 200 | header figures 24, header vintage date(s): {'2026-10-10': 24}

**FWD-8 peer identity** -- subject key equal on thesis and peers: True; crosswalk vintage equal: True (2026-10-09)
- members 12 | United States alphabetic 12 | resolvable (`<T> US`, or an all-digit ticker by its Japan code or a unique held name) 6 | served MEASURED 6
- served a key the pool does not hold under that form (leaked): 0 [] | resolvable but not served (missing): 0 [] | served a different key (wrong): 0 [] | rows with no identity.resolution: 0
- **agrees: YES**

**FWD-38 vintages** -- figure vintages within one trading day of the header's: 1448 of 1460; object as-of dates within one trading day: 2 of 13

| kind | route and path | date | header date | n | trading days behind | within 1 |
|---|---|---|---|---|---|---|
| object | `peers` `//as_of` | 2026-10-11 | 2026-10-10 | 1 | 0 | yes |
| object | `peers` `//universe_vintage` | 2026-10-02 | 2026-10-10 | 1 | 5 | NO |
| figure | `peers` `//vintage` | 2026-10-11 | 2026-10-10 | 1 | 0 | yes |
| figure | `peers` `/members[]/cap_vintage` | 2026-10-02 | 2026-10-10 | 12 | 5 | NO |
| object | `peers` `/peer_read/as_of` | 2026-10-11 | 2026-10-10 | 1 | 0 | yes |
| figure | `peers` `/subject/cap_vintage` | 2026-10-10 | 2026-10-10 | 1 | 0 | yes |
| figure | `peers` `/subject/market_cap_vintage` | 2026-10-10 | 2026-10-10 | 1 | 0 | yes |
| figure | `thesis` `/fiscal_year_figures[]/vintage` | 2026-10-10 | 2026-10-10 | 686 | 0 | yes |
| figure | `thesis` `/header_figures[]/vintage` | 2026-10-10 | 2026-10-10 | 24 | 0 | yes |
| object | `thesis` `/management/as_of` | 2026-09-15 | 2026-10-10 | 1 | 18 | NO |
| object | `thesis` `/management/object_as_of` | 2026-09-15 | 2026-10-10 | 1 | 18 | NO |
| object | `thesis` `/management/management_read/as_of` | 2026-09-15 | 2026-10-10 | 1 | 18 | NO |
| object | `thesis` `/management/pool_read/as_of` | 2026-09-19 | 2026-10-10 | 1 | 15 | NO |
| figure | `thesis` `/model/cases/base/px_last/vintage` | 2026-10-10 | 2026-10-10 | 1 | 0 | yes |
| figure | `thesis` `/model/fiscal_year_figures[]/vintage` | 2026-10-10 | 2026-10-10 | 686 | 0 | yes |
| figure | `thesis` `/model/forecast_figures[]/vintage` | 2026-10-10 | 2026-10-10 | 47 | 0 | yes |
| figure | `thesis` `/model_cases/base/px_last/vintage` | 2026-10-10 | 2026-10-10 | 1 | 0 | yes |
| object | `thesis` `/posture/as_of` | 2026-09-15 | 2026-10-10 | 1 | 18 | NO |
| object | `thesis` `/posture/comparable_membership/as_of` | 2026-09-15 | 2026-10-10 | 1 | 18 | NO |
| object | `thesis` `/posture/membership/as_of` | 2026-09-15 | 2026-10-10 | 1 | 18 | NO |
| object | `thesis` `/posture/posture_read/as_of` | 2026-09-15 | 2026-10-10 | 1 | 18 | NO |
| object | `thesis` `/scores/as_of` | 2026-09-17 | 2026-10-10 | 1 | 16 | NO |
| object | `thesis` `/scores/scores_read/as_of` | 2026-09-17 | 2026-10-10 | 1 | 16 | NO |

page states the cross-vintage itself (`peers.subject.cross_vintage_caveat`): yes -- the subject's scalars carry the model block's own vintage (2026-10-10T13:02:24Z); every candidate carries the scanner's asOf -- the band is graded ACROSS those two vintages and neither is re-dated

## ROG_SW_Equity

route status: thesis 200, peers 200 | header figures 22, header vintage date(s): {'2026-10-10': 22}

**FWD-8 peer identity** -- subject key equal on thesis and peers: True; crosswalk vintage equal: True (2026-10-09)
- members 12 | United States alphabetic 8 | resolvable (`<T> US`, or an all-digit ticker by its Japan code or a unique held name) 7 | served MEASURED 7
- served a key the pool does not hold under that form (leaked): 0 [] | resolvable but not served (missing): 0 [] | served a different key (wrong): 0 [] | rows with no identity.resolution: 0
- **agrees: YES**

**FWD-38 vintages** -- figure vintages within one trading day of the header's: 1644 of 1656; object as-of dates within one trading day: 2 of 10

| kind | route and path | date | header date | n | trading days behind | within 1 |
|---|---|---|---|---|---|---|
| object | `peers` `//as_of` | 2026-10-11 | 2026-10-10 | 1 | 0 | yes |
| object | `peers` `//universe_vintage` | 2026-10-02 | 2026-10-10 | 1 | 5 | NO |
| figure | `peers` `//vintage` | 2026-10-11 | 2026-10-10 | 1 | 0 | yes |
| figure | `peers` `/members[]/cap_vintage` | 2026-10-02 | 2026-10-10 | 12 | 5 | NO |
| object | `peers` `/peer_read/as_of` | 2026-10-11 | 2026-10-10 | 1 | 0 | yes |
| figure | `peers` `/subject/cap_vintage` | 2026-10-10 | 2026-10-10 | 1 | 0 | yes |
| figure | `peers` `/subject/market_cap_vintage` | 2026-10-10 | 2026-10-10 | 1 | 0 | yes |
| figure | `thesis` `/fiscal_year_figures[]/vintage` | 2026-10-10 | 2026-10-10 | 790 | 0 | yes |
| figure | `thesis` `/header_figures[]/vintage` | 2026-10-10 | 2026-10-10 | 22 | 0 | yes |
| object | `thesis` `/management/as_of` | 2026-10-07 | 2026-10-10 | 1 | 2 | NO |
| object | `thesis` `/management/object_as_of` | 2026-10-07 | 2026-10-10 | 1 | 2 | NO |
| figure | `thesis` `/model/fiscal_year_figures[]/vintage` | 2026-10-10 | 2026-10-10 | 790 | 0 | yes |
| figure | `thesis` `/model/forecast_figures[]/vintage` | 2026-10-10 | 2026-10-10 | 39 | 0 | yes |
| object | `thesis` `/posture/as_of` | 2026-09-16 | 2026-10-10 | 1 | 17 | NO |
| object | `thesis` `/posture/membership/as_of` | 2026-09-16 | 2026-10-10 | 1 | 17 | NO |
| object | `thesis` `/posture/posture_read/as_of` | 2026-09-16 | 2026-10-10 | 1 | 17 | NO |
| object | `thesis` `/scores/as_of` | 2026-09-17 | 2026-10-10 | 1 | 16 | NO |
| object | `thesis` `/scores/scores_read/as_of` | 2026-09-17 | 2026-10-10 | 1 | 16 | NO |

page states the cross-vintage itself (`peers.subject.cross_vintage_caveat`): yes -- the subject's scalars carry the model block's own vintage (2026-10-10T13:08:49Z); every candidate carries the scanner's asOf -- the band is graded ACROSS those two vintages and neither is re-dated

## Verdicts

| name | FWD-8 identity agrees | figure vintages within 1 trading day | object as-of within 1 trading day |
|---|---|---|---|
| ASML_NA_Equity | YES | 1675 of 1687 | 2 of 11 |
| BA_US_Equity | YES | 1448 of 1460 | 2 of 13 |
| ROG_SW_Equity | YES | 1644 of 1656 | 2 of 10 |

