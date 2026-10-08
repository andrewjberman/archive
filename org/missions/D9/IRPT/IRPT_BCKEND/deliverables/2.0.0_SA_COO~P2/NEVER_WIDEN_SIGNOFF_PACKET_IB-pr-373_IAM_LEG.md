# Never-widen sign-off packet -- IB-pr-373 IAM leg (row D2-W181-S1): irpt-export-render may persist a Performance client statement

**Prepared by:** `2.0.0_SA_COO~P2` (dell2), 2026-10-08 ~22:5xZ | **For:** `1.0.0_SA_CTO~DELL2` (CTO half, msg 1815) and laptop
`2.0.0_SA_COO~C` (applier routing, msg 1813) | **Parent pair:** IB-pr-373 (packet blob d7264acfc8; COO half @cb29ea67bd; CTO half
@ece42ad420, whose condition 2 makes this leg its own sign-off, owed before the route) | Nothing in this packet is applied.

## Why

The Performance client statement writer (code kind CUSTODY_REPORT) is live in `irpt-export-render` since IB-pr-374 (CodeSha256
`rNjtTwcm...`). The route `POST /api/scoped/investor-reporting/custody-report` is NOT applied. The function's role
(`aws_iam_role.export_render`) has no write to the requests table and no S3 write or read for the two families the persist touches.
So the persist fails CLOSED today. This leg grants exactly those calls.

**Measured call set (code at HEAD):**
- DynamoDB writes are `put_item` only, conditional: `reports/repository.py:437` (index publish) and `reports/retention.py:296` (retention
  reserve). There is no `update_item` and no transact call, so **UpdateItem is NOT granted.**
- The S3 blob store calls `put_object` and, to verify after the put, `get_object` on the CUSTODY_REPORT key. It reads the retained
  REQUEST_COMPOSITION artifact with `get_object`.
- DynamoDB `GetItem` and `kms:Decrypt` via DynamoDB on the requests table already exist (`export_render_submit`,
  `b1_submit.tf:57-72`) and are unchanged.

## Root, address and plan shape

- **Root:** `infra/aws/terraform/investor-reporting/export` (state `investor-reporting/export/tfstate`).
- **Address:** ONE new resource, `aws_iam_role_policy.export_render_custody_persist`, name `irpt-export-render-custody-persist-policy`,
  role `aws_iam_role.export_render.id`. It is a separate resource so that removing it is the whole rollback.
- **Plan shape:** `1 to add, 0 to change, 0 to destroy`, and only that address. Any other diff is a STOP.

## The exact statements (HCL, in the export root's own locals idiom; no ARN or prefix typed by hand)

Every ARN and prefix comes from the registry and outputs the root already reads (LGIC R-naming):
- the reporting bucket: `data.terraform_remote_state.core.outputs.reporting_bucket`;
- the table: `...outputs.tables.requests`;
- the KMS key: `...outputs.kms_key_arn`;
- the served firms: `local.b1_served_firms`, the three registry firms 49financial, cottonwood and inflection, spelled through
  `scopes.json`;
- the families: from `infra/logic/registry/reporting_policies.json`. CUSTODY_REPORT is in `irpt-custody-x10-v1` (ACTIVE): tier
  `platinum`, table `custody_reports`. REQUEST_COMPOSITION is in `irpt-x10-v1`: tier `state`, table `request_compositions`.

