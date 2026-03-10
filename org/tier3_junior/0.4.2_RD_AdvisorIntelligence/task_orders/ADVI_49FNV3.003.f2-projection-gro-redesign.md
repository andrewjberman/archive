<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-03-09-003</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.2_RD_AdvisorIntelligence</issued_to>
    <date>2026-03-09</date>
    <status>complete</status>
    <thread_serial>ADVI_49FNV3-003</thread_serial>
    <thread_ref>org/threads/ADVI_49FNV3-003-f2-projection-visualization-gro-chart-re/</thread_ref>
  </metadata>

  <objective>
    Redesign the F2 projection system and GRO chart in PartnerAnalytics.tsx based on the
    converged specification from thread ADVI_49FNV3-003. Fixes 4 flaws: AUA projection 0/0
    regression, GRO chart unintelligibility, tooltip "(add)" format, and GRO tooltip _proj leakage.
    Single-file change. No backend or data contract changes.
  </objective>

  <scope>
    <pages>
      <page>portal/src/pages/AdvisorIntelligence/</page>
    </pages>
    <files>
      <file action="modify">portal/src/pages/AdvisorIntelligence/components/PartnerAnalytics.tsx</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">AUA full-history prior lookup: Refactor AUA aggregation to mirror the
      existing NNA "fullPeriodMap + windowedPeriodKeys" pattern. Build allSortedAuaPeriods from
      unfiltered timeseriesData.aua.data. Filter to windowedPeriodKeys for display. Compute
      prior/priorPrior from full-history list, not windowed list. Preserve endDate on period rows
      and category keys exactly as timeseriesData.aua.categories provides (NMNC/NMEC casing).</requirement>

    <requirement id="2">AUA projection unavailable: When full-history prior period end is missing
      (true first period in dataset), render NO ghost bars and show a single tooltip line:
      "Projection unavailable (insufficient history)". Tooltip-only -- no inline badge.</requirement>

    <requirement id="3">AUA projection formula (unchanged logic, just correct prior source):
      delta = actual - priorEnd (from full history).
      projectedDelta = delta * ratio (totalDays / elapsedDays).
      projectedValue = priorEnd + projectedDelta.
      Cap: capDelta = 1.5 * priorPeriodChange; cappedValue = min(projectedValue, priorEnd + capDelta).
      Ghost = max(0, cappedValue - actual).</requirement>

    <requirement id="4">AUA + NNA tooltip projection format: Replace "(add)" ghost increment rows
      with "Projected Full Period" section showing full projected values with "(currently ...)"
      parentheticals.
      AUA example: "New Client Assets: $P (currently $A)" / "Projected Total: $P (currently $A)".
      NNA gross example: "Inflows: +$P (currently +$A)" / "Outflows: -$P (currently -$A)" /
      "Net: +$P (currently +$A)".
      NNA net-only: show Net only + projected Net only.</requirement>

    <requirement id="5">GRO chart redesign: Convert from 3-line chart to ComposedChart hybrid.
      Stacked bars: market + nna with stackId="gro" and stackOffset="sign".
      Overlay line: total (stroke width 3).
      ReferenceLine y={0}.
      Y-axis label: "AUA Change" or "Period delta AUA" to clarify these are period deltas, not
      absolute values.</requirement>

    <requirement id="6">GRO projection: Total-only. Emit only total_proj as dashed line extension
      (strokeDasharray="6 3", legendType="none"). Do NOT emit market_proj or nna_proj.</requirement>

    <requirement id="7">GRO tooltip: Datum-driven rendering from payload[0].payload. Do NOT use
      payload.map(). Deterministic rows:
      - Header: {label} + subtitle "AUA change (period delta)"
      - Market: +/-$X (sign-colored: green positive, red negative)
      - Net Flows: +/-$X (sign-colored)
      - Total Change: +/-$X (sign-colored)
      - Comparison vs prior (Total only): MoM/QoQ/YoY Change as +/-$delta (no %)
      - Projected Full Period (Total only, last/incomplete): "Projected Total Change: +/-$P
        (currently +/-$A)"
      Filter rule: never render *_proj series rows.</requirement>

    <requirement id="8">GRO hero metrics: Add 3 tiles when panelViewMode === 'gro', using the
      existing tile container pattern:
      - Market (delta $)
      - Net Flows (delta $)
      - Total Change (delta $)
      Comparison vs prior period for Total only (delta $ only, no % -- sign flips make % nonsensical).
      Same granularity-based comparison label logic (MoM/QoQ/YoY) as existing AUA/NNA tiles.</requirement>

    <requirement id="9">GRO legend labels: Expand to descriptive labels if space permits:
      "Market (delta AUA)", "Net Flows (NNA)", "Total (Market + NNA)".
      Fallback to short labels if space-constrained, but tooltip/section titles must carry meaning.</requirement>

    <requirement id="10">Keep existing "project the last bar in dataset" behavior (not calendar
      current period). This handles data lag gracefully.</requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">AUA / Interval: Year / Window: 1Y: last bar shows ghost if period incomplete
      and full-history prior exists. If no prior: tooltip shows "Projection unavailable
      (insufficient history)" and no ghost bar.</criterion>
    <criterion id="2">AUA tooltip on last bar: "Projected Full Period" shows full projected values
      with "(currently ...)" parentheticals. No "(add)" rows anywhere.</criterion>
    <criterion id="3">NNA tooltip on last bar: same pattern -- full projected inflows/outflows/net
      with "(currently ...)" parentheticals.</criterion>
    <criterion id="4">GRO mode: chart renders as stacked bars (market + nna) + total line.
      ReferenceLine at y=0. Y-axis labeled.</criterion>
    <criterion id="5">GRO tooltip: shows exactly Market / Net Flows / Total Change (sign-colored),
      Total comparison vs prior, projected Total for last period. No duplicated projection rows.
      No *_proj leakage.</criterion>
    <criterion id="6">GRO hero metrics: 3 tiles visible below chart (Market / Net Flows /
      Total Change). Total has comparison vs prior.</criterion>
    <criterion id="7">bunx tsc -b passes clean.</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Single file: PartnerAnalytics.tsx only. Do not modify types.ts, other tabs, or
      backend code.</constraint>
    <constraint>No backend or data contract changes. All data already exists in
      timeseries_chart.json.</constraint>
    <constraint>Preserve existing AUA/NNA tooltip sections (actual values, growth comparison).
      Only the "Projected" section changes format.</constraint>
    <constraint>Do not add market/nna projections to GRO -- Total-only per thread decision.</constraint>
    <constraint>Do not add an inline badge for "projection unavailable" -- tooltip-only per
      thread decision.</constraint>
  </constraints>

  <dependencies>
    <dependency agent="1.0.0_SA_CTO"
                task="ADVI_49FNV3-003 thread convergence"
                status="complete"/>
  </dependencies>

  <deliverables>
    <deliverable type="commit">Portal DEV commit implementing all 10 requirements.
      Commit message: "0.4.2_RD_AdvisorIntelligence: ADVI_49FNV3.003 -- F2 projection redesign + GRO hybrid chart"</deliverable>
  </deliverables>

  <references>
    <ref type="thread">org/threads/ADVI_49FNV3-003-f2-projection-visualization-gro-chart-re/</ref>
    <ref type="analysis">org/tier1_exec/1.0.0_SA_CTO/deliverables/ADVI_49FNV3-F2-visualization-analysis.md</ref>
    <ref type="receipt">org/tier3_junior/0.4.2_RD_AdvisorIntelligence/threads/ADVI_49FNV3-003-f2-projection-visualization-gro-chart-re_1.0.0_SA_CTO+0.4.0_DE_ClientPlatform.md</ref>
    <ref type="prd">docs/architecture/ADVISOR_INTELLIGENCE_49FN_V3_PRD.md</ref>
  </references>
</task_order>
