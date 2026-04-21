<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-04-21-inflec-w1.4-partner-table</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <date>2026-04-21</date>
    <status>staged</status>
    <project_code>ADVI_INFLEC</project_code>
  </metadata>

  <objective>
    Create `opal-partner-inflection` DynamoDB table (per-partner identity-bridge table read by `opalinvest-auth-handler` at login to inject advisor claims into JWT). Existing `modules/partner-firm-table/main.tf` is parameterized — TO is a one-liner module instantiation mirroring `partner-firms/49financial.tf` exactly. Ships under the `partner-firms` Terraform workspace (same as 49financial.tf), not under inf-pipeline.
  </objective>

  <context>
    ADVI_INFLEC PRD v1.2 §4.2 row 1. CTO confirmed (§8.1 row "Direct TF read") that the module is already parameterized. Precedent `partner-firms/49financial.tf`:

    ```hcl
    module "firm_49financial" {
      source  = "../modules/partner-firm-table"
      firm_id = "49financial"
    }
    ```

    This TO creates `partner-firms/inflection.tf` with identical shape:

    ```hcl
    module "firm_inflection" {
      source  = "../modules/partner-firm-table"
      firm_id = "inflection"
    }
    ```

    Table schema inherited from module: PK=email, attributes advisorKey/advisorName/advisorRole/firmRole/createdAt/createdBy, GSI ByAdvisorRole, PAY_PER_REQUEST billing.

    **Dependency chain:** W1.4 creates the table → W1.5 generalizes `opalinvest-auth-handler` to read any `opal-partner-*` table → W5.5 provisions Inflection user rows in this table. W1.4 and W1.5 can be concurrent if AE is confident generalization doesn't trip existing 49F path (regression test in W5.9).
  </context>

  <compiler_tools_mandate>
    Phase 1 (before writing):
    <run>cat infra/aws/terraform/partner-firms/49financial.tf</run>
    <expect>5-line module block with source=../modules/partner-firm-table and firm_id=49financial. Single source of style.</expect>

    <run>cat infra/aws/terraform/partner-firms/main.tf</run>
    <expect>Backend config + provider. Note the state key.</expect>

    <run>cat infra/aws/terraform/modules/partner-firm-table/variables.tf</run>
    <expect>firm_id variable defined; any validation constraints. Confirm `inflection` satisfies validation (lowercase alphanumeric).</expect>

    Phase 2 (during implementation):
    <run>.tools/terraform.exe plan (from partner-firms/)</run>
    <expect>Plan: 1 to add (aws_dynamodb_table.partner_table named opal-partner-inflection), 0 to change, 0 to destroy. No unexpected modifications.</expect>

    <run>.tools/terraform.exe apply</run>
    <expect>Apply succeeds; table created; 0-diff plan on rerun.</expect>

    Phase 3 (after apply):
    <run>aws dynamodb describe-table --table-name opal-partner-inflection</run>
    <expect>Status ACTIVE. Keyschema PK=email. Attributes [email, advisorRole]. GSI [ByAdvisorRole]. BillingMode PAY_PER_REQUEST. Tags {Project=ADVI, ManagedBy=terraform, Partner=inflection}.</expect>
    <if_mismatch>Any schema deviation vs 49F table = module drift — flag before tagging.</if_mismatch>

    <run>aws dynamodb describe-table --table-name opal-partner-49financial --query 'Table.KeySchema'</run>
    <expect>Identical to inflection — confirms module parity.</expect>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    shared_resource: `infra/aws/terraform/partner-firms/` workspace + modules/partner-firm-table/ module.
    last_write_owner: 0.7.0_AE_CloudOps.
    required_action: "W1.5 (auth-handler generalization) depends on this table existing — can be concurrent but W1.5 cannot deploy until W1.4 applied. If W1.5 deploys first, 49F still works (hardcoded table name) but Inflection login errors silently on missing table. Sequence: W1.4 apply → W1.5 deploy → W5.5 row provisioning."
  </cross_domain_coordination>

  <acceptance_criteria>
    1. Table `opal-partner-inflection` exists with schema identical to `opal-partner-49financial`.
    2. `infra/aws/terraform/partner-firms/inflection.tf` committed — 5-line module block mirroring 49financial.tf.
    3. `terraform apply` 0-diff on rerun.
    4. Tag `partner-firms-v{next}` (check `git tag -l "partner-firms-v*" | sort -V | tail -5` for next increment) pushed with `--follow-tags`.
    5. Session log at `org/tier2_senior/0.7.0_AE_CloudOps/logs/2026-04-{NN}/advi_inflec_w1_4_partner_table.md` with plan/apply output + describe-table parity check.
  </acceptance_criteria>

  <scope>
    <files>
      <file action="create">infra/aws/terraform/partner-firms/inflection.tf</file>
      <file action="reference">infra/aws/terraform/partner-firms/49financial.tf</file>
      <file action="reference">infra/aws/terraform/modules/partner-firm-table/main.tf</file>
      <file action="reference">infra/aws/users/ONBOARDING.md §5 Step 2</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">Mirror `49financial.tf` exactly — only `firm_id` differs. No module source override.</requirement>
    <requirement id="2">Do NOT create table via `aws dynamodb create-table` CLI. Terraform-only per CLAUDE.md Rule 1 + ONBOARDING.md §5 Step 2 "R10 — after AE ships TF module, CLI path is dead".</requirement>
    <requirement id="3">Do NOT provision rows in this TO. Rows ship in W5.5.</requirement>
    <requirement id="4">Tag after deploy per CLAUDE.md Rule 6.</requirement>
    <requirement id="5">Verify `describe-table` matches 49F table schema before tagging.</requirement>
  </requirements>

  <deliverables>
    <deliverable type="commit">`infra/aws/terraform/partner-firms/inflection.tf` — author 0.7.0_AE_CloudOps.</deliverable>
    <deliverable type="tag">`partner-firms-v{next}` with `--follow-tags`.</deliverable>
    <deliverable type="document">Session log.</deliverable>
  </deliverables>

  <do_not>
    <rule>Do NOT `aws dynamodb create-table` CLI.</rule>
    <rule>Do NOT touch modules/partner-firm-table/ — module is already correct.</rule>
    <rule>Do NOT provision rows — W5.5.</rule>
    <rule>Do NOT skip the describe-table parity check vs 49F.</rule>
  </do_not>
</task_order>
