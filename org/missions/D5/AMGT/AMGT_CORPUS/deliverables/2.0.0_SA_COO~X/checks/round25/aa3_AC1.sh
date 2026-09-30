#!/usr/bin/env bash
# AMGT_CORPUS round 25 -- check as a file: aa3_AC1 -- the class table of the remaining UNRESOLVED against the served count and the builder projection. Run from the repo root.
cd "$(git rev-parse --show-toplevel)" || exit 2
export PYTHONPATH="$(pwd)"
python org/missions/D5/AMGT/AMGT_CORPUS/deliverables/2.0.0_SA_COO~X/checks/round25/aa3_check.py 2>&1 | grep -E '^aa3 |Error' | tail -1
