<task_order>
  <metadata>
    <id>TRSB_TFIMPT.W3</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <coordinator>0.4.0_DT_ClientPlatform (CloudFront behavior add — if new behavior required on portal main CF)</coordinator>
    <date>2026-04-21</date>
    <status>staged</status>
    <project_code>TRSB_TFIMPT</project_code>
    <priority>P1 (closes the routing-is-console-only gap; final wave)</priority>
    <sla>1 day from GO (API GW import + CF wiring + comp-routes registration + smoke test)</sla>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/TRSB_TFIMPT.md (sections 1.G3, 3.Wave 3, 6.TO-3, 7)</ref>
    <ref type="precedent_pattern">CDRS_TFIMPT.002-.005 (CloudFront distribution imports, 2026-04-15) — pattern for CF behavior wiring + route registration</ref>
    <ref type="precedent_pattern">CDRS_TFIMPT.007 (partner-firm TF module + shared-lib + auth-handler generalization, 2026-04-15) — pattern for multi-resource coordinated import</ref>
    <ref type="precedent_pattern">AUTH_TFIMPT.001 (CloudFront distribution import, 2026-04-06) — first-pattern import + comp-routes population</ref>
    <ref type="project_json">org/projects/TRSB_TFIMPT.json</ref>
    <ref type="target_files">infra/aws/terraform/trade-pipeline/apigateway.tf (new) + existing portal CF behaviors (if touch needed) + infra/aws/terraform/trade-pipeline/{main,CHANGELOG}.{tf,json}</ref>
  </references>

  <objective>
    Close G3: import the live API Gateway(s) fronting trade Lambdas into `trade-pipeline/apigateway.tf`, wire the `/api/general/trades/*` path to the imported GW via CloudFront behavior, register the routes in `comp-routes` so `comp-routes trace trade-submission-handler` returns a populated chain. Target tag `trade-pipeline-v1.5.0`.

    Post-W3: the entire trade subsystem becomes compiler-visible end-to-end. CF → [behavior] → API GW → authorizer → Lambda → DDB trace is populated in the graph. This closes ADHC_ROUTER Phase 2 gap for this subsystem and lets future trade PRDs use `comp-routes trace` for change-blast analysis.
  </objective>

  <scope>
    <files>
      <file action="create">infra/aws/terraform/trade-pipeline/apigateway.tf — `aws_api_gateway_rest_api` (or v2 equivalent) + resources + methods + integrations + deployments + stages + Lambda permissions (per live GW inventory)</file>
      <file action="modify">infra/aws/terraform/public-api-cdn/cloudfront.tf (or equivalent portal CF TF) — add CloudFront behavior for `/api/general/trades/*` → trade-pipeline API GW origin (IF behavior doesn't already exist on live CF)</file>
      <file action="modify">infra/aws/terraform/trade-pipeline/CHANGELOG.json</file>
      <file action="modify">infra/aws/terraform/trade-pipeline/README.md — document the API GW import, authorizer integration, route map</file>
    </files>
  </scope>

  <deliverables>
    <deliverable id="identify-live-gateways">
      1. `aws apigateway get-rest-apis` + `aws apigatewayv2 get-apis` — filter by name for "trade" or "opal-trade" or similar.
      2. For each identified GW: `aws apigateway get-resources --rest-api-id &lt;id&gt;` (map full resource/method/integration tree) + `aws apigateway get-authorizers --rest-api-id &lt;id&gt;` + `aws apigateway get-stages --rest-api-id &lt;id&gt;` + `aws apigateway get-deployments --rest-api-id &lt;id&gt;`.
      3. Capture Lambda permission resource policies: `aws lambda get-policy --function-name &lt;fn&gt;` for each trade Lambda — capture the `lambda:InvokeFunction` principal=apigateway.amazonaws.com statements (these become `aws_lambda_permission` resources in TF).
      4. Manifest: per-GW full resource tree + auth-model + stage config + Lambda permissions, written to `data/trade/apigateway-inventory-{DATE}.json` (diagnostic artifact, uncommitted).
    </deliverable>
    <deliverable id="author-apigateway-tf">
      1. Author `apigateway.tf` resources matching live byte-for-byte (follow CDRS_TFIMPT.006 pattern: recon-drives-implementation, don't assume config — discover it).
      2. Resources in scope (per live inventory): `aws_api_gateway_rest_api` / `aws_api_gateway_resource` / `aws_api_gateway_method` / `aws_api_gateway_integration` / `aws_api_gateway_authorizer` / `aws_api_gateway_deployment` / `aws_api_gateway_stage` / `aws_api_gateway_method_response` / `aws_api_gateway_integration_response` / `aws_lambda_permission` (one per Lambda-GW binding).
      3. Per-resource `terraform import` — use `terraform plan -target=&lt;resource&gt;` to verify 0-diff resource-by-resource before proceeding to next. Do NOT batch imports blindly — `-target` per resource, 0-diff gate, then next.
      4. Full `terraform plan` (no `-target`) 0-diff across all imported resources.
      5. `terraform apply` (no-op; all imports already materialized).
    </deliverable>
    <deliverable id="cloudfront-wiring">
      1. Check live portal main CF distribution for existing `/api/general/trades/*` behavior: `aws cloudfront get-distribution-config --id &lt;portal-main-cf-id&gt;` + filter `CacheBehaviors` for trade paths.
      2. If behavior exists on live CF: add it to the TF (update `public-api-cdn/cloudfront.tf` or equivalent, matching live). Import-only; no live change.
      3. If behavior doesn't exist: MCP 0.4.0_DT_ClientPlatform before adding — CF changes on portal main CF are DT 0.4's domain per PRD §5. Coordinate on whether the add belongs in portal-auth/portal-cdn vs trade-pipeline. Default: portal-cdn TF (keeps behaviors in one CF config file).
      4. Verify CF origin points at trade-pipeline API GW invocation URL + auth header forwarding + cache behavior matches expected.
    </deliverable>
    <deliverable id="comp-routes-population">
      1. After `apigateway.tf` + CF changes land: `comp-build` to refresh compiler graph.
      2. `comp-routes trace trade-submission-handler` — expect populated chain: `CloudFront (portal-main) → [/api/general/trades/* behavior] → API GW (trade) → [authorizer] → Lambda (trade-submission-handler)`.
      3. `comp-routes auth-map` — confirm trade routes show expected auth tier (likely `[AUTH]` per portal convention).
      4. `comp-routes behaviors` — confirm new CF behavior appears + no collision with other `/api/general/*` behaviors.
    </deliverable>
    <deliverable id="smoke-test-and-tag">
      1. End-to-end smoke per §8 Q4 fixture: submit one test trade. Capture CloudWatch trace across CF → API GW → authorizer → handler → DDB write + SES. Verify no 403 / 500 / timeout.
      2. Pre-tag: `git tag -l "trade-pipeline-v*" | sort -V | tail -5` — confirm next version is `v1.5.0` (after W2 `v1.4.0`).
      3. `git commit --only --author="0.7.0_AE_CloudOps <0.7.0_AE_CloudOps@opal.agent>"`.
      4. `git tag -a trade-pipeline-v1.5.0 -m "W3 API Gateway import + route wiring"` + `git push origin CLOUD --follow-tags`.
    </deliverable>
  </deliverables>

  <wire_contract>
    Zero runtime behavior delta expected.
    - API GW resources already exist on live; `terraform import` is metadata-only.
    - Lambda permission resource policies already grant API GW invoke; import just captures them in TF.
    - CF behavior either already exists (import-only) or gets added (coordinate with DT 0.4 — and the add itself is a live change — this is the only potential wire-contract risk).
    - Risk: if `terraform apply` strips a Lambda permission that was hand-created outside TF, every API-GW-triggered invocation 500s. Mitigation: Phase 2 `-target` per resource, 0-diff gate, then next.
  </wire_contract>

  <acceptance_criteria>
    1. `terraform plan` 0-diff on trade-pipeline post-W3 applies.
    2. All live API GW resources represented in `apigateway.tf`: REST API + resources + methods + integrations + authorizers + deployments + stages + Lambda permissions. `aws apigateway get-rest-apis` matches TF resource count.
    3. CloudFront behavior for `/api/general/trades/*` either exists on live CF (imported into TF) OR added per DT 0.4 MCP coordination.
    4. `comp-routes trace trade-submission-handler` returns populated chain.
    5. `comp-routes auth-map` shows trade routes at expected auth tier.
    6. `comp-iam gaps` still clean post-W3 (W2 closed service gap; W3 doesn't re-open it).
    7. End-to-end smoke test: test trade submit → CloudWatch trace shows full CF → API GW → authorizer → handler → DDB write + SES. No 4xx/5xx.
    8. Tag `trade-pipeline-v1.5.0` exists and pushed.
    9. Session log at `org/tier2_senior/0.7.0_AE_CloudOps/logs/{DATE}/trsb_tfimpt_w3_api_gateway_import_and_route_wiring.md` reproducing every `<run>` + observed-result + pass/fail vs `<expect>`.
    10. MCP COMPLETE to COO with commit hash + tag + comp-routes output + CloudWatch trace excerpt.
    11. PROJECT closeout: on W3 complete, project status flips to `complete`; TRSB_TFIMPT moved from Active to Completed in `org/projects/REGISTRY.md`.
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>aws apigateway get-rest-apis + aws apigatewayv2 get-apis (filtered for trade)</run>
        <expect>Live API GW(s) identified by ID + name. At least 1 expected (trade-submission-handler implies 1 GW per PRD §1.G3). If 0 returned, trade flow is using a different entry point (direct Lambda invoke via CF Lambda@Edge?) — surface to COO.</expect>
        <if_mismatch>STOP. If 0 GWs found, the assumption that API GW exists is wrong — need to re-scope W3 entirely.</if_mismatch>
      </step>
      <step>
        <run>aws apigateway get-resources --rest-api-id &lt;id&gt; + get-authorizers + get-stages</run>
        <expect>Full resource tree + authorizer config + stage config captured. Authorizer should reference trade-authorizer (+ trade-recon-authorizer if live). Stages should include at least one production stage.</expect>
        <if_mismatch>If authorizer config is unexpectedly broken or missing, recon up the call chain — may indicate a recent incident. Surface.</if_mismatch>
      </step>
      <step>
        <run>For each trade Lambda: aws lambda get-policy --function-name &lt;fn&gt; (capture Lambda permission statements)</run>
        <expect>Each Lambda has at least one `lambda:InvokeFunction` statement with `Principal=apigateway.amazonaws.com` + `SourceArn` matching the trade GW's invoke pattern. These become `aws_lambda_permission` TF resources.</expect>
        <if_mismatch>If a Lambda has no apigateway principal, it's invoked some other way (direct invoke, scheduled rule) — document. If missing an expected permission, that Lambda's integration path is broken live — escalate.</if_mismatch>
      </step>
      <step>
        <run>comp-routes trace trade-submission-handler (BEFORE)</run>
        <expect>"No match for: trade-submission-handler" — baseline W3-gap signal per PRD §2.</expect>
        <if_mismatch>If result returns, W3 already partially shipped — audit.</if_mismatch>
      </step>
      <step>
        <run>comp-routes behaviors (BEFORE)</run>
        <expect>Capture current CF behaviors pre-change. Verify no existing `/api/general/trades/*` behavior collides. Portal main CF is the likely parent; confirm by grepping `infra/aws/terraform/portal-*/cloudfront*.tf` for existing trade paths.</expect>
        <if_mismatch>If behavior already exists on portal main CF TF, W3 CF scope is import-only (easier); if only on live, need to author + import.</if_mismatch>
      </step>
      <step>
        <run>aws cloudfront get-distribution-config --id &lt;portal-main-cf-id&gt; | jq '.DistributionConfig.CacheBehaviors.Items[] | select(.PathPattern | contains("trade"))'</run>
        <expect>Either matches an existing behavior (import-only path) OR returns empty (add-behavior path, requires DT 0.4 MCP).</expect>
        <if_mismatch>If ambiguous or DT 0.4 MCP needed, pause W3 before authoring the CF change. This is the coordination gate per PRD §5.</if_mismatch>
      </step>
    </phase>

    <phase id="2" when="before commit">
      <step>
        <run>Per-resource: terraform plan -target=aws_api_gateway_&lt;resource_type&gt;.&lt;name&gt;</run>
        <expect>0-diff on that specific resource after import. Proceed to next only when current resource plans clean.</expect>
        <if_mismatch>If diff, edit TF field-by-field to match live. NEVER apply a plan that mutates live for an imported resource.</if_mismatch>
      </step>
      <step>
        <run>terraform plan (global, no -target)</run>
        <expect>0-diff across ALL resources. If any per-target plans were 0-diff individually but the global plan shows drift, there's cross-resource coupling (e.g. deployment + stage version pinning). Investigate.</expect>
        <if_mismatch>Reconcile before apply.</if_mismatch>
      </step>
      <step>
        <run>If CF behavior ADD needed: terraform plan on public-api-cdn (or portal CF TF path)</run>
        <expect>Single net-new `cache_behavior` block + matching origin config if new origin needed. Plan is the live-change preview — review carefully before apply.</expect>
        <if_mismatch>If scope extends beyond single behavior (e.g. requires new origin, new origin request policy, new response headers policy), MCP DT 0.4 + COO before apply.</if_mismatch>
      </step>
    </phase>

    <phase id="3" when="after commit">
      <step>
        <run>terraform plan (trade-pipeline + public-api-cdn if touched)</run>
        <expect>0-diff across both.</expect>
        <if_mismatch>Post-apply drift. STOP, capture, surface.</if_mismatch>
      </step>
      <step>
        <run>comp-build + comp-routes trace trade-submission-handler</run>
        <expect>Populated chain: `CloudFront → [behavior path] → API GW → [authorizer] → Lambda:trade-submission-handler`.</expect>
        <if_mismatch>If still empty, the comp-routes indexer needs the CF-API-GW edge hint — may need to add/update a hint file (see comp-tools.yaml for route-hint config).</if_mismatch>
      </step>
      <step>
        <run>comp-routes auth-map + comp-routes behaviors</run>
        <expect>Trade routes at expected auth tier. CF behaviors table includes `/api/general/trades/*`.</expect>
        <if_mismatch>If auth tier is unexpected (e.g. public when should be auth-gated), there's a CloudFront or authorizer config issue — investigate before marking complete.</if_mismatch>
      </step>
      <step>
        <run>End-to-end smoke per §8 Q4 fixture</run>
        <expect>Test trade submit traces cleanly through CF → API GW → authorizer → handler → DDB + SES. CloudWatch log groups capture expected invocation sequence.</expect>
        <if_mismatch>If 403 at authorizer, Lambda permission was stripped somewhere. If 500 at handler, code path affected by env-var or role change. Revert individually per resource.</if_mismatch>
      </step>
      <step>
        <run>comp-iam gaps (global, post-W3)</run>
        <expect>Still clean — W2 reclaimed services stay indexed; W3 doesn't re-open gaps.</expect>
        <if_mismatch>If gap surfaces, investigate whether API GW authorizer integration needs additional IAM that W2 didn't cover.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    <item>**DT 0.4 CloudFront MCP gate** (PRD §5): if W3 requires ADD of a `/api/general/trades/*` CF behavior on portal main CF (not already there), 0.4.0_DT_ClientPlatform owns that distribution and must be MCP'd before the TF change lands. COO relays or AE 0.7 MCPs directly per RAVC. If behavior already lives on live + TF just needs to import it, DT 0.4 coordination is courtesy heads-up, not gate.</item>
    <item>**Portal CF TF path** — confirm whether `public-api-cdn/cloudfront.tf` or `portal-auth/cloudfront.tf` (or similar) is the right home. Follow CDRS_TFIMPT.002-.005 precedent for which file owns which behavior.</item>
    <item>**Authorizer dependency** — W2 reclaimed trade-authorizer code. W3 imports the API GW authorizer config that points at that Lambda. Both must be in a consistent state; a W3 before W2 (or W2 without W3) leaves the authorizer partially managed. PRD §3 strict ordering is the discipline.</item>
    <item>Tag series: `trade-pipeline-v1.5.0`. Verify tag base `v1.4.0` (W2) exists before cutting `v1.5.0`.</item>
    <item>**PROJECT CLOSEOUT** on W3 complete: COO flips project status `active → complete`, moves REGISTRY row Active → Completed. This TO is the terminal wave of TRSB_TFIMPT.</item>
  </cross_domain_coordination>

  <dependencies>
    <dependency agent="0.7.0_AE_CloudOps" task="TRSB_TFIMPT.W2 complete" status="pending">
      W3 imports API GW authorizer config that references W2's reclaimed trade-authorizer Lambda. Ordering: W2 → W3.
    </dependency>
    <dependency agent="0.4.0_DT_ClientPlatform" task="CloudFront behavior coordination MCP" status="pending">
      AE 0.7 MCPs DT 0.4 before CF behavior change lands. Scope = gate on whether behavior is import-only (existing on live) or new-add (DT 0.4 explicit ack required).
    </dependency>
    <dependency agent="2.0.0_SA_COO" task="W3 status flip staged→pending" status="pending">
      Gates on W2 complete + DT 0.4 CloudFront pre-coordination. COO flips on both.
    </dependency>
  </dependencies>

  <next>On W2 complete + DT 0.4 CF MCP coordinated: COO flips this TO staged→pending + dispatches GO. On AE commit + tag + push: MCP COMPLETE to COO with commit hash + tag + comp-routes populated output + CloudWatch smoke-trace excerpt. COO flips project status → complete, moves TRSB_TFIMPT from Active to Completed in REGISTRY.md.</next>
</task_order>
