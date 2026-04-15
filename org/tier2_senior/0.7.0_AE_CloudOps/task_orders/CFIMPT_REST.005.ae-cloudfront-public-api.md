<task_order>
  <metadata>
    <id>0.7.0_AE_CloudOps-2026-04-15-cfimpt-rest-005-public-api</id>
    <issued_by>0.7.0_AE_CloudOps (self-authored from cloud inventory audit; trigger: Andrew direction 2026-04-15)</issued_by>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <date>2026-04-15</date>
    <status>staged</status>
    <project_code>CFIMPT_REST</project_code>
    <priority>P1 (sprint) -- most complex of the 5; 5 cache behaviors</priority>
  </metadata>

  <references>
    <ref type="trigger">docs/analysis/2026-04-15_cloud_inventory_audit.md section 6b</ref>
    <ref type="precedent">CFIMPT_REST.001..004 establish the pattern</ref>
  </references>

  <objective>
    Import CloudFront distribution **E398SP0DG1ME0Y** ("Opal Portal Public API CDN -
    Caches public endpoints from API Gateway") into Terraform state. Single API Gateway
    origin (`7k3ed8px20.execute-api.us-east-1.amazonaws.com`) with 6 total cache
    behaviors (1 default + 5 custom). No L@E, no WAF, no alias.

    The 5 custom behaviors likely correspond to specific public API path patterns
    (probably `/api/general/*`, `/v1/*`, etc). Each must be replicated EXACTLY in TF --
    cache key contents, allowed methods, TTLs, and forwarded headers/cookies.

    TF home: new top-level module `infra/aws/terraform/public-api-cdn/` (does not
    fit cleanly inside any existing pipeline -- it fronts API GW that is shared
    across multiple Lambdas).
  </objective>

  <scope>
    <files>
      <file action="create">infra/aws/terraform/public-api-cdn/main.tf</file>
      <file action="create">infra/aws/terraform/public-api-cdn/cloudfront.tf</file>
      <file action="create">infra/aws/terraform/public-api-cdn/variables.tf</file>
    </files>
  </scope>

  <deliverables>
    <deliverable id="cf-import">
      1. `aws cloudfront get-distribution --id E398SP0DG1ME0Y` -- full config including all 5 behaviors. Save raw JSON locally for reference during TF authoring.
      2. For each of the 5 custom behaviors capture: `PathPattern`, `AllowedMethods`, `CachedMethods`, `CachePolicyId` OR forwarded values (legacy), `OriginRequestPolicyId`, `ResponseHeadersPolicyId`, `MinTTL/DefaultTTL/MaxTTL`, `ViewerProtocolPolicy`, `Compress`.
      3. Identify API Gateway `7k3ed8px20` -- which Lambda(s) does it front? (`aws apigateway get-rest-api --rest-api-id 7k3ed8px20` and grep TF for the ID.) If TF-managed, reference by data source; if not, declare in this TO or defer.
      4. Write `aws_cloudfront_distribution.public_api` matching every behavior exactly. Cache behaviors must appear in the same order TF emits them (precedence-sensitive).
      5. State backend: `public-api-cdn/tfstate`.
      6. Import.
      7. `terraform plan` -> 0-diff. EXPECT this one to take 2-3 plan/edit cycles to converge -- 6 behaviors = 6x the surface area for cache-policy field-level drift.
      8. `terraform apply` (no-op).
      9. Tag `public-api-cdn-v1.0.0`.
    </deliverable>
  </deliverables>

  <acceptance_criteria>
    1. `terraform plan` 0-diff in public-api-cdn.
    2. All 6 behaviors preserved with identical PathPattern + cache key.
    3. Tag pushed.
    4. pipeline_inventory.xml updated.
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step><run>aws cloudfront get-distribution --id E398SP0DG1ME0Y > /tmp/public-api-cdn-config.json</run><expect>JSON saved for behavior-by-behavior copying.</expect></step>
      <step><run>aws apigateway get-rest-api --rest-api-id 7k3ed8px20</run><expect>API GW identity confirmed; check TF coverage.</expect></step>
      <step><run>grep -rln "7k3ed8px20" infra/aws/terraform/</run><expect>Determine if API GW already TF-managed; pick reference strategy.</expect></step>
    </phase>
    <phase id="2" when="before commit">
      <step><run>terraform plan</run><expect>0-diff. Most likely failure mode: cache-policy field defaults differ -- match TF to live.</expect></step>
    </phase>
    <phase id="3" when="after commit">
      <step><run>terraform plan</run><expect>0-diff.</expect></step>
    </phase>
  </compiler_tools_mandate>

  <dependencies>Sequence last among the 5 -- the 6-behavior config benefits from pattern reps in .001-.004 first.</dependencies>

  <next>On complete: CloudFront TF coverage = 100% (6/6). Update README "Known Issues" + cloud inventory report. Optional follow-up: add CI lint flagging any future console-only distribution.</next>
</task_order>
