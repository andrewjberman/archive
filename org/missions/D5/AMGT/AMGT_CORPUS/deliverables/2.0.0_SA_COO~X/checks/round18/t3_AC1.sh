#!/usr/bin/env bash
# AMGT_CORPUS round 18 -- check as a file: t3_AC1 -- the reader census. Run from the repo root.
cd "$(git rev-parse --show-toplevel)" || exit 2
python org/missions/D5/AMGT/AMGT_CORPUS/deliverables/2.0.0_SA_COO~X/checks/round18/t3_census.py 2>&1 | grep -E '^t3 ' | tail -1
