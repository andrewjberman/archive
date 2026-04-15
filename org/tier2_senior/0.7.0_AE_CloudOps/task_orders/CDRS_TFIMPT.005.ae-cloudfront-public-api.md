<task_order>
  <metadata>
    <id>0.7.0_AE_CloudOps-2026-04-15-cfimpt-rest-005-public-api</id>
    <issued_by>0.7.0_AE_CloudOps (self-authored from cloud inventory audit; trigger: Andrew direction 2026-04-15)</issued_by>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <date>2026-04-15</date>
    <status>complete</status>
    <project_code>CDRS_TFIMPT</project_code>
    <priority>P1 (sprint) -- most complex of the 5; 5 cache behaviors</priority>
  </metadata>

  <references>
    <ref type="trigger">docs/analysis/2026-04-15_cloud_inventory_audit.md section 6b</ref>
    <ref type="precedent">CDRS_TFIMPT.001..004 establish the pattern</ref>
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
    5. Session log's Compiler Tools section reproduces each `<run>` + observed-result + pass/fail vs. `<expect>` (CTO Rule 7 locked 2026-04-15).
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step><run>aws cloudfront get-distribution --id E398SP0DG1ME0Y > /tmp/public-api-cdn-config.json</run><expect>JSON saved for behavior-by-behavior copying.</expect><if_mismatch>STOP. Surface the CLI error to COO; do not author 6 behaviors against stale/guessed config.</if_mismatch></step>
      <step><run>aws apigateway get-rest-api --rest-api-id 7k3ed8px20</run><expect>API GW identity confirmed; check TF coverage.</expect><if_mismatch>If API returns NotFoundException, the CloudFront origin references a deleted/renamed API GW — STOP and surface to COO before import (config is broken upstream).</if_mismatch></step>
      <step><run>grep -rln "7k3ed8px20" infra/aws/terraform/</run><expect>Determine if API GW already TF-managed; pick reference strategy.</expect><if_mismatch>If TF-managed: reference via resource address. If not: declare by domain_name only in this TO and log a follow-up. Do NOT attempt to import the API GW here.</if_mismatch></step>
    </phase>
    <phase id="2" when="before commit">
      <step><run>terraform plan</run><expect>0-diff. Most likely failure mode: cache-policy field defaults differ -- match TF to live.</expect><if_mismatch>Edit TF behavior-by-behavior to match live. Expect 2-3 iterations. Do NOT apply a plan that mutates live cache keys (would invalidate prod caches). Surface to COO if a policy ID cannot be represented.</if_mismatch></step>
    </phase>
    <phase id="3" when="after commit">
      <step><run>terraform plan</run><expect>0-diff.</expect><if_mismatch>Post-apply drift = incomplete import. STOP, capture delta, surface to COO; do NOT tag or mark complete.</if_mismatch></step>
    </phase>
  </compiler_tools_mandate>

  <dependencies>Sequence last among the 5 -- the 6-behavior config benefits from pattern reps in .001-.004 first.</dependencies>

  <closeout date="2026-04-15" commit="pending-on-commit">
    (a) **Import landed on first-try 0-diff.** Zero plan/edit cycles needed (TO estimated 2-3). All 6 behaviors use AWS-managed policy IDs (no inline forwarded_values legacy) which is the best-case CF import shape.
    (b) API GW `7k3ed8px20` is **v2 HTTP API** (not v1 REST). The TO's Phase 1 step 2 `aws apigateway get-rest-api` returned NotFoundException because v2 lives in a different namespace (`aws apigatewayv2 get-api`). **Corpus note for future AE CF imports over API GW origins:** if `get-rest-api` returns NotFoundException, try `apigatewayv2 get-api --api-id <id>` before concluding the API GW is broken.
    (c) API GW is referenced in `partners-api/api-gateway.tf` + `bd-pipeline/api-gateway.tf` as string literals (not as a resource). Referenced in this module by domain_name only (per TO contingency path for unmanaged API GWs).
    (d) HttpVersion = `http2and3` (differs from .001-.004 which are http2 only). Noted inline.
    (e) New top-level module `infra/aws/terraform/public-api-cdn/` — state key `public-api-cdn/tfstate`. Backend initialized; no prior state.
    Full `terraform plan` 0-diff post-apply (apply was tags_all default_tags metadata only, same pattern as all 4 prior imports).
  </closeout>

  <next>On complete: CloudFront TF coverage = 100% (6/6). CDRS_TFIMPT sprint closed. Next: JWT drift reconcile (AE-owned post-sprint follow-up) OR DT 0.4 handoff to CDRS_TFIMPT.006/.007 per COO staging.</next>

  <next>On complete: CloudFront TF coverage = 100% (6/6). Update README "Known Issues" + cloud inventory report. Optional follow-up: add CI lint flagging any future console-only distribution.</next>
</task_order>
