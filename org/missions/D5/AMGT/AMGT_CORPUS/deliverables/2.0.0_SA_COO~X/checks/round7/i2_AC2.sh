#!/usr/bin/env bash
# AMGT_CORPUS round 7 -- check as a file (spine v3.19 L6): i2_AC2. Run from the repo root under the worker's timeout.
cd "$(git rev-parse --show-toplevel)" || exit 2
PYTHONPATH="$(pwd)" python integrations/bloomberg/research/model_block_pull.py cases-report --securities "SAN FP Equity" "BA US Equity" 2>&1 | grep -v -E 'fitz|MuPDF' | tail -4
