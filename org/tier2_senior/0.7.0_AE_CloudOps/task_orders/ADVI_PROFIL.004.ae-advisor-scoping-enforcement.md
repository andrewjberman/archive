<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-04-10-profil-scoping</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <co_owner>0.4.0_DT_ClientPlatform</co_owner>
    <date>2026-04-10</date>
    <status>staged</status>
    <project_code>ADVI_PROFIL</project_code>
  </metadata>

  <objective>
    Extend `shared-advisor-router` (Lambda@Edge or the equivalent authorizer) to reject non-admin requests where the advisor id in the URL path does NOT match the `advisorId` claim in the caller's JWT. Endpoints in scope: `/api/scoped/partners/books/advisor/{advisorId}/platinum-summary`, `platinum/advisors/{advisorId}/summary.json` (Lambda-served, not S3-direct), `platinum/advisors/{advisorId}/timeseries.json` (Lambda-served, not S3-direct). Admin users bypass the check. Returns 403 on mismatch. This is the authoritative defense in depth — frontend gating from .001 is cosmetic; .004 is load-bearing.
  </objective>

  <context>
    Under the ADVI_PROFIL architecture shipped in .001, non-admin advisors reach their own profile via Tab 3, which is hard-wired to their JWT `advisorId` claim (shipped in .002). Frontend gates leaderboard clickability for non-admins and removes all cross-tab navigation paths. However, a non-admin with browser devtools can today construct a fetch to any advisor's platinum endpoints and the server will return the data.

    Current state of scoping (per RD briefing §5.2 and CTO PRD §2):
    - `getPlatinumAdvisorSummary(advisorId, firmOverride)` — unscoped
    - `getPlatinumAdvisorDrilldownSummary(advisorId, firmOverride)` — unscoped
    - `getPlatinumAdvisorTimeseries(advisorId, firmOverride)` — unscoped

    The existing router (`shared-advisor-router` v<current>) handles firm-level scoping and admin bypass; it does not know about an `advisorId` claim because `.002` is the first TO that plumbs one through. Once .002 lands, the JWT verification path at the edge has `jwt.advisorId` available to downstream handlers.

    Enforcement spec:
    ```
    if !isAdmin(jwt) and pathAdvisorId(request) != jwt.advisorId:
        return 403
    ```

    Admin detection logic already exists in the router for firmId-scoped bypass. Reuse the same admin-check primitive. Non-admin users with `jwt.advisorId == null` (admin users without advisor mapping) get no special treatment by this rule because they fail the non-admin precondition — they never reach this check. But a non-admin user with `jwt.advisorId == null` must be rejected on ANY advisor path, since they have no advisor identity to match against.

    Path-pattern matching: extract `{advisorId}` segment from the URL. Be explicit about the patterns to avoid accidental matches on other path shapes:
    - `/api/scoped/partners/books/advisor/([^/]+)/.*`
    - `/platinum/advisors/([^/]+)/.*` (Lambda-served path — NOT the S3-direct CloudFront behavior, which is admin-only by firmId scoping already)

    Integration test required: crafted curl from a non-admin JWT to another advisor's id returns 403; admin same request returns 200; non-admin own-advisor request returns 200.
  </context>

  <compiler_tools_mandate>
    Phase 1 (before writing):
    - `comp-routes` on the full `/api/scoped/partners/books/advisor/*` and `platinum/advisors/*` serving paths. Understand the current auth chain: CloudFront → Lambda@Edge → API Gateway → backend Lambda. Identify exactly where to add the check.
    - `comp-blast shared-advisor-router` — identify every consumer and every upstream path. Confirm no downstream Lambda relies on being able to call other advisors' ids on behalf of a non-admin user.
    - Read the current `shared-advisor-router` Lambda source in full. Locate the admin-check primitive and the existing firm-scoping rule. The new rule must be structurally parallel.
    - Read `infra/aws/lambda/ci/lambda-source-map.json` entry for `shared-advisor-router`.
    - Verify .002 has landed: check `portal-auth-v1.11.*` tag list, read the `auth-validator-edge` source, confirm `jwt.advisorId` is available in the validated claim set downstream.

    Phase 2 (during implementation):
    - Add the path-pattern matching + advisorId equality check. Place it after the existing admin bypass but before any downstream forwarding.
    - Add structured logging (CloudWatch) for 403s: `log.warn("advisor_scoping_denied", userId=jwt.sub, requestedAdvisor=pathAdvisorId, jwtAdvisor=jwt.advisorId, path=request.path)`. This is critical for detecting attack attempts post-ship.
    - Do NOT block on firmId mismatch in this TO — firmId scoping is already handled by the existing router rule. This TO adds a second, advisor-level check on top of the firmId one.
    - Preserve admin bypass: if `isAdmin(jwt)` is true, skip the advisor check entirely.

    Phase 3 (after deploy):
    - Integration test matrix:
      - Non-admin user A (advisorId=A) → own endpoint → expect 200
      - Non-admin user A → other advisor endpoint → expect 403
      - Admin user → any advisor endpoint → expect 200
      - Non-admin user with `advisorId=null` (edge case) → any advisor endpoint → expect 403
    - Run `comp-routes --update` to refresh the serving path graph with the new scoping rule.
    - Verify CloudWatch logs for the 403 cases show the structured denial event.
  </compiler_tools_mandate>

  <cross_domain_coordination>
    shared_resource: `auth-validator-edge` / `shared-advisor-router` Lambda@Edge (or equivalent authorizer) — .002 (AE adds claim, Wave 1), .004 (AE enforces scoping, Wave 2). Two-pass on the same Lambda. Ordering: .004 blocks on .002 being fully deployed (including the `portal-auth-v1.11.{N}` tag).
    shared_resource: Lambda deployment pipeline — follow standard protocol (commit → Terraform → source map → tag → push --follow-tags). Tag bump: next `shared-infra-v1.6.{next}` or a new pipeline name if the router lives in its own pipeline.
    shared_resource: Backend Lambdas behind the router (platinum-summary handler, timeseries handler, etc.) — NOT touched in this TO. The router is the single choke point; backend Lambdas assume the router has enforced scoping.
    last_write_owner: 0.7.0_AE_CloudOps for Lambda@Edge and Terraform.
    required_action: "Wait for .002 to fully land (backend deployed + `portal-auth-v1.11.{next}` tag pushed). Verify via the integration test that a non-admin JWT carries `advisorId` before starting .004. Coordinate deploy timing with DT — the CloudFront invalidation from a Lambda@Edge update can take 5-15 minutes to propagate globally, and the new scoping rule will start enforcing the moment it propagates."
  </cross_domain_coordination>

  <acceptance_criteria>
    1. **Path pattern matching:** Router extracts `{advisorId}` segment from both `/api/scoped/partners/books/advisor/([^/]+)/.*` and `/platinum/advisors/([^/]+)/.*` patterns. Documented regex in the code comment.
    2. **Enforcement rule:** `if !isAdmin(jwt) and pathAdvisorId != jwt.advisorId: return 403`. Admin users bypass. Non-admin with `jwt.advisorId == null` is also rejected (they cannot prove advisor identity).
    3. **Admin bypass preserved:** Existing admin-check primitive reused. Admin users get the same behavior they had before this TO.
    4. **Structured denial logging:** Every 403 emits a CloudWatch log event with userId, requestedAdvisor, jwtAdvisor, path. Event shape documented in the session log.
    5. **Lambda deploy:** Router Lambda modified, Terraform 0-diff plan verified, source map updated, `shared-infra-v1.6.{next}` (or equivalent pipeline) tag pushed with `--follow-tags`.
    6. **Integration test matrix passed:**
       - Non-admin A → own endpoint: 200
       - Non-admin A → other advisor endpoint: 403
       - Admin → any advisor endpoint: 200
       - Non-admin with null advisorId → any advisor endpoint: 403
       Logged in the session log with the actual curl commands, response codes, and response body excerpts.
    7. **CloudFront invalidation:** If the Lambda@Edge deploy requires a CloudFront invalidation, run it and log the invalidation id. Note the propagation window.
    8. **No backend Lambda changes:** The backend platinum-summary handler and timeseries handler are unchanged. The router is the choke point.
    9. **Prerequisite verified:** .002 is fully deployed and the integration test from .002 (non-admin JWT carries `advisorId`) passed before .004 starts.
    10. **Session log:** Documents the prerequisite verification, the regex patterns, the CloudWatch event shape, the integration test matrix output, the deploy tag, the invalidation id (if any), and the compiler tools log.
  </acceptance_criteria>

  <scope>
    <files>
      <file action="modify">infra/aws/lambda/{shared-advisor-router path}/lambda_function.py (or the equivalent authorizer code)</file>
      <file action="modify">infra/aws/terraform/{owning pipeline}/** (if any Terraform changes are needed — likely none, just code update)</file>
      <file action="update">infra/aws/lambda/ci/lambda-source-map.json</file>
      <file action="reference">auth-validator-edge Lambda (verify .002 claim is available)</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">Do NOT start until .002 is fully deployed and verified. The .004 enforcement rule depends on `jwt.advisorId` being present in the validated claim set. Starting .004 before .002 lands will cause every non-admin request to 403 (which is fail-closed, but wrong).</requirement>
    <requirement id="2">Follow the standard Lambda deployment protocol: commit → Terraform (if needed) → source map → annotated tag → push --follow-tags. No `aws lambda update-function-code`.</requirement>
    <requirement id="3">Use the existing admin-check primitive in the router. Do NOT re-derive admin detection from the JWT. Consistency with firmId scoping is important.</requirement>
    <requirement id="4">The .004 check runs AFTER the admin bypass and BEFORE any downstream forwarding. Do not change the ordering of the existing firmId check — .004 is additive.</requirement>
    <requirement id="5">Structured denial logging is MANDATORY. Without it, we cannot detect attack attempts or diagnose false positives post-ship. Use the existing CloudWatch logging pattern in the router.</requirement>
    <requirement id="6">Integration test matrix MUST be run and logged before marking complete. Andrew provides non-admin and admin test credentials if needed — ask via broker message if they aren't already on file.</requirement>
    <requirement id="7">Do NOT widen the scope to other endpoints in this TO. Strictly limit to the three paths listed in §objective. Other endpoints keep their existing firmId scoping.</requirement>
    <requirement id="8">Non-admin with `jwt.advisorId == null` must be rejected (403). This is an edge case: a user who is neither admin nor has a known advisor mapping. They have no legitimate reason to query advisor-scoped endpoints.</requirement>
  </requirements>

  <deliverables>
    <deliverable type="commit">Router Lambda modified with the scoping check. Committed with `--author=0.7.0_AE_CloudOps <0.7.0_AE_CloudOps@opal.agent>`.</deliverable>
    <deliverable type="tag">`shared-infra-v1.6.{next}` (or equivalent pipeline) annotated git tag pushed with `--follow-tags`.</deliverable>
    <deliverable type="source_map">`infra/aws/lambda/ci/lambda-source-map.json` entry updated for the router Lambda.</deliverable>
    <deliverable type="test">Integration test matrix (4 cases) executed and logged.</deliverable>
    <deliverable type="document">Session log at `org/tier2_senior/0.7.0_AE_CloudOps/logs/2026-04-{NN}/advi_profil_004_scoping.md` with prerequisite verification, regex patterns, CloudWatch event shape, integration test output, deploy tag, and compiler tools log.</deliverable>
  </deliverables>

  <do_not>
    <rule>Do NOT start before .002 is fully deployed. Blocking precondition.</rule>
    <rule>Do NOT modify backend Lambdas (platinum-summary handler, timeseries handler, etc.). The router is the choke point.</rule>
    <rule>Do NOT widen to other endpoints outside the three paths listed. Future scoping expansions are separate TOs.</rule>
    <rule>Do NOT skip the structured denial logging. Detection post-ship depends on it.</rule>
    <rule>Do NOT use `aws lambda update-function-code`. All deploys via Terraform.</rule>
    <rule>Do NOT remove or weaken the existing firmId scoping rule. .004 is strictly additive.</rule>
  </do_not>
</task_order>
