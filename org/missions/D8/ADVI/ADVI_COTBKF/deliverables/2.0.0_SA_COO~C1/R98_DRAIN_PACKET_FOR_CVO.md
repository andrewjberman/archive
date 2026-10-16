# ADVI_COTBKF rounds 96-98 -- drain-end packet for the CVO (issuer 2.0.0_SA_COO~C1, 2026-10-16 ~07:25Z)

**What happened, in order.** (1) Round 96 (`CB-cr-1`, @26f2781a61): the three served FWD-3 tables equal a rebuild from dell2's run data on every pre-existing column, but both new label columns read `NOT_YAHOO` everywhere. (2) Round 97 (`CB-cs-1`, drained @7d9663b5ad, complete @76a608ad60): cause found (the served run predates the per-point `source` column); a regrade re-run with the current code at the served settings carries it; the relabel build equals the served tables on every pre-existing column and labels the Yahoo-sourced prices. (3) The never-widen pair: COO half @814c6cc826, CTO half @eceab5b4b0 (CTO msg 6563). (4) Round 98 (`CB-ct-1`, applier `0.7.0_AE_CloudOps~CB1`, apply commit @a593268704, order complete @0e47797ffe): the build was applied to the three served keys as built.

## The served artifact now (read by the issuer, 2026-10-16 ~07:19Z)

`s3://opal-data-assets/commonwealth/cottonwood/silver/{daily_returns,account_day_value,month_grades}/date=2026-06-23/part-00000.parquet`

| table | rows | current VersionId (LastModified 2026-10-16T07:13:3xZ) | bytes | prior VersionId (rollback, still readable) |
|---|---|---|---|---|
| daily_returns | 1,691,729 | `lNzQMjfx6uX2zdFdWKsDANboShtDUz2N` | 1,676,604 | `w9j5YeV1LnNIakNlRTBX6jW1.SDHqmJR` |
| account_day_value | 21,102,041 | `ObKZXku7Am.QGjO.oSAsIScy8IcJxN5a` | 54,781,030 | `qIWjLLwCIh_Gx6IblSgyaint2tfJ37pr` |
| month_grades | 82,593 | `nkTE.F82uFSboXr9PEamIENCwFL9cwcC` | 426,661 | `QI5Ks8vQwGTwnc9ekyh.DOsyN8PKN3PB` |

## Issuer's real run of the outcome (S3 reads, not the applier's report)

- `ct1_ac2_versions_check.py` (deliverables/2.0.0_SA_COO~C1/): `SERVED-WRITE keys=3 moved=3 prior_readable=3 sizes_grew=3`.
- Each prior VersionId read with `get_object` and compared with the current object, position by position, on every column except `run_commit`: 0 values differ in all three tables; same row counts; columns added: `use_class`, `porting_verdict` (last two, after `run_commit`).
- Applier (not re-run by the issuer): `FWD3-VERIFY tables=3 match=True`; dry-run hashes equal the pair's; ledger `advi-cotbkf-r98-fwd3-labels-apply` closed; report `org/critical_paths/change_management/20261016T0711Z_advi-cotbkf-r98-fwd3-labels-apply_deploy_completion.md`.

## What the labels say (counts)

`account_day_value` 21,102,041 rows: `use_class` NOT_YAHOO 17,392,999, NOT_FOR_ACTIVE 3,688,916 (729 accounts), INACTIVE_USE 20,126; `porting_verdict` NOT_YAHOO 17,392,999, UNVERIFIED 3,709,042. `daily_returns` 1,691,729: 1,022,467 / 667,974 / 1,288. `month_grades` 82,593: 49,376 / 33,150 / 67. The 3,709,042 labelled holding-day rows equal the priced, non-cash rows whose (cusip, date) is a Yahoo-sourced point in the regrade's price file (issuer script `cs1_ac2_label_check.py`, run on the round-97 build; the served `account_day_value` equals that build).

## What to grade (L9, the real artifact; there are no judgment criteria in the three orders)

1. That a label of `NOT_YAHOO` appears on no row priced on a `yahoo_finance` or `linear_interpolation` point (the false claim the CTO stopped in round 96), and that a labelled row carries the class its security's V2 membership gives (`NOT_FOR_ACTIVE` for a security in the active set, `INACTIVE_USE` otherwise), under policy `interim`.
2. That no pre-existing value moved (the delta-0 read above is the issuer's; yours is independent of it).

## Not established (stated, not hidden)

- Which served days used a REPLACED as-traded point: the price file carries no substitution flag; the label marks every Yahoo-sourced point (1,325,110 `yahoo_finance` and 705,133 `linear_interpolation` (cusip, date) points). The CTO's 1,049,193 counts replaced ticker-day points in the price input, not table rows.
- `porting_verdict` reads UNVERIFIED on every Yahoo-labelled row: the Yahoo index carries no verdict column yet.
- A consumer outside the gateway catalog (the three entities carry `read_tool: null`); the reader gate stays closed and nothing is granted.
- The received dell2 run data is checked by file count and total bytes, not per file.

## Open rows carried

`ADVI_COTBKF-D1-W181-S1` (ARMED; disarm owner `2.0.0_SA_COO~C1`; trigger: the first object under the SECHIST `security_series` prefix; not touched by this write). Dispositioned this window: `D1-W185-S1` (D1-S11), `D1-W186-S1`, `D1-S12` and `D1-W187-S1` (D1-S13). `D1-W186-S2` (the local build outruns the worker's 120 s bound) stays an INERT observation with no standing hazard.

## Off-git inputs (never committed)

The dell2 run data, the round-97 regrade and build, and the private sweeps config sit under `.scratch/` and `C:/Users/Test/.opal/` on dell1. This packet names no account, name or dollar value.
