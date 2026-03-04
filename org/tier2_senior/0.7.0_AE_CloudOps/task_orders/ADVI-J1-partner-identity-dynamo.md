# Task Order: ADVI-J1 — opal-partner-49financial DynamoDB Table — 0.7.0_AE_CloudOps

```xml
<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-03-04-ADVI-J1-partner-identity-dynamo</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <date>2026-03-04</date>
    <status>pending</status>
    <priority>HIGH — unblocks DT J2/J3 auth stream</priority>
  </metadata>

  <objective>
    Create the opal-partner-49financial DynamoDB table via Terraform in shared-infra.
    This table is the identity bridge between portal users (opal-users-v2) and the
    BD gold layer advisor identity (advisorKey, advisorRole). The auth-handler Lambda
    (owned by DT, Stream J2) will read this table at login time.

    No data population in this task. Table is created empty. Population is a separate
    manual admin operation at advisor onboarding time.
  </objective>

  <references>
    <ref type="prd" priority="PRIMARY">docs/architecture/PARTNER_IDENTITY_TABLE.md</ref>
    <ref type="terraform-module">infra/aws/terraform/shared-infra/</ref>
    <ref type="terraform-strategy">infra/aws/TERRAFORM_PIPELINE_STRATEGY.md</ref>
    <ref type="lambda-deploy-protocol">docs/deployment/LAMBDA_DEPLOYMENT_PROTOCOL.md</ref>
    <ref type="current-shared-infra-tag">shared-infra-v1.2.0</ref>
  </references>

  <requirements>

    <!-- ================================================================ -->
    <!-- PART 1 — DynamoDB Table Resource                                 -->
    <!-- ================================================================ -->
    <requirement id="J1.1">
      Add aws_dynamodb_table resource to infra/aws/terraform/shared-infra/ with these
      exact specifications (from PRD Section 2A):

        resource name: opal_partner_49financial
        table name:    opal-partner-49financial
        billing_mode:  PAY_PER_REQUEST
        hash_key:      email (String) — simple partition key, no sort key

        attributes:
          email       String  (hash_key)
          advisorRole String  (used by GSI)

        GSI:
          name:            ByAdvisorRole
          hash_key:        advisorRole
          projection_type: ALL
          billing_mode:    PAY_PER_REQUEST

        tags:
          Project:    ADVI
          ManagedBy:  terraform
          Partner:    49financial
    </requirement>

    <requirement id="J1.2">
      Increment the shared-infra module version in the Terraform configuration.
      Current tag is shared-infra-v1.2.0 -> next tag will be shared-infra-v1.3.0.
    </requirement>

    <!-- ================================================================ -->
    <!-- PART 2 — IAM Policy for auth-handler Lambda                      -->
    <!-- ================================================================ -->
    <requirement id="J1.3">
      Add an aws_iam_role_policy resource to infra/aws/terraform/shared-infra/main.tf
      granting the auth-handler Lambda role read access to opal-partner-49financial.

      Placement: shared-infra/main.tf — same file as the table. Same Terraform apply.
      Do NOT touch infra/aws/terraform/portal-auth/iam.tf. That file manages the base
      opalinvest-auth-permissions policy. Adding a second inline policy from shared-infra
      is valid AWS (a role can have multiple inline policies with different names).

      Pattern to follow: the existing portal_lambda_ec2_snapshot resource in main.tf
      attaches to "opal-portal-lambda-role" by name string. Use the identical pattern:

        resource "aws_iam_role_policy" "partner_identity_read" {
          name = "PartnerIdentityReadPermissions"
          role = "opalinvest-auth-lambda-role"
          policy = jsonencode({ ... })
        }

      Required DynamoDB actions:
        - dynamodb:GetItem   (read by email PK — primary auth lookup)
        - dynamodb:Query     (GSI ByAdvisorRole — admin enumeration use case)

      Resources: use Terraform references, not hardcoded ARNs:
        - aws_dynamodb_table.opal_partner_49financial.arn
        - "${aws_dynamodb_table.opal_partner_49financial.arn}/index/*"

      The auth-handler role name "opalinvest-auth-lambda-role" is confirmed in:
        infra/aws/terraform/portal-auth/iam.tf line 16 (resource "aws_iam_role" "auth_handler")
    </requirement>

    <!-- ================================================================ -->
    <!-- PART 3 — Plan, Apply, Tag                                        -->
    <!-- ================================================================ -->
    <requirement id="J1.4">
      Follow the standard Terraform deploy sequence:
        1. terraform plan (verify only new resources — no changes to existing ones)
        2. terraform apply
        3. Confirm 0-diff plan on second apply
        4. git tag -a shared-infra-v1.3.0 -m "feat(shared-infra): opal-partner-49financial DynamoDB + IAM (ADVI-J1)"
        5. git push --follow-tags
    </requirement>

    <requirement id="J1.5">
      After apply: verify the table exists in DynamoDB console (or via AWS CLI):
        aws dynamodb describe-table --table-name opal-partner-49financial --region us-east-1
      Confirm hash_key=email, GSI ByAdvisorRole present.
      Document the table ARN in your session log (DT will reference it for J2 IAM).
    </requirement>

  </requirements>

  <acceptance_criteria>
    <criterion id="1">opal-partner-49financial DynamoDB table exists with email PK and ByAdvisorRole GSI.</criterion>
    <criterion id="2">IAM read access granted to auth-handler Lambda role (GetItem + Query).</criterion>
    <criterion id="3">shared-infra-v1.3.0 tag applied and pushed.</criterion>
    <criterion id="4">Table ARN documented in session log for DT J2 reference.</criterion>
    <criterion id="5">Second terraform apply produces 0 changes.</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Do NOT populate table data. Empty table is the correct deliverable.</constraint>
    <constraint>Do NOT modify opal-users-v2 or any existing DynamoDB tables.</constraint>
    <constraint>Do NOT use emojis in any code, Terraform, or log output.</constraint>
    <constraint>Follow LAMBDA_DEPLOYMENT_PROTOCOL.md for any Lambda IAM changes.</constraint>
    <constraint>Commit before apply. Sequence: code -> commit -> plan -> apply -> tag -> push.</constraint>
    <constraint>Commit with: git commit --author="0.7.0_AE_CloudOps &lt;0.7.0_AE_CloudOps@opal.agent&gt;" -m "..."</constraint>
    <constraint>export MSYS_NO_PATHCONV=1 before any Terraform commands with ARN paths on Git Bash (Windows).</constraint>
  </constraints>

  <dependencies>
    <!-- No dependencies — J1 is the root of the J1->J2->J3 chain -->
  </dependencies>

  <deliverables>
    <deliverable type="commit">Terraform: aws_dynamodb_table.opal_partner_49financial in shared-infra</deliverable>
    <deliverable type="commit">Terraform: IAM policy granting auth-handler read access to new table</deliverable>
    <deliverable type="tag">shared-infra-v1.3.0</deliverable>
    <deliverable type="document">Session log with table ARN + apply output + verification results</deliverable>
  </deliverables>

  <handoff_to_dt>
    When J1 is complete, notify 0.4.0_DT_ClientPlatform that the table exists and J2 is unblocked.
    Provide in your session log:
      - Table ARN (arn:aws:dynamodb:us-east-1:313476888478:table/opal-partner-49financial)
      - IAM status (attached to auth-handler role, or attachment point for DT to complete in J2)
  </handoff_to_dt>

</task_order>
```
