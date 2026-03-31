<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-03-11-final-browser-verification</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DE_ClientPlatform</issued_to>
    <date>2026-03-11</date>
    <status>complete</status><!-- APISCP routing verified through subsequent portal work (GLDPRE, BKSCMP). Project closed 2026-03-10. -->
    <phase>4</phase>
  </metadata>

  <objective>
    Final browser verification for ADVI_APISCP. The full infrastructure chain is now live.
    This is the last acceptance criterion for the project. Confirm the Advisor Intelligence
    page loads correctly end-to-end in a real browser session with a valid 49 Financial JWT.
  </objective>

  <context>
    The following infrastructure is now fully deployed on CloudFront EVTSA9VEHNZVH:

    1. Lambda@Edge shared-advisor-router:5 (v6 code) — dynamic OAI routing + OPTIONS handler
       - OPTIONS preflight: returns 204 + CORS headers before X-Firm-Id guard
       - GET: reads X-Firm-Id from JWT-injected header, routes to opal-data-{firmId}/gold/
       - Tag: shared-advisor-router-v6 → d2b405b0

    2. OAI E139998VWH0PD wired to S3-opal-data-bd origin (replaces OAC)
       - opal-data-bd bucket policy grants OAI canonical user s3:GetObject
       - Lambda origin mutation works correctly with OAI (OAC bypass is resolved)

    3. Cache key policy opal-scoped-advisor-by-firm (45eb7514)
       - X-Firm-Id in cache key — firm A responses never served to firm B

    4. S3 CORS on opal-data-bd
       - AllowedOrigins: *, AllowedMethods: GET + HEAD

    5. CloudFront CORS-S3Origin origin request policy (b689b0a8)
       - Forwards Origin header to S3 for CORS evaluation

    6. CloudFront Response Headers Policy opal-scoped-advisor-cors (3570c5b4)
       - Adds Access-Control-Allow-Origin: * to all responses as safety net

    Previous blockers resolved:
    - OAC bypass: fixed by migrating to OAI
    - OPTIONS preflight: fixed by v6 Lambda OPTIONS early-return + RHP
    - Stale March 2 localStorage cache: cleared manually by Andrew
    - S3 had no CORS config: fixed in .004
    - Missing Origin Request Policy on CF behavior: fixed in .004

    DT verified OPTIONS → 204 + CORS headers live.
    COO curl verified GET (no browser) → 200 application/json, data_as_of: 2026-03-09.
    Browser verification with real JWT has NOT been done yet. That is this task.
  </context>

  <requirements>
    <requirement id="1">
      Run the portal locally: /c/Users/AndrewBerman/.bun/bin/bun run dev --port 5175
      from the portal/ directory. (Use 5175 not 5173 -- if 5173 is already running
      that is fine too, any port works since CORS is AllowedOrigins: *.)
    </requirement>
    <requirement id="2">
      Clear browser localStorage before loading the page. DevTools → Application →
      Local Storage → right-click origin → Clear. This removes any stale cache entries
      from before the infrastructure fixes. Hard refresh after clearing (Ctrl+Shift+R).
    </requirement>
    <requirement id="3">
      Log in with a valid 49 Financial user account and navigate to the
      Advisor Intelligence page.
    </requirement>
    <requirement id="4">
      Open DevTools Network tab. Verify the following endpoints all return
      HTTP 200 with Content-Type: application/json (NOT text/html):

        /api/scoped/advisor-intelligence/timeseries_chart.json
        /api/scoped/advisor-intelligence/clients_tab.json
        /api/scoped/advisor-intelligence/architect_leaderboard.json
        /api/scoped/advisor-intelligence/partner_analytics/header_metrics_quarterly.json
        /api/scoped/advisor-intelligence/snapshots/aua_by_architect.json

      For each response, confirm:
        - HTTP 200 (not 401, 403, or any HTML response)
        - Content-Type: application/json
        - Access-Control-Allow-Origin: * is present in response headers
        - Response body is valid JSON (not <!doctype html>)
    </requirement>
    <requirement id="5">
      Verify the page visually renders correctly:
        - Assets Overview header panel populates with AUA / NNA metrics
        - Distribution tab renders charts (not blank)
        - Advisors tab renders leaderboard
        - Clients tab renders data
      None of these should be blank or stuck in a loading state.
    </requirement>
    <requirement id="6">
      Confirm data_as_of is current. Check the Network response for
      timeseries_chart.json -- the data_as_of field should be 2026-03-09
      (the last BD pipeline run date). It must NOT be 2026-03-02 (that was
      the stale portal-v2 data).
    </requirement>
    <requirement id="7">
      If any endpoint returns HTML or fails CORS, escalate immediately with:
        - The exact endpoint URL
        - The HTTP status code
        - The response headers (especially Content-Type and any CORS headers)
        - The first 100 chars of the response body
      Do not attempt to fix Lambda@Edge or CloudFront yourself.
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">All 5 static endpoints return HTTP 200 application/json</criterion>
    <criterion id="2">Access-Control-Allow-Origin: * present on all responses</criterion>
    <criterion id="3">data_as_of: 2026-03-09 on timeseries_chart.json (not 2026-03-02)</criterion>
    <criterion id="4">Page visually renders: header panel, Distribution tab, Advisors tab, Clients tab all populated</criterion>
    <criterion id="5">No HTML responses anywhere in the advisor-intelligence Network requests</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Do not modify any portal code during this task. Verification only.</constraint>
    <constraint>If anything fails, escalate to COO with exact error details. Do not attempt infrastructure fixes.</constraint>
  </constraints>

  <dependencies>
    <!-- All infrastructure complete. No blocking dependencies. -->
  </dependencies>

  <references>
    <ref type="deploy_log">org/tier2_senior/0.4.0_DT_ClientPlatform/logs/2026-03-10/advi_apiscp_004_options_cors_v6_deploy.md</ref>
    <ref type="task_order">ADVI_APISCP.005.cors-response-headers-policy.md (CloudOps -- complete)</ref>
    <ref type="task_order">ADVI_APISCP.004.cors-opal-data-bd.md (CloudOps -- complete)</ref>
    <ref type="task_order">ADVI_APISCP.003.cloudfront-oai-wire-v5-deploy.md (DT -- complete)</ref>
  </references>

  <deliverables>
    <deliverable type="document">Session log with Network tab screenshots/output confirming all 5 endpoints pass</deliverable>
    <deliverable type="confirmation">data_as_of: 2026-03-09 confirmed in timeseries_chart.json response</deliverable>
    <deliverable type="confirmation">Visual page render confirmed (all panels populated)</deliverable>
  </deliverables>
</task_order>
