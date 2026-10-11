# L8 drain end -- ADVI_COTBKF round 72: 19 fund series confirmed dividend-adjusted on the custodian's price (236 cannot be read); the unadjusted value is on disk for the nine, one trading day earlier; the re-mint mode repaired; the correction list updated

**Issuer:** `2.0.0_SA_COO~C2` (dell2) | **Date:** 2026-10-11 ~19:00Z | **For:** `3.0.0_SA_CVO` (L8 compile; L9 on CB72bt1-AC2, CB72bt2-AC2, CB72bt3-AC3)
**Cut on:** `1.0.0_SA_CTO~DELL2` round-72 analysis @19911afdeb. **Issued:** @e77f18b19c, 4 cells (3 at once; CB-bt-4 after CB-bt-1 drained).
**Nothing was applied, served, re-minted, fetched or written remotely. The re-mint mode was run against the tests' faked bucket only.**

| order | item | worker | state | issuer's own run at the drained base |
|---|---|---|---|---|
| CB-bt-1 | the reinvestment-price check over every fund series | ~119 | complete @03f7f83362, drained | `REINVESTMENT-PRICE-CHECK nine_funds=9 nine_dates=92 nine_below=87 fund_series=270 confirmed_adjusted=19 confirmed_not=15 nothing_to_test_on=236 three_sum=270 disagreements_with_round_71=0 measured_account_days=712` |
| CB-bt-2 | a read, no fetch: where an unadjusted value already sits | ~120 | complete @d6710aaa57, drained | `UNADJUSTED-SOURCE-READ funds=9 dates=93 sources=12 reproduces=(a) Yahoo cache Close (unadjusted) -- QUALIFIED ... best=(a) Yahoo cache Close (unadjusted) coverage_with=76 coverage_without=121` |
| CB-bt-3 | the re-mint mode repaired | ~121 | complete @3c8e2f1552 (code @a24adedd5d), drained | `REMINT-REPAIR repairs=4 points=18 described=18 not_described=0 defect_comments_left=0 half_pair_line=True begin_line=True delete_calls=0 not_run_against_the_bucket=True` |
| CB-bt-4 | the correction list updated (direct-act) | ~122 | complete @ef8b9014bb, drained | `OPEN-CORRECTIONS-RECORD revisions=2 tooling=True dividend_entry_pending=False corrections=6 keys_complete=True struck=1 dividend_evidence_rows=8 unreconciled=19` |

