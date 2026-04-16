<task_order>
  <metadata>
    <id>0.4.0_DS_ClientPlatform-2026-04-14-advi-fntend-b6-ds</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform~B</issued_to><!-- re-dialed 2026-04-15 PM by COO from base lane to ~B for post-rerun validator pass -->
    <date>2026-04-14</date>
    <status>complete</status><!-- ~B closed 2026-04-15 22:36Z after B6b fix shipped (see ADVI_FNTEND.B6b.ds-ofc-distribution-by-segment-histogram.md + same-commit D_01 change). All 3 acceptance criteria satisfied: (a) advisors[] populated on EVERY OFC segment (10/10 × 4 quarters) — PASS; (b) per-office per-period AUA via views.ofc_per_period — PASS; (c) NNA bins L0 PASS (office-grain histogram count=12) + L1 PASS post-B6b (per-advisor NNA histogram per office, count=N_advisors_in_office via groupby (_office, _det_advisor) OFC_ROLE_PRIORITY attribution). Original validation against post-19:35Z artifact 22:11Z surfaced the L1 gap; B6b fix landed within the hour. CTO Path C+ approval trail preserved in commit bodies. -->
    <project_code>ADVI_FNTEND</project_code>
    <wave>A</wave>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADVI_FRONTEND_CORRECTNESS.md (Bundle 6: D2+D3+D4)</ref>
  </references>

  <objective>
    OFC snapshot parity contract:
    (a) Populate `officeSegment.advisors[]` on EVERY OFC donut segment (fixes "No advisor data for Austin" at DistributionTab:3086)
    (b) Emit per-office per-period AUA for time-machine at L1 (OfcAdvisorListPanel)
    (c) Emit NNA distribution bins under `views.ofc` at L0 AND per-office at L1.
        **Clarification added 2026-04-14 per RD audit:** "bins" = per-advisor NNA values within the selected office, suitable for bell-curve histogram rendering (same shape as existing GEO/ADV L1 bins — NOT a single NNA value per office).
  </objective>

  <acceptance_criteria>
    1. Every OFC donut segment (all 10 offices) has non-empty advisors[]
    2. per-office per-period AUA present for time-machine
    3. NNA bins under views.ofc at L0 + per-office at L1
    4. MCP COMPLETE to COO
  </acceptance_criteria>

  <compiler_tools_mandate>
    Phase 1: `comp-pipescript io D_01` + `comp-pipescript io` on OFC segment writer; `comp-platinum reverse views.ofc` to enumerate consumers; `comp-blast DistributionTab` (confirm OFC changes don't blast outside this component).
    Phase 2: `python -m py_compile`; `comp-validate`.
    Phase 3: `comp-transform schema-check DistributionTab --feature ofcSnapshot`.
  </compiler_tools_mandate>

  <dependencies>
    <none/>
  </dependencies>
</task_order>
