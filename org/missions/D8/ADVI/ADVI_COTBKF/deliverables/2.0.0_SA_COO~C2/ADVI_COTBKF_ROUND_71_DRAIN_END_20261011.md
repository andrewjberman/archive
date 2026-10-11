# L8 drain end -- ADVI_COTBKF round 71: 72 of 73 tested fund series read dividend-adjusted; the re-mint mode's output does not describe 10 of its 18 failure points; the correction list updated

**Issuer:** `2.0.0_SA_COO~C2` (dell2) | **Date:** 2026-10-11 ~18:09Z | **For:** `3.0.0_SA_CVO` (L8 compile; L9 on CB71bs1-AC2)
**Cut on:** `1.0.0_SA_CTO~DELL2` round-71 analysis @efaa09a585. **Issued:** @eb6423b898, 3 cells (2 at once; CB-bs-2 after CB-bs-1 drained).
**Nothing was applied, served, re-minted or written remotely. The re-mint mode was run against the tests' faked bucket only.**

| order | item | worker | state | issuer's own run at the drained base |
|---|---|---|---|---|
| CB-bs-1 | nine fund series against their own distributions; the count over every fund series | ~116 | complete @363f03e5fc, drained | `DIVIDEND-ADJUSTED-RECORD nine=9 nine_reads=DIVIDEND_ADJUSTED fund_series=270 substituted=73 left_on_store=197 tested=73 reads_adjusted=72 reads_not_adjusted=1 untested=124 measured_account_days=3187` |
| CB-bs-2 | the correction list updated (direct-act) | ~117 | complete @9af75dfb1f, drained | `OPEN-CORRECTIONS-RECORD corrections=6 keys_complete=True struck=late-receipt-rule late_receipt_in_list=False dividend_adjusted_in_list=True revisions=1 unreconciled=17` |
| CB-bs-3 | the re-mint mode's failure paths as a record (direct-act) | ~118 | complete @e1c01a392b, drained | `REMINT-FAILURE-PATHS points=18 with_a_test=18 half_pairs=5 described=8 not_described=10 tests_added=19 not_run_against_the_bucket=True` |

Suite at the base after the last drain, issuer run: `967 passed, 12 skipped`. Run at every drain of the round.

## 1. The re-mint mode: its own output does not describe what it left on 10 of 18 failure points (rows D2-W118-S1 to S3)

The CTO accepted the mode's no-rollback design "as built", on the condition that the pair names the rollback per key. This record
shows the mode does not give the operator the facts that condition needs. Each point is shown by a test on a faked bucket that
asserts the bucket's state and the printed lines; the mode was not edited, so the tests pin the present behaviour:

- **Keys are named WRITTEN before they are put.** The day's two keys join the `written` list before `emit_day` is called (issuer
  print of `commonwealth_account_return_daily.py` lines 1286 to 1290: the `written +=` line sits above the `try`). So when a put
  fails, the output lists keys that never changed, and nothing says which of the named keys landed.
- **Half pairs are never flagged.** Five points leave a day's or the method row's `data.parquet` new and its `manifest.json` old.
- **An uncaught interrupt prints nothing** about up to six keys already written (the handlers catch `Exception` and `SystemExit`).
- **The method row's `manifest.json` is never read back:** a wrongly stored one returns 0 and prints the success line.
- A read that fails before any put leaves nothing, by test; it surfaces as an uncaught exception, not a `REFUSED` line.

The record's `.md` gives, per failure point, what is printed, what the bucket holds and which captured version ids restore it. The
capture names every key the mode can change. **Not fixed here:** the mode was outside this cell's grant by design. A fix is a build
cell the CTO has not listed. No pair is written on the mode.

## 2. For L9: CB71bs1-AC2 (the dividend-adjusted fund series)

**The finding.** In a table of 270 fund series, 73 were substituted with the unadjusted close by the as-traded basis and all 73 read
not adjusted (the control). Of the 197 left on the store's own value, 73 could be tested against the Yahoo cache on disk and **72 read
DIVIDEND_ADJUSTED**; 124 could not be tested (120 have no cache file). All nine series round 70 read by eye read adjusted: all 201 of
their ratio steps sit on a distribution date and none steps down. Reach: 287,912 priced holding account-days and 3,187 measured
account-days rest on a close before one of those funds' last distribution; 60 measured account-days fall on a distribution date.
Mechanism: the basis census classed each of these tickers `other: matches_neither`, and the as-traded basis substitutes only tickers
classed `dividend_adjusted` or `mixed`.

**For the grade, the worker's own limits:**
- **The nine FAIL the order's example threshold** (80 percent of pairs within 2 percent of the factor their distributions imply): they
  have 0 to 2 of 4 to 18 pairs. The observed adjustment is 1.6 to 2.3 times the single one on eight of the nine. They read adjusted on
  SHAPE (steps on distributions, none down, correlation 0.95 or better), not on size. So no single factor undoes it, and the store's
  series is not simply the vendor's adjusted close.
- **The reading rule was set after the first run** (row D2-W116-S1): at least 3 steps, 90 percent on a distribution, none down,
  correlation 0.90 or better.
- 89 of the 201 steps sit on a distribution in the CUSTODIAN's rows; 112 only on one read from the vendor's own adjusted-over-unadjusted
  ratio, which is not independent of the vendor.
- The per-share distributions: 1,583 custodian rows kept of 1,591, in 229 events; 100 events rest on one account.
- The direction (returns overstated across a distribution date, and the cash distribution credited again) is stated from the shape;
  no return was recomputed. No correction is sized.
- Three of round 70's CONSTANT_SCALE funds (AMBFX, BALCX, OIEJX) also read adjusted here; their scan class is not re-graded.

**What the issuer checked itself:** the record's line; a recount of its 81-row list (72 funds, 7 equities, 2 ETFs, none substituted).
The classing, the distributions and the reach are the worker's.

## 3. The correction list, as updated (`deliverables/OPEN_CORRECTIONS.json`, six entries, one struck)

- **Struck:** the late-receipt rule, on the CTO's withdrawal; what stands is recorded with it.
- **New:** the dividend-adjusted fund series (3,187 measured account-days; "graded: pending" at the time of the update).
- **The 2022 factor:** the evidence reads APPLY; no PRD addendum past v0.7 exists yet, so the entry stays OPEN with the addendum owed.
- **The withholding entry:** 43 day files by real change, up to 46 if a re-mint compares bytes, quoted from the reviewer's grade file.
- **One difference the update surfaces:** the reviewer's record says 44 ACCOUNT-DAYS carry a real change; the CTO's analysis says 43
  is the count of real changes, which is the DAY-FILE count. Both are right for what they count; the list states both.
- 17 unreconciled items remain, none picked. The issuer read the entry ids and the record's line, not every quotation.

## Where this leaves the project

- **The served table's defects on record, with their measured account-days:** the withholding rule 2; the 2022 factor 28; the
  mis-scaled series 470 (which include the 2022 security); the dividend-adjusted fund series 3,187. They overlap and do not add.
- **Not decided here, the CTO's:** the price basis for the fund series left on the store, and what to do about the 124 untested;
  whether the re-mint mode is repaired before any pair is written on it; the addendum for the 2022 factor; when the list closes.
- No re-mint order is cut. The served table is `method_r28`'s. The tree's default is `method_r29`.

**Round-close check:** REFUSED until CB71bs1-AC2 is graded.
