# RULE.md -- IRPT_DASHBD round 89, TO-DB-b-167

Written and committed BEFORE any read of a row of the 12 segments. Code and column names (tieout_flow_timing.py,
class90.py, read90.py, table90.py, lib/trading_calendar.py) were read to write it; no row of any segment was opened.
Tolerance: a recomputation CLOSES iff |G - R| * 100 <= 0.35, G the gross and R the recomputed segment return.

## 0. Inputs (names as written by read90.py and table90.py)

- W(s): the gold dates d of the segment's account with start <= d <= end, in date order.
- D(s): the days of W whose `r` (gold column total_return_daily) is not None. This is the module's day set.
- Gold fields per day: `mv` (market_value_eod), `flow` (external_flow), `inc_recv` (income_received),
  `price_reason` (holdings_price_return_reason).
- BD ledger rows (txn): `return_date`, `external_flow`, `market_value`, `income`.
  F_bd(d) = sum of `market_value` over rows with return_date = d and external_flow in {Contribution, Withdrawal}
  (table90 t_flow, sign as stored). I_bd(d) = sum of `income` over rows with return_date = d (table90 t_inc).
- prior_mv: the `mv` of the last gold date before start (tieout_flow_timing.py).
- R (uncorrected recomputation) = relink(D, bd_default, prior_mv) of tieout_flow_timing.py, unchanged.
- G (gross) = (1 + bdr) * (1 + fees / mean) - 1, as the module computes it.
- Trading day: lib/trading_calendar.is_trading_day(d).
- o_bmv, o_emv, o_flow, o_gain, mean and the BD point fields bmv, emv, nadd, ngain, bacc, eacc: as table90.py.

## 1. The closed list and its order

(1) MISSING_PRICE  (2) FLOW_ABSENT_ONE_SIDE  (3) FLOW_ON_NON_TRADING_DAY  (4) INCOME_OFF_FLOW_DAY  (5) BD_ACCRUED_INCOME
(6) UNEXPLAINED.

Each reason's CORRECTION is applied ALONE to the recomputation. A reason TAKES a segment when its TEST holds and its
CORRECTION makes the segment CLOSE. Reasons are tried in list order; the first that takes the segment stands. A segment
no reason takes is UNEXPLAINED.

### 1.1 MISSING_PRICE
- TEST: some d in W has `price_reason` not null and not an empty string. Evidence: the count of such days.
- CORRECTION: each flagged day is treated as a flat-price day. In date order over W, for each flagged d:
  mv(d) := mv(p) + flow(d), where p is the nearest earlier W day carrying a non-null mv (already corrected), or
  prior_mv if none; a null flow counts as 0. Then R is recomputed with D unchanged.

### 1.2 FLOW_ABSENT_ONE_SIDE
- TEST: some d in D where exactly one side carries a non-zero flow: gold flow(d) non-zero and F_bd(d) zero, or F_bd(d)
  non-zero and gold flow(d) zero or null. Evidence: the count of such days.
- CORRECTION: on each such day set the recomputation flow(d) := F_bd(d) (zero where the BD side carries none). R is
  recomputed with D unchanged.

### 1.3 FLOW_ON_NON_TRADING_DAY
- TEST: some d in W has gold flow(d) non-zero and is_trading_day(d) false. The BD side is not tested here.
  Evidence: day offsets d - start (calendar days) of those days.
- CORRECTION: each such flow is re-dated to its target: the first day of D after d that is a trading day, or, if none
  follows, the last day of D before d that is a trading day. The source flow is set to zero and its amount is added to
  the target flow (several sources may share a target). If no target exists the correction does not apply. R is
  recomputed.

### 1.4 INCOME_OFF_FLOW_DAY
- TEST: a day d in W with gold inc_recv(d) non-zero and I_bd(d) zero, for which some day d2 in W, d2 != d, with
  |d2 - d| <= 5 calendar days, has I_bd(d2) tying to inc_recv(d): |I_bd(d2) - inc_recv(d)| <= max(1.0, 0.001 * |inc_recv(d)|).
  d2 is the nearest such day (ties to the earlier). Evidence: the day offsets d2 - d of the matched pairs.
- CORRECTION: for each matched pair (d -> d2) with amount a = inc_recv(d), the income is re-dated in the value series:
  if d2 > d, mv(t) := mv(t) - a for every W day t with d <= t < d2 that carries an mv; if d2 < d, mv(t) := mv(t) + a
  for every W day t with d2 <= t < d that carries an mv. R is recomputed with D unchanged.

### 1.5 BD_ACCRUED_INCOME
- TEST: the dollar identity of class90.py holds, with the uncorrected values. Let tie(p, q) be
  |p - q| <= max(1.0, 0.001 * max(|p|, |q|)); tb = tie(bmv, o_bmv), te = tie(emv, o_emv), tn = tie(nadd, o_flow),
  tg = tie(ngain, o_gain); dacc = eacc - bacc; ok_b = tb or |(bmv - o_bmv) - bacc| <= max(1.0, 0.001 * |bacc|);
  ok_e = te or |(emv - o_emv) - eacc| <= max(1.0, 0.001 * |eacc|); ok_g = |(ngain - o_gain) - dacc| <= max(1.0, 0.001 * |dacc|).
  TEST = tn and not (tb and te and tg) and ok_b and ok_e and ok_g. Evidence: the count (1 per segment).
- CORRECTION: the accrual-adjusted recomputation R_acc = (1 + R) * ((o_emv + eacc) / o_emv) / ((o_bmv + bacc) / o_bmv) - 1,
  with R the unchanged bd_default relink. It applies only when o_emv > 0 and o_bmv > 0.

### 1.6 UNEXPLAINED
Every segment that no reason in 1.1 to 1.5 takes.

## 2. Counting rules

- by_reason: each of the 12 segments counted once, under the first reason in list order that takes it.
- uncorrected control (uncorrected_closes_among_12): the number of the 12 whose uncorrected R closes against G under
  bd_default, or whose uncorrected END recomputation closes. Expected 0.
- demoted_to_unexplained: among the 12, those with at least one TEST of 1.1 to 1.5 holding that end UNEXPLAINED.
- combined_only: among the UNEXPLAINED segments, those for which applying two corrections together (both TESTs holding)
  closes. Series corrections (1.1 to 1.4) are applied in list order, then 1.5 as the final accrual adjustment. Counted
  once per segment; the segment stays UNEXPLAINED.
- population.accounts: the distinct accounts among the 88 flow-bearing gradable segments.
- unexplained_per_account: for each account holding at least one UNEXPLAINED segment of the 12, that count, listed in
  ascending numeric order. fwd8_unmet_accounts = the length of that list.
- Evidence values: for count kinds, the per-segment counts of the reasons taken, sorted ascending; for day_offsets kind,
  all offsets of the taken reason, sorted ascending.

## 3. If the rule proves unworkable

Do not edit this file. Add a dated RULE_ADDENDUM.md in this folder and report the count under both readings.

## 4. Limits

The rule decides a cause only as far as the stored columns show it. Corrections are recomputation changes, not
statements of which system is right. A closing correction is evidence the cause is sufficient for the segment, not that
it is the only cause. Trading-day status comes from lib/trading_calendar.py as it stands.
