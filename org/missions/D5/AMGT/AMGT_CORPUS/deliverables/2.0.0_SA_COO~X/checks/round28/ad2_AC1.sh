#!/usr/bin/env bash
# AMGT_CORPUS round 28 -- check as a file: ad2_AC1 -- the zero-value sign over-refusal: refused fiscal figures over 100 keys, BA's DPS shown, no value/unit/other-sign move. Run from the repo root.
cd "$(git rev-parse --show-toplevel)" || exit 2
export PYTHONPATH="$(pwd)"
python org/missions/D5/AMGT/AMGT_CORPUS/deliverables/2.0.0_SA_COO~X/checks/round28/ad2_check.py 2>&1 | grep -E '^ad2 |Error' | tail -1
