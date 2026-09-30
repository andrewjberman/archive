#!/usr/bin/env bash
# AMGT_CORPUS round 20 -- check as a file: v1_AC2 -- the LF write test with the suites that touch the changed calls. Run from the repo root.
cd "$(git rev-parse --show-toplevel)" || exit 2
export PYTHONPATH="$(pwd)"
python -m pytest -q --color=no -p no:cacheprovider integrations/bloomberg/research/tests/test_model_block_unit_map_write.py integrations/bloomberg/research/tests/test_model_block_admit.py lib/research/corpus/tests/test_induction_planted_drive.py lib/research/corpus/tests/test_induction_schedule.py 2>&1 | grep -E 'passed|failed|error|no tests ran' | tail -2
