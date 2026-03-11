<task_order>
  <metadata>
    <id>1.0.0_SA_CTO-2026-03-09-F3b</id>
    <issued_by>1.0.0_SA_CTO</issued_by>
    <issued_to>0.4.0_DE_ClientPlatform</issued_to>
    <date>2026-03-09</date>
    <status>complete</status>
  </metadata>

  <objective>
    The continuous NNA view in Segment Analytics (ContinuousNnaDivergingView) is missing
    drill parity with AUA and CLA continuous views. Andrew expects the same drill behavior
    across all three metrics in both snapshot and continuous modes: click a state or advisor
    to drill in, then click again to see cities or relationships.

    Specifically, ContinuousNnaDivergingView (line 429-668) currently:
    - GEO: drills state level only (via nna_geo_drill). No second-level city drill.
    - ADV: no drill at all (canDrill at line 526 is hardcoded to GEO-only).

    By contrast, ClaContinuousView (line 1335+) has full two-level drill:
    - GEO: state -> city (via geo_drill + geo_city_drill)
    - ADV: architect -> client (via adv_drill)

    And ContinuousChartView (line 922+, used by AUA) has one-level drill:
    - GEO: state -> cities (via geo_drill)
    - ADV: architect -> clients (via adv_drill)

    Bring ContinuousNnaDivergingView up to the same drill level as the other views.
  </objective>

  <scope>
    <pages>
      <page>portal/src/pages/AdvisorIntelligence/tabs/DistributionTab.tsx</page>
    </pages>
    <files>
      <file action="modify">portal/src/pages/AdvisorIntelligence/tabs/DistributionTab.tsx</file>
    </files>
  </scope>

  <context>
    Data paths in timeseries_chart.json (CumulativeChartResponse):
    - nna_geo: NNA by state (top level, currently consumed)
    - nna_geo_drill: NNA by city within a state (currently consumed for GEO L1 drill)
    - nna_adv: NNA by architect (top level, currently consumed but NOT drillable)
    - nna_adv_drill: may or may not exist -- check the data. If it does, wire it.

    The existing pattern in CLA continuous (ClaContinuousView) is the reference
    implementation for two-level drill:
    - L1: drillKey selects a state or architect
    - L2 (GEO): cityKey selects a city within that state
    - L2 (ADV): terminal -- shows client-level series
    - activeView resolves the correct CumulativeChartView based on drill state
    - drillList provides the clickable legend items for the current level

    ContinuousNnaDivergingView uses a different chart type (ComposedChart with
    diverging bars + net NNA line) but the drill state management and legend
    interaction should follow the same pattern.
  </context>

  <requirements>
    <requirement id="1">ADV drill: enable architect-level drill in
      ContinuousNnaDivergingView. Clicking an architect in the legend should drill
      into that architect's NNA series (showing their clients or sub-series). Check
      if nna_adv_drill exists in the data. If it does, consume it. If not, at minimum
      show the filtered single-architect NNA series.</requirement>
    <requirement id="2">GEO second-level drill: after drilling into a state, the legend
      should show cities within that state. Clicking a city should drill further or show
      the city-level NNA series. Check if the nna_geo_drill structure supports a second
      level (city within state). The snapshot view reads by_city from this path
      (nnaDrillData[state].by_city) -- the continuous view should do the same if the
      timeseries equivalent exists.</requirement>
    <requirement id="3">Breadcrumb navigation: add proper breadcrumb for the drill
      hierarchy (same pattern as CLA continuous -- "All States / StateName / CityName"
      with back navigation at each level).</requirement>
    <requirement id="4">Graceful degradation: if drill data does not exist at a given
      level, do not offer the click affordance. No errors, no dead-end clicks.</requirement>
    <requirement id="5">Verify the same drill paths work for both GEO and ADV cohort
      toggles. The cohort toggle should reset drill state (already handled by parent
      component).</requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">NNA continuous GEO: click state legend item -> shows city-level
      NNA diverging bars (or gracefully indicates no city data).</criterion>
    <criterion id="2">NNA continuous ADV: click architect legend item -> shows
      drilled NNA diverging bars for that architect.</criterion>
    <criterion id="3">Breadcrumb back navigation works at each drill level.</criterion>
    <criterion id="4">No errors on any drill path. No regression on AUA or CLA
      continuous views.</criterion>
    <criterion id="5">Portal DEV commit with --author flag. TypeScript clean.</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Use ClaContinuousView (line 1335+) as the reference implementation
      for drill state management. Do not invent a new pattern.</constraint>
    <constraint>Do not modify the diverging bar chart rendering logic itself -- only
      the drill state, data resolution, and legend/breadcrumb interaction.</constraint>
    <constraint>If the timeseries data does not support a particular drill level
      (e.g., nna_adv_drill doesn't exist), degrade gracefully rather than erroring.
      Check the actual JSON before assuming what exists.</constraint>
  </constraints>

  <dependencies>
    <dependency agent="0.4.0_DE_ClientPlatform" task="ADVI_49FNV3.F3-fix" status="complete"/>
  </dependencies>

  <deliverables>
    <deliverable type="commit">Portal DEV commit adding continuous NNA drill parity.</deliverable>
  </deliverables>

  <references>
    <ref type="prd">docs/architecture/ADVISOR_INTELLIGENCE_49FN_V3_PRD.md (F3 section)</ref>
    <ref type="source">portal/src/pages/AdvisorIntelligence/tabs/DistributionTab.tsx</ref>
    <ref type="pattern">ClaContinuousView (line 1335+) -- reference implementation for two-level drill</ref>
    <ref type="pattern">ContinuousChartView (line 922+) -- AUA one-level drill</ref>
    <ref type="target">ContinuousNnaDivergingView (line 429-668) -- the view to modify</ref>
  </references>
</task_order>
