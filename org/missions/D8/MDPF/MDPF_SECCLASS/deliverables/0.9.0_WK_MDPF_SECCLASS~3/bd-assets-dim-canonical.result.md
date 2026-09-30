# MDPF_SECCLASS.TO-SC-t2 -- worker report (0.9.0_WK_MDPF_SECCLASS~3)

## Change

`data/black_diamond/scripts/silver/build_bd_assets_dim.py` `apply_blend()`:

- Added three new columns, computed for EVERY asset (not only BD-coarse ones) via the library's
  public API (`classify`, `get_sub_asset_class`) only:
  - `asset_class_canonical` -- the canonical `etf-classifications` row's class, verbatim; `''`
    when the table carries no row.
  - `sub_asset_class_canonical` -- the canonical row's sub-class; `''` when no row.
  - `class_source` -- `etf-classifications` (resolved) or `unclassified` (no row).
  A BD super class never overrides these -- they are computed independently of
  `asset_super_class_bd`, so an asset with a canonical row keeps that row's class even when BD's
  own super class is fine-grained (non-coarse), and an asset with no row reads `unclassified`
  rather than quietly keeping BD's own value.
- Amendment 1 (row `MDPF_SECCLASS-W3-S2`): removed the print reading `clf._ticker_map` /
  `clf._name_map` (private attributes SC-t-1 retired) and the stale print naming a `bd-securities`
  DynamoDB scan (SC-t-1 already retired that read path). The function now reads the library
  through `classify`/`get_sub_asset_class` only.
- The pre-existing legacy BD-shape blend (`asset_super_class_blend`, `super_class_source`,
  coarse-BD-only, `ETF_TO_BD_SUPER`) is left in place and unmodified beyond reusing the same
  `canonical_class` value already computed in the same loop (no second classify call) -- it is a
  distinct, pre-existing mechanism this order was not asked to change.
- `apply_blend` now takes an optional `classifier=` injection seam for tests (defaults to
  `ETFClassifier.instance()` in production, unchanged callers).
- Docstring's dim-schema block updated to list the three new columns.

## Tests

`data/black_diamond/scripts/silver/tests/test_assets_dim_canonical.py`, five cases on a stubbed
library (no live AWS call):
- `test_canonical_row_overrides_a_bd_super_class` -- GLD's BD super class is `'Equities'`
  (fine-grained, not coarse); the canonical row still wins on `asset_class_canonical`.
- `test_unknown_ticker_is_unclassified_by_name` -- an unknown ticker reads `class_source =
  unclassified`, empty class/sub-class.
- `test_gld_phys_vxx_carry_their_canonical_classes` -- GLD, PHYS, VXX land their canonical
  class/sub-class per the stub table.
- `test_public_api_only_no_private_map_read` -- the stub carries no `_ticker_map`/`_name_map`
  at all; `apply_blend` does not raise (amendment 1).
- `test_class_sources_are_only_etf_classifications_or_unclassified` -- the `class_source` column's
  value set.

`python -m pytest data/black_diamond/scripts/silver/tests/test_assets_dim_canonical.py -q
-p no:cacheprovider` -> **5 passed in 0.98s**.

## Census (real local build, LOCAL only -- no upload)

`org/tier1_exec/2.0.0_SA_COO/deliverables/MDPF_SECCLASS_M/R1_BD_SILVER_CENSUS_20260929.json`, from
a real local build of the silver assets dimension against live `s3://opal-data-bd/silver/
bd_assets.parquet` (3,449,107 transaction rows, columns-restricted read -- a full-column read hit
`ArrowMemoryError` on this device's exhausted virtual memory, measured: `systeminfo` showed 2.6 GB
of 62.8 GB virtual memory available) deduped to 10,937 unique `asset_id`s (idxmax-based dedup --
the committed `build_dim()`'s `sort_values`-based dedup also hit an `ArrayMemoryError` on this
device; same source, same rows, same identity columns, a lighter dedup algorithm used only for
this one-off local build script, not committed to the product file) and the real `apply_blend()`/
`apply_opal_taxonomy()` (live `ETFClassifier.instance()` reads against `etf-classifications`):

- **rows:** 10,937
- **class_sources:** `{"etf-classifications": 296, "unclassified": 10641}`
- **unclassified:** 10,641 (every one named in `unclassified_names`)
- **moved_vs_current:** 296 -- the currently-served `s3://opal-data-bd/silver/bd_assets_dim.parquet`
  (measured live, 2026-09-29) carries no `asset_class_canonical`/`class_source` column at all, so
  every asset this build resolves through `etf-classifications` is new information relative to
  what is currently served.
- **artifacts:** `[".scratch/bd_assets_dim_local_20260929.parquet"]` (local only, not uploaded, not
  committed -- BOUNDS "no upload, no deploy"; scratch is not a deliverable surface).

`python org/tier1_exec/2.0.0_SA_COO/deliverables/MDPF_SECCLASS_M/R1_CHECKS/r1_bd_build_census.py
silver` -> **BUILD-CENSUS silver rows=10937 unclassified=10641** (rc=0).

296/10,937 is a small fraction because `etf-classifications` holds 344 rows today (pre-backfill);
SC-k-1's scheduled backfill (round 1, released after this thread) is what raises that coverage --
same shape as SC-t-1's own resolution census on the gold-layer holdings.

## Proof

`org/missions/D8/MDPF/MDPF_SECCLASS/deliverables/0.9.0_WK_MDPF_SECCLASS~3/MDPF_SECCLASS.TO-SC-t2.bd-assets-dim-canonical.proof_of_spec.json`,
validated `python .tools/proof-of-spec-check.py <instance> SC1-t2-AC1,SC1-t2-AC2` -> VALID rc=0.
Both criteria PASS-by-output; `<status>` flipped to `complete`.

## Commits

See worker report.
