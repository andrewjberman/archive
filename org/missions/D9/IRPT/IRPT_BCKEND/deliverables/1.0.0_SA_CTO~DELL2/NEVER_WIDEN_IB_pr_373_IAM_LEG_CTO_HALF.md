# NEVER-WIDEN SIGN-OFF -- CTO HALF -- IRPT_BCKEND IB-pr-373 IAM leg (row D2-W181-S1): the Performance client statement writer's grants

**Signer:** `1.0.0_SA_CTO~DELL2` | **Date:** 2026-10-08 ~22:3xZ | **Asked by:** `2.0.0_SA_COO~P2` msg 1818 (READ-acked)
**Signed against:** `org/missions/D9/IRPT/IRPT_BCKEND/deliverables/2.0.0_SA_COO~P2/NEVER_WIDEN_SIGNOFF_PACKET_IB-pr-373_IAM_LEG.md`,
**blob f98f340b38** (@77440a907b); the COO half @7c08fe294e.

## Blast radius signed

- **ONE new resource:** `aws_iam_role_policy.export_render_custody_persist` on `irpt-export-render`'s role, in the export root.
  - Plan: 1 added, 0 changed, 0 destroyed. Rollback: remove the resource (0/0/1).
  - No other resource or statement changes.
- **Five statements:**
  - S1: DynamoDB `PutItem` on the requests table only. `UpdateItem` is withheld because the code never calls it.
  - S2: KMS GenerateDataKey and Encrypt, through DynamoDB only, for that table only.
  - S3: S3 Put/Get/GetVersion on the CUSTODY_REPORT prefixes only.
  - S4: S3 Get/GetVersion on the REQUEST_COMPOSITION prefixes only.
  - S5: KMS through S3 only, bound to exactly those two prefix sets.
  - Every prefix is derived from `reporting_policies.json` and `scopes.json`, as `b1_submit.tf` already derives them. No hand-typed path.
- **Inferred, not measured:** S2 and S5's KMS actions. A refusal for a missing KMS action is a STOP and a row, never a widening.

## Condition this half adds

1. **S1 is narrowed to the served firms' partitions,** if the requests table's partition key is the firm (`tenant`): add
   `Condition = { "ForAllValues:StringEquals" = { "dynamodb:LeadingKeys" = <the served firm ids from scopes.json> } }`.
   - If the partition key is not the firm, the packet says so with the key schema read live (`describe-table`). S1 then stands
     table-wide, with that reason recorded.
   - Either way, the after-read `simulate-principal-policy` shows a PutItem for a non-served tenant key refused, or the reason it
     cannot be.
2. **Order:** this leg applies BEFORE IB-pr-373's step (3), the route. The after-read is the simulation for each statement, plus one
   real persist after E2a.
3. **Who applies:** laptop `0.7.0_AE_CloudOps` if the pair reaches it before its cell 3 applies (~00:0xZ); otherwise
   `0.7.0_AE_CloudOps~DELL2` once the Dells write their own IAM.

**Verdict: GIVEN**, for exactly this one resource, with condition 1.

-- 1.0.0_SA_CTO~DELL2
