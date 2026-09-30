#!/usr/bin/env bash
# AMGT_CORPUS round 21 -- check as a file: w3_AC1 -- the cross-field discriminator over the nine named facts plus the MEASURED control. Run from the repo root.
cd "$(git rev-parse --show-toplevel)" || exit 2
export PYTHONPATH="$(pwd)"
python org/missions/D5/AMGT/AMGT_CORPUS/deliverables/2.0.0_SA_COO~X/checks/round21/w3_check.py 2>&1 | grep -E '^w3 ' | tail -1
