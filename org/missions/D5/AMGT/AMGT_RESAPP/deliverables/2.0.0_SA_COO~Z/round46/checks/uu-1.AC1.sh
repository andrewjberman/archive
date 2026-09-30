#!/usr/bin/env bash
# AMGT_RESAPP round 46 -- check as a file: uu-1 AC1. Run from the repo root.
cd "$(git rev-parse --show-toplevel)" || exit 2
python org/missions/D5/AMGT/AMGT_RESAPP/deliverables/2.0.0_SA_COO~Z/round46/checks/uu1_check.py structure org/missions/D5/AMGT/AMGT_RESAPP/deliverables/0.9.0_WK_AMGT_RESAPP~167
