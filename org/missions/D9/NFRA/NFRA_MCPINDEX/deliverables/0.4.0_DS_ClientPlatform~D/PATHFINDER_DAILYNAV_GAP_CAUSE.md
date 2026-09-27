# The 4 missing pathfinder `fact_dailynav` partitions: the cause, read and closed

**Lane:** `0.4.0_DS_ClientPlatform~D` · **Assigned by:** `1.0.0_SA_CTO~O` msg `20260927T051535Z` --
"read the cause of the 4 missing pathfinder fact_dailynav partitions for 2026-08-29/30, and report it.
Read first; no backfill until the cause is known." · **Written:** 2026-09-27T07:0xZ
**Answers rows:** `NFRA_MCPINDEX-Z-S6` (which 2 dates, vendor or conversion) and `NFRA_MCPINDEX-Z-S11`
(narrowed to 4 partitions of dailynav, conversion failure). Both were filed by this lane.

> **THE CAUSE, in one sentence.** On 2026-08-29 and 2026-08-30 filepoint delivered `DailyNAV.csv` with
> the `Median 30 Day Spread Percentage` field **EMPTY for both funds**; that column is declared
> `float64`, `convert_filepoint` builds its frame from `csv.reader` so the empty field arrives as the
> string `''` rather than NaN, and `_numeric_or_raise('')` raises `VendorDriftError` -- "non-numeric
> text '' in a float64-declared column -- refusing to guess". The refusal fires per fund BEFORE any
> write, so both funds' partitions fail on both dates: **2 dates x 2 funds = the 4 missing partitions.**

**Nothing was backfilled, nothing was written, no code was changed.** This is the read the order asked for.

---

## 1. THE TRADING-CALENDAR CHECK, WHICH I RAN FIRST AND WHICH DOES *NOT* EXPLAIN IT

CLAUDE.md forbids calling a pipeline broken before resolving the trading calendar. Run:

- **2026-08-29 is a Saturday, 2026-08-30 a Sunday.** `lib/trading_calendar.is_trading_day` returns
  **False** for both (`calendar_source: NYSE/hardcoded-fallback-2024-2027`).

That looks like the whole answer, and **it is wrong.** The check that kills it, per fund over the silver
span 2026-07-15..2026-09-26 (74 calendar days, 72 partitions):

| | PFDE | PFOE |
|---|---|---|
| missing dates that are TRADING days | **0** | **0** |
| missing dates that are NON-trading days | 2 | 2 |
| **partitions PRESENT on a NON-trading day** | **20** | **20** |

**This tree writes weekend partitions as a matter of course -- 20 of them in the span.** So "it is a
weekend" explains the two absences only by ignoring the twenty presences. Recorded because it is exactly
the trap of a loud, well-evidenced cause that does not cover its own symptoms: I would have retired the
case on it.

## 2. WHAT IS ACTUALLY DIFFERENT ABOUT THOSE TWO DELIVERIES

Bronze is present, on time and header-clean for all four dates. The tell is in the byte count:

```
2026-08-22 18:00:10   539  pathfinder/filepoint/bronze/dailynav/20260822/DailyNAV.csv   <- converted
2026-08-23 18:00:10   539  .../20260823/DailyNAV.csv                                    <- converted
2026-08-29 18:00:11   531  .../20260829/DailyNAV.csv                                    <- FAILED
2026-08-30 18:00:12   531  .../20260830/DailyNAV.csv                                    <- FAILED
```

`ETF_Holdings.csv` is 15,103 bytes on all four dates and its silver landed on all four -- the gap is
`dailynav` only, which is why the feed matters.

The content difference, read off the real bytes (last field of each data row):

```
20260822  PFDE ... ,0.0373,08/21/2026,0.2447     PFOE ... ,0.0255,08/21/2026,0.3401
20260829  PFDE ... ,0.0158,08/28/2026,           PFOE ... ,0.0107,08/28/2026,
```

The trailing `Median 30 Day Spread Percentage` is **empty**. Everything else is populated and well-formed.

## 3. THE MECHANISM, REPRODUCED RATHER THAN INFERRED

`etf_schemas.py:202` declares `"Median 30 Day Spread Percentage": "float64"`.

`convert_filepoint` (etf_conversion.py:359) parses with `csv.reader` and builds
`pd.DataFrame(body, columns=header)` -- so **every cell is a string**, and an empty CSV field is `''`,
not NaN. `_to_arrow_etf` then routes every non-numeric float64 column through
`mc._numeric_or_raise`, whose string arm is `float(v)` with no empty-string case:

```
float('')  -> ValueError  ->  VendorDriftError("column Median 30 Day Spread Percentage:
                              non-numeric text '' in a float64-declared column -- refusing to guess")
```

Run against the REAL bytes of both files, with the declared type printed beside it:

