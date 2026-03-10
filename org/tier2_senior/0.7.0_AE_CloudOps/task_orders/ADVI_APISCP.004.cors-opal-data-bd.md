<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-03-10-cors-opal-data-bd</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <date>2026-03-10</date>
    <status>pending</status>
    <phase>4</phase>
  </metadata>

  <objective>
    The Advisor Intelligence page is blank in the browser. Root cause confirmed by COO:
    opal-data-bd has no CORS configuration and the CloudFront behavior has no Origin
    Request Policy. Browsers send an Origin header on cross-origin fetches; without CORS
    headers in the response, the browser blocks every response silently.

    opal-data-portal-v2 had a CORS config (AllowedOrigins: *) which is why the old
    routing worked in the browser. That config was never mirrored to opal-data-bd when
    routing migrated. This is the sole reason nothing loads on the page.

    Two fixes required:
      1. Add S3 CORS configuration to opal-data-bd
      2. Add AWS managed CORS-S3Origin origin request policy to the CloudFront behavior
         so Origin header is forwarded from CloudFront to S3
  </objective>

  <scope>
    <files>
      <!-- AWS CLI only. No Terraform. No code changes. -->
    </files>
  </scope>

  <requirements>
    <requirement id="1">
      Add CORS configuration to opal-data-bd. Mirror the config from opal-data-portal-v2:

        export MSYS_NO_PATHCONV=1
        python -m awscli s3api put-bucket-cors \
          --bucket opal-data-bd \
          --region us-east-1 \
          --cors-configuration '{
            "CORSRules": [{
              "AllowedHeaders": ["*"],
              "AllowedMethods": ["GET", "HEAD"],
              "AllowedOrigins": ["*"],
              "ExposeHeaders": ["ETag", "x-amz-version-id"],
              "MaxAgeSeconds": 3000
            }]
          }'

      Verify it was applied:
        python -m awscli s3api get-bucket-cors --bucket opal-data-bd --region us-east-1
    </requirement>
    <requirement id="2">
      Add the AWS managed CORS-S3Origin origin request policy to the
      /api/scoped/advisor-intelligence/*.json CloudFront behavior.

      Managed policy ID: b689b0a8-53d0-40ab-baf2-68738e2966ac
      (Name: "CORS-S3Origin" -- forwards Origin, Access-Control-Request-Headers,
       Access-Control-Request-Method to the S3 origin so S3 can evaluate CORS rules)

      Steps:
        a. Get current distribution config + ETag:
             python -m awscli cloudfront get-distribution-config \
               --id EVTSA9VEHNZVH --output json > /tmp/cf_cors.json

        b. In the CacheBehaviors.Items[] entry for PathPattern
           "/api/scoped/advisor-intelligence/*.json", set:
             OriginRequestPolicyId: "b689b0a8-53d0-40ab-baf2-68738e2966ac"

        c. Apply:
             python -m awscli cloudfront update-distribution \
               --id EVTSA9VEHNZVH \
               --distribution-config file:///tmp/cf_cors_updated.json \
               --if-match {ETag}

        d. Wait for status Deployed.
    </requirement>
    <requirement id="3">
      Invalidate to clear any cached non-CORS responses:
        python -m awscli cloudfront create-invalidation \
          --distribution-id EVTSA9VEHNZVH \
          --paths "/api/scoped/advisor-intelligence/*"
    </requirement>
    <requirement id="4">
      Verify with curl that CORS headers are now present:

        export MSYS_NO_PATHCONV=1
        curl -s -D - \
          -H "Authorization: Bearer {valid-jwt}" \
          -H "Origin: https://opalinvest.com" \
          "https://d2n2nzpeqf34ge.cloudfront.net/api/scoped/advisor-intelligence/timeseries_chart.json" \
          2>/dev/null | grep -iE "^access-control|^HTTP"

      Expected: HTTP 200 + Access-Control-Allow-Origin: * in response headers.

      Also verify OPTIONS preflight:
        curl -s -D - -X OPTIONS \
          -H "Origin: https://opalinvest.com" \
          -H "Access-Control-Request-Method: GET" \
          -H "Access-Control-Request-Headers: authorization" \
          "https://d2n2nzpeqf34ge.cloudfront.net/api/scoped/advisor-intelligence/timeseries_chart.json" \
          2>/dev/null | grep -iE "^access-control|^HTTP"

      Expected: HTTP 200 (or 204) + Access-Control-Allow-Origin + Access-Control-Allow-Headers.
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">opal-data-bd bucket has CORS config (AllowedOrigins: *, GET + HEAD)</criterion>
    <criterion id="2">CloudFront behavior has OriginRequestPolicyId: b689b0a8-53d0-40ab-baf2-68738e2966ac</criterion>
    <criterion id="3">curl with Origin header returns Access-Control-Allow-Origin: * on GET response</criterion>
    <criterion id="4">OPTIONS preflight returns CORS headers allowing Authorization header</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Do NOT change AllowedOrigins to anything other than ["*"] without CTO approval. The portal origin may vary (local dev, staging, prod).</constraint>
    <constraint>Do NOT modify any other CloudFront behavior. Only the /api/scoped/advisor-intelligence/*.json behavior.</constraint>
    <constraint>export MSYS_NO_PATHCONV=1 before all AWS CLI calls.</constraint>
    <constraint>This is AWS CLI only. No Terraform changes needed.</constraint>
  </constraints>

  <dependencies>
    <!-- No blocking dependencies. Proceed immediately. -->
  </dependencies>

  <references>
    <ref type="diagnosis">opal-data-portal-v2 CORS config (reference): AllowedOrigins *, GET/HEAD/PUT, AllowedHeaders *, ExposeHeaders ETag + x-amz-version-id</ref>
    <ref type="aws_doc">AWS managed origin request policy CORS-S3Origin: b689b0a8-53d0-40ab-baf2-68738e2966ac</ref>
  </references>

  <deliverables>
    <deliverable type="aws_config">opal-data-bd S3 CORS configuration applied</deliverable>
    <deliverable type="aws_config">CloudFront behavior OriginRequestPolicyId set to CORS-S3Origin</deliverable>
    <deliverable type="document">Session log with curl verification output showing Access-Control-Allow-Origin present</deliverable>
  </deliverables>
</task_order>