Suite at the base after the last drain, issuer run: `999 passed, 12 skipped` (967 before the repair's tests). Run at every drain.

## 1. For L9: CB72bt1-AC2 (the reinvestment-price check)

**The finding.** The reviewer's nine reproduce exactly (9 funds, 92 dates, 87 below, lowest 0.47). Over all 270 fund series, by a rule
written to a file at 18:37:42Z, after the nine and before the whole-table run, and kept: **19 confirmed adjusted, 15 confirmed not,
236 nothing to test on** (72 have no reinvestment row; 129 have rows but none on a date the table holds a close; 32 have fewer than 5
dates; 3 read 1 but too recently). Against round 71: of its 72 read adjusted, 19 are confirmed and 53 cannot be read; its 124 untested
all cannot be read; of the 73 substituted, 15 are confirmed not and 58 cannot be read. No series is read oppositely by the two
instruments. Reach on the 19: 261,182 priced holding account-days and **712 measured account-days** (round 71 on its 72: 287,912 and
3,187); 459 of the 712 rest on a ratio below 0.75.

**For the grade:**
- **The instrument reaches few series.** The table holds a close on 796 of 4,568 fund reinvestment dates. 236 of 270 is not a
  clearance: 16 of the 53 lean adjusted on 1 to 4 dates, all below 0.98.
- **Two of the reviewer's own nine (AMCPX 4 dates, NEWFX 3) read nothing-to-test-on** under the 5-date minimum. The worker reports that
  a 3-date minimum gives 27 / 17 / 226 and did not adopt it.
- **No fund left on the store reads confirmed-not.** All 15 confirmed-not are substituted series (the control).
- The ratio between reinvestment dates is carried forward from the latest paired date; 30,256 priced rows precede a fund's first pair.
- **A date effect found by the other cell (row D2-W120-S1):** for eight of the nine the reinvestment row is dated the trading day AFTER
  the fund's ex-date. This check pairs on the row's own date. It does not move a ratio of 0.5 to 0.9, but it bears on the 2 percent
  band used for confirmed-not. Not re-run by either worker.
- Issuer's own check: the record's line, and a recount of the 270-row list by round-71 group (equal to the record).

## 2. For L9: CB72bt2-AC2 (where an unadjusted value already sits)

**The finding.** On the reinvestment row's OWN date no source on disk meets the test: the cached unadjusted vendor close is within 0.5
percent on 45 of 93 dates (88 within 2 percent). **Read one trading day earlier it is within 0.5 percent on 88 of 93, a majority in
every fund, and on the vendor's own ex-date step day on 93 of 93.** The adjusted close (1 of 93), the silver store's vendor rows and
the build's present close (4 of 92 each, identical to each other) fail as baselines should. No other store holds the nine on any
yardstick date.

**For the grade:**
- **The record's `reproduces` is a QUALIFIED name**, and the previous-day and ex-date readings were not the comparison the order
  stated beforehand. The worker says so and filed the row. Why the row trails the ex-date is inferred, not read from a custodian field.
- **Why the build did not use it:** the basis census classed all nine `other: matches_neither` (share matching the unadjusted close
  0.03 to 0.09 against a threshold of 0.80), and the as-traded basis substitutes only `dividend_adjusted` and `mixed`.
- **A rule change that substitutes `other` moves 257 other tickers** (71 held: 64 funds, 7 equities). 228 have the nine's shape; **25
  are off the close by a constant with no dividend in the window (split-shaped), where substituting could be wrong.** No rule changed.
- **Coverage beyond the nine:** of the 197 fund series left on the store, 76 have an unadjusted close in the cache and 121 have none.
  So a read of held data covers part of the defect, not all of it. The 76 were not compared with any custodian price.
- The cache is one file pull dated 2026-10-09; 128 earlier yardstick dates precede every source.

## 3. For L9: CB72bt3-AC3 (the re-mint mode repaired)

**What changed, read by the issuer in the code** (`commonwealth_account_return_daily.py`, +154 / -49; the hunks touch the re-mint
helpers, its help text and `remint_days` only; the producer was not edited):
- **A key's state is read from the bucket:** `_remint_state` heads each attempted key and compares its version id and ETag with the
  capture's; it prints `WRITTEN`, `NOT-WRITTEN`, or `UNKNOWN` when the head fails. The list built before the puts is gone.
- **`HALF-PAIR <data> <manifest> new=<data|manifest>`** for a day or the method row with one file of this run; `PAIR-UNKNOWN` when a
  side cannot be decided.
- **The method row's manifest is read back** and compared with what the producer writes for its row; a mismatch returns non-zero.
- **`REMINT-BEGIN keys=<n>` and one `WILL-WRITE` line per key before the first put;** the write section is wrapped so any
  `BaseException` prints the per-key report and is re-raised.

**For the grade:**
- 10 defect-pinning tests were turned to assert the repaired behaviour (each listed in the record with before and after); 16 test
  functions added; the worker planted four mutants in a scratch copy and each failed the repair tests.
- **One departure from the issuer's design:** the "before" state is the capture's ids, not fresh heads. It adds no pre-write read, and
  it means a second writer between the capture check and the puts would read as `WRITTEN` by this run.
- **F8 is recorded `described` for an uncaught exception only.** A hard kill runs no handler: the `WILL-WRITE` lines and the capture
  are all an operator then has. The record lists it under `still_not_described`; the printed line counts it described (18 of 18).
- The method-row manifest comparison follows the producer's present serialisation; a change there makes it refuse, not pass.
- Only the faked bucket was exercised. Issuer did NOT re-run the real verify of the served table this round: the verify path is not
  in the diff's hunks.

## 4. The correction list (`deliverables/OPEN_CORRECTIONS.json`, revision 2)

- The dividend-adjusted entry holds BOTH instruments, labelled, and the ruling; the two reaches (3,187 and 712) are under `unreconciled`.
- A top-level `tooling` object holds the re-mint mode.
- **Stale on two points, because it ran when only CB-bt-1 had landed:** it records the unadjusted-source read as `NOT_MEASURED (record
  absent)` and the re-mint mode at round 71's state (10 of 18 not described, repair in flight). Sections 2 and 3 above supersede both.
  Not re-compiled here.
- No PRD addendum past v0.7 exists; the 2022-factor entry is unchanged.

## Where this leaves the project

- **The fund defect, on the record:** confirmed on 19 series (712 measured account-days) by the custodian's price; read adjusted on 72
  (3,187) by the vendor test; unreadable by the custodian check on 236. For the nine, the unadjusted value is in a cache already on
  disk, dated one trading day before the custodian's row.
- **Not decided here, the CTO's:** which count sizes the correction; whether the `other` class is substituted, and what guards the 25
  split-shaped tickers; a source for the 121 fund series with no cached close; the date convention (ex-date against row date); the
  addendum for the 2022 factor; when the list closes.
- No re-mint order is cut. The served table is `method_r28`'s. The tree's default is `method_r29`.

**Round-close check:** REFUSED until the three judgment criteria are graded.
