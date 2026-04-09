<task_order>
  <metadata>
    <id>1.0.0_SA_CTO-2026-04-09-49push-035-de</id>
    <issued_by>1.0.0_SA_CTO</issued_by>
    <issued_to>0.4.0_DE_ClientPlatform~B</issued_to>
    <date>2026-04-09</date>
    <status>complete -- fix_1 (ContinuousMetricBox) pre-existing, fix_2 (Search) DONE (2e94a2c), fix_3 (3-level drill) DONE (2e94a2c), fix_4 (New Clients + granularity) pre-existing. Data validation blocked on AE re-run.</status>
    <project_code>ADVI_49PUSH</project_code>
    <wave>8</wave>
    <phase>Distribution P2-2</phase>
    <mcp_identity>Register with MCP as "0.4.0_DE_ClientPlatform" before starting.</mcp_identity>
  </metadata>

  <objective>
    Distribution tab P2-2: Fix Continuous-GEO-NNA view. Four issues:
    1. Match the metric box layout and styling of P2-1 (same box format, NNA values)
    2. Add State Selection / Search (same as P2-1, ported for NNA)
    3. Add city-level NNA drilldown (Level 0 firm → Level 1 state → Level 2 city)
    4. Add New Clients box
    Also: remove local granularity toggle if present, apply Other-not-clickable rule.
  </objective>

  <context>
    File: portal/src/pages/AdvisorIntelligence/tabs/DistributionTab.tsx
    ContinuousNnaDivergingView (starts ~line 541).

    P2-1 (AUA) has three metric boxes: Total AUA, ValueSincePeriodStart, GrowthRate.
    P2-2 (NNA) already has three metric boxes (lines 692-704): Inflows, Outflows, Net NNA.
    The issue: P2-2's boxes are styled differently from P2-1's boxes, and the layout/padding
    may differ. Andrew wants them to look identical -- same card styling, same proportions --
    just with NNA-appropriate values.

    Mapping P2-1 → P2-2:
      Total AUA              → Total NNA (net for the selected window)
      ValueSincePeriodStart  → Inflows (total inflows for the window)
      GrowthRate             → Outflows (total outflows for the window)
      New Clients            → New Clients (same box, same data source)
  </context>

  <fix_1 label="Match P2-1 metric box layout and styling">
    <description>
      Identify the metric box component/styling used in P2-1 (ContinuousAuaStackedView).
      The three boxes render Total AUA, ValueSincePeriodStart, GrowthRate.
      Apply the identical container, border, background, padding, and typography to
      ContinuousNnaDivergingView's Inflows/Outflows/Net NNA boxes.

      If P2-1 uses a reusable MetricBox or SummaryTile component, use the same component
      in P2-2. If the boxes are inline JSX in each view, extract them to a shared component
      to avoid drift between the two:
        <ContinuousMetricBox label="..." value={...} subLine="..." />
      This shared component is then used in P2-1, P2-2, P2-3, P2-4 identically.

      Note: "Net NNA" label in the third box becomes "Net New Assets" per .031 fix_1.
    </description>
  </fix_1>

  <fix_2 label="State Selection / Search for NNA view">
    <description>
      Port the Search + state selection from P2-1 (.034 fix_2) to the NNA view.
      The NNA view should have an identical search input above its chart.
      Selecting a state drills to that state's NNA series (Level 1).
      Same opaque dropdown, same Other-not-clickable guard, same breadcrumb navigation.

      The ContinuousNnaDivergingView already has a drillParent local state (line 543).
      The search input needs to be wired to setDrillParent just as in the AUA view.
      Share the same Search UI component if one was extracted in .034 -- do not duplicate.
    </description>
  </fix_2>

  <fix_3 label="City-level NNA drilldown (three levels)">
    <description>
      Implement the three-level NNA drill in the GEO-NNA continuous view:

      Level 0 (no state selected):
        Show firm-aggregate NNA diverging bar by state (existing nna_geo behavior).
        Breadcrumb: none / "All States"

      Level 1 (state clicked):
        Show the selected state's NNA as a single diverging bar series (not by city).
        This is: the state's own inflow/outflow/net over the period.
        Data: nna_geo[stateKey] time series.
        Breadcrumb: "All States > {State Name}"

      Level 2 (city clicked from Level 1):
        Show the selected city's NNA diverging bar series.
        Data: nna_geo_drill[stateKey] (DS .033 issue_2) -- city-breakdown NNASeriesView.
        Apply enforceTop9Other to city categories.
        Breadcrumb: "All States > {State} > {City}"
        "Other" at Level 1 (the Other state aggregate) is NOT clickable.
        "Other" at Level 2 (the Other city aggregate) is NOT clickable.

      Back navigation: clicking breadcrumb at any level returns to that level.
      Clicking the chart background or a "back" button returns to the level above.
    </description>
  </fix_3>

  <fix_4 label="New Clients box + granularity toggle removal">
    <description>
      New Clients box: identical to P2-1 fix_5. Use the same ContinuousMetricBox
      component and the same data source (chartData?.new_clients_by_period?.[granularity]).

      Granularity toggle: if ContinuousNnaDivergingView has its own granularity/interval
      state, remove it and use the parent granularity prop (same as .034 fix_1).
      Check: the NNA view uses granularity for period aggregation (line ~1204 area).
      Ensure it reads from the prop, not from local state.
    </description>
  </fix_4>

  <acceptance_criteria>
    1. P2-2 metric boxes are visually identical to P2-1 boxes (shared component)
    2. Total NNA / Inflows / Outflows / New Clients boxes all present and styled consistently
    3. Search input present, opaque dropdown, connects to state drill
    4. Three-level drill works: firm → state → city, breadcrumb updates at each level
    5. "Other" is never clickable at any level in any view
    6. No internal granularity toggle -- uses parent prop
    7. "Net NNA" label replaced with "Net New Assets" per .031
    8. Build clean, no TypeScript errors
  </acceptance_criteria>


  <compiler_tools>
    comp-transform trace DistributionTab
      -- Run before fix_1 (box styling match). Shows the exact JSX render path for
         both ContinuousNnaDivergingView and ContinuousAuaStackedView hero metric tiles.
         Confirms which component renders which box so the shared ContinuousMetricBox
         extraction is surgical and doesn't break existing layout.

    comp-cache collisions
      -- Run after adding 3-level drill state (firm → state → city). The new drill
         keys must be distinct from the top-level NNA chart key or stale data will
         appear when drilling back up.

    comp-pii scan DistributionTab
      -- Run before shipping. City names are not PII but confirm no relationship
         names have leaked into the city drill view from the nna_geo_drill data.
  </compiler_tools>

</task_order>
