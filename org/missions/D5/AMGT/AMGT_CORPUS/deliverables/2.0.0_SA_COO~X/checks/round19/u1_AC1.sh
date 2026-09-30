#!/usr/bin/env bash
# AMGT_CORPUS round 19 -- check as a file: u1_AC1 -- the scalar-exception readers on the REAL committed map (6501 BEST_SALES), with the 8035 control and the Z-W1-S18 module guard. Run from the repo root.
cd "$(git rev-parse --show-toplevel)" || exit 2
export PYTHONPATH="$(pwd)"
python org/missions/D5/AMGT/AMGT_CORPUS/deliverables/2.0.0_SA_COO~X/checks/round19/u1_probe.py 2>&1 | grep -E '^u1 reader' | tail -1
