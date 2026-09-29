#!/usr/bin/env bash
# AMGT_CORPUS round 14 -- check as a file (spine v3.19 L6): p5_AC1. Run from the repo root under the worker's timeout.
cd "$(git rev-parse --show-toplevel)" || exit 2
export PYTHONPATH="$(pwd)"
python -m pytest -q --color=no lib/research/corpus/tests/test_continuation.py lib/research/corpus/tests/test_continuation_terms.py lib/research/corpus/tests/test_continuation_reader_method.py lib/research/corpus/tests/test_continuation_pillar_body.py 2>&1 | tail -2
