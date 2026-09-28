# MX-s-8 PHASE A ANNOUNCE -- `0.9.0_WK_NFRA_MCPINDEX~7`

Cut at CLOUD `f382d1848c`, worktree `/c/tmp/mx-s8`, branch `wk-NFRA_MCPINDEX-7-s8`. PHASE A ONLY (steps 1-7).
No apply, no NEVER-2 ledger, no deploy record.

## Step 1 -- the two hunks, applied by hand to each of the 4 vendored copies

`git diff` per file shows exactly 2 hunks (`git diff <file> | grep -c '^@@'` == 2 for all four):

- `infra/aws/lambda/opal-assets/opal-assets-silver-blackdiamond/mirror_conversion.py` -- 2 hunks (4 ins / 1 del)
- `infra/aws/lambda/opal-assets/opal-assets-silver-etf/mirror_conversion.py` -- 2 hunks (4 ins / 1 del)
- `infra/aws/lambda/opal-assets/opal-assets-silver-eclipse/mirror_conversion.py` -- 2 hunks (4 ins / 1 del)
- `infra/aws/lambda/opal-assets/opal-assets-silver-orion/mirror_conversion.py` -- 2 hunks (4 ins / 1 del)

Hunk A (Z-S3, `to_arrow`): `elif t == "float64" and df[c].dtype == object:` ->
`elif t == "float64" and (df[c].dtype == object or pd.api.types.is_string_dtype(df[c].dtype)):`
Hunk B (Z-S25, `_numeric_or_raise`): inserted `if v == "": return None` ahead of the `try: return float(v)` in the
string arm. Explanatory comments were NOT copied (condition/clause only, per the handoff's "copy it or not, but
the condition/clause is the contract"). All 4 files kept pure-LF line endings (measured before and after: CRLF=0
in every file).

`bash org/missions/D9/NFRA/NFRA_MCPINDEX/deliverables/2.0.0_SA_COO~O/round2/checks/s8.AC1.sh`:
`vendored copies=4 both fixes 4 of 4 old guard 0 -- RESULT: PASS -- exit=0`

## Step 2 -- etf BUILD_MANIFEST.json

`vendor_sha256.mirror_conversion.py`: `d8dd65a2bcf256ed4566c0f72613307db8af96ca20adf980740488848f2b70aa` (old) ->
`3a99127caf2f5c974c72177e056952d88e32442dc54e030fb8079eb8b95415be` (new, matches the patched file's on-disk
sha256, confirmed by direct hash). blackdiamond/eclipse/orion manifests carry no hashes and are untouched.

## Step 3 -- py_compile + silver suite

`python -m py_compile` on all 4 patched vendored copies: OK, no output, rc=0 each.

`python -m pytest data/assets/scripts/silver/tests/ -q`: **311 passed, 11 skipped, 0 failed** (this is the SOURCE
suite -- the handoff doc notes the vendored bundles carry no tests of their own; this is the belt for the two
hunks' logic, confirmed applied identically to source in the 4 copies by AC1).

## Step 4 -- signer measurements (CodeSha256 / LastModified / layer / pandas version)

All 4 functions carry the SAME layer, `arn:aws:lambda:us-east-1:313476888478:layer:pandas-pyarrow-layer:1`, whose
zip's `python/pandas/_version_meson.py` reads `__version__="2.3.2"` -- **pandas 2, not pandas 3** (no `dist-info`
directory in this layer zip; version read from the vendored `_version_meson.py` instead). This means: on the
CURRENTLY-DEPLOYED layer, Z-S3's string-dtype arm is LATENT (pandas 2's `df[c].dtype == object` already catches
every text column; `is_string_dtype` never fires the new branch) -- the handoff's own words, "on pandas 2 the
`str` dtype does not arise and the test passes vacuously." Z-S25's empty-field arm is live regardless of pandas
version (it is a value check, not a dtype check).

