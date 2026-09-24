#!/usr/bin/env bash
# AMGT_CORPUS round 3 -- check as a file (spine v3.19 L6): e2_AC2. Run from the repo root under the worker's timeout.
cd "$(git rev-parse --show-toplevel)" || exit 2
PYTHONPATH="$(pwd)" python integrations/bloomberg/research/model_block_pull.py pull --securities ASML_NA_Equity --dry-run 2>&1 | tail -6
