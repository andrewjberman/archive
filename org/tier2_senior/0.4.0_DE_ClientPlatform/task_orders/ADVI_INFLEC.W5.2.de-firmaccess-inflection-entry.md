<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-04-21-inflec-w5.2-firmaccess</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DE_ClientPlatform</issued_to>
    <date>2026-04-21</date>
    <status>staged</status>
    <project_code>ADVI_INFLEC</project_code>
  </metadata>

  <objective>
    Add `'inflection': new Set(['/advisor-intelligence', ...])` entry to `FIRM_ALLOWED_PATHS` in `portal/src/lib/firmAccess.ts`. Controls which portal pages Inflection users can access (default deny-all without this entry). Match the 49F allowed paths set unless Andrew specifies a subset.
  </objective>

  <context>PRD §4.2 row 5 + ONBOARDING.md §5 Step 4. One-line add. Parallelizable with W5.1 — no portal data dependency.</context>

  <compiler_tools_mandate>
    Phase 1: <run>cat portal/src/lib/firmAccess.ts</run> — current FIRM_ALLOWED_PATHS structure.
    Phase 3: <run>bunx tsc -b portal/</run> — zero TS errors. <run>comp-transform schema-check AdvisorIntelligence</run> — 0 MISSING (firmAccess.ts change shouldn't affect rendered fields).
  </compiler_tools_mandate>

  <cross_domain_coordination>
    shared_resource: `portal/src/lib/firmAccess.ts` — no concurrent TO touches this file.
    last_write_owner: 0.4.0_DE_ClientPlatform.
    required_action: "PRD §10 Q13 (user domain gating) is OPEN — explicit provisioning vs automatic @inflectionwealthmgmt.com gating. firmAccess.ts controls page-access after auth succeeds; domain gating is separate (auth-handler / W1.5 territory). This TO handles page-access scope only."
  </cross_domain_coordination>

  <acceptance_criteria>
    1. `FIRM_ALLOWED_PATHS['inflection']` entry present with `/advisor-intelligence` at minimum.
    2. TypeScript clean.
    3. Session log.
  </acceptance_criteria>

  <scope>
    <files><file action="modify">portal/src/lib/firmAccess.ts</file></files>
  </scope>

  <requirements>
    <requirement id="1">Mirror 49F allowed paths unless Andrew specifies otherwise for Inflection.</requirement>
    <requirement id="2">Commit with --only; author 0.4.0_DE_ClientPlatform.</requirement>
  </requirements>

  <deliverables>
    <deliverable type="commit">firmAccess.ts with inflection entry.</deliverable>
    <deliverable type="document">Session log.</deliverable>
  </deliverables>

  <do_not><rule>Do NOT remove or narrow 49F entry.</rule></do_not>
</task_order>
