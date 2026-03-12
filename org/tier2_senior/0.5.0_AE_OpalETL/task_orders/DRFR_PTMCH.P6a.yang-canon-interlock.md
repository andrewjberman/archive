<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-03-12-drfr-ptmch-p6a-yang-canon-interlock</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.5.0_AE_OpalETL</issued_to>
    <date>2026-03-12</date>
    <status>complete</status>
    <project>DRFR_PTMCH</project>
  </metadata>

  <objective>
    Build the Canon Interlock system for Yang data_pkl (Phase 6a). This adds a passive
    observation layer to the Yang pipeline that compares each new PKL upload against
    established canonical values, flags any changes in the overlap region, and maintains
    an incremental historical record. The system never blocks or gates any pipeline step.

    This is the first phase of the canon interlock. It proves the pattern on the
    highest-value source (Yang data_pkl). Subsequent phases extend to model_pkl,
    Excel sources, and SmartX.
  </objective>

  <references>
    <ref type="prd">docs/architecture/DRFR_PTMCH_CANON_INTERLOCK_PRD.md</ref>
  </references>

  <scope>
    <files>
      <file action="create">infra/aws/lambda/v2_portal/yang_pipeline/canon/yang-canon-interlock/lambda_function.py</file>
      <file action="modify">infra/aws/terraform/yang-pipeline/lambdas.tf</file>
      <file action="modify">infra/aws/terraform/yang-pipeline/yang-pipeline-definition.json</file>
      <file action="modify">infra/aws/lambda/ci/lambda-source-map.json</file>
      <file action="create">tools/canon/backfill_interlock.py</file>
      <file action="create">tools/canon/canon_surgery.py</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">
      NEW LAMBDA: yang-canon-interlock

      Source: infra/aws/lambda/v2_portal/yang_pipeline/canon/yang-canon-interlock/lambda_function.py
      Memory: 1024 MB. Timeout: 120s. Runtime: python3.11. Layer: pandas-pyarrow-layer:1
      (same as generate_positioning, generate_allocation_summary, etc.)

      Input: Step Functions payload (contains $.processed with data_pkl_key, model_pkl_key,
      $.manifest with file list, $.pipeline_execution_id, $.data_as_of_date).

      Phase 6a scope: process data_pkl ONLY. Ignore model_pkl and Excel sources (those are
      Phase 6b). If data_pkl is not in this execution's manifest, return early with
      { "status": "skipped", "reason": "no data_pkl in manifest" }.

      Logic:
      1. Download data_pkl from benchmarks/ (same S3 key as $.processed.data_pkl_key).
         Deserialize with pickle.loads(). Extract dc_master['combined'] DataFrame.
      2. Check if canon exists: s3://opal-data-portal-v2/canon/data_pkl/values/
         If no canon parquet exists → this is the FIRST interlock run (or post-backfill).
         Create initial canon from the full DataFrame. Write year-partitioned parquets.
         Write interlock report with status "initial" (no comparison). Archive file. Done.
      3. If canon exists: load relevant year partitions that overlap with new DataFrame's
         date range. Build a combined canon DataFrame for the overlap region.
      4. Compute overlap: dates present in BOTH canon and new data.
      5. Cell-by-cell comparison for each (date, column) in the overlap:
         - Both float: round(old, 2) != round(new, 2) → flag
         - Both NaN: match (no flag)
         - One NaN, one not: flag (value appeared/disappeared)
         - String/text columns: skip
         - Integer columns: exact match
      6. Generate interlock report JSON:
         {
           "source": "data_pkl",
           "upload_file": "{filename from manifest}",
           "upload_timestamp": ISO8601,
           "overlap_range": [min_date, max_date],
           "total_cells_compared": int,
           "mismatches": int,
           "flags": [ { "date", "column", "canon_value", "new_value", "delta",
                        "delta_pct", "established_by", "overwritten_by" } ],
           "canon_frontier_before": date_str,
           "canon_frontier_after": date_str,
           "status": "clean" | "flagged" | "initial"
         }
         Write to: canon/data_pkl/interlock-reports/{YYYYMMDD}_v{N}.json
      7. Overwrite canon: update year-partitioned parquets with ALL new values
         (not just mismatches — the new data replaces canon for its full date range).
      8. Archive: copy original PKL to canon/archive/data_pkl/{original_filename}
      9. Update control plane: write/update canon/state/control-plane.json with
         data_pkl source entry (canonical_frontier, latest_upload, interlock_status,
         total_interlocks_run, total_flags_lifetime).
      10. CloudWatch: PutMetricData to Opal/CanonInterlock namespace.
          Dimensions: Source=data_pkl, Status={clean|flagged|initial|error}
          Metrics: FlagCount, CellsCompared, OverlapDays, DurationMs.
      11. Error handling: top-level try/except. On ANY exception, log error, emit
          CloudWatch metric with Status=error, return { "status": "error", "error": str }.
          NEVER raise — the Step Functions Catch block handles this, but the Lambda
          should also self-contain errors.
    </requirement>

    <requirement id="2">
      STEP FUNCTIONS: Add Branch E (RunInterlock) to ProcessFileTypes parallel state.

      Modify yang-pipeline-definition.json:
      - Find the ProcessFileTypes Parallel state (contains Branches A-D for generators)
      - Add a 5th branch:
        {
          "StartAt": "RunInterlock",
          "States": {
            "RunInterlock": {
              "Type": "Task",
              "Resource": "arn:aws:lambda:us-east-1:313476888478:function:yang-canon-interlock",
              "Parameters": {
                "manifest.$": "$.manifest",
                "processed.$": "$.processed",
                "prior.$": "$.prior",
                "pipeline_execution_id.$": "$.pipeline_execution_id",
                "data_as_of_date.$": "$.data_as_of_date"
              },
              "ResultPath": "$.interlock",
              "TimeoutSeconds": 180,
              "Catch": [{
                "ErrorEquals": ["States.ALL"],
                "ResultPath": "$.interlock_error",
                "Next": "InterlockFallback"
              }],
              "End": true
            },
            "InterlockFallback": {
              "Type": "Pass",
              "Result": { "status": "error", "reason": "interlock_lambda_failed" },
              "ResultPath": "$.interlock",
              "End": true
            }
          }
        }

      The branch runs in parallel with all existing generator branches. If it fails,
      the Catch routes to InterlockFallback (a Pass state), and the pipeline continues
      normally. Generator results are unaffected.

      NOTE: The ProcessFileTypes Parallel state merges all branch results. Ensure the
      interlock branch's ResultPath ($.interlock) does not collide with any existing
      generator branch's ResultPath.
    </requirement>

    <requirement id="3">
      TERRAFORM: Add yang-canon-interlock Lambda module to lambdas.tf.

      module "canon_interlock" {
        source        = "../modules/yang-lambda"
        function_name = "yang-canon-interlock"
        artifact_key  = "yang-pipeline/yang-canon-interlock.zip"
        role_arn      = local.lambda_role_arn
        runtime       = "python3.11"
        timeout       = 120
        memory_size   = 1024
        system_tag    = "YangPipeline"
        layers        = [local.pandas_layer]
      }

      The existing yang-pipeline-lambda-role already has S3 read/write on
      opal-data-portal-v2/* and CloudWatch PutMetricData. Verify — if not, add
      the necessary IAM statements in iam.tf.

      Update lambda-source-map.json with the new function entry.

      Deploy sequence:
        1. Write Lambda source
        2. Write Terraform (module + Step Functions definition update)
        3. Update lambda-source-map.json
        4. git commit
        5. build-and-upload.sh yang-pipeline (builds new zip)
        6. terraform plan (yang-pipeline) → terraform apply
        7. 0-diff plan
        8. record-deploy + tag + push
    </requirement>

    <requirement id="4">
      CANON S3 PREFIX: Create initial prefix structure (can be done by the Lambda on
      first run, or manually before backfill). Ensure these paths exist after first
      successful interlock run:
        canon/state/control-plane.json
        canon/data_pkl/values/
        canon/data_pkl/interlock-reports/
        canon/archive/data_pkl/

      No manual creation needed — the Lambda and backfill script create these on write.
      Just verify they exist after the first run.
    </requirement>

    <requirement id="5">
      BACKFILL SCRIPT: tools/canon/backfill_interlock.py

      Lists all PKL files in s3://opal-data-portal-v2/benchmarks/ matching
      "data_*_v*.pkl" pattern. Sorts by date extracted from filename.
      Processes sequentially:
        - First file: establish initial canon (no comparison)
        - Subsequent files: run interlock against growing canon
      Writes all artifacts to the same canon/ prefix as the live Lambda.
      Expected runtime: ~5 minutes for ~20 historical PKLs.

      Usage: python tools/canon/backfill_interlock.py [--dry-run]

      This runs locally or on EC2 (not as a Lambda). It needs boto3, pandas, pyarrow.

      The backfill MUST be run BEFORE the next live Yang upload to establish the
      initial canon baseline. Without it, the first live interlock will treat the
      entire PKL as "initial" with no comparison — which is correct but loses the
      opportunity to validate the current canon against history.
    </requirement>

    <requirement id="6">
      SURGERY SCRIPT: tools/canon/canon_surgery.py

      CLI tool per PRD section 12.5. Arguments:
        --source {data_pkl}
        --restore-from {archived filename}
        --date-range {YYYY-MM-DD:YYYY-MM-DD}
        --dry-run (show changes without writing)
        --reason {text} (required for non-dry-run)

      Logic:
        1. Download archived upload from canon/archive/{source}/{filename}
        2. Deserialize, extract DataFrame for date range
        3. Load current canon parquet for the same date range
        4. Compare (show exactly what will change)
        5. On confirmation: overwrite canon parquet for date range
        6. Write surgery report to canon/{source}/surgery-reports/{timestamp}.json
        7. Update control-plane.json

      Usage: python tools/canon/canon_surgery.py --source data_pkl \
             --restore-from "data 20260305 v1.pkl" \
             --date-range 2025-06-01:2025-12-31 \
             --reason "Yang rebased SPY index without notice"
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">
      yang-canon-interlock Lambda deployed to AWS. terraform plan shows 0-diff.
    </criterion>
    <criterion id="2">
      Step Functions definition updated with Branch E. Visible in AWS console
      under YangDataPipeline state machine definition.
    </criterion>
    <criterion id="3">
      Backfill complete: canon/data_pkl/values/ contains year-partitioned parquets.
      canon/data_pkl/interlock-reports/ contains one JSON per historical PKL.
      canon/state/control-plane.json shows data_pkl canonical_frontier.
    </criterion>
    <criterion id="4">
      Live validation: trigger a Yang pipeline execution (or wait for next scheduled
      upload). Confirm: interlock report written, canon updated, CloudWatch metric
      emitted, all generators completed normally.
    </criterion>
    <criterion id="5">
      Surgery script: dry-run mode produces valid output showing what would change.
      (Full surgery test is optional — tool availability is the acceptance criterion.)
    </criterion>
    <criterion id="6">
      Pipeline generators are completely unaffected by interlock. If interlock
      Lambda fails (simulated or real), the Catch → InterlockFallback path activates
      and generators still complete.
    </criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>ZERO FRICTION: The interlock never blocks, gates, or delays any pipeline step.
    It is a parallel observer. If it fails, the pipeline continues identically to today.</constraint>
    <constraint>NO EXISTING LAMBDA READS FROM canon/. The interlock writes to its own
    prefix. No generator, publisher, or time-machine Lambda should be modified to
    read from canon/. Canon is fully decoupled.</constraint>
    <constraint>Phase 6a is data_pkl ONLY. Do not implement model_pkl, peer_excel,
    attribution_excel, cma_excel, or SmartX interlock in this phase. The Lambda
    should have a clean extension point for future sources but only implement data_pkl.</constraint>
    <constraint>Standard deployment protocol: terraform apply only. Tag after 0-diff.
    Push with --follow-tags.</constraint>
    <constraint>build-and-upload.sh may fail on this machine (MSYS2 path issues).
    Use PowerShell workaround per memory notes if needed.</constraint>
  </constraints>

  <dependencies>
    <dependency agent="0.5.0_AE_OpalETL" task="DRFR_PTMCH.P5" status="pending"
      note="P5 modifies yang-time-machine and deploys to yang-pipeline. Complete P5
      first to avoid concurrent Terraform changes on the same pipeline. Both P5 and
      P6a modify yang-pipeline-definition.json — sequential execution required."/>
  </dependencies>

  <deliverables>
    <deliverable type="commit">yang-canon-interlock Lambda source + Terraform module</deliverable>
    <deliverable type="commit">Step Functions definition with Branch E</deliverable>
    <deliverable type="commit">lambda-source-map.json updated</deliverable>
    <deliverable type="deploy">yang-pipeline terraform apply (tag: yang-v2.3.0 or next)</deliverable>
    <deliverable type="data">Backfill: canon/data_pkl/ populated with historical interlock data</deliverable>
    <deliverable type="commit">tools/canon/backfill_interlock.py + tools/canon/canon_surgery.py</deliverable>
    <deliverable type="document">Session log with backfill results (flag profile, canon frontier)</deliverable>
  </deliverables>
</task_order>
