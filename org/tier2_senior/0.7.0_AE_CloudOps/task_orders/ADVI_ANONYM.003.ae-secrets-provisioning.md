<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-04-01-ADVI_ANONYM-003-ae-secrets</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <date>2026-04-01</date>
    <status>pending</status>
    <priority>high</priority>
    <type>infrastructure</type>
    <project>ADVI_ANONYM</project>
  </metadata>

  <objective>
    Provision per-firm HMAC pseudonymization keys in AWS Secrets Manager and
    grant the opal-partners-data Lambda IAM access to read and create them.
    This is the infrastructure prerequisite for ADVI_ANONYM P1. DS will write
    a pseudonymizer module that fetches these keys at runtime; AE ensures the
    keys exist and the Lambda can access them before DT deploys the updated Lambda.
  </objective>

  <references>
    <ref type="prd">docs/architecture/ADVI_ANONYM_PRD.md -- Phase 1, item 4: Per-firm HMAC key provisioning</ref>
    <ref type="iam_file">infra/aws/terraform/partners-api/iam.tf</ref>
    <ref type="lambda_role">opal-partners-data Lambda execution role (check partners-api Terraform for role name)</ref>
  </references>

  <requirements>

    <requirement id="1">
      Query all active firms from DynamoDB opal-users-v2 table:
      ```
      aws dynamodb scan \
        --table-name opal-users-v2 \
        --filter-expression "SK = :meta AND attribute_exists(s3Bucket)" \
        --expression-attribute-values '{":meta":{"S":"META"}}' \
        --projection-expression "firmId" \
        --query "Items[*].firmId.S" \
        --output text
      ```
      This returns the list of active firm IDs that need pseudonymization keys.
    </requirement>

    <requirement id="2">
      For each firm ID returned in Requirement 1, create a Secrets Manager secret
      at path `opal/pseudonym/{firmId}` with a random 256-bit hex key:

      ```bash
      # Generate key and create secret
      KEY=$(python3 -c "import secrets; print(secrets.token_bytes(32).hex())")
      aws secretsmanager create-secret \
        --name "opal/pseudonym/${FIRM_ID}" \
        --secret-string "${KEY}" \
        --description "HMAC pseudonymization key for firm ${FIRM_ID} (ADVI_ANONYM P1)"
      ```

      If the secret already exists (ResourceExistsException), skip it -- do not
      overwrite an existing key (deterministic hashes depend on key stability).

      Log the firm IDs processed and any errors to your session log.
    </requirement>

    <requirement id="3">
      Update the opal-partners-data Lambda execution role IAM policy to include:
      ```json
      {
        "Effect": "Allow",
        "Action": [
          "secretsmanager:GetSecretValue",
          "secretsmanager:CreateSecret"
        ],
        "Resource": "arn:aws:secretsmanager:us-east-1:313476888478:secret:opal/pseudonym/*"
      }
      ```

      Locate the IAM policy in infra/aws/terraform/partners-api/iam.tf.
      Add this statement to the inline policy block for the opal-partners-data role.
      Follow the Terraform deployment sequence (commit -> plan -> apply -> 0-diff -> tag).
      Pipeline: partners-api. Current tag: check `git tag -l "partners-api-v*" | sort -V | tail -5`.
    </requirement>

    <requirement id="4">
      Verify the secrets are accessible from the Lambda execution role after Terraform apply:
      ```bash
      # Simulate Lambda access (use Lambda execution role credentials or test invoke)
      aws secretsmanager get-secret-value \
        --secret-id "opal/pseudonym/${FIRM_ID}" \
        --query SecretString \
        --output text
      ```
      Confirm the secret is retrievable without error.
    </requirement>

    <requirement id="5">
      Commit iam.tf changes with author attribution:
      ```
      git commit --author="0.7.0_AE_CloudOps <0.7.0_AE_CloudOps@opal.agent>" \
          -m "infra(ADVI_ANONYM P1): grant opal-partners-data access to pseudonym secrets"
      ```
      Apply via Terraform. Verify 0-diff. Tag and push per CLAUDE.md protocol.
    </requirement>

    <requirement id="6">
      Write a session log at:
      org/tier2_senior/0.7.0_AE_CloudOps/logs/YYYY-MM-DD/advi_anonym_p1_secrets_provisioning.md

      Include: list of firms provisioned, Terraform tag applied, verification result.
    </requirement>

  </requirements>

  <acceptance_criteria>
    <criterion id="1">Secrets Manager contains `opal/pseudonym/{firmId}` for every active firm in opal-users-v2.</criterion>
    <criterion id="2">opal-partners-data Lambda execution role can call GetSecretValue and CreateSecret on `opal/pseudonym/*` ARN.</criterion>
    <criterion id="3">Terraform at 0-diff after IAM change. partners-api tag incremented and pushed.</criterion>
    <criterion id="4">Secrets retrievable via AWS CLI from the Lambda role -- verified in session log.</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Do NOT overwrite existing `opal/pseudonym/{firmId}` secrets. Skip on ResourceExistsException.</constraint>
    <constraint>Use us-east-1 region for all Secrets Manager operations (Lambda is in us-east-1).</constraint>
    <constraint>Follow Lambda Deployment Protocol for Terraform changes: commit -> plan -> apply -> 0-diff -> tag.</constraint>
    <constraint>Account ID is 313476888478 (verified from Terraform state bucket name).</constraint>
    <constraint>No emojis in code or scripts per CLAUDE.md.</constraint>
  </constraints>

  <dependencies>
    <dependency agent="0.4.0_DS_ClientPlatform" task="ADVI_ANONYM.002.ds-pseudonymizer-lambda" status="staged">
      AE and DS work is parallel. AE provisions infrastructure; DS writes the module that uses it.
      Neither blocks the other. DT deploys after both complete.
    </dependency>
  </dependencies>

  <deliverables>
    <deliverable type="infrastructure">Secrets Manager keys at opal/pseudonym/{firmId} for all active firms</deliverable>
    <deliverable type="terraform">iam.tf updated, partners-api Terraform at 0-diff, new tag pushed</deliverable>
    <deliverable type="document">Session log with firm list, provisioning results, and Terraform tag</deliverable>
  </deliverables>
</task_order>
