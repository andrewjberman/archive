<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-04-08-49push-012-de</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DE_ClientPlatform~A</issued_to>
    <date>2026-04-08</date>
    <status>pending</status>
    <project_code>ADVI_49PUSH</project_code>
    <wave>3</wave>
    <phase>P1+P3</phase>
    <mcp_identity>Register with MCP as "0.4.0_DE_ClientPlatform~A" (not the base serial). This is your instance ID for this session. Use it for register_agent, heartbeat, and inbox-watch.</mcp_identity>
  </metadata>

  <objective>
    Rewire Books tab (ClientsTab.tsx) frontend fetches to platinum/ paths. All 4 drill
    levels: N1 firm, L2 advisor, L3 client, L4 account. Plus ClientDetail panels.
  </objective>

  <context>
    Audit brief: docs/briefs/ADVI_49PUSH_P2_2.4_books_remaining.md
    Master catalog: docs/briefs/ADVI_49PUSH_P2_platinum_file_catalog.md
    PRD: docs/architecture/ADVI_49PUSH_P1_PRD.md (section: Frontend API update)

    DT (0.4.0_DT_ClientPlatform) is updating the serving layer in parallel (.011).
    Message them via MCP to agree on URL patterns before finalizing fetches.
  </context>

  <compiler_tools_mandate>
    1. comp-routes trace getEmployeeLeaderboard
    2. comp-routes trace getBooksClientDetail
    3. comp-routes trace getMixTimeseries
    4. comp-routes trace getBooksAccountComposition
    5. comp-trace ClientsTab --direction both
  </compiler_tools_mandate>

  <requirements>
    <requirement id="1">
      N1 Firm: Replace 4-5 fetches with 1-2:
      OLD: getEmployeeLeaderboard + getClientsTab + getFirmMixViews + getAdvisorFeeEfficiency + getBooksFirmComposition
      NEW: platinum/firm/dashboard.json + platinum/firm/mix_summary.json
    </requirement>

    <requirement id="2">
      L2 Advisor: Replace 3 fetches with 1:
      OLD: getAdvisorBook + getAdvisorMixViews + getBooksAdvisorComposition
      NEW: platinum/advisors/{id}/summary.json
    </requirement>

    <requirement id="3">
      L3 Client inline: Replace 4 fetches with 1:
      OLD: getBooksClientDetail + getRelationshipCompositionStatic + getRelationshipMixViews + getBooksRelationshipTimeseries
      NEW: platinum/clients/{id}/summary.json
    </requirement>

    <requirement id="4">
      L3 ClientDetail panels: Replace Lambda reads with direct S3:
      OLD: getMixTimeseries (Lambda) + getConcentrationTimeseries (Lambda)
      NEW: platinum/clients/{id}/mix_timeseries.json + platinum/clients/{id}/concentration.json
    </requirement>

    <requirement id="5">
      L4 Account: Replace Lambda parquet scan with pre-computed JSON:
      OLD: getBooksAccountComposition (Lambda reads parquet)
      NEW: platinum/accounts/{acct_id}/summary.json
    </requirement>

    <requirement id="6">
      Update TypeScript types for platinum response shapes.
      grep verify: zero gold/ references in ClientsTab.tsx and related Books components.
    </requirement>
  </requirements>

  <deliverables>
    <deliverable>Books tab fully wired to platinum/ paths</deliverable>
    <deliverable>Message to COO with fetch reduction counts per drill level</deliverable>
  </deliverables>
</task_order>
