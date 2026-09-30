#!/usr/bin/env bash
# AMGT_CORPUS round 18 -- check as a file: t1_AC1 -- the population mode, dry-run on the LIVE population (S3 list only, no vendor call). Run from the repo root.
cd "$(git rev-parse --show-toplevel)" || exit 2
export PYTHONPATH="$(pwd)"
python integrations/bloomberg/research/model_block_pull.py admit --dry-run 2>&1 | grep -E '^(admit |REFUSE|usage|error)' | tail -3
