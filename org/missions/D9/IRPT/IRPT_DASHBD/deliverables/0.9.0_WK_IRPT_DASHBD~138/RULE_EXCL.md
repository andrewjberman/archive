# RULE_EXCL.md -- IRPT_DASHBD round 92, TO-DB-b-172 (worker 0.9.0_WK_IRPT_DASHBD~138)

Written and committed BEFORE any computation on the 23 differing days: no row of any of the seven accounts, no pulled
response, no stored daily table and no gold series value was read to write it. Read to write it: RULE_LEDGER.md and
RULE_LEDGER_ADDENDUM.md (worker ~137, the reasons (2) to (5) and Reading B), RULE_DAY.md (worker ~136, the day grain,
the served convention s(d) = (V - f)/m - 1 and the window convention), ledger_rows.py (worker ~137, read only, for its
functions and its record keys), and the round-92 checker's docstring (the record keys). No vendor call, no credential,
no S3 read.

Tolerances (unchanged from rounds 90 and 91): a window CLOSES iff |G_c - R_c| * 100 <= 0.35 (TOL_PP). A day DIFFERS iff
|b(d) - s(d)| * 100 > 0.01 (DAY_DIFFERS_PP). Amount tie: tie(x, a) iff |x - a| <= max(1.0, 0.001 * |a|).
Adjacent trading day, NEAR window, sources and per-day quantities: as RULE_LEDGER.md section 0.

## 0. Per-day quantities (as RULE_LEDGER.md section 0 and RULE_DAY.md section 0)

For a differing day d of an account: b = b(d) (the BD daily return), s = s(d) (the served daily return, gold
total_return_daily), V = market_value_eod(d), f = external_flow(d) (null as 0), a = income_received(d) (null as 0),
m = market_value_eod of the gold date immediately before d; m is APPLICABLE only when non-null and non-zero.
I(d) = sum of income over the BD rows R(d); F(d) = sum of market_value over R(d) rows whose external_flow is
Contribution or Withdrawal.

## 1. The closed list, in order (verbatim names)

(1) BD_EXCLUDES_SERVED_INCOME   (2) BD_INCOME_PER_LOT   (3) DUPLICATE_ROW   (4) BOOKING_DATE_DIFFERS
(5) MISSING_IN_LEDGER           (6) UNEXPLAINED

A differing day takes the FIRST reason, in this order, that has a TEST holding on one of its arms AND whose arm's
CORRECTION brings the day within the day tolerance of Black Diamond: |b(d) - c(d)| * 100 <= 0.01 for a served-side
correction c(d), or |b'(d) - s(d)| * 100 <= 0.01 for a BD-side correction b'(d). Arms are tried in the order stated.
A day no reason takes is UNEXPLAINED. Each differing day is assigned once; the six counts sum to days_differing.

## 2. (1) BD_EXCLUDES_SERVED_INCOME -- NEW, side SERVED, one arm

- TEST: a != 0 AND m is applicable AND |(b - s) + a / m| * 100 <= 0.01.
  In words: on the day, the gap (Black Diamond minus served) equals minus the served income over the prior value,
  within 0.01 pp. If a = 0, or m is not applicable, the TEST does not hold.
