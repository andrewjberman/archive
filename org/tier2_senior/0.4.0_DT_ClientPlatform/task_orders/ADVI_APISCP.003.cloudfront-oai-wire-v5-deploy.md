<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-03-10-cloudfront-oai-wire-v5-deploy</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DT_ClientPlatform</issued_to>
    <date>2026-03-10</date>
    <status>pending</status>
    <phase>3</phase>
  </metadata>

  <objective>
    Wire the OAI delivered by CloudOps into the CloudFront distribution.
    Update the /api/scoped/advisor-intelligence/*.json cache behavior to:
      1. Use OAI instead of OAC for the S3-opal-data-bd origin
      2. Add X-Firm-Id to the cache key policy (mandatory compliance requirement)
    Deploy Lambda@Edge :5 (same v4 code -- no code changes needed).
    Invalidate, verify, tag.

    The v4 code (request.origin.s3.domainName in-place mutation) is correct for OAI.
    OAI is a principal identity -- CloudFront signs all requests as the OAI canonical user
    regardless of which domain Lambda@Edge routes to. No code change to shared-advisor-router.
  </objective>

  <requirements>
    <requirement id="0" phase="preflight">
      BLOCKED. Wait for CloudOps ADVI_APISCP.003 handoff note at:
        org/tier2_senior/0.4.0_DT_ClientPlatform/task_orders/ADVI_APISCP.003.oai-handoff.md

      Read it. Confirm you have:
        - OAI ID (E...)
        - S3CanonicalUserId
        - Confirmation that opal-data-bd bucket policy is applied

      Do not proceed past this gate until the handoff note exists.
    </requirement>
    <requirement id="1">
      Get the current distribution config and ETag:
        export MSYS_NO_PATHCONV=1
        python -m awscli cloudfront get-distribution-config --id EVTSA9VEHNZVH --output json > /tmp/cf_config.json

      Extract the ETag -- needed for the update-distribution call.
    </requirement>
    <requirement id="2">
      Migrate S3-opal-data-bd origin from OAC to OAI.
      In the Origins.Items[] entry for S3-opal-data-bd:
        - Set OriginAccessControlId to "" (empty string, removes OAC)
        - Set S3OriginConfig.OriginAccessIdentity to "origin-access-identity/cloudfront/{OAI_ID}"
    </requirement>
    <requirement id="3">
      Add X-Firm-Id to the cache key for the /api/scoped/advisor-intelligence/*.json behavior.
      MANDATORY compliance requirement: with two firms hitting the same edge PoP, a cache
      hit from firm A must NOT be served to firm B. auth-validator-edge injects X-Firm-Id
      on viewer-request (before cache check), so the header is always present.

      If behavior uses a managed cache policy: create a new custom cache policy forwarding
      X-Firm-Id as a cache key header.
      If behavior uses legacy ForwardedValues: add X-Firm-Id to Headers.Items[] with
      Forward: "whitelist".
    </requirement>
    <requirement id="4">
      Apply updated distribution config via update-distribution with the ETag from step 1.
      Wait for distribution status Deployed before proceeding.
    </requirement>
    <requirement id="5">
      Publish Lambda@Edge :5. Code is unchanged from :4 -- new version creates a clean
      deployment boundary corresponding to the OAI wiring:
        python -m awscli lambda publish-version \
          --function-name shared-advisor-router \
          --description "v5: OAI wiring, X-Firm-Id cache key" \
          --region us-east-1

      Update the behavior LambdaFunctionAssociations origin-request ARN to :5.
    </requirement>
    <requirement id="6">
      Invalidate: python -m awscli cloudfront create-invalidation \
        --distribution-id EVTSA9VEHNZVH --paths "/api/scoped/advisor-intelligence/*"
    </requirement>
    <requirement id="7">
      Post-deploy verification (wait 5-15 min for propagation):
        - curl with valid 49 Financial JWT -> HTTP 200, Content-Type: application/json
        - data_as_of matches current gold date (2026-03-06)
        - Second identical request returns X-Cache: Hit from cloudfront
    </requirement>
    <requirement id="8">
      Tag:
        git tag -a shared-advisor-router-v5 -m "v5: OAI replaces OAC, X-Firm-Id in cache key"
        git push origin shared-advisor-router-v5
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">S3-opal-data-bd origin uses OAI (not OAC) in distribution config</criterion>
    <criterion id="2">X-Firm-Id is in the cache key for the scoped advisor behavior</criterion>
    <criterion id="3">Lambda@Edge :5 published and associated</criterion>
    <criterion id="4">GET with valid JWT returns HTTP 200, application/json, data_as_of: 2026-03-06</criterion>
    <criterion id="5">Second request returns X-Cache: Hit from cloudfront</criterion>
    <criterion id="6">Tagged shared-advisor-router-v5 and pushed</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>BLOCKED on CloudOps ADVI_APISCP.003. Do not proceed until OAI handoff note exists.</constraint>
    <constraint>Do NOT modify shared-advisor-router/index.mjs -- v4 code is correct as-is for OAI.</constraint>
    <constraint>X-Firm-Id cache key is MANDATORY. Ships with this task order, not a follow-up.</constraint>
    <constraint>export MSYS_NO_PATHCONV=1 before all AWS CLI calls with path arguments.</constraint>
    <constraint>CloudFront is not Terraform-managed. All changes via AWS CLI. Document exact commands in session log.</constraint>
  </constraints>

  <dependencies>
    <dependency agent="0.7.0_AE_CloudOps" task="ADVI_APISCP.003.oai-setup-bucket-policy" status="pending"
                gate="org/tier2_senior/0.4.0_DT_ClientPlatform/task_orders/ADVI_APISCP.003.oai-handoff.md"/>
  </dependencies>

  <references>
    <ref type="cto_decision">4387ec08 -- OAI selected, X-Firm-Id cache key mandatory</ref>
    <ref type="brief">org/tier1_exec/1.0.0_SA_CTO/task_orders/ADVI_APISCP.v5-oac-dynamic-origin-brief.md</ref>
    <ref type="source">infra/aws/lambda-edge/shared-advisor-router/index.mjs (v4 code, no changes needed)</ref>
    <ref type="handoff">org/tier2_senior/0.4.0_DT_ClientPlatform/task_orders/ADVI_APISCP.003.oai-handoff.md</ref>
  </references>

  <deliverables>
    <deliverable type="aws_config">CloudFront EVTSA9VEHNZVH: OAI wired, X-Firm-Id cache key, :5 associated</deliverable>
    <deliverable type="tag">shared-advisor-router-v5</deliverable>
    <deliverable type="document">Session log with all AWS CLI commands and verification results</deliverable>
  </deliverables>
</task_order>
