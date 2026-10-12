# L8 drain end -- ADVI_COTBKF round 76: by the price paid, 89 percent of trades in funds left on the store are over 20 percent off (98 percent of the substituted are within 1); 15 fund series fail by trades; the 26 percent is one fund and looks like a flat charge (post hoc); 16 of 31 measured trade days change

**Issuer:** `2.0.0_SA_COO~C2` (dell2) | **Date:** 2026-10-11 ~23:31Z | **For:** `3.0.0_SA_CVO` (L8 compile; L9 on CB76bx1-AC2, CB76bx2-AC2, CB76bx3-AC2,
CB76bx4-AC2)
**Cut on:** `1.0.0_SA_CTO~DELL2` round-76 analysis @8ae9f87cf2 (read by this seat from the file's own history). **Issued:** @ac8000c35b,
5 cells (3 at once; CB-bx-3 after CB-bx-1 and CB-bx-2; the list last).
**Nothing was applied, served, re-minted, built or fetched. No cell read the bucket.**

| order | item | worker | state | issuer's own run at the drained base |
|---|---|---|---|---|
| CB-bx-1 | the 26 percent, closed list first, two orders | ~138 | complete @dbc4d19482, drained | `PURCHASE-ROWS-OFF list_written=True reproduced=1119/936/690 off=246 given=246 given_alt=246 none_found=124 change_with_order=41` |
| CB-bx-2 | the price-paid instrument over the whole table | ~139 | complete @383f6a2c20, drained | `PRICE-PAID control=0/12 fund_series=270 trade_rows=91533 with_amount_and_quantity=91533 with_a_served_close=14250 funds_with_a_row=92 accounts=544 within_1=10523 b1_5=213 b5_20=303 over_20=3211 band_sum=14250 not_reached=178` |
| CB-bx-3 | every fund classed by its trades, rule first | ~140 | complete @a7a2e38ad2, drained | `FUNDS-BY-TRADES rule_written=True minimum_rows=5 share_fails=0.5 fund_series=270 fails=15 passes=17 mixed=0 too_few=60 no_trade_row=178 sum=270 named=15 changes_class=14 conflicts=0` |
| CB-bx-4 | the trade-day return across every account | ~141 | complete @609e6bfd6e, drained | `TRADE-DAY-RETURN quantity_written=True control=12/12 trade_account_days=15103 measured=31 blank=6143 accounts=928 accounts_measured=13 changed_over_10bp=16 b10_50=9 b50_200=5 over_200=2 band_sum=16 accounts_changed=4 funds_changed=3` |
| CB-bx-5 | the correction list brought current (direct-act) | ~142 | complete @bd2aa8da09, drained | `OPEN-CORRECTIONS-RECORD revisions=6 record_absent=0 trade_day_confirmed_on_12=True lead=False state=OPEN corrections=7 keys_complete=True trade_day_evidence_rows=14 unreconciled=34` |

No product code changed in this round (five drains of records, one channel row), so the suite was not re-run: it stands at
`1020 passed, 12 skipped`. The issuer ran each record's line at the base and recounted ONE thing itself: the per-fund list of cell 2
by the substituted flag (3,614 units, 112 within 1 percent, 3,205 over 20 on the funds left on the store; 10,636 units, 10,411 within
1 percent, 6 over 20 on the substituted). Equal to the record. Every other count below is the worker's.

## 1. For L9: CB76bx2-AC2 (the price-paid instrument)

**The denominators.** 270 fund series. 91,533 purchase and sale rows in every account (51,232 and 40,301), every one with an amount
and a quantity; 38 fall under the quantity guard; 91,040 units of (account, effective day, fund, kind). **14,250 units have a served
close on the trade's day; 76,790 pre-date their series' first stored close and are not read.** 92 funds and 544 accounts are read; 178
fund series are not reached (23 with no purchase or sale row; 155 whose rows all pre-date the first stored close).

**The result.** Over the 14,250 read units the served close is within 1 percent of the price paid on 10,523 (73.8 percent), 1 to 5 off
on 213, 5 to 20 on 303, over 20 on 3,211 (22.5 percent; 3,206 of them with the served close BELOW the price). **The whole of it sits
on one side of one flag:**

| funds | units | within 1 percent | over 20 percent off | median ratio |
|---|---|---|---|---|
| left on the store (197 series, 61 read) | 3,614 | 112 (3.1 percent) | 3,205 (88.7 percent) | 0.742 |
| substituted with the unadjusted close (73 series, 31 read) | 10,636 | 10,411 (97.9 percent) | 6 | 1.000 |

The control reproduces (the 12 purchase days: median 0.75864, 0 of 12). On the funds left on the store, sales are off as purchases
are (1,631 of 1,860 sale units over 20 percent; 1,574 of 1,754 purchase units): a front load does not explain it. The 178 series
unreadable by reinvestment and left on the store are sized for the first time: 43 have a read unit, 1,563 of their 1,736 units over 20.

**For the grade:**
- **The instrument reads 14,250 of 91,040 units.** The served table holds a security's close only from its first held day in the
  table, so five trades in six are before it.
- **The overall 73.8 percent is not the defect's size:** it is the substituted funds. The list records this as unreconciled.
- 225 units of the SUBSTITUTED funds are outside the 1 percent band and unexplained (VBIRX: 16 of 60 within 1 percent; one unit at
  0.167).
- Most of the 112 within-1-percent units on funds left on the store are one or two trades in June 2026, and two commodity trusts
  whose adjusted and unadjusted closes are the same: they do not show a right close.
- The share within 1 percent by year (2022: 48 percent; 2025: 97 percent) mixes different funds in different years; the worker did
  not read it as one adjustment shrinking.
- It counts units, not money, and does not say why any unit is off.

## 2. For L9: CB76bx1-AC2 (the 26 percent)

**The closed list, stamped 22:52:32Z, before any off row was looked at:** ten causes, the order (least to most coincidence-prone, the
rate-based fee last) and one alternative order (the fee causes early). Reproduced: 1,119 purchase rows of the 19 funds, 936 with a
close, 690 within 1 percent, 246 off.

**The result.** Under the stated order: a neighbouring day's close 46 (31 prior, 15 next); a reinvestment or exchange 21; a fee by rate
35; a constant excess 20; **none found 124.** Under the alternative: 17, 9, 51, 45, 124. **41 rows change cause with the order.** 243 of
the 246 are ONE fund (VEIRX); every off row has the price paid ABOVE the close. The cache has no fee, commission or price column.

**For the grade:**
- **The rate-based fee test fits at chance:** 51 rows, against 66 and 52 for the same test with every shortfall shifted by 0.35
  points either way. The worker built that control into the list beforehand and reports the test as not holding.
- **Sales are not clean either:** 840 of 942 within 1 percent; all 102 off rows have the price RECEIVED below the close.
- **POST HOC, the worker's, marked so and in no count:** on all 936 purchase rows the amount less shares times close lands within 15
  cents of 0, 3, 10, 15, 19, 30 or 34 dollars (112, 34, 3, 60, 24, 502 and 201 rows), and the sale rows show the same set reversed.
  121 of the 124 none-found rows sit at 3, 15, 30 or 34. A flat dollar charge inside the amount puts a row outside 1 percent exactly
  where the amount is small. **The constants were read off the rows after the look: this describes the rows and is not a test they
  passed.** What the charge is and who takes it is not established.
- So the list and the post hoc reading disagree on whether 124 rows are explained. Both stand in the correction list as unreconciled.
- The 183 purchase rows with no close all pre-date their fund's first served close.

## 3. For L9: CB76bx3-AC2 (which funds)

**The rule, stamped 23:07:58Z, when only the two records' totals had been read:** a unit within 1 percent passes; a unit 1 to 5 percent
off, a purchase up to 5.75 percent below the close, or a gap of 34.15 dollars or less in the charge direction is UNRESOLVED; every other
unit fails. A fund needs 5 decisive units on 3 distinct days; above 0.50 failing it `fails`, at or below 0.10 it `passes`; a fund
cannot pass on units inside the last 180 days alone.

**The result over 270:** fails 15, passes 17, mixed 0, too few 60, no trade row 178. **All 15 failing funds are left on the store:** 8
of the 19 moved in round 74, and 7 that were unreadable by reinvestment (PCBIX, SGIIX, GFFFX, FOCPX, AGTHX, NFFFX, VGHAX). The 17
passing are 15 substituted funds and the two commodity trusts. **0 conflicts with the reinvestment readings**, either way. The named
list is in the record; no correction is proposed.

**For the grade:**
- **The rule's charge excuse uses constants that cell 1 read post hoc.** The worker used them only to take units OUT of the failing
  count, and says so. With the excuse off, one substituted fund (VBIRX) goes from passes to fails.
- **238 of 270 series are not classed by trades.**
- `mixed` is empty: the worker does not say whether that is the data or the width of the unresolved band.
- Sensitivities, reported apart: a 3-unit minimum adds five failing funds (AMBFX, CAIBX, DFREX, ANCFX, ANWPX); a 10-unit minimum
  drops five and turns three passes to too few. No fund moves at a fail line of 0.40 or 0.60.
- Row D2-W140-S1: an issuer clash. The order asked for an `excluded` flag in a `.csv` whose nine columns it also fixed; the flag for
  VBTLX is in the record and the `.md` instead. VBTLX reads too few and is not named.

## 4. For L9: CB76bx4-AC2 (the trade-day return)

**The quantity, stamped 22:47:16Z, before it was computed on any row:** for a purchase, the cash paid less the shares at the served
close, over the value at the account's previous row. **For a sale the term is zero by this definition:** the sold shares are not in
the day's value, and the mis-valuation sits in the previous value, the carried holding, which is not revalued here. The control: on
round 75's 12 purchase days the term equals that round's shares-bought term at ratios of 0.99994 to 1.00004.

**The result.** 15,103 trade account-days in 928 accounts. 8,929 have no served close for any traded fund; 6,143 have a close and fall
on a blank day (6,136 of them because another holding is unpriced); **31 are measured, in 13 accounts. 16 of the 31 change by more than
10 basis points** (9 by 10 to 50, 5 by 50 to 200, 2 by over 200), all purchases, all with the served return too LOW, in 4 accounts and
3 funds. By price fit: 14 where the served close is over 20 percent off the price paid, 2 at 5 to 20, 0 within 5. None is fee-sized.

**For the grade:**
- **31 of 15,103.** The number describes where the served table is priced. It is the trade term only and a first-order term, not a
  rebuilt return.
- The blank days, counted apart and not added: 1,591 of 6,130 would exceed 10 basis points with a previous value formed from the
  positions that ARE valued (the worker calls it an upper figure: a partial sum); 46 of 122 with every position valued.
- Sales contribute nothing by the definition; round 75's three lower-return sale days came from revaluing the holding.
- The order's `blank` was "the rest"; the worker reports `no_close` as a third bucket and says so in the record.

## 5. The correction list (`deliverables/OPEN_CORRECTIONS.json`, revision 6, seven entries)

The trade-day entry reads "CONFIRMED ON 12, size open", `lead` false, `state` `OPEN`, with the four records in its extent and the
size written as what is measured (the trade term on 31 account-days; round 74's 1,577 of 107,316 for the validated funds) and what is
not (the carried holding across all funds; the blank and no-close trade days; the 178 series not reached; any amount in money). The
fund-basis entry gains the price-paid instrument; its floor stays 19, with "15 by trades" beside it as unreconciled. The rule's shape
from the analysis is quoted and marked NOT YET WRITTEN. 34 unreconciled items. No PRD addendum past v0.7 exists. One stale phrase
remains, by the worker's own note: an older item on the fund-basis entry still calls the 26 percent "unexamined".

## 6. A correction to this seat's round 68, on the CTO's sweep (msg 6095)

Seven round-68 files of this seat cite the CTO's round-68 analysis at a hash that names another seat's commit. The right hash is
96cb28be27. The files are not edited; a record beside the round-68 packet carries the correction (@9cb72d5d71). No count changes.

## Where this leaves the project

- **By the price paid, across 544 accounts:** the funds left on the store are valued more than 20 percent off on 89 percent of their
  read trades; the substituted funds are within 1 percent on 98 percent. 15 fund series fail and are named.
- **Not measured:** five trades in six (before the first stored close); 178 of 270 fund series; the carried holding's effect across
  all funds; anything in money.
- **Not decided here, the CTO's:** the fund-basis rule as a PRD addendum, now that the 26 percent has a shape (one fund, and a flat
  charge that is a post hoc reading, not a test); whether the 15 named funds are corrected and how; whether the served table should
  hold closes before a security's first held day; the addendum for the 2022 factor; when the list closes.
- No re-mint order is cut. The served table is `method_r28`'s. The tree's default is `method_r29`.

**Round-close check:** REFUSED until the four judgment criteria are graded.
