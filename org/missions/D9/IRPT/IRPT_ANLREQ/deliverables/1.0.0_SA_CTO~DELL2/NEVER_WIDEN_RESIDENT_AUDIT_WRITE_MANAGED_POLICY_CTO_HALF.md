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

## RE-SIGN 2026-10-21 ~00:45Z (AR-y-481 re-pin; CTO ruling @88ae067327)

- **Packet:** git blob `9f065fb2a59b247318d8144c754c7bd024419121` (commit 8dff583d11), sha256 `89cfbff5dedd90b289b5582218b5695bc2db593092daacfe0af55570de57af60`.
- **Pins, read at HEAD:** resident.tf `2e9a61e656141c8a5194fa942312c0d7aef843a8`; resident_audit_policy.tf `0e084af9b8868f3949127dc7543751ac7204229a`. The old pins f0df570515 and aa565f1c42 are VOID.
- **What the diff shows:**
  - resident_audit_policy.tf changes one comment line only.
  - resident.tf adds the local `resident_audit_policy`, which selects irpt-anlreq-audit-x10-v1, and the audit prefixes now build from that row.
- **Measured equal:** the new row's source (irpt), its ANALYSIS_AUDIT family (platinum, analysis_audit, ceiling 2555, unreferenced null) and its firms (49financial, cottonwood, inflection) equal those of the r34o-era row. So the rendered ARNs and the policy document are unchanged, and the blast radius and rollback above stand.
- **Order:** after r34p is live and after TCKT_VNEXT.TO-R22-DL1 is terminal (one IAM apply at a time). The row flips to ACTIVE, with enforcement_ref = the commit recording this apply, before any audit row is reserved. Shipping that ACTIVE row to the resident is a later release under its own pair.

RE-SIGNED, CTO half, bound to blob 9f065fb2a5 and the sha256 above. The earlier signature on blob b2e2c58200 is superseded.
