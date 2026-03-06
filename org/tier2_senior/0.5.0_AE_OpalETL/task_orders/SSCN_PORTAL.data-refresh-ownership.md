# Task Order: SSCN — Data Refresh Backend Ownership + End-to-End Validation

```xml
<task_order>
  <metadata>
    <id>1.0.0_SA_CTO-2026-03-06-sscn-data-refresh-ownership</id>
    <issued_by>1.0.0_SA_CTO</issued_by>
    <issued_to>0.5.0_AE_OpalETL</issued_to>
    <date>2026-03-06</date>
    <project>SSCN_PORTAL</project>
    <status>complete</status>
  </metadata>

  <objective>
    Establish AE ownership over the opal-data-refresh-api Lambda and all backend
    functionality it serves — DataRefresh (Yang pipeline) and Security Scanner (SSCN)
    alike. This Lambda is currently in the "other" Terraform pipeline, which is a
    catch-all with no first-class documentation. AE must:

    1. Assert domain ownership in AE's README, pipeline_inventory.xml, and the
       "other" Terraform module itself.
    2. Verify IAM on the data-refresh Lambda role for SSCN S3 operations.
    3. Run the first end-to-end upload test with a real FactSet Excel file.

    The data-refresh Lambda is the backend for both the DataRefresh portal page AND
    the Security Scanner portal page. All backend route handlers, presign logic, S3
    proxy reads, IAM, and Terraform for this Lambda are AE's domain. Frontend portal
    pages that consume these routes are DE/RD scope — but the Lambda itself is AE's.
  </objective>

  <scope>
    <files>
      <file action="modify">org/tier2_senior/0.5.0_AE_OpalETL/README.md</file>
      <file action="modify">org/tier2_senior/0.5.0_AE_OpalETL/deliverables/pipeline_inventory.xml</file>
      <file action="modify">infra/aws/terraform/other/main.tf</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">
      README OWNERSHIP DECLARATION:
      Update org/tier2_senior/0.5.0_AE_OpalETL/README.md:

      1. Add the "other" pipeline to the Pipelines Owned table:

         | Other (Data Refresh) | `infra/aws/terraform/other/` | other-v1.1.0 | Yes |

      2. Add a new section "## Data Refresh Backend (opal-data-refresh-api)" after the
         Pipelines Owned table, with content establishing:

         - opal-data-refresh-api Lambda is AE's domain. All backend routes, IAM,
           Terraform, and Lambda source are AE-owned.
         - Route families served: DataRefresh (/data-refresh/*) and Security Scanner
           (/security-scanner/*).
         - Frontend pages that consume these routes (DataRefresh page, SecurityScanner
           page) are DE/RD scope. AE owns the Lambda; DE/RD own the portal pages.
         - Source path: infra/aws/lambda/data_refresh/lambda_function.py
         - Terraform module: infra/aws/terraform/other/
         - IAM role: opal-data-refresh-lambda-role
         - Any route additions or modifications to opal-data-refresh-api require AE
           involvement. DE/DS may propose route handlers (as with SSCN_PORTAL-001) but
           AE reviews, deploys, and owns the runtime behavior.

      This is a declaration of existing fact, not a new responsibility. AE already
      deployed the SSCN presign route (security-scanner-v1.0.0) and DE already added
      GET proxy handlers (18fd997b). The README formalizes what is already true.
    </requirement>

    <requirement id="2">
      PIPELINE_INVENTORY.XML UPDATE:
      The "other" pipeline is not currently documented as a top-level pipeline section
      in pipeline_inventory.xml. Add a section:

        <pipeline name="other"
                  terraform_module="infra/aws/terraform/other/"
                  current_tag="other-v1.1.0"
                  s3_backend_key="other/tfstate"
                  trigger_model="API Gateway HTTP API → opal-data-refresh-api Lambda">

      With a single lambda entry for opal-data-refresh-api listing:
        - All route families: DataRefresh (5 routes), Security Scanner (4 routes)
        - IAM role: opal-data-refresh-lambda-role
        - Runtime, memory, timeout from main.tf
        - S3 artifact key: other/opal-data-refresh-api.zip
        - Related resources: DynamoDB table opal-data-refresh-executions,
          Step Functions YangDataPipeline (DataRefresh), CloudFront distribution
          (DataRefresh invalidation)

      The point: anyone reading pipeline_inventory.xml should find opal-data-refresh-api
      without having to know it lives in the "other" module.
    </requirement>

    <requirement id="3">
      TERRAFORM MODULE COMMENT:
      Update infra/aws/terraform/other/main.tf top comment to replace the generic
      "Other Portal Lambdas" header with a clear ownership statement:

        # Data Refresh API — Terraform Configuration
        # Owner: 0.5.0_AE_OpalETL
        # Lambda: opal-data-refresh-api
        # Routes: DataRefresh (/data-refresh/*) + Security Scanner (/security-scanner/*)
        # Source: infra/aws/lambda/data_refresh/lambda_function.py

      This replaces the existing "Other Portal Lambdas" header. The module may host
      additional Lambdas in the future, but the primary resource is opal-data-refresh-api
      and the comment should reflect that.
    </requirement>

    <requirement id="4">
      IAM VERIFICATION:
      Verify that opal-data-refresh-lambda-role has the necessary S3 permissions for
      SSCN operations:

      Required for presign route (PUT):
        s3:PutObject on arn:aws:s3:::opal-data-portal-v2/security_scanner/*

      Required for GET proxy routes:
        s3:GetObject on arn:aws:s3:::opal-data-portal-v2/json/security_scanner/*

      Both AE (sscn_pipeline_deploy.md) and DE (sscn_proxy_routes.md) flagged this as
      "likely covered" but unverified. Check the actual IAM policy attached to
      opal-data-refresh-lambda-role:

        aws iam list-attached-role-policies --role-name opal-data-refresh-lambda-role
        aws iam get-role-policy --role-name opal-data-refresh-lambda-role --policy-name {name}

      Or check the Terraform state/config for the role policy.

      If the role does NOT have these permissions:
        - Add the necessary policy statements to infra/aws/terraform/other/main.tf
          (or the module that defines the role)
        - terraform plan + apply + 0-diff
        - Tag: other-v1.2.0

      If the role DOES have the permissions (e.g., via a broad opal-data-portal-v2/*
      policy), document the finding in your session log and move on.
    </requirement>

    <requirement id="5">
      END-TO-END UPLOAD TEST:
      Upload the actual FactSet Excel file to validate the full pipeline:

      File: C:\Users\AndrewBerman\Downloads\Screening_DIVZ_IDVZ_20260226.xlsx
      asOf: 20260226

      Option A — direct S3 upload (simplest for first test):
        aws s3 cp "C:/Users/AndrewBerman/Downloads/Screening_DIVZ_IDVZ_20260226.xlsx" \
          "s3://opal-data-portal-v2/security_scanner/uploads/2026-02-26/Screening_DIVZ_IDVZ_20260226.xlsx"

      Option B — presign route (tests the full API path):
        POST /api/scoped/security-scanner/upload-url with body {"asOf":"20260226"}
        PUT the file to the returned presigned URL

      After upload, verify:
        1. CloudWatch logs for /aws/lambda/opal-security-scanner-processor:
           - Lambda triggered
           - 6 universes processed (sp500: ~502, r1000: ~1006, r1000v: ~866,
             acwx: ~1704, eafe: ~684, eafev: ~408 securities)
           - No errors
        2. S3 output artifacts exist:
           - aws s3 ls s3://opal-data-portal-v2/json/security_scanner/latest/
           - aws s3 ls s3://opal-data-portal-v2/json/security_scanner/2026-02-26/
           - Expect: factor_metadata.json + 6x universe_data.json + 6x scanner_data.json
        3. GET proxy routes respond:
           - GET /api/scoped/security-scanner/factors returns 200
           - GET /api/scoped/security-scanner/universe/sp500/scanner returns 200
           - Spot-check: response contains rows with pctls values (not all null)

      If the Lambda fails, check CloudWatch for the error. Common issues:
        - IAM: 403 on S3 PutObject (processor role missing json/security_scanner/* write)
        - Memory: OOM on large universes (Lambda is at 2048 MB, should be sufficient)
        - Timeout: 300s should be sufficient for 2,727 rows x 284 factors x 6 universes

      If GET routes return 403:
        - IAM on opal-data-refresh-lambda-role (requirement 4 — verify GetObject)

      Document all results (pass or fail) in your session log with actual output.
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">AE README contains "other" pipeline in Pipelines Owned table and a Data Refresh Backend ownership section.</criterion>
    <criterion id="2">pipeline_inventory.xml contains a top-level pipeline section for "other" with opal-data-refresh-api Lambda, all 9 routes listed, and related resources.</criterion>
    <criterion id="3">infra/aws/terraform/other/main.tf top comment identifies owner, Lambda, and route families.</criterion>
    <criterion id="4">IAM on opal-data-refresh-lambda-role is verified (session log documents the finding — either "already covered" or "policy added").</criterion>
    <criterion id="5">End-to-end upload test completed. Session log contains: CloudWatch confirmation, S3 artifact listing, GET route response verification. Pass or fail with evidence.</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Do not rename the "other" Terraform module directory. Renaming would change the S3 state key and require a state migration. The ownership assertion is in documentation and comments, not directory structure.</constraint>
    <constraint>Do not modify opal-data-refresh-api Lambda source code. The source is already complete (DE commit 18fd997b). This task order is about ownership documentation, IAM verification, and testing.</constraint>
    <constraint>If IAM changes are needed, follow the standard deploy sequence: commit -> plan -> apply -> 0-diff -> tag (other-v1.2.0) -> push --follow-tags.</constraint>
    <constraint>The upload test uses a real FactSet file. Do not create synthetic test data. The file has been validated for structural compatibility (CTO analysis 2026-03-06).</constraint>
  </constraints>

  <dependencies>
    <dependency agent="none" task="none" status="n/a">
      No blocking dependencies. All infrastructure is deployed (security-scanner-v1.0.0).
      All Lambda source is committed (DS 3879941c, DE 18fd997b, AE 7d0581b2).
      This task order is unblocked and can execute immediately.
    </dependency>
  </dependencies>

  <deliverables>
    <deliverable type="commit">AE README updated with Data Refresh Backend ownership section</deliverable>
    <deliverable type="commit">pipeline_inventory.xml updated with "other" pipeline section</deliverable>
    <deliverable type="commit">infra/aws/terraform/other/main.tf comment updated</deliverable>
    <deliverable type="commit">IAM policy update if needed (other-v1.2.0 tag)</deliverable>
    <deliverable type="log">Session log with end-to-end test results at org/tier2_senior/0.5.0_AE_OpalETL/logs/2026-03-06/</deliverable>
  </deliverables>
</task_order>
```
