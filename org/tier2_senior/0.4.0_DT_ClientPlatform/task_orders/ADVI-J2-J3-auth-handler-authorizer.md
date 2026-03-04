# Task Order: ADVI-J2/J3 — Auth-Handler + Portal-Authorizer Partner Identity — 0.4.0_DT_ClientPlatform

```xml
<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-03-04-ADVI-J2-J3-auth-handler-authorizer</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DT_ClientPlatform</issued_to>
    <date>2026-03-04</date>
    <status>pending</status>
    <priority>HIGH — DT is blocked on Books tab (J4) until J2/J3 complete</priority>
  </metadata>

  <objective>
    Update the auth-handler Lambda (J2) and portal-authorizer Lambda (J3) so that
    advisor identity (advisorKey, advisorRole, firmId) is injected into the JWT at login
    and passed through to Lambda context. This enables scoped Lambdas (Books tab, bd-client-detail)
    to read the advisor's identity from requestContext.authorizer without any query string.

    This supersedes the previous Cognito firmId approach (task order advisor_intelligence_firmid_auth.md).
    The new approach uses a DynamoDB per-partner table (opal-partner-49financial) read by auth-handler.
  </objective>

  <references>
    <ref type="prd" priority="PRIMARY">docs/architecture/PARTNER_IDENTITY_TABLE.md</ref>
    <ref type="prd-parent">docs/architecture/ADVISOR_INTELLIGENCE_COMPLETION.md</ref>
    <ref type="auth-handler">infra/aws/opalinvest_dev/lambda/auth-handler/</ref>
    <ref type="portal-authorizer">infra/aws/users/lambda/portal-authorizer/</ref>
    <ref type="portal-auth-tf">infra/aws/terraform/ (portal-auth module you own, commit 1660ed82)</ref>
    <ref type="scoped-page-access-prd">docs/architecture/SCOPED_PAGE_ACCESS.md</ref>
    <ref type="lambda-deploy-protocol">docs/deployment/LAMBDA_DEPLOYMENT_PROTOCOL.md</ref>
  </references>

  <dependency>
    <blocked_by>
      ADVI-J1 (0.7.0_AE_CloudOps must create opal-partner-49financial table first).
      Do NOT start J2 code changes until J1 is confirmed complete and table ARN is available.
      J1 completion will be documented in AE's session log.
    </blocked_by>
  </dependency>

  <requirements>

    <!-- ================================================================ -->
    <!-- STREAM J2 — auth-handler Lambda                                  -->
    <!-- ================================================================ -->
    <requirement id="J2.1">
      File: infra/aws/opalinvest_dev/lambda/auth-handler/

      After the existing opal-users-v2 lookup succeeds, add a conditional second DynamoDB
      read from opal-partner-49financial:

        CONDITION: user's allowedPages list includes "advisor-intelligence"
          (this is how auth-handler knows the user is a 49 Financial user)

        IF condition met:
          dynamodb.get_item(
            TableName="opal-partner-49financial",
            Key={"email": {"S": user_email}}
          )
          If record found: extract advisorKey, advisorRole
          If no record: omit those claims (graceful degradation — user still logs in)

        JWT claims to add when record found:
          firmId     = "49financial"
          advisorKey = record["advisorKey"]["S"]
          advisorRole= record["advisorRole"]["S"]

      Reference the auth flow diagram in PRD Section 3 (New Flow) for the exact sequence.
    </requirement>

    <requirement id="J2.2">
      Graceful degradation:
        - If opal-partner-49financial has no record for the email: JWT omits advisorKey,
          advisorRole, firmId entirely. User can still log in and access non-scoped pages.
        - If the DynamoDB call itself errors (table unreachable): log the error, do NOT
          fail the login. Treat as "no record found" — degrade gracefully.
        - Do NOT throw a 401/403 when the partner table has no record.
    </requirement>

    <requirement id="J2.3">
      IAM: the auth-handler Lambda role needs GetItem and Query on opal-partner-49financial.
      AE (J1) will either attach this policy or document the attachment point.
      If AE left the IAM attachment for DT (within your portal-auth Terraform module):
        add the policy statement to the auth-handler role in your module.
      Confirm with AE's J1 session log for the exact IAM status before deploying.
    </requirement>

    <!-- ================================================================ -->
    <!-- STREAM J3 — portal-authorizer Lambda                             -->
    <!-- ================================================================ -->
    <requirement id="J3.1">
      File: infra/aws/users/lambda/portal-authorizer/

      The portal-authorizer already passes allowedPages and allowedTabs through to Lambda
      context (from SCOPED_PAGE_ACCESS.md, commit 1660ed82). Apply the same passthrough
      pattern for the three new JWT claims:
        - firmId
        - advisorKey
        - advisorRole

      These claims will be absent from the JWT for non-advisor users. The authorizer must
      pass them through IF present, and omit them IF absent. Do not error when they are
      absent — most users will not have them.

      After J3, scoped Lambdas read advisor identity from:
        event["requestContext"]["authorizer"]["advisorKey"]
        event["requestContext"]["authorizer"]["advisorRole"]
        event["requestContext"]["authorizer"]["firmId"]
    </requirement>

    <!-- ================================================================ -->
    <!-- DEPLOY — Both Lambdas via portal-auth Terraform module           -->
    <!-- ================================================================ -->
    <requirement id="J2J3.deploy">
      Deploy both Lambdas via the portal-auth Terraform module (your module, commit 1660ed82).
      Follow the standard sequence:
        1. Write code changes (auth-handler + portal-authorizer)
        2. git commit (--author="0.4.0_DT_ClientPlatform &lt;0.4.0_DT_ClientPlatform@opal.agent&gt;")
        3. terraform plan (portal-auth module)
        4. terraform apply
        5. Confirm 0-diff on second apply
        6. git tag -a portal-auth-v{X.Y.Z} -m "feat(portal-auth): partner identity JWT claims J2/J3 (ADVI)"
        7. git push --follow-tags

      Update lambda-source-map.json if either Lambda's source path changed.
    </requirement>

    <!-- ================================================================ -->
    <!-- VERIFICATION                                                      -->
    <!-- ================================================================ -->
    <requirement id="J2J3.verify">
      After deploy:
        1. Trigger a login for a test user whose email IS in opal-partner-49financial.
           Verify JWT contains firmId, advisorKey, advisorRole.
        2. Trigger a login for a test user whose email is NOT in opal-partner-49financial.
           Verify login succeeds and JWT does NOT contain those claims (graceful degradation).
        3. Confirm portal-authorizer passes claims to Lambda context:
           Read a scoped Lambda's CloudWatch logs and confirm advisorKey appears in
           requestContext.authorizer for an authenticated advisor user.

      Document verification results in session log.
    </requirement>

  </requirements>

  <acceptance_criteria>
    <criterion id="1">auth-handler reads opal-partner-49financial on login for advisor-intelligence users.</criterion>
    <criterion id="2">JWT contains firmId, advisorKey, advisorRole when record found.</criterion>
    <criterion id="3">Login succeeds with graceful degradation when no partner record exists.</criterion>
    <criterion id="4">portal-authorizer passes firmId, advisorKey, advisorRole to Lambda context.</criterion>
    <criterion id="5">Both Lambdas deployed via portal-auth Terraform module at 0-diff.</criterion>
    <criterion id="6">portal-auth-v{X.Y.Z} tag applied and pushed.</criterion>
    <criterion id="7">Verification results (both test cases) documented in session log.</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>DO NOT start J2 until AE confirms J1 complete (table must exist in DynamoDB).</constraint>
    <constraint>Deploy via Terraform only — never aws lambda update-function-code directly.</constraint>
    <constraint>Do NOT modify opal-users-v2 schema or data.</constraint>
    <constraint>Do NOT remove or change existing JWT claims (email, role, allowedPages, allowedTabs).</constraint>
    <constraint>Do NOT add firmId/advisorKey to opal-users-v2. That table stays generic.</constraint>
    <constraint>Do NOT use emojis in any code or log output.</constraint>
    <constraint>Commit with: git commit --author="0.4.0_DT_ClientPlatform &lt;0.4.0_DT_ClientPlatform@opal.agent&gt;" -m "..."</constraint>
    <constraint>export MSYS_NO_PATHCONV=1 before Terraform commands with ARN paths on Git Bash (Windows).</constraint>
    <constraint>export AWS_EC2_METADATA_DISABLED=true if AWS CLI hangs (see .bashrc — already set).</constraint>
  </constraints>

  <what_this_unlocks>
    J3 completion unblocks:
      - J4: Books tab auth gating (DE + RD — advisorKey -> S3 path, advisorRole -> L1/L2/viewer render)
      - bd-client-detail scoping: advisorKey from context replaces firmId query param
    J4 also requires ADVI-006 Books design brief — COO will schedule that thread after J3.
    Notify COO when J3 is confirmed deployed and tested.
  </what_this_unlocks>

  <deliverables>
    <deliverable type="commit">auth-handler: reads opal-partner-49financial, injects firmId/advisorKey/advisorRole into JWT (J2)</deliverable>
    <deliverable type="commit">portal-authorizer: passes firmId/advisorKey/advisorRole to Lambda context (J3)</deliverable>
    <deliverable type="commit">Terraform: IAM policy attached if needed (J2.3)</deliverable>
    <deliverable type="tag">portal-auth-v{X.Y.Z}</deliverable>
    <deliverable type="document">Session log with verification results for both test cases</deliverable>
  </deliverables>

</task_order>
```
