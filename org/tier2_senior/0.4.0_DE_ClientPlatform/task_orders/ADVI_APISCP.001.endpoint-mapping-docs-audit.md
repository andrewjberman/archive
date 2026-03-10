<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-03-10-endpoint-mapping-docs-audit</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DE_ClientPlatform</issued_to>
    <date>2026-03-10</date>
    <status>pending</status>
  </metadata>

  <objective>
    Update endpoint-mapping.ts documentation to accurately reflect the new scoped routing
    architecture after DT deploys Lambda@Edge v4. Audit frontend API calls for correctness.
    Ensure no frontend code references the eliminated opal-data-portal-v2/json/advisor-intelligence path.
  </objective>

  <scope>
    <files>
      <file action="modify">portal/src/api/endpoint-mapping.ts</file>
      <file action="modify">portal/src/api/endpoints/advisor-intelligence.ts</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">
      Fix the SCOPED comment in endpoint-mapping.ts (line 13). Currently says:
        /api/scoped/* -> S3 origin (s3://opal-data-portal-v2/json/) via shared-advisor-router
      Must be corrected to:
        /api/scoped/* -> S3 origin (s3://opal-data-{firmId}/gold/) via shared-advisor-router (dynamic per-firm)
    </requirement>
    <requirement id="2">
      Add a SCOPED category entry to ENDPOINT_MAPPING for advisor-intelligence endpoints,
      documenting the firm-scoped S3 routing. Currently advisor-intelligence has no entry in
      the mapping (it routes through shared-advisor-router, not through the mapping file).
      At minimum, add documentation comments that make the routing architecture explicit.
    </requirement>
    <requirement id="3">
      Audit advisor-intelligence.ts: confirm static file calls (timeseries_chart.json,
      clients_tab.json, partner_analytics/header_metrics_*.json, snapshots/*.json) route
      via CloudFront /api/scoped/ and do NOT include firmId query params (the router gets
      firmId from X-Firm-Id header, not query string). Dynamic dimension calls that go
      through API Gateway may use firmId param — confirm this separation is still correct.
    </requirement>
    <requirement id="4">
      After DT deploys, verify in browser DevTools Network tab that all advisor-intelligence
      responses show fresh data (data_as_of matching current gold date) and no requests hit
      opal-data-portal-v2.
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">endpoint-mapping.ts comments accurately describe SCOPED routing as
    per-firm S3 bucket (opal-data-{firmId}/gold/), not opal-data-portal-v2</criterion>
    <criterion id="2">No frontend code references opal-data-portal-v2/json/advisor-intelligence</criterion>
    <criterion id="3">bunx tsc -b passes</criterion>
    <criterion id="4">Post-deploy network tab verification confirms fresh data from correct origin</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Wait for DT to deploy Lambda@Edge v4 before doing the post-deploy verification (requirement 4). Requirements 1-3 can be done immediately.</constraint>
    <constraint>Do not modify any Lambda or infrastructure files — this is docs + audit only.</constraint>
  </constraints>

  <dependencies>
    <dependency agent="0.4.0_DT_ClientPlatform" task="ADVI_APISCP.001.lambda-edge-v4-dynamic-routing" status="pending"/>
  </dependencies>

  <references>
    <ref type="prd">docs/architecture/ADVI_APISCP_PRD.md</ref>
  </references>

  <deliverables>
    <deliverable type="commit">Updated endpoint-mapping.ts with correct SCOPED routing documentation</deliverable>
    <deliverable type="document">Session log with audit findings and post-deploy verification</deliverable>
  </deliverables>
</task_order>
