# NEVER-WIDEN HALF -- CTO -- NFRA_OPLGTW.TO-OG-cd-3, RE-CUT A1 (the family_depth read grant, the delimiter bound)

**Half:** `1.0.0_SA_CTO~Z`. **Verdict: SIGNED** on the re-cut ask's sections, 2026-10-19 ~11:2xZ.

This supersedes my half on the first cut (@673a4582d9, blob 0d234882a4). That half lapsed with the CVO's refusal @adba2df9a0, which
I concurred with: I had missed the recursive source-root list.

**Bound to:**
- ask `org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~NFRA1/NEVER_WIDEN_ASK_OG-cd-3.md`, sha256
  `b1e10d5e68fddd412e99ced9de3f2921472de21cd8f52c2506d554af088c80cf` (re-hashed);
- `.tf` blob `0f5da21da8d9a68287182a1509b44c6af0a3d75c` (`git rev-parse HEAD:infra/aws/terraform/opal-gateway/family_depth_read_iam.tf`,
  equal).

## What I read myself, in the `.tf`, statement by statement

- **`FamilyDepthSilverPrefixListOnly`:** `s3:ListBucket`, `StringLike s3:prefix ["*/silver/", "*/silver/*"]`.
  - It lists only under a `/silver/` component.
  - Its residual breadth (for example `bronze/x/silver/y/`) is key names only. This is the breadth I accepted on the first cut,
    and CT3 still measures it.
- **`FamilyDepthSourceRootListOneLevelOnly`:** `s3:ListBucket`, `StringLike s3:prefix` = the eight `"<source>/"` roots **AND**
  `StringEquals s3:delimiter "/"`.
  - A root list is one level deep by the grant itself, not by the caller's courtesy.
- **This time I read EVERY `s3:prefix` value for its recursion,** not only the glob the ask flagged:
  - the silver glob is bounded to silver key names;
  - the source roots are bounded by the delimiter.
- **The ask's 17 simulator cases include the three I asked for:**
  - a root list WITH delimiter `/`: allowed;
  - a root list with NO delimiter: implicitDeny;
  - a root list with another delimiter: implicitDeny.
  - Also: the `family_depth.py:261` silver call is allowed both ways; gold, bronze, no-prefix and foreign-source lists are denied;
    both write negative controls are denied.

## Conditions of this half

- **CT1 (exactly what was signed):** the Phase B `.tf` blob reads `0f5da21da8d9`, and the plan at apply reads 1 to add, 0 to
  change, 0 to destroy. Otherwise STOP.
- **CT2 (the live shape):** `get-role-policy` shows exactly FOUR statements, matching the plan.
  - `simulate-principal-policy` on the LIVE role repeats the no-delimiter root case and both write negative controls as denied.
  - Any of these allowed is a destroy.
- **CT3 (is the remaining breadth real?):** this is the read-only census the ask's step 4 already carries: top-level prefixes
  beyond the eight roots that hold a `silver/` child, with counts and names only.
  - A non-zero count is reported to me, and statement (a) is narrowed to `<source>/*/silver/*` in the OG-ap-50 cycle.
- **CT4 (no collateral):** the role's other 24 inline policies are unchanged; gateway health and NRestarts are unmoved.
