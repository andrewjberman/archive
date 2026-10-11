# RULE -- when was a deposit first invested (IRPT_DASHBD.TO-DB-b-162, worker 0.9.0_WK_IRPT_DASHBD~131)

Written and committed BEFORE any transaction row or per-segment row of these accounts was loaded, printed or inspected. Sources
read to write it: code and schemas only (data/black_diamond/scripts/gold/A_03.positions_cube.py type sets, gold/lib/nna_flows.py
inflow and outflow sets, lib/trading_calendar.py, the column list of the transactions store from a parquet schema, the earlier
records ~116, ~124, ~126, ~127). Nothing here is a ruling on a flow-timing convention; it is a way of counting that another seat
can repeat. If this rule proves unworkable the bytes of this file stay as they are and a dated RULE_ADDENDUM.md is added, with the
count reported under both readings.

## 1. The days and the accounts
The 234 flow-bearing days and 49 accounts of ~127 (FLOWTIME_DENOMINATOR.json, flowtime_count.py): a date inside a segment's
start-to-end window on which the served daily series (gold column external_flow, read as "flow") is non-zero; distinct
(account, date) pairs. A day belongs to the segment whose window holds it (no overlap occurred per ~127). The segment's own end
date is the end of the WINDOW for that day. The account key is account_number with leading zeros stripped, the key ~127 used.

## 2. The store, the date columns, the repeat
- Primary reading: the COPY the tie-out read: bucket opal-data-assets, prefix blackdiamond/49financial/
  silver_legacy/transactions/ (day folders date=<day>). Reason: it is the store the tie-out cells (~108, ~127) read, and the order
  names that store. ~124 shows the original has since been rewritten (ids moved between day files), so the copy is a frozen
  snapshot of the original as of 2026-08-25.
- Second reading, reported BESIDE the primary and never substituted for it: the ORIGINAL s3://opal-data-bd/silver/transactions/
  <day>.parquet, current bytes, same firm (49 Financial), same rule. Reason: ~124 shows the two now differ by which day file
  holds a row, so a reader should see whether the answer moves. A difference between the two is reported, not resolved.
- Placement of a transaction is by its OWN date column, never by the file's day (~126): the DEPOSIT or WITHDRAWAL row is placed by
  return_date (the date column ~127 verified against the served flow days); a PURCHASE is placed by trade_date (the day the
  order was executed). Reason: return_date is the date the served series moves the flow; trade_date is when the cash went to work.
  The day file is used only to find rows (all day files from the earliest deposit day minus 100 calendar days are read (the plan look-back of section 8), so a row
  filed in a later day file is still found).
- The ledger repeats a transaction once per portfolio group: every count uses a transaction_id ONCE (first row kept; the rows are
  identical on date, type and flow label per ~116). A row with no transaction_id is dropped from the count and the number dropped
  is reported.

## 3. Deposit day against withdrawal day against other day
For a flow-bearing day d of account a, take the de-duplicated rows of a with return_date = d and external_flow equal to
Contribution (cash or assets in) or Withdrawal (out). Let IN = those with Contribution, OUT = those with Withdrawal.
- MIXED: IN and OUT both present on d. Class OTHER. Reason: the net hides two opposite flows and the cash that arrived cannot be told.
- DEPOSIT day: IN present, OUT absent, every IN row has transaction_type exactly "Cash Deposit", AND the served flow on d is
  positive. The deposit amount is the sum of |market_value| of those IN rows (each id once). Reason: "Cash Deposit" is the one
  type the estate's flow code (nna_flows INFLOW_TYPES) treats as cash arriving; the sign of the served flow must agree.
- WITHDRAWAL day: OUT present, IN absent, and the served flow on d is negative (any OUT transaction type).
- OTHER day: everything else, namely (a) a day with any IN row of a type other than "Cash Deposit" (a "Transfer In" or a journal
  can be securities arriving in kind, which leaves no cash to invest, and the data does not let this rule tell an in-kind transfer
  from a cash one), (b) MIXED days, (c) a day whose served flow sign disagrees with the sign of the ledger rows, (d) a flow-bearing
  day with no Contribution or Withdrawal row found for it in the store (reported separately as flow days without a ledger row).
deposit_days + withdrawal_days + other_days = flow_bearing_days.

