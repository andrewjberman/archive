<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-03-26-mvplvl-010-de</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DE_ClientPlatform</issued_to>
    <date>2026-03-26</date>
    <status>complete</status>
    <project_code>ADVI_MVPLVL</project_code>
  </metadata>

  <objective>
    L2 advisor composition (Asset Mix + Top Holdings) does not render in the
    Books tab at the "Advisor's Book" drill level. DS diagnostic confirmed all
    20 advisor composition.json artifacts exist on S3 with correct keys,
    well-formed JSON, and the Lambda handler is deployed (partners-api-v1.9.0).

    The issue is portal-side. Investigate and fix the rendering failure.
  </objective>

  <context>
    DS diagnostic (ADVI_MVPLVL.010, 2026-03-26) confirmed:
    - 20 advisor composition.json files on S3 (gold/advisors/{advisor_id}/composition.json)
    - JSON schema: mix[], top_holdings[], scope.advisor_id, total_market_value
    - Sanitization aligned between Python _advisor_id() and TypeScript handleSelectAdvisor
    - Lambda handle_advisor_composition at line 1104 reads the correct S3 key
    - Route: action == 'composition' and entity_type == 'advisor'

    The same CanonicalBookView and ConsolidatedOverviewPanel render correctly
    at N1 (firm) and L3 (client relationship). The L2 path fails silently.

    Key files:
    - portal/src/pages/AdvisorIntelligence/tabs/ClientsTab.tsx
    - portal/src/api/endpoints/advisor-intelligence.ts
    - portal/src/pages/AdvisorIntelligence/types.ts

    DS session log: org/tier2_senior/0.4.0_DS_ClientPlatform/logs/2026-03-26/
      advi_mvplvl_010_l2_mix_tax_diagnostic.md
  </context>

  <scope>
    <pages>
      <page>portal/src/pages/AdvisorIntelligence/</page>
    </pages>
    <files>
      <file action="modify">portal/src/pages/AdvisorIntelligence/tabs/ClientsTab.tsx</file>
      <file action="modify">portal/src/api/endpoints/advisor-intelligence.ts</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">
      Trace the L2 composition data flow end-to-end:

      Step 1a: In ClientsTab.tsx, find getBooksAdvisorComposition() (called at
      line ~386-400 when selectedAdvisorId is set). Verify:
        - The advisorId being passed matches the S3 key format (lowercase, underscores)
        - The endpoint URL constructed is correct (/api/scoped/partners/books/advisor/{id}/composition)
        - The firmId query parameter is correct

      Step 1b: Check the .catch() fallback at lines ~391-398. When the API
      call fails or returns unexpected shape, it falls back to
      synthesizeFromAssetAllocation(). Determine:
        - Is the API call actually failing? (Add console.log or check network tab)
        - Or is the response coming back but being rejected by the type/shape check?
        - Is synthesizeFromAssetAllocation() producing a valid BooksCompositionResponse?

      Step 1c: Check normalizeMixTo4Class() if it exists. Script 12 may return
      asset classes including 'other' and 'cash' separately. The portal 4-class
      taxonomy (equity, fixed_income, alternatives, cash) may not match script 12's
      5-class output (equity, fixed_income, alternatives, cash, other). If
      normalizeMixTo4Class() drops 'other' or mishandles it, the composition
      will render incomplete.
    </requirement>

    <requirement id="2">
      Fix the rendering failure. The composition data exists and the Lambda
      serves it. The fix is in the portal code:

      - If the API call itself is failing: fix the URL construction or error handling
      - If the response shape doesn't match BooksCompositionResponse: fix the type
        adapter or normalization
      - If normalizeMixTo4Class() is dropping data: merge 'other' into the appropriate
        bucket (script 12 uses 'other' for unclassified non-cash items)
      - If synthesizeFromAssetAllocation() is the problem: ensure it produces a shape
        that ConsolidatedOverviewPanel can render

      The fix should make L2 render the same way N1 does -- mix donut with per-class
      breakdown and top holdings table.
    </requirement>

    <requirement id="3">
      Also investigate the PartnerAnalytics Mix toggle. The firm_mix_views.json
      is confirmed rich (24 quarterly, 69 monthly, 7 annual periods) but the
      Mix toggle may not be rendering correctly.

      In PartnerAnalytics.tsx:
      - The Mix chart reads from firmMixChartData (line 1536-1540)
      - firmMixChartData is derived from firmMixViews?.views[auaGranularity] (line 391-409)
      - getFirmMixViews() calls /api/scoped/partners/books/firm/all/mix-views

      Verify:
      - Does the API call succeed? (firm_mix_views.json exists and is served correctly)
      - Does the response match FirmMixViewsResponse type?
      - Does firmMixChartData actually populate with data?
      - If the chart shows "Asset class mix data unavailable" (line 1627), trace why
        firmMixChartData.length === 0
    </requirement>

    <requirement id="4">
      Commit fixes to portal DEV. Author: 0.4.0_DE_ClientPlatform.
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">L2 advisor composition (mix donut + top holdings) renders in Books tab when an advisor is selected</criterion>
    <criterion id="2">PartnerAnalytics Mix toggle renders the stacked bar chart with asset class breakdown</criterion>
    <criterion id="3">Portal DEV commit with fix</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Do NOT modify gold scripts or Lambda code -- data layer is correct</constraint>
    <constraint>Do NOT modify the BooksCompositionResponse type to remove fields -- adapt the rendering to handle the actual shape</constraint>
    <constraint>The 'other' asset class from script 12 should be merged into display -- do not silently drop it</constraint>
  </constraints>

  <dependencies>
    <dependency agent="0.4.0_DS_ClientPlatform" task="ADVI_MVPLVL.010" status="complete">
      DS confirmed all S3 artifacts exist, Lambda handler deployed.
    </dependency>
  </dependencies>

  <deliverables>
    <deliverable type="commit">Portal DEV commit fixing L2 composition rendering</deliverable>
    <deliverable type="commit">Portal DEV commit fixing PartnerAnalytics Mix toggle (if separate issue)</deliverable>
  </deliverables>
</task_order>