| function | CodeSha256 | LastModified | Layers |
|---|---|---|---|
| blackdiamond | `XiJ6ZADpVAwtJcRR4U0l/IhO4+eFfzost0Mz9fnTIJA=` | 2026-08-25T17:14:42.000+0000 | pandas-pyarrow-layer:1, openpyxl-layer:3 |
| etf | `ZyhzyrjuHLi9TfRC9CFSpvPHY6Rcyq/aPgseJafmuTg=` | 2026-09-26T09:26:39.000+0000 | pandas-pyarrow-layer:1 |
| eclipse | `5hRkhhxIMZ2hiAqZWtfVtUnwXZt3xeKPnLryWOo5OJU=` | 2026-07-22T14:50:08.000+0000 | pandas-pyarrow-layer:1 |
| orion | `rwI6QN5qzT30lWZrf87RlSOEl5XmSGkCTUTdlljqDPo=` | 2026-07-15T22:32:26.000+0000 | pandas-pyarrow-layer:1 |

## Step 5 -- rollback zips (outside the repo, `C:/tmp/mx-s8-rollback/`)

Downloaded via `get-function` `Code.Location`, sha256(zip bytes) base64-compared against `CodeSha256` -- **all 4
verified match**.

| function | rollback zip | size (bytes) | sha-verified |
|---|---|---|---|
| blackdiamond | `C:/tmp/mx-s8-rollback/opal-assets-silver-blackdiamond_XiJ6ZADpVAwtJcRR4U0l_IhO4-eFfzost0Mz9fnTIJA.zip` | 57707 | yes |
| etf | `C:/tmp/mx-s8-rollback/opal-assets-silver-etf_ZyhzyrjuHLi9TfRC9CFSpvPHY6Rcyq_aPgseJafmuTg.zip` | 60041 | yes |
| eclipse | `C:/tmp/mx-s8-rollback/opal-assets-silver-eclipse_5hRkhhxIMZ2hiAqZWtfVtUnwXZt3xeKPnLryWOo5OJU.zip` | 36192 | yes |
| orion | `C:/tmp/mx-s8-rollback/opal-assets-silver-orion_rwI6QN5qzT30lWZrf87RlSOEl5XmSGkCTUTdlljqDPo.zip` | 38193 | yes |

Rollback act named: on a failed Phase B leg, redeploy the matching saved zip above for that function (its
`CodeSha256` was verified against the zip named beside it) and close the entry as rolled back.

## Step 6 -- terraform plan (READ-ONLY; no apply, no `-auto-approve`, nothing typed `yes`)

`terraform init -input=false` then `terraform plan -input=false -no-color` in `infra/aws/terraform/opal-assets`,
run AFTER the step-1/step-2 edits were made (worktree state, not a stale read):

```
No changes. Your infrastructure matches the configuration.
```

No `Plan: X to add, Y to change, Z to destroy` line was printed -- there is no diff at all, so literally nothing
is named beyond the 4 functions (satisfying the criterion's letter), but this is NOT the preview of what Phase
B's apply would do: **filed as a BLOCKING/ARMED surprise row `NFRA_MCPINDEX-Z-W7-S1`** -- the 4 functions deploy
via the `yang-lambda` Terraform module's S3-artifact pattern (`source_code_hash` read from
`data.aws_s3_object.artifact.metadata["content-sha256"]`, never from the local source tree per
`infra/aws/terraform/modules/yang-lambda/main.tf:36-39`), so a plan/apply against the un-rebuilt S3 artifacts is
a 0-diff no-op regardless of the vendored `.py` edits. Neither this task order's Phase A nor its Phase B (steps
8-12) names an artifact rebuild+upload step (e.g. `infra/aws/lambda/ci/build-and-upload.sh`); without one, Phase
B's step 9 apply would ALSO read 0-diff and never ship either fix to a running Lambda. Disarm owner
`2.0.0_SA_COO~O`.

## Commits (LOCAL on `wk-NFRA_MCPINDEX-7-s8`)

- `e0750442c9` -- steps 1-2 (4 vendored copies + etf BUILD_MANIFEST.json), author
  `0.9.0_WK_NFRA_MCPINDEX~7`, `GIT_COMMIT_AUTHOR_OVERRIDE=0.9.0_WK_NFRA_MCPINDEX~7` used (issuer-authorized, for
  the AE-lane infra paths in this one commit only).
- this file's own commit (no override; deliverables + surprise-channel paths are this worker's own lane).

## Not run (Phase B, out of scope for this dispatch)

No NEVER-2 ledger opened, no `terraform apply`, no import-health smoke, no `record-terraform-deploy.sh`. GO is
the issuer's, on both never-widen halves signed.
