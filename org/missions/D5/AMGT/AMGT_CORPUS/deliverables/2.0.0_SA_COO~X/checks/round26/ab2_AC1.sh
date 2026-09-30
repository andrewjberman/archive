#!/usr/bin/env bash
# AMGT_CORPUS round 26 -- check as a file: ab2_AC1 -- the series-median unit rule: BP PE_RATIO / PROF_MARGIN and every served UNRESOLVED re-read; bands unchanged. Run from the repo root.
cd "$(git rev-parse --show-toplevel)" || exit 2
export PYTHONPATH="$(pwd)"
python org/missions/D5/AMGT/AMGT_CORPUS/deliverables/2.0.0_SA_COO~X/checks/round26/ab2_check.py 2>&1 | grep -E '^ab2 |Error' | tail -1
