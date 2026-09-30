#!/usr/bin/env bash
# AMGT_CORPUS round 13 -- check as a file (spine v3.19 L6): o1_AC1. Run from the repo root under the worker's timeout.
cd "$(git rev-parse --show-toplevel)" || exit 2
python org/missions/D5/AMGT/AMGT_CORPUS/deliverables/2.0.0_SA_COO~X/checks/round13/o1_check.py structure org/missions/D5/AMGT/AMGT_CORPUS/deliverables/0.9.0_WK_AMGT_CORPUS~1/FWD_EVIDENCE_ROUND13.json 2>&1 | tail -3
