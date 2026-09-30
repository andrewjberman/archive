#!/usr/bin/env bash
# AMGT_CORPUS round 24 -- check as a file: z1_AC1 -- the class table against the checker's own served count and the builder's projected count (slash keys EXCLUDED). Run from the repo root.
cd "$(git rev-parse --show-toplevel)" || exit 2
export PYTHONPATH="$(pwd)"
python org/missions/D5/AMGT/AMGT_CORPUS/deliverables/2.0.0_SA_COO~X/checks/round24/z1_check.py 2>&1 | grep -E '^z1 |Error' | tail -1
