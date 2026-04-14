<task_order>
  <metadata>
    <id>0.4.0_DE_ClientPlatform-2026-04-14-advi-fntend-b3-fe</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DE_ClientPlatform</issued_to>
    <date>2026-04-14</date>
    <status>staged</status>
    <project_code>ADVI_FNTEND</project_code>
    <wave>C</wave>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADVI_FRONTEND_CORRECTNESS.md (Bundle 3)</ref>
  </references>

  <objective>
    Redesign `FeeSummaryPanel` — "Client Fee" headline, per-advisor rows with fee shares,
    rename or remove misleading "Wtd Avg Fee" card.

    **Client rollup (updated 2026-04-14 per CTO ratification):** FE computes client-level `total_fee_usd` + any aggregated `pct_of_client_fee` from DS's per-account `fee_share_usd` / `fee_share_bps`. DS owns the advisor_id → display_name + raw per-account shares; FE owns aggregation. Do not request DS to emit rollups.
  </objective>

  <acceptance_criteria>
    1. Fee Summary panel shows per-advisor rows with fee shares
    2. Profile advisor pinned first
    3. "Wtd Avg Fee" label gone or replaced
    4. `/frontend-dev` closed-loop pass
    5. MCP COMPLETE to COO
  </acceptance_criteria>

  <compiler_tools_mandate>
    Phase 1: `comp-transform schema-check FeeSummaryPanel` + `--feature teamAttribution`.
    Phase 3: `/frontend-dev`.
  </compiler_tools_mandate>

  <dependencies>
    <dependency agent="0.4.0_DS_ClientPlatform" task="ADVI_FNTEND.B3 DS" status="staged"/>
    <dependency agent="0.4.0_DE_ClientPlatform" task="ADVI_FNTEND.B2 FE" status="staged" description="window vocabulary must land first"/>
  </dependencies>

  <cross_domain_coordination>types.ts sequencing with B1/B2/B4/B5.</cross_domain_coordination>
</task_order>
