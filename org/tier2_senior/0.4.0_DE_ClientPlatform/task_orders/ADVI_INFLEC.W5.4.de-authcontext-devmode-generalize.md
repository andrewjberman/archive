<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-04-21-inflec-w5.4-authcontext-devmode</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DE_ClientPlatform</issued_to>
    <date>2026-04-21</date>
    <status>staged</status>
    <project_code>ADVI_INFLEC</project_code>
  </metadata>

  <objective>
    Generalize `portal/src/contexts/AuthContext.tsx` dev-mode: replace 3 hardcoded `'49financial'` instances (L488, L498, L512) with a per-firmId dev toggle supporting both `49financial` and `inflection`. Lower priority than W5.3 but required before Inflection portal smoke tests can use dev-mode login.
  </objective>

  <context>PRD §4.2 row 7. Dev-mode bypass is for local development only. Approach: add a `DEV_FIRM_ID` env var (defaults to `'49financial'`) so any dev can set `DEV_FIRM_ID=inflection` to test Inflection locally. Or: a toggle in a `.env.local` file. DE decides the implementation approach — just ensure both firms work.</context>

  <compiler_tools_mandate>
    Phase 1: <run>grep -n "49financial" portal/src/contexts/AuthContext.tsx</run> — confirm L488/L498/L512 hit count (3).
    Phase 3: <run>bunx tsc -b portal/</run> — zero errors. <run>grep -c "'49financial'" portal/src/contexts/AuthContext.tsx</run> — 0.
  </compiler_tools_mandate>

  <cross_domain_coordination>
    shared_resource: AuthContext.tsx — no concurrent TO touches this file.
    last_write_owner: 0.4.0_DE_ClientPlatform.
  </cross_domain_coordination>

  <acceptance_criteria>
    1. 0 hardcoded '49financial' literals in AuthContext.tsx.
    2. Dev-mode supports firmId=49financial and firmId=inflection (via env var or toggle).
    3. TypeScript clean.
    4. Session log.
  </acceptance_criteria>

  <scope>
    <files><file action="modify">portal/src/contexts/AuthContext.tsx</file></files>
  </scope>

  <requirements>
    <requirement id="1">Production code path unchanged — dev-mode only.</requirement>
    <requirement id="2">Both 49financial and inflection dev-mode work.</requirement>
  </requirements>

  <deliverables>
    <deliverable type="commit">AuthContext.tsx generalized.</deliverable>
    <deliverable type="document">Session log.</deliverable>
  </deliverables>

  <do_not><rule>Do NOT change production auth logic.</rule></do_not>
</task_order>
