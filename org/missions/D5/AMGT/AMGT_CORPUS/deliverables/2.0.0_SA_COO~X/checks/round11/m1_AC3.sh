#!/usr/bin/env bash
# AMGT_CORPUS round 11 -- check as a file: m1_AC3 (AMENDMENT 1, the CTO SHOP carve-out). Run from the repo root.
cd "$(git rev-parse --show-toplevel)" || exit 2
export PYTHONPATH=.
python "org/missions/D5/AMGT/AMGT_CORPUS/deliverables/2.0.0_SA_COO~X/checks/round11/m1_shop.py" 2>&1 | grep -E "^m1 |Traceback" | tail -3
