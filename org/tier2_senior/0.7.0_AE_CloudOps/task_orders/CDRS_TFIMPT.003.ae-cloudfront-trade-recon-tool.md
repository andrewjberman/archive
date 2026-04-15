<task_order>
  <metadata>
    <id>0.7.0_AE_CloudOps-2026-04-15-cfimpt-rest-003-trade-recon</id>
    <issued_by>0.7.0_AE_CloudOps (self-authored from cloud inventory audit; trigger: Andrew direction 2026-04-15)</issued_by>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <date>2026-04-15</date>
    <status>complete</status>
    <project_code>CDRS_TFIMPT</project_code>
    <priority>P1 (sprint) -- adds API Gateway origin pattern</priority>
  </metadata>

  <references>
    <ref type="trigger">docs/analysis/2026-04-15_cloud_inventory_audit.md section 6b</ref>
    <ref type="precedent">CDRS_TFIMPT.001 + .002 establish the import pattern</ref>
  </references>

  <objective>
    Import CloudFront distribution **E2JC2OGK8LM1N7** ("Trade Reconciliation Tool")
    into Terraform state. Two origins:
    - API Gateway `77005oklok.execute-api.us-east-1.amazonaws.com` (`/prod`)
    - S3 `opal-trade-recon-ui` (default origin)
    Plus 1 additional cache behavior beyond default. No Lambda@Edge, no WAF, no alias.

    Trade-recon S3 buckets (`opal-trade-recon-confirms`, `opal-trade-recon-reports`,
    `opal-trade-recon-requests`) are already in trade-pipeline TF -- this distribution
    + opal-trade-recon-ui bucket join the same pipeline.
  </objective>

  <scope>
    <files>
      <file action="create">infra/aws/terraform/trade-pipeline/cloudfront-trade-recon.tf</file>
      <file action="create">infra/aws/terraform/trade-pipeline/s3-trade-recon-ui.tf</file>
    </files>
  </scope>

  <deliverables>
    <deliverable id="cf-import">
      1. `aws cloudfront get-distribution --id E2JC2OGK8LM1N7` -- capture full config including the second behavior.
      2. Identify the API Gateway resource (`77005oklok`) -- check if already in trade-pipeline TF as a `data` source or imported resource. If not, reference by domain name only (don't try to import the API GW in this TO).
      3. Write `aws_cloudfront_distribution.trade_recon` with 2 origins, 2 behaviors (default S3 + custom API GW path).
      4. Write `aws_s3_bucket.trade_recon_ui opal-trade-recon-ui`.
      5. Import both into trade-pipeline state.
      6. `terraform plan` -> 0-diff. The API GW origin's connection-attempts/timeout fields commonly differ between console and TF -- match TF to live.
      7. `terraform apply` (no-op).
      8. Tag `trade-pipeline-v{next}`.
    </deliverable>
  </deliverables>

  <acceptance_criteria>
    1. `terraform plan` 0-diff inside trade-pipeline.
    2. Both origins (S3 + API GW) preserved in TF resource.
    3. Both cache behaviors preserved.
    4. Tag pushed.
    5. Session log's Compiler Tools section reproduces each `<run>` + observed-result + pass/fail vs. `<expect>` (CTO Rule 7 locked 2026-04-15).
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step><run>aws cloudfront get-distribution --id E2JC2OGK8LM1N7 --query 'Distribution.DistributionConfig.{Origins:Origins,DefaultCacheBehavior:DefaultCacheBehavior,CacheBehaviors:CacheBehaviors}'</run><expect>Full origin + behavior config captured.</expect><if_mismatch>STOP. Surface the CLI error to COO; do not author TF against stale/guessed config.</if_mismatch></step>
      <step><run>grep -rln "77005oklok\|trade-recon" infra/aws/terraform/trade-pipeline/</run><expect>Determine if API GW is already TF-managed.</expect><if_mismatch>If API GW IS TF-managed, reference it via resource address (not domain_name string). If NOT managed, reference by domain_name only and note the deferral — do NOT attempt to import the API GW in this TO.</if_mismatch></step>
    </phase>
    <phase id="2" when="before commit">
      <step><run>terraform plan</run><expect>0-diff.</expect><if_mismatch>Edit TF to match live for every drift line; re-plan. Common drift: API GW origin connection-attempts/timeout. Do NOT apply a mutating plan. Surface to COO if a field cannot be represented.</if_mismatch></step>
    </phase>
    <phase id="3" when="after commit">
      <step><run>terraform plan</run><expect>0-diff.</expect><if_mismatch>Post-apply drift = incomplete import. STOP, capture delta, surface to COO; do NOT tag or mark complete.</if_mismatch></step>
    </phase>
  </compiler_tools_mandate>

  <dependencies>Sequence after .002 (same pipeline; avoid concurrent state edits).</dependencies>

  <closeout date="2026-04-15" commit="pending-on-commit">
    (a) Scope flex: single file `cloudfront-trade-recon.tf`; no separate `s3-trade-recon-ui.tf`.
    (b) Rationale: `aws_s3_bucket.trade_recon_ui` + versioning/SSE/PAB/website are already managed in `trade-pipeline/s3.tf:46-80`. Adding a duplicate S3 block would collide.
    (c) Original `<scope>` listed 2 files; substituted 1. Same pattern as .002 (COO ACK'd 18:23Z; no separate flag needed — extension of established pattern).
    API GW 77005oklok is NOT TF-managed; referenced by domain_name only (no import attempted, matching the TO's contingency plan in deliverable #2).
    Targeted `terraform plan` 0-diff post-apply (apply was tags_all metadata only, same as .001/.002).
  </closeout>

  <next>On complete: CDRS_TFIMPT.004 (Market Metrics CDN -- 2 S3 origins).</next>
</task_order>
