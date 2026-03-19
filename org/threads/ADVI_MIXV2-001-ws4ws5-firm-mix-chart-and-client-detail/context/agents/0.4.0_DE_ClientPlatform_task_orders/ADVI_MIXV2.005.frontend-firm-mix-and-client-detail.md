<task_order>
  <metadata>
    <id>0.4.0_DS_ClientPlatform-2026-03-17-005-de-frontend-mix</id>
    <issued_by>0.4.0_DS_ClientPlatform</issued_by>
    <issued_to>0.4.0_DE_ClientPlatform</issued_to>
    <date>2026-03-17</date>
    <status>pending</status>
    <project_code>ADVI_MIXV2</project_code>
  </metadata>

  <objective>
    Two frontend workstreams: (WS4) replace the firm-level mix chart in PartnerAnalytics.tsx
    with a pre-computed absolute dollar stacked bar chart fed from the new firm/mix-views endpoint,
    and (WS5) wire ClientDetailPage.tsx to real data and activate the existing MixTimeseriesPanel
    and ConcentrationPanel. WS4 depends on the Lambda endpoint being live (task order 004 complete).
    WS5 client detail stub removal can begin immediately.
  </objective>

  <scope>
    <pages>
      <page>portal/src/pages/AdvisorIntelligence/components/PartnerAnalytics.tsx</page>
      <page>portal/src/pages/AdvisorIntelligence/ClientDetail/ClientDetailPage.tsx</page>
      <page>portal/src/pages/AdvisorIntelligence/ClientDetail/panels/MixTimeseriesPanel.tsx</page>
      <page>portal/src/pages/AdvisorIntelligence/ClientDetail/panels/ConcentrationPanel.tsx</page>
    </pages>
    <files>
      <file action="modify">portal/src/pages/AdvisorIntelligence/types.ts</file>
      <file action="modify">portal/src/api/endpoints/advisor-intelligence.ts</file>
      <file action="modify">portal/src/pages/AdvisorIntelligence/components/PartnerAnalytics.tsx</file>
      <file action="modify">portal/src/pages/AdvisorIntelligence/ClientDetail/ClientDetailPage.tsx</file>
      <file action="modify">portal/src/pages/AdvisorIntelligence/ClientDetail/panels/MixTimeseriesPanel.tsx</file>
      <file action="modify">portal/src/pages/AdvisorIntelligence/ClientDetail/panels/ConcentrationPanel.tsx</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">
      WS4 — Add TypeScript types to types.ts:
        FirmMixClassValue { value: number; pct: number }
        FirmMixPeriodPoint { period, label, end_date, total_aua, equity: FirmMixClassValue,
          fixed_income: FirmMixClassValue, structured_notes: FirmMixClassValue,
          cash: FirmMixClassValue, other: FirmMixClassValue }
        FirmMixViewsResponse { generated_at, data_as_of, firm_id,
          views: { quarterly: FirmMixPeriodPoint[]; monthly: FirmMixPeriodPoint[]; annually: FirmMixPeriodPoint[] } }
      All pct fields are 0-1 convention. Add comments confirming this.
    </requirement>

    <requirement id="2">
      WS4 — Add API function to advisor-intelligence.ts:
        export async function getFirmMixViews(firmId: string): Promise&lt;FirmMixViewsResponse&gt;
        URL: /api/scoped/partners/books/firm/mix-views?firmId=${LAMBDA_FIRM_ID[firmId] ?? firmId}
    </requirement>

    <requirement id="3">
      WS4 — In PartnerAnalytics.tsx:
        (a) REMOVE: getFirmMixTimeseries import + call, firmMixRaw state, firmMixData useMemo
            (the 20-line period aggregation block at lines ~397-416)
        (b) ADD: useQuery call to getFirmMixViews(firmOverride || 'bd')
            queryKey: ['advisor-intelligence', 'firm-mix-views', firmOverride]
            staleTime: 10 * 60 * 1000 (same as other queries)
        (c) Derive chart data: firmMixViews?.views[granularity] ?? []
            where granularity maps: 'monthly' -&gt; 'monthly', 'quarterly' -&gt; 'quarterly', 'annually' -&gt; 'annually'
    </requirement>

    <requirement id="4">
      WS4 — Replace the 100% stacked bar chart with an absolute dollar stacked bar chart.
      The chart currently uses values like 0.62 (pct) for bar heights. The new chart uses
      asset class dollar amounts as bar heights, stacked to total_aua.

      Chart spec:
        - Recharts BarChart with stackId="mix"
        - dataKey for each Bar: use a computed field (equity_value, fixed_income_value, etc.)
          OR map each FirmMixPeriodPoint to a flat object before passing to BarChart:
          { label, total_aua, equity: pt.equity.value, fixed_income: pt.fixed_income.value, ... }
        - YAxis tickFormatter: formatNumberTo3Digits(value, { unit: '$', includeSign: false })
          (same formatter used in PartnerAnalytics.tsx for NNA bars)
        - domain: [0, 'auto'] — do not hardcode domain={[0, 1]}
        - Colors: same ASSET_CLASS_COLORS already in PartnerAnalytics.tsx

      Tooltip spec (per period bar):
        Line 1: label (period label, bold)
        Line 2: "Total AUA: $X.XXB"
        Divider
        Lines 3-7: each asset class with color dot, label, dollar value, and pct in parens
          e.g., "Equities   $1.02B  (62.0%)"
        Source: use the FirmMixPeriodPoint fields — pt.equity.value and pt.equity.pct * 100
    </requirement>

    <requirement id="5">
      WS5 — ClientDetailPage.tsx: replace the setTimeout stub with a real API call.
      The clientKey param is a relationship_id (confirm by reading how Books tab sets
      the clientKey param in navigation — it should be relationship_id or convertible).
      Call getClientDetail(firmId, clientKey) or the appropriate endpoint that provides
      BooksClientDetailResponse. If a different key mapping is needed, consult ClientsTab.tsx
      to understand how clientKey is set when navigating to ClientDetailPage.
    </requirement>

    <requirement id="6">
      WS5 — Mount MixTimeseriesPanel and ConcentrationPanel in ClientDetailPage.tsx.
      Add selectedAssetClass state (MixAssetClass | null) and mixWindow state (MixWindow).
      Pass relationshipId={clientKey} and firmId={firmId} to both panels.
      The two panels should be shared-state linked: clicking an area in MixTimeseriesPanel
      updates selectedAssetClass, which filters ConcentrationPanel.
    </requirement>

    <requirement id="7">
      WS5 — Remove mock data fallback from MixTimeseriesPanel and ConcentrationPanel.
      Currently: isPlaceholder = !data || data.length === 0; chartData = isPlaceholder ? MOCK_DATA : data
      Change to: show a clean empty state ("No allocation data available for this client")
      instead of rendering MOCK_DATA. The mock data makes it impossible to distinguish
      "no API response" from "real data that happens to look like the mock."
    </requirement>

    <requirement id="8">
      Commit all changes to portal DEV branch:
        git commit --author="0.4.0_DE_ClientPlatform &lt;0.4.0_DE_ClientPlatform@opal.agent&gt;"
      Separate commits for WS4 and WS5 (DE should split these for auditability).
      DE does NOT push — DT pushes portal DEV to remote.
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">WS4: firm-level mix chart shows dollar-valued stacked bars, not percentage bars</criterion>
    <criterion id="2">WS4: tooltip shows both $ and % for each asset class</criterion>
    <criterion id="3">WS4: firmMixData useMemo is completely removed from PartnerAnalytics.tsx</criterion>
    <criterion id="4">WS4: when endpoint returns 503 (data not yet built), chart shows appropriate loading/empty state</criterion>
    <criterion id="5">WS5: ClientDetailPage fetches real client data (no more setTimeout stub)</criterion>
    <criterion id="6">WS5: MixTimeseriesPanel and ConcentrationPanel mounted in ClientDetailPage with live data</criterion>
    <criterion id="7">WS5: selecting an asset class in mix panel filters concentration panel</criterion>
    <criterion id="8">WS5: no mock data rendered in either panel — empty state shown when no data</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>WS4 chart implementation requires Lambda endpoint live (task order 004 complete).
      For WS4 development before endpoint is live: implement against the type contract but leave
      the useQuery in loading state. Do not render mock data for the firm chart either.</constraint>
    <constraint>WS5 can begin immediately — the stub removal and panel mounting do not depend on the Lambda</constraint>
    <constraint>DE commits to portal DEV only — DT pushes</constraint>
    <constraint>No emojis in code or comments</constraint>
    <constraint>Issue a task order to 0.4.2_RD_AdvisorIntelligence for any visual/chart work that
      goes beyond wiring (chart color decisions, layout refinements, legend styling)</constraint>
  </constraints>

  <dependencies>
    <dependency agent="0.4.0_DT_ClientPlatform" task="ADVI_MIXV2.004" status="pending">
      WS4 requires Lambda endpoint to be live. WS5 has no Lambda dependency.
    </dependency>
  </dependencies>

  <deliverables>
    <deliverable type="commit">WS4 firm mix chart committed to portal DEV</deliverable>
    <deliverable type="commit">WS5 client detail wiring committed to portal DEV</deliverable>
    <deliverable type="document">pod_inventory.xml updated with new API functions and component changes</deliverable>
  </deliverables>
</task_order>
