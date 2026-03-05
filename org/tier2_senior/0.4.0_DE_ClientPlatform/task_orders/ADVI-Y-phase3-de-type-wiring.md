# Task Order: Yang V2 Phase 3 Type Wiring — 0.4.0_DE_ClientPlatform

```xml
<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-03-05-ADVI-Y-phase3-de-type-wiring</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DE_ClientPlatform</issued_to>
    <date>2026-03-05</date>
    <status>pending</status>
    <priority>HIGH — blocks all Phase 3 RD task orders. Start immediately.</priority>
    <streams>Y3-types, Y5-types, Y6b-types, Y6d-types, Y9-types, Y13-types, Y15-types</streams>
  </metadata>

  <objective>
    Add TypeScript types to portal/src/pages/AdvisorIntelligence/types.ts for all new
    data keys produced by the DS Phase 2 batch (deployed bd-v2.16.2/bd-v2.16.3) and for
    the Books tab L2/L3/L4 JSON shapes (from ADVI-006 design brief).

    Once your portal DEV commit lands, RD can begin all Phase 3 FE task orders in parallel.
    This is the only blocker on Phase 3.
  </objective>

  <references>
    <ref type="prd">docs/architecture/ADVISOR_INTELLIGENCE_YANG_FEEDBACK_V2.md</ref>
    <ref type="design-brief">docs/architecture/advisor_intelligence/books_tab_design_brief.md</ref>
    <ref type="data_contract">org/tier2_senior/0.4.0_DS_ClientPlatform/deliverables/data_contract.xml</ref>
    <ref type="types">portal/src/pages/AdvisorIntelligence/types.ts</ref>
    <ref type="existing-types-pattern">See CumulativeChartResponse, AdvisorRollingFlowsResponseV2 for extension patterns</ref>
  </references>

  <requirements>

    <requirement id="1">
      Read portal/src/pages/AdvisorIntelligence/types.ts in full before making any changes.
      Identify existing types to extend vs new interfaces to add.
      Read data_contract.xml for exact field names as deployed.
    </requirement>

    <!-- Y5 — Growth Decomposition -->
    <requirement id="Y5-types">
      Add to types.ts:

        export interface GrowthDecompositionPoint {
          period: string  // "2024-01" monthly YYYY-MM
          market: number  // AUA change attributable to market appreciation
          nna: number     // net new assets for the period
          total: number   // market + nna = total AUA change
        }

        export interface GrowthDecompositionView {
          description: string
          data: GrowthDecompositionPoint[]
        }

      Extend CumulativeChartResponse (or whatever type covers timeseries_chart.json) to add:
        growth_decomposition?: GrowthDecompositionView

      Confirm the exact parent response type by reading what getTimeseriesChart() returns.
    </requirement>

    <!-- Y9 — NNA geo/adv/drill with inflow+outflow -->
    <requirement id="Y9-types">
      The deployed timeseries_chart.json now includes nna_geo, nna_adv, nna_geo_drill.
      Each NNA series data point contains: date, [category]: nna_value,
      [category]_inflow: number, [category]_outflow: number.

      Add to types.ts:

        export interface NNASeriesPoint {
          date: string
          [key: string]: number | string  // category, category_inflow, category_outflow
        }

        export interface NNASeriesView {
          description: string
          categories: string[]
          data: NNASeriesPoint[]
        }

        export interface NNAGeoDrillView {
          [stateKey: string]: {
            categories: string[]
            data: NNASeriesPoint[]
          }
        }

      Extend timeseries_chart response type to add:
        nna_geo?: NNASeriesView
        nna_adv?: NNASeriesView
        nna_geo_drill?: NNAGeoDrillView
    </requirement>

    <!-- Y6b/Y6d — Snapshot NNA distribution drill -->
    <requirement id="Y6b-Y6d-types">
      Script 09 now produces a drill key on the nna.geo and nna.adv distribution views
      in header_metrics.json. Confirm exact structure from data_contract.xml, then add:

        export interface NNADistributionDrillEntry {
          total: NNADistributionStats       // re-use or define existing stats shape
          by_city?: { [cityKey: string]: NNADistributionStats }   // Y6b GEO drill
          by_relationship?: { [relKey: string]: NNADistributionStats }  // Y6d ADV drill
        }

        export interface NNADistributionDrill {
          [segmentKey: string]: NNADistributionDrillEntry
        }

      NNADistributionStats shape (confirm from data_contract.xml, but typically):
        export interface NNADistributionStats {
          count: number
          total: number
          percentiles: { p10: number; p25: number; p50: number; p75: number; p90: number }
          inflow_percentiles: { p10: number | null; p25: number | null; p50: number | null; p75: number | null; p90: number | null }
          outflow_percentiles: { p10: number | null; p25: number | null; p50: number | null; p75: number | null; p90: number | null }
          inflow_count: number
          outflow_count: number
          histogram: { bins: number[]; counts: number[] }
        }

      Extend the existing header_metrics nna distribution type to include:
        drill?: NNADistributionDrill

      Read data_contract.xml to confirm exact key names before writing types.
    </requirement>

    <!-- Y3 — AUA asset mix -->
    <requirement id="Y3-types">
      DS deployed aua_mix data. Confirm the exact key location (timeseries_chart.json
      or header_metrics.json) and field shape from data_contract.xml. Then add:

        export interface AuaMixSegment {
          label: string   // "Equities", "Fixed Income", etc.
          value: number
        }

        export interface AuaMixPoint {
          period: string
          segments: AuaMixSegment[]
        }

        export interface AuaMixView {
          data: AuaMixPoint[]
        }

      Extend the appropriate response type to include:
        aua_mix?: AuaMixView
    </requirement>

    <!-- Y13 — Stacked bar monthly -->
    <requirement id="Y13-types">
      advisor_rolling_flows.json stacked_bar now includes a monthly key.

      Extend AdvisorRollingFlowsResponseV2 (or its stacked_bar shape) to add:
        monthly?: { [yearMonth: string]: AdvisorBarEntry[] }
        // yearMonth format: "2024-01" (YYYY-MM period string)

      The AdvisorBarEntry type is unchanged (advisor_name, advisor_id, inflows, outflows,
      nna_net). Confirm AdvisorBarEntry is already exported and reusable.
    </requirement>

    <!-- Y15 — Books tab L2/L3/L4 types (from ADVI-006 design brief Section 6) -->
    <requirement id="Y15-types">
      Add all types from docs/architecture/advisor_intelligence/books_tab_design_brief.md
      Section 6 verbatim. These are the authoritative types — do not deviate.

      Interfaces to add:
        AdvisorBookResponse
        AdvisorBookClient
        ClientDetailResponse
        ClientAccount
        ClientTaxDetail
        CostBasisYear
        GainPosition
        OpenLot

      These are the complete definitions in Section 6 of the design brief.
      Copy them exactly.

      Also add API endpoint functions in portal/src/api/endpoints/advisor-intelligence.ts
      (or equivalent) for the two new scoped fetches:

        getAdvisorBook(advisorId: string): Promise&lt;AdvisorBookResponse&gt;
          // GET /api/scoped/advisor-intelligence/advisors/{advisorId}/book.json

        getClientDetail(clientKey: string): Promise&lt;ClientDetailResponse&gt;
          // GET /api/scoped/advisor-intelligence/clients/{clientKey}.json

      Follow the exact pattern of existing endpoint functions in that file.
    </requirement>

  </requirements>

  <acceptance_criteria>
    <criterion id="1">All new interfaces are exported from types.ts and tsc clean.</criterion>
    <criterion id="2">Existing types (CumulativeChartResponse, AdvisorRollingFlowsResponseV2) are extended, not replaced.</criterion>
    <criterion id="3">Y15 types match design brief Section 6 exactly — no phantom fields, no missing fields.</criterion>
    <criterion id="4">getAdvisorBook() and getClientDetail() endpoint functions added and typed.</criterion>
    <criterion id="5">Portal DEV commit made and hash documented in session log.</criterion>
    <criterion id="6">COO notified when complete so Phase 3 RD task orders are unblocked.</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Read data_contract.xml and the existing types.ts before writing. Do not invent field names.</constraint>
    <constraint>Do not modify any existing type interfaces — only extend or add new ones.</constraint>
    <constraint>Do NOT use emojis in any code or log output.</constraint>
    <constraint>Commit with: git commit --author="0.4.0_DE_ClientPlatform &lt;0.4.0_DE_ClientPlatform@opal.agent&gt;" -m "..."</constraint>
  </constraints>

  <deliverables>
    <deliverable type="commit">portal DEV: types.ts additions (Y3/Y5/Y6b/Y6d/Y9/Y13/Y15 types) + endpoint functions</deliverable>
    <deliverable type="document">Session log with portal DEV commit hash. COO notification.</deliverable>
  </deliverables>

</task_order>
```
