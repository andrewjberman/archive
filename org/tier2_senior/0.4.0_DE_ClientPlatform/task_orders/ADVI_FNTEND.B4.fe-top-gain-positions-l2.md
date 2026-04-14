<task_order>
  <metadata>
    <id>0.4.0_DE_ClientPlatform-2026-04-14-advi-fntend-b4-fe</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DE_ClientPlatform</issued_to>
    <date>2026-04-14</date>
    <status>staged</status>
    <project_code>ADVI_FNTEND</project_code>
    <wave>C</wave>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADVI_FRONTEND_CORRECTNESS.md (Bundle 4)</ref>
  </references>

  <objective>
    Stop passing `[]` at `AdvisorBookView.tsx:282` — wire advisor-summary top_gain_positions.
  </objective>

  <acceptance_criteria>
    1. Top Gain Positions renders on advisor L2 with real data (not [])
    2. L3 (client) unchanged — already works
    3. `/frontend-dev` closed-loop pass
    4. MCP COMPLETE to COO
  </acceptance_criteria>

  <compiler_tools_mandate>
    Phase 3: `/frontend-dev` on AdvisorBookView.
  </compiler_tools_mandate>

  <dependencies>
    <dependency agent="0.4.0_DS_ClientPlatform" task="ADVI_FNTEND.B4 DS" status="staged"/>
  </dependencies>

  <cross_domain_coordination>AdvisorBookView.tsx shared with B1/B5 — sequence commits.</cross_domain_coordination>
</task_order>
