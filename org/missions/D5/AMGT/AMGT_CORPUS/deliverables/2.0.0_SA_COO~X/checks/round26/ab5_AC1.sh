#!/usr/bin/env bash
# AMGT_CORPUS round 26 -- check as a file: ab5_AC1 -- the BP/NG header-currency census and the label rule. Run from the repo root.
cd "$(git rev-parse --show-toplevel)" || exit 2
export PYTHONPATH="$(pwd)"
python org/missions/D5/AMGT/AMGT_CORPUS/deliverables/2.0.0_SA_COO~X/checks/round26/ab5_check.py 2>&1 | grep -E '^ab5 |Error' | tail -1
