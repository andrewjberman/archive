<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-04-06-auth-tfimpt-002-ae</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <date>2026-04-06</date>
    <status>pending</status>
    <project_code>AUTH_TFIMPT</project_code>
  </metadata>

  <objective>
    Import the remaining auth infrastructure into Terraform: opal-users and
    opal-users-v2 DynamoDB tables, SES identity (noreply@opalinvest.dev),
    and Secrets Manager entries (opal/auth/*).
  </objective>

  <scope>
    <files>
      <file action="edit">infra/aws/terraform/portal-auth/dynamodb.tf</file>
      <file action="write">infra/aws/terraform/portal-auth/ses.tf</file>
      <file action="write">infra/aws/terraform/portal-auth/secrets.tf</file>
    </files>
  </scope>

  <deliverables>
    <deliverable id="dynamo-users">
      **DynamoDB: opal-users + opal-users-v2**

      1. Describe both tables via AWS CLI:
         `aws dynamodb describe-table --table-name opal-users`
         `aws dynamodb describe-table --table-name opal-users-v2`
         Capture: key schema, GSIs, billing mode, capacity, TTL, tags.

      2. Add TF resources to `dynamodb.tf` (append to existing file):
         `aws_dynamodb_table.opal_users` and `aws_dynamodb_table.opal_users_v2`

      3. Import:
         `export MSYS_NO_PATHCONV=1`
         `.tools/terraform.exe -chdir=infra/aws/terraform/portal-auth import aws_dynamodb_table.opal_users opal-users`
         `.tools/terraform.exe -chdir=infra/aws/terraform/portal-auth import aws_dynamodb_table.opal_users_v2 opal-users-v2`

      4. Achieve 0-drift.

      Note: opal-users is in BOTH us-east-1 and us-east-2 (see iam.tf policy).
      Import the us-east-1 table. Document the us-east-2 table as a known gap
      (cross-region resources require a second provider block -- flag for future TO).
    </deliverable>

    <deliverable id="ses">
      **SES Identity: noreply@opalinvest.dev**

      1. Check SES identity type:
         `aws ses get-identity-verification-attributes --identities noreply@opalinvest.dev opalinvest.dev`
         Determine if email identity or domain identity.

      2. Write TF resource in `ses.tf`:
         `aws_ses_email_identity.noreply` or `aws_ses_domain_identity.opalinvest_dev`

      3. Import and achieve 0-drift.
    </deliverable>

    <deliverable id="secrets">
      **Secrets Manager: opal/auth/* entries**

      1. List all auth secrets:
         `aws secretsmanager list-secrets --filters Key=name,Values=opal/auth`

      2. Write TF resources in `secrets.tf`. For each secret:
         `aws_secretsmanager_secret.{name}` (manages the secret container only,
         NOT the secret value -- never put secret values in TF code).

      3. Import and achieve 0-drift.

      IMPORTANT: Only import the secret metadata (name, description, tags, rotation config).
      Do NOT import or manage `aws_secretsmanager_secret_version` -- secret values
      stay out of Terraform state.
    </deliverable>
  </deliverables>

  <tooling>
    MANDATORY: Run these compiler modules BEFORE writing TF resources.

    1. **crossref_graph** (org/modules/interpret/crossref_graph.py)
       Scope: infra/aws/terraform/portal-auth/ + all Lambda source dirs that
       reference opal-users, opal-users-v2, SES, or opal/auth secrets.
       Purpose: Map which Lambda functions depend on these resources (via ARN
       strings, table name literals, secret name patterns). The graph confirms
       the IAM policy in iam.tf grants access to the correct table ARNs and
       secret paths -- preventing import of a resource that TF would then
       try to modify because the IAM policy references a different ARN pattern.

    2. **coverage_auditor** (org/modules/adapt/coverage_auditor.py)
       Scope: Run AFTER writing TF resources.
       Source = live DynamoDB tables + SES identities + Secrets (from AWS CLI).
       Registry = TF resources in dynamodb.tf + ses.tf + secrets.tf.
       Purpose: Verify nothing is missed. Catches: tables in us-east-2 that
       aren't in TF (known gap), secrets outside opal/auth/ prefix, etc.
  </tooling>

  <notes>
    - All imports are read-only. Do not apply until 0-diff confirmed.
    - opal-users may have GSIs -- capture all of them in the TF resource.
    - SES identity may have DKIM records -- if domain identity, include
      `aws_ses_domain_dkim` resource.
    - Secrets Manager secrets should only manage the container, never the value.
    - Follow CLAUDE.md: commit before apply, source map, tag.
  </notes>

  <references>
    <ref type="existing_tf">infra/aws/terraform/portal-auth/dynamodb.tf</ref>
    <ref type="existing_tf">infra/aws/terraform/portal-auth/iam.tf</ref>
  </references>

  <dependencies>
    None. Can run in parallel with .001.
  </dependencies>
</task_order>
