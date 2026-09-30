#!/usr/bin/env bash
# AMGT_CORPUS round 23 -- check as a file: y5_AC2 -- the per-figure sign tests (a planted loss year, CAPITAL_EXPEND's convention, NET_DEBT's pair, an UNRESOLVED kept) with the producer suites. Run from the repo root.
cd "$(git rev-parse --show-toplevel)" || exit 2
export PYTHONPATH="$(pwd)"
python -m pytest -q --color=no -p no:cacheprovider integrations/bloomberg/research/tests/test_model_block_sign_per_figure.py integrations/bloomberg/research/tests/test_model_block_resolved_exception.py integrations/bloomberg/research/tests/test_model_block_no_sa_fallback.py integrations/bloomberg/research/tests/test_build_unit_map_classification_split.py 2>&1 | grep -E 'passed|failed|error|no tests ran' | tail -2
