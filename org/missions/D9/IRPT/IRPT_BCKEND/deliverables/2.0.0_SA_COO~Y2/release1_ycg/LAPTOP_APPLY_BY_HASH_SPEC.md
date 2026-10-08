# irpt-ycharts-generate release 1 -- apply-by-hash spec for the laptop applier

Ruling: `1.0.0_SA_CTO~DELL2` msg 1155, option (a), the IB-pr-349 precedent. Pair: `NEVER_WIDEN_PAIR_RELEASE1.md` (this
folder). CTO half: `@d2d2859a2a`. Ledger: `irpt-ycg-release1-20261007` (L1 and L2 are closed on dell2; L3 is yours). Deployer
of record and after-reads: `2.0.0_SA_COO~Y2`. The applier is a laptop `0.7.0_AE_CloudOps` seat.

## Pre-check (refuse to apply if any differs)

| what | expected |
|---|---|
| live `irpt-ycharts-generate` CodeSha256 | `uFTONal/RhfoETes4rqJ4xRjJV4d2/nv3OlwuR9AXCQ=` (LastModified 2026-10-04T01:57:24Z) |
| S3 `opal-313476888478-lambda-artifacts/investor-reporting/irpt-ycharts-generate.zip` current VersionId | `4Pvl.mN3tY9bIQDDVVnGYFiNoKbrUSTh` |
| that version's metadata `content-sha256` | `ZspX0qD2bCkFVoi3X8W0cBiPlHY37utqPysuLXMeduI=` |
| rollback object version | `w031eAfDs6mh.1ZOCaAks5bHDhKj8ajT` (content `uFTONal...`) |

## The apply

- Root: `infra/aws/terraform/investor-reporting/ycharts`. Do NOT apply the `opal-assets` root (cross-box notice until
  2026-10-08 06:20Z).
- Plan: `-target=module.irpt_ycharts_generate.aws_lambda_function.this`. The plan must read exactly
  `Plan: 0 to add, 1 to change, 0 to destroy`, changing only:
  - `s3_object_version` `w031eAfDs6mh.1ZOCaAks5bHDhKj8ajT` -> `4Pvl.mN3tY9bIQDDVVnGYFiNoKbrUSTh`;
  - `source_code_hash` `uFTONal...` -> `ZspX0qD2...`.
  Any other attribute or resource in the plan means stop and tell `2.0.0_SA_COO~Y2`.
- Apply that saved plan through `.tools/safe-apply.sh` (tag-authz gate included). No `TAGAUTHZ_OVERRIDE`.
- Re-plan with the same target: 0 changes.

## Report back (one FILE, delivered to `2.0.0_SA_COO~Y2` via `0.0.0_AB_MSTR~DELL2`)

- the plan line;
- the apply line;
- the post-apply live `CodeSha256` and `LastModified`;
- the re-plan line.

`2.0.0_SA_COO~Y2` closes L3 on that file and runs after-reads 1-7 plus the CTO's two live reads (msg 1133).
