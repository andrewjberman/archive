<task_order>
  <metadata>
    <id>ADVI_49FNV3.F4.stacked-bar-impl</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.2_RD_AdvisorIntelligence</issued_to>
    <date>2026-03-06</date>
    <status>pending</status>
    <thread_serial>ADVI_49FNV3-001</thread_serial>
    <thread_ref>org/threads/ADVI_49FNV3-001-pattern-0-stacked-bar-advisor-inflow-out/</thread_ref>
  </metadata>

  <objective>
    Implement F4: Top Ten Advisors stacked bar in AdvisorsTab. Data contract confirmed in
    ADVI_49FNV3-001 thread: this is frontend-only. No backend changes required.
    `AdvisorBarEntry` interface already exists in types.ts.
  </objective>

  <scope>
    <pages>
      <page>portal/src/pages/AdvisorIntelligence/tabs/AdvisorsTab.tsx</page>
    </pages>
    <files>
      <file action="modify">portal/src/pages/AdvisorIntelligence/tabs/AdvisorsTab.tsx</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">Data source: `stacked_bar.{period}.{role}[]` from `advisor_rolling_flows.json`
      via `getAdvisorRollingFlows()`. Use the existing `AdvisorBarEntry` interface from types.ts:
      `{ advisor_name, advisor_id, inflows, outflows, nna_net }`.
      - `inflows`: positive magnitude
      - `outflows`: positive magnitude (render below zero as `outflowsNeg = -outflows`)
      - `nna_net`: signed (inflows - outflows)
    </requirement>
    <requirement id="2">Chart: Recharts stacked bar with `stackOffset="sign"` and a shared `stackId`.
      Blue bar for inflows (above zero line). Red bar rendered from `outflowsNeg` (below zero).
      ReferenceLine at y=0 (thin, dark). Period keys: qtd, ytd, 1y, 3y, max. Role keys: architects, implementors.</requirement>
    <requirement id="3">Gold NNA dash: render a Scatter or ReferenceDot at y=nna_net for each advisor.
      Use a custom dash/marker shape in gold/amber. This is the same visual pattern as the triangle
      markers in ModelPortfolios Peer Performance.</requirement>
    <requirement id="4">Top N: show top 10 advisors. Sort by `nna_net` descending (tie-break: advisor_name asc).
      Use the role from the current view toggle (architects or implementors).</requirement>
    <requirement id="5">Tooltip: on hover for each advisor bar, show advisor_name, inflows (formatted),
      outflows (formatted), and nna_net (signed, formatted).</requirement>
    <requirement id="6">Replace the existing top-ten panel content only. Do not change the period toggle,
      role toggle, or leaderboard table below.</requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">Stacked bar renders for top 10 advisors with blue inflows above zero, red outflows below zero, gold NNA dash.</criterion>
    <criterion id="2">Period toggle (qtd/ytd/1y/3y/max) updates the chart data correctly.</criterion>
    <criterion id="3">Architect/implementor toggle updates the chart data correctly.</criterion>
    <criterion id="4">TypeScript compiles cleanly (no `any` types introduced).</criterion>
    <criterion id="5">Portal DEV commit with `--author` flag. DE to review before DT pushes to PROD.</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>No backend changes. All data already exists in advisor_rolling_flows.json.</constraint>
    <constraint>Do NOT add total_aua to the sort — it would require a backend change. Use nna_net as sort key.</constraint>
    <constraint>AdvisorBarEntry interface already exists. Do not redefine it — import it from types.ts.</constraint>
  </constraints>

  <dependencies/>

  <deliverables>
    <deliverable type="commit">Portal DEV commit implementing F4 stacked bar.</deliverable>
  </deliverables>

  <references>
    <ref type="prd">docs/architecture/ADVISOR_INTELLIGENCE_49FN_V3_PRD.md</ref>
    <ref type="thread">org/threads/ADVI_49FNV3-001-pattern-0-stacked-bar-advisor-inflow-out/messages/</ref>
  </references>
</task_order>
