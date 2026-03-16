<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-03-16-005-rd-mix-charts</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.2_RD_AdvisorIntelligence</issued_to>
    <date>2026-03-16</date>
    <status>complete</status>
    <thread_serial>ADVI_MVPLVL-005</thread_serial>
    <thread_ref>org/threads/ADVI_MVPLVL-005-addendum-a-mix-timeseries-alignment/</thread_ref>
  </metadata>

  <objective>
    Wire Mix timeseries and Concentration charts into the Books Tab L3 (relationship
    detail) view. 100% stacked area charts using Recharts, linked via asset class
    click filtering.
  </objective>

  <scope>
    <pages>
      <page>portal/src/pages/AdvisorIntelligence/</page>
    </pages>
    <files>
      <file action="create">portal/src/pages/AdvisorIntelligence/ClientDetail/panels/MixTimeseriesPanel.tsx</file>
      <file action="create">portal/src/pages/AdvisorIntelligence/ClientDetail/panels/ConcentrationPanel.tsx</file>
      <file action="modify">portal/src/api/endpoints/advisor-intelligence.ts</file>
      <file action="modify">portal/src/pages/AdvisorIntelligence/tabs/ClientsTab.tsx</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">
      Add API client functions to advisor-intelligence.ts:
      - getMixTimeseries(relationshipId, firmId, window?) -> MixTimeseriesPoint[]
      - getConcentrationTimeseries(relationshipId, firmId, window?) -> ConcentrationResponse
      TypeScript interfaces per thread receipt (Turn 2):
        MixTimeseriesPoint: {date, equity, fixed_income, structured_notes, cash, other} (all number 0-1)
        ConcentrationPoint: {date, asset_name, ticker: string|null, asset_class, market_value, pct}
        ConcentrationResponse: {relationship_id, top_n, data: ConcentrationPoint[]}
    </requirement>
    <requirement id="2">
      MixTimeseriesPanel: 100% stacked area chart (Recharts AreaChart with stackId="mix").
      5 series: equity, fixed_income, structured_notes, cash, other.
      Semantic color mapping. Independent 1Y/3Y/Max window toggle (local state, not lifted).
      No granularity toggle — render daily data directly.
    </requirement>
    <requirement id="3">
      Mix-to-Concentration linkage: local `selectedAssetClass: string | null` state.
      Clicking an asset class area in Mix toggles the filter. Click same class to deselect.
      Non-selected classes render at opacity 0.3. Concentration chart filters to selected class.
    </requirement>
    <requirement id="4">
      ConcentrationPanel: chart showing top-N securities over time, filtered by selectedAssetClass
      when set. Display asset_name as primary label, ticker in parentheses when non-null.
      Header shows "Top {top_n} Holdings" using the top_n field from the response.
    </requirement>
    <requirement id="5">
      Wire both panels into ClientDetailPage below existing PortfolioBalancePanel.
      Pass relationshipId and firmId as props.
    </requirement>
    <requirement id="6">
      L4 (account level): NO changes. Existing PortfolioBalancePanel snapshot stays as-is.
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">bunx tsc -b --noEmit passes with zero errors</criterion>
    <criterion id="2">Mix chart renders 5 asset class areas that always fill to 100%</criterion>
    <criterion id="3">Clicking an asset class in Mix filters Concentration chart</criterion>
    <criterion id="4">Window toggle (1Y/3Y/Max) re-fetches data from endpoint</criterion>
    <criterion id="5">Null ticker holdings display asset_name only (no "(null)" text)</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Use Recharts only — do NOT introduce ApexCharts for these panels</constraint>
    <constraint>Do NOT modify L4 (account detail) views</constraint>
    <constraint>Can begin with mock data before Lambda is live — skeleton state until endpoints are deployed</constraint>
  </constraints>

  <dependencies>
    <dependency agent="0.4.0_DT_ClientPlatform" task="ADVI_MVPLVL.005.lambda-deploy" status="pending">
      Lambda endpoints must be deployed for live data. RD can begin with mock data before this.
    </dependency>
  </dependencies>

  <deliverables>
    <deliverable type="commit">Portal DEV commit with both panels + API client</deliverable>
  </deliverables>
</task_order>
