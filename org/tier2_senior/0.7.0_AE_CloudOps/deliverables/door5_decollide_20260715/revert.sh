#!/usr/bin/env bash
# =============================================================================
# DOOR-5 DE-COLLIDE REVERT -- one command restores the pre-motion collision state.
# Written and committed BEFORE the open (hold-doc requirement: "the revert written
# BEFORE the open. That is the difference between a decision and an accident.")
#
# Restores ALL FOUR keys to the banked pre-motion bytes (the two silver keys are
# untouched by the de-collide; restoring them is an idempotent no-op included so
# this script is a FULL-STATE restore, not a delta guess).
#
# Post-revert expected ETags (single-part MD5s):
#   code/gold/build_assets_dim.py        ee55f2c59c96dbee16b76b3f5b146352 (8,498 B)
#   code/gold/_orion_api_silver_lib.py   65baced672b102f8bebff961a72276ff (21,132 B)
#   code/silver/build_assets_dim.py      7c0df7f0340c593313d6fcb2c47d504e (9,244 B)
#   code/silver/_orion_api_silver_lib.py 7cb5c6ce49d8ea735f7ae42a359f3fce (28,694 B)
#
# Rule 16: Git Bash 3.6.7 utilities only. ASCII only.
# =============================================================================
set -euo pipefail
cd "$(dirname "$0")"

aws s3 cp bank/gold/build_assets_dim.py        s3://opal-data-inf/code/gold/build_assets_dim.py
aws s3 cp bank/gold/_orion_api_silver_lib.py   s3://opal-data-inf/code/gold/_orion_api_silver_lib.py
aws s3 cp bank/silver/build_assets_dim.py      s3://opal-data-inf/code/silver/build_assets_dim.py
aws s3 cp bank/silver/_orion_api_silver_lib.py s3://opal-data-inf/code/silver/_orion_api_silver_lib.py

echo "-- post-revert verification (ETags must match the header) --"
aws s3api list-objects-v2 --bucket opal-data-inf --prefix code/ \
  --query "Contents[?contains(Key, 'build_assets_dim.py') || contains(Key, '_orion_api_silver_lib.py')].{Key:Key,Size:Size,ETag:ETag}" \
  --output table
echo "REVERT COMPLETE -- collision state restored; sync_scripts FATAL guard re-armed."
