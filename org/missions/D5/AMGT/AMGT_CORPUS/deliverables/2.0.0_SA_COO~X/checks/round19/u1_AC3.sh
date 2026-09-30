#!/usr/bin/env bash
# AMGT_CORPUS round 19 -- check as a file: u1_AC3 -- the reader tests, the classification-split suite with them. Run from the repo root.
cd "$(git rev-parse --show-toplevel)" || exit 2
export PYTHONPATH="$(pwd)"
python -m pytest -q --color=no -p no:cacheprovider integrations/bloomberg/research/tests/test_model_block_resolved_exception.py integrations/bloomberg/research/tests/test_build_unit_map_classification_split.py 2>&1 | grep -E 'passed|failed|error|no tests ran' | tail -2
