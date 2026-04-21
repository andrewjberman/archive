<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-04-21-inflec-w5.0.5-regression-test</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DE_ClientPlatform</issued_to>
    <date>2026-04-21</date>
    <status>staged</status>
    <project_code>ADVI_INFLEC</project_code>
  </metadata>

  <objective>
    Verify that the W5.0.4 refactor left all existing 49F portal functionality intact. Run the full `/frontend-dev` AdvisorIntelligence constitution with a 49F test user and confirm every surface renders without regression: leaderboard, books tab, distribution tab, timeseries, drill-down.
  </objective>

  <context>
    PRD §7.3. W5.0.4 moves files around the AdvisorIntelligence tree — if any import path broke or any 49F-specific override was accidentally left in `_shared/`, it shows up here. This is the green-light TO before W5 (Inflection portal integration) can proceed.
  </context>

  <compiler_tools_mandate>
    Phase 1:
    <run>comp-transform schema-check AdvisorIntelligence</run>
    <expect>0 MISSING fields post-refactor. Same or fewer UNUSED vs W5.0.4 baseline.</expect>

    Phase 3:
    <run>/frontend-dev (full AdvisorIntelligence constitution, 49F firmId)</run>
    <expect>PASS on all pages. No console errors, no undefined renders, no broken drills.</expect>

    <run>bunx tsc -b portal/</run>
    <expect>Zero TypeScript errors.</expect>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    <none/>
  </cross_domain_coordination>

  <acceptance_criteria>
    1. `/frontend-dev` AdvisorIntelligence constitution PASS with 49F firmId.
    2. Leaderboard, books tab, distribution tab, timeseries all render with 49F data.
    3. Zero TypeScript errors.
    4. `comp-transform schema-check AdvisorIntelligence` 0 MISSING.
    5. Session log with /frontend-dev output + schema check.
  </acceptance_criteria>

  <scope>
    <files>
      <file action="reference">portal/src/pages/AdvisorIntelligence/** (read-only in this TO)</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">Blocked on W5.0.4 completion.</requirement>
    <requirement id="2">If any regression found: patch in W5.0.4 scope, re-run this TO. Do NOT accept partial PASS.</requirement>
  </requirements>

  <deliverables>
    <deliverable type="document">Session log with /frontend-dev output and pass/fail.</deliverable>
  </deliverables>

  <do_not>
    <rule>Do NOT accept PARTIAL PASS. All surfaces must render.</rule>
  </do_not>
</task_order>
