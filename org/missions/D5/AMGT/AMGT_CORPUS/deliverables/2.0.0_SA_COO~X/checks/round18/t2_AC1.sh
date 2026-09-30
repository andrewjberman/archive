#!/usr/bin/env bash
# AMGT_CORPUS round 18 -- check as a file: t2_AC1 -- Hitachi's replay at HEAD. Run from the repo root.
cd "$(git rev-parse --show-toplevel)" || exit 2
export PYTHONPATH="$(pwd)"
python org/missions/D5/AMGT/AMGT_CORPUS/deliverables/2.0.0_SA_COO~X/checks/round18/t2_replay.py 2>&1 | grep -E '^t2 replay' | tail -1
