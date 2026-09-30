#!/usr/bin/env bash
# AMGT_CORPUS round 26 -- check as a file: ab1_AC2 -- the dossier reader tests. Run from the repo root.
cd "$(git rev-parse --show-toplevel)" || exit 2
export PYTHONPATH="$(pwd)"
python -m pytest -q --color=no -p no:cacheprovider lib/research/corpus/tests/test_dossier_slash_safe_round26.py 2>&1 | grep -E 'passed|failed|error|no tests ran' | tail -2
