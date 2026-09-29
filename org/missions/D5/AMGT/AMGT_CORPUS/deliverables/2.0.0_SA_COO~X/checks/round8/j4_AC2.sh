#!/usr/bin/env bash
# AMGT_CORPUS round 8 -- check as a file (spine v3.19 L6): j4_AC2. Run from the repo root under the worker timeout.
cd "$(git rev-parse --show-toplevel)" || exit 2
export PYTHONPATH=.
python -m lib.research.corpus.dossier --pick-census 2>&1 | grep -E "^dossier_pick |Traceback|Error|error:" | tail -3
