# L8 drain end -- ADVI_COTBKF round 70: the open-corrections list; the 2022 factor reads APPLY; the scan widened; the late-receipt rule out of sample; a re-mint path built and not run

**Issuer:** `2.0.0_SA_COO~C2` (dell2) | **Date:** 2026-10-11 ~17:02Z | **For:** `3.0.0_SA_CVO` (L8 compile; L9 on CB70br2-AC2, CB70br3-AC2, CB70br4-AC2,
CB70br5-AC3)
**Cut on:** `1.0.0_SA_CTO~DELL2` round-70 analysis @991f749df1 and PRD ADDENDUM v0.7 @72d624cd26. **Issued:** @a91be43451, 5 of 5 chains.
**Nothing was applied, served, re-minted or written remotely. The re-mint path was built and tested and was NOT run against the bucket.**

| order | item | worker | state | issuer's own run at the drained base |
|---|---|---|---|---|
| CB-br-1 | the open corrections as one tracked list (direct-act) | ~111 | complete @a1a3a2aa40, drained @f9c64c5a3c | `OPEN-CORRECTIONS-RECORD corrections=6 keys_complete=True states=NOT_ADOPTED,OPEN evidence_rows=22 unreconciled=15 served_method=method_r28 tree_default=method_r29` |
| CB-br-2 | the 2022 spin-off's evidence record | ~112 | complete @1378157ccd, drained @cf12fda202 | `SPINOFF-2022-EVIDENCE cusip=00206R102 event=2022-04-11 factor=1.324 pairs_before=16 pairs_after=26 without_before_2pct=0 with_before_2pct=15 without_after_2pct=26 reads=APPLY measured_account_days=28` |
| CB-br-3 | the close-against-trade scan widened | ~113 | complete @81575c76d5, drained | `SCAN-WIDE-RECORD r69_securities=720 r69_pairs=7979 widenings=7 class_sum=732 mis_scaled=8 too_few_left=334 thin_beyond_10pct_left=44 no_close=1700 no_close_held=1693 fixed_income_unit=True measured_account_days_affected=470` |
| CB-br-4 | the late-receipt rule out of sample | ~114 | complete @7377cc8ec0, drained @4f00757f67 | `RECEIPT-OUT-OF-SAMPLE-RECORD reproduced_blanked=410 reproduced_targets=148 holdouts=2 test_targets_blanked=72+37 test_non_targets_blanked=0+0 same_constants=False+False blanked_r28=410 blanked_r29=411 receipt_classes=7 months_losing_every_day=10` |
| CB-br-5 | a re-mint path in the mint adapter, built and tested, NOT run | ~115 | complete @b3f5e99ed7, drained | `ARD-REMINT-PATH mode=True list_flag=True capture_flag=True last_line=True tests=37 delete_calls=0` |

Suite at the base after the last drain, issuer run: `939 passed, 12 skipped`. Run at every drain of the round. After CB-br-5's drain the
issuer also re-ran the REAL verify of the table served today, because that cell refactored the verify's hash helper:
`ARD-COTTONWOOD-VERIFY days=3325 match=3325/3325 sidecar=match method_row=match manifests=3325/3325 split_store=absent`.

## What the issuer checked itself, and what it did not

- **CB-br-2:** recounted the 42-row pairs table: before the event n=16, without the factor 0 within 2 percent (median 0.7573), with it
  15 (median 1.0027); on or after n=26, without 26 (0.9993), with 0 (1.3231). Equal to the record.
- **CB-br-5:** read the mode's write calls and the order of its refusals in the code: every `REFUSED` precedes the write loop; writes go
  through the producer's `emit_day`; there is no delete or copy call. Did NOT run the mode. Did not read the 549-line test file.
- **CB-br-1:** read the list's table and printed PRD line 282. Did NOT check all 22 evidence quotations against their records.
- **CB-br-3, CB-br-4:** ran each record's line. Every count inside both records is the worker's.

## For L9

**CB70br2-AC2 (the 2022 event).** By the round-68 rule the record reads APPLY: before the event the factor reproduces the traded price
(15 of 16 within 2 percent) and the served close does not (0 of 16); on or after it the served close already does (26 of 26) and the
factor would break it (0 of 26). Every number is the worker's own derivation; the two earlier records agree on what they share. The
trade rows trace to the delivered transactions file by a hash and a file name carried on every row; the bronze bytes were not opened.
**For the grade:** 107 earlier trade dates cannot be compared (the served closes start 2020-07-01); one date reads 1.0304 with the
factor, no cause asserted; the reach is 3,434 priced holding account-days (round 69's scan said 3,062: it stopped at the last trade
date) and 28 measured account-days in one account, on only 1 of which the price LEVEL enters the return directly; the returns that
would move were not computed. The store holds four entries for the security, three of them before any close.

