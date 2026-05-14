<task_order>
  <metadata>
    <id>ADVI_SHARED.005</id>
    <slug>rd-component-extraction</slug>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.2_RD_AdvisorIntelligence</issued_to>
    <date>2026-05-14</date>
    <status>complete</status>
    <dispatch_held>false</dispatch_held>
    <project_code>ADVI_SHARED</project_code>
    <priority>P1 — Category B lint warnings (react-hooks/static-components — inner component declarations); parallel-OK</priority>
    <sla>~1d wall; standalone</sla>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADVI_SHARED.md §3.4 component extraction convention + §4.2 SHARED.005</ref>
    <ref type="audit">docs/briefs/ADVI_SHARED_AUDIT.md §F.1 per-file warning table (Cat B subcounts) + §3.4 audit list (~12 inner components)</ref>
    <ref type="project_json">org/projects/ADVI_SHARED.json</ref>
    <ref type="cross_link">Parallel-OK with .001 .002 .003 .004. Pure refactor.</ref>
  </references>

  <context>
    Apply PRD §3.4 component-extraction convention to the ~12 Category B lint warnings — `react-hooks/static-components` flagged where an inner functional component is declared inside a parent component's render body, defeating React reconciliation.

    **Convention:** Extract each inner component into either:
    - Same-file top-level declaration (preferred if not exported)
    - Sibling file at `{ParentDir}/_components/{InnerName}.tsx` (preferred if reused or shippable)

    Audit §F.1 actual Cat B targets (12 inner components total):
    - InflectionInsightsPanel.tsx (3 inner components)
    - AdvisorPublicProfile.tsx (1 inner component at L1672 per PRD §3.4)
    - AdvisorsTab.tsx (3 inner components — PRD said 4; lint shows 3, 1 may already be resolved)
    - Per audit §F.1 detail for remaining

    Pure refactor — zero semantic change.
  </context>

  <objective>
    Extract ~12 inner components per §3.4 convention. Lint warning count for `react-hooks/static-components` drops to zero (or audit-corrected baseline). Zero behavior change.
  </objective>

  <scope>
    <files>
      <file action="extract">Per audit §F.1 — 12 inner components to top-level or sibling-file extraction</file>
      <file action="readonly_reference">docs/architecture/ADVI_SHARED.md §3.4 + audit §F.1 verbatim</file>
    </files>
  </scope>

  <phase id="1" when="before write">
    <step>
      <run>cd portal && /c/Users/AndrewBerman/.bun/bin/bun run lint 2>&1 | grep "react-hooks/static-components" | wc -l</run>
      <expect>Baseline ~12 per audit; tolerate audit drift ±2.</expect>
      <if_mismatch>Surface drift to COO before scope-locking.</if_mismatch>
    </step>
  </phase>

  <phase id="2" when="before commit">
    <step>
      <run>cd portal && /c/Users/AndrewBerman/.bun/bin/bun run tsc --noEmit</run>
      <expect>0 errors.</expect>
    </step>
    <step>
      <run>cd portal && /c/Users/AndrewBerman/.bun/bin/bun run lint 2>&1 | grep "react-hooks/static-components" | wc -l</run>
      <expect>0 — Cat B eliminated.</expect>
    </step>
    <step>
      <run>bun run dev + visual smoke at extraction sites</run>
      <expect>Zero regression — extractions are render-transparent.</expect>
    </step>
  </phase>

  <phase id="3" when="after commit">
    <step>
      <run>comp-blast on each parent component whose inner was extracted</run>
      <expect>No new downstream nodes; extraction is internal to parent.</expect>
    </step>
  </phase>

  <acceptance_criteria>
    AC1: All 12 inner components extracted per §3.4 convention.
    AC2: Lint `react-hooks/static-components` count drops to 0 (or audit-corrected baseline).
    AC3: tsc 0 errors.
    AC4: bun run dev smoke clean.
    AC5: Zero semantic change verified at extraction sites.
    AC6: Session log + RAVC2 MCP.
  </acceptance_criteria>

  <compiler_tools_mandate>Phases above.</compiler_tools_mandate>

  <cross_domain_coordination>
    HARD DEPENDENCIES: none.
    PARALLEL-OK: .001 .002 .003 .004.
    POTENTIAL OVERLAP: ADVI_INFFIN.011 RD lane — coord internally.
    PORTAL SUBMODULE: DT 0.4 push.
  </cross_domain_coordination>

  <data_reprocess_scope>
    <no_reprocess_needed>Pure refactor.</no_reprocess_needed>
  </data_reprocess_scope>

  <deliverables>
    1. 12 inner components extracted
    2. Commits per RD discipline
    3. Session log + RAVC2
  </deliverables>

  <ravc>RD 0.4.2 RAVC2 to COO on AC1-6 PASS.</ravc>

  <notes>
    **Author identity:** `--author="0.4.2_RD_AdvisorIntelligence <0.4.2_RD_AdvisorIntelligence@opal.agent>"`.
  </notes>
</task_order>
