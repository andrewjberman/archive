<task_order>
  <metadata>
    <id>0.4.0_DS_ClientPlatform-2026-04-14-advi-fntend-b6-ds</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-04-14</date>
    <status>staged</status>
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
    (c) Emit NNA distribution bins under `views.ofc` at L0 AND per-office at L1
  </objective>

  <acceptance_criteria>
    1. Every OFC donut segment (all 10 offices) has non-empty advisors[]
    2. per-office per-period AUA present for time-machine
    3. NNA bins under views.ofc at L0 + per-office at L1
    4. MCP COMPLETE to COO
  </acceptance_criteria>

  <compiler_tools_mandate>
    Phase 1: `comp-pipescript io D_01` + `comp-pipescript io` on OFC segment writer; `comp-platinum reverse views.ofc` to enumerate consumers.
    Phase 2: `python -m py_compile`; `comp-validate`.
    Phase 3: `comp-transform schema-check DistributionTab --feature ofcSnapshot`.
  </compiler_tools_mandate>

  <dependencies>
    <none/>
  </dependencies>
</task_order>
