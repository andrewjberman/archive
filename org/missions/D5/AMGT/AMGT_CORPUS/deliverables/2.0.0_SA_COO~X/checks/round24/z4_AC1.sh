#!/usr/bin/env bash
# AMGT_CORPUS round 24 -- check as a file: z4_AC1 -- the static site census (every path-building function references slash_safe_key) with the BP/BRK encoding and the planted refusal. Run from the repo root.
cd "$(git rev-parse --show-toplevel)" || exit 2
export PYTHONPATH="$(pwd)"
python org/missions/D5/AMGT/AMGT_CORPUS/deliverables/2.0.0_SA_COO~X/checks/round24/z4_check.py 2>&1 | grep -E '^z4 |Error' | tail -1
