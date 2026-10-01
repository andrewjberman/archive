#!/usr/bin/env bash
# AMGT_CORPUS round 27 -- check as a file: ac1_AC1 -- the ZERO-DOMINATED class on BBSE3 CAPITAL_EXPEND; every other unit over 100 keys byte-unchanged; bands unchanged. Run from the repo root.
cd "$(git rev-parse --show-toplevel)" || exit 2
export PYTHONPATH="$(pwd)"
python org/missions/D5/AMGT/AMGT_CORPUS/deliverables/2.0.0_SA_COO~X/checks/round27/ac1_check.py 2>&1 | grep -E '^ac1 |Error' | tail -1
