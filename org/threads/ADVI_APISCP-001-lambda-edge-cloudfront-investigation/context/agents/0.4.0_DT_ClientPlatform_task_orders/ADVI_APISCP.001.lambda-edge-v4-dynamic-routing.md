<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-03-10-lambda-edge-v4-dynamic-routing</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DT_ClientPlatform</issued_to>
    <date>2026-03-10</date>
    <status>pending</status>
  </metadata>

  <objective>
    Update the shared-advisor-router Lambda@Edge from v3 to v4 with dynamic S3 origin routing
    based on the X-Firm-Id header (already injected by auth-validator-edge from the JWT).
    Currently v3 hardcodes opal-data-bd as the origin. v4 must construct the S3 bucket as
    opal-data-{firmId} from the X-Firm-Id header, enabling automatic routing when partner 2
    onboards with zero code changes.
  </objective>

  <scope>
    <files>
      <file action="modify">infra/aws/lambda-edge/shared-advisor-router/index.mjs</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">
      Update infra/aws/lambda-edge/shared-advisor-router/index.mjs to v4:
      - Read X-Firm-Id from request.headers['x-firm-id'][0].value
      - If missing, return 403 with body "Missing firm identity"
      - Construct bucket: opal-data-{firmId}
      - Dynamically set request.origin.s3 to the constructed bucket
      - Retain existing URI rewrite: /api/scoped/advisor-intelligence/* -> /gold/*
      - Update version comment in file header to v4
      PRD Section 4 includes the exact pseudocode.
    </requirement>
    <requirement id="2">
      Verify CloudFront OAI (Origin Access Identity) has s3:GetObject on
      arn:aws:s3:::opal-data-*/*. If only opal-data-bd is granted, expand to wildcard.
      The OAI is on CloudFront distribution EVTSA9VEHNZVH.
    </requirement>
    <requirement id="3">
      Deploy the updated Lambda@Edge to us-east-1 (Lambda@Edge requirement).
      NOTE: CloudFront distribution EVTSA9VEHNZVH is NOT managed in Terraform.
      Lambda@Edge functions are NOT in lambda-source-map.json. The deployment mechanism
      for Lambda@Edge is separate from the standard Terraform Lambda pipeline.
      Confirm how the existing shared-advisor-router is deployed (console, script, or
      separate Terraform) before proceeding.
    </requirement>
    <requirement id="4">
      After deploy, invalidate /api/scoped/advisor-intelligence/* on CloudFront.
      Verify: curl with a valid JWT should return data from opal-data-bd/gold/ with
      data_as_of matching current gold date.
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">GET /api/scoped/advisor-intelligence/timeseries_chart.json with a
    49 Financial JWT returns data from opal-data-bd/gold/ (data_as_of: current gold date)</criterion>
    <criterion id="2">Lambda@Edge code reads X-Firm-Id and constructs origin dynamically
    (no hardcoded bucket name)</criterion>
    <criterion id="3">Request without X-Firm-Id returns 403</criterion>
    <criterion id="4">CloudFront OAI allows s3:GetObject on opal-data-*/*</criterion>
    <criterion id="5">0-diff plan (if Terraform-managed) or equivalent verification</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Lambda@Edge must be deployed to us-east-1. Confirm deployment mechanism before modifying.</constraint>
    <constraint>Do not modify auth-validator-edge — it already correctly injects X-Firm-Id.</constraint>
    <constraint>shared-advisor-router is an origin-request trigger. Dynamic origin mutation is valid only in origin-request phase — this is already correct.</constraint>
    <constraint>CloudFront propagation takes 5-15 minutes. Wait for propagation before verification.</constraint>
    <constraint>Never write partner data to opal-data-portal-v2. This anti-pattern was eliminated 2026-03-10 and must never be recreated.</constraint>
  </constraints>

  <dependencies>
    <!-- No blocking dependencies. DT can proceed immediately. -->
  </dependencies>

  <references>
    <ref type="prd">docs/architecture/ADVI_APISCP_PRD.md</ref>
    <ref type="source">infra/aws/lambda-edge/shared-advisor-router/index.mjs (current v3)</ref>
    <ref type="source">infra/aws/lambda-edge/auth-validator-edge/index.mjs (injects X-Firm-Id)</ref>
  </references>

  <deliverables>
    <deliverable type="commit">Updated shared-advisor-router/index.mjs v4</deliverable>
    <deliverable type="document">Session log documenting deployment steps and verification</deliverable>
  </deliverables>
</task_order>
