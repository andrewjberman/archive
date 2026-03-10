<task_order>
  <metadata>
    <id>1.0.0_SA_CTO-2026-03-10-advi-apiscp-003-oai-setup</id>
    <issued_by>1.0.0_SA_CTO</issued_by>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <date>2026-03-10</date>
    <status>pending</status>
    <thread_serial>ADVI_APISCP-003</thread_serial>
    <thread_ref>org/projects/ADVI_APISCP.json</thread_ref>
  </metadata>

  <objective>
    Create a new CloudFront Origin Access Identity (OAI) for the scoped advisor routing
    behavior and apply a bucket policy to opal-data-bd granting that OAI s3:GetObject.
    This is the prerequisite that unblocks DT (0.4.0_DT_ClientPlatform) from completing
    the v5 CloudFront wiring. DT cannot proceed until you deliver the OAI ID and
    canonical user ID.
  </objective>

  <context>
    Lambda@Edge v4 (shared-advisor-router:4) failed in production because CloudFront
    bypasses OAC signing whenever request.origin is mutated at the Lambda@Edge level.
    This is a fundamental AWS architectural constraint, not a code bug. The fix is to
    migrate the S3-opal-data-bd origin (for the /api/scoped/advisor-intelligence/*
    behavior only) from OAC to OAI. OAI is a principal-based identity that CloudFront
    attaches to all requests from the behavior, regardless of which S3 domain Lambda@Edge
    routes to — making it compatible with dynamic multi-tenant origin selection.

    Architecture decision log: org/tier1_exec/1.0.0_SA_CTO/logs/2026-03-10/advi_apiscp_v5_architecture_decision.md
  </context>

  <scope>
    <files>
      <file action="modify">opal-data-bd S3 bucket policy (AWS-live, no git artifact)</file>
      <file action="create">New OAI: opal-scoped-advisor-oai (AWS-live, no git artifact)</file>
      <file action="modify">org/tier2_senior/0.7.0_AE_CloudOps/task_orders/ADVI_APISCP.003.oai-setup-bucket-policy.md (status: complete)</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">
      Create a new CloudFront Origin Access Identity named opal-scoped-advisor-oai.
      DO NOT reuse EU39UXW7CMSI5 (that OAI belongs to the S3-opalinvest-portal origin
      and must remain isolated). Use:
        aws cloudfront create-cloud-front-origin-access-identity \
          --cloud-front-origin-access-identity-config \
            CallerReference=opal-scoped-advisor-oai-2026-03-10,Comment=opal-scoped-advisor-oai
      Record both the OAI ID (E...) and the S3CanonicalUserId from the response.
    </requirement>

    <requirement id="2">
      Apply a bucket policy statement to opal-data-bd granting the new OAI canonical user
      s3:GetObject on all objects. The statement must be ADDED to the existing bucket policy,
      not replace it. Read the current bucket policy first with:
        aws s3api get-bucket-policy --bucket opal-data-bd
      Then add the following statement:
        {
          "Sid": "AllowScopedAdvisorOAI",
          "Effect": "Allow",
          "Principal": {
            "CanonicalUser": "{S3CanonicalUserId from requirement 1}"
          },
          "Action": "s3:GetObject",
          "Resource": "arn:aws:s3:::opal-data-bd/*"
        }
      Apply the updated policy with:
        aws s3api put-bucket-policy --bucket opal-data-bd --policy '{updated_policy_json}'
      Verify the policy was applied with:
        aws s3api get-bucket-policy --bucket opal-data-bd
    </requirement>

    <requirement id="3">
      Deliver the OAI ID and canonical user ID to DT in your session log.
      Format your deliverable as:
        OAI ID:             E{...}
        S3CanonicalUserId:  {79-char canonical user string}
      DT (0.4.0_DT_ClientPlatform) needs both values to update the CloudFront
      distribution origin config.
    </requirement>

    <requirement id="4">
      Update the partner onboarding checklist that was delivered as part of
      ADVI_APISCP.001 (AE PartnerETL onboarding checklist). Add the following step:
        - Apply bucket policy to opal-data-{firmId} granting OAI opal-scoped-advisor-oai
          (canonical user ID: {from req 1}) s3:GetObject on arn:aws:s3:::opal-data-{firmId}/*
      The onboarding checklist path is in AE PartnerETL deliverables. If you cannot
      locate it, note this in your log and flag to COO.
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">New OAI opal-scoped-advisor-oai exists in AWS. OAI ID and canonical user ID recorded in session log.</criterion>
    <criterion id="2">opal-data-bd bucket policy includes AllowScopedAdvisorOAI statement with correct canonical user ID. Verified with get-bucket-policy.</criterion>
    <criterion id="3">DT has the OAI ID + canonical user ID they need (in your session log, marked clearly).</criterion>
    <criterion id="4">Onboarding checklist updated with OAI bucket policy step.</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Do NOT reuse EU39UXW7CMSI5. Create a new OAI for the scoped advisor routing. Mixing OAI purposes creates permission coupling and complicates future migration.</constraint>
    <constraint>Do NOT remove any existing bucket policy statements from opal-data-bd. Append only — read existing policy first, add the statement, write it back.</constraint>
    <constraint>Do NOT modify the CloudFront distribution. That is DT's responsibility (ADVI_APISCP.003.cloudfront-oai-cache-key-v5.md).</constraint>
    <constraint>Do NOT disable or remove OAC from any other origin on the distribution. OAC continues to serve all other behaviors. Only the S3-opal-data-bd origin for the /api/scoped/ behavior changes to OAI.</constraint>
  </constraints>

  <dependencies>
    <!-- None — CloudOps executes first, unblocks DT -->
  </dependencies>

  <deliverables>
    <deliverable type="aws-live">OAI opal-scoped-advisor-oai created (ID + canonical user ID)</deliverable>
    <deliverable type="aws-live">opal-data-bd bucket policy updated with AllowScopedAdvisorOAI statement</deliverable>
    <deliverable type="document">Session log with OAI ID + canonical user ID clearly marked for DT handoff</deliverable>
    <deliverable type="document">Onboarding checklist updated with OAI bucket policy step</deliverable>
  </deliverables>
</task_order>
