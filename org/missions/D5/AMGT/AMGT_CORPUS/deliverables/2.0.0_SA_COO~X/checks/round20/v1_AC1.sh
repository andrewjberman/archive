#!/usr/bin/env bash
# AMGT_CORPUS round 20 -- check as a file: v1_AC1 -- the 3.9 floor census (AST) over lib/research/corpus/ and integrations/bloomberg/research/. Run from the repo root.
cd "$(git rev-parse --show-toplevel)" || exit 2
export PYTHONPATH="$(pwd)"
python org/missions/D5/AMGT/AMGT_CORPUS/deliverables/2.0.0_SA_COO~X/checks/round20/v1_census.py 2>&1 | grep -E '^v1 ' | tail -1
