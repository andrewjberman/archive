<task_order>
  <metadata>
    <id>0.7.0_AE_CloudOps-2026-04-15-cfimpt-rest-001-analytics</id>
    <issued_by>0.7.0_AE_CloudOps (self-authored from cloud inventory audit; trigger: Andrew direction 2026-04-15)</issued_by>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <date>2026-04-15</date>
    <status>staged</status>
    <project_code>CFIMPT_REST</project_code>
    <priority>P1 (sprint) -- easiest of 5 console-only CloudFront distributions</priority>
  </metadata>

  <references>
    <ref type="trigger">docs/analysis/2026-04-15_cloud_inventory_audit.md section 6b</ref>
    <ref type="precedent">org/tier2_senior/0.7.0_AE_CloudOps/task_orders/AUTH_TFIMPT.001.ae-cloudfront-distribution-import.md (EVTSA9VEHNZVH portal import, 2026-04-06)</ref>
    <ref type="memory">memory/feedback_cloudfront_oac_no_s3_origin_config.md (omit s3_origin_config{} on OAC origins after import)</ref>
  </references>

  <objective>
    Import CloudFront distribution **EF3ZZO0F4UDHH** ("Opal Analytics Dashboard")
    into Terraform state. Lightest lift of the 5 remaining console-only distributions:
    single S3 origin (opal-analytics-dashboard), 1 default behavior, no Lambda@Edge,
    no WAF, no custom alias.

    Suggested TF home: new module `infra/aws/terraform/analytics-dashboard/`
    (the bucket is also untracked; bundle the S3 + CF import into one module).
  </objective>

  <scope>
    <files>
      <file action="create">infra/aws/terraform/analytics-dashboard/main.tf</file>
      <file action="create">infra/aws/terraform/analytics-dashboard/variables.tf</file>
      <file action="create">infra/aws/terraform/analytics-dashboard/cloudfront.tf</file>
      <file action="create">infra/aws/terraform/analytics-dashboard/s3.tf</file>
    </files>
  </scope>

  <deliverables>
    <deliverable id="cf-import">
      Follow the AUTH_TFIMPT.001 pattern:
      1. `aws cloudfront get-distribution --id EF3ZZO0F4UDHH` -- capture full config.
      2. `aws s3api get-bucket-policy --bucket opal-analytics-dashboard` and `get-bucket-website` -- capture S3 setup.
      3. Write `aws_s3_bucket.dashboard` + `aws_cloudfront_distribution.dashboard` resources matching live config exactly.
      4. State backend: `analytics-dashboard/tfstate` in `opal-313476888478-terraform-state`.
      5. `terraform init` then import:
         - `aws_s3_bucket.dashboard opal-analytics-dashboard`
         - `aws_cloudfront_distribution.dashboard EF3ZZO0F4UDHH`
      6. `terraform plan` -> 0-diff. Fix any drift by editing TF to match live, NOT by letting TF change live.
      7. `terraform apply` (no-op).
      8. Tag `analytics-dashboard-v1.0.0` on the import commit; push --follow-tags.
    </deliverable>
  </deliverables>

  <acceptance_criteria>
    1. `terraform plan` returns "No changes. Infrastructure is up-to-date."
    2. `aws_cloudfront_distribution.dashboard` resource ID = EF3ZZO0F4UDHH in state.
    3. `aws_s3_bucket.dashboard` resource ID = opal-analytics-dashboard in state.
    4. Tag `analytics-dashboard-v1.0.0` exists and pushed.
    5. `pipeline_inventory.xml` updated.
    6. README "Known Issues" + cloud inventory report counts decremented.
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step><run>aws cloudfront get-distribution --id EF3ZZO0F4UDHH</run><expect>Full live config captured.</expect></step>
      <step><run>aws s3api get-bucket-policy --bucket opal-analytics-dashboard 2>/dev/null; aws s3api get-bucket-website --bucket opal-analytics-dashboard 2>/dev/null</run><expect>Bucket policy + website config captured (or confirmed absent).</expect></step>
    </phase>
    <phase id="2" when="before commit">
      <step><run>terraform plan</run><expect>0-diff. Resolve every drift by editing TF, not by letting TF mutate live.</expect></step>
    </phase>
    <phase id="3" when="after commit">
      <step><run>terraform plan</run><expect>Still 0-diff post-apply.</expect></step>
    </phase>
  </compiler_tools_mandate>

  <dependencies>None. Standalone import.</dependencies>

  <next>On complete: pick CFIMPT_REST.002 (Trade Form UI -- next-easiest, same pattern).</next>
</task_order>
