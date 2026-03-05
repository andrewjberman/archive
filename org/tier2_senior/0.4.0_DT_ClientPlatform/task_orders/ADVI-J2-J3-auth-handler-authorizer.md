# Task Order: ADVI-J2/J3 — Auth-Handler + Portal-Authorizer Partner Identity — 0.4.0_DT_ClientPlatform

```xml
<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-03-04-ADVI-J2-J3-auth-handler-authorizer</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DT_ClientPlatform</issued_to>
    <date>2026-03-04</date>
    <status>complete</status>
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
      Files to modify (all TypeScript — auth-handler is Node.js/TS, not Python):
        - infra/aws/opalinvest_dev/lambda/auth-handler/src/db.ts
        - infra/aws/opalinvest_dev/lambda/auth-handler/src/types.ts
        - infra/aws/opalinvest_dev/lambda/auth-handler/src/jwt.ts
        - infra/aws/opalinvest_dev/lambda/auth-handler/src/auth.ts

      Read all four files in full before making any changes.

      db.ts — add a new function using the existing docClient (DynamoDBDocumentClient):

        const PARTNER_TABLE_49FIN = 'opal-partner-49financial'

        export async function getPartnerIdentity(email: string): Promise&lt;{
          advisorKey: string
          advisorName: string
          advisorRole: string
        } | null&gt; {
          const response = await docClient.send(
            new GetCommand({
              TableName: PARTNER_TABLE_49FIN,
              Key: { email },
            })
          )
          if (!response.Item) return null
          return {
            advisorKey:  response.Item.advisorKey  as string,
            advisorName: response.Item.advisorName as string,
            advisorRole: response.Item.advisorRole as string,
          }
        }

      types.ts — add three optional fields to AccessTokenPayload:
        advisorKey?:  string   // BD gold layer advisor slug (e.g., "arch_jane_smith")
        advisorName?: string   // Display name (e.g., "Jane Smith")
        advisorRole?: string   // "architect" | "implementor" | "admin" | "viewer"

      jwt.ts — update generateAccessToken signature to accept optional partner identity:
        export async function generateAccessToken(
          user: User,
          partnerIdentity?: { advisorKey: string; advisorName: string; advisorRole: string } | null
        ): Promise&lt;string&gt;

        Add to payload spread (after allowedTabs):
          ...(partnerIdentity &amp;&amp; {
            advisorKey:  partnerIdentity.advisorKey,
            advisorName: partnerIdentity.advisorName,
            advisorRole: partnerIdentity.advisorRole,
          }),

      auth.ts — update login() and refresh() to call getPartnerIdentity when needed:

        TRIGGER: user.allowedPages?.includes('advisor-intelligence')
          (this is how auth-handler knows the user is a 49 Financial advisor)

        In login() after getUser() succeeds:
          let partnerIdentity = null
          if (user.allowedPages?.includes('advisor-intelligence')) {
            try {
              partnerIdentity = await getPartnerIdentity(user.email)
            } catch (err) {
              console.error('WARN: partner identity lookup failed, continuing without:', err)
              // Do not fail the login on partner table error
            }
          }
          const accessToken = await generateAccessToken(user, partnerIdentity)

        Apply the same pattern to refresh() — getPartnerIdentity after getUser().

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
      IAM: AE (J1) attaches the PartnerIdentityReadPermissions policy to role
      opalinvest-auth-lambda-role directly from shared-infra/main.tf. DT does NOT
      need to add any IAM. Verify this is in place by checking AE's J1 session log
      confirms "PartnerIdentityReadPermissions" policy is live on the role before
      you run terraform plan for portal-auth. If AE's log does not confirm this,
      the plan will succeed but the Lambda will get AccessDenied at runtime — stop
      and wait for AE J1 to fully complete first.
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

      Specific change in index.mjs: in the context object (currently lines 194-206),
      add three new fields using the same null-coalescing pattern as existing fields:

        advisorKey:  decoded.advisorKey  || 'null',
        advisorName: decoded.advisorName || 'null',
        advisorRole: decoded.advisorRole || 'null',

      After J3, scoped Lambdas read advisor identity from:
        event.requestContext.authorizer.advisorKey
        event.requestContext.authorizer.advisorRole
        event.requestContext.authorizer.firmId    (already present in context)
    </requirement>

    <!-- ================================================================ -->
    <!-- DEPLOY — Both Lambdas via portal-auth Terraform module           -->
    <!-- ================================================================ -->
    <requirement id="J2J3.deploy">
      Deploy both Lambdas via the portal-auth Terraform module. Deploy J2 and J3 as
      separate apply cycles (J2 first, verify, then J3) to match the dependency order.

      Current portal-auth tag: portal-auth-v1.0.0 (commit 1660ed82, deployed 2026-03-03).
      Next tags: portal-auth-v1.1.0 for J2, portal-auth-v1.2.0 for J3.

      J2 deploy sequence (auth-handler):
        1. Commit auth-handler source changes (db.ts, types.ts, jwt.ts, auth.ts)
           git commit --author="0.4.0_DT_ClientPlatform ..."
        2. Compile TypeScript (REQUIRED before build-and-upload.sh):
           cd infra/aws/opalinvest_dev/lambda/auth-handler
           npm run build
           (produces dist/*.js from src/*.ts — source map lists dist/ files)
        3. Build + upload artifact:
           bash infra/aws/lambda/ci/build-and-upload.sh portal-auth opalinvest-auth-handler
        4. Commit updated source map:
           git add infra/aws/lambda/ci/lambda-source-map.json
           git commit --author="0.4.0_DT_ClientPlatform ..." -m "ci: upload artifacts [skip ci]"
        5. terraform plan + apply (infra/aws/terraform/portal-auth)
        6. 0-diff verify
        7. Update deployment_map.xml, record-terraform-deploy.sh, tag portal-auth-v1.1.0, push

      J3 deploy sequence (portal-authorizer) — after J2 verified:
        1. Commit portal-authorizer source change (index.mjs)
        2. Build + upload artifact (index.mjs needs no compilation):
           bash infra/aws/lambda/ci/build-and-upload.sh portal-auth opal-portal-authorizer
        3. Commit updated source map
        4. terraform plan + apply + 0-diff
        5. Update deployment_map.xml, record-terraform-deploy.sh, tag portal-auth-v1.2.0, push

      Export before any Terraform or AWS CLI:
        export MSYS_NO_PATHCONV=1
        export AWS_EC2_METADATA_DISABLED=true
    </requirement>

    <!-- ================================================================ -->
    <!-- VERIFICATION                                                      -->
    <!-- ================================================================ -->
    <requirement id="J2J3.verify">
      After J2 deploy:
        1. Insert one test record into opal-partner-49financial to enable testing:
             aws dynamodb put-item --table-name opal-partner-49financial \
               --item '{"email":{"S":"test-advisor@49financial.com"},
                        "advisorKey":{"S":"arch_test"},
                        "advisorName":{"S":"Test Advisor"},
                        "advisorRole":{"S":"architect"},
                        "createdAt":{"S":"2026-03-04T00:00:00Z"},
                        "createdBy":{"S":"DT-J2-test"}}'
           (This is a temp test record — not a real advisor. Remove after verification.)
        2. Trigger a login as a user whose email IS in opal-partner-49financial AND
           has "advisor-intelligence" in allowedPages. Decode the JWT (jwt.io or aws logs)
           and verify: firmId="49financial", advisorKey="arch_test", advisorRole="architect".
        3. Trigger a login for a user whose email is NOT in opal-partner-49financial.
           Verify login succeeds and JWT does NOT contain advisorKey/advisorRole.
        4. After J3 deploy: confirm portal-authorizer passes the claims to Lambda context.
           Read a scoped Lambda's CloudWatch logs and confirm advisorKey appears in
           event.requestContext.authorizer for the test advisor user.

      Note: table starts EMPTY after J1. You must insert the test record above before
      any JWT-level verification is possible.

      Document verification results in session log. Remove the test record after testing.
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
