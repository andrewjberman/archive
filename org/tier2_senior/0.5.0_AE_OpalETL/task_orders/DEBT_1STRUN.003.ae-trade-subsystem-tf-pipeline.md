<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-04-06-debt-1strun-003-ae</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.5.0_AE_OpalETL</issued_to>
    <date>2026-04-06</date>
    <status>complete</status>
    <project_code>DEBT_1STRUN</project_code>
  </metadata>

  <objective>
    Create a new Terraform pipeline directory for the trade subsystem and import
    all trade resources into TF state. The trade subsystem is the largest gap
    in the infrastructure audit: 10 Lambdas + 5 S3 buckets + 3 DynamoDB tables
    + 2 IAM roles completely outside Terraform.
  </objective>

  <scope>
    <files>
      <file action="write">infra/aws/terraform/trade-pipeline/main.tf</file>
      <file action="write">infra/aws/terraform/trade-pipeline/lambdas.tf</file>
      <file action="write">infra/aws/terraform/trade-pipeline/s3.tf</file>
      <file action="write">infra/aws/terraform/trade-pipeline/dynamodb.tf</file>
      <file action="write">infra/aws/terraform/trade-pipeline/iam.tf</file>
    </files>
  </scope>

  <deliverables>
    <deliverable id="trade-tf">
      **Trade Subsystem Terraform Pipeline**

      1. **Create pipeline directory**: `infra/aws/terraform/trade-pipeline/`
         S3 backend key: `trade-pipeline/tfstate`
         Follow the reference implementation at `infra/aws/terraform/smartx-pipeline/`.

      2. **Describe all trade resources** via AWS CLI:
         - 10 Lambdas: trade-auth-handler, trade-authorizer, trade-dashboard-api,
           trade-identifier-cache, trade-parquet-batch-export, trade-recon-api,
           trade-recon-auth, trade-recon-authorizer, trade-recon-processor,
           trade-submission-handler, trade-workflow-handler
         - 5 S3 buckets: opal-trade-form-ui, opal-trade-recon-confirms,
           opal-trade-recon-reports, opal-trade-recon-requests, opal-trade-recon-ui
         - 3 DynamoDB: trade-recon-jobs, trade-security-identifiers, trade-users
         - 2 IAM roles: trade-recon-lambda-role, trade-submission-lambda-role

      3. **Write TF resources** matching live config exactly.

      4. **Initialize and import**:
         `export MSYS_NO_PATHCONV=1`
         `.tools/terraform.exe -chdir=infra/aws/terraform/trade-pipeline init`
         Then import each resource.

      5. **Achieve 0-drift** on `terraform plan`.

      6. **Commit, tag** `trade-pipeline-v1.0.0`, push with --follow-tags.
    </deliverable>
  </deliverables>

  <tooling>
    MANDATORY: Run compiler modules BEFORE writing TF.

    1. **crossref_graph** -- Scope: all trade Lambda source dirs + trade S3 buckets.
       Maps dependencies between trade functions (which Lambdas call which DynamoDB
       tables, which read/write which S3 buckets). Prevents missing a resource that
       a Lambda depends on.

    2. **ast_extractor** -- Scope: all 10 trade Lambda source files.
       Extracts imports, function signatures, string literals containing ARNs,
       table names, and bucket names. This IS the resource discovery step.

    3. **coverage_auditor** -- Run AFTER writing TF, BEFORE import.
       Source = live AWS resources (from describe commands).
       Registry = TF resources written.
       Catches any resource you missed.
  </tooling>

  <notes>
    - Trade Lambda source may not exist in the repo. If functions were deployed via
      console, download the code first: `aws lambda get-function --function-name X`
      and save to `infra/aws/lambda/trade/`.
    - Use S3-backed artifact deployment pattern (same as bd-pipeline).
    - Trade subsystem is Pod 3 (TradingOperations) in the org, but TF pipeline
      creation is infrastructure work owned by AE.
    - Follow CLAUDE.md deployment rules strictly. Commit before apply.
  </notes>

  <references>
    <ref type="audit">org/tier2_senior/0.7.0_AE_CloudOps/deliverables/DEBT_1STRUN.001_infrastructure_audit.md</ref>
    <ref type="reference_impl">infra/aws/terraform/smartx-pipeline/</ref>
    <ref type="strategy">infra/aws/TERRAFORM_PIPELINE_STRATEGY.md</ref>
  </references>

  <dependencies>
    <dependency agent="0.5.0_AE_OpalETL" task="DEBT_1STRUN.002" status="pending"/>
  </dependencies>
</task_order>
