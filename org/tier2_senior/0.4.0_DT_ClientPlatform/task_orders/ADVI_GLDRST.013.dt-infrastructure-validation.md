# Task Order: ADVI_GLDRST.013 — Infrastructure Validation

```xml
<task_order>
  <metadata>
    <id>1.0.0_SA_CTO-2026-03-26-gldrst-013</id>
    <issued_by>1.0.0_SA_CTO</issued_by>
    <issued_to>0.4.0_DT_ClientPlatform</issued_to>
    <date>2026-03-26</date>
    <status>staged</status>
    <project_code>ADVI_GLDRST</project_code>
  </metadata>

  <objective>
    Validate that all Lambda functions, CloudFront behaviors, API Gateway
    routes, and Terraform state are correct after the GLDRST migration.
    This is a READ-ONLY validation task. Do NOT modify any infrastructure,
    deploy any code, or run terraform apply. Produce a structured pass/fail report.
  </objective>

  <context>
    After .007 (Lambda path migration) + .008 (CloudFront behavior update) +
    .009 (migration gold rerun), all infrastructure should be serving data
    from the new S3 key layout with zero errors. This task validates that
    the infrastructure layer is healthy and drift-free.
  </context>

  <depends_on>.009 (migration gold rerun must complete successfully)</depends_on>

  <scope>
    Run the following infrastructure validation checks.

    ## Check 1: bd-portal-publisher — Zero Errors

    Query CloudWatch Logs for the bd-portal-publisher Lambda.
    Time range: from .009 gold run completion to now.
    Filter: ERROR, Exception, Traceback, NoSuchKey, AccessDenied.

    PASS: zero matches.
    FAIL: any error related to S3 key resolution or data processing.

    Also verify: the Lambda produced output JSON files at the expected
    new S3 paths (gold/artifacts/, gold/snapshots/, gold/summary/, gold/filters/).

    ## Check 2: bd-portal-advisor-publisher — Zero Errors

    Query CloudWatch Logs for the bd-portal-advisor-publisher Lambda.
    Same time range and filters as Check 1.

    Also verify: per-advisor book.json files exist at gold/entities/advisors/{id}/
    (spot-check 5 advisor IDs).

    ## Check 3: opal-partners-data — Zero 5xx Errors

    Query CloudWatch Logs for the opal-partners-data Lambda.
    Time range: last 24 hours (covers portal usage since .009).
    Filter: 5xx, ERROR, NoSuchKey, AccessDenied.

    PASS: zero 5xx errors. (4xx like 404 for invalid IDs are acceptable.)
    FAIL: any 5xx error or S3 key resolution failure.

    ## Check 4: CloudFront Distribution — Correct Behaviors

    Describe the CloudFront distribution EVTSA9VEHNZVH behaviors.
    For each behavior that routes advisor-intelligence paths:
    - Record the path pattern
    - Record the origin
    - Verify the origin path points to the new S3 key layout

    Compare against the pre-migration CloudFront baseline (if captured
    in pre-flight step 4).

    ## Check 5: Terraform 0-Diff Plans

    Run terraform plan (plan only, NOT apply) for both pipelines:

    ```bash
    export MSYS_NO_PATHCONV=1
    cd infra/aws/terraform/bd-pipeline
    .tools/terraform.exe plan -detailed-exitcode -input=false
    cd infra/aws/terraform/partners-api
    .tools/terraform.exe plan -detailed-exitcode -input=false
    ```

    PASS: exit code 0 (no changes) for both.
    FAIL: exit code 2 (changes detected) — report what Terraform wants to change.

    ## Check 6: API Gateway Route Health

    For each Terraform-managed API Gateway route on opal-portal-data-proxy-api:
    - GET /api/scoped/partners/books/firm/all/composition
    - GET /api/scoped/partners/books/firm/all/mix-views
    - GET /api/scoped/partners/books/advisor/{advisorId}/timeseries
    - GET /api/scoped/partners/books/advisor/{advisorId}/mix-timeseries

    Invoke each route (via curl or aws apigateway test-invoke-method) and verify:
    - HTTP 200 response (with valid auth token)
    - Response body is non-empty JSON
    - No 502/504 Gateway errors

    If auth token is not available for direct invocation, verify the routes
    exist in API Gateway configuration and the Lambda integration is correct.

    ## Check 7: Lambda Code Version Verification

    For each of the 3 migrated Lambdas, verify:
    - Current deployed code SHA256 matches the expected post-.007 artifact
    - Runtime is python3.12
    - Memory and timeout match expected values
    - Environment variables are correct (S3_BUCKET, DISTRIBUTION_ID, etc.)

    ```bash
    aws lambda get-function --function-name bd-portal-publisher \
      --query 'Configuration.{CodeSha256:CodeSha256,Runtime:Runtime,MemorySize:MemorySize,Timeout:Timeout}'
    ```

    ## Check 8: S3 Event Notification Chain

    Verify the pipeline trigger chain is intact:
    - S3 event notification on opal-data-bd for gold/pipeline-complete.json
      still points to bd-portal-publisher Lambda
    - bd-portal-publisher still has ADVISOR_PUBLISHER_FUNCTION and
      CAPTURE_VERSIONS_FUNCTION environment variables set correctly

    This ensures the next daily gold run will trigger the full publisher chain.
  </scope>

  <deliverable>
    A structured validation report in your session log with:
    - Each check (1-8): PASS/FAIL with evidence (CloudWatch excerpts, terraform plan output, API responses)
    - Summary: X/8 checks passed
    - If any FAIL: root cause analysis and remediation recommendation
    - Final verdict: CLEAR or BLOCKED (with blocking reason)

    Report to COO via send_message when complete.
  </deliverable>

  <constraints>
    - READ-ONLY. Do not run terraform apply. Do not deploy code. Do not modify infrastructure.
    - terraform plan only — never terraform apply in this task order.
    - Do not invoke bd-gold-trigger or start the EC2 gold runner.
    - Do not modify CloudFront behaviors.
    - Use MSYS_NO_PATHCONV=1 for all Terraform commands on Windows.
  </constraints>
</task_order>
```
