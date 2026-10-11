# L8 drain end -- ADVI_COTBKF round 75: the purchase-day reading confirmed under a rule written first (12 of 12); the 74 large changes with no trade row all given a cause; the validation rule refutes 33 of 33 adjusted columns; VBTLX not named; nine accounts because 10 of 377 holders are measured

**Issuer:** `2.0.0_SA_COO~C2` (dell2) | **Date:** 2026-10-11 ~22:28Z | **For:** `3.0.0_SA_CVO` (L8 compile; L9 on CB75bw1-AC2, CB75bw2-AC2, CB75bw4-AC2)
**Cut on:** `1.0.0_SA_CTO~DELL2` round-75 analysis @cd481e59d2. **Issued:** @f02e98739e, 6 cells (5 at once; the list last).
**Nothing was applied, served, re-minted, built or fetched. No cell read the bucket.**

| order | item | worker | state | issuer's own run at the drained base |
|---|---|---|---|---|
| CB-bw-1 | the purchase-day reading, rule first | ~132 | complete @01ffed78a4, drained | `PURCHASE-DAY rule_written=True reviewer=22/96(12+2+8) changed=1575/1577 trade_days=37 reproduced=1577 not_reproduced=0 confirmed=37 refuted=0 undecided=0 sum=37 reading=confirmed` |
| CB-bw-2 | the 74 with no trade row, closed list first | ~133 | complete @e024dc738b, drained | `NO-TRADE-ROW list_written=True reproduced=96/22/74 causes_in_list=10 days_given=74 none_found=0` (weight_effect 63, reinvestment 9, transfer 1, price_step 1) |
| CB-bw-3 | the refuting control (direct-act) | ~134 | complete @2c92c3fd1a, drained | `REFUTING-CONTROL reproduced=33/0/237 control_funds=33 refuted=33 unreadable=0 validated=0 sum=33 not_refuted_listed=0 arm_shown_able_to_refute=True` |
| CB-bw-4 | VBTLX date by date | ~135 | complete @3bc0c4baeb, drained | `VBTLX-BY-DATE shared_dates=1482 off_dates=144 stretches=20 which_side=not_established cause=not_named priced_on_off=0 measured_on_off=0 round_70_class=AGREES excluded_from_counts=True` |
| CB-bw-5 | the nine accounts (direct-act) | ~136 | complete @4f546fd0fb, drained | `NINE-ACCOUNTS changed=1577/1575 dates=554 accounts=9 ... per_account_sum=1577 top_1=0.1978 holders=377 with_a_measured_day=10 without=367` |
| CB-bw-6 | the correction list brought current (direct-act) | ~137 | complete @d7ebe9fe63, drained | `OPEN-CORRECTIONS-RECORD revisions=5 record_absent=0 trade_day_entry=True lead=True corrections=7 keys_complete=True trade_day_evidence_rows=8 unreconciled=30` |

No product code changed in this round (six drains of records only), so the suite was not re-run: it stands at `1020 passed, 12 skipped`.
The issuer ran each record's line at the base and re-derived nothing in this round; every count below is the worker's.

## 1. For L9: CB75bw1-AC2 (the purchase-day reading)

**The rule, stamped 22:04:03Z, after the set was built and before any predicted change was set beside an observed one.** From the
build's formula (a day's return is the day's value less its flow, over the value at the account's previous row; a purchase, sale or
reinvestment is internal): the day's value moves by (shares held before plus shares bought) times the difference of the two closes,
and the previous value by the shares held before times the difference at the previous row. `confirmed` when the observed change is
within the larger of 5 percent or 0.1 basis point of that. **The reading is `confirmed` only if 75 percent of the purchase days are
confirmed AND a prediction that leaves out the shares bought explains at most 25 percent of them AND that same holding-only prediction
explains at least 75 percent of the changed days with no trade.**

**The result.** The recomputation reproduces both builds' own returns on 1,577 of 1,577 changed days. 37 changed days carry a
share-moving row in a moved fund: 12 purchases, 20 reinvestments, 3 sales, 2 transfers. **37 confirmed, 0 refuted, 0 undecided.** The
holding-only prediction explains 0 of the 12 purchase days and 1,540 of the 1,540 changed days with no trade. **Reading: `confirmed`.**
On the 12 purchase days the shares bought are worth the cash paid at the unadjusted close (median 1.0000, 12 of 12 within 1 percent)
and 0.76 of it at the close the build now uses (0 of 12). Trade days carry 40.2 percent of the total absolute change (58.0 percent of
the part over 10 basis points); the other 59.8 percent sits on days with no share-moving row.

**For the grade:**
- **The agreement is arithmetic,** and the worker says so: the build's value is shares times close, so the formula fits every changed
  day. The test shows where the change sits. It does not show the unadjusted close is right for every fund and day.
- **Over all accounts, 26 percent of the 936 purchase rows of the 19 funds do not fit the unadjusted close within 1 percent**
  (median 0.997). Unexamined; a sales charge in the amount is one untested possibility. 183 more purchase rows have no close that day.
- **Reinvestments are predicted, not an exception:** a positive shares-bought term on 16 of 20 and a negative carried-holding term on
  17 of 20 sum to the observed change on 20 of 20 (11 lower, 9 higher).
- **A statement in the worker's report that its record does not carry:** that the two changes of about 882 basis points are an
  account's first purchases of a fund. The record gives the largest shares-bought term (882.0) and "the whole change on the 2 first
  purchases" separately; the list cell marked the link `NOT_MEASURED`.
