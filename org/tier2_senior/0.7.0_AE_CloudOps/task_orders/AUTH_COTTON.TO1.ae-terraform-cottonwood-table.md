<?xml version="1.0" encoding="UTF-8"?>
<task_order>
  <metadata>
    <id>AUTH_COTTON.TO1</id>
    <project>AUTH_COTTON</project>
    <title>Provision opal-partner-cottonwood DynamoDB table via Terraform</title>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_date>2026-04-29</issued_date>
    <status>pending</status>
    <priority>high</priority>
    <estimated_effort>30-60 min</estimated_effort>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/AUTH_COTTON.md</ref>
    <ref type="prd_section">§4.1 + §6 TO-1</ref>
    <ref type="module">infra/aws/terraform/modules/partner-firm-table/</ref>
    <ref type="pattern_file">infra/aws/terraform/partner-firms/inflection.tf (4-line pattern to copy)</ref>
    <ref type="target_dir">infra/aws/terraform/partner-firms/</ref>
    <ref type="current_tag">partner-firms-v1.1.0 (verify: git tag -l "partner-firms-v*" | sort -V | tail -3)</ref>
  </references>

  <context>
    AUTH_COTTON onboards Cottonwood as the third partner firm (after 49F + Inflection).
    This TO is the infrastructure foundation — provisioning the partner DynamoDB table.
    No module changes needed: the existing partner-firm-table module is parameterized on
    firm_id only. firm_id="cottonwood" passes the ^[a-z0-9]+$ regex validator.

    The opalinvest-auth-handler Lambda already resolves the partner table name from
    user.firmId (generalized during Inflection onboarding 2026-04-21). No Lambda code
    change needed.

    Parallelizable with TO-2 (portal firmAccess.ts). TO-3 (DDB seed) gates on this.
  </context>

  <scope>
    CREATE infra/aws/terraform/partner-firms/cottonwood.tf:

    EXACT FILE CONTENTS:
    ---
    # =============================================================================
    # Partner Firm: Cottonwood
    # =============================================================================
    #
    # Onboarded via AUTH_COTTON 2026-04-29.
    #
    # To add a new partner firm: copy this file, change `firm_XX` and `firm_id`.
    # firm_id must be lowercase alphanumeric (module validates).
    # =============================================================================

    module "firm_cottonwood" {
      source  = "../modules/partner-firm-table"
      firm_id = "cottonwood"
    }
    ---

    Then:
    1. terraform plan (must show exactly 1 new resource: aws_dynamodb_table, 0 changes to existing)
    2. terraform apply (confirm apply succeeds)
    3. Verify: aws dynamodb describe-table --table-name opal-partner-cottonwood returns ACTIVE
    4. record-terraform-deploy.sh for partner-firms pipeline
    5. git tag -a partner-firms-v1.2.0 -m "feat(AUTH_COTTON.TO1): provision opal-partner-cottonwood table"
    6. git push --follow-tags

    Working dir for terraform: infra/aws/terraform/partner-firms/
    Use .tools/terraform.exe. Set export MSYS_NO_PATHCONV=1 before terraform commands.
  </scope>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>comp-iam service opalinvest-auth-handler</run>
        <expect>IAM policy includes DynamoDB GetItem/PutItem/Query/Scan on opal-partner-* wildcard
        OR explicit opal-partner-cottonwood grant. If only explicit 49F+Inflection grants exist
        with no wildcard, flag to COO before proceeding (IAM patch needed).</expect>
        <if_mismatch>STOP if no wildcard and cottonwood not listed. Surface IAM gap to COO.</if_mismatch>
      </step>
      <step>
        <run>Read infra/aws/terraform/modules/partner-firm-table/main.tf</run>
        <expect>Module creates aws_dynamodb_table with PK=email (S), GSI=ByAdvisorRole,
        billing_mode=PAY_PER_REQUEST. Tags include Partner=var.firm_id. No new variables
        required — firm_id is the only input.</expect>
        <if_mismatch>STOP. If module has drifted and requires new inputs, surface to COO.</if_mismatch>
      </step>
      <step>
        <run>git tag -l "partner-firms-v*" | sort -V | tail -3</run>
        <expect>Latest tag is partner-firms-v1.1.0. Next tag will be v1.2.0.</expect>
        <if_mismatch>If latest is not v1.1.0, report actual latest — next tag is +1 patch from that.</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="before commit — after terraform apply">
      <step>
        <run>.tools/terraform.exe plan (in infra/aws/terraform/partner-firms/)</run>
        <expect>Plan shows exactly 1 resource to add (aws_dynamodb_table.firm_cottonwood_partner_table
        or similar). 0 to change. 0 to destroy.</expect>
        <if_mismatch>STOP. If plan shows changes to existing resources, do not apply. Surface to COO.</if_mismatch>
      </step>
      <step>
        <run>aws dynamodb describe-table --table-name opal-partner-cottonwood --query "Table.TableStatus" --output text</run>
        <expect>ACTIVE</expect>
        <if_mismatch>STOP. Table not active — check apply output for errors.</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after commit and tag push">
      <step>
        <run>aws dynamodb describe-table --table-name opal-partner-cottonwood --query "Table.{KeySchema:KeySchema,GSIs:GlobalSecondaryIndexes,Billing:BillingModeSummary}" --output json</run>
        <expect>KeySchema=[{email,HASH}], GSI=[ByAdvisorRole], BillingMode=PAY_PER_REQUEST</expect>
        <if_mismatch>Module output mismatch — verify module version; surface to COO.</if_mismatch>
      </step>
      <step>
        <run>git tag -l "partner-firms-v1.2.0"</run>
        <expect>Tag exists and is pushed to origin.</expect>
        <if_mismatch>Re-run: git tag -a partner-firms-v1.2.0 -m "..." && git push --follow-tags</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <acceptance_criteria>
    <criterion id="1">
      aws dynamodb describe-table --table-name opal-partner-cottonwood returns TableStatus=ACTIVE.
      Evidence: command output in session log.
    </criterion>
    <criterion id="2">
      Table schema: KeySchema=[{email,HASH}], GSI=ByAdvisorRole, BillingMode=PAY_PER_REQUEST.
      Evidence: describe-table JSON excerpt in session log.
    </criterion>
    <criterion id="3">
      Table tags include Partner=cottonwood. Evidence: describe-table Tags or aws dynamodb
      list-tags-of-resource output.
    </criterion>
    <criterion id="4">
      git tag -l partner-firms-v1.2.0 exists and is pushed to origin.
      Evidence: git tag + git log output in session log.
    </criterion>
    <criterion id="5">
      terraform plan shows 0 changes after apply (idempotency check).
      Evidence: second plan output showing No changes in session log.
    </criterion>
    <criterion id="6">
      RAVC to 2.0.0_SA_COO with: commit hash, table describe-table excerpt,
      tag confirmation. Include explicit signal that TO-3 (DDB seed) is now unblocked
      on the infrastructure side (partner table exists).
    </criterion>
    <criterion id="7">
      Session log includes Compiler Tools section reproducing all phase mandates
      with observed output and explicit pass/fail vs expect.
    </criterion>
  </acceptance_criteria>

  <dependencies>
    <dependency agent="none" status="none"/>
    Parallelizable with AUTH_COTTON.TO2 (portal edit). No shared files.
    TO-3 (DDB seed) gates on this TO's completion.
  </dependencies>

  <cross_domain_coordination>
    <none/>
    cottonwood.tf is a NEW file — no other active project touches partner-firms/.
  </cross_domain_coordination>

  <commit_identity>
    .tools/safe-commit.sh --author "0.7.0_AE_CloudOps &lt;0.7.0_AE_CloudOps@opal.agent&gt;" \
      -m "feat(AUTH_COTTON.TO1): provision opal-partner-cottonwood DynamoDB table" \
      -- infra/aws/terraform/partner-firms/cottonwood.tf
  </commit_identity>

  <notes>
    Use record-terraform-deploy.sh for CHANGELOG.json entry per CLAUDE.md rule 6.
    Terraform binary: .tools/terraform.exe. State bucket: opal-313476888478-terraform-state.
    Export MSYS_NO_PATHCONV=1 before terraform commands on Git Bash.
    TO-1b (ONBOARDING.md refresh) is a parallelizable ride-along — see separate TO.
  </notes>
</task_order>
