# CB-bx-3 -- every fund series classed by its trades, set beside the reinvestment classes (round 76, 0.9.0_WK_ADVI_COTBKF~140)

Generated 2026-10-11T23:13:01Z. Counts, ratios, tickers and dates only. Record: `FUNDS_BY_TRADES.json`; per fund: `FUNDS_BY_TRADES.csv`. Rule written 2026-10-11T23:07:58Z before any fund was classed (`rule.text` in the record). No correction is proposed.

**Headline.** Of 270 fund series under the rule written at 2026-10-11T23:07:58Z: 15 fails, 17 passes, 0 mixed, 60 too_few, 178 no_trade_row (sum 270). The 15 failing funds are ALL left on the store; the 17 passing funds are 15 substituted funds plus the commodity trusts PHYS and PSLV; no substituted fund fails. The 19 moved: 8 fail (ABNFX, BALCX, DFLVX, DISVX, FCNTX, MEIIX, PRILX, VEIRX), 10 are too_few (1 to 4 decisive units) and ACTDX has no trade row; none passes. 14 unreadable-by-reinvestment funds change class (7 fail: PCBIX, SGIIX, GFFFX, FOCPX, AGTHX, NFFFX, VGHAX; 7 pass: FSMAX, MIEKX, MISIX, PSLV, PHYS, FSPSX, FXAIX). Conflicts with the reinvestment reading: 0. VEIRX and PCBIX carry 3022 of the 3432 failing units of all funds. 178 series have no read unit and 60 are too_few, so 238 of 270 series are not classed by trades.

## The rule (written first, kept)

- Unit: record A's (account, effective day, fund, kind); ratio = served close over price paid. PASS within 1 percent. UNRESOLVED (neither): 1 to 5 percent off either way; a purchase up to 5.75 percent below the close (a front load); a charge-sized gap (up to 34.15 dollars in the charge direction, constants from record B's post hoc list). FAIL: every other unit; a sale is never excused by a front load.
- `minimum_rows` 5 decisive units on at least 3 distinct days, else `too_few`. `share_fails` 0.50: above it `fails`; at or below 0.10 `passes`; between `mixed`. Guard: a fund `passes` only with at least 5 decisive units on 3 days before the 180-day window ending at the latest served date, else `too_few`. `no_trade_row` = no read unit (23 with no purchase/sale row, 155 with rows all before the first stored close; one class, two reason codes).

## Five classes over 270

| fails | passes | mixed | too_few | no_trade_row | sum |
|---|---|---|---|---|---|
| 15 | 17 | 0 | 60 | 178 | 270 |

## Against the earlier classes (series)

| group | series | fails | passes | mixed | too_few | no_trade_row |
|---|---|---|---|---|---|---|
| the 19 moved | 19 | 8 | 0 | 0 | 10 | 1 |
| the 33 validated | 33 | 8 | 10 | 0 | 14 | 1 |
| - validated, left on the store | 19 | 8 | 0 | 0 | 10 | 1 |
| - validated, substituted | 14 | 0 | 10 | 0 | 4 | 0 |
| the 237 unreadable | 237 | 7 | 7 | 0 | 46 | 177 |
| - unreadable, left on the store | 178 | 7 | 2 | 0 | 34 | 135 |
| - unreadable, substituted | 59 | 0 | 5 | 0 | 12 | 42 |
| the 73 substituted | 73 | 0 | 15 | 0 | 16 | 42 |
| the 197 left on the store | 197 | 15 | 2 | 0 | 44 | 136 |

By round 72: confirmed_adjusted (19) -> {"fails": 9, "passes": 0, "mixed": 0, "too_few": 10, "no_trade_row": 0}; confirmed_not (15) -> {"fails": 0, "passes": 12, "mixed": 0, "too_few": 2, "no_trade_row": 1}; nothing_to_test_on (236) -> {"fails": 6, "passes": 5, "mixed": 0, "too_few": 48, "no_trade_row": 177}.

## Funds that change class (unreadable by reinvestment, now fails or passes by trades): 14

