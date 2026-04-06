# ADVI_GLDOPS.002 — DS: Pending Marker Fix in EC2 Runner

<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-04-03-gldops-002-ds</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-04-03</date>
    <status>complete</status>
    <priority>P0</priority>
    <project_code>ADVI_GLDOPS</project_code>
  </metadata>

  <objective>
    Re-enable the pending marker check in the EC2 runner and update the watchdog
    to be pending-marker-aware. This ensures daily gold incrementals run even when
    a full rebuild recently completed or is in progress.
  </objective>

  <references>
    <ref type="prd">docs/architecture/ADVI_GLDOPS_PRD.md</ref>
  </references>

  <context>
    Two runner scripts handle pending markers:

    1. **EC2 runner** (`infra/aws/ec2/bd-gold-layer-runner/run-gold-layer.sh`)
       Lines 88-115: pending marker check is COMMENTED OUT. Note says "Disabled:
       causes unwanted double-runs during QA gold rebuilds." This runs AFTER the
       gold scripts runner exits. It is a safety net for cases where the inner
       runner's check didn't fire (e.g., error exit).

    2. **Gold scripts runner** (`data/black_diamond/scripts/gold/run_gold_layer.sh`)
       Lines 256-274: ACTIVE pending marker check. After all gold scripts complete,
       it checks S3 for `gold/trigger-pending.json`. If found, clears marker and
       `exec $0 incremental`. This works correctly but only fires at end of run.

    3. **Watchdog** (`infra/aws/ec2/bd-gold-layer-runner/watchdog-shutdown.sh`)
       Does NOT check for pending markers. If gold processes exit between the
       rebuild completing and the pending incremental starting, watchdog could
       shut down the instance, losing the pending run.

    The bd-gold-trigger Lambda writes `gold/trigger-pending.json` to S3 when the
    instance is already running (conflict path).
  </context>

  <deliverables>
    **File 1: `infra/aws/ec2/bd-gold-layer-runner/run-gold-layer.sh`**

    Uncomment the pending marker check block (lines 94-114). Add a QA rebuild
    guard: if `/tmp/GOLD_QA_REBUILD` marker file exists on the EC2, skip the
    pending check (preserves the safety valve for manual QA rebuilds).

    The re-enabled block should:
    ```
    if [ -f "/tmp/GOLD_QA_REBUILD" ]; then
        log "QA rebuild marker found -- skipping pending check"
    elif aws s3 cp "s3://${S3_BUCKET}/${PENDING_KEY}" "$PENDING_TMP" 2>/dev/null; then
        log "Pending trigger marker found: $(cat $PENDING_TMP)"
        aws s3 rm "s3://${S3_BUCKET}/${PENDING_KEY}"
        log "=== RUNNING PENDING INCREMENTAL RUN ==="
        cd "$SCRIPTS_DIR"
        ./run_gold_layer.sh incremental 2>&1 | tee -a "$LOG_FILE"
        PENDING_EXIT=$?
        log "=== PENDING RUN COMPLETE (exit code: $PENDING_EXIT) ==="
        # Upload pending run log
        TIMESTAMP2=$(date +%Y%m%d_%H%M%S)
        LOG_KEY2="logs/gold-layer/gold_incremental_pending_${RUN_DATE}_${TIMESTAMP2}.log"
        aws s3 cp "$LOG_FILE" "s3://${S3_BUCKET}/${LOG_KEY2}"
    else
        log "No pending trigger marker."
    fi
    ```

    Remove the "Pending marker check disabled" log line at line 115.

    **File 2: `infra/aws/ec2/bd-gold-layer-runner/watchdog-shutdown.sh`**

    Before the "All checks passed: shut down" section (line 55), add a pending
    marker check:

    ```
    # --- Check 4: pending trigger marker ---
    if aws s3 cp "s3://opal-data-bd/gold/trigger-pending.json" /dev/null 2>/dev/null; then
        log "SKIP: pending trigger marker exists -- incremental run expected"
        exit 0
    fi
    ```

    This prevents the watchdog from killing the instance while a pending
    incremental is queued.

    **Verification**: After coding, confirm the gold scripts runner's own pending
    check (lines 256-274) is still correct and doesn't conflict with the EC2
    runner's re-enabled check. Both checks clear the marker before re-running,
    so at most one will fire. The inner runner checks first (during its own
    shutdown sequence), the outer runner is a safety net.

    **Do NOT deploy yet.** Commit locally. AE will push + upload to S3 after
    .001 diagnosis confirms rebuild status.
  </deliverables>

  <dependencies>
    <dependency agent="0.6.0_AE_PartnerETL"
                task="ADVI_GLDOPS.001"
                status="in_progress"
                note="Code the fix now in parallel. Deploy depends on .001 findings." />
  </dependencies>
</task_order>
