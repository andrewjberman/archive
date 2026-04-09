# ADVI_NNAFEE.003 — DT: Phase 1 Deploy (Fee Efficiency Views)

<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-04-06-nnafee-003-dt</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DT_ClientPlatform</issued_to>
    <date>2026-04-06</date>
    <status>staged</status>
    <project_code>ADVI_NNAFEE</project_code>
    <priority>medium</priority>
    <phase>1</phase>
  </metadata>

  <objective>
    Push Phase 1 portal changes (fee efficiency endpoint + views) to portal DEV.
    Verify the scatter plot and ranked table render with live data from
    `advisor_fee_efficiency.json`.
  </objective>

  <context>
    Phase 1 adds fee efficiency views to the Books tab. DE (.001) wires the
    endpoint and types. RD (.002) builds scatter plot, ranked table, and
    drill-down components.

    No infrastructure changes needed -- the JSON is already served via the existing
    CloudFront wildcard behavior for `/api/scoped/advisor-intelligence/artifacts/*`.
  </context>

  <scope>
    ## 1. Pre-Deploy Validation

    - `bunx tsc -b` clean
    - Verify `advisor_fee_efficiency.json` is accessible at the expected S3 path
      (`gold/artifacts/advisor_fee_efficiency.json`)
    - Visual spot-check: scatter plot renders, table sorts, drill-down expands

    ## 2. Push to Portal DEV

    - Commit on portal `DEV` branch
    - Push to remote
    - Verify deployed portal loads the Books tab with new fee efficiency section

    ## 3. Verification

    - Scatter plot: dots render for ~155 advisors, regression line visible
    - Table: sortable by all columns, role/period filters work
    - Drill-down: advisor headline metrics display correctly
  </scope>

  <deliverables>
    <deliverable id="push">Portal DEV pushed with Phase 1 changes</deliverable>
    <deliverable id="verify">Visual verification of fee efficiency views with live data</deliverable>
  </deliverables>

  <dependencies>
    <dependency agent="0.4.0_DE_ClientPlatform" task="ADVI_NNAFEE.001" status="staged"/>
    <dependency agent="0.4.2_RD_AdvisorIntelligence" task="ADVI_NNAFEE.002" status="staged"/>
  </dependencies>
</task_order>
