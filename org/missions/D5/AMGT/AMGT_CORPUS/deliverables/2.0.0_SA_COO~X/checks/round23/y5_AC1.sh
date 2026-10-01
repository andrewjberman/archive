#!/usr/bin/env bash
# AMGT_CORPUS round 23 -- check as a file: y5_AC1 -- the sign reader on every figure of the 97 served blocks against each figure's own value. Run from the repo root.
cd "$(git rev-parse --show-toplevel)" || exit 2
export PYTHONPATH="$(pwd)"
python org/missions/D5/AMGT/AMGT_CORPUS/deliverables/2.0.0_SA_COO~X/checks/round23/y5_signs.py org/missions/D5/AMGT/AMGT_CORPUS/deliverables/2.0.0_SA_COO~X/checks/round23/y4_pass_keys.txt 2>&1 | grep -E '^y5 |Error' | tail -1
