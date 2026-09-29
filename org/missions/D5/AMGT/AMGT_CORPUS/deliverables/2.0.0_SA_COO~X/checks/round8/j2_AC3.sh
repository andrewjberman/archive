#!/usr/bin/env bash
# AMGT_CORPUS round 8 -- check as a file (spine v3.19 L6): j2_AC3. Run from the repo root under the worker timeout.
cd "$(git rev-parse --show-toplevel)" || exit 2
export PYTHONPATH=.
python -m pytest lib/research/corpus/tests/test_induction_run.py lib/research/corpus/tests/test_key_glob_census.py lib/research/corpus/tests/test_readonly_proof.py lib/research/corpus/tests/test_readonly_proof_tristate.py -q --color=no -p no:cacheprovider 2>&1 | tail -3
