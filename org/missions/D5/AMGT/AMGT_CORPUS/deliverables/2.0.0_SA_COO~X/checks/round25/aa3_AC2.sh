#!/usr/bin/env bash
# AMGT_CORPUS round 25 -- check as a file: aa3_AC2 -- the round-25 family tests with the builder suites. Run from the repo root.
cd "$(git rev-parse --show-toplevel)" || exit 2
export PYTHONPATH="$(pwd)"
python -m pytest -q --color=no -p no:cacheprovider integrations/bloomberg/research/tests/test_build_unit_map_families_round25.py integrations/bloomberg/research/tests/test_build_unit_map_families_round24.py integrations/bloomberg/research/tests/test_build_unit_map_families.py integrations/bloomberg/research/tests/test_build_unit_map_discriminate.py integrations/bloomberg/research/tests/test_build_unit_map_exceptions.py integrations/bloomberg/research/tests/test_build_unit_map_classification_split.py 2>&1 | grep -E 'passed|failed|error|no tests ran' | tail -2
