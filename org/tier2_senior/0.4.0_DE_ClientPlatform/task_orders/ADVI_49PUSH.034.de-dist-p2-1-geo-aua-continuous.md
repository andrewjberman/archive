<task_order>
  <metadata>
    <id>1.0.0_SA_CTO-2026-04-09-49push-034-de</id>
    <issued_by>1.0.0_SA_CTO</issued_by>
    <issued_to>0.4.0_DE_ClientPlatform~D</issued_to>
    <date>2026-04-09</date>
    <status>complete -- fix_1/fix_2/fix_4 DONE (33fef24), fix_3 city drill DONE (2e94a2c), fix_5 new_clients_by_period DONE (e0e9780). Validation pending AE gold run landing.</status>
    <project_code>ADVI_49PUSH</project_code>
    <wave>8</wave>
    <phase>Distribution P2-1</phase>
    <mcp_identity>Register with MCP as "0.4.0_DE_ClientPlatform" before starting.</mcp_identity>
  </metadata>

  <objective>
    Distribution tab P2-1: Fix Continuous-GEO-AUA view. Four issues:
    1. Remove the local granularity toggle -- use parent granularity prop throughout
    2. Fix the Search UI -- opaque dropdown, connected to state drill navigation
    3. Wire city-level drilldown (Top 9 + Other, same as P1-1)
    4. Add New Clients box (blocked on DS .033)
    Also establish the universal "Other is never clickable" rule for the whole tab.
  </objective>

  <context>
    File: portal/src/pages/AdvisorIntelligence/tabs/DistributionTab.tsx
    The AUA continuous view is ContinuousAuaStackedView (starts ~line 1088).
    The NNA continuous view is ContinuousNnaDivergingView (starts ~line 541).

    Current state:
    - auaInterval local state (line 1090): ['monthly'|'quarterly'|'annually'] with toggle UI
      at line 1410. This duplicates the parent granularity prop passed via props.
    - Search: implemented (lines 1318-1348) but dropdown has no background/z-index,
      renders transparent over the state list. Clicking a state calls setDrillParent(k)
      which may or may not correctly trigger the city drill.
    - City drill: geoDrillLevel/selectedStateKey exist in parent state but the continuous
      AUA view uses its own drillParent local state -- unclear if city drill (level 2)
      is fully wired.
    - Other not clickable: partial (showArrow logic exists but not explicit for "Other").
  </context>

  <fix_1 label="Remove local granularity toggle -- use parent prop">
    <description>
      In ContinuousAuaStackedView:
      1. Remove auaInterval state (line 1090) and its setter.
      2. Remove the interval toggle UI block (lines 1410-1420).
      3. Replace all references to auaInterval with the granularity prop passed from parent.
         The component already receives granularity as a prop (line 1530 type definition).
         Verify it is being passed at the call site; if not, add it.
      4. The chart will now reflect whatever granularity the user selected in Assets Overview.
         No separate toggle in the Distribution tab.

      Apply the same fix to ContinuousNnaDivergingView if it has its own interval state.
      The goal: ONE granularity control for the entire ADVI page, living in Assets Overview.
    </description>
  </fix_1>

  <fix_2 label="Fix Search dropdown -- opaque, z-indexed, connected">
    <description>
      The search dropdown (lines 1336-1358) renders with a transparent background,
      showing the state list through it. Fix:

      1. Add explicit background to the dropdown container:
           className="absolute ... bg-[hsl(var(--card))] border border-white/20
                      shadow-xl z-50 rounded-lg overflow-hidden"
         Key properties: bg-[hsl(var(--card))] (matches the card/panel background),
         z-50 (renders above the chart), shadow-xl (visual separation).

      2. Each result row should have hover state:
           className="px-3 py-2 hover:bg-white/10 cursor-pointer text-sm text-white/80"

      3. Clicking a search result must drill into that state:
         - Call setDrillParent(k) (already done at line 1348) AND
         - Set selectedStateKey (parent state) so the breadcrumb and drill state are in sync.
         - Check: does setDrillParent also update the parent's selectedStateKey?
           If not, add onDrillChange(k) callback (same pattern as line 359-367 in parent).
         - After selection: clear the search input (setCategorySearch('') -- already done).

      4. Close the dropdown when user clicks outside: add an onBlur handler or a click-outside
         listener on the search input's container. The simplest approach: wrap in a relative
         container and add a transparent overlay div that clears the search on click.
    </description>
  </fix_2>

  <fix_3 label="State click → city-level drilldown (Top 9 + Other)">
    <description>
      Clicking a state in the AUA continuous stacked chart (or selecting via Search)
      should drill to city-level, showing that state's AUA broken down by city (Top 9 + Other).

      Current: drillParent local state controls the view, switching from stacked-all-states
      to stacked-one-state's-categories. This is Level 1 (state drill).

      Level 2 (city drill) requires geo_drill[stateKey] from the platinum data.
      CumulativeChartView for a state's cities is available in chartData?.geo_drill?.[stateKey].

      When a state is selected (drillParent = stateKey):
        - Render that state's city breakdown from geo_drill[stateKey]
        - Apply enforceTop9Other (from DE .029) to city segments
        - Cities are displayed the same way states are at Level 0
        - Clicking a city = Level 2: show a single city's AUA series (no further drill)
        - Breadcrumb: "All States > {State Name}" (Level 1) or
                      "All States > {State} > {City}" (Level 2)

      "Other" segment at any level: NEVER clickable. See fix_4.
    </description>
  </fix_3>

  <fix_4 label="Universal rule: Other is never clickable">
    <description>
      Throughout the ENTIRE Distribution tab (all 8 views, P1 and P2, GEO and ADV),
      segments with key === 'Other' must never be interactive (no click handler,
      no cursor pointer, no hover navigation state).

      Implement as a shared guard in the segment click handler:
        const handleSegmentClick = (key: string) => {
          if (key === 'Other') return   // never drillable
          // ... normal drill logic
        }

      Also: "Other" segments should have a visual distinction that signals
      non-interactivity -- use cursor-default and remove the hover arrow/indicator
      that appears on drillable segments. This applies to both the radial/donut
      segments in snapshot views and the chart bars/areas in continuous views.

      This guard should be applied once in a shared location, not duplicated per view.
    </description>
  </fix_4>

  <fix_5 label="New Clients box (blocked on DS .033)">
    <description>
      Add a "New Clients" metric box alongside the existing AUA metric boxes.
      Position: same row as the existing Total AUA / ValueSincePeriodStart / GrowthRate boxes.

      Content:
        Label: "New Clients"
        Value: sum of new_clients_by_period[granularity] counts within the active time window
        Sub-line: period label (e.g. "YTD" or "Q1 '26")

      Data source: chartData?.new_clients_by_period?.[granularity] (DS .033 issue_1).
      If the field is not yet in the data (pre-.033), render the box with "--" placeholder.

      Style: match the existing metric boxes exactly (same border, background, text sizing).
      Do not introduce a new visual style for this box.
    </description>
  </fix_5>

  <acceptance_criteria>
    1. No internal granularity toggle visible in P2-1 -- chart responds to Assets Overview selection
    2. Search dropdown is opaque, z-indexed above chart, styled consistently
    3. Clicking a search result drills into the state (breadcrumb updates)
    4. State click → city breakdown (Top 9 + Other), city click → single city series
    5. "Other" is visually non-interactive and never triggers a drill at any level
    6. New Clients box present (value or "--" placeholder until DS .033 ships)
    7. Build clean, no TypeScript errors
    8. enforceTop9Other and handleSegmentClick("Other") guard are shared utilities
  </acceptance_criteria>


  <compiler_tools>
    comp-transform trace DistributionTab
      -- Run BEFORE any code changes. Shows the full data flow for ContinuousAuaStackedView:
         getPlatinumCumulativeChart() → chartData → useMemo chains → JSX.
         Reveals exactly where auaInterval is referenced so fix_1 (toggle removal)
         can be surgical rather than a search-and-replace.

    comp-cache collisions
      -- Run after adding new_clients_by_period support. The granularity-keyed
         cache entries for the continuous view could collide with snapshot view keys
         if the React Query key isn't namespaced properly.

    comp-transform schema-check DistributionTab
      -- Run after all fixes. Confirms New Clients box and city drill segments are
         wired to rendered JSX and no UNUSED fields remain in the cumulative chart type.
  </compiler_tools>

</task_order>
