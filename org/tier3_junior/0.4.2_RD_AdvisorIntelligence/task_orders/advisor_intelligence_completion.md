# Task Order: AdvisorIntelligence Portal Completion — 0.4.2_RD_AdvisorIntelligence

```xml
<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-03-03-rd-advisor-intelligence-completion</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.2_RD_AdvisorIntelligence</issued_to>
    <date>2026-03-03</date>
    <status>pending</status>
  </metadata>

  <objective>
    Implement all portal-layer changes for AdvisorIntelligence completion. Covers
    7 streams: Distribution tab continuous and snapshot views (C1-C4), Advisors tab
    UI refactor (H, I, 4C stacked bar), and Books tab implementation (G — blocked).
    Streams C1, C3, H, and I have no data dependencies and can start immediately.
    Streams C2 and C4 are blocked by DT deploying the updated publisher (Stream B1).
  </objective>

  <references>
    <ref>docs/architecture/ADVISOR_INTELLIGENCE_COMPLETION.md</ref>
    <ref>portal/src/pages/AdvisorIntelligence/</ref>
    <ref>portal/src/api/endpoints/advisor-intelligence.ts</ref>
    <ref>portal/src/pages/AdvisorIntelligence/types.ts</ref>
    <ref>portal/src/pages/AdvisorIntelligence/tabs/DistributionTab.tsx</ref>
    <ref>portal/src/pages/AdvisorIntelligence/tabs/AdvisorsTab.tsx</ref>
    <ref>portal/src/pages/AdvisorIntelligence/tabs/ClientsTab.tsx</ref>
  </references>

  <scope>
    <pages>
      <page>portal/src/pages/AdvisorIntelligence/</page>
    </pages>
    <files>
      <!-- Distribution tab -->
      <file action="modify">portal/src/pages/AdvisorIntelligence/tabs/DistributionTab.tsx</file>
      <file action="modify">portal/src/pages/AdvisorIntelligence/types.ts</file>
      <!-- Advisors tab -->
      <file action="modify">portal/src/pages/AdvisorIntelligence/tabs/AdvisorsTab.tsx</file>
      <!-- Books tab (blocked) -->
      <!-- portal/src/pages/AdvisorIntelligence/tabs/ClientsTab.tsx and related — pending thread -->
    </files>
  </scope>

  <requirements>

    <!-- ================================================================ -->
    <!-- STREAM C1 — Continuous NNA GEO: search + city drill-down         -->
    <!-- UNBLOCKED — geo_drill data already in timeseries_chart.json      -->
    <!-- ================================================================ -->
    <requirement id="C1.1">
      Update the GEO continuous NNA view in DistributionTab to render the top-8 states
      as separate series in the cumulative NNA chart. Use the same chart type, axis format,
      color scheme, and window toggle as the Assets Overview header panel's cumulative NNA chart.
      Data source: timeseries_chart.json geo view (per-state categories).
    </requirement>
    <requirement id="C1.2">
      Add a search input in the left panel controls that filters across ALL available states
      (not just top-8). States outside top-8 are accessible via search.
    </requirement>
    <requirement id="C1.3">
      Implement click-to-drill interaction:
        - Clicking a state in the chart legend OR selecting from search drills into that state
        - Chart re-renders showing per-city series for that state
          (sourced from timeseries_chart.json geo_drill[stateKey])
        - A breadcrumb/back control returns to the state-level view
      The drill state is local UI state — no API call needed (data already in the JSON).
    </requirement>
    <requirement id="C1.4">
      The back/breadcrumb must clearly display the current drill level:
        "All States" (default) or "Texas" (drilled) etc.
      Consistent with the existing GEO/ADV cohort toggle pattern already in the page.
    </requirement>

    <!-- ================================================================ -->
    <!-- STREAM C2 — Continuous NNA ADV: search + client drill-down       -->
    <!-- BLOCKED: requires Stream B1 (DT deploys adv_drill)               -->
    <!-- ================================================================ -->
    <requirement id="C2.1">
      GATE: Do not begin C2 until DT confirms adv_drill is deployed and present in
      timeseries_chart.json S3 output.
    </requirement>
    <requirement id="C2.2">
      Implement ADV continuous NNA view identically to GEO (C1), but for architects:
        - Top architects as separate series
        - Search input for architects not in top list
        - Click architect → drill to client/relationship level
          (sourced from adv_drill[architectKey] in timeseries_chart.json)
        - Breadcrumb returns to architect-level view
        - No drill-down past relationship level (client is terminal grain for ADV)
    </requirement>
    <requirement id="C2.3">
      The ADV drill interaction uses the same component and pattern as GEO drill (C1).
      Factor out the drill logic into a shared hook or utility if C1 and C2 share enough
      structure — but only if the abstraction is clean. No premature abstraction.
    </requirement>

    <!-- ================================================================ -->
    <!-- STREAM C3 — Snapshot CLA: simplified two-color visualization     -->
    <!-- UNBLOCKED — data already in header_metrics.json                  -->
    <!-- ================================================================ -->
    <requirement id="C3.1">
      Replace the current CLA snapshot rendering (which incorrectly uses a flows/NNA chart)
      with a clean two-color proportional display:
        - Green = NMNC (New Client AUA percentage of total AUA)
        - Blue = NMEC (Existing Client AUA percentage of total AUA)
        - Preferred format: horizontal stacked bar or split donut — clean, no axes,
          just the two proportions with AUA dollar amounts labeled
      NO inflow/outflow data. NO NNA vocabulary. NO blue/red flows visual language.
    </requirement>
    <requirement id="C3.2">
      The visualization must support the time machine period selector (q1/q2/q3 periods)
      to show how the new-client percentage has shifted over time.
      Data source: header_metrics.json views.aua CLA structure
        (cla.current.geo.totals.nmnc_nna and related fields).
      Confirm field availability with DS if uncertain which fields carry NMNC/NMEC AUA.
    </requirement>
    <requirement id="C3.3">
      Label each segment clearly: "New Clients (NMNC)" in green, "Existing Clients (NMEC)"
      in blue. Include the AUA dollar amount and percentage for each segment.
    </requirement>

    <!-- ================================================================ -->
    <!-- STREAM C4 — Continuous CLA: new time series stacked area chart   -->
    <!-- BLOCKED: requires Stream B1 (DT deploys cla_timeseries)          -->
    <!-- ================================================================ -->
    <requirement id="C4.1">
      GATE: Do not begin C4 until DT confirms cla_timeseries is deployed and present in
      timeseries_chart.json S3 output (cla.total field).
    </requirement>
    <requirement id="C4.2">
      Implement the continuous CLA view as a stacked area chart:
        - Y-axis = dollar AUM (absolute, not percentage)
        - Two stacked areas: NMNC AUM (green, bottom) and NMEC AUM (blue, top)
        - Total height at each date = total firm AUM
        - Date range = same as other continuous views (window toggle applies)
      Data source: timeseries_chart.json cla.total (firm-wide),
        cla.geo / cla.geo_drill (GEO grain), cla.adv (ADV grain — architect is terminal).
    </requirement>
    <requirement id="C4.3">
      Add search input and drill-down behavior consistent with C1/C2:
        - GEO view: search states, click to drill to cities
        - ADV view: search architects (no client drill-down for CLA)
      Same breadcrumb/back pattern.
    </requirement>

    <!-- ================================================================ -->
    <!-- STREAM H — Advisors tab: Portal Primitives Refactor              -->
    <!-- UNBLOCKED                                                         -->
    <!-- ================================================================ -->
    <requirement id="H.1">
      Refactor all sections in AdvisorsTab.tsx to use portal panel primitives:
        Panel, PanelHeader, PanelContent, SmartPanelFooter from @/ui/components/panels
      Sections affected: Top Performers panel, Rolling Flows panel, Leaderboard panel.
      The visual output should be identical to the current layout after refactor —
      this is purely a structural change to match portal conventions.
    </requirement>
    <requirement id="H.2">
      Run bunx tsc -b after refactor to confirm no type errors introduced.
      DE reviews before DT pushes.
    </requirement>

    <!-- ================================================================ -->
    <!-- STREAM I — Advisors tab: Top Performers visual identity           -->
    <!-- UNBLOCKED                                                         -->
    <!-- ================================================================ -->
    <requirement id="I.1">
      Redesign the Top Performers (Top 3 highlights) panel to communicate rank and
      achievement more clearly:
        - Rank (1st / 2nd / 3rd) must be visually prominent
        - Advisor name prominent
        - Key metric (NNA for the active period) immediately readable
        - Use trophy/medal iconography or rank-badge treatment using Lucide icons
          already in the codebase (confirm which Lucide icons are available before choosing)
    </requirement>
    <requirement id="I.2">
      The redesign must work for all period toggles (QTD/YTD/1Y/3Y/Max).
      When the active period changes, Top Performers rankings update accordingly.
    </requirement>
    <requirement id="I.3">
      DE reviews the visual design before DT pushes to DEV.
    </requirement>

    <!-- ================================================================ -->
    <!-- STREAM 4C — Advisors tab: New Rolling Flows visualization        -->
    <!-- BLOCKED: requires Stream B2 (DT deploys script 10 stacked bar)  -->
    <!-- ================================================================ -->
    <requirement id="4C.1">
      GATE: Do not begin 4C until DT confirms stacked_bar data is in
      advisor_rolling_flows.json S3 output (from script 10 Stream B2 deploy).
    </requirement>
    <requirement id="4C.2">
      Implement PRIMARY VIEW — Stacked Bar Chart (default view):
        - X-axis: one bar per architect (or implementor, per toggle)
        - Bars: Inflows (positive, teal or similar), Outflows (inverted downward or negative segment), NNA net (implied)
        - Sorted lowest to highest by NNA (highest performers visually rightmost)
        - Period toggle: QTD / YTD / 1Y / 3Y / Max
        - Architects / Implementors toggle at top (controls both primary and secondary views)
      Data source: advisor_rolling_flows.json stacked_bar.architects / stacked_bar.implementors
    </requirement>
    <requirement id="4C.3">
      Implement SECONDARY VIEW — 1-Year Rolling Line Chart:
        - X-axis: dates over the selected period window
        - Y-axis: 1-year rolling NNA value per advisor
        - One line per advisor (top performers by default, all accessible via search/toggle)
        - Period toggle controls X-AXIS WINDOW (how far back dates go), NOT the rolling window
        - Rolling window is FIXED at 1 year (full year trailing from each date point)
        - Same Architects/Implementors toggle as primary view
      Data source: advisor_rolling_flows.json rolling_1y.architects / rolling_1y.implementors
    </requirement>
    <requirement id="4C.4">
      View toggle (Primary / Secondary) must be clear and accessible.
      Recommended: a segmented control or tab above the chart area.
      The period toggle and Architects/Implementors toggle must remain visible in both views.
    </requirement>

    <!-- ================================================================ -->
    <!-- STREAM G — Books tab implementation                               -->
    <!-- BLOCKED: requires Stream D thread receipt + Stream F deploy      -->
    <!-- ================================================================ -->
    <requirement id="G.1">
      BLOCKED: Do not begin Books tab implementation until both:
        (a) Stream D (Books design thread) receipt is available at:
            org/tier3_junior/0.4.2_RD_AdvisorIntelligence/threads/
        (b) Stream F (DT deploys advisor-publisher with L4 fields) is confirmed complete.
      The thread receipt defines the visual design brief for L2/L3/L4. Do not design
      the Books tab independently — the thread outcome is the specification.
    </requirement>
    <requirement id="G.2">
      When gates are met: implement Books tab per the design brief at
        docs/architecture/advisor_intelligence/books_tab_design_brief.md
      Scope: L2 (advisor book), L3 (relationship view), L4 (account + holdings + tax).
      Access gating: admin sees advisor selector (all advisors), advisor sees only own book.
      Use portal panel primitives throughout (consistent with Stream H refactor).
    </requirement>
    <requirement id="G.3">
      DE coordinates the Books tab implementation — RD implements visuals,
      DE handles API wiring and auth gating logic.
      Do not wire auth gating until 0.7.0_AE_CloudOps has confirmed opal-users-v2 mapping.
    </requirement>

  </requirements>

  <acceptance_criteria>
    <criterion id="1">C1: GEO continuous NNA shows top-8 states as series; search filters all states; click drills to cities; breadcrumb returns to state view.</criterion>
    <criterion id="2">C2: ADV continuous NNA identical to GEO but for architects and clients (post-B1 deploy).</criterion>
    <criterion id="3">C3: CLA snapshot is a clean two-color NMNC/NMEC split; no flows/NNA vocabulary; time machine periods work.</criterion>
    <criterion id="4">C4: CLA continuous is a stacked area chart with NMNC (green) and NMEC (blue) AUM over time at all grains (post-B1).</criterion>
    <criterion id="5">H: All Advisors tab sections use portal panel primitives; bunx tsc -b passes; no visual regression.</criterion>
    <criterion id="6">I: Top Performers shows clear rank (1/2/3), advisor name, and NNA with medal/badge treatment; works across all periods.</criterion>
    <criterion id="7">4C: Stacked bar primary view + rolling line secondary view implemented with period toggle and Architects/Implementors toggle.</criterion>
    <criterion id="8">G: Books tab L2/L3/L4 implemented per design brief; access gating functional (post-thread and post-F).</criterion>
    <criterion id="9">bunx tsc -b passes after each stream's changes.</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Immediate start items (no blocks): C1, C3, H, I. Begin these in your first activation session.</constraint>
    <constraint>C2 and C4 blocked by DT Stream B1 deploy — check DT session log for deploy confirmation before starting.</constraint>
    <constraint>4C blocked by DT Stream B2 deploy — same pattern.</constraint>
    <constraint>G blocked by Stream D thread completion AND Stream F deploy.</constraint>
    <constraint>Do NOT use emojis in any component, comment, or log output. Plain ASCII only.</constraint>
    <constraint>DE (0.4.0_DE_ClientPlatform) must review C3 NMNC/NMEC label accuracy and Top Performers (I) before DT pushes to DEV.</constraint>
    <constraint>Commit with: git commit --author="0.4.2_RD_AdvisorIntelligence &lt;0.4.2_RD_AdvisorIntelligence@opal.agent&gt;" -m "0.4.2_RD_AdvisorIntelligence: AdvisorIntelligence/{Tab} -- description"</constraint>
    <constraint>NOTE: You have 3 pending task orders (page_inventory, distribution_nomenclature_fix, continuous_view_max_window_clients_fix). Complete those before starting C1 if they conflict with the Distribution tab changes. Confirm with DE if there is overlap.</constraint>
    <constraint>NOTE: You have no prior session logs. Write a session log after your first activation and first work session. The COO needs it before scheduling the Books thread (Stream D).</constraint>
  </constraints>

  <dependencies>
    <dependency agent="0.4.0_DT_ClientPlatform" task="advisor_intelligence_completion" status="pending" note="C2, C4 blocked by B1; 4C blocked by B2"/>
    <dependency agent="2.0.0_SA_COO" task="Stream-D-thread" status="pending" note="G blocked by thread completion"/>
    <dependency agent="0.4.0_DT_ClientPlatform" task="advisor_intelligence_completion" status="pending" note="G blocked by F deploy"/>
    <dependency agent="0.4.0_DS_ClientPlatform" task="advisor_intelligence_completion" status="pending" note="C3 field confirmation — DS to confirm NMNC/NMEC field names in header_metrics.json"/>
  </dependencies>

  <deliverables>
    <deliverable type="commit">DistributionTab.tsx: GEO continuous with search + drill (C1)</deliverable>
    <deliverable type="commit">DistributionTab.tsx: ADV continuous with search + drill (C2, post-B1)</deliverable>
    <deliverable type="commit">DistributionTab.tsx: CLA snapshot two-color (C3)</deliverable>
    <deliverable type="commit">DistributionTab.tsx: CLA continuous stacked area (C4, post-B1)</deliverable>
    <deliverable type="commit">AdvisorsTab.tsx: portal primitives refactor (H)</deliverable>
    <deliverable type="commit">AdvisorsTab.tsx: Top Performers visual redesign (I)</deliverable>
    <deliverable type="commit">AdvisorsTab.tsx: stacked bar primary + rolling line secondary (4C, post-B2)</deliverable>
    <deliverable type="commit">ClientsTab.tsx and related: Books tab L2/L3/L4 (G, post-thread + post-F)</deliverable>
  </deliverables>
</task_order>
```
