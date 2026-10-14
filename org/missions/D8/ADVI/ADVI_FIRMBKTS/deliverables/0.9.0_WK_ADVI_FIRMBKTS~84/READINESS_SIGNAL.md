# FB-m-1 readiness signal -- the data frontier from content (2026-10-14)

Machine record: `READINESS_SIGNAL.json` in this folder (`claim: measured`; ruling CTO msg 5552, amended by CTO msg 5571). The guard is `_gold_ready()` in `infra/aws/lambda/inf-portal-publisher/lambda_function.py` (helpers `_latest_key`, `_date_max`, `_dated_frontier`), called once at the top of `lambda_handler`, before the advisor fan-out.

## The dated inputs

| input | key or prefix | date column | loader (base line) |
|---|---|---|---|
| client_perf | `gold/timeseries/client_performance.parquet` | `date` | `:178` (key `:62`) |
| holdings | newest key under `gold/canonical/` containing `holdings_` | `date` | `:192` (prefix `:61`; key rule `:92-103`) |
| canonical_nna | newest key under `gold/canonical/` containing `canonical_nna_` (newest partition only) | `date` | `:186` (prefix `:60`; key rule `:106-114`) |

Each frontier date is the MAXIMUM of the `date` column, read from content with `_load_parquet(key, columns=['date'])`. No parquet body was read (bounds), so each claim is `inferred` from the loader code.

## Excluded

Undated dimensions: `accounts_dim` (`:63`, `:200`), `account_team` (`:64`, `:206`), `household_dim` (`:66`, `:226`). `aum_snapshot` (`:219`) is loaded but no handler output consumes it, so it is excluded too.

## How the served date is read

The served date is the `data_as_of` field of `platinum/firm/snapshots/aua_by_architect.json`, `aua_by_state.json` and `aua_by_region.json`, the three keys the publisher writes. The field is written by `_snapshot_response` (`:766`) from `date_str` (`:787`). The served value is the minimum over the objects that exist. A missing object is absent, not a halt. `aua_by_tax_status.json` is not read: its last write is 2026-06-30 and the publisher no longer writes it. The live architect copy reads `data_as_of` 2026-10-14 (written 12:53:58Z).

## The NNA tolerance and why

The rule is: holdings and client_perf read the same date D, and the newest canonical_nna partition N satisfies D minus 4 calendar days <= N <= D. Live listing of `gold/canonical/canonical_nna_2026-10` (read 13:42Z): partitions for 10-01, 02, 05, 06, 07, 08, 09 and 13. There is none for 10-03/04 (weekend), 10-10/11 (weekend) or 10-12 (Columbus Day). Holdings are daily (`holdings_2026-10-01` to `2026-10-14`, weekends included). So NNA lags a normal day by one business day, and across a Monday holiday by up to four calendar days (Friday 10-09 against Tuesday 10-13). Four days is the bound the CTO ruled.

## What the guard does on each arm

- **(i) holdings and client_perf at D, D after served, NNA one day behind D**: publish. The advisor fan-out, the three snapshot puts and the CloudFront invalidation run as today.
- **(ii) holdings or client_perf one day behind the other (split)**: halt, `reason=frontier-split`. Zero S3 puts, zero Lambda invokes, zero CloudFront calls.
- **(iii) holdings and client_perf at D, D equal to served (same-day re-fire)**: halt, `reason=not-after-served`. Zero writes.
- **(iv) no snapshot object exists**: publish once; the publish stamps `data_as_of`.
- **(v) NNA five calendar days behind D**: halt, `reason=nna-out-of-window`. Zero writes.

A read error on any input, or on a served object that is not a missing key, halts with `reason=read-error`. The halt prints exactly one line, `READINESS HALT: client_perf=<d> holdings=<d> canonical_nna=<d> served=<d|absent> reason=<r>`, and nothing else from the guard. A ready run prints `READINESS OK: ...`.

## Verification

Six unit tests with faked clients and loaders (`infra/aws/lambda/inf-portal-publisher/tests/test_readiness_halt.py`): six passed. The guard is purely additive against base blob 371eb01b42e5c1e4f6ce1c8ddac20071c0636762 (`GUARDDIFF: OK inserted=105 changed=0`). These prove the logic and zero-write discipline only; the frontier against the live bucket is FB-m-2's read.

Open items are in surprise rows `ADVI_FIRMBKTS-D1-W84-S4` to `S9` (investigation file, this cell's coordinate).
