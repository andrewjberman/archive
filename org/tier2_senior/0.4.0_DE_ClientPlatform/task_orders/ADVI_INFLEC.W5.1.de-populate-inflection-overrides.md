<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-04-21-inflec-w5.1-populate-overrides</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DE_ClientPlatform</issued_to>
    <date>2026-04-21</date>
    <status>staged</status>
    <project_code>ADVI_INFLEC</project_code>
  </metadata>

  <objective>
    Populate `_partners/inflection/overrides/` with real Inflection-specific components: `FidelityCustodianBar.tsx` (Fidelity 99.4% custodian concentration viz), and any Lighthouse/IWM/Core model dimension panel if PRD §10 Q10 resolves to "TRN-only sufficient" (deferred panel if not). Wire the partner-router in `index.tsx` to render Inflection overrides when `firmId === 'inflection'`.
  </objective>

  <context>PRD §9 W5.1. Blocked on W4.6 (platinum artifacts in S3) + W5.0.6 (stubs exist). Inflection custodian concentration is 99.4% Fidelity — the custodian bar component should reflect this clearly. The 49F custodian bar shows Fidelity + Schwab split; Inflection's version shows Fidelity-dominant. DE implements the Inflection-specific version in `_partners/inflection/overrides/` — `_shared/` primitive unchanged.</context>

  <compiler_tools_mandate>
    Phase 1:
    <run>comp-transform schema-check AdvisorIntelligence</run>
    <expect>0 MISSING post W5.0.4 refactor. Baseline before override addition.</expect>
    <run>comp-transform ternary-audit AdvisorIntelligence</run>
    <expect>0 gaps where inflection branch is missing in existing ternaries. If gaps found, fix before wiring overrides.</expect>

    Phase 2:
    <run>bunx tsc -b portal/</run>
    <expect>Zero TS errors after each component addition.</expect>

    Phase 3:
    <run>comp-transform schema-check AdvisorIntelligence</run>
    <expect>0 MISSING. New Inflection override components rendered correctly.</expect>
    <run>/frontend-dev (AdvisorIntelligence constitution, Inflection test user if available)</run>
    <expect>PASS. FidelityCustodianBar renders with non-null custodian data.</expect>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    required_action: "Blocked on W4.6 (platinum JSON in S3) + W5.0.6 (stubs). Coordinate with DT on W5.6 auth flow validation timing."
  </cross_domain_coordination>

  <acceptance_criteria>
    1. `FidelityCustodianBar.tsx` renders Fidelity-dominant (99.4%) custodian concentration from platinum data.
    2. `index.tsx` partner-router routes `firmId === 'inflection'` to Inflection overrides.
    3. comp-transform ternary-audit: 0 gaps for inflection branch.
    4. comp-transform schema-check: 0 MISSING.
    5. TypeScript clean.
    6. 49F portal unaffected (regression guard).
    7. Session log.
  </acceptance_criteria>

  <scope>
    <files>
      <file action="modify">portal/src/pages/AdvisorIntelligence/_partners/inflection/overrides/FidelityCustodianBar.tsx</file>
      <file action="modify">portal/src/pages/AdvisorIntelligence/index.tsx</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">Blocked on W4.6 + W5.0.6.</requirement>
    <requirement id="2">comp-transform ternary-audit: 0 gaps before shipping.</requirement>
    <requirement id="3">Composition pattern: shared primitive + inflection prop, not conditional in shared code.</requirement>
  </requirements>

  <deliverables>
    <deliverable type="commit">Override components + index.tsx wiring.</deliverable>
    <deliverable type="document">Session log.</deliverable>
  </deliverables>

  <do_not>
    <rule>Do NOT add Inflection-specific conditionals in _shared/ components.</rule>
    <rule>Do NOT skip ternary-audit.</rule>
  </do_not>
</task_order>
