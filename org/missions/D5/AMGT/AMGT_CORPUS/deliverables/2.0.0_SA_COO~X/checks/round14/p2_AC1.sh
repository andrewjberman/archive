#!/usr/bin/env bash
# AMGT_CORPUS round 14 -- check as a file (spine v3.19 L6): p2_AC1. Run from the repo root under the worker's timeout.
cd "$(git rev-parse --show-toplevel)" || exit 2
export PYTHONPATH="$(pwd)"
python -m pytest -q --color=no -s lib/research/corpus/tests/test_induction_planted_drive.py 2>&1 | grep -E '^fwd4 |passed|failed|error' | tail -4
