# Task Order: SSCN — Terraform Infrastructure

```xml
<task_order>
  <metadata>
    <id>0.3.0_DE_TradingOperations-2026-03-05-sscn-terraform-infra</id>
    <issued_by>0.3.0_DE_TradingOperations</issued_by>
    <issued_to>0.5.0_AE_OpalETL</issued_to>
    <date>2026-03-05</date>
    <status>complete</status>
    <thread_serial>SSCN_PORTAL-001</thread_serial>
    <thread_ref>org/tier2_senior/0.5.0_AE_OpalETL/threads/SSCN_PORTAL-001-pattern-0-security-scanner-data-architec_0.3.0_DS_TradingOperations+0.3.0_DE_TradingOperations.md</thread_ref>
  </metadata>

  <objective>
    Provision all AWS infrastructure for the Security Scanner pipeline via Terraform:
    the processing Lambda (triggered by S3 upload), the S3 event notification, IAM permissions,
    the Lambda Layer for Python dependencies, and the presign API route extension. DS delivers
    the Lambda source; AE deploys it. Follow the mandatory Terraform deployment protocol
    (CLAUDE.md rules 1-6 + infra/aws/TERRAFORM_PIPELINE_STRATEGY.md).
  </objective>

  <scope>
    <files>
      <file action="create">infra/aws/terraform/security-scanner-pipeline/main.tf</file>
      <file action="create">infra/aws/terraform/security-scanner-pipeline/variables.tf</file>
      <file action="create">infra/aws/terraform/security-scanner-pipeline/outputs.tf</file>
      <file action="create">infra/aws/terraform/security-scanner-pipeline/backend.tf</file>
      <file action="create">infra/aws/terraform/security-scanner-pipeline/CHANGELOG.json</file>
      <file action="modify">infra/aws/lambda/ci/lambda-source-map.json</file>
      <!-- If extending opal-data-refresh-api for presign route: -->
      <file action="modify">infra/aws/lambda/opal_data_refresh_api/lambda_function.py</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">
      READ BEFORE STARTING:
      - org/ref/LAMBDA_DEPLOYMENT_PROTOCOL.md (mandatory Lambda deploy protocol)
      - infra/aws/TERRAFORM_PIPELINE_STRATEGY.md (S3 backend, naming conventions, module pattern)
      - infra/aws/terraform/smartx-pipeline/ (reference implementation — use as structural template)
      - infra/aws/lambda/ci/lambda-source-map.json (every Lambda must have an entry here)
      - SSCN_DATA_CONTRACT.md Section 9 for Lambda sizing: 2048 MB memory, 300s timeout
      - SSCN_PORTAL-001 AE turn 8 for full infra convergence decisions

      Confirm DS has committed infra/aws/lambda/opal_security_scanner_processor/lambda_function.py
      before starting Terraform. Do not begin plan/apply until source exists.
    </requirement>
    <requirement id="2">
      TERRAFORM MODULE: infra/aws/terraform/security-scanner-pipeline/
      Backend: S3 state bucket opal-313476888478-terraform-state, key: security-scanner/tfstate
      Use .tools/terraform.exe binary (v1.9.8). Set export MSYS_NO_PATHCONV=1 before plan/apply.
      Follow the S3-backed Lambda zip deployment pattern (build-and-upload.sh → artifact in
      opal-313476888478-lambda-artifacts/security-scanner/opal-security-scanner-processor.zip).
    </requirement>
    <requirement id="3">
      PROCESSING LAMBDA: opal-security-scanner-processor
      Runtime: Python 3.12 (or match the runtime of existing pandas-using Lambdas in yang-pipeline)
      Memory: 2048 MB
      Timeout: 300s
      Source: infra/aws/lambda/opal_security_scanner_processor/lambda_function.py
      S3 artifact key: security-scanner/opal-security-scanner-processor.zip
      Handler: lambda_function.lambda_handler
    </requirement>
    <requirement id="4">
      LAMBDA LAYER: security-scanner-deps
      Build a new layer zip from infra/aws/lambda/opal_security_scanner_processor/requirements.txt
      (pandas + openpyxl). Do NOT reuse the news-trending-deps or yang layers without confirming
      compatibility. Upload to opal-313476888478-lambda-layers/security-scanner-deps.zip.
      Register as an aws_lambda_layer_version resource in the module.
      Attach to the processing Lambda.
    </requirement>
    <requirement id="5">
      S3 EVENT NOTIFICATION:
      The processing Lambda must be triggered by ObjectCreated events on:
        Bucket: opal-data-portal-v2
        Prefix: security_scanner/uploads/
        Suffix: .xlsx
      S3 event notifications for opal-data-portal-v2 are owned by
      infra/aws/terraform/portal-notifications/ (see MEMORY.md: portal-notifications owns ALL
      S3 triggers on opal-data-portal-v2). Register the SSCN trigger there, not in the
      security-scanner-pipeline module. If portal-notifications requires changes, include
      those in this task order's Terraform work.
      IAM: add Lambda resource policy (aws_lambda_permission) allowing S3 to invoke the Lambda.
    </requirement>
    <requirement id="6">
      IAM PERMISSIONS for the processing Lambda execution role:
      Allow:
        s3:GetObject on arn:aws:s3:::opal-data-portal-v2/security_scanner/uploads/*
        s3:PutObject on arn:aws:s3:::opal-data-portal-v2/json/security_scanner/*
        logs:CreateLogGroup, logs:CreateLogStream, logs:PutLogEvents (CloudWatch)
      Deny: all other S3 access (least-privilege).
    </requirement>
    <requirement id="7">
      PRESIGN ROUTE for portal upload (DataRefresh-style):
      Extend the existing opal-data-refresh-api Lambda to handle a new path:
        POST /api/scoped/security-scanner/upload-url
        Request body: { asOf: string }    (format: YYYYMMDD or YYYY-MM-DD)
        Response: { uploadUrl: string, s3Key: string }
        S3 presigned PUT target:
          opal-data-portal-v2/security_scanner/uploads/{asOf}/Screening_DIVZ_IDVZ_{asOf}.xlsx
        Expiry: 15 minutes (match DataRefresh presign TTL)

      Implement the route handler in infra/aws/lambda/opal_data_refresh_api/lambda_function.py.
      Auth: scoped (Dev claim enforced; same mechanism as other /api/scoped/* routes).

      If extending opal-data-refresh-api is blocked or creates unacceptable risk to the existing
      DataRefresh flow, create a new minimal Lambda (opal-security-scanner-api) for the presign
      route only and note the decision in your session log. AE recommendation from SSCN_PORTAL-001
      turn 5 was to extend the existing Lambda (option 1), but option 2 is acceptable.
    </requirement>
    <requirement id="8">
      LAMBDA SOURCE MAP:
      Add entry to infra/aws/lambda/ci/lambda-source-map.json:
        "opal-security-scanner-processor": {
          "source": "infra/aws/lambda/opal_security_scanner_processor/",
          "artifact": "security-scanner/opal-security-scanner-processor.zip",
          "pipeline": "security-scanner-pipeline"
        }
    </requirement>
    <requirement id="9">
      DEPLOYMENT PROTOCOL (non-negotiable per CLAUDE.md):
      Step 1: DS commits source (infra/aws/lambda/opal_security_scanner_processor/)
      Step 2: AE builds zip + uploads to S3 (build-and-upload.sh pattern)
      Step 3: AE commits source map update
      Step 4: terraform plan — review output
      Step 5: terraform apply
      Step 6: 0-diff plan (verify no pending changes)
      Step 7: Update pipeline_inventory.xml with new Lambda entry
      Step 8: record-terraform-deploy.sh + CHANGELOG.json entry
      Step 9: git tag -a security-scanner-v1.0.0 -m "SSCN pipeline: processor Lambda + S3 trigger + layer"
      Step 10: git push --follow-tags

      Tag format: security-scanner-v{X.Y.Z}
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">infra/aws/terraform/security-scanner-pipeline/ module created with valid backend.tf, main.tf, variables.tf, outputs.tf.</criterion>
    <criterion id="2">opal-security-scanner-processor Lambda deployed at 2048 MB / 300s with security-scanner-deps layer attached.</criterion>
    <criterion id="3">S3 ObjectCreated event notification registered (in portal-notifications module) — uploading a .xlsx to security_scanner/uploads/ triggers the Lambda.</criterion>
    <criterion id="4">IAM role grants least-privilege S3 access (get uploads, put json/security_scanner/*).</criterion>
    <criterion id="5">Presign route is live and returns a valid PUT URL for the upload key pattern.</criterion>
    <criterion id="6">lambda-source-map.json updated with opal-security-scanner-processor entry.</criterion>
    <criterion id="7">0-diff plan achieved after apply. Git tag security-scanner-v1.0.0 pushed with --follow-tags.</criterion>
    <criterion id="8">pipeline_inventory.xml updated with SSCN pipeline entry.</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Terraform is the ONLY Lambda deployment mechanism. No aws lambda update-function-code, no deploy.sh, no console.</constraint>
    <constraint>Dependencies go in the Lambda Layer (security-scanner-deps). Do not pip install -t into the source directory.</constraint>
    <constraint>opal-data-portal-v2 S3 triggers must go through portal-notifications module. Do not add S3 notifications outside of that module.</constraint>
    <constraint>Commit before apply. The sequence is code -> Terraform -> source map -> commit -> plan -> apply -> 0-diff -> tag -> push.</constraint>
    <constraint>Do not start Terraform until DS has committed the Lambda source file. An empty Lambda zip will cause a deployment that immediately fails on any invocation.</constraint>
  </constraints>

  <dependencies>
    <dependency agent="0.3.0_DS_TradingOperations" task="SSCN_PORTAL.001-002.processing-lambda.md" status="pending">
      AE cannot build or deploy the Lambda until DS has committed
      infra/aws/lambda/opal_security_scanner_processor/lambda_function.py and requirements.txt.
    </dependency>
  </dependencies>

  <deliverables>
    <deliverable type="commit">CLOUD commit: Terraform module + source map update + CHANGELOG.json</deliverable>
    <deliverable type="commit">CLOUD commit: portal-notifications module update (S3 trigger)</deliverable>
    <deliverable type="document">pipeline_inventory.xml updated with SSCN entry</deliverable>
    <deliverable type="document">Git tag security-scanner-v1.0.0 pushed</deliverable>
    <deliverable type="log">Session log with Deployment Sequence table at org/tier2_senior/0.5.0_AE_OpalETL/logs/</deliverable>
  </deliverables>
</task_order>
```
