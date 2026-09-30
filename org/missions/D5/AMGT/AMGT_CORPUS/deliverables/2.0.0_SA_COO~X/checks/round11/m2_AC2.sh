#!/usr/bin/env bash
# AMGT_CORPUS round 11 -- check as a file (spine v3.19 L6): m2_AC2. Run from the repo root under the worker timeout.
cd "$(git rev-parse --show-toplevel)" || exit 2
export PYTHONPATH=.
python -m lib.research.corpus.dossier --case-positional-census 2>&1 | grep -E "^positional |Traceback|Error|error:" | tail -8
