```xml
<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-03-10-drfr-ptmch-opaletl-p2</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.5.0_AE_OpalETL</issued_to>
    <date>2026-03-10</date>
    <status>pending</status>
    <thread_serial>DRFR_PTMCH-001</thread_serial>
    <thread_ref>org/threads/DRFR_PTMCH-001-portal-time-machine-ae-infrastructure-di/</thread_ref>
  </metadata>

  <objective>
    Build the yang-time-machine Lambda and supporting DataRefresh API endpoint (Layer 1 of
    the Portal Time Machine). S3 versioning is confirmed enabled on opal-data-portal-v2 and
    archive manifests are confirmed healthy (83 files, non-null versionIds, exec 7a407b33
    from 2026-03-08). The mechanism: given a target_date, scan outputs-manifest.json files
    across executions, select the latest execution whose data_as_of_date <= target_date,
    restore all captured JSON files to their version at that execution via CopyObject with
    CopySourceVersionId, update benchmarks/LATEST.json, and invalidate CloudFront.
    Also parameterize semantic-trending-topics-portal-publisher for Layer 3 (news re-publish).
  </objective>

  <scope>
    <files>
      <file action="create">infra/aws/lambda/v2_portal/yang_pipeline/outputs/yang-time-machine/lambda_function.py</file>
      <file action="modify">infra/aws/lambda/data_refresh/lambda_function.py</file>
      <file action="modify">infra/aws/terraform/yang-pipeline/main.tf</file>
      <file action="modify">infra/aws/lambda/ci/lambda-source-map.json</file>
      <file action="modify">infra/aws/lambda/news-pipeline/semantic-trending-topics-portal-publisher/lambda_function.py</file>
      <file action="create">org/tier2_senior/0.5.0_AE_OpalETL/deliverables/DRFR_PTMCH.001.opal-pipeline-findings.md</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">
      PREREQUISITE -- read yang-pipeline-definition.json to confirm Step Functions placement:
      File: infra/aws/terraform/yang-pipeline/yang-pipeline-definition.json (or the path
      that stepfunctions.tf references via file()). Confirm:
        - Is yang-capture-output-versions a step in the state machine?
        - Does it run on every execution (not just full runs)?
        - Does it run AFTER all generator lambdas and AFTER yang-generate-manifest?
      If it is NOT on every run: flag to COO immediately before building the time machine.
      The time machine is only reliable if every execution has an outputs-manifest.json.
    </requirement>

    <requirement id="2">
      yang-time-machine Lambda -- core restore logic:
      New Lambda at infra/aws/lambda/v2_portal/yang_pipeline/outputs/yang-time-machine/lambda_function.py.
      Handler: restore_to_date(event, context).
      Input event: { "target_date": "YYYY-MM-DD" }
      Logic:
        1. List all objects under data-refresh/archive/ matching */outputs-manifest.json.
        2. For each manifest, read the associated metadata.json (same execution prefix)
           to get data_as_of_date and pipeline_completed_at timestamp.
        3. Select the latest execution where data_as_of_date <= target_date AND
           pipeline_completed_at is at or before 17:00 ET on target_date.
           If no such execution exists: return 404 with earliest_available_date.
        4. For each key/versionId pair in the selected manifest's outputs:
           call s3.copy_object(CopySource={Bucket, Key, VersionId=versionId},
           Bucket=BUCKET, Key=key) to restore that exact version.
        5. Update benchmarks/LATEST.json to point to the PKL version from that execution
           (get execution metadata for the pkl_version field).
        6. Invalidate CloudFront for /api/public/* AND /api/scoped/* (use invalidation
           paths confirmed by CloudOps req 4 -- coordinate before hardcoding).
        7. Return { "restored_execution": execId, "data_as_of": date, "files_restored": N }.
      Error handling: if any copy_object fails, log the key and continue (partial restore
      is better than no restore; the caller can retry). Return a summary of failed keys.
    </requirement>

    <requirement id="3">
      DataRefresh API -- new endpoint GET /data-refresh/archive:
      Add to infra/aws/lambda/data_refresh/lambda_function.py.
      Returns a list of available restore points (one per unique data_as_of_date):
        [ { "data_as_of": "YYYY-MM-DD", "execution_id": "...", "pipeline_completed_at": "...",
            "files_captured": N } ]
      Ordered newest-first. This feeds the frontend date picker showing which dates
      are available for Time Machine travel.
      Also add POST /data-refresh/time-machine endpoint that invokes yang-time-machine Lambda
      asynchronously and returns { "status": "initiated", "target_date": date }.
    </requirement>

    <requirement id="4">
      FRED cache -- document as explicit exception:
      yang-refresh-fred-cache writes to cache/fred/ which is NOT under json/ and NOT
      captured by yang-capture-output-versions. Document this gap in the findings doc as:
      "FRED cache (cache/fred/BAMLC0A0CM.csv, BAMLH0A0HYM2.csv) is NOT restored by
      Time Machine. FRED data updates weekly and represents macro market conditions.
      Accepted exception: FRED cache always reflects current data during time-travel."
      Do NOT extend yang-capture-output-versions to capture cache/ in this phase.
    </requirement>

    <requirement id="5">
      NEWS re-publish parameterization (Layer 3):
      Modify infra/aws/lambda/news-pipeline/semantic-trending-topics-portal-publisher/lambda_function.py.
      Current behavior: queries DynamoDB semantic-news-trending-daily for the latest date.
      Required: accept optional event field { "target_date": "YYYY-MM-DD" }.
      If target_date present: query DynamoDB for date = target_date instead of get_latest_trending_date().
      If target_date absent: existing behavior unchanged (backward compatible).
      The portal-time-machine orchestrator (Phase 5) will invoke this Lambda with target_date
      as part of the full time-travel sequence.
    </requirement>

    <requirement id="6">
      Terraform + source map:
      - Add yang-time-machine Lambda to infra/aws/terraform/yang-pipeline/main.tf
        (use the standard yang-lambda module, memory 512MB, timeout 300s -- restore is I/O heavy).
      - Update infra/aws/lambda/ci/lambda-source-map.json with the new Lambda.
      - Update news-pipeline source map entry if semantic-trending-topics-portal-publisher
        changed is in a different pipeline's Terraform.
      Deploy via standard protocol: build-and-upload.sh -> commit -> plan -> apply -> 0-diff -> tag.
    </requirement>

    <requirement id="7">
      FINDINGS DOCUMENT:
      Write org/tier2_senior/0.5.0_AE_OpalETL/deliverables/DRFR_PTMCH.001.opal-pipeline-findings.md
      covering:
        - Step Functions placement verdict (req 1)
        - Archive health: confirmed 83-file manifests with non-null versionIds
        - DynamoDB: opal-portal-market-data confirmed, portal reads at runtime (Market Overview)
        - FRED cache: documented as explicit exception
        - Market-overview Lambda output prefixes (from source map + Lambda source)
        - yang-time-machine implementation notes and deployment tag
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">
      yang-time-machine Lambda deployed. Invoke with a real historical target_date from
      the archive list (e.g., 2026-03-04) and confirm files are restored without errors.
      Check one restored file in S3 matches the expected execution's output.
    </criterion>
    <criterion id="2">
      GET /data-refresh/archive returns a non-empty list of available restore points
      with correct data_as_of dates and file counts.
    </criterion>
    <criterion id="3">
      POST /data-refresh/time-machine with a valid target_date returns { "status": "initiated" }.
      CloudFront invalidation fires. Portal json/ files update to the historical version.
    </criterion>
    <criterion id="4">
      semantic-trending-topics-portal-publisher with { "target_date": "2026-03-05" } returns
      news data for that date. Without target_date: existing behavior unchanged.
    </criterion>
    <criterion id="5">
      Terraform 0-diff after apply. Source map updated. Git tag pushed.
    </criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Do NOT modify the existing handle_rollback function behavior -- yang-time-machine
    is a NEW code path, not a replacement for rollback.</constraint>
    <constraint>FRED cache (cache/fred/) is explicitly out of scope. Do not extend capture
    or restore to that prefix.</constraint>
    <constraint>yang-time-machine must be idempotent: calling it twice with the same
    target_date produces the same result without errors.</constraint>
    <constraint>Coordinate with CloudOps on CloudFront invalidation paths (req 6) before
    hardcoding /api/public/* -- BD data may require /api/scoped/*.</constraint>
    <constraint>Standard deployment protocol: never use aws lambda update-function-code directly.
    All deploys via terraform apply.</constraint>
  </constraints>

  <dependencies>
    <dependency agent="0.7.0_AE_CloudOps" task="DRFR_PTMCH.P1.lifecycle-iam-cloudfront.md"
      status="pending"
      note="IAM permissions (req 3 of CloudOps task order) must be in place before
      yang-time-machine Lambda can copy objects across version IDs. CloudFront invalidation
      paths (req 4 of CloudOps) must be known before req 6 of this task order.
      CloudOps P1 is on the critical path."/>
  </dependencies>

  <deliverables>
    <deliverable type="commit">yang-time-machine Lambda source + Terraform + source map update</deliverable>
    <deliverable type="commit">DataRefresh API new endpoints (GET /data-refresh/archive, POST /data-refresh/time-machine)</deliverable>
    <deliverable type="commit">semantic-trending-topics-portal-publisher target_date parameterization</deliverable>
    <deliverable type="document">org/tier2_senior/0.5.0_AE_OpalETL/deliverables/DRFR_PTMCH.001.opal-pipeline-findings.md</deliverable>
  </deliverables>
</task_order>
```
