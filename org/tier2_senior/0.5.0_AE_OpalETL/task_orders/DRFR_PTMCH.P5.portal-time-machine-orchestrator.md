```xml
<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-03-10-drfr-ptmch-p5-opaletl</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.5.0_AE_OpalETL</issued_to>
    <date>2026-03-10</date>
    <status>pending</status>
    <thread_serial>DRFR_PTMCH-001</thread_serial>
    <thread_ref>org/threads/DRFR_PTMCH-001-portal-time-machine-ae-infrastructure-di/</thread_ref>
  </metadata>

  <objective>
    Two changes for Phase 5. (1) Patch yang-time-machine to exclude append-only JSON paths
    from S3 version restore -- these paths contain time series data that is filtered at
    render time by the frontend, not rolled back at the file level. Restoring an old version
    of an append-only file would truncate its history permanently. (2) Build the
    portal-time-machine Lambda: a single orchestrator that accepts target_date and fans out
    to all three restore layers (yang, BD, news) in parallel. Update the existing
    POST /data-refresh/time-machine endpoint to invoke this orchestrator instead of
    yang-time-machine directly.
  </objective>

  <scope>
    <files>
      <file action="modify">infra/aws/lambda/v2_portal/yang_pipeline/outputs/yang-time-machine/lambda_function.py</file>
      <file action="create">infra/aws/lambda/data_refresh/portal_time_machine/lambda_function.py</file>
      <file action="modify">infra/aws/lambda/data_refresh/lambda_function.py</file>
      <file action="modify">infra/aws/terraform/yang-pipeline/main.tf</file>
      <file action="modify">infra/aws/terraform/data-refresh/main.tf</file>
      <file action="modify">infra/aws/lambda/ci/lambda-source-map.json</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">
      YANG-TIME-MACHINE: exclude append-only paths from S3 version restore.
      The following paths contain append-only time series data. Restoring an old S3 version
      of these files truncates their history -- wrong behavior. These are filtered at render
      time by the frontend (view_as_of date filter), not by file restore.

      Append-only paths to SKIP during restore_outputs():
        - Any key starting with "json/portfolios/" EXCEPT:
            json/portfolios/aum-metrics.json       (snapshot -- DO restore)
            json/portfolios/account-distribution.json  (snapshot -- DO restore)
        - Any key starting with "json/model_portfolios/views/" -- CONFIRM whether
          these are appended or snapshot by reading the smartx_ingestion_pipeline source.
          If appended: skip. If snapshot: restore.

      Implementation: in restore_outputs(), add a check before copy_object:
        if _is_append_only(key): skip with log "SKIP (append-only, frontend filters by date)"
      Add _is_append_only(key) function with the exclusion list above.

      Return the skipped keys in the response as "files_skipped_append_only": [...].
    </requirement>

    <requirement id="2">
      NEW LAMBDA: portal-time-machine orchestrator.
      Path: infra/aws/lambda/data_refresh/portal_time_machine/lambda_function.py
      Input: { "target_date": "YYYY-MM-DD" }

      Fans out to all three restore layers in parallel (async invokes):
        1. yang-time-machine: { "target_date": target_date }
        2. bd-time-machine:   { "target_date": target_date }
        3. semantic-trending-topics-portal-publisher: { "target_date": target_date }

      All three use InvocationType='Event' (async, fire-and-forget).
      Returns immediately with:
        {
          "status": "initiated",
          "target_date": target_date,
          "layers_invoked": ["yang", "bd", "news"],
          "initiated_at": ISO8601
        }

      Env vars: YANG_TIME_MACHINE_FUNCTION, BD_TIME_MACHINE_FUNCTION,
                NEWS_PUBLISHER_FUNCTION
      All three are required. If any env var is missing, return 500.
    </requirement>

    <requirement id="3">
      UPDATE POST /data-refresh/time-machine in lambda_function.py.
      Currently invokes yang-time-machine directly. Change to invoke
      portal-time-machine instead. One line change in handle_time_machine():
        FunctionName = PORTAL_TIME_MACHINE_FUNCTION_NAME (new env var)
      Add TIME_MACHINE_FUNCTION_NAME → PORTAL_TIME_MACHINE_FUNCTION_NAME rename
      or add new env var. Keep backward compat if needed.
    </requirement>

    <requirement id="4">
      TERRAFORM:
      - Add portal-time-machine Lambda to data-refresh/main.tf with env vars pointing
        to the three downstream function names.
      - Add lambda:InvokeFunction permissions on all three downstream Lambdas to the
        portal-time-machine execution role.
      - Update data-refresh Lambda env var to point to portal-time-machine ARN.
      Deploy: build-and-upload (yang-time-machine + portal-time-machine + data-refresh-api)
      → terraform apply yang-pipeline (yang-time-machine change) → terraform apply
      data-refresh (portal-time-machine + api change) → tag both.
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">
      yang-time-machine invoked with a historical date: response includes
      "files_skipped_append_only" containing json/portfolios/ time series keys.
      Verify json/portfolios/aum-metrics.json IS restored (not skipped).
    </criterion>
    <criterion id="2">
      portal-time-machine invoked directly: all three downstream Lambdas fire
      (confirm via CloudWatch Logs for yang-time-machine, bd-time-machine,
      semantic-trending-topics-portal-publisher within 30s).
    </criterion>
    <criterion id="3">
      POST /data-refresh/time-machine calls portal-time-machine (not yang-time-machine
      directly). Confirm via CloudWatch: portal-time-machine log group shows invocation.
    </criterion>
    <criterion id="4">Terraform 0-diff. Tags pushed.</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Do NOT restore json/portfolios/ time series files -- frontend filters these.
    DO restore json/portfolios/aum-metrics.json and json/portfolios/account-distribution.json.</constraint>
    <constraint>portal-time-machine must be fire-and-forget (async). It returns immediately.
    The caller (DataRefresh frontend) polls portal state change, not a response status.</constraint>
    <constraint>Standard deployment protocol: terraform apply only.</constraint>
  </constraints>

  <dependencies>
    <dependency agent="DRFR_PTMCH-P2" task="yang-time-machine deployed" status="complete"
      note="yang-v2.2.2 deployed. yang-time-machine is live. This task patches it."/>
    <dependency agent="DRFR_PTMCH-P3" task="bd-time-machine deployed" status="complete"
      note="bd-v2.18.2 deployed. bd-time-machine is live."/>
  </dependencies>

  <deliverables>
    <deliverable type="commit">yang-time-machine: append-only exclusion list deployed (yang-v2.2.3)</deliverable>
    <deliverable type="commit">portal-time-machine Lambda deployed (data-refresh pipeline)</deliverable>
    <deliverable type="commit">POST /data-refresh/time-machine updated to use portal-time-machine</deliverable>
  </deliverables>
</task_order>
```
