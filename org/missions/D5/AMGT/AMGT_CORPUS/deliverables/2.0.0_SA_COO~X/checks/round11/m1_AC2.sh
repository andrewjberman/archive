#!/usr/bin/env bash
# AMGT_CORPUS round 11 -- check as a file (spine v3.19 L6): m1_AC2. Run from the repo root under the worker timeout.
cd "$(git rev-parse --show-toplevel)" || exit 2
export PYTHONPATH=.
python "org/missions/D5/AMGT/AMGT_CORPUS/deliverables/2.0.0_SA_COO~X/checks/round11/m1_currencies.py" 2>&1 | grep -E "^m1 names |Traceback|Error" | tail -2
