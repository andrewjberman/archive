<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-03-10-cors-response-headers-policy</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <date>2026-03-10</date>
    <status>complete</status>
    <phase>4</phase>
  </metadata>

  <objective>
    OPTIONS preflight returns 200 with no CORS headers, which causes browsers to block
    the subsequent GET. Root cause: auth-validator-edge (viewer-request) intercepts OPTIONS
    before it reaches S3, so S3's CORS config is never invoked for preflight.

    DO NOT modify shared-advisor-router. The fix is a CloudFront Response Headers Policy
    on the /api/scoped/advisor-intelligence/*.json behavior. A Response Headers Policy
    is applied by CloudFront to ALL outbound responses from the behavior AFTER Lambda@Edge
    executes -- including 200, 401, 403, and OPTIONS synthetic responses. This covers the
    preflight case without any code change.

    This is a CloudFront config change only. No Lambda@Edge work.
  </objective>

  <scope>
    <files>
      <!-- AWS CLI only. No Terraform. No code changes. -->
    </files>
  </scope>

  <requirements>
    <requirement id="1">
      Create a custom CloudFront Response Headers Policy:

        export MSYS_NO_PATHCONV=1
        python -m awscli cloudfront create-response-headers-policy \
          --response-headers-policy-config '{
            "Name": "opal-scoped-advisor-cors",
            "CorsConfig": {
              "AccessControlAllowOrigins": {
                "Quantity": 1,
                "Items": ["*"]
              },
              "AccessControlAllowHeaders": {
                "Quantity": 2,
                "Items": ["Authorization", "Content-Type"]
              },
              "AccessControlAllowMethods": {
                "Quantity": 3,
                "Items": ["GET", "HEAD", "OPTIONS"]
              },
              "AccessControlExposeHeaders": {
                "Quantity": 2,
                "Items": ["ETag", "x-amz-version-id"]
              },
              "AccessControlMaxAgeSec": 3000,
              "OriginOverride": false
            }
          }' 2>/dev/null

      Record the ResponseHeadersPolicyId from the output.

      NOTE: OriginOverride: false means if S3 already returns CORS headers,
      CloudFront does NOT override them. If S3 returns no CORS headers (e.g. on
      a 401/403 synthetic response), CloudFront injects them. This is correct
      behavior for all cases.
    </requirement>
    <requirement id="2">
      Attach the Response Headers Policy to the behavior.

        a. Get current distribution config + ETag:
             python -m awscli cloudfront get-distribution-config \
               --id EVTSA9VEHNZVH --output json > /tmp/cf_rhp.json

        b. In CacheBehaviors.Items[] for PathPattern
           "/api/scoped/advisor-intelligence/*.json", set:
             ResponseHeadersPolicyId: "{policy ID from requirement 1}"

        c. Apply:
             python -m awscli cloudfront update-distribution \
               --id EVTSA9VEHNZVH \
               --distribution-config file:///tmp/cf_rhp_updated.json \
               --if-match {ETag}

        d. Wait for status Deployed.
    </requirement>
    <requirement id="3">
      Invalidate:
        python -m awscli cloudfront create-invalidation \
          --distribution-id EVTSA9VEHNZVH \
          --paths "/api/scoped/advisor-intelligence/*"
    </requirement>
    <requirement id="4">
      Verify both GET and OPTIONS now return CORS headers:

        CF="https://d2n2nzpeqf34ge.cloudfront.net"

        echo "=== GET (no JWT -- expect 401 + CORS headers) ==="
        curl -s -D - \
          -H "Origin: https://opalinvest.com" \
          "$CF/api/scoped/advisor-intelligence/timeseries_chart.json" \
          2>/dev/null | grep -iE "^HTTP|^access-control"

        echo "=== OPTIONS preflight ==="
        curl -s -D - -X OPTIONS \
          -H "Origin: https://opalinvest.com" \
          -H "Access-Control-Request-Method: GET" \
          -H "Access-Control-Request-Headers: authorization" \
          "$CF/api/scoped/advisor-intelligence/timeseries_chart.json" \
          2>/dev/null | grep -iE "^HTTP|^access-control"

      Both must return Access-Control-Allow-Origin: * in headers.
      GET may return 401 (no JWT in this test) -- that is correct.
      OPTIONS must return Access-Control-Allow-Headers including authorization.
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">Response Headers Policy opal-scoped-advisor-cors created and attached to behavior</criterion>
    <criterion id="2">GET with Origin header returns Access-Control-Allow-Origin: * (regardless of HTTP status)</criterion>
    <criterion id="3">OPTIONS preflight returns Access-Control-Allow-Origin: * and Access-Control-Allow-Headers: authorization</criterion>
    <criterion id="4">No changes to Lambda@Edge code or shared-advisor-router</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Do NOT modify shared-advisor-router -- the Response Headers Policy handles this entirely at the CloudFront layer.</constraint>
    <constraint>Do NOT modify any other CloudFront behavior. Only the /api/scoped/advisor-intelligence/*.json behavior.</constraint>
    <constraint>OriginOverride must be false -- do not override CORS headers that S3 returns correctly.</constraint>
    <constraint>export MSYS_NO_PATHCONV=1 before all AWS CLI calls.</constraint>
  </constraints>

  <dependencies>
    <dependency agent="0.7.0_AE_CloudOps" task="ADVI_APISCP.004.cors-opal-data-bd" status="complete"/>
  </dependencies>

  <references>
    <ref type="cloudops_finding">OPTIONS preflight returns 200 + no CORS headers (escalated from ADVI_APISCP.004)</ref>
    <ref type="aws_doc">CloudFront Response Headers Policy -- applied after Lambda@Edge, covers all response codes</ref>
  </references>

  <deliverables>
    <deliverable type="aws_config">CloudFront Response Headers Policy opal-scoped-advisor-cors created and attached</deliverable>
    <deliverable type="document">Session log with curl output showing Access-Control-Allow-Origin on both GET and OPTIONS</deliverable>
  </deliverables>
</task_order>