- CORRECTION: remove the served income from the served day's return: V' = V - a; c(d) = (V' - f) / m - 1
  = (V - a - f) / m - 1. This lowers the served return by a / m, the income's share of the prior value, so the
  corrected day moves toward Black Diamond's by that share. It needs V non-null and m applicable; if not, the
  reason does not take the day.
- The day is taken iff the TEST holds AND |b - c| * 100 <= 0.01.
- EVIDENCE: kind "multiple", value k = nearest integer of I(d) / a (k = 0 when I(d) = 0). k = 0 is the day on which
  Black Diamond books no income against the served income; k >= 1 is the BD income as a whole multiple of the served.
- TEST COUNT: test_held_days = the number of differing days on which THIS TEST holds (the test alone, before the
  correction check and before any window test). A day taken by this reason is one of them, so the days taken never
  exceed test_held_days.

## 3. Reasons (2) to (6): RULE_LEDGER.md's TESTs and CORRECTIONS, unchanged, with reason (2) read as Reading B

(2) BD_INCOME_PER_LOT -- side BD, Reading B (RULE_LEDGER_ADDENDUM.md section 3):
- TEST: a != 0; at least two rows of R(d) carry income not zero (NO distinct transaction_id requirement); there is an
  integer k >= 2 with tie(I(d), k * a), k = nearest integer to I(d) / a. Also I(d) != 0: the ~137 code requires it and
  this rule keeps it, stated here so that a count can be repeated.
- CORRECTION: BD income set to a: X = I(d) - a removed from BD; b'(d) = b(d) - X / m. Needs m applicable.
- EVIDENCE: kind "multiple", value k.

(3) DUPLICATE_ROW -- arms BD then served, exactly as RULE_LEDGER.md section 1 (2). EVIDENCE: kind "count", value = the
number of extra copies on day d.

(4) BOOKING_DATE_DIFFERS -- four arms in order (BD income, BD flow, served income, served flow), exactly as
RULE_LEDGER.md section 1 (3), with d2 the adjacent trading day (nearest trading day before and after d, searched up to
10 calendar days, each taken only if it is a gold date of the segment and inside the read windows). EVIDENCE: kind
"day_offsets", value = d2 - d in calendar days, signed.

(5) MISSING_IN_LEDGER -- side SERVED, exactly as RULE_LEDGER.md section 1 (4). EVIDENCE: kind "count", value = the
number of BD rows of day d with no served counterpart within 5 calendar days.

(6) UNEXPLAINED -- every differing day that no reason in (1) to (5) takes. Its offset and signed size are recorded.

Re-test of the other days: each day's TESTS read only the raw inputs of section 0 and the rows; no correction changes
those inputs (a correction changes that day's return only, section 5). The full list is therefore applied to every
differing day, and the re-test after the new reason's days are corrected returns the same assignment for the other
days. The code applies the list once per day.

## 4. Assignment check

A day's assignment is the first reason of section 1 whose TEST and correction hold. BD_EXCLUDES_SERVED_INCOME is first,
so a day with a holding test and a correction within 0.01 pp takes it, whatever the other reasons would say.

## 5. Window closure (RULE_LEDGER.md section 2, unchanged)

D = the compared days of the segment (BD dates whose gold total_return_daily is not null), in date order.
- s'(d) = c(d) for each day taken by a SERVED-side correction (reasons (1), (3) served arm, (5)); s(d) otherwise.
- P_bd = product over the days taken by a BD-side correction (reasons (2), (3) BD arm, (4) BD arms) of
  (1 + b'(d)) / (1 + b(d)); 1 when none.
- G = the gross window figure of round 90: (1 + bdr) * (1 + fees / mean) - 1, with fees / mean used when mean > 0,
  else 0 (RULE_DAY.md section 0).
- G_c = (1 + G) * P_bd - 1.
- R_c = product over D of (1 + s'(d)) - 1.
- The window RE-CLOSES iff |G_c - R_c| * 100 <= 0.35.
- window_closed_after_correction = (UNEXPLAINED days == 0) AND the window re-closes.
- The moved amount of BOOKING_DATE_DIFFERS is not applied to d2 (day grain, RULE_LEDGER.md section 5).

## 6. Negative arm

R0 = product over D of (1 + s(d)) - 1, with no correction. uncorrected_window_misses = (|G - R0| * 100 > 0.35).
Every account must read true here: the uncorrected window misses by more than 0.35 pp.

## 7. Population, sources and recording

Population: the 7 segments and 23 differing days exactly as round 90's record (~136 DAY_READ_7.json, per-account
days_differing in plan order); re-run through tieout_day_read.plan_unexplained and asserted there. Per account in plan
order: days_differing, by_reason (six names), evidence (kind and values for each reason above 0 except UNEXPLAINED),
unexplained_days as {offset, size_pp} (offset = calendar days from the segment start; size_pp = (b - s) * 100,
signed), uncorrected_window_misses and window_closed_after_correction. No account id, no date, no name in the record.

sources: bd_transactions_rows_read = the fresh BD rows read (all columns) for the seven accounts within 5 calendar days
of a differing day; served_rows_read = the fresh served fact_trn rows read likewise. Both are counted and printed.

round91_pattern_8_days_confirmed = (test_held_days == 8), the 8 days round 91's worker measured. If not equal, the
difference is stated as a finding.

summary: accounts_closed_with_reasons = accounts with window_closed_after_correction true; accounts_unexplained = the
rest. surprise_row is recorded if and only if an account is UNEXPLAINED.

## 8. If the rule proves unworkable after the read starts

Do NOT edit this file. Add a dated RULE_EXCL_ADDENDUM.md in this folder and report both readings.

## 9. Limits

Day corrections are single-day recomputations (sections 2, 3 and 5); a closing correction is evidence that the cause is
sufficient for the day, not that it is the only cause. The served correction recomputes the return from V, f and m,
while the TEST reads the gold return s; the two can differ, and a day is taken only when both the TEST and the
correction hold. A correction does not change the prior value m of the next day (day grain). The BD-side denominator is
the served prior-day market value. The served classification is not re-derived; the rows are taken whole.
