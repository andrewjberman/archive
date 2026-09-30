#!/usr/bin/env bash
# AMGT_CORPUS round 18 -- check as a file: t1_AC3 -- the admit step runs after registration on the scheduled path, offline. Run from the repo root.
cd "$(git rev-parse --show-toplevel)" || exit 2
export PYTHONPATH="$(pwd)"
python -m pytest -q --color=no -s lib/research/corpus/tests/test_induction_schedule.py 2>&1 | grep -E '^t1 scheduled|^r1 |passed|failed|error' | tail -4
