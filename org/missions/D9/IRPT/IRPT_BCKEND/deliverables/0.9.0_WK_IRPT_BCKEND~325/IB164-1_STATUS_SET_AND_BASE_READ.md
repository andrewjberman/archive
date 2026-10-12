# IB-pr-470: the closed status set, the NON-POSITIVE-BASE days by what the account held the day before, and the accounts whose claim moves

Base `13e1d6d3fb`. READ ONLY. Arm `READER_CODE_OVER_SERVED_GOLD` (IB-pr-467's, not the deployed route). Latest landed day read: 2026-10-08. Partitions read: the 49F entry 566, orion 1619. Counts only; no account id, balance, return or cash amount is written.

## Answer first: NON-POSITIVE-BASE days in an account that held a position the day before

- the 49F entry SI: all positions 5 of 1223 days (interior 3 of 637); not_determinable 0; with non-zero cash 1219
- the 49F entry YTD: all positions 3 of 1007 days (interior 1 of 364); not_determinable 0; with non-zero cash 1005
- the 49F entry QTD: all positions 0 of 0 days (interior 0 of 0); not_determinable 0; with non-zero cash 0
- the 49F entry 1Y: all positions 3 of 1089 days (interior 1 of 563); not_determinable 0; with non-zero cash 1087
- orion SI: all positions 539402 of 539402 days (interior 3280 of 3280); not_determinable 0; with non-zero cash 0
- orion YTD: all positions 14385 of 14385 days (interior 799 of 799); not_determinable 0; with non-zero cash 0
- orion QTD: all positions 28 of 28 days (interior 0 of 0); not_determinable 0; with non-zero cash 0
- orion 1Y: all positions 22861 of 22861 days (interior 1261 of 1261); not_determinable 0; with non-zero cash 0

Reading the classes: a `held_none` NON-POSITIVE-BASE day is, by the producer's conditions (:869, :872), a day with no position row and a non-zero cash balance that is negative (a debit); the 49F entry's days are almost all of that kind (the `with non-zero cash` figure beside each cell). The orion days all carry zero cash and a position row: by the conditions, included rows all valued exactly zero (held_included_only_or_mixed), or negative keys with no included row (held_other). The gold carries counts and cash, not the cause.


## Status tokens in the producer (data/assets/scripts/gold/irpt_holdings_performance/holdings_performance.py)

- `OK` defined 219, assigned 873: np.select default (:874): none of the three conditions is true, i.e. the basket (included holdings plus positive cash) is above zero or the account is pure cash; the return is computed (:875-878). It can later be overwritten by IMPLAUSIBLE-RETURN (:883) or FOLLOWS-DISCONTINUITY (:952).
- `NO-PRIOR-HOLDINGS` defined 220, assigned 873: np.select choice 1, condition at :869: held_count == 0 and cash_value == 0.0 -- no position row (included, excluded or negative) and exactly zero cash on the prior trading day.
- `ALL-HOLDINGS-EXCLUDED` defined 222, assigned 873: np.select choice 2, conditions at :870-871: held_count > 0, included_count == 0, negative_count == 0 and cash_value <= 0.0 -- the account held positions, none reached the basket (no identifier, or no price on both days), none was negative, and there is no positive cash.
- `NON-POSITIVE-BASE` defined 221, assigned 873: np.select choice 3, condition at :872: account_value <= 0.0 (account_value = included_value + positive cash, :856), reached only when neither earlier condition is true. By the first two conditions that means: (a) no position row and non-zero cash that is negative (a debit; positive cash would make the basket positive); (b) at least one negative position row, no included row, cash <= 0; (c) at least one included row of total value exactly 0 (included rows are value >= 0) and cash <= 0.
- `IMPLAUSIBLE-RETURN` defined 223, assigned 883: after the grade, a row that is status OK whose computed daily_return is <= -1.0 or >= 1.0 (_IMPLAUSIBLE_LO/_HI, :169; mask :881-882) is overwritten (:883) and its return nulled (:884).
- `FOLLOWS-DISCONTINUITY` defined 224, assigned 952: apply_follow_day_rule (:939-955): a row that is still OK whose account was IMPLAUSIBLE-RETURN on the previous trading day (ImplausibleIndex, :907-936) is overwritten; does not cascade.

Can a token outside the constants be written: NO. The column is written at three places in the whole producer package (data/assets/scripts/gold/irpt_holdings_performance/, two modules): np.select (data/assets/scripts/gold/irpt_holdings_performance/holdings_performance.py:873-874) whose choices are three constants and whose default is STATUS_OK; the implausible overwrite (:883, STATUS_IMPLAUSIBLE); the follow-day overwrite (:952, STATUS_FOLLOWS_DISCONTINUITY). holdings_comparison.py only reads the column (:223). A grep of the package for assignments to the status column finds no other writer. The gold's tokens are checked in status_counts_over_the_served_gold.

## Counts over the served gold (every landed partition <= 2026-10-08)

| entry | partitions | rows | OK | NO-PRIOR-HOLDINGS | ALL-HOLDINGS-EXCLUDED | NON-POSITIVE-BASE | IMPLAUSIBLE-RETURN | FOLLOWS-DISCONTINUITY | in gold, not in code |
|---|---|---|---|---|---|---|---|---|---|
| the 49F entry | 566 | 3256566 | 2841381 | 413118 | 467 | 1596 | 2 | 2 | none |
| orion | 1619 | 1430575 | 855536 | 0 | 0 | 575039 | 0 | 0 | none |

## Assignment order

np.select takes the FIRST true condition (data/assets/scripts/gold/irpt_holdings_performance/holdings_performance.py:873-874): NO-PRIOR-HOLDINGS (:869), then ALL-HOLDINGS-EXCLUDED (:870-871), then NON-POSITIVE-BASE (:872), default OK. The code comment at :861-868 states that ALL-HOLDINGS-EXCLUDED is evaluated first so a full exit does not read NON-POSITIVE-BASE.

Can an account holding only excluded, non-negative positions receive NON-POSITIVE-BASE: **NO**. An account holding only excluded, non-negative positions (held_count > 0, included_count 0, negative_count 0) has cash_value either <= 0, which meets the ALL-HOLDINGS-EXCLUDED condition (:870-871) first, or > 0, which makes account_value > 0 (:856, the OK default), so NON-POSITIVE-BASE is unreachable for it. The cases that DO receive NON-POSITIVE-BASE are exactly: (a) no position row and negative cash (a debit); (b) one or more negative position rows, no included row, cash <= 0 (any excluded rows beside them); (c) one or more included rows all valued exactly 0, with cash <= 0 (any excluded or negative rows beside them). Measured cross-check: NON-POSITIVE-BASE days placed held_only_excluded in all cells, all positions, with or without a figure: 0.

## Prior-day holdings rule

The gold carries the four count columns the face names, under these served names: held_count, included_count, negative_count, cash_value (plus excluded_count, which was already read). They describe the account's positions on the BASE day, the prior trading day (or the last close that exists when the row links across a gap): holdings_return(p0, p1, cash, ..., prev_day=base_day) is called with the base-day positions p0 and the base-day cash (data/assets/scripts/gold/irpt_holdings_performance/holdings_performance.py:1065; counts at :843-847; the call reads prev_positions at :758). A 'position row' is a key (identifier, lots summed): held_count = included + excluded + negative keys. The six classes, from the NON-POSITIVE-BASE row's own columns: held_none = held_count 0; held_included_only_or_mixed = included_count >= 1; held_only_negative = every key negative (negative_count == held_count > 0); held_only_excluded = held_count > 0 with included_count 0 and negative_count 0; held_other = held_count > 0, included_count 0, negative_count > 0 and excluded_count > 0; not_determinable = any of the four counts null, or held_count != included + excluded + negative. non_positive_base_all_positions_with_nonzero_cash counts the days (all positions) whose cash_value is not zero.

## the 49F entry: NON-POSITIVE-BASE days by what the account held the prior day

| window | scope | days | held_none | held_included_only_or_mixed | held_only_excluded | held_only_negative | held_other | not_determinable | nonzero cash | accounts with a figure | claim: measured today | as written | if NPB with a prior position also |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| SI | interior | 637 | 634 | 3 | 0 | 0 | 0 | 0 | - | 6896 | 6896 | 18 | 23 |
| SI | all positions | 1223 | 1218 | 4 | 0 | 1 | 0 | 0 | 1219 | 6896 | 6896 | 18 | 23 |
| YTD | interior | 364 | 363 | 1 | 0 | 0 | 0 | 0 | - | 6832 | 6832 | 16 | 19 |
| YTD | all positions | 1007 | 1004 | 2 | 0 | 1 | 0 | 0 | 1005 | 6832 | 6832 | 16 | 19 |
| QTD | interior | 0 | 0 | 0 | 0 | 0 | 0 | 0 | - | 6722 | 6722 | 2 | 2 |
| QTD | all positions | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 6722 | 6722 | 2 | 2 |
| 1Y | interior | 563 | 562 | 1 | 0 | 0 | 0 | 0 | - | 6840 | 6840 | 17 | 20 |
| 1Y | all positions | 1089 | 1086 | 2 | 0 | 1 | 0 | 0 | 1087 | 6840 | 6840 | 17 | 20 |

Where the all-positions days sit (before the first OK day / interior / after the last OK day, of which the last row):

- SI: 90 / 637 / 496 (last row 6); excluded days in accounts with a figure, by status: {"ALL-HOLDINGS-EXCLUDED": 157, "FOLLOWS-DISCONTINUITY": 2, "IMPLAUSIBLE-RETURN": 2, "NO-PRIOR-HOLDINGS": 129207, "NON-POSITIVE-BASE": 1223}; interior reproduces IB-pr-467 (637): yes
- YTD: 148 / 364 / 495 (last row 6); excluded days in accounts with a figure, by status: {"ALL-HOLDINGS-EXCLUDED": 144, "NO-PRIOR-HOLDINGS": 36702, "NON-POSITIVE-BASE": 1007}; interior reproduces IB-pr-467 (364): yes
- QTD: 0 / 0 / 0 (last row 0); excluded days in accounts with a figure, by status: {"ALL-HOLDINGS-EXCLUDED": 6, "NO-PRIOR-HOLDINGS": 124}; interior reproduces IB-pr-467 (0): yes
- 1Y: 30 / 563 / 496 (last row 6); excluded days in accounts with a figure, by status: {"ALL-HOLDINGS-EXCLUDED": 151, "FOLLOWS-DISCONTINUITY": 2, "IMPLAUSIBLE-RETURN": 2, "NO-PRIOR-HOLDINGS": 50971, "NON-POSITIVE-BASE": 1089}; interior reproduces IB-pr-467 (563): yes

## orion: NON-POSITIVE-BASE days by what the account held the prior day

| window | scope | days | held_none | held_included_only_or_mixed | held_only_excluded | held_only_negative | held_other | not_determinable | nonzero cash | accounts with a figure | claim: measured today | as written | if NPB with a prior position also |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| SI | interior | 3280 | 0 | 3268 | 0 | 0 | 12 | 0 | - | 926 | 926 | 0 | 894 |
| SI | all positions | 539402 | 0 | 539338 | 0 | 0 | 64 | 0 | 0 | 926 | 926 | 0 | 894 |
| YTD | interior | 799 | 0 | 792 | 0 | 0 | 7 | 0 | - | 906 | 906 | 0 | 200 |
| YTD | all positions | 14385 | 0 | 14327 | 0 | 0 | 58 | 0 | 0 | 906 | 906 | 0 | 200 |
| QTD | interior | 0 | 0 | 0 | 0 | 0 | 0 | 0 | - | 805 | 805 | 0 | 7 |
| QTD | all positions | 28 | 0 | 28 | 0 | 0 | 0 | 0 | 0 | 805 | 805 | 0 | 7 |
| 1Y | interior | 1261 | 0 | 1254 | 0 | 0 | 7 | 0 | - | 916 | 916 | 0 | 240 |
| 1Y | all positions | 22861 | 0 | 22802 | 0 | 0 | 59 | 0 | 0 | 916 | 916 | 0 | 240 |

Where the all-positions days sit (before the first OK day / interior / after the last OK day, of which the last row):

- SI: 522241 / 3280 / 13881 (last row 125); excluded days in accounts with a figure, by status: {"NON-POSITIVE-BASE": 539402}; interior reproduces IB-pr-467 (3280): yes
- YTD: 4849 / 799 / 8737 (last row 105); excluded days in accounts with a figure, by status: {"NON-POSITIVE-BASE": 14385}; interior reproduces IB-pr-467 (799): yes
- QTD: 9 / 0 / 19 (last row 4); excluded days in accounts with a figure, by status: {"NON-POSITIVE-BASE": 28}; interior reproduces IB-pr-467 (0): yes
- 1Y: 10588 / 1261 / 11012 (last row 115); excluded days in accounts with a figure, by status: {"NON-POSITIVE-BASE": 22861}; interior reproduces IB-pr-467 (1261): yes

## Control

In memory only: plant account A with one ALL-HOLDINGS-EXCLUDED day and account B with one NO-PRIOR-HOLDINGS day (each between two OK days) and run the step-5 counter (moves()) on each; plant C and D, each with one NON-POSITIVE-BASE day (C with a prior included position, D with no prior position), to run the second reading; and run the six-class function on seven planted count rows.

Reading: {"expected": "A moves as written (True, True); B does not (False, False); C moves only under the second reading (False, True); D does not (False, False); classes held_none, held_included_only_or_mixed, held_only_negative, held_only_excluded, held_other, not_determinable, not_determinable: HELD", "moves_as_written_and_if_npb_prior_position_also": {"A_single_ALL-HOLDINGS-EXCLUDED": [true, true], "B_single_NO-PRIOR-HOLDINGS": [false, false], "C_single_NON-POSITIVE-BASE_prior_included_position": [false, true], "D_single_NON-POSITIVE-BASE_held_none": [false, false]}, "six_classes_of_the_planted_rows": ["held_none", "held_included_only_or_mixed", "held_only_negative", "held_only_excluded", "held_other", "not_determinable", "not_determinable"]}

## Not established

- the deployed route's own answer: no Lambda invoked, no sign-in; the deployed package, mapping loader, authorization and envelope were not exercised
- the C-CHAINCLAIM contract's own definition of 'excluded day' and of the claim: only the face's description was used; the PRD addendum text was not graded here
- whether a NON-POSITIVE-BASE day in an account that held a position left a return out in the account's real history: the gold carries the base-day counts and cash, not prices or cash flows, so a zero-valued included position or a negative key is seen, its cause is not
- accounts the reader refuses (no OK row in the window) are not part of 'accounts with a figure'; their NON-POSITIVE-BASE days are reported separately by class and are in no claim-move count
- the producer's status grade was read from the code at the base commit; the gold's partitions were not regenerated, and the silver (prices, identifiers, balances) was not read
- the gold was read once, at the time of this run, capped at 2026-10-08; a later partition may have landed
- the transport check of IB-pr-464 (stand-in versus the reader's own HoldingsGoldSource class) was not repeated: the same stand-in is used; the reproduction of IB-pr-467's interior NON-POSITIVE-BASE counts is the check

Zeros: functions invoked 0, sign-ins 0, AWS writes 0, accounts written 0, values written 0, product files edited 0.
