# Task Order: Yang V2 Phase 1 Visual Fixes — 0.4.2_RD_AdvisorIntelligence

```xml
<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-03-04-ADVI-Y1-Y4-Y6-Y12-phase1-visual</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.2_RD_AdvisorIntelligence</issued_to>
    <date>2026-03-04</date>
    <status>complete</status>
    <priority>HIGH — unblocked, no data dependency, start immediately</priority>
    <streams>Y1, Y4, Y6, Y12</streams>
  </metadata>

  <objective>
    Execute four Phase 1 visual-only changes from the Yang V2 PRD. All use existing data.
    No DS or DT dependency. All are trivial or small effort. Do them in a single session.
  </objective>

  <references>
    <ref type="prd" priority="PRIMARY">docs/architecture/ADVISOR_INTELLIGENCE_YANG_FEEDBACK_V2.md</ref>
    <ref type="prd-v1">docs/architecture/ADVISOR_INTELLIGENCE_COMPLETION.md</ref>
    <ref type="portal-header">portal/src/pages/AdvisorIntelligence/components/PartnerAnalytics.tsx</ref>
    <ref type="portal-advisors">portal/src/pages/AdvisorIntelligence/tabs/AdvisorsTab.tsx</ref>
    <ref type="portal-distribution">portal/src/pages/AdvisorIntelligence/tabs/DistributionTab.tsx</ref>
  </references>

  <requirements>

    <!-- ================================================================ -->
    <!-- Y1 — AUA Stack Order Flip (NMNC on top)                          -->
    <!-- ================================================================ -->
    <requirement id="Y1">
      File: portal/src/pages/AdvisorIntelligence/components/PartnerAnalytics.tsx

      The AUA stacked bar currently renders NMEC (existing clients) on top of NMNC (new clients).
      Yang requires NMNC (new) to render above NMEC (existing).

      Fix: In the BarChart categories array or the Bar component ordering for AUA mode,
      reverse the render order so NMNC renders above NMEC (i.e., NMNC bar is declared
      after NMEC in the JSX if Recharts renders in declaration order, or adjust the
      stackId/data layout so NMNC sits on top of the stack).

      The color mapping is unchanged:
        NMNC = green (--success or CATEGORY_COLORS.NMNC)
        NMEC = blue (CATEGORY_COLORS.NMEC)

      Read PartnerAnalytics.tsx before making the change to confirm the exact Recharts
      stacking pattern in use.

      Effort: Trivial.
    </requirement>

    <!-- ================================================================ -->
    <!-- Y4 — NNA Diverging Bar Alignment + Net Line Centering            -->
    <!-- ================================================================ -->
    <requirement id="Y4.1">
      File: portal/src/pages/AdvisorIntelligence/components/PartnerAnalytics.tsx (NNA mode)

      Bar alignment: Inflow (blue, positive) must extend upward from x-axis; outflow (red,
      negative) must extend downward from x-axis; both bars must share the same horizontal
      x-position per period.

      If the current implementation renders bars side-by-side, fix by ensuring both bars
      use the same stackId value (Recharts will then stack them as diverging bars sharing
      one column per period). Example: both Bar components use stackId="nna". The inflow
      data key is positive; the outflow data key is negative (or use Recharts negative
      bar support). Confirm the current NNA chart structure in PartnerAnalytics.tsx before
      patching.

      Effort: Small.
    </requirement>

    <requirement id="Y4.2">
      Net line anchor point: The yellow net-flow Line's y-value should visually center on
      the bar stack. Per the PRD, compute the display y-value as:
        displayY = (inflow + outflow) / 2
      where inflow is positive and outflow is the negative outflow magnitude (so the midpoint
      of the full bar height). The actual net value (inflow + outflow signed) should still
      appear in the tooltip.

      IMPORTANT: After implementing this, flag to Andrew/Yang for visual confirmation.
      Add a comment in the code: "// Y4: net line anchored at bar midpoint per Yang feedback -- confirm visually"
      The centering formula may need adjustment based on Yang's reaction to the first render.

      Effort: Small.
    </requirement>

    <!-- ================================================================ -->
    <!-- Y6 — Snapshot GEO/ADV NNA: Remove -1k/1k Buckets + Footnote     -->
    <!-- ================================================================ -->
    <requirement id="Y6.1">
      File: portal/src/pages/AdvisorIntelligence/tabs/DistributionTab.tsx
      (or wherever the Snapshot GEO-NNA and Snapshot ADV-NNA histogram views render)

      For BOTH the Snapshot GEO-NNA and Snapshot ADV-NNA histogram views, filter out
      histogram buckets whose range falls entirely within [-1000, 1000].

      Implementation:
        Before passing histogram segment data to the chart, filter out any segment where
        both the range_start and range_end values are within [-1000, 1000]. The exact field
        names depend on the data shape from header_metrics.json — read the current code to
        confirm. If segments have a "bucket label" string (e.g., "-1k-1k" or "0"), match
        by value range, not label string.

      Effort: Trivial.
    </requirement>

    <requirement id="Y6.2">
      After the histogram for BOTH GEO-NNA and ADV-NNA snapshot views, add a footnote
      text element below the chart:

        "Relationships with net flows between -$1,000 and $1,000 are excluded from this distribution."

      Style it as muted/secondary text (use existing muted text className pattern from the
      codebase — whatever DistributionTab.tsx uses for footnotes or caption text).

      Effort: Trivial.
    </requirement>

    <!-- ================================================================ -->
    <!-- Y12 — Drop 1Y Rolling Concept from Advisors Tab                  -->
    <!-- ================================================================ -->
    <requirement id="Y12.1">
      File: portal/src/pages/AdvisorIntelligence/tabs/AdvisorsTab.tsx

      The ADVI-005 4C session (portal DEV 0bceb64) added:
        - flowsView state ('primary' | 'secondary')
        - FLOWS_VIEW_OPTIONS toggle (Stacked / 1Y Rolling) in the Rolling Flows panel header
        - Rolling1YChart secondary view
        - Legacy RollingFlowsChart fallback

      Remove all of this. The Rolling Flows panel should have ONE view only: the stacked
      bar (primary view). Specifically remove:
        - The flowsView state variable and its setter
        - The FLOWS_VIEW_OPTIONS array/constant
        - The view toggle UI in the panel header (keep the period toggle QTD/YTD/1Y/3Y/Max)
        - The Rolling1YChart component and its rendering branch
        - The legacy RollingFlowsChart fallback branch
        - Any imports used exclusively by the removed items

      Keep:
        - The StackedBarChart component and its rendering
        - The stackedBarPeriod state and period toggle (QTD/YTD/1Y/3Y/Max)
        - The Architects/Implementors role toggle
        - All other Advisors tab content (leaderboard, Top Performers)

      The stacked bar is now the sole content of the Rolling Flows panel.

      Effort: Trivial (delete code).
    </requirement>

    <requirement id="Y12.2">
      DS coordination note (do NOT block on this — RD removes the UI, DS removes data separately):
      Add a comment to your session log noting: "rolling_1y key removal from script 10 is DS's
      call — confirm no other consumer before DS drops it. Y12 removes the UI only."
      RD does not need to wait for DS to act on this.
    </requirement>

  </requirements>

  <acceptance_criteria>
    <criterion id="1">AUA stacked bar: NMNC (new clients) renders above NMEC (existing) in all period modes.</criterion>
    <criterion id="2">NNA diverging bar: inflow extends up, outflow extends down, both share the same x-position per period.</criterion>
    <criterion id="3">NNA net line: dot anchored at bar midpoint (inflow + outflow) / 2. Code comment added per Y4.2.</criterion>
    <criterion id="4">Snapshot GEO-NNA and ADV-NNA histograms: no buckets within [-1000, 1000] range.</criterion>
    <criterion id="5">Footnote "Relationships with net flows between -$1,000 and $1,000 are excluded from this distribution." appears below both histograms.</criterion>
    <criterion id="6">Rolling Flows panel: stacked bar only. No 1Y rolling view, no view toggle, no legacy fallback. Period toggle and role toggle remain.</criterion>
    <criterion id="7">tsc clean. No unused imports left behind from Y12 removal.</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Do NOT remove the period toggle (QTD/YTD/1Y/3Y/Max) from Rolling Flows. Only remove the view toggle (Stacked / 1Y Rolling).</constraint>
    <constraint>Do NOT change chart colors, tooltips, or data sources — visual layout changes only for Y1, Y4, Y6.</constraint>
    <constraint>Do NOT add the Advisor toggle (third option) to Top Performers or Rolling Flows — that is Y11/Y13 and gates on DS field confirmation.</constraint>
    <constraint>Do NOT use emojis in any code or log output.</constraint>
    <constraint>Commit with: git commit --author="0.4.2_RD_AdvisorIntelligence &lt;0.4.2_RD_AdvisorIntelligence@opal.agent&gt;" -m "..."</constraint>
    <constraint>Read the relevant portal source files before making changes. Do not patch blind.</constraint>
  </constraints>

  <what_this_unlocks>
    These changes are standalone. No downstream gates.
    Y4 net line visual confirmation is needed from Andrew/Yang before it is considered final.
  </what_this_unlocks>

  <deliverables>
    <deliverable type="commit">portal DEV: Y1 AUA stack flip + Y4 NNA diverging bar + Y6 bucket filter + footnote + Y12 1Y rolling removal</deliverable>
    <deliverable type="document">Session log with per-stream summary and portal DEV commit hash</deliverable>
  </deliverables>

</task_order>
```
