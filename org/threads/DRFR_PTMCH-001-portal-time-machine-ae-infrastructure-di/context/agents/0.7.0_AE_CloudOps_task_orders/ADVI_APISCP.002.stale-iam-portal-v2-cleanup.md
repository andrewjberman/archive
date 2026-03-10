<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-03-10-stale-iam-portal-v2-cleanup</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <date>2026-03-10</date>
    <status>pending</status>
    <phase>2</phase>
  </metadata>

  <objective>
    Remove the stale IAM permission that grants the BD pipeline role s3:PutObject on
    opal-data-portal-v2/*. This permission is a remnant of the eliminated copy-to-portal
    anti-pattern. No active BD pipeline code writes to opal-data-portal-v2 (confirmed by
    0.6.0_AE_PartnerETL audit in Phase 1). Removing it enforces the bucket separation
    invariant at the IAM level.
  </objective>

  <scope>
    <files>
      <file action="modify">infra/aws/terraform/bd-pipeline/iam.tf</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">
      Remove the PortalBucketWrite IAM statement from bd-pipeline/iam.tf (lines 371-376):

        {
          Sid    = "PortalBucketWrite"
          Effect = "Allow"
          Action = "s3:PutObject"
          Resource = "arn:aws:s3:::opal-data-portal-v2/*"
        }

      This is the ONLY change needed. Do not modify any other IAM statements.
    </requirement>
    <requirement id="2">
      Run terraform plan for bd-pipeline. Verify the plan shows ONLY the IAM policy
      update (one in-place change to the role policy). No other resources should be affected.
    </requirement>
    <requirement id="3">
      Run terraform apply. Verify 0-diff plan after apply.
    </requirement>
    <requirement id="4">
      Tag the deployment: check latest bd-pipeline tag with
      git tag -l "bd-v*" | sort -V | tail -5, then tag appropriately.
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">PortalBucketWrite statement removed from iam.tf</criterion>
    <criterion id="2">0-diff terraform plan after apply</criterion>
    <criterion id="3">BD pipeline still functions (no writes to portal-v2 were active)</criterion>
    <criterion id="4">Deployment tagged per protocol</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Follow CLAUDE.md deployment protocol: commit before apply, tag after apply.</constraint>
    <constraint>This is a Terraform change. Use .tools/terraform.exe with MSYS_NO_PATHCONV=1.</constraint>
    <constraint>Do NOT remove any other IAM permissions. Only the PortalBucketWrite statement.</constraint>
  </constraints>

  <dependencies>
    <!-- No blocking dependencies. Phase 1 audit confirmed no active code uses this permission. -->
  </dependencies>

  <references>
    <ref type="audit">0.6.0_AE_PartnerETL Phase 1 audit (commit c3820bb1) — confirmed zero active writes to portal-v2</ref>
    <ref type="prd">docs/architecture/ADVI_APISCP_PRD.md (compliance rule section 2)</ref>
  </references>

  <deliverables>
    <deliverable type="commit">iam.tf with PortalBucketWrite removed</deliverable>
    <deliverable type="tag">bd-pipeline deployment tag</deliverable>
    <deliverable type="document">Session log with terraform plan/apply output</deliverable>
  </deliverables>
</task_order>
