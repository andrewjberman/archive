# BP-b-6 -- lot-level unrealized export: the patch and its fixture proof (nothing applied)

Worker 0.9.0_WK_ADVI_BDPRCE~10, round 2. Base HEAD 6f20fe54c6. Record: `LOT_PROOF.json` (measured by `test_lot_split.py --emit-proof`).

## The diff, in words

`unrealized_lots.diff` (62 lines added, 0 removed) against `data/black_diamond/scripts/silver/merge-daily-incremental.py` at HEAD. It applies byte-exact to the HEAD file.

- Adds `LOT_MEASURE_COLS = ['units', 'cost_basis']`, `LOT_KEY_COLS = ['account_id', 'asset_id', 'open_date', 'unit_cost']`, `build_unrealized_lots()`, `lot_address()` (the builder call, never a typed address) and `_s3_upload_addr()` (uploads to an s3:// address in any bucket).
- In `process_unrealized_xlsx_to_parquet`, after the file date is read and before the position dedup: builds the lot frame from the export, then DROPS the two measure columns from the frame the legacy table is built from. The legacy dedup on `(account_id, asset_name)`, the parquet write and the `silver/unrealized/<date>.parquet` key are unchanged.
- After the legacy upload: writes the lot frame to `<builder address>/data.parquet`. If the export has no Units or Cost Basis column, it logs SKIP and writes no lot table, so the patch is safe to land before the template switch.

## The mapping assumed

- Export headers are the template measure names. The step's own `to_snake_case` (same rule as Cottonwood, `data/cot/scripts/silver/cot_silver_merge.py:154`) turns `Units` into `units` and `Cost Basis` into `cost_basis`.
- Cottonwood's template names the same measures `Units` (sourceColumn `units`) and `Cost Basis` (sourceColumn `costBasis`), both selected.
- The 15 existing 49F headers were read from a real export: `Open Date`, `Unit Cost`, `AccountID`, `AssetID`, `Asset Name` map to the lot key and dedup columns.
- Not verified: the live header text for the two new measures. The fixture uses the assumed names.

## Fixture numbers (recorded export UNREALIZED_DAILY_2026-10-09.xlsx, sha256 5700843f...)

- Export: 500,000 rows, 15 columns, no Units or Cost Basis.
- Legacy table: 108,439 rows, 17 columns (the 15 export columns plus `_source_file` and `_ingested_at`). Legacy sha256 d65ce03d...
- Lot table with the SYNTHETIC `Units` and `Cost Basis` columns: 484,447 rows, key unique, carries `units` and `cost_basis`. The legacy table carries neither.
- Byte equality: repo function on the original export equals patched function on the original export. Patched function on the export with the two columns equals both. Negative control: the repo function on the with-columns export DOES carry `units` and `cost_basis`, so the drop is exercised.
- Address: `s3://opal-data-assets/blackdiamond/49financial/silver/unrealized_lots/date=2026-10-09`, from `lib.opal_naming.address`.
- Test: `LOT SPLIT TEST: OK 7 arms`. A cold run parses the xlsx (about 60 s); the parse is cached in the data directory by sha256.

## The template

- S3 `code/bronze/templates/unrealized.json`: VersionId `VgzqQbd.3F3sAlllb6SWsjKZ2XvXgAfE` (read now), 14,419 bytes, CRLF line endings. Same VersionId as round 1.
- Repo copy: 13,920 bytes, LF line endings. Not byte-equal to S3. Equal after CRLF normalization, and equal as parsed JSON.
- Patched copy `unrealized.patched.json`: built from the S3 bytes, so it is the object the apply would replace and the rollback target. Only the two `isSelected` flags of measures 15 and 16 change (false to true). Parsed diff: exactly two values. 14,417 bytes.

## What the live first export could change that this fixture cannot

1. The two new headers may not be named `Units` and `Cost Basis`. Then the lot table is SKIPped, legacy is unchanged, and no lot table lands. The apply must read a real post-switch export.
2. The lot key is the mandated one and it is not a tax-lot identity on this export. 15,553 rows (3.1%) collapse under it. In 14,514 of the 14,696 colliding groups `Relationship ID` differs. 7,384 rows have a null `Open Date`, which the dedup treats as one value. Surfaced as row `ADVI_BDPRCE-D1-W10-S2`, ARMED, disarm owner `2.0.0_SA_COO~K1`.
3. The export holds exactly 500,000 rows, a round count. Completeness cannot be judged from the fixture. Surfaced as row `ADVI_BDPRCE-D1-W10-S3`.
4. The silver step imports `lib.opal_naming` at run time. If the runner cannot import it, the lot write logs FAIL and writes nothing. Legacy is unaffected.
5. Write access by the BD runner to `opal-data-assets` is not verified. No write was attempted.
6. The synthetic `Units` and `Cost Basis` values only exercise the code path. Their economic meaning (fractional units, cost totals) is not checked.
7. `_ingested_at` is pinned in the test only. The live step stamps it per run, so legacy bytes differ run to run, while the legacy rows, columns and values stay the same.

## Rollback at apply

The S3 template's prior VersionId `VgzqQbd.3F3sAlllb6SWsjKZ2XvXgAfE` is recorded in `LOT_PROOF.json`. Restoring it returns the template to its pre-switch bytes.
