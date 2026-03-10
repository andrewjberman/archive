<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-03-10-lambda-edge-v4-dynamic-routing</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DT_ClientPlatform</issued_to>
    <date>2026-03-10</date>
    <revised>2026-03-10 (post-thread ADVI_APISCP-001)</revised>
    <status>pending</status>
  </metadata>

  <objective>
    Update the shared-advisor-router Lambda@Edge from v3 to v4 with dynamic S3 origin routing
    based on the X-Firm-Id header (already injected by auth-validator-edge from the JWT).
    Currently v3 hardcodes opal-data-bd as the origin. v4 must construct the S3 bucket as
    opal-data-{firmId} from the X-Firm-Id header, enabling automatic routing when partner 2
    onboards with zero code changes.

    REVISED: Thread ADVI_APISCP-001 (Pattern 2 investigation with CloudOps) identified three
    corrections to the original PRD assumptions. This task order incorporates those findings.
    The thread receipt is at:
      0.4.0_DT_ClientPlatform/threads/ADVI_APISCP-001-lambda-edge-cloudfront-investigation_0.7.0_AE_CloudOps.md
  </objective>

  <scope>
    <files>
      <file action="modify">infra/aws/lambda-edge/shared-advisor-router/index.mjs</file>
    </files>
  </scope>

  <requirements>
    <!-- ================================================================== -->
    <!-- PREFLIGHT (MANDATORY — must complete before any code change)       -->
    <!-- Added 2026-03-10 per ADVI_APISCP-001 thread findings               -->
    <!-- ================================================================== -->
    <requirement id="0a" phase="preflight">
      AWS CLI Discovery — CloudFront behavior + origin wiring.
      Run: aws cloudfront get-distribution-config --id EVTSA9VEHNZVH
      Extract and paste into session log:
        - CacheBehaviors.Items[] where PathPattern == "/api/scoped/advisor-intelligence/*"
          -> TargetOriginId
          -> LambdaFunctionAssociations for EventType "origin-request" (full versioned ARN)
        - Origins.Items[] for that TargetOriginId
          -> Determine S3 vs custom origin
          -> Determine OAC vs OAI (check OriginAccessControlId vs S3OriginConfig.OriginAccessIdentity)
      This is a BLOCKING gate. Do not proceed to requirement 1 until this is complete.
    </requirement>
    <requirement id="0b" phase="preflight">
      AWS CLI Discovery — Lambda@Edge function identity + versioning.
      From the association ARN discovered in 0a, run:
        - aws lambda get-function --function-name {NAME} --region us-east-1
          -> Paste Configuration.FunctionArn, Runtime, LastModified
        - aws lambda list-versions-by-function --function-name {NAME} --region us-east-1
          -> Confirm versioning pattern (ensure not on $LATEST)
      This establishes the deployment workflow: publish-version + update-distribution.
    </requirement>
    <requirement id="0c" phase="preflight">
      Determine OAC vs OAI for the scoped origin.
      Thread finding: This environment uses OAC (Origin Access Control, ID E24L6358YRRKAE) for
      at least one S3 origin. The PRD assumed OAI — this may be WRONG.
        - If OAC: the v4 request.origin mutation must preserve OAC-compatible S3 origin shape.
          Do NOT set authMethod: "origin-access-identity".
        - If OAI: the PRD pseudocode may be used as-is.
      Record which auth model applies and adjust implementation accordingly.
    </requirement>

    <!-- ================================================================== -->
    <!-- IMPLEMENTATION (proceed only after preflight is complete)          -->
    <!-- ================================================================== -->
    <requirement id="1">
      Update infra/aws/lambda-edge/shared-advisor-router/index.mjs to v4:
      - Read X-Firm-Id from request.headers['x-firm-id'][0].value
      - If missing, return 403 with body "Missing firm identity"
      - Construct bucket: opal-data-{firmId}
      - Dynamically set request.origin to the constructed bucket
      - IMPORTANT: The exact request.origin mutation shape (replace vs in-place mutate,
        s3 vs custom, authMethod field) MUST match the actual origin type and auth model
        discovered in preflight step 0c. Do NOT hardcode OAI fields unless preflight
        confirms OAI is the auth model for this behavior.
      - Retain existing URI rewrite: /api/scoped/advisor-intelligence/* -> /gold/*
      - Update Host header to match new bucket domain
      - Update version comment in file header to v4
    </requirement>
    <requirement id="2">
      Verify CloudFront access to partner buckets.
      Thread finding: S3 bucket access is PER-BUCKET (no wildcard opal-data-* grant exists).
      The S3 Terraform module grants access via "${aws_s3_bucket.this.arn}/*" — each bucket
      must explicitly grant CloudFront access.
        - Confirm opal-data-bd currently has the CloudFront access policy.
        - If using OAC: new partner buckets need an OAC-compatible bucket policy.
        - If using OAI: new partner buckets need the OAI principal in their bucket policy.
        - Document the exact bucket policy template for partner onboarding.
    </requirement>
    <requirement id="3">
      Deploy the updated Lambda@Edge to us-east-1.
      Use the deployment mechanism discovered in preflight step 0b:
        - Publish a new Lambda version
        - Update the CloudFront behavior association to the new versioned ARN
        - Wait for CloudFront propagation (5-15 minutes)
      NOTE: This is NOT Terraform-managed. Document exact CLI commands used in session log.
    </requirement>
    <requirement id="4">
      Post-deploy verification.
      Invalidate /api/scoped/advisor-intelligence/* on CloudFront.
      Verify: curl with a valid JWT should return data from opal-data-bd/gold/ with
      data_as_of matching current gold date.
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">Preflight AWS discovery is documented in session log with all
    CloudFront config excerpts (behavior, origin, Lambda association, OAC/OAI determination)</criterion>
    <criterion id="2">GET /api/scoped/advisor-intelligence/timeseries_chart.json with a
    49 Financial JWT returns data from opal-data-bd/gold/ (data_as_of: current gold date)</criterion>
    <criterion id="3">Lambda@Edge code reads X-Firm-Id and constructs origin dynamically
    (no hardcoded bucket name)</criterion>
    <criterion id="4">Request without X-Firm-Id returns 403</criterion>
    <criterion id="5">Origin mutation shape matches actual OAC/OAI auth model (not assumed)</criterion>
    <criterion id="6">Partner onboarding bucket policy template is documented</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Lambda@Edge must be deployed to us-east-1. Deployment mechanism must be discovered via preflight, not assumed.</constraint>
    <constraint>Do not modify auth-validator-edge -- it already correctly injects X-Firm-Id.</constraint>
    <constraint>shared-advisor-router is an origin-request trigger. Dynamic origin mutation is valid only in origin-request phase -- this is already correct.</constraint>
    <constraint>Do NOT hardcode authMethod: "origin-access-identity" unless preflight confirms OAI. This environment may use OAC.</constraint>
    <constraint>CloudFront propagation takes 5-15 minutes. Wait for propagation before verification.</constraint>
    <constraint>Never write partner data to opal-data-portal-v2. This anti-pattern was eliminated 2026-03-10 and must never be recreated.</constraint>
    <constraint>S3 bucket access is per-bucket. Partner onboarding requires explicit CloudFront access policy on each opal-data-{firmId} bucket.</constraint>
  </constraints>

  <dependencies>
    <!-- Preflight steps 0a-0c must complete before implementation steps 1-4. -->
    <!-- No external agent dependencies. DT can proceed immediately with preflight. -->
  </dependencies>

  <references>
    <ref type="prd">docs/architecture/ADVI_APISCP_PRD.md</ref>
    <ref type="thread">ADVI_APISCP-001 (Lambda@Edge + CloudFront investigation — Pattern 2)</ref>
    <ref type="receipt">0.4.0_DT_ClientPlatform/threads/ADVI_APISCP-001-lambda-edge-cloudfront-investigation_0.7.0_AE_CloudOps.md</ref>
    <ref type="source">infra/aws/lambda-edge/shared-advisor-router/index.mjs (current v3)</ref>
    <ref type="source">infra/aws/lambda-edge/auth-validator-edge/index.mjs (injects X-Firm-Id)</ref>
  </references>

  <deliverables>
    <deliverable type="document">Preflight discovery log (CloudFront config excerpts, OAC/OAI determination, Lambda versioning pattern)</deliverable>
    <deliverable type="commit">Updated shared-advisor-router/index.mjs v4</deliverable>
    <deliverable type="document">Partner onboarding bucket policy template</deliverable>
    <deliverable type="document">Session log documenting deployment steps and verification</deliverable>
  </deliverables>
</task_order>
