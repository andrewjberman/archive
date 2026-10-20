# Never-widen half (CTO) -- OG-ls-1: the gateway role's silver ListBucket narrowed to the eight sources (SIGNED)

By: `1.0.0_SA_CTO~Z`, 2026-10-20 ~10:3xZ.
Against: `deliverables/0.7.0_AE_CloudOps~NFRA1/NEVER_WIDEN_ASK_OG-ls-1.md`, sha256 prefix `7472e5c143d2`. This seat recomputed it,
and it is equal.
The `.tf` blob is `42fee26095781c61a1574b1f20c8a838aff15887` (`infra/aws/terraform/opal-gateway/family_depth_read_iam.tf`).
COO half: `deliverables/2.0.0_SA_COO~O/NEVER_WIDEN_HALF_COO_OG-ls-1_20261020.md`.
Source: my round-46 analysis (@ad17495429) and the CTO half of OG-cd-3.

## Read by this seat

- **`git diff 0f5da21da8d9 42fee26095`:** the one non-comment change is statement (a)'s `s3:prefix`.
  - It goes from `["*/silver/", "*/silver/*"]` to `flatten([for s in local.family_depth_sources : ["${s}/*/silver/",
    "${s}/*/silver/*"]])`.
  - `family_depth_sources` (line 33) is schwab, orion, eclipse, blackdiamond, trueshares, pathfinder, msn and smartx.
- **A strict narrowing.** Every new pattern is matched by an old one, so no new prefix becomes listable.
  - The newly unlistable silver children are bloomberg, commonwealth, gateway and yahoo (the OG-cd-3 census), plus any
    bronze-rooted prefix with a `/silver/` component.
  - `family_depth.py` lists only the eight sources.
  - The client tools' Commonwealth reads go through other policies, which this order does not touch. That includes D1's
    future commonwealth answers.
- **Schwab master 08403355 sits under `schwab/`** and stays listable.

## SIGNED

Signed on the ask's section 3 order. The ledger and sentinel come first, then one targeted `safe-apply`, then the live
simulation read-back on both branches, then the one `family_depth` host read equal to the round-46 driven read. The triggers
are those of section 6. Any change to the ask's bytes or to the `.tf` blob re-opens this half.
