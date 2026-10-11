# AMGT_RESAPP round 90 -- AMGT-oo-1, the whole-page read (FWD-8, FWD-38)

Live function `opal-amgt-scoped-api`, GET only, read 2026-10-11 by `2.0.0_SA_COO~R1`; trading-day distance from `lib/trading_calendar.trading_days_behind` (NYSE).

## ASML_NA_Equity

route status: thesis 200, peers 200 | header figures 24, header vintage date(s): {'2026-10-10': 24}

**FWD-8 peer identity** -- subject key equal on thesis and peers: True; crosswalk vintage equal: True (2026-10-09)
- members 12 | United States alphabetic 10 | resolvable (`<T> US`, or an all-digit ticker by its Japan code or a unique held name) 7 | served MEASURED 7
- served a key the pool does not hold under that form (leaked): 0 [] | resolvable but not served (missing): 0 [] | served a different key (wrong): 0 [] | rows with no identity.resolution: 0
- **agrees: YES**

**FWD-38 vintages** -- figure vintages within one trading day of the header's: 1674 of 1687; object as-of dates within one trading day: 0 of 11

| kind | route and path | date | header date | n | trading days behind | within 1 |
|---|---|---|---|---|---|---|
| object | `peers` `//as_of` | 2026-09-24 | 2026-10-10 | 1 | 11 | NO |
| object | `peers` `//universe_vintage` | 2026-08-06 | 2026-10-10 | 1 | 45 | NO |
| figure | `peers` `//vintage` | 2026-09-24 | 2026-10-10 | 1 | 11 | NO |
| figure | `peers` `/members[]/cap_vintage` | 2026-08-06 | 2026-10-10 | 12 | 45 | NO |
| object | `peers` `/peer_read/as_of` | 2026-09-24 | 2026-10-10 | 1 | 11 | NO |
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

page states the cross-vintage itself (`peers.subject.cross_vintage_caveat`): yes -- the subject's scalars carry the model block's own vintage (2026-09-19T07:53:19Z); every candidate carries the scanner's asOf -- the band is graded ACROSS those two vintages and neither is re-dated

## BA_US_Equity

route status: thesis 200, peers 200 | header figures 24, header vintage date(s): {'2026-10-10': 24}

**FWD-8 peer identity** -- subject key equal on thesis and peers: True; crosswalk vintage equal: True (2026-10-09)
- members 12 | United States alphabetic 12 | resolvable (`<T> US`, or an all-digit ticker by its Japan code or a unique held name) 6 | served MEASURED 6
- served a key the pool does not hold under that form (leaked): 0 [] | resolvable but not served (missing): 0 [] | served a different key (wrong): 0 [] | rows with no identity.resolution: 0
- **agrees: YES**

**FWD-38 vintages** -- figure vintages within one trading day of the header's: 1447 of 1460; object as-of dates within one trading day: 0 of 13

| kind | route and path | date | header date | n | trading days behind | within 1 |
|---|---|---|---|---|---|---|
| object | `peers` `//as_of` | 2026-09-24 | 2026-10-10 | 1 | 11 | NO |
| object | `peers` `//universe_vintage` | 2026-08-06 | 2026-10-10 | 1 | 45 | NO |
| figure | `peers` `//vintage` | 2026-09-24 | 2026-10-10 | 1 | 11 | NO |
| figure | `peers` `/members[]/cap_vintage` | 2026-08-06 | 2026-10-10 | 12 | 45 | NO |
| object | `peers` `/peer_read/as_of` | 2026-09-24 | 2026-10-10 | 1 | 11 | NO |
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

page states the cross-vintage itself (`peers.subject.cross_vintage_caveat`): yes -- the subject's scalars carry the model block's own vintage (2026-09-19T07:53:20Z); every candidate carries the scanner's asOf -- the band is graded ACROSS those two vintages and neither is re-dated

## ROG_SW_Equity

route status: thesis 200, peers 200 | header figures 22, header vintage date(s): {'2026-10-10': 22}

**FWD-8 peer identity** -- subject key equal on thesis and peers: True; crosswalk vintage equal: True (2026-10-09)
- members 12 | United States alphabetic 8 | resolvable (`<T> US`, or an all-digit ticker by its Japan code or a unique held name) 7 | served MEASURED 7
- served a key the pool does not hold under that form (leaked): 0 [] | resolvable but not served (missing): 0 [] | served a different key (wrong): 0 [] | rows with no identity.resolution: 0
- **agrees: YES**

