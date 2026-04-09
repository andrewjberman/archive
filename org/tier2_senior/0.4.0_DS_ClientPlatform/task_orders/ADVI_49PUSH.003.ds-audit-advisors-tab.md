<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-04-08-49push-003-ds</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform~C</issued_to>
    <date>2026-04-08</date>
    <status>pending</status>
    <project_code>ADVI_49PUSH</project_code>
    <wave>1</wave>
    <phase>P2</phase>
    <mcp_identity>Register with MCP as "0.4.0_DS_ClientPlatform~C" (not the base serial). This is your instance ID for this session. Use it for register_agent, heartbeat, and inbox-watch.</mcp_identity>
  </metadata>

  <objective>
    Design audit of the Advisors tab (P2 workstream 2.3). Trace every fetch the AdvisorsTab
    component makes, inventory every rendered field, identify waste and metric divergence,
    and design the platinum file specification for the leaderboard and rolling flows data.
  </objective>

  <context>
    PRD: docs/architecture/ADVI_49PUSH_P2_PRD.md (read section 2.3 in full).

    The Advisors tab renders:
    - Top 3 Highlights (hero cards by metric window: QTD/YTD/1Y/Max)
    - Leaderboard (3 modes: AUA blocks, NNA flows, Growth bars)
    - Role filter checkboxes (architect, implementor, consultant, local_ops)
    - Rolling flows chart (per-advisor NNA bars + cumulative line)
    - 49F House and Unassigned pinned to bottom, excluded from rankings

    Current fetches: employee_leaderboard.json (D_00) + advisor_rolling_flows.json (D_00).

    CRITICAL CROSS-SURFACE TIE: The leaderboard advisor AUA must equal the advisor summary
    AUA in platinum/advisors/{id}/summary.json from Phase 1. The leaderboard NNA must
    equal the NNA in the PartnerAnalytics ADV donut. These are currently produced by DIFFERENT
    scripts (D_00 vs D_02 vs D_01). Your audit must trace this divergence and specify which
    single gold source the platinum design will use.
  </context>

  <compiler_tools_mandate>
    BEFORE reading any .tsx file or tracing any import manually, run these comp-* commands.
    Do NOT skip this. Do NOT use Explore agents.

    1. comp-trace AdvisorsTab --direction both
       -- shows what AdvisorsTab.tsx fetches and what produces those files

    2. comp-trace employee_leaderboard --direction both
       -- full chain: who produces it, who consumes it

    3. comp-trace advisor_rolling_flows --direction both
       -- full chain for rolling flows data

    4. comp-trace D_00 --all
       -- lists all D_00 function nodes + S3 write targets (leaderboard is shared with Books N1)

    5. comp-blast build_employee_leaderboard
       -- blast radius from the leaderboard builder -- shows all consumers

    6. comp-blast advisor_rolling_flows
       -- blast radius from the rolling flows artifact

    7. comp-trace getAdvisorRollingFlows --direction up
       -- trace the API endpoint to its data source

    THEN use comp-pipescript for authoritative script-level I/O:

    8. comp-pipescript io D_00
       -- every S3 key D_00 reads and writes (source of leaderboard + rolling flows)

    9. comp-pipescript consumers D_00
       -- what consumes D_00 output (verify leaderboard is terminal/portal-only)

    comp-pipescript is AUTHORITATIVE for script I/O (AST-parsed from s3_layout.py).

    THEN use comp-routes for serving layer traces:

    10. comp-routes trace AdvisorsTab
        -- every fetch AdvisorsTab makes, traced end-to-end through serving layer

    11. comp-routes trace getEmployeeLeaderboard
        -- full chain: URL -> CF behavior -> origin -> auth -> router -> S3 key

    12. comp-routes trace getAdvisorRollingFlows
        -- serving chain for rolling flows data

    Use ALL THREE tool families to build your fetch trace table:
    - comp-routes: how data gets from S3 to browser
    - comp-pipescript: how data gets produced
    - comp-trace: cross-layer connections
    Then READ AdvisorsTab.tsx to confirm which fields are actually rendered vs fetched-but-unused.
  </compiler_tools_mandate>

  <scope>
    <files>
      <file action="read">portal/src/pages/AdvisorIntelligence/tabs/AdvisorsTab.tsx</file>
      <file action="read">portal/src/api/endpoints/advisor-intelligence.ts</file>
      <file action="read">data/black_diamond/scripts/gold/D_00.portal_aggregates.py</file>
      <file action="create">docs/briefs/ADVI_49PUSH_P2_2.3_advisors_tab.md</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">
      Follow the Phase 2 audit methodology (PRD section "Audit Methodology"):
      Step 1: Trace the frontend (every useEffect, useQuery, data fetch)
      Step 2: Trace the API layer (direct S3 vs Lambda)
      Step 3: Trace to gold source (which script, which function)
      Step 4: Identify waste + divergence
      Step 5: Design platinum output
      Step 6: Cross-surface consistency matrix
    </requirement>

    <requirement id="2">
      Answer these specific questions from the PRD:
      a) How large is employee_leaderboard.json? Can it be trimmed (e.g., exclude zero-AUA advisors)?
      b) advisor_rolling_flows.json: how much of the time series does the chart render?
         The TOP_N_CHART = 10 constant suggests only top 10. Verify in the .tsx.
      c) Should the Advisors tab share platinum/firm/dashboard.json (Phase 1) for leaderboard
         data, or get its own platinum/firm/leaderboard.json?
      d) Rolling flows: are both architects[] and implementors[] splits rendered, or only
         the role-filtered subset?
    </requirement>

    <requirement id="3">
      CROSS-SURFACE NUMBER TIE ANALYSIS (the most important part of this audit):
      For each of these metrics, trace the EXACT gold source row that produces the value
      on the Advisors tab, and document whether it matches the source for the same metric
      on other surfaces:

      | Metric | Advisors Tab Source | Books L2 Source | PartnerAnalytics Source | Same? |
      |--------|-------------------|-----------------|------------------------|-------|
      | Advisor AUA | ? | ? | ? | ? |
      | Advisor NNA YTD | ? | ? | ? | ? |
      | Advisor Growth % | ? | ? | ? | ? |
      | Advisor Client Count | ? | ? | N/A | ? |

      If they diverge, specify which single source the platinum design should use.
    </requirement>

    <requirement id="4">
      Design deliverable: Platinum file specs for:
      - platinum/firm/leaderboard.json (or embedded in dashboard.json -- make a recommendation)
      - platinum/firm/rolling_flows.json
      Document: approximate size, gold source per field, shared vs exclusive.
    </requirement>
  </requirements>

  <deliverables>
    <deliverable>docs/briefs/ADVI_49PUSH_P2_2.3_advisors_tab.md -- full audit + platinum spec + cross-surface tie analysis</deliverable>
    <deliverable>Session log documenting: comp-* traces run, divergence findings, design decisions</deliverable>
  </deliverables>

  <do_not>
    <rule>Do NOT write any code -- this is design only</rule>
    <rule>Do NOT use Explore agents -- use comp-trace and comp-blast for all tracing</rule>
    <rule>Do NOT design a leaderboard platinum file without resolving the cross-surface metric divergence</rule>
  </do_not>
</task_order>
