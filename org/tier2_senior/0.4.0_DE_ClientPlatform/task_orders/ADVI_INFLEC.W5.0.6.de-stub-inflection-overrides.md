<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-04-21-inflec-w5.0.6-inflection-stubs</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DE_ClientPlatform</issued_to>
    <date>2026-04-21</date>
    <status>complete</status>
    <project_code>ADVI_INFLEC</project_code>
  </metadata>

  <objective>
    Create stub components in `portal/src/pages/AdvisorIntelligence/_partners/inflection/overrides/` and `constants.ts` ready to populate when Inflection gold data lands (W4). Stubs render a placeholder ("Inflection data pending") — they are not empty files. Also create `constants.ts` with Inflection-specific constants: firmId slug, display name, custodian label.
  </objective>

  <context>
    PRD §7.3. After W5.0.5 confirms 49F regression is clean, this TO cements the Inflection partner folder so W5.1 (populate overrides) has a clear landing zone. Key Inflection-specific overrides to stub: FidelityCustodianBar (Inflection is 99.4% Fidelity — distinct from 49F's mixed custodian view), and any Lighthouse/IWM/Core model dimension panel (per PRD §10 Q10 — deferred but stub the hook). All stubs may be concurrent with W5.0.4 if DE prefers.
  </context>

  <compiler_tools_mandate>
    Phase 1:
    <run>comp-transform schema-check AdvisorIntelligence</run>
    <expect>0 MISSING — stubs don't regress the schema.</expect>

    Phase 3:
    <run>bunx tsc -b portal/</run>
    <expect>Zero TypeScript errors — stubs must be properly typed even if they render placeholder text.</expect>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    <none/>
  </cross_domain_coordination>

  <acceptance_criteria>
    1. `_partners/inflection/overrides/` contains at minimum: `FidelityCustodianBar.tsx` (stub), `index.ts` (re-exports).
    2. `_partners/inflection/constants.ts` contains: `FIRM_ID = 'inflection'`, `FIRM_DISPLAY_NAME = 'Inflection Wealth Management'`, `PRIMARY_CUSTODIAN = 'Fidelity'`.
    3. TypeScript clean.
    4. Stubs render a placeholder (not blank — helps QA distinguish "data not yet populated" from "rendering error").
    5. Session log.
  </acceptance_criteria>

  <scope>
    <files>
      <file action="create">portal/src/pages/AdvisorIntelligence/_partners/inflection/overrides/FidelityCustodianBar.tsx</file>
      <file action="create">portal/src/pages/AdvisorIntelligence/_partners/inflection/overrides/index.ts</file>
      <file action="create">portal/src/pages/AdvisorIntelligence/_partners/inflection/constants.ts</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">Stubs must compile. Placeholder render string acceptable.</requirement>
    <requirement id="2">No 49F constants in inflection/ folder.</requirement>
    <requirement id="3">Blocked on W5.0.5 regression passing.</requirement>
  </requirements>

  <deliverables>
    <deliverable type="commit">Inflection stub files + session log.</deliverable>
  </deliverables>

  <do_not>
    <rule>Do NOT put real data logic in stubs — placeholder only.</rule>
  </do_not>
</task_order>