## 4. What counts as "invested"
A qualifying PURCHASE is a de-duplicated row of account a with transaction_type exactly "Buy" (case and surrounding spaces
ignored) and market_value not null and not zero, that is NOT excluded below. NOT counted, with reasons:
- Reinvestment, Dividend Reinvestment, Income Reinvestment, Capital Gains Reinvestment: reinvested income, not the deposit.
- Transfer In, Journal, Corporate Action, Option Exercise, Buy to Close, Short Cover: units arrive without the account choosing
  to deploy cash into a security, or the purchase closes a short; not a deployment of new cash.
- A "Buy" whose transaction_sub_type contains (case-insensitively) "sweep" or "reinvest", or whose asset_name or
  asset_display_name matches the regex (case-insensitive) money market|sweep|fdic|insured deposit|cash reserve|cash management|
  cash & equivalents|cash and equivalents|government cash|treasury cash|bank deposit : a cash sweep is the cash staying cash.
  The number of Buy rows excluded by this sweep test is reported as a count. The rule cannot tell a sweep fund whose name matches
  none of those words; this is a stated limit.
The purchase may be of a security the account already held (cash is fungible); this rule does not ask that the security be new.

## 5. Size
A trade date t counts as the investing day only if the sum of |market_value| of the account's qualifying purchases (each id once)
with trade_date = t is AT LEAST 10 percent of the deposit amount. One threshold, a share of the deposit and not a dollar figure.
Reason: "any purchase" lets a small residual buy of a fund or a standing-plan buy stand for the deposit's deployment; a tenth of the
cash is the least that can be read as putting the deposit to work, and a share scales with deposits of any size. A deposit whose
amount is zero or null is not determinable. Purchases are summed by day because one order is often filled in several lots.

## 6. Time: the calendar, the first purchase, the window
- Calendar: lib/trading_calendar.py (NYSE; is_trading_day, trading_days_between). Trading days between d and t = the number of
  trading days in the half-open range (d, t].
- Candidate purchase days are trade dates t with d <= t <= window end (the segment's own end date), limited by store coverage (below).
  A purchase dated before d never counts.
- The first qualifying trade date t* is the earliest candidate.
  same_day: t* = d.
  next_trading_day: t* is the first trading day strictly after d (if d is a weekend or a holiday, the next trading day is the first
  trading day after it; a deposit on a non-trading day cannot be "same day").
  later: t* is after the next trading day and not later than the window end. The band is the trading-day distance n = trading days
  in (d, t*]: 2 to 5, 6 to 20, over 20 (reported as later_trading_days).
  never_in_window: no qualifying trade date from d to the window end AND the store covers the whole window.
  not_determinable: see section 7.
- A purchase that falls after a LATER flow-bearing day of the same account is still attributed to d (the cash is not tagged);
  this is a stated limit, not a separate class. The count of deposit days whose t* lies beyond the next flow-bearing day of the
  same account is reported as a count.

## 7. Store coverage and not_determinable
- Coverage: a day file holds trades whose trade_date can lie up to 6 days before the file's day; so a store whose newest day file
  is F is firm for trade dates up to F minus 7 calendar days. effective window end = min(segment end, F minus 7 days), F being the
  newest day file of the store being read that holds at least one row. If the effective window end is before d, or before the
  segment end and no qualifying purchase was found in [d, effective window end], the deposit day is not_determinable. A purchase
  found inside the covered range is a fact and is classed even when the window is not fully covered.
- not_determinable also holds: deposit amount zero or null; account not found in the store at all (no row of the account in any
  day file read); a Buy row with an unreadable or missing trade_date on the candidate range (the number of such rows is reported).
- The count never guesses: a deposit day that cannot be placed is not_determinable, not never_in_window.

## 8. Standing purchase plan (counts only, best effort)
deposits_into_accounts_with_a_standing_purchase_plan: a deposit day counts if, in the 90 calendar days before d, the account bought
(qualifying Buy, de-duplicated) the same asset_id on at least three distinct trade dates and the largest gap between consecutive
such dates is at most 35 days. This is a PROXY (a recurring same-asset buy), not a plan record; if asset_id is absent in the store
the count is omitted. Reported with how many of those deposit days fell in same_day.

## 9. Output discipline
Counts only in the tracked record: no account id, client name, amount, security name or ticker; days written with separators; no
run of 8 or more digits. The row-level work file lives under C:/dev/_irpt_private_evidence_20261009/IRPT_DASHBD/
0.9.0_WK_IRPT_DASHBD~131/. The count names no winner among START, MID and END and does not rank them.
