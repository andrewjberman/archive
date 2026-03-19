#!/bin/bash
#
# Gold Layer Generation Pipeline
#
# Wrapper script that calls the optimized unified generator.
# Kept for backwards compatibility with EC2 user-data.
#
# Usage:
#   ./run_all.sh              # Dry run
#   ./run_all.sh --upload     # Production (upload to S3)
#

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "======================================================================"
echo "GOLD LAYER PIPELINE (via unified generator)"
echo "Started: $(date -Iseconds)"
echo "======================================================================"

# Parse arguments
UPLOAD_FLAG=""
VERBOSE_FLAG=""

while [[ $# -gt 0 ]]; do
    case $1 in
        --upload)
            UPLOAD_FLAG="--upload"
            shift
            ;;
        --local)
            # Ignored - unified script always uses S3
            shift
            shift 2>/dev/null || true
            ;;
        -v|--verbose)
            VERBOSE_FLAG="-v"
            shift
            ;;
        *)
            shift
            ;;
    esac
done

# Run the unified generator (loads data once, runs in parallel)
python3 "${SCRIPT_DIR}/generate_all_gold.py" $UPLOAD_FLAG $VERBOSE_FLAG

echo ""
echo "======================================================================"
echo "EXTENDED GOLD GENERATORS (08-10, output to opal-data-bd/gold/)"
echo "======================================================================"

if [ -n "$UPLOAD_FLAG" ]; then
    echo "Running extended gold generators..."

    echo "  [1/3] Timeseries Chart..."
    python3 "${SCRIPT_DIR}/08_generate_timeseries_chart.py" --upload || echo "  ⚠ Timeseries Chart failed"

    echo "  [2/3] Client Detail..."
    python3 "${SCRIPT_DIR}/09_generate_client_detail.py" --upload || echo "  ⚠ Client Detail failed"

    echo "  [3/3] Book Views..."
    python3 "${SCRIPT_DIR}/10_generate_book_views.py" --upload || echo "  ⚠ Book Views failed"

    echo "Extended gold generators complete!"
else
    echo "Skipping extended gold generators (dry run mode)"
fi

echo ""
echo "======================================================================"
echo "PORTAL JSON GENERATORS (for opal-data-portal-v2)"
echo "======================================================================"

# Generate portal-specific JSONs (these output to opal-data-portal-v2 bucket)
if [ -n "$UPLOAD_FLAG" ]; then
    echo "Running portal JSON generators..."

    echo "  [1/4] AUA Chart (from allocations)..."
    python3 "${SCRIPT_DIR}/12_generate_aua_chart.py" --upload || echo "  ⚠ AUA Chart failed"

    echo "  [2/4] Flows Chart (from transactions)..."
    python3 "${SCRIPT_DIR}/13_generate_flows_chart.py" --upload || echo "  ⚠ Flows Chart failed"

    echo "  [3/4] Leaderboards (architect & implementor)..."
    python3 "${SCRIPT_DIR}/11_generate_leaderboards.py" --upload || echo "  ⚠ Leaderboards failed"

    echo "  [4/4] Clients Tab..."
    python3 "${SCRIPT_DIR}/11_generate_clients_tab.py" --upload || echo "  ⚠ Clients Tab failed"

    echo "Portal JSONs complete!"
else
    echo "Skipping portal JSON upload (dry run mode)"
fi

echo ""
echo "======================================================================"
echo "PIPELINE COMPLETE"
echo "Finished: $(date -Iseconds)"
echo "======================================================================"
