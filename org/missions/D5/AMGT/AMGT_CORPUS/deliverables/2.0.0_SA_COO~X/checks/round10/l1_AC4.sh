#!/usr/bin/env bash
# AMGT_CORPUS round 10 -- check as a file: l1_AC4 (amendment on 2.0.0_SA_COO~Z msg 26444). Run from the repo root.
cd "$(git rev-parse --show-toplevel)" || exit 2
export PYTHONPATH=.
python "org/missions/D5/AMGT/AMGT_CORPUS/deliverables/2.0.0_SA_COO~X/checks/round10/l1_import.py" 2>&1 | grep "^l1 " | tail -1