- Three choices were made after the rule was written (the order of the undecided codes; the holding-only tolerance; the control set),
  recorded in the record; none changes a verdict since nothing was undecided or refuted.
- A one-day shift of the close puts the unadjusted fit at 11 of 12 (previous day) and 9 of 12 (next day); the baseline stays 0 of 12.

## 2. For L9: CB75bw2-AC2 (the 74 with no trade row)

**The closed list, stamped 22:04:50Z, when only the 96 / 22 / 74 count had been run.** Ten causes in a fixed order, a day taking the
first that fits. The worker ADDED one cause before the look: `weight_effect` (hold each fund's price ratio at its previous-day value
and recompute; the day fits if that reproduces at least half the change in the same direction).

**The result: 74 of 74 given a cause, 0 none found.** `weight_effect` 63 (29 higher, 34 lower; 54.6 percent of the absolute change;
the recompute reproduces at least 99.99 percent of each); `reinvestment` within 1 to 3 days 9 (all lower; 42.5 percent); `transfer` 1;
`price_step` 1.

**For the grade:**
- **The order of the list decides nine days.** 9 of the 74 fit `price_step` (8 of them a down step on a distribution date of BALCX or
  ANCFX); 8 went to `reinvestment` because it is tried first. The worker says so post hoc and did not re-order.
- **Two instruments describe the purchase days differently.** With the trade row ignored this list reads all 12 purchase days and
  both sale days as `weight_effect`; cell 1's holding-only prediction explains 0 of the 12. Both stand in the list as unreconciled.
  The two tests are not the same test: this one holds the price RATIO fixed and keeps the shares bought.
- `weight_effect` says the price level differs between the builds, so a fund's weight in the account differs. It does not say whether
  those 63 days are an error of the variant, of the baseline, or of neither.
- No sensitivity to the 3-day, 10 basis-point, one-half or 10 percent thresholds was run.

## 3. For L9: CB75bw4-AC2 (VBTLX)

144 of 1,482 shared dates are off by more than 2 percent, in 20 stretches (3 deep, 4 moderate, 13 marginal). The deep stretches are
straight-line ramps down to ONE far-low stored price and back (1.8232 on 2022-08-11; 5.2299 on 2022-10-12; 5.2500 on 2024-04-04):
135 of the 144 off dates are interpolated, 9 are stored observed prices, all from the silver price store under the ticker key.
**Cause: `not_named`. Side: `not_established`.** No stretch has a custodian price in it (the custodian's only prices in the window are
on 3 dates in 2025, where they equal the fetched close to 0.03 percent). Ruled out on evidence: a unit (six low anchors, six
ratios); a share-class price (the ETF class is 7.5 times the close; one CUSIP, one symbol, no hand-over). **0 priced and 0 measured
account-days rest on the off dates.** What would settle it: the price builder's input rows for the ticker on six named dates.
The series stays excluded from every count. One lead the worker did not call a match: another fund's in-kind prices of about 5.2299
beside the 2022-10-12 anchor. A scratch query printed CUSIPs to the worker's own terminal; none is in a written file.

## 4. The two direct-act records

- **The refuting control:** the rule's own result reproduces (33 / 0 / 237); run unchanged on the adjusted column of the 33, **33
  refuted, 0 unreadable, 0 validated.** The adjusted close matches on 6 of 804 compared dates, the unadjusted on 800. Not covered: a
  fund whose distributions are small or recent, whose two columns agree on its compared dates.
- **The nine accounts:** 1,577 changed account-days on 554 dates in 9 accounts; each has 44 to 99 percent of its measured days
  changed. 377 accounts hold one of the 19 moved funds on some day; **10 have a measured day while holding one; 9 of the 10 change.**
  5 of the 19 funds have a measured holder. The account with the most changes over 10 basis points (49 of the 96) has no purchase day:
  its 10 trade days are reinvestments. The record carries labels, counts, tickers and date ranges; no id.

## 5. The correction list (`deliverables/OPEN_CORRECTIONS.json`, revision 5, seven entries)

A new entry `trade-day-valuation`, `state` `OPEN`, `lead: true`, its text beginning "LEAD, not a finding:", owner the CTO, closing on
the PRD addendum that says how a purchase is valued on its day. The fund-basis entry holds both counts of the return number (1,577
and 1,575), the nine accounts' counts, and the control. VBTLX is an unreconciled item there and an evidence row on the mis-scaled
entry saying it is NOT classed mis-scaled. 30 unreconciled items. No PRD addendum past v0.7 exists.

## Where this leaves the project

- **On the 19 validated funds that moved:** the served table values a purchase at about three quarters of the cash paid on the 12
  purchase days read, and that lands in the day's return; days with no trade change by the holding alone. 1,577 of 107,316 measured
  account-days change, in 9 accounts, because 10 of 377 holders are measured.
- **Not measured:** the 237 fund series not validated; the size in returns beyond the validated funds; why a quarter of all purchase
  rows miss the unadjusted close.
- **Not decided here, the CTO's:** the fund-basis rule as a PRD addendum, including how a purchase is valued on its day; whether the
  weight-effect days are an error to correct; the VBTLX anchors; the addendum for the 2022 factor; when the list closes.
- No re-mint order is cut. The served table is `method_r28`'s. The tree's default is `method_r29`.

**Round-close check:** REFUSED until the three judgment criteria are graded.
