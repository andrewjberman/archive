<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-04-08-49push-014-de</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DE_ClientPlatform~C</issued_to>
    <date>2026-04-08</date>
    <status>pending</status>
    <project_code>ADVI_49PUSH</project_code>
    <wave>3</wave>
    <phase>P3</phase>
    <mcp_identity>Register with MCP as "0.4.0_DE_ClientPlatform~C" (not the base serial). This is your instance ID for this session. Use it for register_agent, heartbeat, and inbox-watch.</mcp_identity>
  </metadata>

  <objective>
    Rewire Advisors tab (AdvisorsTab.tsx) fetches to platinum/ paths.
  </objective>

  <context>
    Audit brief: docs/briefs/ADVI_49PUSH_P2_2.3_advisors_tab.md
    Master catalog: docs/briefs/ADVI_49PUSH_P2_platinum_file_catalog.md

    Key finding from audit: advisor_rolling_flows.json (52MB) is dead — already removed
    from gold scripts (.010). getAdvisorRollingFlows already removed from API layer (.010).

    DT (0.4.0_DT_ClientPlatform) is updating the serving layer in parallel (.011).
    Message them via MCP to agree on URL patterns before finalizing fetches.
  </context>

  <compiler_tools_mandate>
    1. comp-routes trace getEmployeeLeaderboard
    2. comp-trace AdvisorsTab --direction both
    3. comp-routes auth-map
  </compiler_tools_mandate>

  <requirements>
    <requirement id="1">
      Advisors tab:
      OLD: getEmployeeLeaderboard -> gold/artifacts/employee_leaderboard.json (681KB)
      NEW: platinum/firm/leaderboard.json (~15KB, QTD+YTD only)

      NOTE: getAdvisorRollingFlows is already removed (.010). If AdvisorsTab.tsx still
      references it, remove the reference.
    </requirement>

    <requirement id="2">
      Update TypeScript types — leaderboard.json is trimmed (QTD+YTD windows only,
      stripped fee/efficiency fields not rendered). Types must match the reduced schema.
    </requirement>

    <requirement id="3">
      grep verify: zero gold/ references in AdvisorsTab.tsx.
    </requirement>
  </requirements>

  <deliverables>
    <deliverable>AdvisorsTab wired to platinum/</deliverable>
    <deliverable>Message to COO with fetch reduction counts</deliverable>
  </deliverables>
</task_order>
