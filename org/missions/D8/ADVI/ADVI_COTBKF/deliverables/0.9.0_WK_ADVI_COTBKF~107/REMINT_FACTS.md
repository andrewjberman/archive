# REMINT_FACTS -- ADVI_COTBKF.TO-CB-bq-2 (round 69), 0.9.0_WK_ADVI_COTBKF~107

Read-only measurement. Nothing was applied, served or written remotely. Counts, dates, columns, addresses, ETags and version ids only.
The record is `REMINT_FACTS.json` beside this file (92 `writes`, 2 `day_files`, 9 `readers`).

Pin: as_of 2026-10-09T11:52:52Z, split-store sha256 `4aca4f1fa311712424df5daf91b68048ff362a88874033e53b31c8b706a362c7`.

## The finding the sign-off needs first

**43 day files change under `method_r29`, not 2.** The two named dates (2014-12-03, 2020-11-13) move `external_flow` and
`total_return_daily`, one row each. 41 more dates hold a blank (UNPRICED) withholding account-day (42 account-days; 2024-12-02 holds two)
whose `daily_returns.flow` moves under `method_r29`; the adapter copies `flow` into `external_flow` on every non-exception row
(`commonwealth_account_return_daily.py` line 546), so those day files change one cell too. The round-68 packet counted the return column only.
Control: the replicated column mapping reproduces all 1,691,729 served day-file rows with 0 differing (applied to the served silver and to
the `method_r28` build), and differs on 44 rows over 43 dates for `method_r29`. Rows ADVI_COTBKF-D2-W107-S1 and -S2 carry this.

## Chain of served writes

- Silver must be re-served first: **true**. The adapter reads only S3 (`source_addresses` 201-202, `read_source` 209-214, `build` 448-455); it has no
  argument or function that builds from local tables.
- `commonwealth_fwd3_serve.py --apply` (773-786) writes all three silver tables in one loop; no per-table flag; refuses an existing object without `--overwrite`.
- Silver changes: `daily_returns` 44 rows (flow), 2 of them also in return; `month_grades` 1 row (computed_pct, month 2014-12, verdict unchanged);
  `account_day_value` 0 data rows. `cash_leg` (method_r28 -> method_r29) and `run_commit` change in EVERY row of all three tables (1,691,729 / 21,102,041 / 82,593).
- `apply_days` (822-891) cannot restrict to 2 dates (it loops over the whole manifest), is mint-only (refuses a non-empty target prefix, 852-862),
  and refuses the tracked manifest (no `split_store`, 834). It rewrites the sidecar and method row on every run (content unchanged).

## The 2 day files

| date | rows | measured | rows changed | columns | day manifest | sidecar |
|---|---|---|---|---|---|---|
| 2014-12-03 | 335 | 23 | 1 | external_flow, total_return_daily | producer content identical; only `landed` (etag, bytes) | no change (row measured under both) |
| 2020-11-13 | 560 | 33 | 1 | external_flow, total_return_daily | producer content identical; only `landed` (etag, bytes) | no change (row measured under both) |

Method row: `method_version` 3 comes from the `sources.json` entry `_commonwealth_delivery`, not from the silver cash-leg label; no change implied by the code.

## Captured state (Branch A)

Both buckets: versioning Enabled, MFADelete none. Silver version ids equal the tracked manifest `source_versions`. Every object's ETag, size, VersionId and
LastModified is in `writes[]`. Rollback per key: server-side copy of the captured VersionId (written, not run).

## Readers

Cottonwood: the mint adapter's `verify_served` (gold), the adapter's `build` read of the silver tables, the serve script's `--verify` (silver).
Others (reporting-gold and reporting-publish handlers, `client_report_figures.py`, the terraform roles) resolve to firm 49financial, not Cottonwood.
`comp-find ... portal` errors in this worktree (empty submodule folder); the base checkout was searched by Grep: comments only.

## Not established

See `not_established` in the record: no re-mint was exercised; the 43-file set is derived (build() not run); version history not listed;
the method row's later LastModified (10:38Z) is unexplained; readers outside the three searched scopes.
