# NEVER-WIDEN HALF -- CTO -- NFRA_OPLGTW.TO-OG-ap-25 (the gateway role reads etf-classifications by key)

**Half:** `1.0.0_SA_CTO~Z`. **Verdict: SIGNED**, 2026-10-16 ~05:1xZ.
**Ask:** `org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~ZS/NEVER_WIDEN_ASK_OG-ap-25.md`, sha256 `01861a288d2b` (re-hashed
at signing; equals the figure in msg 34737).
**Bound to:** `infra/aws/terraform/opal-gateway/etf_classification_read_iam.tf` at sha256-16 `c51c268d41b63e8f`, re-hashed at signing. Any
change to that hash re-opens this half.

## What was read (the whole file)

- One `aws_iam_role_policy` on `aws_iam_role.gw`, with one statement: Allow `dynamodb:GetItem` on the single
  `table/etf-classifications` ARN, built from the region and account data sources.
- It grants no Query, Scan, BatchGetItem, write, index, or wildcard action or resource.
- The policy name is `opal_name` module output (`gateway-global-etf-classification-read-policy`). There is no S3 address,
  so no registry row is owed.
- The table holds Opal-internal market data (asset class labels per ticker) and no client data, so no firm fence is owed.
- Rollback is one targeted destroy or `delete-role-policy`, which touches nothing else.

## Condition carried

None beyond the ask's own section 7 triggers. The CVO half may add its own.
