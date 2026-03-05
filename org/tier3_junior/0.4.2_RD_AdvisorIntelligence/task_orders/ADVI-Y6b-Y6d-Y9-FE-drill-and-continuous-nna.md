# Task Order: Yang V2 Y6b-FE + Y6d-FE + Y9-FE — Snapshot Drill + Continuous NNA Diverging Bar — 0.4.2_RD_AdvisorIntelligence

```xml
<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-03-05-ADVI-Y6b-Y6d-Y9-FE-drill-and-continuous-nna</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.2_RD_AdvisorIntelligence</issued_to>
    <date>2026-03-05</date>
    <status>complete</status>
    <priority>HIGH</priority>
    <streams>Y6b-FE, Y6d-FE, Y9-FE</streams>
  </metadata>

  <objective>
    Three DistributionTab changes from Yang V2 Phase 3:

    Y6b-FE: Add city-level drill-down to Snapshot GEO-NNA histogram (clicking a state
            bar loads the city distribution for that state).

    Y6d-FE: Add relationship-level drill-down to Snapshot ADV-NNA histogram (clicking
            an architect bar loads the per-relationship distribution for that architect).

    Y9-FE:  Replace the line/area chart in Continuous GEO-NNA and Continuous ADV-NNA
            views with a diverging bar chart (inflow above / outflow below), at all
            drill levels. At relationship grain (ADV drill), simplify to a single
            green/pink bar (positive/negative NNA).

    Gate: DE type wiring (ADVI-Y-phase3-de-type-wiring) must be committed to portal DEV.
  </objective>

  <references>
    <ref type="prd">docs/architecture/ADVISOR_INTELLIGENCE_YANG_FEEDBACK_V2.md — Sections 2.2b, 2.3b, 2.6</ref>
    <ref type="portal-distribution">portal/src/pages/AdvisorIntelligence/tabs/DistributionTab.tsx</ref>
    <ref type="types">portal/src/pages/AdvisorIntelligence/types.ts — NNADistributionDrill, NNASeriesView, NNAGeoDrillView (after DE gate)</ref>
    <ref type="recharts-diverging-bar">Y4 session log (2026-03-04): stackOffset="sign" + stackId="nna" is the correct Recharts diverging bar pattern</ref>
  </references>

  <gate>
    DE type wiring must be confirmed before starting. Read the DE session log to confirm
    portal DEV commit hash for the type additions.
  </gate>

  <requirements>

    <!-- ================================================================ -->
    <!-- Y6b-FE — Snapshot GEO-NNA City Drill-Down                        -->
    <!-- ================================================================ -->
    <requirement id="Y6b-FE.1">
      File: portal/src/pages/AdvisorIntelligence/tabs/DistributionTab.tsx
      (specifically the Snapshot GEO-NNA histogram component or view)

      Read DistributionTab.tsx in full before making changes. Identify the Snapshot
      GEO-NNA rendering path and how states are currently shown as bars.

      Current behavior: Snapshot GEO-NNA shows a distribution histogram for all states.
      New behavior: clicking a state bar (or segment) loads the city-level distribution
      histogram for that state. A breadcrumb or Back button returns to state level.

      Data source: the `drill` key on the nna.geo distribution output in header_metrics.json.
        drill[stateKey].by_city[cityKey] = NNADistributionStats

      State to add:
        geoNnaSelectedState: string | null  (null = top-level state histogram)

      When a state is selected:
        - Render the city-level histogram using drill[geoNnaSelectedState].by_city
        - Each city is one bar in the histogram
        - Show breadcrumb: "All States / {StateName}" with click-back to null state
        - Apply the same -1k/1k filter (Y6 fix) and footnote to city-level too
        - Apply the same outflow quartile ranking (Y6c fix — city outflows ranked by abs magnitude)

      Guard: if drill key absent or state has no city data, show a "Drill-down data
      unavailable for this state" message and a Back button to return to state level.
    </requirement>

    <!-- ================================================================ -->
    <!-- Y6d-FE — Snapshot ADV-NNA Relationship Drill-Down                -->
    <!-- ================================================================ -->
    <requirement id="Y6d-FE.1">
      Same pattern as Y6b-FE but for Snapshot ADV-NNA.

      Data source: the `drill` key on the nna.adv distribution output.
        drill[architectKey].by_relationship[relKey] = NNADistributionStats

      State to add:
        advNnaSelectedArch: string | null

      When an architect is selected:
        - Render the relationship-level histogram from drill[advNnaSelectedArch].by_relationship
        - Breadcrumb: "All Architects / {ArchitectName}"
        - Same -1k/1k filter + footnote + outflow quartile ranking
        - Guard for missing drill data

      The interaction model is identical to Y6b-FE — just a different data dimension
      (architects → relationships vs states → cities).
    </requirement>

    <!-- ================================================================ -->
    <!-- Y9-FE — Continuous NNA Diverging Bar at All Drill Levels         -->
    <!-- ================================================================ -->
    <requirement id="Y9-FE.1">
      The Continuous GEO-NNA and Continuous ADV-NNA views currently render a line or
      area chart for the NNA timeseries. Y9-FE replaces these with a diverging bar chart
      at every drill level.

      Recharts pattern (confirmed working from Y4 implementation):
        &lt;ComposedChart&gt; with stackOffset="sign"
        &lt;Bar stackId="nna" dataKey="{category}_inflow" /&gt;   (positive, extends up)
        &lt;Bar stackId="nna" dataKey="{category}_outflow_neg" /&gt; (negative, extends down)
      Where outflow_neg = -(outflow value), computed client-side before passing to chart.

      Data sources (from timeseries_chart.json, typed by DE):
        Top-level GEO view (state): nna_geo — use {state} for nna, {state}_inflow, {state}_outflow
        GEO drill (city): nna_geo_drill[stateKey] — use {city} for nna, {city}_inflow, {city}_outflow
        Top-level ADV view (architect): nna_adv — use {arch} for nna, {arch}_inflow, {arch}_outflow
        ADV drill (relationship/client): existing adv_drill — relationship grain
    </requirement>

    <requirement id="Y9-FE.2">
      Relationship-level exception (ADV drill only):
        At the individual relationship grain, do NOT show inflow/outflow decomposition.
        Instead, render a single bar per period:
          - Green if nna_net is positive for that period
          - Pink (destructive color) if nna_net is negative for that period
        No diverging bar. No stacking. One solid-color bar per period.

      This simplification applies only when drilled to the ADV relationship level.
      All other levels (GEO state, GEO city, ADV architect) use the full diverging bar.
    </requirement>

    <requirement id="Y9-FE.3">
      The interval toggle (Month/Quarter/Year from Y8) does NOT change the granularity
      of the continuous NNA chart. The continuous chart always shows daily-granularity
      data points (the existing behavior). The diverging bar uses the raw data as-is,
      one bar per data point (date).

      If the data is daily and produces too many bars to be readable, RD may choose to
      bucket to the current display window's natural period (e.g., show one bar per week
      or month depending on the date range selected). This is a UX judgment call — use
      the same date windowing already in DistributionTab for the continuous view.
    </requirement>

  </requirements>

  <acceptance_criteria>
    <criterion id="1">Snapshot GEO-NNA: clicking a state loads city-level histogram. Breadcrumb returns to state.</criterion>
    <criterion id="2">Snapshot ADV-NNA: clicking an architect loads relationship-level histogram. Breadcrumb returns to architect.</criterion>
    <criterion id="3">Both drill histograms apply -1k/1k filter + footnote + outflow quartile ranking.</criterion>
    <criterion id="4">Continuous GEO-NNA and ADV-NNA at state/city/architect levels: diverging bar (inflow up, outflow down) using stackOffset="sign" + stackId.</criterion>
    <criterion id="5">Continuous ADV-NNA at relationship level: single green/pink bar per period (no inflow/outflow split).</criterion>
    <criterion id="6">Graceful degradation when drill data absent.</criterion>
    <criterion id="7">tsc clean.</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Do NOT start before DE type wiring portal DEV commit is confirmed.</constraint>
    <constraint>Use stackOffset="sign" + stackId for diverging bars — not side-by-side bars (see Y4 RD session log for the correct Recharts pattern).</constraint>
    <constraint>Do NOT add the -1k/1k filter to non-NNA distributions — only NNA drill views.</constraint>
    <constraint>Do NOT use emojis in any code or log output.</constraint>
    <constraint>Commit with: git commit --author="0.4.2_RD_AdvisorIntelligence &lt;0.4.2_RD_AdvisorIntelligence@opal.agent&gt;" -m "..."</constraint>
  </constraints>

  <deliverables>
    <deliverable type="commit">portal DEV: Y6b-FE snapshot GEO city drill + Y6d-FE snapshot ADV relationship drill + Y9-FE continuous NNA diverging bar</deliverable>
    <deliverable type="document">Session log with portal DEV commit hash</deliverable>
  </deliverables>

</task_order>
```
