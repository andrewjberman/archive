#!/usr/bin/env bash
# AMGT_CORPUS round 19 -- check as a file: u1_AC2 -- Hitachi's served FY1 BEST_SALES unit against the fixed reader's unit (ruling 1's print). Run from the repo root.
cd "$(git rev-parse --show-toplevel)" || exit 2
export PYTHONPATH="$(pwd)"
python org/missions/D5/AMGT/AMGT_CORPUS/deliverables/2.0.0_SA_COO~X/checks/round19/u1_probe.py 2>&1 | grep -E '^u1 served' | tail -1
