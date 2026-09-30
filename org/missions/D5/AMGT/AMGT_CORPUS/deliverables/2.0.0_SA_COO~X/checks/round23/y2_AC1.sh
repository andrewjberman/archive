#!/usr/bin/env bash
# AMGT_CORPUS round 23 -- check as a file: y2_AC1 -- the derive dry-run names the SA fallback held off for the two c2 names. Run from the repo root.
cd "$(git rev-parse --show-toplevel)" || exit 2
export PYTHONPATH="$(pwd)"
python integrations/bloomberg/research/model_block_pull.py derive --dry-run --no-sa-fallback --securities '8316 JP Equity' '8766 JP Equity' 2>&1 | grep -E '^DRY-RUN DERIVE|^DRY RUN DERIVE DONE|error' | tail -3
