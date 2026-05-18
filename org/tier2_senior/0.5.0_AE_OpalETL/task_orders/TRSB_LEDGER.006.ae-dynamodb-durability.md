<task_order>
  <metadata>
    <id>TRSB_LEDGER.006</id>
    <slug>ae-dynamodb-durability</slug>
    <issued_by>2.0.0_SA_COO~B</issued_by>
    <issued_to>0.5.0_AE_OpalETL</issued_to>
    <date>2026-05-18</date>
    <status>pending</status>
    <dispatch_held>false</dispatch_held>
    <dispatch_unblock_condition>GO 2026-05-18 (COO~B decomposition of TRSB_LEDGER PRD v0.1). Phase 2 -- pure Terraform table-config change on dynamodb.tf, runs CONCURRENT with the AE 0.7.0 backend lane. The only real parallelism in this PRD (CTO~B 2026-05-18).</dispatch_unblock_condition>
    <project_code>TRSB_LEDGER</project_code>
    <priority>P1 -- Pillar C. Closes hole B8 (the system-of-record table has no durability protections). Near-zero cost, table-stakes for a record-keeping system.</priority>
    <sla>1d wall -- a Terraform table-config change, no data migration.</sla>
  </metadata>

  <references>
    <prd>docs/architecture/TRSB_LEDGER.md (v0.1) -- section 2.B B8; section 3.6 (durability); section 6 TO-6.</prd>
  </references>

  <objective>
    Give the trade system-of-record DynamoDB tables point-in-time recovery and deletion protection. `aws_dynamodb_table.trade_submissions` and `trade_users` today have neither -- for a system where Andrew called record-keeping "crucial", 35-day continuous PITR and deletion protection are table-stakes.
  </objective>

  <context>
    `infra/aws/terraform/trade-pipeline/dynamodb.tf`: `aws_dynamodb_table.trade_submissions` (and `trade_users`) have neither `point_in_time_recovery` nor `deletion_protection_enabled`. This is a pure Terraform table-config change -- no data migration, no Lambda source, near-zero cost.

    CONCURRENCY NOTE: TRSB_LEDGER.005 (AE 0.7.0) also edits dynamodb.tf -- it repoints the `by-approver` GSI. TO-6 and TO-5 edit DIFFERENT stanzas of the same file (TO-6 = table-level attributes; TO-5 = GSI definitions) but must coordinate so neither clobbers the other. TO-6 is small and fast -- recommended to land FIRST so TO-5 rebases its GSI changes on a dynamodb.tf that already carries the durability attributes.
  </context>

  <scope>
    <step>Phase 1 -- Direct read dynamodb.tf: confirm `trade_submissions` and `trade_users` lack `point_in_time_recovery` and `deletion_protection_enabled`. MCP AE 0.7.0 (TO-5) to agree edit ordering on dynamodb.tf before writing.</step>
    <step>Phase 2 -- Add `point_in_time_recovery { enabled = true }` and `deletion_protection_enabled = true` to `aws_dynamodb_table.trade_submissions` and `aws_dynamodb_table.trade_users`.</step>
    <step>Phase 2 -- terraform plan: the plan must show ONLY the four attribute additions (two per table), nothing else.</step>
    <step>Phase 3 -- terraform apply; commit per CLAUDE.md Rules 1-6 (commit -> plan -> apply -> 0-diff -> tag -> push --follow-tags). Verify PITR is ENABLED via the AWS API.</step>
  </scope>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>Direct read: infra/aws/terraform/trade-pipeline/dynamodb.tf -- trade_submissions + trade_users table stanzas</run>
        <expect>Neither table currently declares point_in_time_recovery or deletion_protection_enabled. comp-* tools N/A (trade pipeline uninstrumented, PRD §5).</expect>
        <if_mismatch>If either attribute is already present, narrow the TO to the table(s) genuinely missing it and note so in the session log.</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="before commit">
      <step>
        <run>.tools/terraform.exe plan</run>
        <expect>The plan shows exactly four attribute additions: point_in_time_recovery + deletion_protection_enabled on trade_submissions, same two on trade_users. No GSI changes, no key-schema changes, no other resource touched. (If TO-5 has already landed its GSI change, the plan still shows only the four durability attributes.)</expect>
        <if_mismatch>If the plan shows anything beyond the four attributes -- especially a GSI delta -- STOP. Pull latest dynamodb.tf, reconcile with TO-5's changes, and re-plan. Do not apply a plan that touches a GSI.</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after commit">
      <step>
        <run>aws dynamodb describe-continuous-backups --table-name opal-trade-submissions (and trade-users table)</run>
        <expect>ContinuousBackupsStatus ENABLED and PointInTimeRecoveryStatus ENABLED for both tables.</expect>
        <if_mismatch>If PITR is not ENABLED, the apply did not take -- re-check the terraform state and re-apply.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <data_reprocess_scope>
    <no_reprocess_needed>Pure table-configuration change -- no data migration, no schema change to items, no Lambda source, no S3 prefix. Existing data is untouched; PITR begins its 35-day window from enable time.</no_reprocess_needed>
  </data_reprocess_scope>

  <cross_domain_coordination>
    shared_resource: infra/aws/terraform/trade-pipeline/dynamodb.tf
    also_in_to: TRSB_LEDGER.005 (AE 0.7.0 -- by-approver GSI repoint, edits the GSI stanzas of the same file)
    last_write_owner: TO-6 and TO-5 edit different stanzas of dynamodb.tf. Recommended order: TO-6 lands first (small, table-attribute-only); TO-5 rebases its GSI changes on top.
    required_action: AE 0.5.0 (this TO) MCP AE 0.7.0 (TO-5) before committing dynamodb.tf. Whoever commits second pulls latest and confirms their terraform plan isolates to their own change.
  </cross_domain_coordination>

  <acceptance_criteria>
    <ac id="AC1">`aws_dynamodb_table.trade_submissions` and `aws_dynamodb_table.trade_users` both declare `point_in_time_recovery { enabled = true }` and `deletion_protection_enabled = true`.</ac>
    <ac id="AC2">terraform plan before apply shows exactly the four attribute additions and nothing else -- no GSI or key-schema delta.</ac>
    <ac id="AC3">`aws dynamodb describe-continuous-backups` confirms PointInTimeRecoveryStatus ENABLED for both tables post-apply.</ac>
    <ac id="AC4">Deployed via terraform apply with a 0-diff-after plan; pipeline git tag applied; pushed with --follow-tags. dynamodb.tf edit coordinated with TO-5 per cross_domain_coordination.</ac>
    <ac id="AC5">No emoji. Session log with the Compiler Tools section. RAVC2 to 2.0.0_SA_COO~B.</ac>
  </acceptance_criteria>

  <scope_files>
    <file action="modify">infra/aws/terraform/trade-pipeline/dynamodb.tf</file>
  </scope_files>

  <deliverables>
    <deliverable type="commit">dynamodb.tf PITR + deletion-protection on trade_submissions + trade_users, deployed via terraform apply (0-diff plan), pipeline tag applied + pushed.</deliverable>
    <deliverable type="document">Session log with the Compiler Tools section. RAVC2 to 2.0.0_SA_COO~B.</deliverable>
  </deliverables>

  <do_not>
    <rule>Do not commit dynamodb.tf without coordinating with AE 0.7.0 (TO-5) -- both TOs touch that file.</rule>
    <rule>Do not apply a terraform plan that shows a GSI delta -- that would mean an unreconciled collision with TO-5.</rule>
    <rule>Do not deploy outside Terraform (CLAUDE.md Rule 1).</rule>
  </do_not>
</task_order>
