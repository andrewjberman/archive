<task_order>
  <metadata>
    <id>1.0.0_SA_CTO-2026-04-09-49push-041-de</id>
    <issued_by>1.0.0_SA_CTO</issued_by>
    <issued_to>0.4.0_DE_ClientPlatform~A</issued_to>
    <date>2026-04-09</date>
    <status>COMPLETE -- page built (commit c450ece DEV). Degrades gracefully until DS .040 ships drilldown_summary.json + per-role timeseries fields.</status>
    <project_code>ADVI_49PUSH</project_code>
    <wave>10</wave>
    <phase>Advisor drilldown page</phase>
    <mcp_identity>Register with MCP as "0.4.0_DE_ClientPlatform" before starting.</mcp_identity>
  </metadata>

  <objective>
    Build the Advisor Drilldown page. Clicking any advisor row in the Advisors tab
    leaderboard navigates to a full-page view with a 2x2 layout: summary card (top-left),
    role composition donut (top-right), and a full-width time series chart (bottom).
  </objective>

  <layout>
    The approved 2x2 grid:

      ┌─────────────────────────┬─────────────────────────┐
      │  SUMMARY CARD  (1×1)    │  ROLE DONUT     (1×1)   │
      │  identity, AUA,         │  donut by role,         │
      │  flows, fee             │  canonical role colors  │
      └─────────────────────────┴─────────────────────────┘
      ┌─────────────────────────────────────────────────────┐
      │  TIME SERIES             (2×1, full width)          │
      │  [AUA] NNA toggle   QTD | YTD | 1Y | Max           │
      └─────────────────────────────────────────────────────┘

    Top row: equal-width halves (50/50), matching height.
    Bottom row: full width, taller than the top row (~55% of total page height).
    Both rows sit inside the existing ADVI page chrome (nav, header).
  </layout>

  <navigation>
    Entry point: clicking an advisor row in AdvisorsTab LeaderboardCards or the
    bar chart sends the user to this page. Use React Router navigation:
      /advisor-intelligence/advisors/{advisor_id}
    If the ADVI page does not yet have nested routes, add one for this path.
    The advisor_id is the slug-formatted name (same as used in platinum S3 paths).

    Page header:
      ← Back to Advisors      {ADVISOR NAME}      ● {Role1}  ● {Role2} ...
    The back button returns to AdvisorsTab, preserving the period and metric toggle state.
    Role badges use canonical role colors (same as the donut and chart).
  </navigation>

  <panel_1 label="Top-left: Summary Card">
    <description>
      Data source: platinum/advisors/{id}/summary.json (already fetched by
      getPlatinumAdvisorSummary or a new dedicated endpoint -- see data_fetching below).

      Three sections separated by subtle dividers (border-t border-white/10):

      SECTION A -- Identity:
        Active Since    {active_since formatted as "MMM DD, YYYY"}
        Roles           rendered as colored badges matching canonical colors

      SECTION B -- AUA (static, not window-sensitive):
        Total AUA       {tagged_aua}         formatted as currency
        Accounts        {account_count}      integer
        Clients         {client_count}       integer

      SECTION C -- Flows (window-sensitive -- updates with time window toggle):
        Net New Assets  {period NNA}         derived from timeseries (see flows_derivation)
        Inflows         {period inflows}     derived from timeseries
        Outflows        {period outflows}    derived from timeseries
        New Clients     {new_clients}        from leaderboard window data

      SECTION D -- Fee:
        Fee-Earning AUA   {fee_earning_aua}
        Non-Fee AUA       {non_fee_earning_aua}
        Avg Fee Rate      {avg_fee_bps_earned} bps
        (NO "Implied Rev / yr" -- excluded by design decision)

      Layout: label left (text-white/50, text-xs), value right (text-white, text-sm font-medium).
      Same two-column pattern used throughout ADVI tooltips and hero tiles.
      Card background: bg-white/5 border border-white/10 rounded-xl p-6.
    </description>

    <flows_derivation>
      The flows section derives period values from platinum/advisors/{id}/timeseries.json
      using window boundaries, not from pre-bucketed data.

      Given the selected window (QTD/YTD/1Y/Max):
        1. Determine window start date (same logic as the timeseries chart X-axis cutoff)
        2. Find the timeseries data point on or before the window start date -- call it P_start
        3. Find the latest data point -- call it P_end
        4. period_nna      = P_end.nna - P_start.nna
           period_inflows  = P_end.cum_inflows - P_start.cum_inflows
           period_outflows = P_end.cum_outflows - P_start.cum_outflows
      This is the same differencing pattern used in _aggregate_nna_to_periods (D_04).
      Flows update reactively when the window toggle changes.
    </flows_derivation>
  </panel_1>

  <panel_2 label="Top-right: Role Composition Donut">
    <description>
      Data source: summary.json role_breakdown section.

      Recharts PieChart with innerRadius (donut style).
      Center label: tagged_aua (the firm-verified total, formatted as currency).
      Center sub-label: "Total AUA"

      Segments (one per role with non-zero AUA):
        architect, implementor, consultant, local_ops, additional_advisor
      Each segment sized by role_breakdown[role].aua.

      Colors: use the SAME canonical role color constants as the time series chart
      checkboxes. Define these in a shared location (e.g. chartColors.ts):
        ROLE_COLORS = {
          architect:          '#60a5fa',   // blue-400 (or existing PALETTE value)
          implementor:        '#34d399',   // emerald-400
          consultant:         '#a78bfa',   // violet-400
          local_ops:          '#fb923c',   // orange-400
          additional_advisor: '#22d3ee',   // cyan-400
        }
      These five colors must be identical in the donut and in the stacked area chart.
      If canonical colors already exist elsewhere in the codebase, use those -- do not
      introduce new color values.

      Legend below the donut (or to the right if space allows):
        ■ {Role Label}    ${AUA}    {pct_of_tagged}%
      One row per role with non-zero AUA. Role label formatted as title case
      ("Local Ops" not "local_ops"). pct_of_tagged from role_breakdown.

      Note: percentages will NOT sum to 100% if the advisor holds multiple roles on
      shared accounts. This is correct. Do not normalize them. If needed, add a
      footnote: "Percentages reflect role overlap and may exceed 100% in aggregate."
    </description>
  </panel_2>

  <panel_3 label="Bottom: Time Series (full width)">
    <description>
      Data source: platinum/advisors/{id}/timeseries.json

      Two toggles in the panel header:
        Left toggle:  [AUA] NNA  (AUA is default, underlined/highlighted active)
        Right toggle: QTD | YTD | 1Y | Max

      The right toggle (window) is shared state with the flows section in panel_1.
      Changing the window updates both the chart AND the flows section simultaneously.

      AUA VIEW (default):
        Recharts AreaChart, stacked=true.
        X-axis: date, filtered to selected window.
        Y-axis: formatted currency ($XXXm).
        Five area series, one per role:
          dataKey="architect_aua"    fill + stroke = ROLE_COLORS.architect
          dataKey="implementor_aua"  fill + stroke = ROLE_COLORS.implementor
          dataKey="consultant_aua"   fill + stroke = ROLE_COLORS.consultant
          dataKey="local_ops_aua"    fill + stroke = ROLE_COLORS.local_ops
          dataKey="addl_advisor_aua" fill + stroke = ROLE_COLORS.additional_advisor
        Fill opacity: 0.75 for bottom series, decreasing slightly for each layer above.
        Tooltip: on hover shows date + all five role AUA values + total_aua.
          Exclude roles with 0 AUA from the tooltip to keep it clean.
        Legend: five checkboxes matching role colors (same style as Distribution tab legends).
          Clicking a checkbox toggles that role series on/off in the chart.
          All checked by default.

      NNA VIEW:
        Recharts ComposedChart (bars + line), same pattern as firm NNA view.
        X-axis: period labels (derived from timeseries by grouping dates into
                QTD/YTD/1Y/Max periods and differencing cumulative values).
        Two bar series (stacked): inflows (positive, green), outflows (negative, red).
        One line series: net NNA, colored by sign per period.
        Tooltip: period label + Inflows + Outflows + Net New Assets.
        Legend: ■ Inflows  ■ Outflows  — Net New Assets
        Does NOT break out by role (NNA is not role-partitioned by design).

      Smooth animation on toggle between AUA and NNA.
      Smooth animation on window change (data filters, not full re-render).
    </description>
  </panel_3>

  <data_fetching>
    New API function in advisor-intelligence.ts:
      getPlatinumAdvisorTimeseries(advisorId: string, firmId: string)
        → GET platinum/advisors/{id}/timeseries.json via S3/CloudFront
        → return type: AdvisorTimeseriesResponse

    The summary.json is already fetched by getPlatinumAdvisorSummary.
    Reuse it for the summary card and donut. Fire both fetches in parallel on page load.

    New TypeScript types needed (types.ts):
      AdvisorTimeseriesPoint {
        date: string
        total_aua: number
        cum_inflows: number
        cum_outflows: number
        nna: number
        architect_aua: number
        implementor_aua: number
        consultant_aua: number
        local_ops_aua: number
        addl_advisor_aua: number
      }
      AdvisorTimeseriesResponse {
        advisor_id: string
        advisor_name: string
        data_as_of: string
        data: AdvisorTimeseriesPoint[]
      }
  </data_fetching>

  <pii_note>
    The advisor drilldown page does not show client names at this stage.
    The summary card shows aggregate counts only (Clients: N, Accounts: N).
    No client roster or relationship-level data is rendered here.
    PII rules from .032 apply if/when client names are added in a future wave.
  </pii_note>

  <acceptance_criteria>
    1. Clicking an advisor in the leaderboard navigates to /advisor-intelligence/advisors/{id}
    2. Back button returns to AdvisorsTab with previous toggle state preserved
    3. Summary card: all four sections render correctly, flows update on window change
    4. Donut: five role segments, canonical colors, center = tagged_aua, legend with AUA + pct
    5. AUA chart: stacked area with role breakdown, checkboxes toggle series on/off
    6. NNA chart: diverging bars + NNA line, period-level (not daily)
    7. Window toggle (QTD/YTD/1Y/Max) updates both the chart AND the flows section simultaneously
    8. "Implied Rev / yr" does NOT appear anywhere in this component
    9. Role colors are identical between the donut and the stacked area chart
    10. Build clean, no TypeScript errors
    11. comp-pii scan passes: no client names rendered
  </acceptance_criteria>


  <compiler_tools>
    comp-platinum page AdvisorsTab
      -- Run before building the drilldown. Full-stack trace of AdvisorsTab: page →
         component → fetch → CloudFront → auth → S3 key → gold script → upstream deps.
         Confirms the serving path for platinum/advisors/{id}/summary.json and
         platinum/advisors/{id}/timeseries.json. Tells you what Lambda route and CF
         behavior to use for the new getPlatinumAdvisorTimeseries endpoint.

    comp-routes trace getPlatinumAdvisorSummary
      -- Verifies the existing advisor summary endpoint's serving path. The new
         timeseries endpoint should follow the same routing pattern. Run to confirm
         the pattern before implementing getPlatinumAdvisorTimeseries.

    comp-cache collisions
      -- Run after adding the new route (/advisor-intelligence/advisors/{id}).
         The new React Query keys for advisor timeseries and summary must not
         collide with the leaderboard's existing advisor-level keys.

    comp-transform schema-check AdvisorDrilldownPage
      -- Run after building the page. Confirms all three panels are wired to their
         data sources and no AdvisorTimeseriesPoint fields are UNUSED.

    comp-pii scan AdvisorDrilldownPage
      -- Run before shipping. Confirms no client names are rendered (the summary
         card shows aggregate counts only). Required gate per .032 rule.
  </compiler_tools>

</task_order>
