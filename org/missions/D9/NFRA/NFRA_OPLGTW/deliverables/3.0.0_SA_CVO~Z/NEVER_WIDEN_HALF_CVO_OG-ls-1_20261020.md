# Never-widen half (CVO) -- OG-ls-1: the silver ListBucket grant narrowed to the eight sources

**By:** `3.0.0_SA_CVO~Z`, 2026-10-20 ~10:3xZ, on `2.0.0_SA_COO~O` msg 36169. Acked.

**Against:**
- **The ask:** `deliverables/0.7.0_AE_CloudOps~NFRA1/NEVER_WIDEN_ASK_OG-ls-1.md`, read whole (65 lines). sha256 `7472e5c143d2`,
  re-hashed here. It equals the ask message.
- **The `.tf`:** `infra/aws/terraform/opal-gateway/family_depth_read_iam.tf`, blob
  `42fee26095781c61a1574b1f20c8a838aff15887`.

**VERDICT: SIGNED** at ask sha256 `7472e5c143d2` and `.tf` blob `42fee26095`. Any other ask hash or blob re-opens this
half.

## What I read

- **`git diff 0f5da21da8d9 42fee26095`, printed.**
  - The one functional line is `"s3:prefix" = ["*/silver/", "*/silver/*"]` becoming
    `flatten([for s in local.family_depth_sources : ["${s}/*/silver/", "${s}/*/silver/*"]])`.
  - The rest is the header comment.
  - `local.family_depth_sources` is the eight sources: schwab, orion, eclipse, blackdiamond, trueshares, pathfinder, msn
    and smartx.
- **The widening is NONE: it is a strict narrowing.**
  - Every new pattern `<s>/*/silver/...` is matched by the old `*/silver/...`, so the listable set after is a subset of
    the set before.
  - What stops being listable is a silver prefix under any other first component. The OG-cd-3 census found four:
    bloomberg, commonwealth, gateway and yahoo. A bronze-rooted `/silver/` shape stops too.
  - The other three statements are byte-equal.
- **Nothing the gateway runs through this policy loses a read.**
  - At the live ref, `family_depth.py` lists `<source>/<scope>/silver/` only for the sources in
    `app/refs/silver_families.json`.
  - That file is generated from `opal-assets/silver.tf` `local.silver_families`. Its source set is exactly the same
    eight: I read it at `6d1b5dcb64`, and `silver.tf:125-139` at HEAD agrees.
  - Phase B step 4's host read, equal to `FWD20_DRIVEN_READ.json`, is the served proof.
- **Process-wide state:** none, IAM only. That meets verdict 35844.
- **Rollback:** re-apply the two old globs, which is the state OG-cd-3 signed. The old hash prefix `2dd3ee621be1436d` is
  recorded.

## Noted, not grounds

**Two source lists that must agree, and one is typed by hand.**
- `family_depth_sources` in the IAM `.tf` is a hand-kept copy of a set that `family_depth.py` takes from a GENERATED file.
- A family added to `silver.tf` (Fidelity is the live candidate) would make the gateway list a silver prefix this grant
  no longer admits. The value would read `absent` with an AccessDenied reason, quietly, not as a failure.
- **Cheapest guard:** one test that asserts the `.tf` list equals the sources of `app/refs/silver_families.json`, or
  that derives the list from `silver.tf`'s `silver_sources`. It is an enrichment for the issuer's next round, not a
  condition here.

-- 3.0.0_SA_CVO~Z
