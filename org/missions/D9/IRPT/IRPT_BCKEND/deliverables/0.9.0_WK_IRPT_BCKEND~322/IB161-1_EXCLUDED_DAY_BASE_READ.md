# IB-pr-467: the reader's interior and last-row excluded days -- what the base was (zero, negative, positive) and how long the zero run

Base `c45e2c5857`. READ ONLY. Arm `READER_CODE_OVER_SERVED_GOLD` (IB-pr-464's, unchanged; NOT the deployed route). Latest landed day read: 2026-10-08 (both entries). Every partition at or before it read once: the 49F entry 566, orion 1619. Counts only; no account id, balance or return is written.

## Answer, leading with the negative and positive-flagged counts (accounts with an interior or last-row excluded day)

**the 49F entry** (primary basis: the row's own account_value, the producer's base):
- SI: 400 accounts; negative base on one or more days: 0; positive flagged base on one or more days: 2; every counted day on a zero base: 398; reproduces IB-pr-464: yes
- YTD: 212 accounts; negative base on one or more days: 0; positive flagged base on one or more days: 0; every counted day on a zero base: 212; reproduces IB-pr-464: yes
- QTD: 5 accounts; negative base on one or more days: 0; positive flagged base on one or more days: 0; every counted day on a zero base: 5; reproduces IB-pr-464: yes
- 1Y: 247 accounts; negative base on one or more days: 0; positive flagged base on one or more days: 2; every counted day on a zero base: 245; reproduces IB-pr-464: yes

**orion** (primary basis: the row's own account_value, the producer's base):
- SI: 178 accounts; negative base on one or more days: 0; positive flagged base on one or more days: 0; every counted day on a zero base: 178; reproduces IB-pr-464: yes
- YTD: 116 accounts; negative base on one or more days: 0; positive flagged base on one or more days: 0; every counted day on a zero base: 116; reproduces IB-pr-464: yes
- QTD: 4 accounts; negative base on one or more days: 0; positive flagged base on one or more days: 0; every counted day on a zero base: 4; reproduces IB-pr-464: yes
- 1Y: 130 accounts; negative base on one or more days: 0; positive flagged base on one or more days: 0; every counted day on a zero base: 130; reproduces IB-pr-464: yes

## What the base is (producer)

- The producer's base is the row's OWN account_value: holdings_performance.py:856 sets account_value = included_value + basket_cash, from the PREVIOUS trading day's positions (holdings_return(prev_positions, day_positions, ...), :743-758; the comment at :857-858 'the whole t-1 book'), and the third np.select condition at :872 (account_value <= 0.0 -> NON-POSITIVE-BASE, assigned at :873-874) tests that same column; daily_return is account-value-divided at :876. The gold therefore carries the base in its own column, and the PRIMARY classes in this file use it: a day's 'prior value' is the row's own account_value, which is the account's basket at the close of the day before. The account_value on the account's PREVIOUS row is a different number, the basket at the close of the day before that, and so a proxy, not the base; it is reported separately for every cell under literal_previous_row (same tables, same sums). Not the reader's end_value: the reader reads the first and last OK rows' account_value (holdings_gold.py:274-275).

- Tolerance: Exactly 0.0 (v == 0.0). No tolerance. A nonzero value is negative or positive by its sign however small; the count of counted days within a cent (0 < |v| < 0.01) of zero but not zero is days_within_a_cent_of_zero_but_not_zero per cell under primary_own_row_base and literal_previous_row. no_prior_row: for the primary basis, the row's own account_value is null; for the literal rule, the account has no earlier row in the gold or it is null.
- Day rule: Per account that the reader gives a figure and with a non-OK day (IB-pr-464's set), take its rows inside the window in date order. A non-OK row (the reader's test, holdings_gold.py:246) is INTERIOR when it lies after the account's first OK row and before its last OK row (between two OK days, chained across); it is the LAST ROW when it is the account's final row in the window and non-OK. A non-OK row before the first OK row is a first-day exclusion and is not counted. A non-OK row after the last OK row that is not the final row (a trailing run longer than one) is neither of the two and is counted only in trailing_nonok_days_neither_interior_nor_last_row. days_counted = interior_days + last_row_days.
- Zero run: For a counted day whose prior value is zero, count the consecutive rows of the account in the gold (across all landed partitions up to 2026-10-08, not only the window) whose account_value is exactly 0.0, going back from the day's own row for the primary basis (row i is zero means the close of the day before is zero; 1 = only the close of the day before), and going back from the previous row for literal_previous_row (1 = only the previous row). Bins 1, 2, 3-5, 6-20, 21-60, more (over 60).

## the 49F entry

| window | accounts | interior days | last-row days | days counted | all-zero accounts | with a negative | with a positive flagged | within a cent, not zero | trailing (neither) | previous row not the previous partition |
|---|---|---|---|---|---|---|---|---|---|---|
| SI | 400 | 16107 | 178 | 16285 | 398 | 0 | 2 | 0 | 33472 | 1 |
| YTD | 212 | 4339 | 114 | 4453 | 212 | 0 | 0 | 0 | 8531 | 0 |
| QTD | 5 | 1 | 4 | 5 | 5 | 0 | 0 | 0 | 6 | 0 |
| 1Y | 247 | 6979 | 122 | 7101 | 245 | 0 | 2 | 0 | 10411 | 0 |

### the 49F entry SI

Interior days (16107) by status and base class (own-row basis):

| status | zero | negative | positive | no prior row |
|---|---|---|---|---|
| ALL-HOLDINGS-EXCLUDED | 118 | 0 | 0 | 0 |
| FOLLOWS-DISCONTINUITY | 0 | 0 | 2 | 0 |
| IMPLAUSIBLE-RETURN | 0 | 0 | 2 | 0 |
| NO-PRIOR-HOLDINGS | 15348 | 0 | 0 | 0 |
| NON-POSITIVE-BASE | 637 | 0 | 0 | 0 |

Zero run (own-row basis): 1=597, 2=553, 3-5=1494, 6-20=5220, 21-60=6453, more=1786

Literal previous-row reading, by class: ALL-HOLDINGS-EXCLUDED: zero=107, negative=0, positive=11, no_prior_row=0; FOLLOWS-DISCONTINUITY: zero=0, negative=0, positive=2, no_prior_row=0; IMPLAUSIBLE-RETURN: zero=0, negative=0, positive=2, no_prior_row=0; NO-PRIOR-HOLDINGS: zero=14781, negative=0, positive=567, no_prior_row=0; NON-POSITIVE-BASE: zero=618, negative=0, positive=19, no_prior_row=0; zero run: 1=553, 2=518, 3-5=1439, 6-20=5005, 21-60=6246, more=1745

Last-row days (178) by status and base class (own-row basis):

| status | zero | negative | positive | no prior row |
|---|---|---|---|---|
| NO-PRIOR-HOLDINGS | 172 | 0 | 0 | 0 |
| NON-POSITIVE-BASE | 6 | 0 | 0 | 0 |

Zero run (own-row basis): 1=2, 2=0, 3-5=2, 6-20=12, 21-60=54, more=108

Literal previous-row reading, by class: NO-PRIOR-HOLDINGS: zero=170, negative=0, positive=2, no_prior_row=0; NON-POSITIVE-BASE: zero=6, negative=0, positive=0, no_prior_row=0; zero run: 1=0, 2=1, 3-5=1, 6-20=12, 21-60=54, more=108

Literal previous-row reading, accounts: all zero 42, with a negative 0, with a positive flagged 358.

### the 49F entry YTD

Interior days (4339) by status and base class (own-row basis):

| status | zero | negative | positive | no prior row |
|---|---|---|---|---|
| ALL-HOLDINGS-EXCLUDED | 89 | 0 | 0 | 0 |
| NO-PRIOR-HOLDINGS | 3886 | 0 | 0 | 0 |
| NON-POSITIVE-BASE | 364 | 0 | 0 | 0 |

Zero run (own-row basis): 1=214, 2=195, 3-5=517, 6-20=1696, 21-60=1621, more=96

Literal previous-row reading, by class: ALL-HOLDINGS-EXCLUDED: zero=80, negative=0, positive=9, no_prior_row=0; NO-PRIOR-HOLDINGS: zero=3689, negative=0, positive=197, no_prior_row=0; NON-POSITIVE-BASE: zero=356, negative=0, positive=8, no_prior_row=0; zero run: 1=195, 2=182, 3-5=494, 6-20=1606, 21-60=1561, more=87

Last-row days (114) by status and base class (own-row basis):

| status | zero | negative | positive | no prior row |
|---|---|---|---|---|
| NO-PRIOR-HOLDINGS | 108 | 0 | 0 | 0 |
| NON-POSITIVE-BASE | 6 | 0 | 0 | 0 |

Zero run (own-row basis): 1=2, 2=0, 3-5=2, 6-20=12, 21-60=54, more=44

Literal previous-row reading, by class: NO-PRIOR-HOLDINGS: zero=106, negative=0, positive=2, no_prior_row=0; NON-POSITIVE-BASE: zero=6, negative=0, positive=0, no_prior_row=0; zero run: 1=0, 2=1, 3-5=1, 6-20=12, 21-60=54, more=44

Literal previous-row reading, accounts: all zero 59, with a negative 0, with a positive flagged 153.

### the 49F entry QTD

Interior days (1) by status and base class (own-row basis):

| status | zero | negative | positive | no prior row |
|---|---|---|---|---|
| NO-PRIOR-HOLDINGS | 1 | 0 | 0 | 0 |

Zero run (own-row basis): 1=1, 2=0, 3-5=0, 6-20=0, 21-60=0, more=0

Literal previous-row reading, by class: NO-PRIOR-HOLDINGS: zero=0, negative=0, positive=1, no_prior_row=0; zero run: 1=0, 2=0, 3-5=0, 6-20=0, 21-60=0, more=0

Last-row days (4) by status and base class (own-row basis):

| status | zero | negative | positive | no prior row |
|---|---|---|---|---|
| NO-PRIOR-HOLDINGS | 4 | 0 | 0 | 0 |

Zero run (own-row basis): 1=2, 2=0, 3-5=2, 6-20=0, 21-60=0, more=0

Literal previous-row reading, by class: NO-PRIOR-HOLDINGS: zero=2, negative=0, positive=2, no_prior_row=0; zero run: 1=0, 2=1, 3-5=1, 6-20=0, 21-60=0, more=0

Literal previous-row reading, accounts: all zero 2, with a negative 0, with a positive flagged 3.

### the 49F entry 1Y

Interior days (6979) by status and base class (own-row basis):

| status | zero | negative | positive | no prior row |
|---|---|---|---|---|
| ALL-HOLDINGS-EXCLUDED | 118 | 0 | 0 | 0 |
| FOLLOWS-DISCONTINUITY | 0 | 0 | 2 | 0 |
| IMPLAUSIBLE-RETURN | 0 | 0 | 2 | 0 |
| NO-PRIOR-HOLDINGS | 6294 | 0 | 0 | 0 |
| NON-POSITIVE-BASE | 563 | 0 | 0 | 0 |

Zero run (own-row basis): 1=307, 2=284, 3-5=769, 6-20=2540, 21-60=2887, more=188

Literal previous-row reading, by class: ALL-HOLDINGS-EXCLUDED: zero=107, negative=0, positive=11, no_prior_row=0; FOLLOWS-DISCONTINUITY: zero=0, negative=0, positive=2, no_prior_row=0; IMPLAUSIBLE-RETURN: zero=0, negative=0, positive=2, no_prior_row=0; NO-PRIOR-HOLDINGS: zero=6009, negative=0, positive=285, no_prior_row=0; NON-POSITIVE-BASE: zero=552, negative=0, positive=11, no_prior_row=0; zero run: 1=284, 2=268, 3-5=738, 6-20=2414, 21-60=2791, more=173

Last-row days (122) by status and base class (own-row basis):

| status | zero | negative | positive | no prior row |
|---|---|---|---|---|
| NO-PRIOR-HOLDINGS | 116 | 0 | 0 | 0 |
| NON-POSITIVE-BASE | 6 | 0 | 0 | 0 |

Zero run (own-row basis): 1=2, 2=0, 3-5=2, 6-20=12, 21-60=54, more=52

Literal previous-row reading, by class: NO-PRIOR-HOLDINGS: zero=114, negative=0, positive=2, no_prior_row=0; NON-POSITIVE-BASE: zero=6, negative=0, positive=0, no_prior_row=0; zero run: 1=0, 2=1, 3-5=1, 6-20=12, 21-60=54, more=52

Literal previous-row reading, accounts: all zero 49, with a negative 0, with a positive flagged 198.

## orion

| window | accounts | interior days | last-row days | days counted | all-zero accounts | with a negative | with a positive flagged | within a cent, not zero | trailing (neither) | previous row not the previous partition |
|---|---|---|---|---|---|---|---|---|---|---|
| SI | 178 | 3280 | 125 | 3405 | 178 | 0 | 0 | 0 | 13756 | 0 |
| YTD | 116 | 799 | 105 | 904 | 116 | 0 | 0 | 0 | 8632 | 0 |
| QTD | 4 | 0 | 4 | 4 | 4 | 0 | 0 | 0 | 15 | 0 |
| 1Y | 130 | 1261 | 115 | 1376 | 130 | 0 | 0 | 0 | 10897 | 0 |

### orion SI

Interior days (3280) by status and base class (own-row basis):

| status | zero | negative | positive | no prior row |
|---|---|---|---|---|
| NON-POSITIVE-BASE | 3280 | 0 | 0 | 0 |

Zero run (own-row basis): 1=174, 2=133, 3-5=357, 6-20=907, 21-60=525, more=1184

Literal previous-row reading, by class: NON-POSITIVE-BASE: zero=3106, negative=0, positive=174, no_prior_row=0; zero run: 1=133, 2=124, 3-5=340, 6-20=821, 21-60=511, more=1177

Last-row days (125) by status and base class (own-row basis):

| status | zero | negative | positive | no prior row |
|---|---|---|---|---|
| NON-POSITIVE-BASE | 125 | 0 | 0 | 0 |

Zero run (own-row basis): 1=0, 2=0, 3-5=4, 6-20=3, 21-60=17, more=101

Literal previous-row reading, by class: NON-POSITIVE-BASE: zero=125, negative=0, positive=0, no_prior_row=0; zero run: 1=0, 2=0, 3-5=4, 6-20=3, 21-60=17, more=101

Literal previous-row reading, accounts: all zero 66, with a negative 0, with a positive flagged 112.

### orion YTD

Interior days (799) by status and base class (own-row basis):

| status | zero | negative | positive | no prior row |
|---|---|---|---|---|
| NON-POSITIVE-BASE | 799 | 0 | 0 | 0 |

Zero run (own-row basis): 1=77, 2=68, 3-5=179, 6-20=400, 21-60=75, more=0

Literal previous-row reading, by class: NON-POSITIVE-BASE: zero=722, negative=0, positive=77, no_prior_row=0; zero run: 1=68, 2=64, 3-5=166, 6-20=355, 21-60=69, more=0

Last-row days (105) by status and base class (own-row basis):

| status | zero | negative | positive | no prior row |
|---|---|---|---|---|
| NON-POSITIVE-BASE | 105 | 0 | 0 | 0 |

Zero run (own-row basis): 1=0, 2=0, 3-5=4, 6-20=3, 21-60=17, more=81

Literal previous-row reading, by class: NON-POSITIVE-BASE: zero=105, negative=0, positive=0, no_prior_row=0; zero run: 1=0, 2=0, 3-5=4, 6-20=3, 21-60=17, more=81

Literal previous-row reading, accounts: all zero 64, with a negative 0, with a positive flagged 52.

### orion QTD

Interior days (0) by status and base class (own-row basis):

(no days)

Zero run (own-row basis): 1=0, 2=0, 3-5=0, 6-20=0, 21-60=0, more=0

Literal previous-row reading, by class: ; zero run: 1=0, 2=0, 3-5=0, 6-20=0, 21-60=0, more=0

Last-row days (4) by status and base class (own-row basis):

| status | zero | negative | positive | no prior row |
|---|---|---|---|---|
| NON-POSITIVE-BASE | 4 | 0 | 0 | 0 |

Zero run (own-row basis): 1=0, 2=0, 3-5=4, 6-20=0, 21-60=0, more=0

Literal previous-row reading, by class: NON-POSITIVE-BASE: zero=4, negative=0, positive=0, no_prior_row=0; zero run: 1=0, 2=0, 3-5=4, 6-20=0, 21-60=0, more=0

Literal previous-row reading, accounts: all zero 4, with a negative 0, with a positive flagged 0.

### orion 1Y

Interior days (1261) by status and base class (own-row basis):

| status | zero | negative | positive | no prior row |
|---|---|---|---|---|
| NON-POSITIVE-BASE | 1261 | 0 | 0 | 0 |

Zero run (own-row basis): 1=100, 2=90, 3-5=241, 6-20=610, 21-60=220, more=0

Literal previous-row reading, by class: NON-POSITIVE-BASE: zero=1161, negative=0, positive=100, no_prior_row=0; zero run: 1=90, 2=85, 3-5=227, 6-20=551, 21-60=208, more=0

Last-row days (115) by status and base class (own-row basis):

| status | zero | negative | positive | no prior row |
|---|---|---|---|---|
| NON-POSITIVE-BASE | 115 | 0 | 0 | 0 |

Zero run (own-row basis): 1=0, 2=0, 3-5=4, 6-20=3, 21-60=17, more=91

Literal previous-row reading, by class: NON-POSITIVE-BASE: zero=115, negative=0, positive=0, no_prior_row=0; zero run: 1=0, 2=0, 3-5=4, 6-20=3, 21-60=17, more=91

Literal previous-row reading, accounts: all zero 64, with a negative 0, with a positive flagged 66.

## Control

In memory only: an account valued positive, zero, positive over three days (5.0, 0.0, 7.0). Rule 'previous row' on three rows valued positive, zero, positive: the third day's prior value is read; rule 'own row' (the producer's base: the row's own account_value is the close of the day before) on the rows for the days after each close: the row that follows the zero close is read. A second plant, rows 0.0, 0.0, 0.0, 4.0, reads the fourth day's prior value; a value of 0.004 is read by the exact-zero rule.

Reading: {"expected": "third day's prior value zero with run length 1: HELD", "own_row_rule_day_after_the_last_close": {"base": "positive", "zero_run": 0}, "own_row_rule_day_after_the_zero_close": {"base": "zero", "zero_run": 1}, "previous_row_rule_third_day": {"prior_value": "zero", "zero_run": 1}, "previous_row_rule_zero_zero_zero_then_positive": {"prior_value": "zero", "zero_run": 3}, "value_0.004_reads": "positive"}

## Not established

- the deployed route's own answer: no Lambda invoked, no sign-in; the deployed package, mapping loader, authorization and envelope were not exercised
- whether the zero base days are 'empty and re-funded' in the account's real history: the gold carries the account's basket, not its cash flows, so an account that went to zero and later returned is seen, a funding event is not
- why a given base is positive on a non-OK day beyond the status token (IMPLAUSIBLE-RETURN, FOLLOWS-DISCONTINUITY, ALL-HOLDINGS-EXCLUDED): the producer's inputs (prices, identifiers) were not read
- the producer's status grade was read from the code at the base commit; the gold's partitions were not regenerated or recomputed
- the transport check of IB-pr-464 (stand-in versus the reader's own HoldingsGoldSource class) was not repeated: the same stand-in is used; the reproduction of IB-pr-464's account counts is the check
- the gold was read once, at the time of this run, capped at 2026-10-08; a later partition may have landed
- accounts the reader refuses (no mapping at the last partition, or no OK row in the window) are not placed, as in IB-pr-464

Zeros: functions invoked 0, sign-ins 0, AWS writes 0, accounts written 0, values written 0.
