<task_order>
  <metadata>
    <id>1.0.0_SA_CTO-2026-04-09-49push-036-de</id>
    <issued_by>1.0.0_SA_CTO</issued_by>
    <issued_to>0.4.0_DE_ClientPlatform~B</issued_to>
    <date>2026-04-09</date>
    <status>complete -- ADV views share ContinuousChartView + ContinuousNnaDivergingView (cohort-aware). Advisor search, drill, Other guard, metric boxes all covered by .034/.035 shared components. Level 2 client drill gracefully no-drills if nna_adv_drill Level 2 absent. Data validation blocked on AE re-run.</status>
    <project_code>ADVI_49PUSH</project_code>
    <wave>8</wave>
    <phase>Distribution P2-3 + P2-4</phase>
    <mcp_identity>Register with MCP as "0.4.0_DE_ClientPlatform" before starting.</mcp_identity>
  </metadata>

  <objective>
    Distribution tab P2-3 (Continuous-ADV-AUA) and P2-4 (Continuous-ADV-NNA).
    These are the advisor-cohort mirrors of P2-1 and P2-2. Apply the same patterns
    established in .034 and .035, replacing geographic hierarchy (state/city) with
    advisor hierarchy (advisor/client). All rules carry over directly.
  </objective>

  <context>
    File: portal/src/pages/AdvisorIntelligence/tabs/DistributionTab.tsx

    P2-3 is the ADV (advisor) version of P2-1 (GEO-AUA):
      - Stacked area/bar chart of AUA over time, broken by advisor (not state)
      - Drill: firm → advisor → client (mirrors state → city)
      - Metric boxes: Total AUA (firm headline), ValueSincePeriodStart, GrowthRate → New Clients
      - Total AUA center = firm headline (same rule as P1-3, never sum of advisor AUAs)

    P2-4 is the ADV version of P2-2 (GEO-NNA):
      - Diverging bar NNA over time, broken by advisor
      - Drill: firm → advisor → client
      - Metric boxes: Total NNA, Inflows, Outflows, New Clients

    The cohort toggle (GEO/ADV) already switches the chart data source between geo/adv
    and nna_geo/nna_adv. Most of the structural work from .034/.035 will already
    apply to P2-3/P2-4 by virtue of the shared component architecture.
    This TO covers ADV-specific differences only.
  </context>

  <adv_specific_differences>

    <diff id="1" label="Advisor search instead of state search">
      The search input placeholder is already cohort-aware: line 1325 reads
      'Search all states...' for GEO and 'Search all architects...' for ADV.
      After .034 fix_2 extracts a shared Search component, verify it works for ADV too:
        - Searches advisor display names (not state names)
        - Clicking a search result drills into that advisor (setDrillParent(advisorKey))
        - Same opaque dropdown styling, same Other-not-clickable guard
    </diff>

    <diff id="2" label="Advisor drill Level 1 → client drill Level 2">
      The ADV drill mirrors the GEO drill:
        Level 0: firm AUA/NNA stacked by top-9 advisors + Other
        Level 1: advisor selected → that advisor's AUA/NNA series over time
          Data: adv_drill[advisorKey] for AUA (DS .033 confirms/adds this)
                nna_adv_drill[advisorKey] for NNA (DS .033 issue_3)
        Level 2: client selected → that client's AUA/NNA series (if DS .033 provides it)
          If Level 2 data is not available (DS .033 deferred it), skip Level 2 in the UI
          and note as a future enhancement. Do not crash or show an error if the drill
          data is absent -- gracefully show Level 1 without a further drill option.

      Client entries at Level 1/2: display pseudonymized names from platinum data (.032 rule).
      "Other" at any level is not clickable.

      Breadcrumb: "All Advisors > {Advisor Name}" (Level 1)
                  "All Advisors > {Advisor} > {Client}" (Level 2, if available)
    </diff>

    <diff id="3" label="Total AUA box = firm headline (not advisor sum)">
      For P2-3 (ADV-AUA): the Total AUA metric box must show the firm headline AUA,
      identical to P1-3 rule (.030 fix_1). It is NOT the sum of advisor AUAs.
      Source: same as .030 -- firm header_metrics AUA passed as prop from parent.
      Apply the same fix established in .030 to the continuous ADV-AUA metric boxes.
    </diff>

    <diff id="4" label="New Clients box">
      Same as P2-1/P2-2: add New Clients box using chartData?.new_clients_by_period.
      The count is firm-wide regardless of which advisor is drilled into.
      (New clients for a specific advisor's book is a future enhancement, not in scope here.)
    </diff>

    <diff id="5" label="Granularity toggle removal">
      Same as .034 fix_1: if the ADV continuous views have their own local granularity
      state, remove it and use the parent prop. The ADV views share the same
      ContinuousAuaStackedView and ContinuousNnaDivergingView components as GEO views
      (just with different data), so .034 fix_1 likely covers this already.
      Verify that switching the cohort from GEO to ADV does not re-introduce a local toggle.
    </diff>

  </adv_specific_differences>

  <shared_rules_reminder>
    All rules from .034 and .035 apply equally to P2-3 and P2-4:
    - "Other" is never clickable at any drill level
    - Metric boxes use shared ContinuousMetricBox component
    - No internal granularity toggle
    - Client names pseudonymized per .032
    - New Clients box present
    - Search dropdown opaque, z-indexed
  </shared_rules_reminder>

  <acceptance_criteria>
    1. P2-3 ADV-AUA: advisor stacked chart with advisor search, firm→advisor drill,
       Total AUA = firm headline (never advisor sum), New Clients box, no granularity toggle
    2. P2-4 ADV-NNA: advisor NNA chart with search, firm→advisor drill,
       Total NNA / Inflows / Outflows / New Clients boxes, no granularity toggle
    3. Client names pseudonymized at Level 2 (or graceful no-drill if data unavailable)
    4. "Other" not clickable at any level in either ADV view
    5. Breadcrumb navigation works for all available drill levels
    6. Shared components from .034/.035 reused -- no ADV-specific duplicates
    7. Build clean, no TypeScript errors
    8. Visual: verify switching cohort GEO ↔ ADV preserves drill level and search state
       (or resets gracefully -- no crash, no stale drill data from previous cohort)
  </acceptance_criteria>


  <compiler_tools>
    comp-transform trace DistributionTab
      -- Run before starting. The ADV continuous views share components with GEO views.
         The trace shows which code paths are truly shared vs duplicated so the ADV
         fixes from .034/.035 carry over automatically or need separate treatment.

    comp-pii scan DistributionTab
      -- Required gate. Client names appear at Level 2 of the ADV drill.
         Run before shipping to confirm all client display_names are pseudonymized
         and no raw relationship names are accessible in the rendered tree.

    comp-cache collisions
      -- Run after adding advisor drill React Query keys. The advisor key must be
         namespaced to prevent collisions with the firm-level nna_adv cache entry.
  </compiler_tools>

</task_order>
