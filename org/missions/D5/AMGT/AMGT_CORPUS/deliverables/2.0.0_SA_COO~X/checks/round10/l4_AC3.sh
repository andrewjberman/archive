#!/usr/bin/env bash
# AMGT_CORPUS round 10 -- check as a file (spine v3.19 L6): l4_AC3. Run from the repo root under the worker timeout.
cd "$(git rev-parse --show-toplevel)" || exit 2
export PYTHONPATH=.
python -m integrations.bloomberg.research.model_block_pull cases-report --securities "AMD US Equity" 2>&1 | grep -E "^cases AMD_US_Equity |^cases_report " | tail -2