| ticker | by trades | group | read units | decisive | failing | median ratio | round 72 |
|---|---|---|---|---|---|---|---|
| PCBIX | fails | left_on_store | 1453 | 1426 | 1426 | 0.748864 | confirmed_adjusted |
| SGIIX | fails | left_on_store | 46 | 43 | 40 | 0.742176 | confirmed_adjusted |
| GFFFX | fails | left_on_store | 35 | 35 | 34 | 0.67923 | nothing_to_test_on |
| FOCPX | fails | left_on_store | 25 | 25 | 25 | 0.639107 | nothing_to_test_on |
| AGTHX | fails | left_on_store | 10 | 10 | 10 | 0.464906 | nothing_to_test_on |
| NFFFX | fails | left_on_store | 6 | 6 | 6 | 0.804542 | nothing_to_test_on |
| VGHAX | fails | left_on_store | 5 | 5 | 5 | 0.661119 | nothing_to_test_on |
| FSMAX | passes | substituted | 2281 | 2281 | 0 | 1.0 | confirmed_not |
| MIEKX | passes | substituted | 2153 | 2153 | 0 | 1.0 | nothing_to_test_on |
| MISIX | passes | substituted | 1129 | 1085 | 0 | 1.0 | nothing_to_test_on |
| PSLV | passes | left_on_store | 54 | 36 | 3 | 1.00122 | nothing_to_test_on |
| PHYS | passes | left_on_store | 51 | 45 | 0 | 0.999764 | nothing_to_test_on |
| FSPSX | passes | substituted | 28 | 28 | 0 | 1.000001 | confirmed_not |
| FXAIX | passes | substituted | 7 | 7 | 0 | 1.0 | nothing_to_test_on |

## Conflicts with the reinvestment reading: 0

No validated left-on-store fund passes; no validated substituted fund fails; no round-72 confirmed_not fund fails; no round-72 confirmed_adjusted fund passes. Round-71 adjusted funds that pass by trades: none. The two instruments agree wherever both speak; the disagreement is only in coverage (the 14 above read by trades what reinvestment could not).

## Substituted funds that fail

None is classed `fails`. Substituted funds with a failing unit: SWPPX 1 of 1 decisive units (too_few); VFIAX 1 of 99 decisive units (passes). VBIRX passes on 16 within-1-percent units and 44 unresolved (it would fail with the charge excuse off).

## The named failing funds (15; all left on the store; VBTLX is not among them, it is too_few)

| ticker | group | read units | failing | median ratio (all / failing) | first failing | last failing | round 74 / round 72 |
|---|---|---|---|---|---|---|---|
| VEIRX | left_on_store | 1596 | 1596 | 0.626575 / 0.626575 | 2023-02-17 | 2024-11-20 | validated / confirmed_adjusted |
| PCBIX | left_on_store | 1453 | 1426 | 0.748864 / 0.748864 | 2021-08-27 | 2024-11-27 | unreadable / confirmed_adjusted |
| ABNFX | left_on_store | 195 | 177 | 0.856716 / 0.856716 | 2022-05-16 | 2025-01-13 | validated / confirmed_adjusted |
| SGIIX | left_on_store | 46 | 40 | 0.742176 / 0.683119 | 2020-07-10 | 2025-08-15 | unreadable / confirmed_adjusted |
| GFFFX | left_on_store | 35 | 34 | 0.67923 / 0.679222 | 2020-07-13 | 2025-10-15 | unreadable / nothing_to_test_on |
| FOCPX | left_on_store | 25 | 25 | 0.639107 / 0.639107 | 2021-10-22 | 2024-10-17 | unreadable / nothing_to_test_on |
| FCNTX | left_on_store | 21 | 15 | 0.909629 / 0.909629 | 2023-11-21 | 2025-10-24 | validated / confirmed_adjusted |
| PRILX | left_on_store | 13 | 13 | 0.415777 / 0.415777 | 2022-01-06 | 2023-02-21 | validated / confirmed_adjusted |
| BALCX | left_on_store | 12 | 12 | 0.75864 / 0.75864 | 2022-05-09 | 2023-03-01 | validated / nothing_to_test_on |
| AGTHX | left_on_store | 10 | 10 | 0.464906 / 0.464906 | 2020-08-31 | 2025-03-12 | unreadable / nothing_to_test_on |
| DISVX | left_on_store | 6 | 6 | 0.810315 / 0.810315 | 2022-02-28 | 2024-08-20 | validated / confirmed_adjusted |
| DFLVX | left_on_store | 7 | 6 | 0.860662 / 0.855621 | 2021-01-25 | 2023-06-27 | validated / confirmed_adjusted |
| NFFFX | left_on_store | 6 | 6 | 0.804542 / 0.804542 | 2022-01-25 | 2025-07-08 | unreadable / nothing_to_test_on |
| MEIIX | left_on_store | 6 | 5 | 0.576683 / 0.53817 | 2021-04-26 | 2024-10-30 | validated / confirmed_adjusted |
| VGHAX | left_on_store | 5 | 5 | 0.661119 / 0.661119 | 2024-01-26 | 2025-03-20 | unreadable / nothing_to_test_on |

