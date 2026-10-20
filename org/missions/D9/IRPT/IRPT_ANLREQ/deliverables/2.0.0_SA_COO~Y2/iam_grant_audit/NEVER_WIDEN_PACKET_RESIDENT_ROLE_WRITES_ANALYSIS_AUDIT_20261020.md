# Never-widen sign-off packet -- the resident role may WRITE the analysis audit record: one Put-only statement added and the KMS context line extended on irpt-ycharts-runner-role, at resident.tf blob efa98ea249

**For:** `1.0.0_SA_CTO~DELL2` (CTO half). **Author and operator:** `2.0.0_SA_COO~Y2`, 2026-10-20. **Applier:** `0.7.0_AE_CloudOps~IB2` (rule 34 macro lane). **Ledger:** `irpt-resident-audit-write-20261020`.
**Authority:** CTO msgs 11466 and 11484 (C-AUDIT-RECORD: a platinum `ANALYSIS_AUDIT` family written by the packager at attach, address `opal-data-irpt/irpt/<firm>/platinum/analysis_audit/`, Andrew's OK recorded at `5635d7306c`). Grounding: AR-y-467 and AR-y-469 (the validating writer and its live wiring) are on the trunk and ship in the resident release r34o; without this grant the writer's put is denied.
**Scope:** ONE Terraform resource changes: `aws_iam_role_policy.runner_resident` (inline policy `irpt-ycharts-runner-resident-policy` on the role `irpt-ycharts-runner-role`, root `infra/aws/terraform/investor-reporting/ycharts`). One new statement; ONE existing line (the KMS encryption-context list) gains one argument. No new role, no trust change, no other statement, no bucket policy, no KMS key policy, no Lambda, no queue, no table, no resident host change.

## 1. The measured gap

The resident host's role carries `s3:PutObject` only on the families of `resident_write_prefixes` and the Opal report prefixes; none names `platinum/analysis_audit`. The reporting bucket `opal-data-irpt` is `aws:kms` with the system key `7f4d3042-...` (read live by the issuer, 2026-10-20 ~18:3xZ), so a put also needs `kms:GenerateDataKey`, which the role's statement `ReportEncryptionViaS3ForResidentFamiliesOnly` allows only for objects whose `kms:EncryptionContext:aws:s3:arn` matches `concat(local.resident_write_prefixes, local.resident_read_prefixes, local.ycdgen_opal_report_prefixes)`. The audit prefixes are in neither.

## 2. What ships

Content pin: `infra/aws/terraform/investor-reporting/ycharts/resident.tf` at git blob `efa98ea24952190f827ae6fe4df0f0b0f2a0a118` (trunk, `box/dell2` at `2423309988e`; worker `0.9.0_WK_IRPT_ANLREQ~342`, order `TO-AR-y-468`, edit commits `6f38e71fc3e`, `3f0b44d5b11`, `ebd5c881a24`, drained `2ff88544d1d`; a different blob voids both halves). Against the state last applied by the G2 model grant (`680818fdb3e`) the file changes by +19 insertions and -1 deletion, which is exactly:
- a local `resident_audit_write_prefixes`: one entry per client firm of `local.resident_scopes`, `arn:aws:s3:::<resident_bucket>/<source>/<firm long>/<tier>/<table>/*` for family `ANALYSIS_AUDIT` (tier `platinum`, table `analysis_audit`) of policy `irpt-anlreq-x10-v1`, no typed bucket, firm, tier or table;
- ONE statement after `ReadTheAnalysisCommentaryDraft`: `Sid WriteTheAnalysisAudit`, `Effect Allow`, `Action ["s3:PutObject"]` only, `Resource local.resident_audit_write_prefixes`;
- the one KMS line: `local.resident_audit_write_prefixes` appended as the fourth argument of the `concat(...)` in `ReportEncryptionViaS3ForResidentFamiliesOnly` (the single deleted line is its old form).
Checks (worker record, re-run by the issuer before this packet): `AUDIT-WRITE-GRANT-OK firms=3 prefixes=3 builder_equal=yes put_only=yes` (each prefix equals the key the naming builder `reporting_destination` gives for that firm and family); the selftest with three mutants prints `CONTROL-FIRES`; `AUDIT-WRITE-BOUND-OK numstat=19/1 files=1` against the trunk commit `5143b9b2565`. Terraform was NOT run on the authoring box (not installed): the plan is the applier's first proof.

## 3. Blast radius

| what | BEFORE | AFTER |
|---|---|---|
| `irpt-ycharts-runner-role` putting objects under `opal-data-irpt/irpt/<firm>/platinum/analysis_audit/` for the 3 client firms | implicitDeny | allowed `s3:PutObject` |
| the same role reading, listing, deleting or reading versions there | implicitDeny | implicitDeny (unchanged: Put only) |
| `kms:GenerateDataKey` and `kms:Decrypt` on the system key for objects whose S3 ARN is under those 3 prefixes | not matched by the condition list | matched (the role still cannot read those objects: no Get) |
| any other prefix, family, bucket, principal, table, queue, key | unchanged | unchanged |

**Who gains:** the resident host's role only, write of one audit JSON per analysis request (validated against `AnalysisAudit.v1` before the put), of the firms the resident already serves. The record holds ticket id and type, the form as filed (the ticket answers), the filer's principal id (and a nullable user type), and the package and commentary pointers; no uploaded file content. The prefixes are in the product bucket, not the fenced firm buckets (Andrew's OK `5635d7306c`). **Writers counted:** the resident host only. **Not widened:** no read path, no cross-firm bucket.

## 4. Apply protocol, in this order

0. Both halves at HEAD naming this file's blob. Open the ledger; read every live worktree's `.open_deploys/` and print the denominator (another open entry naming the ycharts Terraform stack, the role `irpt-ycharts-runner-role` or its policy is a STOP). Outside the weekday 11:30Z-14:15Z band; never alongside another IB2 act (in particular not inside the `r34o` install window of `2.0.0_SA_COO~G2`).
1. **R0, before-reads.** `get-role-policy` of `irpt-ycharts-runner-resident-policy`: record the statement ids (expected to include `ReadTheAnalysisCommentaryDraft` and the model-source read; not `WriteTheAnalysisAudit`), the `ReportEncryptionViaS3ForResidentFamiliesOnly` condition list length, and the sha256 of the canonical document; `simulate-principal-policy` for the role: `s3:PutObject` on a sample key `irpt/49financial/platinum/analysis_audit/ART-<64 hex>/<64 hex>.json` of `opal-data-irpt` = implicitDeny (the baseline). Any other state: STOP.
2. **C, scoped plan.** Root at the trunk commit carrying the pinned blob, `terraform fmt -check resident.tf` first (rc 0, else STOP and tell the issuer: a whitespace re-pin is hers), then `-target=aws_iam_role_policy.runner_resident`: `Plan: 0 to add, 1 to change, 0 to destroy`; the diff of the `policy` attribute adds exactly the one statement `WriteTheAnalysisAudit` and three resource entries to the KMS condition list, and changes nothing else. Anything else: STOP, nothing applied.
3. **A, apply** with `safe-apply` on the saved plan; never `aws iam put-role-policy`.
4. **V, after-reads.** G1 `get-role-policy`: the statement ids are the R0 ids plus `WriteTheAnalysisAudit`; every statement other than the new one and `ReportEncryptionViaS3ForResidentFamiliesOnly` is byte-equal to R0's; the KMS statement differs from R0's only by its condition list gaining the three audit prefixes. G2 the simulation: `s3:PutObject` on the sample audit key = allowed (print the matched statement id), `s3:GetObject`, `s3:GetObjectVersion`, `s3:DeleteObject` on it = implicitDeny, and `s3:PutObject` on a key under another family of the same bucket unchanged from R0. G3 re-plan reads `No changes`.
5. **Record and close** the ledger; report once.

## 5. Rollback

Revert the Terraform commit (or apply the pre-pin `resident.tf`), scoped plan `0 to add, 1 to change, 0 to destroy` removing exactly the statement and the three KMS entries, `safe-apply`, G1 shows the R0 statement ids again. Nothing else moves. The audit put is then denied again; the packager records the audit failure in its own outcome vocabulary and the attach stands (the design of AR-y-467, tested offline; not measured live).

## 6. Not claimed

- That the plan reads 0/1/0 (Terraform was not run at authoring; the applier's plan is the proof).
- That the resident host writes anything yet: the audit writer ships in the `r34o` resident release (`2.0.0_SA_COO~G2`), and the ports write only when `IRPT_TICKETS_TABLE` is set on the host (row W343-S5; not measured).
- That the KMS context entries are matched by the S3 object ARN form the service sends (the existing entries rely on the same form; the first real write is the proof).
- That `jsonschema` is importable in the resident's environment (the writer refuses to write unvalidated records).

## COO half -- 2.0.0_SA_COO~Y2

SIGNED, 2026-10-20, on this packet's bytes at the commit that carries it. The write set: one IAM inline policy of one role (one statement added; one condition list extended by three entries). The blast radius is section 3; the rollback is section 5.

## CTO half -- 1.0.0_SA_CTO~DELL2

(not signed)
