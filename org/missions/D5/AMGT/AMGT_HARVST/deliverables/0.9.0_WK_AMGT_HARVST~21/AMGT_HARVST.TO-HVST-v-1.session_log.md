# HVST-v-1 -- session log, `0.9.0_WK_AMGT_HARVST~21`

**Worktree:** `C:/tmp/wk-hvst-r1`, branch `wk-harvst-7-21`, base `d0171ffe4f`.
**Task order:** `org/missions/D5/AMGT/AMGT_HARVST/task-orders/AMGT_HARVST.TO-HVST-v-1.empty-mapping-cannot-reach-silver.md`
**Risk class:** LOCAL. **No network, no vendor call, no S3 read or write, no deploy.** Every parquet
write below goes to an in-memory `io.BytesIO`, never to a bucket. The held vendor payloads under the
main tree's `.runtime/` were READ ONLY and were never copied into the repo.

## THE CHANGE

`lib/opal_data_harvest/silver_from_bronze.py` -- new module-private `_null_empty_mappings(value)`
and one line in `listing_hit_rows`:

    rows.append({key: _null_empty_mappings(value) for key, value in row.items()})

An EMPTY MAPPING becomes `None`; every other value is returned unchanged. The predicate is
`isinstance(value, dict) and not value`, so NO PUBLISHER AND NO FIELD NAME appears in the fix --
`themes` and `sa` are named only in comments describing the measured firing. Recursion descends into
dicts and lists so an empty mapping NESTED inside a populated one is nulled too (parquet refuses a
`struct<>` child just as hard), while every populated container keeps its type, key order and values.
The coercion is applied PER FIELD VALUE, not to the row container, so a row is never itself nulled
and insertion order is preserved.

`lib/research/harvest/store.py` WAS NOT TOUCHED (standing clause 3). Its `silver_append` at `:348` was
read only, to lift the exact write path (`pa.Table.from_pylist` then `pq.write_table`) into the AC
scripts so the arms exercise the real chokepoint without a client.

## AC1 -- the defect reproduced, then gone, on the real held sa payload

Invocation: `cd "$(git rev-parse --show-toplevel)" && python .scratch/r1/ac1.py` -- rc=0.
The BEFORE arm RUNS `git show HEAD:lib/opal_data_harvest/silver_from_bronze.py`, exec'd as a member
of the `lib.opal_data_harvest` package so its relative imports resolve; the arm-provenance lines are
the control that "before" is not silently the after-bytes.

```
AC1 -- HVST-v-1: empty mapping in a listing row, BEFORE and AFTER, one held sa payload
held payload: C:\Users\Opal Bloomberg\Desktop\ajb_workspace\.runtime\opal-data-harvest\harvest_listing\sa_p1_990943eddbd5a172.json (137260 bytes)
pyarrow 24.0.0 | write path = pa.Table.from_pylist + pq.write_table (store.py:348 verbatim, in-memory buffer, NO S3)

ARM PROVENANCE (the control that the BEFORE arm is really pre-change bytes)
  BEFORE source = <git show HEAD:lib/opal_data_harvest/silver_from_bronze.py>  carries '_null_empty_mappings': False
  AFTER  source = lib/opal_data_harvest/silver_from_bronze.py (worktree)  carries '_null_empty_mappings': True

BEFORE (HEAD bytes): rows built = 20 of 20 expected; empty-mapping field values = 20
  themes on row[0] = {}   (type dict)
  WRITE RAISED: ArrowNotImplementedError: Cannot write struct type 'themes' with no child field to Parquet. Consider adding a dummy child field.
  raised at: pyarrow.lib.ArrowNotImplementedError: Cannot write struct type 'themes' with no child field to Parquet. Consider adding a dummy child field.

AFTER (worktree bytes): rows built = 20 of 20 expected; empty-mapping field values = 0
  themes on row[0] = None   (type NoneType)
  WRITE: SUCCEEDED -- parquet row count written = 20 of 20 expected
  arrow type of themes AFTER = null
  columns = 25

  BEFORE arm ran pre-change bytes (no fix marker)      PASS
  AFTER arm ran post-change bytes (fix marker present) PASS
  BEFORE write raised ArrowNotImplementedError         PASS
  BEFORE error names a struct with no child field      PASS
  AFTER write succeeded                                PASS
  AFTER parquet row count == 20                        PASS
  AFTER rows carry no empty mapping                    PASS
  BEFORE rows carried 20 empty mappings                PASS

AC1 denominator: 8 of 8 checks PASS
AC1: PASS -- defect reproduced on pre-change bytes and gone on post-change bytes
```

