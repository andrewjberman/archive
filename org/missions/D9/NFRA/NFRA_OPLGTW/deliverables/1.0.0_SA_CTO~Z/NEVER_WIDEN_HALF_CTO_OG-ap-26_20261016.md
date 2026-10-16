# NEVER-WIDEN HALF -- CTO -- NFRA_OPLGTW.TO-OG-ap-26 (the etf-classifications grant moves to the internal reader role)

**Half:** `1.0.0_SA_CTO~Z`. **Verdict: SIGNED**, 2026-10-16 ~06:3xZ.
**Ask:** `org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~ZS/NEVER_WIDEN_ASK_OG-ap-26.md`, sha256 `69466be19798` (re-hashed at
signing; equals the figure in msg 34761).
**Bound to:** `infra/aws/terraform/opal-gateway/etf_classification_read_iam.tf` at sha256-16 `867087958bac89b9`, re-hashed at signing.

## What was read

- **The diff against the version this seat signed for OG-ap-25** (@9fc726f92a, sha16 `c51c268d41b63e8f`) is one attachment line,
  `role = aws_iam_role.gw.id` becoming `role = aws_iam_role.int_reader.id`, plus comments. The statement is unchanged: Allow
  `dynamodb:GetItem` on the one `table/etf-classifications` ARN.
- **`aws_iam_role.int_reader`** (`mcpmsp_internal_reader.tf:32-42`) is assumable ONLY by `aws_iam_role.gw.arn`.
- **The net effect narrows.** The instance role loses the grant, and the internal reader gains it. The internal reader is
  the role that holds only Opal-internal reads, and the table is Opal-internal market data with no client data. PRD v3.12
  item 5 (client data never via the internal reader) is not engaged.
- **Plan:** 1 add, 0 change, 1 destroy. The destroy removes the OG-ap-25 attachment, if it was applied, from the instance role.

## Condition carried

The CVO's OG-ap-25 condition carries unchanged: OG-ac-2 proves that a non-Opal refusal makes zero DynamoDB calls.
