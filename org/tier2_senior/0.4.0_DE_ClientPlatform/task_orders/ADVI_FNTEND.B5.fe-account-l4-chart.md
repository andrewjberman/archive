<task_order>
  <metadata>
    <id>0.4.0_DE_ClientPlatform-2026-04-14-advi-fntend-b5-fe</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DE_ClientPlatform</issued_to>
    <date>2026-04-14</date>
    <status>staged</status>
    <project_code>ADVI_FNTEND</project_code>
    <wave>C</wave>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADVI_FRONTEND_CORRECTNESS.md (Bundle 5)</ref>
  </references>

  <objective>
    Render Month/Quarter/Year interval chart on Account L1 drill, mirroring Lifetime Activity.
  </objective>

  <acceptance_criteria>
    1. Account L1 drill renders timeseries chart with M/Q/Y toggle
    2. Pattern matches Lifetime Activity (same interval selector, same series)
    3. `/frontend-dev` closed-loop pass
    4. MCP COMPLETE to COO
  </acceptance_criteria>

  <compiler_tools_mandate>
    Phase 1: `comp-transform schema-check AdvisorBookAccountDetail`; `comp-cache collisions` (new account timeseries likely introduces new React Query key).
    Phase 3: `/frontend-dev` on Account L1 drill.
  </compiler_tools_mandate>

  <dependencies>
    <dependency agent="0.4.0_DS_ClientPlatform" task="ADVI_FNTEND.B5 DS" status="staged"/>
    <dependency agent="0.4.0_DE_ClientPlatform" task="ADVI_FNTEND.B2 FE" status="staged" description="window vocabulary"/>
  </dependencies>

  <cross_domain_coordination>AdvisorBookView.tsx + types.ts sequencing with B1/B3/B4.</cross_domain_coordination>
</task_order>