```
declared type of 'Median 30 Day Spread Percentage': float64

OK   2026-08-22  header matches declared: True  rows=2  dtype=str
    PFDE cell='0.2447' -> 0.2447
    PFOE cell='0.3401' -> 0.3401

FAIL 2026-08-29  header matches declared: True  rows=2  dtype=str
    PFDE cell=''       -> VendorDriftError: non-numeric text '' in a float64-declared column
    PFOE cell=''       -> VendorDriftError: non-numeric text '' in a float64-declared column
```

Note `header matches declared: True` in both -- this is **not** header drift, not a ragged row, not a
shell delivery, and not the conservation AC. It is one empty cell in one declared-numeric column.

Because the refusal is raised per fund inside the per-fund loop and before `write_partition`, a single
empty cell takes down the whole unit for **both** funds. Hence 4, not 2.

## 4. THE DENOMINATOR, AND A FALSIFICATION TEST THAT PASSED

Every `DailyNAV.csv` in bronze was fetched and scanned for empty cells in any of the **10**
float64-declared vendor columns:

```
deliveries scanned (denominator) : 74        (2026-07-15 .. 2026-09-26, the whole corpus)
deliveries with an EMPTY float64 cell : 2
   20260829  {'Median 30 Day Spread Percentage': 2}
   20260830  {'Median 30 Day Spread Percentage': 2}
```

Three things this closes:

1. **Exact correspondence.** The only 2 deliveries with an empty numeric cell are the only 2 dates
   missing from silver. 74 bronze deliveries, 72 silver partitions per fund, difference 2.
2. **The cause is not falsified.** Had any delivery carried an empty float cell and still converted, the
   account above would be wrong. None did.
3. **It is one column, not a class.** 9 of the 10 float64 columns have never been empty; only the median
   spread has, and only twice.

## 5. WHAT THIS MEANS FOR Z-S6 AND Z-S11 -- a refinement, and one correction

- **Z-S6** asked "which 2 dates, and vendor non-delivery or conversion failure". Answered: 2026-08-29 and
  2026-08-30; **neither label is quite right.**
- **Z-S11** concluded "a CONVERSION failure, not a vendor non-delivery -- both bronze units are present,
  on time and well-formed". Confirmed on the file-level facts, and **refined on the cause**: the file
  arrived, so it is not a non-delivery; the converter did precisely what it is written to do, so calling
  it a conversion *failure* misplaces the defect. It is **a vendor FIELD omission meeting a strict
  parse-or-raise contract**. The proximate trigger is upstream data; the amplifier is that one unparseable
  cell fails two funds' whole partitions.

Z-S11's own note also says "reading the converter's own refusal for those two units is the next act".
That act is section 3, and it was done by reproducing the refusal on the real bytes rather than by reading
a log.

## 6. THE ADJUDICABLE QUESTION -- not mine to decide, and stated as one question

**Should an EMPTY field in a float64-declared column be NULL, or is it drift?**

The converter's docstring is deliberate and argues the current behaviour: *"coercing it to null would be
judgment (fillna's evil twin), and Rule 17 forbids exactly that."* That reasoning is about **unparseable
TEXT**, e.g. `'n/a'` or `'--'`, where a null really would be a guess. An **absent** field is arguably a
different case: CSV has no other way to say "the vendor did not supply this", and `_numeric_or_raise`
already returns `None` for `None` and for NaN -- so null-for-absent is a distinction the function
partially makes already, just not for `''`.

Two candidate dispositions, with their costs, for `1.0.0_SA_CTO~O` / `3.0.0_SA_CVO`:

- **(a) Treat `''` as NULL** in `_numeric_or_raise` (one clause beside the existing `None`/NaN arm). The 4
  partitions then convert, with a null spread on those dates. Cost: it is a change to a RATIFIED Rule-17
  boundary shared by the mirror framework and its 4 vendored copies, so it needs the same never-widen
  path as Z-S3 -- and it slightly widens what lands silently.
- **(b) Keep the refusal** and treat these two dates as a permanent, named hole. Cost: the completeness
  guard reads FAIL forever on a cause nobody will fix, which is the state Z-S6 objected to in the first
  place.

**My recommendation is (a)**, narrowly: empty-string-to-null for a *declared-numeric* column only, and
only where the row is otherwise complete. But it edits a ratified contract, so it is a ruling, not a fix I
should take -- and the order said read first, no backfill.

**Either way a backfill is a SEPARATE act** and is not started: under (a) the two units re-convert once
the fix is live in whichever copy the sweep runs from; under (b) nothing is owed but a named hole.

## 7. WHAT I DID NOT DO

- **No backfill, no re-conversion, no forced run.** The order said read first; the cause is now known and
  the remedy is a ruling.
- **No code change.** Section 6 is a proposal, not a patch.
- **No S3 write of any kind.** Every read here was `s3 ls` / `s3 cp` to stdout or to the scratchpad.
- **The vendor was not contacted.** Whether filepoint should have supplied the spread on those two days is
  a real question and vendor egress needs Andrew's word; it is not needed to explain the gap.
- **The 4 vendored Lambda copies were not touched** -- unchanged from the Z-S3 handoff, still AE's.
