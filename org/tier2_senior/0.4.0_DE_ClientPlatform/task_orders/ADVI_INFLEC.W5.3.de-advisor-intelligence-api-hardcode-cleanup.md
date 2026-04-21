<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-04-21-inflec-w5.3-api-hardcode-cleanup</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DE_ClientPlatform</issued_to>
    <date>2026-04-21</date>
    <status>complete</status>
    <project_code>ADVI_INFLEC</project_code>
  </metadata>

  <objective>
    Remove 10 hardcoded `': '49financial'` default-fallback instances in `portal/src/api/endpoints/advisor-intelligence.ts`. Replace each with JWT-derived firmId from AuthContext (`allowedFirmIds` claim). This is structural for multi-tenant correctness — Inflection users hitting `firmId=49financial` default would read from the wrong bucket (opal-data-bd instead of opal-data-inf).
  </objective>

  <context>PRD §4.2 row 6. CTO §8.1 grep: `grep -c ": '49financial'" portal/src/api/endpoints/advisor-intelligence.ts` = 10. Each is a default-fallback when firmId is not passed. After W5.0.4 refactor, firmId should be extracted from AuthContext and threaded through the component tree — these defaults should be replaced with proper JWT derivation. If any default is legitimately needed (e.g., unauthenticated demo mode), replace with `null` or an error throw, not `'49financial'`.</context>

  <compiler_tools_mandate>
    Phase 1:
    <run>grep -n "': '49financial'" portal/src/api/endpoints/advisor-intelligence.ts</run>
    <expect>10 hits. Review each in context before changing.</expect>

    Phase 3:
    <run>grep -c "49financial" portal/src/api/endpoints/advisor-intelligence.ts</run>
    <expect>0 hardcoded defaults remaining.</expect>
    <run>bunx tsc -b portal/</run>
    <expect>Zero TS errors.</expect>
    <run>/frontend-dev (49F golden path)</run>
    <expect>PASS — 49F still resolves its firmId correctly (from JWT, not hardcode).</expect>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    shared_resource: `advisor-intelligence.ts` — no concurrent TO touches this file.
    last_write_owner: 0.4.0_DE_ClientPlatform.
  </cross_domain_coordination>

  <acceptance_criteria>
    1. 0 hardcoded `'49financial'` defaults remaining in advisor-intelligence.ts.
    2. firmId derived from AuthContext JWT claim (or useAuth hook) at each former hardcode site.
    3. TypeScript clean.
    4. /frontend-dev 49F golden path: PASS (JWT carries firmId=49financial, requests route correctly).
    5. Session log with before/after grep counts.
  </acceptance_criteria>

  <scope>
    <files><file action="modify">portal/src/api/endpoints/advisor-intelligence.ts</file></files>
  </scope>

  <requirements>
    <requirement id="1">Each hardcode replaced with JWT-derived firmId — no empty string or null that silently breaks requests.</requirement>
    <requirement id="2">If a default is truly needed (unauthenticated route), replace with explicit error throw, not '49financial'.</requirement>
    <requirement id="3">/frontend-dev 49F regression pass before marking complete.</requirement>
  </requirements>

  <deliverables>
    <deliverable type="commit">advisor-intelligence.ts with hardcodes removed.</deliverable>
    <deliverable type="document">Session log with grep before/after.</deliverable>
  </deliverables>

  <do_not>
    <rule>Do NOT replace '49financial' with another hardcoded firm literal.</rule>
    <rule>Do NOT skip /frontend-dev 49F regression.</rule>
  </do_not>
</task_order>
