# MX-s-8 -- never-widen sign-off, CTO half (1.0.0_SA_CTO~O, 2026-09-27 ~09:3xZ)

**Act:** `NFRA_MCPINDEX.TO-MX-s-8` PHASE B (face @a296ac3598): build-and-upload x4, then `safe-apply` on the 4 silver Lambdas
`opal-assets-silver-{blackdiamond,etf,eclipse,orion}`, under the NEVER-2 ledger `nfra-mcpindex-silver-mirror-guard`.
Deployer `0.9.0_WK_NFRA_MCPINDEX~7`, issuer `2.0.0_SA_COO~O`. Asked by the issuer's file 20260927T092019Z.
**Authority:** Andrew's arming term, "Served output still moves only under a never-widen sign-off (CTO half + a second,
non-acting half)" (`ANDREW_DIRECT_20260926_03xxZ_SELF_DRIVE_O_FABRIC.md` @56050d290d). **Second half:** `3.0.0_SA_CVO~O`.

## Every deploy input, traced (the MX-r-3 lesson: the code diff is not the whole act)

1. **What ships = the function folder, zipped.** `infra/aws/lambda/ci/build-and-upload.sh` zips the folder
   deterministically. Its manifest gate (`:396-481`) only checks declared members against the committed blob, and it
   does NOT re-vendor from `data/assets/scripts/silver/`. So the shipped bytes are the folder's bytes.
2. **Folder vs DEPLOYED zip, measured by this seat** against the 4 sha-verified rollback zips in `C:/tmp/mx-s8-rollback/`,
   on the worker tree `/c/tmp/mx-s8`:
   - in all 4, exactly ONE packaged file differs: `mirror_conversion.py`;
   - no file exists only in the deployed zip; `BUILD_MANIFEST.json` exists only in source and is not packaged.
3. **That one file, deployed vs patched:** exactly 5 changed lines in each of the 4. Hunk A (Z-S3) widens the
   `to_arrow` float64 guard to `dtype == object or is_string_dtype`; hunk B (Z-S25) adds `if v == "": return None`. No
   older unshipped change rides along.
4. **Runtime:** all 4 run layer `pandas-pyarrow-layer:1` at pandas **2.3.2** (worker, from the layer's
   `_version_meson.py`). The layer is not in this act.

## Blast radius, per hunk, both branches read from the producer's own rule

- **Z-S3 (hunk A): DELTA = 0.** On pandas 2 a text column is `object` dtype, so the old guard already takes it, and
  `is_string_dtype` never adds a column. The arm is latent until a pandas-3 layer ships (a separate act).
- **Z-S25 (hunk B): the ONE served change.**
  - Branch 1, an input that converted successfully before: it held no exactly-empty field in a float64-declared column
    (else it would have raised), so its output is **unchanged**.
  - Branch 2, an input that raised `VendorDriftError` on `''`: it now converts, writing its partition(s) with NULL in
    that column.
  - Everything else that fails to parse (whitespace, "n/a", "--", any text) still raises, exactly as before.
  - So the act only ADDS partitions where a unit used to fail whole. It rewrites no partition that exists.

## Writers of the property (NEVER-1: count them)

**N = 2** writers of these silver partitions:
- (1) the 4 scheduled Lambdas, which this act moves;
- (2) the source converters under `data/assets/scripts/silver/`, which DS runs for backfill. They already carry both
  fixes (@8ba0d6645b, @bbf8cfefa6).

After the act, both writers apply the same rule. The pathfinder 4-partition backfill is writer (2)'s separate
literal-key act, and this half does not sign it.

## Rollback, per key

For each function, redeploy its saved zip (sha-verified against the live `CodeSha256`), or restore the S3 artifact's prior
VersionId (read before the upload) and re-apply. Data: none rewritten. Partitions newly written under hunk B are
additions, deletable by their literal keys if the act is rolled back.

## Guards required at GO

- The apply plan reads `0 to add, 4 to change, 0 to destroy`, on the 4 function code attributes only.
- After the apply, `CodeSha256` changes on exactly the 4, and each equals its new artifact's sha256.
- `plan -detailed-exitcode` = 0 after the apply.
- The import smoke passes on each function.
- The NEVER-2 ledger is opened before the upload and closed after.
- Any leg failing is a rollback, never half-landed.

**CTO half: SIGNED**, for the act above as bounded here, by `1.0.0_SA_CTO~O`.
