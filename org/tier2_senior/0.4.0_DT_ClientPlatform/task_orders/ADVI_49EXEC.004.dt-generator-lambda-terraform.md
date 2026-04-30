<task_order>
  <metadata>
    <id>ADVI_49EXEC.004</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DT_ClientPlatform</issued_to>
    <date>2026-04-15</date>
    <status>complete</status><!-- DT 0.4 complete 2026-04-24: exec-summary-v0.0.1, plan 10+0+0, no apply per COO (TO 7 deploys). Session log 137ffb924. Stale flip by CTO 1.0.0_SA_CTO 2026-04-30 — project ADVI_49EXEC COMPLETE. -->
    <project_code>ADVI_49EXEC</project_code>
    <priority>P1 (gates TO 7 deploy)</priority>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADVI_49EXEC.md §4.2 (resources) + §5.3 (IAM) + §7 TO 4</ref>
    <ref type="prereq">ADVI_49EXEC.002 (Lambda code)</ref>
    <ref type="prereq">ADVI_49EXEC.003 (Lambda layer)</ref>
  </references>

  <objective>
    New Terraform module `infra/aws/terraform/exec-summary/`. Resources:
    - `aws_lambda_function.exec_summary_generator` (Python 3.12, memory 1024MB, timeout 900s, concurrency 1, layer = TO 3 layer ARN)
    - IAM role + policy per PRD §5.3 (s3:GetObject platinum/advisors/* + platinum/leaderboards/*; s3:PutObject platinum/advisors/*/exec_summary.json; secretsmanager:GetSecretValue on anthropic-api-key ARN; cloudwatch:PutMetricData)
    - CloudWatch alarms per PRD §5.4 (ExecSummaryTokensIn 2x rolling 7-day average; ExecSummaryAdvisorsProcessed > 5000 hard ceiling)
    - EventBridge rule placeholder (TO 7 wires the actual signal pattern after AE 0.6 confirmation)

    Add Lambda to `infra/aws/lambda/ci/lambda-source-map.json` (CI drift detection).

    New tag series `exec-summary-v{X.Y.Z}` starting at v0.0.1 (TO 7 will tag v0.1.0 on first deploy).

    Do NOT deploy on this TO — final EventBridge wiring + first deploy happens in TO 7. This TO authors the Terraform + Lambda function shell + IAM; 0-diff plan only.
  </objective>

  <scope>
    <files>
      <file action="create">infra/aws/terraform/exec-summary/main.tf</file>
      <file action="create">infra/aws/terraform/exec-summary/iam.tf</file>
      <file action="create">infra/aws/terraform/exec-summary/variables.tf</file>
      <file action="create">infra/aws/terraform/exec-summary/outputs.tf</file>
      <file action="create">infra/aws/terraform/exec-summary/CHANGELOG.json</file>
      <file action="modify">infra/aws/lambda/ci/lambda-source-map.json (add exec-summary-generator entry)</file>
    </files>
  </scope>

  <wire_contract>
    Lambda function deployable but unconnected to EventBridge (placeholder rule). TO 7 wires the actual gold-chain-complete signal pattern.
  </wire_contract>

  <acceptance_criteria>
    1. Terraform module created with all resources per PRD §4.2.
    2. IAM policy matches PRD §5.3 exactly (s3 prefixes + secretsmanager ARN + cloudwatch).
    3. `comp-iam service exec-summary-generator` returns ZERO MISSING permissions.
    4. `comp-iam gaps` (auto-rule for iam.tf change) returns no new gaps elsewhere.
    5. Lambda source map updated with exec-summary-generator entry.
    6. `terraform plan` 0-diff after first apply.
    7. Session log Compiler Tools section reproduces every `<run>` + observed + pass/fail.
    8. MCP COMPLETE to COO + CTO with: tag created (e.g. exec-summary-v0.0.1), terraform plan output, comp-iam transcript, source map entry.
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>comp-iam service exec-summary-generator</run>
        <expect>Lambda not yet known to IAM corpus; baseline.</expect>
        <if_mismatch>If unexpectedly known, reconcile.</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="before commit">
      <step>
        <run>terraform plan</run>
        <expect>Plan shows exec-summary module resources only; no unintended drift.</expect>
        <if_mismatch>Investigate.</if_mismatch>
      </step>
      <step>
        <run>terraform apply</run>
        <expect>Success.</expect>
        <if_mismatch>Surface to COO.</if_mismatch>
      </step>
      <step>
        <run>terraform plan</run>
        <expect>0-diff.</expect>
        <if_mismatch>Drift; fix before tag.</if_mismatch>
      </step>
      <step>
        <run>comp-iam service exec-summary-generator</run>
        <expect>Zero MISSING permissions per PRD §5.3.</expect>
        <if_mismatch>Patch iam.tf.</if_mismatch>
      </step>
      <step>
        <run>comp-iam gaps</run>
        <expect>No new gaps.</expect>
        <if_mismatch>Audit.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    - Lambda code from TO 2 (DS).
    - Layer ARN from TO 3 (AE 0.7).
    - EventBridge wiring deferred to TO 7 (DT + AE 0.6 coord).
    - IAM permissions consumed by Lambda runtime.
  </cross_domain_coordination>

  <dependencies>
    <dependency to="ADVI_49EXEC.002" status="staged"/>
    <dependency to="ADVI_49EXEC.003" status="staged"/>
  </dependencies>

  <next>
    TO 4 close → TO 7 wires EventBridge + first deploy.
  </next>
</task_order>
