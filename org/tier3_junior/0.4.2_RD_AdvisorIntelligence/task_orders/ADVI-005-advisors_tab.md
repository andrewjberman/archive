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
  </metadata>

  <objective>
    Implement the Advisors tab rolling flows redesign (Stream 4C): stacked bar primary
    view + 1Y rolling line secondary view, per the ADVI-005 binding contract. Blocked
    by DT Stream B2 deploy — do not start until DT confirms script 10 update is deployed
    and stacked_bar + rolling_1y are present in advisor_rolling_flows.json.
  </objective>

  <references>
    <ref type="receipt">org/tier3_junior/0.4.2_RD_AdvisorIntelligence/threads/ADVI-005-pattern-0-stacked-bar--rolling-flows-dat_0.4.0_DS_ClientPlatform+0.4.0_DE_ClientPlatform.md</ref>
    <ref type="prd">docs/architecture/ADVISOR_INTELLIGENCE_COMPLETION.md</ref>
  </references>

  <requirements>

    <!-- ================================================================ -->
    <!-- STREAM 4C — Stacked bar primary + rolling line secondary          -->
    <!-- BLOCKED: DT Stream B2 deploy must complete first                  -->
    <!-- ================================================================ -->
    <requirement id="4C.1">
      GATE: Do not start until DT confirms stacked_bar and rolling_1y are present
      in advisor_rolling_flows.json S3 output (Stream B2).
    </requirement>
    <requirement id="4C.2">
      PRIMARY VIEW — Stacked Bar Chart (Recharts, per ADVI-005 receipt):
        - One bar per advisor (advisor_id as key, advisor_name for label)
        - Inflows: positive bar segment
        - Outflows: render downward using -outflows (derived client-side; JSON field is positive magnitude)
        - nna_net: signed, available for tooltip
        - Sorted by nna_net ascending (lowest NNA leftmost, highest rightmost)
        - Period toggle: qtd | ytd | 1y | 3y | max (maps 1:1 to JSON keys)
        - Architects / Implementors toggle at top (controls both views)
        - Tooltip: advisor_name, inflows, outflows (positive), nna_net (signed)
    </requirement>
    <requirement id="4C.3">
      SECONDARY VIEW — 1-Year Rolling Line Chart (Recharts, per ADVI-005 receipt):
        - One line per advisor (top performers by default)
        - Data: rolling_1y.{architects|implementors}[].series (daily points)
        - Each point: { date, nna, inflows, outflows } — plot nna by default
        - Period toggle controls x-axis window slice (how far back), NOT rolling window
        - Rolling window fixed at 1Y (each point = trailing 365 days)
        - Same Architects/Implementors toggle as primary view
        - Tooltip: advisor_name, date, nna value
    </requirement>
    <requirement id="4C.4">
      View toggle (Primary / Secondary): segmented control or tab above chart area.
      Period toggle and Architects/Implementors toggle remain visible in both views.
    </requirement>
    <requirement id="4C.5">
      Use AdvisorRollingFlowsResponseV2 type (defined by DE per ADVI-005 receipt).
      Keep existing legacy chart as fallback until stacked_bar/rolling_1y keys are
      confirmed present in the response (defensive: check for undefined before rendering new views).
    </requirement>

  </requirements>

  <acceptance_criteria>
    <criterion id="1">Stacked bar renders with inflows up, outflows down, sorted by nna_net ascending.</criterion>
    <criterion id="2">Rolling 1Y line renders daily NNA per advisor with period toggle controlling x-axis.</criterion>
    <criterion id="3">Both views respond to Architects/Implementors toggle and period toggle.</criterion>
    <criterion id="4">Outflows displayed as positive in tooltips (no sign confusion).</criterion>
    <criterion id="5">Legacy chart preserved as fallback when new keys are absent.</criterion>
    <criterion id="6">bunx tsc -b passes.</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>BLOCKED by DT Stream B2 deploy. Do not start before confirmation.</constraint>
    <constraint>Implement per ADVI-005 receipt field names and types. Do not invent fields.</constraint>
    <constraint>Outflows in JSON are positive magnitude. Negate client-side for chart only.</constraint>
    <constraint>DE reviews before DT pushes to DEV.</constraint>
    <constraint>No emojis in code.</constraint>
    <constraint>Commit with: git commit --author="0.4.2_RD_AdvisorIntelligence &lt;0.4.2_RD_AdvisorIntelligence@opal.agent&gt;" -m "0.4.2_RD_AdvisorIntelligence: AdvisorIntelligence/AdvisorsTab -- ..."</constraint>
  </constraints>

  <deliverables>
    <deliverable type="commit">AdvisorsTab.tsx: stacked bar primary view + rolling 1Y secondary view</deliverable>
  </deliverables>
</task_order>
```
