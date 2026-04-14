<task_order>
  <metadata>
    <id>0.4.0_DE_ClientPlatform-2026-04-14-advi-fntend-b1-fe</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DE_ClientPlatform</issued_to>
    <date>2026-04-14</date>
    <status>staged</status>
    <project_code>ADVI_FNTEND</project_code>
    <wave>C</wave>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADVI_FRONTEND_CORRECTNESS.md (Bundle 1)</ref>
  </references>

  <objective>
    Wire `feeView` through Summary counts + RoleDonut + Lifetime Activity on AdvisorPublicProfile.
    Remove "fee filter not applied" footnote at `AdvisorBookView:1105`.
  </objective>

  <acceptance_criteria>
    1. Toggling Fees updates Summary counts, RoleDonut segments, and Lifetime Activity chart
    2. No static values when toggling
    3. Footnote removed
    4. `/frontend-dev` closed-loop pass
    5. MCP COMPLETE to COO
  </acceptance_criteria>

  <compiler_tools_mandate>
    Phase 1: `comp-transform schema-check --feature feeView` on AdvisorPublicProfile + RoleDonut + LifetimeActivity.
    Phase 2: `comp-transform ternary-audit` on affected components.
    Phase 3: `/frontend-dev`.
  </compiler_tools_mandate>

  <dependencies>
    <dependency agent="0.4.0_DS_ClientPlatform" task="ADVI_FNTEND.B1 DS" status="staged"/>
  </dependencies>

  <cross_domain_coordination>
    AdvisorBookView.tsx + types.ts touched by B1, B4, B5. Sequential commits; no parallel FE commits to these files.
  </cross_domain_coordination>
</task_order>
