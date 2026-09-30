#!/usr/bin/env bash
# AMGT_CORPUS round 10 -- check as a file (spine v3.19 L6): l2_AC2. Run from the repo root under the worker timeout.
cd "$(git rev-parse --show-toplevel)" || exit 2
export PYTHONPATH=.
python -m lib.research.corpus.base_census 2>&1 | grep -E "^base ADBE_US_Equity |^base_census |Traceback|Error|error:|No module" | tail -4
