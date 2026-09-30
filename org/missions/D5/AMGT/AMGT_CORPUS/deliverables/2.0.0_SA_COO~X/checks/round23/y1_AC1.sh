#!/usr/bin/env bash
# AMGT_CORPUS round 23 -- check as a file: y1_AC1 -- the UNRESOLVED-unit census before (served) and after (the round's builder into a temp map) over the same blocks. Run from the repo root.
cd "$(git rev-parse --show-toplevel)" || exit 2
export PYTHONPATH="$(pwd)"
python org/missions/D5/AMGT/AMGT_CORPUS/deliverables/2.0.0_SA_COO~X/checks/round23/y1_census.py 2>&1 | grep -E '^y1 ' | tail -1
