# Task Order: Yang V2 Y13-FE — Rolling Flows NNA Bar with Interval + AdvisorType — 0.4.2_RD_AdvisorIntelligence

```xml
<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-03-05-ADVI-Y13-FE-rolling-flows-nna-bar</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.2_RD_AdvisorIntelligence</issued_to>
    <date>2026-03-05</date>
    <status>complete</status>
    <priority>HIGH</priority>
    <stream>Y13-FE</stream>
  </metadata>

  <objective>
    Replace the current stacked bar in the Rolling Flows panel (AdvisorsTab.tsx) with
    the NNA diverging bar format: one bar per time period showing aggregate inflow/outflow
    for the selected advisorType. Add Month/Quarter/Year interval toggle using the new
    monthly granularity data from stacked_bar.monthly.

    This supersedes the 4C stacked bar (which showed one bar per advisor, sorted by nna_net).
    The new view shows one bar per period (aggregate across all advisors of the selected type).

    Gate: DE type wiring (ADVI-Y-phase3-de-type-wiring) must be committed to portal DEV.
  </objective>

  <references>
    <ref type="prd">docs/architecture/ADVISOR_INTELLIGENCE_YANG_FEEDBACK_V2.md — Section 3.4</ref>
    <ref type="portal-advisors">portal/src/pages/AdvisorIntelligence/tabs/AdvisorsTab.tsx</ref>
    <ref type="types">portal/src/pages/AdvisorIntelligence/types.ts — AdvisorBarEntry, AdvisorRollingFlowsResponseV2.stacked_bar.monthly (after DE gate)</ref>
    <ref type="recharts-pattern">Use stackOffset="sign" + stackId for diverging bar — see Y4 RD session log (2026-03-04)</ref>
    <ref type="nna-assets-overview">The diverging bar format matches PartnerAnalytics.tsx NNA mode (Y4 fix). Copy that pattern.</ref>
  </requirements>

  <gate>
    DE type wiring must be confirmed. Y13 specifically requires the monthly key type
    (AdvisorRollingFlowsResponseV2.stacked_bar.monthly) to be added by DE before RD can implement.
  </gate>

  <requirements>

    <requirement id="Y13-FE.1">
      Read AdvisorsTab.tsx in full before making changes. Identify the current Rolling
      Flows panel state and the StackedBarChart component (which shows one bar per advisor).

      The new Rolling Flows chart:
        - X-axis: time periods (months, quarters, or years — driven by interval toggle)
        - Y-axis: dollar amount (aggregate inflow/outflow/NNA for all advisors of selected type)
        - Each period bar: diverging format — inflow extends up, outflow extends down
        - Net line: Line component showing aggregate nna_net per period
          (centered at actual NNA value — do NOT use midpoint formula)
        - Recharts: ComposedChart with stackOffset="sign", two Bar components + one Line

      Data aggregation (client-side):
        For each period, sum inflows and outflows across all AdvisorBarEntry items
        in stacked_bar[period][advisorType]:
          period_inflows  = sum(entry.inflows for entry in entries)
          period_outflows = sum(entry.outflows for entry in entries)
          period_nna      = period_inflows - period_outflows
        Then render one bar per period with these aggregated values.
    </requirement>

    <requirement id="Y13-FE.2">
      Interval toggle: Month / Quarter / Year
        Month: use stacked_bar.monthly["2024-01"] keys (new monthly granularity from Y13 DS batch)
        Quarter: use existing stacked_bar["qtd"], ["ytd"] period keys
          (or aggregate monthly data into quarters if QTD/YTD don't align — DS to confirm)
        Year: aggregate monthly data into calendar years

      Default: Month (most granular). Reuse the interval toggle pattern from Y8
      (PartnerAnalytics.tsx continuous AUA stacked bar implementation).

      State to manage:
        rollingFlowsInterval: 'month' | 'quarter' | 'year'  (new, replaces stackedBarPeriod)
    </requirement>

    <requirement id="Y13-FE.3">
      AdvisorType toggle: Architects / Implementors (+ Advisors if Y11 confirmed field exists)

      Check DS Phase 2 session log for Y11 result (did the advisor field exist in the gold layer?).
      If stacked_bar.advisors key exists in the deployed JSON: add "Advisors" as a third toggle option.
      If stacked_bar.advisors does NOT exist: keep Architects / Implementors only. Do not add a
      disabled/placeholder "Advisors" option.

      Read the DS phase 2 session log at org/tier2_senior/0.4.0_DS_ClientPlatform/logs/
      to find the Y11 finding before deciding.
    </requirement>

    <requirement id="Y13-FE.4">
      Tooltip per period bar:
        Period label (e.g., "Jan 2024", "Q1 2024", "2024")
        Inflows: formatted positive dollar amount
        Outflows: formatted positive dollar amount
        NNA: signed dollar amount

      Reuse formatCurrency from @/lib/universalNumberFormatter.
    </requirement>

    <requirement id="Y13-FE.5">
      The period toggle (QTD/YTD/1Y/3Y/Max) used by the old stacked bar is REMOVED.
      It is replaced entirely by the new Month/Quarter/Year interval toggle.
      Remove the old stackedBarPeriod state and STACKED_BAR_PERIOD_OPTIONS constant
      if they are no longer referenced elsewhere in the file.
    </requirement>

  </requirements>

  <acceptance_criteria>
    <criterion id="1">Rolling Flows panel renders a diverging bar per period (aggregate inflow up, outflow down) not per advisor.</criterion>
    <criterion id="2">Interval toggle Month/Quarter/Year is present and drives period bucketing.</criterion>
    <criterion id="3">AdvisorType toggle (Arch/Impl, +Advisors if Y11 confirmed) controls which advisorType is aggregated.</criterion>
    <criterion id="4">Net NNA Line component present. Uses actual NNA value (not midpoint).</criterion>
    <criterion id="5">Old QTD/YTD/1Y/3Y/Max period toggle removed.</criterion>
    <criterion id="6">tsc clean. No unused state or imports from old stacked bar.</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Do NOT start before DE type wiring portal DEV commit is confirmed.</constraint>
    <constraint>Check DS Y11 finding before adding Advisors toggle option.</constraint>
    <constraint>Use stackOffset="sign" + stackId for diverging bar — confirmed pattern from Y4.</constraint>
    <constraint>Do NOT use emojis in any code or log output.</constraint>
    <constraint>Commit with: git commit --author="0.4.2_RD_AdvisorIntelligence &lt;0.4.2_RD_AdvisorIntelligence@opal.agent&gt;" -m "..."</constraint>
  </constraints>

  <deliverables>
    <deliverable type="commit">portal DEV: Y13-FE rolling flows NNA diverging bar with interval + advisorType toggle</deliverable>
    <deliverable type="document">Session log with portal DEV commit hash and Y11 finding citation</deliverable>
  </deliverables>

</task_order>
```
