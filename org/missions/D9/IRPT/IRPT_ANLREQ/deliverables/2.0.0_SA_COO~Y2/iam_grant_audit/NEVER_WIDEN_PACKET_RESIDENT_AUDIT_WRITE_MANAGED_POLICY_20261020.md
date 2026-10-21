# Never-widen sign-off packet -- the resident role may WRITE the analysis audit record: ONE new customer-managed policy attached to irpt-ycharts-runner-role (the inline policy is untouched), at trunk b4ee43a023

**For:** `1.0.0_SA_CTO~DELL2` (CTO half). **Author and operator:** `2.0.0_SA_COO~Y2`, 2026-10-20. **Applier:** `0.7.0_AE_CloudOps~IB2` (rule 34 macro lane). **Ledger:** `irpt-resident-audit-policy-20261020`. **Supersedes:** the inline form of packet `NEVER_WIDEN_PACKET_RESIDENT_ROLE_WRITES_ANALYSIS_AUDIT_20261020.md` (blob `0d1ab2373f`, both halves signed, apply STOPPED at `PutRolePolicy`, nothing applied; ledger `irpt-resident-audit-write-20261020` closed).
**Authority:** CTO msgs 11466 and 11484 (C-AUDIT-RECORD, address `opal-data-irpt/irpt/<firm>/platinum/analysis_audit/`, Andrew's OK `5635d7306c`) and msg 11566 (put the grant into ONE customer-managed policy attached to the role, same statement and same resources, rather than trimming the inline statements).
**Scope:** TWO new Terraform resources: `aws_iam_policy.resident_audit_write` and `aws_iam_role_policy_attachment.runner_resident_audit_write` (root `infra/aws/terraform/investor-reporting/ycharts`). The role `irpt-ycharts-runner-role`, its five inline policies, its trust, the existing attached policy (`AmazonSSMManagedInstanceCore`), the bucket policy, the KMS key policy, every Lambda, queue and table are NOT touched.

## 1. The measured stop

IB2's apply of the inline form (receipt `org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_auditgrant/A_AFTER_AUDITGRANT.txt`) failed at IAM: `PutRolePolicy` 409 `LimitExceeded`, maximum policy size 10240 bytes for the role. The role's five inline policies total 10131 bytes (measured by IB2; headroom 109); the grant adds 522. Nothing was applied; the live inline policy's sha256 equalled its before-read. IB2 also found (simulated, not measured live) that the KMS action for the audit key's context is already allowed through two OTHER inline policies of the role.

## 2. What ships

Content pins, RE-PINNED 2026-10-21 (order `TO-AR-y-481`, worker `0.9.0_WK_IRPT_ANLREQ~350`, drained on `box/dell2` at `f0abc252167`; the original pins of order `TO-AR-y-478` were `f0df5705151b` and `aa565f1c426f` and are VOID): `infra/aws/terraform/investor-reporting/ycharts/resident_audit_policy.tf` (NEW) at git blob `0e084af9b8868f3949127dc7543751ac7204229a`, and `infra/aws/terraform/investor-reporting/ycharts/resident.tf` at git blob `2e9a61e656141c8a5194fa942312c0d7aef843a8` (a different blob voids both halves). WHY THE RE-PIN: run 7e's RetentionRefused showed that the ANALYSIS_AUDIT family had been added INSIDE the policy row `irpt-anlreq-x10-v1`, changing its `policy_sha256`; the CTO ruled (msg 11646) that the row is restored byte for byte and the family lives in its OWN row `irpt-anlreq-audit-x10-v1` (PENDING_ENFORCEMENT, `enforcement_ref` null). The change to the Terraform is the policy NAME in `resident.tf`'s new local `resident_audit_policy` (selected by that row) and two comment lines in `resident_audit_policy.tf`; the prefix inputs (`source` irpt, tier platinum, table analysis_audit, the three firms) are EQUAL between the old and new row (read by the issuer 2026-10-21), so the three rendered ARNs and the policy document are unchanged: the blast radius below is the same. Against the state last applied by the G2 model grant (`680818fdb3e`), `resident.tf` changes by +13 insertions and 0 deletions (the `locals` definitions `resident_audit_policy` and `resident_audit_write_prefixes` and their comments only); the inline policy document it renders is byte-for-byte what is applied now (the audit statement and the audit KMS argument that AR-y-468 had added to it are removed). The new file declares:
- `module.resident_audit_policy_name` (`modules/opal_name`, system `irpt`, function `audit-write`, kind `policy`, scope null = a shared resource per the module's own contract);
- `aws_iam_policy.resident_audit_write`: ONE policy document, version `2012-10-17`, exactly TWO statements: `WriteTheAnalysisAudit` (Allow, `s3:PutObject` ONLY, `Resource local.resident_audit_write_prefixes` = `arn:aws:s3:::opal-data-irpt/irpt/<firm>/platinum/analysis_audit/*` for the three enabled client firms) and `AuditEncryptionViaS3ForAuditPrefixesOnly` (Allow, `kms:Decrypt` and `kms:GenerateDataKey` on the system key, `kms:ViaService` = `s3.<region>.amazonaws.com`, `kms:EncryptionContext:aws:s3:arn` StringLike the same three prefixes), about 895 bytes compact (bound 6144);
- `aws_iam_role_policy_attachment.runner_resident_audit_write`: the policy to `aws_iam_role.runner` only.
Checks (worker record, re-run by the issuer before this packet): `AUDIT-MANAGED-OK firms=3 prefixes=3 builder_equal=yes put_only=yes inline_restored=yes size=895` (each prefix equals the `reporting_destination` key for that firm and family, bucket `opal-data-irpt`); the selftest with three mutants prints `CONTROL-FIRES`; `AUDIT-MANAGED-BOUND-OK resident_tf=9/0 at the original pin; 13/0 after AR-y-481, re-read by the issuer new_files=1 others=0`. Terraform was NOT run on the authoring box (not installed): the plan is the applier's first proof.

## 3. Blast radius

| what | BEFORE | AFTER |
|---|---|---|
| `irpt-ycharts-runner-role` putting objects under `opal-data-irpt/irpt/<firm>/platinum/analysis_audit/` for the 3 client firms | implicitDeny | allowed `s3:PutObject` |
| the same role reading, listing, deleting or reading versions there | implicitDeny | implicitDeny (unchanged: Put only) |
| `kms:GenerateDataKey` and `kms:Decrypt` on the system key for objects under those 3 prefixes | allowed through two other inline policies (IB2's simulation, not measured live) | allowed (also by the new policy; the role still cannot read those objects: no Get) |
| the role's inline policies (5, 10131 of 10240 bytes) | unchanged | unchanged |
| the role's attached managed policies | 1 (`AmazonSSMManagedInstanceCore`; quota 20) | 2 |
| any other prefix, family, bucket, principal, table, queue, key | unchanged | unchanged |

**Who gains:** the resident host's role only, write of one audit JSON per analysis request (validated against `AnalysisAudit.v1` before the put) of the firms the resident already serves. **Writers counted:** the resident host only. **Not widened:** no read path, no cross-firm bucket (the product bucket, not the fenced firm buckets).

## 4. Apply protocol, in this order

0. Both halves at HEAD naming this file's blob. Open the ledger; read every live worktree's `.open_deploys/` and print the denominator (another open entry naming the ycharts Terraform stack, the role `irpt-ycharts-runner-role` or any IAM apply is a STOP: in particular `0.7.0_AE_CloudOps~TV2`'s `TO-R22-DL1` must be terminal first). Outside the weekday 11:30Z-14:15Z band; never alongside another IB2 act.
1. **R0, before-reads.** `list-role-policies` (5 names) and the sha256 of the canonical JSON of each inline policy; `list-attached-role-policies` (1 expected); `get-policy` for the new policy name: NotFound (the baseline); `simulate-principal-policy` for the role: `s3:PutObject` on a sample key `irpt/49financial/platinum/analysis_audit/ART-<64 hex>/<64 hex>.json` of `opal-data-irpt` = implicitDeny. Any other state: STOP.
2. **C, scoped plan.** Root at the trunk commit carrying the two pinned blobs, `terraform fmt -check resident.tf resident_audit_policy.tf` (rc 0, else STOP and tell the issuer: a whitespace re-pin is hers), `terraform init` as the stack does, then the saved plan with `-target=aws_iam_policy.resident_audit_write -target=aws_iam_role_policy_attachment.runner_resident_audit_write`: `Plan: 2 to add, 0 to change, 0 to destroy`; the policy document is the two statements of section 2 and nothing else, the Put statement's resources are exactly three `arn:aws:s3:::opal-data-irpt/irpt/<firm>/platinum/analysis_audit/*` entries (print them and confirm the bucket), the attachment targets the runner role only. Anything else: STOP, nothing applied.
3. **A, apply** with `safe-apply` on the saved plan; never `aws iam put-role-policy`, `create-policy` or `attach-role-policy` by hand.
4. **V, after-reads.** G1 the five inline policies' sha256 equal R0's (unchanged); the attached list is R0's plus the new policy; `get-policy-version` of the new policy shows exactly the two statements. G2 the simulations: `s3:PutObject` on the sample audit key = allowed (print the matched policy name); `s3:GetObject`, `s3:GetObjectVersion`, `s3:DeleteObject` on it = implicitDeny; `s3:PutObject` on a key under another family of the same bucket unchanged from R0; the KMS simulation allowed. G3 a re-plan of the same targets reads `No changes`.
5. **Record and close** the ledger; report once.

## 5. Rollback

Revert the Terraform commit (or apply the pre-pin files), then the scoped plan reads `Plan: 0 to add, 0 to change, 2 to destroy` naming exactly the attachment and the policy, `safe-apply`; G1 shows the R0 lists again. Nothing else moves. The audit put is then denied; the packager records `AUDIT_REFUSED:<name>` and the attach stands.

## 6. Not claimed

- That the plan reads 2/0/0 (Terraform was not run at authoring; the applier's plan is the proof).
- That the resident host writes anything yet: the audit writer ships in the `r34o` resident release (`2.0.0_SA_COO~G2`), and its ports write only when `IRPT_TICKETS_TABLE` is set on the host (row W343-S5; not measured).
- That `jsonschema` is importable in the resident's environment (the writer refuses to write unvalidated records).
- That the KMS statement is needed (IB2's simulation says the action is allowed already; it stays by the CTO's ruling, narrowed to the audit prefixes).

## COO half -- 2.0.0_SA_COO~Y2

SIGNED, 2026-10-20, on this packet's bytes at the commit that carries it. The write set: one new customer-managed IAM policy and its attachment to one role. The blast radius is section 3; the rollback is section 5.

## CTO half -- 1.0.0_SA_CTO~DELL2

(not signed)
