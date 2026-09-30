#!/usr/bin/env bash
# AMGT_CORPUS round 21 -- check as a file: w1_AC2 -- the pack_shape tests with the dossier suites that build the document. Run from the repo root.
cd "$(git rev-parse --show-toplevel)" || exit 2
export PYTHONPATH="$(pwd)"
python -m pytest -q --color=no -p no:cacheprovider lib/research/corpus/tests/test_dossier_pack_shape.py lib/research/corpus/tests/test_dossier_canonical_address.py 2>&1 | grep -E 'passed|failed|error|no tests ran' | tail -2
