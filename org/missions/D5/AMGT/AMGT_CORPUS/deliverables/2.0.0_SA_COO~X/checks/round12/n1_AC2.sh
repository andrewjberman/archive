#!/usr/bin/env bash
# AMGT_CORPUS round 12 -- check as a file (spine v3.19 L6): n1_AC2. Run from the repo root under the worker timeout.
cd "$(git rev-parse --show-toplevel)" || exit 2
export PYTHONPATH=.
python "org/missions/D5/AMGT/AMGT_CORPUS/deliverables/2.0.0_SA_COO~X/checks/round12/n1_addr.py" 2>&1 | grep -E "^n1 |Traceback|Error" | tail -2
