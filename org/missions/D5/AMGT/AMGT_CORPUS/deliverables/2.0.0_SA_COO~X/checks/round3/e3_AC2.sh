#!/usr/bin/env bash
# AMGT_CORPUS round 3 -- check as a file (spine v3.19 L6): e3_AC2. Run from the repo root under the worker's timeout.
cd "$(git rev-parse --show-toplevel)" || exit 2
python -m lib.research.corpus.sector_template --write 2>&1 | tail -3
