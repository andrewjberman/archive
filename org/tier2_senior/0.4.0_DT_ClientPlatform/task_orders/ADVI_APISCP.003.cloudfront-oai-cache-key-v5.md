<task_order>
  <metadata>
    <id>1.0.0_SA_CTO-2026-03-10-advi-apiscp-003-cloudfront-v5</id>
    <issued_by>1.0.0_SA_CTO</issued_by>
    <issued_to>0.4.0_DT_ClientPlatform</issued_to>
    <date>2026-03-10</date>
    <status>complete</status>
    <thread_serial>ADVI_APISCP-003</thread_serial>
    <thread_ref>org/projects/ADVI_APISCP.json</thread_ref>
  </metadata>

  <objective>
    Wire the new OAI (opal-scoped-advisor-oai, created by CloudOps) into CloudFront
    distribution EVTSA9VEHNZVH: migrate S3-opal-data-bd origin from OAC to OAI, update
    the cache policy for /api/scoped/advisor-intelligence/* to vary by X-Firm-Id (compliance
    requirement), re-deploy shared-advisor-router:4 code as :5, invalidate the cache, and
    tag the deployment.
  </objective>

  <context>
    Lambda@Edge v4 failed because OAC signing is bypassed whenever request.origin is
    mutated at the Lambda@Edge origin-request stage. This is an AWS architectural
    constraint. The fix is OAI: when the S3-opal-data-bd origin uses OAI, CloudFront
    signs all requests from this behavior as the OAI principal, regardless of which
    S3 domain Lambda@Edge routes to. Target buckets accept the OAI principal via bucket
    policy — enabling zero-touch onboarding (no distribution change per new partner).

    The v4 Lambda@Edge code is ALREADY CORRECT — it uses authMethod: 'origin-access-identity'.
    No code change is needed. v5 is purely a CloudFront + cache policy reconfiguration.
    Deploy v4 code as Lambda version :5 for audit clarity (v4 = broken attempt, v5 = fixed).

    CRITICAL NEW REQUIREMENT: the cache policy must vary by X-Firm-Id (see requirement 2).
    This was not in the v4 spec. It is a compliance requirement. It must ship with v5.

    Architecture decision log: org/tier1_exec/1.0.0_SA_CTO/logs/2026-03-10/advi_apiscp_v5_architecture_decision.md
  </context>

  <scope>
    <files>
      <file action="modify">CloudFront distribution EVTSA9VEHNZVH (AWS-live — not in Terraform)</file>
      <file action="modify">shared-advisor-router Lambda function (re-publish :5 from same source as :4)</file>
      <file action="modify">org/tier2_senior/0.4.0_DT_ClientPlatform/task_orders/ADVI_APISCP.003.cloudfront-oai-cache-key-v5.md (status: complete)</file>
    </files>
  </scope>

  <requirements>
    <requirement id="0">
      HARD DEPENDENCY: Do not proceed until CloudOps (0.7.0_AE_CloudOps) has delivered
      their ADVI_APISCP.003 task order. You need from their session log:
        - OAI ID:            E{...}
        - S3CanonicalUserId: {79-char canonical user string}
      These values are required to wire the distribution origin correctly.
      Check: org/tier2_senior/0.7.0_AE_CloudOps/logs/{latest-date}/ for their delivery.
    </requirement>

    <requirement id="1">
      Migrate S3-opal-data-bd origin in CloudFront distribution EVTSA9VEHNZVH from OAC
      to OAI.

      Step-by-step:
        1. Get distribution config and ETag:
             aws cloudfront get-distribution-config --id EVTSA9VEHNZVH
        2. In the returned JSON, locate the S3 origin with DomainName containing opal-data-bd.
        3. In that origin's S3OriginConfig:
             - Set: S3OriginConfig.OriginAccessIdentity = "origin-access-identity/cloudfront/{OAI_ID_from_CloudOps}"
             (Replace {OAI_ID_from_CloudOps} with the actual OAI ID, e.g., E1XXXXX...)
        4. Remove the S3OriginConfig.OriginAccessControl references if present (the OAC ID E24L6358YRRKAE).
           Note: OAC is configured in OriginAccessControlId at the origin level. Remove that field or set it to empty.
        5. Write the updated distribution config back:
             aws cloudfront update-distribution --id EVTSA9VEHNZVH \
               --distribution-config file://updated-dist-config.json \
               --if-match {ETag}
        6. Wait for Status: Deployed (poll with aws cloudfront get-distribution --id EVTSA9VEHNZVH).
    </requirement>

    <requirement id="2">
      Update the CloudFront cache policy for the /api/scoped/advisor-intelligence/* behavior
      to vary the cache by X-Firm-Id header.

      This is a COMPLIANCE requirement. Without it, two users from different firms hitting
      the same edge PoP for the same path could share a cache entry — firm A's data served
      to firm B. The auth-validator-edge (viewer-request) already injects X-Firm-Id from
      the validated JWT before the cache check, so the header is available.

      Implementation:
        Option A (preferred) — modify the existing cache policy attached to this behavior
        to include X-Firm-Id in the Headers config:
          - Get the current cache policy ID from the behavior
          - Update it: Headers.Items += ["X-Firm-Id"], Headers.Quantity += 1
          - Apply via aws cloudfront update-cache-policy

        Option B — create a new cache policy with X-Firm-Id included and attach it to
        the behavior. Use if modifying the shared policy would affect other behaviors.

      Verify the cache policy update is applied to the correct behavior before proceeding
      to requirement 3.

      Note: X-Firm-Id must be in the CACHE KEY (cache policy), not just Origin Request
      Policy. They are separate. Both may be updated but the cache key is the requirement.
    </requirement>

    <requirement id="3">
      Re-deploy shared-advisor-router as Lambda version :5.

      The code is identical to v4 (commit 4eff8dee). No source changes. Steps:
        1. Confirm the current Lambda function: shared-advisor-router in us-east-1
        2. Publish a new version from the existing code (or re-zip and upload the same source):
             aws lambda publish-version --function-name shared-advisor-router --description "v5: OAI configured on distribution"
        3. Record the new version ARN (arn:aws:lambda:us-east-1:313476888478:function:shared-advisor-router:5)
        4. Update the CloudFront behavior for /api/scoped/advisor-intelligence/* to reference :5
           (in the same distribution update as requirements 1 and 2, or as a follow-up if separate)

      The Lambda@Edge code already uses authMethod: 'origin-access-identity'. It is correct
      as-is. Publishing as :5 creates audit clarity: :3 = working single-tenant, :4 = broken
      OAC attempt (rolled back), :5 = correct OAI multi-tenant.
    </requirement>

    <requirement id="4">
      After the distribution reaches Status: Deployed, invalidate the scoped advisor cache:
        aws cloudfront create-invalidation \
          --distribution-id EVTSA9VEHNZVH \
          --paths "/api/scoped/advisor-intelligence/*"
      Record the invalidation ID.
    </requirement>

    <requirement id="5">
      Verify end-to-end. Use a 49 Financial user JWT to test:
        curl -s -H "Authorization: Bearer {49fin_jwt}" \
          https://d2n2nzpeqf34ge.cloudfront.net/api/scoped/advisor-intelligence/timeseries_chart.json \
          | jq '.aua.data | last | .date'
      Expected: current gold date (2026-03-06 or later).
      Response Content-Type must be application/json, NOT text/html.
      If you see text/html, OAI is not yet signing correctly — do not tag until resolved.
    </requirement>

    <requirement id="6">
      Tag the deployment:
        git tag -a shared-advisor-router-v5 \
          -m "shared-advisor-router:5 -- OAI migration; cache key varies by X-Firm-Id" \
          4eff8dee
        git push --follow-tags

      Note: 4eff8dee is the v4 source commit. The code is unchanged; the infra change is
      AWS-live (no new git commit needed for the Lambda or CloudFront changes). Tag points
      to the source commit that produced the deployed code.
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">CloudFront distribution EVTSA9VEHNZVH: S3-opal-data-bd origin uses OAI opal-scoped-advisor-oai. No OAC on this origin. Status: Deployed.</criterion>
    <criterion id="2">Cache policy for /api/scoped/advisor-intelligence/* behavior includes X-Firm-Id in the cache key headers.</criterion>
    <criterion id="3">shared-advisor-router:5 is published and wired to the behavior.</criterion>
    <criterion id="4">GET /api/scoped/advisor-intelligence/timeseries_chart.json with a 49 Financial JWT returns HTTP 200, Content-Type: application/json, data_as_of: 2026-03-06 (or current gold date). Not HTML.</criterion>
    <criterion id="5">Cache invalidation /api/scoped/advisor-intelligence/* completed. Invalidation ID recorded in session log.</criterion>
    <criterion id="6">git tag shared-advisor-router-v5 pushed to remote.</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>BLOCKED on CloudOps ADVI_APISCP.003. Do not touch the distribution until you have the OAI ID and canonical user ID from CloudOps.</constraint>
    <constraint>Do NOT remove OAC from any other origin on the distribution. Only S3-opal-data-bd for the scoped advisor behavior changes. Other behaviors (portal-v2, other S3 origins) keep their current auth model.</constraint>
    <constraint>Do NOT re-deploy v4 code changes. The source is 4eff8dee. Publish :5 from that same code. If Lambda requires a new ZIP upload, use the same source — do not modify it.</constraint>
    <constraint>Do NOT skip the X-Firm-Id cache key update. It is a compliance requirement. If the cache policy update proves technically complex (e.g., shared policy affects other behaviors), escalate to CTO before proceeding without it.</constraint>
    <constraint>Do NOT tag until end-to-end verification (requirement 5) passes. Specifically: response must be application/json, not text/html.</constraint>
  </constraints>

  <dependencies>
    <dependency agent="0.7.0_AE_CloudOps" task="ADVI_APISCP.003.oai-setup-bucket-policy" status="pending"/>
  </dependencies>

  <deliverables>
    <deliverable type="aws-live">CloudFront distribution EVTSA9VEHNZVH: S3-opal-data-bd origin migrated OAC → OAI</deliverable>
    <deliverable type="aws-live">Cache policy updated: X-Firm-Id in cache key for /api/scoped/advisor-intelligence/* behavior</deliverable>
    <deliverable type="aws-live">shared-advisor-router:5 published and wired</deliverable>
    <deliverable type="commit">git tag shared-advisor-router-v5 on 4eff8dee, pushed with --follow-tags</deliverable>
    <deliverable type="document">Session log with end-to-end verification output (curl response, Content-Type, gold date)</deliverable>
  </deliverables>
</task_order>
