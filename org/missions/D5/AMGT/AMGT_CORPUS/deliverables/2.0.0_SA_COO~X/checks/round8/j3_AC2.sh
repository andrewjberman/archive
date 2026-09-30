#!/usr/bin/env bash
# AMGT_CORPUS round 8 -- check as a file (spine v3.19 L6): j3_AC2. Run from the repo root under the worker timeout.
cd "$(git rev-parse --show-toplevel)" || exit 2
export PYTHONPATH=.
python -m integrations.bloomberg.research.model_block_pull stamp-census --securities "6861 JP Equity" "BZLFY US Equity" "CAT US Equity" "CSL AU Equity" "PBR US Equity" "TSM US Equity" 2>&1 | grep -E "^stamp_census |^stamp |Traceback|Error|error:" | tail -8
