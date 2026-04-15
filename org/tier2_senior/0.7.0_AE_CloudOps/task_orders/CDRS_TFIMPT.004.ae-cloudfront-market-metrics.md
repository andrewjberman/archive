<task_order>
  <metadata>
    <id>0.7.0_AE_CloudOps-2026-04-15-cfimpt-rest-004-market-metrics</id>
    <issued_by>0.7.0_AE_CloudOps (self-authored from cloud inventory audit; trigger: Andrew direction 2026-04-15)</issued_by>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <date>2026-04-15</date>
    <status>staged</status>
    <project_code>CDRS_TFIMPT</project_code>
    <priority>P1 (sprint) -- two S3 origins, market-overview pipeline</priority>
  </metadata>

  <references>
    <ref type="trigger">docs/analysis/2026-04-15_cloud_inventory_audit.md section 6b</ref>
    <ref type="precedent">CDRS_TFIMPT.001..003 establish the pattern</ref>
    <ref type="iam">infra/aws/terraform/market-overview/* already references E2LPCXXBLDGWXY in IAM grants for invalidation -- distribution is referenced but not resource-managed</ref>
  </references>

  <objective>
    Import CloudFront distribution **E2LPCXXBLDGWXY** ("Opal Capital Market Metrics CDN")
    into Terraform state. Two S3 origins:
    - `opal-data-portal-v2.s3.us-east-1.amazonaws.com` (origin id `S3-opal-data-portal`)
    - `opal-market-data-v2.s3.us-east-1.amazonaws.com` with origin path `/metrics` (default origin, id `S3-opal-data-market-yf`)
    1 additional cache behavior beyond default. No L@E, no WAF, no alias.

    TF home: `infra/aws/terraform/market-overview/` (existing module) or new
    `cloudfront/market-metrics.tf` file inside it. The buckets opal-data-portal-v2
    and opal-market-data-v2 are referenced elsewhere -- decide whether to import
    them too in this TO or defer (recommend defer to a separate "S3 import wave"
    TO so this stays focused on CF).
  </objective>

  <scope>
    <files>
      <file action="create">infra/aws/terraform/market-overview/cloudfront-market-metrics.tf</file>
      <file action="read">infra/aws/terraform/market-overview/iam.tf (or wherever the EF3...invalidation grant lives)</file>
    </files>
  </scope>

  <deliverables>
    <deliverable id="cf-import">
      1. `aws cloudfront get-distribution --id E2LPCXXBLDGWXY` -- full config.
      2. Verify the live `OriginPath` on the second origin (`/metrics`) matches what TF resource will declare.
      3. Write `aws_cloudfront_distribution.market_metrics` with 2 origins + 2 behaviors.
      4. Reference the existing IAM grant in market-overview that already names this distribution ARN -- update to use `aws_cloudfront_distribution.market_metrics.arn` interpolation instead of the hardcoded ID.
      5. Import: `terraform import aws_cloudfront_distribution.market_metrics E2LPCXXBLDGWXY`.
      6. `terraform plan` -> 0-diff.
      7. `terraform apply` (no-op for CF; the IAM interpolation change will show as a no-op replacement-by-reference).
      8. Tag `market-overview-v{next}`.
    </deliverable>
  </deliverables>

  <acceptance_criteria>
    1. `terraform plan` 0-diff in market-overview.
    2. Two origins preserved.
    3. IAM grant updated to reference the imported resource (no more hardcoded distribution ID in IAM).
    4. Tag pushed.
    5. Session log's Compiler Tools section reproduces each `<run>` + observed-result + pass/fail vs. `<expect>` (CTO Rule 7 locked 2026-04-15).
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step><run>aws cloudfront get-distribution --id E2LPCXXBLDGWXY</run><expect>Live config captured.</expect><if_mismatch>STOP. Surface the CLI error to COO; do not author TF against stale/guessed config.</if_mismatch></step>
      <step><run>grep -rn "E2LPCXXBLDGWXY" infra/aws/terraform/market-overview/</run><expect>Find existing IAM grant references for refactor.</expect><if_mismatch>If no references found (contradicts audit), STOP and reconcile with the 2026-04-15 inventory report before refactoring IAM — do not author speculative IAM changes.</if_mismatch></step>
      <step><run>git tag -l "market-overview-v*" | sort -V | tail -3</run><expect>Next-tag identified.</expect><if_mismatch>If no prior tags returned, confirm pipeline tag history with COO before selecting a version.</if_mismatch></step>
    </phase>
    <phase id="2" when="before commit">
      <step><run>terraform plan</run><expect>0-diff (CF) + benign IAM interpolation swap.</expect><if_mismatch>Edit TF to match live for every CF drift line. IAM swap must be resource-reference-only (no policy doc changes). Surface to COO if a field cannot be represented.</if_mismatch></step>
    </phase>
    <phase id="3" when="after commit">
      <step><run>terraform plan</run><expect>0-diff.</expect><if_mismatch>Post-apply drift = incomplete import. STOP, capture delta, surface to COO; do NOT tag or mark complete.</if_mismatch></step>
    </phase>
  </compiler_tools_mandate>

  <dependencies>None hard. Sequence after .003 to space out CF imports.</dependencies>

  <next>On complete: CDRS_TFIMPT.005 (Public API CDN -- 5 cache behaviors, the most complex).</next>
</task_order>
