```xml
<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-03-10-drfr-ptmch-opaletl-p2</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.5.0_AE_OpalETL</issued_to>
    <date>2026-03-10</date>
    <status>complete</status>
    <status_note>ALL REQUIREMENTS DEPLOYED. Req 5: news-v2.7.0 (2026-03-10). Req 2/3/6 + Req 8 (DynamoDB):
    yang-time-machine Lambda deployed at yang-v2.2.0 (2026-03-10, commit 71ef5481).
    DataRefresh endpoints (archive list + time-machine invoke) deployed at data-refresh-v2.1.0 (2026-03-10).
    IAM: S3VersionedRestore on yang-pipeline-lambda-role; InvokeTimeMachine on opal-data-refresh-lambda-role.
    CF paths: /api/general/* + /api/general/json-tiered/* per CloudOps P1 findings.
    Req 4 (FRED cache exception): documented in findings doc. Req 7: findings doc complete.</status_note>
    <thread_serial>DRFR_PTMCH-001</thread_serial>
    <thread_ref>org/threads/DRFR_PTMCH-001-portal-time-machine-ae-infrastructure-di/</thread_ref>
    <revised>2026-03-10 -- REVISED post agent review. Corrections: news publisher path fixed;
    LATEST.json rebuild reads manifest.json not metadata.json; yang-pipeline-lambda-role confirmed
    as IAM target (OpalETL owns this in yang-pipeline/iam.tf, not CloudOps); API Gateway requires
    no TF changes (catch-all proxy already routes all /data-refresh/*). Go-ahead: start now.
    News publisher (req 5) is fully unblocked. Yang-time-machine code (req 2) can be written now
    and deployed after CloudFront paths confirmed by CloudOps P1.</revised>
  </metadata>

  <objective>
    Build the yang-time-machine Lambda and DataRefresh API endpoints (Layer 1 of Portal Time
    Machine). Also parameterize the news trending publisher for Layer 3. Archive manifests are
    confirmed healthy (83 files, non-null versionIds). Step Functions placement confirmed:
    CaptureOutputVersions runs on every execution after GenerateManifest. Outputs-manifest schema
    confirmed: { executionId, dataAsOfDate, pipelineStartedAt, outputCount, outputs: { key: {
    versionId, size, etag, lastModified } } }. OpalETL also owns yang-pipeline IAM additions
    for yang-pipeline-lambda-role (version S3 permissions).
  </objective>

  <scope>
    <files>
      <file action="create">infra/aws/lambda/v2_portal/yang_pipeline/outputs/yang-time-machine/lambda_function.py</file>
      <file action="modify">infra/aws/lambda/data_refresh/lambda_function.py</file>
      <file action="modify">infra/aws/terraform/yang-pipeline/main.tf</file>
      <file action="modify">infra/aws/terraform/yang-pipeline/iam.tf</file>
      <file action="modify">infra/aws/terraform/data-refresh/main.tf</file>
      <file action="modify">infra/aws/lambda/ci/lambda-source-map.json</file>
      <file action="modify">infra/aws/lambda/semantic-trending-topics-portal-publisher/lambda_function.py</file>
      <file action="create">org/tier2_senior/0.5.0_AE_OpalETL/deliverables/DRFR_PTMCH.001.opal-pipeline-findings.md</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">
      CONFIRMED -- Step Functions placement verified by you before this task order arrived.
      CaptureOutputVersions runs on every execution (unconditional), positioned after GenerateManifest
      and before InvalidateCloudFront. Has a Catch block that routes to InvalidateCloudFront on
      error (pipeline does not fail if capture fails). 10-minute window is a known limitation --
      document in findings doc (req 7) but do not change the window in this phase.
      Outputs-manifest schema is confirmed as noted in revision header.
    </requirement>

    <requirement id="2">
      yang-time-machine Lambda:
      Path: infra/aws/lambda/v2_portal/yang_pipeline/outputs/yang-time-machine/lambda_function.py
      Handler: restore_to_date(event, context)
      Input: { "target_date": "YYYY-MM-DD" }
      Logic:
        1. List all objects matching data-refresh/archive/*/outputs-manifest.json (paginated).
           NOTE: execution IDs use two formats -- UUID (e.g. 7a407b33-...) and exec- prefix
           (e.g. exec-30147e4870cf). Both are valid; filter to keys ending in outputs-manifest.json.
        2. For each manifest, read dataAsOfDate and pipelineStartedAt directly from the manifest
           JSON (confirmed schema fields). Do NOT read metadata.json for these fields.
        3. Select latest execution where dataAsOfDate <= target_date AND pipelineStartedAt <=
           17:00 ET on target_date. If none found: return 404 with
           { "error": "no_restore_point", "earliest_available": <oldest dataAsOfDate found> }.
        4. For each key/versionId pair in outputs: call
           s3.copy_object(CopySource={Bucket, Key, VersionId=versionId}, Bucket=BUCKET, Key=key).
           Collect failures. Log each. Continue on failure (partial restore is better than abort).
        5. Rebuild benchmarks/LATEST.json: read
           data-refresh/archive/{executionId}/manifest.json (the original uploaded manifest,
           NOT metadata.json -- this is where PKL file paths and version strings live).
           Reconstruct LATEST.json consistent with how yang-generate-latest builds it.
        6. CloudFront invalidation: use paths confirmed by CloudOps P1 findings doc
           (deliverables/DRFR_PTMCH.001.cloudops-findings.md). Hardcode the confirmed paths.
           Do NOT deploy yang-time-machine until CloudOps P1 findings doc is available.
           Code can be written with a placeholder comment: # CF_PATHS: see CloudOps P1 findings.
        7. Return { "restored_execution": execId, "data_as_of": date,
           "files_restored": N, "files_failed": [key, ...] }.
      Env vars: BUCKET (opal-data-portal-v2), ARCHIVE_PREFIX (data-refresh/archive).
    </requirement>

    <requirement id="3">
      DataRefresh API new endpoints in infra/aws/lambda/data_refresh/lambda_function.py:

      GET /data-refresh/archive -- handle_archive_list(event):
        List data-refresh/archive/*/outputs-manifest.json, read dataAsOfDate + outputCount
        from each manifest. Return sorted newest-first:
        [{ "data_as_of": "YYYY-MM-DD", "execution_id": "...",
           "pipeline_completed_at": "...", "files_captured": N }]

      POST /data-refresh/time-machine -- handle_time_machine(event):
        Parse target_date from request body. Validate YYYY-MM-DD format.
        Invoke yang-time-machine async:
          lambda_client.invoke(FunctionName=TIME_MACHINE_FUNCTION_NAME,
                               InvocationType='Event',
                               Payload=json.dumps({"target_date": target_date}))
        Return { "status": "initiated", "target_date": target_date }.

      API Gateway note (confirmed by you): no Terraform changes needed. The /data-refresh/*
      catch-all proxy already routes to the data-refresh Lambda. New routes work via Lambda
      path inspection only.

      Add to data-refresh/main.tf: TIME_MACHINE_FUNCTION_NAME env var pointing to the
      yang-time-machine Lambda name. Also add lambda:InvokeFunction permission on
      yang-time-machine ARN to opal-data-refresh-lambda-role in data-refresh/main.tf
      (this is the only IAM change in data-refresh -- invoke permission only, not S3).
    </requirement>

    <requirement id="4">
      FRED cache -- document as explicit accepted exception in findings doc:
      "FRED cache (cache/fred/BAMLC0A0CM.csv, cache/fred/BAMLH0A0HYM2.csv) is NOT captured
      by yang-capture-output-versions (scans json/ only). FRED updates weekly. Accepted
      exception for Time Machine Phase 1: FRED cache always reflects current data during
      time-travel. Extending capture scope to cache/ is deferred to a future phase."
      No code change.
    </requirement>

    <requirement id="5">
      NEWS publisher parameterization -- Layer 3:
      CORRECT PATH: infra/aws/lambda/semantic-trending-topics-portal-publisher/lambda_function.py
      (NOT news-pipeline/ subdirectory -- confirmed by you as the correct path).
      Change: in lambda_handler, replace get_latest_trending_date() with:
        target_date = event.get('target_date') if isinstance(event, dict) else None
        if target_date:
            latest_date = target_date
        else:
            latest_date = get_latest_trending_date()
      Backward compatible. Existing callers (EventBridge schedule, S3 trigger) pass no event
      or a non-dict event -- existing behavior unchanged.
      THIS REQ IS FULLY UNBLOCKED. Deploy immediately as news-v2.7.0. No IAM dependency.
      Follow standard news-pipeline deploy sequence.
    </requirement>

    <requirement id="6">
      Terraform + IAM + source map:

      yang-pipeline/main.tf: add yang-time-machine Lambda using yang-lambda module.
        memory_size = 512, timeout = 300 (restore is S3 I/O heavy).
        role = yang-pipeline-lambda-role (existing pipeline role -- confirmed by you as FLAG 4 resolution).

      yang-pipeline/iam.tf: add inline policy TimeMachineRestorePermissions to
      yang-pipeline-lambda-role. Permissions required:
        - s3:GetObjectVersion on arn:aws:s3:::opal-data-portal-v2/*
        - s3:CopyObject on arn:aws:s3:::opal-data-portal-v2/*
        - s3:PutObject on arn:aws:s3:::opal-data-portal-v2/json/*
        - s3:ListBucket on arn:aws:s3:::opal-data-portal-v2 (for manifest listing)
        - cloudfront:CreateInvalidation on the portal CloudFront distribution ARN
          (arn:aws:cloudfront::313476888478:distribution/EVTSA9VEHNZVH)
      OpalETL owns yang-pipeline/iam.tf -- add this directly. No CloudOps involvement needed.

      data-refresh/main.tf: add TIME_MACHINE_FUNCTION_NAME env var to data-refresh Lambda.
      Add lambda:InvokeFunction permission on yang-time-machine to opal-data-refresh-lambda-role.
      This is the only change to data-refresh IAM.

      lambda-source-map.json: add yang-time-machine entry.

      Deploy sequence (two applies, one gate):
        UNBLOCKED NOW:
          1. news-pipeline apply (req 5) → news-v2.7.0
        GATED ON CloudOps P1 findings doc (CF paths):
          2. yang-pipeline apply (yang-time-machine Lambda + IAM) → yang-v2.2.0
          3. data-refresh apply (new endpoints + invoke permission) → data-refresh-v2.1.0
    </requirement>

    <requirement id="8">
      MARKET OVERVIEW DYNAMODB RESTORE -- added by COO 2026-03-10 (full rollback scope):
      Yang-time-machine Lambda already patched by COO with restore_market_data_dynamo().
      The function scans opal-portal-market-data for DAILY#target_date items (the historical
      per-date rows yang-ingest-dynamodb writes on every pipeline run) and writes each back
      as the corresponding LATEST item (the fast-load row the portal reads at request time).
      This gives Market Overview true time travel without PITR restore.

      No IAM change needed -- yang-pipeline-lambda-role already has dynamodb:Scan,
      dynamodb:PutItem, dynamodb:Query on opal-portal-market-data (confirmed from iam.tf).

      MARKET_DATA_TABLE env var already added to module "time_machine" in lambdas.tf by COO.

      Your action for Phase B: build and deploy yang-time-machine as normal. The DynamoDB
      step is already in the Lambda code at commit (COO-authored). Verify in acceptance
      testing: invoke time machine with a historical date, confirm opal-portal-market-data
      LATEST items update to reflect that date's data.

      Coverage limitation: DAILY#target_date items exist only as far back as the yang pipeline
      has been running and writing DAILY items. For dates with no DAILY# row (pre-pipeline or
      gaps), the function logs a warning and skips DynamoDB restore (S3 files still restored).
      Document the earliest restorable Market Overview date in the findings doc.
    </requirement>

    <requirement id="7">
      FINDINGS DOCUMENT:
      Write org/tier2_senior/0.5.0_AE_OpalETL/deliverables/DRFR_PTMCH.001.opal-pipeline-findings.md
      covering:
        - Step Functions placement: CONFIRMED, every run, after GenerateManifest
        - Outputs-manifest schema (as confirmed by you)
        - Archive health: 83-file manifests, non-null versionIds, healthy
        - 10-minute capture window: known limitation, documented, not a blocker
        - DynamoDB opal-portal-market-data: portal reads at runtime (Market Overview), PITR enabled
        - FRED cache: explicit accepted exception (cache/fred/ out of scope)
        - Market-overview Lambda output prefixes (enumerate from lambda-source-map.json source reads)
        - FLAG 3 resolution: pkl_version comes from manifest.json not metadata.json
        - FLAG 6: no API Gateway TF changes needed
        - Deployment tags after apply
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">
      news-v2.7.0 deployed. semantic-trending-topics-portal-publisher invoked with
      { "target_date": "2026-03-05" } returns news data for that date. Without target_date:
      existing behavior unchanged.
    </criterion>
    <criterion id="2">
      yang-time-machine + data-refresh API deployed (after CloudOps P1 CF paths confirmed).
      GET /data-refresh/archive returns non-empty list of restore points.
      POST /data-refresh/time-machine with valid target_date returns { "status": "initiated" }.
      Invoking yang-time-machine directly with a historical date restores json/ files and
      invalidates CloudFront.
    </criterion>
    <criterion id="3">
      Terraform 0-diff on both yang-pipeline and data-refresh after apply.
      Tags pushed: yang-v2.2.0, data-refresh-v2.1.0.
    </criterion>
    <criterion id="4">Findings doc complete.</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>yang-time-machine is a NEW Lambda -- do NOT modify handle_rollback in
    data_refresh/lambda_function.py. Two separate code paths.</constraint>
    <constraint>FRED cache (cache/fred/) is explicitly out of scope. No changes to
    yang-capture-output-versions in this phase.</constraint>
    <constraint>Do NOT deploy yang-pipeline or data-refresh Terraform until CloudOps P1
    findings doc is available (need confirmed CF invalidation paths for yang-time-machine).</constraint>
    <constraint>News publisher change is backward compatible -- existing invocation patterns
    must continue to work unchanged.</constraint>
    <constraint>Standard deployment protocol throughout. No aws lambda update-function-code.</constraint>
  </constraints>

  <go_ahead>
    PROCEED IMMEDIATELY on:
      - Req 5 (news publisher) -- fully unblocked, deploy now as news-v2.7.0
      - Req 2 (yang-time-machine code) -- write now, use CF_PATHS placeholder
      - Req 3 (DataRefresh API code) -- write now
      - Req 6 IAM additions (yang-pipeline/iam.tf, data-refresh/main.tf TF blocks) -- write now
      - Req 7 (findings doc) -- write now (partial; add CF paths section when CloudOps P1 lands)
    HOLD deploy of yang-pipeline + data-refresh until CloudOps P1 findings doc delivers CF paths.
  </go_ahead>

  <dependencies>
    <dependency agent="0.7.0_AE_CloudOps" task="DRFR_PTMCH.P1.lifecycle-iam-cloudfront.md"
      status="pending" scope="CloudFront invalidation paths only"
      note="OpalETL needs the CF path table from CloudOps P1 req 3 to finalize
      yang-time-machine CloudFront invalidation call. IAM is NOT a dependency --
      OpalETL adds their own IAM to yang-pipeline/iam.tf independently."/>
  </dependencies>

  <deliverables>
    <deliverable type="commit">news-v2.7.0: semantic-trending-topics-portal-publisher target_date parameterization</deliverable>
    <deliverable type="commit">yang-time-machine Lambda source + yang-pipeline Terraform + yang-pipeline IAM additions</deliverable>
    <deliverable type="commit">DataRefresh API new endpoints + data-refresh/main.tf env var + invoke permission</deliverable>
    <deliverable type="commit">lambda-source-map.json updated</deliverable>
    <deliverable type="document">org/tier2_senior/0.5.0_AE_OpalETL/deliverables/DRFR_PTMCH.001.opal-pipeline-findings.md</deliverable>
  </deliverables>
</task_order>
```
