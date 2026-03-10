#!/bin/bash
# BD Gold Layer - Detail Generator EC2 User Data Script
# Runs scripts 07, 09, 10, 11 (heavy workloads with positions)

set -e

# Configuration
S3_BUCKET="opal-data-bd"
SCRIPTS_DIR="/home/ec2-user/gold-scripts"
LOG_FILE="/var/log/bd-gold-detail-$(date +%Y%m%d_%H%M%S).log"

# Log everything
exec 1> >(tee -a "$LOG_FILE")
exec 2>&1

echo "======================================================================"
echo "BD GOLD LAYER - STAGE 4 DETAIL GENERATION"
echo "Started: $(date -Iseconds)"
echo "======================================================================"

# Install dependencies
echo ""
echo "=== Installing Dependencies ==="
yum install -y python3.11 python3.11-pip
python3.11 -m pip install --upgrade pip

# Create working directory
mkdir -p "$SCRIPTS_DIR"
cd "$SCRIPTS_DIR"

# Download scripts from S3
echo ""
echo "=== Downloading Scripts from S3 ==="
aws s3 sync s3://${S3_BUCKET}/scripts/gold_layer/ . \
  --exclude "*" \
  --include "07_generate_partner_analytics.py" \
  --include "09_generate_client_detail.py" \
  --include "10_generate_book_views.py" \
  --include "11_generate_clients_tab.py" \
  --include "load_silver.py" \
  --include "pii_hasher.py" \
  --include "utils/*.py"

echo "✓ Scripts downloaded"

# Install Python dependencies
echo ""
echo "=== Installing Python Packages ==="
pip3.11 install pandas pyarrow boto3 numpy python-dateutil s3fs -q
echo "✓ Dependencies installed"

# Run heavy analytics scripts
echo ""
echo "=== Running Heavy Analytics Scripts ==="

run_script() {
  local script=$1
  local start=$(date +%s)

  echo ""
  echo ">>> Running: $script"
  echo "    Started: $(date -Iseconds)"

  python3.11 "$script" --upload

  local end=$(date +%s)
  local duration=$((end - start))
  echo "    Duration: ${duration}s"
  echo "    Status: ✓ Complete"
}

# Execute in order (some have dependencies)
run_script "07_generate_partner_analytics.py"
run_script "09_generate_client_detail.py"
run_script "10_generate_book_views.py"
run_script "11_generate_clients_tab.py"

# Upload log to S3
echo ""
echo "=== Uploading Execution Log ==="
aws s3 cp "$LOG_FILE" "s3://${S3_BUCKET}/logs/gold-detail/$(basename $LOG_FILE)"
echo "✓ Log uploaded"

# Create completion marker
echo ""
echo "=== Creating Completion Marker ==="
echo "{\"status\":\"complete\",\"timestamp\":\"$(date -Iseconds)\",\"log\":\"s3://${S3_BUCKET}/logs/gold-detail/$(basename $LOG_FILE)\"}" > /tmp/completion.json
aws s3 cp /tmp/completion.json "s3://${S3_BUCKET}/status/gold-detail-completion.json"
echo "✓ Completion marker created"

echo ""
echo "======================================================================"
echo "STAGE 4 DETAIL GENERATION COMPLETE"
echo "Finished: $(date -Iseconds)"
echo "======================================================================"

# Auto-shutdown
echo ""
echo "Shutting down instance in 60 seconds..."
sleep 60
shutdown -h now