## AC2 -- the positive control: wsj unmoved, a populated mapping still a struct

Invocation: `cd "$(git rev-parse --show-toplevel)" && python .scratch/r1/ac2.py` -- rc=0.

```
AC2 -- HVST-v-1 POSITIVE CONTROL: wsj unchanged, populated mapping still a struct
pyarrow 24.0.0 | BEFORE = git show HEAD:lib/opal_data_harvest/silver_from_bronze.py (carries fix: False) | AFTER = worktree (carries fix: True)

==============================================================================
ARM A -- wsj HELD listing payloads: byte-identical rows AND identical arrow schema
==============================================================================

-- wsj_p1_45058f937f5eff24.html (598358 bytes held)  rows BEFORE = 20  rows AFTER = 20
   canonical row-set sha256 BEFORE = ea63967cc060054e302c78d84ee9875950139803df673ea39b1b13db0588229b (27195 bytes)
   canonical row-set sha256 AFTER  = ea63967cc060054e302c78d84ee9875950139803df673ea39b1b13db0588229b (27195 bytes)
   ROW SET VERDICT: BYTE-IDENTICAL
   direct equality (before_rows == after_rows): True
   arrow schema BEFORE (25 fields):
      articleUrl: string
      commerceProduct: string
      contentTag: string
      bylineData: list<item: struct<text: string, ref: string, phrase_type: string, id: string, type: string, name: string>>
      flashline: string
      headline: string
      imageAlt: string
      printHeadline: string
      printPublicationDate: string
      seoPathValue: string
      summary: string
      timestamp: string
      article_id: null
      url: string
      search_rank: int64
      search_page: int64
      search_query: string
      query_sha256: string
      source: string
      publisher: string
      fetch_date_utc: date32[day]
      bronze_key: string
      fetched_at: timestamp[us, tz=UTC]
      retrieval_mode: string
      run_stamp: string
   arrow schema AFTER  (25 fields):
      articleUrl: string
      commerceProduct: string
      contentTag: string
      bylineData: list<item: struct<text: string, ref: string, phrase_type: string, id: string, type: string, name: string>>
      flashline: string
      headline: string
      imageAlt: string
      printHeadline: string
      printPublicationDate: string
      seoPathValue: string
      summary: string
      timestamp: string
      article_id: null
      url: string
      search_rank: int64
      search_page: int64
      search_query: string
      query_sha256: string
      source: string
      publisher: string
      fetch_date_utc: date32[day]
      bronze_key: string
      fetched_at: timestamp[us, tz=UTC]
      retrieval_mode: string
      run_stamp: string
   SCHEMA VERDICT: IDENTICAL
   parquet row count BEFORE = 20  AFTER = 20
   table data equality: True

-- wsj_p2_bfec5a47fe3ed50b.html (529261 bytes held)  rows BEFORE = 0  rows AFTER = 0
   canonical row-set sha256 BEFORE = 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945 (2 bytes)
   canonical row-set sha256 AFTER  = 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945 (2 bytes)
   ROW SET VERDICT: BYTE-IDENTICAL
   direct equality (before_rows == after_rows): True
   0 rows on this held page -- no schema to compare (searchResults is an empty list in the captured bytes); row-set identity still measured above

ARM A row denominator: 20 wsj listing rows compared across 2 held pages

==============================================================================
ARM B -- a POPULATED mapping still writes AS A STRUCT (and a nested empty one is nulled)
==============================================================================
rows built = 1 of 1 expected
themes value  = {'berkshire': 'primary'}
nested value  = {'kept': {'inner': 7}, 'dropped': None}
links value   = {'self': '/news/901-populated'}
arrow type of themes = struct<berkshire: string>
arrow type of nested = struct<kept: struct<inner: int64>, dropped: null>
arrow type of links  = struct<self: string>
WRITE: SUCCEEDED -- parquet bytes = 6701, rows = 1
read back from the parquet bytes: themes = {'berkshire': 'primary'}
read back from the parquet bytes: nested = {'kept': {'inner': 7}, 'dropped': None}

  wsj_p1_45058f937f5eff24.html arrow schema identical        PASS
  wsj_p1_45058f937f5eff24.html arrow table data identical    PASS
  wsj_p1_45058f937f5eff24.html parquet row count unchanged   PASS
  wsj_p1_45058f937f5eff24.html row set byte-identical        PASS
  wsj_p1_45058f937f5eff24.html row count unchanged           PASS
  wsj_p2_bfec5a47fe3ed50b.html row set byte-identical        PASS
  wsj_p2_bfec5a47fe3ed50b.html row count unchanged           PASS
  populated themes is a struct with its child                PASS
  populated themes value preserved                           PASS
  populated parent stays a struct with an empty child nulled PASS
  populated links unchanged                                  PASS
  populated-mapping row writes to parquet                    PASS
  populated themes survives the parquet round trip           PASS

AC2 denominator: 13 of 13 checks PASS (wsj rows compared: 20)
AC2: PASS -- wsj row set and schema unmoved; a populated mapping is still a struct
```

