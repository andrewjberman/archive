#!/usr/bin/env bash
# AMGT_CORPUS round 23 -- check as a file: y3_AC1 -- the same-currency anchor on TSM's real raw (no TWD line, no FX field stored) and on the SAP control. Run from the repo root.
cd "$(git rev-parse --show-toplevel)" || exit 2
export PYTHONPATH="$(pwd)"
python org/missions/D5/AMGT/AMGT_CORPUS/deliverables/2.0.0_SA_COO~X/checks/round23/y3_anchor.py 2>&1 | grep -E '^y3 |Error' | tail -1
