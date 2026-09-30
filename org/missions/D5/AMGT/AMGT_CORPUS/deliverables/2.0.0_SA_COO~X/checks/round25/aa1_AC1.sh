#!/usr/bin/env bash
# AMGT_CORPUS round 25 -- check as a file: aa1_AC1 -- the denomination census over the measured population, and the label rule read through _figure_currency. Run from the repo root.
cd "$(git rev-parse --show-toplevel)" || exit 2
export PYTHONPATH="$(pwd)"
python org/missions/D5/AMGT/AMGT_CORPUS/deliverables/2.0.0_SA_COO~X/checks/round25/aa1_check.py 2>&1 | grep -E '^aa1 |Error' | tail -1
