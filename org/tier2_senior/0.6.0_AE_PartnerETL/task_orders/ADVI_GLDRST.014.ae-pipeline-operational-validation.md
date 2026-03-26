# Task Order: ADVI_GLDRST.014 — Pipeline Operational Validation

```xml
<task_order>
  <metadata>
    <id>1.0.0_SA_CTO-2026-03-26-gldrst-014</id>
    <issued_by>1.0.0_SA_CTO</issued_by>
    <issued_to>0.6.0_AE_PartnerETL</issued_to>
    <date>2026-03-26</date>
    <status>staged</status>
    <project_code>ADVI_GLDRST</project_code>
  </metadata>

  <objective>
    Validate that the BD gold layer pipeline operates correctly on the new
    S3 key layout — from gold script execution through publisher invocation
    through manifest capture through time-machine restore capability. This
    is a READ-ONLY validation task. Do NOT run gold layer scripts, modify
    S3 keys, or deploy code. Produce a structured pass/fail report.
  </objective>

  <context>
    After .009 (migration gold rerun), the pipeline has completed one full
    run on the new S3 layout. This task validates the operational health of
    the entire pipeline chain, including components that will be needed for
    ongoing daily/monthly runs and for rollback if issues emerge later.

    Rollback scripts are at: data/black_diamond/scripts/gold/gldrst/
    Preflight snapshot: s3://opal-data-bd/gldrst/preflight/20260326-171617.json
  </context>

  <depends_on>.009 (migration gold rerun must complete successfully)</depends_on>

  <scope>
    Run the following operational validation checks.

    ## Check 1: Gold Run Log Verification

    Download the .009 gold run log from s3://opal-data-bd/logs/gold-layer/.
    Find the most recent gold_{mode}_{date}.log file.
    Verify:
    - Mode was "full" (not incremental)
    - All 16 scripts completed (look for "Running:" and "COMPLETE" markers)
    - No Python tracebacks or errors in the log
    - Final status line shows "COMPLETE -- FULL"
    - Runtime was reasonable (compare to previous full runs if log history exists)

    ## Check 2: Pipeline Sentinel

    Read gold/pipeline-complete.json (at old path) AND gold/meta/pipeline-complete.json
    (at new path, if .006 was deployed).
    Verify:
    - status: "success"
    - mode: "full"
    - timestamp is from the .009 run (within expected window)
    - run_date matches expected date

    ## Check 3: Pipeline Manifest (if .006 deployed)

    Read gold/meta/pipeline-manifest.json.
    Verify:
    - Contains entries for all scripts that ran
    - Each entry has: script_name, status ("success"), row_count, duration_seconds
    - No entries have status "error" or "skipped" unexpectedly

    If .006 was not deployed, mark as SKIP.

    ## Check 4: bd-capture-output-versions Manifest

    List objects at s3://opal-data-bd/snapshots/manifests/.
    Find the manifest timestamped closest to the .009 run completion.
    Verify:
    - Manifest exists (bd-capture-output-versions was triggered)
    - objects_captured count is reasonable (should be >100)
    - outputs dict contains keys from the new layout (gold/dimensions/, gold/timeseries/, etc.)
    - Each entry has a non-null versionId

    If no manifest exists (bd-capture-output-versions may not have fired),
    mark as FAIL and note that time-machine fast-path restore is unavailable.

    ## Check 5: bd-time-machine Readiness

    Verify bd-time-machine can use the manifest from Check 4:
    - The manifest's rebuild_completed_at is parseable
    - The versionIds in the manifest are still valid (spot-check 3: HEAD the
      version to confirm it exists)
    - bd-time-machine Lambda is Active (aws lambda get-function)

    Do NOT actually invoke bd-time-machine. Just verify the inputs it would need
    are present and valid.

    ## Check 6: EC2 Instance State

    Verify the gold runner instance (i-01003b035d2988dfb) is stopped.
    If it's still running, this means the .009 run didn't self-stop —
    potential cost issue and indicator of a failed shutdown sequence.

    ```bash
    aws ec2 describe-instances --instance-ids i-01003b035d2988dfb \
      --query 'Reservations[0].Instances[0].State.Name' --output text
    ```

    PASS: "stopped"
    FAIL: "running" (flag for manual shutdown)

    ## Check 7: CloudFront Invalidation

    Check that a CloudFront invalidation was created for the .009 run.
    ```bash
    aws cloudfront list-invalidations --distribution-id EVTSA9VEHNZVH \
      --query 'InvalidationList.Items[0]' --output json
    ```

    Verify the most recent invalidation was created around the .009 run
    completion time and has Status "Completed".

    ## Check 8: Dual-Write Integrity (Old Keys Still Present)

    Run: python data/black_diamond/scripts/gold/gldrst/verify_migration.py gate3 --verbose

    This verifies:
    - All new keys are populated (gate3 checks)
    - Old keys are still present (dual-write intact)

    PASS: gate3 exits 0.
    FAIL: gate3 exits 1 (report which keys are missing).

    ## Check 9: Scheduling Chain

    Verify the next daily gold run will work correctly:
    - bd-gold-trigger Lambda is Active
    - EventBridge rule for nightly trigger exists and is ENABLED
    - EventBridge rule for monthly full trigger exists and is ENABLED
    - The trigger Lambda's DISTRIBUTION_ID env var is correct (EVTSA9VEHNZVH)

    ```bash
    aws events list-rules --name-prefix "bd-gold" --query 'Rules[*].{Name:Name,State:State}'
    ```

    ## Check 10: Pre-010 Readiness

    Run: python data/black_diamond/scripts/gold/gldrst/verify_migration.py pre010

    Follow the guidance it prints. The output includes manual verification
    steps for confirming zero reads to old paths. Document whether the 48-hour
    soak period has elapsed since .009 completion.
  </scope>

  <deliverable>
    A structured validation report in your session log with:
    - Each check (1-10): PASS/FAIL/SKIP with evidence
    - Summary: X/10 checks passed
    - If any FAIL: root cause analysis and which component needs attention
    - Soak period status: hours elapsed since .009 completion
    - Final verdict: CLEAR or BLOCKED (with blocking reason)

    Report to COO via send_message when complete.
  </deliverable>

  <constraints>
    - READ-ONLY. Do not run gold layer scripts. Do not start the EC2 instance.
    - Do not invoke bd-time-machine (it would actually restore data).
    - Do not invoke bd-gold-trigger (it would start the EC2 instance).
    - Do not modify any S3 keys, Lambda code, or Terraform state.
    - Use the gldrst/ verification scripts where applicable.
  </constraints>
</task_order>
```
