<task_order>
  <metadata>
    <id>1.0.0_SA_CTO-2026-03-30-auth-validator-v8-hotfix</id>
    <issued_by>1.0.0_SA_CTO</issued_by>
    <issued_to>0.4.0_DT_ClientPlatform</issued_to>
    <date>2026-03-30</date>
    <status>archived</status>
    <thread_serial>ADVI_ANONYM-001</thread_serial>
  </metadata>

  <objective>
    SECURITY HOTFIX: Deploy auth-validator-edge v8 which adds a role gate blocking
    non-admin users from advisor-intelligence API paths. Currently ANY authenticated
    user can curl full PII (client names, AUA, geography, account numbers) because
    the admin check is frontend-only. This hotfix returns 403 Forbidden for non-admin
    users on /api/scoped/advisor-intelligence/* and /api/shared/advisor-intelligence/*.
  </objective>

  <scope>
    <files>
      <file action="modify">infra/aws/lambda-edge/auth-validator-edge/index.mjs</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">
      The code change is ALREADY WRITTEN in index.mjs on CLOUD branch (lines 58-66:
      role gate, lines 100-110: forbidden() helper). CTO authored the change. DT's
      job is to build, deploy, and verify.
    </requirement>

    <requirement id="2">
      Build the Lambda@Edge zip:
      ```bash
      cd infra/aws/lambda-edge/auth-validator-edge
      npm install   # installs jsonwebtoken
      # Zip index.mjs + node_modules/ into auth-validator-edge.zip
      ```
    </requirement>

    <requirement id="3">
      Deploy the Lambda@Edge function. The function name is auth-validator-edge
      (or check the current function name in CloudFront distribution EVTSA9VEHNZVH
      viewer-request association). Steps:
      1. Update function code (upload zip)
      2. Publish new version (aws lambda publish-version)
      3. Update CloudFront distribution viewer-request Lambda@Edge association
         to the new version ARN (must be a numbered version, not $LATEST)
      4. Wait for CloudFront distribution to deploy (status: Deployed)

      NOTE: Lambda@Edge functions must be in us-east-1. The CloudFront distribution
      is EVTSA9VEHNZVH (opalinvest.dev). The distribution is currently console-managed
      (not in Terraform), so update via AWS CLI or console.
    </requirement>

    <requirement id="4">
      Verify the hotfix works:
      1. Test with admin JWT: curl advisor-intelligence path -> 200 (should still work)
      2. Test with non-admin JWT: curl advisor-intelligence path -> 403 Forbidden
      3. Test non-advisor-intelligence paths with non-admin -> 200 (should be unaffected)
      4. Check CloudWatch logs for "Auth BLOCKED" log entries
    </requirement>

    <requirement id="5">
      If the distribution is not yet in Terraform, this is a manual deploy. If it IS
      in Terraform (check for aws_cloudfront_distribution resource referencing
      EVTSA9VEHNZVH), use the standard Terraform flow. Either way, commit the
      deployment evidence (version ARN, distribution ID) in your session log.
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">Non-admin users get 403 on /api/scoped/advisor-intelligence/* and /api/shared/advisor-intelligence/*</criterion>
    <criterion id="2">Admin users continue to get 200 on all paths</criterion>
    <criterion id="3">All other API paths unaffected for all users</criterion>
    <criterion id="4">CloudFront distribution status: Deployed with new Lambda@Edge version</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>This is a SECURITY HOTFIX -- prioritize speed. Deploy first, Terraform-ify later if needed.</constraint>
    <constraint>Lambda@Edge must be in us-east-1 region.</constraint>
    <constraint>CloudFront distribution EVTSA9VEHNZVH is console-managed. Do not try to import it into Terraform as part of this hotfix.</constraint>
    <constraint>The code change is already committed on CLOUD. Do NOT modify index.mjs -- just build and deploy what's there.</constraint>
    <constraint>No emojis in any code per CLAUDE.md.</constraint>
  </constraints>

  <dependencies>
    <dependency agent="1.0.0_SA_CTO" task="auth-validator-edge-v8-code" status="complete">Code change written by CTO on CLOUD branch.</dependency>
  </dependencies>

  <deliverables>
    <deliverable type="deploy">auth-validator-edge v8 live on CloudFront distribution EVTSA9VEHNZVH</deliverable>
    <deliverable type="document">Session log with version ARN, verification curl outputs</deliverable>
  </deliverables>
</task_order>
