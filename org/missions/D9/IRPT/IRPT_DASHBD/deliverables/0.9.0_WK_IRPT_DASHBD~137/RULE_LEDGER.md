# RULE_LEDGER.md -- IRPT_DASHBD round 91, TO-DB-b-171 (worker 0.9.0_WK_IRPT_DASHBD~137)

Written and committed BEFORE any read of a transaction row or a ledger row of the seven accounts. Read to write it:
the round-90 day rule (deliverables ~136 RULE_DAY.md, day_reasons.py), tieout/tieout_day_read.py and
tieout/tieout_neither_reasons.py (tie tolerance, day_of, is_trading), read90.py of the private folder ~108 (the column
names it kept and the two store keys), the gold producer's source declaration (data/assets/scripts/gold/irpt_reporting/
sources.json, which names the custody transactions prefix and the money column), and SCHEMA-ONLY probes of one object
per side (column names and types; no row value was printed or held). No account was read by row. No vendor call, no
credential, no S3 write.

Tolerances (as in round 90): a window CLOSES iff |G_c - R_c| * 100 <= 0.35. A day DIFFERS iff |b(d) - s(d)| * 100 > 0.01
(DAY_DIFFERS_PP). Amount tie: tie(x, a) iff |x - a| <= max(1.0, 0.001 * |a|) (tieout_neither_reasons.tie_amt). Near
window for counterparts: NEAR = 5 calendar days either side. Adjacent trading day of d: the nearest trading day strictly
before d and the nearest strictly after d (lib/trading_calendar.is_trading_day), each taken only if it is a gold date
of the segment.

## 0. Sides, columns and per-day quantities

BLACK DIAMOND (BD) side. Store: opal-data-assets, prefix blackdiamond/49financial/silver_legacy/transactions/, one object
per partition date=YYYY-MM-DD. Columns used: return_date (the day d of a BD row), account_number (matched after
strip and removal of leading zeros, as round 89), external_flow (Contribution / Withdrawal mark a flow row), market_value
(the flow amount of such a row, signed as stored), income (the income amount of any row), cusip (security key; asset_id
where cusip is blank), transaction_id (row identity for the per-lot count), trade_date and settle_date (carried, not
tested). For a day d and an account:
- R(d): the BD rows with return_date d.
- I(d) = sum of income over R(d). F(d) = sum of market_value over rows of R(d) whose external_flow is Contribution or
  Withdrawal (round 89 bd_days logic).

