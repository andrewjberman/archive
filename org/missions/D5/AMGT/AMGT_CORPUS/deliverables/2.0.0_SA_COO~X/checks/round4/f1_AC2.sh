#!/usr/bin/env bash
# AMGT_CORPUS round 4 -- check as a file (spine v3.19 L6): f1_AC2. Run from the repo root under the worker's timeout.
cd "$(git rev-parse --show-toplevel)" || exit 2
python -m lib.research.identity.crosswalk --disclosure --as-of "$(date -u +%Y-%m-%d)" 2>&1 | tail -6
