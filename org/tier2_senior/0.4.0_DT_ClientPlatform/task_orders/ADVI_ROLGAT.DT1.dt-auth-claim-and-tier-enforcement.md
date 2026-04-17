<task_order>
  <metadata>
    <id>0.4.0_DE_ClientPlatform-2026-04-17-advi-rolgat-dt1</id>
    <issued_by>0.4.0_DE_ClientPlatform</issued_by>
    <issued_to>0.4.0_DT_ClientPlatform</issued_to>
    <date>2026-04-17</date>
    <status>complete</status><!-- 2026-04-17 DT: portal-auth-v1.13.0 + partners-api-v1.16.1 deployed. Smoke 21/21 PASS. Log: logs/2026-04-17/advi_rolgat_dt1.md -->
    <completion_summary>
      Deployed ADVI_ROLGAT.DT1 tier enforcement across all three backend gates:
      - auth-validator-edge v12: X-Advisor-Role header + tier gate (401 on deny)
      - shared-advisor-router v13: defense-in-depth tier + L1 artifact scope
      - opal-partners-data v2.11: tier gate + L1 advisor scope + implementor payload strip
      Backfill applied to opal-partner-49financial (4 rows; 1 update: Luke -> implementor).
      Smoke test 21/21 PASS including implementor strip verification.
      Tags: portal-auth-v1.13.0 (8ce0bbca), partners-api-v1.16.1 (3a186703).
    </completion_summary>
    <project_code>ADVI_ROLGAT</project_code>
  </metadata>

  <objective>
    Introduce an `advisorRole` JWT claim and enforce L0/L1/L2 data tiering at all three backend gates (auth-validator-edge, shared-advisor-router, opal-partners-data Lambda). This is the trust boundary — frontend gating is cosmetic. Per ARCHITECTURE.md Principle 2: backend enforces. If DT1 leaks, the whole project leaks.
  </objective>

  <context>
    PRD: `docs/architecture/ADVI_ROLGAT_PRD.md` r2 (2026-04-17) — sections 2, 3, 4, 7b. Role enum, tier map, payload-strip rules for implementor, and smoke-test expectations. READ r2 — it supersedes r1. Andrew resolved the three open questions (§8): 4-role enum (no additional_advisor), local_ops = RCU Implementor + Local Ops SL populated only, architects DO NOT cross-advisor-drill (admin-only).

    Current auth surface:
    - `infra/aws/auth/validator.ts` — JWT validation lib imported by Lambdas.
    - `portal/src/contexts/AuthContext.context.ts` — Claims TS interface (DE1 extends this, you do NOT; keep the two in sync by email or MCP).
    - `opal-partner-{firmId}` DynamoDB — per-user firm record; holds `firmRole` today. Add `advisorRole` field here.
    - `infra/aws/lambda-edge/auth-validator-edge/` — viewer-request Lambda@Edge, injects `X-Firm-Id`.
    - `infra/aws/lambda/shared-advisor-router/index.mjs` — origin-request Lambda@Edge, currently only rewrites path.
    - API Gateway Lambda handlers (`opal-partners-data`, etc.) — data producers; route → tier mapping must match edge-level policy.

    Backfill resolution (PRD §2):
    1. RCU Role = Architect → `architect`
    2. RCU Role = Consultant → `consultant` (Local Ops SL presence does NOT change label)
    3. RCU Role = Implementor AND Local Ops SL Number populated → `local_ops`
    4. RCU Role = Implementor AND no Local Ops SL → `implementor`
    Partner-table users with no report match: default to `implementor` floor; log WARN per row for data-quality cleanup.

    Seed data: `C:\Users\AndrewBerman\Downloads\report1776352673541.xls` — HTML-formatted, 141 rows. Columns: Staff Profile Name | RCU Role | Schwab SL Number | Schwab SL Number (Local Ops). Parse with Python `html.parser` (openpyxl rejects HTML as .xls). Expected distribution: ~77 implementor + ~4 local_ops + ~30 consultant + ~30 architect — verify against your backfill output. Join to partner DynamoDB by Staff Profile Name → email mapping owned by AE / CRM — expect 49 Financial has an email<->Staff Profile table somewhere in partners CRM; if not, ship backfill by hand matching for the 141 rows and file a separate cleanup TO.

    Payload strip (PRD §3 L1): for `/advisors/{id}/book` with `advisorRole === 'implementor'`, strip the `clients` array AND cost-basis / tax / income fields from `PlatinumAdvisorSummary`. Keep aggregate metrics (AUA, accounts count, clients count, role_breakdown, small_account_count, fee headline). Frontend already uses `?.` guards so absent fields auto-hide panels.
  </context>

  <compiler_tools_mandate>
    Phase 1 — before writing:
      <run>comp-routes auth-map</run>
      <expect>Current AUTH MAP baseline. Note the WARN about custom_error_response 403->200 HTML — this is why you emit 401 on tier deny, not 403.</expect>
      <if_mismatch>If the auth-map has changed since this TO was written (new routes with AUTH or NO AUTH paths), flag before proceeding — the tier-policy table may need new rows.</if_mismatch>

      <run>comp-routes behaviors</run>
      <expect>23 behaviors. Review the 3 S3 advisor-intelligence behaviors (artifacts depth-2, artifacts depth-3, entities depth-3, *.json depth-1) — these need origin-request router tier enforcement.</expect>
      <if_mismatch>If behaviors have been added, update the router and tier policy table to cover them.</if_mismatch>

      <run>comp-iam service opal-partners-data</run>
      <expect>Current IAM baseline — no new boto3 calls expected unless you add a DynamoDB scope lookup for L2 client-belongs-to-advisor check.</expect>
      <if_mismatch>If you add new DynamoDB/S3 calls, run comp-iam gaps after the iam.tf update.</if_mismatch>

      <run>comp-blast lambda:opal-partners-data</run>
      <expect>Full downstream consumer list. All frontend endpoints should appear — confirm you have coverage.</expect>
      <if_mismatch>Any missing downstream = missing tier-policy row.</if_mismatch>

    Phase 2 — before committing:
      <run>comp-iam gaps</run>
      <expect>0 new gaps after iam.tf changes.</expect>
      <if_mismatch>Add missing permissions to iam.tf before terraform plan.</if_mismatch>

      <run>bash scripts/advi_rolgat_smoke.sh</run>
      <expect>All matrix cells match PRD §7b table. Commit the output to the session log.</expect>
      <if_mismatch>Any 200 where the table expects 401 = leak. Do not ship. Any 401 where the table expects 200 = over-deny. Fix both.</if_mismatch>

    Phase 3 — after committing + terraform apply:
      <run>comp-iam gaps</run>
      <expect>Still 0 after deploy — sanity check.</expect>
      <if_mismatch>Rollback.</if_mismatch>

      <run>comp-routes auth-map</run>
      <expect>No new "NO AUTH" rows introduced accidentally.</expect>
      <if_mismatch>Revert the CloudFront behavior.</if_mismatch>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    shared_resource: `portal/src/contexts/AuthContext.context.ts` (Claims interface)
    also_in_to: ADVI_ROLGAT.DE1
    last_write_owner: 0.4.0_DE_ClientPlatform (DE1 owns the TS interface change)
    required_action: Do NOT edit the portal Claims interface from DT1. The field you emit in the JWT and the field DE1 adds in TS must match exactly — `advisorRole: 'architect' | 'consultant' | 'local_ops' | 'implementor' | null`. Verify by reading DE1's commit before your merge. MCP to 0.4.0_DE_ClientPlatform if the shape you can actually emit differs from the PRD (e.g., DynamoDB backfill lands a different enum).

    shared_resource: `docs/architecture/ADVI_ROLGAT_PRD.md`
    also_in_to: ADVI_ROLGAT.DE1, ADVI_ROLGAT.RD1
    last_write_owner: 0.4.0_DE_ClientPlatform (PRD author)
    required_action: Read-only for DT. If PRD is wrong or underspecified, MCP 0.4.0_DE_ClientPlatform — do not edit in place and create divergent specs.
  </cross_domain_coordination>

  <acceptance_criteria>
    1. `opal-partner-49financial` table has `advisorRole` attribute populated for every item currently in the table. Backfill script committed at `scripts/advi_rolgat_backfill_49financial.py`. Distribution logged: counts for architect, consultant, local_ops, implementor. Expected approx ~30/30/4/77 from report (deviations documented with reason). Partner-table users with no report match default to `implementor` and are listed explicitly in the WARN section of the script output.
    2. Auth Lambda login + `/auth/me` emit `advisorRole` in the user payload (null for users without a partner record). Verified with curl in session log.
    3. JWT access token payload includes `advisorRole` claim. Decoded token pasted in session log.
    4. `auth-validator-edge` injects `X-Advisor-Role` and `X-Advisor-Id` headers on all authenticated requests. Verified by curl + CloudFront trace in session log.
    5. `auth-validator-edge` returns 401 (NOT 403) when `advisorRole` is insufficient for the request path. Tested for an L2 path with a consultant JWT.
    6. `shared-advisor-router` (origin-request) enforces tier on all S3 advisor-intelligence behaviors (artifacts depth-2, artifacts depth-3, entities depth-3, depth-1 *.json). Returns 401 on insufficient tier.
    7. `opal-partners-data` Lambda handler gates every route by tier AND (for L1/L2) by scope (advisorId / clientKey ownership). Returns 401 on insufficient tier, 401 on scope mismatch.
    8. **Payload strip verified**: `GET /api/scoped/advisor-intelligence/advisors/{advisorId}/book` with implementor JWT returns 200 AND response does NOT contain `clients` array AND does NOT contain cost-basis / tax / income fields. Same endpoint with consultant JWT returns full payload including `clients`. Documented in smoke-test output.
    9. `scripts/advi_rolgat_smoke.sh` runs all matrix cells from PRD §7b (four roles × each endpoint tier + payload-strip assertions). Exit 0. Output committed to the session log.
    10. `comp-iam gaps` shows 0 new gaps.
    11. `comp-routes auth-map` after deploy shows no regression.
    12. Session log with Compiler Tools table. Tagged git commit(s) per LAMBDA_DEPLOYMENT_PROTOCOL.md.
    13. MCP COMPLETE to 0.4.0_DE_ClientPlatform with JWT sample + smoke-test matrix + payload-strip diff (implementor vs consultant response body).
  </acceptance_criteria>

  <scope>
    <files>
      <file action="modify">infra/aws/auth/validator.ts</file>
      <file action="modify">infra/aws/auth/validator.py</file>
      <file action="modify">infra/aws/lambda-edge/auth-validator-edge/index.mjs</file>
      <file action="create">infra/aws/lambda-edge/auth-validator-edge/tier_policy.mjs</file>
      <file action="modify">infra/aws/lambda/shared-advisor-router/index.mjs</file>
      <file action="modify">infra/aws/lambda/opal-partners-data/</file>
      <file action="modify">infra/aws/terraform/{applicable pipeline}/iam.tf</file>
      <file action="create">scripts/advi_rolgat_backfill_49financial.py</file>
      <file action="create">scripts/advi_rolgat_smoke.sh</file>
      <file action="reference">docs/architecture/ADVI_ROLGAT_PRD.md</file>
      <file action="reference">portal/src/contexts/AuthContext.context.ts</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">Extend JWT payload with `advisorRole: 'architect' | 'consultant' | 'local_ops' | 'implementor' | null`. Add parseClaims path in both `validator.ts` and `validator.py`. Cached public-key path unchanged.</requirement>
    <requirement id="2">Auth Lambda login + /auth/me read `opal-partner-{firmId}` record and emit `advisorRole`. If record lacks the field, emit null. Do NOT default to a permissive role.</requirement>
    <requirement id="3">Create `tier_policy.mjs` in auth-validator-edge: export a pure function `requiredTierForUri(uri: string): 'L0'|'L1'|'L2'|null`. Policy table must match PRD §3 exactly. Import into origin-request router and (via Layer or vendoring) into opal-partners-data.</requirement>
    <requirement id="4">auth-validator-edge evaluates `requiredTierForUri(request.uri)` against claim. Deny with HTTP 401 on mismatch. Allow if admin bypass (`firmRole==='admin'` OR `firmId==='opal-capital'`). Inject `X-Advisor-Role` and `X-Advisor-Id` headers on allow.</requirement>
    <requirement id="5">shared-advisor-router (origin-request) reads `X-Advisor-Role`/`X-Advisor-Id` from the request, runs `requiredTierForUri`, and for L1/L2 checks that `{advisorId}` path param matches `X-Advisor-Id` unless admin. Deny with 401.</requirement>
    <requirement id="6">opal-partners-data handler: (a) tier check via `tier_policy.mjs`, 401 on mismatch; (b) for L1 `/advisors/{id}/book` with `advisorRole === 'implementor'`, STRIP the `clients` array and cost-basis / tax / income fields from `PlatinumAdvisorSummary` before returning; keep aggregate metrics + role_breakdown + small_account_count + fee headline; (c) for L2 client/account routes, look up client→advisor mapping and reject 401 if client does not belong to `claims.advisorId`'s book. Admin bypass = full payload, no strip, no scope check.</requirement>
    <requirement id="7">Payload strip — DT1 picks and documents one of: (a) single handler branch that redacts fields, OR (b) dual S3 keys per advisor (`book_overview.json` + `book_full.json`) with router picking by role. Session log notes which and why. Either is acceptable if the smoke test verifies an implementor response contains zero client-level data.</requirement>
    <requirement id="8">Backfill script: parse spreadsheet HTML, apply resolution precedence (architect > consultant > local_ops > implementor), write advisorRole attribute. Idempotent. Dry-run default, `--apply` to write. WARN-log every partner-table email with no report match.</requirement>
    <requirement id="9">Smoke-test script: forge a JWT for each of the 4 roles + admin, curl each endpoint, assert status + (for L1 book) payload shape. Matrix prints PASS/FAIL per cell, exits non-zero on any mismatch.</requirement>
    <requirement id="10">Update API Gateway authorizer to pass `advisorRole` through to Lambda `event.requestContext.authorizer.claims`.</requirement>
    <requirement id="11">After terraform apply, tag per LAMBDA_DEPLOYMENT_PROTOCOL.md — check `git tag -l` before picking next version (memory Pipeline Tag Versioning rule).</requirement>
  </requirements>

  <deliverables>
    <deliverable type="commit">JWT claim addition (validator.ts + validator.py + any Layer rebuild).</deliverable>
    <deliverable type="commit">Auth Lambda + API Gateway authorizer (claim emission + passthrough).</deliverable>
    <deliverable type="commit">auth-validator-edge + tier_policy.mjs + shared-advisor-router enforcement.</deliverable>
    <deliverable type="commit">opal-partners-data handler tier + scope gate.</deliverable>
    <deliverable type="commit">iam.tf + terraform apply + tag + push --follow-tags.</deliverable>
    <deliverable type="commit">Backfill script + smoke-test script + smoke-test output captured in session log.</deliverable>
    <deliverable type="document">Session log under `org/tier2_senior/0.4.0_DT_ClientPlatform/logs/{YYYY-MM-DD}/advi_rolgat_dt1.md` with Compiler Tools section and smoke-test matrix.</deliverable>
    <deliverable type="document">MCP COMPLETE message to 0.4.0_DE_ClientPlatform citing JWT sample, matrix exit 0, and commit hashes.</deliverable>
  </deliverables>

  <do_not>
    <rule>Do NOT default null `advisorRole` to anything permissive. Null = local_ops-equivalent = most restrictive.</rule>
    <rule>Do NOT return HTTP 403 for tier deny. The CloudFront custom_error_response (comp-routes behaviors WARN) intercepts 403 to 200 /index.html. Use 401.</rule>
    <rule>Do NOT edit `portal/src/contexts/AuthContext.context.ts`. That is DE1's scope. If the actual emitted shape differs from PRD, MCP 0.4.0_DE — do not fork specs.</rule>
    <rule>Do NOT use `aws lambda update-function-code`. Terraform only, per CLAUDE.md deployment rule 1.</rule>
    <rule>Do NOT inline-pip into Lambda source dirs. Use the existing shared-infra layer mechanism if you need additional deps (unlikely for this TO).</rule>
    <rule>Do NOT skip the smoke test. It is the acceptance gate — the three-gate defense is only provable by running it end-to-end.</rule>
    <rule>Do NOT push to main / PROD. Working branch is CLOUD. Portal submodule is not touched from this TO.</rule>
  </do_not>
</task_order>
