#!/usr/bin/env bash
# AMGT_CORPUS round 21 -- check as a file: w1_AC1 -- the pack_shape census over the 96 keys through dossier.pack_shape, with four controls. Run from the repo root.
cd "$(git rev-parse --show-toplevel)" || exit 2
export PYTHONPATH="$(pwd)"
python org/missions/D5/AMGT/AMGT_CORPUS/deliverables/2.0.0_SA_COO~X/checks/round21/w1_check.py 2>&1 | grep -E '^w1 ' | tail -1
