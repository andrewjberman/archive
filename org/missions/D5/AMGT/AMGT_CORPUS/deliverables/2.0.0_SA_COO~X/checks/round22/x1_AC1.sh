#!/usr/bin/env bash
# AMGT_CORPUS round 22 -- check as a file: x1_AC1 -- would write_one write: the code method against the stored method on three served names. Run from the repo root.
cd "$(git rev-parse --show-toplevel)" || exit 2
export PYTHONPATH="$(pwd)"
python org/missions/D5/AMGT/AMGT_CORPUS/deliverables/2.0.0_SA_COO~X/checks/round22/x1_gate.py 2>&1 | grep -E '^x1 ' | tail -1
