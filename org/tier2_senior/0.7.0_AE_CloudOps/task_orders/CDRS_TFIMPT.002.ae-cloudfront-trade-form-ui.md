<task_order>
  <metadata>
    <id>0.7.0_AE_CloudOps-2026-04-15-cfimpt-rest-002-trade-form-ui</id>
    <issued_by>0.7.0_AE_CloudOps (self-authored from cloud inventory audit; trigger: Andrew direction 2026-04-15)</issued_by>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <date>2026-04-15</date>
    <status>staged</status>
    <project_code>CDRS_TFIMPT</project_code>
    <priority>P1 (sprint) -- 2nd-easiest, same pattern as .001</priority>
  </metadata>

  <references>
    <ref type="trigger">docs/analysis/2026-04-15_cloud_inventory_audit.md section 6b</ref>
    <ref type="precedent">CDRS_TFIMPT.001 (Analytics Dashboard) and AUTH_TFIMPT.001 (portal)</ref>
    <ref type="related">trade-pipeline already has TF state; this distribution may belong there as a sibling resource OR a standalone module -- decide during scope.</ref>
  </references>

  <objective>
    Import CloudFront distribution **E2RNVVND8GSGG3** ("CloudFront distribution for opal-trade-form-ui")
    into Terraform state. Single S3 origin (opal-trade-form-ui), 1 default behavior,
    no Lambda@Edge, no WAF, no custom alias.

    Suggested TF home: add to `infra/aws/terraform/trade-pipeline/` as a new
    cloudfront.tf file (the trade-pipeline module already manages related trade
    resources). Bucket opal-trade-form-ui is also untracked -- import in same TO.
  </objective>

  <scope>
    <files>
      <file action="create">infra/aws/terraform/trade-pipeline/cloudfront-trade-form-ui.tf</file>
      <file action="create">infra/aws/terraform/trade-pipeline/s3-trade-form-ui.tf</file>
    </files>
  </scope>

  <deliverables>
    <deliverable id="cf-import">
      Same pattern as CDRS_TFIMPT.001:
      1. `aws cloudfront get-distribution --id E2RNVVND8GSGG3` -- capture config.
      2. `aws s3api get-bucket-policy --bucket opal-trade-form-ui`; capture website + CORS.
      3. Write `aws_s3_bucket.trade_form_ui` + `aws_cloudfront_distribution.trade_form_ui`.
      4. Import into trade-pipeline state (existing backend key: `trade-pipeline/tfstate`).
      5. `terraform plan` -> 0-diff.
      6. `terraform apply` (no-op).
      7. Tag `trade-pipeline-v{next}` per the pipeline-tag-versioning rule (run `git tag -l "trade-pipeline-v*" | sort -V | tail -3` first).
    </deliverable>
  </deliverables>

  <acceptance_criteria>
    1. `terraform plan` returns 0-diff inside trade-pipeline.
    2. CF + S3 resources both in trade-pipeline state.
    3. Tag pushed.
    4. pipeline_inventory.xml updated.
    5. Session log's Compiler Tools section reproduces each `<run>` + observed-result + pass/fail vs. `<expect>` (CTO Rule 7 locked 2026-04-15).
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step><run>aws cloudfront get-distribution --id E2RNVVND8GSGG3</run><expect>Live config captured.</expect><if_mismatch>STOP. Surface the CLI error to COO; do not author TF against stale/guessed config.</if_mismatch></step>
      <step><run>aws s3api get-bucket-policy --bucket opal-trade-form-ui</run><expect>Policy captured (or confirmed absent).</expect><if_mismatch>If error is anything other than NoSuchBucketPolicy (benign), STOP and surface to COO before authoring the S3 resource.</if_mismatch></step>
      <step><run>git tag -l "trade-pipeline-v*" | sort -V | tail -3</run><expect>Latest tag identified for next-version selection.</expect><if_mismatch>If no prior tags returned, confirm pipeline tag history with COO before selecting a version (do NOT guess).</if_mismatch></step>
    </phase>
    <phase id="2" when="before commit">
      <step><run>terraform plan</run><expect>0-diff.</expect><if_mismatch>Edit TF to match live for every drift line; re-plan. Do NOT apply a plan that mutates live config. If a field cannot be represented in TF, surface to COO before committing.</if_mismatch></step>
    </phase>
    <phase id="3" when="after commit">
      <step><run>terraform plan</run><expect>0-diff post-apply.</expect><if_mismatch>Post-apply drift = incomplete import. STOP, capture the delta, surface to COO; do NOT tag or mark complete.</if_mismatch></step>
    </phase>
  </compiler_tools_mandate>

  <dependencies>None functionally; sequence after .001 to reuse the import pattern + any module conventions established.</dependencies>

  <next>On complete: CDRS_TFIMPT.003 (Trade Reconciliation Tool -- adds API Gateway origin to the pattern).</next>
</task_order>
