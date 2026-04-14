<task_order>
  <metadata>
    <id>0.4.0_DS_ClientPlatform-2026-04-14-advi-fntend-b4-ds</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-04-14</date>
    <status>staged</status>
    <project_code>ADVI_FNTEND</project_code>
    <wave>A</wave>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADVI_FRONTEND_CORRECTNESS.md (Bundle 4: B6)</ref>
  </references>

  <objective>
    Populate `top_gain_positions` on advisor-summary (L2).
    Client-summary (L3) already has the type via `clientDetail.tax.top_gain_positions`.
  </objective>

  <acceptance_criteria>
    1. Advisor-summary artifacts have top_gain_positions populated (not [])
    2. Spot-check 3 advisors shows real data
    3. MCP COMPLETE to COO
  </acceptance_criteria>

  <compiler_tools_mandate>
    Phase 1: `comp-pipescript io` on advisor-summary writer to confirm top_gain_positions plumbed.
    Phase 2: `python -m py_compile`.
    Phase 3: `comp-validate` after rerun.
  </compiler_tools_mandate>

  <dependencies>
    <none/>
  </dependencies>
</task_order>