## AC3 -- the suite as a bound

Invocation: `cd "$(git rev-parse --show-toplevel)" && python -m pytest lib/opal_data_harvest/ -q 2>&1 | tail -15`
(literal, as cut; ANSI colour stripped here only).

PRE-CHANGE run of the identical command, before any edit in this worktree:
`3 failed, 160 passed, 4 subtests passed in 5.73s`, pytest rc=1 read via `PIPESTATUS` (the pipeline's
own rc is `tail`'s and is always 0).

POST-CHANGE:

```
    dj().check()
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

    def check(self):
>       value = self.session.get(self.base + "/client?legacy=false",
                ^^^^^^^^^^^^^^^^
                                 headers={"Referer": self.base + "/", "Accept": "application/json"}).json()
E       AttributeError: 'NoneType' object has no attribute 'get'

lib\opal_data_harvest\publishers.py:672: AttributeError
=========================== short test summary info ===========================
FAILED lib/opal_data_harvest/test_verification.py::Tests::test_disabled_barrons_contract_defers_before_opening_a_browser - FileExistsError: [WinError 183] Cannot create a file when that file already...
SUBFAILED(failures=1) lib/opal_data_harvest/test_worker.py::Tests::test_single_broken_dow_jones_article_is_skipped_but_repeated_server_failure_stops - AttributeError: 'NoneType' object has no attribute 'get'
SUBFAILED(failures=2) lib/opal_data_harvest/test_worker.py::Tests::test_single_broken_dow_jones_article_is_skipped_but_repeated_server_failure_stops - AttributeError: 'NoneType' object has no attribute 'get'
3 failed, 161 passed, 4 subtests passed in 5.35s
```

`160 -> 161 passed`, `3 -> 3 failed`: +1 (this cell's new test), ZERO REGRESSIONS, same three
pre-existing failing nodeids.

THE POPULATION IS NOT THE SUMMARY LINE'S ARITHMETIC. `python -m pytest lib/opal_data_harvest/ -q
--collect-only | tail -3` prints `162 tests collected`, so `3 failed, 161 passed` is 161 passed +
ONE failed test (`test_verification`) + TWO `SUBFAILED` entries, which are subtest failures of a
test that passes at test level (`test_worker`) and are therefore already inside the 161. Adding the
summary's two numbers overstates the population by 2 -- the first version of the proof instance did
exactly that (164) and was corrected against the `--collect-only` read. The pass denominator is
**161 of 162 collected**, against **160 of 161** pre-change.

The +1 is MEASURED on both ends, not inferred: `git show
HEAD~1:lib/opal_data_harvest/test_silver_from_bronze.py | grep -c '^def test'` = 16 against 17 in
the worktree.

The naming clause of AC3 is NOT producible by this invocation -- `pytest -q` prints a nodeid only for
a test that FAILED. Measured: 0 grep hits for the new test's name in the tailed output AND in the
full untailed `-q` stream. Row `AMGT_HARVST-Z-W21-S1` carries it. The auxiliary run that DOES name it:

```
============================= test session starts =============================
platform win32 -- Python 3.11.9, pytest-9.1.1, pluggy-1.6.0 -- C:\Users\Opal Bloomberg\AppData\Local\Programs\Python\Python311\python.exe
rootdir: C:\tmp\wk-hvst-r1
configfile: pytest.ini
plugins: anyio-4.14.1
collecting ... collected 17 items / 16 deselected / 1 selected

lib/opal_data_harvest/test_silver_from_bronze.py::test_empty_mapping_in_a_listing_row_is_nulled_and_writes_for_every_publisher PASSED [100%]

====================== 1 passed, 16 deselected in 0.49s =======================
```

## CONTROLS

MUTANT (`python .scratch/r1/mutant.py`, rc=0) -- `_null_empty_mappings` replaced by identity in the
live module, the new suite test re-run, then reverted:

```
MUTANT CONTROL -- test: test_empty_mapping_in_a_listing_row_is_nulled_and_writes_for_every_publisher
mutation applied: _null_empty_mappings -> identity (the fix removed, nothing else touched)
MUTANT RESULT: FIRED -- AssertionError: sa: empty mapping 'themes' was not nulled: {}
  last frame: File "C:\tmp\wk-hvst-r1\lib\opal_data_harvest\test_silver_from_bronze.py", line 656, in test_empty_mapping_in_a_listing_row_is_nulled_and_writes_for_every_publisher |     assert rows[0][empty_field] is None, \ |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
mutation reverted
empty_mapping_nulled_and_written 4 of 4 publishers, 5 rows written to parquet
POST-REVERT: PASSED (the mutation, not the test, was the difference)
mutant denominator: 1 mutation, 1 test, expected FIRED then PASSED
VERDICT: FIRED-AS-EXPECTED
```

DETERMINISM -- AC1 and AC2 each run twice on the same inputs, outputs compared with `cmp` and
`sha256sum`: both IDENTICAL. `ac1` 9be5d3d874b171f93f68a6d7dda46aed24f7fc884fdbf8c2175eca1008ef9bda,
`ac2` 96cddbae2ac3926265c4acc40e28a88b8e76030dfa7578284abc8baff12e1dea (both runs, both files).

## ROWS FILED

- `AMGT_HARVST-Z-W21-S1` OBSERVATION / ARMED (disarm `2.0.0_SA_COO~Y`) -- AC3's literal `-q`
  invocation cannot name a passing test.
- `AMGT_HARVST-Z-W21-S2` OBSERVATION / ARMED (disarm `2.0.0_SA_COO~Y`) -- the graded suite is
  already red at HEAD (3 failed / 160 passed) and one failure changed its CAUSE between two runs.
- `AMGT_HARVST-Z-W21-S3` OBSERVATION / INERT -- the second held wsj page yields ZERO listing rows
  (`searchResults` is an empty list in the captured bytes), so the wsj control is 20 rows from one
  page, not 40 from two.
