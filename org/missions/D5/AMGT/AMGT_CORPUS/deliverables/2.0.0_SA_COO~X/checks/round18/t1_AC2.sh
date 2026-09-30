#!/usr/bin/env bash
# AMGT_CORPUS round 18 -- check as a file: t1_AC2 -- the refusing transport and the planted name, offline. Run from the repo root.
cd "$(git rev-parse --show-toplevel)" || exit 2
export PYTHONPATH="$(pwd)"
python -m pytest -q --color=no -s integrations/bloomberg/research/tests/test_model_block_admit.py 2>&1 | grep -E '^t1 |passed|failed|error|no tests ran' | tail -4
