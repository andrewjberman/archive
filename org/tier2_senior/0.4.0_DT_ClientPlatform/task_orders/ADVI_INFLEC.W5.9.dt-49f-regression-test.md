<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-04-21-inflec-w5.9-49f-regression</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DT_ClientPlatform</issued_to>
    <date>2026-04-21</date>
    <status>complete</status>
    <project_code>ADVI_INFLEC</project_code>
  </metadata>

  <objective>
    Full 49F regression test after all ADVI_INFLEC shared-infra changes: auth-handler generalization (W1.5), Lambda@Edge FIRM_BUCKET_MAP updates (W1.6/W1.7), portal firmAccess.ts + advisor-intelligence.ts + AuthContext changes (W5.2/W5.3/W5.4). Confirm existing 49F users continue to work end-to-end without regression.
  </objective>

  <context>PRD §9 W5.9. The critical guard: adding Inflection MUST NOT break 49F. Every shared-infra change touched a code path that 49F depends on. This TO is the final quality gate before COO can declare ADVI_INFLEC v1 complete.</context>

  <compiler_tools_mandate>
    Phase 3:
    <run>comp-routes auth-map</run> — no route regressions.
    49F user curl matrix:
    1. 49F admin login → JWT has allowedFirmIds=49financial → 200 on all endpoints.
    2. 49F non-admin → own-advisor endpoints → 200. Other-advisor → 403.
    3. 49F firmId → opal-data-bd bucket (not opal-data-inf).
    4. /frontend-dev AdvisorIntelligence constitution with 49F firmId → PASS.
  </compiler_tools_mandate>

  <cross_domain_coordination>
    required_action: "Blocked on W5.6 + W5.7 (Inflection smoke tests done first). If any 49F regression found: flag immediately to COO + CTO, revert the offending change, and re-test before closing."
  </cross_domain_coordination>

  <acceptance_criteria>
    1. 49F JWT: allowedFirmIds=49financial, bucket resolves to opal-data-bd.
    2. All 49F API endpoints return 200 (or expected 404 for empty data).
    3. ADVI_PROFIL.004a/.004c scoping still works for 49F non-admin users.
    4. /frontend-dev 49F constitution: PASS.
    5. Session log with full curl matrix + /frontend-dev pass record.
  </acceptance_criteria>

  <scope>
    <files><file action="reference">infra/aws/lambda-edge/auth-validator-edge/index.mjs</file></files>
  </scope>

  <requirements>
    <requirement id="1">Blocked on W5.7.</requirement>
    <requirement id="2">Any 49F regression = STOP, escalate immediately, do NOT mark complete.</requirement>
    <requirement id="3">This is the final acceptance gate for ADVI_INFLEC v1.</requirement>
  </requirements>

  <deliverables>
    <deliverable type="document">Session log with curl matrix + /frontend-dev output. MCP COO when complete (ADVI_INFLEC v1 close signal).</deliverable>
  </deliverables>

  <do_not>
    <rule>Do NOT mark complete if any 49F endpoint regresses.</rule>
    <rule>Do NOT skip /frontend-dev 49F pass.</rule>
  </do_not>
</task_order>
