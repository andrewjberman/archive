# ANNOUNCE -- OG-x-4 (R-4 remedy: export memory flat at full width), PHASE A ONLY

Builder: 0.9.0_WK_NFRA_OPLGTW~11 (issuer 2.0.0_SA_COO~O). Order:
org/missions/D9/NFRA/NFRA_OPLGTW/task-orders/NFRA_OPLGTW.TO-OG-x-4.export-flat-at-width.md (issued at 369739a276).

STATE: built and proved LOCALLY. No AWS write, no host contact, no ledger, nothing uploaded. Waiting for PHASE B GO.
Code commits on wk-NFRA_OPLGTW-11 (LOCAL): `d1ba79742c` (the build) and one follow-up (aggregate-export ceiling), listed in the report.

## The hypotheses, measured BEFORE any change (local, python 3.11, pyarrow 18.1.0, duckdb 1.2.2; 11 columns = dim_position; 10 fixture files x 25,000 rows, 200 accounts; `_plan_job` run in a fresh process, RSS polled every 3 ms, MiB)

| rows | old engine as shipped (64 MiB DuckDB, LIMIT cap+1) | old engine, LIMIT removed | new engine (16 MiB DuckDB, no LIMIT, DuckDB scans the files) |
|---|---|---|---|
| 25,000 | 172 | 174 | 160 |
| 125,000 | 220 | 235 | 166 |
| 250,000 | OOM (DuckDB), phase peak 293 | 262 (completes) | 166 |

The old-engine column reproduces OG-r-3's host figures (172 / 225 / >272 MB) to within a few MiB.

- **H1 (input read whole, then registered as `src`): CONFIRMED, but not the whole story.** The resident input alone adds
  about 57 MiB at 250,000 rows (RSS after the read: 147 MiB with no resident input vs 204 MiB); `_read_source`'s 33.5 MiB of
  Arrow tables cost 92 MiB of RSS (read buffers are not released). DuckDB's `memory_limit` does not bound a registered
  Arrow table, as the issuer read it.
- **H2 (a second copy per source in `_read_source`): REFUTED.** `pa.concat_tables` of the 10 per-source tables is zero-copy:
  RSS 186 MiB after the list of tables and 186 MiB after the concatenation, 10 chunks, 250,000 rows.
- **H3 (the maximal query): CONFIRMED as the same input residency; the page result is not the cost.** The maximal query
  (12 objects x 45,000 rows x 215-char Unicode text, page limit 500) in a spawned child: old engine 271,347,712 bytes
  (101.1 percent of the cap, LIMIT_EXCEEDED); new engine 167,575,552 bytes (62.4 percent of the cap), completed, 2.3 s.
  `fetch_arrow_table()` and `to_pylist()` are over 500 rows and were never the peak.
- **H4 (NEW, not in the order): the export statement's `LIMIT cap+1` is a non-spillable top-N.** `integration.export_query` builds the
  plan with `limit = cap + 1`; over `ORDER BY` DuckDB plans a top-N whose heap holds up to 250,001 rows in memory. It is
  what made DuckDB run out of memory at 250,000 rows x 11 columns (old engine as shipped) and it also made the
  earlier 16 MiB working set impossible (OOM at 25,000 rows). Removing it alone turns the OOM into a 262 MiB completion.
- The parent side (`read_export_batches`) is not the child's peak, as the order said; the parent's tracemalloc peak is
  1.8 MiB at both 10,000 and 100,000 rows.

## What was built (paths under `infra/aws/ec2/opal-gateway/`)
- `app/integrations/schwab/engine.py`:
  - `_plan_job` reads only Parquet METADATA (`_source_types`: missing column -> `field_missing_in_source`, differing types ->
    `source_schema_mismatch`, no sources -> `no_data_sources`, unconvertible policy values -> `policy_value_type`), and DuckDB
    itself scans the job's own objects: `open_duckdb(..., sources=...)` sets `allowed_paths` = the source list and
    `allowed_directories` = the spill dir, THEN `enable_external_access = false`, builds `src` as a view (referenced
    columns renamed c0..; the account policy is a semi-join `IN (SELECT v FROM policy_i)` inside the view, so it is applied
    before any generated operator sees a row), then `SET lock_configuration = true`. `DUCKDB_LOCKDOWN` reads back unchanged.
  - An export's statement no longer carries the cap as a LIMIT (`dataclasses.replace(plan, limit=None)`); the count-before-fetch
    refusal (`matched > row_cap`, `fetched_rows = 0`) is untouched and guarantees rows <= cap; the output stays streamed.
  - Export DuckDB working set: 16 MiB for rows-mode (the sort spills to the job dir), 64 MiB for aggregate-mode exports
    (measured: 250,000 groups OOM at 16 and 32 MiB, complete at 64). `_read_source` and `SOURCE_BATCH_ROWS` are removed.
