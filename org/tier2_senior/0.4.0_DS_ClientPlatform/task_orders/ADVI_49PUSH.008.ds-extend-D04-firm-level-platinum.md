<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-04-08-49push-008-ds</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform~A</issued_to>
    <date>2026-04-08</date>
    <status>pending</status>
    <project_code>ADVI_49PUSH</project_code>
    <wave>2b</wave>
    <phase>P3</phase>
    <mcp_identity>Register with MCP as "0.4.0_DS_ClientPlatform~A" (not the base serial). This is your instance ID for this session. Use it for register_agent, heartbeat, and inbox-watch.</mcp_identity>
  </metadata>

  <objective>
    Extend D_04.client_portal_summary.py with the remaining firm-level platinum publishers
    designed in the Phase 2 audits. The catalog (docs/briefs/ADVI_49PUSH_P2_platinum_file_catalog.md)
    recommends expanding D_04 (Option A). This adds ~200 lines and 6 new firm-level files
    so AE can deploy the COMPLETE script in a single deploy cycle.
  </objective>

  <context>
    D_04 currently produces Phase 1 files only (Books tab: dashboard.json, mix_summary.json,
    advisors/*/summary.json, clients/*/summary.json + timeseries, accounts/*/summary.json).

    Phase 2 audits designed 6 additional firm-level platinum files for the remaining ADVI surfaces.
    The master catalog recommends adding them to D_04 rather than creating D_05+.

    READ THESE BEFORE WRITING:
    - docs/briefs/ADVI_49PUSH_P2_platinum_file_catalog.md (master spec -- the blueprint)
    - docs/briefs/ADVI_49PUSH_P2_2.1_partner_analytics.md (platinum specs for partner analytics)
    - docs/briefs/ADVI_49PUSH_P2_2.2_distribution.md (platinum specs for distribution)
    - docs/briefs/ADVI_49PUSH_P2_2.3_advisors_tab.md (platinum specs for advisors tab)
    - docs/briefs/ADVI_49PUSH_P2_cross_surface_matrix.md (divergence resolutions)
    - data/black_diamond/scripts/gold/D_04.client_portal_summary.py (your own P1 code)
  </context>

  <compiler_tools_mandate>
    1. comp-pipescript io D_01
       -- D_01 I/O: source of partner analytics header_metrics data

    2. comp-pipescript io D_00
       -- D_00 I/O: source of timeseries_chart, leaderboard

    3. comp-trace D_01 --all
       -- all D_01 function nodes + outputs

    4. comp-pipescript overlap D_00 D_01
       -- shared artifacts between D_00 and D_01
  </compiler_tools_mandate>

  <requirements>
    <requirement id="1">
      Add these builder functions to D_04 (per catalog specs):

      a) build_partner_analytics_quarterly() -> platinum/firm/partner_analytics_quarterly.json
      b) build_partner_analytics_monthly() -> platinum/firm/partner_analytics_monthly.json
      c) build_partner_analytics_annual() -> platinum/firm/partner_analytics_annual.json
         -- Or merged into one file per catalog recommendation. Follow the catalog decision.
      d) build_cumulative_chart() -> platinum/firm/cumulative_chart.json
         -- Timeseries overview for PartnerAnalytics + Distribution continuous mode
      e) build_leaderboard() -> platinum/firm/leaderboard.json
         -- Employee leaderboard trimmed to QTD+YTD (~15KB per catalog)
      f) build_rolling_flows() -> SKIP. Catalog confirms this is dead code. Do NOT build.
    </requirement>

    <requirement id="2">
      DIVERGENCE RESOLUTIONS (from cross-surface matrix):
      - NNA by GEO/ADV: compute canonical_nna ONCE, use for both snapshot donut and continuous bar
      - Advisor AUA: use advisor_fee_detail (C_08) as single source
      - Firm client count: deduplicate across advisors (shared relationships)
      Follow the canonical platinum source assignments in the cross-surface matrix.
    </requirement>

    <requirement id="3">
      Number consistency: firm-level platinum totals MUST match the entity-level totals
      already produced by D_04 P1 code. Do NOT recompute firm totals independently --
      derive from the same data paths used in the P1 builders.
    </requirement>

    <requirement id="4">
      py_compile clean, all ASCII, no emojis. Follow the existing D_04 code patterns
      (same imports, same S3 upload helpers, same ThreadPoolExecutor usage).
    </requirement>
  </requirements>

  <deliverables>
    <deliverable>D_04.client_portal_summary.py extended with firm-level builders (~1,080 lines total)</deliverable>
    <deliverable>Message to COO (2.0.0_SA_COO) confirming complete, listing new functions added</deliverable>
  </deliverables>

  <do_not>
    <rule>Do NOT create D_05 or any new script file -- expand D_04</rule>
    <rule>Do NOT build rolling_flows -- it is dead code</rule>
    <rule>Do NOT break existing P1 builder functions -- only add new ones</rule>
    <rule>Do NOT deploy -- AE handles that</rule>
  </do_not>
</task_order>
