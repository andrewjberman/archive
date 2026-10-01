#!/usr/bin/env bash
# AMGT_CORPUS round 26 -- check as a file: ab1_AC1 -- the dossier reader resolves the encoded block for BP/NG; a slash-free control is byte-unchanged. Run from the repo root.
cd "$(git rev-parse --show-toplevel)" || exit 2
export PYTHONPATH="$(pwd)"
python org/missions/D5/AMGT/AMGT_CORPUS/deliverables/2.0.0_SA_COO~X/checks/round26/ab1_check.py 2>&1 | grep -E '^ab1 |Error' | tail -1
