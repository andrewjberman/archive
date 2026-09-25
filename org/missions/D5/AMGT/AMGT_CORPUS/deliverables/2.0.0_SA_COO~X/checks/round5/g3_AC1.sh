#!/usr/bin/env bash
# AMGT_CORPUS round 5 -- check as a file (spine v3.19 L6): g3_AC1. Run from the repo root under the worker's timeout.
cd "$(git rev-parse --show-toplevel)" || exit 2
python -m pytest lib/research/corpus/tests/test_backlog_fence_names.py -q --color=no -p no:cacheprovider 2>&1 | tail -3
