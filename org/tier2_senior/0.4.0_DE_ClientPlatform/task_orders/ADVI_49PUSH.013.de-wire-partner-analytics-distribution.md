<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-04-08-49push-013-de</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DE_ClientPlatform~B</issued_to>
    <date>2026-04-08</date>
    <status>pending</status>
    <project_code>ADVI_49PUSH</project_code>
    <wave>3</wave>
    <phase>P3</phase>
    <mcp_identity>Register with MCP as "0.4.0_DE_ClientPlatform~B" (not the base serial). This is your instance ID for this session. Use it for register_agent, heartbeat, and inbox-watch.</mcp_identity>
  </metadata>

  <objective>
    Rewire PartnerAnalytics header + Distribution tab fetches to platinum/ paths.
    These share data sources so one agent handles both to keep URLs consistent.
  </objective>

  <context>
    Audit briefs:
    - docs/briefs/ADVI_49PUSH_P2_2.1_partner_analytics.md
    - docs/briefs/ADVI_49PUSH_P2_2.2_distribution.md
    Master catalog: docs/briefs/ADVI_49PUSH_P2_platinum_file_catalog.md

    DT (0.4.0_DT_ClientPlatform) is updating the serving layer in parallel (.011).
    Message them via MCP to agree on URL patterns before finalizing fetches.
  </context>

  <compiler_tools_mandate>
    1. comp-routes trace PartnerAnalytics
    2. comp-routes trace DistributionTab
    3. comp-routes trace getPartnerAnalytics
    4. comp-routes trace getCumulativeChart
    5. comp-trace PartnerAnalytics --direction both
    6. comp-trace DistributionTab --direction both
  </compiler_tools_mandate>

  <requirements>
    <requirement id="1">
      PartnerAnalytics header:
      OLD: getCumulativeChart -> gold/artifacts/timeseries_chart.json
           getFirmMixViews -> gold/artifacts/firm_mix_views.json
      NEW: platinum/firm/timeseries_overview.json (pre-aggregated timeseries + mix)
    </requirement>

    <requirement id="2">
      Distribution tab:
      OLD: getPartnerAnalytics(gran) -> gold/artifacts/partner_analytics/header_metrics_{gran}.json
           getCumulativeChart -> gold/artifacts/timeseries_chart.json
      NEW: platinum/firm/partner_analytics_{gran}.json
           platinum/firm/cumulative_chart.json (weekly-downsampled)
    </requirement>

    <requirement id="3">
      Update TypeScript types for platinum response shapes.
      grep verify: zero gold/ references in PartnerAnalytics.tsx and DistributionTab.tsx.
    </requirement>
  </requirements>

  <deliverables>
    <deliverable>PartnerAnalytics + DistributionTab wired to platinum/</deliverable>
    <deliverable>Message to COO with fetch reduction counts</deliverable>
  </deliverables>
</task_order>
