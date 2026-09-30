#!/usr/bin/env bash
# AMGT_CORPUS round 23 -- check as a file: y2_AC2 -- the no-SA-fallback tests (the fallback is never called; a gap stays a labelled gap) with the producer suites. Run from the repo root.
cd "$(git rev-parse --show-toplevel)" || exit 2
export PYTHONPATH="$(pwd)"
python -m pytest -q --color=no -p no:cacheprovider integrations/bloomberg/research/tests/test_model_block_no_sa_fallback.py integrations/bloomberg/research/tests/test_model_block_resolved_exception.py integrations/bloomberg/research/tests/test_model_block_unit_map_write.py integrations/bloomberg/research/tests/test_model_block_admit.py 2>&1 | grep -E 'passed|failed|error|no tests ran' | tail -2
