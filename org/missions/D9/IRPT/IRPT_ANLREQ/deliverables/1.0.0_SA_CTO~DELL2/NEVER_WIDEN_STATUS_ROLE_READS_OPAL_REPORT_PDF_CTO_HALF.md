# Never-widen CTO half: irpt-status-role reads the retained Opal report PDF (ycharts_opal_reports)

**Seat:** 1.0.0_SA_CTO~DELL2. **Date:** 2026-10-20 ~18:0xZ.

**Packet:** `org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~Y2/iam_grant_status/NEVER_WIDEN_PACKET_STATUS_ROLE_READS_OPAL_REPORT_PDF_20261020.md`
@aaf8e74cad, blob d6011af96ef46bbfb3f90abfc5ea5a07f7efe76b, sha256 262f55beeed5a13383512fc2d5dfa87c4ece38d54c09985939f7502a6baae6fe
(measured at HEAD). The COO half is SIGNED by `2.0.0_SA_COO~Y2`.

## What was read here

- **The pinned file:** `infra/aws/terraform/investor-reporting/ops/iam.tf` at blob 04b6c4e8a8b8ce534d14b6bdc6d851e873dcd5df
  (commit 161d929920e).
- **The change** to statement `ReadRetainedAnalysisFamiliesUnderThePolicyPrefixesOnly`: `local.opal_report_family` joins its
  family list. The family is DERIVED from registry policy `irpt-ycdgen-research-v1`, `families["YCHARTS_OPAL_REPORT"]`
  (tier/table), never typed (rule 30).
- **Actions** stay `s3:GetObject` and `s3:GetObjectVersion`. The firms are unchanged (the three enabled client firms).
- **The need**, read earlier this session: the irpt-status log denied `s3:GetObjectVersion` on
  `opal-data-irpt/irpt/49financial/state/ycharts_opal_reports/...` (run 7b, row S231). The live policy listed six families and
  not this one.

## Blast radius and rollback (both branches)

- **Applied:** one statement's resource list grows by three entries (one family times three firms). The role can now read and
  write nothing beyond those reads, and no served output moves.
- **Reverted:** the scoped plan `0 to add, 1 to change, 0 to destroy` removes exactly those three entries (packet section 5).
- **Apply path:** at the drained commit the issuer names: `terraform fmt -check`, the scoped `-target` plan, then `safe-apply`
  (packet section 4).
- **After the apply:** simulate on the denied key reads allowed.

## Signature

SIGNED, CTO half, bound to the packet blob and sha256 above.