```hcl
locals {
  cp_custody_policy = one([for p in jsondecode(file("${path.module}/../../../../logic/registry/reporting_policies.json")).policies : p if p.policy_revision == "irpt-custody-x10-v1"])
  cp_custody_prefixes = [for firm in local.b1_served_firms :
    "arn:aws:s3:::${data.terraform_remote_state.core.outputs.reporting_bucket}/${local.cp_custody_policy.source}/${firm}/${local.cp_custody_policy.families["CUSTODY_REPORT"].tier}/${local.cp_custody_policy.families["CUSTODY_REPORT"].table}/*"]
  cp_composition_prefixes = [for firm in local.b1_served_firms :
    "arn:aws:s3:::${data.terraform_remote_state.core.outputs.reporting_bucket}/${local.b1_reporting_policy.source}/${firm}/${local.b1_reporting_policy.families["REQUEST_COMPOSITION"].tier}/${local.b1_reporting_policy.families["REQUEST_COMPOSITION"].table}/*"]
}

resource "aws_iam_role_policy" "export_render_custody_persist" {
  name = "irpt-export-render-custody-persist-policy"
  role = aws_iam_role.export_render.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      { Sid = "S1PutCustodyIndexAndRetentionRowsInServedFirmPartitions", Effect = "Allow",
        Action = ["dynamodb:PutItem"],
        Resource = ["arn:aws:dynamodb:${local.region}:${local.account_id}:table/${data.terraform_remote_state.core.outputs.tables.requests}"],
        Condition = { "ForAllValues:StringEquals" = { "dynamodb:LeadingKeys" = local.b1_served_firms } } },
      { Sid = "S2EncryptIndexWritesViaDynamoOnly", Effect = "Allow",
        Action = ["kms:GenerateDataKey", "kms:Encrypt"],
        Resource = [data.terraform_remote_state.core.outputs.kms_key_arn],
        Condition = { StringEquals = {
          "kms:ViaService" = "dynamodb.${local.region}.amazonaws.com"
          "kms:EncryptionContext:aws:dynamodb:tableName" = data.terraform_remote_state.core.outputs.tables.requests } } },
      { Sid = "S3WriteAndVerifyCustodyReportsOnly", Effect = "Allow",
        Action = ["s3:PutObject", "s3:GetObject", "s3:GetObjectVersion"],
        Resource = local.cp_custody_prefixes },
      { Sid = "S4ReadRetainedRequestCompositionsOnly", Effect = "Allow",
        Action = ["s3:GetObject", "s3:GetObjectVersion"],
        Resource = local.cp_composition_prefixes },
      { Sid = "S5KmsForThoseTwoPrefixesViaS3Only", Effect = "Allow",
        Action = ["kms:GenerateDataKey", "kms:Decrypt"],
        Resource = [data.terraform_remote_state.core.outputs.kms_key_arn],
        Condition = { StringEquals = { "kms:ViaService" = "s3.${local.region}.amazonaws.com" },
                      StringLike = { "kms:EncryptionContext:aws:s3:arn" = concat(local.cp_custody_prefixes, local.cp_composition_prefixes) } } }
    ]
  })
}
```

**What is inferred, not measured:** S2 (KMS on DynamoDB writes) and S5's `kms:GenerateDataKey` follow AWS SSE-KMS behaviour for a
customer-managed key. They are not yet exercised against this table or bucket. The applier's after-read 2 below is the measurement. If
a call is refused for a missing KMS action, that is a STOP and a row, never a widening.

## Rollback, per statement

The whole leg is one resource. Rollback is `terraform apply` with that resource removed from the root: plan
`0 to add, 0 to change, 1 to destroy`, address `aws_iam_role_policy.export_render_custody_persist` only. Per statement:
- S1 to S5 are removed together.
- None of them is referenced by any other statement or resource.
- No data is written by the IAM change itself.
- With the route unapplied, removing the policy returns the function to today's fail-closed state.

## Branch A (applied) and Branch B (rolled back)

- **A:** the role can PutItem only in the three served-firm partitions of `irpt-requests`. It can write and verify objects only under
  `irpt/<firm>/platinum/custody_reports/*`, read only under `irpt/<firm>/state/request_compositions/*`, and use the `irpt` key only via
  DynamoDB on that table or via S3 on those prefixes.
  - **No new principal.** The only caller of the persist remains the guarded Entry: Opal-only, owner server-derived (IB-pr-373).
  - **Nothing is reachable until the route applies,** which is a later order (CTO half condition 2).
- **B:** today's state. The persist fails closed; no grant to undo elsewhere.

## Writers of the changed property

The role's inline policies, written by Terraform in the export root only: one writer, `aws_iam_role_policy.export_render_custody_persist`.

## After-reads (by the applier)

1. **Plan and apply:** `1 to add, 0 to change, 0 to destroy`. A re-plan shows no changes.
2. **Policy simulation** (`aws iam simulate-principal-policy` on the role):
   - allowed: PutItem on `irpt-requests` with LeadingKeys `<firm>`; PutObject and GetObject under one served firm's custody_reports
     prefix; GetObject under its request_compositions prefix;
   - denied: PutItem with a non-served LeadingKey, PutObject under `performance_reports`, and any `UpdateItem`.
3. Live CodeSha256 of irpt-export-render is unchanged (`rNjtTwcm...`): the IAM leg moves no code.
