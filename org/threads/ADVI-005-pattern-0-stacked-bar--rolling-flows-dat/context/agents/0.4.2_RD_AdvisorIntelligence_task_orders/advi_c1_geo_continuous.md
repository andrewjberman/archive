# Task Order: Stream C1 — Continuous NNA GEO View (Search + City Drill-down)

```xml
<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-03-03-advi-c1-geo-continuous</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.2_RD_AdvisorIntelligence</issued_to>
    <date>2026-03-03</date>
    <status>pending</status>
  </metadata>

  <objective>
    Implement the continuous NNA GEO view in DistributionTab with top-8 state series,
    a search input for all states, and click-to-drill into per-city data. Data is already
    deployed in timeseries_chart.json as of bd-v2.14.0. No data dependency — start immediately.
    Your first session log from this work satisfies O3 for the COO to schedule alignment threads.
  </objective>

  <references>
    <ref type="prd">docs/architecture/ADVISOR_INTELLIGENCE_COMPLETION.md</ref>
    <ref>portal/src/pages/AdvisorIntelligence/tabs/DistributionTab.tsx</ref>
    <ref>portal/src/pages/AdvisorIntelligence/types.ts</ref>
    <ref>portal/src/api/endpoints/advisor-intelligence.ts</ref>
  </references>

  <scope>
    <pages>
      <page>portal/src/pages/AdvisorIntelligence/</page>
    </pages>
    <files>
      <file action="modify">portal/src/pages/AdvisorIntelligence/tabs/DistributionTab.tsx</file>
      <file action="modify">portal/src/pages/AdvisorIntelligence/types.ts</file>
    </files>
  </scope>

  <requirements>
    <requirement id="C1.1">
      Read DistributionTab.tsx and types.ts before making any changes. Understand the
      current GEO view rendering and the existing timeseries_chart.json data shape
      (geo view: per-state categories; geo_drill: Record of stateKey to per-city data).
    </requirement>
    <requirement id="C1.2">
      Update the GEO continuous NNA view to render the top-8 states as separate series
      in the cumulative NNA chart. Use the same chart type, axis format, color scheme,
      and window toggle as the Assets Overview header panel cumulative NNA chart.
      Data source: timeseries_chart.json geo.categories (top-8 state keys) and geo.data.
    </requirement>
    <requirement id="C1.3">
      Add a search input in the left panel controls that filters across ALL available
      states in timeseries_chart.json geo.categories — not just the top-8 displayed.
      Selecting a state from search results drills into that state's city data.
    </requirement>
    <requirement id="C1.4">
      Implement click-to-drill interaction:
        - Clicking a state series in the chart legend OR selecting from search
          triggers the drill: chart re-renders with per-city series for that state
          (sourced from timeseries_chart.json geo_drill[stateKey])
        - A back/breadcrumb control returns to the state-level view
        - Drill state is local UI state only — no additional API call needed
        - Breadcrumb must display the current level clearly:
          "All States" at state level, "{StateName}" when drilled
    </requirement>
    <requirement id="C1.5">
      Run bunx tsc -b after changes. DE reviews before DT pushes to DEV.
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">Top-8 states render as separate chart series with consistent color and window toggle.</criterion>
    <criterion id="2">Search input filters all available states including those outside top-8.</criterion>
    <criterion id="3">Click-to-drill shows per-city series from geo_drill[stateKey]; breadcrumb returns to state view.</criterion>
    <criterion id="4">bunx tsc -b passes with no new type errors.</criterion>
    <criterion id="5">DE has reviewed and approved before DT pushes to DEV.</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Data is already in S3 — no DS work or DT deploy needed for this stream. Start immediately.</constraint>
    <constraint>Drill state is local React state — do not add a new API endpoint or query for this.</constraint>
    <constraint>Do NOT use emojis in any component, comment, or log output. Plain ASCII only.</constraint>
    <constraint>Read existing task orders (page_inventory, distribution_nomenclature_fix, continuous_view_max_window_clients_fix) before starting. If they conflict with C1 changes, coordinate with DE first.</constraint>
    <constraint>Commit with: git commit --author="0.4.2_RD_AdvisorIntelligence &lt;0.4.2_RD_AdvisorIntelligence@opal.agent&gt;" -m "0.4.2_RD_AdvisorIntelligence: AdvisorIntelligence/DistributionTab -- C1 GEO continuous search and drill"</constraint>
  </constraints>

  <deliverables>
    <deliverable type="commit">DistributionTab.tsx: GEO continuous NNA with search + city drill-down</deliverable>
    <deliverable type="document">Session log documenting the work (satisfies O3 for COO thread scheduling)</deliverable>
  </deliverables>
</task_order>
```
