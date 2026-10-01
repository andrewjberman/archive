#!/usr/bin/env bash
# AMGT_CORPUS round 24 -- check as a file: z2_AC2 -- the anchor tests. Run from the repo root.
cd "$(git rev-parse --show-toplevel)" || exit 2
export PYTHONPATH="$(pwd)"
python -m pytest -q --color=no -p no:cacheprovider integrations/bloomberg/research/tests/test_unit_anchor.py 2>&1 | grep -E 'passed|failed|error|no tests ran' | tail -2
