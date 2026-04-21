<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-04-21-inflec-w5.0.2-folder-proposal</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DE_ClientPlatform</issued_to>
    <date>2026-04-21</date>
    <status>staged</status>
    <project_code>ADVI_INFLEC</project_code>
  </metadata>

  <objective>
    Using the W5.0.1 component inventory, propose the refactored `portal/src/pages/AdvisorIntelligence/` folder structure: `_shared/` primitives + `_partners/49financial/` overrides + `_partners/inflection/` stubs. Write a concrete file-move plan (old path → new path for every component) and the composition pattern for the top-level `index.tsx` firmId-router. CTO reviews in W5.0.3.
  </objective>

  <context>
    PRD §7.3 target structure (illustrative, DE owns the actual design):
    ```
    AdvisorIntelligence/
      _shared/components/    # shared primitives
      _shared/hooks/
      _shared/types/
      _partners/49financial/overrides/
      _partners/49financial/constants.ts
      _partners/inflection/overrides/  (stubs only at this point)
      _partners/inflection/constants.ts
      index.tsx              # reads firmId from JWT, renders partner view + shared shell
    ```
    Blocked on W5.0.1 (inventory must be complete). No code changes yet — file-move plan only.
  </context>

  <compiler_tools_mandate>
    Phase 1:
    <run>comp-transform schema-check AdvisorIntelligence</run>
    <expect>Baseline schema (same as W5.0.1 output). Verify unchanged since audit.</expect>

    Phase 3:
    <run>(None — document-only TO. No portal code changed.)</run>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    <none/>
  </cross_domain_coordination>

  <acceptance_criteria>
    1. Proposal document at `org/tier2_senior/0.4.0_DE_ClientPlatform/deliverables/advi_inflec_folder_structure_proposal.md`.
    2. Every component from W5.0.1 inventory has a `src path → proposed target path` row.
    3. `index.tsx` composition pattern specified (firmId extraction from AuthContext, partner-router approach).
    4. At least one AMBIGUOUS component from W5.0.1 has a concrete resolution recommendation.
    5. Session log with reasoning summary.
  </acceptance_criteria>

  <scope>
    <files>
      <file action="create">org/tier2_senior/0.4.0_DE_ClientPlatform/deliverables/advi_inflec_folder_structure_proposal.md</file>
      <file action="reference">org/tier2_senior/0.4.0_DE_ClientPlatform/deliverables/advi_inflec_component_inventory.md</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">Blocked on W5.0.1 completion.</requirement>
    <requirement id="2">No code changes. Proposal doc only.</requirement>
    <requirement id="3">CTO reviews before execution (W5.0.3). Do NOT start W5.0.4 without CTO sign-off.</requirement>
  </requirements>

  <deliverables>
    <deliverable type="document">Folder structure proposal + file-move plan.</deliverable>
    <deliverable type="document">Session log.</deliverable>
  </deliverables>

  <do_not>
    <rule>Do NOT move any files yet — plan only.</rule>
    <rule>Do NOT start before W5.0.1 deliverable is committed.</rule>
  </do_not>
</task_order>
