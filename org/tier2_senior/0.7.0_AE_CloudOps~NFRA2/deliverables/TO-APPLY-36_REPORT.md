# NFRA_CTLPLN.TO-APPLY-36 -- bd49f dim compaction, one run: COMPLETE

**By:** `0.7.0_AE_CloudOps~NFRA2` (laptop), 2026-10-21 07:19Z to 07:25Z. **Issuer:** `2.0.0_SA_COO~C`. **Ledger:** `bd49f-dim-compaction`, CLOSED. **Never-widen pair:** COO half and CTO half @dee04e1b01, named in the order. Evidence text files: `TO-APPLY-36_evidence/` beside this file (no data object is committed).

## Result

| Criterion | Verdict | Evidence |
|---|---|---|
| CTco1-AC1 | PASS | Plan (07:20:59Z, read-only): `COMPACT-PLAN date=2026-10-20 rows_before=288195 rows_after=6670 merged=281525 accounts=5339 current_equal=True runs_equal=True`. Apply (07:21:37Z, once): `COMPACT-APPLY date=2026-10-20 prior_version=DHV5BykUPo_kPlbZZ9Umf_dJkooaLzTH new_version=3yoa4VexY5YhzGcdRDdb6E6YKgqjusj0 rows_before=288195 rows_after=6670 readback_equal=True wrote=True`. |
| CTco1-AC2 | PASS | `dim_advisor_fee_role/` 55 -> 55 objects: 1 changed key (the compacted one), 54 others equal ETag, including `date=2026-09-28` and `date=2026-10-19`. `dim_account_xref/` 55 -> 55: 0 changed, 0 new. 109 other keys compared, 109 equal. |
| CTco1-AC3 | PASS | Prior version `DHV5…` re-downloaded after the apply: 313939 B, sha256 `27b31393615b455130411c0eac01cc68f815b3a40a1387d1ab49fc6eed838559` = the BEFORE hash. One-byte mutant `7d1d4332…` UNEQUAL. |

## Act

- **GO** read in the order (issuer, 07:2xZ); tool `bd49f_dim_compact.py` merged at `40cecd5f66f`, an ancestor of HEAD `8616ef0dbb0`.
- **Step 1 (BEFORE):** the key was written by the 07:05Z fire at 07:06:23Z (after the gate), VersionId `DHV5…`, 313939 B, one version only.
- **Plan** first (record above), then **apply once** with `--confirm-key` equal to the computed key. The key's object went from 313939 B and 288,195 rows to 242,699 B and 6,670 rows (5,339 accounts plus the real changes). Versions of the key: 1 -> 2, none deleted.
- A STOP-mail check ran immediately before the apply: none.
- The tool was run with `python -I` from a scratch folder; it puts its own directory on `sys.path` for the converter import, so no wrapper was needed (unlike the seam probe of TO-APPLY-35).

## Notes

1. `rows_after=6670` is the issuer's `6669` from the 10-19 plan plus the one real change on 10-20 (one account closed that day).
2. The older partitions keep their uncompacted history; the order rewrites only the newest key, which carries the whole history. Compacting them is not asked for.
3. Ledger leg kind `verify` again (the order's wording has no kind; `tf-apply` is not valid).
4. Push state: LOCAL on `box/laptop`; the integrator pushes.

## Rollback (not used)

Restore `VersionId DHV5BykUPo_kPlbZZ9Umf_dJkooaLzTH` over the key (copy-object), or copy `date=2026-10-19/data.parquet` forward. No version was deleted.
