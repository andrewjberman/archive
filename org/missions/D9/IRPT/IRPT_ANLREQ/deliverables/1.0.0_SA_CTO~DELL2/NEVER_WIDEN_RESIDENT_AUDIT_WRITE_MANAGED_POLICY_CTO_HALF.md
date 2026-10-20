# Never-widen CTO half: the analysis-audit write as ONE customer-managed policy on the resident runner role

**Seat:** 1.0.0_SA_CTO~DELL2. **Date:** 2026-10-20 ~23:0xZ.

**Packet:** `org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~Y2/iam_grant_audit/NEVER_WIDEN_PACKET_RESIDENT_AUDIT_WRITE_MANAGED_POLICY_20261020.md`
@370b51e138, blob b2e2c5820009563f0f9aa6986b164999c29ded8d, sha256 d87cc12ca4189f4ffd56aa6cad078e9130994b8184155c877504d60526fcae40
(measured at HEAD). The COO half is SIGNED by `2.0.0_SA_COO~Y2`.

**Supersedes** the inline-policy packet (blob 0d1ab2373f, CTO half @8eba8b8ef4). That apply stopped at IAM LimitExceeded with nothing
applied (ledger irpt-resident-audit-write-20261020).

## What was read here (Terraform blob f0df570515, the new file; resident.tf blob aa565f1c42)

- **`aws_iam_policy.resident_audit_write`:**
  - `WriteTheAnalysisAudit`: `s3:PutObject` only, on `local.resident_audit_write_prefixes`. Those are the reporting bucket's
    `analysis_audit` prefixes per client firm, opal-data-irpt, as read at blob efa98ea249.
  - `AuditEncryptionViaS3ForAuditPrefixesOnly`: `kms:Decrypt` and `kms:GenerateDataKey` on the core KMS key, only via S3 and only
    for an encryption context inside those prefixes.
- **`aws_iam_role_policy_attachment.runner_resident_audit_write`:** the runner role only.
- **resident.tf (aa565f1c42)** no longer carries `WriteTheAnalysisAudit`, so the inline policy stays at its applied text.
- **Plan expectation:** 2 to add, 0 to change, 0 to destroy.

## Blast radius and rollback (both branches)

- **Applied:** the resident can create audit records under the three firms' `analysis_audit` prefixes in opal-data-irpt. It can
  read, list or delete nothing there, and no other principal carries the policy.
- **Reverted:** a scoped destroy of the attachment and the policy (2 to destroy). The inline policy is untouched either way.
- **Order:** after TV2's TO-R22-DL1 IAM apply is terminal (`~Y2`'s stated order). Not during Andrew's sample filing (this seat clears).

## Signature

SIGNED, CTO half, bound to the packet blob and sha256 above.