- `tests/test_schwab_export_stream.py`: `test_ogx4_ac03`. `tests/test_schwab_engine.py`: `test_ogx4_source_scan_scope`
  (`src` scans only the listed object; policy keeps 4 of 5 rows; another parquet, csv, COPY, unlock and widening
  `allowed_paths` are all refused; the lockdown settings read back). `tests/acceptance/onhost_bench.py`: the export arm now
  RECORDS the 25,000 / 125,000 / 250,000-row cases at 11 columns (labels `export:tenth|half|full (<N> rows x 11 columns)` in
  `ac2.jobs`) with a `flatness_vs_25k_peak` block (ratio and within-10-percent per case); the halving probes are gone.
- Diff stat (`git diff --stat 369739a276 HEAD`, code only): engine.py 153+/-, onhost_bench.py 47+/-, test_schwab_engine.py +44,
  test_schwab_export_stream.py +53 (4 files, 217 insertions, 80 deletions at `d1ba79742c`).

## OGX4-AC3 (the criterion as written, `xf.AC3.sh`, at HEAD `d1ba79742c`)
```
OGX4-AC3: 11 columns; 10,000-row export: csv 1159136 bytes, 10000 rows; child peak RSS 158056448 bytes (150.7 MiB); parent tracemalloc peak 1907041 bytes (1.8 MiB)
OGX4-AC3: 11 columns; 100,000-row export: csv 11678030 bytes, 100000 rows; child peak RSS 172617728 bytes (164.6 MiB); parent tracemalloc peak 1842636 bytes (1.8 MiB)
OGX4-AC3: ratios 100k/10k at 11 columns -- child 1.092, parent 0.966 (limit 1.2); csv size ratio 10.07
pytest rc=0; named tests passed 1 of 1
RESULT: PASS
```
Direct runs of the test: child ratios 1.108 (69.1 s wall alone) and 1.092 (through the check). **Timing risk:** the check
bounds the test at `timeout 110`; OG-x-3 measured the 2-column run at 86.8 s under load. Eleven columns fit here (69 s
alone; the whole three-test module took 101 s), but a slower or busier box could exceed 110 s.

## Local full-scale bench at the new code (Windows, not the host; `onhost_bench.py --scale full`, 37 s)
| case | outcome | peak child RSS | ratio vs 25k |
|---|---|---|---|
| export tenth, 25,000 x 11 | ok | 173,907,968 | 1.000 |
| export half, 125,000 x 11 | ok | 179,417,088 | 1.032 |
| export full, 250,000 x 11 | ok, csv 37,488,002 B, 13.3 s total (engine job 6.3 s), files gone | 180,879,360 | 1.040 |
| maximal query | ok | 167,550,976 (62.4 percent of the cap) | |
| concurrent pair | ok | 161,660,928 / 158,818,304 | |
Verdict on this box: SUFFICIENT. The host (t4g.small, Linux ARM) is the graded plane; PHASE B measures it.

## Suite counts on the built tree (per module, AUDIT_PATH temp file)
test_schwab_engine 14 passed (was 13; +test_ogx4_source_scan_scope), test_schwab_semantics 14, test_schwab_query 26,
test_schwab_export 27, test_schwab_export_stream 3 (+test_ogx4_ac03), test_schwab_wiring 3, acceptance/test_local_acceptance
+ test_onhost_bench_grader 15: **102 passed, 0 failed.** (engine, export, semantics, query re-run after the last tweak;
stream, wiring and acceptance ran on the tree one line earlier, with rows-mode behaviour identical.) `GW/audit.jsonl` was never dirtied.

## Risks for PHASE B, named now
1. **Wall time of a 250,000-row export.** The engine job took 6.3 s locally but `generate_csv` took 13.3 s in total
   (the parent renders and writes 250,000 rows on the event loop, about 7 s). OG-r-3 measured 8.1 s at 125,000 rows on the
   host; 250,000 rows could read 15 to 25 s against the 30 s bar. The spill is 16 MiB in `/tmp`, which is tmpfs on the host.
2. **DuckDB 16 MiB floor.** Text-heavy rows-mode exports complete within the contract byte cap (144,000 rows x 9 columns
   x 215-char text = about 50 MiB of CSV: ok, 169 MiB peak), and refuse `LIMIT_EXCEEDED/memory` beyond that (192,000 rows,
   which would exceed the 50 MiB byte cap anyway). Aggregate exports keep 64 MiB.
3. **Row-group size.** DuckDB's scan unit is the Parquet row group; a source object written as ONE huge row group costs
   more scan memory than the many-row-group files a producer usually writes (my test fixtures are single-row-group).
4. The policy column is now read by DuckDB (in the view), not by PyArrow before DuckDB; the generated SQL still cannot name it.

## Not done, by design
No release tree, no census, no ledger, no upload, no host run: those are PHASE B (bound 4), on your GO.
