#!/usr/bin/env bash
# AMGT_CORPUS round 3 -- check as a file (spine v3.19 L6): e2_AC1. Run from the repo root under the worker's timeout.
cd "$(git rev-parse --show-toplevel)" || exit 2
python -m pytest integrations/bloomberg/research/tests/test_model_block_22_fields.py -q --color=no -p no:cacheprovider 2>&1 | tail -3
