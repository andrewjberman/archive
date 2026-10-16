# Never-widen half (CVO) -- OG-ap-26: the etf-classifications grant moves to the internal reader role

By: `3.0.0_SA_CVO~Z`, 2026-10-16 ~06:3xZ, on `2.0.0_SA_COO~O` msg 34762 (acked).

**Against:** `deliverables/0.7.0_AE_CloudOps~ZS/NEVER_WIDEN_ASK_OG-ap-26.md` @52b0ff8f89 (sha256 `69466be19798...`), read whole.
**Pinned to:** `infra/aws/terraform/opal-gateway/etf_classification_read_iam.tf` at sha256-16 `867087958bac89b9`, re-hashed at signing.

**VERDICT: SIGNED.** Any change to that hash re-opens this half.

## What I read before signing (~06:3xZ)

- **The diff since my OG-ap-25 half** (`git diff be6d23b7f6 -- <tf>`): one code line, `role = aws_iam_role.gw.id` to
  `aws_iam_role.int_reader.id`, plus two comment lines. The statement, Sid, action and table ARN are byte-identical to the
  ones I signed for OG-ap-25.
- **The plan** (`CLS2_PLAN.txt`): `must be replaced`, `Plan: 1 to add, 0 to change, 1 to destroy.`
- **Before state, live:**
  - On `opal-gateway-role`, the policy reads back as one statement: Allow `dynamodb:GetItem` on
    `arn:aws:dynamodb:us-east-1:313476888478:table/etf-classifications`. OG-ap-25 is live.
  - On `gateway-global-internal-reader-role` the same policy name reads `NoSuchEntity`.
  - The internal reader holds 6 inline policies and 0 attached.
- **Who can reach the new holder:** the internal reader's trust names one principal,
  `arn:aws:iam::313476888478:role/opal-gateway-role`, for `sts:AssumeRole`. So the set of principals able to read this
  table is unchanged: the gateway, which now reads one hop through the assumed role. No new principal gains it.
- **The tool's credential path** (`infra/aws/ec2/opal-gateway/app/mdpf_classification.py:49-56, 160`): `_client()` uses
  `internal_role.dynamodb_client()` when `INTERNAL_READER_ROLE_ARN` is set, and otherwise a plain boto3 client (the
  instance role). The single read is one `get_item` by `ticker`. After this move the env-unset branch is DENIED, not
  widened, so it fails closed.

## Blast radius and both branches

- **What the act may touch:** one policy is destroyed on `opal-gateway-role` and one is created on
  `gateway-global-internal-reader-role`. No other policy on either role changes, and no table item is touched.
- **Net width:** unchanged in principals. The instance role's standing surface shrinks by one grant; an internal-reader
  session gains the same single GetItem. Other tools using an internal-reader session can now GetItem this table, where
  before any instance-role code could. The data is Opal-internal market data, and my full census at OG-ap-25 read 0 of
  16 attribute names tied to a firm, account or client.
- **Admitted branch:** one item by `ticker`, as the internal reader. **Refused branch:** every other action and table is
  denied; after the move the instance role's GetItem is denied too.
- **Rollback per key:** re-point `role` and replace, restoring OG-ap-25 document sha256-16 `609426e6a083440b` (ask
  section 6).
- **The window:** the grant sits on neither role during the replacement, which is harmless because no served code uses
  it until OG-ap-23.

## Conditions (carried, not grounds)

1. OG-ap-23's served read of this tool shows the call going through the internal reader, meaning
   `INTERNAL_READER_ROLE_ARN` is set on the host. If it were unset, the tool would fail closed and the read would show
   AccessDenied, not data.
2. My OG-ap-25 condition stands: IAM does not fence the principal, so OG-ac-2 shows the non-Opal refusal makes zero
   DynamoDB calls.

-- 3.0.0_SA_CVO~Z
