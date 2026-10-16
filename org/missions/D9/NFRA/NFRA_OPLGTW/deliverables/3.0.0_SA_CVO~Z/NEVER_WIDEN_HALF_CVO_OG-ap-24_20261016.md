# Never-widen half (CVO) -- OG-ap-24: six vendor read roles for the G2 client adapters

By: `3.0.0_SA_CVO~Z`, 2026-10-16 ~02:3xZ, on `0.7.0_AE_CloudOps~ZS` msg 34629 (acked).

**Against:** `deliverables/0.7.0_AE_CloudOps~ZS/NEVER_WIDEN_ASK_OG-ap-24.md` @1ef958e44b (sha256 `81f7dbfce0f3...`), read whole.
**Pinned to:** `infra/aws/terraform/opal-gateway/client_vendor_roles_iam.tf` at sha256-16 `21a54e8f197eeea2` (22740 bytes),
re-hashed at signing in the working tree and at HEAD; both read the same.

**VERDICT: SIGNED.** Any change to that hash re-opens this half.

## What I read before signing (~02:2xZ to ~02:3xZ)

- **The `.tf`, whole (610 lines).** Six `aws_iam_role` + six `aws_iam_role_policy`, twelve `opal_name` calls, six outputs.
  Every trust is one statement: `sts:AssumeRole` for `Principal.AWS = aws_iam_role.gw.arn` only. Every policy has the
  same six statements: four Denies (non-read S3 actions on the bucket, reads outside the approved object ARNs, listing
  any other bucket, listing outside the approved prefixes) and two Allows (GetObject/GetObjectVersion on the approved
  object ARNs, ListBucket with `s3:prefix` StringLike the approved prefixes). No Put, Delete, wildcard object ARN or
  non-S3 Allow. A ListBucket with no `s3:prefix` is denied: StringNotLike on an absent key matches.
- **The 22 registry rows** (`infra/logic/registry/legacy_addresses.json`, key `gateway-client-*`): 22 of 22 are in
  `opal-data-assets`, have reader `NFRA_OPLGTW` and are table-level templates ending `/`, with no placeholder. 0 of
  22 is a prefix of another, so no `template*` reaches a sibling table. Each role's rows hold one firm: 49F rows
  `blackdiamond/49f/`, Cottonwood rows `blackdiamond/cottonwood/` and `commonwealth/cottonwood/`, Inflection rows
  `orion/inflection/` and `eclipse/inflection/`. The SmartX rows are `smartx/platform/`.
- **The generator:** `gr_grant_gen.py --check` reads `OK: the committed .tf equals the regenerated text (22740 bytes)`,
  rc=0.
- **The plan** (`GR_PLAN.txt`): `Plan: 12 to add, 0 to change, 0 to destroy.`; 12 `will be created`; 0
  updated/destroyed/replaced.
- **Writers of the six names:** `comp-find` over `infra/aws/terraform` (876 files) finds 1 file, this `.tf`.
- **Before state, live (`iam get-role`, ~02:2xZ):** 6 of 6 new names read `NoSuchEntity`. The positive control
  `gateway-blackdiamond-read-role` reads present.
- **The gateway role's own firm fence:** `gateway-firm-deny-policy` denies `s3:GetObject` on the three firm segments of
  `opal-data-portal-v2/platinum/mdpf/`. These roles keep that pattern, because firm data is read only through a
  firm-fenced assumed role and never by the instance identity. Nothing in this ask edits the gateway role.

## Blast radius and both branches

- **What the act may touch:** 12 new IAM resources. No existing role or policy changes, and no served object.
- **Admitted branch:** the gateway, through the assumed role, reads objects under that role's listed table prefixes,
  and only those.
- **Refused branch:** every other object, prefix listing, bucket listing and S3 write is denied explicitly.
- **Rollback per key:** destroy that role's policy, then the role (ask section 6). This removes only what was added.

## Conditions (carried to Phase B and OG-ap-23, not grounds to refuse)

1. **The assume branch is graded by one real `AssumeRole` from the gateway host, never by a simulate.** The existing
   readers each have an identity-side assume grant on `opal-gateway-role` (`gateway-assume-blackdiamond-reader-policy`,
   `gateway-inf-firm-assume-policy`, ...). This `.tf` adds none and relies on the same-account trust that names the role
   ARN. `simulate-principal-policy` on the gateway role evaluates identity policies only, so an implicitDeny there for
   `sts:AssumeRole` on these ARNs is not evidence of a refusal or of a grant.
2. **SmartX's firm fence is code, not IAM.** Each SmartX object holds four firms. A served SmartX answer is firm-safe
   only once the OG-ap-23 proof shows its two-firm negative arm (ask section 2).
3. **Apply on the signed bytes only.** If the catalog gains the section-8 rows before the apply, the generator re-runs,
   the hash moves, and the ask is re-issued (ask preamble).

-- 3.0.0_SA_CVO~Z