SERVED side. Ledger rows: the custody transaction rows the gold producer builds external_flow and income_received from
(sources.json: schwab master 08335338, transactions_prefix schwab/08335338/silver/fact_trn/ in opal-data-assets, one
object per partition date=YYYY-MM-DD, key account_id with zero pad 10, business_date, money column gross_amount, security
key cusip). The producer's own classification (classify_and_sum) is NOT re-derived here: the served rows of day d are
taken as all fact_trn rows of the account with business_date d and gross_amount not zero, and every served test below
uses only their absolute amounts |gross_amount| (a row-level counterpart) and the producer's per-day gold totals.
Per-day gold totals for d (round 90's series, read90.pkl gold): s(d) = total_return_daily, V(d) = market_value_eod,
f(d) = external_flow (null read as 0), a(d) = income_received (null as 0), m(d) = market_value_eod of the gold date
immediately before d (applicable only when non-null and non-zero).

Corrected returns, one formula per side:
- SERVED correction, changing the served V or f on day d: c(d) = (V' - f') / m(d) - 1 (day_reasons.py convention).
  Served income sits inside V (income x added to V: V' = V + x). Served flow sits in f (f' = f + x).
- BD correction: removing a BD income amount x from day d changes b by -x / m(d); removing a BD flow amount x (a row of
  F) changes b by +x / m(d) (the flow enters the BD end-of-day return as minus F). Adding is the opposite sign.
  b'(d) = b(d) + (change above). Stated limit: m(d) is the served prior-day market value, the common denominator of the
  day grain; no BD market value is read.

## 1. The closed list, in order (verbatim names)

(1) BD_INCOME_PER_LOT   (2) DUPLICATE_ROW   (3) BOOKING_DATE_DIFFERS   (4) MISSING_IN_LEDGER   (5) UNEXPLAINED

A differing day takes the FIRST reason, in this order, that has a TEST holding on one of its arms AND whose arm's
CORRECTION brings the day within 0.01 pp: for a BD-side correction, |b'(d) - s(d)| * 100 <= 0.01; for a served-side correction,
|b(d) - c(d)| * 100 <= 0.01. Arms of a reason are tried in the order stated. A day no reason takes is UNEXPLAINED.

(1) BD_INCOME_PER_LOT -- side: BD. Rows split per lot.
- TEST: a(d) != 0; at least 2 rows of R(d) carry income not zero with at least 2 distinct transaction_id values; and
  there is an integer k >= 2 with tie(I(d), k * a(d)) (k is the nearest integer to I(d) / a(d)).
- CORRECTION: the BD income of day d is set to a(d): remove X = I(d) - a(d) from BD. b'(d) = b(d) - X / m(d).
- EVIDENCE: kind "multiple", value k.

(2) DUPLICATE_ROW -- arms: BD first, then served.
- ARM BD. TEST: two rows of R(d) share the same amount (income for an income row; market_value for a flow row) and the
  same security key, the rows being the same return_date. CORRECTION: remove one copy of that amount x (income: b' =
  b - x / m; flow: b' = b + x / m). EVIDENCE: kind "count", value = number of extra copies on day d.
- ARM SERVED. TEST: a(d) != 0 and tie(a(d), 2 * x) where x is the amount of two served fact_trn rows of day d with equal
  |gross_amount| and equal cusip; or f(d) != 0 and tie(f(d), 2 * x) likewise. CORRECTION: remove one copy: income: V' =
  V - a(d) / 2; flow: f' = f - f(d) / 2. EVIDENCE: kind "count", value = number of extra copies.

(3) BOOKING_DATE_DIFFERS -- the amount matches on an adjacent trading day. Arms: BD income, BD flow, served income,
served flow, in this order. d2 is the adjacent trading day (EVIDENCE value = calendar offset d2 - d, signed).
- ARM BD INCOME. TEST: I(d) != 0; not tie(I(d), a(d)); and tie(I(d), a(d2)) for an adjacent trading day d2.
  CORRECTION: remove I(d) from BD on d (b' = b - I(d) / m(d)). The move to d2 is NOT applied to d2 (day grain; a limit).
- ARM BD FLOW. TEST: F(d) != 0; not tie(F(d), f(d)); and tie(F(d), f(d2)) for an adjacent trading day d2.
  CORRECTION: remove F(d) from BD on d (b' = b + F(d) / m(d)).
- ARM SERVED INCOME. TEST: a(d) != 0; not tie(a(d), I(d)); and tie(a(d), I(d2)) for an adjacent trading day d2.
  CORRECTION: remove a(d) from served on d: V' = V - a(d).
- ARM SERVED FLOW. TEST: f(d) != 0; not tie(f(d), F(d)); and tie(f(d), F(d2)) for an adjacent trading day d2.
  CORRECTION: remove f(d) from served on d: f' = 0.

(4) MISSING_IN_LEDGER -- a row in BD with no counterpart on the served side. Side: SERVED (the served row is added).
- TEST: there is a BD row of R(d) with amount x (income for an income row, market_value for a flow row, |x| > 0) such
  that NO served fact_trn row of the account with business_date within 5 calendar days of d has |gross_amount| with
  tie(|gross_amount|, |x|). EVIDENCE: kind "count", value = number of such BD rows on day d.
- CORRECTION: the served side gains the missing rows of day d: X_inc = sum of the missing income amounts, X_flow = sum of
  the missing flow amounts (signed as stored). V' = V + X_inc; f' = f + X_flow; c(d) = (V' - f') / m(d) - 1.
  A correction needing V or m(d) that is absent or zero does not take the day.

(5) UNEXPLAINED: every differing day that no reason takes. Its size and offset are recorded.

## 2. Window closure after correction

D = the compared days of the segment (BD dates whose gold total_return_daily is not null), in date order.
- s'(d) = c(d) for each day taken by a SERVED-side correction; s(d) otherwise.
- P_bd = product over the days taken by a BD-side correction of (1 + b'(d)) / (1 + b(d)); 1 when none.
- G = round 90's gross window figure (the same fee add-back: (1 + bdr) * (1 + fees / mean) - 1, mean > 0, else 0).
- G_c = (1 + G) * P_bd - 1 (the BD window with the faulty BD rows removed, the same fee add-back).
- R_c = product over D of (1 + s'(d)) - 1.
- The window RE-CLOSES iff |G_c - R_c| * 100 <= 0.35.
- window_closed_after_correction = (UNEXPLAINED days == 0) AND the window re-closes.

## 3. Negative arm

R0 = product over D of (1 + s(d)) - 1 (no correction). uncorrected_window_misses = (|G - R0| * 100 > 0.35).

## 4. Population and recording

Population: the 7 segments and 23 differing days exactly as round 90's record (~136 DAY_READ_7.json; the population is
re-run by tieout_day_read.plan_unexplained and asserted there). Per account in plan order: days_differing, by_reason
(five names), evidence (kind and values per reason above 0 except UNEXPLAINED), unexplained_days as {offset, size_pp}
(offset = calendar days from the segment start; size_pp = (b - s) * 100, signed), uncorrected_window_misses and
window_closed_after_correction. No account id, no date, no name in the record.

Row counts: bd_transactions_rows_read = fresh BD rows of the seven accounts within 5 calendar days of a differing day
(all columns read); served_rows_read = fresh served fact_trn rows of the seven accounts within 5 calendar days of a
differing day. Both counted, printed as counts.

## 5. Limits

Day corrections are single-day recomputations; a corrected day is evidence that the cause is sufficient for the day,
not that it is the only cause. The BD-side correction uses the served prior-day market value as the denominator. The
moved amount of BOOKING_DATE_DIFFERS is not applied to d2. The served classification of the producer is not re-derived;
the served rows are taken whole, and the row counterpart test uses absolute amounts.

## 6. If the rule proves unworkable after the read starts

Do NOT edit this file. Add a dated RULE_LEDGER_ADDENDUM.md in this folder and report both readings.
