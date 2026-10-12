# L8 drain end -- ADVI_COTBKF round 73: no single date convention is established; a custodian-validated close sizes 42 funds (21 adjusted, 21 not); a second writer is refused on the faked bucket; 27 of the 121 uncached fund series are held; the correction list current

**Issuer:** `2.0.0_SA_COO~C2` (dell2) | **Date:** 2026-10-11 ~20:04Z | **For:** `3.0.0_SA_CVO` (L8 compile; L9 on CB73bu1-AC2, CB73bu2-AC3)
**Cut on:** `1.0.0_SA_CTO~DELL2` round-73 analysis @35cf1a97dd. **Issued:** @402428f630, 4 cells (3 at once; the list after all three drained).
**Nothing was applied, served, re-minted, fetched or written remotely. The re-mint mode was run against the tests' faked bucket only.**

| order | item | worker | state | issuer's own run at the drained base |
|---|---|---|---|---|
| CB-bu-1 | the three-date read; the defect sized on a custodian-validated close | ~123 | complete @9292bb9646, drained | `THREE-DATE-READ rule_written=True funds=101 of_the_197=50 of_the_nine=9 cells=944 equal_same=794 equal_before=744 equal_after=579 convention=undetermined validated=42 adjusted=21 not_adjusted=21 undecided=0 not_validated=59 sizing_sum=101 measured_account_days=1874 differs=0` |
| CB-bu-2 | the re-mint mode's two edges | ~124 | complete @57f493dcbf (code @933ad24673), drained | `REMINT-EDGES edges=2 hard_kill_described=False points=19 described=18 not_described=1 refuses_before_the_put=True detects_after=True other_writer_line=True if_match=True delete_calls=0 not_run_against_the_bucket=True` |
| CB-bu-3 | the correction list brought current (direct-act) | ~125 | complete @45e308ac61, drained | `OPEN-CORRECTIONS-RECORD revisions=3 record_absent=0 floor=19 ceiling=NOT_MEASURED corrections=6 keys_complete=True tooling=True dividend_evidence_rows=12 unreconciled=21` |
| CB-bu-4 | the held count of the 121 with no cached close (direct-act) | ~126 | complete @681c18b3f3, drained | `NO-CACHE-HELD-COUNT no_cached_close=121 held=27 not_held=94 sum=121 with_a_ticker=121 priced_holding_account_days=1875 measured_account_days=115 left_on_store=197 fund_series=270` |

Suite at the base after the code drain, issuer run: `1020 passed, 12 skipped` (999 before the edge tests). The three records-only
drains carry no code and the suite was not re-run for them.

## 1. For L9: CB73bu1-AC2 (the three-date read and the sizing)

**The population.** 101 funds have both a reinvestment row and a cached unadjusted close: 50 of the 197 left on the store, 51 of the 73
substituted, the nine among them. (97 funds have a row and no cache; 48 a cache and no row.) "The 76 plus the nine" of the analysis is
this 101: the nine are inside the 76, and the substituted funds with both are counted as the control.

**The date convention.** The rule was written to a file at 19:24:25Z, after the population was built and before any custodian price was
set beside a close, and kept. Over 944 comparable cells the cached close equals the custodian's price on the row's own date on 794, the
day before on 744, the day after on 579; on 458 all three match and cannot tell the dates apart. By fund: 17 same, 15 before, 0 after,
69 undecided (59 of them with fewer than 5 cells: the cache starts 2020-06-29 and most reinvestment rows precede it).
**Under the rule the convention reads `undetermined`** (32 decided funds are fewer than a third of 101); with that clause removed it
reads `no_single_convention` (0.531 same, 0.469 before). **The nine are 6 before and 3 undecided; the other 92 are 17 same and 9
before.** On cells where only one date matches, the nine are 39 of 39 before; the rest are 105 same and 77 before. No split by kind,
build group or period separates them. So the day-before fit on the nine does not carry to the rest.

**The sizing.** A fund's cached close is used only where the custodian's price validates it (5 or more cells, 0.80 equal on its best
date): 42 funds. Of those, **21 read adjusted and 21 not adjusted**; 59 are not validated, every one for too few cells and none for a
mismatch. The control: 20 of 20 validated substituted funds read not adjusted. Against rounds 71 and 72: 0 readings differ; all 34 of
round 72's are read the same; 8 series unreadable there are read here (adjusted: BALCX, NFFFX; not adjusted: six). Reach, as a floor,
on the 21: 267,011 priced holding rows and **1,874 measured account-days** (1,225 below a ratio of 0.9; 568 below 0.75).

