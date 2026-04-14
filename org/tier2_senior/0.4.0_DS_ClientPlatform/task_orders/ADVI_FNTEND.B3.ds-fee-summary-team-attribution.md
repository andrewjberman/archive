<task_order>
  <metadata>
    <id>0.4.0_DS_ClientPlatform-2026-04-14-advi-fntend-b3-ds</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-04-14</date>
    <status>staged</status>
    <project_code>ADVI_FNTEND</project_code>
    <wave>B</wave>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADVI_FRONTEND_CORRECTNESS.md (Bundle 3: B5)</ref>
  </references>

  <objective>
    Per-account fee attribution fields:
    - `client_total_fee_bps`, `client_total_fee_usd`
    - `team_attribution[] = {advisor_id, display_name, fee_share_bps, fee_share_usd, pct_of_client_fee}`
      with profile advisor pinned first.

    **Client-level rollup (added 2026-04-14 per RD audit):** B3 FE confirms during Phase 1 whether Fee Summary panel needs a client-rollup header. If yes, this TO adds client-level `total_fee_usd` + aggregated `team_attribution[]` across all accounts for the client. Default: FE-only rollup from per-account; only fold into DS if Phase 1 surfaces FE infeasibility.
  </objective>

  <acceptance_criteria>
    1. Per-account artifact has all listed fields
    2. team_attribution fee_share_usd sums ≈ client_total_fee_usd
    3. Profile advisor always index 0 in team_attribution
    4. MCP COMPLETE to COO
  </acceptance_criteria>

  <compiler_tools_mandate>
    Phase 1: `comp-pipescript io D_02` for team_attribution emission path.
    Phase 2: `python -m py_compile`.
    Phase 3: `comp-transform schema-check FeeSummaryPanel --feature teamAttribution`.
  </compiler_tools_mandate>

  <dependencies>
    <dependency agent="0.4.0_DS_ClientPlatform" task="ADVI_FNTEND.B2 DS" status="staged" description="window vocabulary"/>
  </dependencies>
</task_order>
