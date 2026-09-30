#!/usr/bin/env bash
# AMGT_CORPUS round 22 -- check as a file: x1_AC2 -- the write-gate tests with the dossier suites. Run from the repo root.
cd "$(git rev-parse --show-toplevel)" || exit 2
export PYTHONPATH="$(pwd)"
python -m pytest -q --color=no -p no:cacheprovider lib/research/corpus/tests/test_dossier_method_bump.py lib/research/corpus/tests/test_dossier_pack_shape.py lib/research/corpus/tests/test_dossier_canonical_address.py lib/research/corpus/tests/test_dossier_case_positional.py lib/research/corpus/tests/test_dossier_case_body.py lib/research/corpus/tests/test_dossier_case_unit.py lib/research/corpus/tests/test_dossier_reader_method.py lib/research/corpus/tests/test_dossier_newest.py 2>&1 | grep -E 'passed|failed|error|no tests ran' | tail -2
