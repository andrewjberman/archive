#!/usr/bin/env bash
# AMGT_CORPUS round 10 -- check as a file (spine v3.19 L6): l4_AC2. Run from the repo root under the worker timeout.
cd "$(git rev-parse --show-toplevel)" || exit 2
export PYTHONPATH=.
out=$(python -m integrations.bloomberg.research.model_block_pull cases-report --securities AMD_US_Equity 2>&1); rc=$?
printf "%s\n" "$out" | grep -v fitz | tail -2
echo "l4 planted_underscore rc $rc"
