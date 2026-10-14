# Never-widen half (CVO) -- OG-hv-2: the harvest read grant and the gateway release of harvest_list / harvest_read

By: `3.0.0_SA_CVO~Z`, 2026-10-14 ~13:3xZ. Heads-up from `2.0.0_SA_COO~O` msg 34046 (acked); amendment A5 @ff91700f3b on
this seat's row Z-S107.

**Against:** `deliverables/0.7.0_AE_CloudOps~Z/NEVER_WIDEN_ASK_OG-hv-2.md`, read whole. It was UNCOMMITTED when read, so
this half binds to its bytes: sha256 `9283dd713e3fb121...`.

**Pinned to:**
- the release `7c558b4e2176a632d13e6301af3e06d434aa1540` on base `90967e39ba4bdca17c6f84d9806c29cc67f8482e`;
- the grant file `infra/aws/terraform/opal-gateway/harvest_read_iam.tf`, sha256 `52e2ed232924cb59...` (uncommitted when
  read).

A change to any of these three is a new ask.

## What I read before signing (this seat's own reads, ~13:2xZ)

- **The release diff:** `git diff --stat 90967e39ba 7c558b4e21` reads 7 files, +450 -4: harvest_read.py, test_og_hv1.py,
  tools.py, destructive_ops.py, data_entitlement.py and the two count tests. That is the ask's list.
  - `harvest_read.py` at the release is byte-equal to box/sitez HEAD.
  - It reads S3 through `internal_role.s3_client()`, the assumed `INTERNAL_READER_ROLE_ARN`. That is the Z-S107
    premise, and the grant now targets it.
- **The grant file:**
  - ONE `aws_iam_role_policy` "int_reader_harvest_read", named `gateway-global-harvest-read-policy`, on
    `aws_iam_role.int_reader`.
  - Actions in the whole file: `s3:GetObject`, `s3:ListBucket`, and the condition key `s3:prefix`. Nothing else.
  - The 24 object-ARN prefixes equal `SERVED_PREFIXES` parsed from the release's `harvest_read.py`, 24 of 24.
  - No bucket-wide `opal-data-harvest/*` ARN.
- **Live, before:**
  - `gateway-global-internal-reader-role` holds 1 inline policy (`gateway-global-internal-reader-policy`) and 0
    attached.
  - Its trust policy names only `opal-gateway-role`, both in Terraform (`mcpmsp_internal_reader.tf:34-40`) and live.
  - Both that role and opal-gateway-role read implicitDeny on `opal-data-harvest` (simulated at Z-S107, ~12:2xZ).
  - EC2_MANIFEST `deployed_commit` 90967e39ba is the base.

## SIGNED: what is newly reachable, and by whom

**W1, the reach.** An Opal principal, through `harvest_list` and `harvest_read`, can read `s3://opal-data-harvest`
under the 24 top-level prefixes, `raw/` included. Andrew's call 8 is "available for opal users only for now, which will
be managed via opalgateway entitlements". The 24 are the list v4 that call 8 widened to. The width is his.

**W2, the role.** `gateway-global-internal-reader-role` gains `s3:GetObject` on those 24 prefixes, plus `s3:ListBucket`
conditioned on them. Its only assumer is opal-gateway-role. No other identity in the account gains anything, and
opal-gateway-role is not widened.

**Both branches, read from IAM's rules rather than predicted:**
- Admitted: an Opal principal on a served prefix gets one listing page, or one object capped at 4 MB.
- Refused before any S3 call:
  - no principal: `principal_required`;
  - not Opal: `harvest_opal_only`;
  - off-list, or `..`: `harvest_prefix_not_served`.
- After ACT 1, an off-list key (`zzz-not-served/`) stays implicitDeny at IAM. That is the bound that makes the grant
  finite.

**The Opal-only boundary is a code gate (`_is_opal_user`), not an IAM gate.** I accept this as the ask states it.
Andrew's own words put the boundary at "opalgateway entitlements". An AWS condition cannot name a gateway identity.
Release tests and AC2's live negative arms hold it.

**Research-only.** The two tools are in `NATIVE_TOOLS` and `SAFE_TOOLS`, not `DATA_GRANT_TOOLS`. The same principal
stays refused every `schwab_*` tool and `blackdiamond_list_fees` (test_oghv1_ac05, test_ogpf1_ac01). PRD v2.8's
research-only arm holds.

**Order and rollback, as signed:**
1. ACT 1, the grant, targeted at the one resource. The untargeted directory also carries OG-mu-1's unapplied
   `market_update_gateway_put`, and the `-target` is part of what is signed.
2. THEN ACT 2, the deploy.

Rollback per act: `delete-role-policy` of the one new name (the existing portal-read policy has a different name and is
never touched), and a redeploy of 90967e39ba (105 of 105 files measured equal to the host).

## Conditions on this half

1. **The served read (AC2 step 7) must run THROUGH THE INSTALLED CODE under an Opal principal.** That means
   `opal_packs_read` True with a byte count. An IAM simulate is not that read: it graded the wrong principal once, which
   is Z-S107. The ACT 2 triggers do not include a served read, so if step 7 fails after the deploy, that is a rollback
   trigger, and an ARMED row names `2.0.0_SA_COO~O`.
2. **The ask must be committed at these bytes** (sha256 9283dd713e3fb121) before the issuer's GO cites this half.

-- 3.0.0_SA_CVO~Z
