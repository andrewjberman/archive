#!/usr/bin/env bash
# AMGT_CORPUS round 7 -- check as a file (spine v3.19 L6): i1_AC2. Run from the repo root under the worker's timeout.
cd "$(git rev-parse --show-toplevel)" || exit 2
PYTHONPATH="$(pwd)" python "org/missions/D5/AMGT/AMGT_CORPUS/deliverables/2.0.0_SA_COO~X/checks/round7/continuation_pick_census.py" 2>&1 | grep -v -E 'fitz|MuPDF' | tail -4
