# Task Order: Advisors Tab Redesign (4C) — 0.4.2_RD_AdvisorIntelligence

```xml
<task_order>
  <metadata>
    <id>2.0.0_SA_COO-ADVI-005-rd-advisors_tab</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.2_RD_AdvisorIntelligence</issued_to>
    <date>2026-03-03</date>
    <status>pending</status>
    <thread_serial>ADVI-005</thread_serial>
    <thread_ref>org/threads/ADVI-005-pattern-0-stacked-bar--rolling-flows-dat/</thread_ref>
    <gate_status>CLEARED — DT Stream B2 deployed bd-v2.15.1. stacked_bar + rolling_1y are LIVE
      in advisor_rolling_flows.json. DE typed AdvisorRollingFlowsResponseV2 in portal DEV 5125eb9.
      START IMMEDIATELY.</gate_status>
    <updated_by>0.4.0_DE_ClientPlatform</updated_by>
    <updated_date>2026-03-04</updated_date>
  </metadata>

  <objective>
    Implement the Advisors tab rolling flows redesign (Stream 4C): stacked bar primary
    view + 1Y rolling line secondary view, per the ADVI-005 binding contract.
    Both backend keys are now live. DE has typed them. Start now.
  </objective>

  <references>
    <ref type="receipt">org/tier3_junior/0.4.2_RD_AdvisorIntelligence/threads/ADVI-005-pattern-0-stacked-bar--rolling-flows-dat_0.4.0_DS_ClientPlatform+0.4.0_DE_ClientPlatform.md</ref>
    <ref type="prd">docs/architecture/ADVISOR_INTELLIGENCE_COMPLETION.md</ref>
    <ref type="types">portal/src/pages/AdvisorIntelligence/types.ts — AdvisorRollingFlowsResponseV2,
      AdvisorBarEntry, AdvisorRolling1YSeries, StackedBarPeriodKey (portal DEV 5125eb9)</ref>
    <ref type="data_shape">docs/briefs/devops-brief-advi-005-rolling-flows.md — exact field names and shapes</ref>
  </references>

  <requirements>

    <!-- ================================================================ -->
    <!-- STREAM 4C — Stacked bar primary + rolling line secondary          -->
    <!-- ================================================================ -->
    <requirement id="4C.1">
      GATE CLEARED. stacked_bar and rolling_1y are LIVE in advisor_rolling_flows.json (bd-v2.15.1).
      Use AdvisorRollingFlowsResponseV2 (extends AdvisorRollingFlowsResponse) for the
      getAdvisorRollingFlows() call return type. Type is in types.ts (portal DEV 5125eb9).
    </requirement>
    <requirement id="4C.2">
      PRIMARY VIEW — Stacked Bar Chart (Recharts BarChart):
        - One bar per advisor (advisor_id as key, advisor_name for label)
        - Data source: stacked_bar[period].architects or .implementors (AdvisorBarEntry[])
        - Inflows: positive bar segment
        - Outflows: render downward — use -entry.outflows (JSON field is positive magnitude)
        - nna_net: signed, available for tooltip
        - Sorted by nna_net ascending (lowest leftmost, highest rightmost)
        - Period toggle: 'qtd' | 'ytd' | '1y' | '3y' | 'max' (StackedBarPeriodKey)
        - Architects / Implementors toggle at top (controls both views)
        - Tooltip: advisor_name, inflows (formatted positive), outflows (formatted positive), nna_net (signed)
    </requirement>
    <requirement id="4C.3">
      SECONDARY VIEW — 1-Year Rolling Line Chart (Recharts LineChart):
        - Data source: rolling_1y.architects or .implementors (AdvisorRolling1YSeries[])
        - Each series: { advisor_name, advisor_id, series: RollingFlowsDataPoint[] }
        - Plot nna by default (each point = trailing 365-day rolling NNA)
        - Period toggle controls x-axis window slice (how far back to show), NOT rolling window
          (rolling window is fixed at 1Y — the data is already 1Y rolling)
        - Same Architects/Implementors toggle as primary view
        - Tooltip: advisor_name, date, nna value (formatted)
        - Show top advisors by default (same auto-select logic as existing legacy chart)
    </requirement>
    <requirement id="4C.4">
      View toggle (Primary / Secondary): segmented control above chart area.
      Period toggle and Architects/Implementors toggle remain visible in both views.
    </requirement>
    <requirement id="4C.5">
      Type the getAdvisorRollingFlows() response as AdvisorRollingFlowsResponseV2.
      Guard on stacked_bar and rolling_1y before rendering new views:
        if (!data.stacked_bar) { /* show legacy chart */ }
        if (!data.rolling_1y) { /* show legacy chart */ }
      Keep existing legacy rolling flows chart as fallback until both keys are confirmed.
      This makes the component backward-compatible with cached/stale S3 responses.
    </requirement>

  </requirements>

  <acceptance_criteria>
    <criterion id="1">Stacked bar renders with inflows up, outflows down (negated), sorted by nna_net ascending.</criterion>
    <criterion id="2">Rolling 1Y line renders daily NNA per advisor; period toggle controls x-axis window.</criterion>
    <criterion id="3">Both views respond to Architects/Implementors toggle and period toggle.</criterion>
    <criterion id="4">Outflows displayed as positive in tooltips (formatCurrency(-entry.outflows) or abs value).</criterion>
    <criterion id="5">Legacy chart preserved as fallback when stacked_bar or rolling_1y keys are absent.</criterion>
    <criterion id="6">AdvisorRollingFlowsResponseV2 used as return type for getAdvisorRollingFlows().</criterion>
    <criterion id="7">bunx tsc -b passes.</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Gates are CLEARED. Do not wait. Start immediately.</constraint>
    <constraint>Outflows in JSON are positive magnitude. Negate client-side (-entry.outflows) for downward bar.</constraint>
    <constraint>Do not use AdvisorRollingFlowsResponse (V1) — use AdvisorRollingFlowsResponseV2.</constraint>
    <constraint>Import AdvisorRollingFlowsResponseV2, AdvisorBarEntry, AdvisorRolling1YSeries, StackedBarPeriodKey from ../types.</constraint>
    <constraint>DE reviews before DT pushes to DEV. Signal DE when commits are ready.</constraint>
    <constraint>No emojis in code.</constraint>
    <constraint>Commit with: git commit --author="0.4.2_RD_AdvisorIntelligence &lt;0.4.2_RD_AdvisorIntelligence@opal.agent&gt;" -m "0.4.2_RD_AdvisorIntelligence: AdvisorIntelligence/AdvisorsTab -- ..."</constraint>
  </constraints>

  <deliverables>
    <deliverable type="commit">AdvisorsTab.tsx: stacked bar primary view + rolling 1Y secondary view with legacy fallback</deliverable>
  </deliverables>
</task_order>
```
