<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-04-10-profil-scoping-004c</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <co_owner>0.4.0_DT_ClientPlatform</co_owner>
    <date>2026-04-10</date>
    <status>staged</status>
    <project_code>ADVI_PROFIL</project_code>
  </metadata>

  <objective>
    Extend `shared-advisor-router` Lambda@Edge with account-id and relationship-id scoping, using the ownership map artifact published by .004b. Covers: (a) `/api/scoped/advisor-intelligence/platinum/accounts/{accountId}/summary.json` (S3-direct origin), (b) `/api/scoped/partners/books/relationship/{relationshipId}/platinum-summary` (API GW origin). Rule: look up the ownership map, find `advisors[jwt.advisorId]`, check whether `{accountId}` or `{relationshipId}` is in the matching set. 403 on miss. Admin bypass preserved. This is Wave 2c and ships after .004a (shared helper) AND .004b (ownership map artifact exists) AND .005 (non-admin drill paths are only reachable via Book view).
  </objective>

  <context>
    .004a covered the simple case (path parameter IS the advisor id). .004c covers the harder case (path parameter is an account or relationship id — enforcement requires a join).

    Route map from CTO comp-routes audit:

    | Endpoint | URL | CF Behavior | Origin | Path-key |
    |---|---|---|---|---|
    | getPlatinumAccountSummary | `/api/scoped/advisor-intelligence/platinum/accounts/{accountId}/summary.json` | `/api/scoped/advisor-intelligence/*.json` | `S3-opal-data-bd` (edge-only) | `{accountId}` |
    | getPlatinumClientSummary | `/api/scoped/partners/books/relationship/{relationshipId}/platinum-summary?firmId=...` | `/api/scoped/partners/*` | `APIGateway-portal` | `{relationshipId}` |

    S3-direct paths are edge-only: `shared-advisor-router` is the only control point. API GW paths could technically be enforced at the API GW authorizer, but we keep everything in the edge router for a single choke point.

    Ownership map (from .004b):
    ```json
    {
      "schema_version": 1,
      "generated_at": "ISO8601",
      "advisors": {
        "{advisor_id}": {
          "accounts": ["{account_id}", ...],
          "relationships": ["{relationship_id}", ...]
        }
      }
    }
    ```
    Read strategy: CloudFront-cached S3 read with ~1-minute TTL (or whatever the platinum CloudFront behavior enforces). Rough cost: 1 S3 GET per edge location per minute. Bounded.

    Enforcement pseudocode:
    ```
    if isAdmin(jwt): bypass
    if jwt.advisorId == null: reject 403

    map = fetch_ownership_map()  # CloudFront-cached
    if map.schema_version != 1: reject 500 (schema mismatch — ops alert)

    entry = map.advisors[jwt.advisorId]
    if entry == null: reject 403  # advisor not in map (inactive? new?)

    if path matches /api/scoped/advisor-intelligence/platinum/accounts/{id}/...:
      if {id} not in entry.accounts: reject 403
    elif path matches /api/scoped/partners/books/relationship/{id}/...:
      if {id} not in entry.relationships: reject 403
    ```

    Dependency ordering:
    - .004a must ship first → establishes the reusable path-matching + advisor-check helper.
    - .004b must ship first AND the first map must be populated on S3 (requires a gold run after .004b code deploy).
    - .005 should land before .004c strictly enforces — otherwise non-admins have no legitimate path to the account/relationship endpoints through the UI anyway, and .004c is a pure defense layer. However, .004c can still ship before .005 for belt-and-suspenders.

    Schema version check: if the map version does not match what .004c expects, reject with 500 and emit an ops alert. This catches the case where .004b schema gets bumped without coordinating .004c.
  </context>

  <compiler_tools_mandate>
    Phase 1 (before writing):
    - Verify .004a is fully deployed (shared-infra-v1.6.{N+1} or wherever it landed). Read the .004a session log to understand the helper design.
    - Verify .004b has populated at least one ownership map at the agreed S3 key. `aws s3 ls s3://opal-data-bd/platinum/shared/advisor_ownership.json` returns non-empty. Cat the file, confirm schema_version == 1.
    - `comp-routes trace getPlatinumAccountSummary` and `comp-routes trace getPlatinumClientSummary` — re-confirm the route map hasn't drifted.
    - `comp-blast shared-advisor-router` — re-verify downstream.
    - Read the .004a helper. Design the extension: (a) add map-fetch step, (b) add account/relationship path patterns, (c) add join check.

    Phase 2 (during implementation):
    - Add path patterns:
      - `^/api/scoped/advisor-intelligence/platinum/accounts/([^/]+)/.*\.json$`
      - `^/api/scoped/partners/books/relationship/([^/]+)/.*$`
    - Add ownership map fetch: use the existing S3 GET pattern in the router if present; add one if not. Cache in-process for the Lambda@Edge instance lifetime OR rely entirely on CloudFront-edge caching.
    - Schema version check: reject with 500 + structured alert log if `schema_version != 1`.
    - Missing advisor in map: reject with 403 + structured denial log (distinct event from "id mismatch" — helps diagnose stale map vs attack).
    - Account/relationship id lookup: straight `in` check against the respective array. Arrays are small (~50 accounts, ~20 relationships per advisor) so O(n) is fine.
    - Reuse the .004a helper for the path-parse + admin-bypass + null-advisor checks. Only the "does this id belong to this advisor" step is new logic.
    - Structured logging: `log.warn("advisor_scoping_denied", {..., rule: "004c", resourceType: "account" | "relationship", pathId: "{id}"})`.

    Phase 3 (after deploy):
    - Integration test matrix (all curls logged):
      1. Non-admin A → `/api/scoped/advisor-intelligence/platinum/accounts/{A-owned account id}/summary.json` → 200
      2. Non-admin A → `/api/scoped/advisor-intelligence/platinum/accounts/{A-not-owned account id}/summary.json` → 403
      3. Non-admin A → `/api/scoped/partners/books/relationship/{A-owned relationship id}/platinum-summary` → 200
      4. Non-admin A → `/api/scoped/partners/books/relationship/{A-not-owned relationship id}/platinum-summary` → 403
      5. Admin → any of the above → 200
      6. Non-admin with `jwt.advisorId == null` → any of the above → 403
      7. Schema mismatch simulation (temporarily bump the map's schema_version to 99 in a dev bucket) → 500 with ops alert. Revert immediately.
    - Verify CloudWatch structured events for each 403 and the 500.
    - `comp-routes --update` after deploy.
  </compiler_tools_mandate>

  <cross_domain_coordination>
    shared_resource: `shared-advisor-router` Lambda@Edge — .004a writes helper; .004c extends with ownership-map lookup. Do NOT duplicate the path-matching or admin-bypass logic.
    shared_resource: `platinum/shared/advisor_ownership.json` — .004b writes; .004c reads at edge. Schema contract is frozen at schema_version 1.
    shared_resource: CloudFront behavior for `platinum/**` — existing, no change expected.
    last_write_owner: 0.7.0_AE_CloudOps for router + Terraform. 0.4.0_DS_ClientPlatform for the ownership map.
    required_action: "Do NOT start until .004a is deployed AND .004b has populated at least one ownership map on S3. Verify both before touching code. Coordinate CloudFront invalidation timing with DT. If the schema version check trips at runtime, that is a STOP-THE-LINE event — immediately revert .004b schema change or roll back .004c."
  </cross_domain_coordination>

  <acceptance_criteria>
    1. **Prerequisites verified:** .004a deployed (tag present), .004b ownership map populated on S3 (file exists, schema_version == 1). Both logged.
    2. **Path patterns added:** Two new regexes for account and relationship paths, commented with origin and CF behavior.
    3. **Helper reused:** .004a path-parse + admin-bypass + null-advisor helper is called from .004c. No duplicated logic.
    4. **Map fetch + cache:** Router reads the map from the agreed S3 key. In-process cache or CloudFront-edge cache (pick one, document). TTL documented.
    5. **Schema version check:** If `schema_version != 1`, reject with 500 and emit structured ops alert. Verified via simulation in Phase 3.
    6. **Missing advisor rejection:** If `advisors[jwt.advisorId] == null`, reject with 403 and emit distinct structured log event ("advisor_not_in_map" or similar) separate from "id mismatch".
    7. **Account/relationship in-set check:** Straight `in` lookup against the arrays. No hashing required at this scale.
    8. **Integration test matrix (7 cases) passed:** All curls logged with response codes and CloudWatch event excerpts.
    9. **Lambda deploy via standard protocol:** Terraform 0-diff, source map updated, `shared-infra-v1.6.{next}` tag pushed with `--follow-tags`.
    10. **No regression on .004a cases:** Non-admin A → own advisor endpoint still 200. Admin bypass still works. Existing firmId scoping still works.
    11. **Session log:** Includes prerequisite verification, path patterns, helper extension, cache strategy, integration test matrix, schema-mismatch simulation, deploy tag, invalidation id, and compiler tools log.
  </acceptance_criteria>

  <scope>
    <files>
      <file action="modify">infra/aws/lambda/{shared-advisor-router path}/lambda_function.py</file>
      <file action="update">infra/aws/lambda/ci/lambda-source-map.json</file>
      <file action="reference">.004a helper (extended, not duplicated)</file>
      <file action="reference">platinum/shared/advisor_ownership.json (read-only at edge)</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">Do NOT start until .004a is deployed AND .004b has populated the ownership map. Verify both.</requirement>
    <requirement id="2">Reuse the .004a helper for path-parse + admin-bypass + null-advisor checks. Duplicated logic is a QA failure.</requirement>
    <requirement id="3">Schema version check is MANDATORY. A mismatch is a stop-the-line event.</requirement>
    <requirement id="4">Missing advisor in map rejects with 403 (not 500) because the more common cause is a newly-created advisor who hasn't been picked up by the next gold run yet. Log distinctly from "id mismatch" to help diagnose.</requirement>
    <requirement id="5">In-process cache OR CloudFront-edge cache for the map fetch — pick one and document the TTL. Do not hit S3 on every request.</requirement>
    <requirement id="6">Standard Lambda deployment protocol. No `aws lambda update-function-code`.</requirement>
    <requirement id="7">Structured denial logging mandatory with `rule: "004c"` and `resourceType: "account" | "relationship"`.</requirement>
    <requirement id="8">Do NOT modify the ownership map schema. .004b owns it. If the schema needs to change, that's a coordinated follow-up TO.</requirement>
    <requirement id="9">.005 is a soft dependency (non-admin UI path reaches these endpoints after .005 lands), but .004c can ship independently for defense in depth.</requirement>
  </requirements>

  <deliverables>
    <deliverable type="commit">Router Lambda modified with .004c enforcement. Committed with `--author=0.7.0_AE_CloudOps`.</deliverable>
    <deliverable type="tag">`shared-infra-v1.6.{next}` tag pushed.</deliverable>
    <deliverable type="source_map">lambda-source-map.json updated.</deliverable>
    <deliverable type="test">Integration test matrix (7 cases) executed and logged, including the schema-mismatch simulation.</deliverable>
    <deliverable type="document">Session log at `org/tier2_senior/0.7.0_AE_CloudOps/logs/2026-04-{NN}/advi_profil_004c_account_scoping.md` with prerequisite verification, helper extension, cache strategy, test matrix, and compiler tools log.</deliverable>
  </deliverables>

  <do_not>
    <rule>Do NOT start before .004a is deployed and .004b ownership map is populated.</rule>
    <rule>Do NOT duplicate .004a helper logic.</rule>
    <rule>Do NOT skip the schema version check.</rule>
    <rule>Do NOT hit S3 on every request. Cache the map.</rule>
    <rule>Do NOT modify the ownership map schema.</rule>
    <rule>Do NOT use `aws lambda update-function-code`.</rule>
    <rule>Do NOT weaken existing firmId scoping or admin bypass.</rule>
  </do_not>
</task_order>
