#!/usr/bin/env bash
# AMGT_CORPUS round 3 -- check as a file (spine v3.19 L6): e2_AC3. Run from the repo root under the worker's timeout.
cd "$(git rev-parse --show-toplevel)" || exit 2
PYTHONPATH="$(pwd)" python integrations/bloomberg/research/model_block_pull.py pull --securities A_US_Equity B_US_Equity C_US_Equity D_US_Equity --dry-run 2>&1 | tail -2
