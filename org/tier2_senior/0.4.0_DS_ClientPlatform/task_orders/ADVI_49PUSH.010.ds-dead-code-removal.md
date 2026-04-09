<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-04-08-49push-010-ds</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform~C</issued_to>
    <date>2026-04-08</date>
    <status>pending</status>
    <project_code>ADVI_49PUSH</project_code>
    <wave>2b</wave>
    <phase>P3</phase>
    <mcp_identity>Register with MCP as "0.4.0_DS_ClientPlatform~C" (not the base serial). This is your instance ID for this session. Use it for register_agent, heartbeat, and inbox-watch.</mcp_identity>
  </metadata>

  <objective>
    Remove dead code and dead artifacts identified during the Phase 2 audits.
    Three dead items confirmed by the audits:
    1. advisor_rolling_flows.json (52MB, never fetched by any portal component)
    2. getAdvisorRollingFlows API endpoint (never imported by any component)
    3. architect_leaderboard.json (legacy, superseded by employee_leaderboard)
  </objective>

  <context>
    Wave 1 audit findings:
    - ~C (.003): advisor_rolling_flows.json is 52MB, produced by D_00:build_advisor_rolling_flows,
      but NO portal component imports getAdvisorRollingFlows. Confirmed deprecated.
    - ~C (.003): getAdvisorRollingFlows exists in advisor-intelligence.ts but is never imported.
    - Master catalog (.007): architect_leaderboard.json flagged as legacy dead code.

    This cleanup ships with the same AE deploy as the D_04 expansion, so removing the
    generation code reduces gold runner time and S3 storage.
  </context>

  <compiler_tools_mandate>
    BEFORE removing anything, verify it is truly dead:

    1. comp-trace advisor_rolling_flows --direction both --all
       -- confirm no downstream consumers

    2. comp-blast build_advisor_rolling_flows
       -- confirm no blast radius

    3. comp-trace architect_leaderboard --direction both --all
       -- confirm no downstream consumers

    4. comp-blast build_architect_leaderboard
       -- confirm no blast radius

    5. comp-routes trace getAdvisorRollingFlows
       -- confirm no serving route consumes this

    6. comp-pipescript consumers D_00
       -- verify which D_00 outputs are actually consumed

    7. Grep for "rolling_flows" across portal/src/ to triple-confirm no component imports it
    8. Grep for "architect_leaderboard" across portal/src/ to triple-confirm

    Only remove code after ALL checks confirm dead. If ANY check shows a live consumer,
    do NOT remove -- report to COO.
  </compiler_tools_mandate>

  <scope>
    <files>
      <file action="modify">data/black_diamond/scripts/gold/D_00.portal_aggregates.py</file>
      <file action="modify">portal/src/api/endpoints/advisor-intelligence.ts</file>
      <file action="reference">data/black_diamond/scripts/gold/lib/s3_layout.py</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">
      D_00.portal_aggregates.py:
      - Remove build_advisor_rolling_flows() function entirely
      - Remove build_architect_leaderboard() function entirely
      - Remove their calls from main()
      - Remove any imports only used by these functions
      - Do NOT remove any other D_00 functions (build_employee_leaderboard,
        build_timeseries_chart, build_clients_tab, etc. are all live)
    </requirement>

    <requirement id="2">
      advisor-intelligence.ts:
      - Remove getAdvisorRollingFlows() function
      - Remove its type definitions if they are exclusive to this function
      - Do NOT remove other API functions
    </requirement>

    <requirement id="3">
      lib/s3_layout.py:
      - Check if ADVISOR_ROLLING_FLOWS and ARCHITECT_LEADERBOARD constants exist
      - If they do, and no other script imports them (verify with comp-pipescript), remove them
      - If other scripts import them, leave them and document
    </requirement>

    <requirement id="4">
      Do NOT delete the S3 objects themselves (gold/artifacts/advisor_rolling_flows.json,
      gold/artifacts/architect_leaderboard.json). That's an AE task. This TO only removes
      the code that generates them.
    </requirement>

    <requirement id="5">
      py_compile D_00.portal_aggregates.py after modifications.
      All changes must be ASCII only, no emojis.
    </requirement>
  </requirements>

  <deliverables>
    <deliverable>D_00.portal_aggregates.py cleaned (2 dead builders removed)</deliverable>
    <deliverable>advisor-intelligence.ts cleaned (1 dead endpoint removed)</deliverable>
    <deliverable>lib/s3_layout.py cleaned if applicable</deliverable>
    <deliverable>Message to COO (2.0.0_SA_COO) confirming: what was removed, what was kept, verification results</deliverable>
  </deliverables>

  <do_not>
    <rule>Do NOT remove any function without first verifying it is dead via comp-* tools + Grep</rule>
    <rule>Do NOT delete S3 objects -- only remove generation code</rule>
    <rule>Do NOT remove build_employee_leaderboard or any other live D_00 function</rule>
    <rule>Do NOT deploy -- AE handles that</rule>
  </do_not>
</task_order>
