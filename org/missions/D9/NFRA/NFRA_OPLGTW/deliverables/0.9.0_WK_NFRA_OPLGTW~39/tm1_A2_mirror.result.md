# OG-tm-1 amendment A2 -- the source mirror, the repin and the rebuilt converter artifact (row W39-S4)

Nothing applied, uploaded or sent. Worker `0.9.0_WK_NFRA_OPLGTW~39`, 2026-10-09 ~01:3xZ.

| Step | Result |
|---|---|
| `data_assets_mirror.patch` applied to `data/assets/scripts/silver/` | `git apply --check` clean, then applied: 4 files, +56 -4 |
| Tests, the two touched files | `46 passed` (`tests/test_conversion_manifest.py`, `tests/test_schwab_runtime.py`) |
| Tests, the whole `data/assets/scripts/silver/tests` | `566 passed, 11 skipped` in 17.02 s, 0 failed (skip reasons not read) |
| Source commit | `47c3c75f11` (full `47c3c75f116bbc9b235b06589f752e7707ee14ff`) |
| Repin | `silver.tf` `silver_build_commit.schwab` `1f03a3f209` -> `47c3c75f11`, commit `7af0b6bc3d`; rollback pin `1f03a3f209` |
| Plan after the repin (`plans/opal-assets.A2.txt`) | one new in-place change: `module.silver_converter["schwab"].aws_lambda_function.this`, `OPAL_BUILD_COMMIT` `1f03a3f209 -> 47c3c75f11`; the other resources unchanged from the Phase A plan |
| Vendored package = source, byte for byte | `probes/tm1_A2_source_equals_package.txt`: at `47c3c75f11`, 11 of 11 `BUILD_MANIFEST.json` `vendored_modules` equal the package file (9 in `data/assets/scripts/silver/`, 2 in `data/assets/scripts/lib/`), by `git show` of both blobs |
| Converter artifact rebuilt from the pin | `BUILD_ONLY=1 bash infra/aws/lambda/ci/build-and-upload.sh opal-assets opal-assets-silver-schwab` at `7af0b6bc3d` (clean tree): **sha256 `AzrzJS+91y57ylRdqGccFPGqWaqAGLFn/jhItkAQCzE=`**, 74,839 bytes, 12 members; identical to the Phase A build-only value |
| Zip vs git at `7af0b6bc3d` | 12 of 12 members equal the committed blobs; vs the LIVE artifact (`v2BztqbuhHD3gH95eMqCQzkjPEotvSoeIezEOfsxu90=`) exactly 2 members differ: `conversion_manifest.py`, `silver_registry.py` |

The sha256 above replaces nothing in the COO half's text; it is the value for the apply order. The zip is local (`BUILD_ONLY`); no S3 write.
Two builds (Phase A at `cb9358a9e0`, now at `7af0b6bc3d`) gave one sha256.
