#!/usr/bin/env bash
# AMGT_CORPUS round 4 -- check as a file (spine v3.19 L6): f2_AC2. Run from the repo root under the worker's timeout.
cd "$(git rev-parse --show-toplevel)" || exit 2
PYTHONPATH="$(pwd)" python integrations/bloomberg/research/model_block_pull.py pull --securities "ADBE US Equity" --dry-run 2>&1 | grep -v -E 'fitz|MuPDF' | tail -12
