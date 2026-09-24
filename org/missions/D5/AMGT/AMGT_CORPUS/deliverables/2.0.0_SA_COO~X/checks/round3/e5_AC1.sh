#!/usr/bin/env bash
# AMGT_CORPUS round 3 -- check as a file (spine v3.19 L6): e5_AC1. Run from the repo root under the worker's timeout.
cd "$(git rev-parse --show-toplevel)" || exit 2
python -m pytest lib/research/corpus/tests/test_backlog.py -q --color=no -p no:cacheprovider -k "empty_shell" 2>&1 | tail -3
