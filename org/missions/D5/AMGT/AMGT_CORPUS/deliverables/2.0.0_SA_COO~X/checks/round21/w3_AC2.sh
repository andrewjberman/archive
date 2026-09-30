#!/usr/bin/env bash
# AMGT_CORPUS round 21 -- check as a file: w3_AC2 -- the discriminator tests (a planted inconsistent input stays UNRESOLVED) with the builder's suites. Run from the repo root.
cd "$(git rev-parse --show-toplevel)" || exit 2
export PYTHONPATH="$(pwd)"
python -m pytest -q --color=no -p no:cacheprovider integrations/bloomberg/research/tests/test_build_unit_map_discriminate.py integrations/bloomberg/research/tests/test_build_unit_map_cli_header.py integrations/bloomberg/research/tests/test_build_unit_map_exceptions.py integrations/bloomberg/research/tests/test_build_unit_map_classification_split.py 2>&1 | grep -E 'passed|failed|error|no tests ran' | tail -2
