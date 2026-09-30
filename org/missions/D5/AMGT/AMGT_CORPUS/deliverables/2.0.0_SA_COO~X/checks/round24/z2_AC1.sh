#!/usr/bin/env bash
# AMGT_CORPUS round 24 -- check as a file: z2_AC1 -- TSM's stored-source census and the discriminator's served reason. Run from the repo root.
cd "$(git rev-parse --show-toplevel)" || exit 2
export PYTHONPATH="$(pwd)"
python org/missions/D5/AMGT/AMGT_CORPUS/deliverables/2.0.0_SA_COO~X/checks/round24/z2_check.py 2>&1 | grep -E '^z2 |Error' | tail -1
