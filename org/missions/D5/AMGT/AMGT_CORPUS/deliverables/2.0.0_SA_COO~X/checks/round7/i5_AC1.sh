#!/usr/bin/env bash
# AMGT_CORPUS round 7 -- check as a file (spine v3.19 L6): i5_AC1. Run from the repo root under the worker's timeout.
cd "$(git rev-parse --show-toplevel)" || exit 2
python org/missions/D5/AMGT/AMGT_CORPUS/deliverables/2.0.0_SA_COO~X/checks/round5/g4_check.py structure org/missions/D5/AMGT/AMGT_CORPUS/deliverables/0.9.0_WK_AMGT_CORPUS~5/FWD_EVIDENCE_ROUND7.json 2>&1 | tail -3
