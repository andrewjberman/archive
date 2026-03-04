# Task Order: AdvisorIntelligence firmId Auth Refactor — 0.7.0_AE_CloudOps

```xml
<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-03-03-ae-advisor-intelligence-firmid-auth</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <date>2026-03-03</date>
    <status>superseded</status>
    <superseded_by>ADVI-J1-partner-identity-dynamo.md</superseded_by>
    <superseded_date>2026-03-04</superseded_date>
    <superseded_note>
      The Cognito custom:firmId approach is dead. DS A5 investigation confirmed that
      financial architects have no portal accounts at all — there is nothing to attach
      a firmId claim to. The new approach is a per-partner DynamoDB identity table
      (opal-partner-49financial) joined to opal-users-v2 by email. The auth-handler
      reads the partner table at login and injects advisorKey/advisorRole/firmId into
      the JWT. See docs/architecture/PARTNER_IDENTITY_TABLE.md for the full PRD.
    </superseded_note>
  </metadata>

  <objective>
    SUPERSEDED — see ADVI-J1-partner-identity-dynamo.md and
    docs/architecture/PARTNER_IDENTITY_TABLE.md.
    Original objective (Cognito firmId claim) is no longer valid.
  </objective>

  <references>
    <ref>docs/architecture/ADVISOR_INTELLIGENCE_COMPLETION.md</ref>
    <ref>infra/aws/lambda/bd-pipeline/</ref>
    <ref>docs/deployment/LAMBDA_DEPLOYMENT_PROTOCOL.md</ref>
  </references>

  <scope>
    <files>
      <!-- AE owns Cognito config; DT owns Lambda update (opal-partners-data) -->
      <file action="investigate">infra/aws/terraform/ (Cognito user pool custom attributes)</file>
      <file action="modify">infra/aws/terraform/ (relevant Cognito or API Gateway authorizer config)</file>
    </files>
  </scope>

  <requirements>

    <!-- ================================================================ -->
    <!-- PART 1 — Cognito custom:firmId claim configuration               -->
    <!-- ================================================================ -->
    <requirement id="J-AE.1">
      Verify whether the Cognito User Pool already has a custom:firmId attribute
      defined on user records for 49 Financial advisors.
      Read the relevant Terraform (aws_cognito_user_pool or similar) to confirm.
    </requirement>
    <requirement id="J-AE.2">
      If custom:firmId does NOT exist:
        Add the custom attribute to the Cognito user pool via Terraform.
        Ensure it is included in the ID token claims.
      If it DOES exist:
        Confirm it is included in the ID token and passes through the API Gateway
        JWT authorizer into requestContext.authorizer for Lambda consumption.
    </requirement>
    <requirement id="J-AE.3">
      Confirm that the API Gateway authorizer (for the scoped advisor endpoints)
      is configured to pass Cognito token claims into the Lambda requestContext.
      If not: update the authorizer configuration via Terraform.
    </requirement>
    <requirement id="J-AE.4">
      Document findings and any Terraform changes in your session log.
      Write a brief spec note (2-3 sentences) for 0.4.0_DT describing:
        - The exact key in requestContext.authorizer where firmId will appear
          (e.g., requestContext.authorizer.claims['custom:firmId'])
        - Whether the claim is already populated for test users or needs new user records
      DT needs this to implement the Lambda-side read.
    </requirement>

    <!-- ================================================================ -->
    <!-- PART 2 — opal-users-v2 advisory (coordinate with DS A5)         -->
    <!-- ================================================================ -->
    <requirement id="J-AE.5">
      Coordinate with 0.4.0_DS_ClientPlatform after their A5 investigation completes.
      DS will surface whether the JWT userId in opal-users-v2 maps to an advisor identity
      in the gold layer. If a new data registration step is needed (new opal-users-v2
      record schema or new mapping table), AE CloudOps owns that infrastructure change.
      Wait for DS A5 findings before designing any new data linkage.
    </requirement>
    <requirement id="J-AE.6">
      If a new opal-users-v2 table schema or DynamoDB index is needed for advisor identity
      resolution: design it in coordination with DS and document in your session log
      before any Terraform changes. Flag to COO if this becomes a significant scope item.
    </requirement>

  </requirements>

  <acceptance_criteria>
    <criterion id="1">Cognito custom:firmId attribute exists on user pool and is included in ID token claims.</criterion>
    <criterion id="2">API Gateway authorizer passes Cognito claims into Lambda requestContext.authorizer.</criterion>
    <criterion id="3">DT has a written spec note with the exact requestContext key for firmId.</criterion>
    <criterion id="4">opal-users-v2 advisor identity mapping gap (if any) documented and flagged to COO.</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>This stream is NOT blocking AdvisorIntelligence completion — do not prioritize above your active infrastructure_inventory task order.</constraint>
    <constraint>Schedule after DT Streams B1 and B2 are confirmed deployed by 0.4.0_DT.</constraint>
    <constraint>Do NOT modify opal-users-v2 table data (only schema/index if needed). User data is not within scope here.</constraint>
    <constraint>Coordinate with 0.4.0_DT on the Lambda-side firmId read — AE configures the claim, DT implements the Lambda change.</constraint>
    <constraint>All Terraform changes follow standard protocol: plan -&gt; apply -&gt; 0-diff -&gt; tag -&gt; push.</constraint>
    <constraint>Do NOT use emojis in any code or log output.</constraint>
    <constraint>Commit with: git commit --author="0.7.0_AE_CloudOps &lt;0.7.0_AE_CloudOps@opal.agent&gt;" -m "..."</constraint>
  </constraints>

  <dependencies>
    <dependency agent="0.4.0_DS_ClientPlatform" task="advisor_intelligence_completion" status="pending" note="J-AE.5 waits for DS A5 opal-users-v2 findings"/>
    <dependency agent="0.4.0_DT_ClientPlatform" task="advisor_intelligence_completion" status="pending" note="Lambda-side firmId read is DT scope; AE provides claim spec"/>
  </dependencies>

  <deliverables>
    <deliverable type="commit">Terraform: Cognito custom:firmId claim configured and in ID token</deliverable>
    <deliverable type="commit">Terraform: API Gateway authorizer passes claims to Lambda context (if change needed)</deliverable>
    <deliverable type="document">Session log with J-AE findings + DT spec note for Lambda-side firmId key</deliverable>
  </deliverables>
</task_order>
```
