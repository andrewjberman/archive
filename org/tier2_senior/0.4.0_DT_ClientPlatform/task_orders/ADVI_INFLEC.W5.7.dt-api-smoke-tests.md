<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-04-21-inflec-w5.7-smoke-tests</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DT_ClientPlatform</issued_to>
    <date>2026-04-21</date>
    <status>staged</status>
    <project_code>ADVI_INFLEC</project_code>
  </metadata>

  <objective>
    Smoke-test all `/api/scoped/advisor-intelligence/*` endpoints with an Inflection JWT. Verify: 200 on all firm-scoped endpoints, 200 on own-advisor endpoints for non-admin, 403 on other-advisor endpoints for non-admin (ADVI_PROFIL.004a/.004c scoping still in effect).
  </objective>

  <context>PRD §9 W5.7. Extends W5.6 with a broader endpoint sweep. DT uses the same Inflection test JWT from W5.6. Key endpoints: leaderboard.json, partner_analytics.json, timeseries/*.json, advisors/{id}/*.json (own vs other). Blocked on W5.6 auth flow validation.</context>

  <compiler_tools_mandate>
    Phase 3:
    <run>comp-routes behaviors</run>
    <expect>CF behaviors unchanged. No new unauthenticated behaviors.</expect>
    Curl matrix (all against Inflection JWT):
    1. GET /api/scoped/advisor-intelligence/platinum/firm/leaderboard.json?firmId=inflection → 200
    2. GET /api/scoped/advisor-intelligence/platinum/firm/partner_analytics.json?firmId=inflection → 200
    3. GET /api/scoped/advisor-intelligence/platinum/advisors/{own_id}/timeseries.json → 200 (non-admin)
    4. GET /api/scoped/advisor-intelligence/platinum/advisors/{other_id}/timeseries.json → 403 (non-admin)
    5. GET /api/scoped/advisor-intelligence/platinum/advisors/{any_id}/timeseries.json → 200 (admin JWT)
    6. GET ...?firmId=49financial with Inflection JWT → 403 (cross-firm blocked by edge firmId check)
  </compiler_tools_mandate>

  <cross_domain_coordination>
    required_action: "Blocked on W5.6. If endpoint 6 (cross-firm firmId mismatch) doesn't return 403, escalate to CTO before proceeding."
  </cross_domain_coordination>

  <acceptance_criteria>
    1. All 6 curl cases pass as expected above.
    2. Cross-firm isolation confirmed (case 6 = 403).
    3. comp-routes behaviors: unchanged.
    4. Session log with all curl outputs + response codes.
  </acceptance_criteria>

  <scope>
    <files><file action="reference">infra/aws/lambda-edge/auth-validator-edge/index.mjs (W1.6)</file></files>
  </scope>

  <requirements>
    <requirement id="1">Blocked on W5.6.</requirement>
    <requirement id="2">Cross-firm isolation test (case 6) is mandatory — not optional.</requirement>
    <requirement id="3">If cross-firm isolation fails, STOP and escalate to CTO immediately.</requirement>
  </requirements>

  <deliverables>
    <deliverable type="document">Session log with curl matrix output.</deliverable>
  </deliverables>

  <do_not>
    <rule>Do NOT skip cross-firm isolation test.</rule>
    <rule>Do NOT accept partial results.</rule>
  </do_not>
</task_order>
