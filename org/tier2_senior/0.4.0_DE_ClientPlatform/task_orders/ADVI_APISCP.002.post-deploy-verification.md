<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-03-10-post-deploy-verification</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DE_ClientPlatform</issued_to>
    <date>2026-03-10</date>
    <status>pending</status>
    <phase>2</phase>
  </metadata>

  <objective>
    Complete the post-deploy browser verification for ADVI_APISCP (Phase 1 requirement 4,
    previously blocked on DT Lambda@Edge v4 deploy). DT has deployed v4 and CloudFront
    propagation is complete. Verify that all advisor-intelligence scoped requests return
    fresh data from the correct origin.
  </objective>

  <scope>
    <files>
      <!-- No files to modify. Verification only. -->
    </files>
  </scope>

  <requirements>
    <requirement id="1">
      Load the AdvisorIntelligence page in dev browser (port 5175).
      Open Network tab in DevTools. Confirm:
      - All /api/scoped/advisor-intelligence/*.json responses return HTTP 200
      - Response payloads contain data_as_of matching current gold date
      - No requests hit opal-data-portal-v2 (check response headers / X-Cache)
    </requirement>
    <requirement id="2">
      Specifically verify these endpoints:
      - timeseries_chart.json
      - clients_tab.json
      - architect_leaderboard.json
      - partner_analytics/header_metrics_quarterly.json
      - snapshots/aua_by_architect.json (or any snapshot file)
      All must return valid JSON with current data.
    </requirement>
    <requirement id="3">
      If any endpoint fails (403, 404, stale data), document which endpoint and the
      exact error. Escalate to DT immediately — do not attempt to fix Lambda@Edge.
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">All scoped advisor-intelligence endpoints return HTTP 200 with current data</criterion>
    <criterion id="2">No requests route to opal-data-portal-v2</criterion>
    <criterion id="3">Verification documented in session log</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>This is verification only. Do not modify any files.</constraint>
    <constraint>Portal must be running locally: bun run dev --port 5175</constraint>
  </constraints>

  <dependencies>
    <dependency agent="0.4.0_DT_ClientPlatform" task="ADVI_APISCP.001.lambda-edge-v4-dynamic-routing" status="complete"/>
  </dependencies>

  <references>
    <ref type="prd">docs/architecture/ADVI_APISCP_PRD.md (acceptance criteria 1-2)</ref>
    <ref type="task_order">ADVI_APISCP.001.endpoint-mapping-docs-audit.md (requirement 4)</ref>
  </references>

  <deliverables>
    <deliverable type="document">Session log with verification results (pass/fail per endpoint)</deliverable>
  </deliverables>
</task_order>
