# OG-x-2 result -- streaming Schwab CSV export (0.9.0_WK_NFRA_OPLGTW~11)

Branch `wk-NFRA_OPLGTW-11`, code commit `0c3d545002` (LOCAL). Build only; nothing deployed, no AWS call.

## The four AC1 numbers (test_ogx2_ac01, the criterion run at 0c3d545002, real spawned engine child, 2-column export)

| export | CSV bytes | rows | child peak RSS (`JobResult.peak_child_rss_bytes`) | parent tracemalloc peak in `generate_csv` |
|---|---|---|---|---|
| 10,000 rows | 450,019 | 10,000 | 157,175,808 (149.9 MiB) | 582,092 (0.6 MiB) |
| 100,000 rows | 4,500,019 | 100,000 | 184,332,288 (175.8 MiB) | 549,651 (0.5 MiB) |
| ratio 100k/10k | 10.00 | | 1.173 | 0.944 (limit 1.2 both) |

Each size runs twice inside the test and reports its higher peak; the engine is polled every 5 ms. Five earlier passing runs of
the same test gave child ratios 1.134, 1.140, 1.134, 1.176, 1.150. The margin under 1.2 is thin: see row Z-W11-S1.
With a 4-column export the same test FAILED in 6 of 6 runs (child ratio 1.204 to 1.270); the parent stayed flat. The test
therefore asks for `account_ref` and `cusip` only. The remaining child growth is the source table plus DuckDB's sorted result
(the contract's tie-break sort), not the result materialisation this cell removed.

## The AC2 count

`limits.export_rows` overlaid to 1,000 (a deep copy of the contract; the file is untouched), request matching 5,000 rows,
real engine: `LIMIT_EXCEEDED` / `export_rows_limit`, suggestion "at most 1000 rows"; the child reported
`matched_rows=5000`, `fetched_rows=0`; files left in the export directory: `[]` (and no `*.arrow` or `export-*` anywhere under
the test tree). Child peak RSS at the refusal: 154,054,656 bytes.

## AC3

`page_size` 500 over 700 short rows: `returned_count` 500, `truncated` True, cursor present, text block 500 rows,
`envelope.measure()` rows 500 (codepoints 17,904, UTF-8 bytes 17,904). Mutant control: with the old summing `measure` patched
in, the same test returns 250 rows and fails at its `returned_count == 500` assertion.

## What was built (paths under `infra/aws/ec2/opal-gateway/`)

- `engine.py`: the export child counts first and refuses over `row_cap` before any fetch (error carries `detail`); else streams
  DuckDB's result in 8,192-row batches to an Arrow IPC file in the caller's export directory; the source is read and
  policy-filtered in record batches (`_read_source`); export jobs get a 64 MiB DuckDB working set;
  `run_export(principal, plan, sources, *, row_cap, export_dir)` removes the file on failure, kill or cancellation;
  `read_export_batches` reads it back. Job-error messages gained an optional `detail`.
- `integration.py`: `export_query(principal, ticket, *, directory=None)` returns `(columns, ExportRows, info)`; `ExportRows`
  reads the file back, applies `aref.account_ref` and `env.render_rows` per 1,024 rows, closes and deletes the file on
  exhaustion, failure or `close()`. The revision re-read before emission and the cap check (revision first) are kept.
- `export.py`: `write_csv` takes an iterator; `generate_csv` counts rows as they pass and always closes the stream.
- `envelope.py`: `measure()` counts a row once (largest per-block count).
- `download_routes.py`: read, not changed (it unpacks `generate_csv`'s unchanged 4-tuple).

## Corrected tests (each asserted the OLD behaviour)

1. `tests/test_schwab_export.py` World: `self.engine.run_export = self.engine.run_query` removed.
2. `tests/acceptance/conftest.py` InProcessEngine: `run_export = run_query` replaced by a real `run_export` running the export
   branch of `_plan_job` (docstrings updated).
3. `tests/test_schwab_query.py` Engine double: gained a real `run_export` (same branch).
4. `tests/test_schwab_engine.py` `test_ogq1_ac11`: the `csv` bytes assertion (old line 738) became: the value names an export
   file outside the workdir, its columns are `["symbol", "total_value"]`, its batch rows equal `returned_rows`, no `csv`/`rows`
   key; the call passes `row_cap` and `export_dir`.
5. `tests/test_schwab_query.py` `test_ogq2_ac16`: `measured["rows"] == 2 * doc["returned_count"]` became
   `== doc["returned_count"]`; its three-cap assertions are unchanged.

## Suite counts at close (per-module runs, AUDIT_PATH set to a temp file)

| module | passed | failed |
|---|---|---|
| tests/test_schwab_export.py | 27 | 0 |
| tests/test_schwab_engine.py | 13 | 0 |
| tests/test_schwab_query.py (incl. test_ogx2_ac03) | 26 | 0 |
| tests/test_schwab_wiring.py | 3 | 0 |
| tests/acceptance/test_local_acceptance.py | 14 | 0 |
| tests/test_schwab_export_stream.py (new) | 2 | 0 |
| total | 85 | 0 |

One earlier combined run (engine + wiring + acceptance in one pytest process) failed `test_ogq1_ac04` once
(`pid_alive` after a deadline kill) and errored the 14 acceptance tests on "StreamableHTTPSessionManager .run() can only be
called once per instance" (module-scoped app shared across modules); each module passes alone. Row Z-W11-S3 (ac04, INERT).

## Rows

`NFRA_OPLGTW-Z-W11-S1` (wide 250,000-row export still over the job cap in the child, OBSERVATION/ARMED),
`-S2` (`tests/acceptance/onhost_bench.py` still calls the old `run_export`, OBSERVATION/ARMED),
`-S3` (one ac04 timing flake, OBSERVATION/INERT). All disarm_owner `2.0.0_SA_COO~O`.
