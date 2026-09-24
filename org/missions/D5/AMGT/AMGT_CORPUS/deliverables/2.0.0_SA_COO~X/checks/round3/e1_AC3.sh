#!/usr/bin/env bash
# AMGT_CORPUS round 3 -- check as a file (spine v3.19 L6): e1_AC3. Run from the repo root under the worker's timeout.
cd "$(git rev-parse --show-toplevel)" || exit 2
python -m lib.research.corpus.induction_run --fire --as-of 2026-09-24 2>&1 | tail -3
