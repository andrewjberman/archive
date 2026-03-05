# Task Order: Yang V2 Y8 — Continuous AUA Area Chart to Stacked Bar — 0.4.2_RD_AdvisorIntelligence

```xml
<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-03-04-ADVI_YANGV2.Y8.continuous-aua-stacked-bar</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.2_RD_AdvisorIntelligence</issued_to>
    <date>2026-03-04</date>
    <status>complete</status>
    <priority>HIGH — unblocked, no data dependency, start after ADVI-Y1-Y4-Y6-Y12</priority>
    <stream>Y8</stream>
  </metadata>

  <objective>
    In DistributionTab, the Continuous GEO-AUA and Continuous ADV-AUA views currently
    render as AreaChart components. Yang requires these to be replaced with stacked bar
    charts, with an Interval toggle (Month / Quarter / Year) added to each view's controls.

    All required data is already present in timeseries_chart.json. This is a frontend-only
    change. No DS or DT deployment needed.
  </objective>

  <references>
    <ref type="prd" priority="PRIMARY">docs/architecture/ADVISOR_INTELLIGENCE_YANG_FEEDBACK_V2.md — Section 2.5</ref>
    <ref type="portal-distribution">portal/src/pages/AdvisorIntelligence/tabs/DistributionTab.tsx</ref>
    <ref type="portal-header">portal/src/pages/AdvisorIntelligence/components/PartnerAnalytics.tsx</ref>
    <ref type="aggregation-pattern">PartnerAnalytics.tsx uses getPeriodInfo() and aggregatedAuaData logic for Month/Quarter/Year bucketing — reuse this pattern</ref>
  </references>

  <toggle_state_decision>
    COO design decision: The Interval toggle (Month / Quarter / Year) is scoped per-view.
    GEO continuous AUA and ADV continuous AUA each have their own independent toggle state.
    There is no shared interval state at the tab level for these views. This avoids
    unnecessary state coordination and matches the existing pattern in PartnerAnalytics.tsx
    where each panel manages its own period state.

    DE does not need to be consulted before implementation. This decision is final.
  </toggle_state_decision>

  <requirements>

    <!-- ================================================================ -->
    <!-- Y8 — Replace AreaChart with BarChart (stacked) + Interval Toggle -->
    <!-- ================================================================ -->
    <requirement id="Y8.1">
      Read DistributionTab.tsx in full before making any changes. Identify the existing
      Continuous GEO-AUA and Continuous ADV-AUA rendering paths (likely the same
      ContinuousChartView component used for NNA, parametrized by metric='aua' or similar,
      or separate chart components). Confirm the chart type currently in use (AreaChart).
    </requirement>

    <requirement id="Y8.2">
      Replace the AreaChart with a stacked BarChart for both GEO-AUA and ADV-AUA
      continuous views.

      Chart specification:
        - Chart type: Recharts BarChart (same import alias used elsewhere)
        - Stacking: all category series use the same stackId (e.g., stackId="aua")
        - Categories: same as current (NMNC and NMEC at minimum; extend if more exist)
        - Colors: unchanged (CATEGORY_COLORS.NMNC, CATEGORY_COLORS.NMEC)
        - X-axis: period labels (derived from the Interval toggle — see Y8.3)
        - Y-axis: AUA formatted as dollar amount (same formatting as current)
        - Tooltip: unchanged behavior (show category breakdown per period)
        - Legend: unchanged

      Reuse the aggregation logic from PartnerAnalytics.tsx (getPeriodInfo() or equivalent
      helper) to bucket daily data into Month / Quarter / Year period bars. Do not duplicate
      the aggregation logic — import or move it to a shared util if not already shared.
    </requirement>

    <requirement id="Y8.3">
      Add an Interval toggle to each continuous AUA view's panel controls.
      Toggle options: Month | Quarter | Year
      Default: Month (most granular, matches the user's expectation for continuous data).

      State: local to the view component (per Y8 toggle state decision above).
      The toggle drives the period bucketing for the BarChart data:
        Month -> one bar per calendar month
        Quarter -> one bar per calendar quarter (Q1/Q2/Q3/Q4)
        Year -> one bar per calendar year

      Reuse the same Interval toggle pattern from PartnerAnalytics.tsx if it exists, or
      implement using the existing tab's toggle component pattern (look at how period
      toggles are implemented in DistributionTab.tsx or AdvisorsTab.tsx for consistency).
    </requirement>

    <requirement id="Y8.4">
      The change applies to BOTH Continuous GEO-AUA and Continuous ADV-AUA views.
      If they share a component (e.g., a single ContinuousChartView with metric prop),
      the change applies at the component level — both views change together.
      If they are separate components or rendered branches, update each separately.

      Continuous NNA views (GEO and ADV) are NOT changed by Y8 — they retain the
      existing line/area format. Only AUA metric changes to stacked bar.
    </requirement>

  </requirements>

  <acceptance_criteria>
    <criterion id="1">Continuous GEO-AUA and ADV-AUA render as stacked BarChart (not AreaChart).</criterion>
    <criterion id="2">Interval toggle (Month / Quarter / Year) is present in both AUA continuous views.</criterion>
    <criterion id="3">Toggle drives period bucketing: switching Month/Quarter/Year changes bar grouping.</criterion>
    <criterion id="4">NMNC and NMEC categories retain their colors. Stacking is correct (NMNC on top per Y1 fix).</criterion>
    <criterion id="5">Continuous NNA views are unchanged.</criterion>
    <criterion id="6">Toggle state is per-view, not shared across GEO and ADV.</criterion>
    <criterion id="7">tsc clean. No unused AreaChart imports left behind.</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Do NOT change the continuous NNA views (GEO or ADV) — this task is AUA only.</constraint>
    <constraint>Do NOT add the Interval toggle to any non-AUA view in this task order.</constraint>
    <constraint>Do NOT modify the aggregation data contract or call new API endpoints.</constraint>
    <constraint>Reuse existing aggregation helpers from PartnerAnalytics.tsx — do not reinvent.</constraint>
    <constraint>Do NOT use emojis in any code or log output.</constraint>
    <constraint>Commit with: git commit --author="0.4.2_RD_AdvisorIntelligence &lt;0.4.2_RD_AdvisorIntelligence@opal.agent&gt;" -m "..."</constraint>
  </constraints>

  <what_this_unlocks>
    Standalone. No downstream gates.
    When Y9-FE ships (after DS data batch + Pattern 0 thread), the interval toggle
    pattern established here will be reused for Continuous NNA diverging bar.
  </what_this_unlocks>

  <deliverables>
    <deliverable type="commit">portal DEV: Y8 continuous AUA stacked bar + Interval toggle</deliverable>
    <deliverable type="document">Session log with portal DEV commit hash</deliverable>
  </deliverables>

</task_order>
```
