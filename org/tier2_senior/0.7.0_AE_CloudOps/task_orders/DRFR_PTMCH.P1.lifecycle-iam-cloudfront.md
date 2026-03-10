```xml
<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-03-10-drfr-ptmch-cloudops-p1</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <date>2026-03-10</date>
    <status>complete</status>
    <thread_serial>DRFR_PTMCH-001</thread_serial>
    <thread_ref>org/threads/DRFR_PTMCH-001-portal-time-machine-ae-infrastructure-di/</thread_ref>
    <revised>2026-03-10 -- REVISED post agent review. IAM scope reduced: each pipeline AE owns
    their own IAM. CloudOps P1 is now lifecycle rules + CloudFront audit only. Two deploys:
    shared-infra-v1.3.0 (lifecycle) and read-only CF audit.</revised>
  </metadata>

  <objective>
    Phase 1 infrastructure prep for Portal Time Machine -- scoped to CloudOps domain only.
    S3 versioning is already enabled on both opal-data-portal-v2 and opal-data-bd (confirmed
    via CLI 2026-03-10). IAM work is REMOVED from this task order -- each pipeline AE owns
    their own IAM (OpalETL adds yang-pipeline-lambda-role permissions in P2; PartnerETL adds
    BD Lambda roles in P3; data-refresh invoke permission goes in P2 alongside data-refresh TF).
    CloudOps P1 is: (1) lifecycle rules on both buckets, (2) CloudFront invalidation scope audit.
    That is the complete scope.
  </objective>

  <scope>
    <files>
      <file action="modify">infra/aws/terraform/shared-infra/main.tf</file>
      <file action="create">org/tier2_senior/0.7.0_AE_CloudOps/deliverables/DRFR_PTMCH.001.cloudops-findings.md</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">
      LIFECYCLE RULES -- opal-data-portal-v2:
      Add aws_s3_bucket_lifecycle_configuration to shared-infra/main.tf referencing the bucket
      by name (bucket = "opal-data-portal-v2"). The bucket is NOT imported into Terraform -- that
      is fine. Terraform can manage a lifecycle configuration on a bucket without owning the
      aws_s3_bucket resource.
      Rules:
        - noncurrentVersionExpiration: noncurrent_days = 90
        - AbortIncompleteMultipartUpload: days_after_initiation = 7
      Do NOT add an Expiration rule. Do NOT expire current versions.
    </requirement>

    <requirement id="2">
      LIFECYCLE RULES -- opal-data-bd:
      Same pattern as req 1, bucket = "opal-data-bd".
      BD gold pipeline runs more frequently than yang (approximately daily). 90-day noncurrent
      expiry is the right bound. Add alongside the portal-v2 rule in the same Terraform resource
      block or as a second resource.
    </requirement>

    <requirement id="3">
      CLOUDFRONT INVALIDATION SCOPE -- read-only audit:
      Run: aws cloudfront get-distribution-config --id EVTSA9VEHNZVH
      List all behaviors and their origins. Produce a table:
        path_pattern | target_origin_id | origin_bucket | invalidation_path_for_time_machine
      Specifically answer:
        - Which path serves opal-data-portal-v2/json/* content? (yang outputs)
        - Which path serves opal-data-bd/gold/* content? (BD advisor intelligence data)
        - Confirm: does the current rollback invalidation (/api/public/*) cover yang outputs?
        - Confirm: does BD data serve under /api/scoped/* requiring a SEPARATE invalidation?
      This table is consumed by OpalETL (yang-time-machine Lambda, req 6 of P2) and
      PartnerETL (bd-time-machine Lambda, req 2 of P3) for hardcoding their CloudFront
      invalidation paths. OpalETL and PartnerETL are blocked on this output before they
      can finalize their Lambda invalidation calls.
      Do NOT modify any CloudFront config. Read-only.
    </requirement>

    <requirement id="4">
      FINDINGS DOCUMENT:
      Write org/tier2_senior/0.7.0_AE_CloudOps/deliverables/DRFR_PTMCH.001.cloudops-findings.md
      covering:
        - Versioning status: both buckets ENABLED (confirmed 2026-03-10 via CLI)
        - Archive manifest health: 83 files, all versionIds non-null (exec 7a407b33, 2026-03-08)
        - DynamoDB PITR: ENABLED on opal-portal-market-data, 35-day window, earliest ~2026-02-13
        - Lifecycle rules: deployed in this task (reqs 1-2), tags applied
        - IAM: explicitly OUT OF SCOPE for CloudOps P1 -- each pipeline AE owns their IAM
        - CloudFront invalidation scope: the table from req 3
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">
      Lifecycle rules deployed on both buckets via terraform apply on shared-infra.
      0-diff plan after apply. Tag: shared-infra-v1.3.0. Pushed with --follow-tags.
    </criterion>
    <criterion id="2">
      CloudFront invalidation scope table present in findings doc with confirmed path
      patterns for both yang outputs (/api/public/* or equivalent) and BD data
      (/api/scoped/* or equivalent). Table must be grounded in get-distribution-config output.
    </criterion>
    <criterion id="3">
      Findings document complete at deliverables/DRFR_PTMCH.001.cloudops-findings.md.
    </criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>IAM is NOT in scope for this task order. Do not modify any IAM roles or
    policies. Each pipeline AE owns their own Lambda execution role permissions.</constraint>
    <constraint>Do NOT import the S3 bucket resources into Terraform. Reference by name only
    in lifecycle configuration resources.</constraint>
    <constraint>Lifecycle rules must use noncurrentVersionExpiration only. Do NOT use
    Expiration (do not expire current versions).</constraint>
    <constraint>CloudFront audit is read-only. Do NOT modify the distribution config.</constraint>
    <constraint>Standard deployment protocol for shared-infra: commit -> plan -> apply ->
    0-diff -> tag shared-infra-v1.3.0 -> push --follow-tags.</constraint>
  </constraints>

  <answers_to_agent_questions>
    <answer id="Q1">IAM file correction confirmed. Do NOT put time-machine IAM in yang-pipeline/iam.tf
    or data-refresh/main.tf from this task order. Each pipeline AE owns their IAM:
    OpalETL adds to yang-pipeline/iam.tf in P2; PartnerETL adds new roles in bd-pipeline in P3.</answer>
    <answer id="Q2">Lifecycle placement confirmed: shared-infra/main.tf as standalone
    aws_s3_bucket_lifecycle_configuration resources referencing buckets by name. Correct call.</answer>
    <answer id="Q3">opal-data-bd write scope: gold/* is the correct boundary. Do not scope tighter.</answer>
  </answers_to_agent_questions>

  <dependencies>
    <dependency agent="DRFR_PTMCH-001" task="thread-receipt" status="complete"
      note="CLI facts confirmed by Andrew 2026-03-10."/>
  </dependencies>

  <deliverables>
    <deliverable type="commit">Lifecycle rules deployed on both buckets via shared-infra Terraform. Tag: shared-infra-v1.3.0.</deliverable>
    <deliverable type="document">org/tier2_senior/0.7.0_AE_CloudOps/deliverables/DRFR_PTMCH.001.cloudops-findings.md with CloudFront invalidation scope table.</deliverable>
  </deliverables>
</task_order>
```
