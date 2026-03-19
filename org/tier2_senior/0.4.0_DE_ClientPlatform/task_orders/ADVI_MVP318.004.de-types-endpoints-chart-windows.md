<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-03-18-mvp318-004-de</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DE_ClientPlatform</issued_to>
    <date>2026-03-18</date>
    <status>complete</status>
    <!-- WS3e: d4ecfc9. WS5: 933dfa3, af4960a. WS4 pod_inventory: RD gate cleared (62143e7), pod_inventory.xml updated 2026-03-19. -->
    <project_code>ADVI_MVP318</project_code>
  </metadata>

  <objective>
    Add advisor-level TypeScript types and API functions for the two new endpoints (WS3e),
    update periodToChartWindow() and ChartWindowOption for MTD/QTD/YTD windows (WS5),
    and update pod_inventory.xml after RD completes ConsolidatedOverviewPanel (WS4 gate).
    All portal changes commit to portal DEV under DE author attribution.
  </objective>

  <context>
    Reference: docs/architecture/ADVI_MVP318_PRD.md §WS3e, §WS4, §WS5.

    WS3e gate: DT must deploy opal-partners-data (partners-api-v1.4.0) before DE commits
    the API functions, so the endpoints are live when DE calls them in development.
    WS3e TypeScript types can be written immediately (no gate). Commit types + functions together
    after DT's WS3d deploy.

    WS5 chart window update: the gold layer run (AE, WS5) must complete AND the portal pipeline
    must re-run (triggered automatically by pipeline-complete.json) before the new MTD/QTD/YTD
    keys appear in the leaderboard response. DE can write the code now but should verify against
    live data after AE's run completes.

    Endpoint URLs:
    - /api/scoped/partners/books/advisor/{advisor_id}/timeseries?firmId={firmId}
    - /api/scoped/partners/books/advisor/{advisor_id}/mix-timeseries?firmId={firmId}&amp;window={window}

    Existing pattern reference: look at how getRelationshipTimeseries() and getRelationshipMixTimeseries()
    are implemented in advisor-intelligence.ts — use the same URL construction pattern with
    LAMBDA_FIRM_ID mapping.
  </context>

  <scope>
    <files>
      <file action="modify">portal/src/api/endpoints/advisor-intelligence.ts (or appropriate types file)</file>
      <file action="modify">portal/src/pages/AdvisorIntelligence/tabs/AdvisorsTab.tsx</file>
      <file action="modify">portal/src/pages/AdvisorIntelligence/types.ts</file>
      <file action="modify">portal/pod_inventory.xml (after RD WS4 ConsolidatedOverviewPanel commit)</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1" workstream="WS3e-types">
      Read portal/src/api/endpoints/advisor-intelligence.ts and portal/src/pages/AdvisorIntelligence/types.ts.
      Identify existing MixTimeseriesPoint type — reuse it for AdvisorMixTimeseriesResponse.data[].

      Add to the types file (or advisor-intelligence.ts, wherever types live):

        export interface AdvisorTimeseriesPoint {
          date: string;
          total_aua: number;
          cum_inflows: number;
          cum_outflows: number;
          nna: number;
        }

        export interface AdvisorTimeseriesResponse {
          advisor_id: string;
          advisor_name: string;
          data_as_of: string;
          data: AdvisorTimeseriesPoint[];
        }

        export interface AdvisorMixTimeseriesResponse {
          advisor_id: string;
          advisor_name: string;
          data_as_of: string;
          data: MixTimeseriesPoint[];
        }
    </requirement>

    <requirement id="2" workstream="WS3e-functions" condition="After DT confirms WS3d deploy (partners-api-v1.4.0)">
      GATE: Wait for DT to confirm opal-partners-data is deployed before committing API functions.

      Add to advisor-intelligence.ts:

        export async function getAdvisorTimeseries(
          advisorId: string,
          firmId: string
        ): Promise&lt;AdvisorTimeseriesResponse&gt; {
          const mappedFirmId = LAMBDA_FIRM_ID[firmId] ?? firmId;
          const url = `/api/scoped/partners/books/advisor/${advisorId}/timeseries?firmId=${mappedFirmId}`;
          return fetchJson&lt;AdvisorTimeseriesResponse&gt;(url);
        }

        export async function getAdvisorMixTimeseries(
          advisorId: string,
          firmId: string,
          window?: MixWindow
        ): Promise&lt;AdvisorMixTimeseriesResponse&gt; {
          const mappedFirmId = LAMBDA_FIRM_ID[firmId] ?? firmId;
          const params = new URLSearchParams({ firmId: mappedFirmId });
          if (window) params.set('window', window);
          const url = `/api/scoped/partners/books/advisor/${advisorId}/mix-timeseries?${params}`;
          return fetchJson&lt;AdvisorMixTimeseriesResponse&gt;(url);
        }

      Match the exact fetch helper and error handling pattern used by existing functions in that file.
      Use MixWindow type if it already exists; if not, use string and add a comment.

      Commit types + functions together to portal DEV:
        git commit --author="0.4.0_DE_ClientPlatform &lt;0.4.0_DE_ClientPlatform@opal.agent&gt;" \
          -m "feat(portal): AdvisorTimeseries types + API functions (ADVI_MVP318 WS3e)"
    </requirement>

    <requirement id="3" workstream="WS5-chart-windows">
      Read portal/src/pages/AdvisorIntelligence/tabs/AdvisorsTab.tsx.
      Locate the periodToChartWindow() function. Currently it maps mtd->3M, qtd->3M, ytd->1Y (fallbacks).
      Update it:
        function periodToChartWindow(p: PeriodKey): ChartWindowOption {
          if (p === 'mtd') return 'MTD'
          if (p === 'qtd') return 'QTD'
          return 'YTD'
        }

      Read portal/src/pages/AdvisorIntelligence/types.ts.
      Locate ChartWindowOption type union. Add 'MTD' | 'QTD' | 'YTD' to it.
      Existing trailing windows (3M, 6M, 1Y, 2Y, 3Y) must remain in the union.

      These changes can be written now but should be verified against live leaderboard data
      after AE's gold layer run completes (AE ADVI_MVP318.003). The leaderboard JSON must
      contain windows.MTD, windows.QTD, windows.YTD before the UI can be tested.

      Commit to portal DEV:
        git commit --author="0.4.0_DE_ClientPlatform &lt;0.4.0_DE_ClientPlatform@opal.agent&gt;" \
          -m "feat(portal): MTD/QTD/YTD chart window support (ADVI_MVP318 WS5)"
    </requirement>

    <requirement id="4" workstream="WS4-pod-inventory" condition="After RD commits ConsolidatedOverviewPanel">
      GATE: Wait for RD to commit all ConsolidatedOverviewPanel work (WS4) to portal DEV.

      After RD commits:
      1. Read portal/pod_inventory.xml (or wherever component inventory lives in the portal dir).
      2. Add entries for:
         - ConsolidatedOverviewPanel component (if new file added by RD)
         - New API endpoint functions: getAdvisorTimeseries, getAdvisorMixTimeseries
         - New route patterns: /books/advisor/{id}/timeseries, /books/advisor/{id}/mix-timeseries
      3. Verify the panel renders at all three levels (N1 firm, L2 advisor, L3 relationship)
         by reviewing RD's commit and checking that the component handles all three drill levels.
      4. Commit pod_inventory.xml update to portal DEV:
           git commit --author="0.4.0_DE_ClientPlatform &lt;0.4.0_DE_ClientPlatform@opal.agent&gt;" \
             -m "chore(portal): update pod_inventory for ConsolidatedOverviewPanel + advisor endpoints (ADVI_MVP318 WS4)"
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">AdvisorTimeseriesResponse, AdvisorTimeseriesPoint, AdvisorMixTimeseriesResponse types added</criterion>
    <criterion id="2">getAdvisorTimeseries() and getAdvisorMixTimeseries() implemented and committed to portal DEV</criterion>
    <criterion id="3">periodToChartWindow() maps mtd->MTD, qtd->QTD, ytd->YTD (no fallbacks)</criterion>
    <criterion id="4">ChartWindowOption union includes 'MTD' | 'QTD' | 'YTD' alongside existing trailing windows</criterion>
    <criterion id="5">pod_inventory.xml updated after RD WS4 commit</criterion>
    <criterion id="6">All changes on portal DEV (not CLOUD parent repo)</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>All portal changes commit to portal DEV, not CLOUD parent repo</constraint>
    <constraint>Do not commit API functions before DT confirms WS3d deploy (endpoints must be live)</constraint>
    <constraint>Reuse existing MixTimeseriesPoint type — do not duplicate it</constraint>
    <constraint>Keep existing ChartWindowOption values (3M, 6M, 1Y, 2Y, 3Y) — only add MTD/QTD/YTD</constraint>
    <constraint>No emojis anywhere (CLAUDE.md rule 13)</constraint>
    <constraint>Use 0.4.0_DE_ClientPlatform as git author on all commits</constraint>
  </constraints>

  <dependencies>
    <dependency agent="0.4.0_DT_ClientPlatform" task="ADVI_MVP318.002 req 4" status="pending">
      opal-partners-data deployed at partners-api-v1.4.0 — gate for WS3e API functions commit
    </dependency>
    <dependency agent="0.4.2_RD_AdvisorIntelligence" task="ADVI_MVP318.005 WS4" status="pending">
      ConsolidatedOverviewPanel all levels committed to portal DEV — gate for pod_inventory update
    </dependency>
  </dependencies>

  <deliverables>
    <deliverable type="commit">Advisor types + API functions committed to portal DEV</deliverable>
    <deliverable type="commit">periodToChartWindow + ChartWindowOption updated in portal DEV</deliverable>
    <deliverable type="commit">pod_inventory.xml updated (after RD WS4 complete)</deliverable>
  </deliverables>
</task_order>
