<task_order>
  <metadata>
    <id>1.0.0_SA_CTO-2026-03-23-mvplvl-009-de</id>
    <issued_by>1.0.0_SA_CTO</issued_by>
    <issued_to>0.4.0_DE_ClientPlatform</issued_to>
    <date>2026-03-23</date>
    <status>pending</status>
    <project_code>ADVI_MVPLVL</project_code>
  </metadata>

  <objective>
    Two views in AdvisorIntelligence are completely non-functional despite all
    upstream projects (GLDPRE, BKSCMP, CLSPT2, MIXV2) being marked complete.
    Andrew confirmed on 2026-03-23 that these do not load at any drill level.
    This task order requires a full end-to-end trace from gold layer output
    through Lambda through TypeScript through frontend component, identifying
    every break in the chain and fixing it.

    The two broken views:

    1. ASSETS OVERVIEW "Mix" toggle — the AUA stacked bar in the header panel
       has an "AUA" toggle (default) and a "Mix" toggle. Mix does not display.
       It must show asset class breakdown (equity, fixed income, alternatives,
       other) in THE EXACT SAME stacked bar format and structure as the
       NMEC/NMNC stacked bars in the "Clients" toggle. Same coloring and
       labeling as CMA taxonomy. "Other" = residual not assigned to the three
       named classes (will primarily be cash).

    2. BOOKS TAB "Asset Mix" + "Top Holdings" — the Overview panels at the top
       of the /books route do not load at any drill level (firm, advisor,
       relationship). Two components are expected:
       (a) Asset Mix radial (donut/pie) showing asset class breakdown
       (b) Top Holdings horizontal bars showing top 9 securities + "Other"
           (everything else collapsed)

       CRITICAL interaction: clicking an asset class segment in the radial
       must filter the Top Holdings view to show the top 9 holdings WITHIN
       THAT CLASS + Other (remaining holdings in that class). Example: if user
       clicks "Fixed Income" in the radial and there are 20 FI holdings, show
       the top 9 by market value + "Other" as the sum of the remaining 11.
       If there are only 3 FI holdings, show all 3 (no "Other" needed). The
       overall top-10 ranking across all classes is IRRELEVANT to per-class
       drill — what matters is top-9 within the selected class.
  </objective>

  <context>
    DEFINITIONS (use consistently across all agents):
    - "Mix" = breakdown by ASSET CLASS (equity, fixed income, alternatives, other)
    - "Concentration" = breakdown by SECURITY (individual holdings ranked by MV)

    DATA SOURCES (gold layer):
    - Script 06b (06b_build_client_mix_timeseries.py) -> firm_mix_views.json,
      per-advisor mix.json, client_mix_timeseries parquet. Uses ETFClassifier
      for 4-class taxonomy (equity, fixed_income, alternatives, cash-as-residual).
    - Script 12 (12_build_composition_artifacts.py) -> firm_composition.json,
      per-advisor composition.json. Contains BOTH asset mix (radial) AND
      top holdings (concentration bars) per class. Uses ETFClassifier.

    LAMBDA ROUTES (opal-partners-data, partners-api-v1.8.0):
    - GET /api/scoped/partners/books/firm/mix-views -> handle_firm_mix_views()
      S3: gold/firm_mix_views.json
    - GET /api/scoped/partners/books/advisor/{id}/mix -> handle_advisor_mix_views()
      S3: gold/advisors/{id}/mix.json
    - GET /api/scoped/partners/books/firm/all/composition -> handle_firm_composition()
      S3: gold/views/firm_composition.json (no-store cache)
    - GET /api/scoped/partners/books/advisor/{id}/composition -> handle_advisor_composition()
      S3: gold/advisors/{id}/composition.json (no-store cache)
    - GET /api/scoped/partners/books/relationship/{id}/composition -> handle_books_composition()
      Computes from holdings parquet at request time (not pre-computed)
    - GET /api/scoped/partners/books/account/{id}/composition -> handle_books_composition()
      Same as relationship — computes from holdings

    PORTAL TYPES (portal/src/pages/AdvisorIntelligence/types.ts):
    - FirmMixViewsResponse, FirmMixPeriodPoint, FirmMixClassValue (lines 1336-1367)
    - AdvisorMixTimeseriesResponse, MixTimeseriesPoint (lines 1390+)
    - BooksCompositionResponse, MixItem (lines 1283-1292, 1265)
    - AuaMixView, AuaMixPoint, AuaMixSegment (lines 1141-1157)
    - MixAssetClass = 'equity' | 'fixed_income' | 'alternatives' | 'cash' (line 1308)

    PORTAL COMPONENTS:
    - PartnerAnalytics.tsx — Assets Overview header panel (AUA / Clients / Mix toggles)
    - ClientsTab.tsx — Books tab with Overview panels
    - AUACompositionChart.tsx — composition chart component
    - DistributionTab.tsx — has mix-related rendering
  </context>

  <scope>
    <pages>
      <page>portal/src/pages/AdvisorIntelligence/</page>
    </pages>
    <files>
      <!-- Investigation targets — read and trace, fix where broken -->
      <!-- Gold layer (DS verifies data exists on S3) -->
      <file action="verify">data/black_diamond/scripts/gold/06b_build_client_mix_timeseries.py</file>
      <file action="verify">data/black_diamond/scripts/gold/12_build_composition_artifacts.py</file>
      <!-- Lambda (DS/AE verifies routes serve data) -->
      <file action="verify">infra/aws/lambda/v2_portal/partners/lambdas/opal-partners-data/lambda_function.py</file>
      <!-- Portal (DE/RD traces API calls through to components) -->
      <file action="modify">portal/src/pages/AdvisorIntelligence/types.ts</file>
      <file action="modify">portal/src/pages/AdvisorIntelligence/components/PartnerAnalytics.tsx</file>
      <file action="modify">portal/src/pages/AdvisorIntelligence/tabs/ClientsTab.tsx</file>
      <file action="modify">portal/src/pages/AdvisorIntelligence/components/AUACompositionChart.tsx</file>
    </files>
  </scope>

  <requirements>
    <!-- ============================================================ -->
    <!-- PHASE 1: Data verification (DS + AE)                         -->
    <!-- Confirm the precomputed JSONs exist on S3 and are well-formed -->
    <!-- ============================================================ -->

    <requirement id="1">
      DS: Verify gold layer output exists on S3 and contains expected shape.

      Check firm_mix_views.json:
        aws s3 cp s3://opal-data-bd/gold/firm_mix_views.json - | python3 -c "
        import json,sys; d=json.load(sys.stdin)
        for g in ['quarterly','monthly','annually']:
            pts = d['views'][g]
            print(f'{g}: {len(pts)} periods')
            if pts: print(f'  last: {pts[-1][\"period\"]} classes={[k for k in pts[-1] if k not in (\"period\",\"label\",\"end_date\",\"total_aua\")]}')"

      Check firm_composition.json:
        aws s3 cp s3://opal-data-bd/gold/views/firm_composition.json - | python3 -c "
        import json,sys; d=json.load(sys.stdin)
        print(f'classes: {len(d.get(\"mix\",[]))}')
        for m in d.get('mix',[]):
            print(f'  {m[\"asset_class\"]}: {len(m.get(\"top_holdings\",[]))} top holdings, mv={m.get(\"market_value\",0):,.0f}')
        print(f'global top: {len(d.get(\"top_holdings\",[]))} holdings')"

      Check at least one advisor has both files:
        aws s3 ls s3://opal-data-bd/gold/advisors/ --recursive | grep -E '(mix\.json|composition\.json)' | head -10

      Report: which files exist, which are missing, and the shape of each.
    </requirement>

    <requirement id="2">
      AE: Verify Lambda routes return data (not 404/500).

      Test from CLI (or browser dev tools network tab):
        curl the following endpoints (substitute real firmId):
        - /api/scoped/partners/books/firm/mix-views?firmId=49financial
        - /api/scoped/partners/books/firm/all/composition?firmId=49financial
        - /api/scoped/partners/books/advisor/{sample_id}/mix?firmId=49financial
        - /api/scoped/partners/books/advisor/{sample_id}/composition?firmId=49financial
        - /api/scoped/partners/books/relationship/{sample_id}/composition?firmId=49financial

      Report: HTTP status, response shape, any errors in CloudWatch.
    </requirement>

    <!-- ============================================================ -->
    <!-- PHASE 2: Frontend trace (DE + RD)                            -->
    <!-- Trace from API call through TypeScript to rendered component  -->
    <!-- ============================================================ -->

    <requirement id="3">
      DE: Trace the API fetch chain for BOTH views.

      For Mix in Assets Overview:
      - Identify which component calls the mix endpoint
      - Trace the response through TypeScript types to the stacked bar renderer
      - Confirm the data shape from Lambda matches what the component expects
      - If the fetch is missing, conditional is wrong, or types don't align — fix it

      For Asset Mix + Top Holdings in Books Overview:
      - Identify which component calls the composition endpoint at each drill level
      - Trace through TypeScript types to the radial chart and horizontal bars
      - Confirm the per-class drill interaction (click class -> filter holdings)
      - If the fetch is missing, conditional is wrong, or types don't align — fix it
    </requirement>

    <requirement id="4">
      RD: Once DE confirms the data path, verify visual rendering.

      Assets Overview Mix:
      - Must render as stacked bar chart, IDENTICAL format to NMEC/NMNC in Clients
      - Labels: Equity, Fixed Income, Alternatives, Other
      - Colors: match existing CMA color scheme used elsewhere in AdvisorIntelligence
      - Aggregate numbers must tie — sum of class values = total AUA for each period

      Books Overview Asset Mix:
      - Radial (donut/pie) chart with class segments
      - Same labels and colors as above
      - Click interaction: selecting a class segment filters Top Holdings

      Books Overview Top Holdings:
      - Horizontal bars, top 9 holdings by market value + "Other" (10th bar = remainder)
      - Default: global top 9 across all classes
      - When a class is selected in the radial: top 9 within that class only
      - If fewer than 10 holdings exist in the selected class, show all (no "Other" bar)
      - Each bar shows: security name/ticker, market value, percentage of class total
    </requirement>

    <!-- ============================================================ -->
    <!-- PHASE 3: Fix and deploy                                      -->
    <!-- ============================================================ -->

    <requirement id="5">
      Based on Phase 1 + 2 findings, fix every break in the chain:
      - If S3 data is missing or malformed: DS fixes the gold script, AE reruns
      - If Lambda route is broken or returning wrong shape: DS fixes, DT deploys
      - If TypeScript types don't match Lambda response: DE fixes types
      - If frontend component has wrong conditional, missing fetch, or rendering bug: DE/RD fix
      - If API endpoint is not wired in the frontend API layer: DE wires it

      Every fix must be committed to the appropriate branch (CLOUD for backend,
      portal DEV for frontend).
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">Assets Overview "Mix" toggle renders stacked bar chart at firm level with equity, fixed income, alternatives, other — same format as NMEC/NMNC in Clients</criterion>
    <criterion id="2">Books tab Overview "Asset Mix" radial renders at firm level</criterion>
    <criterion id="3">Books tab Overview "Asset Mix" radial renders at advisor level</criterion>
    <criterion id="4">Books tab Overview "Asset Mix" radial renders at relationship level</criterion>
    <criterion id="5">Books tab Overview "Top Holdings" renders top 9 + Other at firm level</criterion>
    <criterion id="6">Books tab Overview "Top Holdings" renders top 9 + Other at advisor level</criterion>
    <criterion id="7">Books tab Overview "Top Holdings" renders top 9 + Other at relationship level</criterion>
    <criterion id="8">Clicking a class in the Asset Mix radial filters Top Holdings to that class's top 9 + Other</criterion>
    <criterion id="9">If a class has fewer than 10 holdings, all are shown without an "Other" bar</criterion>
    <criterion id="10">Colors and labels match CMA taxonomy: Equity, Fixed Income, Alternatives, Other</criterion>
    <criterion id="11">Mix stacked bar aggregate numbers tie to total AUA per period</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Do NOT assume data is missing — verify on S3 first. The gold rerun completed 2026-03-20 evening.</constraint>
    <constraint>Do NOT create new gold scripts or Lambda routes. The infrastructure exists (scripts 06b + 12, Lambda routes deployed at partners-api-v1.8.0). The break is likely in the frontend wiring or a Lambda route mismatch.</constraint>
    <constraint>"Other" in the Mix context = residual AUA not assigned to equity, fixed income, or alternatives. This will primarily be cash. Do not add "Cash" as a separate visual label — use "Other".</constraint>
    <constraint>Mix stacked bar MUST follow the exact same data processing pattern as NMEC/NMNC Clients stacked bar — same conditionals, same aggregation rules, same shape. If Clients works, Mix must work the same way.</constraint>
    <constraint>Per-class Top Holdings drill is filtered WITHIN the class, not from the global top list. A holding ranked #50 globally but #1 in Fixed Income MUST appear as the top FI holding.</constraint>
    <constraint>Commit with appropriate --author for each agent's work.</constraint>
    <constraint>No emojis in code (CLAUDE.md rule 13).</constraint>
  </constraints>

  <dependencies>
    <dependency agent="none" status="clear">
      All upstream infrastructure is deployed and operational:
      - Gold scripts 06b + 12 run nightly (last full run 2026-03-20 evening)
      - Lambda partners-api-v1.8.0 deployed with all composition + mix routes
      - ETFClassifier has 3,855 securities in bd-securities DynamoDB
      - Portal types exist in types.ts for all response shapes
      No blockers. This is a wiring/rendering fix, not a new feature.
    </dependency>
  </dependencies>

  <deliverables>
    <deliverable type="document">Phase 1 trace report: which S3 files exist, which Lambda routes return data, where the chain breaks</deliverable>
    <deliverable type="commit">All fixes committed (CLOUD for backend, portal DEV for frontend)</deliverable>
    <deliverable type="verify">Visual confirmation that both views render at all drill levels</deliverable>
  </deliverables>
</task_order>