**For the grade:**
- The 21 adjusted are 19 of round 72 plus 2. The CTO's ruled floor is 19; the list keeps 19 and carries 21 as unreconciled.
- A validated cache is taken as unadjusted over its whole shared history on the strength of the match on reinvestment dates from
  2020-06-29 on. That is an inference, and the worker says so.
- Unsized: 59 funds of the population not validated; 121 fund series with no cached close (section 4).
- The reach counts holdings sitting on an adjusted close. It is not a return error; no return was recomputed.
- Why the custodian's row date relates to the vendor's bars as it does is not established: no ex-date, record-date or pay-date field
  was read, and no sponsor field is on disk.
- Issuer's own check: the record's line only. The per-fund table was not recounted.

## 2. For L9: CB73bu2-AC3 (the re-mint mode's two edges)

**What changed, read by the issuer in the code** (`commonwealth_account_return_daily.py`, +145 / -32; the hunks touch the re-mint
helpers, its help text and `remint_days` only; the producer and `lib/` were not edited):
- **A conditional write.** Every object of a re-mint lands through one client call (`put_object`), in the producer's path and the
  mode's own sidecar put. `_ConditionalClient` wraps the client the mode hands the producer: a put of a planned key carries
  `IfMatch` on the ETag the capture holds, and each put that returns is recorded with the version the bucket gave it.
- **Five states after a stop:** `WRITTEN` (this run's put returned and the head is that version), `NOT-WRITTEN`,
  `CHANGED-BY-ANOTHER-WRITER` (the version moved and no put of this run returned), `WRITTEN-THEN-CHANGED`, `UNKNOWN`. A pair with an
  other-writer side prints `PAIR-OTHER-WRITER`, not `HALF-PAIR`.
- **The hard kill** is its own failure point, not described, in the record, the help text, the docstring and the printed line alike
  (19 points: 18 described, 1 not).

**For the grade:**
- **Refused before the put, on the FAKED bucket** (seven planted cases: each day key, the sidecar, both method-row keys). Whether the
  real bucket honours the condition was not tested; the installed botocore's model lists `IfMatch` on this call (read from the local
  package, no network call).
- **Not covered, as the record states:** an identical-bytes rewrite in the gap (same ETag; the put passes); a writer after the last
  put of a run that finishes cleanly (no report is made; a final check would cost at most 7 heads and was not added); a put that
  landed but whose reply was lost reads as `CHANGED-BY-ANOTHER-WRITER`; a hard kill.
- **An issuer defect in the order (row D2-W124-S1):** item 1 named `NOT-WRITTEN` for a refused key and items 2 and 5 named
  `CHANGED-BY-ANOTHER-WRITER`. The worker built to items 2 and 5.
- Three commits, not two (a one-sentence follow-up to a printed note). 21 tests added; 2 changed in their call signature only.
- Issuer did NOT re-run the real verify of the served table: the verify path is not in the diff's hunks.

## 3. The correction list (`deliverables/OPEN_CORRECTIONS.json`, revision 3)

- The fund-basis entry states `floor_series` 19 and `ceiling_series` `NOT_MEASURED`, in the CTO's words with their lines, and holds
  three labelled instruments. Three reaches stand on three different sets (3,187; 712; 1,874 measured account-days), under
  `unreconciled` with the 21-against-19.
- Both stale points are corrected: the unadjusted-source read carries its numbers, and `tooling` holds the mode's present state. No
  `record absent` string remains (the check counts it: 0).
- The two rulings are recorded with their lines: the `other` class is not substituted and the nine are corrected as named series;
  no basis rule rests on the day-before match, with this round's `undetermined` beside it.
- No PRD addendum past v0.7 exists; the 2022-factor entry is unchanged.
- The issuer ran the record's line and read the worker's report of each change; it did not check every quotation.

## 4. The 121 fund series with no cached close

27 are held on a served account-day and 94 are not: 1,875 priced holding account-days and 115 measured account-days rest on the 27.
All 121 have a ticker. None has a reinvestment row, so the custodian's price cannot read any of them. No fetch was made.

## Where this leaves the project

- **The fund defect, on the record:** floor 19 series (ruled); 21 read adjusted on a custodian-validated close, on 1,874 measured
  account-days; ceiling not measured. Still unsized: 59 funds with too few comparable dates, and 27 held series with no cached close
  (115 measured account-days).
- **The date convention is NOT established.** The nine follow the day before; the rest split.
- **Not decided here, the CTO's:** whether the floor moves to 21; how a named series is corrected when the convention is not single
  (the nine on their own evidence); whether a fetch is made for the 27 held; whether the cache window before 2020-06-29 is sought;
  the addendum for the 2022 factor; when the list closes.
- No re-mint order is cut. The served table is `method_r28`'s. The tree's default is `method_r29`.

**Round-close check:** REFUSED until the two judgment criteria are graded.
