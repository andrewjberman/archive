#!/usr/bin/env bash
# AMGT_CORPUS round 19 -- check as a file: u2_AC1 -- Hitachi's replay through the CLI at HEAD, against the pre-Hitachi map. Run from the repo root.
cd "$(git rev-parse --show-toplevel)" || exit 2
export PYTHONPATH="$(pwd)"
python org/missions/D5/AMGT/AMGT_CORPUS/deliverables/2.0.0_SA_COO~X/checks/round19/u2_replay.py 2>&1 | grep -E '^u2 replay' | tail -1
