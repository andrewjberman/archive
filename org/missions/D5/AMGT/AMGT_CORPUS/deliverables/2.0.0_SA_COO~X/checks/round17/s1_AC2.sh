#!/usr/bin/env bash
# AMGT_CORPUS round 17 -- check as a file (spine v3.19 L6): s1_AC2 -- the producer chain. Run from the repo root.
cd "$(git rev-parse --show-toplevel)" || exit 2
python org/missions/D5/AMGT/AMGT_CORPUS/deliverables/2.0.0_SA_COO~X/checks/round17/s1_census.py 2>&1 | grep -E '^s1 (producer|census MISSING)'