**FWD-38 vintages** -- figure vintages within one trading day of the header's: 1643 of 1656; object as-of dates within one trading day: 0 of 10

| kind | route and path | date | header date | n | trading days behind | within 1 |
|---|---|---|---|---|---|---|
| object | `peers` `//as_of` | 2026-09-24 | 2026-10-10 | 1 | 11 | NO |
| object | `peers` `//universe_vintage` | 2026-08-06 | 2026-10-10 | 1 | 45 | NO |
| figure | `peers` `//vintage` | 2026-09-24 | 2026-10-10 | 1 | 11 | NO |
| figure | `peers` `/members[]/cap_vintage` | 2026-08-06 | 2026-10-10 | 12 | 45 | NO |
| object | `peers` `/peer_read/as_of` | 2026-09-24 | 2026-10-10 | 1 | 11 | NO |
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

page states the cross-vintage itself (`peers.subject.cross_vintage_caveat`): yes -- the subject's scalars carry the model block's own vintage (2026-09-19T07:53:36Z); every candidate carries the scanner's asOf -- the band is graded ACROSS those two vintages and neither is re-dated

## Verdicts

| name | FWD-8 identity agrees | figure vintages within 1 trading day | object as-of within 1 trading day |
|---|---|---|---|
| ASML_NA_Equity | YES | 1674 of 1687 | 0 of 11 |
| BA_US_Equity | YES | 1447 of 1460 | 0 of 13 |
| ROG_SW_Equity | YES | 1643 of 1656 | 0 of 10 |


## Findings (issuer, `2.0.0_SA_COO~R1`, 2026-10-11 ~06:0xZ)

Names: ASML_NA_Equity (the round's named subject), BA_US_Equity (a United States control, 12 of 12 United States members), ROG_SW_Equity
(a Swiss subject whose peers mix SEDOL stems, a UK listing and United States listings). Script: `reads/r90_whole_page_read.py`.

1. **FWD-8 (peer identity agrees with the header company's comparison basis): YES on 3 of 3 names.** The subject key and the crosswalk
   vintage (2026-10-09) are equal on /thesis and /peers; 0 leaked keys, 0 wrong keys, 0 resolvable-but-unserved, 0 rows without an
   `identity.resolution` (ASML 12 members, 7 served MEASURED of 7 resolvable; BA 12 of 12, 6 of 6; ROG 12, 7 of 7 including the
   three non-US members matched by company name). My first run flagged ROG's three name-matched members as "leaked" because the
   expectation covered only `<T> US`; the expectation now includes the route's own all-digit rule, recomputed independently.
2. **FWD-38 (every dated figure's vintage within one trading day of the header's): NOT MET as worded.**
   - Figure vintages: **4,764 of 4,803** within one trading day (1,674 of 1,687 ASML; 1,447 of 1,460 BA; 1,643 of 1,656 ROG). The
     39 outside are, per name, `peers.members[].cap_vintage` = 2026-08-06 (12 members, 45 trading days behind the header's
     2026-10-10) and `peers.vintage` = 2026-09-24 (11 behind). The stored peers object was built against scanner database vintage
     2026-08-06; the live scanner universes read asOf 2026-10-02, so the peer caps on the page are eight weeks older than the
     scanner now holds. The page does state the cross-vintage on the SUBJECT (`peers.subject.cross_vintage_caveat`), not per member.
   - Object as-of dates (posture 2026-09-15/16, scores 2026-09-17, management 2026-09-15 to 2026-10-07, peers 2026-09-24): **0 of 34**
     within one trading day. Each carries its own `as_of`; none claims to be daily.
3. **What this lets a later round grade.** FWD-8's identity half can be graded on this read for these three names. FWD-38 needs a
   standard before it can be graded: figures against the header (met except the peer caps), or every object's as-of (not met by
   design). The one actionable defect is the peers object's refresh (a producer-side rebuild against the 2026-10-02 scanner); it is
   not a cell in this round (producer, not the served function) and is named in the round's message to the CTO.

checked 3 of 3 names (denominators printed per name above)
