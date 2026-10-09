# Never-widen ask -- OG-pn-1, the six held RPS dates of the Tax SMA master (row Z-W46-S3)

By: `0.9.0_WK_NFRA_OPLGTW~50`, Phase A. Halves owed: `1.0.0_SA_CTO~Z`, `2.0.0_SA_COO~O`.
Evidence: `pn1_measure.json` beside this file (S3 reads only; nothing written, deployed, invoked or re-run).
Code: this worktree's branch `wk-NFRA_OPLGTW-33-50`; the commit is named in the worker report.

## 0. The measurement changed the shape of the fix -- read this first

The order says "extend the RPS section-1 pin with the 28 columns". Measured, that cannot work and would be wrong:

- All six held files (20251212, 20251215..20251219) carry ONE identical extra set of 28 columns (`all_six_identical: true`),
  but they carry **no D1 positions section at all**. Their only table is a **D2 account-balance table, 34 columns, equal
  to the RPS section-2 pin in order**. The T1 attests exactly the D2 rows (1, 2, 2, 2, 2, 3).
- `crs_reader.scan_crs` numbers sections by file order, so that lone D2 table becomes "section 1" and is graded against the
  section-1 POSITIONS pin (58 columns). The 28 are exactly the section-2 pin's columns minus the 6 it shares with section 1.
- Adding the 28 to the section-1 pin would still raise: 46 core section-1 columns are absent from the held header
  (`literal_extension_check`), and making them all APPENDED/NULL-fillable would loosen the removal guard and write balances
  into `fact_rps` and `dim_position`. Refused as written; the order's intent (the held dates convert, the guard holds) is met
  another way.
- The converter already converts these dates for 08335338 and 08242234 because their files carry D1 AND D2.
- 08403355 context: bronze 20250911..20251211 are H1+T1 shells (silver landed); 20251222 onward carry D1+D2 and are
  converted (silver present for all four tables on every one of the 86 dates scanned, 20251205..20260410). Of those 86, only the six held dates are D2-only; later dates (files 54 KB and up) were not shape-scanned.

## 1. The code change (source `data/assets/scripts/silver/schwab_conversion.py`; Lambda copy byte-equal)

1. `pin_section(feed, smeta)`: a scanned table is graded against the section its own data tag names (D1 -> 1, D2 -> 2) when
   that (feed, n) is pinned, else its file position. On every file that carries all its sections the tag number equals the
   file position, so nothing that converts today changes.
2. For a file whose tables were routed away from their file position (the D2-only shape), the declared section(s) it did not
   ship (here section 1) are landed as the PINNED 0-row partition (`fact_rps`, `dim_position`), the same shape the 0-row-shell
   law lands, after every real writer has finalized. The vendor T1 attests zero positions. This keeps all four tables present
   for the date, so the record reads complete. The shell branch and this one now share one helper, `_land_pinned_empty`.
3. No pin, projection, schema or drift-guard code changes. The 28 columns are already NAMED in the section-2 pin with the
   vendor's types. The guard still raises: an unknown column under the section-2 pin, the 28 under the section-1 pin, and
   an unknown column in a D2-only file through the whole converter (lands nothing).

Tests: `tests/test_ogpn1_rps_pin.py` (`test_ogpn1_ac01..03`), fixture `tests/fixtures/ogpn1_rps_d2_only_header.json` (the
verbatim H4/H5 header, names only, no account field). Negative control: with the pre-change converter, ac01 and ac02 fail with
the production error (`SchemaDriftError ... 28 columns ... feed=RPS s1`) and ac03 passes.

## 2. Deploy path (the applier's, not this cell's)

- One Lambda: `opal-assets-silver-schwab` (`module.silver_converter["schwab"]`, `infra/aws/terraform/opal-assets/silver.tf`).
  Only `schwab_conversion.py` differs in the package dir; the other 10 vendored modules are unchanged.
