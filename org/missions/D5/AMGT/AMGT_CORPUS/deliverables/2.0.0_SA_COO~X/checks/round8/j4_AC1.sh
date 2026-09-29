#!/usr/bin/env bash
# AMGT_CORPUS round 8 -- check as a file (spine v3.19 L6): j4_AC1. Run from the repo root under the worker timeout.
cd "$(git rev-parse --show-toplevel)" || exit 2
export PYTHONPATH=.
python -m pytest lib/research/corpus/tests/test_dossier_reader_method.py -q --color=no -p no:cacheprovider 2>&1 | tail -3
