#!/usr/bin/env bash
# AMGT_CORPUS round 22 -- check as a file: x2_AC1 -- the unit apply on a temp copy of the committed map, diffed entry by entry, with the u-1 reader probed. Run from the repo root.
cd "$(git rev-parse --show-toplevel)" || exit 2
export PYTHONPATH="$(pwd)"
python org/missions/D5/AMGT/AMGT_CORPUS/deliverables/2.0.0_SA_COO~X/checks/round22/x2_check.py 2>&1 | grep -E '^x2 ' | tail -1
