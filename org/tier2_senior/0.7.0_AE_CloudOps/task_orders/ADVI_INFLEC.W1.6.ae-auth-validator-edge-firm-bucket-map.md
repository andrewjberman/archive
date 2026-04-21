<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-04-21-inflec-w1.6-edge-firm-bucket-map</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <date>2026-04-21</date>
    <status>staged</status>
    <project_code>ADVI_INFLEC</project_code>
  </metadata>

  <objective>
    Add `'inflection': 'inf'` entry to the `FIRM_BUCKET_MAP` inlined in `infra/aws/lambda-edge/auth-validator-edge/index.mjs` (around L101). This maps firmId → bucket-alias for edge-signed S3 reads on the `/api/scoped/advisor-intelligence/*.json` CloudFront behavior. MUST stay in sync with W1.7 (shared-advisor-router). Deploy via Terraform → CloudFront Lambda@Edge propagation ~15 min.
  </objective>

  <context>
    ADVI_INFLEC PRD v1.2 §4.2 row 3. This is one of two Lambda@Edge functions with FIRM_BUCKET_MAP — the other is shared-advisor-router (W1.7). CTO §4.2 note: "Must stay in sync". One-line map add per file. CloudFront invalidation + Lambda@Edge propagation delay is the only complexity.

    Canonical pattern (existing entry for 49financial at L101-ish): `'49financial': 'bd'` — maps firmId to the bucket suffix (`opal-data-{alias}`). Inflection alias is `inf` → `opal-data-inf`. Alias must match `s3Bucket` value in DynamoDB FIRM row (W1.3 writes `s3Bucket=opal-data-inf`) resolved as `${bucket_prefix}-${alias}`. Confirm prefix match in Phase 1.
  </context>

  <compiler_tools_mandate>
    Phase 1 (before writing):
    <run>grep -n "FIRM_BUCKET_MAP\|'49financial'\|'bd'" infra/aws/lambda-edge/auth-validator-edge/index.mjs</run>
    <expect>Confirm FIRM_BUCKET_MAP location + existing 49F/mockadv entries. Copy style.</expect>

    <run>grep -n "FIRM_BUCKET_MAP\|'49financial'\|'bd'" infra/aws/lambda-edge/shared-advisor-router/index.mjs</run>
    <expect>Same map structure at a different line. W1.7 will make identical edit.</expect>

    <run>aws s3 ls opal-data-inf/ 2>&1 | head -1</run>
    <expect>Bucket exists (W1.1 prerequisite). If NoSuchBucket, BLOCK — W1.1 hasn't shipped.</expect>

    <run>aws dynamodb get-item --table-name opal-users-v2 --key '{"PK":{"S":"FIRM#inflection"},"SK":{"S":"METADATA"}}' --query 'Item.s3Bucket.S'</run>
    <expect>"opal-data-inf" — alias derivation (`inf`) must produce this exact bucket. If mismatch, escalate.</expect>

    <run>comp-routes behaviors</run>
    <expect>Current CloudFront behaviors + Lambda@Edge associations. Note viewer-request vs origin-request for auth-validator-edge (viewer-request on `/api/scoped/advisor-intelligence/*.json` behavior).</expect>

    Phase 2 (during implementation):
    <run>.tools/terraform.exe plan (from portal-auth/)</run>
    <expect>1 aws_lambda_function source_code_hash change (auth-validator-edge) + 1 aws_cloudfront_distribution association version bump. Nothing else.</expect>

    <run>.tools/terraform.exe apply</run>
    <expect>Apply succeeds; CloudFront distribution reports PROGRESSING — wait for `InProgress → Deployed` before testing.</expect>

    Phase 3 (after deploy, after 15+ min global propagation):
    Integration test (curl + decode):
    1. `curl -H "Authorization: Bearer $INFLECTION_JWT" https://portal.opalcapital.com/api/scoped/advisor-intelligence/platinum/firm/leaderboard.json` → expect 200 reading from `opal-data-inf` — need a test JWT with `allowedFirmIds=inflection` (coordinate with W5.5 row provisioning).
    2. `curl -H "Authorization: Bearer $49F_JWT" https://portal.opalcapital.com/api/scoped/advisor-intelligence/platinum/firm/leaderboard.json` → expect 200 reading from `opal-data-bd`. W5.9 regression guard.
    3. Internal (opal-capital) admin → same call with firmId=inflection query → expect 200 via admin bypass (current behavior, unchanged).

    <run>comp-routes trace getPlatinumAdvisorTimeseries</run>
    <expect>Route map unchanged; Lambda@Edge version bumped.</expect>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    shared_resource: `auth-validator-edge` Lambda@Edge + CloudFront distribution.
    also_in_to: W1.7 (shared-advisor-router FIRM_BUCKET_MAP — identical edit, different file). MUST ship together or close-enough that the two Lambda@Edge functions don't disagree on firmId resolution.
    last_write_owner: 0.7.0_AE_CloudOps.
    required_action: "Deploy W1.6 + W1.7 as a paired commit + single Terraform apply. Do NOT deploy W1.6 without W1.7 — transient desync means auth-validator-edge accepts Inflection but shared-advisor-router can't route it. Wait for 15 min Lambda@Edge propagation before running integration tests. Coordinate CloudFront invalidation window with portal (typically non-issue — edge-only functions)."
  </cross_domain_coordination>

  <acceptance_criteria>
    1. `index.mjs` FIRM_BUCKET_MAP has `'inflection': 'inf'` entry at the map.
    2. Lambda@Edge redeployed; CloudFront distribution Status `Deployed`.
    3. 15+ min global propagation respected; invalidation id logged.
    4. Integration test: Inflection JWT → reads `opal-data-inf/*.json` successfully (returns 200 or expected 404 if file not yet published; no 403 from the edge function).
    5. Regression: 49F JWT → reads `opal-data-bd/*.json` successfully. No regression.
    6. Internal admin → firmId=inflection query → 200 via admin bypass.
    7. `comp-routes behaviors` unchanged (behavior map stable; only Lambda version bumped).
    8. Tag `portal-auth-v{next}` (or shared-infra-v{next} if edge lives in shared-infra module — confirm in Phase 1) with `--follow-tags`.
    9. Source map updated.
    10. Session log at `org/tier2_senior/0.7.0_AE_CloudOps/logs/2026-04-{NN}/advi_inflec_w1_6_auth_validator_edge.md` with diff, deploy tag, invalidation id, integration test output.
  </acceptance_criteria>

  <scope>
    <files>
      <file action="modify">infra/aws/lambda-edge/auth-validator-edge/index.mjs</file>
      <file action="update">infra/aws/lambda/ci/lambda-source-map.json</file>
      <file action="reference">docs/architecture/ADVI_INFLEC.md §4.2 row 3</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">Map entry: `'inflection': 'inf'` — exact. No aliasing divergence between W1.6 and W1.7.</requirement>
    <requirement id="2">Co-deploy with W1.7. No desync window.</requirement>
    <requirement id="3">Wait ≥15 min for Lambda@Edge global propagation before integration tests. Log invalidation id + wait time.</requirement>
    <requirement id="4">Do NOT modify `auth-validator-edge` logic beyond the one-line map add. Any refactor requires a separate TO.</requirement>
    <requirement id="5">Regression test 49F + internal admin paths BEFORE signaling W5.9 off to DT.</requirement>
    <requirement id="6">Terraform-only deploy. No `aws lambda update-function-code`.</requirement>
  </requirements>

  <deliverables>
    <deliverable type="commit">`index.mjs` + source map update. Author 0.7.0_AE_CloudOps.</deliverable>
    <deliverable type="tag">`portal-auth-v{next}` (or equivalent — confirm Phase 1).</deliverable>
    <deliverable type="document">Session log with integration test output + invalidation id.</deliverable>
  </deliverables>

  <do_not>
    <rule>Do NOT deploy without W1.7 ready.</rule>
    <rule>Do NOT skip Lambda@Edge propagation wait.</rule>
    <rule>Do NOT refactor beyond the map entry.</rule>
    <rule>Do NOT use aws lambda update-function-code.</rule>
  </do_not>
</task_order>
