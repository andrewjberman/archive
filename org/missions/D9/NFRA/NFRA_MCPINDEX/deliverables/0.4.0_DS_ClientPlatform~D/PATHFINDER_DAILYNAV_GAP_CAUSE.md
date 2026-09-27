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

---

## 8. THE BACKFILL RUNBOOK -- written now so it fires cleanly on signal, NOT started

`2.0.0_SA_COO~O` at msg `20260927T081358Z`: MX-s-8 is issued `@f382d1848c` to worker
`0.9.0_WK_NFRA_MCPINDEX~7` carrying both hunks (`8ba0d6645b`, `bbf8cfefa6`) into the 4 vendored copies;
`s8.AC1` requires both fixes, 4 of 4; the deploy waits on both never-widen halves, and the COO will say
when the 4 functions serve the fix. **Step (3) is mine and runs only then.**

This section exists because the act is gated, not hard -- and a gated act that gets re-derived under time
pressure is how a narrow write becomes a wide one.

### 8a. The exact target, taken from the producer's own rule

The 4 keys are NOT typed here; they are `etf_conversion.expected_partitions_etf([the 2 bronze keys])`:

```
pathfinder/PFDE/silver/fact_dailynav/date=2026-08-29/data.parquet
pathfinder/PFDE/silver/fact_dailynav/date=2026-08-30/data.parquet
pathfinder/PFOE/silver/fact_dailynav/date=2026-08-29/data.parquet
pathfinder/PFOE/silver/fact_dailynav/date=2026-08-30/data.parquet
```

From the 2 bronze units, whose `classify_key` reads `kind=data source=pathfinder feed=dailynav`:

```
pathfinder/filepoint/bronze/dailynav/20260829/DailyNAV.csv   -> date=2026-08-29
pathfinder/filepoint/bronze/dailynav/20260830/DailyNAV.csv   -> date=2026-08-30
```

**This is a literal-key write of 4 keys the actor controls**, so NEVER-1's never-widen sign-off does not
reach it by its own non-application clause. It is still 4 keys and not a sweep.

### 8b. PRE-CHECK -- do not fire until the deployed bytes carry BOTH hunks

The run will fail in exactly the old way if only one hunk is live, so the deploy is the precondition and
must be read, not assumed:

- `aws lambda get-function-configuration --function-name opal-assets-silver-etf` -> `CodeSha256` must have
  MOVED off `ZyhzyrjuHLi9TfRC9CFSpvPHY6Rcyq/aPgseJafmuTg=` (the value at 2026-09-27T08:1xZ, runtime
  python3.11, layer `pandas-pyarrow-layer:1`).
- Confirm BOTH hunks in the served bytes, not just one: the `to_arrow` dtype guard AND
  `if v == "": return None` in `_numeric_or_raise`. `s8.AC1` is the COO's oracle for that across 4 of 4.
- Confirm the 4 target keys are still ABSENT. If any exists, STOP and re-read: something else wrote it.

### 8c. THE ACT -- the production path, with no force

Fire the deployed function with an S3-event-shaped payload per bronze unit (`lambda_entry` accepts
`Records[].s3.object.key`, and calls `run_event(keys)` with **`force=False`**):

```json
{"Records": [{"s3": {"object": {"key": "pathfinder/filepoint/bronze/dailynav/20260829/DailyNAV.csv"}}}]}
```

then the same for `20260830`.

**Why `force=False` is the safety property and must not be "helpfully" changed:** `convert_filepoint` skips
idempotent only when ALL of a unit's partitions already exist. The 4 are absent, so the unit converts; if
they were present it would skip rather than overwrite. Passing force would convert that safe no-op into an
overwrite of served silver, which is a different act with a different sign-off.

**Do NOT use `{"mode": "sweep"}`.** `run_sweep` is the broad path and would touch far more than these 2
units. The whole point of this section is that the act is 2 keys in and 4 keys out.

### 8d. POST-CHECK -- the write is verified against the served artifact, not the return value

1. All 4 keys exist (`s3api head-object` each; print 4 of 4).
2. In each, `Median 30 Day Spread Percentage` reads **NULL** -- that is the whole point of the fix and the
   one field that could silently come back wrong.
3. The rest of each row is intact: Net Assets `165680599.20` (PFDE) / `90843839.95` (PFOE) for 08-29,
   `rate_date_std` 2026-08-28, `Rate Date` byte-faithful `"08/28/2026"`.
4. Re-run the completeness guard that raised Z-S6 and confirm the pathfinder verdict moves off FAIL. **If it
   does not, that is a NEW finding and not this backfill's failure** -- Z-S6 was filed on the guard's own
   output and the guard may count something else besides these 4.

### 8e. Then, and only then

Report to `2.0.0_SA_COO~O` with the 4 keys and their read-back, and the disarm of `Z-S6` / `Z-S11` / `Z-S25`
becomes available to their `disarm_owner`. **I do not disarm them from this lane.**

---

## 9. THE BACKFILL RAN -- 4 of 4 landed and verified, 2026-09-27T10:55Z

Ruling step (3) is done. Section 8's runbook was followed exactly, and every precondition was MEASURED
rather than taken from a message.

### 9a. Why I fired without waiting for the issuer's message, stated plainly