## Not established

- WHY a failing fund fails: the instrument compares the served close with Amount over Quantity; it does not say adjusted, a charge or a mis-scale. A fails class says the served close does not reproduce the price paid on most decisive trades; the named list is where a named correction would start, nothing more.
- The 178 no_trade_row series (23 with no purchase/sale row, 155 with rows all before the first stored close) and the 60 too_few series are not classed by trades; 238 of 270. 76790 of 91040 units pre-date a first stored close and are not read.
- Mixed is empty: under the rule every fund with enough decisive units was either at or below a 10 percent failing share or above 50 percent. Whether that is the data or the width of the unresolved band is not tested.
- Unresolved units (1-to-5 percent off; purchases up to 5.75 percent below the close; charge-sized gaps up to 34.15 dollars) are neither pass nor fail. A pass can rest on a minority of a fund's units: VBIRX has more unresolved than decisive units. The charge-sized constants come from record B section 6 (post hoc, read off the 19 funds, not a test).
- SENSITIVITY (marked NOT the result; classed under the rule as written): charge excuse off: {"VBIRX": "passes->fails"}; pass line 0.05: {"PSLV": "passes->mixed"}; minimum_rows 3: {"AMBFX": "too_few->fails", "CAIBX": "too_few->fails", "DFREX": "too_few->fails", "ANCFX": "too_few->fails", "ANWPX": "too_few->fails"}; minimum_rows 10: {"DFIEX": "passes->too_few", "DFCEX": "passes->too_few", "DISVX": "fails->too_few", "DFLVX": "fails->too_few", "FXAIX": "passes->too_few", "MEIIX": "fails->too_few", "NFFFX": "fails->too_few", "VGHAX": "fails->too_few"}; guard off: {"NEA": "too_few->passes"}; fail line 0.40 and 0.60, pass line 0.20 and guard window 365 days: no fund changes.
- VBIRX (a substituted fund, whose served close is the vendor unadjusted close) passes only through the charge-sized excuse: 16 of its 60 read units are within 1 percent and 44 are unresolved; with the excuse off it would fail. PHYS and PSLV pass but record A notes that a within-1-percent left-on-store reading does not show an unadjusted series: a non-distributing trust has the same adjusted and unadjusted close.
- A fund's units are not independent: accounts trading one day share the close, so the failing share is a share of units, not of trades or accounts. The recent-window guard (180 days before the latest served date) was fixed in advance and its length is a judgment.
- VBTLX is excluded by the CTO from every count until its cause has a name. The rule class for it is too_few (1 decisive unit, 0 failing); it is one of the 60 too_few so the five counts sum to 270, and it is not in named. The csv schema has exactly the nine columns the order lists and no column to flag it excluded; the flag is in against_earlier.excluded_tickers and this note.
- The round 71, 72, 73 and 74 readings are read from their records as filed; none was rerun. The round-71 funds read adjusted that pass by trades: none; the round-71 funds read not adjusted that fail by trades: none.
- Recomputed here: the read units (account, effective day, fund, kind) by the recipe of record A (same data, same guard, same day convention) with the dollar gap per unit added; per-fund unit totals equal PRICE_PAID.csv trade_rows for all 270 funds (14250 in all, 92 funds, 91040 units before the close filter). No account id, amount or quantity is written.
