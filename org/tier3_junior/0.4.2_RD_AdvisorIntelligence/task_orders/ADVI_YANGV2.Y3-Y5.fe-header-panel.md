# Task Order: Yang V2 Y3-FE + Y5-FE — Header Panel AUA Mix + GRO Mode — 0.4.2_RD_AdvisorIntelligence

```xml
<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-03-05-ADVI_YANGV2.Y3-Y5.fe-header-panel</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.2_RD_AdvisorIntelligence</issued_to>
    <date>2026-03-05</date>
    <status>complete</status>
    <priority>HIGH</priority>
    <streams>Y3-FE, Y5-FE</streams>
  </metadata>

  <objective>
    Add two new modes to the Assets Overview header panel (PartnerAnalytics.tsx):
    Y3-FE — AUA asset class mix toggle (Mode B "Mix" alongside Mode A "Clients")
    Y5-FE — GRO growth decomposition mode (third option at the top-level mode toggle)

    Both changes are in PartnerAnalytics.tsx. Both use new data keys from the DS Phase 2
    batch (deployed bd-v2.16.2). Gate: DE type wiring must be complete (ADVI-Y-phase3-de-type-wiring).
  </objective>

  <references>
    <ref type="prd">docs/architecture/ADVISOR_INTELLIGENCE_YANG_FEEDBACK_V2.md — Sections 1.3, 1.6</ref>
    <ref type="portal-header">portal/src/pages/AdvisorIntelligence/components/PartnerAnalytics.tsx</ref>
    <ref type="types">portal/src/pages/AdvisorIntelligence/types.ts — AuaMixView, GrowthDecompositionView (after DE gates)</ref>
  </references>

  <gate>
    DE type wiring (ADVI-Y-phase3-de-type-wiring) must be committed to portal DEV before
    starting this task order. Confirm DE's portal DEV commit exists before proceeding.
  </gate>

  <requirements>

    <!-- ================================================================ -->
    <!-- Y3-FE — AUA Asset Mix Toggle                                     -->
    <!-- ================================================================ -->
    <requirement id="Y3-FE.1">
      File: portal/src/pages/AdvisorIntelligence/components/PartnerAnalytics.tsx

      Read the current AUA mode rendering. There is already a top-level mode toggle
      (AUA / NNA). Inside the AUA content panel, add a SECONDARY toggle (upper-right
      of the panel content area, NOT in the panel title row):

        Mode A (default): label "Clients" (current NMNC/NMEC stacked bar — unchanged behavior)
        Mode B: label "Mix" (asset class breakdown stacked bar)

      State: add `auaSubMode: 'clients' | 'mix'` local state, defaulting to 'clients'.

      NOTE on Mode A label: "Clients" is a placeholder. The final label (could be
      "Clients", "Tenure", or "Client Type") is pending Andrew/Yang decision.
      Use "Clients" now. Label is a string constant — easy to change when decided.
    </requirement>

    <requirement id="Y3-FE.2">
      Mode B rendering (auaSubMode === 'mix'):
        Data source: the aua_mix view from the timeseries chart or header metrics response
        (AuaMixView type — confirm exact fetch location from DE types task order).
        Chart: stacked BarChart — one bar per period, segments = asset classes
          (Equities, Fixed Income, Real Estate, Alternatives, Cash, Other)
        Use the existing interval toggle (Month/Quarter/Year from Y8 implementation)
        to determine which period granularity to use.
        Colors: assign distinct colors from a new ASSET_CLASS_COLORS constant.
          Do not reuse NMNC/NMEC colors. Keep colors consistent across periods.
        Tooltip: show segment breakdown on hover.

      Mode A rendering is unchanged — the existing NMNC/NMEC stacked bar stays as-is.

      Guard: if aua_mix data is absent or empty, show a "Data unavailable" state
      (not an error — graceful degradation).
    </requirement>

    <!-- ================================================================ -->
    <!-- Y5-FE — GRO Mode (Growth Decomposition)                          -->
    <!-- ================================================================ -->
    <requirement id="Y5-FE.1">
      File: portal/src/pages/AdvisorIntelligence/components/PartnerAnalytics.tsx

      Extend the top-level mode toggle to add "GRO" as a third option alongside "AUA" and "NNA":
        Mode: AUA | NNA | GRO
      State: extend existing mode state type to include 'gro'.

      Label: "GRO" (short label in toggle). Full label in panel title: "Growth Decomposition".
    </requirement>

    <requirement id="Y5-FE.2">
      GRO mode chart:
        Data source: growth_decomposition.data (GrowthDecompositionPoint[] from timeseries chart)
        Chart type: Recharts ComposedChart with 3 Line series:
          1. Market Performance — label "Market", color distinct (e.g., purple/violet)
          2. NNA — label "NNA", reuse existing NNA color
          3. Total AUA Change — label "Total", color distinct (e.g., orange/amber)
        X-axis: period string, formatted by the Interval toggle (Month/Quarter/Year)
          Same interval toggle as AUA and NNA modes — reuse existing toggle state.
        Y-axis: formatted as dollar amount.
        Lines can go negative (market can be negative in down months).
        Tooltip: show all three values for the hovered period.
        Legend: show all three series labels.

      Guard: if growth_decomposition data is absent, show "Data unavailable" state.
    </requirement>

    <requirement id="Y5-FE.3">
      The interval toggle (Month/Quarter/Year from Y8) applies to GRO mode as well.
      GRO data is monthly-granularity — aggregate to Quarter/Year when those are selected,
      using the same aggregation helper as AUA mode (getPeriodInfo() or equivalent).
      For GRO, the aggregation rule is:
        market = sum of monthly market values in the period
        nna = sum of monthly nna values in the period
        total = market + nna (or sum of monthly totals — they should agree)
    </requirement>

  </requirements>

  <acceptance_criteria>
    <criterion id="1">AUA mode has a secondary sub-toggle "Clients" / "Mix". Default is "Clients".</criterion>
    <criterion id="2">Mode B "Mix" renders a stacked bar by asset class using aua_mix data.</criterion>
    <criterion id="3">Top-level mode toggle now shows AUA / NNA / GRO.</criterion>
    <criterion id="4">GRO mode renders 3-line ComposedChart from growth_decomposition data.</criterion>
    <criterion id="5">Interval toggle applies to both AUA mix and GRO modes.</criterion>
    <criterion id="6">Graceful degradation when aua_mix or growth_decomposition data absent.</criterion>
    <criterion id="7">tsc clean. No unused imports.</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Do NOT start before DE type wiring portal DEV commit is confirmed.</constraint>
    <constraint>The secondary AUA sub-toggle is inside the panel content area, NOT in the panel title row.</constraint>
    <constraint>AUA Mode A label "Clients" is a placeholder — use a named constant so it is easily changed.</constraint>
    <constraint>Do NOT remove or rename the existing AUA / NNA top-level toggle options.</constraint>
    <constraint>Do NOT use emojis in any code or log output.</constraint>
    <constraint>Commit with: git commit --author="0.4.2_RD_AdvisorIntelligence &lt;0.4.2_RD_AdvisorIntelligence@opal.agent&gt;" -m "..."</constraint>
  </constraints>

  <deliverables>
    <deliverable type="commit">portal DEV: Y3-FE AUA mix sub-toggle + Y5-FE GRO mode</deliverable>
    <deliverable type="document">Session log with portal DEV commit hash</deliverable>
  </deliverables>

</task_order>
```
