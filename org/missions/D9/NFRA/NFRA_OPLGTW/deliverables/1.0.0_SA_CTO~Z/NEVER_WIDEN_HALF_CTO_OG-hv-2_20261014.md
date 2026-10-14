# Never-widen half (CTO) -- OG-hv-2: the harvest read grant and the gateway release of harvest_list / harvest_read

By: `1.0.0_SA_CTO~Z`, 2026-10-14 ~13:3xZ. **SIGNED.**

**Against:** `deliverables/0.7.0_AE_CloudOps~Z/NEVER_WIDEN_ASK_OG-hv-2.md` @013844d3e6, read whole, sha256
`9283dd713e3fb121...` (the bytes the CVO half read; working tree equals the commit).

**Pinned to:** release `7c558b4e2176a632d13e6301af3e06d434aa1540` on base `90967e39ba4bdca17c6f84d9806c29cc67f8482e`;
grant file `infra/aws/terraform/opal-gateway/harvest_read_iam.tf` sha256 `52e2ed232924cb59...` @013844d3e6. A change to
any of the three is a new ask.

## Blast radius signed

| act | may touch | rollback per key |
|---|---|---|
| ACT 1 grant | CREATE inline policy `gateway-global-harvest-read-policy` on `gateway-global-internal-reader-role`; `-target=aws_iam_role_policy.int_reader_harvest_read` only (plan 1/0/0; the unapplied `market_update_gateway_put` must NOT ride) | `delete-role-policy` of that one name |
| ACT 2 deploy | install `7c558b4e21` on `i-07dccb1615503ac99`: 7 files, tools 63 -> 65 by the app registry | redeploy `90967e39ba` via `safe-ec2-deploy.sh` (host parity 105/105 measured) |

Order: ACT 1, then ACT 2. Both widenings are named: W1 (an Opal principal reads 24 served harvest prefixes, `raw/`
included, on Andrew's call 8) and W2 (the internal reader role's S3 read on `opal-data-harvest`).

## What this seat read before signing (~13:3xZ)

- **Role fix (my row-Z-S107 condition):** the grant targets `aws_iam_role.int_reader`; `aws_iam_role.gw` absent from the
  file. That is the role `harvest_read.py` assumes.
- **Live trust policy, `get-role gateway-global-internal-reader-role`:** exactly ONE statement, `Allow sts:AssumeRole`,
  Principal `role/opal-gateway-role`, no condition. W2 reaches no identity but the gateway instance role.
- **Grant file bounds:** 24 object ARNs under `opal-data-harvest/`; no bucket-wide `opal-data-harvest/*` ARN; actions in
  the file are exactly `s3:GetObject`, `s3:ListBucket` (+ the `s3:prefix` condition key); no Put, no Delete.
- **Both branches:** the ask's simulate row 3 (off-list prefix stays `implicitDeny` after ACT 1) is the bounded branch,
  row 1 the allowed branch, row 2 the same-principal positive control. Covered.
- **Writers of the property:** N = 2 inline-policy writers on the role, both read by the ask; the name is absent today,
  so ACT 1 is a CREATE.

## Conditions (same as the CVO half's, adopted)

1. The ask stays at its committed bytes (sha256 `9283dd71...`) through the GO.
2. AC2's served read runs through the INSTALLED code (a real `harvest_read` call), never an IAM simulate.

## Accepted risk, named

The Opal-only boundary is a code gate (`_is_opal_user`), not an IAM gate (ask section 6). Accepted: the principal is a
gateway identity IAM cannot see; `test_oghv1_ac02`/`ac04` and AC2's live negative arms hold it.
