```xml
<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-03-10-drfr-ptmch-cloudops-p1</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <date>2026-03-10</date>
    <status>pending</status>
    <thread_serial>DRFR_PTMCH-001</thread_serial>
    <thread_ref>org/threads/DRFR_PTMCH-001-portal-time-machine-ae-infrastructure-di/</thread_ref>
  </metadata>

  <objective>
    Phase 1 infrastructure prep for Portal Time Machine. S3 versioning is already enabled
    on both opal-data-portal-v2 and opal-data-bd (confirmed via CLI 2026-03-10). Phase 1
    now consists of: (1) adding lifecycle rules to bound version accumulation cost, (2)
    closing IAM gaps so opal-data-refresh-api can restore both layers, and (3) confirming
    CloudFront invalidation scope for BD data (does /api/public/* cover it or does
    /api/scoped/* require a separate invalidation?). No new S3 configuration is needed
    beyond lifecycle rules.
  </objective>

  <scope>
    <files>
      <file action="modify">infra/aws/terraform/shared-infra/main.tf</file>
      <file action="modify">infra/aws/terraform/yang-pipeline/iam.tf</file>
      <file action="create">org/tier2_senior/0.7.0_AE_CloudOps/deliverables/DRFR_PTMCH.001.cloudops-findings.md</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">
      LIFECYCLE RULES -- opal-data-portal-v2:
      Add a Terraform lifecycle configuration to the opal-data-portal-v2 bucket that
      expires noncurrent versions after 90 days and aborts incomplete multipart uploads
      after 7 days. This prevents unbounded version accumulation from weekly yang pipeline
      runs (~52 runs/year x 83 files = ~4,300 noncurrent versions/year without a rule).
      Target block in shared-infra Terraform (or wherever the bucket is defined).
      Use aws_s3_bucket_lifecycle_configuration resource if not already present.
    </requirement>

    <requirement id="2">
      LIFECYCLE RULES -- opal-data-bd:
      Same pattern as req 1 for opal-data-bd. BD gold pipeline runs ~daily, so version
      accumulation is higher (365 runs/year x ~80-100 files). 90-day expiry is the
      right bound. Add lifecycle rule alongside the opal-data-portal-v2 rule.
    </requirement>

    <requirement id="3">
      IAM GAP -- opal-data-refresh-api needs cross-bucket restore permissions:
      The yang-time-machine Lambda (to be built by OpalETL) will run under the
      opal-data-refresh-api role (or a new sibling role). It needs:
        - s3:GetObjectVersion on opal-data-portal-v2/* (for yang layer restore)
        - s3:CopyObject sourced from opal-data-portal-v2 (for CopySourceVersionId)
        - s3:PutObject on opal-data-portal-v2/json/* (for restored files)
      The bd-time-machine Lambda will need:
        - s3:ListObjectVersions on opal-data-bd/* (to find the correct version at target date)
        - s3:CopyObject sourced from opal-data-bd (for version restore)
        - s3:PutObject on opal-data-bd/gold/* (for restored files)
      Read infra/aws/terraform/yang-pipeline/iam.tf (current role) and
      infra/aws/lambda/data_refresh/lambda_function.py (current role name).
      Add any missing permission statements via Terraform. Deploy via terraform apply
      following the standard deployment protocol.
    </requirement>

    <requirement id="4">
      CLOUDFRONT INVALIDATION SCOPE -- confirm path coverage:
      Run: aws cloudfront get-distribution-config --id EVTSA9VEHNZVH
      List all behaviors and their origins. Determine:
        - Which path(s) serve opal-data-portal-v2/json/* ? (yang outputs -- invalidation needed)
        - Which path(s) serve opal-data-bd/gold/* ? (BD outputs -- /api/scoped/* ?)
        - Does /api/public/* alone cover yang data, or also BD data?
        - Does /api/scoped/advisor-intelligence/* need a separate invalidation for BD restore?
      Document as a table: path_pattern | origin_bucket | invalidation_path_needed.
      This output is consumed by OpalETL when building the portal-time-machine orchestrator Lambda.
    </requirement>

    <requirement id="5">
      FINDINGS DOCUMENT:
      Write org/tier2_senior/0.7.0_AE_CloudOps/deliverables/DRFR_PTMCH.001.cloudops-findings.md
      covering all 6 original task order requirements plus the CLI-confirmed facts:
        - Versioning: both buckets ENABLED (confirmed 2026-03-10)
        - Archive manifest health: 83 files, all versionIds non-null (exec 7a407b33)
        - DynamoDB PITR: ENABLED, 35-day window, earliest ~2026-02-13
        - Lifecycle rules: deployed in this task (reqs 1-2)
        - IAM gaps: documented and closed (req 3)
        - CloudFront invalidation scope: table from req 4
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">
      Lifecycle rules deployed on both buckets via Terraform (0-diff plan after apply).
      Noncurrent version expiry set to 90 days.
    </criterion>
    <criterion id="2">
      IAM role for time-machine Lambdas has all required S3 permissions on both
      opal-data-portal-v2 and opal-data-bd. Confirmed via terraform plan showing
      no drift after apply.
    </criterion>
    <criterion id="3">
      CloudFront invalidation scope documented as a table in the findings doc.
      OpalETL can read this and wire the correct invalidation paths into the
      portal-time-machine orchestrator.
    </criterion>
    <criterion id="4">
      Findings document complete at deliverables/DRFR_PTMCH.001.cloudops-findings.md.
    </criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Do NOT disable or suspend versioning on either bucket -- it is currently
    enabled and the Time Machine depends on it.</constraint>
    <constraint>Lifecycle rules must use noncurrentVersionExpiration, NOT Expiration --
    do not expire current versions.</constraint>
    <constraint>Follow standard Terraform deployment protocol: commit -> plan -> apply
    -> 0-diff -> tag -> push.</constraint>
    <constraint>Do NOT modify CloudFront config in this task -- req 4 is read-only audit.</constraint>
  </constraints>

  <dependencies>
    <dependency agent="DRFR_PTMCH-001" task="thread-receipt" status="complete"
      note="CLI facts confirmed by Andrew 2026-03-10: versioning enabled on both buckets,
      archive manifests healthy, PITR enabled."/>
  </dependencies>

  <deliverables>
    <deliverable type="commit">Terraform lifecycle rules deployed on opal-data-portal-v2 and opal-data-bd</deliverable>
    <deliverable type="commit">IAM permissions for time-machine roles added to yang-pipeline/iam.tf or equivalent</deliverable>
    <deliverable type="document">org/tier2_senior/0.7.0_AE_CloudOps/deliverables/DRFR_PTMCH.001.cloudops-findings.md</deliverable>
  </deliverables>
</task_order>
```
