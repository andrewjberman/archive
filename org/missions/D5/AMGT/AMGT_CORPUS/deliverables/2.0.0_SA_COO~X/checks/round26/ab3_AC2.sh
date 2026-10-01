#!/usr/bin/env bash
# AMGT_CORPUS round 26 -- check as a file: ab3_AC2 -- the case_rule tests. Run from the repo root.
cd "$(git rev-parse --show-toplevel)" || exit 2
export PYTHONPATH="$(pwd)"
python -m pytest -q --color=no -p no:cacheprovider lib/research/api/tests/test_case_rule_mixed_input_round26.py 2>&1 | grep -E 'passed|failed|error|no tests ran' | tail -2
