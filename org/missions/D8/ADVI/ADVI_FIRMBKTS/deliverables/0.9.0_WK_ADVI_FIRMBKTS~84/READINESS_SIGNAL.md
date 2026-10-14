# FB-m-1 readiness signal -- the data frontier from content (2026-10-14)

Machine record: `READINESS_SIGNAL.json` in this folder (`claim: measured`, ruling CTO msg 5552). The guard is `_gold_ready()` in `infra/aws/lambda/inf-portal-publisher/lambda_function.py`, called once at the top of `lambda_handler`.

## The three dated inputs

| input | key or prefix | date column | loader (base line) |
|---|---|---|---|
| client_perf | `gold/timeseries/client_performance.parquet` | `date` | `:178` (key `:62`) |
| holdings | newest key under `gold/canonical/` containing `holdings_` | `date` | `:192` (prefix `:61`; key rule `:92-103`) |
| canonical_nna | newest key under `gold/canonical/` containing `canonical_nna_` (the newest partition only) | `date` | `:186` (prefix `:60`; key rule `:106-114`) |

Each frontier date is the MAXIMUM of the date column, read from content with `_load_parquet(key, columns=['date'])`. The date column contents were not read here (no parquet body under the bounds), so each claim is `inferred` from the loader code.

Live object names at 13:2xZ: holdings newest `holdings_2026-10-14.parquet`; NNA newest `canonical_nna_2026-10-13.parquet`; `canonical_nna_2026-10-14.parquet` returns 404. Holdings and NNA therefore differ by name, so the rule predicts a HALT today (reason `frontier-split`). This is a prediction from names, not a measured halt; FB-m-2 tests it live.

## Excluded

Undated dimensions: `accounts_dim` (`:63`, `:200`), `account_team` (`:64`, `:206`), `household_dim` (`:66`, `:226`). `aum_snapshot` (`:219`) is loaded but no output of the handler consumes it, so it is excluded too.

## How the served date is read

The served date is the `data_as_of` field of `platinum/firm/snapshots/aua_by_architect.json`, `aua_by_state.json` and `aua_by_region.json`. The field is written by `_snapshot_response` (`:766`), fed by `date_str` (`:787`, the holdings maximum date, or `datetime.date.today()` at `:782` when holdings has no dated rows). One live copy (architect) reads `data_as_of` 2026-10-14. The served value is the minimum over the objects that exist. `aua_by_tax_status.json` is not read: it dates from 2026-06-30 and is no longer written.

## What the guard does on each arm

- **(i) all three at D, D after served**: publish. The advisor fan-out, the three snapshot puts and the CloudFront invalidation run as today.
- **(ii) one input behind (e.g. NNA at D-1)**: halt with `reason=frontier-split`. Zero S3 puts, zero Lambda invokes, zero CloudFront calls.
- **(iii) all at D, served = D (same-day re-fire)**: halt with `reason=not-after-served`. Zero writes.
- **(iv) no snapshot object exists**: publish once; the publish stamps `data_as_of`.

A read error on any input or on a served object that is not a missing key halts (`reason=read-error`). The halt prints one line, `READINESS HALT: client_perf=<d> holdings=<d> canonical_nna=<d> served=<d|absent> reason=<r>`. A ready run prints `READINESS OK: ...`.

Open items are in the surprise rows `ADVI_FIRMBKTS-D1-W84-S4` to `S7` (investigation file, this cell's coordinate).
