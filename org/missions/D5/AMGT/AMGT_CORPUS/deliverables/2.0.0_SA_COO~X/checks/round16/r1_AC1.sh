#!/usr/bin/env bash
# AMGT_CORPUS round 16 -- check as a file (spine v3.19 L6): r1_AC1. Run from the repo root under the worker's timeout.
# The scheduled path, driven offline: the runner the task invokes, in its dry-run mode, over a scratch library with
# one planted EVIDENCED folder and one planted AMBIGUOUS folder.
cd "$(git rev-parse --show-toplevel)" || exit 2
export PYTHONPATH="$(pwd)"
python -m pytest -q --color=no -s lib/research/corpus/tests/test_induction_schedule.py 2>&1 | grep -E '^r1 |passed|failed|error' | tail -4
