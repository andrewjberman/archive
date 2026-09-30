#!/usr/bin/env bash
# AMGT_CORPUS round 20 -- check as a file: v2_AC1 -- the evidence file's structure: 6 rows, both halves, signed-out control, disarm. Run from the repo root.
cd "$(git rev-parse --show-toplevel)" || exit 2
export PYTHONPATH="$(pwd)"
python org/missions/D5/AMGT/AMGT_CORPUS/deliverables/2.0.0_SA_COO~X/checks/round20/v2_check.py structure org/missions/D5/AMGT/AMGT_CORPUS/deliverables/0.9.0_WK_AMGT_CORPUS~2/FWD_EVIDENCE_ROUND20.json 2>&1 | tail -2
