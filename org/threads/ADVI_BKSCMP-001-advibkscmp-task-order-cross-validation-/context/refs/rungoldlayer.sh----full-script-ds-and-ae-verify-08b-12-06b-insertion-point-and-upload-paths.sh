#!/bin/bash
# =============================================================================
# BD Gold Layer Runner
#
# Runs on bd-gold-layer-runner (i-01003b035d2988dfb, r6i.xlarge, 32GB RAM).
# Dispatched via SSM from bd-gold-trigger Lambda.
#
# Two modes:
#
#   incremental [--start-date YYYY-MM-DD]
#     Runs: 00, 02, 05, 05c, 05d, 06b, 07, 08b, 08, 09, 10 (sequential)
#     Default start-date: 8 days ago (covers last full week + buffer)
#     Frequency: daily (Mon-Fri, ~6 PM ET after transaction pipeline)
#
#   full
#     Runs: 00, 01, 02, 04, 03, 05, 05b, 05c, 05d, 06, 06b, 07, 08b, 08, 09, 10 (sequential)
#     Frequency: monthly (1st of every month, 3 AM ET)
#
# All scripts run sequentially. No parallelism — prevents read-during-write
# race conditions on shared S3 parquet files (e.g., 07/08 reading
# client_performance.parquet while 05 is still writing it).
#
# Usage:
#   ./run_gold_layer.sh incremental
#   ./run_gold_layer.sh incremental --start-date 2026-02-16
#   ./run_gold_layer.sh full
# =============================================================================

set -e

MODE="${1:-incremental}"
START_DATE=""

# Parse optional --start-date flag
shift
while [[ $# -gt 0 ]]; do
    case "$1" in
        --start-date) START_DATE="$2"; shift 2 ;;
        *) shift ;;
    esac
done

# Default incremental start date: 8 days ago (covers last full week + weekend buffer)
if [[ "$MODE" == "incremental" && -z "$START_DATE" ]]; then
    START_DATE=$(date -d "8 days ago" +%Y-%m-%d 2>/dev/null || date -v-8d +%Y-%m-%d)
fi

S3_BUCKET="opal-data-bd"
SCRIPTS_DIR="/tmp/gold_layer_scripts"
RUN_DATE=$(date +%Y-%m-%d)
LOG_KEY="logs/gold-layer/gold_${MODE}_${RUN_DATE}.log"

mkdir -p "$SCRIPTS_DIR"

exec > >(tee /tmp/gold_runner.log) 2>&1

echo "============================================================"
echo "BD GOLD LAYER — ${MODE^^}"
echo "Started:    $(date -u '+%Y-%m-%d %H:%M:%S UTC')"
[[ "$MODE" == "incremental" ]] && echo "Start date: ${START_DATE}"
echo "============================================================"
echo ""

# Install/verify dependencies
echo "[setup] Checking Python dependencies..."
pip3 install --quiet --upgrade boto3 pandas pyarrow numpy 2>&1 | tail -3

# Download gold scripts from S3 (medallion: code/gold/)
echo ""
echo "[setup] Downloading gold layer scripts from S3..."
aws s3 sync s3://${S3_BUCKET}/code/gold/ "$SCRIPTS_DIR/" --exclude "archive/*" --quiet
echo "  Downloaded: $(ls $SCRIPTS_DIR/*.py 2>/dev/null | wc -l) scripts"

run_script() {
    local script="$1"
    local args="${@:2}"
    local name
    name=$(basename "$script" .py)
    echo ""
    echo "------------------------------------------------------------"
    echo "Running: $name $args"
    echo "------------------------------------------------------------"
    python3 "$script" --upload $args
}

# =============================================================================
# INCREMENTAL: daily run — accounts dimension, positions_cube (recent dates),
# then downstream views.
# Fully sequential to prevent read-during-write race conditions on S3 parquets.
#
# 05b (account_performance) excluded — full history rebuild, runs in full mode only.
#
# Dependency chain:
#   00 (accounts_dimension)  -->  (picks up new accounts daily)
#   02 (positions_cube)  -->  05 (client_performance)  -->  05c (validate aua vs silver)
#                                                      -->  05d (write aua certification)
#                                                      -->  07 (geo view)
#                                                      -->  08b (architect attribution)  -->  06b (client_mix_timeseries, reads rel_architect_lookup)
#                                                                                         -->  08 (adv view, reads 08b lookup)
#                                                      -->  09 (partner analytics JSON)
#                                                      -->  10 (rolling flows JSON)
# =============================================================================
if [[ "$MODE" == "incremental" ]]; then
    run_script "$SCRIPTS_DIR/00_build_accounts_dimension.py" --incremental
    run_script "$SCRIPTS_DIR/02_build_positions_cube.py" --start-date "$START_DATE"
    run_script "$SCRIPTS_DIR/05_build_client_performance.py"
    # 05c: validate AUA vs silver (non-blocking; SKIP if no silver allocation for today)
    if [ -f "$SCRIPTS_DIR/05c_validate_aua_vs_silver.py" ]; then
        python3 "$SCRIPTS_DIR/05c_validate_aua_vs_silver.py" || true
    fi
    # 05d: write AUA certification JSON (non-blocking; SKIP if no silver allocation for today)
    python3 "$SCRIPTS_DIR/05d_write_aua_certification.py" || true
    run_script "$SCRIPTS_DIR/07_build_nna_aua_by_geography.py"
    run_script "$SCRIPTS_DIR/08b_build_architect_attribution.py"
    run_script "$SCRIPTS_DIR/06b_build_client_mix_timeseries.py" --incremental --workers 8
    run_script "$SCRIPTS_DIR/08_build_nna_aua_by_advisor.py"
    run_script "$SCRIPTS_DIR/09_generate_partner_analytics.py"
    run_script "$SCRIPTS_DIR/10_generate_advisor_rolling_flows.py"