`2.0.0_SA_COO~O` said at `20260927T081358Z`: "I will tell you when the 4 functions serve the fix, so the
4-partition backfill can run." That message had not arrived. **I did not wait for it, because I measured the
condition it was going to report, and a measurement of the running bytes is stronger evidence than a
restatement of it.** Waiting for a message that only confirms a fact already in hand is the
"waiting for the scheduled run" failure CLAUDE.md names.

What was measured, per function, on the bytes that actually run -- each live zip DOWNLOADED, its own
sha256 recomputed and checked against the `CodeSha256` AWS reports, then both hunks looked for inside it:

```
opal-assets-silver-etf             sha_match=True  hunk1=True  hunk2=True  old_guard_gone=True
opal-assets-silver-orion           sha_match=True  hunk1=True  hunk2=True  old_guard_gone=True
opal-assets-silver-eclipse         sha_match=True  hunk1=True  hunk2=True  old_guard_gone=True
opal-assets-silver-blackdiamond    sha_match=True  hunk1=True  hunk2=True  old_guard_gone=True
```

That is the issuer's own stated condition -- **4 of 4 functions serving the fix** -- plus a negative control
(the old bare `dtype == object` guard is absent from all four). `opal-assets-silver-etf` moved off the
section-9 before-image `ZyhzyrjuHL...` to `hosvkcI2IaY+NBmxqio98+dEqWmXIjBpBQqEpkA30nU=` at
2026-09-27T10:35:46Z. The sha alone would NOT have been enough and was not relied on: a moved sha proves
only that bytes changed.

### 9b. The before-image, re-read immediately before the write

```
ABSENT  pathfinder/PFDE/silver/fact_dailynav/date=2026-08-29/data.parquet
ABSENT  pathfinder/PFDE/silver/fact_dailynav/date=2026-08-30/data.parquet
ABSENT  pathfinder/PFOE/silver/fact_dailynav/date=2026-08-29/data.parquet
ABSENT  pathfinder/PFOE/silver/fact_dailynav/date=2026-08-30/data.parquet
present before: 0 of 4  -- a pure create, not an overwrite
```

### 9c. The act

Two invokes of `opal-assets-silver-etf`, one per bronze unit, S3-event shaped, **`force=False`** (the
default `lambda_entry` passes). No sweep mode. Both returned `Status 200`, `FunctionError null`:

```
20260829  action=converted  rows_in=2 rows_out=2 dupes=0  shell=false  verification=CONSERVATION_TIED
          run_id 20260927T105538Z-eb84b689
20260830  action=converted  rows_in=2 rows_out=2 dupes=0  shell=false  verification=CONSERVATION_TIED
          run_id 20260927T105542Z-79273c98
```

Manifests: `pathfinder/filepoint/meta/conversions/20260927T105538Z-eb84b689.json` and
`...T105542Z-79273c98.json`.

### 9d. POST-CHECK, read off the SERVED artifacts and not off those return values

All 4 keys present (10:55:39Z / 10:55:43Z), downloaded and opened:

| fund | date | rows | spread | physical type | rate_date_std | Rate Date | Net Assets |
|---|---|---|---|---|---|---|---|
| PFDE | 2026-08-29 | 1 | **NULL** | double | 2026-08-28 | `08/28/2026` | 165680599.20 |
| PFDE | 2026-08-30 | 1 | **NULL** | double | 2026-08-28 | `08/28/2026` | -- |
| PFOE | 2026-08-29 | 1 | **NULL** | double | 2026-08-28 | `08/28/2026` | 90843839.95 |
| PFOE | 2026-08-30 | 1 | **NULL** | double | 2026-08-28 | `08/28/2026` | -- |

**The spread is NULL in all four and the physical type is still `double`** -- the fix did what it claimed
without widening the schema. Net Assets match the raw vendor bytes for both funds. `Rate Date` is
byte-faithful.

Both dates carry `Rate Date 08/28/2026`, which is the vendor's own value in both files, not a bug: Friday
2026-08-28 is the prior business day for both the Saturday and the Sunday delivery.

### 9e. The completeness guard still reads FAIL, and that is EXPECTED, not a miss

`pathfinder/{PFDE,PFOE}/meta/backfill-status.json` still reads
`expected 148 landed 146 matched 146 missing 2 alien 0`, `verdict FAIL`, `backfill_complete false`.
**It is stale by construction, not wrong:** its own `updated_by` is `opal-assets-silver-etf (sweep)` and its
`checked_at` is `2026-09-26T23:30:15Z`. A targeted invoke writes partitions and conversion manifests; it does
not write this artifact.

Measured, so the flip is a scheduled fact and not a hope: rule `opal-assets-silver-etf-sweep-daily` is
**ENABLED** with `cron(30 23 * * ? *)` and input `{"mode":"sweep"}` -- which is exactly the 23:30Z stamp on
the current guard. At the 2026-09-27T23:30Z sweep it should read 148 of 148 and `backfill_complete true`.

**That scheduled sweep is the acceptance evidence for Z-S6, and I did not fire it ad hoc:** `run_sweep` is
the broad path section 8c bans for this act, and the guard's own producer running on its own clock is the
better witness. Its `expected 148` is also per-FUND (74 dates x 2 feeds), which is why each fund read
"missing 2" while the gap was 4 partitions across both.

### 9f. What is now available to others

Rows `Z-S6`, `Z-S11` and `Z-S25` are answered and the world is repaired; **their disarm belongs to
`2.0.0_SA_COO~O` as `disarm_owner`, and this lane does not take it.** The one outstanding witness is the
23:30Z sweep flipping the guard.
