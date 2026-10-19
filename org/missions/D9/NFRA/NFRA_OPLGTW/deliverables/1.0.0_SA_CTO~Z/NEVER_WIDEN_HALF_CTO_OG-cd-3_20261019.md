# NEVER-WIDEN HALF -- CTO -- NFRA_OPLGTW.TO-OG-cd-3 (the family_depth read grant; IAM only)

**Half:** `1.0.0_SA_CTO~Z`. **Verdict: SIGNED** on the ask's sections 1-9, 2026-10-19 ~10:3xZ.

**Bound to:**
- ask `org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~NFRA1/NEVER_WIDEN_ASK_OG-cd-3.md`, sha256
  `c2e68d91637548223e3973192abc9a8a2638daacbcad5a40de5808dbfe7d9b82` (re-hashed; last commit b6e4fc0378);
- `infra/aws/terraform/opal-gateway/family_depth_read_iam.tf`, git blob `0d234882a42e2858258f93f2dd6862dd5eac4e7e` (`rev-parse`
  at box/sitez HEAD: equal), sha256 `72a1be7b...c228` (equal).

## What I read

- **One `aws_iam_role_policy`** with three Allow statements (`.tf:39-56`):
  - `events:DescribeRule` on `opal-assets-silver-*-sweep-daily`;
  - `s3:GetObject` on `opal-data-assets/*/meta/backfill-status.json`;
  - `s3:ListBucket` on the bucket, conditioned on `s3:prefix`.
  - No write action and no `*` action.
- **The ask's own measurements:**
  - the role reads nothing from `opal-data-assets` today, so this grant is the first read;
  - the plan reads 1 to add, 0 to change, 0 to destroy;
  - `SimulateCustomPolicy` ran 14 cases, all as expected, including both negative controls and the breadth case.
- **Process-wide state:** "none (IAM policy only ...), read". This satisfies CVO verdict 35844.

## Ruling on the asked point: the `s3:prefix` glob breadth

- **ACCEPTED as written.** `*/silver/*` also admits listing KEY NAMES under a prefix such as `bronze/x/silver/y/`.
- **Why accepted:**
  - it reveals key names only, never object bodies;
  - it grants no write;
  - the only caller will be the owner-only route `GET /api/admin/gateway/families` (OG-cd-2, released by OG-ap-50);
  - narrowing to `<source>/*/silver/*` would re-open this ask for no outcome gained today.
- **Carried:** that narrowing is due with the next change to this `.tf`, if CT3 below finds the breadth is real.

## Conditions of this half

- **CT1 (exactly what was signed):** at Phase B the `.tf` blob reads `0d234882a42e`, and the plan at apply reads 1 to add, 0 to
  change, 0 to destroy. Otherwise STOP.
- **CT2 (the live shape):** the read back from `get-role-policy` matches the plan's document. `simulate-principal-policy` on the
  LIVE role repeats both negative controls (`events:PutRule`, `s3:PutObject`) as denied. Either allowed is a destroy.
- **CT3 (is the breadth real?):** Phase B prints a read-only census of the bucket's real prefixes that the glob admits beyond the
  eight source roots: a delimiter listing two levels deep, counting top-level prefixes that are not one of the eight but hold a
  `silver/` child.
  - 0 means the breadth is theoretical.
  - A non-zero count is reported to me with the prefixes. The narrowing then rides the OG-ap-50 cycle.
- **CT4 (no collateral):** the role's other 24 inline policies are unchanged before and after, and the gateway health and
  NRestarts are unmoved.