- By Terraform, by `0.7.0_AE_CloudOps~Z`, never `update-function-code`: rebuild the package from the package dir, upload to the
  artifact key `opal-assets/opal-assets-silver-schwab.zip`, plan, apply through `safe-apply`.
  `local.silver_build_commit.schwab` (silver.tf, outside this cell's paths) moves to the commit whose
  `data/assets/scripts/silver/` tree equals the package dir (rollback pin `47c3c75f11`). The applier records the live artifact's
  S3 VersionId and `source_code_hash` BEFORE the swap.
- Other families, the role, the notification rules, the schedule and the memory/timeout stay as they are.

## 3. What moves, for each of the THREE masters (both branches)

| master | file carries D1 + D2 (every file seen) | file is D2-only (the held shape) |
|---|---|---|
| 08403355 | converts exactly as before (5 real files compared old vs new: identical keys, put order, sha256 of every object; this master's 20260408 and 20251222 included) | the six held dates now convert: `fact_rps_s2` + `dim_balance` carry the D2 rows, `fact_rps` + `dim_position` land 0 rows under their pins (offline dry run on the real bytes: 1,2,2,2,2,3 rows) |
| 08335338 | converts exactly as before (20251212 compared identical) | none seen in the 6-date window; a D2-only file that today raises drift would convert under the same rule |
| 08242234 | converts exactly as before (20251219 compared identical) | none seen in the 6-date window; same rule |

Limit, stated: the old-vs-new byte comparison covers 5 real files and the D2-only census covers 08403355's 86 RPS objects
20251205..20260410 and the six held dates for the other two masters, not every 08335338/08242234 date. An H1+T1 shell file takes
the unchanged shell branch (20251205 compared identical).

## 4. Served tables

No served table or dimension changes. `dim_balance` is the identity projection of the section-2 fact (all 34 columns,
contract SS7d) and already carries the 28; `dim_position` projects 25 position columns and has none of them. No column is
added to any pin or projection. The held dates gain rows in existing tables only.

## 5. Rollback

- Code: re-point the function to the prior artifact version recorded before the swap (same Terraform path), and
  `silver_build_commit.schwab` back to `47c3c75f11`. The prior converter simply refuses the six files again (the held state).
- Data: every key the re-run writes is a first version (no silver exists for the six dates today, measured by head_object on
  all four tables). Rollback per key is `delete-object --version-id` of the recorded version, operator identity, for: 24 silver
  objects (4 tables x 6 dates), the run manifest(s), and the per-date completion/closure records the event run writes (delete
  completion records first, as the OG-bh-1 half orders).

## 6. The re-run of ONLY the six held dates (after the deploy)

- How: invoke the converter once with an S3-event payload naming exactly the six bronze keys
  `schwab/08403355/bronze/rps/{20251212,20251215,20251216,20251217,20251218,20251219}/08403355.CRS<date>.RPS.zip`
  (no bronze object is written or re-created). The 12:15Z sweep would do the same retry on its own and is the fallback; the
  applier takes one path and records it.
- Writes per date: `fact_rps`, `fact_rps_s2`, `dim_position`, `dim_balance` under `schwab/08403355/silver/<table>/date=<d>/`
  (idempotent: a key already landed is skipped), one run manifest per lane per invocation, and the date's complete marker with
  closure (conditional PUT) via `run_event`. A date whose closure cannot qualify is carried INCOMPLETE by the existing
  code, never withheld and never forced.
- Not touched: bronze, the other 5 vendor types, any other date, 08242234, 08335338, `opal-data-schwab`, grants, schedules.
- Served effect: the Gateway may start serving a held date once its closure qualifies, inside the existing grant window; that
  is the served-output move this pair signs.

## 7. Decisions asked of the halves

1. Accept the table-tag routing in place of the section-1 pin extension (section 0).
2. Accept landing the 0-row `fact_rps` / `dim_position` for a D2-only file. Alternative: land only the D2 pair; the date then
   has two of its four tables and may read incomplete again (one-line change).
3. Re-run path: direct six-key invoke, or wait for the 12:15Z sweep.

## Half -- `1.0.0_SA_CTO~Z`

(sign / refuse + date)

## Half -- `2.0.0_SA_COO~O`

(sign / refuse + date)