**CB70br3-AC2 (the scan widened).** The headline, as the record words it: "8 close series are mis-scaled (6 constant-scale and 2 step:
the seven of round 69, all still classed, plus OIEJX, which rests on 3 pairs over 17 days, 2 of them reinvestment prints) -- and that
count is a floor: 334 compared securities are still too few to class (209 have a single pair), 44 of the thin ones still carry a pair
more than 10 percent off, and 1,700 traded securities have no close in the table at all (1,693 of them held, 974,014 account-days
resting on them, every one NOT_MEASURABLE)." **For the grade:**
- The widening moved little: 20 of the 346 left TOO_FEW, almost all through reinvestment prints (1,801 pairs); nearest-close pairing
  added 42 pairs, because the table holds a security only from its first held day.
- **The 1,700 are mostly an absence, not an unmade join:** 1,610 have no row under any key in the six local caches; 90 have a row only
  under a ticker more than one CUSIP claims. And they carry 61.5 percent of the table's NOT_MEASURABLE account-days.
- **A new pattern, read by eye and not tested (row D2-W113-S1):** nine fund series classed NOISY start at a ratio of 0.47 to 0.84 and
  rise in jumps at distribution dates to about 1.00: the shape of a dividend-adjusted close used as a price. If that is what they
  are, the count of wrong series is not 8.
- The worker's own choices: the print-admission test, a minimum-quantity guard it added, and admitting one type with wider tails.
- Fixed income: the unit is fraction of par on both sides, and there are 0 comparable pairs (closes begin 2026-06-08, trades end
  2026-05-05), so it is not classed.

**CB70br4-AC2 (the rule out of sample).** The split was by the parity of a hash of the account id, fixed before any outcome. **Neither
half chose round 69's constants** (28 days, 0.99): both chose 24 days; half A's share is 0.99 from a range of 0.995 to 0.99; half B's
is 0.999, because no step there added mostly targets. Held out: fit on A, tested on B, 72 of 77 target days blanked; fit on B, tested
on A, 37 of 85 (67 at 0.995). 0 non-target outlier days blanked in either direction, on 4 and 13 such days, which the worker itself
calls a thin test. On the `method_r29` build with the served hold list: 411 days blanked against 410; one day is blank under r29 only.
The 410 by receipt: dividend 163, fee refund 108, more than one class 116, reinvested distribution 19, interest 2, 12b1 credit 2. Ten
account-months lose every measured day (8 of them had one). 63 account-months and 17 account-years fully measured today would gain a
blank day. The record recommends nothing. **For the grade:** time was not held out (286 of the 410 are May and June 2026); the labels
on both halves are round 68's classing; half B's constant follows from the worker's own selection rule.

**CB70br5-AC3 (the re-mint path).** `--remint` replaces the day files on a list and refuses, before any write: an empty or malformed
list; a listed date not in the manifest; a capture missing a date or a field, or naming a date off the list; a served ETag or version id
that moved; a listed day equal to the served one; ANY unlisted day that differs; a manifest with no pinned split store or no hold list;
missing pair files; an unstamped manifest; a sidecar or method row that differs and is not in the capture, or is absent. 37 tests on a
versioned fake bucket; one asserts every read precedes the first put; one asserts no delete. On a read-back mismatch it stops, prints
the keys written, returns non-zero and rolls nothing back. **For the grade:** only the fake bucket was exercised (real head and version
shapes, ETag quoting and the 3,323-day unlisted read are untested); `build` was not run, so no real manifest carries a hold list yet;
the worker added the mint's bond count to the mode, which the order did not ask for; the upstream silver re-serve it presumes is
another script's write and is not built; the naming gate warned on `s3://%s/%s` strings in its messages (prints, not addresses).

## The two counts of the flow change

Row D2-W114-S1 (worker ~114's exact comparison): the flow differs on 47 account-days over 46 dates between the two methods, 44 of them
in the outflow term. That is the issuer's round-69 count (47 over 46), now from a second derivation on the hold-list builds. The 44
over 43 of round 69's facts record is the day-file count. The list (CB-br-1) carries both as unreconciled; this row is the first
record that names where the three differ. Not reconciled by the issuer.

## Where this leaves the project

- **The list exists** (`deliverables/OPEN_CORRECTIONS.json`, six entries). It was compiled BEFORE this round's other four records
  landed, so its entries for the 2022 factor, the scan and the late-receipt rule cite round 69's numbers, not round 70's. It is not
  re-compiled here.
- **Not decided here, the CTO's:** the addendum that applies the 2022 factor; what to do about the nine ramp-shaped fund series and
  the 1,700 with no close; whether the late-receipt rule is adopted and with which constants; when the list is closed.
- No re-mint order is cut. The served table is `method_r28`'s. The tree's default is `method_r29`.

**Round-close check:** REFUSED until the four judgment criteria are graded.
