<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-04-21-inflec-w5.6-auth-flow-validation</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DT_ClientPlatform</issued_to>
    <date>2026-04-21</date>
    <status>complete</status>
    <project_code>ADVI_INFLEC</project_code>
  </metadata>

  <objective>
    Validate the full Inflection auth flow end-to-end: Inflection user sign-in → auth-handler resolves `opal-partner-inflection` table (via W1.5 generalization) → JWT carries `allowedFirmIds=inflection` + advisorKey + advisorRole + firmRole → API GW → opal-partners-data Lambda → correct `opal-data-inf` S3 bucket → response returned.
  </objective>

  <context>PRD §9 W5.6. This is the gate before smoke tests (W5.7). Blocked on W1.5 (auth-handler generalization) + W1.6/W1.7 (edge maps) + W5.5 (users provisioned). DT uses the Cognito sign-in flow or the portal login form with the test user provisioned in W5.5.</context>

  <compiler_tools_mandate>
    Phase 3:
    <run>comp-routes auth-map</run>
    <expect>All /api/scoped/advisor-intelligence/* behind edge JWT. No new unauthenticated routes.</expect>
    Decode the Inflection test JWT:
    <run>echo $JWT_B64 | base64 -d | python -m json.tool</run>
    <expect>allowedFirmIds contains 'inflection'. advisorKey, advisorRole, firmRole present for non-admin users.</expect>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    required_action: "Blocked on W1.5 + W1.6 + W1.7 + W5.5. All four must be complete before this auth flow test is meaningful."
  </cross_domain_coordination>

  <acceptance_criteria>
    1. Inflection user can sign in via Cognito (portal login or direct Cognito call).
    2. Decoded JWT: `allowedFirmIds=inflection`, `firmId=inflection`, `advisorKey` non-null for non-admin user.
    3. API call `GET /api/scoped/advisor-intelligence/platinum/firm/leaderboard.json?firmId=inflection` → 200 (or expected 404 if platinum not yet written — 403 is a failure).
    4. opal-partners-data Lambda logs confirm `get_firm_bucket('inflection') = opal-data-inf`.
    5. 49F user login still works (regression).
    6. Session log with JWT decode, API curl output, Lambda CloudWatch log excerpt.
  </acceptance_criteria>

  <scope>
    <files>
      <file action="reference">infra/aws/opalinvest_dev/lambda/auth-handler/src/db.ts (deployed in W1.5)</file>
      <file action="reference">infra/aws/lambda-edge/auth-validator-edge/index.mjs (deployed in W1.6)</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">Blocked on W1.5 + W1.6 + W1.7 + W5.5.</requirement>
    <requirement id="2">JWT decode is mandatory — confirm all expected claims present before proceeding to W5.7.</requirement>
    <requirement id="3">403 on any Inflection API call = auth flow broken. Investigate before proceeding.</requirement>
  </requirements>

  <deliverables>
    <deliverable type="document">Session log with JWT decode, curl outputs, Lambda log excerpt.</deliverable>
  </deliverables>

  <do_not>
    <rule>Do NOT proceed to W5.7 if any Inflection API call returns 403.</rule>
    <rule>Do NOT skip 49F regression test.</rule>
  </do_not>
</task_order>