# =============================================================================
# FULL: monthly rebuild — all scripts in strict dependency order.
# Fully sequential to prevent read-during-write race conditions on S3 parquets.
#
# Dependency chain:
#   00 (accounts_dimension)
#   01 (advisor_assignments_history)   reads 00
#   02 (positions_cube)                reads silver
#   04 (client_dimension)              reads 00
#   03 (holdings_lots)                 reads 02, 00
#   05 (client_performance)            reads 02, 00
#   05b (account_performance)          reads 02, 00, 05
#   05c (validate aua vs silver)       reads 05, silver/allocations (non-blocking)
#   05d (write aua certification)      reads 05, silver/allocations (non-blocking)
#   06 (client_tax_liability)          reads 03
#   06b (client_mix_timeseries)        reads 02, 00, account_performance
#   07 (nna_aua_by_geography)          reads 05, 00
#   08b (architect_attribution)        reads 00, 08(prev), 05b — writes rel_architect_lookup
#   08 (nna_aua_by_advisor)            reads 05, 08b lookup
#   09 (partner_analytics)             reads 05, 05b, 07, 08, 04, 00
#   10 (advisor_rolling_flows)         reads 08, 05, 00, 04
# =============================================================================
elif [[ "$MODE" == "full" ]]; then
    run_script "$SCRIPTS_DIR/00_build_accounts_dimension.py"
    run_script "$SCRIPTS_DIR/01_build_advisor_assignments_history.py"
    run_script "$SCRIPTS_DIR/02_build_positions_cube.py"
    run_script "$SCRIPTS_DIR/04_build_client_dimension.py"
    run_script "$SCRIPTS_DIR/03_build_holdings_lots.py"
    run_script "$SCRIPTS_DIR/05_build_client_performance.py"
    run_script "$SCRIPTS_DIR/05b_build_account_performance.py"
    # 05c: validate AUA vs silver (non-blocking; SKIP if no silver allocation for today)
    if [ -f "$SCRIPTS_DIR/05c_validate_aua_vs_silver.py" ]; then
        python3 "$SCRIPTS_DIR/05c_validate_aua_vs_silver.py" || true
    fi
    # 05d: write AUA certification JSON (non-blocking; SKIP if no silver allocation for today)
    python3 "$SCRIPTS_DIR/05d_write_aua_certification.py" || true
    run_script "$SCRIPTS_DIR/06_build_client_tax_liability.py"
    run_script "$SCRIPTS_DIR/07_build_nna_aua_by_geography.py"
    run_script "$SCRIPTS_DIR/08b_build_architect_attribution.py"
    run_script "$SCRIPTS_DIR/06b_build_client_mix_timeseries.py" --workers 8
    run_script "$SCRIPTS_DIR/08_build_nna_aua_by_advisor.py"
    run_script "$SCRIPTS_DIR/09_generate_partner_analytics.py"
    run_script "$SCRIPTS_DIR/10_generate_advisor_rolling_flows.py"

else
    echo "ERROR: Unknown mode '$MODE'. Use 'incremental' or 'full'."
    exit 1
fi

echo ""
echo "============================================================"
echo "COMPLETE — ${MODE^^}"
echo "Finished:   $(date -u '+%Y-%m-%d %H:%M:%S UTC')"
echo "============================================================"

# Write pipeline-complete sentinel — triggers bd-portal-publisher + bd-portal-advisor-publisher
TIMESTAMP=$(date -u +%Y-%m-%dT%H:%M:%SZ)
echo "{\"status\":\"success\",\"mode\":\"${MODE}\",\"timestamp\":\"${TIMESTAMP}\",\"run_date\":\"${RUN_DATE}\"}" \
  | aws s3 cp - "s3://${S3_BUCKET}/gold/pipeline-complete.json" \
  && echo "Sentinel written: s3://${S3_BUCKET}/gold/pipeline-complete.json"

# Upload log to S3
aws s3 cp /tmp/gold_runner.log "s3://${S3_BUCKET}/${LOG_KEY}" --quiet && \
    echo "Log uploaded: s3://${S3_BUCKET}/${LOG_KEY}"

# Invalidate CloudFront so the portal serves fresh data immediately
INVALIDATION_ID=$(aws cloudfront create-invalidation \
    --distribution-id EVTSA9VEHNZVH \
    --paths "/api/scoped/advisor-intelligence/*" \
    --query 'Invalidation.Id' --output text)
echo "CloudFront invalidation created: ${INVALIDATION_ID}"

# Check for pending trigger before shutdown.
# If bd-gold-trigger fired while we were running, it wrote trigger-pending.json
# instead of starting a new instance. Clear the marker and re-run so no data
# day is skipped. exec replaces this process — the new run will write its own
# pipeline-complete, upload its own log, and check for pending again, so back-
# to-back skipped triggers are handled naturally. The marker is deleted before
# re-exec, so we only loop if a NEW trigger fires during the re-run.
PENDING_KEY="gold/trigger-pending.json"
PENDING_BODY=$(aws s3 cp "s3://${S3_BUCKET}/${PENDING_KEY}" - 2>/dev/null || echo "")
if echo "$PENDING_BODY" | grep -q '"pending"'; then
    echo ""
    echo "============================================================"
    echo "PENDING TRIGGER FOUND — re-running incremental"
    echo "Marker contents: ${PENDING_BODY}"
    echo "============================================================"
    aws s3 rm "s3://${S3_BUCKET}/${PENDING_KEY}" --quiet \
        && echo "Pending marker cleared"
    exec "$0" incremental
fi

# Self-stop: shut down the instance now that all work is done
echo "No pending trigger — shutting down instance..."
shutdown -h now
