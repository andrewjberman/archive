<task_order>
  <metadata>
    <id>ADVI_SHARED.004</id>
    <slug>rd-colocation-refactor</slug>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.2_RD_AdvisorIntelligence</issued_to>
    <date>2026-05-14</date>
    <status>staged</status>
    <dispatch_held>false</dispatch_held>
    <project_code>ADVI_SHARED</project_code>
    <priority>P1 — Category A lint warnings (file-organization react-refresh/only-export-components); parallel-OK with .001/.002/.003 (no type-shape dep)</priority>
    <sla>~2d wall; standalone (no upstream gates)</sla>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADVI_SHARED.md §3.3 file organization convention + §4.2 SHARED.004 + §3.3 top-5 worst-offender list</ref>
    <ref type="audit">docs/briefs/ADVI_SHARED_AUDIT.md §F.1 per-file warning table + §F.3 SHARED.004/005 sizing implications</ref>
    <ref type="project_json">org/projects/ADVI_SHARED.json</ref>
    <ref type="audit_correction">Audit §F.0 — PRD §2.4 framing was 5x off; Cat A actual count = 16 (not ~75). SHARED.004 scope SHRUNK accordingly.</ref>
    <ref type="cross_link">Parallel-OK with .001 .002 .003 .005. No type-shape dep. Pure refactor (no semantic change).</ref>
  </references>

  <context>
    Apply PRD §3.3 file-organization convention (co-location refactor) to the 16 Category A lint warnings — `react-refresh/only-export-components` flagged by ESLint where a single file exports both components AND non-component values (constants, helpers, types).

    **Convention:** Split files so each module exports either ONLY components OR ONLY non-component values. Co-locate the non-component exports into a sibling file (`{Component}/constants.ts` / `{Component}/types.ts` / `{Component}/helpers.ts`) following the existing partner-internal pattern.

    Audit §F.1 actual Cat A files (16 warnings total across these targets — not ~75 as PRD §2.4 predicted):
    - InflectionInsightsPanel.tsx (1 Cat A)
    - DistributionTab.tsx (1 Cat A)
    - FeeEfficiencyPanel.tsx (1 Cat A)
    - PartnerAnalytics.tsx (per top-5 list in PRD §3.3)
    - AdvisorBookView.tsx (per top-5 list)
    - 2 contexts files (per PRD §3.3)
    - Additional files per audit §F.1 detail

    Pure refactor — zero semantic change; file moves only.
  </context>

  <objective>
    Refactor 16 Category A files per §3.3 convention. Each refactored file exports ONLY components OR ONLY non-component values. Lint warning count for `react-refresh/only-export-components` drops to zero.
  </objective>

  <scope>
    <files>
      <file action="split">Per audit §F.1 — 16 Cat A files; refactor each into component-file + co-located non-component-file</file>
      <file action="readonly_reference">docs/architecture/ADVI_SHARED.md §3.3 + audit §F.1 verbatim</file>
    </files>
  </scope>

  <phase id="1" when="before write">
    <step>
      <run>cd portal && /c/Users/AndrewBerman/.bun/bin/bun run lint 2>&1 | grep "react-refresh/only-export-components" | wc -l</run>
      <expect>Baseline warning count (expect 16 per audit §F.0; tolerate ±2 from audit drift since 2026-05-12).</expect>
      <if_mismatch>If count diverged significantly, surface to COO — likely concurrent commits touched scope files.</if_mismatch>
    </step>
    <step>
      <run>comp-blast {Component} for each top-5 file in scope</run>
      <expect>Downstream consumer chain enumerated for each refactor candidate — confirms blast radius bounded before split.</expect>
      <if_mismatch>If a file has unexpectedly large consumer set, split conservatively (preserve re-export from original file with deprecation comment) and surface to COO.</if_mismatch>
    </step>
  </phase>

  <phase id="2" when="before commit">
    <step>
      <run>cd portal && /c/Users/AndrewBerman/.bun/bin/bun run tsc --noEmit</run>
      <expect>0 errors.</expect>
    </step>
    <step>
      <run>cd portal && /c/Users/AndrewBerman/.bun/bin/bun run lint 2>&1 | grep "react-refresh/only-export-components" | wc -l</run>
      <expect>0 — Cat A warnings eliminated.</expect>
      <if_mismatch>Residual warnings; finish the split before commit.</if_mismatch>
    </step>
    <step>
      <run>bun run dev + visual smoke 49F + Inflection critical pages</run>
      <expect>Zero regression — file moves are import-path-transparent.</expect>
    </step>
  </phase>

  <phase id="3" when="after commit">
    <step>
      <run>comp-blast {Component} for each refactored file</run>
      <expect>Same consumer set as Phase 1 (re-exports may be transitively preserved).</expect>
    </step>
  </phase>

  <acceptance_criteria>
    AC1: All 16 Cat A files refactored per §3.3 convention.
    AC2: Lint `react-refresh/only-export-components` count drops to 0 (or audit-drift-corrected baseline).
    AC3: tsc 0 errors.
    AC4: bun run dev smoke clean per partner.
    AC5: Zero semantic change verified (visual diff per scope file).
    AC6: Session log Compiler Tools section + per-file split summary.
    AC7: MCP RAVC2 to COO.
  </acceptance_criteria>

  <compiler_tools_mandate>Phases above; inherits PRD §6.1 template.</compiler_tools_mandate>

  <cross_domain_coordination>
    HARD DEPENDENCIES: none.

    PARALLEL-OK with: .001 .002 .003 .005. Pure refactor; no merge conflict risk if files don't overlap with feature TOs.

    POTENTIAL OVERLAP: ADVI_INFFIN.011 cross-firm consolidation (RD 0.4.2 lane) — RD coordinates internally to avoid touching same files in two TOs same session.

    PORTAL SUBMODULE: DT 0.4 push.
  </cross_domain_coordination>

  <data_reprocess_scope>
    <no_reprocess_needed>Pure refactor.</no_reprocess_needed>
  </data_reprocess_scope>

  <deliverables>
    1. 16 Cat A files refactored
    2. Commits per RD discipline (multiple OK; one per file or per logical group)
    3. Session log with split summary
    4. MCP RAVC2 to COO
  </deliverables>

  <ravc>RD 0.4.2 RAVC2 to COO on AC1-7 PASS.</ravc>

  <notes>
    **PRD framing correction:** Audit §F.0 caught PRD §2.4 5x overcount on Cat A. Scope is 16 files, not 75. Effort drops from 2d to ~1d if scope holds — RD discretion to compress SLA.

    **Author identity:** `--author="0.4.2_RD_AdvisorIntelligence <0.4.2_RD_AdvisorIntelligence@opal.agent>"`.
  </notes>
</task_order>
