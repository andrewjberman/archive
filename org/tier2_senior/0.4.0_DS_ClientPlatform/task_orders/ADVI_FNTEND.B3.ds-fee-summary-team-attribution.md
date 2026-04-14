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

    **DS contract is primary (updated 2026-04-14 per CTO ratification of RD audit):** advisor_id → display_name mapping is DS territory; FE cannot invent. DS emits raw per-account shares per the spec above. FE may compute aggregated rollups (e.g. client-level `total_fee_usd`, `pct_of_client_fee`) from the per-account shares — that's an FE optimization, not a DS scope change. Do NOT narrow DS scope based on FE capability.
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
